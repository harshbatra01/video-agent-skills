// meta key: cursor_light_trail_text_reveal
// meta title: Cursor Reveal
// meta order: 6
// meta refs: analysis/DaVUZK3ywAw/ref_cursor_reveal_card_lf03.png, analysis/DaVUZK3ywAw/ref_cursor_reveal_card_lf09.png, analysis/DaVUZK3ywAw/ref_cursor_reveal_card_lf13.png, analysis/DaVUZK3ywAw/ref_cursor_reveal_card_lf30.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx). Source: a friend's Mac effects library (Oct 2026).

// Tutorial stack (reel DaVUZK3ywAw): a white cursor line sweeps right with the Flow curve 0.36,0.01,0,0.97; a light-trail
// rectangle with a blue Gradient Fill is parented to it (right edge on the cursor) and its gradient Start/End points are keyed
// so the trail grows while the cursor is fast and shrinks to nothing; a solid copy of the rectangle is the alpha matte that
// lets the text exist only left of the cursor; Deep Glow 2 on the trail and the cursor. Loops every 35 frames like the reel card.
function build_cursor_light_trail_text_reveal() {
    var TITLE = "Cursor Reveal";
    var LOOP = 35, NLOOP = 3;
    var COPY = "Go with the flow.";
    var MOVE = 30;                                  // cursor travel in frames (measured on the reel's finished card)
    var comp = effectComp(TITLE, LOOP * NLOOP / FPS);

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
    function walkLog(g, tag, pre) {
        for (var i = 1; i <= g.numProperties; i++) {
            var p = g.property(i), v = "";
            if (p.propertyType == PropertyType.PROPERTY) {
                try { var vv = p.value; v = (vv instanceof Array) ? vv.join(",") : String(vv); } catch (e) { v = "(no value)"; }
                log("  dump " + tag + " | " + pre + p.name + " | " + p.matchName + " | " + v);
            } else walkLog(p, tag, pre + p.name + " > ");
        }
    }
    function deepGlow(l) {
        var g = fxp(l, "PEDG2", [["PEDG2-0017", 500], ["PEDG2-0020", 50], ["PEDG2-0021", 50], ["PEDG2-0054", 100], ["PEDG2-0055", 1]], "Deep Glow 2");
        try { g.property("PEDG2-0018").expression = 'thisComp.layer("CONTROLS").effect("Glow Exposure")("Slider")'; } catch (e) { log("  deep glow exposure link: " + e.toString()); }
        return g;
    }
    function rectGroup(l, fillMatch) {
        var gc = shapeGroup(l);
        var rc = gc.addProperty("ADBE Vector Shape - Rect");
        rc.property("ADBE Vector Rect Size").setValue([1365.4, 119.7]);
        rc.property("ADBE Vector Rect Roundness").setValue(9);
        groupOf(l).addProperty(fillMatch);
        return groupOf(l).property(fillMatch);
    }
    // loop every keyed property on the CONTROLS loop length (0 = play once)
    var LOOPX = 'var L = thisComp.layer("CONTROLS").effect("Loop Length (frames)")("Slider"); var d = thisComp.frameDuration;\n' +
                'L < 1 ? value : valueAtTime(time - Math.floor((time + d / 100) / (L * d)) * L * d);';

    // ---------------------------------------------------------------- layers, bottom to top
    var bg = solidL(comp, "Black Solid 2", [0, 0, 0]);

    var t = txt(comp, COPY, FONTS.regular, 155, [1, 1, 1], ParagraphJustification.CENTER_JUSTIFY, -15, 960, 595);
    t.name = COPY;
    try { log("  cursor text font: " + t.property("Source Text").value.font); } catch (ef) {}
    var tr0 = t.sourceRectAtTime(0, false);
    var X0 = Math.round(960 + tr0.left - 25), X1 = Math.round(960 + tr0.left + tr0.width + 31);
    log("  cursor text spans x " + Math.round(960 + tr0.left) + " to " + Math.round(960 + tr0.left + tr0.width) + ", cursor " + X0 + " to " + X1);

    // Light Trail (tutorial: Shape Layer 2): rectangle + Gradient Fill
    var lt = comp.layers.addShape(); lt.name = "Light Trail";
    var gf = rectGroup(lt, "ADBE Vector Graphic - G-Fill");
    gf.name = "Gradient Fill 1";
    walkLog(gf, "gfill", "");
    var gcol = gf.property("ADBE Vector Grad Colors");
    var colorsSet = false;
    try { log("  gradient colours valueType " + gcol.propertyValueType + " (NO_VALUE=" + PropertyValueType.NO_VALUE + ")"); } catch (e0) {}

    // Reveal Matte (tutorial: Shape Layer 3): same rectangle, solid white fill
    var rm = comp.layers.addShape(); rm.name = "Reveal Matte";
    var rf = rectGroup(rm, "ADBE Vector Graphic - Fill");
    rf.property("ADBE Vector Fill Color").setValue([1, 1, 1]);

    // Cursor (tutorial: Shape Layer 1): a 2-point path, white 5 px stroke
    var cur = comp.layers.addShape(); cur.name = "Cursor";
    var cg = shapeGroup(cur);
    var cp = cg.addProperty("ADBE Vector Shape - Group");
    var csh = new Shape(); csh.vertices = [[0, -76.5], [0, 76.5]]; csh.closed = false;
    cp.property("ADBE Vector Shape").setValue(csh);
    var cst = groupOf(cur).addProperty("ADBE Vector Graphic - Stroke");
    cst.property("ADBE Vector Stroke Color").setValue([1, 1, 1]);
    cst.property("ADBE Vector Stroke Width").setValue(5);
    cst = groupOf(cur).property("ADBE Vector Graphic - Stroke");
    cst.property("ADBE Vector Stroke Line Cap").setValue(1);

    var ctl = controls(comp);
    slider(ctl, "Loop Length (frames)", LOOP);
    slider(ctl, "Glow Exposure", 0.25);

    // cursor move: Flow curve 0.36,0.01,0,0.97 = out influence 36 % (speed 0.01/0.36 of the average), in influence 100 % (speed 0.03 of the average)
    var cpos = P(cur);
    cpos.setValueAtTime(0, [X0, 540]);
    cpos.setValueAtTime(MOVE / FPS, [X1, 540]);
    var avg = (X1 - X0) / (MOVE / FPS);
    setEase(cpos, 1, 0, 33.3, avg * 0.01 / 0.36, 36);
    setEase(cpos, 2, avg * 0.03, 100, 0, 33.3);
    try { cpos.setSpatialTangentsAtKey(1, [0, 0], [0, 0]); cpos.setSpatialTangentsAtKey(2, [0, 0], [0, 0]); } catch (es) {}
    cpos.expression = LOOPX;

    // trail and matte ride on the cursor: anchor on the rectangle's right edge, parented to Cursor
    var riders = [lt, rm];
    for (var i = 0; i < riders.length; i++) {
        riders[i].parent = cur;
        A(riders[i]).setValue([682.7, 0]);
        P(riders[i]).setValue([0, -2]);
    }

    // Gradient Fill Start/End Point keys from the tutorial (rectangle space, x -682.7..682.7):
    // 0 f start (735,-11.8) end (894,-13.5); 12 f start (-171.9,-15.2) end (679.9,8.4) Easy Ease; 33 f back to the 0 f values.
    var KS = [[0, [735.0, -11.8]], [12, [-171.9, -15.2]], [33, [735.0, -11.8]]];
    var KE = [[0, [894.0, -13.5]], [12, [679.9, 8.4]], [33, [894.0, -13.5]]];
    gf = lt.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group").property("ADBE Vector Graphic - G-Fill");
    gcol = gf.property("ADBE Vector Grad Colors");
    var swap = !colorsSet;   // default gradient runs white -> black: put the tutorial's End values on Start so white = the cursor end
    var spt = gf.property("ADBE Vector Grad Start Pt"), ept = gf.property("ADBE Vector Grad End Pt");
    var kA = swap ? KE : KS, kB = swap ? KS : KE;
    for (var k = 0; k < 3; k++) { spt.setValueAtTime(kA[k][0] / FPS, kA[k][1]); ept.setValueAtTime(kB[k][0] / FPS, kB[k][1]); }
    var gps = [spt, ept];
    for (var q = 0; q < 2; q++) {
        gps[q].setInterpolationTypeAtKey(1, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
        gps[q].setInterpolationTypeAtKey(3, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
        setEase(gps[q], 2, 0, 33.33, 0, 33.33);
        gps[q].expression = LOOPX;
    }
    if (swap) {
        // Script cannot write gradient colour stops, so the grey gradient is turned into the tutorial's look by effects:
        // its brightness becomes the opacity ramp (Shift Channels) and is mapped to #1E52A1 > #0F71F8 > #09B1F7 (Tritone).
        var sc = fxp(lt, "ADBE Shift Channels", [["Take Alpha From", 5]], "Gradient Opacity 0-100 (Shift Channels)");
        fxp(lt, "ADBE Tritone", [["Highlights", hex("#09B1F7")], ["Midtones", hex("#0F71F8")], ["Shadows", hex("#1E52A1")], ["Blend With Original", 0]], "Gradient Colours (Tritone)");
    }
    deepGlow(lt);
    deepGlow(cur);
    var dgp = cur.property("ADBE Effect Parade").property("Deep Glow 2");
    try { log("  deep glow blend " + dgp.property("PEDG2-0024").value + " glow mode " + dgp.property("PEDG2-0103").value + " view " + dgp.property("PEDG2-0053").value); } catch (e3) {}

    // the text only exists left of the cursor
    t.setTrackMatte(rm, TrackMatteType.ALPHA);
    rm.enabled = false;
    ctl.moveToBeginning();

    note(comp, "Cursor Reveal: the Cursor line moves " + X0 + " to " + X1 + " px in 30 frames with the Flow curve 0.36, 0.01, 0, 0.97 (out influence 36 %, in influence 100 %), and Light Trail and Reveal Matte (a 1365 x 120 rectangle, roundness 9) are parented to it with their right edge on the line. " +
        "Reveal Matte is the text's alpha matte, so letters only exist left of the cursor; Light Trail's Gradient Fill Start/End points are keyed at 0, 12 (Easy Ease) and 33 frames so the blue fade grows while the cursor is fast and shrinks to nothing. " +
        "In the tutorial the gradient stops are #1E52A1, #0F71F8, #09B1F7 with opacity 0 to 100; scripts cannot set gradient stops, so here the default white-to-black gradient is reversed and Shift Channels plus Tritone turn it into the same blue fade (set the stops in Edit Gradient and delete those two effects to work exactly like the tutorial). " +
        "Deep Glow 2 (Radius 500, Threshold 50) sits on the trail and the cursor; CONTROLS sets the glow exposure and the 35-frame loop (0 plays it once).");
    return comp;
}
