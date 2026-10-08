# Changelog

## 1.0.2 — 2026-10-08

- Replaced the public PyTorch/CUDA inference path with a portable ONNX Runtime
  CPU path while retaining PyTorch only for training, export, and parity checks.
- Added the frozen 25.7 MB opset-18 model, Git-LFS tracking, exact model SHA-256,
  source-checkpoint lineage, and a self-contained v2 release manifest.
- Added exporter-side graph checking, tensor-contract checks, random multi-batch
  numerical parity, and full-contour candidate-structure parity validation.
- Updated production manifests and per-piece records to identify the actual ONNX
  model, runtime, release, and source checkpoint independently.
- Split CPU inference, CUDA training, and maintainer export dependencies; added a
  CPU-only CI smoke test over the canonical Stage 1 fixture.
- Preserved atomic per-piece resume and the v1 edge-hypothesis handoff while
  versioning incompatible in-progress inference state to v2.

## 1.0.1 — 2026-10-07

- Retried atomic file replacement when Windows Defender, an indexer, or another
  scanner temporarily denies access to a state file.
- Replaced shared fixed `.tmp` names with unique same-directory temporary files
  for prediction and production JSON, NPZ, and overlay commits.
- Preserved the existing per-observation resume contract; no model, calibration,
  fragment proposal, dataset fingerprint, or output schema changed.

## 1.0.0 — 2026-10-07

- Added the production Stage 1 JSONL adapter with accepted-only defaults,
  provenance retention, path containment, bbox/dimension checks, binary connected
  mask validation, and immutable-input fingerprints.
- Added truth-free boundary compilation and inference using the frozen training
  representation and calibrated global-context hybrid checkpoint.
- Added atomic per-piece edge-hypothesis exports with crop/source coordinates,
  full role and transition probabilities, ranked fragments, visual overlays,
  checksums, exact resume compatibility, and cross-process locking.
- Added a public post-export verifier for manifests, checksums, tensor shapes,
  normalized probabilities, coordinates, candidate order, and checkpoint identity.
- Froze the release checkpoint/dataset fingerprints and published the model card,
  holdout results, Stage 1 integration guide, JSON Schemas, example handoff, CI,
  license, and release checklist.
- Kept the checkpoint out of Git history; it is distributed as the `v1.0.0`
  release asset `stage2_boundary_v1.0.0.pt`.

## 0.6.4 — 2026-10-07

- Expanded fragment evaluation into a complete Recall@1/@3/@5/@10 matrix at
  IoU 0.50 and 0.80 while preserving the v2 top-5 metric names.
- Added overall and per-difficulty candidate-count minimum, mean, median, p90,
  p95, p99, maximum, zero, over-five, and over-ten statistics.
- Added explicit rank-6-through-10 recovery fields for every top-5 IoU 0.80
  failure, including top-10 endpoint errors and cyan recovery overlays.
- Versioned evaluation and failure-diagnostic schemas to v3 and v2 respectively.
- Kept this release measurement-only: model weights, calibration, and proposal
  generation are unchanged from the frozen v0.6.3 checkpoint.

## 0.6.3 — 2026-10-07

- Fixed endpoint adjustment for nearly complete circular seams: adjusted lengths
  are now bounded by the configured search radius and can never fall below the
  minimum fragment length.
- Replaced destructive transition splitting with hierarchical hypotheses that
  preserve raw and endpoint-adjusted parent fragments alongside split children.
- Added a lower-threshold transition-split hypothesis for real boundaries whose
  endpoint probability is useful but below the primary split threshold.
- Bounded the number of transition splits per parent and exactly deduplicated
  hypotheses so additional uncertainty does not create an unbounded candidate set.
- Versioned fragment calibration as v2 and jointly calibrate the primary and
  relaxed transition thresholds on the reserved calibration split.
- Added one resumable `refine_boundary_fragments.py` command that recalibrates and
  validates an existing trained winner without retraining or touching holdout.
- Added regression tests for the observed one-point circular collapse, minimum
  fragment enforcement, parent preservation, and relaxed split hypotheses.

## 0.6.2 — 2026-10-06

- Fixed CUDA checkpoint resume during experiment promotion by converting
  checkpoint-mapped RNG states back to the CPU ByteTensors required by PyTorch.
- Fixed transition/global-context cache collisions between different puzzles that
  reuse observation names such as `piece_004__view_01`; cache identities now use
  the unique puzzle boundary path and observation index.
- Fixed transition-balanced profiling/training when an observation is indexed as
  uncertain but its soft transition target peaks below 0.50; the sampler now uses
  the strongest soft transition points and deterministically skips unusable entries.
- Migrated CUDA AMP profiling and training contexts to the current `torch.amp` API.
- Added explicit transition-centered sampling to 20% of the default training
  stream, while retaining compatibility with custom three-role weight maps.
- Added an extra-large local hybrid candidate so model capacity is measured rather
  than inferred from the compact baseline checkpoint.
- Added a global-context hybrid candidate that combines local RGB/mask strips with
  a normalized 256-point complete contour, whole-piece mask, and cross-attention.
- Extended training, profiling, calibration, inference, and prediction paths to
  carry global context without changing the Stage 1-derived dataset on disk.
- Expanded the OOM-safe profiler to include batch size 8 and to choose loader
  workers jointly on representative local and global models.
- Changed successive-halving promotion to emphasize top-5 IoU 0.80 fragment recall
  and transition F1 instead of allowing point accuracy to dominate.
- Changed fragment-threshold calibration to prefer accurate endpoints over loose
  overlap.
- Added fragment metrics by difficulty plus automatic JSON/PNG diagnostics for
  every validation truth seam missed at top-5 IoU 0.80.
- Versioned checkpoints, profiles, experiments, evaluations, and the public role
  pipeline so changed sampling/model inputs cannot be resumed unsafely.
- Expanded tests for transition sampling, global context, global model outputs,
  the larger candidate registry, and best-fragment matching.

## 0.6.0 — 2026-10-06

- Replaced synchronous training-time strip generation with a deterministic
  map-style loader and configurable Windows-safe worker prefetch.
- Preserved exact batch resume by deriving every window from its epoch and absolute
  sample index; prefetched but unconsumed windows no longer advance sampler state.
- Added base, wide, large, temporal-plus-attention, geometry-only, and raster-only
  contour-model candidates.
- Expanded hardware profiling into an OOM-safe worker and model matrix with fetch,
  compute, throughput, VRAM, per-model best, and common safe recommendations.
- Added a resumable validation-only successive-halving runner: all candidates train
  to 3 epochs, the top two to 10, and the winner to 20 before one calibration pass.
- Ranked experiments using point-role quality and full-contour fragment recall;
  routine model selection never evaluates the protected holdout split.
- Added fixed CUDA 12.6 PyTorch requirements for the Windows/GTX 1070 environment.
- Added tests for model candidates, fragment-aware ranking, and memory-headroom
  profile selection.

## 0.5.0 — 2026-10-06

- Added `BoundaryRoleNetV1`, a lightweight dual-stream contour network combining
  observable mask geometry with aligned RGB/mask raster strips.
- Removed supervision-only label confidence and truth distance from model inputs;
  they remain loss weights/diagnostics, preventing synthetic ground-truth leakage.
- Added soft three-role loss, transition/endpoint focal loss, stable-region
  smoothness loss, role-balanced training, and natural-distribution validation.
- Added exact batch-level training resume, atomic last/best checkpoints, safe Ctrl+C,
  deterministic RNG restoration, early stopping, and training histories.
- Added resumable training-statistics compilation and GPU throughput/memory profiling.
- Added full closed-contour sliding-window inference with overlap aggregation.
- Added probabilistic seam-fragment proposals with hysteresis, circular contours,
  transition-based splitting, multiple thresholds, and ranked top-K candidates.
- Added calibration-only temperature fitting and fragment-threshold selection;
  the holdout split remains protected from routine evaluation.
- Added full-contour metrics, difficulty-stratified reports, fragment recall@K,
  and calibrated prediction export with atomic per-observation resume and overlays.
- Added one public `run_boundary_role_pipeline.py` command over modular statistics,
  training, calibration, and validation stages.
- Expanded tests for statistics, calibration, metrics, fragment extraction, model
  shape/loss behavior, natural sampling, and prediction rendering.

## 0.4.0 — 2026-10-05

- Added one public `run_stage2_pipeline.py` command for canonical, observation,
  boundary, and final validation stages while retaining modular internals.
- Added atomic per-puzzle checkpoints and `--resume` to canonical and observation
  generation, matching the existing boundary compiler behavior.
- Added a cross-platform process lock, atomic pipeline state, clean Ctrl+C handling,
  status reporting, stop-after controls, and completed-stage adoption.
- Added exact resume compatibility checks using configurations and input fingerprints.
- Added a bounded-memory boundary-training index and role-balanced circular-window
  sampler over the 43M-point-scale dataset.
- Added local RGB/mask raster strips plus contour geometry and soft targets for the
  future dual-stream boundary-role model.
- Added an optional deterministic PyTorch `IterableDataset` adapter and a loader
  inspection command.
- Added resume-equivalence, unified-pipeline, and streaming-loader tests.

## 0.3.0 — 2026-10-05

- Added ordered clockwise contour extraction for observed masks.
- Added uniformly sampled boundary geometry features and compact per-puzzle arrays.
- Added soft seam, page-border, and uncertainty targets with distance-aware snapping.
- Added canonical seam tracks for all owners and observation views.
- Added minimum seam-length and projection-coverage gates for match-training tracks.
- Prevented future observation perturbations from disconnecting a piece or silently dropping a lobe.
- Added boundary-role and stable seam-ID preview montages.
- Added input fingerprint checks, output fingerprints, JSON Schemas, and validation.
- Added atomic puzzle writes and safe `--resume` support for long compilation jobs.
- Expanded the tests for contour geometry, mappings, role targets, correspondence direction, determinism, and resume behavior.

## 0.2.0 — 2026-10-04

- Added deterministic source-file train/validation/calibration/holdout splits.
- Added exact difficulty schedules and difficulty-conditioned cut distributions.
- Added per-piece, per-seam, and per-puzzle geometry diagnostics.
- Added the direct observation compiler with independent transforms and controlled imaging/mask corruption.
- Added exact crop/source-page forward and inverse homographies for every observation.
- Added observation previews, manifests, fingerprints, schemas, and validation.
- Expanded the test suite with split, observation, determinism, connectivity, and homography tests.

## 0.1.1

- Added the complete local virtual-environment requirements, including PyMuPDF.
- Improved the missing-PDF-dependency error message.

## 0.1.0

- Introduced deterministic canonical puzzle generation for 2-to-30+ pieces.
- Added exact piece, seam, adjacency, page-border, and cut-event truth.
