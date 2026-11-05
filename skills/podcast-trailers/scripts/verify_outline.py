#!/usr/bin/env python3
"""
Verify an intro outline against the transcript it was built from.

    python verify_outline.py "<outline.md>" "<transcript>" [--alias "Nadia=Nadja,Nadya"] ... [--search-in FILE]

<transcript>: the Whisper .txt (best), or a .srt / .tsv / .json from transcribe.py, premiere-ae-editing hear.py or
prtranscript.py. Every format is flattened to plain words before comparing.

Speech-to-text routinely misspells proper nouns, and the outline should carry the *correct* spelling. Tell the checker
about each correction with --alias so it compares fairly:

    --alias "Nadia=Nadja,Nadya" --alias "Kaplan=Caplan"

--search-in FILE checks the search phrases against another transcript: the one the editor will actually search. When
the episode sits in a Premiere project that is Premiere's own transcript, exported with premiere-ae-editing
scripts/prproj/prtranscript.py project.prproj words.json. Without it, phrases are checked against <transcript>.

Four checks, in the order they tend to fail:

  1. VERBATIM     every quoted line actually appears in the transcript
  2. UNIQUE       every `search phrase` matches exactly one place
  3. EM DASH      none present (standing rule for every document)
  4. PLACEHOLDER  no TODO / TBD / XX / bracketed stubs left behind

Why normalise so hard: Whisper's .txt has almost no punctuation and inconsistent casing, while the outline is written
with real punctuation. Comparing them raw produces false failures on every line. So both sides are flattened to bare
lowercase words before comparison; that still catches real paraphrasing (changed or reordered words) while ignoring the
punctuation gap.

Quotes may be straight or curly. This file is pure ASCII on purpose: the curly quotes, the ellipsis and the em dash are
built with chr(), so a find-and-replace run over the file cannot switch a check off silently. (The copy this was
adapted from had lost its curly quotes, and its em dash constant was a literal character despite its own comment.)

Exit code is the number of real problems (capped at 125), so it can gate a workflow. Read-only: writes nothing.
"""
import json
import re
import sys
import unicodedata

# Built with chr() rather than literal characters or backslash-u escapes: some file-writing tools decode backslash-u
# escapes into the literal character, which is most likely how the original lost its own em dash constant.
LDQ, RDQ, LSQ, RSQ = chr(0x201C), chr(0x201D), chr(0x2018), chr(0x2019)
QUOTES = '"' + LDQ + RDQ      # straight, left and right double quotes
APOS = "'" + LSQ + RSQ        # straight, left and right single quotes
ELLIPSIS = chr(0x2026)
EM = chr(0x2014)              # em dash


def flatten(s):
    """Lowercase, strip accents and punctuation, collapse whitespace."""
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.replace(RSQ, "'").replace(LSQ, "'")
    s = s.replace(LDQ, '"').replace(RDQ, '"')
    s = s.lower()
    s = re.sub(r"[^a-z0-9' ]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def load_text(path):
    """The spoken text of a transcript file as one string (.txt, .srt, .tsv or .json)."""
    with open(path, encoding="utf-8-sig", errors="replace") as fh:
        raw = fh.read()
    low = path.lower()
    if low.endswith(".json"):
        data = json.loads(raw)
        if isinstance(data, dict):
            if isinstance(data.get("segments"), list):
                return " ".join(str(s.get("text", "")) for s in data["segments"] if isinstance(s, dict))
            if isinstance(data.get("words"), list):
                return " ".join(str(w.get("w", w.get("word", ""))) for w in data["words"] if isinstance(w, dict))
            if "text" in data:
                return str(data["text"])
        if isinstance(data, list):
            if data and isinstance(data[0], dict) and "words" in data[0]:
                # prtranscript.py: one entry per media item; use the biggest transcript
                best = max(data, key=lambda t: len(t.get("words") or []))
                if len(data) > 1:
                    print(f"note: {path} holds {len(data)} transcripts; using the largest "
                          f"(near '{best.get('near_title')}')")
                ws = sorted(best.get("words") or [], key=lambda w: float(w.get("t", 0)))
                return " ".join(str(w.get("w", "")) for w in ws)
            return " ".join(str(s.get("text", "")) for s in data if isinstance(s, dict))
        raise ValueError(f"unrecognised JSON transcript layout in {path}")
    if low.endswith(".srt"):
        keep = []
        for line in raw.splitlines():
            t = line.strip()
            if not t or t.isdigit() or "-->" in t:
                continue
            keep.append(t)
        return " ".join(keep)
    if low.endswith(".tsv"):
        out = []
        for i, line in enumerate(raw.splitlines()):
            parts = line.split("\t")
            if i == 0 and parts[:2] == ["start", "end"]:
                continue
            if len(parts) >= 3:
                out.append("\t".join(parts[2:]))
        return " ".join(out)
    return raw


def fragments(quote):
    """Split a quote on elisions; each side is checked separately."""
    parts = re.split(r"\.{3}|" + ELLIPSIS + r"|\[\.\.\.\]", quote)
    return [p for p in (flatten(x) for x in parts) if len(p.split()) >= 3]


def classify(fragment, transcript_words, transcript_flat):
    """
    Decide how a quoted fragment relates to the source.

      EXACT      appears word for word
      CONDENSED  every word appears in order, with words dropped in between. This is normal trailer editing
                 (stutters, "like", false starts get cut). Fine, but the outline should mark the elision so the
                 editor knows a cut is happening.
      PARAPHRASE words were added, changed or reordered. This is the real error: the phrase does not exist in the
                 footage, so the editor searches for something that was never said.

    Condensation is detected by walking the quote's words through the transcript in order. A window cap keeps a match
    from being satisfied by words scattered across the whole episode.
    """
    if fragment in transcript_flat:
        return "EXACT", None

    words = fragment.split()
    if not words:
        return "EXACT", None

    span_cap = max(60, len(words) * 6)
    start_positions = [i for i, w in enumerate(transcript_words) if w == words[0]]
    for start in start_positions:
        idx = start
        matched = 1
        for w in words[1:]:
            found = None
            for j in range(idx + 1, min(idx + 25, len(transcript_words))):
                if transcript_words[j] == w:
                    found = j
                    break
            if found is None:
                break
            idx = found
            matched += 1
        if matched == len(words) and (idx - start) <= span_cap:
            dropped = (idx - start + 1) - len(words)
            return "CONDENSED", dropped

    # how far does it match, to help diagnose
    for n in range(len(words), 2, -1):
        probe = " ".join(words[:n])
        if probe in transcript_flat:
            return "PARAPHRASE", probe
    return "PARAPHRASE", None


def main():
    for stream in (sys.stdout, sys.stderr):
        try:
            stream.reconfigure(encoding="utf-8", errors="replace")   # Windows consoles default to cp1252
        except (AttributeError, ValueError):
            pass

    args = sys.argv[1:]
    aliases, positional, search_in = {}, [], None
    i = 0
    while i < len(args):
        a = args[i]
        if a == "--alias" and i + 1 < len(args):
            spec = args[i + 1]
            if "=" in spec:
                correct, variants = spec.split("=", 1)
                aliases[flatten(correct)] = [flatten(v) for v in variants.split(",") if v.strip()]
            i += 2
        elif a == "--search-in" and i + 1 < len(args):
            search_in = args[i + 1]
            i += 2
        elif a in ("-h", "--help"):
            print(__doc__)
            return 2
        else:
            positional.append(a)
            i += 1

    if len(positional) < 2:
        print(__doc__)
        return 2

    outline_path, transcript_path = positional[0], positional[1]
    try:
        with open(outline_path, encoding="utf-8-sig", errors="replace") as fh:
            outline = fh.read()
        transcript = flatten(load_text(transcript_path))
        # Search phrases are checked against the UN-aliased text, because the editor types them into an NLE that
        # transcribed the same audio. A phrase should carry the spelling the machine will actually find, even when the
        # prose above it carries the corrected human spelling.
        search_text = flatten(load_text(search_in)) if search_in else transcript
    except (OSError, ValueError) as err:
        print(f"cannot read input: {err}")
        return 2

    # Rewrite the transcript's misspellings to the outline's corrected forms so a deliberate name fix does not read as
    # a paraphrase. A function replacement keeps the corrected text literal.
    for correct, variants in aliases.items():
        for v in variants:
            if v:
                transcript = re.sub(r"\b" + re.escape(v) + r"\b", lambda _m, c=correct: c, transcript)
    if aliases:
        shown = ", ".join(f"{v[0]}...->{k}" for k, v in aliases.items() if v)
        print(f"aliases applied: {shown}")

    problems = 0
    transcript_words = transcript.split()
    print(f"outline    {outline_path}")
    print(f"transcript {transcript_path}  ({len(transcript_words):,} words)")
    if search_in:
        print(f"search in  {search_in}  ({len(search_text.split()):,} words)")
    print()

    # ---- 1. verbatim ------------------------------------------------------------------------------------------------
    # Quoted speech in the inline form: **Speaker:** "...." (straight or curly quotes). Voice-over is written copy, not
    # something anyone said on the episode, so it is excluded: checking it against the transcript would always fail.
    narration = re.compile(r"\b(VO|V\.O\.|voice[- ]?over|narration|narrator|title card)\b", re.I)
    q_open = "[" + QUOTES + "]"
    q_body = "[^" + QUOTES + "]"
    inline = re.compile(r"\*\*([^*]+):\*\*\s*" + q_open + "(" + q_body + "{12,})" + q_open)
    quotes = [q for label, q in inline.findall(outline) if not narration.search(label)]

    # Scene-script format: a bold speaker header opens a block, for example
    #     **GUEST NAME** *(50:23-50:27, 51:07-51:13)*
    # and the lines under it are bare quotes, one stacked line per thought. "VO:" blocks are narration (not tape) and
    # their lines are unquoted, so they are skipped. Bracketed production directions and Search lines do not end a
    # block; a markdown heading does.
    header = re.compile(r"^\*\*([A-Z][A-Z0-9 ." + APOS + r"-]*):?\*\*")
    bare = re.compile(r"^[-*]?\s*" + q_open + r"(.{12,})" + q_open + r"\s*$")
    context = None
    for raw in outline.splitlines():
        s = raw.strip()
        if re.match(r"^#+\s", s):
            context = None
            continue
        m = header.match(s)
        if m:
            context = "vo" if narration.search(m.group(1)) else "speaker"
            continue
        if re.match(r"^(VO|VOICEOVER)\s*:?\s*$", s, re.I):
            context = "vo"
            continue
        if re.match(r"^\[.*\]$", s) or re.match(r"^Search:", s):
            continue
        qm = bare.match(s)
        if qm and context == "speaker":
            quotes.append(qm.group(1))

    print(f"[1] VERBATIM  {len(quotes)} quoted lines")
    if not quotes:
        print("    ! found no quoted lines: check the outline's quote format")
        problems += 1
    condensed_n = 0
    for q in quotes:
        label = (q[:62] + "...") if len(q) > 62 else q
        frags = fragments(q)
        verdicts = [classify(f, transcript_words, transcript) for f in frags]
        kinds = [v[0] for v in verdicts]
        if "PARAPHRASE" in kinds:
            problems += 1
            print(f'    FAIL  "{label}"')
            for (kind, info), frag in zip(verdicts, frags):
                if kind == "PARAPHRASE":
                    if info:
                        print(f'          not in transcript past: "{info[:58]}"')
                    else:
                        print(f'          not in transcript at all: "{frag[:58]}"')
        elif "CONDENSED" in kinds:
            condensed_n += 1
            drop = sum(v[1] or 0 for v in verdicts if v[0] == "CONDENSED")
            print(f'    trim  "{label}"  ({drop} words cut: mark the elision)')
        else:
            print(f'    ok    "{label}"')
    if condensed_n:
        print(f"    {condensed_n} line(s) condensed. Allowed (that is the edit),")
        print("    but show the cut with '...' so the client sees it.")
    print()

    # ---- 2. search phrase uniqueness ------------------------------------------------------------------------------
    # Counted as substrings of the flattened text on purpose: an NLE's transcript search also finds a phrase inside a
    # longer word run, so a phrase that occurs inside another one would land the editor in the wrong place.
    phrases = []
    for line in outline.splitlines():
        if re.match(r"\s*Search:", line) or ("`" in line and "Search" in line):
            phrases += re.findall(r"`([^`]+)`", line)
    phrases = [p for p in phrases if len(p.split()) >= 2]
    print(f"[2] UNIQUE    {len(phrases)} search phrases")
    for p in phrases:
        n = search_text.count(flatten(p))
        if n == 1:
            print(f"    ok    `{p}`")
        elif n == 0:
            problems += 1
            print(f"    FAIL  `{p}`  not in the transcript")
        else:
            problems += 1
            print(f"    FAIL  `{p}`  appears {n}x, the editor will land in the wrong place")
    print()

    # ---- 3. em dashes -------------------------------------------------------------------------------------------------
    em = [(n + 1, line.strip()) for n, line in enumerate(outline.splitlines()) if EM in line]
    print(f"[3] EM DASH   {len(em)} found")
    for ln, text in em:
        problems += 1
        print(f"    FAIL  line {ln}: {text[:78]}")
    if not em:
        print("    ok    none")
    print()

    # ---- 4. placeholders ----------------------------------------------------------------------------------------------
    pat = re.compile(r"\bTODO\b|\bTBD\b|\bFIXME\b|\bXX+\b|\[name\]|\[guest\]|<[a-z ]+>", re.I)
    holes = [(n + 1, line.strip()) for n, line in enumerate(outline.splitlines()) if pat.search(line)]
    print(f"[4] PLACEHOLDER  {len(holes)} found")
    for ln, text in holes:
        problems += 1
        print(f"    FAIL  line {ln}: {text[:78]}")
    if not holes:
        print("    ok    none")

    print()
    print("=" * 60)
    if problems:
        print(f"{problems} problem(s): fix before this goes to the client")
    else:
        print("clean: safe to send")
    return problems


if __name__ == "__main__":
    sys.exit(min(main(), 125))
