---
name: "novelty-check"
description: "Verify research idea novelty against recent literature. Use when user says \"\u67e5\u65b0\", \"novelty check\", \"\u6709\u6ca1\u6709\u4eba\u505a\u8fc7\", \"check novelty\", or wants to verify a research idea is novel before implementing."
---

# Novelty Check Skill

Check whether a proposed method/idea has already been done in the literature: **$ARGUMENTS**

## Canonical Experiment Adapter

When the repository contains `docs/research/WORKFLOW.md` and the request names
an `EXP-ID`, run `scripts/experiment_ledger.py outline <EXP-ID>` and read its
Intent Anchor, intended claim, Current Route, and novelty-relevant method docs.
Novelty analysis may inform the spec or paper workspace, but it must not change
experiment lifecycle, outcome, route, or launch state. Default to a chat report;
write a durable report only when the user requests one and place it under
`docs/research/` or `docs/paper/`, not in a root-level tracker.

## Instructions

Given a method description, systematically verify its novelty:

### Phase A: Extract Key Claims
1. Read the user's method description
2. Identify 3-5 core technical claims that would need to be novel:
   - What is the method?
   - What problem does it solve?
   - What is the mechanism?
   - What makes it different from obvious baselines?

### Phase B: Multi-Source Literature Search
For EACH core claim, search using ALL available sources:

1. **Web Search** (via `WebSearch`):
   - Search arXiv, Google Scholar, Semantic Scholar
   - Use specific technical terms from the claim
   - Try at least 3 different query formulations per claim
   - Include year filters for 2024-2026

2. **Known paper databases**: Check against:
   - ICLR 2025/2026, NeurIPS 2025, ICML 2025/2026
   - Recent arXiv preprints (2025-2026)

3. **Read abstracts**: For each potentially overlapping paper, WebFetch its abstract and related work section

### Phase C: Adversarial Verification
Challenge the novelty assessment locally by trying to disprove each claimed delta,
searching synonyms, precursor mechanisms, and adjacent application domains. Spawn a
fresh reviewer only when the user explicitly asks for a second opinion or subagent
review. Treat same-family review as an additional perspective, not independent proof.

### Phase D: Novelty Report
Output a structured report:

```markdown
## Novelty Check Report

### Proposed Method
[1-2 sentence description]

### Core Claims
1. [Claim 1] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
2. [Claim 2] — Novelty: HIGH/MEDIUM/LOW — Closest: [paper]
...

### Closest Prior Work
| Paper | Year | Venue | Overlap | Key Difference |
|-------|------|-------|---------|----------------|

### Overall Novelty Assessment
- Score: X/10
- Recommendation: PROCEED / PROCEED WITH CAUTION / ABANDON
- Key differentiator: [what makes this unique, if anything]
- Risk: [what a reviewer would cite as prior work]
- Decision owner: user

### Suggested Positioning
[How to frame the contribution to maximize novelty perception]
```

### Important Rules
- Be BRUTALLY honest — false novelty claims waste months of research time
- "Applying X to Y" is NOT novel unless the application reveals surprising insights
- Check both the method AND the experimental setting for novelty
- If the method is not novel but the FINDING would be, say so explicitly
- Always check the most recent 6 months of arXiv — the field moves fast
- A recommendation is decision input, not authorization to implement, abandon,
  launch, or change an experiment route

## Review Tracing

If an optional reviewer is used, save its trace following `../shared-references/review-tracing.md`. Otherwise, report the search queries, closest papers, and final novelty decision directly.
