from __future__ import annotations

from datetime import datetime
from typing import Callable, Iterable, Optional, TypeVar

import torch

TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class ProcessPoolRunner:
    """Queue-based multiprocessing helper."""

    def __init__(self, process_num: int, process_function: Callable[[TInput], TOutput]):
        torch.multiprocessing.set_start_method("spawn", force=True)
        torch.multiprocessing.set_sharing_strategy("file_system")
        self.process_num = process_num
        self.process_function = process_function

    def _infer(self, rank: int, q_input, q_output) -> None:
        print(f"In each function, the pid of this process is {rank}.")
        while True:
            payload = q_input.get()
            if payload is None:
                print(f"[{datetime.now()}] Process #{rank} ended.")
                break
            index, inputs = payload
            q_output.put((index, self.process_function(inputs)))

    def run(self, inputs: Iterable[TInput]) -> list[tuple[int, TOutput]]:
        q_input = torch.multiprocessing.Queue()
        q_output = torch.multiprocessing.Queue()

        processes = []
        for rank in range(self.process_num):
            p = torch.multiprocessing.Process(target=self._infer, args=(rank, q_input, q_output))
            p.start()
            processes.append(p)

        indexed_inputs = list(enumerate(inputs))
        for payload in indexed_inputs:
            q_input.put(payload)
        for _ in processes:
            q_input.put(None)

        results = [q_output.get() for _ in indexed_inputs]
        for p in processes:
            p.join()

        return sorted(results, key=lambda x: x[0])


class ProcessPoolRunnerNoInput(ProcessPoolRunner):
    """Variant for functions that do not require an input payload."""

    def __init__(self, process_num: int, process_function: Callable[[], TOutput]):
        super().__init__(process_num=process_num, process_function=lambda _: process_function())

    def run_for_count(self, task_count: Optional[int] = None) -> list[tuple[int, TOutput]]:
        count = self.process_num if task_count is None else task_count
        return self.run([None] * count)
