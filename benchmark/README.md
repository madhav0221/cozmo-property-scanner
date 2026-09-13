# Benchmark Set

The assignment provides no captures, so the benchmark must be built and committed or supplied as a separate raw-data bundle.

## Required composition

```text
benchmark/raw/
  multi_room/
    photos/
      living_room/       # 2-8 original iPhone stills
      kitchen/
      hallway/
      capture_metadata.json
    video/original_walkthrough.mov
    lidar/
      rgb/
      depth/
      poses.csv
      intrinsics.json
      capture_metadata.json
  furnished_damage/
    photos/
    video/
    lidar/
  repeatability/
    room_01_capture_a/
    room_01_capture_b/
  ground_truth/
    multi_room_measurements.json
    furnished_damage_measurements.json
    repeatability_measurements.json
```

The multi-room set must contain at least three rooms plus a connector. The furnished room must include staged damage from two classes. The same rooms must be captured at all three tiers, and at least one room must be captured twice at the same tier.

## Ground truth

Measure wall lengths, opening widths, ceiling height, room footprint, adjacency, and staged damage extents with a laser measurer or tape. Store the raw measurements, operator, instrument, date, and units. Keep the original sensor files and any consumer-app export beside the measurements.

## Running one capture

```powershell
python -m cozmo_scan.cli --tier photos --input .\benchmark\raw\multi_room\photos --output .\benchmark\runs\multi_room_photos
```

The benchmark report must be generated from the resulting JSON, not typed manually.
