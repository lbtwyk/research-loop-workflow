thread_id: 01a0cc47-fa15-7a80-a814-6a39aa0e97a1
updated_at: 2026-09-25T06:23:38+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T11-21-04-01a0cc47-fa15-7a80-a814-6a39aa0e97a1.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Causal codec investigation and OD codec root-cause repair audit

Rollout context: Work was performed in `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws`, mainly under `Musics2Dance/`. The user wanted to understand why the new causal codec produces more active motion but also jitter/instability, then later asked whether a general OD codec root-cause repair was correct.

## Task 1: Causal codec mechanism and iteration direction

Outcome: partial

Preference signals:

- The user asked for a mature, clean-system-compatible iteration direction rather than a quick patch, and contrasted active motion, accuracy, jitter, and robot executability. Future work should separate codec reconstruction, generator distribution, decoder geometry, and deployment safety instead of treating visual activity as proof of correctness.
- The user values first-principles reasoning and mature-method evidence, with explicit controls and bounded experiments before changing the mainline.

Key steps:

- Inspected causal codec implementation, experiment registry, prior amplitude audits, generator-root-cause reports, rotation-stability plans, and MotionStreamer references.
- Verified the causal codec uses 38D motion, D+C latent structure, two frames per token, causal convolutions, and a K64 generator history. The decoder supports repeat or polyphase upsampling.
- Compared real-action reconstruction against autonomous generation and traced failures through fixed-latent replay, Jacobians, C scaling, D controls, and codec phase controls.
- Reviewed MotionStreamer evidence: causal autoencoder reconstruction quality does not necessarily predict long-horizon generation quality; Two-Forward/generated-history training is relevant to exposure bias.

Reusable knowledge:

- Large-motion preservation is not the main proven problem. Prior 38D audits found codec reconstruction retained roughly 97.3% range and 97.2% speed relative to reference, while low amplitude was concentrated in autonomous generation. Do not infer that the causal codec principle is wrong from low-amplitude generated clips alone.
- A major instability mechanism was localized: some generated D+C trajectories decode to nearly zero or nearly collinear 6D rotation bases. Gram-Schmidt/6D conversion then amplifies small latent or decoder perturbations into large physical orientation changes. In 56 selected severe cases, FP32 replay reproduced 56/56 failures versus 0/56 matched normal controls; failed basis norm averaged about 0.087 versus about 0.998 normal. Increasing diffusion steps from 10 to 100 only reduced failures from 56 to 51, so sampler step count is not the main fix.
- The decoder also contributes a separate two-frame phase texture: shifting the codec start by one frame changed the parity of joint jerk, indicating a causal two-frame grid/up-sampling issue. This effect exists in real-action reconstruction and should not be attributed entirely to the generator.
- `model/g1_token_causal_codec.py` uses `hidden.repeat_interleave(2)` for default upsampling and a causal decoder receptive field constrained to fit K64. The polyphase option is initialized as two identity copies and was planned as a matched decoder ablation, not a proven improvement.
- A uniform C scaling or C removal is not a general solution: complete-window controls showed C=0 can remove selected failures but introduces other failures and changes amplitude/speed. The fault is a D+C trajectory/decoder-geometry interaction.
- Existing rotation/continuity losses were applied around real encodings or paired denoising paths, not comprehensively around autonomous D-selection trajectories and degenerate 6D regions. Current auxiliary generator supervision also stops gradients through hard D selection and earlier decoder history, so it cannot directly train every causal source of the failure.
- The main research direction was to prioritize generated-history training such as teacher-free history resampling/Resampling Forcing or Two-Forward-style controls, while separately testing decoder rotation stability and two-frame phase/upsampling. Do not silently launch these routes or claim they are validated without formal matched experiments.

Failures and how to do differently:

- Do not equate “more active” with “more correct”; active motion may come with unsafe root rotations or jitter.
- Do not claim arbitrary latent-noise fragility: normal and real-codec neighborhoods were largely stable; the evidence points to specific degenerate output geometry.
- Do not replace codec and generator diagnosis with extra width, more diffusion steps, C scaling, or global smoothing without matched controls.
- The initial investigation did not itself launch or validate a new formal training route, so conclusions remained recommendations rather than accepted scientific results.

References:

- `Musics2Dance/docs/experiments/reviews/EXP-20260922-fd-causal-codec-generator-root-cause.md`
- `Musics2Dance/docs/research/CAUSAL_CODEC_GENERATION_READINESS_20260921.md`
- `Musics2Dance/model/g1_token_causal_codec.py`
- `Musics2Dance/model/g1_token_causal_objective.py`
- MotionStreamer: `https://arxiv.org/abs/2503.15451`; official implementation `https://github.com/zju3dv/MotionStreamer`

## Task 2: Audit of general OD codec root-cause repair

Outcome: partial

Preference signals:

- The user explicitly required “不要patch一个specific问题，而是做成通用的solution” -> future repairs should target the shared mechanism, preserve old evidence, and avoid sample-specific clipping, smoothing, or hand-picked exclusions.
- The user wanted direct executable launch commands, but the workflow must still distinguish delivery/readiness from actual cluster submission and scientific completion.

Key steps:

- Read the referenced Codex thread before relying on it, then inspected the repair implementation, experiment contract, tests, proof artifacts, release package, and installed runtime.
- Identified the repaired mechanism as complete-sequence target coverage rather than a special-case fix for a few OD clips.
- Re-ran focused tests and added an audit report under the experiment review directory.

Reusable knowledge:

- The confirmed prior defect was a mismatch between training target coverage and full-sequence codec use: earlier training could omit true sequence starts and transition regions while inference/re-encoding still required them. A failed checkpoint showed enormous losses when the omitted prefix was included, e.g. approximately `53.77` versus `2.337e14` on one diagnostic clip.
- The repair in `dataset/g1_codec_windows.py` uses `source_aligned_complete_target_blocks_v1`: uniformly choose a training sequence, then a non-overlapping source-aligned target block; cover every complete two-frame token including startup, middle, and final partial blocks; carry up to 252 real preceding frames; preserve an empty cache at true starts; mask right padding.
- `model/g1_token_causal_objective.py` now handles frame-zero pose supervision and only computes velocity/acceleration/jerk where real history exists. Empty derivative selections are skipped rather than reduced to invalid means.
- New checkpoints record `window_protocol` and reject old incomplete-coverage checkpoints during resume, re-encoding, and OD generator input preparation. New formal outputs use an isolated directory; old failed jobs, weights, and caches remain preserved.
- Evidence was strong for implementation correctness: 15426 training sequences, six sources, 467 distinct lengths, 128176 target blocks, and 7712902 real frames were audited; 53 tests passed; 13 focused tests passed; source-aligned block/full-sequence history equivalence passed with only floating-point-scale differences; workspace, published commit `f08df96`, and installed release runtime matched across 12 runtime files.
- Real-size proof completed two updates and exact resume, with startup windows and finite losses, and downstream TF/RF/160-frame interfaces passed. This proves execution and boundary semantics, not long-run codec quality.
- Formal 100000-step retraining had not been submitted in the audited state because Kubernetes creation verification returned HTTP 403. Therefore the repair was judged correct and suitable for formal retraining, but OD quality, late-training stability, orientation accuracy, amplitude, and generator readiness remained unverified.

Failures and how to do differently:

- Do not call the repair a quality solution based on two-step proof, test passing, or successful package delivery. The prior failure appeared late in training, so formal retraining must inspect loss spikes, per-sample extremes, orientation error, amplitude, and latent scale before starting OD generator training.
- Do not reuse the old OD codec or its re-encoded generator inputs after changing the coverage protocol.
- Do not confuse a hot-storage package, a dry-run, or a launch command with a submitted/running Kubernetes Job; the audited submission was blocked by 403.

References:

- `Musics2Dance/dataset/g1_codec_windows.py`
- `Musics2Dance/tests/test_g1_codec_windows.py`
- `Musics2Dance/docs/experiments/reviews/EXP-20260924-c64-fd-od-calibrated-rf-complete-sequence-audit-20260925.md`
- `Musics2Dance/docs/experiments/reviews/EXP-20260924-c64-fd-od-calibrated-rf-complete-sequence-repair-20260925.md`
- `Musics2Dance/runs/c64_complete_sequence_repair_20260925/audit.json`
- `Musics2Dance/runs/c64_complete_sequence_repair_20260925/proof/receipt.json`
- Exact verification: `.venv311/bin/python -m unittest tests.test_g1_codec_windows tests.test_g1_c64_stack tests.test_g1_supervised_geometry` -> 13 tests passed; broader suite -> 53 tests passed.
