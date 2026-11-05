// meta key: wave_blur_text_reveal
// meta title: Wave Blur Text
// meta order: 3
// meta refs: analysis/Daacg6ktthE/ref_wave_blur_text_reveal_0.93.png, analysis/Daacg6ktthE/ref_wave_blur_text_reveal_1.27.png, analysis/Daacg6ktthE/ref_wave_blur_text_reveal_1.87.png, analysis/Daacg6ktthE/ref_wave_blur_text_reveal_3.20.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// Daacg6ktthE: a word on white with soft blue clouds starts big and bokeh-blurred; a sharp area spreads over it from
// the top left along a wavy diagonal front. Camera Lens Blur on an adjustment layer reads its blur amount from a hidden
// 'Map' precomp, where a white shape with Wave Warp + Fast Box Blur slides down (white = blurred, black = sharp).
// Comp frame N = reel frame 26 + N (the card in the reel shows comp frames 0-70). All timings below were fitted to
// the reel frame by frame: the Map keys are the tutorial's (speed graph 3150 px/s at 0 f decaying to 0 at 1:04),
// the text Scale and the two text animators were measured from the finished loop.
function build_wave_blur_text_reveal() {
    var DUR = 3.0;
    var TITLE = "Wave Blur Text";
    var BGC = hex("#FDFDFD");

    function fr(n) { return n / FPS; }
    // temporal ease with explicit speeds (units per second, signed for non-spatial values) and influences (%)
    function easeAt(prop, idx, inS, inI, outS, outI) {
        var n = 1;
        if (!prop.isSpatial && (prop.propertyValueType == PropertyValueType.TwoD || prop.propertyValueType == PropertyValueType.ThreeD)) n = prop.keyValue(idx).length;
        var a = [], b = [];
        for (var i = 0; i < n; i++) { a.push(new KeyframeEase(inS, inI)); b.push(new KeyframeEase(outS, outI)); }
        try { prop.setTemporalEaseAtKey(idx, a, b); } catch (e) { log("  ease " + prop.name + ": " + e.toString()); }
    }
    // kfe(prop, [[frame, value, inSpeed, inInf, outSpeed, outInf], ...])
    function kfe(prop, list) {
        for (var i = 0; i < list.length; i++) prop.setValueAtTime(fr(list[i][0]), list[i][1]);
        for (var j = 0; j < list.length; j++) {
            var k = list[j];
            easeAt(prop, prop.nearestKeyIndex(fr(k[0])), k[2], k[3], k[4], k[5]);
        }
    }
    function blob(comp, name, w, h, col, x, y, op) {
        var l = ellipseL(comp, name, w, h, col, x, y);
        if (op !== undefined) O(l).setValue(op);
        return l;
    }
    function drift(l, dx, dy) {
        var p0 = P(l).value;
        P(l).setValueAtTime(0, p0); P(l).setValueAtTime(DUR, [p0[0] + dx, p0[1] + dy]);
    }
    function animGroup(l) { return l.property("ADBE Text Properties").property("ADBE Text Animators"); }
    // a text animator with the given property match names; returns its name (re-fetch by name after every add)
    function addAnimator(l, name, propNames) {
        animGroup(l).addProperty("ADBE Text Animator");
        animGroup(l).property(animGroup(l).numProperties).name = name;
        for (var i = 0; i < propNames.length; i++) animGroup(l).property(name).property("ADBE Text Animator Properties").addProperty(propNames[i]);
        animGroup(l).property(name).property("ADBE Text Selectors").addProperty("ADBE Text Selector");
        return name;
    }
    function animProps(l, name) { return animGroup(l).property(name).property("ADBE Text Animator Properties"); }
    function selector(l, name) { var s = animGroup(l).property(name).property("ADBE Text Selectors"); return s.property(1); }
    function setSel(l, name, pairs) {
        for (var i = 0; i < pairs.length; i++) {
            var q = findProp(selector(l, name), pairs[i][0]);
            if (!q) { log("  selector no " + pairs[i][0]); continue; }
            try { q.setValue(pairs[i][1]); } catch (e) { log("  selector " + pairs[i][0] + ": " + e.toString()); }
        }
    }

    // ---- 'Shapes': soft blue clouds (layout matched to the reel's background), blurred on the precomp layer
    var sh = effectComp(TITLE + " - Shapes", DUR);
    var bT = blob(sh, "Tint lower right", 2600, 900, hex("#A9D0F8"), 1250, 1150, 50);
    var bA = blob(sh, "Blob top-left", 1050, 950, hex("#78B6F5"), -160, 60, 95);
    var bL = blob(sh, "Blob left", 500, 700, hex("#A6CEF8"), -120, 520, 60);
    var bB = blob(sh, "Blob bottom", 1700, 520, hex("#5EAAF4"), 1420, 1190);
    var bD = blob(sh, "Blob top-right", 1000, 380, hex("#A9D0F8"), 1760, -60, 55);
    var bE = blob(sh, "Blob right", 700, 900, hex("#A9D0F8"), 2060, 560, 60);
    drift(bA, 30, 15); drift(bB, 60, -10); drift(bD, -40, 10); drift(bE, -20, 20); drift(bT, 20, -15); drift(bL, 10, 0);

    // ---- 'Map': the blur map. White = full blur radius, black = sharp. (Tutorial: 'Shape Layer 1 Comp 2', renamed Map.)
    var mp = effectComp(TITLE + " - Map", DUR);
    var mbg = solidL(mp, "Black (sharp)", [0, 0, 0]);
    var ml = mp.layers.addShape(); ml.name = "Shape Layer 1";
    A(ml).setValue([0, 0]); P(ml).setValue([960, 540]);
    var gc = ml.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group").property("ADBE Vectors Group");
    var s = new Shape();
    // slanted top edge: through comp (0,793) and (1920,383) when the layer sits at 960,540
    s.vertices = [[-1260, 317], [1260, -221], [1260, 1160], [-1260, 1160]]; s.closed = true;
    gc.addProperty("ADBE Vector Shape - Group").property("ADBE Vector Shape").setValue(s);
    var fl = ml.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group").addProperty("ADBE Vector Graphic - Fill");
    fl.property("ADBE Vector Fill Color").setValue([1, 1, 1]);
    fxp(ml, "ADBE Wave Warp", [["ADBE Wave Warp-0001", 1], ["ADBE Wave Warp-0002", 26], ["ADBE Wave Warp-0003", 421], ["ADBE Wave Warp-0004", 90],
        ["ADBE Wave Warp-0005", 1.0], ["ADBE Wave Warp-0006", 2], ["ADBE Wave Warp-0007", 0], ["ADBE Wave Warp-0008", 1]]);
    fxp(ml, "ADBE Box Blur2", [["Blur Radius", 22], ["Iterations", 3], ["Blur Dimensions", 1], ["Repeat Edge Pixels", 1]]);
    // tutorial keys: 0:00 moved up (whole word blurred), 1:04 home, 2:05 moved down (whole word sharp).
    // Ease read off the tutorial's speed graph: 3150 px/s spike at 0 f with a long tail to 0 at 1:04, then a slow build.
    kfe(P(ml), [[0, [960, 320], 0, 4, 3150, 4], [34, [960, 540], 0, 50, 0, 85], [65, [960, 770], 0, 16.7, 0, 16.7]]);

    // ---- main comp
    var c = effectComp(TITLE, DUR);
    c.bgColor = BGC;
    var ctl = controls(c);
    slider(ctl, "Blur Radius", 10);
    var bg = solidL(c, "BG", BGC);
    var shl = addComp(c, sh, "Shapes");
    shl.moveAfter(ctl);
    fxp(shl, "ADBE Gaussian Blur 2", [["ADBE Gaussian Blur 2-0001", 420], ["ADBE Gaussian Blur 2-0003", 1]]);
    bg.moveToEnd();

    var t = txt(c, "TITLE", FONTS.medium, 360, hex("#050B14"), ParagraphJustification.CENTER_JUSTIFY, -20, 958, 535);
    t.name = "TITLE";
    centreAnchor(t);
    P(t).setValue([958, 535]);
    t.moveBefore(shl);
    // the 'camera movement' (Scale, fitted to the reel): fast settle from 176 % to 100 % at 1:04, then an accelerating
    // pull-back to 81 % at 2:10 (where the reel cuts away), then a short ease to rest
    kfe(S(t), [[0, [176, 176], 0, 5, -300, 5], [34, [100, 100], 0, 100, 0, 30], [70, [81, 81], -70, 10, -70, 30], [82, [73, 73], 0, 60, 0, 60]]);

    // the 'text animations', fitted to the reel letter by letter:
    // 1) Blue sweep: the right-hand letters start blue and turn to ink from left to right (Ramp Up range slides right)
    var a1 = addAnimator(t, "Animator 1 - Blue sweep", ["ADBE Text Fill Color"]);
    animProps(t, a1).property("ADBE Text Fill Color").setValue(hex("#3C6EF0"));
    selector(t, a1).name = "Range Selector 1";
    setSel(t, a1, [["ADBE Text Range Type2", 1], ["ADBE Text Range Shape", 2], ["ADBE Text Percent Start", 0], ["ADBE Text Percent End", 69]]);
    kfe(findProp(selector(t, a1), "ADBE Text Percent Offset"), [[4, 35, 0, 30, 0, 30], [28, 100, 0, 30, 0, 30]]);
    // 2) Rise + fade: the last letters sit lower and paler, and rise into place (Range Selector Amount decays)
    var a2 = addAnimator(t, "Animator 2 - Rise and fade", ["ADBE Text Position 3D", "ADBE Text Opacity"]);
    animProps(t, a2).property("ADBE Text Position 3D").setValue([0, 87, 0]);
    animProps(t, a2).property("ADBE Text Opacity").setValue(40);
    selector(t, a2).name = "Range Selector 1";
    setSel(t, a2, [["ADBE Text Range Type2", 1], ["ADBE Text Range Shape", 2], ["ADBE Text Percent Start", 40], ["ADBE Text Percent End", 100],
        ["ADBE Text Levels Min Ease", 100]]);
    kfe(findProp(selector(t, a2), "ADBE Text Selector Max Amount"), [[1, 100, 0, 10, 0, 10], [30, 0, 0, 100, 0, 100]]);
    t.motionBlur = true;
    c.motionBlur = true; c.shutterAngle = 180; c.shutterPhase = -90;
    try { c.motionBlurSamplesPerFrame = 16; } catch (e7) {}

    var mapL = addComp(c, mp, "Map");
    mapL.moveBefore(t);
    mapL.enabled = false;

    var adj = adjL(c, "Adjustment layer");
    adj.moveBefore(mapL);
    ctl.moveToBeginning();
    var clbName = fxp(adj, "ADBE Camera Lens Blur", [["ADBE Camera Lens Blur-0001", 10], ["ADBE Camera Lens Blur-0003", 4], ["ADBE Camera Lens Blur-0004", 0],
        ["ADBE Camera Lens Blur-0005", 1], ["ADBE Camera Lens Blur-0006", 0], ["ADBE Camera Lens Blur-0007", 100],
        ["ADBE Camera Lens Blur-0011", 1], ["ADBE Camera Lens Blur-0012", 1], ["ADBE Camera Lens Blur-0013", 0], ["ADBE Camera Lens Blur-0014", 0],
        ["ADBE Camera Lens Blur-0017", 0], ["ADBE Camera Lens Blur-0019", 0], ["ADBE Camera Lens Blur-0021", 1], ["ADBE Camera Lens Blur-0022", 1]]).name;
    // Blur Map Layer = the Map layer (set last, after every reorder)
    try { adj.property("ADBE Effect Parade").property(clbName).property("ADBE Camera Lens Blur-0010").setValue(mapL.index); } catch (e2) { log("  clb layer " + e2.toString()); }
    try {
        adj.property("ADBE Effect Parade").property(clbName).property("ADBE Camera Lens Blur-0001").expression =
            "thisComp.layer(\"CONTROLS\").effect(\"Blur Radius\")(1)";
    } catch (e6) { log("  clb expr " + e6.toString()); }

    note(c, "Wave blur text reveal. The Adjustment layer's Camera Lens Blur (Hexagon iris, Blur Map Layer = Map, Luminance) reads its blur from the hidden Map precomp, where Shape Layer 1 is a white shape with a slanted top edge, Wave Warp (height 26, width 421) and Fast Box Blur 22: white is blurred, black is sharp, and its Position keys (moved up at 0:00, home at 1:04, moved down at 2:05) sweep the wavy sharp front across the word. The TITLE Scale keys (176 to 100 to 81 %) are the camera move, and two text animators (a blue colour sweep and a rise and fade on the last letters) settle each letter into the dark ink from left to right. Change the strength with CONTROLS > Blur Radius (the tutorial shows 9, the reel reads about 10), the word in the text layer, and the clouds in the Shapes precomp.");
    return c;
}
