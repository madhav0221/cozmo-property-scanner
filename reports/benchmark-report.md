# Benchmark Report

This report summarizes the supplied capture dataset and the results produced by the local pipeline. Accuracy gates are marked `NOT EVALUATED` where the dataset does not contain the reference measurements needed for comparison. LiDAR runs use `depth_pose_projection`; photo and video runs use `placeholder_layout`.

## Supplied capture inventory

The three supplied archives are LiDAR-style bundles. The complete inventory is recorded in [extracted-capture-inventory.json](../benchmark/extracted-capture-inventory.json).

| Capture | Files | Size | RGB | Depth | Confidence | Poses | IMU | Intrinsics |
|---|---:|---:|---|---|---|---|---|---|
| `single_room.zip` | 3,434 | 88.5 MB | yes | yes | yes | yes | yes | yes |
| `single_scan_floor_only.zip` | 10,506 | 276.7 MB | yes | yes | yes | yes | yes | yes |
| `single_scan_with_ceiling.zip` | 19,494 | 508.4 MB | yes | yes | yes | yes | yes | yes |

## Pipeline run evidence

All three archives were run with the one-command LiDAR entry point. Each completed and emitted one room plus the contract artifacts: `result.json`, `floor_plan.svg`, `floor_plan.png`, `measurements.json`, `damage.json`, `scope.json`, `diagnostics.json`, and `point_cloud.ply`.

| Capture | Tier | Frames used | Points | Geometry status | Accuracy status |
|---|---|---:|---:|---|---|
| `single_room.zip` | LiDAR | 86 / 1,715 | 66,007 | `depth_pose_projection` | Not scored: no ground truth |
| `single_scan_floor_only.zip` | LiDAR | 263 / 5,251 | 201,984 | `depth_pose_projection` | Not scored: no ground truth |
| `single_scan_with_ceiling.zip` | LiDAR | 488 / 9,745 | 374,783 | `depth_pose_projection` | Not scored: no ground truth |

These runs verify depth-plus-pose point-cloud reconstruction and artifact generation. Dimensional accuracy, room-plane extraction, damage accuracy, and drift performance are not reported because the supplied archives do not include laser/tape measurements or a multi-room benchmark.

## Organized photo and video runs

The organized media under `captures/organized/` was processed through the same CLI entry point. The media was grouped by capture session. Room labels were left unspecified where the source filenames did not identify rooms.

| Input | Runs | Rooms emitted per run | Output artifacts per run | Geometry status |
|---|---:|---:|---:|---|
| Photo sessions | 7 | 1 | 7 | `placeholder_layout` |
| Video files | 15 | 1 | 7 | `placeholder_layout` |

The photo sessions contain 46 JPEGs and the video sessions contain 15 MP4s. These runs verify direct photo-folder and direct-video-file ingestion, common JSON generation, rendered-plan generation, measurements/damage/scope artifact generation, and one-command execution. Visual reconstruction, multi-room adjacency, and video motion estimation are outside the measured results in this report.

## Constraints and submission scope

The following dataset and scope limitations explain why some PDF deliverables are reported as `NOT EVALUATED`:

1. **Reference measurements are absent from the supplied dataset.** The capture bundles contain sensor files and media, but no laser/tape measurements for wall lengths, opening widths, ceiling heights, floor areas, damage extents, or room adjacency. Accuracy errors and gate pass/fail results therefore cannot be calculated.
2. **The supplied sensor bundles are single-room captures.** The dataset does not contain the required three-room-plus-connector property, a repeated capture of the same room, or a staged-damage benchmark. Repeatability, photo-tier whole-property stitching, and multi-room adjacency therefore cannot be scored.
3. **The photo and video sets are uncalibrated evaluation inputs.** Their source metadata does not identify room names or provide ground truth. They verify ingestion and output generation, but not visual reconstruction or motion-estimation accuracy.
4. **LiDAR processing is limited to sampled depth-plus-pose point-cloud projection.** It produces measured point-cloud bounds and a PLY artifact. Plane extraction, dimensioned room geometry, drift correction, and calibrated uncertainty are outside this implementation; generated room fields are not presented as measured geometry.
5. **The dataset contains no consumer-app export.** A head-to-head comparison requires the same rooms to be processed by a named incumbent application, with its export retained for comparison.
6. **A fix-loop result requires an evaluated failure.** Before/after metrics and a prediction can only be reported after a benchmark gate has been measured against ground truth.

Accordingly, this submission demonstrates the local CLI, direct capture ingestion, common output contract, LiDAR depth/pose point-cloud projection, generated artifacts, tests, documentation, and reproducible run structure. Accuracy, repeatability, drift performance, damage-classification performance, and consumer-app comparison are not claimed without the corresponding reference data.

## Synthetic smoke test

The current automated fixture was run through the real pipeline and produced three rooms (`bedroom`, `kitchen`, and `living room`) plus six output artifacts. The collected summary is stored in [benchmark/smoke-test-result.json](../benchmark/smoke-test-result.json). This fixture uses fake image bytes and has no laser ground truth, so it is not evidence for any Round 1 accuracy gate.

## Gate summary

| Tier | Wall length | Opening width | Ceiling height | Repeatability | Whole-property stitch | Status |
|---|---:|---:|---:|---:|---:|---|
| Photos | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | BLOCKED: no photo benchmark |
| Video | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | BLOCKED: no video benchmark |
| LiDAR | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | BLOCKED: no ground truth |

Required thresholds: photos wall lengths within +/-8%, video +/-3%, opening widths <=2 cm on >=85%, ceiling height <=1.5 cm per room, repeatability <=1 cm or 0.5% per wall, and photo footprint within +/-8% with correct adjacency and no overlaps.

## Repeatability

| Room | Tier | Capture A | Capture B | Maximum wall spread | Gate |
|---|---|---:|---:|---:|---|
| NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | BLOCKED: no repeat capture or ground truth |

## Drift ablation

| Capture | Drift correction | Footprint error | Overlaps | Adjacency errors | Evidence path |
|---|---|---:|---:|---:|---|
| NOT EVALUATED | Off | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | BLOCKED: drift correction not implemented |
| NOT EVALUATED | On | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | BLOCKED: drift correction not implemented |

Drift evaluation requires a documented correction method such as loop closure, a pose graph, or plane anchoring. Using poses as-is does not satisfy this gate.

## Head-to-head comparison

| Room | Dimension | Cozmo error | Consumer app and version | Consumer error | Winner |
|---|---|---:|---|---:|---|
| NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | BLOCKED: no consumer-app export |

Use two benchmark rooms and the same LiDAR captures for both systems.

## Timing

| Tier | Device | Capture time | Cold processing time | Output files |
|---|---|---:|---:|---|
| Photos | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED |
| Video | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED | NOT EVALUATED |
| LiDAR | Not recorded | Not recorded | Not recorded | Generated |
