"""Procedural SFX (our own, free): whooshes, impacts, risers, glitch ticks, as 48 kHz stereo WAV.

usage: python sfx.py OUT_DIR
Mix them LOW under the song (about -14 to -20 dB below it): the song is the product, these only add weight to cuts.
"""
import sys, os, wave
import numpy as np

SR = 48000
rng = np.random.default_rng(7)

def write(path, x):
    x = np.asarray(x, np.float32)
    if x.ndim == 1: x = np.stack([x, x], 1)
    x = x / (np.abs(x).max() + 1e-9) * 0.89                     # -1 dBFS peak
    w = wave.open(path, "wb"); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 32767).astype(np.int16).tobytes()); w.close(); return path

def bandpass_sweep(n, f0, f1, q=2.0):
    """noise through a resonant band-pass whose centre glides f0 -> f1 (simple state-variable filter)"""
    x = rng.standard_normal(n); y = np.zeros(n); low = band = 0.0
    fc = np.geomspace(f0, f1, n)
    for i in range(n):
        f = 2 * np.sin(np.pi * fc[i] / SR); high = x[i] - low - band / q
        band += f * high; low += f * band; y[i] = band
    return y

def whoosh(dur=0.45, up=True, peak_at=0.8):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    y = bandpass_sweep(n, 250 if up else 3500, 3500 if up else 250, q=1.4)
    env = np.where(t < peak_at, (t / peak_at) ** 2.2, np.exp(-(t - peak_at) / 0.06))
    y *= env; pan = np.clip(t * 1.4 - 0.2, 0, 1) if up else 1 - t
    return np.stack([y * (1 - 0.6 * pan), y * (0.4 + 0.6 * pan)], 1)

def impact(dur=1.4):
    n = int(dur * SR); t = np.arange(n) / SR
    f = 38 + 70 * np.exp(-t / 0.05)                              # sub drop 108 -> 38 Hz
    sub = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t / 0.45)
    click = rng.standard_normal(n) * np.exp(-t / 0.012) * 0.6
    body = bandpass_sweep(n, 900, 120, q=0.9) * np.exp(-t / 0.18) * 0.5
    tail = np.convolve(rng.standard_normal(n) * np.exp(-t / 0.35), np.ones(64) / 64, mode="same") * 0.08
    return sub + click + body + tail

def riser(dur=1.2):
    n = int(dur * SR); t = np.linspace(0, 1, n)
    noise = bandpass_sweep(n, 400, 7000, q=1.2) * t ** 2.5
    tone = np.sin(2 * np.pi * np.cumsum(np.geomspace(180, 900, n)) / SR) * t ** 3 * 0.3
    return (noise + tone) * (1 - np.exp(-(1 - t) / 0.01))

def glitch(dur=0.18):
    n = int(dur * SR); y = np.zeros(n); i = 0
    while i < n:
        L = int(rng.integers(120, 900)); seg = np.sign(np.sin(2 * np.pi * rng.uniform(300, 3000) * np.arange(L) / SR)) * rng.uniform(0.2, 1)
        y[i:i + L] = seg[: max(0, min(L, n - i))]; i += L + int(rng.integers(0, 600))
    return y * np.exp(-np.linspace(0, 3, n))

if __name__ == "__main__":
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for name, x in [("whoosh_up", whoosh(0.45, True)), ("whoosh_down", whoosh(0.4, False)), ("whoosh_short", whoosh(0.22, True, 0.85)),
                    ("impact", impact()), ("riser", riser()), ("glitch", glitch())]:
        print(write(os.path.join(out, name + ".wav"), x))
