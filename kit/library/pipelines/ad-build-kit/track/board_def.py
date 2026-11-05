"""reference frame + board/line geometry for the 3 things whiteboard (1512x852 source/4 coords)"""
import numpy as np
REF_FRAME = 'tt_frames/p0_3004/f_03042.tif'      # source frame 3042 (seq ~1.48 s)
BOARD = [(488, 213), (746, 204), (808, 585), (529, 611)]          # outer wooden frame TL, TR, BR, BL
EXCLUDE = [((765, 288), (845, 412)), ((486, 386), (528, 446))]     # her hands on the board edges in the reference
# rotated text-line boxes: (cx, cy, w, h, angle_deg)
LINES = {
    'L1':  (611.5, 273.0, 236, 58, -4.0),
    'L2a': (617.5, 338.5, 232, 56, -4.0),
    'L2b': (597.0, 375.0, 160, 46, -3.0),
    'L3a': (643.0, 421.5, 258, 56, -4.0),
    'L3b': (609.0, 466.0, 164, 50, -3.0),
}


def box_corners(cx, cy, w, h, ang):
    a = np.deg2rad(ang); c, s = np.cos(a), np.sin(a)
    pts = np.array([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, h / 2], [-w / 2, h / 2]])
    return pts @ np.array([[c, s], [-s, c]]) + [cx, cy]


def region_mask(shape, grow=6):
    """template pixels: board quad grown a little (frame edges), minus the hands"""
    from PIL import Image, ImageDraw
    q = np.array(BOARD, float); c = q.mean(0); q = c + (q - c) * (1 + grow / 150.0)
    im = Image.new('L', (shape[1], shape[0]), 0); d = ImageDraw.Draw(im)
    d.polygon([tuple(p) for p in q], fill=255)
    for (x0, y0), (x1, y1) in EXCLUDE: d.rectangle([x0, y0, x1, y1], fill=0)
    return np.asarray(im) > 0
