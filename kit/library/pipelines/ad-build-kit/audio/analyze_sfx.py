"""Measure every SFX: format, length, peak dBFS, onset (10 % env) and main peak time, tail, band energy shares, number of separate hits.
Writes sfx_analysis.json"""
import os, sys, json, struct, wave, glob
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
DIR = r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Audio\SFX"


def read_wav(p):
    """int16/24/32 PCM and float32 WAV -> float64 (n, ch), sr"""
    with open(p, 'rb') as f: b = f.read()
    assert b[:4] == b'RIFF' and b[8:12] == b'WAVE', p
    i = 12; fmt = None; data = None
    while i + 8 <= len(b):
        cid = b[i:i + 4]; sz = struct.unpack('<I', b[i + 4:i + 8])[0]; body = b[i + 8:i + 8 + sz]
        if cid == b'fmt ': fmt = struct.unpack('<HHIIHH', body[:16])
        elif cid == b'data': data = body
        i += 8 + sz + (sz & 1)
    tag, ch, sr, _, _, bits = fmt
    if tag == 0xFFFE: tag = 3 if bits == 32 and b'\x03\x00' in b[:200] else 1
    if tag == 3: a = np.frombuffer(data[:len(data) // 4 * 4], dtype='<f4').astype(np.float64)
    elif bits == 16: a = np.frombuffer(data[:len(data) // 2 * 2], dtype='<i2').astype(np.float64) / 32768
    elif bits == 24:
        u = np.frombuffer(data[:len(data) // 3 * 3], dtype=np.uint8).reshape(-1, 3).astype(np.int32)
        v = u[:, 0] | (u[:, 1] << 8) | (u[:, 2] << 16); v = np.where(v >= 1 << 23, v - (1 << 24), v)
        a = v.astype(np.float64) / (1 << 23)
    elif bits == 32: a = np.frombuffer(data[:len(data) // 4 * 4], dtype='<i4').astype(np.float64) / 2 ** 31
    else: raise ValueError(bits)
    return a[:len(a) // ch * ch].reshape(-1, ch), sr, bits, tag


def analyse(p):
    a, sr, bits, tag = read_wav(p)
    m = np.abs(a).max(axis=1)
    k = max(1, int(0.003 * sr)); env = np.convolve(m, np.ones(k) / k, mode='same')
    pk = env.max() + 1e-12
    onset = int(np.argmax(env >= 0.1 * pk)); peak = int(np.argmax(env >= 0.9 * pk))
    after = np.where(env[peak:] > pk * 10 ** (-40 / 20))[0]
    tail = (after[-1] if len(after) else 0) / sr
    mono = a.mean(axis=1)
    seg = mono[max(0, peak - int(0.05 * sr)): peak + int(0.4 * sr)]
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)))) ** 2; f = np.fft.rfftfreq(len(seg), 1 / sr); tot = sp.sum() + 1e-18
    band = lambda lo, hi: float(sp[(f >= lo) & (f < hi)].sum() / tot)
    # separate hits: envelope peaks above -12 dB of max at least 60 ms apart
    e2 = np.convolve(m, np.ones(int(0.01 * sr)) / int(0.01 * sr), mode='same'); thr = e2.max() * 10 ** (-12 / 20)
    hits = []; i = 0
    while i < len(e2):
        if e2[i] >= thr:
            j = i
            while j < len(e2) and e2[j] >= thr * 0.5: j += 1
            hits.append(round((i + int(np.argmax(e2[i:j]))) / sr, 3)); i = j + int(0.06 * sr)
        else: i += 1
    side = a[:, 0] - a[:, 1] if a.shape[1] > 1 else np.zeros(1); mid = a.mean(axis=1)
    width = float(np.sqrt((side ** 2).mean()) / (np.sqrt((mid ** 2).mean()) + 1e-12)) if a.shape[1] > 1 else 0.0
    return dict(file=os.path.basename(p), sr=sr, bits=bits, ch=int(a.shape[1]), dur=round(len(a) / sr, 3), peak_db=round(20 * np.log10(np.abs(a).max() + 1e-12), 1),
                onset=round(onset / sr, 4), peak_t=round(peak / sr, 4), attack_ms=round((peak - onset) / sr * 1000, 1), tail=round(tail, 3),
                sub150=round(band(0, 150), 3), lowmid=round(band(150, 1000), 3), pres=round(band(1000, 4000), 3), air6k=round(band(6000, sr / 2), 3),
                hits=hits[:12], width=round(width, 2))


if __name__ == '__main__':
    rows = [analyse(p) for p in sorted(glob.glob(os.path.join(DIR, '*.wav')))]
    json.dump(rows, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sfx_analysis.json'), 'w'), indent=0)
    print('%-38s %5s %3s %6s %6s %6s %7s %6s | %5s %5s %5s %5s | %s' % ('file', 'sr', 'bit', 'dur', 'peakdB', 'onset', 'peak_t', 'tail', 'sub', 'lmid', 'pres', 'air', 'hits'))
    for r in rows:
        print('%-38s %5d %3d %6.2f %6.1f %6.3f %7.3f %6.2f | %5.2f %5.2f %5.2f %5.2f | %s' % (r['file'][:38], r['sr'], r['bits'], r['dur'], r['peak_db'], r['onset'], r['peak_t'], r['tail'],
              r['sub150'], r['lowmid'], r['pres'], r['air6k'], ' '.join('%.2f' % h for h in r['hits'][:6])))
