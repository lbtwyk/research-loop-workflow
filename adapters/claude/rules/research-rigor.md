# Research Rigor For Claude

Claude brings ideas and reasoning; this file keeps the science correct. It adds
to `AGENTS.md` for Claude Code only. For scientific checks it overrides the
HERO Scope Limits: a check for leakage, population mismatch, a wrong number, a
wrong checkpoint or a run that never happened always names a concrete failure,
so it is always in scope. HERO still governs code hardening, security, hashes
and style.

None of this is an approval step. Run the checks inline as part of the work;
most take one short script or one file read.

## Think Wide First

For a non-trivial question (a surprising result, a design choice, a failure,
a new method idea), widen before you narrow:

- Write down at least two competing explanations or designs, and always
  include the boring one: a bug, a leak, the wrong file, a metric artefact.
- Look from every angle that applies:
  - data: split, overlap, preprocessing, which items are in the population;
  - model and training: initialization, checkpoint, schedule, seeds;
  - evaluation: does the metric measure the claim, where do GT and chance sit,
    windowing and length;
  - causality: what else changed, confounders, the simplest alternative;
  - operations: did it actually run, on which inputs and code;
  - literature: what is known, how similar ideas failed.
- Name the observation that separates the candidates, then check the cheapest
  decisive one.

Creativity is welcome at this stage. Do not prune ideas because they are
unusual; prune them because an observation rules them out.

## Hypothesis Versus Fact

An idea stays a hypothesis until evidence exists, and is written as one. When
a hypothesis becomes an experiment, its spec records three lines next to the
Intent Anchor: the prediction, the result that would refute it, and the
strongest alternative explanation.

## Rigor Checks

Before a result-based conclusion goes to the user, into a paper, or under a
new launch, check the items that apply. Each one is a real error this workflow
has already made.

1. **Same population.** Compared numbers come from the same items, windows,
   lengths, filtering and evaluator.
2. **Unseen means unseen.** Held-out items share nothing that matters with
   training: the same song or music, performance, subject or source copy, not
   only a different file name.
3. **Numbers reproduced.** Every reported number is re-read from its evidence
   file by script in this session, not copied from memory or an earlier
   message. Facts recalled from memory (citations, APIs, published results)
   are checked against a primary source.
4. **Identity.** The checkpoint, weights, data version and code commit are the
   ones the claim names.
5. **It really ran.** Jobs, triggers and downstream steps have exit codes and
   outputs; a scheduled or submitted step is not a result.
6. **Sanity anchors.** GT and chance sit where expected (GT at least as good as
   generated, mismatched pairs near chance) before a new metric or scorer is
   trusted.
7. **Alternative ruled out.** The leading explanation beat the competitor from
   Think Wide First on a direct observation, not on plausibility.

In chat, mention a check only when it failed, changed the conclusion, or could
not be done; an unchecked point is stated as unchecked, never dropped. When an
experiment's conclusion is written, record the applicable checks in its spec.
See also the `experiment-integrity.md` shared reference installed with the
research skills.

## Independent Codex Check

Codex is the strict second reader. The project requires it at two points, as
the quality gate allowed by the subagent policy. Spawn the `reviewer` agent
with a bounded question and the exact frozen artifact paths:

- **Idea to experiment.** Before the first launch of a new experiment whose
  hypothesis Claude proposed: can this design refute the hypothesis, and is
  there leakage, a confounder or a population mismatch? This is a design review
  of the spec and contract; code review still follows the AGENTS.md rule.
- **Claim to paper or outcome.** Before a new number or claim enters the paper,
  or before an experiment outcome is proposed to the user for acceptance: give
  the claim text and raw evidence paths; Codex recomputes and checks scope.

Routine launches, reruns, monitoring, repairs, ablations of an accepted design
and ordinary chat answers do not need Codex. Fix its findings yourself; its
verdict is input, not acceptance. If it cannot run, say `REVIEW_UNAVAILABLE`
and do not substitute your own judgment.
