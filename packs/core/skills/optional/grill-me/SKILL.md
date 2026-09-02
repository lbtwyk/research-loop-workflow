---
name: grill-me
description: Stress-test a plan in frontier rounds while updating its spec after each round. Use when the user asks to be grilled, wants a design challenged, requests batch grilling, or needs a plan reconciled with project docs, terminology, code, or recorded decisions.
---

Interview the user relentlessly until you reach a shared understanding. Map this as a **design tree**: every decision branches into the decisions that hang off it.

Work the tree in **rounds**. The **frontier** is every decision whose prerequisites are already settled — the questions you can ask now without guessing at answers you have not heard yet. Ask the whole frontier in one numbered round, give a recommended answer for each, and wait for the user's answers before the next round. Recompute the frontier after every round; a question that depends on another question still open in the current round belongs to a later round.

Batch rounds are the default. If the user or repository instructions explicitly request one question at a time, honor that override without changing the live-spec contract.

Finding facts is your job, never the user's. If a fact can be found by exploring the environment, codebase, documentation, experiment artifacts, tools, or external sources, look it up rather than asking the user. The decisions are the user's: put each decision to them with your recommendation and wait for their answer.

During codebase exploration, also discover the repository's actual documentation structure before assuming names. Look for docs that constrain the plan: glossary or domain-language docs, architecture notes, decision records, design docs, experiment specs, README-style project guidance, and repo-specific agent instructions. Common names like `CONTEXT.md`, `CONTEXT-MAP.md`, or `docs/adr/` are examples only; prefer whatever naming and location the current project already uses. Treat docs as evidence about the project's language and prior decisions, not as decorative background.

## Live Spec Contract

Before the first question, identify the applicable existing spec from the
repository's conventions and the user's request. Prefer the active or explicitly
named spec. If several files are genuinely plausible, ask the user which one to
edit. If no spec exists and the project has a clear convention, create the
minimal spec there; otherwise use `SPEC.md` in the project root.

Treat that spec as the live source of truth throughout the interview:

1. Establish a baseline from the user's plan and verified repository facts.
2. Ask the complete current frontier as one numbered round, with a recommended
   answer for each decision.
3. After the user answers, update the spec immediately before computing the next
   frontier.
4. Write only confirmed decisions as settled requirements. Keep unresolved or
   partially answered matters under `Open Questions` instead of guessing.
5. Revise the canonical section when an answer changes an earlier decision;
   preserve dated history only when the project's spec convention requires it.
6. Briefly state what changed in the spec, then continue with the next question.

Do not postpone spec writing until the interview ends. Spec edits are the one
project mutation allowed during grilling. Do not implement code, change runtime
configuration, launch jobs, or modify unrelated artifacts unless the user gives
a separate explicit instruction.

The session is done only when every reachable branch of the design tree has
been visited, the spec reflects all confirmed decisions, and no decision remains
silently assumed.

## Experiment Ledger Adapter

When the repository contains `docs/research/WORKFLOW.md`, keep the method above
unchanged and route its live spec through the canonical experiment workflow:

- resolve an explicitly named experiment with
  `scripts/experiment_ledger.py outline EXP-ID`;
- use that experiment's `EXP-*.md` as the live spec for a route or contract
  decision, or the existing `docs/research/modules/` blueprint for a purely
  architectural design decision;
- inspect code, contracts, artifacts, and recorded decisions before asking, and
  batch only genuine unresolved decisions;
- never create a parallel tracker or change lifecycle, outcome, route, launch,
  or scientific acceptance without the user's explicit answer.

## Documentation-Aware Grilling

- Challenge against existing language. If the user uses a term that conflicts with the project's glossary, methodology, terminology, or other domain-language docs, call it out immediately and ask which meaning should win.
- Sharpen fuzzy or overloaded terms. Propose a precise canonical term when the user says something ambiguous, especially when nearby docs or code distinguish concepts with similar names.
- Test domain boundaries with concrete scenarios. Invent edge cases that force the user to decide where one concept, workflow, owner, or responsibility ends and another begins.
- Cross-reference claims with code and docs. If the user says the system behaves one way but code or docs show another, surface the contradiction directly and ask which source of truth should change.
- Capture each resolved term and decision in the live spec immediately. Treat
  existing glossaries and ADRs as evidence during grilling, but do not edit them
  during the interview unless the user explicitly expands the requested output.
- Keep the spec canonical rather than appending a chat transcript. Integrate
  answers into the relevant goals, contract, architecture, evaluation, risks,
  non-goals, or open-question section.
