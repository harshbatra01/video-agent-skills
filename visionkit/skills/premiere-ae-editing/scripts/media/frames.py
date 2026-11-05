"""See video without watching it: exact frames and labelled contact sheets with PyAV (no ffmpeg CLI on this PC).

usage:
  python frames.py info FILE [FILE ...]                         codec, size, fps, frames, duration, audio
  python frames.py sheet OUT.png FILE "label@sec" ... [--cols 4] [--w 480]
        frames at exact times, labelled "label m:ss.ss"; an argument without @ is a time with no label
  python frames.py even OUT.png N FILE [FILE ...] [--w 320]     N evenly spaced frames per file, one row per file
  python frames.py grab FILE SEC OUT.png                        one full-resolution frame
  python frames.py dupes A.png B.png ...                        md5 of the pixels: flags identical frames
        (Premiere's Export Frame can silently repeat the previous frame when exports overlap)

Why sheets: one downscaled labelled sheet answers a question in a single image read instead of ten.
Seeking: jumps to the keyframe before t, decodes forward to the first frame at or after t (half a frame tolerance).
"""
import sys, os, hashlib, argparse
import av
from PIL import Image, ImageDraw, ImageFont


# macOS (from the Mac port, Oct 2026): label fonts are tried by their full macOS paths first (the paths the Mac port
# used); Windows uses the same font names as before.
MAC_FONTS = ('/System/Library/Fonts/Supplemental/Arial Bold.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf',
             '/System/Library/Fonts/Helvetica.ttc')


def _font(size):
    for f in (MAC_FONTS if sys.platform == 'darwin' else ()) + ('arialbd.ttf', 'arial.ttf', 'segoeui.ttf'):
        try: return ImageFont.truetype(f, size)
        except OSError: pass
    return ImageFont.load_default()


def info(path):
    c = av.open(path)
    try:
        out = dict(file=os.path.basename(path), duration=round(float(c.duration or 0) / 1e6, 3))
        if c.streams.video:
            v = c.streams.video[0]
            out.update(codec=v.codec_context.name, w=v.width, h=v.height, fps=round(float(v.average_rate or 0), 3),
                       frames=v.frames, pix=v.format.name if v.format else None)
        if c.streams.audio:
            a = c.streams.audio[0]
            out.update(audio='%s %d Hz %d ch' % (a.codec_context.name, a.rate, a.channels))
        return out
    finally:
        c.close()


class Grabber:
    def __init__(self, path):
        self.c = av.open(path); self.v = self.c.streams.video[0]; self.tb = self.v.time_base
        self.half = 0.5 / float(self.v.average_rate or 30)

    def at(self, t):
        self.c.seek(int(max(0.0, t - 1.5) / self.tb), stream=self.v, backward=True)
        last = None
        for fr in self.c.decode(self.v):
            if fr.pts is not None and fr.pts * self.tb >= t - self.half: return fr.to_image()
            last = fr
        return last.to_image() if last else None

    def close(self): self.c.close()


def sheet(out, path, items, cols=4, tw=480):
    g = Grabber(path); ims = []
    for it in items:
        lab, t = it.rsplit('@', 1) if '@' in it else ('', it)
        t = float(t); im = g.at(t)
        if im is not None: ims.append((('%s %d:%05.2f' % (lab, int(t // 60), t % 60)).strip(), im.convert('RGB')))
    g.close()
    if not ims: sys.exit('no frames')
    w0, h0 = ims[0][1].size; th = int(round(tw * h0 / w0))
    rows = (len(ims) + cols - 1) // cols; font = _font(15)
    S = Image.new('RGB', (cols * tw, rows * th), (20, 20, 20)); d = ImageDraw.Draw(S)
    for i, (lab, im) in enumerate(ims):
        x, y = (i % cols) * tw, (i // cols) * th
        S.paste(im.resize((tw, th)), (x, y))
        if lab: d.rectangle([x, y, x + 9 * len(lab) + 6, y + 20], fill=(0, 0, 0)); d.text((x + 3, y + 1), lab, fill=(255, 220, 0), font=font)
    S.save(out); print(out, S.size, len(ims), 'frames')


def even(out, n, files, tw=320):
    rows = []
    for f in files:
        meta = info(f); dur = meta['duration'] or 1.0
        g = Grabber(f)
        ims = [g.at(dur * (k + 0.5) / n) for k in range(n)]
        g.close()
        rows.append(('%s  %sx%s %s fps %.2f s %s' % (meta['file'], meta.get('w'), meta.get('h'), meta.get('fps'), dur, meta.get('codec')), [i for i in ims if i is not None]))
    w0, h0 = rows[0][1][0].size; th = int(round(tw * h0 / w0)); font = _font(13)
    S = Image.new('RGB', (n * tw, len(rows) * (th + 18)), (30, 30, 30)); d = ImageDraw.Draw(S)
    for r, (lab, ims) in enumerate(rows):
        y = r * (th + 18); d.text((3, y + 2), lab, fill=(255, 220, 0), font=font)
        for k, im in enumerate(ims): S.paste(im.convert('RGB').resize((tw, th)), (k * tw, y + 18))
    S.save(out); print(out, S.size)


def main():
    if len(sys.argv) < 2: sys.exit(__doc__)
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == 'info':
        for f in rest: print(info(f))
    elif cmd == 'sheet':
        ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('file'); ap.add_argument('items', nargs='+')
        ap.add_argument('--cols', type=int, default=4); ap.add_argument('--w', type=int, default=480); a = ap.parse_args(rest)
        sheet(a.out, a.file, a.items, a.cols, a.w)
    elif cmd == 'even':
        ap = argparse.ArgumentParser(); ap.add_argument('out'); ap.add_argument('n', type=int); ap.add_argument('files', nargs='+')
        ap.add_argument('--w', type=int, default=320); a = ap.parse_args(rest)
        even(a.out, a.n, a.files, a.w)
    elif cmd == 'grab':
        g = Grabber(rest[0]); im = g.at(float(rest[1])); g.close(); im.save(rest[2]); print(rest[2], im.size)
    elif cmd == 'dupes':
        seen = {}
        for f in rest:
            h = hashlib.md5(Image.open(f).convert('RGB').tobytes()).hexdigest()
            print('%s %s%s' % (h[:10], os.path.basename(f), ('  DUPLICATE of ' + seen[h]) if h in seen else ''))
            seen.setdefault(h, os.path.basename(f))
    else:
        sys.exit(__doc__)


if __name__ == '__main__':
    main()
