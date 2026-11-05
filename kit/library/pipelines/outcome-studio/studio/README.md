# Outcome studio (built 13 Oct 2026)

Faceless posts for Outcome (outcome.xyz) built from live market data. Read `PLAYBOOK.md` for what to post and the rules; this file is how to run it.
Research behind it: `..\research\` (start with `00-status.md`, formats in `18-format-catalogue.md`, dates and facts in `19-calendar-and-facts.md`).

## Daily run (about 5 minutes of machine time)
1. Keep the price archive running all day, every day: double-click `start_archive.bat` (or `python archive.py`; saves every 5 min, minute prices during matches, and asks Windows not to idle-sleep while it runs). Market history disappears when a market settles, so replays, upsets and comebacks only exist for games the archive saw live. Check `data\archive\archive.log`.
2. `python ocs.py scan` : today's matches (48 h), season and macro markets, biggest 24 h moves, top traders.
3. `python ocs.py plan YYYY-MM-DD` : writes `batches\<date>.json`, a starting set of posts. Edit it: drop weak posts, add facts to pick posts, set captions (`caption`), posting notes (`when`), slide overrides.
4. `python ocs.py build batches\<date>.json [--only id1,id2] [--no-video]`
5. `python ocs.py sheet <date>` : one contact sheet `out\<date>\_sheet.jpg` to check everything.
Post from `FINALS\<date>\@<page>\NN_<id>\`: `ig_N.jpg` (Instagram carousel 1080x1350), `tt_N.jpg` (TikTok photo mode 1080x1920), `video.mp4` (1080x1920; video recipes carry their own sound effects, the older card videos are silent), `caption.txt`. All captions together in `captions.txt`. A rebuilt post never overwrites a delivered one: it goes to `NN_<id>_v2`.

## Recipes (batch "recipe" + "args")
| recipe | args | makes |
|---|---|---|
| matchday | comp ("UEFA Champions League" / "UEFA Europa League"), day "YYYYMMDD", title | home/draw/away % card, 5 games per slide + animated video |
| pick | match (key "Q422" or words "Man City PSG"); batch field "facts": {"Team name": {"facts": ["...", "..."], "source": "ESPN, 13 Oct"}} | split-screen "X or Y?", fact slides, the money's answer, CTA + flip video |
| swing | market ("Ballon d'Or"), names [..], days, title, sub | race chart with deltas + line-drawing video |
| quiz | part, items [{q, market, outcome, team, context}] | Guess the % carousel (answer position varies), answers slide |
| breaking | market, outcome, headline ("{a} *{p}*" fill in a/an and the %), note, kicker | "The market says" card with 24 h change + chart |
| tier / ranking / pricetags | market, title, sub | tier list, favourites ranking, price tags (cents) |
| ladder_touch | asset ("BTC", "HYPE", "CL" = oil) | price-target ladder with a NOW line |
| ladder_ipo | company ("Anthropic") | IPO first-day value ladder + IPO-confirmed chances |
| number | market, outcome, line, sub | one giant number |
| cheapest | n | the lowest-priced outcomes on the board |
| top3 | window ("24h", "7d", "30d") | client format: hook + #3/#2/#1 real profile screenshots + CTA (needs the username OK) |
| howto | market ("Q422"), recapture (true) | client format: 5 slides over real outcome.xyz screens (no UI covered) |
| pnl | username, coin (optional, best trade if empty), theme ("light"/"dark") | client format: our own P&L card, transparent PNG for the edit |
| replay / upset / comeback | key ("Q412") | after a game: minute-by-minute chart replay with goal markers; upset = winner was under 35% at kickoff; comeback = winner was under 25% at half-time |
| radar | day "YYYYMMDD", comp, n | Upset Radar: tonight's underdogs with the best shot (favourite 55%+) |
| radar_result | keys ["Q408", ...] | the callback: same games with results, "1 of 3 hit" |
| barrace | market, days (30) | chance race: bar chart race of a title or award race over its daily history (video first) |
| fakereal | claim (a claim really circulating), market, outcome_label, claim_note (where it was seen), note | Fake vs Real: "The internet says X. The money says 2%." |

### Video recipes (motion.py: 9:16 video with the sound baked in, each format with its own look)
Sound comes from the video's own timeline (`window.getCues()` in `templates/motion_more.js`, mixed by `sfx.py`), so picture and sound never drift. The mixer plays real recorded effects from `assets\sfx\house` (46 CC0 sounds from Kenney and Freesound, `sfx.json` holds each file's hit point so the hit lands on the frame; licences in `assets\sfx\LICENCES.md`) and falls back to its own synth. Beds: a cue named `file:crowd_bed` (or rain_bed, wind) plays a whole file. Effects only, peaks at -3 dB: room for a trending sound added in-app. Video-only posts get `cover.jpg` (frame 0).
Stock footage: `footage\stock\<theme>\` (football, city_night, sky, trading, race; Mixkit and Coverr free licences, every clip frame-checked for faces and logos; `LICENCES.md` lists source and licence per file; check the terms allow paid promotion before posting). `motion.stock_cut([(name, seconds), ...], out)` makes one hard-cut clip from them.
| recipe | args | makes |
|---|---|---|
| forecast | comp ("UEFA Champions League"), keys [optional], hero (key) | the football weather forecast: sunniest game as the hero, "Sunny spells" (favourite 70%+), "Storm warning" (nobody above 50%), "Upset watch" (best long shots). Weather look. Post the forecast check next morning |
| race | market ("Q198"), n (6), race_no, seed (default: today's date) | "If the title race was a race": club balls race up a track, the finishing order is ONE draw weighted by the real chances (seed logged), then the real chances. Neon look. Daily series |
| countdown | market ("Q199"), n (8) | the money's top N revealed from last place to the favourite, each card flies into the board. Broadcast look |
| quizclock | matches ["Q410", ...] (3 to 5) | Guess the favourite: 3-second clock per game, then the real chances; end card "comment your score". Tabloid look |
| sim100 | match ("Q407") | one match played 100 times: cells resolve in a random order (seeded), then sort into blocks. Paper look |
| linestory | market, labels [2 outcomes], names, days, title, kicker, hero_label, next_line | one chart: two lines draw themselves, the crossing ("THE FLIP") is pinned, the delta lands. Terminal look |
| livetape | tape ("footage/btc15m_HHMM.mp4" from `python livetape.py btc15`), lead (40), tail (8), speed (1.6) | the real outcome.xyz app filmed live: Bitcoin's last seconds, the result, end card |
| take | market, labels [..], lines [3 short lines], still (photo) + move {x0, x1, z0, z1} or clip + start, title, note | hot take in big words over footage, then the receipt with the real chances |
| pnl_film | username, coin, still/clip + move, title, side, mask (true) | the client's P&L edit: our card from the real trade drops in over footage (username masked until the client OK) |
| aichat | match, ai_pick, ai_answer (a REAL model reply, checked facts), day | AI vs the money, day N |
| reel | comp ("UEFA Champions League"), day, keys [optional], seg (1.45 s) | tonight's games in about 15 seconds: hard cuts on stock football footage (a city shot when the host city has one: London = Tower Bridge), one game and its real chance per cut, stadium sound underneath |
| thennow | market ("Q391"), days (30), n (3) | Then vs Now board: the top n with their chance `days` ago (or the market's first day) above today's, arrows and point changes. Board look. Proof: 96x on a 3.93K page |
| matchline | key ("Q409"), focus (optional 0 home / 1 away) | full-time line replay: the match told by the money, kick-off to whistle, goal spikes with scorer captions and crowd sound, resolved 100/0 at full time. Prices: goal-cam 10-second prices when the game was filmed, else real trades plus 5-minute book snapshots whose three chances add to about 100% (wide-spread snapshots dropped); a side that barely traded is drawn faint and labelled |
| scoreboard | day ("20261013") or keys [..] | last night's favourites: one row per game (the favourite at kick-off and its chance), a tick or a cross, the tally. Same template after every match night |
| goalclip | key ("Q412"), n (event number) | the real app filmed during a match by `goalcam.py`: the chance jumps on screen when the goal goes in, GOAL badge, before and after chip. Works after the market settles |
| wheel / timed / outof100 / demo | match (+ day, seed) / match / match / market | client wheel format, call it in 3, out of 100, app demo over real screens |
Morning after a match night: `python postmatch.py list YYYYMMDD` (scores, pre-match chances, upset / comeback flags), then a batch of matchline (the upsets and comebacks), scoreboard and goalclip posts (pick score events from `out\_goalcam\<key>\events.json`). Example: `batches\2026-10-14_after.json`.
Goal cam on match nights: `python goalcam.py run Q405 Q407 ...` (waits for each kick-off, films the match pages at 4 fps, keeps 150 s before to 60 s after every goal or 8-point price jump, stops after full time, then cuts `footage\goalcam_<key>_<n>.mp4`). Re-cut later with `python goalcam.py cut <key>`.
Research verdicts (`..\research\22-video-formats-round2.md`): lead with race, then-vs-now, countdown, 100 games and the quiz; the weather forecast and a commentator voice have no proof yet (test, never the main slot); keep odds and venue names out of titles.
Check a new or changed format fast: `python videotest3.py sheet [names]` (one contact sheet per format), then `python videotest3.py video [names]`.

Market words for `find`: a key (`Q412`, `O8573`), words in the title ("Premier League winner"), or {"kind": "fed", "q": "Q289"}.
`python postmatch.py list YYYYMMDD` shows archived matches, their pre-match chances and which of upset / comeback they qualify for.

## Files
- `ocdata.py` data (Hyperliquid info API + Outcome API, market titles, sanity checks), `archive.py` price archive, `formats.py` post builders, `traders.py` leaderboard / fills / P&L, `postmatch.py` replays, `howto.py` + `capture.py` real outcome.xyz screens, `render.py` headless Chrome renderer (stills + frame-by-frame video), `templates/studio.html` the card designs, `templates/motion.html` + `templates/motion_more.js` the video formats (GSAP timelines, look kit: night, broadcast, tabloid, paper, terminal, weather, neon), `motion.py` video builders, `sfx.py` our own synthesised sound effects + mixer, `livetape.py` films the real app, `ocs.py` the CLI, `gallery.py` the review page (`python gallery.py <date> [<date> ...]`), `selftest.py` / `videotest*.py` render checks.
- `brand.json`: PLACEHOLDER page identity (handle, name, avatar), CTA line, risk line, disclosure (`#ad` is put in front of every caption), time zone label for kickoffs, fonts.
- `assets/`: fonts (OFL), Outcome's own logo files (client marks, use only for Outcome posts), `teams.json` (146 clubs: colours, codes), `players.json` (Ballon d'Or nominees), flags, icons. `refs/`: reference posts per format with contact sheets.
- Needs: Chrome, Python 3.13 (Pillow, numpy, websockets, av), ffmpeg (found automatically).

## Data rules built in
- Prices are mids from Hyperliquid (`allMids`); a market is skipped when its sides do not add to about 100%, or a price is the 0.5 placeholder of an untraded side.
- Every slide carries a time stamp; numbers are never typed by hand.
- Market names come from Outcome's own descriptions; duplicate listings from other venues (trade.xyz) are dropped in favour of Outcome's.
