from __future__ import annotations

import argparse
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

from toolbox.core.qwen import QwenToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Build metadata csv by merging image-caption txt and camera-caption txt.")
    parser.add_argument("--image_caption_txt", type=str, required=True)
    parser.add_argument("--camera_caption_txt", type=str, required=True)
    parser.add_argument("--output_csv", type=str, required=True)
    parser.add_argument("--image_index_filter", type=int, default=0, help="Only keep image paths with this frame index.")
    args = parser.parse_args()

    out = QwenToolkit.build_metadata_csv_from_pair_texts(
        image_caption_txt=args.image_caption_txt,
        camera_caption_txt=args.camera_caption_txt,
        output_csv=args.output_csv,
        image_index_filter=args.image_index_filter,
    )
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
