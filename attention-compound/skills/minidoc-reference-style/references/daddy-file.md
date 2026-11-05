# The Daddy file (user's design, 19 Oct 2026)

Every video job keeps `DADDY.md` at the job root: the single source of truth for the video (intent, style law, user
verdicts, the locked script, the facts allowed on screen, production state, effects and why, an auto-generated inventory
of every shot, overlay and sound with times, and a numbered decision log). Template: `DADDY_TEMPLATE.md`. Tool:
`scripts/daddy.py` (copy into the job's tools; adapt `shows()` and `SPOKEN` to the job's people and places).

## The gate (before building ANY addition: an edit, shot, effect, motion graphic, caption change, sound, script line)
1. Write the proposal (what, kind, t0, t1, text on screen, purpose).
2. `python3 tools/daddy.py <job> check proposal.json`: automatic rules
   A1 redundancy (labels for what the viewer already knows), A2 text repeating the caption, A3 repetition, A4 caption-band
   collision, A5 numbers not in the facts table, A6 additions on rule-break moments, A7 no purpose,
   A8 multi-hit sound files, A9 splices inside words, A10 callouts that do not follow a moving graphic.
3. Six judgment questions: new for the viewer? fits the theme? does the reference do this here? what does it cost?
   does a user verdict already rule on it? is this the best form and place?
4. Verdict ADD / ADD WITH CHANGES / REJECT; log it (D-xxx); build; `daddy.py sync`; `daddy.py audit` before every render.

## Why it exists
The user caught, in one round: a pointless name card for a person on screen for 15 s, a gavel sound that hit three
times, a box drifting off its target, a cut inside "congratulations", "dollars" playing after a soundbite. Each was
a context mistake, not a craft mistake. The gate asks the context questions every time, and every new note becomes a new
automatic check (that is how A8 to A10 were added).

## Limits (say them)
- The automatic checks catch mechanical classes of mistake; taste is the six questions plus the user's verdicts.
- The audio checks measure, they do not listen: Claude cannot hear, so each audio fix still needs the user's ears.
