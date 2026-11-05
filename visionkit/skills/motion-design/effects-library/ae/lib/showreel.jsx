// showreel.jsx: "00 Showreel" comp that plays every effect's main comp back to back with its name in a small pill.
// list = [[key, title], ...] in library order; SHOTS[key] holds each built main comp.
function buildShowreel(list) {
    var parts = [], total = 0;
    for (var i = 0; i < list.length; i++) {
        var c = SHOTS[list[i][0]];
        if (!c) { log("showreel: missing " + list[i][0]); continue; }
        parts.push([c, list[i][1], total]); total += c.duration;
    }
    if (!parts.length) return null;
    var reel = newComp("00 Showreel (all effects)", total);
    reel.parentFolder = ROOTF;
    for (var j = 0; j < parts.length; j++) {
        var L = reel.layers.add(parts[j][0]);
        L.startTime = parts[j][2];
        L.inPoint = parts[j][2]; L.outPoint = parts[j][2] + parts[j][0].duration;
        try { L.audioEnabled = false; } catch (ea) {}
        if (parts[j][0].width != reel.width || parts[j][0].height != reel.height) {
            var s = Math.min(reel.width / parts[j][0].width, reel.height / parts[j][0].height) * 100;
            S(L).setValue([s, s]);
        }
        var lab = (j + 1 < 10 ? "0" : "") + (j + 1) + "  " + parts[j][1];
        var pl = pill(reel, lab, 48, reel.height - 64, 30, [0.05, 0.05, 0.07], [1, 1, 1], null);
        for (var q = 0; q < pl.length; q++) {
            pl[q].startTime = 0; pl[q].inPoint = parts[j][2]; pl[q].outPoint = Math.min(parts[j][2] + 2.0, parts[j][2] + parts[j][0].duration);
            pl[q].moveToBeginning();
        }
    }
    note(reel, "Every effect in this library, back to back. Each segment is the effect's main comp; open the comp in its folder to edit it.");
    return reel;
}
