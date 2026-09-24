# Training Efficiency

For a new or unsettled cluster launch, list the ordinary resource request and
one or two viable faster shapes. Compare expected queue wait plus time to the
declared result, not GPU count or isolated step speed. Use recent matched
runtime evidence first; run short, bounded probes only when the choice remains
open. Preserve the scientific batch, optimizer, seed, update budget, inputs,
and evaluation scope across candidates.

Record for each candidate: GPUs and memory, placement/queue, expected wait,
measured or inferred update throughput, total time to result, failure risk,
and evidence. Mark estimates as estimates. Select the fastest viable shape,
keep the ordinary one as fallback, then run the exact-launch correctness
preflight. Recheck the choice only when workload or scheduler facts change.

Resource choices may close as `keep`, `change`, or `unknown` from normal logs.

## Order

1. Reuse a verified running allocation when the step fits.
2. Right-size GPUs, CPUs, memory, and walltime from code-backed estimates and
   recent elapsed or MaxRSS evidence.
3. Prefer same-effective-batch GPU sharing (for example MPS) before adding
   GPUs.
4. Prefer whole-node exclusive packing before an unmatched `batch_size`
   change.
5. Use checkpointable backfill and bounded waves when the queue is the
   constraint.
6. Fall back to the site's ordinary partition when a reserved pool does not
   fit.

Do not retune a running formal job. Record a durable resource decision only
when it changes the next launch.

Site billing, reservation names, and per-user caps live in
[isambard-site.md](isambard-site.md) or a project overlay. Reservation name
for preflight is `RESEARCH_LOOP_SLURM_RESERVATION` (default `interactive`).
