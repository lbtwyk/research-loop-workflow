"""Resource observation and near-fastest selection, without live Slurm jobs."""

import copy
import importlib.util
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from contextlib import ExitStack, redirect_stdout
from types import SimpleNamespace
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = Path(os.environ.get("SLURM_SCRIPTS_UNDER_TEST", ROOT / "packs/slurm/scripts"))


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


snapshot = load("slurm_state_snapshot")
policy = load("slurm_resource_policy")


def candidate(identifier, seconds, cost, **extra):
    return {
        "id": identifier, "feasible": True,
        "time_to_result_seconds": seconds, "cost_nhr": cost,
        "evidence": ["Matched runtime and actual billing; queue wait is estimated"],
        **extra,
    }


def comparison(*candidates, **extra):
    return {
        "schema_version": 1,
        "comparison_basis": "same frozen contract and all remaining declared results",
        "candidates": list(candidates), **extra,
    }


class ResourcePolicyTests(unittest.TestCase):
    def test_next_boundary_recomputes_changed_throughput_and_switch_cost(self):
        payload = comparison(candidate("ordinary", 100, 10), candidate("shared", 110, 6))
        self.assertEqual(policy.select_resources(payload)["selected_candidate_id"], "shared")
        payload["candidates"][1]["time_to_result_seconds"] = 130
        payload["candidates"][1]["evidence"] = ["new stable runtime plus restart/requeue overhead"]
        self.assertEqual(policy.select_resources(payload)["selected_candidate_id"], "ordinary")

    def test_known_hard_violation_is_not_hidden_by_another_missing_metric(self):
        for payload in (
            comparison(candidate("over-budget", None, 10), cost_budget_nhr=5),
            comparison(candidate("late", 100, None), deadline_seconds=50),
        ):
            self.assertEqual(policy.select_resources(payload)["status"], "infeasible")

    def test_default_ten_percent_selects_cheaper_inclusive_boundary(self):
        result = policy.select_resources(comparison(
            candidate("fast", 100, 10), candidate("balanced", 110, 6),
            candidate("too-slow", 111, 4), candidate("dominated", 109, 12),
        ))
        self.assertEqual(result["selected_candidate_id"], "balanced")
        self.assertEqual(result["fastest_candidate_id"], "fast")
        self.assertAlmostEqual(result["time_limit_seconds"], 110)
        self.assertNotIn("dominated", result["pareto_candidate_ids"])
        self.assertEqual(result["slowdown_tolerance"], 0.10)
        self.assertTrue(result["advisory"])

    def test_explicit_tolerance_and_cli_override(self):
        payload = comparison(candidate("fast", 100, 10), candidate("cheap", 120, 5), slowdown_tolerance=0.20)
        self.assertEqual(policy.select_resources(payload)["selected_candidate_id"], "cheap")
        self.assertEqual(policy.select_resources(payload, slowdown_tolerance=0)["selected_candidate_id"], "fast")

    def test_budget_and_deadline_filter_before_fastest_reference(self):
        result = policy.select_resources(comparison(
            candidate("over-budget", 50, 20), candidate("late", 110, 2),
            candidate("fits", 100, 6), cost_budget_nhr=10, deadline_seconds=105,
        ))
        self.assertEqual(result["selected_candidate_id"], "fits")
        self.assertEqual(result["fastest_candidate_id"], "fits")
        self.assertEqual(len(result["excluded"]), 2)

    def test_equal_cost_prefers_faster_then_stable_identifier(self):
        result = policy.select_resources(comparison(
            candidate("z", 100, 5), candidate("a", 100, 5), candidate("slow", 105, 5),
        ))
        self.assertEqual(result["selected_candidate_id"], "a")

    def test_unknown_is_not_zero_cost_or_zero_time(self):
        payload = comparison(candidate("unknown", None, None))
        result = policy.select_resources(payload)
        self.assertEqual(result["status"], "unknown")
        self.assertIsNone(result["selected_candidate_id"])
        payload["candidates"].append(candidate("known", 100, 5))
        result = policy.select_resources(payload)
        self.assertEqual(result["selected_candidate_id"], "known")
        self.assertEqual(result["unranked"][0]["id"], "unknown")

    def test_missing_evidence_cannot_win(self):
        result = policy.select_resources(comparison(
            candidate("unsupported", 1, 0, evidence=[]), candidate("known", 100, 5),
        ))
        self.assertEqual(result["selected_candidate_id"], "known")
        self.assertIn("evidence", result["unranked"][0]["missing"])

    def test_infeasible_and_exhausted_budget_have_no_selection(self):
        for payload in (
            comparison(candidate("unsafe", 1, 0, feasible=False, reason="real-time clock failure")),
            comparison(candidate("over-budget", 100, 5), cost_budget_nhr=4),
        ):
            self.assertEqual(policy.select_resources(payload)["status"], "infeasible")

    def test_invalid_numeric_inputs_are_rejected(self):
        for value in (True, -1, float("nan"), float("inf"), "10"):
            with self.subTest(value=value), self.assertRaises(ValueError):
                policy.select_resources(comparison(candidate("bad", 100, value)))
        for key in ("slowdown_tolerance", "cost_budget_nhr", "deadline_seconds"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                policy.select_resources(comparison(candidate("a", 100, 5), **{key: -1}))

    def test_comparison_and_feasibility_must_be_explicit(self):
        for payload in (
            {"schema_version": 1, "candidates": []},
            comparison(candidate("a", 100, 5, feasible="yes")),
            comparison(candidate("a", 100, 5), candidate("a", 110, 4)),
        ):
            with self.assertRaises(ValueError):
                policy.select_resources(payload)

    def test_selection_does_not_modify_input(self):
        payload = comparison(candidate("a", 100, 5))
        before = copy.deepcopy(payload)
        policy.select_resources(payload)
        self.assertEqual(payload, before)


class SnapshotObservationTests(unittest.TestCase):
    def runner(self, command):
        output = ""
        if command[0] == "squeue":
            self.assertIn("--all", command)
            self.assertIn("--array", command)
            output = "101|workq|worker|RUNNING|00:10|01:00|1|nid1|normal|gpu:1|8|24G\n202_0|workq|array|PENDING|0:00|01:00|1|Dependency|normal|gpu:1|8|24G\n202_1|workq|array|PENDING|0:00|01:00|1|Dependency|normal|gpu:1|8|24G\n"
        elif command[:3] == ["scontrol", "show", "job"]:
            identifier = command[-1]
            self.assertNotIn("[", identifier)
            state = "RUNNING" if identifier == "101" else "PENDING"
            allocation = "cpu=72,billing=72,gres/gpu=1,gres/gpu:gh200=1" if identifier == "101" else "(null)"
            output = f"JobId={identifier} JobState={state} Reason=Dependency NumNodes=1 NumCPUs=72 AllocTRES={allocation} ReqTRES=cpu=8,gres/gpu=1 BatchFlag=1\n"
        elif command[:3] == ["scontrol", "show", "step"]:
            output = "StepId=101.batch Name=batch TRES=(null)\nStepId=101.0 Name=python TRES=cpu=8,gres/gpu=1,gres/gpu:gh200=1\n"
        elif command[0] == "sacct":
            self.assertNotIn("-X", command)
            output = "100|old|workq|normal|COMPLETED|01:00|02:00|cpu=72,gres/gpu=1,billing=72||0:0|72|00:30|gres/gpuutil=80|gres/gpumem=1024M\n100.batch|batch|workq|normal|COMPLETED|01:00|02:00|cpu=72||0:0\n100.0|python|workq|normal|COMPLETED|01:00|02:00|cpu=8|1048576K|0:0|8|00:30|gres/gpuutil=80|gres/gpumem=1024M\n"
        elif command[:3] == ["scontrol", "show", "config"]:
            output = "PrivateData = jobs,users\nPriorityWeightFairShare = 0\n"
        return subprocess.CompletedProcess(command, 0, output, "")

    def test_arrays_keep_each_element_resource_identity(self):
        result = snapshot.collect_snapshot(user="test", runner=self.runner)
        self.assertEqual([job["job_id"] for job in result["jobs"]], ["101", "202_0", "202_1"])
        self.assertEqual(result["jobs"][1]["requested_gpus"], 1)
        self.assertEqual(result["strategy_input"]["pending_reason_counts"], {"Dependency": 2})

    def test_step_statistics_are_separate_from_allocation_history(self):
        result = snapshot.collect_snapshot(user="test", runner=self.runner)
        self.assertEqual(len(result["recent_jobs"]), 1)
        self.assertEqual(len(result["recent_steps"]), 2)
        self.assertIsNone(result["recent_jobs"][0]["max_rss"])
        self.assertIsNone(result["recent_steps"][0]["max_rss"])
        self.assertEqual(result["recent_steps"][1]["max_rss"], "1048576K")
        self.assertEqual(result["recent_steps"][1]["allocation_id"], "100")
        self.assertEqual(result["recent_steps"][1]["tres_usage_in_ave"], "gres/gpuutil=80")

    def test_generic_and_typed_gpu_tres_are_not_double_counted(self):
        self.assertEqual(snapshot.gpu_count("gres/gpu=2,gres/gpu:gh200=2"), 2)
        self.assertEqual(snapshot.gpu_count("gres/gpu:a=1,gres/gpu:b=2"), 3)
        self.assertEqual(snapshot.gpu_count("cpu=8,mem=24G"), 0)
        self.assertIsNone(snapshot.gpu_count("(null)"))
        result = snapshot.collect_snapshot(user="test", runner=self.runner)
        self.assertEqual(result["strategy_input"]["running_allocations"][0]["committed_step_gpus"], 1)

    def test_failed_source_stdout_is_not_used_as_valid_data(self):
        def runner(command):
            if command[0] == "sacct":
                return subprocess.CompletedProcess(command, 1, "100|misleading\n", "query failed")
            return self.runner(command)
        result = snapshot.collect_snapshot(user="test", runner=runner)
        self.assertEqual(result["recent_jobs"], [])
        self.assertEqual(result["recent_steps"], [])
        self.assertEqual(result["sources"]["recent_jobs"]["status"], "unavailable")

    def test_unknown_step_usage_does_not_offer_free_dispatcher_gpus(self):
        for failed in (True, False):
            with self.subTest(failed=failed), tempfile.TemporaryDirectory() as temporary:
                ready = Path(temporary) / "101/ready.json"
                ready.parent.mkdir()
                ready.write_text('{"job_id": "101"}')
                def runner(command):
                    if command[:3] == ["scontrol", "show", "step"]:
                        return subprocess.CompletedProcess(command, int(failed), "StepId=101.0 Name=python TRES=(null)\n", "unavailable" if failed else "")
                    return self.runner(command)
                with mock.patch.dict(os.environ, {
                    "RESEARCH_LOOP_INTERACTIVE_DISPATCH_ROOT": temporary,
                    "M2D_INTERACTIVE_DISPATCH_ROOT": temporary,
                }):
                    result = snapshot.collect_snapshot(user="test", runner=runner)
                allocation = result["strategy_input"]["running_allocations"][0]
                self.assertTrue(allocation["dispatcher_ready"])
                self.assertIsNone(allocation["committed_step_gpus"])
                self.assertIsNone(allocation["reusable_gpus"])

    def test_capture_interval_and_live_priority_facts_are_retained(self):
        result = snapshot.collect_snapshot(user="test", runner=self.runner)
        self.assertLessEqual(result["capture_started_at"], result["captured_at"])
        self.assertEqual(result["strategy_input"]["scheduler_config"]["PriorityWeightFairShare"], "0")


class InstalledPolicyTests(unittest.TestCase):
    def test_launch_packet_keeps_exact_command_and_existing_gates(self):
        ledger_path = SCRIPTS / "experiment_ledger.py"
        if not ledger_path.is_file():
            ledger_path = ROOT / "packs/core/scripts/experiment_ledger.py"
        spec = importlib.util.spec_from_file_location("resource_test_ledger", ledger_path)
        ledger = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(ledger)
        item = {"id": "EXP-20261018-resource-test", "lifecycle": "ready"}
        config = {"allowed_launchers": ["scripts/train.py"], "execution_kind": "training"}
        command = ["python", "scripts/train.py", "--frozen"]
        args = SimpleNamespace(experiment_id=item["id"], scope="train", launch_command=["--", *command], slurm_snapshot="snapshot.json", resource_candidates="candidates.json", slowdown_tolerance=None, output=None)
        with tempfile.TemporaryDirectory() as temporary, ExitStack() as stack:
            root = Path(temporary)
            (root / "snapshot.json").write_text(json.dumps({"schema_version": 1, "captured_at": "now", "jobs": [], "recent_jobs": []}))
            (root / "candidates.json").write_text(json.dumps(comparison(candidate("fast", 100, 10), candidate("balanced", 110, 6), snapshot_captured_at="now")))
            stack.enter_context(mock.patch.dict(sys.modules, {"slurm_resource_policy": policy, "scripts.slurm_resource_policy": policy}))
            for name, value in {
                "load_registry": {}, "find_experiment": item,
                "contract_errors": ([], config), "resolve_launch_scope": ("train", config),
                "launch_review_gate": (True, "ok", "basis"), "review_is_current": (True, "ok", "basis"),
                "operational_is_current": (True, "ok", "basis"),
                "current_preflight_receipt": ("passed", None, None),
                "compile_stage_closure": {"stages": [{"stage": "train", "state": "not_launched", "depends_on": []}]},
            }.items():
                stack.enter_context(mock.patch.object(ledger, name, return_value=value))
            scheduler = stack.enter_context(mock.patch.object(ledger.subprocess, "run", side_effect=AssertionError("read-only packet must not execute commands")))
            output = io.StringIO()
            with redirect_stdout(output):
                ledger.command_launch_packet(root, args)
            packet = json.loads(output.getvalue())
            self.assertEqual(packet["resource_selection"]["selected_candidate_id"], "balanced")
            self.assertEqual(packet["launch"]["command"], command)
            self.assertTrue(packet["launch"]["ready"])
            scheduler.assert_not_called()
            args.resource_candidates = None
            self.assertIsNone(ledger.compile_resource_selection(root, args, None))
            args.resource_candidates = "candidates.json"
            with self.assertRaisesRegex(ledger.LedgerError, "requires --slurm-snapshot"):
                ledger.compile_resource_selection(root, args, None)

    def test_install_includes_cli_and_read_only_ledger_integration(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["bash", str(ROOT / "install.sh"), "--dest", str(root), "--slurm", "--agent", "codex"], check=True, capture_output=True)
            self.assertTrue((root / ".agents/skills/research-experiment-spec/SLURM.md").is_file())
            payload = comparison(candidate("fast", 100, 10), candidate("balanced", 110, 5), snapshot_captured_at="2026-10-18T00:00:00+00:00")
            (root / "candidates.json").write_text(json.dumps(payload))
            cli = subprocess.run([sys.executable, "scripts/slurm_resource_policy.py", "candidates.json"], cwd=root, text=True, capture_output=True, check=True)
            self.assertEqual(json.loads(cli.stdout)["selected_candidate_id"], "balanced")
            code = "from scripts import experiment_ledger as l; from pathlib import Path; from types import SimpleNamespace; import json; a=SimpleNamespace(resource_candidates='candidates.json',slowdown_tolerance=None); print(json.dumps(l.compile_resource_selection(Path.cwd(),a,{'captured_at':'2026-10-18T00:00:00+00:00'})))"
            result = subprocess.run([sys.executable, "-c", code], cwd=root, text=True, capture_output=True, check=True)
            self.assertEqual(json.loads(result.stdout)["selected_candidate_id"], "balanced")
            mismatch = subprocess.run([sys.executable, "-c", code.replace("00:00:00+00:00", "01:00:00+00:00")], cwd=root, text=True, capture_output=True)
            self.assertNotEqual(mismatch.returncode, 0)
            self.assertIn("snapshot_captured_at", mismatch.stderr)
            help_result = subprocess.run([sys.executable, "scripts/experiment_ledger.py", "launch-packet", "--help"], cwd=root, text=True, capture_output=True, check=True)
            self.assertIn("--resource-candidates", help_result.stdout)


if __name__ == "__main__":
    unittest.main()
