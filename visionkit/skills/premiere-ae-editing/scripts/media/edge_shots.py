"""Pre-render stray-frame check: for every clip edge in a snapped EDL, find the exact camera cuts (frame level) within
0.4 s and flag edges that would leave 1-4 frames of another shot inside the clip.

    python edge_shots.py VIDEO EDL_SNAPPED.json [--fps 29.97002997]

Cheap: decodes only 0.8 s around each edge at 160x90. A cut = a frame whose mean difference to the previous frame is
over 4x the window median and over 12 (0-255 scale)."""
import json
import sys

import av
import numpy as np


def frames_around(path, t, fps, half=0.4):
    c = av.open(path)
    st = c.streams.video[0]
    st.thread_type = 'AUTO'
    c.seek(int(max(0.0, t - half - 1.0) / st.time_base), stream=st, backward=True)
    out = []
    for f in c.decode(st):
        ft = float(f.pts * st.time_base)
        if ft < t - half - 1e-3:
            continue
        if ft > t + half:
            break
        out.append((ft, f.to_ndarray(width=160, height=90, format='gray').astype(np.float32)))
    c.close()
    return out


def cuts_in(fr):
    if len(fr) < 3:
        return []
    d = [float(np.abs(fr[i][1] - fr[i - 1][1]).mean()) for i in range(1, len(fr))]
    med = float(np.median(d)) + 1e-6
    return [fr[i][0] for i in range(1, len(fr)) if d[i - 1] > max(12.0, 4 * med)]


def main():
    video, edl = sys.argv[1], sys.argv[2]
    fps = float(sys.argv[sys.argv.index('--fps') + 1]) if '--fps' in sys.argv else 30.0
    e = json.load(open(edl))
    bad = 0
    for part in ('hook', 'story'):
        for k, c in enumerate(e.get(part, [])):
            a, b = c[0], c[1]
            for side, t in (('in', a), ('out', b)):
                cuts = cuts_in(frames_around(video, t, fps))
                for ct in cuts:
                    if side == 'in' and t - 1e-3 <= ct < t + 4.5 / fps and ct - t > 0.5 / fps:
                        bad += 1
                        print(f'STRAY {part}{k} in {a:.3f}: camera cut {ct:.3f} = {round((ct - a) * fps)} frame(s) of the old shot at the start (move in to {ct:.3f})')
                    if side == 'out' and t - 4.5 / fps < ct <= t + 1e-3 and t - ct > 0.5 / fps:
                        bad += 1
                        print(f'STRAY {part}{k} out {b:.3f}: camera cut {ct:.3f} = {round((b - ct) * fps)} frame(s) of the next shot at the end (move out to {ct:.3f})')
    print(f'edge_shots: {bad} stray-frame edges')


if __name__ == '__main__':
    main()
