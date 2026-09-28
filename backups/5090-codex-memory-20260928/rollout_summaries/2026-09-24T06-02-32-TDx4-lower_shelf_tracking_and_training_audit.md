thread_id: 01a0d202-2a1a-73a3-a994-2f1e636edbe6
updated_at: 2026-09-24T09:25:32+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T14-02-32-01a0d202-2a1a-73a3-a994-2f1e636edbe6.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# Lower-shelf inference, tracking-error, and data/training audit

Rollout context: `/home/wangyukun/ubt_isaac_sim_ws`; user explicitly rejected PD tuning as the remedy and required accurate tracking-error attribution before selecting an optimization. Referenced chat was read before relying on it.

## Task 1: Tracking-error audit and bounded controller scope

Outcome: partial

Preference signals:
- The user said: “我们不要靠调整pd来解决物理抖动的问题” -> keep original PD and investigate inference/execution/physical causes separately.
- The user chose: “允许额外接触反馈参与控制，但保持原PD” -> contact feedback may be used in a downstream controller, while original gains, force limits, model, physics, and task gates remain fixed.
- The user selected “1a，2a” -> after bilateral carrying is established, continuously monitor and make bounded grasp-preservation corrections; release remains policy-initiated, with feedback only delaying release until reliable shelf support.
- The user chose the bounded scope excluding chassis retreat and shelf-entry trajectory correction -> do not silently expand feedback control into base motion or entry planning.

Key steps:
- Read the prior lower-shelf thread and reports. Prior evidence remained 7/40 full lower completions; previous grasp/entry+damping candidate was 0/2 versus native 0/2 and was not promoted.
- Recomputed tracking from 10 existing runs in `0.logs/n17_v3_tracking_audit_20260924/`, with 16,756 matched action endpoints. Joint ordering, per-step alignment, and target continuity checks passed with zero mismatch.
- Distinguished three quantities: raw model-requested target vs pre-step measured pose; requested target vs final applied target after limit/interpolation/controller edits; previous applied target vs current measured pose (physical tracking error).
- For failed seed 502 at 2–10 s, raw right-wrist request-to-state p95 was about 25.75°, while 18.87° was removed by execution limiting. Near drop, while both hands still contacted the box, wrist errors were small: seeds 502/503/504/508 median errors were approximately 0.03–0.18°.
- A fixed-target hold showed persistent loaded-state bias, especially left wrist (~10.41° median in the 12–20 s window), but this is not proof of torque saturation.
- Updated the experiment spec with confirmed decisions and open engineering questions; no new simulation, training, PD change, or controller implementation was launched.

Failures and how to do differently:
- Do not call `previous_target-current` “model accuracy”; it measures post-limit physical response and can hide raw target clipping.
- Do not infer that small wrist error means grasp stability or sufficient actuator torque; pair error with contact, support, box attitude, and drop timing.
- Check per-episode tick resets before joining traces; global `physics_tick` offsets can otherwise create false mismatches.

Reusable knowledge:
- `N17_V3_TARGET_LIMIT_MODE=measured` uses a 0.12 rad target step limit around measured joint state; this can materially alter the raw request.
- Existing diagnostic trace records `previous_target`, current joint state, contact forces, box pose/velocity, and reaction effort. Reaction effort is a constraint/contact reaction measurement, not commanded torque or saturation.
- Canonical audit artifacts: `0.logs/n17_v3_tracking_audit_20260924/audit.json` and `REPORT.md`.

## Task 2: Data and training-integrity audit

Outcome: partial

Preference signals:
- The user requested deep root-cause investigation rather than immediately launching another optimizer/training route -> preserve negative evidence and separate verified defects from hypotheses.
- The audit maintained original PD and did not promote a controller or claim improved autonomous success.

Key steps:
- Audited 500 lower demonstrations and 771,289 decoded frames; no corrupt videos, missing frames, or non-finite values were found. 743 attempts yielded 500 included successful episodes.
- Verified uploaded archive identities/checksums and reconstructed numeric data. Stored extrema matched the combined data exactly; all 1,030 retained model tensors were finite.
- Found a concrete training-contract defect: intended top-four language-layer tuning was not forwarded by the model-loading path. The retained checkpoint has `tune_top_llm_layers: 0`; all 176 language-layer tensors remained unchanged, while 537 action-head tensors changed. A recording-loader reproduction confirmed the omission.
- Found all 500 demonstrations had a 20.39–27.45° wrist target reset at descent entry, while actual wrist motion was only about 0.00457° median. This is a command/target handoff, not demonstrated physical jitter.
- Demonstrations used tilt feedback on all 500 successful collection episodes, while the VLA input lacks direct contact/box feedback. Dataset coverage was narrow: 113 full parameter sets and roughly 1–2 mm initial box-position span; 165 successful samples had weaker grasp-quality indicators.
- Ran 1,344 offline model predictions and 288 baselines. Training-seen midpoint error was about 0.459° without RTC; predicting across the descent boundary rose to 3.158° and max single-joint error reached ~27.5°. Self-history continuation over 768 predictions showed handoff timing from 4 frames early to 5 frames late, median 1.5 frames late.

Failures and how to do differently:
- Do not claim the missing top-four-layer training explains all drops; training logs/trainer state were unavailable and no causal retraining comparison was run.
- Offline probes used training-seen demonstrations and are not generalization or autonomous-success evidence.
- Do not label command resets as physical jitter, and do not use demonstration future/oracle continuation as deployment evidence.

Reusable knowledge:
- Training flag locations: `launch_utars_v3_finetune.py:118`, model loading `gr00t/model/gr00t_n1d7/setup.py:86`, unfreeze logic `qwen3_backbone.py:109`.
- Audit report: `docs/experiments/reviews/EXP-20260902-data-training-audit-20260924.md`.
- Audit closure: `0.logs/n17_v3_data_training_audit_20260924/closure.json`; status was accessible-audit complete, integrity verdict FAIL for the intended top-four training contract, with no production-code, PD, physical-trial, or training changes.

References:
- `/home/wangyukun/ubt_isaac_sim_ws/0.logs/n17_v3_tracking_audit_20260924/REPORT.md`
- `/home/wangyukun/ubt_isaac_sim_ws/0.logs/n17_v3_data_training_audit_20260924/closure.json`
- `/home/wangyukun/ubt_isaac_sim_ws/docs/experiments/EXP-20260902-utars-groot-n17-old-upper-new-lower-37mix.md`
- Prior physical evidence: `0.logs/n17_v3_physics_rootcause_20260922/REPORT.md` and `0.logs/n17_v3_grasp_repair_20260922/REPORT.md`
