# Slurm Strategy Reference

## Decision Table

These are candidates, not a fixed preference order. Apply the installed
`TRAINING_EFFICIENCY.md` policy: among comparable feasible shapes within 10% of
the fastest time to all remaining results, select the lowest billed cost.
Respect existing budget, concurrency and deadline limits before comparison.

| Situation | Prefer | Do not use when |
|---|---|---|
| GPU preflight on Isambard | `--reservation=interactive` plus `--immediate` | Never omit the bounded deadline |
| Current user already has a running reservation job | Join uncommitted resources already in its fixed `AllocTRES` with `srun --jobid=JOB_ID --exact --exclusive --ntasks=1` | Owner, `Reservation=interactive`, running state, allocated shape, or remaining walltime is not verified |
| Long-running or high-throughput formal workload | Ordinary `workq` without the interactive reservation | Do not move it to the short-lived pool |
| Exact-resume training with a useful short interval | `--time` maximum, `--time-min` useful minimum, pre-timeout signal | Resume is approximate, incomplete, or a shortened run is useless |
| Independent compute process leaves usable GPU capacity | Matched same-effective-batch MPS candidate | Combined host/HBM/shared memory does not fit, real-time/no-MPS contract, or no useful measured gain |
| Many independent short one-GPU tasks | One multi-GPU allocation with concurrent exclusive steps | Mutable state overlaps or one step failure cannot be surfaced |
| Matched comparison still untrained, user approved | Raise `batch_size` on every compared route/seed together | A running trajectory, or one side of an already-trained control |
| Eligible tasks exceed live per-user backfill test cap | Pack tasks or submit bounded waves | The cap is unverified or dependencies require the full graph |
| Partition default over-requests host memory per GPU | Measured `--mem-per-gpu` with headroom | Evidence shows the lower request can OOM |
| Multi-GPU work naturally occupies a node | Full-node allocation | Work uses only a fraction of the requested GPUs |

## Live Diagnosis

`slurm_state_snapshot.py` uses `squeue --all --array` and one `sacct` query
including execution steps. Keep allocation records separate from step usage;
do not use `sacct -X` for MaxRSS/CPU/GPU utilization. Unknown is not zero and a
failed step query cannot prove unused allocation capacity. Estimate billed cost
from actual AllocTRES and site rules, not smaller requested CPU counts. Use
eligible-to-start history for queue estimates, not dependency wait as runnable
queue delay. Snapshot start/end times describe an interval, not atomic state.

Read scheduler facts with:

```bash
squeue --all -u "$USER" -o '%.18i %.9P %.28j %.8T %.10M %.10l %.6D %R'
scontrol show config | rg 'SchedulerType|SchedulerParameters|Priority|Preempt|PrivateData'
sdiag
sinfo --all -Nel
scontrol show partition --all
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

### Reservation routing and visibility

On Isambard specify `--reservation=interactive` without `--partition`
or a QoS override. Slurm selects its hidden partition and limits.
Default queue/partition views omit hidden resources; always use `--all`.
`PrivateData` may hide peer jobs/accounts, so no visible peer usage is not
proof that peers cannot use the pool. Do not treat `Accounts=root` alone
as denial: on 2026-10-14, account `brics.u6ym` completed GPU probe 7413875
in partition `interactive` despite that display. A bounded probe using
the current account and correct routing decides access.

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

Official BriCS policy: the `interactive` reservation is for short-lived
preflight, debugging and exploratory work, billed at 1.5x NHR, with up to
4 nodes and 8 hours. Inspect live partition QoS and per-user allocation caps.
The maximum walltime does not authorize long-running or high-throughput
training. Such work uses ordinary `workq` without the reservation.
Project authorization cannot override the site policy.

- https://docs.isambard.ac.uk/user-documentation/guides/slurm-advanced/
- https://docs.isambard.ac.uk/user-documentation/information/job-scheduling/
- https://docs.isambard.ac.uk/user-documentation/guides/accounting/

## Short Preflight Allocation Reuse

Reuse only the current user's verified running reservation allocation with
uncommitted resources inside its fixed `AllocTRES`. Use exact exclusive
steps with separate mutable paths and visible exit status. A one-GPU
allocation cannot claim other idle GPUs on the node. Release resources when
the short-lived work ends; do not hold the pool for recurring training waves.

For durable long-running batch work, use Slurm-owned background `sbatch`
in ordinary `workq` without `--reservation=interactive`, return job/log
identifiers immediately, and inspect later. Do not replace reservation-only
routing with `workq` plus the reservation even if a probe happens to start.

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

Consider this for independent underfilled compute workloads. Compare aggregate
useful throughput, per-task slowdown, billed cost, host/shared memory and HBM.
Neither unused HBM nor busy % proves a speedup. Preserve frozen batch, seed,
paths and exact resume. Do not use MPS for frozen no-MPS or real-time control
work. A larger batch remains a separate authorized scientific change.

```bash
mps_pipe=/tmp/m2d-mps-${SLURM_JOB_ID}-${SLURM_RESTART_COUNT:-0}
mps_log=/tmp/m2d-mps-log-${SLURM_JOB_ID}-${SLURM_RESTART_COUNT:-0}
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

- Choose on the remaining critical-path horizon, including evaluation/render
  stages. Reconsider only at useful task/stage/checkpoint boundaries or material
  resource facts. Include startup, checkpoint, restart, retries and requeue
  costs. Apply changes to future submissions, not running frozen jobs.

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
