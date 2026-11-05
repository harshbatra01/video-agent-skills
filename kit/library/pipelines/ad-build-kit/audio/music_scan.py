"""Download Epidemic preview MP3s (public lq previews), decode with VLC, and print a compact structure map per track:
per-bar loudness digits, voice-band share (masking risk), low-end share, key guess, ending type."""
import os, sys, json, urllib.request
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atools as A

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'music_prev'); os.makedirs(OUT, exist_ok=True)
SR = 22050
NAMES = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
MAJ = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
MIN = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def fetch(key, url):
    mp3 = os.path.join(OUT, key + '.mp3'); wav = os.path.join(OUT, key + '.wav')
    if not os.path.exists(mp3): urllib.request.urlretrieve(url, mp3)
    if not os.path.exists(wav): A.extract_wav(mp3, wav, sr=SR)
    x, sr = A.load_wav(wav)
    return x.mean(axis=1), sr


def band_share(seg, sr, lo, hi):
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2; f = np.fft.rfftfreq(len(seg), 1 / sr)
    return float(sp[(f >= lo) & (f < hi)].sum() / (sp.sum() + 1e-18))


def key_guess(x, sr):
    n = 8192; hop = 4096; chroma = np.zeros(12)
    f = np.fft.rfftfreq(n, 1 / sr); ok = (f > 60) & (f < 2000)
    pc = (np.round(12 * np.log2(f[ok] / 261.63)) % 12).astype(int)
    for i in range(0, len(x) - n, hop * 4):
        s = np.abs(np.fft.rfft(x[i:i + n] * np.hanning(n)))[ok]
        chroma += np.bincount(pc, weights=s, minlength=12)
    best = []
    for r in range(12):
        c = np.roll(chroma, -r)
        best.append((np.corrcoef(c, MAJ)[0, 1], NAMES[r] + ' major')); best.append((np.corrcoef(c, MIN)[0, 1], NAMES[r] + ' minor'))
    best.sort(reverse=True)
    return best[0][1], round(best[0][0], 2), best[1][1]


def scan(key, url, bpm):
    x, sr = fetch(key, url)
    dur = len(x) / sr; bar = 4 * 60.0 / bpm
    nb = int(dur / bar)
    rms = np.array([np.sqrt(np.mean(x[int(i * bar * sr):int((i + 1) * bar * sr)] ** 2)) + 1e-9 for i in range(nb)])
    db = 20 * np.log10(rms); top = db.max()
    digits = ''.join(str(int(np.clip((d - top + 30) / 3, 0, 9))) for d in db)
    # voice band share over the loud part of the track
    mid = x[int(0.3 * len(x)):int(0.3 * len(x)) + 20 * sr]
    vshare = band_share(mid, sr, 300, 3000); low = band_share(mid, sr, 0, 150)
    # ending: last 10 s envelope, find last strong onset and what follows
    tail = x[-10 * sr:]; env = np.convolve(np.abs(tail), np.ones(int(0.02 * sr)) / int(0.02 * sr), mode='same')
    env_db = 20 * np.log10(env + 1e-9)
    d = np.diff(env_db[::int(0.01 * sr)])
    jumps = np.where(d > 6)[0]
    last_hit = round(dur - 10 + jumps[-1] * 0.01, 2) if len(jumps) else None
    end_db = round(env_db[-int(0.3 * sr):].mean() - env_db.max(), 1)
    k = key_guess(x, sr)
    return dict(key=key, dur=round(dur, 1), bpm=bpm, bar=round(bar, 3), map=digits, voice=round(vshare, 2), low=round(low, 2),
                last_hit=last_hit, end_db=end_db, tonality=k)


if __name__ == '__main__':
    cf = sys.argv[1] if len(sys.argv) > 1 else 'music_cands.json'
    cands = json.load(open(os.path.join(HERE, cf)))
    rows = []
    for c in cands:
        try:
            r = scan(c['key'], c['url'], c['bpm']); r['title'] = c['title']; rows.append(r)
            print('%-22s %5.1fs %3d bpm bar %.2fs  key %-9s(%.2f)  voice %.2f low %.2f  last hit %s end %s dB' % (
                c['title'][:22], r['dur'], r['bpm'], r['bar'], r['tonality'][0], r['tonality'][1], r['voice'], r['low'], r['last_hit'], r['end_db']))
            print('   bars: ' + r['map'])
        except Exception as e:
            print(c['title'], 'ERR', e)
    json.dump(rows, open(os.path.join(HERE, cf.replace('cands', 'scan')), 'w'), indent=1)
