# 12. Faceless sports formats for Outcome (football first, then NFL and NBA)

Written 13 Oct 2026 for the Outcome project (Vision Clipping). Scope: faceless TikTok, Instagram and YouTube Shorts formats from 2025 to 2026 that could carry a real "% chance" from an Outcome market. Numbers were pulled 13 Oct 2026 unless a date is given.

Client rules kept in every idea below: say "% chance", never bet, betting or odds-style numbers, never promise profit, never cover the market chart or the logo, CTA line "Trade with zero fees on Outcome.xyz". One flag on that CTA: 01-what-is-outcome.md found that "zero fees" is not fully accurate (no fee to open, about 0.05% to 0.14% on close or settle), so get the wording approved in writing before anything ships.

## 1. Format table

OS = outlier score (type shown). V/F = views divided by followers. Build = how hard to automate with the vc-news style pipeline (HTML template, headless Chrome, ffmpeg, batch JSON).

| # | Format | Where and how long | Best verified proof | Outlier | Outcome data | Build | Main risk |
|---|---|---|---|---|---|---|---|
| F1 | Supercomputer reveal ("Opta says Arsenal 45%") | TikTok, Shorts, Reels, 20 to 60 s | Sky Sports Football, Opta plus Neville, 2.67M views, 20 Apr 2026, 3.3M followers | 8.3x avg likes; Opta's own TikTok 0.3x | none (third-party number) | Easy | Small pages get nothing without a famous voice |
| F2 | Race swing card ("went from 50% to 66%") | Shorts, TikTok, carousel, 8 to 20 s | IFR Football, Polymarket Ballon d'Or top 5 Short, 36K views, 22 Sep 2026 | 9.7x channel median | daily and hourly price history | Easy | Thin markets move on a few trades |
| F3 | Ballon d'Or poll card (who deserves it, plus the crowd %) | TikTok, Shorts, 5 slides or 15 to 30 s | fr.football31, 491K views, 84.8K likes, 5.6K comments, 24 Sep 2026 | 16.2x avg likes | Ballon d'Or market | Easy | Ceremony date and fake winner edits |
| F4 | Matchday prediction card (home, draw, away %) | TikTok, Reels, Shorts, 15 s | footballmaster3333, UCL fixtures card, 4.07M views, 8 Sep 2026, 286.6K followers | V/F 14.2x; 91.9x avg likes | every UCL and Europa match market | Easy | "Tips" wording; regulation-time rule |
| F5 | Chart replay (the line moving through a match or race) | Shorts, TikTok, Reels, 15 to 30 s | No viral proof found. Idea is normal on TV (Opta live win probability, Polymarket UFC scoreboard) | n/a | price candles 1 min to 1 day | Medium | Never cover chart or logo; do not claim cause |
| F6 | Market vs model ("Opta 45%, the crowd 60%") | all three, 20 to 30 s or 3 slides | Whitespace. Both halves proven (F1, F2) | n/a | any winner market plus one outside number | Medium | Quote Opta as source only |
| F7 | Called-it / upset retrospective (pre-match % vs result) | all three, 15 to 30 s | NBA playoff upset meme, 2.15M views, 3 May 2026, 14.7K followers | V/F 146x | price at kickoff minus 1 h, results | Medium | Never say "we called it" |
| F8 | Weekly crowd-vs-AI scoreboard (NFL first) | TikTok, Reels, 60 to 180 s weekly | imjacobrose "ChatGPT NFL picks" 17.9M views, 15 Sep 2026 (tagged #kalshipartner) | V/F 88x; like rate only 0.16% | weekly NFL game markets | Medium | "Picks" language; paid reach is not organic proof |
| F9 | Table-prediction carousel (crowd's top 6) | TikTok photo mode, Reels carousel, 6 to 21 slides | jonathanweston75 21-photo table, 282K views, 20 Jul 2025 | V/F 30x | EPL winner market | Easy | Peaks in pre-season |
| F10 | Ranked-list explainer ("Top 5 ...") | TikTok, Shorts, 45 to 70 s | fubotvcanada "Top 5 highest xG misses", 1.34M views, 13 Nov 2024 | 6.9x avg likes | top movers, top chances | Medium | Needs clip rights or stills |
| F11 | Bar chart race / data timeline | TikTok, Shorts, 20 s to 4 min | hai08a "Most valuable players 2004 to 2026", 307K views, 11 Sep 2026 | 22.7x V/F; 7.6x avg likes | 14 to 30 day price series | Medium | Long versions drop off |
| F12 | Stat duel (A vs B, one stat each, then the %) | TikTok, Shorts, 60 to 130 s | goalwhiz08 Messi vs Ronaldo dribbles, 172K views, 21 Apr 2026 | 0.8x avg likes (average) | link to a market | Medium | Stat source terms; weak on TikTok |
| F13 | Football facts mini-doc (voice-over, possibly AI voice) | TikTok, Shorts, 60 s | legoat2215 "Red Card King", 8.96M views, 30 Oct 2025 | 12.2x avg likes | closing market line | Medium to hard | Not Outcome-specific; voice and footage rights |
| F14 | "Invest now" market meme | TikTok, Reels, 15 to 60 s | mkz1_0 "Invest now", 1.75M views, 32.3K shares, 24 Aug 2026 | 13.1x sibling median | price move of a player or club | Hard (humour) | "Invest" can sound like advice |
| F15 | Title-race fan-edit meme | TikTok, Reels, 25 to 75 s | provhl "NOT LIKE US", 3.14M views, 18 Apr 2026, 8.4K followers | V/F 373x | race % as a corner chip | Hard (humour) | Song and clip rights |
| F16 | 10-second POV / reaction meme with a % chip | TikTok, Reels, 6 to 10 s | purejokes0 "Champions League final", 1.68M views, 76.8K shares, 30 May 2026 | 53.6x avg likes | latest % after the result | Hard (humour) | Clip rights; speed |
| F17 | Hot-take text over clips with a market "receipt" | TikTok, Reels, 45 to 90 s | habibx03 "YAMAL > RONALDO", 2.81M views, 192.8K shares, #polymarketpartner, 19 Jul 2026 | 54.2x avg likes | the % as proof line | Medium | Paid-partner disclosure; clip rights |

## 2. How to read the numbers (and what I could not measure)

- **TikTok per-video stats** came from the tikwm.com root endpoint (GET). It works. The account post lists (user/posts, feed/search) were blocked by a Cloudflare check today, on GET and POST, with and without www, and through r.jina.ai and WebFetch. Workaround: hashtag video lists (challenge/posts), account totals (user/search: followers, total likes, video count) and r.jina.ai profile reads.
- **Outlier scores.** The brief asked for views divided by the account's median of recent posts. I could only do that properly on YouTube (median of the last 45 Shorts). For TikTok I used three honest proxies and label which one each time:
  - **OS-med**: views divided by the median views of sibling posts I sampled (TikTok sample is biased high, because hashtag lists show popular posts).
  - **OS-likes**: the post's likes divided by that account's average likes per video (lifetime likes divided by video count). It is a mean, not a median, so big accounts look flatter than they are.
  - **V/F**: views divided by followers.
- **Instagram: UNVERIFIED.** The search tool only returns Instagram profile pages, r.jina.ai hits the login wall, and the embed route needs a post code that I could not find. No Instagram number below is stated as fact. If you paste 5 to 10 Instagram post links I can run the embed route on them.
- **Paid or fake reach is flagged.** Many of the biggest numbers are tagged #kalshipartner or #polymarketpartner (paid creators), and some are fake "winner announced" edits.
- **No video or image files were downloaded or viewed.** "Looks like" notes are inferred from caption, length, audio and photo count, and say so.
- **Outcome prices** came from the public Hyperliquid info API (outcomeMeta, allMids, candleSnapshot), pulled 13 Oct 2026 at about 06:23 PC local time. Untraded outcomes show a placeholder 50% mid, so I checked before using any number (see Appendix A).

## 3. What the data says (read this before the details)

1. **Probability framing is rare on TikTok, and that is both the gap and the warning.** Hashtag totals on 13 Oct 2026: #ballondor 34.45B views, #premierleaguepredictions 548M, #titlerace 529M, versus #footballodds 1.6M, #optaanalyst 2.8M, #footballprobability 333K, #winprobability 177K, #optasupercomputer 141K, #premierleagueodds 75K, #titleodds 12K, #nbaodds 1.7M, #nbatitleodds 37K, #nflfutureodds 73K, #superbowlodds 1.4M, #ballondorrace 1.5M, #ballondorpredictions 1.1M. The attention is in the topics, not in "odds" or "probability" posts.
2. **The biggest numbers in my sample came from six things:** a famous page reacting to a number (Sky, 2.67M); a daily 15-second fixture card (4.07M for a 287K page); 6 to 10 second memes with 4% to 7% share rates (up to 192.8K shares on one post); voice-over football facts (8.96M); paid weekly NFL AI picks (4M to 18M views but only 0.14% to 0.2% likes); and fake "Ballon d'Or winner" edits (14.7M).
3. **Plain data posts from small pages flop.** Mirror Football's supercomputer table: 1,045 views. Opta Analyst's own TikTok (35.3K followers): about 20K views on supercomputer posts, 0.3x its average likes. Squawka's "guess who scored more" quiz: 13.5K views on 174K followers.
4. **The one prediction-market number that clearly beat its channel was a Ballon d'Or one:** IFR Football's Polymarket top 5, 9.7x its channel median. The Ballon d'Or is the strongest topic available right now (ceremony reported as 26 Oct 2026 in London, UNVERIFIED, from two YouTube titles).
5. **Fake winner edits are a lane for a real number.** "Ballondor winner 2026 kylian mbappe" (py10_1, 20,963 followers) got 14.73M views and 1.44M likes on 3 Sep 2026, and a French sports page posted "Mbappe just won the Ballon d'Or 2026" on 1 Oct 2026 (1.13M views). The ceremony had not happened. A real "% chance on Outcome" post is the honest counter.
6. **Prediction-market brands win through creators, not through their own pages.** Official @polymarketsports has 753.9K followers and 27.4M likes, but a recent post (11 Oct 2026, NFL overtime reaction) got 92K views, 0.4x its own average likes. The creator tags are enormous: #kalshipartner 5.78B views, #polymarketpartner 156M.
7. **Outcome has something these pages lack: real price history.** In the 8 days to 13 Oct, Kane went from 50% to 66% and Yamal from 43% to 28% on Outcome. Almost no one is making "the line moved" content on TikTok.
8. **Showing a market % beside sport is normal on TV now.** Opta Live Win Probability on Prime Video (100,000 simulations of the rest of the match); Polymarket's Fan Prediction Scoreboard inside UFC and Zuffa Boxing broadcasts (announced 13 Nov 2025); Polymarket official partner of MLS (26 Jan 2026) and of OneFootball (about two weeks before the 2026 World Cup).
9. **Do not copy the fake-bet playbook.** A WSJ investigation (reported by Quartz, second-hand here) said Polymarket paid creators to post fake betting clips: 1,105 TikTok videos reviewed, 778 appeared to show a bet being placed, none showed the real site. Outcome's brief already says the real event must be shown.

## 4. Detail per format

Every TikTok number below was read from the tikwm root endpoint on 13 Oct 2026 (views, likes, comments, shares, saves). Follower counts are from tikwm user/search or r.jina.ai profile reads on the same day. YouTube numbers are from r.jina.ai page reads.

### F1. Supercomputer reveal (Opta supercomputer or an AI says "X% chance")

- **Where and length.** TikTok, Shorts, Reels. 20 to 60 s video, or a 5-slide carousel.
- **Looks like (inferred from captions and lengths).** A table or title-chance graphic from Opta Analyst, a voice or a pundit reacting, ending on "do you agree?". Sky's version is a 23 s studio clip with Gary Neville reacting.
- **Verified examples.**
  - Sky Sports Football, "The Opta supercomputer's Premier League probabilities left Gary Neville speechless!" https://www.tiktok.com/@skysportsfootball/video/7630815925700185366 . 20 Apr 2026. 2,666,992 views, 178.7K likes, 2.6K comments, 5.8K shares, 7.7K saves, 23 s. 3.3M followers.
  - Daily Mail Sport, "Supercomputer predicts the 2025/26 Premier League table" (Daily Mail BREAKDOWN). https://www.tiktok.com/@dailymailsport/video/7538100523916872982 . 13 Aug 2025. 1,340,792 views, 93.0K likes, 1.3K shares, 62 s. 6.8M followers.
  - Rory Talks Football (YouTube Short), "The SUPERCOMPUTER Premier League Prediction". https://www.youtube.com/shorts/2At69Nh1olM . 14 Aug 2026. 131K views, 3.1K likes. 103K subscribers.
  - Flops from the same idea: Mirror Football, https://www.tiktok.com/@mirrorfootball/video/7434500561996680481 , 7 Nov 2024, 1,045 views, 32 likes, 115K followers. Opta Analyst's own World Cup post (France 27%), https://www.tiktok.com/@optaanalyst/video/7660491789014420758 , 9 Jul 2026, 19,996 views, 224 likes, 35.3K followers.
- **Outlier.** Sky 8.3x its average likes (V/F 0.8x). Daily Mail 1.4x. Rory 0.78x its channel median (167,000 over the last 45 Shorts), so an average Short for him. Opta Analyst 0.3x. Mirror about 0.
- **Why it works.** A surprise number about someone's club, and a ready argument. Send trigger: tag the mate whose team is rated low. It only worked when a big page or a known voice carried it.
- **Outcome version.** Do not run it alone as a new page. Use it as the first half of F6 (market vs model).
- **Needs.** One number a week from Opta Analyst (copy by hand; I did not test scraping). Easy.
- **Risk.** Opta and Stats Perform graphics are theirs: quote the figure and name the source, do not copy their charts (my reading, not legal advice).

### F2. Race swing card (title race or award race: "went from A% to B%")

- **Where and length.** Shorts, TikTok video or photo, Reels. 8 to 20 s, or 3 to 5 slides.
- **Looks like (inferred).** Name, old number crossing to new number, a small line under it, one line of context. Big type, dark plate, no cover over the chart.
- **Verified examples.**
  - IFR Football (YouTube Short), "POLYMARKET'S TOP 5 FOR THE 2026 BALLON D'OR!" https://www.youtube.com/shorts/B93o41RX2Ns . 22 Sep 2026. 36,073 views, 228 likes. 161K subscribers.
  - Barca Media (YouTube video), "Lamine Yamal Has Now Taken Over Harry Kane To Win The 2026 Ballon Dor". https://www.youtube.com/watch?v=B5GRdCmDpbY . 28 Sep 2026. 10,126 views, 256 likes. 106K subscribers. I did not confirm which market the title is quoting.
  - ESPN UK, "Arsenal's PL title chances just 5%?! 'You're BUGGING!'" https://www.youtube.com/watch?v=MW-8Sxbkoek . 21 Nov 2024. 10,152 views, 125 likes. 1.6M subscribers. A shock % alone was not enough here.
  - Squawka, "Arsenal top at Christmas... can they win the Premier League title?" https://www.tiktok.com/@squawkafootball/video/7165143725570608389 . 12 Nov 2022. 92,346 views, 6.5K likes, 20 s. Old, shown for the type only.
- **Outlier.** IFR's Polymarket Short is 9.7x the channel median (3,700 across 45 Shorts).
- **Why it works.** A contest with a tribe on each side, and "went from" is a story while "is at" is only a level. The IFR post shows the Ballon d'Or is the topic that carries a market number today.
- **Outcome version (real data, daily closes, UTC).** Ballon d'Or: Kane 50% on 5 Oct, 48, 49, 54, 61, 64, then 66% on 11, 12 and 13 Oct. Yamal 43% on 5 Oct, 45, 44, 39, then a drop to 28% on 9 Oct, 30, 28, 29, 28. Two stories: "Kane up 16 points in 8 days" and "Yamal lost 11 points in one day (8 Oct to 9 Oct) and 17 in three days". No story in the other big markets: Arsenal EPL winner 58% (28 Sep) to 62% (9 Oct) to 60% (13 Oct); Man City 23% to 20%; Barcelona UCL winner 22% to 23% for 15 days. Rule: only post a swing when the 24 h or 7 day move is 8 points or more, on a market with real volume.
- **Needs.** candleSnapshot (1d or 1h) for each outcome, a "biggest movers" scan across all sports outcomes each morning, one template. Easy.
- **Risk.** Thin markets can move on a handful of trades; do not say why it moved; say "chance on Outcome", never "will win".

### F3. Ballon d'Or poll card (who deserves it, plus the crowd %)

- **Where and length.** TikTok video 15 to 30 s or 5-slide photo, Shorts, Reels.
- **Looks like (inferred).** Two or five names, a big question line, comments invited. Short, under 30 s on the best small example.
- **Verified examples.**
  - fr.football31, "who truly deserves the Ballon d'Or 2026 between Mbappe and Yamal?" https://www.tiktok.com/@fr.football31/video/7689116030567828749 . 24 Sep 2026. 491,131 views, 84.8K likes, 5.6K comments, 1.2K shares, 20.4K saves, 28 s. 54,969 followers (24 videos).
  - beIN SPORTS France, "Who will win the Ballon d'Or? Kane, Mbappe, Yamal, Dembele, Olise... who is YOUR favourite?" https://www.tiktok.com/@beinsportsfr/video/7666015704780393750 . 24 Jul 2026. 416,831 views, 88.5K likes, 5.8K comments, 85 s. 8.07M followers.
  - noahtalksfootball24, "Mbappe's running the show... who do you think deserves the Ballon d'Or?" https://www.tiktok.com/@noahtalksfootball24/video/7592990630922718475 . 8 Jan 2026. 776.8K views, 13.1K likes, 538 comments, 44 s. 50.2K followers.
  - Watch-out examples (fake): py10_1, "Ballondor winner 2026 kylian mbappe", https://www.tiktok.com/@py10_1/video/7681338434052721927 , 3 Sep 2026, 14.73M views, 1.44M likes, 79.5K shares, 19 s. nalnetsport, "Kylian Mbappe vient de remporter le Ballon d'Or 2026", https://www.tiktok.com/@nalnetsport/video/7691637818220612897 , 1 Oct 2026, 1.13M views, 61.2K likes, 215K followers.
- **Outlier.** fr.football31 16.2x its average likes (V/F 8.9x), saves 4.2% of views, comments 1.1% of views. beIN 2.5x. noahtalksfootball24 V/F 15.5x.
- **Why it works.** Every fan tribe has a name to defend, so people comment and save. Save trigger: "come back after the ceremony".
- **Outcome version (13 Oct 2026).** Kane 66%, Yamal 28%, Messi 3%, Dembele 2%, Mbappe 2%. Hook: "The crowd on Outcome gives Kane a 66% chance of the 2026 Ballon d'Or. A week ago it was 50%." Slide 2: the five names with %. Slide 3: the 8 Oct to 9 Oct Yamal drop. Slide 4: the poll line ("Is 28% too low for Yamal?"). Slide 5: CTA.
- **Needs.** Ballon d'Or question (Q391) plus candles. Easy.
- **Risk.** Ceremony date reported as 26 Oct 2026 in London from two YouTube titles (UNVERIFIED; confirm with France Football). Stop posting new cards the hour the result is public. Never use the word "winner" before it is announced. Player photos need a rights decision, so name plates in type are the safe version.

### F4. Matchday prediction card (home, draw, away %)

- **Where and length.** TikTok 15 s video or photo set, Reels, Shorts.
- **Looks like (inferred).** A vertical list of the day's fixtures, three numbers per match, a one-line prompt. The best example is 15 s with "original sound" (no music), so probably a quick pan of static fixture graphics.
- **Verified examples (same page, three days).** footballmaster3333, 286,617 followers, 1,320 videos.
  - "UEFA Champions League WEDNESDAY FIXTURES Matchday 1 - What are your tips". https://www.tiktok.com/@footballmaster3333/video/7683291811258944801 . 8 Sep 2026. 4,066,702 views, 155.3K likes, 4.5K shares, 18.4K saves, 15 s.
  - THURSDAY fixtures. https://www.tiktok.com/@footballmaster3333/video/7683694090290040097 . 10 Sep 2026. 2,343,347 views, 94.5K likes, 14.3K saves.
  - TUESDAY fixtures. https://www.tiktok.com/@footballmaster3333/video/7682845033011236128 . 7 Sep 2026. 473,309 views, 9.8K likes.
  - Related, weekly score cards: billytalksfootball (389.6K followers), "Gameweek 8 Premier League Score Predictions". https://www.tiktok.com/@billytalksfootball/video/7559939989295959318 . 11 Oct 2025. About 1.63M views, 31.4K likes, 57 s. Seven weekly posts I sampled ran 0.74M to 1.69M.
  - Text-media proof that "% chance vs club" headlines get clicks: Empire of the Kop, "Supercomputer gives Liverpool just 24.3% chance vs PSG", 8 Apr 2026.
- **Outlier.** Wednesday card: V/F 14.2x, 91.9x average likes. Thursday: 8.2x and 55.9x. Tuesday: 1.7x and 5.8x. Same page, same format, a 10x spread in three days, so judge the format on a month, not a post.
- **Why it works.** Fast, tribal, repeatable, and saved for later (18.4K saves). A daily slot trains the audience to come back.
- **Outcome version (live lines, matches on 13 to 15 Oct 2026, % chance on Outcome).**
  - Arsenal v Lille: Arsenal 80, draw 14, Lille 6.
  - Atletico v Man United: Atletico 51, draw 24, United 25.
  - Galatasaray v Barcelona: Barcelona 77, draw 13, Galatasaray 10.
  - Inter v Club Brugge 78 / 14 / 8, Viking v Bayern 4 / 7 / 89, Villarreal v Napoli 45 / 25 / 29 (home / draw / away).
  - Man City v PSG (14 Oct): City 45, draw 23, PSG 32. Roma v Real Madrid: Real 51, draw 24, Roma 26. LASK v Liverpool 10 / 14 / 76 (home / draw / away).
  - Prompt line: "Your call?" in place of "tips".
- **Needs.** outcomeMeta (questions of type sportsContestResult with participants and scheduledStart) plus allMids. Team-name clean-up. HTML template to PNG or MP4. Easy.
- **Risk.** "Tips" is betting language, so avoid it. Each match question resolves on regulation time (90 minutes plus stoppage) so say so in the caption. Skip any outcome whose price is exactly 0.50 with no volume.

### F5. Chart replay (the line moving through a match or a race)

- **Where and length.** Shorts, TikTok, Reels. 15 to 30 s.
- **Looks like (proposed).** The Outcome price line drawing itself across the match, with markers for kickoff, goals, red cards and full time, and the final number large at the end.
- **Verified examples.** No viral example found. #winprobability has only 176.7K views on TikTok in total (13 Oct 2026), so it is open ground. The idea is normal on TV: Opta Live Win Probability on Prime Video's Premier League coverage (100,000 simulations of the rest of the match; the Stats Perform page says it debuted in Prime's first games "earlier in December", year not shown in the snippet I could read), and Polymarket's Fan Prediction Scoreboard in UFC and Zuffa Boxing broadcasts (announced 13 Nov 2025).
- **Why it should work.** It is the "from 90% to 5%" story in its cleanest form, and the chart is Outcome's actual product.
- **Outcome version.** Pull 1 or 5 minute candles for the match window. First candidates: tonight's Galatasaray v Barcelona (Barcelona 77% pre-match) and Arsenal v Lille (Arsenal 80%). Publish at full time.
- **Needs.** Candles (easy). Goal and card minutes from a free football data source (I did not test one: UNVERIFIED which is best). Without events, use kickoff and full time markers only. Medium.
- **Risk.** Client rule: never cover the market chart or logo. If you redraw the chart rather than screen-record it, get Outcome's OK. Do not claim cause ("because of the red card"). Show date and "price on Outcome".

### F6. Market vs model ("Opta says 45%, the Outcome crowd says 60%")

- **Where and length.** All three. 20 to 30 s, or 3 slides.
- **Looks like (proposed).** Two big numbers side by side with source labels and dates, one line of why the gap is interesting, a question.
- **Verified examples.** None found as a named format, which is the opening. Its two halves are proven (F1 got 2.67M on Sky; F2 got 9.7x on IFR).
- **Real numbers.** Opta Analyst pre-season run (simulated 13 Aug 2026, article 14 Aug, 10,000 simulations): Arsenal 38.0%, Man City 20.5%, Liverpool 9.2%, Man United 6.2%, Aston Villa 4.8%, Chelsea 4.1%. After the first weekend (Sports Illustrated summary, not opened by me): Arsenal 45.18%, City 22.05%, Liverpool 8.18%, Chelsea 5.38%. Outcome on 13 Oct: Arsenal 60%, City 20%, Chelsea 8%, Liverpool 6%. So the gap on Arsenal is about 15 points against an Opta figure that is nine matchweeks old. **Do not post until the same-day Opta number is copied.**
- **Needs.** One outside number a week, dated and linked in the caption. Medium.
- **Risk.** Name Stats Perform as the source, do not imply they endorse Outcome. "The crowd prices it higher than the model" is a statement about prices, not a prediction.

### F7. Called-it / upset retrospective (pre-match % vs the result)

- **Where and length.** All three. 15 to 30 s. Also fits the client's P&L card edit.
- **Looks like (proposed).** "Before kickoff the Outcome crowd gave X a 12% chance." Final score. "That was 12%." The price line, then (only if the client approves real usernames) a P&L card of someone who held it.
- **Verified examples.**
  - Upset meme in NBA: psalms.777, "When I realized this matchup was over before it started. #Embiid #Sixers #NBAPlayoffs #UpsetAlert". https://www.tiktok.com/@psalms.777/video/7635598367552195871 . 3 May 2026. 2.15M views, 45.2K likes, 2.5K shares, 61 s. 14.7K followers (V/F 146x).
  - Weak market-retro posts: La Presse (YouTube Short), "Polymarket : est-ce que les paris ont vu juste ?" https://www.youtube.com/shorts/_JrH7YwQPgk , 9 Oct 2026, 704 views, 5 likes, 28.8K subs. A small channel's "PSG / Arsenal 57% Polymarket", https://www.youtube.com/shorts/SNpTNr-Lxo0 , 24 May 2026, read as 0 views (may be a parse miss).
  - A creator line "Polymarket Sports gave Man City only 28%" (account @adika.s.takes, promo code in the caption) appeared in a search summary only. Video link not captured. UNVERIFIED.
- **Why it works.** Hindsight proof and a punchline. The weak numbers above say the retro works as the ending of a hot take, not as a standalone post.
- **Outcome version.** A detector: any settled match where the winning side's Yes price one hour before kickoff was 25% or lower (or the draw was 15% or lower). Post within 30 minutes of full time.
- **Needs.** Price at kickoff minus 1 hour (candles), results from the settled question, optional leaderboard P&L card. Medium.
- **Risk.** Never "we called it" (nobody at Outcome predicts). A 12% event happening does not make the crowd wrong. Real usernames on cards need the client's permission (open item in 00-status.md).

### F8. Weekly crowd-vs-AI scoreboard (NFL first, then EPL)

- **Where and length.** TikTok and Reels. 60 to 180 s. Once a week.
- **Looks like (inferred).** ChatGPT's answer on screen game by game, a voice, a running record in the title ("12-4 so far").
- **Verified examples.**
  - imjacobrose (203,565 followers, #kalshipartner): "ChatGPT is 12-4 so far, here's week 2". https://www.tiktok.com/@imjacobrose/video/7685872142776405279 . 15 Sep 2026. 17,901,516 views, 28.5K likes, 2.3K shares, 119 s.
  - Same account, week 5. https://www.tiktok.com/@imjacobrose/video/7693930763825253662 . 7 Oct 2026. 9.56M views, 13.3K likes, 128 s. Week 4. https://www.tiktok.com/@imjacobrose/video/7691391788052974878 . 30 Sep 2026. 3.78M views, 5.5K likes.
  - itszoofuh (68,618 followers, #kalshipartner): "NFL Week 5 Predictions". https://www.tiktok.com/@itszoofuh/video/7694184718417300749 . 8 Oct 2026. 4.63M views, 9.1K likes, 159 s.
- **Outlier.** V/F 88x and 47x (imjacobrose), 67x (itszoofuh). But the like rate is 0.14% to 0.2%, against 3% to 12% on organic football posts in this report. Treat the views as partly paid or passive. What it proves: a Kalshi-linked program is paying for exactly this weekly format, and it fits a series.
- **Why it works.** A running record is a series hook; "can an AI beat the crowd" is a fresh argument.
- **Outcome version.** "Outcome crowd vs ChatGPT, Week N": crowd % for each game at lock time, the AI's pick stored before kickoff, final scores, running score. Outcome's NFL winner market today (Super Bowl 2027): Rams 11%, Bills 10%, Chiefs 10%, Seahawks 9%, Ravens 9%. Weekly game markets were not in the list when I pulled it on Tuesday 13 Oct (likely listed nearer kickoff: UNVERIFIED).
- **Needs.** Crowd % snapshot at lock, AI picks saved with a timestamp, a free score feed. Medium.
- **Risk.** Avoid "picks" and "bet" wording. Competitor money is behind this format. AI-generated labels may be needed on the platform.

### F9. Table-prediction carousel (the crowd's top 6)

- **Where and length.** TikTok photo mode (up to 35 images), Reels carousel (UNVERIFIED), Shorts. 6 to 21 slides.
- **Looks like.** One slide per team from 20th to 1st, or one table slide. The 21-photo example uses a FIFA World Cup anthem as audio.
- **Verified examples.**
  - jonathanweston75, "My 2025/2026 premier league season prediction! 20th Leeds, 19th Brighton ...". https://www.tiktok.com/@jonathanweston75/video/7529273402666896662 . 20 Jul 2025. 281,849 views, 19.1K likes, 21 photos, audio "Dreamers". About 9.5K followers (V/F 30x).
  - callum_wm (640,070 followers, face-led AR filter), "FILTER predicts ENTIRE 25/26 PREMIER LEAGUE TABLE". https://www.tiktok.com/@callum_wm/video/7536938360552672519 . 10 Aug 2025. 2,524,149 views, 95.5K likes, 142 s.
  - Premier League (27.6M followers), "Robbie Fowler predicts his Premier League 2026/27 table". https://www.tiktok.com/@premierleague/video/7672427954747575574 . 10 Aug 2026. 2,304,791 views, 216.7K likes, 201 s.
  - Tag size: #premierleaguepredictions 548.36M views, #premierleaguetable 198.74M.
- **Why it works.** Everyone has a different table; the save and the comment are "I disagree with 14th".
- **Outcome version.** The crowd's title-chance table, top 6: Arsenal 60, Man City 20, Chelsea 8, Liverpool 6, Spurs 3, Man United 2. It is a title-chance table, not a points table, because only a winner market exists for the league.
- **Needs.** Winner market (Q198). Easy.
- **Risk.** Peaks in August. In-season it is a weaker slot.

### F10. Ranked-list explainer ("Top 5 ...")

- **Where and length.** TikTok, Shorts. 45 to 70 s.
- **Looks like (inferred).** A numbered countdown, a clip or still per item, a voice, the number-one reveal last.
- **Verified examples.**
  - fubotvcanada (227,150 followers), "The Top 5 highest xG chances this season that DIDN'T result in a goal". https://www.tiktok.com/@fubotvcanada/video/7436835886408486175 . 13 Nov 2024 (older than the 2025 window, but the cleanest example). 1,337,585 views, 89.0K likes, 1.4K shares, 2.0K saves, 62 s.
  - Rory Talks More, "The Premier League xPTS Table". https://www.tiktok.com/@rory_talks_more/video/7407426637211421984 . 26 Aug 2024. 171,815 views, 9.2K likes, 63 s. 214,769 followers (V/F 0.8x).
- **Outlier.** fubotvcanada V/F 5.9x, 6.9x its average likes.
- **Why it works.** A countdown holds people to the end, and everyone argues about the order.
- **Outcome version.** "Top 5 biggest movers on Outcome this week" or "Top 5 Champions League teams by title chance" (Barcelona 23, Bayern 14, Arsenal 13, PSG 13, Real Madrid 11). Type and stills only, so no clip rights are needed.
- **Needs.** A weekly mover scan and a template. Easy with stills, Medium with clips.
- **Risk.** The proof is old (2024). Clips need rights.

### F11. Bar chart race / data timeline

- **Where and length.** TikTok, Shorts. 20 s to 4 min (the 4 minute versions are what is being posted today; shorter is better for Outcome).
- **Looks like (inferred).** Bars or lines moving over time with a counter in the corner.
- **Verified examples.**
  - hai08a (13,539 followers, 223 videos), "Part 1 | Most Valuable Football Players | (2004 to 2026)". https://www.tiktok.com/@hai08a/video/7684092565196410135 . 11 Sep 2026. 306,716 views, 6.7K likes, 240 s.
  - Same page, "Most Followed Footballers on Instagram (2014 to 2026)". https://www.tiktok.com/@hai08a/video/7682287413028244758 . 6 Sep 2026. 107,790 views, 2.1K likes, 120 s.
  - Tag #barchartrace has 177.4M views but I found no football video above 100K in my sample.
- **Outlier.** V/F 22.7x and 7.6x average likes on the first post, so a small page broke out.
- **Why it works.** Watching a lead change is its own payoff. The longer one beat the shorter one, so length is not the problem; a clear race is.
- **Outcome version.** A 20 to 30 s replay of Kane vs Yamal from 1 Oct to today (the lines cross, then split), or "EPL winner race since the market opened". Same data as F2, shown as motion.
- **Needs.** Candle series, a render engine (HTML canvas via headless Chrome, or After Effects as an element). Medium.
- **Risk.** Keep the client's chart untouched if it is shown; label as "price on Outcome".

### F12. Stat duel (A vs B, one stat each, then the %)

- **Where and length.** TikTok, Shorts. 60 to 130 s.
- **Verified examples.**
  - goalwhiz08 (159,381 followers), "Who's dribble is more effective? Messi OR Ronaldo?" https://www.tiktok.com/@goalwhiz08/video/7631232802154974486 . 21 Apr 2026. 171.6K views, 17.9K likes, 1.1K comments, 4.4K shares, 3.1K saves, 133 s.
  - Squawka, "GUESSING who scored more Premier League goals". https://www.tiktok.com/@squawkafootball/video/7435936477340618016 . 11 Nov 2024. 13,512 views, 301 likes, 78 s. 174,210 followers (V/F 0.08x).
- **Outlier.** goalwhiz08 V/F 1.1x and 0.8x its average likes, so an ordinary post. Squawka's quiz was 0.08x.
- **Why it works / does not.** Stat comparisons are an average performer on TikTok. Use one as the hook inside F3 ("Kane vs Yamal in goals and assists"), not as a standalone.
- **Outcome version.** Two stat lines, then "The crowd on Outcome: Kane 66%, Yamal 28%."
- **Needs.** A stat source (FBref, Understat or similar; I did not check their terms). Medium.
- **Risk.** A wrong stat kills trust. Quote the source and date.

### F13. Football facts mini-doc (voice-over, possibly AI voice)

- **Where and length.** TikTok, Shorts. 60 s (all three examples are exactly 60 s).
- **Looks like (inferred).** Narration over stills or clips, a "did you know" hook in the first second, a punchline.
- **Verified examples.**
  - legoat2215 (322,840 followers, 286 videos), "The most dangerous defender in the world: the Red Card King". https://www.tiktok.com/@legoat2215/video/7567039678013132054 . 30 Oct 2025. 8,956,098 views, 171.6K likes, 9.6K comments, 8.3K shares, 13.5K saves, 60 s.
  - Same page, "The ONLY Player in Football History Who Was NEVER Substituted!" https://www.tiktok.com/@legoat2215/video/7691619846357814560 . 1 Oct 2026. 1.39M views, 60.9K likes.
  - romsbayfutbol (576K followers), Hojlund and Portugal clip with an Indonesian caption. https://www.tiktok.com/@romsbayfutbol/video/7691931775777377558 . 2 Oct 2026. 1.31M views, 124.0K likes.
  - Tag #FootballFacts has 4.06B views.
- **Outlier.** legoat2215: V/F 27.7x, 12.2x its average likes, 21.9x the median of five sampled posts (biased high).
- **Why it works.** Curiosity gap and "did you know" sharing.
- **Outcome version.** Filler between market posts. Close the story with one live number only when it fits (for example, after a Kane records story: "the crowd gives him 66% for the Ballon d'Or"). Facts must be checked.
- **Needs.** Script (Claude), AI voice, stills. Medium to hard because of footage.
- **Risk.** Not market content. Image rights, factual errors, AI-voice labels.

### F14. "Invest now" market meme

- **Where and length.** TikTok, Reels. 15 to 60 s.
- **Looks like (inferred).** A player or club clip, a trading-language caption, a chart-up gesture or sound.
- **Verified examples.**
  - mkz1_0 (25,259 followers, 1,636 videos), "Invest now" (Chelsea, Joao Pedro, Cole Palmer). https://www.tiktok.com/@mkz1_0/video/7677714839908764960 . 24 Aug 2026. 1,747,440 views, 209.0K likes, 1.2K comments, 32.3K shares, 9.6K saves, 60 s.
  - Same page, "Top 3 minimum is a must" (Liverpool). https://www.tiktok.com/@mkz1_0/video/7668649145799937313 . 31 Jul 2026. 219.7K views.
- **Outlier.** 13.1x the median of 11 sampled posts from the page, 51.7x its average likes, V/F 69x. Share rate 1.85%.
- **Why it works.** Stock-market language for fandom is understood in one second and gets forwarded.
- **Outcome version.** The same joke with a real line: "Kane: 50% to 66% in 8 days". Say "chance", never "invest" or "buy".
- **Needs.** A human picks the target and the joke. The mover scan can suggest the target. Hard to automate.
- **Risk.** "Invest" reads as financial advice. The client bans promising profit.

### F15. Title-race fan-edit meme

- **Where and length.** TikTok, Reels. 25 to 75 s.
- **Verified examples.**
  - provhl (8,425 followers, 39 videos), "NOT LIKE US" #mancity #arsenal #titlerace. https://www.tiktok.com/@provhl/video/7629905765804854550 . 18 Apr 2026. 3,139,855 views, 376.6K likes, 798 comments, 19.1K shares, 23.0K saves, 47 s. A second post, "19/4, no problem", did 734K views and 79.0K likes on 15 Apr 2026 (link not captured).
  - carmplus (25.5K followers), #arsenal #titlerace. https://www.tiktok.com/@carmplus/video/7626774087746014486 . 9 Apr 2026. 1.80M views, 126.9K likes, 3.8K shares, 76 s.
  - Context: Arsenal won the 2025/26 title (Premier League's own "all FOUR Arsenal Premier League trophy lifts", https://www.tiktok.com/@premierleague/video/7644485095558057238 , 27 May 2026, 1.76M views, 249.3K likes), so Arsenal content has the biggest tribe.
- **Outlier.** V/F 373x. 5.6x average likes (39 videos only, so the average is high).
- **Why it works.** Two huge tribes, a hit song as the joke, bragging rights.
- **Outcome version.** A two-beat post: the meme first, then one last card with the number ("Arsenal title chance on Outcome: 60%"). Never put the number in the middle of the joke.
- **Needs.** A human editor with taste. Hard.
- **Risk.** Song and clip rights. #titlerace has 529M views, so it is crowded.

### F16. 10-second POV / reaction meme with a % chip

- **Where and length.** TikTok, Reels. 6 to 10 s.
- **Verified examples.**
  - noahjpresents (5,840 followers, 392 videos), "Bro was so angry #refereepov". https://www.tiktok.com/@noahjpresents/video/7654197574227791126 . 22 Jun 2026. 1,648,981 views, 139.4K likes, 377 comments, 5.5K shares, 5.8K saves, 6 s.
  - purejokes0 (117,916 followers), "Champions League final". https://www.tiktok.com/@purejokes0/video/7645790126722780438 . 30 May 2026. 1,679,140 views, 127.6K likes, 76.8K shares, 8.8K saves, 10 s, audio "Copines". Second: "Brighton smash Arsenal 3-0". https://www.tiktok.com/@purejokes0/video/7687275213398134019 . 19 Sep 2026. 864.5K views, 61.8K likes, 35.5K shares, 10 s.
  - Official account version: Arsenal, "POV: Frimmy watching The Arsenal win at the Bernabeu. Again." https://www.tiktok.com/@arsenal/video/7494645882726452502 . 18 Apr 2025. 589,664 views, 71.1K likes, 156 s. 14M followers.
- **Outlier.** noahjpresents V/F 282x, 51.9x average likes. purejokes0 53.6x and 26.0x average likes; share rate 4.6% and 4.1%.
- **Why it works.** Ten seconds loops, costs nothing to forward, and the share is the whole point.
- **Outcome version.** After the joke lands, 1.5 seconds of end card: "Arsenal title chance on Outcome: 60%". Or a separate post the next morning with the number.
- **Needs.** A fast human edit. A template version (text joke plus end chip) is possible. Hard.
- **Risk.** Clip rights; speed matters because the joke dies in hours.

### F17. Hot-take text over clips with a market "receipt"

- **Where and length.** TikTok, Reels. 45 to 90 s.
- **Verified examples.**
  - habibx03 (78,063 followers), "YAMAL > RONALDO" with #polymarketpartner. https://www.tiktok.com/@habibx03/video/7664371543010446614 . 19 Jul 2026. 2,812,740 views, 382.6K likes, 8.6K comments, 192.8K shares, 24.1K saves, 47 s.
  - young.kippa (1,279,614 followers), "Arsenal are gonna win the Champions league @Polymarket". https://www.tiktok.com/@young.kippa/video/7636530350302203158 . 5 May 2026. 345,792 views, 38.3K likes, 83 s. And "Bayern Munich are INSANE @Polymarket". https://www.tiktok.com/@young.kippa/video/7626141400580558102 . 7 Apr 2026. 328,639 views, 31.6K likes. Whether these two are paid is UNVERIFIED.
  - Official Polymarket Sports (753,953 followers), "THIS WAS THE WORST OVERTIME OF ALL TIME". https://www.tiktok.com/@polymarketsports/video/7695543607385689362 . 11 Oct 2026. 92,005 views, 8.7K likes, 91 s.
- **Outlier.** habibx03 54.2x average likes, share rate 6.9%. young.kippa 0.6x to 0.7x its average likes, so the tag did not lift it. Polymarket Sports 0.4x.
- **Why it works.** The hot take drives the shares. The market tag is a disclosure, not the hook.
- **Outcome version.** Faceless: text on clips. "Yamal > Ronaldo?" and a last slide "The crowd on Outcome gives Yamal 28% for the Ballon d'Or." The number is the receipt that makes the take checkable.
- **Needs.** Clip supply and a human to write the take. Medium.
- **Risk.** Any paid or per-view post needs the upfront "Ad" label plus the platform label (see 03-platform-rules.md). No "I'm putting my money on this" language.

## 5. Prediction markets inside sports media, 2025 to 2026

- **UFC and Zuffa Boxing.** Polymarket became the official prediction market, announced 13 Nov 2025 (TKO Group, multi-year). A "Fan Prediction Scoreboard" shows live market prices during fights. A social series called "Matchup Predictions: Who's Next?" uses the data. (Covers, Unchained, Decrypt, Cointelegraph.)
- **MLS and Leagues Cup.** Polymarket is "Official and Exclusive Prediction Market Partner", announced 26 Jan 2026. The release talks about "prediction-based insights" and fan sentiment on MLS digital platforms. It does not mention broadcasts or showing odds.
- **OneFootball.** Exclusive deal reported about two weeks before the 2026 World Cup: 200M monthly users, a 645M fan ecosystem (The Defiant). The text I could read does not say how probabilities are displayed.
- **Prime Video and Opta.** Opta Live Win Probability simulates the rest of the match 100,000 times and shows win and draw chances live. Stats Perform says it "sparked online debate" in its first games. Year not shown in what I could read.
- **Seen only in search summaries, not opened: UNVERIFIED.** Polymarket and the Bundesliga for 2026-27, a DAZN tie-up, the New York Yankees (rest of 2026), BLAST esports (2026), SEGG Media's Sports.com Predict, and a BVM Sports match report on 12 Oct 2026 with a "Presented by Polymarket" credit.
- **Creator wave.** #kalshipartner 5.78B views, #polymarketpartner 156M, #polymarketsports 2.4M (13 Oct 2026). The WSJ story (via Quartz, second-hand): 1,105 TikTok videos reviewed, 778 appeared to show a bet, none showed the real site; creators paid $2,000 to $3,000 a month; about 140M views (Tubular). Quartz blocked my fetch, so quote none of this until the WSJ piece is opened.
- **Meaning for Outcome.** Showing a market % beside sport is no longer odd. A faceless page that does only that with real, dated, checkable numbers and a visible price history is the gap. Avoid the voice-over "I bet" skit style that is under scrutiny.

## 6. The big stat brands: what I could and could not verify

TikTok account totals read 13 Oct 2026 (tikwm user/search). Average likes per video = lifetime likes divided by video count.

| Account | Followers | Lifetime likes | Videos | Avg likes per video |
|---|---|---|---|---|
| @433 | 19,198,061 | 676.7M | 5,215 | 129,752 |
| @espnfc | 19,318,919 | 607.6M | 6,060 | 100,267 |
| @onefootball | 8,212,447 | 308.9M | 6,166 | 50,097 |
| @brfootball | 7,396,451 | 138.0M | 3,067 | 45,011 |
| @transfermarkt | 3,660,172 | 132.2M | 3,776 | 34,997 |
| @tifofootball_ | 585,328 | 24.3M | 1,100 | 22,085 |
| @squawkafootball | 174,210 | 6.0M | 837 | 7,127 |
| @statmuse | 47,707 | 3.6M | 388 | 9,182 |
| @optaanalyst | 35,336 | 1.0M | 1,514 | 660 |
| @skysportsfootball | 3,330,134 | 182.6M | 8,459 | 21,587 |
| @dailymailsport | 6.8M (r.jina read; one tikwm read returned 0) | 843.5M | 12,891 | 65,433 |
| @polymarketsports | 753,953 | 27.4M | 1,241 | 22,089 |
| @kalshi | 688,556 | 16.0M | 805 | 19,816 |
| @polymarket | 171,433 (a third-party page listed about 29.5K in Mar 2026) | 6.6M | 970 | 6,766 |

- **GOAL:** the handle @goal on TikTok is a different small account (30,008 followers, 0 videos). The real GOAL handle is UNVERIFIED. FotMob and Sofascore were not found by exact handle either.
- **Which post types get their biggest numbers on these brands:** I could not rank them, because their post lists need the blocked endpoint, and Instagram cannot be read from here. UNVERIFIED. What the averages show: 433 and ESPN FC average 100K+ likes per video across 5,000+ videos, which is a clip-and-news engine, not a stat-graphic engine. StatMuse is small on TikTok (47.7K) and Opta Analyst's TikTok is tiny next to its reputation. The stat-graphic carousels that did well in my sample came from small pages (F9, F11), not from these brands.
- **Next step if you want this answered properly:** send 10 top-post links per brand (any platform) and I run the same pipeline, or let me scan their hashtags.

## 7. Ranked top 8 for a brand-new faceless page

Ranked on proof of demand, fit with real Outcome data, how fully it can be automated, and risk.

| Rank | Format | Why it is here | Proof | Shelf life |
|---|---|---|---|---|
| 1 | F4 Matchday prediction card | Daily, tribal, saved; built from the market list with no human input | 4.07M and 2.34M views on one 287K page | All season |
| 2 | F3 Ballon d'Or poll card | Biggest topic in football right now, comments and saves are high, and fake winner edits leave room for a real number | 491K views and 20.4K saves on a 55K page; #ballondor 34.45B | Until the ceremony (26 Oct, UNVERIFIED) |
| 3 | F2 Race swing card | Needs real moves, and Outcome has them (Kane +16 and Yamal -15 in 8 days) | IFR Polymarket short 9.7x its channel median | All year, post only on moves of 8 points or more |
| 4 | F5 Chart replay at full time | The one format only Outcome can make: the live chart is the product | No proof yet, open ground (#winprobability 177K) | All year, test early |
| 5 | F7 Called-it / upset retrospective | Ties to the client's P&L card and trader stories | Upset meme 2.15M views; market retros alone are weak | All year |
| 6 | F8 Weekly crowd-vs-AI scoreboard (NFL) | A series hook, and paid players are running this exact idea | 4M to 18M views, but paid and passive | NFL season |
| 7 | F11 Race timeline (animated lines) | Same data as F2 as motion, small pages broke out with it | 22.7x followers on a 13.5K page | All year |
| 8 | F6 Market vs model | A new angle with no direct competitor, but needs a weekly outside number | Halves proven, whole unproven | Weekly |

Phase 2, needs a human with taste: F14 "Invest now", F15 title-race edits, F16 10-second reaction memes, F17 hot takes. They have the highest ceilings in my sample (50x average likes, 4% to 7% share rates) and the lowest automation. Try two a week once the daily cards run. Filler only: F13 football facts and F10 ranked lists. Skip for now: F1 on its own (no distribution), F9 outside August, F12 as a standalone (average results).

## 8. Weekly rhythm idea

Matchdays carry the volume, midweek carries the stories. UCL and Europa nights on Outcome this week: Tue 13 and Wed 14 Oct (UCL), Thu 15 Oct (Europa). The Premier League had no match markets in the list on Tuesday, only the title market, so weekends lean on the race. NFL game markets were not listed on Tuesday (UNVERIFIED for Sunday).

| Day | Main post | Reactive post | Notes |
|---|---|---|---|
| Mon | F8 scoreboard result (Week N final) | F7 called-it from the weekend | Recap day |
| Tue (UCL) | F4 card, morning | F5 chart replay or F7 at full time | One card per night |
| Wed (UCL) | F4 card, morning, plus F3 poll card in the evening | F5 or F7 at full time | Peak day: 3 posts |
| Thu (Europa, NFL Thursday) | F4 card, plus F8 "crowd vs AI" lock post | F7 at full time | NFL picks locked before kickoff |
| Fri | F2 swing roundup | F6 market vs model (weekly) | Needs a fresh Opta number |
| Sat (EPL) | F2 if the title chance moved 5+ points | F16 or F14 if a human is on | No EPL match markets |
| Sun (NFL) | F8 scoreboard update at night | F5 chart replay of the biggest swing | Needs weekly NFL markets |
| Midweek, no match | F11 timeline, F10 ranked list, F13 facts | none | Batch these on a free day |

Launch pace: 5 posts a week for the first month (4 cards plus 1 story), same asset on all three platforms with the caption changed. NBA starts later this month (date UNVERIFIED), and its winner market has placeholder prices today, so reuse F2 and F4 for it once real prices appear. I found no verified viral NBA odds or probability example; NBA tags are tiny (#nbaodds 1.7M, #nbatitleodds 37K).

## 9. Risks that apply to every format

1. **Audience geography.** Outcome's terms block the US, UK, UAE, Singapore, Hong Kong, South Korea, China, Ontario, Belgium and others (00-status.md). The biggest football audiences are UK and EU. Decide target countries before launch.
2. **Platform rules.** TikTok's Branded Content Policy (31 Aug 2026), Meta pre-authorisation and YouTube's links rule are in 03-platform-rules.md. Paid or per-view posts need the upfront "Ad" label plus the platform label.
3. **India.** You edit from India; the Online Gaming Act 2025 section 6 point in 00-status.md applies.
4. **Rights.** Club crests, player photos and broadcast footage. The type-only cards in F2, F3, F4, F6, F10, F11 avoid most of it.
5. **Market integrity.** Do not post a price that is a placeholder or on a thin book, and do not tell people to move a price.
6. **Fake-bet content.** Always show the real event and real market. Keep realistic numbers (client demo rule).
7. **Wording.** Say "% chance", "the crowd", "your call". Avoid bet, odds, tips, picks, invest, lock, guaranteed.
8. **AI voice and AI labels** where a platform requires them.

## 10. Open items for you

1. Paste 5 to 10 Instagram post links (stat carousels, Opta, Squawka, B/R, 433) and I will run the embed route, since Instagram could not be measured.
2. Do you want crests and player photos, or type-only cards?
3. May I ask Outcome whether a redrawn chart is acceptable under "never cover the chart"?
4. Is a weekly hand-copied Opta number fine for F6?
5. Which countries are the target audience?
6. Are you comfortable with the F8 "crowd vs ChatGPT" comparison, given that Kalshi-linked creators run the same idea?

## Appendix A. Real Outcome data pulled 13 Oct 2026 (about 06:23 PC local time)

Source: public Hyperliquid info API. No key. Three POST calls to https://api.hyperliquid.xyz/info with a JSON body:

- `{"type":"outcomeMeta"}` lists outcomes and questions (313 outcomes, 35 questions). A question has a template, a description (competition, participants, scheduledStart, stage, resolution rules), named outcomes and a fallback outcome.
- `{"type":"allMids"}` gives mid prices. The coin key for an outcome is `#` plus the outcome id plus a side digit: 0 is Yes, 1 is No. Example: Kane to win the Ballon d'Or is outcome 8657, so Yes is `#86570`.
- `{"type":"candleSnapshot","req":{"coin":"#86570","interval":"1d","startTime":ms,"endTime":ms}}` gives price history (open, close, high, low, volume, trades). Also `{"type":"l2Book","coin":"#86570"}` for the order book.

Caveats: an outcome with no book shows a placeholder mid of exactly 0.50 ("template fallback" rows too). Check candle volume or the book first, and check that the Yes prices in a market add to about 100%.

**Markets (mid prices, % chance):**

- Ballon d'Or 2026 (Q391): Kane 66, Yamal 28, Messi 3, Dembele 2, Mbappe 2.
- Premier League winner 2026/27 (Q198): Arsenal 60, Man City 20, Chelsea 8, Liverpool 6, Spurs 3, Man United 2.
- Champions League winner 2026/27 (Q199): Barcelona 23, Bayern 14, Arsenal 13, PSG 13, Real Madrid 11, Man City 7.
- NFL Super Bowl winner 2027 (Q200): Rams 11, Bills 10, Chiefs 10, Seahawks 9, Ravens 9, Cowboys 2.
- NBA winner 2026/27 (Q430): mixed with placeholders (Minnesota 52, Boston 50 and Miami 50 look like placeholders next to Cleveland 25, San Antonio 23, Oklahoma City 20). Do not publish until a book check is done. MLB championship (Q250) is all placeholders.
- UCL matchday 2, home / draw / away: Arsenal v Lille 80 / 14 / 6 (13 Oct). Atletico v Man United 51 / 24 / 25 (13 Oct). Galatasaray v Barcelona 10 / 13 / 77 (13 Oct). Inter v Club Brugge 78 / 14 / 8 (13 Oct). Viking v Bayern 4 / 7 / 89 (13 Oct). Villarreal v Napoli 45 / 25 / 29 (13 Oct). RB Leipzig v PSV 56 / 20 / 24 (13 Oct). Man City v PSG 45 / 23 / 32 (14 Oct). Roma v Real Madrid 26 / 24 / 51 (14 Oct). Aston Villa v Fenerbahce 59 / 22 / 18 (14 Oct). LASK v Liverpool 10 / 14 / 76 (14 Oct). Bodo/Glimt v Dortmund 30 / 23 / 47 (14 Oct). Europa League matchday 2 on 15 Oct also listed.

**Daily closes, % chance (UTC days; the last day is partial):**

- Kane, Ballon d'Or: 5 Oct 50, 6 Oct 48, 7 Oct 49, 8 Oct 54, 9 Oct 61, 10 Oct 64, 11 Oct 66, 12 Oct 66, 13 Oct 66. Volume 772,402 shares over the nine days.
- Yamal, Ballon d'Or: 5 Oct 43, 6 Oct 45, 7 Oct 44, 8 Oct 39, 9 Oct 28, 10 Oct 30, 11 Oct 28, 12 Oct 29, 13 Oct 28. Volume 325,415 shares.
- Arsenal, EPL winner: 58 (28 Sep), 58, 60, 61 (1 Oct), 61 through 8 Oct, 62 (9 Oct), 61, 61, 60, 60 (13 Oct).
- Man City, EPL winner: 23 (28 Sep), 19, 22, 18, 18, 21, 21, 21, 21, 20, 21, 20, 18, 20, 20, 20 (13 Oct).
- Barcelona, UCL winner: 22 to 23 every day from 28 Sep to 13 Oct. Arsenal, UCL winner: 13 every day.

## Sources (all read 13 Oct 2026 unless marked)

**Tools and endpoints.**
- tikwm.com root endpoint https://tikwm.com/api/?url=<video url> (per-video stats); https://www.tikwm.com/api/user/search , /challenge/search , /challenge/posts (account totals, hashtag lists). user/posts, user/info and feed/search returned a Cloudflare challenge.
- r.jina.ai reader for TikTok profiles (followers), YouTube pages and channel Shorts lists.
- Hyperliquid info API https://api.hyperliquid.xyz/info (POST).

**Articles and pages.**
- Opta Analyst, Premier League predictions 2026-27, article dated 14 Aug 2026 (simulations run 13 Aug): https://theanalyst.com/articles/premier-league-predictions-2026-27
- Sports Illustrated, "Supercomputer predicts final 2026-27 Premier League table after Arsenal's perfect start" (figures 45.18% and 22.05% seen in a search summary, page not opened): https://www.si.com/soccer/supercomputer-predicts-final-2026-27-premier-league-table-arsenal-perfect-start
- Empire of the Kop, 8 Apr 2026, "Supercomputer gives Liverpool just 24.3% chance vs PSG": https://www.empireofthekop.com/2026/04/08/supercomputer-gives-liverpool-just-24-3-chance-vs-psg/
- Stats Perform, "Explained: what is win probability and how does it work" (fetch returned 403; facts from a search summary): https://www.statsperform.com/news/explained-what-is-win-probability-and-how-does-it-work
- Polymarket and UFC, 13 Nov 2025: https://www.covers.com/industry/polymarket-becomes-the-official-prediction-market-of-ufc-nov-13-2025 , https://unchainedcrypto.com/ufc-partners-with-polymarket-to-launch-real-time-fan-prediction-scoreboard-in-live-fight-broadcasts/ , https://decrypt.co/348502/ufc-parent-tko-signs-polymarket-exclusive-prediction-market-deal , https://cointelegraph.com/news/polymarket-bring-real-time-forecasting-ufc-broadcasts
- Soccer United Marketing and Polymarket (MLS, Leagues Cup), 26 Jan 2026: https://www.mlssoccer.com/news/soccer-united-marketing-and-polymarket-announce-multi-year-partnerships-with-major-league-soccer-and-leagues-cup
- The Defiant, Polymarket and OneFootball (about two weeks before the World Cup): https://thedefiant.io/polymarket-plugs-into-onefootballs-645m-fan-network-two-weeks-before-the-world-cup
- Quartz on the WSJ creator story (fetch returned 403; details from a search summary): https://qz.com/polymarket-fake-bets-creators-influencers-us-users-062226
- Seen only in search results: https://marketingdive.com/news/campaign-trail-polymarket-bets-on-celebs-to-build-its-own-ad-universe/832012 , https://bvmsports.com/2026/10/12/paul-george-makes-his-debut-vs-a-shorthanded-76ers-team/ , https://streamer.guide/blog/blast-polymarket-partnership-2026 , https://affpapa.com/polymarket-becomes-new-york-yankees-prediction-partner/

**Project files read.** 00-client-brief.md, 00-status.md, 01-what-is-outcome.md (endpoint notes) in this folder.

**Every TikTok and YouTube link used is inside the format sections above, with its post date.**
