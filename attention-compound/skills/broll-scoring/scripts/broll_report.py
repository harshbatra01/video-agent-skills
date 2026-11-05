# Builds BROLL-REPORT tables and totals from <prefix>_metrics.json (measured) + labels.py (eye labels).
# python3 -I broll_report.py <report/broll dir>  -> prints markdown to stdout (column names: REF_LABEL, OURS_LABEL env)
import json, sys, importlib.util
from collections import defaultdict
D = sys.argv[1]
sp = importlib.util.spec_from_file_location("labels", f"{D}/labels.py"); L = importlib.util.module_from_spec(sp); sp.loader.exec_module(L)
def load(px, lab):
    rows = json.load(open(f"{D}/{px}_metrics.json")); lab = L.parse(lab)
    for r in rows:
        r.update(lab[r["n"]]); r["S"] = (2 * r["M"] + r["Q"] + r["F"]) / 2
    return rows
def stats(rows):
    T = sum(r["dur"] for r in rows); w = lambda k: sum(r[k] * r["dur"] for r in rows) / T
    pic = [r for r in rows if r["type"] not in ("card",)]; Tp = sum(r["dur"] for r in pic)
    by = defaultdict(float)
    for r in rows: by[r["type"]] += r["dur"]
    return dict(T=T, n=len(rows), S=w("S"), M=w("M"), Q=w("Q"), F=w("F"),
                weak=sum(r["dur"] for r in rows if r["S"] < 5), weakn=sum(1 for r in rows if r["S"] < 5),
                small=sum(r["dur"] for r in pic if r["subj"] < 20) / Tp, mis=sum(r["dur"] for r in rows if r["M"] <= 2),
                by={k: v / T for k, v in by.items()})
R, O = load("ref", L.REF), load("ours", L.OURS); a, b = stats(R), stats(O)
p = lambda x: f"{100*x:.0f}%"
import os
print(f"| Measure | {os.environ.get('REF_LABEL', 'Reference')} | {os.environ.get('OURS_LABEL', 'Ours')} |\n|---|---|---|")
for nm, k, f in [("Shots", "n", "{:.0f}"), ("Length (s)", "T", "{:.1f}"), ("B-roll score /10 (time-weighted)", "S", "{:.1f}"),
                 ("Match to words /5", "M", "{:.2f}"), ("Quality /5", "Q", "{:.2f}"), ("Framing /5", "F", "{:.2f}")]:
    print(f"| {nm} | {f.format(a[k])} | {f.format(b[k])} |")
print(f"| Weak shots (score under 5) | {a['weakn']} shots, {a['weak']:.1f} s | {b['weakn']} shots, {b['weak']:.1f} s |")
print(f"| Time on shots that miss the words (match 2 or less) | {a['mis']:.1f} s ({p(a['mis']/a['T'])}) | {b['mis']:.1f} s ({p(b['mis']/b['T'])}) |")
print(f"| Picture time where the subject fills under 20% of frame | {p(a['small'])} | {p(b['small'])} |")
for t in ["clip", "still", "news", "grid", "gfx", "card"]:
    print(f"| Screen time: {t} | {p(a['by'].get(t,0))} | {p(b['by'].get(t,0))} |")
for title, rows in [("Reference: every shot", R), (f"{os.environ.get('OURS_LABEL', 'Ours')}: every shot", O)]:
    print(f"\n### {title}\n\n| # | in s | len s | said | shows | type | subject % | Q | F | M | score | sharp | note |\n|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for r in rows:
        print(f"| {r['n']} | {r['t0']:.2f} | {r['dur']:.2f} | {r['said']} | {r['shows']} | {r['type']} | {r['subj']} | {r['Q']} | {r['F']} | {r['M']} | **{r['S']:.1f}** | {r['sharp']} | {r['note']} |")
