# Outcome: client brief digest (read 13 Oct 2026)

Sources: `C:\VISION\OUTCOME\Faceless-Formats.pdf` (4 formats), `C:\VISION\OUTCOME\Outcome Formats.pdf` (UGC formats, talking head), the linked "Outcome Creator Guide" Google Doc, the Drive examples, outcome.xyz and the P&L card maker. Checked live in the built-in browser.

## What Outcome is (seen on the site, 13 Oct 2026)
- outcome.xyz: prediction market "on Hyperliquid". Yes/No (or team A / team B / draw) markets. Prices shown as payout multipliers and "$100 -> $375" lines, plus % chances.
- Tabs: All, Sports, Crypto, Economics, Finance, Esports. Bottom bar: Home, BTC 15m, Activity, Profile. Sign-in via Google, email, X, wallets (Privy).
- Market types live today: 15-minute and daily Up/Down on BTC, ETH, SOL, HYPE, gold, silver, WTI oil, S&P 500, US100, MU, SPCX; "BTC touches X by end of October"; football (UCL matches, EPL winner, UCL winner, Ballon d'Or), NFL games + Super Bowl winner, NBA winner, Fed decision, "Anthropic first-day market cap". Biggest volumes: UCL winner $2.4M, EPL winner $2.2M, NFL winner $2M.
- "Daily Rewards / TRADE TO EARN / $1,000,000 rewards program" banner (gold ticket); "$340,096 / $1M have been rewarded".
- Leaderboard: outcome.xyz/leaderboard (Today / 7D / 30D / All, sort by P&L, 46 pages). Profiles: outcome.xyz/profile/<name> show outcomes traded, win rate, wins/losses, P&L chart (1D/7D/30D/ALL), portfolio, volume, Hall of Fame badges, past-days P&L, open positions (shares, side, entry and mark price, PnL), open orders, history.
- Look: near-black UI, white Inter-style type, lightning-bolt logo, accents hot pink and neon yellow-green, gold rewards ticket.

## Data we can automate from
- P&L card maker http://dev.jbfx.me/leaderboard (fan-built, "Outcome Leaderboard & PnL Share Cards"): Top traders / Top trades, Daily / Weekly / 30 days / All time, 1000 traders ranked. Per trader: joined date, realised PnL, positions, win rate, staked, earned. "Card" on any resolved trade renders a share PNG (themes Auto, World Cup, Default, Hype, BTC).
  JSON behind it: `/api/leaderboard?duration=24h|all&limit=50`, `/api/trader?username=`, `/api/positions?username=&window=all&include=all`, `/api/card?coin=...&username=...&style=...` (PNG).
- outcome.xyz itself calls `o1.outcome.xyz/api/v1/...` (markets/series, profile/lookup, portfolio/lookup) and the public Hyperliquid API (`api.hyperliquid.xyz/info`), so trades are on-chain and public.
- All-time #1 (13 Oct): trader-J, +$503,008 realised from 2 trades (2026 World Cup Champion: SPAIN +$341,892, ARGENTINA NO +$161,116, settled 20 Jul 2026, staked $760,765). Card shows 856,418 shares at 60.08c, bought $514,526, to win $856,418.

## Rules in every brief
- Say the plug (or close to it): "On outcome.xyz, the world's FASTEST prediction market, traders predict ___ will happen with a __% chance."
- Faceless CTA line: "Trade with zero fees on Outcome.xyz".
- Never cover the graph, the lines, the names or the Outcome logo (or the buy buttons).
- Never say "bet", "betting", "I'm putting my money / house on this". Never guarantee or exaggerate profits. Finance: say it is not financial advice, do your own research. Politics: deliver the news, no personal opinions.
- Demo format: money shown must be realistic (under $10k title, trade around $1,000 or less) and the real event must be shown, "to not be deceptive".
- Creator Guide: about 1 minute long (finance 40 s to 1 min), no repeated facts, hook = hot take / shock / bold question ("Will I stop scrolling?"), plug at 50 to 70% of the video (finance can plug at the end), plug lasts 8 to 10 s, good music (named: Yvesnord, Mozart Requiem Lacrimosa, Lucifer Waltz, "Just Asking at night"; wheel format: "Last Surprise").

## The 4 faceless formats (the job)
| # | Format | Shape | Inputs | Example seen |
|---|---|---|---|---|
| 1 | How-to tutorial | 5-slide carousel: hook, find a market, make the prediction, payout, CTA | Outcome UI screenshots, a market, payout | Slides = real app screenshots + TikTok white text boxes, arrows, circles, emoji. "How to turn your predictions into profit on Outcome.xyz" over the $503k P&L chart; "Find a market you have an edge on"; "Think it's gonna happen? Buy YES / Think it won't? Buy NO"; $500 -> payout $26,737 circled "BE RIGHT -> PROFIT"; "Ready to make your call? Trade with zero fees on outcome.xyz" |
| 2 | P&L card edit | Short video | Trader, P&L card, market, category | P&L card (background removed) over a film-scene edit; card shows "You predicted NO, SKHX above 1,180.7 ... $0.20 -> $1.00, bought $4,780, earned $24,000, Outcome / OXVELKA". "Trade with zero fees on Outcome.xyz" at the bottom. Ref TikTok @jackpot_0_ |
| 3 | Top 3 traders | 5-slide carousel: hook, #3, #2, #1, CTA | Leaderboard, 3 profiles, big wins | Slide 1 = Wolf of Wall Street still + "TOP 3 TRADERS ON Outcome IN THE LAST 24 HOURS" (green accents). Slides 2 to 4 = big 3D number (pink 3, silver 2, gold 1) over the trader's profile banner + P&L chart. CTA "Think you can make the list?" Ref TikTok @cryptodailyfeed |
| 4 | Trader story | 4-slide carousel: hook, the trades, what happened, CTA | Leaderboard trader, total profit, the event, trades, match stats | "How [user] made $5K trading Portugal vs Wales"; CTA "Think you can spot the next one?" Example folder "worldcup trade story" needs a Google sign-in (not shared publicly) |

## UGC formats that could run faceless
From the UGC doc (talking head by default): Demo format (no talking: "How to make $_k in _ minutes with Gemini + Outcome.xyz", text steps on screen), Sankey "I DM'd every top trader" (SankeyMATIC diagram + AI-written reply), Insane trader headline (screen recording of the trader's orders + voiceover), Clueless bait (payout comparison, other venues renamed "Venue A/B"; the PDF image is an Outcome graphic "Same trade. Biggest payout." $100 on DET Lions: Outcome $322.00 vs $311.45 / $307.70), Rankings, Guess the player/stock, Informative finance (headline + numbers), Spin the wheel series.
Face-only (skip for faceless): post/pre-match commentary, transfer news reactions, clip reactions, street interviews.
