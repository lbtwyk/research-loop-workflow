---
name: kubernetes-gpu-quota-diagnosis
description: Diagnose an ogi-llm Kubernetes GPU Job that is Running 0/1, Pending, or has no Pod; distinguish quota admission and same-node scheduling blocks from trainer failures before cleanup or resubmission.
allowed-tools: Bash
---

## When to use

Use for a Kubernetes Job that cannot create a Pod, reports `Running 0/1`, is Pending, or appears GPU-quota/scheduling blocked. Do not use it to delete Jobs, Pods, or other users' work; that needs explicit authorization after ownership and current state are verified.

## Inputs and context

1. Take `$0` as the Job name and `$1` as the namespace; default the namespace to `ogi-llm` only when the caller has not supplied one.
2. Record the newest user-provided status as potentially stale. Get current state before interpreting old `describe` output.

## Procedure

1. Inspect the Job first:

   ```bash
   kubectl describe job "$0" -n "${1:-ogi-llm}"
   ```

   Read Events for `FailedCreate` and quota text such as `exceeded quota: gpu-quota`.
2. List current nonterminal Pods and inspect JSON/JSONPath resource requests, `author` labels, and owner controllers. Do not rely on task names or instantaneous GPU utilization; quota is based on requested `nvidia.com/gpu`. Avoid `custom-columns` for dotted resource names.
3. If there is no Pod and Events show admission quota, keep the waiting Job: it can retry when quota frees. Report the requested, used, and limit values plus safe cleanup candidates only if their owner/current state has been verified.
4. If a Pod is Pending, inspect its Events, GPU request, node selectors/affinity, and tolerations. A single 2-GPU Pod needs both requested GPUs on one eligible node; `Insufficient nvidia.com/gpu` plus taint exclusions is a scheduling fact, not proof of total free capacity or fragmentation. Do not resubmit while it is Pending unless the caller asks for a scoped change.
5. If a Pod is Running, do not resubmit. Tail the Job log:

   ```bash
   kubectl logs -f --tail=50 -n "${1:-ogi-llm}" job/"$0"
   ```

   Treat `preflight` as startup; `formal_started` plus increasing `update` values is real training progress.

## Efficiency plan

- Make one current Job/Pod snapshot before proposing action; use that to avoid repeated stale queries.
- Stop diagnosis once the Pod is Running and logs show increasing updates, unless the caller asks for training-performance analysis.
- For a Pending Pod, stop after one current Pod/Event/toleration snapshot unless the caller authorizes changing the resource shape; namespace-only listings cannot establish node capacity or other-namespace allocations.
- Keep a no-Pod diagnosis to Events/quota; logs cannot diagnose a Pod that does not exist.

## Pitfalls and fixes

- `Running 0/1` with no Pod -> likely admission failure, not trainer failure -> inspect Events/quota before logs.
- Old `describe` says blocked but a later dump shows a Pod -> state changed -> trust a fresh nonterminal Pod listing and preserve the Job.
- Low utilization or a name containing `4gpu` -> not evidence of a quota request or abnormal owner -> inspect actual `nvidia.com/gpu` requests and controller metadata.
- Pending multi-GPU Pod with `Insufficient nvidia.com/gpu` -> could be same-node placement and eligibility constraints -> inspect Events/tolerations; do not claim an 8-GPU node, a free GPU count, or proven fragmentation from namespace-only output.

## Verification checklist

- The Job's current Pod existence and phase are known.
- Any quota claim includes requested, used, and limit values from current Events/state.
- Any cleanup recommendation names a verified owner/controller and has explicit authorization.
- A Pending Pod has current Events, GPU request, and toleration/eligibility constraints recorded before proposing a split or other resource-shape change.
- If a Pod exists, logs establish whether it is only preflight or has increasing formal updates.
