# The faceless post studio (`outcome-studio/`)

Faceless posts for a prediction-market client, produced from live market data and real footage. Built 13 to 14 Oct
2026. The folder has three parts:
- `studio/`: the data and footage machine (market data, a price archive, scans and plans, real-app capture and live
  filming, the post-match routine, a DevTools render engine with the first card and motion formats, an SFX mixer, a
  review gallery maker). Read its README and PLAYBOOK first.
- `newsdesk/`: a fork of the news builder in the approved house look, plus a keyed reaction layer, a black background
  for app recordings and scene beds (`beds.py`). This is what the current sample pack was built with.
- `research-tools/`: readers and measurement scripts used by the research rounds (how to use them for research is in
  research-and-sourcing; the measurement method is in references/review-pages-and-qa.md section 4).
What the posts should be (the number as the punchline, real moments first, most posts without a number, the word-swap
table for gambling-adjacent clients, platform permissions) is in social-video-formats. The client's own rules, risks
and open decisions are in the client file.

## 1. What the verdicts taught the pipeline
| Round | What was built | Verdict | Pipeline lesson |
|---|---|---|---|
| 1 | 18 designed data cards from live prices | "these are all SAME types of posts bro" | vary the kind of post, not the card |
| 2 | 40 motion videos, each format in its own designed look, SFX-pack sound | "the UI is bad", "It's not worth posting them", "I can't watch them" | the engine was fine; designed dashboards, skins and pack sound are ad tells on a native page |
| 3 | plan page with a white-box TikTok text style | "i dont like this text style bro its TOOO off beat" | show one mock frame of a new look before building around it; the user's taste wins on look |
| 4 | 9 posts in the house look (real clips, our app recordings, one caption, a reaction face) | pending | start from a real moment; the number is the punchline |
- The rejected engine is still worth keeping: the DevTools renderer, the timeline cue sheet and the SFX mixer suit
  explainers and data videos for other clients; the timing rules of the motion formats were never the problem.
- A fact found by measuring our own output (OCR word counts, text position, cuts per 10 s against 49 to 148 native
  references) turned "looks designed" into 8 fixes. Do that before any redesign.

## 2. Daily run
1. **Keep the price archive running all day, every day:** `start_archive.bat` on Windows, `start_archive.sh` on the Mac
   (runs `caffeinate -i python3 -u archive.py`), or `python3 archive.py` (`--once` for a test). Every 5 minutes it saves
   about 658 to 670 mids and the perps, the market list when it changes, 1-minute candles of live and just-finished
   matches, ESPN scoreboards and the 15-minute and daily up/down series (the venue keeps only the last 50). About 9.1 MB
   for 2 days; `data/archive/archive.log` has one line per cycle. Why: a market's price history is deleted the moment it
   settles, so replays, upsets and "then vs now" posts exist only for what the archive saw live. That archive is the only
   copy of past prices; ship or back it up only if those dates are wanted.
2. **See what is on:** `python3 ocs.py scan` (48 h of matches, season and macro markets, 24 h movers, top traders).
3. **Morning after a match night:** `python3 postmatch.py list YYYYMMDD` lists archived matches with their chances 1
   minute before kick-off, upsets (the winner was under 35% at kick-off) and comebacks (the winner was under 25% at
   half-time). Goal markers snap to the biggest 1-minute price jump within 6 minutes of the ESPN minute. Why: the
   night's upsets are the best punchline posts (one night: favourites won 5 of 9; a 7% side won 4-3 away).
4. **Pre-match facts:** `python3 facts.py <league slug> <YYYYMMDD> "<team words>"` prints 2 checkable facts per side
   from ESPN's public JSON (check before posting).
5. **Film the real app** when the moment needs it: `python3 livetape.py btc15 [before=90] [after=20]` for the last
   90 s of a 15-minute Bitcoin window plus 20 s after; `python3 goalcam.py run <keys...>` on match nights;
   `python3 capture.py home | market <path> | profile <user>` for phone-size screenshots.
6. **Plan:** `python3 ocs.py plan YYYY-MM-DD` writes a starter batch for the studio card formats (edit it). For the
   house-look posts, write the batch for the newsdesk fork by hand (section 4). A daily "story finder" over the archive
   (upsets, longshots, biggest moves, then vs now, captions drafted) is planned, not built.
7. **Build and check:** section 4; one sheet; numbers against the app's own on-screen labels.
8. **Review page** (references/review-pages-and-qa.md), then the human posts.

## 3. Market data rules (prediction markets in general, HIP-4 in particular)
- Coin id = "#" + (10 x outcomeId + side), side 0 = Yes or participant A, side 1 = No or B (so `#2120` = outcome 212,
  side 0). The mid is the chance: 0.663 = 66.3%.
- A mid of exactly 0.5 with no book is an untraded placeholder: never publish it.
- Skip a multi-way market unless its sides add up to 90% to 106%.
- Build titles from the description fields (`template:sportsContestResult` with participant A, participant B,
  competition, scheduled start). Clean featured names came from the client's incentives endpoint, which needs a full
  browser User-Agent.
- Drop duplicate listings from other venues; prefer the client's own.
- Never type a number by hand; time-stamp every slide; numbers on frame 0 are final and true, never mid-count.
- Thin in-match markets go stale or flicker (a side showed 66% while losing 1-3): use the goal cam's 10-second
  prices when the game was filmed, else real trades plus 5-minute snapshots whose chances add to about 100% (wide-spread
  snapshots dropped), a median filter, then the resolved 100/0 at full time.
- **Captions quote the app's on-screen label, not the polled mid** (polled 52%, the screen showed 70%).
- **Strip accents in every name matcher** (NFKD, drop the combining marks): an accented club name broke fact and
  result matching twice. Club-word stripping (" FC", "AFC ", and so on) helps too.
- **A draw in a game format is one weighted draw** by the real chances, seeded with the date by default, the seed
  logged, and the post says it is a draw. Why: reproducible, not staged.
- Public keyless data that was enough for everything: the client's API (60 requests a minute: leaderboard, profile,
  portfolio, markets lookup, series, settled, top movers, live sports); Hyperliquid's info API (`outcomeMeta`,
  `allMids`, `candleSnapshot`, `l2Book`, `recentTrades` (last 10 only), `userFillsByTime`, WebSocket); the client's
  public stats site; ESPN public
  JSON (scoreboards, goal minutes, form, pre-match odds); Binance and Coinbase candles; Google News and Federal
  Reserve RSS; Polymarket and Kalshi public APIs for comparison. A fan-built P&L card site wraps these with bugs: a
  design reference only.
- Run collectors from a home connection: the fan site's code says the client's Cloudflare blocks cloud serverless
  addresses. Unverified: whether the client's site and API load from the boss's country (its terms block some
  countries). Check before relying on capture and filming.
- Data bugs we fixed (keep the guards): anonymous leaderboard rows gave HTTP 400 (skip, take the next trader); market
  names read from the wrong JSON path (`data.markets.<id>.outcome`); P&L read-back must start from the market's
  `firstTrade`.

## 4. The house-look builder (the newsdesk fork)
- Same batch fields as references/daily-news-run.md plus:
  - `react`: {`path`, `in`, `crop` "w:h:x:y" (the figure), `h` (pixels tall, 860 to 900 worked), `x`, `y` offsets,
    `key` (default 0x00FF00), `sim` (0.16), `blend` (0.08)}. ffmpeg keys it with `chromakey=0x00FF00:0.16:0.08` then
    `despill=type=green`, scales it, and overlays it bottom centre. It is also written as `<id>_react.mov` (QuickTime
    Animation, ARGB, about 220 MB) on its own Premiere track (V1 clip, V2 reaction, V3 headline, A1 audio). If the
    template's figure has a straight crop edge, push the figure so that edge sits on the frame edge (a full-width key
    otherwise showed the edge, and an early key clipped a shirt).
  - clip `"bg": "black"` for app screen recordings (a blurred copy of the recording only showed smeared logos above
    the card).
- Build: `python3 -X utf8 vcn.py build batches/<batch>.json [--only ids]`, `python3 vcn.py sheet <batch>`. The Drive
  copy goes to the client's own posting folder (its own setting, never the music pages' folder); it was set up but
  never run.
- Caption order used: `#ad` first; the fact line; an open question ("Too high or too low?"); the source and date
  ("Price from <app>, 1 minute before kick-off"); "Not financial advice" on finance; optionally the brand's closer;
  clip and photo credits ("🎥: @handle"); the `when` window. Keep the CTA in one `brand.json` line.
- Placeholders until the client decides: page identity "@yourpage" / "Your Page" with a dark "YP" avatar, the CTA line,
  masked trader usernames. Every review page lists what must change before posting (the real handle and avatar, fresh
  prices on the day, the usernames OK).
- Checks before handing over: every number equals the app's own label at that moment; no UI covered (the client bans
  text over the chart, logo, names and Yes/No buttons; a headline over the chart was moved to the tweet layout); crops
  and keys on the sheet; date-bound lines ("tonight", "in 12 days") still true on the posting day, else refresh the
  numbers or rebuild as `_v2`.

## 5. Filming the real app
Why: the real app screen is the one device every prediction-market partner hit shared; it shows the brand without an
added logo and has no broadcast-rights problem. Designed copies of the app were rejected.
- **Phone emulation:** headless Chrome at 390x844 CSS px, device scale 3, mobile on, an iPhone Safari User-Agent;
  screenshots are 1170 px wide.
- **Filming:** capture screenshots as fast as Chrome paints (about 10 to 15 a second), record each frame's real time,
  then retime to a steady 30 fps with an ffmpeg concat list of per-frame durations, `fps=30,scale=1080:-2`, libx264
  CRF 18. One filmed 15-minute Bitcoin window: 2,015 frames, result UP.
- **Pop-ups on someone else's React/Next.js app:** never delete DOM nodes (removing them crashed the page). Instead:
  click the dialog's close button and press Escape; inject a style rule that hides `[role=dialog],
  [role=presentation][data-open], [data-radix-portal], [data-overlay], [vaul-drawer], [data-vaul-overlay]` and restores
  scrolling; re-apply it every 15 frames while filming; make the injector null-safe (`document.head ||
  document.documentElement`); run a 4 s test film before any timed window. Why: one timed film was unusable because a
  sign-in modal and a separate 12 px blur layer came back; the next was clean.
- **Goal cam** (`goalcam.py`): one headless Chrome per match, waits for kick-off minus 2 minutes, films the match page
  at about 4 fps into a rolling 4-minute buffer, keeps 150 s before to 60 s after every event, stops after full time or
  settlement, then `goalcam.py cut <key>` writes `footage/goalcam_<key>_<n>.mp4` (30 fps, real time) + `events.json`.
  `goalcam.py test <key> 40` films any page for 40 s and fakes an event at 20 s to test the chain. Caught: one side
  21% to 52/70%, another 55% to 72%, another 31% to 55%.
- **Goal-cam events must hold.** An event = an ESPN score change (polled every 20 s) or a home/away price move of 8+
  points within 60 s (polled every 10 s). To count, the median of the last 30 s must differ from the median 60 to 120 s
  ago, with at least 3 samples each; no two events within 90 s; ESPN names matched on the short name and the full
  label, accent-insensitive. Why: one-poll spikes in a thin order book are noise; the hold test dropped all 3 false
  flickers (1 to 3 points once smoothed).

## 6. Keeping long capture jobs alive
- On Windows the tools call `SetThreadExecutionState(0x80000001)` (ES_CONTINUOUS | ES_SYSTEM_REQUIRED), which blocks
  idle sleep while the process runs and changes no setting; closing the lid or a manual Sleep still stops it. On the
  Mac use `caffeinate -i` around the command. The original `goalcam.py` called the Windows function unguarded (around
  line 238); the kit copy wraps it in a try, so on the Mac start it as `caffeinate -i python3 goalcam.py run ...`.
- Retry page loads every 15 s; restart a crashed camera after 5 s; a background waiter reports at kick-off + 10 min.
- Run always-on jobs outside the chat session (Task Scheduler on Windows, launchd on the Mac) and check them before
  every match night. Why: a short internet outage once killed 3 of 6 cameras (the hide rule threw on a null page head and
  took the threads down, before the restart loop existed), and later the archive and a goal-cam relaunch both stopped
  at the same minute (exit code 4, cause unverified, possibly the chat session closing).

## 7. Sound for borrowed clips (scene beds)
- If a clip's sound is the moment's own audio (crowd, commentary, our filming), keep it. If it carries someone else's
  song (a song title, or another account's "original sound"; a spectrogram shows laid-on music), mute it and build a
  scene bed from the house CC0 sounds. Silence is weak; someone else's song is not ours to use.
- `python3 beds.py btc <out.wav> <dur> <close_at>`: heartbeat at -10 dB at 0 and 11.4 s, tick/tock every 1 s at -6 dB
  up to the close, a hit at -4 dB + a ding at -8 dB at the result.
- `beds.py goal <out.wav> <dur> <goal_at>`: stadium bed at -12 dB, crowd roar at -2 dB on the goal.
- `beds.py press <out.wav> <dur>`: crowd bed at -18 dB, photographers' shutters at -6 / -9 dB.
- `beds.py tv <out.wav> <dur>`: a match on a TV in the room at -16 dB (lifestyle clips).
- The builder normalises the mix to about -14 LUFS. The house set: 46 WAVs, 48 kHz 16-bit mono, leading silence
  trimmed, peaks at -3 dBFS, hit points in `sfx.json` (`hit_offset_s`), licences in `assets/sfx/LICENCES.md`; sources
  Kenney (6 packs, 470 files, CC0) and Freesound filtered to CC0 with the licence re-checked on each page (originals
  need a login, so the scripts took the HQ preview MP3s). No casino, slot or "gamblecore" packs.
- `beds.py` imports the studio's `sfx.py` and needs the house WAVs (media: copy them or rebuild the set).

## 8. The DevTools engine and the first formats (kept for reuse)
- `ocs.py scan | plan | build | sheet` drives the older studio over 21 still recipes and 20+ video recipes (the main ones
  are listed below; `studio/README.md` has the rest).
- `render.py` (the engine: references/render-pipeline.md section 2), `formats.py` (card builders), `motion.py` +
  `templates/motion.html` + `templates/motion_more.js` (GSAP timelines, a look kit, impacts, a timeline cue sheet),
  `sfx.py` (synth SFX, the house-sound mixer, cue sheets), `gallery.py` (a review page over several batches),
  `selftest.py` / `videotest*.py` (render checks: `python3 videotest3.py sheet [names]`, then `video [names]`).
- Card recipes built: matchday chances, pick a side, race swing, guess the %, "the market says", tier list, ranking,
  price tags, probability ladders, the one big number, cheapest outcomes, chart replay, upset, comeback, upset radar,
  fake vs real, the client's top 3, how-to over real app screens in a phone frame, our own P&L card. Video recipes:
  forecast, ball race, countdown, timer quiz, 100 games, line story, live tape, hot take, P&L film, app demo, AI vs the
  money, wheel, then vs now, tonight in 15 seconds, full-time line replay, favourites scoreboard, goal clip.
- Their designed look was rejected for native pages; use the engine and the timing rules (motion-design) for other
  clients' explainers, not these skins.
- Template bugs we fixed (keep the guards): quiz answers always in the middle (randomise); "a 18%" (an a/an helper);
  "Other" rows; colour clashes between team colours (an override table + a pair picker); a how-to that covered the
  chart (moved into a phone frame); a legend over the footer; an empty first frame (start 0.5 s in); asterisks from the
  colour markup leaking (parse markup with a small state machine); a hot take showing one player while naming another
  (camera hold range fixed).
- `motion.html` loads GSAP 3.12.5 (`assets/js/gsap.min.js`, GreenSock standard licence): re-download it or ship it.

## 9. Extending
- **A new data detector** (for the story finder): read the archive, emit candidates with the numbers and their times,
  never post a placeholder mid, add the app-label check.
- **A new house-look format:** extend the newsdesk fork (not the music newsdesk), one test post, one sheet.
- **Tagged clip libraries** (planned): reactions (20 to 30 clips of 2 to 6 s, green screen where possible, moods:
  crying, shocked, stunned, smirk, laughing, devastated fan, frustrated manager, "calma", "this is fine"), characters,
  lifestyle, pundits. Log every borrowed file in `footage/borrowed/SOURCES.md` (URL, author, post date, views,
  content, where burned-in text sits, duration, size, audio, licence); keep the untouched `_src` copy next to the cut.
- **Event kits** (planned): a dated-hook kit filmed from a TV and a phone with the market open (for example a central
  bank decision day).
- Risks the boss owns (client file): gambling and finance rules per platform, the editor's country's law on money-game
  ads, the accuracy of the client's own CTA claims (the `brand.json` CTA still carried a claim research found
  inaccurate), borrowed match, film and streamer footage, and the terms of third-party mirror sites used for reading.
