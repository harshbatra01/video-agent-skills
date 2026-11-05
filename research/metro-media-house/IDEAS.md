# Next-video ideas for the Metro Media House style (5 Nov 2026)

Defaults applied (user, 5 Nov): organic post (no ad tail), voice picked by ear later. Footage: no restrictions (user verdict 6 Nov 2026: any copyrighted or licensed clips may be used, including feature films; no restrictions).

## How this was run
`skills/idea-finder` flow, steps 1 to 6, by hand:
- The radar (`radar.py`) could not run. It needs Horizon and last30days cloned, and this environment blocks Google News, Hacker News, Reddit and Wikipedia from the shell. The radar is also tuned for AI launch news, while this page picks backstory stories with a present-day hook.
- **Collect:** the web search tool, about 15 queries on 5 Nov 2026 (sources at the end).
- **Big score:** `idea-finder/scripts/rubric.md` scale (who, mass appeal, consequence, freshness; 0 to 10 each).
- **Kill checks:** footage, who already posted this angle, shelf life.
- **Story score:** the page-fit checklist from `STUDY.md` section 8, 7 points:
  1. famous photo
  2. known name plus a comparison
  3. a paradox or hidden link
  4. printable numbers
  5. a real clip of the person saying it
  6. a zoom-out to now
  7. a mirrored kicker
- Story scores decide the rank. Big scores only filter.

Fact grades follow `story-script-writer`: A = read at the primary source, B = reporting that cites it, C = reported or estimated, or the sources conflict. Nothing here is graded A yet. Every number must be rechecked at the source before the script locks.

## Ranked

### 1. Masayoshi Son: the man who lost $70 billion, and just bet his company again
**Story in 2 lines:** In 2000, Son was briefly the richest man on Earth, then lost about $70 billion in the crash. Six minutes with Jack Ma turned $20 million into a stake once worth more than $200 billion. Now the same gut has put more than $60 billion into OpenAI, and his own credit rating is flinching.
- **Hook photo:** Son with Jack Ma. A famous handshake photo is likely, but needs finding. Alternative: the Jan 2025 Stargate announcement photo (Trump, Son, Altman, Ellison). It is stronger as "the most expensive photo", but political.
- **Hook draft:** "This might be the most expensive handshake in history, and the man on the left is about to find out if he can do it twice."
- **Comparison slot:** open. "basically the biggest gambler in tech" needs a sharper pop-culture match. Film clips are allowed (user, 6 Nov).
- **Paradox:** the gut call that made him is the gut call that could break SoftBank.
- **Beats with numbers:** about $70 billion lost in the crash (B); richest for three days (B); $20 million in Alibaba after a 5 to 6 minute meeting (B); stake above $200 billion at the 2020 peak (B); more than $60 billion into OpenAI for roughly 11 to 13% (C, sources conflict); S&P outlook moved to negative (B); executives asked what happens if OpenAI fails (B, Bloomberg, May 2026).
- **Real clip:** Son has said "We lost around $70 billion" on record (B). Find the video.
- **Zoom-out:** "Every time you use ChatGPT, you are using Son's bet."
- **Kicker draft:** "The first time, he lost his own money. This time, he borrowed it first." (The borrowing must be checked first.)
- **Peg:** SoftBank Group Q2 FY2026 results on **10 Nov 2026**, confirmed on SoftBank's own notice page. AI-spending worries already hit tech stocks in October.
- **Big score:** who 8, mass 7, consequence 8, freshness 7: **8**.
- **Kill checks:** footage likely (keynotes, interviews, the 2014 Alibaba IPO, Son and Altman on stage). Who posted: "the man who lost $70 billion" is a common YouTube story, so the angle has to be the repeat bet on OpenAI. Shelf life: weeks, and evergreen after the peg.
- **Story score: 7/7.** Same shape as the page's Ackman reel (rise, fall, repeat), with a different person.
- **Risks:** no investment advice. Do not say "buy" or "sell"; describe the bet only. The OpenAI dollar figure must come from SoftBank's filings.

### 2. The OpenAI Mafia: the people who quit OpenAI are now worth more than it was
**Story in 2 lines:** The PayPal Mafia built the internet. A group of people who walked out of OpenAI now run Anthropic, Perplexity, Safe Superintelligence and Thinking Machines. The ones who left over safety may be the first to go public.
- **Hook photo:** an early OpenAI team photo with the future founders in one frame. **Unsure one exists or is usable. This is the kill check to clear first.**
- **Hook draft:** "This might be the most expensive group photo in AI, and most of the people in it don't work there anymore."
- **Paradox:** they left the company to slow down, and ended up racing it.
- **Beats:** Anthropic public S-1 filed 26 Oct 2026, Q3 revenue $17 billion, pricing expected about 19 to 20 Nov (C, not official); 18 notable alumni startups (B, TechCrunch, Feb 2026); 65 alumni startups worth $1.3 trillion combined (C, Dealroom chart).
- **Zoom-out and kicker:** a direct callback to the page's own YC and PayPal Mafia reels: "The PayPal Mafia built the internet you scroll. The OpenAI Mafia is building the thing that scrolls for you."
- **Peg:** the Anthropic IPO, expected mid to late November (C).
- **Big score:** who 8, mass 7, consequence 8, freshness 9: **8**.
- **Kill checks:** footage likely for the people, the hook photo unsure. Who posted: TechCrunch and many pages have run "OpenAI mafia" lists. Shelf life: until the IPO, then it turns into a different story.
- **Story score: 6/7** (no confirmed hook photo).
- **Flags you need to decide:** (a) Claude's maker is Anthropic, so this is a conflict of interest. The repo rule says flag it and let you decide the framing. (b) This repo already has an Anthropic IPO job (`examples/anthropic-ipo`), so the topic may repeat our own past work.

### 3. Jensen Huang: the booth at Denny's
**Story in 2 lines:** Nvidia was planned in a Denny's booth by a former Denny's dishwasher, then came within 30 days of running out of money. Its CEO still runs the world's most valuable chip company as if it were 30 days from death.
- **Hook photo:** the Denny's booth with its 2023 plaque (B).
- **Hook draft:** "This might be the most valuable table in the world."
- **Paradox:** the richest chip company in history is run on a motto about going bankrupt.
- **Beats:** founding meetings at a San Jose Denny's in 1992 or 1993 (B, sources disagree on the year); came within 30 days of running out of money (B); Huang says he has used the line for 33 years (B, Rogan interview).
- **Real clip:** Huang saying "30 days from going out of business" on a podcast (B). Find it.
- **Peg:** Nvidia Q3 FY2027 results, best-supported date 17 Nov 2026 (C, not confirmed against Nvidia's own release).
- **Big score:** who 9, mass 8, consequence 8, freshness 6: **8**.
- **Kill checks:** footage plentiful. **Who posted: very heavily covered**; the Denny's story has run on Fortune, CNBC, AOL and many reels. Shelf life: evergreen.
- **Story score: 7/7 on fit, but low on uniqueness.** `idea-finder` says avoid opening lines and shots already in the feed, and this one is everywhere.

### 4. The Traitorous Eight: the photo before the PayPal Mafia
**Story in 2 lines:** In 1957, eight young scientists walked out on a Nobel winner, who called them traitors. They started Fairchild, then Intel, and the chip industry traces back to one 1960 photo.
- **Hook photo:** Wayne Miller's 1960 Fairchild founders portrait (B, Magnum and the Computer History Museum). **Rights: it is a Magnum photo, so licence it or drop it.**
- **Hook draft:** "Before the PayPal Mafia, there was this photo."
- **Paradox:** the man who called them traitors won a Nobel Prize, and they won Silicon Valley.
- **Kicker draft:** "The PayPal Mafia built the internet. These eight built the thing it runs on."
- **Peg:** weak. The AI chip boom and Nvidia's results on 17 Nov are context only.
- **Big score:** who 5, mass 6, consequence 7, freshness 3: **5**.
- **Kill checks:** **footage thin**, mostly stills and archive. That breaks our moving-footage target (`edit-loop-guard` loop 4). Who posted: well known in tech history circles, rarely as a reel. USVC's book ad in EIN shows a Fairchild logo, so the sponsor may already cover it.
- **Story score: 5/7** (names not famous, no real clip found yet).

## Killed
### 5. Musk's $474 million midterm loss
- Very fresh (4 Nov 2026). About $474 million spent (B, a New York Times tally reported by Fast Company and CNBC). Paxton and Abbott, both backed by Musk, lost (B). Big score about 8.
- **Kill reason:** partisan politics. Nothing in the 4 reels takes a political side, and the repo's rule keeps political imagery out unless the story is political. This one is wholly political. Reopen only if you want the page to take that risk.

## What 4 reels and one search pass cannot tell us
- Metro Media House's full post history (Instagram is blocked here, and search found nothing), so we may repeat a topic they already did.
- Views, so the Big score cannot be calibrated against this page's winners. That is `idea-finder`'s own known problem.

## Sources (searched 5 Nov 2026)
- Forbes Australia, richest people, Nov 2026: https://www.forbes.com.au/news/billionaires/top-10-richest-people-in-world/
- CNBC, Musk midterms: https://www.cnbc.com/2026/11/04/elon-musk-midterms-ai-data-centers.html
- Fast Company, Musk $474M: https://www.fastcompany.com/91634243/elon-musk-spent-nearly-500-million-on-the-midterms-it-bought-him-almost-nothing
- SoftBank Group, Q2 FY2026 briefing notice: https://group.softbank/en/news/info/20261002
- Bloomberg, Son bounced back after the dot-com crash: https://www.bloomberg.com/news/articles/2017-10-11/how-softbank-s-son-bounced-back-after-the-dot-com-crash
- CNN, Son and Ma: https://edition.cnn.com/2019/12/06/tech/masa-son-jack-ma
- Fortune, Son, OpenAI and Trump: https://fortune.com/asia/2025/04/01/masayoshi-son-softbank-openai-trump/
- Bloomberg Government, Son's OpenAI bet raises concern: https://news.bgov.com/securities-law/softbank-founders-starstruck-bet-on-openai-raises-concern
- TechCrunch, OpenAI mafia: https://techcrunch.com/2025/04/26/the-openai-mafia-15-of-the-most-notable-startups-founded-by-alumni
- Dealroom, OpenAI mafia chart: https://dealroom.co/charts/openai-mafia.html
- Yahoo Finance, Anthropic IPO: https://finance.yahoo.com/technology/ai/article/anthropic-ipo-what-we-know-143321078.html
- NBC Miami, Huang and Denny's: https://www.nbcmiami.com/news/business/money-report/jensen-huang-started-his-2-trillion-company-nvidia-at-a-dennys-breakfast-booth/3302554
- Fortune, Huang's 30 days line: https://fortune.com/2025/12/04/nvidia-ceo-admits-he-works-7-days-a-week-including-holidays-in-a-constant-state-of-anxiety-out-of-fear-of-going-bankrupt/
- Nvidia results date (secondary): https://www.cmelitegroup.com/knowledge-hub/nvidia-earnings-date/
- Wikipedia, Traitorous eight: https://en.wikipedia.org/wiki/Traitorous_eight
- Magnum, Fairchild founders photo: https://store.magnumphotos.com/products/the-fairchild-shockley-8-who-started-silicon-valleys-first-start-up-usa-1960
- Computer History Museum, Fairchild founders: https://www.computerhistory.org/revolution/artifact/275/1388
