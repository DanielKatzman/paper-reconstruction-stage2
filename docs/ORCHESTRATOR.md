# Stage 2 v2 orchestrator contract

Distribution 2.0.0 preserves core software 1.0.2, ONNX model release 1.0.0,
calibration and the Stage 3-authenticated release manifest. Its LF bytes are
preserved on every platform: release manifest SHA-256 is
`0381683f5c8226974d73915b355bdd5936d80707219e7f083dcdf08f1ecfcfbc`.

Use Python 3.14, release constraints and CPUExecutionProvider. Source/model
verification is `tools/verify_release.py`; installed model verification is
`paper-stage2 verify --models <models>`. Assets are external to the wheel.

Input is an immutable prepared Stage 1 directory. Import accepted pieces only;
preserve physical IDs, binary connected crop masks, native pixel scale and bbox
translation. Compose the explicit Stage 1 boundary adapter before this stage for
predicted-mask captures. Stage 2 does not edit its input or read evaluation truth.

Run `paper-stage2 run --input <job/stage1> --output <job/stage2> --models <models>`.
The wrapper uses the existing frozen defaults, enforces the model/configuration
identity, runs production inference, then invokes independent output verification.
Thread budget can be selected with `--cpu-threads` (default 4). New computation
requires a dedicated output directory. Interrupted per-piece work can resume via
the identical command with `--resume`.

Progress goes to stderr; stdout contains one JSON result. Exit 0 means verified
evidence publication, 2 failure, 130 interruption. A published export is not a
solved page. Process locking and checksum/configuration-based resume retain the
existing core semantics. Confirm a crashed process is stopped before manually
recovering a stale lock; no automatic lock takeover is provided.

Output remains `edge_hypotheses_manifest.json`, schema
`stage2.edge-hypotheses-manifest.v1`, with `pieces/*.json` schema
`stage2.edge-hypotheses.v1`, NPZ arrays and optional overlays. Contours are
clockwise; x right, y down; source coordinates equal crop coordinates plus bbox
origin. Preserve the complete role/transition probabilities and ranked fragment
alternatives; no candidate becomes a final edge merely by ranking first.

Stage 3 v2.0.0 consumes this unchanged handoff with its original release/model
checks. Pin the v2 distribution's new source inventory separately in the
composition lock; do not rewrite Stage 3's historical Stage 2 v1.0.2 qualification
receipt. New integration receipts document the new packaging composition.
