# Slurm Training

Use this module when Slurm schedules the work. The core workflow owns the
experiment and scientific decision; this module owns queue facts, launch proof,
job recovery, and stage execution.

1. Read the project's site overlay for partitions, reservations, limits, and
   storage. Do not apply another site's settings.
2. Use `slurm_state_snapshot.py` for current queue facts and the ledger's
   `launch-packet` to inspect declared stages before submission.
3. For training, run or reuse the exact-command preflight described in
   [PREFLIGHT.md](PREFLIGHT.md). Submit through the ledger's `launch` command.
4. Track the real job state, log, checkpoint, and downstream stages. Recover
   demonstrated same-contract failures; keep scheduler completion separate
   from experiment acceptance.

[TRAINING_EFFICIENCY.md](TRAINING_EFFICIENCY.md) covers resource choices.
The core `training-check-acceptance` skill owns the automatic operational loop;
this module supplies its Slurm status, preflight, launch, and recovery details.
