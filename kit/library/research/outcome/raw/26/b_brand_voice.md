# Outcome (outcome.xyz): own voice, posts and look
Research 26 / b, written 14 Oct 2026. X counts cover 15 Sep to 13 Oct 2026 (29 days). UNVERIFIED marks anything I could not confirm. Emoji are named, not pasted.
Files: images `raw\26\brand\media\` (57, all checked as real JPEGs), sheet `raw\26\sheets\30_outcome_own_posts.jpg` (57 tiles), data `raw\26\brand\` (X timeline jsonl, app UI strings json, other channels json), brand guide copies `raw\26\brand\pages\` (DESIGN.md byte for byte, one .md per guide page, README with provenance).

## 0. Short version
1. Biggest find: Outcome runs an official PUBLIC brand guide, press kit link and AI-ready DESIGN.md at https://brand.outcome.xyz/ . It fixes voice, banned words, fonts, colours, canvas sizes (section 1). Section 7.3 of `01-what-is-outcome.md` says no press kit was found; that is now out of date.
2. Official voice is "quietly forceful": short declarative lines, no hedging, no exclamation marks, never bet / wager / gambling / punt. The X account matches: 0 uses of bet, 2 exclamation marks in 115 posts, emoji in 9 of 151.
3. Real X voice is a news-desk headline plus a market number. BREAKING or JUST IN opens 46% of posts, half carry a $ figure, 17% state a chance or odds. Caps on 26%. One sentence per line, median 24 words.
4. Signature lines: "Trade the outcome." (call to action, posted as a self-reply with a market link under news posts), "The outcome is inevitable", "On Outcome, you trade the game", "Outcome settled. Traders paid."
5. Look is two systems. App: near-black, mint Up/Yes and coral Down/No buttons. Social: loud flat colour fields, PP Neue Corp Narrow Ultrabold caps, oil-painted cut-outs, one-colour logo lockup. The cyan/magenta mark appears in 0 of 57 images.
6. Best performers: traction milestones and launches, mostly video (226K, 210K, 96K views). Sports previews are weakest (median 1.5K views).

## 1. Official brand guide (new)
- Site: https://brand.outcome.xyz/ ("Outcome Brand Tool"). Its "Public" block offers Brand Guide (logos, palette, type), "Open press kit", "Download all assets". A "Partnerships / KOLs" block offers a co-marketing kit (social tiles, co-branded lockups, AMA and Spaces art, asset pack, templates, web assets). Contact hello@outcome.xyz, buttons Press enquiry, Partnership enquiry, Request portal access.
- I read the guide pages and https://brand.outcome.xyz/DESIGN.md (15 KB markdown, its stated use is "paste into any LLM") as text only. I did not log in, ask for access or download the asset packs. Partner/KOL pages show nothing without portal access, so any KOL terms or disclosure rules are UNVERIFIED.
- **Voice (paraphrased):** states, does not pitch; confidence earned; short declarative English; if a line needs a qualifier, cut it. Tone by context: product UI minimal and functional; social/community sharp, direct, sometimes provocative, "a member of the community, not a brand account"; marketing confident, cinematic, big claims backed by real numbers; docs clear and precise. Character: "Reliable Rebels", Sage plus Outlaw, adjectives innovative, transparent, high-conviction. Metaphor: Outcome is the race car, the trader is the driver.
- **Never use:** bet, wager, wagering, gambling, punt, game-changing, VCs, discounts, payout percentages. **Avoid:** stacks, casino-adjacent framing, hedges (we believe, we think, perhaps, maybe, hopefully), slang without purpose, exclamation marks, hype words, over-explaining. Frame markets as skill and signal. Model lines in the guide: "You saw it. You acted. You were right." and "One market, built by its community."
- **Look rules:** one idea per frame; headline fills about half the canvas, PP Neue Corp Narrow Ultrabold, always caps; body PP Neue Corp Normal Medium; no drop shadows or outlines on type. Every photo gets an oil-painting treatment, used full-bleed or as a cut-out cropped on one or two edges; no stock photos, no external AI filters, no gradient over photos. Nine-region placement grid; logo and body copy sit in corners opposite the headline; layer order background, texture, image, headline, body, logo, footer. Textures by group: canvas (Main), spray (Culture), halftone (Business). Icons: Phosphor, no emoji on buttons.
- **Canvas presets:** IG post 1080x1080; IG Story and TikTok 608x1080; IG landscape 1080x566; X post 1080x608; X header 1080x360.
- **Palette (hex from DESIGN.md):** Signal Green #1AFF57, Deep Forest #055D1C, Violet Ultra #8952EE, Twilight Indigo #240F4C, Near-black #171717, Off-white #F5F5F5; Culture: High-Vis Yellow #E6FF2F, Rally Orange #FF8825, Protest Pink #FF9DBE; Business: Executive Teal #04AC7D, Protocol Blue #03379D, Alert Red #FD6C6B. Ten themes, any theme on any graphic. This is the marketing palette; the app UI uses the different `--oc-*` tokens in brand.json.
- **Also in the guide:** logo is the icon mark or the wordmark only, never rebuilt, gradient-filled or traced; imagery is high-contrast, oil-painted, shot wide. Brand-character "don'ts": gambling-coded or casino-adjacent, generic or flashy, celebrating disruption without an alternative. The guide contradicts itself on colour: the Design Language page says four hues (green, fuchsia, turquoise, neutral), the Color System page nine palettes and eight themes, DESIGN.md ten themes. Use DESIGN.md.
- **Claims in the guide not to reuse without client sign-off:** "faster than any competitor", "60x lower fees than Polymarket", "$20M staked", "200K+ testnet users". UNVERIFIED, and the app FAQ gives a 500K HYPE bond worth about $40M, so the numbers disagree.

## 2. Tone of voice and vocabulary
### 2.1 Where the words came from
| Channel | How read | Voice in one line |
|---|---|---|
| X @Outcomexyz (27,030 followers, joined 4 Dec 2024) | FxTwitter JSON, 160 timeline items (151 own, 9 reposts) | news-desk headline plus a number; caps for big moments; dry jokes; almost no emoji |
| X @OutcomeSports (539 followers, joined 27 Aug 2026) | FxTwitter, 20 posts | calm football/NFL previews that end in a question; "Don't just watch. Trade the outcome." |
| Telegram announcements | public preview t.me/s/Announcement_Outcome, 19 posts 18 Jun to 29 Sep | launch hype: caps lines, "Tap in", "Just use Outcome", racing-car emoji as a bullet |
| Instagram @outcomexyz (48 followers, 9 posts) | embed pages, 6 readable (7 to 13 Oct) | plain finance explainer, 3 to 4 hashtags, a not-advice disclaimer, "link in bio" |
| Discord (6,503 members, 385 online) | public invite JSON | description: Prediction Markets on Hyperliquid, Trade outcomes on crypto and more soon (older than the X bio) |
| App UI | message dictionary inside the page payload, about 1,340 strings | labels are minimal; achievement cards are jokey crypto slang |
| Docs, blog | docs.outcome.xyz (18 pages), blog.outcome.xyz (one post, 7 Jul 2026) | plain second-person explainer; "defined risk", "asymmetric upside", "2.5x on $0.40" |

### 2.2 Tone verdict
- Crypto-native news desk with a cheeky edge. Not formal, not meme-heavy. Hype comes from capital letters and slogan fragments, not emoji or exclamation marks.
- Sporty only in previews (short facts, then a question). Provocative in small doses (a joke about conferences, "Hype bears in disbelief").
- Crypto slang is light: GM, Gmeow, predictoor, Uptober, "WE ARE SO BACK", cashtags ($HYPE, $BTC in 21 of 151 posts), HIP-4. 10 of 115 main posts close with the single word "Hyperliquid".
- App achievement cards go further (degen, FOMO, airdrop, "huge balls", "lost real sleep over fake money") but that is product copy, not X.

### 2.3 Word counts (115 main posts = 83 originals + 32 quote posts; 36 self-replies counted apart)
- Action: trade/traded/trading 28 posts (24%), trader(s) 12 (10%), predict(s/ed) 7 (6%), prediction(s) 5 (4%), predictoor 1, call 1. bet/betting 0, degen 0, LFG 0.
- Market: market(s) 28 (24%), volume 17 (15%), price 19 (17%), chance 14 (12%), odds 12 (10%), touch 13 (11%), probability 0.
- Result and money: win/won/winner 9 (8%), rewards 4, earn 4, payout 3, paid/pays 3.
- Brand: "outcome(s)" in any sense 54 (47%, brand name plus generic), inevitable 4, "trade the game" 1, GM or Gmeow 4 (3%), "on Outcome" 15.
- Openers: BREAKING 31 (27%) and JUST IN 23 (20%), together 53 of 115 (46%).
- Self-replies (36): trade 28 (78%), outcome 31 (86%): the fixed line "Trade the outcome." plus a market link (16 times word for word).
- Telegram (19 posts): trade 11, outcome 18, market 7, rewards 6, predict 5, trader 4, win 4, paid/payout 4, inevitable 4, odds 3, earn 3; bet, degen, GM, LFG 0; no exclamation marks; racing-car emoji in 16 of 19 posts as the marker before the call-to-action line. Instagram (6 captions): trade 3, market 4, outcome 5, odds 3, trader 2; predict, bet, win 0; about 3 hashtags per post; not-advice disclaimer in 5 of 6.
- Style: all-caps 30 posts (26%), sentence case 80 (70%), mixed 5. Emoji in 9 of 151 posts: siren, red circle (as a BREAKING marker), check marks in one list, football, American football, pointing hand, Singapore flag, salute face. Hashtags 0 (two hits are "#1"). Exclamation marks 2. Ends in a question 17. $ figure in 57 (50%), % figure 32 (28%), stated chance or odds 20 (17%).

### 2.4 Example lines (all under 15 words)
| # | Line | Where, date | Link |
|---|---|---|---|
| 1 | On Outcome, you trade the game. | X, 8 Oct 2026 | https://x.com/Outcomexyz/status/2108260638695010410 |
| 2 | THE OUTCOME IS INEVITABLE. | X, 5 Oct 2026 | https://x.com/Outcomexyz/status/2107064046944219365 |
| 3 | Trade the outcome. | X reply, 10 Oct 2026 | https://x.com/Outcomexyz/status/2108905495612555557 |
| 4 | Outcome settled. Traders paid. | X, 10 Oct 2026 | https://x.com/Outcomexyz/status/2108905483268657156 |
| 5 | WE DEPLOYED. YOU TRADED. | X, 29 Sep 2026 | https://x.com/Outcomexyz/status/2104933457285742990 |
| 6 | GUYS CALM DOWN. | X, 25 Sep 2026 | https://x.com/Outcomexyz/status/2103403501351289151 |
| 7 | GM Predictoors. Public service announcement. | X, 23 Sep 2026 | https://x.com/Outcomexyz/status/2102667893083357192 |
| 8 | Hype bears in disbelief. | X, 18 Sep 2026 | https://x.com/Outcomexyz/status/2100894112454979700 |
| 9 | Whose side are you on? | X, 13 Oct 2026 | https://x.com/Outcomexyz/status/2110078117054460295 |
| 10 | Is this market mispriced? | X, 8 Oct 2026 | https://x.com/Outcomexyz/status/2108127733113040937 |
| 11 | 9,000 hours of League and nothing to show for it? | X, 13 Oct 2026 | https://x.com/Outcomexyz/status/2110037001533812886 |
| 12 | Please don't go to conferences again, its bad for business. | X, 11 Oct 2026 | https://x.com/Outcomexyz/status/2109164782020698321 |
| 13 | Can't stop winning. | X, 17 Sep 2026 | https://x.com/Outcomexyz/status/2100555001877905693 |
| 14 | Feet up. Beers in. Outcomes, inevitable. | X, 16 Sep 2026 | https://x.com/Outcomexyz/status/2100273134012121189 |
| 15 | Same $100. Same side. Three venues. | X, 17 Sep 2026 | https://x.com/Outcomexyz/status/2100734412333646190 |
| 16 | Who bows at Anfield on Sunday? | X, 8 Oct 2026 | https://x.com/Outcomexyz/status/2108187673722806455 |
| 17 | Trade the Outcome. Get paid. | X reply, 21 Sep 2026 | https://x.com/Outcomexyz/status/2102060810311000372 |
| 18 | Don't just watch. Trade the outcome. | @OutcomeSports, 7 Oct 2026 | https://x.com/OutcomeSports/status/2107913391771898136 |
| 19 | Just Keep Clicking Playas. | Telegram, 8 Sep 2026 | https://t.me/Announcement_Outcome/65 |
| 20 | Check out our finance markets on Outcome.xyz. | Instagram, about 13 Oct 2026 | https://www.instagram.com/p/DeahhMWuqjB/ |

### 2.5 Guide versus practice
- Matches: no bet/wager/punt/gambling words in 115 posts, almost no exclamation marks, short declaratives, numbers as proof, "Hyperliquid." as a plain sign-off.
- Looser than the guide: Telegram ("Playas", "You're already late"), the 11 Oct conference joke, "Get paid" and "Stop leaving money on the table" in X lines, and the app's own "4% discount" labels (the guide bans "discounts").
- Instagram follows its own explainer style and always adds a disclaimer; the pinned X launch video thumbnail is a card with a two-line risk disclaimer.

## 3. What they post and amplify
### 3.1 Mix of the 151 own posts (my classification; medians)
| Type | n | Likes | Views | Notes |
|---|---|---|---|---|
| News headline plus a market chance (macro, oil, crypto, AI) | 30 | 27 | 1,639 | the daily staple, usually a topic-coloured card or chart |
| Link self-reply ("Trade the outcome." plus market URL) | 29 | 4 | 378 | under news and sports posts |
| Partner, event, team, Spaces | 17 | 46 | 2,488 | Gate Web3, ShareXYZ, Hyperliquid Forum, co-founders |
| News headline only | 16 | 21 | 1,812 | two outliers: 77K and 31K views |
| Hyperliquid or prediction-market ecosystem news | 13 | 76 | 4,472 | HIP-4 limits, buybacks, Kraken |
| Volume and traction milestones | 12 | 66 | 3,239 | mean views 22K |
| Launches, new markets, rewards | 12 | 64 | 4,568 | mean views 32K |
| Sports previews | 11 | 23 | 1,552 | most sports content sits on @OutcomeSports |
| Settled markets, trader wins, best-odds proof | 8 | 33 | 1,770 | P&L share cards |
| Memes, engagement bait, community | 3 | 18 to 29 | about 1,300 | thin: "Gmeow @grok", FPL league code |
- All 115 main posts: median 37 likes and 2,294 views (mean 63 and 8,563) on 27,030 followers.
- Cadence: 5.2 own posts a day, 4.0 without self-replies (max 8, 3 empty days). 93% Mon to Fri. 77% go out 10:00 to 18:59 UTC (15:30 to 00:29 IST), peaks 16:00 and 18:00 UTC. Match posts run to kickoff ("35 minutes to kickoff", "tonight").
- Top views: 226,417 ($100M HIP-4 volume video, 29 Sep); 210,465 (S&P 500 every 15 minutes, video, 15 Sep); 96,200 (NFL season tradeable, video, 19 Sep); 77,315 (Hyperliquid passes Nasdaq, 21 Sep, also top likes 1,229). Pinned launch video (29 Aug): 687,813 views, 2,864 likes, 52 s.
- Top engagement mechanics: "QRT with your call, then trade it" (Gate Web3 welcome, 9 Oct: 297 likes, 256 reposts); "list all the nuggets, win a golden upgrade code"; "Who should be in Outcome's video?"; @OutcomeSports "call the exact score, win $250" (follow, comment, drop profile link).
- By format (main posts, median views): video 3,693 (17 posts), text only 2,965 (39), photo 1,814 (59).
### 3.2 Video
- 17 of 151 posts (11%). Median 24 s (7 to 90 s). Mostly 1920x1080, about a quarter 1080x1350 (4:5), one square.
- First frames (thumbnails only, I did not download video): big white number on black ("$1,000,000"); B&W stock crowd; floating 3D market cards on black; a Blockworks conference clip of a speaker; a glitch-style "NaN" title frame; white frame with caps title, teal 3D logo coins and tiny disclaimer; football match card; Gate Web3 phone mock-up on bright green. The pinned video thumbnail is "OUTCOME.XYZ" in caps on near-black plus a two-line risk disclaimer (first or last frame, UNVERIFIED).
### 3.3 Who they amplify
- 9 reposts in 29 days: co-founders (@OutcomeAK x2, @IamGyomei), @OutcomeSports, @hypurr_co, a trader's claim that Hyperliquid beats Polymarket quotes on NFL (@Scott_eth, 305 likes), a conference recap (@jbfxdotme), an interview recap (@pangboygg), esports news (@sportful).
- 32 quote posts (21%): 12 quote their own posts to add a new angle; the rest quote @sharexyz x3, @ThisIsNewWave_ x3 (founder interview), @HL_forum x2, @OutcomeSports x2, @IamGyomei x2, and one each of @Payward (Kraken), @SECGov, @Cointelegraph, @SpaceX, @monolith_fund, @HyperliquidPC, @Footballtweet, @Scott_eth. A reply under the Gate welcome also quotes @GateDEX.
- Co-founders post under their own handles with "building the inevitable" in the bio: @OutcomeAK, @IamGyomei, @OutcomeMiG.
### 3.4 Other channels
- Telegram: about weekly, up to 113K views (first sports market, 4 Sep). Lines include "You're already late" and a 29 Aug note that a $40k influencer budget went to traders instead (top PnL trader each week gets $10k, UNVERIFIED whether still running).
- Instagram: 3 reels and 3 image posts in 7 to 13 Oct (dates derived from post IDs, UNVERIFIED), 0 to 6 likes each. Topics: Nasdaq overnight sessions, SpaceX debt, jobs report, Fed, Nvidia, LoL leaderboard.
- Blog: one SEO explainer (prediction markets versus leverage), author Jack Booth, links carry UTM tags.

## 4. Visual style (sheet 30_outcome_own_posts.jpg)
Sample: latest 40 X posts with media (28 Sep to 13 Oct, 48 images), 6 Instagram covers, X banner, avatar, pinned video thumbnail.
| Template (posts of the 40) | Look |
|---|---|
| Sports preview card (4 static, 2 as video) | deep plum or olive or black field; huge condensed % numerals in copper and sky blue (or yellow score digits); oil-painted player cut-outs; team names in caps; crests plus kickoff in UTC; "Outcome | sports" lockup with a pink or lime parallelogram tag. Second tile is a "Coming up next" stats card (form chips, head-to-head, injury notes) |
| Topic news card (9) | 16:9 split: left a flat colour field (emerald for energy and economy, blue for politics, purple for regulation) with caps headline, oil-painted cut-out and lockup bottom-left; right a dark app odds chart with Yes/No or Up/Down %, countdown boxes and the Outcome watermark |
| Chart or screenshot only (8) | app odds charts (white lines on black), stats.outcome.xyz HIP-4 share bars, third-party dashboards, a returns heat map |
| Win / P&L share card (3 posts, 9 cards) | white paper field, trophy art, "You predicted [side]" pill, event title, big "+$" profit, lime panel with Shares, Avg. Price, Bought, Earned, footer lockup plus the trader's avatar and handle |
| Instagram covers (6) | different system: dark news photos (real people), ultra-condensed white caps headline with the key phrase in red, small "Outcome.xyz" tag top-left, swipe arrows |
| Others | Fantasy Premier League promo (cyan to violet gradient, navy caps), Gate Web3 partner clip, one conference photo, one Hyperliquid-made graphic |
- **Fonts:** PP Neue Corp, Narrow Ultrabold for caps headlines, Normal Medium for small text (guide plus the Brand Tool's font files). Commercial font, not downloaded. App UI uses Geist or Inter; the site CSS names Bebas Neue as its own fallback. Instagram headlines use a different condensed caps face (UNVERIFIED which).
- **Colours seen (sampled from the images, about +/-4 per channel):** neon green #1AFE56 (banner, matches Signal Green), lavender #BA9ADA (crypto), yellow #E2FE02 (sports), mint #02DA9E (economics), coral #FE423E (finance), blue #0252FA (politics), black tag #0A0E12; plum #4C0C3C, copper #CC7C4C, sky #74C4F4, lime panel #D4EC04, dark olive #3C4404, emerald #04AC7C, royal blue #04349C, IG red #D4242C. Emerald and blue match the guide's Executive Teal and Protocol Blue; the sports plum, copper, sky, olive and lime are NOT in the guide, so treat them as the Outcome Sports sub-brand look. The X banner shows five category colours as vertical strips with vertical caps labels.
- **Logo:** angular bolt mark plus "Outcome" wordmark, always one colour that matches the card (white, dark green, lime). Placement: bottom-left on news and win cards, top-centre on sports cards (with the tag), top-left on Instagram, bottom-right tag "PREDICT IT" plus lockup on the X banner. Avatar is the black mark on white painted plaster. Cyan/magenta mark: 0 of 57 images.
- **Photo versus graphic:** photos are painted cut-outs of real people (players, officials, Trump, Buffett, Musk). Rights for likenesses and club crests are not ours to assume, so do not copy them without the client's say-so. Instagram uses real news photos, which breaks the guide's own no-stock-photo rule.
- **Meme templates:** none seen. Humour lives in the copy (puns, deadpan lines). No Wojak, Drake or screenshot-of-tweet formats in the sample.
- **App screenshots:** used as the right half of news cards and as stand-alone chart posts; the market-page screenshot is desktop-style and always dark.

## 5. App screens (phone)
Sources: page text of outcome.xyz (14 Oct), the app's own string dictionary, X images, and another task's capture sheet `raw\26\sheets\31_outcome_app_screens.jpg`. I saw the app logged out and region-blocked, so a signed-in state is UNVERIFIED.
- **Home:** top bar with logo lockup, leaderboard icon and "Sign In" pill; category tabs All, Sports, Crypto, Esports, Economics, Finance; gold ticket banner "Daily Rewards / Trade to earn / Predict the outcome" with a "$349,151.01 / $1M have been rewarded" counter and "Tap to Learn More"; a "Live" row of pills (BTC, WTIOIL, HYPE, ETH, GOLD, SILVER, SOL, S&P500, SPCX, US100, Soccer, Football, E Sports, Basketball); a card feed; bottom nav Home, BTC 15m, Activity, Profile. The "app" is an installable web app (PWA).
- **Cards:** multi-outcome cards list outcomes with %; two-sided cards show side names with multipliers and a payout line, for example "Up x1.1 / Down x11.3" and "$100 -> $110 / $100 -> $1,132"; tags Live, New, "Ends in 07:30:10", "$161.6k Vol.".
- **Market page (phone):** back arrow, "Sign In", title with coin or crest, stats Chance, Volume, Open interest, chips Rules and Rewards, Target and Current boxes, chart with an Outcome watermark and end labels such as "RC 41%", tabs Positions, Open Orders, History, Outcomes, then two big buttons: mint "UP 2.00X" and coral "DOWN 2.00X", or "YES 2.44x" and "NO 1.69x". The desktop page text also lists an Order Book (Price, Shares, Total, Spread) and a countdown in days, hr, min.
- **Buy / Sell panel (exact words):** tabs Buy and Sell; order type Market, Limit, Convert, 1-Tap; side Yes or No (also Up/Down or a team code); Amount with +5 +10 +50 +100 Max; toggle to Shares; Payout (buying) or Cash Out (selling); "Order Information" with Est. fill price and Slippage; CTA "Place Order" (states: Sign In, Accept Terms, Complete setup, Unavailable in your region, Insufficient balance). Phone drawer is titled "Trade" with "Buying" or "Selling". No "Buy Yes" string exists in the dictionary (a signed-in button could still join Buy and the side, UNVERIFIED); "Predict" is used as copy and a route name, not a button.
- **Prices:** order book in cents ("63¢", spread "0.001¢"); outcome rows in % ("62%"); Yes/No panel "Yes 62¢ / No 38¢"; two-team games "LAR 1.14x / ARI 8.10x"; cards "Up x1.47" plus "$100 -> $147". The docs explain 40 cents = 40% likely and a $1 payout.
- **Share / P&L card:** actions "Share your win", "Share your loss", "Share on X", "Download"; default post text names @OutcomeXYZ and a rocket emoji. Card fields: You predicted [side], event, +$ profit, Shares, Avg. Price in cents with 3 decimals ("50.349¢"), Bought, Earned, avatar and username. Toasts: "Card shared!", "Card downloaded!". Tagline on profile sharing: "Let the numbers speak."
- **Leaderboard:** "Leaderboard / Top performers across all outcomes", tabs Today, Weekly, Monthly, All, modes Profit/Loss, ROI (%), Volume; rows show rank, avatar, badges, "+$17,009.72", "+44.15%", volume.
- **Rewards page:** steps "Trade on Outcome", "Post Orders Near The Price", "Earn daily in USD"; "Traders of the day"; FAQs. Badges and "Achievement Unlocked" cards (Hall of Fame, Genesis Depositor).

## 6. Official brand, press, media-kit, creator pages
- YES: https://brand.outcome.xyz/ (public guide, a "press kit" button I did not open, DESIGN.md; partner kit gated). Ask the client for portal access and the asset pack. Verbatim copies of what I read are in `raw\26\brand\pages\`.
- Other official pages: blog.outcome.xyz (Ghost), docs.outcome.xyz (support by Discord, email, live chat; hello@outcome.xyz), stats.outcome.xyz/builder, t.me/Announcement_Outcome (public), GitHub Outcome-xyz (SDK).
- No creator, affiliate, ambassador or UGC page found. outcome.xyz/brand, /press, /media-kit, /creators, /ambassador, /affiliate, /partners, /about, /blog all return 404. Only hint: the Telegram influencer-budget line above.
- A general web search was not possible (the session's search budget was used up), so nothing beyond Outcome's own domains was checked. Worth a follow-up search for third-party coverage.

## 7. What this means for our faceless posts
- Write the way the news desk does: statement, one number, one question or one CTA line. Use "Trade the outcome." as the closing line.
- Caps for milestones only; sentence case for previews. No exclamation marks, no emoji, no bet/wager/punt/gambling, no payout percentages, no "discount", no hedges.
- Follow the guide: PP Neue Corp (ask for the font files or use the Bebas Neue fallback), flat theme colours, oil-painted cut-outs, one-colour lockup opposite the headline, no drop shadows. TikTok preset is 608x1080 (9:16); export at 1080x1920.
- Copy the proof formats that work: big-number milestone video, news card with live odds chart, win card with Shares / Avg. Price / Bought / Earned. Keep the not-advice disclaimer from their videos and Instagram.
- Real faces and crests are everywhere in their art; for us use objects and places painted in the same style unless the client clears people.

## 8. UNVERIFIED and gaps
- X numbers come from the FxTwitter mirror (14 Oct), not X's own API; the sample is 29 days, so medians are rough. Post-type labels are my own.
- Instagram: 3 of 9 posts not visible; dates come from post IDs. Telegram racing-car emoji meaning (the guide's race-car metaphor) is a guess.
- Colour values are sampled from compressed images; use the DESIGN.md hex values for builds.
- I did not see partner/KOL pages, the Outcome Creator Guide, a signed-in app, or a loss card.

## Sources (read 14 Oct 2026 unless noted)
- X data: https://api.fxtwitter.com/2/profile/Outcomexyz/statuses , https://api.fxtwitter.com/2/profile/Outcomexyz , https://api.fxtwitter.com/2/profile/OutcomeSports/statuses , https://api.fxtwitter.com/Outcomexyz/status/2093618947396411581 (pinned, 29 Aug)
- Site and app: https://outcome.xyz/ , /markets/sports , /markets/crypto , /markets/crypto/o7180 , /markets/sports/q391 , /markets/sports/o11458 , /leaderboard , /rewards (read through r.jina.ai); app strings from the HTML of https://outcome.xyz/markets/crypto/o7180
- Brand: https://brand.outcome.xyz/brand-guide (+ /voice-tone, /brand-character, /design-language, /colors, /about-outcome, /logo, /design-md; Typography read from the index page), https://brand.outcome.xyz/DESIGN.md
- Docs and blog: https://docs.outcome.xyz/llms.txt and pages introduction, how-prediction-markets-work, placing-your-first-trade, closing-a-position, managing-your-positions, badges-and-cards, leaderboard, recurring-markets; https://blog.outcome.xyz/prediction-markets-vs-leverage-trading/ (7 Jul 2026)
- Social: https://t.me/s/Announcement_Outcome ; https://www.instagram.com/outcomexyz/embed/ and https://www.instagram.com/p/DecPcClJ4ec/ , /DeahhMWuqjB/ , /DeYJo01umS_ , /DeXXIPaPbPL/ , /DeSwCIUOMpC/ , /DeNTPkHvqiG/ ; https://discord.com/api/v9/invites/outcome?with_counts=true ; https://polymart.app/outcome-xyz (third-party blurb, no posts)
- Background (not redone): `outcome\research\01-what-is-outcome.md` section 7; `outcome\studio\assets\logos\outcome\brand.json`.
