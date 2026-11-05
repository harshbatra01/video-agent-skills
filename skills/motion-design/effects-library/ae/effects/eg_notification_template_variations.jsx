// meta key: eg_notification_template_variations
// meta title: Essential Graphics Template
// meta order: 17
// meta refs: analysis/DaSns3-PXuz/ref_eg_notification_variations_7.67.png, analysis/DaSns3-PXuz/ref_eg_notification_variations_8.93.png, analysis/DaSns3-PXuz/ref_eg_notification_variations_9.33.png, analysis/DaSns3-PXuz/ref_eg_notification_variations_10.33.png, analysis/DaSns3-PXuz/ref_eg_notification_variations_11.00.png
// Staged copy: neutral names, fonts from FONTS (lib/effects_lib.jsx). Source: a friend's Mac effects library (Oct 2026).
// Technique demo (reel DaSns3-PXuz, Window > Essential Graphics). One notification comp "UI" exposes Title, Message,
// Time and an Icon dropdown in Essential Graphics. The main comp nests it six times and changes each copy through its
// Essential Properties (keyed with hold keys) instead of duplicating comps. Motion copied from the reel frame by frame:
// a pull-back from the single card to the cluster (speed peaks on the cut at frame 40), one blank frame at 80, then the
// variations land with a small 3D tilt and motion blur.
function build_eg_notification_template_variations() {
    var TITLE = "Essential Graphics Template";
    var DUR = 6, CUT = 40, SWAP = 80;
    var FM = FONTS.medium, FR = FONTS.regular, FB = FONTS.bold;
    var WHITE = [1, 1, 1];
    // Icon dropdown order = the order of the icons in the Icons comp (frame 0 = item 1)
    var APPS = [
        ["Messages", "4+ new messages"],
        ["Chat", "7 unread messages."],
        ["Team", "Message from X Media."],
        ["Payments", "Payout balance: $10K."],
        ["Wallet", "Received $400 from Sam."],
        ["Clips", "Mia posted a new video."]
    ];

    // ---------------------------------------------------------------- small helpers (local)
    function shapeLayer(comp, name) { var l = comp.layers.addShape(); l.name = name; P(l).setValue([0, 0]); return l; }
    function addRectGroup(l, w, h, r, x, y, fill, stroke, sw) {
        var g = shapeGroup(l);
        var rc = g.addProperty("ADBE Vector Shape - Rect");
        rc.property("ADBE Vector Rect Size").setValue([w, h]); rc.property("ADBE Vector Rect Roundness").setValue(r);
        rc.property("ADBE Vector Rect Position").setValue([x, y]);
        var root = l.property("ADBE Root Vectors Group"), gg = root.property(root.numProperties).property("ADBE Vectors Group");
        if (stroke) { var st = gg.addProperty("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Color").setValue(stroke); st.property("ADBE Vector Stroke Width").setValue(sw || 2); }
        if (fill) { gg = root.property(root.numProperties).property("ADBE Vectors Group"); var f = gg.addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(fill); }
    }
    function addEllipseGroup(l, w, h, x, y, fill, stroke, sw) {
        var g = shapeGroup(l);
        var el = g.addProperty("ADBE Vector Shape - Ellipse");
        el.property("ADBE Vector Ellipse Size").setValue([w, h]); el.property("ADBE Vector Ellipse Position").setValue([x, y]);
        var root = l.property("ADBE Root Vectors Group"), gg = root.property(root.numProperties).property("ADBE Vectors Group");
        if (stroke) { var st = gg.addProperty("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Color").setValue(stroke); st.property("ADBE Vector Stroke Width").setValue(sw || 2); }
        if (fill) { gg = root.property(root.numProperties).property("ADBE Vectors Group"); var f = gg.addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(fill); }
    }
    function addPathGroup(l, verts, closed, fill, stroke, sw) {
        var g = shapeGroup(l);
        var sh = new Shape(); sh.vertices = verts; sh.closed = !!closed;
        g.addProperty("ADBE Vector Shape - Group").property("ADBE Vector Shape").setValue(sh);
        var root = l.property("ADBE Root Vectors Group"), gg = root.property(root.numProperties).property("ADBE Vectors Group");
        if (stroke) {
            var st = gg.addProperty("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Color").setValue(stroke); st.property("ADBE Vector Stroke Width").setValue(sw || 2);
            gg = root.property(root.numProperties).property("ADBE Vectors Group");
            st = gg.property("ADBE Vector Graphic - Stroke"); st.property("ADBE Vector Stroke Line Cap").setValue(2); st.property("ADBE Vector Stroke Line Join").setValue(2);
        }
        if (fill) { gg = root.property(root.numProperties).property("ADBE Vectors Group"); var f = gg.addProperty("ADBE Vector Graphic - Fill"); f.property("ADBE Vector Fill Color").setValue(fill); }
    }
    // one keyframe with explicit speed (units per FRAME) and influence (%) on both sides
    function keyAt(prop, f, v, inSpd, inInf, outSpd, outInf) {
        prop.setValueAtTime(f / FPS, v);
        var idx = prop.nearestKeyIndex(f / FPS), n = 1;
        if (!prop.isSpatial && (prop.propertyValueType == PropertyValueType.TwoD || prop.propertyValueType == PropertyValueType.ThreeD)) n = prop.keyValue(idx).length;
        var a = [], b = [];
        for (var d = 0; d < n; d++) {
            a.push(new KeyframeEase(prop.isSpatial ? Math.abs(inSpd * FPS) : inSpd * FPS, Math.max(0.1, inInf)));
            b.push(new KeyframeEase(prop.isSpatial ? Math.abs(outSpd * FPS) : outSpd * FPS, Math.max(0.1, outInf)));
        }
        try { prop.setTemporalEaseAtKey(idx, a, b); } catch (e) { log("  ease " + prop.name + ": " + e.toString()); }
    }
    function holdAll(prop) { for (var k = 1; k <= prop.numKeys; k++) prop.setInterpolationTypeAtKey(k, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD); }
    function oneFrame(l, k) { l.inPoint = k / FPS; l.outPoint = (k + 1) / FPS; }

    // ---------------------------------------------------------------- Icons comp: one icon per frame (frame 0 = item 1)
    var IW = 200, IC = 100;
    var icons = effectComp(TITLE + " - Icons", DUR, IW, IW);
    // 6 Clips: play triangle with two offset tints
    var ic6 = shapeLayer(icons, "6 Clips");
    addPathGroup(ic6, [[76, 57], [76, 137], [140, 97]], true, WHITE, null, 0);      // first group draws on top
    addPathGroup(ic6, [[70, 54], [70, 134], [134, 94]], true, hex("#8FD6FF"), null, 0);
    addPathGroup(ic6, [[82, 60], [82, 140], [146, 100]], true, hex("#FFB86B"), null, 0);
    oneFrame(ic6, 5);
    // 5 Wallet: two-tone bold W
    var w5b = txt(icons, "W", FB, 128, hex("#58C4FF"), ParagraphJustification.CENTER_JUSTIFY, 0, IC + 7, IC + 5);
    w5b.name = "5 Wallet back"; centreAnchor(w5b); P(w5b).setValue([IC + 7, IC + 5]); oneFrame(w5b, 4);
    var w5 = txt(icons, "W", FB, 128, hex("#1565D8"), ParagraphJustification.CENTER_JUSTIFY, 0, IC, IC);
    w5.name = "5 Wallet"; centreAnchor(w5); P(w5).setValue([IC, IC]); oneFrame(w5, 4);
    // 4 Payments: violet dollar sign
    var p4 = txt(icons, "$", FB, 150, hex("#A78BFA"), ParagraphJustification.CENTER_JUSTIFY, 0, IC, IC);
    p4.name = "4 Payments"; centreAnchor(p4); P(p4).setValue([IC, IC]); oneFrame(p4, 3);
    // 3 Team: four coloured rounded squares
    var t3 = shapeLayer(icons, "3 Team");
    addRectGroup(t3, 46, 46, 14, 74, 74, hex("#5B8DEF"));
    addRectGroup(t3, 46, 46, 14, 126, 74, hex("#86A9F3"));
    addRectGroup(t3, 46, 46, 14, 74, 126, hex("#3E6FD6"));
    addRectGroup(t3, 46, 46, 14, 126, 126, hex("#A9C1F6"));
    oneFrame(t3, 2);
    // 2 Chat: neon green speech bubble outline with three dots
    var c2 = shapeLayer(icons, "2 Chat");
    var GREEN = hex("#5FD1C1");
    addEllipseGroup(c2, 112, 104, 100, 96, null, GREEN, 10);
    addPathGroup(c2, [[62, 128], [52, 152], [80, 142]], false, null, GREEN, 10);
    addEllipseGroup(c2, 15, 15, 76, 96, GREEN, null, 0);
    addEllipseGroup(c2, 15, 15, 100, 96, GREEN, null, 0);
    addEllipseGroup(c2, 15, 15, 124, 96, GREEN, null, 0);
    oneFrame(c2, 1);
    // 1 Messages: cool 4-colour gradient tile (solid + 4-Color Gradient, alpha matte = rounded square) + white bubble
    var m1g = shapeLayer(icons, "1 Messages bubble");
    addEllipseGroup(m1g, 80, 70, 100, 96, null, WHITE, 9);
    addPathGroup(m1g, [[76, 120], [68, 138], [90, 128]], false, null, WHITE, 9);
    oneFrame(m1g, 0);
    var m1s = solidL(icons, "1 Messages gradient", hex("#C53A8E"));
    fxp(m1s, "ADBE 4ColorGradient", [["Point 1", [30, 30]], ["Color 1", hex("#3B5BDB")], ["Point 2", [170, 30]], ["Color 2", hex("#4DABF7")],
        ["Point 3", [30, 170]], ["Color 3", hex("#63E6BE")], ["Point 4", [170, 170]], ["Color 4", hex("#748FFC")]], "4-Color Gradient");
    var m1t = rrect(icons, "1 Messages tile (matte)", 140, 140, 36, hex("#C53A8E"), null, 0, IC, IC);
    m1t.moveBefore(m1s);
    matte(m1s, m1t, TrackMatteType.ALPHA);
    try { m1t.enabled = false; } catch (emt) {}
    oneFrame(m1s, 0); oneFrame(m1t, 0);
    m1g.moveToBeginning();
    note(icons, "Icon artwork, one icon per frame (frame 0 = Messages ... frame 5 = Clips). The Icon layer in the UI comp is time-remapped to frame (Icon dropdown - 1). Neutral placeholder marks, no real app logos.");

    // ---------------------------------------------------------------- UI comp: the template (named 'UI' in the reel)
    var UW = 1000, UH = 380, CX = 500, CY = 180, CW = 885, CH = 228;
    var LEFT = CX - CW / 2, RIGHT = CX + CW / 2;
    var ui = effectComp(TITLE + " - UI", DUR, UW, UH);
    var cont = rrect(ui, "Main container", CW, CH, 56, hex("#05070C"), null, 0, CX, CY);
    fxp(cont, "ADBE Drop Shadow", [["Shadow Color", [0, 0, 0]], ["Opacity", 0.42 * 255], ["Direction", 180], ["Distance", 16], ["Softness", 48]], "Drop Shadow");
    // glossy right / bottom rim: a blurred light ring shifted up-left, clipped to the card by an alpha matte
    var gm = rrect(ui, "Gloss matte", CW, CH, 56, WHITE, null, 0, CX, CY);
    var gl = rrect(ui, "Edge gloss", CW, CH, 56, null, hex("#B9BDC8"), 8, CX - 11, CY - 4);
    gl.moveBefore(gm);
    fxp(gl, "ADBE Gaussian Blur 2", [["Blurriness", 7], ["ADBE Gaussian Blur 2-0003", 0]], "Gaussian Blur");
    O(gl).setValue(62);
    gm.moveBefore(gl);
    matte(gl, gm, TrackMatteType.ALPHA);
    // icon: the Icons comp, time-remapped by the dropdown, with a soft Glow like the reel's logos
    var icL = addComp(ui, icons, "Icon");
    P(icL).setValue([LEFT + 42 + 70, CY - 2]);
    S(icL).setValue([100, 100]);
    fxp(icL, "ADBE Glo2", [["Glow Threshold", 45], ["Glow Radius", 24], ["Glow Intensity", 0.7]], "Glow");
    // texts
    var tTitle = txt(ui, APPS[0][0], FM, 60, WHITE, ParagraphJustification.LEFT_JUSTIFY, -8, LEFT + 209, CY - 10); tTitle.name = "Title";
    var tMsg = txt(ui, APPS[0][1], FR, 50, hex("#8A8F99"), ParagraphJustification.LEFT_JUSTIFY, -8, LEFT + 209, CY + 54); tMsg.name = "Message";
    var tNow = txt(ui, "now.", FR, 40, hex("#8A8F99"), ParagraphJustification.RIGHT_JUSTIFY, 0, RIGHT - 54, CY + 13); tNow.name = "Time";
    // controller: Dropdown Menu Control 'Icon' (script-friendly stand-in for the reel's media-replacement logo)
    var ctl = ui.layers.addNull(DUR); ctl.name = "Controller"; P(ctl).setValue([60, 40]);
    fx(ctl, "ADBE Dropdown Control");
    try { ctl.property("ADBE Effect Parade").property(1).property(1).setPropertyParameters(["Messages", "Chat", "Team", "Payments", "Wallet", "Clips"]); }
    catch (em) { log("  dropdown items " + em.toString()); }
    try { ctl.property("ADBE Effect Parade").property(1).name = "Icon"; } catch (enm) { log("  dropdown rename " + enm.toString()); }
    var menu = ctl.property("ADBE Effect Parade").property(1).property(1);
    try {
        icL.timeRemapEnabled = true;
        var trp = icL.property("ADBE Time Remapping");
        trp.expression = 'framesToTime(Math.round(thisComp.layer("Controller").effect("Icon")("Menu").value) - 1)';
        icL.outPoint = DUR;
    } catch (etr) { log("  icon time remap " + etr.toString()); }
    icL.moveToBeginning(); tTitle.moveToBeginning(); tMsg.moveToBeginning(); tNow.moveToBeginning(); ctl.moveToBeginning();

    // Essential Graphics panel: name 'Notification', primary comp = this UI comp
    var EGP_OK = true;
    try { ui.openInEssentialGraphics(); } catch (eo) { log("  openInEssentialGraphics " + eo.toString()); }
    try { ui.motionGraphicsTemplateName = "Notification"; } catch (en) { log("  EGP name " + en.toString()); }
    var expose = [[tTitle.property("Source Text"), "Title"], [tMsg.property("Source Text"), "Message"], [tNow.property("Source Text"), "Time"], [menu, "Icon"]];
    for (var x = 0; x < expose.length; x++) {
        try {
            if (expose[x][0].canAddToMotionGraphicsTemplate(ui)) expose[x][0].addToMotionGraphicsTemplateAs(ui, expose[x][1]);
            else { log("  EGP cannot add " + expose[x][1]); EGP_OK = false; }
        } catch (ea) { log("  EGP add " + expose[x][1] + ": " + ea.toString()); EGP_OK = false; }
    }
    note(ui, "The template ('UI' in the reel). Window > Essential Graphics: Name 'Notification', Primary 'UI', properties Title, Message, Time (Source Text) and Icon (the Dropdown Menu Control on Controller, which time-remaps the Icon layer). Change the look here once and every nested copy follows.");

    // ---------------------------------------------------------------- main comp
    var c = effectComp(TITLE, DUR);
    c.motionBlur = true;
    try { c.shutterAngle = 360; c.shutterPhase = -180; } catch (es) {}
    solidL(c, "BG", hex("#FDFDFD"));
    // CLUSTER: the pull-back. Anchor sits low in the cluster so one scale move goes from the single centred card
    // (98 %) to the whole cluster (44 %). Speeds read off the reel: 5-6 % per frame at the cut, long tail after.
    var cl = c.layers.addNull(DUR); cl.name = "CLUSTER (pull-back)"; cl.threeDLayer = true;
    A(cl).setValue([0, 306, 0]); P(cl).setValue([960, 659.5, 0]);
    var sc = S(cl);
    keyAt(sc, 0, [98, 98, 98], 0, 33, 0, 80);
    keyAt(sc, CUT, [66, 66, 66], -6, 10, -5, 25);
    keyAt(sc, CUT + 6, [54, 54, 54], -1, 40, -1, 20);
    keyAt(sc, 75, [44, 44, 44], 0, 50, 0, 33);
    keyAt(sc, DUR * FPS, [43.2, 43.2, 43.2], 0, 33, 0, 33);
    var clOp = slider(cl, "Cluster Opacity", 100);
    var cop = clOp.property(1);
    kf(cop, [[SWAP - 1, 100], [SWAP, 0], [SWAP + 1, 55], [SWAP + 2, 86], [SWAP + 3, 100]]);
    for (var ck = 1; ck <= cop.numKeys; ck++) cop.setInterpolationTypeAtKey(ck, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
    cop.setInterpolationTypeAtKey(1, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.HOLD);
    // SWAP SETTLE: the variations land with a small 3D tilt (rotation about the cluster centre)
    var st = c.layers.addNull(DUR); st.name = "SWAP SETTLE (tilt in)"; st.threeDLayer = true;
    st.parent = cl; A(st).setValue([0, 0, 0]); P(st).setValue([0, 0, 0]); S(st).setValue([100, 100, 100]);
    var trX = tr(st).property("ADBE Rotate X"), trY = tr(st).property("ADBE Rotate Y"), trZ = tr(st).property("ADBE Rotate Z");
    kf(trX, [[SWAP, 0], [SWAP + 1, 16, 33, 12], [SWAP + 6, 0, 75, 33]]);
    kf(trY, [[SWAP, 0], [SWAP + 1, -11, 33, 12], [SWAP + 6, 0, 75, 33]]);
    kf(trZ, [[SWAP, 0], [SWAP + 1, -1.5, 33, 12], [SWAP + 6, 0, 75, 33]]);
    kf(S(st), [[SWAP, [100, 100, 100]], [SWAP + 1, [106, 106, 106], 33, 12], [SWAP + 6, [100, 100, 100], 75, 33]]);
    var rotProps = [trX, trY, trZ, S(st)];
    for (var rp = 0; rp < rotProps.length; rp++) rotProps[rp].setInterpolationTypeAtKey(1, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.HOLD);

    function eprop(L, nm) {
        var g = null;
        try { g = L.essentialProperty; } catch (e1) { g = null; }
        if (!g) { try { g = L.property("ADBE Layer Overrides"); } catch (e2) { g = null; } }
        if (!g) return null;
        try { return g.property(nm); } catch (e3) { return null; }
    }
    function setText(p, f, s) {
        if (!p) return;
        try { var td = p.valueAtTime(f / FPS, false); td.text = s; p.setValueAtTime(f / FPS, td); }
        catch (e1) { try { p.setValueAtTime(f / FPS, s); } catch (e2) { log("  set text " + e2.toString()); } }
    }
    // the six copies: offsets measured on the reel cluster (template px; card 885 = reel 352)
    var SLOTS = [["UI - centre (original)", [0, 143], 0], ["UI - top", [0, -410], 1], ["UI - mid left", [-611, -126], 2],
                 ["UI - mid right", [613, -126], 3], ["UI - bottom left", [-611, 410], 4], ["UI - bottom right", [613, 410], 5]];
    var OPX = 'value * thisComp.layer("CLUSTER (pull-back)").effect("Cluster Opacity")("Slider") / 100';
    var first = null;
    for (var n = 0; n < SLOTS.length; n++) {
        var Ln = c.layers.add(ui); Ln.name = SLOTS[n][0];
        Ln.threeDLayer = true; Ln.motionBlur = true;
        A(Ln).setValue([CX, CY, 0]);
        Ln.parent = st; P(Ln).setValue([SLOTS[n][1][0], SLOTS[n][1][1], 0]); S(Ln).setValue([100, 100, 100]);
        tr(Ln).property("ADBE Rotate X").setValue(0); tr(Ln).property("ADBE Rotate Y").setValue(0); R(Ln).setValue(0);
        O(Ln).expression = OPX;
        if (n > 0) {
            kf(O(Ln), [[0, 0], [CUT, 100]]); holdAll(O(Ln));
            var v = APPS[SLOTS[n][2]];
            setText(eprop(Ln, "Title"), 0, APPS[0][0]); setText(eprop(Ln, "Message"), 0, APPS[0][1]);
            setText(eprop(Ln, "Title"), SWAP, v[0]); setText(eprop(Ln, "Message"), SWAP, v[1]);
            var ic = eprop(Ln, "Icon");
            if (ic) { try { ic.setValueAtTime(0, 1); ic.setValueAtTime(SWAP / FPS, SLOTS[n][2] + 1); holdAll(ic); } catch (ei) { log("  icon key " + ei.toString()); } }
            else log("  no Icon essential property on " + Ln.name);
        } else first = Ln;
    }
    first.moveBefore(c.layer("BG"));
    // caption in the reel's style (white, bold, dark drop shadow + wide grey halo)
    var cap = txt(c, "one graphic", FB, 104, WHITE, ParagraphJustification.CENTER_JUSTIFY, -30, 960, 800);
    cap.name = "CAPTION";
    setText(cap.property("Source Text"), 0, "one graphic");
    setText(cap.property("Source Text"), CUT, "6 copies");
    setText(cap.property("Source Text"), SWAP, "6 variations.");
    fxp(cap, "ADBE Drop Shadow", [["Shadow Color", [0, 0, 0]], ["Opacity", 0.6 * 255], ["Direction", 180], ["Distance", 5], ["Softness", 16]], "Drop Shadow");
    fxp(cap, "ADBE Drop Shadow", [["Shadow Color", [0.25, 0.25, 0.27]], ["Opacity", 0.32 * 255], ["Direction", 180], ["Distance", 34], ["Softness", 150]], "Halo");
    cap.moveToBeginning();
    st.moveToBeginning(); cl.moveToBeginning(); cap.moveToBeginning();

    note(c, "Essential Graphics template: the 'UI' comp exposes Title, Message, Time and an Icon dropdown in Window > Essential Graphics (name 'Notification'), and this comp nests it six times, setting each copy in its Essential Properties instead of making six comps. The copies start identical, CLUSTER pulls back from one card to all six (98 to 44 %, speed peaks on the cut at frame 40, shutter 360), and at frame 80 one blank frame hides the swap: hold keys on each copy's Essential Properties change app, text and icon while SWAP SETTLE tilts the cluster in (X 16, Y -11 deg to 0 over 5 frames). Edit the card once inside the UI comp, or type new text and pick an icon on any copy's Essential Properties.");
    if (!EGP_OK) log("  EGP not fully set up");
    return c;
}
