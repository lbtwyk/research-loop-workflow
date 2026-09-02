# Training Preflight

Training preflight is one executable proof for a new or changed formal launch
identity. Reuse the passing receipt while the identity is unchanged. It is not
a miniature experiment.

This document is the interface. The slurm pack supplies the scheduler
implementation.

## Contract Interface

A training launcher must be identified when its filename is not unambiguously
a training entrypoint. A scope that owns one kind of launcher may use
`execution_kind`; mixed scopes use `launcher_kinds`.

```json
{
  "execution_kind": "training",
  "training_preflight": {
    "cpu_checks": [
      {
        "name": "real-path",
        "command": "python train_route.py --preflight ...",
        "covers": [
          "entrypoint",
          "real_data",
          "loader_single_process",
          "loader_formal_workers",
          "loader_soak",
          "train_step",
          "checkpoint_resume",
          "downstream_hook"
        ]
      }
    ],
    "gpu_check": {
      "mode": "local",
      "command": "python train_route.py --gpu-preflight ..."
    }
  }
}
```

Across the declared CPU checks the command must prove:

- entrypoint imports and exact argument or config resolution;
- real dataset construction and at least one real sample or batch;
- DataLoader iteration with `num_workers=0` and the formal worker settings;
- a bounded soak across enough real samples to exercise lazy handles;
- a finite forward, loss, backward, and optimizer step;
- atomic checkpoint save, reload, and the next exact-resume step;
- one cheap invocation of the first declared downstream hook.

Synthetic tensors, import-only tests, `--dry-run`, and a forward without
optimizer or checkpoint proof do not satisfy the interface.

`gpu_check.mode` is `local` or `slurm_interactive`. An immediate GPU probe
may be recorded as `skipped_unavailable` only if the program never starts.
Once the GPU program starts, failure is real and blocks submission.

Ledger commands `preflight` and `launch` load the slurm pack. Without that
pack they refuse instead of inventing a local substitute.
