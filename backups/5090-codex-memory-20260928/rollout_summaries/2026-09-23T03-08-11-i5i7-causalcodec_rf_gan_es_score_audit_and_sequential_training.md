thread_id: 01a0cc3c-3082-7ad2-bedd-f0ad433169a7
updated_at: 2026-09-25T15:02:17+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T11-08-11-01a0cc3c-3082-7ad2-bedd-f0ad433169a7.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Reviewed GAN/ES and continued causal-codec experiments; new RF-strength run remains incomplete

Rollout context: The user asked to inspect the referenced “调研GAN与ES训练方向” thread, report all scores, and continue analysis in `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws`. The work centered on Musics2Dance CausalCodec experiments, comparing prior CoF/RF/GAN/ES evidence and launching a new RF history-strength experiment.

## Task 1: Audit prior GAN/ES/RF/CausalCodec results and report score boundaries

Outcome: partial

Preference signals:

- The user requested “汇报全部分数，然后继续实验分析,” so future reports should distinguish every metric/window/arm and explicitly separate completed scores from running or merely proposed experiments.
- The user’s workflow expects novelty to be judged alongside maturity and engineering cost; do not treat ES as preferred merely because it is novel.

Key steps:

- Read the referenced thread with `read_thread`; the initial call incorrectly used `turnLimit:20` although the tool allows at most 10, then succeeded with `turnLimit:10`.
- Reconciled the prior formal result report and artifacts rather than treating design/CPU evidence as quality results.
- Prior 6250-step causal music self-calibration scores on 18 songs × 3 sampling seeds included: old quarter music match `0.0977`, old half `0.1039`, fixed `0.1092`, dynamic `0.1060`; joint jerk `1355.35`, `1340.51`, `1197.86`, `1197.15`; >90° transitions `14`, `16`, `6`, `2`; FIDk `197.94`, `176.59`, `86.73`, `78.97`; FIDg `0.6062`, `0.8654`, `0.9334`, `0.8393`; diversity `16.49`, `15.72`, `12.93`, `13.50` respectively.
- The strongest supported mechanism result was historical feedback improving forecast-reliability estimation: after removing 5 audio-overlap songs, error fell `27.80%`, improving `12/13` songs, adjusted `p=0.000732`; this is not a dance-quality gain.
- Future-dependence intervention changed all 54 tested states when Future was disabled or replaced, so the generator did use Future; downstream quality benefit remained statistically unproven.
- Prior direct CoF/RF comparison: CoF music score `0.102731`, continuous RF `0.105489`, joint RF `0.097671`; joint RF did not dominate overall. Existing reports explicitly caution that 3 sampling seeds are not training replications and the formal 18-song cohort has prior-use/audio-overlap limitations.
- Prior GAN/ES cost evidence: local third-update timing was approximately CoF `4.46s`, GAN `74.29s`, ES `71.06s`; isolated benchmark summary listed GAN `89.13→74.29s` and ES `81.63→71.06s`. These were bounded local timings, not H100 wall-clock proof. Cluster observations showed GAN/ES around `23.17/21.72s` per update versus CoF commonly about `1.7s`; no new GAN/ES quality scores were established in this rollout.

Failures and how to do differently:

- Do not report the CPU reliability result (`27.8%`) as dance quality, and do not turn intervention sensitivity into proof of useful Future semantics.
- Do not claim the new experiment has completed: the final state had no new quality scores; only an earlier RF/CoF suite had completed.
- Preserve artifact/provenance distinctions: `training_complete`, evaluation completion, video completion, Kubernetes completion, and scientific acceptance are separate.

Reusable knowledge:

- Frozen contract for this family: `multirate1024_balanced`, seed1234, native38/30Hz, D512+C16, K64 history, deployment H4/C4, 8-frame commits, C NFE10, 183 training / 18 test songs, 48 source groups/update, 6250 updates per arm.
- Current CoF is commit-wise D+C Two-Forward and does not support the old B71/physical-boundary novelty claim.
- Teacher-free supervised history resampling/RF is the more mature next direction; ES/GAN remain substantially slower and their current long-backprop effectiveness is not established.

References:

- `docs/experiments/reviews/EXP-20260922-fd-causal-music-self-calibration-results-20260923.md`
- `docs/experiments/reviews/EXP-20260922-fd-rf-cof-full-comparison-20260923.md`
- `runs/causal_music_self_calibration/results-check-20260923/`
- `runs/rf_cof_standard_comparison/scorebook/`

## Task 2: Implement and run RF history-strength experiment

Outcome: partial

Preference signals:

- The user authorized implementation and execution without shrinking the matched budget; future similar work should preserve the frozen contract and run operational checks before expensive training.
- The user expects automatic continuation and status checks rather than repeated requests for permission when the scientific route is already approved.

Key steps:

- Added experiment `EXP-20260923-fd-rf-rollout-strength` with two arms from the same RF base6250: `rf_joint_shift1` (only continuous-history noise shift 0.6→1.0) and `rf_joint_free2` (two short autonomous deployment-style free bursts per source group).
- Added boundary diagnostic, runner, tests, and standard-video-suite integration. The 16-group/32-boundary diagnostic passed: free2 boundary p90 `0.081343` versus gate limit `0.249751`; exact two-step resume passed for both arms; proof peaks were about `13.19GB` and `13.31GB`; downstream 128-frame generation/render proof passed.
- Independent review initially found two issues: short-video seed motion reuse and a race that could start arm 2 after arm 1 failed. Both were fixed; delta review passed. Contract lint passed with 0 errors; 14 focused unit tests passed.
- Relaunched the 70-case RF/CoF standard visual suite after the seed fix. It completed `70/70`; actual frame fingerprints for short tracks 036/063/098 showed all three sampling seeds differed.
- Started persistent local 5090 pipeline PID `3135019`. Actual VRAM invalidated the initial “parallel fits” estimate: R1 used about `15,646 MiB`, other processes about `2,623 MiB`, total used `18,317/32,607 MiB`. The scheduler correctly kept R2 queued to run sequentially after R1.
- At the final check, R1 had advanced from 1331 to 1336/6250 in 30 seconds, with fresh status age about 6 seconds, update time about `11.42s`, and estimated remaining time about `15.7h`. R2 had no log/status/checkpoint yet. New evaluation, scores, and videos had not started.

Failures and how to do differently:

- A prior standard-render implementation reused seed1234 for different short-video seeds; always verify saved motion keys and compare actual rendered frame fingerprints before trusting videos.
- PyTorch proof allocation underestimated real process VRAM; use live `nvidia-smi` after formal startup, not only proof peaks, to decide concurrency.
- The rollout ended while training was still running. The next check should inspect R1 advancement, allow the persistent scheduler to start R2 only after R1 completes, then complete declared evaluation, music interventions, 70 videos, and reporting without changing the contract.
- Disk space was only about 186GB free (`95%` used); monitor before generating large downstream artifacts.

Reusable knowledge:

- Experiment record: `docs/experiments/EXP-20260923-fd-rf-rollout-strength.md`.
- Runner: `scripts/run_g1_rf_rollout_local.py --stage all`.
- Persistent log: `runs/rf_rollout_strength_local/pipeline.log`.
- R1 log/status: `runs/rf_rollout_strength_local/rf_joint_shift1/train.log` and `status.json`.
- R2 is intentionally absent until R1 completion; do not manually launch a duplicate.

References:

- Review: `docs/experiments/reviews/EXP-20260923-fd-rf-rollout-strength-prelaunch.md`
- Proof: `runs/rf_rollout_strength_local/proof/receipt.json`
- Diagnostic: `runs/rf_rollout_strength_local/diagnostic.json`
- VRAM evidence: `runs/rf_rollout_strength_local/resource-observation.json`
- Video manifest: `runs/rf_cof_standard_comparison/videos/manifest.json` (`complete`, `70`)
- Exact test command: `.venv311/bin/python -m unittest -q tests.test_g1_rf_rollout_strength tests.test_g1_history_resampling`
