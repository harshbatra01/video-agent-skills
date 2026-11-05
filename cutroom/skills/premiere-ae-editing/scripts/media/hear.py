"""Hear any media file: local Whisper (faster-whisper, large-v3-turbo, CPU int8) -> words with timings.
usage: python hear.py <media file> <out.json> [vocab.txt] [model]
vocab.txt (optional): names the model should spell right (people, places, products), any separator. Used as hotwords
on EVERY 30 s window (an initial prompt alone only reaches the first window: a name came out garbled after it).
Output JSON: {"file", "duration", "segments": [{"s","e","text"}], "words": [{"s","e","w","p"}]}"""
import sys, json, os, time, wave


# ---- macOS branch (from the Mac port, Oct 2026). Windows never runs it; the faster-whisper code further down is unchanged.
# With mlx-whisper installed (Apple Silicon, its own venv) a Mac transcribes with mlx-whisper large-v3-turbo on the GPU:
#   ~/.venvs/mlx-whisper/bin/python hear.py <media> <out.json> [vocab.txt] [model] [--vocab F] [--model M] [--from S] [--to S]
# Without mlx-whisper (Intel Mac, venv missing) it falls through to faster-whisper below (pip install faster-whisper av),
# which takes only the positional form: --vocab/--model/--from/--to need mlx-whisper.
# mlx-whisper decodes media with ffmpeg (Homebrew), and its first run downloads the model from Hugging Face (about 1.6 GB).
# Differences from the Windows path:
# - no hotwords in mlx-whisper: the vocab file only becomes the initial prompt (first 30 s window), and a names prompt once
#   hallucinated the names into the opening seconds: check the first words and the names by ear.
# - --from/--to transcribe one window (ffmpeg cuts it first); times stay in the FULL file's seconds. Word timestamps on a
#   whole long file once dropped about two thirds of the speech: word-level work on a 20+ minute file goes window by window.
# - after each run it prints words per 5 minutes (a talking track runs ~900-1100; a sudden drop to double digits is a
#   decode loop, not silence: re-run that region alone) and flags a short segment repeated 8+ times in a row.
# - "duration" in the JSON is the end of the last segment, not the file length.
def _mac_mlx_main():
    import argparse, subprocess, tempfile, collections
    import mlx_whisper
    models = {'turbo': 'mlx-community/whisper-large-v3-turbo', 'large-v3-turbo': 'mlx-community/whisper-large-v3-turbo',
              'large-v3': 'mlx-community/whisper-large-v3-mlx'}
    ap = argparse.ArgumentParser()
    ap.add_argument('src'); ap.add_argument('out')
    ap.add_argument('vocab_pos', nargs='?'); ap.add_argument('model_pos', nargs='?')   # the Windows positional form
    ap.add_argument('--vocab'); ap.add_argument('--model')
    ap.add_argument('--from', dest='t0', type=float); ap.add_argument('--to', dest='t1', type=float)
    a = ap.parse_args()
    vocab, model = a.vocab or a.vocab_pos, a.model or a.model_pos or 'turbo'
    src, off, tmp = a.src, 0.0, None
    if a.t0 is not None or a.t1 is not None:
        fd, tmp = tempfile.mkstemp(suffix='.wav', prefix='hear_'); os.close(fd)
        cmd = ['ffmpeg', '-v', 'error', '-y']
        if a.t0 is not None: cmd += ['-ss', '%.3f' % a.t0]
        if a.t1 is not None: cmd += ['-to', '%.3f' % a.t1]
        cmd += ['-i', a.src, '-vn', '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le', tmp]
        subprocess.run(cmd, check=True)
        src, off = tmp, a.t0 or 0.0
    prompt = ' '.join(open(vocab, encoding='utf-8').read().split())[:800] if vocab else None
    t0 = time.time()
    r = mlx_whisper.transcribe(src, path_or_hf_repo=models.get(model, model), language='en', word_timestamps=True,
                               condition_on_previous_text=False, initial_prompt=prompt)
    if tmp: os.remove(tmp)
    res = {'file': a.src, 'duration': None, 'segments': [], 'words': []}
    for s in r.get('segments', []):
        res['segments'].append({'s': round(s['start'] + off, 2), 'e': round(s['end'] + off, 2), 'text': s['text'].strip()})
        for w in s.get('words') or []:
            res['words'].append({'s': round(w['start'] + off, 2), 'e': round(w['end'] + off, 2), 'w': w['word'].strip(),
                                 'p': round(w.get('probability', 0), 2)})
    if res['segments']: res['duration'] = res['segments'][-1]['e'] - off
    json.dump(res, open(a.out, 'w', encoding='utf-8'), indent=0)
    print('done: %d segments, %d words, %.0f s audio in %.0f s' % (len(res['segments']), len(res['words']),
                                                                   res['duration'] or 0, time.time() - t0))
    if (res['duration'] or 0) > 600:   # sanity checks from real failures
        per = collections.Counter(int((w['s'] - off) // 300) for w in res['words'])
        counts = [per.get(i, 0) for i in range(int(res['duration'] // 300) + 1)]
        print('words per 5 min:', counts)
        med = sorted(counts)[len(counts) // 2] if counts else 0
        for i, c in enumerate(counts[:-1]):
            if med and c < 0.25 * med: print('  CHECK block %d-%d min: %d words (median %d): loop or silence?' % (i * 5, i * 5 + 5, c, med))
    run, prev = 1, None
    for s in res['segments']:
        if s['text'] == prev and len(s['text']) < 20:
            run += 1
            if run == 8: print('  CHECK repeated "%s" from %.1f s: decode loop, re-run that region alone' % (s['text'], s['s']))
        else: run, prev = 1, s['text']


if sys.platform == 'darwin':
    import importlib.util
    if importlib.util.find_spec('mlx_whisper') is not None:
        _mac_mlx_main()
        sys.exit(0)

import numpy as np
from faster_whisper import WhisperModel


def load_audio(path, sr=16000):
    """16 kHz mono float32. WAVs at 16 kHz mono load directly; anything else is decoded with PyAV
    (faster-whisper 1.2.1's own decoder passes metadata_errors, which PyAV 19 no longer accepts).
    32-bit float WAVs (raw takes from a DAW) are not PCM to the wave module: they go to PyAV too."""
    if path.lower().endswith('.wav'):
        try:
            w = wave.open(path)
        except wave.Error:
            w = None
        if w is not None:
            with w:
                if w.getframerate() == sr and w.getnchannels() == 1 and w.getsampwidth() == 2:
                    return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
    import av
    out = []
    with av.open(path) as c:
        rs = av.AudioResampler(format='s16', layout='mono', rate=sr)
        for f in c.decode(audio=0):
            for g in rs.resample(f):
                out.append(g.to_ndarray().reshape(-1))
        for g in rs.resample(None):
            out.append(g.to_ndarray().reshape(-1))
    return np.concatenate(out).astype(np.float32) / 32768.0


src, out = sys.argv[1], sys.argv[2]
prompt = None
if len(sys.argv) > 3:
    prompt = ' '.join(open(sys.argv[3], encoding='utf-8').read().split())[:800]
t0 = time.time()
MODEL = sys.argv[4] if len(sys.argv) > 4 else 'large-v3-turbo'   # 'large-v3' = slower, tighter word timings (use for cut points)
model = WhisperModel(MODEL, device='cpu', compute_type='int8', cpu_threads=os.cpu_count() or 4)
segs, info = model.transcribe(load_audio(src), language='en', word_timestamps=True, initial_prompt=prompt, hotwords=prompt,
                              condition_on_previous_text=False, vad_filter=False, beam_size=5)
res = {'file': src, 'duration': info.duration, 'segments': [], 'words': []}
for s in segs:
    res['segments'].append({'s': round(s.start, 2), 'e': round(s.end, 2), 'text': s.text.strip()})
    for w in s.words or []:
        res['words'].append({'s': round(w.start, 2), 'e': round(w.end, 2), 'w': w.word.strip(), 'p': round(w.probability, 2)})
json.dump(res, open(out, 'w', encoding='utf-8'), indent=0)
print('done: %d segments, %d words, %.0f s audio in %.0f s' % (len(res['segments']), len(res['words']), info.duration, time.time() - t0))
