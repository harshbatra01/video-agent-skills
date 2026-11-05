# 04 Trend signals: free and cheap machine-readable sources

Tested live on Wednesday 7 October 2026, roughly 14:00 to 15:30 UTC, with WebFetch and WebSearch only (no browser, no logins, no media downloads). Machine-readable twin of this file: `04-trend-signals.json`.

How to read this:

- **Verified** means the URL was fetched today and returned real, current data. The sample value is what came back.
- **UNVERIFIED** means it could not be tested today (needs a key, a login, a different country, or the fetch was blocked). Claims about those come from the cited docs or third parties.
- Sample values were read through WebFetch's text extraction. Where possible they were cross-checked (for example Taylor Swift "Patient Zero" is UK number 1 on Official Charts, Apple Music UK and kworb at the same time).

## 0. Key findings

1. **Where the script runs matters.** These tests ran from the user's machine in India. Deezer's own `/infos` endpoint answered `"country_iso": "IN"`, `"open": false`, and every Deezer chart, editorial and artist-albums call came back as `{"data":[],"total":0}` with no error. `www.tiktok.com` and `ads.tiktok.com` refused the connection outright (`ECONNREFUSED 202.56.230.30:443` and `ECONNREFUSED 13.127.247.216:443`). India has blocked TikTok since 29 June 2020 ([Wikipedia: Restrictions on TikTok](https://en.wikipedia.org/wiki/Restrictions_on_TikTok)). **Run the daily job on a UK or US server**, and treat an empty array as an error, not as "nothing is trending".
2. **Best free stack that works today, no key:** Shazam CSVs (UK top 200, UK Hip-Hop/Rap, UK Discovery, UK cities), Apple Music most-played JSON, kworb (Spotify daily per country with stream counts, plus Apple, iTunes, YouTube mirrors), Official Charts HTML (Singles, Albums, Hip Hop and R&B, Afrobeats, Trending), Wikimedia pageviews, Google Trends Trending Now RSS, iTunes Lookup, MusicBrainz, YouTube channel RSS.
3. **Locked or paywalled:** Billboard (bot traffic is redirected to a TollBit paywall that returns HTTP 402), Spotify regional charts (login), Spotify Web API (Premium-owned dev apps only, new-releases and artist top-tracks removed for dev mode in February 2026), TikTok Creative Center (blocked here, songs ranking reportedly removed in a 2026 redesign), Last.fm (free key, but commercial use needs an agreement), YouTube Data API (free key needed).
4. **Dead:** old Google Trends daily RSS (404), pytrends (GitHub repo archived 17 Apr 2025), the YouTube Trending page (removed 21 Jul 2025), Tokboard (domain no longer resolves), `assets.billboard.com` (expired certificate). `rss.applemarketingtools.com` still works but now 301-redirects to `rss.marketingtools.apple.com`.
5. **Corrections to the earlier handoff** (`vision-clipping-handoff/handoff/data/monitoring-sources.json`):
   - "TikTok Creative Center ... Free and works without logging in. The single most useful free tool": it is unreachable from India, and at least one 2026 source says the public songs ranking is gone (see section 4).
   - "Spotify Who We Be ... An add is a genuine postable news event": a new Spotify API app cannot read Spotify-owned editorial playlists since 27 Nov 2024 ([Spotify blog](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api)), so adds cannot be detected by script.
   - "HipHopDX release dates ... The best single answer": the list loads by JavaScript, so a plain fetch only sees "Loading releases...".

## 1. Charts

GB first, then US. "Rolling 7 days" means each daily file covers the past 7 days.

| Source | Region | URL pattern | Auth / cost | Verified 7 Oct | Sample value today | Notes |
|---|---|---|---|---|---|---|
| Shazam Top 200 CSV | world, GB, US, many more | `https://www.shazam.com/services/charts/csv/top-200/{world\|united-kingdom\|united-states}` | none, free | Yes | GB #1 PVT "Kangaroo"; world #1 Imael Angel "BAD TIMES"; US #1 KAROL G, Judeline & rusowsky "BbY WOW" | First line is a date header: "Wednesday, 7 October 2026 [performance over the past 7 days]". Columns Rank, Artist, Title. Ranks only, no Shazam counts. |
| Shazam Hip-Hop/Rap CSV | GB, US, world | `https://www.shazam.com/services/charts/csv/genre/{country-slug}/hip-hop-rap` | none, free | Yes | GB #1 Dave & Tems "Raindance", #2 Skepta, Suggs & Chase & Status "Innocent Smile"; US #2 Belly Gang Kushington & 21 Savage "WTF GOIN" | UK genres offered: Dance, Hip-Hop/Rap, Pop. The UK list also held a Russian-language track at #6, so do not assume every row is a UK act. |
| Shazam Discovery CSV | GB | `https://www.shazam.com/services/charts/csv/discovery/united-kingdom` | none, free | Yes | GB #1 Wxoda "Vibin", #3 Skepta, Suggs & Chase & Status "Innocent Smile" | Emerging tracks. Best free early-warning list found. |
| Shazam Viral CSV | GB | `https://www.shazam.com/services/charts/csv/viral/united-kingdom` | none, free | Yes | GB #1 PVT "Kangaroo", #3 Van Morrison "Bulbs" | Different order from the top 200. |
| Shazam city CSV | 15 UK cities | `https://www.shazam.com/services/charts/csv/top-50/united-kingdom/{city}` | none, free | Yes (London) | London #1 PVT "Kangaroo" | Cities listed on the UK page: Belfast, Birmingham, Brighton, Bristol, Cardiff, Edinburgh, Glasgow, Leeds, Liverpool, London, Manchester, Newcastle upon Tyne, Nottingham, Portsmouth, Sheffield. |
| Apple Music most-played songs JSON | GB, US, per storefront | `https://rss.marketingtools.apple.com/api/v2/{gb\|us}/music/most-played/{10\|25\|50\|100}/songs.json` | none, free | Yes | GB #1 Taylor Swift "Patient Zero"; US #1 Drake & Don Toliver "Solar Eclipse" (released 2026-10-02) | Feed "updated: Wed, 7 Oct 2026 14:21:16 +0000". Each item has `genres` and `releaseDate`, which helps the rap filter and the "new" flag. Old host `rss.applemarketingtools.com` returns 301 to this one. |
| Apple Music most-played albums JSON | GB, US | `.../most-played/25/albums.json` | none, free | Yes at limit 25 | GB #1 Taylor Swift "The Life of a Showgirl: The Encore", #2 Drake "HABIBTI (FOMO)" (2026-10-02) | Limit 50 and 100 returned HTTP 504 twice today (GB and US); limit 25 worked. Add retries. |
| iTunes Store legacy RSS, genre filter | GB, US | `https://itunes.apple.com/{gb\|us}/rss/{topsongs\|topalbums}/limit={n}/genre=18/json` | none, free | Yes | GB Hip-Hop/Rap songs #1 Raven Astrid "O Mighty Sea, Carry Me", #2 Dave & Tems "Raindance"; GB albums #1 Karan Aujla "AUJLA SZN 1 - EP"; US songs #1 Downey "Blink" | Genre 18 = Hip-Hop/Rap. Download sales only, small volumes, noisy. Useful for "NEW" entries on release day. |
| Spotify Charts public endpoint | global only | `https://charts-spotify-com-service.spotify.com/public/v0/charts` | none, free | Yes | Weekly Top Songs Global #1 Taylor Swift "Patient Zero" (2026-10-01) | Returns 3 charts only: global weekly songs, albums, artists, with current, previous and peak rank. |
| Spotify Charts regional (charts.spotify.com) | GB, US, cities, Viral | `https://charts-spotify-com-service.spotify.com/auth/v0/charts/regional-gb-daily/latest` | login (Spotify account) | UNVERIFIED | HTTP 401 without a token | Landing page says "Log in to access all our global charts". Whether a CSV download exists after login could not be checked (no logins allowed). |
| kworb Spotify daily per country | GB, US, 70+ | `https://kworb.net/spotify/country/{gb\|us}_daily.html` (also `_weekly`, `_daily_totals`) | none, free | Yes | GB chart dated 2026/10/05: #1 Sam Fender "Rein Me In (w/ Olivia Dean)" 295,990 streams (+10,506); #2 Ashe "Stop The Wedding!" (+40,456). US #1 Taylor Swift "Patient Zero" 1,208,069 | Only free per-country Spotify source found. Columns include daily and 7-day stream changes. Lag about 2 days (5 Oct chart on the afternoon of 7 Oct). Static HTML, no API. |
| kworb Apple Music per country | GB, US, 100+ | `https://kworb.net/charts/apple_s/{uk\|us}.html` | none, free | Yes | UK #1 Taylor Swift "Patient Zero" (10:02 EDT) | Note `uk`, not `gb`. Positions and moves only. |
| kworb iTunes per country | GB, US | `https://kworb.net/charts/itunes/{uk\|us}.html` | none, free | Yes | UK #1 HUGEL, Imael Angel & Ultra Naté "Movin' To The Sun"; #4 NEW Royal Blood "Dead Company" | kworb FAQ: iTunes data from Apple's feed, updated every couple of minutes ([FAQ](https://kworb.net/faq.html)). |
| kworb YouTube daily per country | GB, US | `https://kworb.net/youtube/insights/{uk\|us}_daily.html` | none, free | Yes | UK chart dated 2026/10/01: #1 Taylor Swift "Patient Zero" 420,981 streams | About 6 days behind today. |
| kworb Shazam and Deezer mirrors | GB, US, many | `https://kworb.net/charts/shazam/uk.html`, `https://kworb.net/charts/deezer/uk.html` | none, free | Yes (index page) | UK Shazam #1 PVT "Kangaroo"; UK Deezer #1 Ella Langley "Choosin' Texas" | Index of every country and platform: `https://kworb.net/charts/`. |
| kworb US radio (Mediabase via All Access) | US | `https://kworb.net/radio/` | none, free | Yes | #1 Tame Impala "Dracula - JENNIE Remix" (7 Oct) | US only. |
| Official Singles Chart | GB | `https://www.officialcharts.com/charts/singles-chart/` | none, free (HTML) | Yes | Week 2 to 8 Oct 2026: #1 Taylor Swift "Patient Zero" (new) | Chart week runs Friday to Thursday; main charts unveiled Friday 4pm to 5:45pm UK; BBC Radio 1 "First Look" Sunday 6pm to 7pm ([OCC](https://www.officialcharts.com/who-we-are/our-charts-and-data/)). Raw data is B2B subscription only. |
| Official Albums Chart | GB | `https://www.officialcharts.com/charts/albums-chart/` | none, free | Yes | #1 Taylor Swift "The Life of a Showgirl" (last week 84), #2 Keo "Put a Smile On For Me" (new) | |
| Official Hip Hop and R&B Singles | GB | `https://www.officialcharts.com/charts/official-hip-hop-and-r-and-b-singles-chart/` | none, free | Yes | #1 Dave/Tems "Raindance" (49 weeks), #5 Drake "Janice STFU" | Albums version: `/charts/official-hip-hop-and-r-and-b-albums-chart/` (not fetched). The slug `/charts/r-and-b-singles-chart/` is only a loading shell. |
| Official Afrobeats Chart | GB | `https://www.officialcharts.com/charts/afrobeats-chart/` | none, free | Yes | Week 4 to 10 Oct: #1 Victony "Slick" | |
| Official Singles Chart Update | GB | `https://www.officialcharts.com/charts/singles-chart-update/` | none, free | Yes | #1 "Patient Zero", #3 Jamie Miller "Babydoll" | Midweek view; page labelled 5 to 11 Oct 2026. |
| Official Trending Chart | GB | news article: `https://www.officialcharts.com/chart-news/trending-songs-uk-{month}-{day}-{year}/` | none, free | Yes | 6 Oct 2026: #1 Noah Kahan "Draw You Out", #2 Drake ft. Don Toliver "Solar Eclipse", #16 Morrisson "COS OF YOU" | Top 20 of songs growing week on week, from the first four sales days (Friday to Monday), max two per artist. Articles seen dated Tuesdays. |
| Official Charts archive by date | GB | `https://www.officialcharts.com/charts/{slug}/{YYYYMMDD}/{chart-id}/` | none, free | Seen in search results, not fetched | e.g. `/charts/rock-and-metal-singles-chart/20261002/111/` | Lets the script read last week's chart for history. |
| Billboard Hot 100 and Hot Rap Songs | US | `https://www.billboard.com/charts/hot-100/`, `https://www.billboard.com/charts/rap-song/` | blocked for bots | UNVERIFIED | Our fetch got 307 to `tollbit.billboard.com`, then HTTP 402 Payment Required | Hot 100 is released online on Tuesdays ([Wikipedia](https://en.wikipedia.org/wiki/Billboard_Hot_100)). Not tested with a normal browser user agent. `assets.billboard.com` has an expired certificate. |
| Billboard Hot 100 via Official Charts mirror | US | `https://www.officialcharts.com/charts/billboard-hot-100-chart/` (also `/charts/billboard-200/`) | none, free | Yes | Week 30 Sep to 6 Oct 2026: #1 Ella Langley "Choosin' Texas", #2 Stella Lefty "Boston" | Free route to the Hot 100. No Hot Rap Songs mirror found. |
| Deezer chart API | IP-based country | `https://api.deezer.com/chart/{0\|116}/tracks` | none, free | UNVERIFIED (empty from India) | `{"data":[],"total":0}` | No country parameter: the chart follows the caller's IP. Editorial ids include 0 All, 116 Rap/Hip Hop, 165 R&B. Deezer API terms: use "strictly limited for a non-commercial purpose" ([terms](https://developers.deezer.com/termsofuse)). |
| Deezer chart playlists | GB, US | `https://api.deezer.com/playlist/1111142221` (Top UK), `https://api.deezer.com/playlist/1313621735` (Top USA) | none, free | Yes | Top UK #1 Ella Langley "Choosin' Texas" (modified 7 Oct 14:54); Top USA #1 Stella Lefty "Boston" | Works even from India. Deezer's UK audience is small, so weight it low. |
| Last.fm geo.getTopTracks | GB, US | `https://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=united%20kingdom&api_key={KEY}&format=json` | key (free) | UNVERIFIED | HTTP 400 without a key | `api_key` is required, no user auth ([docs](https://www.last.fm/api/show/geo.getTopTracks)). Commercial use without a commercial agreement is "a material breach" ([ToS](https://www.last.fm/api/tos)). |
| YouTube Charts site | GB, US | `https://charts.youtube.com/charts/TrendingVideos/gb/RightNow` | none | UNVERIFIED | HTML is a JavaScript shell, no chart data | Use kworb's YouTube pages or the YouTube Data API instead (section 3). |

## 2. New release detection (artist watchlist)

| Source | Region | URL pattern | Auth / cost | Verified 7 Oct | Sample value today | Notes |
|---|---|---|---|---|---|---|
| iTunes Search (resolve artist id) | GB, US | `https://itunes.apple.com/search?term={name}&entity=musicArtist&country=gb` | none, free | Yes | Central Cee = artistId 1085149646, Hip-Hop/Rap | Store the id once per artist. |
| iTunes Lookup (latest releases) | GB, US | `https://itunes.apple.com/lookup?id={artistId}&entity=album&sort=recent&limit=20&country=gb` (also `entity=song`) | none, free | Yes | Central Cee newest: "The Team - Single" (2026-08-18) | Results are NOT reliably newest first despite `sort=recent`: sort by `releaseDate` yourself. Apple: "limited to approximately 20 calls per minute" ([docs](https://performance-partners.apple.com/search-api)). |
| MusicBrainz release groups | global | `https://musicbrainz.org/ws/2/release-group?artist={MBID}&fmt=json&limit=100` | none, free | Yes | Central Cee MBID b0337af1-8d93-4671-b6c9-ba306bf942bf, 58 release groups, newest "The Team" (Single, 2026-08-18) | 1 request per second on average per IP, and a User-Agent with contact details is required, or you get 503 ([rate limiting](https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting)). |
| MusicBrainz releases by date | GB | `https://musicbrainz.org/ws/2/release?query=date:2026-10-02%20AND%20country:GB&fmt=json` | none, free | Yes | 61 GB releases dated 2026-10-02 (first: Would-Be-Goods "Tears Before Bedtime") | Community-entered, skewed to indie, rock and reissues. Weak for UK rap. |
| YouTube channel uploads RSS | any channel | `https://www.youtube.com/feeds/videos.xml?channel_id={UC...}` | none, free | Yes (tested on YouTube's own channel) | 16 entries, newest published 2026-10-06T21:00:32Z | Good free "new video" detector for GRM Daily, Link Up TV, Mixtape Madness, Pressplay and artist channels. Needs the UC channel id: resolve once with `channels.list?forHandle=@handle` (1 quota unit, [docs](https://developers.google.com/youtube/v3/docs/channels/list)). The old `?user=grmdaily` form returned 404. |
| Wikipedia "2026 in hip-hop" via MediaWiki API | mostly US | `https://en.wikipedia.org/w/api.php?action=parse&page=2026_in_hip-hop&prop=wikitext&section={n}&format=json` | none, free | Yes | Released albums, 2 Oct 2026: Quavo "Qrömelife", Quadeca "Life 1", NoCap "Heaven on Mars" | Sections: "Released albums" by month (October = section 23 today), "Upcoming releases", "Events". List sections first with `prop=sections`, the index moves as the page grows. |
| HotNewHipHop monthly list | US | e.g. `https://www.hotnewhiphop.com/1011309-hip-hop-albums-dropping-october-2026` | none, free | Yes | 23 Oct: Anderson .Paak & Cordae "Heavy Is The Crown" | Article published 29 Sep 2026, says the list is tentative. HTML, needs an LLM or parser. |
| HipHopDX release dates | US | `https://hiphopdx.com/release-dates` | none | UNVERIFIED | Page shell shows "Loading releases..." | Data is loaded by JavaScript; no endpoint confirmed. |
| Deezer artist albums | IP-based | `https://api.deezer.com/artist/{id}/albums` | none, free | UNVERIFIED (empty from India) | Artist search works (Central Cee id 12096038, 668,395 fans); albums list empty here | Re-test from a UK or US server. Non-commercial terms. |
| Deezer editorial releases | IP-based | `https://api.deezer.com/editorial/{0\|116}/releases` | none, free | UNVERIFIED (empty from India) | `{"data":[],"total":0}` | 116 = Rap/Hip Hop. |
| Spotify Web API artist albums | global | `GET https://api.spotify.com/v1/artists/{id}/albums` | oauth (client credentials), app owner must have Premium | UNVERIFIED | not tested (no app) | Still documented, max `limit` now 10 ([reference](https://developer.spotify.com/documentation/web-api/reference/get-an-artists-albums)). |
| Spotify Web API new releases, top tracks | global | `GET /browse/new-releases`, `GET /artists/{id}/top-tracks` | oauth | Removed for dev mode | n/a | Removed for Development Mode apps from 11 Feb 2026 (new) and 9 Mar 2026 (existing), along with batch `GET /tracks`, `/albums`, `/artists`, the `popularity` and `followers` fields, and search `limit` cut to max 10 ([migration guide](https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide)). Dev mode needs Premium, 5 users per app; Client ID limit raised to 25 and quota counted per developer account from 23 Jul 2026 ([blog](https://developer.spotify.com/blog/2026-07-23-web-api-quota-updates)). Since 27 Nov 2024 new apps also lost related artists, recommendations, audio features, featured and category playlists, and Spotify-owned editorial playlists ([blog](https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api)). Extended quota needs an established business and at least 250k MAU ([quota modes](https://developer.spotify.com/documentation/web-api/concepts/quota-modes), [criteria](https://developer.spotify.com/blog/2025-04-15-updating-the-criteria-for-web-api-extended-access)). |

## 3. Attention spikes

| Source | Region | URL pattern | Auth / cost | Verified 7 Oct | Sample value today | Notes |
|---|---|---|---|---|---|---|
| Wikimedia pageviews, per article daily | any language wiki | `https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/en.wikipedia/all-access/user/{Article}/daily/{YYYYMMDD}/{YYYYMMDD}` | none, free | Yes | Dave_(rapper): 884 views on 29 Sep, 887 on 6 Oct (flat, no spike) | Yesterday's data is available today. Send a descriptive User-Agent: compliant bots get 200 requests per minute, unidentified clients 10 per minute ([rate limits](https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits), [access policy](https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/access-policy.html)). |
| Wikimedia top articles per day | en.wikipedia | `https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access/{YYYY}/{MM}/{DD}` | none, free | Yes | 6 Oct 2026: #4 Steve_Gleason 515,772, #11 Freddie_Jackson 167,925 | Global English audience. |
| Wikimedia top per country | GB, US | `https://wikimedia.org/api/rest_v1/metrics/pageviews/top-per-country/GB/all-access/{YYYY}/{MM}/{DD}` | none, free | Yes | GB 6 Oct: #2 Jeffrey_Archer 163,700, #4 Harry_Kane 55,800 | Views are rounded (`views_ceil`). Covers all Wikimedia projects. |
| Google Trends Trending Now RSS | GB, US | `https://trends.google.com/trending/rss?geo={GB\|US}` | none, free | Yes | GB "state pension" 10000+, "the social reckoning" 1000+; US "why is the stock market down today" 5000+ | Only 10 items per feed, each with approx traffic and news headlines. Not music-specific: match against the watchlist. The old `https://trends.google.com/trends/trendingsearches/daily/rss?geo=GB` returns 404. |
| Google Trends API (official) | per country and region | apply at `https://developers.google.com/search/apis/trends` | application only | UNVERIFIED | n/a | Still alpha today; the page says "we're now accepting applications for alpha testers". 5-year rolling window, daily to yearly, country and sub-region ([blog Jul 2025](https://developers.google.com/search/blog/2025/07/trends-api)). |
| pytrends | n/a | `https://github.com/GeneralMills/pytrends` | n/a | DEAD | Archived by the owner on 17 Apr 2025; last PyPI release 4.9.2 (13 Apr 2023) | Do not build on it. |
| YouTube Data API v3 videos.list mostPopular | GB, US, per region | `https://www.googleapis.com/youtube/v3/videos?part=snippet,statistics&chart=mostPopular&regionCode=GB&videoCategoryId=10&maxResults=50&key={KEY}` | key (free Google Cloud project) | UNVERIFIED (HTTP 403 without a key) | n/a | 1 quota unit per call; `maxResults` up to 50 ([videos.list](https://developers.google.com/youtube/v3/docs/videos/list)). Default quota: 100 `search.list` calls, 100 `videos.insert` calls and 10,000 units per day for everything else ([getting started](https://developers.google.com/youtube/v3/getting-started)). Since 21 Jul 2025 `mostPopular` returns videos from the Trending Music, Movies and Gaming charts instead of the old Trending list ([revision history](https://developers.google.com/youtube/v3/revision_history)). New 3 Jun 2026: `videos.batchGetStats`, 1 unit in its own bucket, handy for daily view velocity. |
| kworb YouTube trending music (worldwide) | global with per-country ranks | `https://kworb.net/youtube/trending.html` | none, free | Yes | Updated 2026-10-07 10:10 EDT; #2 Conep, YOVNGCHIMI, DJ Luian "Kirby (Official Video)" (#4 US) | Each row lists the video's position per country, so filter rows mentioning United Kingdom. |
| kworb YouTube 24h views, Anglophone | global | `https://kworb.net/youtube/realtime_anglo.html` | none, free | Yes | #1 "Golden" Official Lyric Video (KPop Demon Hunters), 1,857,644 views in 24h | Dominated by catalogue hits: only score videos uploaded in the last 14 days. |
| Reddit (r/hiphopheads, r/ukdrill) | global, UK | `https://www.reddit.com/r/hiphopheads/new.json` | oauth for API use | UNVERIFIED | WebFetch is not allowed to fetch reddit.com | Third parties report 100 queries per minute with OAuth, 10 without, and no commercial use on the free tier ([octolens](https://octolens.com/blog/reddit-api-pricing)). Not confirmed against Reddit's own terms today. |

## 4. TikTok sounds and hashtags

| Source | Region | URL pattern | Auth / cost | Verified 7 Oct | Sample value today | Notes |
|---|---|---|---|---|---|---|
| TikTok Creative Center (web) | reportedly 27 countries for hashtags | `https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en`; reported new canonical path `ads.tiktok.com/creative/creativeCenter` ([novoads, 19 Jul 2026](https://novoads.ai/en/blog/tiktok-creative-center)) | none for browsing (reported) | UNVERIFIED | `ECONNREFUSED 13.127.247.216:443` from India | Reports conflict. An Apify actor built for the 2026 "TikTok One Creative Suite" redesign says "no longer publishes a public songs ranking; the old Songs page now redirects to hashtags", the Creator tab says "Coming soon", and what remains is hashtags (27 countries), videos (5 countries: US, JP, ID, TH, VN) and top ads ([Apify](https://apify.com/symphonic_mullite/tiktok-creative-center-trends)). Novoads (Jul 2026) says hashtags are now "ranked lists by industry" and trends analytics need an account. Older guides still describe a Songs tab ([Creatify](https://creatify.ai/blog/tiktok-creative-center), [Birch, Oct 2025](https://bir.ch/blog/tiktok-creative-center)). Check by hand from a UK connection before relying on it. |
| Creative Center internal JSON | as above | `https://ads.tiktok.com/creative_radar_api/v1/popular_trend/sound/rank_list?period=7&page=1&limit=20&country_code=GB` | signed headers | UNVERIFIED | `ECONNREFUSED` from India | Scrapers describe minting the required signed headers in-process ([Apify datapeak](https://apify.com/datapeak/tiktok-creative-center)). Fragile; may not serve songs at all after the redesign. |
| Apify Creative Center scraper | 27 countries (hashtags) | Apify actor `symphonic_mullite/tiktok-creative-center-trends` | Apify account, pay per item | UNVERIFIED (not run) | n/a | $0.003 per trend item ($3 per 1,000), "no TikTok login, no cookies and no API key". Runs on Apify's servers, so the India block does not apply. |
| Tokchart global | global | `https://tokchart.com/` | none, free | Yes | #1 "sauti asilia - deefleek1" by MR FLEEK (score 981, 665K videos); #3 girl in red "we fell in love in october" (1,862,681 videos) | Free page is global only, no country selector. `https://tokchart.com/dashboard/music/GB` shows a login form. |
| Tokchart plans and API | GB, US, many | `https://tokchart.com/pricing`, `https://tokchart.com/api` | paid | Yes (pricing page) | Pro $14.99/mo, Business $59/mo, Discovery $149/mo; Music Trends API "From $99/mo", Audio UGC API custom | API endpoints listed: `GET /api/v1/trending/global`, `GET /api/v1/tiktok/audio/trending/global`. Rate limits not stated. |
| Soundcharts | many | `https://soundcharts.com/pricing` | paid | Yes (pricing page) | PRO $129/mo includes "TikTok charts" and "API Access"; API plan from $50/mo, 10k queries/month | |
| Chartmetric | many | `https://chartmetric.com/pricing` | paid | Yes (pricing page) | Manager $40/mo, Premium $117/mo, Ultra $150/mo (billed yearly) | Page does not say which plans include TikTok charts or API. |
| Songstats | many | `https://songstats.com/pricing` | paid | UNVERIFIED | pricing table did not render | |
| Tokboard | n/a | `https://tokboard.com/` | n/a | DEAD | `getaddrinfo ENOTFOUND tokboard.com` | Domain no longer resolves. |
| Free proxies for TikTok virality | GB | Shazam Discovery and Viral CSVs, Official Trending Chart, Tokchart global | none | Yes | see sections 1 and 4 | Inference, not a TikTok measure: sounds that blow up on TikTok usually show up as Shazam and download spikes first. |

Lead to check later (outside this brief, not tested): this Claude setup has a connector exposing a tool named `tiktok_music_trending`. Worth testing as a TikTok sound source.

## 5. Is YouTube's Trending page still there?

No. YouTube announced on 10 to 11 July 2025 that the Trending page was going away ([9to5Google](https://9to5google.com/2025/07/10/youtube-trending-page-removal/)); the API docs date the switch to 21 July 2025 ([revision history](https://developers.google.com/youtube/v3/revision_history)). The help article now points to YouTube Charts: "you can find trending charts for selected content categories like trending film trailers and trending music videos, as well as for trending gaming videos via the Gaming Explore page", updated roughly every 30 minutes and the same for everyone in a country ([YouTube Help](https://support.google.com/youtube/answer/7239739?hl=en-GB)). 9to5Google also lists Weekly Top Podcast Shows. For a script: `charts.youtube.com` is a JavaScript app, so use the Data API `mostPopular` with `videoCategoryId=10` (now fed by the Trending Music chart), or kworb's YouTube pages.

## 6. Dead, locked or unverified at a glance

| Item | Status today | Evidence |
|---|---|---|
| Google Trends old daily RSS | Dead | HTTP 404 |
| pytrends | Dead | GitHub archived 17 Apr 2025 |
| YouTube Trending page | Dead | Removed 21 Jul 2025 |
| Tokboard | Dead | DNS does not resolve |
| assets.billboard.com | Dead | "certificate has expired" |
| Billboard charts for scripts | Locked | 307 to tollbit.billboard.com, then HTTP 402 |
| Spotify regional/daily/viral charts | Locked | HTTP 401; page asks to "Log in with Spotify" |
| Spotify Web API new releases, top tracks, popularity | Locked for dev mode | Feb 2026 migration guide |
| Spotify editorial playlists via API | Locked for new apps | Nov 2024 blog |
| TikTok Creative Center | Blocked from India, songs reportedly removed | ECONNREFUSED; Apify note |
| Tokchart country charts | Login / paid | Login form on `/dashboard/music/GB` |
| Deezer chart, editorial, artist albums | Empty from India | `/infos`: `"country_iso":"IN","open":false` |
| Last.fm geo charts | Needs free key; commercial agreement for business use | HTTP 400 without key; ToS |
| YouTube Data API | Needs free key | HTTP 403 without key |
| Google Trends API | Alpha, by application | Official page |
| HipHopDX calendar | Not script-readable | "Loading releases..." |
| Reddit, Genius | Not testable here | WebFetch refused both domains |

## 7. Building a daily "what's hot" score

Suggested design (a starting point to tune, not a tested model):

1. **Run location and timing.** Run on a UK or US server. Good daily slot: around 15:00 UK, after Apple's feed refresh (seen at 14:21 UTC) and Google Trends' morning items. Add weekly jobs: Official Charts Friday after 17:45 UK, Official Trending Chart article on Tuesday, Billboard Hot 100 (via the Official Charts mirror) from Tuesday.
2. **Track key.** Normalise "artist - title": lowercase, strip "feat./ft./with", brackets like "(w/ Olivia Dean)" or "[Mixed]", and accents (Nate vs Naté). Join every chart on that key.
3. **Chart points.** For each source s with N rows: `points_s = (N - rank + 1) / N`. Suggested weights: Spotify via kworb 1.0, Apple Music 1.0, Shazam top 200 0.8, YouTube via kworb 0.7, Official Charts 1.0 (weekly), iTunes 0.3, Deezer playlist 0.2. UK sources count 1.0, US 0.6.
4. **Momentum.** Add a term for rising: kworb `Streams+` and `7Day+` as a percentage, rank change (`P+`), `NEW` flags, presence on Shazam Discovery or Viral, and low "days on chart" with a high rank.
5. **Rap filter.** A track counts as rap if Apple `genres` contains Hip-Hop/Rap, or it is on the Shazam hip-hop-rap CSV, the iTunes genre 18 feed or the Official Hip Hop and R&B chart, or the artist is on the watchlist.
6. **Artist spikes.** Wikipedia views yesterday divided by the median of the previous 28 days; flag at 3x or more and at least 1,000 views (thresholds to tune). Also flag when a Google Trends RSS item matches an artist name.
7. **Release flag.** New item in the last 7 days from iTunes Lookup, MusicBrainz, YouTube channel RSS or the Wikipedia release table.
8. **Score.** `hot = 0.45 * chart + 0.25 * momentum + 0.20 * spike + 0.10 * release` (each scaled 0 to 1), then hand the top 20 with their reasons to the AI agent to pick stories.

Insights from today's data:

- **Empty is not zero.** Geo-IP silently empties Deezer and blocks TikTok from India without an error. Every source needs a "got fewer than N rows" alarm.
- **Momentum beats position.** The tops of today's lists are long-runners: Sam Fender "Rein Me In" has 473 days on Spotify UK and Olivia Dean "Man I Need" 417. A raw rank score will keep picking old songs; deltas and NEW flags find the stories.
- **Leading vs lagging.** Shazam Discovery (Wxoda "Vibin" at #1) and Tokchart lead; Spotify and Apple daily confirm; Official Charts (Friday) and Billboard (Tuesday) lag. Use leads for "about to blow" posts and the weekly charts for scheduled chart-news slots.
- **Song hot vs artist in the news.** Charts never show arrests, beef, deaths or tour news. Wikipedia spikes and Google Trends matches catch those; pairing them with the release flag tells the agent which kind of story it is.
- **Licence check for a business.** Deezer's API terms are non-commercial and Last.fm needs a commercial agreement. Apple RSS, Shazam CSV, Official Charts pages, Wikimedia and YouTube are the safer core for a commercial page. Scraped HTML (kworb, Official Charts, Tokchart) has no official API: use it for internal ranking and do not republish whole tables.

## 8. Sources

- Shazam UK charts page: https://www.shazam.com/charts/top-200/united-kingdom
- Apple Marketing Tools RSS generator: https://rss.marketingtools.apple.com/
- iTunes Search API docs: https://performance-partners.apple.com/search-api
- Spotify Charts landing page: https://charts.spotify.com/home
- Spotify Web API changes Nov 2024: https://developer.spotify.com/blog/2024-11-27-changes-to-the-web-api
- Spotify extended access criteria Apr 2025: https://developer.spotify.com/blog/2025-04-15-updating-the-criteria-for-web-api-extended-access
- Spotify developer access update Feb 2026: https://developer.spotify.com/blog/2026-02-06-update-on-developer-access-and-platform-security
- Spotify Feb 2026 migration guide: https://developer.spotify.com/documentation/web-api/tutorials/february-2026-migration-guide
- Spotify quota update Jul 2026: https://developer.spotify.com/blog/2026-07-23-web-api-quota-updates
- Spotify Get Artist's Albums: https://developer.spotify.com/documentation/web-api/reference/get-an-artists-albums
- Spotify Get New Releases (marked deprecated): https://developer.spotify.com/documentation/web-api/reference/get-new-releases
- kworb FAQ: https://kworb.net/faq.html
- kworb chart index: https://kworb.net/charts/
- Official Charts list: https://www.officialcharts.com/charts/
- Official Charts timing: https://www.officialcharts.com/who-we-are/our-charts-and-data/
- Official Trending Chart 6 Oct 2026: https://www.officialcharts.com/chart-news/trending-songs-uk-october-6-2026/
- Billboard Hot 100 schedule: https://en.wikipedia.org/wiki/Billboard_Hot_100
- Deezer API terms: https://developers.deezer.com/termsofuse
- Last.fm geo.getTopTracks: https://www.last.fm/api/show/geo.getTopTracks
- Last.fm API terms: https://www.last.fm/api/tos
- MusicBrainz rate limiting: https://musicbrainz.org/doc/MusicBrainz_API/Rate_Limiting
- Wikimedia API rate limits: https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits
- Wikimedia Analytics API access policy: https://doc.wikimedia.org/generated-data-platform/aqs/analytics-api/documentation/access-policy.html
- Google Trends API page: https://developers.google.com/search/apis/trends
- Google Trends API announcement: https://developers.google.com/search/blog/2025/07/trends-api
- pytrends repo: https://github.com/GeneralMills/pytrends
- pytrends on PyPI: https://pypi.org/project/pytrends/
- YouTube videos.list: https://developers.google.com/youtube/v3/docs/videos/list
- YouTube channels.list: https://developers.google.com/youtube/v3/docs/channels/list
- YouTube API quota: https://developers.google.com/youtube/v3/getting-started
- YouTube API revision history: https://developers.google.com/youtube/v3/revision_history
- YouTube Help on trending and Charts: https://support.google.com/youtube/answer/7239739?hl=en-GB
- 9to5Google on Trending removal: https://9to5google.com/2025/07/10/youtube-trending-page-removal/
- India TikTok ban: https://en.wikipedia.org/wiki/Restrictions_on_TikTok
- Apify Creative Center trends actor: https://apify.com/symphonic_mullite/tiktok-creative-center-trends
- Apify Creative Center scraper (signed headers): https://apify.com/datapeak/tiktok-creative-center
- Novoads on Creative Center changes: https://novoads.ai/en/blog/tiktok-creative-center
- Creatify Creative Center guide: https://creatify.ai/blog/tiktok-creative-center
- Birch Creative Center guide: https://bir.ch/blog/tiktok-creative-center
- Tokchart pricing and API: https://tokchart.com/pricing, https://tokchart.com/api
- Soundcharts pricing: https://soundcharts.com/pricing
- Chartmetric pricing: https://chartmetric.com/pricing
- Reddit API pricing (third party): https://octolens.com/blog/reddit-api-pricing
- HotNewHipHop October 2026 list: https://www.hotnewhiphop.com/1011309-hip-hop-albums-dropping-october-2026
- Wikipedia 2026 in hip-hop: https://en.wikipedia.org/wiki/2026_in_hip-hop
