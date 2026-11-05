"""Map an edited music file back to its source track: which source time each part of the edit comes from (finds the cuts).
Coarse search on a 2 kHz decimated copy, then refined at full rate."""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from track_an import load

SR = 48000; D = 24; SRD = SR // D


def dec(x):
    n = len(x) // D * D
    return x[:n].reshape(-1, D).mean(axis=1)


def xcorr_locate(f, seg):
    n = len(f) + len(seg); nfft = 1 << (n - 1).bit_length()
    c = np.fft.irfft(np.fft.rfft(f, nfft) * np.conj(np.fft.rfft(seg, nfft)), nfft)[:len(f) - len(seg) + 1]
    cs = np.concatenate([[0], np.cumsum(f ** 2)])
    norm = np.sqrt(cs[len(seg):len(seg) + len(c)] - cs[:len(c)] + 1e-12) * (np.linalg.norm(seg) + 1e-12)
    r = c / norm; k = int(np.argmax(r))
    return k, float(r[k])


def segments(edit_path, src_path, blk_s=0.5):
    e = load(edit_path).mean(axis=1); s = load(src_path).mean(axis=1)
    ed, sd = dec(e), dec(s); blk = int(blk_s * SRD)
    rows = []
    for i in range(0, len(ed) - blk, blk):
        k, q = xcorr_locate(sd, ed[i:i + blk])
        rows.append((i / SRD, k / SRD, q))
    segs = []
    for t, src, q in rows:
        off = src - t
        if not segs or abs(off - segs[-1][2]) > 0.03:
            segs.append([t, src, off, q])
    return segs, len(e) / SR


if __name__ == '__main__':
    segs, dur = segments(sys.argv[1], sys.argv[2])
    print('edit %.2f s' % dur)
    for t, src, off, q in segs:
        print('  edit %6.2f s <- source %7.2f s (offset %+8.2f, match %.2f)' % (t, src, off, q))
