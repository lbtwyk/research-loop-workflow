thread_id: 019fcb3b-c1f8-7331-a079-a169b3af742f
updated_at: 2026-08-12T08:50:00+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/08/04/rollout-2026-08-04T13-25-18-019fcb3b-c1f8-7331-a079-a169b3af742f.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# Workspace H200 docs were reconciled, the smoke-job flow was corrected, and the later 100-episode closed-loop comparison completed with arm-only clearly outperforming full-policy.

Rollout context: workspace `/home/wangyukun/ubt_isaac_sim_ws`; primary thread about the GR00T N1.7 / H200 workflow, then later a closed-loop batch comparison on the 30,000-step local checkpoint. The user repeatedly pushed for up-to-date docs, exact next steps, and finally asked where the videos are.

## Task 1: Reconcile the latest H200 smoke-job workflow and submission path

Outcome: success

Preference signals:

- The user asked, "你再看一下最新更新过的h200文档，是不是流程你想错了" -> future agents should re-read the latest H200 docs instead of relying on earlier assumptions or memory of old Pod/StatefulSet/MPIJob workflows.
- The user asked for "给我详细怎么做，一步步教我" -> future agents should default to step-by-step operational guidance when giving H200 instructions.
- The user’s corrections made it clear that KubeSphere and the 5090 do not share a filesystem; future agents should not tell the user to "put the YAML in the KubeSphere current directory" and should instead produce a copy/paste heredoc from the 5090 side.
- The user’s follow-up about the docs showed they care about current state over earlier plans; future agents should check `docs/h200-current-state.yaml` and the latest H200 workflow doc before advising.

Key steps:

- Read the latest H200 workflow docs and state file and found the current authoritative submission path.
- Verified the smoke YAML with the dedicated validator and confirmed it was the expected contract (`H200_SMOKE_JOB_OK`).
- Corrected the submission flow to use `syntheticdatageneration/script/vla_n17_fullbody/print_kubesphere_apply.sh`, which emits a KubeSphere-ready heredoc from the 5090 side.
- Confirmed the final smoke Job contract: v2 image, node08/node10 only, one GPU, H200 preflight, and 100-step smoke.

Failures and how to do differently:

- The earlier guidance that implied copying the YAML into the KubeSphere terminal was wrong; the 5090 and KubeSphere environments do not share a filesystem.
- The first cut also over-relied on a generic Pod watch pattern; the updated workflow uses the specific Job name and the validator-generated contract.
- When the docs change, do not preserve stale assumptions about the submission path or the environment boundary.

Reusable knowledge:

- The authoritative H200 state lived in `docs/h200-current-state.yaml`, then `docs/H200_SIMPLE_WORKFLOW.md`, then the experiment spec.
- The smoke YAML that passed validation was `0.logs/h200_jobs/job-same-shelf-500-smoke.yaml`.
- `validate_h200_smoke_job.py` confirmed the exact contract and printed `H200_SMOKE_JOB_OK`.
- `print_kubesphere_apply.sh` is the right way to hand the Job to KubeSphere; it emits a full `kubectl apply -f - <<'EOF' ... EOF` block.

References:

- [1] `python3 syntheticdatageneration/script/vla_n17_fullbody/validate_h200_smoke_job.py 0.logs/h200_jobs/job-same-shelf-500-smoke.yaml` -> `H200_SMOKE_JOB_OK`
- [2] `print_kubesphere_apply.sh` output shape: `kubectl apply -f - <<'EOF' ... EOF`
- [3] H200 doc update: Job `utars-groot-n17-same-shelf-500-smoke-v2`, image `ubhub.ubtrobot.com/ogi/wangyukun-groot-n17-h200:cu128-torch271-v2`, hosts `node08,node10`, `gpu=1 run_mode=smoke max_steps=100`

## Task 2: Run and compare the 100-episode closed-loop batches for arm-only vs full-policy

Outcome: success

Preference signals:

- The user repeatedly checked status with short prompts like "现在呢" / "现在结果怎么样" / "现在呢"; future agents should respond with concise current-state summaries that include progress counts and concrete artifact paths.
- The user asked where the videos are after completion, so future agents should surface exact video directories and counts, not only success rates.
- The user’s correction about the latest docs implied they want the current operational plan to be evidence-backed; for batch evals, provide the live counts, report paths, and codec checks.

Key steps:

- Added a preflight to `run_sdg_n17_v3_closed_loop.sh` so a stale policy-server port fails before Isaac Sim starts; this prevented repeating the earlier `12319`/`12317` mismatch.
- Ran the 100-episode `locked_arms` batch first on the fixed training snapshot and same 100 seeds.
- Then ran the 100-episode `full_policy` batch on the same seeds, same snapshot, same server port.
- Summarized each condition and compared them with `compare_n17_batch_reports.py`.
- Verified all 200 final videos were H.264.

Failures and how to do differently:

- The first full-batch attempt failed because the policy server URL/port was stale; the fix was to add an explicit server health preflight and use the known-good `12317` port.
- During the long batch, some `.tmp.mp4` files and intermediate result files were still moving; do not finalize until the result counts, per-condition video counts, and temp-file counts settle.
- The run is serial for a reason: parallel startup had previously hit a Vulkan allocation failure. Keep the serial pattern if the environment is unchanged.

Reusable knowledge:

- `locked_arms` finished with 100/100 rows, pick 88%, place 86%, final task 86%, strict final 0%; all 100 videos were H.264 and had no temp files left.
- `full_policy` finished with 100/100 rows, pick 48%, place 34%, final task 34%, strict final 0%; all 100 videos were H.264 and had no temp files left.
- The unified H.264 check over the batch videos returned `UNIFIED_MP4_H264 total=200 bad=0`.
- The comparison artifact was `0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/comparison.json`.
- The stable per-condition reports were `0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/reports/locked_arms.json` and `reports/full_policy.json`.
- The per-condition video roots were `0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/videos/locked_arms` and `.../videos/full_policy`.

References:

- [1] Arm-only report: `pick=0.88`, `place=0.86`, `final_task=0.86`, `strict_final_task=0.0`
- [2] Full-policy report: `pick=0.48`, `place=0.34`, `final_task=0.34`, `strict_final_task=0.0`
- [3] Comparison output: locked arm-only beat full-policy by 52 percentage points on relaxed final-task success (`86%` vs `34%`)
- [4] Video directory layout: `.../videos/locked_arms/episode_000_dual_view.mp4` and `.../videos/full_policy/episode_000_dual_view.mp4`
- [5] The batch video total was 200 MP4s, about 313 MB across both conditions

## Task 3: Explain where the generated videos live

Outcome: success

Preference signals:

- When the user asked "视频都在哪里", the important thing was not just the path but a ready-to-open directory and counts per condition.
- Future agents should answer video-location questions with the exact top-level directory plus condition subdirectories and file naming pattern.

Key steps:

- Checked the batch artifact layout on disk.
- Confirmed two condition subdirectories under the batch `videos/` root, each with 100 MP4s.

Reusable knowledge:

- The correct batch video root is `/home/wangyukun/ubt_isaac_sim_ws/0.logs/n17_v3_batch_eval/20260806_30000_100ep_stage_video/videos/`.
- Inside it are `locked_arms/` and `full_policy/`.
- Each episode video is named like `episode_000_dual_view.mp4`.
- Total size was about 313 MB for both conditions combined.

References:

- [1] `find .../videos -maxdepth 2 -type d` returned the root plus `videos/full_policy` and `videos/locked_arms`
- [2] `locked_arms`: 100 MP4s, about 143 MB
- [3] `full_policy`: 100 MP4s, about 170 MB
- [4] Example filenames: `episode_000_dual_view.mp4` through `episode_099_dual_view.mp4`
