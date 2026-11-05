"""Assemble gfx_v2.jsx: header + v1 helpers + v2 builders + batch spec (JSON) + render loop.
Overlay timings are absolute sequence seconds here and converted to comp-relative times.
usage: python make_gfx_v2.py [name,name,...]   (ONLY list; default all)"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "C:/VISION/IMMUFIX/repair/ENCODED RUSHES/Motion graphics/gfx_v2/"
IN = HERE.replace('\\', '/') + '/gfx_in/'
W, R, G = 'WHITE', 'RED', 'GREEN'

SPECS = []           # (kind, start_seq, spec with absolute times in keys ending with '@')


def add(kind, start, end, **sp):
    sp['_start'] = start; sp['_end'] = end
    SPECS.append((kind, sp))


def rel(t, s): return round(t - s, 4)


# ---------------------------------------------------------------- 3 questions (974102f7)
add('card', 3.45, 8.22, name='q3_q1', q="Why can't we just eat a good balanced diet with lots of fruits and vegetables instead of taking a supplement?", tA=3.62, tB=7.90, exit='pop', ad='974102f7')
add('article', 10.95, 13.50, name='q3_news', img='natgeo_head.png', iw=1080, ih=530, cw=1000, exit='cut', ad='974102f7',
    hl=[[756, 848, 247, 301, 12.27, 12.47], [71, 889, 315, 369, 12.78, 13.40]])
add('card', 18.55, 21.33, name='q3_q2', q='How does it work?', tA=19.35, tB=19.95, exit='cut', ad='974102f7')
add('cap', 21.33, 23.03, name='q3_body', bdIn=True, ad='974102f7', beats=[dict(kick=[['YOUR BODY', W]], kIn=21.36, mains=[['RECOGNISES', 22.37]], out=-1)])
add('stack', 24.20, 26.68, name='q3_vmn', ad='974102f7', words=[['VITAMINS', 24.77, 560], ['MINERALS', 25.23, 960], ['NUTRIENTS', 25.62, 1360]])
add('card', 29.55, 32.18, name='q3_q3', q='How long until I see the benefits?', tA=30.60, tB=32.05, exit='cut', ad='974102f7')
add('counter', 41.58, 42.70, name='q3_since', ad='974102f7', **{'from': 2026, 'to': 1998, 'a': 41.60, 'b': 41.98, 'size': 210, 'x': 78, 'numY': 470, 'just': 'L',
    'label': 'TAKING IT SINCE', 'labelY': 255, 'sub': 'ALMOST 30 YEARS', 'subY': 545, 'tSub': 42.02, 'dim': False, 'bd': 'top', 'out': 42.70})
# ---------------------------------------------------------------- 3 things (f233433f)
add('qmark', 0.40, 3.70, name='tt_qmark', ad='f233433f', tIn=0.55, tOut=3.45)
add('glass', 3.55, 9.37, name='tt_p1', ad='f233433f', x0=40, y0=110, w=520, kick=[['NUMBER ONE', 3.60]], main=[['NO MEGA', 4.02], ['DOSES', 4.58]], tIn=3.55, tOut=9.12)
add('meter', 9.40, 13.18, name='tt_meter', ad='f233433f', c0=10.62, c1=11.62, fo=12.95, endLabel='MEGA DOSE')
add('glass', 14.40, 19.05, name='tt_p2', ad='f233433f', x0=40, y0=110, w=520, kick=[['ENHANCED', 15.10], ['NUTRIENT', 15.74]], main=[['BIOAVAILABILITY', 16.30]],
    tIn=14.40, tOut=-1, p2=dict(t=17.15, noun='noun', **{'def': 'How much of a nutrient your body can actually absorb and use.'}))
add('cap', 19.05, 21.20, name='tt_powder', ad='f233433f', bdIn=True, beats=[dict(kick=[['WE', W]], kIn=19.06, mains=[['FORMULATED', 19.26]], out=20.00),
                                                                       dict(kick=[['TO ENSURE', W]], kIn=20.06, mains=[['YOUR BODY', 20.58]], out=-1)])
add('stack', 22.78, 25.27, name='tt_vmn', ad='f233433f', words=[['VITAMINS', 22.90, 560], ['MINERALS', 23.42, 960], ['NUTRIENTS', 24.10, 1360]])
add('glass', 27.60, 30.62, name='tt_p3', ad='f233433f', x0=40, y0=110, w=520, kick=[['BETTER', 28.18], ['CELLULAR', 28.58]], main=[['UPTAKE', 29.06]], tIn=27.60, tOut=30.37)
add('cap', 31.74, 33.90, name='tt_almost', ad='f233433f', bdIn=True, beats=[dict(kick=[['ALMOST', W]], kIn=31.76, mains=[['100%', 32.18, dict(a=32.18, b=32.66, **{'from': 0, 'to': 100, 'suf': '%'})]], out=-1)])
add('cap', 35.10, 36.87, name='tt_cells', ad='f233433f', bdIn=True, flash=False, beats=[dict(kick=[['IMMEDIATELY', W]], kIn=35.22, mains=[['INTO THE CELLS', 36.10]], out=-1)])
# ---------------------------------------------------------------- I'm 52 (348e0ba6)
add('cap', 15.96, 17.05, name='i52_24', ad='348e0ba6', bdIn=True, beats=[dict(kick=[['SINCE I WAS', W]], kIn=15.97, mains=[['24', 16.40, dict(a=16.40, b=16.75, **{'from': 0, 'to': 24})]], out=-1)])
add('cap', 17.05, 18.97, name='i52_scoop', ad='348e0ba6', bdIn=True, beats=[dict(kick=[['JUST ONE', W]], kIn=17.06, mains=[['25G SCOOP', 17.80]], out=-1)])
add('cap', 18.97, 19.92, name='i52_water', ad='348e0ba6', bdIn=False, beats=[dict(kick=[['MIXED WITH', W]], kIn=18.97, mains=[['WATER', 19.36]], out=-1)])
add('stack', 21.28, 23.00, name='i52_vmn', ad='348e0ba6', words=[['VITAMINS', 21.30, 560], ['MINERALS', 21.88, 960], ['NUTRIENTS', 22.36, 1360]])
# ---------------------------------------------------------------- Ran professionally (0991faf2)
add('cap', 3.38, 5.77, name='rp_wr', ad='0991faf2', bdIn=True, beats=[dict(kick=[['WORLD RECORD', W]], kIn=3.67, mains=[['16 YEARS', 4.88, dict(a=4.88, b=5.22, suf=' YEARS', **{'from': 0, 'to': 16})]], out=-1)])
add('cap', 8.18, 10.78, name='rp_pills', ad='0991faf2', bdIn=True, beats=[dict(kick=[['A', W], ['MULTITUDE', R], ['OF', W]], kIn=8.38, mains=[['PILLS', 9.73], ['SUPPLEMENTS', 10.15]], out=-1)])
add('stack', 15.62, 17.48, name='rp_vmn', ad='0991faf2', words=[['VITAMINS', 15.64, 560], ['MINERALS', 16.30, 960], ['NUTRIENTS', 16.80, 1360]])
add('cap', 19.75, 21.48, name='rp_water', ad='0991faf2', bdIn=True, beats=[dict(kick=[['ONE', W]], kIn=19.76, mains=[['SCOOP', 20.02]], out=20.46),
                                                                       dict(kick=[['MIXED WITH', W]], kIn=20.52, mains=[['WATER', 20.98]], out=-1)])
# ---------------------------------------------------------------- Secret weapon (593f11c4)
add('article', 2.75, 5.68, name='sw_news', img='bbc_card.png', iw=700, ih=463, cw=980, exit='pop', ad='593f11c4', y=900,
    hl=[[551, 651, 273, 297, 3.05, 3.20], [21, 459, 304, 328, 3.20, 4.00], [565, 640, 349, 373, 4.25, 4.45]])
add('cap', 12.35, 14.30, name='sw_train', ad='593f11c4', bdIn=True, beats=[dict(kick=[['TWO WEEKS LATER', W]], kIn=12.37, mains=[['TRAINING', 13.59]], out=-1)])
add('cap', 14.30, 16.48, name='sw_win', ad='593f11c4', bdIn=True, beats=[dict(kick=[['THREE MONTHS LATER', W]], kIn=14.32, mains=[['EUROPEAN CHAMPION', 15.18]], out=-1)])
# ---------------------------------------------------------------- I held the record / ready to recover (404c5cb2)
add('cap', 2.67, 4.72, name='hr_asks', ad='404c5cb2', bdIn=True, beats=[dict(kick=[['THE MARATHON', W]], kIn=2.69, mains=[['ASKS A LOT', 3.31]], out=-1)])
add('cap', 4.72, 6.67, name='hr_train', ad='404c5cb2', bdIn=True, beats=[dict(kick=[['MONTHS OF', W]], kIn=5.15, mains=[['TRAINING', 5.63]], out=-1)])
add('window', 14.30, 16.32, name='hr_window', ad='404c5cb2', tK=14.42, a=15.08, b=15.40, tU=15.42, t30=15.83)
add('cap', 16.32, 18.05, name='hr_refuel', ad='404c5cb2', bdIn=True, beats=[dict(kick=[['THE BEST TIME TO', W]], kIn=16.34, mains=[['REFUEL', 17.44]], out=-1)])
add('cap', 19.36, 20.90, name='hr_recover', ad='404c5cb2', bdIn=True, beats=[dict(kick=[['FOR THE', W]], kIn=19.73, mains=[['RECOVERY', 19.90]], out=-1)])
add('cap', 26.77, 28.28, name='hr_scoop', ad='404c5cb2', bdIn=True, beats=[dict(kick=[['ONE', W]], kIn=26.78, mains=[['SCOOP', 26.98]], out=27.34),
                                                                         dict(kick=[['MIXED WITH', W]], kIn=27.40, mains=[['WATER', 27.65]], out=-1)])
add('cap', 28.28, 29.60, name='hr_ready', ad='404c5cb2', bdIn=True, flash=False, beats=[dict(kick=[["I'M", W]], kIn=28.29, mains=[['READY TO RECOVER', 28.66]], out=-1)])
# ---------------------------------------------------------------- People are always surprised (664b35b2)
add('cap', 2.75, 3.83, name='ps_gear', ad='664b35b2', bdIn=True, beats=[dict(kick=[['RATHER THAN', W]], kIn=2.76, mains=[['RUNNING GEAR', 3.38]], out=-1)])
add('cap', 5.93, 7.52, name='ps_90', ad='664b35b2', bdIn=True, below=['OF THE TIME', 6.90], beats=[dict(kick=[], kIn=5.93, mains=[['90%', 5.94, dict(a=5.94, b=6.40, suf='%', **{'from': 0, 'to': 90})]], out=-1)])
add('flash', 7.48, 7.70, name='fx_flash', ad='664b35b2')
add('cap', 13.57, 15.48, name='ps_drains', ad='664b35b2', bdIn=True, beats=[dict(kick=[['LOTS OF', W], ['DRAINS', R], ['ON MY', W]], kIn=13.58, mains=[['IMMUNE SYSTEM', 14.71]], out=-1)])
add('cap', 20.72, 21.80, name='ps_24', ad='664b35b2', bdIn=True, beats=[dict(kick=[['SINCE I WAS', W]], kIn=20.73, mains=[['24', 21.15, dict(a=21.15, b=21.50, **{'from': 0, 'to': 24})]], out=-1)])

def build_specs():
    qm = json.load(open(os.path.join(HERE, '..', 'track', 'masks_tt.json')))['qmark']
    out = []
    for kind, sp in SPECS:
        s, e = sp['_start'], sp['_end']
        d = json.loads(json.dumps({k: v for k, v in sp.items() if not k.startswith('_')}))
        R = lambda t: rel(t, s)
        if kind == 'cap':
            for bt in d['beats']:
                bt['kIn'] = R(bt['kIn'])
                if bt['out'] > 0: bt['out'] = R(bt['out'])
                bt['mains'] = [[m[0], R(m[1])] + ([dict(m[2], a=R(m[2]['a']), b=R(m[2]['b']))] if len(m) > 2 else []) for m in bt['mains']]
            if 'below' in d: d['below'] = [d['below'][0], R(d['below'][1])]
        elif kind == 'stack': d['words'] = [[w[0], R(w[1]), w[2]] for w in d['words']]
        elif kind == 'card': d['tA'] = R(d['tA']); d['tB'] = R(d['tB'])
        elif kind == 'article': d['hl'] = [h[:4] + [R(h[4]), R(h[5])] for h in d['hl']]
        elif kind == 'glass':
            d['kick'] = [[k[0], R(k[1])] for k in d['kick']]; d['main'] = [[m[0], R(m[1])] for m in d['main']]
            d['tIn'] = R(d['tIn']); d['tOut'] = R(d['tOut']) if d['tOut'] >= 0 else -1
            if 'p2' in d: d['p2']['t'] = R(d['p2']['t'])
        elif kind == 'meter':
            for k in ('c0', 'c1', 'fo'): d[k] = R(d[k])
        elif kind == 'qmark':
            d['tIn'] = R(d['tIn']); d['tOut'] = R(d['tOut'])
            d['track'] = [[round(r[0] - s, 4)] + r[1:] for r in qm if s - 0.05 <= r[0] <= e + 0.05]
        elif kind == 'counter':
            for k in ('a', 'b', 'tSub', 'out'): d[k] = R(d[k])
        elif kind == 'window':
            for k in ('tK', 'a', 'b', 'tU', 't30'): d[k] = R(d[k])
        d['dur'] = round(e - s, 4)
        out.append([kind, d, s, e])
    return out


if __name__ == '__main__':
    only = sys.argv[1].split(',') if len(sys.argv) > 1 else []
    specs = build_specs()
    json.dump([[k, d] for k, d, s, e in specs], open(os.path.join(HERE, 'gfx_v2_specs.json'), 'w'), indent=0)
    meta = {d['name']: dict(kind=k, start=s, end=e, ad=d.get('ad')) for k, d, s, e in specs}
    json.dump(meta, open(os.path.join(HERE, 'gfx_v2_meta.json'), 'w'), indent=0)
    hdr = '''// Immufix motion graphics v2 (generated by make_gfx_v2.py). Run: AfterFX.exe -r gfx_v2.jsx
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
''' % (OUT, IN, json.dumps(only))
    helpers = open(os.path.join(HERE, 'gfx_helpers_v1.jsx'), encoding='utf-8').read()
    # v1 counter builder (reused for q3_since) lives after the helpers in gfx_v1.jsx
    v1 = open(os.path.join(HERE, 'gfx_v1.jsx'), encoding='utf-8').read()
    counter_src = v1[v1.index('function counter(sp)'):v1.index('// ---------------------------------------------------------------- the batch')]
    body = open(os.path.join(HERE, 'gfx_v2_body.jsx'), encoding='utf-8').read()
    run = '''
var SPECS = %s;
var COLORS = {"WHITE": WHITE, "RED": RED, "GREEN": GREEN};
function fixColors(o) { if (o instanceof Array) { for (var i = 0; i < o.length; i++) { if (typeof o[i] == "string" && COLORS[o[i]] && i == 1) o[i] = COLORS[o[i]]; else fixColors(o[i]); } } else if (o && typeof o == "object") { for (var k in o) fixColors(o[k]); } }
try {
    var proj = app.newProject();
    var f = new Folder(OUT); if (!f.exists) f.create();
    var outs = [];
    for (var j = 0; j < SPECS.length; j++) {
        var kind = SPECS[j][0], sp = SPECS[j][1], c = null;
        var want = !ONLY.length; for (var q = 0; q < ONLY.length; q++) if (ONLY[q] == sp.name) want = true;
        if (!want) continue;
        fixColors(sp);
        try {
            if (kind == "cap") c = caption2(sp);
            else if (kind == "stack") c = stack(sp);
            else if (kind == "card") c = qcard2(sp);
            else if (kind == "article") c = article2(sp);
            else if (kind == "glass") c = glass2(sp);
            else if (kind == "meter") c = meter2(sp);
            else if (kind == "qmark") c = qmark(sp);
            else if (kind == "counter") c = counter(sp);
            else if (kind == "window") c = windowGfx(sp);
            else if (kind == "flash") c = flashGfx(sp);
            outs.push([sp.name, c]); log("built " + sp.name);
        } catch (e) { log("FAILED " + sp.name + ": " + e.toString() + " line " + e.line); }
        writeFile(OUT + "gfx_v2_log.txt", LOG.join("\\n"));
    }
    var gs = []; for (var gk in GEOM) { var g = GEOM[gk]; gs.push('"' + gk + '": {"x0": ' + g.x0 + ', "y0": ' + g.y0 + ', "w": ' + g.w + ', "h1": ' + g.h1 + ', "h2": ' + g.h2 + ', "r": ' + g.r + ', "tIn": ' + g.tIn + ', "tOut": ' + g.tOut + ', "tG": ' + g.tG + ', "dur": ' + g.dur + '}'); }
    writeFile(OUT + "glass_geom.json", "{" + gs.join(", ") + "}");
    proj.save(new File(OUT + "immufix_gfx_v2.aep"));
    for (var o = 0; o < outs.length; o++) {
        var rq = proj.renderQueue.items.add(outs[o][1]);
        rq.outputModule(1).applyTemplate("High Quality with Alpha");
        rq.outputModule(1).file = new File(OUT + outs[o][0]);
        log("render " + outs[o][0]); writeFile(OUT + "gfx_v2_log.txt", LOG.join("\\n"));
        proj.renderQueue.render();
        rq.remove();
    }
    proj.save();
    LOG.push("render done");
} catch (err) { LOG.push("FATAL " + err.toString() + " line " + err.line); }
writeFile(OUT + "gfx_v2_log.txt", LOG.join("\\n"));
writeFile(OUT + "gfx_v2_DONE.txt", "done");
''' % json.dumps([[k, d] for k, d, s, e in specs])
    open(os.path.join(HERE, 'gfx_v2.jsx'), 'w', encoding='utf-8').write(hdr + helpers + '\n' + counter_src + '\n' + body + run)
    print('wrote gfx_v2.jsx with', len(specs), 'specs')
