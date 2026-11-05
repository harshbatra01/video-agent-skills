# Outcome data triggers: what a daily script can pull, and 15 story detectors

Prepared 13 Oct 2026. All tests were run live between 00:10 and 01:20 UTC, one request at a time, 1 to 2 seconds apart. No logins, no keys, nothing downloaded except small JSON (PNG cards were measured in memory only, nothing saved).

Raw samples: `C:\VISION\VISION CLAUDE\outcome\research\raw\data-scout\` (52 trimmed JSON files named A01 to F01, no images). Each file holds the exact request and a trimmed response. `F01_detector_samples_today.json` holds the sample output of all 15 detectors.

Companion files: `00-client-brief.md`, `01-what-is-outcome.md` (section 10 lists the endpoints this file tests).

---

## 1. The 15 detectors

### 1.1 Summary table

Reliability: High = official data, rule is simple. Medium = works but needs a cross-check or an archive. Low = rare, partial or easy to get wrong.

| # | Detector | One-line rule | Main source | Reliability | Fired today (13 Oct)? |
|---|---|---|---|---|---|
| 1 | Top traders by P&L | Rank by realised P&L, 24h / 7d / 30d / all, plus best P&L as a % of volume traded (volume over $1,000) | Outcome leaderboard API | High | Yes: trader-W +$21.7k |
| 2 | Best single positions | Biggest profit on one market by one trader, 24h or longer | Hyperliquid fills + Outcome market names | Medium | Yes: +$4.0k best |
| 3 | Whale orders | Single fill of $1,500 or more (today's scale), largest trade ever in a market | stats site hourly maximum, market stats, wallet fills | Low to medium | Weak: top fill $4.8k |
| 4 | Top traders' open positions | 3 or more of the top 20 on the same side of one market, or one open position of $5,000+ | Outcome profile lookup + Hyperliquid wallet balances | Medium to high | Yes: 4 of 20 hold the Rams |
| 5 | Biggest swings in 24h | Chance moved 8+ points (event markets 5+) with 15+ traders | Hyperliquid candles + allMids | Medium to high | Yes: Rams v Bills -11 pts |
| 6 | Upsets and blown leads | Loser's average price 60%+ or peak 85%+, volume over $20k, confirmed by score timeline | Outcome settled stats + ESPN | Medium | Yes: 3 NFL, 4 football |
| 7 | Longshots that came in | Winner priced under 15% beforehand | Same as 6, better with our archive | Low (rare) | Weak: 1 draw |
| 8 | Score shock | A goal, score or red card moves the match market 8+ points in 3 minutes | Outcome/ESPN live score + Hyperliquid 1m candles | Medium | Yes: Rams v Bills live |
| 9 | Markets starting or closing today | Matches kicking off and price markets expiring within 24h | outcomeMeta + allMids | High | Yes: 9 UCL games |
| 10 | New markets | Questions listed since yesterday (ids only go up) | outcomeMeta + incentives list | High | Yes: Europa League, NBA |
| 11 | Crowd vs bookmaker | Outcome price differs from sportsbook odds by 5+ points | allMids + ESPN odds | High data, low hit rate | No: max gap 2.6 pts |
| 12 | Trader consistency and streaks | In the top 100 of all three windows, green-day streaks, best and worst day | Leaderboard + portfolio lookup | Medium to high | Yes: 33 traders |
| 13 | BTC 15-minute scoreboard and late flips | Up/down count, streaks, markets that reversed late | markets/series + market stats | High data, tiny stakes | Yes: 2 swings, 3 miscalls |
| 14 | Fed, IPO and macro odds with a headline | Odds for the Fed decision and Anthropic IPO ladder, move of 3+ points, matching headline | Market question lookup + RSS | High (odds) | Yes: Fed hike 15.7 to 17.9% |
| 15 | Platform records | Record volume day, users, busiest hour, rewards paid | stats site + rewards service | High numbers, careful meaning | Yes: record days 10 to 12 Oct |

### 1.2 Five things to know before using the table

1. Everything the 15 detectors need can be pulled today with plain HTTP, no key. The best sources are NOT the fan site. Outcome's own API (`o1.outcome.xyz`) and Hyperliquid's public info API are open, richer and fresher. The fan site (`dev.jbfx.me`) is a thin wrapper on those two, with bugs, so use it only as a shortcut or a design reference.
2. Three hard limits shape the whole pipeline:
   - **Price history of a market vanishes the moment it settles.** Hyperliquid returns HTTP 500 and `null` for candles and trades of a settled coin, even 20 minutes after expiry. Outcome's own market page for a settled game says "Graph coming soon. Charts for settled markets are a feature we're building." So the pipeline must save prices while markets are live. Start this archive job first, because yesterday's history cannot be rebuilt.
   - **There is no global trade feed.** `recentTrades` gives only the last 10 trades of one coin. Big orders must be found per wallet, per hour (stats site), per market (largest trade stat), or live over a WebSocket.
   - **Many markets only carry raw template names** (`template:sportsContestResult`, "Unknown market"). We must build the titles ourselves. The rules are in section 3 and work for every market type seen today.
3. Scale check for "whale" and "big win" wording. On 12 Oct the biggest single fill through Outcome in any hour was $4,800. The best single position of the day was about $4,000. The top trader of the day made +$16.9k (00:35 UTC) to +$21.7k (01:05 UTC). The $503k trader-J case from the World Cup in July is an extreme outlier.
4. Volume numbers are shaky. The same market can show 24h volume above its lifetime volume, and a handful of market-maker accounts dominate. One account (trader-U) traded $3.2M in 24 hours. Quote volume only if it matches what the Outcome page shows (Yes plus No lifetime notional) and never as proof of popularity.
5. Run the collector from a home or office IP. The fan site's own code says Outcome's Cloudflare blocks AWS serverless addresses and relays through the visitor's browser instead. My home connection worked for every Outcome call. Not tested from a cloud server.

### 1.3 Detector cards

All "sample today" values were fetched 13 Oct 2026, 00:10 to 01:20 UTC. Live boards move, so expect small differences between samples. Times are UTC.

#### D1. Top traders by P&L (24h, 7d, 30d, all time)
- **Finds:** the traders with the most realised profit in a window. Variants: best `pnl_pct` with volume over $1,000; traders who are in the top 100 of all three windows. Internal only: the same call with `"order_by":"asc"` lists the biggest 24h losers (today trader-L -$10,581 on $5,844 volume, trader-C -$9,992 on zero 24h volume, trader-E -$4,181). Never post losses: no shaming, no "lost it all" hooks. Feeds the Top 3 traders carousel and the trader story.
- **Endpoint:** `POST https://o1.outcome.xyz/api/v1/leaderboard` with body `{"duration":"24h","filter_by":"pnl","order_by":"desc","offset":0,"limit":10}`. Fields per row: `position`, `username` (null means anonymous), `pnl`, `pnl_pct`, `volume`, `x_verified`, `hof.equipped_badges`, `avatar`, `banner`. Response also has `total` and `last_updated_at`. `duration` must be `24h`, `168h`, `720h` or `all`. Fan twin: `GET https://dev.jbfx.me/api/leaderboard?duration=24h&limit=50`.
- **Sample today (01:05):** #1 trader-W +$21,673 (+26.9%) on $80,436 volume. #2 trader-P +$4,322 (+80.8%) on $5,351. #3 trader-B +$3,229 on $150,715. #4 trader-Y +$1,762 (+56.9%) on $3,098. #5 trader-F +$1,530. Best `pnl_pct` with volume over $1,000: trader-P, trader-Y, then trader-A (+35.4%). About 450 traders are ranked in the 24h window. 7d leader trader-W +$10,492. 30d leader trader-27 +$19,608. All-time leader trader-J +$503,008.
- **Reliability: High.** Official data. Freshness of `last_updated_at`: 24h under 1 minute, all-time about 10 minutes, 7d about 30 minutes, 30d about 1 hour. Caveats: only realised P&L counts. `pnl_pct` is profit divided by the volume the trader traded in the window (checked: 4,322 / 5,351 = 80.8%), not the return on a stake. Top dollar spots go to heavy-volume accounts (trader-W traded $2.8M in 30 days), so use `pnl_pct` with a volume floor for relatable stories. Anonymous rows have no name and must not be unmasked. Naming a real user needs the client's written OK (open question in 01 section 10.4).

#### D2. Best single positions
- **Finds:** the biggest realised profit on one market by one trader, with stake, payout and % return. This is the "P&L card" candidate. Feeds the P&L card edit and the trader story.
- **Endpoint (own build, recommended):** (1) leaderboard top 20 as in D1. (2) `POST https://o1.outcome.xyz/api/v1/profile/lookup` with `{"username":"trader-W"}` gives the wallet `address`. (3) `POST https://api.hyperliquid.xyz/info` with `{"type":"userFillsByTime","user":"0x<wallet>","startTime":<ms>,"endTime":<ms>}`. (4) Group fills by `coin`. Net profit = sum of `closedPnl` minus sum of `fee`. Stake = sum of `px * sz` over `Buy` fills (buys can be older than the window, so query back to the first buy for the full stake). (5) Name the market with `POST /api/v1/markets/lookup` (section 3). **Shortcut:** `GET https://dev.jbfx.me/api/top-trades?window=24h&limit=25&scan=20` (slow, about 5 seconds, scans only the top 20 traders).
- **Sample today:** trader-P +$4,016 (+51%) on Como v AS Roma, side NO on Como, stake $7,805, payout $11,821, settled 12 Oct 05:44. trader-W +$3,712 (+112%) on Atlanta Falcons v Baltimore Ravens, Ravens side, stake $3,307, settled 04:48. trader-W +$3,305 on Colts v Steelers (Steelers side, $8,090 payout). My own fill-based totals agree with the fan list within $16 (fees).
- **Reliability: Medium.** Traps: (a) the fan Top trades list reads only the latest 2,000 fills of busy accounts, so early buys are missing. trader-W's coin `#87691` shows 555 shares bought against 4,435 settled, an exit price of 7.99 and +616%. The profit is right (about +$1,933), the stake and the % are wrong. Recompute the stake from every buy by paging `userFillsByTime` back to the first buy. (b) Fills with `dir` = `Merge Outcome` (an account that splits and merges pairs) make per-coin P&L meaningless: trader-N on Spain shows +7,319% ($1,049 stake, +$76,757 profit), which is not real. Drop any position where settled shares differ from bought shares, that has a Merge fill, or whose exit price is above 1. (c) Scanning only the top 20 traders misses big wins by others. (d) Fan titles are often `template:...` or "Unknown market".

#### D3. Whale orders (largest single fills)
- **Finds:** single fills above a size threshold. Suggested threshold today: $1,500 (World Cup days would need $25,000). Also the largest trade ever in a market. Feeds the "Insane trader headline" format and market-of-the-day posts.
- **Endpoints:**
  - Per hour: `GET https://stats.outcome.xyz/api/builder/hourly?builder=0x<wallet>&hours=24`. Field `series.biggestNotionalFill` (one value per hour, settlements appear to be excluded).
  - Per market: `POST https://o1.outcome.xyz/api/v1/markets/lookup` gives `yesStats` and `noStats` with `largestTrade`, `avgTradeNotional`, `medianTradeNotional`, `trades`, `uniqueTraders`.
  - Per wallet: `userFillsByTime` (see D2). A wallet from `recent-fills` or the WebSocket becomes a name with `POST /api/v1/profile/lookup` `{"address":"0x..."}`.
  - Live: `GET https://stats.outcome.xyz/api/builder/recent-fills?builder=<same address>` (latest 100 fills with wallet in `user`, only about 15 seconds of history), or the Hyperliquid WebSocket `trades` stream per coin.
- **Sample today:** biggest fill per hour over 24h: $4,799.50 (19:00 hour), $4,424.00 (13:00), $2,807.36 (18:00). Largest trade ever per market side: $4,813 (NO on Manchester United, EPL winner), $4,646 (NO on Kansas City, NFL winner), $4,343 (NO on PSG, UCL winner). Largest order by a top-20 trader: trader-W bought 2,000 shares of "no draw" in Galatasaray v Barcelona at 87.0 cents, $1,740.
- **Reliability: Low to medium.** The hourly maximum does not say who or which market. I could not find the $4,799 fill among the 20 top P&L traders or the 10 highest-volume traders I scanned. Typical trade is small (median $14 to $36 in the busiest markets).

#### D4. What the top traders hold right now (open positions)
- **Finds:** the open outcome-token positions of the top traders, grouped by market and side. Triggers: 3 or more of the top 20 traders on the same side of one market (a "crowded bet"), or one open position of $5,000 or more. Shows cost, average entry, current price and unrealised P&L. Feeds previews ("the top traders are all on the Rams") and live-position versions of the "Insane trader headline" format.
- **Endpoint:** wallets from `POST https://o1.outcome.xyz/api/v1/profile/lookup` (`{"username":"trader-W"}`), then `POST https://api.hyperliquid.xyz/info` with `{"type":"spotClearinghouseState","user":"0x<wallet>"}`. In `balances[]` keep rows whose `coin` starts with `+` and whose `total` is above 0. Shares = `total`, cost = `entryNtl`, average entry = `entryNtl / total`, current price = `allMids["#" + same digits]`, unrealised = `total x price - entryNtl`. Name the market with section 3.
- **Sample today (top 20 by 24h P&L, 20 wallet calls):** 4 of the 20 hold the Rams to beat the Bills (trader-W, trader-Y, trader-F, leveragewizard): $8,975 cost, average entry 61.5%, now 53.9%, about -$1,109 unrealised. Biggest single open position: salty_bid8217, $10,133 on Arsenal to win the Premier League (entry 57.9%, now 59.9%). trader-R and liquidator both hold No on "HYPE touches 100" ($5,470 cost, about +$3,560). trader-W alone holds 22 open outcome positions, the largest $5,608 on the Rams and $5,449 on Bayern at Viking (entry 89%).
- **Reliability: Medium to high.** Cost basis matches the fan site's open positions (2,000 shares at 0.8702 = $1,740). It is a snapshot, positions change by the minute. Many top traders are market makers who hold several tokens of one market, so check that a "crowded" side is not hedged by the opposite token. The same call shows a wallet's cash (trader-W holds $126k USDC): public, but never show balances or addresses. Naming traders needs the client's OK.

#### D5. Biggest swings in 24h
- **Finds:** markets whose chance moved most in 24 hours. Rule: 8 points or more for event markets with at least 15 unique traders; 5 points for sports, Fed or IPO stories on quiet days. Keep price-linked markets (BTC, oil, touch ladders) in a separate list because they only follow the asset.
- **Endpoint:** (1) list: `GET https://o1.outcome.xyz/api/v1/outcomes/meta` (313 open outcomes). (2) stats: `POST /api/v1/markets/lookup` in batches of 50 (7 calls). (3) history: `POST https://api.hyperliquid.xyz/info` with `{"type":"candleSnapshot","req":{"coin":"#85650","interval":"1h","startTime":<ms>,"endTime":<ms>}}`. Open of the first candle against `{"type":"allMids"}` now. Also `GET https://o1.outcome.xyz/api/v1/top-movers` (only 3 rows, 6 hour window, raw titles).
- **Sample today (45 liquid coins checked):** BTC above $83,988 at 06:00 UTC (daily) 49.5% to 0.2% (-49.3 pts). Rams v Bills (NFL, live) Rams win 61.8% to 50.4% (-11.4). Anthropic first-day market cap above $2,000B 65.7% to 58.3% (-7.4). Fed hike 15.7% to 17.9% (+2.3). Every football futures market moved under 2 points. Outcome's own top-movers list shows only the BTC bucket and two untraded markets at 50%.
- **Reliability: Medium to high** while the market is live. After settlement the history is gone (section 5). Thin markets jump, so keep the 15-trader filter.

#### D6. Upsets and blown leads
- **Finds:** a settled game where the favourite lost, or a side that traded at 85% or more did not win. Target rule: the loser was priced at 70% or more just before the event (needs our own archive, section 7). Proxy rule until then: loser's average price (`vwap`) at least 0.60, or loser's peak (`maxPrice`) at least 0.85, market volume at least $20,000. Then confirm with the score timeline. Feeds news-style hooks and "Rankings".
- **Endpoint:** `GET https://o1.outcome.xyz/api/v1/outcomes/settled?limit=50&name=template:sportsContestWinner` (NFL, two-way), plus `...name=template:sportsContestParticipant2` and `...name=template:sportsContestDraw2` (football three-way). Fields: `settleFraction` (1 means this outcome's Yes side paid), `yesStats` and `noStats` with `vwap`, `minPrice`, `maxPrice`, `lastPrice`, `volumeNotional`, `lastTrade`. Question level: `GET /api/v1/settle/outcome/400?type=question` gives `winningNamedIndex` (0 = home, 1 = draw, 2 = away) and the settle time. Confirm with ESPN (section 4.5): goal minutes in `competitions[0].details`.
- **Sample today:** NFL: Falcons v Ravens ($262k volume), Falcons traded up to 91% and lost 23-30 in overtime. Seahawks v 49ers ($459k), Seattle's average price 60%, peak 76%, 49ers won. Jaguars 19-17 Eagles: the Eagles led 17-16 with 0:08 left, peaked at 98% (average only 25%), then the Jaguars kicked a field goal as time ran out. Cowboys 16-24 Buccaneers (9 Oct, $75k), Dallas averaged 74% and lost. Football: Levante 3-3 Sevilla, Sevilla peaked at 99% (led 2-0 at 54' and 3-2 at 90'+5', Levante equalised 90'+10'). Monaco 2-2 Toulouse (Monaco led 2-0 at 38', peaked 88%). Man Utd 1-1 Tottenham (Mbeumo 73', Spurs red card 78', Solanke equaliser 90'+2', United peaked 92%). Bayern 2-2 Augsburg: Bayern never led, averaged 81%, peaked at 90% and only drew.
- **Reliability: Medium.** The peak can be one stray print. Liverpool 0-3 Man City shows a 0.99 peak for Liverpool, who never led. Always check the goal timeline. The "favourite" label is a proxy until we keep our own pre-kickoff price (section 7).

#### D7. Longshots that came in
- **Finds:** a winner priced under 15% (or 20%) before the event. Clean rule needs our own archived price at T minus 60 minutes. Without it, use the winner's `vwap` from D6's data as an upper bound.
- **Endpoint:** same as D6.
- **Sample today:** one hit in the latest batch (20 football matches and 22 NFL games with volume over $20k, 10 to 12 Oct): Augsburg 2-2 Bayern, where the Draw traded at 10% on average. The next lowest winners were draws at 23% and 24%. The lowest team win was Tampa Bay over Dallas (NFL, 9 Oct) at 26%.
- **Reliability: Low.** Rare, and today's only hit is a draw. Do NOT use the fan "all-time" top-trades list for longshot stories: its biggest percentage trades are the artifacts described in D2.

#### D8. Score shock (a goal, touchdown or red card moves the market)
- **Finds:** a score or card event followed by a move of 8 points or more within 3 minutes. Feeds match-reaction videos.
- **Endpoint:** score: `GET https://o1.outcome.xyz/api/v2/sports/american_football/matches/zp5rzobooy8vm82/live` (provider id comes from `markets/lookup` `metadata.providerId`; sports list in section 4.1; cache 5 seconds when live). Or ESPN: `GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401872994` (scoring plays with a `wallclock` time). Price: `{"type":"candleSnapshot","req":{"coin":"#85650","interval":"1m",...}}`, only while the market is live.
- **Sample today:** Rams v Bills (NFL), kickoff 00:15. Rams win price about 61% before kickoff, 46.3% at 00:41 with the Bills ahead 6-0 (field goals at 13:23 and 0:10 left in the first quarter). Biggest one-minute moves: 00:16 (-3.6 pts), 00:18 (+2.7), 00:37 (+2.6). The market moved on the drives more than on the kick timestamp.
- **Reliability: Medium.** Works end to end for NFL. For football I verified goal minutes only for finished matches (ESPN and TheSportsDB), and no football match was live during testing, so the in-play incident format and goal-to-price alignment are untested. ESPN wall-clock times can be a minute or two off. A recorder must run through the match, because candles vanish at settlement.

#### D9. Markets starting or closing today
- **Finds:** matches kicking off and price markets expiring in the next 24 hours, with the % chance and the "$100 pays $X" line (100 divided by the price as a fraction, so 80.3 cents pays about $124 per $100 if it wins). Feeds "today on Outcome" carousels and previews.
- **Endpoint:** `POST https://api.hyperliquid.xyz/info` `{"type":"outcomeMeta"}` (same data as `GET https://o1.outcome.xyz/api/v1/outcomes/meta`). Question `description` has `scheduledStart:YYYYMMDD-HHMM`, price outcomes have `time:` or `expiry:`. Chance: `{"type":"allMids"}`, coin `"#" + 10 * outcomeId` for the Yes side. Clean names for 76 featured markets: `GET https://outcome.xyz/api/incentives/current`.
- **Sample today:** 9 Champions League games on 13 Oct. 16:45: Lens v Sporting 37.9 / 25.4 / 36.7 (home / draw / away), Sabah v Slavia 27.4 / 25.2 / 47.4. 19:00: Arsenal v Lille 80.3 / 13.6 / 6.3, Galatasaray v Barcelona 10.2 / 12.9 / 76.7, Viking v Bayern 4.1 / 6.7 / 89.3, Inter v Brugge 77.6 / 14.4 / 7.7, Atletico v Man Utd 51.0 / 24.1 / 25.1, Villarreal v Napoli, Leipzig v PSV. Another 9 Champions League and 8 Europa League games follow on 14 and 15 Oct. 35 markets end within 24 hours (27 price thresholds on S&P 500, US100 (XYZ100), gold, silver, oil, BTC, HYPE and stocks, 4 recurring, 4 NFL).
- **Reliability: High.** Kickoffs match ESPN and TheSportsDB.

#### D10. New markets
- **Finds:** questions listed since yesterday. Rule: question ids only go up, so save yesterday's highest id (433 today) and list questions above it. Ignore the recurring 15-minute series.
- **Endpoint:** same `outcomeMeta`. Listing time for the 76 featured markets: `GET https://outcome.xyz/api/incentives/current`, field `scoring_params.listing_at`. Also `GET https://o1.outcome.xyz/api/v1/outcomes/registered?limit=50` (newest first).
- **Sample today:** listed on 12 Oct: Europa League matchday 2 (Q425 to Q433, 09:08 to 11:02), 2026/27 NBA winner (Q430, 09:30), daily thresholds on S&P 500, US100 (XYZ100), MU, SPCX (20:00) and oil, gold, silver (21:00).
- **Reliability: High.**

#### D11. Crowd vs bookmaker gap
- **Finds:** Outcome's price against sportsbook odds ("pundit" here means a bookmaker, since no free pundit-picks feed exists). Rule: gap of 5 points or more. For the Fed, compare with Polymarket.
- **Endpoint:** Outcome `allMids`, against `GET https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard?dates=20261013`, field `events[].competitions[0].odds[0].moneyline.{home,away,draw}.close.odds` (DraftKings, American odds). Convert to probability, divide by the sum to remove the bookmaker margin (about 5%). Fed: `GET https://gamma-api.polymarket.com/public-search?q=fed%20decision%20october&limit_per_type=3`.
- **Sample today:** 18 Champions League games compared. Outcome sat within 0.3 to 2.6 points of DraftKings (mean largest gap 1.4). Largest: Slovan v Stuttgart (Stuttgart 76.2 against 73.6), LASK v Liverpool, Galatasaray v Barcelona. Fed October: Outcome 81.0 no change / 17.9 hike / 0.4 cut against Polymarket 80.5 / 18.5 / 0.5.
- **Reliability: High data, low hit rate.** Liquid games track the bookmakers, so look at futures and thin markets for real disagreement.

#### D12. Trader consistency and streaks
- **Finds:** traders in the top 100 of the 24h, 7d and 30d lists at once, green-day streaks, best and worst day. Feeds the trader story.
- **Endpoint:** three leaderboard calls (limit 100), then `POST https://o1.outcome.xyz/api/v1/portfolio/lookup` with `{"username":"trader-I","window":"30d"}`. `pnlHistory` is `[epoch ms, cumulative realised P&L]`, daily for 30d, hourly for 1d, about 6-hourly for 7d. Day change = difference between points.
- **Sample today:** 33 traders are in the top 100 of all three windows. trader-I: 17 green days out of 29, a 5-day green streak, best day +$1,168, worst day -$239, 30-day +$4,728. trader-K: +$6,960 in 30 days, best day +$3,590, worst day -$4,510. trader-Y: +$8,817 in 30 days but only 6 green days (a few big wins).
- **Reliability: Medium to high.** The last `pnlHistory` point is today's 00:00 UTC value, so today's gain is not in the streak, and a flat day is not green.

#### D13. BTC 15-minute scoreboard and late flips
- **Finds:** results of the last 50 BTC (also ETH, HYPE) 15-minute markets: up/down count, streaks, and markets that reversed late (peak 90%+ then below 10%, or the last print on the wrong side).
- **Endpoint:** `GET https://o1.outcome.xyz/api/v1/markets/series?category=out-btc-15m&past=50` gives `current` and `past[]` (`outcomeId`, `expiry`, `result` yes or no). Then `POST /api/v1/markets/lookup` for `minPrice`, `maxPrice`, `lastPrice`, `volumeNotional`. The settlement reference is the Hyperliquid BTC perp: `{"type":"candleSnapshot","req":{"coin":"BTC","interval":"15m",...}}`. Daily series work too: `out-gold-24h`, `out-sp500-24h`, `-btc-24h`.
- **Sample today:** last 50 markets (12:30 to 00:45): 19 up, 31 down, longest streak 6 ups, current streak 1 up. Market 11710 (strike $82,889, expiry 21:45): Yes traded as high as 99.8% and finished at 0.09%, No won. Market 11630 (strike $82,431, 17:45): the last Yes print was 99.8% and No still won, which fits settlement being a 60-second average after expiry.
- **Reliability: High data.** The markets are tiny ($100 to $800 each). Use for "coin flip" formats with no money claims.

#### D14. Fed, IPO and macro odds with a headline
- **Finds:** odds for the FOMC decision, the Anthropic first-day market cap ladder and IPO-confirmed markets. Trigger: a move of 3 points or more in 24 hours, or a matching headline. Feeds the "Informative finance" format.
- **Endpoint:** `GET https://o1.outcome.xyz/api/v1/markets/question/289` (Fed October 2026 question, `scheduledDecision:20261028-1800`) with `allMids` for the % and `candleSnapshot` for the 24h change. Anthropic ladder: `outcomeMeta` outcomes named `template:companyIpoFirstDayMarketCap` (description has `marketCapThresholdB`). Headlines: `GET https://news.google.com/rss/search?q=Anthropic+IPO&hl=en-US&gl=US&ceid=US:en`, `GET https://www.federalreserve.gov/feeds/press_all.xml`. Cross-check: Polymarket (D11).
- **Sample today:** Fed decision 28 Oct 18:00 UTC: no change 81.0% (83.8% a day ago), hike 17.9% (15.7%), cut 0.4%. Anthropic first-day market cap above $1.5T 80.2%, $1.75T 73.7%, $2T 58.3% (was 65.7%), $2.25T 32.0%, $2.5T 26.5%. IPO confirmed by 30 Nov: 70.1%. Headlines: "Anthropic will be 'most ridiculous IPO' of year, analyst says" (CNBC, 7 Oct); Fed minutes for 15-16 Sep released 7 Oct.
- **Reliability: High** for odds. Headlines are keyword matches, so a person picks. Finance posts need the "not financial advice" line from the brief.

#### D15. Platform records
- **Finds:** record volume day, unique users, busiest hour, rewards paid. Feeds brand-update posts.
- **Endpoint:** `GET https://stats.outcome.xyz/api/builder/volume-daily?builder=0x<wallet>&startDate=2026-09-29&format=rows`, `.../api/builder/hourly?builder=...&hours=24`, `.../api/builder/stats?builder=...`, and `GET https://pd-liquidity-rewards-payouts.outcome-e91.workers.dev/v1/rewards`.
- **Sample today:** record volume day 12 Oct $6.74M (345,700 fills, 496 users), then 11 Oct $6.63M and 10 Oct $5.18M. The four days before were $0.67M to $0.92M. Yesterday was 2.2 times the 7-day average. Since launch the builder code has handled $129.5M, 26% of all HIP-4 volume, 5,366 users. Rewards paid: $340,096 of the $1M pool (matches the site banner), $11,630 in the last 24 hours, 3,090 wallets paid.
- **Reliability: High** for the numbers, careful with the meaning. Volume counts fills tagged with Outcome's builder code and is dominated by market makers (496 users made 345,700 fills). Fine for "record day", weak as "people are flocking in".

---

## 2. One collector run feeds all 15 (about 140 requests, about 4 minutes)

| Step | Request | Count | Feeds |
|---|---|---|---|
| Market list | `POST api.hyperliquid.xyz/info {"type":"outcomeMeta"}` | 1 | 5, 9, 10, 14 |
| Live chances | `POST api.hyperliquid.xyz/info {"type":"allMids"}` | 1 | 5, 9, 11, 14 |
| Market stats | `POST o1/api/v1/markets/lookup` (50 ids each, 313 open outcomes) | 7 | 3, 5, 6, 13 |
| Names | `GET outcome.xyz/api/incentives/current` | 1 | 9, 10 |
| Leaderboards | `POST o1/api/v1/leaderboard` (24h, 168h, 720h pnl; 24h losers; 24h volume; all) | 6 | 1, 12 |
| Top trader fills | per trader: `profile/lookup` + `userFillsByTime` (top 20) | 40 | 2, 3 |
| Top trader positions | per trader: `spotClearinghouseState` (top 20, wallets from the line above) | 20 | 4 |
| Settled results | `GET o1/api/v1/outcomes/settled?limit=50&name=...` | 3 | 6, 7 |
| BTC 15m | `GET o1/api/v1/markets/series` + one `markets/lookup` | 2 | 13 |
| 24h history | `candleSnapshot` for about 45 liquid coins (not needed if our archive exists) | 45 | 5, 8 |
| Platform | stats `builder/volume-daily`, `hourly`, `stats`, rewards | 4 | 15 |
| Outside | ESPN (2 to 3), TheSportsDB (1), Polymarket (1), news RSS (3) | 9 | 6, 8, 11, 14 |

Outcome's API allows 60 requests a minute per IP (response header `x-ratelimit-limit: 60`), so a 1.3 second gap is safe. Hyperliquid and the stats site returned no limit headers and never pushed back.

**Separate archive job (start now):** every 15 minutes save `allMids` (626 prices, one call). During matches and big events also save 1-minute candles, or subscribe to the WebSocket. This is what makes D5, D7, D8 and any "chart of the market" format possible after the event.

---

## 3. How markets are named and mapped (the "#2120" question)

- **Coin id = `#` + (10 x outcomeId + side).** Side 0 is the first side (Yes, or participant A), side 1 the second (No, or participant B). `#2120` is outcome 212 side 0: "Spain to win the 2026 World Cup", Yes. `#1731` is outcome 173 side 1: Argentina NO. `#85650` is outcome 8565 side 0: Rams (to beat the Bills). Plain names (`BTC`) are perps, `@123` are spot pairs, `xyz:NAME` are trade.xyz perps. The two sides of one outcome add to about 100% (`#108280` 80.30% and `#108281` 19.70%).
- **Master list:** `outcomeMeta` (Hyperliquid) or `GET o1/api/v1/outcomes/meta` returns `outcomes[]` (`outcome` id, `name`, `description`, `sideSpecs`, `venue`) and `questions[]` (`question` id, `name`, `description`, `fallbackOutcome`, `namedOutcomes`). `description` is a pipe-separated list of `key:value` pairs (split on `|` then on the first `:`). 313 open outcomes and 35 questions today. `venue`: `out` = Outcome (191), `skew` (61), `txyz` (53, probably trade.xyz from the name), none = Hyperliquid's own recurring markets.
- **Football match ("Arsenal v Lille: Arsenal"):** question 412, `name` = `template:sportsContestResult`, description has `participantA:Arsenal|participantB:LOSC Lille|competition:UEFA Champions League|scheduledStart:20261013-1900`. `namedOutcomes` = `[10828, 10829, 10830]` = Arsenal win, Draw, Lille win. Yes coin of each: `#108280`, `#108290`, `#108300`. Mid prices: 80.3 / 13.6 / 6.3. The `fallbackOutcome` (10827) is the "other" bucket. Outcome names are `template:sportsContestParticipant2` (team win, `description` = `participant:Arsenal`) and `template:sportsContestDraw2` (draw).
- **Two-way game (NFL):** outcome 8565, `name` = `template:sportsContestWinner`, description has `participantA:Los Angeles Rams|participantB:Buffalo Bills|scheduledStart|shortNameA|shortNameB`. Side 0 coin = A wins, side 1 coin = B wins. Totals (`template:sportsTotal`, `line:54.5`, Over/Under) and spreads (`template:sportsSpread`, `spread:+2.5`) sit on other venues (`txyz`).
- **Price markets:** `template:binaryPrice` (`perp:BTC|threshold:81863|time:20261013-0100`, Yes = above), `template:priceTouch` (`target:87500|time:20261101-0000`), recurring series (`Recurring`, `class:priceBinary`, `period:1d` or 15m) with `metadata.category` such as `out-btc-15m`.
- **Fed, IPO, awards:** `template:policyRateNoChange / Decrease / Increase` under question 289, `template:companyIpoFirstDayMarketCap` (`company:Anthropic|marketCapThresholdB:1500`), `template:awardCandidate` (`candidate:Harry Kane`), tournament winners `template:sportsTournamentParticipant`.
- **Best source of nice titles:** `GET https://outcome.xyz/api/incentives/current` has 76 featured markets with clean names such as "UEFA Champions League Matchday 2: Arsenal v LOSC Lille" and "Federal Reserve's Open Market Committee October 2026 rate decision" (ids `Q412`, `Q289`, `O8565`). For the rest, build the title from the description fields as above. Do not use the fan site's titles for new markets, and do not use Outcome's `top-movers` titles (raw templates).
- **Question to side labels:** `POST /api/v1/markets/lookup` returns `metadata.sides[]` with names and `assetId` (for example "Atlanta Falcons" `#85640`) for sports markets.

---

## 4. Endpoint notes: exact working requests

Syntax is Git Bash `curl`. The fan site redirects http to https (HTTP 308), so use the https address. In Python use a plain `urllib` POST with `Content-Type: application/json`. All requests below returned HTTP 200 on 13 Oct 2026 unless stated. Sample responses: raw folder file in brackets.

### 4.1 Outcome official API, base `https://o1.outcome.xyz` (no key, JSON, CORS open)
Found in Outcome's own JS bundle on outcome.xyz (the SDK client). Limit: 60 requests a minute per IP.

```
# leaderboard: duration 24h|168h|720h|all, filter_by pnl|pnl_pct|volume, order_by asc|desc, limit max 100, offset+limit max 1000   [B01, B02]
curl -s -X POST https://o1.outcome.xyz/api/v1/leaderboard -H 'Content-Type: application/json' -d '{"duration":"24h","filter_by":"pnl","order_by":"desc","offset":0,"limit":10}'
# one trader's rank in a window (username only, address lookup is disabled)   [B05]
curl -s -X POST https://o1.outcome.xyz/api/v1/leaderboard/search -H 'Content-Type: application/json' -d '{"username":"trader-W","duration":"168h"}'
# wallet address, avatar, joined date; also accepts {"address":"0x..."} instead of username   [B03]
curl -s -X POST https://o1.outcome.xyz/api/v1/profile/lookup -H 'Content-Type: application/json' -d '{"username":"trader-W"}'
# P&L history for the chart; window 1d|7d|30d|all   [B04]
curl -s -X POST https://o1.outcome.xyz/api/v1/portfolio/lookup -H 'Content-Type: application/json' -d '{"username":"trader-W","window":"30d"}'
# market names + stats for up to 50 outcome ids   [B06]
curl -s -X POST https://o1.outcome.xyz/api/v1/markets/lookup -H 'Content-Type: application/json' -d '{"outcome_ids":[10828,8565,11748]}'
# one match question with all its outcomes   [B07]
curl -s https://o1.outcome.xyz/api/v1/markets/question/413
# results of recurring series: category from market metadata   [B08, B08b]
curl -s 'https://o1.outcome.xyz/api/v1/markets/series?category=out-btc-15m&past=50'
# every open market (92 KB)   [B10]
curl -s https://o1.outcome.xyz/api/v1/outcomes/meta
# newest registered / settled (limit max 50, filters name, class, underlying, period; no offset)   [B11]
curl -s 'https://o1.outcome.xyz/api/v1/outcomes/registered?limit=50'
curl -s 'https://o1.outcome.xyz/api/v1/outcomes/settled?limit=50&name=template:sportsContestWinner'
# settlement of one question or outcome   [B12]
curl -s 'https://o1.outcome.xyz/api/v1/settle/outcome/400?type=question'
# Outcome's own "top movers" (3 rows)   [B09]
curl -s https://o1.outcome.xyz/api/v1/top-movers
# live score and status; sport in football, basketball, tennis, baseball, volleyball, handball, cricket, ice_hockey, american_football, waterpolo, badminton, table_tennis, snooker, formula1, lol, dota2, csgo   [B13]
curl -s https://o1.outcome.xyz/api/v2/sports/american_football/matches/zp5rzobooy8vm82/live
```

Notes:
- Numbers in the leaderboard and portfolio are strings with many decimals. Parse as float.
- `markets/lookup` stats per side: `trades`, `uniqueTraders`, `volumeNotional`, `volumeContracts`, `lastPrice`, `vwap`, `minPrice`, `maxPrice`, `avgTradeNotional`, `medianTradeNotional`, `largestTrade`, `firstTrade`, `lastTrade`, `settlementClosedPnl`. Settled markets keep these, which is the only price-range record that survives settlement. `is_active` says whether the market is live.
- `series?past=` returns at most 50 results (about 12.5 hours of 15-minute markets). Categories seen: `out-btc-15m`, `out-eth-15m`, `out-hype-15m`, daily `out-sp500-24h`, `out-xyz100-24h`, `out-mu-24h`, `out-spcx-24h`, `out-cl-24h`, `out-gold-24h`, `out-silver-24h`, and Hyperliquid's own `-btc-24h`, `-eth-24h`, `-sol-24h`, `-hype-24h`. Composing a wrong category gives HTTP 400 with a message to read it from `metadata.category`.
- Live sports data (TheSports provider) for football comes as `match.home_scores / away_scores` arrays (goals, half time, red cards, yellow cards, corners, extra time, penalties). NFL live data includes `live.incidents` with scores and a play-by-play list.
- Same-origin and other Outcome services. `outcome.xyz/api/incentives/current` sits behind Cloudflare bot checks: curl's default User-Agent and a bare `Mozilla/5.0` got HTTP 403, a full browser User-Agent string and my Python request got 200. Treat it as optional and keep the description-based titles (section 3) as the fallback.
```
# 76 featured markets with clean names, listing times and reward sizes   [B14]
curl -s -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36' https://outcome.xyz/api/incentives/current
# liquidity-reward payouts (found in the JS): totals, per wallet, periods, leaderboard of wallets   [B16]
curl -s https://pd-liquidity-rewards-payouts.outcome-e91.workers.dev/v1/rewards
curl -s 'https://pd-liquidity-rewards-payouts.outcome-e91.workers.dev/v1/rewards/leaderboard?limit=3'
curl -s 'https://pd-liquidity-rewards-payouts.outcome-e91.workers.dev/v1/rewards/periods?limit=2'
```

### 4.2 Hyperliquid public info API, `POST https://api.hyperliquid.xyz/info` (no key)
```
# [C01] all open outcomes and questions
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"outcomeMeta"}'
# [C02] mid price of every coin; outcome coins start with '#' (626 today)
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"allMids"}'
# [C03] last 10 trades only, with both wallet addresses
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"recentTrades","coin":"#108280"}'
# [C04] order book, 20 levels a side
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"l2Book","coin":"#108280"}'
# [C05] candles: 1m, 15m, 1h, 1d tested; live markets only
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"candleSnapshot","req":{"coin":"#85650","interval":"1m","startTime":1791850000000,"endTime":1791853600000}}'
# [C07] a wallet's fills (max 2000 a call; move startTime past the last fill to page). Old fills stay available.
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"userFillsByTime","user":"0x<wallet>","startTime":1791765000000,"endTime":1791853600000}'
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"userFills","user":"0x<wallet>"}'
# [C11] a wallet's balances; outcome tokens are coins '+85650' etc (open positions)
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"spotClearinghouseState","user":"0x<wallet>"}'
# [C08] settled outcome details
curl -s https://api.hyperliquid.xyz/info -H 'Content-Type: application/json' -d '{"type":"settledOutcome","outcome":8564}'
```
- Fill fields: `coin`, `px`, `sz` (shares), `side`, `time`, `dir` (`Buy`, `Sell`, `Settlement`, `Merge Outcome`), `closedPnl`, `fee`, `startPosition`, `hash`. Opening fills have zero fee. A winning settlement pays $1 per share (px 1.0).
- WebSocket (works with Python `websockets`) [C09]: connect `wss://api.hyperliquid.xyz/ws`, send `{"method":"subscribe","subscription":{"type":"trades","coin":"#85650"}}`. Also `outcomeMetaUpdates` (new markets pushed), `allMids`, `l2Book`, `candle`. Not tested at 626 coins at once; check Hyperliquid's per-IP subscription limits before building the recorder.
- BTC reference for the 15-minute markets: `{"type":"candleSnapshot","req":{"coin":"BTC","interval":"15m",...}}` [C10].

### 4.3 Outcome stats site, base `https://stats.outcome.xyz/api` (no key, cached 60 s)
Outcome's analytics page (data by Hydromancer). `builder=0x<wallet>` is Outcome's builder code, the tag on every trade placed through outcome.xyz.
```
curl -s 'https://stats.outcome.xyz/api/builder/stats?builder=0x<wallet>'            # [D01] volume, share, fills, users
curl -s 'https://stats.outcome.xyz/api/builder/volume-daily?builder=0xab5d...b704&startDate=2026-09-29&format=rows'  # [D02] daily, back to 2026-05-02
curl -s 'https://stats.outcome.xyz/api/builder/hourly?builder=0xab5d...b704&hours=24'                              # [D03] volume, fills, activeUsers, newUsers, biggestNotionalFill
curl -s 'https://stats.outcome.xyz/api/builder/category-stats?builder=0xab5d...b704'                               # [D01] crypto 77%, sports 23%, economics 0.3% of builder volume
curl -s 'https://stats.outcome.xyz/api/builder/recent-fills?builder=0xab5d...b704'                                 # [D04] latest 100 fills with wallet
curl -s 'https://stats.outcome.xyz/api/aggregate/category?category=sports'                                         # network volume by builder
curl -s 'https://stats.outcome.xyz/api/outcomes/registered?kind=all&limit=100'                                     # [D05] newest 100, adds 24h volume and open interest
```
(Use the full 42-character builder address in real calls.) Live % fallbacks if Hyperliquid is down: `markets/lookup` `lastPrice` per side (last trade, not the mid), the same field in `stats.outcome.xyz/api/outcomes/registered`, or the Liquidiction pages. `liquidiction.xyz` is HTML only (server-rendered pages such as `/market/<slug>-<outcomeId>`), with no API routes I could find. Its settled-market pages show the result text and no price history in the page HTML.

### 4.4 Fan-built API, base `https://dev.jbfx.me/api` (unofficial, no key)
It relays o1 and Hyperliquid. Handy shortcuts, not a foundation: the site calls itself fan-built, runs on serverless hosting and can disappear.
```
curl -s 'https://dev.jbfx.me/api/leaderboard?duration=24h&limit=50'              # [A01] duration 24h|168h|720h|all, limit max 100 (default 25), offset works; 7d and 30d are rejected (bad_duration)
curl -s 'https://dev.jbfx.me/api/trader?username=trader-J'                  # [A05] address, joined date, 30 daily P&L points, pnl30d; username only
curl -s 'https://dev.jbfx.me/api/positions?username=trader-J&window=all&include=all'   # [A06, A07] positions + summary (wins, losses, winRate, pnl, bought, earned; counts resolved positions only); window 24h or all only; include=all adds open positions (trader-W: 134 rows against 111 resolved); truncated=true means the 2,000-fill cap was hit
curl -s 'https://dev.jbfx.me/api/top-trades?window=24h&limit=25&scan=20'        # [A08] the Top trades tab; window 24h|168h|720h|all; slow, partial
```
- **Card PNG:** `GET /api/card?coin=%232120&closedAt=1784533891137&username=trader-J` returns `image/png` [A09]. Optional: `theme=wc|default|hype|btc`, `closedAt` (picks the position), `address`, `title`, `side`, `avatar`, `download=1`. Size: 1,780 x 2,188 px (default card, measured) or 1,929 x 1,941 px (World Cup card), 1.5 to 3.6 MB, 1 to 7 seconds to render, cached 24h. It returns HTTP 409 `position_not_card_ready` for markets the site does not know. Passing `address` plus `title` plus `side` forces a name for those unknown markets only (tested on the NFL game). For markets the site "knows" only as a template id (all new football match markets), the card prints `template:sportsContestResult` and ignores our title. So cards are fine for price markets and the World Cup, unusable for football matches. Plan to render our own card in HTML (every field is in the data above) or ask the fan builder for a fix.
- The page `https://dev.jbfx.me/leaderboard` and `.../leaderboard/derive.js` contain the fan site's logic. `derive.js` rebuilds positions from fills and shows the Merge/Settlement handling and the 2,000-fill limit, which explain the artifacts in D2.

### 4.5 Free outside data (no key unless stated)
| Need | Request | Result |
|---|---|---|
| Football fixtures, scores, goal minutes | `GET https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/scoreboard?dates=20261013` (league slugs tested: `uefa.champions`, `uefa.europa`, `eng.1`, `esp.1`, `ger.1`, `fra.1`, `ita.1`) [E01, E02] | Events with `competitions[0].details` (minute, scorer, red and yellow cards) and DraftKings odds for upcoming games. Unofficial, no published terms. Cache 5 to 10 s |
| Football, second source | `GET https://www.thesportsdb.com/api/v1/json/3/eventsday.php?d=2026-10-13&l=4480` and `.../lookuptimeline.php?id=2494059` (public key `3`; UCL 4480, EPL 4328) [E04] | Fixtures, kickoff UTC, scores, goal minutes for finished matches |
| NFL scores and plays | `GET https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard[?dates=20261018]`, `.../football/nfl/summary?event=<id>` [E03] | Scores, status, DraftKings lines before kickoff, scoring plays with `wallclock`, win probability |
| Crypto candles and price | `GET https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=15m&limit=3`; `GET https://api.exchange.coinbase.com/products/BTC-USD/candles?granularity=900`; `GET https://api.coinbase.com/v2/prices/BTC-USD/spot` [E05] | All worked from this network. Settlement uses the Hyperliquid perp (4.2), so these are cross-checks |
| Fed and IPO headlines | `GET https://news.google.com/rss/search?q=<query>&hl=en-US&gl=US&ceid=US:en`; `GET https://www.federalreserve.gov/feeds/press_all.xml`; `GET https://www.cnbc.com/id/10000664/device/rss/rss.html` [E06] | Plain RSS. Google News works for any query. The CNBC feed returned 403 to curl's default User-Agent but 200 to a Python request, so send a browser User-Agent. GDELT's DOC API returned `{}` after 13 seconds, skip it |
| Other venues' odds | `GET https://gamma-api.polymarket.com/public-search?q=fed%20decision%20october&limit_per_type=3`; `GET https://external-api.kalshi.com/trade-api/v2/markets?series_ticker=KXFED&status=open&limit=40` [E07] | Polymarket and Kalshi prices (Kalshi's `api.elections.kalshi.com` host reset the connection here, `external-api.kalshi.com` works) |

---

## 5. Price history and large trades: what exists

| Question | Answer |
|---|---|
| Can we get the price history of a live market? | Yes. `candleSnapshot` on the outcome coin, 1m to 1d candles, with volume and trade count. 94 fifteen-minute candles came back for 24 hours. |
| Of a settled market? | No. HTTP 500 and `null`, tested on a World Cup coin, an NFL game that settled 12 Oct and a BTC 15-minute market that expired 20 minutes earlier. Outcome's page says it is still building settled-market charts. The only survivors are the lifetime stats (`minPrice`, `maxPrice`, `vwap`, `lastPrice`, `largestTrade`) in `markets/lookup` and `outcomes/settled`. |
| Can we rebuild an old price path from fills? | Not reliably. I tried the Coventry v Newcastle market with fills of 6 busy traders: plenty of pre-match ticks, none in play. |
| Individual large trades? | Not as a list. `recentTrades` = last 10 trades. Options: hourly maximum (stats site), `largestTrade` per market, per-wallet fills (months back are available, up to 2000 a call), recent-fills (100), WebSocket trades stream. |
| Can we see how a big position was built? | Yes, via fills. trader-J's $514,526 Spain position was 733 buys (median $595, largest $19,891) between 17 Jul 22:35 and 18 Jul 21:49 UTC, and the Argentina NO side was 331 buys. It was not one order. Good trader-story detail. |
| Who made a trade? | `recentTrades`, the WebSocket and `recent-fills` give wallet addresses. `POST /api/v1/profile/lookup` with `{"address":"0x..."}` returns the Outcome username (tested: the wallet seen in the live fills is trader-U, the $3.2M a day market maker). So whale wallets can be named. Keep addresses out of posts, and never use the lookup to unmask rows the leaderboard shows as anonymous. |

---

## 6. Failures, traps and gaps

1. **History after settlement is gone** (section 5). Fix: archive job, section 7.
2. **No global trade feed.** Whale detection is partial. Fix: WebSocket recorder for the big markets, or accept D3 as a weak detector.
3. **Names.** New markets show as templates on the fan site, on Outcome's top-movers and in Hyperliquid's own fields. Fix: title builder (section 3) and the incentives list.
4. **Fan P&L artifacts.** Busy accounts are cut at 2,000 fills, and Merge Outcome fills distort per-coin P&L: impossible exit prices, +7,319% "trades". Fix: the filter rule in D2 and our own fill build.
5. **Peak prices can be stray prints** (Liverpool 0.99). Fix: confirm blown leads with the goal timeline (ESPN or TheSportsDB) or our own saved prices.
6. **Volume numbers disagree.** The stats proxy's `volumeNotional24h` can exceed lifetime volume (outcome 11464 NO side: 110,548 in 24 hours against 9,805 lifetime). Leaderboard `volume` equals the sum of the trader's own buy and sell fills (checked: trader-P $5,351 exact). Outcome-page volume equals Yes plus No lifetime notional (checked on the settled Falcons v Ravens page: $262,391). The brief's HIP-4 figure ($14.7M a week, Liquidiction) is smaller than the stats site's Outcome-only $18.5M for 10 to 12 Oct, so definitions differ. Use one definition per post and name it.
7. **Cloudflare and cloud servers.** Outcome's WAF reportedly blocks AWS serverless addresses (statement in the fan site's code). Run the collector from a normal connection. The Hyperliquid API worked from here and the fan site says it is reachable from cloud too.
8. **`outcomes/registered` cursor on the stats proxy does not advance** (cursor in equals cursor out, same 100 rows; the site's own code stops on a repeated cursor). Use `outcomeMeta` plus `markets/lookup` for the full list.
9. **Win rate, outcomes traded and wins/losses** (shown on Outcome profile pages) have no official endpoint I could find. Compute from fills, or use the fan `positions` summary (built from the last 2000 fills).
10. **Avatars and banners** come as small numbers (`"avatar":"1"`, `"banner":"3"`); I found no public image path for them (`cdn.outcome.xyz/assets/avatars/...` returns 403). X-verified traders carry a `pbs.twimg.com` photo link on the fan API. For the Top 3 carousel's profile banner we need a screenshot of the profile page or the client's asset pack. The P&L chart can be drawn from `portfolio/lookup`.
11. **Football in-play data not verified.** Outcome's live endpoint should carry goal incidents like it does for NFL, but no football match was live during testing. First test: Lens v Sporting at 16:45 UTC today.
12. **Stats site odds pages are dead** for our purposes: hard wired to the finished World Cup winner market, `books: []`.
13. **Outcome's old feed routes** (`/api/v1/feeds/football/matches/...`, `/feeds/.../scoreboard`) returned Cloudflare 502 with `Retry-After: 60`. Use `/api/v2/sports/.../live`.
14. **Free football keys:** football-data.org returns 403 for the Champions League without a token and an empty list for `/v4/matches`. API-Football and The Odds API return missing-key errors. All three have free tiers (below).
15. **Chance definition.** `allMids` mids match Liquidiction's % to 0.1 point (Arsenal 80.3 against 80.4). I did not check which exact value the Outcome page shows (mid or last trade). Confirm once with a screenshot before using "chance" in captions.
16. **Wallet balances are public.** `spotClearinghouseState` also shows a wallet's cash and other tokens. Do not publish balances or addresses.
17. **Time.** Everything is UTC. Schedule strings are `YYYYMMDD-HHMM`. The site tab says "Today" but the API window is a rolling 24 hours.

---

## 7. What to do next

**Build order**
1. Start the archive job today (every 15 minutes `allMids`; 1-minute candles or WebSocket for football matches, NFL games and Fed day).
2. Easy and reliable first: D1, D9, D10, D14, D15, D13.
3. Then D2, D4, D6, D12 (need the filters above).
4. Last: D5, D8, D7 (need the archive or a recorder), D3 (weak), D11 (low hit rate).

**Free keys that would help** (no cost, sign-up needed)
- football-data.org token: fixtures and results for the Champions League and big leagues, 10 requests a minute.
- API-Football key: free 100 calls a day, in-play events (goals with minute) in one call.
- The Odds API key: free 500 credits a month, bookmaker odds for any league (better than ESPN's single DraftKings line).
- FRED API key: US rates and CPI series for Fed posts.

**Ask the client**
1. Written OK to name users (D1, D2, D12) and to show Merge-free P&L cards; anonymous rows stay anonymous.
2. Whether losses (the internal losers list in D1) may ever appear in posts, and whether showing open positions (D4) is fine.
3. Which "chance" and which volume figure the Outcome UI shows, so captions match the screen.

---

## 8. Files

Raw folder: `C:\VISION\VISION CLAUDE\outcome\research\raw\data-scout\`
- A01 to A09: fan API (leaderboard, limits and errors, trader, positions, top trades, card checks).
- B01 to B16: Outcome o1 and same-origin APIs (leaderboard, profile, portfolio, markets, series, outcomes meta, settled, live sports, incentives, failures, rewards service).
- C01 to C11: Hyperliquid info API and WebSocket (outcomeMeta, allMids, trades, book, candles, history-gone proof, fills, settledOutcome, BTC perp, wallet balances and open positions).
- D01 to D06: stats.outcome.xyz (builder stats, daily, hourly, recent fills, registered cursor, empty odds).
- E01 to E08: free outside data (ESPN, TheSportsDB, Binance/Coinbase, news, Polymarket/Kalshi, key gaps).
- F01: sample output of all 15 detectors, computed 13 Oct 2026 about 01:00 UTC.
