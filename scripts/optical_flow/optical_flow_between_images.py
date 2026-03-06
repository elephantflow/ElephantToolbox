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
import matplotlib.pyplot as plt

from toolbox.core.optical_flow import OpticalFlowToolkit


def compute_optical_flow(img1_path, img2_path, resize=(576, 1024)):
    return OpticalFlowToolkit.compute_between_images(img1_path, img2_path, resize)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute and visualize optical flow between two images.")
    parser.add_argument("--img1_path", type=str, required=True)
    parser.add_argument("--img2_path", type=str, required=True)
    parser.add_argument("--save_path", type=str, default=None)
    args = parser.parse_args()

    flow_vis, _ = compute_optical_flow(args.img1_path, args.img2_path)
    if args.save_path:
        cv2.imwrite(args.save_path, flow_vis)
        print(f"Saved: {args.save_path}")
    else:
        plt.figure(figsize=(12, 6))
        plt.imshow(cv2.cvtColor(flow_vis, cv2.COLOR_BGR2RGB))
        plt.title("Optical Flow Visualization")
        plt.axis("off")
        plt.show()


if __name__ == "__main__":
    main()
