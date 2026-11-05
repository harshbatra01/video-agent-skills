"""Side by side, frame by frame: our transition vs the reference moment it copies (the training loop's mirror).

usage: python compare.py OUT.png PAIR [PAIR ...] [--n 12] [--h 120] [--stats]
  --stats also prints per frame L/S/C (mean luma / luma spread / colourfulness): flat white = high L, S near 0
  PAIR = "OURS.mp4@t0[@y0,h]|REF.mp4@t0[@crop x0,y0,x1,y1]|label"
  - frames start at t0 and run n frames at each video's own frame rate
  - our @y0,h crops the letterbox band (e.g. @560,800); a ref crop like @438,0,842,720 takes the middle of a pillarbox
Each pair = two rows (ours on top, labelled, then the reference), every thumbnail the same height.
"""
import sys
import av
from PIL import Image, ImageDraw, ImageFont


def grab(path, t0, n, crop=None, band=None):
    c = av.open(path); s = c.streams.video[0]; fps = float(s.average_rate)
    c.seek(int(max(0, t0 - 1.0) / s.time_base), stream=s); out = []
    for fr in c.decode(s):
        t = float(fr.pts * s.time_base)
        if t < t0 - 0.5 / fps: continue
        im = fr.to_image()
        if band: im = im.crop((0, band[0], im.width, band[0] + band[1]))
        if crop: im = im.crop(tuple(crop))
        out.append((t, im))
        if len(out) >= n: break
    c.close()
    return out


def main():
    args = [a for a in sys.argv[1:]]
    stats = "--stats" in args
    if stats: args.remove("--stats")
    n = int(args[args.index("--n") + 1]) if "--n" in args else 12
    H = int(args[args.index("--h") + 1]) if "--h" in args else 120
    for flag in ("--n", "--h"):
        if flag in args: i = args.index(flag); del args[i:i + 2]
    outp, pairs = args[0], args[1:]
    font = ImageFont.truetype(("C:/Windows/Fonts/arialbd.ttf" if sys.platform == "win32" else "/System/Library/Fonts/Supplemental/Arial Bold.ttf"), 11)
    rows = []
    for p in pairs:
        ours, ref, label = p.split("|")
        o = ours.split("@"); r = ref.split("@")
        band = [int(v) for v in o[2].split(",")] if len(o) > 2 else None
        crop = [int(v) for v in r[2].split(",")] if len(r) > 2 else None
        rows.append((label + "  (ours)", grab(o[0], float(o[1]), n, band=band)))
        rows.append((label + "  (reference)", grab(r[0], float(r[1]), n, crop=crop)))
    def scaled(im): return im.resize((max(1, int(im.width * H / im.height)), H))
    W = max(sum(scaled(im).width + 2 for _, im in fr) for _, fr in rows) + 4
    sheet = Image.new("RGB", (W, len(rows) * (H + 30) + 4), (22, 22, 26)); d = ImageDraw.Draw(sheet); y = 2
    for k, (label, frames) in enumerate(rows):
        d.text((4, y), label, fill=(255, 220, 120) if k % 2 == 0 else (150, 200, 255), font=font); x = 2
        for t, im in frames:
            si = scaled(im); sheet.paste(si, (x, y + 14)); d.text((x + 2, y + 14 + H + 1), f"{t:.2f}", fill=(200, 200, 200), font=font); x += si.width + 2
        y += H + 30 + (6 if k % 2 else 0)
    sheet.save(outp); print(outp, sheet.size)
    if stats:      # per-frame numbers: L = mean luma, S = luma spread (structure; flat white/black ~0), C = colourfulness
        import numpy as np
        for label, frames in rows:
            vals = []
            for t, im in frames:
                a = np.asarray(im.convert("RGB").resize((96, max(1, int(96 * im.height / im.width))))).astype(np.float32)
                y = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
                vals.append(f"{y.mean():3.0f}/{y.std():2.0f}/{(a.max(2) - a.min(2)).mean():2.0f}")
            print(f"{label[:34]:34s} " + " ".join(vals))


if __name__ == "__main__":
    main()
