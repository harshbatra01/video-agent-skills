---
name: idea-finder
description: Find topical video ideas and judge them by the story they can become, not by a single strength score. Covers the news radar, the Big score against the Story score, kill checks, mini context, context packs and big-name podcasts as a source. Use when picking the next video topic, scanning news, setting up an idea pipeline, or deciding if an idea is worth making.
---

# Idea finder

## The belief (from the user's voice notes)
An idea score is only a forecast. The real test is the story you can make from it. A crazy idea with no unique story is weak. A moderate idea with a unique, powerful story is better.

## The flow
Only steps 1 to 4 have been built, and the radar is run by hand. The rest is a design with guessed thresholds.
1. **Collect:** X pages, RSS, Google News, Hacker News, Reddit.
2. **Filter with no AI:** age, seen before, noise, off topic, near copies. Group posts into events. Keep an event with a signal: official post, breakout (2.5 times the page's median), several sources or a strong Hacker News score.
3. **Big score** with small AI: who, mass appeal, consequence, freshness. This score only filters. Scale: `scripts/rubric.md`.
4. **Kill checks:** is there footage, who already posted this angle, how long will it stay fresh.
5. **Mini context, then Story score:** one rough story per event, compared head to head. This score decides. Unsourced beats do not count.
6. **Notify the user:** event, both scores, the story in 2 lines, sources. The user replies go or kill. Nothing posts automatically.
7. **Context pack with sources:** timeline, past chapters, numbers, quotes, what people miss, footage map, competitor angles.
8. **3 to 5 different stories** from one pack. The best goes first, the others can follow.
9. **Results ledger:** views, hold and sends feed back into both scores.

## Story skeleton
Person, stakes, turn, 2 to 3 dated beats, planted detail, an ending that flips the hook, visual proof, a theme-linked peg, and an angle other pages will not post.
Calibrate before trusting: the judge must rank known winners above flops.

## Sources worth adding
- **Big-name podcasts:** Altman, Dario Amodei, Musk and similar appear about weekly. Make reels from what is new in them.
- **Mass interest signals:** Google Trends and Wikimedia pageview spikes.
- **Competitor videos:** YouTube channel feeds.
- One day's rough count: X was first on 1 of 5 top events, and Google News or RSS carried all 5. So more X pages is not the first fix.

## Uniqueness
A viewer sees many posts on the same topical story. Check the actual feed and avoid opening lines and shots already used.

## Tools
- `scripts/radar.py`, `config.json`, `rubric.md`, `README.md`: the radar. It needs Horizon and last30days cloned, per its README, and its paths must be edited. AI scoring uses your Claude usage. Reading X through fxtwitter is unofficial and can break.
- `scripts/context_scan.py`, `scripts/video_digest.py`: YouTube, Reddit, Hacker News and autocomplete scan for one topic. Needs yt-dlp.

## Known problems
Recall is untested and the user has not reviewed a list. One event mixed two stories. `people_miss` came out generic with the small model.
