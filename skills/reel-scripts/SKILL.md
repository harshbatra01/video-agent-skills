---
name: reel-scripts
description: Write voice-over scripts for short-form story reels, faceless mini-docs and founder or expert reels. Covers cinematic story scripts (a hook with a famous name or a number, an open loop, a "But" turn, dated scenes, a payoff, a callback kicker), reels written in a real person's own voice from their posts and talks, and AI voice paste blocks (ElevenLabs v3) with at most one or two audio tags. Use it whenever the user asks for a reel script, a VO, a voice-over for an edit, a story reel about a news event or a person, a script "in the style of" a creator, hooks, or an AI voice read, even if they only say "write me something about X for the page". Delivers the voice-over only unless asked for more.
---

# Reel and mini-doc scripts

The voice-over sets the timing of the whole edit, so the script comes before any storyboard or build. These rules come
from a reviewer's notes on story and founder scripts written in October 2026 and from a study of 93 reels of a faceless
mini-doc page. Lessons from our own reviews that apply to scripts are folded in and marked "(ours)".

## What to deliver
- **Just the voice-over**, plus one line with the word count and the estimated length. The reviewer: "dont do footage
  on screen and material. just the voiceover script" and "no need for source as well". Add on-screen notes, footage
  lists, alternate hooks or sources only when asked.
- **Facts checked privately first** against the company's own posts, filings and reliable outlets, newest developments
  included. Leave out what you cannot back up, and say in chat (not in the script) which claims move fast and need a
  check before recording.
- **Never invent a number, a poll result, a quote or a stat** (ours). If a hook needs a number, find a real one or pick
  a different hook.
- **An AI voice paste block** when the voice will be generated: the same text with one or two audio tags at most, saved
  for the moment that matters; pacing comes from ellipses and line breaks (`references/voice-and-elevenlabs.md`).
- **No em dashes** anywhere, the voice-over included.
- **An editable document.** The user edits scripts themselves: build on their edited version, suggest changes in chat,
  never overwrite their copy.
- **Check the client's rules first** (ours): some clients want no AI voice at all, or none in certain formats. Their
  project file says so.

## Pick the register
| Script | Voice | Rules |
|---|---|---|
| Story reel in a reference creator's style (theme pages, mini-docs) | dramatic and cinematic: present tense, short fragments allowed, date and place stamps, question-and-answer twists, "But" turns, a kicker that calls back to the hook | `references/story-reel-formula.md` |
| Founder or expert reel in that person's voice | how they talk and write, at their measured speaking pace | `references/founder-reels.md` |
| Calm explainer, trailer bridge, client copy | plain full sentences, natural connectives, no slogans or announcer fragments, no proper names in an AI read | this file; trailers in the `podcast-trailers` skill |

Plain prose governs client copy, documents and calm explainers. Dramatic story reels are the one exception: there the
reference style is what earns the views, and plain narration was called boring.

## How a story script gets written
1. **Research deeply first**: the backstory (often a chapter from years earlier) and the last 48 hours of news. A recap
   in date order "reads as boring even when every fact is right".
2. **Pass the logline test** (ours): one sentence a stranger understands, such as "they try X, then Y happens". Every
   beat must serve it. If you cannot write that sentence, the story is not ready.
3. **Find the scenes and the payoff**: a cold-open scene with concrete details, a frame the hook sets up ("stolen
   twice" sets up two acts), a detail planted early that pays off at the end.
4. **Write to the skeleton**: a hook of about 12 words with a famous name or a number, finished inside 3.5 s; an open
   loop by about 17%; the "But" turn near the middle; the climax as short beats; a callback kicker or a viewer-facing
   hypothetical to close. No business lesson unless asked: on the studied page, story-only reels beat lesson reels by a
   wide margin.
5. **Length**: most reference reels run 72 to 91 s, about 246 words at about 190 wpm; the longest ran 363 words.
6. **Read it as the narrator** before delivering: every sentence speakable in one breath, numbers written the way they
   are said, names the voice engine can pronounce (or kept off the read).

## Interest first (ours)
A new page gets no reach from loyalty, only from the story and the first seconds. Before writing, check that the topic
is fresh or carries real tension, and that the first line alone would stop a stranger. Judge a script by what it will
do for retention, click-through and average view duration, not by how clever it is. Drop a weak story instead of
filling a quota.

## Check the read after recording or generating (our tools)
These scripts live in the `premiere-ae-editing` skill (paths are relative to that skill):
- Word timings of a take: `python scripts/media/hear.py take.wav take.json names.txt` (names.txt lists names it must
  spell). It runs on both machines: faster-whisper on Windows; on an Apple Silicon Mac run it with the mlx-whisper
  venv's Python (`~/.venvs/mlx-whisper/bin/python`), where the names list only primes the first 30 s, so check names
  by ear (premiere-ae-editing `references/timing.md`). Compare the words with the script: a missing short word is a
  swallowed word.
- Tighter alignment to catch swallowed words: WhisperX forced alignment (premiere-ae-editing `references/timing.md`,
  "Long raw footage"). It was set up on an NVIDIA GPU; on a Mac it runs on the CPU or MPS, several times slower
  (premiere-ae-editing `references/mac-notes.md`).
- Loudness: `python scripts/media/atools.py take.wav` (about -16 LUFS for a mastered voice-over file).
- For a plain segment transcript of a long recording, the `podcast-trailers` skill's `scripts/transcribe.py` works on
  either machine.
Installing anything for this is the user's call: say the name, the source and the size first.

## Which reference to read
| You need | Read |
|---|---|
| The measured story formula, what performed, hook types, a rewrite example | `references/story-reel-formula.md` |
| Founder reels: reference accounts, the measured format, learning someone's voice | `references/founder-reels.md` |
| ElevenLabs tags and settings, consented voice clones, local models | `references/voice-and-elevenlabs.md` |

Sources: a friend's Mac skill set (Oct 2026), with lessons from our own jobs (Sept to Oct 2026) marked "(ours)".
