# 11. Faceless formats for prediction markets and trading (researched 13 Oct 2026)

Scope: what is working in 2025 to 2026 for faceless TikTok, Instagram, YouTube Shorts and X pages that talk about prediction markets (Polymarket, Kalshi, Hyperliquid HIP-4 venues) and trading. Built for the Outcome (outcome.xyz) page network. All dates UTC. All counts were read on 13 Oct 2026 and will have moved. Nothing was downloaded; only page data and JSON text were read.

Read this first (3 caveats)
1. tikwm.com is now behind a Cloudflare bot challenge (direct and through r.jina.ai). I did not try to get past it. TikTok numbers below come from TikTok's own page data read through the r.jina.ai raw-HTML reader (video page = views, likes, comments, shares, saves, date, author followers; creator embed page = a small account's latest posts). Verified accounts (Polymarket, Kalshi, Polymarket Sports, 60 Minutes) return an empty list, so their top-post lists come from the third-party Socialpruf site and most of those posts no longer open.
2. Instagram shows no reel numbers to a logged-out reader, so I have NO post-level Instagram data for the official accounts (UNVERIFIED). Small-page Instagram numbers are reused from 02-reference-posts.md.
3. Outlier score = views divided by the median views of the account's recent posts. YouTube: median of the latest 48 Shorts on the channel page. TikTok: median of the latest posts the embed page lists (n shown). X shows no views and no follower counts to a logged-out reader, so X rows give likes and compare with the same account's other posts. A hit older than the sample window can show an inflated ratio; I say so where it applies.

---

## 1. Format table (18 formats)

Evidence: STRONG = 3+ verified posts, MEDIUM = 2, WEAK = 1 or none. Automation: Easy = data plus a template, Medium = data plus some assets or human picking, Hard = footage, rights or manual work. Rank = position in the top 8 for a brand-new faceless page (section 2).

| # | Format | Best platform | What it looks like | Best verified proof (views / likes, account size, outlier) | Outcome version | Automation | Risk | Evidence | Rank |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Odds-move "BREAKING" card | X, then TikTok photo / IG carousel | One headline line with a record high or low, the new %, two chart images | @Polymarket 14,865 likes (20 Sep 2026), 9,550 likes (21 Sep 2026); same account median of 7 posts read = 2,066 likes (x7.2) | "BREAKING: Outcome traders now price [team] at X% for the [UCL], was Y% yesterday", real market chart left uncovered | Easy | Low | STRONG (official accounts), weak for fan copies (141 likes) | 2 |
| 2 | Football favourites ranking | TikTok, Shorts, X | Top 5 list with flags or kits, % beside each name, 60 to 90 s or 3 to 5 slides | @wolusfcb 2.3M views / 157.1K likes, 280.8K followers (x22.1); @zone2.foot 328.3K views, 192.2K followers (x56.2); Short "Chances Of Winning The Ballon D'or 2026" 802K views (x17.6) | Ballon d'Or, EPL winner, UCL winner, Golden Boot from live Outcome prices, with 7 day change arrows | Easy | Low to medium (image rights) | STRONG | 1 |
| 3 | Daily odds table series | X, IG story / carousel | Same template daily: title, rows of Name + % + (+/- vs yesterday) | @KalshiPolitics 3,183 likes (12 Oct 2026); @KalshiFC 4,503 likes (7 Sep 2026) | "UCL WINNER ODDS ON OUTCOME (+/- vs yesterday)" every day, same slot | Easy | Low | MEDIUM | 4 |
| 4 | Real trade payout story (flash card or 45 s narrated) | X, Shorts, TikTok | Stake, odds, twist, payout: "$20 -> $20,000"; or a trader's streak told over screenshots | @PolymarketSport 10,167 likes (8 Oct 2026); Short "He made $70k predicting the price of eggs" 97.5K views, 1.95K-sub channel (x48.8); Short "From $28 to $29k in 3 weeks" 182.2K views, 369-sub channel (x70) | Real resolved trade from the Outcome leaderboard, with market, side, entry price, payout and date; "$100 -> $375" style line from the UI | Medium | HIGH if staged (this is the format Polymarket was sued over); medium with real on-chain trades | MEDIUM | 3 |
| 5 | P&L card over an edit | TikTok | 13 s, big card with a green number over a film or meme edit, loud sound, one caption line | @jackpot_0_ 226,900 views / 28.8K likes, 1,182 followers (x22.2). Its other 4 posts: 2.7K to 11.3K | Real Outcome P&L card (dev.jbfx.me /api/card) over an edit, CTA "Trade with zero fees on Outcome.xyz" at the bottom | Medium | Film-clip copyright; fake-win risk low if the card is real | WEAK (1 verified hit) | 5 |
| 6 | Top traders carousel | TikTok photo, IG carousel | Hook slide, #3, #2, #1, CTA; big number over each trader's profile and chart | Brief's example @cryptodailyfeed is removed (TikTok: "author_status, status_audit_not_pass"); no replacement found | "Top 3 traders on Outcome in the last 24 hours" from /api/leaderboard?duration=24h | Easy | Medium (profit display, usernames, the example was removed) | WEAK, unproven in this niche | 7 |
| 7 | Big-trade alert feed | X (trust feed only) | Fixed template: market, size, price, potential payout | @whalewatchpoly 0 to 4 likes on 5 alerts; Shorts "Whale Alert" 22 views; story version @lookonchain 874 likes | "Biggest Outcome trade today", then a follow-up when it settles | Easy | Medium (wallet privacy, implied insider claims) | STRONG (that raw alerts flop) | no |
| 8 | Unusual-trade news explainer | TikTok, Shorts, X | News footage or cards, a time gap ("hours before"), a big number, a mystery | @60minutes TikTok 753.7K views / 69.2K likes; Bloomberg Short 399K views; DeFranco Short 1.26M views | Only when a real Outcome trade or a news event gives a clean time gap; wording "unusual timing", never "insider" | Medium | High (defamation, insider accusations, India law) | STRONG for demand | 6 |
| 9 | "The market says" reaction clip | Shorts, TikTok | A celebrity, streamer or meme clip plus a market screenshot: "according to the market there is a 7% chance" | John Casterline Short 6.2M views / 291.3K likes (x3.3); ChaosOdds Short 507.8K views, 1.32K subs (x109); ClipHype Short 101K views, 728 subs (x24.6) | Outcome market screenshot after a trending sports or crypto moment | Hard (footage rights) | Medium to high (clip copyright, disclosure) | MEDIUM | no |
| 10 | Clip with a live odds-line banner (clipper format) | Shorts, TikTok, IG Reels, X | Sports or meme clip, banner above the bottom 30% with a % line that moves with the action | DoomScroll Rankings Short 8.48M views / 182.4K likes, 26.8K subs (x652 vs latest 48, hit is older than the sample); Polymarketupdates Short 8.33M views, 15.3K subs (x278) | Outcome banner using the REAL price history of the match window, never a simulated line | Hard | HIGH (paid clipping, undisclosed ads, simulated line = deceptive, footage rights) | STRONG for reach | no |
| 11 | Sports moment clip + caps caption (Polymarket Sports recipe) | TikTok | Highlight clip, one shouting line, 4 to 5 hashtags, no odds on screen | Polymarket Sports TikTok (753.9K followers): avg 139K views per post, top post 4.2M views (Socialpruf, posts no longer open: UNVERIFIED) | Not recommended for a new page without footage rights | Hard | Footage copyright; IG originality rule (30 Apr 2026) | MEDIUM | no |
| 12 | How-it-works explainer / how-to | TikTok, Shorts, IG | Screen-record or 5 slides: find a market, read the %, what a YES share pays | 60 Minutes Short "What is Polymarket?" 401K views; Economist TikTok 86.6K views / 4,246 likes; TikTok Discover pages show standing search demand | "How a YES share pays $1 on Outcome" with one real market and the UI payout line | Medium | Medium (the brief's title "turn your predictions into profit" is a profit promise: change it) | MEDIUM (demand), weak (reach) | 8 |
| 13 | Challenge diary ("Day N") | Shorts, IG | Serial: "Day 2 of turning $100 into $100k" | Walter Blake Knoblock Short 93.4K views, 115K subs (x7.8). Safe variant, no money: @rynssport IG 9,524 likes on 284 followers | "Day N of predicting the UCL, here is what the market said" (no stake) | Medium | HIGH with money (profit-promise, "make money online" signal); low without | WEAK | no |
| 14 | AI agent or bot experiment | Shorts, TikTok | Screen-record plus voice: "I let an AI read the market" | Ray Fu Short "How to build prediction trading market bots with Claude" 292.8K views / 13.1K likes | AI reads Outcome prices and posts a scoreboard of predictions (no money claims) | Medium | Medium to high (results claims) | WEAK to MEDIUM | no |
| 15 | Wallet / KOL PnL tracker and copy-trading talk | TikTok, Shorts | Wallet list, PnL numbers, "see the data, link in bio" | @solana_trading best post 5,103 views, 7,355 followers (x6.7), others 405 to 1,044; Tanja Trades Short "The truth about copy trading" 295.6K views (x22.7) | "What the top Outcome wallets hold today" (open positions are public) | Easy | Medium (copy-trading = financial promotion) | WEAK | no |
| 16 | Sponsored game-sim predictions (#PolymarketPartner) | Shorts | Game footage, voiceover: "I predicted the rest of the World Cup" | ASP FC Short 5.50M views / 115.1K likes, 901K subs (x4.1); Thogden Short 3.40M views, 2.7M subs (x12.5) | A UCL or EPL prediction series run on game footage | Hard | Paid disclosure, production load | MEDIUM | no |
| 17 | Live market resolution moment | TikTok, Shorts | Last 60 s of a 15-minute crypto market, price chart, tense music, result card | @loganpaul clip on Polymarket's TikTok 1.5M views / 73.2K likes (face, 17 Apr 2026). Faceless supply side NOT found | Result card for each BTC 15m window ("went UP, YES paid $1") | Medium | High (fast-gambling feel; keep to results, not instructions) | WEAK | no |
| 18 | Trader comedy skits (reference only) | Shorts | Character sketch about traders; one version has a Polymarket plug | Yeti dyor Short 52.5M views / 767.7K likes (x8.9); Pino Short 106.1M views / 685.2K likes | Not buildable faceless; use as a partnership target | Hard | Sponsor disclosure | MEDIUM | no |

---

## 2. Ranked top 8 for a brand-new faceless page

Scoring: reach shown by small accounts, fit to Outcome's live markets, ease of automating with real Outcome data, and risk. Week 1 launch set = 1, 2 and 3 (they share one data feed and one template engine).

1. Football favourites ranking (format 2). Three separate small accounts hit x17 to x56 on "who is the favourite" lists with no market data at all (wolusfcb, zone2.foot, football fans). Outcome has Ballon d'Or, EPL winner, UCL winner live. Adding a real Outcome % is the only differentiator needed. Easy, low risk. Avoid player photos until rights are sorted (use names, flags, club colours).
2. Odds-move "BREAKING" card (format 1). The two biggest official X posts in this research are this format (14,865 and 9,550 likes). Trigger: a 24 hour move above N points or a record high or low on an Outcome market. Easy, low risk, but X audience is built over time, so cross-post as a TikTok photo post and an IG carousel.
3. Real trade payout story (format 4). Highest proof of shareability (10,167 likes on X; x48 to x70 on tiny Shorts channels). Use only real, resolved, on-chain Outcome trades with date and market shown. It is also the format that got Polymarket sued, so the guardrails in section 4 are not optional.
4. Daily odds table (format 3). Low reach per post, but the cheapest series to run and it builds a habit slot ("UCL winner odds, today"). Use as the daily baseline between bigger posts.
5. P&L card over an edit (format 5). The client's own reference. One verified hit (x22.2) and four siblings at 2.7K to 11.3K, so plan for a 1 in 5 hit rate, not a guarantee. Use licensed or stock footage, not film scenes.
6. Unusual-trade news explainer (format 8). Biggest raw demand (60 Minutes 753.7K views, DeFranco 1.26M, Bloomberg 399K) but event-driven and legally the touchiest. Run only when a real, checkable event exists.
7. Top-3 traders carousel (format 6). Outcome-native data, trivial to build, but the brief's example is gone and I found no proof it works in this niche. Test for two weeks with a strict cap.
8. How-it-works explainer (brief format 1, format 12 here). Standing search demand (TikTok Discover pages), low virality. Keep wording free of "profit" promises.

Not recommended for a new page: 10 (banner clips) and 11 (sports clips) because of footage rights, undisclosed-ad risk and the IG reposting rule; 13 with money; 17 until a faceless version is proven.

---

## 3. Detail per format

Each block: look, verified examples (link, platform, date, numbers, account size, outlier, how I read it), why it works, the Outcome version with real data, what to automate, risk. "Read via" says which route gave the numbers.

### Format 1. Odds-move "BREAKING" card

Look: one text line in news voice with a record or all-time move and the new % ("surges to an all-time high ... 58% chance"), two attached chart images (the market chart screenshot and a second view). No logo overlay. No music (X); on TikTok/IG the same two images become a photo post.

Examples (X, read via X's public tweet-data endpoint: likes and replies only):
- https://x.com/Polymarket/status/2101683638064607551 : 20 Sep 2026, 14,865 likes, 581 replies, 2 images. "BREAKING: Flavio Bolsonaro surges to an all-time high in Brazil's presidential election odds, with the first round just two weeks away. 58% chance." Account follower count UNVERIFIED (not shown logged out). Against the median of the 7 @Polymarket posts I read (2,066 likes): x7.2.
- https://x.com/Polymarket/status/2102072830858817830 : 21 Sep 2026, 9,550 likes, 1,424 replies, 2 images. "Vivek Ramaswamy crashes to a record low in the odds to win Ohio's governor race. Democrat Amy Acton now favored at 58%." x4.6. The 1,424 replies show people arguing about the number.
- https://x.com/Polymarket/status/2023899611224482162 : 17 Feb 2026, 3,333 likes, 637 replies. Odds of a religious return doubled to 6%. The same account's weaker posts: 2,066 likes (NVIDIA earnings odds collapse, 19 Nov 2025), 1,646 (6 Jul 2026), 853 (18 Aug 2026).
- Kalshi version: https://x.com/KalshiSports/status/2087543566117503392 : 12 Aug 2026, 1,219 likes, "Harry Kane's Kalshi odds to win the Ballon d'Or have reached an all-time high of 60%". https://x.com/Kalshi/status/2017259629797933301 : 30 Jan 2026, 790 likes (Fed chair market, about $100M traded).
- Fan-page copy that did NOT travel: https://x.com/PolymarketMoney/status/2066602393320427955 : 15 Jun 2026, 141 likes. https://x.com/GrindeOptions/status/2109666607928848824 : 12 Oct 2026, 21 likes.

Why it works: it reads as news, not as an ad. The hook is a record (all-time high, record low) plus a short clock ("first round two weeks away"). People send it because the % is a claim they can argue with. Replies are the engagement signal.
Outcome version: pull the market price series; post when a price moves 10+ points in 24 hours or sets a record high or low. Text: "Outcome traders now give [team] a X% chance to win the [competition] (was Y% yesterday)." Keep the market chart image untouched and add the plug line and "Trade with zero fees on Outcome.xyz" only as plain text outside the chart.
Automation: data = Outcome market prices (o1.outcome.xyz/api/v1 is undocumented; Hyperliquid public info API is the stable fallback), a trigger rule, an HTML card template, a human check. Easy.
Risk: low. Do not say "the world's most accurate"; Outcome's volume is small (HIP-4 about $14.7M a week against Polymarket about $3.6B per 01-what-is-outcome.md), so write "Outcome traders", not "the crowd". Not financial advice line. X bans gambling in paid partnerships (03-platform-rules.md).

### Format 2. Football favourites ranking

Look: a ranked list of 5 names with flags, kits or numbers; TikTok 60 to 90 s with a voice or text-to-speech, or 3 to 5 slides; the headline claims a favourite ("X IS THE FAVOURITE TO WIN THE BALLON D'OR") with a siren emoji.

Examples:
- https://www.tiktok.com/@wolusfcb/video/7654311092851690774 : TikTok, 22 Jun 2026, 2.3M views, 157.1K likes, 3,686 comments, 19.9K shares, 8,170 saves, 72 s. Account 280.8K followers, median of its 11 listed posts 104.2K views, so x22.1. Read via TikTok page data.
- https://www.tiktok.com/@zone2.foot/video/7640285221828562208 : TikTok, 16 May 2026, 328.3K views, 26.3K likes, 626 comments, 261 shares, 4,630 saves, 89 s. Account 192.2K followers; median of 13 posts 5,842 views, so x56.2. French-language list of five favourites.
- https://www.youtube.com/shorts/kQx4hPOzoTE : "Chances Of Winning The Ballon D'or 2026..." football fans channel (143K subs), 27 Sep 2025, 802,065 views, 3,452 likes. Channel median (latest 48 Shorts) 45.5K, so x17.6.
- https://www.youtube.com/shorts/grnkw1ODXbM : "Ballon d'Or Contenders: Goals vs Assists" BALLIX FOOTBALL (8.39K subs), 11 Oct 2026, 347,178 views. Channel median 18K, so x19.3. A stat-comparison version of the same idea.
- https://www.youtube.com/shorts/cSEkxRnddQg : "The Craziest Ballon d'Or 2026 Race Ever?" MadridZone (5.93K subs), 24 Sep 2026, 245,640 views, 1,674 likes, x4.7.
- Official-brand X versions: https://x.com/PolymarketSport/status/2067640740931322188 (18 Jun 2026, 5,262 likes: Golden Boot odds with flags, "$200 on Yamal pays out $10,000"); https://x.com/KalshiFC/status/2096958875392004112 (7 Sep 2026, 4,503 likes: current Ballon d'Or chances the day before the nominees).
- Official account with no market data: https://www.tiktok.com/@ballondor/video/7663815219788991777 : 18 Jul 2026, 1.7M views, 219.2K likes, 8.8M followers ("100 days to go"). Shows how much traffic the topic carries.

Why it works: fan identity. A ranking is a debate starter ("where is my player?"), so comments and shares are the trigger, and the list is easy to send to a friend. The three small-account hits contain no market data at all, so the topic is the engine and the market % is a credibility add-on.
Outcome version: Outcome has live Ballon d'Or, EPL winner, UCL winner markets (biggest volumes: UCL winner $2.4M, EPL winner $2.2M per the client brief). Card: "BALLON D'OR: WHO DO OUTCOME TRADERS BACK?" top 5, price as %, arrow for 7 day change, CTA slide. Second slide: "$100 -> $X" style payout line for the favourite, copied from the UI.
Automation: data = prices from the Outcome series API; assets = flags, club colours, a typeface; player photos need rights (avoid or use licensed). Easy.
Risk: low. Keep "may change", add not financial advice. Do not claim the market "predicts" the winner.

### Format 3. Daily odds table

Look: a title in caps, 2 to 6 rows, each "Name: X% (+/- change from yesterday)", coloured tags, two images.
Examples:
- https://x.com/KalshiPolitics/status/2109635033979847156 : 12 Oct 2026, 3,183 likes, 191 replies. "TEXAS SENATE WINNER ODDS: (+/- change from yesterday)". Follower count UNVERIFIED.
- https://x.com/KalshiFC/status/2096958875392004112 : 7 Sep 2026, 4,503 likes (see format 2).
Why it works: a recurring slot people check; the +/- column is the news. Weak per post, strong as a habit.
Outcome version: "UCL WINNER ODDS ON OUTCOME (vs yesterday)", "EPL WINNER", "NFL WEEK X GAMES", "BTC 15m: last 8 results". One template, many markets.
Automation: data = daily snapshot job saving yesterday's prices; template; scheduler. Easy.
Risk: low. Same wording rules as format 1.

### Format 4. Real trade payout story

Look: (a) flash: one card or 15 s video, stake, entry odds, twist, payout ("$20 into $20,000"); (b) 45 s narrated story over screenshots with a person's streak or a freak result.
Examples:
- https://x.com/PolymarketSport/status/2108223688755786041 : X, 8 Oct 2026, 10,167 likes, 196 replies, video. "A Polymarket user put $20 on UNDER 7.5 runs in Yankees-Rays at 0.1% odds after a home run made it 4-4... Officials then overturned the HR for fan interference & no more runs scored, turning $20 into $20,000." Follower count UNVERIFIED.
- https://www.youtube.com/shorts/xryOs7hP7JE : "He made $70k predicting the price of eggs on polymarket", Three Markets podcast channel (1.95K subs), 9 Sep 2025, 97,542 views, 1,688 likes. Channel median 2.0K (only 9 Shorts), so x48.8. Description says it is entertainment content.
- https://www.youtube.com/shorts/cXSNJEz_18s : "From $28 to $29k in 3 weeks", Gorilla Predictions (369 subs), 4 Dec 2025, 182,178 views, 2,569 likes. The channel lists only 4 Shorts (median 2.6K), so x70 is shaky. What the video shows is not verified: UNVERIFIED that the trade is real.
- Weak version: https://x.com/marlowxbt/status/2015814991484461335 : 26 Jan 2026, 118 likes, "He lost everything in 2024... deposited his last $500... Two months later: $251K profit" (a wallet story with a hex address).
Why it works: a tiny stake, a huge multiple, a twist the viewer can retell in one sentence. Send trigger: "no way". Disbelief drives shares and comments.
Outcome version: pick a REAL resolved trade from outcome.xyz/leaderboard (the all-time #1 in the client brief is +$503,008 realised from 2 trades; smaller, more relatable ones exist daily). Show market name, side, entry price, shares, payout, settle date, and a line "One resolved trade, not typical." Use the card the dev.jbfx.me /api/card route renders.
Automation: data = /api/leaderboard, /api/trader, /api/positions, /api/card (fan-built, so stability is a risk; the Hyperliquid info API is the on-chain cross-check). A weekly human check that the trade is real on-chain and that the user name may be shown. Medium.
Risk: the highest in the set. The Polymarket scandal was exactly staged wins on lookalike sites (WSJ via The Block, 21 Jun 2026, see 03-platform-rules.md). Rules for us: only real settled trades; no mock-ups; no "you could"; no "turn $X into $Y" promise wording; stake sizes realistic; show date; include "not financial advice". Samples that show only wins are cherry-picking, so also post a loss or a flat day now and then (a "Biggest loss of the week" card is real data and builds trust).

### Format 5. P&L card over an edit

Look: 13 s vertical video, a large P&L card with background removed over a film scene or meme edit, a loud hype sound, a one-line caption with 4 to 5 hashtags. Per the brief the card is the Outcome share card.
Example (the only verified viral one):
- https://www.tiktok.com/@jackpot_0_/video/7676843272941325590 : TikTok, 22 Aug 2026, 226,900 views, 28.8K likes, 295 comments, 1,438 shares, 3,375 saves, 13 s, original sound, caption "Memecoins are so back" plus 5 hashtags. Account 1,182 followers, 56.8K total likes, only 5 posts ever, all between 13 and 22 Aug 2026. Median of the 5 = 10,200 views, so x22.2. The four siblings: 11,300 / 10,200 / 9,360 / 2,681 views. I did not see the picture; "P&L card over an edit" is per the brief.
- Meme cousin on Instagram (from 02-reference-posts.md): shant.tradez, 27 Jul 2026, 11,918 likes on 775 followers, "bro made $40,000,000 and now he just aura farms".
Why it works: the number is the thumbnail; the edit supplies mood; the sound does the retention. The hit-rate is the lesson: 1 of 5 posts took off, the rest sat at the account's floor of about 10K.
Outcome version: the card shows "You predicted NO ... $0.20 -> $1.00, bought $4,780, earned $24,000" (the brief's sample). Use real settled trades only. Place the card inside the safe area, never over the Outcome logo or the chart inside the card, and put "Trade with zero fees on Outcome.xyz" as bottom text. See the client rule on "zero fees" wording in 01-what-is-outcome.md (close fee exists).
Automation: data = /api/card PNG; assets = royalty-free footage library and background-removal for the card, sound licence. Medium.
Risk: copyright of film scenes (use licensed or stock footage). Fake-win risk low if the card is real. Platform risk: money-flex content can be flagged as financial promotion.

### Format 6. Top traders carousel

Look: 5 slides: hook (movie still plus "TOP 3 TRADERS ON Outcome IN THE LAST 24 HOURS"), #3, #2, #1 (big 3D number over the trader's profile banner and P&L chart), CTA "Think you can make the list?" (per the brief).
Evidence:
- The brief's example https://www.tiktok.com/@cryptodailyfeed/photo/7675106142749494559 (17 Aug 2026 by ID): TikTok's page data now says the author or the audit did not pass ("author_status,status_audit_not_pass") and the account's creator embed lists no posts. So the example was removed or restricted. Old follower figure (~832K) is from a search result, UNVERIFIED.
- Demand signals only: TikTok Discover page "How to See Who The Top Traders Buy into on Kalshi" and a Nomos Polymarket leaderboard post surfaced in search (UNVERIFIED, not opened). YouTube long form "Meet the Internet's Richest Kalshi Trader" (Champ) has 108,731 views (7 months old), shows curiosity about top traders.
Why it should work: ranking plus a face-free "who is winning" window; rankings are saved. But I have no verified small-account hit, and the one example is gone, so treat it as a test.
Outcome version: /api/leaderboard?duration=24h&limit=3, then /api/trader for each profile image and chart. Real usernames are public on outcome.xyz/profile, but get the client's written okay before showing names or P&L cards.
Automation: Easy (data + template).
Risk: medium. Removal risk is shown by the example. "Think you can make the list?" is fine; never "you can earn".

### Format 7. Big-trade alert feed (and its story upgrade)

Look: a fixed template: market, side, amount, price, potential payout, one comment line.
Evidence of failure:
- https://x.com/whalewatchpoly/status/1974992908567605547 (6 Oct 2025, 4 likes), https://x.com/whalewatchpoly/status/1976412924181643775 (9 Oct 2025, 0 likes), https://x.com/whalewatchpoly/status/1964982237549457906 (8 Sep 2025, 0 likes, 1 reply). Template "Market, Bought, Odds, Potential Win" with sports markets and a $35K to $60K size. The account is labelled "Polymarket Traders" by X (an affiliated badge).
- https://www.youtube.com/shorts/rS8o05AxFVA : "Polymarket Whale Alert - Big Money Just Moved", 22 views. https://www.youtube.com/shorts/3HhAiONB2sw : "Polymarket Whale Lost $1.8 million on UFC!", predictionist channel (96 subs, median 199 views), 11 May 2026, 2,057 views, 20 likes, x10.3.
Contrast, the story version: https://x.com/lookonchain/status/2007639475497881625 : 4 Jan 2026, 874 likes, 101 replies, 3 images, Paraphrase of the post: three wallets, described by the poster as insiders, took positions on Maduro leaving office just hours before his arrest, for a reported profit of $630,484, and the wallets were created and pre-funded days in advance. Follower count UNVERIFIED.
Why raw alerts fail: no stakes for the viewer and no reason to share. What lifts it: a named outcome, a time gap and a question.
Outcome version: use alerts only as a trust feed on X (automated, every big Outcome fill), and turn the best one each week into a story card ("Largest trade this week: $X on Y at Z cents. Result: ...").
Automation: Easy for alerts (Hyperliquid info API fills filter), Medium for stories.
Risk: medium. Do not publish wallet addresses of ordinary users; do not hint at insider knowledge.

### Format 8. Unusual-trade news explainer

Look: news footage or text cards, a clock ("hours before"), a total ($2.4 million, $630,484), a win rate (98%), a mystery. 60 to 100 s.
Examples:
- https://www.tiktok.com/@60minutes/video/7641011689969732878 : TikTok, 17 May 2026, 753,700 views, 69.2K likes, 825 comments, 8,205 shares, 8,911 saves, 101 s, 3.5M followers. Paraphrase: nine connected Polymarket accounts made about $2.4 million trading almost only on U.S. military operations, with a 98% win rate (Bubblemaps analysis). No outlier (embed list not available for this verified account).
- https://www.youtube.com/shorts/STGxF5B3mTg : Bloomberg News, 23 Apr 2026, 399,069 views, 8,719 likes (a US soldier arrested over trading on the Maduro capture).
- https://www.youtube.com/shorts/pWscXpIcUWI : "Insider Trading at the White House Is an Open Secret", DeFranco News Clips, 20 Apr 2026, 1,258,342 views, 65,802 likes.
- https://www.youtube.com/shorts/D-yfdPLsUyE : Ryan McBeth, 6 Jan 2026, 104,733 views, 4,889 likes.
Why it works: crime, money and a clock. "Send this to a friend who trades" is the trigger.
Outcome version: Outcome markets are sports, crypto and macro, so insider stories are rarer. Use it for (a) real news about prediction markets with what Outcome traders priced, (b) a checkable on-chain pattern on Outcome with neutral wording ("a new account bought $X of YES 20 minutes before the goal").
Automation: Medium (news selection is human; B-roll and cards templated).
Risk: high. Defamation if you imply insider trading, private wallets, and India's Online Gaming Act exposure for ads (03-platform-rules.md section IN). Facts only, source on screen.

### Format 9. "The market says" reaction clip

Look: a short clip of a celebrity, streamer or meme, plus a market screenshot; caption "according to the market there is a 7% chance". Face on camera in the source clip, but the PAGE can be faceless.
Examples:
- https://www.youtube.com/shorts/fHj3hcPGRNI : John Casterline (8.4M subs), 1 Jun 2025, 6,227,577 views, 291,320 likes; description "According to Polymarket, there's only a 7% chance it actually happens" plus the market link. Channel median 1.9M, x3.3.
- https://www.youtube.com/shorts/HXJjHEzpP90 : "Rare Trump W??" ChaosOdds (1.32K subs), 4 Mar 2026, 507,822 views, 3,544 likes, hashtags #polymarket #memes. Channel median 4,650, x109.
- https://www.youtube.com/shorts/-v3TenjMmL0 : ClipHype (728 subs), 11 Mar 2026, 101,061 views, 578 likes, #viralitypoly; description: a streamer finds a market about whether he will shave his head. Channel median 4,100, x24.6.
Why it works: the market turns a personality moment into a number everyone argues with. For tiny channels the ratio comes from borrowed attention.
Outcome version: after a trending sports or crypto moment, screenshot the live Outcome market on the topic (never covering chart or logo) and add one line. Needs a trigger from news, not from Outcome data.
Automation: Hard (clip sourcing and rights). Risk: clip copyright, disclosure if paid.

### Format 10. Clip with a live odds-line banner (clipper format)

Look: a sports or meme clip. A banner sits above the bottom 30% of the frame: a small chart with a % line that jumps green when "your" side scores and red when the other side does. Captions must not cover it.
Rules, from the brief a clipper actually sees (FindClout Kalshi tutorial, read 13 Oct 2026): pay "$130 per million" views; pick a two-option market; start the line at 50/50 or at the score in the first frame; upload the finished clip; tap GREEN when your team scores and RED when the other side does; one tap per moment; generate banner video; keep the banner above the bottom 30%; no caption over the banner; chart moves must match the action; trim the first 1 to 2 s; "Ruining a brand's clip standard restricts your access to all campaigns." Platforms named: TikTok and Reels.
Examples (YouTube Shorts from the #viralitypoly campaign tag, banner not seen by me):
- https://www.youtube.com/shorts/myoepLVEUTs : DoomScroll Rankings (26.8K subs), 12 Feb 2026, 8,478,700 views, 182,434 likes, a TJR clip. The channel's latest 48 Shorts median 13K (this hit is older than that sample, so x652 overstates the contemporary ratio).
- https://www.youtube.com/shorts/idoxBEs-Uvo : Polymarketupdates (15.3K subs), 19 Feb 2026, 8,330,217 views, 156,751 likes; median 30K, x277.7. The channel name contains "polymarket", which the NACA complaint says clippers were told not to do (allegation, see 03-platform-rules.md).
- https://www.youtube.com/shorts/-v3TenjMmL0 : ClipHype, 101K views (format 9).
Campaign terms seen: Content Rewards "PolyMarket Clipping (TJR, Logan Paul, etc.)" by Virality: $3.00 per 1K views, minimum payout $0.99, caps $300 TikTok / $450 YouTube / $450 X; budget $5,375, $0 left, status Paused; platforms TikTok, YouTube, X; "Post Sports content with the polymarket banner"; "GOOD quality"; Tier 1 / US views; hashtag #viralitypoly; banner required; 136.9M views approved; top clippers listed at $1.7k, $1.1k, $900. The page headline says "$10 per 100k views", which conflicts with $3.00 per 1K (about $300 per 100k): confirm before relying on either.
Why it works: borrowed attention (a clip that already travels) plus a moving line that rewards watching to the end. The line is "sticky" because it reacts to what is on screen.
Outcome version (the honest one): use the REAL price history of the Outcome market during the match window, so the line really moved with the market. Do not simulate. Football clips need rights: only use footage you are licensed to use.
Automation: Hard: footage, time sync of price series to the clip, banner render (HTML or After Effects), disclosure caption.
Risk: HIGH. FindClout's own tool lets the line be simulated, which is the deceptive part. Disclosure: Garbage Day (29 Jun 2026) found very few posts marked as ads; paid clips must carry "Ad" plus the platform label. IG's originality rule (30 Apr 2026) hides reposts from Discover.

### Format 11. Sports moment clip + caps caption (Polymarket Sports recipe)

Look: a highlight clip, one shouting line with 1 to 3 siren emojis and 4 to 5 hashtags (team, league, event). No odds on screen.
Evidence (Socialpruf, 12 months to 13 Oct 2026; posts did not open on TikTok, UNVERIFIED direct): Polymarket Sports TikTok: 753,900 followers (read from TikTok embed header), 27.4M hearts, 370 videos, average 139K views and 14.9K likes, engagement 10.8%. Top by views: "Looks like the league I fell in love with" 4.20M views / 345K likes (about 10 Jan 2026 by ID); "WHAT IS GOING ON IN TORONTO" 1.56M / 158K likes; "GAME OF THE YEAR" 981K / 127K likes. None of the top 20 captions mention odds.
Verified comparable: https://www.tiktok.com/@wolusfcb/video/7693643427333836064 : the Adidas profile-picture clip, 6 Oct 2026, 1.8M views, x17.3 vs the account's median 104.2K.
Why it works: it is football-page content; the brand rides the audience and puts its edge in the bio ("Most accurate sports odds in the world").
Outcome version: not recommended for a new page without footage rights. If used, only with licensed highlight feeds and an end card of the live Outcome price.
Automation: Hard. Risk: footage copyright; IG repost suppression.

### Format 12. How-it-works explainer / how-to

Look: either a 5-slide carousel of Outcome screenshots with TikTok text boxes, arrows and circles, or a 40 to 60 s screen-record.
Examples:
- https://www.youtube.com/shorts/18p0tugu0LE : "What is Polymarket?" 60 Minutes, 2 Dec 2025, 401,276 views, 2,719 likes.
- https://www.youtube.com/shorts/ULfJ5nfld9g : Good Work (1.7M subs), 18 Dec 2025, 258,356 views, 15,284 likes, "proving Kalshi and Polymarket aren't gambling" (face on camera).
- https://www.tiktok.com/@theeconomist/video/7669786166081670422 : 3 Aug 2026, 86,600 views, 4,246 likes, 443 saves, 177 s, 1.7M followers; asks who decides when an outcome is unclear.
- Demand pages on TikTok Discover (not posts): how to interpret Polymarket odds; how to see who the top traders buy on Kalshi; Polymarket Bitcoin 5-minute strategy; is Kalshi legit; does Kalshi make you pay taxes; Polymarket Openclaw (AI agents).
Why: standing search intent, saves.
Outcome version: "How a YES share works: price is the chance, a correct share pays $1" using one live market and the UI payout line ($100 -> $375). Replace the brief's title "How to turn your predictions into profit" (promise) with "How a YES share pays $1".
Automation: Medium (screenshots refreshed from a headless browser; text boxes templated).
Risk: medium. Profit wording. Zero fees claim (see 01 file).

### Format 13. Challenge diary ("Day N")

Look: a serial post with a day counter.
Examples:
- https://www.youtube.com/shorts/bw1_1vde2B4 : "Day 2 of turning $100 into $100k on Kalshi", Walter Blake Knoblock (115K subs), 23 Sep 2025, 93,373 views, 1,133 likes. Channel median 12K (n=23), x7.8.
- Safe variant (from 02-reference-posts.md): https://www.instagram.com/reel/Ddhe4nRyHcz/ rynssport, 20 Sep 2026, 9,524 likes on 284 followers, "Day 1 of predicting sports with zero knowledge" (no money).
- TikTok claims of "$10 to $500 live" and "$5 to $10,000 challenge" came up in search: UNVERIFIED.
Why: serial curiosity, "part 2" comments.
Outcome version: "Day N of predicting the UCL with the market as my guide" with no stake; or "Outcome week in numbers".
Risk: HIGH with money (profit-promise and "make money online" signals); low without.

### Format 14. AI agent or bot experiment

Examples: https://www.youtube.com/shorts/shZwbIRtObE : Ray Fu, 2 May 2026, 292,775 views, 13,109 likes. A TikTok claim that two AI agents turned $1,000 into about $14,200 came up in search (UNVERIFIED).
Why: novelty plus a scoreboard.
Outcome version: an AI reads Outcome prices and publishes predictions with a public scoreboard (right or wrong), no money results. Outcome has an SDK (github.com/Outcome-xyz/hip4).
Risk: results claims are a fake-win vector.

### Format 15. Wallet / KOL PnL tracker and copy-trading talk

Examples:
- https://www.tiktok.com/@solana_trading/video/7640115477313801494 : 15 May 2026, 5,103 views, account 7,355 followers, median of 4 posts 759, x6.7 ("The best Solana wallet PnL tracker"). Its 4 Oct 2026 post "Combined KOL PnL: +$150.8K ... link in bio" got 1,044 views (x1.4).
- https://www.youtube.com/shorts/4fTh5ZQ3J00 : "The truth about copy trading", Tanja Trades (146K subs), 23 Sep 2025, 295,647 views, 2,443 likes, x22.7.
Why: curiosity about what winners hold; the truth-telling angle ("the truth about ...") travels more than a tracker ad.
Outcome version: "What the top Outcome wallets hold" from /api/positions. Never "copy them".
Risk: copy-trading is a financial promotion; keep to information.

### Format 16. Sponsored game-sim predictions (#PolymarketPartner)

Examples (all disclosed by hashtag):
- https://www.youtube.com/shorts/qKOjSK-sgq0 : ASP FC (901K subs), 8 Jul 2026, 5,504,687 views, 115,132 likes, x4.1 vs median 1.35M.
- https://www.youtube.com/shorts/ggI7pU49AJg : Xaid (333K subs), 28 Jun 2026, 5,874,243 views, x1.7 (his normal level is high).
- https://www.youtube.com/shorts/8mDeNYn6iJE : Thogden (2.7M subs), 2 Jul 2026, 3,395,936 views, x12.5.
- https://www.youtube.com/shorts/CQnMeZAY0TY : Barca Legion (931K subs), 15 Jul 2026, 626,065 views, x5.4.
Pattern: football game footage, a fast voice, "I predicted the rest of the World Cup" hooks.
Outcome version: UCL or EPL prediction series on game footage. Hard (production), disclosed sponsorship needed.

### Format 17. Live market resolution moment

Evidence: https://www.tiktok.com/@polymarket/video/7629758650223037710 is a @loganpaul video (author 19.0M followers) co-listed on Polymarket's profile: 17 Apr 2026, 1,500,000 views, 73,200 likes, 3,396 saves, 35 s, "Last 5 seconds got me queasy". A face video. No faceless version found (UNVERIFIED supply). Demand: TikTok Discover page "Poly Market Bitcoin 5 Minute Market Strategy".
Outcome version: the BTC 15m tab is an Outcome asset. Result cards per window or a screen recording of the last 60 s, with the chart left uncovered.
Risk: high-speed gambling feel; keep to results, not instructions.

### Format 18. Trader comedy skits (reference only)

- https://www.youtube.com/shorts/7g2UtVScDLc : Yeti dyor (1.17M subs), 29 Oct 2025, 52,499,100 views, 767,661 likes; title plugs polymarket.com in a Halloween trader sketch. Channel median 5.9M, x8.9.
- https://www.youtube.com/shorts/trVmDXMaj-M : Pino (139K subs), 8 May 2025, 106,112,949 views, 685,155 likes, "Non-profitable Trader" (no prediction market; sets the ceiling for trader humour).
Not buildable faceless; use as sponsorship targets.

---

## 4. Guardrails that apply to every format

- Fake-win line: the Polymarket scandal was creators filming fake wins on dummy copies of the site (WSJ via The Block, 21 Jun 2026; NACA complaint 26 Jun 2026; see 03-platform-rules.md). Every number we post must be a real, settled or open, on-chain Outcome trade or price, with the date. No mock-ups.
- Profit line: never "make $", "turn $X into $Y", "easy". Use "one resolved trade" and "not financial advice".
- Words: never say bet or betting; use trade, predict, market, YES/NO.
- Client rules: never cover the market chart or logo; CTA "Trade with zero fees on Outcome.xyz" (the fee wording is flagged in 01-what-is-outcome.md: a small close fee exists since about 5 Sep 2026).
- Disclosure: paid or per-view posts need "Ad" plus the platform label.

---

## 5. Official brand accounts: what their top posts are

Account sizes read on 13 Oct 2026.

| Platform | Account | Size | What the top posts are | Source and status |
|---|---|---|---|---|
| TikTok | @polymarket | 171,400 followers, 6.6M likes, verified; Socialpruf: 546 posts in 12 months, avg 68.4K views, avg 3.11K likes | (1) Gopuff sweepstakes promo, author @gopuff, 3 Jul 2026, 5.0M views but 1,947 likes, 20 s (read on TikTok); (2) 6ix9ine / Maduro news clip, 3 Apr 2026, 2.87M views, 289K likes (Socialpruf only); (3) AI book-pulping story, 29 Jul 2026, 2.27M views, 70.4K likes (Socialpruf only); (4) Trump Iran remarks, 6 Apr 2026, 1.54M views, 44.0K likes (Socialpruf only); (5) @loganpaul "Last 5 seconds got me queasy" 17 Apr 2026, 1.5M views, 73.2K likes (read on TikTok) | 3 of 5 do not open (one is flagged "content_classification,status_audit_not_pass"): UNVERIFIED format for those. Pattern: news clips with a one-line caption and creator or brand collabs |
| TikTok | @polymarketsports | 753,900 followers, 27.4M likes, verified; avg 139K views, 14.9K likes, 10.8% engagement | Highlight clips with a caps caption (format 11). Top 4.2M views / 345K likes | 5 of 5 tested posts do not open now: UNVERIFIED direct |
| TikTok | @kalshi | 688,400 followers, 15.9M likes, verified; Socialpruf: 508 posts, avg 11.5K views, 289 likes, 2.61% | Top post 580K views / 60.7K likes (22 Nov 2025 by ID); next 175K, 144K, 141K, 130K | 5 of 5 do not open now: UNVERIFIED format. Kalshi's own page is weak on TikTok; its reach is paid creators |
| TikTok | @kalshisports | not found by that handle | | UNVERIFIED |
| YouTube | Kalshi (@kalshi_markets) | 10.5K subs | Ad "Predictions | Kalshi x Jose Mourinho", 31 s, 5 Jun 2026, 19,782,698 views, 172 likes (ad-style numbers) | Read on YouTube |
| YouTube | Polymarket-Official (@Polymarket-Official) | 589 subs | 48 Shorts of news headlines, median 17 views, top 1,000 | Official status UNVERIFIED |
| Instagram | @polymarket, @polymarketsports (468K per a search snippet), @polymarketfc, @polymarketbaseball, @kalshi, @kalshisports | | No post numbers visible logged out | UNVERIFIED |
| X | @Polymarket | followers UNVERIFIED | "BREAKING + odds move + 2 charts": 14,865 / 9,550 / 3,333 likes (format 1) | Read |
| X | @PolymarketSport | UNVERIFIED | Real-user payout story 10,167 likes; Golden Boot ranking 5,262 likes | Read |
| X | @Kalshi, @KalshiSports, @KalshiPolitics, @KalshiFC | UNVERIFIED | Daily table 3,183 likes; Ballon d'Or chances 4,503 likes; Fed chair 790 likes | Read |

What the official pages do not do: they rarely post P&L cards. Their biggest reach is either breaking-odds posts on X, real-user payout stories on X, sports clips on TikTok, or paid and partner creators.

---

## 6. Clipping and creator campaigns

What exists:
- Kalshi through FindClout (app.findclout.com/kalshi/tutorial; Garbage Day, 29 Jun 2026): odds-line banner on sports and meme clips (format 10); $130 per million views; payouts through PayPal, screenshots up to about $2,000; Discord about 5,000 members; meme pages aimed at US and UK Gen Z; an HN comment (UNVERIFIED) claims about 50 Instagram pages doing 40 to 50 million views a day; very few posts marked as ads; "Kalshi x Messi" World Cup edits approved through Frame.io.
- Polymarket through Virality: Content Rewards campaign at $3.00 per 1K views (paused, $5,375 budget used, 136.9M views approved); Whop product "Polymarket Official Clipping" (9.2K members, 4.8 rating on 156 ratings, free to join, a reviewer says it refills slowly); NPR (12 May 2026) says Polymarket offered 50 cents per 1,000 views from a $70,000 budget (archived page 19 Mar 2026); NACA alleges $1 per 1,000 (allegation). Agency LuvKaizen (self-reported) says a Polymarket clipping run gave 185M impressions in 3 months (38M, 66M, 81M), split TikTok 42%, Reels 35%, Shorts 23%, top video 3.2M views. Hashtags in use: #viralitypoly (clippers), #PolymarketPartner (disclosed creators).
- Formats clippers were asked for: (1) banner on a sports or meme clip; (2) streamer or podcaster clips that mention a market (Tyler1 haircut market; PBD Podcast "The Prediction Market Knew Before Anyone Else", 1,383,211 views, 15 Oct 2025); (3) a product "naturally featured" in a meme (a non-market example from the Garbage Day piece); (4) brand football edits.
- HIP-4 venues (Outcome and others): I found no clipping or creator campaign for Outcome or any HIP-4 venue on Whop, Content Rewards or Vyro. Outcome's own X account (x.com/Outcomexyz) advertises trade-to-earn rewards ($1,000,000 pool, per search snippets, not opened) and posts resolved-market winners. UNVERIFIED that none exists in private channels.

What it means for Outcome: the clipper brief is a strong idea (a moving line on a clip), but the safe version is real price history, licensed footage and an "Ad" label.

---

## 7. Not found / gaps

- Instagram post-level numbers for official accounts and for clipping pages: not available logged out.
- Top posts of @polymarket, @polymarketsports, @kalshi on TikTok: only 2 of 15 tested posts open; the rest are Socialpruf-only.
- X follower counts and views: not available, so X outlier scores are within-account only.
- A faceless proof of formats 6 (top traders), 14 and 17: none verified.
- A clipping or creator campaign for any HIP-4 venue: none found.
- tikwm.com is now behind a Cloudflare challenge; if it comes back, `user/posts` would replace the embed and Socialpruf routes.

Routes that worked (for the automation phase): r.jina.ai with header `X-Return-Format: html` on a TikTok video URL (parse the `__UNIVERSAL_DATA_FOR_REHYDRATION__` JSON); the same on `tiktok.com/embed/@handle` (latest posts with views for non-verified accounts); YouTube search and `/channel/<id>/shorts` pages (parse `ytInitialData`); X `cdn.syndication.twimg.com/tweet-result?id=<id>&token=a` for likes; Socialpruf pages for top TikTok lists; the WebSearch tool with `allowed_domains` set to tiktok.com, x.com or instagram.com to find posts.

---

## 8. Sources with dates (all read 13 Oct 2026 unless stated)

TikTok page data (r.jina.ai raw HTML route)
- https://www.tiktok.com/@jackpot_0_/video/7676843272941325590 (posted 22 Aug 2026); creator embed https://www.tiktok.com/embed/@jackpot_0_
- https://www.tiktok.com/@60minutes/video/7641011689969732878 (17 May 2026)
- https://www.tiktok.com/@theeconomist/video/7669786166081670422 (3 Aug 2026)
- https://www.tiktok.com/@wolusfcb/video/7654311092851690774 (22 Jun 2026); .../7693643427333836064 (6 Oct 2026); embed https://www.tiktok.com/embed/@wolusfcb
- https://www.tiktok.com/@zone2.foot/video/7640285221828562208 (16 May 2026); embed https://www.tiktok.com/embed/@zone2.foot
- https://www.tiktok.com/@ballondor/video/7663815219788991777 (18 Jul 2026)
- https://www.tiktok.com/@polymarket/video/7658304791289793823 (Gopuff, 3 Jul 2026) and .../7629758650223037710 (@loganpaul, 17 Apr 2026)
- https://www.tiktok.com/@solana_trading/video/7640115477313801494 (15 May 2026); embed https://www.tiktok.com/embed/@solana_trading
- https://www.tiktok.com/@cryptodailyfeed/photo/7675106142749494559 (17 Aug 2026 by ID; status "author_status,status_audit_not_pass")
- Account headers: tiktok.com/embed/@polymarket, @kalshi, @polymarketsports
- Third-party stats: https://socialpruf.com/tiktok/polymarket ; /tiktok/kalshi ; /tiktok/polymarketsports (12 months to 13 Oct 2026)

YouTube (public search and channel pages)
- Shorts links as listed in section 3; channel stats read from https://www.youtube.com/channel/<id>/shorts for UCoMR9UyiAW2iM2jMZnbfwoQ (ASP FC), UCao1WxRGF3lO7nyussvnAFA (Xaid), UCnU7ly6zEcQxUScjhkgFYAQ (Thogden), UCqSJc3nMNcA90MwnzgA2mFA (Barca Legion), UCxF_EoVuEjuiI2TAZja2gMg (DoomScroll Rankings), UCdJQDITquSrPURfW4V0sg7Q (Polymarketupdates), UCBFAxFWvsyy6S4b8ETjisqQ (ClipHype), UCFFfvfUAYuAzUUea0ohojFg (ChaosOdds), UCSJiVuYRNA_x8wzNvxdlEtw (football fans), UCJWBQxmH3Qw7ftKGlyOnj7w (BALLIX FOOTBALL), UCm0v-J78Qc4ijc9Mg8tAWqg (MadridZone), UCcNF8uo5xFNPf4vGg3W3NaA (Tanja Trades), UCdaEipK588TVhtz2ddQsCHA (Yeti dyor), UCuFdxAB-aXZRtRv8cA_hN9Q (Pino), UCdYBb83d2h5tlb1y7Tz87hg (Three Markets), UCuECK5m8bmB9UczJDQkHsaQ (Gorilla Predictions), UCq4zBbHxchTQHOokRQwuvKg (predictionist), UCD7G81DXCDVmCajU6Oi8x7g (Walter Blake Knoblock), UCE7spuKzxP1k8A-XucxxUAQ (John Casterline), UC_-hYjoNe4PJNFa9iZ4lraA (Good Work), UCUMPemO46nJTp-0iX9JXedQ (Kalshi), UCwNiPybAvLXUKYko-MGZOdQ (Polymarket-Official)

X (public tweet-data endpoint, likes and replies)
- Tweet IDs read: Polymarket 2101683638064607551, 2102072830858817830, 2023899611224482162, 1991196710865957228, 2074186977105109064, 2089757802512179692; PolymarketSport 2108223688755786041, 2067640740931322188; PolymarketMoney 2066602393320427955; Kalshi 2017259629797933301, 1914682606886506659; KalshiSports 2087543566117503392; KalshiPolitics 2109635033979847156; KalshiFC 2096958875392004112; lookonchain 2007639475497881625; marlowxbt 2015814991484461335; whalewatchpoly 1974992908567605547, 1976412924181643775, 1964982237549457906, 1973759018058256531, 1940182762847162684; GrindeOptions 2109666607928848824; BusinessInsider 2047375503686828309

Clipping and campaigns
- https://app.findclout.com/kalshi/tutorial (undated tutorial page)
- https://www.garbageday.email/p/we-spent-a-month-hiding-in-a-kalshi-clipping-discord (29 Jun 2026; read through a page-summary tool)
- https://contentrewards.com/discover/56213dc4-a110-42d4-bb5e-7832e654d980 (campaign page, live)
- https://whop.com/joined/polymarket-official-clipping/products/polymarket-5c/ (live listing)
- NPR via KJZZ, 12 May 2026: https://www.kjzz.org/npr-top-stories/2026-05-12/the-clipping-economy-how-short-form-video-clippers-are-overrunning-the-internet
- https://www.luvkaizen.com/case-studies/polymarket-clipping (vendor, self-reported)
- https://www.tubefilter.com/?p=190947 (16 Feb 2026; Polymarket-sponsored YouTube video "bonus" entry, 64,939 views)
- Not opened (403): https://sbcnews.co.uk/marketing/2026/06/30/kalshi-x-marketing/ (search snippet says Kalshi slip-style graphics appear on @FCReplays videos on X; UNVERIFIED)

Context files in this folder: 00-client-brief.md, 01-what-is-outcome.md, 02-reference-posts.md, 03-platform-rules.md.
