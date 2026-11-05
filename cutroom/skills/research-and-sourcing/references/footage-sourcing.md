# Finding footage, stills and documents

Where to get pictures for an edit or a post. Which shot to use where, and how to cut it, lives in editing-playbook;
download, frame-grab and OCR mechanics live in premiere-ae-editing (references/youtube-downloads.md,
references/media-toolkit.md, references/stills-and-sources.md). Rights for every source: licensing-and-rights.md.

## Contents
1. The order to look in
2. The client's and the talent's own material
3. Official sources for news visuals
4. YouTube research without downloading
5. Footage maps, and links for the user to download
6. Archive of famous people
7. Free stock libraries
8. Photos and public-domain archives
9. Documents as evidence: headlines, articles, papers, posts
10. Filming the real app instead of faking screens
11. Borrowed clips when platforms are blocked
12. Tagged clip libraries
13. AI footage
14. When nothing exists
15. Quality and hygiene checks
16. Downloads: the rules and where the mechanics are

## 1. The order to look in
1. **The client's own material and masters:** their rushes, B-roll, brand press footage, product shots, the talent's
   own photos. Why: the cleanest rights and the best quality (a YouTube copy is a re-encode).
2. **The talent's or subject's own team** for archive and photos of a famous person. Why: the fastest clean route; the
   big archives are editorial only (licensing-and-rights.md section 6).
3. **Official channels:** the artist's own channel and videos, the event organiser's own clips, broadcasters' own posts.
4. **Free stock and licensed archive**, and public-domain archives for history.
5. **Platform clips with a credit,** X post media at original size, YouTube thumbnails, and frames from music videos as
   artist photos (news pages).
6. **Your own recordings** (the real app, a real screen) when the subject is a product.
7. **A pickup shoot or AI generation** (the user generates AI) when nothing exists (section 14).

Avoid: other pages' watermarked edits (they count as reposts and look it), auto-generated YouTube "Topic" thumbnails
(a logo on black), thumbnails carrying a label logo, dark fan rips, photos where the subject is tiny, and news-agency or
broadcaster photos (placeholders only until licensed).

## 2. The client's and the talent's own material
- Catalogue every clip into usable sections with source times and the subject's position (contact sheets), so a
  request becomes a lookup. Placement judgement: editing-playbook.
- When a generic shot is disliked, look for the talent's own footage of the same idea first (a disliked pool shot became
  the talent's own calf-stretch shot under "for the recovery").
- **Diff overlapping asset folders at intake and ask which set is current.** Why: older presenter stills were reused
  while newer ones sat in the shared folder, and the swap cost 17 re-renders later ("replace ... WHEREVER they are in
  the video").
- **Picking from a client's own video library** (for cutdowns): score candidates on title action words, the page's
  topic multipliers, the YouTube outlier band (2 to 4x did best on Facebook), length (18 to 45 min feeds a long cut, a
  standalone and shorts) and freshness (never posted, or 180+ days since the last post). Then check by hand that the user
  has not already edited it, the page's history (by length within 5% and by title) and the Most-replayed heatmap.
- **Watch for cross-promo inside the client's own videos:** a narrator's promo for another video, with 4 s of a
  different person, slipped into one cut. Cut such clips whole.
- **Ask for masters** rather than downloading the client's own uploads (licensing-and-rights.md section 10).
- **Ask the user for packs** when downloads are blocked: YouTube blocked 4K re-downloads after about 40 downloads, and
  the user can supply 4K scene packs or clips.
- Music clients: ask for edit-ready versions of the song (music-and-sfx-sourcing.md section 1).

## 3. Official sources for news visuals
- Sourcing order for a news post: the artist's official video or channel, the organiser's own clips (a promoter's 4K
  face-off, a festival's own live clip), platform clips with a credit, X post media at original size (`?name=orig`),
  YouTube thumbnails (`i.ytimg.com/vi/<id>/maxresdefault.jpg`, 1280x720, then `hqdefault.jpg`), then frames from music
  videos as artist photos.
- Drop the story when no usable solo photo exists (two big US artists were dropped from one batch for that reason). A
  fan rip of a classic track was swapped for the festival's own live clip.
- When the only copy of a live clip carries another page's burned-in caption, ffmpeg `delogo` over its box removes it
  while keeping the native UI (a LIVE badge, live comments). It is a rights and originality risk: flag it, the reviewer
  decides (licensing-and-rights.md section 9).
- Source badges for platform stories: the platform's logo as a simple-icons SVG in its brand colours (editorial use;
  never imply endorsement).
- Downloading exact sections of a YouTube video (1080p H.264, `--download-sections "*S-E" --force-keyframes-at-cuts`)
  instead of whole files: premiere-ae-editing youtube-downloads.md and media-toolkit.md section 2.

## 4. YouTube research without downloading
Why: exact timestamps for every script line at almost no token cost, and nothing is downloaded. Reading a video's page,
captions, heatmap and scrub storyboard is fine; downloading is a separate decision (section 16).
- **Search through the public results page:** `https://www.youtube.com/results?search_query=<query>`. Find
  `ytInitialData` in the HTML (match `ytInitialData\s*=\s*`), decode from the first `{` with
  `json.JSONDecoder().raw_decode`, and walk the tree for `videoRenderer` objects: `videoId`, the `title` runs,
  `ownerText` (channel), `lengthText`, `viewCountText`, `publishedTimeText`. Run many queries in parallel and print one
  table of unique videos with the queries that found each. Some result pages came back without a findable
  `ytInitialData`; the looser match, retries with backoff and about 3 threads fixed it. One run: 30 queries, 88 unique
  videos.
- **Watch-page facts:** `lengthSeconds`, `ownerChannelName`, `uploadDate`, `shortDescription`,
  `playabilityStatus.status` and `<meta name="title">`, read from the watch page's HTML.
- **Storyboard contact sheets (the scrub-preview sprites):**
  1. The watch page holds `"playerStoryboardSpecRenderer":{"spec":"..."}`. Replace the escaped ampersand `\u0026` with `&` and split on `|`.
  2. Part 0 is the base URL. Each further part is one level: `w#h#count#cols#rows#interval#name#sigh`.
  3. Use the last level (the biggest tiles). The time step is `interval / 1000` seconds, or `length / count` when the
     interval is 0.
  4. Frame k sits on sprite sheet `s = k // (cols x rows)`. The sheet URL is the base with `$L` replaced by the level
     index and `$N` by the level name (with `$M` replaced by s), plus `sigh=<sigh>`.
  5. Crop each tile at its column and row, label it with its time, and lay the tiles out 8 per row. Aim for tiles of
     about 192x108 and two videos per image (a first try made 3200 px sheets: too big to read).
  - One round produced 18 sheets and a footage map for 7 ads; the user then downloaded only the moments named.
- **Most replayed:** the heatmap comes in the metadata JSON (`yt-dlp -J --skip-download`, about 45 s a video, nothing
  downloaded). It finds hook moments in long videos and songs (music-and-sfx-sourcing.md section 3).
- **Be gentle:** about 80 quick metadata lookups in a row triggered YouTube's bot check; space requests and run one
  YouTube job at a time across sessions.
- Helpers built for this (search, watch info, storyboard sheets) were lost once when a session's scratch folder was
  cleaned; keep such tools in the job or kit folder (research-reports-and-folders.md section 6). Copies recovered from
  a transcript sit in `library/pipelines/youtube-research/` (`yt_search.py`, `ytinfo.py`,
  `storyboard.py`, `sb_batch.py`, `crops.py`, `sharp.py`): untested since recovery, and `sb_batch.py` predates the
  192x108 tile fix, so test them on one video and re-apply that fix before relying on them.

## 5. Footage maps, and links for the user to download
- **A footage map per script line:** video ID, channel, the usable moments with timestamps, a label (exact, stand-in,
  mood only), and what is wrong with each (logos, officials, blur, low resolution). Mark videos to avoid and why (a
  roadside moment the talent would not want shown; a video whose title makes a wrong claim).
- **When the user downloads,** give numbered links in chat in priority groups ("Download first": 6, "the rest": 12),
  each with the timestamps of the usable moments. Why: the user could not click local paths in chat, and timestamps mean
  he grabs only what gets used.
- **Public figures' own clips:** give exact URLs and timestamps for the user to download.
- A private pull-list page (stock picks per line, archive and its licence route, what needs approval) works well before
  anything is downloaded (research-reports-and-folders.md section 7).

## 6. Archive of famous people
- Expect editorial-only archive: one agency held about 151 clips of a famous athlete, all editorial; the key year of
  the script's story had no video anywhere, only stills; and the stills of a famous collapse were taken after a race,
  not during the illness the script describes, so they could not illustrate that line.
- **Agency comps are placeholders:** Getty pages are readable by script, and `downloadableFilmCompUrl` in the page JSON
  gives a watermarked comp (one was 576x432, 28 s). Name it `COMP-WATERMARKED_<agency>-<id>_<what>.mp4` and keep it in a
  folder named "... (watermarked comps - licence before use)".
- **Frame-check every archive shot before use:** other famous people in frame (royals, celebrities), rivals and other
  athletes, sponsor and kit logos, event marks, a rival drink brand (three agency refuel stills showed a sports drink),
  family members (they need consent), officials. Crop, blur or skip.
- SD archive reads as archive: present it that way rather than pretending it is sharp (placement: editing-playbook).
- Narrated pieces ask for archive on real-world beats (shutdowns, firings) more often than you would guess (tentative:
  one reviewer's pattern).

## 7. Free stock libraries
- **Pexels** (free licence, no attribution): good for objects (tablets, capsules, powders, bottles); weak for supplement
  shelves and protein tubs (mostly cosmetics and grains). Search pages block curl with a Cloudflare page, so search in a
  browser pane and read the results from the page (the search page's `__NEXT_DATA__` JSON: media-toolkit.md section 3).
  Make one labelled thumbnail sheet per search and shortlist by eye. Thumbnails sit at
  `images.pexels.com/videos/{id}/{slug}-{id}.jpeg?auto=compress&w=300`. Older clip IDs resolve at
  `videos.pexels.com/video-files/{id}/{id}-{hd|uhd}_{w}_{h}_{fps}fps.mp4` (HEAD-probe first); newer IDs (above about 20M)
  cannot be guessed, so use the site's own download link or the user grabs them. Never click the Turnstile on a clip
  page. Skip AI-generated results. One round: 22 searches, about 520 clips reviewed on 23 sheets, 27 direct downloads
  offered. Free API keys avoid the 403s: ask the user for them.
- **Mixkit:** "Free" clips are fine; "Restricted" means personal use only (it ruled out most of its Bitcoin, chart,
  neon and named-city clips); free files are 720p; it answered 429 once.
- **Coverr:** use its non-AI clips; its API needs a key, but its tag pages work without one.
- **Pixabay:** fine licence; blocks scripts without a free API key.
- **iStock comps** are for test layouts only (licensing-and-rights.md section 5).
- **Frame-check every clip** for faces in focus (no strangers' faces in a celebrity ad: hands and objects are fine, the
  user: "video of hand full of pills and stuff i still can keep"), brand names (boot brands, sponsor boards, a sponsor
  logo in a skyline), other trading platforms' screens, landmarks with lighting copyright (the Eiffel Tower at night),
  and anything wrong for the client that a slug hides (holiday hats, religious symbols, brand names on props). One round
  kept 34 free clips (1.25 GB) and rejected 11 of 45 for these reasons.
- **Stock is filler only.** Stock used as wallpaper reads as an ad on native pages, and some brand guides ban stock
  photos outright.
- **Unflattering health subjects:** identifiable people may not be shown in a bad light or as endorsing a product, so
  use the backs and tops of heads, hands, mirrors and a scalp camera (for hair loss); add a "posed by model" note when a
  model appears in an unflattering subject.
- **Niche gadgets:** no free stock existed of people wearing them (Pexels, Mixkit and Pixabay searched); a stand-in that
  matches the line (a woman in a plain cap, because the voice says the caps look normal) held the slot until real
  footage arrived. Offer a shoot or the brand's press B-roll.

## 8. Photos and public-domain archives
- **Wikimedia Commons API** for photos of players and public figures: take the largest standard sizes (portraits
  1920x2880, landscapes 3840x2560), because full-size originals get rate-limited. Credits: "Photo: Name, CC BY 4.0";
  for CC BY-SA "Photo: Name, CC BY-SA 4.0, via Wikimedia Commons" (edited versions stay under the same licence); CC0
  needs nothing; mark edits "(edited)".
- **Public-domain film and images:** Prelinger Archives (on archive.org) for old film; NIH/NLM and CDC PHIL for lab and
  medical history; NASA imagery (the Black Marble night Earth). Expect tiny photos of minor historical figures.
- US federal government video may be public domain (tentative: not checked for one central-bank press video).
- News-agency and broadcaster photos are placeholders until licensed.

## 9. Documents as evidence: headlines, articles, papers, posts
- Evidence beats illustration: the actual tweet, letter, filing, launch graphic, paper or headline. (How to show it:
  editing-playbook and motion-design.)
- **Headlines:** only ones that really ran, word for word from the live page, tagged verified or not. One round found
  26 headlines and checked 14 word for word on the live pages. Capture with headless Chrome (premiere-ae-editing
  stills-and-sources.md). Crop the "[an error occurred while processing this directive]" line on old BBC pages; decline
  the cookie banner first (the Guardian's "No, thank you"). Recreate without mastheads or logos (licensing-and-rights.md
  section 7).
- **Papers:** Europe PMC's REST API for the full text when PMC blocks scripts; PubMed pages screenshot well for a
  source card; quote from the full text when the screenshot lacks the line.
- **Shop pages** that crash headless Chrome: use the user's screenshot, or a typeset quote card of the exact text.
  Blur seller names on shop screenshots. Brand names on a product: repaint on smooth surfaces rather than blur (a blur
  box reads as hiding something; method in premiere-ae-editing).
- **Fetch blocks:** big news sites block research fetchers; take the publish time from Google News RSS and the page from
  the user's browser.

## 10. Filming the real app instead of faking screens
Why: the real app screen was the one device every partner hit in the category shared; it shows the brand without an
added logo; it has no broadcast-rights problem; and designed stat or odds cards failed (one automated card page had 2
views, and our own designed cards were rejected: "the UI is bad").
- **Capture:** headless Chrome at 390x844 CSS px, device scale 3, an iPhone user agent. Take screenshots as fast as
  Chrome paints (about 10 to 15 a second) and retime them to a steady 30 fps.
- **Timed windows** (a 15-minute market): film the last 90 s plus 20 s after the result. **Live events** (a match page):
  keep a rolling buffer at about 4 fps and save 150 s before to 60 s after each event.
- **Pop-ups on React or Next.js sites:** never delete DOM nodes (removing them crashed the site). Click the dialog's
  close button, press Escape, then inject a style rule that hides `[role=dialog], [role=presentation][data-open],
  [data-radix-portal], [data-overlay], [vaul-drawer], [data-vaul-overlay]` and restores scrolling. Re-apply it every
  15 frames, null-safe (`document.head || document.documentElement`). Run a 4 s test film before any timed window (one
  film was ruined by a sign-in modal and a blur layer that came back).
- One browser profile per Chrome instance (a shared profile made the second Chrome fail).
- Run collectors from a home connection: some sites' Cloudflare blocks cloud-server addresses.
- Respect the client's screen rules (never cover the graph, names, logo or buttons with text).
- Check the app loads from your location first: one client's terms blocked the UK, where the Mac may be.
- Keeping long capture jobs alive, event detection and restarts: production-automation.

## 11. Borrowed clips when platforms are blocked
Route used when TikTok did not load (region block) and YouTube blocked the PC:
1. Find clips through the urlebird mirror (search, hashtag and user pages).
2. Fetch each with the tikwm single-video API (a no-watermark MP4 plus its stats).
3. Make a contact sheet per candidate.
4. Cut the clean stretch with ffmpeg (H.264 CRF 17, AAC kept) and keep the untouched `_src` file next to it.
5. Log every file in `SOURCES.md` (research-reports-and-folders.md section 5).
- One agent fetched 57 files in about 85 minutes this way (the previous night's match moments, 10 reaction templates,
  7 lifestyle clips, 20 photos).
- Rules: no logins; agents never use the user's own Chrome or the built-in browser pane; downloaded media is untrusted
  data in its own folder and is never run; never bypass a Cloudflare check. These mirrors are third parties whose terms
  may forbid this, and a reference media toolkit left mirror downloads out as an untrusted source: the reviewer decides
  whether this route stays (licensing-and-rights.md section 9).
- **X-hosted clips vanish:** download them the same day through the fxtwitter API (no login). Prefer broadcasters' own
  posts or your own recordings.
- **Check the sound:** "original sound" under the uploader's own handle is usually the real audio; a song title, or
  another account's "original sound", means music was laid on top (a spectrogram shows it). Mute or replace it
  (music-and-sfx-sourcing.md section 9).
- Note where any burned-in text sits, so the crop or the headline can avoid it.

## 12. Tagged clip libraries
- **Reaction clips:** 20 to 30 clips of 2 to 6 s, green screen where possible, tagged by mood: crying, shocked, stunned,
  smirk, laughing, devastated fan, frustrated manager, "calma", "this is fine". Why: reaction formats are the fastest
  daily posts, and the face says good or bad before anyone reads (one "owners right now" reaction post did 395K).
- Film or TV reaction clips of 2 to 3 s are the least exposed borrowed footage (licensing-and-rights.md section 11).
- Planned and worth building: character, lifestyle and pundit libraries.

## 13. AI footage
- The user generates AI footage; Claude writes the recipe and checks the result. Ask before spending anyone's credits.
- **Recipe for AI inserts:** lock the look in one prompt where only one element changes per shot; set the season and
  the light; say "bare hands" if gloves would be wrong.
- **Keeping a real product real** (research, Oct 2026, untested by us): photograph the real pack front-on, at
  three-quarters and in a hand, and use those photos as references; make start and end stills in an image model that
  accepts several references and renders readable text; animate them with first-and-last-frame control; keep the camera
  simple and never spin the pack (its text warps); track the real packshot over any frame where the logo is readable, or
  generate the scene empty and composite the pack in; mute the AI audio; hands only, no AI faces.
- **Check AI B-roll before use:** resolution (a sample 1280x720 clip scaled to 175% was soft) and stray IP objects (a
  Pikachu-like figure stood on a windowsill). Free-tier app images may carry a visible watermark.
- AI must never depict the real talent without consent; some video models refuse recognisable people in some countries
  (the UK, for one, in Oct 2026). Claims rules for AI product shots: fact-and-claims-checks.md section 11.

## 14. When nothing exists
- Say so early and offer a pickup shoot, the brand's press B-roll, AI generation (the user) or a labelled stand-in.
  Why: a weak stand-in costs a review round. Example: no free library had "a shelf crammed with supplement tubs, then
  only the pouch"; the reviewer then asked for AI B-roll there.
- Placeholders: tag every stand-in "PLACEHOLDER" on screen and list each slot with timecodes in the build notes, so
  nothing ships by accident and the 3D artist or shooter gets a work list.

## 15. Quality and hygiene checks
- **Source quality is part of the look:** heavy effects on low-resolution footage look cheap; the best fan packs
  advertise 4K at 60 to 120 fps (often upscaled); 720p knockouts read soft.
- **Before cataloguing a pack:** rename files to ASCII (`fNN_name.mp4`; emoji names broke tools); find the real
  picture inside pillar or letter bars; note burned-in captions, score bugs and watermarks (a fan pack had a blurred
  watermark top left; a compilation burned fighter names and a "Round 2" bug into a 4:3 picture); check for hidden cuts
  inside "shots" of compilations and scene packs; expect about a third of fan-pack "action" shots to hide the subject
  (110 of 167, 35 of 67 and 49 of 103 were clear in three packs). Mechanics: premiere-ae-editing timing.md.
- **For a key moment, source every angle:** the live wide shot and the close replays. One wide shot zoomed 2.2x was soft
  and unreadable (how to use them: editing-playbook).
- Other channels' end cards and burned-in intro titles get cut out (editing-playbook).
- Watermarks that OCR misses can be found from pixels; clean copies of watermarked memes usually exist on the original
  posts (only when the user asks): media-toolkit.md section 4.
- **Reference downloads for study** (only when the user approves): 720p is enough (5 to 15 MB each); use an
  orientation-neutral size limit (five vertical references failed because the filter assumed landscape).
- Check free disk space before big pulls.

## 16. Downloads: the rules and where the mechanics are
- Ask first: the host, the folder, the file naming and the total size. One download at a time across every session,
  into the job folder, logged in a manifest. Never buy anything.
- YouTube: premiere-ae-editing references/youtube-downloads.md (the PO-token route, Windows script; on a Mac use the
  plain yt-dlp route in media-toolkit.md section 1 until the script is ported). Read the rights note first
  (licensing-and-rights.md section 10).
- One moment of a long video, frame-accurately, without the whole file: media-toolkit.md section 2.
- Instagram reels of public accounts and X videos download with yt-dlp without a login.
- A Vimeo video that answers 401 is restricted by its owner, and a TikTok blocked on one network may be blocked for a
  reason: ask the client for the file instead of working around it.
- When YouTube blocks every route (it did, even with the PO token), ask early for a throwaway account's cookies file
  (never a personal account) or for clips supplied by the user.
