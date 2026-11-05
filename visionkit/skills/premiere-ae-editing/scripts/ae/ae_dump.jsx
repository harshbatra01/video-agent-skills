// ae_dump.jsx TEMPLATE (filled in by ae_dump.py): read-only dump of AE projects (comps, layers, effects, keyframes, expressions, text).
// Opens COPIES of the .aep files and closes them without saving.
app.beginSuppressDialogs();
var HERE = __HERE__; var STEM = __STEM__;
var FILES = __FILES__;
var OUT = __OUT__;
// macOS (from the Mac port, Oct 2026): ae_run.py there runs this inside the AE that is already open, so refuse when it
// holds a project, never quit AE, and write Unix line feeds (ExtendScript writes \r on the Mac). Windows is unchanged.
var MAC = (File.fs == "Macintosh");
// ae_run.py takes <stem>_log.txt as proof that the script started (on Windows it gives up after 150 s without it and
// then kills AE, which cut off long dumps): write it first.
(function () { var lf = new File(HERE + STEM + "_log.txt"); lf.encoding = "UTF-8"; if (MAC) lf.lineFeed = "Unix"; lf.open("w"); lf.write("START " + app.version); lf.close(); })();
var L = [];
function w(s) { L.push(s); }
function save() { var f = new File(OUT); f.encoding = "UTF-8"; if (MAC) f.lineFeed = "Unix"; f.open("w"); f.write(L.join("\n")); f.close(); }
function r2(x) { return Math.round(x * 100) / 100; }
function sv(o, k) { try { var v = o[k]; if (typeof v == "number") return r2(v); return v; } catch (e) { return "ERR(" + k + ")"; } }
function fmtv(v) {
    try {
        if (v instanceof Array) {
            var a = [];
            for (var i = 0; i < v.length; i++) a.push(r2(v[i]));
            return "(" + a.join(",") + ")";
        }
        if (typeof v == "number") return String(r2(v));
        if (typeof v == "boolean") return String(v);
        return "obj";
    } catch (e) { return "?"; }
}
function kf(p) {
    if (!p) return "";
    var s = "";
    try {
        if (p.numKeys > 0) {
            s += p.numKeys + "kf[";
            var n = Math.min(p.numKeys, 6);
            for (var k = 1; k <= n; k++) {
                s += r2(p.keyTime(k)) + "s=" + fmtv(p.keyValue(k));
                if (k < n) s += " ";
            }
            if (p.numKeys > 6) s += " ...";
            s += "]";
        }
    } catch (e) { s += "(kf err)"; }
    try {
        if (p.expressionEnabled && p.expression) s += " EXPR{" + p.expression.replace(/\s+/g, " ").substring(0, 160) + "}";
    } catch (e2) {}
    return s;
}
function walkProps(grp, depth, out) {
    for (var i = 1; i <= grp.numProperties; i++) {
        var p = grp.property(i);
        if (!p) continue;
        if (p.propertyType == PropertyType.PROPERTY) {
            var k = kf(p);
            if (k) out.push(new Array(depth + 1).join("  ") + p.name + ": " + k);
        } else if (depth < 6) {
            var sub = [];
            walkProps(p, depth + 1, sub);
            if (sub.length) { out.push(new Array(depth + 1).join("  ") + "[" + p.name + " / " + p.matchName + "]"); for (var j = 0; j < sub.length; j++) out.push(sub[j]); }
        }
    }
}
if (MAC && app.project && (app.project.file !== null || app.project.dirty || app.project.numItems > 0)) {
    w("REFUSED: AE already has a project open (" + (app.project.file ? app.project.file.fsName : "untitled") + "); close it first");
    FILES = [];
}
for (var fi = 0; fi < FILES.length; fi++) {
    try {
        var proj = app.open(new File(FILES[fi]));
        w("################ " + FILES[fi] + "  items=" + app.project.numItems);
        for (var i = 1; i <= app.project.numItems; i++) {
            var it = app.project.item(i);
            if (it instanceof FootageItem) {
                var src = "";
                try { src = it.file ? it.file.fsName : (it.mainSource instanceof SolidSource ? "SOLID " + it.mainSource.color : ""); } catch (e) {}
                w("FOOTAGE " + it.name + " | " + it.width + "x" + it.height + " | " + src + (it.footageMissing ? " (MISSING)" : ""));
            }
        }
        for (var i = 1; i <= app.project.numItems; i++) {
            var c = app.project.item(i);
            if (!(c instanceof CompItem)) continue;
            w("");
            var keys = ["name", "width", "height", "duration", "frameRate", "numLayers"];
            var cl = "COMP";
            // never read c.bgColor: it throws "invalid numeric result" in AE 2026
            for (var kk = 0; kk < keys.length; kk++) { var got = "ERR"; try { got = c[keys[kk]]; } catch (e) { got = "ERR " + e.toString(); } cl += " " + keys[kk] + "=" + got; }
            w(cl);
            for (var j = 1; j <= c.numLayers; j++) {
                var ly = c.layer(j);
                // layer.matchName is reliable here; instanceof ShapeLayer was not (a shape layer came out as LIGHT)
                var lmn = ""; try { lmn = ly.matchName; } catch (e) {}
                var type = { "ADBE Text Layer": "TEXT", "ADBE Vector Layer": "SHAPE", "ADBE Camera Layer": "CAMERA", "ADBE Light Layer": "LIGHT" }[lmn] || "";
                if (!type && ly.source) type = (ly.source instanceof CompItem) ? "PRECOMP:" + ly.source.name : (ly.nullLayer ? "NULL" : "AV:" + ly.source.name);
                var line = "  L" + j + " " + type + " '" + sv(ly, "name") + "' in " + sv(ly, "inPoint") + " out " + sv(ly, "outPoint") + " stretch " + sv(ly, "stretch") +
                    " 3D=" + sv(ly, "threeDLayer") + " enabled=" + sv(ly, "enabled") + " blend=" + sv(ly, "blendingMode") + " matte=" + sv(ly, "trackMatteType");
                try { if (ly.parent) line += " parent=" + ly.parent.name; } catch (e) {}
                w(line);
                if (type == "TEXT") {
                    try {
                        var td = ly.property("ADBE Text Properties").property("ADBE Text Document").value;
                        w("     text: \"" + td.text.replace(/\r/g, " / ") + "\" font=" + td.font + " size=" + td.fontSize + " fill=" + td.fillColor + (td.applyStroke ? " stroke" : ""));
                    } catch (e) {}
                }
                var out = [];
                walkProps(ly, 2, out);
                for (var q = 0; q < Math.min(out.length, 40); q++) w(out[q]);
                if (out.length > 40) w("      ... " + (out.length - 40) + " more");
                var fx = ly.property("ADBE Effect Parade");
                if (fx && fx.numProperties) {
                    var names = [];
                    for (var e = 1; e <= fx.numProperties; e++) names.push(fx.property(e).name + "<" + fx.property(e).matchName + ">");
                    w("     effects: " + names.join(", "));
                }
            }
        }
        app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES);
    } catch (err) { w("ERROR " + FILES[fi] + ": " + err.toString() + " line " + err.line); }
    save();
}
w("DONE");
save();
if (MAC) { try { app.endSuppressDialogs(false); } catch (ed) {} }
var d = new File(HERE + STEM + "_DONE.txt"); d.open("w"); d.write("done"); d.close();
if (!MAC) app.quit();
