thread_id: 01a0b378-0fdd-7bb1-8c60-f051ce14156c
updated_at: 2026-09-24T15:39:53+00:00
rollout_path: /home/wangyukun/.codex/sessions/2026/09/18/rollout-2026-09-18T15-43-05-01a0b378-0fdd-7bb1-8c60-f051ce14156c.jsonl
cwd: /home/wangyukun/ubt_isaac_sim_ws/m2d-ws

# Research workflow and preflight responsibilities were clarified and synchronized

Rollout context: Work covered `/home/wangyukun/research-loop-workflow` and `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance`. The user repeatedly preferred concise rules and corrected overcomplicated workflow wording.

## Task 1: Separate repository synchronization from issue/PR discussion

Outcome: success

Preference signals:
- The user clarified: “有阶段性结果再更新issuespr，很多时候是把产物证据更新repo，web可以读然后分析就可以了” -> sync useful code, documents, logs, and evidence to the repository independently; update issue/PR discussion only for meaningful stage results or decisions.
- The user said: “不要规则越堆越多” -> express the workflow with one short governing principle instead of layered repetitive conditions.

Key steps:
- Updated the GitHub handoff skill, core workflow, async workflow, project workflow, and comment template.
- Final principle: repository sync happens when outputs are useful; issue/PR updates are reserved for stage results or needed decisions.
- Verified installed copies and upstream source copies.

Reusable knowledge:
- GitHub repository synchronization is transport/publication for Web-readable artifacts, not inherently a request for scientific approval.
- Keep scientific acceptance, operational status, repository sync, and issue/PR discussion separate.
- Changes were synchronized to `research-loop-workflow` commit `599c6e7ed72ddd766e3a9a9b2df3ab4963aff884` and later preflight updates to `b8cd1966d8e5b0686e0e9a54b42870a14ac18f58`.

## Task 2: Make approved training checks complete the operational lifecycle

Outcome: success

Key steps:
- Moved `training-check-acceptance` into the reusable core skill layer so local GPU, Slurm, and Kubernetes workflows share the same lifecycle.
- Removed the old bounded-cycle behavior (“only repair once”, “check again next cycle”).
- The skill now continues approved operational work through repair/resume, declared downstream stages, evaluation, rendering, analysis, and formal reporting.
- It pauses only for a scientific route/contract/claim/outcome decision or an unrepairable external blocker.
- Updated project rules, core workflow, installation examples, Codex metadata, and installed skill copies.

Validation:
- Core ledger tests passed (`4 tests`, `OK`).
- Installation checks passed for core, local, Slurm, Kubernetes, combined, and personal installs.
- Skill validation passed; stale bounded-cycle phrases were searched for and removed.
- Changes synchronized to `research-loop-workflow` commit `599c6e7ed72ddd766e3a9a9b2df3ab4963aff884` and Musics2Dance commit `6cfc79a2047342b074eaec0267ce55eddab5f6c0`.

## Task 3: Correct local versus cluster preflight responsibilities

Outcome: success

Preference signals:
- The user explicitly required local preflight too: local should run a lightweight end-to-end validation proving the real flow completes without errors; cluster preflight should additionally compare ordinary and aggressive resource/training configurations to choose the fastest viable setup.

Key steps:
- Local preflight now means a short real-data path through a training update, checkpoint save/reload, and declared downstream entrypoints on tiny isolated inputs. It proves operational connectivity/error-free execution, not model quality or full throughput.
- Cluster preflight now has two responsibilities: compare normal and viable faster resource shapes using queue wait plus time to all declared results, then run the exact-command correctness proof for the selected shape on the target scheduler/cluster.
- Scientific settings remain fixed across resource candidates: batch, optimizer, seed, update budget, inputs, and evaluation scope. The ordinary configuration remains a fallback.
- Slurm documentation, training-efficiency guidance, KubeSphere documentation, local training docs, experiment-spec review routing, project `AGENTS.md`, workflow docs, README, and installed skills were aligned.
- Explicitly preserved target-cluster proof for Slurm (`slurm_interactive`) while allowing legacy local mode only as direct-GPU proof.

Validation:
- `git diff --check`, shell syntax, Python compilation, core tests, and skill validation all passed.
- Installation routing checks confirmed local, Slurm, and Kubernetes installs contain the appropriate preflight guidance.
- Remote contents were fetched and verified after synchronization.
- Musics2Dance preflight/workflow changes synchronized to commit `9a9ea48156e8a747de372ece8190fed11caf0b47`.

Failures and how to do differently:
- Initial wording incorrectly implied local work only needed changed-seam checks and early formal-run evidence. The user corrected this; future workflow edits must explicitly retain a lightweight local full-path preflight.
- Initial GitHub tree creation failed because deletion entries included files already absent remotely; the retry first compared local deletions against the remote tree, then succeeded.

References:
- `/home/wangyukun/research-loop-workflow/packs/local/docs/LOCAL_TRAINING.md`
- `/home/wangyukun/research-loop-workflow/packs/slurm/docs/PREFLIGHT.md`
- `/home/wangyukun/research-loop-workflow/packs/slurm/docs/TRAINING_EFFICIENCY.md`
- `/home/wangyukun/research-loop-workflow/packs/kubernetes/docs/KUBERNETES.md`
- `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/docs/research/modules/TRAINING_PREFLIGHT.md`
- `/home/wangyukun/ubt_isaac_sim_ws/m2d-ws/Musics2Dance/docs/research/modules/TRAINING_EFFICIENCY.md`
