# Voice-over

One intro-card voice-over, roughly 12 seconds, sitting after the hook. Its job is to orient someone who has just been
hit with 20 seconds of raw tape and does not yet know who they are listening to.

**No proper names in the read** (client feedback, August 2026). The AI voice mispronounces names often enough that
people, organisations, places and foreign terms all stay out of the spoken voice-over. The on-screen title card carries
the names as text; the voice-over describes instead: "a mother of four", "the founder of an air ambulance company",
"the schools that raised him". Write the card text into the outline next to the voice-over so the client sees both.

It states what happened and what the episode is about. When the opening hook is cut before its payoff, the voice-over
resolves it: state the withheld fact plainly, then pivot to what the episode contains. But **never re-state what the
audio just said** (client feedback, July 2026): if the hook plays its payoff, the voice-over carries who the guest is
instead (role, what they built, why they are worth an hour, all without the name). It **never gives away the closing
scene or any reveal the middle is withholding**.

Deliver it twice: clean prose first (so the client can read it), then tagged (so it can be pasted into ElevenLabs).

## Length
Twelve seconds is about 30 to 35 words at the slow, weighted pace these reads want. Cut adjectives before facts.

## Structure that works
> "Twelve years ago, she sold her bakery to pay for her son's treatment. This is the debt she never mentions, the town
> that showed up anyway, and a promise she has kept every morning since."

(An invented example.) Three moves: **the fact**, then **what the episode contains** as a list of three (which gives the
read its cadence), then **an image that hints at the ending without naming it**. The pronoun is safe because the hook
just showed her; the card under the read says who she is by name.

## The interleaved segments
Two to four more short segments sit between scenes as the cut's narrative spine. Each is one to four short stacked
lines doing exactly one job:
- **Hand the viewer the fact the tape assumes** ("All of it gets raised one ask at a time.").
- **Turn the story** ("There was just one problem. They didn't have a building." / "Then everything changed.").
- **Ask the question the next scene answers** ("So after all of it... what actually counts?").
Same rules: no proper names, plain English, never re-state the adjacent tape, never touch the closer. Short stacked
lines, not paragraphs. Prefer the host's real question on tape over a voice-over bridge whenever it does the same job.

Plain spoken sentences, not announcer fragments: "Husbands are his whole job. This hour: the test every husband
fails..." was rejected as reading horribly, while "He's a husband coach. Guys who love their wives and still get it
wrong, that's who he works with all day." read like a person talking. Keep lines short and plain; "conversational" did
not mean chatty or longer.

## ElevenLabs v3 tags
**House rule (Oct 2026): at most one or two audio tags per read**, saved for the moment that matters. A block with a tag
on nearly every line was rejected ("dont use this many tags"). Ellipses and line breaks do the pacing.

| Tag | Use |
|-----|-----|
| `[long pause]` | before the turn, where the weight sits |
| `[whispers]` | the very last clause only |
| `[exhales]` | a breath before something hard; easy to overuse |
| `[quietly]` `[softly]` `[gently]` | a drop in volume and intensity |
| `[slowly]` | stretches the following phrase |
| `[somber]` | overall register, once at the top if at all |

Tagged version of the example:
```
Twelve years ago... she sold her bakery... to pay for her son's treatment.

[long pause] This is the debt she never mentions... the town that showed up anyway...
and a promise [whispers] she has kept every morning since.
```

## Settings and workflow
- Stability 60 to 70 (lower wanders between takes; higher flattens out).
- No names in the read. If the client insists on one, respell it phonetically, flag it, and get their sign-off on the
  pronunciation before delivery.
- Generate four or five takes and comp the best pieces. If a voice over-acts, remove `[exhales]` first.
- The ElevenLabs key lives in an environment variable the user sets; never view, print or store it.
- Check each take against its script before delivery (`premiere-ae-editing` `scripts/media/hear.py` for word timings on
  Windows or a Mac, or this skill's `scripts/transcribe.py` for a quick segment transcript): a missing short word is a
  swallowed word.
