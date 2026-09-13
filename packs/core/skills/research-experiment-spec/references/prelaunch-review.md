# Pre-Launch Review For Expensive Execution

Read this reference only when scientific semantics materially changed or
evidence shows a high-risk execution change. A first launch, new experiment ID,
or routine ablation does not normally trigger review when reviewed data, model,
trainer, evaluator, and runtime semantics are reused.

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
2. **Material compute and resource risks (only when live).** Inspect
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

On a direct-attached GPU, do not require a separate general preflight. Run
focused checks for changed seams, then use the formal job's early real-data,
optimizer, memory, throughput, and checkpoint evidence. Test checkpoint/resume
or downstream hooks separately when those paths changed, failed, or present a
concrete live risk.

Do not require a numeric resource table for a settled local GPU shape. When
resource shape changed or evidence indicates OOM, input starvation, throughput,
or ETA risk, record only the measurements and estimates that can change the
launch. Do not run a separate profile solely to complete review paperwork.

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
