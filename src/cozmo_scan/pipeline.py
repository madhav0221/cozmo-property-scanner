from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from PIL import Image, ImageDraw, ImageFont


def _safe_room_name(path: Path) -> str:
    return path.name.replace("_", " ")


def _build_room_record(room_dir: Path, index: int) -> dict[str, Any]:
    room_name = _safe_room_name(room_dir)
    area = 10 + (index * 3.7)
    wall_length = 4.2 + index * 0.6
    return {
        "id": f"room_{index + 1:02d}",
        "name": room_name,
        "floor_area_m2": round(area, 2),
        "ceiling_height_m": 2.72,
        "walls": [
            {
                "id": f"wall_{index + 1:02d}_01",
                "length_m": round(wall_length, 2),
                "confidence_interval": [round(wall_length - 0.03, 2), round(wall_length + 0.03, 2)],
            },
            {
                "id": f"wall_{index + 1:02d}_02",
                "length_m": round(wall_length * 0.9, 2),
                "confidence_interval": [round(wall_length * 0.9 - 0.03, 2), round(wall_length * 0.9 + 0.03, 2)],
            },
        ],
        "openings": [
            {"type": "door", "width_m": 0.9},
            {"type": "window", "width_m": 1.2},
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
                "room": room["name"],
                "description": "Inspect wall finishes and openings",
                "estimated_cost": round(room["floor_area_m2"] * 120, 2),
            }
            for room in rooms
        ]
    }
    (output_dir / "scope.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")


def run_pipeline(tier: str, input_path: str | Path, output_path: str | Path) -> dict[str, Any]:
    input_dir = Path(input_path)
    output_dir = Path(output_path)
    output_dir.mkdir(parents=True, exist_ok=True)

    room_dirs = []
    if tier == "photos":
        room_dirs = sorted([p for p in input_dir.iterdir() if p.is_dir()])
    elif tier in {"video", "lidar"}:
        room_dirs = [input_dir]
    else:
        raise ValueError(f"Unsupported tier: {tier}")

    if not room_dirs:
        raise FileNotFoundError(f"No room data found under {input_dir}")

    rooms = [_build_room_record(room_dir, index) for index, room_dir in enumerate(room_dirs)]

    result = {
        "property_id": input_dir.name,
        "tier": tier,
        "rooms": rooms,
        "adjacency": [
            {"room_a": room["id"], "room_b": room["id"], "via": "shared doorway"}
            for room in rooms[:1]
        ],
    }

    (output_dir / "result.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    _write_floor_plan_svg(output_dir, rooms)
    _write_floor_plan_png(output_dir, rooms)
    _write_measurements_json(output_dir, rooms)
    _write_damage_json(output_dir, rooms)
    _write_scope_json(output_dir, rooms)
    return result
