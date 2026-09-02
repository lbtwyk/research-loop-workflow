#!/usr/bin/env python3
"""Run the bounded, real-path checks required before a training submission."""

from __future__ import annotations

import os
import shlex
import subprocess
import time
from pathlib import Path
from typing import Mapping, Sequence


def required_reservation() -> str:
    return os.environ.get("RESEARCH_LOOP_SLURM_RESERVATION", "interactive")

REQUIRED_CPU_CAPABILITIES = frozenset(
    {
        "entrypoint",
        "real_data",
        "loader_single_process",
        "loader_formal_workers",
        "loader_soak",
        "train_step",
        "checkpoint_resume",
        "downstream_hook",
    }
)
GPU_MODES = frozenset({"local", "slurm_interactive"})
DEFAULT_CPU_TIMEOUT_SECONDS = 1800
DEFAULT_GPU_TIMEOUT_SECONDS = 600
MIN_SLURM_IMMEDIATE_SECONDS = 5
GPU_UNAVAILABLE_MARKERS = (
    "can't run immediately",
    "cannot run immediately",
    "unable to allocate resources",
    "requested node configuration is not available",
    "required node not available",
    "nodes required for job are down, drained or reserved",
)


class PreflightError(RuntimeError):
    pass


def _command(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise PreflightError(f"{label} must be a non-empty command string")
    return value.strip()


def _timeout(value: object, label: str, default: int) -> int:
    if value is None:
        return default
    if not isinstance(value, int) or isinstance(value, bool) or value <= 0:
        raise PreflightError(f"{label} must be a positive integer")
    return value


def _option_value(tokens: list[str], *names: str) -> str | None:
    for index, token in enumerate(tokens):
        for name in names:
            if token.startswith(f"{name}="):
                return token.partition("=")[2]
            if token == name and index + 1 < len(tokens):
                value = tokens[index + 1]
                return None if value.startswith("-") else value
    return None


def _has_option(tokens: list[str], *names: str) -> bool:
    return any(
        token == name or token.startswith(f"{name}=")
        for token in tokens
        for name in names
    )


def _validate_interactive_srun(command: str, *, label: str) -> None:
    try:
        tokens = shlex.split(command)
    except ValueError as error:
        raise PreflightError(f"gpu_check command cannot be parsed: {error}") from error
    has_srun = "srun" in (Path(token).name for token in tokens)
    reservation = _option_value(tokens, "--reservation")
    job_id = _option_value(tokens, "--jobid")
    has_one_task = any(
        token == "--ntasks=1"
        or (
            token in {"--ntasks", "-n"}
            and index + 1 < len(tokens)
            and tokens[index + 1] == "1"
        )
        for index, token in enumerate(tokens)
    )
    if not has_srun:
        raise PreflightError(f"{label} must use srun; login-node execution is forbidden")
    if not has_one_task:
        raise PreflightError(
            f"{label} must use --ntasks=1 so the check runs once"
        )

    if job_id is not None:
        if reservation is not None:
            raise PreflightError(
                f"{label} must choose one transport: --jobid reuse or a new "
                f"--reservation={required_reservation()} allocation"
            )
        if not _has_option(tokens, "--exact") or not _has_option(
            tokens, "--exclusive"
        ):
            raise PreflightError(
                f"{label} reusing an allocation must use --jobid together "
                "with --exact and --exclusive"
            )
        return

    if reservation != required_reservation():
        raise PreflightError(
            f"{label} must use either srun --jobid=JOB_ID or "
            f"srun --reservation={required_reservation()}"
        )

    immediate_value = _option_value(tokens, "--immediate")
    if immediate_value is None:
        raise PreflightError(
            f"{label} must set an explicit --immediate "
            f"timeout of at least {MIN_SLURM_IMMEDIATE_SECONDS} seconds"
        )
    try:
        immediate_seconds = int(immediate_value)
    except ValueError as error:
        raise PreflightError(
            f"{label} --immediate timeout must be an integer"
        ) from error
    if immediate_seconds < MIN_SLURM_IMMEDIATE_SECONDS:
        raise PreflightError(
            f"{label} --immediate timeout must be at least "
            f"{MIN_SLURM_IMMEDIATE_SECONDS} seconds to span a scheduler cycle"
        )


def validate_definition(value: object) -> dict[str, object]:
    """Validate and normalize one contract-declared training preflight."""
    if not isinstance(value, dict):
        raise PreflightError("training_preflight must be an object")
    raw_checks = value.get("cpu_checks")
    if not isinstance(raw_checks, list) or not raw_checks:
        raise PreflightError("training_preflight cpu_checks must be a non-empty list")

    checks: list[dict[str, object]] = []
    covered: set[str] = set()
    names: set[str] = set()
    for index, raw in enumerate(raw_checks):
        label = f"training_preflight cpu_checks[{index}]"
        if not isinstance(raw, dict):
            raise PreflightError(f"{label} must be an object")
        name = raw.get("name")
        if not isinstance(name, str) or not name.strip():
            raise PreflightError(f"{label} name must be a non-empty string")
        name = name.strip()
        if name in names:
            raise PreflightError(f"duplicate training preflight check name: {name}")
        names.add(name)
        command = _command(raw.get("command"), f"{label} command")
        timeout_seconds = _timeout(
            raw.get("timeout_seconds"),
            f"{label} timeout_seconds",
            DEFAULT_CPU_TIMEOUT_SECONDS,
        )
        capabilities = raw.get("covers")
        if (
            not isinstance(capabilities, list)
            or not capabilities
            or not all(
                isinstance(capability, str) and capability
                for capability in capabilities
            )
        ):
            raise PreflightError(f"{label} covers must be a non-empty string list")
        unknown = set(capabilities) - REQUIRED_CPU_CAPABILITIES
        if unknown:
            raise PreflightError(
                f"{label} has unknown capabilities: {', '.join(sorted(unknown))}"
            )
        covered.update(capabilities)
        checks.append(
            {
                "name": name,
                "command": command,
                "covers": sorted(set(capabilities)),
                "timeout_seconds": timeout_seconds,
            }
        )

    missing = REQUIRED_CPU_CAPABILITIES - covered
    if missing:
        raise PreflightError(
            "training_preflight cpu_checks do not cover: " + ", ".join(sorted(missing))
        )

    raw_gpu = value.get("gpu_check")
    if not isinstance(raw_gpu, dict):
        raise PreflightError("training_preflight gpu_check must be an object")
    mode = raw_gpu.get("mode")
    if mode not in GPU_MODES:
        raise PreflightError(
            "training_preflight gpu_check mode must be local or slurm_interactive"
        )
    gpu_command = _command(
        raw_gpu.get("command"), "training_preflight gpu_check command"
    )
    gpu_timeout_seconds = _timeout(
        raw_gpu.get("timeout_seconds"),
        "training_preflight gpu_check timeout_seconds",
        DEFAULT_GPU_TIMEOUT_SECONDS,
    )
    if mode == "slurm_interactive":
        for check in checks:
            _validate_interactive_srun(
                str(check["command"]), label=f"cpu_check {check['name']}"
            )
        _validate_interactive_srun(gpu_command, label="slurm_interactive gpu_check")

    return {
        "cpu_checks": checks,
        "gpu_check": {
            "mode": mode,
            "command": gpu_command,
            "timeout_seconds": gpu_timeout_seconds,
        },
    }


def gpu_allocation_unavailable(stdout: str, stderr: str) -> bool:
    text = f"{stdout}\n{stderr}".lower()
    return any(marker in text for marker in GPU_UNAVAILABLE_MARKERS)


def _run_command(
    command: str,
    *,
    root: Path,
    env: Mapping[str, str] | None,
    timeout_seconds: int,
) -> dict[str, object]:
    started = time.monotonic()
    try:
        result = subprocess.run(
            command,
            cwd=root,
            env=None if env is None else dict(env),
            shell=True,
            executable="/bin/bash",
            check=False,
            capture_output=True,
            text=True,
            timeout=timeout_seconds,
        )
        returncode = result.returncode
        stdout = result.stdout
        stderr = result.stderr
    except subprocess.TimeoutExpired as error:
        returncode = 124
        stdout = error.stdout or ""
        stderr = (error.stderr or "") + (
            f"\npreflight command timed out after {timeout_seconds}s"
        )
    return {
        "command": command,
        "returncode": returncode,
        "timeout_seconds": timeout_seconds,
        "duration_seconds": round(time.monotonic() - started, 3),
        "stdout": stdout[-8000:],
        "stderr": stderr[-8000:],
    }


def run_preflight(
    definition: object,
    *,
    root: Path,
    env: Mapping[str, str] | None = None,
) -> dict[str, object]:
    """Run CPU checks, then a non-queueing GPU canary, and return evidence."""
    normalized = validate_definition(definition)
    cpu_results: list[dict[str, object]] = []
    for check in normalized["cpu_checks"]:
        result = _run_command(
            str(check["command"]),
            root=root,
            env=env,
            timeout_seconds=int(check["timeout_seconds"]),
        )
        result.update({"name": check["name"], "covers": check["covers"]})
        cpu_results.append(result)
        if result["returncode"] != 0:
            return {
                "status": "failed",
                "cpu_checks": cpu_results,
                "gpu_check": {"status": "not_run_cpu_failed"},
            }

    gpu = normalized["gpu_check"]
    gpu_result = _run_command(
        str(gpu["command"]),
        root=root,
        env=env,
        timeout_seconds=int(gpu["timeout_seconds"]),
    )
    gpu_result["mode"] = gpu["mode"]
    if gpu_result["returncode"] == 0:
        gpu_result["status"] = "passed"
    elif gpu["mode"] == "slurm_interactive" and gpu_allocation_unavailable(
        str(gpu_result["stdout"]), str(gpu_result["stderr"])
    ):
        gpu_result["status"] = "skipped_unavailable"
    else:
        gpu_result["status"] = "failed"

    return {
        "status": (
            "passed"
            if gpu_result["status"] in {"passed", "skipped_unavailable"}
            else "failed"
        ),
        "cpu_checks": cpu_results,
        "gpu_check": gpu_result,
    }
