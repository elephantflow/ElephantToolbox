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


def create_gif_frome_frames(image_list, save_path, duration=2.0):
    fps = int(max(1, round(1000 / duration))) if duration > 0 else 5
    return GifToolkit.frames_to_gif(image_list, save_path, fps=fps)


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert frame images to GIF.")
    parser.add_argument("--frames_root", type=str, required=True)
    parser.add_argument("--save_path", type=str, required=True)
    parser.add_argument("--fps", type=int, default=5)
    args = parser.parse_args()

    image_paths = sorted([p for p in Path(args.frames_root).iterdir() if p.suffix.lower() in {".jpg", ".jpeg", ".png"}])
    out = GifToolkit.frames_to_gif(image_paths, args.save_path, fps=args.fps)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
