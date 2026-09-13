# Compliance Matrix

Status values: `PASS` means verified in this repository, `PARTIAL` means the interface exists but the required real-world capability is not complete, and `PENDING` requires capture hardware, benchmark data, or an external app export.

| Requirement | File path | Artifact / evidence | Status |
|---|---|---|---|
| One command per capture | `src/cozmo_scan/cli.py` | `python -m cozmo_scan.cli --tier ... --input ... --output ...` | PASS for current local pipeline |
| Photo tier input | `src/cozmo_scan/pipeline.py` | Per-room folder and direct session-folder discovery; 7 sessions run | PARTIAL: ingestion verified, image reconstruction pending |
| Video tier input | `src/cozmo_scan/pipeline.py` | Direct MP4 file input; 15 files run | PARTIAL: ingestion verified, video reconstruction pending |
| LiDAR tier input | `src/cozmo_scan/pipeline.py` | Tier accepted by CLI | PARTIAL: no depth/pose/intrinsics processing yet |
| Common JSON output | `src/cozmo_scan/pipeline.py` | `result.json`, measurements, damage, scope | PARTIAL: deterministic starter values |
| Rendered whole-property plan | `src/cozmo_scan/pipeline.py` | `floor_plan.svg`, `floor_plan.png` | PARTIAL: generated layout, not reconstructed geometry |
| Openings and dimensions | `result.json` | Wall and opening fields | PARTIAL: placeholder measurements |
| Damage regions and concealed flags | `damage.json` | Damage fields and rule placeholder | PARTIAL: no visual detector |
| Confidence interval on measurements | `result.json` | Wall intervals | PARTIAL: intervals are not calibrated |
| Capture route | `reports/capture-protocol.md` | Stock capture instructions | PASS as protocol draft; field validation pending |
| Device matrix | `reports/device-matrix.md` | Supported hardware and accuracy table | PENDING measurement validation |
| Benchmark set | `benchmark/README.md` | Required room/capture layout | PENDING raw captures and ground truth |
| Repeatability gate | `reports/benchmark-report.md` | Repeatability table | PENDING two same-room captures |
| Drift ablation | `reports/benchmark-report.md` | On/off comparison table | PENDING real multi-room reconstruction |
| Consumer-app comparison | `reports/benchmark-report.md` | Head-to-head table | PENDING app export and measurements |
| Fix loop | `reports/fix-loop.md` | Before/after declaration | PENDING first benchmark failure |
| Reproduction bundle | `reproduction/README.md` | Re-run instructions and raw-data layout | PARTIAL: runner exists; raw data pending |
| Technical report | `reports/technical-report.md` | Six-page report structure | PARTIAL: draft template |
| Process evidence | Git history | Incremental commits | PENDING future implementation commits |

## Current honest conclusion

The repository is a reproducible starter scaffold, not yet a complete Round 1 submission. The missing work is primarily real capture ingestion, geometry/damage reconstruction, calibrated evaluation, and raw benchmark evidence.
