# Cursor Reviewer Routing

- executor: current Cursor main agent
- reviewer: the `research-reviewer` subagent
- do not hard-code a model or reasoning effort inside a skill
- one independent reviewer only
- do not use Codex `spawn_agent` or Grok `spawn_subagent`

Ordinary code diffs use `/review`, not this scientific reviewer.
