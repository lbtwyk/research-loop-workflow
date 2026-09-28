thread_id: 01a0cd1e-3517-71a1-849f-acb45c91a9a6
updated_at: 2026-09-25T11:48:58+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/23/rollout-2026-09-23T15-15-04-01a0cd1e-3517-71a1-849f-acb45c91a9a6.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Monitored and migrated the CausalCodec RF rollout to clustered single-GPU MPS

Rollout context: In `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws`, the user asked for Experiment 2 progress, ETA, utilization, and dynamic parallel allocation. The referenced thread concerned `EXP-20260923-fd-codec-causal-mixer`, but the later active work also handled `EXP-20260923-fd-rf-rollout-strength`.

## Task 1: Check Experiment 2 / CausalCodec mixer status

Outcome: partial

Preference signals:
- The user explicitly said “可以并行，要记住每张卡里能并行就并行” -> future training checks should consider concurrent workloads within each GPU, not only one process per card.
- The user focused on “eta，利用率…要并行动态分配” -> status reports should include live progress, measured throughput, ETA, GPU utilization, and whether same-card packing is safe.

Key steps:
- Read the referenced thread and identified Experiment 2 as three matched arms: original convolution, equal-parameter convolution, and local causal Transformer.
- Verified the formal contract: seed 1234, three independent one-GPU workers, 6250 updates each for codec/adaptation/stability, equal added parameters for convolution and attention, and no scientific conclusion before full evaluation.
- Read live hot-storage state and logs. At 2026-09-23 15:18 CST the three parent fits were still running: joint 5412/6250, conv 5013/6250, attention 4924/6250. Earlier measurements showed roughly 0.25, 0.27, and 0.33 seconds/update respectively.
- Confirmed the three jobs were running on separate H100/H200 allocations through hot-storage logs, but this rollout could not directly query `kubectl` from the local environment.

Failures and how to do differently:
- An initial `read_thread` call used `turnLimit=20` and failed because the tool maximum is 10; retry with `turnLimit=10`.
- The local machine had no `kubectl` or Slurm command, so cluster status required the authenticated hot-storage log bridge or user-provided KubeSphere output. Do not infer scheduler state from local files alone.

Reusable knowledge:
- Experiment 2’s canonical spec is `Musics2Dance/docs/experiments/EXP-20260923-fd-codec-causal-mixer.md`; launcher is `scripts/run_g1_codec_quality.py`; cluster delivery is `cluster-transfer/EXP-20260923-fd-codec-causal-mixer/release/APPLY_3H.txt`.
- The shared queue uses three one-GPU workers and writes progress under `/hot/upload/EXP-20260923-fd-codec-causal-mixer/results/`; missing `comparison/completion.json` means downstream evaluation has not completed.
- Hot-storage log tails can be read with `scripts/read_m2d_hot_logs.py`; this is useful when cluster control-plane access is unavailable.

## Task 2: Continue RF rollout on cluster and report ETA

Outcome: partial

Preference signals:
- The user asked “check，还要多久，在集群继续给我命令” and later “开跑了，check eta” -> after launch, proactively re-check actual progress and provide executable cluster commands rather than only describing the plan.
- The user accepted moving work to one GPU with MPS, preserving the scientific contract -> keep seed, microbatch, parent checkpoint, and update budget unchanged while improving utilization operationally.

Key steps:
- Monitored `EXP-20260923-fd-rf-rollout-strength`. Local R1 reached an atomic checkpoint at 4950/6250; the local process was stopped cleanly, with 17 unsaved updates intentionally recomputed after resume.
- Uploaded and read back the 4,006,940,281-byte `r1-recovery.pt`; SHA-256 readback verification passed. Handoff metadata was also uploaded and verified.
- Generated and validated the single-H100 MPS submission package at `cluster-transfer/EXP-20260923-fd-rf-rollout-strength/release/PASTE_1H.txt`. The command checks `kubectl auth can-i create jobs.batch -n ogi-llm`, verifies the PVC, avoids duplicate Job creation, and prints Job/Pod status.
- The saved API identity initially received HTTP 403 for Job creation, but the user later submitted successfully through a privileged KubeSphere terminal.
- Verified Job `m2d-rf-rollout-strength-1h` running on `node14`, Pod `m2d-rf-rollout-strength-1h-wzqk2`, no restarts, and two simultaneous private MPS clients.
- Verified both formal arms progressed: R1 resumed from 4950 and reached 5000/6250; R2 started from 0 and reached 52/6250. Both produced new cluster recovery checkpoints.
- Runtime evidence: approximately 13 seconds/update per arm, GPU utilization averaging about 69%, roughly 36 GB HBM used. ETA at the final check (2026-09-24 10:56 CST): R1 around 15:30–16:00 CST; R2 around 09:00–11:00 CST on 2026-09-25. Evaluation and videos occur afterward, so these are training ETAs only.

Failures and how to do differently:
- Do not stop local training until an atomic checkpoint exists, has been uploaded, and readback verified; the first stop attempt correctly waited for the next checkpoint.
- A 403 from one KubeSphere API identity does not prove the user’s web-terminal identity lacks permission. Distinguish API credentials from the terminal’s active account and ask for `kubectl auth can-i create jobs.batch -n ogi-llm` when necessary.
- Recovery files may briefly be absent from FTP immediately after training starts; use status/log files and retry later rather than declaring a failed run.

Reusable knowledge:
- Cluster job name: `m2d-rf-rollout-strength-1h`; namespace: `ogi-llm`; output root: `/hot/upload/EXP-20260923-fd-rf-rollout-strength/results/`.
- Key live artifacts: `results/packing-proof.json`, `results/train-processes.json`, `results/training/rf_joint_shift1/status.json`, `results/training/rf_joint_free2/status.json`, and `results/gpu.csv`.
- `packing-proof.json` records successful two-client MPS validation; `train-processes.json` exposes simultaneous client PIDs and progress.
- The experiment remains scientifically undecided until both arms finish fixed evaluation and video stages; training completion is not scientific acceptance.

References:
- `docs/experiments/EXP-20260923-fd-rf-rollout-strength.md`
- `docs/experiments/contracts/EXP-20260923-fd-rf-rollout-strength.json`
- `cluster-transfer/EXP-20260923-fd-rf-rollout-strength/release/PASTE_1H.txt`
- `runs/rf_rollout_strength_local/cluster-live-first-recovery.json`
- `runs/rf_rollout_strength_local/cluster-handoff.json`
- Exact status evidence: R1 `5000/6250`, R2 `52/6250`, ~13 sec/update, GPU mean utilization ~69%.

