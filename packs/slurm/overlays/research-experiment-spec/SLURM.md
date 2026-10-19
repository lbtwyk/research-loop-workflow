# Slurm Overlay For Research Experiment Spec

When the slurm pack is installed, compile stage closure with a scheduler
snapshot:

```bash
python scripts/slurm_state_snapshot.py --output /tmp/research-loop-slurm.json
python scripts/experiment_ledger.py launch-packet \
  --scope SCOPE --slurm-snapshot /tmp/research-loop-slurm.json \
  EXP-ID -- EXACT-LAUNCH-COMMAND
```

On Isambard, read the installed `docs/research/isambard-site.md` (source:
`packs/slurm/docs/isambard-site.md`) before naming `workq`,
`--reservation=interactive`, or `interactive_qos`. For short preflight use
reservation-only routing without partition or QoS overrides. Inspect hidden
partitions with `--all`; verify access with a bounded probe rather than
inferring denial from `Accounts=root` alone. Long-running training uses workq.

For a new or unsettled resource choice, follow `TRAINING_EFFICIENCY.md`: compare
the same remaining declared results, respect authorized limits, and select the
lowest billed cost within 10% of the fastest feasible time to result. Add
`--resource-candidates FILE` to the read-only packet using that snapshot's
`captured_at`. Unknown estimates remain unranked/advisory. Reconsider at useful
stage/checkpoint boundaries; validate future launches without modifying running
frozen jobs. Array elements and execution-step usage remain separate from
allocation-level accounting in the snapshot.
