thread_id: 01a0aea2-2d88-7ad1-93f5-dabd2b7354da
updated_at: 2026-09-18T05:21:06+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T13-07-39-01a0aea2-2d88-7ad1-93f5-dabd2b7354da_01a0b2e9-c315-7110-a086-05d720e45b8a.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Codec route decision based on matched reconstruction diagnostics

Rollout context: In `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`, the user asked whether to continue the new token-causal D+C codec route after it underperformed the old mainline. The analysis compared checkpoints, tested convergence and streaming correctness, inspected training/objective code, and ran an oracle-latent diagnostic.

## Task 1: Decide whether to continue the token-causal codec route

Outcome: partial

Preference signals:

- The user explicitly asked for a deep analysis and a clear continue/stop recommendation, not merely more metrics -> future analyses should separate verified evidence, causal interpretation, and an actionable investment decision.
- The user’s research workflow values bounded claims and explicit exit criteria -> recommendations should avoid claiming that the architecture itself is disproven when the comparison is not budget/contract matched.

Key steps:

- Compared the old mainline checkpoint against three new 100k-step seeds on all 18 held-out FineDance tracks. Old own-history native MSE was `0.008143`; new seeds were `0.05594–0.05931`, approximately `7.05x` worse. Every new seed lost on all 18 tracks.
- Verified the comparison scope and repaired a misleading metric name: the first three motion channels are local XY steps and height, not world XYZ position; `root_position_rmse_cm` was renamed to `local_xy_step_and_height_l2_rmse_cm` and excluded from the main quality conclusion.
- Checked 50k versus 100k checkpoints. Test MSE improvements were only about `0.9%` (seed 1234), `2.8%` (2345), and `5.6%` (3456), so simply extending the same training was not supported as a solution.
- Verified causal streaming behavior: seed-1234 final full-sequence versus 8-frame incremental decoding differed by at most `4.53e-6`; local real-248-frame warmup versus full-sequence output differed by at most `2.86e-6`. Cache or chunk-boundary bugs were not the main explanation.
- Measured the new model on training data: first-512-frame average joint error was still about `7.22°`, so the gap was not merely held-out generalization.
- Ran a diagnostic optimizing only the latent input to the frozen decoder using the ground-truth motion. On four samples, reconstruction error improved by roughly `54–64%`. This is answer-assisted evidence, not deployable performance, but it indicates the decoder can represent more accurate motion than the normal encoder currently finds.
- Final recommendation: stop current-config expansion and downstream music-generator training; retain the continuous representation as a research direction and allow at most one capped reconstruction-first repair study with precommitted exit criteria. If the repaired model remains several times worse, return to the old mainline for CoF research.

Failures and how to do differently:

- The initial comparison could not support an architecture-causal claim because training budgets, windows, initialization, boundary conditioning, and anchor behavior differ. Future reports must call this a checkpoint/protocol comparison, not an architecture ablation.
- The new model’s smoother motion must not be treated as a quality improvement: joint jerk was lower, but reconstruction and foot-skate quality did not improve.
- Do not continue training merely because training loss is still decreasing; use held-out reconstruction and explicit progress from retained checkpoints.
- The oracle-latent probe uses ground truth and must remain a diagnosis only, never a quality result or deployment proposal.

Reusable knowledge:

- New codec architecture: causal Conv1D D+C, 38D `g1_yaw_anchor_abs_6d`, 16D continuous latent, 512-entry VQ, 248-frame real warmup, 64-frame target windows, batch 64, learning rate `0.0002`.
- Old mainline uses explicit B71 boundary history; new codec has no learned boundary-state input. This changes the information burden and is a plausible mechanism, but it was not isolated causally.
- The current codec is operationally stream-consistent, but operational correctness does not imply reconstruction quality or scientific acceptance.
- No new training was launched and no experiment acceptance/lifecycle decision was changed by the analysis.

References:

- `runs/token_causal_dc/mainline-comparison/comparison.json`: 18-track old/new metrics and scope limits.
- `runs/token_causal_dc/mainline-comparison/REPORT.md`: audited comparison report.
- `runs/token_causal_dc/mainline-comparison/ROUTE_DECISION.md`: detailed route recommendation and diagnostics.
- `runs/token_causal_dc/mainline-comparison/diagnosis.json`: checkpoint, warmup, train/test, and streaming diagnostics.
- `runs/token_causal_dc/mainline-comparison/latent-probe.json`: frozen-decoder oracle-latent probe.
- `eval/compare_token_causal_mainline_codec.py`: comparison evaluator.
- Verified command outcome: `wins {'new_1234': 0, 'new_2345': 0, 'new_3456': 0}`.

