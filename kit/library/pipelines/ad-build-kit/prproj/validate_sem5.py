"""semantic reference checks: every reference points at the right kind of object"""
import sys, re, gzip, collections
p = sys.argv[1]
t = gzip.open(p).read().decode('utf-8') if p.endswith('.prproj') else open(p, encoding='utf-8').read()
tags = {m.group(2): m.group(1) for m in re.finditer(r'\n\t<(\w+) ObjectID="(\d+)"', t)}
bad = collections.Counter(); ex = {}
def chk(kind, pat, ok):
    for m in re.finditer(pat, t):
        tag = tags.get(m.group(1))
        if tag is None or not ok(tag, m.group(1)):
            bad[kind] += 1; ex.setdefault(kind, (m.group(1), tag))
masks = set(oid for oid, tg in tags.items() if tg == 'VideoFilterComponent')
chk('subcomponent', r'<SubComponent Index="\d+" ObjectRef="(\d+)"', lambda tg, o: tg == 'VideoFilterComponent' and 'AE.ADBE AEMask2' in t[t.find('ObjectID="%s"' % o):t.find('</VideoFilterComponent>', t.find('ObjectID="%s"' % o))])
chk('component', r'<Component Index="\d+" ObjectRef="(\d+)"', lambda tg, o: tg.endswith('Component'))
chk('param', r'<Param Index="\d+" ObjectRef="(\d+)"', lambda tg, o: tg.endswith('Param'))
chk('trackitem', r'<TrackItem Index="\d+" ObjectRef="(\d+)"', lambda tg, o: tg.endswith('TrackItem'))
chk('subclip', r'<SubClip ObjectRef="(\d+)"', lambda tg, o: tg == 'SubClip')
print('semantic problems:', dict(bad), ex)
