"""Add the blur masks and house preset names to the built copy of the editor's project (after build_pass.jsx).
Every mask gets the editor's feather (10 image px, at least 20 px on screen). Reveal wipes slide their top edge down to the bottom; boxes and curse
boxes are static (a box on slanted text uses its four-corner outline)."""
import json, shutil, sys
sys.path.insert(0, ".")
from prproj_masks import Project

edl = json.load(open("data/edl_pass.json"))
PROJ = "/CHANGE/ME/<editor project copy> edit.prproj"
SEQ = edl["seq"]
# Effect instance names shown in Premiere's Effect Controls. Set them to the client's own preset names so their editor
# recognises each blur at a glance (the reference job used the client editor's preset names).
NAMES = {"wipe": "blur wipe", "box": "blur box", "curse": "blur curse", "blackout": "black box (hide words)"}
CROP_NAME = "Crop Normal"
TPF = 8467200000

shutil.copy(PROJ, "data/build_pass_unpatched.prproj")
p = Project(PROJ)
v3 = p.track_items(SEQ, "VideoTrackGroup", 2)
assert len(v3) == len(edl["images"]), (len(v3), len(edl["images"]))
masks = 0
for (start, end, item), spec in zip(v3, edl["images"]):
    assert abs(start - round(spec["start"] * 30) * TPF) < TPF, (start, spec["file"])
    if spec.get("skip"):
        continue
    comps = p.chain_components(item)
    gbs = [c.attrib["ObjectID"] for c in comps if c.findtext("MatchName") == "AE.ADBE Gaussian Blur 2"]
    crops = [c.attrib["ObjectID"] for c in comps if c.findtext("MatchName") == "AE.ADBE AECrop"]
    assert len(gbs) == len(spec["blurs"]), (spec["file"], len(gbs), len(spec["blurs"]))
    media_in = p.media_in_seconds(item)
    sp = spec.get("speed", 1.0)
    for gb, bl in zip(gbs, spec["blurs"]):
        box = bl["box"]
        if bl["kind"] == "wipe":
            t0, t1 = bl["path_keys"]
            collapsed = [box[0], box[3] - 0.002, box[2], box[3]]       # top edge slides down to the bottom
            p.add_mask(gb, keys=[(media_in + t0 * sp, box), (media_in + t1 * sp, collapsed)], feather=bl["feather"], hash_mode="fake")
        else:
            p.add_mask(gb, box=box, feather=bl["feather"], hash_mode="fake")
        p.set_instance_name(gb, NAMES[bl["kind"]])
        masks += 1
    for cr in crops:
        p.set_instance_name(cr, CROP_NAME)
p.save()
print(f"patched {masks} masks on {sum(1 for s in edl['images'] if not s.get('skip'))} memes")
