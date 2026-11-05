// meta key: overlap_keyframes_20_50_graph_peak
// meta title: 20-50 Easing Rule
// meta order: 15
// meta refs: analysis/DaNZsi6PGWx/ref_keyframe_bars_explainer_18.00.png, analysis/DaNZsi6PGWx/ref_keyframe_bars_explainer_19.00.png, analysis/DaNZsi6PGWx/ref_overlap_20_50_graph_peak_32.00.png, analysis/DaNZsi6PGWx/ref_overlap_20_50_graph_peak_33.47.png, analysis/DaNZsi6PGWx/ref_overlap_20_50_graph_peak_34.67.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// The reel's keyframe diagram, driven by real keyframes. Two nulls hold the tutorial's keys (Layer A 0f-24f, Layer B 12f-36f).
// The teal bars and hourglass icons are expressions that read those key times, so moving a key moves the diagram. The black
// curve is AE's speed graph for Layer B's ease (same maths as the Graph Editor), drawn from two influence sliders on CONTROLS:
// out 1 / in 91 gives the "sloppy" spike at B's first key, 73 / 73 puts the peak on Layer A's last key (the Graph Peak rule).
function build_overlap_keyframes_20_50_graph_peak() {
    var TITLE = "20-50 Easing Rule";
    var DUR = 6;
    function tMap(f) { return f <= 40 ? f : 40 + (f - 40) * 0.69; }   // demo pacing: tutorial keys (0-36f) stay exact, the explainer after 40f is tightened to fit 6 s
    function kfT(prop, list) { var out = []; for (var i = 0; i < list.length; i++) { var it = list[i].slice(0); it[0] = Math.round(tMap(it[0]) * 10) / 10; out.push(it); } kf(prop, out); }
    var mc = effectComp(TITLE, DUR);
    mc.motionBlur = true;
    try { mc.shutterAngle = 180; mc.shutterPhase = -90; } catch (eSh) {}

    // reel frame is 1904x1078: map its pixel measurements onto 1920x1080
    var K = 1920 / 1904;
    function X(x) { return 960 + (x - 952) * K; }
    function Y(y) { return 540 + (y - 539) * K; }
    var PPF = 31.04 * K;                 // diagram pixels per frame (reel: A keys at x386 and x1131 = 24 frames)
    var FX0 = X(386);                    // diagram x of frame 0
    var YT = Y(585), YBOT = Y(665);      // bar centres before the bars separate
    var GBASE = Y(785), GTOP = Y(547);   // speed graph baseline and peak height (after the separation)

    var FONT = FONTS.medium;
    var NAVY = hex("#061728"), BORDER = hex("#B2B8BE"), DOT = hex("#2386E3");
    var TEAL_B = hex("#22DCCA"), TEAL_A = hex("#1CDDD0"), BAND = hex("#F7E393"), KEYGREY = hex("#55575B");
    var INK = hex("#08080A"), GRID = hex("#C0C5CA"), GUIDE = hex("#3B82D9");

    // ---------------------------------------------------------------- small shape helpers
    function shapeLayer(name) { var l = mc.layers.addShape(); l.name = name; A(l).setValue([0, 0]); P(l).setValue([0, 0]); return l; }
    function addPath(l, verts, closed) {
        var g = shapeGroup(l);
        var s = new Shape(); s.vertices = verts; s.closed = !!closed;
        g.addProperty("ADBE Vector Shape - Group").property("ADBE Vector Shape").setValue(s);
        var root = l.property("ADBE Root Vectors Group");
        return root.property(root.numProperties).property("ADBE Vectors Group");
    }
    function lastGroup(l) { var root = l.property("ADBE Root Vectors Group"); return root.property(root.numProperties).property("ADBE Vectors Group"); }
    function addFill(l, col) { var f = lastGroup(l).addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(col); }
    function addStroke(l, col, w, dash) {
        lastGroup(l).addProperty("ADBE Vector Graphic - Stroke");
        function stk() { return lastGroup(l).property("ADBE Vector Graphic - Stroke"); }
        stk().property("ADBE Vector Stroke Color").setValue(col); stk().property("ADBE Vector Stroke Width").setValue(w);
        stk().property("ADBE Vector Stroke Line Cap").setValue(dash ? 1 : 2); stk().property("ADBE Vector Stroke Line Join").setValue(2);
        var st = stk();
        if (dash) {
            try {
                st.property("ADBE Vector Stroke Dashes").addProperty("ADBE Vector Stroke Dash 1");
                st = lastGroup(l).property("ADBE Vector Graphic - Stroke");
                st.property("ADBE Vector Stroke Dashes").addProperty("ADBE Vector Stroke Gap 1");
                st = lastGroup(l).property("ADBE Vector Graphic - Stroke");
                st.property("ADBE Vector Stroke Dashes").property("ADBE Vector Stroke Dash 1").setValue(dash[0]);
                st.property("ADBE Vector Stroke Dashes").property("ADBE Vector Stroke Gap 1").setValue(dash[1]);
            } catch (ed) { log("  dash failed: " + ed.toString()); }
        }
    }
    function addRect(l, w, h, round) {
        var g = shapeGroup(l);
        var rc = g.addProperty("ADBE Vector Shape - Rect");
        rc.property("ADBE Vector Rect Size").setValue([w, h]); rc.property("ADBE Vector Rect Roundness").setValue(round || 0);
        return lastGroup(l).property("ADBE Vector Shape - Rect");
    }
    function setExpr(prop, ex, label) {
        try {
            prop.expression = ex;
            prop.valueAtTime(5, false);
            if (prop.expressionError && prop.expressionError != "") log("  EXPRESSION FAIL " + label + ": " + prop.expressionError);
        } catch (e) { log("  EXPRESSION FAIL " + label + ": " + e.toString()); }
    }
    function nullL(name, parentL) {
        var n = mc.layers.addNull(DUR); n.name = name;
        A(n).setValue([0, 0]); P(n).setValue([0, 0]);
        if (parentL) n.parent = parentL;
        return n;
    }
    function sep(n) { P(n).dimensionsSeparated = true; return [tr(n).property("ADBE Position_0"), tr(n).property("ADBE Position_1")]; }
    function hourglass(name, parentL) {    // AE's Easy Ease keyframe icon, 23 x 28 px
        var l = shapeLayer(name);
        var a = 11.5 * K, b = 14 * K, w = 2.6 * K, c = 10.5 * K;
        addPath(l, [[-a, -b], [a, -b], [a, -c], [w, 0], [a, c], [a, b], [-a, b], [-a, c], [-w, 0], [-a, -c]], true);
        addFill(l, KEYGREY);
        if (parentL) l.parent = parentL;
        l.motionBlur = true;
        return l;
    }
    function fitTracking(l, target) {   // binary-search the tracking so the measured text width hits the reel's width
        var lo = -160, hi = 80, w = 0;
        for (var i = 0; i < 13; i++) {
            var mid = Math.round((lo + hi) / 2), sp = l.property("Source Text"), d = sp.value;
            d.tracking = mid; sp.setValue(d);
            w = l.sourceRectAtTime(0, false).width;
            if (w > target) hi = mid; else lo = mid;
            if (hi - lo <= 1) break;
        }
        log("  text '" + l.name + "' tracking " + Math.round((lo + hi) / 2) + " width " + Math.round(w) + " (reel " + Math.round(target) + ")");
    }

    // ---------------------------------------------------------------- background
    solidL(mc, "Background", hex("#F9F9F9"));

    // ---------------------------------------------------------------- the real keyframes (the diagram reads these)
    var NA = "Layer A keys", NB = "Layer B keys (Graph Peak)", NS = "Layer B keys (sloppy ease)";
    var kA = nullL(NA), kB = nullL(NB), kS = nullL(NS);
    kfT(P(kA), [[0, [120, 1000], 33, 73], [24, [420, 1000], 73, 33]]);
    kfT(P(kB), [[12, [120, 1040], 33, 73], [36, [420, 1040], 73, 33]]);
    kfT(P(kS), [[12, [120, 1060], 33, 1], [36, [420, 1060], 91, 33]]);
    kA.comment = "Layer A: Position keys at 0f and 24f, Easy Ease 73% (Keyframe Velocity: influence 73 in and out).";
    kB.comment = "Layer B done right: keys at 12f and 36f (starts when A is 50% done), influence 73 / 73, so its speed peaks at 24f = A's last key.";
    kS.comment = "Layer B done wrong: same keys, out influence 1 / in influence 91, so its speed spikes at its first key.";

    // ---------------------------------------------------------------- CONTROLS (one value per idea)
    var ctl = controls(mc);
    var sDrag = slider(ctl, "Drag B (frames)", 0).property(1);
    var sOut = slider(ctl, "B ease out influence %", 1).property(1);
    var sIn = slider(ctl, "B ease in influence %", 91).property(1);

    // expression prelude: diagram x of each key, read from the key nulls (+ the drag slider for Layer B)
    var PRE = 'var C = thisComp.layer("CONTROLS");\n' +
        'var drag = C.effect("Drag B (frames)")("Slider");\n' +
        'var fd = thisComp.frameDuration, ppf = ' + PPF + ', x0 = ' + FX0 + ';\n' +
        'var KA = thisComp.layer("' + NA + '").transform.position, KB = thisComp.layer("' + NB + '").transform.position;\n' +
        'var A1 = x0 + ppf * KA.key(1).time / fd, A2 = x0 + ppf * KA.key(KA.numKeys).time / fd;\n' +
        'var B1 = x0 + ppf * (KB.key(1).time / fd + drag), B2 = x0 + ppf * (KB.key(KB.numKeys).time / fd + drag);\n';
    // AE temporal ease maths: speed-0 keys, influences a (out) and b (in), sampled along the Bezier
    var CURVE = PRE +
        'var a = clamp(C.effect("B ease out influence %")("Slider"), 0.1, 100) / 100;\n' +
        'var b = clamp(C.effect("B ease in influence %")("Slider"), 0.1, 100) / 100;\n' +
        'var base = ' + GBASE + ', hgt = ' + (GBASE - GTOP) + ', N = 160, xs = [], ss = [], mx = 0, im = 0;\n' +
        'for (var i = 0; i <= N; i++) {\n' +
        '  var u = i / N, v = 1 - u;\n' +
        '  xs.push(3 * v * v * u * a + 3 * v * u * u * (1 - b) + u * u * u);\n' +
        '  var s = 6 * u * v / Math.max(3 * (a * v * v + 2 * u * v * (1 - a - b) + b * u * u), 0.000001);\n' +
        '  ss.push(s); if (s > mx) { mx = s; im = i; }\n' +
        '}\n';

    // ---------------------------------------------------------------- rig nulls (layout moves)
    var nDia = nullL("DIAGRAM (layout drift)");
    var nTop = nullL("Top row: Layer B", nDia);
    var nBot = nullL("Bottom row: Layer A", nDia);
    var nPills = nullL("Pills", nDia);

    // ---------------------------------------------------------------- warm glow behind the overlap band
    var bandMidRest = (X(758.5) + X(1135)) / 2;
    var glowL = softEllipse(mc, "Warm glow (overlap)", 760 * K, 520 * K, hex("#F2E3BC"), bandMidRest, YT + 38 * K, 250, 0);
    glowL.parent = nTop;
    setExpr(P(glowL), 'value + [thisComp.layer("CONTROLS").effect("Drag B (frames)")("Slider") * ' + (PPF / 2) + ', 0]', "glow follow");

    // ---------------------------------------------------------------- speed graph grid (appears after the bars separate)
    var grid = shapeLayer("Speed graph grid");
    var gy = [576, 636, 695.5, 755.5];
    for (var gi = 0; gi < gy.length; gi++) { addPath(grid, [[X(762), Y(gy[gi])], [X(1501), Y(gy[gi])]], false); addStroke(grid, GRID, 2); }

    // ---------------------------------------------------------------- bottom row: Layer A bar + keys
    var barA = shapeLayer("Layer A bar");
    addRect(barA, 745 * K + 43 * K, 32 * K, 6); addFill(barA, TEAL_A);
    barA.parent = nBot; barA.motionBlur = true;
    setExpr(P(barA), PRE + '[(A1 + A2) / 2, ' + YBOT + ']', "bar A position");
    setExpr(lastGroup(barA).property("ADBE Vector Shape - Rect").property("ADBE Vector Rect Size"), PRE + '[A2 - A1 + ' + (43 * K) + ', ' + (32 * K) + ']', "bar A size");
    var hA1 = hourglass("Layer A key 1", nBot), hA2 = hourglass("Layer A key 2", nBot);
    setExpr(P(hA1), PRE + '[A1, ' + (YBOT + 40 * K) + ']', "A key 1");
    setExpr(P(hA2), PRE + '[A2, ' + (YBOT + 40 * K) + ']', "A key 2");

    // ---------------------------------------------------------------- top row: overlap band, Layer B bar + keys
    var band = shapeLayer("Overlap band (B key 1 to A key 2)");
    addRect(band, 377 * K, 32 * K, 0); addFill(band, BAND);
    band.parent = nTop; band.motionBlur = true;
    setExpr(P(band), PRE + 'var r = A2 + ' + (4 * K) + ';\n[(B1 + r) / 2, ' + (YT + 38 * K) + ']', "band position");
    setExpr(lastGroup(band).property("ADBE Vector Shape - Rect").property("ADBE Vector Rect Size"), PRE + 'var r = A2 + ' + (4 * K) + ';\n[Math.max(r - B1, 0), ' + (32 * K) + ']', "band size");

    var barB = shapeLayer("Layer B bar");
    addRect(barB, 745 * K + 43 * K, 32 * K, 6); addFill(barB, TEAL_B);
    barB.parent = nTop; barB.motionBlur = true;
    setExpr(P(barB), PRE + '[(B1 + B2) / 2, ' + YT + ']', "bar B position");
    setExpr(lastGroup(barB).property("ADBE Vector Shape - Rect").property("ADBE Vector Rect Size"), PRE + '[B2 - B1 + ' + (43 * K) + ', ' + (32 * K) + ']', "bar B size");
    var hB1 = hourglass("Layer B key 1", nTop), hB2 = hourglass("Layer B key 2", nTop);
    setExpr(P(hB1), PRE + '[B1, ' + (YT + 40 * K) + ']', "B key 1");
    setExpr(P(hB2), PRE + '[B2, ' + (YT + 40 * K) + ']', "B key 2");

    // ---------------------------------------------------------------- Layer B speed graph (live: AE ease maths from the sliders)
    var curve = shapeLayer("Layer B speed graph");
    addPath(curve, [[X(759), GBASE], [X(1505), GBASE]], false); addStroke(curve, INK, 3.6 * K);
    curve.motionBlur = true;
    setExpr(lastGroup(curve).property("ADBE Vector Shape - Group").property("ADBE Vector Shape"),
        CURVE + 'var pts = [[B1, base]];\nfor (var j = 0; j <= N; j++) pts.push([B1 + (B2 - B1) * xs[j], base - ss[j] / mx * hgt]);\npts.push([B2, base]);\ncreatePath(pts, [], [], false);', "speed graph path");
    var curveBlur = gaussBlur(curve, 0);

    // dashed guide on Layer A's last keyframe
    var guide = shapeLayer("Guide: Layer A last key");
    addPath(guide, [[0, Y(395)], [0, Y(875)]], false); addStroke(guide, GUIDE, 2 * K, [8 * K, 6 * K]);
    lastGroup(guide).addProperty("ADBE Vector Filter - Trim");
    var guideTrim = lastGroup(guide).property("ADBE Vector Filter - Trim");
    setExpr(P(guide), PRE + '[A2, 0]', "guide x");

    // dashed circle riding the speed peak
    var mark = shapeLayer("Peak marker");
    var eg = shapeGroup(mark); eg.addProperty("ADBE Vector Shape - Ellipse").property("ADBE Vector Ellipse Size").setValue([50 * K, 50 * K]);
    addStroke(mark, GUIDE, 2 * K, [7 * K, 5 * K]);
    mark.motionBlur = true;
    setExpr(P(mark), CURVE + '[B1 + (B2 - B1) * xs[im], base - hgt];', "peak marker");

    // ---------------------------------------------------------------- caption
    var cap = txt(mc, "Less or more than that will make it sloppy.", FONT, 54, hex("#101923"), ParagraphJustification.CENTER_JUSTIFY, -30, X(952), Y(836));
    cap.name = "Caption";
    fitTracking(cap, 771 * K);
    cap.parent = nDia;
    try {
        var anims = cap.property("ADBE Text Properties").property("ADBE Text Animators");
        anims.addProperty("ADBE Text Animator");
        var an = cap.property("ADBE Text Properties").property("ADBE Text Animators").property(1);
        an.name = "Word reveal";
        an.property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity");
        an = cap.property("ADBE Text Properties").property("ADBE Text Animators").property(1);
        an.property("ADBE Text Animator Properties").addProperty("ADBE Text Blur");
        an = cap.property("ADBE Text Properties").property("ADBE Text Animators").property(1);
        an.property("ADBE Text Animator Properties").property("ADBE Text Opacity").setValue(0);
        an.property("ADBE Text Animator Properties").property("ADBE Text Blur").setValue([9, 9]);
        an.property("ADBE Text Selectors").addProperty("ADBE Text Selector");
        an = cap.property("ADBE Text Properties").property("ADBE Text Animators").property(1);
        var sel = an.property("ADBE Text Selectors").property(1);
        sel.property("ADBE Text Range Advanced").property("ADBE Text Range Type2").setValue(3);   // based on words
        sel.property("ADBE Text Range Advanced").property("ADBE Text Range Shape").setValue(2);   // ramp up
        sel.property("ADBE Text Percent End").setValue(28);
        kfT(sel.property("ADBE Text Percent Offset"), [[76, -28], [108, 100]]);
        linearKeys(sel.property("ADBE Text Percent Offset"));
    } catch (eT) { log("  text animator failed: " + eT.toString()); }
    kfT(O(cap), [[118, 100], [127, 0]]);

    // ---------------------------------------------------------------- pills (precomps: border, fill, dot, label, mosaic label)
    function makePill(label, outerW, dotOff, textOff, textW, sharpAt) {
        var pc = effectComp(TITLE + " - pill " + label.replace("/", "-"), DUR, 700, 240);
        var cx = 350, cy = 120, outerH = 152 * K, left = cx - outerW / 2;
        rrect(pc, "Pill", outerW - 7, outerH - 7, 46, NAVY, BORDER, 7, cx, cy);
        ellipseL(pc, "Dot", 16 * K, 16 * K, DOT, left + dotOff, cy);
        var t = txt(pc, label, FONT, 70, [1, 1, 1], ParagraphJustification.LEFT_JUSTIFY, -30, 0, 0);
        t.name = "Label";
        fitTracking(t, textW);
        var r0 = t.sourceRectAtTime(0, false);
        P(t).setValue([left + textOff - r0.left, cy + 0.352 * 70]);
        var tm = t.duplicate(); tm.name = "Label (pixelated while inactive)";
        var mo = fxp(tm, "ADBE Mosaic", [["Horizontal Blocks", 64], ["Vertical Blocks", 22]]);
        boxBlur(tm, 2, 0);
        kfT(O(pc.layer("Label (pixelated while inactive)")), [[sharpAt, 100], [sharpAt + 4, 0]]);
        kfT(O(pc.layer("Label")), [[sharpAt, 0], [sharpAt + 4, 100]]);
        note(pc, "Pill. The label is pixelated (Mosaic) until the pill becomes active.");
        return pc;
    }
    var pcRule = makePill("20/50 Rule", 476 * K, 72 * K, 116 * K, 287 * K, 40);
    var pcPeak = makePill("Graph Peak", 526 * K, 86 * K, 132 * K, 308 * K, 156);
    function placePill(pc, name, x, rot, popF) {
        var L = addComp(mc, pc, name);
        L.parent = nPills; L.motionBlur = true;
        var y = Y(390);
        kfT(P(L), [[popF, [x, y - 50 * K], 33, 10], [popF + 9, [x, y], 90, 33]]);
        kfT(R(L), [[popF, rot, 33, 10], [popF + 8, 0, 88, 33]]);
        kfT(O(L), [[popF, 0], [popF + 3, 100]]);
        var gb = gaussBlur(L, 0);
        kfT(L.property("ADBE Effect Parade").property(gb.name).property("ADBE Gaussian Blur 2-0001"), [[popF, 16], [popF + 7, 0, 85, 33]]);
        return L;
    }
    var pRule = placePill(pcRule, "Pill: 20/50 Rule", X(611), -7, 22);
    var pPeak = placePill(pcPeak, "Pill: Graph Peak", X(1285), 6, 26);
    // inactive = 71% (the reel's 327 -> 461 px grow), active = 100%
    kfT(S(pRule), [[0, [71, 71]], [40, [71, 71], 33, 20], [64, [100, 100], 90, 33], [118, [100, 100], 33, 55], [152, [71, 71], 95, 33]]);
    kfT(S(pPeak), [[0, [71, 71]], [118, [71, 71], 33, 55], [152, [100, 100], 95, 33]]);

    // ---------------------------------------------------------------- cursor (rides Layer B's bar)
    var cur = shapeLayer("Cursor");
    var cs = 1.27 * K;
    addPath(cur, [[0, 0], [0, 33 * cs], [8 * cs, 25.5 * cs], [13 * cs, 37 * cs], [18 * cs, 35 * cs], [13 * cs, 23.5 * cs], [23.5 * cs, 23.5 * cs]], true);
    addStroke(cur, [1, 1, 1], 2.6 * K); addFill(cur, [0.02, 0.02, 0.03]);
    cur.parent = nTop; cur.motionBlur = true;
    shadow(cur, 0.35, 2, 4, 180);
    setExpr(P(cur), PRE + '[B1 + ' + (340.5 * K) + ', ' + (YT + 3 * K) + ']', "cursor");

    // ---------------------------------------------------------------- the timeline (reel moves, compressed into 6 s)
    function ctlS(nm) { return ctl.property("ADBE Effect Parade").property(nm).property(1); }   // re-fetch: adding sliders invalidates earlier refs
    var dia = sep(nDia), top = sep(nTop), bot = sep(nBot), pls = sep(nPills);
    kfT(dia[1], [[14, -110 * K, 33, 43], [74, 0, 100, 33]]);                                 // layout drifts down
    kfT(top[0], [[0, 560 * K, 33, 13], [34, 0, 94, 33]]);                                     // Layer B bar slides in from the right
    kfT(top[1], [[0, -20 * K, 33, 13], [34, 0, 94, 33], [128, 0, 33, 66], [184, -120 * K, 100, 33]]);
    kfT(bot[0], [[0, -260 * K, 33, 13], [34, 0, 94, 33]]);                                    // Layer A bar slides in from the left
    kfT(bot[1], [[128, 0, 33, 64], [184, 172 * K, 100, 33]]);                                 // bars separate for the graph
    kfT(pls[1], [[128, 0, 33, 66], [184, -120 * K, 100, 33]]);
    kfT(ctlS("Drag B (frames)"), [[68, 0, 33, 76], [84, 7, 79, 33], [88, 7, 33, 31], [112, 0, 97, 33]]);         // cursor drags B to 20% overlap and back to 50%
    kfT(O(band), [[71, 0], [74, 100]]);
    kfT(O(glowL), [[71, 0], [78, 30]]);
    kfT(O(grid), [[148, 0], [160, 100]]);
    kfT(O(curve), [[150, 0], [162, 100]]);
    kfT(curve.property("ADBE Effect Parade").property(1).property("ADBE Gaussian Blur 2-0001"), [[150, 14], [166, 0, 80, 33]]);
    // the ease itself: graph slides in (peak 17% -> 0%), then out 1 / in 91 morphs to 73 / 73
    kfT(ctlS("B ease out influence %"), [[150, 21.9, 33, 3], [192, 1, 94, 33], [196, 1, 33, 55], [232, 73, 98, 33]]);
    kfT(ctlS("B ease in influence %"), [[150, 85.8, 33, 3], [192, 91, 94, 33], [196, 91, 33, 55], [232, 73, 98, 33]]);
    kfT(O(mark), [[186, 0], [190, 100]]);
    kfT(S(mark), [[186, [55, 55], 33, 10], [193, [100, 100], 85, 33]]);
    kfT(O(guide), [[197, 0], [198, 100]]);
    kfT(lastGroup(guide).property("ADBE Vector Filter - Trim").property("ADBE Vector Trim End"), [[197, 0], [206, 100, 80, 33]]);

    // stacking: graph + guides above the bars, pills and cursor on top
    curve.moveToBeginning(); guide.moveToBeginning(); mark.moveToBeginning(); cap.moveToBeginning();
    pRule.moveToBeginning(); pPeak.moveToBeginning(); cur.moveToBeginning();
    var nulls = [ctl, nPills, nBot, nTop, nDia, kS, kB, kA];
    for (var ni = 0; ni < nulls.length; ni++) nulls[ni].moveToBeginning();

    // ---------------------------------------------------------------- check the drawn curve against the real keys
    function analytic(a, b, N) {
        var xs = [], ss = [], mx = 0;
        for (var i = 0; i <= N; i++) {
            var u = i / N, v = 1 - u;
            xs.push(3 * v * v * u * a + 3 * v * u * u * (1 - b) + u * u * u);
            var s = 6 * u * v / Math.max(3 * (a * v * v + 2 * u * v * (1 - a - b) + b * u * u), 0.000001);
            ss.push(s); if (s > mx) mx = s;
        }
        for (var j = 0; j <= N; j++) ss[j] = ss[j] / mx;
        return [xs, ss];
    }
    function checkKeys(nl, a, b) {
        var pr = P(nl), t1 = pr.keyTime(1), t2 = pr.keyTime(2), M = 60, real = [], rmx = 0, h = 0.0005;
        for (var i = 1; i < M; i++) {
            var t = t1 + (t2 - t1) * i / M, v1 = pr.valueAtTime(t + h, false), v0 = pr.valueAtTime(t - h, false);
            var sp = Math.abs(v1[0] - v0[0]) / (2 * h); real.push(sp); if (sp > rmx) rmx = sp;
        }
        var an = analytic(a, b, 2000), worst = 0;
        for (var k = 1; k < M; k++) {
            var xf = k / M, q = 0;
            while (q < an[0].length - 1 && an[0][q + 1] < xf) q++;
            var d = Math.abs(an[1][q] - real[k - 1] / rmx); if (d > worst) worst = d;
        }
        log("  curve check " + nl.name + ": max difference between drawn graph and real keys " + Math.round(worst * 1000) / 10 + "%");
    }
    try { checkKeys(kS, 0.01, 0.91); checkKeys(kB, 0.73, 0.73); } catch (eC) { log("  curve check failed: " + eC.toString()); }
    try { log("  pill scale ease check: out influence at key 2 = " + S(pRule).keyOutTemporalEase(2)[0].influence + ", in at key 3 = " + S(pRule).keyInTemporalEase(3)[0].influence); } catch (eE) { log("  ease check failed: " + eE.toString()); }

    note(mc, "The reel's 20/50 Rule and Graph Peak diagram, built on real keyframes: the nulls Layer A keys (0f to 24f) and Layer B keys (12f to 36f) hold the tutorial's Position keys, and the teal bars, hourglass icons and yellow overlap band are expressions that read those key times (CONTROLS > Drag B shows 20% and 50% overlap). The black curve is AE's speed graph for Layer B's ease, drawn from CONTROLS > B ease out / in influence: 1 and 91 give the sloppy spike on B's first key, 73 and 73 put the peak on Layer A's last key (dashed line). To use the rule on your own layers, start the second layer when the first is 50 to 80% done and set its Keyframe Velocity influence so its Graph Editor speed peak sits on the first layer's last keyframe.");
    return mc;
}
