"""Per-ad facts for the sound pass: sequence length, code card / title / overlay / B-roll times, A1 dialogue pieces
(source file, in-point, clip gain) and a rebuilt dialogue track (with the clip gains) for loudness + ducking.
Writes ads_info.json and dlg_<key>.npy (mono, 48 kHz)."""
import os, sys, re, json, math
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(HERE, '..', 'prproj'))
import atools as A
from build_project import Doc, TPS, for_claude_sequences, video_tracks
from audio_dump import audio_tracks

SR = 48000
XML = os.path.join(HERE, '..', 'prproj', 'out', 'v7.prproj.xml')


def media_path(doc, sub_raw):
    mc = re.search(r'<MasterClip ObjectURef="([^"]+)"', sub_raw).group(1)
    m = doc.raw(mc, uid=True)
    clip = re.search(r'<Clip Index="\d+" ObjectRef="(\d+)"', m).group(1)
    src = re.search(r'<Source ObjectRef="(\d+)"', doc.raw(clip)).group(1)
    med = re.search(r'<Media ObjectURef="([^"]+)"', doc.raw(src)).group(1)
    return re.search(r'<FilePath>([^<]*)</FilePath>', doc.raw(med, uid=True)).group(1)


def items(doc, tr_uid):
    raw = doc.raw(tr_uid, uid=True)
    m = re.search(r'<ClipItems Version="\d+">\s*<TrackItems Version="1">(.*?)</TrackItems>', raw, re.S)
    out = []
    for tid in (re.findall(r'ObjectRef="(\d+)"', m.group(1)) if m else []):
        t = doc.raw(tid)
        s = int(re.search(r'<Start>(-?\d+)</Start>', t).group(1)) / TPS if '<Start>' in t else 0.0
        e = int(re.search(r'<End>(-?\d+)</End>', t).group(1)) / TPS
        sub = re.search(r'<SubClip ObjectRef="(\d+)"', t)
        name, tin, gain, path = '?', 0.0, 0.0, None
        if sub:
            st = doc.raw(sub.group(1)); n = re.search(r'<Name>([^<]*)</Name>', st); name = n.group(1) if n else '?'
            c = re.search(r'<Clip ObjectRef="(\d+)"', st)
            if c:
                ct = doc.raw(c.group(1))
                ip = re.search(r'<InPoint>(-?\d+)</InPoint>', ct); tin = int(ip.group(1)) / TPS if ip else 0.0
                g = re.search(r'<Gain>([^<]*)</Gain>', ct); gain = 20 * math.log10(float(g.group(1))) if g else 0.0
            try: path = media_path(doc, st)
            except Exception: path = None
        out.append(dict(start=round(s, 4), end=round(e, 4), name=name, tin=round(tin, 4), gain=round(gain, 2), path=path, muted='<IsMuted>true</IsMuted>' in t))
    return out


def info():
    doc = Doc(XML); ads = {}
    for n, seq in for_claude_sequences(doc):
        key = seq.attrib['ObjectUID'][:8]
        vts = video_tracks(doc, seq)
        vid = [items(doc, t.attrib['ObjectUID']) for t in vts]
        g, ats = audio_tracks(doc, seq)
        a1 = [i for i in items(doc, ats[0].attrib['ObjectUID']) if not i['muted']]
        L = max(i['end'] for i in vid[0])
        ov = []
        for k, tr in enumerate(vid[1:], start=2):
            for i in tr:
                if i['muted'] or i['name'].startswith('Adjustment Layer'): continue
                ov.append(dict(track=k, start=i['start'], end=i['end'], name=i['name'], tin=i['tin']))
        code = [o['start'] for o in ov if o['name'].startswith('Code')]
        ads[key] = dict(name=n, L=round(L, 4), n_audio=len(ats), code=code[0] if code else None, overlays=sorted(ov, key=lambda o: o['start']), a1=a1)
    json.dump(ads, open(os.path.join(HERE, 'ads_info.json'), 'w'), indent=1)
    return ads


def dialogue(key, ad):
    out = np.zeros(int(ad['L'] * SR) + SR)
    by_src = {}
    for p in ad['a1']: by_src.setdefault(p['path'], []).append(p)
    for path, ps in by_src.items():
        rng = sorted((p['tin'], p['tin'] + p['end'] - p['start']) for p in ps)
        chunks = []
        for a, b in rng:
            if chunks and a - chunks[-1][1] < 8: chunks[-1][1] = max(chunks[-1][1], b)
            else: chunks.append([a, b])
        cache = []
        for ci, (a, b) in enumerate(chunks):
            fn = os.path.join(HERE, 'dlgsrc', '%s_%s_%02d.wav' % (key, re.sub(r'\W', '', os.path.basename(path))[:20], ci))
            os.makedirs(os.path.dirname(fn), exist_ok=True)
            if not os.path.exists(fn): A.extract_wav(path, fn, max(0, a - 0.5), b + 0.5)
            x, sr = A.load_wav(fn); cache.append((max(0, a - 0.5), x.mean(axis=1)))
        for p in ps:
            c0, x = [c for c, (a, b) in zip(cache, chunks) if a - 1e-6 <= p['tin'] <= b + 1e-6][0]
            i0 = int(round((p['tin'] - c0) * SR)); n = int(round((p['end'] - p['start']) * SR))
            seg = x[i0:i0 + n] * 10 ** (p['gain'] / 20)
            j = int(round(p['start'] * SR)); out[j:j + len(seg)] = seg[:len(out) - j]
    out = out[:int(ad['L'] * SR)]
    np.save(os.path.join(HERE, 'dlg_%s.npy' % key), out.astype(np.float32))
    return out


if __name__ == '__main__':
    ads = info()
    for key, ad in ads.items():
        d = dialogue(key, ad)
        st = d[:, None]
        print('%s %-24s L %6.2f code %s  A1 %d clips gains %s  voice %.1f LUFS  peak %.1f dBTP' % (
            key, ad['name'][:24], ad['L'], ad['code'], len(ad['a1']), sorted(set(p['gain'] for p in ad['a1'])), A.lufs(st, SR), A.true_peak_db(st)))
