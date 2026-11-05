# Schema-less round-trip for Premiere's text FlatBuffers (12-byte header: u32 len(fb), u32 0, u32 0x11223344).
# parse() -> nested Table objects with typed scalars; build() -> bytes. Children are laid out after parents
# (uoffsets point forward), vtables precede their tables, scalars aligned to their size.
import base64, struct, os

def U16(b, o): return struct.unpack_from("<H", b, o)[0]
def U32(b, o): return struct.unpack_from("<I", b, o)[0]
def I32(b, o): return struct.unpack_from("<i", b, o)[0]

class Table:
    def __init__(self, fields=None): self.f = dict(fields or {})   # idx -> (kind, value)
    def get(self, i): return self.f.get(i)
    def set(self, i, kind, val): self.f[i] = (kind, val)
    def tab(self, i):
        v = self.f.get(i); return v[1] if v and v[0] == "table" else None

def _isstr(b, p):
    if p < 0 or p + 4 > len(b): return None
    n = U32(b, p)
    if 0 <= n < 4000 and p + 4 + n < len(b) and b[p + 4 + n] == 0:
        try: t = b[p + 4:p + 4 + n].decode("utf-8")
        except Exception: return None
        if all(c >= " " or c in "\n\r\t" for c in t): return t
        return None
    return None
def _istable(b, p):
    if p < 0 or p + 4 > len(b) or p % 2: return False
    vt = p - I32(b, p)
    if vt < 0 or vt + 4 > len(b) or vt % 2: return False
    vl, tl = U16(b, vt), U16(b, vt + 2)
    return 4 <= vl <= 300 and vl % 2 == 0 and 4 <= tl <= 1000

# Field kinds known from Premiere's text data (path from the root table; "*" = any vector element).
FORCE = {(0, 0, "*", 0): "str", (0, 32, "*", 0): "str", (0, 1): "vstr", (0, 0): "vtab", (0, 32): "vtab", (0, 0, "*", 1): "table"}
def _force(path):
    k = FORCE.get(path)
    if k: return k
    return None
def _read_forced(b, p, kind, path):
    v = U32(b, p); tgt = p + v
    if kind == "str":
        n = U32(b, tgt); return "str", b[tgt + 4:tgt + 4 + n].decode("utf-8")
    if kind == "table": return "table", parse_table(b, tgt, path)
    n = U32(b, tgt); elems = []
    for j in range(n):
        q = tgt + 4 + 4 * j; w = U32(b, q); qt = q + w
        if kind == "vstr": m = U32(b, qt); elems.append(b[qt + 4:qt + 4 + m].decode("utf-8"))
        else: elems.append(parse_table(b, qt, path + ("*",)))
    return kind, elems
def parse_table(b, t, path=()):
    vt = t - I32(b, t); vl, tl = U16(b, vt), U16(b, vt + 2); nf = (vl - 4) // 2
    offs = [U16(b, vt + 4 + 2 * i) for i in range(nf)]
    pres = sorted((o, i) for i, o in enumerate(offs) if o)
    T = Table()
    for k, (o, i) in enumerate(pres):
        nxt = pres[k + 1][0] if k + 1 < len(pres) else tl
        gap = nxt - o; p = t + o
        fk = _force(path + (i,))
        if fk: T.f[i] = _read_forced(b, p, fk, path + (i,)); continue
        if gap >= 4 and p % 4 == 0:
            v = U32(b, p); tgt = p + v
            if 0 < v < 8000 and tgt % 4 == 0:
                if _istable(b, tgt): T.set(i, "table", parse_table(b, tgt, path + (i,))); continue
                if tgt + 4 <= len(b):
                    n = U32(b, tgt)
                    if 0 < n < 256 and tgt + 4 + 4 * n <= len(b):
                        elems = []; kinds = set()
                        for j in range(n):
                            q = tgt + 4 + 4 * j; w = U32(b, q); qt = q + w
                            st = _isstr(b, qt) if 0 < w < 8000 else None
                            if st is not None: elems.append(st); kinds.add("str")
                            elif 0 < w < 8000 and _istable(b, qt): elems.append(parse_table(b, qt, path + (i, "*"))); kinds.add("table")
                            else: elems.append(b[q:q + 4]); kinds.add("raw4")
                        if kinds == {"str"}: T.set(i, "vstr", elems); continue
                        if kinds == {"table"}: T.set(i, "vtab", elems); continue
                s = _isstr(b, tgt)
                if s is not None: T.set(i, "str", s); continue
                if tgt + 4 <= len(b) and 0 < U32(b, tgt) < 64 and tgt + 4 + 4 * U32(b, tgt) <= len(b):
                    T.set(i, "vraw4", [b[tgt + 4 + 4 * j:tgt + 8 + 4 * j] for j in range(U32(b, tgt))]); continue
            T.set(i, "raw4", b[p:p + 4]); continue
        if gap == 1 or (gap >= 1 and p % 2 == 1): T.set(i, "raw1", b[p:p + 1]); continue
        if gap >= 2 and p % 2 == 0 and gap < 4: T.set(i, "raw2", b[p:p + 2]); continue
        if gap >= 4: T.set(i, "raw1", b[p:p + 1])   # u8 followed by padding at a 4-aligned slot
        else: T.set(i, "raw1", b[p:p + 1])
    return T

def parse(blob):
    fb = blob[12:]; return parse_table(fb, U32(fb, 0))
def parse_b64(s): return parse(base64.b64decode(s.strip()))

# ---------------------------------------------------------------- builder
class _W:
    def __init__(self): self.buf = bytearray(); self.fix = []
    def align(self, a):
        while len(self.buf) % a: self.buf.append(0)
    def pos(self): return len(self.buf)

def _size(kind):
    return {"raw1": 1, "raw2": 2, "raw4": 4, "str": 4, "table": 4, "vstr": 4, "vtab": 4, "vraw4": 4, "f32": 4, "u32": 4, "i32": 4, "u8": 1}[kind]
def _bytes(kind, v):
    if kind == "raw1": return bytes(v)
    if kind == "raw2": return bytes(v)
    if kind == "raw4": return bytes(v)
    if kind == "f32": return struct.pack("<f", v)
    if kind == "u32": return struct.pack("<I", v)
    if kind == "i32": return struct.pack("<i", v)
    if kind == "u8": return struct.pack("<B", v)
    raise ValueError(kind)

def _write_table(w, T, pending):
    items = sorted(T.f.items())
    nf = (max(i for i, _ in items) + 1) if items else 0
    # inline layout: soffset(4) then 4-byte fields, then 2-byte, then 1-byte
    order = sorted(items, key=lambda kv: -_size(kv[1][0]))
    lay = {}; off = 4
    for i, (k, v) in order:
        s = _size(k)
        while off % s: off += 1
        lay[i] = off; off += s
    tsize = off   # no tail padding: 1-byte fields end exactly at the table end, like flatc's back-to-front layout
    # vtable first (2-aligned), then the table (4-aligned)
    w.align(2)
    vlen = 4 + 2 * nf
    vt = w.pos(); w.buf += struct.pack("<HH", vlen, tsize) + b"".join(struct.pack("<H", lay.get(i, 0)) for i in range(nf))
    w.align(4)
    t = w.pos(); w.buf += bytes(tsize)
    struct.pack_into("<i", w.buf, t, t - vt)
    for i, (k, v) in items:
        p = t + lay[i]
        if k in ("str", "table", "vstr", "vtab", "vraw4"): pending.append((p, k, v))
        else: w.buf[p:p + _size(k)] = _bytes(k, v)
    return t

def _write_obj(w, k, v, pending):
    if k == "str":
        w.align(4); p = w.pos(); data = v.encode("utf-8")
        w.buf += struct.pack("<I", len(data)) + data + b"\x00"; return p
    if k == "table": return _write_table(w, v, pending)
    if k in ("vstr", "vtab", "vraw4"):
        w.align(4); p = w.pos(); w.buf += struct.pack("<I", len(v))
        slots = []
        for e in v:
            q = w.pos(); w.buf += bytes(4); slots.append((q, e))
        for q, e in slots:
            if k == "vraw4": w.buf[q:q + 4] = bytes(e)
            else: pending.append((q, "str" if k == "vstr" else "table", e))
        return p
    raise ValueError(k)

def build_fb(root):
    w = _W(); w.buf += bytes(4)   # root uoffset
    pending = []
    r = _write_table(w, root, pending); struct.pack_into("<I", w.buf, 0, r)
    while pending:
        p, k, v = pending.pop(0)
        q = _write_obj(w, k, v, pending)
        struct.pack_into("<I", w.buf, p, q - p)
    w.align(4)
    return bytes(w.buf)
def build(root):
    fb = build_fb(root)
    return struct.pack("<III", len(fb), 0, 0x11223344) + fb
def build_b64(root): return base64.b64encode(build(root)).decode()

def new_hash(nbytes):
    h = os.urandom(12).hex()
    return "%s-%s-%s-%s-%s%08x" % (h[0:8], h[8:12], h[12:16], h[16:20], h[20:24], nbytes + 12)

def show(T, ind=""):
    for i, (k, v) in sorted(T.f.items()):
        if k == "table": print("%sf%d table" % (ind, i)); show(v, ind + "  ")
        elif k == "vtab":
            print("%sf%d vtab[%d]" % (ind, i, len(v)))
            for j, e in enumerate(v): print("%s  [%d]" % (ind, j)); show(e, ind + "    ")
        elif k in ("raw4",): print("%sf%d raw4 %s (f=%g u=%d)" % (ind, i, bytes(v).hex(), struct.unpack("<f", bytes(v))[0], struct.unpack("<I", bytes(v))[0]))
        else: print("%sf%d %s %r" % (ind, i, k, v if k != "raw1" else bytes(v)[0]))
