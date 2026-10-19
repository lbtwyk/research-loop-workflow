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
- On Isambard a new `interactive` reservation allocation must not specify
  `--partition` or override `--qos`; Slurm selects the hidden partition.
  Inspect it with `squeue --all`, `sinfo --all`, and
  `scontrol show partition --all`. Verify access with a bounded probe, not
  `Accounts=root` alone.
- An unavailable immediate GPU is `skipped_unavailable` and must never enter
  the queue. A started GPU program failure is real and blocks submission.
- Receipts bind the exact command, scope, review basis, and definition.

Ledger commands `preflight`, `launch`, and `launch-packet --slurm-snapshot`
load `scripts/slurm_state_snapshot.py` and `scripts/training_preflight.py`.
For an unsettled shape, `launch-packet --resource-candidates FILE` also loads
`slurm_resource_policy.py`: lowest billed cost within 10% of the fastest
comparable feasible time to result. This read-only calculation is not a GPU
preflight, budget authorization, or permission to change running jobs. Observe
allocation and execution-step usage separately; unknown usage is not zero.

A receipt's top-level `passed` can mean the submission gate permits a
resource-unavailable skip. Report each CPU/GPU check's actual execution status;
do not call `skipped_unavailable` an executed proof. Invalid account,
reservation, partition or QoS is a configuration failure, not a resource skip.
