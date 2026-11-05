"""pp.py: run ExtendScript inside a RUNNING Premiere Pro through the local CEP bridge (com.local.editbridge, installed
from this skill's bridge/ folder with bridge/install_bridge.sh on macOS; on Windows it needs a manual install).

usage: ~/.venvs/premiere-ae/bin/python pp.py --v 2026 job.jsx        run a script file, print what it returns
       ~/.venvs/premiere-ae/bin/python pp.py --v 2025 -e "app.version" run one expression
       ~/.venvs/premiere-ae/bin/python pp.py --v 2026 --status         open projects + active sequence (look before acting)

Ports (since 11 Oct 2026): Premiere 2026 = 47915, Premiere 2025 = 47916, so both can run at once. The token lives in
~/.editbridge_token and is sent as header x-bridge-token: never print or store it. The bridge rejects requests that
carry an Origin header (browsers), so only local tools can call it.

Rules that come with it (see references/premiere-ui.md):
- Look first (--status). The user often has their own projects open in one or both versions.
- Build in a COPY: app.openDocument(copy, true, true, true, true) opens it as a second project; app.projects lists both.
  Never save or close their project; close yours with app.projects[i].closeDocument(0, 0) only if you opened it.
- Import ~20 files per call (one importFiles call with 20 paths), save, then the next call. 150 in one call stalled 2025.
- If the bridge stops answering and the CEP log says "Heartbeat call failed", one Premiere restart fixes it: ASK first.
"""
import sys, os, argparse, urllib.request

PORTS = {'2026': 47915, '2025': 47916}
STATUS = r'''(function () {
    var out = [];
    out.push("Premiere " + app.version);
    for (var i = 0; i < app.projects.numProjects; i++) {
        var p = app.projects[i];
        out.push("project " + i + ": " + p.name + " | " + p.path + (p.path == app.project.path ? "  [active]" : ""));
    }
    var s = app.project.activeSequence;
    out.push("active sequence: " + (s ? s.name + " (" + s.videoTracks.numTracks + "V/" + s.audioTracks.numTracks + "A, end " + s.end + " ticks)" : "none"));
    return out.join("\n");
})();'''


def run(js, version='2026', timeout=900):
    tok = open(os.path.expanduser('~/.editbridge_token')).read().strip()
    req = urllib.request.Request('http://127.0.0.1:%d/' % PORTS[version], data=js.encode('utf-8'), method='POST',
                                 headers={'x-bridge-token': tok, 'Content-Type': 'text/plain; charset=utf-8'})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode('utf-8', 'replace')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('jsx', nargs='?'); ap.add_argument('--v', default='2026', choices=sorted(PORTS))
    ap.add_argument('-e', dest='expr'); ap.add_argument('--status', action='store_true'); ap.add_argument('--timeout', type=int, default=900)
    a = ap.parse_args()
    if a.status: js = STATUS
    elif a.expr: js = a.expr
    elif a.jsx: js = open(a.jsx, encoding='utf-8').read()
    else: sys.exit(__doc__)
    try: print(run(js, a.v, a.timeout))
    except Exception as e: sys.exit('bridge %s (port %d) did not answer: %s' % (a.v, PORTS[a.v], e))
