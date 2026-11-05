# Sound taste: music, SFX and voice

What the soundtrack should do and what reviewers liked or sent back. Every mechanic (loudness meters, the SFX kit
builder, cue sheets, lanes, bar-grid music edits, Premiere level maths, export presets) lives in premiere-ae-editing
references/audio.md. Music and SFX sourcing and licences: research-and-sourcing.

## Contents
1. Claude cannot hear: the split
2. Verdicts on sound
3. Choosing music
4. Where music moves
5. SFX taste
6. Levels at a glance
7. Voice and voice-over
8. Rights in one paragraph

## 1. Claude cannot hear: the split
- Say it up front, then split the work around it: "Yes, I can do this properly, with one honest catch: I can't hear."
  Claude does timing, levels, variety and loudness (more exactly than by hand, since it knows every animation frame);
  the editor's ears do taste (which track, does a whoosh sound cheap) in quick listening passes with 3 to 5 options.
  Result: "ok sfx is perfect".
- Never call the sound good. Report what the checks measured, and hand over a short listening note: what plays where
  and at what level, then about five timecodes to check first with what should happen at each ("0:04.3: a reverse swish
  builds into the slam"), plus any intended quirks (a planned near-silence, a hit that sits on a word on purpose).
- At most two sound fix rounds, then deliver with the listening note and let the user's ear decide (reference method).
- When the editor replaces your music or levels with their own, keep all of it and only add; never rebalance their mix.

## 2. Verdicts on sound
- Loved: the SFX pass on the premium ads ("ok sfx is perfect"); a music build-up into a reveal in a long cut ("the music syncs
  up nicely there. its a good build up good job"); a temp bed on an explainer ("i like the temp music you had as well").
- Rejected: music that sounds "goofy corporate" (ukulele, whistling, glockenspiel, claps); the first music pick on the
  ads, hopeful orchestral at 90 BPM ("i just dont like this music"); long-cut beds at -38 to -40 LUFS ("toooooo low raise
  it just a bit", +5 dB); pops at -7 LU under the voice (the editor turned them down 3 to 4 dB); clip audio leaking into
  a music edit ("A MAJOR BUG is audio"); SFX-pack sound on native pages (whooshes, ticks and dings were one of four
  reasons a batch failed).
- Second reviewer (reference): temp effects "very repetitive and annoying"; library typing packs "cheap or fake" (a real
  laptop-keyboard recording passed after four sets were rejected); "no more cheap beeps"; too many voice tags ("dont use
  this many tags").
- The reviewer's direction for ads: music must raise the stakes (multiple tracks per section, booms), not decorate.

## 3. Choosing music
- **Follow the piece's vibe,** one family of music across a series and one sonic logo: "curious, slightly mysterious"
  for explainers and list ads; a comeback story by section: "solo piano / cello, reflective", then "pulsing strings,
  heartbeat, tension build", then "hybrid orchestral, triumphant, taiko and brass". Confident premium: "cinematic hip
  hop", "modern orchestral pulse".
- **Music direction can be delegated** ("you're a better judge so please go ahead and choose") and then replaced by the
  editor's own picks: offer a runner-up they have not heard, keep yours on extra tracks, disabled, so they can swap.
- **Shortlist by measurement before spending downloads:** a track's loudness shape per bar, how much of it sits in the
  voice band (300 to 3000 Hz is masking risk under a voice), key and ending; full files only for 2 to 3 picks (mechanics
  in audio.md).
- **Cutdowns of raw footage:** "dynamic, very low" beds from a handful of the editor's tracks, one bed per scene, switched
  on story beats: calm for openings, talk and the narrator close; a tension track for arguments and threats; a running
  track for fast movement; a thrill track for stand-offs and slow reveals; a riser for the biggest moments and the hook.
  6 to 10 segments per long cut, each reuse offset into the track (0, 20, 30, 40, 60, 100, 120 s) so loops never restart
  at the same spot. Fades in 1.0 to 1.5 s (0.2 to 0.6 s going into action), out 1 to 2 s; the hook's riser fades in 0.2 s
  and out 0.4 s.
- **Music promos (a client's song is the product):** the song is audible from frame 0; in template edits it drops in at
  the template's synced beat drop (the reference track is deleted); in a Top 5 list format the client's song is the
  honourable mention, pushed louder than the rest ("the bigger the volume jump, the bigger the laugh"); peak about -3 dB
  and a 1 s fade on those template formats. Ask clients for edit-ready versions (slowed + reverb, sped up, instrumental,
  no beat switch, a clean 20 to 30 s cut).
- **Native pages:** sound like a page owner, not a template: the moment's own audio (crowd, commentary, our filming), a
  voice, or a licensed track. 130 of 148 native references ran on "original sound". When a borrowed clip carries someone
  else's song, mute it and build a scene bed from free (CC0) house sounds (a stadium bed, a crowd roar on the goal, a
  match on a TV in the room). No casino or "gamblecore" packs near a money product.
- **News reels:** keep the clip's own audio by default, a 1 s fade-out, loudness normalised so every post sits level.
- **Long videos from a short temp track:** restart the track at each chapter boundary (a fresh start reads as
  intentional) and extend sections with a harmony-matched loop (a plain waveform loop sounded wrong). Assert the music
  covers the whole cut before any preview render: two previews went silent after 2:14 because nobody checked.
- Instrumental only under speech; mute the melody stem under the voice when stems exist (research).

## 4. Where music moves
- Music quiet under claims and long explanations, prominent in montages and end cards; up in speech gaps of about 0.4 s
  or more; reveals on bar 1 of a section.
- Switch tracks on a downbeat, hiding the join with a 1 to 2 bar riser into a boom or half a beat of silence; with stems,
  add the drums at the turn and the full mix at the win.
- Drop the music about 0.16 s before a hero hit, with a build rising at least 6 dB into it (reference-set measured QA).
- Cut the music out entirely for a turn line or a quoted guest; let it breathe 1 to 3 s before a new act and hit the new
  track on the act line (reference set).
- Leave 6 to 12 frames of silence before the biggest reveal (research). In fight music edits "the silence is what people
  replay": -5 dB with the treble cut for 4 or 8 beats before a big hit, audio off for 2 frames at a beat switch, music out
  a beat early over room tone at the end (research, untested).
- Music drops before a key loud moment in cutdowns (1 s of silence before one; research default, untested: out 0.5 to
  2 s before it, back 1 to 3 s after with a 3 to 6 s fade).
- Beds pause under a mid-video plug and resume where they stopped (fade out 0.25 s, back in over 0.6 s).
- Endings: music edits end on the section's last downbeat and the end card holds one more bar while the music plays,
  fading the last 0.6 s; an appended CTA gets the music extended to the next downbeat with a final chord on the code or
  the last line; narrated pieces may ease out with two level keys to black and silence if the client wants (second
  reviewer). YouTube end screens lift the music about 8 dB when the voice stops, by keyframes in Premiere, never baked.

## 5. SFX taste
- **Sound arrivals, not exits;** about one accent every 1 to 2 s under speech, on the main (big) caption words only, not
  every caption word; 2 to 4 hero hits per ad; at most one hero per about 4 s (reference set). Rotate 3 to 5 variants and never
  the same pop twice in a row. Pitched sounds tuned to the music's key (retune the kit when the music changes; rising
  stacked words go up +0, +2, +4 semitones). Transients land on the visual frame or 1 frame late, never early (early
  sound is noticed at about 45 ms, late at about 125 ms), so build-ups may start early, hits never: risers run 1 to 3 s
  and end on the hit or 2 to 6 frames before it.
- **A whoosh peaks on the fastest frame of its move; an impact only when the card lands** (research and the reference set's
  method of placing a move sound at the frame of peak speed).
- **Per-event map that worked on the ads** (a research guide, adopted where it fit; the pass was "perfect"): a pop on
  each main caption word; a tick on a kicker only when its main word
  lands 0.35 s or more later; a swish then a glassy ping as a glass card lands; card exits silent; a marker squeak as
  long as a highlighter swipe; ticks rising in pitch on counters, a lock hit on the landing, a low boom on hero numbers;
  a camera shutter on photo reveals; a crowd bed (not whooshes) under archive race footage; a soft "light on" clunk for
  a spotlight; a white flash = a reverse swell into an impact, only in speech gaps, at most 3 per ad; a star rating =
  a swish as the outlines draw, a glassy shimmer as the one star lights, soft alternating ticks as the others fail; the
  same brand sting on the code card in every ad; one sonic logo on every end card. From the reference set: static on
  old-TV shots, keyboard clicks under document and code shots, risers into a new act.
- **Cutdowns:** a whoosh starting 1.3 s before the hook-to-story cut plus a camera shutter on the cut, both at -4 dB; the
  same pair, quieter (-10 dB), on scene flashes and the plug's in and out, so extra flashes do not feel like a new chapter.
- **Music edits:** the song is the product, SFX only add weight to cuts: one SFX family per edit, mixed 11 to 25 dB under
  the song (a riser into the strike, an impact 5 ms before the drop, a short whoosh before each optical transition).
- **Premium means designed, not cartoon:** search words that found premium SFX were "designed glitch impact", "motion
  graphics hit", UI "select / confirm / tech button", "glass ping", "tick pitch up", "locked in", "marker pen draw
  line", "big cheer". Plain "pop" gave cartoon sounds and "impact" gave fight and metal slams.
- **Phones cannot play most impact punch:** most thuds and booms had 89 to 99% of their energy under 150 Hz. Layer a
  bright top over a driven low layer; pure booms only as extra weight on hero moments (research: give a boom a 100 to
  250 Hz thump and some 700 Hz to 1.5 kHz harmonics so it survives phone speakers; low-cut SFX at 100 to 150 Hz).
- **Native pages:** no whoosh or ding packs at all.
- **Reference real-recordings bar** (a quality bar, not a ban on our approved kit): look at every sound on a spectrogram;
  one event per file; reject steady noise, clicks inside a whoosh, clean sine lines on a supposedly physical sound.
  Sounds that passed his review: organic UI clicks, a leather bag drop as a hero thump, a small backpack drop for lands,
  short real swooshes, a reverse swish ended before its peak as a build, paper foley, fast pen strokes, single typewriter
  keys, a real CRT switch-off. Rejected: tonal typing packs, steady-noise clicks, digital camera beeps, generic drop
  impacts, bell drums. On premium finance briefs pops become soft ticks.
- Hooks: no notification-like blips in the first 3 s (TikTok TopView, the full-screen ad that opens the app, bans
  explosions, screams, phone rings and alarms there).
- Mapping drums to devices ("kick = cut, snare = flash") has no source: cutting-and-pacing.md section 8.

## 6. Levels at a glance (targets that worked; how to hit them: audio.md)
LUFS is the loudness scale platforms use (an LU is a difference of 1 on it, so "14 LU under the voice" means 14 lower);
dBTP is the true peak, the loudest point after decoding, which must stay at or under -1.

| Thing | Target |
|---|---|
| Delivery | about -14 LUFS integrated, true peak at or under -1 dBTP |
| Voice | staged to about -17.5 LUFS in the mix, or mastered to -16 LUFS |
| Music under speech | 12 to 18 dB under (about 14 LU under the voice); up in gaps; +8 dB on end screens |
| Pops and accents | about -10 LU under the voice |
| Cutdown beds by role | calm -35, tension -33, running -31, action -28, hook -27 LUFS |
| Music-edit SFX | 11 to 25 dB under the song |
| Explainer heroes | booms -16 to -18 dB, impacts -14 to -16 dB under a -16 LUFS voice (louder reveal booms clipped a preview at 0 dBTP) |
- Sources disagree on music under speech (marked research): a broadcast minimum of 4 LU, 3 to 10 dB in editing guides,
  Premiere's auto-duck at -18 dB, a music library's 12 to 20 dB; ordinary listeners want about 4 LU more gap than
  pros, older listeners more. For a 40 to 65 audience dip the music a few dB around 2 to 4 kHz under speech.
- Research defaults for explainers (not yet tested in a review): voice peaks -6 to -12 dBFS, SFX -10 to -20, music near
  -30 under the voice, ducking 15 to 18 dB with 500 to 800 ms fades.
- Reference-set measured mixes: effects 6 to 10 dB under the voice, heroes allowed to peak within 2 dB of the voice peak.
- Reference set by look: news reels 17 to 22 dB under, launch films 10 to 12 LU, mini-docs only 4 to 6 LU under
  (their music stays loud). Ours stays 12 to 18 dB unless a client asks for that look.

## 7. Voice and voice-over
- No AI voice-over in cutdown shorts ever; narrator VO on hold on long cuts ("lets get our base fixed").
- No AI voice-over on a finance interview show: on-screen type bridges instead (it read as gimmicky, reference set).
- AI voice reads carry no proper names (the card text carries them); at most one or two audio tags per read.
- Voice clones need consent first: written consent on file, the person signs off the outputs, AI content labelled; a
  client's CTA voice made with a clone needs the talent's OK before paid use (flagged).
- Phones are near mono: keep voice, hits, pops and bass centred; pan whooshes only a little; check in mono (research).
- Scripts for a voice: reel-scripts skill (read it as the narrator, one breath per sentence, numbers as said).

## 8. Rights in one paragraph
A creator plan does not cover client work or paid ads; platform music libraries are platform-only; trending sounds are
not cleared for ads; a commercial song baked into "original sound" is still unlicensed; the account type (business or
creator) decides which library a page can use; on music pages posting stays manual in the app so the client's official
sound is attached. Say it out loud when it matters (research-and-sourcing has the detail).
