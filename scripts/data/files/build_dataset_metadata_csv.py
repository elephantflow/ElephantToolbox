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
    parser = argparse.ArgumentParser(description="Build dataset metadata csv with reusable templates.")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_caption = sub.add_parser("from-caption-txt", help="Build csv from caption txt + video/noise roots.")
    p_caption.add_argument("--video_root", required=True)
    p_caption.add_argument("--noise_root", required=True)
    p_caption.add_argument("--caption_metadata_txt", required=True)
    p_caption.add_argument("--output_csv", required=True)
    p_caption.add_argument("--separator", default="#####")
    p_caption.add_argument("--caption_key_mode", default="stem", choices=["stem", "parent", "path_part"])
    p_caption.add_argument("--recursive", action="store_true")

    p_folder = sub.add_parser("from-prompt-map-folder", help="Scan folder and build csv from prompt txt map.")
    p_folder.add_argument("--video_root", required=True)
    p_folder.add_argument("--prompt_txt", required=True)
    p_folder.add_argument("--output_csv", required=True)
    p_folder.add_argument("--separator", default="#####")
    p_folder.add_argument("--prompt_key_mode", default="stem", choices=["stem", "parent", "path_part"])
    p_folder.add_argument("--path_part_index", type=int, default=None)
    p_folder.add_argument("--video_path_mode", default="absolute", choices=["absolute", "relative"])
    p_folder.add_argument("--video_path_prefix", default="videos")
    p_folder.add_argument("--recursive", action="store_true")

    p_multi_desc = sub.add_parser("multicam-from-desc", help="Build multicam csv from description txt.")
    p_multi_desc.add_argument("--description_txt", required=True)
    p_multi_desc.add_argument("--multicam_train_root", required=True)
    p_multi_desc.add_argument("--noise_root", required=True)
    p_multi_desc.add_argument("--output_csv", required=True)
    p_multi_desc.add_argument("--separator", default="#####")
    p_multi_desc.add_argument("--check_exists", action="store_true")

    p_multi_ref = sub.add_parser("multicam-with-reference", help="Build multicam csv with reference_video.")
    p_multi_ref.add_argument("--ann_txt", required=True)
    p_multi_ref.add_argument("--video_root", required=True)
    p_multi_ref.add_argument("--noise_root", required=True)
    p_multi_ref.add_argument("--output_csv", required=True)
    p_multi_ref.add_argument("--separator", default="#####")
    p_multi_ref.add_argument("--camera_count", type=int, default=10)
    p_multi_ref.add_argument("--random_seed", type=int, default=42)
    p_multi_ref.add_argument("--max_rows", type=int, default=None)

    p_multi_all = sub.add_parser("multicam-all-cams", help="Expand each prompt to all camera views.")
    p_multi_all.add_argument("--prompt_txt", required=True)
    p_multi_all.add_argument("--video_root", required=True)
    p_multi_all.add_argument("--noise_root", required=True)
    p_multi_all.add_argument("--output_csv", required=True)
    p_multi_all.add_argument("--separator", default="#####")
    p_multi_all.add_argument("--camera_count", type=int, default=10)
    p_multi_all.add_argument("--check_exists", action="store_true")

    p_openvid = sub.add_parser("openvid", help="Build OpenVid csv from source metadata csv.")
    p_openvid.add_argument("--source_csv", required=True)
    p_openvid.add_argument("--video_root", required=True)
    p_openvid.add_argument("--noise_root", required=True)
    p_openvid.add_argument("--output_csv", required=True)
    p_openvid.add_argument("--video_field", default="video")
    p_openvid.add_argument("--caption_field", default="caption")
    p_openvid.add_argument("--require_noise_exists", action="store_true")

    args = parser.parse_args()

    if args.mode == "from-caption-txt":
        out, count = DatasetMetadataToolkit.build_camera_noise_training_csv(
            video_root=args.video_root,
            noise_root=args.noise_root,
            caption_metadata_txt=args.caption_metadata_txt,
            output_csv=args.output_csv,
            separator=args.separator,
            caption_key_mode=args.caption_key_mode,
            recursive=args.recursive,
        )
    elif args.mode == "from-prompt-map-folder":
        prompt_map = DatasetMetadataToolkit.load_prompt_map_from_txt(
            txt_path=args.prompt_txt,
            separator=args.separator,
            key_mode=args.prompt_key_mode,
            path_part_index=args.path_part_index,
        )
        out, count = DatasetMetadataToolkit.build_video_prompt_noise_csv_from_prompt_map(
            video_root=args.video_root,
            prompt_map=prompt_map,
            output_csv=args.output_csv,
            recursive=args.recursive,
            video_path_mode=args.video_path_mode,
            video_path_prefix=args.video_path_prefix,
        )
    elif args.mode == "multicam-from-desc":
        out, count = DatasetMetadataToolkit.build_multicam_training_csv_from_description_txt(
            description_txt=args.description_txt,
            multicam_train_root=args.multicam_train_root,
            noise_root=args.noise_root,
            output_csv=args.output_csv,
            separator=args.separator,
            check_exists=args.check_exists,
        )
    elif args.mode == "multicam-with-reference":
        out, count = DatasetMetadataToolkit.build_multicam_with_reference_csv_from_ann_txt(
            ann_txt=args.ann_txt,
            video_root=args.video_root,
            noise_root=args.noise_root,
            output_csv=args.output_csv,
            separator=args.separator,
            camera_count=args.camera_count,
            random_seed=args.random_seed,
            max_rows=args.max_rows,
        )
    elif args.mode == "multicam-all-cams":
        out, count = DatasetMetadataToolkit.build_multicam_all_cams_csv_from_prompt_txt(
            prompt_txt=args.prompt_txt,
            video_root=args.video_root,
            noise_root=args.noise_root,
            output_csv=args.output_csv,
            separator=args.separator,
            camera_count=args.camera_count,
            check_exists=args.check_exists,
        )
    elif args.mode == "openvid":
        out, count = DatasetMetadataToolkit.build_openvid_camera_noise_csv(
            source_csv=args.source_csv,
            video_root=args.video_root,
            noise_root=args.noise_root,
            output_csv=args.output_csv,
            video_field=args.video_field,
            caption_field=args.caption_field,
            require_noise_exists=args.require_noise_exists,
        )
    else:
        raise SystemExit(f"Unsupported mode: {args.mode}")

    print(f"Saved: {out}")
    print(f"Rows: {count}")


if __name__ == "__main__":
    main()
