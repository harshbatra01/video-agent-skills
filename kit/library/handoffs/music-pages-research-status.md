# Research status (saved 7 Oct 2026, before a session pause)

## Done
- Read the handoff pack, the 6 format SOPs, the research and branding docs, the packages PDF, RAP.prproj and renders, the pitch video (transcribed), and the premiere-ae-editing skill (all tests passed).
- Monitoring accounts: X and Instagram are logged in inside the Claude app's built-in browser (tabs x.com and instagram.com). TikTok still needs a VPN from India.

## Running when the session paused (5 research agents)
If a file below is missing on resume, re-run that brief on the Sonnet model (cheaper), same rules: verify every handle/URL live, dates and sources for numbers, flag dead/fake/impersonator/AI, no copyright talk, no em dashes, WebSearch/WebFetch only, full detail in the file, short summary back.

| File | Brief |
|---|---|
| 01-pages-us-global.md | Best US/global rap and music news pages (TikTok, IG, Shorts, X): @rap, Kurrco, Daily Loud, Rap Alert, Say Cheese, No Jumper, HipHopDX, XXL, Complex, HNHH, RapTV, Pop Base/Crave, Shade Room, Genius + new 2025/26 pages. Per page: handles, followers (source+date), frequency, content mix, originator vs aggregator, signature formats, 2-3 example post URLs. Top 25 ranking + 5-10 "format leaders". |
| 02-pages-uk.md | Identify "gbmc" on X (or GRM Daily?). UK rap/drill/grime news pages across X/IG/TikTok/YT: GRM Daily, UK Rap Daily, UKDrillNews_, UK_Drill_News, Link Up, Mixtape Madness, P110, BL@CKBOX, Pressplay, Complex UK, Trench, ukmusicmedia, lyricalmindsuk, itsallukdrill, ukdrill__ + TikTok-native ones. Same fields; two top-20 rankings (models, news sources); who breaks UK stories first. |
| 03-news-feeds.md + .json | Fast sources a script can read: news site RSS (HNHH, HipHopDX, XXL, Complex, Rap-Up, Vibe, Billboard, NME, Clash, GRM site, Link Up site...), YouTube channel RSS with channel_ids (GRM, Pressplay, MM, Link Up, P110, BL@CKBOX, Sloth, 1Xtra, No Jumper, Akademiks, Genius...), Reddit rss/json status, CourtListener API. Test each feed today, newest item date. |
| 04-trend-signals.md + .json | Daily "what's hot" signals, GB then US: Shazam CSV, Apple Music RSS JSON, Spotify charts access, kworb, Official Charts, Billboard, Deezer, Last.fm, YouTube Charts; release detection (Deezer, iTunes, MusicBrainz, Spotify API limits); spikes (Wikipedia pageviews, Google Trends RSS/API, YouTube mostPopular); TikTok Creative Center (India block). Test each, sample value. |
| 05-access-and-tooling.md | X API tiers/pay-per-use + third-party X APIs (prices), RSSHub/Nitter, logged-in browser risks; Instagram Graph Business Discovery + scrapers; TikTok APIs + India/VPN; Reddit API rules; yt-dlp/gallery-dl status per platform; cheapest daily setup + scale-up setup with monthly cost. |

## Results in so far
- 05-access-and-tooling.md DONE. Cheapest daily setup about $24-30/month: twitterapi.io for X Lists (~$5), Apify Starter $19 for Instagram + TikTok (+ Reddit after 13 Nov 2026), YouTube/Reddit RSS free, yt-dlp + gallery-dl downloads. Official X API is now pay-per-use only ($0.005 per post read, ~$40-80/month at our volume). Nitter dead (Sept 2026). Reddit: RSS ends 13 Nov 2026, new API requests close 31 Oct 2026. TikTok blocked on this PC's Airtel line (use Apify). Instagram downloads need cookies from a throwaway account logged in via Firefox. To install: ffmpeg, yt-dlp, gallery-dl, Deno. User must do every signup, login and key (keys in a local .env).
- 04-trend-signals.md + .json DONE (61 entries, 40 verified live). Core free signals: Shazam UK CSVs (incl. hip-hop and discovery, earliest signal), kworb Spotify daily GB/US (~2 days behind), Apple Music most-played JSON (host now rss.marketingtools.apple.com), Official Charts (Fri 4-5:45pm UK), Wikimedia pageviews (spike = 3x 28-day median), Google Trends Trending Now RSS (new URL, 10 items), iTunes Lookup + MusicBrainz + YouTube RSS for releases, YouTube Data API music trending (free key). Dead/locked: YouTube Trending page (gone 21 Jul 2025), old Google Trends RSS, pytrends, Billboard (402 paywall to scripts), Spotify country charts (login) and most of the Spotify API for new apps, TikTok Creative Center (blocked from India; public songs ranking may be gone). Deezer returns empty lists from India and its terms are non-commercial. Score movement (new entries, rank jumps, stream gains), not position. Untested lead: the connected tiktok_music_trending tool. Handoff errors confirmed: Creative Center oversold, Who We Be adds not trackable, HipHopDX calendar loads by JavaScript.
- 01-pages-us-global.md DONE (saved before the spend limit). 03-news-feeds.json DONE (121 entries, 81 verified; the .md was never written). UK: 5 of 6 sub-reports saved in raw/ (the IG/TikTok-native one was lost; main UK agent died before merging).
- **06-shortlist.md = the merged Phase 1 result. Start here.**
- **07-formats.md = format catalog (6 card + 6 video formats, headline grammar, build route, build order). Done 7 Oct.** Tools installed (ffmpeg, Deno, gallery-dl, yt-dlp via python -m yt_dlp).
- **BUILD DONE 7 Oct: C:\VISION\VISION CLAUDE\vc-news** (README.md). vcn.py = cards (uk, raptv, meme, tweet, chart, list) + videos (split, uk, meme, tweet, quote) via headless Chrome templates + ffmpeg, Premiere XML per video; scan.py = daily digest (81 feeds, 17 X accounts via fxtwitter, Shazam/Apple GB, Google Trends, Wikidata calendar cache); fetch.py = YouTube sections, thumbnails, frames, X media. All formats tested (out/test_formats). Placeholder brand.
- Open: Wikidata rate-limited during an outage (calendar fills itself later); Premiere XML import not yet tested (try during the first real batch); subs (Whisper captions) untested until an interview clip comes up.
- Next: the user will ask for a test batch (scan, pick stories, fetch assets, write batch JSON, build, sheet).

## Next steps
1. Merge the 5 reports into one shortlist: pages to model, the source stack, the access setup.
2. Formats phase: browse the top pages' posts in the built-in browser (logged in), one small contact sheet per page, catalogue every format (video layouts, tweet cards, photo cards, carousels) with exact layouts.
3. Build: daily scan, pick stories, source assets, fill format templates (Premiere via prproj_lib, Photoshop/AE for cards), human posts in-app with the client's sound.
4. Later: a distinct page identity.
