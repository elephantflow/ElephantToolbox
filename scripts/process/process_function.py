from __future__ import annotations

import os
import random
from pathlib import Path

import numpy as np
from PIL import Image


DEFAULT_OUTPUT_DIR = Path(os.environ.get("TOOLBOX_OUTPUT_DIR", "./outputs/random_images"))


def _save_random_image(save_path: Path) -> str:
    save_path.parent.mkdir(parents=True, exist_ok=True)
    image_array = np.random.rand(240, 320, 3) * 255
    image = Image.fromarray(image_array.astype(np.uint8)).convert("RGB")
    image.save(save_path)
    print(f"Saving image: {save_path}")
    return str(save_path)


def save_images(image_name: str) -> str:
    return _save_random_image(DEFAULT_OUTPUT_DIR / image_name)


def save_images_clear() -> str:
    image_name = f"{str(random.randint(0, 100)).zfill(5)}.jpg"
    return _save_random_image(DEFAULT_OUTPUT_DIR / image_name)
