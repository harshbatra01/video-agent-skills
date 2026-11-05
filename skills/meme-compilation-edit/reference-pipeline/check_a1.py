"""After the build: every A1 clip in the saved project matches the cut plan (raw in/out and timeline start)."""
import json, sys
sys.path.insert(0, "review_tools")   # usage: check_a1.py saved.xml "sequence name" [edl_full.json]
from tl import TL, TPF
E = json.load(open(sys.argv[3] if len(sys.argv) > 3 else "edl_full.json"))
T = TL(sys.argv[1], sys.argv[2])
items = T.tracks["A1"]["items"]
got = [(d["in"] // TPF, (d["in"] + d["end"] - d["start"]) // TPF, d["start"] // TPF) for d in items]
want = [(c["raw_in_f"], c["raw_out_f"], c["out_start_f"]) for c in E["cuts"]]
bad = [(g, w) for g, w in zip(got, want) if g != w]
print(f"A1 clips {len(got)} vs plan {len(want)}; mismatches {len(bad) + abs(len(got) - len(want))}", bad[:5])
