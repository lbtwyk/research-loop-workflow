# Research Loop Guidelines

This pack is the agent-neutral research operating system. A consuming project
adds its own data, models, and site overlay. The user accepts scientific
outcomes. Agents implement approved routes, repair demonstrated same-contract
failures, evaluate, audit, and report evidence.

## Agent Execution And Communication

Before asking the user clarifying questions, you should complete the work that is already authorized from context and necessary to make the proposed action concrete and reviewable. The user should be approving a concrete, reviewable result. For example, before deploying a change, writing to an external application, merging a PR or publishing a site, do all the required work first so that user approval is the final step. You don't need user permission for reversible tasks, read-only actions, reviews or fixes, or anything for which authorization is provided earlier in the session or strongly implied from the task instruction.
Do not introduce unsolicited warnings, disclaimers, approval flows, or safety/compliance checklists due to hypothetical risk.

- Infer the requested outcome, not only the literal steps. Use listed steps as
  guidance and fill routine gaps needed for the outcome. Consider callers, data
  flow, verification, downstream artifacts, analysis, and reporting in
  proportion to the task.
- Check the user's premise against evidence and correct material omissions.
  Keep a working definition of done, reassess it as evidence arrives, and report
  material completed results without waiting for a second prompt.
- Never report a task, subagent, training run, deployment, or external action as
  created, started, running, or completed without a successful tool result or
  inspectable runtime evidence. Distinguish prepared commands and submitted
  work from live execution. For an App-native task action, use the corresponding
  App thread tool when exposed; do not silently replace a missing native tool
  with CLI or direct app-server calls.

## Research Workflow

- [docs/research/WORKFLOW.md](docs/research/WORKFLOW.md) is the human-facing
  workflow. After install it lives at `docs/research/WORKFLOW.md`.
- `docs/experiments/registry.json` owns compact lifecycle and outcome state.
  One experiment spec owns the scientific question, route history, evidence,
  and conclusion. Its contract owns frozen executable semantics.
- Resolve formal work from the current user request, then run
  `python scripts/experiment_ledger.py outline <EXP-ID>`. A private worktree
  focus is only a ledger default. Use generated `ACTIVE.md` only to find a
  missing experiment and `INDEX.md` only for history.
- Create a new experiment only for a new falsifiable claim, causal
  intervention, or a materially changed frozen data, representation, training,
  or evaluation contract. Keep bug fixes, recovery, refactors, replications,
  and same-claim revisions as routes or runs in the parent.
- Keep implementation, scheduler state, runtime proof, and scientific
  acceptance separate. Training completion closes only its declared stage.
- The user chooses scientific routes and conclusions. Agents do not accept
  results, choose a successor route, or auto-merge.
- Organize research around one leading advantage and the claim it can support.
- Give each proposed experiment one proof role: establish the method, explain
  the source of the advantage, demonstrate value in the target scenario, or
  eliminate a plausible alternative explanation.
- Lead summaries with problem, gap, method, decisive evidence, and supported
  conclusion.
- Update lifecycle through `scripts/experiment_ledger.py`. Never hand-edit
  generated ACTIVE or INDEX views.

## Review And Launch

- Independent read-only review is used when a change materially alters
  scientific semantics or creates a demonstrated high-risk execution change.
  A first launch, new experiment ID, or routine ablation does not normally
  trigger review when it reuses reviewed data, model, trainer, evaluator, and
  runtime semantics. The implementer cannot issue a required independent pass.
- Review core scientific and contract fidelity first, material resource fit
  second, scoped provenance third, and generic hardening last. Missing
  efficiency precision is `UNCERTAIN`, not a launch veto.
- Reviewers must not request hashes or fingerprints for ordinary source,
  logs, metrics, or renders. Git commit plus dirty paths is enough.
- Use the installed compute module for launch, preflight, status, and recovery.
  Record the exact execution identity and evidence in the experiment ledger.
- A request to check approved training authorizes the full operational loop:
  monitor, repair, resume, finish declared stages, evaluate, and report formal
  results. Continue automatically unless a scientific decision or an
  unrepairable external blocker is reached.

## HERO Scope Limits

Adapted from
[`wanshuiyin/HERO-Anti-OverDefense`](https://github.com/wanshuiyin/HERO-Anti-OverDefense)
at commit `95bac7f1df4b60acb90a91306b199e430220c125` (MIT).

Report anything that is actually wrong. Then keep the fix in scope:

1. This is not a security paper. Verification is welcome; over-defense is not.
   Assume a cooperating operator on their own machine unless the project
   states a real adversary.
2. Do not add hashes unless the hash replaces a materially more expensive
   operation and its result changes what happens next.
3. No defensive scaffolding for cases that do not occur here.
4. No corner-case obsession unless the case is reachable through this
   project's supported use.
5. Where judgement is needed, judge. Do not replace it with a scoring table.

Before running any check, answer: what specific failure would this detect,
and what would I do differently if it occurred? No answer means do not run it.
Say plainly when something is correct. Do not manufacture findings.

## Code And Git

- Match surrounding code and CLI idioms.
- Catch only exceptions that can be handled at I/O, scheduler, persistence,
  cleanup, or top-level process seams.
- Test observable behavior at the real seam.
- Keep commits scoped. Never commit runtime artifacts.
