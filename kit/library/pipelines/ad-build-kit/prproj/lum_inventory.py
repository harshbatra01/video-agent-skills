"""Every Lumetri on every video track item of the 'For claude' ads: ad, track, times, name, muted, key sliders.
usage: python lum_inventory.py project.xml [out.json]"""
import sys, re, json
sys.path.insert(0, '.')
from build_project import Doc, TPS, for_claude_sequences, video_tracks, track_items
from build_v3 import lumetri_ids, item_name
from build_ext import item_times
IDX = {14: 'temp', 15: 'tint', 16: 'sat', 19: 'exp', 20: 'con', 21: 'hil', 22: 'sha', 23: 'whi', 24: 'blk', 42: 'vib'}
doc = Doc(sys.argv[1])
rows = []
for n, s in for_claude_sequences(doc):
    key = s.attrib['ObjectUID'][:8]
    for k, tr in enumerate(video_tracks(doc, s)):
        for it in track_items(doc, tr):
            i = it.attrib['ObjectID']
            try: st, en, _, _ = item_times(doc, i)
            except Exception: continue
            lum = lumetri_ids(doc, i)
            if not lum: continue
            muted = '<IsMuted>true</IsMuted>' in doc.raw(i)
            for ci, c in enumerate(lum):
                ct = doc.raw(c); vals = {}
                for idx, nm in IDX.items():
                    m = re.search(r'<Param Index="%d" ObjectRef="(\d+)"' % idx, ct)
                    if not m: continue
                    p = doc.raw(m.group(1)); v = re.search(r'<StartKeyframe>-?\d+,([^,]+),', p)
                    vals[nm] = (float(v.group(1)) if v else None, '<Keyframes>' in p and bool(re.search(r'<Keyframes>[^<]', p)))
                rows.append(dict(ad=key, adname=s.findtext('Name'), track=k + 1, start=round(st / TPS, 3), end=round(en / TPS, 3), item=i, comp=c, ci=ci,
                                 name=item_name(doc, i), muted=muted, vals={k2: v[0] for k2, v in vals.items()}, kf=[k2 for k2, v in vals.items() if v[1]]))
for r in rows:
    v = r['vals']
    print('%s V%d %6.2f-%6.2f %s%-24s c%d  ' % (r['ad'], r['track'], r['start'], r['end'], 'OFF ' if r['muted'] else '', r['name'][:24], r['ci']) +
          ' '.join('%s=%s' % (k, ('%.1f' % v[k]) if v.get(k) is not None else '-') for k in ('temp', 'tint', 'exp', 'con', 'hil', 'sha', 'whi', 'blk', 'sat', 'vib')) +
          ('  KF:' + ','.join(r['kf']) if r['kf'] else ''))
if len(sys.argv) > 2: json.dump(rows, open(sys.argv[2], 'w'), indent=1)
print(len(rows), 'lumetri instances')
