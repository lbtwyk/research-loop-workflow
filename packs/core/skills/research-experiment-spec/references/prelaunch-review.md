# Pre-Launch Review For Expensive Execution

Read this reference only when an expensive execution family or its hot path
materially changed.

## Static Packet

- Trace the real training hot path and identify expensive calls, serial loops,
  repeated feature/decode/FK work, host-device transfers, and input stalls.
- Derive representative tensor and activation shapes. Estimate model,
  optimizer, activation, and cache memory with explicit headroom.
- Reuse same-hardware measurements when available. Select a semantics-safe
  batch, microbatch, precision, caching, prefetch, and parallel configuration.
- Record projected throughput or completion bounds, checkpoint cadence,
  exact-resume headroom, and assumptions the formal job must verify.
- Right-size dependent evaluation and rendering separately from training.

## Reviewer Priority

This is a research-correctness review with an important compute-efficiency
self-check, not a generic security or defensive-programming audit. Review in
this order and keep the first two categories as the main effort:

1. **Core scientific logic and contract fidelity.** Check the objective, causal
   information boundary, targets and losses, parameter ownership and freeze
   rules, gradient/update/rollout semantics, data split and cache meaning,
   baseline/control separation, evaluator identity, and exact-resume state
   (optimizer, scheduler, EMA, RNG, sampler, and checkpoint cadence).
2. **Material compute and resource risks (required review subsection).** Inspect
   the actual hot path on the target hardware: tensor/activation shapes,
   repeated decode/FK or feature work, serial Python/CPU sections, host-device
   transfers, input stalls, synchronization, memory headroom/OOM risk,
   checkpoint/eval overhead, utilization, throughput, and ETA. Use measured
   evidence when available and code-backed estimates when it is not.
3. **Scoped provenance and identity.** Verify only the identities needed to
   interpret the run or resume it exactly. A SHA256 is required when the frozen
   contract uses it to bind a parent checkpoint, codec, cache, resume state, or
   evaluation/comparison input; it is not required for every source file or
   output artifact.
4. **Generic hardening and style.** Defensive validation, error-message polish,
   security threat modeling, and speculative micro-optimizations are normally
   non-blocking. Do not let them displace the core-logic or hot-path review.

## Decision Boundary

Block launch when code or measurements demonstrate a material correctness,
memory, resume, or operational risk. An efficiency estimate that is merely
uncertain is advisory; repair a demonstrated bottleneck by
batching, vectorizing, caching, prefetching, or changing operational resources
without changing the scientific objective, optimizer-update semantics,
randomness contract, checkpoint cadence, or exact-resume behavior.

Do not block on speculative micro-optimizations or require proof that every
possible optimization has been implemented. Record those as follow-up notes.
Do not submit a separate queued profile job. `sbatch --test-only` validates
scheduler shape, not runtime efficiency; the formal job supplies runtime
confirmation.

After review closure and before queue submission, run the repository's
mandatory training preflight against the exact launch command. Its CPU layer
must execute real data/worker, optimizer-step, checkpoint-resume, and first
downstream-hook paths. A GPU canary may use only a non-queueing immediate Slurm
allocation; explicit resource unavailability is a recorded skip, while a
started GPU program failure blocks launch.

The efficiency self-check should contain a compact numeric table with one row
for each resource and workload field: requested value, measured or code-backed
need, headroom, evidence path, and PASS/UNCERTAIN/BLOCKED result. Include
partition, reservation (`none` or `interactive`), QoS, billing rate (1.0×
ordinary `workq` vs 1.5× reservation NHR), GPU count, CPU count, host memory,
walltime, batch/window shape, workers, prefetch, precision, peak GPU/host
memory, utilization, data-wait fraction, throughput, and projected ETA. Do not
collapse reservation, partition, and QoS into the word `interactive`. A
machine-readable `resource_contract` is useful when it makes the request
reproducible, but its absence does not block a launch.
When available, persist this table through
`experiment_ledger.py record-review --resource-review-file`; `uncertain` rows
are allowed in an overall `PASS`, while `blocked` is reserved for demonstrated
OOM, impossible hard walltime, deadlock/input starvation, or another material
operational failure. Do not submit a separate profile job solely to measure
efficiency; the formal job supplies the confirmation.

## Finding And Output Contract

Return one overall `PASS` or `BLOCKED` decision, with an advisory `UNCERTAIN`
efficiency subsection when estimates are incomplete. Put blocking findings first,
grouped under core correctness, scientific semantics/resume, and
efficiency/memory/throughput. A finding is blocking only when exact evidence
shows a material risk to correctness, scientific interpretation, resume
integrity, memory, or throughput. Put generic defensive/security/style items
and speculative improvements in a separate non-blocking section. Every finding
must include exact `path:line` evidence, consequence, and the smallest fix or
measurement needed to close it. End with the launch recommendation and the
evidence that was actually checked.
