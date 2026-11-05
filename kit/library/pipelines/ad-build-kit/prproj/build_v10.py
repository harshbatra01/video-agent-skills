"""v10 = the user's v9 save (09:13, the source of the V3 renders) + a colour pass on every ad:
more contrast, shadows down, highlights up a touch, a pinch of saturation.
  - A-roll grade layers: per look (sofa / park / river). River ads also get their haze cleared (blacks + shadows down hard),
    the mint cast on the white T-shirt eased (tint toward neutral, a touch warmer) and only a small highlight lift (shirt + sky
    sit near clipping).
  - Camera B-roll (A003_*) with a known look gets that look's pass; other camera B-roll a light pass.
  - Untouched: face-light Lumetris, the 3 things board spotlight (keyframed), archive + stock clips, muted items."""
import sys, re, json, gzip
sys.path.insert(0, '.')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, track_items
from build_v3 import lumetri_ids, item_name
from build_ext import item_times
from build_v9 import edit_param

SRC = 'v10src.xml'
OUT_XML = 'out/v10.prproj.xml'
OUT = r"C:\VISION\IMMUFIX\ads immufix - Claude zooms + titles v10.prproj"
IDX = {'temp': 14, 'tint': 15, 'sat': 16, 'exp': 19, 'con': 20, 'hil': 21, 'sha': 22, 'whi': 23, 'blk': 24, 'vib': 42}
RANGE = {'sat': (0, 200)}
SOFA, PARK, RIVER = {'348e0ba6', 'cd03e189', '664b35b2'}, {'404c5cb2', 'f233433f'}, {'0991faf2', '974102f7', '593f11c4'}
D_SOFA = dict(con=16, hil=14, sha=-14, blk=-8, sat=3, vib=6)        # pass 2: vibrance instead of most of the saturation (skin was going orange)
D_PARK = dict(con=18, hil=12, sha=-14, blk=-12, sat=3, vib=6, tint=6)  # pass 2: + mint cast off the white T-shirt
D_LIGHT = dict(con=4, hil=6, sat=3)


def d_river(v):
    d = dict(hil=4, sha=-20, blk=-30, sat=5, vib=6, tint=6)          # pass 2: the haze needs a much lower black point
    if v['con'] < 40: d['con'] = 26           # 3 questions; the two ads the user already pushed to 65 keep it
    if v['temp'] < 6: d['temp'] = 2
    return d


def look(v):
    if abs(v['hil'] + 21.9) < 0.05 and abs(v['sha'] - 22.7) < 0.05 and abs(v['blk'] + 25.9) < 0.05: return 'ref'
    if abs(v['tint'] + 15) < 0.05 and abs(v['blk'] + 38) < 0.05 and abs(v['sha'] - 14) < 0.05: return 'river'
    if abs(v['tint'] + 18) < 0.05 and abs(v['blk'] + 38) < 0.05: return 'river'          # 3 questions after 35 s
    if abs(v['sha'] - 18) < 0.05 and abs(v['blk'] + 32) < 0.05: return 'park'
    if abs(v['sha'] - 15) < 0.05 and abs(v['blk'] + 36) < 0.05: return 'sofa2'          # People surprised A-roll
    return 'other'


def main():
    doc = Doc(SRC)
    log, done, pdone = [], set(), set()
    for n, s in for_claude_sequences(doc):
        ad = s.attrib['ObjectUID'][:8]
        for k, tr in enumerate(video_tracks(doc, s)):
            for it in track_items(doc, tr):
                i = it.attrib['ObjectID']
                if '<IsMuted>true</IsMuted>' in doc.raw(i): continue
                try: st, en, _, _ = item_times(doc, i)
                except Exception: continue
                lum = lumetri_ids(doc, i)
                if not lum: continue
                name = item_name(doc, i)
                for c in lum:
                    if c in done: continue
                    ct = doc.raw(c); pid, v, kf = {}, {}, False
                    for nm, idx in IDX.items():
                        m = re.search(r'<Param Index="%d" ObjectRef="(\d+)"' % idx, ct)
                        if not m: continue
                        pid[nm] = m.group(1); p = doc.raw(pid[nm])
                        mv = re.search(r'<StartKeyframe>-?\d+,([^,]+),', p); v[nm] = float(mv.group(1)) if mv else 0.0
                        if re.search(r'<Keyframes>[^<]', p): kf = True
                    if len(v) < len(IDX) or kf: continue
                    if v['con'] == 0 and v['hil'] == 0 and v['sha'] == 0 and v['blk'] == 0 and abs(v['exp'] - 0.5) < 0.01: continue   # face light
                    lk = look(v); grade = name.startswith('Adjustment Layer'); cam = name.startswith('A003_')
                    if not (grade or cam): continue                                                     # archive / stock
                    if lk == 'river': d = d_river(v)
                    elif lk in ('ref', 'sofa2'): d = D_PARK if (ad in PARK and grade) else D_SOFA
                    elif lk == 'park': d = D_PARK
                    elif grade:
                        log.append('SKIP unknown grade look %s %s %.2f %s' % (ad, name, st / TPS, v)); continue
                    else: d = D_LIGHT
                    if any(pid[nm] in pdone for nm in d):
                        log.append('SKIP shared params %s %s %.2f' % (ad, name, st / TPS)); continue
                    for nm, dv in d.items():
                        lo, hi = RANGE.get(nm, (-100, 100)); nv = max(lo, min(hi, v[nm] + dv))
                        edit_param(doc, pid[nm], lambda s0, nv=nv: fmt(nv)); pdone.add(pid[nm])
                    done.add(c)
                    log.append('%s V%d %6.2f %-26s %-6s %s' % (ad, k + 1, st / TPS, name[:26], lk, ' '.join('%s %+g' % kv for kv in d.items())))
    txt = doc.text() if hasattr(doc, 'text') else doc.txt
    open(OUT_XML, 'w', encoding='utf-8').write(txt)
    with gzip.open(OUT, 'wb') as f: f.write(txt.encode('utf-8'))
    for l in log: print(l)
    print('edited %d Lumetri instances -> %s' % (len(done), OUT))


if __name__ == '__main__':
    main()
