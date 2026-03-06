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


DEFAULT_FOOD_LIST = [
    "湘西小炒",
    "马英贞牛肉面",
    "炒年糕店",
    "吉祥馄饨",
    "红色招聘牛肉面",
    "川锦汇 麻辣烫",
    "百成福 牛肉面",
    "顺德烧鹅",
    "牛肉汤馆",
    "红烧牛肉面-黄焖鸡",
]


def main() -> None:
    parser = argparse.ArgumentParser(description="Pick food using majority random voting.")
    parser.add_argument("--voters", type=int, default=5)
    args = parser.parse_args()

    food, indices = ExperimentalToolkit.choose_food(DEFAULT_FOOD_LIST, voters=args.voters)
    print(indices)
    print(f"今天吃: {food}")


if __name__ == "__main__":
    main()
