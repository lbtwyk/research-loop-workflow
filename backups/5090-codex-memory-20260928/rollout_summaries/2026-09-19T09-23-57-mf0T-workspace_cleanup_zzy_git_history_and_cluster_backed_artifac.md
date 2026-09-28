thread_id: 01a0b8fa-c664-7df2-b061-3b1b31a32643
updated_at: 2026-09-26T18:16:14+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/19/rollout-2026-09-19T17-24-49-01a0b8fa-c664-7df2-b061-3b1b31a32643_01a0b8fb-8fa8-7723-bbb1-e491d2e1b1ce.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# Workspace cleanup and disk-recovery rollout completed

Rollout context: In `/home/wangyukun/ubt_isaac_sim_ws`, the user wanted obsolete intermediate products, uploaded cluster artifacts, stale images, and zzy's no-longer-needed local history removed while preserving current working models, data, code, active jobs, and useful evidence. The user explicitly said: “只要是上传过集群的都可以当作有” and later authorized removing zzy's Git history because he had left.

## Task 1: Remove obsolete local GR00T/LingBot artifacts and caches

Outcome: success

Preference signals:

- The user said “只要是上传过集群的都可以当作有” -> for future cleanup, historical proof of upload/cluster consumption is sufficient to treat a local copy as disposable, without requiring live cluster access unless stronger verification is requested.
- The user repeatedly asked to keep the newest working model and remove old fine-tuning outputs -> use exact, evidence-backed paths and preserve current inference/evaluation artifacts by default.

Key steps:

- Removed five older fine-tuned GR00T model directories previously uploaded to or consumed by cluster jobs: 10k same-shelf, 30k same-shelf, 50k single-shelf, matched-two-task, and old-upper/all-lower 37mix. Total logical bytes removed: `62,941,224,749`. Kept the current model `ubt_vla_ws/ubt_vla_data/r01-old-new-lower-37mix-60k`, base model, and current evaluation report.
- Removed obsolete lower-evaluation videos (~1.3 GB), old GR00T optimizer state (~12 GB), old M2D v1 image and builder cache (~8.5 GB), and several cluster-backed LingBot artifacts recorded in cleanup manifests.
- Removed zzy-owned LingBot checkpoint copies, stale images, old environments, HF/pip/uv/LarkShell/NVIDIA/npm caches, and other verified disposable artifacts while preserving code, model/data trees, experiment archives, and manifests.
- Removed completed GitHub evidence-upload clone `/tmp/utars-results-20260921` after confirming 1,456 files, all hashes verified, clean worktree, and final commit `6117badd4b7e8edbac2238a5807dcda7444771bd`; freed about 7.43 GB.
- Removed verified audit archive parts and an unused temporary M2D environment; freed about 20.3 GB.
- Removed a published/locally loaded M2D v2 image archive; freed about 4.91 GB.
- Removed a completed ModelScope advancement staging tree after `transfer-completion.json` reported `complete: true`, no failures, and verified groups; freed about 46.6 GB.
- Removed an image compiler archive after registry publication with digest receipt; freed about 5.0 GB.

Reusable knowledge:

- Current GR00T inference model: `/home/wangyukun/ubt_isaac_sim_ws/ubt_vla_ws/ubt_vla_data/r01-old-new-lower-37mix-60k`.
- Current lower-evaluation evidence: `0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/manifest.json` and `REPORT.md`.
- Shared/hard-linked directories can greatly overstate reclaimable space. Compare inode/link counts and actual free-space change rather than trusting `du` totals.
- Docker image sizes are not additive; check active containers, image IDs/digests, and `docker system df -v` before deleting images or caches.
- Do not claim live cluster verification from local upload records; this host lacked Kubernetes access. State clearly when deletion relies on historical upload/consumption evidence.

Failures and how to do differently:

- A first cleanup script used the wrong field name in `closure.json` and failed with `KeyError: 'download_identities_verified'`; the corrected check used `closure['checks']['download_identities_verified']` before deletion.
- Removing an image tag alone did not immediately reclaim disk because builder layers remained; `docker builder prune -f` was required.
- A 16.5 GB `/tmp/ulab-latest.tar.gz` belonged to `user:user`, so deletion as `wangyukun` was denied and it was preserved.
- Two similar M2D result directories were not duplicates: 15 matched large files were byte-different, so both were retained.

References:

- Cleanup records are under `0.logs/cleanup/`, including `20260919_uploaded_old_groot_models_removed.json`, `20260924-modelscope-advancement-cleanup.json`, `20260924-compiler-image-archive.json`, `20260924_zhong_obsolete_caches_env_removed.json`, `20260924_zhong_git_history_removed.json`, `20260926_completed_utars_upload_clone_removed.json`, `20260926_verified_audit_parts_and_old_env_removed.json`, and `20260926_old_m2d_v2_image_archive_removed.json`.
- Disk snapshots: about 61 GB free at the start of the 2026-09-26 check, about 92 GB free after the final cleanup sequence.

## Task 2: Remove zzy's obsolete Git history

Outcome: success

Preference signals:

- The user said that because zzy had left, “git历史没有用了吧，把大文件删掉应该也没问题” -> when explicitly authorized, remove the departed user's local Git metadata while preserving working files and clearly recording the irreversible loss of local history.

Key steps:

- Diagnosed `/home/zhongzhengyang/lingbot-vla-v2/.git` at roughly 176–188 GB, mainly historical multi-GB model checkpoints. The user's largest `syntheticdatageneration/.git` was about 12 GB; M2D `.git` was about 1.2 GB.
- Checked large Git blobs and found model checkpoint history, not merely duplicate pack copies. Earlier unreachable objects were only about 170 KB, so pruning them would not solve the space issue.
- After explicit authorization, inventoried 17 zzy-owned `.git` directories and removed only those metadata directories, preserving working trees. Logical Git metadata removed: `209,583,710,208` bytes (~195.2 GiB); observed free-space increase was about 194.4 GiB.
- Verified no zzy Git directories remained and key working files still existed: `lingbot-vla-v2/README.md`, `deploy/lingbot_vla_v2_policy.py`, `syntheticdatageneration/scenarios`, SmolVLA archives, LingBot base model files, and LingBot data.

Reusable knowledge:

- Removing `.git` metadata does not remove the working tree; it removes local commit history, branches, reflogs, and the ability to recover prior versions locally.
- The zzy Git history contained large checkpoint blobs such as ~5 GB safetensor shards and was not safely reducible by deleting a few duplicate files; history rewrite or full metadata removal was required.
- Before deleting another user's Git metadata, verify no active processes/container mounts, snapshot the inventory and heads/status, restrict deletion to exact `.git` directories, and verify working-tree paths afterward.

References:

- Inventory: `0.logs/cleanup/20260924_zhong_git_history_inventory.tsv`.
- Pre-delete heads/status: `0.logs/cleanup/20260924_zhong_git_history_heads_status.txt`.
- Final cleanup record: `0.logs/cleanup/20260924_zhong_git_history_removed.json`.
- The final verification reported zzy's directory at about 168 GB and zero remaining `.git` directories.

## Task 3: Final disk check and duplicate-result investigation

Outcome: success

Key steps:

- Final disk check showed about 92 GB available, with zzy's directory at about 168 GB and M2D `runs` at about 649 GB.
- Confirmed the completed evidence upload clone was fully verified before deletion.
- Compared large files in `c64_od_codec_root_cause_20260925` and `c64_complete_sequence_repair_20260925`; 15 matched large paths were all byte-different, so no result directory was deleted.
- Preserved active/current M2D runs and cluster-transfer artifacts because they were recent or lacked sufficient deletion evidence.

Failures and how to do differently:

- Similar-looking result trees must be compared by content (`cmp`/hash), not directory size or matching filenames alone.
- Current or recently modified training/evaluation outputs should remain until their experiment lifecycle and cluster delivery state are explicitly closed.

