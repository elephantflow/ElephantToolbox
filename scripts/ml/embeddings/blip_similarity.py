from __future__ import annotations

import argparse
import os

import torch
from PIL import Image
from lavis.models import load_model_and_preprocess
from tqdm import tqdm

from toolbox.core.data_io import JsonToolkit


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model, vis_processors, text_processors = load_model_and_preprocess(
    "blip_image_text_matching", "large", device=device, is_eval=True
)


def blip_visualization(image_path, caption):
    raw_image = Image.open(image_path).convert("RGB")
    img = vis_processors["eval"](raw_image).unsqueeze(0).to(device)
    txt = text_processors["eval"](caption)

    sim1 = model({"image": img, "text_input": txt}, match_head="itc").detach().cpu().numpy()
    sim2 = model({"image": img, "text_input": txt + " " + txt + " " + txt}, match_head="itc").detach().cpu().numpy()
    return sim1, sim2


def main() -> None:
    parser = argparse.ArgumentParser(description="Run BLIP ITM similarity comparison on jsonl annotations.")
    parser.add_argument("--jsonl", required=True, help="jsonl with fields: clip_name, caption")
    parser.add_argument("--frame_root", required=True, help="folder containing <clip_name>.jpg")
    args = parser.parse_args()

    data = JsonToolkit.read_jsonl(args.jsonl)
    sim1bigger = 0
    sim2bigger = 0
    simequal = 0

    for ann in tqdm(data):
        video_frame_path = os.path.join(args.frame_root, ann["clip_name"] + ".jpg")
        caption = ann["caption"]
        try:
            sim1, sim2 = blip_visualization(video_frame_path, caption)
            if sim1 > sim2:
                sim1bigger += 1
            elif sim1 == sim2:
                simequal += 1
            else:
                sim2bigger += 1
        except Exception as e:
            print(f"skip {video_frame_path}: {e}")

    total = sim1bigger + sim2bigger + simequal
    print(f"sim1bigger number is: {sim1bigger}")
    print(f"sim2bigger number is: {sim2bigger}")
    print(f"simequal number is: {simequal}")
    print(f"total number is: {total}")


if __name__ == "__main__":
    main()
