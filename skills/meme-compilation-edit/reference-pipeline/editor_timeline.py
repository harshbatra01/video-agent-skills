"""A human editor's finished cut (gunzipped .prproj as data/editor_cut.xml): voice clips on V1/A1 and meme items on V3,
in seconds, for the blur and crop pass (plan_pass.py)."""
import json, sys
sys.path.insert(0, "review_tools")
from tl import TL, TPS
SEQ = "CHANGE_ME sequence"          # the editor's sequence name
T = TL("data/editor_cut.xml", seq_name=SEQ)
out = {}
for k in ("V1", "A1", "V2", "V3", "V4", "V5"):
    out[k] = [{"name": d["name"], "start": round(d["start"] / TPS, 4), "end": round(d["end"] / TPS, 4),
               "in": round(d["in"] / TPS, 4) if d["in"] is not None else None, "speed": d["speed"]} for d in T.tracks[k]["items"]]
json.dump(out, open("data/editor_timeline.json", "w"), indent=0)
v1 = out["V1"]
print({k: len(v) for k, v in out.items()}, "| seq end", max(d["end"] for d in v1), "| src span", min(d["in"] for d in v1), max(d["in"] + d["end"] - d["start"] for d in v1))
same = sum(1 for a, b in zip(out["V1"], out["A1"]) if abs(a["start"] - b["start"]) < 0.01 and abs(a["in"] - b["in"]) < 0.01)
print("V1/A1 matching clips:", same)
gaps = [round(b["start"] - a["end"], 3) for a, b in zip(v1, v1[1:]) if b["start"] - a["end"] > 0.001]
print("V1 holes:", len(gaps), gaps[:5])
pieces = [{"a": d["in"], "b": round(d["in"] + d["end"] - d["start"], 4), "seq": d["start"]} for d in v1]
json.dump({"pieces": pieces}, open("regions_full.json", "w"))
v3 = out["V3"]
print("V3 first/last:", v3[0]["name"], v3[0]["start"], "|", v3[-1]["name"], v3[-1]["end"])
print("V3 kinds:", sorted({d["name"].rsplit(".", 1)[-1].lower() if "." in d["name"] else d["name"] for d in v3}))
