# v8b builder (v8 plus the 19 Oct second notes: the voice-over is split in real silence (after "dollars", not inside it);
# Fink's soundbite runs to the end of "congratulations"; the gavel is one strike; a limiter holds the true peak).
# v8 builder (v7 plus the 19 Oct notes: real, varied SFX only at shifts; Fink's audio fixed; chromatic aberration at the
# borders only; VOIDED and REVERSED redesigned). v7 notes follow.
# v7 builder: reference style, video first. Music plan (96 bpm) -> edit plan (cuts on the grid at the word, B-roll is moving
# footage wherever a licensed clip exists) -> score with a sound on every cut -> picture -> mix. New against v6:
#  - clips from sources/video (WEF 2026 Musk and Fink, VOA, NASA/SpaceX, courtroom, padlock, CNBC host, Cybertruck)
#  - graphics drawn over darkened moving footage, never on an empty brown card (one black card kept as the rule break: "But")
#  - 9-grid sequence on "It's what happens ... take it away": cells flash white, Musk enters from the right through a
#    negative frame, lands as a black-and-white cut-out, cells fill with playing clips, slow push in
#  - the rule break: Larry Fink's real line plays with its own sound for 5 s (voice-over pauses, one held shot)
#  - frame-edge look on every frame (edge blur, wide magenta/green fringe, pink rim), flicker on stills
#  - subtitles: Didot Italic + tight Helvetica Neue Bold, white on dark, black on bright (picked per frame)
# python3 build_v7.py <job_dir> <out.mp4>     (TEST=1 for a one-frame-per-shot sheet)
import json, os, re, subprocess, sys, hashlib
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont, ImageOps
J, OUTF = sys.argv[1], sys.argv[2]
sys.path.insert(0, os.path.join(J, "tools")); import synth
from scipy.io import wavfile
W, H, FPS = 1080, 1920, 30
BPM = 96.0; S16 = 60 / BPM / 4
def snap(t): return round(t / S16) * S16

# ---------------- voice with the inserted soundbite ----------------
VO0 = f"{J}/vo/vo_v2b_final.wav"; vw = json.load(open(f"{J}/vo/vo_v2b_final_words.json"))["words"]
SB_FILE, SB_T0, SB_T1 = f"{J}/sources/video/v_wef_musk_2026.webm", 366.45, 372.27   # 372.27: measured end of "congratulations" (Musk's "Oh" follows)   # Fink: "...so congratulations."
def silence_after(t, path, thr=-50.0, need=0.05):   # first real silence (-50 dB: a word tail at -34 dB is still the word) after t on the waveform (word timings are not enough)
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", path, "-t", "3", "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    e = 20 * np.log10(np.sqrt((a[:len(a) // 160 * 160].reshape(-1, 160) ** 2).mean(1)) + 1e-9); run = 0
    for i, v in enumerate(e):
        run = run + 1 if v < thr else 0
        if run * 0.01 >= need: return t + (i + 1 - run) * 0.01
    return t + 3
ins_after = silence_after(vw[161]["s"], VO0)   # whisper glued "trillion dollars" and ended it at 59.74; the real end is about 60.28
GAP = 0.30; SB_LEN = SB_T1 - SB_T0; SHIFT = GAP + SB_LEN + GAP
SB_AT = snap(ins_after + GAP)                  # the soundbite starts on the grid
SHIFT = (SB_AT - ins_after) + SB_LEN + GAP
words = [dict(w) for w in vw]
for w in words[162:]: w["s"] += SHIFT; w["e"] += SHIFT
fw = json.load(open(f"{J}/research/wef_words.json"))["words"]
SBW = [{"w": w["w"], "s": SB_AT + w["s"] - SB_T0, "e": SB_AT + w["e"] - SB_T0, "sb": True} for w in fw if SB_T0 - 0.05 <= w["s"] < SB_T1]
os.makedirs(f"{J}/render/v8b", exist_ok=True)
VO = f"{J}/render/v8b/vo_v7.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", VO0, "-filter_complex",
                f"[0:a]atrim=0:{ins_after:.3f},asetpts=PTS-STARTPTS[a];[0:a]atrim={ins_after:.3f},asetpts=PTS-STARTPTS[b];"
                f"anullsrc=r=48000:cl=stereo,atrim=0:{SHIFT:.3f}[s];[a][s][b]concat=n=3:v=0:a=1[o]", "-map", "[o]", "-ar", "48000", VO], check=True)
SB_WAV = f"{J}/render/v8b/soundbite.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(SB_T0), "-i", SB_FILE, "-t", f"{SB_LEN:.3f}", "-vn", "-af",
                "highpass=f=90,afade=t=in:d=0.04,afade=t=out:st=%.3f:d=0.08" % (SB_LEN - 0.08),   # positioned in the mix (v7 bug: delay before -t gave silence)
                "-ar", "48000", "-ac", "2", SB_WAV], check=True)
VO_END = words[-1]["e"]; LAST = snap(VO_END + 0.45); END = VO_END + 2.0
def ws(i): return words[i]["s"]
def we(i): return words[i]["e"]

# ---------------- 1. music plan ----------------
SECTIONS = [(0, 3, "hook"), (24, 1, "context breakdown"), (38, 3, "story build"), (56, 4, "drop 1: the ruling"), (64, 2, "turn"),
            (85, 4, "drop 2: Texas"), (122, 1, "stops: locked out, reversed"), (133, 2, "tension"), (147, 3, "build"),
            (157, 4, "drop 3: one trillion"), ("sb", 1, "soundbite: music drops out"), (162, 2, "peg"), (173, 4, "final callback"), (183, 2, "outro")]
HITS = [(0, "open"), (6, "drop"), (9, "swell"), (24, "swell"), (38, "hit"), (47, "impact"), (56, "drop"), (63, "impact"), (64, "hit"),
        (85, "drop"), (93, "impact"), (118, "impact"), (127, "click"), (127, "impact"), (132, "impact"), (133, "hit"), (146, "impact"),
        (157, "drop"), (162, "hit"), (173, "drop"), (202, "end")]
def at(i): return SB_AT if i == "sb" else (0.0 if i == 0 else snap(ws(i)))
sec = [{"t0": at(i), "energy": e, "name": n} for i, e, n in SECTIONS]
for k in range(len(sec)): sec[k]["t1"] = sec[k + 1]["t0"] if k + 1 < len(sec) else END
hits = [{"t": 0.0 if i == 0 else snap(ws(i) + 0.02), "kind": k, "word": words[i]["w"]} for i, k in HITS]
plan = {"bpm": BPM, "s16": S16, "sections": sec, "hits": hits, "soundbite": [SB_AT, SB_AT + SB_LEN]}
json.dump(plan, open(f"{J}/music/music_plan_v8b.json", "w"), indent=1)

# ---------------- 2. edit plan ----------------
V = "video/"; P4 = "v4/"
WEF, VOA2, VOA1 = V + "v_wef_musk_2026.webm", V + "v_voa_2billionaires.webm", V + "v_voa_musk_shrink.webm"
COURT22, COURT17, LOCK, CRAMER = V + "v_court_shirehall_22.webm", V + "v_court_shirehall_17.webm", V + "v_padlock_open.webm", V + "v_cnbc_cramer_fedex.webm"
CYBER, FALCON, STARSHIP = V + "v_cybertruck_tokyo.webm", V + "v_falcon_heavy_test.webm", V + "v_starship_ift1_wb57.webm"
SPEECH = "s01_musk_inauguration_2025.webm"
def C(f, s, look="", fx=0.5, rate=1.0): return {"k": "clip", "f": f, "s": s, "look": look, "fx": fx, "rate": rate}
def P(f, look="", fx=0.5, fy=0.4, z=(1.0, 1.06)): return {"k": "photo", "f": f, "look": look, "fx": fx, "fy": fy, "z": z}
def G(typ, bg, **d): return {"k": "gfx", "type": typ, "d": d, "bg": bg}
def POL(f, box, side=False): return {"k": "pol", "f": f, "box": box, "side": side}
def BURST(*fs, look="warm"): return {"k": "burst", "fs": list(fs), "look": look}
BLK = {"k": "blk"}
COLO = "p_musk_colorado_2022_full.jpg"; COLO_S1 = (1553, 180, 2843, 2473); COLO_POL = (1240, 300, 3140, 2048)
SHOTS = [
 (0, {"k": "photo", "f": COLO, "box": COLO_S1, "look": "warm_bloom", "z": (1.0, 1.04)}, "blocks"),
 (2, POL(COLO, COLO_POL, side=True), "whip:SCARIEST"),
 (4, C(WEF, 610.0, "warm_green", 0.47), "pop"),
 (5, C(SPEECH, 217.0, "teal", 0.5), "pop"),
 (("end", 5), C(WEF, 905.0, "washed", 0.47), "cut"),
 (6, C(SPEECH, 226.0, "blue", 0.5), "flash"),
 (7, P(P4 + "gold_01.jpg", "warm"), "cut"),
 (9, {"k": "grid9"}, "cut"),
 (24, C(COURT22, 28.0, "warm", 0.5), "flash"),
 (27, C(COURT22, 30.5, "warm_green", 0.45), "cut"),
 (29, C(CRAMER, 20.0, "bw", 0.55), "cut"),
 (31, C(CRAMER, 40.0, "warm", 0.6), "cut"),
 (33, C(COURT17, 8.0, "teal", 0.5), "pop"),
 (35, C(COURT22, 30.5, "warm", 0.6), "cut"),
 (38, G("year", C(VOA2, 7.0), big="2018"), "flash"),
 (39, P("p_tesla_board_2016.jpg", "warm"), "cut"),
 (41, C(WEF, 1000.0, "warm_green", 0.47), "cut"),
 (44, BURST(P4 + "money_04.jpg", P4 + "gold_02.jpg", P4 + "gold_03.jpg", P4 + "vault_02.jpg", P4 + "money_02.jpg"), "cut"),
 (47, G("number", C(FALCON, 140.0), big="$56B", sub="Musk's 2018 Tesla pay package"), "flash"),
 (49, G("crowd", C(CRAMER, 50.0)), "cut"),
 (51, P(P4 + "gavel_03.jpg", "red"), "shake"),
 (52, P(P4 + "bust_02.jpg", "bw", 0.5, 0.3), "cut"),
 (54, G("shares", C(CRAMER, 33.0), lit=9, label="9 shares"), "pop"),
 (56, G("year", C(COURT22, 27.0), big="Jan 2024"), "flash"),
 (58, P(P4 + "judge_02.jpg", "bw", 0.5, 0.45), "cut"),
 (60, P(P4 + "gavel_03.jpg", "warm"), "shake"),
 (61, G("number", C(CYBER, 16.0), big="$56B", sub="the pay deal"), "cut"),
 (63, G("stamp", C(CYBER, 18.0), under="$56B", stamp="VOIDED"), "whip:VOIDED"),
 (64, BLK, "cut"),
 (65, C(WEF, 1170.0, "teal", 0.47), "pop"),
 (66, C(COURT17, 13.0, "warm", 0.5), "cut"),
 (69, C(VOA2, 58.0, "warm_green", 0.5), "cut"),
 (72, C(VOA2, 59.8, "warm", 0.62), "cut"),   # 61 s and later is a rally: avoid
 (74, G("quote", C(VOA1, 36.5), text="Never incorporate your company in the state of Delaware", by="Elon Musk on X, January 2024"), "flash"),
 (83, C(VOA2, 39.5, "red", 0.5), "cut"),
 (85, P(P4 + "hourglass_01.jpg", "warm"), "flash"),
 (87, G("map", C(VOA2, 59.5)), "cut"),
 (88, C(WEF, 629.5, "warm", 0.5), "cut"),
 (93, P(P4 + "txflag_02.jpg", "warm"), "whip:TEXAS"),
 (94, P("p_texas_capitol_night.jpg", "warm"), "cut"),
 (97, P(P4 + "lawbooks_01.jpg", "warm_green"), "cut"),
 (100, C(VOA2, 52.0, "teal", 0.5), "cut"),
 (102, P(P4 + "lawbooks_02.jpg", "red"), "pop"),
 (104, C(COURT22, 28.5, "warm", 0.4), "cut"),
 (107, P("p_tesla_board_2016.jpg", "bw"), "cut"),
 (111, G("grid", C(CRAMER, 25.0), lit=3, label="3% of Tesla needed to sue the board"), "pop"),
 (116, C(CRAMER, 30.0, "warm", 0.62), "cut"),
 (118, G("number", C(CRAMER, 47.0), big="$30B+", sub="of stock (2025 prices)"), "flash"),
 (122, P(P4 + "bust_02.jpg", "bw", 0.5, 0.3), "cut"),
 (125, G("shares", C(COURT17, 8.0), lit=9, label="9 shares"), "cut"),
 (127, C(LOCK, 24.0, "red", 0.5), "shake"),
 (129, P(P4 + "judge_02.jpg", "bw", 0.5, 0.45), "cut"),
 (132, G("stamp", C(COURT22, 32.0), under="Ruling", stamp="REVERSED"), "whip:REVERSED"),
 (133, G("year", C(COURT22, 29.0), big="Dec 2025"), "pop"),
 (135, C(COURT22, 30.0, "warm", 0.6), "cut"),
 (137, P(P4 + "jx_01.jpg", "bw", 0.35, 0.35), "cut"),
 (138, G("number", C(CYBER, 22.0), big="$56B", sub="given back"), "pop"),
 (143, P(P4 + "dollar_02.jpg", "warm"), "cut"),
 (146, G("number", C(LOCK, 12.0), big="$1", sub="awarded to the shareholder"), "shake"),
 (147, C(WEF, 290.0, "warm_green", 0.6), "cut"),
 (149, C(WEF, 1706.5, "warm", 0.5), "cut"),
 (152, C(CRAMER, 45.0, "teal", 0.4), "cut"),
 (155, P(P4 + "gold_02.jpg", "warm"), "cut"),
 (157, C(FALCON, 138.0, "warm", 0.5), "flash"),
 (160, G("counter", C(FALCON, 150.0), to=1_000_000_000_000, sub="approved by over 75% of votes cast"), "flash"),
 ("sb", {"k": "clip", "f": WEF, "s": SB_T0, "look": "warm_green", "fx": 0.62, "rate": 1.0, "hold": True}, "flash"),
 (162, G("year", C(VOA2, 7.5), big="Wed 21 Oct"), "pop"),
 (164, C(VOA2, 8.0, "teal", 0.5), "cut"),
 (167, P("p_tesla_board_2016.jpg", "bw"), "cut"),
 (169, C(COURT17, 4.0, "warm", 0.5), "cut"),
 (172, P(P4 + "gavel_03.jpg", "bw"), "shake"),
 (173, POL(COLO, COLO_POL), "flash"),
 (178, C(WEF, 1500.0, "warm_green", 0.47), "pop"),
 (180, P(P4 + "gold_01.jpg", "red"), "cut"),
 (183, C(WEF, 1706.0, "bw", 0.5), "cut"),
 (188, C(LOCK, 10.0, "red", 0.5), "cut"),
 (194, G("number", C(CRAMER, 52.0), big="$30B+", sub="just to sue the board"), "flash"),
 (197, P(P4 + "doors_02.jpg", "warm", z=(1.0, 1.12)), "cut"),
 (202, BLK, "shake"),
]
shots = []
for key, vis, fx in SHOTS:
    t0 = SB_AT if key == "sb" else snap(we(key[1])) if isinstance(key, tuple) else (0.0 if key == 0 else snap(ws(key) + 0.02))
    if shots and t0 < shots[-1]["t0"] + S16: t0 = shots[-1]["t0"] + S16
    shots.append({"t0": t0, "vis": vis, "fx": fx, "word": key})
for k in range(len(shots)): shots[k]["t1"] = shots[k + 1]["t0"] if k + 1 < len(shots) else LAST
# pace pass (split shots over 0.63 s into 0.31-0.47 s pieces at word starts on the grid; punch-ins alternate)
MAXP, MINP = 3 * S16, 2 * S16
paced = []
for s_ in shots:
    v = s_["vis"]; d = s_["t1"] - s_["t0"]
    hold = v["k"] in ("gfx", "grid9") or v.get("hold") or (v["k"] == "pol" and v.get("side")) or s_["fx"] == "blocks"
    if d <= 4 * S16 + 1e-6 or hold: paced.append(s_); continue
    pts = [s_["t0"]]
    for w in words:
        c = snap(w["s"] + 0.02)
        if c - pts[-1] >= MINP - 1e-6 and s_["t1"] - c >= MINP - 1e-6: pts.append(c)
    fill = [pts[0]]
    for c in pts[1:] + [s_["t1"]]:
        while c - fill[-1] > MAXP + 1e-6 and s_["t1"] - (fill[-1] + MAXP) >= MINP - 1e-6: fill.append(fill[-1] + MAXP)
        if c < s_["t1"] - 1e-6 and c - fill[-1] >= MINP - 1e-6: fill.append(c)
    for k, a0 in enumerate(fill):
        a1 = fill[k + 1] if k + 1 < len(fill) else s_["t1"]; vv = dict(v)
        if k % 2 == 1: vv["punch"] = 1 if (k // 2) % 2 == 0 else -1
        if v["k"] == "clip": vv["s"] = v["s"] + (a0 - s_["t0"])          # the clip keeps playing through the split
        paced.append({"t0": a0, "t1": a1, "vis": vv, "fx": s_["fx"] if k == 0 else "cut", "word": s_["word"] if k == 0 else "split"})
shots = paced
shots.append({"t0": LAST, "t1": END, "vis": {"k": "gfx", "type": "sting", "d": {}, "bg": None}, "fx": "cut", "word": "end"})
json.dump([{"t0": round(s["t0"], 4), "t1": round(s["t1"], 4), "fx": s["fx"], "vis": s["vis"], "word": str(s["word"])} for s in shots], open(f"{J}/edit/edit_v8b.json", "w"), indent=0)
cuts = [{"t": s["t0"], "fx": s["fx"].split(":")[0]} for s in shots if not (SB_AT < s["t0"] < SB_AT + SB_LEN)]
for s in shots:
    if s["vis"]["k"] == "burst":
        t = s["t0"] + 3 / FPS
        while t < s["t1"] - 1e-6: cuts.append({"t": t, "fx": "cut"}); t += 3 / FPS
G9 = next(s for s in shots if s["vis"]["k"] == "grid9")
for k, dt in enumerate((0.13, 0.2, 0.27, 0.33, 0.47, 0.6, 0.73, 0.87, 1.0)): cuts.append({"t": G9["t0"] + dt, "fx": "pop" if k in (4, 5) else "cut"})

if os.environ.get("PLAN_ONLY"): print(f"plan: soundbite {SB_AT:.3f}-{SB_AT + SB_LEN:.3f}, split after {ins_after:.3f}, shift {SHIFT:.3f}, end {END:.2f}"); sys.exit(0)
# ---------------- 3. score: music only (no per-cut hits); real SFX only at shifts, each sound different ----------------
music_plan = dict(plan, hits=[{"t": h["t"], "kind": "drop"} for h in hits if h["kind"] == "drop"])   # keeps risers and suck-outs before drops
mix = synth.render({**music_plan, "hits": []}, [], END)
a0, a1 = int(SB_AT * synth.SR), int((SB_AT + SB_LEN) * synth.SR); mix[a0:a1] *= 0.12   # music drops out under the soundbite
mix = mix / (np.max(np.abs(mix)) + 1e-9) * 0.7
wavfile.write(f"{J}/music/score_v8b.wav", synth.SR, np.stack([mix, mix], 1).astype(np.float32))
SFXD = f"{J}/sources/sfx"; SFXI = json.load(open(f"{SFXD}/sfx_info.json"))
def shot_at(word): return next(x["t0"] for x in shots if x["word"] == word)
G9T = next(x["t0"] for x in shots if x["vis"]["k"] == "grid9")
CALL = next(x["t0"] for x in shots if x["word"] == 173)
# (time, file, gain dB, align): align "onset" puts the sound's attack on the time, "peak" its loudest point, "end" its end
SFX = [
 (0.0, "sfx_vhs_glitch", -4, "onset"),                      # opener blocks
 (shot_at(2) - 0.06, "sfx_whoosh_swipe", -6, "peak"),       # whip into the polaroid
 (shot_at(2), "sfx_shutter", -2, "peak"),                   # the polaroid "taken"
 (shot_at(6), "sfx_boom_impact2", -4, "peak"),              # drop on "isn't"
 (G9T + 0.47, "sfx_whoosh_deep", -8, "peak"),               # figure enters the grid
 (G9T + 0.53, "sfx_glitch_short", -10, "onset"),            # the negative frame
 (shot_at(24), "sfx_metal_impact", -8, "peak"),             # shift into the courtroom section
 (shot_at(47), "sfx_cinema_boom", -9, "peak"),              # $56B
 (shot_at(60), "sfx_gavel_single", 0, "peak"),                     # "the judge agrees" on the gavel
 (shot_at(63) + 0.1, "sfx_stamp", -6, "onset"),             # VOIDED stamp lands
 (shot_at(85), "sfx_riser", -8, "peak"),                    # drop 2: Texas
 (shot_at(85), "sfx_trailer_boom", -10, "peak"),
 (shot_at(93) - 0.06, "sfx_whoosh_swipe", -8, "peak"),      # TEXAS whip
 (shot_at(127), "sfx_lock", 2, "peak"),                     # "Locked out"
 (shot_at(132) + 0.1, "sfx_gavel_single", -2, "peak"),             # REVERSED
 (shot_at(157), "sfx_riser", -6, "peak"),                   # drop 3: one trillion
 (shot_at(160), "sfx_trailer_boom", -6, "peak"),
 (CALL - 0.06, "sfx_whoosh_deep", -8, "peak"),              # callback: the polaroid returns
 (CALL, "sfx_shutter", -2, "peak"),
 (shot_at(202), "sfx_door_slam", 0, "peak"),                # "...get in the door."
]
sfx = np.zeros(int(END * 48000) + 48000 * 8)
for t, name, gdb, align in SFX:
    x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", f"{SFXD}/{name}.mp3", "-ac", "1", "-ar", "48000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
    inf = SFXI[name + ".mp3"]; off = inf["onset"] if align == "onset" else inf["peak"] if align == "peak" else inf["dur"]
    st = int((t - off) * 48000); x = x / (np.max(np.abs(x)) + 1e-9) * 10 ** (gdb / 20) * 0.7
    if st < 0: x = x[-st:]; st = 0
    sfx[st:st + len(x)] += x[:len(sfx) - st]
sfx = sfx[:int(END * 48000)]
wavfile.write(f"{J}/music/sfx_v8b.wav", 48000, np.stack([sfx, sfx], 1).astype(np.float32))
json.dump([{"t": round(t, 3), "sfx": n, "gain_db": g} for t, n, g, _ in SFX], open(f"{J}/music/sfx_cues_v8b.json", "w"), indent=0)

# ---------------- 4. picture ----------------
SERIF = ("/System/Library/Fonts/Supplemental/Didot.ttc", 1); SANS = ("/System/Library/Fonts/HelveticaNeue.ttc", 1)
FC = {}
def font(k, s):
    if (k, s) not in FC: FC[(k, s)] = ImageFont.truetype(SANS[0], s, index=SANS[1]) if k == "sans" else ImageFont.truetype(SERIF[0], s, index=SERIF[1])
    return FC[(k, s)]
WHITE, GOLD, RED, DIM = (245, 242, 235), (236, 196, 120), (225, 60, 50), (190, 186, 178)
rng = np.random.default_rng(5)
def to_np(im): return np.asarray(im.convert("RGB"), np.float32) / 255
def to_im(a): return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8))
def blur(a, r): return to_np(to_im(a).filter(ImageFilter.GaussianBlur(r)))
LOOKS = {
    "warm_bloom": dict(mul=(1.12, 0.96, 0.82), lift=(0.025, 0.008, 0.0), gamma=1.38, hal=(1.0, 0.45, 0.25), ha=0.6),
    "warm":       dict(mul=(1.08, 0.98, 0.86), lift=(0.02, 0.01, 0.0), gamma=1.3, hal=(1.0, 0.6, 0.35), ha=0.45),
    "warm_green": dict(mul=(1.02, 1.03, 0.86), lift=(0.03, 0.04, 0.02), gamma=1.2, hal=(1.0, 0.75, 0.4), ha=0.35),
    "teal":       dict(mul=(0.86, 1.00, 1.04), lift=(0.0, 0.015, 0.02), gamma=1.35, hal=(0.6, 0.9, 1.0), ha=0.3),
    "washed":     dict(mul=(1.08, 1.0, 0.96), lift=(0.05, 0.035, 0.035), gamma=1.05, hal=(1.0, 0.8, 0.85), ha=0.45),
    "blue":       dict(mul=(0.7, 0.85, 1.18), lift=(0.0, 0.01, 0.05), gamma=1.2, hal=(0.4, 0.6, 1.0), ha=0.4),
    "bw":         dict(mul=(1, 1, 1), lift=(0.01, 0.01, 0.01), gamma=1.35, hal=(1.0, 1.0, 1.0), ha=0.4),
    "red":        dict(mul=(1, 1, 1), lift=(0, 0, 0), gamma=1.0, hal=(1.0, 0.3, 0.3), ha=0.5),
    "purple":     dict(mul=(1, 1, 1), lift=(0, 0, 0), gamma=1.0, hal=(0.8, 0.4, 1.0), ha=0.3),
    "": dict(mul=(1.05, 1.0, 0.92), lift=(0.02, 0.01, 0.0), gamma=1.25, hal=(1.0, 0.7, 0.5), ha=0.35),
}
def grade(a, look):   # per-shot colour, highlights bloom; the frame-edge look is added once at the end (finish)
    L = LOOKS[look]
    if look == "bw": g = a.mean(2, keepdims=True); a = np.repeat(np.clip((g - 0.5) * 1.45 + 0.5, 0, 1), 3, 2)
    if look == "red": g = np.clip((a.mean(2, keepdims=True) - 0.5) * 1.3 + 0.5, 0, 1); a = np.concatenate([np.clip(g * 1.25, 0, 1), g ** 1.8 * 0.45, g ** 1.8 * 0.42], 2)
    if look == "purple": g = np.clip((a.mean(2, keepdims=True) - 0.5) * 1.2 + 0.45, 0, 1); a = np.concatenate([g * 0.62 + g ** 3 * 0.5, g * 0.22 + g ** 3 * 0.4, g * 0.78], 2)
    a = a * np.array(L["mul"]); a = np.clip(a + np.array(L["lift"]) * (1 - a), 0, 1) ** L["gamma"]
    hi = np.clip((a.mean(2, keepdims=True) - 0.62) / 0.38, 0, 1) * a
    return 1 - (1 - a) * (1 - blur(hi, 22) * np.array(L["hal"]) * L["ha"])
# frame-edge look, measured on the reference corners: edge blur rising to the corners, magenta/green fringe up to ~1.2% of
# width, a thin pink rim, vignette. Applied to the whole frame including captions, like the reference.
YY, XX = np.mgrid[0:H, 0:W]; RR = np.sqrt(((XX - W / 2) / (W / 2)) ** 2 + ((YY - H / 2) / (H / 2)) ** 2)
EDGE = (np.clip((RR - 0.62) / 0.75, 0, 1) ** 1.4)[..., None]
VIG = np.clip(1.1 - 0.5 * RR ** 2.0, 0.2, 1)[..., None]
dist = np.minimum.reduce([XX, W - 1 - XX, YY, H - 1 - YY]).astype(np.float32)
RIM = (np.exp(-dist / 10.0) * 0.55)[..., None] * np.array([1.0, 0.35, 0.8])
def ca(a, k=0.012):
    out = a.copy()
    for ch, s in ((0, 1 + k), (2, 1 - k * 0.6)):
        im = Image.fromarray((a[..., ch] * 255).astype(np.uint8)); w2, h2 = int(W * s), int(H * s); im = im.resize((w2, h2), Image.BILINEAR)
        if s > 1: im = im.crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
        else: c = Image.new("L", (W, H)); c.paste(im, ((W - w2) // 2, (H - h2) // 2)); im = c
        out[..., ch] = np.asarray(im, np.float32) / 255
    return out
GRAIN = [np.repeat(np.repeat(rng.normal(0, 0.03, (H // 2, W // 2, 1)).astype(np.float32), 2, 0), 2, 1) for _ in range(6)]
CA_MASK = (np.clip((RR - 0.55) / 0.55, 0, 1) ** 1.6)[..., None]   # 0 in the centre, full at the corners
def ca_out(a, k):   # radial channel split with no empty edges: red scaled most, green half, blue not at all
    out = a.copy()
    for ch, s_ in ((0, 1 + k), (1, 1 + k * 0.5)):
        im = Image.fromarray((a[..., ch] * 255).astype(np.uint8)); w2, h2 = int(W * s_), int(H * s_)
        im = im.resize((w2, h2), Image.BILINEAR).crop(((w2 - W) // 2, (h2 - H) // 2, (w2 - W) // 2 + W, (h2 - H) // 2 + H))
        out[..., ch] = np.asarray(im, np.float32) / 255
    return out
def finish(a, f):   # v8: chromatic aberration near the borders only (red out, blue in: magenta and green fringes); no rim, no edge blur
    a = a * (1 - CA_MASK) + ca_out(a, 0.022) * CA_MASK
    return np.clip(a * VIG + GRAIN[f % 6], 0, 1)

def cover(im, fx=0.5, fy=0.4, scale=1.1):
    bw, bh = int(W * scale), int(H * scale); r = max(bw / im.width, bh / im.height)
    im = im.resize((int(im.width * r) + 1, int(im.height * r) + 1), Image.LANCZOS)
    x = min(max(int(im.width * fx - bw / 2), 0), im.width - bw); y = min(max(int(im.height * fy - bh / 2), 0), im.height - bh)
    return im.crop((x, y, x + bw, y + bh))
SC = {}
def still(v):
    key = json.dumps({k: v[k] for k in v if k != "punch"}, sort_keys=True)
    if key not in SC:
        im = Image.open(f"{J}/sources/{v['f']}").convert("RGB")
        im = im.crop(v["box"]).resize((int(W * 1.1), int(H * 1.1)), Image.LANCZOS) if "box" in v else cover(im, v.get("fx", 0.5), v.get("fy", 0.4))
        SC[key] = to_im(grade(to_np(im.resize((W, H))), v.get("look", ""))).resize((int(W * 1.1), int(H * 1.1)), Image.BILINEAR)
    return SC[key]
def push(base, p, z0, z1, cx=0.5):
    z = z0 + (z1 - z0) * p; bw, bh = base.size; cw, ch = int(bw / 1.1 / z), int(bh / 1.1 / z); x, y = int((bw - cw) * cx), (bh - ch) // 2
    return to_np(base.crop((x, y, x + cw, y + ch)).resize((W, H), Image.BILINEAR))
CL = {}
def clip_frames(f, start, dur, fx):
    key = hashlib.md5(f"{f}{start:.3f}{dur:.3f}{fx}".encode()).hexdigest()[:12]
    d = f"{J}/render/v8b/cache/{key}"
    if not os.path.isdir(d):
        os.makedirs(d)
        subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{start:.3f}", "-i", f"{J}/sources/{f}", "-t", f"{dur + 0.1:.3f}", "-r", str(FPS), "-vf",
                        f"crop=w=ih*9/16:h=ih:x=(iw-ow)*{fx}:y=0,scale={W}:{H}:flags=bicubic", "-q:v", "3", f"{d}/%04d.jpg"], check=True)
    if d not in CL: CL[d] = sorted(os.listdir(d))
    return d, CL[d]
def clip_img(v, lt, dur, look=None):
    d, fs = clip_frames(v["f"], v["s"], dur, v.get("fx", 0.5))
    if not fs: return np.zeros((H, W, 3), np.float32)
    return grade(to_np(Image.open(f"{d}/{fs[min(int(lt * FPS), len(fs) - 1)]}")), v.get("look", "") if look is None else look)
def flicker(a, t):   # micro flicker on stills so the eye never rests (reference: stills breathe every 2-3 frames)
    k = int(t * FPS) // 2; r = np.random.default_rng(k); return np.clip(a * (1 + r.uniform(-0.06, 0.06)) + r.uniform(0, 0.025), 0, 1)
# graphics: drawn on a transparent layer over darkened, blurred moving footage
def centered(d, y, text, f, fill): d.text((W / 2, y), text, font=f, fill=fill, anchor="mm")
def wrap(text, f, maxw):
    out, line = [], ""
    for w in text.split():
        t = (line + " " + w).strip()
        if f.getbbox(t)[2] > maxw and line: out.append(line); line = w
        else: line = t
    return out + [line]
LC = {}
def gfx_layer(typ, D):
    key = json.dumps([typ, D], sort_keys=True)
    if key in LC: return LC[key]
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if typ == "sting": centered(d, 960, "[ PAGE LOGO ]", font("sans", 64), DIM + (255,)); centered(d, 1040, "end sting placeholder", font("i", 40), DIM + (255,))
    elif typ == "year": centered(d, 760, D["big"], font("i", 230 if len(D["big"]) < 9 else 170), (235, 225, 210, 255))
    elif typ == "number": centered(d, 690, D["big"], font("i", 300), GOLD + (255,)); centered(d, 860, D["sub"], font("i", 52), DIM + (255,))
    elif typ == "crowd":
        for r in range(26):
            for c in range(18): d.ellipse((90 + c * 52, 300 + r * 44, 110 + c * 52, 320 + r * 44), fill=(120, 116, 110, 210))
        d.ellipse((90 + 9 * 52 - 8, 300 + 13 * 44 - 8, 118 + 9 * 52, 328 + 13 * 44), fill=GOLD + (255,))
    elif typ in ("shares", "grid"):
        cols, sz, gap = 10, 58, 18; ox, oy = (W - (cols * sz + (cols - 1) * gap)) / 2, 330
        for k in range(100):
            r, c = divmod(k, cols); col = ((GOLD if not D.get("dim") else RED) + (255,)) if k < D["lit"] else (70, 66, 64, 200)
            d.rectangle((ox + c * (sz + gap), oy + r * (sz + gap), ox + c * (sz + gap) + sz, oy + r * (sz + gap) + sz), fill=col)
        centered(d, oy + 10 * (sz + gap) + 60, D["label"], font("sans" if D.get("dim") else "i", 52), (RED if D.get("dim") else DIM) + (255,))
    elif typ == "stamp":   # v8: the word or number alone on top; strike and stamp are animated in gfx()
        centered(d, 640, D["under"], font("i", 250), (232, 226, 214, 255))
    elif typ == "quote":
        y = 420; d.text((120, y - 40), "“", font=font("i", 220), fill=GOLD + (255,)); y += 140
        for line in wrap(D["text"], font("i", 92), 840): d.text((120, y), line, font=font("i", 92), fill=WHITE + (255,)); y += 108
        d.text((120, y + 40), "— " + D["by"], font=font("sans", 36), fill=DIM + (255,))
    elif typ == "map":
        centered(d, 520, "DELAWARE", font("sans", 90), DIM + (255,)); centered(d, 1000, "TEXAS", font("sans", 130), WHITE + (255,))
        d.line((W / 2, 600, W / 2, 890), fill=GOLD, width=8); d.polygon([(W / 2 - 34, 880), (W / 2 + 34, 880), (W / 2, 930)], fill=GOLD)
        centered(d, 1100, "Tesla reincorporated, June 2024", font("i", 52), DIM + (255,))
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(im.split()[3].filter(ImageFilter.GaussianBlur(14)).point(lambda x: int(x * 0.8)))
    LC[key] = Image.alpha_composite(sh, im); return LC[key]
def gfx(s, t):
    v = s["vis"]; lt = t - s["t0"]; p = min(lt / max(s["t1"] - s["t0"], 0.01), 1)
    if v.get("bg"):
        bg = clip_img(v["bg"], lt, s["t1"] - s["t0"] + 0.2, "bw" if v["type"] in ("stamp", "year") else "warm")
        bg = blur(bg, 9) * 0.38
    else: bg = np.zeros((H, W, 3), np.float32) + 0.02
    lay = gfx_layer(v["type"], v["d"]).copy()
    if v["type"] == "stamp":   # strike-through draws across in 4 frames, then the stamp punches in below (no overlap)
        d = ImageDraw.Draw(lay); bb = d.textbbox((W / 2, 640), v["d"]["under"], font=font("i", 250), anchor="mm")
        e = min(lt / (4 / FPS), 1); x0, x1 = bb[0] - 30, bb[2] + 30
        d.line((x0, 650, x0 + (x1 - x0) * e, 630), fill=RED + (255,), width=16)
        if lt >= 5 / FPS:
            k = min((lt - 5 / FPS) / (4 / FPS), 1); sc = 1.35 - 0.35 * (1 - (1 - k) ** 3)
            st = Image.new("RGBA", (760, 210), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)
            sd.rectangle((8, 8, 752, 202), outline=RED + (255,), width=12); sd.text((380, 108), v["d"]["stamp"], font=font("sans", 128), fill=RED + (255,), anchor="mm")
            st = st.resize((int(760 * sc), int(210 * sc)), Image.BILINEAR).rotate(-5, expand=True, resample=Image.BICUBIC)
            lay.alpha_composite(st, ((W - st.width) // 2, 960 - st.height // 2))
    if v["type"] == "counter":
        d = ImageDraw.Draw(lay); e = 1 - (1 - min(p * 2.2, 1)) ** 3
        centered(d, 690, f"${56e9 + (v['d']['to'] - 56e9) * e:,.0f}", font("i", 108), GOLD + (255,)); centered(d, 820, v["d"]["sub"], font("i", 52), DIM + (255,))
    z = 1.0 + 0.05 * p; bw, bh = int(W * z), int(H * z)
    lay = lay.resize((bw, bh), Image.BILINEAR).crop(((bw - W) // 2, (bh - H) // 2, (bw - W) // 2 + W, (bh - H) // 2 + H))
    im = to_im(bg).convert("RGBA"); im.alpha_composite(lay); return to_np(im)
# polaroid
CARD_W = 640; PH_W, PH_H = CARD_W - 52, int((CARD_W - 52) * 0.92); CARD_H = PH_H + 26 + 110
PC = {}
def polaroid(v, p, bgclip=None, lt=0.0):
    key = (v["f"], tuple(v["box"]))
    if key not in PC:
        ph = Image.open(f"{J}/sources/{v['f']}").convert("RGB").crop(v["box"]).resize((W, H), Image.LANCZOS)
        PC[key] = to_im(grade(to_np(ph), "warm_bloom")).resize((PH_W, PH_H), Image.LANCZOS)
    card = Image.new("RGBA", (CARD_W, CARD_H), (238, 236, 230, 255)); card.paste(PC[key], (26, 26))
    sc = 0.97 + 0.04 * p; card = card.resize((int(CARD_W * sc), int(CARD_H * sc)), Image.LANCZOS).rotate(-2.4 + 1.2 * p, expand=True, resample=Image.BICUBIC)
    bg = to_im(blur(clip_img(bgclip, lt, 2.0, "bw"), 10) * 0.25) if bgclip else Image.new("RGB", (W, H), (0, 0, 0))
    glow = Image.new("L", (W, H), 0); ox, oy = int(W / 2 - card.width / 2), int(H * 0.46 - card.height / 2 + 6 * np.sin(p * 3.1))
    glow.paste(card.split()[3], (ox, oy)); glow = glow.filter(ImageFilter.GaussianBlur(40))
    bg = Image.composite(Image.new("RGB", (W, H), (60, 52, 46)), bg, glow.point(lambda x: x // 3)); bg.paste(card, (ox, oy), card); return to_np(bg)
def giant(word, size=430, shift=0, alpha=1.0, hblur=24):
    lay = Image.new("L", (W * 2, H), 0); d = ImageDraw.Draw(lay); d.text((W + shift, H * 0.47), word, font=font("i", size), fill=int(255 * alpha), anchor="mm")
    lay = lay.resize((W * 2 // hblur, H), Image.BILINEAR).resize((W * 2, H), Image.BILINEAR).crop((W // 2, 0, W // 2 + W, H))
    g = np.asarray(lay, np.float32)[..., None] / 255; return np.clip(g * 1.3 + blur(np.repeat(g, 3, 2), 22) * 0.9, 0, 1)
# block reveal
CELL = 60; GCn, GRn = W // CELL, H // CELL + 1
REV = np.where(rng.random((GRn, GCn)) < 0.45, rng.uniform(0.03, 0.3, (GRn, GCn)), -1.0); REV[3:12, 5:13] = rng.uniform(0.22, 0.5, (9, 8))
FLASH_B = [(1 / 30, 5, 5, 4, 5), (2 / 30, 10, 7, 4, 4), (5 / 30, 11, 4, 4, 3), (6 / 30, 4, 9, 3, 4), (8 / 30, 1, 12, 3, 4), (12 / 30, 13, 16, 3, 3)]
def blocks(a, lt):
    if lt > 0.5: return a
    m = to_np(to_im(a).resize((GCn, GRn - 1), Image.BILINEAR).resize((GCn * CELL, (GRn - 1) * CELL), Image.NEAREST).resize((W, H), Image.NEAREST))
    mask = np.kron((REV > lt).astype(np.float32), np.ones((CELL, CELL)))[:H, :W, None]; a = a * (1 - mask) + m * mask
    for ft, cx, cy, cw, ch in FLASH_B:
        if ft <= lt < ft + 1 / 30 + 1e-6:
            r2 = np.random.default_rng(int(ft * 1000))
            for yy in range(cy, cy + ch):
                for xx in range(cx, cx + cw):
                    if r2.random() < 0.7: al = r2.uniform(0.8, 0.97); sl = a[yy * CELL:(yy + 1) * CELL, xx * CELL:(xx + 1) * CELL]; sl[:] = al + (1 - al) * sl
    return a
# 9-grid sequence (reference 4.6-6.4 s): collage behind a 3x3 grid, cells flash, figure enters from the right through a
# negative frame, black-and-white cut-out lands centre, cells flash white and fill with playing clips, slow push in.
CUT_DIR = f"{J}/sources/cutouts/wef600"
CUT_F = sorted(f for f in os.listdir(CUT_DIR) if f.startswith("f_")); CUT_M = sorted(f for f in os.listdir(CUT_DIR) if f.startswith("m_"))
CELLS = [C(WEF, 300.0), C(CRAMER, 22.0), C(VOA2, 40.5), C(CYBER, 10.0), C(WEF, 1706.0), C(VOA2, 59.0), C(CRAMER, 36.0), C(WEF, 1890.0), C(VOA2, 8.0)]
def cutout(lt):
    k = min(int(lt * FPS), len(CUT_F) - 1)
    fr = Image.open(f"{CUT_DIR}/{CUT_F[k]}").convert("RGB"); mk = Image.open(f"{CUT_DIR}/{CUT_M[k]}").convert("L").resize(fr.size)
    s = 2.6; fr = fr.resize((int(fr.width * s), int(fr.height * s)), Image.BICUBIC); mk = mk.resize(fr.size, Image.BILINEAR)
    g = ImageOps.autocontrast(ImageOps.grayscale(fr), cutoff=2); g = g.point(lambda x: int(255 * min(1, max(0, (x / 255 - 0.5) * 1.5 + 0.5))))
    return g.convert("RGB"), mk
def grid9(s, t):
    lt = t - s["t0"]; dur = s["t1"] - s["t0"]
    cw, ch = W // 3, H // 3
    base = Image.new("RGB", (W, H)); fill_at = [0.62 + 0.07 * k for k in (4, 1, 7, 3, 5, 0, 8, 2, 6)]
    for k, cv in enumerate(CELLS):
        if lt >= fill_at[k]:   # the cell plays its clip
            fr = to_im(clip_img(cv, lt - fill_at[k], dur, "warm")).resize((cw, int(cw * H / W))).crop((0, (int(cw * H / W) - ch) // 2, cw, (int(cw * H / W) - ch) // 2 + ch))
        else:                  # purple duotone collage behind the grid before the cells fill
            fr = to_im(clip_img(cv, 0.0, dur, "purple") * 0.75).resize((cw, int(cw * H / W))).crop((0, (int(cw * H / W) - ch) // 2, cw, (int(cw * H / W) - ch) // 2 + ch))
        base.paste(fr, ((k % 3) * cw, (k // 3) * ch))
    a = to_np(base); d = ImageDraw.Draw(base)
    for k in range(1, 3): d.line((k * cw, 0, k * cw, H), fill=(15, 10, 20), width=5); d.line((0, k * ch, W, k * ch), fill=(15, 10, 20), width=5)
    a = to_np(base)
    for k, ft in enumerate((0.13, 0.2, 0.27, 0.33)):          # cells flash white one by one, then the whole frame blows out
        if ft <= lt < ft + 2 / FPS: c = (4, 1, 5, 3)[k]; a[(c // 3) * ch:(c // 3 + 1) * ch, (c % 3) * cw:(c % 3 + 1) * cw] = 0.96
    for k in range(9):                                          # each cell flashes white as it fills
        if fill_at[k] - 2 / FPS <= lt < fill_at[k]: a[(k // 3) * ch:(k // 3 + 1) * ch, (k % 3) * cw:(k % 3 + 1) * cw] = 0.95
    if 0.4 <= lt < 0.47: a = a + (1 - a) * 0.92
    z = 1.0 + 0.08 * max(0, lt - 0.55) / max(dur - 0.55, 0.1)   # slow push in
    if lt >= 0.47:
        g, mk = cutout(lt - 0.47)
        if lt < 0.53:   # enters from the right, motion blurred
            off = int(W * 0.35 * (1 - (lt - 0.47) / 0.06)); g = g.filter(ImageFilter.BoxBlur(12))
        else: off = 0
        im = to_im(a); x = (W - g.width) // 2 + off; y = H - g.height + int(H * 0.06)
        im.paste(g, (x, y), mk); a = to_np(im)
        if 0.53 <= lt < 0.57: a = 1 - a; a = a * np.array([0.75, 1.0, 0.8])     # one negative frame, green tint
    if dur > 1.6 and 1.35 <= lt < 1.42: a = to_np(to_im(a).resize((W // 30, H // 30)).resize((W, H), Image.NEAREST)) * 0.6 + 0.35   # blocky smear
    zi = to_im(a); bw, bh = int(W * z), int(H * z)
    return to_np(zi.resize((bw, bh), Image.BILINEAR).crop(((bw - W) // 2, (bh - H) // 2, (bw - W) // 2 + W, (bh - H) // 2 + H)))
def shot_img(s, t):
    v = s["vis"]; lt = t - s["t0"]; p = min(lt / max(s["t1"] - s["t0"], 0.01), 1)
    if v["k"] == "grid9": return grid9(s, t)
    if v.get("punch"):
        if v["k"] == "clip": base = to_im(clip_img(v, lt, s["t1"] - s["t0"])).resize((int(W * 1.1), int(H * 1.1)))
        elif v["k"] == "photo": base = still(v)
        else: base = to_im(shot_img(dict(s, vis={k: x for k, x in v.items() if k != "punch"}), t)).resize((int(W * 1.1), int(H * 1.1)))
        a = push(base, p, 1.32, 1.38, 0.5 + 0.18 * v["punch"]); return flicker(a, t) if v["k"] == "photo" else a
    if v["k"] == "clip": return clip_img(v, lt, s["t1"] - s["t0"])
    if v["k"] == "photo": return flicker(push(still(v), p, *v.get("z", (1.0, 1.06))), t)
    if v["k"] == "pol": return polaroid(v, p, None if v.get("side") else C(WEF, 1706.0), lt)
    if v["k"] == "blk": return np.zeros((H, W, 3), np.float32) + 0.015
    if v["k"] == "burst":
        k = int(lt * FPS / 3); f = v["fs"][k % len(v["fs"])]; return flicker(push(still({"f": f, "look": v["look"], "fx": 0.5, "fy": 0.45}), 0.5, 1.0, 1.08), t)
    return gfx(s, t)
# captions: 1-3 word groups that build word by word; white on dark, black on bright; Fink's line captioned too
EMPH = set("scariest musk money delaware referee jury judge elon sues nine agrees voided appeal moves never texas law rules sue locked reversed court back trillion wednesday nobody door congratulations tesla".split())
def nrm(x): return re.sub(r"[^a-z0-9]", "", x.lower())
CAPW = sorted(words + SBW, key=lambda w: w["s"])
groups, cur = [], []
for w in CAPW:
    if cur and (cur[-1].get("sb") != w.get("sb")): groups.append(cur); cur = []
    cur.append(w)
    if len(cur) == 3 or re.search(r"[.,?!:]$", w["w"]): groups.append(cur); cur = []
if cur: groups.append(cur)
CAPS = []
for g, nx in zip(groups, groups[1:] + [None]):
    end = min((nx[0]["s"] - 0.02) if nx else LAST, g[-1]["e"] + 0.6)
    for k, w in enumerate(g): CAPS.append((w["s"] - 0.02, end if k == len(g) - 1 else g[k + 1]["s"] - 0.02, [x["w"] for x in g[:k + 1]]))
CC = {}
def cap_layer(ws_, y, dark_text):
    key = (tuple(ws_), y, dark_text)
    if key in CC: return CC[key]
    parts = []
    for w in ws_:
        c = w.strip(); n = nrm(c)
        if re.search(r"\d", c): parts.append((c, font("i", 124), (20, 18, 16) if dark_text else GOLD, 0))
        elif n in EMPH: parts.append((c, font("sans", 98), (12, 12, 12) if dark_text else WHITE, -5))
        else: parts.append((c, font("i", 116), (12, 12, 12) if dark_text else WHITE, 0))
    def width(c, f, tr): return sum(f.getbbox(ch)[2] + tr for ch in c) - tr if tr else f.getbbox(c)[2]
    sp = 20; widths = [width(c, f, tr) for c, f, _, tr in parts]; tot = sum(widths) + sp * (len(parts) - 1); sc = min(1.0, 980 / max(tot, 1))
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(lay); x = (W - tot * sc) / 2
    for (c, f, col, tr), wd in zip(parts, widths):
        f2 = f if sc == 1 else ImageFont.truetype(f.path, int(f.size * sc), index=getattr(f, "index", 0))
        if tr:   # tight tracking for the bold sans, like the reference
            xx = x
            for ch_ in c: d.text((xx, H * y), ch_, font=f2, fill=col + (255,), anchor="ls"); xx += (f2.getbbox(ch_)[2] + tr) * 1
        else: d.text((x, H * y), c, font=f2, fill=col + (255,), anchor="ls")
        x += (wd + sp) * sc
    halo = lay.filter(ImageFilter.GaussianBlur(14))
    if dark_text: halo = Image.merge("RGBA", (*[Image.new("L", (W, H), 255)] * 3, halo.split()[3].point(lambda v: int(v * 0.7))))
    out = Image.alpha_composite(Image.alpha_composite(Image.new("RGBA", (W, H)), halo), halo)
    CC[key] = Image.alpha_composite(out, lay); return CC[key]
SIDE = {"thing": (112, 0.44), "about": (W - 112, 0.49)}
def frame(t):
    i = next((k for k, s in enumerate(shots) if s["t0"] <= t < s["t1"]), len(shots) - 1); s = shots[i]; lt = t - s["t0"]
    fx = s["fx"]; nxt = shots[i + 1] if i + 1 < len(shots) else None
    if nxt and nxt["fx"].startswith("whip:") and nxt["t0"] - 2 / FPS <= t:
        word = nxt["fx"].split(":")[1]; ph = to_im(shot_img(s, t)).resize((W // 30, H)).resize((W, H), Image.BILINEAR)
        a = 1 - (1 - np.clip(to_np(ph) * 1.25, 0, 1)) * (1 - giant(word, 470 if len(word) < 9 else 360, -60))
    else:
        a = shot_img(s, t)
        if fx == "blocks": a = blocks(a, lt)
        if fx.startswith("whip:") and lt < 2 / FPS: a = 1 - (1 - a) * (1 - giant(fx.split(":")[1], 430 if len(fx) < 14 else 340, -420, 0.55 * (1 - lt * FPS / 2), 34))
        if fx == "flash" and lt < 2 / FPS: a = a + (1 - a) * (0.92 if lt < 1 / FPS else 0.45)
        if fx == "pop" and lt < 1 / FPS: a = a + (1 - a) * 0.35
        if fx == "shake" and lt < 5 / FPS:
            amp = int(36 * (1 - lt * FPS / 5)); dx, dy = (amp, -amp // 2) if int(lt * FPS) % 2 == 0 else (-amp, amp // 2)
            a = np.roll(np.roll(a, dx, 1), dy, 0); a = a + (1 - a) * 0.25 * (1 - lt * FPS / 5)
    im = to_im(a).convert("RGBA"); v = s["vis"]
    if v["k"] == "pol" and v.get("side"):
        for w in words[2:4]:
            if w["s"] - 0.02 <= t:
                x, y = SIDE[nrm(w["w"])]; lay = Image.new("RGBA", (W, H)); ImageDraw.Draw(lay).text((x, H * y), w["w"], font=font("i", 92), fill=(250, 248, 242, 255), anchor="mm")
                g = lay.filter(ImageFilter.GaussianBlur(12)); im = Image.alpha_composite(Image.alpha_composite(im, g), lay)
    elif not (v["k"] == "gfx" and v["type"] in ("quote", "sting", "stamp")):   # the stamp prints the word itself
        c = next((c for c in CAPS if c[0] <= t < c[1]), None)
        if c:
            y = 0.56 if v["k"] == "gfx" and v["type"] in ("number", "counter") else 0.80 if v["k"] == "gfx" and v["type"] in ("map", "grid", "shares", "crowd") else 0.70 if v["k"] == "gfx" and v["type"] == "stamp" else 0.5
            band = a[int(H * y) - 110:int(H * y) + 30, 140:W - 140]; dark_text = float((band.mean(2) > 0.7).mean()) > 0.45   # more than 45% of the band is bright   # bright behind the words: black text
            im = Image.alpha_composite(im, cap_layer(c[2], y, dark_text))
    return to_np(im)

if os.environ.get("SNAP"):   # SNAP=t writes one full-size finished frame
    t_ = float(os.environ["SNAP"]); to_im(finish(frame(t_), 0)).save(f"{J}/render/v8b/snap_{t_:.2f}.png"); print("snap"); sys.exit(0)
if os.environ.get("FRAMES"):   # FRAMES=t0,t1 renders every frame in that span to a sheet
    t0_, t1_ = map(float, os.environ["FRAMES"].split(",")); ts = np.arange(t0_, t1_, 1 / FPS); tw, th = 180, 320; cols = 12
    S = Image.new("RGB", (cols * tw, ((len(ts) + cols - 1) // cols) * th)); d = ImageDraw.Draw(S)
    for k, t in enumerate(ts):
        S.paste(to_im(finish(frame(t), k)).resize((tw, th)), ((k % cols) * tw, (k // cols) * th)); d.text(((k % cols) * tw + 3, (k // cols) * th + 3), f"{t:.2f}", fill=(255, 230, 0))
    S.save(f"{J}/render/v8b/frames_{t0_:.1f}-{t1_:.1f}.jpg", quality=85); print("frames sheet", len(ts)); sys.exit(0)
if os.environ.get("TEST"):
    mids = [(s["t0"] + s["t1"]) / 2 for s in shots]; tw, th = 135, 240; cols = 16
    S = Image.new("RGB", (cols * tw, ((len(mids) + cols - 1) // cols) * th)); d = ImageDraw.Draw(S)
    for k, t in enumerate(mids):
        S.paste(to_im(finish(frame(t), k)).resize((tw, th)), ((k % cols) * tw, (k // cols) * th)); d.text(((k % cols) * tw + 3, (k // cols) * th + 3), f"{t:.1f}", fill=(255, 230, 0))
    S.save(f"{J}/render/v8b/test_sheet_v8b.jpg", quality=85); print("test sheet:", len(shots), "shots"); sys.exit(0)
clean = f"{J}/render/v8b/clean_v8b.mp4"
n = int(END * FPS)
ff = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", clean], stdin=subprocess.PIPE)
for f in range(n):
    ff.stdin.write((finish(frame(f / FPS), f) * 255).astype(np.uint8).tobytes())
    if f % 300 == 0: print("frame", f, "of", n, flush=True)
ff.stdin.close(); ff.wait()
# ---------------- 5. mix: voice + soundbite (positioned) + music ducked under both + SFX ----------------
sbd = int(SB_AT * 1000)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", clean, "-i", VO, "-i", SB_WAV, "-i", f"{J}/music/score_v8b.wav", "-i", f"{J}/music/sfx_v8b.wav", "-filter_complex",
                "[1:a]aformat=sample_rates=48000:channel_layouts=stereo,highpass=f=80,acompressor=threshold=-20dB:ratio=3[vo];"
                f"[2:a]aformat=sample_rates=48000:channel_layouts=stereo,acompressor=threshold=-24dB:ratio=3,volume=2.2,adelay={sbd}|{sbd}[sb];"
                "[vo][sb]amix=inputs=2:normalize=0:duration=longest,asplit[v][sc];"
                "[3:a]volume=0.75[m];[m][sc]sidechaincompress=threshold=0.05:ratio=3:attack=15:release=200[md];"
                "[4:a]volume=0.9[fx];[v][md][fx]amix=inputs=3:normalize=0:duration=longest,loudnorm=I=-14:TP=-1.5,alimiter=limit=0.83:level=false,apad=pad_dur=3[a]", "-map", "0:v", "-map", "[a]",
                "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-maxrate", "25M", "-bufsize", "50M", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "256k", "-shortest", OUTF], check=True)
print(f"done: {len(shots)} shots, {len(SFX)} sound effects, {END:.2f} s -> {OUTF}")
