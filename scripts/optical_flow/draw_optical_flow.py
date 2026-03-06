from __future__ import annotations

import argparse

import cv2
import numpy as np
import torch
from torchvision.utils import flow_to_image


def flow_to_image_torch(flow):
    flow_t = torch.from_numpy(np.transpose(flow, [2, 0, 1]))
    flow_im = flow_to_image(flow_t)
    return np.transpose(flow_im.numpy(), [1, 2, 0])


def draw_flow(im, flow, step=40, norm=1):
    h, w = im.shape[:2]
    y, x = np.mgrid[step / 2:h:step, step / 2:w:step].reshape(2, -1).astype(int)
    if norm:
        fx, fy = flow[y, x].T / (abs(flow[y, x]).max() + 1e-8) * step // 2
    else:
        fx, fy = flow[y, x].T
    ex = x + fx
    ey = y + fy
    lines = np.vstack([x, y, ex, ey]).T.reshape(-1, 2, 2).astype(np.uint32)
    vis = im.astype(np.uint8)
    for (x1, y1), (x2, y2) in lines:
        cv2.line(vis, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.circle(vis, (x1, y1), 2, (0, 0, 255), -1)
    return vis


def draw_optical_flow(flow):
    h, w = flow.shape[:2]
    magnitude, angle = cv2.cartToPolar(flow[..., 0], flow[..., 1])
    hsv = np.zeros((h, w, 3), dtype=np.float32)
    hsv[..., 0] = angle * 180 / np.pi / 2
    hsv[..., 1] = 1.0
    hsv[..., 2] = cv2.normalize(magnitude, None, 0.0, 1.0, cv2.NORM_MINMAX)
    return (cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR) * 255).astype(np.uint8)


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize optical flow between two images.")
    parser.add_argument("--img1", required=True)
    parser.add_argument("--img2", required=True)
    parser.add_argument("--save_path", required=True)
    parser.add_argument("--mode", choices=["hsv", "torch", "arrow"], default="torch")
    args = parser.parse_args()

    frame1 = cv2.imread(args.img1)
    frame2 = cv2.imread(args.img2)
    if frame1 is None or frame2 is None:
        raise FileNotFoundError("Cannot read input images")

    prev = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    nxt = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prev, nxt, None, 0.5, 3, 15, 3, 5, 1.2, 0)

    if args.mode == "hsv":
        flow_vis = draw_optical_flow(flow)
    elif args.mode == "arrow":
        flow_vis = draw_flow(frame2, flow, step=40, norm=1)
    else:
        flow_vis = flow_to_image_torch(flow)

    cv2.imwrite(args.save_path, flow_vis)
    print(f"Saved: {args.save_path}")


if __name__ == "__main__":
    main()
