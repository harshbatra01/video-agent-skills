// effects_lib.jsx: shared helpers for the effects library builds (on top of ae_lib.jsx).
// Globals provided by effects_build.py: W, H, FPS, HERE, STOCK (absolute stock folder path ending in "/"), ROOTF (root folder),
// EFFECT_FOLDER (the project folder of the effect being built, set before each build_<key>() call).
// ES3 only (no let/const/arrow/JSON/Array.indexOf/map/forEach).

var FOLDERS = {};
function folder(name, parent) {
    var key = (parent ? parent.id : "root") + "/" + name;
    if (FOLDERS[key]) return FOLDERS[key];
    var f = app.project.items.addFolder(name);
    if (parent) f.parentFolder = parent;
    FOLDERS[key] = f; return f;
}
var STOCKF = null;
// Import a stock file by name (e.g. "jogger.mov", "blossom_photo.png"); cached, filed under "_Stock footage".
function stock(name) {
    var it = imp(STOCK + name);
    try {
        if (!STOCKF) STOCKF = folder("_Stock footage (Pexels, free licence)", ROOTF);
        it.parentFolder = STOCKF;
    } catch (e) { log("  stock folder " + e.toString()); }
    return it;
}
// A comp filed inside the current effect's folder.
function effectComp(name, dur, w, h) {
    var c = newComp(name, dur, w, h);
    if (EFFECT_FOLDER) c.parentFolder = EFFECT_FOLDER;
    return c;
}
// SOURCE precomp: one stock file covering the frame. Users swap the footage inside it (Alt-drag replace) to reuse the effect.
// opts: {start: source seconds to start from, crop: [x0,y0,x1,y1], w, h}
function sourceComp(name, file, dur, opts) {
    opts = opts || {};
    var c = effectComp(name, dur, opts.w, opts.h);
    var L = c.layers.add(stock(file));
    cover(L, opts.crop || null, c.width, c.height);
    if (opts.start) L.startTime = -opts.start;
    L.inPoint = 0; L.outPoint = dur;
    try { L.audioEnabled = false; } catch (e) {}
    c.comment = "SOURCE: swap the footage in this comp to reuse the effect on your own shot.";
    return c;
}
// Add a comp as a layer (precomp) in another comp, full duration.
function addComp(parentComp, child, name) { var L = parentComp.layers.add(child); if (name) L.name = name; L.startTime = 0; return L; }
// Expression slider / checkbox controls on a layer (usually a null or adjustment layer named "CONTROLS").
function slider(l, name, v) { var e = fx(l, "ADBE Slider Control"); e.name = name; e.property(1).setValue(v); return l.property("ADBE Effect Parade").property(name); }
function checkbox(l, name, v) { var e = fx(l, "ADBE Checkbox Control"); e.name = name; e.property(1).setValue(v ? 1 : 0); return l.property("ADBE Effect Parade").property(name); }
function colorCtl(l, name, v) { var e = fx(l, "ADBE Color Control"); e.name = name; e.property(1).setValue(v); return l.property("ADBE Effect Parade").property(name); }
function controls(comp) { var n = comp.layers.addNull(comp.duration); n.name = "CONTROLS"; n.enabled = true; P(n).setValue([80, 80]); return n; }
// Effect by match name with a list of [param matchName or display name, value] pairs. Re-fetches the effect after adding.
function fxp(l, mn, pairs, label) {
    var e = fx(l, mn);
    if (label) { try { e.name = label; } catch (en) {} }
    var nm = e.name;
    if (pairs) for (var i = 0; i < pairs.length; i++) {
        var ep = l.property("ADBE Effect Parade").property(nm);
        var p = null;
        try { p = ep.property(pairs[i][0]); } catch (e1) { p = null; }
        if (!p) p = findProp(ep, pairs[i][0]);
        if (!p) { log("  fxp " + mn + " no param " + pairs[i][0]); continue; }
        try { p.setValue(pairs[i][1]); } catch (e2) { log("  fxp " + mn + " " + pairs[i][0] + ": " + e2.toString()); }
    }
    return l.property("ADBE Effect Parade").property(nm);
}
// Keys with explicit frame numbers at the comp frame rate: kf(prop, [[frame, value, inInf?, outInf?], ...])
function kf(prop, list) {
    var t = [];
    for (var i = 0; i < list.length; i++) t.push([list[i][0] / FPS, list[i][1], list[i][2], list[i][3]]);
    keys(prop, t);
}
// Hex colour "#RRGGBB" to AE [r,g,b] 0-1.
function hex(h) { h = h.replace("#", ""); return [parseInt(h.substr(0, 2), 16) / 255, parseInt(h.substr(2, 2), 16) / 255, parseInt(h.substr(4, 2), 16) / 255]; }
// Write a short "how it works" note on a comp (shows in the Project panel Comment column).
function note(comp, s) { try { comp.comment = s; } catch (e) {} }

// Fonts by role. The builds were made with SF Pro Display (Apple) and Inter; Georgia Bold for the dither wordmark.
// effects_build.py can override any role with FONT_OVERRIDES (env FX_FONTS, JSON), e.g. on a machine without SF Pro:
//   FX_FONTS={"regular": "Inter-Regular", "medium": "Inter-Medium", "bold": "Inter-Bold"}
// A missing FONT renders in a substitute face (layouts measured with sourceRectAtTime adapt); a missing GLYPH renders blank.
var FONTS = { regular: "SFProDisplay-Regular", medium: "SFProDisplay-Medium", bold: "SFProDisplay-Bold", serifBold: "Georgia-Bold",
              uiRegular: "Inter-Regular", uiMedium: "Inter-Medium", uiSemiBold: "Inter-SemiBold", uiLight: "Inter-Light", uiBold: "Inter-Bold" };
if (typeof FONT_OVERRIDES == "object" && FONT_OVERRIDES) { for (var fontRole in FONT_OVERRIDES) FONTS[fontRole] = FONT_OVERRIDES[fontRole]; }
