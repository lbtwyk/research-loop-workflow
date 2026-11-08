# Reviewer Independence Protocol

## Core Principle

The reviewer must judge primary artifacts directly. The executor can define the review role, scope, and file list, but must not pre-digest the content into a preferred narrative.

## What Can Be Passed

- reviewer role or persona
- review objective
- absolute file paths
- structural metadata such as section count or venue
- concrete output schema

## What Must Not Be Passed

- executor summaries of file contents
- executor interpretations of results
- executor recommendations about what the reviewer should conclude
- "what changed since last round" narratives unless the skill explicitly requires diff-focused follow-up
- leading or coaching questions

## Correct Pattern

```text
Review the project as a senior ML reviewer.

Files to read directly:
- /path/to/docs/experiments/EXP-ID.md
- /path/to/docs/experiments/contracts/EXP-ID.json
- /path/to/runtime/EXP-ID/eval/summary.json
- /path/to/src/
```

## Incorrect Pattern

```text
The main contribution is a new loss function that improves by 15%.
I think the weak point is the ablation.
Please confirm this is publishable.
```

## Multi-Round Follow-Up

When a review needs a follow-up round, pass revised artifacts or a targeted
question, not the executor's spin on what changed.

## Applies To

Every reviewer call made by a shared research skill, whatever adapter spawns
it (see `reviewer-routing.md`).
