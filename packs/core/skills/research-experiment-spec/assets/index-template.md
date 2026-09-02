# Experiment Index

This is a generated view. Use `registry.json` as the lifecycle-metadata source of truth and full `EXP-*.md` specs as the complete source of truth for design, evidence, history, and conclusions.

## Active Experiments

| ID | Lifecycle | Outcome | Branch/Worktree | Core Change | Current Conclusion | Latest Artifact | Next Action |
|---|---|---|---|---|---|---|---|
| _none yet_ |  |  |  |  |  |  |  |

## Closed Experiments

| ID | Lifecycle | Outcome | Branch/Worktree | Core Change | Current Conclusion | Latest Artifact | Next Action |
|---|---|---|---|---|---|---|---|
| _none yet_ |  |  |  |  |  |  |  |

## State Model

- Lifecycle: `draft`, `ready`, `queued`, `running`, `evaluating`, `deciding`, `blocked`, `closed`.
- Outcome: `accepted`, `rejected`, `inconclusive`, `superseded`, or `unclassified`.

## Rules

- Read `ACTIVE.md` first, then the relevant complete spec.
- Create a new spec only for a new falsifiable question, claim, causal intervention, or materially changed frozen contract.
- Keep seeds, retries, checkpoints, evaluations, renders, and presentation artifacts under their parent experiment.
- Include the experiment ID in run, Slurm, render, metric, and checkpoint paths when practical.
- Never truncate or summarize away prior experiment conclusions.
