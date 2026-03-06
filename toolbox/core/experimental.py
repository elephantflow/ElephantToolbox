from __future__ import annotations

import random
from pathlib import Path

import numpy as np


class ExperimentalToolkit:
    """Container for legacy experimental utilities, now parameterized and reusable."""

    @staticmethod
    def add_audio_to_video(video_path: str | Path, audio_path: str | Path, output_path: str | Path, loop_audio: bool = False) -> Path:
        from moviepy.editor import AudioFileClip, VideoFileClip

        video_clip = VideoFileClip(str(video_path))
        audio_clip = AudioFileClip(str(audio_path))

        if audio_clip.duration > video_clip.duration:
            audio_clip = audio_clip.subclip(0, video_clip.duration)
        elif loop_audio and audio_clip.duration < video_clip.duration:
            audio_clip = audio_clip.loop(duration=video_clip.duration)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        video_clip.set_audio(audio_clip).write_videofile(str(out), codec="libx264", audio_codec="aac")
        return out

    @staticmethod
    def detect_hands(image_path: str | Path, output_path: str | Path | None = None, max_num_hands: int = 2):
        import cv2
        import mediapipe as mp

        image = cv2.imread(str(image_path))
        if image is None:
            raise FileNotFoundError(f"Image not found: {image_path}")

        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(static_image_mode=True, max_num_hands=max_num_hands, min_detection_confidence=0.5)
        result = hands.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                x_min = y_min = float("inf")
                x_max = y_max = float("-inf")
                for lm in hand_landmarks.landmark:
                    h, w, _ = image.shape
                    x, y = int(lm.x * w), int(lm.y * h)
                    x_min = min(x_min, x)
                    y_min = min(y_min, y)
                    x_max = max(x_max, x)
                    y_max = max(y_max, y)
                cv2.rectangle(image, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)
                mp.solutions.drawing_utils.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        if output_path:
            out = Path(output_path)
            out.parent.mkdir(parents=True, exist_ok=True)
            cv2.imwrite(str(out), image)
            return out
        return image

    @staticmethod
    def wavelet_edges(image_path: str | Path):
        import cv2
        import pywt

        img = cv2.imread(str(image_path), cv2.IMREAD_GRAYSCALE)
        if img is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")
        cA, (cH, cV, cD) = pywt.dwt2(img, "haar")
        edges = np.sqrt(cH ** 2 + cV ** 2 + cD ** 2)
        edges = (edges - edges.min()) / (edges.max() - edges.min() + 1e-8)
        return img, edges

    @staticmethod
    def gaussian_blur_image(image_path: str | Path, output_path: str | Path, kernel: int = 31, sigma: int = 15) -> Path:
        import cv2

        image = cv2.imread(str(image_path))
        if image is None:
            raise FileNotFoundError(f"Cannot read image: {image_path}")
        blurred = cv2.GaussianBlur(image, (kernel, kernel), sigma)

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        cv2.imwrite(str(out), blurred)
        return out

    @staticmethod
    def crop_video_center_square(video_path: str | Path, output_path: str | Path, crop_size: int = 1080) -> Path:
        return ExperimentalToolkit.crop_video_center(
            video_path=video_path,
            output_path=output_path,
            crop_width=crop_size,
            crop_height=crop_size,
        )

    @staticmethod
    def crop_video_center(
        video_path: str | Path,
        output_path: str | Path,
        crop_width: int | None = None,
        crop_height: int | None = None,
    ) -> Path:
        from moviepy.editor import VideoFileClip

        clip = VideoFileClip(str(video_path))
        w, h = clip.size
        if w <= 0 or h <= 0:
            clip.close()
            raise RuntimeError("Invalid video frame size.")

        if crop_width is None and crop_height is None:
            side = min(w, h)
            crop_width, crop_height = side, side
        elif crop_width is None:
            crop_width = crop_height
        elif crop_height is None:
            crop_height = crop_width

        crop_width = int(crop_width)
        crop_height = int(crop_height)
        if crop_width <= 0 or crop_height <= 0:
            clip.close()
            raise ValueError("crop_width and crop_height must be positive.")
        if crop_width > w or crop_height > h:
            clip.close()
            raise ValueError(f"Crop size ({crop_width}, {crop_height}) exceeds video frame ({w}, {h}).")

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        cropped = clip.crop(x_center=w / 2, y_center=h / 2, width=crop_width, height=crop_height)
        cropped.write_videofile(str(out), codec="libx264", audio_codec="aac")
        cropped.close()
        clip.close()
        return out

    @staticmethod
    def crop_video_by_box(
        video_path: str | Path,
        output_path: str | Path,
        x: int,
        y: int,
        width: int,
        height: int,
    ) -> Path:
        from moviepy.editor import VideoFileClip

        clip = VideoFileClip(str(video_path))
        frame_w, frame_h = clip.size

        x = int(x)
        y = int(y)
        width = int(width)
        height = int(height)

        if width <= 0 or height <= 0:
            clip.close()
            raise ValueError("width and height must be positive.")
        if x < 0 or y < 0:
            clip.close()
            raise ValueError("x and y must be non-negative.")
        if x + width > frame_w or y + height > frame_h:
            clip.close()
            raise ValueError(
                f"ROI ({x}, {y}, {width}, {height}) exceeds video frame ({frame_w}, {frame_h})."
            )

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)

        cropped = clip.crop(x1=x, y1=y, x2=x + width, y2=y + height)
        cropped.write_videofile(str(out), codec="libx264", audio_codec="aac")
        cropped.close()
        clip.close()
        return out

    @staticmethod
    def blacken_video_edges(video_path: str | Path, output_path: str | Path, border_size: int = 200, max_frames: int | None = None) -> Path:
        import cv2

        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        writer = cv2.VideoWriter(str(out), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

        count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frame[:border_size, :, :] = 0
            frame[-border_size:, :, :] = 0
            frame[:, :border_size, :] = 0
            frame[:, -border_size:, :] = 0
            writer.write(frame)
            count += 1
            if max_frames and count >= max_frames:
                break

        cap.release()
        writer.release()
        return out

    @staticmethod
    def enhance_pose_video(input_video_path: str | Path, output_video_path: str | Path) -> Path:
        import cv2

        cap = cv2.VideoCapture(str(input_video_path))
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {input_video_path}")

        fps = cap.get(cv2.CAP_PROP_FPS)
        w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        split_w = w // 3

        out = Path(output_video_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        writer = cv2.VideoWriter(str(out), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

        kernel = np.ones((5, 5), np.uint8)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            left = frame[:, :split_w]
            middle = frame[:, split_w : 2 * split_w]
            right = frame[:, 2 * split_w :]

            gray = cv2.cvtColor(middle, cv2.COLOR_BGR2GRAY)
            _, mask = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            dilated = cv2.dilate(mask, kernel, iterations=4)
            enhanced = cv2.bitwise_and(middle, middle, mask=dilated)
            enhanced = cv2.GaussianBlur(enhanced, (5, 5), 0)
            enhanced = cv2.convertScaleAbs(enhanced, alpha=3, beta=30)
            final_middle = np.zeros_like(middle)
            final_middle[dilated > 0] = enhanced[dilated > 0]

            writer.write(np.hstack((left, final_middle, right)))

        cap.release()
        writer.release()
        return out

    @staticmethod
    def merge_videos_side_by_side(video_dir: str | Path, output_path: str | Path, skip_frames: int = 2, fps: int = 30) -> Path:
        from moviepy.editor import VideoFileClip, clips_array, concatenate_videoclips
        from moviepy.video.fx.all import time_mirror

        root = Path(video_dir)
        paths = sorted([p for p in root.iterdir() if p.is_file() and not p.name.startswith(".")])
        clips = []
        for path in paths:
            clip = VideoFileClip(str(path))
            clips.append(clip.subclip(skip_frames / fps))

        min_h = min(clip.h for clip in clips)
        resized = [clip.resize(height=min_h) for clip in clips]
        combined = clips_array([resized])
        final = concatenate_videoclips([combined, time_mirror(combined)])

        out = Path(output_path)
        out.parent.mkdir(parents=True, exist_ok=True)
        final.write_videofile(str(out), codec="libx264", fps=fps)
        return out

    @staticmethod
    def merge_videos_grid(input_folder: str | Path, output_file: str | Path, videos_per_row: int = 8, rows: int = 3, fps: float = 15.0) -> Path:
        import cv2

        videos = [str(p) for p in Path(input_folder).iterdir() if p.suffix.lower() in {".mp4", ".avi", ".mov"}]
        random.shuffle(videos)
        count = videos_per_row * rows
        if len(videos) < count:
            raise ValueError(f"Need at least {count} videos")
        selected = videos[:count]

        caps = [cv2.VideoCapture(path) for path in selected]
        heights = []
        for c in caps:
            ok, frame = c.read()
            if not ok:
                raise RuntimeError("Cannot read selected video frame")
            heights.append(frame.shape[0])
            c.set(cv2.CAP_PROP_POS_FRAMES, 2)

        target_h = min(heights)
        batches: list[list[np.ndarray]] = []
        min_len = None
        for cap in caps:
            frames = []
            while True:
                ok, frame = cap.read()
                if not ok:
                    break
                h, w, _ = frame.shape
                nw = int(w * (target_h / h))
                frames.append(cv2.resize(frame, (nw, target_h)))
            cap.release()
            batches.append(frames)
            min_len = len(frames) if min_len is None else min(min_len, len(frames))

        frames_out: list[np.ndarray] = []
        for i in range(min_len or 0):
            row_frames = []
            for r in range(rows):
                row = cv2.hconcat([batches[r * videos_per_row + c][i] for c in range(videos_per_row)])
                row_frames.append(row)
            frame = cv2.vconcat(row_frames)
            frames_out.append(frame)

        if not frames_out:
            raise RuntimeError("No merged frames generated")

        out = Path(output_file)
        out.parent.mkdir(parents=True, exist_ok=True)
        h, w = frames_out[0].shape[:2]
        writer = cv2.VideoWriter(str(out), cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
        for frame in frames_out:
            writer.write(frame)
        for frame in reversed(frames_out):
            writer.write(frame)
        writer.release()
        return out

    @staticmethod
    def choose_food(food_list: list[str], voters: int = 5) -> tuple[str, list[int]]:
        indices = [random.randint(0, len(food_list) - 1) for _ in range(voters)]
        counts = np.bincount(indices)
        return food_list[int(np.argmax(counts))], indices

    @staticmethod
    def transfer_person_names(names_str: str, keep_count: int = 10) -> str:
        names = names_str.split(", ")
        parts: list[str] = []
        for i, name in enumerate(names):
            if i >= keep_count:
                parts.append("others")
                break
            chunks = name.split(" ")
            if len(chunks) < 2:
                parts.append(name)
            else:
                parts.append(f"{chunks[1]}, {chunks[0]}")
        return " and ".join(parts)

    @staticmethod
    def birthday_interval_days(target_date: str) -> int:
        from datetime import datetime

        today = datetime.strptime(datetime.now().strftime("%Y-%m-%d"), "%Y-%m-%d")
        target = datetime.strptime(target_date, "%Y-%m-%d")
        return (today - target).days

    @staticmethod
    def pos_extract(sentence: str) -> tuple[list[str], list[str]]:
        import nltk
        from nltk import pos_tag
        from nltk.tokenize import word_tokenize

        nltk.download("punkt", quiet=True)
        nltk.download("averaged_perceptron_tagger", quiet=True)
        tagged_words = pos_tag(word_tokenize(sentence))
        nouns = [word for word, pos in tagged_words if pos.startswith("N")]
        verbs = [word for word, pos in tagged_words if pos.startswith("V")]
        return nouns, verbs

    @staticmethod
    def pca_variance(X: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        from sklearn.decomposition import PCA
        from sklearn.preprocessing import StandardScaler

        X_scaled = StandardScaler().fit_transform(X)
        pca = PCA()
        pca.fit(X_scaled)
        variance_ratio = pca.explained_variance_ratio_
        return variance_ratio, np.cumsum(variance_ratio)
