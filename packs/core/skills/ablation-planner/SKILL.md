---
name: ablation-planner
description: Design reviewer-oriented ablation studies after promising or partial results. Use for "设计消融", "还缺哪些消融", "怎么证明每个模块有效", or when result-to-claim identifies a bounded evidence gap.
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit
---

# Ablation Planner

Design the smallest experiment set that distinguishes competing explanations.
Planning is not authorization to implement or launch.

## Canonical Experiment Adapter

When `scripts/experiment_ledger.py` and `docs/research/WORKFLOW.md` exist:

1. Resolve the explicit `EXP-ID` and run:

   ```bash
   python scripts/experiment_ledger.py outline EXP-ID
   ```

2. Read the Intent Anchor, Current Route, Current Conclusion, exact result
   artifacts, frozen invariants, available controls, and compute evidence.
3. Use the experiment spec and contract instead of `EXPERIMENT_LOG.md`,
   `EXPERIMENT_TRACKER.md`, `findings.md`, or legacy research contracts.
4. Classify each proposal:
   - same claim and invariant contract: a route or run in the parent experiment;
   - new falsifiable claim, causal intervention, or materially changed frozen
     data/representation/training/evaluation contract: a candidate new
     experiment requiring user approval.

For other repositories, use only explicitly supplied method, result, and budget
files; do not invent a tracker.

## Design

For every proposed ablation state:

- `name` and exact intervention;
- `what_it_tests` and the competing explanations it separates;
- frozen controls and matched identities;
- `expected_if_component_matters`;
- decisive metrics, qualitative evidence, and failure signals;
- estimated GPU/CPU/memory/walltime and dependencies;
- priority and why a cheaper experiment cannot answer the same question;
- whether it is a parent route or candidate new experiment.

Prioritize component removal/replacement and high-information controls over
wide hyperparameter sweeps. Delete no-op or low-information ablations.

## Required Output

```markdown
## Candidate Ablation Plan

| Priority | Route | What it tests | Frozen controls | Decision evidence | Compute | Dependency |
|---|---|---|---|---|---|---|

### Unnecessary Ablations
- ...

### Proposed Run Order
1. ...

### Contract Impact
- parent routes: ...
- candidate new experiments: ...
- user decisions required: ...
```

Use a fresh reviewer only when the user explicitly requests a second opinion.
Treat its suggestions as input, not authority.

## Approval Boundary

- Stop after the plan unless the user explicitly authorizes implementation or
  launch.
- After approval, record the route in the canonical experiment spec, update or
  create the contract as required, and follow the normal review/launch flow.
- Never silently drop an approved comparison, change budget, implement a
  different intervention, or choose the winning route.
- Preserve negative ablation evidence in the parent experiment spec.

If an optional reviewer is used, retain its trace following
`../shared-references/review-tracing.md`.
