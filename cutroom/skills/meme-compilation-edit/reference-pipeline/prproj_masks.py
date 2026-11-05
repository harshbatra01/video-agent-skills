"""Add Premiere effect masks (and preset-style instance names, clip gain) to a saved .prproj.

Premiere's scripting API cannot create masks, so this edits the project XML directly,
cloning the mask structure Premiere itself writes (24 parameters, 2cin path blobs).

Proven on Premiere Pro 2025 (25.x) projects in meme edits. Premiere 2026 projects use a different mask component
(AE.ADBE AEMask2): use our premiere-ae-editing skill there (references/prproj-format.md section 8, prproj_lib.mask_path_blob).
StartKeyframeValue needs a BinaryHash attribute or Premiere silently drops the path, so add_mask writes a unique
placeholder hash by default (hash_mode="fake", what every build used); hash_mode="none" leaves it out.
"""
import base64, gzip, os, re, struct, xml.etree.ElementTree as ET

TPS = 254016000000
HERE = os.path.dirname(os.path.abspath(__file__))
# The mask to clone. Default: mask_template_pp2025.xml next to this script, which holds one Gaussian Blur mask
# (MatchName "AE.ADBE AEMask", 24 params) exactly as Premiere Pro 2025 wrote it in a finished editor's project.
# Or set PRPROJ_MASK_TEMPLATE to any .prproj that has at least one such mask: its first mask is used.
TEMPLATE = os.environ.get("PRPROJ_MASK_TEMPLATE", os.path.join(HERE, "mask_template_pp2025.xml"))

def path_blob(box):
    """Rectangle [x0,y0,x1,y1] or a four-corner outline [[x,y] TL, TR, BR, BL] (0-1, source-image space) -> base64 2cin
    path. The outline lets a box follow slanted text, like a shop sign in a photo (Oct 13 2026)."""
    if len(box) == 4 and isinstance(box[0], (list, tuple)):
        pts = [(float(x), float(y)) for x, y in box]
    else:
        x0, y0, x1, y1 = box
        pts = [(x0, y0), (x1, y0), (x1, y1), (x0, y1)]
    b = b"2cin" + struct.pack("<III", 2, 0, len(pts))
    for x, y in pts:
        b += struct.pack("<I6fI", 0, x, y, x, y, x, y, 1)
    return base64.b64encode(b).decode()

_MASK_RE = r'\n\t<VideoFilterComponent ObjectID="(\d+)"[^>]*>(?:(?!\n\t</VideoFilterComponent>).)*?<MatchName>AE\.ADBE AEMask</MatchName>'

def _load_template(path=None):
    path = path or TEMPLATE
    if path.endswith(".prproj"):
        s = gzip.open(path, "rt", encoding="utf-8").read()
    else:
        s = open(path, encoding="utf-8").read()
    m = re.search(_MASK_RE, s, re.S)
    if not m:
        raise ValueError("no Gaussian Blur mask (AE.ADBE AEMask) found in " + path)
    def obj(oid):
        return re.search(r'\n\t<(\w+) ObjectID="%s"[^>]*>.*?\n\t</\1>' % oid, s, re.S).group(0)
    mask = obj(m.group(1))
    params = re.findall(r'<Param Index="(\d+)" ObjectRef="(\d+)"', mask)
    return mask, [(int(i), obj(r), r) for i, r in params]

_MASK, _PARAMS = None, None

def _template():
    global _MASK, _PARAMS
    if _MASK is None:
        _MASK, _PARAMS = _load_template()
    return _MASK, _PARAMS

class Project:
    def __init__(self, path):
        self.path = path
        self.text = gzip.open(path, "rt", encoding="utf-8").read()
        self.next_id = max(int(x) for x in re.findall(r'ObjectID="(\d+)"', self.text)) + 1
        self.new_objects = []
        self._index()

    def _index(self):
        root = ET.fromstring(self.text)
        self.by_id = {e.attrib["ObjectID"]: e for e in root if "ObjectID" in e.attrib}
        self.by_uid = {e.attrib["ObjectUID"]: e for e in root if "ObjectUID" in e.attrib}

    def ref(self, el):
        if el is None:
            return None
        a = el.attrib
        return self.by_id.get(a.get("ObjectRef")) if "ObjectRef" in a else self.by_uid.get(a.get("ObjectURef"))

    def track_items(self, seq_name, kind="VideoTrackGroup", track_index=0):
        """[(start_ticks, end_ticks, trackitem_el)] for one track of a sequence, in time order."""
        for seq in self.by_uid.values():
            if seq.tag == "Sequence" and seq.findtext("Name") == seq_name:
                for tg in seq.findall(".//TrackGroups/TrackGroup"):
                    g = self.ref(tg.find("Second"))
                    if g is None or g.tag != kind:
                        continue
                    tracks = [self.ref(t) for t in g.findall(".//Tracks/Track")]
                    tr = tracks[track_index]
                    out = []
                    for ti in tr.findall(".//ClipItems/TrackItems/TrackItem"):
                        it = self.ref(ti)
                        out.append((int(it.findtext(".//TrackItem/Start")), int(it.findtext(".//TrackItem/End")), it))
                    return sorted(out, key=lambda x: x[0])
        raise KeyError(seq_name)

    def chain_components(self, trackitem):
        chain = self.ref(trackitem.find("./ClipTrackItem/ComponentOwner/Components"))
        return [self.ref(c) for c in chain.findall(".//Components/Component")]

    def media_in_seconds(self, trackitem):
        sub = self.ref(trackitem.find(".//SubClip"))
        clip = self.ref(sub.find("Clip"))
        return int(clip.findtext(".//InPoint")) / TPS

    # ---- text edits ----
    def _replace_object(self, oid, fn):
        pat = re.compile(r'(\n\t<(\w+) ObjectID="%s"[^>]*>.*?\n\t</\2>)' % oid, re.S)
        m = pat.search(self.text)
        self.text = self.text[:m.start(1)] + fn(m.group(1)) + self.text[m.end(1):]

    def set_instance_name(self, comp_id, name):
        def f(block):
            if "<InstanceName>" in block:
                return re.sub(r"<InstanceName>[^<]*</InstanceName>", "<InstanceName>%s</InstanceName>" % name, block)
            return block.replace("<Intrinsic>false</Intrinsic>", "<Intrinsic>false</Intrinsic>\n\t\t\t<InstanceName>%s</InstanceName>" % name, 1)
        self._replace_object(comp_id, f)

    def add_mask(self, gb_comp_id, box=None, keys=None, feather=10.0, hash_mode="fake"):
        """Attach a mask to a Gaussian Blur component.
        box: static rectangle; keys: [(media_seconds, box), ...] for an animated path."""
        _mask_tpl, _params_tpl = _template()
        mask_id = self.next_id; self.next_id += 1
        idmap = {}
        objs = []
        for idx, block, old in _params_tpl:
            nid = self.next_id; self.next_id += 1
            idmap[old] = nid
            nb = re.sub(r'ObjectID="\d+"', 'ObjectID="%d"' % nid, block, count=1)
            if "<Name>Mask Path</Name>" in nb:
                start_box = box if box is not None else keys[0][1]
                blob = path_blob(start_box)
                if hash_mode == "none":
                    sv = '<StartKeyframeValue Encoding="base64">%s\n\t\t</StartKeyframeValue>' % blob
                else:  # unique placeholder hash + Premiere's length field (len + 12)
                    ln = len(base64.b64decode(blob)) + 12
                    hx = os.urandom(12).hex()
                    h = "%s-%s-%s-%s-%s%08x" % (hx[0:8], hx[8:12], hx[12:16], hx[16:20], hx[20:24], ln)
                    sv = '<StartKeyframeValue Encoding="base64" BinaryHash="%s">%s\n\t\t</StartKeyframeValue>' % (h, blob)
                nb = re.sub(r"<StartKeyframeValue[^>]*>.*?</StartKeyframeValue>", sv, nb, flags=re.S)
                if keys:
                    ks = "".join("%d,%s;" % (round(t * TPS), path_blob(b)) for t, b in keys)
                    nb = nb.replace("<IsTimeVarying>false</IsTimeVarying>", "<IsTimeVarying>true</IsTimeVarying>")
                    nb = nb.replace("<StartKeyframePosition>", "<Keyframes>%s</Keyframes>\n\t\t<StartKeyframePosition>" % ks)
            if "<Name>Mask Feather</Name>" in nb:
                nb = re.sub(r"<StartKeyframe>[^<]*</StartKeyframe>", "<StartKeyframe>-91445760000000000,%s,0,0,0,0,0,0</StartKeyframe>" % repr(float(feather)), nb)
            objs.append(nb)
        mb = re.sub(r'ObjectID="\d+"', 'ObjectID="%d"' % mask_id, _mask_tpl, count=1)
        mb = re.sub(r'<Param Index="(\d+)" ObjectRef="(\d+)"/>', lambda m: '<Param Index="%s" ObjectRef="%d"/>' % (m.group(1), idmap[m.group(2)]), mb)
        self.new_objects.append(mb)
        self.new_objects.extend(objs)

        def f(block):
            if "<SubComponents" in block:
                raise ValueError("component %s already has a mask" % gb_comp_id)
            return block.replace("\t\t<MatchName>", '\t\t<SubComponents Version="1">\n\t\t\t<SubComponent Index="0" ObjectRef="%d"/>\n\t\t</SubComponents>\n\t\t<MatchName>' % mask_id, 1)
        self._replace_object(gb_comp_id, f)
        return mask_id

    def set_audio_gain(self, audio_clip_ids, gain_linear):
        for oid in audio_clip_ids:
            def f(block):
                if "<Gain>" in block:
                    return re.sub(r"<Gain>[^<]*</Gain>", "<Gain>%s</Gain>" % repr(gain_linear), block)
                return block.replace("\t\t<AudioChannelLayout>", "\t\t<Gain>%s</Gain>\n\t\t<AudioChannelLayout>" % repr(gain_linear), 1) if "<AudioChannelLayout>" in block else \
                    block.replace("\n\t</AudioClip>", "\n\t\t<Gain>%s</Gain>\n\t</AudioClip>" % repr(gain_linear))
            self._replace_object(oid, f)

    def save(self, path=None):
        text = self.text
        if self.new_objects:
            text = text.replace("\n</PremiereData>", "\n" + "\n".join(o.lstrip("\n") for o in self.new_objects) + "\n</PremiereData>")
        ET.fromstring(text)  # must still be well-formed
        with gzip.open(path or self.path, "wt", encoding="utf-8") as f:
            f.write(text)
