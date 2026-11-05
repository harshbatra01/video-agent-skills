"""Mac (Apple Silicon) only as written: mlx-whisper. On Windows use faster-whisper (see README).
Re-transcribe phrases where Whisper produced repetition garbage (e.g. 'fine fine fine ...')."""
import json, re, wave, numpy as np, mlx_whisper
w = wave.open("raw_a0.wav"); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
P = json.load(open("pieces_asr.json"))
def looped(t):
    toks = re.findall(r"[a-z0-9']+", t.lower())
    return len(toks) >= 6 and max(toks.count(v) for v in set(toks)) >= max(5, len(toks) // 2)
fixed = 0
for pc in P:
    if not looped(pc["text"]):
        continue
    a, b = pc["a"], pc["b"]
    clip = np.concatenate([np.zeros(8000, np.float32), x[int(a * 16000):int(b * 16000)], np.zeros(8000, np.float32)])
    best = None
    for kw in ({"temperature": (0.0, 0.2, 0.4)}, {"temperature": 0.3}):
        r = mlx_whisper.transcribe(clip, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                                   condition_on_previous_text=False, word_timestamps=True, **kw)
        txt = " ".join(s["text"].strip() for s in r["segments"]).strip()
        if not looped(txt):
            best = (txt, [{"w": ww["word"].strip(), "s": round(ww["start"] - 0.5 + a, 2), "e": round(ww["end"] - 0.5 + a, 2)}
                          for s in r["segments"] for ww in s.get("words", [])])
            break
    print(f"{a:7.2f}-{b:7.2f} was: {pc['text'][:60]!r} -> {best[0] if best else 'STILL LOOPING'!r}")
    if best:
        pc["text"], pc["words"] = best
        fixed += 1
json.dump(P, open("pieces_asr.json", "w"), indent=0)
print("fixed", fixed)
