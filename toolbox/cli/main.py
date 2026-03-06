from __future__ import annotations

import argparse
import importlib
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

CANONICAL_COMMANDS = {
    # image
    "img.merge": "scripts.image.merge_images",
    "img.merge-random": "scripts.image.merge_random_images",
    "img.resize": "scripts.image.resize_image",
    "img.png2jpg": "scripts.image.convert_png_to_jpg",
    "img.jpg2png": "scripts.image.convert_jpg_to_png",
    "img.mask": "scripts.image.extract_entity_from_mask",
    "img.pose": "scripts.image.enhance_pose_image",
    "img.split-merged": "scripts.image.split_merged_image",
    "img.blur": "scripts.image.image_gaussian_blur",
    # video
    "vid.split": "scripts.video.split_video",
    "vid.split-batch": "scripts.video.split_videos_in_half",
    "vid.to-audio": "scripts.video.video_to_audio",
    "vid.to-gif": "scripts.video.video_to_gif",
    "vid.to-frames": "scripts.video.media_to_frames",
    "vid.from-frames": "scripts.video.frames_to_video",
    "vid.crop-center": "scripts.video.crop_video_center",
    "vid.resize": "scripts.video.resize_video",
    "vid.merge-image": "scripts.video.merge_image_and_video",
    # data
    "data.download": "scripts.data.files.download_file",
    "data.download-hf": "scripts.data.files.download_huggingface",
    "data.rename": "scripts.data.files.rename_files",
    "data.excel": "scripts.data.excel.read_excel",
    "data.camera-noise-csv": "scripts.data.files.write_camera_noise_training_csv",
    "data.meta-csv": "scripts.data.files.build_dataset_metadata_csv",
    # optical flow
    "flow.compute": "scripts.optical_flow.optical_flow_between_images",
    "flow.draw": "scripts.optical_flow.draw_optical_flow",
    # process
    "proc.cpu": "scripts.process.multi_process_cpu",
    "proc.gpu": "scripts.process.multi_process_gpu",
    # visualization
    "viz.wordcloud": "scripts.visualization.draw_word_cloud",
    "viz.bar": "scripts.visualization.draw_grouped_bar",
    "viz.temporal": "scripts.visualization.draw_video_temporal",
    # qwen
    "ai.qwen.meta-csv": "scripts.ml.qwen.build_qwen_metadata_csv",
    "ai.qwen2vl.image": "scripts.ml.qwen.infer_qwen2vl_images",
    "ai.qwen3vl.video": "scripts.ml.qwen.infer_qwen3vl_videos",
    "ai.qwen3.text": "scripts.ml.qwen.infer_qwen3_text_from_csv",
    # ui
    "ui.gradio": "toolbox.ui.app",
}

ALIASES = {
    # backward compatible aliases
    "image.merge": "img.merge",
    "image.merge_random": "img.merge-random",
    "image.resize": "img.resize",
    "image.png2jpg": "img.png2jpg",
    "image.jpg2png": "img.jpg2png",
    "image.mask_extract": "img.mask",
    "image.pose_enhance": "img.pose",
    "image.split_merged": "img.split-merged",
    "image.blur": "img.blur",
    "video.split": "vid.split",
    "video.split_batch": "vid.split-batch",
    "video.to_audio": "vid.to-audio",
    "video.to_gif": "vid.to-gif",
    "video.to_frames": "vid.to-frames",
    "video.from_frames": "vid.from-frames",
    "video.crop_center": "vid.crop-center",
    "video.resize": "vid.resize",
    "video.merge_with_image": "vid.merge-image",
    "data.download_hf": "data.download-hf",
    "data.camera_noise_csv": "data.camera-noise-csv",
    "data.meta_csv": "data.meta-csv",
    "process.cpu": "proc.cpu",
    "process.gpu": "proc.gpu",
    "qwen.meta_csv": "ai.qwen.meta-csv",
    "qwen2vl.image": "ai.qwen2vl.image",
    "qwen3vl.video": "ai.qwen3vl.video",
    "qwen3.text": "ai.qwen3.text",
}


def resolve_command(command: str) -> tuple[str, str]:
    canonical = ALIASES.get(command, command)
    module = CANONICAL_COMMANDS.get(canonical)
    if module is None:
        raise SystemExit(f"Unknown command: {command}. Use --list.")
    return canonical, module


def main() -> None:
    parser = argparse.ArgumentParser(description="Unified ElephantToolbox CLI")
    parser.add_argument("command", nargs="?", help="Command key, e.g. vid.split")
    parser.add_argument("--list", action="store_true", help="List canonical commands")
    parser.add_argument("--list-all", action="store_true", help="List canonical commands and aliases")
    parser.add_argument("args", nargs=argparse.REMAINDER, help="Arguments passed to target command")
    ns = parser.parse_args()

    if ns.list_all:
        print("Canonical commands:")
        for key in sorted(CANONICAL_COMMANDS):
            print(f"  {key} -> {CANONICAL_COMMANDS[key]}")
        print("\nAliases:")
        for key in sorted(ALIASES):
            print(f"  {key} -> {ALIASES[key]}")
        return

    if ns.list or not ns.command:
        print("Canonical commands:")
        for key in sorted(CANONICAL_COMMANDS):
            print(f"  {key} -> {CANONICAL_COMMANDS[key]}")
        return

    canonical, module_name = resolve_command(ns.command)
    mod = importlib.import_module(module_name)
    if not hasattr(mod, "main"):
        raise SystemExit(f"Module {module_name} has no main()")

    sys.argv = [canonical, *ns.args]
    mod.main()


if __name__ == "__main__":
    main()
