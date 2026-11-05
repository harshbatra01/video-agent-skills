#!/usr/bin/env python3
# Collects the per-reel numbers from raw/<id>/ into numbers.json. Same tool and threshold for every reel.
import json, numpy as np
R = ["DclpjyxhKF6", "DdHKc5GBqT-", "Dee-mp9BJqG", "DfFsUfUx0dZ"]; out = {}
for id in R:
    d = f"raw/{id}"; sh = json.load(open(f"{d}/shots_ref.json")); mo = json.load(open(f"{d}/motion.json"))
    ev = json.load(open(f"{d}/events.json")); fps = ev["fps"]; sc = json.load(open(f"{d}/scores.json"))["frames"]
    tr = json.load(open(f"../../reference-reels/{id}/reel.transcript.json")); W = tr["words"]; dur = len(sc) / fps
    inv = json.load(open(f"{d}/inverted.json"))["times"]; m = []
    for t in inv:
        if not m or t - m[-1] > 0.2: m.append(t)
    dd = np.array([s["dur"] for s in sh]); fr = np.array([s["frames"] for s in sh])
    q = [round(sum(1 for s in sh if a * dur / 4 <= s["t0"] < (a + 1) * dur / 4) / (dur / 4), 2) for a in range(4)]
    vid = sum(o["dur"] for o in mo if o["kind"] == "video"); st = sum(o["dur"] for o in mo if o["kind"] == "still")
    col = json.load(open(f"{d}/colour.json")); gl = json.load(open(f"{d}/gap_level.json")); bm = json.load(open(f"{d}/beat_map.json"))
    sw = json.load(open(f"{d}/shotwords/sw_shots.json"))
    out[id] = dict(duration_s=round(dur, 1), fps=fps, words=len(W), wpm=gl["wpm"],
        shots_cut_events=len(sh), micro_shots_inside_events=None, median_shot_s=round(float(np.median(dd)), 2), p90_shot_s=round(float(np.percentile(dd, 90)), 2),
        longest_shot_s=round(float(dd.max()), 2), shots_per_s=round(len(sh) / dur, 2), shots_le_4_frames_pct=round(100 * float((fr <= 4).mean()), 1),
        shots_first_5s=sum(1 for s in sh if s["t0"] < 5), words_first_5s=sum(1 for w in W if w["s"] < 5),
        cuts_per_s_by_quarter=q, shots_ffmpeg_scene_025=len(sw),
        cut_plus_flash_events=sum(1 for e in ev["events"] if e["kind"] == "CUT+FLASH"), flicker_events=sum(1 for e in ev["events"] if e["kind"] == "FLICKER"),
        inverted_frame_events=len(m), inverted_per_min=round(len(m) / dur * 60, 1),
        moving_share_tool_pct=round(100 * vid / dur), still_share_tool_pct=round(100 * st / dur),
        near_mono_shots_pct=round(100 * sum(1 for s in sh if s["sat"] < 12) / len(sh)),
        near_black_frames_pct=round(100 * sum(1 for x in sc if x["luma"] < 12) / len(sc), 1),
        bright_frames_pct=round(100 * sum(1 for x in sc if x["luma"] > 200) / len(sc), 1),
        colour=dict((k, col[k]) for k in ("mean_brightness", "mean_saturation", "colourfulness_median", "vivid_pixels_pct", "near_black_pct", "near_grey_pct", "vivid_hue_share_pct")),
        music_under_voice_db=gl["music_under_voice_db"], voice_gap_total_s=gl["gap_s"], tail_after_voice_s=gl["tail_s"],
        bpm_fit=bm["bpm"], onsets_on_grid=bm["onsets_on_grid"], onsets_chance=bm["chance"], cuts_on_beat=bm["cuts_on_beat"], cuts_on_beat_chance=bm["cuts_on_beat_chance"])
    rs = open(f"{d}/ref_stats.txt").read(); import re
    out[id]["micro_shots_inside_events"] = int(re.search(r"\+(\d+) micro", rs).group(1))
    out[id]["cuts_within_012s_of_word_start_pct"] = int(re.search(r"word start: (\d+)%", rs).group(1))
json.dump(out, open("numbers.json", "w"), indent=1)
keys = [k for k in out[R[0]] if k != "colour"]
for k in keys: print(f"{k:36}", " | ".join(str(out[i][k]) for i in R))
for k in out[R[0]]["colour"]: print(f"{k:36}", " | ".join(str(out[i]["colour"][k]) for i in R))
