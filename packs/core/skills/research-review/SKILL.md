---
name: research-review
description: Get a fresh-context second opinion on research. Use only when the user explicitly asks for "第二视角", "子代理复核", "模拟审稿", "independent review", or an external-style adversarial review.
---

# Research Review

Provide a read-only second perspective. This skill is not the ordinary local
analysis path and does not own experiment state, route selection, or scientific
acceptance.

## Context

When the request concerns a canonical experiment:

1. Resolve the explicit `EXP-ID` and run
   `scripts/experiment_ledger.py outline <EXP-ID>`.
2. Load the Intent Anchor, relevant route, exact evidence, Current Conclusion,
   and the user's review question.
3. For a formal expensive-launch review, use the packet and decision contract
   defined by `research-experiment-spec`; do not substitute this general mock
   review for that gate.

For a paper, architecture, or idea review without an experiment, use only the
explicit narrative, claim, method, and evidence files named by the task.

## Reviewer Route

- Spawn a reviewer only because the user explicitly requested this skill or the
  formal workflow requires its configured read-only reviewer.
- Spawn the reviewer through the installed agent adapter. Do not hard-code a
  model or reasoning effort in this shared skill.
- Send exact frozen artifacts and a bounded question. The reviewer must be
  read-only and must not edit files, launch work, choose a route, or accept a
  conclusion.
- Record same-family review as a second perspective, not cross-family
  independence.

## Review Priorities

Ask the reviewer to assess, in order relevant to the request:

1. scientific logic, causal information, objective, controls, and claim scope;
2. evidence provenance, evaluator identity, missing comparisons, and
   contradictory results;
3. material implementation or resource implications when execution is in
   scope;
4. narrative, novelty positioning, and the smallest decisive follow-up.

Require exact file/artifact evidence and separate demonstrated defects from
uncertainty or optional improvements.

## Reconciliation

The main agent compares the review with verified local evidence, answers factual
errors, and returns:

- findings that stand;
- findings rejected with evidence;
- unresolved uncertainty;
- candidate claim or experiment changes requiring user decision.

Do not iterate until superficial consensus. Stop when the user's bounded review
question is answered or further progress needs new evidence.

## Persistence

- Default to a concise chat result.
- If the user requests a durable canonical-experiment review, store it under
  `docs/experiments/reviews/` with the experiment ID.
- Paper-only reviews belong in the paper workspace chosen by the user.
- Do not write a root-level review file, update project memory, edit lifecycle,
  or choose the next route automatically.

Retain reviewer traces following `../shared-references/review-tracing.md` when a
reviewer is used.
