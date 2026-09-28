# ogi-llm GPU distribution snapshot — 2026-09-22

User requested a short record of llm resource shape. Source: user-pasted kubectl Pods and scheduling Events in side conversation. This is a historical snapshot, not live availability.

- node13: Running m2d-causal-history-3h-llm-only-69hhb requests 3 GPUs; Running yiming-ma-4gpu-512gi-data-code1-shell-job-qwvp7 requests 4 GPUs. Confirmed namespace Running requests on node13 total 7 GPUs. Node total capacity was not readable/verified; do not assert 8 GPUs or exactly 1 free as fact.
- node14: completed shared music shard 3 previously requested 1 GPU. Current pasted namespace list showed no positive Running GPU request there; actual free GPUs and other namespace allocations unknown.
- Shared music 5H ran as five independent 1-GPU Pods: four on node13, one on node14; all Succeeded. It did not require five GPUs on one node.
- m2d-causal-stability-2h-gs7wg: Pending, requests 2 GPUs in one Pod (same node), CPU 24, memory 128Gi. Events: 4 nodes Insufficient nvidia.com/gpu; other nodes excluded by pool/control-plane taints. Only ogi-llm pool tolerated. No CPU/memory shortage reported.
- User reports group has two remaining GPUs. Fragmentation across nodes is plausible, not proven by available namespace-only evidence. User cannot list cluster nodes (Forbidden).
- User authorized main chat to quickly split pending 2H stability work into two independently schedulable 1-GPU tasks, preserve six arms/budget and separate outputs, preserve Running 3H history job, reuse completed music. This side chat did not implement or send a message to main chat; no cross-thread messaging tool available.
