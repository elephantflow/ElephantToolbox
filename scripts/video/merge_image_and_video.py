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


def combine_videos_with_image(video1_path, video2_path, image_path, output_path):
    return VideoToolkit.combine_videos_with_image(video1_path, video2_path, image_path, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge two videos with one static image in the middle.")
    parser.add_argument("--video1_path", type=str, required=True)
    parser.add_argument("--video2_path", type=str, required=True)
    parser.add_argument("--image_path", type=str, required=True)
    parser.add_argument("--output_path", type=str, required=True)
    args = parser.parse_args()

    out = combine_videos_with_image(args.video1_path, args.video2_path, args.image_path, args.output_path)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
