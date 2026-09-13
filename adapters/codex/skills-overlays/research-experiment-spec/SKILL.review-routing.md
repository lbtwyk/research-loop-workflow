---
name: research-experiment-spec
description: Maintain experiment specs, lifecycle, routes, launches, evidence, and conclusions. Use for planning, running, resuming, evaluating, or closing ML experiments.
---

# Research Experiment Spec

Keep one canonical spec per scientific question. Preserve conclusions, negative
evidence, decision reasons, measurements, and artifact provenance.

When present, `docs/research/WORKFLOW.md` is the human-facing ownership and
lifecycle reference. This skill is its phase-loading adapter; it does not create
a second tracker.

## Load By Phase

1. Resolve the experiment from the current user request or the objective already
   adopted by this thread. Dormant worktree focus is not task authority. Use
   ACTIVE.md only for navigation when the experiment is missing or changing.
2. Run scripts/experiment_ledger.py outline [EXP-ID].
3. Planning reads Intent Anchor and Current Route. Semantic implementation adds
   Current Execution Snapshot and the full contract. Monitoring/recovery reads
   the snapshot, logs, manifest, checkpoint, and accepted contract identity.
Critical review/formal launch loads the full contract and review context.
Evaluation/handoff reads exact artifacts, metrics, renders, provenance, and
the current conclusion.
4. Use INDEX.md only for history.

## Experiment Versus Route

Create a new EXP only for a new falsifiable claim, causal intervention, or
materially changed frozen data, representation, training, or evaluation
contract. Keep bug fixes, refactors, replications, and same-claim revisions as
routes/runs in the parent.

When substantively touching an active spec, lazily converge navigation to
Intent Anchor, Current Route, Current Execution Snapshot, and Current Conclusion
and Next Action. Do not bulk-migrate untouched specs. Preserve each replaced
route's design, reason, decisive evidence, decision, successor, and artifacts.

## Evidence And Execution

- Keep focus private and dormant per worktree. Read or update it only after the
  thread has explicitly entered formal experiment work; when an inferred target
  differs from stored focus, ask before replacing it.
- Record matched controls, invariants, data/cache semantics, training/evaluation
  shape, gates, failure signals, tracking, cadence, and reviewable renders.
- Separate implementation, scheduler state, runtime proof, and scientific
  acceptance.
- Treat training completion as one stage, never experiment completion. Before a
  route is closed or handed off as complete, reconcile every declared
  downstream evaluation, render, analysis, and reporting stage against its
  expected artifact and recorded job; preserve unsubmitted stages explicitly.
- Compile that closure from contract `launch_scopes`, ledger launch manifests,
  exact `completion_evidence`, and one current Slurm snapshot. Use
  `scripts/slurm_state_snapshot.py --output /tmp/m2d-slurm.json`, then
  `scripts/experiment_ledger.py launch-packet --scope SCOPE --slurm-snapshot
  /tmp/m2d-slurm.json EXP-ID -- EXACT-LAUNCH-COMMAND`. The packet is read-only;
  do not create a parallel stage tracker or treat it as scientific acceptance.
- Preserve commit, environment, command, jobs/logs, parent/cache identity,
  checkpoints, resume point, review basis, failures, metrics, and next action.
- On a direct-attached GPU, validate changed seams and use the formal run's
  early real-data, optimizer, memory, throughput, and checkpoint evidence as
  execution proof. Require standalone resume, downstream-hook, or resource
  proof when that seam changed, failed, or presents a concrete live risk.
  Cluster launch/preflight remains scheduler-pack policy.
- Update through ledger add/update/close/lint; never hand-edit generated views.
- Result-to-claim and experiment audit provide decision evidence. Only the user
  accepts an outcome or chooses a successor scientific route.

## Review Routing

For materially changed scientific semantics or a demonstrated high-risk
execution change, read
[prelaunch review](references/prelaunch-review.md) and
[lifecycle and review](references/lifecycle-and-review.md). Use one read-only
critical reviewer and follow their impact-priority rubric: core logic first,
live material efficiency/resource risk second, scoped provenance third, and
generic hardening last. A first launch, new experiment ID, or routine ablation
does not normally trigger review when reviewed semantics and runtime paths are
reused. Resource estimates are useful when they can change the launch. Return a
clear `PASS` or demonstrated `BLOCKED`, with `UNCERTAIN` only for a material
open question. Main-agent proof closure is sufficient for same-contract proof
findings; use delta review only for changed semantics, reviewer judgment,
failed proof, or unresolved uncertainty.
