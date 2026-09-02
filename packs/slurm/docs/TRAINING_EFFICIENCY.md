# Training Efficiency

Observe once, choose placement or packing, compile the launch packet, then
close the decision as `keep`, `change`, or `unknown` from normal logs.

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
