"""Edit plan (JSON) -> one layered After Effects project + rendered preview.

usage: python build_edit.py PLAN.json [--only-test SECONDS] [--range A-B] [--final]
  --range renders only A..B seconds of the full edit (the comp's work area): check one moment for a fraction of the time
  writes  <plan dir>/ae/<name>.jsx  (+ .aep saved after the build, every layer live)
  renders <plan dir>/renders/<name>.mp4 (H.264 with audio) or ProRes 422 .mov with --final
then run:  python ~/.claude/skills/premiere-ae-editing/scripts/ae/ae_run.py <jsx>   (Windows; Mac: see premiere-ae-editing mac-notes.md)

Plan keys (times are EDIT seconds):
  name, w, h, fps, dur, audio {file, in}
  clips    [{file, t0, t1, src | rk [[t, src t]...], speed, focus [x,y] | [[t,x,y]...], zoom 1 | [[t,z]...], smooth, name,
             matte {file, src0}, fit true (whole frame over a blurred copy: end cards)}]
  look     {cc {sat, con, temp, tint, exp, hi, sh, whites, blacks}, vig, grain}
  overlays [{file, t0, scale, opacity, mode "screen"|"add"}]
  battery  [{t0, t1, from, to, label, accent [r,g,b], dim 0-100 (over footage; omit = black card), levels [[t, v], ...]}]
  words    [{text, t0, t1, style hero|cap|slam, font, size, color, x, y, tracking, from, shade 0-1, depth_color, depth,
             behind CLIP | layer "bar", sub {text, size, y, font, color}}]
           y = the BASELINE (capitals rise about 0.72 x size above it), x = the centre
  hits     [{t, punch [amt, dur], shake [amp, dur, freq, rot], flash [dur, peak, color, mode, lead], expo [stops, dur],
             sil {clip, frames, glow}}]
  band     [y0, h]                          letterbox: the picture in a band (GASS x Mbappe: [560, 800]), bars above / below
  popouts  [{clip, t0, t1}]                 that clip's player cut out ABOVE the bars (breaks out of the band)
  zoomcuts [{t, amt}]                       rush-in zoom + radial blur across the cut at t (replaces whips)
  fade     [t0, t1]                         picture and music fade out at the end
  whips    [{t, dir 1|-1, dur, dist}]       (old) slide transition: rejected by the user on 13 Oct (mirror tiles show)
  bloom    [threshold, radius, intensity]   soft glow on the highlights of the picture (e.g. [72, 70, 0.3])
  transitions [{type, t, ...}]              invert {pattern "IN.N"} | cflash {a, b, dur, peak} | glitch {before, after, amt}
                                            | spin {deg} | shutter {close, open} | rgb {clipA, clipB, frames, px}
                                            | pop {clip, sx, sy, dur} | posterize {t0, t1, fps}
                                            optical (fx_lib.jsx, per-frame keyed): recipe {pattern "EKEKSDSDCC", line}
                                            | blowout {warm, leak} | zoomrush {amt, center, blur, chroma CLIP} | smear
                                            {vertical, tint, len} | paint {color, hold} | vortex {spin} | flood {cols, each,
                                            research pass 2: typeflash {word, pattern "WB", size} | freezeclone {clip, times,
                                            t_end} | ghost {clip, t0, t1, n, dt} | popfreeze {clip, sx, sy, frames} | print
                                            {clip, frames, label}; recipe chars T / V = impact frames; silstack P = poster
                                            op, drain} | rays {x, y, peak} | defocus {cast, radius}
  auras    [{clip, t0, t1, color, grow, soft, energy}]   energy glow behind the player (cutout re-laid above it)
  reticles [{t, t1, x, y, color, r}]        lock-on ring that lands on (x, y) in COMP pixels at t
  breaths  [[t0, t1]]
"""
import sys, os, json, math
sys.path.insert(0, os.path.join((os.environ.get('PAE_SCRIPTS') or os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts')), 'ae'))
from ae_build import write_jsx

HERE = os.path.dirname(os.path.abspath(__file__))
LIB = os.path.join(HERE, "ae", "edits_lib.jsx")
FXLIB = os.path.join(HERE, "ae", "fx_lib.jsx")        # optical transitions + hero effects (14 Oct study)
J = json.dumps
MODES = {"screen": "BlendingMode.SCREEN", "add": "BlendingMode.ADD", "normal": "BlendingMode.NORMAL", "overlay": "BlendingMode.OVERLAY",
         "lighten": "BlendingMode.LIGHTEN", "color_dodge": "BlendingMode.COLOR_DODGE"}

def P(path): return os.path.abspath(path).replace("\\", "/")

def rk_of(c):
    if "rk" in c: return c["rk"]
    sp = c.get("speed", 1.0); s0 = c.get("src", 0.0)
    return [[c["t0"], s0], [c["t1"], s0 + (c["t1"] - c["t0"]) * sp]]

def snap_plan(plan):
    """put every event exactly on its frame, a hair before it. Plans store times like 20.1667 (4 decimals), which is
    AFTER the real frame time 20.16666...: a layer starting there showed up one frame late (13 Oct: about a third of all
    cuts and hits were 1 frame late until this). Rule: frame time minus 0.1 ms for every in / out point and hit."""
    fps = plan["fps"]
    sn = lambda t: (math.floor(t * fps + 0.5) / fps - 1e-4) if t > 0.001 else t
    for c in plan.get("clips", []): c["t0"], c["t1"] = sn(c["t0"]), sn(c["t1"])
    for key in ("words", "popouts", "looks", "battery"):
        for w in plan.get(key, []): w["t0"], w["t1"] = sn(w["t0"]), sn(w["t1"])
    for key in ("hits", "zoomcuts", "whips", "reticles", "transitions"):
        for h in plan.get(key, []):
            if "t" in h: h["t"] = sn(h["t"])
            if "t0" in h: h["t0"], h["t1"] = sn(h["t0"]), sn(h["t1"])
            if "t_end" in h: h["t_end"] = sn(h["t_end"])
            if "times" in h: h["times"] = [sn(x) for x in h["times"]]
    for w in plan.get("words", []):
        if w.get("t_strike") is not None: w["t_strike"] = sn(w["t_strike"])
    for o in plan.get("overlays", []): o["t0"] = sn(o["t0"])
    plan["breaths"] = [[sn(a), sn(b)] for a, b in plan.get("breaths", [])]
    return plan

_MDUR = {}
def rk_matte(rk, m):
    """a clip's remap keys shifted onto its matte file, CLAMPED to the matte's own length (a pre-rolled clip, e.g. for
    an iris transition, asked the matte for negative time and AE refused the build)"""
    f = m["file"]
    if f not in _MDUR:
        try:
            j = json.load(open(f[:-4] + ".json")); _MDUR[f] = max(0.0, len(j["rows"]) / j["fps"] - 1.0 / j["fps"])
        except Exception:
            _MDUR[f] = None
    hi = _MDUR[f]
    return [[t, round(min(max(0.0, s - m["src0"]), hi if hi is not None else 1e9), 5)] for t, s in rk]

def grid_seq(pattern, n):
    """flash-grid patterns -> (frame offset of the first frame relative to the cut, per-frame panel strings, fade).
    Frame 0 (the cut, on the beat) is the fullest frame."""
    full = "1" * n
    if pattern == "fill":            # one panel per frame, left to right / top to bottom, then fade into the next clip
        return -(n - 1), ["1" * (i + 1) + "0" * (n - i - 1) for i in range(n)], 4
    if pattern == "fill_rev":
        return -(n - 1), ["0" * (n - i - 1) + "1" * (i + 1) for i in range(n)], 4
    if pattern == "fill2":           # two panels per frame
        k = (n + 1) // 2; return -(k - 1), ["1" * min(n, 2 * (i + 1)) + "0" * max(0, n - 2 * (i + 1)) for i in range(k)], 4
    if pattern == "centre":          # from the middle outwards
        k = (n + 1) // 2
        seqs = ["".join("1" if (n - 1) // 2 - i <= b <= n // 2 + i else "0" for b in range(n)) for i in range(k)]
        return -(k - 1), seqs, 4
    if pattern == "alt":             # odd panels, even panels, all, then fade
        return -2, ["".join("1" if b % 2 == 0 else "0" for b in range(n)), "".join("1" if b % 2 else "0" for b in range(n)), full], 4
    if pattern == "pass":            # a lit block passes over the cut: GASS x Mbappe halves = "pass" with n=2 rows
        return -(n - 1), ["1" * (i + 1) + "0" * (n - i - 1) for i in range(n)] + ["0" * (i + 1) + "1" * (n - i - 1) for i in range(n - 1)], 0
    if pattern == "unfill":          # full on the cut, then panels switch off one by one to reveal the next clip
        return 0, ["0" * i + "1" * (n - i) for i in range(n)], 0
    raise ValueError("unknown grid pattern " + pattern)

def prep_geo(plan):
    """slices: the in-coming clip starts `pre` frames early (seen between the flying strips), the out-going original
    ends there (its strips take over). iris: the in-coming clip's remap starts early (its copy plays inside the growing
    silhouette) but the clip itself still starts on the cut."""
    fps = plan["fps"]; clips = plan["clips"]
    for tr in plan.get("transitions", []):
        if tr["type"] not in ("slices", "iris"): continue
        kb = tr["clipB"]; cb = clips[kb]; pre = tr.get("pre", 4 if tr["type"] == "slices" else 5) / fps
        rk = cb["rk"]; sp = (rk[1][1] - rk[0][1]) / (rk[1][0] - rk[0][0]) if rk[1][0] > rk[0][0] else 1.0
        if rk[0][0] > tr["t"] - pre - 1e-4:
            cb["rk"] = [[round(tr["t"] - pre, 5), round(rk[0][1] - (rk[0][0] - (tr["t"] - pre)) * sp, 5)]] + rk
        if tr["type"] == "slices": cb["t0"] = round(tr["t"] - pre, 5)
    return plan

def spec(plan, test=None, rng=None):
    plan = prep_geo(plan)
    def act(cl, code):       # clips from pillarboxed / letterboxed sources: frame inside the real picture only
        return f'ACTIVE = {J(cl["active"])}; {code} ACTIVE = null;' if cl.get("active") else code
    dur = test or plan["dur"]
    L = []
    L.append(f'var c = newComp({J(plan["name"])}, {dur}); c.motionBlur = true; c.shutterAngle = 180; c.shutterPhase = -90;')
    if rng: L.append(f'c.workAreaStart = {rng[0]}; c.workAreaDuration = {round(rng[1] - rng[0], 4)};')
    band = plan.get("band")
    L.append('BAND = ' + (J(dict(y0=band[0], h=band[1])) if band else 'null') + ';')
    a = plan.get("audio")
    if a:
        L.append(f'var au = c.layers.add(imp({J(P(a["file"]))})); au.startTime = {-a["in"]}; au.inPoint = 0; au.outPoint = {dur};')
        fd = plan.get("fade")
        if fd:
            L.append('try { var lv = au.property("ADBE Audio Group").property("ADBE Audio Levels"); '
                     f'lv.setValueAtTime({fd[0]}, [0, 0]); lv.setValueAtTime({fd[1]}, [-48, -48]); ' + '} catch (e) { log("  audio fade " + e.toString()); }')
    for fx_ in plan.get("sfx", []):
        if fx_["t"] < dur: L.append(f'sfxL(c, {J(P(fx_["file"]))}, {fx_["t"]}, {fx_.get("db", -14)});')
    clips = plan.get("clips", [])
    def args(cl):
        t1 = min(cl["t1"], dur); foc = cl.get("focus")
        return t1, rk_of(cl), (J(foc) if foc else "null"), J(cl.get("zoom", 1))
    # 1. footage (inside the band when there is one)
    for k, cl in enumerate(clips):
        if cl["t0"] >= dur: continue
        t1, rk, foc, zm = args(cl)
        if cl.get("fit"):          # whole 16:9 frame over a blurred copy (end card)
            L.append(f'var L{k} = fitClip(c, {J(P(cl["file"]))}, {cl["t0"]}, {t1}, {J(rk)}, {J(cl.get("name", "clip %02d" % k))});')
        else:
            L.append(act(cl, f'var L{k} = clip(c, {J(P(cl["file"]))}, {cl["t0"]}, {t1}, {J(rk)}, {foc}, {zm}, {J(cl.get("name", "clip %02d" % k))});'))
        if cl.get("smooth"): L.append(f'smooth(L{k});')
        if cl.get("mblur", True): L.append(f'L{k}.motionBlur = true;')
    made = set()
    def matte(k):
        if k in made: return
        cl = clips[k]; t1, rk, foc, zm = args(cl); m = cl["matte"]
        rkm = rk_matte(rk, m)
        L.append(act(cl, f'var M{k} = matteFor(c, {J(P(m["file"]))}, {cl["t0"]}, {t1}, {J(rkm)}, {foc}, {zm});')); made.add(k)
    # 2. overlays (light leaks, bars, burns) over the picture
    for o in plan.get("overlays", []):
        if o["t0"] < dur:
            L.append(f'overlay(c, {J(P(o["file"]))}, {o["t0"]}, {o.get("scale", "null")}, {o.get("opacity", "null")}, {MODES.get(o.get("mode", "screen"))});')
    for b in plan.get("battery", []):
        if b["t0"] < dur:
            L.append(f'battery(c, {b["t0"]}, {min(b["t1"], dur)}, {b["from"]}, {b["to"]}, {J(b.get("label", ""))}, {J(b.get("accent"))}, '
                     f'{J(b["dim"]) if "dim" in b else "undefined"}, {J(b.get("levels", []))});')
    # type: style "hero" (big, textured, depth copy), "cap" (small, tracked), default "slam"; layer "behind" / "bar" / front
    def word(w):
        t1 = min(w["t1"], dur); x = w.get("x", plan["w"] / 2); y = w.get("y", plan["h"] * 0.5); st = w.get("style", "slam")
        if st == "strike":
            ts_ = w.get("t_strike")
            L.append(f'strikeWord(c, {J(w["text"])}, {w["t0"]}, {t1}, {J(ts_) if ts_ is not None else "null"}, {x}, {y}, {w.get("size", 46)}, '
                     f'{J(w.get("font", "ProximaNova-Extrabld"))}, {J(w.get("color", [1, 1, 1]))}, {J(w.get("line"))});')
        elif st == "outline":
            L.append(f'outlineText(c, {J(w["text"])}, {w["t0"]}, {t1}, {x}, {y}, {w.get("size", 500)}, {J(w.get("font", "GalanoGrotesque-Black"))}, '
                     f'{J(w.get("color", [1, 1, 1]))}, {w.get("stroke", 6)}, {w.get("from", 125)});')
        elif st == "hero":
            L.append(f'heroText(c, {J(w["text"])}, {w["t0"]}, {t1}, {x}, {y}, {w.get("size", 300)}, {J(w.get("font", "GalanoGrotesque-Black"))}, '
                     f'{J(w.get("color", [1, 1, 1]))}, {J(w.get("depth_color"))}, {J(w.get("depth"))}, {w.get("tracking", 0)}, {w.get("from", 125)});')
        elif st == "cap":
            L.append(f'caption(c, {J(w["text"])}, {w["t0"]}, {t1}, {x}, {y}, {w.get("size", 36)}, {J(w.get("font", "ProximaNova-Semibold"))}, '
                     f'{w.get("tracking", 380)}, {J(w.get("color", [1, 1, 1]))});')
        else:
            L.append(f'slamWord(c, {J(w["text"])}, {w["t0"]}, {t1}, {J(w.get("font", "GalanoGrotesque-Black"))}, {w.get("size", 190)}, '
                     f'{J(w.get("color", [1, 1, 1]))}, {x}, {y}, {w.get("tracking", 0)}, {w.get("from", 135)}, {w.get("shade", 0)});')
        sb = w.get("sub")
        if sb:
            L.append(f'subLine(c, {J(sb["text"])}, {w["t0"] + 0.06}, {t1}, {J(sb.get("font", "ProximaNova-Extrabld"))}, {sb.get("size", 40)}, '
                     f'{J(sb.get("color", [1, 1, 1]))}, {x}, {sb.get("y", plan["h"] * 0.56)}, {sb.get("tracking", 380)});')
    for w in plan.get("words", []):   # platform UI covers the bottom ~20% and the right edge on TikTok / Reels / Shorts
        y = w.get("y", plan["h"] * 0.5); sy = (w.get("sub") or {}).get("y", y); top = y - 0.72 * w.get("size", 190)
        if max(y, sy) > plan["h"] * 0.76 or top < plan["h"] * 0.1:
            print(f"SAFE ZONE: {w['text']!r} spans y={top:.0f}-{max(y, sy):.0f}, outside 10-76% of the height")
    behind, inbar, front = {}, [], []
    for w in plan.get("words", []):
        if w["t0"] >= dur: continue
        if "behind" in w and clips[w["behind"]].get("matte"): behind.setdefault(w["behind"], []).append(w)
        elif w.get("layer") == "bar": inbar.append(w)
        else: front.append(w)
    # 3. type behind the player: word, then (outline), then the player cut out above it
    outl = {o["clip"]: o for o in plan.get("outlines", []) if o["clip"] < len(clips) and clips[o["clip"]].get("matte")}
    for k in sorted(set(behind) | set(outl)):
        for w in behind.get(k, []): word(w)
        matte(k); cl = clips[k]; t1, rk, foc, zm = args(cl)
        if k in outl:
            o = outl[k]; m = cl["matte"]; rkm = rk_matte(rk, m)
            L.append(act(cl, f'outlineL(c, {J(P(m["file"]))}, {cl["t0"]}, {t1}, {J(rkm)}, {foc}, {zm}, {J(o.get("color", [1, 0.85, 0.2]))}, {o.get("grow", 8)}, {o.get("glow", 50)});'))
        L.append(act(cl, f'cutoutL(c, {J(P(cl["file"]))}, {cl["t0"]}, {t1}, {J(rk)}, {foc}, {zm}, M{k});'))
    # 3b. auras: energy glow behind the player, the player cut out again above it
    for au in plan.get("auras", []):
        k = au["clip"]; cl = clips[k]
        if au["t0"] >= dur or not cl.get("matte"): continue
        matte(k); t1, rk, foc, zm = args(cl); m = cl["matte"]; rkm = rk_matte(rk, m)
        a0, a1 = au["t0"], min(au["t1"], dur)
        L.append(act(cl, f'aura(c, {J(P(m["file"]))}, {a0}, {a1}, {J(rkm)}, {foc}, {zm}, {J(au.get("color", [0.62, 0.2, 1]))}, {au.get("grow", 14)}, {au.get("soft", 22)}, {J(au.get("energy", True))});'))
        L.append(act(cl, f'var AU{k} = cutoutL(c, {J(P(cl["file"]))}, {a0}, {a1}, {J(rk)}, {foc}, {zm}, M{k}); AU{k}.name = "aura cutout {k}";'))
    # 4. silhouette strobes
    for h in plan.get("hits", []):
        sl = h.get("sil")
        if sl and h["t"] < dur and clips[sl["clip"]].get("matte"):
            matte(sl["clip"]); times = [round(h["t"] + f / plan["fps"], 4) for f in sl.get("frames", [0, 2])]
            L.append(f'silStrobe(c, M{sl["clip"]}, {J(times)}, {J(sl.get("color"))}, {sl.get("glow", 40)});')
    # 5. section looks (B&W ...), then colour pops above them
    for sp in plan.get("looks", []):
        if sp["t0"] < dur:
            L.append(f'lumetri(adjSpan(c, "look span", {sp["t0"]}, {min(sp["t1"], dur)}), {J(sp.get("cc", {}))});')
    for cp in plan.get("colorpops", []):
        k = cp["clip"]; cl = clips[k]
        if cl["t0"] >= dur or not cl.get("matte"): continue
        matte(k); t1, rk, foc, zm = args(cl)
        L.append(f'colorPop(c, {cl["t0"]}, {t1});')
        L.append(act(cl, f'cutoutL(c, {J(P(cl["file"]))}, {cl["t0"]}, {t1}, {J(rk)}, {foc}, {zm}, M{k});'))
    # 5b. the grade and vignette sit BELOW the transitions: a white frame must stay flat white, a colour flood flat
    look_ = plan.get("look")
    if look_: L.append(f'look(c, {J(look_.get("cc", {}))}, {look_.get("vig", 0)}, 0);')
    # 6. hits move the picture (below the bars, so the letterbox stays still)
    for h in plan.get("hits", []):
        t = h["t"]
        if t >= dur: continue
        if "expo" in h: L.append(f'expoPop(c, {t}, {h["expo"][0]}, {h["expo"][1]});')
        if "punch" in h: L.append(f'punch(c, {t}, {h["punch"][0]}, {h["punch"][1]});')
        if "shake" in h:
            sh = h["shake"] + [None] * (4 - len(h["shake"]))
            L.append(f'shake(c, {t}, {sh[0]}, {sh[1]}, {sh[2] or 14}, {sh[3] or 2});')
    for z in plan.get("zoomcuts", []):
        if z["t"] < dur: L.append(f'zoomCut(c, {z["t"]}, {z.get("amt", 1.2)});')
    for wp in plan.get("whips", []):
        if wp["t"] < dur: L.append(f'whip(c, {wp["t"]}, {wp.get("dir", 1)}, {wp.get("dur", 0.12)}, {wp.get("dist", 0.55)});')
    f1 = 1 / plan["fps"]
    bl = plan.get("bloom")
    if bl: L.append(f'glowSpan(c, 0, {dur}, {bl[0]}, {bl[1]}, {bl[2]});')
    # posterize first: it holds frames, so anything above it (flickers, flashes) must not be under it
    order = sorted(plan.get("transitions", []), key=lambda tr: 0 if tr["type"] == "posterize" else 1)
    for tr in order:                                 # the transition library (edits_lib.jsx "transitions v2")
        ty = tr["type"]; t = tr.get("t", tr.get("t0", 0))
        if t >= dur: continue
        if ty == "invert": L.append(f'invertFlicker(c, {t}, {J(tr.get("pattern", "I"))});')
        elif ty == "cflash": L.append(f'colorFlash(c, {t}, {J(tr.get("a"))}, {J(tr.get("b"))}, {tr.get("dur", 0.16)}, {tr.get("peak", 90)});')
        elif ty == "glitch": L.append(f'glitchCut(c, {t}, {tr.get("before", 2)}, {tr.get("after", 2)}, {tr.get("amt", 1)});')
        elif ty == "spin": L.append(f'spinCut(c, {t}, {tr.get("deg", 18)}, {tr.get("before", 3)}, {tr.get("after", 4)});')
        elif ty == "shutter": L.append(f'shutterCut(c, {t}, {tr.get("close", 3)}, {tr.get("open", 4)});')
        elif ty == "posterize": L.append(f'posterizeSpan(c, {tr["t0"]}, {min(tr["t1"], dur)}, {tr.get("fps", 12)});')
        # ---- fx_lib (optical, round 3: per-frame keyed) ----
        elif ty == "recipe": L.append(f'frameRecipe(c, {t}, {J(tr.get("pattern", "W"))}, {J(tr.get("line"))});')
        elif ty == "blowout":
            lk = tr.get("leak")
            L.append(f'lightBlowout(c, {t}, {J(tr.get("warm"))}, {J(P(lk)) if lk else "null"});')
        elif ty == "zoomrush":
            L.append(f'zoomRush(c, {t}, {tr.get("pre", 3)}, {tr.get("post", 7)}, {tr.get("amt", 1.5)}, {J(tr.get("center"))}, {tr.get("blur", 95)});')
            if tr.get("chroma") is not None:
                L.append(f'radialSplit(c, L{tr["chroma"]}, {t}, {round(t + tr.get("chroma_frames", 5) * f1, 5)}, {tr.get("chroma_amt", 0.06)});')
        elif ty == "smear": L.append(f'smear(c, {t}, {J(tr.get("vertical", True))}, {J(tr.get("tint"))}, {tr.get("len", 320)});')
        elif ty == "paint": L.append(f'lightPaint(c, {t}, {J(tr.get("color"))}, {tr.get("hold", 10)});')
        elif ty == "vortex": L.append(f'vortex(c, {t}, {tr.get("spin", 28)});')
        elif ty == "flood": L.append(f'colorFlood(c, {t}, {J(tr.get("cols") or [tr.get("color", [0.85, 0.05, 0.1])])}, {tr.get("each", 4)}, {tr.get("op", 92)}, {tr.get("drain", 3)}, {J(tr.get("steps"))});')
        elif ty == "rays": L.append(f'lightBurst(c, {t}, {tr.get("x", plan["w"] / 2)}, {tr.get("y", plan["h"] / 2)}, {tr.get("peak", 520)});')
        elif ty == "defocus": L.append(f'defocus(c, {t}, {J(tr.get("cast"))}, {tr.get("radius", 160)});')
        elif ty == "typeflash":
            L.append(f'typeFlash(c, {t}, {J(tr["word"])}, {J(tr.get("pattern", "WB"))}, {tr.get("size", 420)}, {J(tr.get("font"))});')
        elif ty in ("freezeclone", "ghost", "popfreeze"):
            k = tr["clip"]
            if not clips[k].get("matte"): continue
            matte(k)
            if ty == "freezeclone": L.append(f'freezeClone(c, L{k}, M{k}, {J(tr["times"])}, {tr["t_end"]});')
            elif ty == "ghost": L.append(f'ghostTrail(c, L{k}, M{k}, {tr["t0"]}, {tr["t1"]}, {tr.get("n", 6)}, {tr.get("dt", 0.05)});')
            else: L.append(f'popFreeze(c, L{k}, M{k}, {t}, {tr.get("frames", 8)}, {tr["sx"]}, {tr["sy"]});')
        elif ty == "print":
            L.append(f'photoPrint(c, L{tr["clip"]}, {t}, {tr.get("frames", 12)}, {J(tr.get("label"))}, {tr.get("rot", -2.5)});')
        elif ty == "grid":
            o, seq, fade = grid_seq(tr.get("pattern", "fill"), tr.get("n", 7))
            L.append(f'flashGrid(c, {t}, {tr.get("n", 7)}, {J(tr.get("vertical", True))}, {J(seq)}, {o}, {J(tr.get("color"))}, {tr.get("fade", fade)}, {tr.get("op", 100)});')
        # ---- geometry + flash (fx_lib section 12) ----
        elif ty == "silstack":
            kb = tr["clipB"]
            if clips[kb].get("matte"):
                matte(kb); L.append(f'silStack(c, {t}, M{kb}, {J(tr.get("pattern", "FI"))}, {J(tr.get("field"))});')
        elif ty == "slices":
            L.append(f'sliceOut(c, L{tr["clipA"]}, L{tr["clipB"]}, {t}, {tr.get("n", 6)}, {tr.get("pre", 4)}, {J(tr.get("vertical", False))}, {tr.get("flash", 82)});')
        elif ty == "iris":
            kb = tr["clipB"]
            if clips[kb].get("matte"):
                matte(kb); L.append(f'silIris(c, L{kb}, M{kb}, {t}, {tr.get("pre", 5)}, {tr["sx"]}, {tr["sy"]}, {tr.get("flash", 72)});')
        elif ty == "rgb":
            n = tr.get("frames", 4); px = tr.get("px", 26)
            if tr.get("clipA") is not None: L.append(f'rgbSplit(c, L{tr["clipA"]}, {round(t - (n // 2) * f1, 5)}, {t}, {px});')
            if tr.get("clipB") is not None: L.append(f'rgbSplit(c, L{tr["clipB"]}, {t}, {round(t + (n - n // 2) * f1, 5)}, {px});')
        elif ty == "pop":
            k = tr["clip"]; cl = clips[k]
            if not cl.get("matte"): continue
            matte(k); t1_, rk, foc, zm = args(cl); d = tr.get("dur", 6 * f1)
            L.append(act(cl, f'var POP{k} = cutoutL(c, {J(P(cl["file"]))}, {t}, {round(t + d, 5)}, {J(rk)}, {foc}, {zm}, M{k}); POP{k}.name = "pop {k}";'))
            L.append(f'popIn(c, POP{k}, M{k}, {t}, {tr["sx"]}, {tr["sy"]}, {d});')
    for b0, b1 in plan.get("breaths", []):
        if b0 < dur: L.append(f'breath(c, {b0}, {min(b1, dur)});')
    # 7. the letterbox bars, type that sits in them, the player popping out over them, then front type
    if band: L.append('bars(c);')
    for w in inbar: word(w)
    for po in plan.get("popouts", []):
        k = po["clip"]; cl = clips[k]
        if po["t0"] >= dur or not cl.get("matte"): continue
        matte(k); t1, rk, foc, zm = args(cl)
        rkm = rk_matte(rk, cl["matte"])     # pop-outs sit above the bars: no mirrored extension
        L.append(act(cl, f'BAND_EXTEND = false; var PM{k} = matteFor(c, {J(P(cl["matte"]["file"]))}, {po["t0"]}, {min(po["t1"], dur)}, {J(rkm)}, {foc}, {zm}); '
                 f'var PO{k} = cutoutL(c, {J(P(cl["file"]))}, {po["t0"]}, {min(po["t1"], dur)}, {J(rk)}, {foc}, {zm}, PM{k}); PO{k}.name = "popout {k}"; BAND_EXTEND = true;'))
    for w in front: word(w)
    for r in plan.get("reticles", []):
        if r["t"] < dur:
            L.append(f'reticle(c, {r["t"]}, {min(r["t1"], dur)}, {r.get("x", plan["w"] / 2)}, {r.get("y", plan["h"] / 2)}, {J(r.get("color"))}, {r.get("r", 110)});')
    # 8. flashes on top, the grade over everything, the end fade last
    for h in plan.get("hits", []):
        t = h["t"]
        if t < dur and "flash" in h:
            f = h["flash"] + [None] * (5 - len(h["flash"]))
            L.append(f'flash(c, {t}, {f[0]}, {J(f[2] or [1, 1, 1])}, {f[1] or 100}, {MODES.get(f[3]) if f[3] else "null"}, {f[4] or 0});')
    if look_ and look_.get("grain"): L.append(f'grain(c, {look_["grain"]});')
    fd = plan.get("fade")
    if fd and fd[0] < dur: L.append(f'fadeOut(c, {fd[0]}, {min(fd[1], dur)});')
    L.append("return c;")
    body = "\n    ".join(L)
    return f'SHOTS[{J(plan["name"])}] = (function () {{\n    {body}\n}})();'

def main():
    pp = sys.argv[1]; plan = json.load(open(pp, encoding="utf-8"))
    test = float(sys.argv[sys.argv.index("--only-test") + 1]) if "--only-test" in sys.argv else None
    rng = [float(v) for v in sys.argv[sys.argv.index("--range") + 1].split("-")] if "--range" in sys.argv else None
    final = "--final" in sys.argv
    base = os.path.dirname(os.path.abspath(pp))
    name = plan["name"] + ("_test" if test else "") + (f"_r{rng[0]:.1f}-{rng[1]:.1f}" if rng else "")
    plan = snap_plan(dict(plan, name=name))
    aedir = os.path.join(base, "ae"); outdir = os.path.join(base, "renders"); os.makedirs(aedir, exist_ok=True)
    jsx = write_jsx(os.path.join(aedir, name + ".jsx"), [dict(name=name, template="prores" if final else "h264")], [spec(plan, test, rng)],
                    out_dir=outdir, libs=(LIB, FXLIB), w=plan["w"], h=plan["h"], fps=plan["fps"], template="h264",
                    aep_path=os.path.join(aedir, name + ".aep"))
    print(jsx)

if __name__ == "__main__":
    main()
