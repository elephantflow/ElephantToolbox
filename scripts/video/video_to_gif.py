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

import imageio
from PIL import Image

from toolbox.core.videos import VideoToolkit


def decordReadVideo(video_path):
    # kept for backward compatibility with older imports
    frames = VideoToolkit.read_video_frames_cv2(video_path)
    return frames, len(frames)


def create_gif_frome_frames(frames, save_path, duration=2.0):
    fps = int(max(1, round(1000 / duration))) if duration > 0 else 8
    imageio.mimsave(save_path, frames, 'GIF', duration=1000 / fps, loop=0)
    return Path(save_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert video to gif.")
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--save_path", type=str, required=True)
    parser.add_argument("--fps", type=int, default=8)
    args = parser.parse_args()

    frames_bgr = VideoToolkit.read_video_frames_cv2(args.video_path)
    frames = [Image.fromarray(frame[:, :, ::-1], mode="RGB") for frame in frames_bgr]
    imageio.mimsave(args.save_path, frames, 'GIF', duration=1000 / args.fps, loop=0)
    print(f"Saved: {args.save_path}")


if __name__ == "__main__":
    main()
