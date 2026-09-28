# M2D GPU use preference

The user explicitly requested on 2026-09-23: "可以并行，要记住每张卡里能并行就并行".
When preparing independent M2D training runs, use concurrency within each allocated GPU where memory and measured execution permit it, including CUDA MPS. Do not interpret a one-GPU allocation as requiring sequential experiments. Keep each run's effective batch, seed, training budget, artifacts and exact resume independent; verify actual memory fit and concurrency. The current convolutional C16/C64 codec comparison has one H100/H200 available, so prepare both single-seed arms concurrently on that one allocated card. This does not authorize extra GPUs or changes to existing jobs.
