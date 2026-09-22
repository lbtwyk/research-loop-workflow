# Research Workflow

This is the canonical human-facing workflow. The experiment ledger is the
single interface for durable state. Skills, GitHub, a scheduler, and generated
Markdown views are adapters around it.

## Sources Of Truth

| Concern | Owner |
|---|---|
| Scientific question, Intent Anchor, route history, evidence, conclusion | One `docs/experiments/EXP-*.md` spec |
| Lifecycle, outcome, current conclusion, latest artifact, next action | `docs/experiments/registry.json` |
| Frozen data, model, training, evaluation, launcher, and stage semantics | The experiment contract JSON |
| Independent review decision and evidence | `docs/experiments/reviews/` |
| Execution proof and current runtime facts | The selected compute module's receipt, job, session, logs, and artifacts |
| Current and historical navigation | Generated `ACTIVE.md` and `INDEX.md` |

Do not create parallel trackers such as `EXPERIMENT_LOG.md`,
`EXPERIMENT_TRACKER.md`, or `findings.md`. Do not use GitHub labels, W&B
state, scheduler state, or generated views as scientific authority.

## Entering Experiment Work

Resolve the experiment from the user's explicit request or the objective
already adopted by the task. A dormant worktree focus is only a ledger default.

```bash
python scripts/experiment_ledger.py outline EXP-ID
```

Read only the sections required by the current phase:

- planning: Intent Anchor and Current Route;
- semantic implementation: add Current Execution Snapshot and the contract;
- monitoring or recovery: add logs, manifests, checkpoints, and resume identity;
- review or launch: add the full contract and review context;
- evaluation or claim analysis: add exact artifacts, metrics, renders,
  provenance, and Current Conclusion.

Use `ACTIVE.md` only when the experiment identity is missing or changing. Use
`INDEX.md` only for history.

## Claim-Centered Planning And Narrative

- **Lead with one advantage.** State the problem, why the current approach is
  insufficient, the route's leading advantage, and the bounded claim that
  advantage could support.
- **Choose the battlefield.** Compare on the task, metric, or operating
  constraint that reflects the claimed value.
- **Assign one proof role per experiment.** Prove the method works, explain
  where the advantage comes from, demonstrate value in the target setting, or
  rule out a competing explanation.
- **Let evidence reshape the claim.** Preserve a non-win. Do not automatically
  promote it into a global weakness.
- **Write the final logic, not the chronology.** Lead with
  `problem -> gap -> method -> decisive evidence -> supported conclusion`.
- **Use limitations proportionately.** State evidence that materially bounds
  the claim, reproducibility, interpretation, or intended use.

## Lifecycle

```text
draft -> ready -> queued -> running -> evaluating -> deciding -> closed
```

`blocked` may interrupt any active phase. Outcome is separate from lifecycle
and is recorded only as `accepted`, `rejected`, `inconclusive`, or
`superseded`. A finished scheduler job is runtime evidence, not experiment
completion or scientific acceptance.

Create a new experiment only for a new falsifiable claim, causal intervention,
or a materially changed frozen contract. Bug fixes, recovery, replication,
refactoring, and same-claim revisions stay as routes or runs in the parent.

## End-To-End Flow

1. The user chooses the scientific question, leading advantage, battlefield,
   bounded claim, and approved route.
2. The spec records those choices. A contract freezes executable semantics
   when formal work is required.
3. Implementation and focused tests establish readiness.
4. Materially changed scientific semantics or a demonstrated high-risk
   execution change receives one independent read-only review. A first launch,
   new experiment ID, or routine ablation reusing reviewed semantics uses
   focused validation.
5. Select the installed compute module and prepare the exact launch. Use its
   resource and preflight rules only where they apply.
6. Record the command, environment, runtime identity, logs, and expected
   artifacts in the experiment. The compute module owns submission and live
   status checks.
7. Verify actual progress and the declared downstream stages. Reuse the same
   contract for operational recovery.
8. Update the ledger with the observed runtime and evidence.
9. A training check owns the operational loop: inspect, repair demonstrated
   same-contract failures, complete declared stages, and report. It never
   accepts the science.
10. Experiment audit verifies code, artifacts, metric values, provenance, and
    evaluation scope.
11. Result-to-claim names the strongest supported claim and the comparison
    that carries it.
12. The user decides the scientific outcome. The ledger then updates or closes
    the experiment.
13. Sync finished code, documents, and useful evidence to the repository when
    ready so Web can read them. Update issue/PR discussion for stage results or
    needed decisions, not for each repository push.

Keep implementation, scheduler state, runtime proof, and scientific acceptance
explicitly separate.

Compute modules: `LOCAL_TRAINING.md` for a direct GPU, `SLURM.md` and
`PREFLIGHT.md` for Slurm, or `KUBERNETES.md` for Kubernetes/KubeSphere. A
project may install more than one; choose by the actual execution target.

## Stage Closure

Use contract `launch_scopes` as the executable stage list. A scope may declare
`depends_on` and exact `completion_evidence` files. The evidence must be the
final artifact or receipt, not a broad output directory.

The ledger's stage view partitions declared scopes into completed or remaining.
It never submits a job. The selected compute module explains any scheduler
snapshot or launch command.

## Skill Responsibilities

- `research-experiment-spec`: resolve the experiment and load phase-specific
  context.
- `experiment-audit`: verify evidence and place durable reports under the
  experiment review directory.
- `result-to-claim`: name the strongest supported claim and the comparison
  that carries it.
- `ablation-planner`: give each proposed experiment one claim-relevant proof
  role.
- `research-review`: a read-only second perspective when explicitly requested
  or required by the formal review gate.
- `github-research-handoff`: sync research outputs; discuss stage results or
  needed decisions in issues and PRs.
- Compute-specific training checks and resource optimization belong to their
  compute modules.

Novelty and formula work may inform a spec. Neither owns experiment lifecycle.

## Durable Updates

```bash
python scripts/experiment_ledger.py update EXP-ID ...
python scripts/experiment_ledger.py close EXP-ID ...
python scripts/experiment_ledger.py sync
python scripts/experiment_ledger.py lint
```

Preserve negative evidence, replaced-route reasons, exact artifact provenance,
and unsupported conclusions.
