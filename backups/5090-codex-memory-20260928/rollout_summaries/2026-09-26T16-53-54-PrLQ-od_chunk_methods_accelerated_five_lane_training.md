thread_id: 01a0dea3-394a-7a13-8e87-72f793d06ada
updated_at: 2026-09-26T18:17:37+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T00-53-54-01a0dea3-394a-7a13-8e87-72f793d06ada.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# OD chunk-method transfer and accelerated five-lane training

Rollout context: In `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`, the user asked to select promising FD chunk methods, add existing seam constraints, retrain them on the full OD data stack, and compare against the C64 D+C enhanced RF baseline.

## Task 1: Select chunk methods and define OD comparison

Outcome: success

Preference signals:
- The user explicitly requested “挑几个现在看起来结果比较好的chunk方法” and asked to “加上我们用到的接缝约束” while comparing OD against FD -> future runs should select candidates from completed FD evidence, preserve seam constraints, and compare domains under matched evaluation rather than optimize only one metric.
- The user specified “64的dc增强rf作为baseline” -> retain C64 D+C enhanced RF as the explicit baseline.
- The workflow preserved full OD rather than shrinking OD to the FD population, and retained extreme inputs without clipping, smoothing, or deletion -> this is an important default for similar data-domain comparisons.

Key steps:
- Inspected FD completed results and selected: current latent chunk, current latent chunk with seam/velocity constraint, motion chunk with seam/velocity constraint, latent chunk RF route, and C64 D+C enhanced RF baseline.
- Used OD complete-sequence-repair C64 codec and its full re-encoded OD cache, not the earlier failed codec/cache.
- Confirmed OD input population: 15,426 codec-training sequences, 10,923 reliable music-paired generator sequences, 671,528 source groups, all groups nonempty; 5961 groups have fewer than eight targets and are retained with real target counts.

Reusable knowledge:
- OD complete-sequence repair finished 100,000 codec updates and 144-track reconstruction evaluation: joint median 16.044→1.477 degrees, orientation 24.556→1.055 degrees, amplitude ratio 0.360→0.994, severe failures 6/144→0/144, and no million-scale loss at 5,000 logged points. This validates the repaired codec as the OD input, but does not validate OD generation quality.
- OD codec residual tail issues remain: 340/18,541 cached sequences have standardized values >20; the largest tail is associated with visible input tails and excess third-order variation. Do not claim all OD quality is repaired or start generator acceptance from codec metrics alone.
- The experiment contract is `EXP-20260927-od-chunk-transfer`; frozen route uses 90,000 updates, 48 source groups/update, seed 1234, full OD data, and separate RF continuation semantics. Scientific acceptance remains false.

References:
- `docs/experiments/EXP-20260927-od-chunk-transfer.md`
- `docs/experiments/contracts/EXP-20260927-od-chunk-transfer.json`
- `runs/od_chunk_transfer_20260927/selection-results.json`
- OD inputs: `/hot/upload/EXP-20260924-c64-fd-od-calibrated-rf/complete-sequence-repair-20260925/results/od/inputs`

## Task 2: Validate and deploy execution acceleration

Outcome: success

Key steps:
- Added exact-trajectory acceleration: expanded CUDA graph cache capacity to 64 shapes, batched physical-history transfer instead of hundreds of tiny GPU copies, and removed redundant baseline computation while preserving scientific settings.
- Added explicit execution-migration records and preserved old recovery checkpoints under `speed/cutover/<cell>/before-execution-change.pt`.
- Ran 25 focused tests successfully and contract lint returned zero errors.
- Same-checkpoint comparisons proved identical model/optimizer/source-order state after 100 updates for chunk methods and 20 updates for the D+C baseline; baseline RNG state also matched.
- Measured speedups: ordinary latent chunk 0.532→0.374 s/update (42.2% faster), latent seam-constrained 0.725→0.416 (74.5%), motion seam-constrained 0.523→0.348 (50.1%), and C64 D+C baseline TF 2.045→1.771 (15.5%).
- Replaced all five original Jobs only after archiving checkpoints and waiting for Pods to terminate. The accelerated `-fast-0927` Jobs were Running with zero restarts and had advanced beyond their cutover points.

Failures and how to do differently:
- A broad speed-probe initially failed because per-step diagnostics were not isolated under a `speed-probe` output directory. Future diagnostic runs must use the required isolated output naming.
- Initial live speed readings included CUDA graph-cache warmup and were not treated as stable throughput. Report warmup separately and use later windows for operational estimates.
- Do not extrapolate TF speedups to RF: the rollout explicitly records that RF-stage speed must be measured separately.

Reusable knowledge:
- Verified accelerated release: `dce3c9019961`; hot-storage readback was confirmed.
- Formal runtime report: `runs/od_chunk_transfer_20260927/SPEED.md`; machine-readable evidence: `runs/od_chunk_transfer_20260927/ACCELERATED.json` and `speed-final-ready/execution-proof.json`.
- At final readback, all five lanes were Running with zero restarts and progressed approximately to: latent chunk 2730, latent RF warmup 4200, latent seam-constrained 3920, motion seam-constrained 4230, and C64 D+C baseline 1080.
- The five lanes retain full OD, effective batch, source order, seed, music conditions, loss definitions, and 90,000-update budgets; acceleration changes execution only.

References:
- `runs/od_chunk_transfer_20260927/SPEED.md`
- `runs/od_chunk_transfer_20260927/ACCELERATED.json`
- `runs/od_chunk_transfer_20260927/speed-final-ready/execution-proof.json`
- `runs/od_chunk_transfer_20260927/speed-final-ready/check-final.json`
- `scripts/run_kubesphere_command.py`
- Hot-storage release: `m2d-update-dce3c9019961.pyz` (readback verified)

## Task 3: Continue OD training and downstream delivery

Outcome: partial

Reusable knowledge:
- Training had only reached early/mid updates at rollout end. RF phases, final evaluations, OD native scoring, standard videos, and scientific reporting were not complete.
- Standard 60-second, continuous-cut, 175-video, and 21-combination-video delivery workflows were prepared and waiting on formal model completion.
- Future status reports must distinguish: checkpoint archived, Job submitted, Pod Running, formal stage completed, evaluation completed, video delivered, and scientific acceptance. Do not describe the ongoing training as a quality result.
