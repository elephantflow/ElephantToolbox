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

from toolbox.core.gifs import GifToolkit


def read_using_imageio(input_file: str, output_dir: str):
    return GifToolkit.gif_to_frames(input_file, output_dir)


def read_using_image(input_file: str, output_dir: str):
    return GifToolkit.gif_to_frames(input_file, output_dir)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract frames from gif.")
    parser.add_argument("--input_file", type=str, required=True)
    parser.add_argument("--output_dir", type=str, required=True)
    args = parser.parse_args()

    saved = read_using_imageio(args.input_file, args.output_dir)
    print(f"Saved {len(saved)} frames to {args.output_dir}")


if __name__ == "__main__":
    main()
