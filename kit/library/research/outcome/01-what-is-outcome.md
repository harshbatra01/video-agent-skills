# Outcome (outcome.xyz): fact-checked brief

Prepared 13 Oct 2026. Purpose: facts for faceless short-form posts (TikTok, Instagram, YouTube Shorts) promoting Outcome.
Companion files in this folder: 00-client-brief.md (the team's digest of the client brief), 02-reference-posts.md.

## How to read this file

- Tags like [O14] point to the source index at the bottom. Each entry there has a URL and a date. A number with a tag is sourced; a number with no tag is my own arithmetic and says so.
- UNVERIFIED = not confirmed by a first-party source (outcome.xyz, docs.outcome.xyz, Hyperliquid docs or announcements), or only seen in a weak source.
- Source grades: A = Outcome or Hyperliquid first-party. B = reputable press or research. C = trackers, vendor blogs, aggregators, fan-built tools. D = X posts I could not open, seen only through search summaries or aggregators.
- [C1] = 00-client-brief.md, i.e. what the team saw live in a browser on 13 Oct 2026.
- Tool limits (so you know what I could not see): X returns HTTP 402 to my fetch tool. These outcome.xyz pages return 403 to it: /terms, /privacy, /leaderboard, /rewards, /world-cup, /profile/..., market pages, /api/. The home page loads but live prices and percentages are filled in by JavaScript, so they show as blanks. The Terms text came to me as search-engine excerpts. Hyperliquid's info API is POST-only, so I could not query it. No browser, no logins, no downloads were used.

---

## 1. Bottom line

1. "Zero fees" is not accurate today. Opening a position is free and Outcome's own platform fee (builder code) is 0 for now. But a small fee is charged when you close or settle. In third-party data for three accounts, fee-bearing closes first appear on 5 Sep 2026 and run at roughly 0.05% to 0.14% of the money received (example: 3,000 USDC payout, 2.10 USDC fee). Closes up to 30 Jul 2026 showed no fee. [T3] See 2.10.
2. "World's FASTEST prediction market" has no support. No independent benchmark exists. The supportable speed fact is Hyperliquid's own: median 0.2 s and 99th percentile 0.9 s from sending an order to a committed response, for a co-located client. [H4] Outcome's own docs only say "near-instant". [O23] See 2.9.
3. "trader-J made 500k+ from 2 World Cup trades" checks out against the data I could read: +$503,008.19 on $760,764.81 staked, two trades (Spain YES, Argentina NO), both settled 20 Jul 2026. It is a huge outlier: #2 all-time is $66,934. [T3] See 5.5.
4. "Kimchi" could not be found on Outcome's leaderboard (not in the all-time top 1,000 by profit, not in the last-24h list). There is a famous unrelated crypto trader called Kimchi, so do not mix them up. See 5.6.
5. Not available in the US, UK, UAE, Singapore, Hong Kong, South Korea, China, Ontario, Belgium and sanctioned places (per the Terms). The operator is TytanTech Corporation of Panama. Outcome has no financial licence that I could find. See section 3 and section 9.
6. Outcome's "Same trade. Biggest payout." graphic ($322.00 vs $311.45 / $307.70 per $100) [C1] is almost exactly what Polymarket's and Kalshi's published entry fees would produce at the same price (my arithmetic from [N16][N17]). So the gap is a fee gap, not better odds. See 8.3.
7. Settlement is not instant for event markets. Resolution is in Beta with a stated target of 4 hours after the official result. [O11] The World Cup champion markets settled the morning after the final (07:51 UTC on 20 Jul 2026). [T3] See 2.5.
8. Volume figures disagree between sources because some count face value and some count cash paid. Always name the source and date. See 6.6.
9. The team is pseudonymous. No founder names, no VC funding found. Self-funded claim is UNVERIFIED. There is no token. See section 6.
10. Official social: X, Instagram, Discord (plus a Telegram link). No official TikTok or YouTube found. No creator, affiliate or ambassador programme found. See section 7.

### Claim check table (client brief wording)

| Claim | Verdict | Supportable wording |
|---|---|---|
| "World's FASTEST prediction market" | UNVERIFIED, no benchmark, not found in Outcome's own public pages | "Built on Hyperliquid's on-chain order book" |
| "Runs on Hyperliquid, a super fast blockchain" | True | "Runs on Hyperliquid, which reports about 200,000 orders per second" [H4][H5] |
| "Fully on-chain central limit order book" | True for matching, which happens on Hyperliquid's own chain (HyperCore). Outcome does not run its own matching engine [O7] | "Trades match on Hyperliquid's on-chain order book" |
| "Trades confirm in under 1 second" | Mostly true for order matching (median 0.2 s, p99 0.9 s, co-located client) [H4]. Not true for deposits (minutes) [O5] or event settlement (hours) [O11] | "Orders match in about a fifth of a second, per Hyperliquid" or just "near-instant" (Outcome's own word) [O23] |
| "Trade with zero fees on Outcome.xyz" | Not accurate (see 2.10) | "No fee to open a trade. Small fee when you close or settle." Or "0% Outcome platform fee" |
| "Outcome pays more than other venues" | Not a general fact. True only as a fee effect in one sample trade | Avoid, or "No entry fee, so more of your stake works for you" |
| trader-J 500k+ from 2 World Cup trades | Verified (see 5.5) | Say exactly what the data shows, with a past-results disclaimer |
| Kimchi on the leaderboard | UNVERIFIED | Do not use until the team shows a screenshot of it |

---

## 2. What it is and how it works

### 2.1 In plain English
- Outcome is a website for trading Yes/No event contracts. You buy a YES or NO token. The price in cents is the market's chance for that side. If your side is right, each token pays 1 USDC. If wrong, 0. [O3][O24]
- Money and trades live on Hyperliquid, not at Outcome. There is no separate Outcome account. Your Hyperliquid wallet works across the network, and collateral is shared with perps and spot. [O7]
- Outcome is two things: a front end (website) for Hyperliquid's HIP-4 markets, and a HIP-4 "deployer" that creates and settles its own markets under the venue name "out", backed by a 500,000 HYPE bond. [O8]
- Outcome describes the site as an interface to Outcome-deployed markets and other Hyperliquid markets. [O8]

### 2.2 Is it built on Hyperliquid HIP-4? Yes.
- HIP-4 is Hyperliquid's outcome-market upgrade: fully collateralised contracts that settle within a fixed range, no leverage, no liquidation. [H1]
- Hyperliquid announced it on 2 Feb 2026 (testnet first). [N1]
- HIP-4 went live on mainnet on 2 May 2026 with a recurring daily BTC binary. Outcome was one of the first front ends (the other named at launch was Stratium). [N5][N20]
- Real-world event markets (Fed, CPI, sports) arrived on 25 May 2026, with validators acting as the oracle. [N7]
- Permissionless deployment went live on mainnet on 29 Aug 2026. Outcome posted a 500,000 HYPE bond and became the first permissionless deployer. [H9, msg 585][N11]
- It is not an AMM, not a separate chain, and not Polymarket-style (no UMA oracle). [N4]

### 2.3 Contract mechanics
- Each market has a YES token and a NO token. The two sides share one order book: a YES bid at price p is the same as a NO offer at 1 - p. [H1]
- Prices run from about 0.1 cent to 99.9 cents (Hyperliquid bounds 0.001 to 0.999 dollars). [N4]
- The two sides add up to about 100 cents, minus the bid/ask spread. [O9][O24]
- No leverage, no liquidation, no margin calls. The most you can lose is what you paid. [O3]
- You can sell before the event resolves, at the current price. [O24]
- Split/merge: 1 USDC can be split into one YES plus one NO and merged back. In multi-outcome questions a set with one YES of every outcome pays exactly 1 USDC. [O24]
- Order types: limit (you set the price) or market (best available price). Market orders can slip across price levels (docs example: a 1,000-token buy at a 40 cent best price averages about 42.3 cents). [O6][O23]
- Open orders are cancelled automatically when a market resolves. [O12]
- Minimum order: Outcome's SDK enforces a $1 notional floor; the exchange minimum for outcomes is not documented (a Chainstack testnet doc said $10, UNVERIFIED for mainnet). [O25][N19]

### 2.4 How a payout works (two examples)
- Docs example: 100 YES tokens bought at 40 cents cost 40 USDC. They are worth 100 USDC if the event happens and 0 if not. [O3]
- Real example (fan-built data, settled 20 Jul 2026): 856,418 "Spain" shares in the 2026 World Cup Champion market bought at an average 0.6008, cost $514,525.96, paid $856,418.00, profit $341,892.04. [T3]
- The team's UI shows this as "$100 -> $X" payout lines next to the percentage. [C1][O1]

### 2.5 Resolution and settlement
- Price markets settle on Hyperliquid's mark price at the settlement time, by linear interpolation between the mark updates just before and after it. [O9][O12]
- Price Binary: average price (TWAP) over X seconds right after expiry, X scaled to the contract period; YES if at or above the strike. Price Touch: rolling 1-second TWAP, YES the moment it touches and stays YES; NO if never touched by expiry. Price Scalar: 1-second TWAP, pays in proportion inside a range. [O11]
- Event markets: Outcome resolves the markets it deploys against an official source named in the template. If the official source has not published, independent reputable reporting can be used. Later appeals or corrections do not change a resolved market. [O13]
- Markets deployed by Hyperliquid's validators are settled by a validator vote. [O12][N7]
- Timing: at mainnet rollout the target is resolution within 4 hours of the official result, with a goal of seconds. Resolution is in Beta. [O11][O13]
- Real timing example: the World Cup final was played 19 Jul 2026; the champion positions settled the next morning, 20 Jul 2026 at 07:51 UTC (match end time not checked). [T3][N24]
- Dispute process: none described. Outcome's own docs say there is no separate dispute token and no claims process. [O12] A review found Outcome's pages describe event resolution three different ways. [N21]
- Bond: 500,000 HYPE, held by Outcome, checkable on-chain from the deployer address 0x<wallet>. Validators can slash it if a market is poorly defined or settled wrongly. It cannot be withdrawn until all outstanding markets settle. [O8]
- Redemption is automatic. No claim step. Proceeds show up in the USDC balance. [O12]
- Void or cancelled events: general handling not covered in the settlement page. [O12] Sports templates do cover it: in two-way sports markets a draw, no contest or unresolved result pays $0.50 to each side; in three-way markets the draw is a real outcome. [O13]
- Sports counting rule: only the "Counted Play" counts. Extra time, overtime, shoot-outs and tiebreaks are excluded even if a source includes them. [O13] This matters for football match posts.
- Fed rate template: three-way (No change, Decrease, Increase). If the decision is cancelled, postponed without replacement, or unpublished by the deadline, "No change" resolves YES. [O13]
- Outcome's selection algorithm lists event markets, capped at 100 live markets and 500 new markets per day. Single contests go live about 24 hours before the event. Users can request markets in Discord. [O13]

### 2.6 Money in and out
- Settlement currency is USDC. [O3][O7] Older press and trackers say USDH, which Hyperliquid has since phased out (USDH markets settled by 20 Jun 2026). [H9, msgs 560-561][N4] Do not say "USDH".
- Deposit: open the Deposit panel, choose the source chain and asset, enter amount, confirm in wallet. Native USDC goes through Circle CCTP. Other assets go through Across and are converted to USDC. Most deposits land within minutes. [O5]
- Which chains and tokens are supported is not listed in the docs; the Deposit panel decides. Card or bank deposit is not documented. [O5]
- Withdraw: USDC via CCTP, Arbitrum by default (any EVM address allowed). Costs: a HyperEVM gas fee of a fraction of a cent plus Circle's forwarding fee, roughly 20 cents to Arbitrum. Outcome charges no withdrawal fee. Usually completes in seconds. [O15]
- Fiat withdrawal is "coming soon" via Meld and will need identity verification (KYC) and depend on region. [O15]

### 2.7 Account, KYC, custody, web vs mobile
- Sign-in: social login through Privy (Google, Apple, email; Privy creates a wallet) or any EVM wallet (MetaMask, Rabby). Both are described as non-custodial. [O4] The team also saw X and wallets offered live on 13 Oct. [C1]
- KYC: I found no KYC step for trading in Outcome's docs. The only KYC mention is for the upcoming fiat withdrawals. [O4][O15] The Terms still require you to be outside prohibited places and 18+ (see section 3).
- Custody: non-custodial. If outcome.xyz goes down, funds and positions stay on Hyperliquid and can be closed through other HIP-4 interfaces. [O7][O21]
- Web vs mobile: only the website found. The mobile layout has a bottom bar (Home, BTC 15m, Activity, Profile). [O1] I found no iOS or Android app (UNVERIFIED).
- Support: Discord ticket, hello@outcome.xyz, in-app live chat (Support link in the footer). [O22]

### 2.8 Onboarding steps a new user goes through
1. Open outcome.xyz. Browsing needs nothing. [O4] (From the US you can browse but wallet connect, deposit and trading are disabled; seen on market pages through search results.)
2. Sign in: Google, Apple, email, X (team saw it), or connect a wallet. [O4][C1]
3. Accept the Terms of Service with a one-time signature, separate from connecting. [O4]
4. Approve Outcome's builder code once (a transaction request). It lets Outcome attach its fee code to trades; the fee is currently 0. Builder address 0x<wallet>. [O4][O17]
5. Optional: activate the Hyperliquid referral code for a 4% discount on taker fees (first $25M of volume). Offered at first sign-up, or later from the profile page. [O16][H6]
6. Fund the account (see 2.6). [O5]
7. Enable trading once: self-custody wallets sign a one-time message that lasts until the session ends; Privy users get this automatically at sign-in. After that you do not sign every order. [O6]
8. Open a market, pick the outcome (YES/NO or team), choose limit or market, enter size, review, confirm. The order goes in instantly; it fills at once if the book can fill it, otherwise it rests until filled or cancelled. [O6][O23]
9. Hold to settlement (automatic payout) or sell any time. Withdraw USDC to Arbitrum or another chain. [O12][O15]

### 2.9 Speed claims check
- Hyperliquid docs: mainnet supports about 200,000 orders per second; one-block finality. [H4][H5]
- Hyperliquid docs: for an order from a co-located client, end-to-end latency (send request to receive committed response) has median 0.2 seconds and 99th percentile 0.9 seconds. [H4]
- A normal person on a phone is not co-located, so real numbers will be a bit higher. The official numbers are for co-located clients.
- Outcome's docs give no figure: submission is "near-instant", cancels "generally instant". [O23]
- Other numbers in the wild (0.07 s block times, "tens of milliseconds") come from secondary or vendor sources and do not match the official docs. Ignore them. [N23]
- No source ranks Outcome or HIP-4 as the fastest prediction market. Polymarket matches orders off-chain and settles on-chain, which is also fast in practice, and its speed is not measured in the press. [N19]
- Order of magnitude on scale: HIP-4 7-day volume was $14.7M on 12 Oct 2026 [T1], against Polymarket about $3.6B and Kalshi about $15.8B in the last week of Sept 2026 [N14]. "Fastest" does not mean "biggest".

### 2.10 "Zero fees" check

| Cost | Status on 13 Oct 2026 | Evidence |
|---|---|---|
| Opening / buying a position | No fee | Hyperliquid fee page: outcome trading only charges fees when closing or settling [H3]. Open positions show fees of 0 in third-party data [T3] |
| Closing by selling, or holding to settlement | A small fee exists. Observed about 0.05% to 0.07% of proceeds on some markets and about 0.10% to 0.14% on others (the football match markets in the sample were in the higher group). Example: 3,000 USDC payout, 2.10 fee; 584 payout, 0.8176 fee | Third-party fan API (dev.jbfx.me) for accounts trader-W, trader-Z, trader-D: fee-bearing closes first visible 5 Sep 2026, none visible between 30 Jul and 5 Sep; zero fees on every visible close through 30 Jul 2026 [T3]. Consistent with Hyperliquid's mid-Aug 2026 notice that fees would be switched on at the next upgrade, at an average of half the spot trading fee [H9, msg 580]. The notice that switched them on is not in the messages I could read. UNVERIFIED by a first-party rate table |
| HIP-4 base fee, first-party wording | HIP-4 page still says "fees are currently zero for initial testing" (undated) [H1]. Conflicts with the above. Trust the dated evidence, flag the page as stale | [H1][H9] |
| Outcome builder-code fee | 0 now. Docs say it may change. User approves a maximum | [O14][O17] |
| Deployer fee scale (a 0 to 10x multiplier on the base fee, set by each deployer) | Outcome's value is not published. The roughly 2x gap between football match markets (about 0.14%) and some other markets (about 0.07%) in the sample is consistent with different scales (my inference, UNVERIFIED) | [H2][H9, msg 580][T3] |
| Settlement fee | Docs say one is deducted from payouts and shown in each market spec; the amount is not in the docs. In July 2026 payouts equalled shares x $1 exactly (no deduction) | [O12][O14][T3] |
| Maker rebates | None on outcome markets | [H3] |
| Deposit | Network cost for CCTP; Across fee varies by chain and asset. Shown before you confirm | [O5][O14] |
| Withdrawal | About 20 cents (CCTP) plus a fraction of a cent of gas. Outcome adds nothing | [O15] |
| Spread | A real cost, wide in thin markets and near resolution | [O21] |
| Referral discount | 4% off taker fees on the first $25M of volume. It discounts a fee that exists | [O16][H6] |

How other venues charge (published formulas):
- Polymarket taker fee = shares x rate x p x (1 - p), by category: crypto 0.07, sports 0.05, finance 0.04, politics 0.04, economics 0.05, culture 0.05, geopolitics 0. Makers pay nothing and get rebates. Docs example: 100 sports shares at $0.50 = $1.25. [N16] (checked 13 Oct 2026)
- Kalshi taker fee = 0.07 x contracts x p x (1 - p) rounded up to the next cent; makers 0.0175 on products that have maker fees. [N17] (read through a search excerpt of kalshi.com/docs/kalshi-fee-schedule.pdf; the direct fetch failed)

Safer wording: "No fee to open a trade. A small fee (roughly 0.05% to 0.14% of what you receive) applies when you close or settle. Check current fees in the app." If the client insists on "zero fees", get it in writing and ask which fee they mean.

---

## 3. Who can use it

From Outcome's Terms of Service (operator: TytanTech Corporation, Panama). I could not open the page (403); this is from search-engine excerpts of the Terms and should be rechecked against the live text. [O26]
- Prohibited places (residents, people located there, or companies incorporated or based there, plus citizens or nationals of these places wherever they are): United States and its territories; United Kingdom; UAE; Singapore; Hong Kong; South Korea; China; Province of Ontario (Canada); Belgium and other EU member states where the activity is not permitted; Cuba; Crimea and occupied regions of Ukraine; Iran; North Korea; Sudan; Syria; Afghanistan; Myanmar; and anywhere under UN, UK, US or EU sanctions. The company can add places.
- Not named in the excerpts I read: India, France, Germany, Australia, Quebec, Thailand, Taiwan, Poland, Italy, Switzerland. That is not clearance. India is UNVERIFIED either way and I did not research Indian law.
- Minimum age 18, or the local age of majority if higher.
- No VPN, proxy or Tor to get around blocks. The company uses geo-blocking, IP and device checks, and suspends immediately. It can suspend or revoke access at any time.
- Disputes: Panama law, binding individual arbitration in Panama City (CECAP), class action waiver.
- Docs risks page: unavailable in the US, certain Canadian provinces and sanctioned territories; Hyperliquid has its own restrictions; you must confirm local legality yourself. [O21]
- Hyperliquid also blocks US users in its UI and API. [N19] Outcome market pages show a "not available in your region (US)" notice to US visitors, and wallet connect, deposits and trading are switched off there (seen through search results of the market pages, not by me directly).
- Content consequence: do not target US, UK, UAE, Singapore, Hong Kong, South Korea, China, Ontario or Belgium audiences. Put "not available in some countries" in the post.

---

## 4. Markets

### 4.1 Categories
- Site tabs on 13 Oct 2026: All, Sports, Crypto, Economics, Finance, Esports. [O1] The site map confirms the same five category paths (sports, crypto, esports, economics, finance). [O27]
- Social bios also say Politics and Culture ("Politics & more"; "News, Finance, Politics & Culture"). [O29] There is no Politics or Culture tab on the site, so treat those as UNVERIFIED as live categories. A few culture-type markets exist (for example "Anthropic First-Day > $1,750B"). [O1]
- Esports: a tab and URL path exist, but I could not see how many esports markets are live (UNVERIFIED).

### 4.2 Market types
- Binary: YES/NO for events, or UP/DOWN for price direction. [O9]
- Multi-outcome "question": exactly one outcome resolves YES (tournament winner, Ballon d'Or, election, Fed decision). [O9]
- Price bucket / "multi-price": price ranges, exactly one bucket pays. [O9]
- Recurring series: a new instance deploys on a fixed cadence (15 minutes, daily); only one live instance per series; positions do not roll over. [O10]
- Price Touch: "does X touch a level by end of month". [O11]
- Sports templates: two-way contest winner; tournament winner with a "No winner" fallback; three-way contest result (home, draw, away); a scalar over/under template exists but was not in use at launch. [O13]
- Examples seen live on 13 Oct: BTC / HYPE / ETH Up or Down 15 min; BTC Multi Outcomes Daily (price ranges); WTIOIL and SPCX Up or Down Daily; "BTC touches 87,500 / 90,000 by end of October 2026"; "HYPE touches 100 by end of October 2026"; "S&P500 above 7,805.7 at 13 Oct 2026 20:00 UTC"; Gold above 4,174; Silver above 60.347; "FED Decision in October?" (Increase, Decrease, No change); football (Champions League and Europa League matches, EPL winner, UCL winner, Ballon d'Or); NFL games and the 2027 NFL winner; 2026/2027 NBA winner. [O1]

### 4.3 Volumes on the Outcome home page (13 Oct 2026, total volume shown on each card) [O1]

| Market | Volume |
|---|---|
| 2026/2027 UEFA Champions League winner | $2.4M |
| 2026/2027 English Premier League winner | $2.2M |
| 2027 NFL winner | $2.0M |
| FED Decision in October? | $894.1k |
| 2026 Ballon d'Or winner | $554.2k |
| NFL: Los Angeles Rams vs Buffalo Bills | $530.7k |
| UCL: RC Lens vs Sporting CP | $143.3k |
| BTC touches 87,500 by end of October | $136.6k |
| Anthropic First-Day > $1,750B | $135.7k |
| BTC touches 90,000 by end of October | $132.6k |
| UCL: Galatasaray vs FC Barcelona | $97.5k |
| HYPE touches 100 by end of October | $90.4k |
| WTIOIL touches 100 by end of October | $75.4k |
| 2026/2027 NBA winner | $23.2k |
| S&P500 above 7,805.7 (13 Oct) | $1.9k |
| WTIOIL Up or Down Daily | $1.1k |

### 4.4 Live percentages (third-party aggregator, fetched 13 Oct 2026, snapshot time not shown; prices move all day) [T1]
Outcome's own home page shows blanks for percentages when fetched without JavaScript, so these come from Liquidiction's market list.

| Market (deployer) | Chance | 24h volume | Open interest | Notes |
|---|---|---|---|---|
| BTC above $82,185 (Outcome) | YES 23.9% | $0 | $437 | |
| HYPE above $82.285 (Outcome) | YES 67.9% | $0 | $377 | |
| ETH above $2,473.6 (Outcome) | YES 7.1% | $0 | $185 | |
| BTC touch ladder, $75,000 level (Outcome) | YES 24.4% | $155,595 (whole ladder) | $81,837 | Expires 1 Nov |
| WTI touch ladder, $75 level (Outcome) | YES 8.5% | $109,618 (whole ladder) | $25,915 | Expires 1 Nov |
| S&P 500 above $7,805.7 (Outcome) | YES 57.3% | $1,667 | $618 | |
| Gold above $4,174 (Outcome) | YES 46.6% | $531 | $313 | |
| Crude oil above $92.386 (Outcome) | YES 56.6% | $636 | $534 | |
| RC Lens v Sporting CP | 37.9 / 25.4 / 36.7 (home / draw / away) | $97,487 | $7,022 | 13 Oct 16:45 |
| Galatasaray v Barcelona | 10.4 / 12.9 / 76.7 | $44,770 | $19,097 | 13 Oct 19:00 |
| Inter v Club Brugge | 78.0 / 14.4 / 7.7 | $37,721 | $5,863 | 13 Oct 19:00 |
| Arsenal v Lille | 80.4 / 13.5 / 6.3 | $19,964 | $10,992 | 13 Oct 19:00 |
| Atletico Madrid v Man Utd | 50.6 / 24.1 / 25.1 | $43,398 | $22,049 | 13 Oct 19:00 |
| Viking FK v Bayern Munich | 4.2 / 6.3 / 89.5 | $29,308 | $24,203 | 13 Oct 19:00 |
| NFL: LAR v BUF moneyline | prices not shown | $293,051 | $30,145 | 13 Oct 00:15 |
| For contrast, Hyperliquid's own daily BTC market, "BTC above $83,988" | YES 0.8% | $107,564 | $125,087 | Not an Outcome-deployed market |

### 4.5 Typical volume and liquidity (read from the tables above)
- Season-long futures (UCL, EPL, NFL winners): about $2M each in total volume.
- Single matches, 24h volume on 13 Oct: Champions League about $11k to $97k (open interest about $2.8k to $24k); Europa League about $0.4k to $3.8k (open interest about $0.4k to $1.7k); NFL games about $42k to $293k (open interest about $1.2k to $30k). Total volume shown on two Champions League cards: $97.5k and $143.3k. [T1][O1]
- Month-end "touch" ladders (BTC and oil): about $110k to $156k of 24h volume across the whole ladder, with open interest of about $26k to $82k. [T1]
- Single daily threshold markets deployed by Outcome: from $0 to a few thousand dollars in 24h volume and a few hundred dollars of open interest. Thin. [T1]
- Largest individual markets ever, by all-time volume (HIP-4, all front ends): three World Cup champion markets at $11.9M, $9.0M and $6.3M, then daily BTC strikes at $2M to $3.6M each. [T1] (12 Oct 2026)
- Outcome's own risk page says spreads can be wide in quieter markets and books thin near resolution. [O21]
- Whole-network scale for context: 276 open markets on 12 Oct 2026, 10,305 deployed since 2 May, 10,121 settled. [T1]

### 4.6 Dated hooks visible on 13 Oct 2026
Champions League matchdays 13 to 15 Oct; NFL games; the October Fed decision market; BTC and HYPE and oil end-of-month touches; Ballon d'Or 2026 winner. [O1][T1]

---

## 5. Leaderboard and P&L

### 5.1 What exists
- Official page: https://outcome.xyz/leaderboard (leaderboard icon in the header; also in the site map). [O1][O27] It loads data by JavaScript; my fetch got 403.
- Per the team's live look: windows Today / 7D / 30D / All, sorted by P&L, 46 pages. [C1] Docs say traders are ranked by P&L and volume and shown by wallet or profile. [O19]
- Profiles: outcome.xyz/profile/<name>. The team saw outcomes traded, win rate, wins and losses, P&L chart (1D, 7D, 30D, All), portfolio, volume, Hall of Fame badges, open positions and history. [C1]
- Badges and cards: achievement items with no money value; up to 3 can be pinned to a profile, visible to people who open it from the leaderboard. [O18]
- Home page has "Traders of the day" and "Top movers" sections (empty when fetched without JavaScript). [O1]
- Shareable P&L cards: no official feature is documented. The "cards" in Outcome's docs are badges, not P&L cards. [O18] The card maker in the client brief is a fan-built site (dev.jbfx.me/leaderboard, builder not named, no Outcome affiliation shown). It offers Daily / Weekly / 30 days / All time and card themes (Auto, World Cup, Default, Hype, BTC). [T3]
- Anonymous option: some leaderboard rows are flagged anonymous and show no username. Do not unmask them using wallet addresses. [T3]

### 5.2 Third-party leaderboards (not Outcome)
- Loris Tools: Outcome.xyz trader leaderboard, ranked by volume, all-time, 4,804 traders, snapshot 12 Oct 2026 20:04 UTC. Shows wallet addresses only (no usernames). Top 25 by volume include one trader at +$107.76K realised P&L; most show small negatives. [T2]
- Liquidiction: HIP-4 leaderboard "across all frontends" with 24H / 7D / 30D / All tabs; rows did not render for me. [T1]

### 5.3 Fan-built API snapshot (all-time list, updated 12 Oct 2026 00:41 UTC; cap 1,000 rows)
| Rank | Username | P&L | P&L % | Volume |
|---|---|---|---|---|
| 1 | trader-J | $503,008.19 | 66.12% | $760,764.81 |
| 2 | (anonymous) | $66,934.50 | 15.58% | $429,524.55 |
| 3 | trader-D | $62,392.16 | 23.28% | $268,031.12 |
| 4 | trader-28 | $59,202.23 | 15.59% | $379,858.22 |
| 5 | trader-Z | $52,213.55 | 10.92% | $478,309.22 |
Source [T3]. #1 is 7.5 times #2 (my arithmetic).

Last-24h list (updated 12 Oct 2026 23:31 UTC): 443 traders; #1 "trader-W" +$16,838.68 on $79,604 volume; #2 trader-P +$5,982.82; #3 trader-B +$3,710.73. [T3] Use this scale when the team shows "realistic" numbers.

### 5.4 Username pattern
Many default names look like word_word plus four digits (trader-J, trader-D, trader-N, trader-B, trader-F), which suggests Outcome auto-generates names and users can rename (trader-W, trader-Z, trader-Q). Inference only, UNVERIFIED. [T3]

### 5.5 trader-J: what can be verified
Source: fan API positions and trader endpoints, read 13 Oct 2026. They match what the team saw on outcome.xyz. [T3][C1] I could not check the fills on a Hyperliquid explorer because those apps need JavaScript.

| | Spain | Argentina NO |
|---|---|---|
| Market | 2026 World Cup Champion, "SPAIN TO WIN" (coin #2120) | 2026 World Cup Champion, Argentina, NO side (coin #1731) |
| Shares | 856,418 | 407,355 |
| Average entry | 0.6008 | 0.6045 |
| Cost | $514,525.96 | $246,238.85 |
| Paid at settlement | $856,418.00 | $407,355.00 |
| Profit | $341,892.04 (66.45%) | $161,116.15 (65.43%) |
| Opened (UTC) | 17 Jul 2026 22:35:22 | 17 Jul 2026 23:24:42 |
| Settled (UTC) | 20 Jul 2026 07:51:31 | 20 Jul 2026 07:51:27 |

- Totals: 2 positions, 2 wins; bought $760,764.81; earned $1,263,773; profit $503,008.19. The sums reconcile.
- Fees on both positions: 0. Payouts equal shares x $1 exactly. [T3]
- Account created 17 Jul 2026 22:34:31 UTC (about a minute before the first trade, two days before the final). No activity in the last 30 days. Public address shown by the fan API: 0x<wallet> (pseudonymous; for checking only, do not put it in posts). [T3]
- Context: Spain beat Argentina 1-0 in the final on 19 Jul 2026. [N24] Both positions were effectively the same bet (Spain wins) placed within an hour at about 60 cents. Argentina had the busiest champion book in the World Cup markets ($35.4M, Quicknode count). [N22]
- Outcome's own X post on 7 Jul 2026 said its top three traders were up $200K+ that month, with no names (grade D, seen via search summary). A user post on 19 Jul 2026 said top traders were "up hundreds of thousands" (anecdote). [D][T4]
- Safe use: it is a real result, an extreme outlier and a concentrated two-trade bet on one match. Never present it as typical. Add a past-results disclaimer. The user is not flagged anonymous, but get the client's written OK to name or card a real user.

### 5.6 Kimchi
- No username "Kimchi" or "kimchi" or "kim chi" in the fan API all-time list (all 1,000 rows checked across 10 pages) or the 24h list (all 443 rows checked). The API only supports 24h and all-time, so 7D and 30D lists were not checked. [T3] It is also not in Loris's top 25 by volume, which lists wallets only. [T2]
- There is a famous unrelated "Kimchi" (@kimchi1x on X), reported in late July 2026 to have made about $40M on the TRUMP memecoin; the figure is disputed. [N26] One of the team's reference reels (Instagram, shant.tradez, 27 Jul 2026) jokes about this person. [02-reference-posts.md]
- So the "Kimchi" in the brief may be that viral person, not an Outcome user. UNVERIFIED either way. Ask the client for a screenshot. Do not imply any link between Outcome and the viral trader.

---

## 6. Company

### 6.1 Operator and legal
- Terms name TytanTech Corporation, incorporated in Panama, as the provider of the Outcome services. It says it does not own, control or custody Hyperliquid, and the site only submits orders. [O26] (search excerpt)
- No financial licence found. Prediction markets are regulated differently by country and rules are changing. [O21]

### 6.2 Timeline
| Date | Event | Source |
|---|---|---|
| Dec 2024 | X account @Outcomexyz created; renamed 3 times, last on 2 Feb 2026 | [T4] |
| 22 May 2025 | Discord server created (derived from the server ID, my calculation) | [O28] |
| 4 Nov 2025 | X post about a new leaderboard and bridge after a HyperEVM mainnet go-live (grade D, UNVERIFIED) | [D] |
| 2 Feb 2026 | Hyperliquid announces outcome trading (HIP-4) on testnet | [N1] |
| 30 Apr 2026 | Pre-launch post: 200,000+ testnet users, 500+ resolutions (grade D) | [D] |
| 2 May 2026 | HIP-4 mainnet; Outcome front end live | [N5][N20] |
| 11 Jun to 19 Jul 2026 | World Cup. Spain beat Argentina 1-0 in the final on 19 Jul | [N24] |
| 29 Aug 2026 | Permissionless HIP-4 deployment; Outcome posts a 500,000 HYPE bond (about $42M then), launches 28 markets and a rewards programme of up to $1,000,000 | [N11][H9] |
| 10 Sep 2026 | trade.xyz launches rival HIP-4 "Events" | [N15] |
| 5 Oct 2026 | SDK @outcome.xyz/hip4 v1.3.0 released | [O25] |
| 11 Oct 2026 | Outcome says daily volume hit a record $5.18M (X, via aggregator) | [T4] |

So: "launch" is 2 May 2026 for the front end and 29 Aug 2026 for Outcome's own deployer venue. Sources mix these up.

### 6.3 Team
- No public founder names. GitHub org shows no public members. [O31]
- A launch-day post (2 May 2026) congratulated "@InfiniteAK4 and the team". Role not stated (grade D). A coin directory lists three co-founder handles (OutcomeAK, MIG, Gyomei). UNVERIFIED and weak.
- X profile location reads Georgia. [T4]
- The public SDK repo lists one contributor by real name; I am not repeating it because role is unconfirmed.

### 6.4 Funding
- No VC funding reported. "Self-funded, no venture capital" appears in a Phemex article (seen only through a search summary, direct fetch failed; it dates the 500,000 HYPE stake at about $16M, from the earlier testnet period) and on an aggregator page. UNVERIFIED. [N31][T4]
- What is verifiable: Outcome says it holds a 500,000 HYPE bond on-chain at the deployer address in 2.5. KuCoin/Odaily put it at roughly $42M on 29 Aug 2026. [O8][N11]

### 6.5 Relation to Hyperliquid
- Independent third-party builder, not run by Hyperliquid Labs. Hyperliquid runs the chain, matching, oracle for its own markets, and the HIP-4 rules. Outcome runs the website and its own deployer venue. [O7][O8]
- On 12 Oct 2026 there were 3 registered HIP-4 deployers on mainnet (Outcome, Skew, trade.xyz Events) and 28 approved templates. [T1][T2]
- Do not say "official Hyperliquid product".

### 6.6 Traction (names the source; definitions differ)
Volume can be quoted as face value (contracts) or cash paid (premium). Example: the first daily BTC market had 6.6M contracts but $3.3M premium. [N27] Always say which.

| Figure | Date | Source |
|---|---|---|
| HIP-4 day one: $6.05M volume, about 0.7% of prediction market volume | 2 to 3 May 2026 | [N27] |
| First three daily BTC markets: $9.3M premium volume, 4,039 wallets, 129,802 fills | 5 May 2026 | [N27] |
| Outcome routed about $1.5M, 3% of HIP-4 activity | by 18 May 2026 | [N10] |
| HIP-4 weekly volume $16.32M (World Cup $9.63M, about 60%); open interest all-time high about $24.77M | 11 Jun / 28 Jun 2026 | [N9] |
| HIP-4 first month about $100M | 20 Jul 2026 | [N8] |
| After 29 Aug opening, Outcome about 85% of HIP-4 volume; HIP-4 Aug daily average $545K; 31 Aug $1.97M | 3 Sep 2026 | [N12] |
| Outcome volume above $11M since 29 Aug; about 70% share on 31 Aug; daily traders 1,256 to 1,841 | 4 Sep 2026 | [N13] |
| HIP-4 cumulative above $350M (trackers about $395M mid-Sept) | 25 Sep 2026 | [N14] |
| HIP-4 crossed $520M total volume, 162 days after launch (X post by Thriggar) | 11 Oct 2026 | [N28] |
| Outcome's own posts: "$110,000,000 in outcomes traded on HIP-4", on track for $500M with about 20,000 traders, Outcome nearly 1/4 of HIP-4 volume | 9 to 10 Oct 2026 | [T4] (grade D) |
| Outcome says a record $5,180,000 daily volume | 11 Oct 2026 | [T4] (grade D) |
| HIP-4 all front ends: all-time $332.2M, 24h $3.78M, 7d $14.73M, 30d $51.11M | 12 Oct 2026 22:59 UTC | [T1] |
| HIP-4 unique traders: 24h 2,175; 7d 3,470; 30d 6,195; all-time 21,262 | 12 Oct 2026 | [T1] |
| Wallets on Loris's Outcome.xyz leaderboard: 4,804 | 12 Oct 2026 | [T2] |
| Rewards: $340,096 of the $1M programme rewarded | 13 Oct 2026 | [C1] |
| Rewards paid: $238,071 to market makers and traders | 30 Sep 2026 | [D] (grade D) |
| Discord members: 6,313 (366 online) | 13 Oct 2026 | [O28] |

The tracker totals ($332M, $395M, $520M, "$110M") do not agree. Different trackers, different definitions. Quote one source and its date, never a mix.

### 6.7 Token
No token or points programme announced; airdrop pages call it speculation. [N29][N30] The Terms excerpt says points, if any, are virtual with no monetary value. [O26] Do not hint at an airdrop.

---

## 7. Brand

### 7.1 Name usage
- Brand name: **Outcome** (capital O). Used in the logo, page titles ("... | Outcome"), docs, X display name, Discord server name and the app manifest name. [O1][O27][O28]
- Domain: **outcome.xyz** (lowercase). The client's CTA writes "Outcome.xyz", which is readable but not how the site writes it. X handle: @Outcomexyz. Instagram: @outcomexyz.
- On-chain label: venue "out", name "OUT". [O8]
- Do not confuse with: Hyperliquid's generic term "outcome markets" (lower case, the product type); the X account @OutcomeMarketX ("forecast terminal of Hyperliquid", relation unknown); unrelated apps called Outcome.

### 7.2 Taglines and lines Outcome itself uses
- "Prediction Markets on Hyperliquid" (X bio; Discord description) [D][O28]
- "Trade outcomes on Sports, Crypto, Economics, Finance, Politics & more." (X bio, per search summary) [D]
- "Prediction markets on Hyperliquid. Trade Sports, News, Finance, Politics & Culture all in one place. Join the Rewards" (Instagram bio) [O29]
- "Trade to earn" and "Predict the outcome" on the rewards banner, with "Daily Rewards" [O1]
- "Trade Outcome Prediction Markets on Hyperliquid" (title of the Instagram short link page) [O30]
- "They saw the Outcome. Do you?" (X, 7 Jul 2026) [D]
- "On Outcome, you trade the game." (X, 8 Oct 2026) [T4]
- "The #1 prediction market on Hyperliquid" (X, 9 Oct 2026). A superlative; third-party share data is in 6.6. [T4]
- "World's fastest prediction market": not found in Outcome's public pages or docs. It is in the client brief only.

### 7.3 Colours and logo
- Background colour #0B0C0F (near-black), from the web app manifest (theme and background colour). [O27]
- App icon (outcome.xyz/icon.svg): two mirrored angular shapes forming one abstract mark, upper shape cyan #00FFFF, lower shape magenta #FF00F2. [O27]
- Logo lockup (outcome.xyz/lockup-dark-gray.svg): the same abstract symbol on the left plus a lowercase geometric sans-serif wordmark on the right, a single light gray fill #F5F5F5 for dark backgrounds. [O27]
- The team's live look: near-black UI, white Inter-style text, a lightning-bolt style logo, hot pink and neon yellow-green accents, a gold rewards ticket. [C1] I could not confirm the yellow-green hex.
- No press kit, /brand or /press page found (not in the site map). [O27] Ask the client for official assets and usage rules.

### 7.4 Official accounts

| Platform | Handle / URL | Size (date) | What it posts | Source |
|---|---|---|---|---|
| X | @Outcomexyz, https://x.com/Outcomexyz | 26.4K followers, 62 following, 11.1K posts; joined Dec 2024; snapshot date not shown (page checked 13 Oct) | Volume milestones, "market settled and traders paid", football match previews with market links, macro takes (Fed, oil), partner welcomes (Gate Web3, 9 Oct), rewards, a Fantasy Premier League league, memes. 14 posts between 8 and 11 Oct 2026 had 15 to 284 likes and 0.8K to 5.2K views | [T4] |
| Instagram | @outcomexyz, https://www.instagram.com/outcomexyz/ | 48 followers (13 Oct 2026) | Carousels and reels; 7 recent posts between 30 Aug and 11 Oct 2026; bio link go.outcome.xyz/ig with campaign tags | [O29][O30] |
| Discord | https://discord.com/invite/outcome | 6,313 members, 366 online (13 Oct 2026) | Support tickets, market requests, announcements | [O28] |
| Telegram | https://t.me/annoucement_outcome (spelled that way) | not shown; the page is a contact page, channel contents not visible | go.outcome.xyz/tg points to the World Cup page | [O31][O30] |
| TikTok | none found | n/a | n/a | search, 13 Oct |
| YouTube | no official channel found. youtube.com/@outcomexyz is an unrelated channel. A video titled "Prediction Markets on Hyperliquid powered by Outcome" exists, channel unknown | n/a | n/a | search, 13 Oct |
| GitHub | https://github.com/Outcome-xyz (SDK "hip4", 7 stars) | 6 followers | SDK, docs | [O31] |
| Docs / support | https://docs.outcome.xyz ; hello@outcome.xyz | | | [O22] |

### 7.5 Creator, affiliate, referral, ambassador, UGC programmes
- None public. I found no Outcome creator, affiliate, ambassador or UGC terms, and no payment terms. The team holds an "Outcome Creator Guide" [C1]; I could not see it.
- Referral: only the Hyperliquid referral programme. Referee gets 4% off fees on the first $25M volume. Referrer needs $10,000 volume to create a code and earns 10% of the referee's fees (less the referee's discount) on the referee's first $1B volume. [H6][O16] Outcome's docs do not name an Outcome code. Because outcome fees are tiny, referral earnings would be tiny.
- Tracking: Outcome records UTM parameters on a visitor's first visit. Embedded iframes carry no UTM, so Outcome cannot attribute them. [O25] Outcome's short links are on go.outcome.xyz (a Dub-hosted domain). Example: go.outcome.xyz/ig redirects to outcome.xyz/all with utm_source=instagram, utm_medium=social, utm_campaign=pd-launch, utm_content=bio. [O30]
- Rewards run by Outcome itself: the up-to-$1M "Daily Rewards / Trade to earn" programme paid in USDC; liquidity rewards of $1,000,000 in 24-hour epochs split 40% quotes, 50% maker fills, 10% taker fills, needing Outcome's builder code on every order, with typical per-market budgets of about $100 to $400 per 24h (Monarch runs the scoring); badges and cards. [O20][N21]
- World Cup Liquidity Programme (ended; the docs page now fails to load): champion market shared daily pool $600, match markets 5x during live play (grade D, search summary).
- UNVERIFIED third-party items: a weekly $10,000 prize for the best percentage P&L (Fridays 08:00 UTC) and a "Genesis Depositor" badge for depositing more than $10. [N29]
- Ask the client for: written creator terms, pay, approved claims, disclosure wording (#ad), geo rules, permission to show usernames and logos.

---

## 8. Competitors and positioning

### 8.1 Side by side
| | Outcome (HIP-4) | Polymarket | Kalshi |
|---|---|---|---|
| Where | Hyperliquid's own chain (HyperCore) | Polygon, off-chain order matching with on-chain settlement [N19] | Regulated US exchange (CFTC), US dollars |
| Matching | Fully on-chain order book [H5] | Off-chain order book [N19] | Exchange |
| Fees | Free to open; roughly 0.05% to 0.14% of proceeds on close or settle (see 2.10) | Taker fee by category, up to 7% x p x (1-p); makers free [N16] | 7% x p x (1-p) taker [N17] |
| Resolution | Outcome or Hyperliquid validators; Beta; no dispute process [O11][O12] | UMA optimistic oracle; 2-hour challenge window, 48 to 72 hours if disputed twice [N19] | Exchange team |
| Who can use | Not US, UK, UAE, Singapore, HK, Korea, China, Ontario, Belgium and others [O26] | International site blocks US users [N19] | US-focused, regulated [N4] |
| Latest weekly volume | HIP-4 all front ends $14.73M (7d to 12 Oct 2026) [T1] | about $3.6B (last week of Sept 2026, Artemis) [N14] | about $15.8B face value (same week) [N14] |
| Strength | Speed, shared margin with perps and spot, self-custody, small fees, crypto price ladders and 15-minute markets | Biggest long tail, social feel | Regulated, sports-heavy, Robinhood and Coinbase reach [N4] |
| Weakness | Small catalogue and liquidity, unlicensed, geo-blocked, resolution still Beta | Fees on entry, US limits | Fees, US-only |

### 8.2 Other Hyperliquid outcome venues
- Hyperliquid's own app: canonical validator-deployed markets (daily BTC, ETH, SOL, HYPE binaries, World Cup champion). [H9][T1]
- trade.xyz "Events": launched 10 Sep 2026, venue "txyz", Up/Down on stocks, commodities and pre-IPO names plus some sports; settles using its own HIP-3 perp prices. [N15]
- Skew: second permissionless deployer, stake supplied by Hyperion DeFi; about 1% of HIP-4 volume right after opening. [N11][N12]
- Stratium: another front end named at launch. [N20]
- Liquidiction and Loris: independent trackers and aggregators (not venues). [T1][T2]

### 8.3 "Outcome pays more than other venues for the same market"
- A winning share pays $1.00 on every venue. What differs is the price you paid, the fees and the spread.
- Evidence for: the team's own "Same trade. Biggest payout." graphic: $100 on DET Lions pays $322.00 on Outcome vs $311.45 and $307.70 on two unnamed venues. [C1] My arithmetic: Outcome's $322.00 implies a 31.06 cent price. Apply Polymarket's sports formula (rate 0.05) at that price and $100 buys about $311.27 of payout. Apply Kalshi's (0.07) and it is about $307.18. Those are within about 0.2% of the two quoted figures. So the gap is almost fully explained by other venues' entry fees. This is my calculation; which venues "A" and "B" are is UNVERIFIED. [N16][N17]
- That lead survives Outcome's own exit fee: at the observed 0.14% close fee, $322.00 nets about $321.55 (my arithmetic).
- Anecdotes: three user posts on 19 Jul 2026 say Outcome has no fee, better prices, tight spreads. Anecdotal: the aggregator page itself warns that many reviews and updates come from the project's own or promotional accounts. [T4]
- Evidence against a general claim: no independent like-for-like study exists; one search found no tool that shows HIP-4, Polymarket and Kalshi prices together. Prices differ by moment and market; liquidity is far thinner on Outcome, so big orders slip.
- Safe form: "Outcome has no entry fee, so more of your stake goes into the trade." Avoid "pays more", "best odds" and "biggest payout" as a general claim. If used, show the dated example with the formula assumptions and keep it as an example, not a promise.

---

## 9. What a promoter must avoid claiming

1. "Zero fees" or "free trading" with no qualifier (see 2.10).
2. "Fastest", "instant payouts", "instant settlement". Event resolution is Beta with a 4-hour target; deposits take minutes. [O5][O11]
3. "Regulated", "licensed", "CFTC approved", "legal everywhere". Outcome is run by a Panama company, blocks many countries, and no regulator has approved it. Prediction-market rules are unsettled. [O21][O26]
4. Hyperliquid and US news is not an approval. On 19 Aug 2026 Trump said the CFTC chair is working to bring Hyperliquid to the US in "fully compliant and legal fashion". That does not mean approval, and Hyperliquid is not available to US users today. [N6][N19] CME and ICE reportedly pressed the CFTC about Hyperliquid in May 2026. [N6b] Singapore's MAS listed Hyperliquid on its Investor Alert List (Hyperliquid announcement, mid-2026, date not shown). [H9, msg 564]
5. "Risk free", "guaranteed", "can't lose", "no risk because no liquidation". You can lose the whole stake. Smart contract, bridge, stablecoin, resolution and liquidity risks are all listed on Outcome's own risk page. [O21]
6. Presenting rare wins as normal. trader-J's result is 7.5 times the next best all-time (my arithmetic from [T3]). Show the date, the stake, the risk and "past results do not predict future results". Keep money shown realistic. The team's own rule is trades around $1,000 or less. [C1]
7. Fake or staged trades. Fortune reports that a June 2026 WSJ story said Polymarket hired young creators to film fake profitable trades, and that the CFTC is investigating Polymarket's social media activity. New York City Council opened an advertising probe of four prediction-market platforms on 12 Aug 2026, covering deceptive marketing, young users and compulsive wagering. [N5b] Use real positions, real events, real dates.
8. Appealing to minors. Outcome is 18+. Avoid youth-coded hooks and gambling-win imagery. Never use "bet" (the team's own rule) because the legal and platform-policy risk is higher. [C1]
9. Targeting blocked countries (section 3). Do not suggest VPN use. The Terms prohibit it. [O26]
10. Token, airdrop, points value or "early user rewards" language. Nothing is announced. [N29]
11. "Official Hyperliquid product" or implied Hyperliquid endorsement.
12. "Outcome pays more than Polymarket/Kalshi" as a general claim (see 8.3).
13. Naming real users, showing wallet addresses, or unmasking anonymous rows without the client's written permission.
14. Using the viral trader "Kimchi" (the $40M memecoin story) as if tied to Outcome. [N26]
15. "Non-custodial means safe". Non-custodial only means Outcome does not hold the funds. Resolution, bridge and smart-contract risk remain. [O21]

Platform rules (check before posting; I did not find the TikTok, Instagram or YouTube Shorts policy text):
- Google Ads allows prediction-market ads only in the US and only for CFTC-authorised exchanges (and NFA-registered brokers), after certification; effective 21 Jan 2026. Outcome would not qualify, so paid Google or YouTube ads are not an option (my inference). [N18]
- The NFL bans prediction-market ads on its broadcasts (Feb 2026 report) [N5c], and lawmakers and the New York City Council are scrutinising youth-targeted social ads for Kalshi and Polymarket. [N5b]
- Ask the client which disclosure wording they want (#ad or equivalent) in each target country.

---

## 10. Endpoints, gaps and questions for the client

### 10.1 Public endpoints (what exists and what I could read)
- No documented Outcome REST API for markets or leaderboard. https://outcome.xyz/api/ exists (robots.txt disallows crawlers) but returns 403 to my tool. [O27]
- The team saw the web app call o1.outcome.xyz/api/v1/... (markets/series, profile/lookup, portfolio/lookup). [C1] Undocumented: a plain GET on /api/v1/markets/series gives HTTP 400, and /api/v1/profile/lookup gives 405 (POST only).
- Hyperliquid info API: POST https://api.hyperliquid.xyz/info with a JSON body, types such as allMids and outcomeMeta (outcomeMeta is referenced in the HIP-4 docs). Public, no key. Needs POST, which my tool could not do. [H8][H1][H2]
- Outcome SDK @outcome.xyz/hip4 (TypeScript, beta, v1.3.0 released 5 Oct 2026, licence BUSL-1.1): events, market data, account, trading, wallet, auth modules. `outcomeRewards` reads a public unauthenticated payouts service (programme totals, wallet earnings, periods, a rewards leaderboard); limit 120 requests a minute per IP, cached 60 seconds; the base URL is not published in the docs. Source: https://github.com/Outcome-xyz/hip4 [O25][O31]
- Embeds: https://outcome.xyz/embed/{outcomeId} with options chart, grid, yaxis, activity, buy (set to 0 to hide); suggested sizes 400x400, 400x300, 340x604. [O25]
- Market URL patterns: /markets/{category}/q{questionId}?outcome={outcomeId} and /markets/{category}/o{outcomeId}; recurring series use slugs such as /markets/crypto/out-btc-15m. [O25][O1]
- Official stats dashboard: https://stats.outcome.xyz (network volume, builder share, World Cup odds, settlement data, powered by Hydromancer); JavaScript only, I got the title only. [O32]
- Easiest static source for live percentages and 24h volume: Liquidiction's market list (https://liquidiction.xyz/). Fan-built leaderboard JSON: http://dev.jbfx.me/api/leaderboard?duration=24h|all&limit=100&offset=N and /api/positions?username=... (unofficial, may disappear). [T1][T3]

### 10.2 Conflicts between sources (so you do not repeat the wrong one)
- Settlement currency: USDC now (Outcome docs, Galaxy) vs USDH in older press (The Block Feb 2026, Alea Jun 2026). Use USDC. [O3][N4][N1]
- Who deployed the May to Aug markets: Hyperliquid's validators (canonical) vs "Outcome deployed the first wave" (Crypto Briefing, 14 Jul 2026, which also says every market went through validators). Outcome's own deployer launch is 29 Aug. [N4][N9b][N11]
- Deployer stake: 1,000,000 HYPE in early reports, 500,000 HYPE in the final spec. [H9, msg 575]
- HIP-4 base fee: "currently zero" on the HIP-4 page vs fees in the dated data. [H1][T3]
- Totals: $332M, $395M, $520M, $110M. See 6.6.
- Rewards: "$200,000 a month" vs "$1M pool". Both are repeated by weak sources. [N13][N29]
- Early-2026 articles say HIP-4 requires 1M HYPE and settles in USDH; both are out of date.

### 10.3 Still UNVERIFIED
- Exact current fee rates by market, the settlement fee in each market spec, and Outcome's deployer fee scale.
- The complete current Terms jurisdiction list (read through excerpts only).
- Leaderboard fields on Outcome's own page for 7D and 30D; any official P&L share card.
- Any "Kimchi" on Outcome.
- Founders, funding, and "self-funded".
- A TikTok or YouTube channel; what the Telegram channel carries.
- The weekly $10K P&L prize, the Genesis Depositor badge, the Gate Web3 tie-up, a mobile app.
- Politics, culture and esports markets being live.
- Nothing in this file was checked on-chain.

### 10.4 Questions to put to the client
1. Which fee statement is approved: "zero fees", "no fee to open", "0% Outcome fee"?
2. Written permission to name or card users (trader-J, others), and whether anonymous rows are off limits.
3. Screenshot or link for "Kimchi".
4. Creator terms: pay, usage rights, approved claims list, disclosure wording, banned countries.
5. Official brand assets and the yellow-green and pink hex values.
6. Are the TikTok and Instagram pages we post from theirs or ours, and how should links be tagged (UTM)?
7. Is "world's fastest" a claim they can substantiate in writing?

---

## 11. Source index (URL, date)

### Outcome first-party (grade A). Docs pages are undated; fetched 13 Oct 2026.
- [O1] Home page https://outcome.xyz (13 Oct 2026)
- [O2] Docs index https://docs.outcome.xyz/llms.txt (52 pages, 13 Oct 2026)
- [O3] Introduction https://docs.outcome.xyz/introduction.md
- [O4] Wallets and accounts https://docs.outcome.xyz/wallets-and-accounts.md
- [O5] Funding https://docs.outcome.xyz/funding-your-account.md
- [O6] First trade https://docs.outcome.xyz/placing-your-first-trade.md
- [O7] Outcome and Hyperliquid https://docs.outcome.xyz/outcome-and-hyperliquid.md
- [O8] Deployer architecture https://docs.outcome.xyz/outcome-architecture.md (also https://docs.outcome.xyz)
- [O9] Market types https://docs.outcome.xyz/market-types.md
- [O10] Recurring markets https://docs.outcome.xyz/recurring-markets.md
- [O11] Resolution https://docs.outcome.xyz/resolution.md
- [O12] Resolution and settlement https://docs.outcome.xyz/resolution-and-settlement.md
- [O13] Real world events https://docs.outcome.xyz/real-world-events.md
- [O14] Fees https://docs.outcome.xyz/fees.md
- [O15] Withdrawing https://docs.outcome.xyz/withdrawing-funds.md
- [O16] Fee discount https://docs.outcome.xyz/trading-fee-discount.md
- [O17] Builder codes https://docs.outcome.xyz/builder-codes.md
- [O18] Badges and cards https://docs.outcome.xyz/badges-and-cards.md
- [O19] Leaderboard https://docs.outcome.xyz/leaderboard.md
- [O20] Liquidity rewards https://docs.outcome.xyz/outcome-liquidity-rewards.md
- [O21] Risks https://docs.outcome.xyz/risks.md
- [O22] Support https://docs.outcome.xyz/support.md
- [O23] Order lifecycle https://docs.outcome.xyz/order-lifecycle.md
- [O24] How prediction markets work; tokens and pricing https://docs.outcome.xyz/how-prediction-markets-work.md ; https://docs.outcome.xyz/outcome-tokens-and-pricing.md
- [O25] SDK pages: https://docs.outcome.xyz/sdk/introduction.md ; /sdk/guides/recipes/embedded-markets.md ; /sdk/guides/recipes/showcase-markets-code.md ; /sdk/reference/events-adapter.md ; /sdk/reference/market-data-adapter.md ; /sdk/guides/trading.md ; /sdk/reference/outcome-rewards.md ; /sdk/changelog.md (v1.3.0, 5 Oct 2026)
- [O26] Terms of Service https://outcome.xyz/terms (direct fetch 403; text via search excerpts, 13 Oct 2026)
- [O27] Site files: https://outcome.xyz/robots.txt ; /sitemap.xml (213 URLs, lastmod 12 Oct 2026) ; /manifest.webmanifest ; /icon.svg ; /lockup-dark-gray.svg (13 Oct 2026)
- [O28] Discord invite API https://discord.com/api/v10/invites/outcome?with_counts=true (13 Oct 2026)
- [O29] Instagram https://www.instagram.com/outcomexyz/ (13 Oct 2026)
- [O30] Short links https://go.outcome.xyz/ig and /tg (13 Oct 2026)
- [O31] GitHub https://github.com/Outcome-xyz and https://github.com/Outcome-xyz/hip4 (13 Oct 2026)
- [O32] Stats site https://stats.outcome.xyz/ (title only, 13 Oct 2026)

### Hyperliquid first-party (grade A)
- [H1] HIP-4 page https://hyperliquid.gitbook.io/hyperliquid-docs/hyperliquid-improvement-proposals-hips/hip-4-outcome-markets (read 13 Oct 2026, undated)
- [H2] HIP-4 deployer actions https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/hip-4-deployer-actions.md (13 Oct 2026)
- [H3] Fees https://hyperliquid.gitbook.io/hyperliquid-docs/trading/fees (13 Oct 2026)
- [H4] HyperCore overview https://hyperliquid.gitbook.io/hyperliquid-docs/hypercore/overview (13 Oct 2026)
- [H5] Docs home https://hyperliquid.gitbook.io/hyperliquid-docs (13 Oct 2026)
- [H6] Referrals https://hyperliquid.gitbook.io/hyperliquid-docs/referrals (13 Oct 2026)
- [H7] Builder codes https://hyperliquid.gitbook.io/hyperliquid-docs/trading/builder-codes (13 Oct 2026): user approves a maximum builder fee; caps stated for perps (0.1%) and spot (1%), outcomes not stated
- [H8] Info endpoint https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/info-endpoint (13 Oct 2026)
- [H9] Announcements channel https://t.me/s/hyperliquid_announcements (messages 560 to 595; only times shown, not dates; msg 580 dated 14 Aug 2026 by one secondary source; msg 585 is the week of 24 to 29 Aug 2026)

### Press and research (grade B unless noted)
- [N1] The Block, 2 Feb 2026, https://theblock.co/post/388023/hyperliquid-outcome-prediction-markets-limited-risk-options-trading
- [N4] Galaxy Research, 9 Jun 2026, https://www.galaxy.com/insights/research/hyperliquid-hip-4-prediction-markets-polymarket-kalshi-analysis
- [N5] bitcoin.com, 2 May 2026, https://news.bitcoin.com/hyperliquid-launches-hip-4-and-targets-polymarket-with-zero-fee-outcome-markets/
- [N5b] Fortune, 12 Aug 2026, https://fortune.com/2026/08/12/kalshi-polymarket-nyc-probe/
- [N5c] Tubefilter, 3 Feb 2026, https://www.tubefilter.com/2026/02/03/prediction-market-ads-kalshi-polymarket-super-bowl/ (seen in search results only)
- [N6] CoinDesk, 19 Aug 2026, https://www.coindesk.com/markets/2026/08/19/hype-jumps-11-as-trump-says-cftc-is-working-to-bring-hyperliquid-to-u-s
- [N6b] The Block, 15 May 2026, https://www.theblock.co/news/regulation/2026-05-15-hyperliquid-onchain-perps-offer-efficiency-transparency-ice-cme-cftc-oversight-401512 (seen in search results only)
- [N7] The Block, 26 May 2026, https://www.theblock.co/post/402511/hyperliquid-validator-prediction-markets
- [N8] The Block, 20 Jul 2026, https://www.theblock.co/post/408875/hyperliquid-hip-4-permissionless-deployment
- [N9] Crypto Briefing, 28 Jun 2026, https://cryptobriefing.com/hip-4-open-interest-ath-world-cup/ ; Value The Markets, 28 Jun 2026, https://www.valuethemarkets.com/cryptocurrency/news/hyperliquids-hip-4-sees-unprecedented-growth-driven-by-world-cup-prediction-markets
- [N9b] Crypto Briefing, 14 Jul 2026, https://cryptobriefing.com/outcome-xyz-permissionless-prediction-markets-hyperliquid/
- [N10] Privy blog, 18 May 2026, https://privy.io/blog/from-perps-to-prediction-markets-understanding-hip-4-and-hyperliquid-next-phase
- [N11] KuCoin News (repost of Odaily), 31 Aug 2026, https://www.kucoin.com/news/flash/hyperliquid-hip-4-deployment-begins-outcome-becomes-first-builder
- [N12] crypto.news, 3 Sep 2026, https://crypto.news/hyperliquid-hip-4-volume-triples-after-open-rollout/
- [N13] MEXC News, 4 Sep 2026, https://www.mexc.co/news/1206539 (grade C)
- [N14] The Merkle, 25 Sep 2026, https://themerkle.com/hyperliquids-outcome-markets-are-compounding-fast-hip-4-volume-tops-350-million (grade C); Crypto Economy, 29 Sep 2026, https://crypto-economy.com/?p=336006 (weekly volumes, Artemis data)
- [N15] Bankless, 10 Sep 2026, https://www.bankless.com/read/news/trade-xyz-launches-hip-4-event-markets
- [N16] Polymarket fee docs https://docs.polymarket.com/trading/fees (read 13 Oct 2026)
- [N17] Kalshi fee schedule https://kalshi.com/docs/kalshi-fee-schedule.pdf (via search excerpt, 13 Oct 2026)
- [N18] Google Ads policy update https://support.google.com/adspolicy/answer/16749907?hl=en (announced 5 Jan 2026, effective 21 Jan 2026)
- [N19] Chainstack, 4 May 2026, https://chainstack.com/hyperliquid-hip4-vs-polymarket-2026/ (grade C); Chainstack testnet trading doc https://docs.chainstack.com/docs/hyperliquid-hip4-outcome-markets-trading (grade C)
- [N20] Forklog, 2 May 2026 (search result only) https://forklog.com/en/hyperliquid-launches-prediction-markets/
- [N21] CoinCodeCap, 2 Sep 2026 (updated 30 Sep), https://coincodecap.com/outcome-xyz-review (grade C)
- [N22] Quicknode World Cup page, undated (written after the tournament), https://www.quicknode.com/world-cup (grade C; vendor-compiled; counts both books of each team market)
- [N23] Official 0.2 s figure is [H4]; the 0.07 s and "tens of milliseconds" figures were seen in QuillAudits and Eco pages via search (grade C, ignored)
- [N24] defirate.com World Cup recap, July to Oct 2026, https://defirate.com/prediction-markets/world-cup-odds/ (final: Spain 1-0 Argentina, 19 Jul 2026)
- [N26] Kimchi (@kimchi1x) coverage, 30 to 31 Jul 2026, via HTX news https://www.htx.com/news/he-made-40-million-from-trump-coin-and-is-in-the-spotlight-a-287nR429/ (grade C; seen in search results only; the $40M figure is disputed)
- [N27] Hyperliquid India Substack, 5 May 2026, https://hyperliquidindia.substack.com/p/hip-4-outcome-go-mainnet (grade C)
- [N28] KuCoin News (Thriggar post), 11 Oct 2026, https://www.kucoin.com/news/insight/HIP/6acb0a3944c213000789203c (grade C)
- [N29] usethebitcoin.com Outcome guide, 1 Sep 2026, https://usethebitcoin.com/airdrop/outcome-airdrop-guide/ (grade C, affiliate-style); [N30] airdrops.io, updated 31 Aug 2026, https://airdrops.io/outcome/ (grade C)
- [N31] Phemex, early 2026 (undated in my view), https://phemex.com/news/article/outcome-launches-leveraged-prediction-markets-on-hyperliquid-testnet-57415 (grade D: direct fetch failed; read only through a search summary)

### Trackers, fan tools, aggregators (grade C or D)
- [T1] Liquidiction: stats https://liquidiction.xyz/hip4/stats (snapshot 12 Oct 2026 22:59 UTC); market list https://liquidiction.xyz/ (13 Oct 2026); leaderboard https://liquidiction.xyz/leaderboard (did not render)
- [T2] Loris Tools Outcome.xyz leaderboard https://loris.tools/hip4/leaderboard/outcomexyz (snapshot 12 Oct 2026 20:04 UTC); https://loris.tools/hip4
- [T3] Fan-built Outcome leaderboard and card maker http://dev.jbfx.me/leaderboard ; JSON read 13 Oct 2026: /api/leaderboard?duration=all (updated 12 Oct 2026 00:41 UTC) and duration=24h (updated 12 Oct 2026 23:31 UTC), /api/trader?username=trader-J, /api/positions?username=trader-J | trader-W | trader-Z | trader-D (timestamps converted by me)
- [T4] Polymart aggregator page https://polymart.app/outcome-xyz (read 13 Oct 2026; relays Outcome's X posts of 8 to 11 Oct 2026, X follower snapshot, user reviews of 19 Jul 2026)
- [D] X posts seen only through search summaries (X blocked for my tool), dated by decoding the post ID: Outcome, 7 Jul 2026 (https://x.com/Outcomexyz/status/2074541629332181279); Outcome, 4 Nov 2025 (https://x.com/Outcomexyz/status/1985693547606262134); launch-day congratulation, 2 May 2026 (https://x.com/Onoja_Cee/status/2050546971006652695); Hyperliquid Hub, 30 Apr 2026 (https://x.com/Hyperliquid_Hub/status/2049700166647853072); Arrakis Finance article, 21 May 2026 (https://x.com/ArrakisFinance/article/2057491856938946940); the "$238,071 paid out" post of 30 Sep 2026 (seen in a search summary, post URL not captured)

### Client files
- [C1] C:\VISION\VISION CLAUDE\outcome\research\00-client-brief.md (13 Oct 2026)
