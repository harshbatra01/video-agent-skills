"""Edit 02: Anthony Edwards x Travis Scott "SICKO MODE" (song 50.25-73.86 s, 23.6 s).

Base: BAR BUILD + BEAT-SWITCH RESET (research pass 2, Itai Rosen's Ja Morant edit): a glare to open, one play per
beat-pair escalating (arrival, handle, finish, absurd), "Gone on you with the pick and roll" on his drive and poster
dunk, "he in SICKO MODE" as the title builds in the top bar, then the song's famous beat switch is the RESET: the
beat drops out, the picture goes B&W in a lit tunnel doorway after a poster-silhouette strobe; the new beat DROPS on
the strongest hit (61.47) with colour back, a type flash, and clips half as long; the payoff ends on the biggest dunk
frozen and held. The song's most replayed stretch (55-68 s) is the middle of the edit.
New on top of the base set: freeze clones on the rise (static rim camera), ghost trail on the drive, type flash on
the drop, the numeral sandwich (hollow "1" behind, EDWARDS in front: first overall pick, 2020).
"""
import os, sys
KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the edits-kit folder
sys.path.insert(0, os.path.join(KIT, "tools"))
from plankit import Edit, RED, GARNET, GOLD

e = Edit("02_ant_sickomode", song_in=50.25, dur=23.61, gallery="ant")
C, F, S = e.C, e.F, e.S
LEAK = os.path.join(KIT, "assets", "overlays", "warm", "leak_a.mp4")   # make it with tools/overlays.py

# 0.00 the glare (quiet open)
k0 = e.add("1_025", 0.0, C(1.94), src=42.4, speed=0.8, zoom=[[0.0, 1.04], [C(1.94), 1.12]], still=True)
e.hit(F(S(51.74)), expo=[0.5, 0.15])                                                 # "Yeah": the flash follows the voice
# the bar build: arrival, handle, finish, absurd
k1 = e.add("1_051", C(1.94), C(2.72), src=76.4)                                     # the arrival
e.tr("blowout", C(1.94), leak=LEAK); e.hit(C(1.94), punch=[1.08, 0.3])
k2 = e.add("0_018", C(2.72), C(3.50), src=44.0)                                     # handle
e.tr("recipe", C(2.72), pattern="VT")
k3 = e.add("0_018", C(3.50), C(4.27), src=45.0)                                     # finish: the same drive, the layup
e.tr("zoomrush", C(3.50), amt=1.35)
k4 = e.add("0_061", C(4.27), C(5.05), src=128.7)                                    # absurd
e.tr("grid", C(4.27), pattern="pass", n=2, vertical=False, color=[0.94, 0.94, 0.88])
k5 = e.add("0_073", C(5.05), S(55.86), src=144.2)
e.tr("recipe", C(5.05), pattern="EKEK", line=[1, 0.85, 0.3])
# "Gone on you with the pick and roll": the drive and the poster dunk (the dunk lands on "roll")
k6 = e.add("1_004", S(55.86), S(57.90), src=15.35 - (S(57.60) - S(55.86)))
e.tr("blowout", S(55.86), leak=LEAK)
e.tr("ghost", S(55.86), clip=k6, t0=S(55.86) + 0.3, t1=S(57.60), n=6, dt=0.05)
e.hit(F(S(57.60)), punch=[1.12, 0.3], shake=[24, 0.35], sil=dict(clip=k6, frames=[0, 2], glow=45))
# "Young flame, he in SICKO MODE": the rise, frozen copies on the beats, the title builds
k7 = e.add("1_064", S(57.90), S(59.34), src=116.3)
e.tr("zoomrush", S(57.90), amt=1.3)
tc = [S(57.90) + 0.25, S(57.90) + 0.55, S(57.90) + 0.85]
e.tr("freezeclone", S(57.90), clip=k7, times=tc, t_end=F(S(59.00)))
e.hit(F(S(59.00)), sil=dict(clip=k7, frames=[0, 2], glow=45))
e.title(["SICKO", "MODE"], [S(59.00), S(59.34)], S(61.47))
# THE RESET: the beat drops out; poster-silhouette strobe, B&W, the lit doorway
k8 = e.add("1_026", S(59.34), S(61.47), src=47.4, speed=0.9, zoom=[[S(59.34), 1.04], [S(61.47), 1.14]])
e.tr("silstack", S(59.34), clipB=k8, pattern="PPK")
e.looks.append(dict(t0=S(59.34), t1=S(61.47), cc=dict(sat=0, con=40, exp=-0.3)))
# THE DROP (61.47, the strongest hit): colour, a type flash, clips half as long on every kick
k9 = e.add("0_030", S(61.47), C(11.61), src=66.0)
e.tr("typeflash", S(61.47), word="SICKO MODE", pattern="WB", size=290)
e.tr("grid", S(61.47) + 2 / 30, pattern="unfill", n=7, vertical=True, color=[1, 1, 1])
e.hit(S(61.47), punch=[1.14, 0.35], shake=[30, 0.45, 16, 3])
k10 = e.add("0_056", C(11.61), C(12.0), src=120.5)
e.tr("recipe", C(11.61), pattern="I")
k11 = e.add("0_022", C(12.0), C(12.39), src=59.0)
e.tr("recipe", C(12.0), pattern="I")
k12 = e.add("0_058", C(12.39), C(12.78), src=125.3)
e.tr("recipe", C(12.39), pattern="VT")
k13 = e.add("0_073", C(12.78), C(13.15), src=145.0)
e.tr("recipe", C(12.78), pattern="I")
k14 = e.add("1_065", C(13.15), C(13.93), src=119.6)
e.tr("blowout", C(13.15), leak=LEAK)
k15 = e.add("0_009", C(13.93), C(14.71), src=31.6)
e.tr("smear", C(13.93), vertical=True, tint=[1, 0.88, 0.3])
# "Make this here with all the ice on in the booth": the numeral sandwich
k16 = e.add("1_005", C(14.71), S(67.62), src=17.9)
e.tr("grid", C(14.71), pattern="fill", n=7, vertical=True, color=[1, 1, 1])
t0n = C(14.71) + 0.12
import typeset
gw = typeset.measure("1", "GalanoGrotesque-Black", 760)[0]
e.words.append(dict(text="1", t0=t0n, t1=S(67.62), style="outline", size=760, y=1300, x=e.side_x(k16, t0n + 0.5, gw), behind=k16,
                    color=[1, 0.82, 0.3], stroke=8))
e.words.append(dict(text="EDWARDS", t0=t0n + 0.15, t1=S(67.62), style="hero", font="Coolvetica-HeavyComp", size=220, y=1330, depth_color=[0.05, 0.25, 0.55]))
e.caption("1ST OVERALL PICK  ·  2020 NBA DRAFT", t0n + 0.25, S(67.62))
e.hit(t0n, sil=dict(clip=k16, frames=[0, 2], glow=45))
# "At the gate outside, when they pull up, they get me loose"
k17 = e.add("0_019", S(67.62), C(18.67), src=46.7)
e.tr("zoomrush", S(67.62), amt=1.3)
k18 = e.add("1_041", C(18.67), S(70.36), src=59.5)
e.tr("recipe", C(18.67), pattern="EKEK", line=[1, 0.85, 0.3])
# "Yeah, jump out, boys": the biggest dunk last, slowed, frozen on the flight, held past the line
spd = (66.30 - 65.55) / (S(72.36) - S(70.36))
k19 = e.add("0_030", S(70.36), e.dur, src=65.55, speed=spd, smooth=True)
e.tr("blowout", S(70.36), leak=LEAK)
sx, sy = e.subj_src(k19, S(72.36))
e.tr("popfreeze", S(72.36), clip=k19, frames=14, sx=sx, sy=sy)
e.hit(S(72.36) + 14 / 30, shake=[22, 0.35])
e.save(2, fade=0.6)
