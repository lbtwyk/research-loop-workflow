thread_id: 01a0ae92-039d-74d0-8c08-7c3a5f0d6acb
updated_at: 2026-09-24T05:57:21+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T16-53-19-01a0ae92-039d-74d0-8c08-7c3a5f0d6acb.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# Diagnosed lower-shelf evaluation jitter, completed follow-up evaluation, and archived evidence

Rollout context: `/home/wangyukun/ubt_isaac_sim_ws`; the user wanted root-cause analysis and repair of visibly jittery lower-level videos, then requested complete results/evidence be preserved in their GitHub repository.

## Task 1: Diagnose and repair lower-level inference/execution jitter

Outcome: partial

Preference signals:
- The user explicitly asked “要根因修复” rather than a cosmetic smoothing workaround -> future work should trace model output, RTC conversion, execution timing, and physical outcomes before tuning parameters.
- The user wanted complete evidence, including failures and videos, not only a headline metric -> preserve all runs, reports, and verification artifacts.

Key steps:
- Inspected the active lower-level evaluation, runtime mixin, RTC helpers, inference server, model processor, reports, and per-episode traces.
- Confirmed the policy uses relative joint actions while RTC continuation was vulnerable to applying actions against the wrong reference state; the previous action chunk must be inserted inside `collated_inputs["inputs"]["action"]`, not passed as a top-level `get_action(action=...)` argument.
- Investigated horizon/continuation indexing, latency-aware frozen prefixes, state normalization, waist timing, joint limiting, contact/drop accounting, and execution traces.
- Ran multiple controlled repair/diagnostic batches and retained the reports, logs, traces, and videos.

Reusable knowledge:
- N1.7 v3 contract is action horizon 32, execution/replan horizon 16, RTC overlap 16, frozen prefix originally 4; relative body-joint actions require decoding against the current state.
- A successful pick does not imply successful lower placement. The lower bottleneck is after pickup: lowering, transport, release, and withdrawal.
- Main lower evaluation before repair: 36/40 pick, 0/40 place, 37 drop records; later success-first evaluation: 39/40 pickup and 7/40 actual completions.
- Follow-up audit found no client errors or expired requests, but did not record full physics traces; do not attribute every failure solely to the model or claim deterministic reproducibility.

Failures and how to do differently:
- Early conclusions that remaining failures were definitely model-only were too strong; the same seed previously succeeded and later failed.
- A final pose can be acceptable while a process drop flag remains true; preserve original scoring and report the measurement ambiguity rather than rewriting the result.
- `ffmpeg` was unavailable; use the installed Isaac/GR00T Python environment with OpenCV/PyAV for video inspection.

References:
- Main eval root: `0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/`
- Final report: `.../REPORT.md`
- Results: `.../same_shelf_lower_level/runs/full_policy/merged/n17_v3_closed_loop_results.jsonl`
- Runtime: `syntheticdatageneration/scenarios/training/mixins/VlaN17V3RuntimeMixin.py`
- RTC: `syntheticdatageneration/sdg_utils/n17_v3_rtc.py`, `script/vla_n17_fullbody/n17_v3_rtc_infer.py`, `script/vla_n17_fullbody/n17_v3_rtc_reference.py`
- Final verified focused tests: 59 passed.

## Task 2: Preserve complete results in GitHub

Outcome: success

Preference signals:
- The user said “就放到主分支，证据也放到repo就行不要发布” and “readme把这次作为主结果” -> publish artifacts directly to the repository main branch, avoid a new Release, and lead the README with the current result.
- The user asked which videos succeeded/failed -> maintain an explicit 1-based episode index mapping success/failure to repository paths.

Key steps:
- Confirmed private repository `https://github.com/lbtwyk/utars-isaac-vla-pipeline`, branch `main`.
- Published the result/source branch, then merged/pushed the content to `main`.
- README now leads with 7/40 actual completions (17.5%), 39/40 pickup, and the qualification that this is simulation evidence rather than a reliable real-robot success claim.
- Uploaded all 1,456 evidence files in bounded batches after an HTTP 408 interrupted the first larger-batch attempt; final upload receipt reported `ALL EVIDENCE ON MAIN 6117badd4b7e8edbac2238a5807dcda7444771bd` and exit 0.
- Local manifest/hash verification passed for all 1,456 files; the latest run includes 120 original videos and 40 combined aliases. No new Release was retained.

Reusable knowledge:
- Repository evidence-sync should be independent of issue/PR discussion; only update discussion for stage results or decisions.
- Large evidence uploads should use small bounded commits/batches; the 400 MiB batch hit GitHub HTTP 408, while 64 MiB batches resumed successfully.
- Keep explicit upload status, commit IDs, manifests, and verification logs. The final online recheck later hit GitHub TLS/EOF, so completion claims were based on successful push receipts and local final-commit inventory.

Failures and how to do differently:
- The first attempt created a draft Release and uploaded large assets, but the user explicitly changed the requirement to main-branch repository storage; the draft Release was deleted and unused local archives were removed.
- Do not claim remote completeness from a failed API refresh; distinguish successful push receipts/local verification from live remote re-fetch evidence.

References:
- Repository: `https://github.com/lbtwyk/utars-isaac-vla-pipeline`
- README result: `README.md`
- Video index: `docs/results/lower-20260918/VIDEOS.md`
- Evidence root: `docs/evidence/lower-20260918/`
- Main completion commit: `6117badd4b7e8edbac2238a5807dcda7444771bd`
- Success episodes (1-based): 7, 10, 17, 19, 20, 21, 25; failures: all other 33 episodes.
