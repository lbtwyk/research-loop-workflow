#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
DEST=""
PERSONAL=0
INSTALL_CORE=0
INSTALL_SLURM=0
INSTALL_TOPIC=""
AGENTS=()
OPTIONAL=0

usage() {
  cat <<'EOF'
Install research-loop-workflow packs into a project or personal skill dir.

  ./install.sh --dest /path/to/project --core
  ./install.sh --dest /path/to/project --core --slurm --agent cursor
  ./install.sh --dest /path/to/project --core --slurm --topic musics2dance --agent cursor --agent codex
  ./install.sh --personal --core --agent cursor

Default is --core only when at least one of --core/--slurm/--topic/--agent is set.
--dest is required unless --personal is used alone for skills.
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dest) DEST="${2:-}"; shift 2 ;;
    --personal) PERSONAL=1; shift ;;
    --core) INSTALL_CORE=1; shift ;;
    --slurm) INSTALL_SLURM=1; shift ;;
    --topic)
      INSTALL_TOPIC="${2:-}"
      shift 2
      ;;
    --agent) AGENTS+=("${2:-}"); shift 2 ;;
    --optional) OPTIONAL=1; shift ;;
    -h|--help) usage; exit 0 ;;
    *) echo "unknown argument: $1" >&2; usage; exit 2 ;;
  esac
done

if [[ "$INSTALL_CORE" -eq 0 && "$INSTALL_SLURM" -eq 0 && -z "$INSTALL_TOPIC" && ${#AGENTS[@]} -eq 0 ]]; then
  INSTALL_CORE=1
fi
if [[ "$INSTALL_SLURM" -eq 1 || -n "$INSTALL_TOPIC" ]]; then
  INSTALL_CORE=1
fi
if [[ -n "$INSTALL_TOPIC" && "$INSTALL_TOPIC" != "musics2dance" ]]; then
  echo "unsupported topic: $INSTALL_TOPIC" >&2
  exit 2
fi
if [[ "$PERSONAL" -eq 0 && -z "$DEST" ]]; then
  echo "--dest is required unless --personal is used for skills only" >&2
  exit 2
fi

copy_dir() {
  local src="$1"
  local dest="$2"
  mkdir -p "$dest"
  cp -a "$src"/. "$dest"/
}

install_skills() {
  local src_root="$1"
  local dest_root="$2"
  mkdir -p "$dest_root"
  local skill
  for skill in "$src_root"/*; do
    [[ -d "$skill" ]] || continue
    [[ "$(basename "$skill")" == "optional" ]] && continue
    [[ "$(basename "$skill")" == "shared-references" ]] && continue
    copy_dir "$skill" "$dest_root/$(basename "$skill")"
  done
  if [[ -d "$src_root/shared-references" ]]; then
    copy_dir "$src_root/shared-references" "$dest_root/shared-references"
  fi
  if [[ "$OPTIONAL" -eq 1 && -d "$src_root/optional" ]]; then
    for skill in "$src_root/optional"/*; do
      [[ -d "$skill" ]] || continue
      copy_dir "$skill" "$dest_root/$(basename "$skill")"
    done
  fi
}

overlay_dir() {
  local src="$1"
  local dest="$2"
  [[ -d "$src" ]] || return 0
  mkdir -p "$dest"
  cp -a "$src"/. "$dest"/
}

if [[ -n "$DEST" ]]; then
  DEST="$(mkdir -p "$DEST" && cd "$DEST" && pwd)"
  if [[ "$INSTALL_CORE" -eq 1 ]]; then
    mkdir -p "$DEST/scripts" "$DEST/docs/research" "$DEST/docs/experiments/contracts" "$DEST/docs/experiments/reviews"
    cp -a "$ROOT/packs/core/scripts/experiment_ledger.py" "$DEST/scripts/"
    cp -a "$ROOT/packs/core/scripts/experiment_guard.py" "$DEST/scripts/"
    cp -a "$ROOT/packs/core/docs/workflow/WORKFLOW.md" "$DEST/docs/research/WORKFLOW.md"
    cp -a "$ROOT/packs/core/docs/workflow/PREFLIGHT.md" "$DEST/docs/research/PREFLIGHT.md"
    if [[ ! -f "$DEST/AGENTS.md" ]]; then
      cp -a "$ROOT/packs/core/AGENTS.md" "$DEST/AGENTS.md"
    fi
    if [[ ! -f "$DEST/docs/experiments/registry.json" ]]; then
      cp -a "$ROOT/packs/core/templates/experiments/registry.json" "$DEST/docs/experiments/registry.json"
    fi
    if [[ ! -f "$DEST/docs/research/experiment-template.md" ]]; then
      cp -a "$ROOT/packs/core/templates/experiments/experiment-template.md" "$DEST/docs/research/experiment-template.md"
    fi
    if [[ ! -f "$DEST/docs/experiments/contracts/contract-template.json" ]]; then
      cp -a "$ROOT/packs/core/templates/experiments/contract-template.json" "$DEST/docs/experiments/contracts/contract-template.json"
    fi
  fi
  if [[ "$INSTALL_SLURM" -eq 1 ]]; then
    mkdir -p "$DEST/scripts" "$DEST/docs/research"
    cp -a "$ROOT/packs/slurm/scripts/"*.py "$DEST/scripts/"
    cp -a "$ROOT/packs/slurm/docs/." "$DEST/docs/research/"
  fi
  if [[ "$INSTALL_TOPIC" == "musics2dance" ]]; then
    mkdir -p "$DEST/scripts" "$DEST/docs/research" "$DEST/research/schemas"
    cp -a "$ROOT/packs/musics2dance/scripts/research_async_guard.py" "$DEST/scripts/"
    cp -a "$ROOT/packs/musics2dance/docs/." "$DEST/docs/research/"
    cp -a "$ROOT/packs/musics2dance/schemas/." "$DEST/research/schemas/"
    cp -a "$ROOT/packs/musics2dance/overlays/hosts.md" "$DEST/docs/research/HOSTS.md"
  fi
fi

for agent in "${AGENTS[@]+"${AGENTS[@]}"}"; do
  case "$agent" in
    cursor)
      if [[ "$PERSONAL" -eq 1 ]]; then
        install_skills "$ROOT/packs/core/skills" "$HOME/.cursor/skills"
        if [[ "$INSTALL_SLURM" -eq 1 ]]; then
          install_skills "$ROOT/packs/slurm/skills" "$HOME/.cursor/skills"
        fi
        if [[ "$INSTALL_TOPIC" == "musics2dance" ]]; then
          install_skills "$ROOT/packs/musics2dance/skills" "$HOME/.cursor/skills"
        fi
        overlay_dir "$ROOT/adapters/cursor/skills-overlays" "$HOME/.cursor/skills"
      fi
      if [[ -n "$DEST" ]]; then
        install_skills "$ROOT/packs/core/skills" "$DEST/.cursor/skills"
        if [[ "$INSTALL_SLURM" -eq 1 ]]; then
          install_skills "$ROOT/packs/slurm/skills" "$DEST/.cursor/skills"
        fi
        if [[ "$INSTALL_TOPIC" == "musics2dance" ]]; then
          install_skills "$ROOT/packs/musics2dance/skills" "$DEST/.cursor/skills"
        fi
        overlay_dir "$ROOT/adapters/cursor/skills-overlays" "$DEST/.cursor/skills"
        mkdir -p "$DEST/.cursor/hooks" "$DEST/.cursor/rules"
        cp -a "$ROOT/adapters/cursor/.cursor/rules/." "$DEST/.cursor/rules/"
        cp -a "$ROOT/packs/core/scripts/experiment_guard.py" "$DEST/.cursor/hooks/experiment_guard.py"
        if [[ "$INSTALL_TOPIC" == "musics2dance" ]]; then
          cp -a "$ROOT/packs/musics2dance/scripts/research_async_guard.py" "$DEST/.cursor/hooks/research_async_guard.py"
          cp -a "$ROOT/adapters/cursor/.cursor/hooks.with-async.json" "$DEST/.cursor/hooks.json"
        else
          cp -a "$ROOT/adapters/cursor/.cursor/hooks.json" "$DEST/.cursor/hooks.json"
        fi
      fi
      ;;
    codex)
      if [[ "$PERSONAL" -eq 1 ]]; then
        install_skills "$ROOT/packs/core/skills" "$HOME/.codex/skills"
        if [[ "$INSTALL_SLURM" -eq 1 ]]; then
          install_skills "$ROOT/packs/slurm/skills" "$HOME/.codex/skills"
        fi
        if [[ "$INSTALL_TOPIC" == "musics2dance" ]]; then
          install_skills "$ROOT/packs/musics2dance/skills" "$HOME/.codex/skills"
        fi
        overlay_dir "$ROOT/adapters/codex/skills-overlays" "$HOME/.codex/skills"
      fi
      if [[ -n "$DEST" ]]; then
        install_skills "$ROOT/packs/core/skills" "$DEST/.agents/skills"
        if [[ "$INSTALL_SLURM" -eq 1 ]]; then
          install_skills "$ROOT/packs/slurm/skills" "$DEST/.agents/skills"
        fi
        if [[ "$INSTALL_TOPIC" == "musics2dance" ]]; then
          install_skills "$ROOT/packs/musics2dance/skills" "$DEST/.agents/skills"
        fi
        overlay_dir "$ROOT/adapters/codex/skills-overlays" "$DEST/.agents/skills"
        mkdir -p "$DEST/.codex/hooks"
        cp -a "$ROOT/packs/core/scripts/experiment_guard.py" "$DEST/.codex/hooks/experiment_guard.py"
        if [[ "$INSTALL_TOPIC" == "musics2dance" ]]; then
          cp -a "$ROOT/packs/musics2dance/scripts/research_async_guard.py" "$DEST/.codex/hooks/research_async_guard.py"
          cp -a "$ROOT/adapters/codex/.codex/hooks.with-async.json" "$DEST/.codex/hooks.json"
        else
          cp -a "$ROOT/adapters/codex/.codex/hooks.json" "$DEST/.codex/hooks.json"
        fi
      fi
      ;;
    *)
      echo "unsupported agent: $agent" >&2
      exit 2
      ;;
  esac
done

echo "installed to ${DEST:-personal skills}"
echo "core=$INSTALL_CORE slurm=$INSTALL_SLURM topic=${INSTALL_TOPIC:-none} agents=${AGENTS[*]:-none}"
