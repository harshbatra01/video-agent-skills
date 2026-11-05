#!/usr/bin/env python3
"""
Transcribe a podcast episode (or any long recording) for outline work, on a Mac or a Windows PC.
Replaces the Mac-only transcribe.sh of the original skill.

    python transcribe.py "<audio or video>" ["<output dir>"] [options]

Writes <name>.txt, <name>.tsv and <name>.srt (by default next to the audio):
  .txt  one segment per line: read it, search it
  .tsv  start ms / end ms / text: the most compact source for timecodes (the same layout as Whisper's own .tsv)
  .srt  timecoded, for pulling a specific moment
A window run (--start / --dur / --slow) writes <name>_<start>s.* with its times already shifted to the full episode.

Backends ("--backend auto" takes the first one installed, in this order):
  mlx      mlx-whisper on Apple Silicon Macs: the Python package, or the mlx_whisper command (also looked for in
           ~/.venvs/mlx-whisper/bin). Default model mlx-community/whisper-large-v3-turbo.
  faster   faster-whisper on Windows, Linux or any Mac CPU, CUDA with --device cuda. Default model large-v3-turbo.
           The same engine as premiere-ae-editing scripts/media/hear.py.
  whisper  the openai-whisper command line. Default model base.en (slow and rough).

Options:
  --backend auto|mlx|faster|whisper
  --model NAME        a model name or a Hugging Face repo id (default per backend, above)
  --language en       the spoken language, or "auto" to let the model detect it (default en)
  --device cpu|cuda   faster-whisper only (default cpu)
  --names FILE        names the model must spell (any separator), used as hotwords on every window; faster-whisper only
  --start SEC --dur SEC   transcribe one window only (a hard name, a decode loop); about 25 s is enough
  --slow 0.75         slow the window down first (needs ffmpeg); times are mapped back to the original

Rules carried over from real episodes:
  - condition-on-previous-text is always off: long recordings otherwise fall into repetition loops.
  - No word timestamps on whole episodes: they once dropped about two thirds of the speech. Take word timings only for
    the passages you cut (premiere-ae-editing scripts/media/hear.py) and snap the cuts with speech_cuts.py.
  - After a full run this prints words per 5 minutes. A conversation runs about 900 to 1,100; a sudden drop, or the
    same line repeated, means a decode loop: re-run that stretch with --start / --dur.
  - Names come out wrong reliably: verify every proper noun outside the transcript (SKILL.md step 2).

Needs ffmpeg on PATH or the PyAV package to decode audio, numpy, and one backend. Installing any of them is the user's
call: say the name, the source and the size first. Model weights download on the first run (about 1.6 GB for
large-v3-turbo). CUDA on Windows needs the NVIDIA wheels (pip install nvidia-cublas-cu12 "nvidia-cudnn-cu12==9.*");
this script adds their DLL folders itself and uses float16, because int8 fails on RTX 50 cards.
"""
import argparse
import importlib.util
import json
import os
import platform
import re
import shutil
import subprocess
import sys
import tempfile
import time
import unicodedata
import wave
from pathlib import Path

SR = 16000
DEFAULT_MODEL = {"mlx": "mlx-community/whisper-large-v3-turbo", "faster": "large-v3-turbo", "whisper": "base.en"}
NO_BACKEND = """no speech-to-text backend found. Ask the user before installing one (say the name, source and size):
  Mac with Apple Silicon: pip install mlx-whisper   (in a venv)
  Windows or any PC:      pip install faster-whisper   (the engine premiere-ae-editing hear.py uses)
Or transcribe inside Premiere (Text panel, Transcribe) and read it with premiere-ae-editing scripts/prproj/prtranscript.py."""


def say(*parts):
    print(*parts, file=sys.stderr, flush=True)


def fix_console():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to cp1252
        except (AttributeError, ValueError):
            pass


def fmt(t):
    t = int(t)
    h, rest = divmod(t, 3600)
    m, s = divmod(rest, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"


# ---- finding the file -------------------------------------------------------------------------------------------------

def norm_name(name):
    """A file name as a person reads it: NFKC folds no-break and narrow spaces into plain spaces; case is ignored."""
    s = unicodedata.normalize("NFKC", name)
    s = re.sub(r"\s+", " ", s)
    return s.casefold().strip()


def find_input(path):
    """WhatsApp and some exporters put U+202F (a narrow no-break space) in file names, so a typed path misses.
    Look in the same folder for a name that differs only in such spaces or in case. Refuse when several match, so a
    similar-looking file is never transcribed by mistake."""
    p = Path(path)
    if p.is_file():
        return p
    folder = p.parent
    if not folder.is_dir():
        return None
    want = norm_name(p.name)
    hits = [c for c in folder.iterdir() if c.is_file() and norm_name(c.name) == want]
    if len(hits) == 1:
        say(f"not found at that exact path; matched: {hits[0]}")
        return hits[0]
    if len(hits) > 1:
        say("several files match that name; pass the exact path:")
        for h in hits:
            say("  ", h)
    return None


# ---- audio ------------------------------------------------------------------------------------------------------------

def load_audio(path, start=None, dur=None, slow=None):
    """16 kHz mono float32 samples. ffmpeg when it is on PATH (fast seeking, atempo), else PyAV."""
    import numpy as np
    ff = shutil.which("ffmpeg")
    if ff:
        cmd = [ff, "-nostdin", "-v", "error"]
        if start is not None:
            cmd += ["-ss", f"{start:.3f}"]
        if dur is not None:
            cmd += ["-t", f"{dur:.3f}"]
        cmd += ["-i", str(path), "-vn", "-sn", "-dn"]
        if slow:
            cmd += ["-filter:a", f"atempo={slow:g}"]
        cmd += ["-ac", "1", "-ar", str(SR), "-acodec", "pcm_s16le", "-f", "s16le", "-"]
        raw = subprocess.run(cmd, stdout=subprocess.PIPE, check=True).stdout
        return np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if slow:
        raise SystemExit("--slow needs ffmpeg on PATH")
    try:
        import av
    except ImportError:
        raise SystemExit("needs ffmpeg on PATH or the PyAV package to decode audio")
    chunks, first, got = [], None, 0
    need = int(round(dur * SR)) if dur else None
    with av.open(str(path)) as container:
        stream = container.streams.audio[0]
        if start:
            container.seek(int(start * 1_000_000))   # microseconds; lands at or before the start
        resampler = av.AudioResampler(format="s16", layout="mono", rate=SR)
        for frame in container.decode(stream):
            if first is None:
                first = float(frame.time or 0.0)
            for out in resampler.resample(frame):
                a = out.to_ndarray().reshape(-1)
                chunks.append(a)
                got += len(a)
            if need is not None and got >= need + int(max(0.0, (start or 0.0) - first) * SR) + SR:
                break
        for out in resampler.resample(None):
            chunks.append(out.to_ndarray().reshape(-1))
    x = np.concatenate(chunks) if chunks else np.zeros(0, dtype=np.int16)
    if start and first is not None:
        x = x[max(0, int(round((start - first) * SR))):]
    if need is not None:
        x = x[:need]
    return x.astype(np.float32) / 32768.0


def write_wav(path, audio):
    import numpy as np
    pcm = (np.clip(audio, -1.0, 1.0) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ---- backends ---------------------------------------------------------------------------------------------------------

def has_module(name):
    try:
        return importlib.util.find_spec(name) is not None
    except (ImportError, ValueError):
        return False


def mlx_cli():
    exe = shutil.which("mlx_whisper")
    if exe:
        return exe
    cand = Path.home() / ".venvs" / "mlx-whisper" / "bin" / "mlx_whisper"
    return str(cand) if cand.is_file() and os.access(cand, os.X_OK) else None


def pick_backend(want):
    apple = platform.system() == "Darwin" and platform.machine() == "arm64"
    avail = {
        "mlx": apple and (has_module("mlx_whisper") or mlx_cli() is not None),
        "faster": has_module("faster_whisper"),
        "whisper": shutil.which("whisper") is not None,
    }
    if want != "auto":
        if not avail[want]:
            raise SystemExit(f"backend '{want}' is not available on this machine\n{NO_BACKEND}")
        return want
    for name in ("mlx", "faster", "whisper"):
        if avail[name]:
            return name
    raise SystemExit(NO_BACKEND)


def mlx_repo(model):
    """mlx models live on Hugging Face under mlx-community; pass a full repo id when a name differs."""
    if "/" in model:
        return model
    m = model.lower()
    if m in ("turbo", "large-v3-turbo"):
        return "mlx-community/whisper-large-v3-turbo"
    return f"mlx-community/whisper-{m}-mlx"


def run_cli(exe, audio, src, model, language, workdir, whole_file, dashes):
    """mlx_whisper and openai-whisper share their flags; mlx spells them with dashes, whisper with underscores."""
    flag = (lambda f: "--" + f.replace("_", "-")) if dashes else (lambda f: "--" + f)
    with tempfile.TemporaryDirectory(dir=str(workdir)) as tmp:
        if whole_file:
            inp = str(src)
        else:
            inp = os.path.join(tmp, "window.wav")
            write_wav(inp, audio)
        cmd = [exe, inp, flag("model"), model, flag("output_format"), "json", flag("output_dir"), tmp,
               flag("verbose"), "False", flag("condition_on_previous_text"), "False"]
        if language:
            cmd += [flag("language"), language]
        subprocess.run(cmd, check=True)
        with open(os.path.join(tmp, Path(inp).stem + ".json"), encoding="utf-8") as fh:
            data = json.load(fh)
    return [(float(s["start"]), float(s["end"]), str(s["text"]).strip()) for s in data.get("segments", [])]


def run_mlx(audio, src, model, language, workdir, whole_file):
    repo = mlx_repo(model)
    lang = None if language == "auto" else language
    if has_module("mlx_whisper"):
        import mlx_whisper
        opts = {"path_or_hf_repo": repo, "condition_on_previous_text": False, "verbose": None}
        if lang:
            opts["language"] = lang
        result = mlx_whisper.transcribe(audio, **opts)
        return [(float(s["start"]), float(s["end"]), str(s["text"]).strip()) for s in result.get("segments", [])]
    return run_cli(mlx_cli(), audio, src, repo, lang, workdir, whole_file, dashes=True)


def add_nvidia_dlls():
    """Windows: faster-whisper on CUDA needs the cuBLAS and cuDNN DLLs of the nvidia-* pip wheels on the DLL path."""
    if os.name != "nt":
        return
    import site
    roots = []
    try:
        roots += list(site.getsitepackages())
    except AttributeError:
        pass
    roots.append(site.getusersitepackages())
    for root in roots:
        base = Path(root) / "nvidia"
        if not base.is_dir():
            continue
        for b in base.glob("*/bin"):
            try:
                os.add_dll_directory(str(b))
            except (OSError, AttributeError):
                pass
            os.environ["PATH"] = str(b) + os.pathsep + os.environ.get("PATH", "")


def run_faster(audio, model, language, device, names):
    if device == "cuda":
        add_nvidia_dlls()
    from faster_whisper import WhisperModel
    compute = "float16" if device == "cuda" else "int8"
    whisper = WhisperModel(model, device=device, compute_type=compute, cpu_threads=os.cpu_count() or 4)
    opts = {"language": None if language == "auto" else language, "condition_on_previous_text": False,
            "vad_filter": False, "beam_size": 5}
    if names:
        opts["hotwords"] = names
    try:
        segments, _info = whisper.transcribe(audio, **opts)
    except TypeError:
        if "hotwords" not in opts:
            raise
        say("note: this faster-whisper has no hotwords option; running without the names list")
        opts.pop("hotwords")
        segments, _info = whisper.transcribe(audio, **opts)
    return [(float(s.start), float(s.end), s.text.strip()) for s in segments]


# ---- outputs ----------------------------------------------------------------------------------------------------------

def ts_srt(t):
    ms = int(round(t * 1000))
    h, ms = divmod(ms, 3_600_000)
    m, ms = divmod(ms, 60_000)
    s, ms = divmod(ms, 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"


def write_outputs(segs, base):
    """Write .txt, .tsv and .srt for segs = [(start_s, end_s, text)]. base is the path without an extension."""
    def out(ext):
        return Path(str(base) + ext)   # not with_suffix: names such as "Show x Guest 1.5" keep their dots

    with open(out(".txt"), "w", encoding="utf-8", newline="\n") as fh:
        for _s, _e, text in segs:
            fh.write(text + "\n")
    with open(out(".tsv"), "w", encoding="utf-8", newline="\n") as fh:
        fh.write("start\tend\ttext\n")
        for s, e, text in segs:
            fh.write(f"{round(s * 1000)}\t{round(e * 1000)}\t{text.replace(chr(9), ' ')}\n")
    with open(out(".srt"), "w", encoding="utf-8", newline="\n") as fh:
        for i, (s, e, text) in enumerate(segs, 1):
            fh.write(f"{i}\n{ts_srt(s)} --> {ts_srt(e)}\n{text.replace('-->', '->')}\n\n")
    return [out(x) for x in (".txt", ".tsv", ".srt")]


def health(segs, every=300):
    """Words per 5-minute bin, flagging bins far under the median, repeated lines (decode loops) and an invented
    closing "Thank you." over music. Returns the list of warnings."""
    warnings = []
    if not segs:
        say("no speech found")
        return ["no speech found"]
    bins = {}
    for s, _e, text in segs:
        k = int(s // every)
        bins[k] = bins.get(k, 0) + len(text.split())
    last = max(bins)
    complete = [bins.get(i, 0) for i in range(last)]   # the last bin is usually partial
    median = sorted(complete)[len(complete) // 2] if complete else 0
    say("words per 5 min (a conversation runs about 900 to 1,100):")
    for i in range(last + 1):
        n = bins.get(i, 0)
        flag = ""
        if i < last and median and n < 0.5 * median:
            flag = "  <- LOW: a decode loop or a long silence? re-run this stretch with --start/--dur"
            warnings.append(f"low word count at {i * every // 60}-{(i + 1) * every // 60} min")
        say(f"  {i * every // 60:4d}-{(i + 1) * every // 60:<4d} min  {n:5d}{flag}")
    run, prev, run_start = 0, None, 0.0

    def report(count, at):
        msg = f"REPEAT: the same line {count}x from {fmt(at)}: likely a decode loop, re-run that window"
        say("  " + msg)
        warnings.append(msg)

    for s, _e, text in segs:
        key = re.sub(r"\W+", " ", text.lower()).strip()
        if key and key == prev:
            run += 1
        else:
            if run >= 2:
                report(run + 1, run_start)
            run, prev, run_start = 0, key, s
    if run >= 2:
        report(run + 1, run_start)
    tail = re.sub(r"[^a-z ]", "", segs[-1][2].lower()).strip()
    if tail in ("thank you", "thanks for watching", "thank you for watching", "thank you so much"):
        msg = f"CHECK: the last line '{segs[-1][2]}' at {fmt(segs[-1][0])} may be invented over closing music"
        say("  " + msg)
        warnings.append(msg)
    return warnings


# ---- main -------------------------------------------------------------------------------------------------------------

def main():
    fix_console()
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter,
                                 usage="%(prog)s AUDIO [OUTDIR] [options]")
    ap.add_argument("audio")
    ap.add_argument("outdir", nargs="?")
    ap.add_argument("--backend", choices=["auto", "mlx", "faster", "whisper"], default="auto")
    ap.add_argument("--model")
    ap.add_argument("--language", default="en")
    ap.add_argument("--device", choices=["cpu", "cuda"], default="cpu")
    ap.add_argument("--names")
    ap.add_argument("--start", type=float)
    ap.add_argument("--dur", type=float)
    ap.add_argument("--slow", type=float)
    a = ap.parse_args()
    if a.slow is not None and not 0.5 <= a.slow <= 2.0:
        ap.error("--slow must be between 0.5 and 2.0")

    src = find_input(a.audio)
    if src is None:
        say(f"ERROR: cannot find {a.audio}")
        return 1
    outdir = Path(a.outdir) if a.outdir else src.parent
    outdir.mkdir(parents=True, exist_ok=True)

    backend = pick_backend(a.backend)
    model = a.model or DEFAULT_MODEL[backend]
    if model.endswith(".en") and a.language not in ("en", "auto"):
        say(f"note: {model} is an English-only model; pass --model to read {a.language}")
    names = None
    if a.names:
        names = " ".join(Path(a.names).read_text(encoding="utf-8-sig").split())[:800]
        if backend != "faster":
            say("note: --names works with faster-whisper only, so it is ignored here (a names list used as a prompt "
                "once hallucinated the names into the opening seconds)")
            names = None

    window = a.start is not None or a.dur is not None or a.slow is not None
    stem = src.stem + (f"_{int(a.start or 0)}s" if window else "") + ("_slow" if a.slow else "")
    use_array = window or backend == "faster" or (backend == "mlx" and has_module("mlx_whisper"))

    t0 = time.time()
    audio = load_audio(src, a.start, a.dur, a.slow) if use_array else None
    length = f" ({fmt(len(audio) / SR)} of audio)" if audio is not None else ""
    say(f"transcribing {src.name}{length} with {backend} / {model}")

    if backend == "faster":
        segs = run_faster(audio, model, a.language, a.device, names)
    elif backend == "mlx":
        segs = run_mlx(audio, src, model, a.language, outdir, whole_file=not window)
    else:
        lang = None if a.language == "auto" else a.language
        segs = run_cli(shutil.which("whisper"), audio, src, model, lang, outdir, whole_file=not window, dashes=False)

    if window:   # map window times back to the full episode
        k, off = (a.slow or 1.0), (a.start or 0.0)
        segs = [(off + s * k, off + e * k, t) for s, e, t in segs]
    segs = [(s, e, t) for s, e, t in segs if t]

    files = write_outputs(segs, outdir / stem)
    say(f"\ndone in {time.time() - t0:.0f} s: {len(segs)} segments")
    for f in files:
        say(f"  {f}")
    if window:
        say("window run: the times are already shifted to the full episode")
    else:
        health(segs)
    say("next: verify every proper noun outside the transcript (SKILL.md step 2)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
