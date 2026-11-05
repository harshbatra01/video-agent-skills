"""Timeline loader: every track item with sequence start/end, media in/out, clip object, components."""
import os
import xml.etree.ElementTree as ET
TPS = 254016000000; TPF = 8467200000
class TL:
    def __init__(self, path, seq_name=os.environ.get("MEME_SEQ", "CHANGE_ME sequence")):   # or set MEME_SEQ
        root = ET.parse(path).getroot()
        self.by_id = {e.attrib["ObjectID"]: e for e in root if "ObjectID" in e.attrib}
        self.by_uid = {e.attrib["ObjectUID"]: e for e in root if "ObjectUID" in e.attrib}
        self.tracks = {}
        for seq in self.by_uid.values():
            if seq.tag == "Sequence" and seq.findtext("Name") == seq_name:
                for tg in seq.findall(".//TrackGroups/TrackGroup"):
                    g = self.ref(tg.find("Second"))
                    if g is None: continue
                    k = "V" if g.tag == "VideoTrackGroup" else "A"
                    for i, t in enumerate(g.findall(".//Tracks/Track")):
                        tr = self.ref(t)
                        items = []
                        for ti in tr.findall(".//ClipItems/TrackItems/TrackItem"):
                            it = self.ref(ti)
                            sub = self.ref(it.find(".//SubClip"))
                            clip = self.ref(sub.find("Clip")) if sub is not None else None
                            d = {"start": int(it.findtext(".//TrackItem/Start")), "end": int(it.findtext(".//TrackItem/End")),
                                 "name": sub.findtext("Name") if sub is not None else None, "item": it, "clip": clip,
                                 "in": int(clip.findtext("./Clip/InPoint") or clip.findtext(".//InPoint")) if clip is not None else None,
                                 "out": int(clip.findtext("./Clip/OutPoint") or clip.findtext(".//OutPoint")) if clip is not None else None,
                                 "speed": float(clip.findtext(".//PlaybackSpeed") or 1) if clip is not None else 1}
                            items.append(d)
                        items.sort(key=lambda d: d["start"])
                        trans = []
                        for ti in tr.findall(".//TransitionItems/TrackItems/TrackItem"):
                            it = self.ref(ti)
                            trans.append(it)
                        self.tracks[f"{k}{i+1}"] = {"items": items, "trans": trans, "el": tr}
    def ref(self, el):
        if el is None: return None
        a = el.attrib
        return self.by_id.get(a.get("ObjectRef")) if "ObjectRef" in a else self.by_uid.get(a.get("ObjectURef"))
    def seq_to_raw(self, t, track="A1"):
        """sequence ticks -> raw recording seconds (None if no voice clip there)"""
        for d in self.tracks[track]["items"]:
            if d["start"] <= t < d["end"]:
                return (d["in"] + (t - d["start"]) * d["speed"]) / TPS
        return None
    def raw_to_seq(self, r, track="A1"):
        for d in self.tracks[track]["items"]:
            if d["in"] <= r * TPS < d["in"] + (d["end"] - d["start"]):
                return (d["start"] + r * TPS - d["in"]) / TPS
        return None
