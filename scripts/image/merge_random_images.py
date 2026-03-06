from __future__ import annotations

import sys
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = None
for parent in [CURRENT_FILE.parent, *CURRENT_FILE.parents]:
    if (parent / "toolbox").is_dir():
        PROJECT_ROOT = parent
        break
if PROJECT_ROOT is None:
    PROJECT_ROOT = CURRENT_FILE.parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import argparse

from toolbox.core.images import ImageToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Create random merged images.")
    parser.add_argument("--input_folder", type=str, required=True)
    parser.add_argument("--output_folder", type=str, required=True)
    parser.add_argument("--output_count", type=int, default=30)
    parser.add_argument("--per_image_count", type=int, default=3)
    parser.add_argument("--target_height", type=int, default=1360)
    args = parser.parse_args()

    saved = ImageToolkit.build_random_merged_images(
        input_dir=args.input_folder,
        output_dir=args.output_folder,
        output_count=args.output_count,
        per_image_count=args.per_image_count,
        target_height=args.target_height,
    )
    for path in saved:
        print(f"Saved: {path}")
    print("Done!")


if __name__ == "__main__":
    main()
