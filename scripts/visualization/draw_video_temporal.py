from __future__ import annotations

import argparse

import cv2
import matplotlib.pyplot as plt
import numpy as np


def compute_optical_flow(video_path, max_frames=16, resize=(32, 32)):
    cap = cv2.VideoCapture(video_path)
    flows = []

    ret, prev = cap.read()
    if not ret:
        return np.array([])
    prev = cv2.resize(prev, resize)
    prev_gray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)

    while cap.isOpened() and len(flows) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.resize(frame, resize)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        flow = cv2.calcOpticalFlowFarneback(prev_gray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
        mag, _ = cv2.cartToPolar(flow[..., 0], flow[..., 1])
        flows.append(np.clip(mag, 0, 15) / 15)
        prev_gray = gray

    cap.release()
    return np.array(flows)


def visualize_volume_scalar(volume, cmap='viridis', point_size=4, save_path='flow_vis.png'):
    if volume.size == 0:
        raise ValueError("Empty volume")
    T, H, W = volume.shape
    xs, ys, zs = np.meshgrid(np.arange(W), np.arange(H), np.arange(T))

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(xs.flatten(), ys.flatten(), zs.flatten(), c=volume.flatten(), cmap=cmap, s=point_size, alpha=0.9)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_zticks([])
    ax.view_init(elev=30, azim=120)
    plt.savefig(save_path, bbox_inches='tight', dpi=300)


def main() -> None:
    parser = argparse.ArgumentParser(description="Visualize video temporal optical-flow volume.")
    parser.add_argument("--video_path", required=True)
    parser.add_argument("--save_path", default="flow_vis.png")
    parser.add_argument("--max_frames", type=int, default=16)
    args = parser.parse_args()

    vol = compute_optical_flow(args.video_path, max_frames=args.max_frames)
    visualize_volume_scalar(vol, cmap='plasma', save_path=args.save_path)
    print(f"Saved: {args.save_path}")


if __name__ == "__main__":
    main()
