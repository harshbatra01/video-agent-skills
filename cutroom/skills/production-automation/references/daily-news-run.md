# The daily news run

Design notes for a daily news pipeline. The code is not included: build it from these notes.

The newsdesk turns the day's music and rap news into finished posts for two news pages: cards, carousels, 9:16
headline, tweet and split videos, Story stills with poll space, a captions file per page and a posting schedule. Every
video ships its Premiere layers and two XMLs. Built 7 Oct 2026, run daily from 8 Oct; 9 batches by 13 Oct.
What makes a post worth building (the interest test, hooks, captions, posting windows, platform rules) is in
social-video-formats; verifying stories and sourcing footage is in research-and-sourcing. This file is the machine.

## 1. The run at a glance
| Step | Who | Command or action | Time |
|---|---|---|---|
| 1 Trigger | user | "today's batch" (nothing runs on a timer yet) | |
| 2 Scan | Claude | `python3 scan.py` | about 5 s |
| 3 News sweep | Claude | Google News RSS: `UK rap when:2d`, `UK rapper when:2d`, a few big UK names | 1 min |
| 4 Shortlist | Claude | drop covered stories, topic fatigue and the skip list; score the rest; build only 7/10+ | |
| 5 Pick the set | Claude | 1 video + 1 carousel per page per day, UK first, never one asset on both pages | |
| 6 Verify | Claude | one primary source per story type; sources and skips into the batch `note` | most of the time |
| 7 Added fact | Claude | the one number, time or context the source does not show | |
| 8 Assets | Claude | `fetch.py search / peak / yt / loud / thumb / frame / x / url`, one YouTube call at a time | |
| 9 Spec | Claude | write `batches/<date>.json` (`ls` first) | |
| 10 Build | Claude | `python3 vcn.py build batches/<date>.json [--only a,b]` | about 1 min |
| 11 Look | Claude | `python3 vcn.py sheet <date>`; fix undelivered drafts in place; re-check | |
| 12 Deliver | Claude | `python3 vcn.py drive <date>`; update `FINALS/SCHEDULE.md`; hand-over table + sheet + videos | |
| 13 Review | user, reviewer | notes (often phone screenshots); delivered posts change only as `_v2` | |
| 14 Post | user | from the Drive phone app in the window, the client's official sound picked in the app | |
| 15 Measure | user | Insights at 24 h and 72 h, Story poll counts back to Claude (not started yet) | |
- Claude time: about 8 to 10 minutes for a 4-post batch, about 35 minutes on a heavy verification day.
- Automatic inside the tools: ranking, breakout metrics, bar cropping, loudness, number colouring, versioning,
  captions file, the Drive copy.

## 2. Files
- `README.md` (daily run, every post field), `PLAYBOOK.md` (the page-manager rules: interest test, retention,
  30-day plan, metrics), `captions.md` (caption house style), `brand.json` (pages, handles, avatars, tweet style
  light/dark, accents, fonts; identity is a placeholder until decided).
- `scan.py` (digest), `fetch.py` (assets), `vcn.py` (builder, sheet, Drive copy), `templates/card.html` (every
  layout, the colour markup, number colouring, the fit loop).
- `batches/` (one JSON per day; worked examples ship), `FINALS/<batch>/@<page>/` (clean finals) +
  `FINALS/SCHEDULE.md`, `out/<batch>/premiere/` (layers and XMLs), `out/<batch>/_temp/` (scratch), `out/scan/`,
  `in/` (downloads), `assets/` (avatars, cached emoji and logos).
- Needs: Chrome, Python 3 with Pillow and PyAV (`av`), ffmpeg with libass (subtitles), yt-dlp + Deno (YouTube),
  gallery-dl (optional), the premiere-ae-editing scripts `media/hear.py` (subtitles) and `media/frames.py` (sheet).

## 3. Scan and pick
- **Lean by default.** `scan.py` reads 12 main X pages (5 UK, 7 US leaders) through the free, unofficial fxtwitter API
  (`api.fxtwitter.com/2/profile/<handle>/statuses`, `/status/<id>`, `/2/search?q=<terms> since:YYYY-MM-DD`), default
  window 30 hours, and writes `out/scan/scan_<time>.md` (UK top, all top, Breaking out, Most talked about, viral posts,
  What's working) plus a `.json` of every post. Why lean: "all of this stuff can easily be found from main pages...
  payout is so low if we have so many sources" (the editor). `--full` adds 81 feeds, Shazam and Apple charts, Google
  Trends and a birthday calendar; it reads the feed list (`03-news-feeds.json`) from `VC_RESEARCH_DIR`, else from
  `../research`.
- **Retry before calling a handle dead:** 2 to 3 tries with letter-case variants and reordered terms (five handles
  404'd once and worked on a retry).
- **Breakout metrics.** `over` = a post's views divided by its page's MEDIAN views (2.5x or more = breaking out);
  `talk` = (replies + quotes) per 1,000 views, on posts over 5K views (debate potential); `share` = (reposts + saves)
  per 1,000 views. "What's working" groups the last 7 days of scans by story type. Why the median: one viral outlier
  moves an average and hides what is normal (the reviewer's concept doc used "3x the page's average"; we advised the
  median).
- **Artist ranking.** UK sources weigh 1.5 and UK artists x1.3, plus chart and trend presence and `log10(views)/2`;
  aliases for every spelling seen; short ambiguous names matched case-sensitively; a separate UK top section. Why: raw
  counts favour US pages that post 20 to 40 times a day and buried UK stories; one big page misspelled an artist in 14
  of 15 posts.
- **The news sweep** catches what the X pages skip (a big show announcement was only on news sites) and gives exact
  publish times, the best "who posted first" tool.
- **An empty result is an error.** Geo-blocks fail silently (a chart API returned `{"data":[]}` from a blocked region with no
  error); give every source a "fewer than N rows" alarm and run scans from a UK or US machine when possible.
- **Pick the set:** 1 video + 1 carousel per page per day (the standing routine since 10 Oct), UK first; the UK page
  gets UK stories, the wider page gets the biggest rap, music and money stories; never the same asset on both pages,
  and if one video serves both, each page gets its own section of it.
- **Skip list and verification** are research-and-sourcing rules; the batch `note` records the sources checked and
  every story left out with its reason (example: "Skipped: ... (no winners list online yet), ... (tabloid dating
  rumours), ... (prison violence)").

## 4. Assets (`fetch.py`)
- `yt <url|id> <start_s> <dur_s> <out.mp4>`: an exact 1080p H.264 section, `-f "bv*[height<=1080][vcodec^=avc1]+
  ba[ext=m4a]/bv*[height<=1080]+ba/b[height<=1080]/b" --download-sections "*S-E" --force-keyframes-at-cuts
  --merge-output-format mp4` (dur 0 = whole video). Why: exact H.264 sections import cleanly in Premiere and skip
  whole-video downloads.
- `search "<query>" [n]` (`ytsearchN:`, prints id, title, channel, duration, views, live status: finds scheduled
  premieres); `peak <id> [dur] [skip]` (start of the most replayed window from the YouTube heatmap, skipping the first
  8 s); `loud <video> [dur] [skip]` (loudest RMS window, skipping the first 10 s and last 6 s, for uploads too new for a
  heatmap); `thumb` (`maxresdefault.jpg` 1280x720, then `hqdefault`); `frame <video> <sec> <out.jpg>` (music video
  frames make good artist photos); `x <status> <prefix>` (every photo and video of an X post via fxtwitter, photos at
  `?name=orig`); `url <url> <out>`.
- **Cut music-video news on the hook or chorus, never the intro:** the heatmap's best window first; if the upload is too
  new, the hook line in a Whisper transcript; else the loudest window. Frame 0 is a face (shift `fx`/`fy` if cut off).
  Cut out other channels' end cards and burned-in intro titles. (Taste: editing-playbook.)
- **YouTube etiquette:** every yt-dlp call goes through one throttled function: one at a time across every process
  (`out/.yt_lock`, stale after 20 min), 6 s apart, `--sleep-requests 0.75`. If blocks come back often: a THROWAWAY
  account's cookies exported to `secrets/youtube_cookies.txt` (the script uses it automatically and never prints it).
  Never a personal or the reviewer's account: Google can flag accounts used by download tools.
- `fetch.py` does not start the PO-token server or set the `mweb` client that premiere-ae-editing's `ytdl.py` uses,
  so it may get lower formats or blocks sooner; for fewer blocks reuse that skill's token setup (Windows) or its plain
  yt-dlp route (Mac).
- Instagram downloads need cookies (gallery-dl with a throwaway account). TikTok was blocked from the editor's country.

## 5. The batch file (the single source of truth)
- Common fields: `id` (e.g. `z1_headline`: page letter + order + slug), `fmt`, `account` (or once per batch),
  `headline` (`*word*` = accent colour, `^word^` = second accent, red; 1 to 3 hook words), `sub`, `label` (a pill:
  NEW MUSIC, THROWBACK, CHARTS, COURT...) or `logo` (a platform badge: any simple-icons name such as applemusic,
  spotify, billboard, or a PNG path), `theme` (beef / court / breaking red #FF3B30, charts / money green #30D158,
  throwback / birthday orange #FF9F0A, a RapTV-style orange #FF7A00, news yellow #FFD60A) or `accent` "#hex",
  `caption`, `when` (the posting window note).
- Media: `photo` + `focus` ("center 25%"), `photos` (two for split and vs), `inset`, `faces`; or `clip` {`path`, `in`,
  `dur`, `fx`/`fy` 0 to 1, `fill` "crop" | "blur", `crop` (false | "w:h:x:y"), `pre` (an ffmpeg filter such as
  delogo), `bg` "black" in the faceless fork}.
- Audio: {`mode` clip | song | mix, `song`, `song_in` (start at the beat drop), `bed_db`}. Subtitles: `subs: true`,
  `subs_until` (stop before the song), `subs_margin`.
- Engagement: `slides` [{photo, focus, headline}] turns a card into a carousel (`NN_post/1.png` = the card, then one
  slide per photo); `story: true` + `poll: "A / B"` adds a 9:16 Story still with room for a poll sticker; `pin` = a
  first comment to pin. All three show up in the captions file.
- Batch level: `name`, `account`, and a `note` listing sources checked and stories skipped. Delivered rebuilds keep
  their old settings in `history`.

## 6. Formats the builder knows
| fmt | Kind | Notes |
|---|---|---|
| `uk` | card, or video when a clip is given | card: full-bleed photo, dark gradient, condensed caps headline in the bottom third, pill or platform logo, optional inset circle, avatar + @handle; video: headline under the clip, wide clips in a blurred box at least 760 px tall centred at y 650 |
| `raptv` | card | photo on the top 60%, 8 px accent rule, a date badge ("OCT/26") |
| `meme` | card or video | white band with an Impact headline (video band 460 px), face circles with a red ring for court and beef |
| `tweet` | card or video | our own page's tweet only (light or dark), no blue tick unless verified; a photo tweet is drawn as a real screenshot with the photo inside; video = card on top, clip under it |
| `split` | video | two photos 540x470 on top, white rounded caption box, clip from y 560 (the @rap-style standard layout) |
| `quote` | video | the exact words as the headline, the speaker as `sub` |
| `chart`, `list`, `vs`, `slide`, `ytc`, `tt` | cards (and a one-off video style) | chart rank with up/down/NEW and stats; list rows (`style: prices`); two-photo VS with a Story version; carousel slides; a YouTube comment rebuilt sharp in YouTube's dark style; a plain caption style |
- Cards are 1080x1350 PNG; videos 1080x1920 at 30 fps.
- Parked formats (seen, not built): calendar cards (birthdays, anniversaries: off by default), sticker-caption
  freestyle clips, named series.

## 7. What the template does for you (`templates/card.html`)
- **Fonts by role:** a condensed heavy grotesque (Coolvetica Hv Comp) for card headlines; Proxima Nova Extrabold for
  video headlines and the split caption box; Impact for meme headers; Helvetica for tweet cards; a numbers face
  (Bahnschrift on Windows) for stats. Why: a 5-font A/B on a real video showed the condensed face was hard to read on a
  phone, so video headlines use the wider face. House fonts can be set per page in `brand.json`.
- **Numbers in the accent colour automatically** on cards, video headlines and every carousel slide; tweet cards stay
  plain like real tweets; names that start with digits are skipped. Regex: `NUM=/(^|[\s(\/'"‘“;-])((?:#|\$|£)?\d(?:[\d,.]*\d)?(?:\s?(?:BILLION|MILLION|BN|K|M|B|%|PM|AM)\b)?\+?)(?=$|[\s),.!?:;'"’”\/-])/gi`
  and `NUM_SKIP=/^(21 SAVAGE|50 CENT|42 DUGG|24KGOLDN|1017)/i` (the regex contains curly quotes and a pound sign on
  purpose). Why: the number is usually the hook, and the reviewer asked for numbers always in another colour. A post with
  `autohl: false` keeps its numbers plain.
- **Page mark = the page's avatar + @handle**, never a text wordmark; on videos it sits as a byline above the headline.
  Why: a handle reads as a page people can search and follow.
- **Platform logo tiles** instead of label pills for platform stories (simple-icons SVG in brand colours on a rounded
  tile, radius 23%), cached in `assets/logos`. Why: a logo reads faster than a word and signals a real source.
- **iPhone-style emoji everywhere:** Apple PNGs from the emoji-datasource-apple set on jsdelivr (160 px, then 64 px),
  cached in `assets/emoji`; the regex covers flags, VS16, skin tones and ZWJ sequences. Why: system emoji looked
  off-brand next to the leaders' posts.
- **Text fits by measuring** (section 1 of references/render-pipeline.md) and long titles that are wider than a
  portrait frame go full width on a blurred backdrop instead of being cropped.
- **Safe zone:** headline and face between about 15% and 65% of the height (the profile grid crops 1080x1920 to 3:4,
  240 px off the top and bottom, and app buttons cover the right and bottom). Known gap: the `uk` video headline sits
  lower than this; a template change to test.

## 8. Video details the builder handles
- Letterbox bars detected and cut, a `pre` filter (delogo), layouts, loudness and the one-run layer outputs:
  references/render-pipeline.md section 3.
- **Speech subtitles, never lyrics.** Whisper word times (16 kHz mono WAV through `hear.py`, faster-whisper
  large-v3-turbo) become an ASS file: a phrase breaks at a pause over 0.3 s, at . ! ? or at a Whisper segment start;
  long phrases split evenly into chunks of up to 4 words; uppercase; Proxima Nova Extrabold 70 px, white, black outline
  6, bottom centre, `MarginV` 560 by default; each line ends at the next start or 0.4 s after its last word; swears
  starred (f*ck, sh*t, b*tch...). Subtitles stop before the song (`subs_until`). Why: the song is the audio, lyrics on
  screen risk misquotes, and word-count chunks cut thoughts in half ("TOO MUCH MAN PEACE").
- **Audio modes:** the clip's own sound by default; `song` (client song from its drop); `mix` (song bed under the clip);
  every render fades the last second and normalises to about -14 LUFS.
- **Length follows the payoff:** 14 to 16 s for headline videos, 23 s for a chorus with 4 hook lines, 30 s for a live
  clip with an arc, 36 s when the payoff needs it. Length is a test variable, judged on skip rate.

## 9. Build, look, deliver
- **Build** writes `FINALS/<batch>/@<page>/NN_slug.mp4|png` (numbered per page in posting order; carousels as a folder
  of `1.png, 2.png...`), a `captions.txt` per page (each file with its caption, `[post <window>]`, the Story still and
  poll, the pin; every version on disk listed and the latest marked), and Premiere layers + `<id>.xml` +
  `<id>_source.xml` in `out/<batch>/premiere/`. A failure prints `FAIL <id>` and the rest still builds.
- **Look** with one contact sheet: every card plus 2 frames per video (at 1 s and at 60%), 216x384 cells, 6 columns,
  skipping files that start with `_` and the overlay and base layers. Check every frame 0 (a face, the right person,
  no Vevo or chart logo, nothing cut off). Fix undelivered drafts in place with `--only`.
- **Deliver to Drive** (Drive for desktop): `<Drive>/<posting folder>/<DD MM YYYY>/<page>/` holding the videos, the
  carousel slides loose as `1.png, 2.png...` (subfolders only when a page has 2+ carousels that day) and
  `captions.txt`; identical files are skipped (byte compare), a changed file is saved as `_v2`, `captions.txt` is
  refreshed in place. Why: the team posts from the Drive phone app, and a share link cannot be written without a
  signed-in account. Copy the user's own folder layout ("see how i sorted for yesterday").
- **Schedule file** `FINALS/SCHEDULE.md`: per built post its page, UK window, type, file and headline, marked POST,
  optional or skip; batches that never went up expire; posts that would be stale ("drops tonight at 7pm" after 7pm) are
  marked do-not-post. Windows come from social-video-formats; note the clock change (BST ends 25 Oct 2026) and the
  offset to the editor's time zone.
- **Hand-over** per batch: a table per page (window, format, source), what was left out and why, which facts were
  checked where, what to watch next, the sheet and the videos attached.

## 10. Review and versions
- Read notes post by post, turn vague notes into concrete changes and say your reading back before rebuilding ("adjust
  font and a few bits" became a readable font plus a bigger clip box).
- "dont make the changes just keep this in mind": change the template defaults, `captions.md` and the playbook, not
  the delivered posts.
- Delivered posts change only as `_v2`, `_v3` (finals, Premiere layers, Story stills); old settings go in `history`.
  Move undelivered drafts to `_superseded` before a rebuild, never delete them.
- Premiere route for a re-cut: import `<id>_source.xml` and slip V1, or give Claude a timestamp (about 20 s, keeps the
  house loudness).

## 11. Not automated, proposed, and open
- Posting stays manual in the app so the client's official sound is attached (API posting may count as "original
  sound": unverified).
- Proposed, not approved: two scans a UK day (morning and late afternoon, because beef and court stories break in the
  evening); a scheduled run; Trial Reels to A/B two openings of the day's best story (only the first 3 s change).
- Open: the team has not yet imported a news-post XML in Premiere; measurement (Insights at 24 h and 72 h, poll
  counts, own medians after 20 posts) has not started; editor minutes and Claude usage per batch were never measured.
- Dated dependencies: fxtwitter is unofficial and can vanish; Reddit RSS ends 13 Nov 2026; Nitter is gone; the
  research behind the playbook dates from 7 to 8 Oct 2026.

## 12. Extending the newsdesk
- **A new format:** a layout block in `card.html` + the format name in `vcn.py` (`CARD_ONLY` / `VIDEO_ONLY` sets and
  any layout branch in `video()`), a row in the README fields table, one test post in a test batch, one sheet.
- **A new page:** an account in `brand.json` (handle, avatar, tweet style, fonts) and its Drive folder name.
- **A new client:** fork the folder (the faceless fork is the example), with its own brand file, batches, finals and
  Drive folder; never edit the original for a client.
- **A new source:** add it to the lean list only if the main pages miss it; give it a row-count alarm.
- **Two scans a day or a timed run:** see references/scheduling-and-unattended-runs.md; keep the human approval of the
  slate.
