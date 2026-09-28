thread_id: 01a0d703-eed8-7c12-b917-3b15bb36329e
updated_at: 2026-09-27T15:39:20+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T13-22-34-01a0d703-eed8-7c12-b917-3b15bb36329e.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# OD C64 codec root-cause repair and full-run verification

Rollout context: In `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`, the user explicitly requested a general root-cause solution for OD codec failures rather than a specific patch, then requested direct launch commands and later asked to check the completed run.

## Task 1: Implement general complete-sequence supervision repair

Outcome: success

Preference signals:
- The user asked for “根因修复，不要patch一个specific问题，而是做成通用的solution” -> future fixes should target the shared mechanism, preserve old failure evidence, and avoid sample-specific clipping, smoothing, or hard-coded exceptions.
- The user later said “你都要给我命令直接启动” -> when a runnable cluster task is authorized, provide or execute a complete, directly usable command rather than only describing a launch path.

Key steps:
- Root cause was traced from the failed OD run: previous changes expanded loss coverage but the sampler still omitted real starts of many 65–316-frame sequences and mature-window prefixes.
- Added shared `dataset/g1_codec_windows.py` with `CausalMotionWindows`: uniformly choose a training sequence, then a source-aligned non-overlapping target block; retain up to 252 real preceding frames; cover every complete real token; mask right padding; preserve causal boundaries.
- Integrated the protocol into the scratch codec trainer, checkpoint identity, input preparation, downstream stack checks, and old-checkpoint/input rejection. Existing FD artifacts and failed OD outputs remain historical and isolated.
- Added boundary, streaming-equivalence, RNG-resume, finite-gradient, and partial-block tests. Main suite reached 53 passing tests; all 467 observed OD sequence lengths were checked for complete coverage; full-size codec, TF/RF resume, and 160-frame downstream proof passed; independent read-only review passed.
- Published implementation and evidence to PR #56; final publication head reached `3999d1413b957507fac17801fef2653c1722b41d`.

Reusable knowledge:
- The repair route is `codec-complete-sequence-coverage-repair`, preserving seed 1234, OD 15426 training sequences, D512+C64/1024-width codec, batch/microbatch 64, and 100000 updates while changing only the sampling coverage contract.
- Formal OD generator retraining must remain gated on repaired codec quality; completion of codec training/evaluation does not imply scientific acceptance or generator readiness.

References:
- `dataset/g1_codec_windows.py`
- `tests/test_g1_codec_windows.py`
- `docs/CAUSAL_OD_C64_COMPLETE_SEQUENCE_REPAIR_RUN.md`
- `docs/experiments/reviews/EXP-20260924-c64-fd-od-calibrated-rf-complete-sequence-results-20260927.md`
- `https://github.com/lbtwyk/Musics2Dance/pull/56`

## Task 2: Check completed 100k run and audit remaining failures

Outcome: partial

Key steps:
- Used the verified KubeSphere webpage-terminal route via `scripts/run_kubesphere_command.py`, queried exact Job/Pod state, and read hot-storage artifacts back. The Job `m2d-od-c64-complete-sequence-20260925` completed successfully on node13 with exit code 0; codec training, re-encoding, and evaluation all completed.
- Verified final checkpoint/input identity, finite weights and cached latents, 15426 training tracks and 18541 cached tracks, and the complete-sequence protocol.
- Matched the same 144 held-out clips across six sources against the original and startup-only repairs. Compared with startup-only repair: median joint error 16.044°→1.477°, root orientation 24.556°→1.055°, amplitude ratio 0.360→0.994, severe clips 6/144→0/144, and million-plus logged losses 124/5000→0/5000. All 144 clips improved on the compared metrics.
- Additional tail diagnostics found 340/18541 cached clips with standardized residual magnitude above 20; five largest-tail examples had jerk intensity 1.87–3.69× reference despite only 2.95–4.49° joint error. This is diagnostic evidence, not a new acceptance threshold, and the source of the tail has not been proven.

Failures and how to do differently:
- Do not claim the codec is universally fixed or start OD generators solely from the strong 144-clip panel. Remaining input-tail and high-jerk behavior is unresolved; investigate coordinate/time continuity and component-wise reconstruction errors before selecting another route.
- The experiment spec initially contained stale “not submitted/403” text after the webpage-terminal launch succeeded; future checks should reconcile live scheduler state and hot-storage completion records before reporting status.
- Broad ledger lint still reported two pre-existing unregistered experiment documents; scoped contract lint passed with 0 errors.

References:
- Job: `m2d-od-c64-complete-sequence-20260925`; Pod: `m2d-od-c64-complete-sequence-20260925-snwps`
- Hot results: `/hot/upload/EXP-20260924-c64-fd-od-calibrated-rf/complete-sequence-repair-20260925/results/`
- Report: `docs/experiments/reviews/EXP-20260924-c64-fd-od-calibrated-rf-complete-sequence-results-20260927.md`
- PR stage comment: `https://github.com/lbtwyk/Musics2Dance/pull/56#issuecomment-5848013553`
- Verified command route: `.venv311/bin/python scripts/run_kubesphere_command.py --script <absolute-script> --output <receipt.json>`
