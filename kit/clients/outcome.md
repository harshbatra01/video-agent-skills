# Outcome (outcome.xyz): faceless, automated posts for a prediction market

Client file for the boss's Claude. Sources: Kanishk's chat of 13 to 14 Oct 2026, his memory notes and the files on his
PC (checked 14 Oct 2026). Dates and times are IST unless marked UTC. "The user" = Kanishk.

## Start here

- **Status (14 Oct 2026):** sample pack v2 (9 posts in the vc-news house look, built in the `newsdesk` fork) is on a
  private review page waiting for a keep-or-cut verdict ("Tell me which ones to keep or cut"). Several of its posts are
  date-bound and already stale: posts 3, 4, 5 and 8 say "today, 14 Oct", post 9 says "tonight", post 6 says "12 days".
- **Rejected before that:** all studio data cards ("these are all SAME types of posts bro") and all motion-graphic
  videos ("the UI is bad", "not worth posting", "I can't watch them"), and a TikTok-style white text box ("TOOO off
  beat").
- **Down right now:** the price archive stopped at 17:45 IST on 14 Oct and the goal-cam relaunch failed (exit code 4)
  before that night's matches. Real traders' usernames are on HOLD with the client; the plan page's decisions are
  unanswered.
- **Very next step:** ask Kanishk for the v2 verdict (he shares the page with Jaden). Refresh the numbers on any kept
  post on its posting day or rebuild it as `_v2`. Get answers to the open decisions (pages, platforms, account type,
  footage policy, real trades, closing line). If match nights matter, the archive and the goal cam must be restarted
  (on Kanishk's PC: `start_archive.bat`; on a Mac: `start_archive.sh` from the kit copy, ideally under launchd).

## What the client is and wants

### The product (research 01, 13 Oct)
- outcome.xyz is a front end and market deployer for Hyperliquid HIP-4 outcome markets: Yes / No (or team A / draw /
  team B) tokens; the price is the chance; a correct share pays 1 USDC. The app shows % chance, cents in the order book,
  button multipliers ("YES 2.44x") and "$100 -> $375" payout lines.
- Markets: football (UCL matches, EPL and UCL winners, the Ballon d'Or), US sports (NFL games and the Super Bowl, the NBA
  winner), crypto (BTC / ETH / SOL / HYPE 15-minute and daily up/down, "BTC touches X"), macro and markets (oil, gold,
  silver, S&P 500, US100, single stocks, the Fed decision, the Anthropic IPO first-day market cap).
- Size: HIP-4 weekly volume about $14.7M (Polymarket: about $3.6B); about 26 to 27K followers on X, 48 on Instagram,
  6,313 in Discord; no TikTok or YouTube; a "Trade to earn" rewards programme.
- Company: operated by TytanTech Corporation (Panama), pseudonymous team, no licence found. Terms block the US, UK, UAE,
  Singapore, Hong Kong, South Korea, China, Ontario and Belgium (plus EU states where not permitted) and ban VPN use.

### The brief (`C:\VISION\OUTCOME\Faceless-Formats.pdf`, `Outcome Formats.pdf`; digest in `research\00-client-brief.md`)
- Vision Clipping markets Outcome with FACELESS posts produced automatically, the way vc-news runs the rap pages.
- The client's 4 faceless formats: (1) How-to: a 5-slide carousel over real app screenshots; (2) P&L card edit: our
  card over a film-scene edit; (3) Top 3 traders: 5 slides with big 3D 3 / 2 / 1 numbers over the profiles; (4) Trader
  story: 4 slides (its Drive folder needs a sign-in: "trader story i dont have acesss either").
- Also a UGC (talking-head) formats doc and the Outcome Creator Guide: about 1 minute (finance 40 to 60 s); the hook is a
  hot take, a shock or a bold question; the plug lands at 50% to 70% and lasts 8 to 10 s; music is named (Mozart's
  "Lacrimosa", "Lucifer Waltz", Yvesnord, "Just Asking at night", "Last Surprise" for the wheel).
- **Client rules:** close with "Trade with zero fees on Outcome.xyz"; never say "bet" or "betting"; never cover the
  graph, the lines, names, the logo or buttons; no profit promises; "not financial advice" on finance; realistic money
  (title under $10k, trades about $1,000 or less, the real event shown); "#ad" first in captions.
- **Audience:** the client handles countries ("the project is already running. so countries are taken care of dont
  worry"). Never raise geo again, never aim at blocked countries, never hint at VPNs.

### What the user wants (and how it changed)
- 13 Oct: faceless formats, automated, with variety. After the first cards: "these are all SAME types of posts bro":
  wanted video bits, motion design, innovation, variety, formats a random viewer gets in 2 seconds.
- 13 Oct night, after the motion videos: "the UI is bad", "not good posts", "not worth posting", "I can't watch them",
  "no intention or reason to go well", "I don't think you researched enough". Wanted instead: viral formats a random
  viewer understands at a glance, modelled on what UGC creators and prediction-market brands actually post, translated
  to pages with no creator on camera. It does NOT have to be pure faceless: background clips, lifestyle footage, movie
  edits, aura edits and other people's clips are fine, as long as no creator is on camera. "Look at Outcome's branding
  and use it". Do not patch weak posts; research first.
- 14 Oct: "based on research do the best formats cook them up". Text style: the vc-news house look, not the brand look
  and not the TikTok box.

### Who gives notes, who does what
- **Kanishk:** decisions and taste, logins in the built-in browser, keys and throwaway cookies, keeping the PC on for
  match nights, sharing review pages with Jaden, posting with in-app sound.
- **Jaden and the client:** approvals and client-side permissions (usernames, CTA wording, brand kit, footage policy,
  platform permissions).
- **Claude:** research, the data jobs, sourcing, writing, building, checking, review pages, status files and memory.

## Formats and specs

### Sizes and shapes
- Instagram carousels 1080x1350, 5 to 8 slides (10 for rankings); TikTok photo mode, 5 slides. Videos 1080x1920, 30 fps.
- Carousels carry numbers and short clips carry moments: make both (TikTok video gets 5.6x the views of image posts;
  Instagram carousels 6.9% engagement vs 3.3% for Reels, about 9x the saves of single images; 16 of PolymarketFC's top
  20 posts are carousels or photos).
- Slide 2 is a second cover (Instagram re-serves a scrolled-past carousel from slide 2): its own hook and the key number,
  never "continued". Keep the number identical on every slide.
- Lengths: memes and moments 6 to 20 s; story posts 25 to 60 s (9 of the 12 highest ratios were under 20 s). v2 videos
  ran 8.8 to 17.5 s.
- A borrowed 16:9 clip can sit letterboxed on a black 9:16 canvas with the hook in the black space (23 of 71 measured
  TikToks are not 9:16). In vc-news `uk` blur mode wide clips sit at 40% height above the headline; tweet videos put the
  clip under the card.

### The plan (plan page, 14 Oct): 13 native formats plus the client's, on the same rules
- **(A) The number as the punchline:** "The money said 79%. Then this happened."; then vs now under a reaction face
  (6.14M on 1,640 followers); the "How did he know" smirk edit; a reaction clip plus one line (488K on 4,010).
- **(B) The real app as footage:** a BTC POV with the live screen and one emoji (647K on 622); a collapse filmed off a
  screen (510K on 2,850); a meltdown over the match page using a borrowed reaction clip.
- **(C) Borrowed footage plus one real number:** "I was 80% happy" (Real Madrid, 2.58M); "He says X, the money says Y"
  (1.5M on 109K); the "hits different" lifestyle POV (4.36M); aura and football edits with a number beat (waits on the
  footage decision).
- **(D) Carousels and text:** one star per slide (23.9M); "More likely than" (30,979 likes); RIP cards; price polls.
- **The client's formats kept on the same rules:** P&L card over an aura edit (229K on 1,180); hands-only how-to (2.81M
  on 12.8K); whale story (2.01M on 65.8K).
- **Skip:** whale alerts, daily wraps, higher-or-lower, "if you invested", broadcast clips with a % banner, weather skins
  as a hook, "Day N of turning $100 into...".
- **Why (research conclusions):** rounds 1 and 2 (13 Oct, stats and thumbnails only) found that topics and game
  mechanics beat "odds" content (#ballondor 34.45B views vs #footballodds 1.6M), whale alerts get 0 to 4 likes, daily
  wraps under 300 views, then-vs-now boards did 96x on a 3.93K page, stat face-offs 80x, plain countdowns 10x to 105x
  while odds-titled ones got 0.22x, and partner hits use the real app screen. Round 3 (14 Oct, about 350 to 400 real posts
  checked as frames) is the one that counts: the number as the punchline, a real moment first, most posts without a
  number, the real app as the device, house-look text (Kanishk's call).
- **Daily mix per page:** 4 moments or memes (no number, or one as the joke); 2 punchline posts; 1 real-app post;
  1 carousel; +2 the morning after a match night. The app shows up in about 1 of 6 posts, as a short insert, and never
  as a number on the cover.
- **Volume:** one account per sport (one football page first, then crypto and macro); 1 to 3 posts a day per page while
  testing; 5 posts per launch format over 2 weeks; judge a format after 30 to 50 posts, not 5.

### Native text rules (measured: our 22 videos vs 49 no-face TikToks)
- 4 to 9 readable words at a time (ours had 10.5, native 4), nothing tiny (under 1.8% of frame height: ours 27, native
  0), text mid-screen (native centre at 50% of height; ours 26%), inside x 120 to 918 and y 270 to 1250.
- Cover text inside the central 1080x1350 band (Instagram crops the grid to 3:4 since Jan 2025).
- At most 2 text sizes, nothing under 40 px, nothing in the bottom 20% or the right 160 px.
- The source and risk lines go in the post caption. No text on the app's chart, logo or YES / NO buttons (client rule).
- Burn in at most one iPhone-style emoji, at the end of the hook, never in the brand's closing line.
- **House look:** the vc-news look (bold caps headline with coloured numbers, a tweet card over a clip, carousels), with
  the Outcome accent #1AFF57 (Signal Green) and the second accent #FF3B30. Headline per `newsdesk\captions.md`: lead
  with names, 6 to 14 words, facts only, `*number*` green and `^number^` red, at most one emoji.
- Show the chance the way traders see it: the real app screen (a recording, a crop, or filmed on a phone) or one number
  in the text. Never a designed % card, gauge, bar, race or weather icon.

### Motion and cutting rules
- Real movement only: motion comes from the footage or the live price line; 5% to 10% punch-ins on the number or the
  goal; hard cuts; something real moves in the first second. No slide-ins, wipes, 3D flips or counting numbers.
- Pick one native rhythm per format: memes, fan moments and screen recordings = one continuous shot with one line;
  edits = 3+ hard cuts per 10 s on the beat (ours sat in between at 1.1 cuts per 10 s, "the worst of both").
- Hooks are situations, shocks or a POV, never the market: 4 to 12 words, no greeting, no "odds", no venue name.
  TikTok's guidance: the proposition by 3 s, the hook landed by 6 s.
- The market goes in as a short insert framed as the stakes: brand on screen at most 25% of the runtime unless the app
  moment is the story; one Outcome mention at 50% to 70% (partner videos used the app for 1.5 to 8 s, 8 of 12 between
  about 20% and 77% of the runtime).
- Frame 0 is the cover: every number on it is final and true, never mid-count. Motion renders start 0.5 s in.
- Timing rules from research 21 (for data explainers on other clients; the Outcome videos that used them failed on their
  designed look, not their timing): a 2-second test (freeze frame 0 and frame 60: a stranger can name the subject, the
  number and why it matters); one idea per scene, 2 to 4 s, at most 4 things on screen; hero number at least 150 px,
  held still at least 0.5 s after it lands; text hold in seconds = max(1.0, 0.4 + 0.33 x words); headline at most 7
  words, 42 characters a line, 2 lines; the number reacts within 1 to 2 frames of the event; an impact = a 2 to 3 frame
  flash + a decaying 8 to 12 frame shake + a 105% to 112% punch in 4 to 6 frames + a hit sound, at most 2 per video;
  frame grid at 30 fps: tiny 4 to 6, normal 8 to 12, big 15 to 20, reveal 24 to 36.

### Sound
- Sound like a page owner, not a template: 130 of 148 native references run on "original sound" (105 under the page's
  own name). Bake in the moment's own audio (crowd, commentary, our filming), a voice, or a licensed track. No whoosh,
  tick and ding packs on native pages ("Fake sound" was one of 4 reasons batch 1 failed). No casino or slot packs and no
  "gamblecore" audio ("Let's go gambling" says the banned word).
- Check a borrowed clip's sound: "original sound" under the uploader's own handle is usually real audio; a song title or
  another account's "original sound" means music was laid on top (a spectrogram shows it): mute or replace it, never use
  someone else's song.
- **Scene beds from CC0 house sounds** (`newsdesk\beds.py`, used in v2 wherever a clip carried a laid-on song): BTC POV:
  heartbeat -10 dB at 0 and 11.4 s, tick/tock every 1 s at -6 dB up to the close, hit -4 dB + ding -8 dB at the result;
  goal: stadium bed -12 dB, crowd roar -2 dB on the goal; post-match: crowd bed -18 dB, photographers' shutters at -6 /
  -9 dB; lifestyle: a match on a TV in the room, -16 dB. vcn.py normalises the mix to about -14 LUFS.
- **House sound set:** 46 WAVs, 48 kHz 16-bit mono, leading silence trimmed, peaks at -3 dBFS, hit points in `sfx.json`
  as `hit_offset_s` (the attack for hits, the loudest point for whooshes and risers, 0 for beds). Sources: Kenney (6
  packs, 470 files, CC0) and Freesound filtered to CC0 with the licence re-checked on each page (HQ preview MP3s; originals
  need a login).
- The account type decides the music plan: TikTok business accounts only see the Commercial Music Library, many trending
  tracks are not cleared for business use, and baking a commercial song into "original sound" does not license it. Ask
  the client whether the accounts are business or creator accounts.

### Captions (in this order)
- "#ad" first; the fact line; an ask ("Too high or too low?"); the source and date ("Price from Outcome, 1 minute before
  kick-off"); "Not financial advice" on finance; optionally "Trade the outcome."; the clip credit ("🎥: @handle") and the
  photo credit; a `when` window.
- Every paid or per-view post: a plain "Ad" in its first line or frame AND the platform's toggle (the UK ASA and the US
  FTC both say the platform label alone may not be enough).

### Word-swap table (the client bans "bet"; TikTok reads slips, odds boards and winnings as gambling cues)
- bet / bettors -> call, took Yes / No, the money, traders; odds (in titles) -> chance, priced at, the money says;
  parlay / slip / ticket -> position, receipt (receipt only for a real Outcome position screen); lock / banker -> the
  money's favourite; cash out -> sold at 8¢, paid $1 a share; fade / tail -> with or against the money; "will happen"
  -> "is priced at". Drop entirely: money glitch, free money, side hustle, gambling, casino, jackpot. Receipt-style posts
  go on X and Instagram only.

### Data rules (Hyperliquid HIP-4 markets)
- Coin id = "#" + (10 x outcomeId + side), side 0 = Yes or participant A, side 1 = No or B (`#2120` = outcome 212, side
  0). The mid is the chance (0.663 = 66.3%). A mid of exactly 0.5 with no book is an untraded placeholder: never publish
  it. Skip a multi-way market unless its sides add up to 90% to 106%. Build titles from the description fields
  (`template:sportsContestResult` with `participantA|participantB|competition|scheduledStart`); clean featured names
  come from `outcome.xyz/api/incentives/current` (needs a full browser User-Agent). Drop duplicate listings from other
  venues. Never type a number by hand; time-stamp every slide.
- Archive prices while markets are live (history vanishes at settlement; only lifetime stats survive).
- Thin in-match markets go stale or flicker (Inter at 66% while 1-3 down): use goal-cam 10-second prices, else trades plus
  5-minute snapshots whose chances add to about 100%, a median filter, then the resolved 100/0.
- Captions match the app's own on-screen labels, not polled mids (Sabah polled at 52% but showed 70% on screen).
- Public, keyless endpoints: Outcome's own API `o1.outcome.xyz` (60 requests a minute: leaderboard, profile, portfolio,
  markets lookup, series, settled, top movers, live sports); Hyperliquid's info API (outcomeMeta, allMids, candleSnapshot,
  l2Book, recentTrades = last 10 only, userFillsByTime, WebSocket); Outcome's stats site; ESPN public JSON (scoreboards,
  goal minutes, form, pre-match odds); Binance and Coinbase candles; Google News and Federal Reserve RSS; Polymarket and
  Kalshi public APIs for comparison. Research 15 defines 15 story detectors with 37 working curl examples. Run collectors
  from a home IP (a fan site's code says Outcome's Cloudflare blocks AWS serverless addresses). The fan-built P&L card
  site has bugs: design reference only.
- A game-format draw is one weighted draw with a logged seed (by default the date): reproducible, not staged, and say it
  is a draw.

### The brand (brand.outcome.xyz, saved verbatim in `research\raw\26\brand\pages\` because the site later answered 403)
- App colours: background #0B0C0F, text #F5F8FF, YES / UP #99FFBC, NO / DOWN #FF3D5E, live #FF0051, rewards gold
  #FFD699, logo mark (app icon only) cyan #00FFFF over magenta #FF00F2.
- Marketing palette: Signal Green #1AFF57 (hero), Deep Forest #055D1C, Violet Ultra #8952EE, Twilight Indigo #240F4C,
  Near-black #171717, Off-white #F5F5F5, High-Vis Yellow #E6FF2F, Rally Orange #FF8825, Protest Pink #FF9DBE, Executive
  Teal #04AC7D, Protocol Blue #03379D, Alert Red #FD6C6B (chosen to avoid casino feelings).
- Type: the app uses Inter; marketing uses PP Neue Corp Narrow Ultrabold (commercial; the site falls back to Bebas Neue).
  No shadows, outlines or tints on type. Photos go through their oil-paint stylisation; no stock photos.
- Voice: "quietly forceful", declarative, no exclamation marks. Banned: bet, wager, gambling, punt, payout percentages,
  casino framing. Lines to reuse: "Trade the outcome." (their fixed closer), "Outcome settled. Traders paid.", "Whose side
  are you on?", "Is this market mispriced?".
- The user chose the house look over the brand look for the text style.

## House look and taste rules (with the verdicts)

- **The number is the punchline or the stakes, never the product.** A price alone is not content (Paddy Power's own price
  posts got 4 to 13 likes; its banter with a number as the punchline 2,911 to 23,133). One number per frame, attached to
  a face or a moment; brackets for tags "(2%)"; absurd sizes travel (0.1%, 2%, 9%, 92%). The user on the v1 cards:
  "These are not good posts. It's not worth posting them."
- **Most posts carry no number:** moments and memes build the audience, number posts spend it (none of Polymarket Sports'
  20 most-viewed TikToks mentions a price).
- **The winning shape:** "the money said X%, then this happened": a longshot that landed or a favourite that fell, with
  the chance next to the moment that decided it. Two numbers side by side make tension (line vs result, then vs now,
  cost vs payout). A favourite that simply wins has no story.
- **Pick the number format by goal:** label memes earn shares, receipts earn saves, a favourite-on-a-loser post earns
  quotes, price polls earn replies.
- **Variety means different kinds of posts, not different skins.** The look kit (weather, broadcast, tabloid, paper,
  terminal, neon) read as a motion-template pack and was rejected: one text treatment per page; vary the format, the
  footage and the moment.
- **Avoid the ad tells:** no logo or brand name on frame 0; no template chrome (avatar-and-handle header, category pills,
  slide counters, footers, legal lines); no designed card or dashboard in place of a moment; no stock footage as
  wallpaper; no slide-ins, wipes or counting numbers; no pitch on screen ("Trade now", URLs, "zero fees", payouts); no
  whoosh or ding packs; text reacts, it does not explain.
- **TikTok white rounded box with black lowercase text: out.** "i dont like this text style bro its TOOO off beat", even
  though research said the hits use it. The user's taste wins on look: show one mock frame of a new text style first.
- **Honest versions of viral lies, never the lie:** every number links to a live market with a date; real settled trades
  only; losses as honest as wins. The WSJ (Jun 2026) found 778 of 1,105 Polymarket TikToks showed trades filmed on copies
  of the app; a fake "53% odds" screenshot of a market that never existed went viral. The client brief's "Sankey" format
  (a faked DM with an AI-written reply) was skipped. AI answers must be real model replies based on real form data
  (ESPN).
- **Keep supercar and luxury footage away from the product** (it reads as "trade to get rich", which the client bans);
  the lifestyle slot uses a lounge with the match on TV and a POV that keeps it the viewer's call. A Lambo version of
  post 9 was offered for comparison; the verdict was pending on 14 Oct (open question for Jaden), so keep this default.
- **A "How did he know" smirk edit is honest only when a price really moved before the news** (otherwise it implies
  insider knowledge; insider-timed trades drew Congressional letters in 2026). Log the time of the price move and of the
  news.
- **Formats with no proof go in a "Tests" section, never the opening slot** (the weather skin flopped: Saints 4.8K on
  172K, FOX Weather 902 on 1.08M, a crypto weather report 1 view).
- **Check outside facts on the posting day:** player facts change (Salah left Liverpool for Trabzonspor in Aug 2026);
  "last night" and "in 12 days" posts expire.
- **Benchmarks to copy:** PolymarketFC on Instagram (325K followers, 1.21B views in 12 months, about 10.7 posts a day, a
  typical post about 0.96x its follower count; hits are carousels with one star per slide, a giant %, a money line, the
  real app chart last; its Yamal post showed 55%, 51% and 50.8%, a mistake to avoid); kalshi.sports on TikTok (real fan
  or press footage, one caption, 8 to 17 s, 494K to 934K organic views a post on 7,516 followers). Co-author Instagram
  posts with @outcomexyz so its profile collects the views (needs the client's OK). Discount bought reach: organic hits
  run at 5 to 12 likes per 100 views; mark posts at about 0.1% likes per view or lower as "likely promoted".

## Every deliverable and version, with status

| When | What | Where | Verdict |
|---|---|---|---|
| 13 Oct 10:46 to 11:43 UTC | studio data cards: a 9-post dry run, a 14-post sample day, an 18-post showcase (matchday card, pick a side, race swing, quiz, "the market says", tier, ranking, price tags, cheapest dreams, IPO and BTC ladders, chance race, Upset Radar, Fake vs Real, Top 3 traders, How-to, P&L card) | `studio\FINALS\2026-10-14_SAMPLE`, `studio\FINALS\2026-10-13\@yourpage`, gallery v1 | REJECTED: "these are all SAME types of posts bro" |
| 13 Oct 12:00 to 21:34 UTC | 12, then 14, then 15 videos, plus 7 morning-after videos: 40 posts on one page (forecast weather report, weighted-draw ball race, countdown, timer quiz, 100 games, Fed line story, BTC live tape, hot take, P&L film, app demo, AI vs the money, wheel, 2 then-vs-now boards, "tonight in 15 seconds"; morning after: 3 replays, a favourites scoreboard, 3 goal-cam clips) | `studio\FINALS\2026-10-13b`, `studio\FINALS\2026-10-14_after`, gallery v2 to v6 | REJECTED: "the UI is bad", "not worth posting", "I can't watch them" |
| 14 Oct 00:11 UTC | plan page with TikTok Sans white-box mocks | plan page | text style "TOOO off beat"; the formats taken as the direction |
| 14 Oct 03:39 UTC | **v2: 9 house-look posts** (7 videos, 1 carousel, 1 card, a Premiere XML per video) | `newsdesk\FINALS\2026-10-14_pack\@yourpage`, v2 review page | PENDING: "Tell me which ones to keep or cut" |

**The 9 v2 posts:**
1. BTC POV, last 15 s, $107 above the line (tweet card over our app recording, clock bed).
2. Sabah 21% to 70% after one goal (goal-cam footage, tweet layout so the chart stays clear).
3. "INTER WERE 79% TO BEAT BRUGGE. BRUGGE WON 4-3" (uk headline over the 87th-minute winner).
4. "BAYERN FANS RN (86% TO WIN BEFORE KICK-OFF)" (a keyed devastated-fan reaction over a fan-cam of Viking's 3-3
   equaliser).
5. Yamal 43% on 5 Oct, 30% today (over his Player of the Match clip).
6. Ballon d'Or 6-slide carousel: Kane 63%, Yamal 30%, Dembele 2%, Messi 2%; the last slide is the real app card.
7. "The Fed raising rates this month (19%) is more likely than Liverpool winning the league (4%)" (tweet card).
8. "BRUGGE FANS WHO CALLED IT AT 7%" (smirk label meme with The Mentalist's smirk, Brugge fans' sound).
9. "pov: City v PSG tonight and you called City at 45%" (lounge lifestyle clip).
- All v2 posts use placeholders until the client decides: page identity "@yourpage" / "Your Page" with a dark "YP"
  avatar, the CTA in one config line, trader usernames masked. Undelivered drafts were moved to `_superseded`, not
  deleted. Before posting: the real handle and avatar, fresh prices on the day, the usernames OK.

**Review pages (private artifacts in Kanishk's account; he must share them with Jaden):**
- Gallery (v1 cards and videos, 6 versions on one link): https://claude.ai/artifact/9bgYzLmZ8rz8DtWgC8JG77
- Plan (13 native formats, the look, the posting system, 5 decisions): https://claude.ai/artifact/ReJnugLoXrDFPwCK5W9ndb
- v2 pack: https://claude.ai/artifact/DPG6G2GUmm88AmhWkgRPMp
- Their HTML sources sit in the old session's Temp scratchpad
  (`C:\Users\Kanishk\AppData\Local\Temp\claude\C--VISION-IMMUFIX-repair-ENCODED-RUSHES\650ebeeb-994f-4ee8-940d-d300a001745a\scratchpad\`
  folders `gallery_1013`, `plan_v2`, `pack_1014`): copy them out if the links must be republished. Republish from the
  same path to keep the URL.

## Review history, round by round

- **Intake (13 Oct):** 3 agents read the client files, followed every link, checked the live product read-only and
  fact-checked the brief. Findings for Jaden: "zero fees" is not accurate (opening is free, but about 0.05% to 0.14% on
  close or settle since about 5 Sep 2026); "world's fastest" has no benchmark (only Hyperliquid's 0.2 s median latency
  exists); a star trader named in the brief is not on the leaderboard; the "demo format" link is a Pump.fun clip; one
  example account was gone; the Trader Story folder needs a sign-in. India's Online Gaming Act was raised once; the user
  said countries are handled.
- **Round 1 (13 Oct, the 18-post card showcase):** "these are all SAME types of posts bro". Done: 6 video formats with
  their own looks and baked-in sound, plus footage formats (live app tape, hot take over a photo, P&L edit), stock clips
  and CC0 sounds, the goal cam, a 40-post review page.
- **Round 2 (13 Oct night, the videos):** "the UI is bad", "not good posts", "not worth posting", "I can't watch them",
  "I don't think you researched enough". Done: research round 3 (5 agents, about 350 to 400 real posts checked as
  frames, 3M tokens), a measured diagnosis of our own output (8 ad tells), the plan page. "Nothing new gets built until
  you've decided."
- **Round 3 (14 Oct, the plan page mock):** the TikTok white box "TOOO off beat"; "based on research do the best formats
  cook them up". Done: v2 in the house look in the newsdesk fork, 9 posts, a review page.
- **Round 4:** the v2 verdict is pending.

## What went wrong and the fix

**Rejected output**
1. The 18 data cards were "all SAME types": one family of designed cards with light animation and the number as the
   product. Fix: video and footage formats. Rule: vary the kind of post, not the card.
2. The motion videos were rejected: a designed look (dashboards, skins, pills, about 37 words on screen, SFX packs), and
   rounds 1 and 2 never looked at frames. Fix: frame research, a measured diagnosis, the plan page. Rule: a plan page with
   proof frames before building; measure text density against the references.
3. The TikTok box text was "TOOO off beat": research was followed over the user's taste. Fix: the house look. Rule: one
   mock frame first; the user's taste wins on look.

**Sourcing**
4. YouTube blocked every route on 13 Oct (PO token, embed Error 153, the headless-player fallback `ytgrab.py`). No fix;
   sourcing moved to TikTok mirrors and our own recordings. Rule: ask early for a throwaway account's cookies or for clips
   from the user.
5. X goal clips were deleted (404) and a broadcaster's post had only a thumbnail. Rule: download the same day; prefer
   broadcasters' own posts or our own recordings.
6. Stock was blocked or restricted (Pexels and Pixabay 403 without free API keys, Coverr's API needs a key, Mixkit 429 and
   "Restricted" = personal use only, which ruled out most Bitcoin, chart, neon and named-city clips). Fix: Mixkit Free +
   Coverr tag pages; 11 of 45 clips rejected (boot brands, sponsor boards, faces in focus, a sponsor logo in a skyline,
   TradingView / KuCoin / Binance screens; the Eiffel Tower's night lighting has a copyright claim). Rule: ask for the
   free keys; frame-check every clip; stock is filler only.

**Code and environment**
7. Heredoc and sed escaping broke patches 5+ times (motion.py, ocs.py, goalcam.py, gallery.py, a vcn.py sed). Fix:
   Write/Edit with a parse-check first.
8. A nested template literal inside a JS ternary broke a template. Fix: parentheses or concatenation, then an esprima
   check (no Node on this PC).
9. An Italic fallback font got picked. Fix: a recursive font search that skips Italic files; variable fonts at weights
   100 to 900.
10. UTF-8 printing failed: `python -I` ignores PYTHONIOENCODING. Fix: `python -I -X utf8`.
11. Removing pop-up DOM nodes crashed outcome.xyz (React re-render). Fix: click the close button, press Escape, then a CSS
    hide rule. Rule: never delete nodes on someone else's app.
12. The 12:15 UTC BTC film was unusable (a sign-in modal and a separate 12 px blur layer came back). Fix: hide
    `[role=dialog], [role=presentation][data-open], [data-radix-portal], [data-overlay], [vaul-drawer],
    [data-vaul-overlay]`, restore scrolling, re-apply every 15 frames null-safe, and run a 4 s test film before any timed
    window. The 12:30 film was clean.
13. Git Bash turned `/markets/...` into a Windows path. Fix: full URLs or `MSYS_NO_PATHCONV=1` (not an issue on a Mac).
14. The How-to failed in a batch: two Chromes shared a profile. Fix: one profile per port.

**Data**
15. HTTP 400 on a profile lookup (anonymous leaderboard rows): skip them, take the next trader.
16. Wrong market names: `coin_name` read the wrong JSON path. Fix: `data.markets.<id>.outcome`.
17. Wrong P&L numbers. Fix: the read-back starts from the market's `firstTrade`; we make our own cards because the fan
    site's cards had bugs.
18. v1 design bugs, each fixed: quiz answers always in the middle (now random); "a 18%" (an `a_an` helper); "Other" rows;
    colour clashes (`OVERRIDE` + `pair()`); the How-to covered the chart (moved into a phone frame); a legend over the
    footer; an empty first frame (0.5 s lead); markup asterisks (a state machine); a lingering question; upside-down wheel
    labels; a hot take showing Messi while naming Yamal (the camera now holds at x 0.6 to 0.66).
19. ESPN matching failed on "Atlético" twice. Fix: strip accents (unicodedata NFKD, drop combining marks; Bodø/Glimt is the
    same trap).

**Goal cam and replays**
20. The goal cam lost 3 of 6 matches in a DNS outage (00:28 IST, 13 Oct): the hide rule threw on a null head and killed
    the threads. Fix: a null-safe hider, page retries every 15 s, a restart loop.
21. False goal-cam events from thin-book flicker. Fix: the median hold test plus 90 s spacing (it dropped all 3 false
    flickers).
22. Replays showed wrong in-match prices (Inter 66% while 1-3 down). Fix: goal-cam 10 s prices, filtered trades and
    snapshots, then the resolved 100/0.

**Posts and files**
23. `batches\2026-10-14.json` was overwritten (no check before writing). Fix: rebuilt exactly from the transcript (the
    original Write plus each Edit). Rule: `ls` first and unique batch names.
24. The Sabah post: the uk headline covered the app chart (a client rule) and the caption said 52% while the app showed
    70%. Fix: the tweet layout and the on-screen label.
25. Smeared logos above a tweet card (the blurred fill copied the app recording). Fix: `"bg": "black"`.
26. The green-screen key clipped a shirt, then showed a straight edge from the template itself. Fix: a full-width key,
    with the figure pushed so that edge sits on the frame edge.
27. Borrowed clips carried other people's songs. Fix: scene beds from the house SFX.
28. An unverified hashtag count sat in an example post. Fix: a placeholder until read live. Rule: no unchecked number in
    any draft.

**Process**
29. The shared WebSearch budget (about 200) ran out on 4 of the 5 round-3 agents. Fix: those items marked UNVERIFIED.
    Rule: split search-heavy tracks and plan a follow-up turn.
30. The archive and the goal cam stopped at about 17:46 IST on 14 Oct (goal cam exit code 4). Cause unverified (possibly
    the session closing). No fix yet. Rule: run always-on jobs outside the chat (Task Scheduler on Windows, launchd on a
    Mac) and check them before each match night.
- Also: a parallel session reverted the Outcome memory index line once (13 Oct): re-read memory before editing it; keep
  `research\00-status.md` current at every phase.

## Open items and next steps

1. **The v2 verdict** (9 posts). Refresh numbers on the posting day or rebuild expired posts as `_v2`.
2. **The plan page's decisions, unanswered:** pages and platforms; business vs creator accounts (this decides the music);
   the footage policy and who supplies clips; whether real trades are shown and usernames hidden or shown; the closing
   line ("Trade the outcome." vs "zero fees"), the brand kit and the PP Neue Corp font files.
3. **Client questions via Jaden:** the usernames HOLD; the CTA wording ("zero fees" is inaccurate as written; the CTA
   lives in one config line, `brand.json`, which still says "zero fees"); platform permissions (TikTok One and a
   Registered Business Account for gambling or finance branded content from 31 Aug 2026; TikTok's prediction-market ad
   policy needs trading or event-contract wording; Meta's written pre-authorisation for real-money gambling and crypto
   branded content; on YouTube links, logos and spoken mentions of uncertified gambling sites are banned since 19 Mar
   2025, so do not show, say or link Outcome there until the client confirms how Google classes it; X bans gambling in
   paid partnerships since Feb 2026); the on-screen ad label wording; co-authoring with @outcomexyz; licences (Mixkit and
   Coverr for paid promotion of a prediction market, Epidemic's scope, the borrowed match, film and streamer clips:
   "Match, film and streamer clips are the client's decision", asked 14 Oct).
4. **The always-on jobs are down** (see Start here). They were down ahead of LASK v Liverpool (22:15 IST) and Man City v
   PSG, Roma v Real Madrid, Villa v Fenerbahce and Bodø/Glimt v Dortmund (00:30 IST) on 14 Oct.
5. **Not built yet:** the daily story finder for the native formats (upsets, longshots, biggest moves, then vs now,
   captions written); tagged clip libraries (reactions, characters, lifestyle, pundits; the reaction library should hold
   20 to 30 clips of 2 to 6 s, green screen where possible, moods: crying, shocked, stunned, smirk, laughing, devastated
   fan, frustrated manager, "calma", "this is fine"); real "then" screenshots on a timer; a Fed-day kit for 28 Oct (a TV
   and a phone with the market, filmed from 18:00 UTC); a Lambo version of post 9; follow-ups for "AI vs the money" day 1
   (the AI picked Atletico and the wheel picked Barcelona: both were right) and the forecast check.
6. **Upgrades to ask for:** free Pexels and Pixabay API keys, a free Freesound login, a throwaway YouTube cookies file
   (never a personal account), X and Instagram logged back in inside the built-in browser (Claude never types
   passwords), the client's brand kit and the PP Neue Corp files. AI B-roll (Higgsfield) costs credits: ask first.
7. **Housekeeping:** nobody has tested importing the newsdesk Premiere XMLs; `vcn.py drive` has never run for Outcome;
   `studio\_tmp_fetch` (856 MB) and `studio\out` (5 GB) can be cleaned (Kanishk's call; nothing was deleted).
8. **Research gaps (UNVERIFIED):** Instagram post numbers (views are hidden), TikTok's grid crop, the sound on Shorts,
   whether the Fed's press video is public domain.
9. **For the boss's Mac:** check that outcome.xyz and `o1.outcome.xyz` load from his location before relying on the
   capture and filming tools (Outcome's terms block the UK).
10. **Dated hooks to use:** US CPI 14 Oct 12:30 UTC; FOMC 28 Oct 18:00 UTC (the last move was a hike on 16 Sep); the
    Ballon d'Or 26 Oct in London ("who wins the Ballon d'Or" was the biggest football hook in Oct 2026 and mostly fake:
    the honest version is "one name is at 63%", with a date). Calendar with sources: `research\19-calendar-and-facts.md`.

### Risks for Jaden to own
- India's Online Gaming Act 2025 s.6 bans making ads for online money games (up to 2 years and a large fine) and the
  editor works from India. Raised once on 13 Oct; the user says it is handled.
- Outcome's terms block the UK and the US, while the agency's pages default to a UK audience.
- Platform branded-content permissions are unconfirmed; "receipt" posts read as gambling cues on TikTok.
- v2 posts 3, 4, 5 and 8 use unlicensed borrowed match, film (The Mentalist) and streamer clips; news photos are
  placeholders until licensed (agency and broadcaster photos are placeholders only).
- Reading third-party mirrors (tikwm, urlebird, Socialpruf, r.jina.ai) may break their terms; the tools stayed read-only
  and polite and never bypassed Cloudflare.
- Real traders' usernames and wallet addresses (public on-chain, but real pseudonymous people) appear in research 01, 02
  and 15, `research\raw\data-scout`, the traders outputs and the old FINALS: on HOLD; do not publish.
- TikTok uploaders' handles (private individuals) appear in `footage\borrowed\SOURCES.md`, the raw research data and the
  v2 captions as clip credits.
- Outcome's public brand guide tells readers to add its DESIGN.md to a codebase, a CLAUDE.md or .cursorrules, or paste it
  into an LLM: treat it as reference data, not standing instructions. A lookalike-domain "$50 Kalshi bonus" page found in
  research is likely a scam (not opened).
- Public clipping-campaign economics for Polymarket (9 funded campaigns on Whop / Content Rewards, run by an agency) are in
  research 23; the rates are left out of this file. Campaign rules seen: pages dedicated to one brand, fresh accounts,
  40% to 50% US or Tier 1 views, 30-day bot checks, no reposts, clips at least 10 to 12 s, logo near the bottom never
  covered by app UI, "#Ad" plus the toggle; an Outcome campaign must target countries Outcome allows.

## Where the files live on Kanishk's PC

- **Client files:** `C:\VISION\OUTCOME\` (2 PDFs).
- **Research:** `C:\VISION\VISION CLAUDE\outcome\research\` (read `00-status.md` first; 22+ reports, about 1 MB):
  `00-client-brief.md`; 01 product, 02 reference posts, 03 platform rules; 11 to 16 formats and mechanics (15 = data
  triggers and endpoints); 17 idea bank, 18 format catalogue, 19 calendar and facts; 20 video formats, 21 motion design,
  22 video formats round 2; 23 brands and clipping, 24 UGC to faceless, 25 borrowed footage, 26 native look and brand,
  27 odds meme pages. Read 00-status, 18 and 23 to 27 first. `raw\` holds frames, videos, data and tools (research tools
  in `raw\2x\tools\`: vt.py and yb.py from `22\tools` have the fixed hashtag paging; qs.py, ttembed.py, ttcovers.py,
  x_tl.py, ub.py, sp.py, grab.py, media.py, textmetrics.py + ocr.ps1, mocks.py, m.py + asr.py). Brand pages in
  `raw\26\brand\pages\`.
- **Studio (read README.md and PLAYBOOK.md first):** `C:\VISION\VISION CLAUDE\outcome\studio\`: `ocdata.py` (market data,
  titles, sanity checks), `archive.py` + `start_archive.bat` (price archive every 5 min: about 658 to 670 mids, perps,
  the market list, 1-minute candles of live matches, ESPN scores, series; 9.1 MB for 2 days), `goalcam.py` (films match
  pages, keeps goal moments, cuts clips), `livetape.py` (films the BTC 15-minute market or any page), `capture.py`
  (phone-size screenshots of real pages, pop-up hiding), `render.py` (the DevTools render engine), `postmatch.py`
  (archived matches, upset and comeback flags, replays), `facts.py` (ESPN form facts), `traders.py` (leaderboard, fills,
  P&L read-back; usernames on HOLD), `sfx.py` (synth SFX, house-sound mixer, cue sheets), the old card and motion studio
  (`ocs.py`, `formats.py`, `motion.py`, `howto.py`, `gallery.py`, `templates\studio.html`, `motion.html`,
  `motion_more.js`, tests; output rejected, parts reusable), `brand.json`, `batches\*.json`, `assets\` (teams.json with
  146 team colours and codes, players.json with 30 Ballon d'Or nominees, fonts, Outcome logos: client marks, Outcome
  work only), `footage\borrowed\` + `SOURCES.md`, `footage\stock\` + `LICENCES.md`, tapes `footage\goalcam_*.mp4/json`
  and `btc15m_*.mp4/json`, `data\archive\` (the only copy of the 13 to 14 Oct price history: it cannot be rebuilt).
  `motion.html` loads GSAP 3.12.5 (standard licence).
- **Newsdesk fork (the house-look builder):** `C:\VISION\VISION CLAUDE\outcome\newsdesk\` = a copy of vc-news with its own
  `brand.json` (placeholder identity), batches and Drive folder `G:\My Drive\OUTCOME POSTS VISION` ("never the rap posts
  folder"). Its `templates\card.html`, `captions.md` and `fetch.py` match vc-news; only `vcn.py` changed: a `react` layer
  (ffmpeg `chromakey=0x00FF00:0.16:0.08` then `despill=type=green`, optional crop, figure scaled to h = 860 to 900 px,
  overlaid bottom centre with x/y offsets, also written as `<id>_react.mov` qtrle ARGB, about 220 MB, on its own Premiere
  track) and clip `"bg": "black"` for app recordings. Plus `beds.py`. Batches: `2026-10-14_test.json`,
  `2026-10-14_pack.json` (the best example of every field). FCP7 XML per video: V1 the clip layer (`_base.mp4`), V2 the
  keyed reaction (`_react.mov`) when there is one, V3 the headline overlay PNG, A1 the audio WAV.
- **Memory notes (Kanishk's Claude):** outcome-project, feedback-outcome-native-viral.
- **Do not ship or share:** `studio\out\` (5.0 GB caches and goal-cam buffers), `studio\footage\` media (1.9 GB),
  `studio\_tmp_fetch\` (856 MB), `studio\FINALS\` (273 MB), both `_chrome_profile\` folders (may hold site cookies),
  `newsdesk\out\`, `FINALS\`, `in\`, `research\raw\23..27\` media and data (about 2.1 GB, with usernames),
  `research\raw\data-scout\` (wallet addresses), `studio\refs\` (other people's post covers), `studio\assets\emoji\`
  (licence unclear), `newsdesk\assets\accounts\` (other Vision pages' avatars).

## Which kit skills and pipelines to use for this client

- **Pipelines:** `~/VisionKit/kit/library/pipelines/outcome-studio/`: `studio/` (data, archive, goal cam, live tape,
  capture, render engine, postmatch), `newsdesk/` (the house-look builder: the fork's `vcn.py` with the `react` layer
  and `"bg": "black"`, `beds.py`, its `brand.json`, `templates/card.html` and the v2 batch
  `batches/2026-10-14_pack.json`) and `research-tools/`. The fork uses the music newsdesk's `fetch.py` and
  `captions.md` from `pipelines/newsdesk/` (identical copies were not duplicated). If the kit's copies are older than
  Kanishk's `outcome\` folder, ask him for the current ones.
- **social-video-formats:** native viral formats, faceless pages, the content bar, platform rules for gambling-adjacent
  clients, carousels vs clips.
- **research-and-sourcing:** research by frames (download real viral posts, timestamped contact sheets dense in the first
  3 s, Whisper transcripts, rank by views / followers, flag paid and co-authored posts), reading platforms without logins,
  borrowed clips, Commons photos, CC0 sound, licences.
- **production-automation:** the daily data-to-post routine, the archive and always-on jobs, review pages, forking a
  pipeline per client.
- **motion-design:** native text rules and real-movement rules (and the explainer timing rules for other clients).
- **editing-playbook:** the verdict library and the "plan page before building" habit.
- **premiere-ae-editing:** the FCP7 XML route and checks.

### How a faceless Outcome post gets made (state at v2)
1. **Intake:** read every client file, follow every link, check the live product read-only, write
   `research\00-client-brief.md`, fact-check the claims, start `00-status.md`. Look for the client's public brand guide on
   day 1 (try brand.<domain>) and save it verbatim.
2. **Research:** 5 or 6 agents on separate tracks, one report file each, using the frame-based method. Each brief: today's
   date and 3 lines of client context; "read these earlier files first, do not repeat them"; the exact output file and
   section order; allowed methods (WebSearch / WebFetch, public JSON, media-only downloads, one request at a time, no
   logins, no posting or liking); "every number gets a source URL and date", "mark UNVERIFIED", "never invent numbers",
   plain English, no em dashes; a budget of 70 to 90 tool calls and a 100 to 150 word reply. Cost seen: 58 to 83 min,
   185 to 313 tool calls, 590K to 660K tokens per agent.
3. **Plan page, then decisions:** formats with proof frames, the look, how the pages run, the open decisions. Build nothing
   big until the user answers.
4. **Always-on data (on the PC, lid open):** `start_archive.bat` all day; `python goalcam.py run Q405 Q407 ...` on match
   nights; `python livetape.py btc15` for BTC windows; `python capture.py market|home|profile` for app screenshots.
   Keep-awake: Windows `SetThreadExecutionState(0x80000001)` while the process runs (closing the lid still stops it);
   Mac: `caffeinate -i`. Page loads retry every 15 s; a crashed camera restarts after 5 s.
5. **Find the day's stories:** the morning after, `python postmatch.py list YYYYMMDD` (chances 1 minute before kick-off;
   upsets = winner under 35% at kick-off; comebacks = winner under 25% at half-time; goal markers snap to the biggest
   1-minute jump within 6 minutes of the ESPN minute); live prices and movers with `ocs.py scan`; ESPN form with
   `python facts.py uefa.champions 20261013 "Atletico"`; dated hooks from research 19.
6. **Pick formats** from the 13 native formats plus the client's 3, following the daily mix. Most posts have no number.
7. **Source footage:** our own app recordings first, then borrowed clips (find through the urlebird TikTok mirror; download
   with the tikwm single-video API; a contact sheet per candidate; cut the clean stretch with ffmpeg at H.264 CRF 17 with
   AAC kept and keep the untouched `_src`; log every file in `footage\borrowed\SOURCES.md` with URL, author, post date,
   views, content, where burned-in text sits, duration, size, audio, licence), the reaction library, lifestyle B-roll,
   Commons photos (CC BY-SA 4.0 needs "Photo: Name, CC BY-SA 4.0, via Wikimedia Commons"; portraits 1920x2880,
   landscapes 3840x2560). Agents never use the user's own Chrome or the built-in browser pane.
8. **Write** the headline and caption (rules above).
9. **Batch file:** `newsdesk\batches\<date>_<name>.json` (`ls` first): `fmt` (`uk`, `tweet`, slides), `headline`, `sub`,
   `label`; `clip` {path, in, dur, fx, fy, fill blur/crop, bg black}; `react` {path, in, crop, h, x, y}; `audio` {mode
   clip/song/mix, song, song_in}; `photo`, `focus`, `slides`, `caption`, `when`.
10. **Sound:** the clip's own audio when it is the real crowd or commentary; otherwise a bed
    (`python beds.py goal in\x.wav 13 6.0`).
11. **Build:** `python -X utf8 vcn.py build batches\<x>.json [--only ids]` writes `FINALS\<batch>\@<page>\NN_<id>` +
    `captions.txt`, and the Premiere layers and XML into `out\<batch>\premiere\`.
12. **Check:** `python vcn.py sheet <batch>` plus one combined frame sheet (split it if too tall to read); numbers must
    match the app's on-screen labels; no UI covered; crops and keys checked; rebuild only failures; delivered posts go to
    `_v2`, old versions to `_old_versions`, undelivered drafts to `_superseded`.
13. **Review page:** a private Artifact (small web copies, videos with sound, captions with copy buttons and posting
    windows, a "why it works" line with proof numbers and the data source behind every number, grouped by format, untested
    formats under "Tests"); say it is private and must be shared with Jaden.
14. **Verdict** (user, Jaden): keep or cut; record verdicts in memory and `00-status.md`.
15. **Posting (human):** refresh numbers on the day, the real page identity, in-app sound where needed, the "Ad" label and
    the paid-partnership toggle, co-author with @outcomexyz if agreed. `python vcn.py drive <date>` would copy to
    `G:\My Drive\OUTCOME POSTS VISION` (set up, never run).

### Filming the real app (the studio's tools)
- Headless Chrome at 390x844 CSS px, device scale 3, iPhone user agent; screenshots as fast as Chrome paints (about 10 to
  15 a second), retimed to a steady 30 fps. `livetape.py btc15` films the last 90 s of a 15-minute window plus 20 s
  after. `goalcam.py` films each match page at about 4 fps into a rolling buffer and keeps 150 s before to 60 s after each
  event. An event is an ESPN score change (polled every 20 s) or a home/away move of 8+ points within 60 s (polled every
  10 s); it must hold (the median of the last 30 s vs the median 60 to 120 s ago, at least 3 samples each); no two
  events within 90 s; match ESPN on the short name and the full label, accent-insensitive. Results seen: the 12:30 UTC
  BTC window filmed (2,015 frames, result UP); the goal cam caught Sabah 21% to 52/70%, Atletico 55% to 72%, Sporting
  31% to 55%; favourites won 5 of 9 on 13 Oct (Brugge at 7% won 4-3 at Inter; Viking at 5% drew 3-3 with Bayern).
- `render.py`: one headless Chrome per batch over the DevTools protocol (Python websockets) with a free port and its own
  profile per instance; templates expose `window.show(spec)` and `window.renderAt(t)`; each frame a
  `Page.captureScreenshot` JPEG at q93 piped into ffmpeg (`-f image2pipe -c:v mjpeg -i -`) to libx264 CRF 17, yuv420p,
  +faststart; GSAP timelines seeked per frame; fonts injected with @font-face. Speed: a 7 s chart video in 11 s; 18 posts
  (104 images, 14 videos) in about 4 minutes. The engine is solid; the designed look was what failed.

### Mac notes (untested)
- **Already fixed in the kit copies** (14 Oct; Kanishk's originals on his PC still carry the Windows paths):
  `studio/render.py` and the fork's `vcn.py` find Mac Chrome by themselves or read `CHROME_PATH`; the fork searches the
  Mac font folders plus `VC_FONT_DIRS`; the skill path reads `PAE_SCRIPTS`; the Drive folder reads `OUTCOME_DRIVE_DIR`
  (Mac: `~/Library/CloudStorage/GoogleDrive-<account>/My Drive/OUTCOME POSTS VISION`, never the rap posts folder); the
  XML file URLs work for `/Users/...` paths; `goalcam.py`'s Windows keep-awake call is wrapped in a try (run it as
  `caffeinate -i python3 goalcam.py run ...`); `studio/start_archive.sh` runs the archive under `caffeinate -i`;
  `textmetrics.py` reads `TEXTMETRICS_ROOT`. Settings: `pipelines/outcome-studio/.env.example`.
- **Still Windows-only:** `ocr.ps1` (Windows OCR; on a Mac use the premiere-ae-editing skill's `scripts/media/ocr`,
  Apple Vision built from `ocr.swift`, same JSON; or `ocrmac` / tesseract) and `textmetrics.py`, which calls it; `asr.py` uses CUDA (use CPU faster-whisper or mlx-whisper); `mocks.py` uses the
  Windows emoji and Arial font paths. `brew install ffmpeg`; run `python3 -X utf8`.
- Python packages: Pillow, numpy, websockets (sync client), av (PyAV); optional esprima, yt-dlp (+ Deno + bgutil for
  YouTube), faster-whisper.
- **Needs his own:** Google Drive for desktop (for `vcn.py drive`), optionally a throwaway YouTube account's cookies,
  Pexels and Pixabay API keys, a Freesound account, his own X and Instagram logins for reading, a Proxima Nova licence
  (Coolvetica licence to check, Bahnschrift to substitute), and a music licence that covers client posts.
