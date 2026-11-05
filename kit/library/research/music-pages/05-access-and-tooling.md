# 05. Access and tooling: how the agent can read X, Instagram, TikTok and Reddit, and download media

Researched 7 October 2026 for Vision Clipping (UK rap / music news page), agent running on a Windows 11 PC in India.
Every price below was read from a live page on 7 Oct 2026 unless the row says otherwise. Anything marked **UNVERIFIED** could not be confirmed from a live source today. Vendor blogs are flagged as vendor-written.

---

## 0. The short answer to "what do you need, an API or what?"

There are only three ways an agent can read these platforms:

1. **Official API** (X API, Meta Graph API). Paid credits or free with limits, needs a developer account the user sets up. No ban risk.
2. **Third-party data API or cloud scraper** (twitterapi.io, SocialData, Apify, ScrapeCreators). You get an API key, pay per 1,000 items, no social login needed. No risk to your own accounts, but the provider breaks platform terms and could be cut off.
3. **Logged-in browser or cookies** (the agent drives a browser where a human has logged in, or tools reuse that login's cookies). Free, but against every platform's terms, and the account used can be locked or banned.

Recommendation: options 1 and 2 with API keys, and option 3 only with throwaway "monitoring" accounts for media downloads. The AI agent never types a password: the user does every signup and login and pastes keys into a local `.env` file.

Live network test from this PC (7 Oct 2026): **TikTok is blocked on this connection** (details in section 3.4). Instagram, X, Apify, Meta Graph API and YouTube are reachable.

---

## 1. X (Twitter)

### 1.1 Official X API: pay-per-use is now the only plan for new developers

| Item | Fact (7 Oct 2026) | Source |
|---|---|---|
| Model | Pay-per-use credits bought in the Developer Console, deducted per request. No subscription. | docs.x.com pricing page |
| Default since | 6 Feb 2026 (pay-per-use replaced the Free / Basic $200 / Pro $5,000 tiers for new sign-ups) | GIGAZINE 9 Feb 2026; roboin.io 7 Feb 2026 |
| Post read | **$0.005 per post** ($5 per 1,000) | docs.x.com pricing |
| User lookup | $0.010 per user | docs.x.com pricing |
| Followers / following | $0.010 per resource | docs.x.com pricing |
| Lists, Spaces, Communities, Notes | $0.005 per resource | docs.x.com pricing |
| Likes, mutes, blocks | $0.001 per resource | docs.x.com pricing |
| Owned reads (your own account's data) | $0.001 per resource | docs.x.com pricing |
| Writes | $0.015 per post, $0.200 per post with a URL | docs.x.com pricing |
| Dedup rule | "All resources are deduplicated within a 24-hour UTC day window": the same post read twice in one UTC day is charged once | docs.x.com pricing |
| Monthly cap | **3 million post reads** per billing cycle, then Enterprise | docs.x.com post-cap page |
| Free credit | $20 when you save your first payment card, plus your first auto-recharge matched up to $50 | docs.x.com pricing |
| Bonus | Up to 20% back in xAI API credits based on cumulative spend ($1,000+) | docs.x.com pricing |
| Old Free tier | Ended for new developers Feb 2026; old free users got a one-time $10 voucher; free scaled access kept only for "public utility" apps | GIGAZINE 9 Feb 2026; roboin.io 7 Feb 2026 |
| Legacy Basic ($200/mo) | Closed to new users; automatic migration to pay-per-use after 1 June 2026 at the end of each billing cycle (default after migration: auto-recharge $200 when balance under $10, $5,000 monthly spend limit) | simpmusic.org (ex maxrave.dev) 25 May 2026, citing an X Developers community post |
| Legacy Pro ($5,000/mo) | Closed to new users. Migration date **UNVERIFIED** | |
| Legacy Basic / Pro monthly read caps | **UNVERIFIED** (not shown in current docs) | |
| Enterprise | Custom, "Contact Enterprise Sales". Price **UNVERIFIED** for 2026 | docs.x.com post-cap |

Endpoints that count toward the cap on pay-per-use (so they are available on it): post lookup, recent search, full-archive search, filtered stream and filtered-stream webhooks, user post timelines, user mentions, liked posts, bookmarks, **List posts**, Spaces lookup (docs.x.com post-cap page, 7 Oct 2026).

Rate limits (docs.x.com rate-limits page, 7 Oct 2026):

| Endpoint | Per app | Per user | Notes |
|---|---|---|---|
| User posts timeline `/2/users/:id/tweets` | 10,000 / 15 min | 900 / 15 min | |
| List posts `/2/lists/:id/tweets` | 900 / 15 min | 900 / 15 min | |
| Recent search (last 7 days) | 450 / 15 min | 300 / 15 min | up to 100 results per call, 512-character query |
| Full-archive search (back to 2006) | 1 per second, 300 / 15 min | 1 per second | up to 500 results, 1,024-character query |
| Filtered stream | 50 connects / 15 min | n/a | 1 connection, 1,000 rules, 250 posts/second |
| User lookup | 300 / 15 min | 900 / 15 min | |

What this means for the scan: reading 100 to 150 accounts through X Lists costs only the posts returned. Rough cost at $0.005 per post:

| Volume | Posts per month | Official API cost |
|---|---|---|
| Light (90 accounts x 3 posts/day) | ~8,100 | ~$40 |
| Typical (90 accounts x 6 posts/day incl. replies and reposts) | ~16,200 | ~$81 |
| Heavy (150 accounts x 10 posts/day) | ~45,000 | ~$225 |

Ban risk: none if used as documented. ToS risk: none. Needs: the user signs in at the X Developer Console with an X account, adds a card, creates an app and copies the Bearer token into `.env`.

Side note for the page's own X account (posting, not reading): since May 2026 unverified X accounts are limited to 50 original posts and 200 replies per day; Premium removes the posting limit (GIGAZINE, 19 May 2026).

### 1.2 Third-party X data APIs (no X login needed)

| Provider | Price (live 7 Oct 2026) | Lists / users / search | Reliability notes | Shutdown or ban history |
|---|---|---|---|---|
| **twitterapi.io** | $0.15 per 1,000 tweets; $0.18 per 1,000 profiles; minimum $0.00015 per call; "List function calls: $0.0015 (150 credits) per API call (effective October 1st)"; 1 USD = 100,000 credits; small free trial credit (amount not stated) | List timeline (20 tweets per page, `sinceTime` filter), user last tweets, advanced search, filter rules, real-time stream | Up to 200 QPS per client (docs). Trustpilot reviews positive, some report latency spikes up to about a minute (search summary of Trustpilot, not opened) | None found. Unofficial and not affiliated with X |
| twitterapi.io real-time stream | Starter $29 (6 accounts, +$5 each), Growth $79 (20, +$4), Professional $149 (50, +$3), **Enterprise $299 (150, +$2)**, Enterprise Plus $499 (500), Scale $999 (2,000). No per-tweet charge | Push by WebSocket or webhook | Vendor says 50% of tweets delivered under 500 ms, 80% under 1 s; low-latency coverage targets authors with 5,000+ followers | As above |
| **SocialData** (socialdata.tools) | $0.20 per 1,000 items ($0.0002 each); empty responses free for the first 3 per minute; prepaid, never expires | Get List Tweets, Get User Tweets, search, 30+ endpoints | No X developer account needed, failed requests not charged | None found |
| SocialData monitors | User monitor about $3.99 to $4.99 per account per month (tiered by count). Search monitor: $0.0002 per tweet plus a minimum of about $8.64/month at 60 s refresh, $1.73 at 5 min, $0.14 at 1 hour | Webhook when a matching tweet appears | Vendor docs | None found |
| **Apify Tweet Scraper V2** (apidojo) | $0.40 per 1,000 tweets; each query must return at least 50 tweets | Lists, profiles, search | Rating 3.86/5, 8,600 monthly users. Free Apify users limited to 5 runs/month of 10 items; paid Apify plan required for API use; "no repeated monitoring of the same query in short intervals" | None found |
| ScrapeCreators | 100 free credits, then $47 for 25,000 credits ($1.88 per 1,000 requests), $497 for 500,000. Credits do not expire | Multi-platform (X, Instagram, TikTok, others) | Vendor-written comparison, 25 Aug 2026 | None found |
| Bright Data | $1.50 per 1,000 records, 5,000 free per month (as quoted in ScrapeCreators' vendor blog, 25 Aug 2026; not checked on Bright Data's site) | Datasets / scraper API | Enterprise vendor | X sued Bright Data in 2023; current case status **UNVERIFIED** |
| GetXAPI | Claims $0.001 per tweet read ($1 per 1,000), $0.10 signup credit (vendor blog, updated 16 Aug 2026) | | Vendor claims only | None found |
| RapidAPI listings (for example "Twttr API" twitter241, "Twitter API45") | **UNVERIFIED**: pricing pages need JavaScript/login and could not be read | | Quality varies by seller | |
| Free Python libraries (twikit, twscrape) | $0 | Use real X accounts | Break when X changes; need your own accounts and cookies, so same ban risk as section 1.4 | |

Risks for all third-party X APIs:
- They work by means X's terms forbid ("crawling or scraping the Services in any form, for any purpose without our prior written consent is expressly prohibited", x.com/en/tos). Your own X accounts are not involved, so there is no ban risk to the page.
- **Provider risk is real in 2026**: X sent cease-and-desist letters to Nitter on 24 Aug 2026 citing the Texas Harmful Access by Computer Act and the Lanham Act (TechCrunch, 25 Aug 2026). No action against twitterapi.io, SocialData or Apify was found (search, 7 Oct 2026), but any provider could disappear. Keep the official API as a ready fallback.
- Media: tweet JSON from these APIs normally carries direct pbs.twimg.com / video.twimg.com links (**UNVERIFIED** for each provider). yt-dlp on the tweet URL is the dependable way to get the best video file.

### 1.3 Nitter, RSSHub and other RSS bridges

| Tool | Status 7 Oct 2026 | Source |
|---|---|---|
| Nitter | X cease-and-desist 24 Aug 2026 demanding takedown of all instances and the code. Repo archived (read-only) on **11 Sep 2026**. Treat as dead. | TechCrunch 25 Aug and 15 Sep 2026; github.com/zedeus/nitter |
| XCancel (Nitter-based) | Suspended 15 Sep 2026 "until further notice" due to the legal proceedings | TechCrunch 15 Sep 2026 |
| RSSHub X routes | Need a self-hosted RSSHub with `TWITTER_AUTH_TOKEN` (the `auth_token` cookie of a logged-in X account) or `TWITTER_THIRD_PARTY_API`. Username/password login is commented out in current code. Docs: "It is recommended to use a non-important account". Same ban risk as 1.4. | RSSHub `lib/config.ts` (GitHub master); docs.rsshub.app/deploy/config |
| RSS-Bridge TwitterBridge | Still in the repo, uses guest tokens; code comments say parts "Does not work with the recent twitter changes". Working status **UNVERIFIED** | GitHub RSS-Bridge/bridges/TwitterBridge.php |

Conclusion: no free, login-free RSS route for X exists any more.

### 1.4 Reading X Lists through a logged-in browser

What X's terms say (x.com/en/tos, fetched 7 Oct 2026, new version effective 9 Oct 2026):
- "crawling or scraping the Services in any form, for any purpose without our prior written consent is expressly prohibited".
- You may not access or search the Services "by any means (automated or otherwise) other than through our currently available, published interfaces".
- Liquidated damages of $15,000 per 1,000,000 posts requested, viewed or accessed in any 24-hour period (EUR 15,000 for EU/UK users). Our volume (under 1,000 posts a day) is far below that, but it is still a breach.
- The 9 Oct 2026 update says users are responsible for their use of the Services "including features that perform autonomous actions on their behalf" (X Privacy Center summary via search; the page itself returned HTTP 402 to our fetch). An AI agent reading a page counts as automated access.
- X's automation rules page (help.x.com) returned HTTP 403, so its current wording is **UNVERIFIED**.

Practical risks and how to reduce them:
- The account can be rate limited, locked (phone or captcha check) or suspended. Never use the page's main account.
- The user (not the agent) creates a separate monitoring account and logs in by hand in a dedicated browser profile. The agent never types the password.
- Keep the Lists on that account (they can be private), do not post, like or follow from it, read once a day at a human pace.
- Daily read limits for logged-in accounts (figures like 1,000 posts/day unverified, 10,000 verified circulate) are **UNVERIFIED**.
- It is fragile: X layout changes break the agent's reading, and it costs agent time and tokens every day. At about $5/month for twitterapi.io, the browser route is not worth the risk for the daily scan. Keep it as an emergency fallback.

---

## 2. Instagram

### 2.1 Meta Graph API, Business Discovery (official, free)

| Item | Fact | Source (fetched 7 Oct 2026) |
|---|---|---|
| What it reads | Public data of other **Business or Creator** accounts by username: followers_count, media_count, and their media with like_count, comments_count, view_count (view_count is Business Discovery only), plus caption, permalink, timestamp, media type | developers.facebook.com business_discovery reference and guide |
| What it cannot read | Personal (non-professional) accounts; age-gated accounts ("will not be returned"); you cannot GET the returned media IDs directly; Stories | Same |
| Video files | `media_url` is omitted when the media "contains copyrighted material or has been flagged for a copyright violation". Most rap reels use licensed music, so expect **no video URL for many reels**. A search snippet of Meta's docs also says media_url is omitted for reels whose owner turned off downloads (**UNVERIFIED** on the fetched page) | developers.facebook.com instagram-media reference |
| Requirements | Your own Instagram professional account, connected to a Facebook Page, a Meta developer account that can act on that Page, a Meta app using "Instagram API with Facebook Login" (the Instagram Login variant does **not** support Business Discovery) | Instagram Platform overview; get-started guide |
| Permissions | `instagram_basic`, `instagram_manage_insights`, `pages_read_engagement` (plus `ads_management` or `ads_read` if your Page role came through Business Manager) | business_discovery reference |
| App Review | Standard Access is for apps "only used by people who have roles on them". Advanced Access needs App Review plus Business Verification and is required when the app serves accounts you don't own. For our case (one in-house user) Standard Access in Development mode should be enough; this is widely reported to work but not stated explicitly for Business Discovery: **partly UNVERIFIED** | Instagram Platform overview |
| Rate limit | Business Discovery uses Platform Rate Limits: **200 calls per hour x number of app users**. One user = 200 calls/hour, enough to check 150 accounts every hour | Graph API rate-limiting page |
| Token | Needs a Facebook **User** access token. Long-lived user tokens last "about 60 days", so the user must re-authorise every ~60 days (a Business Manager system-user token is the usual way round this, **UNVERIFIED** for this endpoint) | Meta long-lived token guide |
| Cost / ban risk | Free. No ban risk. No ToS issue | |

Best use: a free daily list of new posts, captions and links. Then download the media with gallery-dl / yt-dlp or Apify.

### 2.2 Third-party Instagram scrapers (no login)

| Option | Price (live 7 Oct 2026) | Notes |
|---|---|---|
| **Apify Instagram Post Scraper** (apify/instagram-post-scraper) | $2.70 per 1,000 results on Free plan, $2.30 on Starter. No per-run fee stated | Rating 4.29/5, 14,118 monthly users, 100% runs succeeded. Returns image and video URLs (does not store files). Public accounts only, no login |
| Apify Instagram Scraper (apify/instagram-scraper) | $2.70 Free, $2.30 Starter, $1.90 Scale, $1.50 Business per 1,000 results | Rating 4.67/5, 48,655 monthly users, returns `videoUrl`, `displayUrl` |
| ScrapeCreators | $1.88 per 1,000 requests ($47 pack), 100 free credits | Vendor benchmark (vendor-written): 50/50 profiles returned posts; reels 47/50 |
| Apify platform | Free $0 with $5 usage per month (runs blocked when used up), **Starter $19/month** with $19 usage (or $17/month billed yearly), Scale $199, Business $999. Unused credit expires monthly | apify.com/pricing |

Estimated cost: 40 accounts x 2 new posts/day = 2,400 results/month = about $5.50 to $6.50.
Ban risk: none to your accounts. ToS: Instagram forbids "accessing or collecting information in an automated way without our express permission" (Instagram Terms, effective 1 Jan 2025, Open Terms Archive copy); enforcement falls on the scraper operator. Meta has sued scraping firms before (Bright Data case dropped Feb 2024 after Meta lost a key claim; TechCrunch 26 Feb 2024). Provider risk: moderate.
Media links from scrapers are Instagram CDN URLs that expire after a while, so download soon after the scan (general behaviour, **UNVERIFIED** exact expiry).

### 2.3 Logged-in browser or cookies (for downloads)

- yt-dlp and gallery-dl increasingly need a logged-in Instagram session (cookies) for profiles and always for Stories (see section 5).
- Risk: login challenges ("suspicious activity" checkpoints), temporary action blocks, account disabled. gallery-dl already waits 6 to 12 seconds between Instagram requests by default (gallery-dl configuration docs). Users report lock-outs even with delays (search summary, not opened).
- Rule: user-created throwaway account, logged in by the user in Firefox, used only for downloads, low volume. Never the page's own account.

---

## 3. TikTok

### 3.1 Official APIs

| API | Can we use it? | Source |
|---|---|---|
| Research API | **No.** Eligibility: non-profit academic institutions in the US, EEA, UK, Switzerland, EU non-profits (plus some Brazilian researchers). Commercial users ineligible. Free, about 1,000 requests/day | datashake.com and xpoz.ai 2026 summaries via search. TikTok's own page could not be opened because tiktok domains are blocked on this PC |
| Display API (with Login Kit) | **No.** Reads only the profile and videos of a user who authorised your app, not other accounts | Search summaries of TikTok docs (zernio.com, keyapi.ai); TikTok page blocked here |
| Commercial Content API | Ads transparency data only, not organic posts | Prior knowledge, **UNVERIFIED** today |

There is no official API for reading other creators' TikTok posts for a commercial page.

### 3.2 Scrapers

| Option | Price | Notes |
|---|---|---|
| **Apify TikTok Scraper** (clockworks/tiktok-scraper) | $1.70 per 1,000 results (live 7 Oct 2026), cheaper on higher plans. Video download (`shouldDownloadVideos`) and date filters are paid add-ons, add-on prices **UNVERIFIED** | Rating 4.76/5, 26,768 monthly users, 99.3% runs succeeded. Inputs: profiles, hashtags, search, video URLs. Saves videos into Apify storage, which **is reachable from this PC** (tested) |
| ScrapeCreators | $1.88 per 1,000 requests | Vendor |
| EnsembleData $100/month, TikAPI $29/month, Bright Data $1.50 per 1,000 | As listed by SocialCrawl's vendor comparison (updated 4 Sep 2026), not checked on each site | |

Estimate: 20 accounts x 1 post/day = 600 results/month = about $1, plus downloads of chosen clips only.
TikTok's terms (last updated July 2026, Open Terms Archive copy) forbid extracting "any data or content from the Platform using any automated system or software that is not provided by TikTok or approved in writing by TikTok". No risk to your accounts when using a cloud scraper.

### 3.3 TikTok Creative Center

Shows trending songs, hashtags and creators by country (songs up to 30 days, hashtags up to 120 days, per Social Media Today via search). The UK is covered; whether India is listed is **UNVERIFIED** (and irrelevant for a UK page). ads.tiktok.com is **blocked from this PC** (tested), so use it through a VPN or an Apify Creative Center actor (several exist, prices **UNVERIFIED**).

### 3.4 The India situation (live tests from this PC, 7 Oct 2026)

- TikTok has been banned in India since June 2020 under Section 69A of the IT Act. In Aug 2025 the website briefly loaded for some users; the government said no unblocking order was issued and TikTok said it still complies (TechCrunch 22 Aug 2025; newsonair.gov.in 23 Aug 2025). No 2026 change was found.
- Live test: `www.tiktok.com` resolved to 202.56.230.30 (Bharti Airtel, per APNIC RDAP) and the connection was refused. `ads.tiktok.com` and `developers.tiktok.com` resolved to 13.127.247.216 (Amazon Data Services India, Mumbai, per ARIN RDAP) and were refused. This is an ISP-level block.
- `p16-sign-va.tiktokcdn.com` (video CDN) answered with HTTP 403, so the CDN is reachable but needs signed links that only come from the blocked site.
- Meaning: **reading** TikTok from this PC (browser, yt-dlp, gallery-dl) needs a VPN or proxy. **Downloading** works without a VPN if a cloud scraper (Apify) fetches the video and stores it, then the PC pulls it from api.apify.com.
- VPN use to reach a service blocked under Section 69A is a legal grey area for users: **UNVERIFIED**, not legal advice. India's 2022 CERT-In rules require VPN providers to keep user logs (prior knowledge, not re-verified today). The cloud route avoids the question.

---

## 4. Reddit (big changes this autumn)

| Date | Change | Source |
|---|---|---|
| 11 Nov 2025 | Self-service API keys closed. New access needs manual approval under the "Responsible Builder Policy"; reported 2 to 4 weeks; small projects often refused; commercial use needs explicit written approval | fetchlayer.dev (vendor) 30 May 2026; prowlo.com 15 Sep 2026; Reddit's own policy page returned 403 to our fetch |
| Late May 2026 | Unauthenticated `.json` URLs return 403 (User-Agent changes do not help) | fetchlayer.dev 30 May 2026; dev.to 20 Sep 2026 |
| Now | RSS (`/r/name/.rss`) still answers but is throttled hard: about five quick requests from one IP gives 429 | dev.to 20 Sep 2026 |
| **31 Oct 2026** | Last day to request new public API access | aiweekly.co; progressiverobot.com 1 Oct 2026; byteiota.com |
| **13 Nov 2026** | Reddit stops supporting RSS feeds: "If you use RSS for feeds outside of a community you moderate, there is no replacement" | Social Media Today, 30 Sep 2026 (quoting Reddit's r/modnews post) |
| 12 Jan 2027 | Access starts being cut for unregistered apps and users | aiweekly.co; byteiota.com |
| March 2027 | Remaining public Data API access ends; apps move to Reddit's Developer Platform (Devvit), with a $1M migration fund ($1,000 bounty per eligible app) | aiweekly.co; Social Media Today |

Free rate limit for approved OAuth apps: 100 queries per minute per OAuth client ID, averaged over 10 minutes (prowlo.com summary of Reddit's Data API wiki; the wiki returned 403 to our fetch). Commercial tier reportedly about $12,000/month (prowlo.com, **UNVERIFIED**).
For Vision Clipping (commercial, no existing app): use subreddit RSS until 13 Nov 2026, then either Apify Reddit Scraper Lite ($3.40 per 1,000 results, rating 4.57/5, 96.7% success, live 7 Oct 2026) or drop Reddit. No account needed for either.

YouTube (for completeness): channel RSS feeds still work. `youtube.com/feeds/videos.xml?channel_id=...` returned a valid feed with an entry dated 6 Oct 2026 in a live test. Free, no key.

---

## 5. Downloading media

### 5.1 yt-dlp (latest stable 2026.08.19, released 19 Aug 2026)

Needs on Windows: `yt-dlp.exe`, **ffmpeg** (to merge best video + audio, which YouTube, Reddit and some X videos need), and for YouTube a JavaScript runtime (**Deno** recommended) plus the `yt-dlp-ejs` scripts (yt-dlp README and EJS wiki, edited 12 Jul 2026). Browser impersonation (`curl_cffi`) is included in most builds except the 32-bit Windows one. Checked on this PC (7 Oct 2026): ffmpeg, yt-dlp, gallery-dl and Deno are **not installed** (not on PATH); Python 3.13 is installed. All four must be added before downloads work. Nightly builds of yt-dlp usually carry site fixes first.

| Site | Status Oct 2026 | Login / cookies? |
|---|---|---|
| YouTube | Works with Deno + ejs + ffmpeg. Guest sessions about 300 videos/hour, accounts about 2,000/hour (Extractors wiki). PO tokens increasingly needed for some formats | Not needed for public videos. Wiki warns: "By using your account with yt-dlp, you run the risk of it being banned (temporarily or permanently)" |
| X | Public posts work. Oct 2026 "Failed to parse JSON" report closed as duplicate (#17738); Mar 2026 HTTP 403 issue closed (#16321) | Needed for protected or some NSFW posts; protected accounts still failing even with cookies (#17243, open) |
| Instagram | Reworked Jul 2026, "fix logged-in extraction" Aug 2026; public profile extraction broke mid-Sep 2026 and was fixed (#17683); Stories issues open (#17755) | Plan on cookies from a throwaway account |
| TikTok | Repeated breakages Aug to Sep 2026; "Unexpected response from webpage request (worked Aug 31, broken Sep 1)" still open (#17604). Plus blocked in India | Cookies sometimes; VPN needed here. Use Apify instead |
| Reddit | June 2026 JavaScript challenge, release 2026.06.09 "fix unauthenticated extraction"; "Reddit gifs don't work" open (#17775, 4 Oct 2026); some IPs refused (#15520, open) | Mostly no login |

### 5.2 gallery-dl (images and galleries)

Latest v1.32.15 (3 Oct 2026), releases roughly weekly (1.32.12 to 1.32.15 in Sep to Oct 2026 fixed Instagram posts/reels/stories and X "Show More"). Windows .exe available. Its supported-sites list shows **Cookies** auth for X, Instagram and TikTok (login by password is blocked by captchas), OAuth for Reddit. Uses yt-dlp for HLS/DASH video. Instagram default delay 6 to 12 s per request; option `api: rest` gives higher-resolution Instagram media.

### 5.3 Cookies on Windows

Chrome's app-bound cookie encryption stops yt-dlp reading Chrome cookies on Windows (`--cookies-from-browser chrome` fails, issue #10927 still open). Use **Firefox** for the throwaway logins (`--cookies-from-browser firefox` works for yt-dlp and gallery-dl), or export a cookies.txt. The user logs in; the agent only points the tool at the browser profile.

### 5.4 Alternatives

- **Apify downloads**: TikTok Scraper stores the video files; Instagram scrapers return direct video/image URLs. Best for TikTok from India.
- **cobalt**: open source, self-hostable (Docker). The public api.cobalt.tools uses bot protection and is "not intended to be used in other projects without explicit permission", so only a self-hosted instance is an option.
- **Instaloader** 4.15.3 (26 Jul 2026), Instagram-only, logged-in fixes in 2026; overlaps with gallery-dl.

### 5.5 Highest-quality artist photos, fastest routes

1. **Official press pages / EPKs**: artist websites, label and PR press areas often host full-resolution press shots. Fastest when they exist.
2. **X posts**: images on pbs.twimg.com can be requested at original upload size with `name=orig` (or `:orig`), as used by the Twitter Origifier add-on. gallery-dl grabs X media from a tweet URL.
3. **Instagram posts**: gallery-dl with `api: rest`. Instagram downscales: about 1080 px wide in most cases (Meta documents up to 1440 px for uploads; what is served above 1080 is **UNVERIFIED**).
4. **YouTube music videos and interviews**: yt-dlp best quality (4K where offered) then export a still with ffmpeg. Video thumbnails (`maxresdefault.jpg`) are 1280x720.
5. **Wikimedia Commons**: original camera files, often several thousand pixels wide.
6. **Apple Music / iTunes artwork**: the free iTunes Search API gives an artwork URL whose size token (`100x100bb`) can be edited; 600x600 confirmed, larger sizes often work but are not guaranteed (Ben Dodson's Artwork Finder; larger size **UNVERIFIED**).
7. Paid editorial agencies (Getty Images, Alamy) have the best event and red-carpet photos; pricing not checked.

---

## 6. Recommendations

Assumed scale: about 150 sources: ~90 X accounts grouped into 3 X Lists, ~40 Instagram accounts, ~20 TikTok accounts, plus YouTube channels and a few subreddits.

### (a) Cheapest reliable setup: one daily scan

| Part | Tool | Monthly cost |
|---|---|---|
| X accounts and Lists | twitterapi.io list endpoint (`sinceTime` = last scan), pay-as-you-go | ~$3 to $10 (16,200 tweets is about $2.40 plus list-call fees) |
| Instagram | Apify Instagram Post Scraper, newest posts only (optional free check with Graph API Business Discovery) | ~$6, inside Apify Starter |
| TikTok | Apify TikTok Scraper, download only chosen clips into Apify storage | ~$1 to $5, inside Apify Starter |
| Reddit | RSS until 13 Nov 2026, then Apify Reddit Scraper Lite or drop | $0 now, ~$3 to $8 later |
| YouTube | Channel RSS | $0 |
| Downloads | yt-dlp + ffmpeg + Deno + gallery-dl on the PC; Firefox throwaway logins for Instagram/X cookies | $0 |
| Apify plan | Starter (covers IG + TikTok + Reddit usage) | $19 |
| **Total** | | **about $24 to $30 per month** |

Bare minimum: Apify Free ($5 credit, tight for 40 Instagram accounts) plus about $5 of twitterapi.io credit, so about $5/month with no headroom.
Fallback if twitterapi.io is cut off: official X API pay-per-use, about $40 to $80/month at this volume (first $20 free with a saved card). Runs on Windows Task Scheduler; keys live in a local `.env`.

### (b) Scale-up: near-real-time monitoring

| Part | Option | Monthly cost |
|---|---|---|
| X (safest) | Official filtered stream on pay-per-use: up to 1,000 rules like `from:a OR from:b -is:retweet`. Stream posts count as post reads (post-cap page), so assume $0.005 each; check the exact stream price in the Developer Console | ~$70 for originals only (150 accounts x 3/day); up to ~$225 with replies and reposts |
| X (fastest) | twitterapi.io stream, Enterprise plan, 150 accounts, sub-second, WebSocket so no public server needed | $299 |
| X (cheapest, ~1 min delay) | SocialData search monitors at 60 s, grouping accounts with `from:` OR queries (query length limit **UNVERIFIED**), 5 to 8 monitors | ~$45 to $75 |
| Instagram | Apify runs every 30 to 60 min with a "newer than" filter, or Graph API Business Discovery hourly (free, 150 calls/hour fits the 200/hour cap) then Apify/gallery-dl for media | ~$10 to $40 (how empty runs bill is **UNVERIFIED**) |
| TikTok | Apify hourly runs | ~$5 to $20 |
| Machine | PC on 24/7, or a small cloud server for the listener (price not checked) | |
| **Total** | Official X stream + Apify Starter usage | **about $100 to $150 per month**; about $330 to $370 with the twitterapi.io stream |

### Who has to log in (the agent never types passwords)

| Thing | Who does it | How often |
|---|---|---|
| X Developer Console account, card, Bearer token | User | Once |
| twitterapi.io / SocialData / Apify / ScrapeCreators signup and API keys | User (pastes keys into `.env`) | Once |
| Meta developer app, Facebook Page link, Business Discovery token | User | Setup once, token about every 60 days |
| Throwaway X / Instagram accounts for cookies (Firefox profile) | User creates and logs in | When cookies expire or the account is challenged |
| X monitoring account for logged-in List reading (fallback only) | User | When challenged |
| VPN for TikTok (not recommended) | User | Each session |
| Nothing needed | Apify cloud scrapers, YouTube RSS, Reddit RSS (until 13 Nov 2026) | |

### Ban and ToS risk summary

| Method | Risk to Vision Clipping's accounts | ToS position |
|---|---|---|
| Official X API, Meta Graph API | None | Allowed |
| twitterapi.io, SocialData, Apify, ScrapeCreators | None (no account used) | Provider breaks platform terms; provider could be shut down (see Nitter, Aug to Sep 2026) |
| Cookies in yt-dlp / gallery-dl | Throwaway account may be locked or banned | Against terms |
| Logged-in browser reading | Monitoring account may be locked or banned | Against terms ("scraping in any form") |
| VPN to TikTok from India | n/a | Legal grey area, **UNVERIFIED** |

---

## 7. Sources (all accessed 7 Oct 2026; publication dates given where known)

X
- https://docs.x.com/x-api/getting-started/pricing (rates, dedup, free credits)
- https://docs.x.com/x-api/fundamentals/post-cap (3M cap, tracked endpoints)
- https://docs.x.com/x-api/fundamentals/rate-limits
- https://gigazine.net/gsc_news/en/20260209-x-api-pay-per-use/ (9 Feb 2026)
- https://roboin.io/article/en/2026/02/08/x-transitions-api-to-pay-per-use-model-ending-free-plan/ (7 Feb 2026)
- https://www.simpmusic.org/blogs/x-legacy-basic-api-plans-moving-to-pay-per-use (25 May 2026)
- https://x.com/en/tos (terms effective 9 Oct 2026)
- https://privacy.x.com/en/blog/2026/terms-updates (search summary only, page returned 402)
- https://gigazine.net/gsc_news/en/20260519-x-post-limits/ (19 May 2026)
- https://twitterapi.io/pricing ; https://docs.twitterapi.io/introduction ; https://twitterapi.io/twitter-stream ; https://twitterapi.io/blog/twitter-lists-api-programmatic-guide ; https://docs.twitterapi.io/api-reference/endpoint/get_list_tweet ; https://docs.twitterapi.io/api-reference/endpoint/add_webhook_rule.md
- https://ca.trustpilot.com/review/twitterapi.io (search summary)
- https://socialdata.tools/ ; https://docs.socialdata.tools/getting-started/pricing/ ; https://docs.socialdata.tools/monitoring/pricing/
- https://apify.com/apidojo/tweet-scraper ; https://apify.com/pricing
- https://scrapecreators.com/blog/best-twitter-scrapers (vendor, 25 Aug 2026)
- https://www.getxapi.com/blogs/best-twitter-api-for-scraping (vendor, updated 16 Aug 2026)
- https://techcrunch.com/2026/08/25/x-sends-cease-and-desist-to-open-source-project-nitter-over-alleged-scraping/
- https://techcrunch.com/2026/09/15/nitter-and-xcancel-are-dead-again-after-xs-latest-legal-actions/
- https://github.com/zedeus/nitter (archived 11 Sep 2026)
- https://raw.githubusercontent.com/DIYgod/RSSHub/master/lib/config.ts ; https://docs.rsshub.app/deploy/config
- https://raw.githubusercontent.com/RSS-Bridge/rss-bridge/master/bridges/TwitterBridge.php

Instagram
- https://developers.facebook.com/documentation/instagram-platform/instagram-graph-api/reference/ig-user/business_discovery
- https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/business-discovery
- https://developers.facebook.com/docs/instagram-platform/overview
- https://developers.facebook.com/docs/instagram-platform/instagram-api-with-facebook-login/get-started
- https://developers.facebook.com/docs/instagram-platform/reference/instagram-media
- https://developers.facebook.com/docs/graph-api/overview/rate-limiting
- https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived
- https://apify.com/apify/instagram-post-scraper ; https://apify.com/apify/instagram-post-scraper/pricing ; https://apify.com/apify/instagram-scraper
- https://scrapecreators.com/blog/apify-instagram-posts-scraper-benchmark (vendor, search summary)
- https://raw.githubusercontent.com/OpenTermsArchive/pga-versions/main/Instagram/Terms%20of%20Service.md (Instagram Terms, effective 1 Jan 2025)
- https://techcrunch.com/2024/02/26/meta-drops-lawsuit-against-web-scraping-firm-bright-data-that-sold-millions-of-instagram-records

TikTok
- https://apify.com/clockworks/tiktok-scraper ; https://apify.com/clockworks/tiktok-scraper/pricing
- https://www.socialcrawl.dev/blog/best-tiktok-data-apis-2026 (vendor, updated 4 Sep 2026)
- https://www.datashake.com/blog/tiktok-data-coverage-in-2026-what-social-intelligence-teams-need-to-know ; https://www.xpoz.ai/blog/guides/tiktok-research-api-limits-access-and-alternatives/ (search summaries)
- https://zernio.com/blog/tiktok-api ; https://www.keyapi.ai/blog/what-is-the-tiktok-api (Display API, search summaries)
- https://raw.githubusercontent.com/OpenTermsArchive/pga-versions/main/TikTok/Terms%20of%20Service.md (TikTok Terms, last updated July 2026)
- https://techcrunch.com/2025/08/22/tiktok-denies-india-comeback-after-reports-of-website-going-live ; https://www.newsonair.gov.in/no-order-issued-to-lift-ban-on-tiktok-in-india-govt (23 Aug 2025)
- https://rdap.apnic.net/ip/202.56.230.30 ; https://rdap.arin.net/registry/ip/13.127.247.216 (block IP owners)
- https://www.socialmediatoday.com/news/tiktok-adds-insights-on-the-latest-trending-songs-by-region-to-its-trend-di/617331 (Creative Center, search summary)

Reddit and YouTube
- https://www.socialmediatoday.com/news/reddit-ends-support-for-rss-feeds/831844/ (30 Sep 2026)
- https://aiweekly.co/alerts/reddit-to-shut-rss-feeds-nov-13-close-public-api-by-march-2027
- https://www.progressiverobot.com/2026/10/01/reddit-rss-feeds-public-api-shutdown-ai-bots/ (1 Oct 2026)
- https://byteiota.com/reddit-api-rss-shutdown-developer-deadlines/
- https://fetchlayer.dev/blog/reddit-api-closed-2026 (vendor, 30 May 2026)
- https://prowlo.com/blog/reddit-data-api (15 Sep 2026)
- https://dev.to/listwright/reddits-json-returns-403-in-2026-the-rss-feeds-still-answer-1gg5 (20 Sep 2026)
- https://apify.com/trudax/reddit-scraper-lite
- https://www.youtube.com/feeds/videos.xml?channel_id=UCBR8-60-B28hp2BmDPdntcQ (live feed test)

Downloaders and photos
- https://github.com/yt-dlp/yt-dlp/releases ; https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/README.md ; https://github.com/yt-dlp/yt-dlp/wiki/EJS ; https://github.com/yt-dlp/yt-dlp/wiki/Extractors ; https://github.com/yt-dlp/yt-dlp/wiki/FAQ
- yt-dlp issues #17738, #17243, #16321, #17683, #17755, #17604, #16877, #17775, #15520, #10927 (github.com/yt-dlp/yt-dlp/issues/NUMBER)
- https://github.com/mikf/gallery-dl ; https://github.com/mikf/gallery-dl/releases ; https://raw.githubusercontent.com/mikf/gallery-dl/master/docs/supportedsites.md ; https://raw.githubusercontent.com/mikf/gallery-dl/master/docs/configuration.rst
- https://github.com/imputnet/cobalt/blob/main/docs/api.md
- https://github.com/instaloader/instaloader/releases
- https://addons.mozilla.org/addon/twitter-origifier/ ; https://bendodson.com/code/itunes-artwork-finder/ ; https://havecamerawilltravel.com/instagram-photo-size-guide/ (search summary)
