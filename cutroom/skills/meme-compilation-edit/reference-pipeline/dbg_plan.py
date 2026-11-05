import json, os, sys
from plan_blurs import plan, words_of, display_name_lines, is_ui, make_blocks
pieces = json.load(open("assign.json")); dec = json.load(open("decisions.json"))
cut = set(dec["cut"])
for k, f in dec["reassign"].items(): pieces[int(k)]["meme"] = f
for k, b in dec.get("trim", {}).items():
    pieces[int(k)]["b"] = b; pieces[int(k)]["words"] = [w for w in pieces[int(k)]["words"] if w["s"] < b]
ocr = {}
for l in open("img_ocr.jsonl"):
    r = json.loads(l); ocr[os.path.basename(r["file"]).replace(".webp.png", ".webp").replace(".WEBP.png", ".WEBP").replace(".mp4.png", ".mp4")] = r
for name in sys.argv[1:]:
    idx = [i for i, p in enumerate(pieces) if p["meme"] == name and i not in cut]
    timed = []
    for i in idx:
        pc = pieces[i]
        for w in pc["words"]:
            for ww in words_of(w["w"]):
                timed.append((ww, max(w["s"], pc["a"]), w["e"]))
    print("=====", name, "pieces", idx)
    print("  spoken:", " ".join(t[0] for t in timed))
    o = ocr[name]
    names = display_name_lines(o["lines"])
    for L in o["lines"]:
        print(f"   {'UI ' if is_ui(L, names) else '   '}{L['b'][0]:.3f},{L['b'][1]:.3f},{L['b'][2]:.3f},{L['b'][3]:.3f} {L['t']}")
    blocks, blurs = plan(o["lines"], timed)
    for b in blocks:
        print("  BLOCK", b["read_t"], "|", " / ".join(L["t"] for L in b["lines"]))
    for b in blurs:
        print("  BLUR", b["kind"], b.get("raw_t", b.get("raw_first")), b.get("raw_last", ""), "|", " / ".join(L["t"] for L in b.get("lines", [])) or b.get("word"))
