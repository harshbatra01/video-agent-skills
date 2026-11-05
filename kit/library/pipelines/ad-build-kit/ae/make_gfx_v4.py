"""gfx_v4.jsx: v9 review fixes, rendered to Motion graphics\\gfx_v4
  - hr_window: same animation, moved off her face into the caption zone (kicker at KICK_Y, number at MAIN_Y,
    bottom backdrop like the captions)
  - cta_end: one reusable CTA end card (for the ads that end without a code card), synced to the CTA voice.
usage: python make_gfx_v4.py [name,name,...]"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import make_gfx_v2 as M

OUT = "C:/VISION/IMMUFIX/repair/ENCODED RUSHES/Motion graphics/gfx_v4/"
CTA = json.load(open(os.path.join(HERE, 'cta_spec.json'))) if os.path.exists(os.path.join(HERE, 'cta_spec.json')) else None

WINDOW_LOW = r'''
// hr_window, lower: same timing as v2, laid out like the captions so it sits under her face
function windowGfx(sp) {
    var c = newComp(sp.name, sp.dur);
    backdrop(c, 980, H + 80, 420, 74, 0);
    var k = txt(c, "VULNERABLE FOR", KICK, 52, RED, ParagraphJustification.CENTER_JUSTIFY, 160, 540, KICK_Y);
    shadow(k, 0.55, 3, 14); keys(O(k), [[sp.tK, 0], [sp.tK + 0.16, 100]]); keys(P(k), [[sp.tK, [540, KICK_Y + 26]], [sp.tK + 0.22, [540, KICK_Y], 70, 33]]);
    var NY = MAIN_Y - 10;
    var n = txt(c, "20–30", BIG, 270, WHITE, ParagraphJustification.CENTER_JUSTIFY, 6, 540, NY);
    var r = rect(n); A(n).setValue([r.left + r.width / 2, r.top + r.height / 2]); P(n).setValue([540 + r.left + r.width / 2, NY + r.top + r.height / 2]);
    n.property("Source Text").expression = "time < " + sp.t30 + " ? String(Math.round(ease(time, " + sp.a + ", " + sp.b + ", 0, 20))) : '20–30';";
    gradText(n, WHITE, GREY); shadow(n, 0.55, 5, 24); glow(n, 60, 20, 0.3);
    keys(O(n), [[sp.a - 0.02, 0], [sp.a + 0.06, 100]]);
    keys(S(n), [[sp.a, [92, 92]], [sp.a + 0.2, [100, 100]], [sp.t30 - 0.01, [100, 100]], [sp.t30 + 0.07, [110, 110]], [sp.t30 + 0.26, [100, 100]]]);
    var u = txt(c, "MINUTES", KICK, 52, WHITE, ParagraphJustification.CENTER_JUSTIFY, 180, 540, NY + 118);
    shadow(u, 0.55, 3, 14); keys(O(u), [[sp.tU, 0], [sp.tU + 0.16, 100]]); keys(P(u), [[sp.tU, [540, NY + 142]], [sp.tU + 0.22, [540, NY + 118], 70, 33]]);
    return c;
}
'''

CTA_JSX = r'''
// one reusable CTA end card: soft bottom backdrop, kicker words, the code as the hero word in a gold-edged glass pill,
// "20% OFF" counting up, small line at the bottom. Times come from the CTA voice (sp.*).
function ctaEnd(sp) {
    var c = newComp(sp.name, sp.dur);
    c.motionBlur = true;
    backdrop(c, 860, H + 80, 460, 78, 0);
    var els = [];
    // 1) kickers: "HEAD OVER TO IMMUFIX", then "USE THIS DISCOUNT CODE" in the same place
    var ka = txt(c, sp.kickA, KICK, 54, WHITE, ParagraphJustification.CENTER_JUSTIFY, 160, 540, 1060);
    shadow(ka, 0.6, 3, 16); keys(O(ka), [[sp.tKA, 0], [sp.tKA + 0.14, 100], [sp.tKAout, 100], [sp.tKAout + 0.12, 0]]);
    keys(P(ka), [[sp.tKA, [540, 1088]], [sp.tKA + 0.24, [540, 1060], 70, 33], [sp.tKAout, [540, 1060]], [sp.tKAout + 0.12, [540, 1040]]]);
    var kb = txt(c, sp.kickB, KICK, 54, WHITE, ParagraphJustification.CENTER_JUSTIFY, 160, 540, 1060);
    shadow(kb, 0.6, 3, 16); keys(O(kb), [[sp.tKB, 0], [sp.tKB + 0.14, 100]]); keys(P(kb), [[sp.tKB, [540, 1088]], [sp.tKB + 0.24, [540, 1060], 70, 33]]);
    // 2) the code: glass pill + big word
    var PW = 920, PH = 230, PY = 1215;
    var pill = rrShape(c, "code pill", PW, PH, PH / 2, [0.04, 0.05, 0.07], 72, [0.81, 0.68, 0.39], 3, 100, 540 - PW / 2, PY - PH / 2);
    A(pill).setValue([PW / 2, PH / 2]); P(pill).setValue([540, PY]);
    keys(O(pill), [[sp.tCode - 0.06, 0], [sp.tCode + 0.08, 100]]);
    keys(S(pill), [[sp.tCode - 0.06, [86, 86]], [sp.tCode + 0.22, [100, 100], 80, 20]]);
    var w = bigWord(c, sp.code, sp.tCode, PY + 82, 860, 190, null);
    keys(S(w.main), [[sp.tCode, [124, 124]], [sp.tCode + 0.24, [100, 100], 80, 20], [sp.dur, [103, 103]]]);
    keys(O(w.main), [[sp.tCode, 0], [sp.tCode + 0.06, 100]]);
    // shine sweep across the code
    var sh = solid(c, "shine", [1, 1, 1]); sh.blendingMode = BlendingMode.ADD;
    var sm = new Shape(); sm.vertices = [[-60, PY - PH / 2], [0, PY - PH / 2], [-120, PY + PH / 2], [-180, PY + PH / 2]]; sm.closed = true;
    var mk = sh.Masks.addProperty("Mask"); mk.property("maskShape").setValue(sm); mk.property("maskFeather").setValue([30, 30]);
    keys(O(sh), [[sp.tShine, 0], [sp.tShine + 0.05, 20], [sp.tShine + 0.5, 20], [sp.tShine + 0.55, 0]]);
    keys(P(sh), [[sp.tShine, [540, 960]], [sp.tShine + 0.55, [540 + 1200, 960]]]);
    // 3) "20% OFF" counting
    var n = txt(c, "20% OFF", BIG, 210, WHITE, ParagraphJustification.CENTER_JUSTIFY, 6, 540, 1560);
    n.property("Source Text").expression = "time < " + sp.tOffEnd + " ? String(Math.round(ease(time, " + sp.tOff + ", " + sp.tOffEnd + ", 0, 20))) + '% OFF' : '20% OFF';";
    gradText(n, [1, 0.93, 0.71], [0.81, 0.68, 0.39]); shadow(n, 0.55, 5, 24); glow(n, 55, 18, 0.28);
    keys(O(n), [[sp.tOff - 0.02, 0], [sp.tOff + 0.06, 100]]);
    keys(S(n), [[sp.tOff, [92, 92]], [sp.tOff + 0.2, [100, 100]], [sp.tOffEnd, [100, 100]], [sp.tOffEnd + 0.07, [108, 108]], [sp.tOffEnd + 0.26, [100, 100]]]);
    var fl = solid(c, "flash", [1, 1, 1]); keys(O(fl), [[sp.tCode, 0], [sp.tCode + 0.033, 18], [sp.tCode + 0.15, 0]]);
    return c;
}
'''

if __name__ == '__main__':
    only = sys.argv[1].split(',') if len(sys.argv) > 1 else []
    specs = [[k, d] for k, d, s, e in M.build_specs() if d['name'] == 'hr_window']
    if CTA: specs.append(['cta', CTA])
    hdr = '''// Immufix motion graphics v4 (generated by make_gfx_v4.py). Run: AfterFX.exe -r gfx_v4.jsx
app.beginSuppressDialogs();
var OUT = "%s";
var IN = "%s";
var ONLY = %s;
var W = 1080, H = 1920, FPS = 60;
var WHITE = [1, 1, 1], RED = [1, 0.231, 0.188], GREEN = [0.204, 0.820, 0.482], YELLOW = [1, 0.79, 0.235], INK = [0.08, 0.08, 0.09];
var GREY = [0.77, 0.79, 0.82], HL = [1, 0.81, 0.23];
var BIG = "Coolvetica-HeavyComp", KICK = "ProximaNova-Extrabld", SEMI = "ProximaNova-Semibold", REG = "ProximaNova-Regular";
var SERIFB = "Georgia-Bold", SERIFI = "Georgia-Italic";
var MAIN_Y = 1590, KICK_Y = 1370;
var LOG = [];
function log(s) { LOG.push(s); }
function writeFile(path, s) { var f = new File(path); f.encoding = "UTF-8"; f.open("w"); f.write(s); f.close(); }
''' % (OUT, M.IN, json.dumps(only))
    helpers = open(os.path.join(HERE, 'gfx_helpers_v1.jsx'), encoding='utf-8').read()
    body = open(os.path.join(HERE, 'gfx_v3_body.jsx'), encoding='utf-8').read()
    run = '''
var SPECS = %s;
try {
    var proj = app.newProject();
    var f = new Folder(OUT); if (!f.exists) f.create();
    var outs = [];
    for (var j = 0; j < SPECS.length; j++) {
        var kind = SPECS[j][0], sp = SPECS[j][1], c = null;
        var want = !ONLY.length; for (var q = 0; q < ONLY.length; q++) if (ONLY[q] == sp.name) want = true;
        if (!want) continue;
        try {
            if (kind == "window") c = windowGfx(sp);
            else if (kind == "cta") c = ctaEnd(sp);
            outs.push([sp.name, c]); log("built " + sp.name);
        } catch (e) { log("FAILED " + sp.name + ": " + e.toString() + " line " + e.line); }
        writeFile(OUT + "gfx_v4_log.txt", LOG.join("\\n"));
    }
    proj.save(new File(OUT + "immufix_gfx_v4.aep"));
    for (var o = 0; o < outs.length; o++) {
        var rq = proj.renderQueue.items.add(outs[o][1]);
        rq.outputModule(1).applyTemplate("High Quality with Alpha");
        rq.outputModule(1).file = new File(OUT + outs[o][0]);
        log("render " + outs[o][0]); writeFile(OUT + "gfx_v4_log.txt", LOG.join("\\n"));
        proj.renderQueue.render();
        rq.remove();
    }
    proj.save();
    LOG.push("render done");
} catch (err) { LOG.push("FATAL " + err.toString() + " line " + err.line); }
writeFile(OUT + "gfx_v4_log.txt", LOG.join("\\n"));
writeFile(OUT + "gfx_v4_DONE.txt", "done");
''' % json.dumps(specs)
    open(os.path.join(HERE, 'gfx_v4.jsx'), 'w', encoding='utf-8').write(hdr + helpers + '\n' + body + '\n' + WINDOW_LOW + CTA_JSX + run)
    print('wrote gfx_v4.jsx:', [s[1]['name'] for s in specs])
