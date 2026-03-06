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
    parser = argparse.ArgumentParser(description="Run Qwen3 text refinement from csv metadata.")
    parser.add_argument("--model_path", type=str, required=True, help="Qwen3 text model path.")
    parser.add_argument("--input_csv", type=str, required=True, help="Input csv file.")
    parser.add_argument("--output_txt", type=str, required=True, help="Output txt path.")
    parser.add_argument("--id_field", type=str, default="video_pth")
    parser.add_argument("--image_desc_field", type=str, default="image_description")
    parser.add_argument("--camera_desc_field", type=str, default="camera_description")
    parser.add_argument(
        "--question",
        type=str,
        default=(
            "Integrate only the camera pose information from the camera description into the image description. "
            "Do not add any entities or objects not present in the image description, output one short sentence."
        ),
    )
    parser.add_argument("--max_new_tokens", type=int, default=2048)
    parser.add_argument(
        "--strip_before_token_id",
        type=int,
        default=-1,
        help="If >0, trim generated ids before last occurrence of this token id (for thinking-model cleanup).",
    )
    args = parser.parse_args()

    strip_token = args.strip_before_token_id if args.strip_before_token_id > 0 else None
    out = QwenToolkit.qwen3_text_refine_from_csv(
        model_path=args.model_path,
        input_csv=args.input_csv,
        output_txt=args.output_txt,
        image_desc_field=args.image_desc_field,
        camera_desc_field=args.camera_desc_field,
        question=args.question,
        id_field=args.id_field,
        max_new_tokens=args.max_new_tokens,
        strip_before_token_id=strip_token,
    )
    print(f"Saved: {out}")


if __name__ == "__main__":
    main()
