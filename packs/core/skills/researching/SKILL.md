---
name: researching
description: Research papers, official docs, and implementations to solve a technical question with cited evidence. Use for research, related work, method comparison, or cross-domain mechanism search.
---

# Researching

Turn a local blocker into a mechanism question and return options that can
change an implementation or decision, not a generic literature list.

## Workflow

1. Inspect enough local code/spec/evidence to state the observable failure,
   controllable intervention, invariants, and acceptance test.
2. Search the same domain, the underlying mechanism, and adjacent domains that
   solve the same mechanism under different names.
3. Prefer papers, official documentation, official repositories, and artifact
   backed reproductions.
4. Compare serious candidates by mechanism, assumptions, evidence, released
   code, local fit, incompatibilities, compute, and smallest informative test.
5. Verify consequential details against paper text and released code. Label
   mappings verified, inferred, unavailable, or ambiguous.
6. Translate the best ideas into minimal local interventions, matched controls,
   expected signatures, and falsification tests.
7. Report observations, synthesis, recommendation, uncertainty, and decisions
   still owned by the user.

Read [research method](references/research-method.md) for search matrices, claim
tracing, artifact archiving, and output detail. Use pdf-to-markdown only when
complete text matters, paper-reading-coach for guided reading, and
paper-deep-dive for implementation-grade reconstruction.

Keep research synthesis in the main agent. Do not spawn an explore
subagent for files you already have, or for ordinary implementation.

## Guardrails

Browse when facts, software, or recommendations may have changed. Cite exact
primary sources. Do not equate popularity or stars with fit. Do not broaden an
experiment, replace frozen controls, choose acceptance, or launch an unapproved
route. Separate published evidence, code behavior, local observation, and
inference.
