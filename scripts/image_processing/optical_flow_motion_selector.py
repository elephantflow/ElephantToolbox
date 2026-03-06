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

import cv2

from toolbox.core.optical_flow import OpticalFlowToolkit


def find_least_motion_frame(video_path):
    idx, frame, score = OpticalFlowToolkit.find_motion_extreme_frame(video_path, max_frames=100, least_motion=True)
    return idx, frame, score


def main() -> None:
    parser = argparse.ArgumentParser(description="Find least-motion frame in video by optical flow.")
    parser.add_argument("--video_path", type=str, required=True)
    parser.add_argument("--save_path", type=str, default=None)
    args = parser.parse_args()

    idx, frame, score = find_least_motion_frame(args.video_path)
    print(f"Least motion frame index: {idx}, score: {score:.6f}")
    if args.save_path:
        cv2.imwrite(args.save_path, frame)
        print(f"Saved: {args.save_path}")


if __name__ == "__main__":
    main()
