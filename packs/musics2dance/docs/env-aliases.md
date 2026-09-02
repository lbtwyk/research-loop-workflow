# Environment Aliases

Canonical names live in the core and slurm packs:

- `RESEARCH_LOOP_RESEARCH_ASYNC`
- `RESEARCH_LOOP_TRAINING_PREFLIGHT`
- `RESEARCH_LOOP_FORMAL_LAUNCH_COMMAND_JSON`
- `RESEARCH_LOOP_SLURM_RESERVATION`
- `RESEARCH_LOOP_INTERACTIVE_DISPATCH_ROOT`

Older Musics2Dance worktrees used `M2D_*`. The slurm snapshot still accepts
`M2D_INTERACTIVE_DISPATCH_ROOT` as a fallback. Prefer the `RESEARCH_LOOP_*`
names in new work.
