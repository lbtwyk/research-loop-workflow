---
name: github-research-handoff
description: Sync research outputs to GitHub; update issues or PR discussion for stage results or decisions.
---

# GitHub Research Handoff

Sync finished code, documents, and useful evidence to the repository as they
become ready so Web can read them. A repository push needs no issue/PR comment
or Web decision. Update issue/PR discussion for a stage result or a decision
that is actually needed. Keep observations and interpretation distinct.

## Workflow

1. Resolve the repository, target issue or PR, and explicit experiment ID from
   the request. Run `scripts/experiment_ledger.py outline <EXP-ID>`, then read
   the relevant spec sections and contract. Use `ACTIVE.md` only when the
   experiment identity is missing or changing and `INDEX.md` only for history
   or baseline lookup. If the user says "latest issue", inspect open issues
   before selecting a target.
2. If an allowed human has already approved a runnable route, execute or resume
   it. Sync scoped code, docs, and useful evidence when ready; reserve discussion
   updates for stage results or concrete scientific decisions.
3. Re-check scheduler exit states, checkpoint/log paths, metric JSON, eval
   completeness, render manifests, and the exact baselines used. Do not write
   from memory alone.
4. Write a concise English handoff unless the user requests another language.
   Lead with factual status. Separate observed evidence from interpretation and
   recommended choices. Read
   [references/comment-template.md](references/comment-template.md) when a
   result comparison or decision request needs a structured comment.
5. Push scoped code/docs/evidence when ready. For a stage result, post through
   GitHub MCP or `gh`, then capture the final URL.
6. After a confirmed GitHub URL is available, record it in the focused spec
   through the ledger. Do not hand-edit generated ACTIVE or INDEX views.

## Authority And Quality Bar

- A handoff does not authorize accepting/rejecting a route, selecting the next
  hypothesis, merging a branch, or closing the issue.
- Do not treat sample renders as full evaluation or hide missing/partial gates.
- Include repository-relative artifact paths and a compact comparison table when
  the decision depends on metrics.
- Give concrete decision options only after supplying the evidence needed to
  distinguish them.
- Keep runtime artifacts out of Git. Keep the published handoff and pushed
  source state consistent; if publication is intentionally deferred, say so.
