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
import os
import time
from pathlib import Path

import imageio
from tqdm import tqdm

from toolbox.core.videos import VideoToolkit


def read_using_imageio(input_file, output_dir):
    frames = imageio.mimread(input_file)
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    for i, frame in enumerate(frames):
        imageio.imwrite(os.path.join(output_dir, f"{str(i).zfill(3)}.jpg"), frame)


def cv2BatchSaveFrames(video_path, save_root_path, sample_rate=1):
    saved = VideoToolkit.extract_frames(video_path, save_root_path, only_first=False)
    if sample_rate > 1:
        for idx, path in enumerate(saved):
            if idx % sample_rate != 0 and path.exists():
                path.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract frames from mp4 or gif file/folder.")
    parser.add_argument('--input_pth', type=str, required=True)
    parser.add_argument('--save_type', type=str, default="simple", choices=["simple", "all"])
    args = parser.parse_args()

    input_path = Path(args.input_pth)
    save_all = args.save_type == "all"

    ts = time.strftime("(%Y-%m-%d %H*%M*%S)", time.localtime())

    def save_single_media(media_path: Path, frame_dir: Path):
        frame_dir.mkdir(parents=True, exist_ok=True)
        if media_path.suffix.lower() == ".gif":
            frames = imageio.mimread(str(media_path))
            limit = len(frames) if save_all else 1
            for i in range(limit):
                imageio.imwrite(str(frame_dir / f"{i:03d}.jpg"), frames[i])
        else:
            saved = VideoToolkit.extract_frames(media_path, frame_dir, only_first=not save_all)
            if not saved:
                raise RuntimeError(f"No frames extracted from {media_path}")

    if input_path.is_file():
        frame_dir = Path(f"{str(input_path).removesuffix(input_path.suffix)}_frames_{ts}")
        save_single_media(input_path, frame_dir)
    else:
        out_root = input_path.parent / f"{input_path.name}_frames_{ts}"
        for media in tqdm(sorted(input_path.iterdir())):
            if media.suffix.lower() in {".mp4", ".gif"}:
                save_single_media(media, out_root / media.stem)

    print("video to frames finished.")


if __name__ == "__main__":
    main()
