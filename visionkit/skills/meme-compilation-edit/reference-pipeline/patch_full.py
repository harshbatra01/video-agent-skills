"""Full edit: add the blur masks, house preset names and +15 dB clip gain to the saved project."""
import json, shutil, sys
sys.path.insert(0, ".")
from prproj_masks import Project
from xml_gap_audit import audit

edl = json.load(open("edl_full.json"))
PROJ = "/CHANGE/ME/<job> edit v2.prproj"
SEQ = "CHANGE_ME sequence"
# Effect instance names shown in Premiere's Effect Controls. Set them to the client's own preset names so their editor
# recognises each blur at a glance (the reference job used the client editor's preset names).
NAMES = {"wipe": "blur wipe", "box": "blur box", "curse": "blur curse", "blackout": "black box (hide words)"}
CROP_NAME = "Crop Normal"
GAIN_15DB = 5.6234130859375   # the clip gain value the editor uses on every voice clip

bad = audit(PROJ, SEQ)
if bad:
    raise SystemExit("GAP AUDIT FAILED, not patching: " + "; ".join(bad))
shutil.copy(PROJ, "build_full_unpatched.prproj")
p = Project(PROJ)
v3 = p.track_items(SEQ, "VideoTrackGroup", 2)
assert len(v3) == len(edl["images"]), (len(v3), len(edl["images"]))
masks = 0
for (start, end, item), spec in zip(v3, edl["images"]):
    assert start == spec["start_f"] * 8467200000, (start, spec["file"])
    comps = p.chain_components(item)
    gbs = [c.attrib["ObjectID"] for c in comps if c.findtext("MatchName") in ("AE.ADBE Gaussian Blur 2", "AE.ADBE Tint")]
    crops = [c.attrib["ObjectID"] for c in comps if c.findtext("MatchName") == "AE.ADBE AECrop"]
    assert len(gbs) == len(spec["blurs"]), (spec["file"], len(gbs), len(spec["blurs"]))
    media_in = p.media_in_seconds(item)
    for gb, bl in zip(gbs, spec["blurs"]):
        box = bl["box"]
        if bl["kind"] == "wipe":
            t0, t1 = bl["path_keys"]
            collapsed = [box[0], box[3] - 0.002, box[2], box[3]]   # top edge slides down to the bottom
            sp = spec.get("speed", 1.0)   # keyframes on speed-changed clips are stored in media time
            p.add_mask(gb, keys=[(media_in + t0 * sp, box), (media_in + t1 * sp, collapsed)], feather=bl.get("feather", 10.0), hash_mode="fake")
        else:
            p.add_mask(gb, box=box, feather=bl.get("feather", 10.0), hash_mode="fake")
        p.set_instance_name(gb, NAMES[bl["kind"]])
        masks += 1
    for cr in crops:
        p.set_instance_name(cr, CROP_NAME)

# video memes: whole media fitted to the slot with a speed change (how the editor does it)
import re, subprocess
TPS = 254016000000
for (start, end, item), spec in zip(v3, edl["images"]):
    if not spec.get("video"):
        continue
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", spec["path"]],
                               capture_output=True, text=True).stdout)
    m_ticks = round(dur * TPS)
    speed = m_ticks / (end - start)
    clip_id = p.ref(p.ref(item.find(".//SubClip")).find("Clip")).attrib["ObjectID"]
    def fix(block, m_ticks=m_ticks, speed=speed):
        block = re.sub(r"<PlaybackSpeed>[^<]*</PlaybackSpeed>", "<PlaybackSpeed>%r</PlaybackSpeed>" % speed, block)
        block = re.sub(r"<InPoint>[^<]*</InPoint>", "<InPoint>0</InPoint>", block, count=1)
        return re.sub(r"<OutPoint>[^<]*</OutPoint>", "<OutPoint>%d</OutPoint>" % m_ticks, block, count=1)
    p._replace_object(clip_id, fix)
    print(f"video {spec['file']}: {dur:.3f}s media into {(end - start) / 8467200000:.0f} frames, speed {speed:.4f}")

a1 = p.track_items(SEQ, "AudioTrackGroup", 0)
clip_ids = []
for _, _, item in a1:
    sub = p.ref(item.find(".//SubClip"))
    clip_ids.append(p.ref(sub.find("Clip")).attrib["ObjectID"])
# +15 dB like the editor, except on clips whose peak would clip: those get just enough to peak at -0.5 dBFS
import wave, numpy as np
w = wave.open("raw_st48.wav"); sr = w.getframerate(); nch = w.getnchannels()
pcm = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).reshape(-1, nch).astype(np.float32) / 32768
voice = np.abs(pcm[:, 1] if nch > 1 else pcm[:, 0])   # the mic is on the right channel
assert len(a1) == len(edl["cuts"]), (len(a1), len(edl["cuts"]))
ceiling = 10 ** (-0.5 / 20)
low = []
for n, (cid, c) in enumerate(zip(clip_ids, edl["cuts"])):
    pk = float(voice[int(c["raw_in_f"] / 30 * sr):int(c["raw_out_f"] / 30 * sr)].max())
    g = GAIN_15DB if pk * GAIN_15DB <= ceiling else ceiling / pk
    if g < GAIN_15DB:
        low.append(f"cut {n} at {c['out_start_f'] / 30:.1f}s: {20 * np.log10(g):.1f} dB")
    p.set_audio_gain([cid], g)
print("gain below +15 dB to avoid clipping:", low or "none")
p.save()
print(f"patched {masks} masks on {len(v3)} memes, gain on {len(clip_ids)} audio clips")
