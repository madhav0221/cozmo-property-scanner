# Stock Capture Protocol

## Route

Use the native iPhone Camera app for photos and video. Use an iPhone Pro-class LiDAR logging app that exports depth, poses, and camera intrinsics for the LiDAR tier. The exact LiDAR app and version must be recorded in `reports/device-matrix.md` before a defense run.

## Photos tier

1. Use an iPhone 15 or newer.
2. Create one folder per room using stable names such as `living_room`, `hallway`, and `bedroom_01`.
3. Take 2 to 8 still photographs per room.
4. Stand at different corners and aim at wall intersections, doors, and windows.
5. Keep the phone upright, level, and approximately 1.2 to 1.7 m above the floor.
6. Keep the full wall and floor visible where possible. Avoid zoom, portrait mode, flash, mirrors, and people blocking surfaces.
7. Do not move furniture between rooms or captures.
8. Copy the room folders into one capture directory and pass that directory to the CLI.

## Video tier

1. Use an iPhone 15 or newer and the native Camera app.
2. Record one continuous 4K/30 walkthrough, about 10 to 20 seconds per room.
3. Start at the entrance, walk slowly around the perimeter, and pause at each opening.
4. Keep the phone upright and point toward walls and floor intersections.
5. Avoid rapid rotation, motion blur, zoom, reflective-only views, and blocked doorways.
6. Export the original clip without messaging-app compression.

## LiDAR tier

1. Use a Pro-class iPhone with LiDAR.
2. Record depth, RGB frames, poses, timestamps, and camera intrinsics with the selected logging app.
3. Walk slowly around the property, revisit the starting area for loop closure, and pause at room connections.
4. Export the raw sensor bundle without resampling or deleting confidence data.

## Handoff

Copy the capture to the machine running the pipeline. Record device model, OS version, app name/version, capture duration, and any known obstruction in a `capture_metadata.json` file. Run one command per capture as described in `reproduction/README.md`.
