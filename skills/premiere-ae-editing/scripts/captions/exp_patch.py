# Patch caption FormattedTextData blobs in a scratch .prproj with per-caption style variants.
# usage: python exp_patch.py SCRATCH.prproj OUT.prproj variants.py   (captions whose text holds "variant N" get APPLY[N])
# The variants file is Python and is run here with exec(): only pass a file you wrote yourself (see variants_example.py).
import gzip, os, re, struct, sys, base64
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fbtool
from fbtool import Table
SRC, DST, VARIANTS = sys.argv[1], sys.argv[2], sys.argv[3]
if os.path.abspath(DST).lower() == os.path.abspath(SRC).lower():
    sys.exit("refusing to overwrite the input: write a new file")
x = gzip.open(SRC).read().decode("utf-8")
def f32(v): return ("raw4", struct.pack("<f", v))
def u32(v): return ("raw4", struct.pack("<I", v))
def u8(v): return ("raw1", bytes([v]))
def color(r, g, b): return ("table", Table({0: u8(r), 1: u8(g), 2: u8(b)}))
def base(T, font="Lora-Italic", size=58, fill=(255, 244, 236)):
    S = T.tab(0)
    S.f[1] = ("vstr", [font])
    run = S.f[0][1][0]; cs = run.tab(1)
    cs.f[1] = f32(size)
    cs.f[2] = color(*fill)
    return S
ns = {"Table": Table, "f32": f32, "u32": u32, "u8": u8, "color": color, "base": base}
exec(open(VARIANTS).read(), ns)
APPLY = ns["APPLY"]
pat = re.compile(r'<FormattedTextData Encoding="base64" BinaryHash="([^"]+)">([^<]+)</FormattedTextData>')
remap = {}
def sub(m):
    h, b64 = m.group(1), m.group(2).strip()
    T = fbtool.parse_b64(b64)
    txt = T.tab(0).f[0][1][0].f[0][1]
    k = int(re.search(r"variant (\d+)", txt).group(1)) if re.search(r"variant (\d+)", txt) else None
    if k is None or k not in APPLY: return m.group(0)
    APPLY[k](T)
    blob = fbtool.build(T); nh = fbtool.new_hash(len(blob)); remap[h] = nh
    return '<FormattedTextData Encoding="base64" BinaryHash="%s">%s\n\t\t</FormattedTextData>' % (nh, base64.b64encode(blob).decode())
x2 = pat.sub(sub, x)
for old, new in remap.items(): x2 = x2.replace('BinaryHash="%s"' % old, 'BinaryHash="%s"' % new)
gzip.open(DST, "wb").write(x2.encode("utf-8"))
print("patched", len(remap), "captions ->", DST)
