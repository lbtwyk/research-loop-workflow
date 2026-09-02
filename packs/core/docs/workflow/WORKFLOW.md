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
| Pre-queue executable proof | Ignored scheduler receipt bound to the exact launch |
| Current scheduler facts | One explicit snapshot, when a scheduler pack is installed |
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
4. The first expensive launch or a changed scientific contract receives one
   independent read-only review. Same-contract operational repairs use focused
   validation.
5. If resource shape is still unsettled and a scheduler pack is installed,
   choose the launch from live evidence. Prefer same-effective-batch sharing,
   then whole-node exclusive packing, before unmatched batch-size changes.
6. When a scheduler snapshot exists, compile the exact launch packet. The
   packet does not submit anything.
7. A new or changed training identity runs one real-path preflight; an
   unchanged identity reuses its receipt. Immediate GPU probes may be
   `skipped_unavailable` only if the program never starts.
8. Launch and durable runtime identity go through the ledger.
9. A training check owns the operational loop: inspect, repair demonstrated
   same-contract failures, complete declared stages, and report. It never
   accepts the science.
10. Experiment audit verifies code, artifacts, metric values, provenance, and
    evaluation scope.
11. Result-to-claim names the strongest supported claim and the comparison
    that carries it.
12. The user decides the scientific outcome. The ledger then updates or closes
    the experiment.
13. GitHub handoff publishes ledger-backed evidence. It does not create a
    second status record.

Keep implementation, scheduler state, runtime proof, and scientific acceptance
explicitly separate.

Preflight is specified in [PREFLIGHT.md](PREFLIGHT.md). `launch` and
`preflight` require the slurm pack. Without that pack, use `outline`, `add`,
`update`, `close`, `sync`, `lint`, and the review commands.

## Stage Closure

Use contract `launch_scopes` as the executable stage list. A scope may declare
`depends_on` and exact `completion_evidence` files. The evidence must be the
final artifact or receipt, not a broad output directory.

```bash
python scripts/experiment_ledger.py launch-packet \
  --scope SCOPE --slurm-snapshot /tmp/research-loop-slurm.json \
  EXP-ID -- EXACT-LAUNCH-COMMAND
```

The packet partitions declared scopes into completed or remaining. It never
submits a job.

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
- `github-research-handoff`: publish existing evidence and decision requests.
- `training-check-acceptance` and `slurm-training-optimizer` belong to the
  slurm pack.

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
