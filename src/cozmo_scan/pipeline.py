from __future__ import annotations

import json
import tempfile
import zipfile
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw

from .reconstruction import reconstruct_lidar


def _safe_room_name(path: Path) -> str:
    return path.stem.replace("_", " ") if path.is_file() else path.name.replace("_", " ")


def _interval(value: float, half_width: float) -> list[float]:
    return [round(value - half_width, 3), round(value + half_width, 3)]


def _build_room_record(room_dir: Path, index: int) -> dict[str, Any]:
    room_name = _safe_room_name(room_dir)
    area = 10 + (index * 3.7)
    wall_length = 4.2 + index * 0.6
    ceiling_height = 2.72
    wall_01 = {
        "id": f"wall_{index + 1:02d}_01",
        "surface_id": f"surface_{index + 1:02d}_wall_01",
        "length_m": round(wall_length, 2),
        "confidence_interval": _interval(wall_length, 0.03),
    }
    wall_02_length = wall_length * 0.9
    wall_02 = {
        "id": f"wall_{index + 1:02d}_02",
        "surface_id": f"surface_{index + 1:02d}_wall_02",
        "length_m": round(wall_02_length, 2),
        "confidence_interval": _interval(wall_02_length, 0.03),
    }
    openings = [
        {
            "id": f"opening_{index + 1:02d}_01",
            "type": "door",
            "width_m": 0.9,
            "confidence_interval": _interval(0.9, 0.02),
            "surface_id": wall_01["surface_id"],
        },
        {
            "id": f"opening_{index + 1:02d}_02",
            "type": "window",
            "width_m": 1.2,
            "confidence_interval": _interval(1.2, 0.02),
            "surface_id": wall_02["surface_id"],
        },
    ]
    return {
        "id": f"room_{index + 1:02d}",
        "name": room_name,
        "floor_area_m2": round(area, 2),
        "floor_area_confidence_interval_m2": _interval(area, 0.5),
        "ceiling_height_m": ceiling_height,
        "ceiling_height_confidence_interval_m": _interval(ceiling_height, 0.015),
        "walls": [wall_01, wall_02],
        "openings": openings,
        "surfaces": [
            {"id": wall_01["surface_id"], "type": "wall", "wall_id": wall_01["id"]},
            {"id": wall_02["surface_id"], "type": "wall", "wall_id": wall_02["id"]},
            {"id": f"surface_{index + 1:02d}_floor", "type": "floor"},
            {"id": f"surface_{index + 1:02d}_ceiling", "type": "ceiling"},
        ],
        "damage_regions": [
            {
                "id": f"damage_{index + 1:02d}_01",
                "surface_id": wall_01["surface_id"],
                "class": "surface_finish",
                "extent_m2": round(area * 0.08, 2),
                "extent_confidence_interval_m2": _interval(area * 0.08, 0.1),
            }
        ],
        "concealed_damage_flags": [
            {
                "surface_id": wall_01["surface_id"],
                "flag": False,
                "rule": "no concealed-damage evidence available from current capture",
            }
        ],
        "scope_line_items": [
            {
                "id": f"scope_{index + 1:02d}_01",
                "surface_id": wall_01["surface_id"],
                "description": "Inspect wall finish and opening perimeter",
                "estimated_cost": round(area * 120, 2),
            }
        ],
    }


def _write_floor_plan_svg(output_dir: Path, rooms: list[dict[str, Any]]) -> None:
    width = 860
    height = 520
    padding = 40
    svg = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<rect width="100%" height="100%" fill="#f3f4f6"/>',
    ]

    for index, room in enumerate(rooms):
        x0 = padding + (index % 3) * 250
        y0 = padding + (index // 3) * 180
        rect_x = x0
        rect_y = y0
        rect_w = 180
        rect_h = 120
        svg.append(f'<rect x="{rect_x}" y="{rect_y}" width="{rect_w}" height="{rect_h}" rx="12" fill="#dbeafe" stroke="#1d4ed8" stroke-width="2"/>')
        svg.append(f'<text x="{rect_x + 12}" y="{rect_y + 28}" font-family="Arial, sans-serif" font-size="18" fill="#111827">{room["name"]}</text>')
        svg.append(f'<text x="{rect_x + 12}" y="{rect_y + 60}" font-family="Arial, sans-serif" font-size="14" fill="#374151">{room["floor_area_m2"]} m²</text>')
        svg.append(f'<text x="{rect_x + 12}" y="{rect_y + 82}" font-family="Arial, sans-serif" font-size="14" fill="#374151">Ceiling {room["ceiling_height_m"]} m</text>')

    svg.append('</svg>')
    (output_dir / "floor_plan.svg").write_text("\n".join(svg), encoding="utf-8")


def _write_floor_plan_png(output_dir: Path, rooms: list[dict[str, Any]]) -> None:
    image = Image.new("RGB", (860, 520), color=(243, 244, 246))
    draw = ImageDraw.Draw(image)
    for index, room in enumerate(rooms):
        x0 = 40 + (index % 3) * 250
        y0 = 40 + (index // 3) * 180
        draw.rounded_rectangle((x0, y0, x0 + 180, y0 + 120), radius=12, fill=(219, 234, 254), outline=(29, 78, 216), width=2)
        draw.text((x0 + 12, y0 + 12), room["name"], fill=(17, 24, 39))
        draw.text((x0 + 12, y0 + 42), f"{room['floor_area_m2']} m²", fill=(55, 65, 81))
        draw.text((x0 + 12, y0 + 62), f"Ceiling {room['ceiling_height_m']} m", fill=(55, 65, 81))
    image.save(output_dir / "floor_plan.png")


def _write_measurements_json(output_dir: Path, rooms: list[dict[str, Any]]) -> None:
    payload = {
        "rooms": [
            {
                "id": room["id"],
                "name": room["name"],
                "floor_area_m2": room["floor_area_m2"],
                "ceiling_height_m": room["ceiling_height_m"],
                "walls": room["walls"],
            }
            for room in rooms
        ]
    }
    (output_dir / "measurements.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_damage_json(output_dir: Path, rooms: list[dict[str, Any]]) -> None:
    payload = {
        "damage_regions": [
            {
                "room": room["name"],
                "severity": "low",
                "area_m2": round(room["floor_area_m2"] * 0.08, 2),
                "concealed_damage": False,
            }
            for room in rooms
        ]
    }
    (output_dir / "damage.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _write_scope_json(output_dir: Path, rooms: list[dict[str, Any]]) -> None:
    payload = {
        "scope_line_items": [
            {
                "room_id": room["id"],
                **item,
            }
            for room in rooms for item in room["scope_line_items"]
        ]
    }
    (output_dir / "scope.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def _prepare_input(input_path: Path) -> tuple[Path, tempfile.TemporaryDirectory[str] | None]:
    if input_path.suffix.lower() != ".zip":
        return input_path, None

    temporary_dir = tempfile.TemporaryDirectory()
    with zipfile.ZipFile(input_path) as archive:
        archive.extractall(temporary_dir.name)
    extracted = Path(temporary_dir.name)
    directories = [path for path in extracted.iterdir() if path.is_dir()]
    return directories[0] if len(directories) == 1 else extracted, temporary_dir


def _collect_input_summary(input_dir: Path) -> dict[str, Any]:
    files = [input_dir] if input_dir.is_file() else [path for path in input_dir.rglob("*") if path.is_file()]
    extensions: dict[str, int] = {}
    for path in files:
        extensions[path.suffix.lower() or "<none>"] = extensions.get(path.suffix.lower() or "<none>", 0) + 1
    return {
        "file_count": len(files),
        "total_bytes": sum(path.stat().st_size for path in files),
        "extensions": extensions,
        "signals_present": {
            "rgb_video": input_dir.is_file() and input_dir.suffix.lower() == ".mp4" or (input_dir / "rgb.mp4").exists(),
            "depth": (input_dir / "depth").is_dir() if input_dir.is_dir() else False,
            "confidence": (input_dir / "confidence").is_dir() if input_dir.is_dir() else False,
            "poses": (input_dir / "odometry.csv").exists() if input_dir.is_dir() else False,
            "imu": (input_dir / "imu.csv").exists() if input_dir.is_dir() else False,
            "intrinsics": (input_dir / "camera_matrix.csv").exists() if input_dir.is_dir() else False,
        },
    }


def run_pipeline(tier: str, input_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    source_path = Path(input_path)
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)
    input_dir, temporary_dir = _prepare_input(source_path)

    try:
        room_dirs = []
        if tier == "photos":
            room_dirs = sorted([p for p in input_dir.iterdir() if p.is_dir()])
            if not room_dirs and any(input_dir.glob("*.jpg")) or not room_dirs and any(input_dir.glob("*.jpeg")):
                room_dirs = [input_dir]
        elif tier in {"video", "lidar"}:
            room_dirs = [input_dir]
        else:
            raise ValueError(f"Unsupported tier: {tier}")

        if not room_dirs:
            raise FileNotFoundError(f"No room data found under {input_dir}")

        rooms = [_build_room_record(room_dir, index) for index, room_dir in enumerate(room_dirs)]
        reconstruction = None
        if tier == "lidar":
            reconstruction = reconstruct_lidar(input_dir, output_dir)
        adjacency = [
            {"room_a": rooms[index - 1]["id"], "room_b": room["id"], "via": "shared doorway"}
            for index, room in enumerate(rooms) if index > 0
        ]
        result = {
            "schema_version": "round1-contract-draft-1",
            "property_id": source_path.stem if source_path.suffix.lower() == ".zip" else input_dir.name,
            "tier": tier,
            "implementation_status": "contract_and_ingestion_scaffold; reconstruction_pending",
            "input_summary": _collect_input_summary(input_dir),
            "rooms": rooms,
            "stitched_plan": {
                "room_ids": [room["id"] for room in rooms],
                "adjacency": adjacency,
                "overlaps_detected": False,
                "geometry_status": reconstruction["status"] if reconstruction else "placeholder_layout",
            },
            "adjacency": adjacency,
            "uncertainty_status": "intervals are draft placeholders until calibrated against ground truth",
            "reconstruction": reconstruction,
        }

        (output_dir / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        _write_floor_plan_svg(output_dir, rooms)
        _write_floor_plan_png(output_dir, rooms)
        _write_measurements_json(output_dir, rooms)
        _write_damage_json(output_dir, rooms)
        _write_scope_json(output_dir, rooms)
        (output_dir / "diagnostics.json").write_text(
            json.dumps({"input": result["input_summary"], "reconstruction": reconstruction}, indent=2),
            encoding="utf-8",
        )
        return result
    finally:
        if temporary_dir is not None:
            temporary_dir.cleanup()
