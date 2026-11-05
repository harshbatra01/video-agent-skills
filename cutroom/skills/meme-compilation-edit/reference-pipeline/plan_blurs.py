"""Automatic house-style blur plan for one meme.

Given the meme's OCR lines and the narrator's timed words for that meme, returns:
  blocks: content text blocks with the time each is first read
  blurs:  wipe / box / curse specs with raw-time anchors (same shapes build_edl expects)
Rules (the reference house style + the reviewer's rules, Sep 29 2026):
  - the first block he reads keeps its first line visible; the rest of that block is wiped as he reads it
    (block of 3+ lines whose wipe is the meme's first reveal -> the wipe starts when the meme appears)
  - every block read later gets a snap reveal (40 -> 0 in 0.4 s) when he starts reading it
  - text he never reads is left alone
  - any word against YouTube guidelines gets a tight curse blur
"""
import re, difflib, os

UI_PATTERNS = [
    r"^@\w+\s*([·•.].*)?$", r"@\w+\s*[·•.]", r"View \d+ (more )?repl", r"^X\.com$", r"\b\d{1,2}:\d{2}\s*(AM|PM)\b",
    r"\d[\d.,]*\s*[KkMm]?\s*(Views|Reposts?|Retweets?|Likes|Quotes?|Repl(y|ies)|Bookmarks?|Comments?)\b",
    r"^(Views|Reposts|Likes|Quotes|Replies)$", r"^Follow$", r"^Subscribe$", r"Show this thread", r"Replying to",
    r"^Relevant", r"View quotes", r"Translate post", r"\breposted\b", r"^Pinned", r"Show more", r"^\d+(\.\d+)?[KkMm]?$",
    r"^[·•]\s*\d+[hdm]$", r"^\d+[hdm]$", r"^(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d", r"Copy link",
    r"^[-@]?[\w.]+\s+[·•]?\s*\d+[smhdw]$", r"^Read \d+ replies", r"^Follow\b", r"^(Reply|Responder|Antworten|Vote|Share)$", r"[•·]\s*(Creator|Author)\b", r"^X$", r"^\.\.\.$", r"^…$", r"Translated from", r"Show original", r"^Replying to",
]
UI_RE = re.compile("|".join(UI_PATTERNS), re.I)

CURSE_RE = re.compile(
    # The reviewer's rule: blur any word against YouTube guidelines, mild profanity included (crap, deadass),
    # sexual terms, slurs, self-harm and severe-violence terms; figurative words like "killing" or "died" stay.
    r"(fuck|shit|bitch|b\*tch|^ass$|^asses$|asshole|dumbass|deadass|badass|jackass|smartass|^damn|goddamn|^hell$|"
    r"^crap|^piss|^dick|^cock$|pussy|cunt|bastard|whore|^slut|^wtf$|^tf$|^stfu$|^mfs?$|motherf|bullshit|^prick|twat|wanker|"
    r"douche|retard|^sex$|^sexual|porn|^nude|naked|horny|boob|^thot|testicle|^twink|suicid|murder|^execut(e|ed|es|ing|ion|ions|ioner)$|^rape|terroris|"
    r"cocaine|^meth$|heroin|^nazi|hitler|^[il]mf?ao|nigg|ni\*g|n\*gg|^fag|tranny)",
    re.I)

def words_of(s):
    ws = re.findall(r"[a-z0-9']+", s.lower().replace("’", "'"))
    return ["i" + w[1:] if w == "l" or re.match(r"^l'(ll|m|ve|d)$", w) else w for w in ws]

_DICT = None
def _is_word(w):
    global _DICT
    if _DICT is None:
        try:
            # macOS / Linux word list; on Windows set WORDS_FILE to any one-word-per-line list (without one, every
            # 4+ letter "name:" line counts as a username)
            _DICT = set(x.strip().lower() for x in open(os.environ.get("WORDS_FILE") or "/usr/share/dict/words", encoding="utf-8", errors="replace"))
        except OSError:
            _DICT = set()
    return w.lower() in _DICT

def is_username(t):
    """'deucalio:', 'lesbiansinwesteros:', 'crisp_samosa', 'bootyeatr69': a poster's name, not text to reveal."""
    t = t.strip()
    m = re.match(r"^@?([a-z0-9_.\-]{4,}):$", t)
    if m and (re.search(r"[\d_]", m.group(1)) or not _is_word(m.group(1))):
        return True
    if not re.match(r"^@?[A-Za-z][A-Za-z0-9_.\-]{4,}$", t) or t.endswith("."):
        return False
    return re.search(r"\d|_|\.\w", t) is not None

def is_ui(line, name_lines):
    t = line["t"].strip()
    if is_username(t):
        return True
    if UI_RE.search(t):
        return True
    if line in name_lines:
        return True
    if re.search(r"\d\s*%|\$\s*\d|\d\s*\$", t):
        return False                  # "8-9%!", "100$": numbers he reads are text
    if len(words_of(t)) == 0:
        return True
    letters = re.sub(r"[^A-Za-z]", "", t)
    if len(letters) <= 1 or (len(letters) <= 2 and re.search(r"\d", t) and not re.search(r"\b[a-z]{2}\b", t.lower())):   # "3 298", "Q10K", "J" (not "at 56%")
        return True
    return False

def display_name_lines(lines):
    """A display-name line sits directly above an @handle line."""
    out = []
    for i, L in enumerate(lines):
        for M in lines:
            if M is L:
                continue
            if not re.match(r"^@\w+\s*([·•.].*)?$", M["t"].strip()) or len([w for w in L["t"].split() if re.search(r"\w", w)]) > 5:
                continue
            above = -0.005 <= M["b"][1] - L["b"][3] < 0.06 and abs(M["b"][0] - L["b"][0]) < 0.05
            same_row = min(L["b"][3], M["b"][3]) - max(L["b"][1], M["b"][1]) > 0.5 * (L["b"][3] - L["b"][1]) and -0.01 <= M["b"][0] - L["b"][2] < 0.08
            if above or same_row:
                out.append(L)
    # "Name @handle · 22h" on one line is caught by UI_RE already
    return out

def make_blocks(lines):
    """Group content lines into blocks: consecutive, aligned (left edge or centre), small vertical gap. Every open block
    is a candidate, so two-column grids ("This was the / professor" beside "This was the / uniform") group per column.
    Dialogue turns, bullets and label lines ending in ':' ("you receive:") start their own block; a 1-2 word tag in
    another text size under a paragraph ("Advice/Help" flair) is not part of it (the reviewer's fixes, Oct 4 2026)."""
    lines = sorted(lines, key=lambda L: (L["b"][1], L["b"][0]))
    def is_label(L):
        t = L["t"].strip()
        return t.endswith(":") and len(t.split()) <= 3
    dialogue = sum(1 for L in lines if is_label(L)) >= 2
    blocks = []
    for L in lines:
        h = L["b"][3] - L["b"][1]
        t = L["t"].strip()
        turn = re.match(r"^\s*[a-z][a-z ]{0,14}:\s", t, re.I) is not None
        if turn and blocks:
            # "...but whoever / you are: you have improved..." is a sentence running on, not a speaker label (the reviewer, Oct 11 2026)
            above = [B[-1] for B in blocks if B[-1]["b"][3] <= L["b"][1] + 0.002 and L["b"][1] - B[-1]["b"][3] < 0.9 * h
                     and min(L["b"][2], B[-1]["b"][2]) - max(L["b"][0], B[-1]["b"][0]) > 0]
            if above and not re.search(r"[.!?:\"”)]\s*$", above[-1]["t"].strip()) and len(above[-1]["t"].split()) >= 5:
                turn = False                       # a full line running on (a short name line above "Police:" does not count)
        bullet = t.startswith(("•", "◦", "▪")) or re.match(r"^\d{1,2}[.)]\s", t) is not None
        best = None
        if not (turn or bullet or (dialogue and is_label(L))):
            for bl in blocks:
                P, B0 = bl[-1], bl[0]
                if len(bl) == 1 and is_label(P):
                    continue                           # a standalone label ("you receive:") closes its block
                ph = P["b"][3] - P["b"][1]
                gap = L["b"][1] - P["b"][3]
                if not (-0.5 * min(h, ph) < gap < 0.9 * max(h, ph)):
                    continue
                if min(L["b"][2], P["b"][2]) - max(L["b"][0], P["b"][0]) <= 0:
                    continue
                if max(h, ph) > 2.0 * min(h, ph):
                    continue                           # a different text size: another element (label on a can, caption)
                if t.lower() == B0["t"].strip().lower():
                    continue                           # the block's opening line again: the next panel starts ("Watching")
                aligned = abs(L["b"][0] - B0["b"][0]) < 0.035
                if (B0["t"].lstrip().startswith(("•", "◦", "▪")) or re.match(r"^\s*\d{1,2}[.)]\s", B0["t"])) and 0 < L["b"][0] - B0["b"][0] < 0.08:
                    aligned = True                     # the wrapped line of a bullet or numbered item
                if abs((L["b"][0] + L["b"][2]) / 2 - (P["b"][0] + P["b"][2]) / 2) < 0.03:
                    aligned = True                     # centred caption lines
                if not aligned:
                    continue
                if len(t.split()) == 1 and abs(h - ph) > 0.3 * ph and len(bl) >= 2:
                    continue                           # flair / tag in another size ("Advice/Help")
                if best is None or gap < best[0]:
                    best = (gap, bl)
        if best:
            best[1].append(L)
        else:
            blocks.append([L])
    blocks.sort(key=lambda bl: (bl[0]["b"][1], bl[0]["b"][0]))
    return blocks

SHORT = {"ppl": "people", "u": "you", "ur": "your", "w": "with", "bc": "because", "b4": "before", "pls": "please",
         "bf": "boyfriend", "gf": "girlfriend", "sth": "something", "smth": "something", "abt": "about", "cuz": "because",
         "tho": "though", "thru": "through", "ya": "you", "r": "are", "n": "and", "im": "i'm", "dont": "don't"}

def _eq(a, b):
    a, b = SHORT.get(a, a), SHORT.get(b, b)
    return a == b or (len(a) > 2 and len(b) > 2 and difflib.SequenceMatcher(None, a, b).ratio() >= 0.8)

def align(line_words, timed, start_from=0, min_frac=0.6):
    """Where the block's opening words are spoken in order.
    The first word may be paraphrased ("guys" for "yall"), but then the next words must match.
    Acceptance uses the first 5 words; among accepted positions the one matching most of the first
    10 words wins (earliest on a tie), so a similar earlier sentence does not steal the match.
    Returns (index, start_time) or None."""
    if not line_words:
        return None
    probe5 = line_words[:5]
    need = len(probe5) if len(probe5) <= 2 else max(2, -(-len(probe5) * 3 // 5))
    probe = line_words[:10]
    cands = []
    for i in range(start_from, len(timed)):
        for skip_first in (0, 1):
            pr = probe[skip_first:]
            if not pr or not _eq(timed[i][0], pr[0]):
                continue
            j, hit, hit5, gaps = i + 1, 1, 1, 0
            for n, w in enumerate(pr[1:], start=1 + skip_first):
                for k in range(j, min(j + 5, len(timed))):
                    if _eq(timed[k][0], w):
                        hit += 1
                        hit5 += n < 5
                        gaps += k - j            # spoken words skipped to reach this one
                        j = k + 1
                        break
            ok = hit5 >= need if not skip_first else hit5 >= max(3, need - 1)
            if not ok and not skip_first and hit >= 3 and hit >= 0.5 * len(probe):
                ok = True        # he swapped a word or two while reading ("Watching it in incognito" for "...porn in an incognito tab")
            if ok:
                # a paraphrased first word was spoken just before the match (an unspoken "Me:" label was not)
                # (not for a list number: "3." is never spoken, so the match starts at the item's first word)
                start = i - 1 if skip_first and not re.match(r"^\d+$", probe[0]) and i > start_from and timed[i][1] - timed[i - 1][2] < 0.6 else i
                cands.append((hit / len(probe) - 0.04 * gaps, start))   # a tight run of words beats a scattered one
    if not cands:
        return None
    top = max(s for s, _ in cands)
    start = min(st for s, st in cands if s >= top - 0.07)
    return start, timed[start][1]

def fuzzy_align(bw, timed, start_from=0, thr=0.72):
    """Short label (1-4 words) matched as a string against windows of spoken words."""
    target = " ".join(bw)
    best = None
    for i in range(start_from, len(timed)):
        for m in (len(bw) - 1, len(bw), len(bw) + 1):
            if m < 1 or i + m > len(timed):
                continue
            r = difflib.SequenceMatcher(None, target, " ".join(t[0] for t in timed[i:i + m])).ratio()
            if r >= thr and (best is None or r > best[0] + 0.02):
                best = (r, i)
    return (best[1], timed[best[1]][1]) if best else None

def reading_end(block_words, timed, start_idx, stop_idx=None):
    """(end time, index) of the last of the block's words he speaks, matched in order from start_idx, each word within a
    few spoken words of the previous match (the reviewer, Oct 3 2026: a wipe ends when he FINISHES reading the block).
    In-order matching keeps a repeated ending ("...bleed out and die" in the next reply) from stretching the block."""
    hi = min(len(timed), start_idx + 2 * len(block_words) + 8)
    if stop_idx is not None:
        hi = min(hi, stop_idx)
    j, last, misses = start_idx, None, 0
    for w in block_words:
        found = None
        for k in range(j, min(hi, j + (5 if last is not None else 2))):   # the opening words must sit at the start
            if _eq(SHORT.get(timed[k][0], timed[k][0]), SHORT.get(w, w)):
                found = k
                break
        if found is None:
            misses += 1
            if misses > 6:
                break                      # he stopped reading this block
            continue
        last, j, misses = found, found + 1, 0
    return (timed[last][2], last) if last is not None else (None, None)

def last_word_time(line_words, timed, from_idx):
    """Start time of the block's last word as spoken (fuzzy), searching forward from the block start."""
    target = line_words[-1]
    best = None
    for k in range(from_idx, min(len(timed), from_idx + 80)):
        if timed[k][0] == target or difflib.SequenceMatcher(None, timed[k][0], target).ratio() >= 0.8:
            best = timed[k][1]
    return best

def plan(ocr_lines, timed_words):
    """timed_words: [(normalized word, start_raw_s, end_raw_s), ...] for this meme, in speaking order."""
    names = display_name_lines(ocr_lines)
    content = [L for L in ocr_lines if not is_ui(L, names)]
    blocks = make_blocks(content)
    def _label(bl):
        t = bl[0]["t"].strip()
        return len(bl) == 1 and t.endswith(":") and len(t.split()) <= 3
    dialogue = sum(1 for bl in blocks if _label(bl)) >= 2
    if dialogue:
        turns = []
        for bl in blocks:
            if _label(bl) or not turns:
                turns.append(list(bl))
            elif _label(turns[-1][:1]) and abs(bl[0]["b"][1] - turns[-1][-1]["b"][3]) < 0.12:
                turns[-1] += bl
            else:
                turns.append(list(bl))
        blocks = turns
    out_blocks = []
    for bl in blocks:
        w0 = words_of(bl[0]["t"])
        ball = [w for L in bl for w in words_of(L["t"])]
        a = align(ball if len(w0) <= 2 and len(bl) > 1 else w0, timed_words)   # a short label line: match the whole turn
        for k in (1, 2):
            if a is None and len(ball) - k >= 3 and k < len(w0):
                a = align(ball[k:], timed_words)      # he skipped the opening word(s): "Pro tip:", "so"
        if a is None and len(bl) >= 2 and len(w0) <= 4:
            # an unspoken short first line is usually a display name glued onto the text: start from line 2
            a2 = align(words_of(bl[1]["t"]), timed_words)
            if a2 is not None:
                bl, a = bl[1:], a2
        bw = [w for L in bl for w in words_of(L["t"])]
        if a is None and 1 <= len(bw) <= 4:
            a = fuzzy_align(bw, timed_words)          # a short label Whisper misheard
        out_blocks.append({"lines": bl, "words": bw, "read_idx": a[0] if a else None, "read_t": a[1] if a else None})
    for b in out_blocks:
        if len(b["words"]) < 2 and not (b["read_t"] is not None and len(b["words"]) == 1 and len(b["words"][0]) >= 3):
            b["read_idx"] = b["read_t"] = None
    # labels that open with the same words ("This was the professor" / "This was the uniform"): align each by its own words
    same = {}
    for b in out_blocks:
        if 3 < len(b["words"]) <= 5:          # short labels only ("This was the professor")
            same.setdefault(tuple(b["words"][:3]), []).append(b)
    for key, bs in same.items():
        if len(bs) < 2:
            continue
        for b in bs:
            hit = align(b["words"][3:], timed_words) or fuzzy_align(b["words"][3:], timed_words)
            if hit:
                k = hit[0]
                while k > 0 and hit[0] - k < 3 and timed_words[k - 1][0] in key:
                    k -= 1
                b["read_idx"], b["read_t"] = k, timed_words[k][1]
    read = [b for b in out_blocks if b["read_t"] is not None]
    read.sort(key=lambda b: b["read_t"])
    # a block whose match sits inside the span of an earlier block's reading is an echo (e.g. a logo word)
    spans = []
    kept = []
    for b in read:
        if any(s0 <= b["read_idx"] <= s1 for s0, s1 in spans):
            b["read_idx"] = b["read_t"] = None
            continue
        b["read_end"], end_idx = reading_end(b["words"], timed_words, b["read_idx"])
        if end_idx is None:
            end_idx = b["read_idx"]
        spans.append((b["read_idx"], end_idx))
        kept.append(b)
    read = kept
    blurs = []
    for n, b in enumerate(read):
        nxt = read[n + 1]["read_idx"] if n + 1 < len(read) else None
        if nxt is not None:   # never past the start of the next block he reads
            b["read_end"] = min(b["read_end"] or 1e9, timed_words[nxt][1]) if b["read_end"] else timed_words[nxt][1]
        spoken_s = (b["read_end"] - b["read_t"]) if b.get("read_end") else 0
        if dialogue:
            if n > 0:
                blurs.append({"kind": "box", "lines": b["lines"], "raw_t": b["read_t"], "n_lines": 1,
                              "spoken": spoken_s or None})   # a turn snaps in like a punchline
            continue
        if n == 0:
            # first block: the meme's first text line stays visible; the rest is wiped from the meme's start to the end
            # of his reading. When a separate title line sits above the block ("Shark fact:"), that title is the visible
            # line and the whole block is wiped (the reviewer, Oct 4 2026). 2-line first blocks get no blur at all (Oct 3 2026)
            title_above = any(L["b"][3] <= b["lines"][0]["b"][1] + 0.002 and L not in b["lines"] for L in content)
            if len(b["lines"]) >= 3:
                rest = b["lines"] if title_above else b["lines"][1:]
                a2 = align(words_of(rest[0]["t"]), timed_words, start_from=b["read_idx"] or 0)
                t_first = a2[1] if a2 else b["read_t"]
                blurs.append({"kind": "wipe", "lines": rest, "n_lines_block": len(b["lines"]),
                              "raw_first": t_first, "raw_block": b["read_t"], "raw_end": b["read_end"]})
        elif len(b["lines"]) >= 3 and (len(b["words"]) >= 12 or spoken_s >= 3.0):
            blurs.append({"kind": "wipe", "lines": b["lines"], "n_lines_block": len(b["lines"]), "later": True,
                          "raw_first": b["read_t"], "raw_end": b["read_end"]})
        else:
            blurs.append({"kind": "box", "lines": b["lines"], "raw_t": b["read_t"], "n_lines": len(b["lines"]),
                          "spoken": spoken_s or None})
    # curse words anywhere in the meme text (content or UI lines)
    for L in ocr_lines:
        for w in L["words"]:
            core = w["t"].strip(".,!?\"'()[]:;*").lower()
            if core and CURSE_RE.search(core):
                blurs.append({"kind": "curse", "word": w["t"], "word_box": w["b"], "line": L["t"]})
    return out_blocks, blurs
