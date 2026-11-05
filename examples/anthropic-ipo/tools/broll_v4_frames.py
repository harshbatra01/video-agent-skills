#!/usr/bin/env python3
"""B-roll v4 test frames beside Attention Compound. No render, stills only.
Writes research/broll_v4/pairs/NN_ours.jpg and NN_ac.jpg plus pairs.json."""
import json, math, pathlib, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

H = pathlib.Path.home(); J = H / "VisionKit/mine/jobs/minidoc-02-anthropic-ipo"
sys.path.insert(0, str(H / "VisionKit/mine/jobs/minidoc-01/tools"))
from edge_zoom_ca import edge_zoom_ca

FO = J / "research/footage"; OUT = J / "research/broll_v4/pairs"; OUT.mkdir(parents=True, exist_ok=True)
W, HH = 1440, 1080
SERIF, SANS = ("/System/Library/Fonts/Supplemental/Didot.ttc", 1), ("/System/Library/Fonts/HelveticaNeue.ttc", 1)
font = lambda p, s: ImageFont.truetype(p[0], s, index=p[1])
REF = {"elon": J / "research/ac-refs/raw1/reel.mp4", "max": J / "research/ac-refs/raw2/reel.mp4", "altman": H / "VisionKit/mine/jobs/minidoc-01/ref/reference.mp4"}
ABC, BB, NBC, CBS, M60, HEAR, FB = "M8j_Py_TQ9k", "8welyuCkxnM", "IjCJKr_KzRw", "YL3FAM4rfy8", "aAPpQC-3EyE", "ZC58H12VOHk", "Agaioeefut0"
rng = np.random.default_rng(7)


def ref_frame(src, k):
    "Frame k of an fps=1 pass, the same frame the 1 fps study sheets show."
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(src), "-vf", f"fps=1,select=eq(n\\,{k})", "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    import io
    return Image.open(io.BytesIO(raw)).convert("RGB")


def grab(src, t):
    raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(t), "-i", str(src), "-frames:v", "1", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
    import io
    return Image.open(io.BytesIO(raw)).convert("RGB")


def fill(im, w=W, h=HH, cx=.5, cy=.5):
    s = max(w / im.width, h / im.height); im = im.resize((int(im.width * s + .5), int(im.height * s + .5)), Image.LANCZOS)
    x = int((im.width - w) * cx); y = int((im.height - h) * cy); return im.crop((x, y, x + w, y + h))


def clip(c, t, **k): return fill(grab(FO / f"{c}.mp4", t), **k)


def vignette(w, h, c0, c1, power=1.6):
    y, x = np.mgrid[0:h, 0:w]; d = np.hypot((x - w / 2) / (w / 2), (y - h / 2) / (h / 2)) / 1.414
    k = np.clip(d, 0, 1) ** power; a = np.array(c0, np.float32) * (1 - k[..., None]) + np.array(c1, np.float32) * k[..., None]
    a += rng.normal(0, 1.6, (h, w, 1)); return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def drop(bg, card, xy, angle=0, blur=26, off=(14, 22), alpha=150):
    c = card.convert("RGBA").rotate(angle, expand=True, resample=Image.BICUBIC); m = c.split()[3]
    s = Image.new("L", bg.size, 0); s.paste(m.point(lambda v: min(v, alpha)), (xy[0] + off[0], xy[1] + off[1])); s = s.filter(ImageFilter.GaussianBlur(blur))
    bg.paste(Image.new("RGB", bg.size, (0, 0, 0)), (0, 0), s); bg.paste(c, xy, m); return bg


def paper_stack():
    "Real filing pages on a grey seamless, Max's press-clipping stack. Yellow mark sits on the real words."
    bg = vignette(W, HH, (232, 232, 234), (120, 120, 124))
    cover = grab(FO / f"{FB}.mp4", 22); cover = cover.crop((int(cover.width * .2), 0, int(cover.width * .8), cover.height))
    a = Image.open(J / "edit/doc/a.png").convert("RGB"); c = Image.open(J / "edit/doc/c.png").convert("RGB")
    arr = np.asarray(a, np.float32).copy(); arr[775:845, 1470:2170] *= np.array((1, .93, .42), np.float32); a = Image.fromarray(arr.astype(np.uint8))
    def page(im, w): return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    drop(bg, page(c, 640), (70, 200), 7); drop(bg, cover.resize((560, int(cover.height * 560 / cover.width)), Image.LANCZOS), (800, 170), -6); drop(bg, page(a, 860), (290, 300), 2)
    return bg


def wood(w, h):
    n = rng.normal(0, 1, (h, 1)); grain = np.convolve(n[:, 0], np.ones(9) / 9, "same")
    rows = np.tile(grain[:, None], (1, w)); xn = rng.normal(0, 1, (h, w)); xn = np.array(Image.fromarray(((xn + 3) * 40).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1)).resize((w, h)), np.float32) / 255 - .5
    v = .5 + rows * 1.1 + xn * .35
    base = np.stack([84 + v * 46, 56 + v * 34, 34 + v * 24], -1); im = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8))
    vg = vignette(w, h, (255, 255, 255), (70, 60, 55), 1.4); return Image.fromarray((np.asarray(im, np.float32) * np.asarray(vg, np.float32) / 255).astype(np.uint8))


def fake_site(w, h, tag):
    im = Image.new("RGB", (w, h), (246, 247, 250)); d = ImageDraw.Draw(im); B = (38, 48, 74); G = (196, 202, 214)
    d.rectangle((0, 0, w, h * .1), fill=(232, 235, 241)); d.rounded_rectangle((w * .05, h * .03, w * .28, h * .07), 6, fill=B)
    d.rounded_rectangle((w * .08, h * .2, w * .62, h * .28), 8, fill=B); d.rounded_rectangle((w * .08, h * .32, w * .5, h * .36), 6, fill=G)
    d.rounded_rectangle((w * .08, h * .41, w * .3, h * .49), 8, fill=(40, 110, 240))
    for i in range(3):
        x = w * (.08 + i * .29); d.rounded_rectangle((x, h * .6, x + w * .26, h * .92), 10, fill=(255, 255, 255), outline=G, width=2)
        d.rounded_rectangle((x + 14, h * .64, x + w * .2, h * .68), 5, fill=B)
        for j in range(3): d.rounded_rectangle((x + 14, h * (.73 + j * .05), x + w * .22, h * (.75 + j * .05)), 3, fill=G)
    f = font(SANS, int(h * .06)); tw = d.textlength(tag, font=f); d.rounded_rectangle((w * .95 - tw - 24, h * .025, w * .95, h * .085), 6, fill=(200, 40, 40)); d.text((w * .95 - tw - 12, h * .03), tag, font=f, fill=(255, 255, 255))
    return im


def polaroid():
    "Fake company page as a photo on wood, Max's gas station polaroid."
    from broll_v4_wood import wood2
    bg = wood2(W, HH); ph = fake_site(620, 500, "FAKE"); card = Image.new("RGB", (700, 700), (238, 234, 222)); card.paste(ph, (40, 40))
    n = np.asarray(card, np.float32) + rng.normal(0, 1.2, (700, 700, 1)); card = Image.fromarray(np.clip(n, 0, 255).astype(np.uint8))
    return drop(bg, card, (340, 150), -5, blur=24)


def cream(draw):
    a = np.asarray(vignette(W, HH, (240, 232, 212), (206, 196, 170), 2.0), np.float32); a += rng.normal(0, 3, a.shape); im = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    S = 3; lay = Image.new("L", (W * S, HH * S), 0); draw(ImageDraw.Draw(lay), S); lay = lay.resize((W, HH), Image.LANCZOS)
    im.paste(Image.new("RGB", (W, HH), (58, 44, 34)), (0, 0), lay); return im


def wifi_off(d, S):
    cx, cy = W * S // 2, int(HH * S * .63); lw = 9 * S
    for r in (120, 230, 340, 450):
        rr = r * S
        for off in (0, 26 * S):  # double line, engraved
            d.arc((cx - rr - off, cy - rr - off, cx + rr + off, cy + rr + off), 222, 318, fill=255, width=lw if off == 0 else 3 * S)
    d.ellipse((cx - 44 * S, cy - 44 * S, cx + 44 * S, cy + 44 * S), outline=255, width=lw)
    for i in range(9):  # hatch in the dot
        y = cy - 36 * S + i * 9 * S; h = int(math.sqrt(max(0, (40 * S) ** 2 - (y - cy) ** 2))); d.line((cx - h, y, cx + h, y), fill=255, width=2 * S)
    d.line((cx - 400 * S, cy - 470 * S, cx + 400 * S, cy + 90 * S), fill=255, width=14 * S)


def dots_1800():
    "1800 dots on black: 1,800 moves, each one a dead end."
    a = np.zeros((HH, W, 3), np.float32); cols, rows = 72, 25; x0, y0, st = 118, 250, 17.2
    im = Image.fromarray(a.astype(np.uint8)); glow = Image.new("RGB", (W, HH)); d = ImageDraw.Draw(glow)
    for j in range(rows):
        for i in range(cols):
            x, y = x0 + i * st, y0 + j * st; lit = (i + j * cols) < 1800
            c = (255, 62, 44) if rng.random() < .985 else (255, 220, 200)
            d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=c)
    im = Image.blend(glow, glow.filter(ImageFilter.GaussianBlur(9)), .35); return Image.fromarray(np.clip(np.asarray(im, np.float32) * 1.1, 0, 255).astype(np.uint8))


def barrel(im, k=.1):
    w, h = im.size; y, x = np.mgrid[0:h, 0:w].astype(np.float32); nx, ny = (x - w / 2) / (w / 2), (y - h / 2) / (h / 2); r = nx ** 2 + ny ** 2
    sx = ((nx * (1 + k * r)) * .94 * w / 2 + w / 2).clip(0, w - 1).astype(int); sy = ((ny * (1 + k * r)) * .94 * h / 2 + h / 2).clip(0, h - 1).astype(int)
    return Image.fromarray(np.asarray(im)[sy, sx])


def tv(screen):
    "Old TV in a dark room with real footage on it, Max's TV row and Elon's five-years TV."
    bg = np.zeros((HH, W, 3), np.float32); top = wood(W, 300); bg[:300] = np.asarray(top, np.float32) * np.linspace(.75, .08, 300)[:, None, None]
    bg[300:] += np.array((12, 10, 9), np.float32); im = Image.fromarray(bg.astype(np.uint8)); bw, bh = 1120, 840; x0, y0 = 160, 150
    body = Image.new("RGBA", (bw, bh), (0, 0, 0, 0)); d = ImageDraw.Draw(body); d.rounded_rectangle((0, 0, bw, bh), 70, fill=(23, 19, 16, 255), outline=(60, 50, 42, 255), width=4)
    d.rounded_rectangle((26, 26, bw - 26, bh - 26), 56, fill=(9, 8, 7, 255)); drop(im, body, (x0, y0), 0, blur=30, alpha=220)
    sw, sh = bw - 120, bh - 120; s = fill(screen, sw, sh); s = barrel(s, .09)
    a = np.asarray(s, np.float32); a[::3] *= .84; a *= 1.06
    y, x = np.mgrid[0:sh, 0:sw]; g = 1 - .55 * np.clip(np.hypot((x - sw / 2) / (sw / 2), (y - sh / 2) / (sh / 2)) - .55, 0, 1) ** 1.5; a *= g[..., None]
    s = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)); m = Image.new("L", (sw, sh), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, sw, sh), 80, fill=255); m = m.filter(ImageFilter.GaussianBlur(3))
    im.paste(s, (x0 + 60, y0 + 60), m)
    lg = Image.new("L", (W, HH), 0); ImageDraw.Draw(lg).rounded_rectangle((x0 + 40, y0 + 40, x0 + bw - 40, y0 + bh - 40), 80, fill=255); lg = lg.filter(ImageFilter.GaussianBlur(60))
    spill = Image.blend(Image.new("RGB", (W, HH)), fill(screen).filter(ImageFilter.GaussianBlur(80)), .4); out = np.asarray(im, np.float32) + np.asarray(spill, np.float32) * (np.asarray(lg, np.float32)[..., None] / 255) * (1 - np.asarray(m.resize((W, HH)), np.float32)[..., None] / 255 * 0)
    return Image.fromarray(np.clip(out, 0, 255).astype(np.uint8))


def chats():
    "Blurred chat cards pulled off a stack. No readable text: invented text would be a fake record."
    bg = vignette(W, HH, (226, 228, 232), (104, 108, 118))
    for i, (x, y, ang) in enumerate([(120, 200, -9), (760, 170, 8), (250, 560, 5), (800, 590, -6), (470, 330, -2)]):
        c = Image.new("RGB", (540, 330), (252, 252, 253)); d = ImageDraw.Draw(c); d.ellipse((28, 26, 84, 82), fill=(150, 165, 190))
        for j in range(5):
            d.rounded_rectangle((104 if j < 2 else 28, 34 + j * 54, 500 - (j * 53 % 120), 62 + j * 54), 10, fill=(150, 156, 170) if j % 2 else (62, 74, 110))
        c = c.filter(ImageFilter.GaussianBlur(4)); drop(bg, c, (x, y), ang, blur=20)
    return bg


def black_word():
    a = vignette(W, HH, (32, 30, 34), (0, 0, 0), .9); return a


def caption(im, words, y=740):
    fS, fB = font(SERIF, 62), font(SANS, 54); d = ImageDraw.Draw(im); parts = [(w, fB if b else fS) for w, b in words]
    wd = [d.textlength(w + " ", font=f) for w, f in parts]; x = (W - sum(wd)) / 2; mask = Image.new("L", (W, 130), 0); m = ImageDraw.Draw(mask)
    for (w, f), a in zip(parts, wd): m.text((x, 30), w, font=f, fill=255); x += a
    band = np.asarray(im.crop((200, y + 20, W - 200, y + 110)).convert("L"), np.float32).mean(); bright = band > 150
    col, g = ((12, 12, 14), (255, 255, 255)) if bright else ((255, 255, 255), (0, 0, 0))
    im.paste(Image.new("RGB", (W, 130), g), (0, y), mask.filter(ImageFilter.GaussianBlur(9)).point(lambda v: min(255, int(v * 1.6)))); im.paste(Image.new("RGB", (W, 130), col), (0, y), mask); return im


def finish(im, words, y=740):
    a = np.asarray(im.convert("RGB"), np.float32) / 255; a = edge_zoom_ca(a, .16, n=4, wash=.35); im = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
    return caption(im, words, y)



PR = J / "research/props_v4"; HFB, HFC = "rN_7QlYg_b8", "Y7XVEZZZ0bA"


def prop(name, cx=.5, cy=.5, k=.62, tint=(.88, .95, 1.08)):
    "A real photo pulled dark at the edges so one object carries the frame."
    im = fill(Image.open(PR / name).convert("RGB"), cx=cx, cy=cy); a = np.asarray(im, np.float32); y, x = np.mgrid[0:HH, 0:W]
    d = np.hypot((x - W / 2) / (W / 2), (y - HH / 2) / (HH / 2)) / 1.414; a *= np.clip(1.05 - k * d ** 1.4, .1, 1.1)[..., None] * np.array(tint, np.float32)
    return Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))


def earth_dark():
    e = Image.open(PR / "earth_night.jpg").convert("RGB").crop((1000, 1400, 7200, 6050)).resize((W, HH), Image.LANCZOS); a = np.asarray(e, np.float32)
    m = np.clip((a[..., 0] - 26) / 22, 0, 1)[..., None]; b = np.asarray(Image.fromarray((a * (1 - m)).clip(0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14)), np.float32)
    return Image.fromarray(((a * (1 - m) + b * m) * .9).clip(0, 255).astype(np.uint8))


def tv_real(screen):
    "The real old TV photo with footage on its real screen."
    t = Image.open(PR / "tv_vintage.jpg").convert("RGB").crop((0, 40, 1830, 1412)).resize((1600, 1200), Image.LANCZOS); a = np.asarray(t, np.float32); yy, xx = np.mgrid[0:1200, 0:1600]
    a *= np.clip(.62 - .5 * np.hypot((xx - 765) / 800, (yy - 480) / 640), .07, .62)[..., None] * np.array((.86, .94, 1.08), np.float32); t = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    x0, y0, x1, y1 = 391, 182, 1140, 776; s = fill(screen, x1 - x0, y1 - y0); ar = np.asarray(s, np.float32).copy(); ar[::4] *= .82; s = Image.fromarray(ar.clip(0, 255).astype(np.uint8))
    m = Image.new("L", (x1 - x0, y1 - y0), 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, x1 - x0, y1 - y0), 64, fill=255); t.paste(s, (x0, y0), m.filter(ImageFilter.GaussianBlur(4)))
    return t.crop((45, 0, 1485, 1080))


PAIRS = [
 dict(t="1.0 s", say="released a document", ours=lambda: clip(ABC, 37, cx=.2), cap=[("released a", 0), ("document", 1)], src="ABC News: the reporter holds the filing pages", ac=("altman", 47), kind="Real news"),
 dict(t="2.0 s", say="for investors", ours=paper_stack, cap=[("for", 0), ("investors", 1)], src="Built: real S-1 pages, highlight on the real words", ac=("max", 55), kind="Built object"),
 dict(t="5.2 s", say="resist shutdown", ours=lambda: clip(ABC, 57, cx=0), cap=[("resist", 0), ("shutdown", 1)], src="ABC News: its card with this exact phrase", ac=("altman", 27), kind="Real news"),
 dict(t="12.9 s", say="what could go wrong", ours=lambda: clip(BB, 96, cx=.12), cap=[("what could go", 0), ("wrong", 1)], src="Bloomberg: on-air chyron on the risk warning", ac=("elon", 34), kind="Real news"),
 dict(t="19.0 s", say="during testing", ours=lambda: clip(M60, 364), cap=[("during", 0), ("testing", 1)], src="60 Minutes: Anthropic staff in their office", ac=("max", 13), kind="Real people"),
 dict(t="23.0 s", say="a fake company", ours=polaroid, cap=[("a", 0), ("fake", 1), ("company", 0)], src="Built: illustration, invented page", ac=("max", 40), kind="Built object"),
 dict(t="27.2 s", say="you have no internet", ours=earth_dark, cap=[("no", 0), ("internet", 1)], src="NASA Black Marble with the city lights removed", ac=("elon", 44), kind="Real photo, altered"),
 dict(t="33.2 s", say="got nowhere", ours=lambda: prop("door_locked.jpg", k=.8), cap=[("got", 0), ("nowhere", 1)], src="Commons photo: chained, locked gate", ac=("elon", 56), kind="Real photo"),
 dict(t="42.0 s", say="433 real users", ours=lambda: prop("mailboxes.jpg", k=.5, tint=(1, 1, 1)), cap=[("433", 1), ("real users", 0)], src="Commons photo: endless mailboxes", ac=("elon", 56), kind="Real photo"),
 dict(t="46.5 s", say="deleted a user's account", ours=lambda: prop("shredder.jpg", k=.7, tint=(1, .9, .9)), cap=[("deleted", 1)], src="Commons photo: paper shredder blades", ac=("altman", 28), kind="Real photo"),
 dict(t="48.5 s", say="pulled their chats", ours=lambda: prop("switchboard.jpg", k=.7, tint=(1, 1, 1)), cap=[("pulled their", 0), ("chats", 1)], src="Commons photo: old telephone switchboard", ac=("max", 40), kind="Real photo"),
 dict(t="66.5 s", say="hacked a real company", ours=lambda: clip(HFB, 18, cx=.25), capy=560, cap=[("hacked a", 0), ("real company", 1)], src="Bloomberg: chyron says OpenAI's models hacked Hugging Face", ac=("altman", 60), kind="Real news"),
 dict(t="68.0 s", say="Hugging Face", ours=lambda: clip(HFC, 64, cx=.15), capy=560, cap=[("Hugging", 1), ("Face", 1)], src="CNBC: Hugging Face's CEO on the hack, name in the chyron", ac=("elon", 34), kind="Real people"),
 dict(t="76.5 s", say="three break-ins", ours=lambda: clip(HFC, 18, cx=.75), capy=60, cap=[("three", 1), ("break-ins", 0)], src="CNBC card, dated 7/30: Anthropic says its models hacked 3 companies in testing", ac=("altman", 27), kind="Real news"),
 dict(t="79.5 s", say="researchers asked the AI", ours=lambda: tv_real(clip(M60, 560)), cap=[("Researchers", 1), ("asked", 0)], src="Real old-TV photo. On screen: 60 Minutes, researcher at test logs", ac=("max", 29), kind="Built object"),
 dict(t="91.0 s", say="it stopped", ours=lambda: clip(HEAR, 90, cx=0), cap=[("it", 0), ("stopped", 1)], src="Senate hearing: nameplate reads Dario Amodei", ac=("elon", 35), kind="Real people"),
 dict(t="96.5 s", say="built to be careful", ours=lambda: clip(M60, 190), cap=[("built to be", 0), ("careful", 1)], src="60 Minutes: Anthropic people round a table", ac=("elon", 61), kind="Real people"),
 dict(t="110.5 s", say="will Anthropic still stop?", ours=lambda: clip(M60, 768), cap=[("still", 0), ("stop?", 1)], src="60 Minutes: the CEO, close", ac=("elon", 66), kind="Real people"),
]


def main():
    data = []
    for i, p in enumerate(PAIRS, 1):
        im = finish(p["ours"](), p["cap"], p.get("capy", 740)); n = f"{i:02d}"; im.resize((720, 540), Image.LANCZOS).save(OUT / f"{n}_ours.jpg", quality=86)
        r, t = p["ac"]; g = ref_frame(REF[r], t); g = g.resize((int(g.width * 540 / g.height), 540), Image.LANCZOS); g.save(OUT / f"{n}_ac.jpg", quality=86)
        data.append(dict(n=n, t=p["t"], say=p["say"], src=p["src"], ac=f"{ {'elon': 'AC Elon', 'max': 'AC Max', 'altman': 'AC Altman'}[r]} at {t} s", kind=p["kind"])); print(n, p["say"], flush=True)
    json.dump(data, open(OUT / "pairs.json", "w"), indent=1)
    names = sorted(OUT.glob("*_ours.jpg")); S = Image.new("RGB", (900, 225 * len(names)), (20, 20, 20))
    for j, q in enumerate(names):
        a = Image.open(q).resize((300, 225)); b = Image.open(str(q).replace("_ours", "_ac")); b = b.resize((int(b.width * 225 / b.height), 225)); S.paste(a, (0, j * 225)); S.paste(b, (310, j * 225))
    S.save(OUT / "check.jpg", quality=82)


if __name__ == "__main__": main()
