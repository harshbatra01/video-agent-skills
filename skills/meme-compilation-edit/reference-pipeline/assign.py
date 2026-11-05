"""Match every spoken phrase to a meme and flag phrases to cut, for review.

Screen first (which file Drive shows at the phrase's midpoint, ignoring flips shorter than 1.5 s),
text second (a strong match to another meme on screen within +-6 s wins, e.g. he starts reading
the next meme a moment before the preview switches). Flags: restart (the next phrase repeats its
opening words), noise (no words), loop (Whisper repetition garbage).
Outputs: assign.json (per phrase) and review.txt (narration grouped by meme).
"""
import json, os, re, difflib

CLIENT = "/CHANGE/ME/client folder/"
ocr = {}
for line in open("img_ocr.jsonl"):
    r = json.loads(line)
    ocr[os.path.basename(r["file"]).replace(".webp.png", ".webp").replace(".WEBP.png", ".WEBP").replace(".mp4.png", ".mp4")] = r

def words(s):
    return re.findall(r"[a-z0-9']+", s.lower().replace("’", "'"))

meme_words = {f: words(" ".join(L["t"] for L in r["lines"])) for f, r in ocr.items()}
runs = json.load(open("screen_runs.json"))
stable = [r for r in runs if r["file"] and r["b"] - r["a"] >= 1.5]

def screen_at(t):
    best, bd = None, 1e9
    for r in stable:
        if r["a"] <= t < r["b"]:
            return r["file"]
        d = min(abs(t - r["a"]), abs(t - r["b"]))
        if d < bd:
            best, bd = r["file"], d
    return best

def score(pw, f):
    mw = meme_words.get(f) or []
    if not mw or not pw:
        return 0.0
    ms = set(mw)
    return sum(1 for w in pw if w in ms or difflib.get_close_matches(w, mw, n=1, cutoff=0.8)) / len(pw)

pieces = json.load(open("pieces_asr.json"))
for pc in pieces:
    t = (pc["a"] + pc["b"]) / 2
    pw = words(pc["text"])
    scr = screen_at(t)
    cands = []
    for r in stable:
        if r["b"] > t - 6 and r["a"] < t + 6 and r["file"] not in cands:
            cands.append(r["file"])
    sc = {f: round(score(pw, f), 2) for f in cands}
    best = max(sc, key=sc.get) if sc else None
    meme = scr
    if best and best != scr and sc[best] >= 0.6 and len(pw) >= 3 and sc[best] > sc.get(scr, 0) + 0.25:
        meme = best
    pc["meme"] = meme
    pc["screen"] = scr
    if len(pw) >= 3:
        g = max(meme_words, key=lambda f: score(pw, f))
        pc["global"] = [g, round(score(pw, g), 2)]
    pc["reads"] = bool(meme and sc.get(meme, 0) >= 0.6 and len(pw) >= 2)
    pc["flags"] = []
    if not pw:
        pc["flags"].append("noise")
    toks = pw
    if len(toks) >= 6 and max(toks.count(w) for w in set(toks)) >= max(5, len(toks) // 2):
        pc["flags"].append("loop")

# restarts: a phrase whose opening words are repeated by the next phrase (he restarted the line)
for i in range(len(pieces) - 1):
    w1, w2 = words(pieces[i]["text"]), words(pieces[i + 1]["text"])
    if not w1 or not w2:
        continue
    common = 0
    while common < min(len(w1), len(w2)) and w1[common] == w2[common]:
        common += 1
    if common >= 2 or (len(w1) >= 1 and w2[:len(w1)] == w1) or (common >= 1 and len(w1) <= 2 and pieces[i]["text"].rstrip().endswith(("-", "..."))):
        pieces[i]["flags"].append("restart")

# garbled first tries: a short phrase that sounds like the opening of the phrase right after it ("You'll wait for that."
# before "You are late for work.", "What the hell?" before "Who the hell?", "Then out." before "They're now translucent.").
# The reviewer cut all three (Oct 4 2026). Flag only: similar short comments ("Not scary." / "Scary.") were kept.
def _n(t):
    return re.sub(r"[^a-z ]", "", t.lower().replace("’", "'")).strip()
for i in range(len(pieces) - 1):
    p, q = pieces[i], pieces[i + 1]
    t1, t2 = _n(p["text"]), _n(q["text"])
    if not t1 or not t2 or "restart" in p["flags"] or len(t1.split()) > 6 or p["b"] - p["a"] > 1.8 or q["a"] - p["b"] > 1.5:
        continue
    if difflib.SequenceMatcher(None, t1, t2[:len(t1) + 3]).ratio() >= 0.5:
        p["flags"].append("false-start?")
# the same word on both sides of a join ("...a change of heart and..." / "And has become cruel"): trim the first copy
for i in range(len(pieces) - 1):
    w1, w2 = words(pieces[i]["text"]), words(pieces[i + 1]["text"])
    if w1 and w2 and w1[-1] == w2[0] and len(w2) > 1 and pieces[i + 1]["a"] - pieces[i]["b"] < 1.2:
        pieces[i]["flags"].append("dup-join:" + w1[-1])

json.dump(pieces, open("assign.json", "w"), indent=0)
with open("review.txt", "w") as f:
    cur = None
    for k, pc in enumerate(pieces):
        if pc["meme"] != cur:
            cur = pc["meme"]
            f.write(f"\n## {cur}\n")
        tag = "READ" if pc["reads"] else "comm"
        fl = (" <" + ",".join(pc["flags"]) + ">") if pc["flags"] else ""
        gl = pc.get("global")
        gx = f"   [best match anywhere: {gl[0]} {gl[1]}]" if gl and gl[0] != pc["meme"] and gl[1] >= 0.6 else ""
        f.write(f"  #{k:<4d}{pc['a']:7.2f}-{pc['b']:7.2f} [{tag}]{fl} {pc['text']}{gx}\n")
print(len(pieces), "phrases;", sum(1 for p in pieces if "restart" in p["flags"]), "restarts;",
      sum(1 for p in pieces if "noise" in p["flags"]), "noise;", sum(1 for p in pieces if "loop" in p["flags"]), "loops")
