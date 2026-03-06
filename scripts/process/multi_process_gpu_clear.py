from __future__ import annotations

import torch
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

from toolbox.core.process_pool import ProcessPoolRunnerNoInput
from scripts.process.process_function import save_images_clear


class SDVideoModelEvaluator:
    def __init__(self, process_num, process_function):
        self.process_num = process_num
        self.runner = ProcessPoolRunnerNoInput(process_num=process_num, process_function=process_function)

    def __call__(self):
        if not torch.cuda.is_available():
            print("No GPU found. Running as multiprocessing demo only.")
        results = self.runner.run_for_count(self.process_num)
        indexes, outputs = zip(*results) if results else ([], [])
        print(list(indexes), list(outputs))
        return "__call__ function executed finished."


if __name__ == "__main__":
    process_num = 4
    evaluator = SDVideoModelEvaluator(process_num=process_num, process_function=save_images_clear)
    _ = evaluator()
