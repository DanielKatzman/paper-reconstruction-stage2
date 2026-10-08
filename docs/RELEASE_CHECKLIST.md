# Stage 2 v1.0 release checklist

## Frozen research evidence

- [x] Source-level train/validation/calibration/holdout isolation
- [x] Architecture and checkpoint selected without holdout
- [x] Calibration and fragment proposal frozen before holdout
- [x] Full validation audit completed
- [x] Protected holdout evaluated once
- [x] Checkpoint and dataset fingerprints recorded
- [x] Model card and holdout summary published

## Production contract

- [x] Canonical Stage 1 JSONL handoff supported
- [x] Accepted-only default with explicit override
- [x] Stage 1 paths, dimensions, bbox, binary mask, and connectivity validated
- [x] Stage 1 directory treated as immutable
- [x] Truth-free contour compilation matches the training representation
- [x] Crop and original-capture coordinates exported
- [x] Ranked fragment hypotheses plus full probabilities exported
- [x] Atomic per-piece commits and puzzle-level resume
- [x] ONNX, source-checkpoint, and output integrity hashes
- [x] CPU-only ONNX Runtime production path with no PyTorch dependency
- [x] Random-tensor and full-contour PyTorch/ONNX parity validation
- [x] Public post-export verifier
- [x] Input/output JSON Schemas and self-contained handoff fixture

## Repository hygiene

- [x] One public production inference command
- [x] One public output verification command
- [x] Training/generator tools retained as modular research utilities
- [x] CPU inference, CUDA training, and maintainer export requirements separated
- [x] Unit tests and clean-extraction test pass
- [x] CI configuration included
- [x] Production ONNX tracked with Git LFS; training checkpoint excluded
- [x] Version and changelog set to the latest v1.0 patch

## Manual release steps

1. Install Git LFS, commit the source and ONNX pointer, and push the v1.0 tag.
2. Confirm `git lfs ls-files` lists `stage2_boundary_v1.0.0.onnx`.
3. Compare the ONNX SHA-256 to `models/release.json`.
4. Install only `requirements-inference.txt` in a clean CPU environment.
5. Run the example and a real Stage 1 handoff, then run
   `verify_stage2_output.py --release models/release.json` on both exports.

Stage 3 is deliberately out of scope for this repository. It starts from the
verified `edge_hypotheses_manifest.json` output contract.
