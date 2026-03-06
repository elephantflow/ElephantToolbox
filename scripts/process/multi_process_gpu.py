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

from toolbox.core.process_pool import ProcessPoolRunner


def fake_gpu_infer(prompt_batch):
    score = [199 for _ in prompt_batch]
    return {"prompts": prompt_batch, "clip_scores": score}


class SDVideoModelEvaluator:
    def __init__(self):
        self.seed = 42
        self.prompts = [
            "a man is playing pingpang.",
            "a woman is playing pingpang.",
            "a child is playing pingpang.",
        ]
        self.batch_size = 1

    def __call__(self, process_num):
        if not torch.cuda.is_available():
            print("No GPU found. Running as multiprocessing demo only.")

        batches = [
            self.prompts[start_idx : start_idx + self.batch_size]
            for start_idx in range(0, len(self.prompts), self.batch_size)
        ]
        runner = ProcessPoolRunner(process_num=process_num, process_function=fake_gpu_infer)
        results = runner.run(batches)
        outputs = [item for _, item in results]
        print(outputs)
        return "__call__ function executed finished."


if __name__ == "__main__":
    evaluator = SDVideoModelEvaluator()
    process_num = 4
    _ = evaluator(process_num)
