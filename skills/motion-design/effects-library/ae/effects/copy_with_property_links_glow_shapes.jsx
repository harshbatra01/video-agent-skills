// meta key: copy_with_property_links_glow_shapes
// meta title: Linked Effects (Ctrl+Alt+C)
// meta order: 16
// meta refs: analysis/DcBTMVShtWj/ref_property_links_glow_shapes_0.00.png, analysis/DcBTMVShtWj/ref_property_links_glow_shapes_16.50.png, analysis/DcBTMVShtWj/ref_property_links_glow_shapes_20.00.png, analysis/DcBTMVShtWj/ref_effect_stack_panel_6.33.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx). Source: a friend's Mac effects library (Oct 2026).
// Technique demo: Shape Layer 1 carries the effect stack; layers 2-10 carry the same effects whose every property is an
// expression link to Shape Layer 1 (what Edit > Copy With Property Links + Paste writes). Animating the master drives all ten.
function build_copy_with_property_links_glow_shapes() {
    var TITLE = "Linked Effects (Ctrl+Alt+C)";
    var DUR = 6;
    var c = effectComp(TITLE, DUR);
    var BLUE = hex("#1E82E9");
    var bg = solidL(c, "BG", hex("#010101"));

    function dumpFx(eff, tag) {      // log every param (name | matchName | value) once, for later tuning
        function walk(g, pre) {
            for (var i = 1; i <= g.numProperties; i++) {
                var p = g.property(i), v = "";
                if (p.propertyType == PropertyType.PROPERTY) {
                    try { var vv = p.value; v = (vv instanceof Array) ? vv.join(",") : String(vv); } catch (e) { v = "?"; }
                    log("  dump " + tag + " | " + pre + p.name + " | " + p.matchName + " | " + v);
                } else walk(p, pre + p.name + " > ");
            }
        }
        walk(eff, "");
    }
    function polyGroup(l, pts, sides, radius, rot) {
        var g = shapeGroup(l);
        var st = g.addProperty("ADBE Vector Shape - Star");
        st.property("ADBE Vector Star Type").setValue(2);            // polygon
        st.property("ADBE Vector Star Points").setValue(sides);
        st.property("ADBE Vector Star Outer Radius").setValue(radius);
        st.property("ADBE Vector Star Rotation").setValue(rot || 0);
        return l;
    }
    function fillOf(l, col) { var f = groupOf(l).addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(col); }
    // [type, x, y, size w, size h or sides, rotation]
    var SH = [
        ["rect", 250, 560, 250, 150, 0],
        ["hex", 330, 250, 125, 6, 0],
        ["rect", 900, 205, 180, 180, 45],
        ["rect", 1560, 135, 170, 170, 18],
        ["ell", 1240, 400, 230, 230, 0],
        ["rect", 1645, 425, 150, 150, 0],
        ["ell", 420, 860, 220, 220, 0],
        ["rect", 690, 905, 130, 130, 40],
        ["rect", 1100, 815, 180, 180, 45],
        ["hex", 1560, 830, 125, 6, 0]
    ];
    var L = [];
    for (var i = 0; i < SH.length; i++) {
        var d = SH[i], l = c.layers.addShape();
        l.name = "Shape Layer " + (i + 1);
        if (d[0] == "rect") { var g = shapeGroup(l); var rc = g.addProperty("ADBE Vector Shape - Rect"); rc.property("ADBE Vector Rect Size").setValue([d[3], d[4]]); }
        else if (d[0] == "ell") { var g2 = shapeGroup(l); g2.addProperty("ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size").setValue([d[3], d[4]]); }
        else polyGroup(l, null, d[4], d[3], 0);
        fillOf(l, BLUE);
        P(l).setValue([d[1], d[2]]); R(l).setValue(d[5]);
        L.push(l);
    }

    // master stack on Shape Layer 1 (values read from the reel's Effect Controls)
    var m = L[0];
    var rough = fxp(m, "ADBE Roughen Edges", [["Edge Type", 1], ["Border", 8], ["Edge Sharpness", 1], ["Fractal Influence", 1], ["Scale", 100], ["Complexity", 2]]);
    var dg = fxp(m, "PEDG2", [["Radius", 500], ["Exposure", 0.17], ["Threshold", 55], ["Threshold Smooth", 55]]);
    var ds = fxp(m, "ADBE Drop Shadow", [["ADBE Drop Shadow-0001", [0, 0, 0]], ["ADBE Drop Shadow-0002", 127.5], ["ADBE Drop Shadow-0003", 135], ["ADBE Drop Shadow-0004", 5], ["ADBE Drop Shadow-0005", 19]]);
    var gr = fxp(m, "VISINF Grain Implant", [["Viewing Mode", 3], ["Intensity", 0.7], ["Size", 0.3]]);

    // demo keys on the master: everything else follows through the links
    var mep = m.property("ADBE Effect Parade");
    var expo = findProp(mep.property(2), "Exposure");
    if (expo) kf(expo, [[12, 0.08], [40, 0.30], [66, 0.08]]);
    var bord = findProp(mep.property(1), "Border");
    if (bord) kf(bord, [[76, 8], [102, 26], [126, 8]]);
    var inten = findProp(mep.property(4), "Intensity");
    if (inten) kf(inten, [[134, 0.3], [152, 1.2], [168, 0.7]]);

    // Copy With Property Links: same effects on 2-10, each property linked to the master by expression
    function collect(g, path, out) {
        for (var i2 = 1; i2 <= g.numProperties; i2++) {
            var p = g.property(i2), pp = path.concat([i2]);
            if (p.propertyType == PropertyType.PROPERTY) {
                if (p.propertyValueType != PropertyValueType.NO_VALUE && p.propertyValueType != PropertyValueType.CUSTOM_VALUE && p.canSetExpression) out.push([pp, p.name, p.matchName, g.name]);
            } else collect(p, pp, out);
        }
    }
    function byPath(eff, path) { var p = eff; for (var k = 0; k < path.length; k++) p = p.property(path[k]); return p; }
    var MN = [], NAMES = [];
    for (var e = 1; e <= mep.numProperties; e++) { MN.push(mep.property(e).matchName); NAMES.push(mep.property(e).name); }
    var linked = 0, failed = 0, firstFail = "";
    for (var li = 1; li < L.length; li++) {
        var cl = L[li];
        for (var e2 = 0; e2 < MN.length; e2++) fxp(cl, MN[e2], null);
        for (var e3 = 0; e3 < MN.length; e3++) {
            var props = []; collect(mep.property(e3 + 1), [], props);
            for (var q = 0; q < props.length; q++) {
                var tgt = byPath(cl.property("ADBE Effect Parade").property(e3 + 1), props[q][0]);
                if (!tgt || !tgt.canSetExpression) continue;
                var base = 'comp("' + TITLE + '").layer("Shape Layer 1").effect("' + NAMES[e3] + '")';
                var cands = [base + '("' + props[q][1] + '")', base + '("' + props[q][2] + '")', base + '("' + props[q][3] + '")("' + props[q][1] + '")'];
                var ok = false;
                for (var cc = 0; cc < cands.length && !ok; cc++) {
                    try {
                        tgt.expression = cands[cc]; tgt.expressionEnabled = true;
                        tgt.valueAtTime(0, false);
                        if (tgt.expressionEnabled && (!tgt.expressionError || tgt.expressionError == "")) ok = true;
                    } catch (ex) { ok = false; }
                }
                if (ok) linked++; else { failed++; if (!firstFail) firstFail = NAMES[e3] + " / " + props[q][1] + ": " + tgt.expressionError; try { tgt.expression = ""; } catch (ex2) {} }
            }
        }
    }
    log("  property links: " + linked + " linked, " + failed + " not linkable" + (firstFail ? " (first: " + firstFail + ")" : ""));

    // on-screen read-out of the master values and a selection box on the master
    var hud = rrect(c, "Readout plate", 1060, 58, 29, hex("#0B1220"), hex("#24324A"), 2, 960, 1028);
    var rd = txt(c, "Shape Layer 1", FONTS.medium, 26, hex("#DCE6F5"), ParagraphJustification.CENTER_JUSTIFY, -5, 960, 1037);
    rd.name = "Readout (expression)";
    rd.property("Source Text").expression =
        'var m = thisComp.layer("Shape Layer 1");\n' +
        'var x = m.effect("' + NAMES[1] + '")("' + (expo ? expo.name : "Exposure") + '").value, b = m.effect("' + NAMES[0] + '")("Border").value, g = m.effect("' + NAMES[3] + '")("Intensity").value;\n' +
        '"Shape Layer 1 drives all 10   |   Glow Exposure " + x.toFixed(2) + "   Border " + b.toFixed(1) + "   Grain " + g.toFixed(2);';
    var top = txt(c, "CTRL + ALT + C   on Shape Layer 1,   CTRL + V   on layers 2-10", FONTS.medium, 28, hex("#8FA3BF"), ParagraphJustification.CENTER_JUSTIFY, 20, 960, 56);
    top.name = "Shortcut caption";
    var sel = c.layers.addShape(); sel.name = "Master selection box"; P(sel).setValue([250, 560]);
    var sg = shapeGroup(sel); sg.addProperty("ADBE Vector Shape - Rect").property("ADBE Vector Rect Size").setValue([300, 200]);
    var sst = groupOf(sel).addProperty("ADBE Vector Graphic - Stroke");
    sst.property("ADBE Vector Stroke Color").setValue(hex("#9FC4F5")); sst.property("ADBE Vector Stroke Width").setValue(2);
    try { var dd = groupOf(sel).property("ADBE Vector Graphic - Stroke").property("ADBE Vector Stroke Dashes"); dd.addProperty("ADBE Vector Stroke Dash 1");
          groupOf(sel).property("ADBE Vector Graphic - Stroke").property("ADBE Vector Stroke Dashes").property("ADBE Vector Stroke Dash 1").setValue(10); } catch (ed) {}
    O(sel).setValue(70);
    var mt = txt(c, "master", FONTS.medium, 24, hex("#9FC4F5"), ParagraphJustification.LEFT_JUSTIFY, 0, 102, 448);
    mt.name = "Master label";

    note(c, "Shape Layer 1 is the master: Roughen Edges, Deep Glow 2, Drop Shadow and Add Grain with the reel's values. Layers 2-10 carry the same four effects, and every property on them is an expression link to Shape Layer 1, which is exactly what Edit > Copy With Property Links (Ctrl+Alt+C) and Paste writes. Change any value on Shape Layer 1 (the demo keys Deep Glow Exposure, Roughen Border and Grain Intensity) and all ten shapes update.");
    return c;
}
