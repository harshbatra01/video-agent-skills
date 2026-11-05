// meta key: one_frame_glitch_burst
// meta title: One-Frame Glitch Transition
// meta order: 13
// meta refs: analysis/DdoSNUYvtPg/ref_one_frame_glitch_burst_0.90.png, analysis/DdoSNUYvtPg/ref_one_frame_glitch_burst_1.00.png, analysis/DdoSNUYvtPg/ref_one_frame_glitch_burst_1.03.png, analysis/DdoSNUYvtPg/ref_one_frame_glitch_burst_1.10.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// A 6-frame burst around a hard cut from a dark scene to a bright one, built from trimmed 1- and 2-frame layers:
// M-3 luminance-inverted grey smear of A, M-2/M-1 white flash, M the incoming scene zoom-blurred with a dark lens edge,
// M+1/M+2 a hard vertical split (left side = the incoming scene frozen, RGB-inverted, smeared), then clean B from M+3.
// Measured from the reel (top pane, 30 fps): split edge at 48.6 % then 47.9 % of the width, bowing 30 px right near the
// bottom; the rings inside SOURCE B land at 255 % and settle 179 % (M+3) to 100 % (M+30) with an exponential ease-out.
function build_one_frame_glitch_burst() {
    var DUR = 3.5;
    var M = 30;   // the cut: first frame of scene B

    function t(n) { return n / FPS; }
    function holdAll(prop) { for (var i = 1; i <= prop.numKeys; i++) prop.setInterpolationTypeAtKey(i, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD); }
    // explicit bezier speeds (value units per second) on one key, in and out set separately
    function easeAt(prop, idx, sIn, infIn, sOut, infOut) {
        var n = 1;
        if (!prop.isSpatial && (prop.propertyValueType == PropertyValueType.TwoD || prop.propertyValueType == PropertyValueType.ThreeD)) n = prop.keyValue(idx).length;
        var ei = [], eo = [];
        for (var i = 0; i < n; i++) { ei.push(new KeyframeEase(sIn, infIn)); eo.push(new KeyframeEase(sOut, infOut)); }
        try { prop.setTemporalContinuousAtKey(idx, false); } catch (e0) {}
        try { prop.setTemporalEaseAtKey(idx, ei, eo); } catch (e1) { log("  glitch param ease " + prop.name + ": " + e1.toString()); }
    }
    function eff(l, nm) { return l.property("ADBE Effect Parade").property(nm); }
    function ctlExpr(nm) { return 'thisComp.layer("CONTROLS").effect("' + nm + '")("Slider")'; }
    function circleShape(cx, cy, r) {
        var k = 0.5523, s = new Shape();
        s.vertices = [[cx, cy - r], [cx + r, cy], [cx, cy + r], [cx - r, cy]];
        s.inTangents = [[-k * r, 0], [0, -k * r], [k * r, 0], [0, k * r]];
        s.outTangents = [[k * r, 0], [0, k * r], [-k * r, 0], [0, -k * r]];
        s.closed = true; return s;
    }
    function pathLayer(comp, name, verts, fill, x, y) {
        var l = comp.layers.addShape(); l.name = name;
        var g = shapeGroup(l);
        var sh = new Shape(); sh.vertices = verts; sh.closed = true;
        g.addProperty("ADBE Vector Shape - Group").property("ADBE Vector Shape").setValue(sh);
        groupOf(l).addProperty("ADBE Vector Graphic - Fill").property("ADBE Vector Fill Color").setValue(fill);
        P(l).setValue([x, y]); return l;
    }

    // =====================================================================================================
    // SOURCE A: the outgoing dark UI scene ("Import the [file] same assets" + a row of project files)
    var srcA = effectComp("One-Frame Glitch Transition - SOURCE A", DUR);
    solidL(srcA, "BG near-black", hex("#05040C"));
    softEllipse(srcA, "floor haze (blue)", 2000, 760, hex("#1C1B46"), 960, 1110, 420, 60);
    softEllipse(srcA, "top haze", 1500, 520, hex("#0D0D22"), 960, 120, 320, 45);
    var st1 = strokeLine(srcA, "light line 1", [-120, 120], [1350, 1180], [1, 1, 1], 2, 0, 0); O(st1).setValue(7);
    var st2 = strokeLine(srcA, "light line 2", [1250, -60], [2050, 900], [1, 1, 1], 2, 0, 0); O(st2).setValue(6);
    var st3 = strokeLine(srcA, "light line 3 (horizon)", [-60, 497], [1980, 492], [1, 1, 1], 2, 0, 0); O(st3).setValue(5);
    var push = srcA.layers.addNull(DUR); push.name = "PUSH (slow zoom)";
    P(push).setValue([960, 560]);
    var aL = [];
    var tA1 = txt(srcA, "Import the", FONTS.medium, 56, hex("#E2DCE0"), ParagraphJustification.RIGHT_JUSTIFY, -20, 822, 415); tA1.name = "Import the"; aL.push(tA1);
    var tA2 = txt(srcA, "same assets", FONTS.medium, 56, hex("#E2DCE0"), ParagraphJustification.LEFT_JUSTIFY, -20, 1100, 415); tA2.name = "same assets"; aL.push(tA2);
    glow(tA1, 40, 18, 0.35); glow(tA2, 40, 18, 0.35);
    var pg = pathLayer(srcA, "file page", [[-48, -61], [22, -61], [48, -35], [48, 61], [-48, 61]], hex("#F2F1F4"), 964, 383); aL.push(pg);
    var pf = pathLayer(srcA, "file fold", [[22, -61], [48, -35], [22, -35]], hex("#C9C8CF"), 964, 383); aL.push(pf);
    var pmov = txt(srcA, ".mov", FONTS.regular, 22, hex("#A3A2A8"), ParagraphJustification.CENTER_JUSTIFY, 0, 964, 392); aL.push(pmov);
    var plab = txt(srcA, "Lost asset.mov", FONTS.regular, 17, hex("#8E898D"), ParagraphJustification.CENTER_JUSTIFY, 0, 964, 478); aL.push(plab);
    var icon6 = null;
    for (var i = 0; i < 6; i++) {
        var ix = 963 + (i - 2.5) * 168, iy = 718;
        var ib = rrect(srcA, "file " + (i + 1) + " card", 124, 146, 10, hex("#08035E"), hex("#231C8E"), 2, ix, iy);
        var ifo = pathLayer(srcA, "file " + (i + 1) + " fold", [[34, -73], [62, -73], [62, -45]], hex("#9385E8"), ix, iy);
        var ibig = txt(srcA, "P" + (i + 1), FONTS.bold, 58, hex("#8175D8"), ParagraphJustification.CENTER_JUSTIFY, -10, ix, iy + 8);
        var ism = txt(srcA, "AEP", FONTS.bold, 22, hex("#B0B4DE"), ParagraphJustification.CENTER_JUSTIFY, 20, ix, iy + 46);
        var ilab = txt(srcA, "Project " + (i + 1), FONTS.medium, 15, hex("#C9C7D2"), ParagraphJustification.CENTER_JUSTIFY, 0, ix, iy + 98);
        if (i == 5) {   // the last file pops in with a small tilt, as in the reel
            icon6 = srcA.layers.addNull(DUR); icon6.name = "file 6 tilt"; P(icon6).setValue([ix, iy]);
            ib.parent = icon6; ifo.parent = icon6; ibig.parent = icon6; ism.parent = icon6; ilab.parent = icon6;
            kf(R(icon6), [[0, 9], [14, 0, 33, 70]]);
            aL.push(icon6);
        } else { aL.push(ib); aL.push(ifo); aL.push(ibig); aL.push(ism); aL.push(ilab); }
    }
    for (i = 0; i < aL.length; i++) aL[i].parent = push;
    kf(S(push), [[0, [97, 97]], [M, [100, 100], 33, 60]]);
    // a small light streak crossing the last file
    var spark = rrect(srcA, "light streak", 54, 6, 3, [1, 1, 1], null, 0, 1450, 560);
    R(spark).setValue(-58); spark.motionBlur = true; srcA.motionBlur = true;
    kf(P(spark), [[2, [1470, 540]], [24, [1330, 770]]]);
    kf(O(spark), [[2, 0], [5, 100], [20, 100], [24, 0]]);

    // =====================================================================================================
    // SOURCE B: the incoming bright title (static white + blue floor; rings and words land big and settle)
    // local time 0 = the cut frame M.
    var srcB = effectComp("One-Frame Glitch Transition - SOURCE B", DUR);
    var bb = solidL(srcB, "BG white + blue floor", hex("#F9F9F9"));
    fxp(bb, "ADBE Ramp", [["Start of Ramp", [960, 560]], ["Start Color", hex("#F9F9F9")], ["End of Ramp", [960, 1165]], ["End Color", hex("#1F48D8")]], "Gradient Ramp (floor)");
    var ringsZ = srcB.layers.addNull(DUR); ringsZ.name = "RINGS ZOOM";
    P(ringsZ).setValue([863, 540]);
    var rings = [[416, 71], [538, 94], [702, 119]];
    for (var r = 0; r < rings.length; r++) {
        var R0 = rings[r][0], T = rings[r][1];
        var rl = srcB.layers.addShape(); rl.name = "ring " + (r + 1);
        // tube shading: outer dark edge, base, highlight, light inner edge, soft inner glow, invisible pad (keeps the blur unclipped)
        var bands = [[2 * R0 + T * 0.5, T * 0.5, "#1238B5", 100], [2 * R0, T * 0.62, "#124FC0", 100], [2 * R0 - T * 0.5, T * 0.34, "#1F7ED3", 100],
                     [2 * R0 - T * 0.82, T * 0.18, "#4AA0E2", 100], [2 * R0 - T - 34, 70, "#DBE9FB", 70], [2 * R0 + T + 120, 4, "#FFFFFF", 0]];
        for (var q = 0; q < bands.length; q++) {
            rl.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
            var gi = rl.property("ADBE Root Vectors Group").numProperties;
            var vg = rl.property("ADBE Root Vectors Group").property(gi).property("ADBE Vectors Group");
            vg.addProperty("ADBE Vector Shape - Ellipse");
            rl.property("ADBE Root Vectors Group").property(gi).property("ADBE Vectors Group").property(1).property("ADBE Vector Ellipse Size").setValue([bands[q][0], bands[q][0]]);
            rl.property("ADBE Root Vectors Group").property(gi).property("ADBE Vectors Group").addProperty("ADBE Vector Graphic - Stroke");
            var sk = rl.property("ADBE Root Vectors Group").property(gi).property("ADBE Vectors Group").property(2);
            sk.property("ADBE Vector Stroke Color").setValue(hex(bands[q][2]));
            sk.property("ADBE Vector Stroke Width").setValue(bands[q][1]);
            sk.property("ADBE Vector Stroke Opacity").setValue(bands[q][3]);
        }
        P(rl).setValue([960, 540]);
        gaussBlur(rl, 12);
        rl.parent = ringsZ;
    }
    // RINGS ZOOM scale (measured): 255 / 170 / 168 % held on the burst frames, 179 % at M+3, then one eased key to 100 % at M+30
    var rz = S(ringsZ);
    var rk = [[0, 255], [1, 170], [2, 168], [3, 179], [30, 100]];
    for (q = 0; q < rk.length; q++) rz.setValueAtTime(t(rk[q][0]), [rk[q][1], rk[q][1]]);
    for (q = 1; q <= 3; q++) rz.setInterpolationTypeAtKey(q, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD);
    rz.setInterpolationTypeAtKey(4, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.BEZIER);
    rz.setInterpolationTypeAtKey(5, KeyframeInterpolationType.BEZIER, KeyframeInterpolationType.BEZIER);
    easeAt(rz, 4, 0, 10, -825, 10);
    easeAt(rz, 5, 0, 10, 0, 33);

    // words: "That loses the Flow", word by word over a grey underline; they zoom 75 % as much as the rings (parallax) and rise 62 px
    var textZ = srcB.layers.addNull(DUR); textZ.name = "TEXT ZOOM (75% of rings)";
    P(textZ).setValue([802, 540]);
    var words = [["That", 0, "#3A56C0", 74, FONTS.regular], ["loses", 4, "#3A56C0", 74, FONTS.regular], ["the", 10, "#3A56C0", 74, FONTS.regular], ["Flow", 17, "#18191E", 92, FONTS.medium]];
    var wl = [], ww = [], tot = 0, gap = 22;
    for (q = 0; q < words.length; q++) {
        var w = txt(srcB, words[q][0], words[q][4], words[q][3], hex(words[q][2]), ParagraphJustification.LEFT_JUSTIFY, -20, 0, 0);
        w.name = words[q][0];
        var rr = rect(w); wl.push(w); ww.push([rr.left, rr.width]); tot += rr.width + (q ? gap : 0);
    }
    var x0 = 961 - tot / 2, xx = x0, ends = [];
    for (q = 0; q < wl.length; q++) {
        P(wl[q]).setValue([xx - ww[q][0], 569]); xx += ww[q][1]; ends.push(xx); xx += gap;
        var o = O(wl[q]);
        if (q > 0) kf(o, [[words[q][1], 0], [words[q][1] + 2, 100]]);
        if (q == 3) {
            fxp(wl[q], "ADBE Tint", [["Map Black To", hex("#A4A6AE")], ["Map White To", hex("#FFFFFF")]], "Tint (grey to ink)");
            kf(eff(wl[q], "Tint (grey to ink)").property("Amount to Tint"), [[17, 100], [18, 100], [21, 0]]);
        }
    }
    var ul = srcB.layers.addShape(); ul.name = "underline";
    shapeGroup(ul);
    groupOf(ul).addProperty("ADBE Vector Shape - Rect");
    groupOf(ul).addProperty("ADBE Vector Graphic - Fill");
    groupOf(ul).property(2).property("ADBE Vector Fill Color").setValue(hex("#8A90A0"));
    P(ul).setValue([0, 0]);
    var usz = groupOf(ul).property(1).property("ADBE Vector Rect Size");
    var upo = groupOf(ul).property(1).property("ADBE Vector Rect Position");
    var lens = [[0, ww[0][1] + 120], [4, ends[1] - x0 + 70], [10, ends[2] - x0 + 50], [17, ends[3] - x0]];
    for (q = 0; q < lens.length; q++) { usz.setValueAtTime(t(lens[q][0]), [lens[q][1], 3]); upo.setValueAtTime(t(lens[q][0]), [x0 + 10 + lens[q][1] / 2, 588]); }
    holdAll(usz); holdAll(upo);
    kf(O(ul), [[17, 100], [20, 0]]);
    // parent while TEXT ZOOM is still at 100 %, THEN animate it (parenting compensates for the parent's current transform)
    for (q = 0; q < wl.length; q++) wl[q].parent = textZ;
    ul.parent = textZ;
    S(textZ).expression = 'var s = thisComp.layer("RINGS ZOOM").transform.scale[0]; var k = 100 + (s - 100) * 0.75; [k, k];';
    kf(P(textZ), [[0, [802, 602]], [3, [802, 556]], [8, [802, 540], 33, 70]]);

    // =====================================================================================================
    // MAIN: the burst, layer by layer, like the agent built it (top to bottom: FLASH, SPLIT matte, B_INV, B_ZOOM, B, A_INV, A)
    var c = effectComp("One-Frame Glitch Transition", DUR);
    var ctl = controls(c);   // made first so the expressions below find it
    slider(ctl, "Smear Length", 30);
    slider(ctl, "Zoom Blur", 70);
    slider(ctl, "Invert Smear", 40);
    solidL(c, "BG black", [0, 0, 0]).moveToEnd();
    var la = addComp(c, srcA, "A (outgoing)");
    la.outPoint = t(M - 3);

    // burst frame 1 (M-3): A, luminance-inverted, desaturated, smeared sideways, nudged
    var lai = addComp(c, srcA, "A_INV (M-3)");
    lai.inPoint = t(M - 3); lai.outPoint = t(M - 2);
    fxp(lai, "ADBE Invert", [["Channel", 1]], "Invert");   // RGB invert + Saturation -100 below = a luminance invert in grey
    fxp(lai, "ADBE HUE SATURATION", [["Master Saturation", -100]], "Hue/Saturation");
    fxp(lai, "ADBE Motion Blur", [["Direction", 90], ["Blur Length", 30]], "Directional Blur (smear)");
    eff(lai, "Directional Blur (smear)").property("Blur Length").expression = ctlExpr("Smear Length");
    var atf = fxp(lai, "ADBE Geometry2", [["ADBE Geometry2-0002", [972, 540]], ["ADBE Geometry2-0003", 103]], "Transform (nudge)");

    // clean B from M+1 (B_ZOOM covers M, the split covers the left part of M+1 and M+2)
    var lb = addComp(c, srcB, "B (incoming)");
    lb.startTime = t(M); lb.inPoint = t(M + 1); lb.outPoint = DUR;

    // burst frame 4 (M = the cut): B with a radial zoom blur and a dark lens edge on the left corners
    var lz = addComp(c, srcB, "B_ZOOM (M)");
    lz.startTime = t(M); lz.inPoint = t(M); lz.outPoint = t(M + 1);
    var lm = lz.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"); lm.name = "lens edge";
    lm.property("ADBE Mask Shape").setValue(circleShape(1110, 540, 1035));
    lm.property("ADBE Mask Feather").setValue([26, 26]);
    fxp(lz, "CC Radial Fast Blur", [["Center", [1110, 540]], ["Amount", 70]], "CC Radial Fast Blur");
    eff(lz, "CC Radial Fast Blur").property("Amount").expression = ctlExpr("Zoom Blur");

    // burst frames 5-6 (M+1, M+2): the cut frame frozen, RGB-inverted and smeared, seen through the SPLIT matte
    var lbi = addComp(c, srcB, "B_INV (M+1 to M+2)");
    lbi.startTime = t(M);
    try {
        lbi.timeRemapEnabled = true;
        var tm = lbi.property("ADBE Time Remapping");
        tm.setValueAtTime(t(M + 1), 0);
        for (q = tm.numKeys; q >= 1; q--) if (Math.abs(tm.keyTime(q) - t(M + 1)) > 0.0005) tm.removeKey(q);
        holdAll(tm);
    } catch (etr) { log("  glitch param time remap: " + etr.toString()); }
    lbi.inPoint = t(M + 1); lbi.outPoint = t(M + 3);
    fxp(lbi, "ADBE Invert", [["Channel", 1]], "Invert (RGB)");
    fxp(lbi, "ADBE Motion Blur", [["Direction", 90], ["Blur Length", 40]], "Directional Blur (smear)");
    eff(lbi, "Directional Blur (smear)").property("Blur Length").expression = ctlExpr("Invert Smear");

    var sm = solidL(c, "SPLIT matte", [1, 1, 1]);
    sm.inPoint = t(M + 1); sm.outPoint = t(M + 3);
    var mk = sm.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"); mk.name = "split edge";
    function split(x) {   // straight in the top half, bowing 30 px right toward the bottom
        var s = new Shape();
        s.vertices = [[-80, -80], [x, -80], [x, 580], [x + 32, 1160], [-80, 1160]];
        s.inTangents = [[0, 0], [0, 0], [0, 0], [-10, -230], [0, 0]];
        s.outTangents = [[0, 0], [0, 0], [0, 250], [0, 0], [0, 0]];
        s.closed = true; return s;
    }
    var mp = mk.property("ADBE Mask Shape");
    mp.setValueAtTime(t(M + 1), split(938)); mp.setValueAtTime(t(M + 2), split(925)); holdAll(mp);
    mk.property("ADBE Mask Feather").setValue([1.5, 1.5]);

    // burst frames 2-3 (M-2, M-1): white flash
    var fl = solidL(c, "FLASH white", hex("#FBFBFB"));
    fl.inPoint = t(M - 2); fl.outPoint = t(M);

    // stack order, top to bottom
    lai.moveBefore(la);
    lb.moveBefore(lai);
    lz.moveBefore(lb);
    lbi.moveBefore(lz);
    sm.moveBefore(lbi);
    fl.moveBefore(sm);
    ctl.moveToBeginning();
    matte(lbi, sm, TrackMatteType.ALPHA);

    try { c.markerProperty.setValueAtTime(t(M), new MarkerValue("M: the cut (first frame of B)")); } catch (em) {}
    note(c, "A six-frame burst built from trimmed layers around the cut M. A_INV (M-3) is the outgoing shot with Invert and Hue/Saturation -100 (together a grey luminance invert), a 30 px Directional Blur and a small nudge right, then FLASH white holds M-2 and M-1. B_ZOOM (M) is the incoming shot with CC Radial Fast Blur 70 and a feathered lens edge mask that lets the black show in the left corners, and on M+1 and M+2 B_INV (the cut frame frozen by Time Remap, RGB-inverted, smeared 40 px) shows through the SPLIT matte, whose hold-keyed mask edge sits at 938 then 925 px and bows right near the bottom. Retime by sliding the layers, change the smear and blur on CONTROLS, and swap the two SOURCE comps for your own shots (the rings settle 255 to 100 % lives inside SOURCE B).");
    return c;
}
