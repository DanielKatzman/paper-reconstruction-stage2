# v2 integration validation

The full existing Stage 2 suite plus release-interface checks runs with
`python -m unittest discover -s tests -v`. Training-model tests skip when optional
Torch is absent; CPU production tests exercise actual ONNX inference and release
integrity. No model training, calibration or holdout rerun is part of this release.

The composition workspace records fresh four-stage CPU execution and exact
artifacts in `VALIDATION.md` and the
[qualification receipt](../provenance/INTEGRATION_VALIDATION.json).
`tools/verify_release.py` checks distribution metadata, complete runtime inventory
and frozen assets; `paper-stage2 inspect` independently validates a published
handoff. New tests reject mismatched model release configuration.

All 54 tests completed on Windows and Ubuntu/WSL: 51 passed and 3 optional
training tests skipped. Fresh four-stage CPU runs on both platforms produced a
supported connected four-piece assembly. Container deployment remains a
separate qualification gate. Synthetic fixtures and historical holdout metrics
have different scopes and must not be presented as real-photo accuracy results.
