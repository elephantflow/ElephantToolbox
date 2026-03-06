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
import os

from tqdm import tqdm

from toolbox.core.images import ImageToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert jpg/jpeg images in a folder to png format.")
    parser.add_argument("--image_dir", type=str, required=True)
    args = parser.parse_args()

    image_dir = Path(args.image_dir)
    jpgs = sorted([p for p in image_dir.iterdir() if p.suffix.lower() in {".jpg", ".jpeg"}])

    save_dir = image_dir.parent / f"{image_dir.name}_png"
    os.makedirs(save_dir, exist_ok=True)

    for image in tqdm(jpgs):
        out = save_dir / f"{image.stem}.png"
        ImageToolkit.jpg_to_png(image, out)


if __name__ == "__main__":
    main()
