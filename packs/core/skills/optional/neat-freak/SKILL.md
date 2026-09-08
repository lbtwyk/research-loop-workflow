---
name: neat-freak
description: Reconcile documentation affected by a change or milestone with code. Use for requested doc sync, tidy, stale-doc repair, or handoff cleanup; inspect the whole repository only when the user requests a whole-repository audit.
---

# Neat-Freak

Keep the documentation affected by the user's task accurate and useful for
its readers. A request to review or recommend changes is read-only.

## Scope And Evidence

Start from the requested change, relevant diff, and named documents. Read
project guidance and inspect directly affected documentation and its direct
consumers. Follow links where they can reveal a real inconsistency; do not
enumerate or read every document, memory file, or project by default.

For an explicit whole-repository cleanup, enumerate the requested repository's
documentation and assess it against current evidence. Do not automatically
expand into other repositories or historical cleanup.

## Update

When editing is authorized, update the existing canonical sections. Use project
agent guidance for conventions, and user-facing docs for usage and operation;
do not duplicate every fact across both. Keep scientific history, negative
evidence, and provenance. Remove obsolete guidance only when current evidence
establishes that it is obsolete.

Use the experiment ledger for its owned state and generated views. Do not create
a second tracker. Update global instructions only when the user explicitly
requests the cross-project policy change.

Memory writes require an explicit user request and must use the platform's
authorized memory-update mechanism. A doc-sync request is not memory-write
authorization. Do not rewrite protected memory files.

Resolve routine factual inconsistencies from code and recorded decisions.
Ask only for a material unresolved choice, conflicting user intent, or missing
authority. Continue independent authorized work while that decision is pending.
Report unrelated historical findings separately instead of silently fixing them.

## Completion

Check the changed statements, commands, paths, and direct consumers that could
be affected. Stop when these are aligned; expand verification only for new
changes, failures, or concrete unresolved evidence. No full-library checklist
or relative-date word purge is required.

Report the changed files and any material unresolved item. If no update is
needed, say so; do not manufacture edits to satisfy the skill.

Use references/sync-matrix.md only when identifying a relevant document
consumer is unclear; it supplies examples, not mandatory edits or extra scope.
