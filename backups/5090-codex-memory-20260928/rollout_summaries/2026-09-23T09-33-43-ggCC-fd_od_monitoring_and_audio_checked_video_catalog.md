thread_id: 01a0cd9d-2740-7fe3-b4b5-ae402b63242a
updated_at: 2026-09-25T05:52:28+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T13-50-05-01a0cd9d-2740-7fe3-b4b5-ae402b63242a_01a0d1f6-c48e-70a1-b7d3-055dd6aed119.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Monitoring and standard-video catalog improvements

Rollout context: Work occurred in `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`, covering live FD/OD training monitoring and a request to make generated videos clearly organized and audio-verified.

## Task 1: FD/OD live progress and ETA

Outcome: success

Key steps:
- Read hot-storage queue and status files through `scripts/read_m2d_hot_logs.py`.
- At the 2026-09-24 05:50 UTC snapshot: FD TF was `2700/3125` at about `2.15 s/update`; OD codec was `4780/100000` at about `0.339 s/update`; music had 9 completed, 9 running, and 6 pending shards.
- GPU lane logs showed all three H100 80GB cards near full utilization, so there was no evidence that music sharing caused a major slowdown at that point.
- Verified that training entrypoints support exact checkpoint recovery: FD/OD generator training uses `recovery.pt`, validates contract identity, restores optimizer/RNG/source order, and handles SIGTERM; codec training writes `latest.pt` and supports resume.

Reusable knowledge:
- The configured queue originally allowed only three single-GPU lanes, with up to two trainers or four music clients per GPU. The queue is dependency-driven and preserves task state in `results/queue.json`.
- Music is split into 24 balanced shards totaling 366,489 forecast rows. The status reader may return truncated completion JSON tails; use the queue task state or sufficiently large tail reads rather than blindly parsing a short tail.
- The later repository contract documents a five-card-style separation preference, but this rollout did not actually submit a five-card replacement. Do not claim that a rescheduling change was executed without a new scheduler readback.

Failures and how to do differently:
- A first ETA aggregation failed with `JSONDecodeError: Extra data` because completion JSON was read from a truncated tail. Increase `--tail-bytes` or use queue status for completion classification.
- Several requested status files returned FTP `550 No such file or directory`; missing artifacts mean the downstream stage had not started, not that it had failed.

References:
- `runs/c64_fd_od_20260924/check-status-20260924-live-2.json`
- `runs/c64_fd_od_20260924/check-fivecard-20260924-live.json`
- `scripts/read_m2d_hot_logs.py`
- Queue snapshot: OD codec `4780/100000`, FD TF `2700/3125`, music `9 complete / 9 running / 6 pending`.

## Task 2: Make standard video delivery audio-safe and self-describing

Outcome: success

Preference signals:
- The user asked: “要完全做好，视频生成都要有个通用的目录表统一展示每个视频对应的是什么，要写清楚架构，在视频生成代码里就要写成默认” -> future video-generation work should default to a unified catalog, explicit model architecture/panel mapping, and final-video-only delivery.
- The user questioned why some files were silent -> distinguish temporary silent composition files from deliverable videos and prevent users from encountering intermediates.

Key steps:
- Identified `silent.mp4` as an intermediate created before source-audio muxing, not the intended deliverable.
- Added `scripts/g1_video_catalog.py`, which publishes only audio-verified final MP4s/previews into `public/` and writes `index.html`, `CATALOG.md`, `catalog.csv`, and `catalog.json` with song, split, seed, time range, panel position, labels, and architecture descriptions.
- Changed standard renderers to use temporary work directories for silent composites/panels and clean them automatically after muxing.
- Applied the catalog behavior to causal-native renders, RF/CoF standard renders, and the C64 FD/OD report renderer; added a C64 FD standard-suite entrypoint.
- Re-published the existing FD set: 35/35 videos, 35 previews, all audio/video decode checks passed, zero remaining `silent.mp4` files in the result tree. Hot-storage catalog files were read back successfully.
- Added tests rejecting silent videos and stale public media; `tests.test_g1_video_catalog` passed 2 tests. Real 720-frame smoke tests for both generic and C64 render paths passed.
- Committed and pushed on branch `codex/c64-standard-video-catalog-20260925`; draft PR: https://github.com/lbtwyk/Musics2Dance/pull/57, clean and mergeable against the C64 results branch at the time of checking.

Reusable knowledge:
- Local final catalog: `runs/c64_fd_od_20260924/standard-videos/public/index.html` and `public/CATALOG.md`.
- Hot-storage catalog directory: `/1-H集群-热存储/zzy-data/upload/EXP-20260924-c64-fd-od-calibrated-rf/fd-standard-videos-20260925/`.
- A video is eligible for publication only if its verification receipt reports complete decoded video and audio; catalog publication rejects missing audio.
- Architecture descriptions must be attached to panel arms, not inferred only from display labels.

Failures and how to do differently:
- The first documentation patch failed because expected surrounding lines had changed; inspect the current file context before patching.
- Rebasing the catalog branch onto the newer codec-results branch produced a documentation conflict; it was resolved by preserving both the repair history and the video-catalog entry, then tests were rerun.

References:
- `scripts/g1_video_catalog.py`
- `scripts/render_g1_c64_fd_standard_suite.py`
- `tests/test_g1_video_catalog.py`
- Commit after rebase: `4505576` (remote branch initially pointed to `6e9b123`; force-with-lease updated it).
- PR #57: `https://github.com/lbtwyk/Musics2Dance/pull/57`
