#!/usr/bin/env python3
# Scriptable checks from edit-loop-guard. Warns and fails, never edits anything. The user decides.
#   guard_check.py <storyboard.json> [--locked locked.json] [--video render.mp4]
# storyboard.json: {"shots":[{"t0","t1","idea","kind":"video|still|graphic|black","asset","source","must_read":false}],
#                   "sfx":[{"t","sfx"}]}
# locked.json: [{"id","field","value","shot_index"}] where field is a key of that shot.
# Limits approved by the user on 4 Nov 2026, see REFERENCE-STUDY.md. Moving share target is about 67% by hand labels.
import json,sys,os,subprocess,argparse
OPEN=5.0; MAX_IDEAS=2; MAX_ROUGH_HITS=20; MAX_MUST_READ=0; TARGET_MOVING=67
HIT_SCALE=41/28   # rough count found 41 hits where the Elon v18 cue list had 28
p=argparse.ArgumentParser(); p.add_argument("board"); p.add_argument("--locked"); p.add_argument("--video"); a=p.parse_args()
B=json.load(open(a.board)); S=B["shots"]; X=B.get("sfx",[]); out=[]
def add(i,l,m): out.append((i,l,m))
first=[s for s in S if s["t0"]<OPEN]
ideas=[]
for s in first:
    if s.get("idea") and s["idea"] not in ideas: ideas.append(s["idea"])
add("G1","PASS" if len(ideas)<=MAX_IDEAS else "FAIL",f"ideas in the first 5 s: {len(ideas)} (limit {MAX_IDEAS}): {', '.join(ideas)}")
cues=sum(1 for c in X if c["t"]<OPEN); est=round(cues*HIT_SCALE)
add("G2","PASS" if est<=MAX_ROUGH_HITS else "FAIL",f"planned sound cues in the first 5 s: {cues}, about {est} rough hits (limit {MAX_ROUGH_HITS})")
mr=[s for s in first if s.get("must_read")]
add("G3","PASS" if len(mr)<=MAX_MUST_READ else "FAIL",f"graphics to read in the first 5 s: {len(mr)} (limit {MAX_MUST_READ})")
tot=sum(s["t1"]-s["t0"] for s in S) or 1; mv=sum(s["t1"]-s["t0"] for s in S if s.get("kind")=="video")/tot*100
add("G4","PASS" if mv>=TARGET_MOVING else "WARN",f"planned moving footage: {mv:.0f}% (target about {TARGET_MOVING}%)")
xs=sorted(X,key=lambda c:c["t"])
rep=[(u["sfx"],round(u["t"],2)) for u,v in zip(xs,xs[1:]) if u["sfx"]==v["sfx"] and v["t"]-u["t"]>0.25]
add("G5","PASS" if not rep else "WARN",f"same sound back to back: {len(rep)}"+(f", first at {rep[0][1]} s" if rep else "")+" (rapid bursts under 0.25 s are not counted)")
miss=[i+1 for i,s in enumerate(S) if not s.get("asset") or not s.get("source")]
add("G6","PASS" if not miss else "FAIL",f"shots missing an asset or source: {len(miss)}"+(f", first is shot {miss[0]}" if miss else ""))
gaps=[round(u["t1"],2) for u,v in zip(S,S[1:]) if v["t0"]-u["t1"]>0.02]
add("G7","PASS" if not gaps else "FAIL",f"gaps in the timeline: {len(gaps)}"+(f", first at {gaps[0]} s" if gaps else ""))
if a.locked:
    bad=[]
    for L in json.load(open(a.locked)):
        i=L.get("shot_index")
        if i is None or i>=len(S) or S[i].get(L["field"])!=L["value"]: bad.append(L["id"])
    add("G8","PASS" if not bad else "FAIL",f"locked items changed or missing: {len(bad)}"+(f": {', '.join(bad)}" if bad else ""))
if a.video:
    T=os.path.dirname(os.path.abspath(__file__))
    h=json.loads(subprocess.run([sys.executable,f"{T}/sound_hits.py",a.video],capture_output=True,text=True).stdout)
    add("G9","PASS" if h["first5"]<=MAX_ROUGH_HITS else "FAIL",f"rough sound hits in the render, first 5 s: {h['first5']} (limit {MAX_ROUGH_HITS})")
    c=json.loads(subprocess.run([sys.executable,f"{T}/colour_stats.py","render",a.video],capture_output=True,text=True).stdout)
    v=c["vivid_hue_share_pct"]; blue=v["cyan_blue"]; br=c["mean_brightness"]
    add("G10","PASS" if br>=0.30 and blue>=20 else "WARN",f"colour: brightness {br} (Altman 0.36), blue {blue}% of vivid pixels (Altman 34%). A warning light only, the user's eye decides")
for r in out: print(f"{r[0]:<4}{r[1]:<5}{r[2]}")
n=sum(1 for r in out if r[1]=="FAIL"); print(f"\n{n} fail, {sum(1 for r in out if r[1]=='WARN')} warn. Not checked by script: stranger test, B-roll match, sound sync, taste.")
sys.exit(1 if n else 0)
