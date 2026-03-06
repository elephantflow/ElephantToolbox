from __future__ import annotations

from pathlib import Path

import cv2
import numpy as np


class OpticalFlowToolkit:
    """Reusable optical flow methods."""

    @staticmethod
    def read_image(path: str | Path, resize: tuple[int, int] | None = None) -> np.ndarray:
        image = cv2.imread(str(path))
        if image is None:
            raise FileNotFoundError(f"Cannot read image: {path}")
        if resize:
            image = cv2.resize(image, resize, interpolation=cv2.INTER_AREA)
        return image

    @staticmethod
    def compute_farneback_flow(frame1: np.ndarray, frame2: np.ndarray) -> np.ndarray:
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
        return cv2.calcOpticalFlowFarneback(gray1, gray2, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    @staticmethod
    def flow_to_color(flow: np.ndarray) -> np.ndarray:
        magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        hsv = np.zeros((flow.shape[0], flow.shape[1], 3), dtype=np.float32)
        hsv[..., 0] = angle * 180 / np.pi / 2
        hsv[..., 1] = 1.0
        hsv[..., 2] = cv2.normalize(magnitude, None, 0.0, 1.0, cv2.NORM_MINMAX)
        bgr = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)
        return (bgr * 255).astype(np.uint8)

    @classmethod
    def compute_between_images(
        cls,
        img1_path: str | Path,
        img2_path: str | Path,
        resize: tuple[int, int] = (576, 1024),
    ) -> tuple[np.ndarray, np.ndarray]:
        img1 = cls.read_image(img1_path, resize=resize)
        img2 = cls.read_image(img2_path, resize=resize)
        flow = cls.compute_farneback_flow(img1, img2)
        return cls.flow_to_color(flow), flow

    @staticmethod
    def find_motion_extreme_frame(
        video_path: str | Path,
        max_frames: int = 100,
        least_motion: bool = True,
    ) -> tuple[int, np.ndarray, float]:
        cap = cv2.VideoCapture(str(video_path))
        if not cap.isOpened():
            raise FileNotFoundError(f"Cannot open video: {video_path}")

        ok, prev = cap.read()
        if not ok:
            raise RuntimeError("Cannot read first frame")

        prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
        metrics: list[float] = []
        frames: list[np.ndarray] = []

        while len(metrics) < max_frames:
            ok, frame = cap.read()
            if not ok:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
            magnitude = np.sqrt(flow[..., 0] ** 2 + flow[..., 1] ** 2)
            metrics.append(float(np.mean(magnitude)))
            frames.append(frame)
            prev_gray = gray

        cap.release()
        if not frames:
            raise RuntimeError("No readable frames after first frame")

        index = int(np.argmin(metrics) if least_motion else np.argmax(metrics))
        return index, frames[index], metrics[index]
