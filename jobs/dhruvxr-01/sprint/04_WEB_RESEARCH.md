# 04 Web research: who makes the dark monochrome SaaS launch-film style, how, with what

Status: VERSION 2, written 2026-11-05 07:50 UTC. Final pass by 07:54 UTC.
Author: web-research subagent. Brief: jobs/dhruvxr-01/sprint/BRIEF.md.

## Rules used in this file
- All reads dated 2026-11-05 (UTC).
- SNIPPET = seen in a WebSearch result summary only. The source page itself was not opened. Treat as unverified until someone opens the URL.
- UNVERIFIED = background knowledge, no source found this session.
- BLOCKED = host not in the session's allowed network domains. Not worked around.
- Claude cannot watch or hear video. Nothing here says how a video looks or sounds unless a written source says so.
- No claim below is a measured fact from the reference videos. Those numbers live in research/dhruvxr/STUDY.md.

## 0. Short answer
- No source named a studio that "owns" this exact look (dark monochrome, 2 to 4 frame bursts, dot-matrix forms, tilted 3D UI, glitch hits, tiny grey sans). Searches for that look returned generic "launch video" sellers.
- The work found comes from 3 groups: (a) in-house brand motion teams at SaaS companies, (b) solo motion designers and small studios selling "launch video" packages on Contra, Fiverr and Dribbble, (c) new AI tools that sell launch videos without After Effects.
- Tools named in sources: After Effects, Cinema 4D, Figma, Redshift, Octane, Blender (as a bonus skill), DaVinci Resolve (grade), Jitter (Figma to motion, exports video, GIF, Lottie), Remotion (code, has a halftone effect).
- The @_dhruvxr identity was not confirmed. A fueler.io profile surfaced but fueler.io is BLOCKED.

## 1. Who makes it

### 1a. In-house teams at SaaS companies (SNIPPET)
| Company | What the source says | URL | Status |
|---|---|---|---|
| Linear | Job ad for a motion role making "promotional videos that highlight Linear's features and benefits", which suggests in-house films | https://builtindublin.ie/job/motion-storyteller/4629107 | SNIPPET |
| Vercel | "Motion Designer, Brand" job covering "product launches, campaigns, events, social content, and videos" | https://job-boards.greenhouse.io/vercel/jobs/5648721004 | SNIPPET |
| Whop | Contractor ad, "Animator / Motion Designer", "USD 60-90 / hour", dated May 2025 per the summary | https://jobs.signalfire.com/companies/whop/jobs/51613137-animator-motion-designer | SNIPPET |
| Whop | Self-reported credit by Drice Roland: "Whop, Oct 2023 - Nov 2023 ... announcement video for V3 of their web application". Not the WHP brand film. Not independently verified | https://www.therookies.co/u/Drice | SNIPPET |

- No official credit was found for the WHP reference film. Next step (not done): check the film's own post or description for credits.

### 1b. Freelancers and small studios selling launch videos (SNIPPET)
| Who | Offer | Tools named | Price / time | URL |
|---|---|---|---|---|
| Novra Design (UK) | 3D launch video; "placing the product in 3D space so viewers understand it before reading" (summary wording) | Cinema 4D, Redshift, After Effects | from $25,000, 6 weeks | https://contra.com/s/blrAqNBb-premium-3-d-launch-video |
| Yunis Mikayilov | Launch videos for funded AI startups | not stated | from $8,000 | https://contra.com/s/AZF3272L-launch-videos-for-funded-ai-startups |
| The Flow Concept | Script to final motion | not stated | from $5,000, 3 weeks | https://contra.com/s/XMRlWYN7-saa-s-product-launch-video-script-to-final-motion-in-3-weeks |
| AGFX Studio | SaaS launch film with app user flow | After Effects, Cinema 4D, Figma | from $2,500, 4 weeks | https://contra.com/s/Y7QFMZgo-saas-explainer-videos |
| Hisham Jawahir (Berlin) | Launch video incl. UI/UX flow walkthrough and sound design | not stated | from $899, 3 weeks | likely https://contra.com/s/cbl7bBrc-launch-video-for-for-your-product-startup-or-saa-s (URL-to-name match not confirmed) |
| Amine Ignaoun | "clean, product-focused motion graphic videos for SaaS teams" | not stated | from $600 | https://contra.com/s/mr6XLEom-motion-design-for-saa-s |
| Steve Lemuel | Raycast "Kinetic Product Motion" portfolio piece, not an official Raycast credit | Figma UI, DaVinci grade | n/a | https://contra.com/p/llNMeeMX-raycast-kinetic-product-motion |
| Nen Creative | Design studio for early-stage companies; motion hires need After Effects and Figma, Cinema 4D and Blender as bonus | AE, Figma, C4D, Blender | n/a | https://wellfound.com/jobs/4219963-motion-designer |
| Cleev.io | Motion and brand studio | Redshift, Cinema 4D, After Effects, Octane | n/a | https://cleeviox.com/motion |
| Launch3d | Hiring an After Effects designer to animate "UI, typography, product moments, launch claims, and social-ready sequences" (summary wording) | After Effects | n/a | https://jobs.weekday.works/motion-system-designer-at-launch3d-wkdyu2bi89 |

- Price spread seen: $600 to $25,000 per launch video (SNIPPET, sellers' own starting prices).

### 1c. AI tools selling launch videos (SNIPPET, titles only)
- Motion ("the agent for motion design"), has a launch-videos page: https://motion.so/solutions/launch-videos
- Topview Motion Studio, "Create launch videos without touching After Effects": https://www.hunted.space/dashboard/topview-ai
- Lago blog post titled "we killed our motion design job": https://getlago.com/blog/we-killed-our-motion-design-job (BLOCKED, content not read)

### 1d. dhruvxr
- A profile for "Dhruv Raghuwanshi", "Video Editor | Motion Artist", India, claiming "10M+ Views Across Platforms And 10K+ Leads": https://fueler.io/dhruvxr/timeline (SNIPPET; fetch BLOCKED). That this is the same person as @_dhruvxr on X is NOT verified.

## 2. How they make it (SNIPPET unless marked)
- UI built in Figma, then animated in After Effects (AGFX, Nen Creative listings above; also https://contra.com/p/bY7clAN2-ui-to-after-effects-motion-graphics-for-product-launch, title only).
- Figma to Jitter: import via the Figma plugin, edit and animate in the browser, export video, GIF or Lottie. Jitter has a tutorial for a Product Hunt launch GIF or video: https://blog.jitter.video/how-to-animate-your-figma-files/ . Jitter 1.0 launched 9 Feb 2023; Figma plugin 26 May 2021: https://www.producthunt.com/products/jitter/launches
- 3D shots: Cinema 4D with Redshift or Octane, comped in After Effects (Novra, Cleev.io above).
- Grade in DaVinci Resolve (Steve Lemuel piece above).
- Halftone / dot-matrix looks in After Effects:
  - Boris FX Sapphire HalfTone: https://borisfx.com/support/documentation/sapphire/ae/halftone/
  - BCC Halftone, "Circle or Square for dots or lines for a scanline effect": https://borisfx.com/blog/create-after-effects-halftone-plugin-2-methods/
  - Aejuice Halftone (AE, Premiere, OFX): https://aejuice.com/product/halftone/
  - AEsweets Halftone, listed at $24.99 (summary wording; page not opened): https://www.toolfarm.com/?p=22391
  - No plugin: native "Ball Action" plus other native effects: https://lesterbanks.com/2016/12/quick-simple-halftone-effect-effects/
  - Code route: Remotion documents a halftone effect: https://www.remotion.dev/docs/effects/halftone
- JUDGED (not from a source): for our ffmpeg + PIL/numpy engine, a dot-matrix form is a luminance grid sampled every N px and drawn as dots sized by brightness; this matches what the plugins above describe ("dots of varying sizes", Toolfarm listing).

## 3. Tools
| Tool | Named in a source this session? | Source |
|---|---|---|
| After Effects | yes | Novra, AGFX, Nen, Cleev.io, Launch3d (above) |
| Cinema 4D | yes | Novra, AGFX, Nen (bonus), Cleev.io |
| Redshift / Octane | yes | Novra, Cleev.io |
| Figma | yes | AGFX, Nen, Steve Lemuel, Jitter |
| Blender | yes, as "bonus" only | Nen Creative |
| DaVinci Resolve | yes | Steve Lemuel |
| Jitter | yes | Jitter blog, Product Hunt |
| Remotion | yes (halftone doc) | remotion.dev |
| Rive, Cavalry, Spline, Rotato, Screen Studio | NOT found in any source this session | UNVERIFIED, not checked |
| Glitch plugins (e.g. Red Giant Universe) | NOT found this session | UNVERIFIED, not checked |

## 4. What the top videos did differently
- Not established. No source this session gave view counts, rankings or a breakdown of top launch films. Do not cite anything here as fact.
- One seller's claim (SNIPPET): putting the product "in 3D space so viewers understand it before reading" (Novra Design, URL above). This is a sales claim, not evidence.

## 5. Music and SFX sources
| Source | What the source says | License note | URL | Status |
|---|---|---|---|---|
| Epidemic Sound | own page: 50,000+ tracks, 200,000+ SFX (other sites give lower counts) | subscription; no extra royalties once subscribed (third-party wording) | https://www.epidemicsound.com | SNIPPET |
| Artlist | music, SFX, footage, templates, plugins; "Artlist Max" bundle; SFX like "UI Designer - Processing Glitch Whoosh" | subscription license | https://artlist.io/sfx/track/ui-designer---processing-glitch-whoosh-/54633 | SNIPPET |
| Musicbed | music licensing for video, film, advertising; custom plan; no free trial; remixing needs Musicbed permission | per-track or plan | https://webcatalog.io/en/apps/musicbed/alternatives | SNIPPET (third party) |
| Uppbeat | SFX such as "Sci-fi whoosh UI click", "Subtle whoosh mouse click" | check plan terms | https://uppbeat.io/sfx/sci-fi-whoosh-ui-click/167419/57464 | SNIPPET |
| Pixabay | UI, interface and software SFX categories; Pixabay Content License said to allow commercial use without attribution, no resale as-is | verify on Pixabay's own license page (not opened) | https://pixabay.com/sound-effects/ ; license claim from https://gyre.pro/es/blog/top--websites-with-free-sound-effects | SNIPPET |
| Freesound | license varies per file; CC0 files exist | record each file's license | https://wanamelon.itch.io/dracula-nap-defense/devlog/818099/sound-effects-attribution | SNIPPET (third party) |
| Motion Array | "Digital Glitch Interferences", "Glitch Whoosh Transitions" | paid subscription | https://motionarray.com/sound-effects/glitch-whoosh-transitions-1360382/ | SNIPPET |
| AudioJungle (Envato) | "Glitchy Soft UI Click 03" | per-item license | https://audiojungle.net/item/glitchy-soft-ui-click-03/59280276 | SNIPPET |
| A Sound Effect | UI SFX library bundle (sci-fi, mechanical UI) | per-library license | https://www.asoundeffect.com/sound-library/user-interface-sound-effects-library-bundle-horror-sci-fi-musical-and-mechanical-ui-interactions | SNIPPET |

- Caveat from a guide (SNIPPET): royalty-free still has usage terms; check paid ads, broadcast and client work: https://www.studiobinder.com/blog/royalty-free-music-for-commercial-use
- JUDGED default for our spec piece: use only tracks and SFX whose license file we can save next to the project; prefer CC0 or Pixabay-licensed SFX for a no-cost draft; buy a single-track license for a client deliverable.

## 6. Blocked, not checked, open
- BLOCKED: fueler.io, getlago.com (DNS not allowed in this session). After 2 blocked hosts, stopped opening pages (tool guidance). To read them, the user must allow these domains in network settings.
- Not attempted: X/Twitter pages, Vimeo credits, Behance, YouTube descriptions.
- Not checked: any view counts, any studio's own site, any plugin price on its vendor page.
- All rows above are SNIPPET level: open each URL before quoting it to a client.
