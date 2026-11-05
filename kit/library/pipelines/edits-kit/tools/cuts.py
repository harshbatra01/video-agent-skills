"""Cut timing helpers: put cuts on the strongest drum hits, check a plan's sync before rendering.

as a module:
  H = hits(beats_json, song_in, dur)          [(edit t, strength 0-1)] kicks + snares, strength relative to the loudest
  t = on(t_plan, H, win=0.2)                  the strongest hit near t_plan (distance-weighted), floored to a frame
  fr(t, fps)                                  floor to a frame start (cut lands 0-1 frame BEFORE the hit, like top edits)
CLI: python cuts.py PLAN.json BEATS.json SONG_IN    -> every cut with its nearest hit, offset in frames, strength
Why: a fixed beat grid drifts off a real performance (this song's snares swing up to 0.15 s), and the strongest hits are
not evenly spaced. Measured on top edits: cuts land on strong kicks/snares 0-1 frame early.
"""
import sys, json, math


def hits(beats_json, song_in, dur, kinds=("kicks", "snares")):
    b = json.load(open(beats_json))
    raw = [(t - song_in, s) for k in kinds for t, s in b[k] if song_in <= t < song_in + dur]
    mx = max(s for _, s in raw) if raw else 1
    merged = []
    for t, s in sorted(raw):                       # kick + snare on the same instant = one hit, keep the stronger
        if merged and t - merged[-1][0] < 0.03: merged[-1] = (merged[-1][0], max(merged[-1][1], s / mx))
        else: merged.append((t, s / mx))
    return merged


def fr(t, fps=30):
    return math.floor(t * fps + 1e-6) / fps


def on(t, H, win=0.2, fps=30, min_s=0.0):
    best, score = None, -1
    for h, s in H:
        if abs(h - t) <= win and s >= min_s:
            sc = s * (1 - 0.5 * abs(h - t) / win)
            if sc > score: best, score = h, sc
    return round(fr(best if best is not None else t, fps), 4)


def report(plan, H, fps=30, strong=0.5):
    cuts = sorted(set(round(c["t0"], 3) for c in plan["clips"] if c["t0"] > 0.01))
    on_hit = 0
    for t in cuts:
        near = [x for x in H if -1.5 / fps <= t - x[0] <= 0.5 / fps]     # strongest hit the cut could belong to
        h, s = max(near, key=lambda x: x[1]) if near else min(H, key=lambda x: abs(x[0] - t))
        off = (t - h) * fps; ok = -1.5 <= off <= 0.5 and s >= strong; on_hit += ok
        print(f"cut {t:6.2f}  hit {h:6.2f} s{s:.2f}  {off:+.1f} f  {'ok' if ok else '--'}")
    print(f"{on_hit}/{len(cuts)} cuts on a strong hit (0-1 frame early)")


if __name__ == "__main__":
    plan = json.load(open(sys.argv[1], encoding="utf-8"))
    report(plan, hits(sys.argv[2], float(sys.argv[3]), plan["dur"]), plan.get("fps", 30))
