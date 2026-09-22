# Local GPU Training

Use this module when the training process runs on a GPU attached to the current
host. The core workflow still owns the experiment, contract, evidence, and
scientific decision.

- Launch the frozen command in a durable session with an explicit log and output
  directory. Record the command, environment, process/session identity, and
  checkpoint path in the experiment.
- Check changed code and data seams before launch. Use the formal run's early
  real-data, optimizer, GPU-memory, and throughput evidence as the usual runtime
  proof. Add a separate resume or downstream check when that path changed or
  failed.
- Follow the live process and artifacts; do not infer progress from a session
  name alone. Preserve the same contract and checkpoint identity on recovery.
- Training completion closes only the training stage. Evaluate and report the
  remaining declared stages before asking for a scientific decision.
