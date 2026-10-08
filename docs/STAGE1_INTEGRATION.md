# Stage 1 → Stage 2 integration contract

Stage 2 v1.0 consumes the immutable output directory produced by Stage 1. It
does not modify that directory and does not require synthetic seam truth during
production inference.

## Required Stage 1 layout

```text
stage1_output/
  segmentation_manifest.jsonl
  segmentation_run.json
  pieces/                 # tight RGBA piece crops
  piece_masks/            # matching binary 0/255 crop masks
  masks/                  # full-capture masks (Stage 1 provenance)
  overlays/               # optional Stage 1 review images
```

Each non-empty JSONL line is one capture record. Stage 2 requires these fields:

| Field | Meaning |
|---|---|
| `schema_version` | Stage 1 record schema identifier |
| `capture_id` | Unique filesystem-safe ID |
| `original_size_hw` | Original capture `[height, width]` |
| `bbox_xywh` | Tight crop `[x, y, width, height]` in original-capture pixels |
| `piece_path` | Relative path to the RGBA crop |
| `piece_mask_path` | Relative path to its binary crop mask |
| `accepted` | Whether the piece passed Stage 1 review |

Unknown Stage 1 fields are retained as provenance. By default, rejected records
are skipped. `--include-unaccepted` is an explicit research override.

Before inference, Stage 2 verifies relative-path containment, unique IDs, crop
and mask dimensions, bbox bounds, binary masks, and exactly one connected mask
component. It fingerprints the manifest row plus the actual crop and mask bytes,
so changing Stage 1 data invalidates an old resume safely.

## Production command

Install `requirements-inference.txt`, ensure the Git-LFS model
`models/stage2_boundary_v1.0.0.onnx` is present, and run from the repository
root. Production is CPU-only and does not require PyTorch or CUDA:

```powershell
python .\scripts\run_stage2_inference.py `
  --input "C:\path\to\stage1_output" `
  --output ".\generated\stage2_edge_hypotheses" `
  --resume
```

The CLI loads `models/release.json` by default, checks the ONNX SHA-256 before
creating a runtime session, validates all input/output tensors, and explicitly
selects `CPUExecutionProvider`. `--release` can point to another self-contained
release directory. `--batch-size`, `--stride`, and `--cpu-threads` are optional
performance controls; the frozen defaults are used otherwise.

The output must be outside the Stage 1 directory. A per-piece JSON record is the
atomic commit marker. With `--resume`, already committed pieces are reused only
after their identity, checksum, and core array shapes have been revalidated.

## Stage 2 output

```text
stage2_edge_hypotheses/
  edge_hypotheses_manifest.json
  inference_state.json
  pieces/
    <capture_id>.json
    <capture_id>.npz
  overlays/
    <capture_id>.png
```

The JSON record carries Stage 1 provenance and ranked, uncertain edge-fragment
hypotheses. The NPZ contains:

- ordered clockwise contour points in crop and original-capture coordinates;
- tangent, inward normal, curvature, corner strength, thickness, and arc length;
- per-point logits and probabilities for `seam`, `page_border`, and `uncertain`;
- per-point role-transition logits and probabilities.

It intentionally contains no synthetic truth fields. Stage 3 must consume the
probabilities and ranked hypotheses, not reinterpret every Stage 2 candidate as
a final edge declaration.

## Coordinate convention

- Pixel origin is top-left; x increases right and y increases down.
- Crop coordinates refer to `piece_path` / `piece_mask_path`.
- Source-capture coordinates refer to `original_size_hw`.
- Mapping is translation by the bbox origin:
  `source_xy = crop_xy + bbox_xywh[:2]`.
- The same mapping is recorded as `crop_to_source_homography`.

## Verify before Stage 3

```powershell
python .\scripts\verify_stage2_output.py `
  --input ".\generated\stage2_edge_hypotheses" `
  --release ".\models\release.json"
```

The verifier checks the completed manifest/state, path containment, checksums,
array names and shapes, finite normalized probabilities, coordinate mapping,
candidate ordering, optional overlay integrity, ONNX identity, release version,
and source-checkpoint lineage.
