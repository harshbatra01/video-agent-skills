#!/usr/bin/env python3
"""Break-in look test, about 8 s, built objects with real photos, on the real voice.
broll_v4_test.py [still]   'still' writes 4 check frames instead of a video."""
import json, pathlib, re, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

H = pathlib.Path.home(); J = H / "VisionKit/mine/jobs/minidoc-02-anthropic-ipo"
sys.path.insert(0, str(J / "tools"))
from broll_v4_frames import W, HH, font, SANS, wood, fake_site, drop, caption, edge_zoom_ca, rng

P = J / "research/props_v4"; OUT = J / "research/broll_v4/test"; OUT.mkdir(parents=True, exist_ok=True)
FPS = 30; T0, T1 = 22.1, 30.5
WD = json.load(open(J / "vo/v2/words.json")); WD = WD["words"] if isinstance(WD, dict) else WD
MONO = "/System/Library/Fonts/Menlo.ttc"


def word_t(word, after):
    for w in WD:
        if w["t0"] >= after and re.sub(r"\W", "", w["w"]).lower() == word: return w["t0"]
    raise KeyError(word)


T_WORD = word_t("hack", 24.5); T_HACK = word_t("the", 24.5); T_NOINT = word_t("you", 26.5); T_ON = word_t("internet", T_NOINT + 1)
BOLD = {"fake", "hack", "internet", "mistake"}
caps = []; buf = []
for w in WD:
    if w["t1"] < T0 or w["t0"] > T1: continue
    buf.append(w)
    if len(buf) == 2 or re.search(r"[.,?!]$", w["w"].strip()): caps.append(buf); buf = []
if buf: caps.append(buf)
caps = [dict(t0=c[0]["t0"], t1=(caps[i + 1][0]["t0"] if i + 1 < len(caps) else c[-1]["t1"] + .3), w=[(x["w"].strip().rstrip(".,"), re.sub(r"\W", "", x["w"]).lower() in BOLD) for x in c]) for i, c in enumerate(caps)]

# polaroid layers
from broll_v4_wood import wood2
BG_W = wood2(int(W * 1.08), int(HH * 1.08))
card = Image.new("RGB", (700, 700), (238, 234, 222)); card.paste(fake_site(620, 500, "FAKE"), (40, 40))


def polaroid(t):
    age = t - T0; k = min(age / .35, 1); k = 1 - (1 - k) ** 3; z = 1 + .03 * (age / 2.7)
    bg = BG_W.resize((int(W * 1.08 * z), int(HH * 1.08 * z)), Image.BILINEAR); x, y = (bg.width - W) // 2, (bg.height - HH) // 2; bg = bg.crop((x, y, x + W, y + HH))
    s = 1.35 - .35 * k; c = card.resize((int(620 * s), int(620 * s)), Image.BICUBIC); ang = -5 + 11 * (1 - k)
    return drop(bg, c, (W // 2 - c.width // 2 - 20, 500 - c.height // 2), ang, blur=24)


# TV: real photo, real screen position, room pulled dark so the screen carries the frame
tv0 = Image.open(P / "tv_vintage.jpg").convert("RGB").crop((0, 40, 1830, 1412)).resize((1600, 1200), Image.LANCZOS)
a = np.asarray(tv0, np.float32); yy, xx = np.mgrid[0:1200, 0:1600]
SX0, SY0, SX1, SY1 = 391, 182, 1140, 776  # screen box in this crop
d = np.hypot((xx - 765) / 800, (yy - 480) / 640); a *= np.clip(.62 - .5 * d, .07, .62)[..., None] * np.array((.86, .94, 1.08), np.float32)
tv_dark = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
mask = Image.new("L", (1600, 1200), 0); ImageDraw.Draw(mask).rounded_rectangle((SX0, SY0, SX1, SY1), 64, fill=255); mask = mask.filter(ImageFilter.GaussianBlur(4))
fm = ImageFont.truetype(MONO, 104)


def tv(t):
    age = t - (T_HACK - .25); txt = "> hack it"; n = int(np.clip((t - T_WORD + .25) / .05, 0, len(txt) - 2)) + 2
    sw, sh = SX1 - SX0, SY1 - SY0; s = Image.new("RGB", (sw, sh), (6, 14, 12)); d = ImageDraw.Draw(s)
    shown = txt[:n] + ("_" if int(age * 5) % 2 == 0 else " "); d.text((70, sh // 2 - 66), shown, font=fm, fill=(175, 255, 205))
    gl = s.filter(ImageFilter.GaussianBlur(14)); s = Image.fromarray(np.clip(np.asarray(s, np.float32) + np.asarray(gl, np.float32) * .9, 0, 255).astype(np.uint8))
    ar = np.asarray(s, np.float32).copy(); ar[::4] *= .78; y2, x2 = np.mgrid[0:sh, 0:sw]; ar *= (1 - .5 * np.clip(np.hypot((x2 - sw / 2) / (sw / 2), (y2 - sh / 2) / (sh / 2)) - .5, 0, 1))[..., None]
    fr = tv_dark.copy(); fr.paste(Image.fromarray(ar.clip(0, 255).astype(np.uint8)), (SX0, SY0), mask.crop((SX0, SY0, SX1, SY1)))
    z = 1 + .05 * np.clip(age / 2, 0, 1); cw, ch = int(1440 / z * 1.05), int(1080 / z * 1.05); cx, cy = 765, 500
    return fr.crop((cx - cw // 2, cy - ch // 2, cx - cw // 2 + cw, cy - ch // 2 + ch)).resize((W, HH), Image.BICUBIC)


# Earth at night, NASA Black Marble: whole globe with lights removed, pushes in, lights come on at "internet"
e0 = Image.open(P / "earth_night.jpg").convert("RGB").crop((0, 1024, 8192, 7168)).resize((2880, 2160), Image.LANCZOS); ea = np.asarray(e0, np.float32)
warm = np.clip((ea[..., 0] - 26) / 22, 0, 1)[..., None]
base = np.asarray(Image.fromarray((ea * (1 - warm)).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(20)), np.float32)
dark = np.clip((ea * (1 - warm) + base * warm) * 1.55, 0, 255)
bloom = np.asarray(Image.fromarray((ea * warm).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(12)), np.float32)
lit = np.clip(ea * 1.6 + bloom * 2.6, 0, 255)


def earth(t):
    k = np.clip((t - T_ON) / .3, 0, 1); u = np.clip((t - T_NOINT) / (T1 - T_NOINT), 0, 1); u = u * u * (3 - 2 * u)
    z = .5 + .42 * u; cw, ch = int(1440 / z), int(1080 / z); cx = int(1440 - 40 * u); cy = int(1080 - 270 * u)
    x0, y0 = int(np.clip(cx - cw / 2, 0, 2880 - cw)), int(np.clip(cy - ch / 2, 0, 2160 - ch))
    a = dark[y0:y0 + ch, x0:x0 + cw] * (1 - k) + lit[y0:y0 + ch, x0:x0 + cw] * k
    return Image.fromarray(a.clip(0, 255).astype(np.uint8)).resize((W, HH), Image.BICUBIC)


tagf = ImageFont.truetype(SANS[0], 24, index=0)
grain = [np.int16(rng.normal(0, 3.2, (HH // 2, W // 2, 1))).repeat(2, 0).repeat(2, 1) for _ in range(6)]


def frame(i):
    t = T0 + i / FPS
    im = polaroid(t) if t < T_HACK - .25 else tv(t) if t < T_NOINT else earth(t)
    a = edge_zoom_ca(np.asarray(im, np.float32) / 255, .08 if t < T_HACK - .25 else .16, n=4, wash=.35); im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    d = ImageDraw.Draw(im); d.text((W - 190, HH - 56), "ILLUSTRATION", font=tagf, fill=(225, 225, 225))
    for c in caps:
        if c["t0"] <= t < c["t1"]: caption(im, c["w"], 900 if t < T_HACK - .25 else 800); break
    ar = np.asarray(im, np.int16) + grain[i % 6]; f = i - int((T_ON - T0) * FPS)
    if 0 <= f < 3: k = (.8, .45, .15)[f]; ar = (ar * (1 - k) + 255 * k).astype(np.int16)
    return np.clip(ar, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    N = int((T1 - T0) * FPS); print("T_HACK", T_HACK, "T_NOINT", T_NOINT, "T_ON", T_ON, "frames", N)
    if len(sys.argv) > 1:
        S = Image.new("RGB", (4 * 480, 360))
        for j, t in enumerate((23.6, 26.2, 27.3, 29.6)): S.paste(Image.fromarray(frame(int((t - T0) * FPS))).resize((480, 360)), (j * 480, 0))
        S.save(OUT / "still.jpg", quality=86); sys.exit()
    tmp = OUT / "_v.mp4"
    wr = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{HH}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", str(tmp)], stdin=subprocess.PIPE)
    for i in range(N): wr.stdin.write(frame(i).tobytes())
    wr.stdin.close(); wr.wait()
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-i", str(tmp), "-ss", str(T0), "-t", str(T1 - T0), "-i", str(J / "render/v3/Anthropic_IPO_v3.mp4"), "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", str(OUT / "Anthropic_IPO_breakin_test_v1.mp4")], check=True); tmp.unlink(); print("done")
