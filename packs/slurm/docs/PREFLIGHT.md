# Training Preflight

> Slurm training launch proof. Local GPU and Kubernetes use their own modules.

Cluster preflight has two parts: compare a normal resource request with viable
faster shapes using [TRAINING_EFFICIENCY.md](TRAINING_EFFICIENCY.md), then run
the executable correctness proof for the selected exact launch. The ledger's
`preflight` command implements the latter and reuses its passing receipt while
that launch identity is unchanged. Short resource probes are useful only when
they can change the choice; they do not replace the correctness proof.

The Slurm pack supplies the scheduler implementation.

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
      "mode": "slurm_interactive",
      "command": "srun --ntasks=1 --jobid=<verified-allocation> --exact --exclusive python train_route.py --gpu-preflight ..."
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

Use `slurm_interactive` for target-cluster proof. The implementation also
accepts `local` for legacy direct-GPU use, which does not prove Slurm execution.
An immediate GPU probe may be recorded as `skipped_unavailable` only if the
program never starts.
Once the GPU program starts, failure is real and blocks submission.

Ledger commands `preflight` and `launch` load the Slurm pack. The local and
Kubernetes modules use their own preflight paths.
