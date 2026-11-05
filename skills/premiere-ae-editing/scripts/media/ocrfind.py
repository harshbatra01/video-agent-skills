"""Find a phrase in OCR'd screenshots -> one highlight rect per text line [x, y, w, h] in image px.
Use it to put highlighters / boxes / zooms exactly on the words the voice reads (article screenshots, product pages).

step 1 (Windows built-in OCR, no install):  powershell -File ocr.ps1 ocr.json shot1.png shot2.png ...
step 2:  python ocrfind.py ocr.json shot1.png "the exact phrase"     or in Python:
         from ocrfind import find; r = find('ocr.json', 'shot1.png', 'the exact phrase')  -> {'rects', 'score', 'of', 'text'}
Matching is fuzzy per word (OCR misreads); check r['score'] == r['of'] and look at the rects on a sheet once.
"""
# macOS step 1 (from the Mac port, Oct 2026): Apple Vision OCR writes the same ocr.json shape, so step 2 is unchanged:
#   swiftc -O scripts/media/ocr.swift -o scripts/media/ocr      (once; needs the Xcode Command Line Tools)
#   scripts/media/ocr ocr.json shot1.png shot2.png ...
import json, re, os, sys
_C = {}


def _load(ocr_json):
    if ocr_json not in _C: _C[ocr_json] = json.load(open(ocr_json, encoding='utf-8-sig'))
    return _C[ocr_json]


def _n(s): return re.sub(r'[^a-z0-9$%.]', '', s.lower())


def words(ocr_json, img):
    out = []
    lines = _load(ocr_json)[os.path.basename(img)]
    if isinstance(lines, dict): lines = [lines]
    for li, line in enumerate(lines):
        ws = line['words']
        if ws and not isinstance(ws[0], list): ws = [ws]
        for w in ws: out.append((li, w[0], float(w[1]), float(w[2]), float(w[3]), float(w[4])))
    return out


def find(ocr_json, img, phrase, pad=(6, 4)):
    ws = words(ocr_json, img)
    target = [_n(t) for t in phrase.split() if _n(t)]
    toks = [_n(w[1]) for w in ws]
    best = None
    for i in range(len(ws)):
        k = 0; j = i; score = 0
        while k < len(target) and j < len(ws):
            if not toks[j]: j += 1; continue
            if toks[j] == target[k] or (len(target[k]) > 3 and (toks[j].startswith(target[k][:4]) or target[k].startswith(toks[j][:4]))): score += 1
            k += 1; j += 1
        if best is None or score > best[0]: best = (score, i, j)
    score, i, j = best
    rects = {}
    for (li, t, x, y, w, h) in ws[i:j]:
        r = rects.setdefault(li, [x, y, x + w, y + h])
        r[0] = min(r[0], x); r[1] = min(r[1], y); r[2] = max(r[2], x + w); r[3] = max(r[3], y + h)
    out = [[round(r[0] - pad[0], 1), round(r[1] - pad[1], 1), round(r[2] - r[0] + 2 * pad[0], 1), round(r[3] - r[1] + 2 * pad[1], 1)] for li, r in sorted(rects.items())]
    return dict(rects=out, score=score, of=len(target), text=' '.join(w[1] for w in ws[i:j]))


if __name__ == '__main__':
    if len(sys.argv) < 4: sys.exit(__doc__)
    print(find(sys.argv[1], sys.argv[2], sys.argv[3]))
