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


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply Gaussian blur to image.")
    parser.add_argument("--image_path", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--kernel", type=int, default=31)
    parser.add_argument("--sigma", type=int, default=15)
    args = parser.parse_args()

    out = ExperimentalToolkit.gaussian_blur_image(args.image_path, args.output_path, kernel=args.kernel, sigma=args.sigma)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
