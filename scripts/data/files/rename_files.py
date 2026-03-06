from __future__ import annotations

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

import argparse

from toolbox.core.files import FileToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Rename files under subfolders to sequential names.")
    parser.add_argument("--folder", type=str, required=True)
    parser.add_argument("--suffix", type=str, default=".mp4")
    args = parser.parse_args()

    total = FileToolkit.rename_randomized_sequential(args.folder, suffix=args.suffix)
    print(f"Renamed files: {total}")


if __name__ == "__main__":
    main()
