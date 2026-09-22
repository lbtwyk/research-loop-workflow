# Kubernetes / KubeSphere Training

Use this module when a Kubernetes Job runs the work, including KubeSphere's Job
interface. The core workflow owns the experiment and scientific decision; this
module owns cluster delivery, Job status, and result readback.

1. Read the project's cluster overlay for namespace, GPU quota, node rules,
   storage, image, and access path. Prepare a versioned code/config delivery;
   do not modify source used by running Jobs.
2. Validate the exact Job manifest and inputs before submission. Record the
   image, code version, command, data and checkpoint mounts, output paths, and
   expected evidence in the experiment.
3. Distinguish a prepared manifest, created Job, scheduled Pod, running
   container, completed training, and completed evaluation. When a Job has no
   Pod, inspect Job events and namespace quota before reasoning from idle GPUs.
4. Keep logs readable during execution. Export metrics, useful logs, configs,
   and result manifests to storage the owner can read; verify readback before
   reporting delivery. Preserve checkpoint identity on a same-contract resume.

The project's overlay supplies concrete Job renderers, transfer commands, and
storage paths. This module does not assume cluster access from the local host.
