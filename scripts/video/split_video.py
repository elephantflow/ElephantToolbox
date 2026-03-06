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

from toolbox.core.videos import VideoToolkit


def split_video(input_path, start_time, end_time, output_path):
    return VideoToolkit.split_video_with_moviepy(input_path, start_time, end_time, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Split one video by time range.")
    parser.add_argument("--input_video_path", type=str, required=True)
    parser.add_argument("--output_video_path", type=str, required=True)
    parser.add_argument("--start_time", type=float, required=True)
    parser.add_argument("--end_time", type=float, required=True)
    args = parser.parse_args()

    out = split_video(args.input_video_path, args.start_time, args.end_time, args.output_video_path)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
