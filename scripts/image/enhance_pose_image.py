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


def enhance_pose_img(pose_img, save_pth):
    return ImageToolkit.enhance_pose_image(pose_img, save_pth)


def pose_black_to_wihte(pose_img, save_pth):
    return ImageToolkit.black_to_white_background(pose_img, save_pth)


def main() -> None:
    parser = argparse.ArgumentParser(description="Enhance one pose image or all pose images in a folder.")
    parser.add_argument("--input", type=str, required=True)
    parser.add_argument("--output", type=str, required=True)
    parser.add_argument("--mode", type=str, choices=["enhance", "black_to_white"], default="enhance")
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)

    fn = enhance_pose_img if args.mode == "enhance" else pose_black_to_wihte

    if input_path.is_file():
        out = fn(input_path, output_path)
        print(f"Saved: {out}")
        return

    output_path.mkdir(parents=True, exist_ok=True)
    for file in sorted(input_path.iterdir()):
        if file.suffix.lower() in {".jpg", ".jpeg", ".png"}:
            fn(file, output_path / file.name)
    print(f"Saved folder: {output_path}")


if __name__ == "__main__":
    main()
