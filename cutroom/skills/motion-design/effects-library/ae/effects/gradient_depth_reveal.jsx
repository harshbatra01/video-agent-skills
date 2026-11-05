// meta key: gradient_depth_reveal
// meta title: Gradient Depth Reveal
// meta order: 7
// meta refs: analysis/DdwPfZJTGiP/ref_gradient_depth_reveal_1.20.png, analysis/DdwPfZJTGiP/ref_gradient_depth_reveal_1.60.png, analysis/DdwPfZJTGiP/ref_gradient_depth_reveal_1.80.png, analysis/DdwPfZJTGiP/ref_gradient_depth_reveal_2.07.png, analysis/DdwPfZJTGiP/ref_gradient_depth_reveal_depthmap_6.00.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// The depth map is turned into flowing pastel colour bands (a looping gradient map driven by time), then the real clip
// reveals through Gradient Wipe with the depth map as its gradient: nearest pixels first, the sky last.
function build_gradient_depth_reveal() {
    var DIAG = false;
    var DUR = 4.3;
    var MAIN = "Gradient Depth Reveal";
    var SKY_BOTTOM = 625;                 // y below which nothing is keyed as sky (keeps the white goal posts out)

    function rectMask(l, x0, y0, x1, y1, feather) {
        var m = l.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        var s = new Shape(); s.vertices = [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]; s.closed = true;
        m.property("ADBE Mask Shape").setValue(s);
        if (feather) m.property("ADBE Mask Feather").setValue([feather, feather]);
        return m;
    }
    // the looping pastel palette sampled at phase L + time * speed (what Colorama's Output Cycle does)
    function toneExpr(L) {
        return "var L = " + L + ";\nvar spd = thisComp.layer(\"CONTROLS\").effect(\"Phase Speed (deg per s)\")(\"Slider\") / 360;\n" +
            "var P = [[0, [236,198,168]], [0.20, [195,118,230]], [0.375, [217,113,210]], [0.597, [232,174,218]], [0.778, [177,149,224]], [1.0, [236,198,168]]];\n" +
            "var ph = ((L + time * spd) % 1 + 1) % 1; var c = P[0][1];\n" +
            "for (var i = 0; i < P.length - 1; i++) { if (ph >= P[i][0] && ph <= P[i + 1][0]) { c = linear(ph, P[i][0], P[i + 1][0], P[i][1], P[i + 1][1]); break; } }\n" +
            "[c[0] / 255, c[1] / 255, c[2] / 255, 1];";
    }
    function pastelToner(l) {
        var tn = fxp(l, "CC Toner", [], "CC Toner (looping palette)");
        setDeep(tn, "Tones", 3);
        var TN = [["Highlights", 1.0], ["Brights", 0.75], ["Midtones", 0.5], ["Darktones", 0.25], ["Shadows", 0.0]];
        for (var i = 0; i < TN.length; i++) {
            tn = l.property("ADBE Effect Parade").property("CC Toner (looping palette)");
            var tp = findProp(tn, TN[i][0]);
            if (tp) { try { tp.expression = toneExpr(TN[i][1]); } catch (ee) { log("  toner expr " + TN[i][0] + ": " + ee.toString()); } }
            else log("  toner: no " + TN[i][0]);
        }
    }

    // ---- SOURCE: a shot with clear depth layers (near grass, far trees, sky). The camera tilts down after 3.5 s, so the
    // hand-built depth map below matches best early; the reveal is finished by then.
    var src = sourceComp(MAIN + " - SOURCE A", "field_runner.mov", DUR);
    var mat = sourceComp(MAIN + " - SOURCE A matte", "field_runner_matte.mov", DUR);

    // ---- DEPTH MAP (white = near, black = far). Built natively; drop a real depth video (Depth Anything) in here instead.
    var dm = effectComp(MAIN + " - DEPTH MAP (white = near)", DUR);
    // ground and trees: a vertical ramp bent by Levels gamma, so far things stay dark grey and the near grass gets most of the range
    var ramp = solidL(dm, "Ground ramp (far dark grey to near white)", [0, 0, 0]);
    fxp(ramp, "ADBE Ramp", [["Start of Ramp", [960, 280]], ["Start Color", [0, 0, 0]], ["End of Ramp", [960, 1080]], ["End Color", [1, 1, 1]], ["Ramp Shape", 1]], "Gradient Ramp");
    var rl = fx(ramp, "ADBE Easy Levels2"); rl.name = "Levels (bend the ramp)";
    rl = ramp.property("ADBE Effect Parade").property("Levels (bend the ramp)");
    setp(rl, "Gamma", 0.45); setp(rl, "Output Black", 0.1);
    var sky = solidL(dm, "Sky = far (black)", [0, 0, 0]);
    var skyKey = addComp(dm, src, "Sky key (Extract keeps the bright sky)");
    fxp(skyKey, "ADBE Extract", [["Black Point", 150], ["White Point", 255], ["Black Softness", 40], ["White Softness", 0]], "Extract");
    rectMask(skyKey, -20, -20, 1940, SKY_BOTTOM, 20);
    matte(sky, skyKey, TrackMatteType.ALPHA);
    var near = solidL(dm, "Runner = near (light grey)", [0.9, 0.9, 0.9]);
    var nm = addComp(dm, mat, "Runner matte");
    matte(near, nm, TrackMatteType.LUMA);
    var tex = addComp(dm, src, "Texture (clip in Black & White, Overlay 35 %)");
    fxp(tex, "ADBE Black&White", [], "Black & White");
    tex.blendingMode = BlendingMode.OVERLAY; O(tex).setValue(35);
    var soft = adjL(dm, "Soften like a depth model");
    gaussBlur(soft, 8);
    soft.moveToBeginning();

    // ---- main comp: Depth Map (colour bands) under the Clip (Gradient Wipe by depth)
    var c = effectComp(MAIN, DUR);
    var dl = addComp(c, dm, "Depth Map");
    var cr = fxp(dl, "APC Colorama", [], "Colorama (tutorial version, off)");
    var ps = findProp(cr, "Phase Shift");
    if (ps) { try { ps.expression = "time*200"; } catch (ep) { log("  colorama phase: " + ep.toString()); } }
    dl.property("ADBE Effect Parade").property("Colorama (tutorial version, off)").enabled = false;
    pastelToner(dl);

    var clip = addComp(c, src, "Clip");
    var gw = fxp(clip, "ADBE Gradient Wipe", [["Transition Softness", 1], ["Gradient Placement", 3], ["Invert Gradient", 0]], "Gradient Wipe");
    try { gw.property("Gradient Layer").setValue(dl.index); } catch (eg) { log("  gradient layer: " + eg.toString()); }
    gw = clip.property("ADBE Effect Parade").property("Gradient Wipe");
    // 100 % at f30 (1:00) -> 0 % at f96 (3:06): fast start (out 5 %), long tail (in 70 %). With Softness 100 % the visible
    // reveal runs about f36-f70 (grass at 1.3 s, hills 1.8 s, sky haze clearing by 2.3 s), fitted to the reel's frames.
    // (scripting reads this percent as 0-1)
    kf(gw.property("Transition Completion"), [[30, 1, 33, 5], [96, 0, 70, 33]]);

    var ctl = controls(c);
    slider(ctl, "Phase Speed (deg per s)", 200);
    ctl.moveToBeginning();

    note(c, "Gradient Depth Reveal. 'Depth Map' plays the depth comp through CC Toner (Pentone) whose five tone colours sample a looping pastel palette at time x Phase Speed, so colour bands flow through the depth (the tutorial does this with Colorama, Phase Shift = time*200; that Colorama sits on the layer switched off). 'Clip' sits on top with Gradient Wipe, Gradient Layer = Depth Map, Softness 100 %, keyed 100 % at 1:00 to 0 % at 3:06 with a fast start and a long tail, so the nearest pixels turn real first and the sky last. Put your own depth video into the DEPTH MAP comp to reuse it.");
    if (!DIAG) return c;

    var dg = effectComp(MAIN + " - DIAG", DUR);
    var q1 = addComp(dg, dm, "dm"); S(q1).setValue([50, 50]); P(q1).setValue([480, 270]);
    var q2 = addComp(dg, c, "main"); S(q2).setValue([50, 50]); P(q2).setValue([1440, 270]);
    var q3 = addComp(dg, src, "src"); S(q3).setValue([50, 50]); P(q3).setValue([480, 810]);
    var rc = effectComp(MAIN + " - DIAG ramp", DUR, 960, 540);
    var rs = solidL(rc, "ramp", [0, 0, 0]);
    fxp(rs, "ADBE Ramp", [["Start of Ramp", [0, 270]], ["Start Color", [0, 0, 0]], ["End of Ramp", [960, 270]], ["End Color", [1, 1, 1]], ["Ramp Shape", 1]]);
    var rctl = controls(rc); slider(rctl, "Phase Speed (deg per s)", 200);
    var rr = addComp(rc, (function () { var k = effectComp(MAIN + " - DIAG ramp src", DUR, 960, 540); var s2 = solidL(k, "r", [0, 0, 0]); fxp(s2, "ADBE Ramp", [["Start of Ramp", [0, 270]], ["Start Color", [0, 0, 0]], ["End of Ramp", [960, 270]], ["End Color", [1, 1, 1]], ["Ramp Shape", 1]]); return k; })(), "toned");
    pastelToner(rr);
    P(rr).setValue([480, 405]); S(rr).setValue([100, 50]);
    var q4 = addComp(dg, rc, "ramp"); P(q4).setValue([1440, 810]);
    return dg;
}
