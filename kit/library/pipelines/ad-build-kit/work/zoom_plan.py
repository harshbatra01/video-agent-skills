"""Zoom segments per ad (seconds; boundaries snap to V1 cuts / B-roll ends in the builder).
Grammar copied from the user's reference (Sequence 04, V3):
  intro : quick ease-out from Q% (0.87 s) x slow drift D% -> 100 over the segment   (reference: 120 x 110)
  push  : quick eased punch 100 -> P% (1.13 s) x linear slow push 100 -> 100 + rate*dur
  pull  : quick ease-out P% -> 100 (1.12 s) x linear drift (end of previous slow push) -> 100
Zoom level is continuous across every boundary (pull starts where the push ended), like the reference.
Boundaries sit where the talking head comes back from B-roll or at sentence starts, so each move is seen;
pushes run into B-roll cuts (e.g. into the London archive), pulls land after them.
anchor: Transform anchor = position (fraction of frame), set near Paula's face so she stays framed when zoomed."""
DEFAULT = dict(anchor=(0.5, 0.33), punch=110.0, intro=(115.0, 108.0))
GENTLE = dict(anchor=(0.40, 0.35), punch=104.0, intro=(104.0, 103.0))     # whiteboard ad: keep the board in frame

ZOOM = {
    # I held the record: every return from B-roll gets a move
    '404c5cb2': dict(DEFAULT, segs=[('intro', 0.0, 2.667), ('push', 2.667, 6.667, 1.8), ('pull', 6.667, 13.033),
                                    ('push', 13.033, 18.05, 1.6), ('pull', 18.05, 23.55), ('push', 23.55, None, 1.5)]),
    # People are always surprised
    '664b35b2': dict(DEFAULT, segs=[('intro', 0.0, 5.933), ('push', 5.933, 11.617, 1.6), ('pull', 11.617, 18.267),
                                    ('push', 18.267, 21.80, 1.8), ('pull', 21.80, None)]),
    # ran professionally: push into the London archive, land after it
    '0991faf2': dict(DEFAULT, segs=[('intro', 0.0, 2.183), ('push', 2.183, 5.767, 1.8), ('pull', 5.767, 10.783),
                                    ('push', 10.783, 14.183, 2.0), ('pull', 14.183, 21.483), ('push', 21.483, 24.783, 2.0),
                                    ('pull', 24.783, None)]),
    # 1 star reviews
    'cd03e189': dict(DEFAULT, segs=[('intro', 0.0, 2.883), ('push', 2.883, 8.067, 1.7), ('pull', 8.067, 13.867),
                                    ('push', 13.867, None, 1.3)]),
    # 3 questions: a push on each question, a pull as each answer lands
    '974102f7': dict(DEFAULT, segs=[('intro', 0.0, 3.617), ('push', 3.617, 6.917, 2.0), ('pull', 6.917, 16.133),
                                    ('push', 16.133, 23.033, 1.5), ('pull', 23.033, 29.617), ('push', 29.617, 35.033, 1.5),
                                    ('pull', 35.033, 41.583), ('push', 41.583, None, 1.5)]),
    # 3 things to check: gentle, anchored left of centre so the whiteboard never gets cropped
    'f233433f': dict(GENTLE, segs=[('intro', 0.0, 3.60), ('push', 3.60, 13.183, 0.25), ('pull', 13.183, 25.267),
                                   ('push', 25.267, 30.617, 0.4), ('pull', 30.617, 40.117), ('push', 40.117, 44.767, 0.4),
                                   ('pull', 44.767, None)]),
    # Secret weapon: build into "and then I discovered Immufix", release after
    '593f11c4': dict(DEFAULT, segs=[('intro', 0.0, 2.367), ('push', 2.367, 7.30, 1.8), ('pull', 7.30, 14.30),
                                    ('push', 14.30, 20.483, 1.5), ('pull', 20.483, None)]),
}
