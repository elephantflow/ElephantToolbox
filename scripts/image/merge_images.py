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

from toolbox.core.images import ImageToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Concatenate all images in a folder horizontally.")
    parser.add_argument("--image_folder", type=str, required=True)
    parser.add_argument("--output_path", type=str, default=None)
    args = parser.parse_args()

    image_folder = Path(args.image_folder)
    image_paths = ImageToolkit.list_images(image_folder)
    output_path = Path(args.output_path) if args.output_path else image_folder / "result.jpg"
    output = ImageToolkit.merge_horizontally(image_paths, output_path)
    print(f"拼接完成，保存路径为：{output}")


if __name__ == "__main__":
    main()
