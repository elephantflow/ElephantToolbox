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
    parser = argparse.ArgumentParser(description="Center-crop video (square or custom width/height).")
    parser.add_argument("--video_path", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--crop_size", type=int, default=0, help="Square crop size. If >0, overrides width/height.")
    parser.add_argument("--crop_width", type=int, default=0, help="Custom crop width.")
    parser.add_argument("--crop_height", type=int, default=0, help="Custom crop height.")
    args = parser.parse_args()

    if args.crop_size > 0:
        out = ExperimentalToolkit.crop_video_center_square(args.video_path, args.output_path, crop_size=args.crop_size)
    else:
        crop_width = args.crop_width if args.crop_width > 0 else None
        crop_height = args.crop_height if args.crop_height > 0 else None
        out = ExperimentalToolkit.crop_video_center(
            args.video_path,
            args.output_path,
            crop_width=crop_width,
            crop_height=crop_height,
        )
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
