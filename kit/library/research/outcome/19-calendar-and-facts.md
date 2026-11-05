# 19. Calendar of hooks and verified facts, 13 to 23 Oct 2026

Built 13 Oct 2026, about 11:30 UTC (before the first 13 Oct kickoff). All times are UTC unless marked. IST = UTC + 5:30 (16:45 UTC = 22:15 IST, 19:00 UTC = 00:30 IST next day). Clocks: UK and Europe go back an hour on Sun 25 Oct, so UEFA slots move to 17:45 and 20:00 UTC from the 26th. Everything in the 13 to 23 Oct window uses 16:45 and 19:00 UTC.

## Read this first (what changes your brief)

1. The last Fed decision was a HIKE (16 Sep, to 3.75% to 4.00%), not a hold. "Hike" is a live outcome, and the 14 Oct CPI is the swing event.
2. Ballon d'Or voting closed on 28 Sep. The 50% to 66% Kane move is traders guessing how 100 journalists voted. I found NO confirmed news at the time of the jump (9 Oct, 17:45 UTC). Cause is UNVERIFIED. Do not say "leak confirmed" or "Kane has won".
3. Anthropic has scheduled nothing publicly except the 1 Jun confidential filing. Everything else (investor day 14 Oct, roadshow week of 9 Nov, trading before 26 Nov, $1.8T to $2T) is Bloomberg, Reuters or WSJ reporting. Say "reported", never "will".
4. Best close calls for "Pick a Side" (bookmaker lines on ESPN, 13 Oct): Man City v PSG, Betis v Porto, Lyon v Palace, Shakhtar v AEK, Celta v Juventus, Union SG v Sociedad, Hoffenheim v Besiktas, Como v Feyenoord, Roma v Real Madrid.

## How to read this file

- VERIFIED = checked against the source named on the line. UNVERIFIED = single weak source, conflicting sources, or not found. Do not put UNVERIFIED lines on screen without a re-check.
- "Form" = last five competitive games in all competitions, oldest first, friendlies left out. ESPN's own "last five" box includes friendlies, so a few sides differ from it.
- Facts are written under 12 words so they fit a card. The date in brackets is the day the data was pulled (13 Oct 2026). League tables count games played to that date.
- ESPN pages used: team results `https://www.espn.com/soccer/team/results/_/id/{id}` (opened and matched for Man City), league table `https://www.espn.com/soccer/table/_/league/{slug}` (link format taken from ESPN's own API), match page `https://www.espn.com/soccer/match/_/gameId/{id}`. Raw JSON behind them: `https://site.api.espn.com/apis/site/v2/sports/soccer/{league}/scoreboard?dates=YYYYMMDD`, `.../uefa.champions/summary?event={id}`, `.../all/teams/{id}/schedule`, `https://site.api.espn.com/apis/v2/sports/soccer/{slug}/standings`.
- Kickoff times were cross-checked two ways: ESPN scoreboard (UTC) and Outcome's own market data (`POST https://api.hyperliquid.xyz/info {"type":"outcomeMeta"}`, field `scheduledStart`). All 26 football markets and all NFL games agree.

---

## 1. Calendar, 13 to 23 Oct (UTC)

"Q" = Outcome question id in outcomeMeta (13 Oct). Sources for times: ESPN scoreboards and Outcome `scheduledStart`.

### Tue 13 Oct (today), Champions League matchday 2, first night

| UTC | Match | Venue | Q |
|---|---|---|---|
| 16:45 | RC Lens v Sporting CP | Stade Bollaert-Delelis | 405 |
| 16:45 | Sabah Baku v Slavia Praha | Baku Olympic Stadium | 406 |
| 19:00 | Arsenal v Lille | Emirates | 412 |
| 19:00 | Atletico Madrid v Man United | Metropolitano | 407 |
| 19:00 | Galatasaray v Barcelona | RAMS Park | 413 |
| 19:00 | Inter v Club Brugge | San Siro | 409 |
| 19:00 | RB Leipzig v PSV | Red Bull Arena | 411 |
| 19:00 | Viking v Bayern | Viking Stadion | 408 |
| 19:00 | Villarreal v Napoli | La Ceramica | 410 |

Hook: Bayern, Kane's club, are at Viking at 19:00 while his Ballon d'Or price sits at about 62%. I found no Kane fitness or line-up news for this game (UNVERIFIED either way).

### Wed 14 Oct

| UTC | Event | Note | Q |
|---|---|---|---|
| 12:30 | US CPI for September (08:30 ET) | BLS: "scheduled to be released on October 14, 2026, at 8:30 A.M. Eastern Time". August was 3.4% y/y; forecasts about 3.6% to 3.7%, core about 2.4%. Source: https://www.bls.gov/cpi/ (13 Oct) | n/a |
| not reported | Anthropic investor day, San Francisco HQ | Bloomberg 1 Oct: invitations sent; Anthropic declined to comment. NOT company-confirmed. https://www.bloomberg.com/news/articles/2026-10-01/anthropic-is-said-to-plan-pre-ipo-investor-day-as-listing-nears | outcome 5112 (IPO by 30 Nov) |
| 16:45 | Feyenoord v Como | De Kuip | 416 |
| 16:45 | LASK v Liverpool | Raiffeisen Arena, Linz | 415 |
| 19:00 | AS Roma v Real Madrid | Olimpico | 423 |
| 19:00 | Aston Villa v Fenerbahce | Villa Park | 421 |
| 19:00 | Bodo/Glimt v Dortmund | Aspmyra | 418 |
| 19:00 | Man City v PSG | Etihad | 422 |
| 19:00 | Real Betis v Porto | La Cartuja | 417 |
| 19:00 | Shakhtar v AEK Athens | Stamford Bridge, London (Shakhtar's home ground this season) | 419 |
| 19:00 | Slovan Bratislava v Stuttgart | Narodny futbalovy stadion | 420 |

Shakhtar at Stamford Bridge: https://www.espn.com/soccer/story/_/id/49681961 and https://shakhtar.com/en/news/2026/august/21_news/21_shakhtar_stamford_bridge/ (Aug 2026).

### Thu 15 Oct, Europa League matchday 2

| UTC | Match | Venue | Q |
|---|---|---|---|
| 16:45 | Lyon v Crystal Palace | Groupama Stadium | 425 |
| 16:45 | RB Salzburg v AC Milan | Red Bull Arena | 428 |
| 16:45 | Torreense v Sunderland | Estadio Dr. Magalhaes Pessoa, Leiria | 426 |
| 16:45 | Union Saint-Gilloise v Real Sociedad | King Power at Den Dreef | 429 |
| 19:00 | Benfica v Celtic | Estadio da Luz | 433 |
| 19:00 | Bournemouth v Sturm Graz | Vitality Stadium | 427 |
| 19:00 | Celta Vigo v Juventus | Balaidos | 431 |
| 19:00 | Hoffenheim v Besiktas | PreZero Arena | 432 |

### Fri 16 Oct

- 00:15 UTC (Thu 8:15 pm ET): NFL Thursday night, Seahawks (3-2) at Broncos (3-2), Seattle -3, Prime Video. https://site.api.espn.com/apis/site/v2/sports/football/nfl/scoreboard?dates=20261015 (13 Oct). Outcome shows this game at `scheduledStart` 20261016-0015.

### Sat 17 Oct, Premier League (positions are ESPN, 13 Oct, after 6 games each)

| UTC | Match | Positions | Flag |
|---|---|---|---|
| 11:30 | Everton v Chelsea (Hill Dickinson Stadium) | 5th v 6th, both 10 pts | BIG |
| 14:00 | Brentford v Liverpool | 4th v 9th (Liverpool lost 0-3 to City on 11 Oct) | BIG |
| 14:00 | Man City v Ipswich | 1st (6 wins from 6) v 10th | BIG (can go 7 from 7) |
| 14:00 | Fulham v Hull City | 20th (2 pts) v 8th | low |
| 16:30 | Newcastle v Aston Villa | 11th v 16th | medium |

### Sun 18 Oct, Premier League and NFL week 6

| UTC | Match | Positions or note | Flag |
|---|---|---|---|
| 13:00 | Leeds v Man United | 7th v 13th | BIG |
| 13:00 | Brighton v Crystal Palace | 3rd v 12th | medium |
| 13:00 | Bournemouth v Sunderland | 18th v 17th, relegation fight | low brand |
| 15:30 | Nottingham Forest v Arsenal | 15th v 2nd (Arsenal 15 pts, City 18) | BIG |
| 13:30 | NFL London: Texans (1-4) v Jaguars (4-1), Wembley, NFL Network | Jacksonville -3 | marquee |
| 17:00 | NFL: Ravens (4-1) at Browns; Bears at Falcons; Titans (0-5) at Colts; Jets at Patriots; Saints at Giants; Panthers at Eagles; Steelers at Buccaneers | CBS and Fox | slate |
| 20:05 | NFL: Cardinals (1-4) at Rams (2-3), Fox | Rams -13.5 | |
| 20:25 | NFL: Chargers (0-5) at Chiefs (4-0), CBS; Bills (4-1) at Raiders (3-2), CBS | Chiefs -8.5, Bills -6 | marquee |

### Mon 19 Oct (UTC) and the Sunday and Monday night NFL games

- 00:20 UTC Mon (Sun 8:20 pm ET): NFL Sunday night, Cowboys (2-3) at Packers (3-2), NBC, Green Bay -1.5.
- 19:00 Premier League: Tottenham (19th, 3 pts, no wins in 6) v Coventry (14th), medium.
- 00:15 UTC Tue 20 Oct (Mon 8:15 pm ET): NFL Monday night, Commanders (1-3-1) at 49ers (5-0), ESPN and ABC, SF -7.5.
- NFL source for all of the above: ESPN NFL scoreboard, dates 20261015, 20261018, 20261019 (13 Oct). Outcome lists the same games with the same start times.

### Tue 20 Oct

- NBA opening night, three games, all NBC and Peacock (ESPN scoreboard 20261020; schedule also in NBC affiliate coverage):
  - 19:00 Celtics at Pistons (3:00 pm ET)
  - 23:00 76ers at Knicks (7:00 pm ET); the Knicks raise their banner as defending champions (per NBC affiliate preview, single source)
  - 01:30 UTC Wed 21 Oct: Thunder at Spurs (9:30 pm ET)
  - https://www.nbcnewyork.com/nba/nba-opening-night-schedule-games-watch-knicks-spurs-sixers-thunder-celtics-pistons/6535251/ and https://site.api.espn.com/apis/site/v2/sports/basketball/nba/scoreboard?dates=20261020 (13 Oct). Regular season runs to 11 Apr 2027. Story hooks from that preview (LeBron's 76ers debut, Jaylen Brown trade) are single-source: UNVERIFIED, re-check before use.
- Champions League matchday 3, first night (ESPN, 13 Oct): 16:45 Fenerbahce v Slavia Praha, Sabah v Dortmund; 19:00 Roma v Slovan, Porto v PSV, Liverpool v Villarreal, Man City v AEK, Napoli v Bodo/Glimt, PSG v Barcelona (big), Stuttgart v Atletico.

### Wed 21 Oct

- Champions League matchday 3, second night: 16:45 Como v Man United, Lille v Galatasaray; 19:00 Aston Villa v Viking, Bayern v Arsenal (big), Club Brugge v Lens, Inter v Shakhtar, Betis v Feyenoord, Real Madrid v Leipzig, Sporting v LASK. Outcome has not listed these yet (13 Oct).

### Thu 22 Oct and Fri 23 Oct

- Europa League matchday 3 on Thu 22 Oct at 16:45 and 19:00 UTC, for example Juventus v Rennes, Lech v Sunderland, Ferencvaros v Torreense (ESPN scoreboard 20261022; not fully listed here).
- About Fri 23 to Sun 25 Oct: the date by which Anthropic's public S-1 would have to appear if the roadshow starts Mon 9 Nov (15-day rule, my arithmetic from Bloomberg's report; no filing date is announced). UNVERIFIED as a date.

### Just outside the window (for planning)

- Mon 26 Oct: Ballon d'Or ceremony, London Palladium (VERIFIED, see section 3). Start time UNVERIFIED.
- Tue 27 to Wed 28 Oct: FOMC. Statement Wed 28 Oct at 18:00 UTC (2:00 pm EDT). Source: https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm (13 Oct, "October 27-28", no projections that meeting); release time from the 16 Sep statement "For release at 2:00 p.m. EDT" and Outcome field `scheduledDecision:20261028-1800`.
- Thu 5 Nov: Outcome's Ballon d'Or market `resolutionDeadline` is 20261105-2359.
- Week of 9 Nov: possible Anthropic roadshow start (reported). Thu 26 Nov: Thanksgiving, the reported "trade before" date.

---

## 2. "Pick a Side" fact packs, 14 and 15 Oct

Each side has two facts (A = form, B = table position or a headline result). Each match also has head-to-head, team news and the bookmaker line. Moneylines are DraftKings via ESPN (13 Oct), shown only to help you pick close games, not as a claim. Team news for 14 Oct is from UEFA.com (13 Oct); for 15 Oct it is third-party and UNVERIFIED. Team news changes by kickoff: re-check on the day.

UEFA team news page (all 14 Oct clubs): https://www.uefa.com/uefachampionsleague/news/02aa-21cf3c78cf12-1c26cfd9b696-1000--champions-league-predicted-line-ups-matchday-2-team-news-/ (13 Oct)

### Wed 14 Oct, Champions League matchday 2

**1. Feyenoord v Como | 16:45 | De Kuip | ESPN 401915416 | Q416** (https://www.espn.com/soccer/match/_/gameId/401915416)
- Feyenoord A: Last five WLWWW, 18 scored, 6 conceded. https://www.espn.com/soccer/team/results/_/id/142 (13 Oct)
- Feyenoord B: 1st in Eredivisie, 20 points from 8 games. https://www.espn.com/soccer/table/_/league/ned.1 (13 Oct)
- Como A: Last five WWWLD, 10 scored, 5 conceded. https://www.espn.com/soccer/team/results/_/id/2572 (13 Oct)
- Como B: 7th in Serie A, 11 points from 6 games. https://www.espn.com/soccer/table/_/league/ita.1 (13 Oct)
- Head to head: no earlier meeting listed. Matchday 1: Feyenoord lost 1-5 at Barcelona, Como beat Leipzig 4-1 (ESPN results pages).
- Team news (UEFA): Feyenoord out Borges, Bos, Moder, Nelson, Nieuwkoop, Smal, Van Persie, Watanabe doubtful. Como: Kean doubtful.
- Line: Como -105, Feyenoord +240, draw +320.

**2. LASK v Liverpool | 16:45 | Raiffeisen Arena, Linz | ESPN 401915415 | Q415**
- LASK A: Last five WLLDL, 7 scored, 9 conceded. https://www.espn.com/soccer/team/results/_/id/4411 (13 Oct)
- LASK B: 3rd in Austrian Bundesliga, 16 points from 8 games. https://www.espn.com/soccer/table/_/league/aut.1 (13 Oct)
- Liverpool A: Last five WDWWL, 6 scored, 5 conceded. https://www.espn.com/soccer/team/results/_/id/364 (13 Oct)
- Liverpool B: 9th in Premier League, 9 points from 6 games. https://www.espn.com/soccer/table/_/league/eng.1 (13 Oct)
- Head to head: Liverpool won both, 3-1 away (21 Sep 2023) and 4-0 home (30 Nov 2023). https://www.espn.com/soccer/match/_/gameId/401915415 (13 Oct)
- Team news (UEFA): LASK out Usor, Bello. Liverpool out Bradley, Ekitike, Leoni; Isak, Gakpo, Szoboszlai doubtful.
- Line: Liverpool -350, LASK +800, draw +500.

**3. Roma v Real Madrid | 19:00 | Olimpico | ESPN 401915414 | Q423**
- Roma A: Last five WDWDD, 7 scored, 4 conceded. https://www.espn.com/soccer/team/results/_/id/104 (13 Oct)
- Roma B: 3rd in Serie A, 14 points, unbeaten in 6. https://www.espn.com/soccer/table/_/league/ita.1 (13 Oct)
- Real Madrid A: Last five WWWLW, 11 scored, 6 conceded. https://www.espn.com/soccer/team/results/_/id/86 (13 Oct)
- Real Madrid B: 4th in La Liga, 18 points from 8 games. https://www.espn.com/soccer/table/_/league/esp.1 (13 Oct)
- Head to head: Madrid unbeaten in last five meetings (4 wins, 1 draw); last competitive one Roma 0-2 Madrid, 27 Nov 2018. https://www.espn.com/soccer/match/_/gameId/401915414 (13 Oct)
- Team news (UEFA): Roma out Cristante, Svilar; Koulierakis doubtful. Madrid out Asencio, Militao, Rodrygo. UNVERIFIED conflict: a search summary of another preview says Valverde is missing, Mbappe is training alone and Malen is doubtful; that is not in UEFA's list.
- Line: Madrid -110, Roma +260, draw +300.
- Spark: matchday 1 scorers Valverde and Mbappe (Madrid 2-1 Inter), Cristante (Roma 1-1 at Fenerbahce). ESPN summary leaders: https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/summary?event=401915414 (13 Oct)

**4. Aston Villa v Fenerbahce | 19:00 | Villa Park | ESPN 401915409 | Q421**
- Villa A: Last five WLWWD, 12 scored, 9 conceded. https://www.espn.com/soccer/team/results/_/id/362 (13 Oct)
- Villa B: 16th in Premier League, 5 points from 6 games. https://www.espn.com/soccer/table/_/league/eng.1 (13 Oct)
- Fenerbahce A: Last five LDDWW, 13 scored, 3 conceded. https://www.espn.com/soccer/team/results/_/id/436 (13 Oct)
- Fenerbahce B: 4th in Super Lig, 13 points from 7 games. https://www.espn.com/soccer/table/_/league/tur.1 (13 Oct)
- Head to head: only listed meeting, Villa won 1-0 on 22 Jan 2026. https://www.espn.com/soccer/match/_/gameId/401915409 (13 Oct)
- Team news (UEFA): Villa out Maatsen; Goretzka, Hemmings, Ruggeri doubtful. Fenerbahce out Muldur.
- Line: Villa -155, Fenerbahce +400, draw +320.

**5. Bodo/Glimt v Dortmund | 19:00 | Aspmyra | ESPN 401915393 | Q418**
- Bodo A: Last five WLWLW, 9 scored, 11 conceded. https://www.espn.com/soccer/team/results/_/id/2980 (13 Oct)
- Bodo B: 2nd in Eliteserien, 53 points from 22 games. https://www.espn.com/soccer/table/_/league/nor.1 (13 Oct)
- Dortmund A: Last five WWWWD, 12 scored, 6 conceded. https://www.espn.com/soccer/team/results/_/id/124 (13 Oct)
- Dortmund B: 2nd in Bundesliga, 13 points from 5 games. https://www.espn.com/soccer/table/_/league/ger.1 (13 Oct)
- Head to head: only meeting, 2-2 draw on 10 Dec 2025. https://www.espn.com/soccer/match/_/gameId/401915393 (13 Oct)
- Team news (UEFA): Bodo out Bjortuft (suspended), Evjen, Riisnaes, Mikkelsen. Dortmund: Ryerson, Chukwumeka doubtful.
- Line: Dortmund +105, Bodo +215, draw +310.
- Spark: Guirassy scored twice in Dortmund's 3-2 v Villarreal on matchday 1. https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/summary?event=401915393 (13 Oct)

**6. Man City v PSG | 19:00 | Etihad | ESPN 401915407 | Q422**
- City A: Last five WWWWW, 16 scored, 3 conceded. https://www.espn.com/soccer/team/results/_/id/382 (13 Oct)
- City B: 1st in Premier League, 18 points, six wins from six. https://www.espn.com/soccer/table/_/league/eng.1 (13 Oct)
- PSG A: Last five LWWWW, 13 scored, 5 conceded. https://www.espn.com/soccer/team/results/_/id/160 (13 Oct)
- PSG B: 6th in Ligue 1, 11 points from 6 games. https://www.espn.com/soccer/table/_/league/fra.1 (13 Oct)
- Head to head: City lead 3-2 in the last five; PSG won the last, 4-2 on 22 Jan 2025. https://www.espn.com/soccer/match/_/gameId/401915407 (13 Oct)
- Team news (UEFA): City none listed. PSG out Mayulu.
- Line: City +115, PSG +200, draw +300. Closest big match of the night.
- Spark: Haaland scored both goals in City's 2-0 at Porto; Ferran Torres scored three and Dembele two in PSG's 6-1 v Slovan. https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/summary?event=401915407 (13 Oct)

**7. Real Betis v Porto | 19:00 | La Cartuja | ESPN 401915408 | Q417**
- Betis A: Last five WWWDW, 12 scored, 6 conceded. https://www.espn.com/soccer/team/results/_/id/244 (13 Oct)
- Betis B: 3rd in La Liga, 19 points from 8 games. https://www.espn.com/soccer/table/_/league/esp.1 (13 Oct)
- Porto A: Last five WLWWW, 11 scored, 6 conceded. https://www.espn.com/soccer/team/results/_/id/437 (13 Oct)
- Porto B: 1st in Primeira Liga, eight wins from eight. https://www.espn.com/soccer/table/_/league/por.1 (13 Oct)
- Head to head: none listed by ESPN. Matchday 1: Betis won 3-2 at Lille, Porto lost 0-2 to City.
- Team news (UEFA): Betis out Firpo; Ruibal doubtful. Porto out Bednarek (suspended), William Gomes; Sanusi doubtful.
- Line: Betis +105, Porto +240, draw +275.
- Spark: defender Marc Bartra scored twice at Lille on matchday 1. https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/summary?event=401915408 (13 Oct)

**8. Shakhtar v AEK Athens | 19:00 | Stamford Bridge, London | ESPN 401915406 | Q419**
- Shakhtar A: Drew 1-1 at PSV on matchday 1. https://www.espn.com/soccer/team/results/_/id/493 (13 Oct)
- Shakhtar B: 1st in Ukrainian league, 21 points from 8. UNVERIFIED single source (Fotmob, Tribuna, Fox Sports snippets, 10 Oct): https://www.fotmob.com/teams/9728/overview/shakhtar-donetsk
- AEK A: Last five WWDWW, 12 scored, 2 conceded. https://www.espn.com/soccer/team/results/_/id/887 (13 Oct)
- AEK B: 2nd in Greek Super League, 14 points from 6 games. https://www.espn.com/soccer/table/_/league/gre.1 (13 Oct)
- Head to head: none listed. AEK beat LASK 1-0 on matchday 1.
- Team news (UEFA): Shakhtar out Eguinaldo, Azarov; Marlon Santos doubtful. AEK out Strakosha; Varga doubtful.
- Line: AEK +165, Shakhtar +170, draw +235. Almost a coin flip.
- Note: ESPN does not carry the Ukrainian league, so Shakhtar form needs a second source before use.

**9. Slovan Bratislava v Stuttgart | 19:00 | Narodny futbalovy stadion | ESPN 401915405 | Q420**
- Slovan A: Lost 1-6 at PSG on matchday 1. https://www.espn.com/soccer/team/results/_/id/521 (13 Oct)
- Slovan B: Beat Celje 3-2 on aggregate to qualify. https://www.espn.com/soccer/team/results/_/id/521 (13 Oct; legs 19 and 26 Aug, second leg after extra time)
- Stuttgart A: Last five WWLLW, 10 scored, 5 conceded. https://www.espn.com/soccer/team/results/_/id/134 (13 Oct)
- Stuttgart B: 11th in Bundesliga, 6 points from 5 games. https://www.espn.com/soccer/table/_/league/ger.1 (13 Oct)
- Head to head: Stuttgart won the last meeting 3-1 (21 Jan 2025), lead 2-0-1. https://www.espn.com/soccer/match/_/gameId/401915405 (13 Oct)
- Team news (UEFA): Slovan none listed. Stuttgart out Nartey, Tiago Tomas, Al-Dakhil, Jaquez; Chabot, Mittelstaedt doubtful.
- Line: Stuttgart -340, Slovan +800, draw +500.
- Spark: Demirovic scored three in Stuttgart's 3-1 v Viking on matchday 1. https://site.api.espn.com/apis/site/v2/sports/soccer/uefa.champions/summary?event=401915405 (13 Oct)
- Slovan's Slovak league position is UNVERIFIED (one 365Scores snapshot says 4th, 16 points from 8).

### Thu 15 Oct, Europa League matchday 2

Team news below comes from starting11.com (https://starting11.com/europa-league, undated) unless stated. It is UNVERIFIED. UEFA has no matchday 2 team-news page for this round that I could find.

**10. Lyon v Crystal Palace | 16:45 | Groupama Stadium | ESPN 401915566 | Q425** (https://www.espn.com/soccer/match/_/gameId/401915566)
- Lyon A: Last five WDWWL, 10 scored, 4 conceded. https://www.espn.com/soccer/team/results/_/id/167 (13 Oct)
- Lyon B: 4th in Ligue 1, 11 points from 6 games. https://www.espn.com/soccer/table/_/league/fra.1 (13 Oct)
- Palace A: Last five WLWDW, 12 scored, 4 conceded. https://www.espn.com/soccer/team/results/_/id/384 (13 Oct)
- Palace B: 12th in Premier League, 7 points from 6 games. https://www.espn.com/soccer/table/_/league/eng.1 (13 Oct)
- Head to head: only listed meeting, Palace won 2-0 on 5 Aug 2023. ESPN match page (13 Oct)
- Team news: Lyon striker Openda expected out after a leg injury at Lens (L'Equipe via Get French Football News, OneFootball): https://onefootball.com/en/news/lois-openda-out-of-lyon-v-crystal-palace-in-europa-league-on-thursday-43596803 . Palace: Henderson out per WhoScored and starting11; other Palace names conflict (UNVERIFIED).
- Line: Lyon +115, Palace +215, draw +270.

**11. Salzburg v AC Milan | 16:45 | Red Bull Arena | ESPN 401915568 | Q428**
- Salzburg A: Last five WDWWD, 10 scored, 2 conceded. https://www.espn.com/soccer/team/results/_/id/2790 (13 Oct)
- Salzburg B: 2nd in Austrian Bundesliga, 18 points from 8 games. https://www.espn.com/soccer/table/_/league/aut.1 (13 Oct)
- Milan A: Last five DDLWD, 7 scored, 6 conceded. https://www.espn.com/soccer/team/results/_/id/103 (13 Oct)
- Milan B: 5th in Serie A, 12 points, unbeaten in 6. https://www.espn.com/soccer/table/_/league/ita.1 (13 Oct)
- Head to head: Milan won 4-0 (2 Nov 2022) after a 1-1 draw (6 Sep 2022). https://www.espn.com/soccer/match/_/gameId/401915568 (13 Oct)
- Matchday 1: Salzburg won 1-0 at Levski; Milan lost 0-2 at home to Benfica.
- Team news: Salzburg out Chase, Diabate; Milan Gabbia doubtful or out (sources conflict), UNVERIFIED.
- Line: Milan -125, Salzburg +300, draw +300.

**12. Torreense v Sunderland | 16:45 | Leiria | ESPN 401915575 | Q426**
- Torreense A: Won 2-1 at Lillestrom on matchday 1. https://www.espn.com/soccer/team/results/_/id/21615 (13 Oct)
- Torreense B: Won Portuguese Cup final 2-1 v Sporting, 24 May. https://www.rtp.pt/noticias/desporto/torreense-e-o-primeiro-secundario-a-conquistar-a-taca-de-portugal_v1743251 and https://www.beinsports.com/en-us/soccer/articles/torreense-makes-history-by-winning-the-taca-de-portugal-against-sporting-2026-05-25 (25 May). First second-tier winner; the game went to extra time (VERIFIED, 4 outlets in search).
- Sunderland A: Last five WLWLL, 5 scored, 9 conceded. https://www.espn.com/soccer/team/results/_/id/366 (13 Oct)
- Sunderland B: 17th in Premier League, 4 points from 6 games. https://www.espn.com/soccer/table/_/league/eng.1 (13 Oct)
- Head to head: none. Matchday 1: Sunderland beat AZ 1-0.
- Torreense league position UNVERIFIED (one snapshot: 15th, 6 points from 7 in Liga Portugal 2); ESPN does not carry that league.
- Team news: Torreense Jatta suspended; Sunderland several out, Brobbey among them (starting11), UNVERIFIED.
- Line: Sunderland -255, Torreense +600, draw +425.

**13. Union Saint-Gilloise v Real Sociedad | 16:45 | Den Dreef | ESPN 401915574 | Q429**
- Union A: Last five WWWWD, 14 scored, 3 conceded. https://www.espn.com/soccer/team/results/_/id/5807 (13 Oct)
- Union B: 4th in Belgian Pro League, 20 points from 8 games. https://www.espn.com/soccer/table/_/league/bel.1 (13 Oct)
- Sociedad A: Last five WLLWW, 10 scored, 11 conceded. https://www.espn.com/soccer/team/results/_/id/89 (13 Oct)
- Sociedad B: 6th in La Liga, 13 points from 8 games. https://www.espn.com/soccer/table/_/league/esp.1 (13 Oct)
- Head to head: none listed. Matchday 1: Union won 3-0 at Plzen, Sociedad lost 1-2 to Bournemouth.
- Team news: Union Florucz suspended; Sociedad Aramburu, Odriozola out (starting11), UNVERIFIED.
- Line: Union +140, Sociedad +180, draw +275.

**14. Benfica v Celtic | 19:00 | Estadio da Luz | ESPN 401915562 | Q433**
- Benfica A: Last five WWWLW, 12 scored, 4 conceded. https://www.espn.com/soccer/team/results/_/id/1929 (13 Oct)
- Benfica B: 2nd in Primeira Liga, 19 points from 8 games. https://www.espn.com/soccer/table/_/league/por.1 (13 Oct)
- Celtic A: Last five WLLLW, 4 scored, 7 conceded. https://www.espn.com/soccer/team/results/_/id/256 (13 Oct)
- Celtic B: 1st in Scottish Premiership, 21 points from 8 games. https://www.espn.com/soccer/table/_/league/sco.1 (13 Oct)
- Head to head: Benfica won 3 of last 5 (1 draw); last one Benfica 2-1, 20 Nov 2012. https://www.espn.com/soccer/match/_/gameId/401915562 (13 Oct)
- Matchday 1: Benfica won 2-0 at Milan; Celtic lost 1-3 at home to Ferencvaros. Celtic's form includes a 0-3 League Cup loss at Rangers and 0-1 league loss to Rangers.
- Team news: Celtic Hyun-jun, Johnston, Mheuka out (starting11), UNVERIFIED.
- Line: Benfica -390, Celtic +900, draw +550.

**15. Bournemouth v Sturm Graz | 19:00 | Vitality Stadium | ESPN 401915571 | Q427**
- Bournemouth A: Last five WDWLL, 9 scored, 9 conceded. https://www.espn.com/soccer/team/results/_/id/349 (13 Oct)
- Bournemouth B: 18th in Premier League, 3 points, no wins from 6. https://www.espn.com/soccer/table/_/league/eng.1 (13 Oct)
- Sturm A: Last five LWDLW, 5 scored, 7 conceded. https://www.espn.com/soccer/team/results/_/id/3746 (13 Oct)
- Sturm B: 4th in Austrian Bundesliga, 14 points from 8 games. https://www.espn.com/soccer/table/_/league/aut.1 (13 Oct)
- Head to head: none. Matchday 1: Bournemouth won 2-1 at Sociedad, Sturm drew 0-0 with Rennes. Bournemouth lost 1-5 at Chelsea on 10 Oct.
- Team news: not gathered, UNVERIFIED.
- Line: Bournemouth -525, Sturm +1200, draw +650.

**16. Celta Vigo v Juventus | 19:00 | Balaidos | ESPN 401915560 | Q431**
- Celta A: Last five DDLWD, 7 scored, 3 conceded. https://www.espn.com/soccer/team/results/_/id/85 (13 Oct)
- Celta B: 9th in La Liga, 8 points from 8 games, five draws. https://www.espn.com/soccer/table/_/league/esp.1 (13 Oct)
- Juventus A: Last five DLWWD, 11 scored, 5 conceded. https://www.espn.com/soccer/team/results/_/id/111 (13 Oct)
- Juventus B: 6th in Serie A, 11 points from 6 games. https://www.espn.com/soccer/table/_/league/ita.1 (13 Oct)
- Head to head: none listed. Matchday 1: Celta lost 0-1 at Omonia, Juventus beat NEC 5-0.
- Team news: Juventus Boga, Ekhator, Grabara out; Cabal doubtful (starting11), UNVERIFIED.
- Line: Juventus +115, Celta +250, draw +240.

**17. Hoffenheim v Besiktas | 19:00 | PreZero Arena | ESPN 401915563 | Q432**
- Hoffenheim A: Last five LWLLL, 7 scored, 12 conceded. https://www.espn.com/soccer/team/results/_/id/7911 (13 Oct)
- Hoffenheim B: 17th in Bundesliga, 3 points from 5 games. https://www.espn.com/soccer/table/_/league/ger.1 (13 Oct)
- Besiktas A: Last five WWWLW, 13 scored, 6 conceded. https://www.espn.com/soccer/team/results/_/id/1895 (13 Oct)
- Besiktas B: 2nd in Super Lig, 15 points from 7 games. https://www.espn.com/soccer/table/_/league/tur.1 (13 Oct)
- Head to head: none listed. Matchday 1: Hoffenheim lost 0-2 at OFI Crete, Besiktas beat Marseille 4-1.
- Team news: Hoffenheim Bernardo suspended; Besiktas Keles, Rashica out (starting11), UNVERIFIED.
- Line: Hoffenheim -105, Besiktas +245, draw +310.

---

## 3. Ballon d'Or context

### 3.1 Basics (VERIFIED)

- Ceremony: Monday 26 Oct 2026, London Palladium, the 70th edition and the first held outside Paris. Sources: ESPN 2 Oct https://www.espn.com/soccer/story/_/id/49867974/2026-ballon-dor-full-mens-women-shortlists-host-city-change-vozinha-more ; Wikipedia https://en.wikipedia.org/wiki/2026_Ballon_d%27Or ; Racing Post 1 Oct. Your "26 Oct London" report is right. Start time is UNVERIFIED: Coinspeaker (7 Oct) says 8 pm "BST", but London is on GMT from 25 Oct, so 8 pm local would be 20:00 UTC.
- Shortlist: 30 men, announced on a Tuesday (8 Sep per CryptoSlate and Statsniper; ESPN says "on Tuesday"). Includes Kane, Yamal, Mbappe, Messi, Rodri, Olise, Dembele, Haaland, Bellingham, Vinicius, Vitinha. Voters: 100 journalists (ESPN). Voting closed Mon 28 Sep (World Soccer Talk 10 Oct, Coinspeaker 7 Oct, Legit.ng; Racing Post 1 Oct says voting closed on a Monday).
- Outcome market (question 391, France Football as source, resolves by 5 Nov 23:59 UTC) lists Kane, Yamal, Mbappe, Bellingham, Dembele, Haaland, Messi and "Other". Rodri and Olise presumably sit inside "Other". (outcomeMeta, 13 Oct)
- Their seasons (2 outlets each): Kane 61 goals in 51 Bayern games, 36 league goals, European Golden Shoe, Bundesliga and DFB-Pokal (OLBG 13 Oct https://www.olbg.com/news/ballon-dor-2026-winner-odds-harry-kane-moves-back-ahead-lamine-yamal ; Coinspeaker 7 Oct https://www.coinspeaker.com/polymarket-ballon-dor-odds-kane-yamal). Yamal won La Liga, played the whole World Cup final that Spain won, but Barcelona lost the Champions League quarter-final (same two sources). England lost the World Cup semi-final to Argentina (Racing Post 1 Oct).

### 3.2 What the Outcome price actually did (public candle data, VERIFIED)

Source: `POST https://api.hyperliquid.xyz/info {"type":"candleSnapshot","req":{"coin":"#86570","interval":"1h","startTime":<ms>,"endTime":<ms>}}`. Kane Yes = `#86570`, Yamal Yes = `#86590`. Pulled 13 Oct. Prices are the chance (0.50 = 50%). Each value is the hourly candle close for the hour starting at the time shown, except the 5-minute rows.

| When (UTC) | Kane | Yamal |
|---|---|---|
| 5 Oct 12:00 | 48.6% | 43.1% |
| 6 Oct 12:00 | 47.8% | 46.0% |
| 8 Oct 00:00 | 48.9% | 44.2% |
| 8 Oct 18:00 | 51.8% to 55.6% in the hour | 40.4% to 39.2% |
| 9 Oct 17:30 | 55.5% | 37.4% |
| 9 Oct 17:50 (jump) | 63.5% (5-min bars 17:40 to 17:50, about 30 trades) | 24.5% to 29.3% (24 trades in the 17:45 bar) |
| 10 Oct 00:00 | 60.6% | 32.7% |
| 11 Oct 00:00 | 64.3% | 29.1% |
| 12 Oct 12:00 | 66.7% | 28.4% |
| 13 Oct 03:30 | 64.1% | about 31% |
| 13 Oct 03:45 (dip) | 62.1% (9 trades) | about 32% |
| 13 Oct about 10:30 | 61.7% | about 31% |

- Before 11 Oct the market was thin: most 5-minute bars on 9 Oct had zero trades, so a handful of trades moved the price. On 11 Oct activity jumped (candle volume 305,678 and 8,747 trades that day) and 12 Oct had volume 411,027 and 10,998 trades. So the 64% to 66% level held up with real volume.
- Your numbers check out: Kane 5 Oct close 49.5%, 12 Oct close 65.8%; Yamal 43.1% to 28.4%.
- The same jump shows on Polymarket: CryptoSlate's 10 Oct 01:59 UTC summary says Kane up 8 points and Yamal down 7.3 in one day (https://cryptoslate.com/predictions/market/ballon-dor-winner-2026/). Polymarket on 13 Oct 09:47 UTC: Kane 61.9%, Yamal 31.4% (same page).

### 3.3 Why did Kane rise and Yamal fall? (dated evidence)

1. 29 Aug to 8 Sep: Kane was the clear favourite on Polymarket (65.5% on 29 Aug, 63.6% on 8 Sep, Yamal 14% to 15%). Coinspeaker 7 Oct and CryptoSlate. VERIFIED, 2 sources.
2. 26 Sep: England lost 2-3 to Spain at Wembley. Yamal scored in the 2nd minute and Kane scored a header. https://www.espn.com/soccer/report/_/gameId/401861066 . VERIFIED.
3. 28 Sep: voting closed. Markets flipped to Yamal: bookmakers cut him from 2-1 to 5-6 and some to 4-9 in the week, with Racing Post blaming "exit polls clearly promising" for Yamal but naming no source (1 Oct, https://www.racingpost.com/sport/football-tips/2026-ballon-dor-betting-harry-kane-out-to-6-4-after-big-gamble-on-lamine-yamal-apYB73d5z9Mi/). VERIFIED that odds moved; the reason is UNVERIFIED.
4. 26 Sep to 6 Oct: Kane scored 6 goals in 4 England games (1 v Spain, 1 at Czechia on 29 Sep, 2 in the 7-0 at Croatia on 3 Oct, 2 in the 3-0 v Czechia on 6 Oct). Yamal scored 4 in Spain's first 3 games (1 v England, 2 v Croatia on 29 Sep, 1 v Czechia on 3 Oct) but nothing in the 2-1 win at Croatia on 6 Oct. ESPN match pages (scorers from ESPN summary data): https://www.espn.com/soccer/report/_/gameId/401861066 (England 2-3 Spain), https://www.espn.com/soccer/report/_/gameId/401861092 (Czechia 0-2 England), https://www.espn.com/soccer/report/_/gameId/401861113 (Croatia 0-7 England), https://www.espn.com/soccer/report/_/gameId/401861142 (England 3-0 Czechia), https://www.espn.com/soccer/report/_/gameId/401861084 (Spain 4-1 Croatia), https://www.espn.com/soccer/report/_/gameId/401861118 (Spain 3-1 Czechia), https://www.espn.com/soccer/report/_/gameId/401861137 (Croatia 1-2 Spain). The 6 Oct game was Kane's record-equalling 125th England cap: https://www.aljazeera.com/sports/2026/10/6/kane-equals-england-record-and-scores-twice-in-3-0-win-against-czechia . VERIFIED.
5. 5 to 7 Oct, the market was level: Kalshi 5 Oct Kane 51%, Yamal 47%; Polymarket 7 Oct Kane 48%, Yamal 43.5% (Coinspeaker 7 Oct). Oddschecker 5 Oct had Yamal 10/11 and Kane 6/5 (seen via search; page blocked, UNVERIFIED wording).
6. 6 to 9 Oct: rumour flow. A UK account (The Touchline) said only Yamal and Kane are in contention, order not given, and a Canal+ journalist called it plausible (French Football Weekly, 9 Oct: https://frenchfootballweekly.com/2026/10/09/ballon-dor-2026-leaks-are-confirmed-the-identity-of-the-first-two-revealed/ ). On 9 Oct (updated 16:42 UTC) a Spanish Yahoo piece reported an "alleged" leaked points list with Yamal first on 670, Messi 546, Mbappe 401, Kane 342; no source, no confirmation (https://es-us.noticias.yahoo.com/deportes/filtr%C3%B3-lista-ganador-bal%C3%B3n-oro-164200131.html ). The price moved AGAINST Yamal an hour later, so traders probably did not believe that list. That inference is UNVERIFIED. France Football's stance in past years is that only its head knows the result (World Soccer Talk, 22 Sep 2025).
7. 9 Oct 17:45 UTC is the jump. I found NO named, reliable report at that time that says Kane is winning. Cause: UNVERIFIED. What can be said: it happened on Outcome and Polymarket the same day, after four days of Kane scoring for England, and bookmakers followed.
8. 10 to 13 Oct, bookmakers confirm the swap: World Soccer Talk (updated 10 Oct), quoting Oddschecker, calls Kane "the clear favorite" at 5/4 against Yamal 2/1 in its text and 4/5 against 6/5 in its table (the page contradicts itself) https://worldsoccertalk.com/news/lamine-yamals-2026-ballon-dor-hopes-take-major-hit-as-new-favorite-takes-over/ . OLBG 13 Oct 07:00: bet365 Kane 1/2, Yamal 2/1; at the start of October it was Yamal 1/2, Kane 6/4. A bookmaker analyst is quoted: a move from 6/4 to 1/2 "with votes counted" means something. No event named. VERIFIED that prices moved; reason UNVERIFIED.
9. 10 to 12 Oct: SportBible 11 Oct says Kane's chances got a boost even though he did not score for Bayern (2-2 at Augsburg on 10 Oct) https://www.sportbible.com/football/football-news/harry-kane-bayern-munich-ballon-dor-bundesliga-augsburg-562516-20261011 . Bayern president Hainer said in a Bild video (12 Oct) he would pick Kane over Olise (headline via Orange, not opened, UNVERIFIED detail). Both are weak signals.
10. 13 Oct dip: Kane fell from 64.1% to 62.1% at 03:45 UTC and settled at 62% to 63%, Yamal up 1 to 3 points. I found no news for it, and bet365 was unchanged at 07:00 UTC. Most likely a large sell in a thin overnight book. UNVERIFIED.

Safe on-screen wording: "Voting closed 28 Sep", "100 journalists vote", "Kane scored 6 in 4 England games", "Winner revealed 26 Oct". Unsafe: "leak", "confirmed", "Kane has won".

Not opened (blocked or unreachable): Oddschecker 5 Oct (403), bookies.com 12 Oct (connection refused), Prediction News and Daily Sports pieces (403), X posts. Numbers from those come only through search snippets.

---

## 4. Fed context (5 lines)

1. Last decision, Wed 16 Sep 2026: the FOMC RAISED the target range by 0.25 point to 3.75% to 4.00%, vote 12-0, and said "Inflation remains elevated." https://www.federalreserve.gov/newsevents/pressreleases/monetary20260916a.htm (13 Oct). Chair is Kevin Warsh, sworn in 22 May 2026 (Fed release listing: https://fraser.stlouisfed.org/title/press-releases-board-governors-federal-reserve-system-9237/kevin-warsh-takes-oath-office-chairman-a-member-board-governors-federal-reserve-system-federal-open-market-committee-unanimously-selects-warsh-chairman-728506 ).
2. Why: August CPI rose 0.4% on the month and 3.4% on the year, core 2.4% (BLS release 11 Sep, https://www.bls.gov/cpi/ , 13 Oct). September CPI lands Wed 14 Oct, 12:30 UTC. Forecasts: Cleveland Fed nowcast 3.60% y/y (7 Oct), street about 3.7%, core about 2.4% (https://admiralmarkets.com/analytics/traders-blog/us-cpi-preview-september-2026-forecasts-and-the-core-cpi-outlook , 8 Oct).
3. Next meeting is Tue 27 to Wed 28 Oct, no new projections. The statement comes Wed 28 Oct at 18:00 UTC (2:00 pm EDT, same release time as 16 Sep). https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm (13 Oct); Outcome's two Fed questions (289, 331) both say `scheduledDecision:20261028-1800`.
4. Market view: the market-implied hike chance for 28 Oct was 19.4% on 7 Oct (CME FedWatch in other coverage), down from about 50.9% a week earlier, after the 2 Oct jobs report (+29,000 vs about 90,000 expected, unemployment 4.2%). Williams (29 Sep): "no need for urgency". Bowman (1 Oct): no "urgent need for further action". https://247wallst.com/investing/2026/10/07/october-rate-hike-odds-just-fell-from-51-to-19-in-one-week/ . Outcome's 81% hold and 18% hike (your numbers, 13 Oct) match.
5. After October: about 70% chance of a hike by the 9 Dec meeting (247wallst, 7 Oct) and about 81% for at least one by then (Admiral Markets, citing CME, 5 Oct). Median projection for end-2026 is 4.1%, one more hike. Waller said hikes "need not come at back-to-back meetings". A hot core CPI on 14 Oct is the main threat to the hold price. Treat the percentages as snapshots, they will move after CPI.

## 5. Anthropic IPO context (5 lines)

1. Company-confirmed: on Mon 1 Jun 2026 Anthropic said it had confidentially submitted a draft S-1 to the SEC (a Rule 135 notice, no share count or price). Reported by several outlets that day, for example https://www.gpb.org/news/2026/06/01/ai-giant-anthropic-files-paperwork-for-ipo and https://www.michiganpublic.org/2026-06-01/ai-giant-anthropic-prepares-to-sell-stock-to-the-public-files-preliminary-ipo-paperwork . Last private round: $65B at $965B post-money (May). Anthropic's newsroom index (checked 13 Oct, latest post 8 Oct) shows no later IPO post.
2. Timing has slipped three times in reports: Reuters 4 to 5 Sep (marketing mid-Oct at the earliest, list before the Nov midterms); WSJ 18 Sep (pushed to November so Q3 results can be shown; cited second-hand by tastytrade); Bloomberg 1 Oct (roadshow could start as soon as the week of 9 Nov, trading before Thanksgiving 26 Nov, still by end of 2026, plans can change). https://tastytrade.com/learn/markets/industry/anthropic-ipo/ ; https://www.implicator.ai/anthropic-could-start-ipo-roadshow-week-of-nov-9-putting-debut-before-thanksgiving/ (2 Oct). Secondary sources, the Bloomberg original is the reference.
3. Milestones in your window, all REPORTED: investor day Wed 14 Oct at the San Francisco HQ (Bloomberg 1 Oct; Anthropic declined to comment). No public S-1 on EDGAR as of the latest coverage I saw (headline only, page not opened: https://financefeeds.com/anthropics-14-october-investor-day-nears-but-its-s-1-still-isnt-public-the-ipo-timeline-explained/ ). A public filing must precede the roadshow by 15 days, so about 23 to 25 Oct if 9 Nov holds (my arithmetic). No pricing date, price range, ticker or exchange is announced (Nasdaq is the most-reported venue).
4. Valuation, REPORTED and not from Anthropic: investors consider $1.8T to $2T fair (Bloomberg via implicator.ai, 2 Oct). A raise of about $100B appears only in secondary coverage: UNVERIFIED. Outcome's first-day market cap ladder runs $1.5T to $2.5T with listing deadlines 31 Dec 2026 and 1 Jan 2027 (outcomeMeta, 13 Oct).
5. How to word it: "reported", never "will list on". Outcome's "IPO confirmed by 31 Oct" last traded at 0.04, and the 30 Nov version is your 68%, which fits the reported 9 Nov roadshow and pre-26 Nov debut. The exact meaning of "confirmed" (public S-1, pricing, or first trade) is not in the API: UNVERIFIED, read the rules on outcome.xyz before any post.

---

## 6. Open items and caveats

- UNVERIFIED: cause of the 9 Oct jump and the 13 Oct dip; Ballon d'Or ceremony start time; Shakhtar, Slovan and Torreense league positions; all Europa League team news except Lyon's Openda; Real Madrid, Roma and Milan injury conflicts; single-source NBA opening-night stories.
- Data gaps: ESPN has no Ukrainian, Slovak or Portuguese second-tier data, so those three sides use cup, qualifier and matchday-1 facts instead of league form.
- Whatever the source, tables and forms change after the 13 Oct games and the weekend. Re-pull on the day: scoreboard JSON above plus `.../all/teams/{id}/schedule`.
- Safety: no financial advice, no "will win" claims. Prices are "the market's chance". India rules and platform disclosure rules are in 03-platform-rules.md.
- Tool notes: the Windows console needs `PYTHONIOENCODING=utf-8` for ESPN names with accents.
