#!/usr/bin/env python3
"""Finish pass: flashes, word whips, tags, captions, one edge look over everything.
edit_finish.py <picture.mp4> <timeline.json> <out.mp4> [start end]   (start and end in seconds, for short tests)"""
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.expanduser("~/VisionKit/mine/jobs/minidoc-01/tools"))
from edge_zoom_ca import edge_zoom_ca

W, H, FPS = 1440, 1080, 30
SERIF, SANS = ("/System/Library/Fonts/Supplemental/Didot.ttc", 1), ("/System/Library/Fonts/HelveticaNeue.ttc", 1)
src, tl_path, out = sys.argv[1:4]
T = json.load(open(tl_path))
ss = float(sys.argv[4]) if len(sys.argv) > 4 else 0; ee = float(sys.argv[5]) if len(sys.argv) > 5 else T["end"]
K, WASH = T.get("edge", .16), T.get("wash", .35)
font = lambda p, s: ImageFont.truetype(p[0], s, index=p[1])
fS, fB = font(SERIF, 62), font(SANS, 54); fSb, fBb = font(SERIF, 170), font(SANS, 150)
GR = T.get("grade"); CAP_Y = T.get("cap_y", 740); ILL = T.get("illus", []); EDGE_LOW = T.get("edge_low", []); fI = font((SANS[0], 0), 24)


def caption_img(c):
    HT = 250 if c.get("big") else 130
    im = Image.new("RGBA", (W, HT), (0, 0, 0, 0)); d = ImageDraw.Draw(im); x = 0; parts = []
    for w, bold in c["w"]:
        f = (fBb if bold else fSb) if c.get("big") else (fB if bold else fS); parts.append((w, f, d.textlength(w + " ", font=f)))
    total = sum(p[2] for p in parts) - d.textlength(" ", font=parts[-1][1]); x = (W - total) / 2
    mask = Image.new("L", (W, HT), 0); m = ImageDraw.Draw(mask)
    for w, f, a in parts:
        m.text((x, 30), w, font=f, fill=255); x += a
    return mask


cap_cache = {}


def put_caption(im, c, y):
    key = id(c)
    if key not in cap_cache:
        mask = caption_img(c); cap_cache[key] = (mask, mask.filter(ImageFilter.GaussianBlur(9)))
    mask, glow = cap_cache[key]
    HT = mask.size[1]
    band = np.asarray(im.crop((200, y + 20, W - 200, y + HT - 20)).convert("L"), np.float32).mean()
    bright = band > 150
    col, gcol = ((12, 12, 14), (255, 255, 255)) if bright else ((255, 255, 255), (0, 0, 0))
    im.paste(Image.new("RGB", (W, HT), gcol), (0, y), glow.point(lambda v: min(255, int(v * 1.6))))
    im.paste(Image.new("RGB", (W, HT), col), (0, y), mask)


def whip(im, word, phase):
    "Giant blurred serif word crossing the frame for a few frames."
    f = font(SERIF, 330); lay = Image.new("L", (W * 2, 520), 0); d = ImageDraw.Draw(lay); w = d.textlength(word, font=f); x = W - w / 2 + (0.5 - phase) * 700
    d.text((x, 40), word, font=f, fill=255); lay = lay.filter(ImageFilter.BoxBlur(5)).crop((W // 2, 0, W // 2 + W, 520))
    im.paste(Image.new("RGB", (W, 520), (255, 255, 255)), (0, (H - 520) // 2), lay)


def tag(im, t, kind, age):
    d = ImageDraw.Draw(im); a = min(age / .18, 1);
    if kind == "chyron":
        f = font(SANS, 44); tw = d.textlength(t, font=f); x = 70 - (1 - a) * 500
        d.rectangle((x, 900, x + tw + 56, 980), fill=(190, 20, 30)); d.text((x + 28, 914), t, font=f, fill=(255, 255, 255))
    else:
        f = font(SANS, 70); tw = d.textlength(t, font=f); x = (W - tw) / 2 - 34
        d.rectangle((x, 110, x + tw + 68, 216), fill=(255, 214, 60)); d.text((x + 34, 124), t, font=f, fill=(12, 12, 12))


flash = {}
for t in T["flash"]:
    f = int(round(t * FPS)); flash[f] = .9; flash[f + 1] = .5; flash[f + 2] = .18
whips = {}
for t, word in T["whip"]:
    f = int(round(t * FPS))
    for k in range(4): whips[f + k] = (word, k / 3)
caps = T["captions"]; tags = T["tags"]; low = T.get("caption_low", [])
rng = np.random.default_rng(3); grain = [np.int16(rng.normal(0, 3.2, (H // 2, W // 2, 1))).repeat(2, 0).repeat(2, 1) for _ in range(6)]
N = int((ee - ss) * FPS)
rd = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(ss), "-i", src, "-t", str(ee - ss), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], stdout=subprocess.PIPE)
wr = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
i = 0; ci = 0
while True:
    b = rd.stdout.read(W * H * 3)
    if len(b) < W * H * 3: break
    t = ss + i / FPS; fr = int(round(t * FPS))
    a = np.frombuffer(b, np.uint8).reshape(H, W, 3).astype(np.float32) / 255
    a = edge_zoom_ca(a, .08 if any(p <= t < q for p, q in EDGE_LOW) else K, n=4, wash=WASH)
    if GR:
        a = np.clip(np.clip(a, 0, 1) ** GR[0] * GR[2], 0, 1); l = a.mean(-1, keepdims=True); a = l + (a - l) * GR[1]
    im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    if fr in whips: whip(im, *whips[fr])
    for g in tags:
        if g["t0"] <= t < g["t1"]: tag(im, g["s"], g["kind"], t - g["t0"])
    while ci < len(caps) and caps[ci]["t1"] <= t: ci += 1
    if ci < len(caps) and caps[ci]["t0"] <= t:
        y = next((r[2] if len(r) > 2 else 900 for r in low if r[0] <= t < r[1]), CAP_Y)
        if caps[ci].get("big"): y = min(y, 820) if y != CAP_Y else 410
        put_caption(im, caps[ci], y)
    if any(p <= t < q for p, q in ILL): ImageDraw.Draw(im).text((W - 190, H - 56), "ILLUSTRATION", font=fI, fill=(225, 225, 225))
    arr = np.asarray(im, np.int16) + grain[i % 6]
    if fr in flash:
        k = flash[fr]; arr = (arr * (1 - k) + 255 * k).astype(np.int16)
    wr.stdin.write(np.clip(arr, 0, 255).astype(np.uint8).tobytes()); i += 1
    if i % 300 == 0: print(f"{t:.0f}s", flush=True)
wr.stdin.close(); wr.wait(); rd.stdout.close(); print("frames", i)
