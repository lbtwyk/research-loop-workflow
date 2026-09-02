#!/usr/bin/env python3
"""Maintain the project experiment registry and generated Markdown views.

The registry owns compact lifecycle metadata. Experiment specs remain the full,
human-readable historical record and are never rewritten by this tool.
"""

from __future__ import annotations

import argparse
import fcntl
import getpass
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, Sequence

slurm_state_snapshot = None
training_preflight = None


def load_scheduler_adapters():
    """Load optional Slurm preflight/snapshot modules from the slurm pack."""
    global slurm_state_snapshot, training_preflight
    if slurm_state_snapshot is not None and training_preflight is not None:
        return slurm_state_snapshot, training_preflight
    try:
        from scripts import slurm_state_snapshot as snap, training_preflight as pf
    except ModuleNotFoundError:
        try:
            import slurm_state_snapshot as snap  # type: ignore[no-redef]
            import training_preflight as pf  # type: ignore[no-redef]
        except ModuleNotFoundError as error:
            raise LedgerError(
                "this command requires the slurm pack "
                "(scripts/slurm_state_snapshot.py and scripts/training_preflight.py)"
            ) from error
    slurm_state_snapshot = snap
    training_preflight = pf
    return snap, pf


SCHEMA_VERSION = 1
DEFAULT_REGISTRY = Path("docs/experiments/registry.json")
DEFAULT_INDEX = Path("docs/experiments/INDEX.md")
DEFAULT_ACTIVE = Path("docs/experiments/ACTIVE.md")
WORKTREE_FOCUS_STATE = Path(".research-loop/execution-focus.json")

LIFECYCLES = (
    "draft",
    "ready",
    "queued",
    "running",
    "evaluating",
    "deciding",
    "blocked",
    "closed",
)
ACTIVE_LIFECYCLES = frozenset(LIFECYCLES) - {"closed"}
OUTCOMES = ("accepted", "rejected", "inconclusive", "superseded", "unclassified")
REVIEW_STATUSES = ("required", "pass", "repaired", "fail", "blocked")
CONTRACT_SCHEMA_VERSION = 1
EXECUTION_KINDS = frozenset(
    {"training", "evaluation", "render", "preprocess", "analysis"}
)
JOB_ID_RE = re.compile(
    r"(?m)^(?:Submitted batch job\s+)?(\d+)(?:;[^\s]+)?\s*$"
)
INTENT_ANCHOR_HEADING = "Intent Anchor"
CANONICAL_OUTLINE_HEADINGS = (
    "Intent Anchor",
    "Current Route",
    "Current Execution Snapshot",
    "Current Conclusion and Next Action",
)
MARKDOWN_HEADING_RE = re.compile(r"^(#{2,6})\s+(.+?)\s*$")

LEGACY_STATUS_MAP = {
    "idea": ("draft", None),
    "spec": ("draft", None),
    "ready": ("ready", None),
    "queued": ("queued", None),
    "running": ("running", None),
    "blocked": ("blocked", None),
    "failed": ("closed", "unclassified"),
    "needs_eval": ("evaluating", None),
    "needs_decision": ("deciding", None),
    "finished": ("closed", "unclassified"),
    "rejected": ("closed", "rejected"),
    "archived": ("closed", "unclassified"),
}

ID_RE = re.compile(r"^(EXP-\d{8}-[A-Za-z0-9._-]+)$")
SCOPE_RE = re.compile(r"^[A-Za-z0-9._-]+$")
LINK_RE = re.compile(r"^\[([^]]+)\]\(([^)]+)\)$")
DECLARED_STATUS_RE = re.compile(
    r"^\*{0,2}Status\*{0,2}:\s*`?([^`\n]+?)`?\s*$", re.IGNORECASE
)


class LedgerError(RuntimeError):
    pass


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def project_root(start: Path | None = None) -> Path:
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    raise LedgerError(f"cannot find project root from {current}")


def split_markdown_row(line: str) -> list[str]:
    text = line.strip()
    if not text.startswith("|") or not text.endswith("|"):
        raise LedgerError(f"not a Markdown table row: {line.rstrip()}")

    cells: list[str] = []
    current: list[str] = []
    in_code = False
    escaped = False
    for character in text[1:-1]:
        if escaped:
            current.append(character)
            escaped = False
            continue
        if character == "\\":
            current.append(character)
            escaped = True
            continue
        if character == "`":
            in_code = not in_code
            current.append(character)
            continue
        if character == "|" and not in_code:
            cells.append("".join(current).strip())
            current = []
            continue
        current.append(character)
    cells.append("".join(current).strip())
    return cells


def escape_cell(value: object | None) -> str:
    if value is None:
        return ""
    return str(value).replace("|", "\\|").replace("\n", "<br>")


def parse_id_cell(cell: str) -> tuple[str, str]:
    match = LINK_RE.match(cell.strip())
    if match:
        experiment_id, spec_path = match.groups()
    else:
        experiment_id = cell.strip("` ")
        spec_path = f"{experiment_id}.md"
    if not ID_RE.match(experiment_id):
        raise LedgerError(f"invalid experiment id in INDEX: {experiment_id!r}")
    return experiment_id, spec_path


def map_legacy_status(status: str) -> tuple[str, str | None]:
    normalized = status.strip().strip("`").lower()
    return LEGACY_STATUS_MAP.get(normalized, ("draft", None))


def parse_index(index_path: Path) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    section: str | None = None
    for raw_line in index_path.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("## Active Experiments"):
            section = "active"
            continue
        if raw_line.startswith("## Archived Experiments"):
            section = "archived"
            continue
        if raw_line.startswith("## "):
            section = None
            continue
        if section is None or not raw_line.startswith("| [EXP-"):
            continue

        cells = split_markdown_row(raw_line)
        if section == "active":
            if len(cells) != 6:
                raise LedgerError(
                    f"expected 6 cells in active INDEX row, found {len(cells)}: {raw_line}"
                )
            id_cell, legacy_status, branch, core_change, artifact, next_action = cells
            current_conclusion = ""
        else:
            if len(cells) != 4:
                raise LedgerError(
                    f"expected 4 cells in archived INDEX row, found {len(cells)}: {raw_line}"
                )
            id_cell, legacy_status, current_conclusion, artifact = cells
            branch = ""
            core_change = ""
            next_action = ""

        experiment_id, spec_path = parse_id_cell(id_cell)
        lifecycle, outcome = map_legacy_status(legacy_status)
        rows.append(
            {
                "id": experiment_id,
                "spec": spec_path,
                "lifecycle": lifecycle,
                "outcome": outcome,
                "legacy_status": legacy_status.strip().strip("`"),
                "branch_worktree": branch,
                "core_change": core_change,
                "current_conclusion": current_conclusion,
                "latest_artifact": artifact,
                "next_action": next_action,
                "legacy_index_section": section,
                "legacy_index_row": raw_line,
            }
        )
    return rows


def infer_supplemental_documents(experiments_dir: Path, registered_specs: set[str]) -> list[dict[str, str]]:
    supplemental: list[dict[str, str]] = []
    for path in sorted(experiments_dir.glob("EXP-*.md")):
        if path.name in registered_specs:
            continue
        kind = "results" if "result" in path.stem or "metrics" in path.stem else "supporting"
        parent = ""
        for candidate in sorted(registered_specs, key=len, reverse=True):
            candidate_stem = Path(candidate).stem
            if path.stem.startswith(candidate_stem):
                parent = candidate_stem
                break
        supplemental.append({"path": path.name, "parent": parent, "kind": kind})
    return supplemental


def new_registry(index_path: Path, experiments_dir: Path) -> dict[str, object]:
    experiments = parse_index(index_path)
    registered_specs = {str(item["spec"]) for item in experiments}
    return {
        "schema_version": SCHEMA_VERSION,
        "updated_at": utc_now(),
        "source_import": str(index_path),
        "experiments": experiments,
        "supplemental_documents": infer_supplemental_documents(
            experiments_dir, registered_specs
        ),
    }


def load_registry(path: Path) -> dict[str, object]:
    if not path.exists():
        raise LedgerError(f"registry does not exist: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise LedgerError("registry root must be an object")
    prune_legacy_review_hashes(data)
    return data


LEGACY_REVIEW_HASH_FIELDS = {
    "contract_sha256",
    "reviewed_source_digest",
    "reviewed_contract_sha256",
    "reviewed_path_hashes",
    "reviewed_path_states",
    "operational_source_digest",
    "operational_path_states",
}


def prune_legacy_review_hashes(value: object) -> None:
    if isinstance(value, dict):
        for key in LEGACY_REVIEW_HASH_FIELDS:
            value.pop(key, None)
        for child in value.values():
            prune_legacy_review_hashes(child)
    elif isinstance(value, list):
        for child in value:
            prune_legacy_review_hashes(child)


def write_registry(path: Path, data: dict[str, object]) -> None:
    prune_legacy_review_hashes(data)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def worktree_focus_path(root: Path) -> Path:
    """Return a state path in this worktree's private Git directory."""
    result = subprocess.run(
        ["git", "rev-parse", "--git-path", str(WORKTREE_FOCUS_STATE)],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise LedgerError(f"cannot resolve worktree-local Git state from {root}")
    path = Path(result.stdout.strip())
    return path if path.is_absolute() else root / path


def load_worktree_focus(root: Path) -> dict[str, object] | None:
    path = worktree_focus_path(root)
    if not path.exists():
        return None
    try:
        focus = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise LedgerError(f"invalid worktree focus state: {path}: {error}") from error
    if not isinstance(focus, dict):
        raise LedgerError(f"worktree focus state must be an object: {path}")
    return focus


def write_worktree_focus(root: Path, focus: dict[str, object]) -> Path:
    path = worktree_focus_path(root)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(focus, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    temporary.replace(path)
    return path


def sha256_bytes(contents: bytes) -> str:
    return hashlib.sha256(contents).hexdigest()


def safe_repo_path(root: Path, value: object, label: str) -> Path:
    if not isinstance(value, str) or not value:
        raise LedgerError(f"{label} must be a non-empty repo-relative path")
    relative = Path(value)
    if relative.is_absolute() or ".." in relative.parts:
        raise LedgerError(f"{label} must stay inside the repository: {value!r}")
    path = (root / relative).resolve()
    try:
        path.relative_to(root.resolve())
    except ValueError as error:
        raise LedgerError(f"{label} escapes the repository: {value!r}") from error
    return path


def markdown_section(path: Path, heading: str) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    marker = f"## {heading}"
    starts = [index for index, line in enumerate(lines) if line.rstrip() == marker]
    if len(starts) != 1:
        raise LedgerError(
            f"{path}: expected exactly one heading {marker!r}, found {len(starts)}"
        )
    start = starts[0]
    end = len(lines)
    for index in range(start + 1, len(lines)):
        if lines[index].startswith("## "):
            end = index
            break
    return "".join(lines[start:end])


def markdown_outline(path: Path) -> list[dict[str, object]]:
    """Return headings and their exact inclusive section line ranges."""
    lines = path.read_text(encoding="utf-8").splitlines()
    headings: list[dict[str, object]] = []
    for index, line in enumerate(lines):
        match = MARKDOWN_HEADING_RE.match(line)
        if match is None:
            continue
        headings.append(
            {
                "level": len(match.group(1)),
                "heading": re.sub(r"\s+#+\s*$", "", match.group(2)).strip(),
                "start_line": index + 1,
                "end_line": len(lines),
            }
        )
    for index, current in enumerate(headings):
        current_level = int(current["level"])
        for following in headings[index + 1 :]:
            if int(following["level"]) <= current_level:
                current["end_line"] = int(following["start_line"]) - 1
                break
    return headings


def intent_anchor_errors(root: Path, item: dict[str, object]) -> list[str]:
    experiment_id = str(item.get("id", ""))
    heading = item.get("intent_anchor_section")
    expected_sha = item.get("intent_anchor_sha256")
    if heading is None and expected_sha is None:
        return []
    if not isinstance(heading, str) or not heading:
        return [f"{experiment_id}: intent_anchor_section must be a non-empty string"]
    if not isinstance(expected_sha, str) or not expected_sha:
        return [f"{experiment_id}: intent_anchor_sha256 must be a non-empty string"]
    spec_path = root / "docs/experiments" / str(item.get("spec", ""))
    if not spec_path.is_file():
        return [f"{experiment_id}: cannot validate intent anchor without its spec"]
    try:
        section = markdown_section(spec_path, heading)
    except LedgerError as error:
        return [f"{experiment_id}: {error}"]
    actual_sha = sha256_bytes(section.encode("utf-8"))
    if actual_sha != expected_sha:
        return [
            f"{experiment_id}: Intent Anchor changed; a material change needs a "
            "new experiment, otherwise record the wording correction and refresh its hash"
        ]
    return []


def contract_path(root: Path, item: dict[str, object]) -> Path:
    return safe_repo_path(root, item.get("contract_path"), "contract_path")


def load_contract(root: Path, item: dict[str, object]) -> dict[str, object]:
    path = contract_path(root, item)
    if not path.exists():
        raise LedgerError(f"contract does not exist: {path.relative_to(root)}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise LedgerError(f"contract root must be an object: {path.relative_to(root)}")
    return data


def launch_scopes(contract: dict[str, object]) -> dict[str, dict[str, object]]:
    value = contract.get("launch_scopes")
    if value is None:
        return {}
    if not isinstance(value, dict):
        raise LedgerError("contract launch_scopes must be an object")
    scopes: dict[str, dict[str, object]] = {}
    for name, config in value.items():
        if not isinstance(name, str) or not SCOPE_RE.match(name):
            raise LedgerError(f"invalid launch scope name: {name!r}")
        if not isinstance(config, dict):
            raise LedgerError(f"launch scope {name!r} must be an object")
        scopes[name] = config
    return scopes


def scope_config(
    contract: dict[str, object], scope: str | None
) -> tuple[str | None, dict[str, object] | None]:
    scopes = launch_scopes(contract)
    if not scopes:
        if scope not in (None, "default"):
            raise LedgerError(
                f"contract has no launch_scopes; unexpected scope {scope!r}"
            )
        return None, None
    if scope is None:
        raise LedgerError(
            "contract defines launch_scopes; pass --scope or use a launcher "
            "that resolves to exactly one scope"
        )
    if scope not in scopes:
        raise LedgerError(
            f"unknown launch scope {scope!r}; choose from {', '.join(sorted(scopes))}"
        )
    return scope, scopes[scope]


def scope_list(
    contract: dict[str, object],
    scope: str | None,
    field: str,
    legacy_field: str,
) -> list[object]:
    _name, config = scope_config(contract, scope)
    value = (
        contract.get(legacy_field, [])
        if config is None
        else config.get(field, [])
    )
    if not isinstance(value, list):
        label = legacy_field if config is None else f"launch scope {scope!r} {field}"
        raise LedgerError(f"{label} must be a list")
    return value


def review_record(
    item: dict[str, object], scope: str | None, create: bool = False
) -> dict[str, object]:
    if scope is None:
        return item
    records = item.get("scope_reviews")
    if records is None and create:
        records = {}
        item["scope_reviews"] = records
    if not isinstance(records, dict):
        if create:
            raise LedgerError("registry scope_reviews must be an object")
        return {}
    record = records.get(scope)
    if record is None and create:
        record = {}
        records[scope] = record
    if not isinstance(record, dict):
        if create:
            raise LedgerError(f"registry scope review {scope!r} must be an object")
        return {}
    return record


def preflight_contract_errors(
    label: str,
    config: dict[str, object],
    allowed_launchers: Sequence[object],
) -> list[str]:
    errors: list[str] = []
    execution_kind = config.get("execution_kind")
    if execution_kind is not None and execution_kind not in EXECUTION_KINDS:
        errors.append(
            f"{label} execution_kind must be one of "
            + ", ".join(sorted(EXECUTION_KINDS))
        )
    launcher_kinds = config.get("launcher_kinds")
    declares_training = execution_kind == "training"
    if launcher_kinds is not None:
        if not isinstance(launcher_kinds, dict) or not launcher_kinds:
            errors.append(f"{label} launcher_kinds must be a non-empty object")
        else:
            allowed = {
                str(value).removeprefix("./")
                for value in allowed_launchers
                if isinstance(value, str)
            }
            for launcher, kind in launcher_kinds.items():
                if not isinstance(launcher, str) or not launcher:
                    errors.append(f"{label} launcher_kinds keys must be paths")
                    continue
                if launcher.removeprefix("./") not in allowed:
                    errors.append(
                        f"{label} launcher_kinds contains a launcher outside "
                        f"allowed_launchers: {launcher}"
                    )
                if kind not in EXECUTION_KINDS:
                    errors.append(
                        f"{label} launcher kind for {launcher} must be one of "
                        + ", ".join(sorted(EXECUTION_KINDS))
                    )
                declares_training = declares_training or kind == "training"
    definition = config.get("training_preflight")
    if definition is not None:
        try:
            _, pf = load_scheduler_adapters()
            pf.validate_definition(definition)
        except LedgerError as error:
            errors.append(f"{label} {error}")
        except Exception as error:
            if type(error).__name__ != "PreflightError":
                raise
            errors.append(f"{label} {error}")
    if declares_training and definition is None:
        errors.append(
            f"{label} explicitly declares training but has no training_preflight"
        )
    return errors


def contract_errors(
    root: Path, item: dict[str, object]
) -> tuple[list[str], dict[str, object] | None]:
    experiment_id = str(item.get("id", ""))
    errors: list[str] = []
    try:
        path = contract_path(root, item)
    except LedgerError as error:
        return [f"{experiment_id}: {error}"], None
    if not path.exists():
        return [f"{experiment_id}: missing contract {path.relative_to(root)}"], None
    try:
        contract = load_contract(root, item)
    except (LedgerError, json.JSONDecodeError) as error:
        return [f"{experiment_id}: invalid contract: {error}"], None

    if contract.get("schema_version") != CONTRACT_SCHEMA_VERSION:
        errors.append(
            f"{experiment_id}: contract schema_version must be "
            f"{CONTRACT_SCHEMA_VERSION}"
        )
    if contract.get("experiment_id") != experiment_id:
        errors.append(f"{experiment_id}: contract experiment_id does not match")

    try:
        spec_path = safe_repo_path(root, contract.get("spec_path"), "spec_path")
    except LedgerError as error:
        errors.append(f"{experiment_id}: {error}")
    else:
        expected_spec = root / "docs/experiments" / str(item.get("spec", ""))
        if spec_path != expected_spec.resolve():
            errors.append(f"{experiment_id}: contract spec_path does not match registry")
        elif not spec_path.exists():
            errors.append(f"{experiment_id}: contract spec is missing")
        else:
            heading = contract.get("frozen_spec_section")
            if not isinstance(heading, str) or not heading:
                errors.append(f"{experiment_id}: frozen_spec_section is required")
            else:
                try:
                    section = markdown_section(spec_path, heading)
                except LedgerError as error:
                    errors.append(f"{experiment_id}: {error}")
                else:
                    actual = sha256_bytes(section.encode("utf-8"))
                    if contract.get("frozen_spec_sha256") != actual:
                        errors.append(
                            f"{experiment_id}: frozen spec section changed; "
                            "refresh the scientific contract deliberately"
                        )

    for field in ("review_paths", "invariants", "required_tests", "allowed_launchers"):
        value = contract.get(field)
        if not isinstance(value, list) or not value:
            errors.append(f"{experiment_id}: contract {field} must be a non-empty list")

    review_paths = contract.get("review_paths", [])
    if isinstance(review_paths, list):
        for value in review_paths:
            try:
                path = safe_repo_path(root, value, "review_paths entry")
            except LedgerError as error:
                errors.append(f"{experiment_id}: {error}")
                continue
            if not path.is_file():
                errors.append(f"{experiment_id}: missing review path {value}")

    critical_paths = contract.get("launch_critical_paths")
    if critical_paths is not None:
        if not isinstance(critical_paths, list) or not critical_paths:
            errors.append(
                f"{experiment_id}: launch_critical_paths must be a non-empty list"
            )
        elif isinstance(review_paths, list):
            unknown = [value for value in critical_paths if value not in review_paths]
            if unknown:
                errors.append(
                    f"{experiment_id}: launch_critical_paths are not review_paths: "
                    + ", ".join(str(value) for value in unknown)
                )

    launchers = contract.get("allowed_launchers", [])
    if isinstance(launchers, list):
        for value in launchers:
            try:
                path = safe_repo_path(root, value, "allowed_launchers entry")
            except LedgerError as error:
                errors.append(f"{experiment_id}: {error}")
                continue
            if not path.is_file():
                errors.append(f"{experiment_id}: missing allowed launcher {value}")
            if isinstance(review_paths, list) and value not in review_paths:
                errors.append(
                    f"{experiment_id}: allowed launcher is not a review path: {value}"
                )
        errors.extend(
            preflight_contract_errors(experiment_id, contract, launchers)
        )

    scopes_value = contract.get("launch_scopes")
    if scopes_value is not None:
        if not isinstance(scopes_value, dict) or not scopes_value:
            errors.append(
                f"{experiment_id}: launch_scopes must be a non-empty object"
            )
        else:
            top_tests = contract.get("required_tests", [])
            scope_names = set(scopes_value)
            for scope_name, config in scopes_value.items():
                label = f"{experiment_id}: launch scope {scope_name!r}"
                if not isinstance(scope_name, str) or not SCOPE_RE.match(scope_name):
                    errors.append(f"{experiment_id}: invalid launch scope {scope_name!r}")
                    continue
                if not isinstance(config, dict):
                    errors.append(f"{label} must be an object")
                    continue
                for field in ("critical_paths", "allowed_launchers", "required_tests"):
                    value = config.get(field)
                    if not isinstance(value, list) or not value:
                        errors.append(f"{label} {field} must be a non-empty list")
                critical = config.get("critical_paths", [])
                operational = config.get("operational_paths", [])
                scope_launchers = config.get("allowed_launchers", [])
                scope_tests = config.get("required_tests", [])
                operational_tests = config.get("operational_tests", [])
                if not isinstance(critical, list):
                    critical = []
                if not isinstance(operational, list):
                    errors.append(f"{label} operational_paths must be a list")
                    operational = []
                if not isinstance(scope_launchers, list):
                    scope_launchers = []
                if not isinstance(scope_tests, list):
                    scope_tests = []
                if not isinstance(operational_tests, list):
                    errors.append(f"{label} operational_tests must be a list")
                    operational_tests = []
                if operational and not operational_tests:
                    errors.append(
                        f"{label} operational_tests must be non-empty when "
                        "operational_paths are declared"
                    )
                if isinstance(review_paths, list):
                    unknown = [
                        value
                        for value in [*critical, *operational]
                        if value not in review_paths
                    ]
                    if unknown:
                        errors.append(
                            f"{label} paths are not review_paths: "
                            + ", ".join(str(value) for value in unknown)
                        )
                overlap = set(critical) & set(operational)
                if overlap:
                    errors.append(
                        f"{label} critical_paths and operational_paths overlap: "
                        + ", ".join(sorted(str(value) for value in overlap))
                    )
                if isinstance(launchers, list):
                    unknown = [
                        value for value in scope_launchers if value not in launchers
                    ]
                    if unknown:
                        errors.append(
                            f"{label} allowed_launchers are not top-level "
                            "allowed_launchers: "
                            + ", ".join(str(value) for value in unknown)
                        )
                reviewed_scope_paths = set(critical) | set(operational)
                unreviewed_launchers = [
                    value
                    for value in scope_launchers
                    if value not in reviewed_scope_paths
                ]
                if unreviewed_launchers:
                    errors.append(
                        f"{label} launchers are not scope-reviewed paths: "
                        + ", ".join(str(value) for value in unreviewed_launchers)
                    )
                if isinstance(top_tests, list):
                    unknown_tests = [
                        value
                        for value in [*scope_tests, *operational_tests]
                        if value not in top_tests
                    ]
                    if unknown_tests:
                        errors.append(
                            f"{label} tests are not top-level required_tests: "
                            + ", ".join(str(value) for value in unknown_tests)
                        )
                errors.extend(
                    preflight_contract_errors(label, config, scope_launchers)
                )
                dependencies = config.get("depends_on", [])
                if not isinstance(dependencies, list) or any(
                    not isinstance(value, str) for value in dependencies
                ):
                    errors.append(f"{label} depends_on must be a list of scope names")
                else:
                    unknown_dependencies = sorted(set(dependencies) - scope_names)
                    if unknown_dependencies:
                        errors.append(
                            f"{label} depends_on contains unknown scopes: "
                            + ", ".join(unknown_dependencies)
                        )
                    if scope_name in dependencies:
                        errors.append(f"{label} cannot depend on itself")
                completion_evidence = config.get("completion_evidence", [])
                if not isinstance(completion_evidence, list) or any(
                    not isinstance(value, str) or not value
                    for value in completion_evidence
                ):
                    errors.append(
                        f"{label} completion_evidence must be a list of paths"
                    )
            dependency_map = {
                str(name): config.get("depends_on", [])
                for name, config in scopes_value.items()
                if isinstance(config, dict)
                and isinstance(config.get("depends_on", []), list)
            }
            visiting: set[str] = set()
            visited: set[str] = set()

            def visit_scope(name: str) -> bool:
                if name in visiting:
                    return True
                if name in visited:
                    return False
                visiting.add(name)
                for dependency in dependency_map.get(name, []):
                    if isinstance(dependency, str) and dependency in dependency_map:
                        if visit_scope(dependency):
                            return True
                visiting.remove(name)
                visited.add(name)
                return False

            if any(visit_scope(str(name)) for name in scopes_value):
                errors.append(f"{experiment_id}: launch scope dependencies contain a cycle")
    completion_evidence = contract.get("completion_evidence", [])
    if not isinstance(completion_evidence, list) or any(
        not isinstance(value, str) or not value for value in completion_evidence
    ):
        errors.append(f"{experiment_id}: completion_evidence must be a list of paths")
    return errors, contract


def git_head(root: Path) -> str:
    result = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=root,
        check=False,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip() if result.returncode == 0 else "unknown"


def git_dirty_paths(root: Path, paths: Sequence[object] = ()) -> list[str]:
    command = ["git", "status", "--short", "--untracked-files=all"]
    selected = [str(value) for value in paths if isinstance(value, str)]
    if selected:
        command.extend(["--", *selected])
    result = subprocess.run(
        command, cwd=root, check=False, capture_output=True, text=True
    )
    if result.returncode != 0:
        return []
    return [line[3:] for line in result.stdout.splitlines() if len(line) >= 4]


def review_is_current(
    root: Path, item: dict[str, object], scope: str | None = None
) -> tuple[bool, str, str | None]:
    errors, contract = contract_errors(root, item)
    if errors or contract is None:
        return False, "; ".join(errors), None
    resolved_scope, _config = scope_config(contract, scope)
    record = review_record(item, resolved_scope)
    if record.get("review_status") not in ("pass", "repaired"):
        return (
            False,
            f"review status is {record.get('review_status', 'required')!r}",
            None,
        )
    if contract.get("resource_contract"):
        resource_review = record.get("resource_review")
        if not isinstance(resource_review, dict):
            return False, "resource/efficiency review packet is missing", None
        rows = resource_review.get("rows")
        if not isinstance(rows, list) or not rows or any(
            not isinstance(row, dict) or row.get("decision") == "blocked"
            for row in rows
        ):
            return False, "resource/efficiency review has a BLOCKED row", None
    status = str(record.get("review_status"))
    reviewed_at = str(record.get("reviewed_at") or "recorded-review")
    return True, f"review {status} decision is recorded", reviewed_at


def operational_is_current(
    root: Path,
    item: dict[str, object],
    contract: dict[str, object],
    scope: str | None,
) -> tuple[bool, str, str | None]:
    _resolved_scope, config = scope_config(contract, scope)
    if config is None or not scope_list(
        contract, scope, "operational_paths", "review_paths"
    ):
        return True, "no operational validation is required", None
    record = review_record(item, scope)
    if not record.get("operational_validated_at"):
        return False, "operational validation is not recorded", None
    return True, "operational validation is recorded", str(
        record["operational_validated_at"]
    )


def sorted_experiments(data: dict[str, object]) -> list[dict[str, object]]:
    experiments = data.get("experiments", [])
    if not isinstance(experiments, list):
        raise LedgerError("registry experiments must be a list")
    return sorted(experiments, key=lambda item: str(item.get("id", "")), reverse=True)


def render_rows(experiments: Iterable[dict[str, object]]) -> list[str]:
    rows: list[str] = []
    for item in experiments:
        experiment_id = escape_cell(item.get("id"))
        spec = escape_cell(item.get("spec"))
        link = f"[{experiment_id}]({spec})"
        values = (
            link,
            item.get("lifecycle"),
            item.get("outcome"),
            item.get("legacy_status"),
            item.get("branch_worktree"),
            item.get("core_change"),
            item.get("current_conclusion"),
            item.get("latest_artifact"),
            item.get("next_action"),
        )
        rows.append("| " + " | ".join(escape_cell(value) for value in values) + " |")
    return rows


def render_table(experiments: list[dict[str, object]]) -> str:
    header = (
        "| ID | Lifecycle | Outcome | Legacy Status | Branch/Worktree | "
        "Core Change | Current Conclusion | Latest Artifact | Next Action |\n"
        "|---|---|---|---|---|---|---|---|---|\n"
    )
    rows = render_rows(experiments)
    return header + ("\n".join(rows) if rows else "| _none_ |  |  |  |  |  |  |  |  |")


def compact_text(value: object | None, limit: int = 120) -> str:
    text = " ".join(str(value or "").replace("`", "").split())
    return text if len(text) <= limit else text[: limit - 1].rstrip() + "…"


def render_active_table(experiments: list[dict[str, object]]) -> str:
    header = (
        "| ID | Lifecycle | Outcome | Next Action |\n"
        "|---|---|---|---|\n"
    )
    rows: list[str] = []
    for item in experiments:
        experiment_id = str(item.get("id", ""))
        spec = escape_cell(item.get("spec"))
        values = (
            f"[{escape_cell(experiment_id)}]({spec})",
            item.get("lifecycle"),
            item.get("outcome"),
            compact_text(item.get("next_action")),
        )
        rows.append("| " + " | ".join(escape_cell(value) for value in values) + " |")
    return header + ("\n".join(rows) if rows else "| _none_ |  |  |  |  |")


def render_active(data: dict[str, object]) -> str:
    active = [
        item
        for item in sorted_experiments(data)
        if item.get("lifecycle") in ACTIVE_LIFECYCLES
    ]
    return (
        "<!-- Generated by scripts/experiment_ledger.py; edit registry.json, not this file. -->\n"
        "# Active Experiments\n\n"
        "Compact navigation only. Select an experiment from the current user request "
        "or adopted thread objective, then read its Intent Anchor, current route, and "
        "execution state. Dormant worktree focus is used only by an explicitly invoked "
        "ledger command; use INDEX.md only for historical navigation.\n\n"
        + render_active_table(active)
        + "\n"
    )


def render_index(data: dict[str, object]) -> str:
    experiments = sorted_experiments(data)
    active = [item for item in experiments if item.get("lifecycle") in ACTIVE_LIFECYCLES]
    closed = [item for item in experiments if item.get("lifecycle") == "closed"]
    return (
        "<!-- Generated by scripts/experiment_ledger.py; edit registry.json, not this file. -->\n"
        "# Experiment Index\n\n"
        "The registry is the source of truth for lifecycle metadata. Experiment specs remain "
        "the complete source of truth for design, run history, evidence, and conclusions.\n\n"
        "## Active Experiments\n\n"
        + render_table(active)
        + "\n\n## Closed Experiments\n\n"
        + render_table(closed)
        + "\n\n## State Model\n\n"
        "- Lifecycle: `draft`, `ready`, `queued`, `running`, `evaluating`, `deciding`, `blocked`, `closed`.\n"
        "- Scientific outcome: `accepted`, `rejected`, `inconclusive`, `superseded`, `unclassified`, or blank while unresolved.\n"
        "- Run/job state belongs in the experiment spec or runtime manifest, not in lifecycle.\n"
        "- `legacy_status` preserves the exact pre-registry status and is not rewritten automatically.\n\n"
        "## Rules\n\n"
        "- Resolve current work from the user request or adopted thread objective; use `ACTIVE.md` only for navigation when the experiment is missing or changing.\n"
        "- A material Intent Anchor change creates a new experiment; meaning-preserving corrections must be recorded and re-hashed deliberately.\n"
        "- Create a new experiment only for a new falsifiable question, claim, causal intervention, or materially changed frozen contract.\n"
        "- Seeds, retries, checkpoints, evals, renders, and presentation artifacts normally remain runs or supporting documents under their parent experiment.\n"
        "- Keep bug fixes and implementation revisions for the same claim as routes in the parent spec, not new experiments.\n"
        "- Consolidate replaced routes into compact route-evolution entries; preserve conclusions, negative evidence, decision reasons, and provenance while keeping only the current selected route fully detailed.\n"
        "- Run `python scripts/experiment_ledger.py lint` after registry edits and `sync` to regenerate views.\n"
    )


def sync_views(root: Path, data: dict[str, object]) -> None:
    (root / DEFAULT_ACTIVE).write_text(render_active(data), encoding="utf-8")
    (root / DEFAULT_INDEX).write_text(render_index(data), encoding="utf-8")


def declared_status(spec_path: Path) -> str | None:
    with spec_path.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if line_number > 30:
                break
            match = DECLARED_STATUS_RE.match(line.strip())
            if match:
                return match.group(1).strip().lower()
    return None


def lint_registry(root: Path, data: dict[str, object]) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    if data.get("schema_version") != SCHEMA_VERSION:
        errors.append(
            f"schema_version must be {SCHEMA_VERSION}, found {data.get('schema_version')!r}"
        )

    experiments = sorted_experiments(data)
    seen_ids: set[str] = set()
    seen_specs: set[str] = set()
    for item in experiments:
        experiment_id = str(item.get("id", ""))
        spec_name = str(item.get("spec", ""))
        lifecycle = item.get("lifecycle")
        outcome = item.get("outcome")
        if not ID_RE.match(experiment_id):
            errors.append(f"invalid experiment id: {experiment_id!r}")
        if experiment_id in seen_ids:
            errors.append(f"duplicate experiment id: {experiment_id}")
        seen_ids.add(experiment_id)
        if spec_name in seen_specs:
            errors.append(f"duplicate spec path: {spec_name}")
        seen_specs.add(spec_name)
        if lifecycle not in LIFECYCLES:
            errors.append(f"{experiment_id}: invalid lifecycle {lifecycle!r}")
        if outcome is not None and outcome not in OUTCOMES:
            errors.append(f"{experiment_id}: invalid outcome {outcome!r}")
        if lifecycle != "closed" and outcome is not None:
            warnings.append(
                f"{experiment_id}: outcome {outcome!r} is set before lifecycle is closed"
            )

        spec_path = root / "docs/experiments" / spec_name
        if not spec_path.exists():
            errors.append(f"{experiment_id}: missing spec {spec_name}")
            continue
        status = declared_status(spec_path)
        legacy_status = str(item.get("legacy_status", "")).lower()
        if status and status != legacy_status:
            warnings.append(
                f"{experiment_id}: spec status {status!r} differs from registry legacy_status {legacy_status!r}"
            )
        warnings.extend(intent_anchor_errors(root, item))

        if item.get("contract_path") is not None:
            try:
                path = contract_path(root, item)
            except LedgerError as error:
                errors.append(f"{experiment_id}: {error}")
            else:
                if not path.exists():
                    errors.append(
                        f"{experiment_id}: missing contract {path.relative_to(root)}"
                    )
            review_status = item.get("review_status", "required")
            if review_status not in REVIEW_STATUSES:
                errors.append(
                    f"{experiment_id}: invalid review_status {review_status!r}"
                )
            try:
                contract = load_contract(root, item)
                scopes = launch_scopes(contract)
            except (LedgerError, json.JSONDecodeError):
                scopes = {}
            else:
                if (
                    isinstance(contract.get("efficiency_contract"), dict)
                    and contract.get("efficiency_contract")
                    and not contract.get("resource_contract")
                ):
                    warnings.append(
                        f"{experiment_id}: efficiency_contract has no "
                        "resource_contract; record an estimated request/headroom "
                        "self-check when reviewing (non-blocking)"
                    )
            scope_reviews = item.get("scope_reviews", {})
            if scope_reviews is not None and not isinstance(scope_reviews, dict):
                errors.append(f"{experiment_id}: scope_reviews must be an object")
            elif isinstance(scope_reviews, dict):
                unknown_scopes = set(scope_reviews) - set(scopes)
                if unknown_scopes:
                    errors.append(
                        f"{experiment_id}: scope_reviews reference unknown scopes: "
                        + ", ".join(sorted(str(value) for value in unknown_scopes))
                    )
                for scope_name, record in scope_reviews.items():
                    if not isinstance(record, dict):
                        errors.append(
                            f"{experiment_id}: scope review {scope_name!r} "
                            "must be an object"
                        )
                        continue
                    status = record.get("review_status", "required")
                    if status not in REVIEW_STATUSES:
                        errors.append(
                            f"{experiment_id}: scope {scope_name!r} has invalid "
                            f"review_status {status!r}"
                        )

    if "execution_focus" in data:
        errors.append(
            "execution_focus is worktree-local state; remove it from registry.json "
            "and set it with experiment_ledger.py focus"
        )

    supplemental = data.get("supplemental_documents", [])
    if not isinstance(supplemental, list):
        errors.append("supplemental_documents must be a list")
        supplemental = []
    supplemental_paths: set[str] = set()
    for item in supplemental:
        if not isinstance(item, dict):
            errors.append("supplemental document entries must be objects")
            continue
        path = str(item.get("path", ""))
        supplemental_paths.add(path)
        if not (root / "docs/experiments" / path).exists():
            errors.append(f"missing supplemental document: {path}")
        parent = str(item.get("parent", ""))
        if parent and parent not in seen_ids:
            errors.append(f"supplemental document {path}: unknown parent {parent}")

    disk_docs = {
        path.name for path in (root / "docs/experiments").glob("EXP-*.md")
    }
    unregistered = disk_docs - seen_specs - supplemental_paths
    for path in sorted(unregistered):
        errors.append(f"unregistered experiment document: {path}")

    expected_active = render_active(data)
    expected_index = render_index(data)
    active_path = root / DEFAULT_ACTIVE
    index_path = root / DEFAULT_INDEX
    if not active_path.exists() or active_path.read_text(encoding="utf-8") != expected_active:
        errors.append("ACTIVE.md is missing or stale; run sync")
    if not index_path.exists() or index_path.read_text(encoding="utf-8") != expected_index:
        errors.append("INDEX.md is stale; run sync")
    return errors, warnings


def find_experiment(data: dict[str, object], experiment_id: str) -> dict[str, object]:
    for item in sorted_experiments(data):
        if item.get("id") == experiment_id:
            return item
    raise LedgerError(f"unknown experiment id: {experiment_id}")


def command_import(root: Path, args: argparse.Namespace) -> None:
    registry_path = root / DEFAULT_REGISTRY
    if registry_path.exists() and not args.force:
        raise LedgerError(f"registry already exists: {registry_path}; use --force to replace")
    data = new_registry(root / DEFAULT_INDEX, root / "docs/experiments")
    write_registry(registry_path, data)
    sync_views(root, data)
    print(
        f"imported {len(data['experiments'])} experiments and "
        f"{len(data['supplemental_documents'])} supplemental documents"
    )


def command_sync(root: Path, _args: argparse.Namespace) -> None:
    data = load_registry(root / DEFAULT_REGISTRY)
    write_registry(root / DEFAULT_REGISTRY, data)
    sync_views(root, data)
    print("regenerated docs/experiments/ACTIVE.md and INDEX.md")


def command_lint(root: Path, _args: argparse.Namespace) -> None:
    data = load_registry(root / DEFAULT_REGISTRY)
    errors, warnings = lint_registry(root, data)
    for warning in warnings:
        print(f"WARN: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"lint: {len(errors)} error(s), {len(warnings)} warning(s)")
    if errors:
        raise SystemExit(1)


def command_status(root: Path, args: argparse.Namespace) -> None:
    data = load_registry(root / DEFAULT_REGISTRY)
    if args.experiment_id:
        item = find_experiment(data, args.experiment_id)
        snapshot = None
        if args.slurm_snapshot:
            snapshot = load_slurm_snapshot(root, args.slurm_snapshot)
        elif not args.no_slurm:
            snap, _ = load_scheduler_adapters()
            snapshot = snap.collect_snapshot(
                user=getpass.getuser(), since=args.since
            )
        errors, contract = contract_errors(root, item)
        stages: list[dict[str, object]] = []
        remaining: list[str] = []
        reviews: list[dict[str, object]] = []
        if contract is not None:
            closure = compile_stage_closure(
                root,
                experiment_id=args.experiment_id,
                contract=contract,
                snapshot=snapshot,
            )
            remaining = list(closure["remaining"])
            for stage in closure["stages"]:
                evidence = stage["completion_evidence"]
                latest = stage["latest_launch"]
                stages.append(
                    {
                        "name": stage["stage"],
                        "state": stage["state"],
                        "job_id": (
                            None if latest is None else latest.get("slurm_job_id")
                        ),
                        "scheduler_state": stage["scheduler_state"],
                        "missing_evidence": [
                            row["path"]
                            for row in evidence["paths"]
                            if not row["fresh_since_launch"]
                        ],
                    }
                )
            scope_names = list(launch_scopes(contract)) or [None]
            for scope in scope_names:
                record = review_record(item, scope)
                reviews.append(
                    {
                        "scope": scope or "default",
                        "status": record.get("review_status", "required"),
                    }
                )
        states = {str(stage["state"]) for stage in stages}
        if errors or "terminal_unverified" in states:
            overall = "needs_attention"
        elif states & {"running", "queued"}:
            overall = "running" if "running" in states else "queued"
        elif stages and not remaining:
            overall = "operationally_complete"
        elif stages:
            overall = "not_complete"
        else:
            overall = str(item.get("lifecycle", "unknown"))
        unavailable = []
        if snapshot is not None:
            unavailable = [
                name
                for name, source in snapshot.get("sources", {}).items()
                if isinstance(source, dict) and source.get("status") != "ok"
            ]
        payload = {
            "schema_version": 1,
            "captured_at": utc_now(),
            "experiment_id": args.experiment_id,
            "lifecycle": item.get("lifecycle"),
            "outcome": item.get("outcome"),
            "status": overall,
            "reviews": reviews,
            "stages": stages,
            "remaining": remaining,
            "next_action": item.get("next_action"),
            "contract_errors": {"count": len(errors), "items": errors[:3]},
            "scheduler": {
                "captured": snapshot is not None,
                "unavailable_sources": unavailable,
            },
        }
        print(
            json.dumps(
                payload,
                ensure_ascii=False,
                indent=2 if args.pretty else None,
                separators=None if args.pretty else (",", ":"),
            )
        )
        return
    experiments = sorted_experiments(data)
    if not args.all:
        experiments = [
            item for item in experiments if item.get("lifecycle") in ACTIVE_LIFECYCLES
        ]
    for item in experiments:
        print(
            "\t".join(
                (
                    str(item.get("id", "")),
                    str(item.get("lifecycle", "")),
                    str(item.get("outcome") or "-"),
                    str(item.get("next_action") or "-"),
                )
            )
        )


def command_add(root: Path, args: argparse.Namespace) -> None:
    if not ID_RE.match(args.experiment_id):
        raise LedgerError(f"invalid experiment id: {args.experiment_id!r}")
    registry_path = root / DEFAULT_REGISTRY
    data = load_registry(registry_path)
    experiments = data.get("experiments", [])
    if not isinstance(experiments, list):
        raise LedgerError("registry experiments must be a list")
    if any(item.get("id") == args.experiment_id for item in experiments):
        raise LedgerError(f"experiment already registered: {args.experiment_id}")

    spec_name = args.spec or f"{args.experiment_id}.md"
    spec_path = root / "docs/experiments" / spec_name
    if not spec_path.exists():
        raise LedgerError(
            f"spec does not exist: {spec_path}; create the complete spec before registering it"
        )
    if any(item.get("spec") == spec_name for item in experiments):
        raise LedgerError(f"spec already registered: {spec_name}")
    try:
        anchor = markdown_section(spec_path, INTENT_ANCHOR_HEADING)
    except LedgerError as error:
        raise LedgerError(
            f"new experiment specs require ## {INTENT_ANCHOR_HEADING}: {error}"
        ) from error

    new_item = {
            "id": args.experiment_id,
            "spec": spec_name,
            "lifecycle": args.lifecycle,
            "outcome": None,
            "legacy_status": args.legacy_status or args.lifecycle,
            "branch_worktree": args.branch_worktree or "",
            "core_change": args.core_change or "",
            "current_conclusion": args.current_conclusion or "",
            "latest_artifact": args.latest_artifact or "",
            "next_action": args.next_action or "",
            "intent_anchor_section": INTENT_ANCHOR_HEADING,
            "intent_anchor_sha256": sha256_bytes(anchor.encode("utf-8")),
            "intent_anchor_updated_at": utc_now(),
            "intent_anchor_update_reason": "initial experiment registration",
        }
    requested_contract = getattr(args, "contract_path", None)
    if requested_contract:
        path = safe_repo_path(root, requested_contract, "contract_path")
        if not path.is_file():
            raise LedgerError(f"contract does not exist: {requested_contract}")
        new_item["contract_path"] = requested_contract
        new_item["review_status"] = "required"
    experiments.append(new_item)
    supplemental = data.get("supplemental_documents", [])
    if isinstance(supplemental, list):
        data["supplemental_documents"] = [
            item for item in supplemental if item.get("path") != spec_name
        ]
    data["updated_at"] = utc_now()
    write_registry(registry_path, data)
    sync_views(root, data)
    print(f"registered {args.experiment_id}")


def mutate_experiment(root: Path, args: argparse.Namespace, close: bool = False) -> None:
    registry_path = root / DEFAULT_REGISTRY
    data = load_registry(registry_path)
    item = find_experiment(data, args.experiment_id)
    if close:
        item["lifecycle"] = "closed"
        item["outcome"] = args.outcome
    else:
        if args.lifecycle is not None:
            item["lifecycle"] = args.lifecycle
        if args.outcome is not None:
            item["outcome"] = None if args.outcome == "none" else args.outcome
    for argument, key in (
        ("contract_path", "contract_path"),
        ("legacy_status", "legacy_status"),
        ("branch_worktree", "branch_worktree"),
        ("core_change", "core_change"),
        ("current_conclusion", "current_conclusion"),
        ("latest_artifact", "latest_artifact"),
        ("next_action", "next_action"),
        ("contract_path", "contract_path"),
        ("provenance_state", "provenance_state"),
    ):
        value = getattr(args, argument, None)
        if value is not None:
            if argument == "contract_path":
                path = safe_repo_path(root, value, "contract_path")
                if not path.is_file():
                    raise LedgerError(f"contract does not exist: {value}")
                item.setdefault("review_status", "required")
            item[key] = value
    if getattr(args, "contract_path", None) is not None:
        path = contract_path(root, item)
        if not path.is_file():
            raise LedgerError(
                f"contract does not exist: {path.relative_to(root)}"
            )
        item["review_status"] = "required"
    data["updated_at"] = utc_now()
    write_registry(registry_path, data)
    sync_views(root, data)
    print(f"updated {args.experiment_id}")


def command_focus(root: Path, args: argparse.Namespace) -> None:
    registry_path = root / DEFAULT_REGISTRY
    data = load_registry(registry_path)
    find_experiment(data, args.experiment_id)
    focus = {
        "experiment_id": args.experiment_id,
        "milestone": args.milestone,
        "updated_at": utc_now(),
    }
    path = write_worktree_focus(root, focus)
    print(
        f"focused {args.experiment_id}: {args.milestone}\n"
        f"worktree state: {path}"
    )


def command_outline(root: Path, args: argparse.Namespace) -> None:
    data = load_registry(root / DEFAULT_REGISTRY)
    experiment_id = args.experiment_id
    implicit_focus = experiment_id is None
    if experiment_id is None:
        focus = load_worktree_focus(root)
        experiment_id = focus.get("experiment_id") if focus else None
        if not isinstance(experiment_id, str) or not experiment_id:
            raise LedgerError(
                "outline needs an experiment id or a valid worktree-local focus"
            )
    item = find_experiment(data, experiment_id)
    if implicit_focus and (
        item.get("lifecycle") == "closed" or item.get("outcome") == "superseded"
    ):
        lifecycle = item.get("lifecycle")
        outcome = item.get("outcome") or "unset"
        raise LedgerError(
            f"stored worktree focus {experiment_id} is stale "
            f"(lifecycle={lifecycle}, outcome={outcome}); run "
            f"`scripts/experiment_ledger.py outline <EXP-ID>` for an explicit "
            "experiment, or replace it with "
            "`scripts/experiment_ledger.py focus <EXP-ID> --milestone \"...\"`"
        )
    spec_path = safe_repo_path(
        root,
        (Path("docs/experiments") / str(item.get("spec", ""))).as_posix(),
        "experiment spec",
    )
    if not spec_path.is_file():
        raise LedgerError(f"experiment spec does not exist: {spec_path}")
    headings = markdown_outline(spec_path)
    relative = spec_path.relative_to(root)
    print(f"experiment: {experiment_id}")
    print(f"spec: {relative}")
    print("canonical:")
    for expected in CANONICAL_OUTLINE_HEADINGS:
        matches = [heading for heading in headings if heading["heading"] == expected]
        if not matches:
            print(f"  missing | {expected}")
            continue
        status = "present" if len(matches) == 1 else "duplicate"
        ranges = ", ".join(
            f"{match['start_line']}-{match['end_line']}" for match in matches
        )
        print(f"  {status} | {ranges} | {expected}")
    print("headings:")
    for heading in headings:
        print(
            f"  H{heading['level']} | {heading['start_line']}-"
            f"{heading['end_line']} | {heading['heading']}"
        )


def command_anchor_refresh(root: Path, args: argparse.Namespace) -> None:
    registry_path = root / DEFAULT_REGISTRY
    data = load_registry(registry_path)
    item = find_experiment(data, args.experiment_id)
    heading = item.get("intent_anchor_section", INTENT_ANCHOR_HEADING)
    if not isinstance(heading, str) or not heading:
        heading = INTENT_ANCHOR_HEADING
    spec_path = root / "docs/experiments" / str(item.get("spec", ""))
    section = markdown_section(spec_path, heading)
    item["intent_anchor_section"] = heading
    item["intent_anchor_sha256"] = sha256_bytes(section.encode("utf-8"))
    item["intent_anchor_updated_at"] = utc_now()
    item["intent_anchor_update_reason"] = args.reason
    data["updated_at"] = utc_now()
    write_registry(registry_path, data)
    print(f"refreshed Intent Anchor hash for {args.experiment_id}: {args.reason}")


def command_contract_lint(root: Path, args: argparse.Namespace) -> None:
    data = load_registry(root / DEFAULT_REGISTRY)
    item = find_experiment(data, args.experiment_id)
    errors, _contract = contract_errors(root, item)
    for error in errors:
        print(f"ERROR: {error}")
    print(f"contract-lint: {len(errors)} error(s)")
    if errors:
        raise SystemExit(1)


def run_required_tests(
    root: Path, commands: Sequence[object]
) -> list[dict[str, object]]:
    results: list[dict[str, object]] = []
    for value in commands:
        if not isinstance(value, str) or not value.strip():
            raise LedgerError("required_tests entries must be non-empty command strings")
        result = subprocess.run(
            value,
            cwd=root,
            shell=True,
            executable="/bin/bash",
            check=False,
            capture_output=True,
            text=True,
        )
        results.append(
            {
                "command": value,
                "returncode": result.returncode,
                "stdout": result.stdout[-4000:],
                "stderr": result.stderr[-4000:],
            }
        )
    return results


def delta_review_precondition(item: dict[str, object]) -> str | None:
    if item.get("review_status") not in ("fail", "blocked"):
        return "delta review requires a previous fail or blocked decision"
    return None


def load_json_file(root: Path, value: str, label: str) -> object:
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise LedgerError(f"{label} file does not exist: {path}") from error
    except json.JSONDecodeError as error:
        raise LedgerError(f"{label} file is not valid JSON: {path}: {error}") from error


def normalized_review_findings(payload: object) -> list[dict[str, object]]:
    values = payload.get("findings") if isinstance(payload, dict) else payload
    if not isinstance(values, list) or not values:
        raise LedgerError("review findings must contain a non-empty findings list")
    findings: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, value in enumerate(values, start=1):
        if not isinstance(value, dict):
            raise LedgerError(f"review finding {index} must be an object")
        finding_id = str(value.get("id", "")).strip()
        if not finding_id or finding_id in seen:
            raise LedgerError(
                f"review finding {index} must have a unique non-empty id"
            )
        seen.add(finding_id)
        closure_mode = str(value.get("closure_mode", "proof")).strip()
        if closure_mode not in ("proof", "reviewer"):
            raise LedgerError(
                f"review finding {finding_id} closure_mode must be proof or reviewer"
            )
        summary = str(value.get("summary", "")).strip()
        required_proof = str(value.get("required_proof", "")).strip()
        evidence = value.get("evidence", [])
        if not summary or not required_proof:
            raise LedgerError(
                f"review finding {finding_id} requires summary and required_proof"
            )
        if not isinstance(evidence, list) or not all(
            isinstance(item, str) and item.strip() for item in evidence
        ):
            raise LedgerError(
                f"review finding {finding_id} evidence must be a list of strings"
            )
        findings.append(
            {
                "id": finding_id,
                "category": str(value.get("category", "semantics")).strip(),
                "summary": summary,
                "evidence": evidence,
                "required_proof": required_proof,
                "closure_mode": closure_mode,
            }
        )
    return findings


def normalized_resource_review(payload: object) -> dict[str, object]:
    """Validate an optional numeric resource/efficiency review packet."""
    if not isinstance(payload, dict):
        raise LedgerError("resource review must be a JSON object")
    summary = str(payload.get("summary", "")).strip()
    rows = payload.get("rows")
    if not summary or not isinstance(rows, list) or not rows:
        raise LedgerError("resource review requires summary and non-empty rows")
    required = {
        "field",
        "requested",
        "need",
        "headroom",
        "evidence",
        "decision",
    }
    normalized: list[dict[str, object]] = []
    for index, value in enumerate(rows, start=1):
        if not isinstance(value, dict):
            raise LedgerError(f"resource review row {index} must be an object")
        missing = sorted(required - set(value))
        if missing:
            raise LedgerError(
                f"resource review row {index} is missing: {', '.join(missing)}"
            )
        decision = str(value["decision"]).strip().lower()
        if decision not in ("pass", "uncertain", "blocked"):
            raise LedgerError(
                f"resource review row {index} decision must be pass, uncertain, or blocked"
            )
        evidence = value["evidence"]
        if not isinstance(evidence, list) or not all(
            isinstance(item, str) and item.strip() for item in evidence
        ):
            raise LedgerError(
                f"resource review row {index} evidence must be non-empty strings"
            )
        normalized.append(
            {
                "field": str(value["field"]).strip(),
                "requested": value["requested"],
                "need": value["need"],
                "headroom": value["headroom"],
                "evidence": list(dict.fromkeys(evidence)),
                "decision": decision,
            }
        )
    return {"summary": summary, "rows": normalized}


def normalized_repair_closure(payload: object) -> tuple[str, list[dict[str, object]]]:
    if not isinstance(payload, dict):
        raise LedgerError("repair closure must be a JSON object")
    summary = str(payload.get("summary", "")).strip()
    values = payload.get("closures")
    if not summary or not isinstance(values, list) or not values:
        raise LedgerError("repair closure requires summary and non-empty closures")
    closures: list[dict[str, object]] = []
    seen: set[str] = set()
    for index, value in enumerate(values, start=1):
        if not isinstance(value, dict):
            raise LedgerError(f"repair closure {index} must be an object")
        finding_id = str(value.get("id", "")).strip()
        if not finding_id or finding_id in seen:
            raise LedgerError(
                f"repair closure {index} must have a unique non-empty id"
            )
        seen.add(finding_id)
        closure_summary = str(value.get("summary", "")).strip()
        changed_paths = value.get("changed_paths", [])
        tests = value.get("tests", [])
        if not closure_summary:
            raise LedgerError(f"repair closure {finding_id} requires a summary")
        if not isinstance(changed_paths, list) or not all(
            isinstance(path, str) and path.strip() for path in changed_paths
        ):
            raise LedgerError(
                f"repair closure {finding_id} changed_paths must be strings"
            )
        if not isinstance(tests, list) or not all(
            isinstance(command, str) and command.strip() for command in tests
        ):
            raise LedgerError(f"repair closure {finding_id} tests must be strings")
        closures.append(
            {
                "id": finding_id,
                "summary": closure_summary,
                "changed_paths": sorted(set(changed_paths)),
                "tests": list(dict.fromkeys(tests)),
            }
        )
    return summary, closures


def command_review_context(root: Path, args: argparse.Namespace) -> None:
    data = load_registry(root / DEFAULT_REGISTRY)
    item = find_experiment(data, args.experiment_id)
    errors, contract = contract_errors(root, item)
    if errors or contract is None:
        raise LedgerError("contract is not reviewable: " + "; ".join(errors))
    requested_scope = getattr(args, "scope", None)
    resolved_scope, config = scope_config(contract, requested_scope)
    if config is None:
        critical_paths = list(
            dict.fromkeys(
                contract.get("launch_critical_paths")
                or contract.get("review_paths", [])
            )
        )
        operational_paths: list[object] = []
    else:
        critical_paths = list(
            dict.fromkeys(
                scope_list(contract, resolved_scope, "critical_paths", "review_paths")
            )
        )
        operational_paths = list(
            dict.fromkeys(
                scope_list(
                    contract, resolved_scope, "operational_paths", "review_paths"
                )
            )
        )
    record = review_record(item, resolved_scope)
    payload: dict[str, object] = {
        "experiment_id": args.experiment_id,
        "launch_scope": resolved_scope,
        "review_mode": args.mode,
        "review_status": record.get("review_status", "required"),
        "reviewed_at": record.get("reviewed_at"),
        "git_head": git_head(root),
        "git_dirty_paths": git_dirty_paths(
            root, [*critical_paths, *operational_paths, item["contract_path"]]
        ),
        "contract_path": item["contract_path"],
        "launch_critical_paths": critical_paths,
        "operational_paths": operational_paths,
    }
    anchor_heading = item.get("intent_anchor_section")
    if isinstance(anchor_heading, str):
        spec_path = root / "docs/experiments" / str(item["spec"])
        payload["intent_anchor"] = markdown_section(spec_path, anchor_heading)
    if args.mode == "delta":
        reason = delta_review_precondition(record)
        if reason:
            raise LedgerError(reason)
        payload["previous_review_summary"] = record.get("review_summary")
    else:
        allowed_launchers = (
            contract["allowed_launchers"]
            if config is None
            else config["allowed_launchers"]
        )
        required_tests = (
            contract["required_tests"]
            if config is None
            else config["required_tests"]
        )
        operational_tests = [] if config is None else config.get(
            "operational_tests", []
        )
        payload.update(
            {
                "frozen_spec_section": contract["frozen_spec_section"],
                "review_paths": critical_paths,
                "invariants": contract["invariants"],
                "training_contract": contract.get("training_contract", {}),
                "efficiency_contract": contract.get("efficiency_contract", {}),
                "resource_contract": contract.get("resource_contract", {}),
                "data_contract": contract.get("data_contract", {}),
                "evaluation_contract": contract.get("evaluation_contract", {}),
                "resource_contract": contract.get("resource_contract", {}),
                "efficiency_contract": contract.get("efficiency_contract", {}),
                "allowed_launchers": allowed_launchers,
                "required_tests": required_tests,
                "operational_tests": operational_tests,
            }
        )
    print(json.dumps(payload, indent=2, ensure_ascii=False))


def command_record_review(root: Path, args: argparse.Namespace) -> None:
    registry_path = root / DEFAULT_REGISTRY
    data = load_registry(registry_path)
    item = find_experiment(data, args.experiment_id)
    errors, contract = contract_errors(root, item)
    if errors or contract is None:
        raise LedgerError("cannot record review: " + "; ".join(errors))
    requested_scope = getattr(args, "scope", None)
    resolved_scope, config = scope_config(contract, requested_scope)
    record = review_record(item, resolved_scope, create=True)
    if args.mode == "delta":
        reason = delta_review_precondition(record)
        if reason:
            raise LedgerError(reason)
    operational_paths = (
        []
        if config is None
        else scope_list(
            contract, resolved_scope, "operational_paths", "review_paths"
        )
    )
    findings_file = getattr(args, "findings_file", None)
    findings = (
        normalized_review_findings(
            load_json_file(root, findings_file, "review findings")
        )
        if findings_file
        else []
    )
    resource_review_file = getattr(args, "resource_review_file", None)
    resource_review = (
        normalized_resource_review(
            load_json_file(root, resource_review_file, "resource review")
        )
        if resource_review_file
        else None
    )
    if args.status == "pass" and resource_review is not None:
        if any(row["decision"] == "blocked" for row in resource_review["rows"]):
            raise LedgerError(
                "cannot record pass: resource review contains demonstrated blockers"
            )
    if args.status == "pass":
        required_tests = (
            contract["required_tests"]
            if config is None
            else config["required_tests"]
        )
        operational_tests = [] if config is None else config.get(
            "operational_tests", []
        )
        commands = list(dict.fromkeys([*required_tests, *operational_tests]))
        test_results = run_required_tests(root, commands)
        failures = [
            result for result in test_results if result["returncode"] != 0
        ]
        if failures:
            commands = ", ".join(str(result["command"]) for result in failures)
            raise LedgerError(f"cannot record pass: required tests failed: {commands}")
    record["review_status"] = args.status
    record["review_mode"] = args.mode
    record["reviewed_at"] = utc_now()
    record["reviewer"] = args.reviewer
    record["review_summary"] = args.summary
    record["review_findings"] = findings
    if resource_review is not None:
        record["resource_review"] = resource_review
    else:
        record.pop("resource_review", None)
    for obsolete in (
        "reviewed_source_digest",
        "reviewed_contract_sha256",
        "reviewed_path_states",
        "reviewed_path_hashes",
        "reviewed_intent_anchor_sha256",
        "operational_source_digest",
        "operational_path_states",
        "operational_path_hashes",
    ):
        record.pop(obsolete, None)
    for field in (
        "repair_closure",
        "repair_closure_actor",
        "repair_closure_at",
        "repair_test_results",
        "approval_basis",
    ):
        record.pop(field, None)
    if args.status == "pass" and operational_paths:
        record["operational_validated_at"] = utc_now()
        record["operational_validator"] = args.reviewer
        record["operational_summary"] = "validated with the scientific review"
    data["updated_at"] = utc_now()
    write_registry(registry_path, data)
    scope_text = f" scope {resolved_scope}" if resolved_scope else ""
    print(f"recorded {args.status} review for {args.experiment_id}{scope_text}")


def command_close_review_findings(root: Path, args: argparse.Namespace) -> None:
    registry_path = root / DEFAULT_REGISTRY
    data = load_registry(registry_path)
    item = find_experiment(data, args.experiment_id)
    errors, contract = contract_errors(root, item)
    if errors or contract is None:
        raise LedgerError("cannot close review findings: " + "; ".join(errors))
    requested_scope = getattr(args, "scope", None)
    resolved_scope, config = scope_config(contract, requested_scope)
    record = review_record(item, resolved_scope, create=True)
    if record.get("review_status") not in ("fail", "blocked"):
        raise LedgerError(
            "repair closure requires a previous fail or blocked review"
        )
    findings = record.get("review_findings")
    if not isinstance(findings, list) or not findings:
        raise LedgerError(
            "blocked review has no structured findings; delta review is required"
        )
    reviewer_findings = [
        str(finding.get("id"))
        for finding in findings
        if isinstance(finding, dict)
        and finding.get("closure_mode", "proof") == "reviewer"
    ]
    if reviewer_findings:
        raise LedgerError(
            "delta review is required for reviewer-closure findings: "
            + ", ".join(reviewer_findings)
        )

    closure_payload = load_json_file(
        root, args.evidence_file, "repair closure"
    )
    closure_summary, closures = normalized_repair_closure(closure_payload)
    repaired_resource_review = (
        normalized_resource_review(closure_payload["resource_review"])
        if isinstance(closure_payload, dict)
        and "resource_review" in closure_payload
        else None
    )
    finding_ids = {
        str(finding.get("id"))
        for finding in findings
        if isinstance(finding, dict)
    }
    closure_ids = {str(closure["id"]) for closure in closures}
    if closure_ids != finding_ids:
        missing = sorted(finding_ids - closure_ids)
        unknown = sorted(closure_ids - finding_ids)
        details: list[str] = []
        if missing:
            details.append("missing " + ", ".join(missing))
        if unknown:
            details.append("unknown " + ", ".join(unknown))
        raise LedgerError(
            "repair closure must cover every reviewed finding: "
            + "; ".join(details)
        )

    declared_paths = {
        str(path)
        for closure in closures
        for path in closure["changed_paths"]
    }
    critical_paths = {
        str(value)
        for value in (
            contract.get("review_paths", [])
            if config is None
            else scope_list(
                contract, resolved_scope, "critical_paths", "review_paths"
            )
        )
    }
    unknown_paths = sorted(declared_paths - critical_paths)
    if unknown_paths:
        raise LedgerError(
            "repair closure names paths outside the reviewed scope: "
            + ", ".join(unknown_paths)
        )

    required_tests = (
        contract["required_tests"]
        if config is None
        else config["required_tests"]
    )
    operational_tests = [] if config is None else config.get(
        "operational_tests", []
    )
    closure_tests = [
        str(command)
        for closure in closures
        for command in closure["tests"]
    ]
    commands = list(
        dict.fromkeys([*closure_tests, *required_tests, *operational_tests])
    )
    if not closure_tests:
        raise LedgerError(
            "repair closure requires at least one focused regression test"
        )
    test_results = run_required_tests(root, commands)
    failures = [
        result for result in test_results if result["returncode"] != 0
    ]
    if failures:
        failed = ", ".join(str(result["command"]) for result in failures)
        raise LedgerError(
            f"cannot close review findings: required tests failed: {failed}"
        )

    operational_paths = (
        []
        if config is None
        else scope_list(
            contract, resolved_scope, "operational_paths", "review_paths"
        )
    )
    record["review_status"] = "repaired"
    record["repair_closure"] = {
        "summary": closure_summary,
        "closures": closures,
    }
    record["repair_closure_actor"] = args.actor
    record["repair_closure_at"] = utc_now()
    record["repair_test_results"] = [
        {
            "command": result["command"],
            "returncode": result["returncode"],
        }
        for result in test_results
    ]
    record["approval_basis"] = (
        "independent_review_plus_main_agent_proof_closure"
    )
    if repaired_resource_review is not None:
        if any(
            row["decision"] == "blocked"
            for row in repaired_resource_review["rows"]
        ):
            raise LedgerError(
                "repair closure resource review still has a BLOCKED row"
            )
        record["resource_review"] = repaired_resource_review
    for obsolete in (
        "reviewed_source_digest",
        "reviewed_contract_sha256",
        "reviewed_path_states",
        "reviewed_path_hashes",
        "reviewed_intent_anchor_sha256",
        "operational_source_digest",
        "operational_path_states",
        "operational_path_hashes",
    ):
        record.pop(obsolete, None)
    if operational_paths:
        record["operational_validated_at"] = utc_now()
        record["operational_validator"] = args.actor
        record["operational_summary"] = "validated with repair closure"
    data["updated_at"] = utc_now()
    write_registry(registry_path, data)
    scope_text = f" scope {resolved_scope}" if resolved_scope else ""
    print(
        f"closed review findings for {args.experiment_id}{scope_text}; "
        "status repaired"
    )


def command_record_operational(root: Path, args: argparse.Namespace) -> None:
    registry_path = root / DEFAULT_REGISTRY
    data = load_registry(registry_path)
    item = find_experiment(data, args.experiment_id)
    errors, contract = contract_errors(root, item)
    if errors or contract is None:
        raise LedgerError(
            "cannot record operational validation: " + "; ".join(errors)
        )
    requested_scope = getattr(args, "scope", None)
    resolved_scope, config = scope_config(contract, requested_scope)
    if config is None:
        raise LedgerError(
            "operational validation requires a scoped contract with "
            "operational_paths"
        )
    current, reason, _review_basis = review_is_current(root, item, resolved_scope)
    if not current:
        raise LedgerError(
            "operational validation cannot refresh a stale scientific review: "
            + reason
        )
    operational_paths = scope_list(
        contract, resolved_scope, "operational_paths", "review_paths"
    )
    if not operational_paths:
        raise LedgerError(
            f"launch scope {resolved_scope!r} has no operational_paths"
        )
    test_results = run_required_tests(
        root, config.get("operational_tests", [])
    )
    failures = [result for result in test_results if result["returncode"] != 0]
    if failures:
        commands = ", ".join(str(result["command"]) for result in failures)
        raise LedgerError(
            f"cannot record operational validation: tests failed: {commands}"
        )
    record = review_record(item, resolved_scope, create=True)
    for obsolete in (
        "operational_source_digest",
        "operational_path_states",
        "operational_path_hashes",
    ):
        record.pop(obsolete, None)
    record["operational_validated_at"] = utc_now()
    record["operational_validator"] = args.actor
    record["operational_summary"] = args.summary
    data["updated_at"] = utc_now()
    write_registry(registry_path, data)
    print(
        f"recorded operational validation for {args.experiment_id} "
        f"scope {resolved_scope}"
    )


def normalized_command(args: argparse.Namespace) -> list[str]:
    command = list(args.launch_command)
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        raise LedgerError("launch command is required after --")
    return command


def current_preflight_receipt(
    root: Path,
    *,
    item: dict[str, object],
    contract: dict[str, object],
    scope: str | None,
    config: dict[str, object] | None,
    command: list[str],
    review_basis: str,
) -> tuple[str, Path | None, dict[str, object] | None]:
    launcher = command_launcher(command)
    if launcher is None or execution_kind_for_launcher(
        contract, config, launcher
    ) != "training":
        return "not_required", None, None
    try:
        definition = training_preflight_definition(contract, config)
        fingerprint, identity = preflight_identity(
            root, item, contract, scope, command, definition, review_basis
        )
    except LedgerError:
        return "missing_definition", None, None
    candidate = preflight_receipt_path(root, str(item["id"]), fingerprint)
    if not candidate.is_file():
        return "missing", None, None
    receipt = json.loads(candidate.read_text(encoding="utf-8"))
    if receipt.get("identity") != identity or receipt.get("status") != "passed":
        return "stale_or_failed", None, None
    return "passed", candidate, receipt


def load_slurm_snapshot(root: Path, value: str | None) -> dict[str, object] | None:
    if value is None:
        return None
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    if not path.is_file():
        raise LedgerError(f"Slurm snapshot does not exist: {path}")
    snapshot = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(snapshot, dict) or snapshot.get("schema_version") != 1:
        raise LedgerError("Slurm snapshot must be a schema_version 1 object")
    for field in ("jobs", "recent_jobs"):
        if not isinstance(snapshot.get(field), list):
            raise LedgerError(f"Slurm snapshot {field} must be a list")
    return snapshot


def launch_manifests(root: Path, experiment_id: str) -> list[dict[str, object]]:
    manifests: list[dict[str, object]] = []
    for path in sorted((root / "slurm" / experiment_id).glob("launch-manifest-*.json")):
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            raise LedgerError(f"cannot read launch manifest {path}: {error}") from error
        if isinstance(value, dict) and value.get("experiment_id") == experiment_id:
            value = dict(value)
            value["manifest_path"] = str(path.relative_to(root))
            manifests.append(value)
    return manifests


def evidence_record(
    root: Path, values: Sequence[object], launched_at: object
) -> dict[str, object]:
    launch_time: datetime | None = None
    if isinstance(launched_at, str) and launched_at:
        try:
            launch_time = datetime.fromisoformat(launched_at.replace("Z", "+00:00"))
        except ValueError:
            launch_time = None
    paths: list[dict[str, object]] = []
    for value in values:
        path = Path(str(value))
        resolved = path if path.is_absolute() else root / path
        exists = resolved.exists()
        modified_at = (
            datetime.fromtimestamp(resolved.stat().st_mtime, timezone.utc)
            if exists
            else None
        )
        fresh = bool(
            exists
            and launch_time is not None
            and modified_at is not None
            and modified_at >= launch_time
        )
        paths.append(
            {
                "path": str(value),
                "exists": exists,
                "fresh_since_launch": fresh,
            }
        )
    return {
        "declared": bool(paths),
        "complete": bool(paths)
        and all(bool(path["fresh_since_launch"]) for path in paths),
        "paths": paths,
    }


def scheduler_state_for_job(
    snapshot: dict[str, object] | None, job_id: object
) -> str | None:
    if snapshot is None or not isinstance(job_id, str):
        return None
    for field in ("jobs", "recent_jobs"):
        for job in snapshot.get(field, []):
            if not isinstance(job, dict):
                continue
            if str(job.get("job_id", "")).split(".", 1)[0] == job_id:
                state = str(job.get("state", "")).split()[0].rstrip("+")
                return state or None
    return None


def compile_stage_closure(
    root: Path,
    *,
    experiment_id: str,
    contract: dict[str, object],
    snapshot: dict[str, object] | None,
) -> dict[str, object]:
    scopes = launch_scopes(contract)
    stage_configs: dict[str, dict[str, object]] = scopes or {"default": contract}
    manifests = launch_manifests(root, experiment_id)
    stages: list[dict[str, object]] = []
    completed: list[str] = []
    for name, config in stage_configs.items():
        scope_manifests = [
            manifest
            for manifest in manifests
            if manifest.get("launch_scope") == (None if name == "default" else name)
        ]
        latest = max(
            scope_manifests,
            key=lambda value: str(value.get("launched_at", "")),
            default=None,
        )
        evidence = evidence_record(
            root,
            config.get("completion_evidence", []),
            None if latest is None else latest.get("launched_at"),
        )
        scheduler_state = scheduler_state_for_job(
            snapshot, None if latest is None else latest.get("slurm_job_id")
        )
        if evidence["complete"] and scheduler_state == "COMPLETED":
            state = "completed"
            completed.append(name)
        elif scheduler_state in {"PENDING", "CONFIGURING"}:
            state = "queued"
        elif scheduler_state in {"RUNNING", "COMPLETING"}:
            state = "running"
        elif latest is None:
            state = "not_launched"
        elif scheduler_state is not None:
            state = "terminal_unverified"
        else:
            state = "launched_untracked"
        stages.append(
            {
                "stage": name,
                "execution_kind": config.get("execution_kind", "ambiguous"),
                "depends_on": config.get("depends_on", []),
                "state": state,
                "completion_evidence": evidence,
                "latest_launch": latest,
                "scheduler_state": scheduler_state,
            }
        )
    declared = list(stage_configs)
    return {
        "declared": declared,
        "completed": completed,
        "remaining": [name for name in declared if name not in completed],
        "stages": stages,
    }


def command_launch_packet(root: Path, args: argparse.Namespace) -> None:
    data = load_registry(root / DEFAULT_REGISTRY)
    item = find_experiment(data, args.experiment_id)
    errors, contract = contract_errors(root, item)
    if errors or contract is None:
        raise LedgerError("cannot compile launch packet: " + "; ".join(errors))
    command = normalized_command(args)
    scope, config = resolve_launch_scope(contract, args.scope, command)
    launcher = command_launcher(command)
    allowed_launchers = (
        contract["allowed_launchers"] if config is None else config["allowed_launchers"]
    )
    command_allowed = command_uses_allowed_launcher(command, allowed_launchers)
    review_current, review_reason, review_basis = review_is_current(root, item, scope)
    operational_current, operational_reason, operational_basis = operational_is_current(
        root, item, contract, scope
    )
    snapshot = load_slurm_snapshot(root, args.slurm_snapshot)
    closure = compile_stage_closure(
        root,
        experiment_id=args.experiment_id,
        contract=contract,
        snapshot=snapshot,
    )
    selected_stage = next(
        stage
        for stage in closure["stages"]
        if stage["stage"] == (scope or "default")
    )
    dependency_states = {
        stage["stage"]: stage["state"] for stage in closure["stages"]
    }
    unmet_dependencies = [
        name
        for name in selected_stage["depends_on"]
        if dependency_states.get(name) != "completed"
    ]
    preflight_status = "unknown"
    preflight_path: Path | None = None
    if review_basis is not None:
        preflight_status, preflight_path, _receipt = current_preflight_receipt(
            root,
            item=item,
            contract=contract,
            scope=scope,
            config=config,
            command=command,
            review_basis=review_basis,
        )
    blockers: list[str] = []
    if not review_current:
        blockers.append(review_reason)
    if not command_allowed:
        blockers.append("command does not use an allowed contract launcher")
    if preflight_status not in {"passed", "not_required"}:
        blockers.append(f"training preflight is {preflight_status}")
    if unmet_dependencies:
        blockers.append("unfinished dependencies: " + ", ".join(unmet_dependencies))
    packet = {
        "schema_version": 1,
        "compiled_at": utc_now(),
        "experiment_id": args.experiment_id,
        "lifecycle": item.get("lifecycle"),
        "launch_scope": scope,
        "stage_closure": closure,
        "launch": {
            "command": command,
            "launcher": launcher,
            "command_allowed": command_allowed,
            "execution_kind": (
                "ambiguous"
                if launcher is None
                else execution_kind_for_launcher(contract, config, launcher)
            ),
            "review_current": review_current,
            "review_note": review_reason,
            "operational_validation_current": operational_current,
            "operational_validation_note": operational_reason,
            "operational_validation_basis": operational_basis,
            "training_preflight_status": preflight_status,
            "training_preflight_receipt": (
                None if preflight_path is None else str(preflight_path.relative_to(root))
            ),
            "unmet_dependencies": unmet_dependencies,
            "ready": not blockers,
            "blockers": blockers,
        },
        "slurm_snapshot": (
            None
            if snapshot is None
            else {
                "captured_at": snapshot.get("captured_at"),
                "user": snapshot.get("user"),
                "strategy_input": snapshot.get("strategy_input"),
                "sources": snapshot.get("sources"),
            }
        ),
    }
    text = json.dumps(packet, indent=2, ensure_ascii=False) + "\n"
    if args.output is None:
        print(text, end="")
    else:
        output = Path(args.output)
        if not output.is_absolute():
            output = root / output
        output.parent.mkdir(parents=True, exist_ok=True)
        temporary = output.with_suffix(output.suffix + ".tmp")
        temporary.write_text(text, encoding="utf-8")
        os.replace(temporary, output)
        print(output)


def begin_async_launch(
    root: Path,
    *,
    experiment_id: str,
    review_basis: str,
    command: list[str],
) -> tuple[object, Path] | tuple[None, None]:
    """Create one durable intent per reviewed async command before execution."""
    if os.environ.get("RESEARCH_LOOP_RESEARCH_ASYNC") != "1":
        return None, None
    payload = {
        "schema_version": 1,
        "experiment_id": experiment_id,
        "review_basis": review_basis,
        "command": command,
    }
    fingerprint = sha256_bytes(
        json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    )
    launch_root = root / "slurm" / experiment_id / "async-launches"
    launch_root.mkdir(parents=True, exist_ok=True)
    lock = (launch_root / "launch.lock").open("a+", encoding="utf-8")
    fcntl.flock(lock.fileno(), fcntl.LOCK_EX)
    intent_path = launch_root / f"{fingerprint}.json"
    if intent_path.exists():
        previous = json.loads(intent_path.read_text(encoding="utf-8"))
        lock.close()
        raise LedgerError(
            "async launch blocked: this exact reviewed command already has a "
            f"durable intent at {intent_path.relative_to(root)} "
            f"(status={previous.get('status', 'unknown')}); reconcile it "
            "instead of submitting a duplicate"
        )
    payload.update(
        {
            "fingerprint": fingerprint,
            "status": "submission_unknown",
            "created_at": utc_now(),
        }
    )
    descriptor = os.open(
        intent_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644
    )
    with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, ensure_ascii=False)
        handle.write("\n")
        handle.flush()
        os.fsync(handle.fileno())
    return lock, intent_path


def complete_async_launch(
    intent_path: Path | None,
    *,
    returncode: int,
    job_id: str | None,
    manifest_path: Path,
) -> None:
    if intent_path is None:
        return
    payload = json.loads(intent_path.read_text(encoding="utf-8"))
    payload.update(
        {
            "status": "submitted" if returncode == 0 else "submission_unknown",
            "returncode": returncode,
            "slurm_job_id": job_id,
            "manifest_path": str(manifest_path),
            "updated_at": utc_now(),
        }
    )
    temporary = intent_path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, intent_path)


def unique_launch_manifest_path(
    directory: Path,
    stamp: str,
    job_id: str | None,
) -> Path:
    suffix = f"-{job_id}" if job_id is not None else ""
    candidate = directory / f"launch-manifest-{stamp}{suffix}.json"
    collision = 1
    while candidate.exists():
        candidate = directory / (
            f"launch-manifest-{stamp}{suffix}-{collision:02d}.json"
        )
        collision += 1
    return candidate


def command_launcher(command: Sequence[str]) -> str | None:
    """Return the actual script/executable entrypoint for supported launch forms."""
    words = [str(token) for token in command]
    index = 0
    while index < len(words) and (
        "=" in words[index] and not words[index].startswith(("/", "./"))
    ):
        index += 1
    if index >= len(words):
        return None
    executable = Path(words[index]).name
    tail = words[index + 1 :]
    if executable == "env":
        nested = 0
        while nested < len(tail) and (
            tail[nested].startswith("-") or "=" in tail[nested]
        ):
            nested += 1
        return command_launcher(tail[nested:])
    if executable == "sbatch":
        if any(token == "--wrap" or token.startswith("--wrap=") for token in tail):
            return None
        positional = False
        for token in tail:
            if token == "--":
                positional = True
                continue
            if not positional and token.startswith("-"):
                continue
            return token.removeprefix("./")
        return None
    if executable in {"bash", "sh", "zsh"} or executable.startswith("python"):
        if any(token in {"-c", "-lc", "-m"} for token in tail):
            return None
        for token in tail:
            if token == "--":
                continue
            if token.startswith("-"):
                continue
            return token.removeprefix("./")
        return None
    return words[index].removeprefix("./")


def command_uses_allowed_launcher(
    command: Sequence[str], allowed_launchers: Sequence[object]
) -> bool:
    launcher = command_launcher(command)
    allowed = {
        value.removeprefix("./")
        for value in allowed_launchers
        if isinstance(value, str)
    }
    return launcher is not None and launcher in allowed


def resolve_launch_scope(
    contract: dict[str, object],
    requested_scope: str | None,
    command: Sequence[str],
) -> tuple[str | None, dict[str, object] | None]:
    scopes = launch_scopes(contract)
    if not scopes:
        return scope_config(contract, requested_scope)
    if requested_scope is not None:
        return scope_config(contract, requested_scope)
    matches = [
        name
        for name, config in scopes.items()
        if command_uses_allowed_launcher(
            command, config.get("allowed_launchers", [])
        )
    ]
    if len(matches) == 1:
        return matches[0], scopes[matches[0]]
    if not matches:
        raise LedgerError(
            "launch command does not resolve to any launch scope; pass --scope"
        )
    raise LedgerError(
        "launch command matches multiple launch scopes; pass --scope explicitly: "
        + ", ".join(sorted(matches))
    )


def execution_kind_for_launcher(
    contract: dict[str, object],
    config: dict[str, object] | None,
    launcher: str,
) -> str:
    normalized_launcher = launcher.removeprefix("./")
    for owner in (config, contract):
        if not isinstance(owner, dict):
            continue
        mapping = owner.get("launcher_kinds")
        if isinstance(mapping, dict):
            for path, kind in mapping.items():
                if (
                    isinstance(path, str)
                    and path.removeprefix("./") == normalized_launcher
                    and kind in EXECUTION_KINDS
                ):
                    return str(kind)
        kind = owner.get("execution_kind")
        if kind in EXECUTION_KINDS:
            return str(kind)

    name = Path(normalized_launcher).stem.lower()
    if "train" in name or "pretrain" in name:
        return "training"
    if any(
        token in name
        for token in (
            "eval",
            "render",
            "benchmark",
            "analy",
            "prepare",
            "build",
            "cache",
        )
    ):
        return "evaluation" if "eval" in name else "analysis"
    return "ambiguous"


def training_preflight_definition(
    contract: dict[str, object], config: dict[str, object] | None
) -> dict[str, object]:
    value = None if config is None else config.get("training_preflight")
    if value is None:
        value = contract.get("training_preflight")
    if value is None:
        raise LedgerError(
            "training launch has no training_preflight; declare real CPU checks "
            "and a local or non-queueing GPU check in its contract scope"
        )
    try:
        _, pf = load_scheduler_adapters()
        return pf.validate_definition(value)
    except Exception as error:
        if type(error).__name__ != "PreflightError":
            raise
        raise LedgerError(f"invalid training_preflight: {error}") from error


def preflight_identity(
    root: Path,
    item: dict[str, object],
    contract: dict[str, object],
    scope: str | None,
    command: list[str],
    definition: dict[str, object],
    review_basis: str,
) -> tuple[str, dict[str, object]]:
    launcher = command_launcher(command)
    if launcher is None:
        raise LedgerError("cannot identify the launcher for training preflight")
    safe_repo_path(root, launcher, "training launcher")
    payload = {
        "schema_version": 1,
        "experiment_id": item["id"],
        "launch_scope": scope,
        "review_basis": review_basis,
        "launch_command": command,
        "launcher": launcher,
        "training_preflight": definition,
    }
    fingerprint = sha256_bytes(
        json.dumps(
            payload, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    )
    return fingerprint, payload


def preflight_receipt_path(root: Path, experiment_id: str, fingerprint: str) -> Path:
    return root / "slurm" / experiment_id / "preflights" / f"{fingerprint}.json"


def preflight_environment(
    command: Sequence[str],
) -> dict[str, str]:
    env = os.environ.copy()
    tokens = list(command)
    index = 0
    if tokens and Path(tokens[0]).name == "env":
        index = 1
        while index < len(tokens) and tokens[index].startswith("-"):
            index += 1
    for token in tokens[index:]:
        if "=" not in token or token.startswith(("/", "./")):
            break
        key, value = token.split("=", 1)
        if not re.match(r"^[A-Za-z_][A-Za-z0-9_]*$", key):
            break
        env[key] = value
    env["RESEARCH_LOOP_TRAINING_PREFLIGHT"] = "1"
    env["RESEARCH_LOOP_FORMAL_LAUNCH_COMMAND_JSON"] = json.dumps(list(command))
    return env


def run_training_preflight(
    root: Path,
    *,
    item: dict[str, object],
    contract: dict[str, object],
    scope: str | None,
    command: list[str],
    review_basis: str,
    force: bool = False,
) -> tuple[Path, dict[str, object]]:
    _resolved_scope, config = scope_config(contract, scope)
    definition = training_preflight_definition(contract, config)
    fingerprint, identity = preflight_identity(
        root, item, contract, scope, command, definition, review_basis
    )
    receipt_path = preflight_receipt_path(
        root, str(item["id"]), fingerprint
    )
    if receipt_path.is_file() and not force:
        receipt = json.loads(receipt_path.read_text(encoding="utf-8"))
        if receipt.get("identity") == identity and receipt.get("status") == "passed":
            return receipt_path, receipt

    _, pf = load_scheduler_adapters()
    result = pf.run_preflight(
        definition,
        root=root,
        env=preflight_environment(command),
    )
    receipt = {
        "schema_version": 1,
        "created_at": utc_now(),
        "fingerprint": fingerprint,
        "identity": identity,
        **result,
    }
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    temporary = receipt_path.with_suffix(".tmp")
    temporary.write_text(
        json.dumps(receipt, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, receipt_path)
    if result["status"] != "passed":
        raise LedgerError(
            "training preflight failed; inspect "
            f"{receipt_path.relative_to(root)}"
        )
    return receipt_path, receipt


def command_preflight(root: Path, args: argparse.Namespace) -> None:
    data = load_registry(root / DEFAULT_REGISTRY)
    item = find_experiment(data, args.experiment_id)
    contract = load_contract(root, item)
    command = normalized_command(args)
    resolved_scope, config = resolve_launch_scope(contract, args.scope, command)
    current, reason, review_basis = review_is_current(
        root, item, resolved_scope
    )
    if not current or review_basis is None:
        raise LedgerError(f"preflight blocked: {reason}")
    allowed_launchers = (
        contract["allowed_launchers"]
        if config is None
        else config["allowed_launchers"]
    )
    if not command_uses_allowed_launcher(command, allowed_launchers):
        raise LedgerError(
            "preflight blocked: command does not use an allowed contract launcher"
        )
    launcher = command_launcher(command)
    if launcher is None or execution_kind_for_launcher(
        contract, config, launcher
    ) != "training":
        raise LedgerError("preflight is required only for a training launcher")
    receipt_path, receipt = run_training_preflight(
        root,
        item=item,
        contract=contract,
        scope=resolved_scope,
        command=command,
        review_basis=review_basis,
        force=args.force,
    )
    print(
        json.dumps(
            {
                "status": receipt["status"],
                "gpu_status": receipt["gpu_check"]["status"],
                "receipt": str(receipt_path.relative_to(root)),
            },
            indent=2,
        )
    )


def command_launch(root: Path, args: argparse.Namespace) -> None:
    registry_path = root / DEFAULT_REGISTRY
    data = load_registry(registry_path)
    item = find_experiment(data, args.experiment_id)
    contract = load_contract(root, item)
    command = normalized_command(args)
    requested_scope = getattr(args, "scope", None)
    resolved_scope, config = resolve_launch_scope(
        contract, requested_scope, command
    )
    current, reason, review_basis = review_is_current(root, item, resolved_scope)
    if not current or review_basis is None:
        raise LedgerError(f"launch blocked: {reason}")
    operational_current, operational_reason, operational_basis = (
        operational_is_current(root, item, contract, resolved_scope)
    )
    allowed_launchers = (
        contract["allowed_launchers"]
        if config is None
        else config["allowed_launchers"]
    )
    if not command_uses_allowed_launcher(command, allowed_launchers):
        raise LedgerError(
            "launch blocked: command does not use an allowed launcher from the contract"
        )
    launcher = command_launcher(command)
    if launcher is None:
        raise LedgerError("launch blocked: cannot identify the allowed launcher")
    execution_kind = execution_kind_for_launcher(contract, config, launcher)
    preflight_status, preflight_path, preflight_receipt = current_preflight_receipt(
        root,
        item=item,
        contract=contract,
        scope=resolved_scope,
        config=config,
        command=command,
        review_basis=review_basis,
    )
    if args.dry_run:
        print(
            json.dumps(
                {
                    "experiment_id": args.experiment_id,
                    "launch_scope": resolved_scope,
                    "review_status": review_record(
                        item, resolved_scope
                    ).get("review_status"),
                    "approval_basis": review_record(
                        item, resolved_scope
                    ).get("approval_basis", "independent_review_pass"),
                    "provenance_degraded": False,
                    "promotable": True,
                    "execution_kind": execution_kind,
                    "training_preflight_status": preflight_status,
                    "training_preflight_receipt": (
                        None
                        if preflight_path is None
                        else str(preflight_path.relative_to(root))
                    ),
                    "operational_validation_current": operational_current,
                    "operational_validation_note": operational_reason,
                    "operational_validation_basis": operational_basis,
                    "command": command,
                },
                indent=2,
            )
        )
        return

    if execution_kind == "ambiguous":
        raise LedgerError(
            "launch blocked: ambiguous launcher kind; declare execution_kind or "
            "launcher_kinds in the contract before submission"
        )
    if execution_kind == "training" and preflight_status != "passed":
        preflight_path, preflight_receipt = run_training_preflight(
            root,
            item=item,
            contract=contract,
            scope=resolved_scope,
            command=command,
            review_basis=review_basis,
        )
        preflight_status = "passed"

    async_lock, async_intent = begin_async_launch(
        root,
        experiment_id=args.experiment_id,
        review_basis=review_basis,
        command=command,
    )
    try:
        launched_at = utc_now()
        launch_env = os.environ.copy()
        result = subprocess.run(
            command,
            cwd=root,
            check=False,
            capture_output=True,
            text=True,
            env=launch_env,
        )
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        job_match = JOB_ID_RE.search(result.stdout)
        job_id = job_match.group(1) if job_match else None
        manifest = {
            "schema_version": 1,
            "experiment_id": args.experiment_id,
            "launch_scope": resolved_scope,
            "launched_at": launched_at,
            "git_head": git_head(root),
            "git_dirty_paths": git_dirty_paths(root),
            "contract_path": item["contract_path"],
            "provenance_degraded": False,
            "promotable": True,
            "execution_kind": execution_kind,
            "operational_validation_current": operational_current,
            "operational_validation_note": operational_reason,
            "operational_validation_basis": operational_basis,
            "training_preflight_status": preflight_status,
            "training_preflight_receipt": (
                None
                if preflight_path is None
                else str(preflight_path.relative_to(root))
            ),
            "training_preflight_gpu_status": (
                None
                if preflight_receipt is None
                else preflight_receipt["gpu_check"]["status"]
            ),
            "reviewer": review_record(item, resolved_scope).get("reviewer"),
            "reviewed_at": review_record(item, resolved_scope).get("reviewed_at"),
            "review_status": review_record(item, resolved_scope).get(
                "review_status"
            ),
            "approval_basis": review_record(item, resolved_scope).get(
                "approval_basis", "independent_review_pass"
            ),
            "repair_closure_actor": review_record(item, resolved_scope).get(
                "repair_closure_actor"
            ),
            "repair_closure_at": review_record(item, resolved_scope).get(
                "repair_closure_at"
            ),
            "operational_validator": review_record(item, resolved_scope).get(
                "operational_validator"
            ),
            "operational_validated_at": review_record(item, resolved_scope).get(
                "operational_validated_at"
            ),
            "command": command,
            "returncode": result.returncode,
            "slurm_job_id": job_id,
        }
        stamp = launched_at.replace(":", "").replace("+00:00", "Z")
        manifest_path = unique_launch_manifest_path(
            root / "slurm" / args.experiment_id,
            stamp,
            job_id,
        )
        manifest_path.parent.mkdir(parents=True, exist_ok=True)
        manifest_path.write_text(
            json.dumps(manifest, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        complete_async_launch(
            async_intent,
            returncode=result.returncode,
            job_id=job_id,
            manifest_path=manifest_path.relative_to(root),
        )
    finally:
        if async_lock is not None:
            async_lock.close()
    if result.returncode != 0:
        raise LedgerError(
            f"launcher exited {result.returncode}; manifest: {manifest_path.relative_to(root)}"
        )
    if job_id is not None:
        item["lifecycle"] = "queued"
        item["latest_launch_manifest"] = str(manifest_path.relative_to(root))
        item["latest_job_id"] = job_id
        data["updated_at"] = utc_now()
        write_registry(registry_path, data)
        sync_views(root, data)
    print(f"launch manifest: {manifest_path.relative_to(root)}")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)

    import_parser = subparsers.add_parser(
        "import-index", help="create registry.json from the existing hand-written INDEX.md"
    )
    import_parser.add_argument("--force", action="store_true")
    import_parser.set_defaults(handler=command_import)

    sync_parser = subparsers.add_parser("sync", help="regenerate Markdown views")
    sync_parser.set_defaults(handler=command_sync)

    lint_parser = subparsers.add_parser("lint", help="validate registry and generated views")
    lint_parser.set_defaults(handler=command_lint)

    status_parser = subparsers.add_parser(
        "status", help="show active experiments or one compact experiment status"
    )
    status_parser.add_argument("experiment_id", nargs="?")
    status_parser.add_argument("--all", action="store_true")
    status_parser.add_argument("--slurm-snapshot")
    status_parser.add_argument("--no-slurm", action="store_true")
    status_parser.add_argument("--since", default="now-2days")
    status_parser.add_argument("--pretty", action="store_true")
    status_parser.set_defaults(handler=command_status)

    focus_parser = subparsers.add_parser(
        "focus", help="set the one experiment and milestone restored after compaction"
    )
    focus_parser.add_argument("experiment_id")
    focus_parser.add_argument("--milestone", required=True)
    focus_parser.set_defaults(handler=command_focus)

    outline_parser = subparsers.add_parser(
        "outline", help="list an experiment spec's headings and exact line ranges"
    )
    outline_parser.add_argument("experiment_id", nargs="?")
    outline_parser.set_defaults(handler=command_outline)

    anchor_refresh_parser = subparsers.add_parser(
        "anchor-refresh",
        help="re-hash a meaning-preserving Intent Anchor wording correction",
    )
    anchor_refresh_parser.add_argument("experiment_id")
    anchor_refresh_parser.add_argument("--reason", required=True)
    anchor_refresh_parser.set_defaults(handler=command_anchor_refresh)

    contract_lint_parser = subparsers.add_parser(
        "contract-lint", help="validate a guarded experiment implementation contract"
    )
    contract_lint_parser.add_argument("experiment_id")
    contract_lint_parser.set_defaults(handler=command_contract_lint)

    review_context_parser = subparsers.add_parser(
        "review-context", help="emit the frozen contract and current source digest"
    )
    review_context_parser.add_argument("experiment_id")
    review_context_parser.add_argument(
        "--mode", choices=("full", "delta"), default="full"
    )
    review_context_parser.add_argument("--scope")
    review_context_parser.set_defaults(handler=command_review_context)

    record_review_parser = subparsers.add_parser(
        "record-review", help="record an independent pre-training review decision"
    )
    record_review_parser.add_argument("experiment_id")
    record_review_parser.add_argument(
        "--status", required=True, choices=("pass", "fail", "blocked")
    )
    record_review_parser.add_argument(
        "--mode", choices=("full", "delta"), default="full"
    )
    record_review_parser.add_argument("--scope")
    record_review_parser.add_argument("--reviewer", required=True)
    record_review_parser.add_argument("--summary", required=True)
    record_review_parser.add_argument(
        "--findings-file",
        help="JSON findings with proof or reviewer closure mode",
    )
    record_review_parser.add_argument(
        "--resource-review-file",
        help=(
            "optional JSON resource/efficiency estimate table; use it to "
            "record requested-vs-needed headroom and uncertainty"
        ),
    )
    record_review_parser.set_defaults(handler=command_record_review)

    close_findings_parser = subparsers.add_parser(
        "close-review-findings",
        help="close proof-type blockers after a same-contract repair",
    )
    close_findings_parser.add_argument("experiment_id")
    close_findings_parser.add_argument("--scope")
    close_findings_parser.add_argument("--evidence-file", required=True)
    close_findings_parser.add_argument("--actor", required=True)
    close_findings_parser.set_defaults(handler=command_close_review_findings)

    operational_parser = subparsers.add_parser(
        "record-operational",
        help="validate scoped operational launch files without refreshing a scientific review",
    )
    operational_parser.add_argument("experiment_id")
    operational_parser.add_argument("--scope", required=True)
    operational_parser.add_argument("--actor", required=True)
    operational_parser.add_argument("--summary", required=True)
    operational_parser.set_defaults(handler=command_record_operational)

    preflight_parser = subparsers.add_parser(
        "preflight",
        help="run the mandatory real-path checks for one exact training launch",
    )
    preflight_parser.add_argument("experiment_id")
    preflight_parser.add_argument("--scope")
    preflight_parser.add_argument("--force", action="store_true")
    preflight_parser.add_argument("launch_command", nargs=argparse.REMAINDER)
    preflight_parser.set_defaults(handler=command_preflight)

    packet_parser = subparsers.add_parser(
        "launch-packet",
        help="compile stage closure and exact launch readiness without submitting",
    )
    packet_parser.add_argument("experiment_id")
    packet_parser.add_argument("--scope")
    packet_parser.add_argument("--slurm-snapshot")
    packet_parser.add_argument("--output")
    packet_parser.add_argument("launch_command", nargs=argparse.REMAINDER)
    packet_parser.set_defaults(handler=command_launch_packet)

    launch_parser = subparsers.add_parser(
        "launch",
        help="launch after current review and mandatory training preflight",
    )
    launch_parser.add_argument("experiment_id")
    launch_parser.add_argument("--scope")
    launch_parser.add_argument("--dry-run", action="store_true")
    launch_parser.add_argument("launch_command", nargs=argparse.REMAINDER)
    launch_parser.set_defaults(handler=command_launch)

    add_parser = subparsers.add_parser(
        "add", help="register a newly created full experiment spec"
    )
    add_parser.add_argument("experiment_id")
    add_parser.add_argument("--spec")
    add_parser.add_argument("--lifecycle", choices=LIFECYCLES, default="draft")
    add_parser.add_argument("--legacy-status")
    add_parser.add_argument("--branch-worktree")
    add_parser.add_argument("--contract-path")
    add_parser.add_argument("--core-change")
    add_parser.add_argument("--current-conclusion")
    add_parser.add_argument("--latest-artifact")
    add_parser.add_argument("--next-action")
    add_parser.set_defaults(handler=command_add)

    update_parser = subparsers.add_parser("update", help="update one registry entry")
    update_parser.add_argument("experiment_id")
    update_parser.add_argument("--lifecycle", choices=LIFECYCLES)
    update_parser.add_argument("--outcome", choices=(*OUTCOMES, "none"))
    update_parser.add_argument("--legacy-status")
    update_parser.add_argument("--branch-worktree")
    update_parser.add_argument("--core-change")
    update_parser.add_argument("--current-conclusion")
    update_parser.add_argument("--latest-artifact")
    update_parser.add_argument("--next-action")
    update_parser.add_argument(
        "--contract-path",
        help="Repository-relative guarded contract path.",
    )
    update_parser.add_argument(
        "--provenance-state",
        choices=("degraded", "reconciled"),
        help="Record only the final degraded or reconciled provenance state.",
    )
    update_parser.set_defaults(handler=lambda root, args: mutate_experiment(root, args))

    close_parser = subparsers.add_parser("close", help="close one experiment")
    close_parser.add_argument("experiment_id")
    close_parser.add_argument("--outcome", required=True, choices=OUTCOMES)
    close_parser.add_argument("--legacy-status")
    close_parser.add_argument("--current-conclusion")
    close_parser.add_argument("--latest-artifact")
    close_parser.add_argument("--next-action")
    close_parser.set_defaults(
        handler=lambda root, args: mutate_experiment(root, args, close=True)
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        root = project_root()
        args.handler(root, args)
    except LedgerError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
