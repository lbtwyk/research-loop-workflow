#!/usr/bin/env python3
"""Capture one read-only Slurm state snapshot for launch strategy decisions."""

from __future__ import annotations

import argparse
import getpass
import json
import os
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Callable, Sequence

Runner = Callable[[Sequence[str]], subprocess.CompletedProcess[str]]
FIELD_RE = re.compile(r"(?:^|\s)([A-Za-z][A-Za-z0-9_/]*)=")


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_command(command: Sequence[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        list(command), check=False, capture_output=True, text=True, timeout=30
    )


def parse_key_value_records(text: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for line in text.splitlines():
        matches = list(FIELD_RE.finditer(line))
        if not matches:
            continue
        record: dict[str, str] = {}
        for index, match in enumerate(matches):
            end = matches[index + 1].start() if index + 1 < len(matches) else len(line)
            record[match.group(1)] = line[match.end() : end].strip()
        records.append(record)
    return records


def parse_pipe_records(text: str, fields: Sequence[str]) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for line in text.splitlines():
        if not line.strip():
            continue
        values = line.rstrip("\n").split("|")
        if values and values[-1] == "":
            values.pop()
        values.extend([""] * (len(fields) - len(values)))
        records.append(dict(zip(fields, values[: len(fields)])))
    return records


def parse_config(text: str) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in text.splitlines():
        if "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def integer(value: str | None) -> int | None:
    if value is None:
        return None
    match = re.match(r"^\d+", value)
    return int(match.group()) if match else None


def gpu_count(tres: str | None) -> int | None:
    if not tres:
        return None
    matches = re.findall(r"(?:^|,)(?:gres/)?gpu(?:[:/][^=,]+)?=(\d+)", tres)
    return sum(int(value) for value in matches) if matches else None


def source_result(
    runner: Runner, command: Sequence[str]
) -> tuple[subprocess.CompletedProcess[str] | None, dict[str, object]]:
    try:
        result = runner(command)
    except (OSError, subprocess.TimeoutExpired) as error:
        return None, {
            "status": "unavailable",
            "command": list(command),
            "error": str(error),
        }
    source: dict[str, object] = {
        "status": "ok" if result.returncode == 0 else "unavailable",
        "command": list(command),
        "returncode": result.returncode,
    }
    if result.returncode != 0:
        source["error"] = result.stderr.strip() or result.stdout.strip()
    return result, source


def collect_snapshot(
    *, user: str, since: str = "now-2days", runner: Runner = run_command
) -> dict[str, object]:
    sources: dict[str, object] = {}

    queue_command = [
        "squeue",
        "-h",
        "-u",
        user,
        "-o",
        "%i|%P|%j|%T|%M|%l|%D|%R|%q|%b|%C|%m",
    ]
    queue_result, sources["queue"] = source_result(runner, queue_command)
    queue_fields = (
        "job_id",
        "partition",
        "name",
        "state",
        "elapsed",
        "time_limit",
        "nodes",
        "reason_or_nodes",
        "qos",
        "tres_per_node",
        "cpus",
        "memory",
    )
    jobs = parse_pipe_records(queue_result.stdout, queue_fields) if queue_result else []

    details: dict[str, dict[str, str]] = {}
    for job in jobs:
        job_id = job["job_id"]
        result, source = source_result(
            runner, ["scontrol", "show", "job", "-o", job_id]
        )
        sources[f"job:{job_id}"] = source
        if result:
            records = parse_key_value_records(result.stdout)
            if records:
                details[job_id] = records[0]
    for job in jobs:
        detail = details.get(job["job_id"], {})
        job.update(
            {
                "reservation": detail.get("Reservation", ""),
                "qos": detail.get("QOS", job["qos"]),
                "reason": detail.get("Reason", job["reason_or_nodes"]),
                "alloc_tres": detail.get("AllocTRES", ""),
                "req_tres": detail.get("ReqTRES", ""),
                "num_cpus": integer(detail.get("NumCPUs")),
                "num_nodes": integer(detail.get("NumNodes")),
                "batch_flag": integer(detail.get("BatchFlag")),
                "work_dir": detail.get("WorkDir", ""),
                "stdout": detail.get("StdOut", ""),
                "stderr": detail.get("StdErr", ""),
                "allocated_gpus": gpu_count(detail.get("AllocTRES")),
                "requested_gpus": gpu_count(detail.get("ReqTRES")),
            }
        )

    steps_by_job: dict[str, list[dict[str, object]]] = {}
    for job in jobs:
        if job["state"] != "RUNNING":
            continue
        job_id = job["job_id"]
        result, source = source_result(
            runner, ["scontrol", "show", "step", "-o", job_id]
        )
        sources[f"steps:{job_id}"] = source
        records = parse_key_value_records(result.stdout) if result else []
        steps_by_job[job_id] = [
            {
                "step_id": record.get("StepId", ""),
                "name": record.get("Name", ""),
                "state": record.get("State", ""),
                "nodes": integer(record.get("Nodes")),
                "cpus": integer(record.get("CPUs")),
                "tasks": integer(record.get("Tasks")),
                "tres": record.get("TRES", ""),
                "gpus": gpu_count(record.get("TRES")) or 0,
            }
            for record in records
        ]

    sinfo_result, sources["partitions"] = source_result(
        runner, ["sinfo", "-h", "-o", "%P|%a|%l|%D|%t|%G"]
    )
    partitions = (
        parse_pipe_records(
            sinfo_result.stdout,
            ("partition", "availability", "time_limit", "nodes", "state", "gres"),
        )
        if sinfo_result
        else []
    )

    reservation_result, sources["reservations"] = source_result(
        runner, ["scontrol", "show", "reservation", "-o"]
    )
    reservations = (
        parse_key_value_records(reservation_result.stdout) if reservation_result else []
    )

    qos_fields = (
        "name",
        "max_jobs_per_user",
        "max_submit_jobs_per_user",
        "max_tres_per_user",
        "max_tres_per_job",
        "max_wall",
        "flags",
    )
    qos_command = [
        "sacctmgr",
        "-nP",
        "show",
        "qos",
        "format=Name,MaxJobsPU,MaxSubmitJobsPU,MaxTRESPU,MaxTRESPerJob,MaxWall,Flags",
    ]
    qos_result, sources["qos"] = source_result(runner, qos_command)
    qos = parse_pipe_records(qos_result.stdout, qos_fields) if qos_result else []

    config_result, sources["config"] = source_result(
        runner, ["scontrol", "show", "config"]
    )
    config = parse_config(config_result.stdout) if config_result else {}
    scheduler_config = {
        key: value
        for key, value in config.items()
        if key
        in {"SchedulerParameters", "SchedulerType", "PreemptMode", "PriorityType"}
    }

    recent_fields = (
        "job_id",
        "name",
        "partition",
        "qos",
        "state",
        "elapsed",
        "time_limit",
        "alloc_tres",
        "max_rss",
        "exit_code",
    )
    recent_command = [
        "sacct",
        "-X",
        "-S",
        since,
        "-u",
        user,
        "-nP",
        "-o",
        "JobIDRaw,JobName,Partition,QOS,State,Elapsed,Timelimit,AllocTRES,MaxRSS,ExitCode",
    ]
    recent_result, sources["recent_jobs"] = source_result(runner, recent_command)
    recent_jobs = (
        parse_pipe_records(recent_result.stdout, recent_fields) if recent_result else []
    )

    pending_reasons = Counter(
        job["reason"] for job in jobs if job["state"] == "PENDING" and job["reason"]
    )
    allocations: list[dict[str, object]] = []
    dispatch_root = Path(
        os.environ.get("RESEARCH_LOOP_INTERACTIVE_DISPATCH_ROOT")
        or os.environ.get("M2D_INTERACTIVE_DISPATCH_ROOT")
        or str(Path.home() / ".cache/research-loop/interactive")
    )
    for job in jobs:
        if job["state"] != "RUNNING":
            continue
        ready_path = dispatch_root / job["job_id"] / "ready.json"
        dispatcher_ready = False
        if ready_path.is_file():
            try:
                ready = json.loads(ready_path.read_text(encoding="utf-8"))
                dispatcher_ready = str(ready.get("job_id")) == job["job_id"]
            except (OSError, json.JSONDecodeError):
                dispatcher_ready = False
        steps = steps_by_job.get(job["job_id"], [])
        committed_gpus = sum(int(step["gpus"]) for step in steps)
        allocated_gpus = job["allocated_gpus"]
        allocations.append(
            {
                "job_id": job["job_id"],
                "name": job["name"],
                "partition": job["partition"],
                "reservation": job["reservation"],
                "qos": job["qos"],
                "time_limit": job["time_limit"],
                "elapsed": job["elapsed"],
                "alloc_tres": job["alloc_tres"],
                "allocated_gpus": allocated_gpus,
                "batch_flag": job["batch_flag"],
                "active_steps": steps,
                "committed_step_gpus": committed_gpus,
                "dispatcher_ready": dispatcher_ready,
                "reusable_gpus": (
                    max(0, int(allocated_gpus) - committed_gpus)
                    if dispatcher_ready and allocated_gpus is not None
                    else None
                ),
            }
        )
    return {
        "schema_version": 1,
        "captured_at": utc_now(),
        "user": user,
        "sources": sources,
        "jobs": jobs,
        "partitions": partitions,
        "reservations": reservations,
        "qos": qos,
        "recent_jobs": recent_jobs,
        "strategy_input": {
            "pending_reason_counts": dict(sorted(pending_reasons.items())),
            "running_allocations": allocations,
            "scheduler_config": scheduler_config,
        },
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--user", default=getpass.getuser())
    parser.add_argument("--since", default="now-2days")
    parser.add_argument("--output", type=Path)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    snapshot = collect_snapshot(user=args.user, since=args.since)
    text = json.dumps(snapshot, indent=2, ensure_ascii=False) + "\n"
    if args.output is None:
        print(text, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        temporary = args.output.with_suffix(args.output.suffix + ".tmp")
        temporary.write_text(text, encoding="utf-8")
        temporary.replace(args.output)
        print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
