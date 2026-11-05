# Shot table + pacing stats from events.json, scores.json, transcript.json and the video.
import json, subprocess, sys
import numpy as np
A = sys.argv[1]; video = sys.argv[2]; tr = sys.argv[3]
E = json.load(open(f"{A}/events.json")); fps = E["fps"]; S = json.load(open(f"{A}/scores.json"))["frames"]; n = len(S)
W = json.load(open(tr))["words"]
cuts = [e["start"] for e in E["events"] if e["kind"].startswith("CUT")]
# micro-shots inside long events: count frames whose own diff is a jump (>40) within the event
micro = sum(sum(1 for i in range(e["start"] + 1, e["end"] + 1) if S[i]["diff"] > 40) for e in E["events"] if e["frames"] >= 3)
bounds = [0] + cuts + [n]
w, h = 64, 48
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", video, "-vf", f"scale={w}:{h}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
V = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32)
shots = []
for a, b in zip(bounds, bounds[1:]):
    if b <= a: continue
    m = V[(a + b) // 2]; sat = float((m.max(2) - m.min(2)).mean())
    t0, t1 = a / fps, b / fps
    said = " ".join(x["w"] for x in W if x["s"] < t1 and x["e"] > t0)
    shots.append({"t0": round(t0, 2), "t1": round(t1, 2), "dur": round(t1 - t0, 2), "frames": b - a, "sat": round(sat, 1), "said": said})
json.dump(shots, open(f"{A}/shots_ref.json", "w"), indent=0)
d = np.array([s["dur"] for s in shots])
print(f"shots {len(shots)} (+{micro} micro-shots inside montage events) | median {np.median(d):.2f}s mean {d.mean():.2f}s | under 0.25s: {(d<0.25).sum()} | over 1.5s: {(d>1.5).sum()}")
secs = [("hook 0-5", 0, 5), ("context 5-20", 5, 20), ("turn 20-28", 20, 28), ("escalation 28-45", 28, 45), ("fallout 45-60", 45, 60), ("peg 60-75", 60, 75), ("kicker 75-86.5", 75, 87)]
for nm, a, b in secs:
    dd = [s["dur"] for s in shots if a <= s["t0"] < b]
    print(f"  {nm:18} shots {len(dd):3}  median {np.median(dd):.2f}s  cuts/s {len(dd)/(b-a):.2f}")
starts = np.array([x["s"] for x in W]); ends = np.array([x["e"] for x in W])
ct = np.array([c / fps for c in cuts])
near_start = np.mean([np.min(np.abs(starts - t)) <= 0.12 for t in ct])
mid_word = np.mean([any((starts + 0.08 < t) & (t < ends - 0.08)) for t in ct])
gaps = np.mean([np.min(np.abs(starts - t)) for t in ct])
print(f"cuts within 0.12s of a word start: {near_start:.0%} | cuts inside a word: {mid_word:.0%} | mean distance to nearest word start {gaps:.2f}s")
print(f"words per shot: {len(W)/len(shots):.2f} | shots per sentence approx: {len(shots)/ sum(1 for x in W if x['w'][-1] in '.?!'):.1f}")
bw = sum(1 for s in shots if s["sat"] < 12); print(f"near-monochrome shots (low saturation): {bw}/{len(shots)} = {bw/len(shots):.0%}")
lu = np.array([x["luma"] for x in S]); print(f"flash frames (luma > 200): {(lu>200).sum()} | near-black frames (luma < 12): {(lu<12).sum()} = {(lu<12).mean():.0%} of runtime")
