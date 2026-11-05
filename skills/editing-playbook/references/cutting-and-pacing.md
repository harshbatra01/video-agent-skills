# Cutting and pacing

How much to keep, where the edges go, and how fast each format moves. The mechanics (word timings, snapping cuts to
the audio, edge checks, subtitle reading, beat detection) live in premiere-ae-editing references/timing.md; this file
is the judgement.

## Contents
1. The rule under every cut
2. How much of the source to keep
3. Dead air, edges and in-points
4. Clean voice-over (studio narration)
5. Field audio (dashcam, street, interviews with radio)
6. B-roll edges and shot length
7. Pace by format
8. Music edits: rhythm and sync
9. Lengths by format
10. Choosing the source window

## 1. The rule under every cut
- **Cut on the audio, never on transcript times, and never mid-sentence or mid-word.** Whisper word starts land 0.1 to
  1 s off; cuts on raw times looked "not cut properly and not synced". Snap every edge to the real audio and check it
  (timing.md, `speech_cuts.py`, `edge_words.py`).
- What "never mid-sentence" means in practice:
  - A cut that touches a word keeps the whole word. When the next speaker overlaps, cut exactly on the word end.
  - Finishing the line beats a clean camera switch: no camera rule may move a cut into speech.
  - A phrase repeated by the same voice within about 1 s ("wait, wait... wait!") is one sentence.
  - A subtitle ending in a comma means the sentence goes on.
  - Lines with numbers: forced alignment skips digits, so end on the subtitle edge or on the loudness.
  - A short run of digital silence inside a line (a broadcaster's censor mute, about 0.2 s at -120 dBFS) is part of the
    word, never a pause.
- **Every audio edit gets a 4-frame equal-power crossfade**, centred on the cut, with handles from both sides ("apply 4
  frame cross fade between ALL the audio clips to prevent peaking").

## 2. How much of the source to keep
| Cut | Keep | Why |
|---|---|---|
| Long cutdown of raw footage | about 70 to 78% of the source | review 6: "cut stuff shorter" after a loved round that kept 84 to 91% |
| The editor's own tight cuts | 85 to 90%, a cut every about 2.5 s, median removed gap 0.5 s | measured on 131 of his sequences |
| The editor's chunk cuts | 40 to 60% (median removed gap 3 to 10 s) | same measurement |
| A slow comedy sequence | keep every shot where the subject is visible (one kept 67%) | the quiet stretch IS the joke; cutting all dead air left 56% and no joke |
| Graphic material | leave the harm to people out (one kept 53%) | warning screens, decency; keep what happens next |
- Cut inside arcs (slow talk, repeats, logistics, repeated callouts, gear talk), never whole arcs.
- Where the editor tightens our cuts by hand (measured clip by clip on one round): long-cut hook 18.0 to 14.5 s (-19%),
  standalone hook 14.7 to 12.5 s (-15%), short A 77.6 to 70.4 s (-9%), short B 75.8 to 52.5 s (-31%, it became a
  montage), short C 67.3 to 64.7 s (-4%); the stories, the plug spot and a 5:30 closing section were left alone. So pace
  matters most in hooks and shorts; natural pauses are fine inside long-cut stories.
- Action sequences: cut repeated location and speed callouts and empty stretches; keep near-misses, the peak moments
  and the impacts.
- Talk: remove the dead air between lines when talk is all that is happening.

## 3. Dead air, edges and in-points
- **Hooks and shorts:** no pause over about 0.3 s, even inside a clip; end about 0.2 s after the last word (the
  editor's range 0.11 to 0.30 s) and start on the first word. Subtitle ends linger 0.5 to 1.1 s after the speech, so
  never use them as tight outs.
- **Long-cut stories:** relaxed padding, the editor's measured habit: out a median 0.29 s after the last word, lead-in
  0.5 s before the next.
- **In-points:** a clip whose event has no line starts about 1 s before the event; a clip with a line starts on its
  first word, never on the tail of the previous line. Cut the wait before a visual event ("cut a second or two
  before it arrives") and start on the shot where the action is visible.
- **Dead beats inside kept clips:** low motion = cut; high motion = usually action (a sudden move), keep it.
- **Echoes:** the same line heard live and again over a second source, each subtitled: keep the first copy. A later
  echo can bridge a time jump (it saved 6 s once).
- **Stateful on-screen graphics** (an item counter, a score, a running tally) stay in order across long cuts; add a
  short beat back if a cut would skip a number. Shorts may skip (open question whether that is always fine).
- **Empty frames before a line** go. **Stray shots** (under 0.5 s of another camera at a clip edge) go.
- **Research defaults for long cuts** (from sourced research, not verdicts): gaps
  between kept sentences 3 to 6 frames when tight and 9 to 12 normally at 30 fps (18+ only when the silence is the
  tension); a J-cut (the sound of the next shot starting before its picture) of 6 to 15 frames so a loud moment, shout or
  call is heard before its picture appears; compress waiting, never cause and effect (keep the reason, the
  warnings, the reveal and the final choice); check 12 frames either side of every cut. Use them where our
  own data says nothing; where they differ, the editor's measured habits above win (his long-cut stories keep more air
  than the report's 9 to 12 frames).

## 4. Clean voice-over (studio narration, AI voices, podcasts)
The friend's reviewer measured these on his own fixes of a quiet narrator recording. They are the default for clean
studio voice; section 5 is the default for noisy field audio. `speech_cuts.py` (premiere-ae-editing) applies these
absolute rules by default: `--keep` gives clean in and out points for the phrases you keep (add `--words` with the
transcript so breaths and final consonants are told apart), `--scan` runs the edge scan on a cut list and exits 1 when
it finds a chopped edge, and `--phrases` lists every phrase with its edges and restart flags (`--wav-dir` writes each
piece out so it can be transcribed on its own). `--rel` switches to the older relative rule for field audio (section 5).
Commands and options: premiere-ae-editing `references/timing.md`, "Cut edges from the audio".
- **Handles:** keep a word's soft tail down to about -70 dB absolute on the raw recording (before any clip gain); start
  1 to 2 frames before the first frame at -70 dB or louder; end about 3 frames (at most 5) after the last one. The -72
  to -80 dB room-noise band is dead air. A relative threshold (noise floor + 12 dB) was "far too low" on quiet audio.
- **The final consonant belongs to the word:** inside the last word, a bump after a short silence is the release
  ("stan-d", "secon-ds"): keep it. Only a soft bump after the words (peak under -55 dB) is a breath. Start soft "S"
  onsets where they rise from the floor.
- **Breaths:** cut them at both ends, even at -58 to -70 dB. A per-phrase transcript can turn a lone breath into words
  (Whisper heard one as "Thank you."): a piece that never rises above -55 dB is a breath whatever its transcript says.
- The -70 and -55 dB levels fit the raw takes tested (room floors -72 to -78 dB) but are tunable (`--edge`, `--loud`):
  check a few edges by ear on a new microphone or room.
- **Edge scan before every build:** no cut edge may have audio louder than -55 dB on both sides. The scan must find
  nothing. Why: a level test catches chopped words a transcript misses; our word-edge check plus this level check is
  stronger than either.
- **Dead air inside a question and its answer** goes too (a 1.7 s pause was cut). A transcript that stretches the next
  phrase's first word over 0.8 s is hiding a pause.
- **False starts and restarts:** speech-to-text merges "Gen Z won't- Gen Z won't..." into one phrase; transcribe each
  phrase on its own to catch them. A per-phrase restart check is mandatory on narrator recordings.
- **Repeated words at a join:** cut the first copy and put a 4-frame audio crossfade on the join.
- **Stray fragments** ("Dream.", "I suppose."): drop clear mumbles only. A short piece stuck to the end of a kept
  phrase with no silence between is often the rest of the last word (three such cuts were restored).
- **Notes to the editor inside the recording** ("use the HQ copy", "put a black square over" a word): do what they ask
  and cut the instruction. Abandoned reads get cut.
- **Never trim the presenter's real words to match the script.** Ad-libs stay; the edit follows what was said.
- **Masters with digital silence between edited phrases:** the RMS level (average loudness per 10 ms window) gives
  exact edges there; transcript end times ran early and clipped a word.

## 5. Field audio (dashcam, radio, crowds)
The noise floor sits far above -70 dB, so use relative pauses (`speech_cuts.py --rel`; the tool warns when the floor is
above -65 dB), subtitle-aligned words and the edge checks in timing.md ("Long raw footage"). Judgement calls:
- Burned-in subtitles and the raw speech-recogniser words both get checked at every edge; four real clipped endings in
  one batch only showed up in the raw words.
- Overlapping speakers (a narrator over dialogue) have no clean cut point: keep that stretch whole.
- Narrator lines that cross-fade: cut at the first frame of the fade, or the next line flashes for 2 frames.
- Look at both sides of every white transition: 4 of 4 real misses in one round hid there or at hook edges.

## 6. B-roll edges and shot length
- **Hard cuts only, on phrase breaks.** A dissolve exposes a moment of ungraded log footage where an adjustment-layer
  grade is cut around B-roll, and off-grid edges leave 1-frame slivers.
- **Before a slow B-roll, let the speaker talk 1 to 2 s first** ("it seems a BIIIT slow... maybe just have [her] talk
  for a sec or two and then go into the broll").
- **Filler B-roll right before another B-roll goes:** show the speaker, then start the next B-roll exactly on the
  product word.
- **When B-roll is removed to show A-roll,** extend the zoom layers and grade pieces over the new A-roll ("the zooms and
  stuff should be there when A roll comes in"), or a gap shows ungraded log footage with no zoom.
- **Overlays start with their B-roll and never spill into the next shot;** if an overlay needs more time, start the
  B-roll earlier (a meter got its B-roll moved 0.4 s earlier so it lands on "100 times").
- **Titles never spill into the next B-roll or clash with other graphics;** titles leave before the next cut.
- **A product hero shot lands and holds still before the cut** ("move then cut"): the reviewer could not focus on a
  pack still moving. Research: hold product, claim and end card 2 to 3 s.
- **Never cut away from a page the voice is still reading,** or while the speaker points at or writes on a prop.
- **No fade that leaves one frame of the talking head before a cut:** hard cut instead.
- **A shot that flashes for a few frames is an error** ("comes for 5 frames ish and goes, its jarring and an error"):
  cut it and let the next shots breathe.
- **Shot floor for ads and explainers: about 0.9 s** ("no super small clips small is fine but not super small");
  montage clips 1.0 to 1.2 s. The friend's mini-doc references use 2 to 4 frame shots, but only when a client asks for
  that look, and then with one subject and matched framing.

## 7. Pace by format
| Format | Pace | Source |
|---|---|---|
| Talking-head ad | no stretch of 4 s or more with no visual change (make a dead-stretch map first); a hard change about every 3 s; shots above 0.9 s | our reviews |
| YouTube explainer | a hard change about every 3.4 s but only about a third of frames moving; fill long voice holds with slow movement, not more text; one movement at a time | the client's sample, our test ("not this many movements together") |
| Research targets, explainers | median shot 3 to 6.5 s; 7 to 13 visual changes a minute; a layout swap every 20 to 40 s; never 60 s static | vendor samples (starting points) |
| Native social post | pick ONE: a continuous shot with one line, or 3+ hard cuts per 10 s on the beat | in-between ("1.1 cuts per 10 s with designed frames") was the worst of both |
| Cutdown short | word-tight, no pause over 0.3 s, open on action | reviews 3 and 4 |
| Friend's news-reel references | median shot 1.2 to 1.8 s, a change every 0.9 to 1.7 s, proof bursts of 3 to 5 shots at 0.3 to 0.5 s | measured references, not our default |
| Friend's designed explainers | median shot 1.5 to 2.2 s, but a caption swap every 0.6 to 0.7 s | measured references |
| Friend's mini-docs (16:9, both looks) | 87 to 141 shots a minute, median 0.24 to 0.56 s, a quarter of shots 2 to 4 frames, voice 162 to 225 wpm from frame one; rebuild target 90 to 110 a minute, median 0.4 s | measured references (per look: reference-looks.md sections 5 to 7) |
| Friend's launch films | about 1.4 s average shot, cuts follow the voice phrases, not the beat | measured references |
- **Dead-stretch map:** before adding anything to a talking-head piece, mark every stretch of 4 s or more with no B-roll,
  graphic or cut. Two ads with 12.8 s and 10.7 s stretches got the most inserts. Why: it turns "edits feel slow" into a
  list of exact places to fill.
- **Timing to the word:** the picture changes on the word it illustrates; pose swaps 2 frames before the stressed word;
  text appears on its word's first spoken frame; a word starting within about 0.2 s before a cut appears on the cut, and
  the phrase after a text beat waits for the next shot; zooms start after the word lands ("wait a bit before zooming").
  Retime a collaborator's 3D renders (time remap) so their hit lands on the word (a whip on "But inside", a laser on
  "laser", a device line-up at 2x).
- **Start a move every time the picture comes back from B-roll** so it is seen, and push into a B-roll cut and land the
  pull after it (zoom choreography that was kept).
- **One thing moves at a time;** "dynamic" means speed contrast inside one move, not more cuts or angle swings (friend's
  reviewer).
- **Transition share:** hard cuts by default in ads and narrated pieces (85 to 90% plain cuts in the studied references,
  the motion living inside the shots). Music edits are the exception (section 8).

## 8. Music edits: rhythm and sync
- **Cut on the strongest hit near each planned cut,** floored to a frame so cuts land 0 to 1 frame early (the picture
  may lead the sound, never trail it: the same rule as SFX in sound-taste.md section 5, seen from the other side); report
  sync against chance before rendering (a fixed grid got 31% of cuts on strong hits against 27% chance; the
  strongest-hit snap got 54 to 62%). Mechanics: timing.md "Music edits".
- **Sync the transition's peak to the hit,** not only the cut frame: the white frame, the streak peak or the fullest flash
  panel lands on the beat (the best references' raw cut frames synced anywhere from 7% to 83%).
- **Flashy does not mean more cuts:** premium football edits cut 0.6 to 1.3 times a second, with 40 to 75% of shots
  lasting 3/4 to 3 beats; mograph strobe edits are the exception (3.8 cuts a second, 84% of shots under 3/8 of a beat).
- **Effect density:** aim for 20 to 35% of frames in a transition or effect state, a transition on every cut, about 5
  white frames per 10 s and 25+ colour bursts per 10 s (a version at about 1% of frames in an effect state read as
  basic). Crop letterbox bars before measuring.
- **Vary density by section:** the densest stretch is the payoff zone; one top edit used only 2 flashes in 30 s and leaned
  on type.
- **Lyric moments beat drum hits when the words matter:** a cut on "hit" or a title on the sung word reads as intent (one
  edit put 13 of 24 cuts on strong drum hits and the rest on lyric words).
- **Beat arithmetic:** frames per beat = 60 / BPM x fps (150 BPM at 30 fps = 12 frames, a 16th = 3 frames); tempo
  detectors read half or double time (one song read 138, 94 and 70 BPM), so trust the kick and snare list over the BPM.
- **Hit strength is relative to the loudest hit:** after a big drop every earlier hit reads weak, so judge sync in quiet
  sections by distance to the nearest hit (normalising per section is still to build).
- "Kick = cut, snare = flash, 808 = shake" has no source: folklore, test by ear.
- Build recipes for every device: motion-design.

## 9. Lengths by format
| Format | Length | Note |
|---|---|---|
| News reel | 14 to 16 s headline videos; 23 s for a chorus with 4 hook lines; 30 s for a live clip with an arc; 36 s when the payoff needs it | brand data peaks at 30 to 60 s, so test 8 to 12 s against 20 to 30 s on skip rate |
| Faceless moment or meme | 6 to 20 s | 9 of the 12 highest ratios were under 20 s |
| Faceless story post | 25 to 60 s | a guide's "about 1 minute", finance 40 to 60 s |
| Cutdown short | follows the story (delivered 0:27 to 1:32) | "they dont HAVE to be 1 mins long" |
| Standalone segment | 5 to 6 min | delivered 5:00 to 6:29 |
| Long cutdown | 10 min or more where the story allows (tentative) | delivered 6:23 to 25:16 |
| Premium ad | 21 to 34 s (research); ours ran 21 to 51 s, 5 s more with a CTA end | |
| YouTube explainer | about 10 min plus a 15 to 20 s end screen | |
| Music edit | YouTube median 39 s (middle half 27 to 56 s); also a 13 s loop version (research) | 75 edits with 150K+ views |
| Story reel (friend) | 72 to 91 s, about 246 words at about 190 wpm | |
| Founder reel (friend) | median 77.5 s, 254 words, 204 wpm | |

## 10. Choosing the source window
- **Music-video news:** cut on the hook or chorus, never the intro ("the main part of the song should go here"). Order:
  YouTube's Most-replayed window (skip the first 8 s); if the upload is too new, the hook line in a transcript; else the
  loudest window (skip the first 10 s and the last 6 s).
- **Music edits:** start one beat before the drop, include the song's most-replayed stretch, end on a section's last
  downbeat plus one bar.
- **Cutdowns:** skip the source channel's own 0 to 8 s teaser; open on the narrator's intro cut to the stakes line.
- **Borrowed clips:** cut out other channels' end cards and burned-in intro titles; never post the same footage on two
  pages at the same time: give each page its own section of the source (one page took the chorus, the other the dance
  stretch, and a 4 s overlap was flagged). Why: duplicates read as reposts under the originality rules.
- **Check requested in and out times against the source length** before rendering ("4:50 to 6:05" on a 6:02 video was
  a typo for 5:05).
