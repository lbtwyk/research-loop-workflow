---
name: experiment-audit
description: Audit experiment integrity before claiming results by checking artifact provenance, metric code, reported values, dead code, and evaluation scope. Use for "审计实验", "check experiment integrity", "audit results", or before result-to-claim.
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob
---

# Experiment Audit

Audit actual code and artifacts. This skill reports integrity and claim impact;
it does not accept a scientific conclusion or maintain a separate tracker.

## Canonical Experiment Adapter

When `scripts/experiment_ledger.py` and `docs/research/WORKFLOW.md` exist:

1. Resolve the explicit `EXP-ID` and run:

   ```bash
   python scripts/experiment_ledger.py outline EXP-ID
   ```

2. Read the Intent Anchor, Current Route, Current Execution Snapshot, Current
   Conclusion, contract, exact evaluator/config paths, result artifacts,
   baseline artifacts, and declared scope.
3. Do not read or create `EXPERIMENT_TRACKER.md`, `EXPERIMENT_LOG.md`,
   `findings.md`, or root-level `EXPERIMENT_AUDIT.*` files.

For repositories without this interface, audit only the explicitly supplied
code, configuration, result, ground-truth, and claim files.

## Checks

For each reported result verify:

1. **Ground-truth provenance**: dataset source versus model-derived proxy;
   classify proxy or simulation evidence explicitly.
2. **Metric semantics**: denominators, directions, units, aggregation,
   self-normalization, baseline compatibility, and whether the executed path
   actually calls the reported metric.
3. **Artifact identity**: existence, readability, exact keys/values,
   checkpoint, data split, evaluator, seed, parent/cache identity, and any
   degraded provenance.
4. **Evaluation scope**: number of examples, durations, seeds, datasets,
   comparison coverage, and whether claim wording exceeds that scope.
5. **Stage closure**: every contract-declared stage is completed or explicitly
   remaining; training completion does not hide evaluation, render, analysis,
   or handoff work.
6. **Dead or divergent paths**: defined-but-unused metrics, stale reports,
   duplicate evaluators, and results produced by code different from the
   claimed route.

Use exact `path:line` and artifact evidence. Do not require blanket hashes; bind
only identities needed to interpret the result.

## Output

Report `PASS`, `WARN`, or `FAIL` for every check and an overall verdict, then
state the impact on each intended claim:

```markdown
## Experiment Integrity Audit: EXP-ID

- overall: PASS | WARN | FAIL
- evidence_scope: ...

| Check | Status | Evidence | Claim impact |
|---|---|---|---|

### Missing Or Contradictory Evidence
- ...

### Supported Audit Conclusions
- ...

### Required Repairs Or Qualifications
- ...
```

An integrity `FAIL` prevents a clean claim from being presented until the user
reviews the failure or the demonstrated defect is repaired; the skill itself
does not change lifecycle or outcome.

## Persistence

- For a canonical experiment, durable reports belong under
  `docs/experiments/reviews/` and include the experiment ID.
- Record the report path in the experiment spec or ledger only when persistence
  is part of the task.
- Do not write a project-root audit file or a second machine tracker.
- Use a fresh reviewer only when the user explicitly asks for one. A same-family
  reviewer is a second perspective, not independent acceptance.

If an optional reviewer is used, retain its trace following
`../shared-references/review-tracing.md`.
