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

from toolbox.core.videos import VideoToolkit


def frame2video_path(frames_path, video_save_path, fps=15):
    return VideoToolkit.frames_to_video(frames_path, video_save_path, fps=fps)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert a frame folder to video.")
    parser.add_argument("--frames_root", type=str, required=True)
    parser.add_argument("--video_save_path", type=str, required=True)
    parser.add_argument("--fps", type=int, default=15)
    args = parser.parse_args()

    frame_paths = sorted([p for p in Path(args.frames_root).iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
    out = frame2video_path(frame_paths, args.video_save_path, fps=args.fps)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
