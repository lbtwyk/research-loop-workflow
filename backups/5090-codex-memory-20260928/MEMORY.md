# Task Group: Musics2Dance current CausalCodec64 native34 D+C/RF cluster training
scope: Adapt the current token-causal C64 route to native34 without substituting legacy34, then distinguish validated execution seams and live codec progress from downstream quality or acceptance.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=the native34 representation contract is reusable within this checkout, but Job/Pod, checkpoint progress, GPU telemetry, artifact paths, and acceptance are time-specific and require live recheck.

## Task 1: Implement current CausalCodec64 native34 route, partial

### rollout_summary_files

- rollout_summaries/2026-09-27T11-54-23-vH8A-native34_c64_dc_rf_cluster_training.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T19-54-23-01a0e2b7-6160-73a2-8353-70c4a0be9f28.jsonl, updated_at=2026-09-28T02:21:21+00:00, thread_id=01a0e2b7-6160-73a2-8353-70c4a0be9f28, route/contract/preflight implemented; final pipeline pending)

### keywords

- EXP-20260927-fd-c64-34d-dc-rf, CausalCodec64, native34, g1_yaw_delta, native38, legacy-dynamic-rf, D+C, MRT2, enhanced-RF, 16-frame-commit, NFE10, training_preflight

## Task 2: Validate and launch formal cluster training, partial

### rollout_summary_files

- rollout_summaries/2026-09-27T11-54-23-vH8A-native34_c64_dc_rf_cluster_training.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T19-54-23-01a0e2b7-6160-73a2-8353-70c4a0be9f28.jsonl, updated_at=2026-09-28T02:21:21+00:00, thread_id=01a0e2b7-6160-73a2-8353-70c4a0be9f28, H100 proof and formal codec run verified; generator/evaluation/video stages pending)

### keywords

- m2d-c64-34d-rf-0927, m2d-c64-34d-rf-0927-2wl24, node13, H100 80GB, 63060/100000, exact-resume, recovery checkpoint, RF supervision730, m2d-c64-34d-standard, stage-closure-20260928.json

## User preferences

- when selecting the representation, the user confirmed “当前 CausalCodec64 改为 34D，其他保持当前配置” -> adapt the current token-causal C64 D+C route; do not silently substitute the existing legacy chunk-causal 34D experiment. [Task 1]
- when the user said “对，开始实现，并且在集群训上” -> after route validation, carry the approved route through cluster launch while keeping submitted, running, evaluated, and accepted states distinct. [Task 1] [Task 2]
- when requesting speed/GPU utilization, preserve seed, effective batch, update counts, and scientific semantics; optimize only after exact-state proof. [Task 1]

## Reusable knowledge

- Native34 `g1_yaw_delta` is local planar translation 2D, height 1D, yaw sin/cos 2D, and 29 joint DOFs; it removes root roll/pitch. Update `dataset/motion_representation.py`, objective/decoded supervision, streaming state, evaluation conversion, and video generation together. Do not merely set `motion_dim=34`, pad into native38, or retain native38 rotation slices/losses. [Task 1]
- The frozen contract is FineDance 183 train/18 test, seed1234, 48 source groups/update, scratch C64 codec 100000 updates, then TF3125 plus enhanced joint RF9375 = 12500 generator updates, 16-frame/0.5333-second commits, calibrated past/style/future music attention, and NFE10. Native34 reconstructs cumulative yaw from the first available pose; frame zero is supervised, derivatives require preceding history, and padded yaw is identity/excluded from supervision. [Task 1]
- Local validation passed 11 tests, exact codec/TF/RF model-optimizer-source-RNG recovery, causal generation, scoring, and full audio/video decode; an independent reviewer returned `PASS`. H100 target proof passed codec batch64, generator microbatch256, and RF supervision730. These are execution/recovery seam proofs, not quality results. [Task 2]
- At the recorded check, Job `m2d-c64-34d-rf-0927` / Pod `m2d-c64-34d-rf-0927-2wl24` was on node13 H100 80GB, codec was 63060/100000 with finite losses, zero restarts, recovery checkpoint updates, and ~68.3% mean last-10-minute utilization. Final codec/re-encoding/evaluation, TF, RF, numerical evaluation, standard videos, 21 grids, and owner acceptance remained pending. [Task 2]

## Failures and how to do differently

- `contract-lint` initially failed because `training_preflight` was absent; add the explicit real-route preflight before launch and require `contract-lint: 0 error(s)`. [Task 1]
- `resourcequotas is forbidden` during one inspection does not prove the user cannot operate the Job/Pod through their KubeSphere terminal. Query the exact Job/Pod and hot-storage artifacts; do not resubmit an existing Job. [Task 2]
- A historical native38 run has different sampling/training semantics, so it cannot establish a pure representation-only causal effect. Local disk reached 100% during proof artifacts; delete temporary recovery copies only after exact-resume proof and independent review, preserving final models, logs, receipts, and inputs. [Task 1] [Task 2]

# Task Group: Musics2Dance OD chunk transfer and exact-trajectory acceleration
scope: Run the full-OD chunk-method comparison against the C64 D+C enhanced-RF baseline, and optimize execution only after exact-state proof; do not mistake early operational progress for a quality result.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=the experiment contract, release, checkpoints, throughput, and Job states are time-specific; reuse the proof and reporting boundaries only after rechecking the live contract and cluster state.

## Task 1: Select FD chunk methods and define the full-OD comparison, completed

### rollout_summary_files

- rollout_summaries/2026-09-26T16-53-54-PrLQ-od_chunk_methods_accelerated_five_lane_training.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T00-53-54-01a0dea3-394a-7a13-8e87-72f793d06ada.jsonl, updated_at=2026-09-26T18:17:37+00:00, thread_id=01a0dea3-394a-7a13-8e87-72f793d06ada, comparison selection/contract complete; quality evidence pending)

### keywords

- EXP-20260927-od-chunk-transfer, OD, C64, D+C, enhanced-RF, chunk, seam-constraint, complete-sequence-repair, 671528 source groups, 90000-updates

## Task 2: Prove execution-only acceleration and migrate five H100 lanes, completed

### rollout_summary_files

- rollout_summaries/2026-09-26T16-53-54-PrLQ-od_chunk_methods_accelerated_five_lane_training.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T00-53-54-01a0dea3-394a-7a13-8e87-72f793d06ada.jsonl, updated_at=2026-09-26T18:17:37+00:00, thread_id=01a0dea3-394a-7a13-8e87-72f793d06ada, exact-state proof, cutover, and hot-storage readback complete)

### keywords

- CUDA-graphs, speed-probe, exact-resume, model optimizer source-order RNG, ogi-llm, -fast-0927, dce3c9019961, ACCELERATED.json, execution-proof.json

## Task 3: Continue RF, evaluation, and video delivery, partial

### rollout_summary_files

- rollout_summaries/2026-09-26T16-53-54-PrLQ-od_chunk_methods_accelerated_five_lane_training.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T00-53-54-01a0dea3-394a-7a13-8e87-72f793d06ada.jsonl, updated_at=2026-09-26T18:17:37+00:00, thread_id=01a0dea3-394a-7a13-8e87-72f793d06ada, formal training running; RF/evaluation/videos/report pending)

### keywords

- latent RF warmup, native OD scoring, 175 videos, 21 combinations, checkpoint archived, Pod Running, scientific acceptance

## User preferences

- when selecting an OD comparison, the user asked “挑几个现在看起来结果比较好的chunk方法” and “加上我们用到的接缝约束” -> choose from completed FD evidence, retain seam/velocity constraints, and compare domains under matched evaluation. [Task 1]
- when the user specified “64的dc增强rf作为baseline” -> retain C64 D+C enhanced RF as the explicit matched baseline. [Task 1]
- when accelerating an active route, the user accepted continuation only after exact-state comparisons -> archive recovery state, prove the same trajectory, then replace the Job; report TF and RF throughput separately. [Task 2]

## Reusable knowledge

- The frozen `EXP-20260927-od-chunk-transfer` route uses the repaired C64 OD codec, full re-encoded OD cache, 90,000 updates, 48 source groups/update, seed 1234, and separate RF continuation. It retains all 671,528 nonempty source groups, including 5,961 with fewer than eight real targets; do not clip, smooth, delete, pad, or silently shrink OD to FD scale. [Task 1]
- The repaired codec completed 100,000 updates and 144-track reconstruction: joint median `16.044→1.477°`, orientation `24.556→1.055°`, amplitude `0.360→0.994`, severe failures `6/144→0/144`. This validates the generator input codec only, not OD generator or long-dance quality. Residual tails persist in 340/18,541 cached sequences with standardized value >20. [Task 1]
- Execution-only changes were 64 CUDA-graph cache entries, batched physical-history transfer, and removal of redundant baseline computation. Same-checkpoint windows preserved model, optimizer, source order, and baseline RNG state: ordinary latent chunk `0.532→0.374 s/update`, latent seam `0.725→0.416`, motion seam `0.523→0.348`, C64 D+C TF `2.045→1.771`. [Task 2]
- Before cutover, preserve `speed/cutover/<cell>/before-execution-change.pt`; release `dce3c9019961` was hot-storage readback-verified, contract lint had 0 errors, and 25 focused tests passed. [Task 2]
- Keep state labels separate: checkpoint archived, Job submitted, Pod Running, formal stage completed, evaluation completed, video delivered, and scientific acceptance. At handoff the five lanes were only early/mid training; RF, native OD scoring, standard videos, and the scientific report were not complete. [Task 3]

## Failures and how to do differently

- Do not treat finite reconstruction or improved codec medians as proof that OD inputs are fully healthy, nor infer generator/long-dance quality from codec reconstruction. [Task 1]
- Diagnostic logging outside an isolated `speed-probe` output was rejected. First post-migration readings include CUDA graph-cache warmup; use stable later windows, and never claim RF speedup from TF measurements. [Task 2]
- Prepared 175 standard videos and 21 continuous-cut/60-second combinations are not deliverables until actual artifacts and readback verification exist. [Task 3]

# Task Group: Musics2Dance representation experiment planning and delivery-behavior correction
scope: Plan the first C64 full-continuous and scratch causal-VAE comparisons under ledger/contract control, and correct unwanted artifact-delivery behavior at its source rather than by adding blanket rules.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=use the planning and provenance-correction method broadly, but recheck the live ledger, contracts, workdir, and artifact state before treating a plan as a launch or result.

## Task 1: Plan first two representation experiments, partial

### rollout_summary_files

- rollout_summaries/2026-09-25T06-32-18-QZn9-m2d_experiment_planning_and_localhost_memory_overgeneralizat.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T14-32-18-01a0d743-c8ca-76c2-b455-07047969f47f.jsonl, updated_at=2026-09-27T15:23:31+00:00, thread_id=01a0d743-c8ca-76c2-b455-07047969f47f, planning/ledger inspection only; no formal launch or training proof)

### keywords

- full-continuous latent, causal-VAE, matched scratch D+C control, C64, H100, experiment_ledger.py, training_preflight, launch packet, CAUSAL_CODEC_DUAL_LATENT_VAE_MOTION_SPACE_REVIEW_20260925.md, workdir

## Task 2: Correct unsolicited localhost URL behavior, success

### rollout_summary_files

- rollout_summaries/2026-09-25T06-32-18-QZn9-m2d_experiment_planning_and_localhost_memory_overgeneralizat.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T14-32-18-01a0d743-c8ca-76c2-b455-07047969f47f.jsonl, updated_at=2026-09-27T15:23:31+00:00, thread_id=01a0d743-c8ca-76c2-b455-07047969f47f, scoped pelican workaround traced and generalized rules removed)

### keywords

- localhost, file://, overgeneralization, pelican, HTML, SVG, representation-videos, video-delivery, 20260927-localhost-overgeneralization-correction.md

## User preferences

- when requesting the first two experiments, the user said “那先实现前两个实验，要从头开始的就从头开始，我在集群训练，各自一h100拉满速度” -> prioritize those routes, initialize scratch components from scratch, and plan one maximally utilized H100 per experiment without changing the scientific contract. [Task 1]
- when the user corrected “不是，你要找出为什么会给出网址，然后改掉这个，而不是加一条规则” -> trace the provenance of unwanted behavior and correct its originating memory/source, rather than layering on a blanket rule. [Task 2]

## Reusable knowledge

- Intended fair comparison: reuse frozen C64 for full-continuous-vs-D+C generation; train causal VAE from scratch with a matched scratch D+C control using the same repaired data protocol. Drive lifecycle with `scripts/experiment_ledger.py` outlines, contract validation, exact preflight, launch packet, and ledger updates—not hand-edited generated views. [Task 1]
- Source inspection/planning establishes readiness only. The rollout did not verify implementation, submission, or training; an exploratory command also failed with `No such file or directory` until rerun from the `Musics2Dance` checkout. [Task 1]
- The pelican local-HTML incident supports only a workaround after that reported opening failure. It does not justify default localhost URLs for experiment video directories; the three generalized workspace/video-delivery rules were removed. [Task 2] [ad-hoc note]

## Failures and how to do differently

- Do not claim implementation, submission, or training completion from code inspection and planning; check the real workdir and then require preflight/launch/runtime evidence. [Task 1]
- Do not promote a scoped workaround into a global user preference. For unexpected delivery behavior, trace the source and remove the unsupported generalization; experiment renderers/catalogs write local artifacts and do not require an HTTP server. [Task 2] [ad-hoc note]

# Task Group: Musics2Dance CausalCodec artifact publication and ModelScope delivery
scope: Publish accepted CausalCodec code/evidence and final artifacts while keeping GitHub free of large runtime products and exposing incomplete background transfers honestly.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws; reuse_rule=PR, branch, artifact paths, and remote listing are time-specific; recheck current checkout, remote state, and user publication scope before any transfer.

## Task 1: Publish accepted CausalCodec code and evidence, completed

### rollout_summary_files

- rollout_summaries/2026-09-24T08-35-45-99Br-causalcodec_artifact_publication_github_modelscope_hf.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T16-35-45-01a0d28e-6fc3-7a12-a067-46412d0c361d.jsonl, updated_at=2026-09-26T16:54:14+00:00, thread_id=01a0d28e-6fc3-7a12-a067-46412d0c361d, scoped GitHub publication and accepted C64 codec evidence)

### keywords

- CausalCodec, C64, C16, GitHub, PR #56, codex/codec-latent-results-20260924, 889b2af, 22907f3, py_compile, git diff --check, HuggingFace, ConnectionError

## Task 2: Archive OD cache and eligible final artifacts to ModelScope, partial

### rollout_summary_files

- rollout_summaries/2026-09-24T08-35-45-99Br-causalcodec_artifact_publication_github_modelscope_hf.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T16-35-45-01a0d28e-6fc3-7a12-a067-46412d0c361d.jsonl, updated_at=2026-09-26T16:54:14+00:00, thread_id=01a0d28e-6fc3-7a12-a067-46412d0c361d, OD cache upload background/partial; final-model-only scope enforced)

### keywords

- ModelScope, lbtwyk/musics2dance-foredance-repro, causalcodec-20260924/od-music-cache, ms-cache-complete.json, 24 shards, 6610 tracks, 9/24, resume_od_cache.sh, final-model-only

## Task 3: Decide whether to upload to Hugging Face, completed

### rollout_summary_files

- rollout_summaries/2026-09-24T08-35-45-99Br-causalcodec_artifact_publication_github_modelscope_hf.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T16-35-45-01a0d28e-6fc3-7a12-a067-46412d0c361d.jsonl, updated_at=2026-09-26T16:54:14+00:00, thread_id=01a0d28e-6fc3-7a12-a067-46412d0c361d, direct no-proxy HF check failed; upload intentionally skipped)

### keywords

- Hugging Face, huggingface.co/api/whoami-v2, HTTP_PROXY, HTTPS_PROXY, ALL_PROXY, ConnectionError, max retries, no-proxy

## User preferences

- when the user said “gh不包含大产物” -> keep GitHub to code, configs, reports, and concise evidence; exclude checkpoints, videos, audio, and caches. [Task 1]
- when the user said “只上传最终模型，不要中间产物了” -> publish final models only; cancel/exclude FD TF base and OD recovery checkpoints, then verify remote absence. [Task 1][Task 2]
- when the user said “后台上传” -> detach long transfers and provide resumable remote verification rather than blocking the interactive task. [Task 2]
- when the user clarified “我指的是hf” and “如果fd要用代理，就算了” -> make one direct no-proxy connectivity check and skip HF if it fails; do not configure a proxy merely to force transfer. [Task 3]

## Reusable knowledge

- Accepted mainline is the FineDance pure-convolution C64 codec, codec-only evidence: C64 development-test joint MAE `1.2211°` versus C16 `8.3226°`; do not promote this to generator or robot claims. PR #56 is mergeable and contains no large artifact extensions. [Task 1]
- Large runtime artifacts belong in private ModelScope dataset `lbtwyk/musics2dance-foredance-repro`. The OD cache completion criterion is all 24 remote shard archives with matching sizes plus `runs/causalcodec_publish_20260924/ms-cache-complete.json`; 9/24 was the only remotely verified state at handoff. [Task 2]
- With proxy variables unset, both `https://huggingface.co/api/whoami-v2` and `https://huggingface.co` failed with `ConnectionError`/max retries; local authentication did not overcome the network blocker, so HF upload was intentionally skipped. [Task 3]
- Related skill: `/home/wangyukun/.codex/skills/kubesphere-operations/SKILL.md` for hot-storage transfers and live cluster readback. [Task 2]

## Failures and how to do differently

- A publication-worktree test environment lacked both a usable pytest/PyTorch combination; `py_compile` and `git diff --check` passed, but do not claim full pytest coverage. [Task 1]
- Do not call a local-complete or background-running cache transfer remotely published. Stop intermediate uploads immediately after a final-model-only scope correction and verify their remote absence. [Task 2]
- Do not use a proxy to turn an explicitly no-proxy HF decision into an upload; report the direct connectivity failure and skipped state. [Task 3]

# Task Group: Musics2Dance KubeSphere hot-storage and webpage-terminal operations
scope: Automate 5090 hot-storage transfers and `ogi-llm` Job operations through the verified KubeSphere webpage terminal, including safe state readback after unreliable calls.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=use the current project tool/skill and recheck identity, permissions, namespace, and exact targets before side-effecting commands.

## Task 1: Automate KubeSphere Job inspection, creation, and deletion, completed

### rollout_summary_files

- rollout_summaries/2026-09-25T07-36-16-6zJx-kubesphere_hot_storage_command_automation_skill.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T15-36-16-01a0d77e-593f-72a0-868a-e49f7c470b33.jsonl, updated_at=2026-09-26T17:19:22+00:00, thread_id=01a0d77e-593f-72a0-868a-e49f7c470b33, create/query/delete proof through webpage terminal)

### keywords

- run_kubesphere_command.py, ogi-llm, kubectl auth can-i, KubeSphere API, HTTP 403, WebSocket, SSH port forward, 10.10.92.3:30880, Host, Origin, token Cookie, m2d-command-proof-6642112a

## Task 2: Use the installed kubesphere-operations skill for hot storage and cluster commands, completed

### rollout_summary_files

- rollout_summaries/2026-09-25T07-36-16-6zJx-kubesphere_hot_storage_command_automation_skill.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T15-36-16-01a0d77e-593f-72a0-868a-e49f7c470b33.jsonl, updated_at=2026-09-26T17:19:22+00:00, thread_id=01a0d77e-593f-72a0-868a-e49f7c470b33, skill validation and project-path checks passed)

### keywords

- kubesphere-operations, transfer_m2d_hot_stream.py, transfer_m2d_hot_via_jump.py, read_m2d_hot.py, read_m2d_hot_logs.py, /hot/upload, /1-H集群-热存储/zzy-data/upload, incremental upload, readback

## User preferences

- when the user asked for “自动化命令”“可以创建删除任务等等” -> use the verified automated channel and read back state instead of asking the user to manually paste routine KubeSphere commands. [Task 1]
- when the user requested the workflow as a skill -> reuse the installed procedure for transfers, logs, query/submit/delete/replace work rather than maintaining a second ad-hoc implementation. [Task 2]

## Reusable knowledge

- `scripts/run_kubesphere_command.py` establishes the SSH forwarding, OAuth login, webpage-terminal WebSocket session, segmented script transport, output capture, and exit-code propagation. It proved a `parallelism=0` create/query/delete Job without Pod/GPU use, plus >7KB scripts, Chinese output, and remote `exit 7`. [Task 1]
- A normal KubeSphere management API HTTP 403 does not establish that the webpage terminal lacks permission: `kubectl auth can-i create jobs -n ogi-llm` and `delete jobs` were both `yes` there. After a disconnect/timeout, query exact Job/Pod state before retrying; results may be unknown. [Task 1]
- Hot storage is container `/hot/upload/` and FTP `/1-H集群-热存储/zzy-data/upload/`; `/项目数据/` is not hot storage. Upload deltas only, never overwrite running release source, and read back after transfer. [Task 2]
- Related skill: `/home/wangyukun/.codex/skills/kubesphere-operations/SKILL.md`. [Task 2]

## Failures and how to do differently

- 5090 direct console access timed out and the jump host could not resolve the console hostname. Use the tested private IP over SSH forwarding with correct `Host`, `Origin`, and token Cookie; Bearer-only WebSocket handshakes timed out. [Task 1]
- File upload/readback, submitted Job, allocation, running Pod, completed training, and completed result are separate evidence states. Do not replay create/delete blindly after connection loss or promote a single receipt into later states. [Task 1][Task 2]

# Task Group: Local HTML/SVG visualization delivery
scope: Create self-contained browser animations; retain the reported pelican file-opening incident as a scoped historical workaround only.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws; reuse_rule=the generated visualization path, port, and HTTP workaround are session-specific; do not generalize one local-opening failure into a default delivery rule.

## Task 1: Create and preview a pelican-riding-a-bicycle SVG animation, partial

### rollout_summary_files

- rollout_summaries/2026-09-25T05-21-47-O7JY-svg_pelican_bike_animation_local_preview.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T13-21-47-01a0d703-3735-7181-a75d-117f195f6a6e.jsonl, updated_at=2026-09-26T13:44:55+00:00, thread_id=01a0d703-3735-7181-a75d-117f195f6a6e, reported local-opening failure; HTTP workaround verified, final browser display unconfirmed)

### keywords

- HTML, SVG, pelican, bicycle, CSS animation, python3 -m http.server, localhost, port conflict, OSError: [Errno 98] Address already in use, HTTP 200

## User preferences

- for a creation request, the user said “不要检索，不要思考，直接开始干，干完直接展示” -> implement and present directly; do not front-load searching or a long plan. [Task 1]

## Reusable knowledge

- The completed page was `/home/wangyukun/.codex/visualizations/2026/09/25/01a0d703-3735-7181-a75d-117f195f6a6e/pelican/index.html`, with self-contained SVG animation and pause/resume controls. [Task 1]
- After the user reported this specific animation would not open, `python3 -m http.server 18765 --bind 127.0.0.1 --directory <dir>` and an HTTP `200` check provided a working workaround. It is evidence about this incident, not a general local-artifact delivery requirement. [Task 1] [ad-hoc note]

## Failures and how to do differently

- The user reported this animation's local path would not open, but did not confirm final browser display; use an HTTP workaround only after a comparable reported opening failure, rather than offering unsolicited localhost URLs. [Task 1] [ad-hoc note]
- Port `8765` failed with `OSError: [Errno 98] Address already in use`; for this workaround, switch to an available alternate port and verify it rather than retrying the occupied port. [Task 1]

# Task Group: Codex project conversation-title management for multi-task research chats
scope: Rename 5090 project conversations for future retrieval without changing anything but a thread title.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws; reuse_rule=use only for Codex project thread-title work; re-read current thread content and preserve originals where the dominant topic is ambiguous.

## Task 1: Rename 5090 project conversation titles by created date and mainline, completed

### rollout_summary_files

- rollout_summaries/2026-09-24T04-54-55-STE2-5090_multi_task_conversation_title_normalization.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T12-54-55-01a0d1c4-44ee-7233-832b-9ec4aba49ffe.jsonl, updated_at=2026-09-26T16:48:34+00:00, thread_id=01a0d1c4-44ee-7233-832b-9ec4aba49ffe, 29 titles verified; 13 accurate titles and five title-less histories unchanged)

### keywords

- codex_app__list_threads, codex_app__read_thread, codex_app__set_thread_title, createdAt, Asia/Shanghai, MMDD｜主题, m2d-5090, multi-task-chat, title-normalization

## User preferences

- when naming a chat, the user corrected: “中间的tag不用，标题要更简洁，更能知道里面的元素” -> use `MMDD｜具体主题`, without a type tag. [Task 1]
- when the user said “我经常一个chat做很多事情” -> inspect the starting goal, important turns, and actual outputs; title the most retrievable unified research thread rather than the old title or final local task. [Task 1]
- when the topic cannot be determined, the user asked to keep the original name -> do not force a guessed title for mixed/low-evidence chats. [Task 1]
- when the user said “就做5090上面的” -> limit title maintenance to `remote-ssh-discovered:ubt-5090` project conversations. [Task 1]

## Reusable knowledge

- Use thread `createdAt`, converted to `Asia/Shanghai`, for the `MMDD` prefix; do not use `updatedAt`. A compact unified title may include equally important elements, e.g. `0923｜CausalCodec精度与C64迭代`. [Task 1]
- Change only via `codex_app__set_thread_title`; do not alter project name, content, ownership, sort, pin, or archive state. In this run 29 titles were read back and verified; 13 good originals and five title-less histories were left unchanged. [Task 1]

## Failures and how to do differently

- Type-tagged titles and vague topics were rejected -> begin with `MMDD｜主题`, using concrete objects, problems, experiments, or deliverables. [Task 1]
- Thread-tool outputs may be JSON strings: inspect the returned type before accessing `.threads` or parsing. [Task 1]
- Renaming changes `updatedAt` and can reorder visible chats; do not promise the sidebar order is unchanged merely because no sort/pin/archive call was made. [Task 1]

# Task Group: /home/wangyukun/ubt_isaac_sim_ws UTars / Isaac Sim / VLA Feishu technical-report handoff
scope: Produce a concise, final-version technical handoff package for Feishu without importing unrelated Musics2Dance history or turning diagnostics into formal results.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws; reuse_rule=report layout and source hierarchy are reusable; recheck evidence paths, media links, and final metrics before a new handoff.

## Task 1: Create and verify concise Feishu technical handoff package, completed

### rollout_summary_files

- rollout_summaries/2026-09-22T09-19-17-yUpo-utars_techreport_feishu_handoff_and_training_inference_consi.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T17-19-17-01a0c869-924b-71d0-9a4b-caf03d445046.jsonl, updated_at=2026-09-24T05:57:11+00:00, thread_id=01a0c869-924b-71d0-9a4b-caf03d445046, final Markdown package, download paths, and unresolved training/inference boundary)

### keywords

- UTars, Isaac Sim, VLA, Feishu, 飞书云文档, REPORT.md, 飞书正文.md, utars-techreport-20260922, E1—E6, UTars飞书交接材料.zip

## Task 2: Update report videos and rerun corrected upper evaluation, partial

### rollout_summary_files

- rollout_summaries/2026-09-23T08-12-20-jrML-utars_report_upper_rerun_and_video_package.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T16-12-20-01a0cd52-a44c-7b71-8c87-49b729abc493.jsonl, updated_at=2026-09-24T08:50:12+00:00, thread_id=01a0cd52-a44c-7b71-8c87-49b729abc493, corrected-inference upper evaluation completed: 13/40 full-task success)

### keywords

- 视频索引.md, 20260923_upper_8f8_40ep, stage score, actual completion, inference_steps=8, rtc_frozen_steps=8, finish.sh, PyAV

## User preferences

- when the user said “只写 UTars / Isaac Sim / VLA” -> do not add Musics2Dance to this report. [Task 1]
- when the user asked “只要几页”“按最终的版本来，不用讲中间迭代的版本” -> default to about three pages, covering only final method/design intent and representative results. [Task 1]
- when the user said “不足要少说，挑重点的贡献说，比如原来我接手的时候没有的东西现在做完了” -> organize around “原来缺什么 → 补了什么 → 现在能做什么”, not an iteration/debugging chronology. [Task 1]
- when the user needs “飞书云文档格式” -> deliver copyable/importable Markdown first, with images, video, and evidence index as companion material. [Task 1]
- for video evidence, the user said “直接发这里”“给路径，我下载” -> provide absolute downloadable local paths, not only an embed or prose. [Task 1]
- when the user corrected “新的推理才是对的” and “不用管严格，只要成功就行啊” -> rerun with the repaired inference pipeline and use full completion (place on target, release, no drop) rather than grasp-tilt warning as the main metric; when they said “不用一直等”, launch long evaluation in the background with status and finalizer paths. [Task 2]
- for report videos, selected clips must carry the complete-batch denominator/provenance; upper success means target placement, release, and no drop, not an old stage score or a grasp-tilt warning alone. [Task 2]

## Reusable knowledge

- Recommended handoff structure: “目标/贡献 → 最终方法 → 代表性验证 → 接手入口与后续方向”. Distinguish formal results from diagnostics: lower-model representative completion is actual 7/40, never an older stage score. [Task 1]
- Current verified package is `/home/wangyukun/ubt_isaac_sim_ws/docs/briefs/utars-techreport-20260922/`: `REPORT.md` is canonical, `飞书正文.md` is an identical copy; old Word/PDF/JSON are drafts, not current truth. [Task 1]
- `UTars飞书交接材料.zip` contains eight files: main draft, Feishu copy, handoff index, environment record, README, technical architecture, scene image, and representative success video. Five Markdown documents had no broken local links, the two bodies matched exactly, E1—E6 were present, and images/package generation succeeded. [Task 1]
- The corrected upper rerun uses `20260923_upper_8f8_40ep/`, 40 fixed seeds, 8 inference/8 frozen RTC steps, clipping, and 16-action replanning. It completed `13/40 = 32.5%` full-task success (stage score `33/40` is not the report metric), with 40 results, 120 H.264 videos, and no client errors validated before rebuilding the 20-file report ZIP; use GR00T venv PyAV because `ffprobe` is absent. [Task 2]

## Failures and how to do differently

- The first proposal was too long and included intermediate iterations; start with the short, final-version, contribution-led structure. [Task 1]
- The package was not actually imported/published to Feishu. Before upload, check image embedding and formula rendering, and replace local absolute paths with internal shared links or attachments. [Task 1]
- Do not say “训推不一致已解决”: runtime action/reference/timing defects are fixed, but 7/40 lower completion leaves policy/physics closed-loop reliability unresolved. [Task 1]
- Do not label old upper stage scores or selected historical videos as current full-task success; old videos remain explicitly historical, while the corrected upper batch is 13/40 complete. [Task 2]

# Task Group: /home/wangyukun/ubt_isaac_sim_ws bilingual UTars robotics portfolio publishing
scope: Build a bilingual, video-first portfolio from provenance-checked UTars/Isaac Sim evidence without inflating simulation or selected-video claims.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws; reuse_rule=recheck the canonical report, source clips, current Pages deployment, and profile-repository state before a new publication.

## Task 1: Publish bilingual visual portfolio and selected UTars clips, partial

### rollout_summary_files

- rollout_summaries/2026-09-24T09-11-35-qF1a-bilingual_utars_portfolio_website_video_update.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T17-11-35-01a0d2af-3ffe-7823-9939-52d5a350b8ac.jsonl, updated_at=2026-09-24T12:45:00+00:00, thread_id=01a0d2af-3ffe-7823-9939-52d5a350b8ac, website commit pushed; Pages was still building and profile push unverified)

### keywords

- lbtwyk.github.io, bilingual, video-first, PyAV, assets/videos/upper.mp4, episode_023, seed 2026080604, bb303ee, GitHub Pages

## User preferences

- when the user requested “中英双语的视觉作品集” with large videos and concise/fancy descriptions -> preserve bilingual, visual-first dark/cyan presentation; avoid unnecessary technical detail. [Task 1]
- when the user rejected an upper clip as visually unbalanced -> compare the full successful cohort visually as well as quantitatively; do not claim “completely level.” [Task 1]

## Reusable knowledge

- Start from canonical `docs/briefs/utars-techreport-20260922/REPORT.md` and `视频索引.md`; retain batch denominators plus simulation/accelerated-playback labels so selected clips never imply real-robot execution or an inflated success rate. [Task 1]
- System `python3` lacks PyAV; use `/home/wangyukun/ubt_isaac_sim_ws/ubt_vla_ws/ubt_vla_code/Isaac-GR00T-N1.7/.venv/bin/python` for inspection/export. The revised upper clip is September 23 seed `2026080604`, `episode_023/combined.mp4`, source `0–8.0s`, exported as `assets/videos/upper.mp4`; it is more balanced but still pitches during lifting. [Task 1]
- Website commit `bb303ee621fee481543d5d01138a076e347d06f0` was pushed to `lbtwyk/lbtwyk.github.io` main; the last check only showed Pages `building`. [Task 1]

## Failures and how to do differently

- A low-tilt metric did not make the first upper selection visually balanced -> review full successful clips for symmetry, completion, and endpoint quality before publishing. [Task 1]
- Do not claim the GitHub profile repository was published: it was cloned but this rollout has no profile commit/push verification. [Task 1]

# Task Group: research-loop training acceptance and repository synchronization
scope: Make a user-authorized training check complete its operational lifecycle and report formally; keep ready artifact publication independent from issue/PR discussion.
applies_to: cwd=/home/wangyukun/research-loop-workflow + /home/wangyukun/ubt_isaac_sim_ws/m2d-ws; reuse_rule=apply automatic repair/resume only inside an approved experiment contract; stop for scientific route/contract/claim/outcome decisions or external blockers.

## Task 1: Separate repository sync from issue/PR discussion, completed

### rollout_summary_files

- rollout_summaries/2026-09-18T07-43-05-YZAg-research_workflow_preflight_and_github_handoff_alignment.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T15-43-05-01a0b378-0fdd-7bb1-8c60-f051ce14156c.jsonl, updated_at=2026-09-24T15:39:53+00:00, thread_id=01a0b378-0fdd-7bb1-8c60-f051ce14156c, workflow, install, and preflight-policy validation passed)

### keywords

- training-check-acceptance, automatic-loop, same-contract-repair, formal-report, github-repository-sync, issue, PR, Web, GitRPC::BadObjectState, WORKFLOW.md

## Task 2: Correct local versus cluster preflight, completed

### rollout_summary_files

- rollout_summaries/2026-09-18T07-43-05-YZAg-research_workflow_preflight_and_github_handoff_alignment.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T15-43-05-01a0b378-0fdd-7bb1-8c60-f051ce14156c.jsonl, updated_at=2026-09-24T15:39:53+00:00, thread_id=01a0b378-0fdd-7bb1-8c60-f051ce14156c, policy/docs/install validation passed; no experiment launched)

### keywords

- local-gpu, Slurm, Kubernetes, TRAINING_PREFLIGHT.md, TRAINING_EFFICIENCY.md, checkpoint save/reload, queue wait, declared result, experiment ledger

## User preferences

- when the user said “检查就是要自动处理好问题，有结果就按正式方式汇报，除非有科学决策再停下来，要不然都自动处理” -> a check authorizes monitoring, same-contract repair/resume, evaluation, analysis, evidence updates, and formal reporting; do not return routine status or ask for another check. [Task 1]
- when the user corrected “有阶段性结果再更新issuespr，很多时候是把产物证据更新repo，web可以读然后分析就可以了” -> push ready useful evidence independently; issue/PR discussion is only for a stage result or needed decision. [Task 1]
- when the user said “不要规则越堆越多” -> retain one concise operational rule rather than accumulating overlapping clauses. [Task 1]
- when local preflight is in scope, the user required it remain lightweight but prove the real flow runs without errors; cluster preflight must compare normal and aggressive viable configurations and choose the fastest evidence-supported option. [Task 2]

## Reusable knowledge

- The `training-check-acceptance` stop boundary is a required scientific route/contract/claim/outcome decision or an external blocker that cannot be repaired locally; it never authorizes the agent to choose those decisions. [Task 1]
- Skill source is `packs/core/skills/training-check-acceptance`; runtime-specific modules cover local, Slurm, and Kubernetes. Keep large/private runtime artifacts out of Git while publishing durable summaries, selected logs, and accessible locations. [Task 1]
- Local/direct-GPU preflight is a real-data isolated run through one update, checkpoint save/reload, and declared downstream entrypoints; it proves execution readiness, not quality or throughput. Cluster preflight compares queue wait plus time to the declared result under fixed science, then proves the selected exact launch on its target cluster; Slurm ledger `preflight` remains Slurm-specific. [Task 2]

## Failures and how to do differently

- After changing a stopping rule, search the whole workflow repository, installed skill, project `AGENTS.md`, and example project for stale bounded-cycle wording. [Task 1]
- `GitRPC::BadObjectState` on remote-tree deletion -> fetch the remote tree first and delete only paths that still exist remotely. [Task 1]
- Do not describe local preflight as only changed-seam checks or cluster preflight as merely “can start”; preserve the end-to-end local proof and cluster efficiency comparison. [Task 2]

# Task Group: ogi-llm Kubernetes GPU scheduling, quota diagnosis, and split delivery
scope: Diagnose and operationally prepare M2D GPU Jobs safely; distinguish admission quota, same-node scheduling, and trainer failure, preserving active work and exact scientific contracts.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws; reuse_rule=commands/capacity/job state are time-specific; inspect current nonterminal Pods, owner metadata, Events, requests, and `ogi-llm` eligibility before cleanup, split, or status claims.

## Task 1: Recover the blocked M2D committed-trajectory Job, completed

### rollout_summary_files

- rollout_summaries/2026-09-19T08-25-39-vb59-kubernetes_gpu_quota_and_committed_trajectory_cost_audit.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T16-58-01-01a0b8c5-6493-7560-9a92-78a194682cf3_01a0c32f-be1c-71f1-bdf7-6d94456d54fa.jsonl, updated_at=2026-09-24T06:27:16+00:00, thread_id=01a0b8c5-6493-7560-9a92-78a194682cf3, quota diagnosis and no-budget-change cost audit)

### keywords

- kubectl, ogi-llm, gpu-quota, nvidia.com/gpu, FailedCreate, Running 0/1, Pending, node13, node14, m2d-causal-stability-2h-gs7wg, JSONPath, formal_started

- Related skill: skills/kubernetes-gpu-quota-diagnosis/SKILL.md

## Task 2: Split the Pending two-GPU stability suite into two one-GPU Jobs, delivery verified but not submitted

### rollout_summary_files

- rollout_summaries/2026-09-18T05-30-08-lolw-omg_root_rotation_audit_and_split_stability_training.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T00-05-52-01a0b2fe-587e-7a60-b6b1-ebaf4a49312e_01a0c4b7-742e-7c20-bc9f-f20250f95eea.jsonl, updated_at=2026-09-23T16:46:46+00:00, thread_id=01a0b2fe-587e-7a60-b6b1-ebaf4a49312e, split package/tests/readback verified; cluster execution unverified)

### keywords

- m2d-causal-stability-2h, m2d-causal-stability-1h-a, m2d-causal-stability-1h-b, APPLY_SPLIT_1H.txt, m2d-update-62d86a24a125.pyz, test_g1_stability_split.py, MPS, shared-music, awaiting_cluster_submission_or_startup

## Task 3: Enforce `ogi-llm` scheduling and prepare automatic calibration continuation, partial

### rollout_summary_files

- rollout_summaries/2026-09-22T02-12-44-bDMc-ogi_llm_gpu_isolation_and_automatic_training_continuation.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T10-12-44-01a0c6e3-0d78-7bf3-b128-19efed157ec0.jsonl, updated_at=2026-09-24T06:27:02+00:00, thread_id=01a0c6e3-0d78-7bf3-b128-19efed157ec0, continuation package/mock tests verified; local host could not enable it)

### keywords

- ogi/node-pool=ogi-llm, START_AUTO.txt, m2d-music-calibration-12500-3h, extend-12500, Complete=True, Failed=True, reviewer, 6sol high

## User preferences

- when the user asked “怎么看现在谁在跑，如果我自己的有问题占了就可以清” -> inspect current nonterminal Pods, GPU requests, `author`, and owner controllers before suggesting deletion; low utilization alone is not abnormality. [Task 1]
- preserve an existing waiting Job rather than blindly resubmitting it: Kubernetes can retry Pod creation after quota frees. [Task 1]
- when the user said “用什么组就只能申请那个组的卡” and “正确的应该是允许这个组里的所有卡” -> schedule only in `ogi-llm`; do not treat other-pool tolerations as permission and do not pin hostnames when any eligible `ogi-llm` node should work. [Task 1]
- when splitting the stability Job, the user said “无需再做排队诊断或询问确认” and “音乐已完成，不要重算” -> make only the specified operational change, retain `m2d-causal-history-3h-llm-only`, and reuse the verified shared music cache. [Task 2]
- when the user clarified “要自动的” for the 6250→12500 continuation -> provide a detached watcher that waits for completion and avoids manual second intervention. [Task 3]
- when music preparation or independent M2D tasks are in scope, the user said “记住音乐处理速度要拉满速度，利用好h卡” -> prioritize measured throughput, H-card utilization, reuse loaded models/shared music caches, and concurrent independent tasks within each GPU when resources permit; follow the currently authorized card limit. [ad-hoc note]

## Reusable knowledge

- Quota uses requested `nvidia.com/gpu`, not instantaneous utilization or name strings such as `4gpu`. For dotted resource keys, use JSON/JSONPath rather than `custom-columns`. [Task 1]
- `m2d-commit-trajectory-3h-fast-r1` initially had 0 Pods with `requested ...=3, used ...=8, limited ...=9`; later `m2d-commit-trajectory-3h-fast-r1-5wfq2` was Running on 3 GPUs, so no cleanup was justified. Once a Pod exists, `kubectl logs -f --tail=50 -n ogi-llm job/<job>` can distinguish `preflight` from `formal_started` plus increasing `update`. [Task 1]
- Corrected multi-GPU YAML uses exactly one `ogi/node-pool=ogi-llm` toleration and no `affinity`, `nodeSelector`, `nodeName`, or other-pool tolerance; hot-storage readback proves artifact delivery, never submission/state. [Task 1]
- Historical 2026-09-22 snapshot: node13 had visible namespace requests totaling seven GPUs (3-GPU history Job plus a 4-GPU job), while the pending stability Job requested two GPUs in one Pod; node capacity, other namespaces, and actual free GPUs were not observable. Five shared-music shards were independent one-GPU Pods, not a five-GPU same-node requirement. [ad-hoc note]
- Split lanes are fixed: `1h-a` has `cof_continue`, `decoder_continue`, `decoder_phase`; `1h-b` has `cof_rollout_stability`, `decoder_rotation`, `decoder_rotation_phase`. Preserve 6250 updates, trainer/config/randomness/effective batch, MPS concurrency, disjoint shard outputs, and merge six completion receipts before evaluation/rendering. `tests/test_g1_stability_split.py` passed 2 tests; the mock proved one old-Job deletion/two creates without history-Job mutation. [Task 2]
- `extend-12500/START_AUTO.txt` waits for `Complete=True`, stops on `Failed=True`, detects an existing continuation, then submits `m2d-music-calibration-12500-3h`; it preserves original artifacts, uses new `training-12500/` outputs, one `ogi-llm` toleration, and no hostname restriction/suspend/delete behavior. Mock cases passed, but it was only uploaded/readback-verified because local host lacks `kubectl`. The requested independent reviewer setting `6sol high` was not implemented/verified. [Task 3]

## Failures and how to do differently

- A pasted `describe` state can be stale: re-query the newest nonterminal Pod listing before acting. With no Pod, read Job Events/quota; Job logs are not useful until a Pod exists. [Task 1]
- Namespace-only Pod output and Forbidden node listing do not establish total node capacity, free GPUs, other-namespace allocations, or fragmentation. [Task 1]
- Never claim a Job was submitted/running from YAML or a hot-storage receipt. Distinguish prepared, uploaded/readback-verified, submitted, allocated, running, and completed. Archive exact old Job/Pod state before replacement; only merge after both shards carry all six receipts. [Task 2]
- A manual continuation is not enough when automatic continuation was requested; include the detached watcher and state whether it has actually been enabled. Do not claim the reviewer change without locating, applying, and verifying its configuration. [Task 3]

# Task Group: Musics2Dance OMG/O-Dance root-rotation provenance and data gate
scope: Decide whether OMG/O-Dance is fit for causal-codec training and trace abrupt root rotations to the actual layer before proposing remediation.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=dataset counts/rates are audit-specific; rerun the quality gate and provenance checks for changed data/version/representation.

## Task 1: Audit OMG/O-Dance quality and source provenance, completed

### rollout_summary_files

- rollout_summaries/2026-09-18T05-30-08-lolw-omg_root_rotation_audit_and_split_stability_training.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T00-05-52-01a0b2fe-587e-7a60-b6b1-ebaf4a49312e_01a0c4b7-742e-7c20-bc9f-f20250f95eea.jsonl, updated_at=2026-09-23T16:46:46+00:00, thread_id=01a0b2fe-587e-7a60-b6b1-ebaf4a49312e, all packages audited; raw O-Dance launch gate not met)

### keywords

- OMG, O-Dance, root-rotation, retarget, Parquet, SciPy, quaternion, wxyz, xyzw, 6D, audit_root_rotation_provenance.py, root_events_over90.jsonl

## User preferences

- when the user said “下载完了如果数据质量更好，就可以跑上od栈的causalcodec训练了” -> download completion is not launch authorization; compare the user-relevant quality gate first. [Task 1]
- when the user asked “根因调查” -> trace raw source, loader, quaternion conversion, slicing, 6D conversion, and codec round trip rather than stopping at aggregate rates. [Task 1]

## Reusable knowledge

- 9/9 packages completed: 26,149 episodes/10,541,226 frames. FD root >90° was `0.130/100000`, max `93.18°`; OMG was `0.416/100000`, max `175.40°`. OMG joint jumps were lower, but the root gate was not improved; overlapping OMG episodes make these exposure rates, not matched unique-event rates. 79.26% of OMG episodes are shorter than the 316-frame window, so a short-episode causal contract is needed before a direct switch. [Task 1]
- Direct official-Parquet filtering plus independent SciPy SO(3) for 42 episodes/49 events found loader error `0.0`, contiguous indices, SciPy/project difference `1.25e-10°`, and 6D round-trip difference `1.47e-5°`; seven source files matched fixed-version SHA256. Audited jumps were not introduced by loading, index/slice, wxyz→xyzw, 6D, or codec conversion; at least some are upstream human-to-G1 retarget/source defects. [Task 1]
- 6D is preferable for training representation but cannot repair invalid source trajectories. Favor targeted discontinuity repair/control with an unmodified baseline; preserve normal amplitude/turns and do not globally smooth/delete/filter by one threshold. [Task 1]

## Failures and how to do differently

- Saved-quaternion checks alone cannot rule out processing faults -> directly filter official Parquet by IDs, independently compute SO(3), verify frame/timestamps, and hash official files. [Task 1]
- Do not call OMG “cleaner” merely because joint-jump counts are lower when root jumps are worse. [Task 1]

# Task Group: Musics2Dance CausalCodec mechanism, coverage repair, and route selection
scope: Diagnose causal D+C generation separately from codec reconstruction, repair OD supervision semantics generically, and evaluate causal-native routes without overstating execution proof as quality.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=recheck the ledger, frozen contract, codec/checkpoint identity, and GPU availability before training; the completed codec repair does not authorize OD generator training while residual tails remain unresolved.

## Task 1: Review CausalCodec mismatch training direction, partial with a ranked next candidate

### rollout_summary_files

- rollout_summaries/2026-09-21T10-07-03-7i5T-causal_music_calibration_future_dependence_audit.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T21-19-48-01a0c36e-f518-7801-8bb2-f9ca761f5cdd_01a0c41f-6c44-7be2-a94e-094e4d91055f.jsonl, updated_at=2026-09-24T06:27:09+00:00, thread_id=01a0c36e-f518-7801-8bb2-f9ca761f5cdd, causal-native audit plus Future-dependence diagnostic; downstream benefit unproven)

### keywords

- causalcodec, multirate1024_balanced, D512+C16, K64, H4/C4, NFE10, CoF, ES, GAN, Resampling Forcing, self-resampling, rotation-collapse, z_ref - e(D_sampled)

## Task 2: Audit Future-music calibration dependence and benefit, diagnostic completed

### rollout_summary_files

- rollout_summaries/2026-09-21T10-07-03-7i5T-causal_music_calibration_future_dependence_audit.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T21-19-48-01a0c36e-f518-7801-8bb2-f9ca761f5cdd_01a0c41f-6c44-7be2-a94e-094e4d91055f.jsonl, updated_at=2026-09-24T06:27:09+00:00, thread_id=01a0c36e-f518-7801-8bb2-f9ca761f5cdd, dependence established; dance-quality gain unproven)

### keywords

- Future, calibration, reliability, Future-zero, wrong-Future, matched-state, 54/54, forecast-utility proxy MSE, future-dependence.json, dynamic, fixed

## Task 3: Diagnose active-but-jittery causal codec mechanism, partial

### rollout_summary_files

- rollout_summaries/2026-09-23T03-21-04-5fep-causal_codec_root_cause_and_od_complete_sequence_repair_audi.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T11-21-04-01a0cc47-fa15-7a80-a814-6a39aa0e97a1.jsonl, updated_at=2026-09-25T06:23:38+00:00, thread_id=01a0cc47-fa15-7a80-a814-6a39aa0e97a1, mechanism diagnosis; no formal route validated)

### keywords

- D+C, 6D rotation, Gram-Schmidt, decoder jitter, phase artifact, repeat_interleave(2), MotionStreamer, Two-Forward, Resampling Forcing

## Task 4: Implement, train, and audit OD complete-sequence coverage repair, partial

### rollout_summary_files

- rollout_summaries/2026-09-25T05-22-34-yRj0-od_c64_complete_sequence_root_cause_repair_and_verification.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T13-22-34-01a0d703-eed8-7c12-b917-3b15bb36329e.jsonl, updated_at=2026-09-27T15:39:20+00:00, thread_id=01a0d703-eed8-7c12-b917-3b15bb36329e, complete-sequence root-cause repair, 100k run, and exact-state verification; generator still gated)

### keywords

- source_aligned_complete_target_blocks_v1, CausalMotionWindows, g1_codec_windows.py, window_protocol, 100000 updates, 144 clips, residual tails, run_kubesphere_command.py, 53 tests, 66.37M, 3999d14

## User preferences

- when choosing a research route, the user asked “从第一性原理和成熟度和novelty出发” -> separate mechanism fit, evidence, engineering cost, and innovation boundary, then give a clear investment order rather than assuming ES is preferred. [Task 1]
- keep the new codec, 183/18 split, 6250 updates per arm, and fair controls; do not shrink budget or alter the frozen contract because ES/GAN is slow. Do bounded/read-only validation first and request approval before formal training. [Task 1]
- when the user worried calibration might “hacking导致不用未来” -> change Future while holding history, Past, Style, decoder state, and randomness fixed; report Future sensitivity separately from quality usefulness. [Task 2]
- when the user contrasted “更活跃” motion with accuracy, jitter, and robot executability -> report amplitude, reconstruction, long-horizon stability, geometry validity, and executability independently. [Task 3]
- when the user said “不要patch一个specific问题，而是做成通用的solution” -> repair shared sampling/target semantics; preserve old evidence and avoid clipping, smoothing, or hand-picked exclusions. [Task 4]

## Reusable knowledge

- Frozen system: `multirate1024_balanced` seed1234 at 100000 steps, native38/30Hz, D512+C16, two frames per latent; both generator branches consume full K64 D+C history, deployment is H4/C4 with 8-frame commits and C NFE10. [Task 1]
- Current CoF is commit-wise D+C Two-Forward: self-generate/rewrite the last 4 tokens, then use sampled D to relocate the C target. It lacks the old explicit B71/physical boundary-state closure, so do not reuse that old novelty claim. [Task 1]
- Preferred next candidate is teacher-free supervised history resampling/Resampling Forcing: generate an erroneous K64 D+C history near real history with stop-gradient, then supervise real-future D classification and C denoising; relocate C as `z_ref - e(D_sampled)` when D changes. Compare first against original CoF from same start, 183/18, 48 condition groups/update, and 6250 updates, assessing long-horizon degradation, amplitude, pauses, diversity, and music response at equal GPU time. [Task 1]
- Rotation failure is not solely exposure bias: real generator-history and decoder-prefix controls still flipped; all 20 generated >90-degree events coincided with 6D direction-basis degeneration. Treat rotation/geometry supervision as a separate study. The 162 one-minute feedback split had no stable benefit, and CPU self-resampling finite/nonzero gradients establish connectivity only. [Task 1]
- Matched-state Future-zero/wrong-Future changed all `54/54` states (mean next-segment joint-angle difference 7.28°/7.80°); repeated original input was bitwise identical, so Future is causally used. This does not establish quality gain: music-score differences were non-significant and removing history feedback had a higher mean; the narrow supported result is 27.8% forecast-utility proxy-MSE reduction on the audio-disjoint 13-song subset, not better dance quality. [Task 2]
- Prior 38D reconstruction retained roughly 97.3% range and 97.2% speed; low amplitude was concentrated in autonomous generation. In 56 severe D+C cases, FP32 replay reproduced 56/56 failures versus 0/56 normal controls: near-degenerate 6D bases are amplified by Gram-Schmidt, while 10→100 denoising steps only changed failures 56→51. A separate two-frame phase artifact flips jerk parity when codec start shifts by one frame. [Task 3]
- `model/g1_token_causal_codec.py` has causal convolutions, two frames/token, K64-compatible history, and default `repeat_interleave(2)`; polyphase, rotation-stability, and generated-history training are matched-ablation candidates, not validated fixes. [Task 3]
- The OD defect was train/inference coverage mismatch: omitted starts/transitions could expose `53.77 -> 2.337e14` loss. `dataset/g1_codec_windows.py` now uses `CausalMotionWindows`: uniformly choose a sequence then a non-overlapping source-aligned 64-frame target block, retain up to 252 real preceding frames, mask right padding, and give every complete source token target support. [Task 4]
- The repair audit covered 15,426 sequences from six sources, 467 lengths, 128,176 blocks, and 7,712,902 real complete-token frames. 53 tests, source-aligned equivalence, 66.37M-parameter exact resume, TF/plain-RF/strong-RF resumes, and 160-frame generation passed. The repaired codec then completed 100,000 updates: the matched 144-clip panel improved joint median `16.044→1.477°`, orientation `24.556→1.055°`, amplitude `0.360→0.994`, severe failures `6/144→0/144`, and million-plus logged losses `124/5000→0/5000`. New checkpoints record `window_protocol` and reject old incomplete-coverage checkpoints/inputs. [Task 4]

## Failures and how to do differently

- Do not equate continuous-distribution ES theory, 162 inference diagnostics, or CPU finite-gradient checks with current D+C hard-D-credit/four-particle long-backprop effectiveness, convergence, or speed. GPU self-resampling throughput remains unverified after an OOM under roughly 30 GiB competing use. [Task 1]
- Do not copy video-method flow timesteps, KV cache, error bank, or teacher setup directly; retain discrete D/continuous C relocation, pred-x0/cosine diffusion, K64 history, and deployment semantics. Do not jointly change feedback split, history construction, rotation loss, and ES window in the first comparison. [Task 1]
- Nonzero attention/reliability cannot disprove hacking; matched intervention can prove dependence but not usefulness. Do not claim self-correction quality from 6-to-2 rotations/small scores or mix local posthoc trajectories with formal cluster scores. [Task 2]
- Do not equate “more active” with correct or safe motion, attribute arbitrary latent-noise fragility, or substitute smoothing, C scaling/removal, more width, or extra sampler steps for causal controls. [Task 3]
- Loss-mask changes alone do not repair positions the sampler never presents: compare objective masks and the actual sampling distribution across every sequence length and full-sequence inference position. The completed 100k codec validates a generator input, not OD generator or long-dance quality: 340/18,541 cached clips still had standardized residual magnitude >20 and the five largest tails had jerk intensity `1.87–3.69×` reference. Investigate coordinate/time continuity and component-wise errors rather than smoothing, clipping, filtering, or starting OD generators. Never resume the damaged old protocol route; reconcile live Job/Pod state and hot-storage completion records before repeating stale “not submitted/403” text. [Task 4]

# Task Group: Musics2Dance FineDance-inspired GS-G1 and parallel MMR+ evaluation
scope: Adapt and use a clearly labeled G1 genre-matching metric alongside MMR+ across saved motion outputs; preserve metric provenance, duplicate-audio disclosure, and conservative comparison boundaries.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=GS-G1 is an independent robot adaptation, not official FineDance human-motion GS; reuse the frozen scorer contract only after checking the output inventory and evaluation population.

## Task 1: Adapt and validate GS-G1, completed

### rollout_summary_files

- rollout_summaries/2026-09-22T08-13-49-aUbT-g1_genre_matching_score_parallel_mmr_evaluation.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance, rollout_path=/home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T16-13-49-01a0c82d-a4df-7591-ba05-19ea0651f1e1.jsonl, updated_at=2026-09-24T06:27:09+00:00, thread_id=01a0c82d-a4df-7591-ba05-19ea0651f1e1, frozen independent scorer with CPU/GPU proof)

### keywords

- FineDance, Genre Matching Score, GS-G1, AST, AGCN, G1 FK, configs/experiments/gs_g1.json, duplicate-audio, nonduplicate13, local_g1_gpu_lock.py

## Task 2: Score old mainline and local experiments with GS-G1 and MMR+, completed

### rollout_summary_files

- rollout_summaries/2026-09-22T08-13-49-aUbT-g1_genre_matching_score_parallel_mmr_evaluation.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance, rollout_path=/home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T16-13-49-01a0c82d-a4df-7591-ba05-19ea0651f1e1.jsonl, updated_at=2026-09-24T06:27:09+00:00, thread_id=01a0c82d-a4df-7591-ba05-19ea0651f1e1, 17 unique settings and 1,620 records consolidated)

### keywords

- supplement_g1_genre_matching.py, MMR+, history-resampling, rotation-supervision, trajectory-stability, source-inventory.json, song-cluster CI, full18, nonduplicate13

## User preferences

- when the user requested literature `genrematching score` “和 mmr+ 平行” -> retain MMR+, report the new metric separately, and do not create a composite score. [Task 1][Task 2]
- when the user selected an independent G1 adaptation -> call it `GS-G1`; do not claim official FineDance GS/weights exist or compare its absolute values to FineDance human-motion results. [Task 1]
- when the user required 183 songs and disclosure of five duplicate-audio train/test pairs -> always show both full18 and nonduplicate13. [Task 1]
- when the user said “还有resampling的” -> enumerate old mainline, native, rotation, stability, and history-resampling saved-output groups; distinguish historical aliases from unique settings. [Task 2]
- preserve each experiment’s comparison scope and do not auto-accept results: report point estimates and song-cluster CIs, leaving scientific acceptance to the user. [Task 2]

## Reusable knowledge

- Public FineDance repositories had no usable genre/coherent retrieval module; official issues #16/#18 requesting it were unanswered. `GS-G1` is frozen in `configs/experiments/gs_g1.json`: 183 songs, 146 fit/37 validation across 35 audio groups, native G1 FK, AST AudioSet initialization, jointly trainable audio/motion branches, seed1234, 3000 updates, batch32 FP32, and fixed-final scoring. [Task 1]
- AST was strictly converted with evidence at `runs/gs_g1/assets/ast/conversion.json`; CPU proof, GPU batch32 proof, and validation passed. Cross-song margin was 0.5839 with 95% CI [0.4899, 0.6662]. [Task 1]
- `runs/gs_g1/local-evaluation-20260923/` contains `REPORT.md`, `RESULTS.json`, `SUMMARY.csv`, `source-inventory.json`, and `completion.json`: four groups, 17 unique settings, 22 main entries, 30 conditions, 1,620 records, shared 18 songs × 3 seeds × frames264:984. [Task 2]
- Resampling GS means are base .6674/.6442, CoF .6762/.6352, continuous RF .6747/.6329, joint RF .6806/.6415 (full18/nonduplicate13); every key contrast CI crosses zero. The old-mainline vs CoF 18-song gain does not survive the 13-song subset. Rotation B-vs-A’s limited GS signal does not overturn the failed extreme-rotation endpoint; stability/decoder effects are near zero with intervals crossing zero. [Task 2]
- GS-G1 measures style/genre matching only. Keep it separate from MMR+, rotation, beat alignment, amplitude, foot sliding, and visual quality; it does not authorize automatic scientific acceptance. [Task 2]

## Failures and how to do differently

- Do not infer an official FineDance implementation/checkpoint from the paper/repositories. Label adapted retrieval provenance and disclose duplicates. [Task 1]
- A monitor-only remote watcher stalled local work despite an idle 5090. `scripts/local_g1_gpu_lock.py` must serialize actual GPU computation, not process presence. [Task 1]
- Remote hot-storage readback mtimes cannot prove generation order; use completion manifests. Do not count exact saved-motion aliases as independent evidence or call small gains wins when song-cluster CIs cross zero. [Task 2]

# Task Group: Musics2Dance causal codec cluster results and hot-storage delivery
scope: Validate formal causal-codec matrices against local conclusions and make future cluster results readable from the 5090.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=recheck experiment/metric boundaries and deployment state; automatic export applies only to launchers carrying the new code.

## Task 1: Validate the H100 four-variant × three-seed causal codec matrix, completed

### rollout_summary_files

- rollout_summaries/2026-09-21T09-12-03-UVeh-cluster_causal_codec_results_and_auto_export.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance, rollout_path=/home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T17-12-03-01a0c33c-96ce-7991-92b2-b516ea344a29.jsonl, updated_at=2026-09-24T06:27:16+00:00, thread_id=01a0c33c-96ce-7991-92b2-b516ea344a29, all 12 final records identity-checked and reaggregated)

### keywords

- EXP-20260918-fd-causal-codec-capacity, H100, RTX5090, native-MSE, compact256, multirate256, multirate512, multirate512_balanced, verify_comparison.py, completion.json

## Task 2: Add automatic readable result export for future cluster jobs, completed

### rollout_summary_files

- rollout_summaries/2026-09-21T09-12-03-UVeh-cluster_causal_codec_results_and_auto_export.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance, rollout_path=/home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T17-12-03-01a0c33c-96ce-7991-92b2-b516ea344a29.jsonl, updated_at=2026-09-24T06:27:16+00:00, thread_id=01a0c33c-96ce-7991-92b2-b516ea344a29, exporter and four launchers validated; old jobs unchanged)

### keywords

- export_m2d_results.py, results-records.tar.gz, download-manifest.json, /hot/upload/, M2D_HOT_STORAGE.md, run_token_causal_codec_cluster.py, test_m2d_result_export.py

## User preferences

- when asking whether the cluster result “也支持我们本地训练完后的判断” -> compare exact variant, seed, training-step, test-track, and metric boundaries, not one aggregate. [Task 1]
- when the user said “以后要自动导出成果到5090可以读取下载的地方” -> default future cluster launchers to a 5090-readable result directory/records archive. [Task 2]

## Reusable knowledge

- `EXP-20260918-fd-causal-codec-capacity` has 12 completed 100k-step runs, 183 train/18 test tracks, and the same `supervised_geometry_v1`: native-MSE means were compact256 `0.057629`, multirate256 `0.053709`, multirate512 `0.065307`, balanced512 `0.048242`; all seeds reproduce balanced512 < multirate256 < compact256 < ordinary multirate512. All final records passed identity/aggregation checks and `verify_comparison.py` reaggregated them with max error `1.4551915228366852e-11`. [Task 1]
- `scripts/export_m2d_results.py` writes `results-records.tar.gz` and `download-manifest.json` under `/hot/upload/`, including metrics/configs/logs while excluding runtime/raw data/code; it is integrated into four cluster launchers and has a passing exporter test plus `py_compile`. [Task 2]

## Failures and how to do differently

- `550 Permission denied` on FTP `training/` is not training failure: export from a KubeSphere/container-mounted hot disk, then download via jump host. Require `completion.json`, final evaluation records, and fixed-final aggregation; `previous-job.log` around steps 4400–4500 is not final evidence. [Task 1]
- Do not claim universal physical or generation improvement: foot-skate direction differed, the matrix excludes later 1024 training, and checkpoint binaries/videos were not independently reopened (artifact closure WARN). [Task 1]
- The export hook applies only after a new code package is deployed and can be bypassed by forced termination/node loss; verify the manifest after recovery. [Task 2]

# Task Group: Musics2Dance committed-trajectory GAN/ES efficiency audit
scope: Diagnose slow committed-trajectory post-training without changing a live Job, frozen experiment budget, or scientific method.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=use cost findings as a design audit, not as a speedup/quality claim; remeasure target hardware before optimization.

## Task 1: Audit slow GAN and energy-score arms against code and mature methods, partial

### rollout_summary_files

- rollout_summaries/2026-09-19T08-25-39-vb59-kubernetes_gpu_quota_and_committed_trajectory_cost_audit.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T16-58-01-01a0b8c5-6493-7560-9a92-78a194682cf3_01a0c32f-be1c-71f1-bdf7-6d94456d54fa.jsonl, updated_at=2026-09-24T06:27:16+00:00, thread_id=01a0b8c5-6493-7560-9a92-78a194682cf3, code/data reconstruction and literature comparison; no Job/budget change)

### keywords

- train_g1_commit_trajectory.py, objective_batch, CommittedRollout.step, burn-in, Self-Forcing, DMD2, EAR, DPPO, gradient-truncation, COMMITTED_TRAJECTORY_TRAINING_COST_AUDIT_20260921.md

## User preferences

- when comparing with mature papers/code while the task is running -> distinguish verified engineering bottlenecks from scientific redesigns; do not alter the active Job or frozen budget without approval. [Task 1]
- preserve 183 training/18 test tracks and 6250 additional updates per arm; do not reduce the split or update budget merely because GAN/ES is slower. [Task 1]

## Reusable knowledge

- Exact CPU reconstruction of 350 updates/16,800 source groups found burn-in 0/16/32/64 counts `7603/3329/3140/2728`, mean useful 19.5438, but every batch maxed at 64. `objective_batch` loops to batch `max(row["burnin"])`, computes completed-row proposals, then masks/discards them: nominal discarded particle-plan work was 69.46%, 46.80% including startup/scored generation. This is work-count evidence, not measured wall-time. [Task 1]
- `CommittedRollout.step` has 10 residual denoising steps per 8-frame commit, long scored backward chains, and activation checkpointing. GAN does per-group critic/generator work; ES distance work is already batched, so ES is mainly generation-bound. First evaluate compact/grouped burn-in work and batched GAN critic operations; only then separately assess bounded-gradient/Self-Forcing-style training. [Task 1]
- Self Forcing has few-step diffusion, random exit, no-gradient earlier steps, and detached previous-frame cache gradients; DMD2 uses selected generator paths plus score/critic updates; EAR has a two-sample direct stochastic Energy Score; DPPO separates no-gradient rollout collection. These are references, not drop-in equivalent objectives. [Task 1]

## Failures and how to do differently

- Do not equate 46.80% nominal forward-work reduction with a wall-clock speedup: compaction can lower GPU utilization and alter RNG/resume behavior. Full target GPU telemetry/phase timings were not captured. [Task 1]
- Do not simply switch 10 denoising steps to 4, cache trajectories for repeated optimization, or reduce 6250 updates: each changes the method or confounds a matched comparison. [Task 1]

# Task Group: /home/wangyukun/ubt_isaac_sim_ws disk cleanup with retention evidence
scope: Safely reclaim workspace space while protecting current models, raw acquisition data, evaluation evidence, and active services.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws; reuse_rule=deletion paths and free-space figures are historical; reuse audit/retention rules only.

## Task 1: Delete user-approved raw lower-shelf HDF5, completed

### rollout_summary_files

- rollout_summaries/2026-09-17T02-02-53-Tj4q-disk_cleanup_0logs_raw_dataset.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T10-02-53-01a0ad1a-3f6d-71b1-b1b4-72783845ad96.jsonl, updated_at=2026-09-17T04:04:34+00:00, thread_id=01a0ad1a-3f6d-71b1-b1b4-72783845ad96, freed about 263GiB)

### keywords

- HandlingBox_lower_hold_level_500_20260825, dataset.hdf5, RAW_DATASET_REMOVED, CONVERTED_TRAINING_DATA_PRESENT, hard links, lsof, 12317

## Task 2: Remove obsolete cluster-backed GR00T/LingBot artifacts, caches, and archives, completed

### rollout_summary_files

- rollout_summaries/2026-09-19T09-23-57-mf0T-workspace_cleanup_zzy_git_history_and_cluster_backed_artifac.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/19/rollout-2026-09-19T17-24-49-01a0b8fa-c664-7df2-b061-3b1b31a32643_01a0b8fb-8fa8-7723-bbb1-e491d2e1b1ce.jsonl, updated_at=2026-09-26T18:16:14+00:00, thread_id=01a0b8fa-c664-7df2-b061-3b1b31a32643, audited artifact/cache/archive cleanup; final observed free space ~92GB)

### keywords

- uploaded-to-cluster, Git-history, Docker, hardlinks, inode/link-count, r01-old-new-lower-37mix-60k, cleanup-records, df

## Task 3: Remove explicitly authorized zzy Git history while preserving working trees, completed

### rollout_summary_files

- rollout_summaries/2026-09-19T09-23-57-mf0T-workspace_cleanup_zzy_git_history_and_cluster_backed_artifac.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/19/rollout-2026-09-19T17-24-49-01a0b8fa-c664-7df2-b061-3b1b31a32643_01a0b8fb-8fa8-7723-bbb1-e491d2e1b1ce.jsonl, updated_at=2026-09-26T18:16:14+00:00, thread_id=01a0b8fa-c664-7df2-b061-3b1b31a32643, 17 exact `.git` directories removed after authorization and verification)

### keywords

- zzy, /home/zhongzhengyang/lingbot-vla-v2/.git, syntheticdatageneration/.git, git-history, heads-status, reachability, 209583710208, 194.4 GiB

## User preferences

- for irreplaceable raw research data, the user said “确认删除” -> obtain explicit confirmation for the exact target first. [Task 1]
- the user clarified “只要是上传过集群的都可以当作有” -> documented prior cluster upload/assembly is enough for local deletion, but preserve newest/current model and evaluation by default. [Task 2]
- when the user said zzy had left and “git历史没有用了吧，把大文件删掉应该也没问题” -> only with explicit authorization, remove exact departed-owner `.git` metadata while preserving the working files and recording the irreversible loss of local history. [Task 3]
- distinguish converted training copies from original raw acquisition data; the user challenged treating cluster conversion as a raw-data backup. [Task 1][Task 2]

## Reusable knowledge

- Before deleting, inspect path, project references, open handles, inode/link accounting, retention evidence, and `df -h`; after, verify retained current model/base/evaluation/service and actual free space. [Task 1][Task 2]
- Docker tag removal may retain build layers; after active-container/shared-layer checks use `docker builder prune -f`, then verify `df -h`. [Task 2]
- Five GR00T model copies (62,941,224,749 bytes), verified old archive parts, a temporary M2D runtime, and a published image archive were removed while retaining current model, working files, logs/configs/analyses/manifests, and active artifacts; use `0.logs/cleanup/` audits. Inode/link counts are mandatory before recovery estimates. [Task 2]
- zzy's 17 `.git` directories contained historical multi-GB checkpoint blobs; unreachable objects were only about 170 KB, so ordinary pruning would not materially help. Before full metadata removal, snapshot heads/status, confirm no active processes/container mounts, delete only exact `.git` paths, then verify working-tree paths. Logical metadata removed was `209583710208` bytes and observed free-space increase about 194.4 GiB. [Task 3]

## Failures and how to do differently

- Directory sums and Docker “reclaimable” can overstate actual safe recovery. Converted-data upload evidence never proves raw HDF5 backup. [Task 1][Task 2]
- Validate actual closure JSON nesting before destructive execution; `download_identities_verified` was under `closure['checks']`, not the top level. Similar-sized directories are not duplicates: 15 matched large M2D paths had zero byte-identical files and were retained. Cross-user `/tmp/ulab-latest.tar.gz` failed with `Operation not permitted`; do not force removal. [Task 2]
- Do not delete individual large Git packfiles just because they contain old-looking weights: determine reachability and whether the goal is pruning or full metadata removal first. [Task 3]

# Task Group: Musics2Dance research-to-GitHub handoff workflow
scope: Publish ready code/documents/evidence for Web analysis while keeping repository synchronization independent from issue/PR discussion.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws and /home/wangyukun/research-loop-workflow; reuse_rule=recheck current workflow files and skill source before edits; use the concise policy rather than adding layered rules.

## Task 1: Separate repository synchronization from issue/PR discussion, completed

### rollout_summary_files

- rollout_summaries/2026-09-18T07-43-05-YZAg-research_workflow_preflight_and_github_handoff_alignment.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T15-43-05-01a0b378-0fdd-7bb1-8c60-f051ce14156c.jsonl, updated_at=2026-09-24T15:39:53+00:00, thread_id=01a0b378-0fdd-7bb1-8c60-f051ce14156c, workflow and skill validation passed)

### keywords

- github-research-handoff, repository-sync, issue, PR, Web-analysis, WORKFLOW.md, ASYNC_RESEARCH_WORKFLOW.md, run_github_research.py, quick_validate.py

## User preferences

- when the assistant coupled artifact delivery with issue/PR updates, the user corrected: “有阶段性结果再更新issuespr，很多时候是把产物证据更新repo，web可以读然后分析就可以了” -> sync useful code/evidence to the repository independently; reserve discussion updates for stage results or decisions. [Task 1]
- when the user said “不要规则越堆越多” -> use one short governing principle, not layered repeated workflow conditions. [Task 1]

## Reusable knowledge

- Final principle: “产物准备好就同步仓库，供 Web 读取；issue/PR 只在有阶段性结果或需要决策时更新。” Branch pushes can make files available to Web without requiring a comment or decision. [Task 1]
- Canonical M2D workflow files are `Musics2Dance/docs/research/WORKFLOW.md`, `Musics2Dance/docs/research/ASYNC_RESEARCH_WORKFLOW.md`, and `Musics2Dance/scripts/run_github_research.py`. The skill source is `/home/wangyukun/research-loop-workflow/packs/core/skills/github-research-handoff/`; installed copy is `/home/wangyukun/.codex/skills/github-research-handoff/`. [Task 1]
- Validate edits with `python3 -m unittest tests.test_run_github_research -q`, `quick_validate.py .../github-research-handoff`, and `git diff --check`. [Task 1]

## Failures and how to do differently

- Do not make a GitHub result package/comment a prerequisite for pushing code and evidence. Repository publication and discussion updates are separate operations. [Task 1]

# Task Group: Musics2Dance 38D amplitude audit and GitHub/Web evidence handoff
scope: Diagnose latest 38D-versus-34D motion amplitude and publish reproducible non-video evidence for owner/Web decision.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=recheck ledger, accepted representation, branch, and remote decision state.

## Task 1: Diagnose latest 38D amplitude versus 34D, completed

### rollout_summary_files

- rollout_summaries/2026-09-18T06-09-08-mIeS-38d_amplitude_diagnosis_github_evidence_handoff.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T14-09-08-01a0b322-0e7f-7213-b849-6b547c81ba6a.jsonl, updated_at=2026-09-18T08:23:58+00:00, thread_id=01a0b322-0e7f-7213-b849-6b547c81ba6a, 324-clip audit separated codec capacity from autonomous generation)

### keywords

- 38D, 34D, g1_yaw_anchor_abs_6d, B71, AM-FHC, AJ-FHC, amplitude_audit_20260918, 036, q0 repetition

## Task 2: Publish evidence and request Web decision, completed

### rollout_summary_files

- rollout_summaries/2026-09-18T06-09-08-mIeS-38d_amplitude_diagnosis_github_evidence_handoff.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T14-09-08-01a0b322-0e7f-7213-b849-6b547c81ba6a.jsonl, updated_at=2026-09-18T08:23:58+00:00, thread_id=01a0b322-0e7f-7213-b849-6b547c81ba6a, verified non-video evidence release)

### keywords

- PR #54, Issue #53, amplitude-audit-20260918, assets=13, all_digests_verified, no_video_assets, researchos:waiting-web

## User preferences

- when the user said “最新的 38d 主线” and asked “是38d的问题还是训练出了问题” -> separately test representation/codec reconstruction, generator, music condition, history, and rendering; do not infer from aggregate scores. [Task 1]
- “实验 证据要传上” but “视频不需要，其他的日志啥的可以” -> publish measurements, logs, scripts, motion traces, static figures, and reports, but omit video. [Task 1][Task 2]
- provide an explicit pending decision; do not automatically launch training or replace the mainline. [Task 2]

## Reusable knowledge

- 38D codec preserved large motion (range/speed 97.3%/97.2% versus 34D 96.6%/90.6%); low amplitude is concentrated in autonomous generation, not a proven codec-capacity/rendering failure. [Task 1]
- Root-local wrist/ankle under-activity was stable (AM−34D -6.3pp, AJ−34D -5.3pp); 036 is repeated failure while 063/098 prevent a universal-collapse claim. Current interpretation is conservative autonomous generation/long autoregressive history, not uniquely dimension/loss/steps. [Task 1]
- Branch `codex/38d-amplitude-audit-20260918`, PR #54, Issue #53, release `amplitude-audit-20260918`: 13 digest-verified assets, no videos, no training launched. [Task 2]

## Failures and how to do differently

- GitHub large assets timed out through proxy -> verify proxy, use direct API if needed, and check every asset size/digest. Do not present true-state injection (about 5x boundary velocity jump) or no-music as a repair. [Task 1][Task 2]

# Task Group: Musics2Dance token-causal codec and full-song MRT2 generator readiness
scope: Decide the D+C codec route and validate its full-song MRT2 cache/generator preflight without conflating operational readiness with scientific acceptance.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=checkpoint/cache details are run-specific; preserve comparison and validation boundaries.

## Task 1: Decide whether to continue token-causal codec route, partial with stop recommendation

### rollout_summary_files

- rollout_summaries/2026-09-17T09-10-59-kIEa-token_causal_codec_route_decision.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T13-07-39-01a0aea2-2d88-7ad1-93f5-dabd2b7354da_01a0b2e9-c315-7110-a086-05d720e45b8a.jsonl, updated_at=2026-09-18T05:21:06+00:00, thread_id=01a0aea2-2d88-7ad1-93f5-dabd2b7354da, current configuration should stop expanding)

### keywords

- token-causal, D+C, FineDance, B71, causal Conv1D, 0.008143, 7.05x, oracle-latent, wins {'new_1234': 0, 'new_2345': 0, 'new_3456': 0}

## Task 2: Build and verify full-song MRT2 cache, completed

### rollout_summary_files

- rollout_summaries/2026-09-18T02-53-12-6KD9-m2d_modelscope_fullsong_mrt2_cache_sync.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T10-53-12-01a0b26e-aa7e-7512-9bdc-a5d06f11a5e3.jsonl, updated_at=2026-09-18T08:57:37+00:00, thread_id=01a0b26e-aa7e-7512-9bdc-a5d06f11a5e3, cache and generator preflight passed; formal training not launched)

### keywords

- ModelScope, MRT2, FutureMusicStore, token_causal_fullsong, zstd -t, paired motion length, 95411, 6399, generator_train_resume

## User preferences

- when the user asked “深度分析，给我个结果要不要继续这条路线” -> provide evidence, causal limits, and clear investment recommendation, not only metrics. [Task 1]
- when asked to upload and download simultaneously -> monitor inventories in parallel, transfer only missing/changed files, and leave long transfers backgrounded. [Task 2]
- distinguish downloaded asset, readable cache, local preflight, formal training, and scientific acceptance; use direct Chinese counts/blocker/next-step updates. [Task 2]

## Reusable knowledge

- Old held-out MSE `0.008143` beat new 100k seed MSE `0.05594–0.05931` (about 7.05x), every new seed lost all 18 tracks, and 50k→100k gain was only 0.9–5.6%. Streaming passed (`4.53e-6` full/incremental), but training reconstruction was about 7.22 degrees. [Task 1]
- Oracle latent gains about 54–64% diagnose encoder/objective information allocation only. Stop current-config expansion/downstream generator training; allow at most one capped reconstruction-first repair study with precommitted exit criteria. [Task 1]
- Cache path is `modelscope/repro/foredance-mainline-20260912/generator/condition_caches/token_causal_fullsong/`: 201 tracks, 95,411 train/6,399 test cutoffs, eight archives passed `zstd -t`, reader passed 201 tracks/603 probes. Use paired length `min(raw_motion_length, floor(audio_frames*30/sample_rate)+15)`; never pad/fabricate. [Task 2]
- Seed-1234 generator preflight passed finite updates and exact resume error 0.0; this is execution readiness only. [Task 2]

## Failures and how to do differently

- Do not call old/new an architecture ablation: budgets, windows, initialization, anchors, and boundary conditioning differ. Do not use lower jerk/decreasing loss as quality proof. [Task 1]
- Before recomputation, ask for other private full-song sources. Audio/action mismatch causes EOF; `.venv311` is under `Musics2Dance`, and unavailable `pytest` cannot be reported as passing. [Task 2]

# Task Group: /home/wangyukun/ubt_isaac_sim_ws GR00T N1.7 lower-shelf RTC/physics diagnosis, success-first evaluation, and evidence archival
scope: Diagnose relative-action/RTC and physical grasp/jitter failures, evaluate bounded repairs with strict completion metrics, and archive requested evidence without turning replay evidence into an autonomous-improvement claim.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws; reuse_rule=scene/checkpoint/service-specific; revalidate live service, physics, metrics, and seeds.

## Task 1: Diagnose and evaluate lower-shelf jitter, partial

### rollout_summary_files

- rollout_summaries/2026-09-17T08-53-19-VgaT-lower_eval_root_cause_and_github_evidence_archive.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T16-53-19-01a0ae92-039d-74d0-8c08-7c3a5f0d6acb.jsonl, updated_at=2026-09-24T05:57:21+00:00, thread_id=01a0ae92-039d-74d0-8c08-7c3a5f0d6acb, relative-action/RTC defect, qualified 7/40 result, and main-branch evidence archive)

### keywords

- RTC, relative-actions, collated_inputs["inputs"]["action"], action horizon 32, execute/replan 16, overlap 16, target drift, jitter, n17_v3_rtc_reference.py

## Task 2: Run success-first 8/8 lower 40-episode evaluation, partial

### rollout_summary_files

- rollout_summaries/2026-09-17T08-53-19-VgaT-lower_eval_root_cause_and_github_evidence_archive.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T16-53-19-01a0ae92-039d-74d0-8c08-7c3a5f0d6acb.jsonl, updated_at=2026-09-24T05:57:21+00:00, thread_id=01a0ae92-039d-74d0-8c08-7c3a5f0d6acb, 7/40 actual lower placements; stability and model-only attribution unproven)

### keywords

- same_shelf_lower_level, inference_steps=8, rtc_frozen_steps=8, 7/40, pick 39/40, legacy final 8/40, 12 cm tolerance, H.264, 2026080501

## Task 3: Archive reports, source, and failure evidence to GitHub main, completed

### rollout_summary_files

- rollout_summaries/2026-09-17T08-53-19-VgaT-lower_eval_root_cause_and_github_evidence_archive.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T16-53-19-01a0ae92-039d-74d0-8c08-7c3a5f0d6acb.jsonl, updated_at=2026-09-24T05:57:21+00:00, thread_id=01a0ae92-039d-74d0-8c08-7c3a5f0d6acb, main-branch reports/source/video evidence archived with local receipt)

### keywords

- lbtwyk/utars-isaac-vla-pipeline, main, 6117badd4b7e8edbac2238a5807dcda7444771bd, 1456/1456, push_status.json, HTTP 408, TLS/EOF, 64 MiB, hash verification

## Task 4: Focused physics/grasp repair verification, partial

### rollout_summary_files

- rollout_summaries/2026-09-22T07-16-07-eRP9-lower_shelf_jitter_pd_grasp_focused_verification.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/22/rollout-2026-09-22T15-16-07-01a0c7f8-cf32-78b1-a187-322171d391d7.jsonl, updated_at=2026-09-24T06:27:09+00:00, thread_id=01a0c7f8-cf32-78b1-a187-322171d391d7, repaired RTC/execution mismatches; replay jitter improved but autonomous placement did not)

### keywords

- GR00T-N1.7, grasp, damping, contact-force, tilt, drop, N17_V3_GRASP_CONSTRAINT, fixed-scene, retreat_audit.json, initial_target_obj_pose is None

## Task 5: Audit tracking error and bound controller scope, partial

### rollout_summary_files

- rollout_summaries/2026-09-24T06-02-32-TDx4-lower_shelf_tracking_and_training_audit.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T14-02-32-01a0d202-2a1a-73a3-a994-2f1e636edbe6.jsonl, updated_at=2026-09-24T09:25:32+00:00, thread_id=01a0d202-2a1a-73a3-a994-2f1e636edbe6, read-only diagnosis; no controller/PD/training change)

### keywords

- N1.7, lower-shelf, tracking-error, N17_V3_TARGET_LIMIT_MODE=measured, max_joint_step_rad=0.12, raw requested target, final applied target, physics_tick, grasp-feedback

## Task 6: Audit lower data and training-integrity contract, partial

### rollout_summary_files

- rollout_summaries/2026-09-24T06-02-32-TDx4-lower_shelf_tracking_and_training_audit.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T14-02-32-01a0d202-2a1a-73a3-a994-2f1e636edbe6.jsonl, updated_at=2026-09-24T09:25:32+00:00, thread_id=01a0d202-2a1a-73a3-a994-2f1e636edbe6, integrity verdict FAIL for intended top-four language-layer contract; causal retraining untested)

### keywords

- tune_top_llm_layers, qwen3_backbone.py, launch_utars_v3_finetune.py, 176 language-layer tensors, 537 action-head tensors, 500 demonstrations, teacher-forced, closure.json

## User preferences

- “根因修复” rather than cosmetic smoothing -> inspect action semantics, reference frames, timing, and execution traces before tuning. [Task 1]
- report complete evidence: counts, paths, codec checks, and per-failure caveats, not just a rate. [Task 1]
- when the user said “就放到主分支，证据也放到repo就行不要发布” and “readme把这次作为主结果” -> use main-branch evidence, not a Release, and lead the README with 7/40. [Task 3]
- when the user said “现在不用发散性尝试，做确定性优化验证，快点得到结果” and later “不再增加方案” -> freeze the selected intervention, run only predeclared matched controls, and wait for owner approval before extra seeds/variants. [Task 4]
- report success-rate evidence, not cosmetic smoothing: holding the box while retreating, tilted, or unreleased is failure. [Task 4]
- when fixing physical jitter, the user said “不要靠调整pd” -> retain original PD and separately diagnose raw inference target, execution limiting, physical tracking, contact/support, and drop timing. [Task 5]
- when the user chose “允许额外接触反馈参与控制，但保持原PD” and “1a，2a” -> feedback is downstream bounded bilateral grasp preservation; release stays policy-initiated and feedback may only delay it until support is reliable, with no silent base-motion or shelf-entry expansion. [Task 5]
- when requesting a root-cause route, preserve negative evidence and distinguish verified training defects from hypotheses; do not launch retraining or controller variants silently. [Task 6]

## Reusable knowledge

- N1.7 relative arm actions decode against the current reference state. RTC continuation must transform the previous absolute chunk into that new reference, preserve physically executed prefix, and align replanning to inference latency; old-reference reuse creates jitter/target drift. Previous RTC action data belongs under `collated_inputs["inputs"]["action"]`; a top-level `action` passed to `model.get_action()` is an API error. [Task 1]
- Canonical evaluation `0.logs/n17_v3_batch_eval/20260918_success_first_8f8_lower_40ep/`: 40 unique seeds, 7/40 actual completions (17.5%), pickup 39/40, legacy final 8/40 with one outside the 12 cm tolerance; 120 H.264 videos decoded and no client/expired-request errors. [Task 2]
- Main README leads with qualified 7/40. The sanitized main-branch evidence export completed `87/87` batches and `1456/1456` files with hash verification, exit code 0, final reported commit `6117badd4b7e8edbac2238a5807dcda7444771bd`; it excludes credentials, raw datasets, model weights, proprietary assets, internal infrastructure, and company Git history. A later API tree re-fetch hit TLS/EOF, so distinguish upload receipts/local inventory from a fresh online fetch. [Task 3]
- Candidate C (grasp/entry feedback plus 3x arm damping) improved a fixed replay but is privileged contact/geometry feedback, not VLA-only evidence: common loaded 2.5–15 s roughness fell 49.45%, box angular-speed p95 27.16%, tilt p95 8.82°→6.02°, while 15–30 s tilt p95 worsened 4.02°→7.42°. Keep `N17_V3_GRASP_CONSTRAINT=0` for native/default autonomous evaluation. [Task 4]
- Fresh-policy matched cases were candidate 0/2 versus native 0/2: one held the box but retreated about 7.75 m, never reached/released, and ended ~50.29° tilted; the other dropped at 55.30 s after retreat. Preserve 14 complete 60 s trials separately from two pre-episode initialization failures; 42 originals plus 3 comparison videos decoded. [Task 4]
- Tracking audit matched 16,756 action endpoints across 10 runs. Always separate raw requested target vs pre-step state, requested vs final applied target, and previous applied vs current measured state; the old analysis mainly measured only the third. In failed seed 502, right-wrist raw request/state p95 was ~25.75° and ~18.87° was removed by limiting, while near-drop wrist errors were only ~0.03–0.18° medians despite bilateral contact. [Task 5]
- `N17_V3_TARGET_LIMIT_MODE=measured` limits target steps to 0.12 rad around measured state; reaction effort is a contact/constraint reaction measurement, not commanded torque or saturation. Canonical artifacts are `0.logs/n17_v3_tracking_audit_20260924/audit.json` and `REPORT.md`. [Task 5]
- 500 demos/771,289 decoded frames had no corrupt video, missing frames, or nonfinite numeric values, but the intended top-four language-layer tuning was not forwarded: retained checkpoint `tune_top_llm_layers: 0`, 176 language tensors unchanged, 537 action-head tensors changed, and recording-loader reproduction confirmed the omission. Dataset coverage is narrow and demonstrations used tilt feedback absent from VLA inputs. [Task 6]
- All 500 demos have a 20.39–27.45° wrist target reset at descent while physical wrist movement was ~0.00457° median: target handoff, not physical jitter. Training-seen offline midpoint RMSE ~0.459° and cross-descent ~3.158° are diagnostics, not autonomous-success evidence. [Task 6]

## Failures and how to do differently

- Do not call residual failures model-only or 8/8 reliable: seed `2026080501` was non-deterministic; `2026080513` had valid pose plus a drop flag, while `2026080515` lost the object without one; full physics traces were absent. Do not report pickup as task success. [Task 1][Task 2]
- A 400 MiB upload batch hit HTTP 408/TLS failure; resume from a confirmed remote commit in 64 MiB batches and never re-upload confirmed batches. A draft Release was deleted after scope correction: never create one when main is requested. Rewrite `WORKSPACE/...` Markdown image links to repository-relative paths before external publication. [Task 3]
- Do not infer success from delayed drop or lower joint roughness; require target pose, release, no-drop, and tilt/quality gates together. The delayed 3 cm lift/six-sample median latch failed full replay at 50.73 s and must not be retained. [Task 4]
- Startup errors `initial_target_obj_pose is None` then `target_obj is None` arose from lazy pose fields. Read the settled USD box prim pose through the existing pose helper and keep pre-action initialization failures outside episode success statistics. Do not promote damping, grasp-span constraints, wrist-force increases, or base slew changes from replay-only evidence. [Task 4]
- Do not call `previous_target-current` “model accuracy”: it can hide raw clipping. Correct cumulative `physics_tick` offsets per episode before joins, and pair small joint error with contact, support, box attitude, and drop timing. [Task 5]
- The missing top-four training flag is a verified contract defect, not proof it explains all drops: training logs/trainer state and a causal retraining comparison were unavailable. Never use oracle future-action continuation or training-seen offline probes as deployment/generalization evidence. [Task 6]

# Task Group: Musics2Dance workspace bootstrap, private artifacts, and historical Isambard context
scope: Create/secure M2D checkout, verify private ModelScope assets, and use historical Isambard notes without treating them as live state.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws; reuse_rule=current research state comes from checkout AGENTS.md, ledger, contract, and live artifacts.

## Task 1: Bootstrap owner-only M2D workspace and verify ModelScope assets, partial/success

### rollout_summary_files

- rollout_summaries/2026-09-17T02-11-24-Sg0X-m2d_workspace_modelscope_download_verification.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/17/rollout-2026-09-17T10-11-24-01a0ad22-0a18-73f0-a179-639d17ab826b.jsonl, updated_at=2026-09-17T13:33:48+00:00, thread_id=01a0ad22-0a18-73f0-a179-639d17ab826b, checkout/ACL and source-current artifact integrity verified; training configuration incomplete)

### keywords

- m2d-ws, prior-dev, GIT_LFS_SKIP_SMUDGE, m2d-train, ModelScope, 5725 blobs, hash_bad=0, inference_verified=false, Isambard

## User preferences

- “这个m2d的权限只能给我自己开” and requested `m2d-train` naming -> restrict access; claim process naming only after scheduler/`nvidia-smi` verification. [Task 1]
- “拉下来更新本地记忆” means import specified backup locally, not reverse-upload current memory. [Task 1]

## Reusable knowledge

- `prior-dev` shallow clone with `GIT_LFS_SKIP_SMUDGE=1` avoids unneeded LFS; confirm no residual git/git-lfs before resolving `.git/index.lock`. ModelScope needs refreshed manifest, retries, per-file size/SHA256, and `zstd -t`; source-current integrity does not prove training readiness. [Task 1]
- The canonical research-workflow source is `lbtwyk/research-loop-workflow`; local `/home/wangyukun/research-loop-workflow` matched `origin/main` commit `82996a3` on 2026-09-17. Keep machine-specific `~/.codex/config.toml` and `~/.codex/AGENTS.md` separate from that public source. [ad-hoc note]
- Start M2D research from `m2d-ws/AGENTS.md`, project `AGENTS.md`, ledger, frozen contract, and live artifacts. Isambard material under `/home/wangyukun/.codex/memory-imports/isambard-20260908/` and old `/lus/lfs1aip2/...` paths are historical only. [Task 1] [ad-hoc note]

## Failures and how to do differently

- Do not describe code/download completion as training configured or scientific acceptance. Recheck active code/ledger/issues before acting on archived research direction. [Task 1] [ad-hoc note]

# Task Group: /home/wangyukun/ubt_isaac_sim_ws H200 submission and fixed-scene closed-loop comparison
scope: Use current H200 Job docs and run controlled arm-only versus full-policy batches with video closure.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws; reuse_rule=recheck current H200 state and server port; batch values are checkpoint-specific.

## Task 1: Reconcile H200 smoke-job submission, completed

### rollout_summary_files

- rollout_summaries/2026-08-04T05-25-18-12qz-h200_doc_reconciliation_and_100ep_closed_loop_comparison.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/08/04/rollout-2026-08-04T13-25-18-019fcb3b-c1f8-7331-a079-a169b3af742f.jsonl, updated_at=2026-08-12T08:50:00+00:00, thread_id=019fcb3b-c1f8-7331-a079-a169b3af742f, latest-doc smoke path validated)

### keywords

- docs/h200-current-state.yaml, H200_SIMPLE_WORKFLOW.md, validate_h200_smoke_job.py, H200_SMOKE_JOB_OK, print_kubesphere_apply.sh

## Task 2: Run 100-episode locked-arms versus full-policy comparison, completed

### rollout_summary_files

- rollout_summaries/2026-08-04T05-25-18-12qz-h200_doc_reconciliation_and_100ep_closed_loop_comparison.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/08/04/rollout-2026-08-04T13-25-18-019fcb3b-c1f8-7331-a079-a169b3af742f.jsonl, updated_at=2026-08-12T08:50:00+00:00, thread_id=019fcb3b-c1f8-7331-a079-a169b3af742f, same-seed comparison and H.264 closure completed)

### keywords

- locked_arms, full_policy, 12317, UNIFIED_MP4_H264 total=200 bad=0, comparison.json, episode_000_dual_view.mp4

## User preferences

- “你再看一下最新更新过的h200文档，是不是流程你想错了” -> consult current docs/state before advice. “给我详细怎么做，一步步教我” -> provide copy/paste operational steps. [Task 1]
- Short “现在呢” status prompts need live counts, artifact path, and blocker; video-location answers need root/condition directories/counts. [Task 2]

## Reusable knowledge

- Read `docs/h200-current-state.yaml`, then `docs/H200_SIMPLE_WORKFLOW.md`; validate smoke YAML and use `print_kubesphere_apply.sh` heredoc because 5090 and KubeSphere do not share filesystem. [Task 1]
- Preflight server port 12317 before Isaac Sim. Keep serial batches if unchanged; parallel start previously hit Vulkan allocation failure. Locked arms 86% relaxed final versus full policy 34%; finalize only after settled counts, zero `.tmp.mp4`, and `UNIFIED_MP4_H264 total=200 bad=0`. [Task 2]

## Failures and how to do differently

- Do not tell the user to place YAML in a shared KubeSphere directory. A stale server port caused first batch failure; validate service before simulation. [Task 1][Task 2]

# Task Group: /home/wangyukun/ubt_isaac_sim_ws SDG recovery and GR00T 1,000-episode cluster diagnosis
scope: Validate bounded SDG same-task recovery and diagnose N1.7 training Jobs that show Running without a Pod.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws; reuse_rule=verify current recovery code, acceptance thresholds, namespace, and quota before applying.

## Task 1: Audit same-task SDG recovery acceptance, completed/partial

### rollout_summary_files

- rollout_summaries/2026-08-06T07-39-21-pkWy-utars_sdg_autonomous_recovery_audit_and_same_shelf_grasp_qua.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/08/06/rollout-2026-08-06T15-39-21-019fd603-3375-7193-8c3d-85803452d066.jsonl, updated_at=2026-08-13T03:15:04+00:00, thread_id=019fd603-3375-7193-8c3d-85803452d066, bounded recovery audit and acceptance record)

### keywords

- RecoverySupervisor, natural_execution_correction, same_shelf_grasp_quality_recovery, command_bias_m, HDF5 v3, H.264

## Task 2: Design 1,000-episode Any-GPU route and diagnose quota block, partial

### rollout_summary_files

- rollout_summaries/2026-08-10T09-10-01-Y3aK-utars_groot_n17_single_shelf_1000_anygpu_quota_block.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/08/10/rollout-2026-08-10T17-10-01-019feaef-a589-7830-850f-a52951e18786.jsonl, updated_at=2026-08-12T03:06:35+00:00, thread_id=019feaef-a589-7830-850f-a52951e18786, contract validated but training never started)

### keywords

- 1000条全部用上, Any-GPU, no tactile, ogi-llm, ogi-pub, Running 0/1, FailedCreate, gpu-quota

- Related skill: skills/kubernetes-gpu-quota-diagnosis/SKILL.md

## User preferences

- when the user asked for “自动数采里面的算法自动纠错机制” -> establish in-task correction, not merely reset/retry; preserve corrected failures and reject unsafe/partial recordings. [Task 1]
- “1000条全部用上”, task-level language, and no tactile are contract boundaries. When the user said “算了先不用pub了”, stay in the current namespace with read-only diagnostics first. [Task 2]

## Reusable knowledge

- Recovery is state-aware bounded controller: detect -> stabilize -> replan -> execute -> verify -> continue. It uses stage/contact/support/tilt/force/speed thresholds; inspect `HandlingMultiBoxScenarioShelfAutoCollect.py` and `recovery_supervisor.py`. [Task 1]
- A `Running 0/1` Job may have no Pod/no steps. `kubectl describe job ... -n ogi-llm` Events/failed-create count revealed GPU quota `used 9, limit 9`; 72-hour deadline continues while blocked. [Task 2]

## Failures and how to do differently

- Do not call recovery a general self-estimating algorithm; inspect observation fields, not final exception text. Do not query labels/logs repeatedly when no Pod exists; inspect Job events/quota. [Task 1][Task 2]
- Do not move to `ogi-pub` until PVC/storage ownership and create permission are proven. [Task 2]

# Task Group: /home/wangyukun/ubt_isaac_sim_ws LingBot-VLA 2.0 benchmark pipeline
scope: Build and preflight mixed real/sim UTars LingBot training, evaluation, and serving.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws; reuse_rule=dataset roots/counts and patches are checkout-specific; revalidate contract before training.

## Task 1: Build and preflight LingBot-VLA 2.0 pipeline, completed

### rollout_summary_files

- rollout_summaries/2026-07-07T07-29-32-jMPA-utars_lingbot_vla2_benchmark_ready.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/07/07/rollout-2026-07-07T15-29-32-019f3b7b-6b62-7a90-ac3a-e36d61298c86.jsonl, updated_at=2026-07-12T19:23:20+00:00, thread_id=019f3b7b-6b62-7a90-ac3a-e36d61298c86, ready and preflight-validated)

### keywords

- lingbot-vla-v2, weighted 60/40, LeRobot v2.1, MODE=preflight, relative_joint_position, 16 active dimensions, 55D, 12325

## User preferences

- for UTars work, the user steered toward “can it run” / “what is ready” -> answer with concrete readiness and executable next path, not abstract design. [Task 1]

## Reusable knowledge

- Local datasets must use `root`; non-contiguous v2.1 episode indices need explicit `episodes` from `meta/episodes.jsonl`; use weighted virtual 60% real/40% sim instead of concatenation. Valid contract is 16 active/55D canonical, 50-step, `relative_joint_position`, no future image. [Task 1]

## Failures and how to do differently

- Passing local `train` as HF repo id fails. Mark joint actions `relative_type: joint` or quaternion-relative default can corrupt deltas. [Task 1]

# Task Group: Ubuntu x86_64 ToDesk package selection
scope: Select correct ToDesk Linux package after local distribution and CPU architecture check.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws; reuse_rule=rerun OS/architecture checks before installation.

## Task 1: Select ToDesk installation package, completed

### rollout_summary_files

- rollout_summaries/2026-09-18T07-55-36-ovtB-todesk_ubuntu_x86_64_version_selection.md (cwd=/home/wangyukun/ubt_isaac_sim_ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T15-55-36-01a0b383-87d0-7722-bce0-88c24dda6567.jsonl, updated_at=2026-09-18T07:55:57+00:00, thread_id=01a0b383-87d0-7722-bce0-88c24dda6567, correct package identified)

### keywords

- ToDesk, Ubuntu 22.04.5 LTS, x86_64, amd64, Debian/Ubuntu/Mint, .deb

## Reusable knowledge

- Observed host was Ubuntu 22.04.5 LTS x86_64; choose Linux Debian/Ubuntu/Mint x64 amd64 `.deb`, not ARM64/RPM. Verify with `uname -m; cat /etc/os-release`. [Task 1]

# Task Group: Musics2Dance C64 FD/OD and RF cluster ETA monitoring
scope: Report live C64 FD/OD and RF rollout progress from hot-storage evidence while separating training, evaluation, videos, reports, and authoritative scheduler state.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=job status, checkpoints, card capacity, and hot paths are live-state specific; preserve exact resume identity and inspect current statuses before action.

## Task 1: Check C64 FD/OD and RF rollout ETA, partial

### rollout_summary_files

- rollout_summaries/2026-09-23T05-34-30-SdDu-c64_fd_od_eta_monitoring.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T17-20-12-01a0ccc2-22bc-7850-807f-2d0911811644_01a0d2b7-2478-7cd1-964f-ca57a246a170.jsonl, updated_at=2026-09-25T09:28:12+00:00, thread_id=01a0ccc2-22bc-7850-807f-2d0911811644, live state partial; full pipeline incomplete)

### keywords

- C64, FD, OD, RF, ETA, read_m2d_hot_logs.py, queue.json, FileNotFoundError, results-records.tar.gz.partial, kubectl

## User preferences

- when the user said “check eta” and then “check” -> proactively inspect live records and give concise evidence-backed status/ETA without demanding detailed scope. [Task 1]
- ETA reports must separate training, evaluation, videos, and final report completion. [Task 1]

## Reusable knowledge

- At 2026-09-24 22:18 CST: OD codec was 100000/100000; OD TF 380/3125 at ~2.1 s/update; both FD RF arms 9375/9375; ordinary FD evaluation complete and strong evaluation running; OD RF had not started. Separate RF R1 was 6250/6250 and R2 3478/6250 with ~9.17 hours remaining. [Task 1]
- Read hot-storage JSON/status/metrics through `.venv311/bin/python scripts/read_m2d_hot_logs.py`, saving snapshots under `runs/c64_fd_od_20260924/`; parse queue state and recent rates. Authoritative pod/GPU allocation requires current KubeSphere `kubectl get pods`/`get jobs` output. [Task 1]
- All 24 music batches/calibration completed. Its later `FileNotFoundError` for `results-records.tar.gz.partial` occurred during export after task completion; downstream OD training continued, so do not rerun music by default. [Task 1]

## Failures and how to do differently

- Missing FTP artifacts (`550 No such file or directory`) are unavailable/not-yet-produced evidence, not failure. Do not call the pipeline complete from a finished training/evaluation portion; OD RF, remaining evaluations, comparisons, videos, and report were pending. [Task 1]
- Do not extrapolate unstarted downstream speeds or treat storage records as actual pod allocation. Investigate export races separately and retry after hot-storage lag. [Task 1]

# Task Group: Musics2Dance RF rollout-strength training and GAN/ES versus RF/CoF evidence audit
scope: Audit causal-codec comparison claims, then monitor matched Resampling Forcing rollout-strength arms on RTX5090 while preserving fair contract, safe memory scheduling, and downstream-closure boundaries.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=metrics, GPU allocation, disk capacity, and experiment status must be re-read; do not treat diagnostics or prior control videos as current-arm quality evidence.

## Task 1: Audit GAN/ES and prior RF/CoF evidence, partial

### rollout_summary_files

- rollout_summaries/2026-09-23T03-08-11-i5i7-causalcodec_rf_gan_es_score_audit_and_sequential_training.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T11-08-11-01a0cc3c-3082-7ad2-bedd-f0ad433169a7.jsonl, updated_at=2026-09-25T15:02:17+00:00, thread_id=01a0cc3c-3082-7ad2-bedd-f0ad433169a7, provenance-qualified prior-score audit; no new RF quality scores)

### keywords

- multirate1024_balanced, CoF, continuous RF, joint RF, GAN, ES, 0.102731, 0.105489, 0.097671, FIDk, FIDg, 27.8%, proxy, dance-quality

## Task 2: Check R1/R2 RF rollout-strength training, partial

### rollout_summary_files

- rollout_summaries/2026-09-23T03-08-11-i5i7-causalcodec_rf_gan_es_score_audit_and_sequential_training.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T11-08-11-01a0cc3c-3082-7ad2-bedd-f0ad433169a7.jsonl, updated_at=2026-09-25T15:02:17+00:00, thread_id=01a0cc3c-3082-7ad2-bedd-f0ad433169a7, R1 running; R2 intentionally queued because live VRAM was unsafe)

### keywords

- EXP-20260923-fd-rf-rollout-strength, rf_joint_shift1, rf_joint_free2, RTX5090, nvidia-smi, resource-observation.json, pipeline.log, free2 p90, 70/70, motion_key

## User preferences

- when the user asked “汇报全部分数，然后继续实验分析” -> report complete metric/window/condition coverage, label proxy, diagnostic, and formal evidence, then continue the authorized analysis. [Task 1]
- when choosing routes, assess maturity, novelty, first-principles fit, and engineering cost; do not assume ES is preferred. [Task 1]
- when the user says `check`, complete the approved operational loop instead of only reporting passive status; keep 48 groups/update, seed1234, 6250 updates, and unchanged data/model/loss/optimizer/deployment. [Task 2]

## Reusable knowledge

- Frozen system: `multirate1024_balanced`, seed1234, native38/30Hz, D512+C16, K64 D+C history, H4/C4 deployment, C NFE10, 8-frame commits. In the 6250-step RF/CoF comparison, music match was CoF `0.102731`, continuous RF `0.105489`, joint RF `0.097671`; joint RF had jerk `1355.35`, 14 severe rotations, FIDk `197.94`, FIDg `0.60624`, diversity `16.49`. One seed/18 songs with five audio overlaps establishes no global winner. [Task 1]
- Fixed/dynamic calibration reduced jerk about 11.6% versus old controls, but dynamic did not significantly beat fixed. Historical feedback reduced reliability-estimation MSE 27.8% on 13 audio-disjoint songs: a diagnostic result, not dance-quality improvement. Local third-update times (CoF ~4.46 s, GAN ~74.29 s, ES ~71.06 s) are non-isolated operational timings, not H100 or quality claims. [Task 1]
- R1 only changes continuous-history noise shift 0.6→1.0. R2 retains 0.6 and adds two short autonomous D+C free bursts, so call it hybrid RF/free-rollout, not plain RF. The admission diagnostic (`free2 p90=0.081343` vs limit `0.249751`) establishes boundary executability, not quality or D-error exposure. [Task 2]
- Live process memory overrides proof estimates: on 32,607 MiB, R1 used about 15,646 MiB plus 2,623 MiB other use, so concurrent full R1/R2 was unsafe. The persistent launcher must recheck R1 completion/failure after waits before launching R2. [Task 2]

## Failures and how to do differently

- Do not treat CPU gradient checks, reliability-predictor MSE, input interventions, finite updates, or training completion as proof of dance-quality gains or self-correction benefit. [Task 1]
- Proof-peak estimates overstated parallel capacity; always recheck live `nvidia-smi` after launch and serialize arms when reserve is insufficient. Recheck R1 completion/failure after each launcher wait before starting R2. [Task 2]
- A running trainer/checkpoint is not completion; metrics, music interventions, 70 videos, analysis/report, and owner acceptance remain separate. Treat pre-fix videos as superseded; 70/70 rerendered controls are prior evidence, not R1/R2 scores. Use each short case's saved `motion_key` and verify artifact identity before qualitative comparison. [Task 2]

# Task Group: Musics2Dance causal codec mixer monitoring, cluster MPS, and audio-safe video delivery
scope: Monitor independent causal-codec work, prove safe same-GPU MPS continuation, and make standard video outputs final-audio-only and self-describing.
applies_to: cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance; reuse_rule=cluster permissions, GPU telemetry, queue entries, and releases are time-specific; do not create duplicate workers or submit superseded packages.

## Task 1: Monitor causal mixer experiment and continue RF rollout with MPS, partial

### rollout_summary_files

- rollout_summaries/2026-09-23T07-15-04-6rfU-causalcodec_cluster_mps_monitoring_and_eta.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T15-15-04-01a0cd1e-3517-71a1-849f-acb45c91a9a6.jsonl, updated_at=2026-09-25T11:48:58+00:00, thread_id=01a0cd1e-3517-71a1-849f-acb45c91a9a6, mixer monitoring plus submitted/verified RF MPS continuation)

### keywords

- EXP-20260923-fd-codec-causal-mixer, joint_stable, conv_stable, attention_stable, EXP-20260923-fd-rf-rollout-strength, CUDA_MPS_PIPE_DIRECTORY, packing-proof.json, m2d-rf-rollout-strength-1h, node14

## Task 2: Publish audio-checked standard videos with a unified catalog, completed

### rollout_summary_files

- rollout_summaries/2026-09-23T09-33-43-ggCC-fd_od_monitoring_and_audio_checked_video_catalog.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/24/rollout-2026-09-24T13-50-05-01a0cd9d-2740-7fe3-b4b5-ae402b63242a_01a0d1f6-c48e-70a1-b7d3-055dd6aed119.jsonl, updated_at=2026-09-25T05:52:28+00:00, thread_id=01a0cd9d-2740-7fe3-b4b5-ae402b63242a, audio-safe catalog implemented and verified)

### keywords

- g1_video_catalog.py, silent.mp4, audio mux, public/index.html, CATALOG.md, catalog.csv, catalog.json, PR-57, tests.test_g1_video_catalog

## Task 3: Standardize labelled 60-second model-comparison grids, partial

### rollout_summary_files

- rollout_summaries/2026-09-26T16-36-41-rCgD-standardized_g1_video_grid_delivery.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/27/rollout-2026-09-27T00-36-41-01a0de93-7687-7e72-a4e6-d038bcdecc27.jsonl, updated_at=2026-09-27T15:39:19+00:00, thread_id=01a0de93-7687-7e72-a4e6-d038bcdecc27, reusable default grid/catalog pipeline and one 21-grid delivery complete; OD delivery pending)

### keywords

- build_g1_standard_grid.py, g1_video_catalog.py, grid60, 60-second, 1–9 panels, method_label, modules_label, Beat It, song-switch, validate_video, audio-complete, completion.json, watch-grid60.sh

## Task 4: Deliver representation standard suite and comparison grids, completed

### rollout_summary_files

- rollout_summaries/2026-09-25T06-32-18-QZn9-m2d_experiment_planning_and_localhost_memory_overgeneralizat.md (cwd=/home/wangyukun/ubt_isaac_sim_ws/m2d-ws, rollout_path=/home/wangyukun/.codex/sessions/2026/09/25/rollout-2026-09-25T14-32-18-01a0d743-c8ca-76c2-b455-07047969f47f.jsonl, updated_at=2026-09-27T15:23:31+00:00, thread_id=01a0d743-c8ca-76c2-b455-07047969f47f, 35 standard scenarios plus 21 grid videos, decode/audio and manifest verified)

### keywords

- representation_standard_suite_20260927, standard_cases=35, grid60_cases=21, final_videos=56, audio_video_full_decode, public/videos, local HTML catalog, completion manifest

## User preferences

- when the user says “每张卡里能并行就并行” and asks about half utilization -> assess MPS/same-GPU packing, but preserve batch, learning rate, seed, budget, and independent outputs; report progress, update/s, memory, policy, and ETA. [Task 1] [ad-hoc note]
- when the user said “要完全做好，视频生成都要有个通用的目录表统一展示每个视频对应的是什么，要写清楚架构，在视频生成代码里就要写成默认” -> make unified catalog plus architecture descriptions a default renderer output; deliver only audio-complete media. [Task 2]
- when the user requested “最多比如9个视频”, clear method/module labels, and standardized video directories -> default to a labelled 1–9-panel comparison grid plus unified catalog, not scattered MP4s. [Task 3]
- when the user asked for this to be “所有模型训练完后的视频渲染默认流程” -> finalizers require standard source renders, grid generation, catalog creation, and audio/video validation; incomplete sources stay incomplete and cannot be replaced with old-model output. [Task 3]

## Reusable knowledge

- Mixer has three matched one-GPU arms (`joint_stable`, `conv_stable`, `attention_stable`), seed1234 and 6250 updates/stage; at 2026-09-23 15:18 CST parent fits were 5412/5013/4924. Preserve its shared queue and no conclusion until downstream evaluation completes. [Task 1]
- RF MPS continuation: stop locally only at an atomic, uploaded/readback-verified checkpoint; R1 restarted at 4950 (17 unsaved updates recomputed), R2 at 0. User web terminal successfully submitted `m2d-rf-rollout-strength-1h` on node14; two private MPS clients, no restarts, ~13 sec/update/arm, ~69% mean GPU utilization and ~36GB HBM were observed. Training ETA excludes evaluation/videos. [Task 1]
- `packing-proof.json` plus `train-processes.json` prove two-client MPS; preserve seed, microbatch, parent checkpoint, update budget, disjoint outputs, and exact resume. An API HTTP 403 can differ from a privileged KubeSphere terminal identity. [Task 1]
- `scripts/g1_video_catalog.py` admits only MP4s with receipts showing complete decoded video and audio, publishes them/previews to `public/`, and writes `index.html`, `CATALOG.md`, `catalog.csv`, and `catalog.json`; architecture descriptions map to panel arms. FD output had 35 final videos/35 previews, zero `silent.mp4`; 2 unit tests and generic/C64 720-frame smoke renders passed. [Task 2]
- `scripts/build_g1_standard_grid.py` creates 1–9-panel labelled 60-second grids after checking matching audio, seed, source track, start frame, frame count, panel receipts, and full decode; `g1_video_catalog.py` publishes only verified final MP4s/previews to `public/` plus `index.html`, `CATALOG.md`, `catalog.csv`, and `catalog.json`. The canonical suite is 15 test songs, two training-display songs, Beat It, and three continuous song switches: 21 grids at 30 fps/1800 frames, unsmoothed. [Task 3]
- `runs/latent_chunk_history_20260926/standard-delivery/grid60/public/` is a verified completed delivery: manifests report `status: complete`, `count: 21`, every grid has 1800 frames and passed audio/video verification; `completion.json` records `grid60_videos: 21`. OD output remains pending until its `standard-delivery/completion.json` and `grid60/manifest.json` exist and are verified. [Task 3]
- The representation suite delivered 35 standard scenarios and 21 one-minute comparison grids (56 videos total); its final manifest reported `status=complete`, `standard_cases=35`, `grid60_cases=21`, `final_videos=56`, and `audio_video_full_decode=true`. Artifacts are under `runs/representation_standard_suite_20260927/public/videos` and `runs/representation_standard_suite_20260927/videos/grid60/public/videos`; the local HTML catalog is an artifact, not a requirement to start an HTTP server. [Task 4] [ad-hoc note]

## Failures and how to do differently

- `read_thread` rejects `turnLimit>10`; cluster status without local `kubectl`/Slurm needs hot-storage logs or user KubeSphere output. Do not infer scheduler state from local files, stop before an atomic checkpoint, or call training completion scientific acceptance. [Task 1]
- Do not expose render-workspace intermediates: silent composites/panels belong in temporary directories and must be removed after muxing. Rebase conflicts can touch experiment docs; preserve both newer repair history and catalog evidence, then rerun tests. [Task 2]
- Source standard videos alone do not prove grid delivery. Require completion/manifest/catalog records and per-panel matching song, seed, start, frame count, and audio/video receipts before reporting a grid complete. Use `.venv311` and the project `_ffmpeg_exe()`/`validate_video` helper if the direct import path stalls in `scipy/librosa`; system `ffprobe` is unavailable. A watcher launched with `--skip-grid` cannot satisfy the default flow: wait for all OD sources, then rerun without it. [Task 3]
