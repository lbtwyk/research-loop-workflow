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
