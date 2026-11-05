// meta key: mixed_media_cutout
// meta title: Mixed Media
// meta order: 11
// meta refs: analysis/DdL719cApOS/ref_mixed_media_wipe_0.67.png, analysis/DdL719cApOS/ref_mixed_media_2.40.png, analysis/DdL719cApOS/ref_mixed_media_22.00.png, analysis/DdL719cApOS/ref_mixed_media_21.20.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// Photocopy background + colour sticker cut-out, all stepping at 12 fps. Background: Black & White, a coarse Fractal Noise
// stipple, then one adjustment layer crushes Levels and Tints ink #1E2327 / paper #DBD8D3, with paper specks on top.
// Subject: the colour clip through a person matte, a little desaturated, over a white Minimax border with a thin dark rim.
// The original colour clip wipes away right to left (Linear Wipe on hold keys) one frame after the sticker switches on.
function build_mixed_media_cutout() {
    var DUR = 5;
    var MAIN = "Mixed Media";
    var S0 = 20;              // frame the sticker switches on; the background wipe starts one frame later
    var START = 0.5;          // source seconds to start from (footage and matte stay in sync)

    function post12(l) { fxp(l, "ADBE Posterize Time", [["Frame Rate", 12]], "Posterize Time"); }
    function ef(l, nm) { return l.property("ADBE Effect Parade").property(nm); }
    function harden(l) { fxp(l, "ADBE Easy Levels2", [["Input Black", 0.3], ["Input White", 0.7]], "Levels (harden matte edge)"); }

    // ---- SOURCE + MATTE. The matte (white = subject) was made outside AE (Apple Vision person segmentation);
    // for your own shot, put a Roto Brush or AI matte in the MATTE comp.
    var src = sourceComp(MAIN + " - SOURCE A", "field_runner.mov", DUR, { start: START });
    var mat = sourceComp(MAIN + " - MATTE (white = subject)", "field_runner_matte.mov", DUR, { start: START });

    var c = effectComp(MAIN, DUR);
    var ctl = controls(c);
    slider(ctl, "Outline Width", 5);
    slider(ctl, "Stipple Grain %", 40);

    // MM_BG: the shot in black and white, sky pushed bright so Levels can flatten it to paper
    var bg = addComp(c, src, "MM_BG (black & white)");
    post12(bg);
    fxp(bg, "ADBE Black&White", [["Blues", 280], ["Cyans", 240], ["Greens", 50], ["Yellows", 70]], "Black & White");
    fxp(bg, "ADBE Unsharp Mask2", [["Amount", 160], ["Radius", 2], ["Threshold", 0]], "Unsharp Mask");

    // MM_Stipple: coarse grain under the photocopy adjustment, so Levels turns it into toner dots in the mid-tones
    var st = solidL(c, "MM_Stipple grain (Overlay)", [0.5, 0.5, 0.5]);
    st.blendingMode = BlendingMode.OVERLAY;
    var fs = fxp(st, "ADBE Fractal Noise", [["Contrast", 130]], "Fractal Noise (stipple)");
    setDeep(ef(st, "Fractal Noise (stipple)"), "Noise Type", 3);
    setDeep(ef(st, "Fractal Noise (stipple)"), "Complexity", 1);
    setDeep(ef(st, "Fractal Noise (stipple)"), "Scale", 2);
    var sc = findProp(ef(st, "Fractal Noise (stipple)"), "Scale"); if (sc) log("  mm param check: stipple Scale = " + sc.value);
    var rs = findProp(ef(st, "Fractal Noise (stipple)"), "Random Seed");
    if (rs) rs.expression = "Math.floor(time * 12);"; else log("  mm param: no Random Seed");
    O(st).expression = 'thisComp.layer("CONTROLS").effect("Stipple Grain %")("Slider");';

    // MM_Photocopy: one adjustment layer = crushed Levels + ink/paper Tint over the two layers below it
    var pc = adjL(c, "MM_Photocopy (Levels + Tint)");
    fxp(pc, "ADBE Easy Levels2", [["Input Black", 0.1], ["Input White", 0.72], ["Gamma", 0.92]], "Levels");
    fxp(pc, "ADBE Tint", [["Map Black To", hex("#1E2327")], ["Map White To", hex("#DBD8D3")], ["Amount to Tint", 100]], "Tint (ink + paper)");

    // MM_Paper: dark dust specks (Multiply), changing with every 12 fps frame
    var dust = solidL(c, "MM_Paper specks (Multiply)", [1, 1, 1]);
    dust.blendingMode = BlendingMode.MULTIPLY; O(dust).setValue(65);
    fxp(dust, "ADBE Fractal Noise", [["Contrast", 400], ["Brightness", 185]], "Fractal Noise (specks)");
    setDeep(ef(dust, "Fractal Noise (specks)"), "Noise Type", 1);
    setDeep(ef(dust, "Fractal Noise (specks)"), "Scale", 4);
    setDeep(ef(dust, "Fractal Noise (specks)"), "Complexity", 1);
    var ev = findProp(ef(dust, "Fractal Noise (specks)"), "Evolution"); if (ev) ev.expression = "time * 400;";
    post12(dust);

    // MM_Original: the colour clip, wiped away right to left on hold keys
    var orig = addComp(c, src, "MM_Original (colour, Linear Wipe)");
    var lw = fxp(orig, "ADBE Linear Wipe", [["Wipe Angle", 270], ["Feather", 50]], "Linear Wipe");
    var tcp = lw.property("Transition Completion");
    var K = [[0, 5], [1, 45], [2, 50], [4, 55], [6, 58], [8, 80], [10, 98], [11, 100]];
    tcp.setValueAtTime(S0 / FPS, 0);
    for (var k = 0; k < K.length; k++) tcp.setValueAtTime((S0 + 1 + K[k][0]) / FPS, K[k][1]);
    for (var h = 1; h <= tcp.numKeys; h++) tcp.setInterpolationTypeAtKey(h, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD);
    orig.outPoint = (S0 + 13) / FPS;

    // MM_Outline: the matte grown by Minimax, turned into alpha, filled light grey, thin dark rim from Drop Shadow
    var ol = addComp(c, mat, "MM_Outline (sticker border)");
    post12(ol);
    harden(ol);
    var mm = fxp(ol, "ADBE Minimax", [["Radius", 5]], "Minimax (grow)");
    for (var di = 1; di <= mm.numProperties; di++) { try { var dp = mm.property(di); log("  mm param dump: " + dp.name + " = " + dp.value); } catch (ed) {} }
    try { findProp(mm, "Radius").expression = 'Math.round(thisComp.layer("CONTROLS").effect("Outline Width")("Slider"));'; } catch (e1) { log("  mm param: minimax radius expr " + e1.toString()); }
    var sh = fxp(ol, "ADBE Shift Channels", [], "Shift Channels (alpha from luma)");
    try { ef(ol, "Shift Channels (alpha from luma)").property("Take Alpha From").setValue(5); } catch (e2) { log("  mm param: shift alpha " + e2.toString()); }
    fxp(ol, "ADBE Fill", [["Color", hex("#E4E6E6")]], "Fill");
    gaussBlur(ol, 0.7);
    shadow(ol, 0.55, 0, 3);
    ol.inPoint = S0 / FPS;

    // MM_Subject: colour subject through the matte, 40 % less saturated, faded blacks, a touch sharper
    var sub = addComp(c, src, "MM_Subject (colour cut-out)");
    post12(sub);
    fxp(sub, "ADBE HUE SATURATION", [], "Hue/Saturation");
    setDeep(ef(sub, "Hue/Saturation"), "Master Saturation", -40);
    fxp(sub, "ADBE Easy Levels2", [["Output Black", 0.07]], "Levels (fade blacks)");
    fxp(sub, "ADBE Unsharp Mask2", [["Amount", 60], ["Radius", 1.5]], "Unsharp Mask");
    var sm = addComp(c, mat, "MM_Matte (hidden)");
    post12(sm);
    harden(sm);
    sm.moveBefore(sub);
    matte(sub, sm, TrackMatteType.LUMA);
    sub.inPoint = S0 / FPS; sm.inPoint = S0 / FPS;

    // MM_Grain: fine grain over everything at the full 30 fps
    var gr = adjL(c, "MM_Grain (every frame)");
    fxp(gr, "ADBE Noise2", [["Amount of Noise", 5], ["Noise Type", 0]], "Noise");
    gr.inPoint = S0 / FPS;

    // stack, top to bottom: CONTROLS, grain, matte, subject, outline, original, specks, photocopy, stipple, bg
    pc.moveBefore(bg); st.moveAfter(pc);
    dust.moveBefore(pc);
    orig.moveBefore(dust);
    ol.moveBefore(orig);
    sub.moveBefore(ol);
    sm.moveBefore(sub);
    gr.moveToBeginning();
    ctl.moveToBeginning();

    note(c, "Mixed Media: a photocopy background with a colour sticker cut-out, all stepping at 12 fps (Posterize Time). MM_BG goes Black & White with the sky pushed bright, MM_Stipple adds coarse Fractal Noise in Overlay, and the MM_Photocopy adjustment crushes Levels (in 10 / 72 %) and Tints ink #1E2327 to paper #DBD8D3; specks multiply on top. MM_Subject shows the colour runner through the matte (Saturation -40) over MM_Outline, the matte grown 5 px by Minimax and filled light grey with a thin Drop Shadow rim. MM_Original wipes off right to left on hold keys one frame after the sticker appears; for your own shot swap SOURCE A and put its subject matte in the MATTE comp.");
    return c;
}
