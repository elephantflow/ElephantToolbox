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
    parser = argparse.ArgumentParser(description="Merge videos in one folder horizontally and append reversed segment.")
    parser.add_argument("--video_dir", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--skip_frames", type=int, default=2)
    parser.add_argument("--fps", type=int, default=30)
    args = parser.parse_args()

    out = ExperimentalToolkit.merge_videos_side_by_side(args.video_dir, args.output_path, args.skip_frames, args.fps)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
