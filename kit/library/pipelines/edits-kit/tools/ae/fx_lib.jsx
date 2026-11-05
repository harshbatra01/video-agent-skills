// fx_lib.jsx: optical transitions and hero effects, rebuilt from frame-by-frame study of top edits (14 Oct 2026).
// Needs ae_lib.jsx + edits_lib.jsx first (ES3). Every transition is adjustment layers / band-size solids spanning the
// cut, keyed PER FRAME, placed BELOW the letterbox bars.
// What the study taught (round 1-2 vs the reference frames, tools/compare.py):
// - Transitions are LUMINOUS and OPTICAL (light, streaks, blur, colour floods, line-art strobes), never geometric
//   (no rigid spins / slides / boxes / blades: the user rejected those as "PowerPoint").
// - Flat white lasts 1-3 frames at most. The body of a transition keeps STRUCTURE and COLOUR (streaks, blobs, tints).
//   Never stack exposure + glow + screen on the same frames: that is how rounds 1-2 turned everything into blank white.
// - Think in frames: a top transition is a recipe of 6-12 distinct frames (frameRecipe below).
// Param matchNames were dumped from this AE (tools/ae/probe/effects_params.txt).

var F1 = 1 / FPS;
function kf(prop, list, inInf, outInf) {        // [[t, v], ...] then ease every key
    for (var i = 0; i < list.length; i++) prop.setValueAtTime(list[i][0], list[i][1]);
    for (var j = 1; j <= prop.numKeys; j++) easeKey(prop, j, inInf || 60, outInf || 60);
}
// per-frame keys: values[i] lands on frame (t + (o + i) frames); linear between frames (they are 1 frame apart anyway)
function fk(prop, t, o, values) {
    for (var i = 0; i < values.length; i++) prop.setValueAtTime(t + (o + i) * F1, values[i]);
    for (var j = 1; j <= prop.numKeys; j++) { try { prop.setInterpolationTypeAtKey(j, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR); } catch (e) {} }
}
function mn(eff, name) { return eff.property(name); }
function holdAll(prop) { for (var j = 1; j <= prop.numKeys; j++) { try { prop.setInterpolationTypeAtKey(j, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD); } catch (e) {} } }
function bandC(comp) { var fb = frameBox(comp); return [fb.cx, fb.cy]; }
function colourFrames(comp, name, col, t, o, ops, mode) {   // ops[i] = opacity on frame t + (o + i)
    var s = bandSolid(comp, name, col); s.inPoint = t + o * F1; s.outPoint = t + (o + ops.length) * F1;
    if (mode) s.blendingMode = mode;
    var op = O(s); for (var i = 0; i < ops.length; i++) op.setValueAtTime(t + (o + i) * F1, ops[i]); holdAll(op);
    return s;
}
function bandSolid(comp, name, col) { var fb = frameBox(comp), s = solidL(comp, name, col, comp.width, fb.h); P(s).setValue([fb.cx, fb.cy]); return s; }

// ------------------------------------------------------------------ 0. band extend: lives in edits_lib clip()
// In a letterbox layout the footage only covers the band; distortions (blur, spin, shake) would pull black from above /
// below. clip() gives every footage layer Motion Tile (output height 300%, mirror edges) when BAND is set, so there is
// mirrored picture beyond the band. (Tried and failed: an adjustment-layer Motion Tile SCALES the whole comp into the
// tile and squashed the picture; a Transform stretch of the edge rows needed a 90x buffer: GPU out of memory.)
function bandExtend(comp) { return null; }

// ------------------------------------------------------------------ 1. frame recipe (strobe language)
// One character per frame from t. A top-edit transition is often a sequence of distinct 1-frame looks:
//   E line art on white      K glowing lines on black (lineCol)     I colour negative     N mono negative
//   B hard B&W               W white frame        X black frame      S bright vertical streak
//   D dark vertical streak   C colour vertical streak (saturated)    H bright horizontal streak
//   Z zoom-blur burst        R Y U G P O colour frames (red yellow blue green purple orange, picture ghosting)
//   . untouched
// e.g. LeBron "Highest in the Room" 41.87: "EKEKSDSDCC". Mbappe Nightcrawler 20.80: "YYYYRRRRRR".
var RECIPE_COL = { R: [1, 0.13, 0.07], Y: [1, 0.9, 0.35], U: [0.1, 0.25, 1], G: [0.2, 1, 0.25], P: [0.55, 0.1, 1], O: [1, 0.5, 0.08] };
function frameRecipe(comp, t, pattern, lineCol) {
    var out = [];
    for (var i = 0; i < pattern.length; i++) {
        var ch = pattern.charAt(i), t0 = t + i * F1; if (ch == ".") continue;
        if (ch == "W" || ch == "X") { var s0 = bandSolid(comp, "frame " + ch + " " + t0.toFixed(3), ch == "W" ? [1, 1, 1] : [0, 0, 0]); s0.inPoint = t0; s0.outPoint = t0 + F1; out.push(s0); continue; }
        if (RECIPE_COL[ch]) { var sc = bandSolid(comp, "frame " + ch + " " + t0.toFixed(3), RECIPE_COL[ch]); sc.inPoint = t0; sc.outPoint = t0 + F1; O(sc).setValue(86); out.push(sc); continue; }
        var a = adjSpan(comp, "frame " + ch + " " + t0.toFixed(3), t0, t0 + F1);
        if (ch == "E" || ch == "K") {   // lift + contrast first, so dark night footage still gives lines
            var pre = fx(a, "ADBE Exposure2"); setp(pre, "ADBE Exposure2-0003", 1.2);
            setp(fx(a, "ADBE Brightness & Contrast 2"), "ADBE Brightness & Contrast 2-0002", 45);
            fx(a, "ADBE Find Edges"); fx(a, "ADBE Black&White");
            if (ch == "K") {   // ref L ~20: mostly black, sparse thin lines
                fx(a, "ADBE Invert"); var lv = fx(a, "ADBE Easy Levels2"); setDeep(lv, "Input Black", 0.3); setDeep(lv, "Input White", 0.9);
                if (lineCol) { var ti = fx(a, "ADBE Tint"); setp(ti, "ADBE Tint-0001", [0, 0, 0]); setp(ti, "ADBE Tint-0002", lineCol); }
                glow(a, 30, 18, 0.6);
            } else { var lv2 = fx(a, "ADBE Easy Levels2"); setDeep(lv2, "Input Black", 0.2); setDeep(lv2, "Input White", 0.78); }   // ref 237/24: white paper, thin lines
        } else if (ch == "T" || ch == "V") {   // impact frames: hard B&W threshold, V inverted (anime impact frames)
            setp(fx(a, "ADBE Threshold2"), "ADBE Threshold2-0001", 0.43);   // NORMALIZED 0-1 from scripts (110 / 255)
            if (ch == "V") fx(a, "ADBE Invert");
        } else if (ch == "I") { fx(a, "ADBE Invert"); }
        else if (ch == "N") { fx(a, "ADBE Black&White"); fx(a, "ADBE Invert"); }
        else if (ch == "B") { fx(a, "ADBE Black&White"); setp(fx(a, "ADBE Brightness & Contrast 2"), "ADBE Brightness & Contrast 2-0002", 70); }
        else if (ch == "S" || ch == "D" || ch == "C" || ch == "H") {
            var db = fx(a, "ADBE Motion Blur"); setp(db, "ADBE Motion Blur-0001", ch == "H" ? 90 : 0); setp(db, "ADBE Motion Blur-0002", 300);
            var tf = fx(a, "ADBE Geometry2"); try { tf.property("ADBE Geometry2-0011").setValue(0); tf.property(ch == "H" ? "ADBE Geometry2-0004" : "ADBE Geometry2-0003").setValue(180); } catch (e1) {}
            var ex = fx(a, "ADBE Exposure2");
            if (ch == "S" || ch == "H") { setp(ex, "ADBE Exposure2-0003", 3.5); setp(ex, "ADBE Exposure2-0004", 0.22); fx(a, "ADBE Black&White"); setp(fx(a, "ADBE Brightness & Contrast 2"), "ADBE Brightness & Contrast 2-0002", 40); }
            if (ch == "D") { setp(ex, "ADBE Exposure2-0003", -6.5); }
            if (ch == "C") { setp(ex, "ADBE Exposure2-0003", 2.3); setp(ex, "ADBE Exposure2-0004", 0.08); lumetri(a, { sat: 220, con: 55 }); }
        } else if (ch == "Z") {
            var tz = fx(a, "ADBE Geometry2"); try { tz.property("ADBE Geometry2-0001").setValue(bandC(comp)); tz.property("ADBE Geometry2-0002").setValue(bandC(comp)); tz.property("ADBE Geometry2-0003").setValue(130); } catch (e2) {}
            var rb = fx(a, "CC Radial Fast Blur"); mn(rb, "CC Radial Fast Blur-0001").setValue(bandC(comp)); setp(rb, "CC Radial Fast Blur-0002", 90); setp(rb, "CC Radial Fast Blur-0003", 2);
            setp(fx(a, "ADBE Exposure2"), "ADBE Exposure2-0003", 0.5);
        }
        out.push(a);
    }
    return out;
}

// ------------------------------------------------------------------ 2. light blow-out
// Per frame (0 = first frame of the next shot): -2 hot orange, -1/0/+1 cream-white, +2/+3 golden haze, then the
// warm cast fades by +8. ref: TikTok compilation 106.57-106.80 (orange, orange, white x3, golden x2, warm shot).
function lightBlowout(comp, t, warm, leakFile) {
    var a = adjSpan(comp, "blowout " + t.toFixed(2), t - 3 * F1, t + 8 * F1);
    var ex = fx(a, "ADBE Exposure2");      // frames t-3 .. t+7
    fk(mn(ex, "ADBE Exposure2-0003"), t, -3, [0, 1.2, 3, 3, 3, 2.2, 1.8, 0.5, 0.15, 0, 0]);
    var out = [a];
    out.push(colourFrames(comp, "blowout orange " + t.toFixed(2), [1, 0.45, 0.08], t, -2, [52]));
    out.push(colourFrames(comp, "blowout white " + t.toFixed(2), [1, 0.99, 0.97], t, -1, [93, 97, 92]));
    out.push(colourFrames(comp, "blowout gold " + t.toFixed(2), warm || [1, 0.86, 0.52], t, 2, [82, 76, 22, 8]));
    if (leakFile) { var lk = overlay(comp, leakFile, t + 2 * F1, 130, 55, BlendingMode.SCREEN); lk.outPoint = t + 7 * F1; out.push(lk); }
    return out;
}

// ------------------------------------------------------------------ 3. zoom rush (passed round 2: unchanged)
// Out-going rushes into the lens into pure streaks around the cut; the in-coming arrives over-zoomed, slightly rolled,
// settles over 7 frames. With chroma = rainbow tunnel. refs: Speed x Ronaldo 12.53-12.80, Greatest Football Edit 55.20.
function zoomRush(comp, t, pre, post, amt, center, blur) {
    var p = (pre || 3) * F1, q = (post || 7) * F1, k = 100 * (amt || 1.5), c = center || bandC(comp), b = blur || 95;
    var a = adjSpan(comp, "zoomrush " + t.toFixed(2), t - p, t + q);
    var tf = fx(a, "ADBE Geometry2");
    try { tf.property("ADBE Geometry2-0001").setValue(c); tf.property("ADBE Geometry2-0002").setValue(c); } catch (e) {}
    var sc = tf.property("ADBE Geometry2-0003");
    sc.setValueAtTime(t - p, 100); sc.setValueAtTime(t - 0.001, k); sc.setValueAtTime(t, k * 1.06); sc.setValueAtTime(t + q, 100);
    easeKey(sc, 1, 10, 90); easeKey(sc, 2, 90, 10); easeKey(sc, 3, 10, 92); easeKey(sc, 4, 96, 10);
    var ro = tf.property("ADBE Geometry2-0007");
    ro.setValueAtTime(t - p, 0); ro.setValueAtTime(t - 0.001, 5); ro.setValueAtTime(t, -7); ro.setValueAtTime(t + q, 0); easeKey(ro, 4, 95, 10);
    tfBlur(tf);
    var rb = fx(a, "CC Radial Fast Blur"); mn(rb, "CC Radial Fast Blur-0001").setValue(c); setp(rb, "CC Radial Fast Blur-0003", 2);
    var am = mn(rb, "CC Radial Fast Blur-0002");
    am.setValueAtTime(t - p, 0); am.setValueAtTime(t - 2 * F1, 55); am.setValueAtTime(t - F1, 88); am.setValueAtTime(t, b);
    am.setValueAtTime(t + 2 * F1, b * 0.8); am.setValueAtTime(t + q, 0);
    for (var i = 1; i <= am.numKeys; i++) easeKey(am, i, 50, 50); easeKey(am, am.numKeys, 95, 10);
    var ex = fx(a, "ADBE Exposure2"); kf(mn(ex, "ADBE Exposure2-0003"), [[t - p, 0], [t, 0.9], [t + q, 0]], 70, 40);
    return a;
}

// ------------------------------------------------------------------ 4. smear (streak hold)
// The picture becomes streaks along one axis for ~7 frames and the next shot resolves out of them. Exposure stays low
// (+0.5 max): the colour of the streaks is the point. ref: LeBron 16.87-17.00 (yellow / white / purple vertical bars).
function smear(comp, t, vertical, tintCol, len) {
    var a = adjSpan(comp, "smear " + t.toFixed(2), t - 2 * F1, t + 10 * F1), L = len || 320;
    var tf = fx(a, "ADBE Geometry2"); try { tf.property("ADBE Geometry2-0011").setValue(0); } catch (e0) {}
    fk(vertical ? tf.property("ADBE Geometry2-0003") : tf.property("ADBE Geometry2-0004"), t, -2, [100, 150, 190, 190, 190, 190, 190, 185, 170, 140, 110, 100]);
    var db = fx(a, "ADBE Motion Blur"); setp(db, "ADBE Motion Blur-0001", vertical ? 0 : 90);
    fk(mn(db, "ADBE Motion Blur-0002"), t, -2, [0, L * 0.6, L, L, L, L, L, L * 0.95, L * 0.8, L * 0.5, L * 0.2, 0]);
    var bc = fx(a, "ADBE Brightness & Contrast 2"); fk(mn(bc, "ADBE Brightness & Contrast 2-0002"), t, -2, [0, 45, 75, 75, 75, 75, 75, 75, 60, 35, 10, 0]);
    var ex = fx(a, "ADBE Exposure2"); fk(mn(ex, "ADBE Exposure2-0003"), t, -2, [0, 1.0, 1.8, 1.8, 1.8, 1.75, 1.7, 1.65, 1.3, 0.7, 0.2, 0]);
    if (tintCol) {
        var ti = fx(a, "ADBE Tint"); setp(ti, "ADBE Tint-0001", [tintCol[0] * 0.35, tintCol[1] * 0.2, tintCol[2] * 0.45]); setp(ti, "ADBE Tint-0002", tintCol);
        fk(mn(ti, "ADBE Tint-0003"), t, -2, [0, 22, 32, 32, 32, 32, 30, 26, 18, 10, 4, 0]);
    }
    return a;
}

// ------------------------------------------------------------------ 5. light painting (white kick + glowing figure on black)
// One white frame on the cut, then the next shot shows only its highlights, tinted (cyan), smeared sideways, on black,
// fading back to the normal picture over the hold. ref: Messi "SHOCK" 13.37-13.53.
function lightPaint(comp, t, col, hold) {
    var h = hold || 10, w = bandSolid(comp, "paint kick " + t.toFixed(2), [1, 1, 1]); w.inPoint = t - F1; w.outPoint = t;
    var a = adjSpan(comp, "light paint " + t.toFixed(2), t, t + (h + 4) * F1);
    var lv = fx(a, "ADBE Easy Levels2"); setDeep(lv, "Input Black", 0.36);
    var ti = fx(a, "ADBE Tint"); setp(ti, "ADBE Tint-0001", [0.05, 0.08, 0.12]); setp(ti, "ADBE Tint-0002", col || [0.62, 0.93, 1]);
    var db = fx(a, "ADBE Motion Blur"); setp(db, "ADBE Motion Blur-0001", 90); setp(db, "ADBE Motion Blur-0002", 300);
    glow(a, 45, 40, 0.5);
    var ex = fx(a, "ADBE Exposure2"); kf(mn(ex, "ADBE Exposure2-0003"), [[t, -0.3], [t + h * F1, -2.0]], 33, 33);
    var o = O(a); o.setValueAtTime(t, 100); o.setValueAtTime(t + h * F1, 100); o.setValueAtTime(t + (h + 4) * F1, 0);
    return [w, a];
}

// ------------------------------------------------------------------ 6. spin vortex (rotational blur tunnel, no twirl)
// A spin blur (Radial Blur, Spin) plus a zoom blur builds a swirling tunnel of the picture's own colours; scale up
// first so nothing outside the band is pulled in. ref: LeBron "Highest in the Room" 29.38-29.50.
function vortex(comp, t, spin) {
    var c = bandC(comp), a = adjSpan(comp, "vortex " + t.toFixed(2), t - 4 * F1, t + 10 * F1);
    var tf = fx(a, "ADBE Geometry2"); try { tf.property("ADBE Geometry2-0001").setValue(c); tf.property("ADBE Geometry2-0002").setValue(c); } catch (e) {}
    fk(tf.property("ADBE Geometry2-0003"), t, -4, [100, 108, 118, 130, 140, 142, 142, 140, 136, 128, 118, 110, 104, 100]);
    var rbl = fx(a, "ADBE Radial Blur"); try { setp(rbl, "ADBE Radial Blur-0003", 1); mn(rbl, "ADBE Radial Blur-0002").setValue(c); } catch (e1) { log("  vortex spin " + e1.toString()); }
    var s = spin || 42;
    fk(mn(rbl, "ADBE Radial Blur-0001"), t, -4, [0, s * 0.35, s * 0.7, s, s, s, s, s, s, s * 0.9, s * 0.6, s * 0.3, s * 0.1, 0]);
    var rb = fx(a, "CC Radial Fast Blur"); mn(rb, "CC Radial Fast Blur-0001").setValue(c); setp(rb, "CC Radial Fast Blur-0003", 2);
    fk(mn(rb, "CC Radial Fast Blur-0002"), t, -4, [0, 35, 70, 92, 96, 96, 96, 96, 94, 88, 70, 40, 12, 0]);
    var ex = fx(a, "ADBE Exposure2"); fk(mn(ex, "ADBE Exposure2-0003"), t, -4, [0, 0.4, 0.9, 1.3, 1.4, 1.4, 1.4, 1.4, 1.35, 1.2, 0.8, 0.4, 0.1, 0]);
    var bc = fx(a, "ADBE Brightness & Contrast 2"); fk(mn(bc, "ADBE Brightness & Contrast 2-0002"), t, -4, [0, 25, 55, 85, 95, 95, 95, 95, 90, 75, 50, 25, 8, 0]);
    var ds = fx(a, "ADBE Tint"); fk(mn(ds, "ADBE Tint-0003"), t, -4, [0, 15, 35, 55, 60, 60, 60, 60, 58, 50, 30, 12, 3, 0]);
    return a;
}

// ------------------------------------------------------------------ 7. colour flood (sequence)
// The frame floods with colour, the picture ghosting through, stepping through colours, then drains. cols each held
// 'each' frames. ref: Mbappe Nightcrawler 20.80-20.97 (yellow x4, red x6+). Round 2 was close; colours brighter now.
function colorFlood(comp, t, cols, each, op, drain, steps) {
    // steps = [[[r,g,b], frames, opacityStart, opacityEnd], ...]; without steps: cols each held for 'each' frames at op
    var out = [], fb = frameBox(comp), tt = t;
    if (!steps) { steps = []; for (var q = 0; q < cols.length; q++) steps.push([cols[q], each || 4, op || 92, q == cols.length - 1 ? (op || 92) * 0.6 : (op || 92)]); }
    for (var i = 0; i < steps.length; i++) {
        var c0 = steps[i][0], n = steps[i][1], s = bandSolid(comp, "flood " + i + " " + t.toFixed(2), c0);
        var r = fx(s, "ADBE Ramp"); setDeep(r, "Start of Ramp", [comp.width * 0.5, fb.h * 0.5]); setDeep(r, "End of Ramp", [comp.width * 1.0, fb.h * 1.2]);
        setDeep(r, "Start Color", [Math.min(1, c0[0] * 1.05 + 0.08), Math.min(1, c0[1] * 1.05 + 0.08), Math.min(1, c0[2] * 1.05 + 0.08)]);
        setDeep(r, "End Color", [c0[0] * 0.9, c0[1] * 0.9, c0[2] * 0.9]); setDeep(r, "Ramp Shape", 2);
        s.inPoint = tt; s.outPoint = tt + n * F1;
        var oo = O(s); for (var k = 0; k < n; k++) oo.setValueAtTime(tt + k * F1, steps[i][2] + (steps[i][3] - steps[i][2]) * (n > 1 ? k / (n - 1) : 0));
        holdAll(oo); out.push(s); tt += n * F1;
    }
    return out;
}

// ------------------------------------------------------------------ 8. light rays burst (impact)
// 2 frames of a bright, desaturated ray burst WITH structure (dark streaks radiating), then the shot returns glowing.
// ref: Speed x Ronaldo 26.37-26.43. (Round 2 was 4 frames of flat white: exposure now +0.9 max.)
function lightBurst(comp, t, x, y, peak) {
    var a = adjSpan(comp, "rays " + t.toFixed(2), t, t + 6 * F1);
    var lr = fx(a, "CC Light Rays"); mn(lr, "CC Light Rays-0002").setValue([x, y]);
    setp(lr, "CC Light Rays-0003", 140); setp(lr, "CC Light Rays-0004", 12);
    var pk = peak || 520; fk(mn(lr, "CC Light Rays-0001"), t, 0, [pk, pk * 0.8, pk * 0.35, pk * 0.15, pk * 0.05, 0]);
    var ex = fx(a, "ADBE Exposure2"); fk(mn(ex, "ADBE Exposure2-0003"), t, 0, [0.9, 0.7, 0.35, 0.15, 0.05, 0]);
    var bw = adjSpan(comp, "rays mono " + t.toFixed(2), t, t + 2 * F1); fx(bw, "ADBE Black&White"); O(bw).setValue(88);
    setp(fx(bw, "ADBE Brightness & Contrast 2"), "ADBE Brightness & Contrast 2-0002", 35);
    return [a, bw];
}

// ------------------------------------------------------------------ 9. defocus (blur space)
// Out-going melts into bright soft haze; the in-coming starts as glowing colour blobs on black and focuses over ~12
// frames. ref: Hero Edit "+5 hours" 14.35-14.53. Round 2 read well (vivid blobs); a longer focus pull now.
function defocus(comp, t, castCol, radius) {
    var r = radius || 120, a = adjSpan(comp, "defocus " + t.toFixed(2), t - 3 * F1, t + 12 * F1);
    var gb = fx(a, "ADBE Gaussian Blur 2"); setp(gb, "ADBE Gaussian Blur 2-0003", 1);
    fk(mn(gb, "ADBE Gaussian Blur 2-0001"), t, -3, [0, r * 0.35, r * 0.75, r, r * 0.95, r * 0.85, r * 0.72, r * 0.58, r * 0.45, r * 0.33, r * 0.22, r * 0.13, r * 0.06, r * 0.02, 0]);
    var ex = fx(a, "ADBE Exposure2"); fk(mn(ex, "ADBE Exposure2-0003"), t, -3, [0, 1.2, 2.2, 2.0, 1.8, 1.5, 1.2, 0.9, 0.65, 0.45, 0.25, 0.1, 0, 0, 0]);
    var bc = fx(a, "ADBE Brightness & Contrast 2"); fk(mn(bc, "ADBE Brightness & Contrast 2-0002"), t, -3, [0, 0, 0, 25, 25, 22, 18, 14, 10, 6, 3, 0, 0, 0, 0]);
    if (castCol) {
        var ti = fx(a, "ADBE Tint"); setp(ti, "ADBE Tint-0001", [castCol[0] * 0.05, castCol[1] * 0.05, castCol[2] * 0.08]); setp(ti, "ADBE Tint-0002", castCol);
        fk(mn(ti, "ADBE Tint-0003"), t, -3, [0, 10, 20, 75, 70, 62, 52, 42, 32, 22, 12, 5, 0, 0, 0]);
    }
    var tf = fx(a, "ADBE Geometry2"); fk(tf.property("ADBE Geometry2-0003"), t, -3, [100, 104, 108, 112, 111, 109, 107, 105, 104, 103, 102, 101, 100, 100, 100]);
    var hz = colourFrames(comp, "defocus haze " + t.toFixed(2), [0.7, 0.71, 0.73], t, -2, [45, 50], BlendingMode.NORMAL);
    var gl = colourFrames(comp, "defocus glow " + t.toFixed(2), castCol || [0.95, 0.3, 0.18], t, 0, [62, 58, 50, 42, 34, 26, 18, 11, 5], BlendingMode.SCREEN);
    return [a, hz, gl];
}

// ------------------------------------------------------------------ 10. radial chromatic split on a clip layer
// Red copy scaled up, blue copy scaled down (Add): colour fringes radiate from the centre, collapsing over [t0, t1].
function radialSplit(comp, L, t0, t1, amt) {
    var k = amt || 0.06, out = [], OFF = 10;
    var base = fx(L, "ADBE Shift Channels");
    var pr = base.property("ADBE Shift Channels-0002"), pb = base.property("ADBE Shift Channels-0004");
    pr.setValueAtTime(t0 - 0.002, 2); pr.setValueAtTime(t0, OFF); pr.setValueAtTime(t1, 2);
    pb.setValueAtTime(t0 - 0.002, 4); pb.setValueAtTime(t0, OFF); pb.setValueAtTime(t1, 4);
    var spec = [[2, OFF, OFF, 1 + k], [OFF, OFF, 4, 1 - k]];
    for (var i = 0; i < 2; i++) {
        var c = L.duplicate(); c.name = L.name + (i ? " blue" : " red");
        try { var ep = c.property("ADBE Effect Parade"); for (var q2 = ep.numProperties; q2 >= 1; q2--) if (ep.property(q2).matchName == "ADBE Shift Channels") ep.property(q2).remove(); } catch (er) {}
        var sc = fx(c, "ADBE Shift Channels"); setp(sc, "ADBE Shift Channels-0002", spec[i][0]); setp(sc, "ADBE Shift Channels-0003", spec[i][1]); setp(sc, "ADBE Shift Channels-0004", spec[i][2]);
        c.blendingMode = BlendingMode.ADD; c.inPoint = Math.max(L.inPoint, t0); c.outPoint = Math.min(L.outPoint, t1);
        var tf = fx(c, "ADBE Geometry2"); var cc = bandC(comp);
        try { tf.property("ADBE Geometry2-0001").setValue(cc); tf.property("ADBE Geometry2-0002").setValue(cc); } catch (e2) {}
        kf(tf.property("ADBE Geometry2-0003"), [[t0, 100 * spec[i][3]], [t1, 100]], 80, 30);
        c.moveBefore(L); out.push(c);
    }
    return out;
}

// ------------------------------------------------------------------ 11. aura (energy glow around the player)
// The matte grown, broken up by animated turbulence and blurred, in a saturated colour ADDED behind the player cutout;
// a wider, fainter copy gives the bloom. refs: Messi SHOCK 17.90 (purple), 27.20 (pink); Ronaldo "3 hours" 12.07.
function aura(comp, matteFile, t0, t1, rkM, focus, zoom, col, grow, soft, energy) {
    var out = [], c = col || [0.62, 0.2, 1];
    var spec = [[(grow || 18) * 2.2, (soft || 26) * 2.2, 60], [grow || 18, soft || 26, 100]];
    for (var i = 0; i < 2; i++) {
        var m2 = matteFor(comp, matteFile, t0, t1, rkM, focus, zoom); m2.name = "aura matte " + i + " " + t0.toFixed(2);
        var mm = fx(m2, "ADBE Minimax"); try { setDeep(mm, "Radius", spec[i][0]); setDeep(mm, "Operation", 2); } catch (e) { log("  aura minimax " + e.toString()); }
        if (energy !== false) {
            var td = fx(m2, "ADBE Turbulent Displace");
            setp(td, "ADBE Turbulent Displace-0002", 70); setp(td, "ADBE Turbulent Displace-0003", 45);
            mn(td, "ADBE Turbulent Displace-0006").expression = "time * " + (i ? 720 : 480);
        }
        var bb = fx(m2, "ADBE Box Blur2"); setp(bb, "Blur Radius", spec[i][1]); setp(bb, "Iterations", 3);
        var s = solidL(comp, "aura " + i + " " + t0.toFixed(2), c); s.inPoint = t0; s.outPoint = t1;
        s.setTrackMatte(m2, TrackMatteType.LUMA); s.blendingMode = BlendingMode.ADD; O(s).setValue(spec[i][2]);
        out.push(s);
    }
    return out;
}

// ------------------------------------------------------------------ 12. geometry + flash (14 Oct, after the v6 review)
// The user: "even geometry ones can be done if done well, mixed with flashes in interesting ways". These use what our
// pipeline has and fan packs do not: a SAM 2 matte of the player on every clip.

// silStack: graphic silhouette frames on the cut, one look per frame from t (Hamilton x Norris "4x4" 0.70-1.00):
// 'F' flat field colour + the next shot's player as a WHITE silhouette, 'I' white field + the player in the field
// colour, 'K' black field + white player, 'W' white frame, '.' the shot itself.
function silStack(comp, t, matteLayer, pattern, fieldCol) {
    var col = fieldCol || [0.62, 0.05, 0.18], out = [];
    for (var i = 0; i < pattern.length; i++) {
        var ch = pattern.charAt(i), t0 = t + i * F1; if (ch == ".") continue;
        var bg = ch == "F" ? col : (ch == "K" ? [0, 0, 0] : [1, 1, 1]);   // P = white field + BLACK player (poster)
        var f = bandSolid(comp, "stack " + ch + " " + t0.toFixed(3), bg); f.inPoint = t0; f.outPoint = t0 + F1; out.push(f);
        if (ch == "W") continue;
        var s = solidL(comp, "stack sil " + t0.toFixed(3), ch == "I" ? col : (ch == "P" ? [0, 0, 0] : [1, 1, 1])); s.inPoint = t0; s.outPoint = t0 + F1;
        s.setTrackMatte(matteLayer, TrackMatteType.LUMA); out.push(s);
    }
    return out;
}

// sliceOut: the frame cracks with light (hot white lines along the strip edges for 2 frames), then breaks into n strips
// that fly off in alternating directions with motion blur, revealing the next shot underneath; the beat lands on a
// white frame. Lout must already end at t - pre and Lin start at t - pre (build_edit extends them).
function sliceOut(comp, Lout, Lin, t, n, pre, vertical, flashOp) {
    var N = n || 6, f = pre || 4, t0 = t - f * F1, fb = frameBox(comp), W = comp.width, out = [];
    var A_ = A(Lout).valueAtTime(t0, false), P_ = P(Lout).valueAtTime(t0, false), S_ = S(Lout).valueAtTime(t0, false)[0] / 100;
    function toL(x, y) { return [A_[0] + (x - P_[0]) / S_, A_[1] + (y - P_[1]) / S_]; }
    var top = fb.cy - fb.h / 2, bot = fb.cy + fb.h / 2;
    for (var i = 0; i < N; i++) {
        var d = Lout.duplicate(); d.name = Lout.name + " slice " + i; d.inPoint = t0; d.outPoint = t; d.moveBefore(Lin);
        var a0, a1, b0, b1;
        if (vertical) { a0 = i * W / N; a1 = (i + 1) * W / N; b0 = top - 40; b1 = bot + 40; }
        else { a0 = -40; a1 = W + 40; b0 = top + i * fb.h / N; b1 = top + (i + 1) * fb.h / N; }
        var m = d.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"), sh = new Shape();
        sh.vertices = [toL(a0, b0), toL(a1, b0), toL(a1, b1), toL(a0, b1)]; sh.closed = true; m.property("ADBE Mask Shape").setValue(sh);
        var tf = fx(d, "ADBE Geometry2"), pp = tfp(tf, "pos"), v0 = pp.value, dir = (i % 2 ? 1 : -1);
        var dist = (vertical ? fb.h * 1.5 : W * 1.5) / S_, lag = (i % 3) * F1 * 0.5;
        pp.setValueAtTime(t0 + F1 + lag, v0);
        pp.setValueAtTime(t - 0.002, vertical ? [v0[0], v0[1] + dir * dist] : [v0[0] + dir * dist, v0[1]]);
        easeKey(pp, 1, 33, 90); easeKey(pp, 2, 10, 33);
        tfBlur(tf); d.motionBlur = true;
        var ex = fx(d, "ADBE Exposure2"); kf(mn(ex, "ADBE Exposure2-0003"), [[t0, 0.2], [t - F1, 1.2]], 33, 33);
        out.push(d);
        if (i > 0) {   // light crack along the boundary, first 2 frames
            var ln = vertical ? solidL(comp, "crack " + i, [1, 0.97, 0.9], 8, fb.h) : solidL(comp, "crack " + i, [1, 0.97, 0.9], W, 8);
            P(ln).setValue(vertical ? [a0, fb.cy] : [W / 2, b0]); ln.inPoint = t0; ln.outPoint = t0 + 2 * F1;
            glow(ln, 10, 45, 2.2); out.push(ln);
        }
    }
    Lout.outPoint = Math.min(Lout.outPoint, t0);
    out.push(colourFrames(comp, "slice flash " + t.toFixed(2), [1, 1, 1], t, 0, [flashOp || 82, 30]));
    return out;
}

// silIris: the next shot bursts out of its own player's silhouette: a copy of the in-coming clip shown through a copy of
// its matte that scales from small to huge about the player (sx, sy = source px) over the out-going shot, glowing; the
// beat lands on a white frame and the full next shot.
function silIris(comp, Lin, Min, t, pre, sx, sy, flashOp) {
    // per frame from t - pre: the window (his silhouette, scaled about him) grows 25% -> 700%; the next shot stays
    // readable inside it (v1 blew it out to white with exposure 1.8 + glow: read as a white frame); a hot white rim
    // traces the silhouette edge; the beat lands on a white frame.
    var f = pre || 6, t0 = t - f * F1;
    var grow = [25, 40, 70, 130, 260, 520, 900, 1200, 1500].slice(0, f);
    function scaled(name, extraGrow) {
        var mm = Min.duplicate(); mm.name = name; mm.inPoint = t0; mm.outPoint = t; mm.enabled = false;
        if (extraGrow) { var mx = fx(mm, "ADBE Minimax"); try { setDeep(mx, "Radius", extraGrow); setDeep(mx, "Operation", 2); } catch (e0) {} }
        var tf = fx(mm, "ADBE Geometry2");
        try { tf.property("ADBE Geometry2-0001").setValue([sx, sy]); tf.property("ADBE Geometry2-0002").setValue([sx, sy]); } catch (e) { log("  iris anchor " + e.toString()); }
        fk(tf.property("ADBE Geometry2-0003"), t0, 0, grow);
        return mm;
    }
    var d = Lin.duplicate(); d.name = Lin.name + " iris"; d.inPoint = t0; d.outPoint = t;
    var mm = scaled("iris matte " + t.toFixed(2), 0);
    d.setTrackMatte(mm, TrackMatteType.LUMA);
    var ex = fx(d, "ADBE Exposure2"); fk(mn(ex, "ADBE Exposure2-0003"), t0, 0, [0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, 0, 0].slice(0, f));
    var mr = scaled("iris rim matte " + t.toFixed(2), 10);
    var rim = solidL(comp, "iris rim " + t.toFixed(2), [1, 0.97, 0.9]); rim.inPoint = t0; rim.outPoint = t;
    rim.setTrackMatte(mr, TrackMatteType.LUMA); glow(rim, 20, 30, 1.4); rim.moveAfter(d);
    var wf = colourFrames(comp, "iris flash " + t.toFixed(2), [1, 1, 1], t, 0, [flashOp || 72, 22]);
    return [d, mm, mr, rim, wf];
}

// ------------------------------------------------------------------ 13. flash grid (the user's "geometry", 14 Oct)
// Flat flash panels lit frame by frame across the cut, the way the user's own GASS x Mbappe edit does it (cream top
// half, full frame, bottom half over the new shot, clean) and his description: "seven vertical rectangles appearing one
// by one, all white flashes, then fading into the next clip". The band is split into n panels (vertical = columns,
// else rows); seq[i] = a "0/1" string per panel for frame (o + i) relative to t; after the last frame every panel still
// lit fades out over fade frames. Crisp edges, hold keys: a new look every frame.
function flashGrid(comp, t, n, vertical, seq, o, col, fade, op) {
    var fb = frameBox(comp), W = comp.width, c = col || [0.94, 0.94, 0.9], out = [], f = fade || 0, pk = op || 100;
    for (var b = 0; b < n; b++) {
        var w = vertical ? Math.ceil(W / n) + 1 : W, h = vertical ? fb.h : Math.ceil(fb.h / n) + 1;
        var s = solidL(comp, "grid " + b + " " + t.toFixed(2), c, w, h);
        P(s).setValue(vertical ? [(b + 0.5) * W / n, fb.cy] : [W / 2, fb.cy - fb.h / 2 + (b + 0.5) * fb.h / n]);
        var first = -1, last = -1;
        for (var i = 0; i < seq.length; i++) if (seq[i].charAt(b) == "1") { if (first < 0) first = i; last = i; }
        if (first < 0) { s.remove(); continue; }
        var endF = (last == seq.length - 1) ? last + 1 + f : last + 1;
        s.inPoint = t + (o + first) * F1; s.outPoint = t + (o + endF) * F1;
        var oo = O(s);
        for (var j = first; j <= last; j++) oo.setValueAtTime(t + (o + j) * F1, seq[j].charAt(b) == "1" ? pk : 0);
        if (last == seq.length - 1) for (var k = 1; k <= f; k++) oo.setValueAtTime(t + (o + last + k) * F1, pk * (1 - k / (f + 1)));
        holdAll(oo); out.push(s);
    }
    return out;
}

// ------------------------------------------------------------------ 14. research pass 2 techniques (14 Oct)
// helpers: hold a layer (and its framing) on one moment, or play it delayed, via expressions on remap + transform
function holdAt(L, ti) {
    try { L.property("ADBE Time Remapping").expression = "valueAtTime(" + ti.toFixed(4) + ")"; } catch (e) { log("  hold remap " + e.toString()); }
    var props = [A(L), S(L), P(L)];
    for (var i = 0; i < props.length; i++) if (props[i].numKeys > 0) props[i].expression = "valueAtTime(" + ti.toFixed(4) + ")";
}
function delayBy(L, dt) {
    try { L.property("ADBE Time Remapping").expression = "valueAtTime(time - " + dt.toFixed(4) + ")"; } catch (e) { log("  delay remap " + e.toString()); }
}
function cutoutCopy(L, M, t0, t1, name) {   // a fresh copy of the clip shown through a fresh copy of its matte
    var d = L.duplicate(), m = M.duplicate(); d.name = name; m.name = name + " matte";
    d.inPoint = t0; d.outPoint = t1; m.inPoint = t0; m.outPoint = t1; m.enabled = false;
    d.setTrackMatte(m, TrackMatteType.LUMA);
    return [d, m];
}

// typeFlash: the flash carries a lyric word: per frame 'W' = black word on a white band, 'B' = white word on a black
// band, '.' = nothing (Charli xcx "Von dutch" lyric video). One ultra-condensed heavy face, fitted to the band.
function typeFlash(comp, t, word, pattern, size, font) {
    var fb = frameBox(comp), out = [], f = font || "Coolvetica-HeavyComp";
    for (var i = 0; i < pattern.length; i++) {
        var ch = pattern.charAt(i), t0 = t + i * F1; if (ch == ".") continue;
        var bgc = ch == "W" ? [1, 1, 1] : [0, 0, 0], tc = ch == "W" ? [0.04, 0.04, 0.05] : [1, 1, 1];
        var bg = bandSolid(comp, "typeflash bg " + t0.toFixed(3), bgc); bg.inPoint = t0; bg.outPoint = t0 + F1; out.push(bg);
        var l = txt(comp, word, f, size || 420, tc, ParagraphJustification.CENTER_JUSTIFY, 0, comp.width / 2, fb.cy);
        var r = centreAnchor(l); P(l).setValue([comp.width / 2, fb.cy]); l.inPoint = t0; l.outPoint = t0 + F1; out.push(l);
    }
    return out;
}

// freezeClone: across one bar a frozen copy of the player stays on each beat (times), all of them vanish on tEnd
// (put a white silhouette strobe on tEnd with the hits). Gatorade "FOREVER" ghosts.
function freezeClone(comp, L, M, times, tEnd) {
    var out = [];
    for (var i = 0; i < times.length; i++) {
        var cc = cutoutCopy(L, M, times[i], tEnd, "clone " + times[i].toFixed(2));
        holdAt(cc[0], times[i]); holdAt(cc[1], times[i]);
        var ex = fx(cc[0], "ADBE Exposure2"); setp(ex, "ADBE Exposure2-0003", 0.25 + 0.1 * i);
        out.push(cc[0], cc[1]);
    }
    // duplicates land directly above L, so every clone sits above the live clip: put a live cut-out on top of them all
    var live = cutoutCopy(L, M, times[0], tEnd, "clone live " + times[0].toFixed(2));
    if (out.length) live[0].moveBefore(out[0]);
    out.push(live[0], live[1]);
    return out;
}

// ghostTrail: n fading copies of the player, each dt later in the past, trail one move; they snap off at t1 and the
// live player stays sharp on top (NBA promo motion trails, Peter Sarellas).
function ghostTrail(comp, L, M, t0, t1, n, dt) {
    var out = [], N = n || 6, D = dt || 0.05;
    for (var i = 1; i <= N; i++) {   // each duplicate lands directly above L: g1 ends up on top, gN lowest
        var cc = cutoutCopy(L, M, t0, t1, "ghost " + i + " " + t0.toFixed(2));
        delayBy(cc[0], i * D); delayBy(cc[1], i * D);
        O(cc[0]).setValue(70 * Math.pow(0.78, i));
        var ti = fx(cc[0], "ADBE Tint"); setp(ti, "ADBE Tint-0003", 70);
        var ex = fx(cc[0], "ADBE Exposure2"); setp(ex, "ADBE Exposure2-0003", 0.8);
        out.push(cc[0], cc[1]);
    }
    var live = cutoutCopy(L, M, t0, t1, "ghost live " + t0.toFixed(2));
    if (out.length) live[0].moveBefore(out[0]);
    out.push(live[0], live[1]);
    return out;
}

// popFreeze: the moment freezes, the player pops forward 100 -> 114 -> 110% about (sx, sy) with a soft shadow while
// the frozen background blurs and darkens; a white frame opens it (FicTic pop-up cut-out freeze).
function popFreeze(comp, L, M, t, frames, sx, sy) {
    var n = frames || 8, t1 = t + n * F1, out = [];
    var bg = L.duplicate(); bg.name = "freeze bg " + t.toFixed(2); bg.inPoint = t; bg.outPoint = t1; holdAt(bg, t);
    var gb = fx(bg, "ADBE Gaussian Blur 2"); setp(gb, "ADBE Gaussian Blur 2-0003", 1); kf(mn(gb, "ADBE Gaussian Blur 2-0001"), [[t, 0], [t + 3 * F1, 26]], 33, 85);
    var ex = fx(bg, "ADBE Exposure2"); kf(mn(ex, "ADBE Exposure2-0003"), [[t, 0], [t + 3 * F1, -1.1]], 33, 85);
    out.push(bg);
    var cc = cutoutCopy(L, M, t, t1, "freeze pop " + t.toFixed(2)); holdAt(cc[0], t); holdAt(cc[1], t);
    cc[0].moveBefore(bg);
    var tf = fx(cc[0], "ADBE Geometry2");
    try { tf.property("ADBE Geometry2-0001").setValue([sx, sy]); tf.property("ADBE Geometry2-0002").setValue([sx, sy]); } catch (e) {}
    var sc = tf.property("ADBE Geometry2-0003"); sc.setValueAtTime(t, 100); sc.setValueAtTime(t + 2 * F1, 114); sc.setValueAtTime(t + 4 * F1, 110);
    easeKey(sc, 2, 33, 60); easeKey(sc, 3, 80, 33);
    shadow(cc[0], 0.6, 18, 40);
    out.push(cc[0], cc[1]);
    out.push(colourFrames(comp, "freeze flash " + t.toFixed(2), [1, 1, 1], t, 0, [90, 35]));
    return out;
}

// photoPrint: freeze, a white frame, then the moment as a white-bordered print on paper with a small label
// (AZgoat "Coldest moments x Photos"): the cream-panel look he likes, as a still.
function photoPrint(comp, L, t, frames, label, rot) {
    var n = frames || 12, t1 = t + n * F1, fb = frameBox(comp), out = [];
    var paper = bandSolid(comp, "print paper " + t.toFixed(2), [0.93, 0.92, 0.88]); paper.inPoint = t; paper.outPoint = t1; out.push(paper);
    var ph = L.duplicate(); ph.name = "print " + t.toFixed(2); ph.inPoint = t; ph.outPoint = t1; holdAt(ph, t);
    try { var ep = ph.property("ADBE Effect Parade"); for (var q = ep.numProperties; q >= 1; q--) if (ep.property(q).matchName == "ADBE Tile") ep.property(q).remove(); } catch (e0) {}
    var m = ph.property("ADBE Mask Parade").addProperty("ADBE Mask Atom"), sh = new Shape();
    var A_ = A(ph).valueAtTime(t, false), P_ = P(ph).valueAtTime(t, false), S_ = S(ph).valueAtTime(t, false)[0] / 100;
    function toL(x, y) { return [A_[0] + (x - P_[0]) / S_, A_[1] + (y - P_[1]) / S_]; }
    var mx = comp.width * 0.08, my = fb.h * 0.09;
    sh.vertices = [toL(mx, fb.cy - fb.h / 2 + my), toL(comp.width - mx, fb.cy - fb.h / 2 + my), toL(comp.width - mx, fb.cy + fb.h / 2 - my * 1.9), toL(mx, fb.cy + fb.h / 2 - my * 1.9)];
    sh.closed = true; m.property("ADBE Mask Shape").setValue(sh);
    var tf = fx(ph, "ADBE Geometry2"); try { tf.property("ADBE Geometry2-0001").setValue(toL(comp.width / 2, fb.cy)); tf.property("ADBE Geometry2-0002").setValue(toL(comp.width / 2, fb.cy)); } catch (e1) {}
    var rr = tf.property("ADBE Geometry2-0007"); rr.setValueAtTime(t, 0); rr.setValueAtTime(t + 3 * F1, rot || -2.5); easeKey(rr, 2, 85, 33);
    var sc = tf.property("ADBE Geometry2-0003"); sc.setValueAtTime(t, 108); sc.setValueAtTime(t + 3 * F1, 100); easeKey(sc, 2, 85, 33);
    shadow(ph, 0.45, 10, 24); ph.moveBefore(paper); out.push(ph);
    if (label) { var lb = caption(comp, label, t + 2 * F1, t1, comp.width / 2, fb.cy + fb.h / 2 - my * 0.95, 30, "ProximaNova-Semibold", 340, [0.12, 0.12, 0.13]); out.push(lb); }
    out.push(colourFrames(comp, "print flash " + t.toFixed(2), [1, 1, 1], t, 0, [95]));
    return out;
}

// outlineText: a hollow numeral / word (stroke only): the back layer of the numeral sandwich
function outlineText(comp, s, t0, t1, x, y, size, font, col, sw, from) {
    var l = comp.layers.addText(s), p = l.property("Source Text"), d = p.value;
    d.resetCharStyle(); d.resetParagraphStyle(); d.font = font || "GalanoGrotesque-Black"; d.fontSize = size;
    d.applyFill = false; d.applyStroke = true; d.strokeColor = col || [1, 1, 1]; d.strokeWidth = sw || 6; d.strokeOverFill = true;
    d.justification = ParagraphJustification.CENTER_JUSTIFY; p.setValue(d); P(l).setValue([x, y]);
    centreAnchor(l); l.name = s + " outline"; l.inPoint = t0; l.outPoint = t1; l.motionBlur = true; slamScale(l, t0, from || 125);
    return l;
}

// strikeWord: a name in tracked caps that gets struck through with a red bar on tStrike (a hit list ticked off,
// one name per knockout). The bar wipes across in 2 frames and the name dims under it.
function strikeWord(comp, text, t0, t1, tStrike, x, y, size, font, col, lineCol) {
    var l = txt(comp, text, font || "ProximaNova-Extrabld", size || 46, col || [1, 1, 1], ParagraphJustification.CENTER_JUSTIFY, 260, x, y);
    var r = centreAnchor(l); l.name = "name " + text; l.inPoint = t0; l.outPoint = t1;
    var o = O(l); o.setValueAtTime(t0, 0); o.setValueAtTime(t0 + 2 * F1, 100);
    if (tStrike !== null && tStrike !== undefined && tStrike < t1) { o.setValueAtTime(tStrike + 2 * F1, 100); o.setValueAtTime(tStrike + 5 * F1, 55); }
    var out = [l];
    if (tStrike !== null && tStrike !== undefined && tStrike < t1) {
        var w = r.width + 40, bar = solidL(comp, "strike " + text, lineCol || [0.9, 0.06, 0.1], Math.round(w), Math.max(6, Math.round((size || 46) * 0.16)));
        var p = P(l).value; P(bar).setValue([p[0], p[1]]); bar.inPoint = tStrike; bar.outPoint = t1;
        A(bar).setValue([0, bar.source.height / 2]); P(bar).setValue([p[0] - w / 2, p[1]]);
        var sc = S(bar); sc.setValueAtTime(tStrike, [0, 100]); sc.setValueAtTime(tStrike + 2 * F1, [100, 100]);
        out.push(bar);
    }
    return out;
}
