# Completed-Task Report

Produce a complete but concise report. Never return only scheduler status, a
checkpoint path, or raw metrics.

## Status And Identity

Name the frozen task/route and exact run. Distinguish scheduler, training,
evaluation, and task completion; state whether a verdict is authorized.

## Execution And Evidence

Give job IDs, command, logs, checkpoint/resume provenance, runtime, throughput,
utilization/memory when available, and metric/render paths. Confirm evaluated
checkpoint, cache, split, evaluator, and render inputs match the contract.

## Results And Baselines

Tabulate every declared metric against the strongest relevant baseline, with
directions and material deltas. State which gates passed. Mark missing or
partial evidence explicitly; sample renders never replace full metrics.

## Qualitative And Diagnostic Analysis

Compare required renders with the same baselines. Explain visible strengths,
regressions, failure modes, quantitative/qualitative contradictions, anomalies,
efficiency changes, tradeoffs, and coverage or statistical limits.

## Conclusion Boundaries

State what the evidence supports and does not support. Keep scientific
acceptance with the user unless explicitly delegated.

## Next Action

Give the exact next action or decision options without choosing for the user.
