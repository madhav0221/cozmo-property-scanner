# Reproduction Bundle

This directory documents the files needed to regenerate every reported number without calling Cozmo infrastructure.

## Fresh machine

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e .
python -m pip install pytest
python -m pytest -q
```

## One command per capture

```powershell
python -m cozmo_scan.cli --tier photos --input .\benchmark\raw\multi_room\photos --output .\benchmark\runs\multi_room_photos
python -m cozmo_scan.cli --tier video --input .\benchmark\raw\multi_room\video --output .\benchmark\runs\multi_room_video
python -m cozmo_scan.cli --tier lidar --input .\benchmark\raw\multi_room\lidar --output .\benchmark\runs\multi_room_lidar
```

Each output folder must retain `result.json`, rendered plans, measurements, damage, scope, diagnostics, and the command metadata used to create it. LiDAR runs additionally retain `point_cloud.ply` and depth/pose reconstruction diagnostics. Photo and video runs retain the common contract while their geometry status remains explicitly marked in the result.
