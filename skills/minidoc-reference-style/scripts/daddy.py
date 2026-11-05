# The Daddy file tool: keeps DADDY.md (the video's single source of truth) in sync with the real edit, and reviews every
# proposed addition against it before it is built.
#   python3 daddy.py <job> sync                 regenerate the AUTO inventory inside DADDY.md (shots, overlays, SFX, entities)
#   python3 daddy.py <job> audit                run every automatic check on what is in the edit now
#   python3 daddy.py <job> check proposal.json  review one proposed addition (see DADDY.md "How to propose")
# Automatic checks (rule ids match DADDY.md section 3):
#   A1 redundancy: a label names a person or place the viewer already knows (named in the voice-over twice or shown 2+ times)
#   A2 duplicate text: on-screen text repeats the caption words on screen at the same moment
#   A3 repetition: the same sound or overlay type again within 8 s, or more than 3 times in the video
#   A4 collision: an overlay box overlaps the caption band while a caption is showing
#   A5 facts: every number or claim on screen must be in the facts table with a source
#   A6 rule breaks: nothing new may land on the black breather card or on a soundbite, except naming an unknown speaker
#   A7 purpose: a proposal must say what the viewer gains; empty purpose is rejected
#   A8 sound files: a sound effect that contains several hits (a triple gavel) plays as several hits: flag it
#   A9 splices: every voice-over split and soundbite edge must sit in real silence (word timings glue words together)
#   A10 moving targets: a callout drawn on a graphic that pushes in must zoom with it, or it drifts off target
# Base version: DADDY_BASE=v8b (default v8b) selects edit_<base>.json, music_plan_<base>.json, sfx_cues_<base>.json, build_<base>.py
import json, os, re, sys, html
from html.parser import HTMLParser
J, CMD = sys.argv[1], sys.argv[2]
DADDY = f"{J}/DADDY.md"
BASE = os.environ.get("DADDY_BASE", "v8b")
EDIT = f"{J}/edit/edit_{BASE}.json"; SFXC = f"{J}/music/sfx_cues_{BASE}.json"; PLAN = f"{J}/music/music_plan_{BASE}.json"; BUILD = f"{J}/tools/build_{BASE}.py"
OVER = f"{J}/hyperframes/overlay-v9/index.html"
CAPTION_BAND = (0.40, 0.60)          # captions sit around mid-frame (y as share of height)

def nrm(x): return re.sub(r"[^a-z0-9]", "", x.lower())
# ---------- the timeline as the viewer gets it ----------
import subprocess
import numpy as np
def level_db(path, t, dur=0.06, ss_first=True):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{max(t, 0):.3f}", "-i", path, "-t", f"{dur:.3f}", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    return 20 * np.log10(np.sqrt(np.mean(a ** 2)) + 1e-9) if len(a) else -120.0
def silence_after(t, path, thr=-50.0, need=0.05):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-t", "3", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    e = 20 * np.log10(np.sqrt((a[:len(a) // 160 * 160].reshape(-1, 160) ** 2).mean(1)) + 1e-9); run = 0
    for i, v in enumerate(e):
        run = run + 1 if v < thr else 0
        if run * 0.01 >= need: return t + (i + 1 - run) * 0.01
    return t + 3
VO0 = f"{J}/vo/vo_v2b_final.wav"
vw = json.load(open(f"{J}/vo/vo_v2b_final_words.json"))["words"]; plan = json.load(open(PLAN))
sb0, sb1 = plan["soundbite"]
bsrc = open(BUILD).read() if os.path.exists(BUILD) else ""
m = re.search(r'SB_FILE, SB_T0, SB_T1 = f"\{J\}/([^"]+)", ([\d.]+), ([\d.]+)', bsrc)
SB_SRC, SB_IN, SB_OUT = (f"{J}/{m.group(1)}", float(m.group(2)), float(m.group(3))) if m else (None, None, None)
ins_after = silence_after(vw[161]["s"], VO0) if "silence_after(vw[161]" in bsrc else vw[161]["e"]
shift = (sb0 - ins_after) + (sb1 - sb0) + 0.30
words = [dict(w, s=w["s"] + (shift if i > 161 else 0), e=w["e"] + (shift if i > 161 else 0)) for i, w in enumerate(vw)]
shots = json.load(open(EDIT)); sfx = json.load(open(SFXC))
# who or what each source shows (extend when new sources arrive)
def shows(v):
    f = (v.get("f") or "").lower(); s = v.get("s", 0)
    if v.get("k") == "grid9": return ["Elon Musk"]
    if "wef" in f: return ["Larry Fink"] if (260 <= s <= 400 or 1880 <= s <= 1900) else (["Elon Musk"] if 440 <= s <= 2060 else [])
    if "musk" in f or "s01_musk" in f or "colorado" in f or "april_2022" in f or "voa_musk" in f: return ["Elon Musk"]
    if "chancery" in f or "court" in f: return ["Delaware court"]
    if "giga" in f or ("voa_2billionaires" in f and 57 <= s <= 63): return ["Giga Texas"]
    if v.get("k") == "pol": return ["Elon Musk"]
    return []
SPOKEN = {"Elon Musk": ["elon", "musk"], "Larry Fink": ["fink", "larry"], "Delaware court": ["delawares", "court", "delaware"],
          "Giga Texas": ["texas"], "Wilmington, Delaware": ["delaware", "delawares"], "Austin, Texas": ["texas"]}
ALIAS = {"wilmington,delaware": "Wilmington, Delaware", "austin,texas": "Austin, Texas", "elonmusk": "Elon Musk", "larryfink": "Larry Fink"}

# ---------- overlays from the HyperFrames composition ----------
class P(HTMLParser):
    def __init__(s): super().__init__(); s.clips = []; s.stack = []; s.cur = None; s.depth = 0
    def handle_starttag(s, tag, a):
        a = dict(a)
        if "data-start" in a and "class" in a and "clip" in a["class"] and a.get("id") != "root":
            s.cur = {"id": a["id"], "t0": float(a["data-start"]), "t1": float(a["data-start"]) + float(a["data-duration"]), "text": []}; s.depth = 1; s.clips.append(s.cur)
            if a.get("data-daddy-region"): s.cur["region"] = tuple(float(x) for x in a["data-daddy-region"].split(","))   # real y extent, share of height
            return
        if s.cur is not None: s.depth += 1
    def handle_endtag(s, tag):
        if s.cur is not None:
            s.depth -= 1
            if s.depth <= 0: s.cur = None
    def handle_data(s, d):
        if s.cur is not None and d.strip(): s.cur["text"].append(html.unescape(d.strip()))
p = P(); p.feed(open(OVER).read()); overlays = p.clips
KIND = {"chy": "name label", "loc": "place label", "mk": "hand callout", "map": "route map", "tick": "ticker"}
REGION = {"name label": (0.66, 0.83), "place label": (0.11, 0.22), "hand callout": (0.08, 0.50), "route map": (0.0, 1.0), "ticker": (0.82, 0.88)}
for o in overlays: o["kind"] = KIND.get(o["id"].split("-")[0], "other"); o.setdefault("region", REGION.get(o["kind"], (0, 1)))

def caption_band(t):   # caption height per shot type, exactly as the v8 builder places it
    s = next((x for x in shots if x["t0"] <= t < x["t1"]), None); v = s["vis"] if s else {}
    if v.get("k") == "gfx" and v.get("type") in ("quote", "sting", "stamp"): return None
    y = 0.56 if v.get("type") in ("number", "counter") else 0.80 if v.get("type") in ("map", "grid", "shares", "crowd") else 0.70 if v.get("type") == "stamp" else 0.5
    return (y - 0.065, y + 0.02)
def caption_at(t):
    # 1-3 word groups as built in v8: the words spoken in the last 1.2 s
    return " ".join(w["w"] for w in words if w["s"] <= t <= w["e"] + 0.6)
def entity_history(name, t):
    keys = SPOKEN.get(name, [nrm(name)]); spoken = [w for w in words if w["s"] < t and nrm(w["w"]) in keys]
    shown = [s for s in shots if s["t0"] < t and name in shows(s["vis"])]
    return spoken, shown

# ---------- checks ----------
def review(item, everything):
    out = []; t0, t1 = item["t0"], item["t1"]; kind = item.get("kind", "other"); text = " ".join(item.get("text", []))
    if kind in ("name label", "place label"):
        ent = ALIAS.get(nrm(",".join(x for x in item.get("text", []) if x)[:40]).replace(",", ","), None) or (item.get("entity") or "")
        if not ent:
            for k in ALIAS:
                if all(part in nrm(text) for part in k.split(",")): ent = ALIAS[k]
        if ent:
            sp, sh = entity_history(ent, t0)
            if kind == "name label" and (len(sp) >= 2 or (len(sp) >= 1 and len(sh) >= 2)):   # shown but never named is still unknown
                out.append(("A1", "FAIL", f"{ent} is already established at {t0:.1f} s: named {len(sp)} times in the voice-over and shown in {len(sh)} shots before it"))
            elif kind == "place label" and len(sh) >= 2:
                out.append(("A1", "WARN", f"{ent} already shown in {len(sh)} shots before {t0:.1f} s"))
            else: out.append(("A1", "PASS", f"{ent}: named {len(sp)}x, shown {len(sh)}x before it, so the label is new information"))
    cap = nrm(caption_at((t0 + t1) / 2)); txt = nrm(text)
    if txt and cap and (txt in cap or (len(cap) > 3 and cap in txt)): out.append(("A2", "FAIL", f"on-screen text repeats the caption '{caption_at((t0+t1)/2)}'"))
    same = [o for o in everything if o is not item and o.get("kind") == kind and abs(o["t0"] - t0) < 8]
    if same and kind not in ("hand callout",): out.append(("A3", "WARN", f"another {kind} within 8 s ({', '.join(o['id'] for o in same)})"))
    if sum(1 for o in everything if o.get("kind") == kind) > (3 if kind != "hand callout" else 5): out.append(("A3", "WARN", f"more than the allowed count of {kind}s in the video"))
    r = item.get("region", (0, 1)); band = caption_band((t0 + t1) / 2)
    if kind != "route map" and band and r[0] < band[1] and r[1] > band[0] and caption_at((t0 + t1) / 2): out.append(("A4", "WARN", f"region {r} overlaps the caption band {tuple(round(x,2) for x in band)} while '{caption_at((t0+t1)/2)}' shows"))
    nums = re.findall(r"\$?\d[\d,.]*\s*(?:%|billion|trillion|[BT]\b)?", text)
    facts = open(DADDY).read().split("## 6. Facts")[1].split("## 7.")[0] if os.path.exists(DADDY) and "## 6. Facts" in open(DADDY).read() else ""
    for n in nums:
        if nrm(n) and nrm(n) not in nrm(facts): out.append(("A5", "FAIL", f"'{n.strip()}' is not in the facts table"))
    if any(s["vis"]["k"] == "blk" and s["t0"] <= t0 < s["t1"] for s in shots): out.append(("A6", "FAIL", "lands on the black breather card (a deliberate empty frame)"))
    if sb0 <= t0 < sb1 and kind != "name label": out.append(("A6", "FAIL", "lands on the soundbite (rule-break hold)"))
    if "purpose" in item and not item["purpose"].strip(): out.append(("A7", "FAIL", "no stated purpose"))
    return out

def verdict(res): return "REJECT" if any(r[1] == "FAIL" for r in res) else "ADD WITH CHANGES" if any(r[1] == "WARN" for r in res) else "ADD"

def strikes(path, start=0.0, dur=None):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    a = a[int(start * 16000):int((start + dur) * 16000) if dur else None]; e = 20 * np.log10(np.sqrt((a[:len(a) // 160 * 160].reshape(-1, 160) ** 2).mean(1)) + 1e-9)
    hits, last = [], -1
    for i in range(1, len(e)):   # a hit = a loud onset that rises out of near-silence (a boom's rumbling tail is not a new hit)
        if e[i] > e.max() - 14 and e[i - 1] < e[i] - 6 and e[max(0, i - 15):i].min() < e.max() - 30 and i - last > 30: hits.append(i / 100); last = i
    return hits
def audio_checks():
    out = []
    for c in sfx:
        h = strikes(f"{J}/sources/sfx/{c['sfx']}.mp3")
        if len(h) > 1: out.append(("A8", "FAIL", f"{c['sfx']} at {c['t']:.2f}s contains {len(h)} hits (at {', '.join(f'{x:.2f}' for x in h)} s in the file); trim to one"))
    lv = level_db(VO0, ins_after - 0.03)
    out.append(("A9", "PASS" if lv < -35 else "FAIL", f"voice-over split at {ins_after:.2f}s: level {lv:.0f} dB {'(silence)' if lv < -35 else '(inside a word)'}"))
    if SB_SRC:
        for nm, t in (("soundbite in", SB_IN), ("soundbite out", SB_OUT)):
            lv = level_db(SB_SRC, t - 0.03, 0.06)
            fw_ = json.load(open(f"{J}/research/wef_words.json"))["words"] if "wef" in SB_SRC else []
            cut = [w for w in fw_ if w["s"] < t < w["e"] - 0.02]
            nxt = next((w for w in fw_ if w["s"] >= t), None)
            msg = f"{nm} at {t:.2f}s (source): level {lv:.0f} dB"
            if nm == "soundbite out" and cut: out.append(("A9", "FAIL", msg + f", cuts the word '{cut[0]['w']}'"))
            else: out.append(("A9", "PASS" if lv < -30 or nm == "soundbite out" else "WARN", msg + (f"; next word '{nxt['w']}' at {nxt['s']:.2f}s" if nxt else "")))
    return out
def geometry_checks():
    out = []; src = open(OVER).read()
    for o in overlays:
        if o["kind"] != "hand callout": continue
        g = next((s for s in shots if s["t0"] <= o["t0"] + 0.05 < s["t1"]), None)
        if g and g["vis"].get("k") == "gfx" and f'follow("{o["id"]}"' not in src:
            out.append(("A10", "FAIL", f"{o['id']} is drawn on a {g['vis'].get('type')} that pushes in 5% but does not follow it: it drifts off target"))
        elif g: out.append(("A10", "PASS", f"{o['id']} follows its graphic's push-in"))
    return out
if CMD == "audit":
    print(f"Audit of the current edit: {len(shots)} shots, {len(overlays)} overlays, {len(sfx)} sound effects\n")
    for o in overlays:
        res = review(o, overlays); print(f"{o['id']:<10} {o['t0']:6.2f}-{o['t1']:6.2f}s {o['kind']:<12} {verdict(res):<17} | " + " ; ".join(f"{a} {b}: {c}" for a, b, c in res if b != "PASS") or "")
    names = [s["sfx"] for s in sfx]
    for i, s in enumerate(sfx):
        near = [x for x in sfx if x is not s and x["sfx"] == s["sfx"] and abs(x["t"] - s["t"]) < 8]
        if near: print(f"SFX {s['sfx']} at {s['t']:.2f}s  A3 WARN: same sound again within 8 s")
    print("\nSFX reuse counts:", {n: names.count(n) for n in sorted(set(names)) if names.count(n) > 1})
    print("\nAudio and geometry checks:")
    for a, b, c in audio_checks() + geometry_checks(): print(f"  {a} {b}: {c}")
elif CMD == "check":
    item = json.load(open(sys.argv[3])); item.setdefault("text", [item.get("text_on_screen", "")]); item.setdefault("region", REGION.get(item.get("kind"), (0, 1)))
    res = review(item, overlays + [item]); v = verdict(res)
    print(f"Proposal: {item.get('what')}  ({item['t0']}-{item['t1']} s, {item.get('kind')})")
    for a, b, c in res: print(f"  {a} {b}: {c}")
    print(f"  Automatic verdict: {v}")
    print("  Now answer the six judgment questions in DADDY.md section 0 and log the decision in section 9.")
elif CMD == "sync":
    lines = ["<!-- AUTO:BEGIN (generated by tools/daddy.py sync; do not edit by hand) -->", "", "### Shots (cut on the 96 bpm grid at the word)", "",
             "| # | in s | out s | word | picture | effect | shows |", "|---|---|---|---|---|---|---|"]
    for i, s in enumerate(shots):
        v = s["vis"]; pic = v.get("f") or v.get("type") or v["k"]
        if v["k"] == "clip": pic = f"{os.path.basename(v['f'])} @{v['s']:.1f}s ({v.get('look','')})"
        if v["k"] == "gfx" and v.get("bg"): pic = f"{v['type']} over {os.path.basename(v['bg']['f'])}"
        if v.get("punch"): pic += " (punch-in)"
        w = s["word"]; ww = words[int(w)]["w"] if w.isdigit() else w
        lines.append(f"| {i+1} | {s['t0']:.2f} | {s['t1']:.2f} | {ww} | {pic} | {s['fx']} | {', '.join(shows(v))} |")
    lines += ["", "### Overlays (HyperFrames layer)", "", "| id | in s | out s | kind | text |", "|---|---|---|---|---|"]
    for o in overlays: lines.append(f"| {o['id']} | {o['t0']:.2f} | {o['t1']:.2f} | {o['kind']} | {' / '.join(o['text'])[:90]} |")
    lines += ["", "### Sound effects", "", "| s | sound | gain dB |", "|---|---|---|"] + [f"| {x['t']:.2f} | {x['sfx']} | {x['gain_db']} |" for x in sfx]
    lines += ["", "### Who is on screen and when (first name in voice-over, first time shown)", ""]
    for ent in ("Elon Musk", "Larry Fink"):
        sp, _ = entity_history(ent, 999); sh = [s for s in shots if ent in shows(s["vis"])]
        lines.append(f"- {ent}: named {len(sp)} times, first at {sp[0]['s']:.2f} s; on screen in {len(sh)} shots, first at {sh[0]['t0']:.2f} s" if sp and sh else f"- {ent}: on screen in {len(sh)} shots" + (f", first at {sh[0]['t0']:.2f} s" if sh else ""))
    lines.append("\n<!-- AUTO:END -->")
    d = open(DADDY).read(); a, b = d.index("<!-- AUTO:BEGIN"), d.index("<!-- AUTO:END -->") + len("<!-- AUTO:END -->")
    open(DADDY, "w").write(d[:a] + "\n".join(lines) + d[b:]); print(f"synced: {len(shots)} shots, {len(overlays)} overlays, {len(sfx)} SFX")
