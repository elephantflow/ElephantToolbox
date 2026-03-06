from __future__ import annotations

import argparse

from PIL import Image
from torchvision import transforms
from transformers import CLIPImageProcessor


def handle_image_by_defined_processor(img):
    processor = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
        transforms.Normalize((0.48145466, 0.4578275, 0.40821073), (0.26862954, 0.26130258, 0.27577711)),
    ])
    return processor(img)


def handle_image_by_default_processor(img):
    processor = CLIPImageProcessor()
    return processor(images=img, return_tensors="pt").pixel_values[0]


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare image tensor for CLIP input.")
    parser.add_argument("--image_path", required=True)
    args = parser.parse_args()

    img = Image.open(args.image_path).convert("RGB")
    img1 = handle_image_by_defined_processor(img)
    img2 = handle_image_by_default_processor(img)
    print(f"img1 {img1.shape} img2 {img2.shape}")
    print(img1.max())
    print(img1.min())


if __name__ == "__main__":
    main()
