"""Colour-space settings of the media whose path contains a needle (VideoStream override fields)."""
import re, sys, ntpath


def media_info(path, needle):
    t = open(path, encoding='utf-8').read()
    out = []
    for m in re.finditer(r'<Media ObjectUID="([^"]+)"[^>]*>(.*?)</Media>', t, re.S):
        body = m.group(2)
        fp = re.search(r'<FilePath>([^<]*)</FilePath>', body)
        if not fp or needle not in fp.group(1): continue
        vs = re.search(r'<VideoStream ObjectRef="(\d+)"', body)
        vraw = ''
        if vs:
            s = t.index('<VideoStream ObjectID="%s"' % vs.group(1)); e = t.index('</VideoStream>', s); vraw = t[s:e]
        keys = {}
        for k in ('IsColorSpacOverridden', 'InputLUTSpecified', 'FrameRate', 'CodecType'):
            mm = re.search(r'<%s>([^<]*)</%s>' % (k, k), vraw); keys[k] = mm.group(1) if mm else None
        ocs = re.search(r'<OverriddenColorSpace[^>]*>(.*?)</OverriddenColorSpace>', vraw, re.S)
        orig = re.search(r'<OriginalColorSpace[^>]*>(.*?)</OriginalColorSpace>', vraw, re.S)
        out.append(dict(file=ntpath.basename(fp.group(1)), media_uid=m.group(1), vs=vs.group(1) if vs else None, keys=keys,
                        override=ocs.group(1) if ocs else None, original=orig.group(1) if orig else None, vraw_len=len(vraw)))
    return out


if __name__ == '__main__':
    for p, n in [a.split(':') for a in sys.argv[1:]]:
        for r in media_info(p, n):
            print(p, r['file'][:64], r['keys'], 'vs', r['vs'])
            print('    override:', (r['override'] or 'NONE')[:260].replace('\n', ' '))
            print('    original:', (r['original'] or 'NONE')[:160].replace('\n', ' '))
