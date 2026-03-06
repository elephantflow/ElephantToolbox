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
    parser = argparse.ArgumentParser(description="Blacken video borders.")
    parser.add_argument("--video_path", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--border_size", type=int, default=200)
    parser.add_argument("--max_frames", type=int, default=0)
    args = parser.parse_args()

    out = ExperimentalToolkit.blacken_video_edges(
        args.video_path,
        args.output_path,
        border_size=args.border_size,
        max_frames=(args.max_frames if args.max_frames > 0 else None),
    )
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
