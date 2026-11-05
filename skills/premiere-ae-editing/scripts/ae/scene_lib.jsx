// scene_lib.jsx: scene builders for storyboard-to-After-Effects builds: SF Pro Display captions with the Smooth Text
// Transition, plates and image sequences rendered from a storyboard kit, flashes, fades, HUD brackets, boxes, typed text,
// RGB hits, the night and paper grades, a finish comp, chain() for multi-step two-key moves, a camera on a world layer,
// depth-of-field bands, sample-frame test comps and a native ordered dither zone. Origin: a short documentary reel built
// from an approved storyboard (13 Oct 2026).
// Load order: ae_lib.jsx, motion_lib.jsx, then this file (it uses k2, EASES, setEase, eff, setE, impF, filed, chanOnly).
// NOTE: CAP and capFont() below REPLACE motion_lib's versions for the whole generated script (function declarations are
// hoisted, the last one wins), so motion_lib's capRow() / counterRow() also switch to these SF Pro fonts and sizes when
// this file is loaded. Use cap() from this file, or leave this file out when a build needs motion_lib's caption fonts.
// Fonts: SF Pro Display is an Apple font (not on Windows; check its licence before client renders).
// Globals the generator must set: PLATES (folder of rendered plates, trailing slash); VIG = {ac: png, mm: png, mmdark: png}
// for finish() (this skill ships assets/ae/vignette_*.png); BAYER (folder holding bayer_<cell>px.png threshold maps, trailing
// slash; this skill ships assets/ae/bayer_2px..5px.png) for ditherZone().

// ---------------------------------------------------------------- captions (SF Pro Display, storyboard capAC)
var CAP = 76, FONT_CI = "SFProDisplay-Medium", FONT_CB = "SFProDisplay-Bold";
function capFont(kind) { return kind == "i" ? [FONT_CI, 1, -15] : [FONT_CB, 1, -15]; }
function styleCap(L) {
    eff(L, "ADBE Drop Shadow", "Shadow");
    setE(L, "Shadow", "Opacity", 140); setE(L, "Shadow", "Direction", 180); setE(L, "Shadow", "Distance", 2); setE(L, "Shadow", "Softness", 14);
    eff(L, "ADBE Glo2", "Glow"); setE(L, "Glow", "Glow Threshold", 55); setE(L, "Glow", "Glow Radius", 16); setE(L, "Glow", "Glow Intensity", 0.35);
}
// cap(c, words, tOut, yFrac): words = [[text, "i"|"b", tOn], ...]; centred on one baseline at yFrac of the frame.
// Each word arrives with the Smooth Text Transition (blur 10 -> 0, opacity 0 -> 100, rise 12 px -> 0, two settle keys, 5 frames).
function cap(c, words, tOut, yFrac, tIn0) {
    var Ls = [], rs = [], total = 0, gap = CAP * 0.24, i;
    for (i = 0; i < words.length; i++) {
        var f = capFont(words[i][1]);
        var L = txt(c, words[i][0], f[0], CAP * f[1], [1, 1, 1], ParagraphJustification.LEFT_JUSTIFY, f[2], 0, 0);
        L.name = "caption: " + words[i][0];
        var r = rect(L); Ls.push(L); rs.push(r); total += r.width;
    }
    total += gap * (Ls.length - 1);
    var x = W / 2 - total / 2, yb = H * yFrac + CAP * 0.36;
    for (i = 0; i < Ls.length; i++) {
        var tOn = words[i][2];
        Ls[i].inPoint = Math.max(0, tOn - fr(1)); Ls[i].outPoint = tOut;
        k2(P(Ls[i]), tOn, [x - rs[i].left, yb + 12], tOn + fr(5), [x - rs[i].left, yb], "settle");
        k2(O(Ls[i]), tOn, 0, tOn + fr(4), 100, "settle");
        var bl = gaussBlur(Ls[i], 0);
        k2(bl.property("ADBE Gaussian Blur 2-0001"), tOn, 10, tOn + fr(5), 0, "settle");
        styleCap(Ls[i]);
        x += rs[i].width + gap;
    }
    return Ls;
}

// ---------------------------------------------------------------- rendered layers and sequences
var SEQ = {};
function impSeq(first, alpha) {
    if (SEQ[first]) return SEQ[first];
    var io = new ImportOptions(new File(first)); io.sequence = true; io.forceAlphabetical = true;
    var it = app.project.importFile(io);
    try { it.mainSource.conformFrameRate = FPS; } catch (e) {}
    if (alpha) { try { it.mainSource.alphaMode = AlphaMode.STRAIGHT; } catch (e2) {} }
    filed(it, "_plates"); SEQ[first] = it; return it;
}
function impStill(path, alpha) {
    var it = impF(path);
    if (alpha) { try { it.mainSource.alphaMode = AlphaMode.STRAIGHT; } catch (e) {} }
    filed(it, "_plates");
    return it;
}
// plate: a still layer placed like a camera window. o.cx/o.cy = image px at the frame centre (default image centre),
// o.s = scale in percent (default: fit the frame), o.to = {cx, cy, s, style} for one eased move over [t0, t1].
function plate(c, path, t0, t1, o) {
    o = o || {};
    var L = c.layers.add(impStill(path, o.alpha));
    L.startTime = 0; L.inPoint = t0; L.outPoint = t1;
    var iw = L.source.width, ih = L.source.height, fit = Math.max(W / iw, H / ih) * 100;
    var s0 = o.s || fit, cx0 = (o.cx === undefined ? iw / 2 : o.cx), cy0 = (o.cy === undefined ? ih / 2 : o.cy);
    P(L).setValue([W / 2 + (o.dx || 0), H / 2 + (o.dy || 0)]);
    A(L).setValue([cx0, cy0]); S(L).setValue([s0, s0]);
    if (o.to) {
        var m = o.to, ta = m.t0 === undefined ? t0 : m.t0, tb = m.t1 === undefined ? t1 : m.t1, st = m.style || "gentle";
        var s1 = m.s || s0, cx1 = (m.cx === undefined ? cx0 : m.cx), cy1 = (m.cy === undefined ? cy0 : m.cy);
        if (cx1 != cx0 || cy1 != cy0) k2(A(L), ta, [cx0, cy0], tb, [cx1, cy1], st);
        if (s1 != s0) k2(S(L), ta, [s0, s0], tb, [s1, s1], st);
    }
    if (o.blend) L.blendingMode = o.blend;
    if (o.op !== undefined) O(L).setValue(o.op);
    if (o.name) L.name = o.name;
    L.quality = LayerQuality.BEST;
    return L;
}
// seqL: an image sequence rendered from the storyboard kit with progress p = 0..1 across its n frames.
// Two time-remap keys map [t0, t1] onto the whole sequence with ease style (default gentle); the last frame holds to tOut.
function seqL(c, first, n, t0, t1, o) {
    o = o || {};
    var L = c.layers.add(impSeq(first, o.alpha));
    // time remapping first: a sequence is shorter than the comp, and AE clamps in/out points to the source until
    // remapping is on (setting them first left the layer ending before its shot began)
    L.startTime = 0; L.timeRemapEnabled = true;
    L.outPoint = (o.tOut === undefined ? t1 : o.tOut); L.inPoint = t0;
    var trm = L.property("ADBE Time Remapping"), end = (n - 1) / FPS;
    var a = o.from === undefined ? 0 : o.from * end, b = o.until === undefined ? end : o.until * end;
    trm.setValueAtTime(t0, a); trm.setValueAtTime(t1, b);
    for (var k = trm.numKeys; k >= 1; k--) { var kt = trm.keyTime(k); if (Math.abs(kt - t0) > 1e-4 && Math.abs(kt - t1) > 1e-4) trm.removeKey(k); }
    var i0 = trm.nearestKeyIndex(t0), i1 = trm.nearestKeyIndex(t1);
    if (o.style == "linear") { trm.setInterpolationTypeAtKey(i0, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR); trm.setInterpolationTypeAtKey(i1, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR); }
    else { var e = EASES[o.style || "gentle"]; setEase(trm, i0, 33.3, e[0]); setEase(trm, i1, e[1], 33.3); }
    var iw = L.source.width, fit = W / iw * 100;
    S(L).setValue([o.s || fit, o.s || fit]); P(L).setValue([W / 2, H / 2]);
    if (o.to) { var m = o.to; k2(S(L), m.t0 === undefined ? t0 : m.t0, [o.s || fit, o.s || fit], m.t1 === undefined ? t1 : m.t1, [m.s, m.s], m.style || "gentle"); }
    if (o.blend) L.blendingMode = o.blend;
    if (o.name) L.name = o.name;
    L.quality = LayerQuality.BEST;
    return L;
}
function P2(name) { return PLATES + name + ".png"; }
function J2(name) { return PLATES + name + ".jpg"; }
function S0(name, fmt) { return PLATES + name + "/" + name + "_0000." + (fmt || "png"); }

// ---------------------------------------------------------------- small motion pieces
function flash(c, t, frames, op) {
    var s = solidT(c, "white flash", [1, 1, 1], t, t + fr(frames || 4));
    k2(O(s), t, op || 100, t + fr(frames || 4), 0, "settle"); return s;
}
function blackT(c, t0, t1) { return solidT(c, "black", [0, 0, 0], t0, t1); }
// fade a layer in or out with two keys
function fadeIn(L, t, frames) { k2(O(L), t, 0, t + fr(frames || 6), O(L).value || 100, "settle"); }
function fadeOut(L, t, frames, to) { k2(O(L), t - fr(frames || 6), O(L).value, t, to || 0, "accel"); }
// HUD brackets: four corner marks closing from a larger box onto (x, y, w, h); tag above in JetBrains Mono
function hud(c, x, y, w, h, t0, t1, col, tag, from) {
    col = col || [1, 1, 1];
    var L = c.layers.addShape(); L.name = "HUD brackets";
    var root = L.property("ADBE Root Vectors Group"), k = Math.min(w, h) * 0.18;
    var corners = [[[0, k], [0, 0], [k, 0]], [[w - k, 0], [w, 0], [w, k]], [[w, h - k], [w, h], [w - k, h]], [[k, h], [0, h], [0, h - k]]];
    for (var i = 0; i < 4; i++) {
        var g = root.addProperty("ADBE Vector Group"); var gp = g.property("ADBE Vectors Group");
        var pth = gp.addProperty("ADBE Vector Shape - Group"); var sh = new Shape(); sh.vertices = corners[i]; sh.closed = false; pth.property("ADBE Vector Shape").setValue(sh);
        var st = root.property(i + 1).property("ADBE Vectors Group").addProperty("ADBE Vector Graphic - Stroke");
        st.property("ADBE Vector Stroke Color").setValue(col); st.property("ADBE Vector Stroke Width").setValue(3);
    }
    A(L).setValue([w / 2, h / 2]); P(L).setValue([x + w / 2, y + h / 2]);
    L.inPoint = t0; L.outPoint = t1;
    var f = from || 1.6;
    k2(S(L), t0, [100 * f, 100 * f], t0 + fr(8), [100, 100], "settle");
    k2(O(L), t0, 0, t0 + fr(3), 100, "settle");
    if (tag) {
        var T = txt(c, tag, "JetBrainsMono-Regular", 22, col, ParagraphJustification.LEFT_JUSTIFY, 40, 0, 0);
        T.name = "HUD tag"; var r = rect(T); P(T).setValue([x - r.left, y - 14]); T.inPoint = t0 + fr(6); T.outPoint = t1;
        k2(O(T), t0 + fr(6), 0, t0 + fr(10), 100, "settle");
    }
    return L;
}
// rectangle shape (comp coordinates), optional fill/stroke, anchor at its left edge so Scale X grows it from the left
function box(c, name, x, y, w, h, fill, stroke, sw, t0, t1, round) {
    var L = c.layers.addShape(); L.name = name;
    var g = L.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
    var rr = g.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Rect");
    rr.property("ADBE Vector Rect Size").setValue([w, h]); rr.property("ADBE Vector Rect Position").setValue([w / 2, h / 2]);
    if (round) rr.property("ADBE Vector Rect Roundness").setValue(round);
    var gp = L.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group");
    if (stroke) { var st = gp.addProperty("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Color").setValue(stroke); st.property("ADBE Vector Stroke Width").setValue(sw || 2); }
    if (fill) { var fl = L.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group").addProperty("ADBE Vector Graphic - Fill"); fl.property("ADBE Vector Fill Color").setValue(fill); }
    A(L).setValue([0, h / 2]); P(L).setValue([x, y + h / 2]);
    L.inPoint = t0; L.outPoint = t1;
    return L;
}
// a mono text block (JetBrains Mono), typed on with a two-key "typed" slider (linear: one character per step)
function typed(c, s, font, size, col, x, y, t0, t1, tOut, lead) {
    var L = txt(c, s, font || "JetBrainsMono-Regular", size, col || [1, 1, 1], ParagraphJustification.LEFT_JUSTIFY, 0, 0, 0);
    if (lead) { var td = L.property("Source Text").value; td.leading = lead; L.property("Source Text").setValue(td); }
    var r = rect(L); P(L).setValue([x - r.left, y - r.top]);
    L.inPoint = Math.max(0, t0 - fr(1)); L.outPoint = tOut;
    var n = s.length;
    var ctl = fx(L, "ADBE Slider Control"); ctl.name = "typed";
    k2(L.property("ADBE Effect Parade").property("typed").property(1), t0, 0, t1, n, "linear");
    var an = L.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
    an.property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity").setValue(0);
    var sel = an.property("ADBE Text Selectors").addProperty("ADBE Text Expressible Selector");
    sel.property("ADBE Text Expressible Amount").expression = 'textIndex > effect("typed")(1) ? 100 : 0';
    return L;
}
// one-frame RGB split glitch on a layer at time t (offset copies in Add for 1-2 frames)
function rgbHit(c, L, t, frames, px) {
    var f = frames || 2, d = px || 18, ch = [[1, 0, 0], [0, 0, 1]];
    for (var i = 0; i < 2; i++) {
        var X = L.duplicate(); X.name = L.name + " (split " + i + ")";
        X.inPoint = t; X.outPoint = t + fr(f); X.blendingMode = BlendingMode.ADD;
        chanOnly(X, i == 0 ? 0 : 2, "Channel");
        var p = P(X).value; P(X).setValue([p[0] + (i == 0 ? d : -d), p[1]]); O(X).setValue(80);
    }
}
// chanOnly(L, i, label) lives in motion_lib.jsx

// ---------------------------------------------------------------- the night grade (storyboard finish "ac") and the finish comp
// grade (black 0.04, gamma 1.06, contrast 1.16, saturation 0.84) + bloom (above 0.68, sigma 28 px = Blurriness 60, screen 50%)
function nightGrade(c, t0, t1, bloomOp) {
    var g = adjL(c, "night grade (crushed blacks, punch, less saturation)");
    eff(g, "ADBE Pro Levels2", "Black and gamma"); setE(g, "Black and gamma", "Input Black", 0.04); setE(g, "Black and gamma", "Gamma", 1 / 1.06);
    eff(g, "ADBE Pro Levels2", "Contrast"); setE(g, "Contrast", "Input Black", 0.5 - 0.5 / 1.16); setE(g, "Contrast", "Input White", 0.5 + 0.5 / 1.16);
    eff(g, "ADBE HUE SATURATION", "Saturation"); var ms = findProp(g.property("ADBE Effect Parade").property("Saturation"), "Master Saturation"); if (ms) { try { ms.setValue(-16); } catch (e) {} }
    var bl = adjL(c, "bloom (highlights above 68%, screened)");
    eff(bl, "ADBE Pro Levels2", "Highlights only"); setE(bl, "Highlights only", "Input Black", 0.68);
    eff(bl, "ADBE Gaussian Blur 2", "Bloom blur"); setE(bl, "Bloom blur", "Blurriness", 60); setE(bl, "Bloom blur", "Repeat Edge Pixels", 1);
    bl.blendingMode = BlendingMode.SCREEN; O(bl).setValue(bloomOp === undefined ? 50 : bloomOp);
    g.inPoint = t0; g.outPoint = t1; bl.inPoint = t0; bl.outPoint = t1;
    return g;
}
// paper/cork grade (storyboard "mmdark"): light contrast, small bloom
function paperGrade(c, t0, t1) {
    var g = adjL(c, "paper grade");
    eff(g, "ADBE Pro Levels2", "Black and gamma"); setE(g, "Black and gamma", "Input Black", 0.02); setE(g, "Black and gamma", "Gamma", 1 / 1.03);
    var bl = adjL(c, "paper bloom");
    eff(bl, "ADBE Pro Levels2", "Highlights only"); setE(bl, "Highlights only", "Input Black", 0.8);
    eff(bl, "ADBE Gaussian Blur 2", "Bloom blur"); setE(bl, "Bloom blur", "Blurriness", 48); setE(bl, "Bloom blur", "Repeat Edge Pixels", 1);
    bl.blendingMode = BlendingMode.SCREEN; O(bl).setValue(22);
    g.inPoint = t0; g.outPoint = t1; bl.inPoint = t0; bl.outPoint = t1;
}
// finish comp: black base, the content comp as three channel copies scaled apart (fringe), the tube vignette multiplied
// (per-shot vignette kind via o.vig = [[t0, t1, "ac"|"mm"|"mmdark"], ...]), a light soften and mono grain.
function finish(content, name, o) {
    o = o || {};
    var f = newComp(name, content.duration); filed(f, "Scenes (Dynamic Link)");
    solidL(f, "black base", [0, 0, 0]);
    var sc = [100.7, 100.35, 100];   // every channel at least full size, so bright frames get no coloured edge
    for (var i = 0; i < 3; i++) {
        var L = f.layers.add(content); L.name = ["red", "green", "blue"][i] + " (fringe)";
        chanOnly(L, i, "channel " + i);
        if (i > 0) L.blendingMode = BlendingMode.ADD;
        S(L).setValue([sc[i], sc[i]]);
        try { L.audioEnabled = false; } catch (ea) {}
    }
    var vs = o.vig || [[0, content.duration, "ac"]];
    for (var v = 0; v < vs.length; v++) {
        var vg = f.layers.add(impStill(VIG[vs[v][2]])); vg.name = "tube vignette (" + vs[v][2] + ")"; vg.blendingMode = BlendingMode.MULTIPLY;
        vg.inPoint = vs[v][0]; vg.outPoint = vs[v][1];
    }
    var soft = adjL(f, "soften"); eff(soft, "ADBE Gaussian Blur 2", "Soften"); setE(soft, "Soften", "Blurriness", 1.2); setE(soft, "Soften", "Repeat Edge Pixels", 1);
    var gr = adjL(f, "grain"); eff(gr, "ADBE Noise", "Grain"); setE(gr, "Grain", "Amount of Noise", 4); setE(gr, "Grain", "ADBE Noise-0002", 0);
    return f;
}
// scene(): content comp + finish comp; returns {c: content, f: finish}
function scene(name, dur) {
    var c = newComp(name + " content", dur); filed(c, "Scene content");
    return c;
}

// ---------------------------------------------------------------- moves made of two-key segments
// chain(prop, [[t, v], [t, v, style], ...]): each consecutive pair is one move (two keys) with that move's ease;
// every key has zero speed, so each move starts and lands cleanly. Spatial tangents are zeroed (straight paths).
function chain(prop, list) {
    var i, k;
    for (i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]);
    for (i = 0; i < list.length; i++) {
        k = prop.nearestKeyIndex(list[i][0]);
        var inS = i > 0 ? (list[i][2] || "gentle") : null, outS = i < list.length - 1 ? (list[i + 1][2] || "gentle") : null;
        if (inS == "hold" || outS == "hold") { prop.setInterpolationTypeAtKey(k, inS == "hold" ? KeyframeInterpolationType.HOLD : KeyframeInterpolationType.BEZIER, outS == "hold" ? KeyframeInterpolationType.HOLD : KeyframeInterpolationType.BEZIER); }
        if (inS == "linear" || outS == "linear") { prop.setInterpolationTypeAtKey(k, inS == "linear" ? KeyframeInterpolationType.LINEAR : KeyframeInterpolationType.BEZIER, outS == "linear" ? KeyframeInterpolationType.LINEAR : KeyframeInterpolationType.BEZIER); }
        var inInf = (inS && EASES[inS]) ? EASES[inS][1] : 33.3, outInf = (outS && EASES[outS]) ? EASES[outS][0] : 33.3;
        if (inS != "linear" && outS != "linear" && inS != "hold" && outS != "hold") setEase(prop, k, inInf, outInf);
        if (prop.isSpatial) { try { prop.setSpatialTangentsAtKey(k, [0, 0], [0, 0]); } catch (es) {} }
    }
}
// camera on a (collapsed) world layer: frames = [[t, [ax, ay], scalePct, style], ...]
function camera(L, frames) {
    var a = [], s = [];
    for (var i = 0; i < frames.length; i++) { a.push([frames[i][0], frames[i][1], frames[i][3]]); s.push([frames[i][0], [frames[i][2], frames[i][2]], frames[i][3]]); }
    P(L).setValue([W / 2, H / 2]);
    chain(A(L), a); chain(S(L), s);
}
function nullL(c, name, x, y) { var n = c.layers.addNull(c.duration); n.name = name; A(n).setValue([0, 0]); P(n).setValue([x, y]); return n; }
// parent a layer to p and set its transform in p's space (p's anchor is its origin)
function child(L, p, x, y, sPct, rot) { L.parent = p; P(L).setValue([x, y]); if (sPct !== undefined) S(L).setValue([sPct, sPct]); R(L).setValue(rot || 0); return L; }
// soft blur bands (shallow depth of field): blurred adjustment layers masked to top and bottom bands with feather
function dofBands(c, t0, t1, top, bottom, blur) {
    var out = [];
    var specs = [[0, top], [bottom, H]];
    for (var i = 0; i < 2; i++) {
        var a = adjL(c, "depth of field " + (i ? "bottom" : "top")); a.inPoint = t0; a.outPoint = t1;
        var y0 = specs[i][0], y1 = specs[i][1], m = a.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        var sh = new Shape(); sh.vertices = [[-50, y0 - (i ? 0 : 200)], [W + 50, y0 - (i ? 0 : 200)], [W + 50, y1 + (i ? 200 : 0)], [-50, y1 + (i ? 200 : 0)]]; sh.closed = true;
        m.property("ADBE Mask Shape").setValue(sh); m.property("ADBE Mask Feather").setValue([220, 220]);
        boxBlur(a, blur || 10, 0);
        chain(O(a), [[t0, 0], [t0 + fr(6), 100, "settle"], [t1 - fr(4), 100, "linear"], [t1, 0, "accel"]]);
        out.push(a);
    }
    return out;
}
// a rectangle matte solid in a layer's own space (for reveals), not visible
function matteSolid(c, name, w, h) { var s = solidL(c, name, [1, 1, 1], Math.round(w), Math.round(h)); s.enabled = false; return s; }

// ---------------------------------------------------------------- review helper
// testComp: a short comp that shows the finish comp at chosen times, for fast sample renders. Sample i sits on frame 2i
// and plays at normal speed through that frame (linear remap keys half a frame either side), so motion blur is real;
// the odd frames carry the jumps between samples and are thrown away.
function testComp(f, times, name) {
    var n = times.length, tc = app.project.items.addComp(name, W, H, 1, Math.max(2, 2 * n) / FPS, FPS);
    filed(tc, "_tests");
    var L = tc.layers.add(f); L.timeRemapEnabled = true;
    var trm = L.property("ADBE Time Remapping"), i, k, ks = [];
    for (i = 0; i < n; i++) {
        var a = (2 * i - 0.5) / FPS, b = (2 * i + 0.5) / FPS;
        if (a >= 0) { trm.setValueAtTime(a, Math.max(0, times[i] - 0.5 / FPS)); ks.push(a); }
        else { trm.setValueAtTime(0, times[i]); ks.push(0); }
        trm.setValueAtTime(b, times[i] + 0.5 / FPS); ks.push(b);
    }
    for (k = trm.numKeys; k >= 1; k--) { var kt = trm.keyTime(k), ours = false; for (i = 0; i < ks.length; i++) if (Math.abs(kt - ks[i]) < 1e-4) ours = true; if (!ours) trm.removeKey(k); }
    for (k = 1; k <= trm.numKeys; k++) trm.setInterpolationTypeAtKey(k, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
    L.outPoint = tc.duration;
    return tc;
}

// ---------------------------------------------------------------- ordered dither in a zone (native: Mosaic, a Bayer
// threshold map in Linear Light, Posterize). zone = mask vertices in comp px; feather softens the edge of the zone.
function ditherZone(c, t0, t1, zone, feather, cell, levels, amt, name) {
    var mk = function (L) {
        var m = L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"); var sh = new Shape(); sh.vertices = zone; sh.closed = true;
        m.property("ADBE Mask Shape").setValue(sh); m.property("ADBE Mask Feather").setValue([feather, feather]); return m;
    };
    var a = adjL(c, (name || "dither") + ": blocks"); eff(a, "ADBE Mosaic", "Mosaic");
    setE(a, "Mosaic", "Horizontal Blocks", Math.round(W / cell)); setE(a, "Mosaic", "Vertical Blocks", Math.round(H / cell)); setE(a, "Mosaic", "Sharp Colors", 1);
    mk(a); a.inPoint = t0; a.outPoint = t1;
    var b = c.layers.add(impStill(BAYER + "bayer_" + cell + "px.png")); b.name = (name || "dither") + ": threshold map";
    b.blendingMode = BlendingMode.LINEAR_LIGHT; O(b).setValue(amt || 22); mk(b); b.inPoint = t0; b.outPoint = t1;
    var p = adjL(c, (name || "dither") + ": steps"); eff(p, "ADBE Posterize", "Posterize"); setE(p, "Posterize", "Level", levels || 5);
    mk(p); p.inPoint = t0; p.outPoint = t1;
    return [a, b, p];
}
