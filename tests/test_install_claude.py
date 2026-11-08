"""Install checks for the Claude Code adapter."""

import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def install(*args, home):
    return subprocess.run(
        ["bash", str(ROOT / "install.sh"), *args],
        env={**os.environ, "HOME": str(home)},
        capture_output=True,
        text=True,
        check=True,
        timeout=60,
    )


class ClaudeAdapterTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.home = Path(tmp.name) / "home"
        self.dest = Path(tmp.name) / "project"
        self.home.mkdir()

    def test_project_install_loads_rules_and_routes_review(self):
        install("--dest", str(self.dest), "--slurm", "--agent", "claude", home=self.home)
        self.assertEqual(
            (self.dest / "CLAUDE.md").read_text().split(),
            ["@AGENTS.md", "@.claude/rules/research-rigor.md"],
        )
        rigor = (self.dest / ".claude/rules/research-rigor.md").read_text()
        self.assertIn("Think Wide First", rigor)
        self.assertTrue((self.dest / ".claude/skills/shared-references/experiment-integrity.md").is_file())
        self.assertTrue((self.dest / "AGENTS.md").is_file())
        self.assertIn("codex", (self.dest / ".claude/agents/reviewer.md").read_text())
        routing = (self.dest / ".claude/skills/research-review/SKILL.md").read_text()
        self.assertIn("`reviewer` agent", routing)
        self.assertNotIn("installed agent adapter", routing)

    def test_installed_hook_denies_unledgered_training_launch(self):
        install("--dest", str(self.dest), "--slurm", "--agent", "claude", home=self.home)
        experiments = self.dest / "docs/experiments"
        (experiments / "contracts/EXP-T.json").write_text(
            json.dumps(
                {
                    "experiment_id": "EXP-T",
                    "allowed_launchers": ["scripts/slurm_train_demo.sh"],
                }
            )
        )
        (experiments / "registry.json").write_text(
            json.dumps(
                {
                    "experiments": [
                        {
                            "id": "EXP-T",
                            "contract_path": "docs/experiments/contracts/EXP-T.json",
                        }
                    ]
                }
            )
        )
        settings = json.loads((self.dest / ".claude/settings.json").read_text())
        command = settings["hooks"]["PreToolUse"][0]["hooks"][0]["command"]
        env = {**os.environ, "CLAUDE_PROJECT_DIR": str(self.dest)}

        def run_hook(bash_command):
            payload = {
                "hook_event_name": "PreToolUse",
                "cwd": str(self.dest),
                "tool_input": {"command": bash_command},
            }
            return subprocess.run(
                ["bash", "-c", command],
                input=json.dumps(payload),
                env=env,
                capture_output=True,
                text=True,
                check=True,
                timeout=30,
            ).stdout.strip()

        denied = json.loads(run_hook("scripts/slurm_train_demo.sh --epochs 1"))
        self.assertEqual(denied["hookSpecificOutput"]["permissionDecision"], "deny")
        self.assertEqual(run_hook("squeue -u someone"), "")

    def test_existing_project_files_are_kept(self):
        (self.dest / ".claude").mkdir(parents=True)
        (self.dest / ".claude/settings.json").write_text('{"permissions": {}}\n')
        (self.dest / "CLAUDE.md").write_text("mine\n")
        done = install("--dest", str(self.dest), "--slurm", "--agent", "claude", home=self.home)
        self.assertEqual((self.dest / ".claude/settings.json").read_text(), '{"permissions": {}}\n')
        self.assertEqual(
            (self.dest / "CLAUDE.md").read_text(), "mine\n\n@.claude/rules/research-rigor.md\n"
        )
        self.assertIn("kept existing", done.stderr)
        install("--dest", str(self.dest), "--slurm", "--agent", "claude", home=self.home)
        self.assertEqual((self.dest / "CLAUDE.md").read_text().count("research-rigor"), 1)

    def test_personal_install_writes_skills_and_reviewer(self):
        install("--personal", "--core", "--agent", "claude", home=self.home)
        self.assertTrue((self.home / ".claude/agents/reviewer.md").is_file())
        routing = (self.home / ".claude/skills/shared-references/reviewer-routing.md").read_text()
        self.assertIn("`reviewer` agent", routing)


if __name__ == "__main__":
    unittest.main()
