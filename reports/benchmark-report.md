# Benchmark Report

This report contains the verified capture inventory and pipeline-run evidence available so far. Accuracy gates are marked `NOT EVALUATED` because the supplied archives contain no laser/tape ground truth and the current geometry status is `placeholder_layout`.

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

These runs prove depth-plus-pose point-cloud reconstruction and artifact generation. They do not prove dimensional accuracy, room-plane extraction, damage accuracy, or drift performance because the archives contain no laser/tape measurements and no multi-room benchmark.

## Organized photo and video runs

The organized media under `captures/organized/` was processed through the same CLI entry point. The source media was grouped by reliable WhatsApp date/time session; room names were not inferred from filenames.

| Input | Runs | Rooms emitted per run | Output artifacts per run | Geometry status |
|---|---:|---:|---:|---|
| Photo sessions | 7 | 1 | 7 | `placeholder_layout` |
| Video files | 15 | 1 | 7 | `placeholder_layout` |

The photo sessions contain 46 JPEGs total and the video sessions contain 15 MP4s total. These runs verify direct photo-folder and direct-video-file ingestion, common JSON generation, rendered-plan generation, measurements/damage/scope artifact generation, and one-command execution. They do not yet demonstrate visual reconstruction, multi-room adjacency, or video motion estimation.

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

The final report must explain loop closure, pose graph, plane anchoring, or the actual correction method. Using poses as-is is not sufficient.

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
