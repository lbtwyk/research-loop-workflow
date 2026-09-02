---
name: handoff
description: Write or update project-root HANDOFF.md for fresh-context continuation. Use for a handoff, next-agent summary, or saving progress for another conversation.
---

# Handoff

Create or update `HANDOFF.md` in the current project root so another agent can resume without reading the full conversation.

## Workflow

1. Check whether `HANDOFF.md` already exists in the project root.
2. If it exists, read it first and preserve still-relevant context.
3. Inspect the current local state as needed: recent files changed, relevant commands/logs, blockers, and any user-stated goals.
4. Write a concise Markdown handoff with these sections:
   - `Goal`: what the work is trying to accomplish.
   - `Current Progress`: what has already been done and where.
   - `What Worked`: successful commands, approaches, paths, or decisions.
   - `What Didn't Work`: failed attempts, errors, or dead ends to avoid repeating.
   - `Next Steps`: clear action items for the next agent.
5. Save the document as `HANDOFF.md` in the project root.
6. Tell the user the absolute file path and that they can start a fresh conversation with that path.

## Writing Rules

- Ground the handoff in verified local state, not guesses.
- Include exact paths, branch/worktree names, command names, job IDs, or log files when they matter.
- Keep it useful for continuation: prefer durable facts and active blockers over chat history.
- Do not include secrets, auth tokens, private cookies, or raw credentials.
- If the handoff replaces stale content, remove or rewrite the stale parts instead of appending contradictory notes.
