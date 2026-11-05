// edits_lib.jsx: After Effects helpers for music edits (needs ae_lib.jsx first; ES3 only).
// Every layer stays live in the comp (nothing baked): footage, hits, type and motifs are separate layers so a change is
// one layer edit and one render.

// ------------------------------------------------------------------ footage
// clip(comp, file, t0, t1, rk, focus, zoom, name)
//   rk    = time remap keys [[comp t, source t], ...] (2 keys = constant speed; more = ramps)
//   focus = [[comp t, x, y], ...] subject position in SOURCE pixels (anchor follows it = auto reframe), or [x, y]
//   zoom  = extra zoom on top of "cover" (1 = just fill the frame), or [[t, z], ...]
// BAND = {y0, h}: the picture lives in a horizontal band (letterbox, our GASS x Mbappe look: 1080 x 800 in 1080 x 1920),
// black bars above and below where type can sit. Clips "cover" the band instead of the comp. null = full frame.
var BAND = null;
var BAND_EXTEND = true;
var ACTIVE = null;        // [x0, y0, x1, y1] source px: the real picture inside a pillarboxed / letterboxed source   // false while building layers that sit ABOVE the bars (pop-outs): no mirrored extension
function frameBox(comp) {
    return BAND ? { cx: comp.width / 2, cy: BAND.y0 + BAND.h / 2, w: comp.width, h: BAND.h } : { cx: comp.width / 2, cy: comp.height / 2, w: comp.width, h: comp.height };
}
function bars(comp) {      // the two black bars, ABOVE the picture and its hits, BELOW type that sits in the bars
    if (!BAND) return [];
    var top = solidL(comp, "bar top", [0, 0, 0], comp.width, BAND.y0); P(top).setValue([comp.width / 2, BAND.y0 / 2]);
    var bh = comp.height - BAND.y0 - BAND.h, bot = solidL(comp, "bar bottom", [0, 0, 0], comp.width, bh);
    P(bot).setValue([comp.width / 2, BAND.y0 + BAND.h + bh / 2]);
    return [top, bot];
}
function clip(comp, file, t0, t1, rk, focus, zoom, name) {
    var L = remapL(comp, file, rk);
    try { if (L.hasAudio) L.audioEnabled = false; } catch (ea) {}   // footage sound OFF: the song is the only audio (v1-v4 bug)
    if (BAND && BAND_EXTEND) {   // mirrored picture beyond the band, so blurs / spins / shakes never pull in black (14 Oct)
        try { var mt = fx(L, "ADBE Tile"); setDeep(mt, "Output Height", 170); setDeep(mt, "Output Width", 100); setDeep(mt, "Mirror Edges", 1); } catch (et) { log("  band tile " + et.toString()); }
    }
    if (name) L.name = name;
    L.inPoint = t0; L.outPoint = t1;
    var src = L.source, fb = frameBox(comp);
    var ax0 = ACTIVE ? ACTIVE[0] : 0, ay0 = ACTIVE ? ACTIVE[1] : 0, ax1 = ACTIVE ? ACTIVE[2] : src.width, ay1 = ACTIVE ? ACTIVE[3] : src.height;
    var nx = function (v) { return v <= 1.5 ? v * src.width : v; }, ny = function (v) { return v <= 1.5 ? v * src.height : v; };
    var base = Math.max(fb.w / (ax1 - ax0), fb.h / (ay1 - ay0)) * 100;
    var halfW = fb.w / 2, halfH = fb.h / 2;
    function clampAnchor(x, y, z) {   // keep the frame covered by real picture: no black edges, no source bars
        var s = base * z / 100, hw = halfW / s, hh = halfH / s;
        return [Math.min(ax1 - hw, Math.max(ax0 + hw, x)), Math.min(ay1 - hh, Math.max(ay0 + hh, y))];
    }
    var zs = (zoom instanceof Array) ? zoom : [[t0, zoom || 1]];
    var zAt = function (t) { var z = zs[0][1]; for (var i = 0; i < zs.length; i++) if (zs[i][0] <= t) z = zs[i][1]; return z; };
    if (zs.length > 1) { var sk = []; for (var i = 0; i < zs.length; i++) sk.push([zs[i][0], [base * zs[i][1], base * zs[i][1]]]); keys(S(L), sk); }
    else S(L).setValue([base * zs[0][1], base * zs[0][1]]);
    P(L).setValue([fb.cx, fb.cy]);
    if (focus && focus.length && (focus[0] instanceof Array)) {
        var ak = [];
        for (var j = 0; j < focus.length; j++) ak.push([focus[j][0], clampAnchor(nx(focus[j][1]), ny(focus[j][2]), zAt(focus[j][0]))]);
        var ap = A(L);
        for (var q = 0; q < ak.length; q++) ap.setValueAtTime(ak[q][0], ak[q][1]);
        for (var r = 1; r <= ap.numKeys; r++) { try { ap.setInterpolationTypeAtKey(r, KeyframeInterpolationType.BEZIER); ap.setSpatialAutoBezierAtKey(r, true); } catch (e) {} }
    } else {
        var f = focus || [(ax0 + ax1) / 2, (ay0 + ay1) / 2];
        A(L).setValue(clampAnchor(nx(f[0]), ny(f[1]), zAt(t0)));
    }
    return L;
}
// fitClip: the whole 16:9 frame inside the 9:16 comp (end cards, wide gestures that a crop would cut), over a blurred,
// darkened cover copy of itself; a slow push keeps it alive. Leaves empty bands above / below for a title and credit.
function fitClip(comp, file, t0, t1, rk, name, blurR, dimStops, push) {
    var bg = clip(comp, file, t0, t1, rk, null, 1, (name || "fit") + " bg");
    boxBlur(bg, blurR || 40, 1); exposure(bg, -(dimStops || 1.6));
    var fg = remapL(comp, file, rk); fg.name = (name || "fit") + " fg"; fg.inPoint = t0; fg.outPoint = t1;
    try { if (fg.hasAudio) fg.audioEnabled = false; } catch (ea) {}
    var sw = fg.source.width, sh = fg.source.height, s = Math.min(comp.width / sw, comp.height / sh) * 100, k = push || 1.05;
    A(fg).setValue([sw / 2, sh / 2]); P(fg).setValue([comp.width / 2, comp.height / 2]);
    keys(S(fg), [[t0, [s, s]], [t1, [s * k, s * k]]]);
    return fg;
}
// optical-flow slow motion for remapped layers (AE's own Pixel Motion: free Twixtor stand-in)
function smooth(L) { try { L.frameBlendingType = FrameBlendingType.PIXEL_MOTION; L.containingComp.frameBlending = true; } catch (e) { log("  smooth " + e.toString()); } }

// Transform effect params by matchName with a name fallback (logged once so the mapping can be checked)
var TF_LOGGED = false;
function tfp(tf, which) {
    if (!TF_LOGGED) { var names = []; for (var i = 1; i <= tf.numProperties; i++) names.push(tf.property(i).matchName + "=" + tf.property(i).name); log("Transform params: " + names.join(" | ")); TF_LOGGED = true; }
    var m = { pos: ["ADBE Geometry2-0002", "Position"], scale: ["ADBE Geometry2-0003", "Scale"], rot: ["ADBE Geometry2-0007", "Rotation"],
              usecomp: ["ADBE Geometry2-0009", "Use Composition's Shutter Angle"], shutter: ["ADBE Geometry2-0010", "Shutter Angle"] }[which];
    for (var j = 0; j < m.length; j++) { try { var p = tf.property(m[j]); if (p) return p; } catch (e) {} }
    return findProp(tf, m[m.length - 1]);
}
function tfBlur(tf) { try { tfp(tf, "usecomp").setValue(0); tfp(tf, "shutter").setValue(200); } catch (e) { log("  tf blur " + e.toString()); } }

// ------------------------------------------------------------------ hits (adjustment layers over everything below)
function adjSpan(comp, name, t0, t1) { var a = adjL(comp, name); a.inPoint = Math.max(0, t0); a.outPoint = Math.min(comp.duration, t1); return a; }
// zoom punch: jumps to amt on the hit and eases back over dur (Transform effect, so it has motion blur)
function punch(comp, t, amt, dur) {
    var a = adjSpan(comp, "punch " + t.toFixed(2), t - 0.001, t + dur);
    var tf = fx(a, "ADBE Geometry2");
    var sc = tfp(tf, "scale");
    sc.setValueAtTime(t, 100 * amt); sc.setValueAtTime(t + dur, 100);
    easeKey(sc, 1, 33, 10); easeKey(sc, 2, 85, 33);
    tfBlur(tf);
    return a;
}
// decaying shake: wiggle with an exponential envelope, editable afterwards through the expression numbers
function shake(comp, t, amp, dur, freq, rot) {
    var a = adjSpan(comp, "shake " + t.toFixed(2), t, t + dur);
    var tf = fx(a, "ADBE Geometry2");
    var env = "var d = time - " + t.toFixed(4) + "; var e = Math.exp(-4 * d / " + dur.toFixed(3) + ");";
    tfp(tf, "pos").expression = env + " seedRandom(" + Math.round(t * 1000) + ", true); value + (wiggle(" + (freq || 14) + ", " + amp + ") - value) * e;";
    tfp(tf, "rot").expression = env + " seedRandom(" + Math.round(t * 1000 + 7) + ", true); value + (wiggle(" + (freq || 14) + ", " + (rot || 2) + ") - value) * e;";
    tfp(tf, "scale").setValue(100 + amp / 9);   // a touch of zoom hides the moving edges
    tfBlur(tf);
    return a;
}
// flash: a solid that hits peak opacity on the hit and falls off (white = classic flash; colours via blend ADD)
function flash(comp, t, dur, color, peak, mode, lead) {
    // inside the band only: a part-opacity white over the black bars turns them grey (looked cheap, 13 Oct)
    var s = BAND ? solidL(comp, "flash " + t.toFixed(2), color || [1, 1, 1], comp.width, BAND.h) : solidL(comp, "flash " + t.toFixed(2), color || [1, 1, 1]);
    if (BAND) P(s).setValue([comp.width / 2, BAND.y0 + BAND.h / 2]);
    s.inPoint = Math.max(0, t - (lead || 0)); s.outPoint = Math.min(comp.duration, t + dur);
    if (mode) s.blendingMode = mode;
    var o = O(s);
    if (lead) o.setValueAtTime(t - lead, 0);
    o.setValueAtTime(t, peak || 100); o.setValueAtTime(t + dur, 0);
    for (var i = 1; i <= o.numKeys; i++) easeKey(o, i, 33, 33);
    try { easeKey(o, o.numKeys, 60, 10); } catch (e) {}
    return s;
}
// exposure pop: brightens the picture itself (feels like a camera flash, keeps the image readable)
function expoPop(comp, t, stops, dur) {
    var a = adjSpan(comp, "expo " + t.toFixed(2), t - 0.001, t + dur);
    var e = fx(a, "ADBE Exposure2"); var p = findProp(e, "Exposure");
    p.setValueAtTime(t, stops); p.setValueAtTime(t + dur, 0); easeKey(p, 2, 70, 33);
    return a;
}
// black frame breath before a big moment
function breath(comp, t0, t1) { var b = solidL(comp, "breath " + t0.toFixed(2), [0, 0, 0]); b.inPoint = t0; b.outPoint = t1; return b; }
// overlay clip (light leak, bar, burn, streak) in Screen
function overlay(comp, file, t0, scale, opacity, mode) {
    var L = comp.layers.add(imp(file)); L.startTime = t0; L.inPoint = t0;
    L.blendingMode = mode || BlendingMode.SCREEN;
    if (scale) S(L).setValue([scale, scale]);
    if (opacity !== undefined && opacity !== null) O(L).setValue(opacity);
    return L;
}
// glow spanning a range (adjustment)
function glowSpan(comp, t0, t1, thresh, radius, intensity) { var a = adjSpan(comp, "glow", t0, t1); glow(a, thresh || 60, radius || 60, intensity || 0.8); return a; }
// global look: Lumetri + vignette + grain
function look(comp, cc, vig, grainAmt) {
    var a = adjL(comp, "LOOK"); lumetri(a, cc || {});
    if (vig) vignette(comp, vig);
    if (grainAmt) grain(comp, grainAmt);
    return a;
}

// ------------------------------------------------------------------ type
// word that slams in on the hit: scale from big to 100 with motion blur, holds, cuts out
function slamWord(comp, s, t0, t1, font, size, color, x, y, tracking, from, shade) {
    var l = txt(comp, s, font, size, color, ParagraphJustification.CENTER_JUSTIFY, tracking || 0, x, y);
    if (shade) shadow(l, shade, 0, Math.max(20, size * 0.12));     // soft dark halo: reads over any footage, no visible box
    centreAnchor(l); l.inPoint = t0; l.outPoint = t1; l.motionBlur = true;
    var sc = S(l); sc.setValueAtTime(t0, [from || 135, from || 135]); sc.setValueAtTime(t0 + 0.12, [100, 100]); sc.setValueAtTime(t1, [104, 104]);
    easeKey(sc, 2, 85, 33);
    return l;
}
// small line under a title (artist credit, stat line)
function subLine(comp, s, t0, t1, font, size, color, x, y, tracking) {
    var l = txt(comp, s, font, size, color, ParagraphJustification.CENTER_JUSTIFY, tracking || 200, x, y);
    centreAnchor(l); l.inPoint = t0; l.outPoint = t1;
    var o = O(l); o.setValueAtTime(t0, 0); o.setValueAtTime(t0 + 0.15, 100);
    return l;
}

// ------------------------------------------------------------------ motif: charging battery
// battery(comp, t0, t1, from, to, label, accent, bg, levels): the fill grows from the old level to the new one on entry.
//   bg     = undefined/true: plain black card | number 0-100: black at that opacity over the footage (it keeps moving) | false: none
//   levels = [[t, value], ...] later steps that tick instantly (e.g. 97, 98, 99 on a snare roll)
function battery(comp, t0, t1, from, to, label, accent, bg, levels) {
    var cw = comp.width, ch = comp.height, cx = cw / 2, cy = ch * 0.47;
    var bw = cw * 0.74, bh = bw * 0.42, r = bh * 0.16, sw = 16;
    var col = accent || [0.1, 0.95, 0.3];
    var layers = [];
    if (bg !== false) {
        var b = solidL(comp, "batt bg", [0.02, 0.02, 0.025]); b.inPoint = t0; b.outPoint = t1; layers.push(b);
        if (typeof bg === "number") O(b).setValue(bg);
    }
    var lv = levels || [];
    var shell = rrect(comp, "batt shell", bw, bh, r, null, [0.92, 0.92, 0.92], sw, cx, cy); shell.inPoint = t0; shell.outPoint = t1; layers.push(shell);
    var nub = rrect(comp, "batt nub", bh * 0.12, bh * 0.36, bh * 0.05, [0.92, 0.92, 0.92], null, 0, cx + bw / 2 + bh * 0.09, cy); nub.inPoint = t0; nub.outPoint = t1; layers.push(nub);
    var inner = bw - 2 * sw - 16, ih = bh - 2 * sw - 16;
    var fill = rrect(comp, "batt fill", inner, ih, r * 0.55, col, null, 0, cx, cy); fill.inPoint = t0; fill.outPoint = t1;
    // grow from the left edge: anchor at the left of the shape, x scale = level
    var g = fill.property("ADBE Root Vectors Group").property(1);
    try { g.property("ADBE Vector Transform Group").property("ADBE Vector Anchor").setValue([-inner / 2, 0]); g.property("ADBE Vector Transform Group").property("ADBE Vector Position").setValue([-inner / 2, 0]); } catch (e) { log("  batt anchor " + e.toString()); }
    var gs = g.property("ADBE Vector Transform Group").property("ADBE Vector Scale");
    gs.setValueAtTime(t0, [Math.max(0.5, from), 100]); gs.setValueAtTime(t0 + 0.35, [Math.max(0.5, to), 100]); easeKey(gs, 2, 85, 33);
    for (var q = 0; q < lv.length; q++) gs.setValueAtTime(lv[q][0], [Math.max(0.5, lv[q][1]), 100]);
    // steps: the entry ramp (key 1 -> 2) stays eased, every later change is a hold (instant tick)
    for (var k = 2; k <= gs.numKeys; k++) { try { gs.setInterpolationTypeAtKey(k, k == 2 ? KeyframeInterpolationType.BEZIER : KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD); } catch (e) { log("  batt hold " + e.toString()); } }
    glow(fill, 75, 30, 0.45); layers.push(fill);
    var pct = txt(comp, to + "%", "GalanoGrotesque-Black", bh * 0.42, [1, 1, 1], ParagraphJustification.CENTER_JUSTIFY, 0, cx, cy + bh * 0.16);
    pct.inPoint = t0; pct.outPoint = t1;
    var lvs = []; for (var q2 = 0; q2 < lv.length; q2++) lvs.push("[" + lv[q2][0].toFixed(3) + "," + lv[q2][1] + "]");
    pct.property("Source Text").expression = "var a = " + from + ", b = " + to + ", L = [" + lvs.join(",") + "], t = Math.min(1, Math.max(0, (time - " + t0.toFixed(3) + ") / 0.35));" +
        " var v = a + (b - a) * (1 - Math.pow(1 - t, 3)); for (var i = 0; i < L.length; i++) if (time >= L[i][0]) v = L[i][1]; Math.round(v) + '%';";
    layers.push(pct);
    if (label) { var lb = subLine(comp, label, t0 + 0.05, t1, "ProximaNova-Extrabld", bh * 0.16, col, cx, cy + bh * 0.85, 380); layers.push(lb); }
    return layers;
}

// ------------------------------------------------------------------ mattes (SAM 2 roto videos, same size as the source clip)
// the matte gets the clip's exact framing; rkM = the clip's remap keys shifted to the matte file's own time base
function matteFor(comp, matteFile, t0, t1, rkM, focus, zoom) {
    var m = clip(comp, matteFile, t0, t1, rkM, focus, zoom, "matte " + t0.toFixed(2));
    m.enabled = false; return m;
}
// cutout: a copy of the clip that only shows where the matte is white (puts the player in front of type)
function cutoutL(comp, file, t0, t1, rk, focus, zoom, matteLayer) {
    var c = clip(comp, file, t0, t1, rk, focus, zoom, "cutout " + t0.toFixed(2));
    c.setTrackMatte(matteLayer, TrackMatteType.LUMA); c.motionBlur = true; return c;
}
// silhouette strobe: the player as a flat glowing shape on single frames (our GASS signature)
function silStrobe(comp, matteLayer, times, color, glowR) {
    var out = [];
    for (var i = 0; i < times.length; i++) {
        var s = solidL(comp, "sil " + times[i].toFixed(3), color || [1, 0.98, 0.92]);
        s.inPoint = times[i]; s.outPoint = times[i] + 1 / FPS;
        s.setTrackMatte(matteLayer, TrackMatteType.LUMA);
        if (glowR) glow(s, 20, glowR, 1.2);
        out.push(s);
    }
    return out;
}

// ------------------------------------------------------------------ sound design
function sfxL(comp, file, tStart, db) {
    var L = comp.layers.add(imp(file)); L.startTime = tStart; L.inPoint = Math.max(0, tStart);
    try { L.property("ADBE Audio Group").property("ADBE Audio Levels").setValue([db, db]); } catch (e) { log("  sfx level " + e.toString()); }
    return L;
}

// neon outline: a slightly grown silhouette in a colour, placed BEHIND the cutout so only a rim shows, then glowed
function outlineL(comp, matteFile, t0, t1, rkM, focus, zoom, color, grow, glowR) {
    var m2 = matteFor(comp, matteFile, t0, t1, rkM, focus, zoom); m2.name = "outline matte " + t0.toFixed(2);
    var mm = fx(m2, "ADBE Minimax");
    try { setDeep(mm, "Radius", grow || 8); setDeep(mm, "Operation", 2); } catch (e) { log("  minimax " + e.toString()); }
    var s = solidL(comp, "outline " + t0.toFixed(2), color || [1, 0.85, 0.2]); s.inPoint = t0; s.outPoint = t1;
    s.setTrackMatte(m2, TrackMatteType.LUMA);
    glow(s, 10, glowR || 50, 1.6);
    return s;
}
// colour pop: world goes B&W for the span, the player (cutout) stays in colour above it
function colorPop(comp, t0, t1) { var a = adjSpan(comp, "B&W pop " + t0.toFixed(2), t0, t1); lumetri(a, { sat: 0, con: 25 }); return a; }

// ------------------------------------------------------------------ transitions
// whip: the picture slides out fast before the cut and the next shot slides in from the other side (motion blurred).
// Adjustment layer = it works on whatever is below; Motion Tile mirrors the edges so no black shows.
function whip(comp, t, dir, dur, dist) {
    var d = dur || 0.12, f = 1 / FPS, w = comp.width, cx = comp.width / 2, cy = comp.height / 2, k = (dir || 1) * (dist || 0.55) * w;
    var a = adjSpan(comp, "whip " + t.toFixed(2), t - d, t + d);
    var mt = fx(a, "ADBE Tile");
    setDeep(mt, "Output Width", 300); setDeep(mt, "Output Height", 300); setDeep(mt, "Mirror Edges", 1);
    var tf = fx(a, "ADBE Geometry2"), p = tfp(tf, "pos");
    p.setValueAtTime(t - d, [cx, cy]); p.setValueAtTime(t - f, [cx - k, cy]); p.setValueAtTime(t, [cx + k, cy]); p.setValueAtTime(t + d, [cx, cy]);
    easeKey(p, 1, 33, 10); easeKey(p, 2, 90, 33); easeKey(p, 3, 33, 90); easeKey(p, 4, 85, 33);
    try { p.setInterpolationTypeAtKey(2, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.HOLD); } catch (e) { log("  whip hold " + e.toString()); }
    tfBlur(tf);
    return a;
}
// ------------------------------------------------------------------ lock-on reticle ("I hit my target")
// ring + ticks that spin and shrink onto (x, y) and lock exactly on tLock; holds to t1 then fades.
function reticle(comp, tLock, t1, x, y, color, r) {
    var col = color || [1, 0.85, 0.2], rad = r || 110, t0 = tLock - 0.2;
    var l = comp.layers.addShape(); l.name = "reticle " + tLock.toFixed(2);
    var g1 = shapeGroup(l); g1.addProperty("ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size").setValue([2 * rad, 2 * rad]);
    var s1 = g1.addProperty("ADBE Vector Graphic - Stroke"); s1.property("ADBE Vector Stroke Color").setValue(col); s1.property("ADBE Vector Stroke Width").setValue(6);
    var g2 = shapeGroup(l); g2.addProperty("ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size").setValue([12, 12]);
    g2.addProperty("ADBE Vector Graphic - Fill").property("ADBE Vector Fill Color").setValue(col);
    var dirs = [[0, -1], [1, 0], [0, 1], [-1, 0]];
    for (var i = 0; i < 4; i++) {
        var g = shapeGroup(l), rc = g.addProperty("ADBE Vector Shape - Rect"), hz = dirs[i][0] !== 0;
        rc.property("ADBE Vector Rect Size").setValue(hz ? [46, 7] : [7, 46]);
        rc.property("ADBE Vector Rect Position").setValue([dirs[i][0] * (rad + 8), dirs[i][1] * (rad + 8)]);
        g.addProperty("ADBE Vector Graphic - Fill").property("ADBE Vector Fill Color").setValue(col);
    }
    P(l).setValue([x, y]); l.inPoint = t0; l.outPoint = t1; l.motionBlur = true;
    var sc = S(l); sc.setValueAtTime(t0, [280, 280]); sc.setValueAtTime(tLock, [100, 100]); sc.setValueAtTime(tLock + 0.08, [112, 112]); sc.setValueAtTime(tLock + 0.18, [100, 100]);
    easeKey(sc, 2, 90, 33);
    var ro = R(l); ro.setValueAtTime(t0, -90); ro.setValueAtTime(tLock, 0); easeKey(ro, 2, 90, 33);
    var o = O(l); o.setValueAtTime(t0, 0); o.setValueAtTime(t0 + 0.05, 100); o.setValueAtTime(t1 - 0.08, 100); o.setValueAtTime(t1, 0);
    glow(l, 20, 25, 1.0);
    return l;
}

// ------------------------------------------------------------------ designed type (13 Oct v4, after the user's review)
// heroText: the big number / word (best placed BEHIND the player with a cutout above it, like the "16" the user loved).
// Looks: white with a soft top-to-bottom sheen and fine grain inside the letters (no flat "default text" look), a soft
// glow, and an offset copy in a colour behind it = printed depth (the big "2" in the Spain 2026 promo). Slams in.
function slamScale(l, t0, from) {
    var sc = S(l), f = from || 125; sc.setValueAtTime(t0, [f, f]); sc.setValueAtTime(t0 + 0.13, [100, 100]); sc.setValueAtTime(t0 + 3, [104, 104]);
    easeKey(sc, 2, 85, 33);
}
function heroText(comp, s, t0, t1, x, y, size, font, color, depthCol, depth, tracking, from) {
    var f = font || "GalanoGrotesque-Black", d = (depth === undefined || depth === null) ? Math.round(size * 0.03) : depth, out = [];
    if (depthCol) {
        var b = txt(comp, s, f, size, depthCol, ParagraphJustification.CENTER_JUSTIFY, tracking || 0, x, y); centreAnchor(b);
        b.name = s + " depth"; b.inPoint = t0; b.outPoint = t1; b.motionBlur = true; slamScale(b, t0, from);
        var pb = P(b), p0 = pb.value; pb.setValueAtTime(t0, p0); pb.setValueAtTime(t0 + 0.16, [p0[0] + d, p0[1] + d]); easeKey(pb, 2, 85, 33);
        out.push(b);
    }
    var l = txt(comp, s, f, size, color || [1, 1, 1], ParagraphJustification.CENTER_JUSTIFY, tracking || 0, x, y);
    var r = centreAnchor(l); l.name = s; l.inPoint = t0; l.outPoint = t1; l.motionBlur = true; slamScale(l, t0, from);
    try {   // sheen: Gradient Ramp fills only inside the letters; points are in layer space (rect from centreAnchor)
        var rp = fx(l, "ADBE Ramp");
        setDeep(rp, "Start of Ramp", [r.left + r.width / 2, r.top]); setDeep(rp, "End of Ramp", [r.left + r.width / 2, r.top + r.height]);
        setDeep(rp, "Start Color", color || [1, 1, 1]); setDeep(rp, "End Color", [0.74, 0.75, 0.78]); setDeep(rp, "Blend With Original", 0);
        var nz = fx(l, "ADBE Noise"); setDeep(nz, "Amount of Noise", 14);
    } catch (e) { log("  hero texture " + e.toString()); }
    glow(l, 55, Math.max(20, size * 0.06), 0.35);
    out.push(l);
    return out;
}
// caption: small, wide-tracked, light; the quiet partner of a big hero word. Rises in over 0.2 s.
function caption(comp, s, t0, t1, x, y, size, font, tracking, color) {
    var l = txt(comp, s, font || "ProximaNova-Semibold", size || 36, color || [1, 1, 1], ParagraphJustification.CENTER_JUSTIFY, tracking === undefined ? 380 : tracking, x, y);
    centreAnchor(l); l.name = "cap " + s; l.inPoint = t0; l.outPoint = t1;
    var o = O(l); o.setValueAtTime(t0, 0); o.setValueAtTime(t0 + 0.2, 92); easeKey(o, 2, 85, 33);
    var p = P(l), p0 = p.value; p.setValueAtTime(t0, [p0[0], p0[1] + 14]); p.setValueAtTime(t0 + 0.2, p0); easeKey(p, 2, 85, 33);
    shadow(l, 0.55, 0, 18);
    return l;
}
// zoomCut: a clean replacement for whips. The outgoing shot rushes in (scale + radial blur over 2 frames), the cut lands
// at the peak, the incoming shot settles from the same zoom over 3 frames. Nothing mirrored, nothing static.
function zoomCut(comp, t, amt, settle) {
    var f = 1 / FPS, k = 100 * (amt || 1.2), d = settle || 3 * f;
    var a = adjSpan(comp, "zoomcut " + t.toFixed(2), t - 2 * f, t + d);
    var tf = fx(a, "ADBE Geometry2"), sc = tfp(tf, "scale");
    sc.setValueAtTime(t - 2 * f, 100); sc.setValueAtTime(t - 0.001, k); sc.setValueAtTime(t, k); sc.setValueAtTime(t + d, 100);
    easeKey(sc, 1, 33, 10); easeKey(sc, 2, 90, 33); easeKey(sc, 4, 85, 33);
    tfBlur(tf);
    try {
        var rb = fx(a, "CC Radial Fast Blur"), am = findProp(rb, "Amount");
        am.setValueAtTime(t - 2 * f, 0); am.setValueAtTime(t, 55); am.setValueAtTime(t + d, 0);
        var ce = findProp(rb, "Center"); var fb = frameBox(comp); if (ce) ce.setValue([fb.cx, fb.cy]);
    } catch (e) { log("  zoomcut blur " + e.toString()); }
    return a;
}
// fade the whole picture to black at the end (an adjustment would not darken the bars; a solid does)
function fadeOut(comp, t0, t1) { var s = solidL(comp, "fade out", [0, 0, 0]); s.inPoint = t0; s.outPoint = t1; var o = O(s); o.setValueAtTime(t0, 0); o.setValueAtTime(t1, 100); return s; }

// ------------------------------------------------------------------ transitions v2 (13 Oct, after "make them cool")
// All are adjustment layers / solids placed BELOW the letterbox bars (they change the picture, never the bars).
// invertFlicker: one character per frame from t: "I" colour negative, "N" B&W negative, "M" hard B&W negative, "B" B&W
// (positive, high contrast), "." untouched. e.g. "IN.N" = negative, mono negative, normal, mono negative.
function invertFlicker(comp, t, pattern) {
    var f = 1 / FPS, out = [];
    for (var i = 0; i < pattern.length; i++) {
        var ch = pattern.charAt(i); if (ch == ".") continue;
        var a = adjSpan(comp, "flicker " + ch + " " + (t + i * f).toFixed(2), t + i * f, t + (i + 1) * f);
        if (ch == "N" || ch == "M" || ch == "B") fx(a, "ADBE Black&White");
        if (ch != "B") fx(a, "ADBE Invert");
        if (ch == "M" || ch == "B") { var bc = fx(a, "ADBE Brightness & Contrast 2"); setp(bc, "ADBE Brightness & Contrast 2-0002", 70); }
        out.push(a);
    }
    return out;
}
// colorFlash: a diagonal gradient wash (e.g. orange to pink) over the picture in Add mode: peaks on t, falls off over dur.
function colorFlash(comp, t, colA, colB, dur, peak) {
    var fb = frameBox(comp), f = 1 / FPS, d = dur || 0.16;
    var s = solidL(comp, "cflash " + t.toFixed(2), [1, 1, 1], comp.width, fb.h); P(s).setValue([fb.cx, fb.cy]);
    var g = fx(s, "ADBE Ramp");
    setDeep(g, "Start of Ramp", [0, 0]); setDeep(g, "End of Ramp", [comp.width, fb.h]);
    setDeep(g, "Start Color", colA || [1, 0.55, 0.12]); setDeep(g, "End Color", colB || [1, 0.12, 0.45]);
    s.blendingMode = BlendingMode.ADD; s.inPoint = t - f; s.outPoint = t + d;
    var o = O(s); o.setValueAtTime(t - f, 0); o.setValueAtTime(t, peak || 90); o.setValueAtTime(t + d, 0);
    easeKey(o, 2, 33, 10); easeKey(o, 3, 70, 33);
    return s;
}
// glitchCut: a short digital break around the cut: square-wave slice shifts that change every frame, hue offset,
// scale and position jitter. before / after = frames on each side of the cut.
function glitchCut(comp, t, before, after, amt) {
    var f = 1 / FPS, b = before || 2, n = (before || 2) + (after || 2), k = amt || 1;
    var a = adjSpan(comp, "glitch " + t.toFixed(2), t - b * f, t - b * f + n * f);
    var seed = "seedRandom(" + Math.round(t * 1000) + " + Math.floor(time * " + FPS + "), true); ";
    var ww = fx(a, "ADBE Wave Warp");
    try {
        ww.property("ADBE Wave Warp-0001").setValue(2);
        ww.property("ADBE Wave Warp-0004").setValue(0);
        ww.property("ADBE Wave Warp-0005").setValue(0);
        ww.property("ADBE Wave Warp-0002").expression = seed + "random(30, 140) * " + k + ";";
        ww.property("ADBE Wave Warp-0003").expression = seed + "random(40, 260);";
        ww.property("ADBE Wave Warp-0007").expression = seed + "random(0, 360);";
        ww.property("ADBE Wave Warp-0006").setValue(1);
    } catch (e) { log("  glitch wave " + e.toString()); }
    try {
        var co = fx(a, "CC Color Offset");
        for (var j = 1; j <= co.numProperties; j++) { var p = co.property(j); if (p.name.indexOf("Phase") >= 0) p.expression = seed + "random(-180, 180);"; }
    } catch (e2) { log("  glitch hue " + e2.toString()); }
    var tf = fx(a, "ADBE Geometry2");
    tfp(tf, "scale").expression = seed + "random(102, 112);";
    tfp(tf, "pos").expression = seed + "value + [random(-40, 40) * " + k + ", random(-12, 12)];";
    return a;
}
// spinCut: rotational zoom across the cut: the out-going shot turns +deg and grows, the in-coming one arrives from -deg.
function spinCut(comp, t, deg, before, after) {
    var f = 1 / FPS, d = deg || 18, b = (before || 3) * f, e = (after || 4) * f;
    var a = adjSpan(comp, "spin " + t.toFixed(2), t - b, t + e), tf = fx(a, "ADBE Geometry2");
    var r = tfp(tf, "rot"), sc = tfp(tf, "scale"), cover = 100 * (1.0 + 1.4 * Math.sin(Math.abs(d) * Math.PI / 180)) + 8;
    r.setValueAtTime(t - b, 0); r.setValueAtTime(t - 0.001, d); r.setValueAtTime(t, -d); r.setValueAtTime(t + e, 0);
    sc.setValueAtTime(t - b, 100); sc.setValueAtTime(t - 0.001, cover); sc.setValueAtTime(t, cover); sc.setValueAtTime(t + e, 100);
    easeKey(r, 1, 33, 10); easeKey(r, 2, 90, 33); easeKey(r, 4, 85, 33); easeKey(sc, 1, 33, 10); easeKey(sc, 2, 90, 33); easeKey(sc, 4, 85, 33);
    tfBlur(tf); try { tfp(tf, "shutter").setValue(300); } catch (es) {}
    return a;
}
// shutterCut: the letterbox closes on the picture (two black blades from the bars) and opens on the next shot.
function shutterCut(comp, t, closeF, openF, edge) {
    if (!BAND) return null;
    var f = 1 / FPS, c = (closeF || 3) * f, o = (openF || 4) * f, w = comp.width, half = BAND.h / 2 + 6;
    var y0 = BAND.y0, y1 = BAND.y0 + BAND.h, mid = BAND.y0 + BAND.h / 2, out = [];
    var spec = [[y0 - half / 2, mid - half / 2], [y1 + half / 2, mid + half / 2]];
    for (var i = 0; i < 2; i++) {
        var s = solidL(comp, "shutter " + i + " " + t.toFixed(2), [0, 0, 0], w, half); s.inPoint = t - c; s.outPoint = t + o;
        var p = P(s); p.setValueAtTime(t - c, [w / 2, spec[i][0]]); p.setValueAtTime(t - 0.001, [w / 2, spec[i][1]]); p.setValueAtTime(t, [w / 2, spec[i][1]]); p.setValueAtTime(t + o, [w / 2, spec[i][0]]);
        easeKey(p, 1, 33, 10); easeKey(p, 2, 95, 33); easeKey(p, 4, 90, 33); s.motionBlur = true; out.push(s);
    }
    if (edge !== false) {
        var ln = solidL(comp, "shutter line " + t.toFixed(2), [1, 0.95, 0.85], w, 6); P(ln).setValue([w / 2, mid]); ln.inPoint = t - f; ln.outPoint = t + f;
        glow(ln, 10, 60, 2); out.push(ln);
    }
    return out;
}
// rgbSplit: a TRUE channel split on one clip layer for [t0, t1]: the base keeps green only, a red copy and a blue copy
// (Add mode) sit offset sideways and slide back into register by t1.
function rgbSplit(comp, L, t0, t1, px) {
    var d = px || 26, out = [], OFF = 10;   // Shift Channels menu: 1 Alpha 2 Red 3 Green 4 Blue ... 9 Full On 10 Full Off
    var base = fx(L, "ADBE Shift Channels");
    var pr = base.property("ADBE Shift Channels-0002"), pb = base.property("ADBE Shift Channels-0004");
    pr.setValueAtTime(t0 - 0.002, 2); pr.setValueAtTime(t0, OFF); pr.setValueAtTime(t1, 2);
    pb.setValueAtTime(t0 - 0.002, 4); pb.setValueAtTime(t0, OFF); pb.setValueAtTime(t1, 4);
    var cols = [[2, OFF, OFF, d], [OFF, OFF, 4, -d]];
    for (var i = 0; i < 2; i++) {
        var c = L.duplicate(); c.name = L.name + (i ? " blue" : " red");
        try { var ep = c.property("ADBE Effect Parade"); for (var q = ep.numProperties; q >= 1; q--) if (ep.property(q).matchName == "ADBE Shift Channels") ep.property(q).remove(); } catch (er) { log("  rgb strip " + er.toString()); }
        var sc = fx(c, "ADBE Shift Channels"); setp(sc, "ADBE Shift Channels-0002", cols[i][0]); setp(sc, "ADBE Shift Channels-0003", cols[i][1]); setp(sc, "ADBE Shift Channels-0004", cols[i][2]);
        c.blendingMode = BlendingMode.ADD; c.inPoint = Math.max(L.inPoint, t0); c.outPoint = Math.min(L.outPoint, t1);
        var tf = fx(c, "ADBE Geometry2"), p = tfp(tf, "pos"), v = p.value;
        p.setValueAtTime(t0, [v[0] + cols[i][3], v[1]]); p.setValueAtTime(t1, v); easeKey(p, 2, 80, 33);
        c.moveBefore(L); out.push(c);
    }
    return out;
}
// popIn: the player (cutout) pops forward on the cut: scales 122% to 100% about himself with a white rim, while the rest
// of the picture dims for a moment. sx, sy = the subject in SOURCE pixels (from his matte).
function popIn(comp, cut, matteLayer, t, sx, sy, dur) {
    var f = 1 / FPS, d = dur || 6 * f;
    var dim = adjSpan(comp, "pop dim " + t.toFixed(2), t, t + d); var ex = fx(dim, "ADBE Exposure2"); var pe = findProp(ex, "Exposure");
    pe.setValueAtTime(t, -1.6); pe.setValueAtTime(t + d, 0); easeKey(pe, 2, 70, 33);
    dim.moveAfter(cut);
    var tf = fx(cut, "ADBE Geometry2");
    try { tf.property("ADBE Geometry2-0001").setValue([sx, sy]); tfp(tf, "pos").setValue([sx, sy]); } catch (e) { log("  pop anchor " + e.toString()); }
    var sc = tfp(tf, "scale"); sc.setValueAtTime(t, 122); sc.setValueAtTime(t + d, 100); easeKey(sc, 2, 85, 33); tfBlur(tf);
    var rim = solidL(comp, "pop rim " + t.toFixed(2), [1, 1, 1]); rim.inPoint = t; rim.outPoint = t + 2 * f;
    rim.setTrackMatte(matteLayer, TrackMatteType.LUMA); glow(rim, 10, 40, 1.5); O(rim).setValue(70);
    return [dim, rim];
}
// posterizeSpan: stepped, laggy motion (12 fps look) for a section
function posterizeSpan(comp, t0, t1, fps) { var a = adjSpan(comp, "posterize " + t0.toFixed(2), t0, t1); setp(fx(a, "ADBE Posterize Time"), "ADBE Posterize Time-0001", fps || 12); return a; }
