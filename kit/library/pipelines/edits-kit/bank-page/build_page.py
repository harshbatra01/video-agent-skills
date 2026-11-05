"""Parse the research markdown files into bank JSON and render the page.

usage: python build_page.py RESEARCH_DIR page/template.html page/ouredit.json page/our_summary.json page/aims.json OUT.html
Prints a parse report (entries, urls, tags per file) so formats that slipped can be fixed.
"""
import sys, os, re, json, hashlib, glob
from datetime import date

RES, TPL, OURJ, SUMJ, AIMS, OUT = sys.argv[1:7]

FAMILIES = {
    "CUT": ("Cuts & speed", "beat-cut micro-cut stutter-repeat freeze-frame reverse speed-ramp smooth-slowmo jump-zoom match-cut"),
    "CAMERA": ("Camera moves", "shake zoom-punch whip-pan rotate-tilt 3d-camera mirror-edge-transition spin-transition dolly-zoom"),
    "LIGHT": ("Light & flash", "white-flash color-flash invert-flash strobe exposure-pop glow light-leak lens-flare light-rays film-burn"),
    "COLOR": ("Colour", "cc-grade bw color-pop duotone-tint posterize halftone contrast-crush sat-pulse"),
    "DISTORT": ("Distortion & texture", "grain vhs glitch rgb-split chromatic-aberration wave-warp displacement datamosh pixel-sort lens-distortion motion-blur radial-zoom-blur echo-trails slit-scan kaleidoscope"),
    "COMPOSITE": ("Roto & compositing", "roto-cutout outline-stroke text-behind-subject clone bg-swap split-screen-grid overlay-texture particles 3d-elements scribble-doodle"),
    "TYPE": ("Type & captions", "lyric-text word-by-word kinetic-type 3d-text tracked-text glitch-text outline-text song-card stat-graphics"),
    "STRUCTURE": ("Structure", "hook-first-second build-to-drop beat-switch slow-intro outro-card loop-ending"),
}
FAM = {k: {"name": v[0], "tags": v[1].split()} for k, v in FAMILIES.items()}
KNOWN = {t: f for f, d in FAM.items() for t in d["tags"]}
ALIAS = {"velocity": "speed-ramp", "speed-ramps": "speed-ramp", "twixtor": "smooth-slowmo", "slow-mo": "smooth-slowmo", "slowmo": "smooth-slowmo",
         "flash": "white-flash", "flashes": "white-flash", "white flash": "white-flash", "shakes": "shake", "camera-shake": "shake",
         "zoom": "zoom-punch", "zoom-in": "zoom-punch", "b&w": "bw", "black-and-white": "bw", "colour-pop": "color-pop", "colorpop": "color-pop",
         "rgb": "rgb-split", "chromatic": "chromatic-aberration", "ca": "chromatic-aberration", "roto": "roto-cutout", "rotoscope": "roto-cutout",
         "outline": "outline-stroke", "stroke": "outline-stroke", "text-behind": "text-behind-subject", "lyrics": "lyric-text", "lyric": "lyric-text",
         "3d": "3d-camera", "parallax": "3d-camera", "overlay": "overlay-texture", "overlays": "overlay-texture", "light-leaks": "light-leak",
         "deep-glow": "glow", "cc": "cc-grade", "grade": "cc-grade", "freeze": "freeze-frame", "invert": "invert-flash", "echo": "echo-trails",
         "trails": "echo-trails", "mirror": "mirror-edge-transition", "spin": "spin-transition", "whip": "whip-pan", "hook": "hook-first-second",
         "drop": "build-to-drop", "loop": "loop-ending", "song card": "song-card", "spotify-card": "song-card"}
LANES = [("01", "football", "Football"), ("02", "basketball", "Basketball & US sports"), ("03", "combat", "Fights, F1 & more"),
         ("04", "amv", "Anime & edit scene"), ("05", "captions", "Captions & type"), ("07", "roto", "Roto & compositing"),
         ("08", "sync", "Sync & structure")]
URL_RE = re.compile(r"https?://[^\s<>\)\]\|\"'`]+")
report = []

def slug(s):
    s = s.lower().strip().strip("*_`").replace("&", "and")
    s = re.sub(r"\(.*?\)", "", s)
    s = re.sub(r"[^a-z0-9+]+", "-", s).strip("-")
    return s

def norm_tag(tok):
    raw = tok.strip().strip("*_`.").strip()
    if not raw: return None
    newp = raw.lower().startswith("new:")
    if newp: raw = raw[4:]
    raw = re.sub(r"\(.*?\)", "", raw)
    raw = re.sub(r"\b\d{1,2}:\d{2}\b.*", "", raw).strip()
    s = slug(raw)
    if not s: return None
    if s in KNOWN: return s
    if s in ALIAS: return ALIAS[s]
    if raw.lower() in ALIAS: return ALIAS[raw.lower()]
    for k in KNOWN:  # token that contains a known tag (e.g. "white-flash-on-kicks")
        if s.startswith(k + "-") or s == k: return k
    if newp and len(s) <= 28: return s
    return None

def parse_tags(text):
    out = []
    for tok in re.split(r"[,;/]| \+ |\s·\s", text or ""):
        t = norm_tag(tok)
        if t and t not in out: out.append(t)
    return out

def sections(md):
    """split by '## ' headings -> list of (heading, body)"""
    parts = re.split(r"(?m)^#{1,2}\s+(?!#)", md)
    out = []
    for p in parts[1:]:
        h, _, body = p.partition("\n")
        out.append((h.strip(), body))
    return out

def entries(body):
    parts = re.split(r"(?m)^###\s+", body)
    out = []
    for p in parts[1:]:
        h, _, rest = p.partition("\n")
        out.append((re.sub(r"^\d+[\.\)]\s*", "", h.strip()).strip(" *"), rest))
    return out

def kv(rest):
    """bullet 'Key: value' lines -> dict (lowercased key), plus all text"""
    d = {}
    for line in rest.splitlines():
        m = re.match(r"^\s*[-*]\s*\**([A-Za-z][A-Za-z /'&()\-]{1,40}?)\**\s*:\**\s*(.*)$", line)
        if m:
            k = m.group(1).lower().strip()
            d[k] = (d.get(k, "") + " " + m.group(2)).strip()
    return d

def pick(d, *keys):
    for k in d:
        for want in keys:
            if k.startswith(want): return d[k]
    return ""

PLAT = re.compile(r"tiktok|instagram|youtube|shorts|reels|twitter|\bx\b|reddit|vimeo|facebook|behance|twitch|kick", re.I)

def parse_linkline(line):
    out = dict(platform="", creator="", subject="", song="", views="", date="")
    parts = [p.strip() for p in line.split("|")]
    for p in parts[1:] if parts and URL_RE.search(parts[0]) else parts:
        pl = p.lower()
        if not p or URL_RE.fullmatch(p): continue
        if pl.startswith("creator") or p.startswith("@"):
            out["creator"] = re.sub(r"^creator:?\s*", "", p, flags=re.I)
        elif re.search(r"views|likes|plays", pl) or re.fullmatch(r"[\d.,]+\s*[kmb]\+?", pl):
            out["views"] = re.sub(r"^(views/likes|views|likes)\s*:?\s*", "", p, flags=re.I)
        elif pl.startswith("song") or pl.startswith("music") or pl.startswith("audio"):
            out["song"] = re.sub(r"^(song|music|audio)\s*(\(if known\))?:?\s*", "", p, flags=re.I)
        elif pl.startswith("date") or re.search(r"\b20[12]\d\b", pl) and len(p) < 24:
            out["date"] = re.sub(r"^date:?\s*", "", p, flags=re.I)
        elif pl.startswith("platform") or (PLAT.search(pl) and len(p) < 30 and not out["platform"]):
            out["platform"] = re.sub(r"^platform:?\s*", "", p, flags=re.I)
        elif pl.startswith("subject") or not out["subject"]:
            out["subject"] = re.sub(r"^subject:?\s*", "", p, flags=re.I)
        elif not out["song"]:
            out["song"] = p
    for k in out:
        v = out[k].strip(" *")
        if v.lower() in ("unknown", "n/a", "-", "(unverified)", "not found", "?", "none"): v = ""
        out[k] = v
    return out

def clean(s, n=400):
    s = re.sub(r"\s+", " ", (s or "")).strip()
    s = s.replace("**", "")
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"

def table_rows(body):
    rows, head = [], None
    for line in body.splitlines():
        if not line.strip().startswith("|"): head = None if not line.strip() else head; continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c): continue
        if head is None: head = [c.lower() for c in cells]; continue
        rows.append(dict(zip(head, cells)))
    return rows

def creators_from(body, lane):
    out = []
    for r in table_rows(body):
        handle = next((r[k] for k in r if "handle" in k or "account" in k or "creator" in k or "name" in k), "")
        allt = " ".join(r.values())
        url = (URL_RE.search(allt) or [None])[0] if URL_RE.search(allt) else ""
        m = re.search(r"\[([^\]]+)\]\((https?://[^)]+)\)", handle)
        if m: handle, url = m.group(1), m.group(2)
        out.append(dict(handle=clean(re.sub(URL_RE, "", handle), 60) or "(unnamed)", url=url,
                        platform=clean(next((r[k] for k in r if "platform" in k), ""), 40),
                        style=clean(next((r[k] for k in r if "style" in k or "signature" in k or "why" in k), ""), 220),
                        followers=clean(next((r[k] for k in r if "follow" in k or "subs" in k), ""), 30), lane=lane))
    if not out:  # bullet form
        for line in body.splitlines():
            m = re.match(r"^\s*[-*]\s*(.+)$", line)
            if m and URL_RE.search(line):
                u = URL_RE.search(line).group(0)
                txt = clean(URL_RE.sub("", m.group(1)), 260)
                out.append(dict(handle=clean(txt.split(" ")[0], 60), url=u, platform="", style=txt, followers="", lane=lane))
    return out

def tutorials_from(body, lane):
    out = []
    for line in body.splitlines():
        if not URL_RE.search(line): continue
        u = URL_RE.search(line).group(0)
        m = re.search(r"\[([^\]]+)\]\(" + re.escape(u), line)
        txt = m.group(1) if m else clean(URL_RE.sub("", line).strip("-*| "), 140)
        txt = re.sub(r"\s*\|\s*", " · ", txt).strip(" ·")
        tech = ""
        tm = re.search(r"(technique|teaches|covers|for)\s*:?\s*([^|]+)$", line, re.I)
        if tm: tech = clean(tm.group(2), 60)
        out.append(dict(title=clean(txt, 140) or u, url=u, technique=tech, lane=lane))
    return out

def bullets(body):
    out = []
    for line in body.splitlines():
        m = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.+)$", line)
        if m: out.append(clean(m.group(1), 360))
    return out

def uid(s):
    return hashlib.sha1(s.encode()).hexdigest()[:10]

items, creators, tutorials, patterns, techniques, tools = [], [], [], [], [], []
seen = {}
for num, lane, lname in LANES:
    f = glob.glob(os.path.join(RES, num + "-*.md"))
    if not f: report.append(f"{num} {lane}: MISSING"); continue
    md = open(f[0], encoding="utf-8").read()
    n_items = 0
    for h, body in sections(md):
        hl = h.lower()
        if "standout" in hl or "edits" in hl and "creator" not in hl and "tutorial" not in hl and "breakdown" not in hl or hl.startswith("1"):
            for title, rest in entries(body):
                d = kv(rest)
                urls = URL_RE.findall(rest)
                if not urls: continue
                linkline = pick(d, "link")
                meta = parse_linkline(linkline) if linkline else dict(platform="", creator="", subject="", song="", views="", date="")
                main = URL_RE.search(linkline).group(0) if linkline and URL_RE.search(linkline) else urls[0]
                main = main.rstrip(".,;")
                key = re.sub(r"[?#].*$", "", main.lower().rstrip("/")) if "youtube.com/watch" not in main else main.lower()
                tags = parse_tags(pick(d, "techni", "tags"))
                why = pick(d, "why")
                blob = why + " " + rest
                if re.search(r"\[W\]|checked:\s*frames|frame sheet|viewed in a|scrubbed", blob, re.I): ev = "W"
                elif re.search(r"thumbs only|preview stills|storyboard|\bstills\b", blob, re.I): ev = "T"
                elif re.search(r"\[M\]|metadata only|not viewed|unverified", blob, re.I): ev = "M"
                else: ev = ""
                why = re.sub(r"\[(W|M)\]\s*", "", why)
                tier = ""
                tm = re.search(r"\s*[\[(]([ABCDPU])(?:,[^\])]*)?[\])]\s*$", title)
                if tm: tier, title = tm.group(1), title[:tm.start()].strip()
                if tier in ("D", "U"): ev = "M"
                it = dict(id=uid(key), lane=lane, title=clean(title, 120), url=main, links=[u.rstrip(".,;") for u in urls[:6]], ev=ev, tier=tier,
                          why=clean(why, 380), steal=clean(pick(d, "steal"), 260), tags=tags, **{k: clean(v, 80) for k, v in meta.items()})
                if key in seen:
                    prev = seen[key]
                    prev["tags"] = prev["tags"] + [t for t in tags if t not in prev["tags"]]
                    if lane not in prev["lanes"]: prev["lanes"].append(lane)
                    if it["why"] or it["steal"]: prev["also"].append(dict(lane=lane, why=it["why"], steal=it["steal"]))
                    for k in ("views", "date", "song", "creator"):
                        if not prev[k] and it[k]: prev[k] = it[k]
                    if not prev["ev"] or (prev["ev"] != "W" and it["ev"] == "W"): prev["ev"] = it["ev"]
                    if not prev["tier"] and it["tier"]: prev["tier"] = it["tier"]
                    continue
                it["lanes"] = [lane]; it["also"] = []
                seen[key] = it; items.append(it); n_items += 1
        elif "creator" in hl or "account" in hl:
            creators += creators_from(body, lane)
        elif "breakdown" in hl or "tutorial" in hl:
            tutorials += tutorials_from(body, lane)
        elif "pattern" in hl or "song" in hl and "trend" in hl:
            patterns += [dict(lane=lane, text=b) for b in bullets(body) if not URL_RE.fullmatch(b)][:16]
    untagged = sum(1 for i in items if i["lane"] == lane and not i["tags"])
    report.append(f"{num} {lane}: {n_items} items ({untagged} without tags)")

# effects catalogue -> techniques
f6 = glob.glob(os.path.join(RES, "06-*.md"))
if f6:
    md = open(f6[0], encoding="utf-8").read()
    for h, body in sections(md):
        hl = h.lower()
        if "creator" in hl or "account" in hl: creators += creators_from(body, "effects"); continue
        if "breakdown" in hl or "tutorial" in hl: tutorials += tutorials_from(body, "effects"); continue
        if "pattern" in hl: patterns += [dict(lane="effects", text=b) for b in bullets(body)][:16]; continue
        for title, rest in entries(body):
            d = kv(rest)
            tl = parse_tags(pick(d, "tags"))
            tag = (tl[0] if tl else None) or norm_tag(title) or norm_tag("new:" + title)
            fam = KNOWN.get(tag, "NEW")
            ex = []
            for line in rest.splitlines():
                u = URL_RE.search(line)
                if not u or re.match(r"^\s*-\s*(Looks|Tags|Trend|Music)", line): continue
                parts = [x.strip() for x in line.strip().lstrip("-* ").split("|")]
                kind = parts[0] if parts and not URL_RE.search(parts[0]) else ""
                ttl = parts[2] if len(parts) > 2 else ""
                evm = re.search(r"\[(SEEN|MEASURED|TITLE)\]", line)
                note = line[evm.end():].strip() if evm else ""
                ex.append(dict(url=u.group(0).rstrip(".,;"), kind=kind[:6], label=clean(ttl, 80), ev=(evm.group(1) if evm else ""), note=clean(note, 240)))
            techniques.append(dict(tag=tag, fam=fam, name=clean(title, 70), look=clean(pick(d, "looks", "look", "what"), 240),
                                   trend=clean(pick(d, "trend"), 220), sync=clean(pick(d, "music sync", "sync"), 220), examples=ex[:5]))
    report.append(f"06 effects: {len(techniques)} techniques")
else:
    report.append("06 effects: MISSING")

# tools
f9 = glob.glob(os.path.join(RES, "09-*.md"))
if f9:
    md = open(f9[0], encoding="utf-8").read()
    for h, body in sections(md):
        hl = h.lower()
        if "creator" in hl or "seller" in hl or "editor" in hl and "pattern" not in hl: creators += creators_from(body, "tools"); continue
        if "breakdown" in hl or "tutorial" in hl: tutorials += tutorials_from(body, "tools"); continue
        if "pattern" in hl: patterns += [dict(lane="tools", text=b) for b in bullets(body)][:16]; continue
        for title, rest in entries(body):
            d = kv(rest)
            urls = URL_RE.findall(rest)
            if not urls and not d: continue
            tools.append(dict(name=clean(title, 70), url=(urls[0].rstrip(".,;") if urls else ""), price=clean(pick(d, "price", "cost"), 60),
                              does=clean(pick(d, "what it does", "does", "what"), 240), tags=parse_tags(pick(d, "which effects", "powers", "effects", "tags")),
                              common=clean(pick(d, "how common", "common", "used by", "popular"), 200), compat=clean(pick(d, "compat", "works", "platform"), 70),
                              alt=clean(pick(d, "free alt", "alternative", "free"), 160)))
    report.append(f"09 tools: {len(tools)} tools")
else:
    report.append("09 tools: MISSING")

# earlier artifacts -> patterns (rules of thumb + build sheets)
f10 = glob.glob(os.path.join(RES, "10-*.md"))
if f10:
    md = open(f10[0], encoding="utf-8").read()
    for blk in re.split(r"(?m)^###\s+", md)[1:]:
        h, _, body = blk.partition("\n")
        if re.search(r"rules of thumb|build|cold open", h, re.I):
            patterns += [dict(lane="past", text=b) for b in bullets(body)][:10]

# dedupe creators by handle
cd = {}
for c in creators:
    k = c["handle"].lower().lstrip("@")
    if k and k not in cd: cd[k] = c
creators = list(cd.values())
td = {}
for t in tutorials:
    if t["url"] not in td: td[t["url"]] = t
tutorials = list(td.values())

lanes = [dict(id=l, name=n) for _, l, n in LANES] + [dict(id="effects", name="Effects catalogue"), dict(id="tools", name="Tools")]
bank = dict(generated=date.today().strftime("%d %b %Y").lstrip("0"), families=FAM, lanes=[l for l in lanes if l["id"] not in ("effects", "tools")],
            items=items, techniques=techniques, creators=creators, tutorials=tutorials, tools=tools, patterns=patterns,
            aims=json.load(open(AIMS, encoding="utf-8")))
our = json.load(open(OURJ)); our.update(json.load(open(SUMJ, encoding="utf-8")))
def js(o): return json.dumps(o, ensure_ascii=False).replace("</", "<\\/")
html = open(TPL, encoding="utf-8").read().replace("__BANK_JSON__", js(bank)).replace("__OUR_JSON__", js(our))
open(OUT, "w", encoding="utf-8").write(html)
tagc = {}
for i in items:
    for t in i["tags"]: tagc[t] = tagc.get(t, 0) + 1
newtags = sorted([t for t in tagc if t not in KNOWN], key=lambda t: -tagc[t])
print("\n".join(report))
print(f"TOTAL items {len(items)}, techniques {len(techniques)}, creators {len(creators)}, tutorials {len(tutorials)}, tools {len(tools)}, patterns {len(patterns)}")
print("new tags:", ", ".join(f"{t}({tagc[t]})" for t in newtags[:30]))
print(f"page {os.path.getsize(OUT)//1024} KB -> {OUT}")
