<!-- Boss-kit copy of the 7 Oct 2026 handoff (history; newer research corrected some claims). The partner who ran that session is called "the partner" here. -->

# Footage sourcing, by vertical

The one sentence version: **the terminology differs per sport, and using the wrong word returns nothing.** Football says "scene pack". Basketball says "logoless". Combat sports has neither and does not need one.

---

## Football

**Scene packs are the answer and they are the best source of any vertical.** Pre-cut, colour graded, watermark free 4K clip bundles of a single player or moment, usually distributed as Google Drive or Mega folders by dedicated accounts.

This works for football and not for other sports because broadcast football is visually uniform, widely mirrored, and a dedicated 4K upscaling scene grew up around it.

Risk tiering for football footage is in `01-platform-rules.md`. The short version: **current week Premier League, La Liga and Champions League never goes on YouTube Shorts**, because Content ID there is automated.

A football-only YouTube channel list was compiled in the session and lives in `Vision Clipping - Format and Sourcing Research.docx`, which also contains eight football formats, eight music formats, a player roster and scene pack sources.

---

## Basketball

### The word is "logoless", not "scene pack"

Searching "NBA scene pack" returns almost nothing. The general purpose scene pack infrastructure, including scenepacks.com with its 160,000 member Discord, is film, TV, anime and games. Its only sport is UFC. Zero basketball.

Basketball instead runs a **YouTube native** ecosystem where packs are published as 10 to 35 minute videos you download with yt-dlp, not as Drive folders.

### Why the ecosystem exists, which is the genuinely useful part

**Broadcasters deliberately moved the NBA score bug to bottom centre so that it survives a 9:16 crop.** This is documented, not inferred. Networks did it specifically so their graphics stay visible in footage cropped for vertical social video.

So a centre crop, the standard reframe, is the one crop that **guarantees** you keep the bug. Football's top corner bugs crop away cleanly. Basketball's do not. That single fact is why logoless packs exist: the pack maker removes the bug once so nobody else has to.

Compounding problems specific to basketball:
- **Three score bug designs in circulation.** The 2025-26 rights deal split games across ESPN/ABC, NBC/Peacock and Amazon Prime Video, with TNT out. Mixing sources in one edit means mixing bug styles plus legacy TNT footage.
- **The wide tracking shot.** Basketball's main camera is a wide side court angle. Cropping 16:9 to 9:16 discards about 44 percent of the width, and the ball handler frequently ends up outside the crop. This forces **keyframed pan and scan**, two or three keyframes per clip. A single static crop does not work. Football tolerates one because its iso cams are tighter.

### Active logoless channels

| Channel | Covers | Note |
|---|---|---|
 | [TwizzyLogoless](https://www.youtube.com/@TwizzyLogoless) | NBA, NFL, college | 53.4k subs. The anchor of the scene. 15 to 35 minute packs. [116 video NBA playlist](https://www.youtube.com/playlist?list=PLI9YQjFHMkS2ZuJObmmkIhZ0wBI8acQ5L) |
| [4K Hoops](https://www.youtube.com/@hoops_highlights_4k) | NBA only | Full 2026 Finals packs |
| [5star twixtors](https://www.youtube.com/@5startwixtors) | NBA, UFC, boxing | Only channel stating **no watermark** in titles as standard. Packs ship **pre time remapped**, so CapCut users get AE grade slow motion |
| [crawfrd2K](https://www.youtube.com/@crawfrd2K) | Classic era | Jordan, Kobe, Iverson, Reggie Miller. Best vintage source found |
| [ktostro index](https://www.youtube.com/playlist?list=PLdA2mVkbLz8WeAJullWOK1jHWfZsSyt5x) | Everything | **Start here.** 49 packs sorted by player surname, hand built across many channels |
| [DXO'S SCENEPACKS](https://payhip.com/hoopswithdxo/collection/dxos-scenepacks) | Modern and classic | The only real NBA pack store. Most items free, bundles 1 to 3 USD |

### Raw footage when no pack exists
- [NBA official](https://www.youtube.com/@NBA). Daily. Their player hype reels are effectively free scene packs. Also hosts full classic games.
- **archive.org full games, direct MP4.** Roughly 5GB per game, higher bitrate than any YouTube rip. Example: [Bulls sweep the Bad Boy Pistons 1991](https://archive.org/details/youtube-395kV56gsdA) is a 4,997MB file.
- [Airball Clips](https://www.youtube.com/@airballclips). 555k subs, daily. Open runs, private gym runs, bag work. **Non broadcast angles, so no score bug at all.**
- [Home Team Hoops](https://www.youtube.com/@HomeTeamHoops). The real streetball source. Drew League, pro am. The official Drew League channel has been idle a year.

### Avoid
**Ballislife** actively Content ID claims. Their channel description states the watermark must stay visible, you must wait 36 hours, and "we will claim our video".

Dead: `discord.gg/twizzylogoless` returns Unknown Invite. `t.me/nba_clips` was hijacked. House of Highlights is almost entirely MLB in offseason. `@HoopCentral` has not uploaded to YouTube in four years.

---

## Fight (UFC and boxing)

### There is no scene pack ecosystem, and it does not matter

What exists is small, amateur and mostly **Topaz upscaled from 1080p**, so the advertised 4K is interpolated. The better packs sit behind Discord invite walls reachable only from a TikTok bio.

It does not matter, because **the promotions give the footage away**. Serious fight editors rip from official sources and grade it themselves. Copy that workflow.

| Source | What it gives | Quality |
|---|---|---|
| [UFC](https://www.youtube.com/@ufc) | Full fights, full post fight press conferences, free fight marathons, vertical KO shorts. Multiple uploads daily. **The single best source and wildly underused by editors.** | up to 4K |
| [ONE Championship](https://www.youtube.com/@ONEChampionship) | Huge volumes of full fights free. Muay Thai and kickboxing KOs nobody in the UFC edit space touches. **The genuine untapped lane.** | 1080p to 4K |
| [Top Rank Boxing](https://www.youtube.com/@toprank) | Bob Arum's library. Decades of boxing, HD remasters of 80s and 90s material | HD remaster |
| [Matchroom Boxing](https://www.youtube.com/@MatchroomBoxing) | Best source for press conference and weigh in footage, because Eddie Hearn posts everything. Full prelims free | 1080p+ |
| [Anatomy of a Fighter](https://www.youtube.com/@AnatomyofaFighter) | 860k subs, 723 videos, 207M views. **Already cinematically shot and graded.** This is the look scene packs try to fake | cinematic |
| [ufc-ripper](https://github.com/m4heshd/ufc-ripper) | The entire UFC back catalogue including PRIDE, WEC, Strikeforce at native resolution. Needs a paid Fight Pass subscription. Actively maintained | native |
| [@janis1x](https://www.youtube.com/@janis1x) | 4K 60fps fighter clip packs, Topaz upscaled, made explicitly for editors. The most practical single channel | upscaled |

### archive.org, verified file by file
- [best-of-ufc](https://archive.org/details/best-of-ufc). **27 official UFC highlight compilations**, 720p, 6 to 16 minutes each. The closest thing to a real UFC scene pack that exists.
- [UFC 1 to 10 complete](https://archive.org/details/ufc.1-10.-webrip.-h-264-wiz). 720p, roughly 2GB each.
- [Tyson vs Buster Douglas](https://archive.org/details/tyson-vs-douglas). 1,491MB, 59 minutes. Highest bitrate Tyson file found.
- [Thrilla in Manila](https://archive.org/details/muhammad-ali-vs-joe-frazier-iii-thrilla-in-manila-hd-production). 720p, best looking Ali file on the platform.

### archive.org traps
- The item **UFC229** is titled "Ultra HD" and is actually 1280 x 720. Do not build a 4K edit on it.
- The item titled **"MIKE TYSON BOXING"** is a 90 second **video game trailer** at 320 x 240, and it ranks near the top of every Tyson search.
- **Search by fighter name, never by "boxing".** The generic search is polluted with unrelated VHS rips.
- **"Clips For Edits" on YouTube is a football channel**, not combat sports, despite ranking for every fight clip search.

---

## Military

- **DVIDS** (dvidshub.net). 1.8M+ assets, searchable by branch, mostly public domain. The backbone of the military page. There is a **free API** at api.dvidshub.net/docs with separate endpoints for assets, video, podcasts and live content, so the footage pull can be automated rather than browsed. The **news RSS** at dvidshub.net/rss/news is confirmed working, with per-unit feeds available.
- Official branch accounts: `@USArmy`, `@USNavy` (carrier operations is the best performing visual material in the niche), `@usairforce`, `@USMC`, `@SpaceForceDoD`. All published to be reshared.
- **NARA** and the aggregator front end at nara.getarchive.net, which searches NARA and DVIDS together.
- **archive.org bulk collections**, downloadable whole: [Military_Archive_me](https://archive.org/details/Military_Archive_me), 378 files, 37.4GB, with helmet cam POV. [ukraine-war-combat-footage](https://archive.org/details/ukraine-war-combat-footage), 600+ videos. Both were uploaded before generative video was viable, so they are **provably pre-AI**.
- **Airshow calendars** are the predictable content lane. MILAVIA, the Blue Angels official schedule, AirshowStuff. Airshows produce the best free aviation footage of the year on known dates.
- **Raw UGC texture**, which is what the aura farming angle actually needs: [Funker530](https://funker530.com/video/archive-3), [WarLeaks](https://www.youtube.com/@WarLeaker) (2.8M subs, wall to wall helmet cam), [Combat Obscura](https://tubitv.com/movies/685512/combat-obscura) free on Tubi, and Telegram at [@WarArchive_ua](https://t.me/WarArchive_ua).

**The tension to decide consciously:** DVIDS and NARA are the provably real sources but read as archival and institutional. The sources with the right intimate helmet cam texture are exactly where deepfakes land first. Pick which way you would rather be wrong.

---

## Rap and UK scene

42 of the 152 sources in `data/monitoring-sources.json` are tagged `UK`. Filter on that tag.

The headline findings:
- **There is no UK equivalent of Kurrco.** The space is fragmented across a dozen mid-size accounts. Closest single follow is `@UKRapDaily`, then `@UKDrillNews_` and `@UK_Drill_News`. You need three or four, not one.
- **Instagram is stronger than X for this scene.** `@ukmusicmedia`, `@ukrapdaily_`, `@lyricalmindsuk`.
- **r/ukdrill, 233k members, is frequently first**, ahead of the aggregator accounts.
- **Two under-followed platforms uploading every 12 hours:** P110 (596k, the only reliable non-London pipeline) and BL@CKBOX (221k). Everyone watches GRM Daily and sleeps on these.
- **Two fixed windows** worth building a schedule around: Official Charts drop **Friday 4pm to 5.45pm UK**, and Kenny Allstar's Rap Show on 1Xtra is **Saturday 9 to 11pm** since the April 2026 slot move. That is the biggest premiere and playlist-add slot in UK rap.

**Handle traps, all verified:** `@drill_uk` is a disability research programme. `@MadAboutBars` is restaurant reviews. `@TheColdroom` is a Dubai t-shirt brand. `@ComplexUK` without the underscore is a random three-follower account; the real one is `@complex_uk`. `@nosignalradio` is unrelated; the real one is `@theresnosignall` with a double L.

**Dead or paused:** SBTV (no upload since December 2025), Rated Awards (nothing since 2022), Wireless Festival (cancelled for 2026), Crack Magazine's X account (archived).
