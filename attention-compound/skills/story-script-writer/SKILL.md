---
name: story-script-writer
description: Find the story and write a narrated mini-doc or story reel script in locked stages, scored for interest, simplicity and mass reach. Covers scene hunting, the interest score (12 checks out of 24, with the Simple group), the Attention Compound formula, plain spoken language, fact grading and read-aloud length. Use when picking an angle, turning news into a story, writing or fixing a voice-over, when a script feels like information and not a story, or when asked to score how interesting or simple a script is.
---

# Story script writer

Built on the Anthropic IPO script (3 to 4 Nov 2026). Evidence is 4 reference scripts with no retention data, and our own video has no posted results yet. Treat every number as a working guide.

## The main lesson
Our first script read as easily as the references (reading ease 80) and still failed. Only 6% of its words described something happening. The references run 40% to 79%.
**Simple words do not make a story.** Fix the story, not the words.

## The stages
Show one stage, get it locked, then write the next. Never draft the whole script first. The user questioned every part when we did that, and continuity broke.

1. **Hunt scenes.** Read around the key line in a source, not only keyword hits. Our keyword search missed the best scene, one page after the line we kept quoting. Look for moments where someone does something.
2. **Plan score.** Score the rough plan (`references/interest-score.md`). Below the pass mark, change the story.
3. **Core question.** Options with a recommendation.
4. **Outline** in bullet points.
5. **Hook**, with about half the writing time.
6. **Body**, one part at a time.
7. **Outro.** Return to a detail planted early, now changed. No lesson.
8. **Language pass.** Read aloud, simple words, cut.
9. **Title**, last.

After any locked change, recheck the lines on both sides of it.

## Story rules
- One continuous case, not a list of facts. Follow one incident all the way.
- The hook's promise must be paid by something bigger.
- Explain in one clause, then move.
- One picture carries the idea: a kill switch, three Central Parks, a fake company.
- Massy means a stranger knows a name in it, or an everyday thing makes it clear.
- Formula and checks: `references/ac-formula.md`.

## Language (from 2 Varun Mayya reels and the user's notes)
- The problem was not long words. Fragments averaging 7.4 words read as hard. His sentences average 11 to 12.
- Full sentences, as you would say them to a friend. One idea each.
- Link each line to the last with So, That or But.
- After a fact, say plainly what it means.
- Replace metaphors that need decoding. "Fake" beat "pretend". "Brakes" was dropped from the words.
- The picture carries the proof. Say "here" and show it.

## Length
- Use the real read, not a word-count guess. Lock the length before the storyboard.
- References: about 250 to 280 words, 72 to 87 s, 180 to 210 words a minute.
- Our 292-word script ran 1:52 at the voice's 159 words a minute, about 25 s over the references. Test the voice's pace before you trim.
- Mark boring or not relatable lines before they get pictures. Keep every longer version.

## Facts
- Grade each fact: A read at the primary source, B reporting that cites it, C reported or estimated. Only use what you can back up.
- Check the user's named examples before building on them. One incident we were given belonged to a different company.
- Keep a "must not say" list and what the source does not claim.
- Recheck any time-sensitive line on posting day. Never fabricate numbers or quotes.
- No investment advice. If Claude's maker is the subject, flag the conflict and let the user decide the framing.

## Scoring tool
`scripts/interest_score.py` measures a script you have tagged line by line. It counts. It does not judge. See `references/interest-score.md`.

## Worked example
`examples/anthropic-ipo/` in this pack: `STORY-SCRIPT_v1-parts.md`, `STORY-SCRIPT_v5.txt`, `STORY-LIBRARY.md`.
