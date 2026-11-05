"""Add the external B-roll (Paula archive from YouTube + Pexels stock) to the Premiere-saved B-roll project.

- imports every downloaded external clip into a new "External B roll" bin (Rec.709 media, no colour override)
- takes out three weaker camera B-roll shots so every ad stays at or under ~40 % B-roll
- places the new shots on the B-roll track (V2, or V4 in the reference) with Motion framing and a light Lumetri
- re-cuts the master grade adjustment layer so it covers exactly the parts of each ad with no B-roll
Text-level surgery on the decompressed XML; untouched objects stay byte-identical.
"""
import sys, os, re, uuid, gzip, json, ntpath
sys.path.insert(0, '.')
from build_project import Doc, TPS, fmt, for_claude_sequences, video_tracks, track_items
from build_broll import strip_inline, clone_component, chain_components, clone_chain, set_times, set_inout, item_parts, set_track_items
sys.path.insert(0, '../work')
import ext_plan, mp4info

F60 = 4233600000
REF = '348e0ba6'
PROJ_DIR = r'C:\VISION\IMMUFIX'
LABEL = ('10776567', 'BE.Prefs.LabelColors.6')          # Rose: external clips stand out on the timeline
TCF = {10160640000: 101, 10594584000: 110, 8475667200: 103, 8467200000: 104, 10584000000: 100, 4233600000: 108}
BIN_NAME = 'External B roll'

# light Lumetri for Rec.709 footage: master look (curves, wheels, vignette) kept, LOG-specific basic corrections zeroed
NEUTRAL = {15: 0.0, 19: 0.0, 20: 0.0, 21: 0.0, 22: 0.0, 23: 0.0, 24: 0.0, 41: 0.0, 42: 0.0}
GRADE = {   # index: 14 Temp, 16 Saturation, 19 Exposure, 41 Sharpen, 42 Vibrance
    'powder':         {14: 4.0, 16: 95.0, 19: -0.3},
    'capsules_hands': {14: 2.0, 16: 85.0},
    'green_shake':    {14: 3.0, 16: 95.0},
    'spill':          {14: 3.0, 16: 90.0},
    'counting':       {14: 6.0, 19: -0.1},
    'poured':         {14: 4.0},
    'veg':            {14: 0.0, 16: 88.0, 19: 0.2},
    'chicago':        {14: 6.0, 16: 95.0, 19: 0.35, 41: 20.0, 42: 5.0},
    'london':         {14: 0.0, 16: 90.0, 19: 0.3, 41: 20.0},
}
AUDIO_LAYOUT = '[{"channellabel":100},{"channellabel":101}]'


def set_times2(ti_txt, start, end):
    """like set_times but keeps Premiere's element order (Node, Start, End)"""
    ti_txt = re.sub(r'<End>\d+</End>', '<End>%d</End>' % end, ti_txt)
    if re.search(r'<Start>\d+</Start>', ti_txt):
        if start: ti_txt = re.sub(r'<Start>\d+</Start>', '<Start>%d</Start>' % start, ti_txt)
        else: ti_txt = re.sub(r'\n\t*<Start>\d+</Start>', '', ti_txt)
    elif start:
        ti_txt = re.sub(r'(\n\t*)(<End>\d+</End>)', lambda m: '%s<Start>%d</Start>%s%s' % (m.group(1), start, m.group(1), m.group(2)), ti_txt, 1)
    return ti_txt


def esc(s):
    return s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


# ---------------------------------------------------------------- media import
def media_info(path):
    r = mp4info.info(path)
    v = [t for t in r['tracks'] if t.get('handler') == 'vide'][0]
    a = [t for t in r['tracks'] if t.get('handler') == 'soun']
    assert v['stts_n'] == 1, 'variable frame rate: ' + path
    delta = v['stts'][0][1]
    assert (TPS * delta) % v['timescale'] == 0
    fr = TPS * delta // v['timescale']
    audio = None
    if a:
        assert TPS % a[0]['rate'] == 0 and a[0]['channels'] == 2
        audio = TPS // a[0]['rate']
    return dict(fr=fr, dur=v['nsamples'] * fr, w=v['wh'][0], h=v['wh'][1], audio=audio,
                mtime_us=int(round(os.path.getmtime(path) * 1e6)))


def media_objects(doc, path):
    """all objects Premiere writes for an imported H.264 .mp4 (templates: B roll bin clip + a YouTube download from the user's other projects)"""
    mi = media_info(path)
    name = esc(ntpath.basename(path)); p = esc(path)
    rel = esc('.' + path[len(PROJ_DIR):]) if path.lower().startswith(PROJ_DIR.lower() + '\\') else p
    ids = {k: doc.new_id() for k in ('li', 'vc', 'ccg', 'mk', 'vms', 'vs')}
    u = {k: str(uuid.uuid4()) for k in ('cpi', 'mc', 'media')}
    A = mi['audio'] is not None
    if A: ids.update({k: doc.new_id() for k in ('acc', 'ac', 'ams', 'sc0', 'sc1', 'ccv', 'cc0', 'cc1', 'as')})
    lc, ln = LABEL
    T = []
    T.append('\t<ClipProjectItem ObjectUID="%s" ClassID="cb4e0ed7-aca1-4171-8525-e3658dec06dd" Version="1">\n'
             '\t\t<ProjectItem Version="1">\n\t\t\t<Node Version="1">\n\t\t\t\t<Properties Version="1">\n'
             '\t\t\t\t\t<Column.PropertyText.Label>%s</Column.PropertyText.Label>\n\t\t\t\t</Properties>\n\t\t\t</Node>\n'
             '\t\t\t<Name>%s</Name>\n\t\t</ProjectItem>\n\t\t<MasterClip ObjectURef="%s"/>\n\t</ClipProjectItem>' % (u['cpi'], ln, name, u['mc']))
    mc = ['\t<MasterClip ObjectUID="%s" ClassID="fb11c33a-b0a9-4465-aa94-b6d5db2628cf" Version="12">' % u['mc'],
          '\t\t<LoggingInfo ObjectRef="%s"/>' % ids['li']]
    if A: mc += ['\t\t<AudioComponentChains Version="1">', '\t\t\t<AudioComponentChain Index="0" ObjectRef="%s"/>' % ids['acc'], '\t\t</AudioComponentChains>']
    mc += ['\t\t<Clips Version="1">', '\t\t\t<Clip Index="0" ObjectRef="%s"/>' % ids['vc']]
    if A: mc += ['\t\t\t<Clip Index="1" ObjectRef="%s"/>' % ids['ac']]
    mc += ['\t\t</Clips>', '\t\t<AudioClipChannelGroups ObjectRef="%s"/>' % ids['ccg'], '\t\t<Name>%s</Name>' % name]
    if A: mc += ['\t\t<DefMappingID>0551e2a0-6da1-4691-800e-b3ded5ca94f7</DefMappingID>']
    mc += ['\t\t<MasterClipChangeVersion>%d</MasterClipChangeVersion>' % (8 if A else 2), '\t</MasterClip>']
    T.append('\n'.join(mc))
    T.append('\t<ClipLoggingInfo ObjectID="%s" ClassID="77ab7fdd-dcdf-465d-9906-7a330ca1e738" Version="10">\n'
             '\t\t<ClipName>%s</ClipName>\n\t\t<TimecodeFormat>%d</TimecodeFormat>\n\t\t<MediaInPoint>0</MediaInPoint>\n'
             '\t\t<MediaOutPoint>%d</MediaOutPoint>\n\t\t<MediaFrameRate>%d</MediaFrameRate>\n\t</ClipLoggingInfo>'
             % (ids['li'], name, TCF.get(mi['fr'], 998), mi['dur'], mi['fr']))
    if A:
        T.append('\t<AudioComponentChain ObjectID="%s" ClassID="3cb131d1-d3c0-47ae-a19a-bdf75ea11674" Version="4">\n'
                 '\t\t<DefaultVol>true</DefaultVol>\n\t\t<DefaultVolumeComponentID>1</DefaultVolumeComponentID>\n'
                 '\t\t<DefaultChannelVolumeComponentID>2</DefaultChannelVolumeComponentID>\n\t\t<ComponentChain Version="3">\n\t\t</ComponentChain>\n'
                 '%s\t\t<AudioChannelLayout>%s</AudioChannelLayout>\n\t\t<ChannelType>1</ChannelType>\n\t</AudioComponentChain>'
                 % (ids['acc'], '' if mi['audio'] == 5292000 else '\t\t<FrameRate>%d</FrameRate>\n' % mi['audio'], AUDIO_LAYOUT))

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
                      '\t\t<AudioChannelLayout>%s</AudioChannelLayout>\n' % (ids['sc0'], ids['sc1'], AUDIO_LAYOUT)))
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
                 % (ids['as'], mi['audio'], AUDIO_LAYOUT, mi['dur']))
    T.append('\t<VideoStream ObjectID="%s" ClassID="a36e4719-3ec6-4a0c-ab11-8b4aab377aa5" Version="23">\n\t\t<FrameRate>%d</FrameRate>\n'
             '\t\t<Duration>%d</Duration>\n\t\t<IgnoreAlpha>true</IgnoreAlpha>\n\t\t<FrameRect>0,0,%d,%d</FrameRect>\n\t\t<CodecType>1635148593</CodecType>\n'
             '\t\t<OriginalColorSpace>{"baseColorProfile":{"colorProfileData":"AQAAAP////8=","colorProfileName":"BT.709,8-bit,Display-Referred"},"baseProfileType":1}</OriginalColorSpace>\n'
             '\t\t<AlphaType>3</AlphaType>\n\t\t<FieldTypeIsUncertain>true</FieldTypeIsUncertain>\n\t\t<OriginalImageOrientationType>1</OriginalImageOrientationType>\n'
             '\t</VideoStream>' % (ids['vs'], mi['fr'], mi['dur'], mi['w'], mi['h']))
    master = dict(cpi_uid=u['cpi'], mc_uid=u['mc'], master_vclip=ids['vc'], name=name, info=mi, path=path)
    return master, T


def bin_object(doc, name, item_uids):
    tmpl_root = [c for c in doc.root if c.tag == 'RootProjectItem'][0]
    uid = str(uuid.uuid4())
    items = ''.join('\n\t\t\t\t<Item Index="%d" ObjectURef="%s"/>' % (i, x) for i, x in enumerate(item_uids))
    txt = ('\t<BinProjectItem ObjectUID="%s" ClassID="dbfd6653-24da-480e-a35e-ba45e9504e4b" Version="1">\n\t\t<ProjectItem Version="1">\n'
           '\t\t\t<Node Version="1">\n\t\t\t\t<Properties Version="1">\n\t\t\t\t</Properties>\n\t\t\t</Node>\n\t\t\t<Name>%s</Name>\n'
           '\t\t</ProjectItem>\n\t\t<ProjectItemContainer Version="1">\n\t\t\t<Items Version="1">%s\n\t\t\t</Items>\n'
           '\t\t</ProjectItemContainer>\n\t</BinProjectItem>' % (uid, esc(name), items))
    rt = doc.raw(tmpl_root.attrib['ObjectUID'], uid=True)
    n = len(re.findall(r'\n\t\t\t\t<Item Index="\d+" ObjectURef="[^"]+"/>', rt))
    rt2 = rt.replace('\n\t\t\t</Items>\n\t\t</ProjectItemContainer>\n\t</RootProjectItem>',
                     '\n\t\t\t\t<Item Index="%d" ObjectURef="%s"/>\n\t\t\t</Items>\n\t\t</ProjectItemContainer>\n\t</RootProjectItem>' % (n, uid), 1)
    assert rt2 != rt
    doc.replace_obj(tmpl_root.attrib['ObjectUID'], rt2, uid=True)
    return uid, txt


# ---------------------------------------------------------------- deleting objects
def delete_obj(doc, key):
    s, e = doc.span(key)
    if doc.txt[e:e + 1] == '\n': e += 1
    doc.txt = doc.txt[:s] + doc.txt[e:]


def component_ids(doc, comp_id):
    out = [comp_id]
    t = doc.raw(comp_id)
    out += re.findall(r'<Param Index="\d+" ObjectRef="(\d+)"\s*/>', t)
    for sid in re.findall(r'<SubComponent Index="\d+" ObjectRef="(\d+)"\s*/>', t):
        out += component_ids(doc, sid)
    return out


def item_object_ids(doc, ti_id):
    t = doc.raw(ti_id)
    sc = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
    ch = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    vc = re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sc)).group(1)
    ids = [ti_id, sc, vc, ch]
    for c in chain_components(doc, ch): ids += component_ids(doc, c)
    return ids


def delete_item(doc, ti_id):
    for k in item_object_ids(doc, ti_id): delete_obj(doc, k)


# ---------------------------------------------------------------- items
def item_times(doc, ti_id):
    t = doc.raw(ti_id)
    s = re.search(r'<Start>(\d+)</Start>', t); e = int(re.search(r'<End>(\d+)</End>', t).group(1))
    sc = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
    vc = re.search(r'<Clip ObjectRef="(\d+)"', doc.raw(sc)).group(1)
    vt = doc.raw(vc)
    return int(s.group(1)) if s else 0, e, int(re.search(r'<InPoint>(-?\d+)</InPoint>', vt).group(1)), vc


def retime_item(doc, ti_id, start, end):
    s, e, tin, vc = item_times(doc, ti_id)
    off = tin - s
    doc.replace_obj(ti_id, set_times2(doc.raw(ti_id), start, end))
    doc.replace_obj(vc, set_inout(doc.raw(vc), start + off, end + off))


def clone_item(doc, ti_id, start, end, overrides_by_comp=None):
    """deep clone of a track item (chain, components, clip instance) at a new time; media offset kept"""
    overrides_by_comp = overrides_by_comp or {}
    s, e, tin, vc_id = item_times(doc, ti_id)
    off = tin - s
    t = doc.raw(ti_id)
    sc_id = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
    ch_id = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    objs, comp_ids = [], []
    for i, cid in enumerate(chain_components(doc, ch_id)):
        ncid, texts = clone_component(doc, cid, overrides_by_comp.get(i)); comp_ids.append(ncid); objs += texts
    nch, chtxt = clone_chain(doc, ch_id, comp_ids)
    nvc, nsc, nti = doc.new_id(), doc.new_id(), doc.new_id()
    vctxt = set_inout(strip_inline(doc.raw(vc_id).replace('ObjectID="%s"' % vc_id, 'ObjectID="%s"' % nvc, 1)), start + off, end + off)
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1))
    titxt = doc.raw(ti_id).replace('ObjectID="%s"' % ti_id, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    titxt = set_times2(titxt, start, end)
    return nti, objs + [chtxt, vctxt, sctxt, titxt]


def ext_item(doc, tmpl_ti, master, start, end, src_in, px, py, scale, lum_overrides):
    """new B-roll clip on the template's structure: new media, Motion framing, light Lumetri"""
    t = doc.raw(tmpl_ti)
    sc_id = re.search(r'<SubClip ObjectRef="(\d+)"', t).group(1)
    ch_id = re.search(r'<Components ObjectRef="(\d+)"', t).group(1)
    comps = chain_components(doc, ch_id)
    mot = [c for c in comps if '<MatchName>AE.ADBE Motion</MatchName>' in doc.raw(c)][0]
    lum = [c for c in comps if '<MatchName>AE.ADBE Lumetri</MatchName>' in doc.raw(c)][0]
    nmot, mtexts = clone_component(doc, mot, {'Position': '%.6f:%.6f' % (px, py), 'Scale': float(scale)})
    nlum, ltexts = clone_component(doc, lum, lum_overrides)
    nch, chtxt = clone_chain(doc, ch_id, [nmot, nlum])
    mvc = master['master_vclip']
    nvc, nsc, nti = doc.new_id(), doc.new_id(), doc.new_id()
    vctxt = strip_inline(doc.raw(mvc).replace('ObjectID="%s"' % mvc, 'ObjectID="%s"' % nvc, 1))
    vctxt = re.sub(r'\n\t\t\t<InUse>[^<]*</InUse>', '', vctxt)
    vctxt = re.sub(r'(<Source ObjectRef="\d+"/>)', r'\1\n\t\t\t<OutPoint>%d</OutPoint>\n\t\t\t<InPoint>%d</InPoint>' % (src_in + (end - start), src_in), vctxt, 1)
    vctxt = re.sub(r'<ClipID>[^<]*</ClipID>', '<ClipID>%s</ClipID>' % uuid.uuid4(), vctxt)
    sctxt = doc.raw(sc_id).replace('ObjectID="%s"' % sc_id, 'ObjectID="%s"' % nsc, 1)
    sctxt = re.sub(r'(<Clip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nvc, sctxt)
    sctxt = re.sub(r'(<MasterClip ObjectURef=")[^"]+(")', r'\g<1>%s\g<2>' % master['mc_uid'], sctxt)
    sctxt = re.sub(r'<Name>[^<]*</Name>', lambda m: '<Name>%s</Name>' % master['name'], sctxt)
    titxt = t.replace('ObjectID="%s"' % tmpl_ti, 'ObjectID="%s"' % nti, 1)
    titxt = re.sub(r'(<Components ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nch, titxt)
    titxt = re.sub(r'(<SubClip ObjectRef=")\d+(")', r'\g<1>%s\g<2>' % nsc, titxt)
    titxt = re.sub(r'\n\t\t\t<IsMuted>[^<]*</IsMuted>', '', titxt)
    titxt = set_times2(titxt, start, end)
    return nti, mtexts + ltexts + [chtxt, vctxt, sctxt, titxt]


# ---------------------------------------------------------------- grade signature
def chain_signature(doc, ti_id):
    ch = re.search(r'<Components ObjectRef="(\d+)"', doc.raw(ti_id)).group(1)
    sig = []
    for c in chain_components(doc, ch):
        t = doc.raw(c)
        pid = re.search(r'<Param Index="19" ObjectRef="(\d+)"', t).group(1)
        sig.append(re.search(r'<StartKeyframe>(-?\d+),([^,]+),', doc.raw(pid)).group(2))
    return tuple(sig)


def original_grade_items(v3doc, key):
    """(start, end, signature) of the grade adjustment items before any B-roll cut (from the Premiere-saved grade project)"""
    seq = [s for n, s in for_claude_sequences(v3doc) if s.attrib['ObjectUID'].startswith(key)][0]
    trs = video_tracks(v3doc, seq)
    g = trs[3] if key == REF else trs[2]
    out = []
    for ti in track_items(v3doc, g):
        tid = ti.attrib['ObjectID']
        s, e, tin, vc = item_times(v3doc, tid)
        out.append((s, e, chain_signature(v3doc, tid)))
    return sorted(out)


def subtract(a, b, cuts):
    pieces = [(a, b)]
    for x, y in sorted(cuts):
        nxt = []
        for p, q in pieces:
            if y <= p or x >= q: nxt.append((p, q)); continue
            if x > p: nxt.append((p, x))
            if y < q: nxt.append((y, q))
        pieces = nxt
    return [(p, q) for p, q in pieces if q - p >= F60]


# ---------------------------------------------------------------- blobs
BLOB = re.compile(r'<(StartKeyframeValue|PremiereFilterPrivateData)( [^>]*?BinaryHash="([^"]+)")(/>|>([^<]*)</\1>)')


def normalize_blobs(orig_txt, txt):
    """after deletions: every blob's data must sit at its first occurrence in document order (and only there)"""
    data = {}
    for m in BLOB.finditer(orig_txt):
        if m.group(4) != '/>' and m.group(5): data.setdefault(m.group(3), m.group(5))
    seen, edits = set(), []
    for m in BLOB.finditer(txt):
        h = m.group(3); inline = m.group(4) != '/>'
        if h not in seen:
            seen.add(h)
            if not inline and h in data:
                edits.append((m.start(), m.end(), '<%s%s>%s</%s>' % (m.group(1), m.group(2), data[h], m.group(1))))
        elif inline:
            edits.append((m.start(), m.end(), '<%s%s/>' % (m.group(1), m.group(2))))
    for s, e, rep in sorted(edits, reverse=True):
        txt = txt[:s] + rep + txt[e:]
    return txt, len(edits)


# ---------------------------------------------------------------- build
def build(src_xml, v3_xml, out_path, log=print):
    doc = Doc(src_xml)
    orig_txt = doc.txt
    v3 = Doc(v3_xml)
    report = {'ads': {}}
    # 1. media + bin
    masters, new_media_objs = {}, []
    for k, path in ext_plan.MEDIA.items():
        assert os.path.exists(path), path
        masters[k], objs = media_objects(doc, path)
        new_media_objs += objs
    bin_uid, bin_txt = bin_object(doc, BIN_NAME, [masters[k]['cpi_uid'] for k in ext_plan.MEDIA])
    body = doc.txt.rstrip()
    assert body.endswith('</PremiereData>')
    doc.txt = body[:-len('</PremiereData>')].rstrip('\n') + '\n' + '\n'.join(new_media_objs + [bin_txt]) + '\n</PremiereData>\n'
    log('imported %d external clips into bin "%s"' % (len(masters), BIN_NAME))
    # 2. per ad
    seqs = {s.attrib['ObjectUID'][:8]: (n, s) for n, s in for_claude_sequences(doc)}
    new_objs = []
    for key, (name, seq) in seqs.items():
        adds = ext_plan.ADD.get(key, []); rems = [r[1] for r in ext_plan.REMOVE if r[0] == key]
        if not adds and not rems: continue
        trs = video_tracks(doc, seq)
        v1 = track_items(doc, trs[0])
        cut_ticks = sorted({int(t.findtext('.//TrackItem/Start') or 0) for t in v1} | {int(t.findtext('.//TrackItem/End')) for t in v1})
        seq_end = max(int(t.findtext('.//TrackItem/End')) for t in v1)

        def snap(sec):
            tk = sec * TPS
            for c in cut_ticks:
                if abs(c - tk) < 0.021 * TPS: return c
            return int(round(tk / F60)) * F60
        btr, gtr = (trs[3], trs[4]) if key == REF else (trs[1], trs[2])
        b_items = [t.attrib['ObjectID'] for t in track_items(doc, btr)]
        g_items = [t.attrib['ObjectID'] for t in track_items(doc, gtr)]
        tmpl_b = b_items[0]
        # remove camera B-roll shots
        keep, removed = [], []
        for bid in b_items:
            s, e, _, _ = item_times(doc, bid)
            if any(abs(s - r * TPS) < 0.02 * TPS for r in rems): removed.append((bid, s, e))
            else: keep.append(bid)
        assert len(removed) == len(rems), (name, rems, removed)
        # new external shots (template B-roll item captured before any deletion)
        added = []
        for it in sorted(adds, key=lambda d: d['t0']):
            a, b = snap(it['t0']), min(snap(it['t1']), seq_end)
            mi = masters[it['media']]['info']
            fr = mi['fr']
            src_in = int(round(it['src'] * TPS / fr)) * fr
            assert src_in + (b - a) <= mi['dur'], ('source too short', it)
            s = it['scale'] / 100.0
            px = (540 - (it['cx'] * mi['w'] - mi['w'] / 2) * s) / 1080
            lov = dict(NEUTRAL); lov.update(GRADE[it['media']])
            nti, objs = ext_item(doc, tmpl_b, masters[it['media']], a, b, src_in, px, 0.5, it['scale'], lov)
            new_objs += objs; added.append((nti, a, b))
        for bid, s, e in removed: delete_item(doc, bid)
        b_all = sorted([(item_times(doc, x)[0], x) for x in keep] + [(a, x) for x, a, b in added])
        intervals = sorted([item_times(doc, x)[:2] for x in keep] + [(a, b) for x, a, b in added])
        for (a1, b1), (a2, b2) in zip(intervals, intervals[1:]): assert b1 <= a2, ('overlap', name, a1 / TPS, b1 / TPS, a2 / TPS)
        # grade: desired pieces per original item, re-using existing piece objects of the same item
        originals = original_grade_items(v3, key)
        pieces_by_sig = {}
        for gid in g_items:
            pieces_by_sig.setdefault(chain_signature(doc, gid), []).append(gid)
        final_g = []
        for s0, e0, sig in originals:
            want = subtract(s0, e0, intervals)
            pool = sorted(pieces_by_sig.get(sig, []), key=lambda x: item_times(doc, x)[0])
            assert pool, ('no grade piece for', name, sig)
            tmpl = pool[0]
            used = set()
            for p, q in want:
                best = None
                for gid in pool:
                    if gid in used: continue
                    s, e, _, _ = item_times(doc, gid)
                    ov = min(e, q) - max(s, p)
                    if s0 <= s < e0 and (best is None or ov > best[0]): best = (ov, gid)
                if best and best[0] > 0:
                    gid = best[1]; used.add(gid)
                    s, e, _, _ = item_times(doc, gid)
                    if (s, e) != (p, q): retime_item(doc, gid, p, q)
                    final_g.append((p, gid))
                else:
                    nti, objs = clone_item(doc, tmpl, p, q)
                    new_objs += objs; final_g.append((p, nti))
            for gid in pool:
                s, e, _, _ = item_times(doc, gid)
                if gid not in used and s0 <= s < e0:
                    delete_item(doc, gid)
        final_g.sort()
        set_track_items(doc, btr.attrib['ObjectUID'], [x for _, x in b_all])
        pending = (gtr.attrib['ObjectUID'], [x for _, x in final_g])
        cover = sum(b - a for a, b in intervals) / seq_end
        report['ads'][key] = dict(name=seq.findtext('Name'), broll=[(round(a / TPS, 3), round(b / TPS, 3)) for a, b in intervals],
                                  grade=len(final_g), coverage=round(cover * 100, 1),
                                  added=[(it['media'], round(snap(it['t0']) / TPS, 3), round(min(snap(it['t1']), seq_end) / TPS, 3)) for it in adds],
                                  removed=[(round(s / TPS, 3), round(e / TPS, 3)) for _, s, e in removed])
        report['ads'][key]['_pending'] = pending
        log('%-45s +%d external, -%d camera shots, B-roll %.0f%% of %.1fs, grade in %d pieces'
            % (seq.findtext('Name')[:45], len(added), len(removed), cover * 100, seq_end / TPS, len(final_g)))
    body = doc.txt.rstrip()
    doc.txt = body[:-len('</PremiereData>')].rstrip('\n') + '\n' + '\n'.join(new_objs) + '\n</PremiereData>\n'
    for key, r in report['ads'].items():
        uid, ids = r.pop('_pending')
        set_track_items(doc, uid, ids)       # grade track lists are set last (cloned pieces now exist in the text)
    doc.txt, nfix = normalize_blobs(orig_txt, doc.txt)
    log('blob data moved/deduplicated at %d places' % nfix)
    xml_out = out_path + '.xml'
    open(xml_out, 'w', encoding='utf-8', newline='\n').write(doc.txt)
    with open(xml_out, 'rb') as f, gzip.open(out_path, 'wb') as g: g.write(f.read())
    report['masters'] = {k: dict(name=m['name'], mc=m['mc_uid'], **{kk: vv for kk, vv in m['info'].items()}) for k, m in masters.items()}
    return xml_out, report


if __name__ == '__main__':
    x, rep = build(sys.argv[1], sys.argv[2], sys.argv[3])
    json.dump(rep, open(sys.argv[3] + '.report.json', 'w'), indent=1)
