// ---------------------------------------------------------------- helpers
function easeKey(prop, idx, inInf, outInf) {
    var n = 1;
    if (!prop.isSpatial && (prop.propertyValueType == PropertyValueType.TwoD || prop.propertyValueType == PropertyValueType.ThreeD)) n = prop.keyValue(idx).length;
    var a = [], b = [];
    for (var i = 0; i < n; i++) { a.push(new KeyframeEase(0, inInf)); b.push(new KeyframeEase(0, outInf)); }
    prop.setTemporalEaseAtKey(idx, a, b);
}
// keys(prop, [[t, v, inInfluence, outInfluence], ...]) ; influences default 33
function keys(prop, list) {
    for (var i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]);
    for (var j = 0; j < list.length; j++) easeKey(prop, prop.nearestKeyIndex(list[j][0]), list[j][2] || 33.3, list[j][3] || 33.3);
}
function tr(l) { return l.property("ADBE Transform Group"); }
function P(l) { return tr(l).property("ADBE Position"); }
function S(l) { return tr(l).property("ADBE Scale"); }
function O(l) { return tr(l).property("ADBE Opacity"); }
function R(l) { return tr(l).property("ADBE Rotate Z"); }
function A(l) { return tr(l).property("ADBE Anchor Point"); }
function fx(l, mn) { return l.property("ADBE Effect Parade").addProperty(mn); }
function newComp(name, dur) { var c = app.project.items.addComp(name, W, H, 1, dur, FPS); c.bgColor = [0, 0, 0]; return c; }

function txt(comp, s, font, size, color, just, tracking, x, y) {
    var l = comp.layers.addText(s);
    var p = l.property("Source Text"), d = p.value;
    d.resetCharStyle(); d.resetParagraphStyle();
    d.font = font; d.fontSize = size; d.applyFill = true; d.fillColor = color; d.applyStroke = false;
    d.tracking = tracking || 0; d.justification = just || ParagraphJustification.CENTER_JUSTIFY;
    p.setValue(d);
    P(l).setValue([x, y]);
    return l;
}
function boxTxt(comp, s, font, size, color, w, leading, x0, y0) {
    var l = comp.layers.addBoxText([w, 900], s);
    var p = l.property("Source Text"), d = p.value;
    d.resetCharStyle(); d.resetParagraphStyle();
    d.font = font; d.fontSize = size; d.applyFill = true; d.fillColor = color; d.applyStroke = false;
    d.justification = ParagraphJustification.LEFT_JUSTIFY; d.autoLeading = false; d.leading = leading;
    p.setValue(d);
    var r = l.sourceRectAtTime(0, false);
    P(l).setValue([x0 - r.left, y0 - r.top]);
    return l;
}
function rect(l) { return l.sourceRectAtTime(0, false); }
function fitWidth(l, maxW) {
    var r = rect(l);
    if (r.width > maxW) { var p = l.property("Source Text"), d = p.value; d.fontSize = d.fontSize * maxW / r.width; p.setValue(d); }
    return rect(l);
}
// put the anchor at the visual centre of the text so scale pops from the middle; keep it where it was
function centreAnchor(l) {
    var r = rect(l), p = P(l).value, ax = r.left + r.width / 2, ay = r.top + r.height / 2;
    A(l).setValue([ax, ay]); P(l).setValue([p[0] + ax, p[1] + ay]);
    return r;
}
function shapeGroup(l) { return l.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group").property("ADBE Vectors Group"); }
function findIn(l, mn) {
    var gc = l.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group");
    for (var i = 1; i <= gc.numProperties; i++) if (gc.property(i).matchName == mn) return gc.property(i);
    return null;
}
// rounded rectangle centred on the layer origin; returns layer
function rrect(comp, name, w, h, r, fill, stroke, sw, x, y) {
    var l = comp.layers.addShape(); l.name = name;
    var gc = shapeGroup(l);
    var rc = gc.addProperty("ADBE Vector Shape - Rect");
    rc.property("ADBE Vector Rect Size").setValue([w, h]); rc.property("ADBE Vector Rect Roundness").setValue(r);
    if (stroke) { var st = gc.addProperty("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Color").setValue(stroke); st.property("ADBE Vector Stroke Width").setValue(sw || 2); }
    if (fill) { var f = gc.addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(fill); }
    P(l).setValue([x, y]);
    return l;
}
function ellipse(comp, name, d, fill, stroke, sw, x, y) {
    var l = comp.layers.addShape(); l.name = name;
    var gc = shapeGroup(l);
    gc.addProperty("ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size").setValue([d, d]);
    if (stroke) { var st = gc.addProperty("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Color").setValue(stroke); st.property("ADBE Vector Stroke Width").setValue(sw || 2); st.property("ADBE Vector Stroke Line Cap").setValue(2); }
    if (fill) { var f = gc.addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(fill); }
    P(l).setValue([x, y]);
    return l;
}
function tickPath(comp, name, size, color, sw, x, y) {
    var l = comp.layers.addShape(); l.name = name;
    var gc = shapeGroup(l);
    var pth = gc.addProperty("ADBE Vector Shape - Group");
    var s = new Shape(); s.vertices = [[-0.42 * size, 0.02 * size], [-0.1 * size, 0.33 * size], [0.45 * size, -0.36 * size]]; s.closed = false;
    pth.property("ADBE Vector Shape").setValue(s);
    gc.addProperty("ADBE Vector Filter - Trim");
    var st = gc.addProperty("ADBE Vector Graphic - Stroke");
    st.property("ADBE Vector Stroke Color").setValue(color); st.property("ADBE Vector Stroke Width").setValue(sw);
    st.property("ADBE Vector Stroke Line Cap").setValue(2); st.property("ADBE Vector Stroke Line Join").setValue(2);
    P(l).setValue([x, y]);
    return l;
}
function solid(comp, name, color) { return comp.layers.addSolid(color, name, W, H, 1, comp.duration); }
function rectMask(l, x0, y0, x1, y1, feather) {
    var m = l.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    var s = new Shape(); s.vertices = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]; s.closed = true;
    m.property("ADBE Mask Shape").setValue(s);
    if (feather) m.property("ADBE Mask Feather").setValue([feather, feather]);
    return m;
}
function matte(l, m) { try { l.setTrackMatte(m, TrackMatteType.ALPHA); } catch (e) { l.trackMatteType = TrackMatteType.ALPHA; } }
function shadow(l, op, dist, soft) {
    var d = fx(l, "ADBE Drop Shadow");
    d.property("ADBE Drop Shadow-0002").setValue(op * 255); d.property("ADBE Drop Shadow-0003").setValue(180);
    d.property("ADBE Drop Shadow-0004").setValue(dist); d.property("ADBE Drop Shadow-0005").setValue(soft);
}
function glow(l, thresh, radius, intensity) {
    var g = fx(l, "ADBE Glo2");
    g.property("Glow Threshold").setValue(thresh); g.property("Glow Radius").setValue(radius); g.property("Glow Intensity").setValue(intensity);
    return g;
}
function gradText(l, top, bottom) {
    var r = rect(l), g = fx(l, "ADBE Ramp");
    g.property("ADBE Ramp-0001").setValue([0, r.top]); g.property("ADBE Ramp-0002").setValue(top);
    g.property("ADBE Ramp-0003").setValue([0, r.top + r.height]); g.property("ADBE Ramp-0004").setValue(bottom);
}
function blurIn(l, t, amount, dur) {
    var b = fx(l, "ADBE Gaussian Blur 2");
    keys(b.property("ADBE Gaussian Blur 2-0001"), [[t, amount], [t + dur, 0, 70, 33]]);
    b.property("ADBE Gaussian Blur 2-0003").setValue(1);
}
function imageLayer(comp, file) {
    var items = app.project.items, it = null;
    for (var i = 1; i <= items.length; i++) if (items[i] instanceof FootageItem && items[i].name == file) it = items[i];
    if (!it) it = app.project.importFile(new ImportOptions(new File(IN + file)));
    return comp.layers.add(it);
}
// outer comp: inner comp layer + exit (fade, optional lift / scale)
function wrap(name, inner, out, lift, grow) {
    var c = newComp(name, inner.duration);
    var l = c.layers.add(inner);
    if (out < inner.duration) {
        keys(O(l), [[out, 100], [inner.duration, 0, 60, 33]]);
        if (lift) keys(P(l), [[out, [540, 960]], [inner.duration, [540, 960 - lift]]]);
        if (grow) keys(S(l), [[out, [100, 100]], [inner.duration, [grow, grow]]]);
    }
    return {comp: c, layer: l};
}
function backdrop(comp, y0, y1, feather, op, tIn) {
    var b = solid(comp, "backdrop", [0, 0, 0]);
    rectMask(b, -60, y0, W + 60, y1, feather);
    if (tIn === null) O(b).setValue(op); else keys(O(b), [[tIn, 0], [tIn + 0.18, op]]);
    return b;
}
