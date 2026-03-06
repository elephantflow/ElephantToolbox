from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def crop_center_same_height_width(image_path):
    img = Image.open(image_path)
    width, height = img.size
    short_side = min(width, height)
    left = (width - short_side) // 2
    top = (height - short_side) // 2
    return img.crop((left, top, left + short_side, top + short_side)).convert("RGB")


def adjust_and_crop_height_large(image_path):
    img = Image.open(image_path)
    width, height = img.size
    new_height = 1920
    new_width = int((new_height / height) * width)
    img_resized = img.resize((new_width, new_height))
    target_width = int(new_height / 1.77)
    left = (new_width - target_width) // 2
    return img_resized.crop((left, 0, left + target_width, new_height)).convert("RGB")


def vertical_video_adjust_and_crop_height_large(image_path):
    img = Image.open(image_path)
    width, height = img.size
    new_width = 1920
    new_height = int((new_width / width) * height)
    img_resized = img.resize((new_width, new_height))
    target_height = int(new_width / 1.77)
    top = (new_height - target_height) // 2
    return img_resized.crop((0, top, new_width, top + target_height)).convert("RGB")


def main() -> None:
    parser = argparse.ArgumentParser(description="Batch crop images to target ratio/size.")
    parser.add_argument("--image_dir", required=True)
    parser.add_argument("--save_dir", required=True)
    args = parser.parse_args()

    image_dir = Path(args.image_dir)
    save_dir = Path(args.save_dir)
    save_dir.mkdir(parents=True, exist_ok=True)

    for image in sorted(image_dir.iterdir()):
        if image.name.startswith('.') or not image.is_file():
            continue
        img = Image.open(image)
        width, height = img.size
        if height / width < 1.3:
            cropped = vertical_video_adjust_and_crop_height_large(image)
        else:
            cropped = adjust_and_crop_height_large(image)
        cropped.save(save_dir / image.name)


if __name__ == "__main__":
    main()
