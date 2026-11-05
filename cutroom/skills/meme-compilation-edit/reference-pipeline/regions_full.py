"""Speech regions + sub-phrase pieces over the whole recording (same thresholds as the 2-min test)."""
import json, numpy as np
db = np.load("db10ms.npy")
TH, FILL, MINBLOB, PRE, POST, MERGE = -60, 0.20, 0.08, 0.10, 0.15, 0.15
idx = np.where(db > TH)[0]
blobs = []; s = p = idx[0]
for i in idx[1:]:
    if (i - p) / 100 > FILL:
        blobs.append([s / 100, (p + 1) / 100]); s = i
    p = i
blobs.append([s / 100, (p + 1) / 100])
keep = [[max(0, a - PRE), b + POST] for a, b in blobs if b - a >= MINBLOB]
regions = []
for k in keep:
    if regions and k[0] - regions[-1][1] < MERGE:
        regions[-1][1] = max(regions[-1][1], k[1])
    else:
        regions.append(k[:])
regions = [[round(a, 2), round(b, 2)] for a, b in regions]
# pieces: split each region at internal quiet runs >= 0.18 s
pieces = []
for ri, (a, b) in enumerate(regions):
    seg = db[int(a * 100):int(b * 100)]
    quiet = seg < -62
    cuts, i = [], 0
    while i < len(quiet):
        if quiet[i]:
            j = i
            while j < len(quiet) and quiet[j]:
                j += 1
            if j - i >= 18 and i > 0 and j < len(quiet):
                cuts.append((i + j) // 2)
            i = j
        else:
            i += 1
    bounds = [0] + cuts + [len(seg)]
    for s0, e0 in zip(bounds[:-1], bounds[1:]):
        if e0 - s0 >= 8:
            pieces.append({"region": ri, "a": round(a + s0 / 100, 2), "b": round(a + e0 / 100, 2)})
json.dump({"regions": regions, "pieces": pieces}, open("regions_full.json", "w"))
tot = sum(b - a for a, b in regions)
print(f"{len(regions)} regions, {len(pieces)} pieces, {tot:.1f} s of speech-with-padding out of {len(db)/100:.0f} s")
