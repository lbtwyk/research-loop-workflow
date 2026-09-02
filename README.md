# research-loop-workflow

Reusable research loop: one experiment spec, one ledger, independent review,
then evidence and a user decision. This repository records the workflow and
skills. It does not contain datasets, models, or experiment results.

Two axes, installed separately:

- Content: `core` / `slurm` / `musics2dance`
- Agent: `cursor` / `codex`

## Install

```bash
# New project, Cursor only
./install.sh --dest /path/to/project --core --agent cursor

# Slurm project
./install.sh --dest /path/to/project --core --slurm --agent cursor

# Music2Dance on both agents
./install.sh --dest /path/to/project --core --slurm --topic musics2dance \
  --agent cursor --agent codex
```

`--agent` is optional. Without it, ledger and docs install, but no
`.cursor/` or `.codex/` files are written.

Personal skill install:

```bash
./install.sh --personal --core --agent cursor
```

Optional paper and process skills: add `--optional`.

## Layout

```text
packs/core/            agent-neutral workflow, ledger, shared skills
packs/slurm/           scheduler snapshot, preflight, Slurm skills
packs/musics2dance/    host skills, async transport
adapters/cursor/       .cursor rules, hooks, research-reviewer overlay
adapters/codex/        .codex hooks, agents/openai.yaml
```

## Commands After Core Install

```bash
python scripts/experiment_ledger.py add EXP-YYYYMMDD-slug
python scripts/experiment_ledger.py outline EXP-YYYYMMDD-slug
python scripts/experiment_ledger.py sync
python scripts/experiment_ledger.py lint
```

`launch` and `preflight` require the slurm pack.

## What This Is Not

- Not a copy of Musics2Dance science or experiment records
- Not a Cursor-only or Codex-only kit
- Not a cluster policy document unless you install `slurm`
