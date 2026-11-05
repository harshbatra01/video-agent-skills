"""Edit 03: Lamine Yamal x Don Miguelo "Y Que Fue?" (song 8.0-37.7 s, 29.7 s, loops).

Base: THEME COMPILATION (celebrations) + LOOP (research pass 2). One celebration per beat-pair, escalating; the hook
"¿Y QUÉ FUE?" ("so what happened?", a taunt) lands on his arms-wide shrug, the repeat lands on his hand-to-ear; the
taunt line "No hiciste na'" ("you did nothing") rides the cheekiest celebrations. Opens and ends inside the same
smirk (hand on chin) so the loop seam is invisible; the song repeats its opening shout right after the end.
Base set: band framing, cuts on the strongest hits, flashes + his flash panels, number/word behind him with a white
silhouette. New on top: flash-on-word (exposure pops on the sung ad-libs), type flash on the hook, freeze-to-photo
prints, giant surname behind, impact frames, poster silhouettes.
Footage: the pilot's Yamal packs (pilot/catalog).
"""
import os, sys
KIT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))   # the edits-kit folder
sys.path.insert(0, os.path.join(KIT, "tools"))
from plankit import Edit, RED, GARNET, GOLD

e = Edit("03_yamal_yquefue", song_in=8.0, dur=29.7, catalog=os.path.join(KIT, "pilot", "catalog"), gallery="yamal")
C, F = e.C, e.F
LEAK = os.path.join(KIT, "assets", "overlays", "warm", "leak_a.mp4")   # make it with tools/overlays.py
CREDIT = "Y QUÉ FUE?  ·  DON MIGUELO"

# 0.00-0.77 the smirk (hand on chin), quiet; the end continues this same shot backwards so the loop is seamless
k0 = e.add("0_062", 0.0, C(0.77), src=189.9, speed=0.9, zoom=[[0.0, 1.04], [C(0.77), 1.12]], still=True)
e.hit(F(0.70), expo=[0.6, 0.15])                                                    # "BAMBO": the flash follows the voice
k1 = e.add("3_006", C(0.77), C(2.11), src=12.45)                                    # knee slide
e.tr("blowout", C(0.77), leak=LEAK); e.hit(C(0.77), punch=[1.1, 0.3], shake=[16, 0.3])
k2 = e.add("2_005", C(2.11), C(3.91), src=17.6)                                     # climbs the stand
e.tr("recipe", C(2.11), pattern="VT"); e.hit(C(2.11), shake=[20, 0.3])
k3 = e.add("2_010", C(3.91), C(4.36), src=43.9)                                     # the kiss
e.tr("zoomrush", C(3.91), amt=1.4)
k4 = e.add("2_010", C(4.36), C(6.63), src=45.2)                                     # Camp Nou, arms up
e.hit(F(4.40), expo=[0.5, 0.15])                                                    # "CHAPA"
e.number("YAMAL", C(4.36), C(6.63), k4, size=760, font="Coolvetica-HeavyComp", depth_color=GARNET, lift=0.15)
k5 = e.add("2_011", C(6.63), C(8.66), src=49.2)                                     # pointing up
e.tr("grid", C(6.63), pattern="pass", n=2, vertical=False, color=[0.94, 0.94, 0.88])
e.hit(F(7.54), expo=[0.5, 0.15])
k6 = e.add("2_002", C(8.66), C(10.23), src=6.0)                                     # close-up, the gesture
e.tr("silstack", C(8.66), clipB=k6, pattern="PPK")
k7 = e.add("2_003", C(10.23), C(11.59), src=10.4)                                   # sits with the fans
e.tr("smear", C(10.23), vertical=True, tint=[1, 0.88, 0.3]); e.hit(F(11.06), expo=[0.5, 0.15])
k8 = e.add("0_071", C(11.59), C(13.18), src=218.0)                                  # hands on head
e.tr("blowout", C(11.59), leak=LEAK)
k9 = e.add("3_010", C(13.18), C(13.84), src=22.4)                                   # pointed at, grinning
e.tr("recipe", C(13.18), pattern="EKEK", line=[1, 0.85, 0.3])
k10 = e.add("2_004", C(13.84), C(14.74), src=15.3)
e.tr("typeflash", C(13.84), word="¿Y QUÉ FUE?", pattern="WB", size=300)            # the hook arrives as a type flash
# THE HOOK: "¿Y QUÉ FUE?" on the shrug; the title builds in the top bar word by word, his head breaks out over it
k11 = e.add("2_007", C(14.74), C(16.79), src=29.4, speed=0.85)
e.tr("grid", C(14.74), pattern="fill", n=7, vertical=True, color=[1, 1, 1])
e.title(["¿Y", "QUÉ", "FUE?"], [14.92, 15.60, 15.82], C(16.79), pop=k11)
e.caption("DON MIGUELO", F(15.0), C(16.79))
e.hit(F(15.82), punch=[1.08, 0.3], sil=dict(clip=k11, frames=[0, 2], glow=45))
# "No hiciste na'": the cheekiest celebrations, two of them frozen into prints
k12 = e.add("2_008", C(16.79), C(18.59), src=37.5)
e.tr("zoomrush", C(16.79), amt=1.4)
e.lyric_line(["NO", "HICISTE", "NA'"], [16.54, 17.22, 17.64], C(18.59) - 0.45)
e.tr("print", C(18.59) - 0.43, clip=k12, frames=13, label=CREDIT)
k13 = e.add("0_044", C(18.59), C(20.40), src=131.6)
e.tr("blowout", C(18.59), leak=LEAK)
k14 = e.add("0_039", C(20.40), C(22.20), src=110.9)
e.tr("grid", C(20.40), pattern="fill", n=5, vertical=False, color=[1, 1, 1])
e.tr("print", C(22.20) - 0.43, clip=k14, frames=13, label="LAMINE YAMAL", rot=2.5)
k15 = e.add("2_005", C(22.20), C(23.10), src=22.15)                                 # hand to ear: "¿y qué fue?"
e.tr("recipe", C(22.20), pattern="VT")
e.tr("typeflash", F(22.54), word="¿Y QUÉ FUE?", pattern="WB", size=300)
k16 = e.add("1_014", C(23.10), C(25.81), src=55.4)                                  # the knee slide, wide
e.tr("grid", C(23.10), pattern="centre", n=7, vertical=True, color=[0.94, 0.94, 0.88])
e.hit(C(25.81) - 0.6, sil=dict(clip=k16, frames=[0, 2], glow=40))
k17 = e.add("3_000", C(25.81), C(27.38), src=0.3)                                   # under the lights
e.tr("defocus", C(25.81), cast=[1, 0.75, 0.45])
k18 = e.add("0_067", C(27.38), C(28.29), src=202.4)                                 # with the team
e.tr("smear", C(27.38), vertical=True)
k19 = e.add("0_062", C(28.29), e.dur, src=188.65, speed=(189.9 - 188.65) / (e.dur - C(28.29)), still=True,
            zoom=[[C(28.29), 1.12], [e.dur, 1.04]], name="0_062 smirk (loop end)")
e.tr("blowout", C(28.29), leak=LEAK)
e.save(1, fade=None)
