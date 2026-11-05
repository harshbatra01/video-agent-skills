# TikTok no-creator reference posts found by agent C (14 Oct 2026)

Window 1 Sep to 14 Oct 2026 (posts before 1 Sep are marked AUG). Bar: 100K+ views, or 5x followers for a small page. Everything below was added with `ref.py add` (media in raw\26\videos, stills in raw\26\frames, rows in raw\26\data\refs.jsonl). Face check: contact sheets of cover + 4 stills per post, read by eye.

Totals: 148 collected by me, 110 clean (nobody presenting on camera, in niche). Stopped on request before the last 11 planned posts.

| niche | collected | clean |
|---|---|---|
| football_clip | 22 | 20 |
| football_edit | 20 | 20 |
| football_meme | 16 | 6 |
| football_stats | 9 | 4 |
| money_trading | 22 | 18 |
| crypto | 16 | 12 |
| betting_meme | 14 | 9 |
| clipping | 21 | 21 |
| slideshow | 8 | 0 |

## Routes that worked

- Earlier research dumps on disk (research\raw\25\data\tt_s_*.txt TikTok search lists, raw\22, raw\23 socialpruf lists, studio\refs): the main source of post ids. The post date is the id shifted right 32 bits, so no call is needed to screen by date.
- r.jina.ai creator embed (tiktok.com/embed/@handle): followers plus the latest 10 to 13 posts with views for non-verified accounts (about 100 handles, one call per 11 s). It answered 403 AbuseAlleviationError until 22:46 UTC on 13 Oct, then worked. Photo-mode posts show as items with an empty playAddr.
- tikwm single-video API through ref.py add: exact stats and media. Slow (10 to 60 s per post) because many sessions shared it and a heavy ffmpeg job ran; no tikwm search or user endpoint was touched.
- socialpruf.com public page (one GET per handle): followers plus 12-month top 20 for tracked brand pages (kalshi.sports, novig, underdogfantasy). Most small pages are not tracked.
- WebSearch with allowed_domains tiktok.com: returns tiktok.com video links, but mostly 2023 to 2025 posts and /discover pages; only caption-matched queries found Oct 2026 posts. The shared budget of 200 searches per turn ran out mid-task, so no more searches were possible.
- Did not work: WebFetch on tiktok.com (connection refused, blocked on this PC), urlebird (HTTP 403, not pursued), one YouTube Shorts run with qs.py (cross-posts did not map to TikTok handles).

## Ids that fail the bar, the dates or the no-creator rule

- Below the bar (under 100K and under 5x followers): none. One post is under 100K but passes as a small page: 7695723370737978632 (sxmvoidedit, 88K on 597 followers).
- Posted before 1 Sep (AUG, a few kept on purpose): 7670662930475584801 (@nayahvoetbal12, 08-05); 7678891272995622174 (@ireogunz, 08-28); 7675911670694251797 (@rugengine.sol, 08-20); 7679250991946026254 (@kingdukeclips, 08-29); 7670757989791403286 (@sftboox, 08-06)
- Creator or actor on camera, drop these (29): @carmplus: 7694638438028430625, 7694362753892420897; @ramo_akh: 7695806028138482974; @wolusfcb: 7693643427333836064; @ireogunz: 7678891272995622174; @young.kippa: 7682495716161375510, 7686988716648320289; @theutdtrey: 7693295496282066196; @habibx03: 7690663016953613590, 7693617531113852182, 7686254205375384864; @alsoclokus: 7695544440764501279; @footballmaster3333: 7683291811258944801, 7683694090290040097, 7682845033011236128, 7696089226600877344; @billsricci: 7684949786612550919, 7688352903165267208; @nqcaylon: 7691761456357854478; @tjrackss: 7694042579502943501; @crypto.lucho: 7693954189197659410; @binance: 7693075422472375566; @elcosto67: 7696000259381562656; @safia.ali60: 7695148066399161607; @kalshi.sports: 7689919499306372366; @outjuggin0078: 7695838401303465229; @talkingfantasysprts: 7691149997533875470; @tgclips94: 7694510777541086477; @pandasupr3m4cy: 7691841627790298398
- Not football, only useful as a bar-chart-race look: 7680984511143841037 (@hai02a, phone brands)
- Labelled slideshow but they are videos made from stills, not photo-mode (8): 7682561462421736734 (@drakostash); 7694008809492139272 (@clazzed.ftbl); 7670757989791403286 (@sftboox); 7683181264832171297 (@dtfootylens); 7685028189340503310 (@dtkd.alan); 7685860476600716565 (@kolobok3098); 7682698669669289230 (@motivational.moneytok); 7696129211005783318 (@ntlgoat7z). Suggested labels are in their lines below.
- Better under another label: 7695468822941224213 (@realnetralll): realnetralll LFC rooster meme graphic: football_meme rather than football_clip; 7696253943462038806 (@iduate): iduate: 10 s POV text meme, better football_meme than football_clip; 7685694158350077204 (@walefx_): walefx_ is a real photo-mode post (5 slides): count as slideshow; 7695231802327223583 (@novig): novig: photo-mode stats slideshow (3 slides), better slideshow

After relabels: football_stats reaches 7 clean (add 7683181264832171297 dtfootylens, 7685028189340503310 dtkd.alan, 7670757989791403286 sftboox [AUG]); football_meme has 6 clean (one is AUG) plus 2 relabel candidates; real photo-mode slideshows collected: 2 (list below), 5 more ready to add.

## Photo-mode slideshows (real photo posts)

Collected: 7695231802327223583 (@novig, 155K); 7685694158350077204 (@walefx_, 649K).

Found in embed lists, passing the bar, NOT collected (stopped on request). Run `python -X utf8 ref.py add slideshow <url>` for any of these:

- https://www.tiktok.com/@absolutelmessi10z/photo/7696263595482533153 (244K, Barca photo post, 13 Oct)
- https://www.tiktok.com/@absolutelmessi10z/photo/7696259103622024480 (255K, Barca photo post, 13 Oct)
- https://www.tiktok.com/@novig/photo/7695496271259356446 (50K on 6.0K followers, NFL stats slides, 11 Oct)
- https://www.tiktok.com/@novig/photo/7695186280568720671 (32K on 6.0K followers, college football slides, 10 Oct)
- https://www.tiktok.com/@nayahvoetbal12/photo/7682388834943831328 (27.5K on 1.3K followers, 6 Sep)

Also found, not collected: goalwhiz08 football stat-duel videos https://www.tiktok.com/@goalwhiz08/video/7695540461733170435 (535K) and https://www.tiktok.com/@goalwhiz08/video/7691360254176840963 (384K) (face not checked); https://www.tiktok.com/@investment.timeline/video/7694794203456474401 (198K, finance POV chart).

## football_clip  (22 collected, 20 clean)

Handles: @absolutelmessi10z (972K), @py10_1 (21K), @coreeditz08 (52K), @romsbayfutbol (578K), @romoil2 (58K), @kenzy4m (55K), @nalnetsport (216K), @realnetralll (116K), @carmplus (26K), @fexo.v3.banned (101K), @iduate (157K)

- 31.22M | 10-06 | @absolutelmessi10z | https://www.tiktok.com/@absolutelmessi10z/video/7693706933689142561 | ok
- 14.84M | 09-03 | @py10_1 | https://www.tiktok.com/@py10_1/video/7681338434052721927 | ok
- 4.61M | 09-26 | @coreeditz08 | https://www.tiktok.com/@coreeditz08/video/7689719389007990038 | ok
- 4.31M | 09-08 | @py10_1 | https://www.tiktok.com/@py10_1/video/7682955487649778952 | ok
- 2.25M | 10-12 | @romsbayfutbol | https://www.tiktok.com/@romsbayfutbol/video/7695678449209396502 | ok
- 2.22M | 09-26 | @romoil2 | https://www.tiktok.com/@romoil2/video/7689975110492523807 | ok
- 2.16M | 09-14 | @kenzy4m | https://www.tiktok.com/@kenzy4m/video/7685494729554939143 | ok
- 2.01M | 10-11 | @romsbayfutbol | https://www.tiktok.com/@romsbayfutbol/video/7695489665029197078 | ok
- 1.54M | 09-12 | @py10_1 | https://www.tiktok.com/@py10_1/video/7684652734326263048 | ok
- 1.32M | 10-02 | @romsbayfutbol | https://www.tiktok.com/@romsbayfutbol/video/7691931775777377558 | ok
- 1.13M | 10-01 | @nalnetsport | https://www.tiktok.com/@nalnetsport/video/7691637818220612897 | ok
- 628K | 10-11 | @realnetralll | https://www.tiktok.com/@realnetralll/video/7695468822941224213 | RELABEL: realnetralll LFC rooster meme graphic: football_meme rather than football_clip
- 404K | 10-13 | @absolutelmessi10z | https://www.tiktok.com/@absolutelmessi10z/video/7696252820730744096 | ok
- 381K | 10-02 | @kenzy4m | https://www.tiktok.com/@kenzy4m/video/7692137380517547282 | ok
- 376K | 10-13 | @absolutelmessi10z | https://www.tiktok.com/@absolutelmessi10z/video/7696261320177388832 | ok
- 328K | 10-09 | @carmplus | https://www.tiktok.com/@carmplus/video/7694638438028430625 | FACE: carmplus creator on camera under a clip
- 327K | 10-10 | @romoil2 | https://www.tiktok.com/@romoil2/video/7695089378359643422 | ok
- 256K | 10-08 | @carmplus | https://www.tiktok.com/@carmplus/video/7694362753892420897 | FACE: carmplus creator on camera under a clip
- 187K | 10-10 | @romoil2 | https://www.tiktok.com/@romoil2/video/7694977424475376926 | ok
- 179K | 10-13 | @fexo.v3.banned | https://www.tiktok.com/@fexo.v3.banned/video/7696004720707570951 | ok
- 165K | 10-13 | @realnetralll | https://www.tiktok.com/@realnetralll/video/7696258643154521364 | ok
- 130K | 10-13 | @iduate | https://www.tiktok.com/@iduate/video/7696253943462038806 | RELABEL: iduate: 10 s POV text meme, better football_meme than football_clip

## football_edit  (20 collected, 20 clean)

Handles: @kylianftblbannedat185k (55K), @_xfnzauol_x (1.10M), @hudsfooty.0 (15K), @el.pana_47 (172K), @jovahn (44K), @filimadethat (468K), @slayzinhov (69K), @javzxem (35K), @zypheredits.00 (56K), @monatarftbl (236K), @s91drr (17K), @templesotuff (9.3K)

- 7.32M | 10-08 | @kylianftblbannedat185k | https://www.tiktok.com/@kylianftblbannedat185k/video/7694400320071355661 | ok
- 6.21M | 10-07 | @kylianftblbannedat185k | https://www.tiktok.com/@kylianftblbannedat185k/video/7693751777132399886 | ok
- 4.21M | 10-12 | @_xfnzauol_x | https://www.tiktok.com/@_xfnzauol_x/video/7695713577151270196 | ok
- 3.48M | 10-13 | @hudsfooty.0 | https://www.tiktok.com/@hudsfooty.0/video/7696061055495179552 | ok
- 2.39M | 10-02 | @el.pana_47 | https://www.tiktok.com/@el.pana_47/video/7692149095451970823 | ok
- 2.25M | 10-13 | @jovahn | https://www.tiktok.com/@jovahn/video/7696239030891023629 | ok
- 2.15M | 09-11 | @filimadethat | https://www.tiktok.com/@filimadethat/video/7684358569856208141 | ok
- 1.78M | 09-23 | @slayzinhov | https://www.tiktok.com/@slayzinhov/video/7688879871640030485 | ok
- 1.77M | 10-11 | @kylianftblbannedat185k | https://www.tiktok.com/@kylianftblbannedat185k/video/7695524643758722318 | ok
- 1.67M | 10-13 | @jovahn | https://www.tiktok.com/@jovahn/video/7696253413084024078 | ok
- 1.57M | 10-05 | @javzxem | https://www.tiktok.com/@javzxem/video/7693216585233861895 | ok
- 1.48M | 09-20 | @javzxem | https://www.tiktok.com/@javzxem/video/7687665717654605064 | ok
- 1.43M | 10-07 | @el.pana_47 | https://www.tiktok.com/@el.pana_47/video/7694003624971717896 | ok
- 1.06M | 10-06 | @javzxem | https://www.tiktok.com/@javzxem/video/7693604561885482258 | ok
- 1.06M | 09-25 | @zypheredits.00 | https://www.tiktok.com/@zypheredits.00/video/7689617852533361940 | ok
- 938K | 10-10 | @monatarftbl | https://www.tiktok.com/@monatarftbl/video/7694981485111069974 | ok
- 902K | 10-07 | @monatarftbl | https://www.tiktok.com/@monatarftbl/video/7693895693034884374 | ok
- 554K | 10-10 | @s91drr | https://www.tiktok.com/@s91drr/video/7694923895018654990 | ok
- 498K | 09-28 | @slayzinhov | https://www.tiktok.com/@slayzinhov/video/7690376041679850773 | ok
- 465K | 10-12 | @templesotuff | https://www.tiktok.com/@templesotuff/video/7695873476955032846 | ok

## football_meme  (16 collected, 6 clean)

Handles: @nayahvoetbal12 (1.3K), @ramo_akh (1.70M), @wolusfcb (281K), @sozsax (421K), @ireogunz (7.7K), @young.kippa (1.30M), @sxmvoidedit (597), @purejokes0 (119K), @theutdtrey (189K), @absolutelmessi10z (972K), @habibx03 (78K), @alsoclokus (8.5K)

- 4.01M | 08-05 | @nayahvoetbal12 | https://www.tiktok.com/@nayahvoetbal12/video/7670662930475584801 | AUG; NOTE: nayahvoetbal12 first-person POV footage, people in frame but nobody presenting (5 Aug)
- 3.49M | 10-12 | @ramo_akh | https://www.tiktok.com/@ramo_akh/video/7695806028138482974 | FACE: ramo_akh two creators on camera (skit)
- 1.82M | 10-06 | @wolusfcb | https://www.tiktok.com/@wolusfcb/video/7693643427333836064 | FACE: wolusfcb creator reacting on camera
- 1.52M | 10-06 | @sozsax | https://www.tiktok.com/@sozsax/video/7693345189796023572 | ok
- 1.13M | 08-28 | @ireogunz | https://www.tiktok.com/@ireogunz/video/7678891272995622174 | AUG; FACE: ireogunz man reacting on camera (POV skit)
- 967K | 09-06 | @young.kippa | https://www.tiktok.com/@young.kippa/video/7682495716161375510 | FACE: young.kippa face-cam reaction over match graphic
- 942K | 10-10 | @sxmvoidedit | https://www.tiktok.com/@sxmvoidedit/video/7694973990065982721 | ok
- 931K | 09-18 | @young.kippa | https://www.tiktok.com/@young.kippa/video/7686988716648320289 | FACE: young.kippa face-cam reaction over Polymarket screen
- 865K | 09-19 | @purejokes0 | https://www.tiktok.com/@purejokes0/video/7687275213398134019 | ok
- 821K | 10-05 | @theutdtrey | https://www.tiktok.com/@theutdtrey/video/7693295496282066196 | FACE: theutdtrey creator on video-call skit
- 437K | 10-13 | @absolutelmessi10z | https://www.tiktok.com/@absolutelmessi10z/video/7696260157784722721 | ok
- 318K | 09-28 | @habibx03 | https://www.tiktok.com/@habibx03/video/7690663016953613590 | FACE: habibx03 green-screen face-cam reaction over clips
- 237K | 10-11 | @alsoclokus | https://www.tiktok.com/@alsoclokus/video/7695544440764501279 | FACE: alsoclokus creator on camera in jersey skit
- 231K | 10-06 | @habibx03 | https://www.tiktok.com/@habibx03/video/7693617531113852182 | FACE: habibx03 green-screen face-cam reaction over clips
- 104K | 09-16 | @habibx03 | https://www.tiktok.com/@habibx03/video/7686254205375384864 | FACE: habibx03 green-screen face-cam reaction over clips
- 88K | 10-12 | @sxmvoidedit | https://www.tiktok.com/@sxmvoidedit/video/7695723370737978632 | small page 147x followers

## football_stats  (9 collected, 4 clean)

Handles: @hai02a (113K), @footballmaster3333 (288K), @legoat2215 (323K), @fr.football31 (57K), @hai08a (14K)

- 19.01M | 09-02 | @hai02a | https://www.tiktok.com/@hai02a/video/7680984511143841037 | NICHE: hai02a: bar-chart race of phone brands, not football (general stats page; keep as stats reference or drop)
- 4.07M | 09-08 | @footballmaster3333 | https://www.tiktok.com/@footballmaster3333/video/7683291811258944801 | FACE: footballmaster3333 presenter in front of fixture graphic
- 2.34M | 09-10 | @footballmaster3333 | https://www.tiktok.com/@footballmaster3333/video/7683694090290040097 | FACE: footballmaster3333 presenter in front of fixture graphic
- 1.42M | 10-01 | @legoat2215 | https://www.tiktok.com/@legoat2215/video/7691619846357814560 | ok
- 509K | 09-24 | @fr.football31 | https://www.tiktok.com/@fr.football31/video/7689116030567828749 | ok
- 473K | 09-07 | @footballmaster3333 | https://www.tiktok.com/@footballmaster3333/video/7682845033011236128 | FACE: footballmaster3333 presenter in front of fixture graphic
- 307K | 09-11 | @hai08a | https://www.tiktok.com/@hai08a/video/7684092565196410135 | ok
- 240K | 10-13 | @footballmaster3333 | https://www.tiktok.com/@footballmaster3333/video/7696089226600877344 | FACE: footballmaster3333 presenter in front of fixture graphic
- 109K | 09-06 | @hai08a | https://www.tiktok.com/@hai08a/video/7682287413028244758 | ok

## money_trading  (22 collected, 18 clean)

Handles: @wallstreet.club (71K), @billsricci (245K), @tjrspace.01 (124K), @tjrrare (1.9K), @bedroomtraderx (70K), @whatif.sim (27K), @urichking (1.8K), @investment.timeline (1.2K), @walefx_ (4.4K), @kojiro_0o (622), @skitradez0 (2.2K), @maxsancho1 (9.8K), @nqcaylon (2.1K), @data.dragonn (95K), @thebulltips (76K), @tjrackss (673)

- 9.45M | 09-12 | @wallstreet.club | https://www.tiktok.com/@wallstreet.club/video/7684464442846792973 | NOTE: wallstreet.club movie-scene clip (actor talks to an interviewer) with burned-in captions, no page presenter
- 4.27M | 09-13 | @billsricci | https://www.tiktok.com/@billsricci/video/7684949786612550919 | FACE: billsricci live-action actors skit
- 3.04M | 10-05 | @tjrspace.01 | https://www.tiktok.com/@tjrspace.01/video/7693165279832116500 | ok
- 2.36M | 09-25 | @tjrrare | https://www.tiktok.com/@tjrrare/video/7689533730515422495 | ok
- 2.16M | 10-02 | @bedroomtraderx | https://www.tiktok.com/@bedroomtraderx/video/7692125225667939616 | ok
- 1.50M | 09-22 | @billsricci | https://www.tiktok.com/@billsricci/video/7688352903165267208 | FACE: billsricci live-action skit, shirtless man at a desk
- 1.29M | 10-10 | @whatif.sim | https://www.tiktok.com/@whatif.sim/video/7695126838766554382 | ok
- 1.13M | 10-08 | @urichking | https://www.tiktok.com/@urichking/video/7694416050724539669 | ok
- 1.13M | 09-15 | @wallstreet.club | https://www.tiktok.com/@wallstreet.club/video/7685899967185145101 | NOTE: wallstreet.club movie-scene clip (actor talks to an interviewer) with burned-in captions, no page presenter
- 887K | 09-07 | @bedroomtraderx | https://www.tiktok.com/@bedroomtraderx/video/7682849356889771286 | ok
- 747K | 09-30 | @investment.timeline | https://www.tiktok.com/@investment.timeline/video/7691351911991217440 | ok
- 649K | 09-15 | @walefx_ | https://www.tiktok.com/@walefx_/video/7685694158350077204 | PHOTO-MODE 5 slides; RELABEL: walefx_ is a real photo-mode post (5 slides): count as slideshow
- 647K | 10-08 | @kojiro_0o | https://www.tiktok.com/@kojiro_0o/video/7694347060451003681 | ok
- 593K | 09-30 | @urichking | https://www.tiktok.com/@urichking/video/7691341043241094420 | ok
- 529K | 09-08 | @walefx_ | https://www.tiktok.com/@walefx_/video/7683107287254273300 | ok
- 501K | 09-17 | @skitradez0 | https://www.tiktok.com/@skitradez0/video/7686497123462008067 | ok
- 493K | 09-29 | @maxsancho1 | https://www.tiktok.com/@maxsancho1/video/7691026258624318751 | ok
- 401K | 10-01 | @nqcaylon | https://www.tiktok.com/@nqcaylon/video/7691761456357854478 | FACE: nqcaylon live-action skit at a desk
- 391K | 09-15 | @data.dragonn | https://www.tiktok.com/@data.dragonn/video/7685794819272101153 | ok
- 378K | 10-08 | @wallstreet.club | https://www.tiktok.com/@wallstreet.club/video/7694128645169827085 | NOTE: wallstreet.club movie-scene clip (actor talks to an interviewer) with burned-in captions, no page presenter
- 360K | 09-28 | @thebulltips | https://www.tiktok.com/@thebulltips/video/7690665582013844757 | ok
- 330K | 10-07 | @tjrackss | https://www.tiktok.com/@tjrackss/video/7694042579502943501 | FACE: tjrackss talking-head clip of a trader (TJR) with captions

## crypto  (16 collected, 12 clean)

Handles: @respawnedreality (16K), @crypto.lucho (2.70M), @rugengine.sol (294K), @cryptonect_ar (520), @binance (3.90M), @elcosto67 (79), @naspadclipp (712), @safia.ali60 (1.4K), @nimpliq (227K), @tianszv (n/a), @urichking (1.8K)

- 4.69M | 09-23 | @respawnedreality | https://www.tiktok.com/@respawnedreality/video/7688699753160297761 | ok
- 2.23M | 10-07 | @crypto.lucho | https://www.tiktok.com/@crypto.lucho/video/7693954189197659410 | FACE: crypto.lucho creators on camera
- 1.51M | 08-20 | @rugengine.sol | https://www.tiktok.com/@rugengine.sol/video/7675911670694251797 | AUG
- 1.01M | 09-15 | @rugengine.sol | https://www.tiktok.com/@rugengine.sol/video/7685579319703391508 | ok
- 784K | 09-06 | @cryptonect_ar | https://www.tiktok.com/@cryptonect_ar/video/7682491425543572758 | ok
- 435K | 10-08 | @rugengine.sol | https://www.tiktok.com/@rugengine.sol/video/7694099360140856596 | ok
- 395K | 10-05 | @binance | https://www.tiktok.com/@binance/video/7693075422472375566 | FACE: binance actor skit (marked ad)
- 367K | 09-28 | @rugengine.sol | https://www.tiktok.com/@rugengine.sol/video/7690697274145508629 | ok
- 365K | 10-13 | @elcosto67 | https://www.tiktok.com/@elcosto67/video/7696000259381562656 | FACE: elcosto67 man face on camera
- 341K | 10-07 | @naspadclipp | https://www.tiktok.com/@naspadclipp/video/7693790619956743430 | ok
- 330K | 10-10 | @safia.ali60 | https://www.tiktok.com/@safia.ali60/video/7695148066399161607 | FACE: safia.ali60 two people on camera skit
- 253K | 10-04 | @nimpliq | https://www.tiktok.com/@nimpliq/video/7692888805140974870 | ok
- 242K | 09-27 | @respawnedreality | https://www.tiktok.com/@respawnedreality/video/7690293136270167329 | NOTE: respawnedreality old-camcorder style footage of a man at a desk, not presenting
- 149K | 09-05 | @tianszv | https://www.tiktok.com/@tianszv/video/7682139826522443028 | ok
- 116K | 09-20 | @urichking | https://www.tiktok.com/@urichking/video/7687756793564368149 | ok
- 102K | 09-21 | @cryptonect_ar | https://www.tiktok.com/@cryptonect_ar/video/7688078032447311126 | ok

## betting_meme  (14 collected, 9 clean)

Handles: @kalshi.sports (7.5K), @underdogfantasy (364K), @outjuggin0078 (15K), @ap_butter1 (4.0K), @yeglazer07 (2.0K), @talkingfantasysprts (990), @novig (6.0K), @tgclips94 (13K), @pandasupr3m4cy (896K)

- 23.58M | 10-06 | @kalshi.sports | https://www.tiktok.com/@kalshi.sports/video/7693614968465263886 | ok
- 1.88M | 09-26 | @underdogfantasy | https://www.tiktok.com/@underdogfantasy/video/7689952808459652365 | ok
- 1.02M | 09-26 | @kalshi.sports | https://www.tiktok.com/@kalshi.sports/video/7689919499306372366 | FACE: kalshi.sports man talking to camera with Kalshi screen
- 934K | 09-28 | @kalshi.sports | https://www.tiktok.com/@kalshi.sports/video/7690653745280978189 | ok
- 612K | 10-12 | @outjuggin0078 | https://www.tiktok.com/@outjuggin0078/video/7695838401303465229 | FACE: outjuggin0078 man talking to camera
- 504K | 10-10 | @kalshi.sports | https://www.tiktok.com/@kalshi.sports/video/7695128512407129357 | ok
- 495K | 10-09 | @kalshi.sports | https://www.tiktok.com/@kalshi.sports/video/7694788198056168718 | ok
- 494K | 09-16 | @kalshi.sports | https://www.tiktok.com/@kalshi.sports/video/7686236389586865421 | ok
- 488K | 10-11 | @ap_butter1 | https://www.tiktok.com/@ap_butter1/video/7695288385824410893 | ok
- 301K | 10-07 | @yeglazer07 | https://www.tiktok.com/@yeglazer07/video/7694023736650992918 | NOTE: yeglazer07 is a Kanye meme page; this post is a gambling text meme
- 261K | 09-30 | @talkingfantasysprts | https://www.tiktok.com/@talkingfantasysprts/video/7691149997533875470 | FACE: talkingfantasysprts man talking to camera
- 155K | 10-11 | @novig | https://www.tiktok.com/@novig/video/7695231802327223583 | PHOTO-MODE 3 slides; RELABEL: novig: photo-mode stats slideshow (3 slides), better slideshow
- 140K | 10-09 | @tgclips94 | https://www.tiktok.com/@tgclips94/video/7694510777541086477 | FACE: tgclips94 man on camera in jersey skit
- 131K | 10-01 | @pandasupr3m4cy | https://www.tiktok.com/@pandasupr3m4cy/video/7691841627790298398 | FACE: pandasupr3m4cy woman face-cam

## clipping  (21 collected, 21 clean)

Handles: @dihanator4000 (236K), @kingdukeclips (9.9K), @mookie.clips (122K), @furevfx (16K), @validclps (118K), @jusmid_ (131K), @viralrushhtv (1.2K), @overlapdaily (109K), @insight.talk0 (19K), @clipcitybandit (725), @cptwillisreacts (526), @clipperzcom0 (998), @thepodinthenet (22K), @doublecoverage_clips (486)

- 10.77M | 09-05 | @dihanator4000 | https://www.tiktok.com/@dihanator4000/video/7682110440557514014 | ok
- 6.16M | 08-29 | @kingdukeclips | https://www.tiktok.com/@kingdukeclips/video/7679250991946026254 | AUG
- 4.82M | 09-22 | @mookie.clips | https://www.tiktok.com/@mookie.clips/video/7688146825425046792 | ok
- 3.77M | 09-14 | @furevfx | https://www.tiktok.com/@furevfx/video/7685415233443204374 | ok
- 3.33M | 10-10 | @validclps | https://www.tiktok.com/@validclps/video/7694827125198703885 | ok
- 2.72M | 09-29 | @mookie.clips | https://www.tiktok.com/@mookie.clips/video/7690762622387358983 | ok
- 2.08M | 09-02 | @jusmid_ | https://www.tiktok.com/@jusmid_/video/7680853288073448725 | ok
- 2.03M | 10-04 | @viralrushhtv | https://www.tiktok.com/@viralrushhtv/video/7692745418127527188 | ok
- 1.77M | 10-11 | @validclps | https://www.tiktok.com/@validclps/video/7695206252569251086 | ok
- 1.71M | 10-10 | @validclps | https://www.tiktok.com/@validclps/video/7694874545798368525 | ok
- 1.50M | 10-09 | @overlapdaily | https://www.tiktok.com/@overlapdaily/video/7694640187594378528 | ok
- 1.29M | 10-06 | @insight.talk0 | https://www.tiktok.com/@insight.talk0/video/7693675420306214174 | ok
- 839K | 09-11 | @kingdukeclips | https://www.tiktok.com/@kingdukeclips/video/7684146891822468365 | ok
- 817K | 10-09 | @overlapdaily | https://www.tiktok.com/@overlapdaily/video/7694729619395726625 | ok
- 775K | 10-07 | @insight.talk0 | https://www.tiktok.com/@insight.talk0/video/7693937343480270111 | ok
- 699K | 10-04 | @clipcitybandit | https://www.tiktok.com/@clipcitybandit/video/7692658162108812557 | ok
- 562K | 10-10 | @overlapdaily | https://www.tiktok.com/@overlapdaily/video/7695054274551762209 | ok
- 548K | 09-26 | @cptwillisreacts | https://www.tiktok.com/@cptwillisreacts/video/7689634096791833864 | ok
- 510K | 10-09 | @clipperzcom0 | https://www.tiktok.com/@clipperzcom0/video/7694792741838015766 | ok
- 315K | 09-18 | @thepodinthenet | https://www.tiktok.com/@thepodinthenet/video/7686863312285437198 | ok
- 307K | 10-10 | @doublecoverage_clips | https://www.tiktok.com/@doublecoverage_clips/video/7695164447169449247 | ok

## slideshow  (8 collected, 0 clean)

Handles: @drakostash (52K), @clazzed.ftbl (26K), @sftboox (118K), @dtfootylens (1.3K), @dtkd.alan (1.3K), @kolobok3098 (561), @motivational.moneytok (33K), @ntlgoat7z (45K)

- 2.15M | 09-06 | @drakostash | https://www.tiktok.com/@drakostash/video/7682561462421736734 | NOTPHOTO: drakostash: cash footage, video, not in our niches
- 1.42M | 10-07 | @clazzed.ftbl | https://www.tiktok.com/@clazzed.ftbl/video/7694008809492139272 | NOTPHOTO: clazzed.ftbl: text over dark footage, video; relabel football_meme
- 919K | 08-06 | @sftboox | https://www.tiktok.com/@sftboox/video/7670757989791403286 | AUG; NOTPHOTO: sftboox: winners list over portraits, video (6 Aug); relabel football_stats
- 853K | 09-08 | @dtfootylens | https://www.tiktok.com/@dtfootylens/video/7683181264832171297 | NOTPHOTO: dtfootylens: static nominee-list graphic as video; relabel football_stats
- 630K | 09-13 | @dtkd.alan | https://www.tiktok.com/@dtkd.alan/video/7685028189340503310 | NOTPHOTO: dtkd.alan: list over clips, video; relabel football_stats
- 619K | 09-15 | @kolobok3098 | https://www.tiktok.com/@kolobok3098/video/7685860476600716565 | NOTPHOTO: kolobok3098: goal clips with music, video; relabel football_edit
- 544K | 09-07 | @motivational.moneytok | https://www.tiktok.com/@motivational.moneytok/video/7682698669669289230 | NOTPHOTO: motivational.moneytok: cash footage, video, not in our niches
- 256K | 10-13 | @ntlgoat7z | https://www.tiktok.com/@ntlgoat7z/video/7696129211005783318 | NOTPHOTO: ntlgoat7z: ceremony clips, video; relabel football_edit
