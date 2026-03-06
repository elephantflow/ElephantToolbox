from __future__ import annotations

import argparse

from PIL import Image
from torchvision import transforms


def processor_for_vae_input(img, height, width):
    processor = transforms.Compose([
        transforms.Resize((height, width)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ])
    return processor(img)


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare image tensor for VAE input.")
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--height", type=int, default=384)
    parser.add_argument("--width", type=int, default=256)
    args = parser.parse_args()

    img = Image.open(args.image_path).convert("RGB")
    out = processor_for_vae_input(img, args.height, args.width)
    print(out.shape)
    print(out.max())
    print(out.min())


if __name__ == "__main__":
    main()
