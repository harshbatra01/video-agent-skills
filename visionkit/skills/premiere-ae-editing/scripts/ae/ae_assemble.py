"""Assemble a review preview (picture + voice + music + SFX) in After Effects and render one H.264 .mp4 with audio.
Use it when the cut lives as an edit list (generated shots + audio) and the user wants a watchable preview fast,
without touching their Premiere project.

usage: python ae_assemble.py edit.json out.mp4      -> writes <edit>_assemble.jsx, then: python ae_run.py <that jsx>
edit.json = {"w": 1920, "h": 1080, "fps": 29.97, "total": 60.0,
             "items": [{"kind": "video|vo|music|sfx", "path": "C:/...", "a": 0.0, "b": 5.0, "si": 0.0, "db": -3.0, "label": "..."}]}
a / b = sequence in / out seconds (b null = to the end of the file, at most 4 s for sfx), si = source in, db = level.
Music gets a 1 s fade in and a 1.5 s fade out. Earlier items end up on TOP (list picture shots in time order).
Check the result with: python ../media/atools.py out.mp4  (aim about -14 LUFS integrated, peaks under -1 dBTP).
"""
# macOS (from the Mac port, Oct 2026; the Windows script is unchanged): on a Mac the written .jsx refuses to run when AE
# already has a project open (ae_run.py there hands scripts to the open AE), sets the sRGB IEC61966-2.1 working space
# (AE 2026's Rec.709 default shifted sRGB PNG colours on the Mac), writes Unix line feeds, closes only its own project
# and never quits AE (ae_run.py quits only an AE it launched). Paths in edit.json are then /abs/path/file.mov.
import json, os, sys

JSX = r'''app.beginSuppressDialogs();
var CFG = %s; var OUT = %s; var HERE = %s; var STEM = %s;
var LOG = [];
function writeFile(p, s) { var f = new File(p); f.encoding = "UTF-8"; f.open("w"); f.write(s); f.close(); }
function log(s) { LOG.push(s); writeFile(HERE + STEM + "_log.txt", LOG.join("\n")); }
log("START " + app.version);
try {
    app.newProject();
    var c = app.project.items.addComp("PREVIEW", CFG.w, CFG.h, 1, CFG.total, CFG.fps);
    var cache = {};
    for (var i = CFG.items.length - 1; i >= 0; i--) {
        var it = CFG.items[i];
        if (!cache[it.path]) cache[it.path] = app.project.importFile(new ImportOptions(new File(it.path)));
        var L = c.layers.add(cache[it.path]); L.name = it.label || it.kind;
        L.startTime = it.a - (it.si || 0);
        var dur = cache[it.path].duration;
        var b = (it.b === null || it.b === undefined) ? Math.min(it.a + (it.kind == "sfx" ? Math.min(dur - (it.si || 0), 4.0) : dur - (it.si || 0)), CFG.total) : it.b;
        L.inPoint = it.a; L.outPoint = b;
        if (it.kind != "video") {
            try { L.enabled = false; } catch (e0) {}
            var lv = L.property("ADBE Audio Group").property("ADBE Audio Levels");
            var db = (it.db === null || it.db === undefined) ? 0 : it.db;
            if (it.kind == "music") { lv.setValueAtTime(it.a, [-48, -48]); lv.setValueAtTime(it.a + 1.0, [db, db]); lv.setValueAtTime(b - 1.5, [db, db]); lv.setValueAtTime(b, [-48, -48]); }
            else lv.setValue([db, db]);
        } else if (it.fit) {
            var s = Math.max(CFG.w / L.source.width, CFG.h / L.source.height) * 100;
            L.property("ADBE Transform Group").property("ADBE Scale").setValue([s, s]);
        }
    }
    log("assembled " + CFG.items.length);
    var rq = app.project.renderQueue.items.add(c);
    rq.outputModule(1).applyTemplate("H.264 - Match Render Settings - 15 Mbps");
    rq.outputModule(1).file = new File(OUT);
    app.project.renderQueue.render();
    log("render preview status " + (rq.status == RQItemStatus.DONE ? "DONE" : rq.status));
} catch (e) { log("FATAL " + e.toString() + " line " + e.line); }
writeFile(HERE + STEM + "_DONE.txt", "done");
try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {}
app.quit();
'''


def _swap(text, old, new):
    """replace exactly one occurrence: if the template changes, fail loudly instead of silently skipping a Mac fix"""
    assert text.count(old) == 1, 'ae_assemble template changed, update the macOS patch: %r' % old[:50]
    return text.replace(old, new)


def _mac_jsx(t):
    """macOS version of the JSX template (before % formatting)"""
    t = _swap(t, 'f.encoding = "UTF-8"; f.open("w");', 'f.encoding = "UTF-8"; f.lineFeed = "Unix"; f.open("w");')
    t = _swap(t, 'try {\n    app.newProject();\n',
              'var OURS = false;\ntry {\n'
              '    if (app.project && (app.project.file !== null || app.project.dirty || app.project.numItems > 0))\n'
              '        throw new Error("refusing to run: AE already has a project open (" + (app.project.file ? app.project.file.fsName : "untitled") + ")");\n'
              '    app.newProject(); OURS = true;\n'
              '    try { app.project.workingSpace = "sRGB IEC61966-2.1"; } catch (ews) {}\n')
    return _swap(t, 'writeFile(HERE + STEM + "_DONE.txt", "done");\ntry { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {}\napp.quit();\n',
                 'if (OURS) { try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {} }\n'
                 'try { app.endSuppressDialogs(false); } catch (ed) {}\nwriteFile(HERE + STEM + "_DONE.txt", "done");\n')


if __name__ == '__main__':
    if len(sys.argv) < 3: sys.exit(__doc__)
    if sys.platform == 'darwin': JSX = _mac_jsx(JSX)
    edit, out = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
    cfg = json.load(open(edit, encoding='utf-8'))
    for it in cfg['items']: it['path'] = it['path'].replace('\\', '/')
    jsx = os.path.splitext(edit)[0] + '_assemble.jsx'
    stem = os.path.splitext(os.path.basename(jsx))[0]
    here = os.path.dirname(jsx).replace('\\', '/') + '/'
    open(jsx, 'w', encoding='utf-8').write(JSX % (json.dumps(cfg), json.dumps(out.replace('\\', '/')), json.dumps(here), json.dumps(stem)))
    json.dump([dict(name='preview', file=out.replace('\\', '/'))], open(os.path.splitext(jsx)[0] + '_jobs.json', 'w'))
    print('wrote', jsx, '| items', len(cfg['items']), '| run: python ae_run.py "%s"' % jsx)
