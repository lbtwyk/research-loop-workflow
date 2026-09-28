thread_id: 01a0e2b7-6160-73a2-8353-70c4a0be9f28
updated_at: 2026-09-28T02:21:21+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T19-54-23-01a0e2b7-6160-73a2-8353-70c4a0be9f28.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Implemented and launched native-34D CausalCodec64 D+C/RF experiment; formal pipeline is still running

Rollout context: In `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`, the user clarified they wanted the current token-causal CausalCodec64 adapted from native 38D to the existing native 34D representation—not the already-existing legacy chunk-causal 34D experiment—and then authorized implementation and cluster training.

## Task 1: Define and implement current CausalCodec64 native34 route

Outcome: partial

Preference signals:

- The user confirmed: “当前 CausalCodec64 改为 34D，其他保持当前配置” and later “对，开始实现，并且在集群训上” -> preserve the current C64 D+C system rather than silently substituting the legacy 34D codec, and proceed through cluster execution once the route is validated.
- The user requested GPU utilization and speed without changing the experiment -> optimize execution only after exact-state proof, while preserving seed, effective batch, update counts, and scientific semantics.

Key steps:

- Read the referenced thread and distinguished `EXP-20260927-fd-c64-34d-dc-rf` from the separate `EXP-20260927-fd-legacy-dynamic-rf` route.
- Confirmed native34 is `g1_yaw_delta`: planar displacement 2D + height + yaw sine/cosine + 29 joint DOFs; it removes root roll/pitch and cannot be implemented by merely changing `motion_dim`.
- Adapted geometry, continuity, decoded supervision, causal training, evaluation conversion, launch tooling, tests, and delivery scripts for native34 while retaining C64 latent width, D+C, calibrated MRT2 music, enhanced RF, 16-frame commits, and NFE10.
- Created and registered `EXP-20260927-fd-c64-34d-dc-rf`, added its contract, prelaunch review, run record, and stage closure evidence.

Reusable knowledge:

- Native34 requires consistent handling across `dataset/motion_representation.py`, `model/g1_token_causal_objective.py`, native training, decoded supervision, streaming state, evaluation, and video generation. Do not pad 34D into native38 or reuse native38 rotation slices/losses.
- Frozen route: FineDance 183 train / 18 test songs, seed 1234, 48 source groups/update, scratch C64 codec for 100,000 updates, then generator TF3125 + enhanced joint RF9375 = 12,500 generator updates, 16 frames/0.5333 s commit, calibrated past/style/future music attention, one H100/H200.
- Native34 geometry uses cumulative yaw reconstruction from the first available pose; frame-zero pose is supervised, while derivatives require real preceding history. Padded yaw is identity and excluded from supervision.
- The historical 38D comparison uses different sampling/training conditions, so the result cannot be interpreted as a clean representation-only causal comparison.

Failures and how to do differently:

- Initial contract lint failed because `training_preflight` was missing; adding the explicit real-route preflight fixed lint (`contract-lint: 0 error(s)`).
- A cluster inspection script hit `resourcequotas is forbidden`; this did not block the user’s own Job/Pod operations. Do not infer inability to operate the cluster from that API permission error.
- Local disk reached 100% during proof artifacts; temporary proof recovery copies were removed only after exact-resume proof and independent review, releasing about 31 GB. Preserve final proof models, logs, receipts, and inputs.

References:

- Experiment: `docs/experiments/EXP-20260927-fd-c64-34d-dc-rf.md`
- Contract: `docs/experiments/contracts/EXP-20260927-fd-c64-34d-dc-rf.json`
- Run record: `runs/c64_34d_20260927/RUN_INFO.md`
- Main launcher: `scripts/run_g1_c64_34d.py`
- Native34 tests: `tests/test_g1_c64_34d.py`
- Independent review: `docs/experiments/reviews/EXP-20260927-fd-c64-34d-dc-rf-prelaunch.md`

## Task 2: Validate and launch formal cluster training

Outcome: partial

Key steps:

- Local validation passed 11 tests, codec/TF/RF exact recovery, causal generation, scoring, and full audio/video decode.
- Independent read-only reviewer `/root/native34_review` returned `PASS`.
- Hot-storage incremental release and assets were readback-verified.
- Submitted Job `m2d-c64-34d-rf-0927`; Pod `m2d-c64-34d-rf-0927-2wl24` runs on `node13` with NVIDIA H100 80GB.
- H100 target proof passed for codec batch64, generator microbatch256, RF supervision730, exact model/optimizer/source/RNG recovery, scoring, and audio/video rendering.
- Formal codec was progressing at the latest check: 63,060/100,000 updates, ~0.262 s/update median over recent points, zero restarts, finite losses, recovery checkpoint updating, and ~68.3% mean GPU utilization over the last 10 minutes (peak 90%).
- Downstream stages had not started: codec finalization/re-encoding, codec evaluation, TF3125, RF9375, numerical evaluation, standard videos, and 21 comparison grids remained pending.

Failures and how to do differently:

- Do not report the local or target proof as a quality result; it proves execution/recovery/downstream seams only.
- Keep stage labels separate: Job submitted, Pod running, codec training progress, generator training, evaluation, video delivery, and scientific acceptance.
- The persistent standard-delivery session `m2d-c64-34d-standard` was waiting for final model artifacts; video completion must be verified from manifests and decode receipts.

References:

- Job: `m2d-c64-34d-rf-0927`
- Pod: `m2d-c64-34d-rf-0927-2wl24`
- Hot root: `/hot/upload/EXP-20260927-fd-c64-34d-dc-rf`
- Latest closure: `runs/c64_34d_20260927/stage-closure-20260928.json`
- Latest detailed check: `runs/c64_34d_20260927/latest-detail.json`
- Status command: `.venv311/bin/python scripts/run_kubesphere_command.py --script runs/c64_34d_20260927/status.sh --output runs/c64_34d_20260927/latest.json`

## Task 3: Scientific conclusion

Outcome: uncertain

No quality result or scientific acceptance was available. The authorized operational route was running, but final codec, generator, evaluation, video, and owner decision stages were incomplete.
