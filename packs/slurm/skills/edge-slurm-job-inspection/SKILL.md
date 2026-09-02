---
name: edge-slurm-job-inspection
description: Use when the user asks what EDGE jobs are waiting or running, wants the exact `squeue`/`sacct` command to reuse, or asks how to find and live-tail the real log file for a Slurm job.
argument-hint: "[job-id or account question]"
allowed-tools:
  - read_file
  - grep
  - run_terminal_command
---

# Slurm Job Inspection

Project root defaults to `$RESEARCH_LOOP_SLURM_PROJECT_ROOT` when set.
Otherwise use the current repository.

## When to use

Use this when the task is about:

1. What jobs are waiting right now
2. What jobs are running right now
3. What `sacct` should be used for recent history
4. How to find the real `StdOut`/`StdErr` path for a live job
5. Why a job is pending because of scheduler policy
6. Whether a queued EDGE run is blocked by quota rather than broken code

Do not use this for non-Slurm tasks, generic repo editing, or finished-output verification after the log path is already known.

## Inputs / context to gather

1. Confirm whether the user wants:
   - waiting jobs only
   - whole account state
   - one specific job ID
   - the live log file for a running job
2. Confirm the relevant scope:
   - EDGE main checkout or worktree
   - current user account on this cluster
3. Capture any concrete job IDs, run IDs, or quoted pending reason from the user.
4. If the task is tied to an active experiment family, note the relevant `docs/experiments/*.md` file before changing scripts.

## Procedure

1. If the question is “what jobs are waiting,” start with the pending-only queue view:
   - `squeue -u "$USER" -t PD -o "%.18i %.9P %.32j %.8u %.2t %.12M %.12l %.6D %R"`

2. If the user may also care about running jobs, broaden immediately:
   - `squeue -u "$USER" -o "%.18i %.9P %.32j %.8u %.2t %.12M %.12l %.6D %R"`

3. If they ask “what about sacct” or want recent history, use:
   - `sacct -u "$USER" --starttime today --format=JobID,JobName%32,State,Elapsed,Start,End,NodeList%24 -X`
   - If they specifically want pending history, also use:
     - `sacct -u "$USER" --starttime today --state=PENDING --format=JobID,JobName%32,State,Elapsed,Start,End,NodeList%24 -X`

4. If the task is about one live job’s log path, recover the real file from scheduler metadata:
   - `scontrol show job <JOBID> | grep -E "StdOut|StdErr"`
   - If a compact machine-readable path helps, also use:
     - `sacct -j <JOBID> --format=JobID,JobName%32,State,StdOut%300 -X --noheader --parsable2`

5. Once `StdOut` is known, give the exact live-watch command:
   - `tail -f <stdout-path>`
   - Also provide a one-shot recent-lines variant when useful:
     - `tail -n 80 <stdout-path>`

6. If a job is pending and the user wants to know why, inspect the scheduler reason before discussing code:
   - `scontrol show job <JOBID>`
   - Look for `Reason=...` such as `QOSMaxJobsPerUserLimit` or `Priority`.

7. If the blocker looks quota-related, reproduce it once with a dry-run submit before changing walltimes repeatedly:
   - `sbatch --test-only <script-or-flags>`
   - If this still returns `AssocGrpCPUMinutesLimit`, treat it as an external account block.

8. Report back in the user’s preferred style:
   - lead with the exact command(s)
   - state whether the query showed waiting jobs, running jobs, or only history
   - if you found a log path, give the exact `tail -f` command

## Efficiency plan

1. Start with the narrowest query that matches the user’s wording.
2. If the narrow query returns only a header or incomplete picture, broaden once instead of running many variants.
3. Cache these facts before answering:
   - current job IDs
   - whether there are pending jobs
   - the pending `Reason` if any
   - the exact `StdOut` path for the target live job
   - whether `sbatch --test-only` confirms an external scheduler/accounting block
4. Stop rules:
   - If the user only asked for commands, do not over-investigate unrelated jobs.
   - If `StdOut` is already known from `scontrol`, stop searching and hand back `tail -f`.
   - If `AssocGrpCPUMinutesLimit` is reproduced, stop micro-tuning walltime and report the quota block.

## Pitfalls and fixes

- Symptom: the answer only mentions waiting jobs, but the user also wants the active run.
  - Likely cause: stopping after the pending-only `squeue` view
  - Fix: broaden to full `squeue -u "$USER"` and then `sacct`

- Symptom: the answer guesses where the log should be instead of giving the real file.
  - Likely cause: relying on repo path conventions instead of scheduler metadata
  - Fix: recover `StdOut` with `scontrol show job` or `sacct -j`

- Symptom: a one-running-job limit gets mistaken for a training bug.
  - Likely cause: not checking the pending `Reason`
  - Fix: inspect `scontrol show job <JOBID>` and report `Reason=QOSMaxJobsPerUserLimit` or other scheduler policy blockers directly

- Symptom: repeated walltime edits keep getting retried but the job never starts.
  - Likely cause: account-level quota such as `AssocGrpCPUMinutesLimit`
  - Fix: confirm once with `sbatch --test-only`, then stop resubmitting and report the run as blocked by quota rather than by code

- Symptom: `scontrol show job <JOBID>` is empty or says the job is invalid.
  - Likely cause: the job already left live Slurm state
  - Fix: switch to `sacct` for historical state and stdout lookup

## Verification checklist

1. Confirm the answer includes the exact command(s) the user can reuse.
2. Confirm you distinguished live queue state from accounting history.
3. If the task involved a running job, confirm you recovered the actual `StdOut` path.
4. If you mention a blocker, confirm it came from the scheduler `Reason`, not a guess.
5. If you claim the run is externally blocked, confirm you reproduced the same error with `sbatch --test-only` or equivalent scheduler evidence.
