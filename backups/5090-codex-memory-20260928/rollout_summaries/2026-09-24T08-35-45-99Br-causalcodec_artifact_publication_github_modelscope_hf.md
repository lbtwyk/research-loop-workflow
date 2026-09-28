thread_id: 01a0d28e-6fc3-7a12-a067-46412d0c361d
updated_at: 2026-09-26T16:54:14+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T16-35-45-01a0d28e-6fc3-7a12-a067-46412d0c361d.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Audited and published causalcodec artifacts across GitHub, ModelScope, and Hugging Face

Rollout context: The user asked to find useful local/cluster causalcodec outputs, models, caches, and code; publish code to GitHub and large artifacts to ModelScope, with Hugging Face only if fast. The user clarified that GitHub must not contain large artifacts, HF should be skipped if it requires a proxy, and finally requested “只上传最终模型，不要中间产物了”.

## Task 1: GitHub code and research publication

Outcome: success

Preference signals:

- The user said “gh不包含大产物” -> keep GitHub limited to code, configs, contracts, reports, and lightweight evidence; do not commit model weights, audio, videos, caches, or archives.
- The user later requested “只上传最终模型，不要中间产物了” -> distinguish final models from intermediate checkpoints before publishing, and remove/avoid training-stage snapshots.

Key steps:

- Audited the dirty main checkout and isolated causalcodec-related changes in worktree `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/cluster-transfer/codec-latent-results-publish`.
- Added current C64 FD/OD implementation, contracts, speed/cutover scripts, verification scripts, tests, and experiment documentation.
- Committed and pushed commit `22907f3` to branch `codex/codec-latent-results-20260924`.
- Created GitHub PR #56: https://github.com/lbtwyk/Musics2Dance/pull/56
- Verified PR is mergeable, contains 100 files, and contains no large artifact extensions.

Failures and how to do differently:

- Focused pytest could not run in the isolated publication worktree: the project `.venv311` lacked pytest, while system pytest lacked PyTorch. Python syntax compilation and `git diff --check` passed. Future publication summaries should state this validation boundary rather than claiming full tests passed.

Reusable knowledge:

- The repository’s workflow requires preserving unrelated dirty changes and publishing scoped code/docs only.
- The accepted FD C64 codec is a codec/reconstruction selection result, not generator-quality evidence; old C16 routes remain diagnostic only.

References:

- PR: `https://github.com/lbtwyk/Musics2Dance/pull/56`
- Branch: `codex/codec-latent-results-20260924`
- Commits: `889b2af feat: publish current C64 FD and OD execution code`; `22907f3 docs: record C64 publication boundary`
- Main C64 artifact source: `runs/codec_latent_results_20260924/records/inputs/c64/codec.pt`, 100,000 steps, code dimension 64.

## Task 2: ModelScope artifact publication

Outcome: partial

Preference signals:

- The user requested final models only and explicitly rejected intermediate artifacts -> do not publish FD TF base checkpoints or OD recovery snapshots.
- The user accepted completed caches and completed calibration as useful deliverables, while OD codec training was still running -> publish completed artifacts with explicit status labels, and do not present in-progress checkpoints as final models.

Key steps:

- Confirmed private repository `lbtwyk/musics2dance-foredance-repro`.
- Uploaded and remotely size-verified FD final C64 codec bundle under `causalcodec-20260924/fd-c64` (12 files, about 500 MB).
- Uploaded and verified completed OD calibration under `causalcodec-20260924/od-calibration` (3 files, about 37 MB); metadata records 2,832 fit sources, 708 development sources, zero overlap, and no official test labels.
- Uploaded and verified C64 reconstruction videos and C16 mixer diagnostics; these are diagnostic evidence, not final generator models.
- Started background upload of 24 OD music-cache archives. At the final readback, 9/24 cache archives were remotely verified; local preparation was complete for all 24 archives (6,610 unique tracks, about 13.7 GB). A resume watchdog was installed, but the final completion marker was not yet observed.
- Stopped the attempted upload of FD TF-base and OD C64 recovery checkpoints before publication; ModelScope listing confirmed `fd-tf-base` and `od-c64-snapshot` were empty, and temporary local copies were removed.

Failures and how to do differently:

- The first FD bundle verification accidentally included ModelScope’s `.ms_upload_cache`; verification was corrected to exclude it.
- Cache upload remained asynchronous and incomplete at rollout end. Treat the cache as partial until `runs/causalcodec_publish_20260924/ms-cache-complete.json` exists and remote listing confirms all 24 sizes.

Reusable knowledge:

- ModelScope upload code must assert repository privacy and verify every remote file’s size after upload.
- Use `scripts/archive_m2d_progress_to_modelscope.py` patterns and `HubApi.upload_folder`/`upload_file`; avoid uploading runtime artifacts or intermediate checkpoints.
- OD C64 was still training: latest live status was 40,000/100,000, `proof=false`; there was no final OD codec model to publish.

References:

- ModelScope dataset: `https://modelscope.cn/datasets/lbtwyk/musics2dance-foredance-repro`
- Publication workspace: `Musics2Dance/runs/causalcodec_publish_20260924/`
- Cache completion marker: `runs/causalcodec_publish_20260924/ms-cache-complete.json`
- Cache remote prefix: `causalcodec-20260924/od-music-cache/`
- Live status evidence: `runs/causalcodec_publish_20260924/final-live-status.json`

## Task 3: Hugging Face connectivity decision

Outcome: success

Preference signals:

- The user clarified “我指的是hf” and then said “如果fd要用代理，就算了” -> perform one direct connectivity check; skip HF entirely if direct access fails rather than configuring or using a proxy.

Key steps:

- Direct requests to Hugging Face failed with `ConnectionError`/max retries after unsetting proxy variables.
- HF upload was skipped as requested.

References:

- Direct check result: `https://huggingface.co/api/whoami-v2` and `https://huggingface.co` both failed without proxy variables.
- Existing authenticated HF identity was present locally, but connectivity—not authentication—was the blocker.
