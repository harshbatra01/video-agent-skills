#!/usr/bin/env python3
"""
Print an episode as timecoded windows at beat size, ready for picking trailer scenes.

    python find_passages.py "<transcript>" [--seconds 35] [--from 0] [--to 999]

<transcript> can be:
  .srt / .tsv   Whisper output (transcribe.py writes both)
  .json         premiere-ae-editing hear.py output ({"segments": [{"s", "e", "text"}]}),
                WhisperX or Whisper JSON ({"segments": [{"start", "end", "text"}]}),
                Premiere's own transcript from prtranscript.py ([{"words": [{"t", "d", "w"}]}]),
                or a plain list of {"start", "end", "text"} segments in seconds
--from / --to are minutes. --seconds is the window length.

Why this exists: neither transcript format is the right shape for picking beats. The .txt has no timecodes, so every
quote you like turns into a hunt for where it was. The .srt has the opposite problem: a 78 minute episode is about 1000
fragments of 4 seconds each, far shorter than anything you would cut. This regroups the episode into windows about as
long as a trailer beat, each stamped with the timecode you need for the outline.

What it does NOT do: find the good passages for you. Whisper emits segments back to back with no silence between them
(in one 78 minute episode, 932 of 976 gaps were exactly zero), so there is no timing signal for where one person stops
and another starts, and no speaker labels. Judging which stretch is one whole thought is reading work. Look for runs
where one person holds the floor and says something complete; those become the middle scenes (rule 2 in SKILL.md).
Always confirm the exact wording against the .txt before quoting, since the text here is joined from segments.

Read-only: it prints to the screen and writes nothing.
"""
import csv
import json
import re
import sys


def tc(ms):
    s = int(ms) // 1000
    return f"{s // 60}:{s % 60:02d}"


def read_srt(path):
    """[(start_ms, end_ms, text)] from SRT. Keeps every text line of a cue, not just the first."""
    pat = re.compile(
        r"(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})\s*-+>\s*(\d{1,2}):(\d{2}):(\d{2})[,.](\d{3})"
    )

    def ms(h, m, s, milli):
        return ((int(h) * 60 + int(m)) * 60 + int(s)) * 1000 + int(milli)

    rows, pending, text = [], None, []
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        for line in fh:
            line = line.strip()
            m = pat.search(line)
            if m:
                if pending and text:
                    rows.append((pending[0], pending[1], " ".join(text)))
                g = m.groups()
                pending, text = (ms(*g[:4]), ms(*g[4:])), []
                continue
            if pending and line and not line.isdigit():
                text.append(line)
    if pending and text:
        rows.append((pending[0], pending[1], " ".join(text)))
    return rows


def read_tsv(path):
    """[(start_ms, end_ms, text)] from a Whisper .tsv (start and end in milliseconds)."""
    rows = []
    with open(path, encoding="utf-8-sig", errors="replace", newline="") as fh:
        # QUOTE_NONE: Whisper does not quote fields, and a line starting with a quote mark must stay text
        for r in csv.DictReader(fh, delimiter="\t", quoting=csv.QUOTE_NONE):
            try:
                rows.append((int(float(r["start"])), int(float(r["end"])), (r.get("text") or "").strip()))
            except (KeyError, ValueError, TypeError):
                continue
    return rows


def _seg_from_words(words):
    return (int(round(words[0][0] * 1000)), int(round(words[-1][1] * 1000)), " ".join(w[2] for w in words))


def read_json(path):
    """[(start_ms, end_ms, text)] from hear.py, Whisper/WhisperX, prtranscript.py or a plain segment list."""
    with open(path, encoding="utf-8-sig") as fh:
        data = json.load(fh)
    rows = []
    if isinstance(data, dict) and isinstance(data.get("segments"), list):
        for s in data["segments"]:
            st, en = s.get("s", s.get("start")), s.get("e", s.get("end"))
            if st is None or en is None:
                continue
            rows.append((int(round(float(st) * 1000)), int(round(float(en) * 1000)), str(s.get("text", "")).strip()))
        return rows
    if isinstance(data, list) and data and isinstance(data[0], dict) and "words" in data[0]:
        # prtranscript.py: one entry per media item in the project; use the biggest transcript
        best = max(data, key=lambda t: len(t.get("words") or []))
        if len(data) > 1:
            print(f"note: {len(data)} transcripts in this file; using the largest "
                  f"({len(best.get('words') or [])} words, near '{best.get('near_title')}')", file=sys.stderr)
        cur = []
        for w in sorted(best.get("words") or [], key=lambda w: float(w.get("t", 0))):
            st = float(w.get("t", 0))
            en = st + float(w.get("d", 0))
            if cur:
                gap, span = st - cur[-1][1], en - cur[0][0]
                if gap > 0.6 or span > 12 or (span > 6 and cur[-1][2].endswith((".", "?", "!"))):
                    rows.append(_seg_from_words(cur))
                    cur = []
            cur.append((st, en, str(w.get("w", "")).strip()))
        if cur:
            rows.append(_seg_from_words(cur))
        return rows
    if isinstance(data, list):
        for s in data:
            if not isinstance(s, dict):
                continue
            st, en = s.get("start", s.get("s")), s.get("end", s.get("e"))
            if st is None or en is None:
                continue
            rows.append((int(round(float(st) * 1000)), int(round(float(en) * 1000)), str(s.get("text", "")).strip()))
        return rows
    raise ValueError("unrecognised JSON transcript layout")


def read_segments(path):
    low = path.lower()
    if low.endswith(".srt"):
        return read_srt(path)
    if low.endswith(".json"):
        return read_json(path)
    return read_tsv(path)


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to cp1252
        except (AttributeError, ValueError):
            pass

    args = list(sys.argv[1:] if argv is None else argv)
    if not args or args[0] in ("-h", "--help"):
        print(__doc__)
        return 2
    path, rest = args[0], args[1:]

    def opt(flag, default):
        if flag in rest:
            try:
                return type(default)(rest[rest.index(flag) + 1])
            except (IndexError, ValueError):
                pass
        return default

    window = opt("--seconds", 35.0)
    t_from = opt("--from", 0.0) * 60_000
    t_to = opt("--to", 9999.0) * 60_000

    try:
        rows = read_segments(path)
    except (OSError, ValueError) as err:
        print(f"cannot read {path}: {err}")
        return 2
    if not rows:
        print(f"no usable segments in {path}: expected a Whisper .srt / .tsv or a transcript .json")
        return 2

    rows.sort(key=lambda r: r[0])
    rows = [r for r in rows if r[1] >= t_from and r[0] <= t_to]
    if not rows:
        print("no segments in that time range")
        return 2

    # group consecutive segments until the window length is reached, preferring to close on what looks like the end
    # of a sentence
    chunks, cur = [], [rows[0]]
    for seg in rows[1:]:
        span = (seg[1] - cur[0][0]) / 1000.0
        ends_clean = cur[-1][2].rstrip().endswith((".", "?", "!"))
        if span >= window and (ends_clean or span >= window * 1.6):
            chunks.append(cur)
            cur = [seg]
        else:
            cur.append(seg)
    chunks.append(cur)

    total_min = (rows[-1][1] - rows[0][0]) / 60000.0
    print(f"{len(chunks)} windows of ~{window:.0f}s across {total_min:.0f} min ({len(rows)} source segments)")
    print("=" * 74)
    for c in chunks:
        start, end = c[0][0], c[-1][1]
        text = re.sub(r"\s+", " ", " ".join(s[2] for s in c)).strip()
        print(f"\n[{tc(start)}]  {(end - start) / 1000:.0f}s")
        print(f"  {text}")

    print()
    print("=" * 74)
    print("Look for a window where one person says a whole thought without being")
    print("interrupted. Those are the beats. Confirm wording against the .txt.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
