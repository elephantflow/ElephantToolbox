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
    parser = argparse.ArgumentParser(description="Attach audio track to video.")
    parser.add_argument("--video_path", required=True)
    parser.add_argument("--audio_path", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--loop_audio", action="store_true")
    args = parser.parse_args()

    out = ExperimentalToolkit.add_audio_to_video(args.video_path, args.audio_path, args.output_path, loop_audio=args.loop_audio)
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
