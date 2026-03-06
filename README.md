# ElephantToolbox

面向图像、视频、数据与深度学习模型推理流程的统一工具箱。  
本项目支持两种使用方式：
1. 直接运行脚本命令（CLI）。
2. 在其他项目中 `import toolbox` 复用核心函数。

## 目录导航
- [快速开始](#快速开始)
- [第一部分：可执行脚本（CLI）](#第一部分可执行脚本cli)
- [第二部分：可导入函数（供其他项目调用）](#第二部分可导入函数供其他项目调用)
- [项目结构](#项目结构)
- [版本与变更](#版本与变更)

## 快速开始

安装（开发模式）：

```bash
cd /Users/gulucaptain/Documents/Github/ElephantToolbox
pip install -e .
```

可选依赖：

```bash
pip install -e ".[ui]"
pip install -e ".[ai]"
```

查看全部命令：

```bash
python toolbox_cli.py --list
python toolbox_cli.py --list-all
```

---

## 第一部分：可执行脚本（CLI）

### 通用调用格式

```bash
python toolbox_cli.py <command> [args...]
```

获取某个功能的参数说明：

```bash
python toolbox_cli.py <command> --help
```

### 1. 图像处理（Image）

| 功能 | 命令 | 说明 | 用法示例 | 相关函数 |
|---|---|---|---|---|
| 图像横向拼接 | `img.merge` | 按顺序拼接图片 | `python toolbox_cli.py img.merge --image_folder ./assets/images --output_path ./outputs/merged.jpg` | `ImageToolkit.merge_horizontally`, `ImageToolkit.list_images` |
| 随机拼接图生成 | `img.merge-random` | 随机抽图拼接并输出多张 | `python toolbox_cli.py img.merge-random --input_dir ./assets/images --output_dir ./outputs/random_merge` | `ImageToolkit.build_random_merged_images` |
| 图像缩放 | `img.resize` | 按比例缩放单图 | `python toolbox_cli.py img.resize --image_path ./a.jpg --scale_ratio 0.5 --output_path ./outputs/a_resize.jpg` | `ImageToolkit.resize_image` |
| PNG 转 JPG | `img.png2jpg` | 格式转换 | `python toolbox_cli.py img.png2jpg --image_path ./a.png --output_path ./outputs/a.jpg` | `ImageToolkit.png_to_jpg` |
| JPG 转 PNG | `img.jpg2png` | 格式转换 | `python toolbox_cli.py img.jpg2png --image_path ./a.jpg --output_path ./outputs/a.png` | `ImageToolkit.jpg_to_png` |
| 掩码主体提取 | `img.mask` | 结合 mask 提取前景/背景 | `python toolbox_cli.py img.mask --real_image_path ./img.jpg --mask_image_path ./mask.png --output_path ./outputs/mask.jpg --keep_background_or_foreground foreground` | `ImageToolkit.get_subject_from_mask` |
| 姿态图增强 | `img.pose` | 增强姿态图显示效果 | `python toolbox_cli.py img.pose --pose_img_path ./pose.png --output_path ./outputs/pose_enhance.png` | `ImageToolkit.enhance_pose_image` |
| 三联图切分 | `img.split-merged` | 截取三联图右侧区域 | `python toolbox_cli.py img.split-merged --image_path ./triptych.jpg --output_path ./outputs/right.jpg` | `ImageToolkit.split_triptych_right` |
| 高斯模糊 | `img.blur` | 图像模糊处理 | `python toolbox_cli.py img.blur --image_path ./a.jpg --output_path ./outputs/blur.jpg --kernel 31 --sigma 15` | `ExperimentalToolkit.gaussian_blur_image` |

### 2. 视频处理（Video）

| 功能 | 命令 | 说明 | 用法示例 | 相关函数 |
|---|---|---|---|---|
| 视频切分 | `vid.split` | 按时间段切分视频 | `python toolbox_cli.py vid.split --input_video_path ./in.mp4 --output_video_path ./out.mp4 --start_time 1 --end_time 3` | `VideoToolkit.split_video_with_moviepy` |
| 批量二分切视频 | `vid.split-batch` | 批量将视频切为两段 | `python toolbox_cli.py vid.split-batch --input_dir ./videos --output_dir ./outputs` | `VideoToolkit.split_video_with_moviepy` |
| 视频转音频 | `vid.to-audio` | 导出音轨 | `python toolbox_cli.py vid.to-audio --video_path ./in.mp4 --audio_path ./out.mp3` | `VideoToolkit.video_to_audio` |
| 视频转 GIF | `vid.to-gif` | 视频生成 GIF | `python toolbox_cli.py vid.to-gif --video_path ./in.mp4 --output_path ./out.gif` | `VideoToolkit.read_video_frames_cv2`, `GifToolkit.frames_to_gif` |
| 视频抽帧 | `vid.to-frames` | 导出帧图像 | `python toolbox_cli.py vid.to-frames --video_path ./in.mp4 --output_dir ./frames` | `VideoToolkit.extract_frames` |
| 帧合成视频 | `vid.from-frames` | 图片序列生成视频 | `python toolbox_cli.py vid.from-frames --frame_dir ./frames --video_save_path ./out.mp4 --fps 15` | `VideoToolkit.frames_to_video` |
| 中心裁剪 | `vid.crop-center` | 按中心区域裁剪视频 | `python toolbox_cli.py vid.crop-center --input_video_path ./in.mp4 --output_video_path ./crop.mp4 --crop_size 768` | `ExperimentalToolkit.crop_video_center`, `ExperimentalToolkit.crop_video_center_square` |
| 视频尺寸调整 | `vid.resize` | 调整视频分辨率 | `python toolbox_cli.py vid.resize --input_video_path ./in.mp4 --output_video_path ./resize.mp4 --fixed_size 512` | `VideoToolkit.resize_video` |
| 图像+双视频拼接 | `vid.merge-image` | 合并两路视频与中间图像 | `python toolbox_cli.py vid.merge-image --video1_path ./a.mp4 --video2_path ./b.mp4 --image_path ./mid.jpg --output_path ./merge.mp4` | `VideoToolkit.combine_videos_with_image` |

### 3. 数据与文件（Data）

| 功能 | 命令 | 说明 | 用法示例 | 相关函数 |
|---|---|---|---|---|
| URL 下载 | `data.download` | 下载单个文件 | `python toolbox_cli.py data.download --url https://example.com/a.zip --output ./outputs/a.zip` | `FileToolkit.download_url` |
| HuggingFace 下载 | `data.download-hf` | 拉取仓库文件 | `python toolbox_cli.py data.download-hf --repo_id xxx/yyy --local_dir ./outputs/hf` | `FileToolkit.download_hf_repo` |
| 文件批量重命名 | `data.rename` | 随机后顺序重命名 | `python toolbox_cli.py data.rename --folder_path ./videos --suffix .mp4` | `FileToolkit.rename_randomized_sequential` |
| Excel 读取 | `data.excel` | 读取指定 sheet 内容 | `python toolbox_cli.py data.excel --file_name ./a.xlsx --sheet_number 0` | `ExcelToolkit.read_excel` |
| CameraNoise CSV 构建 | `data.camera-noise-csv` | 按视频+noise+caption 生成训练 CSV | `python toolbox_cli.py data.camera-noise-csv --video_root /data/videos --noise_root /data/noises --caption_metadata_txt ./captions.txt --output_csv ./metadata.csv` | `DatasetMetadataToolkit.build_camera_noise_training_csv` |
| 统一元数据 CSV 构建 | `data.meta-csv` | 多模板构建 CSV（caption/multicam/openvid） | `python toolbox_cli.py data.meta-csv from-caption-txt --video_root /data/videos --noise_root /data/noises --caption_metadata_txt ./captions.txt --output_csv ./meta.csv` | `DatasetMetadataToolkit.*` |

`data.meta-csv` 子模式：
- `from-caption-txt`
- `from-prompt-map-folder`
- `multicam-from-desc`
- `multicam-with-reference`
- `multicam-all-cams`
- `openvid`

### 4. 光流（Optical Flow）

| 功能 | 命令 | 说明 | 用法示例 | 相关函数 |
|---|---|---|---|---|
| 两图光流计算 | `flow.compute` | 计算并保存光流结果 | `python toolbox_cli.py flow.compute --img1 ./a.png --img2 ./b.png --output_path ./flow.npy` | `OpticalFlowToolkit.compute_between_images` |
| 光流可视化绘制 | `flow.draw` | 输出可视化图像 | `python toolbox_cli.py flow.draw --img1 ./a.png --img2 ./b.png --output_path ./flow_vis.png` | `OpticalFlowToolkit.flow_to_color` |

### 5. 进程（Process）

| 功能 | 命令 | 说明 | 用法示例 | 相关函数 |
|---|---|---|---|---|
| CPU 多进程示例 | `proc.cpu` | CPU 并行任务执行 | `python toolbox_cli.py proc.cpu` | `MultiProcessPool` |
| GPU 多进程示例 | `proc.gpu` | GPU 并行任务执行 | `python toolbox_cli.py proc.gpu` | `MultiProcessPoolBySharedInput` |

### 6. 可视化（Visualization）

| 功能 | 命令 | 说明 | 用法示例 | 相关函数 |
|---|---|---|---|---|
| 词云图 | `viz.wordcloud` | 文本词云可视化 | `python toolbox_cli.py viz.wordcloud --text "hello world"` | `draw_word_cloud` 脚本 |
| 分组柱状图 | `viz.bar` | 分组数据可视化 | `python toolbox_cli.py viz.bar` | `draw_grouped_bar` 脚本 |
| 视频时序图 | `viz.temporal` | 绘制时序趋势 | `python toolbox_cli.py viz.temporal` | `draw_video_temporal` 脚本 |

### 7. Qwen 推理（AI）

| 功能 | 命令 | 说明 | 用法示例 | 相关函数 |
|---|---|---|---|---|
| Qwen 元数据融合 | `ai.qwen.meta-csv` | 两类 caption 文本合并为 CSV | `python toolbox_cli.py ai.qwen.meta-csv --image_caption_txt ./img.txt --camera_caption_txt ./cam.txt --output_csv ./meta.csv` | `QwenToolkit.build_metadata_csv_from_pair_texts` |
| Qwen2-VL 图像推理 | `ai.qwen2vl.image` | 批量图像推理并写入 txt | `python toolbox_cli.py ai.qwen2vl.image --model_path /path/model --input_path ./frames --input_type dir --output_txt ./qwen2vl.txt` | `QwenToolkit.qwen2vl_infer_images` |
| Qwen3-VL 视频推理 | `ai.qwen3vl.video` | 批量视频推理并写入 txt | `python toolbox_cli.py ai.qwen3vl.video --model_path /path/model --input_path ./videos.txt --input_type txt --output_txt ./qwen3vl.txt` | `QwenToolkit.qwen3vl_infer_videos` |
| Qwen3 文本融合推理 | `ai.qwen3.text` | 读取 CSV 执行文本推理 | `python toolbox_cli.py ai.qwen3.text --model_path /path/model --input_csv ./meta.csv --output_txt ./refined.txt` | `QwenToolkit.qwen3_text_refine_from_csv` |

### 8. UI

| 功能 | 命令 | 说明 | 用法示例 | 相关函数 |
|---|---|---|---|---|
| Gradio 可视化工作台 | `ui.gradio` | 启动 Web 交互界面 | `python toolbox_cli.py ui.gradio` | `toolbox.ui.app.build_ui` |

---

## 第二部分：可导入函数（供其他项目调用）

推荐统一入口：

```python
from toolbox.core.api import (
    ImageToolkit,
    VideoToolkit,
    FileToolkit,
    OpticalFlowToolkit,
    DatasetMetadataToolkit,
    QwenToolkit,
    ExperimentalToolkit,
    GifToolkit,
)
```

### 1. 图像主函数

#### 1.1 `ImageToolkit.merge_horizontally`
- 功能：将多张图按最小高度对齐后横向拼接。
- 相关函数：`ImageToolkit.list_images`, `ImageToolkit.resize_to_height`。
- 用法与示例：

```python
from toolbox.core.api import ImageToolkit

images = ImageToolkit.list_images("./assets/images")
out = ImageToolkit.merge_horizontally(images, "./outputs/merged.jpg")
print(out)
```

#### 1.2 `ImageToolkit.get_subject_from_mask`
- 功能：根据掩码提取前景或背景。
- 相关函数：`ImageToolkit.png_to_jpg`, `ImageToolkit.jpg_to_png`。
- 用法与示例：

```python
from toolbox.core.api import ImageToolkit

out = ImageToolkit.get_subject_from_mask(
    real_image_path="./img.jpg",
    mask_image_path="./mask.png",
    output_path="./outputs/mask_subject.jpg",
    keep_background_or_foreground="foreground",
)
```

### 2. 视频主函数

#### 2.1 `VideoToolkit.split_video_with_moviepy`
- 功能：按时间区间切视频。
- 相关函数：`VideoToolkit.split_video_with_ffmpeg`。
- 用法与示例：

```python
from toolbox.core.api import VideoToolkit

out = VideoToolkit.split_video_with_moviepy("./in.mp4", 1.0, 3.0, "./outputs/part.mp4")
```

#### 2.2 `VideoToolkit.extract_frames`
- 功能：导出视频帧到目录。
- 相关函数：`VideoToolkit.read_video_frames_cv2`。
- 用法与示例：

```python
from toolbox.core.api import VideoToolkit

frames = VideoToolkit.extract_frames("./in.mp4", "./outputs/frames", only_first=False)
print(len(frames))
```

#### 2.3 `ExperimentalToolkit.crop_video_center`
- 功能：中心区域裁剪视频（moviepy实现）。
- 相关函数：`ExperimentalToolkit.crop_video_center_square`, `ExperimentalToolkit.crop_video_by_box`。
- 用法与示例：

```python
from toolbox.core.api import ExperimentalToolkit

out = ExperimentalToolkit.crop_video_center(
    video_path="./in.mp4",
    output_path="./outputs/crop.mp4",
    crop_width=720,
    crop_height=720,
)
```

### 3. 数据与 CSV 主函数

#### 3.1 `DatasetMetadataToolkit.build_camera_noise_training_csv`
- 功能：从 `caption txt + video目录 + noise目录` 构建标准训练 CSV。
- 相关函数：`DatasetMetadataToolkit.load_prompt_map_from_txt`, `DatasetMetadataToolkit.scan_videos`, `DatasetMetadataToolkit.write_csv_rows`。
- 用法与示例：

```python
from toolbox.core.api import DatasetMetadataToolkit

out_csv, count = DatasetMetadataToolkit.build_camera_noise_training_csv(
    video_root="/data/videos",
    noise_root="/data/noises",
    caption_metadata_txt="./captions.txt",
    output_csv="./outputs/metadata.csv",
    caption_key_mode="stem",
    recursive=False,
)
```

#### 3.2 `DatasetMetadataToolkit.build_multicam_with_reference_csv_from_ann_txt`
- 功能：构建含 `reference_video` 的多机位训练 CSV。
- 相关函数：`DatasetMetadataToolkit.parse_delimited_pairs`, `DatasetMetadataToolkit.write_csv_rows`。
- 用法与示例：

```python
from toolbox.core.api import DatasetMetadataToolkit

out_csv, count = DatasetMetadataToolkit.build_multicam_with_reference_csv_from_ann_txt(
    ann_txt="./video_anns.txt",
    video_root="/data/multicam/train",
    noise_root="/data/multicam/noises",
    output_csv="./outputs/meta_ref.csv",
    random_seed=42,
    max_rows=3000,
)
```

#### 3.3 `DatasetMetadataToolkit.build_openvid_camera_noise_csv`
- 功能：从 OpenVid 源 CSV 过滤并生成 camera-noise 训练 CSV。
- 相关函数：`DatasetMetadataToolkit.write_csv_rows`。
- 用法与示例：

```python
from toolbox.core.api import DatasetMetadataToolkit

out_csv, count = DatasetMetadataToolkit.build_openvid_camera_noise_csv(
    source_csv="./OpenVidHD.csv",
    video_root="/data/OpenVidHD",
    noise_root="/data/OpenVid/noises",
    output_csv="./outputs/openvid_meta.csv",
)
```

### 4. Qwen 主函数

#### 4.1 `QwenToolkit.qwen2vl_infer_images`
- 功能：批量图像视觉理解并保存为 `txt`。
- 相关函数：`QwenToolkit.collect_inputs`, `QwenToolkit._append_line`。
- 用法与示例：

```python
from toolbox.core.api import QwenToolkit

images = QwenToolkit.collect_inputs("./frames", input_type="dir", allowed_exts=QwenToolkit.IMAGE_EXTS)
out = QwenToolkit.qwen2vl_infer_images(
    model_path="/path/to/Qwen2-VL-7B-Instruct",
    images=images,
    prompt="Please describe the content of the image in detail.",
    output_txt="./outputs/qwen2vl.txt",
)
```

#### 4.2 `QwenToolkit.qwen3vl_infer_videos`
- 功能：批量视频理解并保存为 `txt`。
- 相关函数：`QwenToolkit.collect_inputs`, `QwenToolkit._append_line`。
- 用法与示例：

```python
from toolbox.core.api import QwenToolkit

videos = QwenToolkit.collect_inputs("./videos.txt", input_type="txt", allowed_exts=QwenToolkit.VIDEO_EXTS)
out = QwenToolkit.qwen3vl_infer_videos(
    model_path="/path/to/Qwen3-VL-30B-A3B-Instruct",
    videos=videos,
    prompt="Tell me how the camera lens moves and changes its orientation while shooting the video.",
    output_txt="./outputs/qwen3vl.txt",
)
```

#### 4.3 `QwenToolkit.qwen3_text_refine_from_csv`
- 功能：读取 CSV 并进行文本融合/改写推理。
- 相关函数：`QwenToolkit.build_metadata_csv_from_pair_texts`。
- 用法与示例：

```python
from toolbox.core.api import QwenToolkit

out = QwenToolkit.qwen3_text_refine_from_csv(
    model_path="/path/to/Qwen3-30B-A3B-Instruct-2507",
    input_csv="./outputs/meta.csv",
    output_txt="./outputs/refined.txt",
    image_desc_field="image_description",
    camera_desc_field="camera_description",
    question="Integrate camera pose into image description in one short sentence.",
)
```

### 5. 文件与光流主函数

#### 5.1 `FileToolkit.download_url`
- 功能：下载远程文件。
- 相关函数：`FileToolkit.batch_download_urls_from_file`, `FileToolkit.download_hf_repo`。
- 用法与示例：

```python
from toolbox.core.api import FileToolkit

out = FileToolkit.download_url("https://example.com/a.zip", "./outputs/a.zip")
```

#### 5.2 `OpticalFlowToolkit.compute_between_images`
- 功能：计算两张图像的光流与可视化结果。
- 相关函数：`OpticalFlowToolkit.compute_farneback_flow`, `OpticalFlowToolkit.flow_to_color`。
- 用法与示例：

```python
from toolbox.core.api import OpticalFlowToolkit

flow_vis, flow = OpticalFlowToolkit.compute_between_images("./a.png", "./b.png")
```

### 6. GIF 主函数

#### 6.1 `GifToolkit.frames_to_gif`
- 功能：图片序列转 GIF。
- 相关函数：`GifToolkit.gif_to_frames`, `GifToolkit.concatenate_gifs`。
- 用法与示例：

```python
from toolbox.core.api import GifToolkit

out = GifToolkit.frames_to_gif(
    image_paths=["./frames/0001.png", "./frames/0002.png"],
    save_path="./outputs/out.gif",
    fps=8,
)
```

---

## 项目结构

```text
toolbox/
  core/      # 可复用函数（供 import）
  cli/       # 统一命令分发
  ui/        # gradio 可视化
  utils/
  versioning.py

scripts/
  image/
  video/
  optical_flow/
  data/
    files/
  process/
  visualization/
  ml/
    qwen/
```

---

## 版本与变更
- 当前版本：`VERSION`
- 变更历史：`CHANGELOG.md`
- 架构与构建记录：`building.md`
- 旧路径映射：`docs/MIGRATION_MAP.md`
