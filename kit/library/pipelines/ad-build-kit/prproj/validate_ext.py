"""Semantic checks: new project vs the Premiere-saved B-roll project it was built from."""
import sys, json, re, os, subprocess
sys.path.insert(0, '.')
sys.path.insert(0, '../work')
import ext_plan
from build_project import TPS

F60 = 4233600000
REF = '348e0ba6'
old = json.load(open(sys.argv[1])); new = json.load(open(sys.argv[2]))
ok = True


def fail(*a):
    global ok
    ok = False
    print('  FAIL', *a)


def norm(o):
    if isinstance(o, dict): return {k: norm(v) for k, v in o.items() if k != 'src'}
    if isinstance(o, list): return [norm(x) for x in o]
    return o


for key in old:
    O, N = old[key], new[key]
    print('==', key, O['name'][:40])
    for f in ('captions', 'audio', 'ntracks', 'nexttrack'):
        if O[f] != N[f]: fail(f, 'changed')
    btrack, gtrack = (4, 5) if key == REF else (2, 3)
    od = [d for d in O['detail']]; nd = [d for d in N['detail']]
    by = lambda D, t: [norm(d) for d in D if d['track'] == t]
    # every track except B-roll and grade must be identical
    for t in range(1, O['ntracks'] + 1):
        if t in (btrack, gtrack): continue
        if by(od, t) != by(nd, t): fail('track V%d changed' % t)
    adds = ext_plan.ADD.get(key, [])
    if not adds:
        if by(od, btrack) != by(nd, btrack) or by(od, gtrack) != by(nd, gtrack): fail('untouched ad changed')
        else: print('  untouched ad identical')
        continue
    # B-roll: all old shots still there, unchanged
    ob, nb = by(od, btrack), by(nd, btrack)
    missing = [d for d in ob if d not in nb]
    if missing: fail('old B-roll changed or missing:', [(m['name'], m['start'] / TPS) for m in missing])
    extra = [d for d in nb if d not in ob]
    exp = sorted(adds, key=lambda d: d['t0'])
    if len(extra) != len(exp): fail('expected %d new shots, got %d' % (len(exp), len(extra)))
    for d, it in zip(sorted(extra, key=lambda d: d['start']), exp):
        media = ntpath = os.path.basename(ext_plan.MEDIA[it['media']].replace('\\', '/'))
        if d['name'] != media: fail('media', d['name'], media)
        if abs(d['start'] / TPS - it['t0']) > 0.01 or abs(d['end'] / TPS - it['t1']) > 0.01: fail('times', d['start'] / TPS, d['end'] / TPS, it)
        if abs(d['in'] / TPS - it['src']) > 0.03: fail('source in', d['in'] / TPS, it['src'])
        if (d['out'] - d['in']) != (d['end'] - d['start']): fail('duration mismatch', d)
        fx = {f[0]: f for f in d['fx']}
        mot = fx['Motion'][1]; lum = fx['Lumetri'][1]
        if abs(float(mot['Scale']) - it['scale']) > 1e-3: fail('scale', mot['Scale'], it['scale'])
        print('  + %-16s %6.3f-%6.3f src %7.3f  pos %-22s scale %-9s  Lumetri T%s S%s E%s Tint%s Sh%s Vib%s Con%s Vig%s'
              % (it['media'], d['start'] / TPS, d['end'] / TPS, d['in'] / TPS, mot['Position'], mot['Scale'],
                 lum['14'], lum['16'], lum['19'], lum['15'], lum['41'], lum['42'], lum['20'], lum['110']))
    # grade: pieces tile [0, end) minus B-roll, media offset 3600 s, Lumetri untouched per original item
    ends = [d['end'] for d in nd if d['track'] == 1]
    seq_end = max(ends)
    bint = sorted((d['start'], d['end']) for d in nd if d['track'] == btrack)
    for (a1, b1), (a2, b2) in zip(bint, bint[1:]):
        if b1 > a2: fail('B-roll overlap', a1 / TPS, b1 / TPS, a2 / TPS)
    gp = sorted((d['start'], d['end'], d['in'], json.dumps(d['fx'])) for d in nd if d['track'] == gtrack)
    covered = sorted([(a, b) for a, b in bint] + [(s, e) for s, e, _, _ in gp])
    t = 0
    for a, b in covered:
        if a != t: fail('gap/overlap at %.4f (next starts %.4f)' % (t / TPS, a / TPS))
        t = b
    if t != seq_end: fail('timeline not fully covered: ends %.4f of %.4f' % (t / TPS, seq_end / TPS))
    for s, e, i, fx in gp:
        if i - s != 3600 * TPS: fail('grade media offset', (i - s) / TPS)
    old_sigs = {json.dumps(d['fx']) for d in od if d['track'] == gtrack}
    for s, e, i, fx in gp:
        if fx not in old_sigs: fail('grade effect values changed at %.3f' % (s / TPS))
    if key == REF:
        for s, e, i, fx in gp:
            exp_exp = '1.' if e <= 17.05 * TPS + 1 else '0.699999988079071044921875'
            main = [f for f in json.loads(fx) if f[0] == 'Lumetri' and not f[3]][0]
            if main[1]['19'] != exp_exp: fail('reference grade exposure wrong at %.3f: %s' % (s / TPS, main[1]['19']))
    cover = sum(b - a for a, b in bint) / seq_end
    print('  B-roll %d shots, %.1f%% of %.2fs | grade %d pieces | old B-roll kept: %s' % (len(bint), cover * 100, seq_end / TPS, len(gp), not missing))
print('\nALL CHECKS PASSED' if ok else '\nSOME CHECKS FAILED')
