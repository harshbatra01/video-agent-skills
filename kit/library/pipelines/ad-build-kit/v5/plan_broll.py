"""v5 archive B-roll placements. Times: sequence seconds; src: source seconds; xs: subject x (0-1) to centre; zoom: extra scale factor."""
YT = r"C:\VISION\IMMUFIX\repair\ENCODED RUSHES\YT FOOTAGE\YT FOOTAGE MORE" + "\\"
SRC = {  # key: (file, w, h, fps)
    'STARS': ('Paula Radcliffe Chasing Stars_1080p.mp4', 1920, 1080, 23.976),
    'THANK': ('Thank you Paula the London Marathon salutes one of its greatest champions_1080p.mp4', 1920, 1080, 25),
    'TWS01': ('Young Paula Radcliffe in 2001!  On Running Style, Sydney Olympics and More!  Trans World Sport_1080p.mp4', 1920, 1080, 25),
    'MOTIV': ('Best of motivation distance running, Paula Radcliffe  !_720p.mp4', 1280, 720, 29.97),
    'MAR98': ('1998 IAAF World Cross Country Champs Marrakesh - Senior Womens Highlights_720p.mp4', 1280, 720, 29.97),
}
# (ad, start, end, key, src_in, xs, zoom, label)
PLAN = [
    # People are always surprised (664b35b2)
    ('664b35b2', 2.03, 2.75, 'STARS', 1097.26, 0.53, 1.0, 'dress look-back'),
    ('664b35b2', 2.75, 3.83, 'THANK', 160.20, 0.50, 1.0, 'London 2003 arms out'),
    ('664b35b2', 3.83, 4.85, 'THANK', 196.40, 0.47, 1.0, 'Tower Bridge 2003'),
    ('664b35b2', 4.85, 5.93, 'STARS', 413.80, 0.50, 1.0, 'Chicago 2002 close'),
    ('664b35b2', 5.93, 7.52, 'MOTIV', 7.60, 0.50, 1.0, 'red vest racing (90%)'),
    ('664b35b2', 7.52, 8.38, 'STARS', 1113.80, 0.50, 1.0, 'heels'),
    ('664b35b2', 8.38, 9.25, 'STARS', 1138.00, 0.38, 1.0, 'gala talk'),
    ('664b35b2', 9.25, 9.82, 'STARS', 2024.00, 0.45, 1.0, 'London stage mic'),
    ('664b35b2', 9.82, 10.45, 'STARS', 1473.70, 0.60, 1.0, 'Boston stage mic'),
    ('664b35b2', 11.62, 12.21, 'STARS', 556.50, 0.38, 1.0, 'Tokyo talk'),
    ('664b35b2', 12.21, 13.57, 'STARS', 1326.30, 0.38, 1.0, 'with Joan Benoit Samuelson'),
    ('664b35b2', 13.57, 15.48, 'THANK', 126.20, 0.52, 1.0, 'fan photo'),
    ('664b35b2', 20.72, 21.80, 'MAR98', 20.10, 0.45, 1.0, '1998 age 24'),
    # I held the record / ready to recover (404c5cb2)
    ('404c5cb2', 2.67, 3.55, 'MOTIV', 14.00, 0.50, 1.0, 'racing grind'),
    ('404c5cb2', 3.55, 4.72, 'STARS', 426.60, 0.50, 1.0, 'bent over after Chicago'),
    ('404c5cb2', 4.72, 5.63, 'TWS01', 106.00, 0.50, 1.0, 'grass training sprinklers'),
    ('404c5cb2', 5.63, 6.67, 'TWS01', 201.00, 0.45, 1.0, 'track training close'),
    ('404c5cb2', 10.52, 11.32, 'THANK', 16.70, 0.50, 1.0, 'London 2003 finish clock'),
    ('404c5cb2', 19.36, 20.90, 'STARS', 997.20, 0.55, 1.0, 'pool recovery'),
    ('404c5cb2', 23.55, 25.77, 'STARS', 958.60, 0.50, 1.0, 'trail run'),
    # Ran professionally (0991faf2)
    ('0991faf2', 6.68, 8.18, 'THANK', 32.00, 0.50, 1.0, 'mass start'),
    ('0991faf2', 24.78, 26.10, 'STARS', 466.60, 0.47, 1.0, 'running with her kids'),
    # Secret weapon (593f11c4)
    ('593f11c4', 12.35, 14.30, 'TWS01', 218.00, 0.50, 1.0, 'track training with partner'),
    ('593f11c4', 14.30, 15.40, 'TWS01', 289.00, 0.45, 1.0, 'Ostend lead'),
    ('593f11c4', 15.40, 16.48, 'TWS01', 293.90, 0.42, 1.0, 'Ostend tape'),
    # I'm 52 (348e0ba6)
    ('348e0ba6', 12.68, 13.40, 'THANK', 160.60, 0.50, 1.0, 'career: London 2003'),
    ('348e0ba6', 15.96, 17.05, 'MAR98', 20.10, 0.45, 1.0, '1998 age 24'),
]


def motion(key, xs, zoom):
    f, w, h, fps = SRC[key]
    sc = 1920.0 / h * 100 * zoom
    wd = w * sc / 100
    px = (540 - (xs - 0.5) * wd) / 1080
    lo, hi = (1080 - wd / 2) / 1080, (wd / 2) / 1080    # keep the frame covered
    return round(min(max(px, lo), hi), 5), 0.5, round(sc, 3)
