"""prproj_lib: change Premiere Pro .prproj projects by text surgery (verified on Premiere Pro 2026 / 26.5).

Why text surgery: a .prproj is gzip-compressed XML. Editing the text keeps every object you do not touch
byte-identical, so the user's project survives exactly as they left it. A parse tree is only used for lookups.

    import sys, os; sys.path.insert(0, os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts/prproj'))
    from prproj_lib import *
    doc = Doc.open(r'C:/proj/Show.prproj')            # read only; never edit the user's file in place
    seq = find_sequence(doc, 'Main edit')
    v1 = tracks(doc, seq, 'video')[0]
    for ti in clip_item_ids(doc, v1): print(item_info(doc, ti))
    doc.save(r'C:/proj/Show v2.prproj')                # refuses to overwrite the source; also writes .xml for diffing
    # then: python validate_struct.py "C:/proj/Show.prproj" "C:/proj/Show v2.prproj"

Time: 254016000000 ticks per second. Track item Start/End = sequence time. Clip InPoint/OutPoint and every
keyframe = media time of that clip. Premiere omits <Start> when it is 0.
Object ids: top-level elements carry ObjectID (int, referenced by ObjectRef) or ObjectUID (GUID, ObjectURef).
Premiere renumbers ObjectIDs on every save: find things by content (name, MatchName), never by a remembered id.
"""
import gzip, os, re, sys, uuid, json, base64, struct, ntpath, math
import xml.etree.ElementTree as ET

# Windows and macOS projects (Mac rules from the Mac port, verified there on Premiere 25.6 and 26.5 projects, 11 Oct 2026).
# Projects travel between a Windows PC and a Mac, so the project decides, not the machine this script runs on:
# - <RelativePath> form. Windows Premiere writes '.\sub\file.mp4'; Mac Premiere writes './sub/file.mp4' or '../x/file.mp4'
#   with '&' escaped twice (rel_path()). relink() and import_mp4() write the form of the PROJECT: path_style() reads the
#   project's own media <FilePath>s as it was opened (C:\... or \\server\... = 'win', /Users/... or /Volumes/... = 'mac').
#   Override per call with style='win' / 'mac', or for every project with prproj_lib.PATH_STYLE = 'win' / 'mac'.
#   A project with no media paths falls back to the machine. FilePath is always the real path on this machine (the
#   file must exist here), and Premiere looks there first.
# - a track's own <ID> comes BEFORE <Index> in Mac-saved projects and in most Windows ones too (134 of 220 project files
#   on the Windows PC on 14 Oct 2026; 86 had <Index> first). add_video_track() / add_audio_track() use _set_track_id(),
#   which finds the one numeric <ID> in the Track block in either order. The old regex understood only <Index> first:
#   add_video_track() stopped with "track template not understood" and add_audio_track() silently gave the new track
#   the template's ID (two tracks, one ID). On <Index>-first projects the result is byte-identical to the old code.
# - STRICT_CLONE: clone_item() refuses a clone that would start before its media begins (keep-sync mode moved it earlier
#   than the source allows) instead of writing a negative media in point. This one is a per-machine house default, not a
#   project format: on by default on macOS, off on Windows; set prproj_lib.STRICT_CLONE = True to use it everywhere.
STRICT_CLONE = sys.platform == 'darwin'
PATH_STYLE = None     # None = follow each project's own media paths; 'win' or 'mac' forces that <RelativePath> form

TPS = 254016000000
FRAME_TICKS = {23.976: 10594584000, 24: 10584000000, 25: 10160640000, 29.97: 8475667200, 30: 8467200000,
               50: 5080320000, 59.94: 4237833600, 60: 4233600000}
TIMECODE_FORMAT = {10594584000: 110, 10584000000: 100, 10160640000: 101, 8475667200: 103, 8467200000: 104, 4233600000: 108}
SAMPLE_48K = 5292000              # one 48 kHz audio sample (audio positions rounded to this load fine)
ADJ_IN = 914457600000000          # adjustment layers / synthetic graphics media start at 1 hour of media time
STATIC = -91445760000000000       # StartKeyframe time that means "not animated"


# ------------------------------------------------------------------ small helpers
def s2t(sec): return int(round(sec * TPS))
def t2s(t): return int(t) / TPS


def on_frame(sec, fps):
    """seconds -> ticks snapped to the frame grid of fps (use the SEQUENCE fps for Start/End)"""
    f = FRAME_TICKS.get(fps) or int(round(TPS / fps))
    return int(round(sec * TPS / f)) * f


def db_to_level(db): return 10 ** ((db - 15) / 20.0)        # audio "Level" param (0 dB = 0.1778, -24 dB = 0.01122)
def level_to_db(v): return 20 * math.log10(max(float(v), 1e-12)) + 15
def db_to_gain(db): return 10 ** (db / 20.0)                # AudioClip <Gain> (Audio Gain), FCP XML audio level


def fmt(v):
    s = ('%.6f' % float(v)).rstrip('0')
    return s if s != '-0.' else '0.'


def num(v):
    v = float(v)
    return repr(v) if v != int(v) else '%d.' % v


def kf_scalar(t, v, interp=0, infl=0.33333333333333331):
    """one scalar keyframe 't,v,interp,0,inSpeed,inInfl,outSpeed,outInfl;' (interp 0 linear, 5 bezier), t in media ticks"""
    return '%d,%s,%d,0,0,%r,0,%r;' % (t, num(v), interp, infl, infl)


def kf_audio(t, level):
    """audio Level keyframe exactly as Premiere writes them (influence 1/6)"""
    return '%d,%.12f,0,0,0,0.16666666666666666,0,0.16666666666666666;' % (t, level)


def kf_point(t, x, y, interp=0):
    """point keyframe (Position / Anchor, frame-normalized x:y)"""
    return '%d,%r:%r,%d,0,0,0.33333333333333331,0,0.33333333333333331,5,4,0,0,0,0;' % (t, float(x), float(y), interp)


def color64(r, g, b, a=255):
    """64-bit colour used by effect colour params such as Tint (A<<56 | R<<40 | G<<24 | B<<8)"""
    return str((a << 56) | (r << 40) | (g << 24) | (b << 8))


def esc(s): return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def _tag(obj_txt):
    """element name of an object's text (raw() keeps the leading tab)"""
    return re.match(r'\s*<(\w+)', obj_txt).group(1)


def unesc(s): return s.replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&apos;', "'").replace('&amp;', '&')


# ------------------------------------------------------------------ the document
class Doc:
    """The decompressed project text plus helpers to read/replace whole top-level objects."""

    def __init__(self, txt, path=None):
        if '\r\n' in txt: txt = txt.replace('\r\n', '\n')   # Premiere writes LF; CRLF copies come from text-mode dumps
        self.txt = txt
        self.path = path
        self.orig_txt = txt                 # kept for normalize_blobs() after deletions
        ids = [int(x) for x in re.findall(r'\n\t<\w+ ObjectID="(\d+)"', txt)]
        self.next_id = (max(ids) + 1) if ids else 1
        self._root, self._root_for = None, None

    @classmethod
    def open(cls, path):
        raw = open(path, 'rb').read()
        if raw[:2] == b'\x1f\x8b': raw = gzip.decompress(raw)
        return cls(raw.decode('utf-8'), path)

    @property
    def root(self):
        """parse tree of the CURRENT text (re-parsed after edits; ~1-2 s on a 20 MB project)"""
        if self._root_for is not self.txt:
            self._root, self._root_for = ET.fromstring(self.txt), self.txt
        return self._root

    def new_id(self):
        i = self.next_id; self.next_id += 1; return str(i)

    def span(self, key, uid=False):
        attr = 'ObjectUID' if uid else 'ObjectID'
        m = re.search(r'\n\t<(\w+) %s="%s"[ >]' % (attr, re.escape(str(key))), self.txt)
        if not m: raise KeyError(key)
        tag = m.group(1); start = m.start() + 1
        close = '\n\t</%s>' % tag
        end = self.txt.index(close, start) + len(close)
        return start, end

    def raw(self, key, uid=False):
        s, e = self.span(key, uid); return self.txt[s:e]

    def exists(self, key, uid=False):
        return re.search(r'\n\t<\w+ %s="%s"[ >]' % ('ObjectUID' if uid else 'ObjectID', re.escape(str(key))), self.txt) is not None

    def replace_obj(self, key, new_text, uid=False):
        s, e = self.span(key, uid); self.txt = self.txt[:s] + new_text + self.txt[e:]

    def delete_obj(self, key, uid=False):
        s, e = self.span(key, uid)
        if self.txt[s - 1] == '\n': s -= 1
        self.txt = self.txt[:s] + self.txt[e:]

    def append(self, objs):
        """add new top-level objects (texts) before </PremiereData>"""
        if isinstance(objs, str): objs = [objs]
        body = self.txt.rstrip()
        assert body.endswith('</PremiereData>')
        self.txt = body[:-len('</PremiereData>')].rstrip('\n') + '\n' + '\n'.join(o.strip('\n') for o in objs) + '\n</PremiereData>\n'

    def objects(self, tags, contains=None):
        """one pass over the text: [(tag, id_or_uid, is_uid, body)] for top-level objects whose tag is in tags"""
        if isinstance(tags, str): tags = (tags,)
        pat = re.compile(r'\n\t<(%s) Object(U?)ID="([^"]+)"[^>]*>.*?\n\t</\1>' % '|'.join(tags), re.S)
        out = []
        for m in pat.finditer(self.txt):
            body = m.group(0)
            if contains and contains not in body: continue
            out.append((m.group(1), m.group(3), m.group(2) == 'U', body[1:]))
        return out

    def save(self, out_path, keep_xml=True, force=False):
        if self.path and os.path.abspath(out_path).lower() == os.path.abspath(self.path).lower() and not force:
            raise ValueError('refusing to overwrite the source project; write a new versioned file')
        assert self.txt.rstrip().endswith('</PremiereData>')
        data = self.txt.encode('utf-8')
        with gzip.open(out_path, 'wb') as g: g.write(data)
        if keep_xml:
            with open(out_path + '.xml', 'wb') as f: f.write(data)
        return out_path


# ------------------------------------------------------------------ sequences and tracks
def sequences(doc):
    """[(name, sequence uid)]"""
    out = []
    for m in re.finditer(r'\n\t<Sequence ObjectUID="([^"]+)"', doc.txt):
        n = re.search(r'\n\t\t<Name>([^<]*)</Name>', doc.raw(m.group(1), uid=True))
        out.append((unesc(n.group(1)) if n else '', m.group(1)))
    return out


def find_sequence(doc, name):
    seqs = sequences(doc)
    hits = [u for n, u in seqs if n == name] or [u for n, u in seqs if name.lower() in n.lower()]
    if len(hits) != 1: raise KeyError('sequence %r: %d matches among %s' % (name, len(hits), [n for n, _ in seqs]))
    return hits[0]


def track_groups(doc, seq_uid):
    """{'VideoTrackGroup': id, 'AudioTrackGroup': id, 'DataTrackGroup': id}"""
    out = {}
    for gid in re.findall(r'<Second ObjectRef="(\d+)"', doc.raw(seq_uid, uid=True)):
        out[_tag(doc.raw(gid))] = gid
    return out


def tracks(doc, seq_uid, kind='video'):
    """track uids in index order (index 0 = V1 / A1). kind: video | audio | data (captions)"""
    tag = {'video': 'VideoTrackGroup', 'audio': 'AudioTrackGroup', 'data': 'DataTrackGroup'}[kind]
    gid = track_groups(doc, seq_uid).get(tag)
    if not gid: return []
    return [u for _, u in sorted((int(i), u) for i, u in re.findall(r'<Track Index="(\d+)" ObjectURef="([^"]+)"/>', doc.raw(gid)))]


def seq_frame_ticks(doc, seq_uid):
    g = track_groups(doc, seq_uid)['VideoTrackGroup']
    return int(re.search(r'<FrameRate>(\d+)</FrameRate>', doc.raw(g)).group(1))


def clip_item_ids(doc, track_uid):
    """clip items on a track (a track lists its transitions in a SECOND TrackItems block: never mix them up)"""
    m = re.search(r'<ClipItems Version="\d+">\s*<TrackItems Version="1">(.*?)</TrackItems>', doc.raw(track_uid, uid=True), re.S)
    return re.findall(r'<TrackItem Index="\d+" ObjectRef="(\d+)"/>', m.group(1)) if m else []


def transition_item_ids(doc, track_uid):
    m = re.search(r'<TransitionItems Version="\d+">\s*<TrackItems Version="1">(.*?)</TrackItems>', doc.raw(track_uid, uid=True), re.S)
    return re.findall(r'<TrackItem Index="\d+" ObjectRef="(\d+)"/>', m.group(1)) if m else []


def set_track_items(doc, track_uid, item_ids, sort=True):
    """replace the track's CLIP item list (transitions untouched). sort=True orders by start time."""
    if sort: item_ids = sorted(item_ids, key=lambda i: item_times(doc, i)[0])
    t = doc.raw(track_uid, uid=True)
    block = '<TrackItems Version="1">%s\n\t\t\t\t</TrackItems>' % ''.join(
        '\n\t\t\t\t\t<TrackItem Index="%d" ObjectRef="%s"/>' % (i, x) for i, x in enumerate(item_ids))
    if re.search(r'<ClipItems Version="\d+">\s*<TrackItems', t):
        t = re.sub(r'(<ClipItems Version="\d+">\s*)<TrackItems Version="1">.*?</TrackItems>', lambda m: m.group(1) + block, t, count=1, flags=re.S)
    else:
        t, n = re.subn(r'(<ClipItems Version="\d+">\s*)(<MediaType>)', lambda m: m.group(1) + block + '\n\t\t\t\t' + m.group(2), t, count=1)
        assert n == 1, 'could not hook the item list into the track'
    doc.replace_obj(track_uid, t, uid=True)


def add_to_track(doc, track_uid, new_ids):
    set_track_items(doc, track_uid, clip_item_ids(doc, track_uid) + list(new_ids))


def remove_from_track(doc, track_uid, ids):
    keep = [i for i in clip_item_ids(doc, track_uid) if i not in set(ids)]
    if keep: set_track_items(doc, track_uid, keep)
    else:
        t = doc.raw(track_uid, uid=True)
        t = re.sub(r'(<ClipItems Version="\d+">)\s*<TrackItems Version="1">.*?</TrackItems>\s*', r'\1\n\t\t\t\t', t, count=1, flags=re.S)
        doc.replace_obj(track_uid, t, uid=True)


# ------------------------------------------------------------------ track items
def item_times(doc, ti):
    t = doc.raw(ti)
    s = re.search(r'<Start>(-?\d+)</Start>', t)
    return (int(s.group(1)) if s else 0), int(re.search(r'<End>(-?\d+)</End>', t).group(1))


def item_info(doc, ti):
    """dict: id, tag, start, end (ticks), muted, subclip, chain, clip, master, name, inpoint, outpoint, speed,
    source_tag, media (uid), title, path, nested_seq"""
    t = doc.raw(ti)
    s, e = item_times(doc, ti)
    info = dict(id=ti, tag=_tag(t), start=s, end=e, muted='<IsMuted>true</IsMuted>' in t)
    sc = re.search(r'<SubClip ObjectRef="(\d+)"', t); ch = re.search(r'<Components ObjectRef="(\d+)"', t)
    info['subclip'] = sc.group(1) if sc else None
    info['chain'] = ch.group(1) if ch else None
    if not sc: return info
    st = doc.raw(sc.group(1))
    info['clip'] = re.search(r'<Clip ObjectRef="(\d+)"', st).group(1)
    mc = re.search(r'<MasterClip ObjectURef="([^"]+)"', st); info['master'] = mc.group(1) if mc else None
    nm = re.search(r'<Name>([^<]*)</Name>', st); info['name'] = unesc(nm.group(1)) if nm else None
    ct = doc.raw(info['clip'])
    i = re.search(r'<InPoint>(-?\d+)</InPoint>', ct); o = re.search(r'<OutPoint>(-?\d+)</OutPoint>', ct)
    sp = re.search(r'<PlaybackSpeed>([^<]+)</PlaybackSpeed>', ct)
    info.update(inpoint=int(i.group(1)) if i else 0, outpoint=int(o.group(1)) if o else None, speed=float(sp.group(1)) if sp else 1.0)
    src = re.search(r'<Source ObjectRef="(\d+)"', ct)
    if src:
        srt = doc.raw(src.group(1)); info['source_tag'] = _tag(srt)
        med = re.search(r'<Media ObjectURef="([^"]+)"', srt)
        if med:
            info['media'] = med.group(1); mt = doc.raw(med.group(1), uid=True)
            fp = re.search(r'<FilePath>([^<]*)</FilePath>', mt); ttl = re.search(r'<Title>([^<]*)</Title>', mt)
            info['path'] = unesc(fp.group(1)) if fp else None; info['title'] = unesc(ttl.group(1)) if ttl else None
        sq = re.search(r'<Sequence ObjectURef="([^"]+)"', srt)
        if sq: info['nested_seq'] = sq.group(1)
    return info


def items_at(doc, track_uid, sec, name_part=None):
    """clip items on a track that cover sequence time sec (optionally whose clip name contains name_part)"""
    t = s2t(sec); out = []
    for ti in clip_item_ids(doc, track_uid):
        s, e = item_times(doc, ti)
        if s <= t < e and (name_part is None or name_part.lower() in (item_info(doc, ti).get('name') or '').lower()): out.append(ti)
    return out


def set_times(ti_txt, start, end):
    """set Start/End in a track item's text, keeping Premiere's element order (Node, Start, End); Start 0 = omitted"""
    ti_txt = re.sub(r'<End>-?\d+</End>', '<End>%d</End>' % end, ti_txt)
    if re.search(r'<Start>-?\d+</Start>', ti_txt):
        if start: ti_txt = re.sub(r'<Start>-?\d+</Start>', '<Start>%d</Start>' % start, ti_txt)
        else: ti_txt = re.sub(r'\n\t*<Start>-?\d+</Start>', '', ti_txt)
    elif start:
        ti_txt = re.sub(r'(\n\t*)(<End>-?\d+</End>)', lambda m: '%s<Start>%d</Start>%s%s' % (m.group(1), start, m.group(1), m.group(2)), ti_txt, count=1)
    return ti_txt


def set_inout(clip_txt, tin, tout):
    clip_txt = re.sub(r'<InPoint>-?\d+</InPoint>', '<InPoint>%d</InPoint>' % tin, clip_txt)
    return re.sub(r'<OutPoint>-?\d+</OutPoint>', '<OutPoint>%d</OutPoint>' % tout, clip_txt)


def retime_item(doc, ti, start, end):
    """move/trim an item; the media under its first frame shifts with the new start (like a slip-free trim)"""
    inf = item_info(doc, ti)
    tin = inf['inpoint'] + int(round((start - inf['start']) * inf['speed']))
    doc.replace_obj(ti, set_times(doc.raw(ti), start, end))
    doc.replace_obj(inf['clip'], set_inout(doc.raw(inf['clip']), tin, tin + int(round((end - start) * inf['speed']))))


def set_item_end(doc, ti, end):
    """extend or trim the tail of an item (media in point unchanged). Needs enough media after the out point."""
    inf = item_info(doc, ti)
    retime_item(doc, ti, inf['start'], end)


def disable_item(doc, ti):
    """the 'disable, never delete' rule: IsMuted true right after the SubClip ref (works on caption items too)"""
    t = doc.raw(ti)
    if '<IsMuted>true</IsMuted>' in t: return False
    if '<IsMuted>false</IsMuted>' in t: t2 = t.replace('<IsMuted>false</IsMuted>', '<IsMuted>true</IsMuted>', 1)
    else: t2 = re.sub(r'(\n(\t+)<SubClip ObjectRef="\d+"/>)', lambda m: m.group(1) + '\n' + m.group(2) + '<IsMuted>true</IsMuted>', t, count=1)
    assert t2 != t, 'no SubClip ref to anchor IsMuted'
    doc.replace_obj(ti, t2); return True


def enable_item(doc, ti):
    t = doc.raw(ti); t2 = re.sub(r'\n\t*<IsMuted>true</IsMuted>', '', t)
    doc.replace_obj(ti, t2); return t2 != t


# ------------------------------------------------------------------ effects (components) and params
def chain_components(doc, chain_id):
    return re.findall(r'<Component Index="\d+" ObjectRef="(\d+)"\s*/>', doc.raw(chain_id))


def components(doc, ti):
    """[(component id, MatchName, DisplayName)] of a track item's effects, in chain order"""
    ch = item_info(doc, ti)['chain']
    out = []
    for c in chain_components(doc, ch) if ch else []:
        t = doc.raw(c)
        mn = re.search(r'<MatchName>([^<]*)</MatchName>', t); dn = re.search(r'<DisplayName>([^<]*)</DisplayName>', t)
        out.append((c, mn.group(1) if mn else '', unesc(dn.group(1)) if dn else ''))
    return out


def find_component(doc, ti, matchname=None, display=None):
    hits = [c for c, mn, dn in components(doc, ti) if (matchname is None or mn == matchname) and (display is None or dn == display)]
    return hits[0] if hits else None


def params(doc, comp_id):
    """[(param id, index, Name, ParameterID)]"""
    out = []
    for idx, pid in re.findall(r'<Param Index="(\d+)" ObjectRef="(\d+)"\s*/>', doc.raw(comp_id)):
        t = doc.raw(pid)
        n = re.search(r'<Name>([^<]*)</Name>', t); p = re.search(r'<ParameterID>(\d+)</ParameterID>', t)
        out.append((pid, int(idx), unesc(n.group(1)) if n else '', int(p.group(1)) if p else None))
    return out


def param_id(doc, comp_id, key):
    """key = param Name (str) or Index (int)"""
    for pid, idx, name, _ in params(doc, comp_id):
        if (isinstance(key, int) and idx == key) or name == key: return pid
    raise KeyError('param %r not in component %s (%s)' % (key, comp_id, [n for _, _, n, _ in params(doc, comp_id)]))


def get_value(doc, pid):
    """static value string of a param (StartKeyframe). <CurrentValue> is a stale UI cache: ignore it."""
    m = re.search(r'<StartKeyframe>(-?\d+),([^,<]*)', doc.raw(pid))
    return m.group(2) if m else None


def set_value(doc, pid, value):
    t = doc.raw(pid)
    m = re.search(r'<StartKeyframe>(-?\d+),([^,<]*)', t)
    assert m, 'param %s has no StartKeyframe (blob param?)' % pid
    v = value if isinstance(value, str) else fmt(value)
    t = t[:m.start(2)] + v + t[m.end(2):]
    doc.replace_obj(pid, re.sub(r'\n\t*<CurrentValue>[^<]*</CurrentValue>', '', t))


def set_keys(doc, pid, keys):
    """replace a param's keyframes with a string of kf_scalar/kf_point/kf_audio entries (media time).
    Video params get <IsTimeVarying>true; audio params do not carry that flag (Premiere never writes it there)."""
    t = doc.raw(pid)
    t = re.sub(r'\n\t*<Keyframes>[^<]*</Keyframes>', '', t)
    if not _tag(t).startswith('Audio'):
        if '<IsTimeVarying>' in t: t = re.sub(r'<IsTimeVarying>[^<]*</IsTimeVarying>', '<IsTimeVarying>true</IsTimeVarying>', t)
        else: t = t.replace('\n\t\t<StartKeyframe>', '\n\t\t<IsTimeVarying>true</IsTimeVarying>\n\t\t<StartKeyframe>', 1)
    t = re.sub(r'(<StartKeyframe>[^<]*</StartKeyframe>)', lambda m: m.group(1) + '\n\t\t<Keyframes>%s</Keyframes>' % keys, t, count=1)
    doc.replace_obj(pid, t)


def clear_keys(doc, pid):
    t = doc.raw(pid)
    t = re.sub(r'\n\t*<Keyframes>[^<]*</Keyframes>', '', t).replace('<IsTimeVarying>true</IsTimeVarying>', '<IsTimeVarying>false</IsTimeVarying>')
    doc.replace_obj(pid, t)


def media_time(doc, ti, seq_sec):
    """sequence seconds -> media ticks of that item (keyframes live in media time)"""
    inf = item_info(doc, ti)
    return inf['inpoint'] + int(round((s2t(seq_sec) - inf['start']) * inf['speed']))


INLINE = re.compile(r'(<(StartKeyframeValue|PremiereFilterPrivateData)( [^>]*?BinaryHash="[^"]+"))>[^<]+</\2>')


def strip_inline(txt):
    """clones must only REFERENCE blob data (the original keeps the single inline copy, at the first BinaryHash)"""
    return INLINE.sub(r'\1/>', txt)


def clone_component(doc, comp_id, overrides=None, strip_keys=False):
    """deep copy of an effect component with its params and sub-components (masks).
    overrides: {param Name or Index: value (number or raw string such as '0.5:0.5')}.
    strip_keys=True drops template animation from params you do not override (presets from other projects carry keys)."""
    overrides = overrides or {}
    comp = doc.raw(comp_id); new = doc.new_id(); out = []
    for idx, pid in re.findall(r'<Param Index="(\d+)" ObjectRef="(\d+)"\s*/>', comp):
        nid = doc.new_id()
        p = strip_inline(doc.raw(pid).replace('ObjectID="%s"' % pid, 'ObjectID="%s"' % nid, 1))
        p = re.sub(r'\n\t*<CurrentValue>[^<]*</CurrentValue>', '', p)
        nm = re.search(r'<Name>([^<]*)</Name>', p); nm = unesc(nm.group(1)) if nm else None
        key = int(idx) if int(idx) in overrides else nm if nm in overrides else None
        if key is not None:
            m = re.search(r'<StartKeyframe>(-?\d+),([^,]+),', p)
            val = overrides[key]
            p = p[:m.start(2)] + (val if isinstance(val, str) else fmt(val)) + p[m.end(2):]
        if strip_keys or key is not None:
            p = re.sub(r'\n\t*<Keyframes>[^<]*</Keyframes>', '', p).replace('<IsTimeVarying>true</IsTimeVarying>', '<IsTimeVarying>false</IsTimeVarying>')
        comp = re.sub(r'(<Param Index="%s" ObjectRef=")%s("\s*/>)' % (idx, pid), r'\g<1>%s\g<2>' % nid, comp)
        out.append(p)
    for idx, sid in re.findall(r'<SubComponent Index="(\d+)" ObjectRef="(\d+)"\s*/>', comp):
        nsid, sub = clone_component(doc, sid, strip_keys=strip_keys)
        comp = re.sub(r'(<SubComponent Index="%s" ObjectRef=")%s("\s*/>)' % (idx, sid), r'\g<1>%s\g<2>' % nsid, comp)
        out += sub
    comp = strip_inline(comp.replace('ObjectID="%s"' % comp_id, 'ObjectID="%s"' % new, 1))
    return new, [comp] + out


def clone_chain(doc, chain_id, comp_ids):
    """new component chain object listing the given (already cloned) component ids"""
    new = doc.new_id()
    c = doc.raw(chain_id).replace('ObjectID="%s"' % chain_id, 'ObjectID="%s"' % new, 1)
    items = ''.join('\n\t\t\t\t<Component Index="%d" ObjectRef="%s"/>' % (i, cid) for i, cid in enumerate(comp_ids))
    if re.search(r'<Components Version="1">.*?</Components>', c, re.S):
        c = re.sub(r'<Components Version="1">.*?</Components>', '<Components Version="1">%s\n\t\t\t</Components>' % items, c, count=1, flags=re.S)
    else:
        assert not comp_ids, 'template chain has no Components block to fill'
    return new, c


# ------------------------------------------------------------------ cloning and placing items
_NODE_NEXT = {}


def _fresh_item(doc, titxt):
    """a cloned track item must not keep the template's identity:
    - <HeadTransition>/<TailTransition> refs point at the TEMPLATE's transitions (verified 7 Oct 2026: a clone that kept
      HeadTransition was drawn at the template's time, never at its own)
    - the <Node><ID> number must be unique in the project"""
    titxt = re.sub(r'\n\t*<(?:Head|Tail)Transition ObjectRef="\d+"/>', '', titxt)
    key = id(doc)
    if key not in _NODE_NEXT:
        ids = [int(x) for x in re.findall(r'<Node Version="1">\s*(?:<Properties Version="1">.*?</Properties>\s*)?<ID>(\d+)</ID>', doc.txt, re.S)]
        _NODE_NEXT[key] = max(ids + [3000000]) + 1
    n = _NODE_NEXT[key]; _NODE_NEXT[key] += 1
    return re.sub(r'(<TrackItem Version="\d+">\s*<Node Version="1">\s*(?:<Properties Version="1">.*?</Properties>\s*)?<ID>)\d+(</ID>)',
                  lambda m: '%s%d%s' % (m.group(1), n, m.group(2)), titxt, count=1, flags=re.S)


MOTION_DEFAULTS = {'Position': '0.5:0.5', 'Scale': '100.', 'Scale Width': '100.', 'Rotation': '0.', 'Anchor Point': '0.5:0.5',
                   'Anti-flicker Filter': '0.', 'Crop Left': '0.', 'Crop Top': '0.', 'Crop Right': '0.', 'Crop Bottom': '0.'}


def clone_item(doc, ti, start, end, overrides_by_comp=None, src_in=None):
    """deep clone of a track item (chain, components incl. masks and keyframes, clip instance) at a new time.
    src_in=None keeps the sync offset (media time moves with the item, right for adjustment layers and for
    copying a piece of the same take in sync); pass src_in (ticks) to choose the media in point instead.
    Returns (new item id, object texts): doc.append(texts) then add_to_track(doc, track, [id])."""
    overrides_by_comp = overrides_by_comp or {}
    inf = item_info(doc, ti)
    off = inf['inpoint'] - inf['start'] if src_in is None else src_in - start
    if STRICT_CLONE and start + off < 0:
        raise ValueError('clone would start %.2f s before its media begins (keep-sync mode moved it earlier than its source '
                         'allows): pass src_in=s2t(seconds) to pick the media in point' % ((start + off) / TPS))
    objs, comp_ids = [], []
    for i, cid in enumerate(chain_components(doc, inf['chain'])):
        ncid, texts = clone_component(doc, cid, overrides_by_comp.get(i)); comp_ids.append(ncid); objs += texts
    nch, chtxt = clone_chain(doc, inf['chain'], comp_ids)
    nvc, nsc, nti = doc.new_id(), doc.new_id(), doc.new_id()
    vc = inf['clip']
    vctxt = set_inout(strip_inline(doc.raw(vc).replace('ObjectID="%s"' % vc, 'ObjectID="%s"' % nvc, 1)), start + off, end + off)
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, doc.raw(inf['subclip']).replace('ObjectID="%s"' % inf['subclip'], 'ObjectID="%s"' % nsc, 1))
    titxt = doc.raw(ti).replace('ObjectID="%s"' % ti, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    return nti, objs + [chtxt, vctxt, sctxt, set_times(_fresh_item(doc, titxt), start, end)]


def master_by_name(doc, name):
    """an existing project item (bin clip) by its bin name -> dict(cpi_uid, mc_uid, clips=[clip ids], name)"""
    for kind, key, is_uid, body in doc.objects('ClipProjectItem'):
        n = re.search(r'<Name>([^<]*)</Name>', body)
        if n and unesc(n.group(1)) == name:
            mc = re.search(r'<MasterClip ObjectURef="([^"]+)"', body).group(1)
            clips = re.findall(r'<Clip Index="\d+" ObjectRef="(\d+)"', doc.raw(mc, uid=True))
            return dict(cpi_uid=key, mc_uid=mc, clips=clips, name=name)
    raise KeyError('no project item named %r' % name)


def place_video_item(doc, tmpl_ti, master, start, end, src_in=0, keep=('AE.ADBE Motion',), overrides=None, reset_motion=True):
    """new video clip built on an existing item's structure, playing another master clip.
    master: dict from master_by_name() or import_mp4(); its clips[0] must be the master's VideoClip.
    keep: MatchNames of the template's components to copy ('all' = every component), template keys stripped.
    overrides: {MatchName: {param: value}}, e.g. {'AE.ADBE Motion': {'Position': '0.5:0.4', 'Scale': 120}}
    (Motion Position / Anchor are frame-normalized 'x:y'; Effect Controls shows them in pixels).
    reset_motion: the template's own Motion values (position, scale, CROPS...) are reset to defaults first, so only
    your overrides apply. Pick a template item that HAS a Motion component (Premiere drops an all-default Motion on save)."""
    asked = dict(overrides or {})
    overrides = dict(asked)
    if reset_motion:
        mo = dict(MOTION_DEFAULTS); mo.update(asked.get('AE.ADBE Motion', {})); overrides['AE.ADBE Motion'] = mo
    t = doc.raw(tmpl_ti)
    sc_id = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1); ch_id = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    objs, comp_ids, seen = [], [], set()
    for c in chain_components(doc, ch_id):
        mn = re.search(r'<MatchName>([^<]*)</MatchName>', doc.raw(c)).group(1)
        if keep != 'all' and mn not in keep: continue
        names = [p[2] for p in params(doc, c)]
        ov = {k: v for k, v in (overrides.get(mn) or {}).items() if k in names or isinstance(k, int)}
        nc, texts = clone_component(doc, c, ov, strip_keys=True); comp_ids.append(nc); objs += texts; seen.add(mn)
    missing = [mn for mn in asked if mn not in seen]
    assert not missing, 'template item has no %s component to override: pick one that has it' % missing
    nch, chtxt = clone_chain(doc, ch_id, comp_ids)
    mvc = master['clips'][0]
    nvc, nsc, nti = doc.new_id(), doc.new_id(), doc.new_id()
    vctxt = strip_inline(doc.raw(mvc).replace('ObjectID="%s"' % mvc, 'ObjectID="%s"' % nvc, 1))
    vctxt = re.sub(r'\n\t*<InUse>[^<]*</InUse>', '', vctxt)
    vctxt = re.sub(r'\n\t*<(?:In|Out)Point>-?\d+</(?:In|Out)Point>', '', vctxt)
    vctxt = re.sub(r'(<Source ObjectRef="\d+"/>)', r'\1\n\t\t\t<OutPoint>%d</OutPoint>\n\t\t\t<InPoint>%d</InPoint>' % (src_in + (end - start), src_in), vctxt, count=1)
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sctxt = doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, sctxt)
    sctxt = re.sub(r'(<MasterClip ObjectURef=")[^"]+(")', r'\g<1>%s\g<2>' % master['mc_uid'], sctxt)
    sctxt = re.sub(r'<Name>[^<]*</Name>', lambda m: '<Name>%s</Name>' % esc(master['name']), sctxt, count=1)
    titxt = t.replace('ObjectID="%s"' % tmpl_ti, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    titxt = re.sub(r'\n\t*<IsMuted>[^<]*</IsMuted>', '', titxt)
    return nti, objs + [chtxt, vctxt, sctxt, set_times(_fresh_item(doc, titxt), start, end)]


DEFAULT_AUDIO_CHAIN = ('\t<AudioComponentChain ObjectID="0" ClassID="3cb131d1-d3c0-47ae-a19a-bdf75ea11674" Version="4">\n'
                       '\t\t<DefaultVol>true</DefaultVol>\n\t\t<DefaultVolumeComponentID>1</DefaultVolumeComponentID>\n'
                       '\t\t<DefaultChannelVolumeComponentID>2</DefaultChannelVolumeComponentID>\n\t\t<ComponentChain Version="3">\n'
                       '\t\t\t<Node Version="1">\n\t\t\t\t<Properties Version="1">\n'
                       '\t\t\t\t\t<MZ.ComponentChain.ActiveComponentID>1</MZ.ComponentChain.ActiveComponentID>\n'
                       '\t\t\t\t\t<MZ.ComponentChain.ActiveComponentParamIndex>4294967295</MZ.ComponentChain.ActiveComponentParamIndex>\n'
                       '\t\t\t\t</Properties>\n\t\t\t</Node>\n\t\t</ComponentChain>\n'
                       '\t\t<AudioChannelLayout>%s</AudioChannelLayout>\n\t\t<ChannelType>1</ChannelType>\n\t</AudioComponentChain>')


def _default_audio_chain(doc, prefer, layout):
    """text of an item-level AudioComponentChain with DefaultVol and no effects, for a new audio clip.
    A chain that holds a Volume component must not be cloned (its components would be shared): use the project's
    own default chain if there is one, else the exact structure Premiere 26.5 writes (DEFAULT_AUDIO_CHAIN)."""
    def ok(cid):
        t = doc.raw(cid)
        return '<DefaultVol>true</DefaultVol>' in t and '<Component Index' not in t
    if ok(prefer): return doc.raw(prefer)
    for _, k, _, b in doc.objects('AudioClipTrackItem'):
        c = re.search(r'<Components ObjectRef="(\d+)"', b)
        if c and ok(c.group(1)): return doc.raw(c.group(1))
    return DEFAULT_AUDIO_CHAIN % layout


def place_audio_item(doc, tmpl_ti, master, start, end, src_in=0, gain_db=0.0, clip_index=None):
    """new audio clip (SFX / music) cloned from an existing AudioClipTrackItem (e.g. any A1 item).
    master: dict from master_by_name(); uses its AudioClip (last clip of the master unless clip_index given).
    Level is set with the clip's Audio Gain (<Gain>), no Volume component (DefaultVol). Positions snap to 48 kHz."""
    snap = lambda x: int(round(x / SAMPLE_48K)) * SAMPLE_48K
    start, end, src_in = snap(start), snap(end), snap(src_in)
    mclip = master['clips'][clip_index if clip_index is not None else -1]
    m = doc.raw(mclip); assert _tag(m) == 'AudioClip', 'master clip %s is not an AudioClip' % mclip
    new_objs = []
    ncl = doc.new_id()
    t = re.sub(r'(<AudioClip ObjectID=")\d+(")', r'\g<1>%s\2' % ncl, strip_inline(m), count=1)
    t = re.sub(r'\n\t*<InUse>[^<]*</InUse>', '', t)
    t = re.sub(r'\n\t*<(?:In|Out)Point>-?\d+</(?:In|Out)Point>', '', t)
    t = re.sub(r'<ClipID>[^<]*</ClipID>', '<OutPoint>%d</OutPoint>\n\t\t\t<InPoint>%d</InPoint>\n\t\t\t<ClipID>%s</ClipID>' % (src_in + end - start, src_in, uuid.uuid4()), t, count=1)

    def sc(mo):
        sid = doc.new_id()
        new_objs.append(re.sub(r'(<SecondaryContent ObjectID=")\d+(")', r'\g<1>%s\2' % sid, doc.raw(mo.group(2)), count=1))
        return '%sObjectRef="%s"/>' % (mo.group(1), sid)
    t = re.sub(r'(<SecondaryContentItem Index="\d+" )ObjectRef="(\d+)"/>', sc, t)
    t = re.sub(r'\n\t*<Gain>[^<]*</Gain>', '', t)
    t, n = re.subn(r'(</AudioChannelLayout>)(\n\t</AudioClip>)', lambda mo: mo.group(1) + '\n\t\t<Gain>%r</Gain>' % db_to_gain(gain_db) + mo.group(2), t, count=1)
    assert n == 1, 'gain not inserted'
    new_objs.append(t)
    tt = doc.raw(tmpl_ti); assert _tag(tt) == 'AudioClipTrackItem', 'template must be an AudioClipTrackItem'
    lay = re.search(r'<AudioChannelLayout>([^<]*)</AudioChannelLayout>', m)
    chain_txt = _default_audio_chain(doc, re.search(r'<Components ObjectRef="(\d+)"', tt).group(1),
                                     lay.group(1) if lay else '[{"channellabel":100},{"channellabel":101}]')
    nch = doc.new_id()
    new_objs.append(re.sub(r'(<AudioComponentChain ObjectID=")\d+(")', r'\g<1>%s\2' % nch, chain_txt, count=1))
    nsub = doc.new_id()
    new_objs.append('\t<SubClip ObjectID="%s" ClassID="e0c58dc9-dbdd-4166-aef7-5db7e3f22e84" Version="6">\n\t\t<Clip ObjectRef="%s"/>\n'
                    '\t\t<MasterClip ObjectURef="%s"/>\n\t\t<Name>%s</Name>\n\t\t<OrigChGrp>0</OrigChGrp>\n\t</SubClip>' % (nsub, ncl, master['mc_uid'], esc(master['name'])))
    nti = doc.new_id()
    tt = re.sub(r'(<AudioClipTrackItem ObjectID=")\d+(")', r'\g<1>%s\2' % nti, tt, count=1)
    tt = re.sub(r'<Components ObjectRef="\d+"/>', '<Components ObjectRef="%s"/>' % nch, tt, count=1)
    tt = re.sub(r'<SubClip ObjectRef="\d+"/>', '<SubClip ObjectRef="%s"/>' % nsub, tt, count=1)
    tt = re.sub(r'<Properties Version="1">.*?</Properties>', '<Properties Version="1">\n\t\t\t\t\t</Properties>', tt, count=1, flags=re.S)
    tt = re.sub(r'(</ClipTrackItem>\s*<ID>)[^<]*(</ID>)', r'\g<1>%s\2' % uuid.uuid4(), tt, count=1)
    tt = re.sub(r'\n\t*<IsMuted>[^<]*</IsMuted>', '', tt)
    new_objs.append(set_times(_fresh_item(doc, tt), start, end))
    return nti, new_objs


def set_clip_gain(doc, ti, db):
    """absolute Audio Gain of an audio item's clip instance (shows as 'Gain' in Premiere)"""
    cid = item_info(doc, ti)['clip']; ct = doc.raw(cid)
    if '<Gain>' in ct: ct2 = re.sub(r'<Gain>[^<]*</Gain>', '<Gain>%r</Gain>' % db_to_gain(db), ct, count=1)
    else: ct2 = re.sub(r'(</AudioChannelLayout>)(\n\t</AudioClip>)', lambda m: m.group(1) + '\n\t\t<Gain>%r</Gain>' % db_to_gain(db) + m.group(2), ct, count=1)
    assert ct2 != ct or '<Gain>%r</Gain>' % db_to_gain(db) in ct
    doc.replace_obj(cid, ct2)


def level_param(doc, ti):
    """the 'Level' param of an audio item's Volume effect (exists once a volume was set on that clip in Premiere)"""
    for c, mn, dn in components(doc, ti):
        for pid, idx, name, _ in params(doc, c):
            if name == 'Level': return pid
    raise KeyError('item %s has no Volume Level param (DefaultVol): set a level on it in Premiere once, or use set_clip_gain' % ti)


def set_level_keys(doc, ti, points):
    """volume automation: points = [(sequence seconds, dB), ...] -> Level keyframes in the clip's media time"""
    pid = level_param(doc, ti)
    set_keys(doc, pid, ''.join(kf_audio(media_time(doc, ti, s), db_to_level(db)) for s, db in points))


# ------------------------------------------------------------------ media: find, relink, import
def media_list(doc):
    """[(media uid, Title, FilePath)]"""
    out = []
    for kind, key, is_uid, body in doc.objects('Media'):
        fp = re.search(r'<FilePath>([^<]*)</FilePath>', body); ttl = re.search(r'<Title>([^<]*)</Title>', body)
        out.append((key, unesc(ttl.group(1)) if ttl else '', unesc(fp.group(1)) if fp else ''))
    return out


def find_media(doc, name):
    """media uids whose Title or file name equals name"""
    return [u for u, ttl, fp in media_list(doc) if name in (ttl, ntpath.basename(fp))]


def items_for_media(doc, media_uid):
    srcs = [k for _, k, _, b in doc.objects(('VideoMediaSource', 'AudioMediaSource'), 'ObjectURef="%s"' % media_uid)]
    clips = [k for _, k, _, b in doc.objects(('VideoClip', 'AudioClip')) if any('<Source ObjectRef="%s"/>' % s in b for s in srcs)]
    subs = [k for _, k, _, b in doc.objects('SubClip') if any('<Clip ObjectRef="%s"/>' % c in b for c in clips)]
    return [k for _, k, _, b in doc.objects(('VideoClipTrackItem', 'AudioClipTrackItem')) if any('<SubClip ObjectRef="%s"/>' % s in b for s in subs)]


def media_duration_ticks(path, frame_ticks=None, kind='video'):
    """exact duration with PyAV: video = frame count x frame ticks; audio = samples / rate"""
    import av
    c = av.open(path)
    try:
        if kind == 'video' and c.streams.video:
            v = c.streams.video[0]
            n = v.frames or sum(1 for _ in c.decode(v))
            ft = frame_ticks or int(round(TPS / float(v.average_rate)))
            return n * ft
        if path.lower().endswith('.wav'):
            import wave
            with wave.open(path) as w: return int(round(w.getnframes() / w.getframerate() * TPS))
        a = c.streams.audio[0]
        if a.duration: return int(round(float(a.duration * a.time_base) * TPS))
        return int(round(float(c.duration) / 1e6 * TPS))
    finally:
        c.close()


def relink(doc, old_name, new_path, project_dir, rename=True, log=print, style=None):
    """point the media titled old_name (Title or file name) at new_path, keeping every edit on its clips.
    project_dir = folder of the .prproj you will save (for RelativePath). Updates FileKey, mod time, stream durations
    (when they changed by > 0.02 s), drops the old peak files and renames the clip names that equal the old name.
    style: None = the project's own path form (path_style), or 'win' / 'mac' to force the <RelativePath> form."""
    new_abs = os.path.abspath(new_path); assert os.path.exists(new_abs), new_abs
    uids = find_media(doc, old_name); assert len(uids) == 1, (old_name, len(uids))
    uid = uids[0]; t = doc.raw(uid, uid=True)
    old_title = unesc(re.search(r'<Title>([^<]*)</Title>', t).group(1))
    new_name = os.path.basename(new_abs)
    for tag in ('FilePath', 'ActualMediaFilePath'):
        t = re.sub(r'<%s>[^<]*</%s>' % (tag, tag), lambda m: '<%s>%s</%s>' % (tag, esc(new_abs), tag), t)
    if path_style(doc, style) == 'mac':
        rel_x = rel_path(new_abs, project_dir)      # macOS form, already escaped
    else:
        try:
            rel = '.\\' + os.path.relpath(new_abs, project_dir).replace('/', '\\')
        except ValueError:
            rel = new_abs                      # other drive
        rel_x = esc(rel)
    t = re.sub(r'<RelativePath>[^<]*</RelativePath>', lambda m: '<RelativePath>%s</RelativePath>' % rel_x, t)
    t = re.sub(r'<Title>[^<]*</Title>', lambda m: '<Title>%s</Title>' % esc(new_name), t, count=1)
    t = re.sub(r'<FileKey>[^<]+</FileKey>', '<FileKey>%s</FileKey>' % uuid.uuid4(), t)
    t = re.sub(r'<CCFileModTime>\d+</CCFileModTime>', '<CCFileModTime>%d</CCFileModTime>' % int(os.path.getmtime(new_abs) * 1e6), t)
    t = re.sub(r'\s*<ModificationState [^>]*>[^<]*</ModificationState>', '', t)
    t = re.sub(r'\s*<ModificationState [^>]*/>', '', t)
    t = re.sub(r'\s*<ContentAndMetadataState>[^<]*</ContentAndMetadataState>', '', t)
    doc.replace_obj(uid, t, uid=True)
    durs = []
    for kind, sref in re.findall(r'<(Video|Audio)Stream ObjectRef="(\d+)"', t):
        st = doc.raw(sref)
        old = re.search(r'<Duration>(\d+)</Duration>', st)
        fr = re.search(r'<FrameRate>(\d+)</FrameRate>', st)
        new = media_duration_ticks(new_abs, int(fr.group(1)) if (fr and kind == 'Video') else None, kind.lower())
        if old and abs(new - int(old.group(1))) > TPS * 0.02:
            st = re.sub(r'<Duration>\d+</Duration>', '<Duration>%d</Duration>' % new, st)
        st = re.sub(r'\s*<(ConformedAudioPath|PeakFilePath)>[^<]*</\1>', '', st)
        doc.replace_obj(sref, st)
        durs.append((kind, int(old.group(1)) / TPS if old else None, new / TPS))
    n = 0
    if rename and old_title != new_name:
        n = doc.txt.count('<Name>%s</Name>' % esc(old_title))
        doc.txt = doc.txt.replace('<Name>%s</Name>' % esc(old_title), '<Name>%s</Name>' % esc(new_name))
    if log: log('relink %-30s -> %-30s %s names %d' % (old_title, new_name, ' '.join('%s %.3f->%.3f s' % d for d in durs), n))
    return dict(media=uid, durations=durs, renamed=n)


def rel_path(path, project_dir):
    """<RelativePath> text as Premiere on macOS writes it: './sub/file.mp4' at or below the project folder, '../x/file.mp4'
    above it (seen in 25.6 and 26.5 projects, 11 Oct 2026). Premiere double-escapes '&' here ('&amp;amp;'), so the
    result is escaped twice to match. Used for Mac-style projects (path_style); Windows Premiere writes '.\\file'."""
    try: r = os.path.relpath(path, project_dir).replace('\\', '/')     # '/' also when a Mac project is edited on Windows
    except ValueError: return esc(path)
    return esc(esc(r if r.startswith('..') else './' + r))


_WIN_PATH = re.compile(r'[A-Za-z]:[\\/]|\\\\')        # C:\... C:/... and \\server\share or \\?\C:\... (Premiere previews)


def path_style(doc, style=None):
    """'win' or 'mac': the <RelativePath> form that relink() / import_mp4() write into this project.
    Order: the style argument, then the module setting PATH_STYLE, then the project itself (the majority form of its
    media <FilePath>s in the text as it was OPENED, so a batch of relinks never flips it half way), then the machine
    this runs on (a project with no media paths, or a tie). Synthetic media (numeric FilePaths such as 1396920390 for
    adjustment layers and bars) do not count."""
    s = style or PATH_STYLE
    if s:
        if s not in ('win', 'mac'): raise ValueError("style must be 'win' or 'mac', not %r" % (s,))
        return s
    if getattr(doc, '_path_style', None) is None:
        n_win = n_mac = 0
        for fp in re.findall(r'<FilePath>([^<]*)</FilePath>', doc.orig_txt):
            if _WIN_PATH.match(fp): n_win += 1
            elif fp.startswith('/'): n_mac += 1
        doc._path_style = ('mac' if n_mac > n_win else 'win' if n_win > n_mac else
                           'mac' if sys.platform == 'darwin' else 'win')
    return doc._path_style


def _av_info(path):
    import av
    c = av.open(path)
    try:
        v = c.streams.video[0]
        rate = v.average_rate
        fr = TPS * rate.denominator / rate.numerator
        assert abs(fr - round(fr)) < 1e-6, 'frame rate %s does not give whole ticks' % rate
        fr = int(round(fr))
        n = v.frames or sum(1 for _ in c.decode(v))
        a = c.streams.audio[0] if c.streams.audio else None
        audio = None
        if a:
            assert TPS % a.rate == 0 and a.channels == 2, 'audio must be stereo with an even tick rate'
            audio = TPS // a.rate
        return dict(fr=fr, dur=n * fr, w=v.width, h=v.height, audio=audio, codec=v.codec_context.name,
                    mtime_us=int(round(os.path.getmtime(path) * 1e6)))
    finally:
        c.close()


def import_mp4(doc, path, project_dir, label=('10776567', 'BE.Prefs.LabelColors.6'), style=None):
    """all objects Premiere writes for an imported H.264 .mp4 (verified 26.x). Returns (master dict, object texts).
    Then: doc.append(texts); add the master's cpi_uid to a bin (new_bin / add_to_bin). Label default = Rose.
    style: None = the project's own <RelativePath> form (path_style), or 'win' / 'mac' to force one.
    For ProRes / alpha .mov or anything not H.264: import it in Premiere (Ctrl+I, Cmd+I on a Mac, or the bridge's
    app.project.importFiles), save, then use master_by_name()."""
    if sys.platform == 'darwin': path = os.path.abspath(path)      # macOS port: always write an absolute FilePath
    mi = _av_info(path)
    assert mi['codec'] == 'h264', 'import %s through Premiere instead (codec %s)' % (os.path.basename(path), mi['codec'])
    tcf = TIMECODE_FORMAT.get(mi['fr']); assert tcf, 'unknown timecode format for frame ticks %d' % mi['fr']
    name = esc(ntpath.basename(path)); p = esc(path)
    if path_style(doc, style) == 'mac':
        rel = rel_path(path, project_dir)
    else:
        try: rel = esc('.\\' + os.path.relpath(path, project_dir).replace('/', '\\'))
        except ValueError: rel = p
    ids = {k: doc.new_id() for k in ('li', 'vc', 'ccg', 'mk', 'vms', 'vs')}
    u = {k: str(uuid.uuid4()) for k in ('cpi', 'mc', 'media')}
    A = mi['audio'] is not None
    if A: ids.update({k: doc.new_id() for k in ('acc', 'ac', 'ams', 'sc0', 'sc1', 'ccv', 'cc0', 'cc1', 'as')})
    lc, ln = label
    LAYOUT = '[{"channellabel":100},{"channellabel":101}]'
    T = ['\t<ClipProjectItem ObjectUID="%s" ClassID="cb4e0ed7-aca1-4171-8525-e3658dec06dd" Version="1">\n'
         '\t\t<ProjectItem Version="1">\n\t\t\t<Node Version="1">\n\t\t\t\t<Properties Version="1">\n'
         '\t\t\t\t\t<Column.PropertyText.Label>%s</Column.PropertyText.Label>\n\t\t\t\t</Properties>\n\t\t\t</Node>\n'
         '\t\t\t<Name>%s</Name>\n\t\t</ProjectItem>\n\t\t<MasterClip ObjectURef="%s"/>\n\t</ClipProjectItem>' % (u['cpi'], ln, name, u['mc'])]
    mc = ['\t<MasterClip ObjectUID="%s" ClassID="fb11c33a-b0a9-4465-aa94-b6d5db2628cf" Version="12">' % u['mc'], '\t\t<LoggingInfo ObjectRef="%s"/>' % ids['li']]
    if A: mc += ['\t\t<AudioComponentChains Version="1">', '\t\t\t<AudioComponentChain Index="0" ObjectRef="%s"/>' % ids['acc'], '\t\t</AudioComponentChains>']
    mc += ['\t\t<Clips Version="1">', '\t\t\t<Clip Index="0" ObjectRef="%s"/>' % ids['vc']]
    if A: mc += ['\t\t\t<Clip Index="1" ObjectRef="%s"/>' % ids['ac']]
    mc += ['\t\t</Clips>', '\t\t<AudioClipChannelGroups ObjectRef="%s"/>' % ids['ccg'], '\t\t<Name>%s</Name>' % name]
    if A: mc += ['\t\t<DefMappingID>0551e2a0-6da1-4691-800e-b3ded5ca94f7</DefMappingID>']
    mc += ['\t\t<MasterClipChangeVersion>%d</MasterClipChangeVersion>' % (8 if A else 2), '\t</MasterClip>']
    T.append('\n'.join(mc))
    T.append('\t<ClipLoggingInfo ObjectID="%s" ClassID="77ab7fdd-dcdf-465d-9906-7a330ca1e738" Version="10">\n'
             '\t\t<ClipName>%s</ClipName>\n\t\t<TimecodeFormat>%d</TimecodeFormat>\n\t\t<MediaInPoint>0</MediaInPoint>\n'
             '\t\t<MediaOutPoint>%d</MediaOutPoint>\n\t\t<MediaFrameRate>%d</MediaFrameRate>\n\t</ClipLoggingInfo>' % (ids['li'], name, tcf, mi['dur'], mi['fr']))
    if A:
        T.append('\t<AudioComponentChain ObjectID="%s" ClassID="3cb131d1-d3c0-47ae-a19a-bdf75ea11674" Version="4">\n'
                 '\t\t<DefaultVol>true</DefaultVol>\n\t\t<DefaultVolumeComponentID>1</DefaultVolumeComponentID>\n'
                 '\t\t<DefaultChannelVolumeComponentID>2</DefaultChannelVolumeComponentID>\n\t\t<ComponentChain Version="3">\n\t\t</ComponentChain>\n'
                 '%s\t\t<AudioChannelLayout>%s</AudioChannelLayout>\n\t\t<ChannelType>1</ChannelType>\n\t</AudioComponentChain>'
                 % (ids['acc'], '' if mi['audio'] == SAMPLE_48K else '\t\t<FrameRate>%d</FrameRate>\n' % mi['audio'], LAYOUT))

    def clip(tag, cls, ver, oid, src, extra=''):
        return ('\t<%s ObjectID="%s" ClassID="%s" Version="%d">\n\t\t<Clip Version="18">\n\t\t\t<Node Version="1">\n\t\t\t\t<Properties Version="1">\n'
                '\t\t\t\t\t<asl.clip.label.color>%s</asl.clip.label.color>\n\t\t\t\t\t<asl.clip.label.name>%s</asl.clip.label.name>\n'
                '\t\t\t\t</Properties>\n\t\t\t</Node>\n\t\t\t<MarkerOwner Version="1">\n\t\t\t\t<Markers ObjectRef="%s"/>\n\t\t\t</MarkerOwner>\n'
                '\t\t\t<Source ObjectRef="%s"/>\n\t\t\t<ClipID>%s</ClipID>\n\t\t\t<InUse>false</InUse>\n\t\t</Clip>\n%s\t</%s>'
                % (tag, oid, cls, ver, lc, ln, ids['mk'], src, uuid.uuid4(), extra, tag))
    T.append(clip('VideoClip', '9308dbef-2440-4acb-9ab2-953b9a4e82ec', 11, ids['vc'], ids['vms']))
    if A:
        T.append(clip('AudioClip', 'b8830d03-de02-41ee-84ec-fe566dc70cd9', 8, ids['ac'], ids['ams'],
                      '\t\t<SecondaryContents Version="1">\n\t\t\t<SecondaryContentItem Index="0" ObjectRef="%s"/>\n'
                      '\t\t\t<SecondaryContentItem Index="1" ObjectRef="%s"/>\n\t\t</SecondaryContents>\n'
                      '\t\t<AudioChannelLayout>%s</AudioChannelLayout>\n' % (ids['sc0'], ids['sc1'], LAYOUT)))
        T.append('\t<ClipChannelGroupVectorSerializer ObjectID="%s" ClassID="a3127a8c-95d4-456e-a7f5-171b3f922426" Version="1">\n'
                 '\t\t<ClipChannelVectors Version="1">\n\t\t\t<ClipChannelVectorItem Index="0" ObjectRef="%s"/>\n\t\t</ClipChannelVectors>\n'
                 '\t</ClipChannelGroupVectorSerializer>' % (ids['ccg'], ids['ccv']))
    else:
        T.append('\t<ClipChannelGroupVectorSerializer ObjectID="%s" ClassID="a3127a8c-95d4-456e-a7f5-171b3f922426" Version="1">\n'
                 '\t</ClipChannelGroupVectorSerializer>' % ids['ccg'])
    T.append('\t<Markers ObjectID="%s" ClassID="bee50706-b524-416c-9f03-b596ce5f6866" Version="4">\n\t\t<ByGUID>byGUID</ByGUID>\n'
             '\t\t<LastMetadataState>00000000-0000-0000-0000-000000000000</LastMetadataState>\n'
             '\t\t<LastContentState>00000000-0000-0000-0000-000000000000</LastContentState>\n\t</Markers>' % ids['mk'])

    def msrc(tag, cls, oid):
        return ('\t<%s ObjectID="%s" ClassID="%s" Version="2">\n\t\t<MediaSource Version="4">\n\t\t\t<Content Version="10">\n\t\t\t</Content>\n'
                '\t\t\t<Media ObjectURef="%s"/>\n\t\t</MediaSource>\n\t\t<OriginalDuration>%d</OriginalDuration>\n\t</%s>' % (tag, oid, cls, u['media'], mi['dur'], tag))
    T.append(msrc('VideoMediaSource', 'e64ddf74-8fac-4682-8aa8-0e0ca2248949', ids['vms']))
    if A:
        T.append(msrc('AudioMediaSource', 'f588da05-fc2a-4fbc-9383-74d653b379e3', ids['ams']))
        for i, k in enumerate(('sc0', 'sc1')):
            T.append('\t<SecondaryContent ObjectID="%s" ClassID="f9d004b5-cb04-4e2f-af6f-64fadc2c4be9" Version="1">\n'
                     '\t\t<Content ObjectRef="%s"/>\n\t\t<ChannelIndex>%d</ChannelIndex>\n\t</SecondaryContent>' % (ids[k], ids['ams'], i))
        T.append('\t<ClipChannelVectorSerializer ObjectID="%s" ClassID="333d203b-3a53-4195-8894-fc7523ff3dc7" Version="1">\n'
                 '\t\t<ClipChannels Version="1">\n\t\t\t<ClipChannelItem Index="0" ObjectRef="%s"/>\n\t\t\t<ClipChannelItem Index="1" ObjectRef="%s"/>\n'
                 '\t\t</ClipChannels>\n\t\t<ChannelType>1</ChannelType>\n\t</ClipChannelVectorSerializer>' % (ids['ccv'], ids['cc0'], ids['cc1']))
        for i, k in enumerate(('cc0', 'cc1')):
            T.append('\t<ClipChannelSerializer ObjectID="%s" ClassID="5c89aa7a-89a6-4483-becd-f2b1def42316" Version="1">\n'
                     '\t\t<SourceClipIndex>0</SourceClipIndex>\n\t\t<mSourceChannelIndex>%d</mSourceChannelIndex>\n\t</ClipChannelSerializer>' % (ids[k], i))
    med = ['\t<Media ObjectUID="%s" ClassID="7a5c103e-f3ac-4391-b6b4-7cc3d2f9a7ff" Version="30">' % u['media']]
    if A: med.append('\t\t<AudioStream ObjectRef="%s"/>' % ids['as'])
    med += ['\t\t<VideoStream ObjectRef="%s"/>' % ids['vs'], '\t\t<RelativePath>%s</RelativePath>' % rel, '\t\t<FilePath>%s</FilePath>' % p,
            '\t\t<ImplementationID>1fa18bfa-255c-44b1-ad73-56bcd99fceaf</ImplementationID>', '\t\t<Title>%s</Title>' % name,
            '\t\t<FileKey>%s</FileKey>' % uuid.uuid4()]
    if A: med.append('\t\t<ConformedAudioRate>%d</ConformedAudioRate>' % mi['audio'])
    med += ['\t\t<ActualMediaFilePath>%s</ActualMediaFilePath>' % p, '\t\t<CCFileModTime>%d</CCFileModTime>' % mi['mtime_us'], '\t</Media>']
    T.append('\n'.join(med))
    if A:
        T.append('\t<AudioStream ObjectID="%s" ClassID="0b5cf52f-2b85-4863-890b-8844b64ecfe9" Version="8">\n\t\t<FrameRate>%d</FrameRate>\n'
                 '\t\t<AudioChannelLayout>%s</AudioChannelLayout>\n\t\t<Duration>%d</Duration>\n\t\t<SampleType>7</SampleType>\n\t</AudioStream>'
                 % (ids['as'], mi['audio'], LAYOUT, mi['dur']))
    T.append('\t<VideoStream ObjectID="%s" ClassID="a36e4719-3ec6-4a0c-ab11-8b4aab377aa5" Version="23">\n\t\t<FrameRate>%d</FrameRate>\n'
             '\t\t<Duration>%d</Duration>\n\t\t<IgnoreAlpha>true</IgnoreAlpha>\n\t\t<FrameRect>0,0,%d,%d</FrameRect>\n\t\t<CodecType>1635148593</CodecType>\n'
             '\t\t<OriginalColorSpace>{"baseColorProfile":{"colorProfileData":"AQAAAP////8=","colorProfileName":"BT.709,8-bit,Display-Referred"},"baseProfileType":1}</OriginalColorSpace>\n'
             '\t\t<AlphaType>3</AlphaType>\n\t\t<FieldTypeIsUncertain>true</FieldTypeIsUncertain>\n\t\t<OriginalImageOrientationType>1</OriginalImageOrientationType>\n'
             '\t</VideoStream>' % (ids['vs'], mi['fr'], mi['dur'], mi['w'], mi['h']))
    clips = [ids['vc']] + ([ids['ac']] if A else [])
    return dict(cpi_uid=u['cpi'], mc_uid=u['mc'], clips=clips, name=ntpath.basename(path), info=mi, path=path), T


# ------------------------------------------------------------------ bins
def _root_item(doc):
    m = re.search(r'\n\t<RootProjectItem Object(U?)ID="([^"]+)"', doc.txt)
    return m.group(2), m.group(1) == 'U'


def _container(raw):
    return re.search(r'(<ProjectItemContainer Version="\d+">\s*<Items Version="1">)(.*?)(\s*</Items>)', raw, re.S)


def new_bin(doc, name, item_uids):
    """new top-level bin holding the given ClipProjectItem uids (they must not be in another bin). Appends the bin."""
    uid = str(uuid.uuid4())
    items = ''.join('\n\t\t\t\t<Item Index="%d" ObjectURef="%s"/>' % (i, x) for i, x in enumerate(item_uids))
    doc.append('\t<BinProjectItem ObjectUID="%s" ClassID="dbfd6653-24da-480e-a35e-ba45e9504e4b" Version="1">\n\t\t<ProjectItem Version="1">\n'
               '\t\t\t<Node Version="1">\n\t\t\t\t<Properties Version="1">\n\t\t\t\t</Properties>\n\t\t\t</Node>\n\t\t\t<Name>%s</Name>\n'
               '\t\t</ProjectItem>\n\t\t<ProjectItemContainer Version="1">\n\t\t\t<Items Version="1">%s\n\t\t\t</Items>\n'
               '\t\t</ProjectItemContainer>\n\t</BinProjectItem>' % (uid, esc(name), items))
    rk, ru = _root_item(doc); rt = doc.raw(rk, uid=ru); m = _container(rt)
    old = re.findall(r'<Item Index="\d+" (ObjectU?Ref="[^"]+")/>', m.group(2))
    body = ''.join('\n\t\t\t\t<Item Index="%d" %s/>' % (k, i) for k, i in enumerate(old + ['ObjectURef="%s"' % uid]))
    doc.replace_obj(rk, rt[:m.start(2)] + body + rt[m.end(2):], uid=ru)
    return uid


def add_to_bin(doc, bin_name, item_uids):
    """put project items into an existing bin by name (moving them out of the root if they sit there)"""
    rk, ru = _root_item(doc); rt = doc.raw(rk, uid=ru); m = _container(rt)
    items = re.findall(r'<Item Index="\d+" (ObjectU?Ref="[^"]+")/>', m.group(2))
    keep = [i for i in items if not any(u in i for u in item_uids)]
    if len(keep) != len(items):
        body = ''.join('\n\t\t\t\t<Item Index="%d" %s/>' % (k, i) for k, i in enumerate(keep))
        doc.replace_obj(rk, rt[:m.start(2)] + body + rt[m.end(2):], uid=ru)
    bins = [k for _, k, _, b in doc.objects('BinProjectItem') if '<Name>%s</Name>' % esc(bin_name) in b]
    assert len(bins) == 1, 'bin %r: %d matches' % (bin_name, len(bins))
    bt = doc.raw(bins[0], uid=True); m = _container(bt)
    old = re.findall(r'<Item Index="\d+" (ObjectU?Ref="[^"]+")/>', m.group(2))
    body = ''.join('\n\t\t\t\t\t<Item Index="%d" %s/>' % (k, i) for k, i in enumerate(old + ['ObjectURef="%s"' % x for x in item_uids]))
    doc.replace_obj(bins[0], bt[:m.start(2)] + body + bt[m.end(2):], uid=True)


# ------------------------------------------------------------------ tracks: add
def _set_track_id(t, next_id):
    """set the track's own numeric <ID> inside its <Track Version=..> block, whatever the tag order: <ID>, <MediaType>,
    <Index> (Mac projects, 25.6 and 26.5, seen 11 Oct 2026, and most Windows projects) or <MediaType>, <Index>, <ID>
    (other Windows projects). One numeric <ID> per Track block in both (an audio track's own UUID <ID> sits outside it,
    in <AudioTrack>). Used on every machine. Returns (text, replacements)."""
    m = re.search(r'<Track Version="\d+">.*?</Track>', t, re.S)
    if not m: return t, 0
    blk, n = re.subn(r'<ID>\d+</ID>', '<ID>%d</ID>' % next_id, m.group(0), count=1)
    return t[:m.start()] + blk + t[m.end():], n


def add_video_track(doc, seq_uid, at=None):
    """insert an empty video track at index `at` (0 = V1, None = on top); tracks above move up one"""
    gid = track_groups(doc, seq_uid)['VideoTrackGroup']; g = doc.raw(gid)
    order = sorted((int(i), u) for i, u in re.findall(r'<Track Index="(\d+)" ObjectURef="([^"]+)"/>', g))
    if at is None: at = len(order)
    tmpl = order[-1][1]
    next_id = int(re.search(r'<NextTrackID>(\d+)</NextTrackID>', g).group(1))
    new_uid = str(uuid.uuid4())
    t = doc.raw(tmpl, uid=True).replace('ObjectUID="%s"' % tmpl, 'ObjectUID="%s"' % new_uid, 1)
    t = re.sub(r'(<ClipItems Version="\d+">)\s*<TrackItems Version="1">.*?</TrackItems>', r'\1', t, count=1, flags=re.S)
    t = re.sub(r'(<TransitionItems Version="\d+">)\s*<TrackItems Version="1">.*?</TrackItems>', r'\1', t, count=1, flags=re.S)
    t = re.sub(r'\n\t*<IsMuted>true</IsMuted>', '', t)
    t = re.sub(r'<Index>\d+</Index>', '<Index>%d</Index>' % at, t)
    t, n = _set_track_id(t, next_id)            # either tag order (see the note at the top)
    assert n == 1 and '<TrackItem ' not in t, 'track template not understood'
    for idx, u in order:
        if idx >= at:
            tt = doc.raw(u, uid=True)
            doc.replace_obj(u, re.sub(r'<Index>%d</Index>' % idx, '<Index>%d</Index>' % (idx + 1), tt), uid=True)
    uids = [u for _, u in order]; uids.insert(at, new_uid)
    block = ''.join('\n\t\t\t\t<Track Index="%d" ObjectURef="%s"/>' % (i, u) for i, u in enumerate(uids))
    g = re.sub(r'<Tracks Version="1">.*?\n\t\t\t</Tracks>', '<Tracks Version="1">%s\n\t\t\t</Tracks>' % block, g, count=1, flags=re.S)
    g = g.replace('<NextTrackID>%d</NextTrackID>' % next_id, '<NextTrackID>%d</NextTrackID>' % (next_id + 1), 1)
    doc.replace_obj(gid, g)
    st = doc.raw(seq_uid, uid=True)
    st2 = re.sub(r'(<HSL\.TimelinePatchingAndTargeting\.VideoPatches[^>]*>\[)(.*?)(\]</HSL)', lambda m: m.group(1) + m.group(2) + (',' if m.group(2) else '') + '{"mNumber":-1,"mState":0}' + m.group(3), st, count=1)
    doc.replace_obj(seq_uid, st2, uid=True)
    doc.append(t)
    return new_uid


def _deep_clone(doc, oid, idmap, out):
    if oid in idmap: return idmap[oid]
    new = doc.new_id(); idmap[oid] = new
    t = doc.raw(oid)
    for r in set(re.findall(r'ObjectRef="(\d+)"', t)): _deep_clone(doc, r, idmap, out)
    t = re.sub(r'(<\w+ ObjectID=")\d+(")', r'\g<1>%s\2' % new, t, count=1)
    t = re.sub(r'ObjectRef="(\d+)"', lambda m: 'ObjectRef="%s"' % idmap[m.group(1)], t)
    out.append(t)
    return new


def add_audio_track(doc, seq_uid):
    """new empty audio track on top, cloned from the highest empty audio track (else the top one, items stripped);
    the track's own mixer objects (Components, Panner) are deep-cloned so nothing is shared"""
    gid = track_groups(doc, seq_uid)['AudioTrackGroup']; g = doc.raw(gid)
    order = sorted((int(i), u) for i, u in re.findall(r'<Track Index="(\d+)" ObjectURef="([^"]+)"/>', g))
    empty = [u for _, u in order if not re.search(r'<ClipItems Version="\d+">\s*<TrackItems', doc.raw(u, uid=True))]
    tmpl = empty[-1] if empty else order[-1][1]
    raw = doc.raw(tmpl, uid=True)
    raw = re.sub(r'(<ClipItems Version="\d+">)\s*<TrackItems Version="1">.*?</TrackItems>', r'\1', raw, count=1, flags=re.S)
    raw = re.sub(r'(<TransitionItems Version="\d+">)\s*<TrackItems Version="1">.*?</TrackItems>', r'\1', raw, count=1, flags=re.S)
    raw = re.sub(r'\n\t*<IsMuted>true</IsMuted>', '', raw)
    assert '<TrackItem ' not in raw, 'track template not understood'
    next_id = int(re.search(r'<NextTrackID>(\d+)</NextTrackID>', g).group(1)); idx = len(order)
    idmap, objs = {}, []
    comp = re.search(r'<Components ObjectRef="(\d+)"', raw).group(1); pan = re.search(r'<Panner ObjectRef="(\d+)"', raw)
    nc = _deep_clone(doc, comp, idmap, objs)
    nu = str(uuid.uuid4())
    t = raw.replace(tmpl, nu, 1)
    t = re.sub(r'<Index>\d+</Index>', '<Index>%d</Index>' % idx, t)
    t, n = _set_track_id(t, next_id)            # either tag order; the old regex left <ID>-first tracks with a duplicate ID
    assert n == 1, 'audio track template not understood (no <ID> in its Track block)'
    t = re.sub(r'<Components ObjectRef="\d+"/>', '<Components ObjectRef="%s"/>' % nc, t, count=1)
    if pan:
        npn = _deep_clone(doc, pan.group(1), idmap, objs)
        t = re.sub(r'<Panner ObjectRef="\d+"/>', '<Panner ObjectRef="%s"/>' % npn, t, count=1)
        # the track's own UUID <ID> in <AudioTrack>: right after the Panner, or after a <FrameRate> there (1,916 of 8,233
        # audio tracks on the Windows PC, 14 Oct 2026). The old pattern missed the second layout and the new track kept
        # the template's UUID.
        t, n = re.subn(r'(<Panner ObjectRef="\d+"/>(?:\s*<FrameRate>\d+</FrameRate>)?\s*<ID>)[^<]*(</ID>)',
                       r'\g<1>%s\g<2>' % uuid.uuid4(), t, count=1)
        assert n == 1, 'audio track template not understood (no track UUID after its Panner)'
    doc.append(objs + [t])
    g = doc.raw(gid)
    g = g.replace('</Tracks>', '\t<Track Index="%d" ObjectURef="%s"/>\n\t\t\t</Tracks>' % (idx, nu), 1)
    g = re.sub(r'<NextTrackID>\d+</NextTrackID>', '<NextTrackID>%d</NextTrackID>' % (next_id + 1), g, count=1)
    doc.replace_obj(gid, g)
    st = doc.raw(seq_uid, uid=True)
    m = re.search(r'(<HSL\.TimelinePatchingAndTargeting\.AudioPatches[^>]*>)(\[.*?\])(</)', st)
    if m:
        patches = json.loads(unesc(m.group(2))); patches.append({"mNumber": -1, "mState": 0})
        st = st[:m.start(2)] + json.dumps(patches, separators=(',', ':')) + st[m.end(2):]
        doc.replace_obj(seq_uid, st, uid=True)
    return nu


# ------------------------------------------------------------------ deleting (only things YOU placed; disable the user's)
def component_ids(doc, comp_id):
    out = [comp_id]; t = doc.raw(comp_id)
    out += re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"\s*/>', t)
    for sid in re.findall(r'<SubComponent Index="\d+" ObjectRef="(\d+)"\s*/>', t): out += component_ids(doc, sid)
    return out


def delete_item(doc, ti, track_uid=None):
    """remove a track item you created and the objects only it owns (item, subclip, clip instance, chain, components,
    params, audio secondary contents). Never the shared MasterClip / MediaSource / Markers. Run normalize_blobs after."""
    inf = item_info(doc, ti)
    ids = [ti, inf['subclip'], inf['clip'], inf['chain']]
    ids += re.findall(r'<SecondaryContentItem Index="\d+" ObjectRef="(\d+)"/>', doc.raw(inf['clip']))
    for c in chain_components(doc, inf['chain']): ids += component_ids(doc, c)
    if track_uid: remove_from_track(doc, track_uid, [ti])
    for k in ids:
        if k and doc.exists(k): doc.delete_obj(k)


BLOB = re.compile(r'<(StartKeyframeValue|PremiereFilterPrivateData)( [^>]*?BinaryHash="([^"]+)")(/>|>([^<]*)</\1>)')


def normalize_blobs(doc):
    """after deletions: each blob's data must sit at its FIRST occurrence in document order (and only there)"""
    data = {}
    for m in BLOB.finditer(doc.orig_txt):
        if m.group(4) != '/>' and m.group(5): data.setdefault(m.group(3), m.group(5))
    for m in BLOB.finditer(doc.txt):
        if m.group(4) != '/>' and m.group(5): data.setdefault(m.group(3), m.group(5))
    seen, edits = set(), []
    for m in BLOB.finditer(doc.txt):
        h = m.group(3); inline = m.group(4) != '/>'
        if h not in seen:
            seen.add(h)
            if not inline and h in data: edits.append((m.start(), m.end(), '<%s%s>%s</%s>' % (m.group(1), m.group(2), data[h], m.group(1))))
        elif inline:
            edits.append((m.start(), m.end(), '<%s%s/>' % (m.group(1), m.group(2))))
    for s, e, rep in sorted(edits, reverse=True): doc.txt = doc.txt[:s] + rep + doc.txt[e:]
    return len(edits)


# ------------------------------------------------------------------ binary blobs (mask paths, text docs)
def new_hash(nbytes):
    """BinaryHash = 24 hex + 8 hex (blob length + 12). Premiere 26.5 accepts invented random hashes (verified)."""
    return uuid.uuid4().hex[:24] + '%08x' % (nbytes + 12)


def set_blob(doc, pid, raw_bytes):
    t = doc.raw(pid); b64 = base64.b64encode(raw_bytes).decode()
    t2, n = re.subn(r'<StartKeyframeValue Encoding="base64" BinaryHash="[^"]+"\s*(/>|>[^<]*</StartKeyframeValue>)',
                    '<StartKeyframeValue Encoding="base64" BinaryHash="%s">%s</StartKeyframeValue>' % (new_hash(len(raw_bytes)), b64), t, count=1)
    assert n == 1, 'param %s has no blob value' % pid
    doc.replace_obj(pid, t2)


def mask_path_blob(pts, closed=True):
    """Mask2 'Path' blob. pts = [(x, y, inX, inY, outX, outY)] normalized to the layer frame (absolute tangent points).
    Ellipse masks (Type 1) only work with 4 vertices."""
    b = struct.pack('<III', 2, 1, 31062) + b'\x00' + struct.pack('<II', 2, len(pts))
    for p in pts: b += struct.pack('<I6f', 1, *p)
    return b + (b'\x01' if closed else b'\x00')


def poly_pts(corners): return [(x, y, x, y, x, y) for x, y in corners]


if __name__ == '__main__':
    import sys
    if len(sys.argv) >= 3 and sys.argv[1] == 'unpack':        # python prproj_lib.py unpack in.prproj out.xml
        open(sys.argv[3] if len(sys.argv) > 3 else sys.argv[2] + '.xml', 'w', encoding='utf-8').write(Doc.open(sys.argv[2]).txt)
    elif len(sys.argv) >= 2:                                    # python prproj_lib.py project.prproj -> sequences + tracks
        d = Doc.open(sys.argv[1])
        for n, u in sequences(d):
            print('%s  %s' % (n, u))
            for k in ('video', 'audio'):
                for i, tu in enumerate(tracks(d, u, k)): print('   %s%d %d items' % (k[0].upper(), i + 1, len(clip_item_ids(d, tu))))
    else:
        print(__doc__)
