// meta key: hail_mary_highlight_streak
// meta title: Hail Mary
// meta order: 8
// meta refs: analysis/Dd1Zj4KAUax/ref_hail_mary_card_1.5.png, analysis/Dd1Zj4KAUax/ref_hail_mary_15.4.png, analysis/Dd1Zj4KAUax/ref_hail_mary_len1920_14.8.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx). Source: a friend's Mac effects library (Oct 2026).
// Native rebuild of the "Hail Mary (custom)" shader from the reel. A shader like this is a loop: key the bright pixels
// (Threshold + Knee), then add up copies of them shifted along one axis, each copy a little weaker (Falloff), times
// Streak Intensity, plus Glow, mixed over the untouched shot (Mix). Here every pass of that loop is one layer:
// 49 TAP layers (24 each side + centre) in "streak (shader taps)", all driven by the CONTROLS sliders.
function build_hail_mary_highlight_streak() {
    var DUR = 6;
    var MAIN = "Hail Mary";
    var NT = 24;                       // taps per side
    var ON = 8;                        // frame the streak switches on (Mix 0 -> 1 over 6 frames)
    var CX = "comp(\"" + MAIN + "\").layer(\"CONTROLS\")";
    function ctl(n) { return CX + ".effect(\"" + n + "\")(\"Slider\")"; }
    function boxShape(x0, y0, x1, y1) { var sh = new Shape(); sh.vertices = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]; sh.closed = true; return sh; }
    function boxMask(l, x0, y0, x1, y1, feather) {
        var m = l.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        m.property("ADBE Mask Shape").setValue(boxShape(x0, y0, x1, y1));
        if (feather) m.property("ADBE Mask Feather").setValue([feather, feather]);
        return m;
    }

    // ---- SOURCE A: the shot (night street: small hot street lights and signals on dark tones). Swap it for your own shot.
    var src = sourceComp("Hail Mary - SOURCE A", "rain_street.mov", DUR, { start: 0 });

    // ---- 1. Threshold + Knee: keep only the bright pixels, in their own colour (Extract on luminance)
    var hi = effectComp("Hail Mary - highlights (Threshold + Knee)", DUR);
    var hl = addComp(hi, src, "SOURCE A");
    fxp(hl, "ADBE Extract", [["Black Point", 204], ["White Point", 255], ["Black Softness", 24], ["White Softness", 0]], "Threshold + Knee (Extract)");
    var ex = hl.property("ADBE Effect Parade").property("Threshold + Knee (Extract)");
    ex.property("Black Point").expression = "Math.round(" + ctl("Threshold") + " * 255)";
    ex = hl.property("ADBE Effect Parade").property("Threshold + Knee (Extract)");
    ex.property("Black Softness").expression = "Math.round(" + ctl("Knee") + " * 24)";
    gaussBlur(hl, 1.5);
    // keep the hot point lights only: the wet road below the horizon is one big bright area that would bloom into a blob
    boxMask(hl, -10, -10, 1930, 600, 60);

    // ---- 2. The streak: 2 x 24 + 1 shifted copies of the highlights, Add mode, weight exp(-Falloff * i / 24)
    // Tap spacing = Streak Length / 48, so a long streak breaks into the evenly spaced comb copies seen at 1920.
    var st = effectComp("Hail Mary - streak (shader taps)", DUR);
    solidL(st, "BLACK", [0, 0, 0]);
    for (var k = -NT; k <= NT; k++) {
        var tl = addComp(st, hi, "TAP " + (k > 0 ? "+" + k : "" + k));
        tl.blendingMode = BlendingMode.ADD;
        P(tl).expression = "var a = degreesToRadians(" + ctl("Angle") + ");\nvar s = " + ctl("Streak Length") + " / " + (2 * NT) +
            ";   // tap spacing in px\nvar i = " + k + ";\nvalue + [i * s * Math.cos(a), -i * s * Math.sin(a)];";
        O(tl).expression = "var f = " + ctl("Falloff") + ", n = " + NT + ", i = " + Math.abs(k) +
            ";\nvar sum = 1; for (var q = 1; q <= n; q++) sum += 2 * Math.exp(-f * q / n);   // the shader divides by the summed weights\n" +
            "Math.min(100, 100 * " + ctl("Streak Intensity") + " * Math.exp(-f * i / n) / sum);";
    }

    // ---- 3. Pixel-stretch rows (hero frame detail): one 2 px column of the shot stretched leftwards, seen through thin bands
    var X0 = 1010;
    var ps = effectComp("Hail Mary - pixel stretch", DUR);
    var pl = addComp(ps, src, "SOURCE A (2 px column at x " + X0 + ")");
    boxMask(pl, X0 - 2, 0, X0, 1080, 0);
    A(pl).setValue([X0, 540]); P(pl).setValue([X0, 540]); S(pl).setValue([100 * X0 / 2, 100]);

    // ---- main comp
    var c = effectComp(MAIN, DUR);
    addComp(c, src, "SOURCE A (grade untouched)");

    var streak = addComp(c, st, "HAIL MARY STREAK (Add)");
    streak.blendingMode = BlendingMode.ADD;
    O(streak).expression = ctl("Mix") + " * 100";
    var db = fxp(streak, "ADBE Motion Blur", [["Direction", 90], ["Blur Length", 5]], "Tap smoothing (Directional Blur)");
    db.property("Direction").expression = "90 - " + ctl("Angle") + ";   // AE measures clockwise from vertical";
    db = streak.property("ADBE Effect Parade").property("Tap smoothing (Directional Blur)");
    db.property("Blur Length").expression = "Math.min(6, " + ctl("Streak Length") + " / " + (2 * NT) + " * 0.45);";
    var gl = fxp(streak, "ADBE Glo2", [["Glow Threshold", 60], ["Glow Radius", 45], ["Glow Intensity", 0.5]], "Glow (Glow Amount)");
    gl.property("Glow Intensity").expression = ctl("Glow Amount") + " * 0.5";

    var bands = addComp(c, ps, "PIXEL STRETCH rows");
    O(bands).expression = ctl("Mix") + " * 55";
    var bm = solidL(c, "BANDS (matte)", [1, 1, 1]);
    boxMask(bm, 640, 636, X0, 664, 3);
    boxMask(bm, 700, 742, X0, 756, 3);
    boxMask(bm, 760, 690, X0, 696, 2);
    bm.moveBefore(bands);
    matte(bands, bm, TrackMatteType.ALPHA);

    var slice = addComp(c, src, "SLICE (offset copy, Screen)");
    slice.blendingMode = BlendingMode.SCREEN;
    P(slice).setValue([960 + 30, 540]);
    O(slice).expression = ctl("Mix") + " * 20";
    var sm = boxMask(slice, 0.43 * 1920 - 30, -10, 1960, 1090, 0);
    var msh = sm.property("ADBE Mask Shape");
    msh.setValueAtTime((ON + 2) / FPS, boxShape(0.43 * 1920 - 30, -10, 1960, 1090));
    msh.setValueAtTime((ON + 10) / FPS, boxShape(0.85 * 1920 - 30, -10, 1960, 1090));

    // ---- CONTROLS: the shader's eight sliders, keyed like the reel's preview (tilt, drag the length out to 1920, knee down)
    var cl = controls(c);
    var ang = slider(cl, "Angle", 180);
    var len = slider(cl, "Streak Length", 549.39);
    slider(cl, "Threshold", 0.85);
    var kn = slider(cl, "Knee", 1.0);
    slider(cl, "Streak Intensity", 5);
    slider(cl, "Falloff", 4.24);
    slider(cl, "Glow Amount", 0.97);
    var mix = slider(cl, "Mix", 1);
    kf(mix.property(1), [[ON, 0], [ON + 6, 1, 33, 80]]);
    ang = cl.property("ADBE Effect Parade").property("Angle");
    kf(ang.property(1), [[66, 180, 33, 70], [80, 200.3, 80, 33]]);
    len = cl.property("ADBE Effect Parade").property("Streak Length");
    kf(len.property(1), [[100, 549.39, 33, 70], [114, 1920, 80, 33], [134, 1920, 33, 70], [148, 549.39, 80, 33]]);
    kn = cl.property("ADBE Effect Parade").property("Knee");
    kf(kn.property(1), [[150, 1.0, 33, 60], [160, 0.7, 80, 33]]);
    cl.moveToBeginning();

    note(c, "Hail Mary rebuilds the reel's custom shader natively: the highlights comp keys the bright pixels with Extract (Threshold sets the Black Point, Knee the Black Softness), and the streak comp adds 49 shifted copies of them in Add mode, each weighted by exp(-Falloff x i / 24) times Streak Intensity. The result is added over the untouched shot with a small Directional Blur and Glow, while the pixel-stretch rows and the offset slice copy the hero frame's extra details. All eight shader sliders live on CONTROLS and are keyed like the reel's preview, tilting Angle from 180 to 200.3, dragging Streak Length out to 1920 for the comb look and pulling Knee down to 0.7. Swap your own shot inside Hail Mary - SOURCE A and raise Threshold or move the highlights mask if large bright areas start to bloom.");
    return c;
}
