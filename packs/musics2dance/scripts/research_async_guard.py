#!/usr/bin/env python3
"""Protect pre-existing Slurm jobs during unattended GitHub research."""

from __future__ import annotations

import json
import os
import re
import shlex
import sys
from pathlib import Path
from typing import Any


MINIMUM_NICE = 10000
MUTATING_SCONTROL = {
    "cancel",
    "hold",
    "release",
    "requeue",
    "resume",
    "suspend",
    "update",
}


def shell_words(command: str) -> list[list[str]]:
    commands: list[list[str]] = []
    for line in command.splitlines():
        for segment in re.split(r"(?:&&|\|\||;)", line):
            try:
                words = shlex.split(segment, comments=True, posix=True)
            except ValueError:
                continue
            if words:
                commands.append(words)
    return commands


def executable(words: list[str]) -> tuple[str, list[str]]:
    index = 0
    while index < len(words) and re.fullmatch(
        r"[A-Za-z_][A-Za-z0-9_]*=.*", words[index]
    ):
        index += 1
    if index >= len(words):
        return "", []
    return Path(words[index]).name, words[index + 1 :]


def unsafe_reason(words: list[str]) -> str | None:
    name, tail = executable(words)
    if name == "env":
        index = 0
        while index < len(tail) and (
            tail[index].startswith("-")
            or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tail[index])
        ):
            token = tail[index]
            if token.startswith("SBATCH_NICE="):
                try:
                    if int(token.split("=", 1)[1]) < MINIMUM_NICE:
                        return (
                            "unattended commands cannot lower SBATCH_NICE "
                            f"below {MINIMUM_NICE}"
                        )
                except ValueError:
                    return "invalid SBATCH_NICE override"
            index += 1
        return unsafe_reason(tail[index:]) if index < len(tail) else None
    if name in {"bash", "sh"} and len(tail) >= 2 and tail[0] in {"-c", "-lc"}:
        for nested in shell_words(tail[1]):
            reason = unsafe_reason(nested)
            if reason:
                return reason
        return None
    if name == "scancel":
        return "unattended research cannot cancel any Slurm job"
    if name == "scontrol":
        verb = tail[0].lower() if tail else ""
        if verb in MUTATING_SCONTROL:
            return (
                "unattended research cannot mutate, requeue, hold, release, "
                "or cancel existing Slurm jobs"
            )
    if name == "srun" and any(
        token == "--jobid" or token.startswith("--jobid=")
        for token in tail
    ):
        return (
            "unattended research cannot attach a new step to an existing "
            "Slurm allocation"
        )
    if name != "sbatch":
        return None
    return (
        "the asynchronous worker cannot submit Slurm jobs directly; write a "
        "validated launch request for the deterministic controller"
    )


def deny(reason: str) -> None:
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
    if os.environ.get(
        "RESEARCH_LOOP_RESEARCH_ASYNC",
        os.environ.get("M2D_RESEARCH_ASYNC"),
    ) != "1":
        return 0
    try:
        payload: dict[str, Any] = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0
    if payload.get("hook_event_name") != "PreToolUse":
        return 0
    tool_input = payload.get("tool_input")
    if not isinstance(tool_input, dict):
        return 0
    command = tool_input.get("command", tool_input.get("cmd", ""))
    if not isinstance(command, str):
        return 0
    for words in shell_words(command):
        reason = unsafe_reason(words)
        if reason:
            deny(reason)
            break
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
