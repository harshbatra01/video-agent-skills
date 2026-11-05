"""Premiere transcript decoder (TranscriptData FlatBuffers blobs in a .prproj).
Word table layout: [soffset vtable][uoffset -> string][float32 confidence][int64 start ticks][int64 duration ticks]
(+ optional 4-byte pad) [uint32 len][utf8 text]. Decoding via the uoffset makes the pad irrelevant.
usage: python prtranscript.py project.prproj [out.json]   -> prints per-transcript word counts + owning media"""
import gzip, re, base64, struct, sys, json
TPS = 254016000000

def decode_words(b):
    out, seen = [], set()
    for p in range(4, len(b) - 20):
        conf = struct.unpack_from('<f', b, p)[0]
        if not (0.0 <= conf <= 1.0) or b[p + 3] not in (0x3f, 0x3e, 0x3d, 0x3c, 0x3b, 0x00):
            continue
        off = struct.unpack_from('<I', b, p - 4)[0]
        if not 16 <= off <= 40:
            continue
        sp = p - 4 + off
        if sp + 4 > len(b):
            continue
        n = struct.unpack_from('<I', b, sp)[0]
        if not 1 <= n <= 64 or sp + 4 + n > len(b):
            continue
        st, du = struct.unpack_from('<qq', b, p + 4)
        if not (0 <= st < 10 ** 17 and 0 < du < 30 * TPS):
            continue
        try:
            w = b[sp + 4:sp + 4 + n].decode('utf-8')
        except UnicodeDecodeError:
            continue
        if not w.isprintable() or ' ' in w or sp in seen:
            continue
        seen.add(sp)
        out.append({'t': round(st / TPS, 3), 'd': round(du / TPS, 3), 'w': w, 'c': round(conf, 3)})
    return sorted(out, key=lambda x: x['t'])

def project_transcripts(path):
    t = gzip.open(path, 'rb').read().decode('utf-8')
    res = []
    for m in re.finditer(r'<(\w+) ObjectID="(\d+)"[^>]*>(?:(?!</\1>).)*?<TranscriptData([^>]*)>([^<]*)</TranscriptData>', t, re.S):
        oid, attrs, data = m.group(2), m.group(3), m.group(4)
        b = base64.b64decode(data) if 'base64' in attrs else b''
        # who points at this transcript object -> nearest media title
        ref = re.search(r'ObjectRef="%s"' % oid, t)
        title = None
        if ref:
            back = t[max(0, ref.start() - 6000):ref.start()]
            tt = re.findall(r'<Title>([^<]+)</Title>', back) or re.findall(r'<Name>([^<]+)</Name>', back)
            title = tt[-1] if tt else None
        res.append({'object': oid, 'near_title': title, 'bytes': len(b), 'lang': (re.findall(rb'[a-z]{2,3}-[a-z]{2}', b[:200]) or [b'?'])[0].decode(), 'words': decode_words(b)})
    return res

if __name__ == '__main__':
    tr = project_transcripts(sys.argv[1])
    for r in tr:
        ws = r['words']
        print('obj %s lang %s bytes %d words %d %s | near %s' % (r['object'], r['lang'], r['bytes'], len(ws), ('%.1f-%.1f s' % (ws[0]['t'], ws[-1]['t'])) if ws else '', r['near_title']))
    if len(sys.argv) > 2:
        json.dump(tr, open(sys.argv[2], 'w', encoding='utf-8'), indent=0)
