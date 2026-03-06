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

from toolbox.core.experimental import ExperimentalToolkit


def enhance_pose_in_videos(input_video_path, output_video_path):
    return ExperimentalToolkit.enhance_pose_video(input_video_path, output_video_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Enhance middle pose panel in merged triple-panel videos.")
    parser.add_argument("--input_video_path", required=True)
    parser.add_argument("--output_video_path", required=True)
    args = parser.parse_args()

    out = enhance_pose_in_videos(args.input_video_path, args.output_video_path)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
