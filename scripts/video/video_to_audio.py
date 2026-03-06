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

from toolbox.core.videos import VideoToolkit


def video_to_audio(video_path, audio_path):
    return VideoToolkit.video_to_audio(video_path, audio_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract audio from video.")
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--audio_path", type=str, required=True)
    args = parser.parse_args()

    out = video_to_audio(args.video_path, args.audio_path)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
