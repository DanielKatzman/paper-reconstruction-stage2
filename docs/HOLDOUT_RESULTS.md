# Frozen v1.0 validation and holdout results

Architecture, checkpoint, calibration, and fragment-proposal rules were frozen
before the protected holdout split was opened. The holdout report used the same
checkpoint SHA-256 published in `models/release.json`.

## Summary

| Metric | Validation | Holdout |
|---|---:|---:|
| Observations | 512 | 3,582 |
| Truth fragments | 587 | 4,024 |
| Point accuracy | 0.9966 | 0.9979 |
| Seam F1 | 0.9983 | 0.9990 |
| Page-border F1 | 0.9920 | 0.9960 |
| Uncertain F1 | 0.8152 | 0.8180 |
| Transition F1 | 0.8152 | 0.7991 |
| Recall@1, IoU 0.50 | 0.8620 | 0.8780 |
| Recall@1, IoU 0.80 | 0.8450 | 0.8509 |
| Recall@3, IoU 0.50 | 0.9676 | 0.9744 |
| Recall@3, IoU 0.80 | 0.9557 | 0.9635 |
| Recall@5, IoU 0.50 | 0.9881 | 0.9863 |
| Recall@5, IoU 0.80 | 0.9744 | 0.9764 |
| Recall@10, IoU 0.50 | 0.9966 | 0.9923 |
| Recall@10, IoU 0.80 | 0.9813 | 0.9824 |
| Median best IoU@10 | 0.9995 | 1.0000 |
| Selection score | 0.9614 | 0.9603 |

## Candidate-set size

| Statistic | Validation | Holdout |
|---|---:|---:|
| Mean candidates / observation | 4.07 | 3.81 |
| Median | 4 | 4 |
| p95 | 8 | 8 |
| p99 | 11 | 10 |
| Maximum | 14 | 19 |
| Zero-candidate observations | 0 | 0 |

These measurements support the intended contract: Stage 2 emits a small top-K
set rather than a single irreversible guess. At strict IoU 0.80, holdout recall
rose from 85.09% at rank 1 to 98.24% by rank 10.

## Interpretation

The holdout results are consistent with validation and do not show the expected
pattern of a collapsed or overfit release. They do not establish real-camera
domain performance, because both reports use synthetic Stage 1-like observations.
The production adapter and overlays are therefore part of the release specifically
so real Stage 1 runs can be audited without changing the frozen model.
