from __future__ import annotations

from pathlib import Path
from typing import Any

import gradio as gr
import numpy as np

from toolbox.core.experimental import ExperimentalToolkit
from toolbox.core.files import FileToolkit
from toolbox.core.images import ImageToolkit
from toolbox.core.optical_flow import OpticalFlowToolkit
from toolbox.core.videos import VideoToolkit
from toolbox.versioning import bump_version, get_version


PROJECT_ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = PROJECT_ROOT / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

APP_CSS = """
:root {
  --bg: #eef3f9;
  --panel: #ffffff;
  --line: #dfe5ef;
  --text: #1b2430;
  --muted: #5b6678;
  --accent: #0f766e;
  --accent-soft: #dff5f2;
}
.gradio-container {
  background:
    radial-gradient(1200px 500px at 0% -10%, #d9ebff 0%, transparent 45%),
    radial-gradient(1200px 500px at 100% -10%, #d8f5ee 0%, transparent 45%),
    var(--bg);
  color: var(--text);
}
.app-head {
  background: linear-gradient(135deg, #f7fbff 0%, #f4fffb 100%);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 12px 16px;
  margin-bottom: 10px;
}
.app-head h1 {
  margin: 0 !important;
}
.app-head p {
  margin: 6px 0 0 0 !important;
  color: var(--muted);
}
.app-shell {
  gap: 16px !important;
  align-items: flex-start !important;
}
.sidebar-nav {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 14px;
  position: sticky;
  top: 12px;
  height: fit-content;
}
.content-panel {
  background: var(--panel);
  border: 1px solid var(--line);
  border-radius: 14px;
  padding: 14px;
}
.content-panel .gr-button {
  background: var(--accent) !important;
  border: 1px solid var(--accent) !important;
  color: #fff !important;
}
.content-panel .gr-button:hover {
  filter: brightness(0.95);
}
.section-title h3 {
  margin: 0 0 8px 0 !important;
}
.section-tip p {
  color: var(--muted);
  margin-top: 0 !important;
}
.media-preview {
  height: clamp(240px, 46vh, 460px) !important;
  border-radius: 10px !important;
  overflow: hidden !important;
  border: 1px solid var(--line) !important;
  background: #0f172a !important;
}
.media-preview img,
.media-preview video {
  width: 100% !important;
  height: 100% !important;
  object-fit: contain !important;
  background: #111827;
}
.tool-card {
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 10px;
  background: #fff;
}
.compact-tip {
  background: var(--accent-soft);
  border: 1px solid #bae6df;
  border-radius: 10px;
  padding: 8px 10px;
}
"""


def _ok(msg: str) -> str:
    return f"[OK] {msg}"


def _err(e: Exception) -> str:
    return f"[ERROR] {type(e).__name__}: {e}"


def run_img_merge(image_folder: str, output_name: str) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "merged.jpg")
        image_paths = ImageToolkit.list_images(image_folder)
        out = ImageToolkit.merge_horizontally(image_paths, output)
        return _ok(f"Merged {len(image_paths)} images -> {out}"), str(out)
    except Exception as e:
        return _err(e), None


def run_img_resize(image_path: str, scale_ratio: float, output_name: str) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "resized.jpg")
        out = ImageToolkit.resize_image(image_path, scale_ratio, output)
        return _ok(f"Saved: {out}"), str(out)
    except Exception as e:
        return _err(e), None


def run_png_to_jpg(image_path: str, output_name: str) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "converted.jpg")
        out = ImageToolkit.png_to_jpg(image_path, output)
        return _ok(f"Saved: {out}"), str(out)
    except Exception as e:
        return _err(e), None


def run_jpg_to_png(image_path: str, output_name: str) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "converted.png")
        out = ImageToolkit.jpg_to_png(image_path, output)
        return _ok(f"Saved: {out}"), str(out)
    except Exception as e:
        return _err(e), None


def run_mask_extract(origin_image: str, mask_image: str, keep_mode: str, output_name: str) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "mask_extract.jpg")
        out = ImageToolkit.get_subject_from_mask(origin_image, mask_image, output, keep_background_or_foreground=keep_mode)
        return _ok(f"Saved: {out}"), str(out)
    except Exception as e:
        return _err(e), None


def run_video_split(video_path: str, start_time: float, end_time: float, output_name: str) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "split.mp4")
        out = VideoToolkit.split_video_with_moviepy(video_path, start_time, end_time, output)
        return _ok(f"Saved: {out}"), str(out)
    except Exception as e:
        return _err(e), None


def run_video_center_crop(
    video_path: str,
    crop_size: int,
    crop_width: int,
    crop_height: int,
    output_name: str,
) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "center_crop.mp4")
        if crop_size > 0:
            out = ExperimentalToolkit.crop_video_center_square(video_path, output, crop_size=int(crop_size))
            return _ok(f"Saved (square {int(crop_size)}): {out}"), str(out)

        width = int(crop_width) if crop_width and int(crop_width) > 0 else None
        height = int(crop_height) if crop_height and int(crop_height) > 0 else None
        out = ExperimentalToolkit.crop_video_center(video_path, output, crop_width=width, crop_height=height)
        mode = "auto-square(min side)" if width is None and height is None else f"{width or height}x{height or width}"
        return _ok(f"Saved ({mode}): {out}"), str(out)
    except Exception as e:
        return _err(e), None


def _draw_roi(frame_rgb: np.ndarray, box: tuple[int, int, int, int] | None) -> np.ndarray:
    preview = frame_rgb.copy()
    if box is None:
        return preview

    import cv2

    x, y, w, h = box
    cv2.rectangle(preview, (x, y), (x + w, y + h), (255, 64, 64), 2)
    return preview


def _clamp_roi(frame_w: int, frame_h: int, x: int, y: int, w: int, h: int) -> tuple[int, int, int, int]:
    w = max(1, min(int(w), frame_w))
    h = max(1, min(int(h), frame_h))
    x = max(0, min(int(x), frame_w - w))
    y = max(0, min(int(y), frame_h - h))
    return x, y, w, h


def load_video_frame_for_roi(video_path: str) -> tuple[str, np.ndarray | None, dict[str, Any], int, int, int, int]:
    try:
        frames = VideoToolkit.read_video_frames_cv2(video_path, sample_rate=1)
        if not frames:
            raise RuntimeError("No frames decoded from video.")
        frame_bgr = frames[0]
        frame_rgb = frame_bgr[:, :, ::-1]

        h, w = frame_rgb.shape[:2]
        box_w = max(1, w // 2)
        box_h = max(1, h // 2)
        box_x = (w - box_w) // 2
        box_y = (h - box_h) // 2
        box = (box_x, box_y, box_w, box_h)

        state = {"frame_rgb": frame_rgb, "first_point": None, "box": box}
        preview = _draw_roi(frame_rgb, box)
        return _ok(f"Loaded first frame ({w}x{h}). Click image twice to set ROI corners."), preview, state, box_x, box_y, box_w, box_h
    except Exception as e:
        return _err(e), None, {"frame_rgb": None, "first_point": None, "box": None}, 0, 0, 0, 0


def on_roi_click(evt: gr.SelectData, state: dict[str, Any]) -> tuple[str, np.ndarray | None, dict[str, Any], int, int, int, int]:
    try:
        frame_rgb = state.get("frame_rgb")
        if frame_rgb is None:
            raise RuntimeError("Please load a video frame first.")

        if evt.index is None:
            raise RuntimeError("No click position captured.")

        x2, y2 = int(evt.index[0]), int(evt.index[1])
        first = state.get("first_point")

        if first is None:
            state["first_point"] = (x2, y2)
            preview = _draw_roi(frame_rgb, state.get("box"))
            bx = state.get("box") or (0, 0, 0, 0)
            return _ok(f"Start point set at ({x2}, {y2}). Click second point to finalize ROI."), preview, state, bx[0], bx[1], bx[2], bx[3]

        x1, y1 = first
        left = min(x1, x2)
        top = min(y1, y2)
        width = max(1, abs(x2 - x1))
        height = max(1, abs(y2 - y1))

        h, w = frame_rgb.shape[:2]
        left, top, width, height = _clamp_roi(w, h, left, top, width, height)
        state["box"] = (left, top, width, height)
        state["first_point"] = None

        preview = _draw_roi(frame_rgb, state["box"])
        return _ok(f"ROI updated: x={left}, y={top}, w={width}, h={height}"), preview, state, left, top, width, height
    except Exception as e:
        frame = state.get("frame_rgb")
        preview = _draw_roi(frame, state.get("box")) if frame is not None else None
        box = state.get("box") or (0, 0, 0, 0)
        return _err(e), preview, state, box[0], box[1], box[2], box[3]


def update_roi_from_sliders(x: int, y: int, width: int, height: int, state: dict[str, Any]) -> tuple[np.ndarray | None, dict[str, Any], int, int, int, int]:
    frame_rgb = state.get("frame_rgb")
    if frame_rgb is None:
        return None, state, 0, 0, 0, 0

    frame_h, frame_w = frame_rgb.shape[:2]
    x, y, width, height = _clamp_roi(frame_w, frame_h, x, y, width, height)
    state["box"] = (x, y, width, height)
    state["first_point"] = None
    preview = _draw_roi(frame_rgb, state["box"])
    return preview, state, x, y, width, height


def run_video_free_crop(video_path: str, x: int, y: int, width: int, height: int, output_name: str) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "free_crop.mp4")
        out = ExperimentalToolkit.crop_video_by_box(video_path, output, x, y, width, height)
        return _ok(f"Saved: {out}"), str(out)
    except Exception as e:
        return _err(e), None


def run_video_to_frames(video_path: str, only_first: bool, output_dir_name: str) -> tuple[str, list[str]]:
    try:
        output_dir = OUTPUT_DIR / (output_dir_name or "frames")
        saved = VideoToolkit.extract_frames(video_path, output_dir, only_first=only_first)
        preview = [str(p) for p in saved[:16]]
        return _ok(f"Extracted {len(saved)} frames -> {output_dir}"), preview
    except Exception as e:
        return _err(e), []


def run_video_to_gif(video_path: str, output_name: str, fps: int) -> tuple[str, str | None]:
    try:
        frames = VideoToolkit.read_video_frames_cv2(video_path)
        if not frames:
            raise RuntimeError("No frames decoded from video")

        from PIL import Image
        import imageio

        output = OUTPUT_DIR / (output_name or "video.gif")
        pil_frames = [Image.fromarray(frame[:, :, ::-1]) for frame in frames]
        imageio.mimsave(str(output), pil_frames, "GIF", duration=1000 / max(fps, 1), loop=0)
        return _ok(f"Saved: {output}"), str(output)
    except Exception as e:
        return _err(e), None


def run_video_to_audio(video_path: str, output_name: str) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "audio.mp3")
        out = VideoToolkit.video_to_audio(video_path, output)
        return _ok(f"Saved: {out}"), str(out)
    except Exception as e:
        return _err(e), None


def run_optical_flow(img1: str, img2: str, output_name: str) -> tuple[str, str | None]:
    try:
        output = OUTPUT_DIR / (output_name or "flow.png")
        flow_vis, _ = OpticalFlowToolkit.compute_between_images(img1, img2)

        import cv2

        cv2.imwrite(str(output), flow_vis)
        return _ok(f"Saved: {output}"), str(output)
    except Exception as e:
        return _err(e), None


def run_download_file(url: str, output_name: str) -> str:
    try:
        output = OUTPUT_DIR / (output_name or url.split("/")[-1])
        out = FileToolkit.download_url(url, output)
        return _ok(f"Downloaded: {out}")
    except Exception as e:
        return _err(e)


def run_text_pos(sentence: str) -> str:
    try:
        nouns, verbs = ExperimentalToolkit.pos_extract(sentence)
        return _ok(f"Nouns: {nouns}\nVerbs: {verbs}")
    except Exception as e:
        return _err(e)


def run_bump_version(level: str, note: str) -> str:
    try:
        new_version = bump_version(level=level, note=note)
        return _ok(f"Version updated to {new_version}")
    except Exception as e:
        return _err(e)


def switch_nav(section: str):
    sections = ["Home", "Image", "Video", "Optical Flow", "Data", "NLP", "Version"]
    return tuple(gr.update(visible=(section == item)) for item in sections)


def build_ui() -> gr.Blocks:
    with gr.Blocks(title="ElephantToolbox UI", css=APP_CSS) as demo:
        gr.Markdown(
            """
<div class="app-head">
  <h1>ElephantToolbox Workbench</h1>
  <p>面向图像、视频、数据与文本处理的一站式工作台</p>
</div>
"""
        )
        version_box = gr.Markdown(f"**Current Version:** `{get_version()}`")

        with gr.Row(elem_classes=["app-shell"]):
            with gr.Column(scale=3, min_width=220, elem_classes=["sidebar-nav"]):
                gr.Markdown("### 导航")
                nav = gr.Radio(
                    choices=["Home", "Image", "Video", "Optical Flow", "Data", "NLP", "Version"],
                    value="Home",
                    label="选择功能域",
                )
                gr.Markdown("按功能域切换工作区。")
                gr.Markdown("输出目录：`outputs/`", elem_classes=["compact-tip"])

            with gr.Column(scale=9, elem_classes=["content-panel"]):
                home_panel = gr.Column(visible=True)
                image_panel = gr.Column(visible=False)
                video_panel = gr.Column(visible=False)
                flow_panel = gr.Column(visible=False)
                data_panel = gr.Column(visible=False)
                nlp_panel = gr.Column(visible=False)
                version_panel = gr.Column(visible=False)

        with home_panel:
            gr.Markdown("### 产品概览")
            gr.Markdown(
                "- `Image`：图像拼接、缩放、格式转换、掩码主体提取。\n"
                "- `Video`：视频切分、中心裁剪、自由选区裁剪、抽帧、转 GIF、提取音频。\n"
                "- `Optical Flow`：计算两帧之间的光流并输出可视化结果。\n"
                "- `Data`：从 URL 下载文件到本地工作目录。\n"
                "- `NLP`：句子词性提取（名词与动词）。\n"
                "- `Version`：版本号管理与变更记录更新。"
            )

        with image_panel:
            gr.Markdown("### Image Tools", elem_classes=["section-title"])
            gr.Markdown("用于常见图像处理与素材准备任务。", elem_classes=["section-tip"])
            with gr.Tabs():
                with gr.Tab("Merge"):
                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown("将文件夹内图像按顺序横向拼接为一张图。")
                        img_folder = gr.Textbox(label="Image Folder")
                        img_merge_out = gr.Textbox(label="Output Name", value="merged.jpg")
                        img_merge_btn = gr.Button("Run Merge")
                        img_merge_log = gr.Textbox(label="Log")
                        img_merge_preview = gr.Image(label="Preview", elem_classes=["media-preview"])
                        img_merge_btn.click(run_img_merge, [img_folder, img_merge_out], [img_merge_log, img_merge_preview])

                with gr.Tab("Resize"):
                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown("按缩放比例统一调整单张图像尺寸。")
                        img_path = gr.Textbox(label="Image Path")
                        scale_ratio = gr.Number(label="Scale Ratio", value=0.5)
                        resize_out = gr.Textbox(label="Output Name", value="resized.jpg")
                        resize_btn = gr.Button("Run Resize")
                        resize_log = gr.Textbox(label="Log")
                        resize_preview = gr.Image(label="Preview", elem_classes=["media-preview"])
                        resize_btn.click(run_img_resize, [img_path, scale_ratio, resize_out], [resize_log, resize_preview])

                with gr.Tab("Convert"):
                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown("在 PNG 与 JPG/JPEG 之间进行格式转换。")
                        with gr.Row():
                            with gr.Column():
                                png_path = gr.Textbox(label="PNG Image Path")
                                png_out = gr.Textbox(label="Output Name", value="converted.jpg")
                                png_btn = gr.Button("PNG -> JPG")
                                png_log = gr.Textbox(label="Log")
                                png_preview = gr.Image(label="Preview", elem_classes=["media-preview"])
                                png_btn.click(run_png_to_jpg, [png_path, png_out], [png_log, png_preview])
                            with gr.Column():
                                jpg_path = gr.Textbox(label="JPG/JPEG Image Path")
                                jpg_out = gr.Textbox(label="Output Name", value="converted.png")
                                jpg_btn = gr.Button("JPG -> PNG")
                                jpg_log = gr.Textbox(label="Log")
                                jpg_preview = gr.Image(label="Preview", elem_classes=["media-preview"])
                                jpg_btn.click(run_jpg_to_png, [jpg_path, jpg_out], [jpg_log, jpg_preview])

                with gr.Tab("Mask Extract"):
                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown("根据掩码提取前景主体或背景区域。")
                        origin_image = gr.Textbox(label="Origin Image")
                        mask_image = gr.Textbox(label="Mask Image")
                        keep_mode = gr.Dropdown(["foreground", "background"], value="foreground", label="Keep Mode")
                        mask_out = gr.Textbox(label="Output Name", value="mask_extract.jpg")
                        mask_btn = gr.Button("Run Extract")
                        mask_log = gr.Textbox(label="Log")
                        mask_preview = gr.Image(label="Preview", elem_classes=["media-preview"])
                        mask_btn.click(run_mask_extract, [origin_image, mask_image, keep_mode, mask_out], [mask_log, mask_preview])

        with video_panel:
            gr.Markdown("### Video Tools", elem_classes=["section-title"])
            gr.Markdown("覆盖剪辑、裁剪、拆帧与格式导出等核心视频处理流程。", elem_classes=["section-tip"])
            free_roi_state = gr.State({"frame_rgb": None, "first_point": None, "box": (0, 0, 0, 0)})
            with gr.Tabs():
                with gr.Tab("Split / Crop"):
                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown("按时间区间切分视频片段。")
                        v_path = gr.Textbox(label="Video Path")
                        with gr.Row():
                            v_start = gr.Number(label="Start Time", value=0)
                            v_end = gr.Number(label="End Time", value=2)
                            v_out = gr.Textbox(label="Output Name", value="split.mp4")
                        v_btn = gr.Button("Run Split")
                        v_log = gr.Textbox(label="Log")
                        v_preview = gr.Video(label="Output Video", elem_classes=["media-preview"])
                        v_btn.click(run_video_split, [v_path, v_start, v_end, v_out], [v_log, v_preview])

                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown("从画面中心裁剪，支持正方形优先或自定义宽高。")
                        vc_path = gr.Textbox(label="Video Path")
                        with gr.Row():
                            vc_crop_size = gr.Number(label="Square Crop Size (priority)", value=0, precision=0)
                            vc_crop_w = gr.Number(label="Crop Width (when square size is 0)", value=0, precision=0)
                            vc_crop_h = gr.Number(label="Crop Height (when square size is 0)", value=0, precision=0)
                        vc_out = gr.Textbox(label="Output Name", value="center_crop.mp4")
                        vc_btn = gr.Button("Run Center Crop")
                        vc_log = gr.Textbox(label="Log")
                        vc_preview = gr.Video(label="Output Video", elem_classes=["media-preview"])
                        vc_btn.click(run_video_center_crop, [vc_path, vc_crop_size, vc_crop_w, vc_crop_h, vc_out], [vc_log, vc_preview])

                with gr.Tab("Free ROI Crop"):
                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown(
                            "通过交互方式指定任意裁剪区域（ROI），并应用到整段视频。\n"
                            "1. 点击 `Load First Frame` 载入首帧。\n"
                            "2. 在预览图上点击两次，确定 ROI 对角点。\n"
                            "3. 使用数字框微调 ROI，点击 `Update ROI Preview`。\n"
                            "4. 点击 `Crop Video By ROI` 导出结果。"
                        )
                        vfr_path = gr.Textbox(label="Video Path")
                        vfr_load_btn = gr.Button("Load First Frame")
                        vfr_log = gr.Textbox(label="Log")
                        vfr_image = gr.Image(label="ROI Selector", type="numpy", interactive=True, elem_classes=["media-preview"])
                        with gr.Row():
                            vfr_x = gr.Number(label="ROI X", value=0, precision=0)
                            vfr_y = gr.Number(label="ROI Y", value=0, precision=0)
                            vfr_w = gr.Number(label="ROI Width", value=0, precision=0)
                            vfr_h = gr.Number(label="ROI Height", value=0, precision=0)
                        with gr.Row():
                            vfr_update_btn = gr.Button("Update ROI Preview")
                            vfr_out = gr.Textbox(label="Output Name", value="free_crop.mp4")
                            vfr_crop_btn = gr.Button("Crop Video By ROI")
                        vfr_video = gr.Video(label="Cropped Video", elem_classes=["media-preview"])

                        vfr_load_btn.click(load_video_frame_for_roi, [vfr_path], [vfr_log, vfr_image, free_roi_state, vfr_x, vfr_y, vfr_w, vfr_h])
                        vfr_image.select(on_roi_click, [free_roi_state], [vfr_log, vfr_image, free_roi_state, vfr_x, vfr_y, vfr_w, vfr_h])
                        vfr_update_btn.click(update_roi_from_sliders, [vfr_x, vfr_y, vfr_w, vfr_h, free_roi_state], [vfr_image, free_roi_state, vfr_x, vfr_y, vfr_w, vfr_h])
                        vfr_crop_btn.click(run_video_free_crop, [vfr_path, vfr_x, vfr_y, vfr_w, vfr_h, vfr_out], [vfr_log, vfr_video])

                with gr.Tab("Convert / Extract"):
                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown("将视频解析为图像帧，支持仅导出首帧。")
                        vf_path = gr.Textbox(label="Video Path")
                        vf_only_first = gr.Checkbox(label="Only First Frame", value=False)
                        vf_out = gr.Textbox(label="Output Dir Name", value="frames")
                        vf_btn = gr.Button("Video -> Frames")
                        vf_log = gr.Textbox(label="Log")
                        vf_gallery = gr.Gallery(label="Frames Preview", columns=4, object_fit="contain", height=380)
                        vf_btn.click(run_video_to_frames, [vf_path, vf_only_first, vf_out], [vf_log, vf_gallery])

                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown("导出 GIF 动图，支持设置输出帧率。")
                        vg_path = gr.Textbox(label="Video Path")
                        vg_out = gr.Textbox(label="Output Name", value="video.gif")
                        vg_fps = gr.Slider(1, 30, value=8, step=1, label="FPS")
                        vg_btn = gr.Button("Video -> GIF")
                        vg_log = gr.Textbox(label="Log")
                        vg_preview = gr.Image(label="GIF Preview", elem_classes=["media-preview"])
                        vg_btn.click(run_video_to_gif, [vg_path, vg_out, vg_fps], [vg_log, vg_preview])

                    with gr.Group(elem_classes=["tool-card"]):
                        gr.Markdown("从视频中提取音频轨道为独立文件。")
                        va_path = gr.Textbox(label="Video Path")
                        va_out = gr.Textbox(label="Output Name", value="audio.mp3")
                        va_btn = gr.Button("Video -> Audio")
                        va_log = gr.Textbox(label="Log")
                        va_file = gr.File(label="Output Audio")
                        va_btn.click(run_video_to_audio, [va_path, va_out], [va_log, va_file])

        with flow_panel:
            gr.Markdown("### Optical Flow", elem_classes=["section-title"])
            gr.Markdown("输入两张图像，生成光流可视化结果，便于运动趋势分析。", elem_classes=["section-tip"])
            f_img1 = gr.Textbox(label="Image 1")
            f_img2 = gr.Textbox(label="Image 2")
            f_out = gr.Textbox(label="Output Name", value="flow.png")
            f_btn = gr.Button("Run")
            f_log = gr.Textbox(label="Log")
            f_preview = gr.Image(label="Flow Visualization", elem_classes=["media-preview"])
            f_btn.click(run_optical_flow, [f_img1, f_img2, f_out], [f_log, f_preview])

        with data_panel:
            gr.Markdown("### Data Tools", elem_classes=["section-title"])
            gr.Markdown("从指定 URL 下载文件并保存到输出目录。", elem_classes=["section-tip"])
            d_url = gr.Textbox(label="Download URL")
            d_out = gr.Textbox(label="Output Name", value="download.bin")
            d_btn = gr.Button("Download")
            d_log = gr.Textbox(label="Log")
            d_btn.click(run_download_file, [d_url, d_out], [d_log])

        with nlp_panel:
            gr.Markdown("### NLP Tools", elem_classes=["section-title"])
            gr.Markdown("对输入句子进行词性分析，输出名词与动词集合。", elem_classes=["section-tip"])
            n_sentence = gr.Textbox(label="Sentence")
            n_btn = gr.Button("POS Extract")
            n_log = gr.Textbox(label="Result")
            n_btn.click(run_text_pos, [n_sentence], [n_log])

        with version_panel:
            gr.Markdown("### Version Manager", elem_classes=["section-title"])
            gr.Markdown("管理项目版本号并写入变更记录。", elem_classes=["section-tip"])
            b_level = gr.Dropdown(["patch", "minor", "major"], value="patch", label="Bump Level")
            b_note = gr.Textbox(label="Change Note", value="UI update")
            b_btn = gr.Button("Bump Version")
            b_log = gr.Textbox(label="Log")
            b_btn.click(run_bump_version, [b_level, b_note], [b_log]).then(lambda: f"**Current Version:** `{get_version()}`", None, [version_box])

        nav.change(switch_nav, [nav], [home_panel, image_panel, video_panel, flow_panel, data_panel, nlp_panel, version_panel])

    return demo


def main() -> None:
    demo = build_ui()
    demo.launch(server_name="0.0.0.0", server_port=7860)


if __name__ == "__main__":
    main()
