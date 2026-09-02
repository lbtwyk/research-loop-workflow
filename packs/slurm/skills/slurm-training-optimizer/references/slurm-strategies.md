# Slurm Strategy Reference

## Decision Table

| Situation | Prefer | Do not use when |
|---|---|---|
| GPU preflight on Isambard | `--reservation=interactive` plus `--immediate` | Never omit the bounded deadline |
| Current user already has a running reservation job | Join uncommitted resources already in its fixed `AllocTRES` with `srun --jobid=JOB_ID --exact --exclusive --ntasks=1` | Owner, `Reservation=interactive`, running state, allocated shape, or remaining walltime is not verified |
| Authorized formal workload that fits 8h / 4 nodes | Reservation allocation with packed exclusive steps; accept 1.5× NHR | The scheduler rejects the shape or time, or ordinary `workq` would finish sooner after queue wait |
| Long authorized formal workload on the reservation | Background `sbatch --reservation=interactive` | The run must fail immediately rather than queue, or needs more than 8 hours |
| Exact-resume training with a useful short interval | `--time` maximum, `--time-min` useful minimum, pre-timeout signal | Resume is approximate, incomplete, or a shortened run is useless |
| Low SM% / unused HBM on an independent same-contract process | Same-effective-batch CUDA MPS on one GPU | Host RSS * n exceeds `--mem-per-gpu`, JAX MPS is excluded, or the pair has no canary |
| Many independent short one-GPU tasks | One multi-GPU allocation with concurrent exclusive steps | Mutable state overlaps or one step failure cannot be surfaced |
| Matched comparison still untrained, user approved | Raise `batch_size` on every compared route/seed together | A running trajectory, or one side of an already-trained control |
| Eligible tasks exceed live per-user backfill test cap | Pack tasks or submit bounded waves | The cap is unverified or dependencies require the full graph |
| Partition default over-requests host memory per GPU | Measured `--mem-per-gpu` with headroom | Evidence shows the lower request can OOM |
| Multi-GPU work naturally occupies a node | Full-node allocation | Work uses only a fraction of the requested GPUs |

## Live Diagnosis

Read scheduler facts with:

```bash
squeue -u "$USER" -o '%.18i %.9P %.28j %.8T %.10M %.10l %.6D %R'
scontrol show config | rg 'SchedulerType|SchedulerParameters|Priority|Preempt'
sdiag
sinfo -Nel
scontrol show partition workq
scontrol show qos
scontrol show reservation interactive
sacctmgr -nP show qos format=Name,Priority,MaxJobsPU,MaxSubmitJobsPU,MaxTRES,MaxWall,UsageFactor,Flags
```

Important fields:

- `bf_max_job_user`: maximum jobs from one user tested in a backfill cycle.
- `bf_max_job_test`: total jobs tested in one backfill cycle.
- `default_queue_depth`: main-scheduler examination limit.
- `bf_max_time`: backfill-cycle time budget.
- priority weights and `PreemptMode`: whether age, fair share, size, QOS, or
  preemption can materially change ordering.
- `Reason=None` with stale `LastSchedEval`: possible evidence that a job was not
  recently examined, not evidence of an imminent start.

Treat these values as live observations. On 2026-08-11, Isambard exposed
`bf_max_job_user=25`, but the skill must recheck it every time.

## Interactive GPU Preflight

All executable Isambard preflight layers use Slurm. This includes real-data,
formal-worker, optimizer-step, checkpoint/resume, and downstream-hook CPU
proof. Only lightweight static imports may run directly on a login node. A
direct-attached GPU may use the declared local mode.

### Prevent false unavailable results

An immediate probe still enters Slurm's pending state while the scheduler
examines it. `queued and waiting for resources` is therefore an intermediate
message, not an outcome. Do not cancel on that message and do not report
`skipped_unavailable` until the bounded `srun` process exits.

Before probing, read `sched_min_interval` from `SchedulerParameters`. Convert
its microseconds to seconds and set an explicit integer timeout satisfying
`N >= max(5, ceil(sched_min_interval_seconds) + 2)`. Never use bare
`--immediate` or `--immediate=1`: a deadline shorter than one scheduler cycle
can report unavailable even when the same allocation starts seconds later.

Probe the exact reservation and requested GPU count. A different partition,
reservation, or resource shape answers a different question. Classify only the
final result:

| Final evidence | Classification |
|---|---|
| Exit 0 after allocation and canary completion | `passed` |
| Compliant deadline expires with an explicit immediate-allocation-unavailable message, before the program starts | `skipped_unavailable` |
| Temporary queued text while `srun` is still alive | wait; no classification yet |
| Too-short or implicit deadline, or scheduler defers examination | `inconclusive`; fix the command and retry once |
| Invalid reservation, account, QOS, option, or resource specification | configuration failure |
| Canary starts and then CUDA, dependency, OOM, non-finite, checkpoint, or trainer code fails | real preflight failure |

Record the exact command, timeout, job ID when emitted, return code, and final
stdout/stderr. At most one corrected retry is allowed; do not turn probing into
polling.

Use a bounded exact canary:

```bash
srun \
  --reservation=interactive \
  --immediate=5 \
  --ntasks=1 \
  --gpus=1 \
  --cpus-per-task=8 \
  --mem-per-gpu=48G \
  --time=00:10:00 \
  python TRAINER_OR_PREFLIGHT --gpu-preflight
```

The command returns early on completion. Only its final result, interpreted by
the table above, determines availability. Once the program begins, CUDA,
dependency, OOM, non-finite, checkpoint, or trainer failures are real.
Keep `--ntasks=1`: on Isambard a one-GPU allocation can expose a full CPU
domain, and an unconstrained `srun` step may otherwise start one copy per CPU
group.

When a verified reservation allocation already exists, avoid a second
reservation or `interactive_qos` job and run CPU and GPU checks as isolated
steps:

```bash
srun --jobid="$M2D_INTERACTIVE_JOB_ID" \
  --exact --exclusive --ntasks=1 \
  --gpus=1 --cpus-per-task=8 \
  --chdir=/ABSOLUTE/WORKTREE \
  python TRAINER_OR_PREFLIGHT --preflight
```

Before joining, `scontrol show job -dd JOB_ID` must show the current user,
`JobState=RUNNING`, and `Reservation=interactive`. Inspect active steps and the
allocation shape to confirm the requested resources are free. Do not combine
`--jobid` with `--reservation` or `--immediate`.

Official BriCS docs: the `interactive` **reservation** is a dedicated node
pool billed at **1.5 NHR per node-hour**, max 4 nodes and 8 hours, official
per-user cap 1 running + 1 queued, not for large-volume batch. Faster start
is that pool, not a higher multifactor priority. `interactive_qos` is a
separate one-allocation QoS on the same pool; `workq`+`normal` plus
`--reservation=interactive` still pays 1.5×. Recheck live limits. Canonical
term table: `docs/research/modules/TRAINING_EFFICIENCY.md`.

- https://docs.isambard.ac.uk/user-documentation/guides/slurm-advanced/
- https://docs.isambard.ac.uk/user-documentation/information/job-scheduling/
- https://docs.isambard.ac.uk/user-documentation/guides/accounting/

## Aggressive Formal Reservation Run

Reservation transport and scientific formality are separate. A completed
command may retain formal status when it uses the exact reviewed contract,
ledger identity, inputs, checkpoint semantics, outputs, and downstream gates.
The project owner has confirmed formal-workload authorization and the 1.5×
reservation rate. Treat `--reservation=interactive` as the first-choice
execution transport when it shortens time to the requested result and fits
the 8-hour / 4-node / official per-user job cap.

Eligibility checklist:

1. Run the normal CPU and GPU preflight first.
2. Read the live enforced job, GPU/node, concurrency, and walltime limits before
   allocation; size the route to what Slurm will accept.
3. Use `srun --reservation=interactive --immediate=N` for a single command or
   acquire one allocation and fill it with concurrent `srun --exclusive` steps.
   Run further waves in the same allocation instead of leaving GPUs idle.
4. Preserve the exact formal command identity. Record reservation, QoS, job ID,
   allocation shape, 1.5× billing note, logs, artifacts, and receipt.
5. Compare expected time to useful evidence with ordinary `workq` without a
   reservation. Prefer the reservation when immediate execution wins after the
   premium.
6. Inspect live `interactive_qos` and reservation job caps. `MaxJobsPU=1` or
   an official 1-running-job reservation table limits **allocations**. It does
   not serialize job steps, experiments, or worktrees inside one allocation.
   Two session-owned `srun` jobs both showing `Reservation=interactive` are not
   a policy change.

This path may cover complete training runs, experiment matrices, evaluations,
profiles, and cache builds that fit the reservation. There is no extra
project-side job-count cap beyond scientific usefulness, the 1.5× rate, and
Slurm/BriCS live limits. Preserve disjoint mutable state, capture every step
exit status, release the allocation at completion, and use ordinary `workq`
when the reservation cannot accept the shape or walltime.

### Cross-worktree ownership

Treat the reservation job as a shared allocation while it is running. Its
owner launches formal workloads as `srun --exact --exclusive` steps instead of
consuming the whole allocation with one unscoped command. Another worktree
first discovers the active job and its uncommitted `AllocTRES`, then joins it with
`--jobid`. Every step uses an absolute `--chdir`, separate mutable paths,
explicit logs, and a visible exit status.

Allocation capacity is fixed at submission. A one-GPU allocation cannot launch
a four-GPU step even when three GPUs are idle on its node; those GPUs belong to
neither that job nor its dispatcher. Conversely, GPUs already allocated to the
owner are charged while idle, so request the planned packed shape and release it
when its useful waves finish.

Do not add a global filesystem lock that says the reservation is occupied. A step
may be blocked only when the active allocation lacks its requested resources or
remaining walltime. If the step fits the fixed allocation but resources are
busy, use a later wave. If it exceeds the fixed allocation, use `workq` or wait
to open a correctly sized allocation.

For worktrees added after submission, start the allocation with
`scripts/slurm_interactive_allocation_owner.sh`. Enqueue the reviewed command
through `scripts/interactive_allocation_dispatcher.py enqueue`; the allocation
owner launches and waits for the exact exclusive step, so Codex or SSH may
disconnect. The dispatcher rejects jobs not started with this owner and requests
larger than the owner's fixed GPU allocation; it cannot retrofit another
running batch job. Use `stop --job-id JOB_ID` after the final request. The owner
exits automatically after its bounded idle timeout.

## Background Reservation Long Run

Use Slurm-owned background execution for a long formal run so closing Codex or
SSH cannot kill its controller. Submit one reviewed allocation-owner script
with `sbatch`, not a shell-backgrounded or session-owned `srun`. The owner
launches initial workloads as exact exclusive steps so unused resources remain
joinable:

```bash
job_id=$(sbatch --parsable \
  --reservation=interactive \
  --gpus=4 \
  --cpus-per-task=48 \
  --mem-per-gpu=48G \
  --time=08:00:00 \
  --output=/ABSOLUTE/LOG_ROOT/formal_%j.out \
  --error=/ABSOLUTE/LOG_ROOT/formal_%j.err \
  FORMAL_SCRIPT)
```

Do not pass `--wait`; return the job ID, log paths, and follow command
immediately. A packed script may launch concurrent `srun --exclusive` steps and
must wait for all of them and propagate any failure.

Check `sbatch --help` before assuming it supports `--immediate`. The Isambard
client observed on 2026-08-11 did not. When strict immediate evidence matters,
first run an exact-shape and exact-walltime `srun --immediate=N ... /bin/true`,
then submit the background job. The allocation can change between those two
commands, so the canary is evidence rather than a hold on those nodes. Keep any
older ordinary `workq` copy until the reservation batch job reaches `RUNNING`;
then cancel the duplicate only when authorized. Confirm durable ownership with
`BatchFlag=1` in
`scontrol show job -dd JOB_ID`.

## Checkpointable Backfill

```bash
#SBATCH --time=14:00:00
#SBATCH --time-min=01:00:00
#SBATCH --signal=B:USR1@300
```

The minimum must cover startup, useful work, atomic checkpoint persistence, and
cleanup. The signal handler must save all contract-required optimizer, scaler,
RNG, sampler, and progress state. Record the allocated time limit from the live
job because backfill may grant less than the requested maximum.

Official option semantics:

- https://slurm.schedmd.com/sbatch.html

## Same-Effective-Batch MPS

Prefer this before a larger `batch_size` or another GPU. Independent PyTorch
processes keep their frozen batch, seed, and paths and share one GPU through
NVIDIA CUDA MPS. Host RSS, not HBM, is usually the limiter.

```bash
mps_pipe=/tmp/m2d-mps-${SLURM_JOB_ID}-${SLURM_RESTART_COUNT:-0}
export CUDA_MPS_PIPE_DIRECTORY=${mps_pipe}
export CUDA_MPS_LOG_DIRECTORY=${mps_log}
mkdir -p "${mps_pipe}" "${mps_log}"
nvidia-cuda-mps-control -d
trap 'echo quit | nvidia-cuda-mps-control; rm -rf "${mps_pipe}"' EXIT
```

Launch the packed commands as ordinary processes against that daemon, wait for
every PID, and propagate any failure. Prove the exact pair with a canary
before a formal launch. The repository example is the one-GPU path in
`scripts/submit_omg_clean_dc.py`.

## Packed Steps

Inside an allocation sized for all steps:

```bash
pids=()
srun --exclusive --ntasks=1 --gpus=1 command_a & pids+=("$!")
srun --exclusive --ntasks=1 --gpus=1 command_b & pids+=("$!")
srun --exclusive --ntasks=1 --gpus=1 command_c & pids+=("$!")
srun --exclusive --ntasks=1 --gpus=1 command_d & pids+=("$!")
status=0
for pid in "${pids[@]}"; do wait "$pid" || status=1; done
exit "$status"
```

Assign disjoint run names, caches, logs, outputs, and checkpoints. Packing
reduces scheduler objects and may keep work inside per-user examination caps;
it does not increase priority.

## Resource Shape

- On Isambard, verify the effective request with `scontrol show job -dd`; a
  job-level `--mem` may not express the desired per-GPU host-memory shape under
  partition defaults, while `--mem-per-gpu` does.
- Set CPUs from the actual trainer processes, loader workers, and threading
  configuration. Do not add workers to chase low SM% when AveCPU is already
  about one core per process.
- Set walltime close to observed need plus justified headroom; inflated
  walltime reduces backfill opportunities.
- Use `--exclusive` only when consuming the corresponding node resources.

## Prohibited Shortcuts

Do not recommend or perform unauthorized QOS/reservation use, account spoofing,
priority manipulation, false limits, queue flooding, or dependency chains whose
purpose is only to occupy future queue position. Pre-submitted chains can
sustain utilization after the first job starts, but are not evidence of a
faster legitimate first start and can worsen scheduler load.

Official scheduler references:

- https://slurm.schedmd.com/slurm.conf.html
- https://slurm.schedmd.com/high_throughput.html
