<!-- Boss-kit copy of the 7 Oct 2026 handoff (history; newer research corrected some claims). The partner who ran that session is called "the partner" here. -->

# Platform rules and risk

Everything here was verified during the research session. Policy dates are given because these change.

---

## 1. The account type trap

**The single highest value finding in the whole project.**

| Platform | Account type | Music access |
|---|---|---|
| TikTok | Business | **Commercial Music Library only.** A client's track will not be in it. |
| TikTok | Creator or personal | Full library |
| Instagram | Business or Professional | **Meta Sound Collection only, roughly 14,000 tracks.** |
| Instagram | Creator or personal | Full library |

Every Vision Clipping page must be **Creator or personal**. Not Business.

The failure mode is silent. Nobody is told. Someone switches an account to Business to get better analytics, and from that moment the account cannot use the client's track at all. The campaign quietly stops working.

**Action for automation:** any page health check should read account type first, and alarm on Business.

---

## 2. Originality and repost policies

Three separate policies, all recent, all pointing the same way: platforms are actively demoting content that is republished rather than made.

### TikTok
Content that is **reproduced from elsewhere** or carries a **third party watermark** is ineligible for the For You feed. Not banned, not deleted. Just invisible, which is worse because it looks like the content failed.

**So: strip every third party watermark before posting.** This is not optional polish. It is the difference between reach and no reach. It is also why logoless and scene pack sources matter so much, since they have the watermark removal done already.

### Instagram, policy effective 30 April 2026
Removed repost "aggregators" from recommendations. The policy text **explicitly names** "screenshots with usernames for credit" as a disqualifying pattern.

This directly affects the rap and meme pages, because screenshot-with-credit is the default format in both niches. Those pages need a different visual format: own designed news cards, own text treatment, or video rather than screenshot.

### YouTube, policy effective 15 July 2025
The "inauthentic content" policy. Mass produced and repetitive content is ineligible for monetisation. Shorts at this volume sit squarely in scope.

---

## 3. Multi-account risk

TikTok's terms ban accounts **"operated in bulk"** and **"networks of similar accounts distributing high volume commercial content"**.

Read that against the sold shape: three accounts, same operator, same commercial track, 270 posts a month. The structural match is uncomfortable.

What reduces the match:
- The pages are in **genuinely different niches** with different audiences, different formats and different posting rhythms. They do not look like clones.
- The bios and branding carry no shared signature, no cross promotion, no shared link.
- Posting times and cadences differ per page rather than firing on a shared schedule.
- Each page posts content that stands on its own in its niche, so the account has a reason to exist beyond the campaign.

What increases it: identical posting times, identical caption structures, cross following each other, the same device and IP, and the same track appearing across all three on the same day in the same format.

**Nobody has tested whether this holds at 270 posts a month.** Instrument the first campaign so a shadowban is visible in days, not weeks.

---

## 4. Footage risk tiers

Decided during the session. This is the publish filter, applied **after** something has been found, never before.

### Tier A, clean. Post anywhere.
- **DVIDS** and other US government footage. US government works are not copyrightable. Check each asset's own copyright line, since DVIDS hosts some third party material.
- **MLS clips via TikTok's licensed Library tool.** Licensed inside the app.
- Club, promotion and artist **published** social content, which exists to be reshared.
- Walkouts, face offs, press conferences, weigh ins.
- Self shot and fan cam footage with permission.
- Licensed stock.
- Own designed news cards and graphics.

### Tier B, standard risk. Post, but weigh it.
- Archive match footage.
- Training ground and press conference footage.
- Short fan shot concert clips, credited, never a full song.
- Amateur and regional fight footage.

### Tier C, hot. Post, but **never on YouTube Shorts.**
- Current week Premier League, La Liga, Champions League moments.

**The reason, and this is the useful part:** YouTube runs **automated** Content ID matching. Instagram and TikTok act on complaints. So the same clip that survives on TikTok for weeks gets matched on YouTube within hours. One documented channel took four strikes from UEFA and the Premier League in a single day.

So Tier C content runs on TikTok and Reels only. This is a per-platform decision, not a per-clip one, and it should be encoded in whatever publishing tool gets built.

### Watch it, never post it
- **Unreleased music, leaks, snippets.** This is what ends accounts, not news.
- **Paparazzi and agency photos.** Getty and Backgrid run automated scanning and send demand letters from 800 USD per image.
- Current UFC and DAZN in-ring broadcast footage.
- Graphic injury, death or live conflict footage.
- Unverified gossip claims. The Shade Room settled with 50 Cent and had to post a public retraction.
- Firearms content with any buy, sell or link framing.

---

## 5. AI generated content is now a real sourcing hazard

This came up hardest in the military research and it applies everywhere.

Documented campaigns:
- **100+ inauthentic TikTok accounts, 52,000+ videos, 3.8M views** producing fake soldier content, with Chinese language metadata and anatomically impossible uniforms. (Straight Arrow News)
- **1,000+ deepfaked Ukrainian soldier videos** found by Sensity AI. They seed on **TikTok or Telegram first**, then spread outward. (Euronews, April 2026)
- Fake UK veteran accounts rated 99 percent AI by Hive Moderation. (Lead Stories, July 2026)

**Detection checklist:**
- Clip is **under 8 seconds with no traceable parent video**. That is the generator's output limit.
- Rain droplets frozen on a forehead while the face moves. The best single tell.
- Hands: more than five fingers, fused fingers.
- Insignia and flags: wrong colours, wrong fonts, logos that change mid video, rank in the wrong place.
- Account has a huge follower count but follows nobody, created recently, dozens of near identical videos.
- A Sora watermark that bounces position, often cropped out, so check for an unnaturally tight crop.

**The working rule:** if a clip's earliest traceable appearance is a 2025 or later TikTok or Telegram post from an anonymous account, do not use it. Source from DVIDS and NARA, where every asset carries a named creator, rank, unit and date, or from pre-2023 archive.org collections, which predate viable video generation.

---

## 6. Handle, bio and image specs

| Platform | Handle | Bio | Notes |
|---|---|---|---|
| TikTok | 2 to 24 characters | 80 characters | **30 day cooldown on handle changes.** Get it right first time. |
| Instagram | 1 to 30 characters | 150 characters | |

**Profile pictures:** design at 1080 x 1080. They render as small as **110px**, and they are cropped to a circle. Keep all content in the **middle 60 to 70 percent**. Anything in the corners is gone.

**Banners:** Instagram has **no uploadable banner at all**. TikTok's banner is a hack: a 1260 x 654 image split into three 420 x 654 panels, used as the covers of three pinned videos. It reads as one banner on the profile grid.
