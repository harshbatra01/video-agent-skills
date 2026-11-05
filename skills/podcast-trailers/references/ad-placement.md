# Ad placement: where the sponsor reads go

Given a podcast transcript and one or more ad reads to insert, find the single best spot for each one and hand the
editor exact phrases they can search in their NLE's transcript panel to land on the cut. The episode is already
recorded, the ad reads exist, and the only question is *where they go*.

The deliverable is not a timestamp. Editors place cuts by searching the transcript panel (Premiere, DaVinci Resolve),
so the product is **short, unique, plain-English search phrases** plus a clear instruction of where to cut relative to
each one. Get that right and the editor is done in seconds.

## What to gather first
- **The transcript** (`scripts/transcribe.py` makes one, or use Premiere's own transcript through `premiere-ae-editing`
  `scripts/prproj/prtranscript.py`). The whole method runs on transcript text.
- **The ad reads to place**, and their **required order** if the user gives one. Order is a hard constraint (for
  example "AI ad first, then airline, then personal injury").
- **How they want them spaced**, usually "evenly". Take this seriously; it drives placement.
- **Any thematic wishes**, such as the airline ad near travel talk.

If the user is terse or short of time (common), do not interrogate them. Infer sensible defaults, place the ads, and say
what you assumed.

## Step 1: Map the episode
Build a rough table of contents: which segment covers what, and roughly where it sits. Two things matter most:
- **The climax or thesis peak**: the big reveal, the emotional high, the "this is the most important thing I'll say"
  moment. Ads must NOT interrupt it; an ad dropped into the best moment kills the moment and the ad gets resented. Ads
  belong in the cool-down right after a peak.
- **The main / bonus boundary**: many shows add paywalled bonus content at the end ("questions for our Plus members",
  "bonus round"). Ads do not belong there, because sponsors pay for the main feed. Find where the host says the regular
  episode is over and treat everything after it as off-limits. A case-insensitive search of the transcript (the Grep
  tool) for `plus member|bonus|regular episode|patreon` usually finds it.

For rough positions, word counts per chunk give cumulative percentages, so any line becomes an approximate "% through
the episode". Compute percentages against the **main** episode (up to the bonus boundary), not the full file.

## Step 2: Find candidate breaks
Scan for **clean topic seams**, where a segment finishes and a new one starts:
- an explicit reset: *"OK, let's pick up the story"*, *"so, back to..."*;
- a fresh question that opens a new segment: *"Does X actually...?"*, *"let me ask you about..."*;
- a wrap-up line (*"...and that's the whole point"*) before the subject changes.

Avoid, always: the middle of a story, the middle of a thought, and the climax. Read the words on both sides of the seam
too (our lesson from mid-video inserts): a sentence can run across what looks like a clean change of subject, and an
insert there splits it. Move the cut into a real pause before the sentence.

Two things turn a usable break into a great one:
- **A retention hook right before it.** If the host just teased something ("by the end of this episode you'll walk away
  with concrete stuff about X") or ended on a cliffhanger question, that is the ideal pre-ad moment, because the
  listener stays through the break to get the payoff.
- **A thematic bridge.** An ad that hands off from related content feels native and converts better. Before placing
  each ad, search the transcript for the ad's own topic and see whether a seam sits nearby. Examples that paid off: an
  airline ad right after the hosts debated whether to fly somewhere right now; an AI-software ad right after a riff on
  AI changing the world.

Thematic bridges are worth bending the spacing for, but only a little. If the themed seam is close to where even
spacing wants the ad, take it; if it is far out of position, a clean neutral seam at the right spot beats a themed one
that bunches the ads.

## Step 3: Place the ads
- **Order is fixed.** If the user said AI, then airline, then injury, the AI ad is the earliest regardless of where the
  AI content sits. A lead ad on a clean cliffhanger beats a perfectly themed ad in the wrong order.
- **Even spacing** means even gaps between consecutive ads across the main episode. For N ads, aim near each 1/(N+1)
  mark (3 ads: about 25%, 50%, 75%), then snap each to the nearest clean seam. The lead-in before the first ad and the
  tail after the last can be a bit longer (you do not ad-break the very open or the very close), but the middle gaps
  should look even; nudge one ad to a neighbouring seam if snapping leaves one gap much tighter.

## Step 4: Deliver
Give **one spot per ad**, not a menu: the editor wants a decision. For finding that spot, give **two or three search
phrases**, because the NLE's transcript may differ slightly from yours. Every phrase must be:
- **Unique**: search the transcript for it (the Grep tool, case-insensitive) before handing it over; a phrase that
  appears twice lands in the wrong place. If the episode sits in a Premiere project, check against Premiere's own
  transcript, the one the editor searches.
- **Plain English**: no transliterated names, foreign words or religious terms, which Whisper and the NLE mangle
  differently. "the first group of the 6,000" is safe; a transliterated phrase is not.

State exactly where the cut goes relative to the phrase ("drop the ad right after this line" / "right before this
line"), so the hand-off and the return both land clean.

### Output format
Lead with a one-line confirmation (how many ads, in what order, evenly spaced, all inside the main episode). Then per
ad:
```
**<n>. <Ad name>: ~<X>% in (<rough location, e.g. "first quarter">)**
Search (any one): `phrase A` · `phrase B` · `phrase C`
Cut: drop the ad <right after | right before> "<the anchor line>".
Why: <one sentence: the seam, plus any thematic bridge or retention hook>.
```
Close with the guardrail: name the phrase that marks the bonus boundary and say not to place anything after it. Keep it
scannable: no hedging, no alternative spots.

## Why these rules
- **Search phrases, not timestamps**, because that is how the cut gets made, and unique plain-English phrases are the
  only ones that survive the round trip between two different transcripts.
- **Even spacing across the main episode**, because ads in paywalled bonus content are wasted and even gaps keep the
  listener from feeling ad-flooded in one stretch.
- **Never interrupt the climax; break on a hook**, because retention through the ad is the whole game.
- **Thematic bridges where they fall naturally**, because a themed hand-off reads as part of the show.
- **One spot, many phrases**, because the editor wants a decision plus enough redundancy to find it.
