"""style_captions.py: style the captions of a SAVED Premiere project (Premiere has no scripting API for caption style).

Premiere stores every caption block's text and style as a FlatBuffers blob (<FormattedTextData> inside <Block>
objects). This rewrites those blobs with the fields that were mapped and verified by renders in Premiere 26.5
(Oct 2026, a vertical reel job): font, size, fill colour, shadow off, background box colour / opacity / padding, and the
vertical offset. It writes a NEW project file; the input is never changed.

Close the project in Premiere first (patch the saved file, then open the output), and ask before opening it in a
Premiere that has the user's own projects open: a malformed blob crashed Premiere on open once (every open project
went down with it). Only fields whose types appear in real Premiere blobs are written; see
references/captions-style-patch.md for the field map and the traps.

usage:
  python3 style_captions.py IN.prproj --list
      count caption blobs per font (Premiere's default font for new captions shows up here; on the Mac this was built on it was Monaco)
  python3 style_captions.py IN.prproj OUT.prproj --font Inter-ExtraBold --size 33 [--color 255,255,255]
      [--box 5,11,20 --box-opacity 86 --pad 14] [--no-shadow] [--only-font Monaco] [--y-json heights.json] [--offset F] [--dry]

  --only-font   touch only blobs whose current font is this one (e.g. only the new, still default-styled captions)
  --y-json      JSON {"caption text": y_centre_px, ...} for a 1080x1920 frame; offset = (y - 959) / 1922.2 - 0.439
                (measured on 1080x1920 only: measure again before using it on another frame size)
  --offset      one raw vertical offset for every touched caption (fraction of frame height from the default bottom slot)
Duplicate caption texts share one blob, so they always share one style.
Font names are Adobe's PostScript names; variable fonts may need Adobe's instance name (LoraItalic-Italic, not
Lora-Italic, which silently falls back). Premiere only sees fonts installed before it launched.
"""
import argparse, base64, gzip, json, os, re, struct, sys
import xml.etree.ElementTree as ET

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fbtool  # noqa: E402
from fbtool import Table  # noqa: E402

BLOB = re.compile(r'<FormattedTextData Encoding="base64" BinaryHash="([^"]+)">([^<]+)</FormattedTextData>')


def f32(v): return ("raw4", struct.pack("<f", v))
def u8(v): return ("raw1", bytes([v]))
def color(r, g, b): return ("table", Table({0: u8(r), 1: u8(g), 2: u8(b)}))
def rgb(s): return tuple(int(x) for x in s.split(","))
def offset_for_y(y): return (y - 959.0) / 1922.2 - 0.439


def text_and_font(T):
    S = T.tab(0)
    txt = S.f[0][1][0].f[0][1]
    font = S.f[1][1][0] if 1 in S.f else None
    return txt, font


def style(T, font, size, fill=None, shadow_off=False, box=None, box_opacity=None, pad=None, offset=None):
    """Write the verified fields of the style table (root.f0). Field map: f1 font list; runs f0[*].f1 char style
    (f1 size f32, f2 fill colour table); f11 shadow on (u8); f17 box colour, f18 box on (u8, required), f19 box opacity
    in % (68.0, not 0.68), f20 padding px; f33.f2 vertical offset (f32)."""
    S = T.tab(0)
    S.f[1] = ("vstr", [font])
    for run in S.f[0][1]:
        cs = run.tab(1)
        cs.f[1] = f32(size)
        if fill: cs.f[2] = color(*fill)
    if shadow_off: S.f[11] = u8(0)
    if box:
        S.f[17] = color(*box); S.f[18] = u8(1)
        S.f[19] = f32(box_opacity if box_opacity is not None else 100.0)
        if pad is not None: S.f[20] = f32(pad)
    if offset is not None:
        t33 = S.tab(33)
        if t33 is None: S.f[33] = ("table", Table({2: f32(offset)}))
        else: t33.f[2] = f32(offset)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inp"); ap.add_argument("out", nargs="?")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--font"); ap.add_argument("--size", type=float)
    ap.add_argument("--color", type=rgb); ap.add_argument("--no-shadow", action="store_true")
    ap.add_argument("--box", type=rgb); ap.add_argument("--box-opacity", type=float); ap.add_argument("--pad", type=float)
    ap.add_argument("--only-font"); ap.add_argument("--y-json"); ap.add_argument("--offset", type=float)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    x = gzip.open(a.inp).read().decode("utf-8")

    if a.list:
        fonts = {}
        for m in BLOB.finditer(x):
            try: _, font = text_and_font(fbtool.parse_b64(m.group(2)))
            except Exception: font = "(unparsed)"
            fonts[font] = fonts.get(font, 0) + 1
        for k, v in sorted(fonts.items(), key=lambda kv: -kv[1]): print("%5d  %s" % (v, k))
        return
    if not (a.out and a.font and a.size): sys.exit("need OUT.prproj, --font and --size (or --list)")
    if os.path.abspath(a.out) == os.path.abspath(a.inp): sys.exit("refusing to overwrite the input: write a new file")
    Y = json.load(open(a.y_json)) if a.y_json else None

    remap, done, skipped = {}, [], 0
    def sub(m):
        nonlocal skipped
        h, b64 = m.group(1), m.group(2).strip()
        T = fbtool.parse_b64(b64)
        txt, font = text_and_font(T)
        if a.only_font and font != a.only_font: skipped += 1; return m.group(0)
        off = a.offset
        if Y is not None:
            if txt not in Y: skipped += 1; return m.group(0)
            off = offset_for_y(float(Y[txt]))
        style(T, a.font, a.size, a.color, a.no_shadow, a.box, a.box_opacity, a.pad, off)
        blob = fbtool.build(T); nh = fbtool.new_hash(len(blob)); remap[h] = nh; done.append(txt)
        return '<FormattedTextData Encoding="base64" BinaryHash="%s">%s\n\t\t</FormattedTextData>' % (nh, base64.b64encode(blob).decode())
    x2 = BLOB.sub(sub, x)
    for old, new in remap.items(): x2 = x2.replace('BinaryHash="%s"' % old, 'BinaryHash="%s"' % new)
    ET.fromstring(x2)   # still well-formed
    print("styled %d caption blobs (%d unique texts); left alone %d" % (len(done), len(set(done)), skipped))
    if a.dry: print("dry run: nothing written"); return
    with gzip.open(a.out, "wb") as f: f.write(x2.encode("utf-8"))
    print("wrote", a.out)


if __name__ == "__main__":
    main()
