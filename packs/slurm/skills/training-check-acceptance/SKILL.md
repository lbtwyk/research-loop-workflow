---
name: training-check-acceptance
description: "Run one complete training check: inspect progress, recover same-contract failures, fill declared stages, evaluate finished runs, and report results. Use when the user asks to check training status, failures, resume, missing stages, results, or acceptance."
---

# Training Check Acceptance

On each explicit `check` request, complete one bounded check-and-act cycle. Do
not persistently monitor or wait for separate repair, evaluation, or reporting
prompts.

## Workflow

1. Resolve the experiment from the explicit request, run
   `scripts/experiment_ledger.py outline <EXP-ID>`, then read repository
   guidance, the relevant spec sections, and contract. Capture scheduler state
   once with `scripts/slurm_state_snapshot.py --output /tmp/research-loop-slurm.json`,
   then compile the exact command with `scripts/experiment_ledger.py
   launch-packet --scope SCOPE --slurm-snapshot /tmp/research-loop-slurm.json EXP-ID --
   EXACT-LAUNCH-COMMAND`. Start the closure table from that packet's contract
   scopes, dependencies, launch manifests, jobs, and exact evidence paths.
   Inspect logs, checkpoints, metrics, renders, or a launcher DAG only where the
   packet reports missing or unverified state. Include downstream scopes even
   when they have no job ID yet.
2. Classify the task as `running`, `interrupted`, `stalled`, `not_started`,
   `needs_eval`, or `completed`. Scheduler `COMPLETED` and a final checkpoint
   prove runtime/training completion only.
3. For `running`, verify real advancement, avoid duplicate submission, and
   report the latest meaningful milestone. For `interrupted` or `stalled`,
   diagnose the demonstrated failure, make at most one same-contract operational
   repair, resume through the guarded ledger launcher, and verify new progress.
   Every new or resumed training submission must run or reuse the exact-identity
   training preflight receipt. An immediate GPU preflight may be
   `skipped_unavailable`; it must never be queued, and a started GPU program
   failure remains blocking.
4. Complete any declared missing training, evaluation, render, analysis, or
   report stage
   whose dependencies are satisfied. Preserve the frozen contract, full scope,
   resource class, and exact-resume semantics; never substitute a smoke run.
   A terminal trainer releases downstream work; it never removes that work
   from the closure table. Repair or submit missing downstream stages in this
   same check when authorized.
5. After training finishes, verify checkpoint readability and artifact identity,
   run missing official metrics/renders, and compare the strongest relevant
   baseline. Mark unavailable evidence `missing`, `not run`, or `partial`. If
   resource shape, placement, or utilization was a live decision, close it at
   the first representative stable window or terminal state from normal logs
   and accounting: return `keep`, an exact operational `change` for the next
   launch, or advisory `unknown`. Do not launch a separate profiling job.
   When recording placement, name partition, reservation, and QoS separately.
   Site billing and reservation caps live in the slurm site overlay, not in
   this skill. Do not open a second reservation job if one verified
   allocation can take the step.
6. Claim `completed` only after every contract-declared stage and its evidence
   exist, including required metrics, renders, baseline comparison, and analysis
   where declared. For every completed task, fill
   [references/report-template.md](references/report-template.md). Update state
   through the ledger; never hand-edit generated views. A scientific outcome
   remains pending until the user decides it.

The closure table has one row per declared stage with stage name, dependency,
job ID or `not submitted`, scheduler/runtime status, expected artifact, observed
artifact, and next action. Overall status is the least-complete required row,
not the status of the root or longest-running job.

## Boundaries

- Ground every status in exact job, log, checkpoint, metric, render, and baseline
  paths. Do not hide upstream data/cache corruption with downstream patches.
- Do not change scientific routes/contracts, modify reviewed source during an
  active run, accept/reject results, merge, or cancel for scientific reasons.
  A new expensive launch still goes through `research-experiment-spec` and
  the installed agent adapter's independent reviewer.
- Escalate only repeated or ambiguous failure, a scientific choice, missing
  authority, or final acceptance. In explicitly non-mutating requests, observe
  and report only.
- End after the response; another cycle requires another explicit `check`.
