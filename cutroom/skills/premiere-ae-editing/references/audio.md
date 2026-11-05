# Sound: loudness, mastering, the SFX kit, cues, beds and music edits (mechanics)

What to use where and what reviewers liked or sent back: editing-playbook `references/sound-taste.md`. Finding music
and SFX and their licences: research-and-sourcing (`references/music-and-sfx-sourcing.md`,
`references/licensing-and-rights.md`). Claude cannot hear: say so up front, do the timing, levels, variety and loudness
by numbers, and let the user's ears judge taste in short listening passes (sound-taste section 1).

## Contents
1. Measure, don't guess
2. Targets that worked
3. Voice: intake and mastering
4. Mastering a finished mix
5. Premiere: level maths, crossfades, its own audio tools
6. The SFX kit (bake once)
7. Placing SFX
8. Music beds
9. Music edits on the bar grid
10. Mix offline before touching Premiere
11. Research numbers (not all tested)
12. Licensing and the Epidemic connector
13. Speech to text and cut points

## 1. Measure, don't guess
- `python scripts/media/atools.py FILE [t0 t1]` = integrated LUFS (BS.1770-4, checked against the EBU -23 reference:
  it read -22.99), true peak dBTP, loudest 3 s window. Works on WAV, mp4, mov (PyAV decode). Mono files are measured as
  dual mono (how they sit in a stereo mix: about 3 dB above a mono-only meter).
- Library: `from atools import load_any, lufs, true_peak_db, short_term, peak_time`.
- Cross-check with ffmpeg: `ffmpeg -i FILE -af ebur128=peak=true -f null -` (Summary block); atools matched it to
  0.01 LU on a test file (Mac, 11 Oct 2026).
- Never measure peaks on an `ffmpeg -ac 1` fold-down: it sums correlated channels about 3 dB hot and under-reads wide
  sounds. Measure each channel.
- Measure the true peak of every preview and render, not only the final: one preview hit 0.0 dBTP at its hero booms.
- AE preview renders (`ae_assemble.py`) keep levels exactly: a test file went in at -33.98 and came out at -33.99 LUFS.
- Why the tools decode with PyAV: Python audio without ffmpeg on Windows is fragile (Oct 2026): librosa 1.0 cannot
  load MP4/AAC, pyloudnorm errors on clips under 400 ms, pyebur128 wheels stop at Python 3.12, madmom and essentia are
  best avoided; PyAV bundles FFmpeg.
- Keep music as WAV copies (decode each MP3 once): MP3 decoders differ in start delay and padding, so Premiere and an
  offline reference mix only line up exactly when both read the same WAV.

## 2. Targets that worked

| What | Target |
|---|---|
| Delivery (YouTube, social, paid social) | about -14 LUFS integrated, true peak at or under -1 dBTP, 48 kHz. Meta and TikTok publish no upload target: -14 to -16 LUFS is safe |
| Premiere exports without normalisation | landed at -13 to -15 LUFS with peaks about +0.1 dBTP: normalise (section 4) |
| Voice in the mix | staged to about -17.5 LUFS by clip gain, or VO files mastered to -16 LUFS (section 3) |
| Music under speech | 12-18 dB under (about 14 LU under the voice), up in gaps, +8 dB on end screens |
| Caption pops and accents | about -10 LU under the voice (the user turned -7 LU pops down 3-4 dB) |
| Explainer hero hits under a -16 LUFS voice | booms -16 to -18 dB, impacts -14 to -16 dB (louder grade-reveal booms hit 0.0 dBTP) |
| Other explainer cues (one 10-minute video) | pops -14 to -20 dB, whooshes -16 to -21, marker squeak -14 to -16, ticks -15 to -22, clock ticking -22, temp bed -24 under the voice and -15 on the end screen |
| Beds in cutdowns of long footage | by role, section 8 |
| SFX in music edits | 11-25 dB under the song, section 7 |
| Edits where the client's song is the audio (music-page formats) | song peaks about -3 dBFS, the last 1 s faded (social-video-formats) |

## 3. Voice: intake and mastering
- Intake per voice file: a 16 kHz mono copy (for recognition) and a 48 kHz mono copy (for the edit), a silence map
  (pauses over 0.45 s), lead and tail silence, LUFS and peak. Raw client voice arrived at -34 to -41 LUFS.
- Mastering chain for raw voice, written to copies with timing unchanged: zero-phase FFT high-pass at 80 Hz; pre-gain
  to -26 LUFS so the compressor threshold means the same on every file; compressor 3:1 above -24 dB, 6 dB soft knee,
  attack 8 ms, release 160 ms on a 1 ms RMS envelope; normalise to -16 LUFS; limiter at -2 dBFS with 1 ms look-ahead
  and 60 ms release. Result: preview mixes at -13.4 to -13.7 LUFS. Why the pre-gain: the files arrived spread over 7 LU,
  and one compressor setting only works when every file hits it at the same level.
- Check over-0 dBFS peaks after any clip gain: a +gain that clips needs less gain.
- Cleaned-voice exports whose names carry a music share (Adobe Podcast names like `-music-10p`) may keep some of the
  original music: ask before laying a new bed under them (tentative, never confirmed).

## 4. Mastering a finished mix
- Long cuts rendered with ffmpeg (held -14 LUFS on about 40 renders): two-pass `loudnorm` on the FULL mix (I -14, TP -1,
  LRA 20, `linear=true`), then `alimiter` (limit 0.70, attack 3 ms, release 60 ms, `level=false`), AAC 256k with
  `-aac_pns 0`. A true-peak fix pass re-limits at 0.70, then 0.63, then 0.56, only while the true peak is still over
  -1 dBTP. Results -13.9 to -14.9 LUFS, true peak -1.3 to -2.8 dBTP. Interview-heavy mixes measure about -18.7 LUFS raw,
  so expect big gains there; one short at -15.1 LUFS was accepted.
  Why each part: louder beds pushed true peak to -0.24 dBTP; an AAC noise-substitution burst made a +3 dB spike (next
  bullet); a 192 kHz oversampled limiter made it worse (+1.2 dBTP, the resampler rings), so limit at the delivery rate.
- ffmpeg's native AAC encoder: turn noise substitution off (`-aac_pns 0`). On 12 Oct it made a 4 ms burst that read as a
  +3 dB true-peak spike, and it decoded differently depending on where playback started (random noise in the decoder).
  Find such spikes by oversampling the whole decoded file and listing the loudest 0.1 s windows; one outlier far above
  the rest is an encoder artefact, not the mix.
- Short posts (15-30 s) built by ffmpeg: `afade=t=out:st=<dur-1>:d=1,loudnorm=I=-14:TP=-1.5:LRA=11,aresample=48000`,
  AAC 192k; one pass is enough at that length. A song bed under a clip's own sound sat at -14 dB.
- From Premiere: tick Loudness Normalization in the export settings (-14 LUFS / -1 dBTP), or export with
  `assets/presets/H264 match source, -14 LUFS.epr` (a test measured -14.2 LUFS, -1.0 dBTP; premiere-ui.md "Export").
  The same export option can write a Loudness Report XML that a script can read (research, Sep 2026, not tried).

## 5. Premiere: level maths, crossfades, its own audio tools
- Volume Level param = 10^((dB - 15) / 20); Audio Gain (`<Gain>`) and FCP XML levels = 10^(dB / 20)
  (prproj-format.md section 11).
- Never bake a boost into a WAV that then clips (a +8 dB bed hit peak 1.0): keyframe the Level in Premiere instead.
- Crossfade every audio edit: 4 frames, equal power (Premiere's Constant Power), centred on the cut, with handles from
  both sides. The user: "apply 4 frame cross fade between ALL the audio clips to prevent peaking". The FCP7 XMLs this
  skill writes carry levels but no fades or crossfades: say so, or bake them in the render.
- Premiere floors audio in/out points to whole video frames (seen on the Mac, Premiere 25 and 26): pad short SFX to
  whole frames + 2 ms (ffmpeg `apad=whole_len`) before importing, or the last partial frame (often the loudest pip) is
  lost.
- Premiere 26.5's own audio tools (research, Sep 2026, not tried here): Generate Sound Effects is released (it fits
  the selected range and takes a hummed or clapped timing guide); Generate Music / Soundscape is in beta; Dynamic Auto
  Ducking is announced. Essential Sound tags, Auto Ducking (it writes to an Amplify effect, not to Volume, so a script
  reading Volume misses it), Remix (within about 5 s, shortens only, not for vocals) and the loudness tools are UI only.

## 6. The SFX kit (bake once, then placement is arithmetic)
- Bake a house kit from library downloads instead of placing raw files: read the WAV (16/24/32-bit integer or float),
  resample to 48 kHz (FFT with a taper), trim from 10 ms before the onset (10% of the envelope) to the -50 dB tail
  + 30 ms, 2 ms fade-in, cosine fade-out, normalise to -1 dBFS, write 24-bit. Store per file: `peak_t` (first point at
  90% of a 3 ms envelope), the onset, the duration, `m_max` (maximum momentary loudness), the "phone" loudness (after a
  250 Hz high-pass) and the share of energy under 150 Hz. Why: once the peak time and loudness of every file are known,
  where to put a sound and how loud is arithmetic (section 7); that pass was called "perfect".
- Roles that covered caption-heavy ads: POP1-5 (+ pitched-up copies), TICK1-3, GLASS1-3, a "?" pop, LOCK1-2, LIGHT,
  FLIP, BOOM1-2, SWISH1-3, WHOOSH1-3, SHIM (shimmer), HUD, COUNT ramps, MARK1-2 (marker), CROWD. Name downloads
  `ROLE_Name_<8-char id>.wav` so the builder finds them by role.
- A CC0 house set (Kenney packs, Freesound filtered to CC0 with each page's licence re-checked) for jobs where library
  licences are unclear: 48 kHz 16-bit mono, leading silence trimmed, peaks at -3 dBFS, the hit point stored per file
  as `hit_offset_s` (the attack for hits, the loudest point for whooshes and risers, 0 for beds).
- Phones: most thuds, booms and glitch subs had 89-99% of their energy under 150 Hz, which phone speakers cannot play.
  Make each caption pop from a bright top layer (whoosh-maximise, laser, synth hit, glitch noise, tech button) plus a
  tanh-driven low layer (drive 2-2.5, -3 to -7 dB) aligned on their peaks; use pure booms only as extra weight on hero
  moments. Research adds: a 100-250 Hz thump under a boom, 700 Hz-1.5 kHz harmonics on thumps.
- Check every file after resampling: a 96 kHz "rhythmic clicks" file had 97% of its energy above 6 kHz, mostly above
  24 kHz, and came out nearly silent at 48 kHz.
- Pitched SFX in the music's key: take the dominant frequency between 250 and 5000 Hz in the 0.25 s after the peak, move
  it to the nearest triad note within 2.5 semitones (else the nearest scale note within 6) by resampling. Rising stacked
  words +0, +2, +4 semitones. Retune when the music changes: one kit stayed tuned to G major after every track was
  swapped.
- Signed library download links expire in about an hour: write each batch (about 14 sounds) to a small script and
  download at once. Never ship those scripts or paste the links: they hold signature tokens.
- Procedural SFX for music edits (whoosh up / down / short, impact, riser, glitch; 48 kHz stereo) can be generated by
  script (`python sfx.py OUT_DIR` in `library/pipelines/edits-kit/tools/`); use one family per edit.
- Use the user's own licensed SFX library first and search it by file name (one editor's library was a single folder of
  about 3,750 files in 22 categories, named by content, which made it searchable).

## 7. Placing SFX
- Cue sheet row: the time the main peak must land, the kit sound, the level in LU relative to the dialogue, what it
  marks. Clip gain = dialogue integrated LUFS + relative level - the sound's `m_max`. Clip start = target time -
  `peak_t` + 10 ms. The +10 ms bias is on purpose: a peak on the frame or up to 1 frame late reads as in sync, an early
  one never does (early sound is noticed at about 45 ms, late at about 125 ms, ITU-R BT.1359). Build-ups (risers,
  reverse swells) may start early; hits never. `atools.peak_time` gives the peak offset of a file outside the kit.
- Levels that passed on a pilot (LU against the voice): main-word pops -6 to -10, ticks -15 / -16, card swish -12,
  glass -15 / -16, counts -17, locks -11, hero booms -10 / -14, transition whoosh -9 to -13, title shimmer -14, crowd
  -19; after a check against the voice's local peaks +2 dB on pops, ticks and glass, +4 on counts, +1 on swish, lock and
  whoosh. The user then lowered the pops 3-4 dB (to about -10 LU).
- Cues generated from the same specs that built the graphics (after-effects.md section 1): pops rotate POP1-5 on main
  words, never the same twice in a row; a tick on a kicker only if its main word lands 0.35 s or more later and no
  strike is between; a strike-through = swish; question card swish +0.10 s then glass +0.25 s; headline card swish
  +0.10 s and a marker stroke centred on each highlight; white-flash whoosh +0.11 s; title shimmer +0.15 s; code card
  swish +0.08 s then lock +0.30 s (the same "brand sting" in every ad); star rating: swish as the outlines draw
  (+0.07 s), glass + shimmer as the lit star lands (+0.46 / +0.50 s), alternating ticks every 0.08 s for the failing
  stars; a stacked list of words = the same pop at +0 / +2 / +4 semitones; drop any tick within 0.15 s of another
  accent. Only level notes came back on the roll-out to 7 ads.
- Videos rendered from HTML templates: let the template's own timeline emit the cue sheet (time, name, gain), mix the
  recorded files aligned on their hit points (a synth fallback for missing ones), and mux with a 0.15 s fade-in and a
  0.8 s fade-out. Picture and sound cannot drift apart that way. (On native social pages, pack SFX read as a template:
  sound-taste.)
- Counters: take the LAST N seconds of an accelerating click ramp so its climax lands on the final number (a count up
  to 0.6 s long gets 0.5 s of ramp, up to 0.95 s gets 0.9 s, longer 1.0 s); start at the quietest point between ticks
  (40 ms search), 12 ms fade-in, 40 ms fade-out; place it by FILE START at the count start; a lock hit on the landing
  (-9 to -11 LU); a low boom (-14 LU) only on hero numbers.
- Lanes: up to 3 SFX lanes plus a separate bed lane (new tracks A3+). A sound takes the first lane that is free 10 ms
  after that lane's last clip; if none is, trim the lane whose last sound peaked at least 0.12 s before the new start
  (end it 5 ms before); otherwise drop the new sound and report it. Why: the first strict guard silently dropped hits,
  a key record landing among them.
- Transition pairs in cutdowns (whoosh + camera shutter): hook to story: a whoosh starting 1.3 s before the cut and a
  camera shutter (its 0.5-0.8 s section) on the cut, both at -4 dB; into the end plug the same pair with the shutter
  0.1 s early; scene flashes and an insert's in and out: the same pair at -10 dB, shutter 0.05 s early; a whoosh that
  would start before 0 s plays only its tail. Why the quieter copies: extra flashes must not feel like a new chapter.
- Music edits (the song is the product): one SFX family per edit, 11-25 dB under the song: a rising whoosh 0.36 s
  before the drop at -15 dB and an impact 5 ms before it at -13; a short whoosh 0.15 s before each optical transition
  and 0.2 s before flash panels at -20; a glitch 0.03 s before strobe recipes at -25; an impact 5 ms before each number
  slam at -21; a riser 1.2 s before the key strike at -21; an impact on the payoff at -11. No audio notes came back.
- Built silence in music edits (research, untested): music -5 dB with the treble cut for 4 or 8 beats before a big hit;
  audio off for 2 frames at a beat switch; on fight endings the music out a beat early over room tone.
- Review-round changes as a patch layer: keep each block's original cue list and apply one global list of DROP (time
  +-0.03 s + a name fragment), MOVE (a new time, optionally a new level) and ADD, plus a window where every old cue
  goes (a rebuilt section). Why: every change stays traceable and reversible (54 stale cues removed in one round, 479
  SFX in the cut).
- Resolve every cue by sound name through a cached index of the SFX folders (first match by base name) and FAIL before
  rendering when a name does not resolve.
- What to place and how often (sound arrivals not exits, accent density, hero hits, variants, the per-event map) is
  taste and lives in one place: editing-playbook `sound-taste.md` section 5. This section only makes it buildable.
- Deliver sound with a short listening note: what plays where and at what level, then about five timecodes to check
  first with what should happen at each ("0:04.3: a reverse swish builds into the slam"), plus any intended quirks.
  Never call the sound good; report what the checks show and let the user's ear decide.

## 8. Music beds
- Beds by role in cutdowns of long footage (the bed's own integrated level): calm -35, tension -33, running (fast
  movement) -31, action -28, hook -27 LUFS. Gain = target - the track's own loudness (measure each library track once:
  a riser read -7.6 LUFS, tension tracks -12 to -15). Why: beds at -38 to -40 (calm) and -33 (action) were "toooooo
  low raise it just a bit", so everything went up 5 dB, with no complaint since. Which bed fits which beat: sound-taste.
- Placement: one bed per scene, 6-10 segments per long cut, switched on story beats. Offset each reuse into the track
  (0, 20, 30, 40, 60, 100, 120 s) so a loop never restarts at the same spot. Fades: in 1.0-1.5 s (0.2-0.6 s going into
  action), out 1-2 s; the hook's bed fades in over 0.2 s and out over 0.4 s.
- Pause beds under a mid-video insert and resume where they stopped (out over 0.25 s, back in over 0.6 s). Test
  "inside the insert" with a 1 ms tolerance: a bed that started 0.4 ms after the insert's first frame slipped past an
  exact test and played under it. Render and XML from one shared layout, so checking the XML also checks the render.
  Dry-check the layout before rendering: a bed cue inside a removed stretch made renders fail silently.
- Before a key loud moment or reveal, take the music out (1 s of silence before one worked). Research default
  (untested): out 0.5-2 s before, back 1-3 s after with a 3-6 s fade.
- Crowd bed under archive race footage: merge archive runs less than 0.05 s apart, skip lifestyle and training montage
  clips, lay a 12 s cheer section (0.25 s fade-in, 0.8 s fade-out) at about -19 LU that ends with the run.
- Scene beds from CC0 house sounds when a borrowed clip carries someone else's song (levels used): a heartbeat at
  -10 dB, a tick every 1 s at -6 dB up to the close, a hit at -4 dB plus a ding at -8 dB on the result; a stadium bed at
  -12 dB with a crowd roar at -2 dB on the goal; a post-match crowd bed at -18 dB with photographers' shutters at -6 /
  -9 dB; a match on a TV in the room at -16 dB; then the whole mix normalised to about -14 LUFS.
- Temp bed for a long video from a short track: restart the track at each chapter boundary (a fresh start reads as
  intentional); extend long sections with a loop found by HARMONY: chroma frames (4096-point FFT, hop 2048, 60-4000 Hz
  folded to 12 pitch classes), a 4 s matching window weighted by loudness, loops at least 30 s long; align the seam on
  the waveform (best correlation within +-60 ms over 1.5 s), 0.6 s equal-power crossfade, 0.25 s fade-in and a 2 s tail
  fade per section. Why: a plain waveform loop scored 0.45 and sounded wrong; the chroma loop scored 0.95.
- Before any preview render, assert the music covers the whole cut: two previews went silent after 2:14 because the
  temp track was 133.8 s long, and nobody noticed until the full cut.
- Beds for long videos in Premiere: loop at bar boundaries to the exact length as back-to-back clips, each inside its
  file (prproj-recipes R15), then fades and the end-screen lift (+8 dB) by Level keyframes.

## 9. Music edits on the bar grid
- Beat grid from the library's BPM: refine +-0.3 BPM in 0.02 steps and the phase in 5 ms steps by the mean spectral
  flux at the beat times; the downbeat = the beat of 4 whose 4-beat stride has the most flux; RMS per bar; the final
  chord = the first downbeat after the last bar within 6 dB of the loudest bar. (Edits cut to drum hits use `beats.py`
  kicks and snares instead: timing.md.)
- Fit a track to a piece's length with at most one cut. A: no cut, start inside the track so the final chord lands on
  the target (a bonus when that is the track's real start). B: intro + one downbeat cut, cost = 1.6 x chroma distance
  (bar m against bar j, plus half for the bars before) + 0.025 x the loudness jump in dB + 0.12 if the tail is not a
  multiple of 4 bars + 0.08 if the cut bar is off a 4-bar boundary + 0.2 x |chord time - target|, minus 0.15 x weight
  when the cut lands exactly on a visual moment (a B-roll cut, a title, the code card). Force a cut at a story turn
  ("three months later") and put a boom + whoosh there. 30 ms equal-power crossfade, 0.35 s fade-in on late starts,
  0.5 s fade-out; the chord just before the code card or the last line.
- Bake the level shape into each edit: base gain to 14 LU under the voice (-17.5 LUFS voice); a slow leveller (3 s
  short-term loudness, clamped -5 / +2 LU, 31-point smoothing); +3 dB in speech gaps of 0.40 s or more (gap threshold =
  the voice's 95th percentile - 25 dB); peak cap 0.89. All 17 edits landed 11.5-14.8 LU under the voice.
- An appended CTA on the user's own track: extend their last music clip to the first downbeat after the CTA starts
  (k = ceil(source time / bar length)), then place a baked ending (the last 2 climax bars, the final chord, a 1.2 s
  tail, a cosine fade from 0.3 s after the chord over 0.9 s, -3 dB, 10 ms fade-in) 10 ms before that downbeat, with
  their clip gain. The chord landed on the offer.
- To learn what a library recut did, map the edit back to its source: 0.5 s blocks, normalised cross-correlation on a
  2 kHz decimated copy; jumps in the offset are the cuts (full rate was too slow). Epidemic's EditRecording with a
  forced duration time-stretches: prefer your own bar-grid edit.
- Switching tracks inside a piece (research): on a downbeat, hiding the join with a 1-2 bar riser into a boom or half
  a beat of silence; with stems, add drums at the turn and the full mix at the win.
- The user often picks their own tracks: then keep their mix and only ADD (never rebalance their clip gains).
- Shortlisting candidates from preview MP3s before spending downloads: research-and-sourcing
  `music-and-sfx-sourcing.md` section 5.

## 10. Mix offline before touching Premiere
Rebuild each piece's dialogue exactly as cut (the A1 source in-points plus the existing clip gains), add SFX and music in
numpy, measure integrated LUFS and true peak, write a preview WAV, and only then build the project. One pilot: dialogue
as cut -25.7 LUFS with peaks at -10 dBTP; +8 dB clip gain gave -17.7; the full mix -17.5 LUFS / -1.4 dBTP. The same pass
found the user's own clip gains (+5 to +11 dB) on other ads, one of which clipped at +10 (-1.8 dB fixed it).

## 11. Research numbers (sources disagree; not all tested)
- Music under speech: a broadcast minimum of 4 LU, editing guides 3-10 dB, Premiere's auto-duck -18 dB, a music
  library's 12-20 dB; ordinary listeners want about 4 LU more gap than pros, older listeners more. Ours stays 12-18 dB.
- Ducking 2:1, attack 15-20 ms, release 600-700 ms, hand lifts only in gaps over 0.5 s; or Essential Sound ducking of
  15-18 dB with 500-800 ms fades.
- EQ: cut 1-4 kHz in the music under a voice (or a dynamic EQ keyed by the voice at 1.5-4 kHz); for a 40-65 audience dip
  a few dB around 2-4 kHz; low-cut SFX at 100-150 Hz.
- Phones are near mono: keep voice, hits, pops and bass centred, pan whooshes only a little, check in mono.
- Whole-frame tempos: frames per beat = 60 / BPM x fps; 25 fps: 100 BPM = 15 frames, 125 = 12; 30 fps: 100 = 18,
  120 = 15.
- Risers 1-3 s, ending on the hit or 2-6 frames early; 6-12 frames of silence before the biggest reveal.
- Explainer defaults: VO peaks -6 to -12 dBFS, SFX -10 to -20, music near -30 under the voice; mute the melody stem of
  a library track under a voice.
- A public motion-video kit's mix rules (unvetted): hits closer than 0.15 s get x0.6 gain; reject SFX with more than 50%
  of their energy under 150 Hz or 40% above 6 kHz; true peak at most -1 dBTP; change one thing per round.

## 12. Licensing and the Epidemic connector
- Epidemic Sound: the official MCP (beta) can search and download (`SearchRecordings`, `SearchSoundEffects`,
  `DownloadSoundEffect`, `EditRecording`...). The Creator plan does NOT cover client work or paid ads: that needs Pro or
  Business. The API key lives only in the environment; never view, print or store it.
- Setting the connector up in Claude Code (Windows, 3 Oct 2026; ask first, it changes Claude's own config): only the
  account holder can create the key (valid 1 year), and the USER sets it as a user environment variable (`setx`).
  If `claude` is not on PATH, the desktop app bundles its own CLI:
  `%APPDATA%\Claude\claude-code\<version>\<hash>\claude.exe`.
  Register with it: `mcp add -s user --transport http epidemic-sound https://www.epidemicsound.com/a/mcp-service/mcp
  --header 'Authorization: Bearer ${EPIDEMIC_SOUND_API_KEY}'`. Keep the SINGLE quotes: double quotes let the shell
  expand the variable and would write the key itself into the config; with single quotes the config holds only the
  variable NAME. Check the variable exists without reading it (PowerShell
  `Get-ItemProperty HKCU:\Environment -Name EPIDEMIC_SOUND_API_KEY`, print only "set" / "not set"), fully quit the app
  from the tray, reopen, and confirm with one test search. Claude Desktop and Cursor sign in by OAuth instead. Not tried
  on a Mac. The reviewer needs their own account, plan and key.
- Platform music libraries (TikTok, Instagram) are platform-only. Artlist Pro is the other route for paid ads.
- Music taken from someone else's reel or video is unlicensed, even when the reel is public: say so before it goes into
  a client edit. More: research-and-sourcing `licensing-and-rights.md`.

## 13. Speech to text and cut points
See `timing.md` (Premiere transcripts, faster-whisper on Windows, mlx-whisper on the Mac, snapping cuts to the real
audio). Splitting voice from music (Demucs) and identifying songs: `media-toolkit.md` section 6.
