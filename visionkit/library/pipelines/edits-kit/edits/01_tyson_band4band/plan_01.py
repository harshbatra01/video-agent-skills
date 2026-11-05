"""Edit 01: Mike Tyson x Central Cee ft. Lil Baby "BAND4BAND" (song 44.42-66.0 s, 21.6 s).

Base: FIGHT COLD OPEN (research pass 2): a silent B&W stare, a hard cut into colour on the snare, opponents named on
"Which one? Who do you want, bro? Pick one", the knockout on "I'll HIT one", then "Matter of time till I get them all
ticked off": a HIT LIST of his real knockout victims (names from the footage's own captions), each name struck through
on its knockout, one per drum hit. The hook "We could go band for band" is the payoff montage (the song's most
replayed part, 53-61 s); it ends on his stare and "I'M REALLY A THREAT".
New on top of the base set: impact frames (threshold strobes on contact), stutter strike on the snare roll, pop-up
freeze before the hook, the hit list, the number device on a real record (youngest heavyweight champion, 20).
"""
import os, sys
KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the edits-kit folder
sys.path.insert(0, os.path.join(KIT, "tools"))
from plankit import Edit, RED, GARNET, GOLD, stutter_rk

e = Edit("01_tyson_band4band", song_in=44.42, dur=21.58, gallery="tyson")
C, F, S = e.C, e.F, e.S
LEAK = os.path.join(KIT, "assets", "overlays", "warm", "leak_a.mp4")   # make it with tools/overlays.py
F1 = 1 / 30

# 0.00-2.51 COLD OPEN: the stare, B&W, no flashes, a quiet name
k0 = e.add("0_003", 0.0, C(2.51), src=21.6, speed=0.8, zoom=[[0.0, 1.04], [C(2.51), 1.14]], still=True)
e.looks.append(dict(t0=0.0, t1=C(2.51), cc=dict(sat=0, con=35, exp=-0.2)))
e.caption("MIKE TYSON", 0.35, C(2.51) - 0.1, size=34, tracking=600)
# 2.51 the snare: hard cut into colour. "F's just saw him, I'll flick one"
k1 = e.add("0_006", C(2.51), C(3.13), src=31.6)
e.tr("blowout", C(2.51), leak=LEAK); e.hit(C(2.51), punch=[1.1, 0.3], shake=[20, 0.35])
k2 = e.add("0_001", C(3.13), C(3.96), src=9.2)
e.tr("zoomrush", C(3.13), amt=1.35)
# "Which one? Who do you want, bro? Pick one": the opponents, named
k3 = e.add("1_007", C(3.96), C(4.6), src=98.0, zoom=1.28)
e.strike_name("TUBBS", C(3.96), C(4.6))
k4 = e.add("1_009", C(4.6), C(5.08), src=133.9, zoom=1.28)
e.strike_name("BIGGS", C(4.6), C(5.08)); e.tr("recipe", C(4.6), pattern="I")
k5 = e.add("1_012", C(5.08), C(5.68), src=179.6, zoom=1.28)
e.strike_name("BERBICK", C(5.08), C(5.68)); e.tr("recipe", C(5.08), pattern="I")
k6 = e.add("0_010", C(5.68), F(6.98) - 0.53, src=40.3)                                # "Pick one": he looks up
e.tr("silstack", C(5.68), clipB=k6, pattern="PK")
# "If I shoot my shot, I'll HIT one": Berbick, the punches, then the canvas on "hit"
k7 = e.add("1_012", F(6.98) - 0.53, F(6.98), src=183.3, zoom=1.28)
k8 = e.add("1_012", F(6.98), C(7.38), src=184.05, zoom=1.28, name="Berbick down")
e.tr("recipe", F(6.98), pattern="VT"); e.hit(F(6.98), punch=[1.14, 0.35], shake=[30, 0.45, 16, 3])
e.strike_name("BERBICK", F(6.98), C(7.38), t_strike=F(6.98))
# "Matter of time till I get them all ticked off": one knockout per drum hit, each name struck
k9 = e.add("1_007", C(7.38), C(8.23), src=100.75, zoom=1.28)
e.strike_name("TUBBS", C(7.38), C(8.23), t_strike=C(7.38) + 0.4)
k10 = e.add("1_021", C(8.23), C(8.70), src=310.45, zoom=1.28)
e.strike_name("ETIENNE", C(8.23), C(8.70), t_strike=C(8.23) + 0.1); e.hit(C(8.23), shake=[18, 0.3])
k11 = e.add("1_046", C(8.70), C(9.18), src=612.0, zoom=1.28)
e.strike_name("SELDON", C(8.70), C(9.18), t_strike=C(8.70) + 0.15); e.tr("recipe", C(8.70), pattern="I")
k12 = e.add("1_009", C(9.18), C(9.58), src=139.4, zoom=1.28)
e.strike_name("BIGGS", C(9.18), C(9.58), t_strike=C(9.18) + 0.1); e.tr("recipe", C(9.18), pattern="I")
k13 = e.add("0_009", C(9.58), C(10.04), rk=stutter_rk(C(9.58), C(10.04), 37.45))     # the fall, stuttered on the roll
e.tr("recipe", C(9.58), pattern="VT"); e.hit(C(9.58), punch=[1.12, 0.3])
# "Alright": the breath before the hook: his stare freezes and pops
k14 = e.add("0_004", C(10.04), S(55.50), src=25.0)
sx, sy = e.subj_src(k14, C(10.04) + 0.05)
e.tr("popfreeze", C(10.04) + 0.05, clip=k14, frames=10, sx=sx, sy=sy)
# THE HOOK "We could go band for band": the title word per "band / for / band", the payoff montage
k15 = e.add("0_010", S(55.50), C(12.16), src=40.25, speed=0.85)
e.tr("grid", S(55.50), pattern="fill", n=7, vertical=True, color=[1, 1, 1])
e.title(["BAND", "4", "BAND"], [S(56.10), S(56.32), S(56.48)], C(12.16) + 0.6, pop=k15)
e.hit(F(S(56.48)), punch=[1.08, 0.3], sil=dict(clip=k15, frames=[0, 2], glow=45))
k16 = e.add("1_008", C(12.16), C(13.40), src=128.3, zoom=1.28)                        # Holmes
e.tr("zoomrush", C(12.16), amt=1.4); e.hit(C(12.16) + 1.0, shake=[26, 0.4, 16, 3])
k17 = e.add("2_003", C(13.40), C(14.08), src=53.3)
e.tr("recipe", C(13.40), pattern="EKEK", line=[1, 0.85, 0.3])
k18 = e.add("0_007", C(14.08), C(15.35), src=33.0)
e.tr("blowout", C(14.08), leak=LEAK)
k19 = e.add("0_013", C(15.35), C(16.18), src=58.0)
e.tr("grid", C(15.35), pattern="pass", n=2, vertical=False, color=[0.94, 0.94, 0.88])
k20 = e.add("0_001", C(16.18), S(62.12), src=10.0)                                    # the record
e.tr("zoomrush", C(16.18), amt=1.3)
e.number("20", C(16.18), S(62.12), k20, size=560, depth_color=RED, cap="YOUNGEST HEAVYWEIGHT CHAMPION EVER")
k21 = e.add("2_001", S(62.12), C(18.16), src=6.1)
e.tr("recipe", S(62.12), pattern="VT")
k22 = e.add("0_008", C(18.16), C(18.86), src=36.5)
e.tr("smear", C(18.16), vertical=True, tint=[1, 0.88, 0.3])
k23 = e.add("0_009", C(18.86), S(64.62), src=37.2, speed=0.85, smooth=True)
e.tr("grid", C(18.86), pattern="fill", n=5, vertical=False, color=[1, 1, 1])
# "I'M REALLY A THREAT": the stare, word by word, the last hit freezes him
k24 = e.add("0_012", S(64.62), e.dur, src=55.0, speed=0.7, zoom=[[S(64.62), 1.06], [e.dur, 1.16]], still=True)
e.tr("blowout", S(64.62), leak=LEAK)
e.lyric_line(["I'M", "REALLY", "A", "THREAT"], [S(64.62), S(64.76), S(64.96), S(65.16)], e.dur)
e.tr("silstack", F(S(65.16)), clipB=k24, pattern="PK"); e.hit(F(S(65.16)), punch=[1.1, 0.35], shake=[20, 0.4])
# the knockout compilation burns fighter names into the bottom-left of its 4:3 picture: crop above them
for k_ in (k3, k4, k5, k7, k8, k9, k10, k11, k12, k16): e.keep_above(k_, 572, zoom=1.35)
for k_ in (k3, k9): e.keep_above(k_, 482, zoom=1.6)                                  # the "Round 2" bug (y 490-530)
e.save(3, fade=0.5)
