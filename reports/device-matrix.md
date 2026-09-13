# Device Matrix

Accuracy values are reported only after comparison with laser/tape ground truth.

| Tier | Capture hardware | Capture software | Required raw data | Current implementation | Accuracy |
|---|---|---|---|---|---|
| Photos | iPhone 15 or newer | Native Camera | Original stills, room folders | Folder ingestion only | NOT EVALUATED: ground truth absent |
| Video | iPhone 15 or newer | Native Camera | Original walkthrough clip | File ingestion only | NOT EVALUATED: ground truth absent |
| LiDAR | Pro-class iPhone with LiDAR | Named logging app/version required | RGB, depth, poses, intrinsics, timestamps, confidence | Depth/pose projection and PLY output | NOT EVALUATED: ground truth absent |

For a measured benchmark, add one row per tested device with OS version, capture settings, room count, and wall/opening/ceiling errors.
