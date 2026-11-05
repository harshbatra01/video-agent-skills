# Music and rap news pages

The agency model: a client's track rides as the audio under niche posts on pages we run (network pages) or pages built
for the artist (owned pages). News and culture pages grow on culture; the client's song is attached as the sound at
posting time. The daily build pipeline (scan, batch file, templates, contact sheet, Drive delivery) lives in
`production-automation`; facts and sources in `research-and-sourcing`.

## 1. How the business works, and what that demands of posts
- The product is concentrated volume on ONE sound page in a short window; scattered posts on many sounds are worth
  little. Clients send the MP3 before release plus their TikTok, Instagram and YouTube sound links; a bank of posts is
  built and distribution starts on release day. A manager checks every post before it goes live.
- Post manually in the app with the client's official sound picked there. Why: the post only counts toward the client's
  sound page when that sound is attached in-app. (UNVERIFIED: API-posted videos go up as "original sound" and do not
  count.)
- Pages are Creator or personal accounts, never Business. Why: Business accounts lose the full music library (on TikTok
  they see only the Commercial Music Library). Never hint that a song is promoted.
- One clear niche per page. Example split: a UK rap and culture page (fast, plain, a bit cheeky) and a wider music page
  (the biggest rap and music stories for UK fans, US included, plus money and music business, more "news desk"). Why:
  Instagram matches reels to interest groups, so a clear niche helps; a drifting niche blurs it.
- Never the same asset on two pages, and not the same footage at the same time: give each page its own section of a
  shared video (one page took the chorus, the other the dance stretch; a 4 s overlap was flagged "don't post both at
  exactly the same time"). Why: duplicates read as reposts under the originality rules.
- Pages in one network differ in niche, look and posting times, with no cross-promotion and no shared look. Why: TikTok
  bans networks of similar accounts posting high-volume commercial content.
- Page identity: the page's profile picture + @handle as the mark; bios are blunt, emoji-bulleted noun phrases, never
  poetic; profile pictures are current memes or clean topic marks.
- Proof the model works: RapTV (@rap) is one of nine niche brands run by one company (Low Battery). Platform skew: X size
  does not carry to TikTok (about 6.9M on X vs about 10.6K on TikTok for one page). The open UK lane (Oct 2026): no UK
  page does @rap-style headline news across platforms except GRM Daily.

## 2. The daily slate
- Standing routine since 10 Oct 2026: 1 video + 1 carousel per page per day, picked fresh from that day's scan, UK
  stories first. A new page starts at 2 strong posts a day. Peers post 3 to 5 feed posts a day, but no source shows that
  volume wins, and weak posts teach the algorithm the page is boring.
- Plus 2 to 3 Stories a day with a poll; weekly recaps at most once a week. Suggested weekly rhythm (research, not yet
  run): a ranking carousel on Sunday evening, a this-or-that in Stories midweek, a chart call on Tuesday or Wednesday with
  the result on Friday.
- Breaking news goes out as soon as it is verified. Expire anything stale: a post that says "tonight" after the event is
  wrong, and old batches that never went up count as expired.
- Every post passes the interest test (`content-bar.md` section 2) and carries one added fact.
- Hand-over per batch: a table per page (window, format, source), what was left out on purpose and why, which facts were
  checked where, what to watch next. Why: the editor decides fast when the skips and checks are visible.
- Propose extras on a viral moment: an alternate opening for an A/B test, a timeline carousel, a Story poll, a pinned
  comment.

## 3. Formats
### 3.1 The standard layout of the high performers (the @rap layout)
- One image top left, one top right, a caption box in the middle, the video across the bottom.
- Our split version: two photos 540x470 each; a white rounded caption box in ProximaNova-Extrabold black capitals with 1
  to 2 emoji (fire, "!!") sitting 72 px into the photos; the music video from y 560; the caption uppercase, at most 2
  lines; 22 to 26 s with the song as the audio. Reviewer: "format perfect", with "more urgency" wanted in the caption.

### 3.2 The rap-news formats we run (cards 1080x1350 PNG; videos 1080x1920, 30 fps)
| Format | What it is | Notes |
|---|---|---|
| Headline card | full-bleed photo, dark gradient, caps headline in the bottom third, a label or a platform logo tile, optional inset circle, the page mark | numbers in the accent colour |
| Leader-style card | photo on the top 60%, an 8 px accent rule, a date badge ("OCT/26") | |
| Meme card | a white band with an Impact headline, face circles (red ring for court and beef) | |
| Tweet card | our own account's tweet, drawn like a screenshot; a photo tweet with the image inside the card | only our accounts; light for one page, dark for the other |
| Chart card | blurred cover art, #rank with up, down or NEW, stats | confirm the release art matches |
| List card | rows; a "prices" style with the label left and a big value right | |
| Versus card | two photos, plus a 9:16 Story version | versus belongs in Stories until the page is bigger |
| Comment card | a YouTube comment rebuilt sharp in YouTube's dark style | |
| Headline video | the headline under the clip; a wide clip sits in a blurred box at least 760 px tall centred at y 650 | known gap: this headline sits lower than the 15% to 65% safe zone (template change to test) |
| Meme video | a 460 px headline band over the clip | |
| Tweet video | the tweet card on top, the clip starting just under it | reviewer: "fire" |
| Split video | the @rap layout above | reviewer: "format perfect" |
| Quote video | the exact words as the headline | |
| Plain-caption video | the platform's plain caption style | one-off bonus only |
- Parked: calendar cards (birthdays, anniversaries, release lists: off by default), sticker-caption freestyle clips,
  named series.

### 3.3 The six SOP formats (the reviewer's easy formats for any niche, on TikTok, Reels and Shorts)
These are fixed layouts at 1080x1920 with the client's song as the audio. They are not the rap-news formats. Template
assets live in the Drive folders linked from each SOP.
1. **Top 5 x Artist Songs**: a top 5 list for a famous artist whose sound clashes with the client's; the five lines stay
   empty and the client's song is the only filled line, as the honourable mention. Type: Proxima Nova Semibold 80, white,
   6 px black stroke. Title at (540, 375); rank lines at x 255, y 625 / 765 / 905 / 1045 / 1185; the honourable mention
   at (540, 1330); the source video full screen behind. Push the honourable-mention song louder than the rest: "the
   bigger the volume jump, the bigger the laugh". Examples: "TOP 5 [CLASSIC STAR] SONGS, HM: [client track]".
2. **YouTube Title Swap**: a mobile YouTube player shows one title while a contrasting song plays (an intense track
   labelled calm and classical, or a soft track labelled as a big rap song). Black sides on purpose; the music video at
   (540, 658) scale 57%; the YouTube mobile UI at (540, 1200) scale 191%. Use the mobile UI, never desktop.
3. **Flow State Dictionary**: a dictionary card for "flow state" fixed on top while the client's rap plays; only for
   rappers with a genuinely strong flow. The screenshot layer sits BELOW the video; screenshot at (540, 689) scale 184%;
   video at (540, 1175) scale 57%.
4. **Dancing Comp**: silly, often AI-generated dance videos carrying the song; optional title (an opener, a lyric or the
   song title) in Proxima Nova Semibold 80, stroke 6, at (540, 375); match at least the first beat; peak about -3 dB; a
   reacting caption with an emoji ("what is [character] up to bro?" 😂).
5. **Sports Edits**: a pre-made sports edit; the client song replaces the synced reference song so its drop lands on the
   edit's drop; delete the reference track; most templates are high BPM (rap, drill), a few low BPM ones fit any song;
   fade the last 1 s; peak about -3 dB; export 1080x1920 or 1920x1080 per template.
6. **Military Edits**: as Sports, with jets, aviation and military footage; match the song to the footage's intense,
   cinematic energy first.
- Why the audio rules: the song is the product; the drop sync makes an edit feel deliberate, and in format 1 the volume
  jump is the joke.

### 3.4 Eight music-page formats from the team's research doc
- Concert clips (growth; captions that react or report).
- A tweet-format post over video.
- Big events from the music angle.
- Raw music video clips (filler).
- A trending slideshow.
- Interview clips (growth; Genius as the reference).
- Comment-bait prompts ("Rarest stickers only"): the one format where the client's sound is the point. Check it against
  the "ask, never order" rule first: on Instagram an explicit comment ask loses recommendations (tentative: untested
  which platform suits it).
- Motivational edits.

## 4. Length follows the payoff
- 14 to 16 s for headline videos; 23 s for a chorus with 4 hook lines; 30 s for a live clip with an arc (a countdown, the
  line, the song coming in at 0:22); 36 s when the payoff needs it (all three scorecards, then the draw).
- Why: brand data does not show shorter winning (reach 5.2% under 30 s vs 5.6% at 30 to 60 s), so length is a test:
  8 to 12 s against 20 to 30 s, judged on skip rate.
- The second-by-second plan for a 7 to 15 s reel: `first-three-seconds.md` section 3.

## 5. Picking and preparing the clip
- Cut a music-video post on the hook or the chorus, never the intro (reviewer: "the main part of the song should go here").
  The cut moved from the intro to the first chorus, then the editor asked for a later stretch with "better visuals" (23 s,
  the hook line 4 times). Finding the window (replay heatmap, then the hook line in a transcript, then the loudest
  window): `editing-playbook`.
- Frame 0 is a face: start where the face lands and shift the crop focus if it is cut off.
- Cut out other channels' end cards and burned-in intro titles. Why: someone else's branding reads as a repost and
  wastes the seconds that drive loops.
- Subtitles for speech only, never lyrics; stop them before the song comes in; star out swears (f*ck, sh*t). Why: the
  song is the audio, lyrics on screen add nothing and risk misquotes, and swears risk limits.
- Keep the clip's own audio by default, with a 1 s fade-out and loudness normalised to about -14 LUFS; or the client
  song from its drop; or the song as a bed under the clip (about -14 dB). Mechanics: `premiere-ae-editing`.
- Prefer official sources (the artist's own video, the organiser's clips, platform clips with credit) over other pages'
  watermarked edits; confirm who is who before labelling a face (a wrong name on a face is the fastest way to lose a news
  page's credibility). Sourcing order: `research-and-sourcing`.
- When the only copy carries another page's burned-in caption, the pipeline can paint it out and keep the native UI (the
  LIVE badge, live comments) that makes a live clip feel real. That removes another page's work from its clip: a risk
  call for the reviewer.

## 6. Headlines and captions
- Headline grammar per story type, borrowed from the leaders. Why: a fixed grammar per story type makes captions fast and
  native to the niche.
  - Kurrco: "ARTIST & ARTIST - Title", "TITLE OUT NOW 🚨", "N years ago today ... Favourite track?"
  - RapTV: lines ending "‼️"
  - GBMC: one CAPS keyword, one emoji, asterisk censoring
  - Mixtape Madness: "🗓️: X dropped N years ago"
  - Daily Loud: always ends on a question
  - Pop Crave: neutral and sourced, for stats
- Mark 1 to 3 hook words in the accent colour; numbers are coloured automatically.
- Urgency words (JUST DROPPED, OUT NOW, DROPS TONIGHT AT 7PM, 🚨) only on time-sensitive stories (editor, 8 Oct: urgency
  only where it fits, "see where they would fit"). Everything else leads with the fact and ends on a question.
- Captions: the fact first, a short reaction or question last ("Troll of the year?", "W troll or fumble?"). Personality,
  but light ("have personality dont overdo it tho", editor, 9 Oct). Hype and heavy slang read as AI or spam.
- Caption formulas (research, 8 Oct): fact first, prompt last, 1 to 2 emoji, 0 to 2 hashtags, questions never orders.
  - Anniversary: "[N] years ago today [artist] dropped '[album]' 💿 Which track still goes hardest?"
  - Chart call: "'[Track]' is #[N] on the midweeks 📈 Number one by Friday, yeah or nah?"
  - Release: "[Artist] x [Artist], '[Track]', is out now 🚨 First listen: banger or skip?"
  - W or L: "[Artist] just announced [move]. Was that a W or an L?"
  - Head to head: "[A] and [B] both dropped Friday. Who ate the week?"
  - Hot take: "[Stat]. Our take: [mild opinion]. Are we wrong?"
  - Quote: "[Artist] on [topic]: '[short quote]' Does he have a point?"
  - Who's next: "[Artist] passed [N] monthly listeners from [city] 📈 Who's the next UK name to blow?"
  - Vary the wording: "rate it" and "W or L" sit close to the banned set-word asks.

## 7. Carousels and Stories
- Slide 1 is the card (a claim or a number plus a face); one fact per slide with its own headline; 2 to 3 slides for news,
  5 to 8 for timelines and rankings; the last slide worth sending (a ranking, a chart). Slide 2 is a second cover.
- Ship a 9:16 Story still with room for a poll sticker, and a pinned-comment line, with each carousel.
- Why: carousels lead engagement and saves, sends drive non-follower reach, and Story polls give real numbers for later
  posts. An honest numbers carousel (two rivals' real counts side by side, dated) was approved.

## 8. The house look
- Bold caps headline, numbers in the accent colour, a tweet card over a clip, carousels. Approved by the reviewer and the
  editor, and chosen as the look for faceless brand pages too.
- Accent colour per story type: beef, court, breaking #FF3B30 (red); charts, money #30D158 (green); throwback, birthday
  #FF9F0A (orange); a leader-style orange #FF7A00; general news #FFD60A (yellow). Why: the leaders colour-code by story,
  so the colour tells the story type before the words.
- Platform stories carry the platform's logo tile (Apple Music, Spotify, Billboard), not a word pill like "CHARTS"
  (reviewer). Why: a logo reads faster and signals a real source.
- The page mark is the profile picture + @handle as a byline above the headline, never a text wordmark ("write @[handle] and
  stuff instead to show it is a username. over time we wanna build better and better branding"). Why: a handle reads as
  a page people can search and follow.
- Tweet cards only for our own accounts, no blue tick unless verified. Why: Instagram demotes screenshots of other
  accounts, and wide photos behind a portrait card crop badly.
- Apple-style emoji everywhere ("emojis yeah those type of emojis"): the audience and the leaders use them; Windows emoji
  look off-brand.
- Fonts: a condensed face (Coolvetica Hv Comp) on card headlines only; on video a condensed face was hard to read on a
  phone in a 5-font A/B, so video headlines use Proxima Nova Extrabold; Impact for meme headers; Helvetica for tweet
  cards; a separate face for numbers.
- A title card wider than a portrait frame goes full width on a blurred backdrop, never cropped (a crop cut the title's
  words).
- Template mechanics: `production-automation`; type and motion: `motion-design`.

## 9. Dated hooks: the UK chart week (as of Oct 2026, re-check)
- Official Charts First Look on Sunday (on X 19:30 to 20:00 UTC), the Update on Monday (on X 16:00 to 18:30 UTC), the
  Trending chart on Tuesday, the final chart on Friday (Radio 1 from 16:00, the reveal at 17:45 UK).
- Midweek posts say "on course for #N" and go out before Friday; the Friday chart card goes out after 17:45.
- Why: chart news is the most predictable postable news, and midweeks let a page post before the result.

## 10. Verdicts to match
- Approved: tweet videos ("fire", reviewer); the split format ("format perfect"); the troll-song caption style ("we really
  like the captioning style of the last one video", editor); coloured numbers; platform logo badges; honest numbers
  carousels.
- Rejected or weak: a condensed headline font on video; a CHARTS pill where a platform logo fits; urgency on everything;
  opinion versus posts with no live story ("empty"); stale stories; throwbacks and plain release posts; a low-pull
  freestyle; nice stories with no tension; recaps more than weekly; one artist too often.
- Of the first four batches, the posts the team actually put up were the ones on a live beef story; everything else
  expired. Live tension is what gets posted.

## 11. Risk calls that belong to the reviewer
- News posts reuse music videos, interviews and other pages' footage without a licence; the team accepted that risk for
  its own pages. An older handoff rule for these pages said not to raise copyright concerns on footage sourcing (flag
  only dead, fake, AI or impersonator sources); the reviewer decides whether their kit keeps it. Until they decide, the default
  is ours: no repeated copyright warnings on our own pages (flag only dead, fake, AI or impersonator sources), full
  warnings for paid and client work (`research-and-sourcing` licensing-and-rights.md section 1).
- Painting out another page's burned-in caption (section 5).
- Reading X through an unofficial mirror or a logged-in browser can break X's terms and cost the reading account; use
  throwaway monitoring accounts only, never a page's own.
