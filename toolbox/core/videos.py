from __future__ import annotations

import subprocess
from pathlib import Path

import cv2
import imageio
import numpy as np
from PIL import Image
from moviepy.editor import VideoFileClip


class VideoToolkit:
    """Reusable video operations."""

    @staticmethod
    def split_video_with_moviepy(input_path: str | Path, start_time: float, end_time: float, output_path: str | Path) -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        clip = VideoFileClip(str(input_path))
        segment = clip.subclip(start_time, end_time)
        segment.write_videofile(str(output), codec="libx264")
        clip.close()
        return output

    @staticmethod
    def split_video_with_ffmpeg(
        input_path: str | Path,
        start_time: float,
        end_time: float,
        output_path: str | Path,
        reencode: bool = False,
    ) -> Path:
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        duration = max(0.0, end_time - start_time)
        if duration <= 0:
            raise ValueError("end_time must be greater than start_time.")

        command = ["ffmpeg", "-y", "-ss", str(start_time), "-i", str(input_path), "-t", str(duration)]
        if reencode:
            command += ["-c:v", "libx264", "-c:a", "aac"]
        else:
            command += ["-c:v", "copy", "-c:a", "copy"]
        command.append(str(output))

        subprocess.run(command, check=True)
        return output

    @staticmethod
    def video_to_audio(video_path: str | Path, audio_path: str | Path) -> Path:
        clip = VideoFileClip(str(video_path))
        audio = clip.audio
        if audio is None:
            raise ValueError(f"Video does not contain audio: {video_path}")

        output = Path(audio_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        audio.write_audiofile(str(output))
        clip.close()
        return output

    @staticmethod
    def frames_to_video(frame_paths: list[str | Path], video_save_path: str | Path, fps: int = 15) -> Path:
        if not frame_paths:
            raise ValueError("frame_paths cannot be empty")

        first = Image.open(frame_paths[0])
        size = first.size
        writer = cv2.VideoWriter(str(video_save_path), cv2.VideoWriter_fourcc('M', 'P', '4', 'V'), fps, size)

        for frame_path in frame_paths:
            frame = cv2.imread(str(frame_path))
            if frame is None:
                raise FileNotFoundError(f"Cannot read frame: {frame_path}")
            writer.write(frame)

        writer.release()
        return Path(video_save_path)

    @staticmethod
    def read_video_frames_cv2(video_path: str | Path, sample_rate: int = 1) -> list[np.ndarray]:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")

        frames: list[np.ndarray] = []
        idx = 0
        while True:
            ok, frame = cap.read()
            if not ok:
                break
            if idx % sample_rate == 0:
                frames.append(frame)
            idx += 1
        cap.release()
        return frames

    @staticmethod
    def extract_frames(video_path: str | Path, output_dir: str | Path, only_first: bool = False) -> list[Path]:
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)

        frames = VideoToolkit.read_video_frames_cv2(video_path)
        if only_first:
            frames = frames[:1]

        saved: list[Path] = []
        for i, frame in enumerate(frames):
            path = output / f"{i:05d}.jpg"
            cv2.imwrite(str(path), frame)
            saved.append(path)
        return saved

    @staticmethod
    def resize_video(input_path: str | Path, output_path: str | Path, fixed_size: int) -> Path:
        clip = VideoFileClip(str(input_path))
        width, height = clip.size
        if width > height:
            new_size = (fixed_size, int(height * (fixed_size / width)))
        else:
            new_size = (int(width * (fixed_size / height)), fixed_size)

        resized = clip.resize(newsize=new_size)
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        resized.write_videofile(str(output), codec="libx264")
        clip.close()
        return output

    @staticmethod
    def resize_and_crop_video(
        input_path: str | Path,
        output_path: str | Path,
        fixed_size: int,
        crop_size: tuple[int, int] = (512, 512),
    ) -> Path:
        clip = VideoFileClip(str(input_path))
        width, height = clip.size

        if width > height:
            new_w, new_h = fixed_size, int(height * (fixed_size / width))
        else:
            new_w, new_h = int(width * (fixed_size / height)), fixed_size

        resized = clip.resize(newsize=(new_w, new_h))
        x_center = new_w // 2
        y_center = new_h // 2
        x1 = max(0, x_center - crop_size[0] // 2)
        y1 = max(0, y_center - crop_size[1] // 2)

        cropped = resized.crop(x1=x1, y1=y1, x2=x1 + crop_size[0], y2=y1 + crop_size[1])
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        cropped.write_videofile(str(output), codec="libx264")
        clip.close()
        return output

    @staticmethod
    def combine_videos_with_image(video1_path: str | Path, video2_path: str | Path, image_path: str | Path, output_path: str | Path) -> Path:
        reader1 = imageio.get_reader(str(video1_path))
        reader2 = imageio.get_reader(str(video2_path))
        img = Image.open(image_path)

        n = min(reader1.count_frames(), reader2.count_frames())
        frame1 = reader1.get_data(0)
        frame2 = reader2.get_data(0)
        target_h = min(frame1.shape[0], frame2.shape[0])

        new_w1 = int(frame1.shape[1] * (target_h / frame1.shape[0]))
        new_w2 = int(frame2.shape[1] * (target_h / frame2.shape[0]))
        img_resized = img.resize((int(target_h * (img.width / img.height)), target_h), Image.LANCZOS)

        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)
        writer = imageio.get_writer(str(output), fps=reader2.get_meta_data().get("fps", 15))

        for i in range(n):
            f1 = np.array(Image.fromarray(reader1.get_data(i)).resize((new_w1, target_h), Image.LANCZOS))
            f2 = np.array(Image.fromarray(reader2.get_data(i)).resize((new_w2, target_h), Image.LANCZOS))
            merged = np.hstack([f1, np.array(img_resized), f2])
            writer.append_data(merged)

        writer.close()
        reader1.close()
        reader2.close()
        return output

    @staticmethod
    def merge_image_folders_to_video(folder1: str | Path, folder2: str | Path, output_file: str | Path, fps: int = 25) -> Path:
        files1 = sorted([p for p in Path(folder1).iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
        files2 = sorted([p for p in Path(folder2).iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
        if len(files1) != len(files2):
            raise ValueError("Two folders must have same image count")

        frames: list[np.ndarray] = []
        for p1, p2 in zip(files1, files2):
            i1 = Image.open(p1)
            i2 = Image.open(p2)
            h = min(i1.height, i2.height)
            i1 = i1.resize((int(i1.width * h / i1.height), h))
            i2 = i2.resize((int(i2.width * h / i2.height), h))
            canvas = Image.new("RGB", (i1.width + i2.width, h))
            canvas.paste(i1, (0, 0))
            canvas.paste(i2, (i1.width, 0))
            frames.append(cv2.cvtColor(np.array(canvas), cv2.COLOR_RGB2BGR))

        output = Path(output_file)
        output.parent.mkdir(parents=True, exist_ok=True)
        writer = cv2.VideoWriter(str(output), cv2.VideoWriter_fourcc(*"mp4v"), fps, (frames[0].shape[1], frames[0].shape[0]))
        for frame in frames:
            writer.write(frame)
        writer.release()
        return output
