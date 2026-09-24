# Local GPU Training

Use this module when the training process runs on a GPU attached to the current
host. The core workflow still owns the experiment, contract, evidence, and
scientific decision.

- Before a formal launch, run a **lightweight end-to-end preflight** with the
  project's actual launcher, real data, and a small isolated output. Reach a
  training update, checkpoint save and reload, then each declared evaluation,
  render, or export entrypoint on a tiny input. Check exit status and readable
  outputs. Keep the test short; it proves the path runs without an error, not
  model quality or full-scale throughput.
- Fix any failure and rerun only the affected path. Record the command, log,
  result, and any untested stage in the experiment. A CPU-only check does not
  prove the GPU path. Reuse a passing preflight while the launcher, inputs, and
  downstream paths it exercised are unchanged.
- Launch the frozen formal command in a durable session with an explicit log
  and output directory. Record the command, environment, process/session
  identity, and checkpoint path in the experiment. Use its early progress to
  verify that the full run continues normally.
- Follow the live process and artifacts; do not infer progress from a session
  name alone. Preserve the same contract and checkpoint identity on recovery.
- Training completion closes only the training stage. Evaluate and report the
  remaining declared stages before asking for a scientific decision.
