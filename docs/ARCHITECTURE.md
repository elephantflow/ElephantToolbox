# Architecture

## Design
- `toolbox/core/*`: core class-based modules (`ImageToolkit`, `VideoToolkit`, etc.).
- `scripts/*`: runnable command scripts grouped by domain.
- `toolbox/cli/main.py`: unified command dispatcher.
- `toolbox/ui/app.py`: Gradio visual interaction layer.
- `toolbox/versioning.py`: version read/bump + changelog update.

## Why this layout
- Clear separation of concerns: reusable logic vs runnable entrypoints vs UI layer.
- Consistent naming and discoverability.
- Easy to extend command and UI surfaces without duplicating core logic.

## Command Dispatch
`toolbox_cli.py` delegates commands by key to script modules.

Examples:
- `img.merge` -> `scripts.image.merge_images`
- `vid.split` -> `scripts.video.split_video`
- `data.download-hf` -> `scripts.data.files.download_huggingface`
- `ui.gradio` -> `toolbox.ui.app`

## Migration status
- Legacy uppercase category folders were removed.
- Script names were normalized.
- Redundant compatibility folder `common/` was removed after import migration.
