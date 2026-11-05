"""Transcribe every speech piece on its own (catches restarts a whole-file transcript merges).
Mac (Apple Silicon) only as written: mlx-whisper. On Windows use faster-whisper (see README)."""
import json, wave, numpy as np, mlx_whisper, sys
w = wave.open("raw_a0.wav"); x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
R = json.load(open("regions_full.json"))
out = []
for k, pc in enumerate(R["pieces"]):
    a, b = pc["a"], pc["b"]
    clip = np.concatenate([np.zeros(8000, np.float32), x[int(a * 16000):int(b * 16000)], np.zeros(8000, np.float32)])
    r = mlx_whisper.transcribe(clip, path_or_hf_repo="mlx-community/whisper-large-v3-turbo", language="en",
                               condition_on_previous_text=False, word_timestamps=True,
                               initial_prompt="Reading funny tweets and memes aloud.")
    words = [{"w": ww["word"].strip(), "s": round(ww["start"] - 0.5 + a, 2), "e": round(ww["end"] - 0.5 + a, 2)}
             for s in r["segments"] for ww in s.get("words", [])]
    out.append({**pc, "text": " ".join(s["text"].strip() for s in r["segments"]).strip(), "words": words})
    if k % 50 == 0:
        print(k, a, out[-1]["text"][:60], flush=True)
        json.dump(out, open("pieces_asr.json", "w"))
json.dump(out, open("pieces_asr.json", "w"), indent=0)
print("done", len(out))
