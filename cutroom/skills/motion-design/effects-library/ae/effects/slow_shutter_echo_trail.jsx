// meta key: slow_shutter_echo_trail
// meta title: Slow Shutter
// meta order: 9
// meta refs: analysis/Dd6h1XjRau7/ref_slow_shutter_before_17.50.png, analysis/Dd6h1XjRau7/ref_slow_shutter_18.20.png, analysis/Dd6h1XjRau7/ref_slow_shutter_19.00.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx).
// Slow shutter echo trail: the cut-out subject is smeared along its own motion (pixel-motion frame blending +
// CC Force Motion Blur at 720 deg), then Echo lays 5 discrete ghosts behind it (Composite In Back, Decay 0.75).
// A sharp copy of the subject sits on top so the leading frame stays crisp. 0.3 s clean, then a hard cut to the effect.
function build_slow_shutter_echo_trail() {
    var DUR = 3.5;
    var MAIN = "Slow Shutter";
    var CUT = 0.3;
    var CX = "comp(\"" + MAIN + "\").layer(\"CONTROLS\")";
    function ctl(n) { return CX + ".effect(\"" + n + "\")(\"Slider\")"; }

    // ---- SOURCE A + its subject matte (pixel-motion frame blending so sub-frame samples exist for the smear)
    var src = sourceComp("Slow Shutter - SOURCE A", "wall_dancer.mov", DUR, { start: 0 });
    var mat = sourceComp("Slow Shutter - MATTE", "wall_dancer_matte.mov", DUR, { start: 0 });
    var srcL = src.layer(1);
    var matL = mat.layer(1);
    fxp(matL, "ADBE Minimax", [["Operation", 2], ["Radius", 2], ["Channel", 2]], "Minimax (choke 2 px)");
    gaussBlur(matL, 1.0);
    srcL.frameBlendingType = FrameBlendingType.PIXEL_MOTION; src.frameBlending = true;
    matL.frameBlendingType = FrameBlendingType.PIXEL_MOTION; mat.frameBlending = true;

    // ---- SS_Subject: the dancer cut out by the matte
    var sub = effectComp("Slow Shutter - SS_Subject", DUR);
    var sl = addComp(sub, src, "SOURCE A");
    var ml = addComp(sub, mat, "MATTE");
    matte(sl, ml, TrackMatteType.LUMA);
    sub.frameBlending = true;

    // ---- SS_Smear: each instant smeared along its motion arc (Echo must sit on a separate layer to see this)
    var smc = effectComp("Slow Shutter - SS_Smear", DUR);
    var sml = addComp(smc, sub, "SS_Subject");
    fxp(sml, "CC Force Motion Blur", [["Motion Blur Samples", 8], ["Override Shutter Settings", 1], ["Shutter Angle", 720]], "CC Force Motion Blur");

    // ---- main comp
    var c = effectComp(MAIN, DUR);
    addComp(c, src, "SOURCE A (grade untouched)");

    var trail = addComp(c, smc, "SS_Trail");
    trail.inPoint = CUT;
    fxp(trail, "ADBE Echo", [], "Echo");
    var ec = trail.property("ADBE Effect Parade").property("Echo");
    ec.property(1).setValue(-4 / FPS);
    ec.property(2).setValue(5);
    ec.property(3).setValue(1.0);
    ec.property(4).setValue(0.75);
    ec.property(5).setValue(5);          // Echo Operator: Composite In Back
    ec = trail.property("ADBE Effect Parade").property("Echo");
    ec.property(1).expression = "-" + ctl("Echo Spacing (frames)") + " * thisComp.frameDuration;";
    ec = trail.property("ADBE Effect Parade").property("Echo");
    ec.property(2).expression = "Math.round(" + ctl("Number Of Echoes") + ");";
    ec = trail.property("ADBE Effect Parade").property("Echo");
    ec.property(4).expression = ctl("Decay") + ";";

    var sharp = addComp(c, sub, "SS_Sharp");
    sharp.inPoint = CUT;
    O(sharp).expression = ctl("Sharpness") + ";";

    var cl = controls(c);
    slider(cl, "Echo Spacing (frames)", 4);
    slider(cl, "Number Of Echoes", 5);
    slider(cl, "Decay", 0.75);
    slider(cl, "Sharpness", 100);
    cl.moveToBeginning();

    note(c, "The dancer is cut out with a matte and pre-smeared along his own motion with pixel-motion frame blending and CC Force Motion Blur at a 720 degree shutter. Echo on SS_Trail then lays five ghosts behind him (Composite In Back, Decay 0.75, 4 frames apart), and SS_Sharp keeps the leading frame crisp on top. The clean shot plays for 0.3 s before the hard cut to the effect, like the reel, and the CONTROLS sliders set spacing, ghost count, decay and sharpness.");
    return c;
}
