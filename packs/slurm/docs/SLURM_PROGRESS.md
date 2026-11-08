# Slurm progress

After installing the Slurm pack, run from the project root:

```bash
python3 scripts/slurm_progress.py                  # all live jobs for this user
python3 scripts/slurm_progress.py 123456           # one job; accounting fallback
python3 scripts/slurm_progress.py 123456_0         # one array task
python3 scripts/slurm_progress.py 123456 --json    # source receipts and log tails
python3 scripts/slurm_progress.py --history --since now-2days
```

This is a read-only, one-shot inspection. It needs Python's standard library
and Slurm clients, not CUDA, PyTorch, an allocation, or an SSH service. Do not
submit a job just to inspect progress. It neither resumes nor cancels work.

The default query includes hidden partitions (`--all`) and expands arrays
(`--array`). Each row keeps its own job identity. Queue state takes precedence
over accounting. Jobs no longer in the queue fall back to `sacct`; use an
earlier `--since YYYY-MM-DD` for old jobs. Scheduler failures and unresolved IDs
produce a partial report and exit code 1, not an empty successful queue.

Log paths come from scheduler metadata (`scontrol`, then accounting for old
jobs), not directory guesses. Relative paths resolve against the recorded
working directory; accounting `%j`, `%A`, and `%a` templates use numeric job
and array identities. Unsupported substitutions remain unknown. Both stdout
and stderr are inspected, with shell-quoted follow commands. Missing files are
reported explicitly. Pending jobs do not reuse old log progress.

Each log read is limited to its last 128 KiB and at most `--tail-lines` complete
lines (default 80). Supported training records are JSON lines with integer
`step` and `total` (or `total_steps`). The latest valid record supplies progress,
its optional `stage`, and an optional finite `training_eta_hours`. Other log
formats remain unknown; their last line and full bounded tails in `--json`
still help diagnosis. No percentage or ETA is invented from elapsed walltime.

The displayed percentage is relative to the **trainer-reported budget**. In
resumed or warmup jobs this can be a cumulative full-training budget, not this
allocation's stopping target. ETA is a log-reported training estimate, not a
queue-start estimate, current job/stage ETA, or a new live prediction. Log age
is the file's modification age, not proof that optimization is advancing.

Slurm `COMPLETED` closes scheduler execution only. This command does not load
checkpoints, validate metrics, or mark evaluation, rendering, delivery, or
scientific acceptance complete. Use the experiment ledger and the training
check workflow for those boundaries. For placement and launch resource choices,
continue using `slurm_state_snapshot.py` and `TRAINING_EFFICIENCY.md`.
