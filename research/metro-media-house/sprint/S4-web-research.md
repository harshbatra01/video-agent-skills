# S4 Web research: who makes the Metro Media House style, how, and what top videos do

Status: done (sprint scope; gaps listed in sections 1 to 3)

Sprint window 13:21 to 13:25:30 IST, 2026-11-05. Standard web search only. Source strength is marked: STRONG (official docs, named outlet), WEAK (vendor, affiliate, forum, digest, or search-summary attribution I did not open).

## Main finding

The open web has almost nothing about Metro Media House itself or about named faceless business mini-doc studios; the useful, sourceable material is on technique (After Effects mosaic and grid reveals, word-by-word caption tools) and on comment-to-DM funnels, where all numbers are vendor self-reports.

## 1. Who makes this style

- Metro Media House: a standard search for "Metro Media House" Instagram returned no account page, owner, founder, or agency site. Results were unrelated Metro brands such as West Midlands Metro and Metro TV Indonesia. Owner is UNKNOWN from the open web. (search 13:21 IST; example unrelated hit: https://westmidlandsmetro.com/west-midlands-metro-launches-instagram-account)
- A second query ("metromediahouse" OR "Metro Media House" business stories reels founder) also returned only unrelated Metro brands, such as Metro magazine NZ, Metro Dutch newspaper and Metro TV Indonesia. (https://en.wikipedia.org/wiki/Metro_(magazine) , https://en.wikipedia.org/wiki/Metro_(Dutch_newspaper))
- Similar faceless business pages: a search for faceless business backstory mini-doc pages surfaced only generic paid "faceless reels" guides, not named studios. WEAK, marketing. (https://flowshorts.app/faceless-reels/business , https://fluxnote.io/guides/faceless-instagram-reels-content-strategy)
- One guide says faceless business Reels with infographic animation, revenue screenshots and text overlays get saves and shares, and suggests alternating tactical posts with story posts (failures, pivots, timelines). WEAK, vendor. (https://fluxnote.io/guides/faceless-instagram-reels-content-strategy)
- USVC-style sponsored reels: no result named USVC or an agency that makes these. Nearest context: Slow Ventures launched a 60 million dollar fund to invest in online creators (Bloomberg via BNN, Feb 2025). STRONG for that fact, but it is not an agency. (https://bnnbloomberg.ca/business/company-news/2025/02/13/former-facebook-employees-launch-venture-fund-for-social-media-influencers)
- A 2026 guide claims US brands put over 4 billion dollars into Instagram influencer partnerships in 2025. WEAK, unsourced vendor figure. (https://fluxnote.io/guides/instagram-reels-brand-deals-us-2026)
- Gap: who runs Metro Media House and which agency produces the USVC reels needs a manual Instagram check (bio link, "Paid partnership" label, collab tags), which this sandbox cannot do.

## 2. How it is made (tools and tutorials)

### 3x3 white block photo reveal
- After Effects: CC Image Wipe with Gradient Source set to Mosaic, keyframe Completion 100 to 0 percent to uncover the layer below. WEAK, forum answer. (https://community.adobe.com/t5/after-effects-discussions/reveal-a-photo-through-mosaic-squares/m-p/9286376)
- After Effects: lay out the grid, pre-compose, then Card Wipe or Card Dance for the reveal. WEAK, forum, attribution from a search summary, thread not opened. (https://community.adobe.com/t5/after-effects-discussions/grid-of-headshot-photos-popping-in/m-p/13267968)
- Reels grid effect tutorial: white solid background, duplicate it, apply the Grid effect, then animate. WEAK, third-party digest of a YouTube tutorial. (https://recapio.com/digest/how-to-create-a-viral-instagram-reels-grid-effect-in-after-effects-beginner-tutorial-ep-1-by-motionw)
- Paid or free templates: Motion Array geometric grid transitions (https://motionarray.com/after-effects-templates/geometric-grid-transitions-962328/), Videohive grid transition (https://videohive.net/item/grid-transition-for-after-effects/36431028), Mixkit free grid templates (https://mixkit.co/free-after-effects-templates/grid/). Template pages, not proof Metro uses them.
- Our inference, not sourced: nine white rectangles that drop out one by one on beat is trivial to build in code, so we do not need After Effects for this device.

### Word-by-word captions
- Submagic sells word-by-word highlight, bounce and fade caption templates. WEAK, vendor page. (https://www.submagic.co/ai-caption)
- CapCut auto-captions include highlight and karaoke styles that animate words in time with audio; one comparison says CapCut has fewer word-level styles than Submagic. WEAK, affiliate. (https://freeacademy.ai/lessons/ai-video-editing-auto-captions , https://fluxnote.io/guides/submagic-vs-capcut-captions-2026)
- An Adobe Premiere Pro ideas thread asks for automatic word-by-word caption colouring like the Captions app, which suggests Premiere did not do this natively when posted. WEAK, user request. (https://community.adobe.com/t5/premiere-pro-ideas/captions-change-colors-word-by-word-automatic-same-that-captions-ai-app/m-p/14387618)
- Note: Metro's captions are small white words spread across mid-frame, not the bouncing highlighted style these tools default to, so a custom renderer is closer than any preset (our inference from STUDY.md section 5).

### Single colour-inverted frame cut
- Premiere: Effects > Video Effects > Channel > Invert; one answer suggests the Lightness channel option and desaturating the negative with a colour corrector; another suggests Levels with keyframed gamma. A related tip uses a full-frame white box for 1 to 2 frames as a flash. WEAK, forum. (https://community.adobe.com/t5/premiere-pro/video-effects-for-a-horror-thriller-trailer/m-p/5798185)
- Justin Odisho tutorial, flashing invert colour effect in Premiere, via a link roundup. WEAK, secondary. (https://premierebro.squarespace.com/premiere-in-post/justin-odisho-flashing-invert-color-effect-adobe-premiere-pro)
- Our inference: razor the clip so one frame is isolated, invert only that frame. In ffmpeg this is a negate filter on one frame index.

### Paper cards, polaroids, cut-out subjects
- Documentary-style newspaper effect, no plugins: cut-outs, masks, camera-flash hits, cut-outs parented to a null and nudged in position and scale. WEAK, digest of a YouTube tutorial, but closest match to the Metro look. (https://recapio.com/digest/documentary-style-newspaper-effect-in-after-effects-after-effects-tutorial-no-plugins-by-motion-nati)
- Ben Marriott paper cut-out look (Wiggle Paths for rough edges), project file on Gumroad. (https://lesterbanks.com/2020/02/an-easy-way-to-get-a-paper-cutout-stop-motion-look-in-ae/ , https://benmarriott.gumroad.com/l/NDtPol)
- Drop shadows so cut-outs sit on a surface. WEAK, blog. (https://medium.com/@MilesOfRoses/create-a-paper-cut-out-animation-with-after-effects-e4891f6aba95)
- Jake Bartlett, The Paper Cutout Look in After Effects (Skillshare course). (https://www.skillshare.com/en/classes/the-paper-cutout-look-in-adobe-after-effects/239727349)
- Gap: no tutorial found for the polaroid frame or the person cut-out on a swapped background specifically.

## 3. What top videos in this niche do

- Length: one strategy guide says keep Reels scripts to 60 to 90 seconds. Metro runs 80 to 95 s, at or past that edge. WEAK. (https://fluxnote.io/guides/faceless-instagram-reels-content-strategy)
- Comment-to-get CTA numbers (all vendor self-reports, WEAK):
  - ReplyRush case study, 30 days: 12,640 unique users got a DM, 38.9 percent link click-through from the first DM, followers 24,380 to 29,507. (https://www.replyrush.com/post/case-study-5k-followers-in-30-days-using-replyrush-dm-automation)
  - Zernio claims comment-to-DM gets 90 percent plus open rates versus about 20 percent for email, no method given. (https://zernio.com/comment-to-dm)
  - ManyChat success stories report hundreds of opt-ins and a few thousand dollars from one keyword post. (https://manychat.com/blog/success-stories/pink-sparrow-social/ , https://manychat.com/blog/success-stories/monty-lans/)
  - Risk: a ManyChat community thread reports a viral Reel where the automation fired on only a small share of keyword comments. (https://community.manychat.com/general-q-a-43/instagram-reel-automation-only-triggered-for-a-small-percentage-of-comments-on-a-viral-post-8118)
- No independent benchmark for keyword-comment conversion was found.
- Landscape vs vertical: no Meta or Mosseri data comparing 16:9 and 9:16 Reels was found. Vendor guides recommend 9:16 and say 16:9 shows with bars in Reels placements, with no data. WEAK. (https://socialrails.com/blog/instagram-video-size-format-specifications-guide , https://manychat.com/blog/the-right-instagram-reel-size/)
- Meta is reported to be testing a home for horizontal video on TV while keeping vertical Reels. Medium strength, trade news. (https://ppc.land/instagrams-vertical-video-problem-why-horizontal-matters-on-tv/)
- So Metro's landscape choice is a deliberate "documentary" signal, not a proven reach tactic (our inference).
- Not found in time: hook-type data, words-per-minute benchmarks, top-video view counts for this niche.

## 4. Source list

- https://westmidlandsmetro.com/west-midlands-metro-launches-instagram-account : example of the unrelated hits for "Metro Media House".
- https://flowshorts.app/faceless-reels/business : faceless business reels tool page, WEAK.
- https://fluxnote.io/guides/faceless-instagram-reels-content-strategy : faceless strategy guide, 60 to 90 s advice, WEAK.
- https://fluxnote.io/guides/instagram-reels-brand-deals-us-2026 : sponsored Reels guide, 4 billion dollar claim, WEAK.
- https://bnnbloomberg.ca/business/company-news/2025/02/13/former-facebook-employees-launch-venture-fund-for-social-media-influencers : Slow Ventures 60 million dollar creator fund.
- https://community.adobe.com/t5/after-effects-discussions/reveal-a-photo-through-mosaic-squares/m-p/9286376 : CC Image Wipe Mosaic photo reveal.
- https://community.adobe.com/t5/after-effects-discussions/grid-of-headshot-photos-popping-in/m-p/13267968 : grid of photos popping in, Card Wipe tip, not opened.
- https://recapio.com/digest/how-to-create-a-viral-instagram-reels-grid-effect-in-after-effects-beginner-tutorial-ep-1-by-motionw : Reels grid effect tutorial digest.
- https://motionarray.com/after-effects-templates/geometric-grid-transitions-962328/ : grid transition template.
- https://videohive.net/item/grid-transition-for-after-effects/36431028 : grid transition template.
- https://mixkit.co/free-after-effects-templates/grid/ : free grid templates.
- https://www.submagic.co/ai-caption : Submagic word-by-word caption tool, vendor.
- https://freeacademy.ai/lessons/ai-video-editing-auto-captions : CapCut auto-captions lesson.
- https://fluxnote.io/guides/submagic-vs-capcut-captions-2026 : Submagic vs CapCut comparison, affiliate.
- https://community.adobe.com/t5/premiere-pro-ideas/captions-change-colors-word-by-word-automatic-same-that-captions-ai-app/m-p/14387618 : Premiere feature request for word-by-word captions.
- https://community.adobe.com/t5/premiere-pro/video-effects-for-a-horror-thriller-trailer/m-p/5798185 : Premiere invert and flash frame advice.
- https://premierebro.squarespace.com/premiere-in-post/justin-odisho-flashing-invert-color-effect-adobe-premiere-pro : flashing invert tutorial link.
- https://recapio.com/digest/documentary-style-newspaper-effect-in-after-effects-after-effects-tutorial-no-plugins-by-motion-nati : documentary newspaper cut-out look.
- https://lesterbanks.com/2020/02/an-easy-way-to-get-a-paper-cutout-stop-motion-look-in-ae/ : Ben Marriott paper cut-out technique.
- https://benmarriott.gumroad.com/l/NDtPol : paper cut-out project file.
- https://medium.com/@MilesOfRoses/create-a-paper-cut-out-animation-with-after-effects-e4891f6aba95 : paper cut-out with drop shadows.
- https://www.skillshare.com/en/classes/the-paper-cutout-look-in-adobe-after-effects/239727349 : paper cut-out course.
- https://www.replyrush.com/post/case-study-5k-followers-in-30-days-using-replyrush-dm-automation : comment-to-DM case study numbers, vendor.
- https://zernio.com/comment-to-dm : comment-to-DM open-rate claim, vendor.
- https://manychat.com/blog/success-stories/pink-sparrow-social/ : ManyChat keyword case study.
- https://manychat.com/blog/success-stories/monty-lans/ : ManyChat keyword case study.
- https://community.manychat.com/general-q-a-43/instagram-reel-automation-only-triggered-for-a-small-percentage-of-comments-on-a-viral-post-8118 : automation missing comments on a viral Reel.
- https://socialrails.com/blog/instagram-video-size-format-specifications-guide : Reels format guide, WEAK.
- https://manychat.com/blog/the-right-instagram-reel-size/ : Reels size guide, vendor.
- https://ppc.land/instagrams-vertical-video-problem-why-horizontal-matters-on-tv/ : Meta testing horizontal video on TV.
