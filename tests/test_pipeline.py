import json
import zipfile
from pathlib import Path

import numpy as np
from PIL import Image

from cozmo_scan.pipeline import run_pipeline


def test_run_pipeline_creates_result_and_floorplan(tmp_path):
    capture_dir = tmp_path / "property_demo"
    (capture_dir / "living_room").mkdir(parents=True)
    (capture_dir / "bedroom").mkdir(parents=True)
    (capture_dir / "kitchen").mkdir(parents=True)

    for room_dir in [capture_dir / "living_room", capture_dir / "bedroom", capture_dir / "kitchen"]:
        for idx in range(3):
            (room_dir / f"{idx:03d}.jpg").write_bytes(b"fake image")

    output_dir = tmp_path / "outputs" / "property_demo"
    result = run_pipeline("photos", capture_dir, output_dir)

    assert result["tier"] == "photos"
    assert len(result["rooms"]) == 3
    assert result["rooms"][0]["name"] in {"living_room", "bedroom", "kitchen"}

    result_path = output_dir / "result.json"
    floor_svg = output_dir / "floor_plan.svg"
    floor_png = output_dir / "floor_plan.png"

    assert result_path.exists()
    assert floor_svg.exists()
    assert floor_png.exists()

    payload = json.loads(result_path.read_text())
    assert payload["property_id"] == "property_demo"
    assert payload["rooms"]


def test_run_pipeline_accepts_lidar_zip(tmp_path):
    capture_dir = tmp_path / "single_scan"
    capture_dir.mkdir()
    (capture_dir / "rgb.mp4").write_bytes(b"video")
    (capture_dir / "odometry.csv").write_text(
        "timestamp,frame,x,y,z,qx,qy,qz,qw,fx,fy,cx,cy\n"
        "0,000001,0,0,0,0,0,0,1,100,100,128,96\n"
    )
    (capture_dir / "imu.csv").write_text("timestamp,ax,ay,az\n0,0,0,0\n")
    (capture_dir / "camera_matrix.csv").write_text("1,0,0\n0,1,0\n0,0,1\n")
    (capture_dir / "depth").mkdir()
    (capture_dir / "confidence").mkdir()
    Image.fromarray(np.full((192, 256), 1000, dtype=np.uint16)).save(capture_dir / "depth" / "000001.png")
    Image.fromarray(np.full((192, 256), 255, dtype=np.uint16)).save(capture_dir / "confidence" / "000001.png")

    zip_path = tmp_path / "single_scan.zip"
    with zipfile.ZipFile(zip_path, "w") as archive:
        for path in capture_dir.rglob("*"):
            if path.is_file():
                archive.write(path, path.relative_to(capture_dir))

    result = run_pipeline("lidar", zip_path, tmp_path / "outputs")

    assert result["input_summary"]["signals_present"] == {
        "rgb_video": True,
        "depth": True,
        "confidence": True,
        "poses": True,
        "imu": True,
        "intrinsics": True,
    }
    assert result["stitched_plan"]["geometry_status"] == "depth_pose_projection"
    assert (tmp_path / "outputs" / "point_cloud.ply").exists()


def test_run_pipeline_accepts_direct_photo_folder_and_video_file(tmp_path):
    photo_dir = tmp_path / "photo_session"
    photo_dir.mkdir()
    (photo_dir / "photo_001.jpeg").write_bytes(b"photo")
    photo_result = run_pipeline("photos", photo_dir, tmp_path / "photo_output")

    video_path = tmp_path / "walkthrough.mp4"
    video_path.write_bytes(b"video")
    video_result = run_pipeline("video", video_path, tmp_path / "video_output")

    assert photo_result["rooms"][0]["name"] == "photo session"
    assert photo_result["input_summary"]["file_count"] == 1
    assert video_result["input_summary"]["signals_present"]["rgb_video"] is True
    assert video_result["rooms"][0]["name"] == "walkthrough"
