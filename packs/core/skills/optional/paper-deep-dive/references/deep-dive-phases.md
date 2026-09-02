# Deep Dive Phases

Mechanism: identify observables, controls, guarantees, baseline failure, and the
new information flow. Use a toy or boundary case.

Mathematics: define symbols/shapes/distributions, observed and latent variables,
conditioning, objective derivation, gradient effect, dimensions, limits, and
train/inference availability. Skip algebra that adds no understanding.

Architecture: trace raw inputs, preprocessing, representations, modules, losses,
sampling/decoding, and outputs. State shapes, ordering, normalization,
masking/causality, randomness, and bottlenecks.

Paper-to-code: map claims to official files, functions, configs, defaults, and
revision. Label verified, inferred, unavailable, or ambiguous; report code-paper
differences.

Evidence: map claims to exact figures/tables/ablations. Audit matched data,
capacity, compute, optimization, metrics, variance, selection risk, and whether
qualitative examples are merely illustrative.

Transfer: state shared structure, broken assumptions, local code/data surface,
frozen invariants, matched control, expected signatures, smallest test,
compute/provenance risks, and user decisions.

Synthesis: mechanism, assumptions, equations in causal order, architecture,
strongest and weakest evidence, code agreement, limitations, and reproduction
or adaptation checklist.
