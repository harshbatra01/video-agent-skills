"""Which file Drive's preview shows, from the title-bar OCR (2 fps). Whole-title match first (names with spaces)."""
import json, os, re, difflib
CLIENT = "/CHANGE/ME/client folder/"
files = sorted(f for f in os.listdir(CLIENT) if not f.startswith("."))
def best_file(txt):
    t = txt.replace("•", "").strip()
    cands = []
    for f in files:
        r = difflib.SequenceMatcher(None, t.lower(), f.lower()).ratio()
        r2 = difflib.SequenceMatcher(None, t.split(" ")[0].lower(), f.lower()).ratio()
        cands.append((max(r, r2 if " " not in f else 0), f))
    sc, f = max(cands)
    return f if sc >= 0.72 else None
seq = []
for line in open("title_ocr.jsonl"):
    r = json.loads(line)
    t = (int(re.search(r"t_(\d+)", r["file"]).group(1)) - 1) / 2
    txt = " ".join(L["t"] for L in r.get("lines", [])).strip()
    seq.append((t, best_file(txt) if txt else None, txt))
seq.sort()
runs = []
for t, n, txt in seq:
    if runs and runs[-1]["file"] == n:
        runs[-1]["b"] = t + 0.5
    else:
        runs.append({"file": n, "a": t, "b": t + 0.5, "title": txt[:60]})
json.dump(runs, open("screen_runs.json", "w"), indent=0)
order = []
for v in [r for r in runs if r["file"] and r["b"] - r["a"] >= 1.5]:
    if order and order[-1]["file"] == v["file"]:
        order[-1]["b"] = v["b"]
    else:
        order.append(dict(v))
print(len(runs), "runs;", len(order), "stable visits;", len(set(v["file"] for v in order)), "distinct files")
for v in order:
    print(f"{v['a']:7.1f}-{v['b']:7.1f} ({v['b']-v['a']:5.1f}s) {v['file']}")
