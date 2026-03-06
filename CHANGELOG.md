# Changelog

## 0.3.10 - 2026-03-06
- Rewrote `README.md` with full navigation and two clear sections:
  - executable script commands (CLI),
  - importable reusable functions for external projects.
- Added per-feature descriptions, usage patterns, and runnable examples.
- Documented main-function focus with related-function references for nested logic.

## 0.3.9 - 2026-03-06
- Refactored multiple CSV-building scripts in `FunctionTmp` into reusable core metadata units.
- Extended `DatasetMetadataToolkit` with common parsing/writing and dataset-specific metadata builders.
- Added unified CLI command `data.meta-csv` with subcommands for caption-txt/multicam/openvid style workflows.
- Updated `FunctionTmp/write_csv*.py` scripts to call core reusable methods while keeping script entry behavior.

## 0.3.8 - 2026-03-06
- Added reusable dataset metadata utility:
  - `DatasetMetadataToolkit.build_camera_noise_training_csv` in `toolbox/core/metadata.py`.
- Added CLI wrapper `data.camera-noise-csv` for camera-noise training CSV generation.
- Exported the new toolkit in `toolbox.core.api` for cross-project import usage.
- Updated `FunctionTmp/write_csv_for_cameranoise_training.py` to call the new core function.

## 0.3.7 - 2026-03-06
- Renamed project from `Toolbox-main-refactor` to `ElephantToolbox`.
- Updated project naming in README, building notes, CLI/UI labels, and package metadata.
- Added installed command alias `elephant-toolbox` while keeping `toolbox-cli` for compatibility.

## 0.3.6 - 2026-03-06
- Added package build metadata (`pyproject.toml`) for editable install and cross-project import usage.
- Added stable API aggregation entrypoint: `toolbox/core/api.py`.
- Updated top-level package exports and `__version__` loading in `toolbox/__init__.py`.
- Added architecture/build record document: `building.md`.
- Updated README with library installation and import guidance.

## 0.3.5 - 2026-03-06
- Integrated Qwen inference workflows into unified ElephantToolbox CLI style.
- Added reusable `toolbox/core/qwen.py` for:
  - batch input collection (file/dir/txt list),
  - Qwen2-VL image inference,
  - Qwen3-VL video inference,
  - Qwen3 text refinement from CSV,
  - metadata CSV build from caption text pairs.
- Added runnable wrappers under `scripts/ml/qwen/` and registered new CLI commands.
- Kept original `Qwen/*.py` scripts untouched for backward compatibility.

## 0.3.4 - 2026-03-06
- UI redesign with stronger visual hierarchy and cleaner card-style layout.
- Added sidebar + per-domain tab grouping to reduce scrolling for task discovery.
- Improved media preview rendering with responsive fixed-height containers and `object-fit: contain`.

## 0.3.3 - 2026-03-06
- UI update

## 0.3.2 - 2026-03-06
- UI update

## 0.3.1 - 2026-03-06
- UI update

## 0.3.0 - 2026-03-06
- Added unified Gradio UI plan and implementation scaffold.
- Added runtime version management (`VERSION`, `CHANGELOG.md`, version bump utility module).
- Added UI entrypoint integration with `toolbox_cli.py` command dispatch.
