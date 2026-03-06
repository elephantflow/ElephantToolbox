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
from pathlib import Path

from toolbox.core.files import FileToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Download train/test file lists to folders.")
    parser.add_argument("--train_list", type=str, required=True)
    parser.add_argument("--test_list", type=str, required=True)
    parser.add_argument("--save_root", type=str, required=True)
    args = parser.parse_args()

    root = Path(args.save_root)
    train_dir = root / "train"
    test_dir = root / "test"

    train_saved = FileToolkit.batch_download_urls_from_file(args.train_list, train_dir)
    test_saved = FileToolkit.batch_download_urls_from_file(args.test_list, test_dir)
    print(f"train downloaded: {len(train_saved)}")
    print(f"test downloaded: {len(test_saved)}")


if __name__ == "__main__":
    main()
