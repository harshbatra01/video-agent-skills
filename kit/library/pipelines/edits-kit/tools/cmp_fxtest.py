"""Compare sheets for the fx test reel (pilot/plan_fxtest.json) against the reference moments each transition copies.
usage: python cmp_fxtest.py [ROUND_TAG]   -> pilot/qa/cmp_<tag>_1.png and _2.png
Reads the cut times from plan_fxtest.json, so the sheet follows whatever the test plan holds.
"""
import sys, os, glob, json, subprocess
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
tag = sys.argv[1] if len(sys.argv) > 1 else "r"
R = sorted(glob.glob(os.path.join(KIT, "refs", "*.mp4"))) + sorted(glob.glob(os.path.join(KIT, "refs2", "*.mp4")))
def f(key): return [x for x in R if key.lower() in os.path.basename(x).lower()][0]
REF = {   # transition type -> (reference video, start time, crop) : the moment it was copied from
    "blowout": (f("Ultimate Football"), 106.57, "438,0,842,720"),
    "zoomrush": (f("Speed x Ronaldo"), 12.50, None),
    "smear_v": (f("Lebron"), 16.82, None),
    "smear_h": (f("SHOCK"), 13.33, None),
    "vortex": (f("Lebron"), 29.32, None),
    "edges": (f("Lebron"), 41.83, None),
    "recipe": (f("Lebron"), 41.83, None),
    "paint": (f("SHOCK"), 13.33, None),
    "flood": (f("NIGHTCRAWLER"), 20.78, None),
    "defocus": (f("+5 HOURS"), 14.35, None),
    "rays": (f("Speed x Ronaldo"), 26.30, None),
}
plan = json.load(open(os.path.join(KIT, "pilot", "plan_fxtest.json")))
O = os.path.join(KIT, "pilot", "renders", plan["name"] + ".mp4"); B = f"{plan['band'][0]},{plan['band'][1]}"
pairs, seen = [], set()
for tr in plan["transitions"]:
    key = tr["type"] if tr["type"] != "smear" else ("smear_v" if tr.get("vertical", True) else "smear_h")
    if key not in REF or (tr["type"] == "smear" and any(abs(tr["t"] - t2["t"]) < 0.2 and t2["type"] == "edges" for t2 in plan["transitions"])): continue
    if key in seen: continue
    seen.add(key); rv, rt, crop = REF[key]
    pairs.append(f"{O}@{round(tr['t'] - 3 / 30, 3)}@{B}|{rv}@{rt}" + (f"@{crop}" if crop else "") + f"|{key}")
half = (len(pairs) + 1) // 2
for i, chunk in enumerate((pairs[:half], pairs[half:])):
    out = os.path.join(KIT, "pilot", "qa", f"cmp_{tag}_{i + 1}.png")
    r = subprocess.run(["python", "-I", os.path.join(KIT, "tools", "compare.py"), out] + chunk + ["--n", "12", "--h", "96", "--stats"], capture_output=True, text=True, encoding="utf-8", errors="replace")
    print(r.stdout.strip(), r.stderr[-300:])
