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


def download(url):
    return FileToolkit.download_url(url)


def main() -> None:
    parser = argparse.ArgumentParser(description="Download file from URL.")
    parser.add_argument("--url", type=str, required=True)
    parser.add_argument("--output", type=str, default=None)
    args = parser.parse_args()

    out = FileToolkit.download_url(args.url, args.output)
    print(f"下载成功: {out}")


if __name__ == '__main__':
    main()
