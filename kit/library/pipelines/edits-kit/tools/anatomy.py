"""Edit anatomy: measure the structure of a music edit in one pass.

usage: python anatomy.py VIDEO OUTDIR [--name NAME]
writes OUTDIR/NAME.json (everything measured), OUTDIR/NAME.txt (compact summary) and OUTDIR/NAME_strip.png
(timeline strip: one thumbnail per shot, loudness, cuts, flashes, hits, recurring motifs).

What it measures
- audio: tempo, kicks / snares / onsets (band spectral flux), loudness per frame, the drop (biggest 1 s rise),
  breaths (short dips), sections by loudness level
- picture: cuts (frame-difference spikes), flash frames (sudden brightness jumps, white or colour), black frames,
  B&W stretches, motion per frame (phase correlation), shots with length and motion
- motifs: shots whose picture comes back later in the edit (same footage or graphic, >= 1.5 s apart)
- sync: share of cuts and flashes within 1.5 frames of a hit, and whether they lead or lag
Needs: PyAV, numpy, Pillow, ffmpeg on PATH. Run with python -I.
"""
import sys, os, json, subprocess, tempfile, wave
import numpy as np
import av
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- audio
def load_audio(path, sr=22050):
    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", path, "-vn", "-ac", "1", "-ar", str(sr), tmp], check=True)
    w = wave.open(tmp, "rb"); x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768; w.close()
    os.unlink(tmp)
    return sr, x

def stft_mag(x, n_fft=2048, hop=256):
    win = np.hanning(n_fft); n = 1 + (len(x) - n_fft) // hop
    idx = np.arange(n_fft)[None, :] + hop * np.arange(n)[:, None]
    return np.abs(np.fft.rfft(x[idx] * win, axis=1))

def flux(S, f, lo, hi):
    band = (f >= lo) & (f < hi)
    L = np.log1p(100 * S[:, band]); d = np.diff(L, axis=0); d[d < 0] = 0
    e = np.concatenate([[0], d.sum(1)]); return e / (e.max() + 1e-9)

def peaks(e, hop, sr, k=1.6, w=6, gap=0.09, strong=None):
    """onset peaks; strong=q keeps only peaks whose height is in the top (1-q) of all peaks"""
    out = []; n = len(e)
    for i in range(1, n - 1):
        a, b = max(0, i - 20), min(n, i + 20)
        if e[i] > e[a:b].mean() + k * e[a:b].std() and e[i] == e[max(0, i - w):i + w + 1].max():
            t = i * hop / sr
            if not out or t - out[-1][0] > gap: out.append((round(t, 3), float(e[i])))
    if strong is not None and out:
        thr = np.quantile([v for _, v in out], strong); out = [(t, v) for t, v in out if v >= thr]
    return [t for t, _ in out]

def tempo(e, hop, sr):
    e = e - e.mean(); ac = np.correlate(e, e, "full")[len(e) - 1:]
    best = (120, -1e9)
    for bpm in np.arange(60, 200, 0.5):
        i = int(round(60 / bpm * sr / hop))
        if 2 * i < len(ac):
            v = ac[i] + 0.5 * ac[2 * i]
            if v > best[1]: best = (bpm, v)
    return float(best[0])

def audio_part(path, fps, nframes):
    sr, x = load_audio(path)
    hop = 256; S = stft_mag(x, 2048, hop); f = np.fft.rfftfreq(2048, 1 / sr)
    full, kick, snare = flux(S, f, 30, 11000), flux(S, f, 30, 150), flux(S, f, 1500, 6000)
    spf = sr / fps
    rms = np.array([np.sqrt((x[int(i * spf):int((i + 1) * spf)] ** 2).mean() + 1e-12) for i in range(nframes)])
    db = 20 * np.log10(rms + 1e-9)
    sm = np.convolve(db, np.ones(int(fps // 2)) / int(fps // 2), mode="same")
    # drop = biggest rise of the 1 s mean vs the previous 1 s
    w1 = int(fps); rise = np.full(len(sm), -99.0)
    for i in range(w1, len(sm) - w1): rise[i] = sm[i:i + w1].mean() - sm[i - w1:i].mean()
    di = int(np.argmax(rise)); drop = dict(t=round(di / fps, 2), rise_db=round(float(rise[di]), 1))
    # breaths: dips of 6+ dB below the local 2 s median lasting >= 0.15 s, inside the loud part
    med = np.array([np.median(sm[max(0, i - 2 * w1):i + 2 * w1]) for i in range(len(sm))])
    dip = (sm < med - 6) & (med > np.percentile(sm, 40))
    breaths, i = [], 0
    while i < len(dip):
        if dip[i]:
            j = i
            while j + 1 < len(dip) and dip[j + 1]: j += 1
            if (j - i + 1) / fps >= 0.15: breaths.append([round(i / fps, 2), round((j + 1) / fps, 2)])
            i = j + 1
        else: i += 1
    bpm = tempo(full, hop, sr); period = 60 / bpm; dur = len(x) / sr; best = (0, -1)
    for ph in np.arange(0, period, 0.005):
        ts = np.arange(ph, dur, period); idx = np.clip((ts * sr / hop).round().astype(int), 0, len(full) - 1)
        v = full[idx].sum()
        if v > best[1]: best = (ph, v)
    grid = [round(float(t), 3) for t in np.arange(best[0], dur, period)]
    return dict(bpm=bpm, grid=grid, kicks=peaks(kick, hop, sr, 1.8, strong=0.5), snares=peaks(snare, hop, sr, 1.8, strong=0.5),
                onsets=peaks(full, hop, sr), db=[round(float(v), 1) for v in sm], drop=drop, breaths=breaths)

# ---------------------------------------------------------------- picture
def picture_part(path):
    c = av.open(path); s = c.streams.video[0]; s.thread_type = "AUTO"
    fps = float(s.average_rate); W, H = s.codec_context.width, s.codec_context.height
    tw, th = (64, 36) if W >= H else (36, 64)
    sw, sh = (96, 54) if W >= H else (54, 96)
    small, strip = [], []
    for fr in c.decode(s):
        small.append(fr.reformat(width=tw, height=th, format="rgb24").to_ndarray())
        strip.append(fr.reformat(width=sw, height=sh, format="rgb24").to_ndarray())
    c.close()
    a = np.stack(small).astype(np.float32)
    y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    mx, mn = a.max(-1), a.min(-1)
    sat = np.where(mx > 1, (mx - mn) / np.maximum(mx, 1), 0).mean((1, 2))
    ym = y.mean((1, 2))
    d = np.zeros(len(y)); d[1:] = np.abs(y[1:] - y[:-1]).mean((1, 2))
    # colour-aware difference for cut detection
    dc = np.zeros(len(y)); dc[1:] = np.abs(a[1:] - a[:-1]).mean((1, 2, 3))
    win = np.outer(np.hanning(th), np.hanning(tw)); mot = np.zeros(len(y)); Fp = None
    for i in range(len(y)):
        F = np.fft.fft2((y[i] - y[i].mean()) * win)
        if Fp is not None:
            R = F * np.conj(Fp); R /= np.maximum(np.abs(R), 1e-6); cc = np.fft.ifft2(R).real
            py, px = np.unravel_index(np.argmax(cc), cc.shape)
            py = py - th if py > th // 2 else py; px = px - tw if px > tw // 2 else px
            mot[i] = np.hypot(px, py)
        Fp = F
    return fps, (W, H), a, y, ym, sat, d, dc, mot, strip

def med(a, i, r=4):
    return float(np.median(a[max(0, i - r):i + r + 1]))

def active_area(y):
    """crop letterbox / pillarbox: rows/cols that are near-black in at least half the frames. (95% was too strict: an
    edit that puts its title in the top bar for 13% of the time had the bar counted as picture, cuts went unseen.)"""
    rows = np.percentile(y.mean(2), 50, axis=0) < 14
    cols = np.percentile(y.mean(1), 50, axis=0) < 14
    r = np.where(~rows)[0]; c = np.where(~cols)[0]
    if len(r) < 4 or len(c) < 4: return slice(None), slice(None)
    return slice(r[0], r[-1] + 1), slice(c[0], c[-1] + 1)

def features(a, y, rs, cs):
    g = y[:, rs, cs]; n = len(g)
    std = g.reshape(n, -1).std(1)
    z = (g.reshape(n, -1) - g.reshape(n, -1).mean(1, keepdims=True)) / (std[:, None] + 1e-6)
    sub = a[:, rs, cs].reshape(n, -1, 3)
    hist = np.stack([np.histogramdd(sub[i], bins=(6, 6, 6), range=((0, 256),) * 3)[0].ravel() for i in range(n)])
    hist /= hist.sum(1, keepdims=True) + 1e-9
    return z, hist, std

def detect(fps, ym, sat, d, dc, a=None, y=None):
    n = len(ym)
    rs, cs = active_area(y)
    ym = y[:, rs, cs].mean((1, 2))          # brightness of the PICTURE (black bars would make every dark shot "black")
    z, hist, std = features(a, y, rs, cs)
    blank = std < 7
    def nb(i, step):
        k = i
        for _ in range(9):
            if 0 <= k < n and not blank[k]: return k
            k += step
        return None
    cuts = []
    for i in range(1, n):
        pa, pb = nb(i - 1, -1), nb(i, +1)
        if pa is None or pb is None or pb < i: continue
        if pb != i and not blank[i]: continue
        corr = float(np.dot(z[pa], z[pb]) / z.shape[1]); inter = float(np.minimum(hist[pa], hist[pb]).sum())
        if corr < 0.35 or (corr < 0.6 and inter < 0.55):
            t = i
            if cuts and t - cuts[-1] <= 2: continue
            cuts.append(t)
    flashes = []
    for i in range(1, n):
        up = ym[i] - ym[i - 1]
        if up > 30 or (ym[i] > 200 and ym[i - 1] < 170): flashes.append(i)
    fev, i = [], 0
    while i < len(flashes):
        j = i
        while j + 1 < len(flashes) and flashes[j + 1] - flashes[j] <= 2: j += 1
        fev.append(flashes[i]); i = j + 1
    blacks = [i for i in range(1, n) if ym[i] < 12 and ym[i - 1] >= 12]
    bw = []; low = sat < 0.07; i = 0
    while i < n:
        if low[i] and ym[i] > 15:
            j = i
            while j + 1 < n and low[j + 1]: j += 1
            if (j - i + 1) / fps >= 0.5: bw.append([round(i / fps, 2), round((j + 1) / fps, 2)])
            i = j + 1
        else: i += 1
    return cuts, fev, blacks, bw, (z, hist, blank)

def shots_from(cuts, n, fps, mot, a):
    b = [0] + [c for c in cuts] + [n]; out = []
    for k in range(len(b) - 1):
        s, e = b[k], b[k + 1]
        if e <= s: continue
        mid = (s + e) // 2
        out.append(dict(s=s, e=e, t=round(s / fps, 2), dur=round((e - s) / fps, 2), motion=round(float(mot[s + 1:e].mean()) if e - s > 1 else 0, 2), mid=mid))
    return out

def motifs(shots, feats, fps, min_gap=1.5):
    z, hist, blank = feats
    reps = []
    for sh in shots:
        idx = [k for k in range(sh["s"], sh["e"]) if not blank[k]]
        reps.append(idx[len(idx) // 2] if idx else None)
    n = len(shots); used = [False] * n; groups = []
    for i in range(n):
        if used[i] or reps[i] is None: continue
        grp = [i]
        for j in range(i + 1, n):
            if used[j] or reps[j] is None: continue
            if shots[j]["t"] - shots[grp[-1]]["t"] < min_gap: continue
            corr = float(np.dot(z[reps[i]], z[reps[j]]) / z.shape[1]); inter = float(np.minimum(hist[reps[i]], hist[reps[j]]).sum())
            if corr > 0.9 and inter > 0.75: grp.append(j)
        if len(grp) >= 2:
            for g in grp: used[g] = True
            groups.append(grp)
    return groups

def sync_stats(events_f, hits, fps):
    if not events_f or not hits: return None
    offs = []
    for f in events_f:
        t = f / fps; o = min(hits, key=lambda h: abs(h - t))
        offs.append((t - o) * fps)  # + = picture after the hit (late), - = early
    offs = np.array(offs); on = np.abs(offs) <= 1.5
    early = offs[on]
    # chance: share of all frames that sit within 1.5 frames of some hit (what random cuts would score)
    fr = np.arange(0, int(max(hits) * fps) + 2) / fps
    hh = np.array(hits); near = np.array([np.min(np.abs(hh - t)) * fps <= 1.5 for t in fr])
    return dict(n=len(offs), on_hit_pct=round(float(100 * on.mean()), 1), chance_pct=round(float(100 * near.mean()), 1),
                median_offset_frames=round(float(np.median(early)) if len(early) else 0, 2))

# ---------------------------------------------------------------- strip image
def draw_strip(path_png, name, fps, n, shots, strip, au, cuts, fev, groups, bw, W):
    dur = n / fps; Wd = 1600; x0 = 8; X = lambda t: x0 + (Wd - 2 * x0) * t / dur
    th = 54 if W >= 0 else 54
    Hh = 250; img = Image.new("RGB", (Wd, Hh), (22, 24, 30)); d = ImageDraw.Draw(img)
    try: font = ImageFont.truetype(("C:/Windows/Fonts/arialbd.ttf" if sys.platform == "win32" else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"), 11)
    except Exception: font = ImageFont.load_default()
    d.text((x0, 2), f"{name}  {dur:.1f}s  {len(shots)} shots  {au['bpm']:.0f} BPM  drop {au['drop']['t']}s (+{au['drop']['rise_db']} dB)", fill=(235, 235, 235), font=font)
    # thumbnails: one per shot at its start position (letterbox cropped), scaled to fit width
    st = np.stack(strip[::max(1, len(strip) // 200)]).astype(np.float32)
    sy = 0.2126 * st[..., 0] + 0.7152 * st[..., 1] + 0.0722 * st[..., 2]
    rs, cs = active_area(sy)
    for sh in shots:
        im = Image.fromarray(np.ascontiguousarray(strip[sh["mid"]][rs, cs])); w = max(2, int(X(sh["t"] + sh["dur"]) - X(sh["t"])))
        tw = min(w, int(im.width * 40 / im.height)); im = im.resize((max(1, tw), 40))
        img.paste(im, (int(X(sh["t"])), 18))
    # time-true filmstrip row
    step = max(0.5, dur * 44 / (Wd - 2 * x0)); t = 0.0
    while t < dur - 0.05:
        fi = min(len(strip) - 1, int(t * fps)); im = Image.fromarray(np.ascontiguousarray(strip[fi][rs, cs]))
        w = int(X(min(dur, t + step)) - X(t)) - 1; im = im.resize((max(1, min(w, int(im.width * 34 / im.height))), 34))
        img.paste(im, (int(X(t)), 62)); t += step
    # loudness
    db = np.array(au["db"]); lo, hi = -45, -3; top, bot = 100, 128
    pts = [(X(i / fps), bot - (bot - top) * min(1, max(0, (v - lo) / (hi - lo)))) for i, v in enumerate(db)]
    d.line(pts, fill=(80, 140, 255), width=1)
    # bw stretches
    for a, b in bw: d.rectangle([X(a), 130, X(b), 134], fill=(200, 200, 200))
    # cuts / flashes / kicks / snares
    for c in cuts: d.line([X(c / fps), 138, X(c / fps), 150], fill=(150, 150, 150))
    for f in fev: d.polygon([(X(f / fps), 154), (X(f / fps) + 4, 159), (X(f / fps), 164), (X(f / fps) - 4, 159)], fill=(250, 235, 170))
    for k in au["kicks"]: d.line([X(k), 168, X(k), 176], fill=(56, 198, 208), width=2)
    for s in au["snares"]: d.line([X(s), 178, X(s), 186], fill=(224, 107, 220), width=2)
    cols = [(255, 90, 80), (255, 190, 60), (120, 230, 120), (120, 180, 255), (230, 120, 255)]
    for gi, g in enumerate(groups[:5]):
        for k in g: d.rectangle([X(shots[k]["t"]), 192 + 6 * (gi % 5), X(shots[k]["t"] + max(shots[k]["dur"], 0.15)), 196 + 6 * (gi % 5)], fill=cols[gi])
    dd = au["drop"]["t"]; d.line([X(dd), 16, X(dd), 228], fill=(255, 80, 70), width=2)
    for b0, b1 in au["breaths"]: d.rectangle([X(b0), 97, X(b1), 99], fill=(255, 255, 255))
    for t in range(0, int(dur) + 1, 2): d.text((X(t) - 4, 234), f"{t}", fill=(150, 150, 150), font=font)
    img.save(path_png)

# ---------------------------------------------------------------- main
def main():
    path, out = sys.argv[1], sys.argv[2]
    name = sys.argv[sys.argv.index("--name") + 1] if "--name" in sys.argv else os.path.splitext(os.path.basename(path))[0][:40]
    os.makedirs(out, exist_ok=True)
    fps, (W, H), a, y, ym, sat, d, dc, mot, strip = picture_part(path)
    n = len(ym)
    au = audio_part(path, fps, n)
    cuts, fev, blacks, bw, feats = detect(fps, ym, sat, d, dc, a, y)
    shots = shots_from(cuts, n, fps, mot, a)
    groups = motifs(shots, feats, fps)
    hits = sorted(set(au["kicks"] + au["snares"]))
    half = sorted(set(au["grid"] + [round((g1 + g2) / 2, 3) for g1, g2 in zip(au["grid"], au["grid"][1:])]))
    dur = n / fps
    per2 = [round(sum(1 for c in cuts if k * fps <= c < (k + 2) * fps) / 2, 1) for k in range(0, int(np.ceil(dur)), 2)]
    flash2 = [sum(1 for f in fev if k * fps <= f < (k + 2) * fps) for k in range(0, int(np.ceil(dur)), 2)]
    mot2 = [round(float(mot[int(k * fps):int((k + 2) * fps)].mean()), 1) for k in range(0, int(np.ceil(dur)), 2)]
    res = dict(name=name, file=path, fps=fps, size=[W, H], frames=n, dur=round(dur, 2), audio=au,
               cuts=[round(c / fps, 3) for c in cuts], flashes=[round(f / fps, 3) for f in fev], blacks=[round(b / fps, 3) for b in blacks],
               bw=bw, shots=[{k: v for k, v in s.items() if k != "mid"} for s in shots],
               motifs=[[shots[k]["t"] for k in g] for g in groups], cuts_per_s_by2s=per2, flashes_by2s=flash2, motion_by2s=mot2,
               sync_cuts=sync_stats(cuts, hits, fps), sync_flashes=sync_stats(fev, hits, fps),
               grid_cuts=sync_stats(cuts, half, fps), grid_flashes=sync_stats(fev, half, fps))
    json.dump(res, open(os.path.join(out, name + ".json"), "w"), indent=0)
    durs = [s["dur"] for s in shots]
    lines = [f"{name}: {dur:.1f}s {W}x{H} {fps:.2f}fps | {au['bpm']:.0f} BPM | drop {au['drop']['t']}s (+{au['drop']['rise_db']} dB)",
             f"shots {len(shots)} | median {np.median(durs):.2f}s | min {min(durs):.2f}s | max {max(durs):.2f}s",
             f"cuts/s per 2s: {' '.join(str(v) for v in per2)}",
             f"flashes per 2s: {' '.join(str(v) for v in flash2)}  (total {len(fev)})",
             f"motion per 2s: {' '.join(str(v) for v in mot2)}",
             f"breaths: {au['breaths'][:8]}",
             f"B&W: {bw[:6]} | black frames at: {[round(b / fps, 2) for b in blacks][:10]}",
             f"motifs: {[[shots[k]['t'] for k in g] for g in groups][:6]}",
             f"on kick/snare: cuts {res['sync_cuts']} | flashes {res['sync_flashes']}",
             f"on 8th-note grid: cuts {res['grid_cuts']} | flashes {res['grid_flashes']}"]
    open(os.path.join(out, name + ".txt"), "w", encoding="utf-8").write("\n".join(lines) + "\n")
    draw_strip(os.path.join(out, name + "_strip.png"), name, fps, n, shots, strip, au, cuts, fev, groups, bw, W)
    print("\n".join(lines))

if __name__ == "__main__":
    main()
