"""Word timings of the CTA voice from the project's transcript blobs (any blob whose words include 'discount')."""
import gzip, re, base64, struct, json, sys
TPS = 254016000000
src = sys.argv[1]
t = gzip.open(src, 'rb').read().decode('utf-8') if src.endswith('.prproj') else open(src, encoding='utf-8').read()


def decode_words(b):
    words = []; i = 0
    while i + 24 < len(b):
        if b[i:i + 4] == b'\x00\x00\x80\x3f' or (b[i + 3] in (0x3f, 0x3e) and 0.0 <= struct.unpack_from('<f', b, i)[0] <= 1.0):
            conf = struct.unpack_from('<f', b, i)[0]
            st, du = struct.unpack_from('<qq', b, i + 4)
            n = struct.unpack_from('<I', b, i + 20)[0]
            if 0 <= st < 10 ** 17 and 0 < du < 10 ** 14 and 1 <= n <= 40 and i + 24 + n <= len(b):
                try:
                    w = b[i + 24:i + 24 + n].decode('utf-8')
                    if w.isprintable():
                        words.append((st / TPS, du / TPS, w, round(conf, 2))); i += 24 + n; continue
                except UnicodeDecodeError: pass
        i += 1
    return sorted(words)


found = []
for m in re.finditer(r'<TranscriptData[^>]*Encoding="base64"[^>]*>([^<]+)</TranscriptData>', t):
    try: b = base64.b64decode(m.group(1))
    except Exception: continue
    ws = decode_words(b)
    if any('discount' in w[2].lower() for w in ws): found.append(ws)
for ws in found:
    print(' '.join('%s@%.2f+%.2f' % (w[2], w[0], w[1]) for w in ws))
if found: json.dump(found[0], open('cta_words.json', 'w'))
print(len(found), 'transcript(s) with the CTA')
