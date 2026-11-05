# Sound library for the synthesised score (stand-in music). Same sounds as score.py, as functions.
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
SR = 48000
_rng = np.random.default_rng(11)
def bp(x, lo, hi): return sosfilt(butter(2, [lo, hi], "bandpass", fs=SR, output="sos"), x)
def lp(x, f): return sosfilt(butter(2, f, "lowpass", fs=SR, output="sos"), x)
def saw(f, n): ph = (np.arange(n) * f / SR) % 1.0; return 2 * ph - 1
def env(n, a, d): e = np.exp(-np.arange(n) / SR / d); na = max(1, int(a * SR)); e[:na] *= np.linspace(0, 1, na); return e
_IR = _rng.standard_normal(int(2.2 * SR)) * np.exp(-np.arange(int(2.2 * SR)) / SR / 0.55); _IR /= np.abs(_IR).sum() / 6
def verb(x, wet=0.35): return (1 - wet) * x + wet * fftconvolve(x, _IR)[:len(x)]
def impact(big=1.0):
    n = int(2.5 * SR); sub = np.sin(2 * np.pi * np.cumsum(28 + 90 * np.exp(-np.arange(n) / SR / 0.05)) / SR) * env(n, 0.001, 0.6)
    crack = bp(_rng.standard_normal(n), 900, 7000) * env(n, 0.0005, 0.05)
    braam = lp(sum(saw(f, n) for f in (55, 55.4, 110, 82.4)) / 4, 900) * env(n, 0.01, 0.9)
    return verb(sub + crack * 0.5 + braam * 0.5 * big, 0.3)
def glitch(ms=40):
    n = int(ms / 1000 * SR); x = np.sign(_rng.standard_normal(n)) * (_rng.random(n) > 0.6)
    x = np.repeat(x[::12], 12)[:n]; return bp(x, 1500, 9000) * env(n, 0.0005, ms / 1000 / 2)
def whoosh(s=0.45, rev=False):
    n = int(s * SR); x = bp(_rng.standard_normal(n), 600, 8000) * np.hanning(n) ** 1.5; return x[::-1] if rev else x
def riser(s):
    n = int(s * SR); x = _rng.standard_normal(n) * np.linspace(0, 1, n) ** 3
    tone = np.sin(2 * np.pi * np.cumsum(np.linspace(110, 880, n)) / SR) * np.linspace(0, 1, n) ** 2
    return bp(x, 400, 9000) * 0.7 + tone * 0.15
def tick(): n = int(0.03 * SR); return bp(_rng.standard_normal(n), 5000, 11000) * env(n, 0.0005, 0.008)
def kick(): n = int(0.32 * SR); return np.sin(2 * np.pi * np.cumsum(38 + 70 * np.exp(-np.arange(n) / SR / 0.035)) / SR) * env(n, 0.001, 0.11)

def render(plan, cuts, dur):
    """plan: bpm grid, sections (t0,t1,energy), drops/impacts/hits. cuts: [{t, fx}] from the edit plan; every cut gets a sound."""
    N = int(dur * SR); t = np.arange(N) / SR; S16 = plan["s16"]; grid = np.arange(0, dur, S16)
    energy = np.zeros(N)
    for s in plan["sections"]: energy[int(s["t0"] * SR):int(s["t1"] * SR)] = s["energy"]
    sm = lambda x: np.convolve(x, np.ones(2400) / 2400, mode="same")
    LV = {k: sm((energy >= k).astype(float)) for k in (2, 3, 4)}
    mix = np.zeros(N)
    dr = sum(saw(f, N) for f in (55.0, 55.3, 82.4, 82.0, 110.2)) / 5
    mix += lp(dr, 380) * (0.10 + 0.08 * LV[2] + 0.06 * LV[4]) * np.clip(t / 1.0, 0, 1)
    tk, kk = tick(), kick()
    for i, g in enumerate(grid):
        j = int(g * SR)
        if j + len(kk) >= N: break
        mix[j:j + len(tk)] += tk * (0.22 if i % 4 == 0 else 0.11) * LV[2][j]
        if i % 2 == 0: mix[j:j + len(kk)] += kk * 0.55 * ((1.0 if i % 4 == 0 else 0) * LV[3][j] + (0.45 if i % 4 else 0) * LV[4][j])
    br = sum(saw(f, N) for f in (55.0, 54.7, 110.0, 164.8, 165.3)) / 5
    cut_f = 300 + 900 * (0.5 + 0.5 * np.cos(2 * np.pi * t / (S16 * 8)))
    mix += (lp(br, 700) * 0.6 + lp(br, 1500) * 0.4 * (cut_f > 900)) * 0.16 * LV[4]
    def put(x, at, g=1.0):
        j = int(at * SR); n = min(len(x), N - j)
        if j >= 0 and n > 0: mix[j:j + n] += x[:n] * g
    for h in plan["hits"]:
        a = h["t"]
        if h["kind"] == "drop":
            if a > 1.8: put(riser(1.6), a - 1.6 - S16, 0.6); mix[int((a - S16) * SR):int(a * SR)] *= 0.15
            put(impact(1.0), a, 1.0)
        elif h["kind"] == "impact": put(whoosh(0.35, True), a - 0.35, 0.5); put(impact(0.7), a, 0.85)
        elif h["kind"] == "hit": put(impact(0.3), a, 0.55)
        elif h["kind"] == "end": put(impact(1.0), a, 0.95)
        elif h["kind"] == "open": put(impact(0.6), a, 0.9)
    hit_t = [h["t"] for h in plan["hits"]]
    for c in cuts:   # a sound on every cut; the big ones are already in hits
        a = c["t"]; fx = c.get("fx", "cut")
        if any(abs(a - h) < 0.03 for h in hit_t) and fx not in ("blocks", "whip"): continue
        if fx == "blocks":
            for fr in (0, 1, 2, 5, 6, 8): put(glitch(35), a + fr / 30, 0.7)
        elif fx == "whip": put(whoosh(0.4), a - 0.32, 0.6); put(impact(0.25), a, 0.5)
        elif fx in ("flash", "shake"): put(whoosh(0.3, True), a - 0.3, 0.45); put(impact(0.5), a, 0.65)
        elif fx == "pop": put(glitch(30), a, 0.75); put(impact(0.12), a, 0.4)
        else: put(glitch(25), a, 0.45); put(tick() * 3, a, 0.4)
    mix *= np.clip((dur - t) / 1.2, 0, 1)
    return mix / (np.max(np.abs(mix)) + 1e-9) * 0.7
