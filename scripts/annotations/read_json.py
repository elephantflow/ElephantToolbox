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

from tqdm import tqdm

from toolbox.core.data_io import JsonToolkit


def readJson(json_path):
    return JsonToolkit.read_json(json_path)


def readJsonlines(jsonlines_path):
    return JsonToolkit.read_jsonl(jsonlines_path)


def writeJsonlines(save_path, data_dict=None, names=None, captions=None):
    if data_dict is None:
        data_dict = {}
    if names is None:
        names = []
    if captions is None:
        captions = []

    if data_dict:
        rows = [data_dict]
    else:
        rows = [{"caption": captions[i], "name": names[i]} for i in range(min(len(names), len(captions)))]
    return JsonToolkit.write_jsonl(save_path, rows)


def readMsrvttJson(json_path):
    data = readJson(json_path)
    sentences = data["sentences"]
    video_ids = []
    captions = []
    for ann in tqdm(sentences):
        video_id = ann['video_id']
        caption = ann['caption']
        if video_id not in video_ids:
            video_ids.append(video_id)
            captions.append(caption)
    return video_ids, captions


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Read json/jsonl utility.")
    parser.add_argument("--jsonl", type=str, required=True)
    args = parser.parse_args()

    for ann in readJsonlines(args.jsonl):
        print(ann)
