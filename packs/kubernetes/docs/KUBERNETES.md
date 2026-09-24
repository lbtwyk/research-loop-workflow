# Kubernetes / KubeSphere Training

Use this module when a Kubernetes Job runs the work, including KubeSphere's Job
interface. The core workflow owns the experiment and scientific decision; this
module owns cluster delivery, Job status, and result readback.

1. Read the project's cluster overlay for namespace, GPU quota, node rules,
   storage, image, and access path. Prepare a versioned code/config delivery;
   do not modify source used by running Jobs.
2. Preflight the normal Job shape and list viable faster shapes that fit the
   actual GPU quota and node placement: for example, a larger single Pod or
   parallel independent Jobs when the contract allows them. Validate the
   manifest, image, inputs, and a short real training, checkpoint reload, and
   declared downstream path on the target cluster. Compare expected scheduling
   wait plus measured or inferred
   time to the declared result; keep batch, optimizer, seeds, update budget,
   and evaluation fixed. Select the fastest viable shape and keep the normal
   one as fallback. A manifest validation or local run alone does not prove
   target-cluster execution.
3. Record the selected image, code version, command, GPU request, data and
   checkpoint mounts, output paths, preflight result, and expected evidence in
   the experiment.
4. Distinguish a prepared manifest, created Job, scheduled Pod, running
   container, completed training, and completed evaluation. When a Job has no
   Pod, inspect Job events and namespace quota before reasoning from idle GPUs.
5. Keep logs readable during execution. Export metrics, useful logs, configs,
   and result manifests to storage the owner can read; verify readback before
   reporting delivery. Preserve checkpoint identity on a same-contract resume.

The project's overlay supplies concrete Job renderers, transfer commands, and
storage paths. This module does not assume cluster access from the local host.
