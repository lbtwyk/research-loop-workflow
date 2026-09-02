# Research workflow

- Root `AGENTS.md` and `docs/research/WORKFLOW.md` are the project
  instructions. Do not create a parallel tracker.
- Resolve formal work from the current user request, then run
  `python scripts/experiment_ledger.py outline <EXP-ID>`.
- `docs/experiments/registry.json` owns lifecycle and outcome. One spec owns
  the question, routes, evidence, and conclusion. The contract JSON owns
  frozen executable semantics.
- Use `ACTIVE.md` only to find a missing experiment. Use `INDEX.md` only for
  history. Never hand-edit generated views.
- Keep implementation, scheduler state, runtime proof, and scientific
  acceptance separate. A finished scheduler job is not acceptance.
- First expensive launch or a changed scientific contract needs one
  independent read-only review. Same-contract operational repairs use focused
  validation.
- Launch training through the ledger. Direct `train_*` / `torchrun` of a
  guarded contract is blocked.
- After checks, update through `experiment_ledger.py update|close|sync|lint`.
