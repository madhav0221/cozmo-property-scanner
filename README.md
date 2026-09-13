# Cozmo Property Scanner

A lightweight property-analysis pipeline. It is intentionally designed as a local Python CLI: one capture input yields a structured result JSON and a rendered floor-plan artifact.

## Goals

- Accept a property capture in one of three modes: `photos`, `video`, or `lidar`
- Build a common output schema around room measurements, openings, adjacency, and damage placeholders
- Save `result.json`, `floor_plan.svg`, and `floor_plan.png` in an output folder
- Keep the setup simple enough to run on a fresh machine in under 15 minutes

## Quick start

1. Create a virtual environment
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   ```

2. Install the package
   ```bash
   pip install -e .
   ```

3. Run the CLI on a sample folder
   ```bash
   python -m cozmo_scan.cli --tier photos --input ./sample_capture --output ./outputs/sample_capture
   ```

## Input formats

### Photos
A folder containing room subfolders:

```text
sample_capture/
  living_room/
    001.jpg
    002.jpg
  bedroom/
    001.jpg
```

### Video
A single video file or a folder containing extracted frames.

### LiDAR
A capture folder containing point-cloud or structured capture data.

## Output

The pipeline writes the following into the selected output folder:

```text
result.json
floor_plan.svg
floor_plan.png
measurements.json
damage.json
scope.json
```

## Example result schema

```json
{
  "property_id": "sample_capture",
  "tier": "photos",
  "rooms": [
    {
      "id": "room_01",
      "name": "living_room",
      "floor_area_m2": 18.2,
      "ceiling_height_m": 2.72,
      "walls": [
        {
          "id": "wall_01",
          "length_m": 4.1,
          "confidence_interval": [4.05, 4.15]
        }
      ],
      "openings": [
        {"type": "door", "width_m": 0.9}
      ]
    }
  ]
}
```

## Current implementation status

This starter project delivers a deterministic CLI contract and sample floor-plan rendering so the repo is immediately usable and testable. It intentionally avoids heavy geometry libraries and focuses on an implementation that is easy to extend for real vision pipelines later.
