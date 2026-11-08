# Review Tracing

Keep what a reviewer saw and said, so a surprising verdict can be explained
from the record instead of by asking again.

## What To Keep

For every reviewer call that critiques, scores, verifies a claim, audits an
experiment or gates a patch:

- the full prompt (bounded question plus artifact paths);
- the full response, verbatim;
- reviewer route: model, reasoning effort, `same-family` or `cross-family`;
- exit status, or `REVIEW_UNAVAILABLE`.

The installed adapter decides where these land (the Claude `reviewer` agent
writes `review.md` and `review.err` under `$CODEX_REVIEW_DIR`). Record that
path in the experiment spec next to the decision it informed. Purely
informational agent calls are not traced.

## Using A Trace

When a verdict surprises you, or two reviews disagree, read the saved
response first and find the paragraph where the judgement turned. That
paragraph is the explanation; cite it. Re-running the reviewer without reading
the trace gets a new opinion, not an explanation.

Traces are project-local runtime records; do not commit them.
