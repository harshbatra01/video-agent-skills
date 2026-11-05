"""Build the 'our edit' data for the bank page: filmstrip sprite, key frames, loudness, hits, events.

usage: python page_assets.py video.mp4 beats.json out.json
"""
import sys, json, io, base64
import av
from PIL import Image

video, beats, out = sys.argv[1], sys.argv[2], sys.argv[3]
bj = json.load(open(beats))
STEP = 6            # every 6th frame = 0.2 s
TW, TH = 80, 59     # sprite cell (picture band 1080x800 -> 80x59)
BAND = (0, 560, 1080, 1360)
KEYS = {1: "Silhouette strobe", 81: "Music video whip blur", 98: "MBAPPE 10 still", 107: "GASS logo slam",
        168: "Light-bar wipe", 223: "Dip to white, whip", 285: "Silhouette strobe", 301: "Inverse strobe",
        509: "Portal frame", 521: "Spotify end card"}

c = av.open(video); s = c.streams.video[0]; fps = float(s.average_rate)
cells, keys = [], {}
for i, fr in enumerate(c.decode(s)):
    if i % STEP == 0 or i in KEYS:
        im = fr.to_image().crop(BAND)
        if i % STEP == 0:
            cells.append(im.resize((TW, TH), Image.LANCZOS))
        if i in KEYS:
            k = im.resize((300, 222), Image.LANCZOS)
            b = io.BytesIO(); k.save(b, "JPEG", quality=72)
            keys[i] = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()
n = i + 1
c.close()
sprite = Image.new("RGB", (TW * len(cells), TH))
for k, im in enumerate(cells):
    sprite.paste(im, (k * TW, 0))
b = io.BytesIO(); sprite.save(b, "JPEG", quality=60)
sprite_uri = "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()

events = [
    (0.03, "strobe", "White silhouette on the player, 2 frames with a 1-frame gap"),
    (0.93, "strobe", "Silhouette strobe on the defenders"),
    (1.73, "strobe", "Silhouette strobe"),
    (2.53, "blur", "Blur flash into the music video"),
    (2.60, "blur", "Whip / directional blur, buildings"),
    (3.03, "blur", "Radial zoom blur on the artist"),
    (3.20, "flash", "White flash"),
    (3.23, "still", "MBAPPE 10 back photo, push-in"),
    (3.53, "logo", "GASS logo slams in with vertical motion blur"),
    (4.07, "flash", "1-frame white flash"),
    (4.10, "drop", "DROP: hard cut into the first dribble"),
    (5.57, "wipe", "Light-bar wipe (3 frames)"),
    (7.30, "flash", "Dip to white"),
    (7.70, "flash", "Dip to white"),
    (8.23, "flash", "Dip to white"),
    (9.10, "flash", "Dip to white"),
    (9.43, "strobe", "Silhouette strobe x3"),
    (9.90, "strobe", "Inverse strobe: background white, player stays"),
    (10.30, "flash", "1-frame white flash"),
    (12.30, "wipe", "Light-bar wipe"),
    (13.67, "flash", "Dip to white"),
    (16.30, "blur", "Mirror-edge spin on the net"),
    (16.97, "portal", "Portal frame into the tunnel"),
    (17.00, "blur", "Car tunnel whip blur"),
    (17.37, "card", "Spotify end card, static for 3.2 s"),
]
cuts = [76, 77, 82, 89, 106, 107, 108, 121, 122, 123, 167, 168, 169, 170, 204, 219, 220, 232, 234, 247, 248, 250,
        273, 274, 276, 309, 310, 334, 347, 369, 370, 371, 372, 399, 410, 411, 413, 450, 489, 509, 510, 516, 521]
data = dict(
    fps=fps, frames=n, dur=round(n / fps, 2), bpm=bj["bpm"], step=STEP, cell=[TW, TH], ncells=len(cells),
    sprite=sprite_uri, keys=[dict(f=f, t=round(f / fps, 2), label=KEYS[f], src=keys[f]) for f in sorted(keys)],
    rms=bj["rms_db"], kicks=[round(t, 2) for t, _ in bj["kicks"]], snares=[round(t, 2) for t, _ in bj["snares"]],
    cuts=[round(f / fps, 3) for f in cuts],
    events=[dict(t=t, type=ty, label=l) for t, ty, l in events],
    sections=[dict(a=0, b=2.53, name="Intro", note="letterboxed dribble, silhouette strobes"),
              dict(a=2.53, b=4.10, name="Build", note="music video whips, photo, logo slam"),
              dict(a=4.10, b=17.37, name="Main", note="19 shots, average 0.7 s"),
              dict(a=17.37, b=20.6, name="End card", note="static 3.2 s")],
)
json.dump(data, open(out, "w"))
print(f"frames {n}, cells {len(cells)}, sprite {len(sprite_uri)//1024} KB, keys {sum(len(v) for v in keys.values())//1024} KB")
