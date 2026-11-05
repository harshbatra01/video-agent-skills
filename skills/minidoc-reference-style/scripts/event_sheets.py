# Verification strips: per event, frames from 1 before to 2 after (max 7), labelled. python3 event_sheets.py <events.json> <video> <out_prefix> [per_sheet]
import json, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont
# Font falls back to DejaVu on Linux (patched 5 Nov 2026).
def _pfont(size, paths=("/System/Library/Fonts/Supplemental/Arial.ttf", "/System/Library/Fonts/HelveticaNeue.ttc", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")):
    for p in paths:
        try: return ImageFont.truetype(p, size)
        except OSError: pass
    return ImageFont.load_default()
ev, video, pre = sys.argv[1:4]; per = int(sys.argv[4]) if len(sys.argv) > 4 else 24
E = json.load(open(ev))["events"]; w, h = 160, 120
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3)
F = _pfont(13)
for s in range(0, len(E), per):
    chunk = E[s:s + per]; cols = 7; S = Image.new("RGB", (cols * w + 150, len(chunk) * h), (15, 15, 15)); d = ImageDraw.Draw(S)
    for r, e in enumerate(chunk):
        idx = list(range(max(e["start"] - 1, 0), min(e["end"] + 3, len(V))))[:cols]
        d.text((4, r * h + 4), f"#{s + r + 1} {e['kind']}", font=F, fill=(255, 220, 0))
        d.text((4, r * h + 22), f"t={e['t']:.2f}s  {e['frames']}f", font=F, fill=(220, 220, 220))
        d.text((4, r * h + 40), f"d={e['before_after_diff']} h={e['hdist']}", font=F, fill=(160, 160, 160))
        for c, k in enumerate(idx):
            S.paste(Image.fromarray(V[k]), (150 + c * w, r * h)); d.text((152 + c * w, r * h + 2), str(k), font=F, fill=(0, 255, 0))
    S.save(f"{pre}_{s // per + 1:02d}.jpg", quality=80)
print("sheets:", (len(E) + per - 1) // per)
