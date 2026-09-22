# Lifecycle And Review

## Intent And Routes

The Intent Anchor contains goal, reason, must-remain-true constraints, and
completion evidence, not transient jobs or route details. Material change
normally creates a new experiment; wording-only correction records its reason.

For a superseded route retain identifier, compact design, motivation, decisive
measurements/failures, artifact paths, replacement reason, and successor.
Condense duplication, not evidence or provenance.

## Lifecycle

Lifecycle is operational phase; outcome is scientific meaning. A failed attempt
may remain evidence in an active experiment. Closed experiments retain explicit
accepted, rejected, inconclusive, or superseded meaning.

## Review

On Cursor, spawn the reviewer as in [cursor-subagents.md](cursor-subagents.md). The
child receives the frozen contract, complete scientific review paths,
required identity records, required tests, data/evaluation contract, launcher
scope, and Intent Anchor. It returns PASS, UNCERTAIN, or BLOCKED with
evidence. The implementer cannot issue an independent pass.

Review is used for materially changed scientific semantics or a
demonstrated high-risk execution change. A first launch, new experiment ID, or
routine ablation does not normally trigger review when reviewed data, model,
trainer, evaluator, and runtime semantics are reused.

Review effort is ordered by impact: first core scientific logic and contract
fidelity, then live material hot-path/resource risks, then only the provenance
identities needed for interpretation or exact resume. Resource review is useful
when the requested shape changed or evidence indicates OOM, input wait,
throughput, or ETA risk.
Estimates and same-hardware history are sufficient; missing or ambiguous
details are recorded as `UNCERTAIN` and do not by themselves block launch.
Only demonstrated OOM, impossible hard walltime, deadlock/input starvation,
or another material operational failure blocks on efficiency grounds.
Generic defensive programming, security hardening, and style are non-blocking
unless a concrete consequence reaches correctness, memory, resume, throughput,
or scientific interpretation. SHA256 is therefore required only for
contract-scoped identity bindings (for example parent/codec/cache/resume/
evaluation inputs), not as a blanket requirement for every file or artifact.

After BLOCKED, proof findings may be closed by the main agent with changed paths
and focused tests. Reviewer-judgment findings use one delta review. Changed
scientific semantics or contract require full review. Operational-only repairs
need focused validation, not another scientific review.

Use the selected compute module to launch the frozen command and check runtime
proof. Record the contract, reviewed scientific source when review was required,
exact command, and runtime paths in the experiment.

Always distinguish planned, tested, submitted, allocated, running, completed;
scheduler evidence from model-quality evidence; and clean provenance from
degraded/non-promotable provenance.
