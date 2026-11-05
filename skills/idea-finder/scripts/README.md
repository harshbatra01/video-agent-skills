# Idea radar

Finds big AI and tech news and writes a ranked idea list. Free sources only. It never posts anything.

## Run
```bash
~/VisionKit/third-party/Horizon/.venv/bin/python ~/VisionKit/mine/tools/idea_radar/radar.py
```
- `--no-ai`: stop before AI and print what passed the filters.
- `--no-context`: skip the last30days reaction check.
- `--fresh`: ignore what earlier runs saw. Use it for tests.

Reports go to `runs/`. Edit sources and thresholds in `config.json`, and the scoring scale in `rubric.md`.

## Stages
1. Collect: X pages (fxtwitter, unofficial, no login), RSS, Google News, Hacker News, Reddit.
2. Filter with no AI: age, seen before, noise words, off topic, near copies (SimHash).
3. Group posts into events (TF-IDF). Keep an event only if it has a signal: official post, breakout, several sources or a strong Hacker News score.
4. Score with Claude through the Claude CLI: Big score 0 to 10, kill reason, video angle.
5. Add community reaction with last30days for the top 3 events scoring 7 or more (Reddit, Hacker News, Polymarket).

## What comes from where
- Horizon (MIT, `Thysrael/Horizon`, commit cdd95f8): scrapers imported unchanged; scoring scale adapted in `rubric.md`.
- last30days (MIT, `mvanhorn/last30days-skill`, commit 6894d44): run as a separate program.
- BuzzAgent (`gynet/buzzagent`, no licence): ideas only, no code copied. The filters and grouping here were written fresh.
- The kit: X route and the breakout rule.

To set up on another machine, clone Horizon and last30days into `~/VisionKit/third-party/`, then run `uv sync --no-dev` in Horizon. BuzzAgent is not needed to run this.

## Limits
- Reading X through fxtwitter is unofficial and carries a terms risk. It can break without warning.
- AI scoring uses the user's Claude usage, so frequent runs eat into the limit.
- Scores are AI judgments. Check the links before trusting any claim.
- No timer and no phone alerts yet.
