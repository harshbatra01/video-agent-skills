/* motion_more.js: the look kit, shared motion helpers (impact, mask words, scramble, cue sheet) and the newer video formats:
   countdown (broadcast), quizclock (tabloid), forecast (weather), race (neon), sim100 (paper), linestory (terminal).
   Inlined by render.Studio.load after the main motion.html script. Every frame stays a pure function of t. */
const f30 = n => n / 30;
const LOOKS = {
  night:    {bg:'#0B0C0F', panel:'#14161B', line:'#262A33', text:'#F4F5F7', muted:'#8B919C', acc:'#D4FF3A', acc2:'#FF2E88', acc3:'#22E1FF', on:'#0B0C0F', disp:"'OCDisplay','Anton',Impact,sans-serif", dw:'400'},
  broadcast:{bg:'#06122B', panel:'#0C1D45', line:'#1E3A7A', text:'#FFFFFF', muted:'#93A8D6', acc:'#3CF0FF', acc2:'#FFC83D', acc3:'#FF4D6D', on:'#06122B', disp:"'LookBebas','Bebas Neue',Impact,sans-serif", dw:'400'},
  tabloid:  {bg:'#FFE600', panel:'#FFFFFF', line:'#111111', text:'#0B0B0B', muted:'#3D3D3D', acc:'#E10600', acc2:'#0B0B0B', acc3:'#0057FF', on:'#FFFFFF', disp:"'LookArchivo','Archivo Black',Impact,sans-serif", dw:'400'},
  paper:    {bg:'#F3EFE6', panel:'#FFFFFF', line:'#D9D2C3', text:'#141414', muted:'#6B655A', acc:'#E63B2E', acc2:'#1F4FD8', acc3:'#0E9F6E', on:'#FFFFFF', disp:"'LookInter','Inter',Arial,sans-serif", dw:'900'},
  terminal: {bg:'#030603', panel:'#081008', line:'#174117', text:'#C8FFC8', muted:'#5FA35F', acc:'#39FF14', acc2:'#FF4040', acc3:'#FFD23F', on:'#030603', disp:"'LookMono','JetBrains Mono',Consolas,monospace", dw:'800'},
  weather:  {bg:'#2F6FE0', panel:'rgba(255,255,255,.14)', line:'rgba(255,255,255,.22)', text:'#FFFFFF', muted:'rgba(255,255,255,.8)', acc:'#FFD54A', acc2:'#FF8A8A', acc3:'#A8E8FF', on:'#0B2A66', disp:"'LookInter','Inter',Arial,sans-serif", dw:'300'},
  neon:     {bg:'#0D0221', panel:'#1A0640', line:'#3B1677', text:'#FFFFFF', muted:'#B9A6E8', acc:'#FF2BD6', acc2:'#29F0FF', acc3:'#FFE14D', on:'#0D0221', disp:"'LookAnton','Anton',Impact,sans-serif", dw:'400'},
  board:    {bg:'#0E1116', panel:'#161B22', line:'#2A313C', text:'#FFFFFF', muted:'#8C96A5', acc:'#2BD576', acc2:'#FF4D5E', acc3:'#F5C542', on:'#0E1116', disp:"'LookAnton','Anton',Impact,sans-serif", dw:'400'}
};
const DEFAULT_LOOK = {countdown:'broadcast', quizclock:'tabloid', forecast:'weather', race:'neon', sim100:'paper', linestory:'terminal', thennow:'board', scoreboard:'broadcast'};
let CUES = [], SHAKES = [], SHAKE_ON = false;

/* ---- Match line: the whole match told by the money. The line draws from kick-off to the whistle, goals land as spikes (night look, team colours) ---- */
F.matchline = d => {
  const T = tall(), Sx = d.series, cx = 80, cw = S.w - 170, cyT = T ? 820 : 560, ch = T ? 470 : 380;
  const t0 = d.t0, t1 = d.ft, X = t => cx + (Math.min(t, t1) - t0) / ((t1 - t0) || 1) * cw, Y = p => cyT + ch - p * ch;
  const path = s => s.pts.filter(p => p[0] <= t1).map((p, i) => (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1)).join(' ');
  const F_ = d.focus, ft = d.teams[F_], fs = Sx[F_ === 0 ? 0 : 2];
  const grid = [0, .25, .5, .75, 1].map(v => `<line x1="${cx}" x2="${cx + cw}" y1="${Y(v)}" y2="${Y(v)}" stroke="rgba(255,255,255,${v === .5 ? .16 : .07})" stroke-width="2"/><text x="${cx + cw + 12}" y="${Y(v) + 9}" fill="#8B919C" font-size="24" font-family="OCText,Inter">${Math.round(v * 100)}</text>`).join('');
  const ticks = [[d.ko, 'KO'], [d.ko + 62 * 60000, '2ND HALF'], [t1, 'FT']].map(x => `<text x="${X(x[0])}" y="${cyT + ch + 42}" fill="#8B919C" font-size="24" font-weight="700" text-anchor="middle" font-family="OCText,Inter">${x[1]}</text>`).join('');
  const lines = Sx.map((s, i) => `<path d="${path(s)}" fill="none" stroke="${s.color}" stroke-width="${s.width || 7}" stroke-linejoin="round" stroke-linecap="round" clip-path="url(#mclip)" opacity="${s.thin ? .35 : (i === 1 ? .7 : 1)}" stroke-dasharray="${s.thin ? '10 12' : 'none'}"/>
      <circle id="mh${i}" r="${i === 1 ? 9 : 13}" fill="${s.color}"/>`).join('');
  const goals = d.goals.map((g, k) => `<g class="mg" id="mg${k}" opacity="0"><line x1="${X(g.t)}" x2="${X(g.t)}" y1="${cyT - 6}" y2="${cyT + ch}" stroke="${Sx[g.side === 'home' ? 0 : 2].color}" stroke-width="3" stroke-dasharray="6 7"/>
      <circle cx="${X(g.t)}" cy="${cyT - 30 - (k % 2) * 46}" r="20" fill="${Sx[g.side === 'home' ? 0 : 2].color}"/><text x="${X(g.t)}" y="${cyT - 22 - (k % 2) * 46}" fill="#0B0C0F" font-size="22" font-weight="900" text-anchor="middle" font-family="OCText,Inter">&#9917;</text></g>`).join('');
  const html = wrap(`<div class="abs" style="inset:0;background:radial-gradient(80% 45% at 50% 0%,rgba(255,255,255,.07),transparent 70%),#0B0C0F"></div>
    <div class="abs" id="mlh" style="left:60px;right:60px;top:${T ? 226 : 50}px">
      <div style="display:flex;align-items:center;justify-content:space-between"><span class="pill" style="background:#fff;color:#0B0C0F;font-size:26px">${esc(d.kicker || 'Full time')}</span>
        <span class="dsp num" id="mclock" style="font-size:56px">KO</span></div>
      <div class="dsp" style="font-size:${T ? 84 : 72}px;margin-top:14px">${mwords(d.title)}</div></div>
    <div class="abs" id="mhero" style="left:60px;right:60px;top:${T ? 500 : 290}px;display:flex;align-items:center;gap:24px">
      ${chip(ft, 120)}<div><div id="mhl" style="font-size:30px;font-weight:800;color:var(--muted)">${esc(ft.short)} · before kick-off</div>
      <div id="mhv" class="dsp num" style="font-size:${T ? 170 : 140}px;line-height:1;color:${fs.color}">${pct(d.pre)}</div></div>
      <div style="margin-left:auto;text-align:right"><div style="font-size:26px;font-weight:800;color:var(--muted)">SCORE</div><div id="mscore" class="dsp num" style="font-size:96px;line-height:1">0-0</div></div></div>
    <svg class="abs" style="left:0;top:0" width="${S.w}" height="${S.h}"><defs><clipPath id="mclip"><rect id="mcr" x="0" y="0" width="${cx}" height="${S.h}"/></clipPath></defs>${grid}${ticks}${goals}${lines}</svg>
    <div class="abs" id="mleg" style="left:60px;right:60px;top:${cyT + ch + 70}px;display:flex;gap:26px;font-size:30px;font-weight:800">${Sx.map(s => `<span style="display:flex;align-items:center;gap:10px"><i style="width:30px;height:8px;border-radius:4px;background:${s.color};display:inline-block"></i>${esc(s.label)}</span>`).join('')}</div>
    <div class="abs" id="mgc" style="left:0;right:0;top:${cyT + ch * .18}px;text-align:center;opacity:0"><span id="mgct" class="dsp" style="display:inline-block;font-size:${T ? 58 : 50}px;background:#fff;color:#0B0C0F;padding:8px 28px;border-radius:14px;box-shadow:0 14px 40px rgba(0,0,0,.6)"></span></div>
    <div class="abs" id="mft" style="left:0;right:0;top:${cyT + ch * .25}px;text-align:center;opacity:0"><span class="dsp" style="display:inline-block;font-size:${T ? 120 : 100}px;background:#fff;color:#0B0C0F;padding:8px 36px;border-radius:20px;transform:rotate(-3deg);box-shadow:0 20px 60px rgba(0,0,0,.6)">FULL TIME ${esc(d.score)}</span></div>
    <div class="abs" id="mend" style="inset:0;background:rgba(11,12,15,.95);display:flex;flex-direction:column;justify-content:center;gap:34px;padding:0 70px;opacity:0">
      <div class="dsp" style="font-size:${T ? 112 : 96}px">${mk(d.endTitle || '')}</div>
      <div style="font-size:${T ? 42 : 38}px;font-weight:800;color:#C9CDD4">${esc(d.endSub || '')}</div>
      <div style="font-size:${T ? 44 : 40}px"><span class="box">${esc(d.cta || '')}</span></div></div>
    ${src2(d.src || ('Minute prices from Outcome.xyz · ' + (d.stamp || '')), T ? 1452 : 1300)}`, brandTag());
  const D0 = 1.4, D = d.drawDur || 11.5, tFT = D0 + D, tEnd = tFT + 2.2, dur = tEnd + 3.4;
  const vAt = tt => tt <= t0 ? 0 : (tt >= t1 ? 1 : (tt - t0) / (t1 - t0));
  const valAt = (s, tt) => { const P = s.pts; let v = P[0][1]; for (let j = 0; j < P.length; j++) { if (P[j][0] > tt) break; v = P[j][1]; } return v; };
  const minute = tt => { const m = (tt - d.ko) / 60000; if (m < 0) return 'KO'; if (m <= 47) return Math.max(1, Math.ceil(m)) + "'"; if (m < 62) return 'HT'; const m2 = Math.ceil(m - 17); return m2 > 90 ? "90+'" : m2 + "'"; };
  return {html, dur, build: tl => {
    tl.from('#mlh .pill', {scale: .5, opacity: 0, duration: f30(6), ease: 'back.out(2)'}, 0).from('#mlh .word', {yPercent: 110, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0.02);
    tl.from('#mhero', {y: 30, opacity: 0, duration: f30(7), ease: 'power3.out'}, 0.02); cue(0.03, 'whoosh', -10); cue(D0 - .1, 'whistle', -6); cue(D0, 'file:crowd_bed', -18);
    const o = {u: 0}; tl.to(o, {u: 1, duration: D, ease: 'none'}, D0);
    const score = [0, 0];
    d.goals.forEach((g, k) => { const at = D0 + D * vAt(g.t); tl.to('#mg' + k, {opacity: 1, duration: f30(4)}, at); impact(tl, at, {amp: 14, flash: .5, gain: -4, sub: false}); cue(at, 'roar', -9); });
    TICKS.push(t => {
      const tt = t0 + (t1 - t0) * o.u, x = X(tt); $('#mcr').setAttribute('width', Math.max(cx, x + 3));
      const fin = t >= tFT, last = s => s.pts[s.pts.length - 1][1];                 // after the whistle: the resolved values
      Sx.forEach((s, i) => { const h = $('#mh' + i); h.setAttribute('cx', x); h.setAttribute('cy', Y(fin ? last(s) : valAt(s, tt))); h.style.opacity = o.u > 0 ? 1 : 0; });
      let h_ = 0, a_ = 0; d.goals.forEach(g => { if (g.t <= tt && o.u > 0) { if (g.side === 'home') h_++; else a_++; } });
      $('#mscore').textContent = (t >= tFT ? d.score : h_ + '-' + a_);
      if (o.u > 0) { $('#mhv').textContent = pct(fin ? last(fs) : valAt(fs, tt)); $('#mhl').textContent = ft.short + ' · chance to win · ' + (t >= tFT ? 'FT' : minute(tt)); $('#mclock').textContent = t >= tFT ? 'FT' : minute(tt); }
      // goal caption: the latest goal for 1.3 s after it lands (pure function of t)
      let gc = null; d.goals.forEach(g => { const at = D0 + D * vAt(g.t); if (t >= at && t < at + 1.3 && t < tFT) gc = g; });
      const mgc = $('#mgc'); mgc.style.opacity = gc ? 1 : 0;
      if (gc) { const el = $('#mgct'); el.textContent = 'GOAL! ' + gc.label; el.style.background = Sx[gc.side === 'home' ? 0 : 2].color; el.style.color = lum(Sx[gc.side === 'home' ? 0 : 2].color) > .55 ? '#0B0C0F' : '#fff'; }
    });
    impact(tl, tFT, {amp: 18}); cue(tFT, 'whistle', -2);
    tl.set('#mft', {opacity: 1}, tFT).fromTo('#mft span', {scale: 2.2, rotation: -10}, {scale: 1, rotation: -3, duration: f30(9), ease: 'back.out(2)', immediateRender: false}, tFT);
    tl.to('#mend', {opacity: 1, duration: .35}, tEnd).from('#mend > *', {y: 40, opacity: 0, stagger: f30(4), duration: f30(9), ease: 'power3.out'}, tEnd + .1); cue(tEnd, 'whoosh', -8);
  }};
};

/* ---- Scoreboard: last night's favourites, one row per game, a tick or a cross lands on each (broadcast look) ---- */
F.scoreboard = d => {
  const T = tall(), R = d.rows, n = R.length, top = T ? 232 : 60, y0 = T ? 470 : 300, rh = Math.min(T ? 104 : 90, Math.floor(((T ? 1360 : 1180) - y0) / n) - 8);
  const rows = R.map((r, i) => `<div class="abs sbr" id="sb${i}" style="left:60px;right:60px;top:${y0 + i * (rh + 8)}px;height:${rh}px;border-radius:18px;background:var(--panel);border:2px solid var(--line);display:flex;align-items:center;gap:18px;padding:0 20px">
      ${chip(r.team, rh * .66)}<div style="flex:1;min-width:0"><div style="font-size:${rh * .34}px;font-weight:900;white-space:nowrap;overflow:hidden">${esc(r.line)}</div><div style="font-size:${rh * .24}px;font-weight:700;color:var(--muted)">${esc(r.sub)}</div></div>
      <div class="dsp num" style="font-size:${rh * .56}px;color:var(--muted)">${pct(r.p)}</div>
      <div class="sbm" style="width:${rh * .7}px;height:${rh * .7}px;border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:${rh * .46}px;font-weight:900;opacity:0;background:${r.ok ? 'var(--ok,#2BD576)' : 'var(--bad,#FF4D5E)'};color:#0B0C0F">${r.ok ? '&#10003;' : '&#10007;'}</div></div>`).join('');
  const html = wrap(`<div class="abs" style="inset:0;background:radial-gradient(80% 45% at 50% 0%,rgba(60,240,255,.14),transparent 70%),linear-gradient(180deg,#0A1F4A,#06122B 60%)"></div>
    <div class="abs" id="sbh" style="left:60px;right:60px;top:${top}px">
      <div><span class="pill" style="background:var(--acc);color:var(--on);font-size:28px">${esc(d.kicker || '')}</span></div>
      <div class="dsp" style="font-size:${T ? 96 : 84}px;margin-top:14px">${mwords(d.title)}</div></div>
    ${rows}
    <div class="abs" id="sbt" style="left:40px;right:40px;top:${y0 + n * (rh + 8) + 18}px;text-align:center;opacity:0"><span class="dsp" style="display:inline-block;font-size:${T ? 80 : 70}px;background:#fff;color:#06122B;padding:6px 30px;border-radius:16px">${esc(d.tally || '')}</span></div>
    ${src2(d.src, T ? 1470 : 1300)}`, brandTag());
  const t0 = 1.1, gap = .62, tT = t0 + n * gap + .3, dur = tT + 3.2;
  return {html, dur, build: tl => {
    tl.from('#sbh .pill', {scale: .5, opacity: 0, duration: f30(6), ease: 'back.out(2)'}, 0).from('#sbh .word', {yPercent: 110, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0.02);
    tl.from('.sbr', {x: -70, opacity: 0, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0.03); cue(0.04, 'whoosh', -10);
    R.forEach((r, i) => { const at = t0 + i * gap, m = '#sb' + i + ' .sbm';
      tl.set(m, {opacity: 1}, at).fromTo(m, {scale: 2.4, rotation: -20}, {scale: 1, rotation: 0, duration: f30(8), ease: 'back.out(2.2)', immediateRender: false}, at);
      if (!r.ok) { tl.fromTo('#sb' + i, {x: 0}, {x: 14, duration: f30(2), yoyo: true, repeat: 3, ease: 'none', immediateRender: false}, at); }
      cue(at, r.ok ? 'ding' : 'thud', r.ok ? -8 : -3); });
    tl.set('#sbt', {opacity: 1}, tT).fromTo('#sbt span', {scale: 2, rotation: -6}, {scale: 1, rotation: -2, duration: f30(9), ease: 'back.out(2)', immediateRender: false}, tT);
    impact(tl, tT, {amp: 12, flash: .3, punch: false, gain: -3, sub: false});
  }};
};
function cue(t, name, gain) { if (t >= 0) CUES.push([+t.toFixed(3), name, gain || 0]); }
window.getCues = () => CUES;
function rng(seed) { let s = (seed >>> 0) || 1; return () => { s = (Math.imul(s, 1664525) + 1013904223) >>> 0; return s / 4294967296; }; }
function applyLook(name) {
  const L = LOOKS[name] || LOOKS.night, st = $('#stage');
  for (const k in L) st.style.setProperty('--' + k, L[k]);
  st.style.background = L.bg; st.style.color = L.text; st.dataset.look = LOOKS[name] ? name : 'night';
  return L;
}
(function () {
  const s = document.createElement('style');
  s.textContent = `.dsp{font-family:var(--disp);font-weight:var(--dw);text-transform:uppercase;line-height:.95}
  .mask{display:inline-block;overflow:hidden;vertical-align:top;padding:0 .02em .08em;margin-bottom:-.08em}
  #stage[data-look] .lime{color:var(--acc)} #stage[data-look] .pink{color:var(--acc2)} #stage[data-look] .cyan{color:var(--acc3)}
  #stage[data-look=paper] .box{background:#141414;color:#fff} #stage[data-look=tabloid] .box{background:#0B0B0B;color:#FFE600}
  #stage[data-look=terminal] .box{background:var(--acc);color:#030603;font-family:var(--disp)}
  #stage[data-look=weather] .box{background:#fff;color:#0B2A66}
  .wxr .bar{height:12px;border-radius:6px;background:rgba(255,255,255,.22);overflow:hidden;margin-top:12px}
  .wxr .bar i{display:block;height:100%;border-radius:6px;background:linear-gradient(90deg,#A8E8FF,#FFD54A)}
  .rays{transform-box:fill-box;transform-origin:center;transform:rotate(var(--rot,0deg))}`;
  document.head.appendChild(s);
})();
function mwords(text, cls) { return words(text, cls).replace(/<span class="word/g, '<span class="mask"><span class="word').replace(/<\/span>/g, '</span></span>'); }
function brandTag() {
  const b = S.brand || {}, T = tall();
  return `<div class="abs" style="left:${T ? 64 : 48}px;top:${T ? 150 : 44}px;display:flex;align-items:center;gap:12px;font-weight:800;font-size:28px;color:var(--text);font-family:var(--text-font)"><div style="width:48px;height:48px;border-radius:50%;background:var(--acc);color:var(--on);display:flex;align-items:center;justify-content:center;font-family:var(--disp);font-weight:700;font-size:26px">${esc((b.name || '?').slice(0, 1))}</div>${esc(b.handle || '')}</div>`;
}
function src2(txt, y) {
  const T = tall();
  return `<div class="abs src2" style="left:60px;right:60px;top:${y || (T ? 1452 : 1290)}px;text-align:center;font-size:24px;color:var(--muted);font-weight:700;font-family:var(--text-font)">${esc(txt || ('Chances from Outcome.xyz market prices' + (S.stamp ? ' · ' + S.stamp : '')))}</div>`;
}
function shakeTick(t) {
  let x = 0, y = 0;
  for (const [at, amp] of SHAKES) { const i = (t - at) * 30; if (i >= 0 && i < 14) { const k = Math.pow(.78, i); x += k * amp * Math.sin(i * 2.1); y += k * amp * .7 * Math.cos(i * 2.7); } }
  gsap.set('#shake', {x, y});
}
/* impact = flash (1 frame full, fade 4) + punch scale + decaying shake + hit (+ sub), all on the same frame */
function impact(tl, at, o) {
  o = o || {};
  tl.set('#flash', {opacity: o.flash == null ? .85 : o.flash}, at).to('#flash', {opacity: 0, duration: f30(5), ease: 'none'}, at + f30(1));
  if (o.punch !== false) tl.fromTo('#shake', {scale: 1}, {scale: o.scale || 1.07, duration: f30(5), ease: 'power2.out', immediateRender: false}, at)
    .to('#shake', {scale: 1.0, duration: f30(12), ease: 'power2.inOut'}, at + f30(5));
  SHAKES.push([at, o.amp || 18]);
  if (!SHAKE_ON) { SHAKE_ON = true; TICKS.push(shakeTick); }
  cue(at, o.sound || 'hit', o.gain || 0);
  if (o.sub !== false) cue(at, 'sub', -5);
}
function scrambleIn(el, text, tl, at, dur, seed) {
  const o = {p: 0}; tl.to(o, {p: 1, duration: dur, ease: 'none'}, at);
  const G = 'ABCDEFGHJKLMNPQRSTUVWXYZ0123456789#%$&<>/';
  TICKS.push(t => {
    if (o.p <= 0) { el.textContent = ''; return; }
    const n = text.length, k = Math.floor(o.p * n), fr = Math.floor(t * 30); let s = '';
    for (let i = 0; i < n; i++) { const c = text[i]; if (i < k || c === ' ') s += c; else if (i < k + 6) s += G[Math.abs(i * 7919 + fr * 104729 + (seed || 1) * 31) % G.length]; }
    el.textContent = s;
  });
}
function wrap(inner, extra) { return `<div id="cam" class="abs" style="inset:0;transform-origin:50% 45%"><div id="shake" class="abs" style="inset:0">${inner}</div></div><div class="abs" id="flash" style="inset:0;background:#fff;opacity:0;pointer-events:none"></div>${extra || ''}`; }

/* ---- Countdown: the money's top N, revealed from the last place to the favourite (broadcast look) ---- */
F.countdown = d => {
  const T = tall(), it = d.items, n = it.length;
  const top = T ? 232 : 60, gap = T ? 8 : 6, boardY = T ? 548 : 330, rowH = Math.min(T ? 124 : 100, Math.floor(((T ? 1380 : 1200) - boardY - 70) / n) - gap);
  const cardTop = T ? 560 : 330, cardH = T ? 740 : 620, cardC = cardTop + cardH / 2;
  const yOf = k => boardY + k * (rowH + gap) + rowH / 2 - cardC;
  const rows = it.map((x, i) => {
    const y = boardY + i * (rowH + gap); const [c1] = cols(x.team || {name: x.label});
    return `<div class="abs cdrow" id="cr${i}" style="left:60px;right:60px;top:${y}px;height:${rowH}px;border-radius:18px;background:var(--panel);border:2px solid var(--line);overflow:hidden">
      <div class="abs cdwipe" style="inset:0;background:${c1};transform-origin:0 50%;transform:scaleX(0)"></div>
      <div class="abs" style="left:0;top:0;bottom:0;width:10px;background:${c1}"></div>
      <div class="abs dsp num" style="left:30px;top:0;bottom:0;display:flex;align-items:center;font-size:${rowH * .74}px;color:var(--muted)">${x.rank}</div>
      <div class="abs cdq dsp" style="left:122px;top:0;bottom:0;display:flex;align-items:center;font-size:${rowH * .62}px;color:var(--line)">? ? ?</div>
      <div class="abs cdin" style="left:112px;right:26px;top:0;bottom:0;display:flex;align-items:center;gap:18px;opacity:0">${x.team ? chip(x.team, rowH * .7) : ''}
        <div class="dsp" style="flex:1;font-size:${rowH * .62}px;white-space:nowrap;overflow:hidden">${esc(x.label)}</div>
        <div class="dsp num" style="font-size:${rowH * .74}px;color:${i === 0 ? 'var(--acc2)' : 'var(--acc)'}">${pct(x.p)}</div></div></div>`;
  }).join('');
  const cards = it.map((x, i) => {
    const [c1, c2] = cols(x.team || {name: x.label}); const fav = i === 0;
    const d24 = x.d24 != null && Math.abs(x.d24) >= .01 ? `<div class="abs" style="right:46px;bottom:74px;font-family:var(--text-font);font-size:40px;font-weight:900;padding:8px 22px;border-radius:999px;background:rgba(0,0,0,.38);color:${x.d24 >= 0 ? '#7CFFB2' : '#FF9DB0'}">${x.d24 >= 0 ? '▲' : '▼'} ${Math.abs(Math.round(x.d24 * 100))} pts in 24h</div>` : '';
    return `<div class="abs cdcard" id="cc${i}" style="left:60px;right:60px;top:${cardTop}px;height:${cardH}px;border-radius:40px;overflow:hidden;opacity:0;background:${c1};box-shadow:0 40px 120px rgba(0,0,0,.6)${fav ? ',0 0 0 8px var(--acc2)' : ''}">
      <div class="abs" style="inset:0;background:linear-gradient(160deg,rgba(255,255,255,.2),rgba(0,0,0,.4))"></div>
      <div class="abs dsp num" style="left:46px;top:24px;font-size:${T ? 230 : 200}px;color:${c2}">#${x.rank}</div>
      <div class="abs" style="right:46px;top:52px">${x.team ? chip(x.team, T ? 190 : 160) : ''}</div>
      ${fav ? `<div class="abs" style="left:50px;top:${T ? 262 : 232}px;font-family:var(--text-font);font-size:36px;font-weight:900;letter-spacing:.14em;color:${c2}">THE FAVOURITE</div>` : ''}
      <div class="abs dsp" style="left:46px;right:46px;bottom:${T ? 236 : 206}px;font-size:${x.label.length > 15 ? 104 : x.label.length > 10 ? 124 : 150}px;color:${c2}">${esc(x.label)}</div>
      <div class="abs dsp num cdv" style="left:46px;bottom:34px;font-size:${T ? 210 : 180}px;color:${c2}">0%</div>${d24}</div>`;
  }).join('');
  const html = wrap(`<div class="abs" style="inset:0;background:radial-gradient(80% 45% at 50% 0%,rgba(60,240,255,.2),transparent 70%),linear-gradient(180deg,#0A1F4A,#06122B 60%)"></div>
     <div class="abs" style="inset:0;background:repeating-linear-gradient(90deg,rgba(255,255,255,.025) 0 2px,transparent 2px 120px)"></div>
     <div class="abs" id="cdh" style="left:60px;right:60px;top:${top}px">
       <div><span class="pill" style="background:var(--acc);color:var(--on);font-size:28px">${esc(d.kicker || '')}</span></div>
       <div class="dsp" style="font-size:${T ? 104 : 92}px;margin-top:14px">${mwords(d.title)}</div></div>
     ${rows}${cards}
     <div class="abs" id="cdf" style="left:40px;right:40px;top:${boardY + n * (rowH + gap) + 14}px;font-size:38px;opacity:0;text-align:center;font-family:var(--text-font)"><span class="box">${esc(d.foot || '')}</span></div>
     ${src2(d.src)}`, brandTag());
  const HOLD = .82, FLY = .34, sched = []; let t_ = 1.0;
  for (let k = n - 1; k >= 1; k--) { sched[k] = t_; t_ += HOLD + FLY; }
  sched[0] = t_ + .9; const tEndC = sched[0] + 1.7 + .6, dur = d.dur || tEndC + 2.6;
  return {html, dur, build: tl => {
    tl.from('#cdh .pill', {scale: .5, opacity: 0, duration: f30(6), ease: 'back.out(2)'}, 0);
    tl.from('#cdh .word', {yPercent: 110, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0.02);
    tl.from('.cdrow', {x: -90, opacity: 0, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0.04);
    tl.fromTo('#cam', {scale: 1}, {scale: 1.035, duration: dur, ease: 'none'}, 0);
    cue(0.08, 'whoosh', -10);
    let t = tEndC;
    for (let k = n - 1; k >= 0; k--) {
      const at = sched[k], card = '#cc' + k, row = '#cr' + k, fav = k === 0;
      if (fav) { cue(at - 1.25, 'riser', -7); tl.to('.cdrow', {opacity: .55, duration: .3}, at - 1.0); }
      tl.set(card, {opacity: 1}, at).fromTo(card, {scale: fav ? 1.5 : 1.28, rotation: k % 2 ? -3 : 3}, {scale: 1, rotation: 0, duration: f30(fav ? 10 : 8), ease: 'back.out(1.5)', immediateRender: false}, at);
      const c = counter($(card + ' .cdv'), 0, it[k].p); c.tween(tl, at + .02, fav ? .9 : .24); TICKS.push(c.draw);
      if (fav) impact(tl, at, {amp: 22}); else cue(at, 'pop', -5);
      const hold = fav ? 1.7 : HOLD;
      tl.to(card, {scale: .22, y: yOf(k), opacity: 0, duration: f30(9), ease: 'power3.in'}, at + hold);
      cue(at + hold, 'whoosh', -13);
      tl.to(row + ' .cdwipe', {scaleX: 1, duration: f30(6), ease: 'power2.out'}, at + hold + f30(6))
        .to(row + ' .cdwipe', {scaleX: 0, transformOrigin: '100% 50%', duration: f30(8), ease: 'power2.in'}, at + hold + f30(13));
      tl.to(row + ' .cdq', {opacity: 0, duration: .1}, at + hold + f30(8)).to(row + ' .cdin', {opacity: 1, duration: f30(6)}, at + hold + f30(11));
      if (fav) tl.to('.cdrow', {opacity: 1, duration: .3}, at + hold);
    }
    tl.to('#cdf', {opacity: 1, duration: .01}, t).from('#cdf .box', {scale: .6, opacity: 0, duration: f30(9), ease: 'back.out(2)'}, t); cue(t, 'pop', -8);
    tl.fromTo('#cr0', {scale: 1}, {scale: 1.035, duration: f30(8), yoyo: true, repeat: 1, ease: 'power1.inOut'}, t + .5);
  }};
};

/* ---- Timer quiz: guess the favourite, a 3-second clock per round (tabloid look) ---- */
F.quizclock = d => {
  const T = tall(), R = d.rounds, n = R.length, cy = T ? 920 : 650;
  const side = (s, k) => `<div class="abs qside q${k}" style="left:${k ? 560 : 60}px;width:460px;top:${cy - 330}px;height:660px;display:flex;flex-direction:column;align-items:center;gap:20px">
      ${s.team ? chip(s.team, T ? 300 : 240) : ''}
      <div class="dsp" style="font-size:${s.label.length > 12 ? 48 : 60}px;text-align:center;line-height:1.02;max-width:440px">${esc(s.label)}</div>
      <div class="dsp num qv" style="font-size:${T ? 140 : 120}px;line-height:1">?</div></div>`;
  const rounds = R.map((r, i) => `<div class="abs qr" id="qr${i}" style="inset:0;opacity:${i ? 0 : 1}">${side(r.a, 0)}${side(r.b, 1)}
      <div class="abs qstamp" style="left:${(r.best ? 560 : 60) + 30}px;top:${cy - 390}px;width:400px;height:400px;opacity:0">
        <svg viewBox="0 0 400 400" width="400" height="400"><circle cx="200" cy="200" r="180" fill="none" stroke="var(--acc)" stroke-width="20" stroke-dasharray="1060 70"/></svg>
        <div class="abs dsp" style="left:50%;bottom:-16px;transform:translateX(-50%) rotate(-7deg);background:var(--acc);color:#fff;font-size:44px;padding:8px 24px;border-radius:8px;white-space:nowrap">FAVOURITE</div></div>
      <div class="abs qdraw" style="left:0;right:0;top:${cy + 350}px;text-align:center;font-size:40px;font-weight:900;opacity:0">${Math.round(r.a.p * 100) === Math.round(r.b.p * 100) ? 'By a hair! · ' : ''}Draw ${pct(r.draw)}</div>
      <div class="abs" style="left:0;right:0;top:${cy + 420}px;text-align:center;font-size:30px;font-weight:800;color:var(--muted)">${esc(r.meta || '')}</div></div>`).join('');
  const ends = R.map(r => { const f = r.best ? r.b : r.a; return `<div class="qe" style="display:flex;align-items:center;gap:18px;background:#fff;border:4px solid #0B0B0B;border-radius:18px;padding:12px 20px;box-shadow:8px 8px 0 #0B0B0B">${f.team ? chip(f.team, 70) : ''}<div style="flex:1;font-size:38px;font-weight:900">${esc(f.label)}</div><div class="dsp num" style="font-size:60px;color:var(--acc)">${pct(f.p)}</div></div>`; }).join('');
  const html = wrap(`<div class="abs" style="inset:0;background:var(--bg)"></div>
    <div class="abs" style="inset:0;background:repeating-linear-gradient(-45deg,rgba(0,0,0,.04) 0 22px,transparent 22px 44px)"></div>
    <div class="abs" id="qh" style="left:60px;right:60px;top:${T ? 232 : 60}px;display:flex;align-items:center;justify-content:space-between">
      <span class="dsp" style="background:#0B0B0B;color:#FFE600;font-size:${T ? 60 : 52}px;padding:12px 26px;transform:rotate(-2deg);display:inline-block">${esc(d.title || 'Guess the favourite')}</span>
      <span class="dsp num" id="qn" style="font-size:60px">1/${n}</span></div>
    <div class="abs" id="qsub" style="left:60px;right:60px;top:${T ? 352 : 160}px;font-size:34px;font-weight:800">${esc(d.sub || '')}</div>
    <div id="qrs">${rounds}</div>
    <div class="abs" id="qclock" style="left:${S.w / 2 - 105}px;top:${cy - 295}px;width:210px;height:210px">
      <svg width="210" height="210" style="position:absolute;inset:0"><circle cx="105" cy="105" r="92" fill="#0B0B0B"/><circle id="qring" cx="105" cy="105" r="92" fill="none" stroke="var(--acc)" stroke-width="16" stroke-linecap="round" transform="rotate(-90 105 105)" stroke-dasharray="578" stroke-dashoffset="0"/></svg>
      <div id="qd" class="abs dsp num" style="inset:0;display:flex;align-items:center;justify-content:center;font-size:92px;color:#FFE600">VS</div></div>
    <div class="abs" id="qend" style="left:60px;right:60px;top:${T ? 360 : 170}px;opacity:0;display:flex;flex-direction:column;gap:20px">
      <div class="dsp" style="font-size:${T ? 100 : 86}px;line-height:1">How many did you <span style="color:var(--acc)">get?</span></div>${ends}
      <div style="font-size:40px;font-weight:900;margin-top:6px"><span class="box">Comment your score out of ${n} 👇</span></div></div>
    ${src2()}`, brandTag());
  const plan = []; let s = 0;
  R.forEach((r, i) => { const L = i ? (d.clock2 || 2.5) : (d.clock || 3); const c0 = s + .55; plan.push({s, c0, L, rv: c0 + L}); s = c0 + L + 1.55; });
  const E = s, dur = E + 3.4;
  return {html, dur, build: tl => {
    tl.from('#qh > *', {y: -40, opacity: 0, stagger: f30(2), duration: f30(7), ease: 'power3.out'}, 0);
    R.forEach((r, i) => {
      const P = plan[i], qr = '#qr' + i;
      if (i) {
        tl.to('#qr' + (i - 1), {xPercent: -110, duration: f30(9), ease: 'power2.in'}, P.s - .3).set('#qr' + (i - 1), {opacity: 0}, P.s);
        tl.set(qr, {opacity: 1}, P.s - .02).fromTo(qr, {xPercent: 110}, {xPercent: 0, duration: f30(10), ease: 'power3.out', immediateRender: false}, P.s - .02);
        cue(P.s - .3, 'whoosh', -8);
      } else tl.from(qr + ' .qside', {y: 90, opacity: 0, stagger: f30(2), duration: f30(8), ease: 'power3.out'}, 0.02);
      tl.set('#qring', {attr: {'stroke-dashoffset': 0}}, P.s);
      tl.fromTo('#qclock', {scale: .3}, {scale: 1, duration: f30(8), ease: 'back.out(2.2)', immediateRender: false}, P.s + .12); cue(P.s + .12, 'thud', -6);
      tl.fromTo('#qring', {attr: {'stroke-dashoffset': 0}}, {attr: {'stroke-dashoffset': 578}, duration: P.L, ease: 'none', immediateRender: false}, P.c0);
      const tks = [P.c0]; for (let m = 1; m < Math.ceil(P.L); m++) tks.push(P.rv - m); tks.sort((a, b) => a - b).forEach((at, k) => { cue(at, k % 2 ? 'tock' : 'tick', -3); tl.fromTo('#qd', {scale: 1.45}, {scale: 1, duration: f30(8), ease: 'power3.out', immediateRender: false}, at); });
      cue(P.rv - .5, 'tick', -7); cue(P.rv - .25, 'tick', -7);
      tl.to('#qclock', {scale: 0, duration: f30(5), ease: 'power2.in'}, P.rv);
      tl.to(qr + ' .q' + (1 - r.best), {opacity: .3, duration: f30(8)}, P.rv + .05);
      tl.set(qr + ' .qstamp', {opacity: 1}, P.rv).fromTo(qr + ' .qstamp', {scale: 1.7, rotation: -14}, {scale: 1, rotation: 0, duration: f30(8), ease: 'back.out(2)', immediateRender: false}, P.rv);
      impact(tl, P.rv, {amp: 12, flash: .45, gain: -3, sub: false, sound: 'thud'}); cue(P.rv + .02, 'ding', -4);
      const vs = $$(qr + ' .qv'), tie = Math.round(r.a.p * 100) === Math.round(r.b.p * 100);   // same whole number: show a decimal so the stamp makes sense
      const f1 = v => tie ? (v * 100).toFixed(1) + '%' : pct(v);
      [r.a, r.b].forEach((x, k) => { const o = {v: 0}; tl.to(o, {v: x.p, duration: f30(22), ease: 'expo.out'}, P.rv + .05); TICKS.push(t => { vs[k].textContent = t < P.rv ? '?' : f1(o.v); }); });
      tl.to(qr + ' .qdraw', {opacity: 1, duration: f30(6)}, P.rv + .35);
    });
    tl.to('#qr' + (n - 1), {xPercent: -110, duration: f30(9), ease: 'power2.in'}, E - .3).to('#qsub', {opacity: 0, duration: .2}, E - .3);
    tl.to('#qend', {opacity: 1, duration: .01}, E).from('#qend > *', {x: 120, opacity: 0, stagger: f30(4), duration: f30(9), ease: 'power3.out'}, E);
    cue(E - .3, 'whoosh', -8); for (let k = 0; k < n + 2; k++) cue(E + k * f30(4), 'pop', -10);
    TICKS.push(t => {
      let txt = 'VS', ri = 0;
      for (let i = 0; i < plan.length; i++) { const P = plan[i]; if (t >= P.s - .05) ri = i; if (t >= P.c0 && t < P.rv) txt = String(Math.ceil(P.rv - t - 1e-6)); }
      $('#qd').textContent = txt; $('#qn').textContent = (ri + 1) + '/' + n;
    });
  }};
};

/* ---- Weather icons (our own SVG) ---- */
function wxIcon(kind, size) {
  const cloud = (x, y, w, fill, op) => `<g transform="translate(${x} ${y}) scale(${w / 100})" opacity="${op || 1}"><path d="M22 64 Q4 64 5 49 Q6 34 23 35 Q26 14 47 14 Q66 14 70 32 Q88 30 92 47 Q94 64 77 64 Z" fill="${fill}"/></g>`;
  const sun = (cx, cy, r) => `<g class="rays">${[...Array(8)].map((_, i) => `<rect x="${cx - r * .1}" y="${cy - r * 1.72}" width="${r * .2}" height="${r * .46}" rx="${r * .1}" fill="#FFD54A" transform="rotate(${i * 45} ${cx} ${cy})"/>`).join('')}</g><circle cx="${cx}" cy="${cy}" r="${r}" fill="#FFD54A"/><circle cx="${cx - r * .28}" cy="${cy - r * .28}" r="${r * .5}" fill="#FFE89A" opacity=".55"/>`;
  const bolt = (dx, dy, k) => `<path class="bolt" transform="translate(${dx} ${dy}) scale(${k})" d="M30 0 L8 38 L24 38 L14 70 L46 26 L30 26 L40 0 Z" fill="#FFD54A" stroke="#FFF6CC" stroke-width="2"/>`;
  const rain = `<g class="rain" stroke="#A8E8FF" stroke-width="4" stroke-linecap="round" opacity=".9"><line x1="30" y1="72" x2="25" y2="86"/><line x1="48" y1="72" x2="43" y2="86"/><line x1="66" y1="72" x2="61" y2="86"/></g>`;
  let g = '';
  if (kind === 'sun') g = sun(50, 50, 22);
  else if (kind === 'partly') g = sun(36, 38, 17) + cloud(20, 30, 78, '#F4F7FB');
  else if (kind === 'cloud') g = cloud(4, 8, 66, '#C9D3E3') + cloud(16, 26, 80, '#F4F7FB');
  else if (kind === 'rain') g = cloud(10, 6, 82, '#DCE3EE') + rain;
  else if (kind === 'storm') g = cloud(8, 4, 86, '#8D99B3') + bolt(36, 52, .62);
  else if (kind === 'bolt') g = bolt(18, 12, 1.15);
  return `<svg width="${size}" height="${size}" viewBox="0 0 100 100" style="overflow:visible;flex:none">${g}</svg>`;
}

/* ---- The football weather forecast (weather look) ---- */
F.forecast = d => {
  const T = tall(), H = d.hero, G = d.groups;
  const skyA = 'linear-gradient(180deg,#1A56CF 0%,#3F86EA 55%,#86BEF6 100%)', skyB = 'linear-gradient(180deg,#232B3B 0%,#3D485E 55%,#66748F 100%)', skyC = 'linear-gradient(180deg,#160D2E 0%,#35255E 55%,#5B4A8A 100%)';
  const bigClouds = [[-120, T ? 300 : 120, 520, .16], [520, T ? 620 : 420, 640, .12], [80, T ? 1180 : 900, 700, .1], [700, T ? 1520 : 1200, 520, .14]]
    .map((c, i) => `<div class="abs bcl" data-x="${c[0]}" data-sp="${14 + i * 6}" style="left:0;top:${c[1]}px;width:${c[2]}px;opacity:${c[3]}">${wxIcon('cloud', c[2]).replace('#C9D3E3', '#fff').replace('#F4F7FB', '#fff')}</div>`).join('');
  const rows = g => g.rows.map(r => `<div class="wxr" style="display:flex;align-items:center;gap:22px;padding:20px 0;border-top:1.5px solid rgba(255,255,255,.18)">
      <div style="width:118px;font-size:32px;font-weight:600;opacity:.9">${esc(r.time || '')}</div>${wxIcon(r.icon || g.icon, 92)}
      <div style="flex:1;min-width:0"><div style="font-size:40px;font-weight:700;white-space:nowrap;overflow:hidden">${esc(r.city)}</div><div style="font-size:28px;font-weight:500;opacity:.82;white-space:nowrap;overflow:hidden">${esc(r.line)}</div>
        <div class="bar"><i style="width:${Math.round(r.p * 100)}%"></i></div></div>
      <div class="num wxv" style="font-size:78px;font-weight:300;min-width:170px;text-align:right">${pct(r.p)}</div></div>`).join('');
  const scenes = G.map((g, i) => `<div class="abs wxs" id="wx${i + 1}" style="left:46px;right:46px;top:${T ? 300 : 120}px;opacity:0">
      <div style="display:flex;align-items:center;gap:20px;margin-bottom:24px">${wxIcon(g.icon, 120)}<div><div style="font-size:${T ? 76 : 66}px;font-weight:700;line-height:1">${esc(g.title)}</div><div style="font-size:34px;font-weight:500;opacity:.85;margin-top:8px">${esc(g.sub || '')}</div></div></div>
      <div style="background:rgba(255,255,255,.13);border:1.5px solid rgba(255,255,255,.24);border-radius:38px;padding:8px 32px 14px">
        <div style="font-size:25px;font-weight:700;letter-spacing:.09em;opacity:.75;padding:16px 0 10px">${esc(g.label || '')}</div>${rows(g)}</div></div>`).join('');
  const html = wrap(`<div class="abs" id="skyA" style="inset:0;background:${skyA}"></div><div class="abs" id="skyB" style="inset:0;opacity:0;background:${skyB}"></div><div class="abs" id="skyC" style="inset:0;opacity:0;background:${skyC}"></div>
    <div class="abs" id="glow" style="left:${S.w - 520}px;top:-260px;width:900px;height:900px;border-radius:50%;background:radial-gradient(circle,rgba(255,226,120,.45),transparent 65%)"></div>
    ${bigClouds}
    <div class="abs" id="rainfx" style="inset:-200px 0 0 0;opacity:0;background:repeating-linear-gradient(105deg,transparent 0 46px,rgba(200,230,255,.28) 46px 49px);"></div>
    <div class="abs" id="wx0" style="inset:0">
      <div class="abs" style="left:0;right:0;top:${T ? 236 : 70}px;text-align:center">
        <div style="font-size:32px;font-weight:600;letter-spacing:.06em;opacity:.88">${esc(d.when || '')}</div>
        <div style="font-size:${T ? 86 : 74}px;font-weight:500;margin-top:4px">${esc(H.city)}</div>
        <div class="num" id="wxbig" style="font-size:${T ? 320 : 270}px;font-weight:200;line-height:1;margin:-4px 0 0 40px">0%</div>
        <div style="font-size:${T ? 54 : 48}px;font-weight:600">${esc(H.cond)}</div>
        <div style="font-size:${T ? 36 : 32}px;font-weight:500;opacity:.86;margin-top:10px">${esc(H.sub || '')}</div></div>
      <div class="abs" id="wxhero" style="left:${S.w / 2 - 190}px;top:${T ? 960 : 740}px">${wxIcon(H.icon || 'sun', 380)}</div>
      <div class="abs" style="left:60px;right:60px;top:${T ? 1330 : 1130}px;text-align:center;font-size:34px;font-weight:600;background:rgba(255,255,255,.13);border:1.5px solid rgba(255,255,255,.24);border-radius:28px;padding:20px 24px">${esc(H.line || '')}</div></div>
    ${scenes}
    <div class="abs" id="wxend" style="left:60px;right:60px;top:${T ? 470 : 240}px;opacity:0;text-align:center">
      <div style="display:flex;justify-content:center;gap:24px;margin-bottom:20px">${wxIcon('sun', 150)}${wxIcon('storm', 150)}${wxIcon('bolt', 150)}</div>
      <div style="font-size:${T ? 84 : 72}px;font-weight:700;line-height:1.05">${mk(d.endTitle || 'Forecast check tomorrow morning')}</div>
      <div style="font-size:38px;font-weight:500;opacity:.88;margin:22px 0 40px">${esc(d.endSub || '')}</div>
      <div style="font-size:44px"><span class="box">${esc(d.cta || 'Make your call on Outcome.xyz')}</span></div></div>
    ${src2()}`, brandTag());
  const per = d.per || 4.2, t1 = d.heroDur || 4.0, ends = t1 + G.length * per, dur = ends + 3.6;
  return {html, dur, build: tl => {
    cue(0.02, 'chime', -6);
    tl.from('#wx0 .num', {scale: .85, opacity: 0, duration: f30(8), ease: 'power3.out'}, 0.0);
    const c = counter($('#wxbig'), 0, H.p); c.tween(tl, 0, .42); TICKS.push(c.draw);
    tl.from('#wxhero', {y: 120, opacity: 0, duration: f30(12), ease: 'power3.out'}, 0.0);
    tl.fromTo('#cam', {scale: 1}, {scale: 1.03, duration: t1, ease: 'none'}, 0);
    tl.to('#wx0', {y: -260, opacity: 0, duration: f30(9), ease: 'power2.in'}, t1 - .25); cue(t1 - .28, 'whoosh', -8);
    G.forEach((g, i) => {
      const at = t1 + i * per, id = '#wx' + (i + 1);
      if (i) { tl.to('#wx' + i, {y: -260, opacity: 0, duration: f30(9), ease: 'power2.in'}, at - .25); cue(at - .28, 'whoosh', -8); }
      const sky = g.sky || 'A';
      tl.to('#skyB', {opacity: sky === 'B' ? 1 : 0, duration: .5}, at - .2).to('#skyC', {opacity: sky === 'C' ? 1 : 0, duration: .5}, at - .2).to('#glow', {opacity: sky === 'A' ? 1 : 0, duration: .5}, at - .2);
      tl.to('#rainfx', {opacity: sky === 'B' ? 1 : 0, duration: .4}, at - .1);
      tl.set(id, {opacity: 1}, at - .05).fromTo(id, {y: 260}, {y: 0, duration: f30(11), ease: 'power3.out', immediateRender: false}, at - .05);
      tl.from(id + ' .wxr', {x: 80, opacity: 0, stagger: f30(5), duration: f30(9), ease: 'power3.out'}, at + .25);
      $$(id + ' .wxr').forEach((rw, k) => { cue(at + .25 + k * f30(5), 'pop', -10); const el = rw.querySelector('.wxv'); const cc = counter(el, 0, g.rows[k].p); cc.tween(tl, at + .3 + k * f30(5), .8); TICKS.push(cc.draw); tl.from(rw.querySelector('.bar i'), {width: 0, duration: .8, ease: 'power2.out'}, at + .3 + k * f30(5)); });
      if (g.fx === 'thunder') impact(tl, at + .15, {amp: 16, flash: .9, sound: 'thunder', gain: -1, sub: false});
      if (g.fx === 'bolt') impact(tl, at + .15, {amp: 14, flash: .8, sound: 'crack', gain: -2});
      tl.fromTo('#cam', {scale: 1}, {scale: 1.03, duration: per, ease: 'none', immediateRender: false}, at);
    });
    tl.to('#wx' + G.length, {y: -260, opacity: 0, duration: f30(9), ease: 'power2.in'}, ends - .25); cue(ends - .28, 'whoosh', -8);
    tl.to(['#skyB', '#skyC', '#rainfx'], {opacity: 0, duration: .5}, ends - .2).to('#glow', {opacity: 1, duration: .5}, ends - .2);
    tl.to('#wxend', {opacity: 1, duration: .01}, ends).from('#wxend > *', {y: 60, opacity: 0, stagger: f30(5), duration: f30(10), ease: 'power3.out'}, ends);
    cue(ends + .1, 'chime', -8);
    const st = $('#stage'), bc = $$('.bcl'), rf = $('#rainfx');
    TICKS.push(t => {
      st.style.setProperty('--rot', (t * 24) + 'deg');
      bc.forEach(el => { const x0 = +el.dataset.x, sp = +el.dataset.sp; el.style.transform = `translateX(${((x0 + t * sp + 900) % (S.w + 900)) - 700}px)`; });
      rf.style.transform = `translate(${-(t * 120) % 49}px,${(t * 900) % 300}px)`;
    });
  }};
};

/* ---- The race: club balls race up a track; the finishing order is a draw weighted by the real chances (neon look) ---- */
F.race = d => {
  const T = tall(), B = d.balls, n = B.length, W = S.w, Hh = S.h;
  const L = d.len || 6000, T0 = d.t0 || 2.4, Dr = d.dr || 10.5;
  const lane = (W - 140) / n, x0 = 70, R = Math.min(46, lane * .34);
  const Ystart = Hh - (T ? 520 : 260), Ylead = T ? 860 : 560;
  const rk = {}; d.order.forEach((bi, k) => { rk[bi] = k; });
  const rnd = rng(d.seed || 7);
  const par = B.map((b, i) => {
    const k = rk[i]; let a1 = (rnd() * 2 - 1) * .04, a2 = (rnd() * 2 - 1) * .02, a3 = (rnd() * 2 - 1) * .01;
    if (k === 0) a1 = -.05 - rnd() * .015; if (k === 1) a1 = .05 + rnd() * .015;
    return {a1, a2, a3, D: Dr * (1 + .02 * k + (k ? .006 * rnd() : 0))};
  });
  const cw = .12, warp = u => u <= 0 ? 0 : (u < cw ? u * u / (2 * cw) : u - cw / 2) / (1 - cw / 2);
  const g = (p, u) => { const w = warp(Math.min(1, u)); return w + p.a1 * Math.sin(Math.PI * w) + p.a2 * Math.sin(2 * Math.PI * w) + p.a3 * Math.sin(3 * Math.PI * w); };
  const pos = (i, rt) => { const p = par[i], u = (rt - T0) / p.D; if (u <= 0) return 0; if (u <= 1) return L * g(p, u); return L + (1 - Math.exp(-(u - 1) * 6)) * 130; };
  const A = T0 + Dr - .7, SL = .38, SPAN = 1.15;
  const rtime = t => t < A ? t : (t < A + SPAN / SL ? A + (t - A) * SL : t - SPAN / SL + SPAN);
  const tFin = A + .7 / SL, tEnd = tFin + 2.6, dur = tEnd + 4.8;
  const camOf = rt => { let m = 0; for (let i = 0; i < n; i++) m = Math.max(m, pos(i, rt)); return Math.max(0, m - (Ystart - Ylead)); };
  const marks = [0, .25, .5, .75, 1].map(f => ({d: L * f, lab: f === 0 ? 'START' : f === 1 ? 'FINISH' : Math.round(f * 400) + ' M'}));
  const trackH = L + 2600, trackTop0 = Ystart - (L + 1300);
  const ballHtml = B.map((b, i) => { const [c1, c2] = cols(b.team || {name: b.label}); const code = ((b.team && b.team.code) || b.label.slice(0, 3)).toUpperCase();
    return `<div class="abs rtrail" id="tr${i}" style="left:${x0 + lane * (i + .5) - R * .7}px;top:0;width:${R * 1.4}px;height:10px;border-radius:${R}px;background:linear-gradient(180deg,${c1}dd,${c1}00);opacity:.9"></div>
      <div class="abs rball" id="b${i}" style="left:${x0 + lane * (i + .5) - R}px;top:0;width:${2 * R}px;height:${2 * R}px;border-radius:50%;background:radial-gradient(circle at 35% 30%,rgba(255,255,255,.55),transparent 42%),${c1};border:6px solid ${c2};box-shadow:0 0 28px ${c1},0 0 60px ${c1}88;display:flex;align-items:center;justify-content:center;font-family:var(--disp);font-size:${R * .62}px;color:${c2}">${esc(code)}</div>
      <div class="abs rlab" id="lb${i}" style="left:${x0 + lane * i}px;width:${lane}px;top:0;text-align:center"><div style="font-size:${lane > 150 ? 30 : 26}px;font-weight:900;line-height:1.05">${esc(b.label)}</div><div class="dsp num" style="font-size:44px;color:var(--acc3)">${pct(b.p)}</div></div>
      <div class="abs rpos" id="rp${i}" style="left:${x0 + lane * (i + .5) + R * .55}px;top:0;width:44px;height:44px;border-radius:50%;background:#fff;color:#0D0221;font-family:var(--disp);font-size:28px;display:flex;align-items:center;justify-content:center;opacity:0">1</div>`; }).join('');
  const realRows = [...B].sort((a, b) => b.p - a.p).map(b => `<div class="rr2" style="display:flex;align-items:center;gap:18px">${b.team ? chip(b.team, 72) : ''}<div style="flex:1;font-size:40px;font-weight:900">${esc(b.label)}</div><div class="dsp num" style="font-size:70px;color:var(--acc3)">${pct(b.p)}</div></div>`).join('');
  const html = wrap(`<div class="abs" style="inset:0;background:radial-gradient(70% 40% at 50% 0%,rgba(255,43,214,.25),transparent 70%),linear-gradient(180deg,#14032E,#0D0221)"></div>
    <div class="abs" id="track" style="left:0;right:0;top:${trackTop0}px;height:${trackH}px">
      <div class="abs" style="left:${x0}px;width:${W - 2 * x0}px;top:0;bottom:0;background:repeating-linear-gradient(0deg,rgba(255,43,214,.16) 0 3px,transparent 3px 140px),rgba(255,255,255,.025)"></div>
      ${[...Array(n + 1)].map((_, i) => `<div class="abs" style="left:${x0 + lane * i - 2}px;top:0;bottom:0;width:4px;background:${i === 0 || i === n ? 'var(--acc)' : 'rgba(41,240,255,.35)'};box-shadow:${i === 0 || i === n ? '0 0 18px var(--acc)' : 'none'}"></div>`).join('')}
      ${marks.map(m => `<div class="abs" style="left:${x0}px;width:${W - 2 * x0}px;top:${L + 1300 - m.d - (m.lab === 'FINISH' ? 30 : 3)}px;height:${m.lab === 'FINISH' ? 60 : 6}px;background:${m.lab === 'FINISH' ? 'repeating-conic-gradient(#fff 0 25%,#0D0221 0 50%) 0 0/30px 30px' : 'rgba(255,255,255,.35)'}"></div>
         <div class="abs dsp" style="left:${x0 + 10}px;top:${L + 1300 - m.d - (m.lab === 'FINISH' ? 100 : 60)}px;font-size:${m.lab === 'FINISH' ? 58 : 40}px;color:${m.lab === 'FINISH' ? '#fff' : 'rgba(255,255,255,.5)'}">${m.lab}</div>`).join('')}
    </div>
    ${ballHtml}
    <div class="abs" style="left:0;right:0;top:0;height:${T ? 470 : 260}px;background:linear-gradient(180deg,#0D0221 55%,rgba(13,2,33,0))"></div>
    <div class="abs" id="rh" style="left:60px;right:60px;top:${T ? 226 : 50}px">
      <div style="display:flex;gap:12px"><span class="pill" style="background:var(--acc);color:#fff;font-size:28px">${esc(d.kicker || 'Race #1')}</span></div>
      <div class="dsp" style="font-size:${T ? 84 : 70}px;margin-top:12px">${mwords(d.title)}</div></div>
    <div class="abs" id="rlead" style="left:60px;right:60px;top:${T ? 470 : 280}px;font-size:36px;font-weight:900;opacity:0">LEADER: <span id="rln" class="dsp" style="font-size:52px"></span></div>
    <div class="abs dsp num" id="rgo" style="left:0;right:0;top:${T ? 760 : 560}px;text-align:center;font-size:260px;color:var(--acc3);opacity:0;text-shadow:0 0 40px var(--acc3)">3</div>
    <div class="abs" id="rcap" style="left:40px;right:40px;top:${T ? 560 : 360}px;text-align:center;font-size:52px;opacity:0"><span class="box" id="rcapt"></span></div>
    <div class="abs" id="rwin" style="left:0;right:0;top:${T ? 780 : 560}px;text-align:center;opacity:0"><span class="dsp" style="display:inline-block;font-size:${T ? 130 : 110}px;background:#fff;color:#0D0221;padding:10px 34px;border-radius:20px;transform:rotate(-4deg);box-shadow:0 0 60px var(--acc)">${esc(B[d.order[0]].label)} win!</span></div>
    <div class="abs" id="rend" style="left:50px;right:50px;top:${T ? 300 : 110}px;opacity:0;background:rgba(13,2,33,.95);border:2px solid var(--line);border-radius:34px;padding:38px;display:flex;flex-direction:column;gap:20px">
      <div class="dsp" style="font-size:${T ? 76 : 66}px">The real race, <span style="color:var(--acc)">says the money</span></div>${realRows}
      <div style="font-size:30px;font-weight:700;color:var(--muted);line-height:1.3">${esc(d.note || '')}</div>
      <div style="font-size:42px;margin-top:6px"><span class="box">${esc(d.cta || 'Race #2 tomorrow. Who wins it? 👇')}</span></div></div>
    <div id="rsrc" style="opacity:0">${src2(d.src, T ? 1440 : 1300)}</div>`, brandTag());
  // leader changes (sampled once at build time) -> captions + whooshes
  const ev = []; let last = -1, lastT = -9;
  for (let t = T0 + .8; t < tFin - .2; t += 1 / 30) { const rt = rtime(t); let li = 0; for (let i = 1; i < n; i++) if (pos(i, rt) > pos(li, rt)) li = i; if (li !== last) { if (last >= 0 && t - lastT > 1.6) { ev.push({t, i: li}); lastT = t; } last = li; } }
  const caps = ev.slice(0, 3).map(e => ({t: e.t, txt: B[e.i].label + ' take the lead!'}));
  if (tFin - 1.4 > (caps.length ? caps[caps.length - 1].t + 1.5 : 0)) caps.push({t: tFin - 1.4, txt: 'Photo finish...'});
  return {html, dur, build: tl => {
    tl.from('#rh .pill', {scale: .5, opacity: 0, duration: f30(6), ease: 'back.out(2)'}, 0).from('#rh .word', {yPercent: 110, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0.02);
    tl.from('.rball', {scale: 0, duration: f30(8), stagger: f30(1), ease: 'back.out(2)'}, 0.02); cue(0.05, 'whoosh', -10);
    ['3', '2', '1'].forEach((k, j) => { const at = T0 - 1.5 + j * .5; tl.set('#rgo', {opacity: 1}, at).fromTo('#rgo', {scale: 1.5}, {scale: 1, duration: f30(8), ease: 'power3.out', immediateRender: false}, at); cue(at, 'beep', -6); });
        tl.set('#rgo', {opacity: 1}, T0).fromTo('#rgo', {scale: 1.6}, {scale: 1, duration: f30(8), ease: 'power3.out', immediateRender: false}, T0).to('#rgo', {opacity: 0, duration: f30(8)}, T0 + .45);
    cue(T0, 'beephi', -4); cue(T0, 'whoosh', -6);
    tl.to('.rlab', {opacity: 0, duration: f30(8)}, T0 + .2).to('#rlead', {opacity: 1, duration: f30(8)}, T0 + .6).to('.rpos', {opacity: 1, duration: f30(8)}, T0 + .6);
    caps.forEach(c => { tl.set('#rcapt', {textContent: c.txt}, c.t).to('#rcap', {opacity: 1, duration: f30(4)}, c.t).fromTo('#rcap .box', {scale: .7}, {scale: 1, duration: f30(8), ease: 'back.out(2)', immediateRender: false}, c.t).to('#rcap', {opacity: 0, duration: f30(6)}, c.t + 1.1); cue(c.t, c.txt.startsWith('Photo') ? 'riser' : 'whoosh', c.txt.startsWith('Photo') ? -8 : -9); });
    impact(tl, tFin, {amp: 22});
    tl.set('#rwin', {opacity: 1}, tFin + .05).fromTo('#rwin span', {scale: 2.2, rotation: -12}, {scale: 1, rotation: -4, duration: f30(9), ease: 'back.out(2)', immediateRender: false}, tFin + .05);
    tl.to('#rwin', {opacity: 0, duration: .3}, tEnd - .3).to('#rlead', {opacity: 0, duration: .3}, tEnd - .3);
    tl.to('#rsrc', {opacity: 1, duration: .25}, tEnd).to('#rend', {opacity: 1, duration: .25}, tEnd).from('#rend > *', {y: 50, opacity: 0, stagger: f30(4), duration: f30(9), ease: 'power3.out'}, tEnd + .05); cue(tEnd, 'whoosh', -8);
    $$('#rend .rr2').forEach((r, k) => cue(tEnd + .05 + (k + 1) * f30(4), 'pop', -11));
    const balls = $$('.rball'), trails = $$('.rtrail'), labs = $$('.rlab'), rps = $$('.rpos'), track = $('#track'), rln = $('#rln');
    TICKS.push(t => {
      const rt = rtime(t), cam = camOf(rtime(Math.min(t, tFin))), dt = 1 / 30;
      track.style.transform = `translateY(${cam}px)`; // cam stops when the winner crosses
      const ps = B.map((_, i) => pos(i, rt)); const order = ps.map((p, i) => [p, i]).sort((a, b) => b[0] - a[0]);
      B.forEach((_, i) => {
        const y = Ystart - (ps[i] - cam) - R; balls[i].style.transform = `translateY(${y}px)`;
        const v = Math.max(0, (pos(i, rtime(t + dt)) - ps[i]) / dt); const len = Math.min(320, v * .16);
        trails[i].style.transform = `translateY(${y + R}px)`; trails[i].style.height = len + 'px';
        labs[i].style.transform = `translateY(${y - 120}px)`;
        rps[i].style.transform = `translateY(${y - 34}px)`; rps[i].textContent = order.findIndex(o => o[1] === i) + 1;
      });
      const li = order[0][1]; rln.textContent = B[li].label; rln.style.color = cols(B[li].team || {name: B[li].label})[0] === '#FFFFFF' ? '#fff' : 'var(--acc3)';
    });
  }};
};

/* ---- 100 parallel matches: the same game played 100 times, then sorted (paper look) ---- */
F.sim100 = d => {
  const T = tall(), G = d.groups, seq = d.seq;
  const cs = T ? 68 : 56, gp = T ? 6 : 5, gw = 10 * cs + 9 * gp, gx = (S.w - gw) / 2, gy = T ? 486 : 300;
  const order = seq.map((g, k) => ({g, k})); // k = reveal order = random cell position
  const posOf = idx => [gx + (idx % 10) * (cs + gp), gy + Math.floor(idx / 10) * (cs + gp)];
  const rnd = rng(d.seed || 11); const cellAt = [...Array(100).keys()]; for (let i = 99; i > 0; i--) { const j = Math.floor(rnd() * (i + 1)); [cellAt[i], cellAt[j]] = [cellAt[j], cellAt[i]]; }
  const sorted = [...Array(100).keys()].sort((a, b) => seq[a] - seq[b] || a - b); const target = {}; sorted.forEach((k, idx) => { target[k] = idx; });
  const pitch = `<svg class="abs" width="${cs}" height="${cs}" viewBox="0 0 100 100" style="left:0;top:0"><rect x="8" y="8" width="84" height="84" rx="6" fill="none" stroke="currentColor" stroke-width="4"/><line x1="8" y1="50" x2="92" y2="50" stroke="currentColor" stroke-width="4"/><circle cx="50" cy="50" r="13" fill="none" stroke="currentColor" stroke-width="4"/></svg>`;
  const cells = order.map(o => { const [x, y] = posOf(cellAt[o.k]); return `<div class="abs sc" id="sc${o.k}" style="left:${x}px;top:${y}px;width:${cs}px;height:${cs}px;border-radius:12px;background:#fff;color:#D9D2C3;border:2px solid #E2DBCD">${pitch}<div class="abs scf" style="inset:-2px;border-radius:12px;background:${G[o.g].color};opacity:0"></div><div class="abs scw" style="inset:0;color:rgba(255,255,255,.55);opacity:0">${pitch}</div></div>`; }).join('');
  const legend = G.map((g, i) => `<div class="lg2" style="display:flex;flex-direction:column;align-items:center;gap:4px;flex:1"><div class="num sv${i}" style="font-family:var(--disp);font-weight:900;font-size:${T ? 92 : 76}px;line-height:1;color:${g.color === '#9A948A' ? '#6B655A' : g.color}">0</div><div style="font-size:30px;font-weight:800;text-align:center">${esc(g.label)}</div></div>`).join('');
  const T0 = 1.4, D = 6.2, tk = k => T0 + D * Math.sqrt((k + 1) / 100), tSort = T0 + D + .9, tFoot = tSort + 1.6, dur = tFoot + 3.6;
  const html = wrap(`<div class="abs" style="inset:0;background:#F3EFE6"></div>
    <div class="abs" style="inset:0;background-image:radial-gradient(rgba(20,20,20,.06) 1.5px,transparent 1.5px);background-size:26px 26px"></div>
    <div class="abs" id="sh" style="left:60px;right:60px;top:${T ? 232 : 60}px">
      <div style="font-size:30px;font-weight:800;letter-spacing:.08em;color:var(--acc);text-transform:uppercase">${esc(d.kicker || '')}</div>
      <div class="dsp" style="font-size:${T ? 92 : 80}px;margin-top:10px;text-transform:none;letter-spacing:-.02em">${mwords(d.title)}</div></div>
    ${cells}
    <div class="abs" id="sm1" style="left:${gx}px;top:${gy - 64}px;font-size:32px;font-weight:900;opacity:0"><span class="box" id="sm1t"></span></div>
    <div class="abs" id="sleg" style="left:60px;right:60px;top:${gy + gw + 22}px;display:flex;gap:10px">${legend}</div>
    <div class="abs" id="sfoot" style="left:40px;right:40px;top:${gy + gw + (T ? 168 : 140)}px;text-align:center;font-size:40px;opacity:0"><span class="box">${esc(d.foot || '')}</span></div>
    ${src2(d.src, T ? 1452 : 1300)}`, brandTag());
  return {html, dur, build: tl => {
    tl.from('#sh > *', {y: 40, opacity: 0, stagger: f30(2), duration: f30(7), ease: 'power3.out'}, 0);
    tl.from('#sh .word', {yPercent: 110, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0.02);
    tl.from('.sc', {scale: .6, opacity: 0, duration: f30(6), stagger: .0022, ease: 'power2.out'}, 0.02);
    tl.fromTo('#cam', {scale: 1}, {scale: 1.03, duration: dur, ease: 'none'}, 0);
    cue(0.05, 'whoosh', -10);
    const counts = G.map(() => 0), firsts = d.firsts || [];
    order.forEach(o => {
      const at = tk(o.k), id = '#sc' + o.k;
      tl.to(id + ' .scf', {opacity: 1, duration: f30(3)}, at).to(id + ' .scw', {opacity: 1, duration: f30(3)}, at).fromTo(id, {scale: 1.35}, {scale: 1, duration: f30(7), ease: 'back.out(2)', immediateRender: false}, at);
      if (o.k < 3) { tl.set('#sm1t', {textContent: 'Game ' + (o.k + 1) + ': ' + G[o.g].short}, at).set('#sm1', {opacity: 1}, at).fromTo('#sm1', {x: posOf(cellAt[o.k])[0] - gx}, {x: posOf(cellAt[o.k])[0] - gx, duration: .01, immediateRender: false}, at); cue(at, 'pop', -6); }
      else if (o.k < 40 || o.k % 3 === 0) cue(at, 'click', -16);
    });
    tl.to('#sm1', {opacity: 0, duration: .2}, tk(3) + .2);
    G.forEach((g, i) => { const el = $('.sv' + i); TICKS.push(t => { let c = 0; for (const o of order) if (o.g === i && t >= tk(o.k)) c++; el.textContent = c; }); });
    // sort into blocks so the split is visible at a glance
    order.forEach(o => { const [x1, y1] = posOf(cellAt[o.k]), [x2, y2] = posOf(target[o.k]); tl.to('#sc' + o.k, {x: x2 - x1, y: y2 - y1, duration: f30(16), ease: 'power3.inOut'}, tSort + (target[o.k] % 10) * .012); });
    cue(tSort - .05, 'whoosh', -6);
    impact(tl, tSort + .62, {amp: 8, flash: .25, punch: false, gain: -6, sub: false, sound: 'thud'});
    const hl = d.highlight; if (hl != null) order.filter(o => o.g === hl).forEach(o => tl.fromTo('#sc' + o.k, {scale: 1}, {scale: 1.12, duration: f30(7), yoyo: true, repeat: 1, ease: 'power1.inOut', immediateRender: false}, tFoot - .2));
    tl.to('#sfoot', {opacity: 1, duration: .01}, tFoot).from('#sfoot .box', {scale: .6, opacity: 0, duration: f30(9), ease: 'back.out(2)'}, tFoot); cue(tFoot, 'pop', -6);
  }};
};

/* ---- Line story: one chart, the line draws itself with a live head and the number that matters (terminal look) ---- */
F.linestory = d => {
  const T = tall(), Sx = d.series, cx = 90, cw = S.w - 190, cyT = T ? 790 : 540, ch = T ? 430 : 360;
  const t0 = Sx[0].pts[0][0], t1 = Sx[0].pts[Sx[0].pts.length - 1][0];
  const X = t => cx + (t - t0) / ((t1 - t0) || 1) * cw, Y = p => cyT + ch - p * ch;
  const path = s => s.pts.map((p, i) => (i ? 'L' : 'M') + X(p[0]).toFixed(1) + ' ' + Y(p[1]).toFixed(1)).join(' ');
  const grid = [0, .25, .5, .75, 1].map(v => `<line x1="${cx}" x2="${cx + cw}" y1="${Y(v)}" y2="${Y(v)}" stroke="rgba(57,255,20,.16)" stroke-width="2" stroke-dasharray="${v === .5 ? '0' : '6 10'}"/><text x="${cx - 14}" y="${Y(v) + 9}" fill="#5FA35F" font-size="26" text-anchor="end" font-family="LookMono,Consolas">${Math.round(v * 100)}</text>`).join('');
  const xl = (d.xLabels || []).map(l => `<text x="${X(l[0])}" y="${cyT + ch + 46}" fill="#5FA35F" font-size="26" text-anchor="middle" font-family="LookMono,Consolas">${esc(l[1])}</text>`).join('');
  const ghosts = Sx.map(s => `<path d="${path(s)}" fill="none" stroke="${s.color}" stroke-width="5" stroke-linejoin="round" opacity=".16"/>`).join('');
  const lines = Sx.map((s, i) => `<path id="ln${i}" d="${path(s)}" fill="none" stroke="${s.color}" stroke-width="7" stroke-linejoin="round" stroke-linecap="round" clip-path="url(#lclip)" style="filter:drop-shadow(0 0 8px ${s.color})"/>
      <circle id="hd${i}" r="13" fill="${s.color}"/><circle id="hr${i}" r="13" fill="none" stroke="${s.color}" stroke-width="4"/>
      <g id="hl${i}"><rect x="18" y="-26" width="${s.label.length * 19 + 120}" height="48" rx="8" fill="#030603" stroke="${s.color}" stroke-width="2"/><text x="32" y="9" fill="${s.color}" font-size="28" font-weight="700" font-family="LookMono,Consolas"><tspan>${esc(s.label.toUpperCase())}</tspan> <tspan class="hv">0%</tspan></text></g>`).join('');
  const ev = d.event ? `<g id="evp" opacity="0"><line x1="${X(d.event.t)}" x2="${X(d.event.t)}" y1="${cyT - 20}" y2="${cyT + ch}" stroke="var(--acc3)" stroke-width="3" stroke-dasharray="8 8"/><rect x="${X(d.event.t) - 150}" y="${cyT - 76}" width="300" height="50" rx="8" fill="var(--acc3)"/><text x="${X(d.event.t)}" y="${cyT - 40}" fill="#030603" font-size="28" font-weight="800" text-anchor="middle" font-family="LookMono,Consolas">${esc(d.event.label)}</text></g>` : '';
  const html = wrap(`<div class="abs" style="inset:0;background:radial-gradient(90% 60% at 50% 40%,#0A180A,#030603 75%)"></div>
    <div class="abs" id="lh" style="left:60px;right:60px;top:${T ? 228 : 50}px;font-family:var(--disp)">
      <div style="font-size:28px;color:var(--muted);font-weight:700">&gt;_ ${esc(d.kicker || '')}</div>
      <div id="ltitle" style="font-size:${T ? 76 : 64}px;font-weight:800;line-height:1.05;margin-top:12px;min-height:${T ? 160 : 136}px;text-transform:uppercase"></div></div>
    <div class="abs" id="lbig" style="left:60px;right:60px;top:${T ? 470 : 260}px;display:flex;align-items:flex-end;gap:26px;font-family:var(--disp)">
      <div><div style="font-size:28px;color:var(--muted);font-weight:700">${esc(d.heroLabel || '')}</div><div id="lnum" class="num" style="font-size:${T ? 200 : 170}px;font-weight:800;line-height:.95;color:var(--acc)">${pct(Sx[0].pts[Sx[0].pts.length - 1][1])}</div></div>
      <div id="ldelta" style="margin-bottom:26px;font-size:40px;font-weight:800;background:var(--acc);color:#030603;padding:8px 18px;border-radius:8px;opacity:0">${esc(d.delta || '')}</div></div>
    <svg class="abs" style="left:0;top:0" width="${S.w}" height="${S.h}"><defs><clipPath id="lclip"><rect id="lcr" x="0" y="0" width="${cx}" height="${S.h}"/></clipPath></defs>${grid}${xl}${ghosts}${ev}${lines}<text id="ldt" x="0" y="${cyT + ch + 46}" fill="var(--acc3)" font-size="28" font-weight="800" text-anchor="middle" font-family="LookMono,Consolas"></text></svg>
    <div class="abs" id="lfoot" style="left:60px;right:60px;top:${cyT + ch + 84}px;font-family:var(--disp);opacity:0">
      <div style="font-size:${T ? 40 : 36}px;font-weight:800;color:var(--acc3);line-height:1.2">${esc(d.next || '')}</div>
      <div style="font-size:${T ? 40 : 36}px;font-weight:700;margin-top:16px"><span class="box">${esc(d.foot || '')}</span></div></div>
    <div class="abs" style="inset:0;pointer-events:none;background:repeating-linear-gradient(0deg,rgba(0,0,0,.22) 0 2px,transparent 2px 5px)"></div>
    <div class="abs" style="inset:0;pointer-events:none;background:radial-gradient(120% 90% at 50% 50%,transparent 60%,rgba(0,0,0,.6))"></div>
    ${src2(d.src, T ? 1452 : 1300)}`, brandTag());
  const D0 = 1.6, D = d.drawDur || 6.5, dur = D0 + D + 4.2;
  const evT = d.event ? d.event.t : null, evF = evT != null ? (evT - t0) / ((t1 - t0) || 1) : null;
  // data time as a function of video time: constant speed with a slow-down around the event
  const SLOW = .35, WIN = .1;
  const fr = u => { if (evF == null) return u; const a = Math.max(0, evF - WIN), b = Math.min(1, evF + WIN), wa = a, wb = (b - a) / SLOW, wc = 1 - b, tot = wa + wb + wc; const x = u * tot; if (x < wa) return x; if (x < wa + wb) return a + (x - wa) * SLOW; return b + (x - wa - wb); };
  const valAt = (s, tt) => { const P = s.pts; if (tt <= P[0][0]) return P[0][1]; for (let j = 1; j < P.length; j++) if (P[j][0] >= tt) { const a = P[j - 1], b = P[j]; return a[1] + (b[1] - a[1]) * ((tt - a[0]) / ((b[0] - a[0]) || 1)); } return P[P.length - 1][1]; };
  return {html, dur, build: tl => {
    scrambleIn($('#ltitle'), d.title, tl, 0.0, .42, 3); cue(0.02, 'glitch', -8); for (let k = 0; k < 8; k++) cue(.05 + k * .1, 'type', -16);
    const o = {u: 0}; tl.to(o, {u: 1, duration: D, ease: 'none'}, D0);
    const hv = Sx.map((_, i) => $('#hl' + i + ' .hv'));
    let evShown = false;
    if (evF != null) { const tEv = D0 + D * (() => { let lo = 0, hi = 1; for (let k = 0; k < 40; k++) { const m = (lo + hi) / 2; if (fr(m) < evF) lo = m; else hi = m; } return lo; })(); tl.to('#evp', {opacity: 1, duration: f30(4)}, tEv); impact(tl, tEv, {amp: 10, flash: .35, gain: -4, sub: false, sound: 'glitch'}); cue(tEv - 1, 'riser', -10); }
    for (let k = 0; k < D * 4; k++) cue(D0 + k * .25, 'tick', -20);
    TICKS.push(t => {
      const tt = t0 + (t1 - t0) * fr(o.u), x = X(tt); $('#lcr').setAttribute('width', Math.max(0, x + 4));
      Sx.forEach((s, i) => { const v = valAt(s, tt), y = Y(v); const hd = $('#hd' + i), hr = $('#hr' + i); hd.setAttribute('cx', x); hd.setAttribute('cy', y); hr.setAttribute('cx', x); hr.setAttribute('cy', y);
        const ph = (t * 1.5) % 1; hr.setAttribute('r', 13 + ph * 22); hr.setAttribute('opacity', (1 - ph) * .8);
        $('#hl' + i).setAttribute('transform', `translate(${Math.min(x, cx + cw - (s.label.length * 19 + 140))} ${y + (i ? 46 : -46)})`); hv[i].textContent = pct(v); });
      const ld = $('#ldt'); ld.setAttribute('x', Math.min(Math.max(x, cx + 60), cx + cw - 60)); ld.textContent = (o.u <= 0 || o.u >= .985) ? '' : new Date(tt).toUTCString().slice(5, 11).toUpperCase();
      const vis = o.u > 0 ? 1 : 0; Sx.forEach((_, i) => { $('#hd' + i).style.opacity = vis; $('#hr' + i).style.opacity = vis; $('#hl' + i).style.opacity = vis; });
    });
    const end = D0 + D;
    impact(tl, end + .05, {amp: 16}); tl.to('#ldelta', {opacity: 1, duration: .01}, end + .05).fromTo('#ldelta', {scale: 1.8}, {scale: 1, duration: f30(8), ease: 'back.out(2)', immediateRender: false}, end + .05);

    tl.to('#lfoot', {opacity: 1, duration: .01}, end + .9).from('#lfoot > *', {x: -60, opacity: 0, stagger: f30(5), duration: f30(9), ease: 'power3.out'}, end + .9); cue(end + .9, 'type', -10); cue(end + 1.05, 'pop', -8);
    tl.fromTo('#cam', {scale: 1}, {scale: 1.04, duration: dur, ease: 'none'}, 0);
  }};
};

/* ---- Then vs Now: the same names, two dates, an arrow (board look). Frame 0 shows the THEN row final; NOW flips in one by one ---- */
F.thennow = d => {
  const T = tall(), it = d.items, n = it.length, cw = (S.w - 120 - (n - 1) * 24) / n, bd = n > 3 ? 130 : 150, bdN = n > 3 ? 100 : 112;
  const badge = (x, sz) => x.flag ? `<div style="width:${sz}px;height:${sz}px;border-radius:50%;overflow:hidden;border:5px solid #fff;box-shadow:0 10px 30px rgba(0,0,0,.5);flex:none"><img src="${x.flag}" style="width:100%;height:100%;object-fit:cover"></div>`
    : (x.team ? chip(x.team, sz) : '');
  const col = (x, i, now) => `<div class="tn${now ? 'n' : 't'}" style="width:${cw}px;display:flex;flex-direction:column;align-items:center;gap:12px;text-align:center">${badge(x, now ? bdN : bd)}
      ${now ? '' : `<div style="font-size:${x.label.length > 12 ? 30 : 36}px;font-weight:900;line-height:1.05;min-height:${T ? 76 : 70}px;display:flex;align-items:center">${esc(x.label)}</div>`}
      ${now ? `<div class="dsp num tnv" style="font-size:${T ? 132 : 112}px;line-height:1;color:var(--text)">?</div>
        <div class="tnd" style="font-size:38px;font-weight:900;padding:6px 18px;border-radius:999px;opacity:0;background:${x.now >= x.then ? 'rgba(43,213,118,.16)' : 'rgba(255,77,94,.16)'};color:${x.now >= x.then ? 'var(--acc)' : 'var(--acc2)'}">${x.now >= x.then ? '▲' : '▼'} ${Math.abs(Math.round(100 * x.now) - Math.round(100 * x.then))} pts</div>`
        : `<div class="dsp num" style="font-size:${T ? 104 : 90}px;line-height:1;color:var(--muted)">${pct(x.then)}</div>`}</div>`;
  const top = T ? 232 : 60, y1 = T ? 586 : 330, dv = y1 + (T ? 392 : 340);
  const html = wrap(`<div class="abs" style="inset:0;background:radial-gradient(70% 40% at 50% 0%,rgba(245,197,66,.14),transparent 70%),linear-gradient(180deg,#121720,#0E1116)"></div>
    <div class="abs" id="tnh" style="left:60px;right:60px;top:${top}px">
      <div><span class="pill" style="background:var(--acc3);color:#0E1116;font-size:28px">${esc(d.kicker || '')}</span></div>
      <div class="dsp" style="font-size:${T ? 100 : 86}px;margin-top:14px">${mwords(d.title)}</div></div>
    <div class="abs" style="left:60px;top:${y1 - 52}px"><span class="pill" style="background:var(--panel);border:2px solid var(--line);color:var(--muted);font-size:26px">${esc(d.thenLabel || 'THEN')}</span></div>
    <div class="abs" id="tnT" style="left:60px;right:60px;top:${y1}px;display:flex;gap:24px">${it.map((x, i) => col(x, i, false)).join('')}</div>
    <div class="abs" id="tndiv" style="left:60px;right:60px;top:${dv}px;height:4px;background:var(--line);transform-origin:0 50%"></div>
    <div class="abs" id="tnspan" style="left:0;right:0;top:${dv - 24}px;text-align:center"><span class="pill" style="background:var(--acc3);color:#0E1116;font-size:28px">${esc(d.span || '')} &#8595;</span></div>
    <div class="abs" style="left:60px;top:${dv + 26}px;opacity:0" id="tnnowl"><span class="pill" style="background:var(--text);color:#0E1116;font-size:26px">${esc(d.nowLabel || 'NOW')}</span></div>
    <div class="abs" id="tnN" style="left:60px;right:60px;top:${dv + 84}px;display:flex;gap:24px">${it.map((x, i) => col(x, i, true)).join('')}</div>
    <div class="abs" id="tnf" style="left:40px;right:40px;top:${T ? 1394 : 1180}px;text-align:center;font-size:40px;opacity:0"><span class="box">${esc(d.foot || '')}</span></div>
    ${src2(d.src, T ? 1466 : 1300)}`, brandTag());
  const t0 = 1.55, gap = .8, big = it.reduce((b, x, i) => Math.abs(x.now - x.then) > Math.abs(it[b].now - it[b].then) ? i : b, 0);
  const tBig = t0 + n * gap + .35, dur = tBig + 3.6;
  return {html, dur, build: tl => {
    tl.from('#tnh .pill', {scale: .5, opacity: 0, duration: f30(6), ease: 'back.out(2)'}, 0).from('#tnh .word', {yPercent: 110, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0.02);
    tl.from('.tnt', {y: 40, opacity: 0, duration: f30(7), stagger: f30(2), ease: 'power3.out'}, 0.02);
    tl.from('.tnn > *:first-child', {scale: .7, opacity: 0, duration: f30(7), stagger: f30(2), ease: 'power3.out'}, 0.04);
    tl.fromTo('#cam', {scale: 1}, {scale: 1.03, duration: dur, ease: 'none'}, 0);
    cue(0.04, 'whoosh', -10);
    tl.from('#tndiv', {scaleX: 0, duration: f30(10), ease: 'power2.inOut'}, .9).from('#tnspan .pill', {scale: .4, opacity: 0, duration: f30(8), ease: 'back.out(2)'}, 1.0).to('#tnnowl', {opacity: 1, duration: f30(6)}, 1.1);
    cue(.9, 'whoosh', -8);
    const vs = $$('.tnv'), ds = $$('.tnd');
    it.forEach((x, k) => {
      const at = t0 + k * gap, o = {v: x.then};
      tl.fromTo(vs[k], {rotationX: -90, transformPerspective: 600}, {rotationX: 0, transformPerspective: 600, duration: f30(8), ease: 'power3.out', immediateRender: false}, at);
      tl.to(o, {v: x.now, duration: .6, ease: 'power2.out'}, at + .05);
      TICKS.push(t => { vs[k].textContent = t < at ? '?' : pct(o.v); vs[k].style.color = t < at + .6 ? 'var(--text)' : (x.now >= x.then ? 'var(--acc)' : 'var(--acc2)'); });
      tl.to(ds[k], {opacity: 1, duration: .01}, at + .62).from(ds[k], {scale: .4, duration: f30(8), ease: 'back.out(2.2)'}, at + .62);
      cue(at, 'whoosh', -14); for (let j = 0; j < 4; j++) cue(at + .08 + j * .12, 'tick', -16); cue(at + .62, x.now >= x.then ? 'pop' : 'thud', -5);
    });
    const bc = $$('.tnn')[big];
    tl.fromTo(bc, {scale: 1}, {scale: 1.08, duration: f30(6), ease: 'power2.out', immediateRender: false}, tBig).to(bc, {scale: 1.03, duration: f30(10), ease: 'power2.inOut'}, tBig + f30(6));
    impact(tl, tBig, {amp: 12, flash: .3, punch: false, gain: -2});
    tl.to('#tnf', {opacity: 1, duration: .01}, tBig + .9).from('#tnf .box', {scale: .6, opacity: 0, duration: f30(9), ease: 'back.out(2)'}, tBig + .9); cue(tBig + .9, 'pop', -8);
  }};
};

/* ---- Reel: tonight's games in 15 seconds, hard cuts on real stock footage, one game per cut (night look, team colours) ---- */
F.reel = d => {
  const T = tall(), G = d.segs, n = G.length, cardTop = T ? 1050 : 820;
  const pairChip = (g, sz) => `<div style="display:flex;align-items:center;gap:${sz * .12}px">${chip(g.a.team, sz)}<span class="dsp" style="font-size:${sz * .42}px;color:#fff">v</span>${chip(g.b.team, sz)}</div>`;
  const grid = G.map(g => `<div style="display:flex;justify-content:center">${pairChip(g, 76)}</div>`).join('');
  const cards = G.map((g, i) => {
    const fav = g.pa >= g.pb ? g.a : g.b, pf = Math.max(g.pa, g.pb), flip = pf < .45;
    return `<div class="abs rcard" id="rc${i}" style="left:50px;right:50px;top:${cardTop}px;opacity:0">
      <div style="display:flex;align-items:center;gap:22px">${chip(g.a.team, 120)}<div class="dsp" style="font-size:58px;flex:1;line-height:1;text-shadow:0 4px 18px rgba(0,0,0,.8)">${esc(g.a.label)}<br><span style="color:var(--muted);font-size:40px">v</span> ${esc(g.b.label)}</div>${chip(g.b.team, 120)}</div>
      <div style="margin-top:22px;background:rgba(11,12,15,.9);border:2px solid #2A2E36;border-radius:26px;padding:18px 26px;display:flex;align-items:center;gap:20px">
        <div style="flex:1"><div style="font-size:30px;font-weight:800;color:var(--muted)">${esc(g.time)} · ${flip ? 'too close to call' : 'chance to win'}</div>
          <div style="font-size:44px;font-weight:900;margin-top:4px">${flip ? esc(g.a.label + ' or ' + g.b.label) : esc(fav.label)}</div></div>
        <div class="dsp num" style="font-size:118px;line-height:1;color:${flip ? 'var(--acc3)' : 'var(--acc)'}">${flip ? pct(g.pa) + '/' + pct(g.pb) : pct(pf)}</div></div></div>`;
  }).join('');
  const html = wrap(`${clipLayer()}<div class="abs" style="inset:0;background:linear-gradient(180deg,rgba(0,0,0,.6) 0%,rgba(0,0,0,.1) 30%,rgba(0,0,0,.15) 50%,rgba(0,0,0,.78) 100%)"></div>
    <div class="abs" id="rhud" style="left:50px;right:50px;top:${T ? 226 : 50}px;display:flex;align-items:center;justify-content:space-between;opacity:0">
      <span class="pill" style="background:var(--acc);color:#0B0C0F;font-size:26px">${esc(d.kicker || 'Tonight')}</span><span class="dsp num" id="rcnt" style="font-size:52px;text-shadow:0 4px 18px rgba(0,0,0,.8)">1/${n}</span></div>
    <div class="abs" id="rintro" style="left:50px;right:50px;top:${T ? 300 : 120}px">
      <div class="dsp" style="font-size:${T ? 110 : 92}px;text-shadow:0 6px 30px rgba(0,0,0,.8)">${mwords(d.title)}</div>
      <div id="rgrid" style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:26px 10px;margin-top:46px">${grid}</div></div>
    ${cards}
    <div class="abs" id="routro" style="left:60px;right:60px;top:${T ? 560 : 320}px;opacity:0;text-align:center">
      <div class="dsp" style="font-size:${T ? 104 : 90}px;text-shadow:0 6px 30px rgba(0,0,0,.8)">${mk(d.endTitle || '')}</div>
      <div style="font-size:${T ? 44 : 40}px;margin-top:40px"><span class="box">${esc(d.cta || '')}</span></div></div>
    ${src2(d.src, T ? 1466 : 1300)}`, brandTag());
  return {html, dur: d.dur, build: tl => {
    tl.from('#rintro .word', {yPercent: 110, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0);
    tl.from('#rgrid > div', {scale: .5, opacity: 0, duration: f30(6), stagger: f30(1), ease: 'back.out(2)'}, 0.02);
    cue(0.02, 'hit', -6); cue(0.02, 'file:crowd_bed', -16);
    tl.to('#rintro', {y: -120, opacity: 0, duration: f30(6), ease: 'power2.in'}, G[0].at - .2).to('#rhud', {opacity: 1, duration: f30(5)}, G[0].at);
    G.forEach((g, i) => {
      const id = '#rc' + i, dir = i % 2 ? -1 : 1;
      tl.set(id, {opacity: 1}, g.at).fromTo(id, {xPercent: 110 * dir}, {xPercent: 0, duration: f30(7), ease: 'power3.out', immediateRender: false}, g.at);
      tl.fromTo('#clip', {scale: 1.08}, {scale: 1, duration: f30(9), ease: 'power2.out', immediateRender: false}, g.at);
      tl.to(id, {xPercent: -110 * dir, opacity: 0, duration: f30(5), ease: 'power2.in'}, g.at + g.dur - f30(5));
      cue(g.at - .04, 'whoosh', -6); cue(g.at + .02, 'hit', -14);
    });
    const oa = d.outroAt;
    tl.to('#rhud', {opacity: 0, duration: .2}, oa - .1).to('#routro', {opacity: 1, duration: .01}, oa).from('#routro > *', {y: 60, opacity: 0, stagger: f30(4), duration: f30(9), ease: 'power3.out'}, oa);
    cue(oa - 1, 'riser', -8); cue(oa, 'hit', -2); cue(oa, 'sub', -6);
    TICKS.push(t => { let k = 0; G.forEach((g, i) => { if (t >= g.at - .05) k = i; }); $('#rcnt').textContent = (k + 1) + '/' + n; });
  }};
};

/* ---- Goal cam: the real app filmed live during a match; the price jumps on screen when the goal goes in ---- */
F.goalclip = d => {
  const T = tall(), J = d.jump, endAt = d.endAt, pw = T ? 760 : 560, ph = Math.round(pw * 1920 / 1080), px = (S.w - pw) / 2, py = T ? 430 : 300;
  const chip_ = d.chip ? `<div class="abs" id="gcc" style="left:50px;right:50px;top:${T ? 232 : 60}px;height:${py - (T ? 250 : 70)}px;display:flex;align-items:center;justify-content:center;gap:22px;opacity:0">
      ${d.chip.team ? chip(d.chip.team, 92) : ''}<div class="dsp num" style="font-size:100px;color:#8B919C">${pct(d.chip.from)}</div>
      <div style="font-size:64px;font-weight:900;color:#fff">&#8594;</div><div class="dsp num" id="gcv" style="font-size:132px;color:${d.chip.to >= d.chip.from ? 'var(--acc)' : 'var(--acc2)'}">${pct(d.chip.from)}</div></div>` : '';
  const html = wrap(`<div class="abs" style="inset:0;background:radial-gradient(80% 50% at 50% 30%,rgba(255,59,59,.12),transparent 70%),#0B0C0F"></div>
    <div class="abs" style="inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 2px,transparent 2px 80px),repeating-linear-gradient(90deg,rgba(255,255,255,.03) 0 2px,transparent 2px 80px)"></div>
    <div class="abs" id="phone" style="left:${px}px;top:${py}px;width:${pw}px;height:${ph}px;border-radius:56px;overflow:hidden;border:5px solid #2A2E36;box-shadow:0 40px 120px rgba(0,0,0,.75),0 0 0 2px #000">${clipLayer()}</div>
    <div class="abs" id="gch" style="left:50px;right:50px;top:${T ? 226 : 50}px;height:${py - (T ? 244 : 64)}px;display:flex;flex-direction:column;justify-content:center;gap:12px">
      <div><span class="pill" style="background:#FF3B3B;color:#fff;font-size:26px"><i id="gdot" style="width:14px;height:14px;border-radius:50%;background:#fff;display:inline-block"></i>${esc(d.kicker || 'Live on Outcome')}</span></div>
      <div class="dsp" style="font-size:${T ? 76 : 64}px">${mwords(d.hook || '')}</div></div>
    ${chip_}
    <div class="abs" id="gcb" style="left:0;right:0;top:${py + 120}px;text-align:center;opacity:0">
      <div class="dsp" style="display:inline-block;font-size:${T ? 180 : 150}px;background:var(--acc);color:#0B0C0F;padding:4px 40px;border-radius:24px;transform:rotate(-3deg);box-shadow:0 20px 60px rgba(0,0,0,.6)">${esc(d.badge || 'GOAL')}</div>
      <div class="dsp" style="font-size:${T ? 72 : 62}px;margin-top:16px"><span style="background:rgba(11,12,15,.9);padding:6px 22px;border-radius:14px">${esc(d.score || '')}</span></div></div>
    <div class="abs" id="gce" style="inset:0;background:rgba(11,12,15,.95);display:flex;flex-direction:column;justify-content:center;gap:34px;padding:0 70px;opacity:0">
      <div class="dsp" style="font-size:${T ? 110 : 96}px">${mk(d.endTitle || '')}</div>
      <div style="font-size:${T ? 42 : 38}px;font-weight:800;color:#C9CDD4">${esc(d.endSub || '')}</div>
      <div style="font-size:${T ? 44 : 40}px"><span class="box">${esc(d.cta || '')}</span></div></div>`, brandTag());
  return {html, dur: d.dur, build: tl => {
    tl.from('#phone', {y: 140, opacity: 0, duration: f30(9), ease: 'power3.out'}, 0);
    tl.from('#gch .pill', {scale: .5, opacity: 0, duration: f30(6), ease: 'back.out(2)'}, 0).from('#gch .word', {yPercent: 110, duration: f30(7), stagger: f30(1), ease: 'power3.out'}, 0.02);
    cue(0.05, 'whoosh', -10); cue(J - 1.3, 'riser', -8); cue(0, 'file:crowd_bed', -18); cue(J, 'roar', -5);
    TICKS.push(t => { $('#gdot').style.opacity = (Math.floor(t * 2) % 2) ? .25 : 1; });
    impact(tl, J, {amp: 18});
    tl.fromTo('#phone', {scale: 1}, {scale: 1.06, duration: 1.1, ease: 'power2.out', immediateRender: false}, J);
    tl.set('#gcb', {opacity: 1}, J).fromTo('#gcb > div:first-child', {scale: 2.2, rotation: -10}, {scale: 1, rotation: -3, duration: f30(9), ease: 'back.out(2)', immediateRender: false}, J)
      .from('#gcb > div:last-child', {y: 40, opacity: 0, duration: f30(8), ease: 'power3.out'}, J + .25)
      .to('#gcb', {opacity: 0, duration: .3}, J + 2.2);
    if (d.chip) { tl.to('#gch', {opacity: 0, duration: .2}, J + .5).to('#gcc', {opacity: 1, duration: .2}, J + .6).from('#gcc', {y: 40, duration: f30(9), ease: 'power3.out'}, J + .6);
      const c = counter($('#gcv'), d.chip.from, d.chip.to); c.tween(tl, J + .8, .9); TICKS.push(c.draw); cue(J + .6, 'whoosh', -10); for (let k = 0; k < 6; k++) cue(J + .8 + k * .12, 'tick', -12); }
    tl.to('#gce', {opacity: 1, duration: .35}, endAt).from('#gce > *', {y: 40, opacity: 0, stagger: f30(4), duration: f30(9), ease: 'power3.out'}, endAt + .1); cue(endAt, 'whoosh', -8);
  }};
};

/* ---- Live tape v2: the real app inside a phone frame, the story above it, so nothing on the app is ever covered ---- */
F.livetape = d => {
  const T = tall(), pw = T ? 760 : 560, ph = Math.round(pw * 1920 / 1080), px = (S.w - pw) / 2, py = T ? 430 : 300;
  const boxes = d.steps.map((s, i) => `<div class="abs stp" id="lt${i}" style="left:40px;right:40px;top:${T ? 232 : 60}px;height:${py - (T ? 250 : 70)}px;display:flex;align-items:center;justify-content:center;text-align:center;opacity:0;font-size:${T ? 52 : 44}px"><div>${s.lines.map(l => `<span class="box">${mk(l)}</span>`).join('<br>')}</div></div>`).join('');
  const html = wrap(`<div class="abs" style="inset:0;background:radial-gradient(80% 50% at 50% 30%,rgba(212,255,58,.10),transparent 70%),#0B0C0F"></div>
    <div class="abs" style="inset:0;background:repeating-linear-gradient(0deg,rgba(255,255,255,.03) 0 2px,transparent 2px 80px),repeating-linear-gradient(90deg,rgba(255,255,255,.03) 0 2px,transparent 2px 80px)"></div>
    <div class="abs" style="left:0;right:0;top:0;height:10px;background:rgba(255,255,255,.12)"><div id="prog" style="height:100%;width:0;background:var(--acc)"></div></div>
    <div class="abs" id="phone" style="left:${px}px;top:${py}px;width:${pw}px;height:${ph}px;border-radius:56px;overflow:hidden;border:5px solid #2A2E36;box-shadow:0 40px 120px rgba(0,0,0,.75),0 0 0 2px #000">${clipLayer()}</div>
    ${boxes}
    <div class="abs" id="res" style="left:0;right:0;top:${py + ph * .36}px;text-align:center;opacity:0"><span class="dsp" style="display:inline-block;font-size:${T ? 190 : 160}px;padding:6px 44px;border-radius:26px;background:${d.result === 'UP' ? 'var(--acc)' : 'var(--acc2)'};color:${d.result === 'UP' ? '#0B0C0F' : '#fff'};box-shadow:0 20px 60px rgba(0,0,0,.6)">${esc(d.result || '')}</span></div>
    <div class="abs" id="endc" style="inset:0;background:rgba(11,12,15,.95);display:flex;flex-direction:column;justify-content:center;gap:36px;padding:0 70px;opacity:0">
      <div class="dsp" style="font-size:${T ? 110 : 96}px">${mk(d.endTitle || '')}</div>
      <div style="font-size:${T ? 44 : 40}px;font-weight:800;color:#C9CDD4">${mk(d.endSub || '')}</div>
      <div style="font-size:${T ? 44 : 40}px"><span class="box">${esc(d.cta || 'Call the next 15 minutes on Outcome.xyz')}</span></div></div>`, brandTag());
  return {html, dur: d.dur, build: tl => {
    tl.to('#prog', {width: '100%', duration: d.dur, ease: 'none'}, 0);
    tl.from('#phone', {y: 140, opacity: 0, duration: f30(9), ease: 'power3.out'}, 0); cue(0.03, 'whoosh', -10);
    d.steps.forEach((s, i) => { tl.to('#lt' + i, {opacity: 1, duration: .01}, s.at).from('#lt' + i + ' .box', {scale: .6, opacity: 0, duration: f30(8), ease: 'back.out(2)'}, s.at); cue(s.at, 'pop', -9);
      if (i < d.steps.length - 1) tl.to('#lt' + i, {opacity: 0, duration: .2}, d.steps[i + 1].at - .15); });
    const ra = d.resultAt;
    if (ra != null) {
      tl.fromTo('#phone', {scale: 1}, {scale: 1.05, duration: 3, ease: 'none', immediateRender: false}, ra - 3);
      for (let k = 3; k >= 1; k--) cue(ra - k, 'tick', -4);
      cue(ra - 1.2, 'riser', -9);
      tl.to('#lt' + (d.steps.length - 1), {opacity: 0, duration: .15}, ra);
      tl.set('#res', {opacity: 1}, ra).fromTo('#res span', {scale: 2.4, rotation: -8}, {scale: 1, rotation: -3, duration: f30(9), ease: 'back.out(2)', immediateRender: false}, ra);
      impact(tl, ra, {amp: 18});
    }
    if (d.endAt != null) { tl.to('#endc', {opacity: 1, duration: .35}, d.endAt).from('#endc > *', {y: 40, opacity: 0, stagger: f30(4), duration: f30(9), ease: 'power3.out'}, d.endAt + .1); cue(d.endAt, 'whoosh', -8); }
  }};
};

/* ---- entry point wrapper: look, cue sheet and shake reset per post ---- */
const _show0 = window.show;
window.show = async function (spec) {
  CUES = []; SHAKES = []; SHAKE_ON = false;
  applyLook(spec.look || DEFAULT_LOOK[spec.fmt] || 'night');
  return _show0(spec);
};
