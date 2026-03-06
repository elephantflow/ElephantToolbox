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


def getTimeInterval(target_date):
    return ExperimentalToolkit.birthday_interval_days(target_date)


def main() -> None:
    parser = argparse.ArgumentParser(description="Compute days interval from target date (YYYY-MM-DD) to today.")
    parser.add_argument("--target_date", required=True)
    args = parser.parse_args()

    print(getTimeInterval(args.target_date))


if __name__ == "__main__":
    main()
