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
    parser = argparse.ArgumentParser(description="Merge many videos into a grid and export forward+reverse video.")
    parser.add_argument("--input_folder", required=True)
    parser.add_argument("--output_file", required=True)
    parser.add_argument("--videos_per_row", type=int, default=8)
    parser.add_argument("--rows", type=int, default=3)
    parser.add_argument("--fps", type=float, default=15.0)
    args = parser.parse_args()

    out = ExperimentalToolkit.merge_videos_grid(
        args.input_folder,
        args.output_file,
        videos_per_row=args.videos_per_row,
        rows=args.rows,
        fps=args.fps,
    )
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
