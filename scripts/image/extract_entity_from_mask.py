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
from pathlib import Path

from tqdm import tqdm

from toolbox.core.images import ImageToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract foreground/background based on mask.")
    parser.add_argument("--origin_image", type=str, required=True)
    parser.add_argument("--mask_image", type=str, required=True)
    parser.add_argument("--saved_image", type=str, required=True)
    parser.add_argument("--keep_background_or_foreground", type=str, default="foreground", choices=["foreground", "background"])
    args = parser.parse_args()

    origin = Path(args.origin_image)
    mask = Path(args.mask_image)
    saved = Path(args.saved_image)

    if origin.is_file():
        ImageToolkit.get_subject_from_mask(origin, mask, saved, args.keep_background_or_foreground)
        return

    os.makedirs(saved, exist_ok=True)
    for mask_image in tqdm(sorted(mask.iterdir())):
        if not mask_image.is_file():
            continue
        frame = origin / mask_image.name.replace(".png", ".jpg")
        out = saved / mask_image.name.replace(".png", ".jpg")
        ImageToolkit.get_subject_from_mask(frame, mask_image, out, args.keep_background_or_foreground)


if __name__ == "__main__":
    main()
