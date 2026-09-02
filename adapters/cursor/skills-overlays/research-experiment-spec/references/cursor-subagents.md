# Cursor Subagents For This Skill

Cursor does not read `agents/openai.yaml` or Grok `spawn_subagent`. Use the
`research-reviewer` subagent at `~/.cursor/agents/research-reviewer.md`.

## Scientific / prelaunch review

Use one independent reviewer. Do not review your own launch packet.

1. Write a packet file under `$TMPDIR/cursor-$(id -u)/` (mode 0700) containing
   the experiment id, contract paths, `experiment_ledger.py outline` output,
   changed scientific files, and the resource request.
2. Call the `research-reviewer` subagent:
   - Keep it read-only for source
   - Give it the packet path, the required review-file path, and
     [prelaunch-review.md](prelaunch-review.md)
3. Wait for completion. If the review file is missing, treat as failed review.
4. Record the verdict through the ledger. Only the user accepts a scientific
   outcome.

Code review of ordinary diffs is `/review`, not this path.

## Code exploration

Do not spawn an explore subagent for ordinary implementation or a file you
already have. Keep synthesis in the main agent unless the user explicitly
requests a second perspective.
