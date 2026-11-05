#!/usr/bin/env python3
"""v4 picture: a word-anchored shot list built from research/ac-rules/AC-RULES.md.
Cuts land on spoken words, not on a grid. Bursts for ideas, holds for proof.
edl_v4.py plan | sheet | picture"""
import hashlib, io, json, pathlib, re, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

H = pathlib.Path.home(); J = H / "VisionKit/mine/jobs/minidoc-02-anthropic-ipo"; E = J / "edit"; SEG = E / "seg_v4"; SEG.mkdir(exist_ok=True)
FO = J / "research/footage"; BL = H / "VisionKit/mine/library/blocks"; PR = J / "research/props_v4"; P1 = H / "VisionKit/mine/jobs/minidoc-01/sources/v4"
FPS, W, HH = 30, 1440, 1080; END = 113.0
WORDS = json.load(open(J / "vo/v2/words.json")); WORDS = WORDS["words"] if isinstance(WORDS, dict) else WORDS
D1, D2, D3, D4 = "x2VHFgyawPE", "hQR_VJF6ukk", "h0x7KpG4Lf0", "aAPpQC-3EyE"
NBC, ABC, BB, WSJ, FB, CBS, HEAR, HQ = "IjCJKr_KzRw", "M8j_Py_TQ9k", "8welyuCkxnM", "q1tw29SieHo", "Agaioeefut0", "YL3FAM4rfy8", "ZC58H12VOHk", "THw8qMS_tVo"
HFB, HFC = "rN_7QlYg_b8", "Y7XVEZZZ0bA"
HC = "hue=s=0,eq=contrast=1.9:brightness=-.05:gamma=.92"; REDT = "colorchannelmixer=rr=1.25:gg=.45:bb=.45"; TEAL = "colorchannelmixer=rr=.8:gg=1.02:bb=1.15"


def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())


def at(word, t0):
    k = norm(word)
    for w in WORDS:
        if w["t0"] >= t0 - .05 and norm(w["w"]).startswith(k): return w["t0"]
    raise SystemExit("word " + word)


V = lambda c, t, vf=None, cx=.5, cy=.5: ("v", c, t, vf, cx, cy)
P = lambda f, tr=None, cx=.5, cy=.5: ("p", str(f), tr, cx, cy)   # still with a push. tr: hc, hcw (subject on white, inverted to black), dark, red
O = lambda name, *a: ("o", name) + a
pr = lambda n: PR / n
p1 = lambda n: P1 / n
BLACK = O("black")
EDL = []


def C(word, after, *shots, at_t=None):
    EDL.append((at(word, after) if at_t is None else at_t, list(shots)))


# ---- 0 to 8.5: hook. One subject, one idea, nothing to read before "resist"
C("Anthropic", 0, V(BB, 58), V(FB, 98), V(NBC, 7), at_t=0.0)
C("released", .8, V(ABC, 37, None, .2))
C("document", 1.4, O("stack"))
C("investors", 2.1, P(p1("nyse_02.jpg"), "hc"), P(p1("nyse_03.jpg")))
C("revealing", 3, V(FB, 79))
C("AI", 3.5, V(D3, 3, TEAL))
C("tried", 4.3, V(D4, 58))
C("resist", 4.9, V(ABC, 57, None, 0))
C("And", 6.7, BLACK)
C("scariest", 7.5, V(D2, 60, HC), V(D1, 200, HC), V(D4, 80, HC))
# ---- 9 to 14.7: why it has to say so
C("Anthropic", 9, V(NBC, 1))
C("IPO", 10.1, V(NBC, 24, None, .35))
C("law", 11.6, P(p1("jx_01.jpg"), "hc"), P(p1("scales_01.jpg"), "hcw"), P(p1("justice_04.jpg"), "hc"), P(p1("lawbooks_01.jpg"), "hc"))
C("tell", 12.9, V(D4, 776))
C("buyers", 13.1, P(p1("nyse_01.jpg")))
C("what", 13.5, V(BB, 96, None, .12))
# ---- 15 to 21.5: the filing, the turn
C("And", 15.1, V(WSJ, 182))
C("shutdown", 15.9, V(ABC, 58, None, 0))
C("it", 16.9, O("doc", "a"))
C("during", 17.5, V(D4, 354))
C("testing", 17.8, V(D4, 364))
C("AI", 18.9, V(FB, 62), O("particle"))
C("broke", 19.4, P(p1("vault_01.jpg"), "hc"), P(p1("vault_02.jpg"), "hc"))
C("real", 20, V(D4, 97))
C("computer", 20.4, O("doc", "a"))
# ---- 22 to 30.8: approved test section
C("One", 22.1, O("polaroid"))
C("The", 24.8, O("tv", "> hack it", "typed"))
C("You", 26.8, O("earth"))
# ---- 30.8 to 50: break-in objects
C("It", 30.7, O("dots"))
C("got", 32.9, P(pr("door_locked.jpg"), "dark"))
C("nowhere", 33.1, P(pr("padlock.jpg"), "dark"), P(p1("padlock_02.jpg"), "hc"), P(pr("door_locked.jpg"), "hc"))
C("So", 34, O("earthlit"))
C("found", 35.3, O("site", "REAL"))
C("almost", 36.6, O("twin"))
C("Its", 38.5, O("tv", "> notes", "still"))
C("real", 40, O("tv", "> real website", "still"))
C("433", 41.4, P(p1("crowd_02.jpg"), "dark"))
C("It", 44, P(p1("lightning_01.jpg"), "dark"), P(p1("fire_03.jpg")))
C("took", 45.4, P(pr("mailboxes.jpg")))
C("deleted", 47, P(pr("shredder.jpg"), "red"))
C("pulled", 48.7, P(pr("switchboard.jpg"), "dark"))
# ---- 50 to 57: the question
C("And", 50.2, V(NBC, 7))
C("no", 51.1, V(D1, 216))
C("And", 52.4, V(D2, 96))
C("found", 52.8, V(D3, 12))
C("what", 53.7, V(NBC, 127))
C("did", 54, V(D4, 104))
C("raises", 54.6, BLACK)
C("about", 56.2, V(NBC, 72, None, .35))
# ---- 57.8 to 70.2: OpenAI and Hugging Face
C("Then", 57.7, V(CBS, 3))
C("July", 58.5, V(HFB, 48, None, .7))
C("most", 59.9, O("wall"))
C("AI", 61.3, O("particle"))
C("OpenAI", 62.9, V(CBS, 8), V(CBS, 13), V(CBS, 10))
C("AI", 64, V(NBC, 181))
C("broke", 64.5, P(p1("vault_02.jpg"), "hc"), P(p1("doors_03.jpg"), "hc"))
C("hacked", 66, V(HFB, 18, None, .25))
C("hugging", 67.7, V(HFC, 64, None, .15))
C("just", 68.6, V(CBS, 169), V(CBS, 171))
C("cheat", 69, V(CBS, 96, None, .1))
# ---- 70.7 to 79: what Anthropic checked
C("So", 70.6, V(D4, 620))
C("checked", 71.4, V(D4, 585))
C("141", 71.7, V(D4, 672))
C("own", 74.2, V(D4, 562), V(D4, 609))
C("It", 75.7, V(HFC, 18, None, .75))
C("including", 77.5, O("polaroid_still"))
# ---- 79 to 90: the questions
C("Researchers", 79, O("tvclip", D4, 560))
C("did", 80.9, O("tv", "> did you have\n  permission?", "still"))
C("Most", 82.4, V(D4, 552))
C("said", 83.4, O("tv", "> yes", "still"))
C("Then", 84.6, V(D4, 640))
C("who", 85.5, O("tv", "> who gave it\n  to you?", "still"))
C("Every", 86.5, V(D4, 576), V(D4, 600), V(D4, 544))
C("admitted", 88.3, O("tv", "> not allowed", "red"))
# ---- 90 to 98: it stopped
C("The", 90.2, V(HEAR, 90, None, 0))
C("stopped", 92.3, BLACK)
C("Every", 93.4, V(D4, 562), V(D4, 632), V(D4, 672))
C("This", 95.3, V(D4, 190))
C("built", 96.7, V(D4, 178))
C("careful", 97.4, V(D1, 30))
# ---- 98 to 107: the turn
C("But", 98.3, BLACK)
C("IPO", 98.6, V(NBC, 26, None, .35))
C("expected", 99.4, V(BB, 57))
C("November", 100.7, P(p1("hourglass_01.jpg"), "dark"))
C("And", 101.6, O("doc", "c"))
C("slow", 103.8, P(p1("scales_01.jpg"), "hcw"), P(p1("jx_01.jpg"), "hc"))
C("safety", 104.4, V(D3, 150))
C("Anthropic", 105.3, V(HEAR, 75, None, 0))
C("sued", 106.4, P(p1("gavel_03.jpg"), "hcw"), P(p1("court_02.jpg"), "hc"))
# ---- 107 to 113: the question
C("So", 107.4, V(D1, 240))
C("AI", 108.3, O("particle"))
C("too", 109, P(p1("fire_03.jpg")), P(p1("lightning_01.jpg"), "dark"))
C("will", 110, V(HEAR, 110, None, 0))
C("still", 110.8, V(D4, 768))

# ---- Second pass after the shot count came out at 119 against about 230 at Altman's rate: more looks per phrase.
C("is", 9.5, V(FB, 109))
C("having", 9.7, V(NBC, 19, None, .35))
C("it", 12.4, V(D4, 8))
C("into", 19.7, P(p1("doors_03.jpg"), "hc"), P(p1("padlock_02.jpg"), "hc"))
C("looking", 34.5, P(pr("tv_sets.jpg"), "dark"))
C("real", 42.3, P(p1("crowd_02.jpg"), "dark", .15))
C("users", 43.1, P(p1("crowd_02.jpg"), "dark", .85))
C("email", 45.8, P(pr("mailboxes.jpg"), "dark", .2))
C("addresses", 46.1, P(pr("mailboxes.jpg"), "hc", .7))
C("user", 47.5, P(pr("shredder.jpg"), "dark", .2))
C("account", 47.9, P(pr("shredder.jpg"), "hc", .8))
C("their", 49, P(pr("switchboard.jpg"), None, .1, .2))
C("chats", 49.2, P(pr("switchboard.jpg"), None, .8, .8))
C("Anthropic", 50.3, V(BB, 176))
C("idea", 51.5, V(D4, 256))
C("out", 53, V(D4, 336))
C("next", 54.2, V(D2, 264))
C("biggest", 55.3, V(D3, 156, HC))
C("question", 55.7, BLACK)
C("came", 58.9, V(HFB, 54, None, .7))
C("probably", 59.2, V(CBS, 26))
C("said", 63.3, V(CBS, 20))
C("test", 65.3, V(CBS, 170))
C("real", 66.5, V(HFB, 30, None, .25))
C("face", 67.85, V(HFC, 104, None, .75))
C("test", 69.8, V(HFB, 42, None, .7))
C("Anthropic", 70.8, V(BB, 64))
C(",006", 72.6, V(D4, 664))
C("of", 73.7, V(D4, 632))
C("test", 74.5, V(D4, 562))
C("runs", 74.9, V(D4, 609))
C("time", 83, V(D4, 576))
C("asked", 84.9, V(D4, 648))
C("single", 87.3, V(D4, 664))
C("time", 87.6, V(D4, 600))
C("saw", 91.1, V(HEAR, 100, None, 0))
C("signs", 91.5, V(HEAR, 120, None, 0))
C("AI", 95.9, V(FB, 62))
C("company", 96.3, V(D4, 192))
C("to", 97.1, V(D4, 296))
C("before", 99.8, V(NBC, 96, None, .35))
C("end", 100.3, V(NBC, 102, None, .35))
C("document", 102.1, V(ABC, 38, None, .2))
C("warns", 102.5, O("doc", "c"))
C("could", 106, V(HEAR, 85, None, 0))
C("next", 107.7, V(D2, 192))
C("time", 107.95, P(p1("hourglass_01.jpg"), "hc"))
C("Anthropic", 110.2, V(HEAR, 115, None, 0))
C("AI", 61.3, P(p1("renaissance_01.jpg"), "hc"), P(p1("statue_05.jpg"), "hc"), P(p1("bust_01.jpg"), "hc"), P(p1("renaissance_02.jpg"), "hc"), O("particle"))
C("law", 11.6, P(p1("jx_01.jpg"), "hc"), P(p1("scales_01.jpg"), "hcw"), P(p1("justice_04.jpg"), "hc"), P(p1("court_03.jpg"), "hc"), P(p1("judge_02.jpg"), "hc"), P(p1("lawbooks_01.jpg"), "hc"))
C("broke", 64.5, P(p1("vault_02.jpg"), "hc"), P(p1("doors_03.jpg"), "hc"), P(p1("padlock_01.jpg"), "hc"), P(p1("vault_01.jpg"), "hc"))
C("nowhere", 33.1, P(pr("padlock.jpg"), "dark"), P(p1("padlock_02.jpg"), "hc"), P(p1("padlock_01.jpg"), "dark"), P(p1("vault_01.jpg"), "hc"), P(pr("door_locked.jpg"), "hc"))

# ---- Third pass, from checking every shot against its words (4 Nov). Each line fixes a named miss.
C("AI", 3.5, O("particle"))  # CBS title card carried a headline about something else
C("it", 12.4, V(FB, 22))  # S-1 cover on "it has to", not a title card
C("during", 17.5, V(D4, 358))  # foreground object blocked half the frame
C("real", 20, V(D4, 96.2))  # stray person, use the office screen
for w_, t_ in (("it", 44), ("too", 109)): pass
C("It", 44, P(p1("lightning_01.jpg"), "dark"), P(p1("fire_01.jpg")))  # burned-in timestamp on fire_03
C("too", 109, P(p1("fire_01.jpg")), P(p1("lightning_01.jpg"), "dark"))
C("no", 51.1, V(D1, 228))  # interviewer in frame
C("idea", 51.5, V(D4, 76))  # host in frame
C("out", 53, V(D2, 36))  # host in frame
C("AI", 64, V(NBC, 181, "crop=1440:842:0:0,scale=1440:1080"))  # chyron about Anthropic's valuation cropped off
C("of", 73.7, V(D4, 354))  # variety of researchers
C("test", 74.5, V(D4, 96.2))
C("Most", 82.4, V(D4, 364))
C("time", 83, V(D4, 112))
C("asked", 84.9, V(D4, 366))  # test logs with readable text from a different test
C("Every", 86.5, V(D4, 576), V(D4, 600), V(D4, 366))  # 544 was a readable email from a different test
C("company", 96.3, V(D4, 196))  # table, not an unnamed close-up
C("real", 20, V(D4, 104))  # stray person, use the code screen
C("of", 73.7, V(D4, 359))
C("test", 74.5, V(D4, 672.5))
C("Then", 84.6, V(D4, 364))  # host in frame
DROP = [("real", 42.3), ("users", 43.1), ("their", 49), ("chats", 49.2), ("saw", 91.1), ("signs", 91.5), ("came", 58.9), ("could", 106), ("Anthropic", 110.2)]  # repeats that looked identical: hold instead

LOW = {"doc": 900, "polaroid": 900, "tv": 900, "tvclip": 900, "stack": 800, "site": 900, "twin": 900, "polaroid_still": 900, "dots": 900}
TOP = {(HFC, 18): 60, (ABC, 57): 790, (ABC, 58): 790, (HFB, 48): 880, (BB, 58): 640, (BB, 64): 640, (BB, 176): 640, (BB, 57): 640, (FB, 98): 640, (FB, 109): 640, (NBC, 7): 640, (CBS, 8): 50, (CBS, 13): 50, (CBS, 10): 50, (FB, 22): 900}


def timeline():
    # a later entry at the same time replaces the earlier one, so a burst can be upgraded in place
    items = []; by = {}
    for t, sh in EDL: by[round(t, 3)] = (t, sh)
    for w, a in DROP: by.pop(round(at(w, a), 3), None)
    marks = sorted(by.values(), key=lambda x: x[0])
    for i, (t, shots) in enumerate(marks):
        f0 = int(round(t * FPS)); f1 = int(round((marks[i + 1][0] if i + 1 < len(marks) else END) * FPS)); n = len(shots); f = f0
        for j, s in enumerate(shots):
            burst = n > 1
            # a burst flickers for its first shots, the last one takes what is left
            d = (f1 - f) if j == n - 1 else max(min(5, (f1 - f0) // n), 2)
            items.append(dict(s=s, f0=f, frames=d)); f += d
    return items


def ffrun(*a): subprocess.run([str(x) for x in a], check=True)


def seg_v(s, frames, out):
    _, c, t, vf, cx, cy = s
    fl = f"scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH}:(iw-{W})*{cx}:(ih-{HH})*{cy},fps={FPS},eq=saturation=1.18:contrast=1.08:gamma=.96"
    if vf: fl += "," + vf
    fl += f",tpad=stop_mode=clone:stop_duration=30,trim=end_frame={frames},setpts=PTS-STARTPTS,format=yuv420p"
    ffrun("ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", t, "-i", FO / f"{c}.mp4", "-t", frames / FPS + 2, "-vf", fl, "-an", "-frames:v", frames, "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-g", "30", out)


class Out:
    def __init__(s, out): s.p = subprocess.Popen(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{HH}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-g", "30", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    def put(s, im): s.p.stdin.write(im.tobytes())
    def close(s): s.p.stdin.close(); s.p.wait()


def cover(im, w=W, h=HH, cx=.5, cy=.5):
    k = max(w / im.width, h / im.height); im = im.resize((int(im.width * k + .5), int(im.height * k + .5)), Image.LANCZOS); x, y = int((im.width - w) * cx), int((im.height - h) * cy); return im.crop((x, y, x + w, y + h))


def treat(im, tr):
    if tr is None: return im
    a = np.asarray(im, np.float32) / 255; y, x = np.mgrid[0:a.shape[0], 0:a.shape[1]]; d = np.hypot((x - a.shape[1] / 2) / (a.shape[1] / 2), (y - a.shape[0] / 2) / (a.shape[0] / 2)) / 1.414
    if tr in ("hc", "hcw"):
        g = a.mean(2, keepdims=True)
        if tr == "hcw": g = 1 - g
        g = np.clip((g - .28) * 2.2, 0, 1) ** 1.05; a = np.repeat(g, 3, 2); a *= np.clip(1.15 - .85 * d[..., None] ** 1.6, .05, 1)
    elif tr == "dark": a = a * np.clip(1.08 - .8 * d[..., None] ** 1.4, .1, 1.1) * np.array((.92, .96, 1.06), np.float32)
    elif tr == "red": a = a * np.clip(1.08 - .8 * d[..., None] ** 1.4, .1, 1.1) * np.array((1.15, .62, .6), np.float32)
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))


def seg_p(s, frames, out):
    _, f, tr, cx, cy = s; im = Image.open(f).convert("RGB")
    big = treat(cover(im, int(W * 1.1), int(HH * 1.1), cx, cy), tr); o = Out(out); bw, bh = big.size
    for i in range(frames):
        z = 1 + .09 * (1 - i / max(frames, 1)); cw, ch = int(bw / z), int(bh / z); x, y = (bw - cw) // 2, (bh - ch) // 2
        o.put(big.crop((x, y, x + cw, y + ch)).resize((W, HH), Image.BILINEAR))
    o.close()


_t = None


def T():
    global _t
    if _t is None:
        sys.path.insert(0, str(J / "tools")); sys.argv = sys.argv[:1] + sys.argv[1:]; import broll_v4_test as m; _t = m
    return _t


def seg_o(s, frames, out, f0):
    name = s[1]; o = Out(out); t0 = f0 / FPS
    if name == "black":
        y, x = np.mgrid[0:HH, 0:W]; d = np.hypot((x - W / 2) / (W / 2), (y - HH * .47) / (HH / 2)); a = np.clip(46 * np.exp(-(d * 1.9) ** 2), 0, 255)[..., None].repeat(3, 2).astype(np.uint8); im = Image.fromarray(a)
        for _ in range(frames): o.put(im)
    elif name == "polaroid":
        m = T()
        for i in range(frames): o.put(m.polaroid(t0 + i / FPS))
    elif name == "polaroid_still":
        m = T()
        for i in range(frames): o.put(m.polaroid(m.T0 + 1 + i / FPS * .4))
    elif name == "earth":
        m = T()
        for i in range(frames): o.put(m.earth(t0 + i / FPS))
    elif name == "earthlit":
        m = T(); a = m.lit
        for i in range(frames):
            z = .92 + .5 * i / max(frames, 1); cw, ch = int(1440 / z), int(1080 / z); cx, cy = 1400, 810 - int(40 * i / max(frames, 1))
            o.put(Image.fromarray(a[cy - ch // 2:cy - ch // 2 + ch, cx - cw // 2:cx - cw // 2 + cw].astype(np.uint8)).resize((W, HH), Image.BICUBIC))
    elif name == "tv":
        m = T(); txt, mode = s[2], s[3]; col = (255, 130, 110) if mode == "red" else (175, 255, 205); fm = ImageFont.truetype(m.MONO, 80 if "\n" in txt or len(txt) > 9 else 104)
        for i in range(frames):
            sw, sh = m.SX1 - m.SX0, m.SY1 - m.SY0; sc = Image.new("RGB", (sw, sh), (14, 6, 6) if mode == "red" else (6, 14, 12)); d = ImageDraw.Draw(sc)
            n = len(txt) if mode != "typed" else int(np.clip(i / 2 - 12, 2, len(txt))); shown = txt[:n] + ("_" if i // 6 % 2 == 0 else " "); box = d.multiline_textbbox((0, 0), txt, font=fm); d.multiline_text((60, (sh - (box[3] - box[1])) // 2 - 10), shown, font=fm, fill=col, spacing=24)
            gl = sc.filter(ImageFilter.GaussianBlur(14)); ar = np.clip(np.asarray(sc, np.float32) + np.asarray(gl, np.float32) * .9, 0, 255); ar[::4] *= .78; fr = m.tv_dark.copy(); fr.paste(Image.fromarray(ar.astype(np.uint8)), (m.SX0, m.SY0), m.mask.crop((m.SX0, m.SY0, m.SX1, m.SY1)))
            z = 1 + .05 * i / max(frames, 1); cw, ch = int(1512 / z), int(1134 / z); x0, y0 = 765 - cw // 2, max(500 - ch // 2, 0); o.put(fr.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, HH), Image.BICUBIC))
    elif name == "tvclip":
        m = T(); sw, sh = m.SX1 - m.SX0, m.SY1 - m.SY0
        raw = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", str(s[3]), "-i", str(FO / f"{s[2]}.mp4"), "-frames:v", str(frames), "-vf", f"fps={FPS},scale={sw}:{sh}:force_original_aspect_ratio=increase,crop={sw}:{sh}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        for i in range(frames):
            b = raw[i * sw * sh * 3:(i + 1) * sw * sh * 3]
            ar = np.frombuffer(b, np.uint8).reshape(sh, sw, 3).astype(np.float32).copy(); ar[::4] *= .82; fr = m.tv_dark.copy(); fr.paste(Image.fromarray(ar.astype(np.uint8)), (m.SX0, m.SY0), m.mask.crop((m.SX0, m.SY0, m.SX1, m.SY1)))
            z = 1 + .05 * i / max(frames, 1); cw, ch = int(1512 / z), int(1134 / z); x0, y0 = 765 - cw // 2, max(500 - ch // 2, 0); o.put(fr.crop((x0, y0, x0 + cw, y0 + ch)).resize((W, HH), Image.BICUBIC))
    elif name in ("site", "twin", "stack"):
        m = T(); import broll_v4_frames as bf
        bg = m.BG_W.crop((0, 0, W, HH)) if name != "stack" else None
        if name == "stack": im0 = bf.paper_stack()
        elif name == "site":
            card = Image.new("RGB", (620, 620), (238, 234, 222)); card.paste(bf.fake_site(620, 500, "REAL").resize((560, 452)), (30, 30)); im0 = bf.drop(bg.copy(), card, (390, 110), 4, blur=24)
        else:
            im0 = bg.copy()
            for tag, x, ang in (("FAKE", 70, -5), ("REAL", 740, 4)):
                card = Image.new("RGB", (580, 580), (238, 234, 222)); card.paste(bf.fake_site(620, 500, tag).resize((524, 423)), (28, 28)); bf.drop(im0, card, (x, 180), ang, blur=24)
        for i in range(frames):
            z = 1.0 + .04 * i / max(frames, 1); cw, ch = int(W / z), int(HH / z); o.put(im0.crop(((W - cw) // 2, (HH - ch) // 2, (W + cw) // 2, (HH + ch) // 2)).resize((W, HH), Image.BILINEAR))
    elif name == "dots":
        cols, rows, st, x0, y0 = 72, 25, 17.2, 118, 250; lay = Image.new("RGB", (W, HH)); d = ImageDraw.Draw(lay); rng = np.random.default_rng(5); pts = []
        for j in range(rows):
            for k in range(cols): pts.append((x0 + k * st, y0 + j * st))
        assert len(pts) == 1800; order = rng.permutation(1800)
        for i in range(frames):
            n = int(1800 * min(1, (i + 1) / max(frames * .72, 1))); lo = pts_draw(pts, order, n); o.put(lo)
    elif name == "doc":
        raw = E / f"raw_doc_{s[2]}.mp4"; o.close(); out = pathlib.Path(out)
        if not raw.exists(): ffrun("python3", BL / "screen-photo-push/screen_push.py", E / "doc" / f"{s[2]}.png", E / "doc" / f"{s[2]}_m.png", raw, "--dur", 3, "--moire", .07)
        return seg_v_raw(raw, frames, out)
    elif name == "wall":
        raw = E / "raw_wall_v4.mp4"; o.close(); out = pathlib.Path(out)
        if not raw.exists(): ffrun("python3", BL / "video-wall/video_wall.py", raw, *[FO / f"{c}.mp4" for c in (NBC, BB, ABC, CBS, HFB, HFC, FB, WSJ, D3, D4, D2, D1, HEAR)], "--start", 30, "--dur", 3)
        return seg_v_raw(raw, frames, out)
    elif name == "particle":
        o.close(); return seg_v_raw(BL / "particle-mind/test/particle_mind_test_v1.mp4", frames, pathlib.Path(out), .5)
    o.close()


def pts_draw(pts, order, n):
    lay = Image.new("RGB", (W, HH)); d = ImageDraw.Draw(lay)
    for k in order[:n]:
        x, y = pts[k]; d.ellipse((x - 5, y - 5, x + 5, y + 5), fill=(255, 62, 44))
    return Image.blend(lay, lay.filter(ImageFilter.GaussianBlur(9)), .35)


def seg_v_raw(raw, frames, out, ss=0):
    fl = f"scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},fps={FPS},tpad=stop_mode=clone:stop_duration=30,trim=end_frame={frames},setpts=PTS-STARTPTS,format=yuv420p"
    ffrun("ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", ss, "-i", raw, "-t", frames / FPS + 2, "-vf", fl, "-an", "-frames:v", frames, "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-g", "30", out)


def seg_key(it):
    s = it["s"]; extra = it["f0"] if s[0] == "o" and s[1] in ("polaroid", "earth") else 0
    return hashlib.md5(json.dumps([s, it["frames"], extra, "v4a"], default=str).encode()).hexdigest()[:12]


def build_one(it):
    s = it["s"]; out = SEG / f"{seg_key(it)}.mp4"
    if out.exists() and out.stat().st_size > 0: return out
    tmp = out.with_suffix(".tmp.mp4")
    if s[0] == "v": seg_v(s, it["frames"], tmp)
    elif s[0] == "p": seg_p(s, it["frames"], tmp)
    else: seg_o(s, it["frames"], tmp, it["f0"])
    tmp.rename(out); return out


def captions():
    toks = []
    for w in WORDS:
        x = w["w"].strip()
        if toks and (x.startswith("-") or x.startswith(",")): toks[-1] = dict(toks[-1], w=toks[-1]["w"] + x, t1=w["t1"])
        else: toks.append(dict(w, w=x))
    BOLD = {"anthropic", "ai", "ipo", "shutdown", "hack", "internet", "real", "433", "1800", "141006", "openai", "hugging", "face", "three", "yes", "stopped", "careful", "november", "sued", "stop", "deleted", "fake", "law", "scariest", "nowhere", "permission", "allowed", "chats"}
    BIG = {"1800": "1,800", "433": "433", "141006": "141,006"}; caps, cur = [], []
    def flush():
        if cur:
            c = dict(t0=cur[0]["t0"], t1=cur[-1]["t1"], w=[[x["w"].strip(",.:?") if norm(x["w"]) not in BIG else BIG[norm(x["w"])], norm(x["w"]) in BOLD] for x in cur])
            if any(norm(x["w"]) in BIG for x in cur): c["big"] = True
            caps.append(c); cur.clear()
    for w in toks:
        if norm(w["w"]) in BIG: flush(); cur.append(w); flush(); continue
        cur.append(w)
        if len(cur) == 3 or w["w"][-1] in ",.?:" or cur[-1]["t1"] - cur[0]["t0"] > .8: flush()
    flush()
    for a, b in zip(caps, caps[1:]): a["t1"] = min(b["t0"], a["t1"] + .25)
    return caps


def tl_json(items):
    low = []
    for it in items:
        s = it["s"]; a, b = it["f0"] / FPS, (it["f0"] + it["frames"]) / FPS
        if s[0] == "o" and s[1] in LOW: low.append([a, b, LOW[s[1]]])
        if s[0] == "v" and (s[1], s[2]) in TOP: low.append([a, b, TOP[(s[1], s[2])]])
    ill = [[at("One", 22) - .1, at("And", 50.2) - .02], [at("Researchers", 79), at("The", 90.2) - .02]]
    flashes = sorted({round(t, 3) for t in (at("resist", 4.9), at("And", 6.7), at("law", 11), at("One", 22), at("internet", 29), at("So", 34), at("And", 50.2), at("Then", 57.7), at("hacked", 66), at("So", 70.6), at("Researchers", 79), at("The", 90.2), at("But", 98.3), at("sued", 106.4))})
    return dict(end=END, edge=.16, wash=.35, cap_y=470, grade=[1.2, .85, 1.12], flash=flashes, captions=captions(), caption_low=low, edge_low=[[at("One", 22) - .1, at("The", 24.7) - .25]],
                whip=[[at("shutdown", 5.4), "SHUTDOWN"], [at("infamous", 60.1), "INFAMOUS"], [at("IPO", 10.1), "IPO"], [at("internet", 29.4), "INTERNET"], [at("hacked", 66), "HACKED"], [at("November", 100.7), "NOVEMBER"], [at("sued", 106.4), "SUED"]], tags=[], illus=ill)


def plan():
    items = timeline(); d = np.array([i["frames"] / FPS for i in items]); kinds = {}
    for i in items: k = "video" if i["s"][0] == "v" or (i["s"][0] == "o" and i["s"][1] in ("particle", "wall", "tvclip", "doc")) else "still/object"; kinds[k] = kinds.get(k, 0) + i["frames"] / FPS
    print("shots", len(items), "median", round(float(np.median(d)), 2), "p90", round(float(np.percentile(d, 90)), 2), "max", round(float(d.max()), 2), "under .25s", int((d < .25).sum()), kinds)
    srcs = {}
    for i in items:
        if i["s"][0] == "v": srcs[i["s"][1]] = srcs.get(i["s"][1], 0) + i["frames"] / FPS
    print({k: round(v, 1) for k, v in srcs.items()})
    for i in items:
        if i["frames"] / FPS > 2.5: print("long", round(i["f0"] / FPS, 2), round(i["frames"] / FPS, 2), i["s"][:3])
    return items


def picture():
    items = plan()
    obj = [i for i in items if i["s"][0] == "o"]; rest = [i for i in items if i["s"][0] != "o"]
    with ThreadPoolExecutor(6) as ex: list(ex.map(build_one, rest))
    for i in obj: build_one(i)
    parts = [SEG / f"{seg_key(i)}.mp4" for i in items]; lst = E / "parts_v4.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    ffrun("ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-r", FPS, E / "picture_v4.mp4")
    json.dump(tl_json(items), open(E / "timeline_v4.json", "w")); json.dump(items, open(E / "items_v4.json", "w"), default=str); print("picture done")


if __name__ == "__main__":
    a = sys.argv[1] if len(sys.argv) > 1 else "plan"; sys.argv = sys.argv[:1]
    if a == "plan": plan()
    if a == "picture": picture()
