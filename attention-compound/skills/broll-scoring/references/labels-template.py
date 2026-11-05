# Eye labels for every shot, from the contact sheets (19 Oct 2026). Ranges share one label.
# Fields: shows | type | subject size (% of frame, eye estimate) | Q quality 0-5 | F framing 0-5 | M match to words 0-5 | note
# type: clip = moving footage, still = photo (often with push), card = text/number card, gfx = built graphic,
#       news = broadcast clip with chyron, grid = multi-picture collage
REF = """
1|Altman two-shot photo, face pixel-blocked, giant SCARIEST whip|still|45|4|5|5|hook: the subject is on screen on word 1
2|polaroid of the same photo on black, pushes in|still|30|4|4|5|
"""
OURS = """
1|Musk seated photo, pixel blocks clearing|still|35|4|4|5|
7|gold bar, dark, bar cut off at the bottom|clip|15|2|1|4|USER NOTE: under 20% of frame and cropped
"""
def parse(s):
    out = {}
    for ln in s.strip().splitlines():
        n, shows, typ, subj, q, f, m, note = ln.split("|")
        out[int(n)] = dict(shows=shows, type=typ, subj=int(subj), Q=int(q), F=int(f), M=int(m), note=note)
    return out
