# Claude Code adapter

`./install.sh --dest PROJECT --slurm --agent claude` writes:

- `PROJECT/CLAUDE.md` (`@AGENTS.md` and `@.claude/rules/research-rigor.md`) so
  Claude Code loads the project rules; it reads `CLAUDE.md`, not `AGENTS.md`.
  An existing file is kept and only gets the rigor import line appended once.
- `PROJECT/.claude/rules/research-rigor.md`: Claude-only research rigor. Think
  wide before narrowing, keep ideas as hypotheses until tested, seven
  scientific checks drawn from real past errors, and a Codex check at two
  points (idea to experiment, claim to paper or outcome). Codex does not read
  it, so Codex behaviour is unchanged.
- `PROJECT/.claude/skills/` the pack skills plus the overlays in
  `skills-overlays/`, which route review to the `reviewer` agent.
- `PROJECT/.claude/agents/reviewer.md` a forwarder that runs the review on Codex
  (`gpt-6-astra`, medium) through `codex exec`. It needs a logged-in Codex CLI.
  `codex-local` is used when installed, otherwise `codex` with a read-only sandbox.
  Output goes to `$CODEX_REVIEW_DIR` (default `~/.cache/codex-review`).
- With `--slurm`: `.claude/hooks/experiment_guard.py` and a `PreToolUse` hook in
  `.claude/settings.json` that denies direct training launches matching a
  registered contract; use `experiment_ledger.py launch`. An existing
  `settings.json` is kept; add the hook from `adapters/claude/.claude/settings.json`
  by hand.

`--personal --agent claude` installs the skills and the agent under `~/.claude`.
