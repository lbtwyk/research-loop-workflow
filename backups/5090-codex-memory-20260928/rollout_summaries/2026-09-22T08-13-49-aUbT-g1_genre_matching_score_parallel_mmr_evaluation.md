thread_id: 01a0c82d-a4df-7591-ba05-19ea0651f1e1
updated_at: 2026-09-24T06:25:33+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T16-13-49-01a0c82d-a4df-7591-ba05-19ea0651f1e1.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Implemented and completed a G1-adapted Genre Matching Score evaluation alongside MMR+

Rollout context: In `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`, the user asked to add the literature’s Genre Matching Score to ongoing experiments and evaluate old mainline plus new local experiments in parallel with MMR+. The official FineDance paper defines GS as cosine similarity between learned music-style and dance-genre embeddings, but the public repositories did not include the retrieval module or usable released GS weights. The user therefore chose an explicitly labeled independent `GS-G1` adaptation, not comparable numerically to the human-motion FineDance GS.

## Task 1: Research and design the GS metric adaptation

Outcome: success

Preference signals:

- The user asked for the prior literature metric to be added “和mmr+平行” and allowed major decisions to be grilled -> future evaluation work should preserve existing metrics and report the new metric separately, without replacing or combining scores.
- The user accepted the independent G1 adaptation after the official implementation/weights could not be verified -> clearly label adapted metrics and avoid presenting them as official or directly comparable to paper numbers.
- The user required old mainline and new experiments to be evaluated, later clarifying “还有resampling的” -> include all explicitly requested experiment families and preserve historical/reference arms.

Key steps:

- Verified FineDance ICCV 2023 paper definition: GS is cosine similarity between AST-based music style embeddings and AGCN-based dance genre embeddings, trained with matched/mismatched genre supervision.
- Inspected both public FineDance repositories and issues #16/#18; the public code tree contains generation/training files but no released Genre & Coherent Aware Retrieval Module, and the issues requesting that code had no answer.
- Confirmed local G1 motions cannot be passed directly to a human-body GS evaluator, motivating a separate G1 skeleton adaptation.
- Recorded the route in the history experiment’s `gs_g1` scope rather than creating a parallel experiment tracker.

Reusable knowledge:

- Official FineDance GS evidence is sufficient for the metric concept, not for direct local reuse: paper formula is cross-modal cosine similarity; public code does not expose the retrieval evaluator or verified checkpoint.
- The accepted local adaptation uses AST audio features plus a native G1 FK/AGCN motion branch, jointly trained with genre-supervised cosine objectives. It must be called `GS-G1` and not be compared numerically with the human-motion FineDance table.

References:

- `docs/research/GENRE_MATCHING_SCORE_ADAPTATION_20260922.md`
- `configs/experiments/gs_g1.json`
- FineDance paper: ICCV 2023 / `https://openaccess.thecvf.com/content/ICCV2023/papers/Li_FineDance_A_Fine-grained_Choreography_Dataset_for_3D_Full_Body_Dance_ICCV2023_paper.pdf`
- Official repository: `https://github.com/li-ronghui/FineDance`
- Unresolved upstream issues: FineDance issues #16 and #18

## Task 2: Implement, review, train, and validate GS-G1

Outcome: success

Key steps:

- Implemented the fixed evaluator contract: 183-song population, grouped split of 146 fit / 37 validation songs across 35 independent audio groups, AST AudioSet 0.4593 backbone, native G1 motion features, seed 1234, 3000 updates, batch 32, FP32.
- Downloaded and strictly converted the AST author’s 352,587,836-byte AudioSet checkpoint using the official Transformers v4.30 mapping. Conversion loaded 86,187,264 backbone parameters; classification heads were excluded; numerical parity with the original timm runtime was not claimed.
- Fixed a validation bootstrap issue by resampling complete audio groups while retaining equal-song estimates; validation reports both song and independent-audio-group counts.
- Added exact-resume and trainability checks. Real-data CPU proof passed: both audio and motion weights updated, finite gradients, exact next-step replay after optimizer/RNG restore, and the real held-out validation path ran on 37 songs.
- Added a GPU serialization lock so GS training and local stability evaluation cannot use the 5090 concurrently. The initial queue incorrectly waited on a monitoring process even when the GPU was idle; only the unstarted waiter was stopped and replaced.
- Full batch-32 GPU proof passed with exact resume and both branches updating; peak allocation was 13,117,452,288 bytes (~12.22 GiB). Formal training completed 3000 updates in roughly 1226 seconds at ~0.32–0.33 seconds/update.
- Final validation signal passed: paired margin mean 0.5694 (95% CI [0.4522, 0.6711]) and cross-song margin mean 0.5839 (95% CI [0.4899, 0.6662]), with 35 independent audio groups. This only establishes evaluator readiness, not experiment acceptance.
- Independent scientific review returned `PASS` for implementation semantics while explicitly separating runtime proof and scientific acceptance.

Failures and how to do differently:

- The first local queue treated the existing stability watcher as a GPU blocker even though it only monitored remote results. Use a shared lock for actual GPU work; do not block on status-only monitors.
- The first review/currentness check lacked a resource packet; adding the required resource review allowed the `gs_g1` review to become current.
- Do not interpret completion of GS training or validation as acceptance of any generator route.

References:

- CPU proof: `runs/gs_g1/cpu-proof/proof.json`
- GPU proof: `runs/gs_g1/gpu-proof/proof.json`
- Final checkpoint: `runs/gs_g1/formal/final.pt`
- Validation: `runs/gs_g1/formal/validation.json`
- Review: `docs/experiments/reviews/EXP-20260922-fd-history-gs-g1-review.md`
- Queue/lock: `scripts/queue_gs_g1_local.py`, `scripts/local_g1_gpu_lock.py`, `runs/local-gpu.lock`
- Focused tests: `.venv311/bin/python -m unittest tests.test_gs_g1` -> 7 tests passed

## Task 3: Score old and new experiments with GS-G1 parallel to MMR+

Outcome: success

Preference signals:

- The user requested old mainline and new experiments, then explicitly reminded “还有resampling的” -> reports should include old mainline, native, rotation-supervision, stability, and history-resampling groups, with repeated arms labeled as historical aliases rather than counted as independent experiments.
- The user wants MMR+ “parallel” -> preserve separate GS-G1 and MMR+ columns; never create a composite score or replace MMR+.

Key steps:

- Added `eval/supplement_g1_genre_matching.py` supporting native trajectory, rotation supervision, history resampling, and stability layouts.
- Evaluated the same 18 songs × 3 sampling seeds over frames 264:984, and separately reported the 13-song subset excluding the five disclosed duplicate-audio songs.
- Preserved wrong-music/null-music controls for history resampling, scoring against the original target song.
- Verified accepted MMR+ versions and feature versions across all groups, exact motion reuse for repeated historical arms, and same checkpoint/interval/population for parallel comparisons.
- Completed 4 experiment groups, 17 unique settings, 22 main comparison entries, 30 condition entries, and 1620 per-song/sample records.
- History/resampling GS results: base 0.6674/0.6442, CoF 0.6762/0.6352, continuous resampling 0.6747/0.6329, joint resampling 0.6806/0.6415 for 18/13 songs. All predeclared pairwise intervals included zero.
- Stability GS contrasts versus new-music control also included zero; no clear genre-matching improvement was established.
- Rotation supervision B vs A showed a small positive GS difference: +0.0132 on 18 songs [−0.0006, +0.0318] and +0.0194 on 13 songs [+0.0010, +0.0436], but this does not repair the previously failed extreme-rotation objective.
- Old mainline vs native CoF was +0.2260 on 18 songs but only +0.0396 on the 13-song nonduplicate subset with CI crossing zero; do not claim robust improvement from the full 18-song table alone.

Reusable knowledge:

- Main report: `runs/gs_g1/local-evaluation-20260923/REPORT.md`
- Structured results: `runs/gs_g1/local-evaluation-20260923/RESULTS.json`, `SUMMARY.csv`, `source-inventory.json`
- Per-experiment reports are under each run’s `comparison/genre-matching/` directory.
- GS-G1 measures style/genre matching only; it cannot replace conclusions about beat alignment, physical realism, amplitude, rotation, foot sliding, or video quality.
- The 13-song nonduplicate subset is essential because the 18-song main table contains five train/test duplicate-audio pairs.
- Scientific acceptance remains false/pending; the user must decide how these metric results affect claims or route selection.

References:

- `eval/supplement_g1_genre_matching.py`
- `runs/gs_g1/local-evaluation-20260923/REPORT.md`
- `runs/gs_g1/local-evaluation-20260923/RESULTS.json`
- `runs/gs_g1/local-evaluation-20260923/SUMMARY.csv`
- `runs/gs_g1/local-evaluation-20260923/source-inventory.json`
- MMR+ scorer: `eval/score_g1_causal_native_mmr_plus.py`
- History results: `runs/causal_history_resampling/cluster-readback-20260922/comparison/genre-matching/parallel-scores.json`

## Task 4: Check local 5090 timing and queue state

Outcome: success

Key steps:

- Initially found the 5090 idle but GS blocked by the monitor-only watcher condition; repaired the queue without touching running generator/stability work.
- After repair, GPU proof passed, then training completed at approximately 0.32–0.33 seconds/update; the earlier estimate of 18–20 minutes was consistent with observed runtime.
- Final scoring was moved to CPU and completed without interrupting the independent stability rendering process.

Reusable knowledge:

- Use `nvidia-smi --query-gpu=memory.used,utilization.gpu --format=csv,noheader` for instantaneous state, but distinguish actual GPU clients from monitoring processes and tiny persistent MPS daemons.
- Preserve active cluster jobs and watchers; only stop a demonstrated idle waiter or same-task duplicate.

References:

- Queue record: `runs/gs_g1/queue.json`
- Queue log: `runs/gs_g1/queue.log`
- Completed local evaluation status: `runs/gs_g1/local-evaluation-20260923/status.json`
- Live report command: `tail -f runs/gs_g1/local-evaluation-20260923/run.log`

