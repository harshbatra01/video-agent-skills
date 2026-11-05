<!-- Boss-kit copy of the 7 Oct 2026 handoff (history; newer research corrected some claims). The partner who ran that session is called "the partner" here. -->

# Automation roadmap

Nothing is automated yet. This is the priority order, with what is already solved so you do not redo it.

The partner's stated focus: **sourcing relevant stuff and creating posts, mainly rap for now**, then everything else.

---

## What is already solved, so do not rebuild it

- **The source list.** 152 verified sources in `data/monitoring-sources.json`, tagged by vertical and by speed. 42 are tagged `UK`. Each row has a URL, a note, and a `has_warning` flag for impersonators and dead handles.
- **The daily run order.** A fixed six step, roughly twenty minute scan, slowest moving to fastest moving. It is written out in The Wire Desk artifact. Automating this sequence is the highest value first build.
- **The publish filter.** The footage risk tiers in `01-platform-rules.md`. This is the decision logic a publishing tool needs to encode.
- **The tool stack, priced.** Free tier, roughly 60 USD a month, roughly 465 USD a month, all verified September 2026. In The Wire Desk artifact.

---

## Priority 1: the rap sourcing feed

**The problem it solves:** right now finding out what happened requires a human scanning X, Instagram and Reddit. By the time it is found, it is often late.

**Build:**
1. Filter `monitoring-sources.json` to `verticals` containing `RAP` or `UK`, `speed` of `live`.
2. For the ones with RSS (confirmed working: Variety, Sky Sports, ESPN MMA, DVIDS news), poll directly.
3. For X accounts, there is no clean free API. The practical answer found in the research was **X Lists**, one per vertical, read manually, because X Pro moved behind Premium+ at 40 USD a month on 26 March 2026. If you can solve the ingest problem properly, that is a real win.
4. For Reddit, **unauthenticated RSS was rate limited in June 2026** from roughly 100 requests per 10 minutes to about 1 per minute. Poll slowly, or use authenticated feed parameters from a logged in account's RSS settings.
5. Dedupe and rank. **The signal is volume, not individual posts:** three accounts posting the same thing inside ten minutes is the story. A naive feed that shows everything is no better than scrolling.

**Two fixed windows to schedule around:**
- **Official Charts drop Friday 4pm to 5.45pm UK.** Announced on Radio 1 at 4pm. A weekly, predictable, postable news event.
- **Kenny Allstar's Rap Show on 1Xtra, Saturday 9 to 11pm UK** since the April 2026 slot move. The biggest premiere and playlist-add slot in UK rap.

**Dead ends already found, do not waste time:** Nitter (X Corp sent cease and desist letters in August 2026, most instances dark), CrowdTangle (shut down August 2024, replacement is academics only, so there is **no Instagram trend tool available to a business**, which is a real unfixable gap), Spotify Viral 50 (discontinued May 2026, use the Shazam Top 200 public CSV instead).

---

## Priority 2: post generation

**The constraint that shapes this:** Instagram's 30 April 2026 policy explicitly names "screenshots with usernames for credit" as a disqualifying pattern. So the default rap page format is now a liability.

**What to build instead:** a generator that takes a story and outputs an **own designed news card**, not a screenshot. Consistent template, own typography, the page's own visual language. This is Tier A on the publish filter (own designed graphics) and it dodges the aggregator demotion entirely.

Inputs: headline, body, source attribution, an image. Output: a 1080x1350 or 1080x1920 card plus a caption.

**Caption rules:** no em dashes. No hint that a song is being promoted. Match the page's register, which for these niches is blunt and functional, not writerly.

---

## Priority 3: the page health monitor

Small, cheap, and it protects the whole campaign.

Check per page, daily:
1. **Account type is Creator or personal, never Business.** This is the number one check. See `01-platform-rules.md`.
2. Views per post against that page's own baseline. A sudden collapse across all posts is a shadowban signal, not a content problem.
3. Whether the campaign sound is still attached and still reachable on its sound page.
4. Follower delta.

The reason this is priority 3 and not 5: nobody has tested whether 270 posts a month across three accounts survives TikTok's bulk operation rules. Instrument it so a problem is visible in days.

---

## Priority 4: the footage pipeline

Per vertical, the sourcing is mapped in `03-sourcing.md`. What can actually be automated:

- **DVIDS has a free API** at api.dvidshub.net/docs with separate endpoints for assets, video, podcasts and live content. The military page's footage pull can be fully automated. Start here, it is the easiest win.
- **archive.org has a metadata API** and direct MP4 download URLs. The verified items are listed in `03-sourcing.md` with real resolutions and file sizes.
- **yt-dlp** handles the logoless pack channels and the official promotion channels. The channel list is in `03-sourcing.md`.
- **Airshow calendars** (MILAVIA, Blue Angels official PDF, AirshowStuff) are fixed dates. Build ahead rather than reacting.
- **Fixture calendars:** the Premier League publishes a subscribable calendar feed via pl.ecal.com that auto updates on reschedules. Subscribe, do not copy dates. UEFA has no feed, so Champions League is a manual weekly check.

**Processing order that matters:** **upscale before you crop, not after.** Cropping to 9:16 throws away resolution you cannot get back. Topaz 1080p to 4K first, then crop, then grade. Every logoless channel does exactly this and says so in the title.

---

## Priority 5: the publishing layer

A `postiz` skill is available in the Cowork environment and may be available to Claude Code. It schedules to TikTok, Instagram, YouTube and 25 other channels.

**Before wiring it up, two things have to be encoded:**
1. **The platform split.** Tier C footage never goes to YouTube Shorts, because Content ID there is automated. This is a per-platform routing rule.
2. **Deliberate schedule variance per page.** Identical posting times across three accounts is one of the strongest network signals. The schedule should look like three unrelated operators.

---

## Technical notes carried over

- **Discord beats Slack as the alert inbox.** Slack's free tier caps at 90 days of history and 10 app integrations, and this stack will exceed 10 integrations quickly. Discord has unlimited history and no integration cap.
- **Brand24 is the only listening tool confirmed to cover TikTok and Instagram together**, at 299 USD a month. Awario is a third of the price but its pricing page does not list TikTok. If TikTok coverage matters, that gap is the whole reason to pay the difference.
- **Reddit killed unauthenticated `.json` API access.** It returns a login wall, so scripted scraping needs OAuth. `yt-dlp` handles `v.redd.it` natively and is the best bulk option. Note Reddit stores video and audio as separate streams, so naive downloads come out silent; RapidSave merges them.
- **Instagram and Reddit were both unreachable from automated environments** during this research. Instagram serves a login wall, Reddit returns 403. Any build that depends on reading either will need a real browser session or an authenticated client. Plan for that rather than discovering it.
- **TikTok discovery pages are robots.txt blocked** to automated fetching but load fine in a browser. Their audio use counts are not reachable by script.

---

## Open questions nobody has answered

Flag these to the partner rather than assuming:

1. **Are the five accounts actually created yet?** Nothing in the session confirms it. Handle availability was checked, creation was not.
2. **Client pricing, and the revenue split between the partner, Jaden and Kanishk.** Never discussed. Do not invent numbers.
3. **The Virality referral terms.** Unknown.
4. **Which artist is first.** No client was named.
5. **Who posts.** 270 posts a month is a real operational load. Whether that is the partner, the collaborators, or scheduled automation was never settled, and it changes what should be built first.
