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

from toolbox.core.metadata import DatasetMetadataToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Build camera-noise training metadata CSV.")
    parser.add_argument("--video_root", type=str, required=True)
    parser.add_argument("--noise_root", type=str, required=True)
    parser.add_argument("--caption_metadata_txt", type=str, required=True)
    parser.add_argument("--output_csv", type=str, required=True)
    parser.add_argument("--separator", type=str, default="#####")
    args = parser.parse_args()

    output_csv, count = DatasetMetadataToolkit.build_camera_noise_training_csv(
        video_root=args.video_root,
        noise_root=args.noise_root,
        caption_metadata_txt=args.caption_metadata_txt,
        output_csv=args.output_csv,
        separator=args.separator,
    )
    print(f"Saved: {output_csv}")
    print(f"Rows: {count}")


if __name__ == "__main__":
    main()
