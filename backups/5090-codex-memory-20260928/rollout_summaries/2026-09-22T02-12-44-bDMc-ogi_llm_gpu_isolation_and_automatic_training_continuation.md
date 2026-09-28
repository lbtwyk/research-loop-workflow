thread_id: 01a0c6e3-0d78-7bf3-b128-19efed157ec0
updated_at: 2026-09-24T06:27:02+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T10-12-44-01a0c6e3-0d78-7bf3-b128-19efed157ec0.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Kubernetes GPU-group isolation, training checks, and automatic continuation

Rollout context: `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws`, primarily `Musics2Dance`; user managed `ogi-llm` Kubernetes GPU training and repeatedly requested status checks, stopping/restarting jobs, full result reports, and automatic continuation.

## Task 1: Diagnose and stop/repair two- and three-GPU jobs

Outcome: partial

Preference signals:
- The user clarified that GPU pool isolation is a hard rule: “用什么组就只能申请那个组的卡” and specifically that `ogi-llm` jobs may use only `ogi-llm` GPUs. Future YAML must not tolerate or request other pools.
- The user clarified that the correct configuration is to allow “这个组里的所有卡”, not a fixed hostname list. Future jobs should retain the `ogi-llm` pool restriction while removing node08/node10/node13/node14 affinity restrictions.
- The user expects existing jobs to be inspected and stopped only after preserving logs/checkpoints; do not blindly delete healthy work.

Reusable knowledge:
- The host has no Kubernetes control channel or `~/.kube`; hot-storage readback does not prove submission or running state. Cluster actions require a KubeSphere terminal.
- Historical quota diagnosis: `m2d-commit-trajectory-3h-fast-r1` initially had `FailedCreate` with requested 3, used 8, limit 9, but later created a Running Pod. Re-query current nonterminal Pods before cleanup.
- Correct `ogi-llm` scheduling shape: namespace `ogi-llm`, `nvidia.com/gpu` request equal to limit, toleration only for `ogi/node-pool=ogi-llm`, no affinity/nodeSelector/nodeName restriction.
- The corrected two-card artifact was created at `runs/causal_native_trajectory/llm-only/job-2h-llm-only.yaml`; its apply script was `APPLY_2H_LLM_ONLY.txt`. Local YAML/shell/compile checks passed, but it was not submitted.

Failures and how to do differently:
- Early reasoning incorrectly treated multiple tolerations as permission to borrow other pools. Kubernetes tolerations do not grant cross-pool authorization; follow the user’s hard pool-isolation rule.
- Do not claim a Job is submitted, queued, or blocked from hot-storage release files alone; require `kubectl get/describe` output.

References:
- Namespace/pool: `ogi-llm`; hard user rule: only `ogi-llm` GPUs.
- Useful status commands: `kubectl describe job -n ogi-llm <job>` and `kubectl get pods -n ogi-llm -l job-name=<job> -o wide`.

## Task 2: Three-card history-resampling experiment report

Outcome: partial

Reusable knowledge:
- Four training arms reached 6250 updates: `base`, `cof_control`, `rf_continuous`, `rf_joint`; 18 test songs, three generation seeds, short/60s/120s evaluations.
- Main conclusion: no clear overall improvement over ordinary CoF. `rf_joint` had a local 120-second late-window rotation result of 0 versus 3 for CoF, but only four songs; this is not evidence that rotation instability is solved.
- Music-score paired intervals crossed zero. The joint method was slower (about 223 minutes versus 166.5 minutes for CoF) without a demonstrated broad benefit.
- Video completion was initially 21/22; scientific acceptance remained pending. Results must preserve limitations: one training seed, prior development exposure, and repeated audio pairs.

References:
- Detailed report: `runs/cluster-jobs-20260923/full-report/完整结果.md`.
- Experiment: `EXP-20260922-fd-causal-history-resampling`.

## Task 3: Verify and extend the new music self-calibration training

Outcome: partial

Preference signals:
- The user asked to double the new 6250-step runs to 12500 and then clarified: “要自动的” -> future continuation should be prepared as a one-time detached watcher, not require the user to return after completion.
- The user explicitly confirmed the continuation must remain restricted to `ogi-llm`; future generated continuation YAML should enforce pool-only toleration and no hostname restriction.

Reusable knowledge:
- The original music self-calibration Job eventually ran successfully after an earlier quota failure. Hot logs showed formal progress around fixed 99/6250 and dynamic 96/6250, microbatch 384, `proof=false`, with recovery checkpoints and no observed training error.
- The experiment has two new arms: `fixed` and `dynamic`, each 6250 updates, using a 0.53-second action chunk; old-quarter and old-half controls are evaluation controls, not new training arms.
- The 12500 continuation artifacts were prepared under `runs/causal_music_self_calibration/extend-12500/` and uploaded/read back to the matching hot-storage directory. The continuation preserves original optimizer/update/resume logic and writes separate `training-12500/` outputs.
- `START_AUTO.txt` enables a detached cluster-terminal watcher: wait for the original Job to report `Complete=True`, stop on `Failed=True`, detect an existing continuation Job, and otherwise create `m2d-music-calibration-12500-3h`. Mock tests for complete, failed, existing, and wait-then-complete cases passed.
- Automatic continuation was prepared and uploaded but not confirmed enabled because the local host cannot run `kubectl`; one KubeSphere terminal paste is still required.

Failures and how to do differently:
- The trainer hard-coded 6250 as its formal endpoint, so changing local config cannot extend an already running Job. Use a separate continuation Job from verified checkpoints.
- Do not imply automatic continuation is active until cluster-side evidence shows the detached watcher was started.

References:
- Original Job: `m2d-causal-music-calibration-3h`.
- Continuation Job: `m2d-music-calibration-12500-3h`.
- Enablement file: `runs/causal_music_self_calibration/extend-12500/START_AUTO.txt`.
- Hot path: `/hot/upload/EXP-20260922-fd-causal-music-self-calibration/extend-12500/`.

## Task 4: Reviewer configuration request

Outcome: uncertain

Preference signals:
- The user requested: “独立reviewer改为6sol high”. This is a direct workflow/configuration change request and should be treated as an unresolved requested change until the relevant reviewer configuration is located, modified, and validated.

Failures and how to do differently:
- No tool action or verification for this reviewer-setting request occurred before the rollout ended. Future work should locate the active independent-reviewer configuration, change it to the requested `6sol high` setting, and verify the effective configuration without assuming the change happened.
