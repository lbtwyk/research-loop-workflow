#!/usr/bin/env python3
"""Core ledger commands that must work without the slurm pack."""

from __future__ import annotations

import importlib.util
import json
import os
import tempfile
import unittest
from pathlib import Path


def load_ledger():
    path = Path(__file__).resolve().parents[1] / "scripts" / "experiment_ledger.py"
    spec = importlib.util.spec_from_file_location("experiment_ledger", path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


ledger = load_ledger()


class CoreLedgerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tempdir = tempfile.TemporaryDirectory()
        self.root = Path(self.tempdir.name)
        (self.root / ".git").mkdir()
        experiments = self.root / "docs/experiments"
        experiments.mkdir(parents=True)
        (experiments / "registry.json").write_text(
            json.dumps(
                {
                    "schema_version": 1,
                    "updated_at": "",
                    "source_import": "",
                    "experiments": [],
                    "supplemental_documents": [],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        (experiments / "EXP-20260902-demo.md").write_text(
            "# EXP-20260902-demo\n\nStatus: draft\n\n"
            "## Intent Anchor\n\n- Goal: prove the ledger works without a scheduler.\n"
            "- Why: core pack must stand alone.\n"
            "- Leading advantage / Proof role: establish the method.\n"
            "- Must remain true: no scheduler import.\n"
            "- Completion evidence: generated ACTIVE and INDEX.\n"
            "- Non-goals: training launch.\n\n"
            "## Current Route\n\nCore-only demo.\n\n"
            "## Current Execution Snapshot\n\nNot required.\n\n"
            "## Current Conclusion and Next Action\n\nDraft.\n",
            encoding="utf-8",
        )
        self.addCleanup(self.tempdir.cleanup)
        self.previous = Path.cwd()
        os.chdir(self.root)
        self.addCleanup(os.chdir, self.previous)

    def test_add_outline_sync_lint(self) -> None:
        self.assertEqual(
            ledger.main(
                [
                    "add",
                    "EXP-20260902-demo",
                    "--core-change",
                    "Core-only ledger demo",
                    "--next-action",
                    "Keep as example",
                ]
            ),
            0,
        )
        self.assertEqual(ledger.main(["outline", "EXP-20260902-demo"]), 0)
        self.assertEqual(ledger.main(["sync"]), 0)
        self.assertEqual(ledger.main(["lint"]), 0)
        registry = json.loads(
            (self.root / "docs/experiments/registry.json").read_text(encoding="utf-8")
        )
        self.assertEqual(registry["experiments"][0]["id"], "EXP-20260902-demo")
        self.assertTrue((self.root / "docs/experiments/ACTIVE.md").is_file())
        self.assertTrue((self.root / "docs/experiments/INDEX.md").is_file())

    def test_launch_without_slurm_pack_refuses(self) -> None:
        ledger.slurm_state_snapshot = None
        ledger.training_preflight = None
        with self.assertRaises(ledger.LedgerError):
            ledger.load_scheduler_adapters()


if __name__ == "__main__":
    unittest.main()
