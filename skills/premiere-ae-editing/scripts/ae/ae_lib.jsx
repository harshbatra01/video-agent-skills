// ae_lib.jsx: After Effects 2026 ExtendScript helpers (ES3: no let/const, arrow functions, indexOf, map, JSON).
// Needs the globals the ae_build.py header defines: W, H, FPS, HERE, LOG, LOGNAME, writeFile(), SHOTS.
// Every helper here dodges a trap that cost a render round on a real job; the comment says which.

function log(s) { LOG.push(s); writeFile(HERE + LOGNAME, LOG.join("\n")); }
function inArr(a, v) { for (var i = 0; i < a.length; i++) if (a[i] == v) return true; return false; }

// ---------------------------------------------------------------- properties and keys
function tr(l) { return l.property("ADBE Transform Group"); }
function P(l) { return tr(l).property("ADBE Position"); }
function S(l) { return tr(l).property("ADBE Scale"); }
function O(l) { return tr(l).property("ADBE Opacity"); }
function R(l) { return tr(l).property("ADBE Rotate Z"); }
function A(l) { return tr(l).property("ADBE Anchor Point"); }
// Adding an effect or a shape property INVALIDATES earlier handles on that layer: always re-fetch after adding.
function fx(l, mn) { l.property("ADBE Effect Parade").addProperty(mn); var ep = l.property("ADBE Effect Parade"); return ep.property(ep.numProperties); }
function setp(eff, name, v) { try { eff.property(name).setValue(v); } catch (e) { log("  param " + name + ": " + e.toString()); } }
// Nested params (Fractal Noise > Transform > Scale, Keylight groups) are only reachable by a recursive search.
function findProp(g, name) {
    for (var i = 1; i <= g.numProperties; i++) {
        var p = g.property(i);
        if (p.propertyType == PropertyType.PROPERTY) { if (p.name == name || p.matchName == name) return p; }
        else { var r = findProp(p, name); if (r) return r; }
    }
    return null;
}
function setDeep(eff, name, v) { var p = findProp(eff, name); if (p) { try { p.setValue(v); } catch (e) { log("  deep " + name + ": " + e.toString()); } } else log("  deep " + name + ": not found"); }
function easeKey(prop, idx, inInf, outInf) {
    var n = 1;
    if (!prop.isSpatial && (prop.propertyValueType == PropertyValueType.TwoD || prop.propertyValueType == PropertyValueType.ThreeD)) n = prop.keyValue(idx).length;
    var a = [], b = [];
    for (var i = 0; i < n; i++) { a.push(new KeyframeEase(0, inInf)); b.push(new KeyframeEase(0, outInf)); }
    try { prop.setTemporalEaseAtKey(idx, a, b); } catch (e) {}
}
// keys(prop, [[t, value, inInfluence?, outInfluence?], ...]) eased keys (33 = gentle, 75-90 = strong ease)
// Some params cannot vary over time (Levels "Output White"): they get the last value and a log line instead.
function keys(prop, list) {
    if (!prop.canVaryOverTime) { log("  cannot key " + prop.name); try { prop.setValue(list[list.length - 1][1]); } catch (e) {} return; }
    for (var i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]);
    for (var j = 0; j < list.length; j++) easeKey(prop, prop.nearestKeyIndex(list[j][0]), list[j][2] || 33.3, list[j][3] || 33.3);
}
function linearKeys(prop) { for (var j = 1; j <= prop.numKeys; j++) prop.setInterpolationTypeAtKey(j, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR); }

// ---------------------------------------------------------------- comps, footage, layers
// Never READ comp.bgColor in AE 2026 (throws "invalid numeric result"); setting it is fine.
function newComp(name, dur, w, h) { var c = app.project.items.addComp(name, w || W, h || H, 1, dur, FPS); c.bgColor = [0, 0, 0]; return c; }
var IMP = {};
function imp(path) {   // cached import; PNG cutouts need STRAIGHT alpha or edges go dark
    if (IMP[path]) return IMP[path];
    var it = app.project.importFile(new ImportOptions(new File(path)));
    try { it.mainSource.alphaMode = AlphaMode.STRAIGHT; } catch (e) {}
    IMP[path] = it; return it;
}
function solidL(comp, name, color, w, h) { return comp.layers.addSolid(color, name, w || comp.width, h || comp.height, 1, comp.duration); }
function adjL(comp, name) { var a = solidL(comp, name || "adjust", [1, 1, 1]); a.adjustmentLayer = true; return a; }
// cover the frame with an image/footage layer using a crop rect [x0, y0, x1, y1] in source px
function cover(l, crop, cw, ch) {
    var src = l.source, x0 = crop ? crop[0] : 0, y0 = crop ? crop[1] : 0, x1 = crop ? crop[2] : src.width, y1 = crop ? crop[3] : src.height;
    var s = Math.max((cw || W) / (x1 - x0), (ch || H) / (y1 - y0)) * 100;
    A(l).setValue([(x0 + x1) / 2, (y0 + y1) / 2]); P(l).setValue([(cw || W) / 2, (ch || H) / 2]); S(l).setValue([s, s]);
    return s;
}
// footage with optional time remap rk = [[comp t, source t], ...]. AE adds its own first/last keys: remove ONLY those.
// Removing ALL keys switches time remapping off and the next setValueAtTime throws "property ... is hidden".
function remapL(comp, file, rk) {
    var L = comp.layers.add(imp(file));
    if (rk && L.canSetTimeRemapEnabled) {
        L.timeRemapEnabled = true;
        var tm = L.property("ADBE Time Remapping");
        for (var i = 0; i < rk.length; i++) tm.setValueAtTime(rk[i][0], rk[i][1]);
        for (var j = tm.numKeys; j >= 1; j--) {
            var kt = tm.keyTime(j), mine = false;
            for (var q = 0; q < rk.length; q++) if (Math.abs(rk[q][0] - kt) < 0.0005) mine = true;
            if (!mine) tm.removeKey(j);
        }
        linearKeys(tm);
    }
    L.startTime = 0; L.inPoint = 0; L.outPoint = comp.duration;
    return L;
}
// green/blue screen key (values that keyed Blender green screens cleanly). rgb = screen colour 0-255.
function keyL(comp, file, rgb, rk) {
    var L = remapL(comp, file, rk);
    var kl = fx(L, "Keylight 906");
    try {
        findProp(kl, "Screen Colour").setValue([rgb[0] / 255, rgb[1] / 255, rgb[2] / 255]);
        findProp(kl, "Clip Black").setValue(12); findProp(kl, "Clip White").setValue(88); findProp(kl, "Screen Shrink/Grow").setValue(-0.5);
    } catch (e) { log("  keylight " + e.toString()); }
    return L;
}
// track matte (AE 2023+ API). The matte layer must be hidden.
function matte(layer, matteLayer, type) { layer.setTrackMatte(matteLayer, type || TrackMatteType.ALPHA); matteLayer.enabled = false; }

// ---------------------------------------------------------------- text
// Fonts are PostScript names: "ProximaNova-Semibold", "ProximaNova-Regular", "Montserrat-Black", "SegoeUI-Semibold".
// A missing glyph renders BLANK, no error: Proxima has no check mark, arrows, approx, star or not-equal; Montserrat-Black
// has no check mark. GLYPH_FALLBACK swaps the font for strings holding those (or draw them: checkL, neq shapes).
// macOS has no Segoe UI: there the fallback is ArialUnicodeMS (one weight, has all of these glyphs; on the Mac the port
// was tested on, Proxima Nova and Inter lacked the heavy check mark, Montserrat-Black lacked star and check marks).
// Check a font there with: scripts/media/fontcheck --text "<string>" Font-Name
var GLYPH_FALLBACK = (File.fs == "Macintosh") ? "ArialUnicodeMS" : "SegoeUI-Semibold";
function txt(comp, s, font, size, color, just, tracking, x, y) {
    if (GLYPH_FALLBACK && /[≠→←≈★✓✔×]/.test(s)) font = GLYPH_FALLBACK;
    var l = comp.layers.addText(s);
    var p = l.property("Source Text"), d = p.value;
    d.resetCharStyle(); d.resetParagraphStyle();
    d.font = font; d.fontSize = size; d.applyFill = true; d.fillColor = color; d.applyStroke = false;
    d.tracking = tracking || 0; d.justification = just || ParagraphJustification.CENTER_JUSTIFY;
    p.setValue(d); P(l).setValue([x, y]);
    return l;
}
function rect(l, t) { return l.sourceRectAtTime(t || 0, false); }      // measured box, for plates sized to the text
function centreAnchor(l) {
    var r = rect(l), p = P(l).value, ax = r.left + r.width / 2, ay = r.top + r.height / 2;
    A(l).setValue([ax, ay]); P(l).setValue([p[0] + ax, p[1] + ay]); return r;
}
function typeOn(l, t0, cps) { l.property("Source Text").expression = "var s = value.toString(); var n = Math.floor(Math.max(0, (time - " + t0 + ") * " + (cps || 18) + ")); s.substr(0, n);"; }
// dark plate behind small text (small white text straight on footage was rejected as unreadable)
function pill(comp, label, x, y, size, fill, color, tIn) {
    var t = txt(comp, label, "ProximaNova-Semibold", size || 30, color || [1, 1, 1], ParagraphJustification.LEFT_JUSTIFY, 10, 0, 0);
    var r = rect(t), padX = 22, padY = 12;
    var b = rrect(comp, "pill " + label, r.width + padX * 2, r.height + padY * 2, (r.height + padY * 2) / 2, fill || [0.08, 0.07, 0.07], null, 0, 0, 0);
    O(b).setValue(88);
    P(b).setValue([x + (r.width + padX * 2) / 2, y]);
    P(t).setValue([x + padX - r.left, y - r.top - r.height / 2]);
    t.moveBefore(b);       // layers made earlier sit UNDER later ones: put text above its plate explicitly
    if (tIn !== undefined && tIn !== null) {
        var ls = [b, t];
        for (var i = 0; i < 2; i++) { keys(O(ls[i]), [[tIn, 0], [tIn + 0.2, i == 0 ? 88 : 100]]); var p0 = P(ls[i]).value; keys(P(ls[i]), [[tIn, [p0[0] - 30, p0[1]]], [tIn + 0.3, p0, 70, 33]]); }
    }
    return [b, t];
}

// ---------------------------------------------------------------- shapes
// New shape layers sit at the comp centre: set Position [0,0] when drawing paths in comp coordinates.
function shapeGroup(l) { return l.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group").property("ADBE Vectors Group"); }
function groupOf(l) { return l.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group"); }
function trimOf(l) { var g = groupOf(l); for (var q = 1; q <= g.numProperties; q++) if (g.property(q).matchName == "ADBE Vector Filter - Trim") return g.property(q); return null; }
function rrect(comp, name, w, h, r, fill, stroke, sw, x, y) {
    var l = comp.layers.addShape(); l.name = name;
    var gc = shapeGroup(l);
    var rc = gc.addProperty("ADBE Vector Shape - Rect");
    rc.property("ADBE Vector Rect Size").setValue([w, h]); rc.property("ADBE Vector Rect Roundness").setValue(r);
    if (stroke) { var st = gc.addProperty("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Color").setValue(stroke); st.property("ADBE Vector Stroke Width").setValue(sw || 2); }
    if (fill) { var f = groupOf(l).addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(fill); }
    P(l).setValue([x, y]); return l;
}
function ellipseL(comp, name, w, h, fill, x, y, stroke, sw) {
    var l = comp.layers.addShape(); l.name = name;
    var gc = shapeGroup(l);
    gc.addProperty("ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size").setValue([w, h]);
    if (stroke) { var st = groupOf(l).addProperty("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Color").setValue(stroke); st.property("ADBE Vector Stroke Width").setValue(sw || 2); }
    if (fill) { var f = groupOf(l).addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(fill); }
    P(l).setValue([x, y]); return l;
}
// smooth path through points (Catmull-Rom style tangents); sharp = vertex indexes kept as corners
function crShape(v, closed, sharp, k) {
    k = k || 1 / 6; var n = v.length, inT = [], outT = [];
    for (var i = 0; i < n; i++) {
        var a = v[(i - 1 + n) % n], b = v[(i + 1) % n];
        if (!closed && i == 0) a = v[0]; if (!closed && i == n - 1) b = v[n - 1];
        var d = (sharp && inArr(sharp, i)) ? [0, 0] : [(b[0] - a[0]) * k, (b[1] - a[1]) * k];
        inT.push([-d[0], -d[1]]); outT.push([d[0], d[1]]);
    }
    var s = new Shape(); s.vertices = v; s.closed = !!closed; s.inTangents = inT; s.outTangents = outT; return s;
}
// stroked path drawn on with Trim Paths between t0 and t1 (round caps)
function drawPath(comp, name, verts, color, width, t0, t1, closed, smooth) {
    var l = comp.layers.addShape(); l.name = name; P(l).setValue([0, 0]);
    var gc = shapeGroup(l), sh;
    if (smooth) sh = crShape(verts, !!closed); else { sh = new Shape(); sh.vertices = verts; sh.closed = !!closed; }
    gc.addProperty("ADBE Vector Shape - Group").property("ADBE Vector Shape").setValue(sh);
    groupOf(l).addProperty("ADBE Vector Filter - Trim");
    var st = groupOf(l).addProperty("ADBE Vector Graphic - Stroke");
    st.property("ADBE Vector Stroke Color").setValue(color); st.property("ADBE Vector Stroke Width").setValue(width);
    st = groupOf(l).property("ADBE Vector Graphic - Stroke");
    st.property("ADBE Vector Stroke Line Cap").setValue(2); st.property("ADBE Vector Stroke Line Join").setValue(2);
    var tm = trimOf(l);
    if (t1 > t0) keys(tm.property("ADBE Vector Trim End"), [[t0, 0], [t1, 100, 33, 80]]); else tm.property("ADBE Vector Trim End").setValue(100);
    return l;
}
function strokeLine(comp, name, p0, p1, color, width, t0, t1) { return drawPath(comp, name, [p0, p1], color, width, t0, t1, false, false); }
// drawn check mark (no font here has a safe check glyph)
function checkL(comp, x, y, s, col, w) { return drawPath(comp, "check", [[x - 0.45 * s, y + 0.02 * s], [x - 0.12 * s, y + 0.34 * s], [x + 0.48 * s, y - 0.32 * s]], col, w, 0, 0, false, false); }
// outline box drawn around a rect [x, y, w, h] (prices, claims)
// stack order matters: path, THEN Trim Paths, THEN Stroke (an operator only changes what is above it)
function outlineBox(comp, r, t, color, sw) {
    var l = comp.layers.addShape(); l.name = "box";
    var gc = shapeGroup(l);
    var rc = gc.addProperty("ADBE Vector Shape - Rect");
    rc.property("ADBE Vector Rect Size").setValue([r[2] + 26, r[3] + 22]); rc.property("ADBE Vector Rect Roundness").setValue(14);
    groupOf(l).addProperty("ADBE Vector Filter - Trim");
    var st = groupOf(l).addProperty("ADBE Vector Graphic - Stroke");
    st.property("ADBE Vector Stroke Color").setValue(color || [0.86, 0.16, 0.2]); st.property("ADBE Vector Stroke Width").setValue(sw || 7);
    keys(trimOf(l).property("ADBE Vector Trim End"), [[t, 0], [t + 0.35, 100, 33, 75]]);
    P(l).setValue([r[0] + r[2] / 2, r[1] + r[3] / 2]);
    return l;
}
// highlighter sweeps over text lines of a screenshot (rects from OCR, layer px), MULTIPLY so the words stay crisp
function highlighter(comp, rects, t, dur, color, op) {
    var out = [];
    for (var i = 0; i < rects.length; i++) {
        var r = rects[i], y = r[1] + r[3] / 2;
        var l = strokeLine(comp, "hl" + i, [r[0], y], [r[0] + r[2], y], color || [1, 0.84, 0.24], r[3] * 1.05, t + i * dur * 0.9, t + i * dur * 0.9 + dur);
        groupOf(l).property("ADBE Vector Graphic - Stroke").property("ADBE Vector Stroke Line Cap").setValue(1);
        l.blendingMode = BlendingMode.MULTIPLY; O(l).setValue(op || 80);
        out.push(l);
    }
    return out;
}

// ---------------------------------------------------------------- glows, blurs, light
// Effects on SHAPE layers are clipped to the shape's bounding box: a blurred ellipse shows square edges (the
// "glow cut off as a square" note). Soft light = comp-size SOLID + feathered mask instead:
function softEllipse(c, name, w, h, col, x, y, feather, op) {
    var s = solidL(c, name, col);
    var m = s.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var k = 0.5523, rx = w / 2, ry = h / 2, sh = new Shape();
    sh.vertices = [[x, y - ry], [x + rx, y], [x, y + ry], [x - rx, y]];
    sh.inTangents = [[-k * rx, 0], [0, -k * ry], [k * rx, 0], [0, k * ry]];
    sh.outTangents = [[k * rx, 0], [0, k * ry], [-k * rx, 0], [0, -k * ry]];
    sh.closed = true; m.property("ADBE Mask Shape").setValue(sh);
    m.property("ADBE Mask Feather").setValue([feather || 200, feather || 200]);
    O(s).setValue(op === undefined ? 100 : op);
    return s;
}
function softBand(c, name, col, y0, y1, feather, op) {   // soft horizontal band (floor shadow, light strip)
    var s = solidL(c, name, col);
    var m = s.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"); var sh = new Shape();
    sh.vertices = [[-400, y0], [c.width + 400, y0], [c.width + 400, y1], [-400, y1]]; sh.closed = true;
    m.property("ADBE Mask Shape").setValue(sh); m.property("ADBE Mask Feather").setValue([0, feather || 120]);
    O(s).setValue(op === undefined ? 100 : op);
    return s;
}
// Gaussian blur with Repeat Edge Pixels OFF (on, it also clips glows/shadows to the content box)
function gaussBlur(l, r) { var b = fx(l, "ADBE Gaussian Blur 2"); setp(b, "ADBE Gaussian Blur 2-0001", r); setp(b, "ADBE Gaussian Blur 2-0003", 0); return b; }
function boxBlur(l, r, rep) { var b = fx(l, "ADBE Box Blur2"); setp(b, "Blur Radius", r); setp(b, "Iterations", 3); if (rep !== undefined) setp(b, "Repeat Edge Pixels", rep); return b; }   // Fast Box Blur: far lighter than Camera Lens Blur on big precomps
function lensBlur(l, r) { var b = fx(l, "ADBE Camera Lens Blur"); setp(b, "Blur Radius", r); return b; }
function shadow(l, op, dist, soft, dir) {
    var d = fx(l, "ADBE Drop Shadow");
    d.property("ADBE Drop Shadow-0002").setValue(op * 255); d.property("ADBE Drop Shadow-0003").setValue(dir || 160);
    d.property("ADBE Drop Shadow-0004").setValue(dist); d.property("ADBE Drop Shadow-0005").setValue(soft); return d;
}
function glow(l, thresh, radius, intensity) { var g = fx(l, "ADBE Glo2"); setp(g, "Glow Threshold", thresh); setp(g, "Glow Radius", radius); setp(g, "Glow Intensity", intensity); return g; }
// darken: Levels Output White cannot be keyed; use exposure() when it must animate
function levels(l, outWhite, outBlack, gamma) {
    var v = fx(l, "ADBE Easy Levels2");
    if (outWhite !== null && outWhite !== undefined) setp(v, "Output White", outWhite);
    if (outBlack) setp(v, "Output Black", outBlack);
    if (gamma) setp(v, "Gamma", gamma); return v;
}
function exposure(l, stops) { var e = fx(l, "ADBE Exposure2"); setp(e, "Exposure", stops || 0); return e; }
function tint(l, black, white, amt) { var t = fx(l, "ADBE Tint"); setp(t, "Map Black To", black); setp(t, "Map White To", white); setp(t, "Amount to Tint", amt); return t; }
// Lumetri basics in AE (matchNames found by dumping a real Lumetri)
function lumetri(l, cc) {
    var lu = fx(l, "ADBE Lumetri");
    var map = { temp: "ADBE Lumetri-0007", tint: "ADBE Lumetri-0008", sat: "ADBE Lumetri-0020", exp: "ADBE Lumetri-0011", con: "ADBE Lumetri-0012",
                hi: "ADBE Lumetri-0013", sh: "ADBE Lumetri-0014", whites: "ADBE Lumetri-0015", blacks: "ADBE Lumetri-0016" };
    for (var k in cc) if (map[k]) { try { lu.property(map[k]).setValue(cc[k]); } catch (e) { log("  lumetri " + k + ": " + e.toString()); } }
    return lu;
}
function vignette(comp, amount) {
    var v = solidL(comp, "vignette", [0, 0, 0]);
    var m = v.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape(), w = comp.width, h = comp.height;
    s.vertices = [[w * 0.5, -h * 0.12], [w * 1.12, h * 0.5], [w * 0.5, h * 1.12], [-w * 0.12, h * 0.5]];
    s.inTangents = [[-w * 0.36, 0], [0, -h * 0.36], [w * 0.36, 0], [0, h * 0.36]]; s.outTangents = [[w * 0.36, 0], [0, h * 0.36], [-w * 0.36, 0], [0, -h * 0.36]];
    s.closed = true; m.property("ADBE Mask Shape").setValue(s); m.property("ADBE Mask Feather").setValue([w * 0.25, w * 0.25]);
    m.inverted = true; O(v).setValue(amount); return v;
}
function grain(comp, amount) { var a = adjL(comp, "grain"); setp(fx(a, "ADBE Noise"), "Amount of Noise", amount || 5); return a; }

// ---------------------------------------------------------------- motion
function popIn(l, t, over) {
    var s = S(l).value[0];
    keys(S(l), [[t, [0, 0]], [t + 0.16, [s * (over || 1.1), s * (over || 1.1)], 60, 40], [t + 0.28, [s, s], 50, 70]]);
    keys(O(l), [[t, 0], [t + 0.06, 100]]);
}
function flyIn(L, t, from, dur) {   // from = [dx, dy, dRotation]
    var p = P(L).value, r = R(L).value;
    keys(P(L), [[t, [p[0] + from[0], p[1] + from[1]]], [t + (dur || 0.35), p, 85, 33]]);
    keys(R(L), [[t, r + (from[2] || 0)], [t + (dur || 0.35), r, 85, 33]]);
    keys(O(L), [[t, 0], [t + 0.08, 100]]);
}
function slowPush(l, t0, t1, k) { var s = S(l).value; keys(S(l), [[t0, s], [t1, [s[0] * (k || 1.04), s[1] * (k || 1.04)]]]); }

// ---------------------------------------------------------------- cards
// image card: white paper + masked crop of a screenshot/photo, sized to width w, shadow, motion blur.
// returns {layer, comp, w, h, ox, oy, s}: source px (sx, sy) sit at card px (sx + ox, sy + oy).
function imgCard(comp, name, file, crop, w, x, y, rot, dur) {
    var cr = crop, pad = 18;
    var cw = Math.round(cr[2] - cr[0] + pad * 2), ch = Math.round(cr[3] - cr[1] + pad * 2);
    var cc = newComp(name, dur || comp.duration, cw, ch);
    rrect(cc, "paper", cw, ch, 16, [1, 1, 1], null, 0, cw / 2, ch / 2);
    var sh = cc.layers.add(imp(file)); A(sh).setValue([(cr[0] + cr[2]) / 2, (cr[1] + cr[3]) / 2]); P(sh).setValue([cw / 2, ch / 2]);
    var m = sh.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"); var ms = new Shape();
    ms.vertices = [[cr[0], cr[1]], [cr[2], cr[1]], [cr[2], cr[3]], [cr[0], cr[3]]]; ms.closed = true; m.property("ADBE Mask Shape").setValue(ms);
    var L = comp.layers.add(cc); L.name = name; var s = w / cw * 100; S(L).setValue([s, s]); P(L).setValue([x, y]); R(L).setValue(rot || 0);
    shadow(L, 0.5, 22, 44); L.motionBlur = true;
    return { layer: L, comp: cc, w: cw, h: ch, ox: pad - cr[0], oy: pad - cr[1], s: s };
}
// blurred, dimmed full-frame background from a still (room plate, photo) with a slow push
function stillBg(c, file, blur, dim, crop) { var b = c.layers.add(imp(file)); var s0 = cover(b, crop || null); boxBlur(b, blur || 30, 1); levels(b, dim || 0.45); keys(S(b), [[0, [s0, s0]], [c.duration, [s0 * 1.04, s0 * 1.04]]]); return b; }
