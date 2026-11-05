// motion_lib.jsx: two-key motion helpers and set pieces for After Effects builds (After Effects 2026, ES3 only).
// Load it AFTER ae_lib.jsx: ae_build.write_jsx(..., libs=[".../motion_lib.jsx"]) does that, since ae_lib always comes first.
// Needs the globals W, H, FPS that ae_build.py writes at the top of every generated script. acFinish() also needs a global
// VIGNETTE = path of a tube-vignette PNG (this skill ships assets/ae/vignette_ac.png).
// Origin: the base library of a short documentary reel (13 Oct 2026), reused unchanged for a second one, plus freeze(),
// chanOnly(), rectMatte(), faceMontage(), acGrade() and acFinish() from the first reel's second library.
// House rule (13 Oct 2026): never animate frame by frame. Every motion is
// TWO keys (start and end of the move) shaped in the speed graph, using the effects library's 20-50 easing rule:
//   settle = fast start, long settle (out influence 15 %, in 80 %)   moves that land
//   bell   = 73 / 73, the graph-peak curve                          moves that overlap the next one
//   accel  = slow start, fast end (out 80 %, in 15 %)               whips and squashes that leave on a cut
// Effects-library recipes used: Pixel Reveal, Smooth Text Transition, Cursor Reveal, Luma Dissolve, One-Frame Glitch, Whip Pan,
// Shake Chroma, Slow Shutter, Glowing Stroke.

var EASES = { settle: [15, 80], bell: [73, 73], accel: [80, 15], gentle: [45, 60] };
function fr(n) { return n / FPS; }
function setEase(prop, idx, inInf, outInf) {
    var n = 1;
    if (!prop.isSpatial && (prop.propertyValueType == PropertyValueType.TwoD || prop.propertyValueType == PropertyValueType.ThreeD)) n = prop.keyValue(idx).length;
    var a = [], b = [];
    for (var i = 0; i < n; i++) { a.push(new KeyframeEase(0, Math.max(0.1, inInf))); b.push(new KeyframeEase(0, Math.max(0.1, outInf))); }
    try { prop.setTemporalEaseAtKey(idx, a, b); } catch (e) { log("  ease " + prop.name + ": " + e.toString()); }
}
// k2: one move, two keys, eased in the graph. style: settle | bell | accel | gentle | hold | linear
function k2(prop, t0, v0, t1, v1, style) {
    if (!prop.canVaryOverTime) { try { prop.setValue(v1); } catch (e0) {} return; }
    prop.setValueAtTime(t0, v0); prop.setValueAtTime(t1, v1);
    var i0 = prop.nearestKeyIndex(t0), i1 = prop.nearestKeyIndex(t1);
    if (style == "hold") { prop.setInterpolationTypeAtKey(i0, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD); return; }
    if (style == "linear") {
        prop.setInterpolationTypeAtKey(i0, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR);
        prop.setInterpolationTypeAtKey(i1, KeyframeInterpolationType.LINEAR, KeyframeInterpolationType.LINEAR); return;
    }
    var e = EASES[style || "settle"];
    setEase(prop, i0, 33.3, e[0]); setEase(prop, i1, e[1], 33.3);
    if (prop.isSpatial) { try { prop.setSpatialTangentsAtKey(i0, [0, 0], [0, 0]); prop.setSpatialTangentsAtKey(i1, [0, 0], [0, 0]); } catch (es) {} }
}
function holdAt(prop, t, v) { prop.setValueAtTime(t, v); var i = prop.nearestKeyIndex(t); prop.setInterpolationTypeAtKey(i, KeyframeInterpolationType.HOLD, KeyframeInterpolationType.HOLD); }
function eff(l, mn, name) { var e = fx(l, mn); if (name) { try { e.name = name; } catch (en) {} } return l.property("ADBE Effect Parade").property(name || e.name); }
function eparam(l, effName, p) { var e = l.property("ADBE Effect Parade").property(effName); var q = null; try { q = e.property(p); } catch (x) { q = null; } return q || findProp(e, p); }
function setE(l, effName, p, v) { var q = eparam(l, effName, p); if (q) { try { q.setValue(v); } catch (e) { log("  set " + effName + "/" + p + ": " + e.toString()); } } else log("  no param " + effName + "/" + p); return q; }

var ROOTF = null, FOLD = {};
function bin(name) { if (FOLD[name]) return FOLD[name]; var f = app.project.items.addFolder(name); if (ROOTF) f.parentFolder = ROOTF; FOLD[name] = f; return f; }
function filed(item, folderName) { try { item.parentFolder = bin(folderName); } catch (e) {} return item; }
function pre(name, dur, w, h) { var c = newComp(name, dur, w, h); filed(c, "_precomps"); return c; }
function impF(path) { var it = imp(path); filed(it, "_footage"); return it; }

// ---------------------------------------------------------------- footage
// A source pixel (ax, ay) shown at the frame centre at scale s (percent); clamped so the frame never leaves the source.
function focusPos(ax, ay, sw, sh, sPct) {
    var s = sPct / 100, vw = W / s, vh = H / s;
    var x0 = Math.min(Math.max(ax - vw / 2, 0), Math.max(0, sw - vw)), y0 = Math.min(Math.max(ay - vh / 2, 0), Math.max(0, sh - vh));
    return [(ax - x0) * s, (ay - y0) * s];
}
// clipL: footage from srcIn, cover-fitted, zoom z0 -> z1 around focus (fxF, fyF as fractions of the source), two eased keys.
function clipL(c, path, t0, t1, srcIn, z0, z1, fxF, fyF, style, o) {
    o = o || {};
    var L = c.layers.add(impF(path));
    var base = cover(L, null, c.width, c.height);
    var sw = L.source.width, sh = L.source.height;
    var sp = o.speed || 1;
    if (sp != 1) L.stretch = 100 / sp;
    L.startTime = t0 - srcIn / sp;
    L.inPoint = t0; L.outPoint = t1;
    var ax = (fxF === undefined ? 0.5 : fxF) * sw, ay = (fyF === undefined ? 0.5 : fyF) * sh;
    A(L).setValue([ax, ay]);
    var s0 = base * z0, s1 = base * z1;
    var dx = o.dx || 0, p0 = focusPos(ax, ay, sw, sh, s0), p1 = focusPos(ax, ay, sw, sh, s1);
    p0[0] += dx; p1[0] += dx;   // o.dx: shift the framing sideways (split screens), by position so masks still line up
    if (Math.abs(z1 - z0) > 1e-4) {
        k2(S(L), t0, [s0, s0], t1, [s1, s1], style || "gentle");
        k2(P(L), t0, p0, t1, p1, style || "gentle");
    } else { S(L).setValue([s0, s0]); P(L).setValue(p0); }
    L.motionBlur = true;
    try { L.audioEnabled = false; } catch (ea) {}
    if (o.grade) grade(L, o.grade);
    if (o.name) L.name = o.name;
    return L;
}
// stillL: a PNG (press screenshot) framed like a crop: window centre (cx, cy) in image px at scale s, two eased keys.
function stillL(c, path, t0, t1, cx0, cy0, s0, cx1, cy1, s1, style) {
    var L = c.layers.add(impF(path));
    L.startTime = 0; L.inPoint = t0; L.outPoint = t1;
    P(L).setValue([W / 2, H / 2]);
    if (cx0 != cx1 || cy0 != cy1) k2(A(L), t0, [cx0, cy0], t1, [cx1, cy1], style || "gentle"); else A(L).setValue([cx0, cy0]);
    if (s0 != s1) k2(S(L), t0, [s0 * 100, s0 * 100], t1, [s1 * 100, s1 * 100], style || "gentle"); else S(L).setValue([s0 * 100, s0 * 100]);
    L.motionBlur = true;
    return L;
}
function grade(L, g) {
    if (g == "film") { exposure(L, -0.2); lumetri(L, { temp: -8 }); }
    else if (g == "bright") { exposure(L, 0.45); }
    else if (g == "cool") { lumetri(L, { temp: -14 }); }
    else if (g == "bw") { eff(L, "ADBE Black&White", "B&W"); var lv = eff(L, "ADBE Easy Levels2", "Levels BW"); setE(L, "Levels BW", "Input Black", 0.12); setE(L, "Levels BW", "Input White", 0.80); }
    else if (g == "bwhard") { eff(L, "ADBE Black&White", "B&W"); eff(L, "ADBE Easy Levels2", "Levels BW"); setE(L, "Levels BW", "Input Black", 0.10); setE(L, "Levels BW", "Input White", 0.72); setE(L, "Levels BW", "Gamma", 1.25); }
    else if (g == "invert") { eff(L, "ADBE Invert", "Invert"); }
    else if (g == "purple") { tint(L, [0.05, 0.02, 0.12], [0.75, 0.62, 1.0], 45); exposure(L, -0.24); }
}
function solidT(c, name, col, t0, t1) { var s = solidL(c, name, col); s.inPoint = t0; s.outPoint = t1; return s; }
// AC text-beat background: black with a faint centre glow
function beatBg(c, t0, t1, level) {
    var b = solidT(c, "beat bg", [0, 0, 0], t0, t1);
    var g = softEllipse(c, "beat glow", 1500, 900, [level || 0.10, level || 0.10, level || 0.10], W / 2, H / 2, 420, 100);
    g.inPoint = t0; g.outPoint = t1;
    return b;
}
// smear: the last frames of a shot streak sideways and burn (2 keys on blur, 2 on exposure)
function smearOut(L, t0, t1) {
    eff(L, "ADBE Motion Blur", "Smear"); setE(L, "Smear", "Direction", 90);
    k2(eparam(L, "Smear", "Blur Length"), t0, 0, t1, 230, "accel");
    var ex = eff(L, "ADBE Exposure2", "Smear burn");
    k2(eparam(L, "Smear burn", "Exposure"), t0, 0, t1, 1.4, "accel");
    L.outPoint = t1;
}
// Whip Pan (effects-library recipe): outgoing frame slides right and smears (accel into the cut), incoming arrives from the left and settles.
function whipOut(L, tCut, frames) {
    var t0 = tCut - fr(frames || 7);
    eff(L, "ADBE Tile", "Motion Tile"); setE(L, "Motion Tile", "Output Width", 300); setE(L, "Motion Tile", "Output Height", 130); setE(L, "Motion Tile", "Mirror Edges", 1);
    eff(L, "ADBE Geometry2", "Whip");
    k2(eparam(L, "Whip", "Position"), t0, [L.width / 2, L.height / 2], tCut, [L.width / 2 + 1900 / (S(L).value[0] / 100), L.height / 2 + 25], "accel");
    eff(L, "ADBE Motion Blur", "Whip blur"); setE(L, "Whip blur", "Direction", 90);
    k2(eparam(L, "Whip blur", "Blur Length"), t0, 0, tCut, 900, "accel");
}
function whipIn(L, tCut, frames) {
    var t1 = tCut + fr(frames || 6);
    eff(L, "ADBE Tile", "Motion Tile"); setE(L, "Motion Tile", "Output Width", 300); setE(L, "Motion Tile", "Output Height", 130); setE(L, "Motion Tile", "Mirror Edges", 1);
    eff(L, "ADBE Geometry2", "Whip");
    var sc = S(L).value[0] / 100;
    k2(eparam(L, "Whip", "Position"), tCut, [L.width / 2 - 1700 / sc, L.height / 2 - 25], t1, [L.width / 2, L.height / 2], "settle");
    eff(L, "ADBE Motion Blur", "Whip blur"); setE(L, "Whip blur", "Direction", 90);
    k2(eparam(L, "Whip blur", "Blur Length"), tCut, 900, t1, 0, "settle");
}
// Luma Dissolve (effects-library recipe, native S_DissolveLuma): Gradient Wipe with the layer as its own gradient, inverted.
function lumaDissolveIn(L, t0, t1) {
    eff(L, "ADBE Gradient Wipe", "Luma Dissolve");
    setE(L, "Luma Dissolve", "Transition Softness", 0.12); setE(L, "Luma Dissolve", "Gradient Placement", 3); setE(L, "Luma Dissolve", "Invert Gradient", 1);
    try { eparam(L, "Luma Dissolve", "Gradient Layer").setValue(L.index); } catch (eg) { log("  gradient layer " + eg.toString()); }
    k2(eparam(L, "Luma Dissolve", "Transition Completion"), t0, 1, t1, 0, "settle");
}
// Slow Shutter (effects-library recipe): a smeared echo trail behind a sharp copy.
function slowShutter(c, path, t0, t1, srcIn, z0, z1, fxF, fyF) {
    var trail = clipL(c, path, t0, t1, srcIn, z0, z1, fxF, fyF, "settle", { name: "slow shutter trail" });
    eff(trail, "CC Force Motion Blur", "CC Force Motion Blur");
    setE(trail, "CC Force Motion Blur", "Motion Blur Samples", 8); setE(trail, "CC Force Motion Blur", "Override Shutter Settings", 1); setE(trail, "CC Force Motion Blur", "Shutter Angle", 720);
    eff(trail, "ADBE Echo", "Echo");
    var ec = trail.property("ADBE Effect Parade").property("Echo");
    try { ec.property(1).setValue(-4 / FPS); ec.property(2).setValue(5); ec.property(3).setValue(1.0); ec.property(4).setValue(0.75); ec.property(5).setValue(5); } catch (ee) { log("  echo " + ee.toString()); }
    var sharp = clipL(c, path, t0, t1, srcIn, z0, z1, fxF, fyF, "settle", { name: "slow shutter sharp" });
    O(sharp).setValue(62);
    return sharp;
}

// ---------------------------------------------------------------- type (AC caption pairs + Smooth Text Transition)
// Fonts: Didot-Bold ships with macOS only and DM Serif Display is a free Google font: on Windows install both or change
// FONT_N / FONT_I first (a missing font renders as a substitute, a missing glyph renders blank).
var FONT_I = "DMSerifDisplay-Italic", FONT_B = "Arial-Black", FONT_N = "Didot-Bold", CAP = 86;
var SPECKLE = null;
function capFont(kind) { if (kind == "i") return [FONT_I, 1.05, 0]; if (kind == "n") return [FONT_N, 1.12, -10]; return [FONT_B, 0.86, -70]; }
// one comp-wide speckle layer: tiny white specks used as a luma-inverted matte, so every word gets AC's worn print texture
function speckleLayer(c) {
    var s = solidL(c, "SPECKLE (caption texture matte)", [0, 0, 0]);
    eff(s, "ADBE Fractal Noise", "Fractal Noise");
    setE(s, "Fractal Noise", "Contrast", 600); setE(s, "Fractal Noise", "Brightness", -260);
    var sc = findProp(s.property("ADBE Effect Parade").property("Fractal Noise"), "Scale"); if (sc) { try { sc.setValue(6); } catch (e) {} }
    s.enabled = false; SPECKLE = s;
    return s;
}
function styleWord(L, dark) {
    if (dark) { L.setTrackMatte(SPECKLE, TrackMatteType.LUMA_INVERTED); return; }
    eff(L, "ADBE Drop Shadow", "Shadow");
    setE(L, "Shadow", "Opacity", 72); setE(L, "Shadow", "Distance", 0); setE(L, "Shadow", "Softness", 16);
    eff(L, "ADBE Glo2", "Glow"); setE(L, "Glow", "Glow Threshold", 35); setE(L, "Glow", "Glow Radius", 26); setE(L, "Glow", "Glow Intensity", 0.7);
    if (SPECKLE) L.setTrackMatte(SPECKLE, TrackMatteType.LUMA_INVERTED);
}
// capRow: words [[text, kind, scale, tOn], ...] on one baseline, centred (or from x0 when given). Each word arrives with the
// Smooth Text Transition (blur 10 -> 0, opacity 0 -> 100, rise 14 px -> 0, two settle keys over 5 frames) and holds to tOut.
function capRow(c, name, words, tOut, cy, dark, xs) {
    var Ls = [], rs = [], total = 0, gap = CAP * 0.26, i;
    for (i = 0; i < words.length; i++) {
        var f = capFont(words[i][1]), sz = CAP * f[1] * (words[i][2] || 1);
        var L = txt(c, words[i][0], f[0], sz, dark ? [0.06, 0.06, 0.06] : [1, 1, 1], ParagraphJustification.LEFT_JUSTIFY, f[2], 0, 0);
        L.name = name + ": " + words[i][0];
        var r = rect(L);
        Ls.push(L); rs.push(r); total += r.width;
    }
    total += gap * (Ls.length - 1);
    var x = W / 2 - total / 2, yb = H * (cy || 0.468) + CAP * 0.36;
    for (i = 0; i < Ls.length; i++) {
        var px = xs ? xs[i] : x;
        var tOn = words[i][3], anim = (words[i].length < 5 || words[i][4]);
        Ls[i].inPoint = tOn; Ls[i].outPoint = tOut;
        if (anim) {
            k2(P(Ls[i]), tOn, [px - rs[i].left, yb + 14], tOn + fr(5), [px - rs[i].left, yb], "settle");
            k2(O(Ls[i]), tOn, 0, tOn + fr(4), 100, "settle");
            var bl = gaussBlur(Ls[i], 0);
            k2(bl.property("ADBE Gaussian Blur 2-0001"), tOn, 10, tOn + fr(5), 0, "settle");
        } else P(Ls[i]).setValue([px - rs[i].left, yb]);
        styleWord(Ls[i], dark);
        Ls[i].motionBlur = true;
        x += rs[i].width + gap;
    }
    return Ls;
}
// counter: Didot number counting up on a slider (two settle keys) + the italic word after it
function counterRow(c, t0, t1, target, word) {
    var f = capFont("n"), sz = CAP * f[1] * 1.55;
    var probe = txt(c, "40,022,723", f[0], sz, [1, 1, 1], ParagraphJustification.LEFT_JUSTIFY, f[2], 0, 0);
    var rn = rect(probe);
    var fi = capFont("i"), wl = txt(c, word, fi[0], CAP * fi[1], [1, 1, 1], ParagraphJustification.LEFT_JUSTIFY, 0, 0, 0);
    var rw = rect(wl), gap = CAP * 0.26, total = rn.width + gap + rw.width, x = W / 2 - total / 2, yb = H * 0.468 + CAP * 0.36;
    probe.name = "counter"; wl.name = "counter: " + word;
    var ctl = fx(probe, "ADBE Slider Control"); ctl.name = "count";
    k2(probe.property("ADBE Effect Parade").property("count").property(1), t0, 0, t0 + 0.30, target / 1e6, "settle");   // millions: sliders stop at 1e6
    probe.property("Source Text").expression = 'var v = Math.round(effect("count")(1) * 1e6); v.toString().replace(/\\B(?=(\\d{3})+(?!\\d))/g, ",");';
    var Ls = [probe, wl], xs = [x - rn.left, x + rn.width + gap - rw.left];
    for (var i = 0; i < 2; i++) {
        Ls[i].inPoint = t0; Ls[i].outPoint = t1;
        k2(P(Ls[i]), t0, [xs[i], yb + 14], t0 + fr(5), [xs[i], yb], "settle");
        k2(O(Ls[i]), t0, 0, t0 + fr(4), 100, "settle");
        styleWord(Ls[i], false);
    }
}

// ---------------------------------------------------------------- set pieces
// Pixel Reveal (effects-library recipe): the sharp shot shows through a luma matte of hard blocks that sweep from the bright corner of a radial
// ramp (Gradient Ramp + Turbulent Noise + Mosaic + Exposure + Posterize); under it a pixelated copy, so blocks resolve (AC open).
function pixelReveal(c, path, t0, t1, srcIn, z0, z1, fxF, fyF, revealDur) {
    var pc = pre("PIXEL REVEAL", t1 - t0);
    var under = clipL(pc, path, 0, t1 - t0, srcIn, z0, z1, fxF, fyF, "gentle", { name: "pixelated copy" });
    eff(under, "ADBE Mosaic", "Mosaic"); setE(under, "Mosaic", "Horizontal Blocks", 30); setE(under, "Mosaic", "Vertical Blocks", 17);
    var top = clipL(pc, path, 0, t1 - t0, srcIn, z0, z1, fxF, fyF, "gentle", { name: "sharp shot" });
    var m = clipL(pc, path, 0, t1 - t0, srcIn, z0, z1, fxF, fyF, "gentle", { name: "block matte" });
    eff(m, "ADBE Ramp", "Ramp"); setE(m, "Ramp", "Start of Ramp", [0, 0]); setE(m, "Ramp", "Start Color", [0, 0, 0]);
    setE(m, "Ramp", "End of Ramp", [m.width * 1.1, m.height * 1.1]); setE(m, "Ramp", "End Color", [1, 1, 1]); setE(m, "Ramp", "Ramp Shape", 2);
    eff(m, "ADBE AIF Perlin Noise 3D", "Turbulent Noise"); setE(m, "Turbulent Noise", "Blending Mode", 7);
    eff(m, "ADBE Mosaic", "Mosaic"); setE(m, "Mosaic", "Horizontal Blocks", 30); setE(m, "Mosaic", "Vertical Blocks", 17); setE(m, "Mosaic", "Sharp Colors", 0);
    eff(m, "ADBE Exposure2", "Sweep");
    // the posterized matte only changes between about -1.2 and +4.4 stops; the front moves as 2^-E, so ease "accel"
    // (slow start, fast end) to make the blocks clear at an even pace across the whole reveal
    k2(eparam(m, "Sweep", "Exposure"), 0, -1.2, revealDur, 4.4, "accel");
    eff(m, "ADBE Posterize", "Posterize"); setE(m, "Posterize", "Level", 2);
    top.setTrackMatte(m, TrackMatteType.LUMA); m.enabled = false;
    var L = c.layers.add(pc); L.startTime = t0; L.inPoint = t0; L.outPoint = t1; L.name = "Pixel Reveal";
    return L;
}
// AC print on black: a photo print (frozen frame in a white border) over a huge glowing word, eased drift
function printShot(c, t0, t1, path, srcT, bigWord, rot0, rot1, flash, pz, pfx, pfy) {
    pz = pz || 1.05; pfx = (pfx === undefined) ? 0.5 : pfx; pfy = (pfy === undefined) ? 0.5 : pfy;
    var pw = 640, ph = 480, b = Math.round(pw * 0.04), bb = Math.round(pw * 0.16);
    var pr = pre("print photo " + bigWord, 2, pw + 2 * b, ph + b + bb);
    solidL(pr, "paper", [0.96, 0.96, 0.95]);
    var ph1 = pr.layers.add(impF(path));
    try { freeze(ph1, 0, 2, srcT); } catch (et) { log("  freeze " + et.toString()); }
    ph1.inPoint = 0; ph1.outPoint = 2;
    var s = Math.max(pw / ph1.source.width, ph / ph1.source.height) * 100 * pz;
    var fxs = pfx * ph1.source.width, fys = pfy * ph1.source.height;
    A(ph1).setValue([fxs, fys]); S(ph1).setValue([s, s]); P(ph1).setValue([b + pw / 2, b + ph / 2]);
    var mk = ph1.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    mk.property("ADBE Mask Shape").expression = "createPath([fromComp([" + b + "," + b + "]), fromComp([" + (b + pw) + "," + b + "]), fromComp([" + (b + pw) + "," + (b + ph) + "]), fromComp([" + b + "," + (b + ph) + "])], [], [], true);";
    var word = txt(c, bigWord, FONT_N, 520, [1, 1, 1], ParagraphJustification.LEFT_JUSTIFY, -20, -140, 760);
    word.name = "big word " + bigWord; word.inPoint = t0; word.outPoint = t1;
    gaussBlur(word, 7); eff(word, "ADBE Glo2", "Glow"); setE(word, "Glow", "Glow Threshold", 20); setE(word, "Glow", "Glow Radius", 60); setE(word, "Glow", "Glow Intensity", 1.2);
    O(word).setValue(flash ? 100 : 52);
    k2(P(word), t0, [-140, 760], t1, [-170, 760], "gentle");
    var L = c.layers.add(pr); L.startTime = t0; L.inPoint = t0; L.outPoint = t1; L.name = "print " + bigWord;   // startTime: the precomp is 2 s long
    var dur = t1 - t0, w0 = 640 / (pw + 2 * b) * 100;
    k2(S(L), t0, [w0 * 0.96, w0 * 0.96], t1, [w0 * (1 + 0.08 * dur), w0 * (1 + 0.08 * dur)], "settle");
    k2(R(L), t0, rot0, t1, rot1, "settle");
    P(L).setValue([W / 2, H / 2 + 6]);
    shadow(L, 0.7, 14, 50, 135);
    if (flash) { var fl = solidT(c, "overexposed", [1, 1, 1], t0, t1); O(fl).setValue(35); }
    return L;
}
// split screen: two clips, each showing the middle half of its frame in one half of the screen
function splitShot(c, t0, t1, a, b) {
    var pc = pre("SPLIT tea | coffee", t1 - t0);
    // AE applies masks before effects, so the halves are shifted by position (o.dx), never by a Transform effect
    var la = clipL(pc, a[0], 0, t1 - t0, a[1], a[2], a[3], 0.5, 0.5, "gentle", { dx: -W / 4 });
    var lb = clipL(pc, b[0], 0, t1 - t0, b[1], b[2], b[3], 0.5, b[4] || 0.5, "gentle", { dx: W / 4 });
    var Ls = [la, lb];
    for (var i = 0; i < 2; i++) {
        var m = Ls[i].property("ADBE Mask Parade").addProperty("ADBE Mask Atom"); var sh = new Shape();
        var x0 = i == 0 ? 0 : W / 2, x1 = i == 0 ? W / 2 : W;
        sh.vertices = [[x0, 0], [x1, 0], [x1, H], [x0, H]]; sh.closed = true;
        m.property("ADBE Mask Shape").expression = "var s = createPath([fromComp([" + x0 + ",0]), fromComp([" + x1 + ",0]), fromComp([" + x1 + "," + H + "]), fromComp([" + x0 + "," + H + "])], [], [], true); s;";
    }
    var line = solidL(pc, "divider", [0, 0, 0], 6, H); P(line).setValue([W / 2, H / 2]);
    var L = c.layers.add(pc); L.startTime = t0; L.inPoint = t0; L.outPoint = t1; L.name = "split";
    return L;
}
// AC video wall: 3 x 3 tiles, purple tint, one tile blows out, slow push
function wallShot(c, t0, t1, tiles, flashTile, flashAt, tintAmt) {
    var d = t1 - t0, pc = pre("WALL " + Math.round(t0 * 100), d), tw = W / 3, th = H / 3;
    for (var i = 0; i < tiles.length; i++) {
        var r = Math.floor(i / 3), q = i % 3;
        var L = pc.layers.add(impF(tiles[i][0]));
        var s = Math.max(tw / L.source.width, th / L.source.height) * 100;
        S(L).setValue([s, s]); P(L).setValue([q * tw + tw / 2, r * th + th / 2]);
        L.startTime = -tiles[i][1]; L.inPoint = 0; L.outPoint = d;
        var m = L.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
        m.property("ADBE Mask Shape").expression = "createPath([fromComp([" + (q * tw) + "," + (r * th) + "]), fromComp([" + ((q + 1) * tw) + "," + (r * th) + "]), fromComp([" + ((q + 1) * tw) + "," + ((r + 1) * th) + "]), fromComp([" + (q * tw) + "," + ((r + 1) * th) + "])], [], [], true);";
        try { L.audioEnabled = false; } catch (ea) {}
        if (i == flashTile) { var ex = exposure(L, 0); k2(ex.property("Exposure"), flashAt, 0, d, 4.5, "accel"); }
    }
    var tn = adjL(pc, "purple tint"); tint(tn, [0.04, 0.02, 0.10], [0.78, 0.66, 1.0], tintAmt || 45); exposure(tn, -0.24);
    for (var g = 1; g < 3; g++) { var v = solidL(pc, "grid v", [0, 0, 0], 4, H); P(v).setValue([g * tw, H / 2]); var hh = solidL(pc, "grid h", [0, 0, 0], W, 4); P(hh).setValue([W / 2, g * th]); }
    var Lw = c.layers.add(pc); Lw.startTime = t0; Lw.inPoint = t0; Lw.outPoint = t1; Lw.name = "video wall";
    k2(S(Lw), t0, [102, 102], t1, [102 + 8 * d, 102 + 8 * d], "gentle");
    return Lw;
}
// highlighter (AC lime, multiply): one shape per word rect, parented to the still so it rides the camera move; scale X from
// the rect's left edge, two settle keys, staggered
function highlightRects(c, parentL, rects, t0, dur, col) {
    var out = [];
    for (var i = 0; i < rects.length; i++) {
        var r = rects[i], pad = [6, 5];
        var L = c.layers.addShape(); L.name = "highlight " + i;
        var g = L.property("ADBE Root Vectors Group").addProperty("ADBE Vector Group");
        var rr = g.property("ADBE Vectors Group").addProperty("ADBE Vector Shape - Rect");
        rr.property("ADBE Vector Rect Size").setValue([r[2] + 2 * pad[0], r[3] + 2 * pad[1]]);
        rr.property("ADBE Vector Rect Position").setValue([(r[2] + 2 * pad[0]) / 2, (r[3] + 2 * pad[1]) / 2]);
        var fl = L.property("ADBE Root Vectors Group").property(1).property("ADBE Vectors Group").addProperty("ADBE Vector Graphic - Fill");
        fl.property("ADBE Vector Fill Color").setValue(col || [0.74, 0.86, 0.16]);
        L.parent = parentL;
        A(L).setValue([0, 0]); P(L).setValue([r[0] - pad[0], r[1] - pad[1]]);
        var ts = t0 + i * dur * 0.85;
        k2(S(L), ts, [0, 100], ts + dur, [100, 100], "settle");
        L.blendingMode = BlendingMode.MULTIPLY;
        L.inPoint = parentL.inPoint; L.outPoint = parentL.outPoint;
        out.push(L);
    }
    return out;
}
// Shake Chroma (stand-in for the effects-library recipe): three channel copies of the layer that snap together on the hit, plus a decaying shake
function shakeChroma(c, L, tHit, frames) {
    var t1 = tHit + fr(frames || 9), offs = [[16, 0], [0, 0], [-16, 0]], ch = [[1, 0, 0], [0, 1, 0], [0, 0, 1]];
    var copies = [L, L.duplicate(), L.duplicate()];
    for (var i = 0; i < 3; i++) {
        var X = copies[i];
        chanOnly(X, i, "Channel " + i);
        if (i > 0) X.blendingMode = BlendingMode.ADD;
        eff(X, "ADBE Geometry2", "Chroma offset");
        k2(eparam(X, "Chroma offset", "Position"), tHit, [X.width / 2 + offs[i][0] * 100 / S(X).value[0], X.height / 2], t1, [X.width / 2, X.height / 2], "settle");
    }
    var a = adjL(c, "shake"); a.inPoint = tHit; a.outPoint = t1;
    eff(a, "ADBE Tile", "Motion Tile"); setE(a, "Motion Tile", "Output Width", 130); setE(a, "Motion Tile", "Output Height", 130); setE(a, "Motion Tile", "Mirror Edges", 1);
    eff(a, "ADBE Slider Control", "amp");
    k2(a.property("ADBE Effect Parade").property("amp").property(1), tHit, 30, t1, 0, "settle");
    eff(a, "ADBE Geometry2", "Shake");
    eparam(a, "Shake", "Position").expression = 'var amp = effect("amp")(1); [' + (W / 2) + ' + amp * noise(time * 8.8), ' + (H / 2) + ' + amp * noise(time * 8.8 + 7)];';
    return copies;
}
// One-Frame Glitch Transition (effects-library recipe) into the drop: M is the cut frame. M-2/M-1 white, M = incoming zoom-blurred with a dark
// lens edge, M+1/M+2 = hard vertical split (left: incoming frozen, RGB-inverted, smeared), then the clean shot settles.
function glitchBurst(c, inPath, inSrcT, cutF, fxF, fyF) {
    var tM = fr(cutF);
    solidT(c, "glitch white", [1, 1, 1], fr(cutF - 2), tM);
    var zb = clipL(c, inPath, tM, fr(cutF + 1), inSrcT, 1.6, 1.6, fxF, fyF, "gentle", { name: "glitch: zoom blur" });
    eff(zb, "ADBE Radial Blur", "Zoom"); setE(zb, "Zoom", "Amount", 60); setE(zb, "Zoom", "Type", 2);
    vignetteOn(c, tM, fr(cutF + 1), 85);
    var sR = clipL(c, inPath, fr(cutF + 1), fr(cutF + 3), inSrcT + 1 / FPS, 1.35, 1.35, fxF, fyF, "gentle", { name: "glitch: split right" });
    var sL = clipL(c, inPath, fr(cutF + 1), fr(cutF + 3), inSrcT + 1 / FPS, 1.35, 1.35, fxF, fyF, "gentle", { name: "glitch: split left" });
    eff(sL, "ADBE Invert", "Invert"); eff(sL, "ADBE Motion Blur", "Smear"); setE(sL, "Smear", "Direction", 90); setE(sL, "Smear", "Blur Length", 160);
    var m = sL.property("ADBE Mask Parade").addProperty("ADBE Mask Atom");
    m.property("ADBE Mask Shape").expression = "createPath([fromComp([0,0]), fromComp([" + Math.round(W * 0.486) + ",0]), fromComp([" + Math.round(W * 0.486 + 30) + "," + H + "]), fromComp([0," + H + "])], [], [], true);";
}
function vignetteOn(c, t0, t1, op) { var v = vignette(c, op); v.inPoint = t0; v.outPoint = t1; return v; }
// TV switch-off: the picture squashes to a bright line (accel), the line shrinks to a dot (accel), the dot fades
// TV switch-off (old CRT collapse) as three two-key moves on separate properties, so one dimension never drags
// the other: the picture collapses to a bright line through the screen centre (layer Scale Y, settle), the line
// shrinks to a dot (Transform effect Scale Width, settle), the dot fades. It starts at the TV shot's end framing
// (anchor = screen centre at frame centre, scale s0) so there is no jump at the cut.
function tvOff(c, setComp, freezeT, t0, f1, f2, f3, anchor, s0) {
    var L = c.layers.add(setComp); L.name = "TV switch-off";
    L.startTime = t0 - freezeT;
    try { freeze(L, t0, t0 + 1, freezeT); } catch (e) { log("  tv freeze " + e.toString()); }
    L.inPoint = t0; L.outPoint = fr(f2);
    var t1 = fr(f1), t2 = fr(f2);
    A(L).setValue(anchor); P(L).setValue([W / 2, H / 2]);
    k2(S(L), t0, [s0, s0], t1, [s0, 1.2], "settle");
    eff(L, "ADBE Geometry2", "Collapse width");
    setE(L, "Collapse width", "Anchor Point", anchor); setE(L, "Collapse width", "Position", anchor); setE(L, "Collapse width", "Uniform Scale", 0);
    k2(eparam(L, "Collapse width", "Scale Width"), t1, 100, t2, 2, "settle");
    eff(L, "ADBE Exposure2", "Collapse glow"); k2(eparam(L, "Collapse glow", "Exposure"), t0, 0, t1, 3.0, "settle");
    L.motionBlur = true;
    var dot = softEllipse(c, "TV dot", 26, 26, [1, 1, 1], W / 2, H / 2, 10, 100); dot.inPoint = t2; dot.outPoint = fr(f3);
    k2(O(dot), t2, 100, fr(f3), 0, "accel");
    return L;
}

// ---------------------------------------------------------------- from the first reel's second library
// hold a footage or comp layer on one source frame between comp times tA and tB (keeps exactly two remap keys)
function freeze(L, tA, tB, srcT) {
    L.timeRemapEnabled = true;
    var trm = L.property("ADBE Time Remapping");
    trm.setValueAtTime(tA, srcT); trm.setValueAtTime(tB, srcT);
    for (var k = trm.numKeys; k >= 1; k--) { var kt = trm.keyTime(k); if (Math.abs(kt - tA) > 1e-4 && Math.abs(kt - tB) > 1e-4) trm.removeKey(k); }
}
function chanOnly(L, i, label) {   // keep one colour channel: Levels (Individual Controls) with the other two outputs at 0
    eff(L, "ADBE Pro Levels2", label);
    var names = ["Red", "Green", "Blue"];
    for (var k = 0; k < 3; k++) if (k != i) setE(L, label, names[k] + " Output White", 0);
}
function rectMatte(c, name, x0, y0, x1, y1) {
    var s = solidL(c, name, [1, 1, 1], Math.round(x1 - x0), Math.round(y1 - y0)); P(s).setValue([(x0 + x1) / 2, (y0 + y1) / 2]); s.enabled = false; return s;
}

// face-matched montage: items = [[path, srcT, faceCx, faceCy, faceW, grade]]; every face lands at (tx, ty) at the same
// size; one null pushes the whole run in (two settle keys), so the montage reads as one stutter on one person.
function faceMontage(c, t0F, t1F, items, framesEach, tx, ty, faceW) {
    var t0 = fr(t0F), t1 = fr(t1F);
    var nl = c.layers.addNull(t1 - t0 + 1); nl.name = "MONTAGE push"; nl.startTime = t0; nl.inPoint = t0; nl.outPoint = t1;
    A(nl).setValue([50, 50]); P(nl).setValue([tx, ty]);
    var n = Math.floor((t1F - t0F) / framesEach), Ls = [];
    for (var i = 0; i < n; i++) {
        var it = items[i % items.length];
        var L = c.layers.add(impF(it[0])); L.name = "face " + (i + 1);
        var a = fr(t0F + i * framesEach), b = (i == n - 1) ? t1 : fr(t0F + (i + 1) * framesEach);
        L.startTime = a - it[1] - fr(i % 3); L.inPoint = a; L.outPoint = b;
        A(L).setValue([it[2], it[3]]); var s = faceW / it[4] * 100; S(L).setValue([s, s]); P(L).setValue([tx, ty]);
        try { L.audioEnabled = false; } catch (ea) {}
        if (it[5]) grade(L, it[5]);
        L.parent = nl;
        Ls.push(L);
    }
    k2(S(nl), t0, [100, 100], t1, [109, 109], "settle");
    return Ls;
}

// Attention Compound finish. acGrade: grade + bloom inside the content comp (captions included). The numbers match the
// storyboard renderer: black 0.05, gamma 1.08, contrast 1.18, saturation -18; bloom = highlights above 0.66, Gaussian
// Blurriness 60 (sigma = 0.466 x Blurriness), Screen at 55%. Glow in Add mode blew 40% of a frame to white instead.
function acGrade(c) {
    var g = adjL(c, "AC grade (crushed blacks, punch, less saturation)");
    eff(g, "ADBE Pro Levels2", "Black and gamma"); setE(g, "Black and gamma", "Input Black", 0.05); setE(g, "Black and gamma", "Gamma", 1 / 1.08);
    eff(g, "ADBE Pro Levels2", "Contrast"); setE(g, "Contrast", "Input Black", 0.5 - 0.5 / 1.18); setE(g, "Contrast", "Input White", 0.5 + 0.5 / 1.18);
    eff(g, "ADBE HUE SATURATION", "Saturation"); var ms = findProp(g.property("ADBE Effect Parade").property("Saturation"), "Master Saturation"); if (ms) { try { ms.setValue(-18); } catch (e) { log("  sat " + e.toString()); } }
    var bl = adjL(c, "AC bloom (highlights above 66%, screened)");
    eff(bl, "ADBE Pro Levels2", "Highlights only"); setE(bl, "Highlights only", "Input Black", 0.66);
    eff(bl, "ADBE Gaussian Blur 2", "Bloom blur"); setE(bl, "Bloom blur", "Blurriness", 60); setE(bl, "Bloom blur", "Repeat Edge Pixels", 1);
    bl.blendingMode = BlendingMode.SCREEN; O(bl).setValue(55);
    return g;
}
// acFinish: the render comp: opaque black base, red/cyan fringe (three channel copies scaled apart), the tube vignette PNG
// multiplied (global VIGNETTE), a light soften and mono grain.
function acFinish(content, name) {
    var f = newComp(name, content.duration);
    // opaque black base: the content comp is transparent where no shot covers it (print shots), and the multiplied
    // vignette would show its own white there
    var base = solidL(f, "black base", [0, 0, 0]); base.name = "black base";
    var sc = [100.4, 100, 99.6];   // reelkit chroma(0.004): red scaled up, blue down
    for (var i = 0; i < 3; i++) {
        var L = f.layers.add(content); L.name = ["red", "green", "blue"][i] + " (fringe)";
        chanOnly(L, i, "channel " + i);
        if (i > 0) L.blendingMode = BlendingMode.ADD;
        S(L).setValue([sc[i], sc[i]]);
    }
    // reelkit vignette_crt(corner 0.42, power 3, round_corner 0.05), baked to a PNG (assets/ae/vignette_ac.png) and multiplied
    var vg = f.layers.add(impF(VIGNETTE)); vg.name = "CRT vignette + tube corners"; vg.blendingMode = BlendingMode.MULTIPLY;
    vg.inPoint = 0; vg.outPoint = f.duration;
    var soft = adjL(f, "soften"); eff(soft, "ADBE Gaussian Blur 2", "Soften"); setE(soft, "Soften", "Blurriness", 1.3); setE(soft, "Soften", "Repeat Edge Pixels", 1);
    var gr = adjL(f, "grain"); eff(gr, "ADBE Noise", "Grain"); setE(gr, "Grain", "Amount of Noise", 5); setE(gr, "Grain", "ADBE Noise-0002", 0);   // "Noise Type: Use Color Noise" off = mono grain
    return f;
}
