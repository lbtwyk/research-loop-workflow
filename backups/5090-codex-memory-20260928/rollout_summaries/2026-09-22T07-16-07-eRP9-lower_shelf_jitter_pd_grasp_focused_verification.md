thread_id: 01a0c7f8-cf32-78b1-a187-322171d391d7
updated_at: 2026-09-24T06:00:39+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T15-16-07-01a0c7f8-cf32-78b1-a187-322171d391d7.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# Lower-shelf jitter root-cause investigation and focused grasp verification

Rollout context: In `/home/wangyukun/ubt_isaac_sim_ws`, the user asked for deep root-cause analysis of lower-shelf video jitter, box tilt/drop, and weak grasp, then explicitly narrowed scope to deterministic validation: “现在不用发散性尝试，做确定性优化验证，快点得到结果” and no additional variants.

## Task 1: Diagnose and fix inference/execution mismatch

Outcome: partial

Preference signals:

- The user prioritizes “根因修复” over cosmetic smoothing -> future work should inspect action representation, reference frames, timing, and physical traces before tuning gains.
- The user requested deterministic validation and no further exploration -> freeze a selected intervention, run only predeclared matched controls, and do not expand seeds/parameters without approval.

Reusable knowledge:

- N1.7 relative arm actions are decoded against the current reference state. RTC continuation must re-encode the previous absolute chunk against the new reference, preserve the physically executed prefix, and align replanning with inference latency. Old-reference reuse caused target jumps and jitter.
- Fixed several execution/measurement issues: waist velocity clock, settled initial-height reference, box reset offset, same-tick base/arm command application, 30 Hz/60 Hz midpoint target interpolation, lower evaluation horizon (3600 physics steps/60 s), actual box-filtered contacts, contact buffer size, and physical support versus placement-quality separation.
- Regression evidence: 59 targeted checks passed in the earlier closure route; corrected inference traces had zero action gaps and no expired requests/client errors, but lower placement still failed.

Failures and how to do differently:

- Do not equate lower joint roughness or a successful replay with autonomous task recovery. The formal 8-step/frozen-8 lower evaluation achieved 7/40 actual completions (17.5%), with 39/40 pickups; the remaining failures include real drops, wrong-level returns, and inaccurate placement.
- The train/inference implementation mismatches were repaired, but closed-loop state-distribution mismatch remains unresolved: after a model-induced tilt or retreat, the model encounters states unlike the demonstrations.

References:

- `0.logs/n17_v3_jitter_fix_20260917/REPORT.md`
- `0.logs/n17_v3_control_rootfix_20260917/REPORT.md`
- `0.logs/n17_v3_execution_closure_20260917/REPORT.md`
- `syntheticdatageneration/sdg_utils/n17_v3_rtc.py`
- `syntheticdatageneration/script/vla_n17_fullbody/n17_v3_rtc_reference.py`
- `syntheticdatageneration/scenarios/training/mixins/VlaN17V3RuntimeMixin.py`

## Task 2: Test PD/physics and grasp interventions

Outcome: partial

Preference signals:

- The user explicitly asked whether optimization was PD and wanted a clear result -> distinguish retained production fixes from experimental PD/grasp interventions and report causal limits.
- The user considers holding a tilted or unreleased box a failure -> success requires target placement, release, no drop, and acceptable tilt, not merely delayed drop or lower jitter.

Reusable knowledge:

- Default PD remains unchanged: baseline arm `Kp=5729.578`, `Kd=57.29578`; lifter gains remain separately configured. Experiments increased arm `Kd` to approximately 3x while keeping `Kp` fixed.
- Full-arm 3x damping reduced fixed-command early loaded-arm roughness by about 39–40%; static hold residual roughness fell about 80.9%. However, autonomous full-arm damping achieved 0/6, and shoulder/elbow-only damping achieved 0/4, so damping was not promoted.
- Increasing wrist effort from 20 Nm to 40 Nm reduced tracking error but lost grasp; it was diagnostic only and not adopted.
- Candidate C combined privileged hand/contact/geometry feedback with 3x arm damping. On one fixed successful trajectory replay, common 2.5–15 s loaded roughness fell 49.45%, box angular-speed p95 fell 27.16%, and tilt p95 improved 8.82°→6.02°. In the 15–30 s phase, tilt worsened 4.02°→7.42°.
- Final fresh autonomous cases 502/503 remained 0/2 versus native 0/2. Case 502 held the box for 60 s but retreated roughly 7.75 m, never reached/released, and ended about 50.29° tilted. Case 503 dropped at 55.3 s after severe retreat/tilt. Thus C is not a usable autonomous repair and remains opt-in/default-off.

Failures and how to do differently:

- The delayed-latch D variant failed its fixed 501 replay at about 50.73 s and was discarded. Preserve the negative evidence; do not tune around it.
- Two startup failures came from lazy initialization (`initial_target_obj_pose`/`target_obj` being `None`); they were kept outside episode statistics. Future runs must verify settled USD box pose before runtime initialization.
- Do not claim the roughly 49% replay improvement is solely PD: C also changes privileged grasp/entry control and executed arm targets.

References:

- `0.logs/n17_v3_physics_rootcause_20260922/REPORT.md`
- `0.logs/n17_v3_grasp_repair_20260922/REPORT.md`
- `0.logs/n17_v3_grasp_repair_20260922/closure.json`
- `0.logs/n17_v3_grasp_repair_20260922/replay_comparison.json`
- `0.logs/n17_v3_grasp_repair_20260922/paired_statistics.json`
- `syntheticdatageneration/sdg_utils/n17_v3_grasp_constraint.py`
- `N17_V3_GRASP_CONSTRAINT=0` is the retained default.

## Task 3: Evidence closure and reporting

Outcome: success

Key steps:

- Completed 14 full 60-second focused trials, preserving two pre-episode initialization failures separately.
- Validated 42 original videos plus 3 comparison videos; all decoded as H.264/yuv420p with no temporary videos.
- Passed 17 focused tests, 14 intervention checks, and 6 raw-policy execution checks.
- Stopped the owned model server and simulators; unrelated Musics2Dance services were preserved.

Reusable knowledge:

- The user requires complete evidence and caveats, not only a success rate. Keep replay gains, autonomous outcomes, startup failures, and scope limitations separate.
- No model retraining, default promotion, force/mass/friction change, scoring change, or new formal 40-episode evaluation was performed.
- Final recommendation was to retain native defaults and treat damping/grasp feedback only as diagnostic evidence; any successor route requires explicit owner approval.
