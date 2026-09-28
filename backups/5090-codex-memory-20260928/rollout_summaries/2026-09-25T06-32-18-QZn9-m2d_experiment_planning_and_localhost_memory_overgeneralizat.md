thread_id: 01a0d743-c8ca-76c2-b455-07047969f47f
updated_at: 2026-09-27T15:23:31+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T14-32-18-01a0d743-c8ca-76c2-b455-07047969f47f.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Planned two representation experiments and corrected an overgeneralized delivery behavior

Rollout context: In `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`, the user requested implementing the first two experiments from scratch where needed, with one fully utilized H100 per training job. The rollout also covered completion of a video suite and the user's correction of unsolicited localhost URL delivery.

## Task 1: Define the first two experiments

Outcome: partial

Preference signals:
- The user asked: “那先实现前两个实验，要从头开始的就从头开始，我在集群训练，各自一h100拉满速度” -> prioritize the first two experiments, train scratch components from scratch where required, and plan for one maximally utilized H100 per experiment.
- The assistant converged on: fixed existing C64 codec with full continuous latent generation, plus a scratch causal VAE and matched scratch D+C codec control -> future planning should preserve fair controls and avoid mixing data-repair effects with representation effects.

Key steps:
- Loaded the repository research workflow and experiment-ledger requirements.
- Inspected `docs/research/CAUSAL_CODEC_DUAL_LATENT_VAE_MOTION_SPACE_REVIEW_20260925.md`, existing contracts, codec/generator trainers, and cluster guidance.
- Established the intended comparison: same frozen codec for full-continuous-vs-D+C generation; causal VAE trained from scratch with a matched from-scratch D+C control using the same repaired sampling protocol.
- Verified the project distinguishes implementation readiness, preflight, scheduler state, runtime completion, and scientific acceptance.

Failures and how to do differently:
- No formal experiment launch or training proof occurred in this rollout. Do not claim the experiments were implemented, submitted, or running based only on inspected code and plans.
- One exploratory command omitted `workdir` and produced “No such file or directory”; rerunning from the `Musics2Dance` checkout succeeded.

Reusable knowledge:
- Canonical experiment state is maintained through `scripts/experiment_ledger.py`; use `outline`, contract validation, exact preflight, launch packet, and ledger updates rather than hand-editing generated views.
- Relevant planned artifacts include `train_g1_c64_stack.py`, `train_g1_codec_latent_capacity.py`, `dataset/g1_c64_stack.py`, `configs/experiments/c64_fd_od_calibrated_rf.json`, and the causal VAE/codec research review.

References:
- `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/docs/research/CAUSAL_CODEC_DUAL_LATENT_VAE_MOTION_SPACE_REVIEW_20260925.md`
- `.venv311/bin/python scripts/experiment_ledger.py outline EXP-20260924-c64-fd-od-calibrated-rf`
- User wording: “各自一h100拉满速度”

## Task 2: Complete and deliver representation videos

Outcome: success

Key steps:
- Completed 35 standard scenarios and 21 one-minute comparison-grid videos, 56 videos total.
- Verified full decoded frame counts and audio presence; local HTTP checks returned 200 during the then-used browser delivery workflow.
- Final completion manifest reported `status=complete`, `standard_cases=35`, `grid60_cases=21`, `final_videos=56`, and `audio_video_full_decode=true`.

Reusable knowledge:
- Final local artifact directories were under `runs/representation_standard_suite_20260927/public/videos` and `runs/representation_standard_suite_20260927/videos/grid60/public/videos`.
- The suite includes a local HTML catalog and manifests; video generation itself did not require an HTTP server.

## Task 3: Trace and correct unsolicited localhost URL behavior

Outcome: success

Preference signals:
- The user first said: “为什么都会给出一个网址？把这个修复掉” and then clarified: “不是，你要找出为什么会给出网址，然后改掉这个，而不是加一条规则” -> investigate the actual source of behavior and fix the overgeneralized memory/source, rather than adding a new blanket project rule.

Key steps:
- Traced the behavior to a prior pelican SVG animation rollout where a local HTML file failed to open and a localhost server was a successful workaround.
- Found that this one-off workaround had been incorrectly generalized in memory into a default such as “use localhost over file://”.
- Removed the three newly added workspace/video-delivery rules.
- Added the supported memory correction note: `/home/wangyukun/.codex/memories/extensions/ad_hoc/notes/20260927-localhost-overgeneralization-correction.md`.
- Verified the added rules were removed and the correction note existed.

Failures and how to do differently:
- The first attempted fix merely added rules to suppress localhost URLs; the user rejected that because it did not address the cause. Future agents should trace the provenance of an unwanted behavior before adding policy text.
- Do not generalize a scoped workaround from one HTML-opening incident to all local artifacts or experiment videos.

Reusable knowledge:
- The relevant memory source was the local HTML/SVG visualization entry and its rollout summary, especially the pelican animation incident. Its evidence supports only that one incident required a localhost workaround, not a global delivery preference.

References:
- Correction note: `/home/wangyukun/.codex/memories/extensions/ad_hoc/notes/20260927-localhost-overgeneralization-correction.md`
- Source rollout summary: `/home/wangyukun/.codex/memories/rollout_summaries/2026-09-25T05-21-47-O7JY-create_pelican_bicycle_svg_animation.md`
- User correction: “要找出为什么会给出网址，然后改掉这个，而不是加一条规则”
