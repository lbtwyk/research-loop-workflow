---
name: musics2dance-local-4090-bootstrap-train
description: Use when `/home/tianhup/Desktop/Musics2Dance` needs the real local 4090 bootstrap path, dependency repair, structured-cache validation, or a durable long-running G1 train launch instead of a plan-only answer.
argument-hint: "[experiment or motion-format target]"
allowed-tools:
  - read_file
  - grep
  - run_terminal_command
---

# Musics2Dance Local 4090 Bootstrap And Train

## When to use

Use this when working in `/home/tianhup/Desktop/Musics2Dance` and the task is to:

1. Actually set up the repo on the user's local 4090 machine
2. Run the supported download/process bootstrap path
3. Repair the old Jukebox/Jukemirlib dependency install
4. Validate processed FineDance-G1 caches before training
5. Launch a long-running local G1 training job in a way that leaves a durable tmux/log trail

Do not use this for Slurm jobs, non-local checkouts, or pure analysis tasks that do not need machine bring-up or a live run.

## Inputs / context to gather

1. Confirm the working directory is `/home/tianhup/Desktop/Musics2Dance`.
2. Check the current setup docs and bootstrap script first:
   - `README.md`
   - `docs/NEW_SERVER_SETUP.md`
   - `scripts/bootstrap_finedance_g1_4090.sh`
3. Capture whether the user expects:
   - download/bootstrap only
   - preprocess/cache build
   - a new training launch
   - any motion-format or experiment-specific constraint that changes validation or launch flags
4. Check the repo-local env state:
   - whether `.venv311/bin/python` exists
   - whether `.venv311/bin/activate` is absent in this checkout
5. If the task involves structured condition features, inspect:
   - `data/validate_preprocessed_data.py`
   - the target `processed_data_dir`

## Procedure

1. Start with the repo-local source of truth.
   - Read `docs/NEW_SERVER_SETUP.md` and `scripts/bootstrap_finedance_g1_4090.sh`.
   - Keep in mind this host is local, not Slurm: do not reach for `srun` or `sbatch`.

2. Bring up the env using the working local pattern.
   - If plain `python3.10 -m venv` fails because `ensurepip` or `python3.10-venv` is missing, switch to a conda-created repo-local `.venv311`.
   - Prefer invoking `.venv311/bin/python` directly instead of assuming `source .venv311/bin/activate` exists.

3. Repair the requirements install with the known escape hatch.
   - If `requirements-new-server.txt` fails under default pip resolution or build isolation, rerun with:
   - `python -m pip install --no-build-isolation --use-deprecated=legacy-resolver -r requirements-new-server.txt`

4. Continue the supported bootstrap path.
   - Use `scripts/bootstrap_finedance_g1_4090.sh`.
   - If the env already exists, prefer `--skip-env`.
   - If a large Jukebox download fails late with `curl: (56) OpenSSL SSL_read`, stop and check whether a resumable/local-cache path exists before restarting from scratch.

5. Launch long-running training through a durable tmux path.
   - Start a persistent bash pane.
   - Send commands line by line with `tmux send-keys` rather than stuffing the whole launch into `tmux new-session -d '...'`.
   - Use direct interpreter launch:
   - `PYTHONUNBUFFERED=1 python -m accelerate.commands.launch ...`
   - If MuJoCo could be touched, set `MUJOCO_GL=egl` before import and pass `--g1_mujoco_gl egl`.
   - If the task is training-only, prefer `--skip_train_sample_render` so sample rendering does not kill an otherwise healthy run.

6. Leave behind verification, not just a launch claim.
   - Capture the tmux session name, run dir, log path, and any W&B run id.
   - Confirm any bootstrap/preprocess validation you actually ran plus the first live training progress line before reporting success.

## Efficiency plan

1. Read the setup doc and bootstrap script before probing random machine state.
2. Cache these facts before answering:
   - whether `.venv311/bin/python` exists
   - whether `requirements-new-server.txt` needed the legacy pip flags
   - whether the cache validator passed
   - the exact tmux session, log path, and run dir
3. Stop rules:
   - If the validator passes and the live log shows training progress, stop digging into unrelated system details.
   - If the Jukebox download dies late and the repo has a resumable/cache path, pivot there instead of re-running the same flaky transfer.

## Pitfalls and fixes

- Symptom: bootstrap fails while creating the venv.
  - Likely cause: missing `ensurepip` / `python3.10-venv`
  - Fix: use a conda-created repo-local `.venv311`

- Symptom: `requirements-new-server.txt` fails with `pkg_resources` or `ResolutionImpossible`.
  - Likely cause: build isolation plus the old Jukebox/Jukemirlib dependency shape
  - Fix: rerun with `--no-build-isolation --use-deprecated=legacy-resolver`

- Symptom: the env exists, but activation or the long launch command still fails.
  - Likely cause: `.venv311/bin/activate` is absent here, or tmux command quoting is fragile
  - Fix: use `.venv311/bin/python` directly from a persistent bash pane

- Symptom: processed cache validation fails on `wav2clip_local_motion_intensity_beatness`.
  - Likely cause: stale assumption that features live in one flat directory
  - Fix: validate against the combined structured feature dirs before trusting the cache

- Symptom: healthy training dies at sample generation with `gladLoadGL` or `Native G1 MuJoCo rendering failed to initialize`.
  - Likely cause: missing EGL backend, not broken optimization
  - Fix: set `MUJOCO_GL=egl`, pass `--g1_mujoco_gl egl`, or skip train sample render

## Verification checklist

1. Confirm the working path came from `docs/NEW_SERVER_SETUP.md` and `scripts/bootstrap_finedance_g1_4090.sh`.
2. Confirm the env path and interpreter actually used.
3. Confirm whether the legacy pip flags were required.
4. Confirm the cache validator passed for the intended feature type and motion format.
5. Confirm the final report includes the tmux session, log path, run dir, and at least one live training progress proof point if a launch occurred.
