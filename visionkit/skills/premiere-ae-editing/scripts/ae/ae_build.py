"""ae_build.py: write ONE After Effects script that builds every shot of a batch and renders them one at a time.

Pattern (used for ~100 shots per job): a Python generator decides the shots (times from word timings, crops from
OCR, etc.) and emits short JavaScript "specs"; this writer wraps them with the helper libraries and a safe render loop.

    import sys, os; sys.path.insert(0, os.path.expanduser('~/.claude/skills/premiere-ae-editing/scripts/ae'))
    from ae_build import write_jsx
    shots = [dict(name='T01_TITLE'), dict(name='T02_STAR', template='alpha')]
    specs = ['SHOTS["T01_TITLE"] = (function(){ var c = newComp("T01_TITLE", 4.0); '
             'txt(c, "Hello", "ProximaNova-Semibold", 90, [1,1,1], null, 0, W/2, H/2); return c; })();', ...]
    jsx = write_jsx(r'C:/job/ae/batch1.jsx', shots, specs, out_dir=r'C:/job/renders/batch1', w=1920, h=1080, fps=29.97)
    # then:  python ae_run.py C:/job/ae/batch1.jsx      (set ONLY=T02_STAR to re-render a subset)

Each spec runs inside its own try/catch, so one broken shot logs "BUILD FAIL i" and the rest still render.
Libraries are COPIED into the .jsx when it is written: after editing a library, regenerate the .jsx.
Templates (AE 2026 names, checked 7 Oct 2026): prores = "High Quality" (ProRes 422 10-bit .mov, opaque shots for
Premiere), alpha = "High Quality with Alpha" (ProRes 4444 with alpha, overlays for a top track in Premiere),
h264 = "H.264 - Match Render Settings - 15 Mbps" (previews, carries audio), tiff = "TIFF Sequence with Alpha"
(frames for analysis). There is NO "Apple ProRes 422 HQ" template: asking for it logs "template fail" and falls back.
"""
# macOS (from the Mac port, Oct 2026; Windows output is unchanged): the same template names were found in AE 26.2 on a Mac
# (11 Oct 2026). When this runs on a Mac the generated script also (1) refuses to build if AE already has a project open
# (saved file, unsaved changes or any items), because ae_run.py on the Mac hands scripts to the AE that is already open,
# (2) closes only the project it created and never calls app.quit() (ae_run.py quits only an AE it launched),
# (3) writes its log and DONE flag with Unix line feeds (ExtendScript writes \r on the Mac otherwise), and
# (4) sets the sRGB IEC61966-2.1 working space (working_space='auto'): AE 2026 starts new projects in Rec.709 Gamma 2.4,
# which shifted sRGB PNG colours on the Mac (#1A6317 became #266B23). On Windows 'auto' keeps AE's default, as before;
# pass working_space='sRGB IEC61966-2.1' to opt in there (test one shot first: it changes colours of renders).
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATES = {'prores': 'High Quality', 'alpha': 'High Quality with Alpha', 'h264': 'H.264 - Match Render Settings - 15 Mbps',
             'tiff': 'TIFF Sequence with Alpha', 'hq': 'High Quality'}
EXT = {'prores': '.mov', 'alpha': '.mov', 'h264': '.mp4', 'hq': '.mov'}


def out_file(out_dir, name, template):
    if template == 'tiff':
        return os.path.join(out_dir, name, name + '_[#####].tif').replace('\\', '/')
    return os.path.join(out_dir, name + EXT.get(template, '.mov')).replace('\\', '/')


def _swap(text, old, new):
    """replace exactly one occurrence: if a template line changes, fail loudly instead of silently skipping a Mac fix"""
    assert text.count(old) == 1, 'ae_build template changed, update the macOS patch: %r' % old[:50]
    return text.replace(old, new)


def _mac_run(run):
    """macOS version of the render loop (template text, before % formatting): project guard, close only our project,
    restore dialogs, no app.quit()"""
    run = _swap(run, 'try {\n    log("START " + app.version);\n    app.newProject();\n',
                'var OURS = false;\ntry {\n    log("START " + app.version);\n'
                '    if (app.project && (app.project.file !== null || app.project.dirty || app.project.numItems > 0))\n'
                '        throw new Error("refusing to run: AE already has a project open (" + (app.project.file ? app.project.file.fsName : "untitled") + ")");\n'
                '    app.newProject(); OURS = true;\n')
    return _swap(run, 'writeFile(HERE + %s, "done");\ntry { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {}\napp.quit();\n',
                 'if (OURS) { try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {} }\n'
                 'try { app.endSuppressDialogs(false); } catch (ed) {}\nwriteFile(HERE + %s, "done");\n')


def write_jsx(jsx_path, shots, specs, out_dir, libs=(), w=1920, h=1080, fps=29.97, template='prores', aep_path=None, only=None,
              working_space='auto'):
    """shots: [{'name': comp key in SHOTS, 'template': optional}], specs: JavaScript strings that fill SHOTS[name].
    libs: extra .jsx libraries (ae_lib.jsx is always first). aep_path: save the built project there (for hand fixes).
    only: list of shot names to render (default: env ONLY=a,b or all).
    working_space: 'auto' = sRGB IEC61966-2.1 on macOS, AE's default on Windows; a name forces it; None keeps AE's default."""
    if working_space == 'auto': working_space = 'sRGB IEC61966-2.1' if sys.platform == 'darwin' else None
    J = json.dumps
    jsx_path = os.path.abspath(jsx_path)
    here = os.path.dirname(jsx_path).replace('\\', '/') + '/'
    stem = os.path.splitext(os.path.basename(jsx_path))[0]
    os.makedirs(out_dir, exist_ok=True)
    if only is None: only = [a for a in os.environ.get('ONLY', '').split(',') if a]
    jobs = []
    for s in shots:
        tpl = s.get('template', template)
        f = out_file(out_dir, s['name'], tpl)
        if tpl == 'tiff': os.makedirs(os.path.dirname(f), exist_ok=True)
        jobs.append(dict(name=s['name'], template=TEMPLATES.get(tpl, tpl), file=f))
    hdr = ('// generated by ae_build.py: %s\napp.beginSuppressDialogs();\nvar W = %d, H = %d, FPS = %s;\nvar HERE = %s; var LOGNAME = %s;\n'
           'var LOG = [];\nfunction writeFile(p, s) { var f = new File(p); f.encoding = "UTF-8"; f.open("w"); f.write(s); f.close(); }\n'
           'var SHOTS = {};\nvar ONLY = %s;\n') % (stem, w, h, repr(float(fps)), J(here), J(stem + '_log.txt'), J(only))
    run = '''
try {
    log("START " + app.version);
    app.newProject();
    var BUILDERS = %s;
    for (var i = 0; i < BUILDERS.length; i++) { try { eval(BUILDERS[i]); } catch (e) { log("BUILD FAIL " + i + ": " + e.toString() + " line " + e.line); } }
    var AEP = %s;
    if (AEP) app.project.save(new File(AEP));
    var JOBS = %s;
    for (var n = 0; n < JOBS.length; n++) {
        var jb = JOBS[n];
        if (ONLY.length && !inArr(ONLY, jb.name)) continue;
        var comp = SHOTS[jb.name]; if (!comp) { log("missing " + jb.name); continue; }
        var rq = app.project.renderQueue.items.add(comp);
        // render the comp's work area (a spec can set comp.workAreaStart/Duration to test one moment; default = whole comp)
        try { rq.timeSpanStart = comp.workAreaStart; rq.timeSpanDuration = comp.workAreaDuration; } catch (ets) { log("time span " + ets.toString()); }
        var om = rq.outputModule(1), ok = false;
        try { om.applyTemplate(jb.template); ok = true; } catch (e1) { log("template fail " + jb.template + ": " + e1.toString()); }
        if (!ok) { try { om.applyTemplate("High Quality"); } catch (e2) {} }
        om.file = new File(jb.file);
        try { app.project.renderQueue.render(); } catch (er) { log("render error " + er.toString()); }
        log("render " + jb.name + " status " + (rq.status == RQItemStatus.DONE ? "DONE" : rq.status));
        rq.remove();
    }
    log("ALL DONE");
} catch (err) { log("FATAL " + err.toString() + " line " + err.line); }
writeFile(HERE + %s, "done");
try { app.project.close(CloseOptions.DO_NOT_SAVE_CHANGES); } catch (eq) {}
app.quit();
'''
    if sys.platform == 'darwin':
        run = _mac_run(run)
        hdr = _swap(hdr, 'f.encoding = "UTF-8"; f.open("w");', 'f.encoding = "UTF-8"; f.lineFeed = "Unix"; f.open("w");')
    if working_space:   # right after app.newProject(); %% because the template is %-formatted next
        k = run.index('\n', run.index('    app.newProject();')) + 1
        run = (run[:k] + '    var WS = ' + J(working_space).replace('%', '%%') + ';\n'
               '    try { app.project.workingSpace = WS; } catch (ews) { log("working space fail " + ews.toString()); }\n' + run[k:])
    run = run % (J(list(specs)), J(aep_path.replace('\\', '/') if aep_path else ''), J(jobs), J(stem + '_DONE.txt'))
    lib_paths = [os.path.join(HERE, 'ae_lib.jsx')] + [l for l in libs]
    body = '\n'.join(open(p, encoding='utf-8').read() for p in lib_paths)
    with open(jsx_path, 'w', encoding='utf-8') as f: f.write(hdr + body + '\n' + run)
    json.dump(jobs, open(os.path.join(os.path.dirname(jsx_path), stem + '_jobs.json'), 'w'), indent=1)
    return jsx_path


if __name__ == '__main__':
    print(__doc__)
