# Asynchronous Research Transport

This document contains only the transport rules that differ from the canonical
[research workflow](WORKFLOW.md). Async execution does not own experiment
state, scientific routes, contracts, evaluation requirements, or conclusions.

```text
approved GitHub issue
  -> isolated issue worktree
  -> normal experiment spec and contract
  -> independent implementation or Slurm work
  -> contract-declared evidence
  -> GitHub handoff
  -> user scientific decision
```

## Authorization And Human Boundary

An issue authored by an allowed user and labelled `researchos:ready` authorizes
only the route explicitly described in that issue. The worker may implement and
test it, request a reviewed launch, repair one demonstrated same-contract
operational failure, complete declared stages, and report evidence.

The worker must not invent or rank hypotheses, choose a successor route, change
the scientific contract, accept or reject a result, merge a branch, or start
from an ordinary discussion comment. Use `researchos:waiting-web` whenever a
scientific choice is required.

## Isolation

Each issue owns one branch and worktree:

```text
branch:   researchos/issue-N
worktree: <configured-worktree-root>/issue-N
```

Tracked changes stay in that worktree. Run names, outputs, logs, checkpoints,
evaluation roots, render roots, and mutable caches must be issue-specific. The
branch starts from the configured `prior-dev` base, is pushed for review, and is
never auto-merged.

Parallel routes are allowed only when neither depends on the other's evidence,
checkpoint, selected code, or decision and they share no mutable artifact. A
shared sibling `.tmp` next to a durable cohort or manifest is a mutable
collision, even when final leaf outputs are route-disjoint. A separate issue
or worktree does not by itself justify a new experiment spec.

## Existing Jobs And New Submissions

Existing queued and running jobs are immutable inputs. The controller never
cancels, reprioritizes, requeues, edits, attaches a step to, or adds a dependency
on them.

New jobs use unique issue namespaces, controller-owned `Nice=10000`, one durable
submission intent, and one receipt. Ambiguous submission is reconciled before
retry. The worker writes a schema-valid launch request; the controller performs
the submission after the normal ledger review and contract checks. A new or
changed training identity runs the same real-path preflight; an unchanged
identity reuses its receipt. An unavailable immediate GPU canary is recorded as
skipped and never becomes a queued job.

## Stage Closure And Handoff

`stage_closure.declared` comes from the frozen contract, issue request, and
launcher DAG. Every declared stage is partitioned into `completed` or
`remaining`. A cycle is complete only when nothing remains and every declared
stage has an existing evidence path. Training closes only its own row. An
undeclared render, evaluation, or other stage is not invented by the transport.

The worker writes the GitHub handoff under its ignored issue runtime path. The
controller posts it, and the next cycle records the returned URL in the normal
experiment spec. GitHub labels describe transport only:

- `researchos:ready`: approved work may start or resume;
- `researchos:running`: implementation, execution, or evaluation is active;
- `researchos:waiting-web`: evidence is ready and a user decision is required;
- `researchos:done`: the issue-requested work and handoff are complete;
- `researchos:blocked`: technical reconciliation needs manual attention.

The entrypoint is `scripts/run_github_research.py`; the issue template is
`.github/ISSUE_TEMPLATE/async-research.yml`.
