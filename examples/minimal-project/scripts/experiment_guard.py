#!/usr/bin/env python3
"""Guard contract-matched training launches without injecting thread focus."""

from __future__ import annotations

import json
import shlex
import sys
from pathlib import Path
from typing import Any


def project_root(cwd: object) -> Path | None:
    try:
        current = Path(str(cwd)).resolve() if cwd else Path.cwd().resolve()
    except OSError:
        return None
    for candidate in (current, *current.parents):
        if (candidate / "docs/experiments/registry.json").is_file():
            return candidate
    return None


def load_registry(root: Path) -> dict[str, Any] | None:
    try:
        return json.loads(
            (root / "docs/experiments/registry.json").read_text(encoding="utf-8")
        )
    except (OSError, json.JSONDecodeError):
        return None


def contract_items(
    root: Path, registry: dict[str, Any]
) -> list[dict[str, Any]]:
    experiments = registry.get("experiments", [])
    if not isinstance(experiments, list):
        experiments = []
    registered = [
        item
        for item in experiments
        if isinstance(item, dict)
        and isinstance(item.get("id"), str)
        and isinstance(item.get("contract_path"), str)
    ]
    items_by_id = {str(item["id"]): item for item in registered}
    contracts_dir = root / "docs/experiments/contracts"
    for path in sorted(contracts_dir.glob("*.json")):
        try:
            contract = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        experiment_id = contract.get("experiment_id")
        if not isinstance(experiment_id, str) or not experiment_id:
            continue
        relative_path = path.relative_to(root).as_posix()
        item = items_by_id.setdefault(experiment_id, {"id": experiment_id})
        item.setdefault("contract_path", relative_path)
    return list(items_by_id.values())


def shell_words(command: str) -> list[list[str]]:
    commands: list[list[str]] = []
    try:
        lexer = shlex.shlex(
            command.replace("\n", ";"), posix=True, punctuation_chars=";&|"
        )
        lexer.whitespace_split = True
        lexer.commenters = "#"
        tokens = list(lexer)
    except ValueError:
        return commands
    current: list[str] = []
    for token in tokens:
        if token and all(character in ";&|" for character in token):
            if current:
                commands.append(current)
                current = []
            continue
        current.append(token)
    if current:
        commands.append(current)
    return commands


def executable_index(words: list[str]) -> int | None:
    index = 0
    while index < len(words) and (
        "=" in words[index] and not words[index].startswith(("/", "./"))
    ):
        name = words[index].split("=", 1)[0]
        if not name.replace("_", "").isalnum():
            break
        index += 1
    return index if index < len(words) else None


def is_safe_probe(words: list[str]) -> bool:
    safe_flags = {"--dry-run", "--test-only", "--smoke", "--smoke-test"}
    return any(word in safe_flags for word in words)


def is_direct_training_launch(
    words: list[str], training_markers: set[str] | None = None
) -> bool:
    if is_safe_probe(words):
        return False
    index = executable_index(words)
    if index is None:
        return False
    if training_markers:
        normalized = {word.removeprefix("./") for word in words}
        if normalized & training_markers:
            return True
    executable = Path(words[index]).name
    tail = words[index + 1 :]
    if executable == "sbatch":
        lowered = [token.lower() for token in tail]
        for token in lowered:
            path = Path(token)
            name = path.name
            parts = path.parts
            if name.startswith(
                (
                    "slurm_eval_",
                    "slurm_render_",
                    "slurm_select_",
                    "eval_",
                    "render_",
                    "select_",
                )
            ):
                continue
            if name.startswith(("slurm_train_", "train_")):
                return True
            if name.startswith("slurm_launch_"):
                return not any(
                    marker in name for marker in ("eval", "render", "select")
                )
            if any(
                part in {"train", "training"} or part.startswith("train_")
                for part in parts[:-1]
            ):
                return True
        return False
    if executable == "srun":
        return any(
            token == "torchrun"
            or Path(token).name.startswith("train_")
            or token.endswith("/accelerate")
            for token in tail
        )
    if executable == "torchrun":
        return True
    if executable == "accelerate":
        return bool(tail and tail[0] == "launch")
    if executable.startswith("python"):
        return any(Path(token).name.startswith("train_") for token in tail)
    if executable in {"bash", "sh"}:
        for token in tail:
            name = Path(token).name.lower()
            if name.startswith("slurm_train_"):
                return True
            if name.startswith("slurm_launch_"):
                return not any(
                    marker in name for marker in ("eval", "render", "select")
                )
        return False
    if executable.startswith("slurm_train_"):
        return True
    if executable.startswith("slurm_launch_"):
        return not any(
            marker in executable for marker in ("eval", "render", "select")
        )
    return False


def is_guarded_ledger_launch(words: list[str]) -> bool:
    for index, word in enumerate(words[:-1]):
        if Path(word).name == "experiment_ledger.py" and words[index + 1] == "launch":
            return True
    return False


def experiment_markers(root: Path, item: dict[str, Any]) -> set[str]:
    markers = {str(item["id"])}
    contract_name = item.get("contract_path")
    if not isinstance(contract_name, str):
        return markers
    try:
        contract = json.loads((root / contract_name).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return markers
    for field in ("allowed_launchers", "review_paths", "launch_critical_paths"):
        values = contract.get(field, [])
        if isinstance(values, list):
            markers.update(value.removeprefix("./") for value in values if isinstance(value, str))
    return markers


def training_launcher_markers(
    root: Path, item: dict[str, Any]
) -> set[str]:
    contract_name = item.get("contract_path")
    if not isinstance(contract_name, str):
        return set()
    try:
        contract = json.loads((root / contract_name).read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return set()
    values: list[str] = []
    scopes = contract.get("launch_scopes")
    if isinstance(scopes, dict):
        for config in scopes.values():
            if isinstance(config, dict):
                launchers = config.get("allowed_launchers", [])
                if isinstance(launchers, list):
                    values.extend(
                        value for value in launchers if isinstance(value, str)
                    )
    else:
        launchers = contract.get("allowed_launchers", [])
        if isinstance(launchers, list):
            values.extend(value for value in launchers if isinstance(value, str))
    markers: set[str] = set()
    for value in values:
        name = Path(value).name.lower()
        if any(marker in name for marker in ("eval", "render", "select")):
            continue
        markers.add(value.removeprefix("./"))
    return markers


def command_targets_experiment(words: list[str], markers: set[str]) -> bool:
    normalized = [word.removeprefix("./") for word in words]
    return any(marker in word for marker in markers for word in normalized)


def guard_bash(
    payload: dict[str, Any],
    root: Path,
    items: list[dict[str, Any]],
) -> None:
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return
    command = tool_input.get("command", tool_input.get("cmd", ""))
    if not isinstance(command, str) or not command.strip():
        return
    commands = shell_words(command)
    matched_ids: list[str] = []
    for item in items:
        markers = experiment_markers(root, item)
        training_markers = training_launcher_markers(root, item)
        if any(
            is_direct_training_launch(words, training_markers)
            and command_targets_experiment(words, markers)
            and not is_guarded_ledger_launch(words)
            for words in commands
        ):
            matched_ids.append(str(item["id"]))
    if not matched_ids:
        return
    experiments = ", ".join(dict.fromkeys(matched_ids))
    reason = (
        f"Direct training launch matches guarded contract(s): {experiments}. "
        "Complete contract-lint and the required scoped "
        "scientific review or operational validation, then use: "
        "python "
        "scripts/experiment_ledger.py launch <EXP-ID> -- <command>"
    )
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "deny",
                    "permissionDecisionReason": reason,
                }
            }
        )
    )


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    root = project_root(payload.get("cwd"))
    if root is None:
        return 0
    registry = load_registry(root)
    if registry is None:
        return 0
    if payload.get("hook_event_name") == "PreToolUse":
        guard_bash(payload, root, contract_items(root, registry))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
