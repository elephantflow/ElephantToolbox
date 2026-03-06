# ElephantToolbox 项目构建与演进记录

更新时间：2026-03-06

## 1. 目标与背景

本项目不仅用于“单次脚本处理”，还需要沉淀一批可复用函数，供后续新项目通过 `import` 直接调用。  
因此，项目架构目标从“脚本仓库”升级为“**可复用 Python 库 + CLI/UI 工具层**”。

核心要求：
- 不破坏已有脚本与功能。
- 新功能可以快速接入。
- 常用能力可稳定复用（跨项目 import）。

---

## 2. 框架思路（分层设计）

### 2.1 `toolbox/core`：库层（长期沉淀）

定位：稳定、可复用、参数化的函数/类。  
约束：
- 尽量无副作用（不在函数内部写死路径）。
- 输入显式参数化（路径、模型、阈值、策略等）。
- 输出结构统一（优先返回 `Path` 或结构化结果）。

### 2.2 `scripts/*`：任务入口层（批处理/一次性任务）

定位：命令行参数解析 + 调用 `toolbox/core`。  
约束：
- 不重复实现核心算法逻辑。
- 作为兼容层保留历史调用方式。

### 2.3 `toolbox/cli` 与 `toolbox/ui`

定位：交互层。  
约束：
- 只编排流程，不承载底层算法。
- 作为统一入口服务库层能力。

---

## 3. 本次已执行的具体改造

### 3.1 让项目可被安装为 Python 包

新增文件：
- `pyproject.toml`

落地内容：
- 使用 `setuptools` 作为构建后端。
- 声明基础依赖与可选依赖：
  - `ui`（gradio）
  - `ai`（torch/transformers/qwen-vl-utils/pandas）
- 注册命令行入口：`toolbox-cli = toolbox.cli.main:main`

收益：
- 新项目可通过 `pip install -e /path/to/ElephantToolbox` 复用本库。

---

### 3.2 稳定化顶层包导入面

更新文件：
- `toolbox/__init__.py`

落地内容：
- 新增 `__version__`（从根目录 `VERSION` 读取）。
- 调整 `__all__`，去除无效项并明确导出模块面。

收益：
- 外部项目可稳定读取版本与包入口，减少路径漂移。

---

### 3.3 新增核心 API 聚合入口（便于 import）

新增文件：
- `toolbox/core/api.py`

导出内容：
- `ImageToolkit`
- `VideoToolkit`
- `FileToolkit`
- `GifToolkit`
- `OpticalFlowToolkit`
- `ExperimentalToolkit`
- `QwenToolkit`

并更新：
- `toolbox/core/__init__.py` 增加 `api` 导出

收益：
- 新项目可统一写法：
  - `from toolbox.core.api import ImageToolkit, VideoToolkit`

---

## 4. 推荐使用方式（跨项目复用）

### 4.1 安装（开发模式）

```bash
cd /Users/gulucaptain/Documents/Github/ElephantToolbox
pip install -e .
```

如需 UI 或 AI 依赖：

```bash
pip install -e ".[ui]"
pip install -e ".[ai]"
```

### 4.2 在新项目中 import

```python
from toolbox.core.api import ImageToolkit, VideoToolkit

images = ImageToolkit.list_images("./assets")
out = VideoToolkit.video_to_audio("./input.mp4", "./output.mp3")
```

### 4.3 继续使用统一命令入口

```bash
toolbox-cli --list
toolbox-cli vid.split --input_video_path a.mp4 --output_video_path b.mp4 --start_time 0 --end_time 3
```

---

## 5. 后续扩展约定（新增功能必须遵循）

新增任意视频/音频/文本/AI能力时，按固定流程执行：

1. 在 `toolbox/core/<domain>.py` 实现可复用能力（先库化）。
2. 在 `scripts/<domain>/` 增加轻量 CLI 入口脚本。
3. 在 `toolbox/cli/main.py` 注册命令（含必要别名）。
4. 如需界面，再接入 `toolbox/ui`（非必须）。
5. 更新 `README.md` 与 `CHANGELOG.md`。
6. 保持旧功能兼容，不直接删除历史脚本（除非确认迁移完成）。

---

## 6. 版本与变更管理

- 当前版本：`VERSION` 文件维护。
- 变更历史：`CHANGELOG.md` 维护。
- 当外部 import API 发生不兼容改动时，建议使用 `minor/major` 升级并写明迁移说明。

---

## 7. 备注

本记录文件用于沉淀“架构思路 + 执行动作”，后续每轮结构性调整应追加到本文件，以保证项目长期可维护性和团队协作可追溯性。

---

## 8. 新增函数收录记录（2026-03-06）

来源脚本：
- `FunctionTmp/write_csv_for_cameranoise_training.py`

收录动作：
1. 将主要逻辑封装到 `toolbox/core/metadata.py`：
   - `DatasetMetadataToolkit.build_camera_noise_training_csv(...)`
2. 新增标准 CLI 入口：
   - `scripts/data/files/write_camera_noise_training_csv.py`
   - 命令：`data.camera-noise-csv`
3. 在 `toolbox/core/api.py` 暴露可 import 的工具类：
   - `DatasetMetadataToolkit`
4. 保持原脚本可运行，同时改为调用新核心函数，避免重复逻辑。

---

## 9. CSV 脚本整理与单元化（2026-03-06）

背景：
- `FunctionTmp` 中存在多份写 CSV 脚本，核心流程高度相似，但路径拼接和字段策略略有差异。

执行动作：
1. 扩展 `toolbox/core/metadata.py`，沉淀可复用逻辑单元：
   - `parse_delimited_pairs`
   - `write_csv_rows`
   - `load_prompt_map_from_txt`
   - `scan_videos`
   - `build_video_prompt_noise_csv_from_prompt_map`
   - `build_camera_noise_training_csv`（增强版）
   - `build_multicam_training_csv_from_description_txt`
   - `build_multicam_with_reference_csv_from_ann_txt`
   - `build_multicam_all_cams_csv_from_prompt_txt`
   - `build_openvid_camera_noise_csv`
2. 新增统一 CLI 入口：
   - `scripts/data/files/build_dataset_metadata_csv.py`
   - 命令：`data.meta-csv`（支持多子命令模板）
3. 将 `FunctionTmp` 中多个 `write_csv*.py` 改为调用核心模块，保留原脚本入口和原有硬编码参数语义。

结果：
- CSV 构建逻辑从“多份复制粘贴脚本”变成“核心可复用函数 + 轻量脚本包装”。
- 后续新项目可直接 `import toolbox` 复用这些数据构建能力。
