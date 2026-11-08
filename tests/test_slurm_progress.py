"""Progress at the scheduler/log seam, without launching or modifying jobs."""

import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SCRIPTS = ROOT / "packs/slurm/scripts"
if not DEFAULT_SCRIPTS.is_dir():
    DEFAULT_SCRIPTS = ROOT / "scripts"
SCRIPTS = Path(os.environ.get("SLURM_SCRIPTS_UNDER_TEST", DEFAULT_SCRIPTS))
with mock.patch.object(sys, "path", [str(SCRIPTS), *sys.path]):
    spec = importlib.util.spec_from_file_location("progress", SCRIPTS / "slurm_progress.py")
    progress = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(progress)


class ProgressTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.log = self.root / "train log.out"
        self.log.write_text('{"step": 20, "total": 100, "stage": "generator", "training_eta_hours": 2.5}\n')
        self.commands = []

    def runner(self, command):
        self.commands.append(command)
        if command[0] == "squeue":
            self.assertIn("--all", command)
            self.assertIn("--array", command)
            output = "101|train|RUNNING|00:10|01:00|nid1\n202_0|array|PENDING|0:00|01:00|Dependency\n202_1|array|PENDING|0:00|01:00|Dependency\n"
        elif command[0] == "scontrol":
            output = f"JobId={command[-1]} Reason=Dependency WorkDir={self.root} StdOut={self.log} StdErr= ExitCode=0:0\n"
        elif command[0] == "sacct":
            self.assertIn("-X", command)
            output = f"99|99|old|COMPLETED|01:00|02:00|0:0|{self.root}|train log.out|\n"
        else:
            self.fail(f"Unexpected/mutating command: {command}")
        return subprocess.CompletedProcess(command, 0, output, "")

    def collect(self, **kwargs):
        return progress.collect_progress(user="test", runner=self.runner, **kwargs)

    def test_live_progress_and_pending_arrays_are_separate(self):
        report = self.collect()
        self.assertEqual(report["status"], "ok")
        self.assertEqual([j["job_id"] for j in report["jobs"]], ["101", "202_0", "202_1"])
        self.assertEqual(report["jobs"][0]["progress"]["percent"], 20)
        self.assertIsNone(report["jobs"][1]["progress"])
        self.assertEqual(report["jobs"][1]["reason"], "Dependency")
        self.assertFalse(any(c[0] == "sacct" for c in self.commands))
        self.assertIn("'", report["jobs"][0]["follow_commands"][0])

    def test_array_parent_filter_keeps_all_elements(self):
        report = self.collect(job_ids=["202"])
        self.assertEqual([j["job_id"] for j in report["jobs"]], ["202_0", "202_1"])

    def test_finished_job_falls_back_to_accounting_and_relative_log(self):
        report = self.collect(job_ids=["99"])
        job = report["jobs"][0]
        self.assertEqual(job["state_source"], "sacct")
        self.assertEqual(job["stdout"], str(self.log))
        self.assertEqual(job["progress"]["step"], 20)
        # Scheduler COMPLETED does not turn a 20% log into 100% training.
        self.assertEqual(job["progress"]["percent"], 20)
        self.assertNotIn("training ETA:", progress.format_report(report))

    def test_history_does_not_override_live_state(self):
        report = self.collect(history=True)
        self.assertEqual(len(report["jobs"]), 4)
        self.assertEqual(report["jobs"][0]["state_source"], "squeue")

    def test_unknown_job_is_partial_not_empty_success(self):
        report = self.collect(job_ids=["404"])
        self.assertEqual(report["status"], "partial")
        self.assertEqual(report["unresolved_job_ids"], ["404"])

    def test_scheduler_error_is_not_no_jobs(self):
        def failing(command):
            return subprocess.CompletedProcess(command, 1, "", "controller unavailable")
        report = progress.collect_progress(user="test", runner=failing)
        self.assertEqual(report["status"], "partial")
        self.assertIn("controller unavailable", progress.format_report(report))

    def test_missing_scheduler_is_reported(self):
        def missing(command):
            raise FileNotFoundError(command[0])
        report = progress.collect_progress(user="test", runner=missing)
        self.assertEqual(report["status"], "partial")

    def test_stderr_progress_and_missing_log_are_explicit(self):
        with mock.patch.object(progress, "resolve_log", side_effect=lambda value, *args: (
            str(self.log) if value == "" else str(self.root / "missing")
        )):
            job = self.collect(job_ids=["101"])["jobs"][0]
        self.assertEqual(job["logs"]["stdout"]["status"], "unavailable")
        self.assertEqual(job["progress"]["percent"], 20)

    def test_tail_is_bounded_and_ignores_partial_json(self):
        self.log.write_text("x" * 200000 + '\n{"step": 30, "total_steps": 100}\n{"step": 40')
        log = progress.read_log(str(self.log), 2)
        self.assertEqual(log["progress"]["step"], 30)
        self.assertLess(len("\n".join(log["tail"])), 131072)

    def test_invalid_and_unstructured_progress_remains_unknown(self):
        for record in ("loading cache", "[]", '{"step": true, "total": 100}',
                       '{"step": 200, "total": 100}', '{"step": 1, "total": 0}'):
            self.log.write_text(record + "\n")
            self.assertIsNone(progress.read_log(str(self.log), 80)["progress"])

    def test_invalid_eta_is_not_reported(self):
        self.log.write_text('{"step": 20, "total": 100, "training_eta_hours": NaN}\n')
        log = progress.read_log(str(self.log), 80)
        self.assertIsNone(log["progress"]["training_eta_hours"])
        json.dumps(log, allow_nan=False)

    def test_accounting_array_templates_preserve_numeric_job_identity(self):
        self.assertEqual(progress.resolve_log("%A_%a-%j.out", "202_1", "/logs", "203"), "/logs/202_1-203.out")
        self.assertIsNone(progress.resolve_log("%j.out", "202_1", "/logs"))
        self.assertIsNone(progress.resolve_log("%N.out", "202_1", "/logs"))
        self.assertIsNone(progress.resolve_log("relative.out", "99", "Unknown"))

    def test_cli_json_and_failure_exit_code(self):
        with mock.patch.object(progress, "collect_progress", return_value=self.collect(job_ids=["404"])), redirect_stdout(io.StringIO()) as output:
            self.assertEqual(progress.main(["404", "--json"]), 1)
        self.assertEqual(json.loads(output.getvalue())["unresolved_job_ids"], ["404"])


if __name__ == "__main__":
    unittest.main()
