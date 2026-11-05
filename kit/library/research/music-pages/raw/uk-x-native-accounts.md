METHOD NOTES (tested 7 Oct 2026)
- A single fxtwitter 404 is not reliable today. @UK_Drill_News, @UKDrillNews, @ukrapnews, @UKDrillNews1 and @ukrapupdates all returned 404 on the first call and 200 on a retry with different letter case. Retry 2 to 3 times with case variants before rejecting a handle. The timeline endpoint also returned HTTP 500 three times for @UKDrillNews.
- New working tool: https://api.fxtwitter.com/2/search?q=<terms>. It accepts since:YYYY-MM-DD and until:YYYY-MM-DD and returns about 20 tweets, newest first, with the author's handle, name and follower count plus a cursor. Some term orders 404 at random: reorder the terms and retry. This was the best way to see who posted first, and it is how I found @UKHipHopDaily and @ldn_grassroots.
- Timeline paging works: add ?cursor=<cursor.bottom> to /2/profile/<handle>/statuses.
- The GBMC timeline only surfaced @brtankz and @keep6ixsolid (both quote-tweeting GBMC). GRM's timeline credits only artists.
- The WebSearch budget ran out, then WebFetch hit the spend limit. That is why there are 8 relevant accounts, not 8 to 15. Gaps are marked UNVERIFIED.

ACTIVE / RELEVANT ACCOUNTS

1. GBMC @GreatBritishMC (seed, additions only)
- 26,090 followers (fxtwitter search author data, 7 Oct 2026). 17 own posts from 4 Oct 15:15 to 7 Oct 14:11 UTC, and 20 from 30 Sep 17:37 to 3 Oct 15:11 UTC: about 6 a day.
- Formats seen in 37 post texts:
  - one-sentence headline with one keyword in CAPS (SNITCHING, LEAKS, FIGHT)
  - exactly one closing emoji
  - asterisk censoring
  - "EXCLUSIVE:" prefix
  - hyphen bullet lists for beef rundowns
  - 2 to 4 photo grids for "which rapper" polls
  - Text placement on the media itself: UNVERIFIED.
- Red flags:
  - At least 5 of 37 own posts are Rainbet streamer-win promos.
  - Off-topic fillers: boxing, Lily Phillips, Tyson Fury.
  - 7 Oct "EXCLUSIVE" post alleges a named CGM artist was involved in a shooting, with no source: https://x.com/GreatBritishMC/status/2107836320051536032

2. UK Rap Daily @UKRapDaily
- What it is: a UK rap content account that now promotes its own release, "UK Rap Daily Cypher 2026" (Spotify and Apple Music links on https://ffm.bio/ukrd).
- UK base: UNVERIFIED. The location field is blank, the IG bio shows a UK flag, and the link page carries a Marathon Artists privacy link.
- Platforms:
  - X https://x.com/UKRapDaily: 96,123 followers, blue check (individual), joined 4 Jan 2021, 22,102 tweets (fxtwitter, 7 Oct 2026). Active.
  - IG https://www.instagram.com/ukrapdaily_/: 13.8K followers (7 Oct 2026). 11 posts 3 to 6 Oct, carousels and clips. Active.
  - TikTok @ukrapdaily01 and YouTube @UKRapDaily1 (from its own link page): followers UNVERIFIED.
  - Threads: UNVERIFIED.
- Posting frequency: 9 own posts/replies plus 8 retweets from 5 Oct 17:55 to 7 Oct 12:03 UTC, about 5 a day. Lifetime average is about 10 a day (computed).
- Content mix: cypher promotion, hot-take captions on single clips or photos, retweets of fan praise.
- Originates or aggregates: no breaking news and no "via" credits in this window. It has posted chart stats before: Feb 2025 first-week UK album sales, Central Cee vs The Weeknd (search snippet): https://x.com/UKRapDaily/status/1889026793950289931
- Speed: no evidence. It posted nothing on the Morrison vs Digga D beef from 5 to 7 Oct.
- Formats:
  - opinion caption plus a closing emoji
  - quote-tweets its own post with a question to restart replies
  - line-broken stat comparisons
  - Visual layout: UNVERIFIED.
- Examples:
  - https://x.com/UKRapDaily/status/2107169697682817050 (5 Oct, video, 235,334 views)
  - https://x.com/UKRapDaily/status/2107167822518346023 (5 Oct, 2 photos, 131,652 views)
  - https://x.com/UKRapDaily/status/2107795295325327388 (7 Oct)
- Red flags: currently in a self-promo phase, with engagement-bait posts saying older fans hate the cypher.
- Earlier file's claims:
  - "closest thing to a UK Kurrco / best aggregator": NOT SUPPORTED on 7 Oct (self-promo, no news). Otherwise opinion, UNVERIFIED.
  - Instagram @ukrapdaily_: CONFIRMED.
  - Threads @ukrapdaily_: UNVERIFIED.

3. TheShadeBorough @theshadeborough
- What it is: culture, news, gossip ("tea") and music account. UK flag in bio; UK base otherwise UNVERIFIED.
- X https://x.com/theshadeborough: 18,454 followers, verified (individual), joined 18 Sep 2016, 11,851 tweets (fxtwitter, 7 Oct 2026). Active (2 and 4 Oct).
- IG @theshadeborough and linktr.ee/theshadeborough: not fetched, UNVERIFIED.
- Posting frequency: UNVERIFIED. Lifetime average is about 3 a day (computed).
- Formats: multi-sentence explainer captions covering both sides. Media layout UNVERIFIED.
- Originates or aggregates: aggregates. It posted after GBMC both times on this story.
- Speed: 58 minutes behind GBMC on 4 Oct, about 16 hours behind on 2 Oct.
- Examples:
  - https://x.com/theshadeborough/status/2106829501179335069 (4 Oct)
  - https://x.com/theshadeborough/status/2106002387165204980 (2 Oct)

4. UKHipHopdaily @UKHipHopDaily
- 4,009 followers (fxtwitter search author data, 7 Oct 2026). Active to at least 29 Sep.
- Bio, UK base and posting frequency: UNVERIFIED. The profile call 404'd once before the limit hit.
- Content: Title Case headlines from artists' Instagram posts and previews; some open with a siren emoji and add a bracketed tag such as "( Digga Diss )".
- Some posts land on exactly :00 seconds, which suggests scheduled posting (observation only).
- Speed: ahead of GBMC on 19 Sep and 29 Sep.
- Examples:
  - https://x.com/UKHipHopDaily/status/2104899993568157947
  - https://x.com/UKHipHopDaily/status/2101268567110902264
  - https://x.com/UKHipHopDaily/status/2101330666893857088

5. LDN GRASSROOTS @ldn_grassroots
- 9,595 followers (fxtwitter search author data, 7 Oct 2026).
- Bio, UK base (the name suggests London), posting frequency and formats: all UNVERIFIED.
- Speed: on 21 Sep it was first of three accounts, 80 minutes ahead of @brtankz and 92 minutes ahead of GBMC: https://x.com/ldn_grassroots/status/2101985959482896690

6. Tankz @brtankz
- What it is: a London podcaster (Click It Podcast; bio claims 180k YouTube subscribers) who posts news-style headlines and commentary.
- Location field: London, England.
- 5,279 followers, verified (individual), joined 9 Jun 2020 (fxtwitter, 7 Oct 2026). Active.
- Format: headlines that open with "U.K. Rapper <full name>".
- Speed: 12 minutes ahead of GBMC on 21 Sep, 89 minutes behind on 28 Sep.
- Examples:
  - https://x.com/brtankz/status/2104669876757704707
  - https://x.com/brtankz/status/2102006062874349719
  - https://x.com/brtankz/status/2107535944626631070 (quote of GBMC, 190,520 views)
- Red flag: a personality account that mixes opinion with news.

7. @UKDrillNews (status unclear)
- 23,713 followers, 20,937 tweets, joined 15 Feb 2017, location London, not verified (fxtwitter, 7 Oct 2026). A search snippet (crawl date unknown) showed 24.9K, so followers have dropped.
- Activity: UNVERIFIED (timeline endpoint returned 500).
- Red flags: the display name is a single dash character and the bio is an "entertainment purposes" disclaimer, which suggests a renamed or rumour account. Hold until its activity is confirmed.

8. Official Charts @officialcharts (chart source)
- What it is: the UK chart compiler. London. 339,719 followers, verified organisation, 138,466 tweets (fxtwitter, 7 Oct 2026).
- Timeline: not fetched, UNVERIFIED.
- Formats (from search snippets):
  - midweek "First Look" posts tagging artists
  - "full midweek Top 100" link posts
  - Number 1 race posts asking fans to pledge in the replies
- Examples:
  - https://x.com/officialcharts/status/2020592250539987201 (8 Feb 2026)
  - https://x.com/officialcharts/status/1883628509198709177 (Jan 2025)

UK CHART NEWS ON X
- Only @officialcharts is verified as a working chart source.
- @UKChartsPlus is a 25-follower personal account.
- I could not test any other chart-stat accounts: UNVERIFIED.
- Lead: replies on 6 Oct say Morrison's diss charted (for example @trillarybanks6, https://x.com/trillarybanks6/status/2107493523645764036). Not yet checked against officialcharts.com.

MORRISON VS DIGGA D: WHO POSTED FIRST (times UTC, search page 1 plus timelines, not exhaustive)
- 19 Sep: @UKHipHopDaily 11:14. No GBMC post on this part of the story surfaced.
- 21 Sep: @ldn_grassroots 10:44, then @brtankz 12:04, then GBMC 12:16 (https://x.com/GreatBritishMC/status/2102009089094041846).
- 28 Sep (voice-note leak): GBMC 19:00, then @brtankz 20:29.
- 29 Sep (diss preview): @UKHipHopDaily 11:44. GBMC's next Morrison post was at 19:35, on a different angle.
- 1 Oct (diss released): GBMC 20:23 (https://x.com/GreatBritishMC/status/2105755510058139654, 733,496 views). Search did not reach earlier posts that day, so the first poster is UNVERIFIED.
- 4 Oct (Digga D's reply): GBMC 18:33 (825,466 views), then @theshadeborough 19:31.
- @UKRapDaily (5 to 7 Oct) and @GRMDAILY (20 posts, 1 to 7 Oct) posted nothing on the beef.
- Verdict: GBMC is first or close to first on most stages and gets by far the biggest views, but small accounts beat it on the early stages.

CHECKED AND REJECTED
- @UKDrillNews_: 10 followers, 9 tweets, all from 18 Apr 2021. Dead.
  - Earlier claim "daily UK drill news": the bio matches (CONFIRMED), but it is WRONG as a source.
- @UK_Drill_News: name "UK Drill Daily" and bio (recaps, throwbacks, murders, arrests, song drops) CONFIRMED.
  - Earlier claim "covers the court and prison side": WRONG / UNVERIFIED. Nothing like that in its last 20 posts.
  - Location San Diego, CA; 24 followers. Last activity 16 to 17 Oct 2023 was nine retweets of a crypto giveaway from a suspended account. Dead and likely compromised.
- @UKRapFacts: 12,274 followers, 11,262 following (follow-back pattern), location UK.
  - Last post 11 Nov 2024 (712 views); the one before that was 20 Oct 2020. Dormant.
  - Earlier claims: bio topics CONFIRMED; "context/history over breaking" CONFIRMED in style but irrelevant now.
  - IG @UKRapFacts: UNVERIFIED.
- @PopTingz: 359,151 followers. About 14 posts a day, all US/global pop, plus one Polymarket-sourced post. No UK rap; UK base UNVERIFIED.
- @BuzzingPop: 285,717 followers. About 12 posts a day, US pop. No UK rap.
- @keep6ixsolid: 22,559 followers, Toronto, not UK. It amplifies UK drill stories: its 4 Oct quote of GBMC got 419,105 views.
- @GRIMEDAILY: placeholder account whose bio just points to @GRMDAILY (245 followers, 2 tweets). Can be confused with GRM Daily.
- Empty, personal or tiny: @UKDrillNews1 (132), @news_drill (3), @nation_drill (36), @ukrapupdates (0), @ukrapnews (personal account, 270), @ukmusicnews (244).
- @UKRapCulture: 95 followers on X, but its bio claims 110k on TikTok (tiktok.com/@ukrapculture). Passing to the TikTok agent, UNVERIFIED.
- Repeated 404s, inconclusive because of the flaky API: @UKRapStats (3 tries); @UKHipHopNews, @UKRapCharts, @DrillUKNews, @BritishRapNews, @RapUKNews (2 tries each); @UKRapAlert, @uk_drill, @ukdrillrapnews (1 try each).

SEEN BUT NOT VERIFIED (leads)
- @MusicConnoisseu: 48,055 followers, commentary.
- @livebytherules1: 8,161 followers.
- @trillarybanks6: 9,989 followers, commentator.
- @UKDrillScene: search snippet only, 542 followers, crawl date unknown.