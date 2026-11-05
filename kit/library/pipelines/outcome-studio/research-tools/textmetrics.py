"""Measure on-screen text and pace in short videos (no watching needed).
python -X utf8 textmetrics.py <label> <video.mp4> [<label> <video.mp4> ...]
  or  python -X utf8 textmetrics.py --refs            (every downloaded video in data/refs.jsonl)
For each video:
  - frames at 2 fps for the first 8 s, then 1 fps to 40 s (720 px wide) -> Windows OCR (ocr.ps1)
  - cuts from ffmpeg scene detection (threshold 0.3)
Writes data/textmetrics.jsonl (one summary per video) and prints one line per video.
Metrics: readable text = OCR lines at least 1.8% of frame height tall; tiny text = smaller lines.
"""
import sys, os, json, subprocess, re, statistics, shutil, tempfile

ROOT = os.environ.get("TEXTMETRICS_ROOT") or r"C:\VISION\VISION CLAUDE\outcome\research\raw\26"   # folder holding data/refs.jsonl
DATA = os.path.join(ROOT, "data")
HERE = os.path.dirname(os.path.abspath(__file__))
FF = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.2-full_build\bin")
FFMPEG = shutil.which("ffmpeg") or os.path.join(FF, "ffmpeg.exe")
FFPROBE = shutil.which("ffprobe") or os.path.join(FF, "ffprobe.exe")
WORK = os.path.join(os.environ.get("TEMP", "."), "r26_tm_%d" % os.getpid())
OUT = os.path.join(DATA, "textmetrics.jsonl")


def probe(v):
    o = subprocess.run([FFPROBE, "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height:format=duration", "-of", "json", v], capture_output=True, text=True).stdout
    j = json.loads(o)
    s = j["streams"][0]
    return int(s["width"]), int(s["height"]), float(j["format"]["duration"])


def frames(v, key, dur):
    d = os.path.join(WORK, key)
    if os.path.isdir(d):
        shutil.rmtree(d)
    os.makedirs(d)
    times = [i * 0.5 for i in range(16)] + [float(t) for t in range(8, 41)]
    times = [t for t in times if t < dur - 0.05]
    paths = []
    for t in times:
        p = os.path.join(d, "f%06.2f.png" % t)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-ss", "%.2f" % t, "-i", v, "-frames:v", "1", "-vf", "scale=720:-2", p])
        if os.path.exists(p):
            paths.append((t, p))
    return paths


def cuts(v):
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", v, "-vf", "select='gt(scene,0.3)',showinfo", "-an", "-f", "null", "-"], capture_output=True, text=True)
    return [float(m.group(1)) for m in re.finditer(r"pts_time:([\d.]+)", r.stderr)]


def ocr(paths):
    lst = os.path.join(WORK, "list.txt")
    out = os.path.join(WORK, "ocr.jsonl")
    if os.path.exists(out):
        os.remove(out)
    open(lst, "w", encoding="utf-8").write("\n".join(p for _, p in paths))
    subprocess.run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", os.path.join(HERE, "ocr.ps1"), lst, out], capture_output=True, text=True)
    res = {}
    for l in open(out, encoding="utf-8-sig"):
        try:
            j = json.loads(l)
            res[j["path"]] = j
        except Exception:
            pass
    return res


def words(t):
    return [w for w in re.findall(r"[A-Za-z0-9$%£€.,'!?+\-]+", t) if re.search(r"[A-Za-z0-9]", w)]


def analyse(label, v):
    key = re.sub(r"[^\w.-]", "_", label)[:60]
    W, H, dur = probe(v)
    fr = frames(v, key, dur)
    oc = ocr(fr)
    rows = []
    for t, p in fr:
        j = oc.get(p, {})
        h = j.get("h") or 1
        read, tiny, ys, hs = [], [], [], []
        for ln in j.get("lines", []):
            wl = words(ln.get("text", ""))
            if not wl:
                continue
            if ln["h"] / h >= 0.018:
                read += wl
                ys.append((ln["y"] + ln["h"] / 2) / h)
                hs.append(ln["h"] / h)
            else:
                tiny += wl
        rows.append({"t": t, "read": read, "tiny": len(tiny), "ys": ys, "hs": hs})
    # caption segments: consecutive frames with overlapping readable words
    segs = []
    cur = None
    for r in rows:
        s = set(w.lower() for w in r["read"])
        if not s:
            cur = None
            continue
        if cur and len(s & cur["set"]) / max(1, len(s | cur["set"])) >= 0.5:
            cur["end"] = r["t"]
            cur["set"] |= s
        else:
            cur = {"start": r["t"], "end": r["t"], "set": set(s), "n": len(s)}
            segs.append(cur)
    first8 = [r for r in rows if r["t"] < 8]
    cut = cuts(v)
    med = lambda a: round(statistics.median(a), 3) if a else None
    m = {
        "label": label, "video": v, "w": W, "h": H, "dur": round(dur, 2),
        "frames": len(rows),
        "pct_frames_text": round(100 * sum(1 for r in rows if r["read"]) / max(1, len(rows))),
        "first_text_t": next((r["t"] for r in rows if r["read"]), None),
        "words_per_frame_med": med([len(r["read"]) for r in rows if r["read"]]),
        "words_per_frame_max": max([len(r["read"]) for r in rows] or [0]),
        "tiny_words_per_frame_med": med([r["tiny"] for r in rows]),
        "text_y_med": med([y for r in rows for y in r["ys"]]),
        "text_y_min": round(min([y for r in rows for y in r["ys"]] or [0]), 3),
        "text_y_max": round(max([y for r in rows for y in r["ys"]] or [0]), 3),
        "line_h_med": med([x for r in rows for x in r["hs"]]),
        "segments_first8s": sum(1 for s in segs if s["start"] < 8),
        "segment_len_med": med([round(s["end"] - s["start"] + 0.5, 2) for s in segs]),
        "cuts": len(cut), "cuts_per_10s": round(10 * len(cut) / max(dur, 0.1), 2),
        "first_cut_t": round(cut[0], 2) if cut else None,
        "text_t0": " ".join(rows[0]["read"])[:120] if rows else "",
        "text_samples": [(r["t"], " ".join(r["read"])[:80]) for r in rows if r["read"]][:12],
    }
    with open(OUT, "a", encoding="utf-8") as f:
        f.write(json.dumps(m, ensure_ascii=False) + "\n")
    print("%-34s dur=%5.1f text%%=%3s first=%s wpf=%s max=%s tiny=%s y=%s(%s-%s) lh=%s segs8=%s seglen=%s cuts/10s=%s | t0: %s" % (
        label[:34], dur, m["pct_frames_text"], m["first_text_t"], m["words_per_frame_med"], m["words_per_frame_max"], m["tiny_words_per_frame_med"],
        m["text_y_med"], m["text_y_min"], m["text_y_max"], m["line_h_med"], m["segments_first8s"], m["segment_len_med"], m["cuts_per_10s"], m["text_t0"][:60]))
    shutil.rmtree(os.path.join(WORK, key), ignore_errors=True)
    return m


def main():
    os.makedirs(WORK, exist_ok=True)
    a = sys.argv[1:]
    jobs = []
    if a and a[0] == "--refs":
        done = set()
        if os.path.exists(OUT):
            for l in open(OUT, encoding="utf-8"):
                try:
                    done.add(json.loads(l)["video"])
                except Exception:
                    pass
        seen = {}
        for l in open(os.path.join(DATA, "refs.jsonl"), encoding="utf-8"):
            try:
                r = json.loads(l)
            except Exception:
                continue
            if r.get("video") and os.path.exists(r["video"]):
                seen[r["id"]] = r
        for r in seen.values():
            if r["video"] not in done:
                jobs.append(("%s|%s" % (r["niche"], r["key"]), r["video"]))
        if len(a) > 2:
            keep = set(a[2].split(","))
            jobs = [j for j in jobs if j[0].split("|")[0] in keep]
        if len(a) > 3:
            per = int(a[3])
            byn = {}
            for j in sorted(jobs):
                byn.setdefault(j[0].split("|")[0], []).append(j)
            jobs = [j for v in byn.values() for j in v[:per]]
        if len(a) > 1 and "/" in a[1]:
            k, n = map(int, a[1].split("/"))
            jobs = [j for i, j in enumerate(sorted(jobs)) if i % n == k]
    else:
        jobs = list(zip(a[0::2], a[1::2]))
    for lab, v in jobs:
        try:
            analyse(lab, v)
        except Exception as e:
            print("ERR", lab, str(e)[:100])


main()
