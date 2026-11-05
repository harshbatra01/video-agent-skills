"""plankit: the shared toolkit for writing an edit plan (the pilot's plan_v8.py helpers, made reusable).

    from plankit import Edit
    e = Edit("03_yamal_yquefue", song_in=8.0, dur=29.7, catalog="<kit>/pilot/catalog", gallery="yamal")
    k = e.add("2_007", e.C(14.9), e.C(16.8), src=29.5)          # clip on the strongest hits, framed from its matte
    e.hit(e.C(14.9), punch=[1.1, 0.3]); e.tr("grid", e.C(14.9), pattern="fill", n=7)
    e.number("16", t0, t1, k, size=520)                          # big word behind him + white silhouette + caption
    e.title(["NOW", "OR", "NEVER"], [4.78, 4.94, 5.16], t1, pop=k)  # top-bar title, word per sung word, head pops out
    e.lyric_line(["I", "TOOK", "ONE", "SHOT"], [..times..], t1)  # bottom-bar lyric words on the sung syllables
    e.save()                                                     # writes plan.json + prints the cut-sync report
Times are EDIT seconds (song time minus song_in). C(t) = the strongest kick / snare near t, floored to a frame.
F(t) = floor to a frame (for lyric times). Song files come from EDIT_DIR/song (setup_edit.py makes them).
"""
import os, sys, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); KIT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import automatte, cuts, typeset

RED, GARNET, GREY, GOLD = [0.78, 0.06, 0.12], [0.50, 0.04, 0.16], [0.38, 0.38, 0.40], [1.0, 0.78, 0.15]
BAND = [560, 800]
CAP_Y = 1402


def ramp_rk(t0, t1, s_anchor, t_anchor, v_far=1.3, v_near=0.35, width=0.14, step=1 / 15):
    """velocity ramp: speed dips to v_near around t_anchor; source = s_anchor exactly on t_anchor"""
    v = lambda t: v_near + (v_far - v_near) * (1 - math.exp(-((t - t_anchor) / width) ** 2))
    ts = sorted(set([round(t0 + i * step, 4) for i in range(int((t1 - t0) / step) + 1)] + [round(t1, 4), round(t_anchor, 4)]))
    s_rel = [0.0]
    for x0, x1 in zip(ts, ts[1:]): s_rel.append(s_rel[-1] + (v(x0) + v(x1)) / 2 * (x1 - x0))
    off = s_anchor - s_rel[ts.index(round(t_anchor, 4))]
    return [[round(t, 4), round(sr + off, 4)] for t, sr in zip(ts, s_rel)]


def stutter_rk(t0, t1, s0, rep=4, times=2, speed=1.0, fps=30):
    """time remap that plays `rep` frames, jumps back and plays them again (`times` plays in all), then runs on:
    the stutter strike on a snare roll. Keys sit exactly on frame times (no frame blending on such clips)."""
    f = 1.0 / fps; keys = []
    for k in range(times):
        a = t0 + k * rep * f
        keys += [[round(a, 5), round(s0, 5)], [round(a + (rep - 1) * f, 5), round(s0 + (rep - 1) * f * speed, 5)]]
    a = t0 + times * rep * f
    keys += [[round(a, 5), round(s0 + rep * f * speed, 5)], [round(t1, 5), round(s0 + (rep * f + (t1 - a)) * speed, 5)]]
    return keys


_SIZE = {}
def src_size(path):
    if path not in _SIZE:
        import av
        c = av.open(path); st = c.streams.video[0]; _SIZE[path] = (st.codec_context.width, st.codec_context.height); c.close()
    return _SIZE[path]


def active_area(path, s0, s1, n=5, thr=14):
    """the real picture inside pillarbox / letterbox bars over source seconds s0..s1 (median of n frames).
    Returns [x0, y0, x1, y1] in source px, or None when the picture fills the frame."""
    import av
    c = av.open(path); st = c.streams.video[0]; W, H = st.codec_context.width, st.codec_context.height; frames = []
    for k in range(n):
        tq = s0 + (k + 0.5) / n * (s1 - s0)
        c.seek(int(max(0, tq - 0.6) / st.time_base), stream=st)
        for fr in c.decode(st):
            if float(fr.pts * st.time_base) >= tq - 0.02:
                frames.append(fr.reformat(width=W // 4, height=H // 4, format="gray").to_ndarray().astype(np.float32)); break
    c.close()
    if not frames: return None
    st_ = np.stack(frames)                       # a bar is black in EVERY frame and has no bright pixel at all
    peak = st_.max(axis=0)                       # (dark backgrounds are dark on average but have lights, faces, edges)
    h_, w_ = peak.shape                          # test columns on the middle rows only: captions and score bugs sit on
    r0, r1, c0, c1 = int(0.12 * h_), int(0.72 * h_), int(0.2 * w_), int(0.8 * w_)   # the bars near the corners
    col_bar = (peak[r0:r1].max(0) < 32) & (st_[:, r0:r1].mean(axis=(0, 1)) < 10)
    row_bar = (peak[:, c0:c1].max(1) < 32) & (st_[:, :, c0:c1].mean(axis=(0, 2)) < 10)
    cols = np.where(~col_bar)[0]; rows = np.where(~row_bar)[0]
    if len(cols) < 8 or len(rows) < 8: return None
    x0, x1, y0, y1 = cols[0] * 4, (cols[-1] + 1) * 4, rows[0] * 4, (rows[-1] + 1) * 4
    if (x1 - x0) > 0.97 * W and (y1 - y0) > 0.97 * H: return None
    pad = 6                                                     # stay clear of soft bar edges
    return [int(x0 + pad), int(y0 + pad), int(x1 - pad), int(y1 - pad)]


def fit_caption(text, size, tracking, font="ProximaNova-Semibold", max_w=960):
    """shrink tracking, then size, until a caption fits the frame width (a long caption at 380 tracking ran off
    both edges of a 1080-wide frame)"""
    while tracking > 120 and typeset.measure(text, font, size, tracking)[0] > max_w: tracking -= 20
    while size > 18 and typeset.measure(text, font, size, tracking)[0] > max_w: size -= 2
    return size, tracking


class Edit:
    def __init__(self, name, song_in, dur, catalog=None, gallery=None, edit_dir=None, fps=30, band=BAND, song_dir=None):
        self.dir = edit_dir or os.path.join(KIT, "edits", name)
        self.name, self.song_in, self.dur, self.fps, self.band = name, song_in, dur, fps, band
        sd = song_dir or os.path.join(self.dir, "song")
        self.song_wav = os.path.join(sd, "song.wav"); self.beats = os.path.join(sd, "beats.json")
        self.words_json = os.path.join(sd, "words.json")
        self.H = cuts.hits(self.beats, song_in, dur)
        cat_dir = catalog or os.path.join(self.dir, "catalog")
        cat = json.load(open(os.path.join(cat_dir, "catalog.json"), encoding="utf-8"))
        self.FILES = {f["id"]: f["path"] for f in cat["files"]}; self.SHOT = {s["id"]: s for s in cat["shots"]}
        self.gal = None
        if gallery:
            from reframe import build_gallery
            self.gal = build_gallery(os.path.join(cat_dir, "catalog.json"), gallery)
        self.mattes = os.path.join(self.dir, "mattes", "auto")
        self.clips, self.hits, self.words, self.looks, self.overlays, self.trans = [], [], [], [], [], []
        self.pops, self.sfx, self.outlines, self.colorpops, self.warn, self.MAT = [], [], [], [], [], {}
        self.look = dict(cc=dict(con=18, sat=92, temp=-4, hi=-12, sh=-6, blacks=-8), vig=28, grain=3)
        self.bloom = [86, 60, 0.16]

    # ---------------------------------------------------------------- time
    def C(self, t, win=0.2): return cuts.on(t, self.H, win, self.fps)
    def F(self, t): return round(cuts.fr(t, self.fps), 4)
    def S(self, song_t): return round(song_t - self.song_in, 4)          # song seconds -> edit seconds

    def strong(self, t0, t1, min_s=0.55):
        """strong hits (edit time, strength) between t0 and t1, for laying out a section"""
        return [(round(h, 3), round(s, 2)) for h, s in self.H if t0 <= h < t1 and s >= min_s]

    # ---------------------------------------------------------------- clips
    def add(self, shot, t0, t1, src=None, speed=1.0, zoom=None, rk=None, smooth=False, file=None, box=None, point=None,
            prompt_t=None, focus=None, matte=True, zmax=1.5, zmin=1.03, name=None, still=False, smooth_cam=None):
        sh = self.SHOT.get(shot); f = file or self.FILES[sh["file"]]
        if rk is None:
            s0 = src if src is not None else sh["t0"] + 0.1
            rk = [[t0, round(s0, 4)], [t1, round(s0 + (t1 - t0) * speed, 4)]]
        a, b = min(r[1] for r in rk), max(r[1] for r in rk)
        if sh and (a < sh["t0"] - 0.02 or b > sh["t1"] + 0.02):
            self.warn.append(f"{shot}: source {a:.2f}-{b:.2f} leaves the shot {sh['t0']:.2f}-{sh['t1']:.2f}")
        c = dict(file=f, t0=round(t0, 4), t1=round(t1, 4), name=name or f"{shot or os.path.basename(f)[:10]} {t0:.2f}", smooth=smooth, rk=rk)
        act = active_area(f, a, b)
        if act: c["active"] = act
        m = None
        if matte:
            m = automatte.ensure(f, a, b, self.mattes, box=box, point=point, gallery=None if (box or point) else self.gal,
                                 prompt_t=prompt_t, lo=sh["t0"] if sh else None, hi=sh["t1"] if sh else None)
            if m is None: self.warn.append(f"{shot}: no person found, no matte (centre framing)")
        if m is not None:
            c["matte"] = dict(file=m["file"], src0=m["src0"]); self.MAT[len(self.clips)] = m
            if focus is None:
                keys = automatte.matte_focus(m, t0, t1, rk, **(smooth_cam or dict(win=0.6, cap=0.35)))
                focus = [[t0, float(np.median([k[1] for k in keys])), float(np.median([k[2] for k in keys]))]] if still else keys
            if zoom is None: zoom = max(zmin, automatte.auto_zoom(m, zmax=zmax))
        c["focus"] = focus or [0.5, 0.5]; c["zoom"] = zoom if zoom is not None else zmin
        self.clips.append(c)
        return len(self.clips) - 1

    def keep_left_of(self, k, x_src):
        """reframe clip k so the window's right edge stays left of source column x_src (a score bug on the right)"""
        cl = self.clips[k]; z = cl["zoom"]; z = min(v for _, v in z) if isinstance(z, list) else z
        W, H = src_size(cl["file"]); ax0, ay0, ax1, ay1 = cl.get("active") or [0, 0, W, H]
        base = max(1080 / (ax1 - ax0), self.band[1] / (ay1 - ay0)); fx_max = x_src - 540 / (base * z)
        f = cl["focus"]
        if isinstance(f[0], list): cl["focus"] = [[t, min(x, fx_max), y] for t, x, y in f]
        else: cl["focus"] = [min(f[0], fx_max), f[1]]

    def keep_above(self, k, y_src, zoom=None):
        """reframe clip k so the picture window's bottom edge stays above source row y_src (crops burned-in captions,
        watermarks, score bugs along the bottom of compilation footage). Optionally sets a zoom first."""
        cl = self.clips[k]
        if zoom is not None: cl["zoom"] = zoom
        z = cl["zoom"]; z = min(v for _, v in z) if isinstance(z, list) else z
        W, H = src_size(cl["file"]); ax0, ay0, ax1, ay1 = cl.get("active") or [0, 0, W, H]
        base = max(1080 / (ax1 - ax0), self.band[1] / (ay1 - ay0)); fy_max = y_src - (self.band[1] / 2) / (base * z)
        f = cl["focus"]
        if isinstance(f[0], list): cl["focus"] = [[t, x, min(y, fy_max)] for t, x, y in f]
        else: cl["focus"] = [f[0], min(f[1], fy_max)]

    def side_x(self, k, t, glyph_w, margin=40):
        """x (comp px) for a glyph glyph_w wide BEHIND clip k's player so that most of it shows: on the side of the
        frame with more free room beside his body (a narrow "1" centred behind a centred player vanished completely)"""
        cl = self.clips[k]; m = self.MAT[k]
        rk = cl["rk"]; s_ = rk[0][1]
        for (a, sa), (b, sb) in zip(rk, rk[1:]):
            if a <= t <= b: s_ = sa + (sb - sa) * (t - a) / (b - a) if b > a else sb
        rows = [r for r in m["rows"] if r[1] > 0]; r = min(rows, key=lambda r: abs(r[0] - s_))
        cp = automatte.comp_point(m, cl, t, band=self.band)
        if cp is None: return 540
        # body edges in comp px: map the matte box through the same scale as the head point
        W_, H_ = m["w"], m["h"]; fw = 1080; z = cl.get("zoom", 1); z = z[0][1] if isinstance(z, list) else z
        sc = max(fw / W_, self.band[1] / H_) * z
        x0 = cp[0] + (r[4] - r[8]) * sc; x1 = cp[0] + (r[6] - r[8]) * sc
        left, right = max(0, x0), max(0, 1080 - x1)
        if left >= right: return round(max(glyph_w / 2 + margin, x0 - glyph_w * 0.35))
        return round(min(1080 - glyph_w / 2 - margin, x1 + glyph_w * 0.35))

    def subj_src(self, k, t):
        """head + shoulders of clip k's player in SOURCE px at edit time t"""
        rk = self.clips[k]["rk"]; s_ = rk[0][1]
        for (a, sa), (b, sb) in zip(rk, rk[1:]):
            if a <= t <= b: s_ = sa + (sb - sa) * (t - a) / (b - a) if b > a else sb
        rows = [r for r in self.MAT[k]["rows"] if r[1] > 0]
        r = min(rows, key=lambda r: abs(r[0] - s_))
        return round(r[8], 1), round(r[9] + 0.3 * (r[3] - r[9]), 1)

    # ---------------------------------------------------------------- events
    def hit(self, t, **kw): self.hits.append(dict(t=round(t, 4), **kw))
    def tr(self, ty, t, **kw): self.trans.append(dict(type=ty, t=round(t, 4), **kw))
    def overlay(self, palette, kind, t0, **kw): self.overlays.append(dict(file=os.path.join(KIT, "assets", "overlays", palette, kind + ".mp4"), t0=t0, **kw))
    def sfx_at(self, kind, t, db=-18): self.sfx.append(dict(file=os.path.join(KIT, "assets", "sfx", kind + ".wav"), t=round(t, 3), db=db))

    # ---------------------------------------------------------------- type
    def number(self, text, t0, t1, k, size, depth_color=GARNET, cap=None, cap2=None, lift=0.0, font="GalanoGrotesque-Black", sil=True):
        """the motif he loved: a big word / number behind the player (glyph centre near the top of his head), a 1-frame
        white silhouette on the slam, a small caption in the bottom bar"""
        w, gh = typeset.measure(text, font, size)
        cp = automatte.comp_point(self.MAT[k], self.clips[k], t0 + 0.15, band=self.band) if k in self.MAT else None
        x, top = (cp[0], cp[2]) if cp else (540.0, self.band[0] + 0.3 * self.band[1])
        cy = min(max(top + 0.05 * gh - lift * gh, self.band[0] + gh / 2 + 12), self.band[0] + self.band[1] - gh / 2 - 12)
        x = 540.0 if w > 1000 else min(max(x, w / 2 + 30), 1080 - w / 2 - 30)
        self.words.append(dict(text=text, t0=t0, t1=t1, style="hero", size=size, x=round(x), y=round(cy + gh / 2), behind=k,
                               font=font, depth_color=depth_color, **{"from": 128}))
        if sil: self.hit(t0, sil=dict(clip=k, frames=[0], glow=45), expo=[0.5, 0.18])
        if cap: self.caption(cap, t0 + 0.1, t1, y=CAP_Y, size=34)
        if cap2: self.caption(cap2, t0 + 0.16, t1, y=CAP_Y + 48, size=26, tracking=300)

    def title(self, words, times, t1, pop=None, font="Coolvetica-HeavyComp", depth=RED, max_w=990, y=540):
        """title in the top bar, word by word on the sung times; the player of clip `pop` breaks out over it"""
        ts = typeset.fit(" ".join(words), font, max_w); xs, _ = typeset.line(words, font, ts, gap=0.22)
        for w_, lt, x_ in zip(words, times, xs):
            self.words.append(dict(text=w_, t0=self.F(lt), t1=t1, size=ts, y=y, x=x_, style="hero", layer="bar", font=font, depth_color=depth, **{"from": 135}))
        if pop is not None: self.pops.append(dict(clip=pop, t0=self.clips[pop]["t0"], t1=min(t1, self.clips[pop]["t1"])))
        return ts

    def lyric_line(self, words, times, t1, size=96, y=1446, font="Coolvetica-HeavyComp"):
        xs, _ = typeset.line(words, font, size, gap=0.28)
        for w_, x_, lt in zip(words, xs, times):
            self.words.append(dict(text=w_, t0=self.F(lt), t1=t1, x=x_, y=y, style="slam", font=font, size=size, shade=0.6, **{"from": 140}))

    def strike_name(self, text, t0, t1, t_strike=None, y=CAP_Y + 8, size=46):
        self.words.append(dict(text=text, t0=round(t0, 4), t1=round(t1, 4), style="strike", y=y, size=size,
                               t_strike=round(t_strike, 4) if t_strike is not None else None))

    def caption(self, text, t0, t1, y=CAP_Y, size=34, tracking=380):
        size, tracking = fit_caption(text, size, tracking)
        self.words.append(dict(text=text, t0=t0, t1=t1, style="cap", y=y, size=size, tracking=tracking))

    # ---------------------------------------------------------------- output
    def save(self, version, fade=0.6, extra=None):
        for z in self.trans:      # one sound family: whoosh on light / blur / panel transitions, glitch on strobes
            if z["type"] in ("blowout", "zoomrush", "smear", "defocus", "grid"): self.sfx_at("whoosh_short", z["t"] - 0.15, -20)
            if z["type"] in ("recipe", "silstack", "typeflash"): self.sfx_at("glitch", z["t"] - 0.03, -25)
        plan = dict(name=f"{self.name}_v{version}", w=1080, h=1920, fps=self.fps, dur=self.dur, band=self.band,
                    audio=dict(file=self.song_wav, **{"in": self.song_in}),
                    clips=self.clips, hits=self.hits, words=self.words, overlays=self.overlays, transitions=self.trans,
                    popouts=self.pops, sfx=self.sfx, outlines=self.outlines, colorpops=self.colorpops,
                    look=self.look, looks=self.looks, bloom=self.bloom, fade=[round(self.dur - fade, 3), self.dur] if fade else None)
        if extra: plan.update(extra)
        out = os.path.join(self.dir, f"plan_v{version}.json")
        json.dump(plan, open(out, "w"), indent=1)
        print(f"{plan['name']}: {len(self.clips)} clips, {len(self.hits)} hits, {len(self.words)} words, {len(self.trans)} transitions, {self.dur} s")
        for w_ in self.warn: print("WARN", w_)
        cuts.report(plan, self.H, self.fps)
        return out
