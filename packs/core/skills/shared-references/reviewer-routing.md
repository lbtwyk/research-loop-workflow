# Reviewer Routing

Shared research skills ask for one independent read-only reviewer. How that
reviewer is spawned is defined by the installed agent adapter.

- Cursor and Codex each supply their reviewer command in the matching adapter.

Do not hard-code a model or reasoning effort in a shared skill. One
independent reviewer only, and only when the user explicitly requests a second
perspective or the formal launch gate requires it.

If the reviewer cannot run: emit `BLOCKED` / `REVIEW_UNAVAILABLE`. Never
substitute the executor's own judgment for an independent pass.

Record same-family review as a second perspective, not cross-family
independence:

```yaml
review_independence: same-family
acceptance_status: provisional
```

Give the reviewer exact frozen artifact paths and a bounded question. Keep it
read-only for source.
