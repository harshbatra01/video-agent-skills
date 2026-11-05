# 17 Original ideas bank (13 Oct 2026, my own brainstorm before the agent reports)

What only Outcome has, and every idea below leans on:
1. A live % chance with real money behind it ("the money says"). Fans disagree with it, so it starts arguments with a REAL number (Jaden's bar: polarising, never invented).
2. A chart that jumps when a goal, red card or headline lands. The line is a story with a beginning, a twist and an end.
3. A public leaderboard of real characters: wins, losses, streaks, mystery whales.
4. Every market ends with a definite answer, so a post can be followed by a "callback" post. That builds series and follows.
5. 96 BTC 15-minute markets a day: constant micro drama.
6. Odd markets people are curious about (Anthropic IPO size, Fed hike chance, oil at $100).

Live numbers seen on 13 Oct 2026 (use as mock data; refresh before posting): Ballon d'Or Kane 66%, Yamal 29%, Messi 4%, Haaland 1%. EPL winner Arsenal 60%, City 20%, Chelsea 8%, Liverpool 6%, Spurs 3%, Man Utd 2%. UCL winner Barcelona 23%, Bayern 14%, PSG 13%, Arsenal 13%, Real Madrid 11%. Fed October: no change 81%, increase 18%. Anthropic first-day value above $2T: 58% (x1.72). BTC touches 90K by end of October: 29%. Tonight's UCL: Viking 4% vs Bayern 90%, Galatasaray 10% vs Barcelona 77%, Lille 6% vs Arsenal 80%, Brugge 8% vs Inter 78%, Atletico 51% vs Man Utd 25%.

## A. Football and NFL (biggest audience, most argument)
| # | Name | Shape | The idea | Example with real data | Automation |
|---|---|---|---|---|---|
| A1 | The Money Says | 5-slide carousel | Hot take hook carried by a real %, both sides argued, chart of how it got there, "Do you agree with the money?" | "Traders give Harry Kane a 66% chance of the Ballon d'Or. Lamine Yamal: 29%." | High (market % + chart from API; 2 stat lines per side need a stats source or a quick human check) |
| A2 | Match in 10 Seconds | 9:16 video, 8 to 12 s, loops | A whole match told only by its market line, sped up, goal markers pop on the line, giant % counter ticks | "Atletico vs Man Utd, as told by the money" | High if market candles are available (agent 15 checks) + scores API |
| A3 | The Swing | 9:16 video | One moment that flipped a market: score graphic or clip on top, the chart cliff below, counter "77% -> 12% in 9 minutes" | Any late goal tonight | High (same data as A2) |
| A4 | The 4% Club | carousel or video series | Longshots that actually happened: "The market gave this a 4% chance. It happened." Shows a 4c share paying $1 (mechanics, not a promise) | If Viking beat Bayern tonight | High (detector: winner priced under 15%) |
| A5 | Upset Radar + Callback | pre-match card, then a result post | Before: "3 upsets the market thinks could happen tonight." After: "Upset Radar: 1 of 3 hit." Builds a running record | Viking 4%, Galatasaray 10%, Lille 6% | High |
| A6 | Price Tags (rival banter) | single card or carousel | "What it costs to believe": "Believing Man Utd win the league costs 2c. Spurs: 3c." Rival fans send it to each other | EPL winner list | Very high (one market) |
| A7 | Pundit Receipts | carousel | Real pundit quote vs the market: "He says Liverpool win the league. The money says 6%." Callback when it settles | Needs a sourced quote | Medium (quote found by hand or news search) |
| A8 | Crowd vs Supercomputer | carousel | Opta's published numbers next to Outcome's: "Opta: 45%. The money: 60%. Who's right?" Weekly | Needs Opta's latest article | Medium |
| A9 | Title Race Tracker | weekly video (line or bar race) | Every week the EPL/UCL/Ballon d'Or % lines move; season-long series people follow | Arsenal 60% today | High once history is stored daily |
| A10 | Sliding Doors | video | One miss or red card that changed a season: "Before this miss: 40%. After: 20%." | Needs a big moment | Medium |
| A11 | Last-Minute Heartbreak | video | Markets that went from 95% to zero after the 85th minute | Late winners | High |
| A12 | Guess the Match From the Chart | carousel quiz | Slide 1 shows only a chart line with wild swings; clues on slides 2 to 4; answer last | Any crazy game | High |
| A13 | Trader Team of the Week | carousel | FIFA Ultimate Team-style cards for the week's best traders (rating = win rate, stats = P&L, volume, "specialty: football"). Football fans already love TOTW | jbfx leaderboard | High (needs the OK on usernames) |
| A14 | Your Club, Ranked by Money | carousel tier list | Every UCL club by real %: S tier to "no chance". Ego and identity, everyone checks their club | UCL winner market | Very high |
| A15 | Matchday Board | single card per night | Clean grid of tonight's games with home/draw/away %, the night's "biggest favourite" and "best upset shot" | Tonight's 18 UCL games | Very high |

## B. Crypto, markets and news
| # | Name | Shape | The idea | Example | Automation |
|---|---|---|---|---|---|
| B1 | 15-Minute Thriller | 9:16 video, 15 to 25 s | The last minutes of a BTC 15-minute market: BTC price vs the target line, UP/DOWN chance flipping, countdown clock, ends on RESOLVED. Pick the day's most dramatic flip | "90% DOWN with 60 seconds left" | High (BTC candles + market history) |
| B2 | The Number | single bold card, daily series | One giant number and one line: "81%: the chance traders give the Fed holding rates this month." Newsy, brandable, fast | Fed 81% / 18% hike | Very high |
| B3 | Market Movers | weekly carousel | The biggest % moves of the week across all markets, one slide each with a mini chart | Any week | Very high |
| B4 | IPO Watch | carousel or card | "Traders think Anthropic is worth more than $2T on day one (58%)." Ladder of the value bands as a chart | Anthropic bands 80/74/58/37/26% | Very high |
| B5 | Where the Money Is Going | daily card | Today's top markets by volume: "Tonight's biggest market: Rams vs Bills, $530K traded" | Home page volumes | Very high |
| B6 | Price Ladder | carousel | "Where will BTC be on 31 Oct? The crowd's map": every target band with its %, drawn as a ladder | BTC touches 75K/80K/87.5K/90K/92.5K | Very high |
| B7 | Headline vs Market | card | A real breaking headline, then what the market did in the next hour | Oil, Fed, tariffs | Medium (needs a headline feed) |

## C. Traders and lore (the client's favourite area, needs the username OK)
| # | Name | Shape | The idea | Automation |
|---|---|---|---|---|
| C1 | Who Is trader-J? | 4 to 6 slide mystery carousel or video | The single best story Outcome has: joined 18 Jul 2026, two trades, $760,765 in, $503,008 out, 7.5x the next trader. Mystery framing ("one account, two trades, then silence") | Manual once, evergreen |
| C2 | Same Money, Different Call | carousel | Two traders on opposite sides of the same market; one right, one wrong. Suspense on slide 3 | High (positions data) |
| C3 | Worst Trade of the Week | carousel | An honest loss story: "Bought Bayern at 90c. Viking scored in the 89th." Relatable, funny, and the opposite of a profit promise | High |
| C4 | Streak Watch | card series | The trader with the longest current win streak; follow them all week | Medium (needs streak math from positions) |
| C5 | P&L Card Edit, smarter | 9:16 video | The client's format, but the edit behind the card matches the market (Spain highlights behind a Spain card), not cash piles | Medium (card PNG automatic, edit footage picked per market) |

## D. Engagement mechanics (borrowed, made Outcome-only)
| # | Name | Shape | The idea | Automation |
|---|---|---|---|---|
| D1 | Guess the % | carousel quiz | "Guess what traders give these (answers on the last slide)": 4 markets, reveal at the end. Swipe-through plus "I got 3 of 4" comments | Very high |
| D2 | Higher or Lower | 9:16 video | The Higher or Lower game with markets: "Is Arsenal winning the league MORE or LESS likely than Kane winning the Ballon d'Or?" 3 s timer, reveal | Very high |
| D3 | AI vs the Market | daily pair of posts, season series | The same games picked by an AI model and by the market; next day a running scoreboard ("AI 11/20, Market 14/20"). Nobody else can run this one without the data | High |
| D4 | Story Poll vs Market | IG Story poll, then a post | Poll our followers, then post "62% of our followers say yes. Traders say 60%." (real poll, real market) | Medium (poll is manual in-app) |
| D5 | Comment a Market | reply-to-comment videos | "Comment any match and we'll show you what the money says" then reply videos with the card | Medium |
| D6 | POV Chart Memes | single image or 5 s clip | "POV: you bought Bayern at 90c and Viking score in the 89th" with the real chart cliff | High (chart auto, joke by hand) |

## E. The client's 4 formats, made automatic
- How-to carousel: capture fresh UI screenshots of a live market with headless Chrome (mobile size), place the white text boxes, arrows and circles from a template.
- P&L card edit: card PNG from the card maker; background edit chosen per market category (see C5).
- Top 3 traders in 24h: leaderboard JSON, then either live profile screenshots or our own profile cards in Outcome's style, big 3D numbers 3 / 2 / 1, CTA slide.
- Trader story: trader + trades from positions JSON, match facts from a scores API, chart from market history.

## Ground rules for every idea
Real numbers with a date, the chart and logo never covered, no "bet", no cash piles or win-celebration visuals, no "$100 -> $10,000" bragging (x100 payouts look like get-rich-quick), a risk line in captions, losses shown as honestly as wins.
