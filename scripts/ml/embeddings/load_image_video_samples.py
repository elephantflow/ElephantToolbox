from __future__ import annotations

import argparse
import random
from typing import List

import numpy as np
import torch
from PIL import Image
from decord import VideoReader
from torchvision import transforms


def augmentation(images, transform, state=None):
    if state is not None:
        torch.set_rng_state(state)
    if isinstance(images, List):
        transformed_images = [transform(img) for img in images]
        return torch.stack(transformed_images, dim=0)
    return transform(images)


def main() -> None:
    parser = argparse.ArgumentParser(description="Sample video frames and run consistent transforms.")
    parser.add_argument("--video_path", required=True)
    parser.add_argument("--sample_frames", type=int, default=14)
    parser.add_argument("--sample_rate", type=int, default=8)
    parser.add_argument("--height", type=int, default=385)
    parser.add_argument("--width", type=int, default=256)
    args = parser.parse_args()

    video_reader = VideoReader(args.video_path)
    video_length = len(video_reader)

    clip_length = min(video_length, (args.sample_frames - 1) * args.sample_rate + 1)
    start_idx = random.randint(0, video_length - clip_length)
    batch_index = np.linspace(start_idx, start_idx + clip_length - 1, args.sample_frames, dtype=int).tolist()

    vid_pil_image_list = [Image.fromarray(video_reader[i].asnumpy()) for i in batch_index]
    ref_img = Image.fromarray(video_reader[random.randint(0, video_length - 1)].asnumpy())

    pixel_transform = transforms.Compose([
        transforms.Resize((args.height, args.width)),
        transforms.ToTensor(),
        transforms.Normalize([0.5], [0.5]),
    ])

    cond_transform = transforms.Compose([
        transforms.Resize((args.height, args.width)),
        transforms.ToTensor(),
    ])

    state = torch.get_rng_state()
    pixel_values_vid = augmentation(vid_pil_image_list, pixel_transform, state)
    pixel_values_pose = augmentation(vid_pil_image_list, cond_transform, state)
    pixel_values_ref_img = augmentation(ref_img, pixel_transform, state)

    print(pixel_values_vid.shape)
    print(pixel_values_pose.shape)
    print(pixel_values_ref_img.shape)
    print(pixel_values_vid.max(), pixel_values_vid.min())


if __name__ == "__main__":
    main()
