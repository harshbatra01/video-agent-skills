# Music and SFX sourcing

Where music and sound effects come from, how to pick them and how to get them onto disk cleanly. Levels, placement,
mixing and sound-design taste live in editing-playbook; measuring, kit baking and Premiere audio mechanics in
premiere-ae-editing (references/audio.md); licences in licensing-and-rights.md section 3. Library facts were read on
the official pages in Oct 2026: re-check before relying on them.

## Contents
1. Start with the client's music and the user's own picks
2. Picking music by mood and role
3. Song hooks: "Most replayed" and the fallbacks
4. Epidemic Sound: what it offers, setup, downloads
5. Shortlisting music without spending downloads
6. SFX search words that found premium sounds
7. Screening SFX before you use them
8. Free and CC0 sound sources
9. When a clip carries someone else's song
10. Identifying the songs in a reference

## 1. Start with the client's music and the user's own picks
- **Music promotion clients** send the MP3 or WAV before release plus their TikTok, Instagram and YouTube sound links.
  Posting stays manual in the app so the client's official sound is attached to every post. (Unverified: videos posted
  through an API may go up as "original sound" and not count toward the client's sound page.)
- **Ask clients for edit-ready versions of the song:** slowed + reverb, sped up, instrumental, a no-beat-switch
  version, and a clean 20 to 30 s cut with a clear drop. Why: edits ride these versions (38% of TikTok songs in 2023
  were speed- or pitch-modified, per Pex), and labels ship them on release day.
- **Pairing a song with a subject:** check whether the subject has really used the song. An athlete walking out to a
  song coincided with it reaching Shazam #2 worldwide, and a pilot song was picked because the athlete and his club had
  used it. Why: it cannot be faked, and it moves the song.
- **The user's own picks win.** When the user replaces your music with their own tracks, respect their mix and only add;
  keep your edits on extra tracks, disabled, as swap-ins.
- **Temp music** (a bed from the user's own library) must be replaced or cleared before delivery: it was not cleared for
  that client.

## 2. Picking music by mood and role
- Music follows each piece's vibe. An explainer-style ad wanted "curious or slightly mysterious"; a "hopeful orchestral,
  90 BPM" first pick was rejected ("i just dont like this music"); the reviewer's earlier note on another cut was music that
  sounded "goofy corporate".
- One music family and one sonic logo across a series of ads.
- **Search words by story section** (research for a comeback-story ad): "solo piano / cello, reflective", then
  "pulsing strings, heartbeat, tension build", then "hybrid orchestral, triumphant, taiko and brass". Confident premium:
  "cinematic hip hop", "epic hip hop / orchestral trap", "modern orchestral pulse", "minimal luxury, driving".
  Instrumental, 95 to 120 BPM, cinematic or minimal pulse under speech.
- **Avoid** ukulele, whistling, glockenspiel and claps: the "goofy corporate" sound.
- **Beds by role for long cutdowns:** calm, tension, running (fast movement), thrill (stand-offs), riser (the biggest moments and
  the hook), picked from a handful of library tracks by mood and cycled (levels and placement: editing-playbook).
- **Search filters:** library tags (genre, mood, BPM, energy, vocals, key, duration, instruments). Rule out tracks with
  vocals for use under speech; a stem split confirms it (media-toolkit.md section 6).
- **Similar tracks:** Epidemic can search by similarity to one of its tracks or to a Spotify reference (section 4).

## 3. Song hooks: "Most replayed" and the fallbacks
- For a news reel or edit built on a song or a music video, cut on the hook or chorus, never the intro. Find it in this
  order:
  1. YouTube's "Most replayed" heatmap: take the best N-second window and skip the first 8 s. It comes in the metadata
     JSON (`yt-dlp -J --skip-download`, about 45 s a video, nothing downloaded).
  2. If the upload is too new to have a heatmap, find the hook line in a Whisper transcript.
  3. Otherwise the loudest RMS window, skipping the first 10 s and the last 6 s.
  - Why: the hook is what people know and stay for. The reviewer, on a cut that used a video's intro: "the main part of the
    song should go here". The re-cut used the first chorus, then the user picked a later window with "better visuals"
    and the hook line four times.
- **Music edits:** start the window one beat before the drop, include the song's own most-replayed stretch, and end on
  a section's last downbeat plus one bar (the cut rules: editing-playbook).
- **Long videos:** the same heatmap gives hook candidates for cutdowns (editing-playbook).

## 4. Epidemic Sound: what it offers, setup, downloads
**What it offers (official pages, Oct 2026):**
- An official MCP server (beta), listed in Claude's connector directory since 31 Aug 2026. Claude Desktop and Cursor sign
  in by OAuth; Claude Code needs an API key that only the account holder can create (valid for 1 year).
- Tools: `SearchRecordings` (BPM, mood, duration, instruments, key, vocals), `SearchSoundEffects`,
  `SearchSimilarToRecording` and `SearchSimilarToSoundEffect`, `SearchExternalReferences` (tracks like a Spotify
  reference), `EditRecording` + `PollEditRecordingJob` + `DownloadRecordingEdit` (recut a track to a length up to 5 min;
  a forced duration time-stretches, so we make our own bar-grid edits), `DownloadRecording` (full mix or stems),
  `DownloadSoundEffect` (WAV or MP3, through a signed link), and voiceover tools.
- Searching is free; downloads need a paid plan; the MCP is "not a new license" (your plan decides what you may use:
  licensing-and-rights.md section 3).
- Every search result carries a public low-quality preview MP3 and a waveform JSON: use them to shortlist (section 5).
- Also: a Premiere plugin (Window > Extensions > Epidemic Sound: Studio drafts music and SFX for a section, an
  Assistant, track versions and loops, stems), a Windows and Mac desktop app, 4 stems on most tracks, Adapt (stems and
  length presets, to fit 15 s or 30 s) and Studio (exports FCP7 XML for Premiere), both of which cost plan credits;
  250,000+ SFX in 700+ categories; no downloadable packs.

**Setup for Claude Code (the user does the account steps):**
1. The account holder creates the API key and sets it themselves as a user environment variable
   (`EPIDEMIC_SOUND_API_KEY`). Claude never views, prints or stores it.
2. Register the connector so the config holds only the variable's NAME:
   `claude mcp add -s user --transport http epidemic-sound https://www.epidemicsound.com/a/mcp-service/mcp --header 'Authorization: Bearer ${EPIDEMIC_SOUND_API_KEY}'`
3. Check that the variable exists without reading its value (print only "set" or "not set").
4. Fully quit the app (from the tray) and reopen it; confirm with a test search.
- On the Windows PC the desktop app did not put `claude` on PATH ("claude is not recognized"); its bundled CLI inside the
  app's data folder did the registration. On a Mac, Claude Desktop's OAuth route through the connector directory avoids
  the key entirely (untested on the Mac).
- The reviewer needs their own account, plan and key.

**Downloads:**
- Signed download links expire in about 1 hour. Write each batch (about 14 sounds) to a small script and download at
  once. Name files `ROLE_Name_<8-char id>.wav` so a kit builder can find them by role. Those scripts hold signed links:
  never ship them, never paste the links into reports.
- One sound pass: 49 SFX downloads became a 36-file house kit; 18 music WAVs; 28 music candidates scanned for 7 ads.
- After download, bake a house kit (resample, trim, normalise, store each file's peak offset and loudness) instead of
  placing raw library files: premiere-ae-editing references/audio.md. Placement and levels: editing-playbook.
- Stems: muting the melody stem of a track under a voice is a research default (tentative, untested).

## 5. Shortlisting music without spending downloads
- Fetch each candidate's public preview MP3, decode it, and print one structure line:
  - per-bar loudness as digits 0 to 9 (3 dB steps from 30 dB under the loudest bar);
  - the voice-band share, 300 to 3000 Hz (the masking risk under a voice);
  - the share under 150 Hz;
  - a key guess (Krumhansl profiles);
  - the last strong hit, and the ending level.
- Download full WAVs only for the 2 to 3 picks per piece. One pass covered 28 candidates for 7 ads; a voice-band share of
  0.19 against 0.54 decided between two tracks for the same ad.
- Beat grids, bar-grid edits and endings from the downloaded file: premiere-ae-editing references/audio.md.

## 6. SFX search words that found premium sounds
On Epidemic, these found sounds the user called "perfect" for premium caption and graphics work:
- "designed glitch impact", "motion graphics hit"
- UI "select / confirm / tech button", "glass ping"
- "relay ramp" and "tick pitch up" (counters), "locked in" (a lock), "bubble single" (a "?" pop), "slot crank" (a roll)
- "light switch / lever" (a spotlight), "marker pen draw line" (a highlighter), "big cheer" (a crowd)
- Plain "pop" gave cartoon sounds and plain "impact" gave fight and metal slams ("wrong for premium captions").
- Search the user's own licensed SFX library first, by file name (a well-named library is searchable like a database).

## 7. Screening SFX before you use them
- **Phones:** most thuds, booms and glitch subs had 89 to 99% of their energy under 150 Hz, which phone speakers cannot
  play. Measure the share under 150 Hz before you rely on a sound (layering them: premiere-ae-editing audio.md).
- **Resampling:** a 96 kHz "rhythmic clicks" file had 97% of its energy above 6 kHz, mostly above 24 kHz, and came out
  nearly silent at 48 kHz. Check every sound after conversion.
- **One event per file;** look at a spectrogram sheet and reject two events in one clip, steady noise, clicks inside a
  whoosh, and clean sine lines on a sound that should be physical.
- **"Real" library packs can be fake:** typing packs that reuse 3 to 15 samples sound fake; a real keyboard recording
  passed after four library sets were rejected.
- **Taste depends on the client** (editing-playbook): our caption pops and ticks were "perfect" on ads; another reviewer
  banned synthesized hits ("no more cheap beeps"); native social pages reject SFX-pack sound altogether (fake-sounding
  packs were one of four reasons a batch failed): there, use the moment's own audio.

## 8. Free and CC0 sound sources
- **Kenney:** 6 packs, 470 files, CC0.
- **Freesound:** filter to CC0 (or CC BY with a credit) and re-check the licence on each sound's own page. Originals need
  a login (ask for a free one); without it, scripts can only get the HQ preview MP3s.
- **Sonniss GDC bundles** (large, royalty-free), **Pixabay** and **Mixkit** SFX (ads allowed, no credit needed).
- **Zapsplat's** free tier requires a credit on screen; **BBC Sound Effects** are licensed non-commercial only: avoid
  them for client work.
- **A measured house set:** 46 WAVs, 48 kHz 16-bit mono, leading silence trimmed, peaks at -3 dBFS, the hit point stored
  per file (`hit_offset_s`: the attack for hits, the loudest point for whooshes and risers, 0 for beds).
- **Procedural SFX** made by script (whoosh up, down and short, impact, riser, glitch) carry no licence question; music
  edits used them. Native pages and some reviewers reject synthetic sound (section 7).
- **Premiere's own generators** (research, Sep 2026; untested by us): Premiere 26.5 can generate sound effects that fit
  a selected range and take a hummed or clapped timing guide; Generate Music and Soundscape were in beta. Their use terms
  are Adobe's: check them before client work.
- **Gambling-adjacent clients:** no casino or slot packs, no "gamblecore" audio ("Let's go gambling" says the banned
  word).
- Keep each licence text inside the kit folder (it comes down with the files), and list every sound and track in a
  CREDITS.md at delivery (research-reports-and-folders.md section 5).

## 9. When a clip carries someone else's song
- Build a scene bed from CC0 house sounds instead of keeping the song. Examples: a heartbeat and a ticking clock under a
  price countdown, then a hit and a ding on the result; a stadium bed with a crowd roar on a goal; a crowd bed and
  photographers' shutters after a match; a match playing on a TV in the room for a lifestyle clip. Why: the song is not
  ours to use, and silence is weak. (Levels: editing-playbook.)
- Better still, keep the moment's own audio when it is real (crowd, commentary, our own filming).

## 10. Identifying the songs in a reference
- Split the voice from the music (Demucs), then run Shazam on 10 to 12 s windows of the music stem; the match offset
  shows where the editor started in the song. Mechanics: media-toolkit.md section 6.
- Shazam is an outside service: the snippets leave the machine, so ask before sending a client's audio.
