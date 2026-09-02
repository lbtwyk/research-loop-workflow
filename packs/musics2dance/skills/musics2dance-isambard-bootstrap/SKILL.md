---
name: musics2dance-isambard-bootstrap
description: Use when `/lus/lfs1aip2/projects/u6og/yukunwang.u6og/Musics2Dance` needs the verified Isambard bring-up path, including repo-local env repair, old Jukebox dependency workarounds, and Slurm GPU validation.
argument-hint: "[bootstrap or validation target]"
allowed-tools:
  - read_file
  - grep
  - run_terminal_command
---

# Musics2Dance Isambard Bootstrap

## When to use

Use this when working in `/lus/lfs1aip2/projects/u6og/yukunwang.u6og/Musics2Dance` and the task is to:

1. Make the repo self-sufficient on Isambard
2. Repair the repo-local Python environment for old `jukebox` / `jukemirlib` deps
3. Refresh docs or agent guidance for the cluster path
4. Validate the actual CUDA stack on GH200 GPU nodes

Do not use this for the local 4090 workflow, generic research-only tasks, or non-Slurm environments.

## Inputs / context to gather

1. Confirm the working directory is `/lus/lfs1aip2/projects/u6og/yukunwang.u6og/Musics2Dance`.
2. Read the current sources of truth first:
   - `docs/NEW_SERVER_SETUP.md`
   - `scripts/setup_new_server.sh`
   - `AGENTS.md`
   - `README.md`
3. Check whether `.venv311` already exists and whether it looks partially upgraded.
4. Capture whether the user wants:
   - env repair only
   - full repo bring-up
   - docs and agent guidance updated
   - CUDA validation on GPU nodes

## Procedure

1. Start from the repo-local runbook and script.
   - Read `docs/NEW_SERVER_SETUP.md` and `scripts/setup_new_server.sh` before probing random machine state.
   - Treat `scripts/setup_new_server.sh` as the canonical bootstrap entrypoint.

2. Bring up the repo-local env with the known Isambard shape.
   - Prefer repo-local `.venv311`.
   - If old pinned deps break, install `setuptools<81` first.
   - Run `requirements-new-server.txt` with the known compatibility flags:
   - `--no-build-isolation --use-deprecated=legacy-resolver`

3. If the venv looks half-upgraded, repair that before retrying.
   - Check for leftover backup dirs such as `~setuptools` or `~kg_resources`.
   - Clean the stale backup dirs before trusting the next pip run.

4. Fix torch for the real GPU-node target, not the login node.
   - Use the CUDA 12.6 wheel index when the environment matches the recorded Isambard image:
   - `https://download.pytorch.org/whl/cu126`
   - The validated stack in memory was `torch 2.12.1+cu126` and `torchaudio 2.11.0+cu126` on aarch64 GH200 nodes.

5. Validate CUDA inside Slurm.
   - Do not trust login-node `torch.cuda.is_available()`.
   - Run a short GPU-node validation job and confirm the final torch version, CUDA availability, and visible device.

6. Leave the repo more reusable than you found it.
   - If the user asked for full setup, update `docs/NEW_SERVER_SETUP.md`, `README.md`, and `AGENTS.md` so the working Isambard path is documented for the next run.

7. Run at least one CPU-side sanity check after env repair when possible.
   - Known checks that passed in memory: `py_compile` and `tests.test_g1_motion_prior`.

## Efficiency plan

1. Read the existing runbook and bootstrap script before trying alternate setup commands.
2. Cache these facts before answering:
   - whether `.venv311` exists
   - whether `setuptools<81` was needed
   - whether legacy pip flags were needed
   - which torch wheel index was used
   - what the Slurm GPU validation actually reported
3. Stop rules:
   - If the env installs cleanly, Slurm reports CUDA healthy, and the sanity checks pass, stop exploring unrelated system details.
   - If the login node and GPU node disagree, trust the GPU-node Slurm result and stop re-probing on the login node.

## Pitfalls and fixes

- Symptom: install fails with `ModuleNotFoundError: No module named 'pkg_resources'`.
  - Likely cause: newer setuptools plus build isolation do not match the old pinned Jukebox dependency path.
  - Fix: pin `setuptools<81` and rerun with `--no-build-isolation --use-deprecated=legacy-resolver`.

- Symptom: repeated pip retries behave inconsistently after an interrupted upgrade.
  - Likely cause: stale backup dirs such as `~setuptools` or `~kg_resources`.
  - Fix: clean those leftovers before retrying.

- Symptom: torch looks okay on the login node but CUDA fails or mismatches on the GPU node.
  - Likely cause: wrong wheel choice and misleading login-node probing.
  - Fix: reinstall from the cu126 index when applicable and validate in a short Slurm GPU job.

- Symptom: the repo works for one shell session but the next agent still has to rediscover the path.
  - Likely cause: docs or agent guidance were not updated.
  - Fix: refresh `docs/NEW_SERVER_SETUP.md`, `README.md`, and `AGENTS.md` when the user asked for env/docs/agent setup.

## Verification checklist

1. Confirm the answer names the repo-local sources of truth used.
2. Confirm whether `setuptools<81` and the legacy pip flags were required.
3. Confirm the actual torch and torchaudio stack used on the GPU node.
4. Confirm CUDA was validated in Slurm rather than only on the login node.
5. Confirm any requested doc or agent updates were actually made, not just suggested.
