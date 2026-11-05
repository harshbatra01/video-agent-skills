# 01. US and global rap / music news pages to study

Research date: 7 October 2026. Prepared for Vision Clipping (rap / music news page automation).
Scope: US and global rap, hip-hop and music news and culture pages that post news as short-form video and image posts (TikTok, Instagram, YouTube Shorts), plus the fastest X accounts. UK-only pages are out of scope for this file.

---

## 0. How to read this file

### Source codes

All figures were retrieved on 7 Oct 2026 unless the cell gives another date.

| Code | What it is | Notes |
|---|---|---|
| IG | Public Instagram profile page, `https://www.instagram.com/<handle>/` | Instagram displays rounded counts (for example 12.3M) |
| FX | `https://api.fxtwitter.com/<handle>` (public X profile data) and `https://api.fxtwitter.com/2/profile/<handle>/statuses` (recent posts with UTC timestamps) | Exact follower counts. Timelines worked for some accounts only |
| SP | `https://socialpruf.com/tiktok/<handle>` | TikTok followers plus a 12-month window (7 Oct 2025 to 7 Oct 2026): videos posted in the window, average views per video |
| TS | TikTok profile snippet returned by web search on 7 Oct 2026 | Crawl date not shown. Treat as approximate |
| SRJ | speakrj.com YouTube reports | Data date given in the cell |
| CX26 | Complex, "Hip-Hop Media Power Ranking (The 2026 Edition)", published 5 May 2026 | https://www.complex.com/music/a/dimassanfiorenzo/hip-hop-media-power-ranking-2026-edition |
| WP | Wikipedia article | Date given in the cell where the article gives one |
| calc | My own arithmetic from the figures above (for example posts per day) | Method stated in the cell |

### Rules applied

- Every handle in the ranking was checked live on 7 Oct 2026. Anything I could not confirm is marked UNVERIFIED.
- Instagram post-type mix comes from the 12 most recent grid posts on the profile page, using Instagram's own auto alt-text. Instagram labels some posts "Twitter screenshot", which means the image is laid out like a tweet card (avatar, name, tick, headline text, media under it).
- "Lifetime average" posting rates = total posts on X divided by days since the account joined (calc). Recent rates come from FX timestamps.

### Limits of this pass (read before relying on it)

- TikTok.com is blocked on the network this research ran from (connection refused). TikTok numbers therefore come from SP or TS, and nobody has looked at TikTok on-screen layouts yet. All TikTok layout notes are UNVERIFIED until someone opens the example URLs.
- No images or videos were viewed (no media downloads). Layout notes are built from post text, Instagram alt-text, X media counts and published descriptions. Anything beyond that is marked "verify".
- The session's web-search budget ran out (200 searches) and the fetch tool then hit a spend limit, so some gaps remain. They are listed in section 7.

---

## 1. Key findings

1. **"@rap" and "RapTV" are the same brand.** Instagram @rap is RapTV (12.3M, IG), TikTok @rap is RapTV (11.5M, SP), and RapTV's X handle is now @Rap (1,337,952, FX). Its old X handle @raptvcom now belongs to an unrelated 16-follower account (FX), and Instagram @raptv is an unrelated 147-follower account called "Verse" (IG). RapTV is one of nine Low Battery brands (@rap, @bars, @drip, @controller, @pophive, @reggaetontv, @countryhub, @uncut, @concert), which Low Battery says reach "over 200M fans monthly" (https://raptv.com/workwithus/). This is the closest existing model to Vision Clipping's network-of-niche-pages plan.
2. **X size does not carry over to TikTok.** Daily Loud has 6,918,714 on X (FX) but about 10.6K on TikTok (TS). Say Cheese: 1,688,124 on X vs 26.9K on TikTok (TS). Pop Crave: 7,959,167 on X vs 40.3K on TikTok (SP). The TikTok leaders are video-native brands: RapTV 11.5M followers with 332K average views per video, Genius 9.40M (362K), Complex 6.36M (265K), The Shade Room 3.34M (221K), Bars 2.14M (286K), all SP. HipHopDX has 3.3M plus a UK TikTok with 855.3K (TS).
3. **Speed benchmark (FX timestamps, calc).** Kurrco: 20 X posts in about 11 hours (6 to 7 Oct), so roughly 40 a day. Chart Data: 20 posts in 8 hours on Billboard chart day. Pop Crave: 20 in about 20 hours. RapTV: 19 in about 24 hours. Say Cheese: 19 in about 36 hours. Say Cheese also uploaded 68 YouTube videos on 6 Oct 2026 (SRJ). A once-a-day agent cannot win on speed. It can win by picking the 3 to 5 biggest stories of the last 24 hours and packaging them better.
4. **The same story types recur at every leader and are easy to automate.** Release-day posts ("OUT NOW 🚨"), "N years ago today" anniversaries (RapTV, Kurrco, Pop Crave and XXL all posted the 4-year anniversary of Quavo and Takeoff's "Only Built For Infinity Links" on 6 to 7 Oct 2026), birthdays, chart debuts and projections, "new music dropping at midnight" lists.
5. **The tweet card is the dominant Instagram layout.** Instagram labels recent posts "Twitter screenshot" at Say Cheese (4 of 12), Hot Freestyle (4 of 12), HipHopDX/UPROXX (4 of 12), RapMusic (2 of 12), and once each at Daily Loud, The Shade Room, DJ Akademiks, Our Generation Music and Underground Sound. Our white caption box with black headline is a close cousin of this layout.
6. **Many well-known handles are traps or unstable.** HipHopDX's website now redirects to its Instagram. No Jumper's Instagram was taken down (April 2025, WP). Instagram @kurrco is an unrelated private user (the real page is @kurrco.xyz). Instagram @lyricallemonade is a placeholder (the real page is @lyricalemonade, and on X it is @LyricaLemonade). DJ Akademiks' main X handle did not resolve on 7 Oct 2026. A "Rap Alert" news page could not be verified at all (section 6).

---

## 2. Ranking: top 25 models for our page

Weighting: fit with our formats (vertical video and image news with a client song underneath), how consistent and copyable the template is, scale and engagement on TikTok and Instagram, speed, and red flags.

| # | Page | Main handle(s) | Biggest platform: followers (source) | Why study it | Format leader |
|---|---|---|---|---|---|
| 1 | RapTV (Low Battery) | IG and TikTok @rap, X @Rap | IG 12.3M (IG); TikTok 11.5M (SP) | Closest analogue: one fixed brand template, very high cadence, strong TikTok views | Yes |
| 2 | Say Cheese | IG @saycheesetv, X @SaycheeseDGTL | IG 2.7M (IG) | Tweet-card posts at volume, YouTube 1.61M with Shorts-scale uploads | Yes |
| 3 | Daily Loud | X @DailyLoud, IG @daily_loud | X 6,918,714 (FX) | Largest rap-news X account in this set, tweet-card reels | Yes |
| 4 | Kurrco | X @Kurrco, IG @kurrco.xyz | X 442,198 (FX) | Fastest rap X account, tight headline grammar | Yes |
| 5 | HotNewHipHop | @hotnewhiphop, X @HotNewHipHop | X 4,854,218 (FX) | TikTok clip plus quote captions, IG carousels | Yes |
| 6 | XXL | @xxl, X @XXL | IG 9.1M (IG) | Carousel news, anniversaries with a question prompt | |
| 7 | Complex / Complex Music | @complex, @complexmusic, X @ComplexMusic | IG @complex 10.7M (IG); TikTok 6.36M (SP) | Very high TikTok volume, carousel news | |
| 8 | The Shade Room | @theshaderoom | IG 28M (IG) | Reels-first culture news, strong community voice | |
| 9 | Genius | @genius | YouTube 12M (SRJ); TikTok 9.40M (SP) | Best average TikTok views in this set (362K) | |
| 10 | HipHopDX (UPROXX Studios) | @hiphopdx, TikTok @hiphopdx.uk | TikTok 3.3M (TS) | TikTok news plus a UK TikTok (855.3K) | |
| 11 | Pop Crave | X @PopCrave | X 7,959,167 (FX) | Clean, neutral headline grammar, music stats | Yes |
| 12 | Chart Data | X @chartdata | X 6,157,876 (FX) | Chart-number posts that a template can fill | Yes |
| 13 | DailyRapFacts | X @DailyRapFacts | X 3,990,913 (FX) | Birthday and release-list templates | Yes |
| 14 | Pop Base | X @PopBase | X 7,502,800 (FX) | Fastest verified growth in this set | |
| 15 | Hot Freestyle | IG @hotfreestyle | IG 3.7M (IG) | Viral clip reels in tweet-card layout | |
| 16 | WorldStarHipHop | @worldstar, X @WORLDSTAR | IG 43.5M (IG) | Scale on every platform | |
| 17 | Bars (Low Battery) | @bars | IG 2.4M (IG); TikTok 2.14M (SP) | Repeatable named series | |
| 18 | MyMixtapez | @mymixtapez | IG 1.7M (IG) | About 12 carousels a day | |
| 19 | DJ Akademiks | IG @akademiks | IG 5.1M (IG) | Reels-first news commentary, ranked #1 in CX26 | |
| 20 | Our Generation Music (OGM) | @ourgenerationmusic | IG 870K (IG) | News carousels plus interview clips | |
| 21 | Underground Sound | @undergroundsound | IG 274K (IG) | Growing underground page with a UK branch | |
| 22 | Lyrical Lemonade | @lyricalemonade, X @LyricaLemonade | YouTube 24M (SRJ) | Music-video look, not news | |
| 23 | RapMusic | IG @rapmusic | IG 5M (IG) | Typical large repost page | |
| 24 | Billboard | @billboard, @billboardhiphop | IG 17.5M (IG); X 16,825,590 (FX) | Primary source for chart news | |
| 25 | No Jumper | YouTube, X and TikTok @nojumper | YouTube 4.98M (SRJ, 1 Oct 2026) | Interview clip source | |

---

## 3. Format leaders (8): what an automated template can copy

These eight have the most consistent, rule-like formats. Each spec says what is verified and what still needs a visual check.

### A. RapTV: branded headline card + "‼️" headline grammar
- **Feed image (IG):** photo in the upper part of the frame, a thin horizontal rule, then a large block of condensed, blocky caption text underneath, in a white, black and orange palette with orange for emphasis, plus the RapTV logo. Sources: palette and history from Know Your Meme (orange, white and black since 22 April 2020, https://knowyourmeme.com/memes/sites/raptv-rap); structure from a fan-made generator (image area, divider, caption below, https://yimmyj.github.io/RapTVTemplate/) whose README says the free font SteelFish is close to RapTV's caption font (https://github.com/yimmyj/RapTVTemplate). Exact proportions and logo position: verify on the example URLs.
- **Caption sign-off:** news paragraph ending "Y'all rockin' with ...⁉️" (seen on https://www.instagram.com/p/DeLu1h_FvcQ/, 6 Oct 2026, 68.9K likes, 910 comments).
- **X grammar (FX):** one-line headline ending "‼️" plus a topical emoji ("Drake's 'HABIBTI (FOMO)' remains the #1 album on Apple Music US‼️🏆"); release posts in capitals with "🚨OUT NOW🚨"; "▪️" bullets for lists; many posts carry 2 photos, which X shows side by side (close to our two-photos-across-the-top layout).
- **Template takeaway:** fixed palette, one condensed display font, highlight 1 to 3 key words in the accent colour, fixed sign-off line in the caption.

### B. Say Cheese: tweet card
- **Layout:** the post is a tweet-style card (account name and tick, one-line headline) above the photo or video. Instagram labelled 4 of the last 12 posts "Twitter screenshot" (IG, 6 Oct 2026).
- **Copy:** one plain sentence plus "👀", repeated as the caption ("NBA YoungBoy says he wants to quit music 👀", https://www.instagram.com/p/DeKTn_JScMO/, 8.7K likes, 354 comments).
- **X:** one sentence plus a single photo on most of 19 posts (FX).
- **Template takeaway:** headline text block on white, media below, same sentence reused across X, IG and Shorts.

### C. Daily Loud: tweet card over video
- **Layout:** IG is mostly reels with a text block on the video (8 of 12 recent posts are clips; one labelled "Twitter screenshot"). Exact text position: verify.
- **Copy:** news sentence, then a quote, then a question prompt ("What're your thoughts on this??! 🤔", https://www.instagram.com/reel/DeICS09p_aM/).
- **Template takeaway:** headline box above or on top of a clip, and always end the caption with a question.

### D. Kurrco: minimal X headline grammar
- Verified from 20 posts on 6 to 7 Oct 2026 (FX). Five repeatable patterns:
  1. "ARTIST & ARTIST - Song Title" plus the video.
  2. "TITLE OUT NOW 🚨" in capitals plus the video.
  3. "4 years ago today, Quavo & Takeoff released their project 'ONLY BUILT FOR INFINITY LINKS' 💿♾️ Favorite tracks on the album?" plus 3 photos (https://x.com/Kurrco/status/2107683223996142044).
  4. Statements and chart projections as 2 photos.
  5. "Artist via TikTok 🤳🔥" style source tags.
- **Template takeaway:** a short headline library keyed by story type (release, anniversary, statement, chart, clip).

### E. HotNewHipHop: clip plus quote (TikTok)
- TikTok captions (TS titles): a quoted line, then emoji, then artist hashtags, for example "\"I went stupid in there, I don't know what I said, but...\" 😭🔥 #LilWayne #Drake" (https://www.tiktok.com/@hotnewhiphop/video/7545870084837739783). Also "throwback to ..." clips and short trivia ("You can tell that #LilWayne really inspired #YoungThug").
- On-screen layout: UNVERIFIED (TikTok not reachable). Check the example URLs.
- **Template takeaway:** pull the single best quote from the clip and lead with it.

### F. Pop Crave: neutral one-liner, sourced
- From 20 posts on 6 to 7 Oct 2026 (FX): one neutral sentence, no hype, frequent 2-photo posts, sources named ("per HITSDD"; follow-up reply "Full story from @Deadline").
- Anniversaries go out on the hour ("10 years ago today, Bruno Mars released \"24K Magic.\"", https://x.com/PopCrave/status/2107682329640783903, posted 04:00:00 UTC).
- Streaming milestones: "\"Opalite\" by Taylor Swift has reached 900 MILLION streams on Spotify. It's her 34th song to achieve this." (https://x.com/PopCrave/status/2107770122303615302).
- **Template takeaway:** a calm, factual headline style for non-rap music news and stats.

### G. Chart Data: data line
- From 20 posts on 6 Oct 2026 (FX): one data line plus cover art. Patterns:
  - "Leon Bridges' 'Happiness Anytime' debuts at #74 on this week's Billboard 200 (14K sold)." (https://x.com/chartdata/status/2107577685119504515)
  - "Billboard Hot 100: #21(-9) I Knew It, I Knew You, Taylor Swift [17 weeks]." (https://x.com/chartdata/status/2107490929242460227)
  - Projections: "Drake's 'HABIBTI' expected to rise to #3 on the Billboard 200 with 65K units" (https://x.com/chartdata/status/2107585247030485439)
- **Template takeaway:** fill-in-the-blanks chart card (position, movement, weeks, units) with the cover art.

### H. DailyRapFacts: birthdays and release lists
- From 20 posts, 24 Sep to 5 Oct 2026 (FX):
  - Birthday: "Happy birthday to Lil Wayne 🐐 / He turned 44 today 🎈" plus 2 photos (https://x.com/DailyRapFacts/status/2104229773463486669).
  - Release list: "New music dropping at midnight:" then one line per release, text only (https://x.com/DailyRapFacts/status/2103246809703575823).
  - Stats with emoji bullets: "$390M grossed 💰 / 2 million tickets sold 🎟️ / 47 shows 🎤" (https://x.com/DailyRapFacts/status/2103309501893861485).
- **Template takeaway:** calendar-driven posts that can be generated a day ahead.

Honourable mention for series formats: **Bars (Low Battery)** runs named series listed in its IG highlights: Self Portrait, Name The Sample, Conversations, Breakdowns, KICKING IT, Community, 5 Songs, ON THE GROUND, Blind Karaoke, EOY AWARDS (IG). Its TikTok averages 286K views per video (SP).

---

## 4. Page profiles (ranked pages)

Field order for each page: handles and followers; posting frequency; content mix; originates or aggregates; speed reputation; signature formats; example posts; red flags.

### 1. RapTV (Low Battery)
- **Handles and followers:** IG @rap 12.3M, 1,785 following, verified, bio "What's Next in Hip Hop & Culture‼️ 🔋 a @lowbattery brand" with links to @bars, @concert, @drip (IG). TikTok @rap 11.5M (SP; TS also shows 11.5M followers and 879.5M likes). X @Rap 1,337,952, joined 12 Nov 2018, 19,788 posts, bio "a Low Battery brand" (FX). YouTube: about 528K per a YouTube fan-wiki snippet (https://youtube.fandom.com/wiki/RapTV, date not shown), channel handle UNVERIFIED; note youtube.com/@raptv is an unrelated channel ("Raptv Shampel").
- **Frequency:** X 19 posts in about 24 hours, 6 to 7 Oct (FX). IG 9 grid posts dated 6 Oct (IG). TikTok 2.76K videos in the 12-month window, about 7.6 a day (SP, calc).
- **Content mix:** IG last 12 (3 pinned): 10 carousels, 1 photo, 1 clip; 5 alt-texts say "image of text" (IG). TikTok: 332K average views per video (SP).
- **Originates or aggregates:** mostly aggregates; original series such as "Media Day" (X post "OHGEESY MEDIA DAY EP 28", 6 Oct 2026; IG highlights "Media Day", "Power Rankings", "Rap Madness").
- **Speed:** no independent source found; observed 19 X posts a day.
- **Signature formats:** see format leader A. Covers more than rap (GTA 6, the Paramount and Warner Bros. Discovery merger on 6 Oct 2026).
- **Examples:** https://www.instagram.com/p/DeLu1h_FvcQ/ ; https://www.instagram.com/reel/DeLIHfztLW7/ ; https://x.com/Rap/status/2107841966637518992 (GRAMMY submissions list, 2 photos) ; https://x.com/Rap/status/2107504994853568805 (music video "OUT NOW")
- **Red flags:** parody account @RappTvcum (1,979 followers, bio says "Not affiliated with RapTV. Parody. Fan Account!!", FX); old handle @raptvcom reassigned to an unrelated account (FX); IG @raptv unrelated (IG); Know Your Meme documents earlier parody accounts. The Wikipedia article "RapTV" returned 404 on 7 Oct 2026, so independent background is thin.

### 2. Say Cheese
- **Handles and followers:** IG @saycheesetv 2.7M, verified, bio "700,000,000 youtube views ... Backup page: SAYCHEESEDIGITAL" (IG). X @SaycheeseDGTL 1,688,124, following 49, 54,853 posts, joined 10 Jul 2019 (FX). TikTok @saycheesetv 26.9K followers, 144.4K likes (TS). YouTube "SAY CHEESE!" @saycheesetv 1.61M subscribers, 792.2M views, 5,796 videos (SRJ, 6 Oct 2026).
- **Frequency:** X 19 posts in about 36 hours, about 13 a day (FX, calc). IG: all 12 grid posts dated 6 Oct. YouTube: 68 uploads on 6 Oct 2026 (SRJ).
- **Content mix:** IG last 12: 5 clips, 3 photos, 4 carousels; 4 labelled "Twitter screenshot" (IG). Topics range from rap to sports, crime, politics and consumer recalls (FX).
- **Originates or aggregates:** aggregates.
- **Speed:** no independent source; observed about 13 X posts a day.
- **Signature formats:** format leader B.
- **Examples:** https://www.instagram.com/p/DeKTn_JScMO/ ; https://www.instagram.com/reel/DeLOGQVsoeh/ ; https://x.com/SaycheeseDGTL/status/2107520511123280101
- **Red flags:** posts unverified personal allegations about creators (example: https://x.com/SaycheeseDGTL/status/2107114266147111348, 5 Oct 2026); lookalike X account @Saycheesetv1 (389 followers, not verified, FX); the IG bio advertises a backup page, which suggests they plan for losing the main page (my inference). Tiny TikTok.

### 3. Daily Loud
- **Handles and followers:** X @DailyLoud 6,918,714, following 168,036, 119,359 posts, joined 1 Jan 2012, bio "#1 Source For Hip-Hop/Viral News Across The Planet" (FX). IG @daily_loud 573K, verified, bio "#1 Source For Hip-Hop / Viral News ... DM for credit or removal" (IG). TikTok @dailyloud 10.6K followers, 374.1K likes (TS). YouTube channel exists (https://www.youtube.com/channel/UC0QZGKjjqlWckm15phgZvsA), subscribers UNVERIFIED.
- **Frequency:** X lifetime average about 22 posts a day (calc). IG 12 grid posts over 4 to 6 Oct (IG). X timeline could not be retrieved (FX returned 404).
- **Content mix:** IG last 12: 8 clips, 4 photos; 1 labelled "Twitter screenshot" (IG).
- **Originates or aggregates:** aggregates (bio).
- **Speed:** no independent source found.
- **Signature formats:** format leader C.
- **Examples:** https://www.instagram.com/reel/DeICS09p_aM/ ; https://www.instagram.com/p/DeIQqV6xIuB/ ; https://www.instagram.com/reel/DeLFk8HRfXe/
- **Red flags:** following count of 168,036 points to follow-back growth; X followers rose from 376,296 (SpeakRJ capture of 13 Jan 2022, https://www.speakrj.com/audit/report/DailyLoud/twitter) to 6,918,714 (FX), while a sampled IG reel had 417 likes and 31 comments. Check engagement before treating its X size as reach. Very small TikTok.

### 4. Kurrco
- **Handles and followers:** X @Kurrco 442,198, following 1,344, 26,893 posts, joined 26 Jul 2021, verified, site kurrco.xyz (FX). IG @kurrco.xyz 26.7K, verified (IG). TikTok @kurrco listed on https://linktr.ee/kurrco, followers UNVERIFIED. CX26 (5 May 2026): 385.5K X, 19.5K IG, so X grew about 15% and IG about 37% in five months (calc).
- **Frequency:** 20 X posts in about 11 hours, 6 to 7 Oct 2026 (FX); lifetime average about 14 a day (calc).
- **Content mix:** X posts with video or 1 to 4 photos; IG carousels and clips (IG).
- **Originates or aggregates:** mostly aggregates; occasionally breaks news, for example first to confirm the release date of Playboi Carti's "MUSIC" (Complex, 17 Jul 2026, https://www.complex.com/music/a/dimassanfiorenzo/kurrco-identity-who-runs-rap-twitter).
- **Speed:** "known for speed, typically posting within minutes" (same Complex article); CX26 ranks it #8 for the quickest rap news delivery. Team of three, anonymous, Europe-based founder (Complex).
- **Signature formats:** format leader D.
- **Examples:** https://x.com/Kurrco/status/2107683223996142044 ; https://x.com/Kurrco/status/2107684050357870880 ; https://x.com/Kurrco/status/2107587896966611129
- **Red flags:** anonymous operator; brand deals include betting companies (Complex); IG @kurrco is an unrelated private account ("Carlos Andres", 163 followers, IG).

### 5. HotNewHipHop
- **Handles and followers:** X @HotNewHipHop 4,854,218, joined 12 Mar 2009, 47,596 posts (FX). IG @hotnewhiphop 938K, verified (IG). TikTok @hotnewhiphop 1.1M followers, 57.1M likes (TS).
- **Frequency:** X lifetime average about 7.4 a day (calc); IG about 5 a day in the visible grid (IG).
- **Content mix:** IG last 12: 9 carousels, 3 clips (IG). TikTok: rapper moment clips, throwbacks (TS titles).
- **Originates or aggregates:** aggregates, plus its website (listed in X bio).
- **Speed:** no independent source found.
- **Signature formats:** format leader E.
- **Examples:** https://www.tiktok.com/@hotnewhiphop/video/7545870084837739783 ; https://www.tiktok.com/@hotnewhiphop/video/7510229179942653240 ; https://www.instagram.com/reel/DeKCikEqtvK/
- **Red flags:** none found in this pass.

### 6. XXL
- **Handles and followers:** IG @xxl 9.1M (IG). X @XXL 4,866,572, joined 2 May 2008, 277,656 posts (FX). TikTok @xxl 1.88M; 532 videos in the window; 150.8K average views; top post 9.82M impressions (SP).
- **Frequency:** IG about 9 posts on 6 Oct (IG); X lifetime average about 41 a day (calc); TikTok about 1.5 a day (SP, calc).
- **Content mix:** IG last 12: 11 carousels, 1 clip (IG). Highlights: The Break, 2025 Freshman, XXL Awards 2025, Best Diss Songs, Lids 2025 Class.
- **Originates or aggregates:** originates (magazine, Freshman Class, awards) and aggregates.
- **Speed:** no independent source found.
- **Signature formats:** carousel news; anniversary image with a question prompt ("Four years ago today, Quavo and Takeoff dropped their collab album Only Built For Infinity Links 💿 What's your favorite song on here?", 1.4K likes and 132 comments in its first hour).
- **Examples:** https://www.instagram.com/p/DeMaw86ESiT/ ; https://www.instagram.com/reel/DeK5ZsENqS8/ ; https://www.instagram.com/p/DeKlMMhmQxX/
- **Red flags:** none found.

### 7. Complex / Complex Music
- **Handles and followers:** IG @complex 10.7M; IG @complexmusic 2.1M, bio "Never not listening" (IG). X @ComplexMusic 1,817,149, joined 26 Jan 2011, 160,137 posts (FX). TikTok @complex 6.36M; 7.70K videos in the window; 265K average views; 2.04B views in 12 months (SP). TikTok @complex_uk 43.6K (TS).
- **Frequency:** TikTok about 21 videos a day (SP, calc); IG @complexmusic about 8 posts on 6 Oct (IG); X lifetime average about 28 a day (calc).
- **Content mix:** IG @complexmusic grid: 10 carousels, 2 clips, several co-posted with Complex sister accounts (IG).
- **Originates or aggregates:** originates (editorial, ComplexCon, the annual Media Power Ranking) and aggregates.
- **Speed:** no independent source found.
- **Signature formats:** carousel news on IG; very high-volume TikTok. Layouts: verify.
- **Examples:** https://www.instagram.com/p/DeMl4Kwk3aj/ ; https://www.instagram.com/p/DeLMVRPkQZK/ ; https://x.com/ComplexMusic/status/2078224801072611407 (its "Who Is Kurrco?" post)
- **Red flags:** none found.

### 8. The Shade Room
- **Handles and followers:** IG @theshaderoom 28M, bio "Run by 28M+ hilarious Roommates" (IG); WP lists 28.1M plus 4.8M on The Shade Room Teens. TikTok @theshaderoom 3.34M; 1.06K videos in the window; 221K average views (SP). X @TheShadeRoom 954,692 (FX).
- **Background (WP):** founded March 2014 by Angelica Nwandu, Los Angeles, about 40 staff; nominated Best Hip Hop Platform at the 2024 BET Hip Hop Awards; Shorty Awards 2025 Site of the Year.
- **Frequency:** 6 IG grid posts by early 7 Oct and 6 more on 6 Oct (IG); TikTok about 3 a day (SP, calc); X lifetime average about 16 a day (calc).
- **Content mix:** IG last 12: 8 clips, 2 photos (1 "Twitter screenshot"), 2 carousels (IG).
- **Originates or aggregates:** both; WP lists awards for investigative and branded series.
- **Speed:** no independent source found.
- **Signature formats:** reels with text, tweet-card photos, text carousels; audience addressed as "Roommates" (WP).
- **Examples:** https://www.instagram.com/reel/DeMe9nVSePc/ ; https://www.instagram.com/p/DeMNRQhyjY9/ ; https://www.tiktok.com/@theshaderoom/video/7148279884761206062
- **Red flags:** celebrity gossip brand; music is one strand of many.

### 9. Genius
- **Handles and followers:** TikTok @genius 9.40M; 956 videos in the window; 362K average views; top video 18M views (SP); bio "More Than The Music" (TS). IG @genius 6M (IG). X @Genius 1,636,995 (FX). YouTube 12M (SRJ top-100 list, data date 7 Oct 2026).
- **Frequency:** TikTok about 2.6 a day (SP, calc).
- **Content mix:** artist interviews and lyric breakdowns (SP); IG clips and carousels (IG).
- **Originates or aggregates:** originates.
- **Speed:** not a breaking-news brand.
- **Signature formats:** artist explainer and interview videos. Layouts: verify.
- **Examples:** none retrieved in this pass (UNVERIFIED).
- **Red flags:** none found; hard to copy because it needs artist access.

### 10. HipHopDX (UPROXX Studios)
- **Handles and followers:** IG @hiphopdx 901K, bio "The No. 1 Source for Hip-Hop News from @uproxx" (IG). X @HipHopDX 1,018,684, not verified (FX). TikTok @hiphopdx 3.3M followers, 72.2M likes; @hiphopdx.uk 855.3K followers, 31.6M likes; @hiphopdx.asia 369.8K; @hiphopdx.ger 41.6K (all TS).
- **Ownership:** Warner Music Group sold Uproxx, HipHopDX and Dime to UPROXX Studios (will.i.am, Jarret Myer, Rich Antoniello) on 24 Apr 2024 (https://www.digitalmusicnews.com/2024/04/24/warner-music-sells-uproxx-hiphopdx-dime-magazine/). hiphopdx.com now redirects (HTTP 302) to instagram.com/hiphopdx (checked 7 Oct 2026). WP lists the site as inactive.
- **Frequency:** IG 12 posts from 29 Sep to 6 Oct, about 1.5 a day (IG, calc).
- **Content mix:** every recent IG grid post is a collab with @uproxx or @jeremy_hecht; 4 of 12 labelled "Twitter screenshot" (IG).
- **Originates or aggregates:** now mainly aggregates (no website).
- **Speed:** no independent source found.
- **Signature formats:** tweet-card reels co-posted with UPROXX; TikTok news clips (layout: verify).
- **Examples:** https://www.instagram.com/reel/DeLEYCcJn7h/ ; https://www.instagram.com/reel/DeF0QCiNjks/
- **Red flags:** website closed; brand reduced to co-posts; X not verified. Still worth studying for the UK TikTok account.

### 11. Pop Crave
- **Handles and followers:** X @PopCrave 7,959,167, joined 9 Dec 2015, 161,542 posts (FX); WP lists 6.6M as of 7 Aug 2026. IG @popcrave 282K (IG). TikTok @popcrave 40.3K; 168 videos in the window; 86K average views (SP).
- **Background (WP):** founded December 2015 by Will Cosme, Miami.
- **Frequency:** 20 X posts in about 20 hours (FX), about 24 a day (calc).
- **Content mix:** X text plus photos or video; music, film, TV, celebrity.
- **Originates or aggregates:** mainly aggregates; website carries longer stories and interviews (WP).
- **Speed:** no independent source; observed about 24 posts a day.
- **Signature formats:** format leader F.
- **Examples:** https://x.com/PopCrave/status/2107770122303615302 ; https://x.com/PopCrave/status/2107576144954585107 ; https://x.com/PopCrave/status/2107682329640783903
- **Red flags:** WP: Pop Crave and Pop Base have both had viral misinformation incidents and rank among the Top 200 most community-noted accounts on X; a parody account "Poo Crave" has caused confusion.

### 12. Chart Data
- **Handles and followers:** X @chartdata 6,157,876, joined 18 Jun 2016, 158,640 posts, bio "music charts, awards, industry news and more in real time", site chartdata.org (FX). IG @chartdata is a 572-follower, unverified account with different bio wording; not confirmed as theirs (IG). TikTok: UNVERIFIED.
- **Frequency:** 20 posts in 8 hours on 6 Oct 2026 (FX); lifetime average about 42 a day (calc).
- **Content mix:** one data line plus cover art or text only (FX).
- **Originates or aggregates:** aggregates chart data and cites sources ("via @HITSDD").
- **Speed:** no independent source; observed posting within the chart-release window.
- **Signature formats:** format leader G.
- **Examples:** https://x.com/chartdata/status/2107585247030485439 ; https://x.com/chartdata/status/2107577685119504515 ; https://x.com/chartdata/status/2107490929242460227
- **Red flags:** effectively X-only; Instagram handle not theirs.

### 13. DailyRapFacts
- **Handles and followers:** X @DailyRapFacts 3,990,913, joined 18 Jan 2014, 13,455 posts, location Atlanta (FX). IG @dailyrapfacts 43.1K, not verified (IG). TikTok: UNVERIFIED.
- **Frequency:** 20 X posts over 11 days, about 2 a day (FX, calc).
- **Content mix:** text plus 1 or 2 photos or video (FX).
- **Originates or aggregates:** aggregates.
- **Speed:** no independent source found.
- **Signature formats:** format leader H.
- **Examples:** https://x.com/DailyRapFacts/status/2104229773463486669 ; https://x.com/DailyRapFacts/status/2103309501893861485 ; https://x.com/DailyRapFacts/status/2105658770236027294
- **Red flags:** none found; posting rate is low now.

### 14. Pop Base
- **Handles and followers:** X @PopBase 7,502,800, joined 11 Jun 2019, 96,019 posts (FX). WP: 2M on X in May 2025 and 6.9M as of 27 Aug 2026. IG @popbase 386K (IG). TikTok @popbase 68K (WP).
- **Frequency:** X lifetime average about 36 a day (calc). Timeline not retrieved (FX 404).
- **Content mix and format:** short, headline-driven updates (WP). Post-level layout: UNVERIFIED.
- **Originates or aggregates:** aggregates; operator anonymous (WP).
- **Examples:** none retrieved (UNVERIFIED).
- **Red flags:** misinformation incidents and heavy community-noting (WP); a 2024 Forbes piece cited by WP raised confusion when parody or stylised content resembles news.

### 15. Hot Freestyle
- **Handles and followers:** IG @hotfreestyle 3.7M, verified, bio "Hip Hop, Sports & Entertainment", links @hotfreestylerecords and @miccheckhq (IG). X @HotFreestyle 522,875, following 52 (FX). TikTok: UNVERIFIED.
- **Frequency:** X 20 posts over 19 days, about 1 a day (FX, calc); IG about 3 a day in the visible grid (IG).
- **Content mix:** IG last 12: 10 clips, 2 carousels; 4 labelled "Twitter screenshot" (IG).
- **Originates or aggregates:** aggregates viral clips.
- **Signature formats:** viral clip with a one-line caption and emoji ("Drake called BenDaDonnn to troll him about his recent arrest 😂", FX); tweet-card reels on IG.
- **Examples:** https://www.instagram.com/reel/DeK84QSMTTh/ ; https://www.instagram.com/reel/DeJGHJigQZi/ ; https://x.com/HotFreestyle/status/2107614441021800692
- **Red flags:** none found.

### 16. WorldStarHipHop
- **Handles and followers:** IG @worldstar 43.5M (IG). X @WORLDSTAR 5,203,883, joined 6 Jan 2008 (FX). TikTok @worldstar 13.6M followers, 534.1M likes (TS). YouTube 28M (SRJ top-100 list, 7 Oct 2026).
- **Background (WP):** founded 2005 by Lee "Q" O'Denat; current owner MediaLab AI Inc.
- **Frequency:** X 20 posts over 7 days, about 3 a day (FX, calc).
- **Content mix:** X short headline plus single photo; crime, celebrity, viral; IG clips and images.
- **Originates or aggregates:** aggregates.
- **Examples:** https://x.com/WORLDSTAR/status/2105652318410850470 ; https://x.com/WORLDSTAR/status/2107508975575167132
- **Red flags:** long history of shock and fight videos (WP); sexualised "eye candy" posts in the current X feed (the X bio itself mentions "Eye Candy"). Brand-safety risk next to a client's song.

### 17. Bars (Low Battery)
- **Handles and followers:** IG @bars 2.4M, verified, bio "The Next Generation of Hip Hop 💽 By @lowbattery" (IG). TikTok @bars 2.14M; 732 videos in the window; 286K average views; top post 6.71M views (SP).
- **Frequency:** TikTok about 2 a day (SP, calc).
- **Content mix:** clips and carousels (IG).
- **Originates or aggregates:** originates series content.
- **Signature formats:** named series (see section 3).
- **Examples:** none retrieved (UNVERIFIED).
- **Red flags:** none found.

### 18. MyMixtapez
- **Handles and followers:** IG @mymixtapez 1.7M, verified, bio "Hip-Hop. Culture. What's Trending. 🔥 Breaking news, music & viral moments. DM for Promo" (IG). X @mymixtapez 1,047,645, following 11 (FX). TikTok: UNVERIFIED.
- **Frequency:** all 12 visible IG posts dated 6 Oct 2026 (IG).
- **Content mix:** IG last 12: 11 carousels, 1 photo (IG).
- **Originates or aggregates:** aggregates (also a mixtape app, per X bio).
- **Examples:** https://www.instagram.com/p/DeLdyXuG3ZR/ ; https://www.instagram.com/p/DeKnR20Sp6N/
- **Red flags:** none found.

### 19. DJ Akademiks
- **Handles and followers:** IG @akademiks 5.1M, verified, bio "Official Hip Hop / News Page for AkademiksTV ... Charts @chartdemiks" (IG). X @Akademiks: 1.6M per CX26 (May 2026), but the handle did not resolve on 7 Oct 2026 (FX 404), status UNVERIFIED. X @AkademiksTV 278,856, "Official News/Updates Channel for The Akademy" (FX). TikTok @akademiks 683.4K followers, 10.3M likes (TS). YouTube: DJ Akademiks 2.83M and King Akademiks 1.01M (WP, 21 Mar 2026).
- **Frequency:** IG about 8 posts on 6 Oct (IG).
- **Content mix:** IG last 12: 9 clips, 1 photo ("Twitter screenshot"), 2 carousels (IG).
- **Originates or aggregates:** originates commentary and streams; the IG news page aggregates.
- **Speed:** CX26 ranks him #1 overall (influence, not speed).
- **Examples:** https://www.instagram.com/reel/DeLc-FOtJiR/ ; https://www.instagram.com/p/DeKQdxTgEC7/
- **Red flags:** Twitch ban in January 2025 after sexually explicit questions to a 15-year-old streamer (WP); 2024 New Jersey lawsuit alleging rape, sexual assault and defamation, unresolved per WP; main X handle unresolved; lookalike @DJAKADEMIKS on X is a different DJ (4,509 followers, FX); @theakademytv on IG is private (12K, IG).

### 20. Our Generation Music (OGM)
- **Handles and followers:** IG @ourgenerationmusic 870K, verified, bio "Hip-Hop News, Music & Culture updates 🔰", link to ourgenerationmusic.be (IG). TikTok @ourgenerationmusic 314.2K followers, 31.4M likes (TS). X: handle not found (UNVERIFIED).
- **Frequency:** IG about 8 posts on 6 Oct (IG).
- **Content mix:** IG last 11: 9 carousels, 1 clip ("Twitter screenshot"), 1 photo; highlights SOUNDCHECK, PROD. BY, OGM INTERVIEWS (IG).
- **Originates or aggregates:** aggregates news and originates interviews.
- **Examples:** https://www.instagram.com/p/DeLqB2oFDxs/ ; https://www.tiktok.com/@ourgenerationmusic/video/7610601970046405918 ; https://www.tiktok.com/@ourgenerationmusic/video/7303808723586141486
- **Red flags:** none found.

### 21. Underground Sound
- **Handles and followers:** IG @undergroundsound 274K, verified, name "Underground Sound | Daily Music Posts", bio "For artists, by artists", links to UK branch @undergroundsound.uk and @ugsarchive (IG). CX26 (May 2026): 255K IG, 93.4K X, 48.4K TikTok, ranked #31 as the largest underground rap page. X and TikTok handles: UNVERIFIED.
- **Frequency:** IG about 8 posts on 6 Oct (IG).
- **Content mix:** IG last 12: 4 clips, 4 photos (1 "Twitter screenshot"), 4 carousels (IG).
- **Originates or aggregates:** curates and aggregates underground releases.
- **Examples:** https://www.instagram.com/p/DeHzZx7C_Th/ ; https://www.instagram.com/reel/DeKlEXgC5LE/
- **Red flags:** none found.

### 22. Lyrical Lemonade
- **Handles and followers:** IG @lyricalemonade 4.8M (IG). X @LyricaLemonade 1,281,079 (FX). TikTok @lyricalemonade 2.00M; 754 videos in the window; 98.8K average views; top video 6.11M views (SP). YouTube 24M (SRJ top-100 list, 7 Oct 2026).
- **Content:** freestyle performances and music content (SP). Not a news page.
- **Originates or aggregates:** originates.
- **Examples:** none retrieved (UNVERIFIED).
- **Red flags:** handle spelling traps: IG @lyricallemonade is a 361-follower placeholder pointing to @lyricalemonade (IG).

### 23. RapMusic
- **Handles and followers:** IG @rapmusic 5M, no verification badge shown, bio "🥇 The #1 Rap Community / 🎙 Hip-Hop News & Videos / ... DM for credit/removal" (IG). TikTok: not found (UNVERIFIED).
- **Frequency:** about 9 IG posts on 6 Oct (IG).
- **Content mix:** IG last 12: 9 clips, 2 carousels, 1 photo; alt-texts include "meme of text" and 2 "Twitter screenshot" (IG).
- **Originates or aggregates:** aggregates.
- **Examples:** https://www.instagram.com/reel/DeIvAbcNZDl/ ; https://www.instagram.com/reel/DeJ8u9mBoqi/
- **Red flags:** unverified page, owner unknown.

### 24. Billboard
- **Handles and followers:** IG @billboard 17.5M, links to @billboardhiphop and @billboardcharts (IG). X @billboard 16,825,590 (FX).
- **Content:** magazine covers, chart carousels, clips (IG).
- **Role:** primary source for chart facts that Chart Data, Pop Crave and RapTV repost.
- **Red flags:** none found.

### 25. No Jumper
- **Handles and followers:** YouTube @nojumper 4.98M subscribers, 10,134 videos, 6 uploads on 1 Oct 2026 (SRJ, 1 Oct 2026). X @nojumper 1,421,354, bio "Coolest Podcast In The World. Hosted by @adam22" (FX). TikTok @nojumper 2.3M followers, 109.2M likes (TS). Instagram: taken down, per host Adam22 in April 2025 (WP, https://en.wikipedia.org/wiki/No_Jumper); the profile page returned no account on 7 Oct 2026.
- **Content:** podcast and interview clips. Originates.
- **Red flags:** Instagram removed; February 2025 meme-coin launch that a crypto journalist described as a pump-and-dump (WP); lawsuit by former employees (WP).

---

## 5. Fast-growing and newer pages (2025 to 2026)

Only growth I could date is listed.

| Page | Earlier figure | Now (7 Oct 2026) | Note |
|---|---|---|---|
| Pop Base | X 2M, May 2025 (WP) | X 7,502,800 (FX) | Largest verified jump in this set |
| Kurrco | X 385.5K, IG 19.5K, 5 May 2026 (CX26) | X 442,198 (FX), IG 26.7K (IG) | Founded July 2021; profiled by Complex July 2026 |
| Underground Sound | IG 255K, May 2026 (CX26) | IG 274K (IG) | UK branch @undergroundsound.uk |
| Daily Loud | X 376,296, 13 Jan 2022 (SpeakRJ) | X 6,918,714 (FX) | Older account; see red flags |
| Bars and Pop Hive (Low Battery) | No earlier dated figure | Bars IG 2.4M, TikTok 2.14M; Pop Hive IG 706K, TikTok 68.4K (IG, SP) | Network brands launched alongside RapTV; growth rate UNVERIFIED |

I could not find a dated, sourced list of new 2025 to 2026 TikTok-native rap news pages before the search budget ran out. "Masked Mortal" (TikTok @themaskedmortal, 3.9M in January 2023 per https://ubiquitousinfluence.com/post/rap-creators-2023) is a hip-hop news creator whose current status is UNVERIFIED.

---

## 6. Also checked (not ranked)

| Page | Handle and figure (source) | Why not ranked |
|---|---|---|
| Pop Hive (Low Battery) | IG @pophive 706K (IG); TikTok 68.4K, 1.41K videos in window, 61.4K average views (SP) | Pop culture, not rap. Same network as RapTV |
| Hollywood Unlocked | IG @hollywoodunlocked 4.1M, bio "The Pulse of Pop Culture and Politics" (IG) | Celebrity and politics |
| The Neighborhood Talk | IG @theneighborhoodtalk 2.5M, bio "Owned By: @Kyle.Anfernee" (IG) | Celebrity gossip |
| HipHopNation | IG @hiphopnation 209K, bio "The Sound of the Culture is Hip-Hop Nation on @siriusxm" (IG) | SiriusXM radio channel page, not a news page. No independent "Hip Hop Nation" news page was found |
| @hiphop | IG 354,266, data refreshed 2 Oct 2026 (https://creatordb.app/creatorstats/hiphop/) | Inactive for several months per CreatorDB |
| Rap Radar | X @RapRadar 179,233, not verified (FX) | Activity not checked |
| Pop Tingz | X @PopTingz 359,151 (FX) | Pop culture |
| AkademiksTV | X @AkademiksTV 278,856 (FX) | Feeder account for DJ Akademiks |
| VladTV | YouTube 6.3M (CX26, May 2026) | Long interviews |
| Trap City | YouTube 14M (SRJ top-100 list) | Music promotion channel, not news |
| Masked Mortal | TikTok @themaskedmortal, 3.9M in Jan 2023 | Current status UNVERIFIED; IG @themaskedmortal is a private 1-follower account |
| Rap Alert | X @RapAlert is an unrelated 23-follower account (FX); IG @rapalert returned no profile | No active "Rap Alert" news page could be verified. UNVERIFIED |

---

## 7. Dead, changed, lookalike or unverified handles

| Handle | Platform | Status on 7 Oct 2026 | Source |
|---|---|---|---|
| @raptvcom | X | Old RapTV handle, now an unrelated 16-follower account | FX; KYM shows it was RapTV's in 2022 |
| @raptv | Instagram | Unrelated account "Verse", 147 followers | IG |
| @raptv | YouTube | Unrelated channel "Raptv Shampel" | youtube.com/@raptv |
| @RappTvcum | X | Self-declared RapTV parody, 1,979 followers | FX |
| @kurrco | Instagram | Unrelated private user "Carlos Andres", 163 followers. Real page: @kurrco.xyz | IG |
| @lyricallemonade | Instagram | 361-follower placeholder. Real page: @lyricalemonade | IG |
| @LyricalLemonade | X | Not found. Real handle: @LyricaLemonade | FX |
| @Akademiks | X | Did not resolve (404). Was 1.6M in May 2026 | FX, CX26 |
| @DJAKADEMIKS | X | A different DJ (WPGC radio), 4,509 followers | FX |
| @theakademytv | Instagram | Private, 12K | IG |
| @Saycheesetv1 | X | Lookalike, 389 followers, not verified | FX |
| @nojumper | Instagram | Taken down (April 2025) | WP, IG |
| hiphopdx.com | Web | Redirects to instagram.com/hiphopdx | Direct check |
| @chartdata | Instagram | 572 followers, not verified, not confirmed as Chart Data | IG |
| @hiphop | Instagram | Inactive for months | CreatorDB |
| @RapAlert | X | Unrelated, 23 followers | FX |
| @themaskedmortal | Instagram | Private, 1 follower | IG |

Not checked because of the search and fetch limits: TikTok follower counts for Kurrco, Hot Freestyle, MyMixtapez, Chart Data, DailyRapFacts and RapMusic; YouTube counts for RapTV, Daily Loud, XXL, Complex and HotNewHipHop; X timelines for Daily Loud, Pop Base, XXL, HipHopDX and HotNewHipHop; example posts for Genius, Pop Base, Bars and Lyrical Lemonade; on-screen TikTok layouts for every page.

---

## 8. Sources

Live profile data (7 Oct 2026):
- Instagram profiles: `https://www.instagram.com/<handle>/` for rap, raptv, bars, pophive, daily_loud, saycheesetv, hiphopdx, xxl, complex, complexmusic, hotnewhiphop, popbase, popcrave, theshaderoom, genius, lyricalemonade, lyricallemonade, worldstar, akademiks, theakademytv, hiphopnation, ourgenerationmusic, mymixtapez, hotfreestyle, rapmusic, undergroundsound, kurrco, kurrco.xyz, dailyrapfacts, chartdata, billboard, hollywoodunlocked, theneighborhoodtalk, themaskedmortal, nojumper, rapalert.
- Instagram posts quoted: https://www.instagram.com/p/DeLu1h_FvcQ/ ; https://www.instagram.com/p/DeKTn_JScMO/ ; https://www.instagram.com/reel/DeICS09p_aM/ ; https://www.instagram.com/p/DeMaw86ESiT/
- X profiles: `https://api.fxtwitter.com/<handle>` for Rap, Kurrco, DailyLoud, SaycheeseDGTL, nojumper, HipHopDX, XXL, ComplexMusic, HotNewHipHop, PopBase, PopCrave, TheShadeRoom, Genius, LyricaLemonade, WORLDSTAR, AkademiksTV, Akademiks, chartdata, HotFreestyle, mymixtapez, DailyRapFacts, PopTingz, RapAlert, RapRadar, RappTvcum, Saycheesetv1, DJAKADEMIKS, raptvcom, billboard.
- X timelines: `https://api.fxtwitter.com/2/profile/<handle>/statuses` for Kurrco, Rap, PopCrave, chartdata, HotFreestyle, SaycheeseDGTL, DailyRapFacts, WORLDSTAR.
- TikTok (SP): https://socialpruf.com/tiktok/rap ; /theshaderoom ; /genius ; /complex ; /xxl ; /lyricalemonade ; /popcrave ; /bars ; /pophive
- YouTube (SRJ): https://www.speakrj.com/audit/top/youtube/100/hip_hop_music ; https://www.speakrj.com/audit/report/UCNNTZgxNQuBrhbO0VrG8woA/youtube ; https://www.speakrj.com/audit/report/saycheesetv/youtube
- Other: https://linktr.ee/kurrco ; https://raptv.com/workwithus/ ; https://creatordb.app/creatorstats/hiphop/ ; https://www.speakrj.com/audit/report/DailyLoud/twitter

Articles and references:
- Complex, "Who Is Kurrco? Inside the Anonymous Account Running Rap Twitter", 17 Jul 2026: https://www.complex.com/music/a/dimassanfiorenzo/kurrco-identity-who-runs-rap-twitter
- Complex, "Hip-Hop Media Power Ranking (The 2026 Edition)", 5 May 2026: https://www.complex.com/music/a/dimassanfiorenzo/hip-hop-media-power-ranking-2026-edition
- Complex, reactions to the 2026 ranking, 7 May 2026: https://www.complex.com/music/a/tracewilliamcowen/complex-hip-hop-media-power-ranking-reactions
- Complex, "Hip-Hop Media Power Ranking (2025)", 24 Jul 2025 (no aggregator pages ranked): https://www.complex.com/music/a/dimassanfiorenzo/hip-hop-media-power-ranking-2025
- Know Your Meme, "RapTV / @Rap": https://knowyourmeme.com/memes/sites/raptv-rap
- RapTV template generator and README: https://yimmyj.github.io/RapTVTemplate/ ; https://github.com/yimmyj/RapTVTemplate
- Digital Music News, WMG sells Uproxx, HipHopDX and Dime, 24 Apr 2024: https://www.digitalmusicnews.com/2024/04/24/warner-music-sells-uproxx-hiphopdx-dime-magazine/
- Wikipedia: https://en.wikipedia.org/wiki/Pop_Base ; https://en.wikipedia.org/wiki/Pop_Crave ; https://en.wikipedia.org/wiki/The_Shade_Room ; https://en.wikipedia.org/wiki/WorldStarHipHop ; https://en.wikipedia.org/wiki/HipHopDX ; https://en.wikipedia.org/wiki/DJ_Akademiks ; https://en.wikipedia.org/wiki/No_Jumper
- Ubiquitous Influence, "The Top 7 Rap Creators on TikTok in 2023", 25 Jan 2023: https://ubiquitousinfluence.com/post/rap-creators-2023
- YouTube fan wiki (RapTV subscriber snippet only; page returned HTTP 402 when fetched): https://youtube.fandom.com/wiki/RapTV
