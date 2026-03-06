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


def images_to_video(folder1, folder2, output_file, fps=25):
    return VideoToolkit.merge_image_folders_to_video(folder1, folder2, output_file, fps=fps)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge two frame folders side-by-side into one video.")
    parser.add_argument("--folder1", type=str, required=True)
    parser.add_argument("--folder2", type=str, required=True)
    parser.add_argument("--output_file", type=str, required=True)
    parser.add_argument("--fps", type=int, default=25)
    args = parser.parse_args()

    out = images_to_video(args.folder1, args.folder2, args.output_file, fps=args.fps)
    print(f"视频已保存至 {out}")


if __name__ == "__main__":
    main()
