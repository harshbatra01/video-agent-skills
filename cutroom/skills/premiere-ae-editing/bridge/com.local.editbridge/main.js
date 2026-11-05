// Local-only bridge: runs ExtendScript jobs POSTed by local tools (pp.py). Requires the token in ~/.editbridge_token.
// Security model: listens on 127.0.0.1 only, every request must carry the token (header x-bridge-token), requests with
// an Origin header (browsers) are refused, so only local programs that can read the token file get in. Anything that
// gets in can run any ExtendScript inside Premiere (read/write files as the user), so the token file must stay private.
(function () {
  var http = require('http'), fs = require('fs'), path = require('path'), os = require('os');
  var TOKEN = fs.readFileSync(path.join(os.homedir(), '.editbridge_token'), 'utf8').trim();
  // refuse to start with an empty or short token: an empty one would accept a request with an empty header
  if (TOKEN.length < 20) { return; }
  // Premiere 2025 listens on 47916 so it can run beside Premiere 2026 (47915) without a port clash
  var PORT = 47915;
  try { if (String(JSON.parse(window.__adobe_cep__.getHostEnvironment()).appVersion).split('.')[0] === '25') { PORT = 47916; } } catch (e) {}
  var jobDir = path.join(os.tmpdir(), 'editbridge_jobs');
  try { fs.mkdirSync(jobDir); } catch (e) {}
  var server = http.createServer(function (req, res) {
    if (req.method !== 'POST' || req.headers['x-bridge-token'] !== TOKEN || req.headers.origin) {
      res.writeHead(403); res.end('forbidden'); return;
    }
    var body = '';
    req.on('data', function (c) { body += c; });
    req.on('end', function () {
      var f = path.join(jobDir, 'job_' + Date.now() + '_' + Math.random().toString(36).slice(2) + '.jsx');
      fs.writeFileSync(f, body, 'utf8');
      var call = 'try { String($.evalFile(' + JSON.stringify(f) + ')); } catch (e) { "ERR: " + e.toString() + " (line " + e.line + ")"; }';
      window.__adobe_cep__.evalScript(call, function (result) {
        try { fs.unlinkSync(f); } catch (e) {}
        res.writeHead(200, { 'Content-Type': 'text/plain; charset=utf-8' });
        res.end(String(result));
      });
    });
  });
  server.listen(PORT, '127.0.0.1');
})();
