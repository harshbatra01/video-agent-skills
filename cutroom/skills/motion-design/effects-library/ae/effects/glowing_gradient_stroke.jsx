// meta key: glowing_gradient_stroke
// meta title: Glowing Stroke
// meta order: 5
// meta refs: analysis/DbGCgZrP-GU/ref_glowing_stroke_card_lf03.png, analysis/DbGCgZrP-GU/ref_glowing_stroke_card_lf09.png, analysis/DbGCgZrP-GU/ref_glowing_stroke_card_lf20.png, analysis/DbGCgZrP-GU/ref_glowing_stroke_card_lf31.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).

// Tutorial stack (reel DbGCgZrP-GU): a 2 px line under a prompt box draws on with Trim Paths; a tapered copy of it carries
// Deep Glow 2 (radius 1000) and is the alpha track matte for a colour layer (Gradient Ramp + Colorama with a white/red/white/
// cyan/blue cycle), so the core and the huge haze take the palette colours; Colorama's Phase Shift is keyed with a violent
// start and a long settle so the colours race along the line and come to rest. Colorama's colour wheel cannot be set by
// script, so the palette is rebuilt from six Gradient Ramps in a precomp and scrolled with Offset driven by the same
// Phase Shift keys (degrees) on CONTROLS. Loops every 33 frames with the reel card's slow push-out (switchable).
function build_glowing_gradient_stroke() {
    var TITLE = "Glowing Stroke";
    var LOOP = 33, NLOOP = 3;
    var COPY = "Go with the flow.";
    var NCH = COPY.length;
    var DUR = LOOP * NLOOP / FPS;
    var comp = effectComp(TITLE, DUR);

    function setEase(prop, idx, inSpd, inInf, outSpd, outInf) {
        var n = 1;
        if (!prop.isSpatial && (prop.propertyValueType == PropertyValueType.TwoD || prop.propertyValueType == PropertyValueType.ThreeD)) n = prop.keyValue(idx).length;
        var ia = [], oa = [];
        for (var i = 0; i < n; i++) { ia.push(new KeyframeEase(inSpd, inInf)); oa.push(new KeyframeEase(outSpd, outInf)); }
        try {
            prop.setInterpolationTypeAtKey(idx, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER);
            prop.setTemporalEaseAtKey(idx, ia, oa);
        } catch (e) { log("  ease " + prop.name + " key " + idx + ": " + e.toString()); }
    }
    // two keys at frames f0 -> f1 with the tutorial-style ease (out speed / influence, in speed / influence)
    function key2(prop, f0, v0, f1, v1, outSpd, outInf, inSpd, inInf) {
        prop.setValueAtTime(f0 / FPS, v0); prop.setValueAtTime(f1 / FPS, v1);
        setEase(prop, 1, 0, 33.3, outSpd, outInf);
        setEase(prop, 2, inSpd, inInf, 0, 33.3);
    }
    function easyEase(prop, f0, v0, f1, v1) { key2(prop, f0, v0, f1, v1, 0, 33.33, 0, 33.33); }
    function walkLog(g, tag, pre) {
        for (var i = 1; i <= g.numProperties; i++) {
            var p = g.property(i), v = "";
            if (p.propertyType == PropertyType.PROPERTY) {
                try { var vv = p.value; v = (vv instanceof Array) ? vv.join(",") : String(vv); } catch (e) { v = "(no value)"; }
                log("  dump " + tag + " | " + pre + p.name + " | " + p.matchName + " | " + v);
            } else walkLog(p, tag, pre + p.name + " > ");
        }
    }
    function lineLayer(name, verts, col, width) {
        var l = comp.layers.addShape(); l.name = name;
        var gc = shapeGroup(l);
        var pg = gc.addProperty("ADBE Vector Shape - Group");
        var sh = new Shape(); sh.vertices = verts; sh.closed = false;
        pg.property("ADBE Vector Shape").setValue(sh);
        var st = groupOf(l).addProperty("ADBE Vector Graphic - Stroke");
        st.property("ADBE Vector Stroke Color").setValue(col);
        st.property("ADBE Vector Stroke Width").setValue(width);
        st = groupOf(l).property("ADBE Vector Graphic - Stroke");
        st.property("ADBE Vector Stroke Line Cap").setValue(2);
        st.property("ADBE Vector Stroke Line Join").setValue(2);
        return l;
    }
    function textAnim(l, name) {
        var an = l.property("ADBE Text Properties").property("ADBE Text Animators").addProperty("ADBE Text Animator");
        an.name = name;
        an.property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity").setValue(0);
        return an;
    }
    function rangeSel(l, animName, selName) {
        var an = l.property("ADBE Text Properties").property("ADBE Text Animators").property(animName);
        var sel = an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
        sel.name = selName;
        sel = l.property("ADBE Text Properties").property("ADBE Text Animators").property(animName).property("ADBE Text Selectors").property(selName);
        var adv = sel.property("ADBE Text Range Advanced");
        try { adv.property("ADBE Text Range Units").setValue(2); } catch (e1) { log("  text units: " + e1.toString()); }       // Index
        try { adv.property("ADBE Text Range Type2").setValue(1); } catch (e2) { log("  text based on: " + e2.toString()); }   // Characters
        return l.property("ADBE Text Properties").property("ADBE Text Animators").property(animName).property("ADBE Text Selectors").property(selName);
    }
    var LOOPX = 'var L = thisComp.layer("CONTROLS").effect("Loop Length (frames)")("Slider"); var d = thisComp.frameDuration;\n' +
                'L < 1 ? value : valueAtTime(time - Math.floor((time + d / 100) / (L * d)) * L * d);';

    // ---------------------------------------------------------------- Colorama palette precomp (one 360 degree cycle = 1950 px, like the ramp from x -6 to 1944)
    var PW = 1950;
    var pal = effectComp(TITLE + " - Colorama palette", DUR, PW, 1080);
    var STOPS = [[0, "#F7F7FA"], [48, "#E1000A"], [120, "#E83004"], [180, "#F2F9F7"], [240, "#19FBF5"], [307, "#0A5FD4"], [360, "#F7F7FA"]];
    for (var s = 0; s < STOPS.length - 1; s++) {
        var xa = STOPS[s][0] / 360 * PW, xb = STOPS[s + 1][0] / 360 * PW;
        var sw = Math.ceil(xb - xa) + 2;
        var seg = solidL(pal, "Ramp " + STOPS[s][0] + "-" + STOPS[s + 1][0] + " deg", [1, 1, 1], sw, 1080);
        P(seg).setValue([xa - 1 + sw / 2, 540]);
        fxp(seg, "ADBE Ramp", [["Start of Ramp", [1, 540]], ["Start Color", hex(STOPS[s][1])], ["End of Ramp", [1 + (xb - xa), 540]],
            ["End Color", hex(STOPS[s + 1][1])], ["Ramp Shape", 1], ["Blend With Original", 0]], "Gradient Ramp");
    }
    note(pal, "Colorama Output Cycle rebuilt as six Gradient Ramps: 0 deg #F7F7FA, 48 #E1000A, 120 #E83004, 180 #F2F9F7, 240 #19FBF5, 307 #0A5FD4, back to white at 360. One full cycle spans 1950 px, the width of the tutorial's black-to-white ramp. Change a colour on the matching ramp.");

    // ---------------------------------------------------------------- main comp, bottom to top (CONTROLS first so every expression finds it; moved to the top at the end)
    var ctl = controls(comp);
    slider(ctl, "Loop Length (frames)", LOOP);
    slider(ctl, "Typed Letters", 0);
    checkbox(ctl, "Reel Zoom On", true);
    fx(ctl, "ADBE Angle Control"); ctl.property("ADBE Effect Parade").property(ctl.property("ADBE Effect Parade").numProperties).name = "Colorama Phase Shift";
    var box = rrect(comp, "Fill", 1084, 185, 60, hex("#0A0A0B"), null, 0, 960, 540);

    var ta = txt(comp, COPY, FONTS.regular, 67, hex("#F2F2F2"), ParagraphJustification.LEFT_JUSTIFY, -18, 485, 562);
    ta.name = COPY;
    try { log("  stroke text font: " + ta.property("Source Text").value.font); } catch (ef) {}
    var tb = txt(comp, COPY, FONTS.regular, 67, hex("#5CCFE0"), ParagraphJustification.LEFT_JUSTIFY, -18, 485, 562);
    tb.name = "Go with... flow. 2";
    var td = tb.property("Source Text").value;
    td.applyFill = false; td.applyStroke = true; td.strokeColor = hex("#5CCFE0"); td.strokeWidth = 2.5;
    tb.property("Source Text").setValue(td);

    var arrow = comp.layers.addShape(); arrow.name = "Arrow";
    var ag = shapeGroup(arrow);
    var ap1 = ag.addProperty("ADBE Vector Shape - Group");
    var as1 = new Shape(); as1.vertices = [[0, 15.5], [0, -15.5]]; as1.closed = false; ap1.property("ADBE Vector Shape").setValue(as1);
    var ap2 = groupOf(arrow).addProperty("ADBE Vector Shape - Group");
    var as2 = new Shape(); as2.vertices = [[-11, -4.5], [0, -15.5], [11, -4.5]]; as2.closed = false; ap2.property("ADBE Vector Shape").setValue(as2);
    var ast = groupOf(arrow).addProperty("ADBE Vector Graphic - Stroke");
    ast.property("ADBE Vector Stroke Color").setValue([1, 1, 1]); ast.property("ADBE Vector Stroke Width").setValue(3.5);
    ast = groupOf(arrow).property("ADBE Vector Graphic - Stroke");
    ast.property("ADBE Vector Stroke Line Cap").setValue(2); ast.property("ADBE Vector Stroke Line Join").setValue(2);
    P(arrow).setValue([1393, 547]);

    // Shape Layer 1: the 2 px line along the box's bottom edge, drawn on by Trim Paths
    var sl1 = lineLayer("Shape Layer 1", [[-489, 93], [489, 93]], hex("#2F5BFF"), 2);
    P(sl1).setValue([960, 540]);
    var trim = groupOf(sl1).addProperty("ADBE Vector Filter - Trim");
    groupOf(sl1).property("ADBE Vector Graphic - Stroke").moveTo(groupOf(sl1).numProperties);
    trim = trimOf(sl1);
    try { trim.property("ADBE Vector Trim Type").setValue(1); } catch (et) {}       // Simultaneously
    var tEnd = trimOf(sl1).property("ADBE Vector Trim End");
    easyEase(tEnd, 0, 0, 8, 100);
    tEnd.expression = LOOPX;

    // Shape Layer 2: tapered duplicate (no Trim Paths), Deep Glow 2, opacity 0 -> 100 in 4 frames. Used as the matte.
    var sl2 = lineLayer("Shape Layer 2", [[-489, 93], [489, 93]], hex("#2F5BFF"), 2);
    A(sl2).setValue([-1.5, 93]); P(sl2).setValue([960, 633]);
    var st2 = groupOf(sl2).property("ADBE Vector Graphic - Stroke");
    var taper = st2.property("ADBE Vector Stroke Taper");
    if (taper) walkLog(taper, "taper", "");
    var TP = [["ADBE Vector Taper Length Units", 1], ["ADBE Vector Taper Start Length", 40], ["ADBE Vector Taper End Length", 40],
              ["ADBE Vector Taper Start Width", 0], ["ADBE Vector Taper End Width", 0], ["ADBE Vector Taper Start Ease", 0], ["ADBE Vector Taper End Ease", 0]];
    for (var tpi = 0; tpi < TP.length; tpi++) {
        var tpp = findProp(groupOf(sl2).property("ADBE Vector Graphic - Stroke"), TP[tpi][0]);
        if (!tpp) { log("  taper param missing " + TP[tpi][0]); continue; }
        try { tpp.setValue(TP[tpi][1]); } catch (etp) { log("  taper param " + TP[tpi][0] + ": " + etp.toString()); }
    }
    var dg = fxp(sl2, "PEDG2", [["PEDG2-0017", 1000], ["PEDG2-0018", 0.8], ["PEDG2-0054", 100], ["PEDG2-0055", 1]], "Deep Glow 2");
    try { log("  deep glow blend " + dg.property("PEDG2-0024").value + " glow mode " + dg.property("PEDG2-0103").value + " view " + dg.property("PEDG2-0053").value + " thr " + findProp(dg, "PEDG2-0020").value); } catch (e3) { log("  dg read " + e3.toString()); }
    var op2 = O(sl2);
    easyEase(op2, 0, 0, 4, 100);
    op2.expression = LOOPX;

    // Black Solid 2 in the tutorial (Gradient Ramp + Colorama): here the palette precomp scrolled by Offset
    var palL = addComp(comp, pal, "Black Solid 2 (Colorama palette)");
    P(palL).setValue([PW / 2 - 6, 540]);
    var off = fxp(palL, "ADBE Offset", [["Blend With Original", 0]], "Offset (Colorama Phase Shift)");
    off.property(1).expression = 'var ph = thisComp.layer("CONTROLS").effect("Colorama Phase Shift")("Angle");\n' +
        '[thisLayer.width / 2 - ph / 360 * thisLayer.width, thisLayer.height / 2]';
    palL.setTrackMatte(sl2, TrackMatteType.ALPHA);
    sl2.enabled = false;

    // ---------------------------------------------------------------- type-on (text A) and the scribbled glyphs ahead of it (text B)
    // CONTROLS > Typed Letters (keyed, measured on the reel: fast first letters, slow finish) drives both text layers.
    var typed = ctl.property("ADBE Effect Parade").property("Typed Letters").property(1);
    key2(typed, 0, 0, 31, NCH, (NCH * 0.35 / 0.02) / (31 / FPS), 2, 0, 70);
    typed.expression = LOOPX;
    var TYPEDX = 'thisComp.layer("CONTROLS").effect("Typed Letters")("Slider")';

    textAnim(ta, "Type");
    var sa = rangeSel(ta, "Type", "Range Selector 1");
    sa.property("ADBE Text Index End").setValue(NCH);
    sa.property("ADBE Text Index Start").expression = TYPEDX;

    textAnim(tb, "Scribble Window");
    var sb1 = rangeSel(tb, "Scribble Window", "Hide Typed");
    sb1.property("ADBE Text Index Start").setValue(0);
    sb1.property("ADBE Text Index End").expression = TYPEDX + ' + 2';
    var sb2 = rangeSel(tb, "Scribble Window", "Hide Ahead");
    sb2 = tb.property("ADBE Text Properties").property("ADBE Text Animators").property("Scribble Window").property("ADBE Text Selectors").property("Hide Ahead");
    sb2.property("ADBE Text Index End").setValue(NCH);
    var fStart = sb2.property("ADBE Text Index Start");
    key2(fStart, 0, 3, 11, NCH, ((NCH - 3) * 0.35 / 0.02) / (11 / FPS), 2, 0, 70);
    fStart.expression = LOOPX;
    var tdisp = fxp(tb, "ADBE Turbulent Displace", [["Amount", 45], ["Size", 9], ["Complexity", 2]], "Turbulent Displace");
    try { tdisp.property("Evolution").expression = "time * 1440"; } catch (ee) { log("  turbulent evolution: " + ee.toString()); }
    gaussBlur(tb, 1.2);

    // ---------------------------------------------------------------- reel card push-out (presentation only) + CONTROLS
    var zoom = comp.layers.addNull(DUR); zoom.name = "Reel Zoom (card push-out)";
    P(zoom).setValue([960, 540]); A(zoom).setValue([50, 50]);
    var kids = [box, ta, tb, arrow, sl1, sl2, palL];
    for (var kq = 0; kq < kids.length; kq++) kids[kq].parent = zoom;
    var zs = S(zoom);
    // measured on the reel card: 123.3 % -> 86.3 % over 34 frames, very fast start (out influence 10 %), soft landing
    key2(zs, 0, [123.3, 123.3], 34, [86.3, 86.3], -37 / (34 / FPS) * 8.5, 10, -37 / (34 / FPS) * 0.5, 10);

    var ph = ctl.property("ADBE Effect Parade").property("Colorama Phase Shift").property(1);
    key2(ph, 0, 0, 30, -621, -10000, 3.6, 0, 40);          // tutorial: 0x+0.0 -> -1x-261.0 at 1:00, spike then long decay
    ph.expression = LOOPX;
    zs.expression = 'var on = thisComp.layer("CONTROLS").effect("Reel Zoom On")("Checkbox");\n' +
        'var L = thisComp.layer("CONTROLS").effect("Loop Length (frames)")("Slider"); var d = thisComp.frameDuration;\n' +
        'on == 0 ? [100, 100] : (L < 1 ? value : valueAtTime(time - Math.floor((time + d / 100) / (L * d)) * L * d));';
    zoom.moveToBeginning();
    ctl.moveToBeginning();

    note(comp, "Glowing Stroke: Shape Layer 1 is a 2 px blue line under the prompt box drawn on by Trim Paths (End 0 to 100 % in 8 frames), and Shape Layer 2 is a copy with Stroke Taper 40 % / 40 %, Deep Glow 2 (radius 1000; the tutorial reads exposure 0.15, raised here to 0.8 so the haze matches the reel) and opacity 0 to 100 % in 4 frames. " +
        "Shape Layer 2 is the alpha track matte of the colour layer, so the thin core and the whole haze take the palette colours (white, red, orange-red, white, cyan, blue). " +
        "In the tutorial that layer is a black solid with Gradient Ramp and Colorama; script cannot set Colorama's colour wheel, so the palette is six Gradient Ramps in a precomp scrolled by Offset from CONTROLS > Colorama Phase Shift (0 to -621 degrees in 30 frames, out speed -10000 deg/s at 3.6 %, in influence 40 %). " +
        "Change the palette inside the Colorama palette precomp, the race of colours with the Phase Shift keys, and turn off the reel card's push-out with Reel Zoom On.");
    return comp;
}
