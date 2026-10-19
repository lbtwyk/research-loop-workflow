---
name: slurm-training-optimizer
description: Inspect Slurm resources and select the lowest-cost feasible training or GPU-evaluation shape within 10% of the fastest comparable time to result. Use when placement, allocation reuse, resource shape, concurrency, backfill, or queue breadth can change the next launch, or a training check must close that efficiency decision.
---

# Slurm Training Optimizer

Balance time to all declared results and billed compute: default to the
lowest-cost feasible shape within 10% of the fastest comparable shape. Preserve
scientific semantics, exact resume, artifact isolation, and scheduler policy.

## Load

1. Read repository `AGENTS.md`, `docs/research/WORKFLOW.md`,
   the installed `TRAINING_EFFICIENCY.md` and `TRAINING_PREFLIGHT.md`
   (under `docs/research/` or the project's `docs/research/modules/`),
   and the Isambard site overlay when applicable.
2. Resolve the explicit experiment and run:

   ```bash
   python scripts/experiment_ledger.py outline EXP-ID
   ```

3. Read the exact launch, frozen scientific fields, mutable paths, resource and
   efficiency contracts, exact-resume proof, and comparable runtime evidence.
4. Read [the strategy reference](references/slurm-strategies.md) only for the
   detailed immediate-allocation, dispatcher, MPS, packing, or backfill syntax
   needed by this task.

## Observe And Choose

Capture one common scheduler input:

```bash
python scripts/slurm_state_snapshot.py \
  --output /tmp/research-loop-slurm.json
```

Use its jobs, active steps, `dispatcher_ready`/`reusable_gpus`, QoS,
reservations, partitions, pending reasons, scheduler parameters, and recent
accounting. Include hidden partitions with `--all` and retain `PrivateData`;
do not infer peer usage or access from incomplete visibility. Reservation fields
such as `Accounts=root` alone do not prove account denial: use a correctly
routed bounded probe. Inspect a specific job further only when a missing field could
change the launch. Never infer another user's entitlement.

The capture expands array elements and separates `recent_jobs` allocations
from `recent_steps` execution statistics. Use actual allocated/billed resources,
not just the request. Missing usage is unknown, not zero; failed/unknown step
usage cannot establish free dispatcher GPUs. Respect the capture interval.

Compare the ordinary request with one or two useful alternatives under the same
contract and remaining-result horizon. Respect authorized resource/concurrency
caps, remaining budget, deadlines, memory and real-time constraints first.
Use matched prior evidence, with short probes only when decision-relevant.
Compare end-to-end queue/startup/critical-path/retry time and all remaining
billed node-hours, including switch costs. Remove dominated shapes, then choose
the lowest cost within `T_best * 1.10`; use faster time to break cost ties.
Only an explicit user/contract choice overrides the 0.10 tolerance. The ordinary
request remains a fallback when it satisfies the same hard limits.

Follow the installed `TRAINING_EFFICIENCY.md` input format. The read-only
`scripts/slurm_resource_policy.py` computes this choice; pass candidate estimates
to the existing launch packet with `--resource-candidates FILE`. Missing time,
cost or evidence is unranked, never free; selection is among quantified
comparable candidates, not a proven global optimum.

Generate only useful candidates; this list is not a fixed ranking:

1. Reuse free resources inside a verified dispatcher allocation. A plain batch
   job and node-idle GPUs outside fixed `AllocTRES` are not reusable.
2. On Isambard use `--reservation=interactive` for short preflight, debugging
   or exploratory work within live limits and the accepted 1.5x NHR premium.
   Do not specify `--partition` or override `--qos`; the reservation selects
   the hidden partition and its QoS limits. Long-running or high-throughput
   training uses ordinary `workq`, not this pool.
3. Right-size GPUs, CPUs, `--mem-per-gpu`, and walltime from estimates and
   recent elapsed/`MaxRSS`; keep demonstrated OOM/timeout headroom.
4. Consider same-effective-batch MPS for independent underfilled compute tasks
   after a matched canary, not for a frozen no-MPS or real-time controller.
   Compare true per-GPU jobs with matching multi-GPU packing by time and cost.
   Packed or array steps need unique node-local `TMPDIR` and unique atomic-write
   names; do not rewrite a shared cohort or manifest from every worker.
5. Use `--time-min` only with proved useful atomic exact resume.
6. Use bounded waves when useful jobs exceed the live backfill test cap.
7. Fall back to ordinary `workq` without the reservation when the reserved
   pool cannot start or the workload is outside its short-lived scope.

Keep `batch_size`, LR, seed, update budget, and route fixed. A matched
`batch_size` change requires explicit user approval and cannot alter a running
trajectory or only one side of a comparison.

## Compile And Launch

Pass the same snapshot to the read-only launch packet:

```bash
python scripts/experiment_ledger.py launch-packet \
  --scope SCOPE --slurm-snapshot /tmp/research-loop-slurm.json \
  --resource-candidates /tmp/resource-candidates.json \
  EXP-ID -- EXACT-LAUNCH-COMMAND
```

Candidates must bind the same snapshot timestamp. The recommendation does not
rewrite/execute the launch command or confer resource-budget approval. Compile
the selected exact command and validate it through the existing normal gate.
Settled launches need no fresh candidate file on every check.

When implementation is authorized, change only the operational launcher or
preflight surface, run the selected exact-command correctness preflight, and
use the normal ledger launch path. This skill does not authorize changing a
scientific contract or canceling unrelated jobs.

## Close The Efficiency Loop

During the normal explicit training check, use the first representative stable
window or terminal job evidence. Do not launch a dedicated profiling job.
Capture only decision-relevant facts already available from logs/accounting:
actual placement and `TimeLimit`, elapsed, `MaxRSS`/AveCPU, GPU utilization and
peak HBM when emitted, comparable useful work/s and work/billed node-hour,
packed-step exits, and exact-resume
behavior when used.

Reconsider future allocations at task completion, stage transition, a safe
checkpoint/relaunch boundary, or materially changed throughput/availability,
budget or deadline. Allocate incremental resources to the approved critical
path where finish-time gain per extra node-hour is greatest. Include restart
and requeue costs; keep the current shape when they erase the benefit. Never
cancel, resize, migrate or edit a running frozen job to enact this policy.

Return exactly one efficiency decision:

- `keep`: the request is adequate; do not revisit it until workload or scheduler
  facts materially change.
- `change`: give the exact operational change, evidence, expected benefit, and
  fallback; validate it before the next launch.
- `unknown`: precision is insufficient but no demonstrated failure changes the
  launch; keep it advisory.

Update existing `resource_contract` or `efficiency_contract` only when `change`
modifies the launch. Runtime evidence stays with normal logs/artifacts and the
experiment execution snapshot. Do not create a tracker, scorecard, or repeated
self-audit.

Report the normal and selected shapes, snapshot interval, evidence, estimated
time to result and billed cost for each, the 10% band/explicit override,
launch/preflight state, and the final
`keep`/`change`/`unknown` closure.
Separate scheduler facts, inferred benefit, runtime proof, and scientific
acceptance.

## Boundaries

- Use `--reservation=interactive` only for site-permitted short-lived work
  within the live reservation / partition QoS / account limits. Never combine
  it with an explicit partition or QoS override on Isambard. Project approval
  does not override site policy. Do not open a second reservation allocation
  when one verified allocation can take the step.
- Never weaken exact resume, provenance identity, failure visibility, or
  disjoint mutable paths to reduce wait time.
- Never use unauthorized reservation/QoS, impersonation, negative nice,
  scheduler control, false requests, or queue flooding.
- Block only a demonstrated correctness, OOM, timeout, deadlock, unusable
  throughput, or scientific-interpretation failure; uncertainty is advisory.
