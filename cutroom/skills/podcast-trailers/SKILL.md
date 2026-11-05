---
name: podcast-trailers
description: Turn a podcast or interview episode (audio, video or a transcript) into a client-approval intro, trailer or cold-open outline, with verbatim quotes, unique transcript search phrases an editor pastes into Premiere, a scene script, an AI voice-over with no proper names in the read, and a published page the client can open. Also places ad reads and sponsor spots evenly through an episode, and plans cold opens with b-roll and graphics for interview shows. Use it whenever the user hands over a podcast episode and asks for an intro, trailer, teaser, cold open, "the intro segments", powerful moments, best lines, cliffhanger cut points, a written outline to send a client before editing, where to put the ad reads, or "here's the episode, do your thing", even if they name only one piece (just the transcript, just the VO, just the search phrases).
---

# Podcast trailers, cold opens and ad spots

A podcast episode comes in as audio. What goes back first is a written outline the client approves BEFORE any editing
happens, plus a published page of it they can forward. Nobody is watching you work, so the outline has to survive being
read cold by someone who was not in the conversation.

The deliverable is not a summary of the episode. It is a **cut list**: exact words, in order, that an editor can
assemble into a 60 to 90 second opener without going back to the source to work out what you meant.

Other jobs in this skill: ad placement (`references/ad-placement.md`) and cold opens built with b-roll, archive and
motion graphics for interview shows (`references/cold-open-edits.md`).

Scripts below run with `python` on Windows and `python3` on a Mac; paths are relative to this skill's folder.

## The pipeline
1. Transcribe the audio.
2. Verify the proper nouns (speech-to-text gets names wrong, reliably).
3. Read for the story, pick the scenes.
4. Write the outline, quoting **word for word**.
5. Verify with the bundled script before showing anyone.
6. Publish the page.
7. Script the voice-over for ElevenLabs.

Steps 4 and 5 are where this lives or dies. Read "The four rules" before writing a single scene.

## Run it end to end without stopping
The user edits a lot of episodes and does not want to steer each one. Given an audio file, go all the way to a
published page and a voice-over in one pass; say you are starting, then work.

| Question | Default |
|---|---|
| Where do outputs go? | Beside the audio file, same folder |
| Show and guest names | Infer from the filename, confirm against the first two minutes, where hosts introduce the guest |
| File naming | `<Show> x <Guest> Transcript.srt/.txt`, `<Show> x <Guest> - INTRO OUTLINE.md` |
| Length | about 80 seconds, five or six scenes |
| Publish the page? | Yes, as a private artifact. It is a deliverable, not an extra; the user decides who gets the link |
| Palette | Infer from the content (see "Reading the register") |
| A name is ambiguous | Search the web, pick the best-supported spelling, use it everywhere, note the uncertainty in the footer |
| A great line sits in paywalled bonus content | Leave it out and say why |

Stop and ask only when something is genuinely blocking: the audio is unreadable, the episode has no story, or the file
is not what it claims to be. **Revisions are the exception**: once a page is published the client may have the link, so
say what you intend to change and wait before republishing.

## Reading the register
- **Loss, illness, memorial**: somber palette, long holds, real silence, mid-cut suspense on a withheld fact.
- **Music, comedy, celebration, success**: warm palette, quicker scenes, suspense on a withheld punchline or a turn.
- **Business, teaching, interview**: warm palette, suspense on an unanswered question; the strongest moment is often a
  contrarian claim or a number.
The four rules hold in all three; only the pacing and the palette move.

## Step 1: Transcribe
```
python scripts/transcribe.py "<path to audio or video>" "<output dir>"
```
It picks the best backend that is installed:

| Machine | Backend | Notes |
|---|---|---|
| Mac with Apple Silicon | mlx-whisper, whisper-large-v3-turbo | fastest; the Python package or the `mlx_whisper` command (also found in `~/.venvs/mlx-whisper/bin`) |
| Windows, Linux, any Mac CPU | faster-whisper, large-v3-turbo | CPU int8 by default; `--device cuda` on an NVIDIA card needs the CUDA wheels (see `premiere-ae-editing` `references/timing.md`, "Long raw footage") |
| Either, as a fallback | openai-whisper command line, base.en | slow and rough |

Condition-on-previous-text is always off, because long recordings otherwise fall into repetition loops. It writes
`.txt` (read it, search it), `.tsv` (start ms, end ms, text) and `.srt`. **Never request word timestamps on a whole
episode**: they dropped about two thirds of the speech once. After the run it prints words per 5 minutes across the
file: a healthy conversation runs about 900 to 1,100, and a sudden drop or a repeated line means a decode loop, so
re-run that region on its own.

**Better sources first (our system).**
- If the episode already sits in a Premiere project with a transcript, Premiere's own transcript is the one the editor
  will search. Export it with `premiere-ae-editing` `scripts/prproj/prtranscript.py project.prproj words.json` and check
  the search phrases against it in step 5 (`--search-in`).
- For cut points on the passages you choose (not the whole episode), `premiere-ae-editing` `scripts/media/hear.py`
  gives word timings (a names list works as hotwords on Windows; on a Mac with mlx-whisper it only primes the first
  30 s, so use its `--from` / `--to` windows), and `scripts/media/speech_cuts.py` snaps cuts to the real pauses and
  gives clean in and out points by level (`--keep`, then `--scan` to prove no edge chops a word).
- `premiere-ae-editing` `scripts/media/sapi_words.ps1` (Windows speech recognition, offline) is a last resort: too
  rough for verbatim quotes.
- Installing a backend is the user's call: say the name, the source and the size first. Model weights download on the
  first run (about 1.6 GB for large-v3-turbo).

**Escalate selectively.** When a name, a place or a foreign phrase matters and the transcript reads like nonsense,
re-transcribe that segment only (about 25 s) on a bigger multilingual model, or slowed down:
```
python scripts/transcribe.py "<audio>" "<output dir>" --start 2425 --dur 25 --model large-v3 --language auto
python scripts/transcribe.py "<audio>" "<output dir>" --start 2425 --dur 25 --slow 0.75
```
Window outputs are named `<name>_<start>s.*` and their times are already shifted to the full episode. One episode had a
name plus a foreign-language honorific that came out as gibberish on the small model and resolved cleanly on a 25 s
re-run. Names you already know can go in as hotwords on every window with `--names names.txt` (faster-whisper only):
an initial prompt alone only reaches the first 30 s window, and a names list used as a prompt once hallucinated the
names into the opening seconds.

## Step 2: Verify the proper nouns
A misspelled name in a client document about someone's family costs trust. In one episode the same person's name came
out three different ways; a web search settled it. In another, "Robbie" was actually "Rabbi". Two big models agreeing
on a name means nothing.

List every person, place and organisation you intend to name, and confirm each against a source outside the transcript
(a web search, the client's own material, the episode description) or ask the user. Correct a name everywhere at once,
only in the files you wrote: replace-all in the editor tool, or on a Mac or in Git Bash
```
perl -i -pe 's/\bNadja\b/Nadia/g' "<Show> x <Guest> - INTRO OUTLINE.md"
```
then search those files for the old spelling and expect zero hits. Never run an in-place edit over a wildcard in a
folder you did not create. If a spelling stays uncertain, pick one, use it everywhere, and flag it.

## Step 3: Read for the story
Read the `.txt` end to end first, then a timecoded view at scene size:
```
python scripts/find_passages.py "<transcript.srt>" --seconds 35
python scripts/find_passages.py "<transcript.srt>" --from 40 --to 45     # minutes 40 to 45
```
It also reads the `.tsv`, our `hear.py` JSON and Premiere's transcript JSON from `prtranscript.py`. Look for: **the
spine** (what happened, in order); **continuous passages** where one person says a whole thought in one breath; **the
reveal** the episode exists to deliver (usually what the intro must withhold); **the host's best question**, which often
carries setup the guest does not; **the main / bonus boundary** if the show has paywalled content (everything after it
is off-limits).

## The four rules
These came from the client rejecting earlier drafts.

### 1. Word for word, always
Every line attributed to a speaker is exactly what they said, the host included. A paraphrase reads as an error to a
client who knows the episode, and it sends the editor searching for a phrase that does not exist. Trim by cutting whole
sentences and mark elisions with `...`; never rewrite the words that remain.

### 2. Continuous passages, not stitched one-liners
One person, one breath, one whole thought cuts cleanly and plays as one clip. Lines pulled from four places sound
disjointed and need context they do not have. The client: "I like sections that are kind of continuous... whenever
possible, use continuous sections rather than just bits and clips from different places."

### 3. Give the hook its context
A line that lands in the episode often does not land alone. Bring enough setup with it, or use a host line that does
the same work. Watch for dangling referents (a scene that opens on "the highlight" with nothing saying of what). When
neither the passage nor a host line can carry it, a one-sentence voice-over bridge before the scene can. "This scene has
no context, it feels out of place" was the note when this failed. The scene after the hook is a claim, a number or an
unorthodox opinion, not an anecdote.

### 4. Strongest moment first, suspense in the middle, clean landing last
- **Open on the episode's single strongest moment**, even the emotional peak you would rather save, cut before its own
  payoff finishes. The card voice-over resolves that first loop.
- **Stack open loops through the middle**: a decision cut before its outcome, an attempt cut before its result, a name
  promised and not said.
- **Close cleanly**: a complete thought that lands with a beat of air before the logo, ideally gesturing at something
  the middle withheld. No smash to black before a word of an answer; document that only as an alternate.
- **Client styles win for their show.** When a client sends their own reference scripts (one did: names in the AI read
  and an abrupt question tease to black), write a client-style cut in their exact idiom AND keep a rules-compliant
  variant alongside, flagging the risk (TTS name pronunciation, with phonetic respellings) instead of silently
  overriding them. A finance show's spec trailer explicitly wanted a cliffhanger ending; follow the brief.
- **When the client writes the whole cut themselves**, the job flips to production support: verify every line verbatim
  against the tape, timecode every scene, confirm speakers on the mic tracks, correct quietly to the tape and list every
  difference, state the real runtime honestly, offer the strongest unused material as options without pushing, and
  never re-author their structure.

## Step 4: Write the outline
Framework: **Hook > Life Lesson > Emotional Rollercoaster > Always Leave Wanting More.** Target 80 to 90 seconds. Use
`references/outline-template.md` for the exact section order.

Write the cut as a **scene script**: scene blocks with a bold speaker header and a timecode range, quotes as short
stacked verbatim lines (a new line implies its own cut); voice-over segments woven between scenes as the narrative
spine (three to five, short stacked lines); sparing bracketed production directions at pivotal moments only ([MUSIC
CUTS. 1 BEAT OF SILENCE.], BLACK SCREEN); one `Search:` line per scene with two phrases. Fewer voice-overs and more of
the host is better: use the host's real questions as bridges wherever they do the same job, and keep the voice-over
bridge text in "Swaps".

**Map the whole episode**: right after the summary, "The episode map": 10 to 13 chunks for an hour, each a timecode, a
plain-English name and the host question that opens it, quoted word for word. Include pre-interview chatter.

**Write prose for a reader outside the show's world.** Some client shows serve a specific community, religious or
otherwise, and the editor reading the outline may not share that background: gloss every in-world or foreign term at
first use ("tzedakah (charity)"), introduce every person by who they are, and prefer the plain word. Quotes stay
verbatim; the glossing lives around them.

### Search phrases are the deliverable, not timecodes
Editors place cuts by searching the transcript panel in Premiere or Resolve. Give **two phrases per scene**, each
**unique** in the transcript and in **plain English** (transliterated names and foreign terms get mangled differently by
Whisper and by the NLE, the editing app's own transcript, so they will not match). Timecodes are included as a
convenience. This is the human version of our rule to write cut points as word anchors, not seconds
(`premiere-ae-editing` `references/timing.md`): times written against one transcript slip as soon as another transcript
replaces it.

## Step 5: Verify before showing anyone
```
python scripts/verify_outline.py "<outline.md>" "<transcript.txt>" --alias "Nadia=Nadja,Nadya"
python scripts/verify_outline.py "<outline.md>" "<transcript.txt>" --search-in words.json   # Premiere's own transcript
```
Pass an `--alias` for every name you corrected in step 2 (correct spelling = what Whisper heard). The report separates
**ok** (word for word), **trim** (words dropped in between: normal, mark it with `...`) and **FAIL** (words added or
reordered: a real error). It also checks that every search phrase is unique, that no em dashes crept in and that no
placeholders remain. Search phrases are checked against the un-aliased transcript on purpose, because the editor types
them into an NLE that transcribed the same audio; `--search-in` checks them against that NLE's transcript directly.
The exit code is the number of problems, so zero means safe to send.

## Step 6: Publish the page
A self-contained HTML page published with the Artifact tool: design system, section order and speaker styling in
`references/artifact-template.md`. Load the artifact-design skill first. Write the HTML to a real file in the job folder
(not only the session scratchpad, which can be wiped) and republish the same file for revisions so the client's link
never breaks; confirm before changing a published page.

## Step 7: Voice-over
One card voice-over of about 12 seconds after the hook, plus two to four short segments between scenes. **No proper
names in the read**: the on-screen card carries names; the read uses roles ("the founder of an air ambulance company").
It resolves the opening withhold, never re-states what the tape just said, and never touches the closer. Deliver it as
clean prose inside the script and again as an ElevenLabs block with **at most one or two audio tags** (see
`references/voiceover.md`). Keys for any voice service stay in environment variables the user sets; never view or
store them.

## Output to the user
Lead with the page link and the file path, then the scenes briefly, then anything assumed or unverified (spellings,
trims, assets needed from the client). Say plainly what still needs a human: photos, music clearance, the client's
approval of the outline itself. Short pointers, plain English, no em dashes.

## Our rules that also apply
- Never touch the client's original project. A string-out for Premiere goes in as FCP7 XML from `premiere-ae-editing`
  `scripts/prproj/fcpxml.py`; run `fcpxml.py --check` on it first, because one unresolvable clip makes Premiere refuse
  the whole file. Media paths must be absolute (Windows or macOS form); importing one of these XMLs into Premiere on a
  Mac is still untested, so try a small one first.
- Keep client names and private details about the people in an episode out of anything shared beyond that client.
- Keep the scripts, the outline and the page source in the job folder, never only in the session scratchpad.

## Why these rules
- **Verbatim quoting**, because the outline doubles as the editor's search index.
- **Continuous passages**, because they cut as one clip and carry their own context.
- **Unique plain-English search phrases**, because they are the only thing that survives two different transcriptions.
- **Strongest first, suspense in the middle, clean close**, because the first seconds decide the click and an abrupt
  ending reads as a trick.
- **No names in the AI read**, because a mispronounced name is the one error every listener catches.
- **Lean scenes**, because the client reads the quotes and nothing else; annotation layers were asked off.
- **Verify before delivery**, because this is often about the worst thing that ever happened to the person interviewed.
