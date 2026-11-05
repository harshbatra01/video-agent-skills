# Word-level transcript: python3 asr_words.py <media> <out.json> [model]
import sys, json
from faster_whisper import WhisperModel
m = WhisperModel(sys.argv[3] if len(sys.argv) > 3 else "small.en", device="cpu", compute_type="int8")
import subprocess, numpy as np
raw = subprocess.run(["ffmpeg","-v","error","-i",sys.argv[1],"-ac","1","-ar","16000","-f","f32le","-"],capture_output=True).stdout
audio = np.frombuffer(raw, np.float32)
segs, _ = m.transcribe(audio, word_timestamps=True, vad_filter=False)
words, text = [], []
for s in segs:
    text.append(s.text.strip())
    for w in s.words:
        words.append({"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2)})
json.dump({"text": " ".join(text), "words": words}, open(sys.argv[2], "w"), indent=0)
print(" ".join(text))
