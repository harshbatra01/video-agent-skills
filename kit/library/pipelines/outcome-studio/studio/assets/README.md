# Outcome studio asset kit

Built 13 Oct 2026. Everything came from public pages, no logins, one request at a time with a normal browser User-Agent (about 240 requests in total). No club crests, league logos or player photos were downloaded.

## What is here

| Path | What | Count |
|---|---|---|
| `fonts/` | 5 open-licence font families, each in its own folder with its OFL.txt, plus `fonts.json` | 7 font files |
| `logos/outcome/` | Outcome's own public brand files plus `brand.json` | 18 files |
| `logos/*.svg` | simple-icons (CC0): bitcoin, ethereum, solana, anthropic, openai, spacex, nvidia, tiktok, instagram, youtube, x, plus `icons.json` and the licence | 11 icons |
| `flags/` | one SVG per country code used in teams and players, plus the MIT licence | 35 flags |
| `teams.json` + `teams_meta.json` | clubs and teams with short names, codes, colours, country, league, aliases | 146 teams |
| `players.json` + `players_meta.json` | the official 30 men's 2026 Ballon d'Or nominees | 30 players |
| `emoji/` | 29 PNG files that were already in this folder before the kit. Not covered by this README. | 29 |

## Fonts (`fonts/`, licence: SIL Open Font License 1.1)

Source: github.com/google/fonts, folder `ofl/<family>`. Each file was checked after download: real TrueType (magic bytes `00010000`), size matches the GitHub listing, family name read from inside the file. Details, sha256 and ready-made `@font-face` lines are in `fonts.json`.

| CSS font-family | Files | Weights | Numbers |
|---|---|---|---|
| Inter | `inter/Inter-Variable.ttf`, `Inter-Italic-Variable.ttf` | variable 100 to 900 (also optical size 14 to 32) | proportional by default. Use `font-variant-numeric: tabular-nums` for equal-width digits. |
| Anton | `anton/Anton-Regular.ttf` | 400 | the digit 1 is narrower and there is no tnum feature. Do not use for numbers that change. |
| Bebas Neue | `bebasneue/BebasNeue-Regular.ttf` | 400 | equal-width digits |
| Archivo Black | `archivoblack/ArchivoBlack-Regular.ttf` | 400 | equal-width digits |
| JetBrains Mono | `jetbrainsmono/JetBrainsMono-Variable.ttf`, `JetBrainsMono-Italic-Variable.ttf` | variable 100 to 800 | monospaced, every digit the same width |

OFL lets you use, embed and render these into images and video, including paid work. Do not sell the font files on their own, and keep the OFL.txt with any copy you pass on.

Outcome's own site uses Inter for body text and a commercial display face called PP Neue Corp. Its CSS names Bebas Neue and then Inter as the fallback, so Inter plus Bebas Neue is the closest open match. PP Neue Corp was not downloaded.

## Outcome brand files (`logos/outcome/`)

Outcome's own marks. Use them only for Outcome work. `brand.json` lists every file with source URL, size, sha256, colours found, plus the manifest colours and the site's colour tokens (70 `--oc-*` values read from its CSS). Cloudflare did not block outcome.xyz, cdn.outcome.xyz or docs.outcome.xyz.

| File | What it is | Use it on |
|---|---|---|
| `logo.svg` | colour mark (cyan #00FFFF, magenta #FF00F2) plus near-white wordmark #F5F8FF | dark backgrounds |
| `lockup-dark-gray.svg` | one-colour near-white #F5F5F5 mark and wordmark | dark backgrounds |
| `lockup-light-gray.svg` | one-colour near-black #171717 mark and wordmark. Taken from docs.outcome.xyz because outcome.xyz/lockup-light-gray.svg is a 404 | light backgrounds |
| `icon.svg` | the mark alone, cyan and magenta, transparent background | anywhere |
| `icon-foil.svg` | the mark in flat grey #808080, made for a foil card effect | probably not needed |
| `docs-outcome_logo.svg` | outlined mark from the docs site | optional |
| `favicon-icon-light.svg`, `favicon-icon-dark.svg` | 40x40 rounded tile, light or dark | app tile |
| `favicon.ico` (16, 32, 48), `favicon-icon-light.ico` (32) | favicons | |
| `apple-touch-icon.png` 180, `android-chrome-192x192.png`, `android-chrome-512x512.png`, `mstile-150x150.png` | the crumpled-paper style app icon | |
| `og-image.png` 1200x630 | share image: "THE OUTCOME IS INEVITABLE", "Predict it at outcome.xyz" | |
| `rewards-banner.webp` 1200x494 | the gold rewards ticket: "$1,000,000 Rewards Program, trade to earn on every action, rewards distributed daily" | |
| `manifest.webmanifest`, `browserconfig.xml` | theme_color and background_color are both **#0b0c0f**, tile colour #0b0c0f | |

Core site colours (from its CSS): black #0B0C0F, text #F5F8FF, light blue #C2D6FF, cyan #00FFFF, purple/magenta #FF00F2, green #99FFBC, red #FF3D5E, live red #FF0051, yellow #FFCC00, orange #FFA100, gold #FFD699, info blue #3D9EFF. Surfaces: #111217, #232326, #101216.

Not downloaded on purpose (listed in `brand.json`): the per-market artwork under `cdn.outcome.xyz/assets/outcome/` and `/question/` (can contain crests or player images), the World Cup trophy and World Cup share image (FIFA), the market symbol PNGs, the token art, and site UI pictograms. No rewards badge images exist under `cdn.outcome.xyz/assets/`. The only rewards image is the ticket above, served from `outcome.xyz/images/`.

## Icons (`logos/`, licence: CC0 for the files)

simple-icons 13.21.0 (what `@13` resolves to) from `cdn.jsdelivr.net/npm/simple-icons@13/icons/<slug>.svg`. One colour each, no fill set, 24x24 viewBox. `icons.json` has the official brand hex, for example Bitcoin #F7931A, Solana #9945FF, NVIDIA #76B900, YouTube #FF0000. CC0 covers the files. The logos themselves are trademarks of their owners.

Missing: **hyperliquid**. It is not in simple-icons at 13.21.0 or in the latest release (404 on both, and the data only has Hyper, Hyperskill and HyperX). Outcome serves its own HYPE art (`cdn.outcome.xyz/assets/tokens/hype.webp`, `/assets/pills/hype.svg`). I did not download it because it is a third-party token logo.

## Flags (`flags/`, licence: MIT)

35 files named by code, 4x3 shape: am ar at az be bg br ca co cy cz de ec es fr gb-eng gb-sct ge gr hr hu il it ma mx nl no pl pt si sk sn tr ua us. From lipis/flag-icons 7.2.3 via jsDelivr. Licence text: `flags/LICENSE-flag-icons-MIT.txt`. Every `country` in teams.json and `nationality` in players.json has a file here.

## teams.json (146 teams)

A plain list of objects. Load with `json.load(open("teams.json", encoding="utf-8"))`. Field notes and sources are also in `teams_meta.json`.

| Competition | Teams |
|---|---|
| UEFA Champions League 2026/27 league phase | 36 |
| UEFA Europa League 2026/27 league phase | 36 |
| English Premier League 2026/27 | 20 |
| NFL | 32 |
| NBA | 30 |

English clubs sit in two lists (Arsenal is UCL and EPL), so there are 84 different soccer clubs. The three soccer lists were checked against each other: Outcome's live market feed (all 36 UCL clubs, 16 UEL clubs), ESPN's team lists, and the Wikipedia 2026-27 pages all agree.

| Field | Meaning |
|---|---|
| `name` | long name in plain ASCII, as Outcome or ESPN write it. Look teams up by `name` or `aliases`. |
| `short` | what fans call it (Man City, PSG, Spurs, Rams). Not unique across sports. |
| `code` | three letters. Soccer codes are unique across all 84 clubs. NBA uses the official tricodes. NFL uses Pro-Football-Reference style where ESPN has two letters (GNB, KAN, LVR, NWE, NOR, SFO, TAM, WAS). The same code can exist in two sports (ATL, CHI, MIA). |
| `code_espn` | the abbreviation ESPN uses (what Outcome shows for some NFL teams: KC, LV, TB, NO) |
| `primary`, `secondary` | hex colours, see below |
| `colours` | every colour the source lists, in order |
| `on_dark` | derived accent for Outcome's dark background: first colour of primary and secondary that is not grey, lightened until contrast on #0B0C0F is at least 4.5:1. Use this for chips and bars on dark. |
| `colour_source`, `colour_source_url`, `colour_confidence`, `colour_note` | where each team's colours came from |
| `country` | ISO 3166-1 alpha-2 lowercase, England `gb-eng`, Scotland `gb-sct`. Matches `flags/`. |
| `league` | domestic league (NFL or NBA for those) |
| `competitions` | which of UCL, UEL, EPL, NFL, NBA this team is in now |
| `aliases` | other spellings: Outcome strings, ESPN names, Wikipedia names, with and without accents |
| `espn_id` | ESPN team id |

Aliases: all 24 Outcome spellings from the brief are present exactly as written, each on the right team (Paris Saint Germain on Paris Saint-Germain, Bournemouth AFC on AFC Bournemouth, RC Celta on Celta Vigo, Sabah Baku on Sabah FK, Viking on Viking FK, and so on). They are listed even where they equal `name`. Every club and team name in Outcome's live feed resolves to a record, except the 8 MLB teams (not asked for). Only one alias is ambiguous: "Spurs" is both Tottenham and San Antonio, so match by league.

Colours, in order of trust:
1. **teamcolorcodes.com** (114 teams: 52 soccer clubs, 32 NFL, 30 NBA; 113 are confidence high): the team's own page. `primary` is the first colour listed. `secondary` is the next listed colour that is visibly different (so Arsenal's dark red is skipped). Nine clubs are swapped because TCC lists crest colours first and the shirt colours are different; `colour_note` says which (Barcelona, Bayern, Atletico, Feyenoord, PSV, AZ, Marseille, Crystal Palace, Aston Villa). Tottenham's page lists navy only, so white comes from ESPN and that one is marked medium.
2. **No TCC page (32 clubs)**: ESPN's colour fields, corrected from the club's Wikipedia 2026-27 home kit where ESPN is clearly wrong (for example Slavia's light blue, Olympiacos' blue, Lillestrom's red). Fenerbahce and Olympiacos use the TCC pages for their basketball sections, which share the club's colours. Of these 32, 25 are confidence medium and 7 are confidence **low**, meaning ESPN only and not confirmed: Bodo/Glimt, LASK Linz, Sabah FK, Viking FK, Ararat-Armenia, Dinamo Zagreb, NK Celje.

## players.json (30 players)

A plain list. These are the official 30 men's 2026 Ballon d'Or nominees (ceremony 26 Oct 2026, London Palladium, France Football). Includes the 7 you named: Kane, Yamal, Messi, Dembele, Mbappe, Haaland, Bellingham.

| Field | Meaning |
|---|---|
| `name`, `ascii`, `short`, `short_ascii` | official spelling, plain ASCII (how Outcome writes names), fan name |
| `nationality`, `nationality_name` | ISO code matching `flags/` |
| `club` | club as of 13 Oct 2026 (Wikipedia infobox) |
| `club_team` | the matching `name` in teams.json, or null for Inter Miami, Al-Nassr, Al-Qadsiah |
| `club_2025_26` | the club for the season the award covers |
| `position`, `position_detail` | Forward, Midfielder or Defender from the nominee table, and the infobox position |
| `on_outcome_ballon_dor_market`, `outcome_name` | true for the 7 candidates Outcome lists, with Outcome's spelling |
| `sources` | URLs |

Three players changed club in summer 2026: Rodri (Manchester City to Barcelona), Marc Cucurella (Chelsea to Real Madrid), Ferran Torres (Barcelona to Paris Saint-Germain). `club` is the new club. `club_2025_26` is the old one. Wikipedia's nominee table lists Real Madrid for Cucurella, but his infobox shows Chelsea until 2026, so Chelsea is given.

## Licences and rights

| Part | Licence | Notes |
|---|---|---|
| Fonts | SIL OFL 1.1 | text in each family folder |
| Outcome files | Outcome's own marks | client work only |
| simple-icons | CC0 for the files | the logos are trademarks of their owners |
| flag-icons | MIT | text in `flags/` |
| Data (teams, players) | facts compiled from ESPN, teamcolorcodes.com and Wikipedia | Wikipedia text is CC BY-SA, only facts were taken. Sources are named per team and per player. |

## Not included, and gaps

- Hyperliquid icon (see Icons).
- MLB (Outcome has MLB championship markets: Dodgers, Yankees, Brewers, Rays, Phillies, Braves, Red Sox, Cubs), Conference League clubs, and the 30 women's Ballon d'Or nominees. All can be added.
- Club crests, league logos and player photos: left out on purpose (rights).
- teamcolorcodes.com answered its REST endpoint with a Cloudflare challenge. I did not try to get past it and used its normal team pages instead (116 pages, 1.2 seconds apart, no further challenges).
- TheSportsDB was tried for colours and has none filled in, so it was not used.

## Sources

- Outcome: outcome.xyz (home, /rewards, /world-cup pages, manifest.webmanifest, browserconfig.xml, site CSS), cdn.outcome.xyz, docs.outcome.xyz, and the studio's own `data/archive/meta/20261013-1028.json` for exact market spellings.
- Fonts: https://github.com/google/fonts/tree/main/ofl
- Colours: https://teamcolorcodes.com (page URL on every team), https://site.api.espn.com/apis/site/v2/sports/ (soccer/uefa.champions, soccer/uefa.europa, soccer/eng.1, football/nfl, basketball/nba)
- Participants, players and kits: en.wikipedia.org pages for the 2026-27 UEFA Champions League, UEFA Europa League and Premier League, the 2026 Ballon d'Or, and each player and club article
- Icons: https://cdn.jsdelivr.net/npm/simple-icons@13/
- Flags: https://cdn.jsdelivr.net/gh/lipis/flag-icons@7.2.3/
