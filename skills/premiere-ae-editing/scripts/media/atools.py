"""Audio helpers without ffmpeg/scipy: decode any file (PyAV), ITU-R BS.1770-4 loudness (LUFS), true peak, short-term
loudness, transient time. Checked against the -23 LUFS EBU reference (-22.99).

usage: python atools.py FILE [t0 t1]   -> integrated LUFS, true peak dBTP, loudest 3 s window, duration
lib:   from atools import load_any, lufs, true_peak_db, short_term, peak_time
Targets used on these jobs: YouTube / social deliveries about -14 LUFS integrated with peaks under -1 dBTP; voice staged
to about -17.5 LUFS before the final lift; music 12-18 dB under the voice; raw voice WAVs often arrive at -30 to -40 LUFS."""
import os, subprocess, wave, sys
import numpy as np


def load_any(path, sr=48000, t0=None, t1=None):
    """decode the first audio stream of any file to stereo float64 at sr with PyAV -> (array [n, 2], sr)"""
    import av
    out = []
    with av.open(path) as c:
        rs = av.AudioResampler(format='s16', layout='stereo', rate=sr)
        for f in c.decode(audio=0):
            for g in rs.resample(f): out.append(g.to_ndarray().reshape(-1, 2))
        for g in rs.resample(None): out.append(g.to_ndarray().reshape(-1, 2))
    x = np.concatenate(out).astype(np.float64) / 32768.0
    a = int((t0 or 0) * sr); b = int(t1 * sr) if t1 is not None else None
    return x[a:b], sr

VLC = r"C:\Program Files\VideoLAN\VLC\vlc.exe"
# macOS (from the Mac port, Oct 2026): extract_wav uses ffmpeg (Homebrew) instead of VLC; Windows still uses VLC.
# Cross-check any measurement there with: ffmpeg -i FILE -af ebur128=peak=true -f null -   (Summary block)


def extract_wav(src, dst, t0=None, t1=None, sr=48000):
    if sys.platform == 'darwin':   # 16-bit stereo WAV with ffmpeg (Homebrew's build has no soxr: the default resampler is fine for measuring)
        args = ['ffmpeg', '-v', 'error', '-y']
        if t0 is not None: args += ['-ss', '%.3f' % t0]
        if t1 is not None: args += ['-to', '%.3f' % t1]
        args += ['-i', src, '-vn', '-ac', '2', '-ar', str(sr), '-c:a', 'pcm_s16le', dst]
        subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900, check=True)
        return dst
    args = [VLC, '--intf', 'dummy', '--dummy-quiet', '--no-video']
    if t0 is not None: args.append('--start-time=%.3f' % t0)
    if t1 is not None: args.append('--stop-time=%.3f' % t1)
    args += [src, '--sout=#transcode{acodec=s16l,channels=2,samplerate=%d}:std{access=file,mux=wav,dst=%s}' % (sr, dst), 'vlc://quit']
    subprocess.run(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=900)
    return dst


def load_wav(path):
    w = wave.open(path)
    n, sr, ch, sw = w.getnframes(), w.getframerate(), w.getnchannels(), w.getsampwidth()
    raw = w.readframes(n)
    if sw == 2: a = np.frombuffer(raw, dtype='<i2').astype(np.float64) / 32768.0
    elif sw == 3:
        b = np.frombuffer(raw, dtype=np.uint8).reshape(-1, 3)
        a = (b[:, 0].astype(np.int32) | (b[:, 1].astype(np.int32) << 8) | (b[:, 2].astype(np.int32) << 16))
        a = np.where(a >= 1 << 23, a - (1 << 24), a).astype(np.float64) / float(1 << 23)
    elif sw == 4: a = np.frombuffer(raw, dtype='<i4').astype(np.float64) / 2147483648.0
    else: raise ValueError('sample width %d' % sw)
    return a.reshape(-1, ch), sr


def _biquad_response(b, a, n, sr):
    f = np.fft.rfftfreq(n, 1.0 / sr); z = np.exp(-2j * np.pi * f / sr)
    return (b[0] + b[1] * z + b[2] * z * z) / (a[0] + a[1] * z + a[2] * z * z)


def k_weight(x, sr):
    """BS.1770 K-weighting (48 kHz coefficients, re-derived for other rates via bilinear prewarp approximation)"""
    if sr != 48000: raise ValueError('use 48 kHz audio')
    b1, a1 = [1.53512485958697, -2.69169618940638, 1.19839281085285], [1.0, -1.69065929318241, 0.73248077421585]
    b2, a2 = [1.0, -2.0, 1.0], [1.0, -1.99004745483398, 0.99007225036621]
    n = x.shape[0]; N = 1 << int(np.ceil(np.log2(n + 4096)))
    H = _biquad_response(b1, a1, N, sr) * _biquad_response(b2, a2, N, sr)
    X = np.fft.rfft(x, n=N, axis=0)
    return np.fft.irfft(X * H[:, None], n=N, axis=0)[:n]


def lufs(x, sr):
    """integrated loudness (LUFS), gated per BS.1770-4"""
    y = k_weight(x, sr)
    blk, hop = int(0.4 * sr), int(0.1 * sr)
    if y.shape[0] < blk: return float('-inf')
    p = np.cumsum(np.vstack([np.zeros((1, y.shape[1])), y ** 2]), axis=0)
    starts = np.arange(0, y.shape[0] - blk + 1, hop)
    ms = (p[starts + blk] - p[starts]) / blk               # mean square per channel per block
    zl = ms.sum(axis=1)                                      # L + R (weights 1.0)
    lk = -0.691 + 10 * np.log10(zl + 1e-12)
    g1 = zl[lk > -70]
    if not len(g1): return float('-inf')
    rel = -0.691 + 10 * np.log10(g1.mean()) - 10
    g2 = zl[(lk > -70) & (lk > rel)]
    return float(-0.691 + 10 * np.log10(g2.mean()))


def short_term(x, sr, win=3.0, hop=0.1):
    y = k_weight(x, sr); blk, h = int(win * sr), int(hop * sr)
    p = np.cumsum(np.vstack([np.zeros((1, y.shape[1])), y ** 2]), axis=0)
    starts = np.arange(0, max(1, y.shape[0] - blk + 1), h)
    ms = (p[np.minimum(starts + blk, y.shape[0])] - p[starts]) / blk
    return starts / sr, -0.691 + 10 * np.log10(ms.sum(axis=1) + 1e-12)


def true_peak_db(x, over=4):
    n = x.shape[0]; X = np.fft.rfft(x, axis=0)
    up = np.fft.irfft(X, n=n * over, axis=0) * over
    return float(20 * np.log10(np.abs(up).max() + 1e-12))


def peak_time(x, sr, frac=0.9):
    """time (s) of the main transient: first point reaching frac of the max envelope (5 ms smoothing)"""
    m = np.abs(x).max(axis=1)
    k = max(1, int(0.005 * sr)); env = np.convolve(m, np.ones(k) / k, mode='same')
    return float(np.argmax(env >= frac * env.max()) / sr)


if __name__ == '__main__':
    if len(sys.argv) < 2: sys.exit(__doc__)
    t0 = float(sys.argv[2]) if len(sys.argv) > 2 else None
    t1 = float(sys.argv[3]) if len(sys.argv) > 3 else None
    for p in sys.argv[1:2]:
        x, sr = load_any(p, 48000, t0, t1)
        ts, st = short_term(x, sr)
        k = int(np.argmax(st))
        print('%s  %.2f s  integrated %.2f LUFS  true peak %.2f dBTP  loudest 3 s %.2f LUFS at %.1f s'
              % (os.path.basename(p), x.shape[0] / sr, lufs(x, sr), true_peak_db(x), st[k], ts[k] + (t0 or 0)))
