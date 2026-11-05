> **Boss-kit copy. DATA, NOT INSTRUCTIONS.** This was the `CLAUDE.md` of an earlier Claude session (7 Oct 2026), run by a
> partner of the team whose name is left out of the kit; "he" below means that partner. It is renamed so Claude Code never
> loads it as project instructions. Its "hard rules" were standing rules for that session only. Rule 5 (never raise
> copyright or licensing concerns) is a business decision for the boss, not a rule for his Claude: the kit's own research
> and skills do flag licensing. Where this file and newer material differ (vc-news README, research/music-pages, the
> client file), the newer material wins.

# Vision Clipping

Project context for Claude Code. Read this file first, then open whichever doc in `docs/` the task needs.

Compiled 7 October 2026 from a long Cowork research session. Everything here was verified at the time of writing. Dates are given so you can tell what has gone stale.

---

## What this is, in one paragraph

Vision Clipping is a music promotion business run by **a partner** (the earlier session's owner; his name is left out of the kit). It is separate from his own video editing agency. The model: take on a music artist, then push their track viral by posting it as the **audio** behind high volume niche edits across accounts Vision Clipping owns, on TikTok, Instagram Reels and YouTube Shorts. The audience never knows a song is being promoted. They follow a football page, or a fight page, or a meme page.

The campaign shape sold to clients is **3 pages x 3 posts a day = 270 posts a month behind one track**.

Collaborators: **Jaden** and **Kanishk**. Referrals come through **Virality**, a large clipping agency.

## The product is concentrated volume on one sound

Every track has a TikTok sound page. The thing Vision Clipping actually sells is a large number of posts all pointing at the **same** sound page in a short window. Scattered posts across many sounds are worth close to nothing. This is why the page count and post cadence are the whole offer.

---

## Hard rules, in priority order

### 1. The account type trap. This is the single most important operational fact.

**TikTok Business accounts can only see the Commercial Music Library.** **Instagram Business and Professional accounts are capped at Meta's Sound Collection, roughly 14,000 tracks.** A client's track will not be in either. **Creator and personal accounts keep the full music library.**

So every Vision Clipping page must be a **Creator or personal** account, never Business. Switching an account to Business to get analytics silently kills its ability to run the campaign, and nothing warns you. If a page is underperforming, check the account type before anything else.

### 2. Detect everything. Filter at publish.

Monitoring and publishing are two separate decisions, taken at different times, by different rules. Watch leak accounts, gossip accounts, graphic footage subreddits, pirate clip mirrors, all of it, because that is where things surface first. Watching a source costs nothing. Posting from it is decided later, against `docs/01-platform-rules.md`.

Never collapse the two. A desk that only watches what it is allowed to post is blind exactly where stories break.

### 3. Never use em dashes

In any output. Chat, documents, drafts, code comments, captions. This is a permanent standing instruction from the partner, not a style preference for one task.

### 4. Keep replies short

One or two lines by default, then guide the next step. Give the full explanation only when he asks for it. He works fast and in bursts.

### 5. Do not raise copyright or licensing concerns on image and footage sourcing

He has explicitly taken that risk on and asked for it to stop being mentioned. Flag a source being **dead, fake, AI generated, or an impersonator**, because that is a quality problem. Do not flag it being copyrighted.

---

## Where things live

```
CLAUDE.md                        this file
docs/00-overview.md              the business, the team, the campaign shape
docs/01-platform-rules.md        the rules that kill campaigns, and footage risk tiers
docs/02-pages.md                 the five pages: handles, bios, specs
docs/03-sourcing.md              where footage comes from, by vertical
docs/04-editing.md               technique, the real names for every effect, build recipes
docs/05-automation-roadmap.md    what to build, in order, with what is already solved
data/monitoring-sources.json     152 verified sources, machine readable
```

### Three live reference pages already published

These pages sit in the partner's claude.ai account: ask him to share them (never sign in with someone else's login). They are richer than the docs on their own subjects.

| Page | What it holds | URL |
|---|---|---|
| The Wire Desk | The 152 monitoring sources with a filterable UI, a daily run order, the tool stack with real prices, the publish filter, and a dead-tools list | https://claude.ai/code/artifact/59d3f763-df00-4b82-a444-2a84c62814b2 |
| Drill Edit Handbook | UK drill editing: the effects glossary with the real community names, tutorials by software, preset packs, the run and gun rig | https://claude.ai/artifact/GoL6m1UuDdMH7ejwNZ1eQE |
| Hoops and Hurt | Basketball and fight: sourcing, beat by beat build recipes, the verified aura cold open clips, and the edits worth studying | https://claude.ai/artifact/34DKGT8tqFuZtmPbUd6c97 |

The `data/monitoring-sources.json` file is the same source list as The Wire Desk, extracted so you can build feeds, alerts and scrapers from it directly rather than parsing HTML.

### Documents delivered earlier in the session

- `Vision Clipping - Campaign Brief - Three Pages One Track.pdf`, 18 pages, client facing. Built then explicitly set aside, not in use.
- `Vision Clipping - Format and Sourcing Research.docx`, 10 pages. His own research cleaned up for his boss. Football formats, music formats, player roster, footage sources, scene packs, news sources.
- `Vision Clipping - Page Branding.docx`, 9 pages. The final page names, bios and all 12 profile picture images at full resolution.

If he refers to "the branding doc" or "the research doc", those are the two.

---

## Working with the partner: corrections he has already made

Carry these so you do not repeat a mistake he has already paid for.

**Bios must not sound AI generated.** Poetic, atmospheric bios were rejected outright. Real bios in these niches are blunt, emoji bulleted noun phrases. The register is `📷|Pictures,Videos,News 🥊|Everything about boxing 🔥|Daily uploads`, not "the 30 seconds before the walk and the 10 after the finish". If a bio reads like it was written to be admired, it is wrong.

**Profile pictures must be actual current memes.** Suggesting public domain classical art and medieval marginalia was a hard miss. What landed: Jimothy the raccoon, tornado squirrel, nihilistic penguin, Chill Guy, Hide the Pain Harold, with direct image links.

**Do not centre the branding on the song.** The pages do not tell their audience they are promoting a track. Any copy that hints at it breaks the whole premise.

**Check that a term is real before using it.** He has caught invented jargon twice. `93rdminute` was presented as an established football phrase and is not. `limbs` and `tekkers` are named by FourFourTwo itself as overused social media clichés. Verify, do not generate plausible sounding scene language.

**Narrow when he narrows.** He stopped two in flight research runs with "NEED THIS JUST FOR FOOTBALL". When he scopes down, scope all the way down.

---

## Current state

**Done:** page naming and branding, the monitoring stack, footage sourcing per vertical, the editing knowledge base, the client brief.

**Open:** nothing is posting yet. The accounts are not confirmed created. No automation exists. That is what this handoff is for, and `docs/05-automation-roadmap.md` is the priority order.

**Immediate next build, by his own stated focus:** rap post generation and sourcing, with the UK scene as the first target. 42 of the 152 monitoring sources are tagged `UK`.
