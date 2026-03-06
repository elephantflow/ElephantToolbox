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


def resize_video(input_path, output_path, fixed_size):
    return VideoToolkit.resize_video(input_path, output_path, fixed_size)


def resize_and_crop_video(input_path, output_path, fixed_size, crop_size=(512, 512)):
    return VideoToolkit.resize_and_crop_video(input_path, output_path, fixed_size, crop_size)


def main() -> None:
    parser = argparse.ArgumentParser(description="Resize video, optionally with center crop.")
    parser.add_argument("--input_video_path", type=str, required=True)
    parser.add_argument("--output_video_path", type=str, required=True)
    parser.add_argument("--fixed_side_size", type=int, default=720)
    parser.add_argument("--crop_width", type=int, default=0)
    parser.add_argument("--crop_height", type=int, default=0)
    args = parser.parse_args()

    if args.crop_width > 0 and args.crop_height > 0:
        out = resize_and_crop_video(
            args.input_video_path,
            args.output_video_path,
            args.fixed_side_size,
            crop_size=(args.crop_width, args.crop_height),
        )
    else:
        out = resize_video(args.input_video_path, args.output_video_path, args.fixed_side_size)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
