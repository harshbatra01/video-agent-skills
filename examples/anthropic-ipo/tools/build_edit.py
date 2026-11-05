#!/usr/bin/env python3
"""Anthropic IPO edit v1. Edit SEQ and run. Phases: python3 build_edit.py picture | audio | all
Beat grid comes from the stand-in reel (87.75 bpm, music/user_ref_1/beat_map.json). Swap music: change GRID and audio()."""
import hashlib, json, os, pathlib, re, subprocess, sys
import numpy as np

H = pathlib.Path.home(); J = H / "VisionKit/mine/jobs/minidoc-02-anthropic-ipo"; E = J / "edit"; SEG = E / "seg"; SEG.mkdir(parents=True, exist_ok=True)
FO = J / "research/footage"; BL = H / "VisionKit/mine/library/blocks"; T = J / "tools"
FPS = 30; W, HH = 1440, 1080
WORDS = json.load(open(J / "vo/v2/words.json")); VO = J / "vo/v2/Anthropic_IPO_vo_v2_adam.mp3"; END = 113.0
SB = {b["n"]: b for b in json.load(open(J / "storyboard/storyboard_v1.json"))["beats"]}
BPM = 87.75; PER = 60 / BPM; G0 = 0.5 + 0.534; TURN = 98.4


def snap(t, div=4):
    base = TURN if t >= TURN - 0.05 else G0; step = PER / div; return base + round((t - base) / step) * step


def norm(s): return re.sub(r"[^a-z0-9]", "", s.lower())


def at(word, t0):
    k = norm(word)
    for w in WORDS:
        if w["t0"] >= t0 - .05 and norm(w["w"]).startswith(k): return w["t0"]
    raise SystemExit("word " + word)


D1, D2, D3, D4 = "x2VHFgyawPE", "hQR_VJF6ukk", "h0x7KpG4Lf0", "aAPpQC-3EyE"
NBC, ABC, BB, WSJ, FB, CBS, AL, HEAR = "IjCJKr_KzRw", "M8j_Py_TQ9k", "8welyuCkxnM", "q1tw29SieHo", "Agaioeefut0", "YL3FAM4rfy8", "WxCTRSCzCrk", "ZC58H12VOHk"
SV1, SV2, SV3, KEY, HAND, HACK, CAB, NAS, CN = "V35nBNzfS88", "jqm1i_FSr8Y", "hFbmoms5sD4", "nRGoSNtE80E", "OJA5tP7aniE", "B-QYMpjnsWo", "pwcJZeCgsH0", "Nmn-tdJlI7Q", "F7B4LpEQknA"
RED = "colorchannelmixer=rr=1.25:gg=.55:bb=.55"; TEAL = "colorchannelmixer=rr=.8:gg=1.02:bb=1.15"; WARM = "colorchannelmixer=rr=1.12:gg=1:bb=.82"; BLUE = "colorchannelmixer=rr=.75:gg=.95:bb=1.3"; WASH = "eq=saturation=.6:contrast=.9:brightness=.06"; BW = "hue=s=0"
V = lambda c, i, g=None: ("v", c, i, g)
G = lambda name, sec, arg=None: ("g", name, sec, arg)
# n: beat; seq: footage and graphics in order; hits: cuts forced onto a word.
SEQ = {
 1: [V(D1, 180, TEAL), V(D2, 24), V(D4, 62, BLUE), V(D3, 20), V(D1, 36, WASH), V(D4, 212), V(D2, 96, TEAL), V(D3, 60, WARM)],
 2: [V(D4, 72, BLUE), V(D2, 120), V(D1, 150, TEAL), V(D3, 110), V(D3, 84, WASH), V(SV3, 28.2, RED), V(ABC, 58), V(SV3, 30, RED), V(KEY, 3, RED), V(KEY, 10.5, RED), V(SV2, 3, RED)],
 3: [G("black", 1.2), G("black", 0)],
 4: [V(NBC, 24), V(BB, 57), V(NBC, 38), V(FB, 22), V(ABC, 20), V(NAS, 13), V(CN, 2), V(BB, 66), V(NBC, 72), V(FB, 110), G("videowall", 2.6)],
 5: [V(ABC, 58), V(FB, 22), V(ABC, 60), V(SV3, 46), G("doc_a", 3.0), V(SV3, 28), V(SV3, 32.4, BLUE), V(SV2, 5), V(SV3, 50), V(WSJ, 72), V(SV3, 38.7, TEAL)],
 6: [G("reticle", 1.5), V(KEY, 5), V(HAND, 3), V(ABC, 76)],
 7: [G("terminal", 2.0), V(KEY, 6.6), V(KEY, 6)],
 8: [V(CAB, 2), V(CAB, 12), V(SV2, 6, TEAL), V(CAB, 22), V(SV3, 30.3, BLUE), V(CAB, 28)],
 9: [G("particle", 1.5), V(KEY, 9, BLUE), V(KEY, 13.1), V(ABC, 76), V(HAND, 9), V(SV3, 34), V(KEY, 13, TEAL), V(KEY, 5.3), V(HAND, 12), V(ABC, 78)],
 10: [V(ABC, 85, WASH), V(KEY, 7.9), G("slider", 2.5), V(WSJ, 199), V(ABC, 88), V(HAND, 14), V(ABC, 77)],
 11: [V(ABC, 86), G("dots", 3.0), V(WSJ, 199), V(HAND, 4), V(ABC, 87), V(HAND, 8)],
 12: [V(KEY, 2, RED), V(KEY, 9.2, RED), G("freeze", 1.5, (ABC, 76)), V(HAND, 5, RED), V(KEY, 7), V(KEY, 16, RED), G("stamp", 1.0), V(KEY, 14.4), V(KEY, 11, RED), V(HAND, 10, RED), V(KEY, 11.8), V(HAND, 16)],
 13: [G("pullback", 2.2, (BB, 66))],
 14: [V(D4, 325), V(D3, 158), V(D1, 150), V(D2, 200)],
 15: [G("timeline", 1.03), V(CBS, 8), V(NBC, 176, WARM), V(CBS, 22), V(NBC, 181), V(AL, 15), V(CBS, 15, WARM), V(AL, 70), V(NBC, 170), V(CBS, 91)],
 16: [V(CBS, 8), V(CBS, 24), V(NBC, 178), V(AL, 30), V(CBS, 45), V(CBS, 170), V(AL, 40), V(CBS, 112), V(AL, 95), V(CBS, 26), V(NBC, 180), V(CBS, 60), V(CBS, 120), V(AL, 150), V(CBS, 100), V(CBS, 18)],
 17: [V(SV3, 36), V(KEY, 15, BLUE), V(SV3, 36.6), G("wall", 2.0), V(SV2, 8), V(SV3, 40), V(KEY, 15.7)],
 18: [G("brake", 2.0), V(SV2, 2), V(SV3, 32), V(SV3, 40.8)],
 19: [V(D4, 392), V(D4, 357), V(ABC, 85), V(D4, 359), G("typed", 2.5), V(D4, 392), V(HAND, 12), V(D4, 361)],
 20: [V(D4, 391), V(ABC, 86), V(D4, 393), V(D4, 360), V(D4, 363), V(D4, 395), G("underline", 1.5)],
 21: [V(SV3, 50), V(SV2, 1), V(SV3, 26.1), V(SV3, 42, "eq=brightness=-.25")],
 22: [G("black", 2.6)],
 23: [G("colorize", 3.02)],
 24: [V(NAS, 15), V(CN, 10), V(CN, 30), G("black_tag", 0), V(CN, 25), V(NBC, 24), V(NAS, 16), V(FB, 112), V(FB, 96)],
 25: [G("doc_c", 2.4), V(HEAR, 3), V(HEAR, 40), V(D4, 765), V(FB, 22), V(HEAR, 10), V(D4, 62), V(HEAR, 45), G("gavel", 1.03)],
 26: [V(D2, 290), V(D3, 240), V(D4, 240)],
}
CAP_LOW_G = {"dots", "timeline", "typed", "underline", "stamp", "terminal", "slider", "reticle", "brake", "wall"}
KEYWORDS = {"anthropic", "ai", "ipo", "shutdown", "hack", "internet", "real", "433", "1800", "141006", "openai", "hugging", "face", "three", "yes", "stopped", "careful", "november", "sued", "stop", "deleted"}


def run(*a, **k): return subprocess.run([str(x) for x in a], check=True, **k)


def key(*a): return hashlib.md5(json.dumps(a, default=str).encode()).hexdigest()[:12]


def fit(src, ss, frames, out, vf=None):
    fl = f"scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},fps={FPS},eq=saturation=1.18:contrast=1.08:gamma=.96"
    if vf: fl += "," + vf
    fl += f",tpad=stop_mode=clone:stop_duration=30,trim=end_frame={frames},setpts=PTS-STARTPTS,format=yuv420p"
    run("ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", ss, "-i", src, "-t", frames / FPS + 2, "-vf", fl, "-an", "-frames:v", frames, "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-g", "30", out)


def still(clip, t):
    p = E / f"still_{clip}_{t}.png"
    if not p.exists(): run("ffmpeg", "-nostdin", "-v", "error", "-y", "-ss", t, "-i", FO / f"{clip}.mp4", "-frames:v", "1", "-update", "1", "-vf", f"scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH}", p)
    return p


def gfx(name, sec, arg, frames, out):
    dur = frames / FPS; raw = E / f"raw_{name}{'_200b' if name == 'colorize' else ''}.mp4"
    if name == "black": return run("python3", T / "edit_gfx.py", "black", dur, out)
    if name in ("doc_a", "doc_c"):
        a, b = ("a.png", "a_m.png") if name == "doc_a" else ("c.png", "c_m.png")
        if not raw.exists(): run("python3", BL / "screen-photo-push/screen_push.py", E / "doc" / a, E / "doc" / b, raw, "--dur", max(dur, 2.4), "--moire", .07)
        return fit(raw, 0, frames, out)
    if name == "videowall":
        if not raw.exists(): run("python3", BL / "video-wall/video_wall.py", raw, *[FO / f"{c}.mp4" for c in (NBC, BB, NAS, ABC, CN, CBS, WSJ, FB, D3, AL, HEAR, D4, SV3, D2, D1)], "--start", 30, "--dur", max(dur, 2.6))
        return fit(raw, 0, frames, out)
    if name == "gavel":
        return run("ffmpeg", "-nostdin", "-v", "error", "-y", "-loop", 1, "-i", H / "VisionKit/mine/jobs/minidoc-01/sources/v4/gavel_03.jpg", "-vf", f"scale={W}:{HH}:force_original_aspect_ratio=increase,crop={W}:{HH},fps={FPS},format=yuv420p", "-frames:v", frames, "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", out)
    if name == "particle": return fit(BL / "particle-mind/test/particle_mind_test_v1.mp4", .5, frames, out)
    if name == "colorize":
        if not raw.exists(): run("python3", BL / "colorize-reveal/colorize_reveal.py", FO / f"{D2}.mp4", raw, "--ss", 200, "--dur", max(dur, 3), "--reveal", 2.0)
        return fit(raw, 0, frames, out)
    if name in ("freeze", "pullback"):
        return run("python3", T / "edit_gfx.py", name, dur, out, still(*arg))
    return run("python3", T / "edit_gfx.py", name, dur, out)


ANCHOR = {"stamp": ("deleted", 45, -.32), "underline": ("wasn't", 86, -.25), "gavel": ("sued", 102, 0), "typed": ("yes", 83, -1.7), "dots": ("433", 40, -2.1), "slider": ("real", 35, -.75),
          "reticle": ("fake", 22.5, -.55), "terminal": ("hack", 25, -.3), "doc_a": ("broke", 18, -1.25), "wall": ("141", 70.7, 0), "brake": ("this", 76, -1.3), "doc_c": ("slow", 102, -1.25)}


def fill(seq, a, b, n):
    "Lay footage and free graphics from a to b on half-beats."
    out = []
    if not seq or b - a < 1 / FPS: return out
    gs = sum(round(s[2] / (PER / 2)) * PER / 2 for s in seq if s[0] == "g"); seq = list(seq); nv = sum(s[0] == "v" for s in seq)
    foot = max(b - a - gs, 0); units = max(int(round(foot / (PER / 2))), 0)
    while nv > max(units, 1 if foot > .2 else 0):
        k = max(i for i, x in enumerate(seq) if x[0] == "v"); seq.pop(k); nv -= 1
    u = [units // nv + (1 if i < units % nv else 0) for i in range(nv)] if nv else []
    if nv > 1:
        r = np.random.default_rng(n); r.shuffle(u)
    cur = a; ui = 0
    for j, s in enumerate(seq):
        if s[0] == "v":
            d = max(u[ui], 1) * PER / 2; ui += 1
        else:
            d = round(s[2] / (PER / 2)) * PER / 2
        e = b if j == len(seq) - 1 else min(cur + d, b - 1 / FPS)
        out.append(dict(n=n, s=s, t0=cur, t1=e)); cur = e
    return out


def build_timeline():
    items, flashes, low = [], [], []
    ns = sorted(SB)
    starts = {n: (0.0 if n == 1 else snap(SB[n]["t0"])) for n in ns}; starts[len(ns) + 1] = END
    for n in ns:
        t0, t1 = starts[n], starts[n + 1]; seq = [s for s in SEQ[n] if not (s[0] == "g" and s[2] == 0)]; part = []; cur = t0; pend = []
        for s in seq:
            if s[0] == "g" and s[1] in ANCHOR:
                w, t_, off = ANCHOR[s[1]]; ta = max(cur, snap(at(w, t_) + off)); d = min(round(s[2] / (PER / 2)) * PER / 2, t1 - ta)
                part += fill(pend, cur, ta, n); pend = []
                part.append(dict(n=n, s=s, t0=ta, t1=ta + d)); cur = ta + d
            else:
                pend.append(s)
        part += fill(pend, cur, t1, n)
        if part: part[-1]["t1"] = t1
        for it in part:
            if it["s"][0] == "g" and it["s"][1] in CAP_LOW_G: low.append([it["t0"], it["t1"]])
        items += part; bcuts = [i["t0"] for i in part]
        want = SB[n]["flash_t"]
        if want and bcuts:
            pick = np.linspace(0, len(bcuts) - 1, len(want)).round().astype(int)
            flashes += [round(float(bcuts[i]), 3) for i in sorted(set(pick))]
    fr = [int(round(i["t0"] * FPS)) for i in items] + [int(END * FPS)]
    for i, it in enumerate(items): it["f0"], it["frames"] = fr[i], fr[i + 1] - fr[i]
    return items, sorted(set(flashes)), low


def captions():
    caps, cur = [], []
    def flush():
        if cur: caps.append(dict(t0=cur[0]["t0"], t1=cur[-1]["t1"], w=[[x["w"].strip(",.:?"), norm(x["w"]) in KEYWORDS] for x in cur])); cur.clear()
    for w in WORDS:
        cur.append(w)
        if len(cur) == 3 or w["w"][-1] in ",.?:" or cur[-1]["t1"] - cur[0]["t0"] > .8: flush()
    flush()
    for a, b in zip(caps, caps[1:]): a["t1"] = min(b["t0"], a["t1"] + .25)
    return caps


def picture():
    items, flashes, low = build_timeline(); parts = []
    for it in items:
        s = it["s"]; out = SEG / f"{key(s, it['frames'], 'g96')}.mp4"; parts.append(out)
        if out.exists(): continue
        if s[0] == "v": fit(FO / f"{s[1]}.mp4", s[2], it["frames"], out, s[3])
        else: gfx(s[1], s[2], s[3], it["frames"], out)
        print(it["n"], s[1], it["frames"], flush=True)
    lst = E / "parts.txt"; lst.write_text("".join(f"file '{p}'\n" for p in parts))
    run("ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c:v", "libx264", "-preset", "veryfast", "-crf", "15", "-r", FPS, E / "picture_v1.mp4")
    tl = dict(end=END, edge=.16, wash=.35, flash=flashes, captions=captions(), caption_low=low,
              whip=[[snap(at("shutdown", 5)), "SHUTDOWN"], [snap(at("infamous", 57)), "INFAMOUS"]],
              tags=[dict(t0=snap(at("Hugging", 62)), t1=snap(at("Hugging", 62)) + 2.2, s="Hugging Face", kind="chyron"), dict(t0=snap(at("141", 70)), t1=snap(at("141", 70)) + 2.8, s="141,006 test runs", kind="chyron"),
                    dict(t0=SB[14]["t0"] + .4, t1=SB[14]["t0"] + 2.8, s="Dario Amodei, CEO", kind="chyron"), dict(t0=snap(at("November", 98)), t1=snap(at("November", 98)) + 1.6, s="NOVEMBER", kind="date")])
    json.dump(tl, open(E / "timeline_v1.json", "w")); json.dump([{k: v for k, v in i.items()} for i in items], open(E / "items_v1.json", "w"), default=str)
    print("shots", len(items), "flashes", len(flashes), "video s", round(sum(i["t1"] - i["t0"] for i in items if i["s"][0] == "v"), 1))


SR = 44100


def load(p):
    return np.frombuffer(subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-i", str(p), "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).reshape(-1, 2).astype(np.float64)


def lufs(p):
    e = subprocess.run(["ffmpeg", "-nostdin", "-hide_banner", "-nostats", "-i", str(p), "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    t = e[e.rfind("Summary:"):]; return float(re.search(r"I:\s+(-?[\d.]+)", t).group(1)), float(re.search(r"Peak:\s+(-?[\d.]+)", t).group(1))


def write(a, p, br=False):
    subprocess.run(["ffmpeg", "-nostdin", "-v", "error", "-y", "-f", "f64le", "-ar", str(SR), "-ac", "2", "-i", "-", str(p)], input=a.astype(np.float64).tobytes(), check=True)


def audio():
    SX = H / "VisionKit/mine/jobs/minidoc-01/sources/sfx"; A = E / "audio/sfx"; items, *_ = build_timeline(); N = int(END * SR)
    cue = [("Anthropic", 0, SX / "sfx_boom_impact2.mp3", -8), ("shutdown", 3, A / "fs_348224_Switch-Light-06-wav.mp3", -3), ("broke", 18, A / "fs_211247_Scribble.mp3", -9),
           ("internet", 28.5, SX / "sfx_lock.mp3", -7), ("found", 35.3, SX / "sfx_cinema_boom.mp3", -8), ("deleted", 45, SX / "sfx_stamp.mp3", -5), ("infamous", 58, SX / "sfx_metal_impact.mp3", -8),
           ("broke", 63, SX / "sfx_glitch_short.mp3", -8), ("including", 77.5, SX / "sfx_lock.mp3", -7), ("stopped", 90.3, SX / "sfx_door_slam.mp3", -5), ("But", 98.3, SX / "sfx_trailer_boom.mp3", -5),
           ("sued", 102, SX / "sfx_gavel_single.mp3", -4), ("still", 110.8, SX / "sfx_cinema_boom.mp3", -7)]
    sfx = np.zeros((N, 2)); log = []
    for w, t0, f, g in cue:
        t = at(w, t0) if w != "Anthropic" else 0.0
        x = load(f)[: SR * 3]; pk = np.argmax(np.abs(x).sum(1)[: SR]); x = x / (np.abs(x).max() + 1e-9) * 10 ** (g / 20); x[-2000:] *= np.linspace(1, 0, 2000)[:, None]
        s = max(int(t * SR) - pk, 0); e = min(s + len(x), N); sfx[s:e] += x[: e - s]; log.append(dict(t=round(t, 2), s=f.name))
    json.dump(log, open(E / "sfx_cues_v4.json", "w"))
    vo = load(VO); voice = np.zeros((N, 2)); voice[: len(vo)] = vo[:N]
    m = load(J / "music/user_ref_1/sep/htdemucs/reel/no_vocals.wav"); mus = np.zeros((N, 2)); xf = int(.08 * SR)
    def place(start, ms, me, fade_out=True):
        s = int(start * SR); a = m[int(ms * SR): int(me * SR)]; e = min(s + len(a), N); a = a[: e - s].copy(); a[:xf] *= np.linspace(0, 1, xf)[:, None]
        if fade_out: a[-xf:] *= np.linspace(1, 0, xf)[:, None]
        mus[s:e] += a
    bp = .534; k1 = int((84.5 - bp) / PER); m_end = bp + k1 * PER; t_join = .5 + m_end
    place(.5, 0, m_end)  # first pass of the track
    k2 = int((40 - bp) / PER); m2 = bp + k2 * PER; place(t_join, m2, m2 + (92.86 + .6 - t_join))
    place(TURN, 57.98, 57.98 + (END - TURN))
    env = np.ones(N); tt = np.arange(N) / SR
    def ramp(a, b, v0, v1): i = (tt >= a) & (tt < b); env[i] = np.minimum(env[i], np.linspace(v0, v1, i.sum()))
    ramp(SB[13]["t0"], SB[13]["t0"] + .3, 1, .3); env[(tt >= SB[13]["t0"] + .3) & (tt < SB[14]["t0"])] = .3; ramp(SB[14]["t0"], SB[14]["t0"] + 3, .3, 1)
    stop = snap(at("stopped", 90.3)); ramp(stop, stop + .25, 1, 0); env[(tt >= stop + .25) & (tt < TURN)] = 0
    last = snap(at("stop", 108.5)); ramp(last + .2, last + 1.2, 1, 0); env[tt >= last + 1.2] = 0
    mus = mus * env[:, None] * 10 ** (-3.4 / 20)
    (E / "audio").mkdir(exist_ok=True)
    def master(mix, name):
        p = mix / max(np.abs(mix).max() / .89, 1); t = E / "audio" / f"tmp_{name}.wav"; write(p, t); I, _ = lufs(t); gain = 10 ** ((-14 - I) / 20); q = p * gain; q = np.tanh(q / .95) * .95 if np.abs(q).max() > .95 else q; write(q, E / "audio" / f"{name}.wav"); print(name, "lufs", lufs(E / "audio" / f"{name}.wav"))
    master(voice * 1.0 + sfx * .9 + mus, "mix_music_v4"); master(voice + sfx * .9, "mix_nomusic_v4")
    print("sfx cues", len(cue))


if __name__ == "__main__":
    ph = sys.argv[1] if len(sys.argv) > 1 else "all"
    if ph in ("picture", "all"): picture()
    if ph in ("audio", "all"): audio()
