# Music pages: the rap news pages (@zonegbp and @beatswitchfm)

Client file. This is own product, not an outside client. Sources: the editor's chat
of 7 to 13 Oct 2026, the 14 Oct batch on disk, the editor's memory notes and the files on the editor's PC (checked 14 Oct 2026). Dates are
IST (UTC+5:30); posting windows are UK time. "The user" = the editor.

## Start here

- **Status (14 Oct 2026):** the daily routine runs: **1 video + 1 carousel per page per day**, built by the vc-news
  pipeline whenever the editor asks ("todays batch please"); nothing is scheduled. Latest batch: 14 Oct, built 19:10 to
  19:33 IST and copied to Drive (`RAP POSTS VISION\14 10 2026`): @beatswitchfm = Keffe D sentencing video (breaking:
  post as early as possible, by 17:00 UK) + an A$AP Rocky / Ferg carousel; @zonegbp = Lollypopbeatz's first freestyle
  video + "UK rap has the #5 song of 2026, but no album in the top 40" carousel with a Story poll.
- **Not known:** which of the 10 to 14 Oct posts actually went up. No performance numbers have come back yet (Insights,
  Story poll counts), and nobody has imported a Premiere XML from this pipeline.
- **Very next step:** on request, run the day's batch (vc-news README routine). Ask the editor for 24 h and 72 h Insights
  per post and for yesterday's Russ Millions vs A2 Anti Story poll count (a result post is ready to make). Before the
  reviewer runs the pipeline on his Mac: the kit copy is already patched for Chrome, font folders, the skill path, the
  Drive folder and the XML file URLs; he still sets `VC_DRIVE_DIR`, installs the fonts, signs in his own monitoring
  accounts and tests one post and one XML import (see the last section).

## What the client is and wants

### The business
- **Music promotion:** a client's track rides as the audio under niche posts on pages Vision runs (the network) or pages
  built for the artist (owned pages). The product is concentrated volume on ONE sound page in a short window; scattered
  posts on many sounds are worth little. Every post is manager-checked before it goes live.
- **Pitch video (20 Sep 2026, `presentation\Renders\v2 presentation.mp4`):** a network of fully owned pages; clients
  choose up to 2 niches; 7 niches run, only football edits and news and culture had open slots; pages target a UK
  audience by default, other geos as an add-on; clients send the MP3 or WAV before release plus their TikTok, Instagram
  and YouTube sound links ("so we can link it to all the videos"); a bank of edits is built; distribution starts on
  release day.
- **Packages (structure only; the amounts are in the client PDF):** entry tier (90 network posts, 1 song); standard
  (300 posts, up to 2 songs, 3 niches); premium (300 network + 90 on 3 owned accounts); top (450 network + 270 on 9
  owned accounts). A separate Creative Direction package. Add-ons: dashboard, lander slot, extra song, geo targeting,
  pre-release hold.
- **The news pages grow on culture;** the client's track is attached as the sound at posting time. Posting stays manual
  in the app so the official sound is attached. (Unverified claim still open: API-posted videos go up as "original
  sound" and do not count toward the client's sound page.)
- **Network risk from the earlier handoff:** 3 pages x 3 posts a day = 270 posts a month behind one track, and TikTok
  bans "networks of similar accounts distributing high volume commercial content", so pages must differ in niche, look
  and posting times.

### The goal of this job (the editor, 7 Oct)
- Automate music and rap news: once a day Claude scans the best sources, sources the material and builds posts fast in
  simple fixed formats that stay editable in Premiere. Research first, then build. Credit efficiency is a must ("go a
  biiit easy on the tokens").
- Act as the pages' manager, not a builder: "we need to make sure you are producing interesting stuff, and actually
  working as a manager for the pages trying to grow them from start"; "ideate, you're a good social media manager". On a
  viral moment, propose extras (an alternate opening for an A/B, a beef timeline carousel, a Story poll, a pinned
  comment) and pass on weak stories.

### Who gives notes, who does what
- **the reviewer:** reviews batches on WhatsApp (the editor forwards screenshots) and sets the bar.
- **the editor:** asks for the batch, relays notes, posts from the Drive phone app in the UK window with the client's sound
  picked in the app, adds the poll sticker and pinned comment, and should report numbers.
- **Claude:** scan, pick, verify, add a fact, source assets, write headlines and captions, build, check, deliver to Drive,
  update the schedule and the playbook.

### The pages
- **@zonegbp:** UK rap and culture: fast, plain, a bit cheeky. Dark tweet card, tracksuit pfp.
- **@beatswitchfm:** the biggest rap and music stories for UK fans, US included, plus money and music business, more of a
  news desk. Light tweet card, England-jacket pfp. Bio (branding doc): "if it's loud enough you'll hear it here first"
  (memory adds "dm for credit or removal").
- Football pages in the same list (the reviewer, 7 Oct): @stillbenched, @payedxi.
- The pfp-to-handle match and the display names "Zone GBP" and "BeatSwitch" are Claude's guesses, not confirmed. Neither
  page is verified. `brand.json` colours are placeholders (yellow #FFD60A, red #FF3B30); a distinct identity per page is
  planned later.
- Pages must be Creator or personal accounts (Business accounts lose the full music library), and never hint that a song
  is promoted.
- The old handoff's page list (warmdietcoke_, footycentralhq_, knockoutclipss_, airforceclips_, beatswitchfm) came from
  an earlier session on a shared account and does not match the live list: follow the reviewer's. Its bio rules still hold:
  blunt, emoji-bulleted noun phrases ("📷|Pictures,Videos,News"), never poetic; pfps are current memes or clean topic
  marks.

## Formats and specs

### Sizes
- Cards and carousel slides: 1080x1350 PNG. Videos: 1080x1920, 30 fps, H.264. Story stills: 9:16 with room for a poll
  sticker and a pinned-comment line.

### Formats built in vc-news
- **Cards:** `uk` (full-bleed photo, dark gradient, condensed caps headline in the bottom third, label pill or platform
  logo, optional inset circle, pfp + @handle); `raptv` (photo top 60%, 8 px accent rule, badge "OCT/26"); `meme` (white
  band with an Impact headline, face circles with a red ring for court and beef); `tweet` (our own account,
  screenshot style); `chart` (blurred cover, #rank with up / down / NEW, stats); `list` (rows; `style: prices` puts the
  label left and a big value right); `vs` (two photos plus a 9:16 Story version); `ytc` (a YouTube comment rebuilt sharp
  in YouTube's dark style); `slide` (carousel slides).
- **Videos:** `uk` (headline under the clip; wide clips in a blur box at least 760 tall, centred at y 650); `meme`
  (460 px band); `tweet` (card on top, the clip just under it: card bottom from the overlay's alpha box + 30 px);
  `split` (the @rap layout: photos 540x470 each, caption box at photo height minus 72, clip from y 560, caption
  uppercase, at most 2 lines, 1 to 2 emoji); `quote` (the exact words as the headline); `tt` (plain caption style, a
  one-off bonus).
- **Seen but parked:** calendar cards (birthdays, anniversaries, release lists: off by default per the user),
  sticker-caption freestyle clips, named series.

### The user's own @rap-style post (the model for `split`)
- (local folder) + RENDERS: 1080x1920, two artist photos on top (nested sequence), a white rounded
  caption box with ProximaNova-Extrabold black capitals plus fire and !! emoji PNGs, the music video below (scale 126,
  y 0.646), the song as the audio, 22 to 26 s. Other niche samples in (local folder)
  Basketball}\Renders` end with a Spotify-style song card.

### the reviewer's 6 SOP formats ((local folder); raw versions in `To give to claude\`)
These are "easy formats" across niches for TikTok, Reels and Shorts (owner "Clipping Team"; template assets in Google
Drive folders linked in each PDF, not on this PC). They are NOT the rap news formats (user, 7 Oct).
1. **Top 5 x Artist Songs:** a top 5 list for a famous artist whose sound clashes with the client's; the list stays
   empty and the client's song is the only filled line, as the honourable mention. Proxima Nova Semibold 80, black
   stroke 6 px, white; title at 540,375; rank lines x 255 at y 625 / 765 / 905 / 1045 / 1185; HM at 540,1330; 1080x1920,
   the source video full screen behind the text. Push the honourable-mention song louder than the rest ("the bigger the
   volume jump, the bigger the laugh"). Examples: "TOP 5 ELVIS PRESLEY SONGS, HM: NEXT UP", "TOP 5 TAYLOR SWIFT SONGS,
   HM: SIRENS".
2. **YouTube Title Swap:** a fake YouTube mobile player shows one title while a contrasting song plays (an intense track
   labelled calm and classical, or a soft track labelled as a big rap song). Black sides on purpose; music video at
   540,658 scale 57%; YouTube UI at 540,1200 scale 191%; the mobile UI, not desktop.
3. **Flow State Dictionary:** a Google dictionary card for "flow state" fixed on top while the client's rap plays; only
   for rappers with a genuinely strong flow. Screenshot layer BELOW the video; screenshot at 540,689 scale 184%; video at
   540,1175 scale 57%.
4. **Dancing Comp:** silly, often AI-generated dance videos carrying the song; an optional title (opener, lyric or song
   title) in Proxima Nova Semibold 80, stroke 6, at 540,375; match at least the first beat; peak about -3 dB; a
   reacting caption ("what is bruce banner up to bro?" + a crying-laughing style emoji).
5. **Sports Edits:** a pre-made sports edit; the client song replaces the synced reference song so the drop lands on the
   edit's drop (delete the reference track); most templates are high BPM (rap, drill), a few low BPM fit any song; fade
   the last 1 s; peak about -3 dB; export 1080x1920 or 1920x1080 per template.
6. **Military Edits:** as Sports, with jets, aviation and military footage; match the song to the footage's intense,
   cinematic energy first.

### The team's research doc (`FINAL reviewer\research\the studio - Format and Sourcing Research.docx`)
- The standard layout on almost every high performer: one image top left, one top right, the caption in the middle, the
  video across the bottom (the @rap layout).
- 8 music formats: concert clips (growth; reaction or report captions), tweet-format post over video, big events from
  the music angle, raw music video clips (filler), trending slideshow, interview clips (growth, Genius as the reference),
  comment-bait prompts ("Rarest stickers only": the one format where the client's sound is the point), motivational
  edits. (It also lists 8 football formats.)

### Type, colour and marks
- **Fonts:** Coolvetica Hv Comp (condensed) for card headlines; Proxima Nova Extrabold for video headlines, the split
  caption box and subtitles; Impact for meme headers; Helvetica for tweet cards; Bahnschrift for numbers. A 5-font A/B
  on a real video showed the condensed face is hard to read on a phone, so videos use Proxima Nova.
- **Headline markup:** `*word*` = the accent, `^word^` = a second accent (red); 1 to 3 hook words.
- **Accent per story type:** beef, court, breaking #FF3B30; charts, money #30D158; throwback, birthday #FF9F0A; RapTV
  style #FF7A00; news #FFD60A.
- **Numbers in the accent colour automatically** on cards, video headlines and every carousel slide (regex in
  `templates\card.html`). Tweet cards stay plain like real tweets. Names starting with digits are skipped (21 SAVAGE,
  50 CENT, 42 DUGG, 24KGOLDN, 1017).
- **Page mark:** the page's pfp + @handle, never a text wordmark; on videos a byline above the headline.
- **Platform logo tiles** instead of label pills when the story is about a platform (Apple Music, Spotify, Billboard,
  WWE): simple-icons SVG in brand colours on a rounded tile (radius 23%).
- **Tweet cards** only for our own accounts (light @beatswitchfm, dark @zonegbp), no blue tick unless verified; a photo
  tweet is drawn as a real tweet screenshot with the image inside the card.
- **Emoji:** iPhone-style everywhere: Apple PNGs from the emoji-datasource-apple set (160 px, then 64 px), cached.
- **Safe zone:** headline and face between about 15% and 65% of the height (the grid crops 1080x1920 to 3:4, 240 px
  off top and bottom; app buttons cover the right and bottom). Known gap: the `uk` video headline sits lower than this.

### Audio and subtitles
- Keep the clip's own audio by default. Every render: a 1 s fade-out and loudness normalisation:
  `afade=t=out:st=<dur-1>:d=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000`, AAC 192k. Modes: `clip`, `song` (the
  client's song from `song_in` at its drop), `mix` (song bed under the clip at `bed_db`, default -14 dB).
- Subtitles for speech only, never lyrics; stop them before the song (`subs_until`); star out swears (f*ck, sh*t, b*tch,
  n*gga, m*therf*cker).
- Whisper subtitles: 16 kHz mono WAV through the skill's `hear.py` (faster-whisper large-v3-turbo); a phrase breaks at a
  pause over 0.3 s, at . ! ? or at a Whisper segment start; phrases split evenly into chunks of up to 4 words;
  uppercase; Proxima Nova Extrabold 70 px, white, black outline 6, bottom centre, MarginV 560 by default
  (`subs_margin`); each line ends at the next start or 0.4 s after its last word.

### Cutting rules for news reels
- **First 3 s are the reel's "CTR":** the headline fully on screen from frame 0 (no fade, no logo intro), a face big,
  sound starting on the hook, name and conflict first. 3 to 7 s: the fact plus our added number or time. 7 to 12 s:
  proof (video peak, interview line). Last 2 s: a clock or an open question, ending near frame 0 so it loops, no outro.
  On-screen text at 15 characters a second (Netflix caps 20), at least 1.5 s; headlines 6 to 10 words, front-loaded.
- **Music videos:** cut on the hook or chorus, never the intro. Order: YouTube "Most replayed" heatmap (best window,
  skip the first 8 s); if too new, the hook line in a Whisper transcript; else the loudest RMS window (skip the first
  10 s and last 6 s).
- **Frame 0 is a face:** start where the face lands; shift the crop focus (`fx` / `fy`, 0 to 1) if it is cut off.
- **Length follows the payoff:** 14 to 16 s for headline videos, 23 s for a chorus with 4 hook lines, 30 s for a live
  clip with an arc, 36 s when the payoff needs it. Length is a test variable (8 to 12 s vs 20 to 30 s, judged on skip
  rate).
- Cut out other channels' end cards and burned-in intro titles. Never the same footage on both pages at once: give each
  page its own section of the video.
- Baked-in letterbox bars are cut automatically: ffmpeg `cropdetect=24:2:0` over 4 s from in + 0.5 s, applied only when
  the crop is under 92% and over 40% of width or height; `crop: false` turns it off, `"w:h:x:y"` forces one.

### Carousels and Stories
- Slide 1 is the card (a claim or number plus a face), one fact per slide with its own headline, 2 to 3 slides for news
  and 5 to 8 for timelines and rankings, the last slide worth sending. Plus a 9:16 Story still with room for a poll
  sticker and a pinned-comment line. Polls live in Stories (2 to 3 a day); their real results become next-day posts.

### Posting
- **UK windows (Sprout, Mar 2026):** Mon to Thu 17:00 to 21:00, Fri 17:00 to 18:00, Sat 15:00 to 16:00 and 17:00 to
  19:00, Sun 18:00 to 19:00 (Sunday best). Breaking news as soon as verified; engagement posts 18:00 to 20:00; the Friday
  chart card after 17:45. Sprout labels these GMT and BST ends 25 Oct: test an hour either way.  IST is 4h30 ahead in
  BST, 5h30 after.
- **Volume and mix:** 1 video + 1 carousel per page per day since 10 Oct; no this-or-that posts in the feed until the
  pages have an audience; hashtags 0 to 2 (Instagram caps at 5 since Dec 2025); weekly recaps at most once a week.
- **30-day launch plan (PLAYBOOK.md):** week 1 baseline (1 reel + 1 card a day, metrics at 24 h and 72 h); week 2 hook
  tests; week 3 double down only if skip rate holds; week 4 keep formats above median on sends and follows per reach and
  cut any with three reels in a row above median skip rate; use the pages' own medians after 20 posts. Skip-rate
  averages 2026: 65.5% (1K to 5K followers), 63.4% (10K to 50K), 60.5% (100K+); target under 60% by week 4.
- **Trial Reels** (since 10 Dec 2024) show a reel to non-followers first: use them to A/B two openings of the day's best
  story (only the first 3 s change); eligibility unclear (a 1,000-follower minimum is reported): check for the toggle.

### Sourcing and verification map for this niche
- **Confirm before posting, one primary source per story type:** charts on officialcharts.com (and its First Look),
  Apple Music RSS JSON, iTunes Search / Lookup, kworb, Billboard; premieres on the artist's own YouTube channel (a
  scheduled premiere shows in search with its live_status); events on the organiser's own X account; legal dates on the
  US federal inmate locator; statements on the artist's own Instagram; anything else in 2+ outlets via Google News.
  Legal, violent and "allegedly" items need press or police. Write the sources into the batch `note`.
- **UK chart calendar:** Official Charts First Look on Sunday (X 19:30 to 20:00 UTC), Update on Monday (X 16:00 to 18:30
  UTC), Trending chart on Tuesday, final chart Friday (Radio 1 from 16:00, reveal 17:45 UK). Midweek posts say "on
  course for" and go out before Friday.
- **Who breaks UK rap stories:** GBMC (@GreatBritishMC) is the fastest UK beef page (about 6 posts a day, about 1.5 h
  after the artist's upload) but mixes in gambling promos and unsourced claims: detect with it, never source from it.
  Small accounts (@UKHipHopDaily, @ldn_grassroots) beat it on early stages; GRM Daily ran 20 to 29 h ahead of Link Up on
  shared stories; UK radio brands (1Xtra, Capital XTRA, Rinse) have abandoned X.
- **Handle traps:** @ComplexUK is a 3-follower account (real: @complex_uk); Instagram @kurrco is unrelated (real:
  @kurrco.xyz); @raptvcom belongs to someone else (RapTV is X @Rap); Instagram @lyricallemonade is a placeholder;
  @UKDrillNews_ and @UK_Drill_News are dead (one likely compromised); UK Rap Daily is now self-promo.
- **Sourcing order for visuals:** the artist's official video or channel, the organiser's own clips, platform clips
  (Link Up) with credit, X post media at original size, YouTube thumbnails (`maxresdefault` then `hqdefault`), then
  frames from music videos as artist photos. Avoid other pages' watermarked edits (GBMC), auto-generated YouTube "Topic"
  thumbnails, thumbnails with a Vevo logo, dark fan rips, photos with a tiny subject. Confirm who is who and check every
  face crop before labelling.
- **Free signals that worked (7 Oct):** Shazam CSVs (UK top 200, hip-hop / rap, discovery: the earliest signal), Apple
  Music most-played JSON (host rss.marketingtools.apple.com), kworb (Spotify daily per country, about 2 days behind),
  Official Charts pages, Wikimedia pageviews (spike = 3x the 28-day median and 1,000+ views), Google Trends Trending Now
  RSS (`trends.google.com/trending/rss?geo=GB`), iTunes Lookup, MusicBrainz, YouTube channel RSS. Dead or locked: the
  YouTube Trending page (gone 21 Jul 2025), old Google Trends RSS, pytrends, Tokboard, Billboard to scripts (HTTP 402),
  Spotify country charts (login), Spotify API new releases and top tracks (removed Feb 2026), editorial playlists
  (unreadable since 27 Nov 2024), Reddit RSS (ends 13 Nov 2026). Score movement (new entries, rank jumps, stream gains),
  not position. An empty result is an error, not "nothing trending" (from a blocked region Deezer returns empty data and TikTok
  refuses the connection: run scans from a UK machine when possible).
- **Network proof (for pitches):** RapTV (@rap) is one of nine niche brands run by one company (Low Battery), the model
  Vision sells; X size does not carry to TikTok (Daily Loud about 6.9M on X, about 10.6K on TikTok); no UK page does
  @rap-style headline news across platforms except GRM Daily.

## House look and taste rules (with the verdicts)

### The bar (the reviewer, 8 Oct, round 2)
- Content must be genuinely interesting, judged by retention, CTR and AVD, "not because the system is cool or
  impressive". New pages are "time and topic based, need to hit right": timely, polarising or very current. This-or-that
  "only works when you're bigger". Numbers always a different colour (#68 "in red"), carousels included. Top Boy was too
  old. the editor: "keep this in mind" (rules changed, posts not remade).
- **The interest test** (vc-news PLAYBOOK.md) before building any post: fresh, tension, UK relevance, a strong first
  frame, an added fact; 0 to 2 each; build only at 7/10 or more. Cut posts that fail rather than fill a quota.
- **Never fabricate numbers or poll results.** the reviewer suggested "25% think Dave is better"; Claude declined and offered
  real numbers side by side, the Story poll's real result posted next day ("[X]% of [N] voters on our Story picked..."),
  real quotes, our own call record. One exposed fake stat ends a news page.
- **Every post adds one fact the source does not show** (a chart spot, a time, a count, a date, background): Instagram's
  originality rule (30 Apr 2026) drops accounts that mostly repost; a logo, border, subtitles, credit, speed change or
  screenshot never counts. Examples: "1,700 comments in under 2 hours" on the Digga post; "23 years since 'Boy in da
  Corner' won the Mercury" on Dizzee.

### Captions and headlines
- Urgency words (JUST DROPPED, OUT NOW, DROPS TONIGHT AT 7PM, siren emoji) only on time-sensitive stories: "dont do
  everything urgent captions like reviewer said, see where they would fit". The rest lead with the fact and end on a
  question.
- Personality, but light: fact first, a short reaction or question last ("Troll of the year?", "W troll or fumble?").
  "have personality dont overdo it tho". The user: "we really like the captioning style of the last one video" (the
  Digga troll video, 9 Oct). Hype and heavy slang read as AI or spam.
- Ask, never order: Instagram does not recommend posts that ask for comments, shares, tags or a set word or emoji. "Comment
  W or L", "tag a mate", "like if", "rate it 1-10" are out ("Rate it out of 10" was removed from the Headie post); "Is
  that a W or an L?" is fine.
- Polarising without bait: two named sides, one real fact, a clock, an open question ("Who's winning now?").
- Run the angle the audience already runs with (on the Digga troll song the top comments said "we got trolled"), and
  let two posts on two pages tell one story (the live clip on @zonegbp, the pinned-comment card on @beatswitchfm).
- Headline grammar per story type, borrowed from the leaders: Kurrco "ARTIST & ARTIST - Title", "TITLE OUT NOW", "N years
  ago today ... Favourite track?"; RapTV lines ending "‼️"; GBMC one CAPS keyword, one emoji, asterisk censoring;
  Mixtape Madness "🗓️: X dropped N years ago"; Daily Loud always ends on a question; Pop Crave neutral and sourced for
  stats. Full house style in `vc-news\captions.md`.

### Approved
- Tweet videos: "fire" (the reviewer, 8 Oct). The split format: "format perfect" (but "need better caption, more urgency").
  The Digga troll caption style. Coloured numbers. Platform logo badges (Apple Music instead of the CHARTS pill on the #68
  post). Honest numbers carousels ("Digga D vs Morrisson: the numbers so far", 11 Oct).
- @handles instead of wordmarks: "write @gbp and stuff instead to show it is a username. over time we wanna build better
  and better branding".
- iPhone emoji: "emojis yeah those type of emojis".

### Rejected or weak
- A condensed headline font on video ("adjust font and a few bits", the reviewer on the throwback).
- A CHARTS pill where a platform logo fits; urgency on everything.
- Opinion VS posts with no live story behind them ("empty"; four were made: would not make again).
- Stale stories (Top Boy); throwbacks and plain release posts (scan data: throwbacks 0 of 6 broke out); a low-pull
  freestyle; Hackney courts; nice stories with no tension; recaps more than weekly.
- One artist too often: "we've done too much digga stuff". "keep in mind we gotta do UK stuff".
- Skip list: deaths and tragedies, violent and prison-violence clips, thirst-trap clips, relationship gossip, edited or
  misleading images (an edited-looking Soulja picture was skipped), race angles that can backfire, someone else's skit or
  meme edit, promos dressed as stories, unconfirmed collabs (Fakemink x Skepta was dropped: only Kurrco had it), single
  -source "EXCLUSIVE" or "allegedly" claims, misquotes (a Rihanna "100+ unreleased songs" line), old clips posted as news
  (a Young Adz throwback), too much of one story. From the old handoff: no third-party watermarks, no screenshots with
  username credit, no cross-promotion or shared look between pages, vary posting times, never post leaks, unreleased
  snippets, agency paparazzi photos or unverified gossip.
- Sources stay lean: 12 main X pages plus a news sweep, no calendars or 81-feed stacks by default ("all of this stuff can
  easily be found from main pages ... payout is so low if we have so many sources").
- Cross-check from the Outcome job (14 Oct, same team): this house look (bold caps headline, coloured numbers, a tweet
  card over a clip, carousels) is the look the editor names as the reference; the TikTok white rounded box with black
  lowercase text was "TOOO off beat".

## Every deliverable and version, with status

Batches live in `vc-news\batches\`, finals in `vc-news\FINALS\<batch>\@<page>\NN_slug.mp4|png` + `captions.txt`.
Undelivered drafts are fixed in place; any change to a delivered post becomes `_v2` ("do not replace this one make
version 2. keep that in mind always", 9 Oct).

| Batch file (built) | Posts | Status |
|---|---|---|
| test_formats.json (7 Oct) | 13 format tests (cards and videos) | tests only |
| 2026-10-07.json (7 to 8 Oct) | 8: Headie split, Morrisson #68, Legxacy tweet, Drake list; Lil Baby tweet, NBA YoungBoy, Don, OB Fil | the reviewer round 1; fixes applied as v2; not posted (expired) |
| 2026-10-08.json (8 Oct) | 8: Digga tonight split, Trapstar VS, Russ tweet, Digga vs Morrisson VS; Offset / Don, T-Pain tweet, Wayne / Drake tweet, Young Thug R&B | round 2; only the Digga posts went up |
| 2026-10-08b.json (8 Oct) | 8: Letitia tweet, Hackney, Wiley meme, Top Boy VS; Kay Flock, Italian, Shabang, Drake VS | round 2; not posted (expired). This file and its captions.txt hold a rapper's legal name, prison and release date from a public record: strip before sharing |
| 2026-10-09.json (built 8 Oct night) | 8: UK rap chart list, Tinyboost, Cench / Dave VS, UK recap; Ye, Boosie price list, Carti / Ye VS, rap recap | round 2; not posted (expired) |
| 2026-10-08_digga.json (9 Oct) | 7: Digga troll (+ an alternate opening for a Trial Reels A/B), beef timeline, Digga troll split, Digga live, Digga live tt, pinned "peace" YouTube comment card | the Digga posts went up; caption style praised |
| 2026-10-10.json | 4: Swarmz ambush, UK drops; Gunna, GTA radio | first day of the 1 video + 1 carousel routine; posting not recorded |
| 2026-10-11.json | 4: Morrisson top 40, beef numbers carousel; Summer Walker, Soulja 2028 | first batch copied to Drive; posting not recorded |
| 2026-10-12.json | 5: Digga "on course for #39", Flo Wembley, Swarmz draw; Dizzee, UK First Look | posting not recorded |
| 2026-10-13.json | 4: Giggs Wembley, Russ Millions vs A2 Anti (+ Story poll); Drake 91, Krept ST100 | posting not recorded; the poll result post waits on the vote count |
| 2026-10-14.json | 4: Lollypopbeatz freestyle, UK albums carousel + Story poll; Keffe D sentenced, Rocky / Ferg carousel | built 14 Oct evening and copied to Drive; posting not recorded |

- Audit of what worked by 10 Oct (strong): Morrisson at #68, Digga's reply tonight, the Kay Flock release-date story, the Ye and
  JAY-Z leak, T-Pain on catalogue money, Young Thug going R&B, "only 4 rap songs in the UK top 100", Boosie's price list,
  Lil Baby on BAND4BAND. Would not make again: four empty VS posts, the Quavo throwback, a low-pull freestyle, Hackney
  courts.
- **Other deliverables:** every video also ships its Premiere layers (see the pipeline section); the Claude Doc "Vision
  News Pages: how our workflow runs" (12 Oct, in the editor's claude.ai account: share or export it for the reviewer); the
  review of the reviewer's "Vision Auto Editor" concept doc (night of 11 to 12 Oct).

## Review history, round by round

- **7 Oct, setup:** research first, then build; ffmpeg, yt-dlp, gallery-dl and Deno installed with the user's OK; UK
  pages plus a few US leaders, "only the best ones"; simple videos; Claude writes headlines and captions in the niche's
  style ("do not overdo it"); tweet templates for the two news accounts; lean sources; iPhone emoji; the first batch of
  6 to 8 posts held until "commence operations" ("not yet wait for my next message"). The user on the inherited handoff:
  "dont take everything solid as the sources are a bit ass".
- **Round 1 (the reviewer, 8 Oct, batch 1):** tweet videos "fire"; Headie split "format perfect" but "need better caption, more
  urgency"; Morrisson #68 in red with a platform logo instead of the CHARTS pill; the throwback "adjust font and a few
  bits". Done: all applied (v2), a readable video font and a bigger clip box. The user added: @handles not wordmarks; a
  clean FINALS folder ("have a separate finals one with not a bunch of other random stuff"); urgency only where it
  fits. Then "how can i access directly in premiere" (to move the Morrisson section): every video now ships a
  full-source Premiere XML; the re-cut was done by timestamp ("4:50 to 6:05" on a 6:02 video: "nonono not 6:05, 5:05").
- **Round 2 (the reviewer, 8 Oct, batches 2 to 4):** the content bar above. the editor: keep it in mind rather than remake. Done:
  rules changed (numbers coloured everywhere, carousels emphasised, the interest test, the manager role, no empty VS, no
  fabricated stats, VS polls to Stories); engagement research folded into captions.md; a schedule file marks POST /
  optional / skip (8 of 24 built posts marked POST).
- **9 Oct, Digga D:** his promised diss was a troll song. the reviewer on the video cut on its intro: "the main part of the song
  should go here": re-cut on the first chorus (0:14.8 to 0:30.8); then the user asked for 1:01 to 1:24 ("better
  visuals"), v2, 23 s, the hook line 4 times. The caption style was praised. Rule: never replace a delivered post.
- **10 Oct:** "we want one video and one carousel for each page everyday". Only the Digga posts from batches 2 to 4 had
  gone up; older batches count as expired.
- **11 Oct:** Google Drive delivery in the user's own layout ("add folder with todays date, see how i sorted for
  yesterday").
- **Night of 11 to 12 Oct, the reviewer's "Vision Auto Editor" doc (pasted as text and screenshots; the link was behind another
  workspace's sign-in):** verdict "approve the direction, but not as written", with five fixes: (1) @zonegbp is the UK
  rap news page, not a sport page; (2) a "no third-party pixels or audio in a render" rule would rule out every news post,
  so news pages need their own rule; (3) add a news track (find, verify, add a fact, caption, window), with the operator
  approving a daily slate in one go; (4) for news the code renderer is the main engine, not a fallback; (5) the trending
  loop already runs, keep it running while the Adobe engine is proved. Worth adopting from his doc: a data model
  (project, page, format, job, output, revision, jobs pinned to a format version), timecoded review comments turned into a
  change list you preview then run, automated QA gates (loudness, black frames, safe zones, captions in sync, faces not
  cropped), forking a format per client by swapping the brand kit, editor minutes per video measured from job one,
  rights and contract clauses (Adobe's "no service bureau" clause), configuration sessions in Claude Code run by trained
  editors. Too complex for now: a 15-model intelligence layer, a 4-model reframe stack (try Auto Reframe first), a
  project file for every daily post. Breakout rule: his doc used "3x the page's average"; we advised the median.
  After Effects (Nexrender) is for animated templates such as a tier-list board, budgeting 32 GB or more of RAM per
  render machine (a position, untested).
- **12 Oct:** the workflow written up as a Claude Doc; "keep in mind we gotta do UK stuff"; less Digga.
- **13 Oct:** a Google News sweep added to every scan (Giggs' Wembley show was only on news sites).
- **14 Oct:** daily batch (4 posts). Its note lists the checks (Official Charts "biggest albums of 2026 so far", BBC, PBS,
  Reuters, CNN, WaPo, Billboard, People) and the skips (Blacklisted Honours: no winners list online yet; tabloid dating
  rumours; a Method Man clip that only says "Absolutely"; prison violence; a murder story tied to Digga; a tattoo story;
  the Pope: not our lane).

## What went wrong and the fix

| What broke | Cause | Fix | Rule now |
|---|---|---|---|
| Five research agents died (HTTP 429), one UK sub-report lost | monthly spend limit; a 200-search budget shared by all agents | a resume file with the briefs; finished reports pulled from the agents' saved transcripts by script | write `research\00-status.md` first; cap web calls per agent (12 to 15); agents write their own files |
| Instagram `web_profile_info` returned 429 | about 20 quick lookups | stopped at once | read Instagram slowly, from a monitoring account only |
| Browser-pane screenshots cropped to about 799 px | small pane | `resize_window`, a JS thumbnail overlay, `zoom`, then reset | enlarge first, capture once |
| `yt-dlp` not found after pip | no exe on PATH | `python -m yt_dlp` | call it as a module |
| Wikidata SPARQL 429 | 1 request a minute | 14-day cache, 65 s spacing; the calendar was later dropped | keep slow sources off the daily path |
| The contact sheet included the previous sheet | a glob caught `_sheet.png` | skip `_` files, `--only` filter | prefix helper outputs with `_` |
| UK stories buried, Morrisson missed | US volume; GBMC spelled him "Morrison" in 14 of 15 posts | aliases, UK weights, a UK top section | rank UK separately; alias every spelling seen |
| YouTube "not a bot" block for 15 min | about 15 parallel yt-dlp calls | a throttled call with a cross-process lock (`out\.yt_lock`, stale after 20 min), a 6 s gap, `--sleep-requests 0.75` | one YouTube call at a time, across sessions |
| Black bars inside a music video | bars baked into the file | `cropdetect` auto-crop | detect bars before framing |
| Wide photos cropped badly behind tweet cards | photo behind a portrait card | screenshot-style tweet with the photo inside | choose the layout by photo shape |
| Title card clipped at the edges | text wider than portrait | full width on a blurred backdrop, keeping the 4:3 frame | never crop title cards |
| Vevo or Official Charts logos, faces cut, the wrong person | thumbnail picks, crop focus | refocus, swap the photo, shift `fx` | check every frame 0 on the sheet |
| iTunes matched the wrong release; albums missing | iTunes Search gaps | other sources; story swapped when no clean art | check cover art against the release |
| A subtitle line ran two phrases together ("TOO MUCH MAN PEACE") | grouping on pauses only | also break at segment starts and punctuation | subs follow speech phrases |
| `\b` became a backspace in card.html; two edits silently lost | heredoc escaping; a failed match inside a chained command | a separate patch script; redone with Edit | Write/Edit for code, one edit per call, confirm each |
| cp1252 print errors | Windows console encoding | `PYTHONIOENCODING=utf-8` and `encoding='utf-8'` in subprocess | set UTF-8 for every run that prints emoji |
| A re-cut replaced a delivered post (8 Oct) | before the versioning rule | backup kept in `_temp\superseded`; the builder now versions | delivered means `_v2`, never overwrite |
| `version_of` made `_v2` of undelivered drafts | it versions anything that exists | Claude deleted its own undelivered drafts before rebuilding | move drafts to `_superseded` instead, never delete |
| A re-cut asked for "4:50 to 6:05" on a 6:02 video | a typo in the request | asked; it was 5:05 | check requested in/out times against the source length |
| the reviewer's doc link unreadable | another workspace behind a sign-in | the user pasted text and screenshots | never sign in; ask for an export, paste or share |
| Monitoring logins logged out (13 Oct) | session expiry | the user logged in again | check login state before browser reads |

## Open items and next steps

1. Import one `<id>.xml` and one `<id>_source.xml` in Premiere (nobody has yet; the kit copy's file URLs were fixed for
   Mac paths on 14 Oct, so on a Mac this import is also the test of that fix).
2. Start measuring: Insights at 24 h and 72 h per post (skip rate, average watch time, sends, follows, profile visits)
   and Story poll counts; the pages' own medians after 20 posts; a Sunday review that updates PLAYBOOK.md. Editor minutes
   per video and Claude usage per batch were never measured.
3. Decide on two scans a UK day (morning and late afternoon, because beef and court stories break in the evening) and a
   scheduled run (today every batch is started by hand).
4. Check the Trial Reels toggle; if present, A/B two openings of the day's best story.
5. Template follow-ups: move the `uk` video headline into the 15 to 65% safe zone (test); confirm pfps, display names and
   logos; a distinct identity per page.
6. Port vc-news to the Mac (last section) with his own monitoring logins.
7. Pending posts: the Russ Millions vs A2 Anti poll result (only if the poll ran); a follow-up if Morrisson's or Digga's
   real diss drops.
8. Dated dependencies: fxtwitter is unofficial; Reddit RSS ends 13 Nov 2026; BST ends 25 Oct (windows shift); the
   research is dated 7 to 8 Oct and goes stale.
9. the reviewer's own next steps from his doc: the first format to prove (his proposal: a song tier list), an editor-minutes
   baseline, an engine Mac and a named Adobe seat, an AE tier-list template, a Nexrender spike, a Discord job command.
10. Share or export the Claude Doc "Vision News Pages: how our workflow runs" for the reviewer.

### Decisions for the reviewer (rights and risk)
- **Footage rights:** news posts reuse music videos, interviews and other pages' footage without a licence (the team
  accepted it). His own doc proposes the opposite rule, so the news pages need an explicit rights position. The old
  handoff told Claude not to raise copyright or licensing concerns: decide whether the kit keeps that.
- **Removing another page's burned-in caption** with ffmpeg `delogo` before reposting their clip (used on the Digga live
  clip, `delogo=x=20:y=258:w=536:h=160`, and on the 14 Oct Lollypopbeatz clip from GBMC): it keeps the native UI but
  is a reuse of someone else's post. Decide.
- **Reading X** through the unofficial fxtwitter API or a logged-in browser breaks X's terms and can cost the reading
  account; YouTube cookies from a real account can get it flagged (throwaway only); a VPN for TikTok from a blocked region is a
  legal grey area.
- **API posting** and whether it can carry the client's sound (unverified).
- The old handoff says Claude Code can read pages "through" another person's claude.ai login: never do that. It also
  mentions a publishing skill; posting stays manual.

## Where the files live on the editor's PC

- **The pipeline:** (local folder) (read README.md first, then PLAYBOOK.md, captions.md):
  `vcn.py` (builder: cards, videos, Premiere layers + XML + source XML, versioning, sheet, Drive copy; 33.3 KB),
  `templates\card.html` (every layout, rich-text markup, number colouring, the fit loop; 23.3 KB), `scan.py` (the daily
  digest via fxtwitter; ranking; breakout, talk, share; story-type stats; `--full` adds feeds, Shazam, Apple, Google
  Trends, Wikidata; 20.4 KB), `fetch.py` (YouTube sections, search, heatmap peak, loudest window, thumbnails, frames, X
  media, files; throttled yt-dlp; 8.8 KB), `brand.json` (accounts, handles, pfp paths, tweet style, accents, fonts),
  `batches\` (the daily JSONs; `2026-10-13.json` and `2026-10-08_digga.json` are the best worked examples),
  `FINALS\` (+ `SCHEDULE.md`), `out\` (renders, Premiere layers in `out\<batch>\premiere`, scratch in `_temp`, scans in
  `out\scan`), `in\` (downloads), `assets\` (pfps, cached emoji and logos). Do not share `_chrome_profile\` (a headless
  Chrome profile with a cookies database) or any `secrets\` folder.
- **Research:** (local folder): `00-status.md` (resume notes, read first), 01 US pages, 03 feeds JSON
  (121 feeds, 81 live), 04 trend signals md + json (61 tested, 40 live), 05 access and tooling (dated prices), 06
  shortlist (start here), 07 formats, 08 engagement, 09 growth from zero, 10 retention and hooks, `raw\` (5 UK
  sub-reports).
- **The old handoff (history, partly wrong):** (local folder) (CLAUDE.md, docs
  00 overview, 01 platform rules, 02 pages, 03 sourcing, 04 editing incl. an effects glossary and the UK drill look, 05
  automation roadmap, `data\monitoring-sources.json` with 152 sources) and a zip copy beside it. Research files 04 to 06
  corrected several of its claims. Older pages linked from it (in the user's account): Wire Desk
  (private page) , Drill Edit Handbook
  (private page) , Hoops and Hurt (private page)
  (not read).
- **the reviewer's material:** (local folder): `FINAL reviewer\` (6 SOP PDFs + the research docx),
  `To give to claude\` (raw SOPs; "Music format.pdf" not read), `the studio - Music Packages (Client).pdf`, `PFPS\`.
  Branding doc: (local folder). Pitch video:
  `presentation\Renders\v2 presentation.mp4`.
- **The user's own posts:** (local folder) + RENDERS; niche samples in
  (local folder).
- **Drive (the editor's PC):** `G:\My Drive\RAP POSTS VISION\<DD MM YYYY>\zonegbp|beatswitch\` (video, carousel slides loose
  as `1.png, 2.png...`, subfolders only for 2+ carousels on one page, `captions.txt`); older `BEATSWITCH` and `ZONEGBP`
  folders from 8 Oct.
- **Fork for another client:** (local folder) is a copy of vc-news for Outcome. Never edit
  vc-news for Outcome.
- **Memory notes (Claude):** vision-clipping-project, feedback-vc-content-bar.
- **Do not ship or share:** `vc-news\in\` (1.1 GB downloads), `out\` (521 MB), FINALS media (331 MB),
  (local folder) (another page's clip).

## Which kit skills and pipeline to use for this client

- **Pipeline:** `library/pipelines/newsdesk/` (the vc-news pipeline). If it is missing or older than
  the editor's `vc-news\`, ask him for the current copy.
- **production-automation:** the daily news run, the batch JSON, breakout metrics, the schedule, Drive delivery, how to
  extend and debug the builder.
- **social-video-formats:** the content bar, Instagram's rules (originality, asking vs ordering, Trial Reels), carousels,
  posting windows, music-page posts.
- **research-and-sourcing:** finding and verifying news, the X / YouTube / chart readers, footage sourcing order.
- **editing-playbook:** hooks and cutting rules for news reels, the verdict library.
- **motion-design:** the house look (cards, number colouring, logo tiles).
- **premiere-ae-editing:** XML import, `fcpxml.py --check`, the YouTube download route (`ytdl.py`; it works around
  YouTube's bot check and may break YouTube's terms: use only with rights to the footage, the reviewer decides), `hear.py`.

### The daily run (Claude does steps 1 to 12 when asked)
1. **Trigger:** the user asks for the day's batch.
2. **Scan (about 5 s):** `python scan.py` reads 12 X pages through fxtwitter (UK: GBMC, GRM Daily, UKHipHopDaily, Link Up
   TV, Official Charts; US: RapTV, Kurrco, Daily Loud, Say Cheese, HNHH, Chart Data, Pop Crave) into
   `out\scan\scan_<time>.md` (UK top, All top, Breaking out, Most talked about, viral, What's working) and `.json`.
   Breakout metrics: `over` = views / the page's MEDIAN views (2.5x or more = breaking out); `talk` = (replies + quotes)
   per 1,000 views (posts over 5K views); `share` = (reposts + bookmarks) per 1,000. Artist ranking weighs UK sources 1.5
   and UK artists x1.3, plus chart and trend presence and `log10(views)/2`, with aliases for spellings and short names
   matched case-sensitive.
3. **News sweep** on Google News RSS (`UK rap when:2d`, `UK rapper when:2d`, a few big UK names): exact publish times,
   gets round BBC and Daily Mail blocks.
4. **Shortlist:** drop stories already covered, topic fatigue and the skip list; score the rest with the interest test.
5. **Pick the set:** 1 video + 1 carousel per page, UK first, never one asset on both pages.
6. **Verify** each story at a primary source; write the sources into the batch `note`.
7. **Choose the added fact** per post.
8. **Source assets** with `fetch.py search | peak | yt | loud | thumb | frame | x | url`, one YouTube call at a time: the
   hook section first, a face in frame 0, people identified, no watermarked edits. YouTube sections come as exact 1080p
   H.264 (`--download-sections "*S-E" --force-keyframes-at-cuts`); X media through fxtwitter, photos at `?name=orig`.
9. **Write `batches\<date>.json`** (run `ls` first): per post `id, fmt, account, headline, sub, label|logo, theme|accent,
   caption, when, photo|photos|clip{path,in,dur,fx,fy,fill,crop,pre}, audio{mode,song,song_in,bed_db}, subs, subs_until,
   subs_margin, slides[], story, poll, pin, history[]`; finals numbered per page in posting order.
10. **Build (about 1 min):** `python vcn.py build batches/<date>.json [--only ids]`. Cards and overlays are HTML/CSS
    templates filled with the post JSON and screenshotted by headless Chrome (fonts injected, the fit loop shrinks text
    2 px at a time); videos are ffmpeg composites. It writes the finals + `captions.txt`, and for every video the
    Premiere layers (V1 base clip MP4, V2 overlay PNG, A1 WAV, an FCP7 XML) plus `<id>_source.xml` with the WHOLE source
    on V1 (in/out on our window) so an editor can slip to any part.
11. **Look:** `python vcn.py sheet <date>` makes one contact sheet (every card + 2 frames per video at 1 s and 60%,
    216x384 cells, 6 columns); fix undelivered drafts in place (`--only id`).
12. **Deliver:** `python vcn.py drive <date>` (identical files skipped, changed files saved as `_v2`, captions.txt
    refreshed); update `FINALS\SCHEDULE.md` (POST / optional / skip with the window; stale posts marked do-not-post,
    e.g. a "drops tonight at 7pm" video after the event); send the sheet and videos with a hand-over table per page
    (window, format, source), what was left out and why, which facts were checked where, what to watch next.
13. **Review (human):** notes by WhatsApp screenshot, read post by post with the reading stated back; delivered posts
    change as `_v2`; the Premiere route is importing `<id>_source.xml` and slipping V1, or giving Claude a timestamp
    (a re-render takes about 20 s and keeps the house loudness and fade).
14. **Post (human)** from the Drive phone app in the UK window with the official sound picked in the app; add the poll
    sticker and pinned comment from `captions.txt`.
15. **Measure (human, not started):** Insights and poll counts back to Claude.
- Timing seen: a daily 4-post batch took about 8 to 10 min of Claude time (about 35 min on a heavy-verification day).

### Mac notes (before the reviewer runs it)
- `vcn.py` (the editor's original on the editor's PC): `CHROME` is a Windows path, `FONT_DIRS` are Windows folders, `SKILL` points at
  his skill folder, `DRIVE` = `G:\My Drive\RAP POSTS VISION`, and `file_url()` and the XML writers double the slash on
  Mac paths. **The kit copy (`library/pipelines/newsdesk/`) is already fixed** (14 Oct): Mac Chrome is
  found by itself (or set `CHROME_PATH`), the Mac font folders are searched (plus `VC_FONT_DIRS`), the skill path reads
  `PAE_SCRIPTS`, the Drive folder reads `VC_DRIVE_DIR` (Mac:
  `~/Library/CloudStorage/GoogleDrive-<account>/My Drive/RAP POSTS VISION`), and file URLs work for `/Users/...` paths
  (test one XML import). The sheet label font `arialbd.ttf` still falls back to Pillow's default.
- Fonts: Coolvetica Hv Comp (free from Typodermic), Proxima Nova Extrabold / Semibold / Regular (licensed: Adobe Fonts
  activation gives no file path, so he needs his own font files), Helvetica (macOS ships a .ttc that Chrome may not load
  through @font-face: install .ttf files or swap the tweet font), Impact (ships with macOS), Bahnschrift (Windows only:
  substitute).
- `fetch.py`: WinGet fallbacks are Windows-only; `brew install ffmpeg deno`, `pip install yt-dlp gallery-dl`; reuse the
  skill's PO-token setup for fewer YouTube blocks (fetch.py starts neither the token server nor the mweb client).
- `scan.py` runs as is; from a UK machine TikTok and Deezer work, so the region workarounds fall away.
- Subtitles: the skill's `hear.py` (faster-whisper, CPU) runs on Apple Silicon but slower; mlx-whisper is the Mac-native
  option.
- Versions that worked on Windows: ffmpeg 9.0.2, Deno 2.9.7, gallery-dl 1.32.15, yt-dlp 2026.08.19.
- **Needs his own:** throwaway X and Instagram monitoring accounts logged into his browser (never the pages, never a
  personal account; Claude never types passwords), Google Drive for desktop signed in to the account that owns the
  posting folder, optionally a throwaway YouTube cookies file (`vc-news\secrets\youtube_cookies.txt`), and an X data API
  key, Apify token or Meta Graph token in a local `.env` only if he moves off fxtwitter or adds Instagram and TikTok
  scanning.
