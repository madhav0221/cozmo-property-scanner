# Compliance Matrix

Status values: `PASS` means verified in this repository, `PARTIAL` means the interface exists but the required real-world capability is not complete, and `NOT EVALUATED` means the required benchmark evidence is not present in the supplied dataset.

| Requirement | File path | Artifact / evidence | Status |
|---|---|---|---|
| One command per capture | `src/cozmo_scan/cli.py` | `python -m cozmo_scan.cli --tier ... --input ... --output ...` | PASS for current local pipeline |
| Photo tier input | `src/cozmo_scan/pipeline.py` | Per-room folder and direct session-folder discovery; 7 sessions run | PARTIAL: ingestion verified; image reconstruction not evaluated |
| Video tier input | `src/cozmo_scan/pipeline.py` | Direct MP4 file input; 15 files run | PARTIAL: ingestion verified; video reconstruction not evaluated |
| LiDAR tier input | `src/cozmo_scan/pipeline.py` | ZIP/directory ingestion, depth/pose projection, PLY output | PARTIAL: room-plane extraction and calibrated dimensions are not complete |
| Common JSON output | `src/cozmo_scan/pipeline.py` | `result.json`, measurements, damage, scope | PARTIAL: contract fields are emitted; photo/video geometry remains placeholder |
| Rendered whole-property plan | `src/cozmo_scan/pipeline.py` | `floor_plan.svg`, `floor_plan.png` | PARTIAL: generated layout, not reconstructed geometry |
| Openings and dimensions | `result.json` | Wall and opening fields | PARTIAL: placeholder measurements |
| Damage regions and concealed flags | `damage.json` | Damage fields and rule placeholder | PARTIAL: no visual detector |
| Confidence interval on measurements | `result.json` | Wall intervals | PARTIAL: intervals are not calibrated |
| Capture route | `reports/capture-protocol.md` | Stock capture instructions | PARTIAL: protocol documented; field validation not evaluated |
| Device matrix | `reports/device-matrix.md` | Supported hardware and accuracy table | NOT EVALUATED: measurement validation absent |
| Benchmark set | `benchmark/README.md` | Required room/capture layout | NOT EVALUATED: required benchmark set absent |
| Repeatability gate | `reports/benchmark-report.md` | Repeatability table | NOT EVALUATED: no repeated room capture |
| Drift ablation | `reports/benchmark-report.md` | On/off comparison table | NOT EVALUATED: correction method not implemented |
| Consumer-app comparison | `reports/benchmark-report.md` | Head-to-head table | NOT EVALUATED: app export absent |
| Fix loop | `reports/fix-loop.md` | Before/after declaration | NOT EVALUATED: no measured gate failure |
| Reproduction bundle | `reproduction/README.md` | Re-run instructions and raw-data layout | PARTIAL: run instructions and supplied data inventory present |
| Technical report | `reports/technical-report.md` | Six-page report structure | PARTIAL: report structure provided |
| Process evidence | Git history | Incremental commits | NOT EVALUATED: history does not cover the complete build |

## Submission status

The repository is a reproducible local submission package. The remaining gaps are room-plane and damage reconstruction, calibrated evaluation, multi-room benchmark evidence, and the external comparison artifacts required by the case study.
