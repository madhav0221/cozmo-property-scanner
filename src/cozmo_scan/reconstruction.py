from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image


def _rotation_from_quaternion(qx: float, qy: float, qz: float, qw: float) -> np.ndarray:
    norm = np.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)
    qx, qy, qz, qw = qx / norm, qy / norm, qz / norm, qw / norm
    return np.array(
        [
            [1 - 2 * (qy * qy + qz * qz), 2 * (qx * qy - qz * qw), 2 * (qx * qz + qy * qw)],
            [2 * (qx * qy + qz * qw), 1 - 2 * (qx * qx + qz * qz), 2 * (qy * qz - qx * qw)],
            [2 * (qx * qz - qy * qw), 2 * (qy * qz + qx * qw), 1 - 2 * (qx * qx + qy * qy)],
        ],
        dtype=np.float32,
    )


def _write_ply(path: Path, points: np.ndarray) -> None:
    with path.open("w", encoding="ascii") as output:
        output.write("ply\nformat ascii 1.0\n")
        output.write(f"element vertex {len(points)}\n")
        output.write("property float x\nproperty float y\nproperty float z\nend_header\n")
        np.savetxt(output, points, fmt="%.5f")


def reconstruct_lidar(input_dir: Path, output_dir: Path, frame_stride: int = 20, pixel_stride: int = 8) -> dict[str, Any]:
    depth_dir = input_dir / "depth"
    odometry_path = input_dir / "odometry.csv"
    depth_paths = sorted(depth_dir.glob("*.png"))
    if not depth_paths or not odometry_path.exists():
        raise FileNotFoundError("LiDAR reconstruction needs depth/*.png and odometry.csv")

    with odometry_path.open(newline="", encoding="utf-8") as source:
        reader = csv.DictReader(source)
        odometry = {
            normalized["frame"]: normalized
            for row in reader
            if (normalized := {key.strip(): value.strip() for key, value in row.items() if key is not None and value is not None})
        }

    sample = np.asarray(Image.open(depth_paths[0]))
    height, width = sample.shape
    fx_rgb = float(next(iter(odometry.values()))["fx"])
    fy_rgb = float(next(iter(odometry.values()))["fy"])
    cx_rgb = float(next(iter(odometry.values()))["cx"])
    cy_rgb = float(next(iter(odometry.values()))["cy"])
    rgb_width = max(width, int(round(cx_rgb * 2)))
    rgb_height = max(height, int(round(cy_rgb * 2)))
    scale_x = width / rgb_width
    scale_y = height / rgb_height
    fx, fy = fx_rgb * scale_x, fy_rgb * scale_y
    cx, cy = cx_rgb * scale_x, cy_rgb * scale_y

    rows, columns = np.mgrid[0:height:pixel_stride, 0:width:pixel_stride]
    pixels_x = (columns.astype(np.float32) - cx) / fx
    pixels_y = (rows.astype(np.float32) - cy) / fy
    point_sets = []
    used_frames = 0
    for depth_path in depth_paths[::frame_stride]:
        row = odometry.get(depth_path.stem)
        if row is None:
            continue
        depth_m = np.asarray(Image.open(depth_path), dtype=np.float32)[::pixel_stride, ::pixel_stride] / 1000.0
        valid = (depth_m > 0.1) & (depth_m < 10.0)
        camera_points = np.stack((pixels_x * depth_m, pixels_y * depth_m, depth_m), axis=-1)[valid]
        if not len(camera_points):
            continue
        rotation = _rotation_from_quaternion(*(float(row[key]) for key in ("qx", "qy", "qz", "qw")))
        translation = np.array([float(row[axis]) for axis in ("x", "y", "z")], dtype=np.float32)
        point_sets.append(camera_points @ rotation.T + translation)
        used_frames += 1

    if not point_sets:
        raise ValueError("No valid depth/odometry pairs were reconstructed")
    points = np.concatenate(point_sets, axis=0)
    _write_ply(output_dir / "point_cloud.ply", points)
    minimum = points.min(axis=0)
    maximum = points.max(axis=0)
    return {
        "status": "depth_pose_projection",
        "frames_available": len(depth_paths),
        "frames_used": used_frames,
        "points": len(points),
        "frame_stride": frame_stride,
        "pixel_stride": pixel_stride,
        "depth_unit": "millimetres converted to metres",
        "camera_intrinsics_scaled_to_depth": [round(float(fx), 4), round(float(fy), 4), round(float(cx), 4), round(float(cy), 4)],
        "world_bounds_m": {
            "min": [round(float(value), 4) for value in minimum],
            "max": [round(float(value), 4) for value in maximum],
        },
    }