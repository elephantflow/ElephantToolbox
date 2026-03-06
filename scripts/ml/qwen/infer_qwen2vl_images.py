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
    parser = argparse.ArgumentParser(description="Run Qwen2-VL image inference and save results as txt.")
    parser.add_argument("--model_path", type=str, required=True, help="Local/remote model path for Qwen2-VL.")
    parser.add_argument("--input_path", type=str, required=True, help="Image file, directory, or txt list.")
    parser.add_argument("--input_type", type=str, default="auto", choices=["auto", "dir", "txt", "file"])
    parser.add_argument(
        "--prompt",
        type=str,
        default="Please describe the content of the image in detail.",
    )
    parser.add_argument("--output_txt", type=str, required=True, help="Output txt path.")
    parser.add_argument("--max_new_tokens", type=int, default=128)
    args = parser.parse_args()

    images = QwenToolkit.collect_inputs(args.input_path, args.input_type, allowed_exts=QwenToolkit.IMAGE_EXTS)
    if not images:
        raise SystemExit("No image files found for inference.")

    print(f"Found {len(images)} images.")
    out = QwenToolkit.qwen2vl_infer_images(
        model_path=args.model_path,
        images=tqdm(images, desc="Qwen2-VL"),
        prompt=args.prompt,
        output_txt=args.output_txt,
        max_new_tokens=args.max_new_tokens,
    )
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
