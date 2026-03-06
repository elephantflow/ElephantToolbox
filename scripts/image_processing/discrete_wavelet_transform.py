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

import matplotlib.pyplot as plt

from toolbox.core.experimental import ExperimentalToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute and visualize Haar wavelet edges.")
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--save_path", default=None)
    args = parser.parse_args()

    img, edges = ExperimentalToolkit.wavelet_edges(args.image_path)

    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.title("Original Image")
    plt.imshow(img, cmap='gray')
    plt.subplot(1, 2, 2)
    plt.title("Wavelet Edges")
    plt.imshow(edges, cmap='gray')

    if args.save_path:
        plt.savefig(args.save_path)
        print(f"Saved: {args.save_path}")
    else:
        plt.show()


if __name__ == "__main__":
    main()
