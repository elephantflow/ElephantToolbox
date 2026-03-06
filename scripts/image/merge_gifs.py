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

from toolbox.core.gifs import GifToolkit


def concatenate_gifs(gif_paths, output_path):
    return GifToolkit.concatenate_gifs(gif_paths, output_path)


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge multiple gif files into one gif.")
    parser.add_argument("--gif_root", type=str, required=True)
    parser.add_argument("--output_gif", type=str, required=True)
    args = parser.parse_args()

    gif_root = Path(args.gif_root)
    gif_files = sorted([p for p in gif_root.iterdir() if p.suffix.lower() == ".gif"])
    out = concatenate_gifs(gif_files, args.output_gif)
    print(f"Generated: {out}")


if __name__ == "__main__":
    main()
