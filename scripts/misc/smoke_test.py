"""Simple smoke test for frame extraction utilities."""

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
from pathlib import Path

from toolbox.core.videos import VideoToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract all frames from one video for quick debugging.")
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--save_root", type=str, required=True)
    args = parser.parse_args()

    out_dir = Path(args.save_root)
    saved = VideoToolkit.extract_frames(args.video_path, out_dir, only_first=False)
    print(f"Saved {len(saved)} frames to {out_dir}")


if __name__ == "__main__":
    main()
