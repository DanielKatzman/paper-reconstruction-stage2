# Distribution 2.0.0

Integration packaging around the unchanged Stage 2 software 1.0.2 and model
release 1.0.0. Both output schemas, trained weights, calibration, candidate policy,
CPU execution and core resume/verification behavior are preserved.

- Add `paper-stage2 run/inspect/verify` with explicit model paths and JSON results.
- Verify completed production output before returning a ready result.
- Add CPU setup, constraints, compatibility metadata and full runtime inventories.
- Preserve exact LF model-manifest bytes required by Stage 3 v2.0.0.
- Document Stage 4 v2.0.5 integration and the upstream boundary preparation step.

The package distribution version is 2.0.0; producer `software_version` remains
1.0.2 and authenticated model `release_version` remains 1.0.0. No retraining,
calibration or holdout rerun is included. This is a local release candidate until
source/model assets and validation receipts are published under an immutable tag.
