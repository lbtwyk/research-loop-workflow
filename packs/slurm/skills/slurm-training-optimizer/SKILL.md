---
name: slurm-training-optimizer
description: Inspect live Slurm state, choose the fastest legitimate training or GPU-evaluation launch, and close the efficiency decision from normal runtime evidence. Use when queue placement, reuse of a `--reservation=interactive` allocation, resource shape, GPU occupancy, MPS, node packing, backfill, or queue breadth is still a live decision, or when a training check must decide whether to keep or change that launch.
---

# Slurm Training Optimizer

Minimize time to useful GPU work without changing scientific semantics,
exact-resume behavior, artifact isolation, or scheduler policy.

## Load

1. Read repository `AGENTS.md`, `docs/research/WORKFLOW.md`,
   `docs/research/modules/TRAINING_EFFICIENCY.md`, and
   `docs/research/modules/TRAINING_PREFLIGHT.md`.
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
accounting. Inspect a specific job further only when a missing field could
change the launch. Never infer another user's entitlement.

Choose one coherent route in this order:

1. Reuse free resources inside a verified dispatcher allocation. A plain batch
   job and node-idle GPUs outside fixed `AllocTRES` are not reusable.
2. Use the authorized `--reservation=interactive` fast path when it wins
   wall-clock time, fits the live 8-hour / 4-node / per-user job cap, and the
   1.5× NHR premium is accepted. This is the reserved node pool, not a higher
   Slurm priority score and not automatically `interactive_qos`. Use
   Slurm-owned background `sbatch` for long work.
3. Right-size GPUs, CPUs, `--mem-per-gpu`, and walltime from estimates and
   recent elapsed/`MaxRSS`; keep demonstrated OOM/timeout headroom.
4. Prefer same-effective-batch CUDA MPS for independent processes, then pack
   remaining tasks as exclusive steps in one matching multi-GPU allocation.
   Packed or array steps need unique node-local `TMPDIR` and unique atomic-write
   names; do not rewrite a shared cohort or manifest from every worker.
5. Use `--time-min` only with proved useful atomic exact resume.
6. Use bounded waves when useful jobs exceed the live backfill test cap.
7. Fall back to ordinary `workq` without the reservation when the reserved
   pool cannot start or cannot keep the 8-hour contract.

Keep `batch_size`, LR, seed, update budget, and route fixed. A matched
`batch_size` change requires explicit user approval and cannot alter a running
trajectory or only one side of a comparison.

## Compile And Launch

Pass the same snapshot to the read-only launch packet:

```bash
python scripts/experiment_ledger.py launch-packet \
  --scope SCOPE --slurm-snapshot /tmp/research-loop-slurm.json \
  EXP-ID -- EXACT-LAUNCH-COMMAND
```

When implementation is authorized, change only the operational launcher or
preflight surface, run focused validation, and use the normal ledger
preflight/launch path. Do not submit, cancel, or requeue without authority.

## Close The Efficiency Loop

During the normal explicit training check, use the first representative stable
window or terminal job evidence. Do not launch a dedicated profiling job.
Capture only decision-relevant facts already available from logs/accounting:
actual placement and `TimeLimit`, elapsed, `MaxRSS`/AveCPU, GPU utilization and
peak HBM when emitted, aggregate `update/s`, packed-step exits, and exact-resume
behavior when used.

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

Report the selected command/shape, snapshot time, evidence that determined the
choice, launch/preflight state, and the final `keep`/`change`/`unknown` closure.
Separate scheduler facts, inferred benefit, runtime proof, and scientific
acceptance.

## Boundaries

- Use `--reservation=interactive` only within the project's formal-workload
  authorization and the live reservation / `interactive_qos` / account limits.
  Treat 1.5× NHR as the reservation price, including `workq`+`normal` jobs that
  only add the reservation flag. Do not open a second reservation allocation
  when one verified allocation can take the step.
- Never weaken exact resume, provenance identity, failure visibility, or
  disjoint mutable paths to reduce wait time.
- Never use unauthorized reservation/QoS, impersonation, negative nice,
  scheduler control, false requests, or queue flooding.
- Block only a demonstrated correctness, OOM, timeout, deadlock, unusable
  throughput, or scientific-interpretation failure; uncertainty is advisory.
