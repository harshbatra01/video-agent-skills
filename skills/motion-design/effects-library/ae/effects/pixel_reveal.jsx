// meta key: pixel_reveal
// meta title: Pixel Reveal
// meta order: 1
// meta refs: analysis/DeRssdegQgm/ref_pixel_reveal_0.200.png, analysis/DeRssdegQgm/ref_pixel_reveal_0.333.png, analysis/DeRssdegQgm/ref_pixel_reveal_0.467.png, analysis/DeRssdegQgm/ref_kinetic_word_pan_1.233.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx). Source: a friend's Mac effects library (Oct 2026).
// The hero effect of DeRssdegQgm ("The Pixel Reveal"), built with the tutorial's own stack and shown inside the reel's
// white intro: "This is called" [photo] "The Pixel / Reveal" on one strip that a LAYOUT null pans left with motion blur.
// The photo is the PixelReveal precomp: footage over a luma matte copy carrying Gradient Ramp + Turbulent Noise + Mosaic
// + Exposure + Posterize, where the Exposure keys sweep the blocks on from the bright corner of the ramp (bottom right)
// to the dark corner (top left). Then the photo burns out (Extract) and "and it's pretty easy to make." builds underneath.
function build_pixel_reveal() {
    var TITLE = "Pixel Reveal";
    var DUR = 3.4;
    var PW = 1692, PH = 1128;
    var FONT = FONTS.medium, BLACK = hex("#000000");
    var TN_BLEND = 7, TN_CONTRAST = 100;

    function anims(l) { return l.property("ADBE Text Properties").property("ADBE Text Animators"); }
    // per-word opacity: Text Animator (Opacity 0) + Expression Selector based on Words.
    // curve "expo": 100*2^(-k p) (long tail); curve "quad": ease in-out over D frames.
    function wordFade(l, onsets, D, k, curve) {
        anims(l).addProperty("ADBE Text Animator").name = "Word fade";
        anims(l).property("Word fade").property("ADBE Text Animator Properties").addProperty("ADBE Text Opacity");
        anims(l).property("Word fade").property("ADBE Text Animator Properties").property("ADBE Text Opacity").setValue(0);
        anims(l).property("Word fade").property("ADBE Text Selectors").addProperty("ADBE Text Expressible Selector");
        var s = anims(l).property("Word fade").property("ADBE Text Selectors").property(1);
        var b = findProp(s, "ADBE Text Range Type2") || findProp(s, "Based On");
        try { b.setValue(3); } catch (e) { log("  based on: " + e.toString()); }
        var am = findProp(s, "ADBE Text Expressible Amount") || findProp(s, "Amount");
        var body = (curve == "quad") ?
            "p < 0 ? 100 : (p >= 1 ? 0 : 100 * (1 - (p < 0.5 ? 2 * p * p : 1 - 2 * (1 - p) * (1 - p))));" :
            "p < 0 ? 100 : (p >= 1 ? 0 : 100 * Math.pow(2, -" + k + " * p));";
        am.expression = "// word onsets in comp frames, one per word; D = fade length in frames\n" +
            "var on = [" + onsets.join(", ") + "];\nvar D = " + D + ";\n" +
            "var i = Math.min(textIndex - 1, on.length - 1);\n" +
            "var p = (time / thisComp.frameDuration - on[i]) / D;\n" + body;
    }

    // ---------------------------------------------------------------- photo: SOURCE (a still) + the pixel reveal precomp
    // The reel reveals a still photo, so SOURCE A holds one frozen frame (Time Remap hold) of the skater clip.
    var src = sourceComp(TITLE + " - SOURCE A", "skater.mov", DUR, { w: PW, h: PH, crop: [300, 0, 1920, 1080] });
    var sl = src.layer(1);
    try {
        sl.timeRemapEnabled = true;
        var trm = sl.property("ADBE Time Remapping");
        for (var q = 1; q <= trm.numKeys; q++) trm.setValueAtKey(q, 1.05);
        sl.inPoint = 0; sl.outPoint = DUR;
    } catch (efz) { log("  freeze frame: " + efz.toString()); }
    sl.name = "photo (frozen frame)";

    var pr = effectComp(TITLE + " - PixelReveal precomp", DUR, PW, PH);
    var ctl = controls(pr);
    slider(ctl, "Blocks", 55);
    slider(ctl, "Raggedness (noise contrast)", TN_CONTRAST);
    solidL(pr, "Solid layer", hex("#FFFFFF"));
    var mt = addComp(pr, src, "Footage");
    fxp(mt, "ADBE Ramp", [["Start of Ramp", [0.0009 * PW, -0.0106 * PH]], ["Start Color", [0, 0, 0]],
        ["End of Ramp", [1.133 * PW, 1.124 * PH]], ["End Color", [1, 1, 1]], ["Ramp Shape", 2], ["Ramp Scatter", 0], ["Blend With Original", 0]]);
    var tn = fxp(mt, "ADBE AIF Perlin Noise 3D", [["Blending Mode", TN_BLEND]]);
    var tc = findProp(tn, "Contrast");
    if (tc) tc.expression = "thisComp.layer(\"CONTROLS\").effect(\"Raggedness (noise contrast)\")(\"Slider\")";
    var mo = fxp(mt, "ADBE Mosaic", [["Horizontal Blocks", 55], ["Vertical Blocks", 55], ["Sharp Colors", 0]]);
    findProp(mo, "Horizontal Blocks").expression = "Math.round(thisComp.layer(\"CONTROLS\").effect(\"Blocks\")(\"Slider\"))";
    mo = mt.property("ADBE Effect Parade").property("Mosaic");
    findProp(mo, "Vertical Blocks").expression = "Math.round(thisComp.layer(\"CONTROLS\").effect(\"Blocks\")(\"Slider\"))";
    var exf = fxp(mt, "ADBE Exposure2", null);
    var ev = findProp(mt.property("ADBE Effect Parade").property("Exposure"), "Exposure");
    kf(ev, [[2, -2.53], [49, 14.29]]); linearKeys(ev);
    fxp(mt, "ADBE Posterize", [["Level", 2]]);
    var fill = addComp(pr, src, "Footage");
    fill.setTrackMatte(mt, TrackMatteType.LUMA);
    mt.enabled = false;
    note(pr, "The tutorial pre-comp. Layer 1 Footage uses layer 2 as a Luma track matte. Layer 2 Footage (hidden) carries Gradient Ramp (radial, black top left), Turbulent Noise (all Reset except Blending Mode Overlay), Mosaic 55 x 55, Exposure keyed -2.53 at frame 2 to 14.29 at frame 49 (linear) and Posterize 2, so the matte is hard black and white blocks. Layer 3 is the white solid. CONTROLS: Blocks drives both Mosaic counts, Raggedness drives the noise Contrast.");

    // ---------------------------------------------------------------- main comp
    var c = effectComp(TITLE, DUR);
    c.motionBlur = true; try { c.shutterAngle = 180; c.shutterPhase = -90; c.motionBlurSamplesPerFrame = 16; } catch (e0) {}
    solidL(c, "BG White", hex("#FFFFFF"));

    // phrase 3 (not parented, waits under the photo)
    var t3 = txt(c, "and it’s pretty easy to make.", FONT, 99, BLACK, ParagraphJustification.CENTER_JUSTIFY, -25, 960, 572);
    t3.name = "and it's pretty easy to make.";
    wordFade(t3, [52, 58, 63.4, 68, 72.2, 76.6], 18, 7, "expo");

    // LAYOUT null: anchor at the comp centre so its children use plain comp coordinates at rest
    var lay = c.layers.addNull(DUR); lay.name = "LAYOUT";
    A(lay).setValue([960, 540]);
    var off = [[0, 860], [1, 790], [2, 720], [3, 667], [4, 625], [5, 591], [6, 559], [7, 527], [8, 500], [9, 474], [10, 451], [11, 429], [12, 409],
        [13, 389], [14, 371], [15, 353], [16, 336], [17, 318], [18, 300], [19, 281], [20, 258], [21, 231], [22, 199], [23, 166], [24, 139],
        [25, 117], [26, 99], [27, 84], [28, 71], [29, 60], [30, 50], [32, 35], [34, 23], [36, 15], [38, 9], [40, 5], [42, 2], [44, 1], [46, 0]];
    var lk = [];
    for (var i = 0; i < off.length; i++) lk.push([off[i][0], [960 + off[i][1], 540]]);
    kf(P(lay), lk); linearKeys(P(lay));

    // photo
    var ph = addComp(c, pr, "PixelReveal");
    ph.parent = lay;
    P(ph).setValue([733.5, 540.5]);
    ph.motionBlur = true;
    var sc = [[36, 100], [40, 101.0], [45, 102.1], [47, 103.2], [50, 105.9], [52, 109.6], [54, 114.5], [55, 117.0], [57, 119.6], [59, 122.0], [60, 123.2]];
    var sk = [];
    for (var j = 0; j < sc.length; j++) sk.push([sc[j][0], [sc[j][1] * 0.5, sc[j][1] * 0.5]]);
    kf(S(ph), sk); linearKeys(S(ph));
    var ex = fxp(ph, "ADBE Extract", [["Channel", 1], ["Black Point", 0], ["Black Softness", 0], ["White Softness", 8]]);
    var wp = findProp(ex, "White Point");
    kf(wp, [[46, 255], [47, 207], [48, 203], [49, 198], [50, 190], [51, 179], [52, 103], [53, 96], [54, 86], [55, 50], [56, 28], [57, 24], [58, 8], [59, 0]]);
    linearKeys(wp);
    ph.outPoint = 60 / FPS;

    // phrase 1: right edge 63 px left of the photo
    var t1 = txt(c, "This is called", FONT, 62, BLACK, ParagraphJustification.RIGHT_JUSTIFY, -50, 0, 0);
    t1.name = "This is called";
    t1.parent = lay; P(t1).setValue([248, 562]);
    t1.motionBlur = true;
    wordFade(t1, [0.2, 3.3, 6.9], 16, 9.6, "expo");
    kf(O(t1), [[20, 100], [25, 0]]); linearKeys(O(t1));

    // title: right-aligned at x 1618, two lines
    var t2 = txt(c, "The Pixel\rReveal", FONT, 102, BLACK, ParagraphJustification.RIGHT_JUSTIFY, 10, 0, 0);
    t2.name = "The Pixel / Reveal";
    try { var st = t2.property("Source Text"), d = st.value; d.autoLeading = false; d.leading = 92; st.setValue(d); } catch (el) { log("  leading " + el.toString()); }
    t2.parent = lay;
    t2.motionBlur = true;
    wordFade(t2, [22.1, 28.6, 35.3], 6, 5.8, "expo");
    kf(P(t2), [[46, [1618, 535], 33, 60], [63, [1658, 535], 60, 33]]);
    kf(O(t2), [[46, 100], [63, 0]]); linearKeys(O(t2));

    note(c, "Pixel Reveal, shown the way the reel opens: the photo appears as hard rectangular blocks sweeping from the bottom right to the top left while the whole row pans in. " +
        "Open the PixelReveal precomp for the tutorial stack: the top Footage uses the bottom Footage as a Luma matte, and the bottom copy holds Gradient Ramp, Turbulent Noise (Overlay), Mosaic 55 x 55, Exposure keyed -2.53 to 14.29 (frames 2 to 49, linear) and Posterize 2; retime the Exposure keys to change the speed and swap your shot in SOURCE A. " +
        "In this comp the LAYOUT null pans the row (Position keys on every frame, 180 degree motion blur), each text layer has a Word fade animator whose Amount expression lists the word onsets, and the photo leaves with the Luma Burnout Exit (Extract White Point keys plus a push-in).");

    return c;
}
