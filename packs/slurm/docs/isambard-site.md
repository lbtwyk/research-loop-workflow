# Isambard Site Overlay

Use this only on Isambard-AI. Other Slurm sites should replace it.

| Term | Meaning |
|---|---|
| `workq` | Ordinary training/batch queue; no interactive reservation |
| `--reservation=interactive` | Short-lived preflight, debugging and exploratory work; 1.5x NHR, up to 4 nodes / 8h |
| `interactive` partition | Hidden partition selected automatically by the reservation |
| `interactive_qos` | Partition QoS enforcing reservation limits; inspect live values |

For new reservation allocations, set only `--reservation=interactive`;
do not specify `--partition` or override `--qos`. Slurm selects the hidden
partition and its limits. Long-running or high-throughput formal workloads
belong in ordinary `workq`, not this reservation.

Use `squeue --all`, `sinfo --all` and `scontrol show partition --all` to
include hidden resources. With `PrivateData` enabled, other users' accounts
and jobs may be invisible; an empty peer query is not evidence of no usage.

Do not infer reservation access from `Accounts=root`, a missing partition in
the default view, or the absence of `interactive_qos` in association QoS.
Use a bounded, correctly routed probe under the current project account.
On 2026-10-14, job 7413875 using `brics.u6ym` and reservation alone entered
partition `interactive`, saw a GH200 and completed with exit 0 despite
`Accounts=root` being displayed. This proves that account's access at that
time, not another user's entitlement or a future allocation.

Set `RESEARCH_LOOP_SLURM_RESERVATION=interactive` unless the site overlay
changes the pool name. Immediate preflight commands require an explicit
`--immediate=N` spanning the scheduler cycle; allocation failure and program
failure are different outcomes.

## Cost And Allocation

Use actual `AllocTRES`/billing and the site's node-hour conversion, not requested
CPUs or an assumed GPU-hour price. A single-GPU request may allocate a complete
Grace CPU domain even with a smaller `--cpus-per-task`; reducing that request
alone need not reduce billing. Job-level `--exclusive` reserves/bills the whole
node and is not the same as isolated `srun --exclusive` steps. Include the 1.5x
interactive premium in short-work comparisons; it is not a formal-training
acceleration option. Project budget and permitted concurrency remain separate
constraints, never inferred from idle nodes or association visibility.

Official policy and commands:
[Slurm advanced](https://docs.isambard.ac.uk/user-documentation/guides/slurm-advanced/#interactive-reservation-isambard-ai-phase-2).
[Accounting](https://docs.isambard.ac.uk/user-documentation/guides/accounting/).
