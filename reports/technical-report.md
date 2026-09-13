# Cozmo AI Technical Report

_Maximum six pages when exported._

## 1. Summary

State the capture routes, three tiers, output contract, and current benchmark status.

## 2. Architecture

Describe tier-specific ingestion, the common geometry model, room stitching, damage analysis, uncertainty, and artifact generation. Link to the owning source files.

## 3. Tier design and device matrix

Summarize the stock capture protocol, tested devices, raw data, and accuracy by tier. Use `reports/capture-protocol.md` and `reports/device-matrix.md`.

## 4. Drift handling and error budget

Explain loop closure, pose graph or plane-anchored correction, and show the on/off ablation. Separate sensor, reconstruction, calibration, and stitching error.

## 5. Calibration analysis

Report intervals, coverage, bias, and repeatability. State whether ceiling estimates are biased or unrepeatable when they fail.

## 6. Results

Summarize all gates, the two-room incumbent comparison, processing time, and links to raw data and generated outputs.

## 7. Fix loop

Describe the worst gate, root-cause evidence, shipped fix, prediction, before run, after run, and readable diff. Link to `reports/fix-loop.md`.

## 8. Known failure modes

Cover mirrors, glass, wet-look surfaces, low light, occlusion, thin structures, repeated textures, and unsupported devices. State the fallback or uncertainty behavior for each.

## Current status

This is a report skeleton. It must not be presented as a completed benchmark report until raw captures, ground truth, diagnostics, and measured results are added.
