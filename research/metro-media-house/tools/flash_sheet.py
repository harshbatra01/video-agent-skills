#!/usr/bin/env python3
# One sheet of every non-plain-CUT event (CUT+FLASH, FLASH, FLICKER): frames from 2 before to 4 after.
# flash_sheet.py <events.json> <video> <out.jpg>
import json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
ev, video, out = sys.argv[1:4]
E = [e for e in json.load(open(ev))["events"] if e["kind"] != "CUT"]
w, h = 192, 108
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
F = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
cols = 8; S = Image.new("RGB", (cols * w + 130, max(1, len(E)) * h), (15, 15, 15)); d = ImageDraw.Draw(S)
for r, e in enumerate(E):
    idx = list(range(max(e["start"] - 2, 0), min(e["end"] + 5, len(V))))[:cols]
    d.text((4, r * h + 4), f"{e['kind']}", font=F, fill=(255, 220, 0)); d.text((4, r * h + 22), f"t={e['t']:.2f}s {e['frames']}f", font=F, fill=(220, 220, 220))
    for c, k in enumerate(idx):
        S.paste(Image.fromarray(V[k]), (130 + c * w, r * h)); d.text((132 + c * w, r * h + 2), str(k), font=F, fill=(0, 255, 0))
S.save(out, quality=82); print(len(E), "events")
