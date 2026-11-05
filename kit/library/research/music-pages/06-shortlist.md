# Phase 1 shortlist: pages to model, sources, access (7 Oct 2026)

Built from 01 (US pages), raw/uk-* (5 UK sub-reports), 03-news-feeds.json, 04-trend-signals, 05-access-and-tooling. Details and links live in those files.

## 1. The big picture
- **@rap = RapTV**, one of 9 niche brands run by Low Battery (@rap, @bars, @drip, @controller, @pophive, @reggaetontv, @countryhub, @uncut, @concert). That is Vision's network plan, already proven in the US.
- **No UK page does @rap-style headline news across platforms**, apart from GRM Daily (which is mostly premieres). UK radio brands (1Xtra, Capital XTRA, Rinse, Kenny Allstar, Charlie Sloth) have abandoned X; their output is freestyles and clips on IG, TikTok and YouTube. **A UK-first @rap is an open lane for beatswitchfm.**
- **A once-a-day run cannot win on speed** (Kurrco posts about 40 a day, GBMC follows drops within 1.5 hours). Win by picking the 3 to 5 biggest stories of the last 24 hours and packaging them better, plus calendar posts built a day ahead.

## 2. Pages to model
### Format leaders (US/global)
| Page | Where | Copyable format |
|---|---|---|
| RapTV (@rap) | IG 12.3M, TikTok 11.5M, X @Rap 1.34M | Branded headline card: photo on top, thin rule, big condensed caption text below (free font SteelFish is close), white/black/orange, logo. X: one line ending "‼️", "🚨OUT NOW🚨", 2 photos side by side. Caption sign-off "Y'all rockin' with ...⁉️" |
| Say Cheese | IG @saycheesetv 2.7M | Tweet card: account name + tick + one-line headline, photo or video below, "👀" |
| Daily Loud | X 6.9M | Tweet card over video, caption ends with a question |
| Kurrco | X 442K, IG @kurrco.xyz | 5 headline patterns: "ARTIST & ARTIST - Title", "TITLE OUT NOW 🚨", "N years ago today...", statement or chart as 2 photos, "via TikTok 🤳" |
| HotNewHipHop | TikTok | Clip led by its single best quote |
| Pop Crave | X 8M | Neutral, sourced one-liners; anniversaries on the hour; streaming milestones |
| Chart Data | X 6.2M | Fill-in data line + cover art (position, movement, weeks, units) |
| DailyRapFacts | X 4M | Birthdays, "New music dropping at midnight" lists |
Also study: Bars (named series), Genius (best TikTok average, 362K views), HipHopDX UK TikTok (855K).

### UK
| Page | Where | Notes |
|---|---|---|
| GBMC = @GreatBritishMC | X 26K, TikTok @greatbritishmc_ | Fastest UK beef/drama page, ~6 posts/day, posted the Morrisson diss 1h34m after upload, mirrors to TikTok in ~1 min. Style: one sentence, one CAPS keyword, one emoji, asterisk censoring, "EXCLUSIVE:", bullet rundowns, photo-grid polls. Red flags: Rainbet gambling promos, unsourced "allegedly" claims. Detection source, confirm before posting |
| GRM Daily | X 397K, IG 2.1M, TikTok 1.2M, YT 6.73M | Biggest UK brand; 2-3 X news posts/day (caption + photo + video, same caption as IG graphic), premieres, "N years ago" throwbacks; ~20-29h ahead of Link Up on shared stories |
| Link Up TV | IG 1.2M | Aggregated clips with ♻️ credits, debate prompts, archive clips |
| Mixtape Madness | IG 628K, TikTok 499K | "🗓️: X dropped N years ago" anniversaries, single-image news, show promos |
| Small fast X accounts | @UKHipHopDaily 4K, @ldn_grassroots 9.6K, @brtankz 5.3K, @theshadeborough 18K | Beat GBMC on some early beef stages; Shade Borough writes explainers (+1 to 24h) |
| Official Charts | X 340K, TikTok @officialukcharts | Midweeks: First Look Sun, Update Mon, Trending Tue; chart Fri 4pm to 5:45pm |
Not news (handoff was wrong): UK Rap Daily (now self-promo of its cypher). Dead: @UKDrillNews_, @UK_Drill_News; @UKRapFacts dormant; Pressplay has no X; BL@CKBOX lost its main IG.
**Gap:** UK TikTok/IG-native rap news pages not yet verified (HipHopDX UK TikTok, Underground Sound UK, @ukrapculture TikTok claims 110K). Check in the logged-in browser during the formats study.

## 3. Story types every leader repeats (automate these first)
Release day ("OUT NOW 🚨", "ARTIST & ARTIST - Title"), "N years ago today" anniversaries, birthdays, chart debuts / midweeks / projections, "new music at midnight" lists, beef rundowns, arrests and court (confirm first), interview quotes, viral clips with a question.

## 4. Source stack for the daily scan
1. **Feeds, free, 81 verified** (03-news-feeds.json): site RSS (TMZ hip hop, XXL, HNHH, The Source, AllHipHop, REVOLT, Shade Room, Bossip, Fader, NME, Rolling Stone UK, Notion, Dazed, Crack, GUAP, Sky Ents, MBW, PR Newswire music), 33 YouTube channel feeds (GRM, Mixtape Madness, Link Up, P110, Pressplay, BL@CKBOX, Sloth, 1Xtra, Capital XTRA, No Jumper, VladTV, Breakfast Club, HOT 97, Genius, Complex, XXL, Lyrical Lemonade, On The Radar, COLORS), UK court and police feeds (Judiciary, Find Case Law, CPS, Met Police), Google News RSS search (exact times, indexes YouTube uploads; best "who posted first" and confirmation tool, and the way round BBC/Daily Mail blocks).
2. **X accounts:** read via the fxtwitter API (free, unofficial: /2/profile/<handle>/statuses, /2/search?q=...&since:; flaky, retry with case variants) or twitterapi.io (~$5/mo) if it breaks.
3. **Trend signals** (04): Shazam UK CSVs (earliest), kworb Spotify daily GB/US, Apple Music JSON, Official Charts, Wikipedia pageviews (spike = 3x 28-day median), Google Trends Trending Now RSS, YouTube Data API music trending. Score movement, not position.
4. **Instagram / TikTok:** logged-in browser (now) or Apify Starter $19/mo when volume grows. TikTok is blocked on this connection.
Not usable: Reddit (fetch blocked, RSS ends 13 Nov 2026), Billboard (402 to scripts), grmdaily.com feed (stale), Spotify country charts, TikTok Creative Center from India.

## 5. Access and tools
- Start at $0: feeds + fxtwitter + browser + Google News RSS. Paid fallbacks: twitterapi.io ~$5, Apify $19, official X API ~$40-80/mo.
- To install on this PC (needs your OK): ffmpeg, yt-dlp (+ Deno for YouTube), gallery-dl. Instagram downloads need cookies from a throwaway account in Firefox. TikTok files via Apify.

## 6. Pipeline rules learned
- Detect everything, confirm before posting: arrests, shootings and "allegedly" claims need a press or police source (Google News) first.
- Match name variants (Morrisson / Morrison). Filter gambling promos and off-topic posts from sources.
- Plan around fixed slots: Official Charts midweeks (Sun/Mon/Tue) and Friday chart; Friday releases; Invite Only Thu 5pm; P110 premieres 11:00.
