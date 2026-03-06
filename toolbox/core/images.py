from __future__ import annotations

import random
from pathlib import Path
from typing import Iterable, Sequence

import cv2
import numpy as np
from PIL import Image


class ImageToolkit:
    """Reusable image operations for CLI scripts and library use."""

    IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}

    @classmethod
    def list_images(cls, input_dir: str | Path) -> list[Path]:
        base = Path(input_dir)
        return sorted([p for p in base.iterdir() if p.is_file() and p.suffix.lower() in cls.IMAGE_EXTS])

    @staticmethod
    def resize_to_height(image: Image.Image, target_height: int) -> Image.Image:
        width, height = image.size
        if height == 0:
            raise ValueError("Image height cannot be zero.")
        scale = target_height / height
        return image.resize((max(1, int(width * scale)), target_height), Image.LANCZOS)

    @staticmethod
    def merge_horizontally(image_paths: Sequence[str | Path], output_path: str | Path) -> Path:
        if not image_paths:
            raise ValueError("image_paths cannot be empty.")

        images = [Image.open(path).convert("RGB") for path in image_paths]
        _, heights = zip(*(img.size for img in images))
        target_height = min(heights)

        resized_images = []
        for img in images:
            w, h = img.size
            if h == target_height:
                resized_images.append(img)
                continue
            scale = target_height / h
            resized_images.append(img.resize((max(1, int(w * scale)), target_height), Image.LANCZOS))

        total_width = sum(img.width for img in resized_images)
        merged = Image.new("RGB", (total_width, target_height))

        offset = 0
        for img in resized_images:
            merged.paste(img, (offset, 0))
            offset += img.width

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        merged.save(output)
        return output

    @staticmethod
    def crop_to_aspect_ratio(image: Image.Image, target_ratio: tuple[int, int] = (16, 9)) -> Image.Image:
        width, height = image.size
        target_w = int(height * target_ratio[0] / target_ratio[1])
        if target_w <= width:
            left = (width - target_w) // 2
            return image.crop((left, 0, left + target_w, height))

        target_h = int(width * target_ratio[1] / target_ratio[0])
        top = max(0, (height - target_h) // 2)
        return image.crop((0, top, width, top + target_h))

    @classmethod
    def build_random_merged_images(
        cls,
        input_dir: str | Path,
        output_dir: str | Path,
        output_count: int = 30,
        per_image_count: int = 3,
        target_height: int = 1360,
        target_ratio: tuple[int, int] = (16, 9),
    ) -> list[Path]:
        image_paths = cls.list_images(input_dir)
        if len(image_paths) < per_image_count:
            raise ValueError(f"Need at least {per_image_count} images in {input_dir}.")

        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        saved: list[Path] = []

        for i in range(output_count):
            selected = random.sample(image_paths, per_image_count)
            resized = [cls.resize_to_height(Image.open(path).convert("RGB"), target_height) for path in selected]
            merged = Image.new("RGB", (sum(img.width for img in resized), target_height))

            offset = 0
            for img in resized:
                merged.paste(img, (offset, 0))
                offset += img.width

            merged = cls.crop_to_aspect_ratio(merged, target_ratio)
            save_path = output / f"merged_{i + 1:02d}.jpg"
            merged.save(save_path)
            saved.append(save_path)

        return saved

    @staticmethod
    def png_to_jpg(png_image_path: str | Path, save_jpg_path: str | Path) -> Path:
        image = Image.open(png_image_path).convert("RGB")
        output = Path(save_jpg_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, "JPEG")
        return output

    @staticmethod
    def jpg_to_png(jpg_image_path: str | Path, save_png_path: str | Path) -> Path:
        image = Image.open(jpg_image_path).convert("RGB")
        output = Path(save_png_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        image.save(output, "PNG")
        return output

    @staticmethod
    def get_subject_from_mask(
        real_image_path: str | Path,
        mask_image_path: str | Path,
        output_path: str | Path,
        keep_background_or_foreground: str = "foreground",
        threshold: int = 200,
    ) -> Path:
        image = Image.open(real_image_path).convert("RGB")
        width, height = image.size
        image_np = np.array(image)

        mask = Image.open(mask_image_path).resize((width, height)).convert("RGBA")
        mask = np.array(mask)[:, :, 0]

        if keep_background_or_foreground == "background":
            binary = (mask < threshold).astype(np.uint8)
        else:
            binary = (mask >= threshold).astype(np.uint8)

        result = image_np * np.expand_dims(binary, axis=-1)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        Image.fromarray(result).save(output)
        return output

    @staticmethod
    def split_triptych_right(image_path: str | Path, output_path: str | Path) -> Path:
        image = Image.open(image_path)
        width, height = image.size
        sub_width = width // 3
        right = image.crop((2 * sub_width, 0, width, height))

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        right.save(output)
        return output

    @staticmethod
    def resize_image(image_path: str | Path, scale_ratio: float, output_path: str | Path) -> Path:
        img = cv2.imread(str(image_path), cv2.IMREAD_UNCHANGED)
        if img is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")

        width = int(img.shape[1] * scale_ratio)
        height = int(img.shape[0] * scale_ratio)
        resized = cv2.resize(img, (width, height), interpolation=cv2.INTER_AREA)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output), resized)
        return output

    @staticmethod
    def create_black_image(width: int = 384, height: int = 512, output_path: str | Path = "./output.jpg") -> Path:
        image = np.zeros((height, width, 3), dtype=np.uint8)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output), image)
        return output

    @staticmethod
    def enhance_pose_image(pose_img_path: str | Path, output_path: str | Path) -> Path:
        image = cv2.imread(str(pose_img_path))
        if image is None:
            raise FileNotFoundError(f"Cannot read pose image: {pose_img_path}")

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)

        kernel = np.ones((5, 5), np.uint8)
        dilated = cv2.dilate(mask, kernel, iterations=3)
        enhanced = cv2.bitwise_and(image, image, mask=dilated)
        enhanced = cv2.GaussianBlur(enhanced, (5, 5), 0)
        enhanced = cv2.convertScaleAbs(enhanced, alpha=2, beta=20)

        final = np.zeros_like(image)
        final[dilated > 0] = enhanced[dilated > 0]

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output), final)
        return output

    @staticmethod
    def black_to_white_background(pose_img_path: str | Path, output_path: str | Path) -> Path:
        image = cv2.imread(str(pose_img_path))
        if image is None:
            raise FileNotFoundError(f"Cannot read pose image: {pose_img_path}")

        mask = cv2.inRange(image, np.array([0, 0, 0], dtype=np.uint8), np.array([30, 30, 30], dtype=np.uint8))
        image[mask > 0] = [255, 255, 255]
        image = cv2.medianBlur(image, 3)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(output), image)
        return output
