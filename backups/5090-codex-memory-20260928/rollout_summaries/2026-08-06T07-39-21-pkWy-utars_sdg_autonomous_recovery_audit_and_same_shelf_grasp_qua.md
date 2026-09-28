thread_id: 019fd603-3375-7193-8c3d-85803452d066
updated_at: 2026-08-13T03:15:04+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/08/06/rollout-2026-08-06T15-39-21-019fd603-3375-7193-8c3d-85803452d066.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# The thread evolved from auditing the existing recovery implementation to validating a new same-shelf grasp-quality recovery pipeline with natural randomization and video acceptance gates.

Rollout context: The user asked whether the referenced thread’s implementation was actually a real automatic correction mechanism inside auto data collection, not just reset-and-retry behavior. The workspace was `/home/wangyukun/ubt_isaac_sim_ws`. The agent audited the recovery code paths, ran focused tests, inspected recorded natural-recovery attempts and intervention videos, and then iterated on the same-shelf grasp-quality recovery experiment until it had a state-based correction path and an acceptance record.

## Task 1: Audit whether the existing recovery thread was a real correction mechanism

Outcome: success

Preference signals:
- The user asked: `你看一下这个thread的实现，是不是有问题，我想实现的是自动数采里面的算法自动纠错机制` -> future audits should answer directly whether the implementation truly corrects within the same task flow, not merely whether it retries after failure.
- The user’s earlier recovery-data preferences from the memory file remained relevant: they want in-task recovery / planner re-entry, not whole-scene reset on failure, and they want corrected failures preserved as useful training data.

Key steps:
- Read the referenced recovery thread and confirmed the implementation does not simply discard-and-restart: it keeps the simulator state, discards the failed buffer, and starts a new recovery episode from the stabilized failure state.
- Inspected `HandlingMultiBoxScenarioShelfAutoCollect.py` and `sdg_utils/recovery/recovery_supervisor.py`.
- Verified the recovery logic is rule-driven and bounded: it classifies failures by stage/reason, uses safety thresholds, and can replan/regrasp from the observed physical state.
- Verified the natural execution correction path explicitly zeroes the sampled command bias after accepted recovery, so the retry is not a self-estimated correction model.

Failures and how to do differently:
- The implementation should not be described as a general autonomous “self-correcting algorithm.” It is a state-aware bounded recovery controller with hand-authored failure classes and safety limits.
- Some reasons that look generic can still be classified as recoverable, so future audits should inspect the observation fields and not rely on the final exception string alone.

Reusable knowledge:
- The recovery supervisor already encodes the practical difference between recoverable and unrecoverable failures using stage, contact, support, tilt, force, and speed thresholds.
- The accepted recovery flow is: detect failure -> stabilize -> replan -> execute -> verify -> continue the original task graph.

References:
- `syntheticdatageneration/scenarios/training/HandlingMultiBoxScenarioShelfAutoCollect.py`
- `syntheticdatageneration/sdg_utils/recovery/recovery_supervisor.py`
- `natural_execution_correction` zeroing `command_bias_m` after accepted recovery
- The audited conclusion in the thread: bounded recovery exists, but it is not a general self-estimating correction algorithm.

## Task 2: Validate and stress the natural-recovery / intervention-video pipeline

Outcome: partial

Preference signals:
- The user wanted the system to produce actual correction evidence, not just code or rejected attempts.
- The user implicitly cares about “what should count as proof”; repeated failed or unsafe recordings should not be relabeled as success.

Key steps:
- Inspected the accepted natural-recovery video metadata for the successful `r87` case.
- Verified the intervention video metadata contains explicit markers: failure detected, recovery started, replan generated, recovery execution, retreat/regrasp events, recovery verified, and task success.
- Confirmed the video artifact was H.264, dual-camera (`head_stereo_left_vla` and `camera_04`), and stored with actual pre/post context windows capped at five seconds.
- Ran multiple new natural-recovery recordings (`r13` to `r16`) to try to produce a fresh representative video.
- Observed that some recordings were rejected for the right reasons: one had a tilt above the 12-degree safety envelope, another triggered force rejection, and another failed later during placement with a shelf contact.
- One attempt showed the controller did correct the grasp, but the later place stage still hit collision/quality issues, so that run was not acceptable as an end-to-end deliverable.

Failures and how to do differently:
- Do not deliver recordings that only partially demonstrate correction if the end-to-end task gate fails.
- Do not let the video recording itself change the physical trajectory and then claim the resulting failure as representative success.
- When the natural sample drifts outside the safety envelope, treat it as a rejection rather than stretching the correction logic to fit it.

Reusable knowledge:
- The accepted video format for these interventions is H.264 MP4 with dual cameras and explicit timeline markers.
- The metadata format records actual `pre_roll_actual_seconds` and `post_roll_actual_seconds`, so future readers should inspect those instead of assuming both sides are always a full five seconds.
- The successful recovery case already exists in `syntheticdatageneration/logs/autonomous_replanning_recovery_20260810/.../combined.mp4`.

References:
- Successful accepted intervention video: `syntheticdatageneration/logs/autonomous_replanning_recovery_20260810/r131_first_correction_only_recording/20260810_035248/interventions/attempt-000/recovery-01/combined.mp4`
- Video metadata: `.../metadata.json`
- New natural recordings attempted under `syntheticdatageneration/logs/same_shelf_grasp_quality_recovery_20260813/`
- Example rejected reasons seen in the new runs: `pick_grasp_tilted`, `contact_force_exceeded`, `lower_box_shelf_collision`

## Task 3: Implement and verify the same-shelf grasp-quality recovery acceptance path

Outcome: success

Preference signals:
- The user accepted the direction of using a narrow, state-based correction path and wanted high-quality correction data rather than a generic retry hack.
- The thread showed a consistent preference for conservative safety gating: reject dangerous states instead of forcing them into recovery.

Key steps:
- Tightened the same-shelf grasp-quality recovery policy around observed state.
- Added/validated a fast leveling correction for moderate grasp tilt.
- Added a stronger single-hand / missing-hand completion route that restores the second hand with a short 15 mm correction and requires six consecutive stable bimanual frames before continuing.
- Added/validated natural randomization and acceptance bookkeeping for a 10-attempt run.
- Updated the experiment record and index entries for the new same-shelf grasp-quality recovery experiment.
- Ran focused tests; 58 checks passed.

Failures and how to do differently:
- Some natural samples were too risky and were correctly rejected; one had tilt above the recovery envelope and another triggered force or shelf-contact rejection.
- The strengthened single-hand route was improved in design, but the later replay did not naturally re-trigger in an independent run, so it should not be claimed as independently acceptance-validated yet.

Reusable knowledge:
- The validated state-based correction can handle moderate tilt quickly: the report states a grasp was corrected from about 10.6° to about 7.7° in 0.75 s.
- The 10-attempt acceptance report found 4 eligible recoveries, 3 final task successes, and one unsafe tilt rejection; the accepted recoveries did not produce drops or shelf collisions.
- The new acceptance artifact was written to `docs/experiments/artifacts/same_shelf_grasp_quality_recovery_acceptance_20260813.json`.
- The experiment index was updated to mark the same-shelf grasp-quality recovery experiment as `completed-with-boundary` with “3/4 eligible recoveries finished.”

References:
- `docs/experiments/EXP-20260813-utars-sdg-same-shelf-grasp-quality-recovery.md`
- `docs/experiments/EXP-20260813-utars-sdg-same-shelf-grasp-quality-recovery.md` index entry
- `docs/experiments/artifacts/same_shelf_grasp_quality_recovery_acceptance_20260813.json`
- Final validation evidence: `58 passed in 0.11s`
- Existing confirmed full-success intervention video at `.../autonomous_replanning_recovery_20260810/.../combined.mp4`

## Task 4: Keep the conclusion honest about the mechanism

Outcome: success

Preference signals:
- The user’s wording about `自动纠错机制` makes it important not to overstate a rule-based bounded controller as a general autonomous correction policy.

Key steps:
- The final conclusion was aligned to the evidence: there is a real in-task recovery mechanism, but it is bounded, state-driven, and safety-gated.
- The rollout explicitly distinguished between successful bounded recovery cases and rejected recordings that must not be mislabeled as successes.

Failures and how to do differently:
- Avoid claiming “general algorithmic self-correction” when the implementation still hard-codes state thresholds, failure classes, and some correction actions.
- Do not use a rejected or partial recording as proof of success, even if intermediate sub-steps looked good.

Reusable knowledge:
- Best default phrasing for this codebase: “state-aware bounded recovery / replanning inside the same task flow,” not “general autonomous correction.”
- For future audits, the key questions are: what state is remeasured, what state is preserved, what is replanned, and what is merely logged or cleared.

References:
- `recovery_supervisor.py` classification and safety gates
- `natural_execution_correction` behavior in `HandlingMultiBoxScenarioShelfAutoCollect.py`
- The successful accepted video and the later acceptance report as proof of the boundary between real recovery and rejected samples.
