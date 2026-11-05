"""Build a brand-new Premiere sequence from an edit list as FCP7 XML (xmeml v4): File > Import in Premiere.
Use it when there is no project to modify yet (first assembly of rendered shots + voice + music + SFX).
To change an EXISTING project use prproj_lib.py instead (XML import makes a new sequence, it cannot edit one).

usage: python fcpxml.py edit.json out.xml       (writes the XML, then checks it)
       python fcpxml.py --check A.xml [B.xml]    (checks any FCP7 XML for what makes Premiere refuse it)
edit.json = {"name": "Show rough", "fps": 29.97, "w": 1920, "h": 1080, "total": 600.0,
             "video": [[{"path": "C:/r/shot1.mov", "a": 0.0, "b": 5.2, "si": 0.0, "label": "S01", "link": "c1"}, ...], [V2 ...]],
             "audio": [[{"path": "C:/r/shot1.mov", "a": 0.0, "b": 5.2, "si": 0.0, "db": 0.0, "link": "c1"}, ...], [A2 ...]],
             "sfx":   [{"path": "...", "a": 12.3, "b": null, "db": -10}, ...],      (packed into extra lanes automatically)
             "markers": [[178.0, "mid-roll"], [200.0, "CUT", "a longer note for the marker comment"], ...]}
a / b = sequence seconds (b null = file length, max 4 s for sfx), si = source in, db = clip level. Items that share a
"link" key become one linked clip (a shot's picture and its sound move together). Media facts come from PyAV.
Paths must be absolute: Windows ("C:/r/shot1.mov", "C:\\r\\shot1.mov") or macOS ("/Users/you/r/shot1.mov"). Each
<pathurl> takes the form of its own path, whichever machine builds the XML: file://localhost/C:/r/shot1.mov on
Windows, file://localhost/Users/you/r/shot1.mov on a Mac (path_url / url_path below).

Premiere refuses the WHOLE file ("File Import Failure") over one clip it cannot resolve, so this writes the layout of
XMLs that Premiere 2026 on Windows imported (verified 12 Oct 2026, after a job's first XMLs were refused): project > bin >
sequence; each <file> described in full where it first appears (video AND audio when the file has both, timecode,
channel count, sample rate); a stereo lane becomes two tracks (channels 1 and 2, sent to outputs 1 and 2) linked
together; no clip runs past the end of its file (trimmed with a note: loop music by laying several clips); markers at
the end of the sequence. The refused XMLs had sound clips pointing at a <file> that declared only video, and music
clips running past the end of their MP3.
"""
# Paths: the <pathurl> form follows each path (path_url), not the machine, so a Mac path never gets a doubled slash
# (file://localhost//Users/...) and --check reads both forms back (url_path). Untested so far: importing these XMLs in
# Premiere on a Mac.
# Mixed frame rates: every clipitem here uses the SEQUENCE timebase and each <file> carries the sequence <rate>. The Mac
# port instead gave each <file> its media's true <rate> plus <pproTicksIn>/<pproTicksOut> on every clipitem (a 29.97
# sequence holding 24/25 fps clips imported with the sync off without that, Sep 2026). Not used here, because this layout
# is the one verified on Premiere 2026 (12 Oct 2026). If a mixed-rate import drifts, test that change on a copy first.
import json
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape


def path_url(p):
    """<pathurl> of a media path, by the path's own form (the same on every machine):
    C:\\r\\a b.mov or C:/r/a b.mov -> file://localhost/C:/r/a%20b.mov (Windows, byte-identical to the older code)
    /Users/x/a b.mov             -> file://localhost/Users/x/a%20b.mov (macOS: the path keeps its one leading slash)"""
    if p.startswith('/') and not p.startswith('//'):          # POSIX absolute path; a backslash there is a real character
        return 'file://localhost' + urllib.parse.quote(p, safe='/:')
    return 'file://localhost/' + urllib.parse.quote(p.replace('\\', '/'), safe='/:')


def url_path(u):
    """local path of a <pathurl>, by the URL's own form: file://localhost/C:/x.mov (or C%3a, as Premiere writes it)
    -> C:/x.mov; file://localhost/Users/x.mov and file:///Users/x.mov -> /Users/x.mov; file://server/share/x ->
    //server/share/x."""
    if u.startswith('file://localhost'):
        rest = u[len('file://localhost'):]
    elif u.startswith('file://'):
        rest = u[len('file://'):]
        if not rest.startswith('/'): rest = '//' + rest       # a host name: a Windows network share
    else:
        return urllib.parse.unquote(u)
    rest = urllib.parse.unquote(rest)
    if re.match(r'/[A-Za-z]:([/\\]|$)', rest) or rest.startswith('///'):
        rest = rest[1:]                                        # /C:/x -> C:/x; ///server/share (path_url of \\server) -> //server
    return rest


def _absolute(p):
    return bool(re.match(r'[A-Za-z]:[\\/]', p)) or p.startswith(('/', '\\\\'))


def rate_xml(fps):
    ntsc = abs(fps - round(fps)) > 0.001
    tb = int(round(fps)) if not ntsc else int(round(fps * 1001 / 1000))
    return tb, ('TRUE' if ntsc else 'FALSE'), (tb * 1000 / 1001 if ntsc else float(tb))


_INFO = {}


def info(p):
    """Length (s), video (w, h) or None, audio (channels, sample rate) or None: read once per file."""
    if p not in _INFO:
        import av
        with av.open(p) as c:
            v = c.streams.video[0] if c.streams.video else None
            a = c.streams.audio[0] if c.streams.audio else None
            _INFO[p] = dict(dur=float(c.duration or 0) / 1e6 or 10.0,
                            video=(v.codec_context.width, v.codec_context.height) if v else None,
                            audio=(getattr(a, 'channels', 0) or a.codec_context.channels,
                                   getattr(a, 'sample_rate', 0) or a.codec_context.sample_rate) if a else None)
    return _INFO[p]


class Builder:
    def __init__(self, cfg):
        self.cfg = cfg
        self.tb, self.ntsc, self.fps = rate_xml(cfg.get('fps', 29.97))
        self.files, self.notes, self.n = {}, [], 0

    def fr(self, t): return int(round(t * self.fps))
    def rate(self): return '<rate><timebase>%d</timebase><ntsc>%s</ntsc></rate>' % (self.tb, self.ntsc)
    def url(self, p): return path_url(p)

    def timecode(self):
        return ('<timecode>%s<string>00:00:00%s00</string><frame>0</frame><displayformat>%s</displayformat></timecode>'
                % (self.rate(), ';' if self.ntsc == 'TRUE' else ':', 'DF' if self.ntsc == 'TRUE' else 'NDF'))

    def file_el(self, p):
        """The full description where a file first appears in the document, a reference after that."""
        if p in self.files:
            return '<file id="%s"/>' % self.files[p]
        fid = self.files[p] = 'file-%d' % (len(self.files) + 1)
        if not _absolute(p):
            self.notes.append('%s is a relative path: Premiere needs absolute paths, the import will fail' % p)
        m, media = info(p), ''
        if m['video']:
            media += ('<video><samplecharacteristics>%s<width>%d</width><height>%d</height><anamorphic>FALSE</anamorphic>'
                      '<pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics>'
                      '</video>' % ((self.rate(),) + tuple(m['video'])))
        if m['audio']:
            media += ('<audio><samplecharacteristics><depth>16</depth><samplerate>%d</samplerate></samplecharacteristics>'
                      '<channelcount>%d</channelcount></audio>' % (m['audio'][1], m['audio'][0]))
        return ('<file id="%s"><name>%s</name><pathurl>%s</pathurl>%s<duration>%d</duration>%s<media>%s</media></file>'
                % (fid, escape(os.path.basename(p)), self.url(p), self.rate(), self.fr(m['dur']), self.timecode(), media))

    def place(self, e):
        """Frames (start, end, in, out, file length) of one item, kept inside its file; None if nothing is left."""
        p, si, b = e['path'], e.get('si', 0.0), e['b']
        s, en, i, dur = self.fr(e['a']), self.fr(b), max(0, self.fr(si)), self.fr(info(p)['dur'])
        over = i + (en - s) - dur
        if over > 0:  # a clip past the end of its file makes Premiere refuse the whole XML
            if over > 2:
                self.notes.append('%s at %.2f s ran %d frames past the end of its file: trimmed' % (os.path.basename(p), e['a'], over))
            en -= over
        if en <= s:
            self.notes.append('%s at %.2f s has no length left: left out' % (os.path.basename(p), e['a']))
            return None
        return s, en, i, i + en - s, dur

    def build(self):
        cfg = self.cfg
        lanes = [list(tr) for tr in cfg.get('audio', [])]
        sfx_lanes, ends = [], []
        for e in sorted(cfg.get('sfx', []), key=lambda e: e['a']):
            if e.get('b') is None:
                e = dict(e, b=min(e['a'] + min(info(e['path'])['dur'] - e.get('si', 0.0), 4.0), cfg['total']))
            k = next((i for i, en in enumerate(ends) if e['a'] >= en), None)
            if k is None:
                sfx_lanes.append([]); ends.append(-1.0); k = len(sfx_lanes) - 1
            sfx_lanes[k].append(e); ends[k] = e['b']
        # 1) every clipitem gets its track, place in the track and id first, so linked items can name each other
        items, out_ch = [], {}
        for t, tr in enumerate(cfg.get('video', []), 1):
            k = 0
            for e in tr:
                f = self.place(e)
                if f:
                    k += 1
                    items.append(dict(mt='video', track=t, index=k, e=e, f=f, ch=1,
                                      group=('link', e['link']) if e.get('link') else ('v', t, k)))
        nv, t = len(cfg.get('video', [])), 0
        for ln, lane in enumerate(lanes + sfx_lanes):
            placed = []
            for e in lane:
                if not info(e['path'])['audio']:
                    self.notes.append('%s has no sound: left off the audio tracks' % os.path.basename(e['path']))
                    continue
                f = self.place(e)
                if f:
                    placed.append((e, f))
            pair = any(info(e['path'])['audio'][0] >= 2 for e, _ in placed)
            for ch in ((1, 2) if pair else (1,)):
                t += 1
                out_ch[t] = ch if pair else None
                for k, (e, f) in enumerate(placed, 1):
                    items.append(dict(mt='audio', track=t, index=k, e=e, f=f, ch=min(ch, info(e['path'])['audio'][0]),
                                      group=('link', e['link']) if e.get('link') else ('a', ln, k)))
        na = t
        for k, it in enumerate(items, 1):
            it['id'] = 'clipitem-%d' % k
        self.n = len(items)
        groups = {}
        for it in items:
            groups.setdefault(it['group'], []).append(it)

        # 2) write in document order (video tracks, then audio), so each file is described in full where it first appears
        def clip_xml(it):
            e, (s, en, i, o, dur) = it['e'], it['f']
            fx = self.file_el(e['path'])
            flt = ''
            if it['mt'] == 'audio' and e.get('db'):
                flt = ('<filter><effect><name>Audio Levels</name><effectid>audiolevels</effectid><effectcategory>audiolevels</effectcategory>'
                       '<effecttype>audiolevels</effecttype><mediatype>audio</mediatype><parameter><parameterid>level</parameterid>'
                       '<name>Level</name><valuemin>0</valuemin><valuemax>3.98109</valuemax><value>%.5f</value></parameter></effect>'
                       '</filter>' % min(3.98109, 10 ** (e['db'] / 20)))
            links = ''
            if len(groups[it['group']]) > 1:
                links = ''.join('<link><linkclipref>%s</linkclipref><mediatype>%s</mediatype><trackindex>%d</trackindex>'
                                '<clipindex>%d</clipindex>%s</link>' % (m['id'], m['mt'], m['track'], m['index'],
                                                                         '<groupindex>1</groupindex>' if m['mt'] == 'audio' else '')
                                for m in groups[it['group']])
            return ('<clipitem id="%s"><masterclipid>masterclip-%s</masterclipid><name>%s</name><enabled>TRUE</enabled>'
                    '<duration>%d</duration>%s<start>%d</start><end>%d</end><in>%d</in><out>%d</out>%s<sourcetrack><mediatype>%s'
                    '</mediatype><trackindex>%d</trackindex></sourcetrack>%s%s</clipitem>'
                    % (it['id'], self.files[e['path']].split('-')[1], escape(e.get('label') or os.path.basename(e['path'])), dur,
                       self.rate(), s, en, i, o, fx, it['mt'], it['ch'], flt, links))

        vt = ''.join('<track>%s<enabled>TRUE</enabled><locked>FALSE</locked></track>\n'
                     % ''.join(clip_xml(it) for it in items if it['mt'] == 'video' and it['track'] == k) for k in range(1, nv + 1))
        at = ''.join('<track>%s<enabled>TRUE</enabled><locked>FALSE</locked>%s</track>\n'
                     % (''.join(clip_xml(it) for it in items if it['mt'] == 'audio' and it['track'] == k),
                        '<outputchannelindex>%d</outputchannelindex>' % out_ch[k] if out_ch[k] else '') for k in range(1, na + 1))
        outputs = ''.join('<group><index>%d</index><numchannels>1</numchannels><downmix>0</downmix><channel><index>%d</index>'
                          '</channel></group>' % (k, k) for k in (1, 2))
        mk = ''.join('<marker><name>%s</name><comment>%s</comment><in>%d</in><out>-1</out></marker>'
                     % (escape(m[1]), escape(m[2] if len(m) > 2 else ''), self.fr(m[0])) for m in cfg.get('markers', []))
        name = escape(cfg.get('name', 'Sequence'))
        return ('<?xml version="1.0" encoding="UTF-8"?>\n<!DOCTYPE xmeml>\n<xmeml version="4">\n<project><name>%s</name><children>\n'
                '<bin><name>%s</name><children>\n<sequence id="sequence-1"><name>%s</name><duration>%d</duration>%s%s\n'
                '<media><video><format><samplecharacteristics>%s<width>%d</width><height>%d</height><anamorphic>FALSE</anamorphic>'
                '<pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance><colordepth>24</colordepth>'
                '</samplecharacteristics></format>\n%s</video>\n<audio><numOutputChannels>2</numOutputChannels><format>'
                '<samplecharacteristics><depth>16</depth><samplerate>48000</samplerate></samplecharacteristics></format>'
                '<outputs>%s</outputs>\n%s</audio></media>%s</sequence>\n</children></bin>\n</children></project></xmeml>\n'
                % (name, escape(cfg.get('bin', cfg.get('name', 'Sequence'))), name, self.fr(cfg['total']), self.rate(),
                   self.timecode(), self.rate(), cfg.get('w', 1920), cfg.get('h', 1080), vt, outputs, at, mk))


def check(path):
    """The things that make Premiere refuse an FCP7 XML. Returns a list of problems (empty = clean)."""
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        return ['not well-formed XML: %s' % e]
    probs, files, seen = [], {}, set()
    for f in root.iter('file'):  # a short <file id="x"/> must come after the full description of x
        if f.find('pathurl') is not None:
            files[f.get('id')] = f; seen.add(f.get('id'))
        elif f.get('id') not in seen:
            probs.append('%s is used before it is described' % f.get('id'))
    for fid, f in files.items():
        p = url_path(f.findtext('pathurl'))           # Windows and macOS forms, whichever machine checks
        if not os.path.exists(p):
            probs.append('%s is not on disk: %s' % (fid, p))
    for seq in root.iter('sequence'):
        if not (seq.findtext('rate/timebase') or '').isdigit():
            probs.append('sequence %s: frame rate missing or not a whole number' % seq.findtext('name'))
        for kind in ('video', 'audio'):
            for t, tr in enumerate(seq.findall('media/%s/track' % kind), 1):
                prev = None
                for ci in tr.findall('clipitem'):
                    tag = '%s%d %s' % (kind[0].upper(), t, ci.findtext('name'))
                    try:
                        s, e, i, o, d = (int(ci.findtext(k)) for k in ('start', 'end', 'in', 'out', 'duration'))
                    except (TypeError, ValueError):
                        probs.append('%s: start/end/in/out/duration missing or not whole frames' % tag); continue
                    fe = ci.find('file')
                    f = files.get(fe.get('id')) if fe is not None else None
                    if f is None:
                        probs.append('%s: no file' % tag); continue
                    media = [m.tag for m in f.find('media')] if f.find('media') is not None else []
                    fd = int(f.findtext('duration') or 0)
                    if kind not in media:
                        probs.append('%s: on %s track, but its file declares only %s' % (tag, 'an audio' if kind == 'audio' else 'a video', media or 'nothing'))
                    if e <= s or o <= i:
                        probs.append('%s: no length' % tag)
                    if o - i != e - s:
                        probs.append('%s: source length %d frames, timeline length %d' % (tag, o - i, e - s))
                    if i < 0 or s < 0:
                        probs.append('%s: negative time' % tag)
                    if o > fd:
                        probs.append('%s: runs %d frames past the end of its file' % (tag, o - fd))
                    if prev is not None and s < prev:
                        probs.append('%s: overlaps the clip before it by %d frames' % (tag, prev - s))
                    prev = e
    return probs


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit(__doc__)
    if sys.argv[1] == '--check':
        bad = 0
        for x in sys.argv[2:]:
            pr = check(x)
            bad += bool(pr)
            print(('OK    ' if not pr else 'FAIL  ') + os.path.basename(x))
            for line in pr[:12]:
                print('   ', line)
            if len(pr) > 12:
                print('    ... %d more' % (len(pr) - 12))
        sys.exit(1 if bad else 0)
    cfg = json.load(open(sys.argv[1], encoding='utf-8'))
    b = Builder(cfg)
    xml = b.build()
    open(sys.argv[2], 'w', encoding='utf-8').write(xml)
    for note in b.notes:
        print('  note:', note)
    pr = check(sys.argv[2])
    for line in pr:
        print('  PROBLEM:', line)
    print('wrote', os.path.basename(sys.argv[2]), '| clips', b.n, '| files', len(b.files), '| check:',
          'clean' if not pr else '%d problems' % len(pr))
