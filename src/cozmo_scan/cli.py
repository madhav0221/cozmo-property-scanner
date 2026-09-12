from __future__ import annotations

import argparse
from pathlib import Path

from .pipeline import run_pipeline


def main() -> None:
    parser = argparse.ArgumentParser(description="Cozmo property scan pipeline")
    parser.add_argument("--tier", choices=["photos", "video", "lidar"], required=True)
    parser.add_argument("--input", type=str, required=True, help="Input capture directory or file")
    parser.add_argument("--output", type=str, required=True, help="Directory for generated outputs")
    args = parser.parse_args()

    result = run_pipeline(args.tier, Path(args.input), Path(args.output))
    print(f"Processed {result['property_id']} with {len(result['rooms'])} room(s)")
    print(f"Results written to {args.output}")


if __name__ == "__main__":
    main()
