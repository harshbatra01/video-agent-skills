"""Pilot v8 (= v7 + the user's v7 review): Lamine Yamal x Tkandz "Now or Never" (song 12.80-44.77 s, 31.97 s).
v8: the light crack (7.73, 18.63) and the silhouette burst (13.73) are out; in their place the geometry the user
described: flat flash panels lit frame by frame across the cut (fx_lib section 13): seven vertical white bars appearing
one by one then fading into the next clip, the cream halves of his own GASS x Mbappe edit (top, full, bottom), and the
horizontal version (five white bands filling top to bottom, then fading).
v7: the pop-out title no longer shows a mirrored head; the light painting (6.45), colour floods (7.74, 18.66), the long
sideways smear (13.74), the red streak on "hit my target" and the aura are gone; the replacements are the new
geometry + flash transitions built on our per-clip mattes (fx_lib section 12): a graphic silhouette strobe, the frame
cracking with light into flying strips (sideways and vertical), and the next shot bursting out of the player's own
silhouette with a white rim.
v6: the rejected geometric transitions (spin, glitch boxes, shutter blades) are gone; almost every cut now carries an
optical transition from tools/ae/fx_lib.jsx, each one tuned frame by frame against the reference edit it copies
(STUDY.md): light blow-out, zoom rush + chromatic tunnel, streak smear, light painting, line-art strobe recipes,
colour flood, defocus space, ray burst. Target from the study: 20-35% of frames in a transition / effect state.
v5: clip audio OFF (it was mixing into the song in v1-v4), the zoom cuts replaced by the transition library (shutter,
invert / negative flicker, warm gradient flash, true RGB split, glitch slices, rotational spin), a negative-strobe entry
into the B&W stretch and 12 fps posterized motion inside it, single-frame negatives on the snare roll.

Rebuilt after the user's v3 review (13 Oct):
- GASS x Mbappe framing: the picture in a 1080 x 800 band, black bars above and below (we see far more of every shot,
  the virtual camera moves less, and the type gets clean space). Framing still follows him (SAM 2 mattes), smoothed more.
- No charging battery, no swipes (whips), no black breath frame, no lock-on ring, no forced "GIFT" ball shot.
- Story device the user loved at 22 s ("16" behind his head + white silhouette strobe), now the motif of the edit:
  his story in four numbers behind him, each on a strong hit and a lyric that earns it:
  2007 ("gift since birth": born 13 July 2007) -> 304 ("I came from dirt": Rocafonda, Mataro, postcode 08304) ->
  16 ("not even yet in my prime": youngest scorer in Euros history, 16 years 362 days) -> 10 ("in the end": Barca's 10).
- Designed type: big textured numbers with a coloured depth copy behind the player, small wide-tracked captions in the
  bottom bar, the title in the top bar with his head breaking out of the picture over it.
- The goal: real angles and real time. Build-up (wide), the close reverse-angle replay of the strike with the contact on
  the kick (20.17) and the ball in the net on the biggest kick of the line (21.02, "hit"), then the celebration.
- Ends on the section's last downbeat with a held end card for one more bar (to 31.97), fading out.
Writes plan_v8.json for tools/build_edit.py.
"""
import sys, os, json, math
KIT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(KIT, "tools"))
from reframe import build_gallery
import automatte, cuts, typeset
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
cat = json.load(open(os.path.join(HERE, "catalog", "catalog.json"), encoding="utf-8"))
FILES = {f["id"]: f["path"] for f in cat["files"]}; SHOT = {s["id"]: s for s in cat["shots"]}
BEATS = os.path.join(HERE, "song", "nn_beats.json")
SONG_IN = 12.80; DUR = 31.97; FPS = 30
BAND = [560, 800]                                         # y0, height: the GASS x Mbappe picture band
H = cuts.hits(BEATS, SONG_IN, DUR)
C = lambda t, win=0.2: cuts.on(t, H, win, FPS)            # strongest hit near t, floored to a frame
F = lambda t: round(cuts.fr(t, FPS), 4)
MATTES = os.path.join(HERE, "mattes", "auto")
GOAL = os.path.join(HERE, "footage", "f4_euro_france_goal.mp4")
GAL = build_gallery(os.path.join(HERE, "catalog", "catalog.json"), "yamal")
SMOOTH = dict(win=0.6, cap=0.35)                          # calmer virtual camera than v3 (user: first frame janky)


def ramp_rk(t0, t1, s_anchor, t_anchor, v_far=1.3, v_near=0.35, width=0.14, step=1 / 15):
    v = lambda t: v_near + (v_far - v_near) * (1 - math.exp(-((t - t_anchor) / width) ** 2))
    ts = sorted(set([round(t0 + i * step, 4) for i in range(int((t1 - t0) / step) + 1)] + [round(t1, 4), round(t_anchor, 4)]))
    s_rel = [0.0]
    for x0, x1 in zip(ts, ts[1:]): s_rel.append(s_rel[-1] + (v(x0) + v(x1)) / 2 * (x1 - x0))
    off = s_anchor - s_rel[ts.index(round(t_anchor, 4))]
    return [[round(t, 4), round(sr + off, 4)] for t, sr in zip(ts, s_rel)]


clips, hits, words, looks, overlays, zooms, pops, warn = [], [], [], [], [], [], [], []
trans = []                                                # transition library entries (edits_lib + fx_lib)
LEAK = os.path.join(KIT, "assets", "overlays", "warm", "leak_a.mp4")
auras = []
WARM, BARCA = ([1, 0.55, 0.12], [1, 0.12, 0.45]), ([0.12, 0.3, 1], [0.85, 0.05, 0.3])
def tr(ty, t, **kw): trans.append(dict(type=ty, t=round(t, 4), **kw))
MAT = {}                                                  # clip index -> its matte (shape stats), for placing type


def add(shot, t0, t1, src=None, speed=1.0, zoom=None, rk=None, smooth=False, file=None, box=None, point=None, prompt_t=None,
        focus=None, matte=True, zmax=1.5, zmin=1.03, name=None, still=False):
    """still=True: one fixed framing from the matte's median point (no camera move at all)"""
    sh = SHOT.get(shot); f = file or FILES[sh["file"]]
    if rk is None:
        s0 = src if src is not None else sh["t0"] + 0.1
        rk = [[t0, round(s0, 4)], [t1, round(s0 + (t1 - t0) * speed, 4)]]
    a, b = min(r[1] for r in rk), max(r[1] for r in rk)
    if sh and (a < sh["t0"] - 0.02 or b > sh["t1"] + 0.02):
        warn.append(f"{shot}: source {a:.2f}-{b:.2f} leaves the shot {sh['t0']:.2f}-{sh['t1']:.2f}")
    c = dict(file=f, t0=round(t0, 4), t1=round(t1, 4), name=name or f"{shot or os.path.basename(f)[:10]} {t0:.2f}", smooth=smooth, rk=rk)
    if matte:
        m = automatte.ensure(f, a, b, MATTES, box=box, point=point, gallery=None if (box or point) else GAL, prompt_t=prompt_t,
                             lo=sh["t0"] if sh else None, hi=sh["t1"] if sh else None)
        c["matte"] = dict(file=m["file"], src0=m["src0"]); MAT[len(clips)] = m
        if focus is None:
            keys = automatte.matte_focus(m, t0, t1, rk, **SMOOTH)
            focus = [[t0, float(np.median([k[1] for k in keys])), float(np.median([k[2] for k in keys]))]] if still else keys
        if zoom is None: zoom = max(zmin, automatte.auto_zoom(m, zmax=zmax))
    c["focus"] = focus or [0.5, 0.5]; c["zoom"] = zoom if zoom is not None else zmin
    clips.append(c)
    return len(clips) - 1


def hit(t, **kw): hits.append(dict(t=round(t, 4), **kw))


def subj_src(k, t):
    """head + shoulders point of clip k's player in source px at edit time t (from its matte)"""
    rk = clips[k]["rk"]; s_ = rk[0][1]
    for (a, sa), (b, sb) in zip(rk, rk[1:]):
        if a <= t <= b: s_ = sa + (sb - sa) * (t - a) / (b - a) if b > a else sb
    rows = [r for r in MAT[k]["rows"] if r[1] > 0]
    r = min(rows, key=lambda r: abs(r[0] - s_))
    return round(r[8], 1), round(r[9] + 0.3 * (r[3] - r[9]), 1)


def f2_low(k):
    """the celebrations pack has a blurred watermark block in the top left (source rows 15-160): at zoom 1.2 keep the
    framing low enough that the band starts below row 165"""
    cl = clips[k]; f = cl["focus"]
    if isinstance(f[0], list): cl["focus"] = [[t, x, max(y, 620)] for t, x, y in f]
    else: cl["focus"] = [f[0], max(f[1], 620)]


RED, GARNET, GREY, GOLD = [0.78, 0.06, 0.12], [0.50, 0.04, 0.16], [0.38, 0.38, 0.40], [1.0, 0.78, 0.15]
CAP_Y = 1402                                               # captions: bottom bar, inside the 76% safe line


def number(text, t0, t1, k, size, depth_color, cap=None, cap2=None, lift=0.0):
    """the motif: a big number behind him + his white silhouette on the slam frame + a caption in the bottom bar.
    Placed from his matte: centred on him, the glyphs' centre at the top of his head (so the top of every digit reads and
    his head covers only the lower middle), kept inside the band and on screen."""
    w, gh = typeset.measure(text, "GalanoGrotesque-Black", size)
    cp = automatte.comp_point(MAT[k], clips[k], t0 + 0.15, band=BAND) if k in MAT else None
    x, top = (cp[0], cp[2]) if cp else (540.0, BAND[0] + 0.3 * BAND[1])
    cy = min(max(top + 0.05 * gh - lift * gh, BAND[0] + gh / 2 + 12), BAND[0] + BAND[1] - gh / 2 - 12)
    x = 540.0 if w > 1000 else min(max(x, w / 2 + 30), 1080 - w / 2 - 30)
    words.append(dict(text=text, t0=t0, t1=t1, style="hero", size=size, x=round(x), y=round(cy + gh / 2), behind=k,
                      depth_color=depth_color, **{"from": 128}))
    hit(t0, sil=dict(clip=k, frames=[0], glow=45), expo=[0.5, 0.18])
    if cap: words.append(dict(text=cap, t0=t0 + 0.1, t1=t1, style="cap", y=CAP_Y, size=34))
    if cap2: words.append(dict(text=cap2, t0=t0 + 0.16, t1=t1, style="cap", y=CAP_Y + 48, size=26, tracking=300))


# ---------------------------------------------------------------- timeline (edit seconds)
D = C(0.88)                                                                     # the drop
add("0_029", 0.0, D, src=84.35, speed=0.75, zoom=[[0.0, 1.03], [D, 1.09]], still=True)   # his face, slow push, no camera move
k_drop = add("1_036", D, C(1.71), src=141.0)                                    # "Get up": crouched, looking up
hit(D, sil=dict(clip=k_drop, frames=[0, 2], glow=50), punch=[1.12, 0.3], shake=[18, 0.35])      # a flash would hide the white silhouette
add("0_032", C(1.71), C(2.82), rk=ramp_rk(C(1.71), C(2.82), 89.95, C(1.96), v_far=1.2, v_near=0.4, width=0.12), smooth=True)   # beats his man: slow on the cut inside
hit(C(1.71), punch=[1.06, 0.25]); tr("smear", C(1.71), vertical=True, tint=[1, 0.88, 0.3])              # "and make it work"
add("1_040", C(2.82), C(3.45), src=153.6)                                       # "Ain't no way that I'm sitting..."
hit(C(2.82), expo=[0.4, 0.2]); tr("invert", C(2.82), pattern="I.I")
add("0_060", C(3.45), C(4.31), src=184.30, speed=1.1)                           # "...around": bursts out
tr("blowout", C(3.45), leak=LEAK)                                               # "bursts out": light explodes
# "It's now or never": the title in the top bar, word per beat; his head breaks out of the picture over it
k_now = add("0_064", C(4.31), C(5.59), src=195.45, speed=0.88, zoom=1.3, still=True)
hit(C(4.31), punch=[1.04, 0.2])
TITLE = dict(style="hero", layer="bar", font="Coolvetica-HeavyComp", depth_color=RED, **{"from": 135})
TS = typeset.fit("NOW OR NEVER", "Coolvetica-HeavyComp", 990)                   # one line across the top bar
TX, _ = typeset.line(["NOW", "OR", "NEVER"], "Coolvetica-HeavyComp", TS, gap=0.22)
words += [dict(text=t_, t0=F(lt), t1=C(5.59), size=TS, y=540, x=x_, **TITLE)            # baseline on the band's top edge
          for t_, lt, x_ in zip(["NOW", "OR", "NEVER"], [4.78, 4.94, 5.16], TX)]
pops.append(dict(clip=k_now, t0=C(4.31), t1=C(5.59)))
k_first = add("0_011", C(5.59), C(6.45), src=37.85)                             # loudest snare of the song: the skill
hit(C(5.59), sil=dict(clip=k_first, frames=[0, 2], glow=50), punch=[1.1, 0.3], shake=[20, 0.35])
tr("zoomrush", C(5.59), amt=1.5, chroma=k_first)                                 # loudest snare: chromatic tunnel
k_134 = add("1_034", C(6.45), C(7.31), rk=ramp_rk(C(6.45), C(7.31), 135.5, C(7.10), v_far=1.15, v_near=0.4, width=0.1), smooth=True)   # "You can't tell me..."
hit(C(6.45), shake=[14, 0.3]); tr("silstack", C(6.45), clipB=k_134, pattern="WFIK", field=[0.62, 0.05, 0.18])   # graphic silhouette strobe
k_042 = add("0_042", C(7.31), C(7.74), src=122.9)                                       # "...that I won't"
hit(C(7.31), punch=[1.07, 0.22]); tr("recipe", C(7.31), pattern="EKEK", line=[1, 0.85, 0.3])   # line-art strobe
k_314 = add("3_014", C(7.74), C(8.81), rk=ramp_rk(C(7.74), C(8.81), 31.3, C(8.39), v_far=1.1, v_near=0.4, width=0.12), smooth=True)   # beats a man (stay before 32.03)                                        # "make it": beats a man, he falls
hit(C(7.74), punch=[1.08, 0.25]); tr("grid", C(7.74), pattern="fill", n=7, vertical=True, color=[1, 1, 1])   # seven white bars, one per frame, fade in
# 2007: "Knew that I had this gift since birth"
k_2007 = add("3_020", C(8.81), C(9.68), src=42.3, zoom=1.08)
number("2007", C(8.81), C(9.68), k_2007, size=400, depth_color=GARNET, cap="BORN 13 JULY 2007")
# hood walk into the B&W stretch: "came out the mud ... I had no body, I came from dirt"
add("0_028", C(9.68), C(11.17), src=80.75 - (C(10.52) - C(9.68)))
hit(C(9.68), expo=[0.3, 0.2]); tr("defocus", C(9.68), cast=[0.95, 0.3, 0.18])   # chapter: where he comes from (night, bokeh)
add("0_027", C(11.17), C(12.02), src=77.3)
k_304 = add("3_025", C(12.02), C(13.10), src=51.45)
looks.append(dict(t0=C(10.52), t1=C(13.10), cc=dict(sat=0, con=40, exp=-0.4)))
hit(C(10.52), shake=[16, 0.35]); hit(C(11.17), punch=[1.05, 0.25]); hit(C(12.02), punch=[1.05, 0.25])
tr("recipe", C(10.52), pattern="EKEKSD")                                         # into B&W through a line-art strobe
tr("posterize", C(10.52), t0=C(10.52), t1=C(13.10), fps=12)                       # gritty, laggy motion in the dirt section
tr("invert", C(11.17), pattern="N"); tr("invert", C(12.02), pattern="N")
number("304", C(12.44), C(13.10), k_304, size=470, depth_color=GREY, cap="ROCAFONDA  ·  MATARÓ")
# colour comes back: "Still can't f..., I put it in the work ... I'm really an artist"
k_106 = add("1_006", C(13.10), C(13.74), src=22.35, point=[980, 420], prompt_t=22.75)
hit(C(13.10), punch=[1.1, 0.3])                                                 # colour comes back hard
tr("blowout", C(13.10), leak=LEAK)                                             # colour comes back as light
k_317 = add("3_017", C(13.74), C(14.59), rk=ramp_rk(C(13.74), C(14.59), 37.2, C(14.15), v_far=1.4, v_near=0.4, width=0.12), smooth=True)
tr("grid", C(13.74), pattern="pass", n=2, vertical=False, color=[0.94, 0.94, 0.88])   # GASS x Mbappe cream halves
add("0_078", C(14.59), C(15.89), rk=ramp_rk(C(14.59), C(15.89), 247.25, C(15.45), v_far=0.95, v_near=0.4, width=0.14), smooth=True)
hit(C(14.59), punch=[1.07, 0.25]); hit(C(15.45), expo=[0.5, 0.2]); tr("zoomrush", C(14.59), amt=1.45)
k_keeper = add("0_080", C(15.89), C(17.17), src=250.95)                          # round the keeper and in
hit(C(15.89), shake=[16, 0.3]); hit(C(16.74), punch=[1.08, 0.25]); tr("recipe", C(15.89), pattern="SDSDCC")
k_fin = add("0_050", C(17.17), C(18.02), src=147.7, box=[620, 180, 990, 980], prompt_t=148.13)
hit(C(17.17), sil=dict(clip=k_fin, frames=[0, 2], glow=45), shake=[18, 0.3]); tr("rgb", C(17.17), clipB=k_fin, frames=5, px=30)
k_061 = add("0_061", C(18.02), C(18.66), src=186.13)                                    # "artist": his name on his back
hit(C(18.02), punch=[1.07, 0.25]); tr("zoomrush", C(18.02), amt=1.35)                # (keep his name readable)
# THE GOAL, Euro 2024 semi-final vs France. "This weren't by chance": the build-up, wide
k_bu = add(None, C(18.66), C(19.96), file=GOAL, src=1.85, box=[410, 350, 485, 480], prompt_t=3.20, zmin=1.55, zmax=1.6, name="goal build-up")
tr("grid", C(18.66), pattern="fill", n=5, vertical=False, color=[1, 1, 1]); hit(C(19.30), expo=[0.4, 0.2])   # chapter: the goal, bands top to bottom
# "I took one shot and I hit my target": close reverse angle, contact (source 18.71) on the kick 20.17, ball in the net
# (source 20.25) on the biggest kick of the line 21.02 ("hit"), then slow motion on the net
t_contact, t_net, t_end = C(20.17), C(21.02), C(21.78)
k_strike = add(None, C(19.96), t_end, file=GOAL, rk=[[C(19.96), 18.48], [t_contact, 18.71], [t_net, 20.25], [t_end, 20.45]],
               smooth=True, box=[780, 0, 1250, 1060], prompt_t=18.60, zoom=1.03, name="goal strike (replay)")
cs = clips[k_strike]; cs["focus"] = [r for r in cs["focus"] if r[0] <= t_contact + 0.1] + [[t_net, 960, 540], [t_end, 960, 540]]
hit(C(19.96), punch=[1.06, 0.22]); hit(t_contact, sil=dict(clip=k_strike, frames=[0, 2], glow=50), expo=[0.6, 0.2])
tr("recipe", C(19.96), pattern="EKE", line=[1, 0.85, 0.3])                     # the strike, drawn
hit(t_net, expo=[0.5, 0.15], punch=[1.14, 0.4], shake=[30, 0.5, 16, 3])     # the ball in the net stays visible
tr("rgb", t_net, clipB=k_strike, frames=8, px=40)    # the net: colour split, no white (it hid the goal)
# the payoff line, word by word on the sung words, in the bottom bar (the one lyric that matches the picture exactly)
LY = dict(style="slam", font="Coolvetica-HeavyComp", size=96, shade=0.6, **{"from": 140})
for line, ends in ((["I", "TOOK", "ONE", "SHOT"], F(20.76)), (["AND", "I", "HIT", "MY", "TARGET"], t_end)):
    xs, _ = typeset.line(line, "Coolvetica-HeavyComp", 96, gap=0.28)
    times = [19.96, 20.18, 20.36, 20.54] if line[0] == "I" else [20.76, 20.92, 21.02, 21.22, 21.40]
    for wd, x_, lt in zip(line, xs, times): words.append(dict(text=wd, t0=F(lt), t1=ends, x=x_, y=1446, **LY))
# "I'm not even yet in my prime": the bench celebration + 16 (the effect the user loved, now the motif)
k_cel = add(None, t_end, C(23.39), file=GOAL, src=6.80, box=[110, 330, 660, 1080], prompt_t=7.2, zoom=1.35, name="goal celebration")
hit(t_end, punch=[1.05, 0.22]); tr("blowout", t_end, leak=LEAK)                  # into the celebration
number("16", C(22.53), C(23.39), k_cel, size=470, depth_color=RED, cap="16 YEARS 362 DAYS", cap2="YOUNGEST SCORER IN EUROS HISTORY", lift=0.3)
hit(C(22.53), punch=[1.06, 0.25])
# "I'm not a hundred, yeah, I'm still charging": smiles, then quick cuts on the snare roll
add("0_073", C(23.39), C(24.03, 0.06), src=230.65)
tr("smear", C(23.39), vertical=True, tint=[1, 0.55, 0.7])                        # the smile
overlays.append(dict(file=os.path.join(KIT, "assets", "overlays", "spain", "leak_b.mp4"), t0=C(23.39), opacity=45))
k = add("2_002", C(24.03, 0.06), C(24.24, 0.06), src=7.3, zoom=1.2); f2_low(k)          # f2 pack: blurred watermark top left
add("0_039", C(24.24, 0.06), C(24.42, 0.06), src=111.7)
k = add("2_004", C(24.42, 0.06), C(24.89), src=16.05, zoom=1.2); f2_low(k)
for tt in (24.03, 24.24, 24.42): tr("invert", C(tt, 0.06), pattern="I")       # the snare roll: one negative per hit
# "They don't wanna see me win, but I know in the end I'm winning regardless"
k_pop = add("1_021", C(24.89), C(25.75), src=86.0)                              # hands on head, crowd: colour pop
tr("zoomrush", C(24.89), amt=1.4)
hit(C(24.89), punch=[1.07, 0.25])
add("1_009", C(25.75), C(26.81), src=30.65)                                     # finger in the ear: can't hear them
hit(C(25.75), shake=[16, 0.3]); tr("paint", C(25.75), color=[0.62, 0.93, 1], hold=5)     # cannot hear them
k_10 = add("2_006", C(26.81), C(27.66), src=24.0, speed=0.9, zoom=1.2); f2_low(k_10)  # "in the end": points to the sky, his 10
hit(C(26.81), sil=dict(clip=k_10, frames=[0, 2], glow=45), punch=[1.08, 0.3]); tr("rgb", C(26.81), clipB=k_10, frames=6, px=30)
k_end = add("1_009", C(27.66), DUR, src=33.9, speed=(36.8 - 33.9) / (DUR - C(27.66)), name="1_009 arms wide (end card)")
hit(C(27.66), punch=[1.05, 0.3]); hit(C(28.29), expo=[0.4, 0.2]); tr("blowout", C(27.66), leak=LEAK)

END = C(28.51)                                                                  # the section's last downbeat
words += [dict(text="NOW OR NEVER", t0=END, t1=DUR, size=TS, y=540, **dict(TITLE, **{"from": 112})),
          dict(text="TKANDZ", t0=END + 0.12, t1=DUR, style="cap", y=CAP_Y, size=40, tracking=600)]

SFX = os.path.join(KIT, "assets", "sfx")
sfx = [dict(file=os.path.join(SFX, "whoosh_up.wav"), t=round(D - 0.36, 3), db=-15),
       dict(file=os.path.join(SFX, "impact.wav"), t=round(D - 0.005, 3), db=-13)]
for z in trans:
    if z["type"] in ("blowout", "zoomrush", "smear", "defocus", "flood"): sfx.append(dict(file=os.path.join(SFX, "whoosh_short.wav"), t=round(z["t"] - 0.15, 3), db=-20))
    if z["type"] in ("recipe", "paint", "silstack"): sfx.append(dict(file=os.path.join(SFX, "glitch.wav"), t=round(z["t"] - 0.03, 3), db=-25))
    if z["type"] == "grid": sfx.append(dict(file=os.path.join(SFX, "whoosh_short.wav"), t=round(z["t"] - 0.2, 3), db=-20))
for w in words:
    if w.get("behind") is not None: sfx.append(dict(file=os.path.join(SFX, "impact.wav"), t=round(w["t0"] - 0.005, 3), db=-21))
sfx += [dict(file=os.path.join(SFX, "glitch.wav"), t=round(C(10.52) - 0.02, 3), db=-22),
        dict(file=os.path.join(SFX, "riser.wav"), t=round(C(19.96) - 1.2, 3), db=-21),
        dict(file=os.path.join(SFX, "whoosh_up.wav"), t=round(t_contact - 0.36, 3), db=-17),
        dict(file=os.path.join(SFX, "impact.wav"), t=round(t_net - 0.005, 3), db=-11)]

plan = dict(name="yamal_now_or_never_v8", w=1080, h=1920, fps=FPS, dur=DUR, band=BAND,
            audio=dict(file=os.path.join(HERE, "song", "now_or_never.wav"), **{"in": SONG_IN}),
            clips=clips, hits=hits, words=words, overlays=overlays, transitions=trans, popouts=pops, sfx=sfx, auras=auras,
            outlines=[dict(clip=k_cel, color=GOLD, grow=7, glow=45)], colorpops=[dict(clip=k_pop)],
            look=dict(cc=dict(con=18, sat=92, temp=-4, hi=-12, sh=-6, blacks=-8), vig=28, grain=3), looks=looks, bloom=[86, 60, 0.16],
            fade=[round(DUR - 0.6, 3), DUR])
json.dump(plan, open(os.path.join(HERE, "plan_v8.json"), "w"), indent=1)
print(f"plan v8: {len(clips)} clips, {len(hits)} hits, {len(words)} words, {len(zooms)} zoom cuts, end {DUR}")
for w_ in warn: print("WARN", w_)
cuts.report(plan, H, FPS)
