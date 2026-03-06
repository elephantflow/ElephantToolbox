from __future__ import annotations

import argparse
import sys
from pathlib import Path

from tqdm import tqdm

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
    parser = argparse.ArgumentParser(description="Run Qwen3-VL video inference and save results as txt.")
    parser.add_argument("--model_path", type=str, required=True, help="Local/remote model path for Qwen3-VL.")
    parser.add_argument("--input_path", type=str, required=True, help="Video file, directory, or txt list.")
    parser.add_argument("--input_type", type=str, default="auto", choices=["auto", "dir", "txt", "file"])
    parser.add_argument(
        "--prompt",
        type=str,
        default="Tell me how the camera lens moves and changes its orientation while shooting the video.",
    )
    parser.add_argument("--output_txt", type=str, required=True, help="Output txt path.")
    parser.add_argument("--max_new_tokens", type=int, default=128)
    args = parser.parse_args()

    videos = QwenToolkit.collect_inputs(args.input_path, args.input_type, allowed_exts=QwenToolkit.VIDEO_EXTS)
    if not videos:
        raise SystemExit("No video files found for inference.")

    print(f"Found {len(videos)} videos.")
    out = QwenToolkit.qwen3vl_infer_videos(
        model_path=args.model_path,
        videos=tqdm(videos, desc="Qwen3-VL"),
        prompt=args.prompt,
        output_txt=args.output_txt,
        max_new_tokens=args.max_new_tokens,
    )
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
