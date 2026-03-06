from __future__ import annotations

import argparse

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw grouped bar chart from CSV.")
    parser.add_argument("--csv", required=False, default="")
    parser.add_argument("--save_path", default="radio_plot.png")
    args = parser.parse_args()

    if args.csv:
        df = pd.read_csv(args.csv)
    else:
        data = {
            'Methods': ['UCoFIA', 'Align&Tell', 'X-CLIP', 'Ours'],
            'R@1-DiDeMo': [46.5, 0, 47.8, 49.6],
            'R@5-DiDeMo': [74.8, np.nan, 79.3, 76.5],
            'R@1-MSVD': [47.4, 49.3, 50.4, 50.6],
            'R@5-MSVD': [77.6, 79.1, 80.6, 78.7],
        }
        df = pd.DataFrame(data)

    df_filled = df.fillna(0)
    metrics = [c for c in df_filled.columns if c != 'Methods']
    df_long = pd.melt(df_filled, id_vars=['Methods'], value_vars=metrics, var_name='Metric', value_name='Value')

    sns.set(style="whitegrid")
    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x="Metric", y="Value", hue="Methods", data=df_long, errorbar=None, dodge=True, width=0.5)
    plt.xticks(rotation=45, ha="right")

    for p in ax.patches:
        ax.annotate(
            f'{p.get_height():.1f}',
            (p.get_x() + p.get_width() / 2., p.get_height()),
            ha='center',
            va='center',
            fontsize=10,
            color='black',
            xytext=(0, 5),
            textcoords='offset points',
        )

    plt.ylabel('Text-to-Video performance')
    plt.tight_layout()
    plt.savefig(args.save_path, dpi=200)
    print(f"Saved: {args.save_path}")


if __name__ == "__main__":
    main()
