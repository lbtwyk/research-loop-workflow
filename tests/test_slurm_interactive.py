"""Regression checks for Isambard reservation routing and hidden visibility."""

import importlib.util
import subprocess
import unittest
from pathlib import Path


SCRIPTS = Path(__file__).resolve().parents[1] / "packs/slurm/scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


preflight = load("training_preflight")
snapshot_module = load("slurm_state_snapshot")


class InteractiveTests(unittest.TestCase):
    def test_reservation_only_command_and_isolated_reuse_are_valid(self):
        for command in (
            "srun --account=brics.u6ym --reservation=interactive --immediate=10 --ntasks=1 true",
            "srun --jobid=123 --exact --exclusive --ntasks=1 true",
        ):
            preflight._validate_interactive_srun(command, label="check")

    def test_partition_and_qos_override_are_rejected(self):
        for option in ("--partition=workq", "--partition workq", "-p workq", "--qos=normal", "-q normal"):
            with self.subTest(option=option), self.assertRaisesRegex(
                preflight.PreflightError, "select its partition"
            ):
                preflight._validate_interactive_srun(
                    "srun --reservation=interactive --immediate=10 --ntasks=1 "
                    + option + " true", label="check"
                )

    def test_configuration_and_started_program_failures_are_not_skips(self):
        for message in (
            "Unable to allocate resources: Invalid reservation",
            "Unable to allocate resources: Access denied",
            "Unable to allocate resources: Requested node configuration is not available",
            "job 123 has been allocated resources\nRequested nodes are busy",
        ):
            with self.subTest(message=message):
                self.assertFalse(preflight.gpu_allocation_unavailable("", message))
        self.assertTrue(preflight.gpu_allocation_unavailable(
            "", "Unable to allocate resources: Requested nodes are busy"
        ))

    def test_snapshot_requests_hidden_resources_and_retains_privacy(self):
        commands = []

        def runner(command):
            commands.append(command)
            if command[0] in {"squeue", "sinfo"}:
                self.assertIn("--all", command)
            output = ""
            if command[0] == "sinfo":
                output = "interactive|up|08:00:00|50|mix|gpu:4\n"
            elif command[:3] == ["scontrol", "show", "config"]:
                output = "PrivateData = accounts,jobs,users\n"
            return subprocess.CompletedProcess(command, 0, output, "")

        result = snapshot_module.collect_snapshot(user="test", runner=runner)
        self.assertEqual(result["partitions"][0]["partition"], "interactive")
        self.assertEqual(result["strategy_input"]["scheduler_config"]["PrivateData"], "accounts,jobs,users")


if __name__ == "__main__":
    unittest.main()
