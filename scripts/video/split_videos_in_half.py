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
from multiprocessing import Pool
from pathlib import Path

from decord import VideoReader, cpu
from tqdm import tqdm

from toolbox.core.videos import VideoToolkit
from toolbox.utils.logger import logger


def _split_one_video(args):
    input_video, output_dir, reencode = args
    video_path = Path(input_video)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    vr = VideoReader(str(video_path), ctx=cpu(0))
    duration = len(vr)
    fps = float(vr.get_avg_fps())
    half_frame = int(duration / 2)
    half_time = half_frame / fps
    total_time = (duration - 1) / fps

    out1 = output_dir / f"part1_{video_path.name}"
    out2 = output_dir / f"part2_{video_path.name}"

    VideoToolkit.split_video_with_ffmpeg(video_path, 0.0, half_time, out1, reencode=reencode)
    VideoToolkit.split_video_with_ffmpeg(video_path, half_time, total_time, out2, reencode=reencode)
    return str(video_path), str(out1), str(out2)


def main() -> None:
    parser = argparse.ArgumentParser(description="Split each video into two halves.")
    parser.add_argument("--video_root", type=str, required=True)
    parser.add_argument("--save_root", type=str, required=True)
    parser.add_argument("--n_jobs", type=int, default=8)
    parser.add_argument("--reencode", action="store_true")
    args = parser.parse_args()

    video_root = Path(args.video_root)
    save_root = Path(args.save_root)
    save_root.mkdir(parents=True, exist_ok=True)

    videos = sorted(
        [
            str(video_root / name)
            for name in os.listdir(video_root)
            if (video_root / name).suffix.lower() in {".mp4", ".mov", ".avi", ".mkv"}
        ]
    )

    tasks = [(path, str(save_root), args.reencode) for path in videos]
    with Pool(args.n_jobs) as pool:
        for input_video, out1, out2 in tqdm(pool.imap(_split_one_video, tasks), total=len(tasks)):
            logger.info(f"Split finished: {input_video} -> {out1}, {out2}")


if __name__ == "__main__":
    main()
