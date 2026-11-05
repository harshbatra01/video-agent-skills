"""Transcribe downloaded videos (media only) with faster-whisper on the GPU.
Run with the whisperx venv:  ~/venvs/whisperx/Scripts/python.exe -I asr.py <videos_dir> <data_dir> name [name ...]
Writes <data_dir>/asr_<name>.txt (segment start-end + text) and prints it.
"""
import sys, os, subprocess, shutil, glob
import torch  # noqa: F401  (loads the CUDA runtime DLLs that ctranslate2 needs)
import numpy as np
from faster_whisper import WhisperModel

vid_dir, data_dir, names = sys.argv[1], sys.argv[2], sys.argv[3:]
ff = shutil.which("ffmpeg") or glob.glob(os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\ffmpeg.exe"))[0]
model = WhisperModel("mobiuslabsgmbh/faster-whisper-large-v3-turbo", device="cuda", compute_type="float16")
for name in names:
    src = os.path.join(vid_dir, name + ".mp4")
    if not os.path.exists(src):
        print("=== missing", name)
        continue
    pcm = subprocess.run([ff, "-loglevel", "error", "-i", src, "-vn", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
    audio = np.frombuffer(pcm, dtype=np.float32)
    if audio.size < 1600:
        print("=== asr", name, "no audio")
        continue
    segs, info = model.transcribe(audio, vad_filter=True, beam_size=1)
    lines = ["%5.1f-%5.1f %s" % (s.start, s.end, s.text.strip()) for s in segs]
    txt = "lang %s (%.2f)\n" % (info.language, info.language_probability) + "\n".join(lines)
    with open(os.path.join(data_dir, "asr_%s.txt" % name), "w", encoding="utf-8") as f:
        f.write(txt)
    print("=== asr", name)
    print(txt[:2500])
