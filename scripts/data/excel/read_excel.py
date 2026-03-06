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

from toolbox.core.data_io import ExcelToolkit


read_excel = ExcelToolkit.read_excel
get_max_row_column = ExcelToolkit.get_max_row_column
read_single_column = ExcelToolkit.read_single_column
read_single_row = ExcelToolkit.read_single_row
read_tables = ExcelToolkit.read_tables
save_excel = ExcelToolkit.save_excel


def main() -> None:
    parser = argparse.ArgumentParser(description="Read and write excel files.")
    parser.add_argument("--excel", type=str, required=True)
    parser.add_argument("--sheet", type=int, default=0)
    args = parser.parse_args()

    sheet = read_excel(args.excel, args.sheet)
    rows, cols = get_max_row_column(sheet)
    print(rows, cols)


if __name__ == "__main__":
    main()
