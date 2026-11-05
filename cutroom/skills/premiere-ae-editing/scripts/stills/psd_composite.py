"""Minimal PSD reader: flattened composite (Image Data section) + layer names/bounds. No psd-tools needed.
usage: from psd_composite import read_psd -> (PIL.Image, [layer dicts])"""
import struct
from PIL import Image


def packbits(data, n):
    out = bytearray(); i = 0
    while len(out) < n and i < len(data):
        h = data[i]; i += 1
        if h < 128: out += data[i:i + h + 1]; i += h + 1
        elif h > 128: out += bytes([data[i]]) * (257 - h); i += 1
    return bytes(out[:n])


def read_psd(path):
    b = open(path, 'rb').read()
    sig, ver = b[:4], struct.unpack('>H', b[4:6])[0]
    assert sig == b'8BPS', 'not a PSD'
    ch, h, w, depth, mode = struct.unpack('>HIIHH', b[12:26])
    p = 26
    n = struct.unpack('>I', b[p:p + 4])[0]; p += 4 + n          # colour mode data
    n = struct.unpack('>I', b[p:p + 4])[0]; p += 4 + n          # image resources
    lm_len = struct.unpack('>I' if ver == 1 else '>Q', b[p:p + (4 if ver == 1 else 8)])[0]
    lm_start = p + (4 if ver == 1 else 8)
    layers = []
    try:
        q = lm_start
        li_len = struct.unpack('>I' if ver == 1 else '>Q', b[q:q + (4 if ver == 1 else 8)])[0]; q += 4 if ver == 1 else 8
        if li_len:
            cnt = abs(struct.unpack('>h', b[q:q + 2])[0]); q += 2
            for _ in range(cnt):
                t, l, bt, r = struct.unpack('>iiii', b[q:q + 16]); q += 16
                nch = struct.unpack('>H', b[q:q + 2])[0]; q += 2
                q += nch * (6 if ver == 1 else 10)
                q += 4  # 8BIM
                blend = b[q:q + 4].decode('latin1'); q += 4
                opacity, clip, flags = b[q], b[q + 1], b[q + 2]; q += 4
                extra = struct.unpack('>I', b[q:q + 4])[0]; q += 4
                e = q
                mlen = struct.unpack('>I', b[e:e + 4])[0]; e += 4 + mlen
                blen = struct.unpack('>I', b[e:e + 4])[0]; e += 4 + blen
                nlen = b[e]; name = b[e + 1:e + 1 + nlen].decode('latin1', 'ignore')
                # unicode name (luni) if present
                k = b.find(b'8BIMluni', e, q + extra)
                if k > 0:
                    ul = struct.unpack('>I', b[k + 12:k + 16])[0]
                    name = b[k + 16:k + 16 + ul * 2].decode('utf-16-be', 'ignore')
                kind = 'group-end' if b.find(b'8BIMlsct', e, q + extra) > 0 and name == '</Layer group>' else ''
                for key, label in ((b'TySh', 'text'), (b'SoLd', 'smart'), (b'SoLE', 'smart'), (b'vmsk', 'shape'), (b'vsms', 'shape'), (b'lsct', 'group')):
                    if b.find(b'8BIM' + key, e, q + extra) > 0: kind = kind or label
                layers.append(dict(name=name, box=(l, t, r, bt), blend=blend, opacity=opacity, hidden=bool(flags & 2), kind=kind))
                q += extra
    except Exception as ex:
        layers.append(dict(name='(layer parse stopped: %s)' % ex))
    p = lm_start + lm_len
    comp = struct.unpack('>H', b[p:p + 2])[0]; p += 2
    planes = []
    if comp == 0:
        size = w * h * (depth // 8)
        for c in range(ch): planes.append(b[p + c * size:p + (c + 1) * size])
    elif comp == 1:
        cntsz = 2 if ver == 1 else 4
        counts = [struct.unpack('>H' if ver == 1 else '>I', b[p + i * cntsz:p + (i + 1) * cntsz])[0] for i in range(ch * h)]
        p += ch * h * cntsz
        for c in range(ch):
            rows = []
            for r in range(h):
                n = counts[c * h + r]; rows.append(packbits(b[p:p + n], w)); p += n
            planes.append(b''.join(rows))
    else:
        raise ValueError('compression %d' % comp)
    if depth != 8: raise ValueError('depth %d' % depth)
    if mode == 3 and ch >= 3:
        bands = [Image.frombytes('L', (w, h), planes[i]) for i in range(3)]
        im = Image.merge('RGB', bands)
        if ch >= 4:
            a = Image.frombytes('L', (w, h), planes[3]); im = Image.merge('RGBA', bands + [a])
    elif mode == 1:
        im = Image.frombytes('L', (w, h), planes[0])
    else:
        raise ValueError('mode %d' % mode)
    return im, layers


if __name__ == '__main__':
    import sys
    im, layers = read_psd(sys.argv[1])
    print(im.size, im.mode)
    for L in layers: print(L)
