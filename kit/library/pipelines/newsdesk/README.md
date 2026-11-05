# vc-news: daily rap / music news posts (built 7 Oct 2026)

**Read `PLAYBOOK.md` first**: what each page is for, the interest test every post must pass, retention rules, growth plan and metrics (research/08 to 10). The tools below only build what the playbook says is worth posting.

Branding in `brand.json` is a PLACEHOLDER (wordmark BEATSWITCH, yellow + red accents) until the page identity is decided.
Formats come from `../research/07-formats.md`; headline and caption rules from `captions.md`.

## Daily run
1. `python scan.py` (about 5 s, lean default): reads the 12 main pages on X (GBMC, GRM, UKHipHopDaily, Link Up, Official Charts, RapTV, Kurrco, Daily Loud, Say Cheese, HNHH, Chart Data, Pop Crave); `out/scan/scan_<time>.md` = UK top and all top artists by coverage, then the trending-potential lists: **Breaking out** (a post doing x times its page's usual views), **Most talked about** (replies + quotes per 1k views = debate), then viral posts. Every post is also in the scan json (`posts`) for filtering. `python scan.py --full` adds 81 feeds, charts, trends and the Wikidata calendar (rarely needed: the main pages already cover it). Detection only: confirm court, violence and "allegedly" stories with press or police before posting. Then a quick Google News sweep (`UK rap when:2d`, `UK rapper when:2d`, a few big UK names): the X pages sometimes skip big announcements (13 Oct 2026: Giggs' Wembley show was only on news sites).
2. Pick 5 to 10 stories. Source assets:
   - `python fetch.py yt <video id> <start s> <dur s> clip.mp4` (official videos, interviews, freestyles; dur 0 = whole video)
   - `python fetch.py peak <video id> 15` = start of the most replayed 15 s (YouTube heatmap). New uploads have none: download the whole video and use `python fetch.py loud clip.mp4 15`
   - Source clips with burned-in titles or captions: start after the title, and skip `subs` if the clip already has captions
   - `python fetch.py thumb <video id> photo.jpg` / `python fetch.py frame clip.mp4 3.5 photo.jpg` (artist photos)
   - `python fetch.py x <x status url> prefix` (photos / clips from an X post)
3. Write `batches/<date>.json` (fields below), headlines and captions per `captions.md`.
4. `python vcn.py build batches/<date>.json` then `python vcn.py sheet <date>` (one image to check everything: `out/<date>/_sheet.png`).
5. `python vcn.py drive <date>` copies the finals to Google Drive (`G:\My Drive\RAP POSTS VISION\<DD MM YYYY>\zonegbp|beatswitch\`: video, carousel slides loose as 1.png, 2.png..., captions.txt), the way the user sorts it; the team posts from the Drive app. Changed files never replace old ones (_v2).
   Post from **`FINALS/<date>/@<page>/`**: only the finished posts, numbered in posting order, plus `captions.txt` (caption per file, with `[post ...]` timing notes). Post in-app with the client's sound attached.
   Premiere: `out/<date>/premiere/<id>.xml` (File > Import: V1 clip layer, V2 template overlay, A1 audio) is the finished cut. To pick a different part of the clip, import `<id>_source.xml` instead: V1 is the whole source video (already scaled like the render), A1 its linked audio, V2 the headline; slip V1 with the Slip tool (Y). Scratch files sit in `out/<date>/_temp`.

Needs: Chrome, Python 3.13 (PyAV, Pillow), ffmpeg 9 + Deno (WinGet), yt-dlp and gallery-dl (pip). ffmpeg is found automatically.

YouTube: every yt-dlp call (`fetch.py search | peak | yt`) runs one at a time, 6 s apart; never fire them in parallel (a burst of ~15 on 8 Oct 2026 got a 15-minute "confirm you're not a bot" block; thumbnails kept working). If blocks come back often: log a THROWAWAY YouTube account into a private browser window, export its cookies with a cookies.txt extension to `secrets/youtube_cookies.txt`, close the window. fetch.py then uses the file automatically (nobody opens or prints it). Never a personal or Jaden's account: Google can flag accounts used by download tools.

## Accounts and emoji
`brand.json` holds our two news accounts: `beatswitchfm` (light tweet card) and `zonegbp` (dark tweet card), with pfps in `assets/accounts/` (cropped from Jaden's list; @stillbenched and @payedxi are the football pages). Set `"account"` per post or once per batch. Every non-tweet post carries the page's pfp + @handle (videos: as a byline over the headline). House fonts can be set per page in brand.json (`"fonts": {"VCHead": "file.otf"}`); cards use condensed VCHead, video headlines use VCBox (Proxima Nova Extrabold). No blue tick (neither is verified). Every emoji renders iPhone-style: PNGs come from the emoji-datasource-apple set on first use and are cached in `assets/emoji/`.

## Post fields
Engagement extras (see captions.md > Engagement): `slides` [{photo, focus, headline}] turns a card into a carousel (`NN_post/1.png` = the card, then one slide per photo with a line of context); `story: true` + `poll: "A / B"` adds `NN_post_story.png`, a 9:16 Story still with room for a poll sticker (vs format); `pin` = our take to pin as the first comment. All three show up in captions.txt.

Common: `id`, `fmt`, `account`, `headline` (`*word*` = accent, `^word^` = red), `caption`, optional `when` (posting-time note for captions.txt), `logo` (platform badge instead of a label: `applemusic`, `spotify`, `shazam`, `youtube`, `tiktok`, `billboard`... any simple-icons name, or a png path), `label` (pill: NEW MUSIC, THROWBACK, HAPPY BIRTHDAY, CHARTS, COURT), `theme` (beef, court, breaking = red; charts, money = green; throwback, birthday = orange; raptv = orange; news = yellow) or `accent` "#hex".

| fmt | Kind | Extra fields |
|---|---|---|
| `uk` | card, or video when `clip` given | `photo`, `focus` ("center 25%"), `inset` {src, size, x, y}, `sub` |
| `raptv` | card | `photo`, `focus`, `badge` ("OCT/26") |
| `meme` | card or video | `photo` or `clip`, `faces` [{src, x, y, size}], `band` (header height) |
| `tweet` | card or video | `photo` or `clip`. Card = tweet screenshot with the photo inside (`ph` = photo height, `photo_bg: true` = old photo-behind look); video = card on top, clip under it |
| `vs` | card | `photos` [{src, focus, name}] x2: VS / this-or-that engagement post (beef polls, "which pair?") |

List cards also take `photo` (blurred background) and `style: "prices"` (label left, big price right: price lists, stats).
| `chart` | card | `chart`, `rank`, `move` ("+3", "-2", "NEW", "="), `title`, `artist`, `stats`, `cover` |
| `list` | card | `title`, `sub`, `items` [{artist, title, cover}] |
| `split` | video | `photos` [{src, focus}] x2, clip shown from y=560 under the caption box |
| `quote` | video | `headline` = exact words, `sub` = speaker |

Paths can be relative to this folder (e.g. `in/1007/clip.mp4`). List items take an optional `rank`.
Video `clip`: {`path`, `in`, `dur`, `fx`/`fy` crop focus 0..1, `fill`: "crop" or "blur", `crop`: letterbox bars are cut automatically (false = off, "w:h:x:y" = manual)}. Tweet videos start the clip under the card; wide clips in `uk` blur mode sit at 40% height above the headline. `audio`: {`mode`: "clip" | "song" | "mix", `song`, `song_in` (start at the beat drop), `bed_db` for mix}. Audio is faded out over the last second and normalised to about -14 LUFS. `subs: true` burns in word captions from local Whisper (for interview clips).
