#!/usr/bin/env python3
"""Every shot of a reel with the words said over it. ac_shot_words.py <video> <transcript.json> <out_prefix> [thr]
Writes <prefix>_NN.jpg sheets and <prefix>_shots.json."""
import io, json, re, subprocess, sys
from PIL import Image, ImageDraw, ImageFont
v, tj, px = sys.argv[1:4]; thr = float(sys.argv[4]) if len(sys.argv) > 4 else .25
W = json.load(open(tj)); W = W["words"] if isinstance(W, dict) else W
W = [dict(w=w["w"], s=w.get("s", w.get("t0")), e=w.get("e", w.get("t1"))) for w in W]
def _font(path, size):
    try: return ImageFont.truetype(path, size)
    except OSError: return ImageFont.load_default()
raw = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-i", v, "-vf", f"scale=320:-2,select='gt(scene,{thr})',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
cuts = [0.0] + [float(x) for x in re.findall(r"pts_time:([\d.]+)", raw)]
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", v], capture_output=True, text=True).stdout); cuts.append(dur)
shots = []
for a, b in zip(cuts, cuts[1:]):
    if b - a < .03: continue
    ws = " ".join(w["w"].strip() for w in W if w["s"] < b and w["e"] > a and min(w["e"], b) - max(w["s"], a) > .35 * (w["e"] - w["s"]))
    shots.append(dict(t0=round(a, 2), t1=round(b, 2), words=ws))
json.dump(shots, open(px + "_shots.json", "w"), indent=0)
CW, CH, TH, COLS, ROWS = 200, 150, 44, 12, 8; f = _font("/System/Library/Fonts/HelveticaNeue.ttc", 14); fy = _font("/System/Library/Fonts/HelveticaNeue.ttc", 12)
n = COLS * ROWS
for k in range(0, len(shots), n):
    S = Image.new("RGB", (COLS * CW, ROWS * (CH + TH)), (18, 18, 18)); d = ImageDraw.Draw(S)
    for j, s in enumerate(shots[k:k + n]):
        t = (s["t0"] + s["t1"]) / 2; r = subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-ss", f"{t:.3f}", "-i", v, "-frames:v", "1", "-vf", f"scale={CW}:{CH}:force_original_aspect_ratio=decrease,pad={CW}:{CH}", "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        x, y = (j % COLS) * CW, (j // COLS) * (CH + TH)
        if r: S.paste(Image.open(io.BytesIO(r)).convert("RGB"), (x, y))
        d.text((x + 2, y + CH + 1), f"{s['t0']:.1f} {s['t1'] - s['t0']:.2f}s", font=fy, fill=(255, 220, 60)); d.text((x + 2, y + CH + 16), s["words"][:30], font=f, fill=(255, 255, 255)); d.text((x + 2, y + CH + 30), s["words"][30:60], font=fy, fill=(210, 210, 210))
    S.save(f"{px}_{k // n + 1:02d}.jpg", quality=80)
print(px, "shots", len(shots))
