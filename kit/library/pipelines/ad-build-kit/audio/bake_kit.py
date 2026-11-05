"""Bake the Immufix SFX kit: 48 kHz / 24-bit stereo WAVs, trimmed, layered POPs with driven low layer, pitched pings tuned to the
music key (G major), count ramps cut to length. Writes kit.json with peak offset (for peak-aligned placement) and loudness."""
import os, sys, glob, json, struct
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyze_sfx import read_wav
import atools as A

SRC = r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Audio\SFX"
OUT = r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\Audio\SFX kit"
HERE = os.path.dirname(os.path.abspath(__file__))
SR = 48000
NOTE = ['C', 'C#', 'D', 'Eb', 'E', 'F', 'F#', 'G', 'Ab', 'A', 'Bb', 'B']
TRIAD = [7, 11, 2]            # G B D
SCALE = [7, 9, 11, 0, 2, 4, 6]  # G major


def resample(a, sr_in, sr_out):
    """FFT resampling with padding (anti-aliased by spectral truncation + taper)"""
    if abs(sr_in - sr_out) < 1e-6: return a.copy()
    pad = int(0.05 * sr_in)
    ap = np.pad(a, ((pad, pad), (0, 0)))
    N = len(ap); M = int(round(N * sr_out / sr_in))
    X = np.fft.rfft(ap, axis=0)
    k = min(N, M) // 2 + 1
    Y = np.zeros((M // 2 + 1, a.shape[1]), complex); Y[:k] = X[:k]
    t0 = int(k * 0.94); w = 0.5 * (1 + np.cos(np.linspace(0, np.pi, k - t0)))
    Y[t0:k] *= w[:, None]
    y = np.fft.irfft(Y, n=M, axis=0) * (M / N)
    p2 = int(round(pad * sr_out / sr_in)); m = int(round(len(a) * sr_out / sr_in))
    return y[p2:p2 + m]


def load(prefix):
    p = glob.glob(os.path.join(SRC, prefix + '_*.wav'))
    assert len(p) == 1, (prefix, p)
    a, sr, _, _ = read_wav(p[0])
    if a.shape[1] == 1: a = np.repeat(a, 2, axis=1)
    return resample(a[:, :2], sr, SR)


def pitch(a, semis):
    return a if semis == 0 else resample(a, SR * 2 ** (semis / 12), SR)


def env(a, ms=3):
    k = max(1, int(ms / 1000 * SR)); return np.convolve(np.abs(a).max(axis=1), np.ones(k) / k, mode='same')


def peak_idx(a):
    e = env(a); return int(np.argmax(e >= 0.9 * e.max()))


def drive(a, d):
    return np.tanh(d * a / (np.abs(a).max() + 1e-12)) / np.tanh(d) * np.abs(a).max()


def layer(parts):
    """parts: [(array, gain_db)], aligned on each part's main peak"""
    pk = [peak_idx(x) for x, _ in parts]; lead = max(pk)
    n = max(lead - p + len(x) for (x, _), p in zip(parts, pk))
    out = np.zeros((n, 2))
    for (x, g), p in zip(parts, pk):
        o = lead - p; out[o:o + len(x)] += x * 10 ** (g / 20)
    return out


def dominant_pc(a):
    p = peak_idx(a); seg = a[p:p + int(0.25 * SR)].mean(axis=1)
    sp = np.abs(np.fft.rfft(seg * np.hanning(len(seg)), n=1 << 16)); f = np.fft.rfftfreq(1 << 16, 1 / SR)
    ok = (f > 250) & (f < 5000); fpk = f[ok][np.argmax(sp[ok])]
    midi = 69 + 12 * np.log2(fpk / 440.0)
    return fpk, midi


def tune(a, name):
    fpk, midi = dominant_pc(a)
    best = None
    for pcs, lim in ((TRIAD, 2.5), (SCALE, 6)):
        for target in range(int(midi) - 7, int(midi) + 8):
            if target % 12 in pcs:
                d = target - midi
                if abs(d) <= lim and (best is None or abs(d) < abs(best)): best = d
        if best is not None: break
    best = best or 0.0
    print('   tune %-10s %.0f Hz (%s%+.2f) -> shift %+.2f st' % (name, fpk, NOTE[int(round(midi)) % 12], midi - round(midi), best))
    return pitch(a, best), round(best, 2)


def trim(a, kind, max_len=None, pre_ms=10, floor_db=-50):
    e = env(a); top = e.max()
    if kind == 'swell': on = int(np.argmax(e >= top * 10 ** (-40 / 20)))
    else: on = int(np.argmax(e >= 0.1 * top))
    s = max(0, on - int(pre_ms / 1000 * SR))
    live = np.where(e > top * 10 ** (floor_db / 20))[0]
    end = min(len(a), live[-1] + int(0.03 * SR))
    if max_len: end = min(end, s + int(max_len * SR))
    y = a[s:end].copy()
    fi = int(0.002 * SR); y[:fi] *= np.linspace(0, 1, fi)[:, None]
    tail = len(y) - peak_idx(y); fo = int(min(max(0.05 * SR, 0.3 * tail), 0.25 * SR, max(16, tail - 1)))
    y[-fo:] *= (0.5 * (1 + np.cos(np.linspace(0, np.pi, fo))))[:, None]
    return y


def window_end(a, dur, fade_in=0.012):
    """last `dur` seconds of a ramp, starting at a quiet point between ticks"""
    e = env(a, 2); top = e.max(); live = np.where(e > top * 10 ** (-45 / 20))[0]; end = live[-1] + int(0.03 * SR)
    s0 = end - int(dur * SR); lo = max(0, s0 - int(0.04 * SR))
    s = lo + int(np.argmin(e[lo:s0 + 1]))
    y = a[s:end].copy(); fi = int(fade_in * SR); y[:fi] *= np.linspace(0, 1, fi)[:, None]
    fo = int(0.04 * SR); y[-fo:] *= np.linspace(1, 0, fo)[:, None]
    return y


def write24(path, a):
    a = np.clip(a, -1, 1 - 2 ** -23); v = np.round(a * (2 ** 23 - 1)).astype(np.int32)
    b = np.zeros((len(v) * 2, 3), np.uint8); flat = v.reshape(-1)
    b[:, 0] = flat & 0xFF; b[:, 1] = (flat >> 8) & 0xFF; b[:, 2] = (flat >> 16) & 0xFF
    data = b.tobytes()
    hdr = b'RIFF' + struct.pack('<I', 36 + len(data)) + b'WAVE' + b'fmt ' + struct.pack('<IHHIIHH', 16, 1, 2, SR, SR * 6, 6, 24) + b'data' + struct.pack('<I', len(data))
    with open(path, 'wb') as f: f.write(hdr + data)


def momentary_max(a):
    t, m = A.short_term(np.pad(a, ((int(0.2 * SR), int(0.2 * SR)), (0, 0))), SR, win=0.4, hop=0.01)
    return float(np.max(m))


def hp(a, fc=250.0):
    X = np.fft.rfft(a, axis=0); f = np.fft.rfftfreq(len(a), 1 / SR)
    X *= (1 / np.sqrt(1 + (fc / np.maximum(f, 1e-3)) ** 4))[:, None]
    return np.fft.irfft(X, n=len(a), axis=0)


def finish(name, y, kind, note=''):
    y = y / (np.abs(y).max() + 1e-12) * 10 ** (-1 / 20)
    os.makedirs(OUT, exist_ok=True)
    fn = 'IMX_%s.wav' % name; write24(os.path.join(OUT, fn), y)
    p = peak_idx(y); e = env(y); on = int(np.argmax(e >= 0.1 * e.max()))
    sp = np.abs(np.fft.rfft(y.mean(axis=1))) ** 2; f = np.fft.rfftfreq(len(y), 1 / SR)
    sub = float(sp[f < 150].sum() / (sp.sum() + 1e-18))
    r = dict(name=name, file=fn, kind=kind, dur=round(len(y) / SR, 4), peak_t=round(p / SR, 4), onset_t=round(on / SR, 4),
             m_max=round(momentary_max(y), 2), m_phone=round(momentary_max(hp(y)), 2), sub150=round(sub, 2), note=note)
    print('%-12s %5.2fs peak@%.3f M %6.1f phone %6.1f sub %.2f %s' % (name, r['dur'], r['peak_t'], r['m_max'], r['m_phone'], sub, note))
    return r


def build():
    kit = []
    # layered caption pops: bright top + driven low layer, peaks aligned
    pops = {
        'POP1': [('TOP_WhooshMaximize', 0, 0), ('POP_GlitchThud02', -7, 2.5)],
        'POP2': [('TOP_LazerMaximize', 0, 0), ('POP_GlitchyVarious04', -7, 2.5)],
        'POP3': [('TOP_SynthHitUmm', 0, 0), ('POP_GlitchThud04', -3, 2.5)],
        'POP4': [('POP_GlitchNoiseMetal', 0, 0), ('POP_GlitchSub02', -4, 2.0)],
        'POP5': [('POP_BulletsGlitchSub', 0, 1.5), ('TICK_TechButton05', -8, 0)],
    }
    built = {}
    for name, parts in pops.items():
        xs = []
        for pre, g, d in parts:
            x = trim(load(pre), 'hit', max_len=0.7)
            x = x / np.abs(x).max()
            if d: x = drive(x, d)
            xs.append((x, g))
        y = trim(layer(xs), 'hit', max_len=0.7); built[name] = y
        kit.append(finish(name, y, 'hit', '+'.join(p[0] for p in parts)))
    # rising stack (vitamins / minerals / nutrients): POP1 at G-major steps
    for s, nm in ((2, 'POP1_up2'), (4, 'POP1_up4')):
        kit.append(finish(nm, pitch(built['POP1'], s), 'hit', 'POP1 %+d st' % s))
    for nm, pre in (('TICK1', 'TICK_ConfirmDull'), ('TICK2', 'TICK_SimpleSelect'), ('TICK3', 'TICK_TechButton05')):
        kit.append(finish(nm, trim(load(pre), 'hit', max_len=0.35), 'hit', pre))
    for nm, pre in (('GLASS1', 'GLASS_PingSelect'), ('GLASS2', 'GLASS_ConfirmLight'), ('GLASS3', 'GLASS_TingsMetal'), ('QPOP1', 'QPOP_BubbleSingle02'), ('LOCK2', 'LOCK_LockedIn')):
        y, st = tune(trim(load(pre), 'hit', max_len=1.0), nm)
        kit.append(finish(nm, y, 'hit', '%s tuned %+.2f st' % (pre, st)))
    kit.append(finish('LOCK1', trim(load('LOCK_ConfirmMenu'), 'hit', max_len=0.6), 'hit', 'LOCK_ConfirmMenu'))
    kit.append(finish('LIGHT1', trim(load('LIGHT_SwitchGarageReverb'), 'hit', max_len=0.9), 'hit', 'LIGHT_SwitchGarageReverb'))
    lv = load('LIGHT_LeverMetallic02'); lv = lv[:int(0.55 * SR)]
    kit.append(finish('LIGHT2', trim(lv, 'hit', max_len=0.45), 'hit', 'LIGHT_LeverMetallic02 first hit'))
    kit.append(finish('FLIP1', trim(load('FLIP_SlotCrank'), 'hit', max_len=0.8, pre_ms=5), 'hit', 'FLIP_SlotCrank'))
    kit.append(finish('FLIP2', trim(load('FLIP_RhythmicClicks04'), 'hit', max_len=0.6, pre_ms=5), 'hit', 'FLIP_RhythmicClicks04'))
    for nm, pre, d in (('BOOM1', 'BOOM_CinematicDeep', 3.0), ('BOOM2', 'BOOM_StingerThud', 3.0)):
        x = trim(load(pre), 'hit', max_len=1.8); x = drive(x / np.abs(x).max(), d)
        kit.append(finish(nm, x, 'hit', pre + ' driven'))
    for nm, pre, ml in (('SWISH1', 'SWISH_SoftAiry', 0.9), ('SWISH2', 'SWISH_ClassicDry', 0.7), ('SWISH3', 'SWISH_SwooshLight', 1.2),
                        ('WHOOSH1', 'WHOOSH_MediumTransition', 2.0), ('WHOOSH2', 'WHOOSH_SoftHitShort', 0.8), ('WHOOSH3', 'WHOOSH_TechData02', 1.3),
                        ('SHIM1', 'SHIM_GlassShimmerWhoosh02', 2.2), ('HUD1', 'TOP_BringUpHud', 1.0)):
        kit.append(finish(nm, trim(load(pre), 'swell', max_len=ml), 'swell', pre))
    for nm, pre, d in (('COUNT_10', 'COUNT_RelayRamp01', 1.0), ('COUNT_09', 'COUNT_RelayRamp02', 0.9), ('COUNT_05', 'COUNT_TickPitchUp', 0.5)):
        kit.append(finish(nm, window_end(load(pre), d), 'count', '%s last %.1fs' % (pre, d)))
    json.dump(kit, open(os.path.join(HERE, 'kit.json'), 'w'), indent=1)
    print(len(kit), 'kit files ->', OUT)


if __name__ == '__main__':
    build()
