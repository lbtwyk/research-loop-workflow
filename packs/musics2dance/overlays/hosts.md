# Musics2Dance Host Overlay

FineDance and OMG-native stacks stay separate. Do not copy or silently
retarget OMG data into legacy pickle or cache trees.

| Host | Role |
|---|---|
| Isambard (`u6og`) | Slurm GPU training, evaluation, rendering, heavy preprocess |
| `4090-ts` | Direct-attached 4090, local bootstrap and tmux train |
| `ubt-5090` | Separate KubeSphere host; do not borrow Isambard rules |

For Isambard interactive dispatch reuse, set:

```bash
export RESEARCH_LOOP_INTERACTIVE_DISPATCH_ROOT="$HOME/.cache/musics2dance/interactive"
export M2D_INTERACTIVE_DISPATCH_ROOT="$RESEARCH_LOOP_INTERACTIVE_DISPATCH_ROOT"
```

`M2D_*` names remain aliases for older worktrees. New code reads
`RESEARCH_LOOP_*`.

## Shared Unix Home

The local 4090 workspace may run under Tianhu's Unix account while the project
owner uses a separate Codex identity. Do not edit the base
`/home/tianhup/.codex/config.toml`, base model instructions, authentication, or
globally installed skills for owner-specific behavior. Put CLI personalization
in the explicit `lbtwyk` profile and project behavior in the repository or this
workflow pack. A shared Desktop app-server continues to use its launch-time
`CODEX_HOME`; changing that daemon requires explicit coordination.
