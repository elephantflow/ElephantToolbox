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

from toolbox.core.experimental import ExperimentalToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Detect hands on an image using MediaPipe.")
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--output_path", default=None)
    parser.add_argument("--max_num_hands", type=int, default=2)
    args = parser.parse_args()

    result = ExperimentalToolkit.detect_hands(args.image_path, args.output_path, max_num_hands=args.max_num_hands)
    if args.output_path:
        print(f"Saved: {result}")


if __name__ == "__main__":
    main()
