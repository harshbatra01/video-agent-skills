"""All tracks of an MP4: handler, timescale, duration, sample count, first sample delta, video size / audio rate+channels, keyframes."""
import struct, os, sys, json
CONTAINERS = {b'moov', b'trak', b'mdia', b'minf', b'stbl', b'edts', b'dinf'}


def boxes(f, start, end):
    pos = start
    while pos + 8 <= end:
        f.seek(pos); hdr = f.read(8)
        if len(hdr) < 8: break
        size, typ = struct.unpack('>I4s', hdr); hl = 8
        if size == 1: size = struct.unpack('>Q', f.read(8))[0]; hl = 16
        elif size == 0: size = end - pos
        if size < 8: break
        yield typ, pos, pos + hl, pos + size
        pos += size


def info(path):
    res = {'file': path, 'size': os.path.getsize(path), 'mtime': os.path.getmtime(path), 'tracks': []}
    with open(path, 'rb') as f:
        f.seek(0, 2); end = f.tell()
        moov = [b for b in boxes(f, 0, end) if b[0] == b'moov'][0]
        for t in boxes(f, moov[2], moov[3]):
            if t[0] == b'mvhd':
                f.seek(t[2]); v = f.read(1)[0]
                if v == 1: f.seek(t[2] + 4 + 16); ts, dur = struct.unpack('>IQ', f.read(12))
                else: f.seek(t[2] + 4 + 8); ts, dur = struct.unpack('>II', f.read(8))
                res['movie_ts'], res['movie_dur'] = ts, dur
            if t[0] != b'trak': continue
            tr = {}

            def walk(s, e):
                for typ, p, ds, de in boxes(f, s, e):
                    if typ in CONTAINERS: walk(ds, de)
                    elif typ == b'tkhd':
                        f.seek(ds); v = f.read(1)[0]
                        f.seek(de - 8); w, h = struct.unpack('>II', f.read(8)); tr['tkhd_wh'] = (w / 65536, h / 65536)
                        f.seek(ds + (40 if v == 1 else 40 - 0))  # matrix position differs; read matrix explicitly below
                        mpos = ds + (4 + 8 + 8 + 4 + 4 + 8 + 8 + 2 + 2 + 2 + 2 if v == 1 else 4 + 4 + 4 + 4 + 4 + 4 + 8 + 2 + 2 + 2 + 2)
                        f.seek(mpos); tr['matrix'] = struct.unpack('>9i', f.read(36))
                    elif typ == b'elst':
                        f.seek(ds); v = f.read(1)[0]; f.seek(ds + 4); n = struct.unpack('>I', f.read(4))[0]
                        ents = []
                        for _ in range(n):
                            if v == 1: d, mt = struct.unpack('>Qq', f.read(16))
                            else: d, mt = struct.unpack('>Ii', f.read(8))
                            f.read(4); ents.append((d, mt))
                        tr['elst'] = ents
                    elif typ == b'hdlr':
                        f.seek(ds + 8); tr.setdefault('handler', f.read(4).decode('latin1'))
                    elif typ == b'mdhd':
                        f.seek(ds); v = f.read(1)[0]
                        if v == 1: f.seek(ds + 4 + 16); ts, dur = struct.unpack('>IQ', f.read(12))
                        else: f.seek(ds + 4 + 8); ts, dur = struct.unpack('>II', f.read(8))
                        tr['timescale'] = ts; tr['duration'] = dur
                    elif typ == b'stsd':
                        f.seek(ds + 8); sz, fmt = struct.unpack('>I4s', f.read(8)); tr['codec'] = fmt.decode('latin1')
                        base = ds + 8 + 8
                        if tr.get('handler') == 'vide':
                            f.seek(base + 6 + 2 + 16); w, h = struct.unpack('>HH', f.read(4)); tr['wh'] = (w, h)
                        elif tr.get('handler') == 'soun':
                            f.seek(base + 6 + 2 + 8); ch, bits = struct.unpack('>HH', f.read(4)); f.read(4)
                            rate = struct.unpack('>I', f.read(4))[0] >> 16; tr['channels'] = ch; tr['rate'] = rate
                    elif typ == b'stss':
                        f.seek(ds + 4); n = struct.unpack('>I', f.read(4))[0]
                        tr['stss'] = list(struct.unpack('>%dI' % n, f.read(4 * n)))
                    elif typ == b'stsz':
                        f.seek(ds + 4); ss, n = struct.unpack('>II', f.read(8)); tr['nsamples'] = n
                    elif typ == b'stts':
                        f.seek(ds + 4); n = struct.unpack('>I', f.read(4))[0]
                        tr['stts'] = [struct.unpack('>II', f.read(8)) for _ in range(min(n, 50))]; tr['stts_n'] = n
            walk(t[2], t[3])
            res['tracks'].append(tr)
    return res


if __name__ == '__main__':
    for p in sys.argv[1:]:
        r = info(p)
        print('==', os.path.basename(p), r['size'], 'movie', r.get('movie_dur'), '/', r.get('movie_ts'))
        for tr in r['tracks']:
            d = {k: v for k, v in tr.items() if k not in ('stss',)}
            if 'stss' in tr: d['nkey'] = len(tr['stss']); d['key0'] = tr['stss'][:6]
            print('   ', d)
