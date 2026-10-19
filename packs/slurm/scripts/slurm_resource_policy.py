#!/usr/bin/env python3
"""Choose the lowest-cost comparable resource shape within a near-fastest band.

This is a read-only calculation, not a scheduler or permission to change a job.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

DEFAULT_SLOWDOWN_TOLERANCE = 0.10


def nonnegative_number(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be a finite nonnegative number")
    number = float(value)
    if not math.isfinite(number) or number < 0:
        raise ValueError(f"{label} must be a finite nonnegative number")
    return number


def select_resources(
    payload: dict[str, object], *, slowdown_tolerance: float | None = None
) -> dict[str, object]:
    if not isinstance(payload, dict) or payload.get("schema_version") != 1:
        raise ValueError("resource candidates must be a schema_version 1 object")
    basis = payload.get("comparison_basis")
    if not isinstance(basis, str) or not basis.strip():
        raise ValueError("comparison_basis must identify the same contract and remaining results")
    tolerance = nonnegative_number(
        slowdown_tolerance if slowdown_tolerance is not None else payload.get(
            "slowdown_tolerance", DEFAULT_SLOWDOWN_TOLERANCE
        ),
        "slowdown_tolerance",
    )
    limits = {}
    for key in ("cost_budget_nhr", "deadline_seconds"):
        if payload.get(key) is not None:
            limits[key] = nonnegative_number(payload[key], key)
    candidates = payload.get("candidates")
    if not isinstance(candidates, list) or not candidates:
        raise ValueError("candidates must be a non-empty list")

    ranked = []
    excluded = []
    unranked = []
    identifiers = set()
    for candidate in candidates:
        if not isinstance(candidate, dict):
            raise ValueError("each candidate must be an object")
        identifier = candidate.get("id")
        if not isinstance(identifier, str) or not identifier.strip() or identifier in identifiers:
            raise ValueError("candidate ids must be non-empty and unique")
        identifiers.add(identifier)
        if not isinstance(candidate.get("feasible"), bool):
            raise ValueError(f"{identifier}: feasible must explicitly be true or false")
        if not candidate["feasible"]:
            excluded.append({"id": identifier, "reason": candidate.get("reason") or "infeasible"})
            continue
        values = {}
        missing = []
        for key in ("time_to_result_seconds", "cost_nhr"):
            if candidate.get(key) is None:
                missing.append(key)
            else:
                values[key] = nonnegative_number(candidate[key], f"{identifier}.{key}")
        evidence = candidate.get("evidence")
        if not isinstance(evidence, list) or not evidence or not all(
            isinstance(value, str) and value.strip() for value in evidence
        ):
            missing.append("evidence")
        if (
            "cost_budget_nhr" in limits and "cost_nhr" in values
            and values["cost_nhr"] > limits["cost_budget_nhr"]
        ):
            excluded.append({"id": identifier, "reason": "cost budget exceeded"})
        elif (
            "deadline_seconds" in limits and "time_to_result_seconds" in values
            and values["time_to_result_seconds"] > limits["deadline_seconds"]
        ):
            excluded.append({"id": identifier, "reason": "deadline exceeded"})
        elif missing:
            unranked.append({"id": identifier, "missing": missing})
        else:
            ranked.append({"id": identifier, **values})

    result = {
        "schema_version": 1,
        "advisory": True,
        "comparison_basis": basis,
        "slowdown_tolerance": tolerance,
        **limits,
        "status": "unknown" if unranked else "infeasible",
        "selected_candidate_id": None,
        "fastest_candidate_id": None,
        "time_limit_seconds": None,
        "pareto_candidate_ids": [],
        "excluded": excluded,
        "unranked": unranked,
    }
    if not ranked:
        return result
    frontier = [
        candidate for candidate in ranked
        if not any(
            other["time_to_result_seconds"] <= candidate["time_to_result_seconds"]
            and other["cost_nhr"] <= candidate["cost_nhr"]
            and (
                other["time_to_result_seconds"] < candidate["time_to_result_seconds"]
                or other["cost_nhr"] < candidate["cost_nhr"]
            )
            for other in ranked
        )
    ]
    fastest = min(frontier, key=lambda row: (row["time_to_result_seconds"], row["cost_nhr"], row["id"]))
    time_limit = fastest["time_to_result_seconds"] * (1 + tolerance)
    near_fastest = [row for row in frontier if row["time_to_result_seconds"] <= time_limit]
    selected = min(near_fastest, key=lambda row: (row["cost_nhr"], row["time_to_result_seconds"], row["id"]))
    result.update({
        "status": "selected",
        "selected_candidate_id": selected["id"],
        "fastest_candidate_id": fastest["id"],
        "time_limit_seconds": time_limit,
        "pareto_candidate_ids": sorted(row["id"] for row in frontier),
    })
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("candidates", type=Path)
    parser.add_argument("--slowdown-tolerance", type=float)
    args = parser.parse_args(argv)
    try:
        payload = json.loads(args.candidates.read_text(encoding="utf-8"))
        result = select_resources(payload, slowdown_tolerance=args.slowdown_tolerance)
    except (OSError, ValueError) as error:
        parser.error(str(error))
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
