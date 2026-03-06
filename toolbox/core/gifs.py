from __future__ import annotations

from pathlib import Path

import imageio
from PIL import Image, ImageDraw, ImageFont
from torchvision.transforms import CenterCrop, Compose, Resize


class GifToolkit:
    """Reusable GIF operations."""

    @staticmethod
    def frames_to_gif(image_paths: list[str | Path], save_path: str | Path, fps: int = 5, crop_size: int = 256) -> Path:
        transform = Compose([Resize(crop_size, antialias=False), CenterCrop(crop_size)])
        frames = [transform(Image.open(path)) for path in image_paths]

        output = Path(save_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        imageio.mimsave(str(output), frames, "GIF", duration=1000 / fps, loop=0)
        return output

    @staticmethod
    def gif_to_frames(input_file: str | Path, output_dir: str | Path, suffix: str = ".png") -> list[Path]:
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        frames = imageio.mimread(str(input_file))
        saved: list[Path] = []
        for i, frame in enumerate(frames):
            path = output / f"frame_{i}{suffix}"
            imageio.imwrite(str(path), frame)
            saved.append(path)
        return saved

    @staticmethod
    def concatenate_gifs(gif_paths: list[str | Path], output_path: str | Path, fps: int = 6, with_index_text: bool = True) -> Path:
        if not gif_paths:
            raise ValueError("gif_paths cannot be empty")

        gif_frames = [imageio.mimread(str(path)) for path in gif_paths]
        frame_count = len(gif_frames[0])
        widths, heights = zip(*(Image.open(path).size for path in gif_paths))

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        final_frames: list[Image.Image] = []
        for frame_idx in range(frame_count):
            canvas = Image.new("RGBA", (sum(widths), max(heights)))
            x_offset = 0
            for gif_idx, frames in enumerate(gif_frames):
                frame = Image.fromarray(frames[frame_idx])
                canvas.paste(frame, (x_offset, 0))
                if with_index_text:
                    GifToolkit._annotate(canvas, str(gif_idx + 1), (x_offset + 16, 16))
                x_offset += frame.width
            final_frames.append(canvas.convert("RGB"))

        imageio.mimsave(str(output), final_frames, duration=1000 / fps, loop=0)
        return output

    @staticmethod
    def _annotate(image: Image.Image, text: str, position: tuple[int, int]) -> None:
        draw = ImageDraw.Draw(image)
        try:
            font = ImageFont.load_default()
        except Exception:
            font = None
        draw.text(position, text, font=font, fill=(255, 0, 0))
