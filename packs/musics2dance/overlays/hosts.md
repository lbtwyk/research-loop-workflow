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
in the owner's private home and project behavior in the repository or this
workflow pack.

The owner's SSH sessions use the private home
`/home/tianhup/.homes/lbtwyk`, with Codex state in its own `.codex` directory.
That directory owns the config, model instructions, authentication, mutable
task state, daemon, and control socket. Start or inspect it through
`codex-lbtwyk`; the Desktop App can continue to invoke `codex app-server proxy`.
The owner defaults are `gpt-6-astra` with medium reasoning. Route every Codex
review through the dedicated read-only `reviewer` agent using `gpt-5.6-luna`,
max reasoning, and fast service tier. Keep the ordinary Tianhu home and
`/home/tianhup/.codex/app-server-control/app-server-control.sock`
assigned to Tianhu. Never repoint, restart, or stop that default daemon as part
of owner setup or maintenance.

On `hrl-4090-server`, the owner's MacBook SSH public key is bound to
`/home/tianhup/.local/bin/lbtwyk-ssh-session`. That entry exports the isolated
`HOME`, `CODEX_HOME`, and owner tool path before running the original SSH
command, so an unmodified Desktop App command (`codex app-server proxy`) reaches
the owner's socket automatically. Do not attach this forced command to Tianhu's
SSH keys.
