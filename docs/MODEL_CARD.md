# Stage 2 boundary model card

## Model details

| Item | Value |
|---|---|
| Release | `1.0.0` |
| Architecture | `global_context_hybrid` |
| Task | Ordered-contour boundary-role and transition prediction |
| Roles | seam, page border, uncertain |
| Production model | `stage2_boundary_v1.0.0.onnx` (opset 18) |
| Production SHA-256 | `3e80716280375146e2ef66942688e2a262e503df1011918caff262f0bae388a4` |
| Runtime | ONNX Runtime `CPUExecutionProvider` |
| Source checkpoint SHA-256 | `36dd4eb0f13bc49fc2efc791cca1de03d34997704e11cce5d7cff8a326c1a6fc` |

The model combines local contour geometry, aligned RGB/mask strips, a normalized
whole contour, and whole-piece mask context. Full contours are evaluated with
overlapping windows; calibrated probabilities are converted into a bounded,
ranked set of hierarchical fragment hypotheses.

## Intended use

The model is the second stage of a torn-paper reconstruction pipeline. Its input
is an accepted Stage 1 piece crop plus a clean binary mask. Its output is
uncertain boundary evidence for a later matcher/solver.

It is not intended to reconstruct a page by itself, to declare one final edge
segmentation, or to operate directly on an unsegmented photograph.

## Training and evaluation data

The training system generates intact-page partitions with 2 through 30+ pieces,
including straight, wavy, sharp, notched, torn, and mixed-scissor cuts. It then
creates independently transformed Stage 1-like observations while retaining
exact canonical seam ownership only for supervision and evaluation.

Source-file-level train, validation, calibration, and protected holdout splits
prevent pages from the same source file or PDF from leaking across splits. Model
inputs exclude truth distance and label-confidence fields.

Frozen dataset fingerprints:

- boundary dataset: `6f0b7adee1bff720e387b91917466337ee87ee7b1fcb08fd376aa4358d0f6c50`
- observation dataset: `c5ab61fdbf2647c8ed981642719ac70788de56400b2095802116c328380b0833`

## Results

See [HOLDOUT_RESULTS.md](HOLDOUT_RESULTS.md) for the complete v1 release summary.
On 3,582 protected holdout observations (4,024 truth fragments), recall@10 was
99.23% at IoU 0.50 and 98.24% at IoU 0.80. Median best IoU@10 was 1.0.

## Limitations and risks

- Evidence is currently based on synthetic Stage 1-like observations. Real
  camera/domain evaluation is required before claiming general real-world quality.
- A six-piece real Stage 1 smoke test passed the complete integrity verifier, but
  it was unlabeled and therefore establishes interoperability rather than accuracy.
- Microscopic fragments near multi-seam junctions may not produce a distinct
  transition signal.
- Transition F1 (0.799 on holdout) is materially lower than seam/page-border F1;
  downstream code must retain alternative endpoints and top-K fragments.
- A connected binary mask is required. Mask topology errors from Stage 1 can
  create or remove contour segments that Stage 2 cannot recover.
- The model predicts geometry roles, not pairwise compatibility. Stage 3 must
  still compare fragment appearance/shape and reason globally.

## Reproducibility and integrity

The release metadata is stored in `models/release.json`. Production inference
records the exact ONNX SHA, source-checkpoint lineage, Stage 1
manifest/crop/mask fingerprints, configuration hash, software version, and
output checksums. The CLI rejects a modified model and always selects the CPU
execution provider. Random tensor parity and full-contour example parity both
passed with maximum absolute error below `1.1e-5`; candidate structures matched.
