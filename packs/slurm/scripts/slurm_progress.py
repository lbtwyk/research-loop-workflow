#!/usr/bin/env python3
"""Read-only Slurm job and log-reported training progress (no GPU required)."""

from __future__ import annotations

import argparse
import getpass
import json
import math
import re
import shlex
import time
from pathlib import Path

from slurm_state_snapshot import (
    Runner, parse_key_value_records, parse_pipe_records, run_command,
    source_result, utc_now,
)

QUEUE_FIELDS = ("job_id", "name", "state", "elapsed", "time_limit", "reason_or_nodes")
HISTORY_FIELDS = (
    "job_id", "raw_job_id", "name", "state", "elapsed", "time_limit", "exit_code",
    "work_dir", "stdout", "stderr",
)
EMPTY_PATHS = {"", "Unknown", "None", "(null)", "N/A"}


def resolve_log(value: str, job_id: str, work_dir: str, raw_job_id: str = "") -> str | None:
    if value in EMPTY_PATHS:
        return None
    array, _, task = job_id.partition("_")
    if "%j" in value and task and not raw_job_id:
        return None
    value = value.replace("%j", raw_job_id or job_id).replace("%A", array)
    if task:
        value = value.replace("%a", task)
    # Other Slurm substitutions need scheduler metadata; do not guess a path.
    if "%" in value:
        return None
    path = Path(value)
    if not path.is_absolute():
        if work_dir in EMPTY_PATHS or not Path(work_dir).is_absolute():
            return None
        path = Path(work_dir) / path
    return str(path)


def read_log(path: str | None, lines: int) -> dict:
    if path is None:
        return {"status": "unknown", "path": None, "progress": None}
    try:
        with Path(path).open("rb") as stream:
            stat = stream.seek(0, 2)
            offset = max(0, stat - 131072)
            stream.seek(offset)
            data = stream.read(131072)
        if offset:
            data = data.partition(b"\n")[2]
        # A writer may be in the middle of a JSON record.
        data = data[:data.rfind(b"\n") + 1]
        tail = data.decode("utf-8", errors="replace").splitlines()[-lines:]
        age = max(0, time.time() - Path(path).stat().st_mtime)
    except OSError as error:
        return {"status": "unavailable", "path": path, "error": str(error), "progress": None}
    progress = None
    for line in reversed(tail):
        try:
            record = json.loads(line)
        except json.JSONDecodeError:
            continue
        if not isinstance(record, dict):
            continue
        step, total = record.get("step"), record.get("total", record.get("total_steps"))
        if (type(step) is not int or type(total) is not int
                or not 0 <= step <= total or total <= 0):
            continue
        eta = record.get("training_eta_hours")
        if type(eta) not in (int, float) or not math.isfinite(eta) or eta < 0:
            eta = None
        progress = {
            "step": step, "total": total, "percent": round(100 * step / total, 2),
            "stage": record.get("stage"), "training_eta_hours": eta,
            "evidence": line,
        }
        break
    return {
        "status": "ok", "path": path, "log_age_seconds": round(age, 1),
        "progress": progress, "tail": tail,
    }


def collect_progress(
    *, user: str, job_ids: list[str] | None = None, history: bool = False,
    since: str = "now-2days", tail_lines: int = 80, runner: Runner = run_command,
) -> dict:
    sources = {}
    requested = job_ids or []

    def selected(identifier):
        return not requested or any(
            identifier == wanted or identifier.startswith(wanted + "_")
            for wanted in requested
        )

    result, sources["queue"] = source_result(runner, [
        "squeue", "--all", "--array", "-h", "-u", user, "-o",
        "%i|%j|%T|%M|%l|%R",
    ])
    jobs = {
        job["job_id"]: dict(job, state_source="squeue")
        for job in parse_pipe_records(result.stdout, QUEUE_FIELDS) if selected(job["job_id"])
    } if result else {}
    missing = [identifier for identifier in requested if not any(
        job_id == identifier or job_id.startswith(identifier + "_") for job_id in jobs
    )]
    if history or missing or result is None:
        command = [
            "sacct", "-X", "-nP", "-u", user, "-S", since, "-o",
            "JobID%64,JobIDRaw%64,JobName%200,State%64,Elapsed,Timelimit,ExitCode,WorkDir%2048,StdOut%2048,StdErr%2048",
        ]
        if requested:
            command += ["-j", ",".join(requested)]
        accounting, sources["accounting"] = source_result(runner, command)
        if accounting:
            for job in parse_pipe_records(accounting.stdout, HISTORY_FIELDS):
                if selected(job["job_id"]) and job["job_id"] not in jobs:
                    jobs[job["job_id"]] = dict(job, state_source="sacct")
    for job in jobs.values():
        identifier = job["job_id"]
        if job["state_source"] == "squeue":
            result, sources[f"job:{identifier}"] = source_result(
                runner, ["scontrol", "show", "job", "-o", identifier]
            )
            records = parse_key_value_records(result.stdout) if result else []
            detail = records[0] if records else {}
            job["raw_job_id"] = detail.get("JobId", "")
            for field, key in (("stdout", "StdOut"), ("stderr", "StdErr"), ("work_dir", "WorkDir"),
                               ("exit_code", "ExitCode"), ("reason", "Reason")):
                job[field] = detail.get(key, "")
            job["reason"] = job["reason"] or job["reason_or_nodes"]
        job["logs"] = {}
        for kind in ("stdout", "stderr"):
            path = resolve_log(job.get(kind, ""), identifier, job.get("work_dir", ""), job.get("raw_job_id", ""))
            job[kind] = path
            job["logs"][kind] = (
                {"status": "not_started", "path": path, "progress": None}
                if job["state"] == "PENDING" else read_log(path, tail_lines)
            )
        job["progress"] = next((
            log["progress"] for log in job["logs"].values() if log["progress"] is not None
        ), None)
        job["follow_commands"] = list(dict.fromkeys(
            f"tail -n {tail_lines} -f -- {shlex.quote(path)}"
            for path in (job["stdout"], job["stderr"]) if path
        ))
    unresolved = [identifier for identifier in requested if not any(
        job_id == identifier or job_id.startswith(identifier + "_") for job_id in jobs
    )]
    return {
        "schema_version": 1, "captured_at": utc_now(), "user": user,
        "status": "partial" if unresolved or any(s["status"] != "ok" for s in sources.values()) else "ok",
        "sources": sources, "jobs": list(jobs.values()), "unresolved_job_ids": unresolved,
        "boundary": "Log-reported training budget is not job walltime, downstream-stage closure, or scientific acceptance.",
    }


def format_report(report: dict) -> str:
    lines = [f"Slurm progress | {report['user']} | {report['captured_at']} | {report['status']}"]
    if not report["jobs"]:
        lines.append("No matching jobs observed." if report["status"] == "ok" else "Job state unavailable; see source errors.")
    for job in report["jobs"]:
        lines.append(f"{job['job_id']}  {job['state']}  {job['name']}  elapsed/limit={job['elapsed']}/{job['time_limit']}")
        if job["state"] == "PENDING":
            lines.append(f"  pending reason: {job.get('reason', 'unknown')}")
        elif job["state_source"] == "sacct":
            lines.append(f"  accounting exit code: {job.get('exit_code', 'unknown')}")
        progress = job["progress"]
        if progress:
            lines.append(f"  log-reported training: {progress['step']}/{progress['total']} ({progress['percent']:.2f}%) stage={progress['stage'] or 'unknown'}")
            if job["state"] == "RUNNING" and progress["training_eta_hours"] is not None:
                lines.append(f"  log-reported training ETA: {progress['training_eta_hours']:.2f}h (not job/stage ETA)")
        elif job["state"] != "PENDING":
            lines.append("  training progress: unknown (no supported JSON step/total record)")
        for kind, log in job["logs"].items():
            if log["path"]:
                age = f", log age={log['log_age_seconds']}s" if "log_age_seconds" in log else ""
                lines.append(f"  {kind}: {log['path']} [{log['status']}{age}]")
                if log.get("error"):
                    lines.append(f"    {log['error']}")
                if log.get("tail") and not progress:
                    lines.append(f"    last line: {log['tail'][-1][:240]}")
        lines.extend(f"  follow: {command}" for command in job["follow_commands"])
    for key, source in report["sources"].items():
        if source["status"] != "ok":
            lines.append(f"Source unavailable ({key}): {source.get('error', 'unknown')}")
    if report["unresolved_job_ids"]:
        lines.append("Unresolved job IDs (check --since): " + ", ".join(report["unresolved_job_ids"]))
    lines.append(report["boundary"])
    return "\n".join(lines)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("job_ids", nargs="*", help="job IDs or array parents; default: all live user jobs")
    parser.add_argument("--user", default=getpass.getuser())
    parser.add_argument("--history", action="store_true", help="include accounting jobs since --since")
    parser.add_argument("--since", default="now-2days")
    parser.add_argument("--tail-lines", type=int, default=80)
    parser.add_argument("--json", action="store_true", help="include sources and bounded log tails")
    args = parser.parse_args(argv)
    if args.tail_lines <= 0:
        parser.error("--tail-lines must be positive")
    if any(not re.fullmatch(r"\d+(?:_\d+)?", job) for job in args.job_ids):
        parser.error("job IDs must be numeric allocation IDs or individual array task IDs")
    report = collect_progress(user=args.user, job_ids=args.job_ids, history=args.history,
                              since=args.since, tail_lines=args.tail_lines)
    print(json.dumps(report, indent=2, ensure_ascii=False) if args.json else format_report(report))
    return 0 if report["status"] == "ok" else 1


if __name__ == "__main__":
    raise SystemExit(main())
