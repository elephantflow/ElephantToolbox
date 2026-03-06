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

import matplotlib.pyplot as plt
import numpy as np

from toolbox.core.experimental import ExperimentalToolkit


def main() -> None:
    parser = argparse.ArgumentParser(description="Run PCA variance analysis from ndarray-like text.")
    parser.add_argument("--save_prefix", default="pca")
    args = parser.parse_args()

    X = np.array([[2.5, 3.5, 3.0], [3.5, 2.0, 3.5], [2.0, 3.0, 4.0], [3.0, 3.5, 3.5]])
    variance_ratio, cumulative = ExperimentalToolkit.pca_variance(X)

    plt.figure(figsize=(6, 4))
    plt.bar(range(1, len(variance_ratio) + 1), variance_ratio)
    plt.xlabel('Principal Component')
    plt.ylabel('Variance Ratio')
    plt.title('Explained Variance Ratio by Principal Components')
    plt.savefig(f"{args.save_prefix}_variance.png", dpi=200)

    plt.figure(figsize=(6, 4))
    plt.plot(range(1, len(cumulative) + 1), cumulative, marker='o')
    plt.xlabel('Number of Components')
    plt.ylabel('Cumulative Variance Ratio')
    plt.title('Cumulative Explained Variance Ratio')
    plt.savefig(f"{args.save_prefix}_cumulative.png", dpi=200)

    print("Variance ratio:", variance_ratio)
    print("Cumulative variance ratio:", cumulative)


if __name__ == "__main__":
    main()
