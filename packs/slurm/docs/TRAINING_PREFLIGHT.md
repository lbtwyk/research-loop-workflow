# Slurm Training Preflight

This is the scheduler implementation of the
[PREFLIGHT.md](PREFLIGHT.md) interface.

- CPU and GPU checks run through Slurm, not a login node.
- Target-cluster GPU proof uses `gpu_check.mode=slurm_interactive`. Legacy
  `local` mode proves only a direct GPU, not Slurm execution.
- `slurm_interactive` must use `srun --ntasks=1` and either
  `--jobid` with `--exact --exclusive`, or
  `--reservation=$RESEARCH_LOOP_SLURM_RESERVATION` (default `interactive`)
  plus an explicit `--immediate` timeout.
- An unavailable immediate GPU is `skipped_unavailable` and must never enter
  the queue. A started GPU program failure is real and blocks submission.
- Receipts bind the exact command, scope, review basis, and definition.

Ledger commands `preflight`, `launch`, and `launch-packet --slurm-snapshot`
load `scripts/slurm_state_snapshot.py` and `scripts/training_preflight.py`.
