# Contributing

Stage boundaries and on-disk schemas are part of the public contract. A change
that alters input fields, coordinates, model inputs, output arrays, ONNX identity,
identity, or resume compatibility must update the relevant schema, tests, and
documentation. Breaking contract changes require a new schema version.

Before proposing a change, run:

```bash
PYTHONPATH=src python -m unittest discover -s tests -v
```

Do not commit generated datasets, experiment outputs, virtual environments, or
PyTorch checkpoints. Production ONNX graphs must be tracked with Git LFS and
their SHA-256 recorded under `models/`; source-checkpoint identity remains in
release metadata.
