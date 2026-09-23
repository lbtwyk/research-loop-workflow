---
name: training-check-acceptance
description: "Automatically carry an approved training task through inspection, same-contract repair, remaining stages, evaluation, and formal reporting. Use when the user asks to check training status, failures, resume, missing stages, results, or acceptance."
---

# Training Check Acceptance

A `check` request authorizes the complete operational loop for the approved
route. Continue in the same task until all authorized stages have a formal
result, a scientific decision is required, or a demonstrated external blocker
cannot be repaired from the workspace. Do not return routine status while
authorized operational work remains.

## Workflow

1. Resolve the experiment, run
   `scripts/experiment_ledger.py outline <EXP-ID>`, and read the relevant spec,
   frozen contract, repository guidance, and selected compute module. Build one
   closure table from declared stages, dependencies, launch records, and exact
   evidence paths. Refresh live runtime state when it can change the next
   action.
2. Classify each required stage as `running`, `interrupted`, `stalled`,
   `not_started`, `needs_eval`, or `completed`. A scheduler success or final
   checkpoint proves only its own runtime stage.
3. While work is running, verify real advancement and continue checking at a
   useful cadence. For an interruption or stall, diagnose the demonstrated root
   cause, make the smallest same-contract operational repair, resume, and verify
   new progress. Repeat this loop as needed; a repeated failure calls for deeper
   diagnosis, not a handoff to the user.
4. Automatically run every missing training, evaluation, render, analysis, and
   report stage whose dependencies are satisfied. Preserve the frozen
   scientific contract, full evaluation scope, checkpoint lineage, and exact
   resume semantics. Do not replace a formal stage with a smoke run.
5. Verify checkpoint readability and artifact identity. Run the official
   metrics and renders, compare the declared baseline, and close any live
   resource decision from normal runtime evidence. Mark genuinely unavailable
   evidence as `missing`, `not run`, or `partial`.
6. Update lifecycle and evidence through the ledger. Record each stage result
   with [references/report-template.md](references/report-template.md), then
   continue already authorized downstream work. Pause only when the next action
   would choose or change a scientific route, contract, claim, or final outcome.

The closure table has one row per declared stage with stage, dependency,
runtime identity, current status, expected evidence, observed evidence, and
next action. Overall status is the least complete required row.

## Boundaries

- Ground every status in current job or process state, logs, checkpoints,
  metrics, renders, and baseline paths.
- Operational repairs, resubmission, resume, evaluation, rendering, analysis,
  evidence updates, and formal reporting proceed automatically when they keep
  the approved scientific contract.
- Never choose a scientific route, alter the frozen scientific contract, or
  accept or reject the result. Present the evidence and exact decision when one
  of those choices is reached.
- If credentials, cluster access, quota ownership, unavailable inputs, or
  another external condition makes further action impossible, record the exact
  blocker and the completed evidence before reporting it. Do not use an
  external blocker to stop while a local repair or another authorized stage is
  still possible.
- An explicitly read-only request remains read-only.
