# Finding and confirming stories

How to find what is happening, confirm it, spot what is breaking out, and research a story before it is scripted.
Platform facts were checked between 7 and 14 Oct 2026: re-check any of them before a job depends on it.

## Contents
1. Keep sources lean
2. The news sweep (Google News)
3. Free machine-readable signals, and the dead ones
4. Reading X, Instagram, TikTok and YouTube without logging in
5. Who is fast, who is reliable
6. Handle traps and impersonators
7. Spotting breakouts
8. Ranking stories for a regional page
9. Confirming a story: one primary source per story type
10. Screening: what to leave out
11. The added fact, and angles from the audience
12. Calendars of dated hooks
13. Data that vanishes: capture it the same day
14. Researching a story for a script
15. Traps

## 1. Keep sources lean
- A daily news page needs a handful of main pages plus one news sweep, not a stack of 100+ feeds. Our music-news scan
  reads 12 main X pages (UK and US leaders) plus a Google News sweep; a full mode with 81 feeds, charts, trends and a
  calendar exists and is rarely used. Why: the leaders already aggregate everything, and the user said it plainly:
  "all of this stuff can easily be found from main pages ... payout is so low if we have so many sources".
- Prefer machine-readable primary feeds (RSS, public JSON) over aggregator pages. Why: they are free, stable and
  timestamped, and a script can read them every day.
- Treat an inherited source list or handoff as leads. Re-check every source live and mark it VERIFIED or UNVERIFIED
  with the date. Why: one handoff oversold TikTok Creative Center for trend tracking, relied on the dead YouTube
  Trending page, assumed Spotify playlist adds could be tracked, listed a release calendar that only loads by
  JavaScript, and carried impersonator handles (section 6). The user: "dont take everything solid as the sources are a
  bit ass".

## 2. The news sweep (Google News)
- Add a Google News RSS sweep to every scan (`news.google.com/rss/search?q=<query>`), with queries such as
  `UK rap when:2d`, `UK rapper when:2d` and a few big names in the niche.
- Why: the aggregator pages sometimes skip big announcements (a stadium-show announcement was only on news sites);
  Google News RSS gives exact publish times, which makes it the best "who posted first" tool; and it gets round the
  fetch blocks of sites such as the BBC and the Daily Mail.

## 3. Free machine-readable signals, and the dead ones
Tested 7 Oct 2026 for a music-news page: 61 trend signals (40 live) and 121 feeds (81 live).

| Signal | What it gives |
|---|---|
| Shazam chart CSVs (UK top 200, hip-hop/rap, discovery) | the earliest sign that a song is breaking |
| Apple Music most-played JSON (host now `rss.marketingtools.apple.com`) | daily chart positions |
| kworb | Spotify daily per country, about 2 days behind |
| The chart company's own pages (UK: Official Charts and its First Look) | the official numbers |
| Wikimedia pageviews | a spike = 3x the 28-day median and 1,000+ views |
| Google Trends "Trending Now" RSS (`trends.google.com/trending/rss?geo=GB`) | 10 trending searches |
| iTunes Search / Lookup, MusicBrainz | release facts and cover art |
| YouTube channel RSS | new uploads per channel |

Dead or locked (do not build on them): the YouTube Trending page (gone 21 Jul 2025); the old Google Trends RSS;
pytrends; Tokboard; Billboard pages to scripts (HTTP 402); Spotify country charts (need a login); the Spotify API's new
releases and top tracks (removed Feb 2026) and editorial playlists (unreadable since 27 Nov 2024); Reddit RSS (ends
13 Nov 2026).

- Score movement, not position: new entries, rank jumps, stream gains. Why: a position tells you what everyone
  already knows; movement is the story.
- Data-led clients: look for public, keyless APIs before any scraping (for a prediction-market client: the product's
  own API at 60 requests a minute, the underlying chain's info API, ESPN's public JSON for scores, goal minutes and form,
  exchange price candles, central-bank RSS). Fan-built tools that wrap these had bugs: use them as design references
  only. Run collectors from a home connection, because some sites' Cloudflare blocks cloud-server addresses.
  (Endpoint details belong to the client's pipeline: production-automation.)
- Slow or rate-limited sources: cache them and keep them off the daily path. Wikidata's SPARQL endpoint answered 429
  at about 1 request a minute during an outage; a 14-day cache with 65 s spacing fixed it, and the calendar that needed
  it was later dropped.

## 4. Reading X, Instagram, TikTok and YouTube without logging in
Reading routes carry a terms risk: see licensing-and-rights.md section 9 before you rely on one.
- **X, daily scans:** the unofficial fxtwitter API: `api.fxtwitter.com/2/profile/<handle>/statuses` (add `?cursor=`
  to page), `/status/<id>`, and `/2/search?q=<terms> since:YYYY-MM-DD`. Retry 2 to 3 times with letter-case variants
  and reordered terms before you call a handle dead (five handles failed once with 404 and worked on a case-variant
  retry). Nitter is gone (cease-and-desist Aug 2026, archived 11 Sep 2026), XCancel was down, and RSS bridges now need
  a logged-in cookie. Public syndication also works: `cdn.syndication.twimg.com/tweet-result?id=<id>&token=a` (the
  `token=a` is a public constant) and the public syndication timeline. Clean fallbacks: a paid X data API or X's
  official pay-per-use API (dated prices in `~/VisionKit/kit/library/research/music-pages/05-access-and-tooling.md`).
- **X, one person's posts for a pitch:** read them in the built-in browser where the user's throwaway account is
  signed in; the mirror is only a fallback for public posts, and you say that you used it. A Substack's `/feed` gives
  its 20 newest posts as RSS.
- **Instagram:** the public `/embed/captioned/` page of a post; reel pages and `/popular/<tag>/` grids open in the
  browser pane without a login; view counts can be read off the logged-out profile grid (about 12 reels), but many
  posts hide views when logged out. Socialpruf gives 12-month totals and top posts. Read slowly: the
  `web_profile_info` endpoint answered HTTP 429 after about 20 quick lookups, which puts the reading account at risk.
- **TikTok** (it does not load from India): the tikwm single-video API returns exact views, likes, shares, date,
  length, the sound name, the `is_ad` flag and the media; the urlebird mirror gives search (about 10 results a query),
  hashtag and user pages with rounded follower counts; `r.jina.ai` in front of a TikTok creator embed page lists the
  latest posts of non-verified accounts. Never bypass a Cloudflare check (tikwm's search and user endpoints sit behind
  one). From a UK or US machine TikTok loads normally, so these workarounds fall away.
- **YouTube:** watch pages (section 4 of footage-sourcing.md for search, info and storyboards); InnerTube search with a
  consent cookie; YouTube's own preview stills for filmstrips; `yt-dlp -J --skip-download` for metadata, the "Most
  replayed" heatmap and an `info.json` with caption, likes, comments and timestamp. `yt-dlp "ytsearchN:<query>"`
  prints id, title, channel, duration, views and `live_status`: a scheduled premiere shows in search with its
  `live_status`, which confirms a premiere time.
- The built-in browser pane crops screenshots to about 799 px: enlarge the tab first (`resize_window`), lay the post
  grid out with a small JavaScript thumbnail overlay, capture once with `zoom`, then reset the viewport.
- Check that a logged-in tab is still logged in before you rely on it (both monitoring logins were found logged out
  once; the user logs them back in, Claude never types a password).

## 5. Who is fast, who is reliable
- Map, for each niche, who breaks stories first and who is reliable. Detect with the fast pages, confirm with primary
  sources (section 9), and never use a fast but sloppy page as the source.
- Example (UK rap, Oct 2026): the fastest beef page posted about 6 times a day, about 1.5 h after the artist's own
  upload, and mirrored to TikTok within a minute, but it mixed in gambling promos and unsourced claims, so it was a
  detection source only. Small accounts beat it on early stages; one platform ran 20 to 29 h ahead of another on
  shared stories; the UK radio brands had abandoned X.
- Why: a once-a-day page cannot win on speed, so it wins on picks, checks and the added fact.

## 6. Handle traps and impersonators
- Check every handle you inherit: follower count, posting history, and a link from the brand's own site.
- Seen in one inherited list: a 3-follower account sitting on a big brand's obvious handle (the real one used an
  underscore); an Instagram handle that belonged to an unrelated person (the brand used a `.xyz` suffix); a news
  brand's web-style handle owned by someone else (the brand's X handle was different); a placeholder account; two dead
  "drill news" accounts (one likely compromised); a "daily" page that had turned into self-promotion.
- Why: inherited lists carried all of these as live sources, and an impersonator's post is the classic fake.

## 7. Spotting breakouts
Measure each post against its own page, by the median:
- `over` = the post's views divided by the page's MEDIAN views. 2.5x or more = breaking out.
- `talk` = (replies + quotes) per 1,000 views: debate potential (only for posts over 5K views).
- `share` = (reposts + bookmarks) per 1,000 views.
- Group the last 7 days of scans by story type ("what's working").
- Why the median: one viral outlier inflates an average. The boss's own concept doc used "3x the page's average"; we
  advised the median.
- What it showed in one week: court and legal stories ran about 1.4 to 1.7x usual and a third of them broke out;
  throwbacks broke out 0 times in 6.
- For YouTube videos the same idea is the outlier score: views divided by the median of the 15 uploads either side
  (performance-and-reference-research.md section 6).

## 8. Ranking stories for a regional page
- Raw counts favour high-volume pages (US pages post 20 to 40 times a day) and bury the local stories a UK page needs.
  Weight local sources 1.5, local artists x1.3, add chart and trend presence plus `log10(views) / 2`, and keep a
  separate local top section.
- Alias every spelling you see (one big page misspelled an artist's name in 14 of its 15 posts, so the story was
  missed); match short ambiguous names (Dave, Chip, Future, Drake...) case-sensitively.
- The mechanics live in the news pipeline (production-automation).

## 9. Confirming a story: one primary source per story type
Why: the fastest pages post single-source "EXCLUSIVE" and "allegedly" claims. A page that posts once a day can afford to
check.

| Story type | Confirm at |
|---|---|
| Charts | the chart company's own pages (and its First Look), Apple Music RSS JSON, iTunes Search/Lookup, kworb, Billboard |
| Releases and premieres | the artist's own YouTube channel (a scheduled premiere shows in search with its `live_status`) |
| Events, shows, fights | the organiser's own account or site |
| Legal dates and sentences | the official record (for US federal cases, the federal inmate locator) |
| Statements | the person's own account |
| Anything else | 2 or more independent outlets, found through Google News |

- Legal, violent and "allegedly" items need press or police confirmation before they go near a post.
- Left out on purpose in one week: an unsourced shooting claim (one page only), a misquote ("100+ unreleased songs"),
  a "news" clip that was an old throwback, a collaboration only one page reported, a picture that looked edited.
- Check cover art and release facts against the release itself: iTunes Search once matched the wrong release, and some
  albums are missing from it; swap the story when there is no clean art.
- Confirm who is who and check every face crop before you put a name on a face (a crop once missed the artist). Why: a
  wrong name on a face is the fastest way to lose a news page's credibility.
- Public records name real people: use them to confirm, post only what the story needs, and strip legal names, ages
  and prison details from any file you share.
- Write the sources you checked into the batch file's `note` (research-reports-and-folders.md section 4).

## 10. Screening: what to leave out
- Deaths and tragedies; violent and prison-violence clips; thirst-trap clips; relationship gossip; edited or
  misleading images; race angles that can backfire; someone else's skit or meme edit; promos dressed up as stories;
  unconfirmed collaborations; leaks, unreleased snippets, agency paparazzi photos and unverified gossip; stale stories
  (an old TV show was "too old" to matter); too much of one story or one artist (the user: "we've done too much [one
  artist] stuff").
- Why: these lose reach, mislead, or put the page at risk. The reach side (what each platform demotes) lives in
  social-video-formats; the rights side in licensing-and-rights.md.
- Keep a "left out on purpose" list in every batch hand-over, so the user sees the judgement.

## 11. The added fact, and angles from the audience
- Every post built on someone else's footage needs one fact the source does not show: a chart position, a time, a
  count, a date, background, a change since yesterday, a comparison. Test: could a viewer get this by reading the
  source? Examples: "1,700 comments in under 2 hours" (read off YouTube); "23 years since [album] won the Mercury".
  Why: platform originality rules demote reposts (social-video-formats), and a page with no followers has no other
  way to reach people. Research is where the fact comes from.
- Read the top comments to find the angle the audience is already running with, and run that angle. Example: a
  promised diss track turned out to be a troll song, and the top comment "we got trolled" had 700+ likes; the post
  used that angle.
- Honest number hooks instead of invented ones: real numbers side by side over the same window (views, likes,
  comments, views per day), a Story poll posted the next day with its voter count ("[X]% of [N] voters on our Story
  picked..."), real quotes from the scene, our own call record. Never "25% think X is better" without a real poll
  (fact-and-claims-checks.md section 1).

## 12. Calendars of dated hooks
- Before planning batches, build a calendar of dated hooks with verified facts: every entry has a source and a date,
  or it is marked UNVERIFIED. Examples from one job: a US inflation release (14 Oct, 12:30 UTC), a central-bank rate
  decision (28 Oct, 18:00 UTC), an awards night (26 Oct). Why: timely posts need exact dates, and a wrong date is a
  public mistake.
- The UK chart week (Oct 2026): First Look on Sunday (posted on X about 19:30 to 20:00 UTC), the Update on Monday
  (about 16:00 to 18:30 UTC), the Trending chart on Tuesday, the final chart on Friday (radio show from 16:00, reveal
  17:45 UK time). Midweek posts say "on course for" and go out before Friday. Why: chart news is the most predictable
  postable news, and midweeks let a page post before the result.
- Time zones: digests and many APIs print UTC, the editor may be in India (UTC+5:30), the audience in the UK. British
  Summer Time ends 25 Oct 2026, so UK posting windows move by an hour against UTC and India. Write the zone next to
  every time.

## 13. Data that vanishes: capture it the same day
- Live data disappears: prediction-market prices vanish at settlement (only lifetime stats survive), X-hosted clips get
  deleted (the originals behind official-looking posts were gone by the next day, and a broadcaster's post held only a
  thumbnail). Archive while it is live (a price archive every 5 minutes) and download clips the same day.
- Check outside facts on the posting day: player facts change (a star player transferred clubs in the window), and
  "last night", "tonight" and "in 12 days" posts expire. Refresh prices and counts on the day you post.

## 14. Researching a story for a script
- **Own an angle.** Check who already covered the topic (two credentialled creators had already covered the same
  product type), then take a distinct angle (a cheap-versus-expensive head-to-head plus your own rating) and show
  both sides of a live debate. Why: a me-too review loses to creators with credentials.
- **Name check** before naming a channel, a rating or a series: search the name (a planned channel name was free;
  a similar one was taken by a quiet channel in another niche). In July 2026 more than 1,000 AI channels posing as
  health experts were reported, so expect scrutiny of anything health-related.
- **A story, not a recap.** Research the backstory (often an earlier chapter) and the last 48 hours. A date-order recap
  "reads as boring even when every fact is right". Story shape and hooks: editing-playbook.
- **History beats.** Get the original paper (its PubMed ID), one reliable free article that tells the story, and
  public-domain footage (footage-sourcing.md section 8). Expect only tiny archive photos of minor historical figures.
- **Learning a person before writing for them.** Rank their posts against their own median, measure their speaking
  pace, and keep every line traceable to their own posts, letters or talks; keep the disclaimers they always carry on
  money scripts.
- **Talent check (tentative).** Before an ad, search the talent's recent public controversies: expect them in the
  comments. (Found once by a research agent; no verdict on it.)
- **Comments as demand.** On clip channels, the comments say what viewers want next; the guest's and host's own best
  uploads show which title grammar works.
- **Reference ads.** Meta's Ad Library (set the country, search the brands) shows competitors' live ads; TikTok
  Creative Center's Top Ads by industry is fine for ad references, even though it was oversold for trend tracking
  (tentative).

## 15. Traps
- **An empty result is an error, not "nothing trending".** Geo-blocks fail silently: from India, Deezer returned
  `{"data":[]}` with no error and TikTok refused the connection. Give every source a "fewer than N rows" alarm, and run
  scans from a UK or US machine when you can.
- **Accents break matching.** Strip accents in every name matcher across sources (Unicode NFKD, then drop the
  combining marks): "Atlético" against "Atletico" silently broke fact and result matching twice; "Bodø" is the same
  trap.
- **Rate limits:** Instagram about 20 quick lookups; YouTube about 80 quick metadata lookups in a row, or about 15
  parallel calls, triggers a bot check (it cleared after about 15 to 20 minutes); Wikidata about 1 request a minute
  during an outage.
- **Lookalike domains:** a "bonus" page on a lookalike of a big brand's domain is likely a scam: do not open it.
- **Fetch blocks:** big news sites block research fetchers (BBC, Guardian, NYT, CNN, the Wayback Machine). Use Google
  News RSS for the time and the user's browser for the page.
- **Queue pages and bot walls:** never bypass them (a race organiser's site sat behind a queue page); find the same
  content elsewhere or ask.
