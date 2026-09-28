thread_id: 019f3b7b-6b62-7a90-ac3a-e36d61298c86
updated_at: 2026-07-12T19:23:20+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/07/07/rollout-2026-07-07T15-29-32-019f3b7b-6b62-7a90-ac3a-e36d61298c86.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws

# LingBot-VLA 2.0 UTars benchmark pipeline was made ready and preflight-validated.

Rollout context: The user was already running UTars SDG/Isaac work in `/home/wangyukun/ubt_isaac_sim_ws` and wanted a practical answer about a new handling/box scenario. This rollout pivoted into a much larger follow-on: setting up a LingBot-VLA 2.0 benchmark pipeline for UTars that can consume real teleop data plus SDG handling-box simulation data, then expose it through the existing SDG/VLA service path. The work happened mainly in the LingBot VLA workspace under `ubt_vla_ws/ubt_vla_code/lingbot-vla-v2`, with orchestration docs/scripts added under `syntheticdatageneration/script/vla_lingbot_v2/` and `script/local/README.md`.

## Task 1: LingBot-VLA 2.0 UTars data + training pipeline

Outcome: success

Preference signals:
- The user’s repeated framing was that parts sorting already worked, pick-and-place was in progress, and they wanted the next UTars Isaac task to be handled with teleop and planning. This rollout operationalized that preference into a UTars handling-box pipeline rather than a generic ML benchmark.
- The user kept steering toward “can it run” / “what is ready” style questions rather than abstract design, which suggests future similar requests should default to a concrete readiness check, not a theoretical discussion.

Key steps:
- Inspected the local UTars/Isaac workspace and identified that the handling-box shelf path was the relevant Isaac-side scenario (`HandlingMultiBoxScenarioShelf`) and that the newtask `Packing_Box` path was not the right semantic match for “搬箱子”.
- Located the LingBot-VLA 2.0 codebase and its dataset loader paths, then built a UTars benchmark pipeline around two local dataset roots:
  - real: `/home/wangyukun/ubt_isaac_sim_ws/0.logs/datasets/UTars_real_groot_n17_20260711/train`
  - simulation: `/home/wangyukun/ubt_isaac_sim_ws/0.logs/datasets/HandlingBox_groot_300_20260710/train`
- Added a weighted multi-dataset stream so the combined stream is exactly 60% real / 40% simulation, instead of the upstream concatenation behavior that would overrepresent the larger real set.
- Added a local LeRobot v2.1 compatibility path in LingBot dataset loading so local dataset directories are treated as local roots instead of online repo IDs.
- Added a smoke loader and preflight scripts that verify dataset shapes, weights, and action/state contract before any model download or training.
- Added a policy-server wrapper and eval script so the same benchmark can be served through the existing SDG HTTP interface and evaluated open-loop.
- Updated local docs to describe the new LingBot pipeline and its launch/eval flow.

Reusable knowledge:
- LingBot-VLA 2.0’s local loader needed three practical fixes for this UTars setup:
  1. local dataset directories must be passed as `root`, not as a Hugging Face repo id,
  2. some local v2.1 datasets have non-contiguous episode indices, so the loader needs the explicit episode list from `meta/episodes.jsonl`,
  3. the shared multi-dataset loader concatenates by default, so a weighted virtual stream is needed to preserve a 60/40 real/sim ratio.
- The UTars benchmark contract that passed preflight is:
  - 16 active dimensions for the first-stage UTars arm/head setup,
  - 55D canonical layout in LingBot,
  - 50-step action horizon,
  - `relative_joint_position` action target,
  - `use_future_image: false`,
  - frozen vision encoder + expert-only training for the first run.
- The exact sample counts verified in preflight were 258,561 real frames and 46,984 sim frames, producing a 430,935-sample weighted virtual stream.
- The first-stage UTars mapping should mark actions with `relative_type: joint`, otherwise LingBot’s default quaternion-relative path can mis-handle joint deltas.

Failures and how to do differently:
- An early attempt to open local datasets through LingBot failed because the code tried to treat `train` as a Hugging Face repo id. The fix was to resolve local paths to `root` and explicitly pass the local episode list.
- Another failure mode was that non-contiguous episode indices in the real dataset caused the loader to miss files unless the explicit `episodes=[...]` list was provided from `meta/episodes.jsonl`.
- The training/eval scripts originally omitted the normalization file and valid test trajectory ids; those were corrected so evaluation won’t fail later even after training succeeds.
- The eval launcher needed defaults from the first available local episode, not a hard-coded index.

References:
- [1] Weighted multi-dataset patch and local-compat loader patch were applied in `ubt_vla_ws/ubt_vla_code/lingbot-vla-v2` and mirrored into `syntheticdatageneration/script/vla_lingbot_v2/patches/weighted_multi_dataset.patch`.
- [2] Preflight command that passed: `MODE=preflight ./script/vla_lingbot_v2/run_utars_lingbot_train.sh`
- [3] Passed preflight output included: `"weights": {"real": 0.6, "simulation": 0.4}`, `"active_dimensions": 16`, `"canonical_dimensions": 55`, `"action_target": "relative_joint_position"`.
- [4] Representative smoke-loader output: `weights [0.6, 0.4]`, `physical_frames [258561, 46984]`, `virtual_frames [258561, 172374]`, `total_virtual_frames 430935`.
- [5] A direct sample read succeeded from both domains, confirming the state/action shapes and the dataset contract:
  - real sample: `state_arm [14]`, `state_head [2]`, `action_arm [50, 14]`, `action_head [50, 2]`
  - sim sample: same shapes.
- [6] The policy server wrapper is `script/vla_lingbot_v2/vla_policy_server_lingbot_v2.py`, exposed via `run_lingbot_v2_server.sh` on port `12325`.
- [7] The benchmark documentation was updated in `script/local/README.md`, and the experiment log was updated in `docs/experiments/EXP-20260712-utars-lingbot-vla2-benchmark.md` and `docs/experiments/INDEX.md`.

## Task 2: Experiment record and launch docs

Outcome: success

Preference signals:
- The user did not explicitly ask for experiment ledger updates, but the work followed a research-style workflow and the repo already had an experiments ledger. Recording the pipeline state in the local experiment docs is useful for future similar runs.

Key steps:
- Updated `docs/experiments/EXP-20260712-utars-lingbot-vla2-benchmark.md` from `spec` to `ready` after the preflight passed.
- Added a run-log entry capturing the exact preflight command, the runtime root, the sample counts, and the next action (download model files, then run a one-step GPU memory probe).
- Updated `docs/experiments/INDEX.md` to mark the experiment as ready.
- Expanded `script/local/README.md` to include LingBot setup, preflight, eval, and service launch instructions.

Reusable knowledge:
- For this repo, `docs/experiments/` is the right place to keep durable experiment state; transient command outputs should stay out of AGENTS-style docs and in the experiment log.
- The local LingBot flow now has three stable entry points:
  - `script/vla_lingbot_v2/prepare_utars_lingbot_data.sh`
  - `script/vla_lingbot_v2/run_utars_lingbot_train.sh`
  - `script/vla_lingbot_v2/run_lingbot_v2_server.sh`

References:
- `docs/experiments/EXP-20260712-utars-lingbot-vla2-benchmark.md`
- `docs/experiments/INDEX.md`
- `script/local/README.md`

