from __future__ import annotations

import argparse

import librosa
import matplotlib.patches as ptc
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation as anm


def gettimetext(t):
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = round(t % 60, 2)
    return '{:0>2d}:{:0>2d}:{:0>5.2f}'.format(h, m, s)


def haliluya(ad_file, mod="c", savename="untitle", cut_time=10, update_frq=32, speed=1.0, zoom=2.0, raise_y=3.0):
    au, sr = librosa.load(ad_file)
    k = 40
    au = [au[i] for i in range(0, len(au), k)]
    sr = sr // k

    au = [i * raise_y for i in au]
    survey_border = cut_time / 2
    v_d_time_ms = 1000 / update_frq
    v_d_time_sc = 1 / update_frq

    mass = (cut_time * sr) * speed / zoom
    windata_bd = int(mass // 2)
    play_time_all = len(au) / sr / speed
    frames_ct = int(play_time_all * update_frq) + 2

    def get(a, b):
        _pad = []
        pad_ = []
        st, end = b[0], b[1]
        if st < 0:
            if end > 0:
                _pad = [None] * (-st)
                st = 0
            else:
                return [None] * (end - st)
        if end > len(a):
            pad_ = [None] * (end - len(a)) if st < len(a) else [None] * (2 * windata_bd)
            end = len(a)
        return _pad + a[st:end] + pad_

    fig, ax = plt.subplots(figsize=(6, 3))
    lim_border = survey_border / zoom
    ax.set_xlim(-lim_border, lim_border)
    ax.set_ylim(-2, 2)
    line, = ax.plot([], [], lw=0.5, color='blue')
    time_show = plt.text(0, 1.5, '', fontsize=12, color='g')
    sentry = ptc.Rectangle((-0.005, 1), 0.01, -2, edgecolor='#FF0010', facecolor="none", lw=0.5)
    ax.add_patch(sentry)
    plt.axis('off')

    def update(fct):
        if fct == frames_ct - 1:
            return line,
        t_video = fct * v_d_time_sc
        t_audio = t_video * speed
        time_show.set_text(gettimetext(t_audio))
        ax.set_xlim(t_audio - lim_border, t_audio + lim_border)
        c = int(t_audio * sr)
        data = get(au, [c - windata_bd, c + windata_bd])
        x = np.linspace(t_audio - lim_border, t_audio + lim_border, windata_bd * 2)
        line.set_data(x, data)
        sentry.set_x(t_audio)
        return line,

    ani = anm(fig, update, frames=frames_ct, interval=v_d_time_ms)
    if mod == "s":
        ani.save(f'{savename}_w.mp4', writer='ffmpeg')
    else:
        plt.show()


def main() -> None:
    parser = argparse.ArgumentParser(description="Render scrolling audio waveform animation.")
    parser.add_argument("--audio", required=True)
    parser.add_argument("--mode", default="c", choices=["c", "s"])
    parser.add_argument("--save_name", default="untitle")
    args = parser.parse_args()
    haliluya(args.audio, args.mode, args.save_name)


if __name__ == "__main__":
    main()
