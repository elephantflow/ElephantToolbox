from __future__ import annotations

import argparse
import subprocess

import torch


def get_gpu_memory(gpu_id):
    result = subprocess.run(
        ['nvidia-smi', '--query-gpu=memory.total,memory.used', '--format=csv,nounits,noheader'],
        stdout=subprocess.PIPE,
        text=True,
        check=True,
    )
    memory = [line for line in result.stdout.split("\n") if line.strip()]
    total_memory, used_memory = [int(x.strip()) for x in memory[gpu_id].split(",")]
    return total_memory, used_memory


def main() -> None:
    parser = argparse.ArgumentParser(description="Check and optionally reserve GPU memory.")
    parser.add_argument("--gpu_id", type=int, default=0)
    parser.add_argument("--required_gb", type=float, default=12.0)
    parser.add_argument("--allocate", action="store_true")
    args = parser.parse_args()

    if not torch.cuda.is_available():
        raise SystemError("GPU is not available")

    total_memory, used_memory = get_gpu_memory(args.gpu_id)
    free_memory = total_memory - used_memory
    required_memory = int(args.required_gb * 1024)

    print(f"Total memory: {total_memory / 1024:.2f} GB")
    print(f"Used memory: {used_memory / 1024:.2f} GB")
    print(f"Free memory: {free_memory / 1024:.2f} GB")

    if args.allocate:
        if required_memory > free_memory:
            raise MemoryError(f"Not enough free memory to allocate {args.required_gb} GB")
        tensor = torch.empty(int(required_memory * 1024 ** 2 / 4), dtype=torch.float32, device=f'cuda:{args.gpu_id}')
        print(f"Successfully allocated {args.required_gb}GB of GPU memory.")
        del tensor


if __name__ == "__main__":
    main()
