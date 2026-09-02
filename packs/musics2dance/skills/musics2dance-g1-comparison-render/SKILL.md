---
name: musics2dance-g1-comparison-render
description: Use when `/home/tianhup/Desktop/Musics2Dance` needs a FineDance-G1 comparison render, especially if the user says not to use cached features, wants outputs overwritten, or needs VSCode/browser-preview-safe MP4 verification.
argument-hint: "[song/model spec or output target]"
allowed-tools:
  - read_file
  - grep
  - run_terminal_command
---

# Musics2Dance G1 Comparison Render

## When to use

Use this when working in `/home/tianhup/Desktop/Musics2Dance` and the task is to:

1. Render a new FineDance-G1 multi-model comparison video
2. Compare actual inference behavior instead of cached dataset-feature replay
3. Overwrite an existing comparison directory with a final render
4. Verify that the output MP4 is preview-safe in VSCode/Chromium
5. Render structured model specs that include condition variants such as `pred_controls` or `pred_energy`

Do not use this for training-only jobs, generic metric-only evaluation, or non-MuJoCo media work.

## Inputs / context to gather

1. Confirm the target song or sliced audio source.
2. Capture the requested duration or `sample_size` expectation.
3. Collect the exact `--model` specs, including whether any structured condition variant is needed.
4. Confirm whether the user wants:
   - `--feature_source extract`
   - overwrite of an existing render directory
   - MuJoCo output or temporary stick fallback
5. Check the current helper/test state:
   - `eval/render_g1_checkpoint_comparison.py`
   - `eval/g1_visualization.py`
   - `tests/test_render_g1_checkpoint_comparison.py`

## Procedure

1. Start by inspecting the current render helper and confirming the target output directory naming.

2. Default to inference-style extraction when the user wants real model behavior:
   - Use `--feature_source extract`
   - Later verify the manifest records `feature_source=extract` and `audio_source=extract`

3. If the model specs need structured variants, confirm the helper can parse them:
   - Example shape: `name:feature_type:interp:checkpoint:condition_variant`
   - Known variants captured in memory: `pred_controls`, `pred_energy`

4. Prefer MuJoCo rendering with EGL on this machine:
   - Set `MUJOCO_GL=egl` before running the render path if needed
   - Pass `--g1_render_backend mujoco --g1_mujoco_gl egl`

5. If the GPU is cold or probing hangs, keep momentum with a temporary fallback:
   - Check `nvidia-smi` and any CUDA probe once
   - If the machine is in the known cold-start stall state, use a CPU/stick fallback only as a temporary artifact path
   - If the user wants the final MuJoCo output, overwrite the same target directory once the GPU recovers

6. Run or patch tests when the helper changes:
   - `python -m unittest tests.test_render_g1_checkpoint_comparison`

7. Verify the artifact, not just command success:
   - Confirm the output `comparison.mp4` exists
   - Inspect the adjacent `manifest.json`
   - Run `ffprobe` and confirm the preview-safe shape: `codec_name=aac`, `sample_rate=48000`, `channels=2`, `channel_layout=stereo`

8. If the task is part of an experiment branch, update the relevant `docs/experiments/*.md` entry and index once the artifact and route are verified.

## Efficiency plan

1. Reuse the existing comparison helper rather than inventing a one-off render command.
2. Cache these facts before answering:
   - chosen output directory
   - whether the render used `extract` or cached features
   - whether condition variants were parsed
   - whether MuJoCo used `egl`
   - whether `ffprobe` confirmed AAC stereo 48kHz
3. Stop rules:
   - If the manifest proves `extract` plus the correct condition variants and `ffprobe` proves the audio shape, stop digging.
   - If the GPU issue is only the known cold-start stall, do not over-debug the whole machine before getting a fallback render out.

## Pitfalls and fixes

- Symptom: the comparison is not representative of inference.
  - Likely cause: cached dataset features were used
  - Fix: switch to `--feature_source extract` and verify through `manifest.json`

- Symptom: MuJoCo render setup fails or sample rendering dies with GL initialization errors.
  - Likely cause: wrong or missing GL backend
  - Fix: use `MUJOCO_GL=egl` and `--g1_mujoco_gl egl`; do not treat `gladLoadGL`-style failures as model crashes

- Symptom: a structured v3/r05 render spec is rejected or the wrong condition path runs.
  - Likely cause: the helper does not yet parse `condition_variant`
  - Fix: patch `eval/render_g1_checkpoint_comparison.py`, then rerun tests before rendering

- Symptom: the MP4 has audio but VSCode preview is silent.
  - Likely cause: preview compatibility rather than missing audio
  - Fix: normalize to AAC stereo 48kHz and confirm with `ffprobe`

- Symptom: the user asked to overwrite old stick outputs but both old and new directories remain.
  - Likely cause: treating the fallback render as final
  - Fix: render back into the same target directory once the final MuJoCo path is ready

## Verification checklist

1. Confirm the final artifact path exists and matches the intended directory.
2. Confirm the manifest records the intended `feature_source` and condition variants.
3. Confirm the render backend/backend flags match the machine reality (`egl` for MuJoCo here).
4. Confirm `ffprobe` shows AAC stereo 48kHz for preview safety.
5. If code changed, confirm `python -m unittest tests.test_render_g1_checkpoint_comparison` passed.
