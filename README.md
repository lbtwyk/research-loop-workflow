# research-loop-workflow

Reusable research loop: one experiment spec, one ledger, evidence, and a user
decision. Add only the compute and project modules a workspace uses. This
repository does not contain datasets, models, or experiment results.

Two axes, installed separately:

- Research: `core` → `local`, `slurm`, or `kubernetes` → optional project topic
- Agent: `cursor` / `codex`

## Install

```bash
# Local GPU project
./install.sh --dest /path/to/project --local --agent cursor

# Slurm cluster
./install.sh --dest /path/to/project --slurm --agent cursor

# Kubernetes / KubeSphere cluster
./install.sh --dest /path/to/project --kubernetes --agent codex

# Music2Dance using local GPUs and both cluster types
./install.sh --dest /path/to/project --local --slurm --kubernetes --topic musics2dance \
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
packs/core/            experiment lifecycle, evidence, ledger, shared skills
packs/local/           direct-attached GPU execution
packs/slurm/           Slurm scheduling, preflight, training checks
packs/kubernetes/      Kubernetes/KubeSphere jobs and result delivery
packs/musics2dance/    project and host overlays
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

The ledger's `launch` and `preflight` commands currently require the Slurm
pack. Local and Kubernetes launches use their own launchers and record runtime
evidence in the same experiment ledger. Multiple compute packs can coexist.

## What This Is Not

- Not a copy of Musics2Dance science or experiment records
- Not a Cursor-only or Codex-only kit
- Not a site policy document; site details belong in project overlays
