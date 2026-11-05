"""Real text metrics for laying out type in a plan (After Effects uses the same font files).

as a module:
  w, cap = measure("NEVER", "Coolvetica-HeavyComp", 300, tracking=0)   -> width in px, capital height in px
  xs = line(["NOW", "OR", "NEVER"], font, size, cx=540, gap=0.25)       -> centre x of each word laid out on one line
  fit("NOW OR NEVER", font, max_w=1000)                                 -> the biggest size that fits max_w
Why: guessing widths (0.62 em per letter) put words on top of each other with a condensed font (13 Oct 2026).
Fonts are found by PostScript name in the Windows and per-user font folders (read from each file's name table).
"""
import os, struct, functools
from PIL import ImageFont

DIRS = [d for d in os.environ.get("FONT_DIRS", "").split(os.pathsep) if d] + [
    r"C:\Windows\Fonts", os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts"),
    os.path.expanduser("~/Library/Fonts"), "/Library/Fonts", "/System/Library/Fonts/Supplemental", "/System/Library/Fonts"]


def _psname(path):
    d = open(path, "rb").read(200000)
    if d[:4] == b"ttcf": return None
    n = struct.unpack(">H", d[4:6])[0]
    for i in range(n):
        tag, cs, o, ln = struct.unpack(">4sIII", d[12 + 16 * i: 28 + 16 * i])
        if tag == b"name":
            d = open(path, "rb").read()
            fmt, cnt, so = struct.unpack(">HHH", d[o:o + 6])
            for j in range(cnt):
                pid, eid, lid, nid, l, po = struct.unpack(">HHHHHH", d[o + 6 + 12 * j: o + 18 + 12 * j])
                if nid == 6:
                    s = d[o + so + po: o + so + po + l]
                    return (s.decode("utf-16-be") if pid in (0, 3) else s.decode("latin-1")).replace("\x00", "")
    return None


@functools.lru_cache(None)
def font_files():
    out = {}
    for dd in DIRS:
        if not os.path.isdir(dd): continue
        for f in os.listdir(dd):
            if f.lower().endswith((".ttf", ".otf")):
                try:
                    ps = _psname(os.path.join(dd, f))
                    if ps: out.setdefault(ps, os.path.join(dd, f))
                except Exception:
                    pass
    return out


@functools.lru_cache(None)
def _font(ps, size):
    path = font_files().get(ps)
    if not path: raise KeyError(f"font {ps} not found")
    return ImageFont.truetype(path, size)


def measure(text, ps, size, tracking=0):
    """width (px, including AE tracking: 1/1000 em per unit between letters) and capital height (px)"""
    f = _font(ps, int(round(size)))
    x0, y0, x1, y1 = f.getbbox(text)
    cap = -f.getbbox("H")[1] + f.getbbox("H")[3] if True else 0
    return (x1 - x0) + tracking / 1000 * size * max(0, len(text) - 1), cap


def line(words, ps, size, cx=540, gap=0.25, tracking=0):
    ws = [measure(w, ps, size, tracking)[0] for w in words]; g = gap * size
    total = sum(ws) + g * (len(ws) - 1); x = cx - total / 2; out = []
    for w in ws:
        out.append(round(x + w / 2)); x += w + g
    return out, round(total)


def fit(text, ps, max_w, lo=20, hi=900, tracking=0):
    while hi - lo > 1:
        m = (lo + hi) // 2
        if measure(text, ps, m, tracking)[0] <= max_w: lo = m
        else: hi = m
    return lo


if __name__ == "__main__":
    for ps in ("Coolvetica-HeavyComp", "GalanoGrotesque-Black", "ProximaNova-Semibold"):
        print(ps, measure("NOW OR NEVER", ps, 230), measure("2007", ps, 400), fit("NOW OR NEVER", ps, 1000))
