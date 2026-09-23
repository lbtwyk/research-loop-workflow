# Formal Stage Result Report

Use this report when a declared stage has a result, the full task completes, or
a scientific decision is required. Never return only scheduler status, a
checkpoint path, or raw metrics.

## Status And Identity

Name the frozen route, exact run, completed stage, and remaining stages.
Distinguish runtime, training, evaluation, task completion, and scientific
acceptance.

## Execution And Evidence

Give runtime identities, command, logs, checkpoint/resume provenance, runtime,
throughput, utilization/memory when available, and metric/render paths. Confirm
the evaluated checkpoint, cache, split, evaluator, and render inputs match the
contract.

## Results And Baselines

Tabulate every declared metric against the strongest relevant baseline, with
directions and material deltas. State which gates passed. Mark missing or
partial evidence explicitly; sample renders never replace full metrics.

## Qualitative And Diagnostic Analysis

Compare required renders with the same baselines. Explain visible strengths,
regressions, failure modes, quantitative/qualitative contradictions, anomalies,
efficiency changes, tradeoffs, and coverage or statistical limits.

## Supported Conclusion

State the strongest conclusion supported by the evidence and its limits. Keep
scientific acceptance with the user.

## Continued Action Or Decision

State the operational work already continuing. Ask the user only for the exact
scientific route, contract, claim, or final outcome decision that blocks further
authorized work.
