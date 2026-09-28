thread_id: 01a0b8c5-6493-7560-9a92-78a194682cf3
updated_at: 2026-09-24T06:27:16+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/21/rollout-2026-09-21T16-58-01-01a0b8c5-6493-7560-9a92-78a194682cf3_01a0c32f-be1c-71f1-bdf7-6d94456d54fa.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Diagnosed a Kubernetes GPU-quota block, then audited slow GAN/ES committed-trajectory training

Rollout context: `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws`; namespace `ogi-llm`; experiment `EXP-20260919-fd-commit-trajectory-training`.

## Task 1: Diagnose and resolve the queued recovery Job

Outcome: success

Preference signals:
- The user asked how to see who is running and whether their own problematic jobs could be cleared, indicating they want ownership-aware inspection before deletion rather than blind cleanup.

Key steps:
- `m2d-commit-trajectory-3h-fast-r1` requested 3 GPUs but had no Pod; Job events repeatedly reported `requested: 3, used: 8, limited: 9` for `gpu-quota`.
- Inspected nonterminal Pods using full JSON resources rather than `custom-columns`, because dotted resource names such as `nvidia.com/gpu` can render incorrectly.
- Later output showed the recovery Pod `m2d-commit-trajectory-3h-fast-r1-5wfq2` Running with 3 GPUs. Active requests were the user’s 2-GPU causal job, the user’s 3-GPU recovery job, and a colleague’s 4-GPU job: total 9.

Failures and how to do differently:
- The initial no-Pod quota error was historical once the later Pod listing showed successful admission. Do not delete healthy jobs to resolve an already-cleared quota issue.
- Do not infer GPU usage from job names or low utilization; inspect `resources.requests`, labels, owner references, and process state.

Reusable knowledge:
- A Job can be `Running 0/1` while having no Pod because admission quota blocks Pod creation.
- Preserve a waiting Job; after quota frees, it can retry automatically.
- For cleanup, verify `author`, controller owner, requested GPU count, and whether the workload is abnormal; only remove owner-approved abnormal tasks.

References:
- `kubectl describe job m2d-commit-trajectory-3h-fast-r1 -n ogi-llm`
- `kubectl get pods -n ogi-llm --field-selector='status.phase!=Succeeded,status.phase!=Failed' -o jsonpath=...`
- Final active GPU allocation: `m2d-causal-native-2h-separated-cmb2g`=2, `m2d-commit-trajectory-3h-fast-r1-5wfq2`=3, `yiming-ma-4gpu-512gi-data-code1-shell-job-qwvp7`=4.

## Task 2: Audit slow GAN/ES training and compare mature methods

Outcome: success

Preference signals:
- The user asked whether the slowdown comes from too many steps, insufficient optimization, or an immature design, and requested comparison with mature papers/code. Future analyses should separate measured implementation waste from speculative method redesign and avoid changing the live run without approval.
- Existing constraints remain: preserve the original 183 training/18 test tracks and 6250 additional updates per arm.

Key steps:
- Inspected `train_g1_commit_trajectory.py`, `model/g1_commit_trajectory.py`, acceleration code, current progress snapshots, and archived official sources for Self Forcing, DMD2, EAR, and DPPO.
- Reconstructed the first 350 updates using real source ordering and burn-in selection, without launching GPU training.
- Wrote `docs/research/COMMITTED_TRAJECTORY_TRAINING_COST_AUDIT_20260921.md` and archived evidence under `runs/commit_trajectory/design-audit-20260921/`.

Validated findings:
- Owner snapshots showed GAN 273→274 at 19.55 s/update and ES 329→330 at 16.66 s/update; CoF remained reported at update 4333 and 2.35 s/update. No numeric GPU telemetry was supplied.
- Each update uses 48 groups and 4 particles; the scored trajectory has 16 commits and 10 denoising steps per commit.
- Burn-in reconstruction: mean useful burn-in 19.54 commits, but every batch was padded to a max burn-in of 64. About 69.46% of burn-in particle-plan forwards were discarded; including startup/scored generation, nominal discarded forward work was 46.80%. This is a work-count result, not a guaranteed wall-time speedup.
- GAN loops over groups for critic work; ES distance computation is already batched, so ES is primarily slowed by trajectory generation rather than the energy-score formula.
- No evidence established that 6250 updates are excessive or that H100 hardware is the root cause.

Mature-method comparison:
- Self Forcing uses few-step generation, self-rollout, and stochastic gradient truncation/cache detachment; it is the closest mechanism reference for limiting differentiated work.
- DMD2 uses backward simulation and few-step/one-step distillation; reducing the current 10 steps directly would be a new quality-risky method change.
- EAR demonstrates efficient two-sample Energy Score training, but its direct feed-forward objective is not equivalent to this full committed-trajectory objective.
- DPPO separates rollout collection from later optimization, but adopting it would require a different RL-style objective.

Recommended next action: first compact/pad burn-in work, batch GAN critic processing, and remove avoidable host synchronization while preserving data, particles, objective, budget, gradients, and resume semantics. Then separately test a Self-Forcing-style bounded-gradient variant with matched quality evaluation. No training code, live Job, method contract, or budget was changed in this rollout.
