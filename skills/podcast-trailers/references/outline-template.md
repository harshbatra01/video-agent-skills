# Outline structure

The section order below is what the client is used to reading. Keep it. Written to
`<Show> x <Guest> - INTRO OUTLINE.md`.

The cut itself is a **scene script** (client examples, August 2026): scene blocks of stacked verbatim lines, VO segments
woven between them as the narrative spine, sparing bracketed production directions at pivotal moments, and a `Search:`
line per scene. No numbered beats, no `{ }` cue lines, no `( )` rationale.

```markdown
# <Show> x <Guest> - Intro / Trailer Outline (for client approval)

<Two or three sentences: who the guest is, what happened, why this episode exists,
written for a reader outside the show's world (gloss every in-world term). Name anyone
whose name appears later so the reader is never guessing.>

Tone: <one line. What register the cut is in and what it deliberately avoids.>

Framework: **Hook > Life Lesson > Emotional Rollercoaster > Always Leave Wanting More**
Written as a scene script. Quotes are word for word in short stacked lines; a new line
implies its own cut and `...` marks a cut inside a line. Timecode ranges are source in
and out points. VO lines are read by the AI voice (no names in the read); bracketed
lines are production directions. The backticked phrases under each scene paste
straight into the Premiere transcript panel. Runs about <N> seconds as scripted.

## The episode map
- **mm:ss** <Plain-English chunk name>. "<the host question that opens the chunk, word
  for word>" <One clause of what happens, glossed for a reader outside the show's world.>
<Ten to thirteen rows for an hour, pre-interview chatter included so the editor sees
where the episode proper starts. One line per chunk.>

## The arc
<One short paragraph tracing the scenes in order, naming which loops stay open. The
episode holds every payoff.>

---

## The cut

[OPEN]

**<GUEST>** *(mm:ss-mm:ss)*

"<verbatim line>"

"<verbatim line>"

[<DIRECTION AT THE CUT, IF THE CUT NEEDS STATING>]

Search: `phrase one` · `phrase two`

VO:

<The card VO. Resolves the opening withhold without proper names.>

<Second stacked line.>

[TITLE CARD. MUSIC IN. Card text on screen, not read aloud: <the names and titles the
VO is not saying>.]

**<HOST>** *(mm:ss-mm:ss)*

"<verbatim line>"

Search: `phrase one` · `phrase two`

VO:

<One-line bridge handing the viewer the fact the next scene assumes.>

**<GUEST>** *(mm:ss-mm:ss)*

"<verbatim line>"

"<verbatim line>"

Search: `phrase one` · `phrase two`

VO:

<The question the final scene answers.>

**<GUEST>** *(mm:ss-mm:ss)*

"<the closing thought, complete>"

[MUSIC OUT. LET IT LAND. ONE BEAT OF AIR. LOGO.]

Search: `phrase one` · `phrase two`

---

## VO, tagged for ElevenLabs

ElevenLabs v3, stability 60 to 70, comp from four or five takes. At most one or two audio
tags per read. No names anywhere in the reads; the card carries them.

<One fenced block per VO segment, in script order.>

## Music and pacing
- <two or three bullets; the bracketed directions in the script mark every move>

## Swaps and alternates
- **Softer open:** <alternative opening in-point>
- **Harder ending:** <the smash-to-black cliffhanger cut, only if the client asks.
  Recommend the clean close.>
- **Tighten toward <N>s:** <which scene drops first>

## What we would need
- <assets that must come from the client or family>
- <sign-off on the card copy, since the VO speaks no names>
- <client sign-off before editing starts>

---

Notes: every quoted line is word for word from the transcript; a new stacked line
implies its own cut and `...` marks a cut inside a line; timecode ranges are source in
and out points. <Name and spelling confirmations, and anything deliberately left out
and why.> This is the trailer only.
```

The angle-bracket slots above are template placeholders. `verify_outline.py` flags short ones left in the finished
outline (such as `<Show>` or `<verbatim line>`); check the long descriptive slots by eye.

## Scene shape

Five or six scenes plus three to five VO segments is typical for 80 to 90 seconds. The default distribution,
strongest-first:

| Slot | Job |
|------|-----|
| Open | The episode's single strongest moment, cut before its own payoff finishes. |
| Card VO | Resolves the opening withhold and orients without proper names; the on-screen card text carries the names. Never touches the closer. |
| Scene 2 | The claim. A number, fact, or contrarian opinion that frames the episode. |
| Scene 3 | Mid-cut cliffhanger. A decision or a defiance, cut before the outcome. |
| Scene 4 | The cost. The private spiral or the emotional core, cut before its resolution. |
| Final scene | Clean close. A complete thought that gives the cut its meaning and breathes before the logo, ideally gesturing at something the middle withheld. |

A quick host-guest exchange from one moment plays as a single scene, and often better than a monologue: question,
answer, echo. The middle scenes are the ones that must be continuous passages; if the episode has only two long
uninterrupted runs, they are scenes 3 and 4.

## Stacked lines and elisions

Break a passage into stacked lines at sentence boundaries: each line is one breath the editor can keep or drop. A new
line implies a cut, so consecutive lines need not be contiguous on tape, but every line stays verbatim inside itself.
When words are dropped inside a single line, show it:

```
"I can't explain the pain. It's unbearable... you feel like you're dying."
```

`verify_outline.py` parses both the scene-script format (bold speaker headers with bare stacked quote lines under them)
and the older `**Speaker:** "..."` inline form, which the Swaps section still uses. Straight and curly quotes both work.
VO lines are narration, not tape; the script skips them.
