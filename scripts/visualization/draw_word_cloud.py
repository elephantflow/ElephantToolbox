from __future__ import annotations

import argparse

from matplotlib import pyplot as plt
from wordcloud import WordCloud


def main() -> None:
    parser = argparse.ArgumentParser(description="Draw word cloud from input text.")
    parser.add_argument("--text", default="hello, world, she, he, girl, man, animal")
    parser.add_argument("--output", default="entity.png")
    args = parser.parse_args()

    wc = WordCloud(scale=2, max_font_size=100, background_color='white', collocations=False)
    wc.generate_from_text(args.text)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    plt.tight_layout()
    wc.to_file(args.output)
    plt.savefig(args.output, dpi=200)
    print(f"Saved: {args.output}")


if __name__ == "__main__":
    main()
