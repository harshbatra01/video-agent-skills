# 16. Transplant mechanics: proven faceless formats from other niches, adapted for Outcome

Prepared 13 Oct 2026 for Vision Clipping (Outcome faceless pages). Companion files in this folder: 00-client-brief.md, 01-what-is-outcome.md, 02-reference-posts.md, 03-platform-rules.md. All counts were read on 13 Oct 2026 and will have moved.

Short version. 29 mechanics. 26 have verified examples (TikTok through tikwm, YouTube through watch pages; two of those, #7 and #18, are negative or weak evidence). 3 have no verified faceless example (#13, #19, #23). The pattern that repeats: small accounts (3K to 60K followers) keep getting 2M to 30M plays on formats that hide an answer for a few seconds and make the viewer commit (pick, guess, score). The pattern that fails: football stat duels (higher or lower), "if you invested" posts, text-only POV posts.

## 1. Top 10 transplants, ranked by expected performance for a new faceless page

How I ranked: reach of small accounts (plays per follower in the verified examples), how many independent accounts repeat it, share and comment rates, fit with data Outcome already has, build effort, and risk under the brief and 03-platform-rules.md. Ranks 1 to 3 are the ones to test first.

| Rank | Mechanic (entry) | Proof for small or new pages (verified 13 Oct 2026) | Outcome version (draft) | Effort | Risk |
|---|---|---|---|---|---|
| 1 | Pick a side, crowd split (#10) | 6 accounts of 14K to 185K followers each have a post at 3.8M to 7.5M plays. Shares are 2.3% to 8.2% of plays, the highest share rates in this study. One account (@learnchoice00) has 12 posts above 500K plays from Oct 2025 to Aug 2026 in the hashtag feeds. | "Which side?" poll on real markets, the crowd percent revealed last (Man City v PSG, Roma v Real Madrid, Ballon d'Or) | Low | Medium |
| 2 | Guess the favourite, football quiz round (#1) | @brainquizmania (112K followers) had three posts in 8 days at 10.2M, 5.3M and 4.6M plays. YouTube Short "Guess The Madrid Player!" has 15.0M views on a 464K-sub channel. | 5 rounds from the UCL card: "which result does the crowd rate highest?" | Low | Low |
| 3 | Carousel quiz, "can you get 6/6?" with Part N numbering (#2 and #29) | @hiddengemz111 (22.2K followers): 29.6M plays on a 7-slide photo post, "Part 85". @quizdz1 (56K): 6.3M plays on a 7-slide football logo post. | 7-slide quiz where each slide hides the crowd percent, answers on the last slide. Same files work as an Instagram carousel. | Low | Low |
| 4 | AI vs the crowd (#24) | YouTube: a channel with 2.03K subs got 4.85M views; a 30K-sub channel got 2.83M, 1.75M and 1.08M in three posts from 12 Aug to 4 Sep 2026. | AI's picks for tomorrow's matches next to the crowd's favourites, disagreements marked | Low | Medium |
| 5 | Chance race, bar chart race of a market (#14) | @hai02a (112.5K followers): 18.8M plays, plus 2.2M and 1.7M. @zain02a (4.4K followers): 2.2M plays. | Bars race through the daily price history of the Champions League winner market since 4 Sep | Medium | Low |
| 6 | Crowd tier list (#16) | @sammyshakiry (238K): 6.0M and 3.9M plays. @tier.list.everything (58.8K): 2.0M plays and an 11.8% like rate. | S to C tiers filled from the crowd's percentages (EPL winner, Ballon d'Or) | Low | Low |
| 7 | Timed reveal, 12-second clip (#5) | @spot.the.differan (3.6K followers): 4.5M plays on a 12 s clip. @guess.the.flag08 (17.4K): 2.2M plays on 12 s. | 10-second "call it" clips, and a countdown to a real settlement time (S&P 500 20:00 UTC) | Low | Medium |
| 8 | Map of chances (#15) | @geo.all.day (245K): 10.5M plays, 4.0% shares. @geotok (58.1K): 8.3M plays. | Europe map coloured by each country's summed Champions League title chance | Medium | Low |
| 9 | Race animation (#26) | @marbledecide (255K): 41.9M and 21.3M plays. @mevvomarbles (251K): 11.1M. | Named marbles for the title favourites, labelled "animation, not a forecast" | High | Medium to high |
| 10 | Animal oracle (#25) | @keesenronnie (5.6K followers): 1.23M and 0.87M plays on 13 s to 27 s match picks. | A pet or mascot picks the winner, the crowd percent follows, the result follows | Medium | Low |

Next five if the first ten saturate: Choose a door (#11), Guess the price in cents (#6), Missing-percent puzzle (#3), Trader or market story shorts (#21), Real or fake market quiz (#8).

Hold, do not build yet: Higher or lower stat duels (#7, no faceless hit found), Time machine (#18, weak and risky), Wealth scale (#17, risk), Satisfying payout counters (#20, risk), POV memes (#23, unverified), Live ticker (#19, unverified), Comment-to-decide (#13, no faceless proof).

### How to read this file

- VERIFIED means I re-fetched that exact post on 13 Oct 2026: TikTok through tikwm.com's video endpoint, follower counts through the r.jina.ai reader on the profile; YouTube through the public watch page (views, upload date, channel subscribers). Anything else says UNVERIFIED or "feed only" (seen in a hashtag feed, not re-fetched).
- "x followers" is plays divided by the account's followers on 13 Oct 2026. It is a rough reach multiplier, not a promise.
- I did not watch any video or open any image (rules of this job). "Faceless" is judged from the format, account name and caption, so confirm by eye before cloning. Layout lines marked (typical) describe how the format is normally built; what I did read from data is the duration, slide count, music title, caption and hashtags.
- Discovery route. Direct TikTok is blocked on this PC. tikwm's search and user endpoints answered with a Cloudflare challenge on both GET and POST, so I found posts through tikwm hashtag feeds (about 100 hashtags, 3 to 4 pages of 30 posts each), YouTube search pages and web search, then verified each post one by one.
- Instagram. View counts are hidden from logged-out readers, the public profile JSON returned HTTP 401, and the embed pages came back as an empty shell. So there are no Instagram post-level numbers here. Instagram evidence is platform-level (Metricool and Buffer studies) plus three profile pointers in section 4.
- Ages. Posts older than 2024 are marked "outside the window".

### Outcome data used in the drafts (snapshot S1)

Read 13 Oct 2026 about 00:59 UTC from the public Hyperliquid info API (outcomeMeta and allMids; Outcome's own deployer markets). These are mid prices of each Yes book, so thin books can be off and a market's sides can add to more than 100. The site shows its own number: match it on screen before filming, and re-pull at post time. Volumes are from Outcome's home page on 13 Oct (file 01, section 4.3).

Champions League, matchday 2 (home / draw / away chance, %). Kick-off times UTC.

| 13 Oct | Home | Draw | Away |
|---|---|---|---|
| 16:45 RC Lens v Sporting CP | 37.9 | 25.4 | 36.7 |
| 16:45 Sabah Baku v Slavia Praha | 27.4 | 25.2 | 47.4 |
| 19:00 Galatasaray v Barcelona | 10.2 | 12.9 | 76.7 |
| 19:00 Arsenal v Lille | 80.3 | 13.6 | 6.3 |
| 19:00 Atletico Madrid v Man Utd | 51.0 | 24.1 | 25.1 |
| 19:00 Inter v Club Brugge | 77.6 | 14.4 | 7.7 |
| 19:00 Viking v Bayern Munich | 4.2 | 6.7 | 89.3 |
| 19:00 Villarreal v Napoli | 45.3 | 25.5 | 29.0 |
| 19:00 RB Leipzig v PSV | 55.8 | 20.0 | 24.1 |

| 14 Oct | Home | Draw | Away |
|---|---|---|---|
| 16:45 LASK v Liverpool | 9.7 | 14.5 | 76.0 |
| 16:45 Feyenoord v Como | 27.2 | 23.0 | 50.0 |
| 19:00 Man City v PSG | 44.6 | 23.2 | 32.0 |
| 19:00 AS Roma v Real Madrid | 25.9 | 23.5 | 50.8 |
| 19:00 Aston Villa v Fenerbahce | 59.1 | 22.4 | 18.5 |
| 19:00 Bodo/Glimt v Dortmund | 29.5 | 23.1 | 47.4 |
| 19:00 Slovan Bratislava v Stuttgart | 9.2 | 14.8 | 76.2 |
| 19:00 Shakhtar v AEK Athens | 36.0 | 28.0 | 35.8 |
| 19:00 Real Betis v Porto | 47.7 | 24.8 | 27.4 |

Season markets (leaders only): Champions League winner 2026/27 (volume $2.4M): Barcelona 22.8, Bayern 14.3, Arsenal 13.3, PSG 12.8, Real Madrid 11.0, Man City 6.7. Premier League winner (volume $2.2M): Arsenal 59.9, Man City 19.9, Chelsea 7.5, Liverpool 5.6, Spurs 2.9, Man Utd 1.7. Ballon d'Or 2026 (volume $554.2k): Kane 65.6, Yamal 28.6, Messi 3.2, Dembele 2.5, Mbappe 2.2, Bellingham 0.8, Haaland 0.8. NFL 2027 winner (volume $2.0M): Rams 11.4, Bills 10.0, Chiefs 9.6, Seahawks 9.0, Ravens 8.7, Cowboys 2.4. Fed decision in October (volume $894.1k): no change 81.0, increase 17.9, decrease 0.4.

Daily price markets (13 Oct): WTI crude above 92.386 at 21:00 UTC, 42.8 YES. Gold above 4,174 at 21:00 UTC, 31.4. Silver above 60.347 at 21:00 UTC, 34.5. S&P 500 above 7,805.7 at 20:00 UTC, 36.4.

History exists. The same API's candleSnapshot works on outcome coins (coin is "#" plus outcome id times 10 plus side). Example: Barcelona Yes in the Champions League winner market has daily candles from 4 Sep 2026 (that day: open 13.6, close 17.5) and sits at 22.8 now. That is what makes a chance race, a "how the crowd changed its mind" post and a "guess the chart" quiz possible without screenshots.

Leaderboard facts (file 01, section 5): last-24h list on 12 Oct: trader-W +$16,838.68, trader-P +$5,982.82, trader-B +$3,710.73. All-time #1 trader-J +$503,008.19 from 2 trades (an outlier, never typical). Naming a real user needs the client's written OK.

### Rules applied to every draft

Plug line: "On outcome.xyz, traders predict ___ will happen with a __% chance." Never the banned gambling words from the brief. No profit promises: show only numbers the app shows, as past or live prices, with "not financial advice, do your own research" on finance topics. Our own graphics may use Outcome's data, but if a real Outcome screenshot is used, never cover the graph, names, logo or buy buttons. The CTA line in the brief ("Trade with zero fees on Outcome.xyz") is flagged in file 01 as not accurate, so use the client-approved fee wording. Check 03-platform-rules.md before posting: TikTok, Meta and YouTube each restrict this category.

---

## 2. All mechanics

Evidence grades. A = three or more verified examples at 1M+ plays or views including a small account. B = one or two verified examples, or YouTube only, or doubt about the faceless status. C = weak, negative, or UNVERIFIED.

### Group A. Quizzes and "guess the X"

#### 1. Guess the favourite (football quiz round). Origin: football quiz pages. Grade A

Looks like (typical): 60 s vertical video, 4 to 6 rounds. Each round shows a clue (hidden face, famous goal, transfer path, an "imposter" among four), a 3 to 5 s think pause with a ticking bar, then an answer flash. Ends with "comment your score". One music bed all the way; the verified posts use a library track called "midnight sun". Caption pattern: "Guess the imposter player #quiz #football #footballquiz". The YouTube versions are single-round clips of 10 to 35 s.

Examples (VERIFIED):
- TikTok @brainquizmania (112.1K followers), 20 Mar 2025, 60 s: 10.18M plays, 492K likes (4.8%), 6.1K comments, 131K shares (1.29%), 34.6K saves. 91x followers. https://www.tiktok.com/@brainquizmania/video/7483922562028703007
- YouTube Short, Melodyclipz (464K subscribers), 16 Jul 2025, 10 s: 15.04M views, 127K likes. 32x subscribers. https://www.youtube.com/shorts/pMgzJYvj_tM
- YouTube Short, Blade Sports (1.62M subscribers), 27 Jun 2026, 19 s: 10.69M views. 6.6x subscribers. https://www.youtube.com/shorts/aTFMInokoEI

Why it works: curiosity gap (the answer is held back for seconds), ego and identity ("a real fan gets this"), a score that is easy to compare, and a challenge to send to a friend (shares 1.3% to 2.0% of plays on the three @brainquizmania posts; two of them are in section 6).

Outcome draft: "Guess the favourite", 5 rounds built from tomorrow's UCL card in S1. Round 1: Galatasaray v Barcelona, three buttons, "which result does the crowd on Outcome rate highest?", 4-second bar, reveal Barcelona 76.7, draw 12.9, Galatasaray 10.2. Round 3 is the trap: Atletico v Man Utd, Atletico 51.0, Man Utd 25.1, draw 24.1, "the draw is almost as likely as a United win". Last round is the close one: Man City v PSG, City 44.6, PSG 32.0, draw 23.2. End card "Your score? Think you can read the crowd?" then the plug: "On outcome.xyz, traders predict Barcelona will win with a 76.7% chance." Built from one API pull into an HTML template. Number the series by matchday (see #29). Effort low, risk low.

#### 2. Carousel quiz, "can you get 6/6?" Origin: logo and clue quizzes in TikTok photo mode and Instagram carousels. Grade A

Looks like: 7 photo slides. Slide 1 is the hook; slides 2 to 6 carry one clue each; the last slide gives the answers or asks for the score in the comments. Sound runs under the slides. Football and Premier League versions exist. A numbered caption ("Part 85") signals a series.

Examples (VERIFIED):
- TikTok @hiddengemz111 (22.2K followers), 1 Jan 2025, photo post, 7 slides: 29.57M plays, 392K likes (1.3%), 6.4K comments, 3.3K shares (0.01%), 23.2K saves. 1,332x followers. https://www.tiktok.com/@hiddengemz111/video/7454778025641610542
- TikTok @quizdz1 (56K followers), 29 Mar 2025, photo post, 7 slides: 6.35M plays, 114K likes (1.8%), 1.7K comments, 789 shares (0.01%), 4.2K saves. 113x followers. https://www.tiktok.com/@quizdz1/video/7487266852679355654
- TikTok @quizlax (1.2M followers), 27 Sep 2025, 71 s: 7.38M plays, 155K likes (2.1%), 1.3K comments, 6.9K shares (0.09%), 5.9K saves. 6.2x followers. https://www.tiktok.com/@quizlax/video/7554748533975371039

Why it works: ego and status bait, the swipe itself keeps people on the post, and the numbering turns a one-off into a habit (an audience that waits for Part 86). Platform support: Buffer (19 Mar 2026, 45M+ posts) puts Instagram carousels at a 6.9% median engagement rate against 3.3% for Reels; Metricool (16 Jun 2026, 24.4M Instagram posts) says carousels earn 9 times the saves of single images. On TikTok, Buffer's median is lower for photo posts (1.92% against 3.39% for video), so the wins above are about reach, not average engagement.

Outcome draft: "Can you get 6/6?" carousel, six slides each showing one market with the percent hidden: Premier League winner (Arsenal?), Ballon d'Or (Kane?), Fed decision in October (no change?), UCL winner (Barcelona?), Viking v Bayern (Bayern?), Atletico v Man Utd (draw?). Slide 7 gives the six crowd percentages from S1 (59.9, 65.6, 81.0, 22.8, 89.3, 24.1) and the plug. Do not write "only 1% get this": there is no real statistic behind it (the VC rule is never to fake stats). Same seven PNGs go to TikTok photo mode and Instagram, and a 20-second slideshow cut goes to Shorts. Effort low, risk low.

#### 3. Animated puzzle with answer reveal ("only 1% can solve this"). Origin: IQ and puzzle pages. Grade A for the format, C for fit

Looks like: a 3D or 2D animation of blocks, screws or paperclips, 60 s: a short setup, about 20 to 30 s of "think" time, then the solution plays. One puzzle per post, same template every day, captions "#iqtest #puzzle". Typical.

Examples (VERIFIED):
- TikTok @univea47 (567.7K followers), 2 Mar 2025, 62 s: 47.06M plays, 708K likes (1.5%), 22.1K comments, 12.9K shares (0.03%), 40.1K saves. 83x followers. https://www.tiktok.com/@univea47/video/7477197148061338926
- TikTok @puzzle0105 (634K followers), 4 Feb 2025, 61 s: 28.85M plays, 601K likes (2.1%), 1.3K comments, 10.0K shares (0.03%), 38.1K saves. 46x followers. https://www.tiktok.com/@puzzle0105/video/7467351429687119135
- YouTube Short, BellaHTP (41.3K subscribers), 8 Oct 2026, 22 s: 397K views, 1.5K likes. 9.6x subscribers. https://www.youtube.com/shorts/m0L7CPaLJ8E

Why it works: an open loop the viewer wants closed, ego, and arguing about the answer in the comments.

Outcome draft: "Missing percent puzzle". A three-way market must add to about 100, so show Galatasaray 10.2, draw 12.9, Barcelona "?" and let the viewer solve it (76.7). Then a harder one: Arsenal 80.3, Lille "?", draw 13.6 (6.3). This teaches how Outcome's percentages work in 15 seconds, which is the whole product pitch. The "1%" tagline stays out. Effort low, risk low, but the match to Outcome's audience is indirect.

#### 4. Self-scored trivia ("can you get 10/10?"). Origin: trivia and riddle pages. Grade A

Looks like (typical): 5 to 10 questions, three options each, a 5-second timer, green reveal, ends "comment your score". Runs 70 to 120 s.

Examples (VERIFIED):
- TikTok @factualquiz (752.9K followers), 12 Apr 2025, 116 s: 20.76M plays, 764K likes (3.7%), 7.2K comments, 32.1K shares (0.15%), 84.1K saves. 28x followers. https://www.tiktok.com/@factualquiz/video/7492526711179840799
- TikTok @brainfuel_360 (610.5K followers), 10 Aug 2025, 90 s: 8.05M plays, 577K likes (7.2%), 231K comments, 208K shares (2.58%), 35.8K saves. 13x followers. https://www.tiktok.com/@brainfuel_360/video/7536955066125716750
- TikTok @asadquize (578.1K followers), 16 Feb 2025, 120 s: 11.64M plays, 304K likes (2.6%), 5.9K comments, 28.9K shares (0.25%), 20.6K saves. 20x followers. https://www.tiktok.com/@asadquize/video/7472050044900805911

Why it works: the score becomes social currency, and the comment gate is built into the format. The @brainfuel_360 post is the proof: 231,074 comments is 2.9% of plays, and 2.6% of plays were shares.

Outcome draft: "Beat the crowd" scorecard, the day after the matches. Show the nine favourites from the 13 Oct card in S1 (Barcelona, Arsenal, Inter, Bayern, Atletico, Villarreal, Leipzig, Slavia Praha, RC Lens) and score the crowd: how many of the nine favourites actually won? That count is computed from the settled markets, not guessed, so leave the number blank in the template until they settle. Viewers score themselves too ("you vs the crowd"). Effort low, needs settled-market data, risk low.

#### 5. Tiny timed clips (5 to 12 seconds): flag, spot the difference, brain test. Origin: geography and spot-it pages. Grade A

Looks like: 12 s clip, a question, a 3-2-1 bar, the answer. The 5 s brain-test version is a single line of text and nothing else, built to loop. Sound is usually "original sound".

Examples (VERIFIED):
- TikTok @spot.the.differan (3,629 followers), 27 May 2025, 12 s: 4.53M plays, 44.5K likes (1.0%), 8.0K comments, 1.3K shares (0.03%), 2.3K saves. 1,248x followers. https://www.tiktok.com/@spot.the.differan/video/7509246936197680390
- TikTok @guess.the.flag08 (17.4K followers), 5 Jul 2026, 12 s: 2.24M plays, 37.4K likes (1.7%), 1.2K comments, 763 shares (0.03%), 2.3K saves. 129x followers. https://www.tiktok.com/@guess.the.flag08/video/7659057326271319316
- TikTok @sammy_picc01 (401.1K followers), 24 Jul 2026, 5 s: 4.65M plays, 47.7K likes (1.0%), 56.3K comments, 1.4K shares (0.03%), 4.0K saves. 12x followers. https://www.tiktok.com/@sammy_picc01/video/7666058113459506452

Why it works: urgency, almost no time cost, replays to check, and arguing in comments (the 5 s clip has 56,252 comments; the 8 s clip, in section 6, has 7.6% shares).

Outcome draft: "10-second call". Man City v PSG on screen, a 10-second bar, then Man City 44.6, draw 23.2, PSG 32.0 (S1). Second version uses the real clock: a countdown to a settlement time ("S&P 500 above 7,805.7 at 20:00 UTC, 36.4% YES at 00:59 UTC"), then a follow-up post with the settled result. Effort low, risk medium (price-direction content on TikTok; see 03-platform-rules.md).

#### 6. Guess the price. Origin: shopping, property and product pages. Grade B (faceless proof is thin)

Looks like: an object or house, four price options or a slider, a reveal, then the viewer's "how far off was I".

Examples (VERIFIED):
- TikTok @movewitharan (3,925 followers), 9 Oct 2026, 127 s: 359K plays, 29.8K likes (8.3%), 575 comments, 2.5K shares (0.70%), 3.4K saves. 91x followers. https://www.tiktok.com/@movewitharan/video/7694731859443453206
- TikTok @foundersinc (12.9K followers), 21 Oct 2025, 29 s: 5.37M plays, 114K likes (2.1%), 4.8K comments, 524 shares (0.01%), 6.3K saves. 417x followers. https://www.tiktok.com/@foundersinc/video/7563477240428629261
Context: #guesstheprice has 1.03B lifetime views and 19.9K creators (tikwm, 13 Oct), but most big posts are people reacting on camera (couples, founders), so the faceless version has less proof. @movewitharan is a property page at 3,925 followers.

Why it works: a price is a number everyone can anchor on, the reveal gap, and the ego of being close.

Outcome draft: on Outcome, the price of a Yes share in cents is the chance, so this mechanic fits the product literally. "Guess the price": "What does a Yes on Barcelona to win the Champions League cost, in cents?" Options 12c, 22.8c, 35c (S1 shows 22.8). Then "Arsenal to win the Premier League?" (59.9). State that prices are live mids and move. Effort low, risk low.

#### 7. Higher or lower duels. Origin: football stats and trivia. Grade C (negative finding)

Looks like: two players or items, the viewer says whether the second is higher or lower.

Examples (VERIFIED, all weak; two more in section 6):
- TikTok @footballjoe (765.3K followers), 2 Aug 2024, 44 s: 26.9K plays, 1.5K likes (5.5%), 2 comments, 4 shares (0.01%), 23 saves. 0.04x followers. https://www.tiktok.com/@footballjoe/video/7398519476775308576
- TikTok @transfermarkt (3.7M followers), 23 Oct 2023, 12 s: 56.5K plays, 6.3K likes (11.1%), 97 comments, 1 shares (0.00%), 134 saves. 0.02x followers. https://www.tiktok.com/@transfermarkt/video/7293083709962489120 [outside the 2024 to 2026 window]
- YouTube Short, Razzamataza (406K subscribers), 18 Feb 2024, 46 s: 139K views, 8.1K likes. 0.34x subscribers. https://www.youtube.com/shorts/iZXWc1q2htQ
Context: the @wearetheoverlap post is presenter-led (the caption names Carragher), so it is not faceless proof. #higherorlower has 60.3M lifetime views and 3,373 creators; #guesstheplayer, a quiz tag, has 14.4B lifetime views. I scanned 4 pages of the hashtag at a 400K-plays threshold since Jan 2025 and found none. On YouTube Shorts the "higher or lower" hits are two-person number-guessing games with faces (10M and 9.4M views, seen in search results, not re-fetched), not stat duels.

Why it should work but does not: it is a forced choice with a reveal, yet each round is small and the format has no stake or score. Big accounts get 27K plays on 765K followers (@footballjoe) or 56K on 3.7M (@transfermarkt, Oct 2023, outside the window).

Outcome draft: do not run it as its own series. Use it as one round inside #1: "Is Arsenal's title chance above or below 60%?" (59.9). Effort low, risk low.

#### 8. Real or AI test. Origin: AI image quizzes. Grade B

Looks like: 62 s, pairs of images, "how many did you get right?", answers at the end. Typical.

Examples (VERIFIED):
- TikTok @daifei.aesthetic (24.1K followers), 5 Oct 2025, 62 s: 4.91M plays, 180K likes (3.7%), 2.8K comments, 42.5K shares (0.86%), 9.3K saves. 204x followers. https://www.tiktok.com/@daifei.aesthetic/video/7557739530187525390
Context: YouTube has bigger "real vs AI" posts (15.1M and 10.1M views) but they come from channels with 12.9M and 4.9M subscribers and probably a face on camera, so I left them out as examples.

Why it works: ego (I can spot fakes), real stakes in an AI-saturated feed, and a score to compare.

Outcome draft: "Real market or made up?" Show four market titles, two real and two clearly invented for the quiz (and labelled as invented at the end). Real ones from the home page: "Anthropic First-Day > $1,750B" (volume $135.7k) and "FED Decision in October?" (volume $894.1k). It shows viewers that unusual markets exist. Never present invented titles as real markets after the reveal. Effort low, risk low.

#### 9. Guess the character or song (mystery reveal). Origin: fandom and music quiz pages. Grade B

Looks like: 62 to 78 s, a silhouette, a snippet or a zoomed crop, a reveal.

Examples (VERIFIED):
- TikTok @mmbasically_fan_clips (14K followers), 27 Jul 2026, 78 s: 1.28M plays, 108K likes (8.4%), 179 comments, 2.4K shares (0.19%), 5.3K saves. 91x followers. https://www.tiktok.com/@mmbasically_fan_clips/video/7667012392286489878
- TikTok @liuwu41 (1.1M followers), 12 Apr 2025, 65 s: 4.69M plays, 118K likes (2.5%), 8.9K comments, 60.6K shares (1.29%), 18.2K saves. 4.3x followers. https://www.tiktok.com/@liuwu41/video/7492456136671497502
- TikTok @siyi694 (147.2K followers), 29 Aug 2025, 62 s: 4.83M plays, 48.4K likes (1.0%), 4.5K comments, 3.5K shares (0.07%), 9.3K saves. 33x followers. https://www.tiktok.com/@siyi694/video/7543835564642962710

Why it works: a pure curiosity gap with a recognisable reward. The song versions rely on audio, which is the hook (1.3% shares on @liuwu41).

Outcome draft: "Guess the chart". Draw an unlabelled price line from the API history (Barcelona Yes in the Champions League winner market: 13.6 to 22.8 since 4 Sep, S1) and ask "which market is this?" with three options, then reveal the label. This uses our own chart, so there is no problem with covering Outcome's chart. Effort medium (needs history pull), risk low.

### Group B. Polls and choices

#### 10. Pick a side, "would you rather" and "this or that" (crowd split). Origin: poll and challenge pages. Grade A (strongest in the study)

Looks like: 60 to 64 s, two options (usually images), a countdown, then a percentage split revealed (typical). Caption "What would you rather? #wouldyourather #thisorthat #chooseone". Many posts per day, same template. "The internet's favourite" posts are this mechanic with a public result.

Examples (VERIFIED):
- TikTok @quentra (31.9K followers), 26 Jul 2026, 63 s: 7.46M plays, 469K likes (6.3%), 6.0K comments, 268K shares (3.58%), 34.1K saves. 234x followers. https://www.tiktok.com/@quentra/video/7666709272205593889
- TikTok @quick.pick000 (29.2K followers), 28 Sep 2026, 60 s: 6.18M plays, 413K likes (6.7%), 31.7K comments, 184K shares (2.99%), 17.3K saves. 212x followers. https://www.tiktok.com/@quick.pick000/video/7690592306969234702
- TikTok @chooseone_247 (14.1K followers), 7 Jul 2026, 64 s: 4.60M plays, 273K likes (5.9%), 1.6K comments, 107K shares (2.32%), 10.6K saves. 326x followers. https://www.tiktok.com/@chooseone_247/video/7659846538218294561

Why it works: a forced choice that says something about me (identity), disagreement in the comments (the @quick.pick000 post has 31,733), and a friend to send it to. The share rates (2.3% to 8.2% of plays across seven posts, four of them in section 6) are the highest in this study, which is what pushes it to strangers.

Outcome draft: "Which side?" reel, 3 rounds from S1. Round 1: Man City or PSG tonight? Bars grow to 44.6 and 32.0 (draw 23.2). Round 2: Roma or Real Madrid (25.9 / 50.8, draw 23.5). Round 3: Kane (65.6) or Yamal (28.6) for the 2026 Ballon d'Or. The reveal is labelled "what traders on Outcome say" and the closing line is the plug: "On outcome.xyz, traders predict Kane will win the 2026 Ballon d'Or with a 65.6% chance." Keep payouts and any call to trade out of the poll slides; the CTA sits only on the last card. Use matches and awards, not "will you buy". Effort low, risk medium (a poll next to a financial product).

#### 11. Choose a door (pick one of N). Origin: personality and luck tests on YouTube Shorts. Grade B (YouTube only)

Looks like: three doors or boxes, "which door are you picking?", a pause, then each door's contents. 59 to 65 s.

Examples (VERIFIED):
- YouTube Short, nullslop (316K subscribers), 30 Jan 2026, 65 s: 7.31M views, 342K likes. 23x subscribers. https://www.youtube.com/shorts/e72ow7hbP-4
- YouTube Short, MadAsh (3.37M subscribers), 25 Oct 2025, 59 s: 4.04M views, 110K likes. 1.2x subscribers. https://www.youtube.com/shorts/ThQJorl1B7k

Why it works: tiny agency plus suspense, with the comment "door 2" as a built-in reply.

Outcome draft: "Pick a door": three doors, each hiding one market, and the reveal is how sure the crowd is. Door 1: Fed decision in October (no change 81.0). Door 2: 2026 Ballon d'Or (Kane 65.6). Door 3: Premier League winner (Arsenal 59.9). Ask "which door has the most sure crowd?" Door 1. Effort low, risk low.

#### 12. A versus B split-screen comparison ("who is richer"). Origin: net worth and comparison pages. Grade B

Looks like: two names or images side by side, bars grow, a winner is shown. 39 s on the verified clip.

Examples (VERIFIED):
- YouTube Short, starinstant (46.5K subscribers), 11 Aug 2025, 39 s: 4.17M views, 36.9K likes. 90x subscribers. https://www.youtube.com/shorts/MZYCBuzl3Jg
Context: a 40.9M-view version ("Which Person Is Richer?", 60 s, May 2024) sits on a 12.2M-sub channel that shows faces, so it is not used as proof. No TikTok example verified.

Why it works: everyone has a gut ranking and wants to be right; two bars is the easiest possible visual.

Outcome draft: "Head to head" with two markets, not two people: Arsenal's Premier League title chance (59.9) against Barcelona's Champions League title chance (22.8), "which is more likely?", then bars and the plug. Variant: top two of one market (Kane 65.6 vs Yamal 28.6). Effort low, risk low.

#### 13. Comment-to-decide series. Origin: creator challenges. Grade C (no faceless proof)

Looks like: "comment what I should do next and I will do it", the top comment becomes tomorrow's video.

Examples: feed only, UNVERIFIED as faceless. @dillondacreator04's comment challenges reached 3.57M plays with 32,656 comments (feed numbers, 24 Jun 2025), but the format is built on a person doing things. The closest faceless proof is the comment-gated quiz in #4 (@brainfuel_360).

Why it works: ownership. Viewers feel the next video is theirs.

Outcome draft: a pinned-comment ballot ("A: UCL winner, B: Fed decision, C: Ballon d'Or") and the winner becomes the next day's post. It only works once there is an audience, so use it from week 3, not day 1. Effort low, risk low.

### Group C. Data and graphics

#### 14. Bar chart race. Origin: data-visualisation pages. Grade A on TikTok, weak on Shorts

Looks like: horizontal bars re-ranking year by year, names and flags, a running year counter, calm music. The verified posts run 166 to 203 s, not Shorts length. Title pattern "Most Popular X: Rise and Fall (2007 to 2026)". #barchartrace has 177M lifetime views and 3,221 creators.

Examples (VERIFIED):
- TikTok @hai02a (112.5K followers), 2 Sep 2026, 185 s: 18.79M plays, 597K likes (3.2%), 4.2K comments, 13.9K shares (0.07%), 35.7K saves. 167x followers. https://www.tiktok.com/@hai02a/video/7680984511143841037
- TikTok @hai02a (112.5K followers), 2 Sep 2026, 166 s: 2.19M plays, 59.7K likes (2.7%), 2.0K comments, 2.6K shares (0.12%), 4.9K saves. 19x followers. https://www.tiktok.com/@hai02a/video/7681002443857022222
- TikTok @zain02a (4,398 followers), 7 Aug 2026, 203 s: 2.17M plays, 72.2K likes (3.3%), 1.2K comments, 1.2K shares (0.05%), 5.0K saves. 494x followers. https://www.tiktok.com/@zain02a/video/7671253367112387853
YouTube Shorts of the same idea are weak: "Does investing 100$ monthly in FERRARI make you rich?" 34.8K views (15.4K subs, Nov 2025). So this is a TikTok-first mechanic.

Why it works: waiting for the leader to change is a built-in prediction game, my favourite moving up is a personal reward, and the length gives watch time.

Outcome draft: "Chance race: who the crowd backs for the Champions League". Bars for the six favourites racing through the daily price history from 4 Sep to 13 Oct and ending on Barcelona 22.8, Bayern 14.3, Arsenal 13.3, PSG 12.8, Real Madrid 11.0, Man City 6.7 (S1; the API pull will supply every day from start to end). Start the clip on the final ranking for one second so viewers know what they are waiting to see change. Caption must say these are market chances, not a forecast. Effort medium, risk low.

#### 15. Map animation and map explainers ("what if X became one country"). Origin: geography pages. Grade A

Looks like: an animated map, colours filling in, captions or a voice, 60 s. Explainer variant runs about 168 s ("Why 13 Colonies declared independence").

Examples (VERIFIED):
- TikTok @geo.all.day (244.9K followers), 4 Jan 2025, 60 s: 10.49M plays, 1.02M likes (9.8%), 20.8K comments, 420K shares (4.01%), 137K saves. 43x followers. https://www.tiktok.com/@geo.all.day/video/7456143352879271210
- TikTok @geotok (58.1K followers), 19 Apr 2026, 64 s: 8.32M plays, 265K likes (3.2%), 1.3K comments, 10.1K shares (0.12%), 41.2K saves. 143x followers. https://www.tiktok.com/@geotok/video/7630542013703671062
- TikTok @geoglobetales (2.1M followers), 23 Jul 2026, 168 s: 6.31M plays, 548K likes (8.7%), 3.7K comments, 20.2K shares (0.32%), 58.0K saves. 3.0x followers. https://www.tiktok.com/@geoglobetales/video/7665738589648489759

Why it works: curiosity ("what if"), national identity, and a hard-to-fake visual. The @geo.all.day post has 4.0% shares and 136,868 saves.

Outcome draft: "Where is the title going?" A map of Europe coloured by each country's summed Champions League title chance, adding up every club in the market (the API gives all of them; the six leaders alone are Barcelona 22.8, Bayern 14.3, Arsenal 13.3, PSG 12.8, Real Madrid 11.0, Man City 6.7). Do not state the country totals until computed. Effort medium (map assets), risk low. Fits only markets that have a place on a map.

#### 16. Tier list and ranking reveals (and "rate this"). Origin: ranking pages. Grade A, faceless status UNVERIFIED

Looks like: 17 to 79 s. A blank S/A/B/C/D board, items dropped in one by one with a sound hit, one-line verdicts. "Rate this" is the single-item version.

Examples (VERIFIED):
- TikTok @sammyshakiry (238.4K followers), 28 Jul 2026, 72 s: 6.00M plays, 497K likes (8.3%), 3.2K comments, 50.1K shares (0.84%), 27.5K saves. 25x followers. https://www.tiktok.com/@sammyshakiry/video/7667372772682779926
- TikTok @sammyshakiry (238.4K followers), 5 Aug 2026, 17 s: 3.87M plays, 136K likes (3.5%), 982 comments, 9.4K shares (0.24%), 5.7K saves. 16x followers. https://www.tiktok.com/@sammyshakiry/video/7670621767077055766
- TikTok @tier.list.everything (58.8K followers), 17 Aug 2026, 79 s: 1.98M plays, 232K likes (11.8%), 1.8K comments, 20.9K shares (1.06%), 23.6K saves. 34x followers. https://www.tiktok.com/@tier.list.everything/video/7675058074192776462
Face check: the @sammyshakiry creator may appear or speak on camera; I could not check. Rate-this example: @poppincandyofficial "Rate this order" 3.3M plays, but it is an 11M-follower brand, so not small-account proof.

Why it works: everyone has opinions and disagreement is free reach. Like rates are high (8.3% and 11.8%).

Outcome draft: "Crowd tier list". Tiers by chance (our own cut-offs, say so on screen): S 50% and up, A 15 to 50, B 5 to 15, C under 5. Premier League winner: Arsenal S (59.9), Man City A (19.9), Chelsea B (7.5), Liverpool B (5.6), Spurs C (2.9), Man Utd C (1.7). Ballon d'Or: Kane S (65.6), Yamal A (28.6), Messi C (3.2). Pure template, fully automatic. Effort low, risk low.

#### 17. Wealth scale ("how rich is X", "spend the money"). Origin: finance and net worth pages. Grade A on YouTube, risk high for Outcome

Looks like: a huge number set against everyday objects, a scrolling counter, or a "spend it" game. 29 to 65 s.

Examples (VERIFIED):
- YouTube Short, FactoHolic (22.8M subscribers), 1 Dec 2025, 65 s: 81.32M views, 2.39M likes. 3.6x subscribers. https://www.youtube.com/shorts/4jyR0RXaXXU
- YouTube Short, Fact2Fact (9.52M subscribers), 16 Jun 2026, 60 s: 15.95M views, 382K likes. 1.7x subscribers. https://www.youtube.com/shorts/cbMJUMXSpnQ
- YouTube Short, NYKentertain (871K subscribers), 9 Oct 2025, 29 s: 8.79M views, 240K likes. 10x subscribers. https://www.youtube.com/shorts/UIIcbhTokL8

Why it works: awe at scale, and "what would I do with it".

Outcome draft: only as a volume scale, never as profit: the UCL winner market has $2.4M of volume, the EPL winner $2.2M, the NFL winner $2.0M, the Fed decision $894.1k (volume is money traded, not money won). Any use of the $503,008 all-time #1 result must be framed as one outlier from 2 trades, a past result, never typical. Hold for now: file 03 notes that TikTok restricts gambling and investment-type finance content and bans fake investment offers and get-rich-quick schemes, and wealth-scale posts sit close to that line. Effort low, risk high.

#### 18. Time machine ("if you invested $1,000 in 2015"). Origin: investing pages. Grade C (weak)

Looks like: an asset, a start year, a growing number, "today it would be worth".

Examples (VERIFIED, all weak; two more in section 6):
- YouTube Short, Hustle Reality (214K subscribers), 5 Sep 2022, 16 s: 344K views, 6.2K likes. 1.6x subscribers. https://www.youtube.com/shorts/WByI4-bJGHo [outside the 2024 to 2026 window]
- YouTube Short, Infomapas Global (4.76K subscribers), 16 Jun 2025, 17 s: 20.7K views, 126 likes. 4.4x subscribers. https://www.youtube.com/shorts/rW1XRbvck2M
- TikTok @crypto.lucho (2.7M followers), 7 Oct 2026, 60 s: 2.07M plays, 157K likes (7.6%), 544 comments, 2.1K shares (0.10%), 11.3K saves. 0.77x followers. https://www.tiktok.com/@crypto.lucho/video/7693954189197659410
Context: #ifyouinvested has 13.7K lifetime views and 12 creators on TikTok (tikwm, 13 Oct). The one high-reach example is a story-led post from a 2.7M-follower account in Spanish (face status UNVERIFIED), at 0.8 plays per follower.

Why it is weak: viewers have seen it many times; the high-reach versions are really stories with a person.

Outcome draft: do not post counterfactual profit. Use history for "how the crowd changed its mind": Barcelona's Champions League chance was 13.6 on 4 Sep and is 22.8 now, a move of 9.2 points. That is real, dated, and promises nothing. Effort low, risk high if it turns into "what you would have made".

#### 19. Leaderboard, scoreboard and live ticker. Origin: gaming and news pages. Grade C (UNVERIFIED)

Looks like: a ranked table that updates, a running counter, a news crawl.

Examples: none verified. #leaderboard has 905M lifetime views but the one recent hit in the feed was a mobile-game promo, and #livecounter has 3.0M lifetime views and no hit above 700K plays. The bar chart race (#14) is the nearest verified relative.

Why it should work: a moving number promises something will change.

Outcome draft: the brief's "Top 3 traders" carousel already is the leaderboard format. The only new piece would be a daily "Crowd scoreboard" from the fan API (last-24h #1 trader-W +$16,838.68, #2 trader-P +$5,982.82, #3 trader-B +$3,710.73 on 12 Oct), with the client's OK to name users and a past-results line. Effort low, risk medium.

#### 20. Satisfying counters (ASMR numbers). Origin: satisfying and ASMR pages. Grade A as a category, risk high for Outcome

Looks like: a machine counting notes, a number ticking up, a sound loop. 21 to 97 s.

Examples (VERIFIED):
- YouTube Short, CountAndCalm (221K subscribers), 25 Feb 2025, 27 s: 9.08M views. 41x subscribers. https://www.youtube.com/shorts/HhXCZPJdyx0
- YouTube Short, Rajev Madhava (133K subscribers), 30 Aug 2025, 21 s: 13.30M views, 187K likes. 100x subscribers. https://www.youtube.com/shorts/WGO_fBNOeRU
- TikTok @asmr.soap734 (1.2M followers), 19 Sep 2025, 97 s: 76.31M plays, 4.41M likes (5.8%), 22.0K comments, 340K shares (0.45%), 281K saves. 64x followers. https://www.tiktok.com/@asmr.soap734/video/7551883110841978134
The last one is soap ASMR, listed to show the size of the "satisfying" category (76.3M plays), not as a finance example.

Why it works: sensory loop, completion, easy rewatch.

Outcome draft: only as an end-card flourish: a counter ticking through settled results with a green tick each. Keep real money counters out; the brief keeps figures realistic (title under $10k, trades about $1,000 or less) and shows the real event. Effort low, risk high.


### Group D. Stories and scenes

#### 21. Reddit-style storytime over gameplay. Origin: Reddit story channels. Grade B

Looks like (typical): a narrated story over gameplay or satisfying footage with captions on screen. The verified @storytellings1043 post is a 3,297 s (55 min) "FULL STORY" video; the @our2gens post is 443 s. Neither is Shorts length, so for a 45 to 60 s cut the proof is indirect.

Examples (VERIFIED):
- TikTok @storytellings1043 (20.3K followers), 2 Mar 2026, 3297 s: 7.22M plays, 325K likes (4.5%), 7.9K comments, 19.7K shares (0.27%), 70.3K saves. 356x followers. https://www.tiktok.com/@storytellings1043/video/7612563021403131158
- TikTok @our2gens (199.8K followers), 12 Mar 2026, 443 s: 1.57M plays, 212K likes (13.5%), 3.6K comments, 51.6K shares (3.29%), 21.2K saves. 7.9x followers. https://www.tiktok.com/@our2gens/video/7616444438092500237

Why it works: an open loop that only closes at the end, and background footage that keeps the eye busy. The @our2gens post has 3.3% shares.

Outcome draft: this is the brief's own "Trader story" format, so the new part is the angle: tell the story of one market, not one person. Use only facts already checked in file 01, section 5.5: the 2026 World Cup champion market, Spain beat Argentina 1-0 in the final on 19 Jul 2026, the market settled on 20 Jul at 07:51 UTC, the biggest account bought Spain shares at an average 60.08 cents. If the user is named, get the client's written OK, and say plainly that it is one outlier result from 2 trades, a past result, not typical. Effort medium, risk medium to high (glamorising a large win).

#### 22. "What if you were there" scenario. Origin: science and what-if story pages. Grade B (one account)

Looks like (typical): 80 s of second-person narration ("You are in Central Park when..."), a slow build, AI-style visuals. The verified post is 80 s. A second post from the same account reached 10.81M plays on 5 Oct (feed only, not re-fetched).

Examples (VERIFIED):
- TikTok @man_ia_c (219.5K followers), 6 Oct 2026, 80 s: 13.84M plays, 1.67M likes (12.1%), 9.1K comments, 92.7K shares (0.67%), 145K saves. 63x followers. https://www.tiktok.com/@man_ia_c/video/7693494009494342945

Why it works: immersion and dread, "what would I do", and saves (144,627 saves is 1.0% of plays; the like rate is 12.1%).

Outcome draft: "What does 10.2% look like?" Replay tonight ten times. The crowd's numbers for Galatasaray v Barcelona are Galatasaray 10.2, draw 12.9, Barcelona 76.7 (S1): about one replay where Galatasaray wins, one where it is a draw, eight where Barcelona wins. A scene-based way to teach what a percentage is, with "the crowd's price, not a guarantee" on screen. No invented match events. Effort low, risk low.

#### 23. POV and "nobody:" memes. Origin: relatable-skit accounts. Grade C (UNVERIFIED as a faceless format)

Looks like: a one-line text setup ("POV: ...", "Nobody: ... Me: ..."), 7 to 17 s.

Examples: no verified faceless example. The biggest recent post in the #POV feed is @wes.saint, a 7 s clip with 65.5M plays and 14.4M likes on 14 Jul 2026 (feed only; face status UNVERIFIED, probably a person). #Nobody has 7.67B lifetime views and one post above 2M plays since Jan 2025 (a Foxtel brand ad). My YouTube sample of text-only POV Shorts had 1.3K to 3.2K views each.

Why it works elsewhere: relatability and instant identity. The faceless text version shows no reach in the samples I could read.

Outcome draft: low priority. "POV: it is 18:59 UTC and you checked the table" with Galatasaray v Barcelona numbers. Effort low, risk low, expected performance low.

### Group E. Prediction and suspense

#### 24. AI predicts the future winners. Origin: football "predicted by AI" Shorts. Grade B (YouTube only)

Looks like (typical): 20 to 33 s, a list of years and winners appearing line by line, "predicted by AI" in the title, music. TikTok #aiprediction is tiny (7.0M lifetime views, 2,111 creators, no post above 2M since Jan 2025 in the feed), so this is a YouTube Shorts mechanic so far.

Examples (VERIFIED):
- YouTube Short, Game Day Brah (2.03K subscribers), 17 Jul 2026, 21 s: 4.85M views, 29.7K likes. 2,387x subscribers. https://www.youtube.com/shorts/q7PHmXFoIYk
- YouTube Short, MainFutLab (30K subscribers), 12 Aug 2026, 25 s: 2.83M views, 26.0K likes. 94x subscribers. https://www.youtube.com/shorts/PZJ7hBOE5Ws
- YouTube Short, MainFutLab (30K subscribers), 23 Aug 2026, 27 s: 1.75M views, 19.9K likes. 58x subscribers. https://www.youtube.com/shorts/wQJCgdGzEgc

Why it works: tribal identity ("when is my club's year?"), arguments in the comments, and an authority halo from "AI".

Outcome draft: "AI vs the crowd". Ask an AI model for a winner in each of tomorrow's nine Champions League matches. Left column: the AI's pick, generated that morning, with the model name and time on screen. Right column: the crowd's favourite from S1 (for example Man City 44.6, Real Madrid 50.8). Mark every disagreement in a colour, and post the scoreboard the next day (AI correct, crowd correct, both wrong). A second post: the AI's choice for the 2026 Ballon d'Or against the crowd's Kane at 65.6. Label "AI guess, not advice". File 03 (rule 13) says to label realistic AI visuals and not to use an AI "analyst" or "expert" persona for finance tips, so show the AI as a named tool, never as a character. Effort low, risk medium.

#### 25. Animal oracle. Origin: pet pages doing match predictions. Grade B (one account)

Looks like (typical): a pet picks a side for one match, 13 to 27 s, caption "Ronnie purrrdicts..." with the fixture in the title. #worldcupprediction has 37.1M lifetime views and 3,135 creators.

Examples (VERIFIED):
- TikTok @keesenronnie (5,592 followers), 9 Jul 2026, 27 s: 1.23M plays, 101K likes (8.2%), 2.7K comments, 19.5K shares (1.58%), 2.9K saves. 220x followers. https://www.tiktok.com/@keesenronnie/video/7660609718263516449
- TikTok @keesenronnie (5,592 followers), 12 Jul 2026, 13 s: 875K plays, 23.0K likes (2.6%), 972 comments, 2.0K shares (0.23%), 1.6K saves. 156x followers. https://www.tiktok.com/@keesenronnie/video/7661756779608558881

Why it works: cute plus prediction plus tribal reaction, and the result arrives within hours, so there is a built-in follow-up post.

Outcome draft: "Oracle vs crowd". The pet picks a side for Man City v PSG, the next card shows the crowd (Man City 44.6, draw 23.2, PSG 32.0, S1), and after the match a result card says whether pet and crowd agreed. Use a real pet or a drawn mascot. File 03 (rule 13) says to label realistic AI visuals, so an AI-made cat would need a label and invites questions. Effort medium, risk low.

#### 26. Marble or elimination race. Origin: marble race pages. Grade A for views, weak for brand fit

Looks like: named marbles race down a track for about 60 s with a comeback in the last seconds; longer episodic versions ("Episode 42") run 213 s. The verified @marbledecide post has 22,234 comments.

Examples (VERIFIED):
- TikTok @marbledecide (255.1K followers), 31 Dec 2025, 67 s: 41.95M plays, 1.43M likes (3.4%), 22.2K comments, 66.3K shares (0.16%), 51.0K saves. 164x followers. https://www.tiktok.com/@marbledecide/video/7590024312141188354
- TikTok @mevvomarbles (251.2K followers), 30 Apr 2025, 213 s: 11.14M plays, 609K likes (5.5%), 32.8K comments, 49.0K shares (0.44%), 43.6K saves. 44x followers. https://www.tiktok.com/@mevvomarbles/video/7498889646353698094
- YouTube Short, VITMI (7.7M subscribers), 4 Aug 2026, 46 s: 3.43M views, 40.7K likes. 0.45x subscribers. https://www.youtube.com/shorts/SzgR_dDTTsI

Why it works: pure suspense, "my marble" identity, and viewers predicting the winner in the comments.

Outcome draft: "Race to the line". Six marbles named after the title favourites, with speed weighted by the crowd's chance (Barcelona 22.8, Bayern 14.3, Arsenal 13.3, PSG 12.8, Real Madrid 11.0, Man City 6.7, S1). The result is random inside the weights, so a favourite sometimes loses, and the caption must say "animation, not a forecast". No prices or money on screen. It is a reach engine, not a product explainer, and it can look like a game of chance, so get the client's approval first. Effort high (physics render), risk medium to high.

#### 27. Pack opening and mystery reveals. Origin: card and collectible pages. Grade B, faceless status UNVERIFIED

Looks like (typical): a price on screen, then reveals one at a time, the big hit last. The verified post is 170 s.

Examples (VERIFIED):
- TikTok @bakacenteringguy (318.7K followers), 17 Mar 2026, 170 s: 15.29M plays, 473K likes (3.1%), 2.2K comments, 11.1K shares (0.07%), 29.4K saves. 48x followers. https://www.tiktok.com/@bakacenteringguy/video/7618368911372799246
Face check: the account may show hands only; I could not check.

Why it works: variable reward, stakes, and sensory sound.

Outcome draft: "Flip the card". Face-down cards for the 13 Oct Champions League card; flip one at a time to show the crowd's numbers; the last card is the biggest surprise, Viking v Bayern, with Viking at 4.2 and Bayern at 89.3 (S1). No money on screen. Effort low, risk low.

#### 28. "Guess what happens next" pause-and-guess clip. Origin: viral-clip and challenge pages. Grade B-/C

Looks like (typical): a clip freezes before the key moment, three options, a timer, the reveal. On TikTok, #whathappensnext has 509M lifetime views and 19.7K creators, yet no post above 2M plays since Jan 2025 appeared in the feed pages I read, so the format is quiet there.

Examples (VERIFIED):
- YouTube Short, fun max team (32.6K subscribers), 7 Oct 2026, 20 s: 1.26M views, 13.0K likes. 39x subscribers. https://www.youtube.com/shorts/ZrsAfCn3ZsE
This is a 20 s Short from a 32.6K-sub channel that reached 1.26M views in 6 days.

Why it works: it is a prediction in its simplest form, with an answer a few seconds later.

Outcome draft: "Pause before the whistle". Freeze on a market card minutes before its settlement time (S&P 500 above 7,805.7 at 20:00 UTC, 36.4 YES at the 00:59 UTC read), ask yes or no, then post the settlement in a follow-up. Same idea for WTI crude above 92.386 at 21:00 UTC (42.8 YES). Effort low, risk medium (price-direction content, see file 03).

#### 29. Numbered series wrapper (Part N, Day N). Origin: puzzle and quiz pages. Grade A for "Part N", C for "Day N"

Looks like: the same template every time, with the number in the caption or on the cover, so the profile reads like a season.

Examples (VERIFIED):
- TikTok @vxunitreal (14.8K followers), 4 Aug 2025, 71 s: 14.05M plays, 393K likes (2.8%), 765 comments, 1.7K shares (0.01%), 14.2K saves. 949x followers. https://www.tiktok.com/@vxunitreal/video/7534787903336025357
Also earlier in this file: @hiddengemz111 "Part 85" (29.6M plays, #2) and @brainfuel_360 "part 2" (8.0M plays, 231K comments, #4). "Day N" alone is weak: "Day 1 Prediction - FIFA World Cup" (9 s, Pushpek Sidhu, 4.03M subs, 11 Jun 2026) got 381,761 views, so the number helps only when the content itself earns the repeat.

Why it works: completion drive, a profile page that invites a binge, and an audience that comes back for the next part.

Outcome draft: name every series by matchday and keep the first 3 seconds identical: "Guess the favourite, Matchday 2, Part 14" and "Crowd scorecard, Day 3". Works as a wrapper on #1, #2, #4 and #10. Effort nil, risk low.

---

## 3. Your list, mapped to entries

| You asked about | Entry | Status |
|---|---|---|
| Guess the price | #6 | Thin faceless proof; fits Outcome literally (price in cents is the chance) |
| Guess the player | #1 | Strong |
| Higher or lower | #7 | Negative: no faceless hit; use only as a round inside a quiz |
| Only 1% get this | #2, #3 | Strong, but do not print "1%" without a real statistic |
| Bar chart races, data animations | #14, #15 | Strong on TikTok, weak on Shorts |
| Satisfying reveals | #20, #27 | Huge category, risky transplant |
| Countdown and timer suspense | #5, #28 | Strong for 12 s clips |
| Would you rather | #10 | Strongest in the study |
| Tier lists and rankings | #16 | Strong; faceless status needs a look |
| Rate my posts | #16 | Thin; only a brand example |
| POV and nobody memes | #23 | UNVERIFIED |
| The internet's favourite polls | #10 | Folded into pick-a-side |
| If you had invested | #18 | Weak and risky |
| How rich is X | #17, #12 | Strong on YouTube; risky for Outcome |
| Real vs fake | #8 | One small TikTok account |
| Mystery reveal slideshows | #2, #9 | Strong |
| Storytime slideshows | #21 | Long-audio proof only; photo versions UNVERIFIED |
| Explained in 60 seconds | #15, #22 | Strong |
| Map animations | #15 | Strong |
| What happens next | #28 | Weak on TikTok; one YouTube hit |
| I asked AI to predict X | #24 | YouTube only |
| Leaderboard or scoreboard updates | #19, #14 | Scoreboards UNVERIFIED; bar chart race verified |
| Streak or day N series | #29 | Part N works; Day N weak |
| Comment-to-decide series | #13 | No faceless proof |
| Split-screen comparisons | #12, #10 | Medium |
| Live-ticker videos | #19 | UNVERIFIED |
| Anything else | #11, #22, #25, #26, #27 | Found |

## 4. What failed, Instagram, and what to do first

What did not work in the data (useful to know before spending production time):
- Football and NFL "higher or lower" stat duels: 2.6K to 57K plays on accounts of 46K to 3.7M followers. The one 718K post (@wearetheoverlap) has a presenter on camera (#7).
- "If you invested" posts on Shorts: 21K and 35K views in 2025; the 344K one is from 2022 (#18).
- Text-only POV posts on Shorts: 1.3K to 3.2K views in the sample (#23).
- Bar chart races as Shorts: under 35K views; the wins are 3-minute TikToks (#14).
- "What happens next" on TikTok: no post above 2M plays since Jan 2025 in the feed pages read (#28).
- Live ticker, leaderboard and comment-to-decide: no faceless hit found (#13, #19).

Instagram. No post-level numbers could be read (see "How to read"). Profile pointers from search results on 13 Oct 2026, post-level UNVERIFIED: @nflguesstheplayer (36K followers, 376 posts; guess-the-player quizzes), @zillowgonewild (about 2M followers, 420 posts; the guess-the-price style property account), @thisorthatideas (1,332 followers, 42 posts; would-you-rather polls), @wealthy.og (1M followers; billionaire wealth content). Platform-level: Metricool (16 Jun 2026) found carousels earn 9 times the saves of single images and Reels over 4 times the interactions; Buffer (19 Mar 2026) found Instagram carousels have the highest median engagement (6.9%), ahead of single images (4.4%) and Reels (3.3%). So carousel quizzes (#2), tier lists (#16) and crowd-split cards (#10) are the right Instagram formats, and the same card images can post to TikTok photo mode.

Suggested order for the first two weeks (my suggestion, not tested):
1. Build one data pull (outcomeMeta, allMids, candleSnapshot) that writes a JSON of today's matches and season markets, as the vc-news studio does for rap news.
2. Week 1: run #10, #1 and #2 on the 13 and 14 Oct Champions League cards and the weekend fixtures. Three posts each, same first 3 seconds, numbered with #29.
3. Judge each format on five posts: plays per follower, share rate (benchmarks from this study: quizzes 1.3% to 2.0%, pick-a-side 2.3% to 8.2%) and comment rate.
4. Week 2: add #4 (scorecard from settled markets), #16 (tier list) and #24 (AI vs crowd). Add #14 once the history pull works.
5. Before any of it goes live: client-approved fee wording, the Ad and branded-content labels, and the country rules in file 03.

## 5. Sources and dates

All reads on 13 Oct 2026 unless stated.
- tikwm.com JSON API: /api/ (video fetch by URL: plays, likes, comments, shares, saves, date, duration, photo slides, music), /api/challenge/search (hashtag size), /api/challenge/posts (hashtag feeds). /api/feed/search and /api/user/info and /api/user/posts returned a Cloudflare challenge on GET and POST, so TikTok search and profile lists were not available. Request pattern: one lookup per post.
- TikTok follower counts: r.jina.ai reader on each public profile (https://r.jina.ai/https://www.tiktok.com/@name).
- YouTube: public results pages (to find Shorts) and public watch pages (views, upload date, channel subscribers, likes where shown). YouTube lists subscribers rounded, so ratios are approximate.
- Outcome data: Hyperliquid public info API, https://api.hyperliquid.xyz/info, types outcomeMeta, allMids and candleSnapshot, about 00:59 UTC. Home-page volumes and leaderboard facts are from file 01 in this folder.
- Platform studies: Metricool, "Instagram study 2026" press release, https://metricool.com/press-release-instagram-study-2026/ (published 16 Jun 2026; 24,364,803 posts from 375,118 accounts, Jan to Feb 2025 against Jan to Feb 2026). Buffer, "Best Content Format on Social Platforms in 2026", https://buffer.com/resources/data-best-content-format-social-media/ (19 Mar 2026; 45M+ posts).
- Web search (13 Oct 2026): Instagram profile pages for @nflguesstheplayer, @zillowgonewild, @thisorthatideas, @wealthy.og; TikTok pages for the FootballJOE, Transfermarkt, Overlap, footballquizzler and ballgamepodcast higher-or-lower posts.
- Blocked or not available: direct TikTok, Instagram post pages and profile JSON (HTTP 401), Instagram embeds (empty shell), YouTube like counts for some Shorts.

Unverified or not done: faceless status of every video (not watched); Instagram post numbers; any live-ticker, scoreboard, POV or comment-to-decide example; whether the Outcome percentages shown here still match the site when you read this.

## 6. Extra verified posts (beyond three per entry)

Same checks as above (re-fetched 13 Oct 2026). Kept here so each entry stays at three links.

Entry #1
- TikTok @brainquizmania (112.1K followers), 13 Mar 2025, 60 s: 5.31M plays, 211K likes (4.0%), 12.9K comments, 71.9K shares (1.35%), 12.8K saves. 47x followers. https://www.tiktok.com/@brainquizmania/video/7481398452077808927
- TikTok @brainquizmania (112.1K followers), 12 Mar 2025, 60 s: 4.56M plays, 287K likes (6.3%), 2.3K comments, 90.3K shares (1.98%), 19.0K saves. 41x followers. https://www.tiktok.com/@brainquizmania/video/7480999631787232542
- YouTube Short, GOAL's Front Three (862K subscribers), 20 May 2024, 35 s: 1.15M views, 72.1K likes. 1.3x subscribers. https://www.youtube.com/shorts/LLanw09dg3k

Entry #5
- TikTok @sammy_picc01 (401.1K followers), 7 Oct 2026, 8 s: 420K plays, 27.3K likes (6.5%), 18.1K comments, 32.1K shares (7.63%), 2.0K saves. 1.0x followers. https://www.tiktok.com/@sammy_picc01/video/7693984407069216020

Entry #7
- TikTok @wearetheoverlap (1.4M followers), 16 Mar 2025, 91 s: 718K plays, 23.4K likes (3.3%), 32 comments, 58 shares (0.01%), 625 saves. 0.51x followers. https://www.tiktok.com/@wearetheoverlap/video/7482422093984927009
- TikTok @footballquizzler (45.6K followers), 25 Aug 2024, 60 s: 12.3K plays, 429 likes (3.5%), 135 comments, 122 shares (0.99%), 39 saves. 0.27x followers. https://www.tiktok.com/@footballquizzler/video/7407192474629852449
- TikTok @ballgamepodcast (followers not read), 24 Sep 2025, 75 s: 2.6K plays, 201 likes (7.6%), 1 comments, 0 shares (0.00%), 5 saves. https://www.tiktok.com/@ballgamepodcast/video/7553453310548741406

Entry #10
- TikTok @learnchoice00 (184.8K followers), 5 Jan 2026, 60 s: 6.96M plays, 422K likes (6.1%), 1.8K comments, 450K shares (6.46%), 9.4K saves. 38x followers. https://www.tiktok.com/@learnchoice00/video/7591939935070932254
- TikTok @hotpick12 (99.7K followers), 25 Dec 2025, 60 s: 4.93M plays, 309K likes (6.3%), 1.3K comments, 371K shares (7.52%), 9.9K saves. 49x followers. https://www.tiktok.com/@hotpick12/video/7587857321762508062
- TikTok @dvdsfc (93.4K followers), 3 Mar 2026, 60 s: 3.77M plays, 260K likes (6.9%), 14.0K comments, 295K shares (7.82%), 11.4K saves. 40x followers. https://www.tiktok.com/@dvdsfc/video/7613140376546774294
- TikTok @learnchoice00 (184.8K followers), 5 Feb 2026, 60 s: 1.71M plays, 91.8K likes (5.4%), 324 comments, 141K shares (8.23%), 2.7K saves. 9.3x followers. https://www.tiktok.com/@learnchoice00/video/7603466965277084959

Entry #14
- TikTok @hai02a (112.5K followers), 20 Aug 2026, 200 s: 1.75M plays, 43.5K likes (2.5%), 1.5K comments, 2.8K shares (0.16%), 6.9K saves. 16x followers. https://www.tiktok.com/@hai02a/video/7676036110484655374

Entry #17
- TikTok @professinalquiz4 (244.3K followers), 10 Apr 2026, 69 s: 3.63M plays, 93.7K likes (2.6%), 1.0K comments, 3.0K shares (0.08%), 12.5K saves. 15x followers. https://www.tiktok.com/@professinalquiz4/video/7627087255143845142

Entry #18
- YouTube Short, ChartOrbit (15.4K subscribers), 8 Nov 2025, 60 s: 34.8K views, 270 likes. 2.3x subscribers. https://www.youtube.com/shorts/a0fAcl3g1Io

Entry #24
- YouTube Short, MainFutLab (30K subscribers), 4 Sep 2026, 33 s: 1.08M views, 13.5K likes. 36x subscribers. https://www.youtube.com/shorts/CB51U8Igt3c

Entry #26
- TikTok @marbledecide (255.1K followers), 10 Feb 2026, 62 s: 21.25M plays, 592K likes (2.8%), 14.2K comments, 27.8K shares (0.13%), 19.7K saves. 83x followers. https://www.tiktok.com/@marbledecide/video/7605292889467391254
- YouTube video (26 min), MoreBalls (197K subscribers), 25 Nov 2024, 1603 s: 5.82M views, 16.5K likes. 30x subscribers. https://www.youtube.com/watch?v=_biIzYIUSWg
