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
import os

from toolbox.core.files import FileToolkit


def down_repo(repo_id, allows=None, ignores=None, local_dir=""):
    return FileToolkit.download_hf_repo(repo_id, local_dir, allows or [], ignores or [])


def main() -> None:
    parser = argparse.ArgumentParser(description="Download model/data repo from HuggingFace.")
    parser.add_argument('--repo', type=str, required=True)
    parser.add_argument('--allows', nargs='+', default=[])
    parser.add_argument('--ignores', nargs='+', default=[])
    parser.add_argument('--local', type=str, required=True)
    args = parser.parse_args()

    local_dir = os.path.join(args.local, args.repo)
    out = down_repo(args.repo, args.allows, args.ignores, local_dir)
    print(f"Downloaded to: {out}")


if __name__ == "__main__":
    main()
