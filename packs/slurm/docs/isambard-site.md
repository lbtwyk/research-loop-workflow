# Isambard Site Overlay

Use this only on Isambard-AI. Other Slurm sites should replace it.

| Term | Meaning |
|---|---|
| `workq` | Ordinary queue, 1.0× NHR, up to 24h |
| `--reservation=interactive` | Reserved node pool, 1.5× NHR, official 1-job cap, 8h |
| `interactive_qos` | Separate one-allocation QoS on that reserved pool |

Do not say `interactive` alone. Reservation jobs bill at 1.5× NHR even when
they also use `workq` and `normal`. A per-user cap is an allocation limit, not
a worktree or training-task limit.

Set `RESEARCH_LOOP_SLURM_RESERVATION=interactive` unless the site overlay
changes the pool name.

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
