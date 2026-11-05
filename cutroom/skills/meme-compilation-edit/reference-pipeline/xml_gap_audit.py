"""Gap audit on a saved .prproj: every used track must be continuous from 0 to the sequence end."""
import sys
from prproj_masks import Project

TPF = 8467200000

def audit(path, seq_name):
    p = Project(path)
    problems, end = [], None
    tracks = [("VideoTrackGroup", i, f"V{i+1}") for i in range(3)] + [("AudioTrackGroup", 0, "A1")]
    spans = {}
    for kind, idx, label in tracks:
        items = p.track_items(seq_name, kind, idx)
        if not items:
            continue
        spans[label] = items
        end = max(end or 0, items[-1][1])
    for label, items in spans.items():
        prev = 0
        for s, e, _ in items:
            if s != prev:
                problems.append(f"{label} gap {prev / TPF:g}-{s / TPF:g}")
            if s % TPF or e % TPF:
                problems.append(f"{label} off-frame clip {s / TPF}-{e / TPF}")
            prev = e
        if prev != end:
            problems.append(f"{label} ends at {prev / TPF:g}, sequence at {end / TPF:g}")
    return problems

if __name__ == "__main__":
    bad = audit(sys.argv[1], sys.argv[2])   # usage: xml_gap_audit.py project.prproj "sequence name"
    print("GAP AUDIT FAILED: " + "; ".join(bad) if bad else "gap audit ok")
    sys.exit(1 if bad else 0)
