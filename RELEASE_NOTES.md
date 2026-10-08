# Paper Reconstruction Stage 2 v1.0.2

Stage 2 v1.0 is the closed boundary-understanding component. It consumes accepted
piece crops and binary masks from the Stage 1 JSONL handoff and emits truth-free,
checksummed per-point probabilities plus ranked edge-fragment hypotheses.

Production is now portable and CPU-only. The release includes the frozen
opset-18 ONNX model and needs `onnxruntime`, not PyTorch or CUDA. PyTorch remains
available only through the training/export requirements.

Key evidence and integrity:

- architecture: `global_context_hybrid`, 6,337,604 parameters;
- protected holdout recall@10: 99.23% at IoU 0.50 and 98.24% at IoU 0.80;
- ONNX SHA-256: `3e80716280375146e2ef66942688e2a262e503df1011918caff262f0bae388a4`;
- source checkpoint SHA-256: `36dd4eb0f13bc49fc2efc791cca1de03d34997704e11cce5d7cff8a326c1a6fc`;
- random parity worst absolute error: `9.54e-6`;
- full-contour parity worst absolute error: `1.05e-5`, with identical candidate
  structures on the self-contained Stage 1 fixture.

The source release contains `models/stage2_boundary_v1.0.0.onnx`, tracked with
Git LFS, plus its manifest, checksums, schemas, tests, and integration fixture.
Run `scripts/run_stage2_inference.py` without a device flag; the CLI verifies the
model and selects only `CPUExecutionProvider`.
