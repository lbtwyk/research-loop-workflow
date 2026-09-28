# Raw Memories

Merged stage-1 raw memories (stable ascending thread-id order):

## Thread `019f3b7b-6b62-7a90-ac3a-e36d61298c86`
updated_at: 2026-07-12T19:23:20+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/07/07/rollout-2026-07-07T15-29-32-019f3b7b-6b62-7a90-ac3a-e36d61298c86.jsonl
rollout_summary_file: 2026-07-07T07-29-32-jMPA-utars_lingbot_vla2_benchmark_ready.md

---
description: Ready-validated LingBot-VLA 2.0 UTars pipeline for mixed real/sim handling-box data; added weighted 60/40 sampling, local LeRobot v2.1 compatibility, smoke/preflight checks, eval/server launchers, and experiment ledger updates.
task: set up UTars LingBot-VLA 2.0 benchmark pipeline
task_group: ubt_isaac_sim_ws / lingbot_vla2
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: LingBot-VLA, UTars, LeRobot v2.1, weighted multi-dataset, local dataset root, relative_joint_position, eval launcher, policy server, handling-box, Isaac Sim, preflight
---

### Task 1: UTars LingBot-VLA 2.0 pipeline

task: build and validate UTars LingBot-VLA 2.0 benchmark pipeline from real teleop + SDG handling-box simulation data

task_group: ubt_isaac_sim_ws / lingbot_vla2

task_outcome: success

Preference signals:
- user kept framing the next UTars Isaac task as something that should work with teleop + planning, not a purely abstract benchmark -> future similar asks should default to a concrete runnable pipeline/readiness check.
- user repeatedly asked in a practical “can it run / is it ready” mode -> future similar responses should prioritize operational readiness and exact launch paths over theory.

Reusable knowledge:
- local LingBot dataset loading needed to resolve repo-like strings as `root` when the dataset lives on disk, otherwise the code tried to contact Hugging Face and failed with 401 / repo-id errors.
- local UTars real data had non-contiguous episode indices; explicit `episodes=[...]` from `meta/episodes.jsonl` was required to load the whole split correctly.
- upstream LingBot multi-dataset loading concatenated data by default; to preserve the intended 60/40 real/sim mix, the pipeline needed weighted virtual sampling.
- first-stage UTars should use 16 active dims with a 55D canonical layout, `relative_joint_position`, 50-step horizon, and `relative_type: joint` for action features.
- preflight verified counts: 258,561 real frames + 46,984 sim frames -> 430,935 weighted virtual samples.

Failures and how to do differently:
- treating local `train` as a repo id caused download/auth failures; pass `root` and local episode lists.
- using default action relative handling can miscompute joint deltas; explicitly mark joint actions with `relative_type: joint`.
- eval launcher needed a valid local trajectory id and normalization path; otherwise it could start with wrong defaults.

References:
- `MODE=preflight ./script/vla_lingbot_v2/run_utars_lingbot_train.sh` -> passed and printed `"weights": {"real": 0.6, "simulation": 0.4}`, `"active_dimensions": 16`, `"canonical_dimensions": 55`, `"action_target": "relative_joint_position"`.
- smoke loader output showed `physical_frames [258561, 46984]`, `virtual_frames [258561, 172374]`, `total_virtual_frames 430935`, and sample shapes `state_arm [14]`, `state_head [2]`, `action_arm [50, 14]`, `action_head [50, 2]` for both real and sim.
- key files: `script/vla_lingbot_v2/prepare_utars_lingbot_data.py`, `script/vla_lingbot_v2/validate_lingbot_pipeline.py`, `script/vla_lingbot_v2/smoke_lingbot_dataset.py`, `script/vla_lingbot_v2/vla_policy_server_lingbot_v2.py`, `script/vla_lingbot_v2/run_utars_lingbot_train.sh`, `script/vla_lingbot_v2/eval_utars_lingbot.sh`, `script/vla_lingbot_v2/run_lingbot_v2_server.sh`, `script/vla_lingbot_v2/setup_lingbot_v2_environment.sh`, and `script/vla_lingbot_v2/patches/weighted_multi_dataset.patch`.
- experiment record updated in `docs/experiments/EXP-20260712-utars-lingbot-vla2-benchmark.md` and `docs/experiments/INDEX.md`.

## Thread `019fcb3b-c1f8-7331-a079-a169b3af742f`
updated_at: 2026-08-12T08:50:00+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/08/04/rollout-2026-08-04T13-25-18-019fcb3b-c1f8-7331-a079-a169b3af742f.jsonl
rollout_summary_file: 2026-08-04T05-25-18-12qz-h200_doc_reconciliation_and_100ep_closed_loop_comparison.md

---
description: H200 smoke-job workflow was corrected to use latest docs and KubeSphere heredoc submission; later 100-episode locked_arms vs full_policy batch comparison on a 30,000-step local checkpoint completed, with video locations and codec checks verified
task: reconcile H200 smoke-job workflow and run closed-loop comparison batch
task_group: /home/wangyukun/ubt_isaac_sim_ws
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: H200, KubeSphere, print_kubesphere_apply.sh, validate_h200_smoke_job.py, docs/h200-current-state.yaml, node08, node10, locked_arms, full_policy, 100-episode comparison, H.264, comparison.json, videos
---

### Task 1: Reconcile H200 smoke-job workflow

task: reconcile latest H200 docs and smoke-job submission flow
task_group: H200 workflow / KubeSphere submission
task_outcome: success

Preference signals:
- when the user said "你再看一下最新更新过的h200文档，是不是流程你想错了" -> reread the latest H200 docs first; do not rely on older assumptions about the submission flow
- when the user said "给我详细怎么做，一步步教我" -> default to step-by-step operational instructions for H200/KubeSphere work
- when advising cross-environment handoff, the user correction showed 5090 and KubeSphere do not share a filesystem -> do not tell the user to copy a YAML into KubeSphere's current directory; use a copy/paste heredoc from 5090 instead

Reusable knowledge:
- `docs/h200-current-state.yaml` was the authoritative current-state file; it should be read before `docs/H200_SIMPLE_WORKFLOW.md`, then the experiment spec
- the smoke YAML that validated successfully was `0.logs/h200_jobs/job-same-shelf-500-smoke.yaml`
- `validate_h200_smoke_job.py` printed `H200_SMOKE_JOB_OK` for the correct contract
- `print_kubesphere_apply.sh` emits a self-contained `kubectl apply -f - <<'EOF' ... EOF` block for KubeSphere submission
- the correct smoke Job contract was v2 image, node08/node10 only, one GPU, H200 preflight, and 100-step smoke

Failures and how to do differently:
- earlier guidance implying the YAML should be placed in the KubeSphere terminal was wrong because the 5090 and KubeSphere environments do not share a filesystem
- a generic Pod watch pattern was too loose; the updated workflow uses the specific Job name and validator-generated contract

References:
- `python3 syntheticdatageneration/script/vla_n17_fullbody/validate_h200_smoke_job.py 0.logs/h200_jobs/job-same-shelf-500-smoke.yaml` -> `H200_SMOKE_JOB_OK`
- `kubectl apply -f - <<'EOF'` heredoc emitted by `print_kubesphere_apply.sh`
- Job `utars-groot-n17-same-shelf-500-smoke-v2`, image `ubhub.ubtrobot.com/ogi/wangyukun-groot-n17-h200:cu128-torch271-v2`, hosts `node08,node10`, `gpu=1 run_mode=smoke max_steps=100`

### Task 2: 100-episode locked_arms vs full_policy batch

task: run and compare 100-episode closed-loop batches on the 30,000-step checkpoint
task_group: closed-loop evaluation / Isaac Sim batch analysis
task_outcome: success

Preference signals:
- the user repeatedly asked short status prompts like "现在呢" and "现在结果怎么样" -> future updates should be concise and state the current counts, not just narrate plans
- when the user later asked where the videos are, that implies video directory paths and counts matter as part of the answer
- the user’s doc-correction pattern suggests batch results should be evidence-backed with artifact paths and codec checks

Reusable knowledge:
- the policy server for the 30,000-step local checkpoint listened on `127.0.0.1:12317`; an earlier `12319` mismatch caused a start failure, so a server-health preflight was added to the launcher
- `locked_arms` finished at 100/100 with `pick=88`, `place=86`, `final=86`, `strict=0`; all 100 videos were H.264 and had `tmp=0`
- `full_policy` finished at 100/100 with `pick=48`, `place=34`, `final=34`, `strict=0`; all 100 videos were H.264 and had `tmp=0`
- `comparison.json` stored the cross-condition comparison; it showed locked_arms beat full_policy by 52 percentage points on relaxed final-task success (`86%` vs `34%`)
- unified video validation over both condition roots returned `UNIFIED_MP4_H264 total=200 bad=0`
- batch video layout was `0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/videos/{locked_arms,full_policy}` with files like `episode_000_dual_view.mp4`

Failures and how to do differently:
- the first full-batch attempt used a stale port and needed a preflight fix before Isaac Sim startup
- parallel startup had previously hit a Vulkan allocation failure; serial execution was the stable workaround
- do not finalize while `.tmp.mp4` files remain or while result counts are still changing

References:
- `0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/reports/locked_arms.json`
- `0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/reports/full_policy.json`
- `0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/comparison.json`
- `0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/videos/locked_arms/episode_000_dual_view.mp4`
- `0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/videos/full_policy/episode_000_dual_view.mp4`

### Task 3: video locations

task: answer where the generated batch videos live
task_group: artifact location lookup
task_outcome: success

Preference signals:
- when the user asked "视频都在哪里" -> answer with exact paths and counts, not a vague summary

Reusable knowledge:
- the batch video root is `/home/wangyukun/ubt_isaac_sim_ws/0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/videos/`
- condition subdirectories are `locked_arms/` and `full_policy/`
- each episode file is named `episode_000_dual_view.mp4` through `episode_099_dual_view.mp4`
- total batch video size was about 313 MB

References:
- directory list from `find .../videos -maxdepth 2 -type d`: root + `videos/full_policy` + `videos/locked_arms`
- counts from `find .../videos/locked_arms -name '*.mp4' | wc -l` -> `100`; same for `full_policy`
- total MP4 count across both condition roots: `200`

## Thread `019fd603-3375-7193-8c3d-85803452d066`
updated_at: 2026-08-13T03:15:04+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/08/06/rollout-2026-08-06T15-39-21-019fd603-3375-7193-8c3d-85803452d066.jsonl
rollout_summary_file: 2026-08-06T07-39-21-pkWy-utars_sdg_autonomous_recovery_audit_and_same_shelf_grasp_qua.md

---
description: Audit of UTars SDG recovery implementation plus same-shelf grasp-quality acceptance work; key takeaway is that the system has a real but bounded state-aware recovery/replan path, not a general self-estimating correction algorithm. The rollout also established a 10-attempt same-shelf acceptance record, updated experiment docs, and rejected several unsafe/partial natural recordings that should not be mislabeled as success.
task: audit + implement same-task auto-correction for UTars SDG auto collection
 task_group: /home/wangyukun/ubt_isaac_sim_ws
 task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: RecoverySupervisor, HandlingMultiBoxScenarioShelfAutoCollect.py, natural_execution_correction, intervention_video, H.264 MP4, same_shelf_grasp_quality_recovery, state-aware recovery, replan, bounded controller, safety rejection, natural randomization, accepted recovery, video metadata
---

### Task 1: Audit recovery implementation vs. true automatic correction

task: inspect referenced recovery thread and determine whether it is a real in-task auto-correction mechanism or just reset-and-retry
task_group: SDG recovery audit
task_outcome: success

Preference signals:
- when the user asked `你看一下这个thread的实现，是不是有问题，我想实现的是自动数采里面的算法自动纠错机制` -> future audits should answer directly whether the implementation truly corrects inside the same task flow, not merely whether it retries after failure
- the user’s earlier recovery preference (`不是丢弃然后重新开始，而是真的有纠正功能，如果规划有问题可以重新规划`) continues to imply in-task recovery / planner re-entry rather than whole-scene reset

Reusable knowledge:
- `HandlingMultiBoxScenarioShelfAutoCollect.py` does not just discard and restart; it keeps the simulator state, discards the failed buffer, starts a new recovery episode, and resumes from the stabilized failure state
- recovery decisions are bounded and state-driven in `sdg_utils/recovery/recovery_supervisor.py`; they classify by stage/reason and remeasure contact/support/tilt/force/speed before allowing replan
- accepted natural execution recovery explicitly clears the sampled command bias (`command_bias_m -> [0,0,0]`) after acceptance, so this is not a general self-estimating correction model

Failures and how to do differently:
- do not describe this as a general autonomous self-correcting algorithm; it is a rule-driven bounded recovery controller with hand-authored failure classes and safety thresholds
- do not rely on the final exception string alone; inspect observation fields and contact/support/tilt/force/speed state

References:
- `syntheticdatageneration/scenarios/training/HandlingMultiBoxScenarioShelfAutoCollect.py`
- `syntheticdatageneration/sdg_utils/recovery/recovery_supervisor.py`
- `natural_execution_correction` / `command_bias_m` being zeroed after accepted recovery
- successful bounded recovery behavior observed in accepted video metadata and experiment logs

### Task 2: Validate natural recovery and intervention videos

task: inspect accepted and rejected natural recovery videos/metadata; verify what counts as valid correction evidence
task_group: SDG video + acceptance validation
task_outcome: partial

Preference signals:
- the user wants actual correction evidence, not merely code or rejected attempts
- the thread makes clear that unsafe recordings should not be relabeled as success; future runs should keep that conservative default

Reusable knowledge:
- accepted intervention metadata contains explicit markers such as `failure_detected`, `recovery_started`, `replan_generated`, `recovery_execution`, `recovery_verified`, and `task_success`
- accepted video format is H.264 MP4 with dual cameras (`head_stereo_left_vla` and `camera_04`), and the metadata records actual pre/post context windows (`pre_roll_actual_seconds`, `post_roll_actual_seconds`) capped at five seconds
- the confirmed successful full correction video already exists at `syntheticdatageneration/logs/autonomous_replanning_recovery_20260810/r131_first_correction_only_recording/20260810_035248/interventions/attempt-000/recovery-01/combined.mp4`

Failures and how to do differently:
- do not deliver recordings that only partially demonstrate correction if the end-to-end task gate fails
- do not treat a recording that changes the physical trajectory and then fails later as representative success
- when the natural sample drifts outside the safety envelope, reject it rather than stretching the recovery logic to fit it

References:
- accepted full-success video: `syntheticdatageneration/logs/autonomous_replanning_recovery_20260810/r131_first_correction_only_recording/20260810_035248/interventions/attempt-000/recovery-01/combined.mp4`
- metadata path: `.../metadata.json`
- new recordings explored under `syntheticdatageneration/logs/same_shelf_grasp_quality_recovery_20260813/`
- rejected reasons observed: `pick_grasp_tilted`, `contact_force_exceeded`, `lower_box_shelf_collision`

### Task 3: Implement and verify same-shelf grasp-quality recovery acceptance

task: add/validate same-shelf grasp-quality correction logic, run natural acceptance, and update experiment artifacts
task_group: same-shelf grasp-quality recovery
 task_outcome: success

Preference signals:
- the user accepted moving toward a narrow, state-based correction path and wanted high-quality correction data rather than a generic retry hack
- the thread consistently steered toward conservative safety gating: reject dangerous states instead of forcing them into recovery

Reusable knowledge:
- the validated fast correction can level a moderately tilted grasp quickly; one report states about 10.6° -> 7.7° in 0.75 s
- the 10-attempt acceptance run produced 4 eligible recoveries, 3 final task successes, and one unsafe tilt rejection; no accepted recovery produced drops or shelf collisions
- the acceptance artifact is stored at `docs/experiments/artifacts/same_shelf_grasp_quality_recovery_acceptance_20260813.json`
- the experiment index entry was updated to `completed-with-boundary` and notes `3/4 eligible recoveries finished`

Failures and how to do differently:
- some natural samples were correctly rejected because they exceeded the safety envelope (tilt, force, or later shelf contact)
- the strengthened single-hand route was improved in design, but an independent natural replay did not re-trigger it, so do not claim independent runtime acceptance for that sub-route yet
- do not mislabel failed/new recordings as successful evidence; keep the end-to-end gate strict

References:
- `docs/experiments/EXP-20260813-utars-sdg-same-shelf-grasp-quality-recovery.md`
- `docs/experiments/INDEX.md`
- `docs/experiments/artifacts/same_shelf_grasp_quality_recovery_acceptance_20260813.json`
- verification: `58 passed in 0.11s`

### Task 4: Maintain an honest mechanism description

task: summarize the mechanism precisely without overstating capability
task_group: SDG recovery audit
 task_outcome: success

Preference signals:
- the user’s wording about `自动纠错机制` means it is important not to overstate a rule-based bounded controller as a general autonomous correction policy

Reusable knowledge:
- best default phrasing for this codebase is “state-aware bounded recovery / replanning inside the same task flow,” not “general autonomous correction”
- future audits should answer: what state is remeasured, what state is preserved, what is replanned, and what is merely logged or cleared

Failures and how to do differently:
- avoid claiming general self-correction when the implementation still hard-codes thresholds, failure classes, and correction actions
- do not use rejected or partial recordings as proof of success

References:
- `RecoverySupervisor` classification and safety gates
- `natural_execution_correction` logic in `HandlingMultiBoxScenarioShelfAutoCollect.py`
- successful accepted video + later acceptance report as the proof boundary between real recovery and rejected samples

## Thread `019feaef-a589-7830-850f-a52951e18786`
updated_at: 2026-08-12T03:06:35+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/08/10/rollout-2026-08-10T17-10-01-019feaef-a589-7830-850f-a52951e18786.jsonl
rollout_summary_file: 2026-08-10T09-10-01-Y3aK-utars_groot_n17_single_shelf_1000_anygpu_quota_block.md

---
description: GR00T N1.7 single-shelf 1000-episode finetune was redesigned from H200-only to H100/H200-any-GPU with task-level language and no tactile; the job never trained because namespace GPU quota stayed full and no Pod was ever created, while a move to ogi-pub was blocked by PVC-creation permissions.
task: GR00T N1.7 single-shelf 1000-episode finetune and Job troubleshooting
task_group: /home/wangyukun/ubt_isaac_sim_ws
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: GR00T, N1.7, single-shelf, 1000 episodes, H100/H200, anygpu, quota-block, kubectl, KubeSphere, PVC, Pending, FailedCreate, resourcequota, job-controller, task-level language, no tactile
---

### Task 1: Decide the 1000-episode training contract

task: design/plan GR00T N1.7 training on 1000 single-shelf episodes
task_group: GR00T finetune / dataset contract
task_outcome: success

Preference signals:
- when the user asked whether to make the instruction atomic/phased and whether to add tactile, then later said `以后都要h100h200都可以，不要再用h200的了` -> default future runs to H100/H200-any-GPU unless the user explicitly asks for H200-only
- when the user kept asking `怎么看进度` / `created了，怎么看进度` -> default to direct, minimal status commands and explicit current blocker/next-step reporting

Reusable knowledge:
- The 1000-episode single-shelf dataset was the relevant source for this fine-tune line.
- The collected HDF5 v3 frames did not include tactile/wrist-force observations, so tactile would require a new data contract, not a config flip.
- The adopted main-line design was task-level prompts, no tactile in the main run, and equal task mixing.

Failures and how to do differently:
- The initial H200-only route became obsolete after the user changed scheduling policy; future similar work should treat GPU-class policy as a user-controlled contract.
- The earlier held-out framing was superseded by the user’s request to use all 1000 episodes; future similar runs should explicitly restate whether validation/test partitions are folded into training.

References:
- `syntheticdatageneration/script/vla_n17_fullbody/launch_utars_v3_finetune.py`
- `syntheticdatageneration/script/vla_n17_fullbody/run_utars_v3_finetune.sh`
- `syntheticdatageneration/script/vla_n17_fullbody/convert_sdg_v3_to_groot.py`
- `docs/experiments/EXP-20260810-utars-groot-n17-single-shelf-1000.md`

### Task 2: Render and submit the training Job

task: render Kubernetes Job for 100-step smoke/resume + 50,000-step consolidation
task_group: Kubernetes/KubeSphere training submission
task_outcome: partial

Preference signals:
- when the user asked to move off H200-only and keep going in `ogi-llm` rather than `pub` -> future similar runs should prefer one direct command sequence and avoid namespace hopping until a concrete blocker is proven
- when the user later rejected H200-only scheduling -> default future runs to H100/H200-any-GPU unless explicitly told otherwise

Reusable knowledge:
- The Job manifest was validated locally, including the smoke/resume/full-step sequence and the `ANY_GPU_CHAIN_COMPLETE ... steps=50000` marker.
- A long-lived Job can remain `Running 0/1` while no Pod exists if creation is blocked by admission/quota.

Failures and how to do differently:
- H200-only and namespace-specific routes were superseded by user preference changes.
- Do not infer training progress from `Job Running` alone; check Pod existence and Job events.

References:
- `0.logs/h200_jobs/job-single-shelf-1000-50k-anygpu.yaml`
- `0.logs/h200_jobs/FINAL_SINGLE_SHELF_1000_50K_ANYGPU_APPLY.txt`
- `kubectl describe job utars-groot-n17-single-shelf-1000-50k-anygpu-r01 -n ogi-llm`
- Event snippet: `admission webhook "resourcesquotas.quota.kubesphere.io" denied the request ... exceeded quota: gpu-quota, requested: requests.nvidia.com/gpu=1, used: requests.nvidia.com/gpu=9, limited: requests.nvidia.com/gpu=9`

### Task 3: Diagnose why the Job never started

task: determine whether the Job was canceled, pending, or blocked by infrastructure
task_group: KubeSphere runtime diagnosis
task_outcome: fail

Preference signals:
- when the user asked `是不是被取消了，怎么在pub跑，现在是llm` and later `算了先不用pub了，给我命令查询训练也没有完成` -> investigate the current namespace first and treat namespace migration as a separate decision requiring storage/permission proof
- when the user asked for commands rather than explanation -> provide terse, directly runnable checks

Reusable knowledge:
- `No resources found` on Pod queries did not mean cancellation; in this rollout it meant no Pod had ever been created because quota admission blocked it.
- `kubectl describe job` events were the decisive signal.

Failures and how to do differently:
- The first `pub` idea was blocked by missing PVC creation permission and lack of an owned hot-storage PVC; do not propose a namespace switch without proving storage ownership and creation rights.
- Repeated label-based Pod queries were wasted until the admission error was inspected.

References:
- `kubectl describe job utars-groot-n17-single-shelf-1000-50k-anygpu-r01 -n ogi-llm`
- `FailedCreate ... exceeded quota: gpu-quota, requested: requests.nvidia.com/gpu=1, used: requests.nvidia.com/gpu=9, limited: requests.nvidia.com/gpu=9`
- `kubectl get pods -n ogi-pub -o custom-columns=...`

### Task 4: Check progress after 24 hours

task: verify whether training had begun or finished after a long wait
task_group: Job progress monitoring
task_outcome: fail

Preference signals:
- when the user wanted to know if training had finished, the response should distinguish Job status from Pod existence from step progress

Reusable knowledge:
- A Job can sit at `Running 0/1` for many hours while creation is repeatedly denied by GPU quota.
- In this rollout the running count reached 24h with 1,492 failed-create attempts and zero steps.

Failures and how to do differently:
- The workload never started; keep checking admission/quotas rather than logs when no Pod exists.
- If a Job burns most of its deadline while blocked, recreate it only after quota is available.

References:
- `Running   0/1   24h`
- `FailedCreate 71s (x1492 over 24h) ... exceeded quota: gpu-quota, requested: requests.nvidia.com/gpu=1, used: requests.nvidia.com/gpu=9, limited: requests.nvidia.com/gpu=9`

### Task 5: Consider migration to pub and then back off

task: explore moving the run to `ogi-pub`
task_group: namespace/storage feasibility check
task_outcome: partial

Preference signals:
- when the user asked about running in `pub`, then later said to stop using `pub`, the next default should be to prove storage/permission feasibility before switching namespaces

Reusable knowledge:
- `ogi-pub` exists and has GPU workloads, but the user could not create PVCs there and could not list resource quotas.
- The verified training PVC remained namespace-scoped to `ogi-llm-code-zzy-fs` in `ogi-llm`.

Failures and how to do differently:
- `ogi-pub` migration was blocked by permissions and storage ownership; do not move a training run there without a dedicated PVC and quota proof.
- The attempt to create `ogi-pub-code-wangyukun-fs` was forbidden, so the storage path remains blocked until an admin intervenes.

References:
- `kubectl auth can-i create persistentvolumeclaims -n ogi-pub` -> forbidden
- Attempted PVC: `ogi-pub-code-wangyukun-fs`
- Existing verified PVC: `ogi-llm-code-zzy-fs`

## Thread `01a0ad1a-3f6d-71b1-b1b4-72783845ad96`
updated_at: 2026-09-17T04:04:34+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T10-02-53-01a0ad1a-3f6d-71b1-b1b4-72783845ad96.jsonl
rollout_summary_file: 2026-09-17T02-02-53-Tj4q-disk_cleanup_0logs_raw_dataset.md

description: User-approved deletion of a 262–263GiB raw lower-shelf HDF5 dataset successfully freed about 263GiB while preserving converted training data, models, evaluation artifacts, and the policy server.
task: audit-and-clean-0logs-for-disk-space
task_group: /home/wangyukun/ubt_isaac_sim_ws disk cleanup
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: 0.logs, disk cleanup, HandlingBox_lower_hold_level_500_20260825, dataset.hdf5, converted training data, hard links, df, lsof, policy server

### Task 1: Delete confirmed raw dataset

task: remove-user-approved-raw-hdf5
task_group: local disk cleanup
task_outcome: success

Preference signals:
- When the user said "确认删除", deletion proceeded only after clarifying that the cluster held converted training data rather than a verified raw-data backup -> future cleanup should explicitly separate raw source data from derived training data and request confirmation for irreversible deletion.
- The user asked to clean unused `0.logs` content -> preserve active models, converted datasets, current evaluation results, and running services by default.

Reusable knowledge:
- The dominant removable file was `/home/wangyukun/ubt_isaac_sim_ws/0.logs/datasets/HandlingBox_lower_hold_level_500_20260825/dataset.hdf5`, 281,736,430,684 bytes, with no open process holding it.
- Deleting that single confirmed file reduced `0.logs` from about 405GiB to 142GiB and increased `/` free space from about 72GiB to 335GiB.
- Converted training data remained at `0.logs/groot_n17_old_upper_new_lower_h32_20260902/usable`; the raw source was not verified to exist elsewhere.
- `0.logs` directory totals can overstate reclaimable space because training outputs contain hard-linked/shared files. Deduplicate by inode/link count before estimating savings.
- The policy server at `http://127.0.0.1:12317/` still returned `{"status":"ready", ...}` after cleanup.

Failures and how to do differently:
- A converted dataset on cluster/PVC is not equivalent to a raw HDF5 backup. State the loss of future re-conversion and raw sensor inspection before asking for deletion.
- Do not delete by broad directory pattern when the user approves one dataset; use the exact path and verify no process is using it first.
- Do not promise 200GB from non-dataset logs alone: the audit found only about 72GiB of non-dataset `0.logs` usage, much of it active or shared.

References:
- Pre-delete check: `stat -c 'size=%s links=%h file=%n' .../dataset.hdf5`; `lsof -nP -- .../dataset.hdf5`
- Delete command: `rm -- /home/wangyukun/ubt_isaac_sim_ws/0.logs/datasets/HandlingBox_lower_hold_level_500_20260825/dataset.hdf5`
- Post-delete markers: `RAW_DATASET_REMOVED`, `CONVERTED_TRAINING_DATA_PRESENT`
- Final check: `df -hT /`; `curl -fsS --max-time 3 http://127.0.0.1:12317/`

## Thread `01a0ad22-0a18-73f0-a179-639d17ab826b`
updated_at: 2026-09-17T13:33:48+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T10-11-24-01a0ad22-0a18-73f0-a179-639d17ab826b.jsonl
rollout_summary_file: 2026-09-17T02-11-24-Sg0X-m2d_workspace_modelscope_download_verification.md

---
description: 初始化 Musics2Dance 私有工作区并完成 ModelScope 主线/复现数据下载、补缺失文件及逐文件校验；记录传输慢、私有权限、训练命名与状态边界
 task: m2d workspace bootstrap and ModelScope artifact verification
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: Musics2Dance, m2d-ws, prior-dev, Git LFS, ModelScope, SHA256, zstd, private-permissions, m2d-train, shallow-clone
---

### Task 1: M2D workspace bootstrap

task: create private m2d-ws and clone lbtwyk/Musics2Dance
 task_group: GitHub clone and local workspace setup
 task_outcome: partial

Preference signals:
- 用户说“这个m2d的权限只能给我自己开” -> 类似私有项目默认验证 ACL/权限为 owner-only。
- 用户要求训练及集群显示统一为“m2d-train” -> 后续训练配置应统一作业/容器/可控进程命名，并实际检查 `nvidia-smi`/调度器显示；本轮未完成该验证。
- 用户关心上百 GB 产物下载速度 -> 先测线路，再采用浅克隆、跳过 LFS smudge、断点续传或近端中转。

Reusable knowledge:
- 仓库：`lbtwyk/Musics2Dance`，默认分支 `prior-dev`，commit `24f4f75`。
- 工作区：`/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`。
- 香港到 GitHub 实测约 0.2–1.8 MiB/s，完整 Git pack 约 207 MiB，平均约 0.58 MiB/s；不适合大文件直传。
- 有效 clone 方式：`GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --single-branch --branch prior-dev https://github.com/lbtwyk/Musics2Dance.git Musics2Dance`。
- LFS 模型未自动下载；仓库约 8 GB LFS 对象，按需使用 `git lfs pull --include=...`。
- `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws` 已验证 owner-only：`user::rwx`, `group::---`, `other::---`。

Failures and how to do differently:
- SSH clone 首次因 `Host key verification failed` 失败，改用 `gh auth setup-git` + HTTPS。
- 并发 clone/switch 产生 `.git/index.lock`；执行 Git 操作前检查并发进程和 lock 文件。
- 代码拉取成功不等于本地/集群训练已配置；本轮没有完成 `m2d-train` 命名及训练启动验证。

References:
- `gh search repos music2dance --owner lbtwyk`
- `GIT_LFS_SKIP_SMUDGE=1 git clone --depth 1 --single-branch --branch prior-dev https://github.com/lbtwyk/Musics2Dance.git Musics2Dance`
- `getfacl -p /home/wangyukun/ubt_isaac_sim_ws/m2d-ws`

### Task 2: ModelScope downloads and verification

task: download and verify private ForeDance repro/mainline artifacts
 task_group: ModelScope private artifact transfer
 task_outcome: success

Reusable knowledge:
- Repro: `lbtwyk/musics2dance-foredance-repro`, `master`, local `modelscope/repro/`。
- Mainline: `lbtwyk/musics2dance-foredance-mainline`, `master`, local `modelscope/mainline/`。
- Final repro verification: 5725 blobs, `missing=0`, `size_bad=0`, `hashed=5725`, `hash_bad=0`。
- Mainline verification: 35 non-empty files, no missing or size mismatch; `transport-manifest.json` still says `inference_verified=false`。
- Three zstd archives passed `zstd -t`。
- Do not claim full source publication or training readiness merely because local transfer is complete; repro README still says upload is incomplete.

Failures and how to do differently:
- Initial ModelScope snapshot ended with 2 failed 404 files; query the remote file tree and retry individually.
- Remote manifest changed during download, revealing 512 newly missing files; always refresh the remote manifest after completion and re-run size/SHA256 checks.

References:
- Final check: `blobs 5725 missing 0 size_bad 0 hashed 5725 hash_bad 0`
- Mainline check: `entries 54 files 35 missing [] wrong []`
- Integrity command: `zstd -t data-finedance.tar.zst data-finedance_g1_yaw_anchor_abs_6d_rvqvae_dataset_backups.tar.zst data-finedance_g1_fkbeats.tar.zst`
- Workspace paths: `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/modelscope/{repro,mainline}`

### Task 3: Historical memory import

task: import private Isambard memory archive into local reference storage
 task_group: Codex memory migration
 task_outcome: success

Preference signals:
- 用户纠正“不是，我的意思是拉下来更新本地记忆” -> 备份同步必须先确认方向；用户要从指定私有 HF 归档下载并导入本地，而不是上传本机记忆。

Reusable knowledge:
- Source: `hf://buckets/wyksdsg/musics2dance-server-private/20260908/agents/agent-context-private.tar.gz`。
- Recovered 64 files into `/home/wangyukun/.codex/memory-imports/isambard-20260908/` without overwriting current memory.
- Current-use note: `/home/wangyukun/.codex/memories/extensions/ad_hoc/notes/20260917T100047Z-import-isambard-m2d-memory.md`。
- Archived `/lus/lfs1aip2/...` and `/home/u6og/...` paths are historical; re-check current checkout, ledger, frozen contract, and live artifacts before reuse。

References:
- `hf buckets cp hf://buckets/wyksdsg/musics2dance-server-private/20260908/agents/agent-context-private.tar.gz ...`
- `/home/wangyukun/.codex/memory-imports/isambard-20260908/`

## Thread `01a0ae92-039d-74d0-8c08-7c3a5f0d6acb`
updated_at: 2026-09-24T05:57:21+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T16-53-19-01a0ae92-039d-74d0-8c08-7c3a5f0d6acb.jsonl
rollout_summary_file: 2026-09-17T08-53-19-VgaT-lower_eval_root_cause_and_github_evidence_archive.md

---
description: Lower-shelf N1.7 v3 jitter/root-cause investigation, qualified 40-episode result, and complete main-branch evidence archival
 task: lower-shelf closed-loop inference diagnosis and evidence publication
 task_group: /home/wangyukun/ubt_isaac_sim_ws
 task_outcome: success
 cwd: /home/wangyukun/ubt_isaac_sim_ws
 keywords: N1.7, RTC, relative-actions, lower-shelf, jitter, 7-of-40, H.264, GitHub, evidence-manifest
---

### Task 1: Lower-shelf inference and execution root-cause analysis

task: Diagnose and repair jitter/drop failures in the active lower-level N1.7 closed-loop evaluation.
task_group: Isaac Sim / GR00T N1.7 RTC inference
task_outcome: partial

Preference signals:
- The user asked for “根因修复” -> trace inference/reference-state conversion, RTC timing, action execution, and physical outcome before applying smoothing or parameter-only fixes.
- The user expected complete evidence, including failures and videos -> preserve raw results and qualified interpretations, not only successful episodes.

Reusable knowledge:
- N1.7 v3 uses action horizon 32, execution/replan horizon 16, RTC overlap 16; body-joint actions are relative and must be decoded against the current state.
- RTC previous chunks belong inside `collated_inputs["inputs"]["action"]`; passing top-level `action` to `get_action` causes the known API failure.
- The follow-up success-first run completed 40 unique seeds with 39/40 pickup and 7/40 actual lower placements (17.5%); no client errors or expired requests, but no full physics trace, so model-only attribution is not proven.
- Seed reproducibility is not guaranteed: a previously successful seed later failed.

Failures and how to do differently:
- Do not equate stage placement with full completion; actual completion requires target pose, release, and no recorded drop.
- Do not rewrite a failure where final pose is valid but a process-drop flag exists; preserve original score and document ambiguity.
- `ffmpeg` was unavailable; use OpenCV/PyAV in the GR00T environment for video inspection.

References:
- `0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/`
- `.../REPORT.md`
- `.../same_shelf_lower_level/runs/full_policy/merged/n17_v3_closed_loop_results.jsonl`
- `syntheticdatageneration/scenarios/training/mixins/VlaN17V3RuntimeMixin.py`
- `syntheticdatageneration/script/vla_n17_fullbody/n17_v3_rtc_infer.py`
- Focused export validation: 59 tests passed.

### Task 2: Main-branch evidence archival

task: Publish README, source, reports, all success/failure videos, and historical repair evidence to the user’s private GitHub repository without a new Release.
task_group: GitHub research/evidence handoff
task_outcome: success

Preference signals:
- User said “就放到主分支，证据也放到repo就行不要发布” and “readme把这次作为主结果” -> use main-branch repository storage and lead README with the 7/40 result.
- User requested success/failure video identification -> maintain a 1-based episode index.

Reusable knowledge:
- Repository: `https://github.com/lbtwyk/utars-isaac-vla-pipeline`.
- README primary result: 7/40 actual completions (17.5%), 39/40 pickup; success episodes 7, 10, 17, 19, 20, 21, 25.
- Evidence root: `docs/evidence/lower-20260918/`; video index: `docs/results/lower-20260918/VIDEOS.md`.
- Final local upload receipt: `ALL EVIDENCE ON MAIN 6117badd4b7e8edbac2238a5807dcda7444771bd`; 1,456/1,456 files and hashes verified locally.
- Large uploads should use bounded commits; 400 MiB batches hit GitHub HTTP 408, while 64 MiB resumed batches completed.

Failures and how to do differently:
- A draft Release was initially created, but the user changed the requirement; delete/avoid Release and push directly to main.
- GitHub API re-fetch later failed with TLS/EOF; report this as a verification limitation rather than claiming a fresh online inventory check.

References:
- Main commit: `6117badd4b7e8edbac2238a5807dcda7444771bd`
- Final upload status: `0.logs/exports/lower-results-20260921/push_status.json`
- Final video set: 120 original streams plus 40 combined aliases; all 40 episodes retained, including 33 failures.

## Thread `01a0aea2-2d88-7ad1-93f5-dabd2b7354da`
updated_at: 2026-09-18T05:21:06+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T13-07-39-01a0aea2-2d88-7ad1-93f5-dabd2b7354da_01a0b2e9-c315-7110-a086-05d720e45b8a.jsonl
rollout_summary_file: 2026-09-17T09-10-59-kIEa-token_causal_codec_route_decision.md

---
description: New token-causal D+C codec is operationally stream-consistent but substantially worse than the old mainline; recommend stopping current-config expansion and allowing only one bounded reconstruction-first repair study.
task: decide whether to continue token-causal codec route
task_group: Musics2Dance codec evaluation and research decision
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: token-causal, D+C, FineDance, reconstruction, B71, causal-conv, codec-comparison, oracle-latent, route-decision
---

### Task 1: Token-causal codec route decision

task: decide whether current token-causal codec should replace old mainline
task_group: codec evaluation / experiment decision
task_outcome: partial

Preference signals:
- The user asked for “深度分析，给我个结果要不要继续这条路线” -> similar future work should provide a clear investment recommendation, not only report metrics.
- The workflow expects bounded scientific claims and explicit user ownership of route decisions -> distinguish checkpoint comparison from architecture rejection and do not silently change the experiment route.

Reusable knowledge:
- Across all 18 held-out FineDance tracks, old own-history native MSE was `0.008143`; new seeds at 100k were `0.05594–0.05931`, about `7.05x` worse. Each new seed lost on every track.
- 50k→100k test MSE improvement was only `0.9%`, `2.8%`, and `5.6%` for seeds 1234/2345/3456. More training of the same configuration was not supported as the remedy.
- Streaming implementation is consistent: full versus 8-frame incremental decoding max absolute difference `4.53e-6`; warmup-local versus full-sequence max difference `2.86e-6`.
- The model also had poor training-set reconstruction: first-512-frame mean joint error about `7.22°`, so the issue is not only held-out generalization.
- Optimizing latent inputs into the frozen decoder with ground-truth motion improved four probe samples by roughly `54–64%`. This is answer-assisted diagnosis only, but suggests the decoder has unused representational capacity and the encoder/objective/information allocation should be investigated.
- New codec removes the old model’s explicit B71 boundary-state conditioning while retaining a 16D latent. This plausibly increases information burden, but no isolated experiment proves it is the cause.

Failures and how to do differently:
- Do not call the result a causal architecture ablation: old/new training budgets, windows, anchor behavior, initialization, and boundary inputs differ.
- Do not treat smoother motion or lower jerk as improvement when reconstruction and foot-skate metrics are worse.
- Do not keep extending training based only on decreasing training loss.
- Do not treat oracle-latent optimization as deployable evidence.

References:
- `runs/token_causal_dc/mainline-comparison/comparison.json`
- `runs/token_causal_dc/mainline-comparison/REPORT.md`
- `runs/token_causal_dc/mainline-comparison/ROUTE_DECISION.md`
- `runs/token_causal_dc/mainline-comparison/diagnosis.json`
- `runs/token_causal_dc/mainline-comparison/latent-probe.json`
- `eval/compare_token_causal_mainline_codec.py`
- Exact result handle: `wins {'new_1234': 0, 'new_2345': 0, 'new_3456': 0}`

## Thread `01a0b26e-aa7e-7512-9bdc-a5d06f11a5e3`
updated_at: 2026-09-18T08:57:37+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T10-53-12-01a0b26e-aa7e-7512-9bdc-a5d06f11a5e3.jsonl
rollout_summary_file: 2026-09-18T02-53-12-6KD9-m2d_modelscope_fullsong_mrt2_cache_sync.md

description: 完成 Musics2Dance token-causal generator 所需全曲 MRT2 条件缓存的下载、重算、全量校验和真实训练入口预检；正式生成器训练未启动
 task: ModelScope full-song MRT2 cache synchronization and generator readiness
 task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 task_outcome: success
 cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 keywords: ModelScope, MRT2, FutureMusicStore, token_causal_fullsong, zstd, cutoff, cache manifest, generator preflight, exact resume, paired audio motion length

### Task 1: Build and verify full-song MRT2 cache

task: Synchronize private ModelScope artifacts and make the token-causal generator cache trainable.
task_group: Musics2Dance ModelScope/MRT2 cache workflow
task_outcome: success

Preference signals:
- when the user asked to upload and download simultaneously -> monitor remote inventories in parallel, download only missing/changed files, and leave long transfers running in the background.
- when reporting readiness, distinguish downloaded assets, runnable local setup, formal training launch, and scientific acceptance; never infer the latter from the former.
- user prefers direct Chinese progress updates with concrete counts, blockers, and next actions.

Reusable knowledge:
- Final cache: `modelscope/repro/foredance-mainline-20260912/generator/condition_caches/token_causal_fullsong/`.
- Coverage: 201 tracks total, 183 train / 18 test; 95,411 train cutoffs and 6,399 test cutoffs.
- All eight full-song archives passed size checks and `zstd -t`; extracted cache contains 1619 files.
- Provenance totals: legacy 93,874 rows, prefix 3,015 rows, newly computed 4,921 rows.
- Five tracks had audio shorter than motion; builder now uses paired length `min(raw_motion_length, floor(audio_frames*30/sample_rate)+15)` and never pads or fabricates data.
- `FutureMusicStore` readback passed for all 201 tracks and 603 boundary probes; all hidden states were finite.
- Generator preflight with the seed-1234 codec passed 0/2-worker loaders, 16 real samples per loader, 4 finite updates, and exact resume error `0.0`.
- Formal generator training was not launched; cache and execution readiness only, not quality acceptance.

Failures and how to do differently:
- Initial known ModelScope repos were complete but contained only prefix coverage; ask for alternate private repositories before concluding local recomputation is required.
- Initial builder failed on audio/action length mismatch; always derive required cutoffs from physically available audio plus the motion future horizon.
- `.venv311` is under `Musics2Dance`, not the workspace root. Use `Musics2Dance/.venv311/bin/...` when operating from the parent directory.
- `pytest` was unavailable in the environment; do not report pytest success. Use the verified cache reader, manifest digest, entrypoint preflight, and `py_compile` evidence actually available.

References:
- `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/modelscope/repro/foredance-mainline-20260912/generator/condition_caches/token_causal_fullsong/manifest.json`
- `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/runs/token_causal_dc/full-cache-preflight-20260918/generator/preflight.json`
- `Musics2Dance/scripts/build_token_causal_fullsong_music_cache.py`
- `Musics2Dance/train_g1_token_causal_generator.py`
- `modelscope/logs/token-causal-fullsong-verify-20260918.log`
- Top manifest SHA256: `9afc8c13f1483df1fa8e5eacd100042a697e927075d511e2d0c77fe49277a769`

## Thread `01a0b2fe-587e-7a60-b6b1-ebaf4a49312e`
updated_at: 2026-09-23T16:46:46+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T00-05-52-01a0b2fe-587e-7a60-b6b1-ebaf4a49312e_01a0c4b7-742e-7c20-bc9f-f20250f95eea.jsonl
rollout_summary_file: 2026-09-18T05-30-08-lolw-omg_root_rotation_audit_and_split_stability_training.md

---
description: OMG 根旋转突变已被证明来自上游机器人动作数据/重定向阶段而非本地读取或6D转换；随后将 Pending 双卡稳定性训练拆成两个单卡 Job，完成验证和热盘交付但尚未提交
 task: omg_root_cause_audit_and_single_gpu_stability_split
 task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 task_outcome: partial
 cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
 keywords: OMG, root-rotation, Parquet, SO3, 6D, quaternion, retargeting, causal-codec, KubeSphere, hot-storage, shard, split-job
---

### Task 1: OMG 根旋转异常根因调查

task: trace OMG motion discontinuities through raw Parquet, loader, quaternion/6D conversion, and upstream human-reference data
task_group: OMG data provenance and causal-codec input audit
task_outcome: partial

Preference signals:
- 当用户追问“根因调查”时，不能只报告异常比例；应沿原始文件、episode/frame 索引、读取器、旋转转换、切片边界和上游人体参考逐层验证。
- 用户以“质量更好才训练”为条件；审计必须明确是否满足启动门槛，不能把数据下载完成等同于训练授权。

Reusable knowledge:
- 全量 OMG audit: 9/9 packages, 84,159,903,223 bytes, 26,149 clips, 10,541,226 frames.
- Independent provenance audit reproduced all 49 >90-degree events across 42 episodes directly from official Parquet rows. Loader max error was 0; action-to-next-state max error was 0; timestamp step error was ~3.3e-6 s; SciPy versus independent dot-product rotation error was ~1.25e-10 degrees; encoded 6D versus source step error was ~1.47e-5 degrees.
- Relevant official Parquet files matched upstream SHA256. Therefore the observed jumps are not caused by local file corruption, episode concatenation, the loader, quaternion order handling, or conversion to 6D.
- FineDance 047: robot/G1 source has ~93.18° root jump while nearby original human motion is ~5.49°; this localizes at least that anomaly to upstream human-to-robot retargeting/data generation. AIOZ episode 9740 has a ~175.40° jump.
- Training comparison: FD-G1 root >90° = 0.130 per 100k adjacent transitions; OMG O-Dance = 0.416 per 100k. Joint >90° events are lower in OMG (15.02 vs 35.56 per 100k), but root quality is worse, so the user’s conditional “only train if better” gate was not met.
- OMG uses `observation.state` qpos36: position3 + root quaternion wxyz4 + 29 joints. Project conversion changes only boundary order to xyzw; causal codec training then uses 6D representation. 6D improves neural rotation parameterization but does not remove source discontinuities or prevent decoder outputs from approaching degenerate basis vectors.
- 79.26% of OMG clips are shorter than the existing 316-frame causal window; a future OMG causal route needs an explicit short-episode/context contract and must not silently fabricate history or simply swap the data path.

Failures and how to do differently:
- Do not attribute raw-data jumps to the 6D representation without checking source SO(3) angles before and after encoding.
- Do not smooth/filter/delete OMG motion globally based on a threshold; retain the raw baseline and repair only with an explicit approved contract.
- Do not start raw O-Dance causal training from the current 316-frame FineDance path; short-clip handling and source-quality repair are unresolved.

References:
- `modelscope/omg-download-audit/quality/summary.json`
- `modelscope/omg-download-audit/quality/episodes.jsonl`
- `modelscope/omg-download-audit/quality/root_events_over90.jsonl`
- `Musics2Dance/runs/causal_native_trajectory/cluster-readback-20260921/root-provenance/provenance.json`
- `Musics2Dance/eval/audit_root_rotation_provenance.py`

### Task 2: Split Pending stability training into two single-GPU Jobs

task: replace pending `m2d-causal-stability-2h` with two independent single-GPU jobs while preserving history 3H and reusing completed music
task_group: KubeSphere launch/delivery operations
task_outcome: partial

Preference signals:
- User explicitly authorized direct adjustment without more queue diagnosis or confirmation and required: keep running `m2d-causal-history-3h-llm-only`, disable the pending two-GPU stability job, preserve budgets/config, do not recompute music, and provide complete launch plus two live-log commands.
- Future agents should report “prepared/readback-verified/submitted/running” separately; this rollout prepared and uploaded the replacement but did not submit it.

Reusable knowledge:
- Shard A: `cof_continue`, `decoder_continue`, `decoder_phase`; shard B: `cof_rollout_stability`, `decoder_rotation`, `decoder_rotation_phase`.
- Each arm remains at 6250 updates with original trainer settings; each replacement Job requests 1 GPU, 12 CPU, 64GiB and writes to separate `results/shard-0` or `results/shard-1` output roots.
- `scripts/run_g1_stability_suite.py` supports `--shard 0|1`; `scripts/watch_g1_stability_hot.py --split` merges two three-arm completion receipts and rejects missing/duplicate arms.
- Verification passed: `tests/test_g1_stability_split.py` (2 tests), bash syntax, mocked apply flow. The mocked apply deleted only `m2d-causal-stability-2h` and created `m2d-causal-stability-1h-a/b`; it did not touch `m2d-causal-history-3h-llm-only`.
- Split launch was uploaded and readback-verified. The cluster was not accessible from the local host; no deletion, submission, or training start was verified.
- Completed shared music must be reused: 205 tracks, 4,368,404,480 bytes, SHA256 `112319c3acfd3f35ab354ab4b73535d9ba34c9fa5a1f8af8414c341012d914ae`; no forecast recomputation.

Failures and how to do differently:
- Never claim the pending Job was actually deleted or replacement Jobs started when only the KubeSphere script was prepared. The user must paste the hot-storage launch entry in a cluster terminal.
- Preserve the exact existing history Job and only delete the explicitly named obsolete stability Job, after archiving/guarding as implemented by `APPLY_SPLIT_1H.txt`.

References:
- `runs/causal_native_mrt2/split-single/readiness.json`
- `runs/causal_native_mrt2/split-single/hot-receipt.json`
- `../cluster-transfer/EXP-20260922-fd-causal-stability-suite/release-split/APPLY_SPLIT_1H.txt`
- `../cluster-transfer/EXP-20260922-fd-causal-stability-suite/release-split/LIVE.txt`
- `kubectl logs -f --timestamps --tail=50 -n ogi-llm job/m2d-causal-stability-1h-a`
- `kubectl logs -f --timestamps --tail=50 -n ogi-llm job/m2d-causal-stability-1h-b`

## Thread `01a0b322-0e7f-7213-b849-6b547c81ba6a`
updated_at: 2026-09-18T08:23:58+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T14-09-08-01a0b322-0e7f-7213-b849-6b547c81ba6a.jsonl
rollout_summary_file: 2026-09-18T06-09-08-mIeS-38d_amplitude_diagnosis_github_evidence_handoff.md

description: 最新38D主线动作幅度诊断完成，并将无视频的实验原始证据交给GitHub/Web决策
 task: diagnose_latest_38d_amplitude_vs_34d_and_publish_evidence
 task_group: Musics2Dance research audit and GitHub handoff
 task_outcome: success
 cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 keywords: 38D, 34D, yaw-anchor, B71, AM-FHC, AJ-FHC, amplitude, autonomous-generation, codec-reconstruction, Issue-49, GitHub, evidence-release, Web-decision

### Task 1: 34D/38D动作幅度与生成阶段诊断

task: diagnose_latest_38d_amplitude_vs_34d_and_generation_stage
task_group: Musics2Dance amplitude audit
task_outcome: success

Preference signals:
- 用户说问题来自“最新的 38d 主线”并要求判断“是38d的问题还是训练出了问题” -> 必须把表示/codec还原、生成训练、音乐条件、历史状态、渲染分层验证，不能只根据综合分数下结论。

Reusable knowledge:
- `g1_yaw_anchor_abs_6d` 38D codec 可保留大动作：18首重建 range/speed 为 97.3%/97.2%，优于34D的96.6%/90.6%；低幅度主要出现在自主生成，不是表示容量或渲染缩放。
- 主诊断覆盖18首、24秒统一窗口、3采样seed、model-preroll/K64两种启动协议，共324段；另有57段控制、18首codec重建、324 fixed-landmark检查。
- 全体joint range/speed差异区间跨零，不支持“38D全面塌缩”；但root-local手腕/脚踝活动范围更一致偏小，model-preroll AM−34D为-6.3pp CI[-10.1,-2.2]，AJ为-5.3pp CI[-8.2,-2.7]，各15/18首低于34D。
- 036是稳定失败例：34D 53.0%/42.3%，38D AM 28.1%/15.0%，AJ 38.5%/26.0%；063证明38D仍能产生大动作，098说明范围不小也可能速度不足。
- 真实未来音乐特征和真实初始历史均不能充分修复036；无音乐条件方向不一致。036低活跃在AM/AJ三个训练seed中重复。
- 生成q0重复率/残差RMS等只应作为机制线索，不可当作跨表示直接质量分数。真实状态注入虽恢复段内幅度但产生约5倍边界速度跳变，不是有效修复。
- 当前最稳妥解释是自主生成阶段对部分音乐产生保守动作，并在长时自回归历史中延续；尚不能唯一归因于38D维度、具体loss或训练步数。保留38D完整朝向目标，下一步应由用户/Web选择一个generator-side受控干预或严格34D/38D训练消融。

Failures and how to do differently:
- 原始交接包先包含视频；用户说“视频不需要，其他的日志啥的可以”后，已从release和文档中移除视频/gallery。未来先确认视频上传偏好。
- GitHub大附件通过代理上传多次超时；最终使用直连/绕过代理并验证GitHub asset digest。大文件交接应避免不稳定代理、逐个检查size/digest。

References:
- `docs/experiments/reviews/EXP-20260904-v6f-aq-tmmr-direct-condition-amplitude-audit-20260918.md`
- `runs/amplitude_audit_20260918/analysis/summary.json`
- `runs/amplitude_audit_20260918/analysis/all_324_clips.csv`
- `runs/amplitude_audit_20260918/completion.json`

### Task 2: GitHub/Web实验交接

task: publish_amplitude_audit_and_request_web_decision
task_group: GitHub research handoff
 task_outcome: success

Preference signals:
- 用户要求“实验 证据要传上”，但不需要视频 -> 上传测量、日志、脚本、动作记录、静态图和报告；不上传视频。
- 用户要求“让web端看到所有信息然后给出决策” -> 交接必须提供可读报告、原始证据下载和明确待决策选项，不自动启动训练或替换主线。

Reusable knowledge:
- 私有 release `https://github.com/lbtwyk/Musics2Dance/releases/tag/amplitude-audit-20260918`：13个无视频附件，约206MB，digest已核对。
- Web决策入口为 Issue #53：`https://github.com/lbtwyk/Musics2Dance/issues/53`，标签`researchos:waiting-web`。
- 文档PR为 #54：`https://github.com/lbtwyk/Musics2Dance/pull/54`，分支`codex/38d-amplitude-audit-20260918`，最终commit `1894755f16caf244b405be8d8a831bffbbe5c6e4`。
- 原Issue #49已交叉链接：`https://github.com/lbtwyk/Musics2Dance/issues/49#issuecomment-5727284633`。
- ledger保持原实验`closed/accepted`；无新训练、无主线切换、无科学结论改变。

Failures and how to do differently:
- commit因缺少git身份失败，使用`Yukun Wang <186519092+lbtwyk@users.noreply.github.com>`完成。
- 上传大附件时代理连接导致超时；直连API/禁用代理后完成并验证digest。

References:
- PR: `https://github.com/lbtwyk/Musics2Dance/pull/54`
- Issue: `https://github.com/lbtwyk/Musics2Dance/issues/53`
- Release: `https://github.com/lbtwyk/Musics2Dance/releases/tag/amplitude-audit-20260918`
- Commit: `1894755f16caf244b405be8d8a831bffbbe5c6e4`

## Thread `01a0b378-0fdd-7bb1-8c60-f051ce14156c`
updated_at: 2026-09-24T15:39:53+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T15-43-05-01a0b378-0fdd-7bb1-8c60-f051ce14156c.jsonl
rollout_summary_file: 2026-09-18T07-43-05-YZAg-research_workflow_preflight_and_github_handoff_alignment.md

---
description: Clarified research workflow: sync artifacts independently, automate approved training checks, and distinguish lightweight local preflight from cluster resource-selection preflight
 task: research-workflow-preflight-and-handoff
 task_group: /home/wangyukun/research-loop-workflow + /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
 task_outcome: success
 cwd: /home/wangyukun/research-loop-workflow
 keywords: github-research-handoff, repository-sync, issue-pr, training-check-acceptance, preflight, local-gpu, slurm, kubernetes, training-efficiency
---

### Task 1: Repository sync versus issue/PR discussion

task: Keep GitHub artifacts readable for Web without turning every push into a decision request
task_group: research workflow and GitHub handoff
task_outcome: success

Preference signals:
- The user said: “有阶段性结果再更新issuespr，很多时候是把产物证据更新repo，web可以读然后分析就可以了” -> push useful code, documents, logs, and evidence independently; update issue/PR discussion only for stage results or decisions.
- The user said: “不要规则越堆越多” -> prefer one concise governing principle over many layered workflow rules.

Reusable knowledge:
- Repository synchronization and issue/PR discussion are separate actions. A repository push is not a scientific decision request.
- The concise rule is: sync finished outputs when ready so Web can read them; update issue/PR discussion for stage results or needed decisions, not every push.
- The handoff skill and workflow were updated in the upstream source and installed copy.

Failures and how to do differently:
- The first revision coupled complete result packaging, branch push, and issue/PR update too tightly. The user corrected this; preserve independent artifact sync.

References:
- Upstream handoff skill: `/home/wangyukun/research-loop-workflow/packs/core/skills/github-research-handoff/SKILL.md`
- Project workflow: `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/docs/research/WORKFLOW.md`
- Verified commits: `research-loop-workflow` `b8cd1966d8e5b0686e0e9a54b42870a14ac18f58`; `Musics2Dance` `9a9ea48156e8a747de372ece8190fed11caf0b47`

### Task 2: Automatic approved-training lifecycle

task: Make training checks continue through operational completion and formal reporting
task_group: training-check-acceptance core workflow
task_outcome: success

Reusable knowledge:
- `training-check-acceptance` is a core skill shared by local GPU, Slurm, and Kubernetes workflows.
- An approved `check` authorizes monitoring, same-contract repair/resume, remaining declared stages, evaluation, rendering, analysis, evidence updates, and formal stage reporting.
- Pause only for a scientific route/contract/claim/outcome decision or an external blocker that cannot be repaired locally.
- Training completion alone does not close the experiment; declared downstream stages and evidence remain required.

Validation:
- Core ledger tests: `Ran 4 tests ... OK`.
- Installation routing passed for `--core`, `--local`, `--slurm`, `--kubernetes`, combined installation, and personal installation.
- Skill validation passed for core and installed copies.

References:
- `/home/wangyukun/research-loop-workflow/packs/core/skills/training-check-acceptance/SKILL.md`
- `/home/wangyukun/research-loop-workflow/packs/core/skills/training-check-acceptance/references/report-template.md`
- Installed copy: `/home/wangyukun/.codex/skills/training-check-acceptance/SKILL.md`

### Task 3: Local and cluster preflight split

task: Define lightweight local full-path validation and cluster resource-selection plus exact launch proof
task_group: preflight and training efficiency
 task_outcome: success

Preference signals:
- The user explicitly required that local preflight remain: “本地也要preflight，只不过是轻量化的验证全流程能跑通不会有error” -> never treat local preflight as optional merely because Slurm has a formal preflight.
- The user defined cluster preflight as both correctness and performance/configuration selection: “集群的preflight是列出来正常的和一些激进的适配训练卡训练配置，这样可以选择最快的训练配置” -> compare normal and aggressive viable shapes before selecting the formal launch.

Reusable knowledge:
- Local preflight: run a short real-data path through one training update, checkpoint save/reload, and each declared downstream entrypoint on tiny isolated inputs; verify exit status and readable outputs. It proves the path runs without errors, not quality or full-scale throughput.
- Cluster preflight: compare ordinary and viable faster resource shapes by queue wait plus time to declared results, while keeping scientific settings fixed; then execute the exact-command correctness proof for the selected shape on the target cluster. Keep the ordinary shape as fallback.
- Slurm target-cluster GPU proof uses `slurm_interactive`; legacy `local` mode only proves direct-GPU execution and does not prove Slurm execution.
- KubeSphere requires a validated Job and short real training/checkpoint/downstream run on the target cluster, with Pod, logs, quota fit, and result path recorded.
- The ledger’s built-in `preflight` command remains Slurm-specific; local and Kubernetes use their compute module’s preflight path and record evidence in the same experiment ledger.

Failures and how to do differently:
- Initial docs said direct-attached GPU work only needed changed-seam checks and early formal-run evidence. This was insufficient for the user’s required local full-path proof; future edits must preserve the explicit lightweight local preflight.

Validation:
- `git diff --check` passed.
- Shell syntax and Python compilation passed.
- Core ledger tests passed.
- Skill validation passed for `research-experiment-spec`, `training-check-acceptance`, and `slurm-training-optimizer`.
- Install checks confirmed local, Slurm, and Kubernetes preflight docs route correctly.

References:
- Local module: `/home/wangyukun/research-loop-workflow/packs/local/docs/LOCAL_TRAINING.md`
- Slurm correctness preflight: `/home/wangyukun/research-loop-workflow/packs/slurm/docs/PREFLIGHT.md`
- Slurm efficiency selection: `/home/wangyukun/research-loop-workflow/packs/slurm/docs/TRAINING_EFFICIENCY.md`
- Kubernetes module: `/home/wangyukun/research-loop-workflow/packs/kubernetes/docs/KUBERNETES.md`
- M2D project preflight contract: `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/docs/research/modules/TRAINING_PREFLIGHT.md`
- M2D project efficiency module: `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/docs/research/modules/TRAINING_EFFICIENCY.md`
- Verified remote commits: `b8cd1966d8e5b0686e0e9a54b42870a14ac18f58` and `9a9ea48156e8a747de372ece8190fed11caf0b47`

## Thread `01a0b383-87d0-7722-bce0-88c24dda6567`
updated_at: 2026-09-18T07:55:57+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T15-55-36-01a0b383-87d0-7722-bce0-88c24dda6567.jsonl
rollout_summary_file: 2026-09-18T07-55-36-ovtB-todesk_ubuntu_x86_64_version_selection.md

description: 为 Ubuntu 22.04 x86_64 环境选择正确的 ToDesk Linux 安装包；已确认应使用 Debian/Ubuntu/Mint (x64) 的 amd64 .deb
任务: select_todesk_package_for_ubuntu_x86_64
task_group: linux-software-installation
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: ToDesk, Ubuntu 22.04, x86_64, amd64, deb, Linux

### Task 1: 选择 ToDesk Linux 安装版本

task: select_todesk_package_for_ubuntu_x86_64
task_group: linux-software-installation
task_outcome: success

Preference signals:
- 用户直接询问“本级安装todesk选什么版本”，倾向于先根据本机系统和架构给出明确的版本选择，而不是罗列所有下载选项。

Reusable knowledge:
- 当前机器经检测为 Ubuntu 22.04.5 LTS，CPU 架构为 `x86_64`。
- ToDesk 在 Ubuntu/Debian/Mint 上应选择 Linux 的 Debian/Ubuntu/Mint (x64) `.deb` 包；文件名中的 `amd64` 与本机 `x86_64` 匹配。
- 不应选择 ARM64 包或 RPM 包。

Failures and how to do differently:
- 本次未发现失败；通过先检测 `uname -m` 和 `/etc/os-release`，避免仅凭发行版名称猜测架构。

References:
- 检测命令：`uname -m; cat /etc/os-release`
- 检测结果：`x86_64`、`Ubuntu 22.04.5 LTS`、`VERSION_ID="22.04"`
- 官方 Linux 下载页：`https://docs.todesk.com/linux.html`
- 官方当前 Linux 版本搜索结果：`todesk-v4.8.6.2-...-amd64.deb`

## Thread `01a0b8c5-6493-7560-9a92-78a194682cf3`
updated_at: 2026-09-24T06:27:16+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T16-58-01-01a0b8c5-6493-7560-9a92-78a194682cf3_01a0c32f-be1c-71f1-bdf7-6d94456d54fa.jsonl
rollout_summary_file: 2026-09-19T08-25-39-vb59-kubernetes_gpu_quota_and_committed_trajectory_cost_audit.md

---
description: Diagnosed an ogi-llm GPU quota block and audited slow committed-trajectory GAN/ES training; recovery Job eventually ran, and measured padding/trajectory inefficiency was documented without changing the live experiment
task: gpu-quota-diagnosis-and-committed-trajectory-training-cost-audit
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: Kubernetes, ogi-llm, gpu-quota, nvidia.com/gpu, m2d-commit-trajectory, Self-Forcing, DMD2, EAR, DPPO, burn-in, GAN, energy-score, gradient-truncation
---

### Task 1: Kubernetes GPU quota diagnosis

task: inspect blocked recovery Job and identify safe cleanup candidates
task_group: ogi-llm Kubernetes operations
task_outcome: success

Preference signals:
- When the user asked who is running and whether their own problematic jobs could be cleared, this indicates ownership-aware inspection should precede deletion; do not blindly delete Jobs or Pods.

Reusable knowledge:
- `m2d-commit-trajectory-3h-fast-r1` initially had `0 Active / 0 Succeeded / 0 Failed`; repeated events said `exceeded quota: gpu-quota, requested: requests.nvidia.com/gpu=3, used: requests.nvidia.com/gpu=8, limited: requests.nvidia.com/gpu=9`.
- Inspect nonterminal Pods with full JSON resource dictionaries. `custom-columns` is unreliable for dotted keys such as `nvidia.com/gpu`.
- Later output showed `m2d-commit-trajectory-3h-fast-r1-5wfq2` Running with 3 GPUs. Active GPU requests were user causal-native=2, user recovery=3, colleague `yiming-ma-4gpu-512gi-data-code1-shell-job-qwvp7`=4, totaling 9. The quota block had cleared.
- Keep a waiting Job; it can retry after quota becomes available. Old Suspended/Failed/Complete Job records are not evidence of active GPU consumption.

Failures and how to do differently:
- Treat early FailedCreate events as historical if a later Pod listing proves admission succeeded. Do not delete healthy work to fix an already-cleared quota issue.
- Do not use job names or low instantaneous utilization as proof of abnormality; inspect requested resources, `author`, owner controller, command/process state, and health.

References:
- `kubectl describe job m2d-commit-trajectory-3h-fast-r1 -n ogi-llm`
- `kubectl get pods -n ogi-llm --field-selector='status.phase!=Succeeded,status.phase!=Failed' -o jsonpath=...`
- `kubectl get jobs -n ogi-llm -l author=wangyukun -o wide`

### Task 2: Committed-trajectory GAN/ES cost and design audit

task: determine whether slow GAN/ES training is caused by excessive updates, implementation inefficiency, or immature design
task_group: Musics2Dance committed-trajectory post-training
task_outcome: success

Preference signals:
- The user explicitly requested comparison with mature papers and code and asked whether the issue is too many steps, insufficient optimization, or immature design. Future work should distinguish measured local facts from proposed scientific redesigns.
- Preserve the original 183 training/18 test tracks and 6250 additional updates per arm; do not reduce the budget based only on elapsed time.
- Keep live training and experiment budgets unchanged unless the user approves a method change.

Reusable knowledge:
- `train_g1_commit_trajectory.py::objective_batch` runs 48 source groups/update with 4 particles; scored generation has 16 commits, and each commit uses 10 residual denoising steps. `model/g1_commit_trajectory.py::CommittedRollout.step` uses checkpointed differentiable plans during scored training.
- Real-data CPU reconstruction of the first 350 updates found burn-in counts 0/16/32/64 = 7603/3329/3140/2728 groups; mean useful burn-in=19.5438; every batch had max burn-in=64. Discarded burn-in particle-plan forwards=69.46%; nominal discarded particle-plan forward work including startup/scored generation=46.80%. This is a work-count estimate, not a promised wall-time speedup.
- GAN performs per-group critic calls and discriminator backward work; ES pairwise distance computation is already batched, so ES slowness is mainly trajectory generation.
- No evidence proved 6250 updates are excessive, H100 hardware is at fault, or the run has failed scientifically.
- Audit artifact: `docs/research/COMMITTED_TRAJECTORY_TRAINING_COST_AUDIT_20260921.md`; evidence directory: `runs/commit_trajectory/design-audit-20260921/`; owner snapshots: `owner-progress.json`; source archive manifest: `sources/source-manifest.json`.
- Self Forcing is the closest mature reference: few-step rollout plus stochastic gradient truncation and detached prior context. DMD2 is a few-step/one-step distillation design, EAR shows efficient two-sample Energy Score for a different feed-forward objective, and DPPO separates rollout collection from later optimization under a different RL objective.

Failures and how to do differently:
- Do not conclude “6250 is too many” from remaining-time estimates alone; compare learning curves and quality against both update/source exposure and GPU time.
- Do not directly change 10 denoising steps to 4 or cache generated samples for repeated optimization without treating it as a new scientific method.
- A naive burn-in compaction changes RNG consumption and may affect exact resume; preserve per-sample random streams and validate gradients/checkpoint recovery.
- Naively batching GAN critic work may change spectral-normalization buffer evolution; define intended semantics before changing it.

References:
- `docs/research/COMMITTED_TRAJECTORY_TRAINING_COST_AUDIT_20260921.md`
- `runs/commit_trajectory/design-audit-20260921/measure_work.py`
- `runs/commit_trajectory/design-audit-20260921/burnin-work.json`
- `train_g1_commit_trajectory.py:355-391` (`objective_batch`)
- `train_g1_commit_trajectory.py:639-669` (GAN per-group critic/discriminator work)
- `model/g1_commit_trajectory.py:223-245` (`CommittedRollout.step` and scored rollout)
- `https://arxiv.org/html/2506.08009v1`
- `https://github.com/guandeh17/Self-Forcing`
- `https://arxiv.org/html/2405.14867v1`
- `https://github.com/tianweiy/DMD2`
- `https://arxiv.org/html/2505.07812v1`
- `https://github.com/shaochenze/EAR`
- `https://arxiv.org/abs/2409.00588`
- `https://github.com/irom-princeton/dppo`

## Thread `01a0b8fa-c664-7df2-b061-3b1b31a32643`
updated_at: 2026-09-26T18:16:14+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/19/rollout-2026-09-19T17-24-49-01a0b8fa-c664-7df2-b061-3b1b31a32643_01a0b8fb-8fa8-7723-bbb1-e491d2e1b1ce.jsonl
rollout_summary_file: 2026-09-19T09-23-57-mf0T-workspace_cleanup_zzy_git_history_and_cluster_backed_artifac.md

description: Large-scale workspace cleanup completed; removed cluster-backed obsolete GR00T/LingBot artifacts, verified caches/archives, and all zzy-owned Git metadata after explicit authorization. Preserved current models, code, data, active work, and evidence.
task: workspace_disk_cleanup_and_zzy_git_history_pruning
task_group: /home/wangyukun/ubt_isaac_sim_ws storage cleanup
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: disk-cleanup, uploaded-to-cluster, GR00T, LingBot, zzy, git-history, Docker, hardlinks, inode, ModelScope, cleanup-manifest

### Task 1: Remove obsolete cluster-backed artifacts

task: delete verified obsolete local models, caches, archives, and image tarballs while preserving current work
task_group: workspace storage cleanup
task_outcome: success

Preference signals:
- The user said: “只要是上传过集群的都可以当作有” -> historical evidence of cluster upload/consumption is sufficient for local deletion; live cluster verification is not required unless requested.
- The user repeatedly wanted old fine-tuned outputs removed but the latest working model retained -> use exact-path deletion and preserve current inference/evaluation artifacts.

Reusable knowledge:
- Current GR00T model retained: `ubt_vla_ws/ubt_vla_data/r01-old-new-lower-37mix-60k`.
- Five older GR00T model directories were removed, totaling `62941224749` bytes; current model, base model, and current evaluation reports remained.
- Completed evidence clone `/tmp/utars-results-20260921` was removed only after 1,456 files and all hashes were verified; final commit was `6117badd4b7e8edbac2238a5807dcda7444771bd`.
- ModelScope staging was removed after `transfer-completion.json` reported complete with no failures; physical reclaim was about `46591373312` bytes.
- Verified archive parts plus unused `/tmp/m2d-mrt2-runtime` were removed after audit checks; reclaim was `20315320320` bytes.
- Published/locally loaded M2D v2 archive was removed after immutable digest evidence; reclaim was `4911087616` bytes.
- Docker builder pruning was needed after removing the old M2D v1 tag because layers remained cached.

Failures and how to do differently:
- Do not equate `du` totals with physical reclaim; inspect link counts/inodes and verify `df` before/after.
- Do not claim cluster presence was live-verified; the 5090 had no Kubernetes access, so historical job/upload records were used.
- Similar-sized M2D result directories were retained because 15 matched large files were all byte-different.

References:
- Cleanup records: `0.logs/cleanup/20260919_uploaded_old_groot_models_removed.json`, `20260924-modelscope-advancement-cleanup.json`, `20260924_zhong_obsolete_caches_env_removed.json`, `20260926_completed_utars_upload_clone_removed.json`, `20260926_verified_audit_parts_and_old_env_removed.json`, `20260926_old_m2d_v2_image_archive_removed.json`.

### Task 2: Remove zzy Git history

task: delete explicitly authorized local Git metadata for departed user's workspaces while preserving working trees
task_group: zzy repository cleanup
task_outcome: success

Preference signals:
- The user authorized removal because zzy had left and said the Git history was no longer needed -> when similarly authorized, remove exact `.git` metadata but explain that local commit history/reflogs become unrecoverable.

Reusable knowledge:
- zzy's `/home/zhongzhengyang/lingbot-vla-v2/.git` was about 176–188 GB, dominated by historical multi-GB model checkpoint blobs; user's `syntheticdatageneration/.git` was about 12 GB.
- Unreachable objects were only about 170 KB, so ordinary pruning would not materially help.
- After explicit approval, 17 zzy-owned `.git` directories were removed. Inventory: `0.logs/cleanup/20260924_zhong_git_history_inventory.tsv`; final record: `0.logs/cleanup/20260924_zhong_git_history_removed.json`.
- Logical metadata removed: `209583710208` bytes; observed free-space increase: about 194.4 GiB. No zzy `.git` directories remained.
- Verified working files remained, including `lingbot-vla-v2/README.md`, `deploy/lingbot_vla_v2_policy.py`, `syntheticdatageneration/scenarios`, SmolVLA archives, LingBot base-model files, and LingBot data.

Failures and how to do differently:
- Do not delete individual Git packfiles merely because they are large or contain old-looking weights; first determine reachability and whether the goal is pruning or full metadata removal.
- Before deleting another user's Git metadata, snapshot heads/status, confirm no active processes or container mounts, delete only exact `.git` directories, and verify working-tree paths afterward.

References:
- `0.logs/cleanup/20260924_zhong_git_history_heads_status.txt`
- `0.logs/cleanup/20260924_zhong_git_history_inventory.tsv`
- `0.logs/cleanup/20260924_zhong_git_history_removed.json`

### Task 3: Final disk and duplicate-result check

task: validate post-cleanup state and avoid deleting non-identical current M2D results
task_group: post-cleanup verification
task_outcome: success

Reusable knowledge:
- Final observed free space was about 92 GB; zzy directory about 168 GB; M2D `runs` about 649 GB.
- `c64_od_codec_root_cause_20260925` and `c64_complete_sequence_repair_20260925` had 15 matching large paths but zero byte-identical files; retain both.

References:
- Final disk command: `df -h /`.
- Comparison used `cmp -s` on same-size matched files and found `byte_identical_files=0`.

## Thread `01a0c33c-96ce-7991-92b2-b516ea344a29`
updated_at: 2026-09-24T06:27:11+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T17-12-03-01a0c33c-96ce-7991-92b2-b516ea344a29.jsonl
rollout_summary_file: 2026-09-21T09-12-03-UVeh-cluster_causal_codec_results_and_auto_export.md

description: 核对正式集群 causal codec 三 seed 结果是否支持本地单 seed 判断，并为后续集群任务增加可供 5090 读取的自动成果导出；结果支持 reconstruction 结论但不支持全面物理结论。
task: compare_cluster_causal_codec_with_local_and_add_result_export
task_group: Musics2Dance causal codec experiment and hot-storage workflow
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: EXP-20260918-fd-causal-codec-capacity, causal codec, multirate512_balanced, hot storage, export_m2d_results, 550 Permission denied, RTX5090, three seeds

### Task 1: Compare cluster formal causal codec results with local single-seed results

task: verify whether the formal cluster causal codec supports the prior local conclusion
task_group: causal codec experiment audit and result comparison
task_outcome: success

Preference signals:
- When the user asked whether the cluster result supports the local conclusion, preserve separate identities for local single-seed, cluster three-seed, width1024, and historical mainline results; do not combine them into one claim.
- The user later said: “以后要自动导出成果到5090可以读取下载的地方，这样你可以直接读或者下载” -> future cluster runs should make results directly readable/downloadable by 5090 without requiring another manual KubeSphere export.

Reusable knowledge:
- Formal cluster run: 4 variants × seeds 1234/2345/3456, 100000 steps, batch64, workers2, 183 training tracks and 18 held-out tracks.
- All 12 final evaluations were verified. Reaggregation of per-track metrics matched stored summaries with maximum error `1.4551915228366852e-11`; each run covered 51534 frames.
- Cluster mean native MSE: compact256 `0.057629`, multirate256 `0.053709`, multirate512 `0.065307`, multirate512_balanced `0.048242`.
- Balanced512 vs ordinary512: native MSE `-26.13%` and joint MAE `-12.42%` on average; balanced won joint MAE on all 18 tracks for all three seeds.
- Ordinary512 vs multirate256: native MSE worsened `+21.59%`; the three-seed ranking supports the local observation that simply widening to 512 is not beneficial while reducing auxiliary loss pressure helps.
- Foot-skate did not reproduce the local direction; sparse/model-dependent contact metrics must not be used to claim comprehensive physical improvement.
- The matrix contains no width1024 runs and no music-generation or physical-execution evidence. Historical old-mainline comparison is approximate because training conditions and frame truncation differ.

Failures and how to do differently:
- FTP listing/readback of `training/` and `supervised-loss/training/` returned `550 Permission denied`; this blocked direct result retrieval but did not indicate training failure. The user had to run an export script in KubeSphere.
- Do not claim cluster results before reading completion/evaluation records; the previously retrieved `previous-job.log` only reached roughly steps 4400–4500 and was not final evidence.

References:
- `runs/causal_codec_capacity/cluster-readback-20260921/cluster-results-20260921.tar.gz`
- `runs/causal_codec_capacity/cluster-readback-20260921/extracted/supervised-loss/training/four-variants-3seed-100k-4h/`
- `runs/causal_codec_capacity/cluster-readback-20260921/verify_comparison.py`
- `runs/causal_codec_capacity/cluster-readback-20260921/verified-comparison.json`
- `docs/experiments/reviews/EXP-20260918-fd-causal-codec-capacity-cluster-results-20260921.md`

### Task 2: Add automatic hot-storage result export

task: automatically publish cluster result records for 5090 readback
task_group: M2D hot-storage delivery and cluster launcher workflow
task_outcome: success

Preference signals:
- The user explicitly wants future outputs placed where the local 5090 can read/download them directly -> treat automatic result export as the default for new cluster releases.

Reusable knowledge:
- `scripts/export_m2d_results.py` scans a `/hot/upload/` output directory, makes record files readable, creates `results-records.tar.gz` and `download-manifest.json`, and leaves model/video artifacts at their original paths.
- Export includes metrics, configs, JSON/CSV/Markdown/log/text records; it excludes runtime, raw data, and source code from the records archive.
- Integrated into `run_token_causal_codec_cluster.py`, `run_token_causal_variants_cluster.py`, `run_g1_causal_native_cluster.py`, and `run_g1_commit_cluster.py`.
- The exporter is not scientific acceptance: the manifest explicitly notes that export availability does not imply training completion or scientific acceptance.
- `tests/test_m2d_result_export.py` passed, and all modified launcher/exporter files compiled successfully.

Failures and how to do differently:
- The exporter runs on normal completion or Python exception exit, but cannot run after SIGKILL/node loss; a resumed run should regenerate the export.
- Existing running jobs use the old release and were intentionally not modified; deploy the new package before relying on automatic export.

References:
- `scripts/export_m2d_results.py`
- `tests/test_m2d_result_export.py`
- `docs/M2D_HOT_STORAGE.md` section `2026-09-21 结果自动导出规则`
- `AGENTS.md` hot-storage result delivery guidance

## Thread `01a0c36e-f518-7801-8bb2-f9ca761f5cdd`
updated_at: 2026-09-24T06:27:09+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T21-19-48-01a0c36e-f518-7801-8bb2-f9ca761f5cdd_01a0c41f-6c44-7be2-a94e-094e4d91055f.jsonl
rollout_summary_file: 2026-09-21T10-07-03-7i5T-causal_music_calibration_future_dependence_audit.md

---
description: Audited causal-native train-test-mismatch and tested whether frozen music calibration lets the generator bypass Future; Future is used, but downstream self-correction benefit remains unproven.
task: causal_music_calibration_future_dependence_audit
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: causalcodec, causal-native, train-test-mismatch, Future-attention, calibration, history-feedback, hacking, fixed-vs-dynamic, rotation-degeneration, K64, H4C4, MMR-G1+
---

### Task 1: Audit causal-native train-test-mismatch route

task: Assess whether old ES/GAN/CoF-style methods remain valid on the frozen 1024 causal D+C codec.
task_group: causal-native codec and trajectory training
task_outcome: partial

Preference signals:
- The user asked for first-principles, maturity, and novelty analysis rather than assuming ES is still the right method -> future proposals should separate legacy codec assumptions from the current causal D+C deployment contract.
- The user cares about rotation failures, activity, D/C role separation, and honest claim boundaries -> report system comparisons separately from causal ablations.

Reusable knowledge:
- Current interface is native38D, D512+C16, 30Hz, two frames/token, frozen codec, generator K64 D+C history, H4/C4 deployment and NFE10. The decoder has about 62-token receptive field.
- Native CoF continuation is not a no-CoF/with-CoF ablation: base already used CoF and continuation used the same objective at lower learning rate.
- Generated >90-degree rotations correlate with degenerate 6D rotation outputs; strict FP32, chunk/full decode, GPU graph, and cache/render audits did not find a pipeline conversion bug. Real-history probes still showed flips, so long-horizon exposure bias is not a sufficient explanation.
- 1024 codec 50k→100k reconstruction gains were very small; do not assume longer codec training is the best fix for generator rotation failures.

Failures and how to do differently:
- Do not port old B71/physical-closure novelty claims unchanged; the current route is commit-wise D+C Two-Forward with residual rebase/FHC, not the old explicit physical-state closure.
- Do not attribute system differences to ES/GAN or codec alone when startup, history, codec, generator, and budget also differ.

References:
- `docs/research/CAUSAL_CODEC_COMMIT_TRAINING_MIGRATION_20260921.md`
- `docs/experiments/EXP-20260921-fd-causal-native-trajectory-training.md`
- `docs/experiments/reviews/EXP-20260921-fd-causal-native-rotation-and-training-audit.md`

### Task 2: Test whether calibration bypasses Future

task: Verify if the frozen history-based music reliability mechanism can be gamed by learning to ignore Future.
task_group: causal music self-calibration and Future dependence
 task_outcome: partial

Preference signals:
- The user explicitly worried that calibration might “hacking导致不用未来” -> always perform both matched Future sensitivity tests and downstream quality tests; nonzero reliability alone is insufficient.
- Keep separate claims: “the model uses Future” versus “Future improves motion quality.”

Reusable knowledge:
- Calibration is fit before dance training and frozen; actual training calibration and local artifact matched to ~3.3e-15 coefficient difference; official test labels were not used.
- Matched-state intervention on dynamic6250: repeat-original is bitwise identical; zeroing Future changes all 54/54 states with mean next-segment joint-angle difference ~7.28 degrees; swapping Future to another song changes all 54/54 with ~7.80 degrees; zeroing Past also changes outputs (~8.76 degrees).
- Full short-rollout posthoc comparison on the same dynamic checkpoint: original MMR 0.1088, Future-zero 0.0991, wrong-Future 0.1008, mean-history 0.1152, Future-unit 0.1066. These directions are suggestive but none survived the 24-comparison correction.
- Formal fixed-vs-dynamic result did not establish stable dynamic quality improvement: short MMR dynamic 0.1060 vs fixed 0.1092; severe rotations 2 vs 6, but paired/multiple-comparison evidence was insufficient.
- History feedback improves the reliability proxy itself: on the audio-disjoint 13-song diagnostic subset, proxy MSE fell 27.8%, 12/13 songs improved. This is not evidence of dance-quality gain.

Failures and how to do differently:
- Do not infer Future usefulness from attention/reliability being nonzero. Use identical generated histories, decoder cache, Past/Style, and random draws while zeroing or swapping only positive-lead Future slots.
- Do not infer quality improvement from output sensitivity. Run matched full-rollout metrics and preserve OOD, one-training-seed, repeated-test-audio, and posthoc limitations.
- Do not force a minimum Future weight merely to prevent bypass; adaptive downweighting may be correct when forecasts are bad. The decisive next proof is correct Future > no/wrong Future, then history feedback > current-information-only specifically on naturally bad forecasts.

References:
- `docs/experiments/reviews/EXP-20260922-fd-causal-music-self-calibration-results-20260923.md`
- `runs/causal_music_self_calibration/results-check-20260923/future-dependence.json`
- `runs/causal_music_self_calibration/results-check-20260923/future-only-rollout/significance.json`
- `runs/causal_music_self_calibration/results-check-20260923/feedback-window-analysis.json`
- `.venv311/bin/python scripts/experiment_ledger.py lint` -> `0 error(s), 5 warning(s)`

## Thread `01a0c6e3-0d78-7bf3-b128-19efed157ec0`
updated_at: 2026-09-24T06:27:02+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T10-12-44-01a0c6e3-0d78-7bf3-b128-19efed157ec0.jsonl
rollout_summary_file: 2026-09-22T02-12-44-bDMc-ogi_llm_gpu_isolation_and_automatic_training_continuation.md

description: Kubernetes GPU-pool isolation and automatic continuation workflow for M2D training; user requires ogi-llm-only scheduling, all nodes in that pool, checkpoint-preserving recovery, and detached continuation after a completed 6250-step run
 task: diagnose and manage ogi-llm Kubernetes GPU training jobs
 task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
 task_outcome: partial
 cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
 keywords: kubectl, ogi-llm, gpu-quota, FailedCreate, nvidia.com/gpu, Kubernetes, nodeAffinity, tolerations, 6250, 12500, checkpoint-resume, KubeSphere, independent-reviewer

### Task 1: GPU pool isolation and job recovery

task: enforce ogi-llm-only scheduling and safely inspect/replace two/three-GPU jobs
task_group: Kubernetes GPU scheduling
 task_outcome: partial

Preference signals:
- when the user clarified “用什么组就只能申请那个组的卡” and “正确的应该是允许这个组里的所有卡” -> future manifests must use only `ogi/node-pool=ogi-llm`, remove other pool tolerations, and remove fixed hostname affinity.
- when stopping or replacing a job, preserve logs/checkpoints and inspect current Pods/owner state first; do not delete healthy jobs based on stale quota output.

Reusable knowledge:
- This host lacks a Kubernetes control channel and `~/.kube`; hot-storage artifacts cannot prove a Job was submitted or is running. Cluster actions require a KubeSphere terminal.
- Correct manifest shape: namespace `ogi-llm`; GPU request=limit; toleration `{key: ogi/node-pool, operator: Equal, value: ogi-llm, effect: NoSchedule}`; no `affinity`, `nodeSelector`, or `nodeName` restriction.
- A historical `FailedCreate` quota event (`requested 3, used 8, limit 9`) was later superseded by a Running Pod, so always re-query current nonterminal Pods before cleanup.

Failures and how to do differently:
- Multiple pool tolerations were initially mistaken for cross-pool permission. They are not authorization; obey the user’s hard pool-isolation rule.
- Never infer queued/not-started/running status from delivery files alone.

References:
- Status commands: `kubectl describe job -n ogi-llm <job>`; `kubectl get pods -n ogi-llm -l job-name=<job> -o wide`.
- Corrected local artifact: `runs/causal_native_trajectory/llm-only/job-2h-llm-only.yaml`.

### Task 2: Automatic 6250-to-12500 continuation

task: extend fixed/dynamic music self-calibration arms from 6250 to 12500 while preserving original artifacts
task_group: M2D music self-calibration training
 task_outcome: partial

Preference signals:
- when the user said “我先把新的6250训到两倍” and then “要自动的” -> prepare a detached one-time watcher that waits for completion and submits continuation automatically; do not require a second manual intervention after completion.
- user confirmed continuation remains limited to `ogi-llm` only.

Reusable knowledge:
- Original Job `m2d-causal-music-calibration-3h` eventually ran formally after an earlier quota failure; hot logs showed fixed≈99/6250 and dynamic≈96/6250, `proof=false`, microbatch 384, recovery checkpoints present.
- Continuation artifacts are under `runs/causal_music_self_calibration/extend-12500/`; `START_AUTO.txt` launches a detached watcher which waits for original `Complete=True`, stops on `Failed=True`, detects an existing continuation Job, and creates `m2d-music-calibration-12500-3h`.
- Mock tests for complete, failed, already-existing, and wait-then-complete behavior passed. Upload/readback of continuation files was verified.
- Automatic continuation was prepared but not confirmed enabled; local host cannot run `kubectl`, so cluster-terminal enablement evidence is required.

Failures and how to do differently:
- The formal trainer hard-codes 6250, so changing local config cannot extend the active Job. Use a separate continuation Job from verified checkpoints and save outputs under `training-12500/`.
- Do not claim automation is active until the detached watcher has actually been started in KubeSphere.

References:
- Enablement: `runs/causal_music_self_calibration/extend-12500/START_AUTO.txt`.
- Hot path: `/hot/upload/EXP-20260922-fd-causal-music-self-calibration/extend-12500/`.
- Continuation Job: `m2d-music-calibration-12500-3h`.

### Task 3: Reviewer configuration request

task: change independent reviewer setting to `6sol high`
task_group: workflow/reviewer configuration
 task_outcome: uncertain

Preference signals:
- when the user said “独立reviewer改为6sol high” -> treat this as an explicit configuration change request and verify the effective setting after editing.

Reusable knowledge:
- No configuration file was located or changed in this rollout; the request remained unverified.

Failures and how to do differently:
- Do not claim the reviewer setting changed without locating the active configuration and validating its effective value.

References:
- Exact user request: `独立reviewer改为6sol high`.

## Thread `01a0c7f8-cf32-78b1-a187-322171d391d7`
updated_at: 2026-09-24T06:00:39+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T15-16-07-01a0c7f8-cf32-78b1-a187-322171d391d7.jsonl
rollout_summary_file: 2026-09-22T07-16-07-eRP9-lower_shelf_jitter_pd_grasp_focused_verification.md

description: Lower-shelf N1.7 jitter investigation repaired RTC/execution mismatches and tested PD/grasp interventions; fixed replay jitter improved, but autonomous placement did not improve and no candidate was promoted.
task: lower_shelf_jitter_root_cause_pd_grasp_verification
task_group: /home/wangyukun/ubt_isaac_sim_ws
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: GR00T-N1.7, RTC, relative-actions, train-inference-mismatch, damping, Kp, Kd, grasp-constraint, contact-force, tilt, drop, 7/40, N17_V3_GRASP_CONSTRAINT

### Task 1: Inference and execution root-cause repair

task: repair lower-shelf RTC/reference/timing/execution mismatch
task_group: N1.7 lower-shelf closed-loop evaluation
task_outcome: partial

Preference signals:
- When the user requested “根因修复” and later “不再增加方案”, future runs should inspect action semantics, timing, and traces first, then freeze the selected intervention and avoid exploratory variants.

Reusable knowledge:
- Relative arm actions must be decoded against the current reference state. RTC continuation must re-encode the prior absolute chunk against the new reference, preserve the physically executed prefix, and account for inference latency; old-reference reuse caused target drift/jitter.
- Verified fixes included waist-clock computation, settled initial-height reference, box reset offset, same-tick base/arm application, midpoint target interpolation, 60 s lower horizon, filtered box contacts, larger contact buffer, and separate support/placement/drop measurement.
- The earlier corrected route had zero action gaps and no expired requests/client errors, but autonomous placement remained unreliable. The formal success-first 8/frozen-8 lower run produced 7/40 actual completions and 39/40 pickups.

Failures and how to do differently:
- Do not call train/inference consistency fully solved: representation, normalization, state-clock, and execution mismatches were repaired, but closed-loop distribution shift after tilt/retreat remains unresolved.
- Do not equate pickup, stage success, or lower roughness with complete success; require target pose, release, no-drop, and tilt/quality gates.

References:
- `0.logs/n17_v3_jitter_fix_20260917/REPORT.md`
- `0.logs/n17_v3_control_rootfix_20260917/REPORT.md`
- `0.logs/n17_v3_execution_closure_20260917/REPORT.md`
- `syntheticdatageneration/sdg_utils/n17_v3_rtc.py`
- `syntheticdatageneration/script/vla_n17_fullbody/n17_v3_rtc_reference.py`
- `syntheticdatageneration/scenarios/training/mixins/VlaN17V3RuntimeMixin.py`

### Task 2: PD and grasp intervention verification

task: test damping, wrist effort, and privileged grasp/entry protection
task_group: lower-shelf physical response and grasp stability
 task_outcome: partial

Preference signals:
- The user wants explicit separation of retained defaults versus PD experiments and regards a tilted/unreleased box as failure; future reports should state whether an intervention changes actual completion, not only jitter.

Reusable knowledge:
- Baseline arm gains were `Kp=5729.578`, `Kd=57.29578`; experiments kept Kp fixed and tested approximately 3x arm Kd. Full-arm damping reduced fixed-command early roughness about 39–40% and static-hold residual roughness about 80.9%, but autonomous damping achieved 0/6; shoulder/elbow-only damping achieved 0/4.
- Wrist effort 20→40 Nm reduced tracking error but caused grasp loss; it was diagnostic only and must not be promoted.
- Candidate C combined privileged contact/geometry grasp feedback with 3x damping. Fixed successful replay improved early common-window roughness 49.45%, angular-speed p95 27.16%, and tilt 8.82°→6.02%, but mid-phase tilt worsened 4.02°→7.42°.
- Final fresh autonomous cases remained 0/2 versus native 0/2: one retreated ~7.75 m and ended ~50.29° tilted without release; the other dropped at 55.3 s. `N17_V3_GRASP_CONSTRAINT=0` remains default.

Failures and how to do differently:
- Do not attribute replay improvement solely to PD: Candidate C also modifies arm targets using privileged contact/geometry feedback.
- The D acquisition/latch change failed a fixed replay at ~50.73 s and was discarded. Preserve its negative evidence.
- Keep initialization failures (`initial_target_obj_pose`/`target_obj` lazy-None errors) outside success statistics and verify settled USD box pose before runtime initialization.

References:
- `0.logs/n17_v3_physics_rootcause_20260922/REPORT.md`
- `0.logs/n17_v3_grasp_repair_20260922/REPORT.md`
- `0.logs/n17_v3_grasp_repair_20260922/closure.json`
- `0.logs/n17_v3_grasp_repair_20260922/replay_comparison.json`
- `0.logs/n17_v3_grasp_repair_20260922/paired_statistics.json`
- `syntheticdatageneration/sdg_utils/n17_v3_grasp_constraint.py`
- `N17_V3_GRASP_CONSTRAINT=0`

### Task 3: Evidence and closure

task: preserve complete focused verification evidence and clean up runtime
task_group: experiment closure and reporting
task_outcome: success

Reusable knowledge:
- 14 full 60-second trials, 2 pre-episode startup failures preserved separately; 42 originals plus 3 comparison videos decoded as H.264/yuv420p, no temporary videos.
- 17 focused tests, 14 intervention checks, and 6 raw-policy checks passed.
- No retraining, default promotion, force/mass/friction change, scoring change, or new formal 40-episode run occurred. Owned server/simulators were stopped; unrelated services were preserved.

References:
- `0.logs/n17_v3_grasp_repair_20260922/RESULTS.md`
- `0.logs/n17_v3_grasp_repair_20260922/VIDEOS.md`
- `0.logs/n17_v3_grasp_repair_20260922/closure.json`
- `0.logs/n17_v3_grasp_repair_20260922/REPORT.md`

## Thread `01a0c82d-a4df-7591-ba05-19ea0651f1e1`
updated_at: 2026-09-24T06:25:33+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T16-13-49-01a0c82d-a4df-7591-ba05-19ea0651f1e1.jsonl
rollout_summary_file: 2026-09-22T08-13-49-aUbT-g1_genre_matching_score_parallel_mmr_evaluation.md

description: Implemented and completed a FineDance-inspired G1 Genre Matching Score evaluator, trained it on local data, and scored old/new Musics2Dance experiments alongside MMR+; results are descriptive and not scientifically accepted.
task: gs-g1 genre matching evaluation parallel to mmr-plus
 task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 task_outcome: success
 cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 keywords: FineDance, Genre Matching Score, GS-G1, MMR+, AST, AGCN, G1, resampling, stability, rotation supervision, exact resume, 5090, audio-group bootstrap

### Task 1: Research and freeze GS-G1 adaptation
task: verify official FineDance GS and choose local-compatible evaluator
task_group: literature-to-local-evaluation
task_outcome: success

Preference signals:
- The user requested GS “和mmr+平行” and accepted an independent G1 adaptation after official code/weights were unavailable -> preserve MMR+ separately and label the adapted evaluator honestly.
- The user explicitly wanted old mainline and new experiments, later adding “还有resampling的” -> include all named experiment families and historical references.

Reusable knowledge:
- FineDance defines GS as cosine similarity between learned AST music-style and AGCN dance-genre embeddings trained with matched/mismatched genre supervision.
- Public FineDance repositories/issues did not provide a usable Genre & Coherent Aware Retrieval Module or verified GS checkpoint. Local G1 motion therefore requires an independent adaptation named `GS-G1`; its values must not be compared directly with human-motion FineDance GS tables.

References:
- `docs/research/GENRE_MATCHING_SCORE_ADAPTATION_20260922.md`
- `configs/experiments/gs_g1.json`
- Official repo: `https://github.com/li-ronghui/FineDance`

### Task 2: Train and validate GS-G1
task: train fixed AST+G1 cross-modal evaluator and prove readiness
task_group: gs-g1-training
 task_outcome: success

Reusable knowledge:
- Frozen contract: 183 songs; 146 fit / 37 validation; 35 independent audio groups; seed1234; 3000 updates; batch32; FP32; AST AudioSet0.4593; joint audio/motion training; native G1 FK windows at 30fps.
- Real CPU proof passed with both branches updating and exact optimizer/RNG next-step replay. GPU batch32 proof passed with peak allocation 13,117,452,288 bytes (~12.22 GiB). Formal training completed at ~0.32–0.33 sec/update.
- Validation signal passed: paired margin 0.5694 [0.4522, 0.6711], cross-song margin 0.5839 [0.4899, 0.6662], with 35 independent audio groups.
- Independent review passed implementation semantics; this is not scientific acceptance.

Failures and how to do differently:
- A first queue stalled because it treated a remote stability watcher as a GPU blocker. Serialize actual GPU programs with `runs/local-gpu.lock`; monitoring-only processes should not block training.
- Resource review is required for ledger review currentness when a resource contract exists.

References:
- `runs/gs_g1/formal/final.pt`
- `runs/gs_g1/formal/validation.json`
- `runs/gs_g1/cpu-proof/proof.json`
- `runs/gs_g1/gpu-proof/proof.json`
- `.venv311/bin/python -m unittest tests.test_gs_g1` -> 7 passed

### Task 3: Score old/new experiments beside MMR+
task: matched GS-G1 and MMR+ evaluation over saved motions
task_group: multi-experiment-evaluation
 task_outcome: success

Preference signals:
- “和mmr+平行” means separate metric columns, no composite or replacement.
- “还有resampling的” means history-resampling base/CoF/continuous/joint arms must be included.

Reusable knowledge:
- Evaluated 4 groups, 17 unique settings, 22 main entries, 30 condition entries, 1620 records; all use the same GS checkpoint, 18 songs × 3 seeds, frames264:984, with a separate 13-song nonduplicate subset.
- History GS means: base 0.6674/0.6442, CoF 0.6762/0.6352, continuous RF 0.6747/0.6329, joint RF 0.6806/0.6415 (18/13 songs); predeclared contrasts include zero.
- Stability contrasts versus its new-music control include zero. Rotation-supervision B vs A has a small positive GS signal but does not fix the failed rotation target. Native CoF vs old mainline is positive on all18 but uncertain on nonduplicate13.
- GS-G1 is a style metric only; do not infer physical, beat, amplitude, rotation, or video-quality conclusions.

References:
- `eval/supplement_g1_genre_matching.py`
- `runs/gs_g1/local-evaluation-20260923/REPORT.md`
- `runs/gs_g1/local-evaluation-20260923/RESULTS.json`
- `runs/gs_g1/local-evaluation-20260923/SUMMARY.csv`
- `runs/gs_g1/local-evaluation-20260923/source-inventory.json`
- Per-group outputs: `runs/*/comparison/genre-matching/`

## Thread `01a0c869-924b-71d0-9a4b-caf03d445046`
updated_at: 2026-09-24T05:57:11+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T17-19-17-01a0c869-924b-71d0-9a4b-caf03d445046.jsonl
rollout_summary_file: 2026-09-22T09-19-17-yUpo-utars_techreport_feishu_handoff_and_training_inference_consi.md

description: 用户制作 UTars/Isaac Sim/VLA 3页左右飞书技术交接报告，强调最终方案、已补齐能力、方法 intent 和可下载证据；报告已生成，最后追问训推不一致但未获回答
 task: UTars Isaac Sim VLA techreport and training-inference consistency explanation
 task_group: /home/wangyukun/ubt_isaac_sim_ws
 task_outcome: partial
 cwd: /home/wangyukun/ubt_isaac_sim_ws
 keywords: UTars, Isaac Sim, VLA, Feishu, techreport, HDF5, GR00T N1.7, RTC, relative-actions, jitter, box-drop, training-inference mismatch

### Task 1: 精简飞书技术交接报告

task: produce concise final-version UTars/Isaac Sim/VLA handoff report
task_group: Feishu technical handoff
task_outcome: success

Preference signals:
- 用户说“只写 UTars / Isaac Sim / VLA” -> 不纳入 Musics2Dance。
- 用户说“只要几页”“按最终的版本来，不用讲中间迭代的版本” -> 默认 3 页左右，只讲最终方案和 intent。
- 用户说“挑重点的贡献说，比如原来我接手的时候没有的东西现在做完了” -> 围绕“原来缺什么 → 补了什么 → 现在能做什么”写，少写不足和调参过程。
- 用户说“直接发这里”“给路径，我下载” -> 需要直接返回可复制/下载的绝对路径，不只在材料包中引用。

Reusable knowledge:
- 已生成主稿：`docs/briefs/utars-techreport-20260922/REPORT.md`。
- 已生成飞书材料包：`docs/briefs/utars-techreport-20260922/UTars飞书交接材料.zip`。
- 生成后验证：各 Markdown 无 broken local links，Markdown copies 一致，证据引用齐全；材料包 8 files / 5,521,523 bytes。
- 适合报告主线：自动搬箱示范生成；下层 hold-and-level；HDF5 数据筛选；VLA/GR00T 接入与闭环验证。

Failures and how to do differently:
- 不要重新扩展为 12–15 页或纳入所有历史实验；用户已明确要短、最终版本、面向接手人理解方法。

References:
- `docs/briefs/utars-techreport-20260922/REPORT.md`
- `docs/briefs/utars-techreport-20260922/UTars飞书交接材料.zip`
- `docs/briefs/handlingbox-data-collection-brief-20260722/figures/scenario_overview.jpg`

### Task 2: 掉箱视频路径

task: provide two representative dropped-box videos
task_group: evidence handoff
 task_outcome: success

Reusable knowledge:
- Selected videos are from the same 2026-09-18 lower-level 40-episode policy batch; episode 001 and 002 reports contain `box_dropped_during_sequence`.

References:
- `/home/wangyukun/ubt_isaac_sim_ws/0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/same_shelf_lower_level/runs/full_policy/merged/videos/episode_001/combined.mp4`
- `/home/wangyukun/ubt_isaac_sim_ws/0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/same_shelf_lower_level/runs/full_policy/merged/videos/episode_002/combined.mp4`

### Task 3: 训推不一致问题

task: explain training-inference mismatch and whether it is solved
task_group: GR00T N1.7 / RTC / closed-loop execution
task_outcome: uncertain

Reusable knowledge:
- Relative arm actions must decode against the current reference state; RTC continuation must convert previous absolute chunks into the new reference, preserve physically executed prefixes, and account for inference latency. Reusing old references causes jitter and target drift.
- Verified execution/measurement fixes are complete and independently reviewed; 59 targeted tests passed and 57 videos decoded, but this does not prove general task acceptance.
- Lower 40 evaluation remains 7/40 actual completions; 2026-09-22 physics diagnostics found damping can reduce local roughness without improving autonomous task success. Do not claim the entire training-inference mismatch is solved, and do not attribute every remaining failure to the model without qualification.

Failures and how to do differently:
- The rollout ended immediately after the user asked “训推不一致是什么问题，解决了吗”; no answer or final verification exists. Future response should distinguish: (1) confirmed action/reference/timing fixes, (2) remaining policy/physics interaction, and (3) what is not yet scientifically accepted.

References:
- `0.logs/n17_v3_execution_closure_20260917/REPORT.md`
- `0.logs/n17_v3_physics_rootcause_20260922/REPORT.md`
- `0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/REPORT.md`
- `docs/experiments/EXP-20260902-utars-groot-n17-old-upper-new-lower-37mix.md`

## Thread `01a0ca3c-c380-7931-86b6-f71d26400857`
updated_at: 2026-09-23T14:20:19+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T01-49-34-01a0ca3c-c380-7931-86b6-f71d26400857.jsonl
rollout_summary_file: 2026-09-22T17-49-34-qDsj-m2d_music_self_calibration_cluster_continuation_and_5090_con.md

---
description: Prepared and verified migration of three 5090 Future-control training arms to one cluster H card; cluster submission remained unconfirmed, while the separate 12500 fixed/dynamic continuation was observed running.
task: migrate_5090_future_controls_to_single_cluster_gpu
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: Musics2Dance, EXP-20260922-fd-causal-music-self-calibration, Future controls, MPS, RTX5090, H100, H200, checkpoint resume, hot storage, kubectl, m2d-future-controls-1h
---

### Task 1: Migrate three 5090 controls to one cluster GPU

task: resume film_dynamic, ca_mean_history, and film_ca_dynamic on one cluster H card
task_group: causal music self-calibration / Future controls
task_outcome: partial

Preference signals:
- when the user said “还有在5090上跑的，我要在集群上续跑，单卡跑三个” -> preserve the three-arm route, run them concurrently on one card, and resume rather than restart.

Reusable knowledge:
- Verified local resume starts: `film_dynamic=1563`, `ca_mean_history=1450`, `film_ca_dynamic=0`; preserve optimizer, RNG, source order, input contract, parent identity, seed1234, 48 source groups, physical microbatch16, and 6250-update endpoint.
- Local coordinators/trainers were stopped only after immutable recovery checkpoints were hard-linked and loaded successfully. Last observed local updates were 1567 and 1489, so a few updates may replay from checkpoint.
- Delivered assets and code delta were readback-verified in `/1-H集群-热存储/zzy-data/upload/EXP-20260922-fd-causal-music-self-calibration/future-controls-1h/`; delivery does not imply execution.
- The intended Job is `m2d-future-controls-1h`, one GPU, 16 CPU, 128GiB RAM, no hostname restriction/suspend; runtime uses private CUDA MPS for all three trainers. Target-card memory/throughput remains an empirical startup gate.

Failures and how to do differently:
- The rollout could not submit because the 5090 host and jump host lacked kubectl/cluster configuration. Do not report “started” from upload receipts; execute `APPLY_1H_THREE_CONTROLS.txt` in a cluster terminal and verify Job/Pod plus hot logs.
- Do not reuse the old cluster release without installing the isolated eight-file code delta and validating strict input/checkpoint identity.

References:
- Launch script: `runs/causal_music_self_calibration/migrate-1h-20260923/APPLY_1H_THREE_CONTROLS.txt`
- Resume verifier: `runs/causal_music_self_calibration/migrate-1h-20260923/resume-verification.json`
- Delivery receipt: `runs/causal_music_self_calibration/migrate-1h-20260923/code-delivery.json`
- Cluster runner: `scripts/run_g1_future_controls_cluster.py`

### Task 2: Continue 12500 fixed/dynamic cluster training

task: observe the approved budget extension from 6250 to 12500 for fixed and dynamic arms
task_group: causal music self-calibration / cluster continuation
task_outcome: success

Reusable knowledge:
- Hot-storage readback confirmed both continuation arms running at update `6358` with `proof=false`; preserve this Job and do not replace it while launching the separate Future-controls Job.
- Continuation is a same-claim budget extension, not a new experiment; 12500 evaluation must be generated separately from 6250 evidence.

References:
- `runs/causal_music_self_calibration/migrate-1h-20260923/extension-live.json`
- Hot paths: `/hot/upload/EXP-20260922-fd-causal-music-self-calibration/training-12500/fixed/status.json` and `.../dynamic/status.json`

### Task 3: Accelerate completed-run rendering

task: render saved cluster motions on RTX5090 and deliver videos without regenerating motion
task_group: M2D evaluation/render delivery
task_outcome: success

Reusable knowledge:
- Cluster rendering used software OSMesa and held H GPUs idle. Hardware EGL on RTX5090 was verified as `NVIDIA GeForce RTX 5090/PCIe/SSE2`; completed saved-motion rendering and uploads can be moved to the 5090.
- Four remaining 120-second five-panel videos were rendered from saved `motions.pt`/`cases.json`, validated with full H264/AAC decode, and delivered under `render-accelerated/`; total accelerated rendering was about620.61s.
- Keep score/report closure separate from scientific acceptance; render completion alone does not accept the experiment.

References:
- `runs/causal_music_self_calibration/render-acceleration/accelerated-manifest.json`
- `runs/causal_music_self_calibration/render-acceleration/hardware-manifest.json`
- `runs/causal_music_self_calibration/render-acceleration/render-acceleration-source.tar.gz`
- Renderer validation requires checking actual GL renderer and rejecting `llvmpipe`, `softpipe`, or `swrast` before spending time.

## Thread `01a0cc3c-3082-7ad2-bedd-f0ad433169a7`
updated_at: 2026-09-25T15:02:17+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T11-08-11-01a0cc3c-3082-7ad2-bedd-f0ad433169a7.jsonl
rollout_summary_file: 2026-09-23T03-08-11-i5i7-causalcodec_rf_gan_es_score_audit_and_sequential_training.md

---
description: Audited prior CausalCodec GAN/ES/RF results, fixed a seed-reuse video bug, and launched a matched RF history-strength experiment; R1 remained running and R2 queued due to real RTX5090 VRAM limits.
task: CausalCodec RF/GAN/ES score audit and RF history-strength training
 task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: CausalCodec, CoF, GAN, ES, Resampling Forcing, rf_joint_shift1, rf_joint_free2, RTX5090, VRAM, training-check, seed-reuse, standard-video-suite
---

### Task 1: Audit prior scores and research direction

task: Report complete, provenance-qualified GAN/ES/RF/CausalCodec scores and identify the next mature/novel route.
task_group: CausalCodec research audit
task_outcome: partial

Preference signals:
- when the user asked “汇报全部分数，然后继续实验分析” -> report every arm/window/metric and clearly label completed results versus running or proposed work.
- when choosing routes, the user expects novelty, maturity, mechanism fit, and engineering cost to be separated; do not assume ES is preferred because it is novel.

Reusable knowledge:
- Frozen contract: `multirate1024_balanced`, seed1234, D512+C16, K64, deployment H4/C4, C NFE10, 183/18 songs, 48 groups/update, 6250 updates/arm.
- Prior causal music self-calibration short scores: old quarter/old half/fixed/dynamic music match `0.0977/0.1039/0.1092/0.1060`; joint jerk `1355.35/1340.51/1197.86/1197.15`; >90° transitions `14/16/6/2`; FIDk `197.94/176.59/86.73/78.97`; FIDg `0.6062/0.8654/0.9334/0.8393`; diversity `16.49/15.72/12.93/13.50`.
- Historical feedback improved reliability-estimation error by `27.80%` on the audio-disjoint 13-song diagnostic subset (`12/13` improved, adjusted p `0.000732`), but this is not a dance-quality gain.
- Prior CoF/continuous-RF/joint-RF music scores were `0.102731/0.105489/0.097671`; RF did not establish broad superiority.
- Local third-update timings were approximately CoF `4.46s`, GAN `74.29s`, ES `71.06s`; these are bounded local timings, not isolated H100 benchmarks. Do not infer quality or full-training speed from them.

Failures and how to do differently:
- Never equate reliability-diagnostic error reduction or Future input sensitivity with improved dance quality.
- Do not claim the new RF-strength experiment has quality scores until both arms finish training, evaluation, interventions, and declared videos.

References:
- `docs/experiments/reviews/EXP-20260922-fd-causal-music-self-calibration-results-20260923.md`
- `docs/experiments/reviews/EXP-20260922-fd-rf-cof-full-comparison-20260923.md`
- `runs/causal_music_self_calibration/results-check-20260923/`
- `runs/rf_cof_standard_comparison/scorebook/`

### Task 2: RF history-strength implementation and execution

task: Train `rf_joint_shift1` and `rf_joint_free2` under the frozen RF contract.
task_group: RF rollout-strength experiment
 task_outcome: partial

Preference signals:
- the user authorized implementation and normal execution; preserve the matched 6250-update budget and frozen data/model/evaluation contract.
- approved operational work should continue automatically through monitoring, resume, evaluation, rendering, and reporting; avoid asking again unless a scientific decision is required.

Reusable knowledge:
- `rf_joint_shift1` changes only continuous history noise shift 0.6→1.0.
- `rf_joint_free2` adds two fixed short autonomous deployment-style free bursts per source group; it is a hybrid RF/free-rollout method, not the original RF paper method.
- Boundary diagnostic passed: p90 `0.081343`, gate limit `0.249751`; exact resume passed; proof peaks `13.19GB` and `13.31GB`.
- Independent review passed after fixing: (1) short-video seed motion reuse, and (2) a post-wait scheduler race that could start R2 after R1 failed.
- Contract lint passed with 0 errors and focused unittest passed: `.venv311/bin/python -m unittest -q tests.test_g1_rf_rollout_strength tests.test_g1_history_resampling`.
- Standard RF/CoF visual suite was rerendered successfully: `runs/rf_cof_standard_comparison/videos/manifest.json` reports `complete`, `70`; short tracks 036/063/098 had distinct frame fingerprints for seeds 1234/2345/3456.
- Live RTX5090 evidence showed R1 at about 15,646 MiB plus about 2,623 MiB other use (`18,317/32,607 MiB` total used), so two full-size arms cannot safely run concurrently. Persistent runner PID `3135019` keeps R2 queued until R1 completes.

Failures and how to do differently:
- Verify each video case uses its own `motion_key`; prior implementation reused seed1234 for short clips. Check actual frame fingerprints, not only metadata.
- Use live `nvidia-smi` after formal startup; proof allocations underestimated process VRAM. Keep effective 48 groups/update and microbatch unchanged; sequential execution is preferable to shrinking the contract.
- At rollout end R1 was only `1336/6250`, R2 had no log/status, and no new quality scores existed. Next agent should inspect fresh R1 progress, let the persistent scheduler start R2 only after completion, then run all declared downstream stages.
- Disk was at `95%` with about `186GB` free; monitor before large video/evaluation outputs.

References:
- `docs/experiments/EXP-20260923-fd-rf-rollout-strength.md`
- `docs/experiments/reviews/EXP-20260923-fd-rf-rollout-strength-prelaunch.md`
- `runs/rf_rollout_strength_local/pipeline.log`
- `runs/rf_rollout_strength_local/rf_joint_shift1/train.log`
- `runs/rf_rollout_strength_local/resource-observation.json`
- `runs/rf_rollout_strength_local/proof/receipt.json`
- `runs/rf_rollout_strength_local/diagnostic.json`

## Thread `01a0cc47-fa15-7a80-a814-6a39aa0e97a1`
updated_at: 2026-09-25T06:23:38+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T11-21-04-01a0cc47-fa15-7a80-a814-6a39aa0e97a1.jsonl
rollout_summary_file: 2026-09-23T03-21-04-5fep-causal_codec_root_cause_and_od_complete_sequence_repair_audi.md

---
description: Causal codec investigation separated active motion from correctness; OD codec audit confirmed a general complete-sequence supervision repair, but formal long-run quality remained unverified.
task: causal-codec-diagnosis-and-od-codec-repair-audit
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: causalcodec, MotionStreamer, D+C, 6D rotation, Gram-Schmidt, decoder jitter, phase artifact, C64, OD, complete-sequence coverage, source-aligned-target-blocks, HTTP-403
---

### Task 1: Causal codec mechanism diagnosis

task: diagnose why causal codec is more active but jittery/unstable and propose mature iteration directions
task_group: causal codec architecture and generation stability
task_outcome: partial

Preference signals:
- when the user contrasted “更活跃” motion with accuracy, jitter, and robot executability, they wanted these factors separated rather than treating activity as correctness -> future analyses should report amplitude, reconstruction, long-horizon stability, geometry validity, and executability independently.
- when the user asked for a mature, clean-system-compatible direction, preserve frozen controls and distinguish literature evidence, local observations, inference, and unvalidated proposals.

Reusable knowledge:
- Prior 38D reconstruction audits retained about 97.3% range and 97.2% speed, while low amplitude was concentrated in autonomous generation; do not conclude the codec representation cannot encode large motion.
- Root-cause controls found specific autonomous D+C trajectories enter near-degenerate 6D rotation outputs. In 56 selected severe cases, FP32 replay reproduced 56/56 failures versus 0/56 normal controls; increasing denoising from 10 to 100 steps only changed 56 to 51 failures. The main amplification occurs during 6D orthogonalization, not generic numerical precision.
- The decoder also has a two-frame phase artifact visible in real-action reconstruction; shifting the encoding start by one frame flips jerk parity. This is separate from generator exposure bias.
- `model/g1_token_causal_codec.py` uses causal convolutions, two frames/token, K64-compatible decoder history, and default `repeat_interleave(2)` upsampling. Polyphase and rotation-stability changes were planned as matched ablations, not validated solutions.
- Existing losses and decoded supervision do not fully constrain autonomous hard-D selection, earlier-history influence, or degenerate 6D regions. Future experiments should separately test decoder rotation robustness, phase/upsampling behavior, and generated-history training such as Two-Forward/Resampling Forcing.

Failures and how to do differently:
- Do not equate active-looking output with a correct principle, and do not use global smoothing, C scaling, C removal, extra sampler steps, or more width as substitutes for causal controls.
- Do not claim arbitrary latent-noise fragility; normal and real-codec neighborhoods were mostly stable. Attribute only the evidenced degenerate trajectory/geometry mechanism.

References:
- `docs/experiments/reviews/EXP-20260922-fd-causal-codec-generator-root-cause.md`
- `docs/research/CAUSAL_CODEC_GENERATION_READINESS_20260921.md`
- `model/g1_token_causal_codec.py`
- MotionStreamer `https://arxiv.org/abs/2503.15451`

### Task 2: OD complete-sequence root-cause repair audit

task: verify whether the OD codec repair is general rather than sample-specific
task_group: OD C64 codec training coverage and validation

task_outcome: partial

Preference signals:
- when the user said “不要patch一个specific问题，而是做成通用的solution” -> repair shared sampling/target semantics, not individual clips; preserve old runs and avoid smoothing, clipping, or hand-picked exclusions.
- when providing launch guidance, give executable commands but explicitly distinguish package readiness, permission/dry-run status, actual Job submission, and scientific completion.

Reusable knowledge:
- The confirmed defect was training/inference coverage mismatch: old target sampling could omit true sequence starts and transition regions even though full-sequence inference required them. On a failed checkpoint, changing only the supervised range exposed losses such as `53.77 -> 2.337e14`, showing the omitted prefix contained severe errors.
- `dataset/g1_codec_windows.py` implements `WINDOW_PROTOCOL = "source_aligned_complete_target_blocks_v1"`: uniform sequence selection, then uniform non-overlapping source-aligned blocks; every complete two-frame token is covered, including startup and final partial blocks; up to 252 real preceding frames are retained; right padding is masked.
- `model/g1_token_causal_objective.py` supervises frame-zero pose and skips derivatives without real predecessor history. New checkpoint identities include the window protocol, and old incomplete-coverage checkpoints are rejected by resume/re-encode/OD-generator entrypoints.
- Audit evidence: 15426 training sequences, six sources, 467 distinct lengths, 128176 target blocks, 7712902 real frames; 53 broad tests passed; 13 focused tests passed; source-aligned block/full-sequence equivalence passed; published commit `f08df96` matched workspace and installed runtime across 12 runtime files.
- Two real-size updates, exact resume, re-encoding, TF/RF interface checks, and 160-frame generation passed. These prove implementation and execution seams only; they do not prove 100000-step quality.

Failures and how to do differently:
- Formal 100000-step retraining was not submitted in this audit because Kubernetes creation verification returned HTTP 403. Do not say the OD quality problem is solved until the new run’s late loss spikes, per-sample extreme errors, orientation, amplitude, and latent scales are checked.
- Keep old failed weights, caches, and generator inputs isolated; never resume the old protocol or feed its encodings to a new OD generator.

References:
- `dataset/g1_codec_windows.py`
- `tests/test_g1_codec_windows.py`
- `docs/experiments/reviews/EXP-20260924-c64-fd-od-calibrated-rf-complete-sequence-audit-20260925.md`
- `runs/c64_complete_sequence_repair_20260925/{audit.json,proof/receipt.json,tests.log}`
- `.venv311/bin/python -m unittest tests.test_g1_codec_windows tests.test_g1_c64_stack tests.test_g1_supervised_geometry`

## Thread `01a0ccc2-22bc-7850-807f-2d0911811644`
updated_at: 2026-09-25T09:28:12+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T17-20-12-01a0ccc2-22bc-7850-807f-2d0911811644_01a0d2b7-2478-7cd1-964f-ca57a246a170.jsonl
rollout_summary_file: 2026-09-23T05-34-30-SdDu-c64_fd_od_eta_monitoring.md

description: Monitoring and ETA update for ongoing C64 FD/OD and RF rollout training; latest evidence showed codec and FD training complete, OD TF and evaluations still progressing, with export-race and pod-verification caveats
task: cluster-training-eta-monitoring
task_group: Musics2Dance cluster workflow
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
keywords: Musics2Dance, C64, FD, OD, RF, ETA, hot-storage, read_m2d_hot_logs.py, kubectl, KubeSphere, export race, FileNotFoundError

### Task 1: Check C64 FD/OD and RF rollout ETA

task: cluster-training-eta-monitoring
task_group: Musics2Dance cluster workflow
task_outcome: partial

Preference signals:
- When the user said “check eta” and later “check”, the agent should proactively inspect live records and give a concise status/ETA report without asking for detailed scope.
- ETA reports should explicitly separate training, evaluation, videos, and final report completion; the user’s workflow concerns the whole pipeline, not just training steps.

Reusable knowledge:
- Latest observed C64 state at 2026-09-24 22:18 CST: OD codec 100000/100000; OD TF 380/3125 at about 2.1 sec/update; FD ordinary and strong RF both 9375/9375; ordinary FD evaluation complete while strong evaluation was running; OD RF not started.
- Separate RF rollout state: R1 6250/6250 complete; R2 3478/6250 with approximately 9.17 training hours remaining at that snapshot.
- All 24 music batches and OD calibration completed. The music worker later exited during result export, after task completion, with `FileNotFoundError` for `results-records.tar.gz.partial`; downstream OD training continued, so do not rerun music by default.
- Use `.venv311/bin/python scripts/read_m2d_hot_logs.py` against hot-storage JSON/status/metrics files, save a local snapshot under `runs/c64_fd_od_20260924/`, then parse queue statuses and recent rates. Missing remote files with FTP `550 No such file or directory` mean the artifact is unavailable, not necessarily that the stage failed.
- Actual pod/GPU allocation could not be verified from the workspace. For authoritative cluster state, obtain user-side KubeSphere output using `kubectl get pods ...` and `kubectl get jobs ...`.

Failures and how to do differently:
- Do not claim the full pipeline is complete when only training or one evaluation is complete; OD RF, remaining evaluations, comparisons, videos, and report were still pending.
- Label downstream ETA as provisional when its measured rate has not started. Avoid extrapolating FD RF speed directly to OD RF without evidence.
- Treat storage records as progress evidence but request/inspect Kubernetes pod state before asserting which jobs are actually running.
- Investigate export races independently; the observed failure was `FileNotFoundError: [Errno 2] No such file or directory: '/hot/upload/EXP-20260924-c64-fd-od-calibrated-rf/results/results-records.tar.gz.partial'`.

References:
- `runs/c64_fd_od_20260924/check-latest-2218.json`
- `runs/c64_fd_od_20260924/check-latest-2216.json`
- `runs/c64_fd_od_20260924/fd-eval-live-2216.json`
- `runs/c64_fd_od_20260924/eta-latest-readback.json`
- `.venv311/bin/python scripts/read_m2d_hot_logs.py`
- Requested pod check: `kubectl get pods -n ogi-llm --field-selector=status.phase=Running -o wide | grep -E '^(NAME|m2d-)'; kubectl get jobs -n ogi-llm -l app=m2d-c64-fd-od -o wide`

## Thread `01a0cd1e-3517-71a1-849f-acb45c91a9a6`
updated_at: 2026-09-25T11:48:58+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T15-15-04-01a0cd1e-3517-71a1-849f-acb45c91a9a6.jsonl
rollout_summary_file: 2026-09-23T07-15-04-6rfU-causalcodec_cluster_mps_monitoring_and_eta.md

description: Monitored CausalCodec experiments, migrated RF continuation from local 5090 to one H100 with validated two-process CUDA MPS, and reported live ETA; scientific results remain pending
 task: causalcodec experiment monitoring, checkpoint handoff, cluster MPS continuation
 task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 task_outcome: partial
 cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 keywords: CausalCodec, EXP-20260923-fd-codec-causal-mixer, EXP-20260923-fd-rf-rollout-strength, MPS, H100, KubeSphere, ETA, hot-storage, checkpoint, kubectl

### Task 1: Monitor CausalCodec experiments

task: Check Experiment 2 progress, utilization, ETA, and parallel allocation
task_group: CausalCodec cluster monitoring
task_outcome: partial

Preference signals:
- when discussing GPU usage, the user said “可以并行，要记住每张卡里能并行就并行” -> evaluate same-GPU concurrency/MPS as a default operational option while preserving batch size, seed, and scientific semantics.
- when asking for status, the user requested ETA and utilization -> report measured update rate, GPU utilization, current stage, and ETA rather than generic running/not-running status.

Reusable knowledge:
- Experiment 2 has three matched arms: `joint_stable`, `conv_stable`, `attention_stable`; three independent one-GPU workers, seed 1234, 6250 updates per stage.
- Live progress was read through hot storage because local `kubectl`/Slurm were unavailable. Use `scripts/read_m2d_hot_logs.py` and inspect `results/queue.json`, per-stage `status.json`, and logs.

Failures and how to do differently:
- `read_thread` accepts at most `turnLimit=10`; retry oversized calls with 10.
- Do not claim experiment completion from training progress alone; downstream evaluation, renders, and reports must also be checked.

References:
- `Musics2Dance/docs/experiments/EXP-20260923-fd-codec-causal-mixer.md`
- `cluster-transfer/EXP-20260923-fd-codec-causal-mixer/release/APPLY_3H.txt`
- `scripts/read_m2d_hot_logs.py`

### Task 2: Migrate RF training to cluster MPS

task: Stop local R1 at an atomic checkpoint and resume R1/R2 concurrently on one H100
 task_group: RF rollout cluster continuation
 task_outcome: partial

Preference signals:
- when requesting continuation, the user said “在集群继续给我命令” -> provide a directly executable KubeSphere submission command and verify actual Job/Pod state after launch.

Reusable knowledge:
- Local R1 was stopped at checkpoint update 4950/6250; 17 later unsaved updates were intentionally recomputed. The 4,006,940,281-byte `r1-recovery.pt` was uploaded and readback-verified.
- Job `m2d-rf-rollout-strength-1h` runs on `node14` in namespace `ogi-llm`; two private CUDA MPS clients were observed concurrently. R1 resumed from 4950 and R2 started from 0.
- At the latest verified point: R1 5000/6250, R2 52/6250, approximately 13 seconds/update, mean GPU utilization about 69%, ~36 GB HBM. Training ETA was R1 15:30–16:00 CST Sep 24 and R2 09:00–11:00 CST Sep 25; evaluation/videos are additional.
- Key artifacts: `results/packing-proof.json`, `results/train-processes.json`, `results/training/rf_joint_shift1/status.json`, `results/training/rf_joint_free2/status.json`, `results/gpu.csv`.

Failures and how to do differently:
- Wait for and verify a new atomic checkpoint before stopping local training; never switch from an old recovery point merely to start the cluster sooner.
- A KubeSphere API account may be able to read resources but receive 403 on Job creation; distinguish API identity from the privileged web-terminal identity.
- Recovery files can lag status files immediately after launch; retry hot-storage reads before diagnosing failure.

References:
- `cluster-transfer/EXP-20260923-fd-rf-rollout-strength/release/PASTE_1H.txt`
- `runs/rf_rollout_strength_local/cluster-handoff.json`
- `runs/rf_rollout_strength_local/cluster-live-first-recovery.json`
- Job: `m2d-rf-rollout-strength-1h`; Pod: `m2d-rf-rollout-strength-1h-wzqk2`

## Thread `01a0cd52-a44c-7b71-8c87-49b729abc493`
updated_at: 2026-09-24T08:50:12+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T16-12-20-01a0cd52-a44c-7b71-8c87-49b729abc493.jsonl
rollout_summary_file: 2026-09-23T08-12-20-jrML-utars_report_upper_rerun_and_video_package.md

---
description: Updated UTars Feishu technical-report package with lower/upper videos and completed a corrected-inference upper-level 40-episode evaluation; final upper full-task success was 13/40 (32.5%).
task: update UTars technical report with videos and corrected upper evaluation
task_group: /home/wangyukun/ubt_isaac_sim_ws UTars / Isaac Sim / VLA report handoff
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: UTars, Isaac Sim, VLA, Feishu, REPORT.md, 视频索引.md, upper-evaluation, RTC, inference_steps=8, rtc_frozen_steps=8, 13/40, 32.5%, 7/40, PyAV
---

### Task 1: Report video package and metric correction

task: add lower success/failure videos and historical upper success videos to Feishu report
task_group: UTars technical-report handoff
task_outcome: success

Preference signals:
- when the user asked for “7个成功的和一个失败的下层视频，以及之前上层成功视频2个也放上去” and requested upper success rate -> include representative videos plus explicit full-batch denominators and source-batch labels.

Reusable knowledge:
- Lower canonical result is 7/40 actual full completions (17.5%), with 39/40 pickup; do not replace this with legacy stage scores.
- Selected lower videos: successful seeds `2026080507, 2026080510, 2026080517, 2026080519, 2026080520, 2026080601, 2026080605`; failure seed `2026080518` was released and not dropped but had 13.9 cm horizontal error beyond the 12 cm threshold.
- Historical upper videos selected from `20260819_1000_50k_40ep`, seeds `2026080516` and `2026080517`; they are historical-model evidence and must not represent the current model.
- Final package contains 12 videos: 8 lower, 2 newly rerun upper successes, and 2 historical upper successes.

Failures and how to do differently:
- `apply_patch` context matching failed twice on Chinese report text; use exact file reads and narrow Python replacements when patch context is unstable.

References:
- Canonical report: `docs/briefs/utars-techreport-20260922/REPORT.md`
- Feishu copy: `docs/briefs/utars-techreport-20260922/飞书正文.md`
- Video index: `docs/briefs/utars-techreport-20260922/视频索引.md`
- Package: `docs/briefs/utars-techreport-20260922/UTars飞书交接材料.zip`

### Task 2: Corrected-inference upper-level evaluation

task: rerun same-level upper evaluation using the corrected inference pipeline
task_group: UTars closed-loop evaluation
task_outcome: success

Preference signals:
- when the user said “新的推理才是对的” and “不用管严格，只要成功就行啊” -> use full task completion (target layer, release, no drop) as the primary metric; do not fail solely on pickup tilt warnings.
- when the user said “不用一直等” -> run long evaluations in tmux with a status file and automatic postprocessing rather than blocking the conversation.

Reusable knowledge:
- Model: `ubt_vla_ws/ubt_vla_data/r01-old-new-lower-37mix-60k`.
- Evaluation root: `0.logs/n17_v3_batch_eval/20260923_upper_8f8_40ep/`.
- Contract: same 40 fixed seeds as prior upper batch; `episode_steps=900`; fixed scene seed `610719936`, sample index 10; `inference_steps=8`, `rtc_frozen_steps=8`, RTC enabled with reference clipping, replan after 16 actions, upper target interpolation disabled.
- Final result: 40/40 episodes, observed full-task completion 13/40 (32.5%); stage score 33/40; 120 original videos decoded; no client errors.
- Final files: `actual_completion.json`, `REPORT.md`, `video_checks.json`, `reports/full_policy.json`, `STATUS.md`; `exit_code.txt=0`, `postprocess_exit_code.txt=0`.

Failures and how to do differently:
- `ffprobe` was unavailable. Video validation succeeded using PyAV from `ubt_vla_ws/ubt_vla_code/Isaac-GR00T-N1.7/.venv/bin/python`; future checks can use PyAV directly.
- The old upper values `25/40` and `1/40` are stage/strict-stage scores from the pre-repair pipeline, not the corrected full-task success rate. Keep them as historical context only.

References:
- `0.logs/n17_v3_batch_eval/20260923_upper_8f8_40ep/manifest.json`
- `0.logs/n17_v3_batch_eval/20260923_upper_8f8_40ep/actual_completion.json`
- `0.logs/n17_v3_batch_eval/20260923_upper_8f8_40ep/REPORT.md`
- `docs/experiments/EXP-20260902-utars-groot-n17-old-upper-new-lower-37mix.md`
- Final verification output: `actual=13 40`, `errors=0`; ZIP has 20 files and 12 MP4s; report links pass and `REPORT.md == 飞书正文.md`.

## Thread `01a0cd9d-2740-7fe3-b4b5-ae402b63242a`
updated_at: 2026-09-25T05:52:28+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T13-50-05-01a0cd9d-2740-7fe3-b4b5-ae402b63242a_01a0d1f6-c48e-70a1-b7d3-055dd6aed119.jsonl
rollout_summary_file: 2026-09-23T09-33-43-ggCC-fd_od_monitoring_and_audio_checked_video_catalog.md

---
description: Live FD/OD monitoring and durable standard-video delivery conventions; user requires final videos to be audio-complete and accompanied by a unified architecture catalog.
task: monitor_fd_od_and_publish_audio_checked_video_catalog
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: Musics2Dance, FD, OD, H100, queue.json, read_m2d_hot_logs.py, silent.mp4, video catalog, audio mux, C64, RF, PR-57
---

### Task 1: Monitor FD/OD training

task: read live hot-storage queue, music shards, FD TF, and OD codec progress
task_group: c64-fd-od-training-monitoring
task_outcome: success

Preference signals:
- The user asked for current music, FD, and OD progress and remaining time -> report measured progress separately by stage, with explicit uncertainty for downstream stages that have not started.

Reusable knowledge:
- At the 2026-09-24 snapshot, FD TF was `2700/3125` at about `2.15 s/update`, OD codec was `4780/100000` at about `0.339 s/update`, and music was `9 complete / 9 running / 6 pending` across 24 shards.
- GPU lane logs showed three H100 80GB GPUs near full utilization; no evidence supported attributing the measured slowdown primarily to music sharing.
- Generator training supports exact resume via `recovery.pt` with contract/optimizer/RNG/source-order restoration; codec training supports checkpoint resume via `latest.pt`.

Failures and how to do differently:
- A short FTP tail caused `JSONDecodeError: Extra data` when parsing completion JSON. Use larger `--tail-bytes` or queue state rather than parsing truncated completion files.
- FTP `550 No such file or directory` for downstream status files means those stages had not produced artifacts yet; do not classify them as failed without logs.

References:
- `runs/c64_fd_od_20260924/check-status-20260924-live-2.json`
- `runs/c64_fd_od_20260924/check-fivecard-20260924-live.json`
- `scripts/read_m2d_hot_logs.py`

### Task 2: Publish audio-checked standard videos with a unified catalog

task: change standard video generation so only audio-complete final videos are exposed, with per-video architecture metadata
task_group: video-rendering-and-delivery
 task_outcome: success

Preference signals:
- The user said: “要完全做好，视频生成都要有个通用的目录表统一展示每个视频对应的是什么，要写清楚架构，在视频生成代码里就要写成默认” -> make a unified catalog and architecture descriptions the default output of future video-generation pipelines.
- The user asked why some files were silent -> keep silent composites strictly temporary and never mix them with deliverable videos.

Reusable knowledge:
- `scripts/g1_video_catalog.py` publishes only videos whose decode receipt includes verified audio, copies/links final MP4s and previews into `public/`, and writes `index.html`, `CATALOG.md`, `catalog.csv`, and `catalog.json`.
- Renderers now create silent composites/panel MP4s in temporary directories and remove them after audio muxing.
- The FD standard output was verified as 35 final videos and 35 previews, with zero `silent.mp4` files remaining. Hot-storage catalog files were read back successfully.
- Tests: `python -m unittest tests.test_g1_video_catalog` passed 2 tests; generic and C64 720-frame smoke renders passed with full audio/video decode.

Failures and how to do differently:
- Do not expose the render workspace directory as the user-facing video directory. The public directory must contain only final audio-bearing media and catalog files.
- When rebasing onto a moving results branch, expect experiment-spec conflicts; preserve both the new catalog evidence and newer training/repair history.

References:
- Local catalog: `runs/c64_fd_od_20260924/standard-videos/public/index.html`
- Catalog table: `runs/c64_fd_od_20260924/standard-videos/public/CATALOG.md`
- Hot directory: `/1-H集群-热存储/zzy-data/upload/EXP-20260924-c64-fd-od-calibrated-rf/fd-standard-videos-20260925/`
- Feature branch: `codex/c64-standard-video-catalog-20260925`
- PR: `https://github.com/lbtwyk/Musics2Dance/pull/57`
- Main implementation: `scripts/g1_video_catalog.py`, `scripts/render_g1_c64_fd_standard_suite.py`

## Thread `01a0d1c4-44ee-7233-832b-9ec4aba49ffe`
updated_at: 2026-09-26T16:48:34+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T12-54-55-01a0d1c4-44ee-7233-832b-9ec4aba49ffe.jsonl
rollout_summary_file: 2026-09-24T04-54-55-STE2-5090_multi_task_conversation_title_normalization.md

description: 为 5090 主机上的项目对话建立适合多任务长对话的标题规则并完成重命名；最终成功更新 29 条，保留 13 条准确标题，5 条无可见标题记录未改动
 task: rename_5090_project_conversations_for_multitask_threads
 task_group: codex-sidebar-title-maintenance
 task_outcome: success
 cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
 keywords: codex_app__list_threads, codex_app__read_thread, codex_app__set_thread_title, createdAt, Asia/Shanghai, 5090, m2d-5090, multi-task-chat, title-normalization

### Task 1: 5090 多任务对话标题整理

task: rename project-scoped 5090 Codex threads using creation date and dominant workflow theme
task_group: Codex sidebar title maintenance
task_outcome: success

Preference signals:
- 用户先要求统一格式，随后明确说“中间的tag不用，标题要更简洁，更能知道里面的元素” -> 默认使用 `MMDD｜主题`，去掉“功能/研究/修复”等类型标签，主题写具体对象和问题/产物。
- 用户说“我经常一个chat做很多事情”并要求“根据这个再整理” -> 长对话标题应概括持续主线和重要转向，而不是只依据首条消息、最后一条消息或原标题。
- 用户要求“无法判断主题时不要猜，保留原名” -> 对无法形成可靠单一主题的混合对话保留原名。
- 用户说“就做5090上面的” -> 仅处理 `remote-ssh-discovered:ubt-5090` 上属于项目的对话。

Reusable knowledge:
- 最终标题格式为 `MMDD｜主题`；日期取线程 `createdAt`，按 `Asia/Shanghai` 转换，绝不使用 `updatedAt`。
- 同一研究主线中的设计、实现、训练、排障、评估和汇报应合并成一个可检索主题；若后来转向独立任务，应选择最有长期检索价值的主线，必要时并列两个具体要点。
- 5090 项目为 `m2d-5090`（`/home/wangyukun/ubt_isaac_sim_ws/m2d-ws`）和 `ubt_isaac_sim_ws`（`/home/wangyukun/ubt_isaac_sim_ws`）。
- 通过 `read_thread` 验证最终标题和创建日期，最终结果为 29 条更新成功、`wrong:[]`；另有 13 条已准确标题保留，5 条无可见标题历史记录未改动。

Failures and how to do differently:
- `codex_app__list_threads({limit:1000})` 报错：limit 最大为 50。未来使用 `limit:50`，再分页或结合本地状态数据库补齐。
- 初版给标题加入类型标签，用户要求删除；从一开始应直接采用 `MMDD｜主题`。
- 列表摘要不足以判断长对话主线；应读取用户消息序列和对应 rollout，特别检查后续转向。
- 改标题会触发线程更新时间并可能改变可见顺序；只能保证未主动调用排序/置顶/归档操作，不能承诺顺序绝对不变。

References:
- Final prompt principle: “逐条查看对话的起始目标、重要转向和实际产出；同一研究目标下的设计、实现、训练、排障、评估和汇报，概括成一个主题；格式 MMDD｜主题；无法准确概括时保留原名；只修改对话标题。”
- Verification evidence: `{"verified":29,"wrong":[]}`; project labels remained `m2d-5090`, `ubt_isaac_sim_ws`; sidebar sorting remained `chats=updated_at`, `pinned=updated_at`, `projects=manual`; pinned count remained 0.

## Thread `01a0d202-2a1a-73a3-a994-2f1e636edbe6`
updated_at: 2026-09-24T09:25:32+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T14-02-32-01a0d202-2a1a-73a3-a994-2f1e636edbe6.jsonl
rollout_summary_file: 2026-09-24T06-02-32-TDx4-lower_shelf_tracking_and_training_audit.md

description: Lower-shelf N1.7 tracking-error audit and data/training integrity findings; diagnosis complete but no optimization implemented or validated
 task: lower_shelf_tracking_error_and_data_training_audit
 task_group: /home/wangyukun/ubt_isaac_sim_ws
 task_outcome: partial
 cwd: /home/wangyukun/ubt_isaac_sim_ws
 keywords: N1.7, lower-shelf, tracking-error, target-limit, RTC, grasp-feedback, PD, training-contract, tune_top_llm_layers

### Task 1: Tracking-error audit and controller scope

task: distinguish raw policy target, applied target, and physical tracking error; define bounded feedback scope
task_group: lower-shelf inference/physics diagnosis
task_outcome: partial

Preference signals:
- when asked how to fix physical jitter, the user said “不要靠调整pd” -> keep original PD and diagnose inference/execution/physics separately.
- the user chose “允许额外接触反馈参与控制，但保持原PD” -> contact feedback may modify downstream execution, but original PD, force limits, model, physics, and task gates stay fixed.
- the user selected “1a，2a” -> continuously monitor bilateral grasp after pickup with bounded corrections; policy initiates release, feedback only delays release until support is reliable.
- the user selected the bounded option excluding chassis retreat and shelf-entry correction -> do not expand the controller into base motion or route planning without a new decision.

Reusable knowledge:
- `0.logs/n17_v3_tracking_audit_20260924/` is a read-only audit; no simulation, training, PD, or production-code change was made.
- The audit matched 16,756 action endpoints across 10 runs. Joint ordering and per-step alignment passed with zero target/state mismatch.
- Tracking must be split into: raw requested target minus pre-step state; requested target minus final applied target; and previous applied target minus current measured state. The old analysis primarily measured only the third quantity.
- In failed seed 502 at 2–10 s, right-wrist raw request/state p95 was ~25.75°, while ~18.87° was removed by execution limiting. Near drop, wrist errors remained small (roughly 0.03–0.18° medians) while bilateral contact was still present.
- Canonical report: `0.logs/n17_v3_tracking_audit_20260924/REPORT.md`.

Failures and how to do differently:
- Never interpret post-limit low error as faithful raw-policy execution, grasp stability, or actuator saturation.
- Align physics traces per episode; cumulative `physics_tick` values require offset correction before joins.

References:
- `syntheticdatageneration/sdg_utils/n17_v3_diagnostics.py`
- `syntheticdatageneration/scenarios/training/mixins/VlaN17V3RuntimeMixin.py`
- `0.logs/n17_v3_tracking_audit_20260924/audit.json`
- `N17_V3_TARGET_LIMIT_MODE=measured`, `max_joint_step_rad=0.12`

### Task 2: Data/training integrity audit

task: audit lower data, collection feedback, retained checkpoint, and train/inference boundary behavior
task_group: N1.7 experiment integrity
 task_outcome: partial

Preference signals:
- the user requested root-cause evidence before selecting another route -> preserve negative evidence and do not launch retraining or controller variants silently.

Reusable knowledge:
- 500 lower demonstrations and 771,289 frames decoded successfully; 743 attempts produced 500 included successful episodes. No corrupt videos, missing frames, or non-finite numeric values were found.
- A concrete training-contract defect was verified: intended top-four language-layer tuning was omitted from model loading. The retained model has `tune_top_llm_layers: 0`; 176 language-layer tensors are unchanged from factory, while 537 action-head tensors changed. Recording-loader reproduction confirmed the flag omission.
- Every successful collection episode used box-tilt feedback; model inputs do not directly include contact/box telemetry. Dataset coverage was narrow (113 full parameter sets; initial box-position span about 1.67/1.57/1.05 mm), so offline accuracy does not establish robustness to autonomous drift.
- All 500 demonstrations contain a 20.39–27.45° wrist target reset at descent entry, but actual wrist movement was only ~0.00457° median. Treat this as target handoff, not physical jitter.
- Boundary offline probing found ~0.459° midpoint arm RMSE but ~3.158° when forecasting across descent; self-history continuation (768 predictions) showed target handoff timing 4 frames early to 5 late, median 1.5 frames late. These are training-seen, teacher-forced diagnostics, not autonomous success evidence.
- Closure artifact: `0.logs/n17_v3_data_training_audit_20260924/closure.json`; no PD change, production-code change, physical trial, or new training.

Failures and how to do differently:
- Do not claim missing top-four training explains all drops; original training logs/trainer state were unavailable and no causal retraining comparison exists.
- Do not use oracle future-action continuation or training-seen offline probes as deployment/generalization evidence.

References:
- `docs/experiments/reviews/EXP-20260902-data-training-audit-20260924.md`
- `0.logs/n17_v3_data_training_audit_20260924/TRAINING_FINDING.md`
- `0.logs/n17_v3_data_training_audit_20260924/RUNBOOK.md`
- Training flag paths: `launch_utars_v3_finetune.py:118`, `gr00t/model/gr00t_n1d7/setup.py:86`, `qwen3_backbone.py:109`

## Thread `01a0d28e-6fc3-7a12-a067-46412d0c361d`
updated_at: 2026-09-26T16:54:14+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T16-35-45-01a0d28e-6fc3-7a12-a067-46412d0c361d.jsonl
rollout_summary_file: 2026-09-24T08-35-45-99Br-causalcodec_artifact_publication_github_modelscope_hf.md

---
description: Published scoped causalcodec code to GitHub, uploaded verified final/complete artifacts to private ModelScope, skipped HF when direct access failed, and learned the user’s strict artifact-boundary preferences.
task: causalcodec artifact audit and multi-platform publication
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
keywords: causalcodec, C64, C16, ModelScope, GitHub PR 56, Hugging Face, OD music cache, final model, intermediate checkpoint, upload verification, proxy
---

### Task 1: Publish scoped GitHub code and documentation

task: publish current C64 FD/OD causalcodec implementation without large artifacts
task_group: GitHub research handoff
task_outcome: success

Preference signals:
- When asked to publish artifacts, the user said “gh不包含大产物” -> GitHub should contain only scoped code, configs, contracts, reports, and lightweight evidence; exclude `.pt`, audio, videos, caches, archives, and other large runtime artifacts.
- The user later said “只上传最终模型，不要中间产物了” -> distinguish final models from intermediate training checkpoints before publishing anywhere.

Reusable knowledge:
- Isolated worktree: `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/cluster-transfer/codec-latent-results-publish`.
- Commit `22907f3` was pushed to `codex/codec-latent-results-20260924`; PR #56 is `https://github.com/lbtwyk/Musics2Dance/pull/56`.
- PR verification reported `files 100`, `mergeable MERGEABLE`, and `large_artifacts []`.
- Python compilation and `git diff --check` passed. Focused pytest was not runnable because the publication worktree lacked PyTorch and the project venv lacked pytest.

Failures and how to do differently:
- Do not claim full tests passed from this worktree; report syntax validation separately from runtime test availability.

References:
- `git commit -m "feat: publish current C64 FD and OD execution code"`
- `git commit -m "docs: record C64 publication boundary"`
- `gh pr view 56 --json url,files,mergeable,reviewDecision`

### Task 2: Publish final/complete artifacts to private ModelScope

task: upload useful final models and completed caches while excluding intermediate checkpoints
task_group: ModelScope artifact delivery
task_outcome: partial

Preference signals:
- The user explicitly requested final models only: “只上传最终模型，不要中间产物了” -> never upload FD TF base checkpoints or OD recovery snapshots unless the user later explicitly requests snapshots.
- Completed OD music cache and completed calibration were treated as publishable, while OD codec training remained in progress -> label artifact completion independently from experiment completion.

Reusable knowledge:
- Private destination: `lbtwyk/musics2dance-foredance-repro`.
- Verified remote groups: `causalcodec-20260924/fd-c64` (12 files, ~499,698,182 bytes), `causalcodec-20260924/od-calibration` (3 files, ~37,045,269 bytes), `causalcodec-20260924/fd-c64-videos` (5 files, ~21 MB), and `causalcodec-20260924/diagnostic-c16-mixer` (21 files, ~912 MB).
- FD final C64 codec: `runs/codec_latent_results_20260924/records/inputs/c64/codec.pt`, step 100000, code dimension 64; it is a codec/reconstruction result, not generator-quality evidence.
- OD calibration metadata: 2,832 fit sources, 708 development sources, zero source overlap, no official test labels.
- OD C64 was still training; final live readback showed `40000/100000`, `proof=false`. No final OD codec model existed for publication.
- Intermediate upload was stopped and verified absent remotely: `fd-tf-base` and `od-c64-snapshot` listed zero files.
- OD cache source audit: 24 shards complete, 6,610 track entries, 6,610 unique tracks, zero duplicates, shard sizes 275–276 tracks. Local archives completed at 24 files / 13,743,277,293 bytes.

Failures and how to do differently:
- The cache upload was still asynchronous at rollout end. Do not call it complete until `runs/causalcodec_publish_20260924/ms-cache-complete.json` exists and remote listing verifies all 24 archive sizes.
- Exclude `.ms_upload_cache` from remote verification; it is a local upload helper artifact.

References:
- `runs/causalcodec_publish_20260924/upload_od_cache.py`
- `runs/causalcodec_publish_20260924/resume_od_cache.sh`
- `runs/causalcodec_publish_20260924/ms-cache-complete.json`
- `causalcodec-20260924/od-music-cache/shard-0.tar.zst` through `shard-23.tar.zst`
- `runs/causalcodec_publish_20260924/final-live-status.json`

### Task 3: Decide Hugging Face upload

task: attempt HF only if direct transfer is fast and does not require proxy
task_group: Hugging Face connectivity
 task_outcome: success

Preference signals:
- The user clarified “我指的是hf” and said “如果fd要用代理，就算了” -> make one direct no-proxy connectivity check and skip HF when it fails; do not configure a proxy merely to force the upload.

Reusable knowledge:
- With all proxy variables unset, requests to `https://huggingface.co/api/whoami-v2` and `https://huggingface.co` failed with `ConnectionError`/max retries.
- HF upload was correctly skipped; existing local authentication did not overcome the network blocker.

References:
- Direct check command used `env -u HTTP_PROXY -u HTTPS_PROXY -u ALL_PROXY -u http_proxy -u https_proxy -u all_proxy`.
- Result: `ConnectionError HTTPSConnectionPool(host='huggingface.co', port=443)`.

## Thread `01a0d2af-3ffe-7823-9939-52d5a350b8ac`
updated_at: 2026-09-24T12:45:00+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T17-11-35-01a0d2af-3ffe-7823-9939-52d5a350b8ac.jsonl
rollout_summary_file: 2026-09-24T09-11-35-qF1a-bilingual_utars_portfolio_website_video_update.md

---
description: Implemented and published a bilingual, video-first UTars robotics portfolio site with four short clips; latest upper clip was revised after visual review to a more balanced September 23 success sample.
task: implement bilingual robotics portfolio website and evidence clips
task_group: /home/wangyukun/ubt_isaac_sim_ws portfolio publishing
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws
keywords: UTars, Isaac Sim, lbtwyk.github.io, PyAV, video clipping, GitHub Pages, bb303ee, episode_023
---

### Task 1: Publish bilingual robotics portfolio

task: implement bilingual visual portfolio and publish selected UTars videos
task_group: website and portfolio workflow
task_outcome: partial

Preference signals:
- when the user requested “中英双语的视觉作品集” with large videos and concise/fancy descriptions -> preserve bilingual, visual-first presentation and avoid unnecessary technical detail.
- when the user rejected an upper clip as visually unbalanced -> compare the full successful cohort visually and do not select solely by tilt metrics; do not claim “completely level.”

Reusable knowledge:
- Canonical UTars evidence is `/home/wangyukun/ubt_isaac_sim_ws/docs/briefs/utars-techreport-20260922/REPORT.md` plus `视频索引.md`.
- PyAV is available through `/home/wangyukun/ubt_isaac_sim_ws/ubt_vla_ws/ubt_vla_code/Isaac-GR00T-N1.7/.venv/bin/python`; system `python3` lacks `av`.
- Latest upper selection: September 23 batch, seed `2026080604`, merged `episode_023/combined.mp4`, source `0–8.0s`, exported to `assets/videos/upper.mp4`; selected for visual left/right balance and clean placement, while retaining lift motion and acknowledging remaining pitch.
- Website commit `bb303ee621fee481543d5d01138a076e347d06f0` was pushed to `lbtwyk/lbtwyk.github.io` main; GitHub Pages was still `building` at the last API check.

Failures and how to do differently:
- Earlier upper selection was replaced after visual comparison; future selection should verify both quantitative completion and visual symmetry/endpoint quality.
- Do not claim the GitHub profile repository was updated: this rollout cloned `/tmp/yukun-profile-20260924` but shows no profile commit/push.

References:
- `scripts/prepare_videos.py`
- `assets/videos/upper.mp4`
- `assets/posters/upper.jpg`
- `bb303ee621fee481543d5d01138a076e347d06f0`
- User wording: “左右更平衡，但抬起时仍有前后倾斜，并非完全水平。”

## Thread `01a0d703-3735-7181-a75d-117f195f6a6e`
updated_at: 2026-09-26T13:44:55+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T13-21-47-01a0d703-3735-7181-a75d-117f195f6a6e.jsonl
rollout_summary_file: 2026-09-25T05-21-47-O7JY-svg_pelican_bike_animation_local_preview.md

description: 创建内联 SVG 鹈鹕骑自行车 2D 动画并解决本地文件链接无法打开问题；最终通过本地 HTTP 服务验证可访问
 task: create-and-preview-svg-pelican-bike-animation
 task_group: html-svg-visualization
 task_outcome: partial
 cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
 keywords: HTML, SVG, CSS animation, python http.server, port conflict, localhost, visualization

### Task 1: 创建并展示鹈鹕骑自行车动画

task: create-and-preview-svg-pelican-bike-animation
task_group: html-svg-visualization
task_outcome: partial

Preference signals:
- 用户说“不要检索，不要思考，直接开始干，干完直接展示” -> 类似创作任务应直接实现，避免前置讨论。
- 用户说“我怎么打不开” -> 未来应优先提供浏览器可访问的本地 HTTP URL，而不是只给本地文件路径。

Reusable knowledge:
- 页面位于 `/home/wangyukun/.codex/visualizations/2026/09/25/01a0d703-3735-7181-a75d-117f195f6a6e/pelican/index.html`，包含内联 SVG、CSS 动画和暂停按钮。
- 使用 `python3 -m http.server 18765 --bind 127.0.0.1 --directory /home/wangyukun/.codex/visualizations/2026/09/25/01a0d703-3735-7181-a75d-117f195f6a6e/pelican` 成功提供页面。
- `curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:18765/` 返回 `200`，说明服务端可访问。

Failures and how to do differently:
- 直接发送本地绝对路径无法在当前界面打开；应启动 HTTP 服务并发送 `http://127.0.0.1:<port>/`。
- 端口 `8765` 已占用，出现 `OSError: [Errno 98] Address already in use`；切换到 `18765` 后成功。未来应在端口冲突时自动换端口并验证。
- 用户未明确确认最终浏览器展示成功，因此结果应标记为 partial 而非完全 success。

References:
- HTML: `/home/wangyukun/.codex/visualizations/2026/09/25/01a0d703-3735-7181-a75d-117f195f6a6e/pelican/index.html`
- URL: `http://127.0.0.1:18765/`
- Error: `OSError: [Errno 98] Address already in use`

## Thread `01a0d703-eed8-7c12-b917-3b15bb36329e`
updated_at: 2026-09-27T15:39:20+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T13-22-34-01a0d703-eed8-7c12-b917-3b15bb36329e.jsonl
rollout_summary_file: 2026-09-25T05-22-34-yRj0-od_c64_complete_sequence_root_cause_repair_and_verification.md

description: General OD C64 codec root-cause repair changed incomplete sequence sampling to complete source-aligned target coverage; 100k retraining and 144-clip evaluation completed with major improvement, but residual extreme-input/high-jerk tails remain and OD generator training is still gated.
task: od-c64-complete-sequence-coverage-repair
 task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
 task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: OD, C64, causal codec, CausalMotionWindows, source-aligned targets, startup supervision, KubeSphere, run_kubesphere_command.py, hot storage, PR 56

### Task 1: General sequence-coverage repair

task: replace sample-specific OD startup patch with shared complete-sequence sampler
task_group: Musics2Dance codec training
 task_outcome: success

Preference signals:
- The user required “根因修复，不要patch一个specific问题，而是做成通用的solution” -> preserve shared mechanism fixes and reject per-sample clipping/smoothing/workarounds.
- The user requested “你都要给我命令直接启动” -> provide a complete executable cluster command whenever launch is authorized.

Reusable knowledge:
- `dataset/g1_codec_windows.py` implements `CausalMotionWindows`: uniform sequence selection, uniform non-overlapping source-aligned target blocks, up to 252 real preceding frames, complete-token coverage, and masked right padding.
- The new checkpoint identity protocol is `source_aligned_complete_target_blocks_v1`; old incomplete-coverage checkpoints/OD inputs must not resume or feed the new generator.
- Validation: 53 tests passed; all 467 observed sequence lengths covered; full-size codec and TF/plain-RF/strong-RF exact-resume proofs plus 160-frame generation passed; independent reviewer PASS.

Failures and how to do differently:
- The earlier startup-only repair fixed loss masking but not sampler coverage. Always validate both objective masks and the actual sampling distribution across all sequence lengths.

References:
- `dataset/g1_codec_windows.py`
- `tests/test_g1_codec_windows.py`
- Commit `f08df96ae211ef0cc6149b85ec9b97018bc49d3a`; later docs commit `3999d1413b957507fac17801fef2653c1722b41d`

### Task 2: Full-run check and residual-tail audit

task: check completed OD complete-sequence run and report evidence-scoped outcome
task_group: KubeSphere training/evaluation audit
 task_outcome: partial

Reusable knowledge:
- Job `m2d-od-c64-complete-sequence-20260925` completed successfully (node13, exit 0); codec, re-encoding, and 144 held-out evaluations completed.
- Compared with startup-only repair: joint MAE median `16.044° -> 1.477°`, root orientation `24.556° -> 1.055°`, amplitude ratio `0.360 -> 0.994`, severe clips `6/144 -> 0/144`, and million-plus logged losses `124/5000 -> 0/5000`.
- Remaining issue: 340/18541 cached clips have standardized residual magnitudes >20; five largest-tail clips show reconstructed jerk intensity 1.87–3.69× reference. This is diagnostic only; do not claim all OD quality is solved or start OD generators without further investigation.
- Use the webpage-terminal automation, not ordinary management API status alone: `scripts/run_kubesphere_command.py` can query/create jobs through the verified user terminal; read exact Job/Pod state and hot-storage completion records before retrying or reporting stale 403 status.

Failures and how to do differently:
- Keep live scheduler state, completion artifacts, and experiment docs synchronized; stale “not submitted/403” text persisted until the later check.
- Do not silently filter, smooth, or clip extreme tracks; investigate coordinate/time continuity and component-wise reconstruction errors first.

References:
- Hot results: `/hot/upload/EXP-20260924-c64-fd-od-calibrated-rf/complete-sequence-repair-20260925/results/`
- Report: `docs/experiments/reviews/EXP-20260924-c64-fd-od-calibrated-rf-complete-sequence-results-20260927.md`
- PR: `https://github.com/lbtwyk/Musics2Dance/pull/56`
- Stage comment: `https://github.com/lbtwyk/Musics2Dance/pull/56#issuecomment-5848013553`

## Thread `01a0d743-c8ca-76c2-b455-07047969f47f`
updated_at: 2026-09-27T15:23:31+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T14-32-18-01a0d743-c8ca-76c2-b455-07047969f47f.jsonl
rollout_summary_file: 2026-09-25T06-32-18-QZn9-m2d_experiment_planning_and_localhost_memory_overgeneralizat.md

---
description: Planned two H100 representation experiments; later traced unsolicited localhost video URLs to an overgeneralized memory from one HTML animation incident and corrected the source instead of adding a blanket rule.
task: representation-experiment-planning-and-delivery-behavior-correction
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
 task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
keywords: C64, causal-VAE, D+C, H100, experiment-ledger, representation-videos, localhost, memory-overgeneralization
---

### Task 1: Plan first two representation experiments

task: plan C64 full-continuous generation and scratch causal-VAE comparison
 task_group: Musics2Dance research experiments
 task_outcome: partial

Preference signals:
- when requesting the first two experiments, the user said: “要从头开始的就从头开始…各自一h100拉满速度” -> use scratch initialization where required and plan one maximally utilized H100 per experiment.

Reusable knowledge:
- Intended fair comparison: reuse the frozen C64 codec for full-continuous latent generation; train causal VAE from scratch with a matched scratch D+C control using the same repaired data protocol.
- Experiment lifecycle is ledger-driven; inspect contracts and use exact preflight/launch-packet evidence. No formal launch was verified here.

Failures and how to do differently:
- Do not claim implementation, submission, or training completion from source inspection and planning alone.

References:
- `Musics2Dance/docs/research/CAUSAL_CODEC_DUAL_LATENT_VAE_MOTION_SPACE_REVIEW_20260925.md`
- `Musics2Dance/train_g1_c64_stack.py`
- `Musics2Dance/train_g1_codec_latent_capacity.py`
- `.venv311/bin/python scripts/experiment_ledger.py outline EXP-20260924-c64-fd-od-calibrated-rf`

### Task 2: Correct unsolicited localhost URL behavior

task: trace and repair overgeneralized local-HTML delivery memory
 task_group: memory/source correction
 task_outcome: success

Preference signals:
- The user explicitly rejected merely adding a rule: “你要找出为什么会给出网址，然后改掉这个，而不是加一条规则” -> trace the provenance of unwanted behavior and correct the originating memory/source.

Reusable knowledge:
- Root cause was an overgeneralization of the pelican SVG incident: a one-off failure opening local HTML led to a memory instruction to use localhost generally. That evidence does not support a default for experiment video directories.
- The three newly added workspace/video-delivery rules were removed; the correction was recorded at `/home/wangyukun/.codex/memories/extensions/ad_hoc/notes/20260927-localhost-overgeneralization-correction.md`.

Failures and how to do differently:
- Do not promote a scoped workaround into a global preference. Preserve the incident as history, but remove imperative/generalized “use localhost over file://” guidance from memory sources.

References:
- `/home/wangyukun/.codex/memories/rollout_summaries/2026-09-25T05-21-47-O7JY-create_pelican_bicycle_svg_animation.md`
- `/home/wangyukun/.codex/memories/extensions/ad_hoc/notes/20260927-localhost-overgeneralization-correction.md`
- User wording: “不是，你要找出为什么会给出网址，然后改掉这个，而不是加一条规则”

## Thread `01a0d77e-593f-72a0-868a-e49f7c470b33`
updated_at: 2026-09-26T17:19:22+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T15-36-16-01a0d77e-593f-72a0-868a-e49f7c470b33.jsonl
rollout_summary_file: 2026-09-25T07-36-16-6zJx-kubesphere_hot_storage_command_automation_skill.md

---
description: Verified automatic 5090-to-KubeSphere command execution and reusable skill for hot-storage delivery, logs, and Job lifecycle operations.
task: kubesphere_hot_storage_and_command_automation
 task_group: m2d-ws-kubesphere-operations
task_outcome: success
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: KubeSphere, kubectl, websocket, SSH jump host, hot storage, Job create delete, run_kubesphere_command.py, kubesphere-operations
---

### Task 1: Automate KubeSphere commands

task: Validate and implement automatic Job creation, inspection, deletion, and remote command execution from 5090.
task_group: KubeSphere cluster operations
task_outcome: success

Preference signals:
- When the user said “这样不需要我每次都手动粘贴” and later requested “可以创建删除任务等等” -> future similar work should provide a reusable execution tool and verify the real mutation lifecycle, not only provide commands for manual paste.

Reusable knowledge:
- 5090 reaches KubeSphere through the existing SSH jump host. The jump host cannot resolve `ubk8s.ubtrobot.com`, so use the verified console IP `10.10.92.3:30880` with Host header `ubk8s.ubtrobot.com:30880`; the route is not a permanent IP guarantee and should be rechecked if the endpoint changes.
- The working path is: SSH jump -> local port forward -> `/oauth/token` login -> WebSocket `/kapis/terminal.kubesphere.io/v1alpha2/users/{user}/kubectl` -> send terminal messages and read output.
- WebSocket requires both `Authorization: Bearer <token>` and `token=[REDACTED_SECRET] Cookie; Bearer-only handshake timed out.
- `scripts/run_kubesphere_command.py` executes a local shell script remotely in the authenticated user’s KubeSphere kubectl terminal, chunks long base64 payloads, captures an explicit exit marker, saves a JSON receipt, and propagates the remote exit code.
- Real proof: `m2d-command-proof-6642112a` was created in `ogi-llm`, read back, had no Pod/GPU allocation (`parallelism=0`), deleted, and confirmed absent. A >7KB script with Chinese output and `exit 7` also returned exit code 7 locally.

Failures and how to do differently:
- Direct Kubernetes API Job creation returned 403 for the OAuth route, while the same account’s web kubectl terminal returned `kubectl auth can-i create/delete jobs -n ogi-llm: yes`; do not generalize one interface’s RBAC result to the other.
- On timeout/disconnect, mutation outcome is unknown. Query the exact Job/Pod first; never blindly retry create/delete/start.
- A dry-run request still requires the real create permission and cannot bypass RBAC.

References:
- `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/scripts/run_kubesphere_command.py`
- `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/runs/kubesphere-access-20260925/create-delete-proof.json`
- `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/runs/kubesphere-access-20260925/exit-proof.json`
- Official terminal route: `terminal.kubesphere.io/v1alpha2/users/{user}/kubectl`

### Task 2: Create kubesphere-operations skill

task: Package verified KubeSphere hot-storage and command workflows as a reusable Codex skill.
task_group: Codex skill creation
 task_outcome: success

Preference signals:
- When the user said “把kubesphere的集群热存储和命令相关的工作流做成skill” -> future agents should invoke/reuse `kubesphere-operations` for these workflows instead of rediscovering the transport and permissions.

Reusable knowledge:
- Installed skill: `/home/wangyukun/.codex/skills/kubesphere-operations/`.
- It contains `SKILL.md`, `references/hot-storage.md`, `references/cluster-commands.md`, and `agents/openai.yaml`.
- The skill reuses project scripts rather than duplicating them. It documents verified hot-storage paths, incremental upload/readback, log-tail retrieval, Job create/query/delete/replace, exact-target authorization, and separation of prepared/uploaded/submitted/running/completed evidence.
- It explicitly preserves safety boundaries: no credential/token printing, no kubeconfig in hot storage, no cross-user operations, no broad deletion, and no blind mutation retries.
- Validation passed with `quick_validate.py`; referenced project files were checked and all existed; `run_kubesphere_command.py --help` succeeded.

Failures and how to do differently:
- Do not treat hot-storage upload or a Job manifest as proof of submission or execution. Re-query the cluster and inspect actual Pods/logs/outputs.
- Do not use the skill’s M2D paths for unrelated PVCs/projects without verifying the mapping.

References:
- `/home/wangyukun/.codex/skills/kubesphere-operations/SKILL.md`
- `/home/wangyukun/.codex/skills/kubesphere-operations/references/hot-storage.md`
- `/home/wangyukun/.codex/skills/kubesphere-operations/references/cluster-commands.md`
- Validation: `python3 /home/wangyukun/.codex/skills/.system/skill-creator/scripts/quick_validate.py /home/wangyukun/.codex/skills/kubesphere-operations`

## Thread `01a0de93-7687-7e72-a4e6-d038bcdecc27`
updated_at: 2026-09-27T15:39:19+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T00-36-41-01a0de93-7687-7e72-a4e6-d038bcdecc27.jsonl
rollout_summary_file: 2026-09-26T16-36-41-rCgD-standardized_g1_video_grid_delivery.md

---
description: Implemented and validated a default standardized G1 60-second comparison-grid pipeline with up to nine labelled panels, unified audio/video catalogs, and automatic completion gates; one model group completed, OD group remained pending.
task: standardized_g1_video_grid_pipeline
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: g1_video_catalog.py, build_g1_standard_grid.py, grid60, catalog.json, CATALOG.md, BeatIt, song-switch, validate_video, audio-complete, OD chunk transfer
---

### Task 1: Standard 60-second labelled model grid

task: create reusable default comparison-grid rendering and catalog workflow
task_group: G1 video delivery
task_outcome: success

Preference signals:
- The user requested “最多比如9个视频”, clear method/module labels in every panel, and standardized video directories -> future model video deliveries should default to a labelled grid plus unified catalog, not scattered MP4s.
- The user asked for this to be “所有模型训练完后的视频渲染默认流程” -> finalizers should automatically require standard source renders, grid generation, catalog creation, and audio/video validation before reporting delivery complete.

Reusable knowledge:
- `scripts/build_g1_standard_grid.py` supports 1–9 panels and creates one 60-second, 30fps, 1800-frame grid per standard song/program. It checks matching audio, seed, source track, start frame, frame count, panel receipts, and full decode.
- `scripts/g1_video_catalog.py` publishes only verified final MP4s/previews and writes `public/index.html`, `public/CATALOG.md`, `public/catalog.csv`, and `public/catalog.json`.
- Standard panel sources must be complete final renders; missing source videos leave the grid incomplete and must not be substituted with older model output.
- The shared workflow is wired into `run_g1_rf_cof_standard_suite.py`, `run_g1_rf_rollout_local.py`, and `deliver_g1_granularity_standard.py`; project defaults are documented in `AGENTS.md` and `docs/research/modules/G1_STANDARD_60S_VIDEO_GRID.md`.

Failures and how to do differently:
- An initial run was interrupted while importing heavy dependencies (`scipy/librosa`); use the repo `.venv311` and project ffmpeg helper for future runs.
- A configuration patch briefly introduced an indentation error in `build_g1_standard_grid.py`; it was fixed and compilation/shell/JSON/diff checks passed.
- `ffprobe` is unavailable as a system command; use project `validate_video`/imageio-ffmpeg rather than assuming ffprobe exists.

References:
- `scripts/build_g1_standard_grid.py`
- `scripts/g1_video_catalog.py`
- `scripts/render_g1_causal_native_comparisons.py::validate_video`
- `docs/research/modules/G1_STANDARD_60S_VIDEO_GRID.md`
- `AGENTS.md` standard 60-second grid requirement

### Task 2: Completed model-group grid delivery

task: render and verify standard 60-second grids for a completed model group
task_group: G1 standard video delivery
task_outcome: success

Reusable knowledge:
- `runs/latent_chunk_history_20260926/standard-delivery/grid60/manifest.json` reports `status=complete`, `count=21`.
- `runs/latent_chunk_history_20260926/standard-delivery/grid60/public/catalog.json` also reports `status=complete`, `count=21`.
- All 21 records were checked for existing video/preview files, 1800 frames, and passed verification; panel counts were 6 or 7.
- Group completion is recorded in `runs/latent_chunk_history_20260926/standard-delivery/completion.json` with `grid60_videos: 21` and the public path.

References:
- `runs/latent_chunk_history_20260926/standard-delivery/grid60/public/`
- `public/videos/long_012_60s.mp4` and matching preview
- `public/index.html`, `public/CATALOG.md`, `public/catalog.csv`, `public/catalog.json`

### Task 3: OD full-data model grid

task: attach OD full-data training delivery to the same labelled grid workflow
task_group: OD chunk-transfer standard delivery
task_outcome: partial

Reusable knowledge:
- OD configuration defines explicit labels for latent chunk, latent RF, latent velocity, motion velocity, and OD C64 D+C RF; baseline labels can distinguish FD C64 RF and reference panels.
- OD delivery is intended to produce 175 standard source videos first, then an OD-specific 21-video grid with explicit OD/FD labels.

Failures and how to do differently:
- At rollout end, `runs/od_chunk_transfer_20260927/standard-delivery/completion.json` and `grid60/manifest.json` did not exist. Do not report OD grid completion.
- The already-running OD standard delivery had been launched with `--skip-grid`; a separate `m2d-od-chunk-grid60` tmux watcher was added to wait for group completion and rerun delivery without skipping the grid.

References:
- `runs/od_chunk_transfer_20260927/watch-standard.sh`
- `runs/od_chunk_transfer_20260927/watch-grid60.sh`
- `configs/experiments/20260927-od-chunk-delivery.json`
- tmux sessions `m2d-od-chunk-standard` and `m2d-od-chunk-grid60`

## Thread `01a0dea3-394a-7a13-8e87-72f793d06ada`
updated_at: 2026-09-26T18:17:37+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T00-53-54-01a0dea3-394a-7a13-8e87-72f793d06ada.jsonl
rollout_summary_file: 2026-09-26T16-53-54-PrLQ-od_chunk_methods_accelerated_five_lane_training.md

---
description: Full-OD chunk-method comparison and exact-trajectory acceleration; five H100 lanes resumed successfully, but final quality evidence was not yet available
task: select_fd_chunk_methods_retrain_on_full_od_with_c64_dc_enhanced_rf_baseline_and_accelerate_execution
task_group: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: OD, C64, D+C, enhanced-RF, chunk, seam-constraint, latent, CUDA-graphs, exact-resume, KubeSphere, ogi-llm, hot-storage, 90000-updates
---

### Task 1: Select OD chunk methods and baseline
task: choose promising FD chunk methods, add seam constraints, and retrain on full OD
task_group: OD chunk transfer experiment
task_outcome: partial

Preference signals:
- when the user asked to “挑几个现在看起来结果比较好的chunk方法” and “加上我们用到的接缝约束” -> select candidates from completed FD evidence and preserve seam constraints in the OD comparison.
- when the user specified “64的dc增强rf作为baseline” -> retain C64 D+C enhanced RF as the explicit matched baseline.
- the route kept the full OD population and retained extreme values without clipping, smoothing, or deletion -> similar comparisons should not silently reduce OD to FD scale or hide difficult inputs.

Reusable knowledge:
- The accepted OD input is the complete-sequence-repair C64 codec: 100,000 updates, full re-encoding, and 144-track reconstruction evaluation improved joint median 16.044→1.477°, orientation 24.556→1.055°, amplitude 0.360→0.994, and severe failures 6/144→0/144. This is codec evidence only; it does not establish OD generator quality.
- Full OD generator data inspected remotely contained 15,426 codec-training sequences, 10,923 reliable music-paired sequences, and 671,528 source groups. All groups had real targets; 5,961 groups had fewer than eight targets and were retained rather than padded.
- The formal route is `EXP-20260927-od-chunk-transfer`: 90,000 updates, 48 source groups/update, seed 1234, full OD data, and separate RF continuation. Scientific acceptance remains false.

Failures and how to do differently:
- OD codec tail anomalies remain (340/18,541 cached sequences with standardized residual >20; largest tails correlate with visible input tails). Do not treat finite reconstruction or improved medians as proof that all OD inputs are healthy.
- Do not infer generator or long-dance quality from codec reconstruction; generator evaluation must complete independently.

References:
- `docs/experiments/EXP-20260927-od-chunk-transfer.md`
- `docs/experiments/contracts/EXP-20260927-od-chunk-transfer.json`
- `runs/od_chunk_transfer_20260927/selection-results.json`
- `/hot/upload/EXP-20260924-c64-fd-od-calibrated-rf/complete-sequence-repair-20260925/results/od/inputs`

### Task 2: Accelerate and migrate five H100 training lanes
task: prove execution-only acceleration and replace running Jobs from archived checkpoints
task_group: KubeSphere OD training operations
 task_outcome: success

Preference signals:
- the user accepted acceleration only after exact state comparisons and requested continuation from existing progress -> future migrations should archive recovery state, prove same trajectory, then replace the Job.
- the rollout repeatedly separated measured TF speed from unmeasured RF speed -> report phase-specific throughput and never extrapolate without evidence.

Reusable knowledge:
- Exact same-checkpoint proofs passed: ordinary latent chunk 0.532→0.374 s/update (42.2%), latent seam-constrained 0.725→0.416 (74.5%), motion seam-constrained 0.523→0.348 (50.1%), C64 D+C baseline TF 2.045→1.771 (15.5%). Model, optimizer, source-order, and (for baseline) RNG state matched after the comparison windows.
- Acceleration used 64 CUDA-graph cache entries, batched physical-history transfer, and reduced redundant baseline computation. Scientific batch, seed, loss, data, music conditions, and 90,000-update budget were unchanged.
- Five accelerated Jobs ran under `ogi-llm` with H100 GPUs and zero restarts; cutover points were approximately 1918, 3704, 3502, 3770, and 976 updates. Old checkpoints were preserved at hot storage `speed/cutover/<cell>/before-execution-change.pt`.
- Release `dce3c9019961` was uploaded and hot-storage readback verified. Contract lint returned `0 error(s)` and 25 focused tests passed.

Failures and how to do differently:
- Diagnostic logging outside an isolated `speed-probe` output was rejected. Keep speed probes isolated.
- First post-migration measurements include graph-cache warmup; use stable later windows for reporting.
- Do not claim RF speedup based on TF measurements; RF-stage speed remained to be measured.

References:
- `runs/od_chunk_transfer_20260927/SPEED.md`
- `runs/od_chunk_transfer_20260927/ACCELERATED.json`
- `runs/od_chunk_transfer_20260927/speed-final-ready/execution-proof.json`
- `runs/od_chunk_transfer_20260927/speed-final-ready/check-final.json`
- `scripts/run_kubesphere_command.py`
- `m2d-update-dce3c9019961.pyz` (hot-storage readback verified)

### Task 3: Finish training, evaluation, and video delivery
task: continue five OD runs through RF, scoring, native OD evaluation, and standard videos
task_group: OD experiment completion
task_outcome: partial

Reusable knowledge:
- At rollout end, formal runs were still early; RF phases, final evaluations, native OD scores, scientific report, and standard video delivery were pending.
- Prepared downstream deliverables included 175 standard audio videos and 21 continuous-cut/60-second combinations. These must be reported only after actual artifacts and readback verification exist.
- Keep operational completion separate from scientific acceptance; no quality conclusion was established in this rollout.

## Thread `01a0e2b7-6160-73a2-8353-70c4a0be9f28`
updated_at: 2026-09-28T02:21:21+00:00
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws
rollout_path: /home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T19-54-23-01a0e2b7-6160-73a2-8353-70c4a0be9f28.jsonl
rollout_summary_file: 2026-09-27T11-54-23-vH8A-native34_c64_dc_rf_cluster_training.md

---
description: Current token-causal CausalCodec64 was adapted to native 34D with D+C, calibrated MRT2 music, enhanced RF, and 16-frame commits; local/H100 proofs passed and formal codec training was running, but downstream quality stages were pending.
task: adapt current CausalCodec64 from native38 to native34 and train D+C enhanced RF on cluster
task_group: Musics2Dance native34 C64 experiment
 task_outcome: partial
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance
keywords: CausalCodec64, native34, g1_yaw_delta, D+C, RF, MRT2, H100, KubeSphere, exact-resume, 16-frame-commit, experiment-ledger
---

### Task 1: Implement native34 CausalCodec64 route

task: current token-causal C64 with native34 motion, not legacy chunk-causal 34D
task_group: native34 representation adaptation
task_outcome: success

Preference signals:
- The user explicitly confirmed “当前 CausalCodec64 改为 34D，其他保持当前配置” and authorized cluster training -> preserve the current C64 architecture and do not substitute the existing legacy34 experiment.
- The user asked for high GPU utilization and faster computation -> preserve scientific settings and require exact-state proof before execution optimizations.

Reusable knowledge:
- Native34 is `g1_yaw_delta`: local planar translation 2D, height 1D, yaw sin/cos 2D, and 29 joint DOFs; it removes root roll/pitch. It is not a 38D tensor with channels deleted.
- Native34 adaptation must update geometry, yaw accumulation, decoded supervision, joint/rotation slices, state handling, evaluation conversion, and standard rendering. Merely setting `motion_dim=34`, padding zeros, or retaining native38 losses is invalid.
- Frozen route: FineDance 183 train/18 test, seed1234, 48 source groups/update, C64 codec trained from scratch for 100000 updates, then TF3125 + enhanced joint RF9375 = 12500 generator updates, 16-frame/0.5333s commits, calibrated past/style/future music attention, NFE10.

Failures and how to do differently:
- Initial contract lint failed because `training_preflight` was absent; add the exact real-route preflight before launch. Final lint passed with 0 errors.
- Historical 38D data used different sampling/training semantics; never claim a pure representation-only causal effect from that comparison.

References:
- `docs/experiments/EXP-20260927-fd-c64-34d-dc-rf.md`
- `docs/experiments/contracts/EXP-20260927-fd-c64-34d-dc-rf.json`
- `model/g1_token_causal_objective.py`
- `scripts/run_g1_c64_34d.py`
- `tests/test_g1_c64_34d.py`

### Task 2: Validate and run cluster training

task: local and H100 preflight, then formal KubeSphere Job
 task_group: KubeSphere training execution
 task_outcome: partial

Preference signals:
- The user expects execution to continue through cluster launch once approved; distinguish submitted, running, completed, evaluated, and accepted states.

Reusable knowledge:
- Local proof passed 11 tests, codec/TF/RF exact model/optimizer/source/RNG recovery, causal generation, scoring, and full audio/video decode.
- Independent reviewer `/root/native34_review` returned `PASS`.
- Job `m2d-c64-34d-rf-0927`, Pod `m2d-c64-34d-rf-0927-2wl24`, namespace `ogi-llm`, node13, H100 80GB.
- H100 target proof passed at codec batch64, generator microbatch256, RF supervision730, with exact recovery and downstream score/audio checks.
- Latest observed formal status in the rollout: codec 63060/100000, about 0.262 s/update, zero restarts, finite losses, recovery checkpoint updating, and last-10-minute GPU utilization averaging 68.3% with 90% peak.
- Downstream artifacts were still absent: final codec, encoded inputs, codec evaluation, TF, RF, numerical evaluation, standard videos, and 21 grids.

Failures and how to do differently:
- Do not equate proof completion or early codec progress with final quality.
- Keep standard rendering off the training GPU and wait for checkpoint-bound source manifests and decode receipts.
- If monitoring, query the exact Job/Pod and hot-storage artifacts; do not resubmit an existing Job.

References:
- `runs/c64_34d_20260927/RUN_INFO.md`
- `runs/c64_34d_20260927/stage-closure-20260928.json`
- `runs/c64_34d_20260927/latest-detail.json`
- `runs/c64_34d_20260927/status.sh`
- `runs/c64_34d_20260927/formal-confirmed.json`
- Hot root: `/hot/upload/EXP-20260927-fd-c64-34d-dc-rf`

