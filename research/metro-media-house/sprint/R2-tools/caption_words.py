#!/usr/bin/env python3
"""Metro Media House style word captions.

Words appear one at a time at their start time, small white Inter Medium,
cap height ~3.6% of frame height, centred vertically at 50%, spread across
the width with wide gaps. A line clears at a sentence end or after 4 words.
Text turns black when the background under it is bright (mean luma > 180).

Usage:
  caption_words.py <bg video|image> <transcript.json> <out.mp4>
                   [--w 1920 --h 1080 --fps 25 --t0 0 --t1 3]
transcript.json: {"words":[{"w":"word","s":0.1,"e":0.4}, ...]}
"""
import argparse, glob, json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont

def find_font():
    for p in ["/usr/share/fonts/opentype/inter/Inter-Medium.otf",
              "/usr/share/fonts/truetype/inter/Inter-Medium.ttf"]:
        if os.path.exists(p):
            return p
    hits = glob.glob("/usr/share/fonts/**/Inter*Medium*.[ot]tf", recursive=True)
    hits = [h for h in hits if "Italic" not in h and "Display" not in h] or hits
    if hits:
        return hits[0]
    out = subprocess.run(["fc-match", "-f", "%{file}", "Inter:medium"],
                         capture_output=True, text=True).stdout.strip()
    return out or None

def font_for_cap(path, cap_px):
    size = max(6, int(cap_px / 0.73))
    for _ in range(6):
        f = ImageFont.truetype(path, size)
        bb = f.getbbox("H")
        h = bb[3] - bb[1]
        if h <= 0:
            break
        size = max(6, int(round(size * cap_px / h)))
    return ImageFont.truetype(path, size)

def group_lines(words, maxw=4):
    lines, cur = [], []
    for wd in words:
        cur.append(wd)
        if len(cur) >= maxw or wd["w"].rstrip().endswith((".", "!", "?")):
            lines.append(cur); cur = []
    if cur:
        lines.append(cur)
    return lines

def is_image(p):
    return p.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".bmp"))

def bg_frames(src, W, H, fps, t0, n):
    if is_image(src):
        im = np.asarray(Image.open(src).convert("RGB").resize((W, H)))
        for _ in range(n):
            yield im.copy()
        return
    cmd = ["ffmpeg", "-v", "error", "-ss", str(t0), "-i", src, "-frames:v", str(n),
           "-vf", f"fps={fps},scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}",
           "-f", "rawvideo", "-pix_fmt", "rgb24", "-"]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    sz = W * H * 3
    last = None
    for _ in range(n):
        buf = p.stdout.read(sz)
        if len(buf) < sz:
            buf = None
        if buf is None:
            yield last if last is not None else np.zeros((H, W, 3), np.uint8)
            continue
        last = np.frombuffer(buf, np.uint8).reshape(H, W, 3).copy()
        yield last
    p.stdout.close(); p.wait()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("bg"); ap.add_argument("transcript"); ap.add_argument("out")
    ap.add_argument("--w", type=int, default=1920); ap.add_argument("--h", type=int, default=1080)
    ap.add_argument("--fps", type=float, default=25); ap.add_argument("--t0", type=float, default=0)
    ap.add_argument("--t1", type=float, default=None)
    ap.add_argument("--png", default=None, help="save frame at this time (s) as PNG next to out")
    a = ap.parse_args()
    W, H = a.w, a.h
    words = json.load(open(a.transcript))["words"]
    words = [{"w": str(x["w"]).strip(), "s": float(x["s"]), "e": float(x["e"])} for x in words if str(x["w"]).strip()]
    t1 = a.t1 if a.t1 is not None else (words[-1]["e"] + 0.5 if words else a.t0 + 3)
    n = max(1, int(round((t1 - a.t0) * a.fps)))
    fpath = find_font()
    if not fpath:
        sys.exit("Inter Medium not found")
    font = font_for_cap(fpath, 0.036 * H)
    lines = group_lines(words)
    margin = int(0.08 * W)
    ff = subprocess.Popen(["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                           "-s", f"{W}x{H}", "-r", str(a.fps), "-i", "-",
                           "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "18", a.out],
                          stdin=subprocess.PIPE)
    png_t = float(a.png) if a.png is not None else None
    for i, bg in enumerate(bg_frames(a.bg, W, H, a.fps, a.t0, n)):
        t = a.t0 + i / a.fps
        im = Image.fromarray(bg)
        dr = ImageDraw.Draw(im)
        line = None
        for li, ln in enumerate(lines):
            nxt = lines[li + 1][0]["s"] if li + 1 < len(lines) else ln[-1]["e"] + 0.6
            if ln[0]["s"] <= t < nxt:
                line = ln; break
        if line:
            k = len(line)
            slot = (W - 2 * margin) / max(k, 1)
            luma = None
            for j, wd in enumerate(line):
                if wd["s"] > t:
                    continue
                tw = dr.textlength(wd["w"], font=font)
                cx = margin + slot * (j + 0.5) if k > 1 else W / 2
                x = int(cx - tw / 2)
                bb = font.getbbox("H")
                y = int(H * 0.5 - (bb[1] + bb[3]) / 2)
                x0, x1 = max(0, x), min(W, int(x + tw))
                y0, y1 = max(0, y + bb[1]), min(H, y + bb[3])
                reg = bg[y0:y1, x0:x1].astype(np.float32)
                if reg.size:
                    luma = (0.299 * reg[..., 0] + 0.587 * reg[..., 1] + 0.114 * reg[..., 2]).mean()
                col = (0, 0, 0) if (luma is not None and luma > 180) else (255, 255, 255)
                dr.text((x, y), wd["w"], font=font, fill=col)
        if png_t is not None and abs(t - png_t) < 0.5 / a.fps:
            im.save(os.path.splitext(a.out)[0] + ".png")
        ff.stdin.write(np.asarray(im).tobytes())
    ff.stdin.close(); ff.wait()
    print("wrote", a.out, "frames", n, "font", fpath)

if __name__ == "__main__":
    main()
