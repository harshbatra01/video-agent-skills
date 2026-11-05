"""Per-clip effect dump of one sequence track (gunzipped .prproj XML): motion, crop, blurs, masks (decoded paths)."""
import sys, json, base64, struct
import xml.etree.ElementTree as ET
TPS = 254016000000

def load(path):
    root = ET.parse(path).getroot()
    by_id = {e.attrib["ObjectID"]: e for e in root if "ObjectID" in e.attrib}
    by_uid = {e.attrib["ObjectUID"]: e for e in root if "ObjectUID" in e.attrib}
    def ref(el):
        if el is None: return None
        a = el.attrib
        return by_id.get(a.get("ObjectRef")) if "ObjectRef" in a else by_uid.get(a.get("ObjectURef"))
    return by_id, by_uid, ref

def decode_path(b64):
    b = base64.b64decode(b64)
    if b[:4] != b"2cin": return None
    n = struct.unpack("<I", b[12:16])[0]
    pts = []
    for k in range(n):
        o = 16 + k * 32
        vals = struct.unpack("<I6fI", b[o:o + 32])
        pts.append((round(vals[1], 4), round(vals[2], 4)))
    return pts

def param(p):
    out = {"name": p.findtext("Name")}
    sk = p.findtext("StartKeyframe")
    if sk: out["start"] = sk.split(",")[1] if "," in sk else sk
    kf = p.findtext("Keyframes")
    if kf: out["keys"] = kf
    sv = p.find("StartKeyframeValue")
    if sv is not None and sv.text and sv.text.strip():
        out["value_b64"] = sv.text.strip()
    tv = p.findtext("IsTimeVarying")
    if tv: out["timevary"] = tv
    return out

def comp_info(c, ref):
    info = {"match": c.findtext(".//MatchName"), "instance": c.findtext(".//InstanceName"), "params": [], "masks": []}
    for pe in c.findall("./Component/Params/Param") + c.findall("./Params/Param"):
        p = ref(pe)
        if p is not None: info["params"].append(param(p))
    for se in c.findall("./SubComponents/SubComponent"):
        s = ref(se)
        if s is not None: info["masks"].append(comp_info(s, ref))
    return info

def dump(path, seq_name, kind="VideoTrackGroup", idx=2):
    by_id, by_uid, ref = load(path)
    for seq in by_uid.values():
        if seq.tag == "Sequence" and seq.findtext("Name") == seq_name:
            for tg in seq.findall(".//TrackGroups/TrackGroup"):
                g = ref(tg.find("Second"))
                if g is None or g.tag != kind: continue
                tr = [ref(t) for t in g.findall(".//Tracks/Track")][idx]
                out = []
                for ti in tr.findall(".//ClipItems/TrackItems/TrackItem"):
                    it = ref(ti)
                    sub = ref(it.find(".//SubClip"))
                    clip = ref(sub.find("Clip")) if sub is not None else None
                    chain = ref(it.find("./ClipTrackItem/ComponentOwner/Components"))
                    comps = [comp_info(ref(c), ref) for c in chain.findall(".//Components/Component")] if chain is not None else []
                    out.append({"name": sub.findtext("Name") if sub is not None else None,
                                "start": int(it.findtext(".//TrackItem/Start")) / TPS, "end": int(it.findtext(".//TrackItem/End")) / TPS,
                                "media_in": int(clip.findtext(".//InPoint")) / TPS if clip is not None else None, "fx": comps})
                return sorted(out, key=lambda x: x["start"])
    raise KeyError(seq_name)

if __name__ == "__main__":
    json.dump(dump(sys.argv[1], sys.argv[2], idx=int(sys.argv[4]) if len(sys.argv) > 4 else 2), open(sys.argv[3], "w"), indent=1)
