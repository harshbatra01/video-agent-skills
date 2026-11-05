"""Check rendered MP4s: duration, size, frame count, fps (from the MP4 atoms) + loudness / true peak (VLC -> WAV).
usage: python verify_renders.py <folder> [--noaudio]"""
import os, struct, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atools

CONTAINERS = {b'moov', b'trak', b'mdia', b'minf', b'stbl'}


def atoms(f, start, end):
    pos = start
    while pos + 8 <= end:
        f.seek(pos)
        size, typ = struct.unpack('>I4s', f.read(8)); hdr = 8
        if size == 1: size = struct.unpack('>Q', f.read(8))[0]; hdr = 16
        elif size == 0: size = end - pos
        yield typ, pos + hdr, pos + size
        pos += size


def mp4_info(path):
    out = {'tracks': []}
    with open(path, 'rb') as f:
        f.seek(0, 2); n = f.tell()

        def walk(s, e, trk):
            for typ, a, b in atoms(f, s, e):
                if typ in CONTAINERS:
                    if typ == b'trak':
                        t = {}; walk(a, b, t); out['tracks'].append(t)
                    else: walk(a, b, trk)
                elif typ == b'mvhd':
                    f.seek(a); v = f.read(1)[0]; f.seek(a + (20 if v else 12))
                    ts = struct.unpack('>I', f.read(4))[0]; du = struct.unpack('>Q' if v else '>I', f.read(8 if v else 4))[0]
                    out['duration'] = du / ts
                elif typ == b'tkhd':
                    f.seek(b - 8); w, h = struct.unpack('>II', f.read(8)); trk['wh'] = (w >> 16, h >> 16)
                elif typ == b'mdhd':
                    f.seek(a); v = f.read(1)[0]; f.seek(a + (20 if v else 12))
                    ts = struct.unpack('>I', f.read(4))[0]; du = struct.unpack('>Q' if v else '>I', f.read(8 if v else 4))[0]
                    trk['ts'] = ts; trk['dur'] = du / ts
                elif typ == b'hdlr':
                    f.seek(a + 8); trk.setdefault('kind', f.read(4).decode('latin1'))  # minf has a second (data) hdlr
                elif typ == b'stsz':
                    f.seek(a + 8); trk['samples'] = struct.unpack('>I', f.read(4))[0]
        walk(0, n, None)
    out['size_mb'] = os.path.getsize(path) / 1e6
    return out


if __name__ == '__main__':
    folder = sys.argv[1]; noaudio = '--noaudio' in sys.argv
    res = {}
    for name in sorted(os.listdir(folder)):
        if not name.lower().endswith('.mp4'): continue
        p = os.path.join(folder, name); info = mp4_info(p)
        line = '%-42s %7.3f s  %6.1f MB' % (name[:42], info.get('duration', 0), info['size_mb'])
        for t in info['tracks']:
            if t.get('kind') == 'vide':
                line += '  video %dx%d %d frames %.2f fps' % (t['wh'][0], t['wh'][1], t['samples'], t['samples'] / t['dur'])
        if not noaudio:
            wav = 'vr_tmp.wav'  # relative: VLC's sout parser eats backslashes
            if os.path.exists(wav): os.remove(wav)
            atools.extract_wav(os.path.abspath(p), wav)
            x, sr = atools.load_wav(wav)
            info['lufs'] = atools.lufs(x, sr); info['tp'] = atools.true_peak_db(x)
            info['audio_s'] = len(x) / sr
            line += '  %.1f LUFS  TP %+.1f dBTP  audio %.2f s' % (info['lufs'], info['tp'], info['audio_s'])
        print(line, flush=True)
        res[name] = info
    json.dump(res, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'verify_%s.json' % os.path.basename(folder.rstrip('/\\'))), 'w'), indent=1, default=str)
