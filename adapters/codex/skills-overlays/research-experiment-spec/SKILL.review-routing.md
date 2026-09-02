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
- Before every training submission, run the repository ledger preflight for the
  exact launch command. Require real data/worker, optimizer-step,
  checkpoint-resume, and first-downstream-hook proof. An immediate Slurm GPU
  allocation may be skipped when unavailable; it must never enter the queue.
  On Isambard, do not say `interactive` alone: ordinary `workq` is 1.0× NHR;
  `--reservation=interactive` is a reserved node pool at 1.5× NHR with an
  official 1-job cap and 8-hour limit; `interactive_qos` is a separate
  one-allocation QoS on that pool. Read the term table in
  `docs/research/modules/TRAINING_EFFICIENCY.md`.
- Update through ledger add/update/close/lint; never hand-edit generated views.
- Result-to-claim and experiment audit provide decision evidence. Only the user
  accepts an outcome or chooses a successor scientific route.

## Review Routing

For an expensive first launch or changed scientific contract, read
[prelaunch review](references/prelaunch-review.md) and
[lifecycle and review](references/lifecycle-and-review.md). Use one read-only
critical reviewer and follow their impact-priority rubric: core logic first,
material efficiency/resource fit second as an explicit review subsection,
scoped provenance third, and generic hardening last. The review should include
a numeric request-versus-need estimate table and a clear `PASS`, `UNCERTAIN`,
or demonstrated `BLOCKED` basis; missing precision is recorded as uncertainty,
not an automatic launch veto. For contracts with `resource_contract`, persist
the table with `record-review --resource-review-file` when available; the file
is optional and estimates are acceptable. Main-agent proof closure is sufficient
for same-contract proof
findings; use delta review only for changed semantics, reviewer judgment,
failed proof, or unresolved uncertainty.
