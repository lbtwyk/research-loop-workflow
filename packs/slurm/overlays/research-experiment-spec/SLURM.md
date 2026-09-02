# Slurm Overlay For Research Experiment Spec

When the slurm pack is installed, compile stage closure with a scheduler
snapshot:

```bash
python scripts/slurm_state_snapshot.py --output /tmp/research-loop-slurm.json
python scripts/experiment_ledger.py launch-packet \
  --scope SCOPE --slurm-snapshot /tmp/research-loop-slurm.json \
  EXP-ID -- EXACT-LAUNCH-COMMAND
```

On Isambard, read `packs/slurm/docs/isambard-site.md` before naming
`workq`, `--reservation=interactive`, or `interactive_qos`.
