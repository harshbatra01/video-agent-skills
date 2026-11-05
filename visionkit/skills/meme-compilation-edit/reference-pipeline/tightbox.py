"""Tight curse-word boxes: measure the actual letters inside the OCR word box, drop trailing punctuation,
then pad by a fixed number of on-screen pixels (at least 5 image pixels). Feather: 10 image pixels, as in the client editor's files."""
import numpy as np
from PIL import Image

PAD_SCREEN = 7        # padding around the letters, in 1080p sequence pixels
MIN_PAD_SRC = 5.0     # and never under 5 image pixels, so the feather's soft edge starts outside the letters
FEATHER_MIN_SCREEN = 14.0  # ...and at least 14 px on screen: on big phone screenshots shown at 40-90% a flat 10 image px
                      # is only 4-9 px on screen, still a hard edge (the editor's curse feathers are about 14 px on screen)
FEATHER_SRC = 10.0    # mask feather in the image's own pixels, the same as the editor's files (Oct 13 2026: our 2-5 px feathers
                      # made curse blurs look like hard blank boxes, "blurred too aggressively, can you check [the editor's] files?")

def tight_word_box(path, word_box, scale):
    """word_box: OCR box [x0,y0,x1,y1] normalized. scale: clip scale (1.0 = 100%). Returns (box, feather_layer_px)."""
    im = np.asarray(Image.open(path).convert("RGB")).astype(int)
    H, W, _ = im.shape
    x0, y0, x1, y1 = word_box
    h = (y1 - y0) * H
    ex, ey = 0.08 * h, 0.15 * h
    X0, Y0 = max(0, int(x0 * W - ex)), max(0, int(y0 * H - ey))
    X1, Y1 = min(W, int(x1 * W + ex)), min(H, int(y1 * H + ey))
    reg = im[Y0:Y1, X0:X1]
    border = np.concatenate([reg[0], reg[-1], reg[:, 0], reg[:, -1]])
    bg = np.median(border, axis=0)
    ink = np.abs(reg - bg).max(axis=2) > 60
    # keep only the band of rows that holds the word itself (drops ascenders/descenders of neighbouring lines)
    rowsum = ink.sum(axis=1)
    bands, r = [], 0
    while r < len(rowsum):
        if rowsum[r]:
            q = r
            while q < len(rowsum) and (rowsum[q] or (q + 1 < len(rowsum) and rowsum[q + 1])):
                q += 1
            bands.append((r, q, int(rowsum[r:q].sum())))
            r = q
        else:
            r += 1
    cy = (y0 + y1) / 2 * H - Y0
    band = max(bands, key=lambda b: (b[0] <= cy <= b[1], b[2]))
    ink[:band[0]] = False; ink[band[1]:] = False
    cols = ink.any(axis=0)
    # glyph runs (columns with ink), then drop small trailing/leading marks such as . , ! ?
    runs, c = [], 0
    while c < len(cols):
        if cols[c]:
            d = c
            while d < len(cols) and cols[d]:
                d += 1
            rows = np.where(ink[:, c:d].any(axis=1))[0]
            runs.append([c, d, rows[0], rows[-1] + 1])
            c = d
        else:
            c += 1
    tallest = max(r[3] - r[2] for r in runs)
    while len(runs) > 1 and runs[-1][3] - runs[-1][2] < 0.4 * tallest:
        runs.pop()
    while len(runs) > 1 and runs[0][3] - runs[0][2] < 0.4 * tallest:
        runs.pop(0)
    ix0 = X0 + runs[0][0]; ix1 = X0 + runs[-1][1]
    iy0 = Y0 + min(r[2] for r in runs); iy1 = Y0 + max(r[3] for r in runs)
    feather = max(FEATHER_SRC, FEATHER_MIN_SCREEN / scale)   # never under 10 image px, never under 14 px on screen
    pad = max(PAD_SCREEN / scale, MIN_PAD_SRC, feather / 2)   # the soft edge starts outside the letters
    box = [(ix0 - pad) / W, (iy0 - pad) / H, (ix1 + pad) / W, (iy1 + pad) / H]
    return [round(v, 4) for v in box], round(feather, 2)
