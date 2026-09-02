---
name: github-research-handoff
description: Send evidence-backed research handoffs through GitHub and sync the experiment ledger. Use for Web collaboration, issue decisions, or result handoff.
---

# GitHub Research Handoff

Turn verified local experiment evidence into a durable GitHub handoff. Keep
observations, interpretation, and requested decisions distinct.

## Workflow

1. Resolve the repository, target issue or PR, and explicit experiment ID from
   the request. Run `scripts/experiment_ledger.py outline <EXP-ID>`, then read
   the relevant spec sections and contract. Use `ACTIVE.md` only when the
   experiment identity is missing or changing and `INDEX.md` only for history
   or baseline lookup. If the user says "latest issue", inspect open issues
   before selecting a target.
2. If an allowed human has already approved a runnable route, do not post
   another comment asking whether to launch it. Execute or resume through the
   normal experiment workflow and hand off only completed evidence, a
   demonstrated failure, or a concrete scientific decision.
3. Re-check scheduler exit states, checkpoint/log paths, metric JSON, eval
   completeness, render manifests, and the exact baselines used. Do not write
   from memory alone.
4. Write a concise English handoff unless the user requests another language.
   Lead with factual status. Separate observed evidence from interpretation and
   recommended choices. Read
   [references/comment-template.md](references/comment-template.md) when a
   result comparison or decision request needs a structured comment.
5. Publish according to the execution mode:
   - **Interactive:** post through GitHub MCP (`GetDynamicTools` then
     `CallDynamicTool`) or `gh`. Re-fetch the target, capture the final URL, update the experiment through
     the ledger, stage only scoped source/docs/tests, and push when authorized.
   - **Async worker:** write the handoff Markdown under the ignored issue runtime
     path and return `github_comment_path`. The deterministic controller posts
     the comment and pushes the clean issue branch. Do not post or push directly.
6. After a confirmed GitHub URL is available, record it in the focused spec
   through the ledger. Do not hand-edit generated ACTIVE or INDEX views.

## Authority And Quality Bar

- Async evidence handoff does not authorize accepting/rejecting a route,
  selecting the next hypothesis, merging a branch, or closing the issue.
- Do not treat sample renders as full evaluation or hide missing/partial gates.
- Include repository-relative artifact paths and a compact comparison table when
  the decision depends on metrics.
- Give concrete decision options only after supplying the evidence needed to
  distinguish them.
- Keep runtime artifacts out of Git. Keep the published handoff and pushed
  source state consistent; if publication is intentionally deferred, say so.
