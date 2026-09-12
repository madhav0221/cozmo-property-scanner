import json
from pathlib import Path

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
