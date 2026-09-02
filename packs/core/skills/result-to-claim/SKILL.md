---
name: result-to-claim
description: After experiments finish, name the strongest supported claim and the comparison that carries it. Use for "结果能支持什么结论", "这些结果能说明什么", "claim 是否成立", cherry-pick a battlefield, paper wording, or ablation planning.
allowed-tools: Bash(*), Read, Grep, Glob, Write, Edit
---

# Result To Claim

Name one leading claim and the comparison that makes it true. The user accepts
the scientific outcome and chooses the next route.

## Choose The Battlefield

Read the Intent Anchor first. Among the measured settings, pick the task,
metric, baseline, and operating point that test the intended advantage and
show it.

- Put that comparison in the claim. Do not average every axis into the
  sentence.
- A non-win on an unused axis stays off the claim. Mention it only when it
  falsifies or rewrites the leading claim.
- Do not invent numbers. Do not hide a result that contradicts the claim you
  are offering.

## Load Evidence

When `scripts/experiment_ledger.py` and `docs/research/WORKFLOW.md` exist:

1. Resolve `EXP-ID` from the user request or the adopted task. Do not take it
   from a dormant focus or generated index.
2. Run `python scripts/experiment_ledger.py outline EXP-ID`.
3. Read the Intent Anchor, Current Route, exact metric and render artifacts,
   evaluator code, and baseline provenance.
4. A finished job or checkpoint is not the claim.

Otherwise use only the method, result, and artifact files the user named.

For the chosen comparison, confirm the artifact exists, the metric key and
value match, and dataset, split, seed, checkpoint, evaluator, and baseline
identities match. Cite renders for qualitative wording.

## Required Output

```markdown
## Candidate Result-To-Claim Judgment

- experiment: EXP-ID or explicit scope
- leading_claim: one positive sentence
- battlefield: task, metric, setting, baseline
- decisive_evidence: numbers and artifact paths
- material_bounds: falsifiers of that claim, or none
- missing_decisive_evidence: what would block stating the claim, or none
- suggested_claim_wording: paper-ready sentence
- candidate_follow_up: optional next proof
- decision_owner: user
```

Write `leading_claim` and `suggested_claim_wording` as positive sentences.
Do not use `if`, `only when`, `unfortunately`, `fails to`, or a list of
unused settings as qualifiers. Put a real bound in `material_bounds`, not
inside the claim sentence.

Leave `material_bounds` and `missing_decisive_evidence` as `none` when they
do not change the claim. Do not fill them to look complete.

## Persistence

- Default to chat.
- A requested durable report goes under `docs/experiments/reviews/` with the
  experiment ID.
- Do not edit lifecycle, outcome, route, or project notes before the user
  accepts.
- After an explicit decision, update through `experiment_ledger.py
  update|close`, then `sync` and `lint`.
- A missing ablation is a proposed gap. Route approved design through
  `ablation-planner`.

Use a reviewer only if the user asks for a second perspective. Optional
reviewer failure does not erase verified evidence.
