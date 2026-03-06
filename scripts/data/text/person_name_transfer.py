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

from toolbox.core.experimental import ExperimentalToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Convert 'Given Family' list to 'Family, Given' joined string.")
    parser.add_argument("--names", required=True)
    parser.add_argument("--keep_count", type=int, default=10)
    args = parser.parse_args()

    out = ExperimentalToolkit.transfer_person_names(args.names, keep_count=args.keep_count)
    print(out)


if __name__ == "__main__":
    main()
