# Training Efficiency

Choose the lowest-cost feasible shape whose estimated time to all remaining
declared results is within **10% of the fastest comparable feasible shape**.
This is the default near-fastest policy, not a claim of global optimality.
An explicit user or frozen-contract setting may override `slowdown_tolerance`.
Preserve scientific batch, optimizer, LR, seed, exposure/update budget, inputs,
evaluation scope, exact resume, and disjoint mutable paths.

Use this module while placement, resource shape, or concurrency can change the
decision. A settled launch does not pay another review. Missing precision is
advisory; demonstrated correctness, OOM, timeout, deadlock, real-time execution,
or unusable-throughput failures rule out the affected candidate.

## Observe Once

```bash
python scripts/slurm_state_snapshot.py --output /tmp/research-loop-slurm.json
```

- Queue capture uses `--all --array`: hidden partitions and individual array
  elements retain their resource identity. Inspect only current-user resources;
  retain `PrivateData` and source failures instead of inferring peer access.
- `recent_jobs` contains allocation records; `recent_steps` contains the
  execution-step statistics from the same `sacct` query, without `-X`.
  Use actual `AllocTRES` for placement/billing and step `max_rss`, `total_cpu`,
  and available GPU TRES usage for runtime evidence. Missing statistics are
  `null`, not zero. `MaxRSS` is a task maximum, not total concurrent host usage;
  include other processes and shared/tmpfs memory when sizing concurrency.
- `capture_started_at` through `captured_at` is an observation interval, not
  an atomic scheduler transaction. Recheck a changed fact before the next launch.
  A failed step query or unknown step GPU usage cannot establish reusable GPUs.
- Use matched normal logs first. Capture extra telemetry or a short canary only
  when its result can change this choice; do not create a profiling job.

## Compare Time And Cost

Compare the ordinary request with one or two useful alternatives for the same
frozen contract and the same remaining work. Feasibility includes the authorized
GPU/concurrency cap, remaining budget, site limits, memory/headroom, real-time
requirements, provenance, and exact-resume behavior. Do not invent a project
budget or an entitlement from visible idle resources.

For each candidate, record GPUs/CPUs/host memory/HBM, placement, measured useful
throughput, and evidence. Label queue wait and other estimates explicitly.

```text
T = estimated queue wait + startup/restart + remaining critical-path runtime
    + declared evaluation, rendering and reporting + expected retry overhead
C = remaining billed node-hours across that same work, including allocated
    idle time, startup, retries and switching overhead
T_best = min(T) among comparable, quantified candidates satisfying hard limits
choose lowest C among candidates with T <= T_best * (1 + 0.10)
```

Do not add parallel branch runtimes as if they were sequential. The 10% band
applies to the common remaining-result horizon, not independently to each stage
or wave. Respect a declared deadline and budget before finding `T_best`. Remove
candidates that are both slower and no cheaper; break cost ties by faster time.
Queue waiting without an allocation is not billed runtime. Use the site's
actual billing rule and allocation shape, not requested CPU count or an assumed
GPU-hour conversion. Reusing a held allocation does not make its remaining
occupancy free.

Useful throughput means eligible targets/s for different approved training
batches, or completed valid trials/videos per hour for their respective stages.
Compare useful work per billed node-hour within the same workload; do not add
unrelated updates/s. GPU busy %, HBM occupancy, SM activity and bandwidth are
diagnostics, not interchangeable objectives or reasons to fill memory.

## Read-Only Selection In The Existing Launch Packet

Prepare candidate estimates with existing logs/contracts; this is an input to
the existing launch packet, not a new tracker. Example numbers below are
illustrative, not measured performance:

```json
{
  "schema_version": 1,
  "snapshot_captured_at": "COPY captured_at FROM THE SNAPSHOT",
  "comparison_basis": "same frozen contract and all remaining declared results",
  "candidates": [
    {"id": "ordinary", "feasible": true, "time_to_result_seconds": 100,
     "cost_nhr": 10, "evidence": ["matched logs and billing; estimated queue wait"]},
    {"id": "balanced", "feasible": true, "time_to_result_seconds": 110,
     "cost_nhr": 6, "evidence": ["matched canary and billing; estimated queue wait"]}
  ]
}
```

Optional fields are `slowdown_tolerance` (fraction, default `0.10`),
`cost_budget_nhr` (remaining authorized budget), and `deadline_seconds` (remaining
time to the required result). Use `feasible: false` plus `reason` for a ruled-out
shape. Missing time, cost, or evidence leaves a candidate `unranked`; it cannot
win by being treated as free. Selection is among quantified comparable shapes.
No rankable candidate yields `unknown` or `infeasible`, not a fabricated optimum.

```bash
python scripts/experiment_ledger.py launch-packet \
  --scope SCOPE --slurm-snapshot /tmp/research-loop-slurm.json \
  --resource-candidates /tmp/resource-candidates.json \
  EXP-ID -- EXACT-LAUNCH-COMMAND
```

The packet binds candidates to the snapshot timestamp and returns
`resource_selection`. It never rewrites or executes the supplied command;
`launch.ready` still describes the existing correctness/dependency gates, not
resource-budget approval. Check the selection/limits, compile the chosen exact
command, and run/reuse its normal correctness preflight before normal ledger
launch. An unknown estimate does not block a settled ordinary fallback; a
demonstrated budget or resource violation cannot authorize that fallback.
Standalone arithmetic is available through
`python scripts/slurm_resource_policy.py /tmp/resource-candidates.json`.
The CLI override `--slowdown-tolerance` is a fraction and must reflect an
explicit user/contract choice, not an agent changing the default opportunistically.

## Workload-Dependent Candidates

- Reuse only verified, uncommitted resources within a dispatcher's fixed
  allocation and remaining time. Plain batch jobs are not dispatchers.
- Right-size CPUs, host memory, GPU memory and walltime with measured headroom.
  A smaller CPU request need not reduce actual allocation or billing.
- Consider same-effective-batch MPS for independent underfilled compute
  processes after a matched canary shows useful aggregate gain and acceptable
  individual slowdown. Do not add MPS to a frozen no-MPS or real-time controller
  contract. Memory headroom alone does not establish a gain.
- Compare true per-GPU jobs with matching multi-GPU packing; neither is a fixed
  winner. Use job-level exclusivity only when consuming/requiring the node.
  Concurrent exclusive steps need isolated TMPDIR, atomic-write names, mutable
  outputs, and every exit status propagated. Reuse loaded models/read-only
  caches for short tasks where the contract permits it.
- Use `--time-min` only with proven atomic exact resume and useful work after
  startup/checkpoint/cleanup. Use bounded waves when eligible jobs exceed the
  live backfill examination cap. Dependencies represent real prerequisites.
- On Isambard, `--reservation=interactive` is for short preflight/debugging or
  exploration, with reservation-only routing and the 1.5x NHR premium; formal
  long-running/high-throughput work uses `workq`. Read the installed site overlay
  (`isambard-site.md` in a plain install, or the project's host guidance).

## Dynamic Reallocation And Closure

Reconsider the next allocation at task completion, stage transition, a safe
checkpoint/relaunch boundary, or a material change in availability, measured
throughput, budget or deadline. Prefer incremental resources where they most
reduce the approved workload's critical-path finish per extra billed node-hour;
do not invent scientific priorities. Keep the current shape when queue,
checkpoint/restart and switching costs erase the benefit. Do not poll unchanged
state, repeatedly benchmark a settled choice, or hold idle resources for future
waves. Release completed allocations and avoid stranded tails.

Do not cancel, resize, migrate, retune, or edit the frozen source of running
formal jobs to enact this policy. Apply validated operational changes to future
submissions only. An unmatched batch/precision change needs explicit scientific
authorization and cannot alter a running comparison.

At the normal stable-window or terminal training check, return one decision:
`keep`, `change` (exact next-launch change, evidence, benefit and fallback), or
`unknown` (missing precision remains advisory). Record a durable resource
decision in the existing `resource_contract`/`efficiency_contract` and execution
snapshot only when it changes the next launch. Separate estimated benefit,
measured runtime, stage closure and scientific acceptance. No extra scorecard,
efficiency tracker or scheduling daemon is required.
