#!/usr/bin/env python3
"""dhruvxr-01 sound design v1: our own synthesized music bed and hits, shaped on WHP's measured sound
(research/dhruvxr/sound/WHP_anatomy.json, research/dhruvxr/raw/WHP/envelope_100ms.json). numpy only (no scipy here).
No voice-over yet: the VO slots stay open on WHP's word times.

Measured on WHP and copied here:
- 0.1 to 1.6 s: sub drop, energy under 60 Hz, pitches 30 to 65 Hz, about 0 dB RMS in 0.1 s windows.
- 2.1 to 2.6 s: dip to about -26 dB.
- Hits are dark low thumps: most energy 60 to 250 Hz, centroid 190 to 240 Hz. Logo moment 8.1 to 8.3 s: sub boom plus high sparkle.
- Bed pitches: A2 110, E3 164.6, A3 220, C5 523, E5 659 (A minor), later F3 174.6, F4 349.2, A5 880 (F major 7). Bed about -18 dB.
- Hits land on picture changes (12 of 22 level jumps within 0.1 s, against 27% chance). Fade to silence 15.96 to 16.49 s.
usage: python3 sound.py [out.wav]
"""
import sys, os, json, subprocess
import numpy as np

SR = 48000; DUR = 16.5; N = int(SR * DUR)
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "out", "sound_v1.wav")
rng = np.random.default_rng(42)
t = np.arange(N) / SR

def spec_filter(x, lo=None, hi=None, slope=0.15):
    """Zero-phase FFT band filter with soft edges (slope = fraction of the cutoff used as a cosine taper)."""
    X = np.fft.rfft(x); f = np.fft.rfftfreq(len(x), 1 / SR); g = np.ones_like(f)
    if hi:
        w = hi * slope; g *= np.clip((hi + w - f) / (2 * w), 0, 1)
    if lo:
        w = lo * slope; g *= np.clip((f - (lo - w)) / (2 * w), 0, 1)
    return np.fft.irfft(X * g, len(x))

def env_ad(n, a, d, shape=1.0):
    e = np.exp(-np.arange(n) / SR / d) ** shape; na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na) ** 0.7; return e

def place(buf, x, t0, gain=1.0):
    i = int(t0 * SR)
    if i >= len(buf): return
    m = min(len(x), len(buf) - i); buf[i:i + m] += x[:m] * gain

def db(x): return 20 * np.log10(np.maximum(np.abs(x), 1e-9))

# reverb: decorrelated stereo exponential noise tails, convolved by FFT
def make_ir(sec=2.4, decay=0.6, seed=1):
    r = np.random.default_rng(seed); n = int(sec * SR); e = np.exp(-np.arange(n) / SR / decay)
    ir = r.standard_normal(n) * e; ir = spec_filter(ir, lo=180, hi=7000); return ir / np.sqrt((ir ** 2).sum())
IRL, IRR = make_ir(seed=1), make_ir(seed=2)
def verb(x, wet=0.3):
    n = len(x) + len(IRL); F = lambda a, b: np.fft.irfft(np.fft.rfft(a, n) * np.fft.rfft(b, n), n)[:len(x)]
    return np.stack([(1 - wet) * x + wet * F(x, IRL), (1 - wet) * x + wet * F(x, IRR)])

def sine_sweep(f0, f1, sec, curve=4.0):
    n = int(sec * SR); k = np.linspace(0, 1, n); f = f1 + (f0 - f1) * np.exp(-curve * k)
    return np.sin(2 * np.pi * np.cumsum(f) / SR)

# ---------- elements ----------
def sub_drop():
    """0.1 to 1.6 s: driven sine dropping 65 -> 30 Hz; harmonics from tanh give the 40/50 Hz partials WHP shows."""
    n = int(1.7 * SR); s = sine_sweep(65, 30, 1.7, curve=2.2)
    e = env_ad(n, 0.03, 0.9) * np.clip(1.6 - np.arange(n) / SR, 0, 1) ** 0.5
    x = np.tanh(2.2 * s) * e
    click = spec_filter(rng.standard_normal(int(0.03 * SR)) * env_ad(int(0.03 * SR), 0.0005, 0.006), lo=1500, hi=9000) * 0.25
    x[:len(click)] += click; return x

def thump(pitch_hi=140, pitch_lo=55, decay=0.35, noise=0.35, sparkle=0.0):
    """Dark low hit: falling sine plus low-passed noise. Centroid around 200 Hz like WHP's hits."""
    n = int((decay * 5) * SR); s = sine_sweep(pitch_hi, pitch_lo, n / SR, curve=25) * env_ad(n, 0.002, decay)
    nz = spec_filter(rng.standard_normal(n), lo=60, hi=500) * env_ad(n, 0.001, decay * 0.5) * noise
    x = np.tanh(1.5 * (s + nz))
    if sparkle:
        sp = spec_filter(rng.standard_normal(n), lo=3000, hi=12000) * env_ad(n, 0.003, 0.25) * sparkle; x = x + sp
    return x

def swell(sec=0.6, lo=200, hi=3000):
    """Reverse-noise swell leading into a hit."""
    n = int(sec * SR); k = np.linspace(0, 1, n); return spec_filter(rng.standard_normal(n), lo=lo, hi=hi) * k ** 3

def glitch(sec, seed=7):
    """Digital stutter for the scan-line tear: gated, bit-crushed, band-passed noise bursts on the frame grid."""
    r = np.random.default_rng(seed); n = int(sec * SR); x = np.zeros(n); fl = SR // 30
    for i in range(0, n, fl):
        if r.random() < 0.7:
            m = min(fl, n - i); b = r.standard_normal(m) * (0.4 + 0.6 * r.random())
            b = np.round(b * 6) / 6; b = np.repeat(b[::int(r.integers(2, 9))], int(r.integers(2, 9)))[:m]
            x[i:i + len(b)] += b
    return spec_filter(x, lo=700, hi=7000) * 0.5

def pad(notes, sec, attack=0.9, release=1.2, bright=3200):
    """Soft chorused pad: three detuned triangles per note, low-passed."""
    n = int(sec * SR); tt = np.arange(n) / SR; x = np.zeros(n)
    for f, a in notes:
        for det, ph in ((-0.12, 0.0), (0.0, 1.3), (0.13, 2.1)):
            ff = f * (1 + det / 100 * 6); vib = 1 + 0.002 * np.sin(2 * np.pi * 0.21 * tt + ph)
            p = (np.cumsum(ff * vib) / SR + ph / (2 * np.pi)) % 1; tri = 2 * np.abs(2 * p - 1) - 1; x += tri * a / 3
    e = np.minimum(1, tt / attack) ** 1.5 * np.minimum(1, (sec - tt) / release).clip(0, 1)
    return spec_filter(x * e, lo=70, hi=bright)

# ---------- arrangement (times from WHP / our picture plan) ----------
L = np.zeros(N); mono = np.zeros(N); bedbuf = np.zeros(N)
intro = np.zeros(N); place(intro, sub_drop(), 0.10, 1.0)
AM = [(110.0, 0.20), (164.8, 0.35), (220.0, 0.35), (523.25, 0.22), (659.25, 0.28)]           # A minor, as measured 4.6 to 6.3 s
FM7 = [(110.0, 0.16), (174.6, 0.3), (261.6, 0.3), (349.2, 0.25), (659.3, 0.2), (880.0, 0.22)]  # F major 7 colours, as measured 11.4 to 14 s
place(bedbuf, pad(AM, 7.4), 2.62)                    # starts after the dip (2.1 to 2.6 s stays near silent)
place(bedbuf, pad(FM7, 6.9, attack=1.4), 9.15)
place(bedbuf, pad([(55.0, 0.5)], 1.5, attack=0.4, release=1.0), 0.6, 0.0)   # placeholder slot, silent
hits = [  # (time s, kind, gain) on our picture changes; sound leads the picture by 0 to 3 frames as on WHP
    (1.50, "small", 0.35),   # white flash f45
    (2.53, "mid", 0.70),     # "Backlog" frame f76
    (2.86, "mid", 0.75),     # threshold into crowd from above f86
    (3.03, "small", 0.45),   # app tilt lands f91
    (3.90, "mid", 0.55),     # glitch peak
    (4.36, "big", 0.85),     # white into the crosshair f130
    (6.42, "big", 0.80),     # white flash f195
    (8.08, "boom", 1.00),    # logo bloom f243
    (9.62, "mid", 0.70),     # tiles f287
    (10.73, "mid", 0.65),    # white f322, second burst
    (11.03, "small", 0.50),  # stairwell f331
    (11.23, "small", 0.45),  # fisheye f337
    (14.03, "mid", 0.70),    # wordmark wipe f421
    (14.50, "small", 0.45),  # end accent
]
for tt0, kind, gn in hits:
    x = {"small": thump(120, 60, 0.22, 0.3), "mid": thump(150, 55, 0.35, 0.35), "big": thump(170, 48, 0.5, 0.4, sparkle=0.08),
         "boom": thump(180, 36, 0.9, 0.45, sparkle=0.15)}[kind]
    place(mono, x, tt0, gn)
place(mono, swell(0.5), 8.08 - 0.5, 0.30)            # swell into the logo bloom (WHP level climbs from 7.9 s)
place(mono, swell(0.35, 400, 5000), 4.36 - 0.35, 0.22)
place(mono, glitch(0.57), 3.73, 0.55)                 # scan-line tear f112 to f129
place(mono, glitch(0.10, seed=9), 4.23, 0.4)

# room tone in the dip (WHP sits at about -26 dB there, not silence): dark air plus the sub's own reverb tail
air = spec_filter(rng.standard_normal(N), lo=150, hi=2500); air *= ((t > 1.45) & (t < 2.75)) * np.clip(np.minimum(t - 1.45, 2.75 - t) / 0.3, 0, 1)
rest = verb(mono, wet=0.28) + verb(bedbuf, wet=0.45); lead = verb(intro, wet=0.18)
fade = np.ones(N); i0, i1 = int(15.1 * SR), int(16.3 * SR); fade[i0:i1] = np.linspace(1, 0, i1 - i0) ** 2; fade[i1:] = 0
whp = json.load(open(os.path.join(os.path.dirname(__file__), "../../../research/dhruvxr/raw/WHP/envelope_100ms.json")))
def med_db(x, t0, t1):
    m = x.mean(0) if x.ndim == 2 else x; w = SR // 10
    return float(np.median([10 * np.log10(np.mean(m[i:i + w] ** 2) + 1e-12) for i in range(int(t0 * SR), int(t1 * SR), w)]))
def whp_db(t0, t1): return float(np.median([r["db"] for r in whp if t0 <= r["t"] < t1]))
# level each stem to WHP's measured level in its own section
# TRIM: measured offsets between this stereo levelling and the mono downmix used to measure WHP (render v1 pass 2: bed +2.9, intro +2.0 dB)
TRIM_REST, TRIM_LEAD = -2.9, -2.0
rest *= 10 ** ((whp_db(4.6, 14.0) - med_db(rest, 4.6, 14.0) + TRIM_REST) / 20)
lead *= 10 ** ((whp_db(0.2, 1.5) - med_db(lead, 0.2, 1.5) + TRIM_LEAD) / 20)
air *= 10 ** ((whp_db(2.1, 2.6) - 3 - med_db(air, 2.1, 2.6)) / 20)
st = (rest + lead + air[None, :]) * fade
# limiter: only samples above 0.70 are bent, soft knee, ceiling 0.89 (about -1 dBFS sample peak)
thr, ceil = 0.70, 0.89; a = np.abs(st); over = a > thr
st[over] = np.sign(st[over]) * (thr + (ceil - thr) * np.tanh((a[over] - thr) / (ceil - thr)))
os.makedirs(os.path.dirname(os.path.abspath(OUT)), exist_ok=True)
pcm = (np.clip(st.T, -1, 1) * 32767).astype("<i2").tobytes()
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "s16le", "-ar", str(SR), "-ac", "2", "-i", "-", OUT], input=pcm, check=True)
print("wrote", OUT)
