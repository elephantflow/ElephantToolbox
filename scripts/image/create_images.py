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
    parser = argparse.ArgumentParser(description="Create a black RGB image.")
    parser.add_argument("--width", type=int, default=384)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--output_path", type=str, default="./output.jpg")
    args = parser.parse_args()

    output = ImageToolkit.create_black_image(args.width, args.height, args.output_path)
    print(f"Saved: {output}")


if __name__ == "__main__":
    main()
