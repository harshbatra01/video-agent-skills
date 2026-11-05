# 07 - Roto, masking and compositing in sports edits (lane: ROTOSCOPING / MASKING / COMPOSITING)

Research date: 2026-10-13. Format follows `_brief.md`. No em dashes, no emojis.

## Method and evidence key (read first)

- [F] = frames checked. I looked at YouTube's own public preview frames for the video (scrub storyboard sheets, or thumbnail frames for Shorts) and read the technique off them. No video was downloaded. Timestamps are approximate (tile spacing is about 1 s, so treat as +/- 1 s).
- [M] = metadata only (title, description, chapters, caption). Used for tutorials and a few supporting items.
- Views, likes, subs, dates: yt-dlp, pulled 2026-10-13. Songs and software: copied from each video's description; "(not listed)" means the description does not say.
- TikTok cannot be opened from this PC (connection refused), so TikTok-native hard edits are NOT evidenced here; the creators below are the YouTube-side editors who also post there. Instagram profile, reel and tag pages open through WebFetch (used only for follower counts and captions; reel frames could not be checked). Reddit: the search tool refused the domain, so no Reddit threads were read. Shared web search budget ran out, so some follow-ups (BCC "Depth Map ML", exact AE Object Matte release date) were not searched; see 09-tools-packs-sources.md for those.
- Honest level check: most high-view YouTube "4K edits" are caption/speech edits (see 05, 08) and are NOT roto-heavy. The entries below are the ones where I could see roto cutouts, text behind the subject, outlines, trails, tracked or 3D type, or scene composites. Colour-pop (subject in colour, rest B&W) is the one item in this lane for which I found NO standout sports edit; only tutorials and one B&W-to-colour promo.
- Tool note: `python -I -m yt_dlp` fails here (module lives in the user site-packages). A wrapper that prepends `C:\Users\Kanishk\AppData\Roaming\Python\Python313\site-packages` to sys.path and runs under `-I` works. Scripts: `C:\Users\Kanishk\AppData\Local\Temp\claude\C--VISION-IMMUFIX-repair-ENCODED-RUSHES\295694e7-b49e-48b6-8b23-3d95eb8b59bb\scratchpad\roto`.
- Overlap: entries 1-5, 7, 9, 10, 12, 14-16, 19, 22, 24, 27 also appear in 01-football, 03-combat-f1-other, 05-captions-typography or 08-sync-structure-virality. Here they are described only for their roto/compositing content, with frame-level timestamps (cross-refs given). Entries 6, 8, 11, 13, 17, 18, 20, 21, 23, 25, 26, 28-37 are new to the bank as far as I could tell from the other files' headings.

---

## 1. Standout edits

### 1. Speed x Ronaldo: giant 3D words behind the roto'd player
- Link: https://www.youtube.com/watch?v=hnWplUUmWLQ | YouTube (landscape, 31 s; also a Short: https://www.youtube.com/shorts/wlM5gVQm_uw, 1.0M views) | Creator: @sanchezae (417K subs; IG @sanchezamv1 155K, "400K+ on TikTok" per its bio) | Subject: Ronaldo + IShowSpeed | Song: Phonkha x TREVOLX - VELVETAL (Slowed) | 2.48M views, 92.2K likes | 2025-05-02
- Why it's elite: [F] Almost every second is a composite: a curved 3D screen title, then extruded lettering placed BEHIND the subject with a gold smoke swirl, cloud-wipe transitions and a game-world finale. Description lists After Effects 2024 and Twixtor, project file sold on Payhip. A reaction clip titled "Speed Reacts To Sanchez Edit ... Calls Its The Best Ronaldo Edit Ever Made" (Streamertainment, 57K views, 2025-05-25, https://www.youtube.com/watch?v=dhNe0KxRGIY) appeared three weeks later; the clip does not name the edit, so it is probably this one (unverified). See also 01-football #1.
- Techniques: text-behind-subject (about 4 s gold-smoke swirl with giant RONALDO lettering; about 7-8 s SCORE IT / EGO type behind Speed; about 22 s EGO behind the hug, over sky), 3d-text, roto-cutout, bg-swap, overlay-texture (smoke/cloud wipe about 20-21 s), radial-zoom-blur (rainbow burst about 12 s), outro-card ("SIMPLE AS THAT, BRO." near 29 s)
- Steal this: make the artist or song name a giant 3D object in the scene and put the roto'd athlete in front of it on the drop; reveal the lettering over 4-6 frames with a smoke or cloud wipe.

### 2. Messi x Speed: 3D book intro, gold and pink extruded names, hand-scribbled overlay
- Link: https://www.youtube.com/watch?v=GV4M-cmFtg4 | YouTube (landscape, roughly 5:4 frame, 38 s; letterboxed Short: https://www.youtube.com/shorts/Bq0TJQKdDRw, 279K) | Creator: @sanchezae | Subject: Messi + IShowSpeed | Song: MONTAGEM CONTIGO - Repsaj | 391K views, 16.2K likes | 2025-07-31
- Why it's elite: [F] Opens on a 3D "HISTORY OF FOOTBALL by sanchez" book where the footage appears through a torn-paper hole while the camera pushes in; gold FANTASTIC and PLAYER lettering sits behind Messi; a pink extruded MESSI stands in the stadium with Speed cut out in front and a white scribbled "I AM" written over it (Short frame at about 19 s). See also 01-football #2.
- Techniques: 3d-elements (book), 3d-camera, text-behind-subject (about 1 s and 8 s gold type behind Messi; about 9-19 s pink MESSI in stands), 3d-text, roto-cutout, scribble-doodle (hand-lettered I AM), overlay-texture (paper)
- Steal this: a 1-second "paper hole" or poster intro that the camera pushes through is a cheap hook-first-second that can end on the song title; add one hand-scribbled word over the 3D type for a human feel.

### 3. Erling Haaland Edit: a whole mythology scene built around the player
- Link: https://www.youtube.com/watch?v=UTwEinFQ6b4 | YouTube (landscape 43 s; letterboxed Short: https://www.youtube.com/shorts/b74FqKeuY54, 141K) | Creator: @sanchezae | Subject: Haaland (Norway, World Cup 2026) | Song: Sem Tempo (Super Slowed) | 163K views, 11.5K likes | 2026-07-21
- Why it's elite: [F] Pushes the formula from "text behind player" to full scene swaps: yellow 3D HAALAND type on pitch shots (about 2 s), big GOALS type over interview footage (about 8 s), then a Viking longship and storm-sea sequence (about 16-20 s), Haaland meditating on the centre circle and a horned-helmet close (about 38-43 s). Whether the plates are CGI, AI or stock is not stated (unverified). See also 01-football #3.
- Techniques: bg-swap, roto-cutout, 3d-text, kinetic-type, radial-zoom-blur, cc-grade, glow
- Steal this: pick one metaphor that matches the song (storm, throne, desert) and build 3-4 scene swaps around the roto'd player; the cut-out is the constant, the world changes on each drop.

### 4. THE GOAT "Cristiano Ronaldo" (Montagem Tomada): neon outline lettering and HUD rings
- Link: https://www.youtube.com/watch?v=P1Gh6u0MUzo | YouTube (landscape, 33 s) | Creator: @iluxha_aep (12.6K subs; TikTok @iluxhaep; credits @sanchezae as inspiration) | Subject: Ronaldo | Song: MXZI - Montagem Tomada | 691K views, 20.1K likes | 2025-06-18
- Why it's elite: [F] Among the densest effect-per-second edits I found on YouTube, from a 12.6K-sub channel: glowing "CR7" outline lettering behind a cut-out Ronaldo, a spinning HUD ring over Ballon d'Or trophies, a chromatic kaleidoscope burst, giant PUMA lettering behind young Ronaldo. Description: After Effects 2021, FL Studio 21, Blender (so the track was cut by the editor and a 3D element was built). See also 01-football #4.
- Techniques: outline-text, text-behind-subject (about 11-12 s neon CR7 outline; again about 21 s; about 19 s PUMA behind), roto-cutout, 3d-elements (HUD ring about 13.6 s; description lists Blender), chromatic-aberration, rgb-split, kaleidoscope (about 17 s), radial-zoom-blur, lens-flare, light-rays, glitch
- Steal this: build one glowing outline-lettering graphic (artist name) that flashes on the kick and swaps to a HUD ring on the snare; cut the audio first so every hit is where the visual wants it.

### 5. This Messi edit will SHOCK you: roto outline aura, sparks and bokeh swap
- Link: https://www.youtube.com/watch?v=BcjOvZHZVxA | YouTube (landscape, 36 s) | Creator: @HeroEdit_ae (Hero Edit, 48.5K subs) | Subject: Messi | Song: (not listed) | 629K views, 27.7K likes | 2025-03-17
- Why it's elite: [F] Effect-first, not caption-first: a cyan glowing outline aura with scanline glitch hugging full-body Messi (about 13 s), confetti sparks around the head (about 11 s), neon letter pops (IT, about 14 s), rainbow neon distort (about 18 s), yellow speed lines on pink, then a purple bokeh/particle background swap on the Inter Miami shot (about 24 s). See also 01-football #11.
- Techniques: roto-cutout, outline-stroke, glow, particles, bg-swap, glitch, rgb-split, light-leak, kinetic-type
- Steal this: extend our 1-frame glow strobe to a roto'd FULL-BODY outline that holds 3-6 frames on the beat, with scanline glitch inside the aura.

### 6. BLACK OUT, Max Verstappen: giant red serif type behind the helmet
- Link: https://www.youtube.com/watch?v=XJkfA0Wgj7g | YouTube (landscape, 31 s) | Creator: @yunsuv (2.08K subs) | Subject: Max Verstappen (F1) | Song: black out - leta | 134K views, 4.3K likes | 2025-09-30
- Why it's elite: [F] A one-idea poster system: huge red serif MAX and VERSTAPPEN across the frame with the helmeted driver cut out IN FRONT, mirrored MAXMAX bars behind a celebrating Max, white-background frames with a black cut-out silhouette. Tiny channel, so it is a reachable level. See also 03-combat-f1-other.
- Techniques: text-behind-subject (about 3-9 s MAX; about 12-14 s VERSTAPPEN; about 18-24 s MAXMAX behind the celebration), roto-cutout, kinetic-type, color-flash (white poster frames), cc-grade
- Steal this: one serif face in one colour, with the player's head cut out in front on every lyric hit; works at phone size because the word is bigger than the person.

### 7. DNA, Verstappen x Kendrick Lamar: one-colour type that slides behind the driver
- Link: https://www.youtube.com/watch?v=o4QXiKLv9yo | YouTube (landscape, 33 s) | Creator: @bela-films (Bela Films, 6.79K subs) | Subject: Max Verstappen | Song: audio credited to @shiloh002 (track name not listed) | 1.32M views, likes hidden | 2024-07-29
- Why it's elite: [F] Orange condensed words (GOT, LOYALTY, JOY, INSIDE) appear on the lyric, some hatch-lined or stripe-filled, sitting beside, over or partly behind helmets and faces, with orange smoke and halftone-like fills; the palette never changes. See also 03 #2, 08 #25.
- Techniques: text-behind-subject (partial), kinetic-type, lyric-text, halftone, overlay-texture (smoke), match-cut
- Steal this: lock one brand colour and one typeface so type can be a graphic layer (behind the subject) without turning into noise.

### 8. Messi "Way Down We Go": text and lightning locked into the stadium (older reference)
- Link: https://www.youtube.com/watch?v=jB_won9HULM | YouTube (landscape, 34 s) | Creator: @pyeftbl (41.6K subs; TikTok @pyeftbl per description) | Subject: Messi (World Cup 2022 trophy lift) | Song: "Way Down We Go" per title (audio link in description) | 1.67M views, 57.3K likes | 2023-07-04
- Why it's elite: [F] Story lines in neon lettering lie along the top of the stand like broadcast graphics (about 9-15 s, e.g. "LIONEL MESSI HAS SHAKEN HANDS WITH PARADIS", "THE LITTLE BOY FROM ROSARIO, SANTA FE"), key names recolour (green, cyan), and a cyan electric arc is traced around the trophy and Messi's head (about 18-19 s). 2023, so older than the brief's focus, kept as the clean "tracked text + lightning" reference.
- Techniques: tracked-text, 3d-camera, kinetic-type, glow, overlay-texture (lightning)
- Steal this: track words onto real surfaces in the scene (stand, grass, scoreboard) and recolour the key word instead of using a caption bar.

### 9. Blue Lock x World Cup / E.T. (Dr1zzy): month-long football-anime composite
- Link: https://www.youtube.com/watch?v=LSUL0Vp-cLY | YouTube (landscape, 134 s; chapters Intro 0:00, Edit 0:46, Interlude 1:12, Edit 1:42) | Creator: @Dr1zzy.aep. (Dr1zzy, 26.3K subs; IG dr1zzy.aep 3.2K; credits @sanchezae) | Subject: World Cup stars + Blue Lock | Song: E.T. (Hoodtrap / Mylancore) | 139K views, 7.6K likes | 2026-08-25
- Why it's elite: [F] Creator says it took a month. Big 3D EGOIST lettering, kinetic captions, a real-footage player that disintegrates into white particles (about 1:00-1:10, inside the first "Edit" chapter), glitch and flash cuts between anime and match clips. Project file sold on Payhip (his Yamal edit lists After Effects 2020; the software line for this one was not seen). See also 01-football #14.
- Techniques: 3d-text, kinetic-type, particles (dissolve), roto-cutout, glitch, white-flash, build-to-drop
- Steal this: dissolve the cut-out athlete into particles on the drop and re-form him on the next clip; a dissolve is a roto shot that reads as a transition.

### 10. Ronaldo "Back to Man Utd [RE-UNITED]": glow text tracked onto shirts and faces
- Link: https://www.youtube.com/watch?v=ixIJGmmxjIg | YouTube (landscape, 39 s) | Creator: @slicx7 (Slicx7, 4.67M subs; top Shorts 2.2M to 8.1M views) | Subject: Ronaldo | Song: Egzod and Maestro Chives - Royalty (ft. Neoni) | 554K views, 18.8K likes | 2024-10-04
- Why it's elite: [F] The reference for the "player text tracking" look (several tutorials are titled "@slicx7 like ..."): green glow names (MANCHESTER, TURIN, MADEIRA) sit above the printed name on each club shirt (about 3-5 s), perspective words lie on the pitch (about 12-14 s), glow words follow the face (EMOTIONAL, VERY EMOTIONAL, about 20-23 s), a CR7 and club-crest logo pulse with RE-UNITED (about 17-18 s), fire burst at the end. See also 05 #17.
- Techniques: tracked-text, glow, kinetic-type, overlay-texture (fire), outro-card
- Steal this: track one glowing word to the player's body or face on each lyric hit; the viewer reads it as part of the footage.

### 11. Sky Sports Premier League 2025/26 intro: club-name type behind players in a 3D tunnel
- Link: https://www.youtube.com/watch?v=BBJB6RFRX8U | YouTube (re-upload of the broadcast intro by Pick Six Productions Xtra, 51 s) | Creator: Sky Sports (uploader @PickSixProdXtra) | Subject: Premier League clubs | Song: "G.O.A.T" by Kasabian ft. Cristale | 150K views, 1.2K likes | 2025-08-16
- Why it's elite: [F] Broadcast-level: the whole piece is a perspective tunnel where giant club names and crests are mapped onto the walls and the cut-out players stand in front of them (BOURNEMOUTH, CRYSTAL, TOTTENHAM, BURNLEY style frames), blue/red palette throughout. Aspirational, not DIY.
- Techniques: text-behind-subject, roto-cutout, 3d-elements, tracked-text, cc-grade
- Steal this: for a multi-artist or multi-clip piece, use the same environment (tunnel, wall, stage) for every shot and put the name behind each person; it makes a list read as a system.

### 12. FIFA World Cup 2026 Spain cinematic promo: numerals, silhouettes and 4-up frames
- Link: https://www.youtube.com/watch?v=WgsExxMIvXE | YouTube (landscape, 62 s) | Creator: @henycreate (HENYCREATE and Makkivision, 313 subs) | Subject: World Cup 2026, Spain, Ronaldo, Messi, Yamal | Song: (not listed) | 112K views, 2.2K likes | 2026-07-22
- Why it's elite: [F] A flat-colour motion-design system: giant 2-0-2-6 numerals as the stage, flat white player silhouettes used as fills inside the numbers, cut-out CR7 standing in front of a numeral with SIUUUU lettering behind him, 4-up grids of the numeral. See also 01-football #18.
- Techniques: split-screen-grid, text-behind-subject, roto-cutout, kinetic-type, cc-grade
- Steal this: use one big graphic shape (number, logo, vinyl) as the stage and cut the player in front of it; silhouettes of the player filled with colour make a free transition frame.

### 13. Neymar edit (Austin Edits): several cut-out Neymars as a collage on black
- Link: https://www.youtube.com/watch?v=7hDl2eh7iIk | YouTube (landscape, 23 s) | Creator: @austineditz (Austin Edits, 5.62K subs) | Subject: Neymar | Song: (not listed) | 738K views, 23.7K likes | 2024-06-11
- Why it's elite: [F] Description: After Effects, 12+ hours. The first ~10 s shows 3-4 small roto'd Neymar figures (Brazil, Barcelona kits) standing on pure black with club crests and short text, like a sticker or poster sheet, before the main edit starts.
- Techniques: roto-cutout, clone, split-screen-grid (collage), kinetic-type, cc-grade
- Steal this: open on a "sheet" of 3-4 cut-outs of the same player (different eras or kits) on black as the hook, then cut to the first beat.

### 14. CapCut vs After Effects (Short): what the AE layer actually adds
- Link: https://www.youtube.com/shorts/wcAOKDeat3E | YouTube Short (15 s) | Creator: @HeroEdit_ae | Subject: Neymar (PSG) | Song: (not listed) | 3.02M views, 62.7K likes | 2024-11-16
- Why it's elite: [F] A split-screen A/B of the same Neymar clip: left is plain CapCut, right is After Effects with red liquid-splash particles wrapped around the roto'd head and hand plus scanline texture. The comparison itself is the hook (3M views). See also 01-football #9.
- Techniques: roto-cutout, particles, overlay-texture, split-screen-grid
- Steal this: show "without / with the effect layer" side by side as a 15-second proof clip for the client or as the post itself.

### 15. "That one ronaldo edit (TOOK ME +5 HOURS)": ember outline, inset cards, coloured words
- Link: https://www.youtube.com/watch?v=g2A1zX6ARqA | YouTube (landscape, 73 s) | Creator: @HeroEdit_ae | Subject: Ronaldo (Piers Morgan interview) | Song: (not listed) | 1.22M views, 70.7K likes | 2024-12-26
- Why it's elite: [F] Mostly a documentary edit, but with real compositing: red ember particles on the edge of a cut-out Ronaldo (about 15 s), rounded-corner footage cards floating on black, a CR7 logo build, and a "Over 5 hours of work" title that sells effort. Partial-lane. See also 01-football #10, 05 #13.
- Techniques: outline-stroke, particles, roto-cutout, word-by-word, kinetic-type
- Steal this: tell the viewer how long it took (a title card) and use rounded-corner insets for secondary footage so the cut-out stays the hero.

### 16. "What Subject..?" Ronaldo Boys edit (FicTic): scribbles, glow word, torn frames
- Link: https://www.youtube.com/shorts/A0AfkjiGAxk | YouTube Short (20 s) | Creator: @fictic_editz (720K YT subs; IG fictic_editz 241K) | Subject: Ronaldo | Song: Mande Mande (Slowed and Reverb) per title | 8.90M views, 248K likes | 2026-01-21
- Why it's elite: [F] A meme-structure edit (white title strip "Girls at School" then the Ronaldo answer) with a gold glow word locked to the mouth, a hand-scribbled white "F" drawn onto Ronaldo's cheek, a MADE BY FICTIC stamp, and (on the same channel's Cars edit) torn-paper frame edges. Description: After Effects. See also 01-football #7.
- Techniques: scribble-doodle, glow, word-by-word, kinetic-type, overlay-texture (paper edge)
- Steal this: a scribbled mark that draws itself on the athlete's face on a beat costs almost nothing and reads instantly on a phone.

### 17. Ronaldo ink-hatch Short (Hero Edit): engraving texture over skin and kit
- Link: https://www.youtube.com/shorts/h34HM7Roj_U | YouTube Short (12 s) | Creator: @HeroEdit_ae | Subject: Ronaldo celebration | Song: (not listed) | 192K views, 4.8K likes | 2024-10-01
- Why it's elite: [F] Title says a CapCut tutorial exists for it. The mid-frame shows a pen-and-ink hatch (engraving) texture wrapped across Ronaldo's face and shirt while the background stays soft, so a mobile app gets an "illustrated" look.
- Techniques: scribble-doodle (ink hatch), overlay-texture, cc-grade, roto-cutout
- Steal this: a 12-second Short with ONE illustrated treatment on the hero frame is enough; the CapCut tutorial named in the title shows how it was built.

### 18. "tvrood style" example (Dakyuu, Kai Havertz): outlined cut-out on a dark HUD card
- Link: https://www.youtube.com/watch?v=fbc98d2YR6c | YouTube (landscape, 18 s) | Creator: @dakyuu6045 (Dakyuu, 301 subs; tiny, chosen as a faithful copy of the style) | Subject: Kai Havertz | Song: MONTAGEM TENTA (per title) | 1.9K views | 2026-03-23
- Why it's elite: [F] Shows the 2026 "tvrood style": a roto'd player with a thick white glow outline sitting on a dark poster/HUD card with a NAME label, spec-sheet lines and diagonal white slash bars (the 3D camera move is not checkable from stills; the AnasFTBL tutorial has a "Camera animation setup" chapter). The NDK Edit CapCut tutorial for the same style has 192K views and the AnasFTBL AE tutorial 44K (section 3), so the trend is large even if this example is small. Trend originators per tutorial titles: TikTok @tvrood and @ftb.aep (profiles not reachable, unverified); 01-football #23 covers @ftb.aepp on IG, possibly the same editor (unverified).
- Techniques: roto-cutout, outline-stroke, glow, 3d-camera, kinetic-type, split-screen-grid (card layout)
- Steal this: a player card layout (name tag plus spec lines plus white outline on dark) is a ready-made frame for "artist + song title" cards.

### 19. "Depth style" example (Dmr22k, Ronaldo, "Pursuit"): the depth map as the look
- Link: https://www.youtube.com/watch?v=KOT4my-qqB8 | YouTube (landscape, 125 s) | Creator: @Shpee3r (channel display name Dmr22k, 11.1K subs) | Subject: Ronaldo | Song: Pursuit (Super Slowed) | 19.6K views, 279 likes | 2026-08-23
- Why it's elite: [F] The Aug 2026 trend in its raw form: footage alternates with a grayscale DEPTH MAP of the same shot (white = near, black = far), silhouettes in white fog, plus depth-of-field blur on the colour shots. Small example, big trend: AE tutorial by rdylt09 (193K subs, 53K views, 2026-08-20; chapters include "Face tracking and positioning" and "Color and depth effects"), HOBO Ae AE tutorial 61K views, Alight Motion tutorial 53K views, an IG reel captioned "BCC+DEPTH MAP ML ... #depthstyle" (https://www.instagram.com/reel/Dca9irkqQu9/, 15.1K likes, After Effects 2024). See also 01-football #26.
- Techniques: 3d-camera (parallax), bw, contrast-crush, NEW: depth-map-visual
- Steal this: render a depth-map pass of the key shot and use it as a beat-synced reveal; a niche track (Pursuit) rides the trend with it.

### 20. Ronaldo [Montagem PR] (FootyAnimeFlicks): lightning wrapped around the face
- Link: https://www.youtube.com/watch?v=yCRYvKTaQYY | YouTube (landscape, 67 s) | Creator: @FootyAnimeFlicks (2.06K subs) | Subject: Ronaldo | Song: (not listed) | 639K views, 4.9K likes | 2023-10-07
- Why it's elite: [F] Older, but a clear energy-overlay reference: electric blue lightning wraps Ronaldo's face and kit (about 6-8 s) on a matched grade. Low like ratio, so treat as a reach example.
- Techniques: overlay-texture (lightning), glow, cc-grade
- Steal this: 6-10 frames of lightning that follow the face contour on the drop beat is a cheap "power-up" hit.

### 21. My Best CR7 Edit (crn7.aep.): neon and glitch type placed into the pitch and net
- Link: https://www.youtube.com/watch?v=NozIEwNEI60 | YouTube (landscape, 34 s) | Creator: @crn7.aep1 (crn7.aep., 1.53K subs) | Subject: Ronaldo | Song: Cochise - Super Villain | 62.0K views, 2.5K likes | 2025-10-28
- Why it's elite: [F] After Effects 2024. Yellow glitch DEFEAT lettering sits in the goal frame, neon outline words (Que) tilt over crowd shots, a ring HUD flashes. Shows 1.5K-sub channels already do tracked 3D type.
- Techniques: tracked-text, 3d-text, outline-text, glitch-text, glow
- Steal this: put the keyword of the lyric INSIDE the goal frame or on the pitch in perspective instead of at screen centre.

### 22. Lamine Yamal "LUA NA PRACA" (Dr1zzy): echo trails and zoom blur on the dribble
- Link: https://www.youtube.com/watch?v=n6tSXxIgkw0 | YouTube (landscape, 41 s) | Creator: @Dr1zzy.aep. (26.3K subs; credits @sanchezae; audio "Edited by me") | Subject: Lamine Yamal | Song: LUA NA PRACA (Slowed) | 200K views, 8.8K likes | 2025-11-16
- Why it's elite: [F] First footballer edit by this editor (per description): ghost duplicates of the dribbler trail behind him (afterimages) and strong radial-blur whips; After Effects 2020, project file sold. See also 08 #33.
- Techniques: echo-trails, clone, radial-zoom-blur, cc-grade
- Steal this: 3-5 delayed ghost copies of the player at 20 percent opacity on the fastest move, locked to the bar (same idea as the broadcast clone trails in 34 and 35).

### 23. I AM CHARLES LECLERC (EVILJORDAN, yunsuv): serif lyric type as the image
- Link: https://www.youtube.com/watch?v=xBcsui9B20c | YouTube (landscape, 67 s) | Creator: @yunsuv | Subject: Charles Leclerc (F1) | Song: EVILJORDAN (Guitar Intro/Remix), Playboi Carti, prod. Ratno | 465K views, 21.9K likes | 2025-01-17
- Why it's elite: [F] Opens on a repeating-serif CHARLES LECLERC lockup, then big serif lyric lines (SAFE, SO HOT GOTTA HIDE MY FACE) shown at poster scale over the red/green Italian-flag palette, with drivers placed in front or beside the type. Same channel as entry 6.
- Techniques: lyric-text, kinetic-type, text-behind-subject (partial), cc-grade
- Steal this: set the sung line in one oversized serif face and let the footage sit around it; the line becomes the image.

### 24. REINCARNATED: Hamilton x Kendrick Lamar (Bela Films): lime type around the car
- Link: https://www.youtube.com/watch?v=kX0ws8ZmwAk | YouTube (landscape, 21 s) | Creator: @bela-films | Subject: Lewis Hamilton | Song: (not listed) | 435K views, 18.4K likes | 2024-07-09
- Why it's elite: [F] Acid-lime words (LIFE, ALL, KEEP, BLUEPRINT) pop around and partly behind the car or driver on the lyric, a title card (REINCARNATED), inset photo panels. Companion to entry 7. See also 03 #3.
- Techniques: kinetic-type, lyric-text, text-behind-subject (partial), cc-grade
- Steal this: one acid accent colour for all type against desaturated footage makes the word the loudest thing in frame.

### 25. "ankara messi giant" (ImaginaryFootball): a scale gag as a cut-out
- Link: https://www.youtube.com/watch?v=taeZC-XRsZI | YouTube (19 s) | Creator: @ImaginaryFootball_ch (32.7K subs) | Subject: Messi | Song: (not listed) | 10.4M views, 89.2K likes | 2023-06-16
- Why it's elite: [F] The simplest roto idea in the bank: Messi cut out and scaled giant among tiny defenders on a real match shot. 10.4M views shows a gag beats polish. 2023, so a pre-brief reference.
- Techniques: roto-cutout, NEW: scale-gag
- Steal this: scale the athlete (or the artist) to giant on the first frame as a hook; viewers stay to see why.

### 26. NBA on ESPN "Where superstars become legends": B&W past meets colour present
- Link: https://www.youtube.com/watch?v=0CDOhG8VXGM | YouTube (59 s) | Creator: NBA on ESPN (2.18M subs) | Subject: NBA playoffs 2024 | Song: (not listed) | 164K views, 6.3K likes | 2024-04-20
- Why it's elite: [F] Pairs past and present stars in the same frame (Garnett and Edwards, Kobe and LeBron style pairings) and switches between B&W and colour. Whether the pairs are composited or archive is not confirmed (unverified). The closest thing to colour-pop in a pro sports spot that I found.
- Techniques: bw, cc-grade, match-cut
- Steal this: hold the "old" shot in B&W and release it to colour on the beat; for a music promo, B&W for the verse and colour for the drop.

### 27. Blue Lock X World Cup "Champions" (Blubz): flags and 3D type over anime-football
- Link: https://www.youtube.com/watch?v=lQs5bkOESNs | YouTube (landscape, 35 s) | Creator: @Blubzz (Blubz, 143K subs) | Subject: Blue Lock characters + World Cup nations | Song: IShowSpeed - World Cup (Champions) (edited by the creator) | 129K views, 5.2K likes | 2026-07-25
- Why it's elite: [F] Part of the July-Aug 2026 football-anime crossover wave (with entry 9): national flags dropped into anime panels, 3D BLUBZ PRESENTS and WORLD CUP titles, flash cuts. See also 01-football #15.
- Techniques: kinetic-type, 3d-text, bg-swap, color-flash, build-to-drop
- Steal this: tie the edit to a tournament moment with country flags as colour blocks; flags are free, instantly readable graphics.

### 28. Timeless | Squid Game S2 (sanchezae): 3D type inside scenes, wings and ocean
- Link: https://www.youtube.com/watch?v=2rsf0_hmfGU | YouTube (landscape, 39 s) | Creator: @sanchezae | Subject: Squid Game S2 (translates to sports) | Song: Timeless Guitar Remix [TikTok ver.] | 1.85M views, 90.4K likes | 2025-01-24
- Why it's elite: [F] The same toolkit as the football edits at its top level: extruded gradient type that sits in the set (LEGIT on the ocean), an angel-wing composite behind a character, radial warps, an animated logo outro. Evidence that this look sells at 1.8M views.
- Techniques: 3d-text, text-behind-subject, bg-swap, roto-cutout, radial-zoom-blur, outro-card
- Steal this: a one-second logo or song-card outro that animates like the rest of the edit.

### 29. Homelander "BLOODY BRAZIL" (sanchezae): outline lettering behind the character
- Link: https://www.youtube.com/watch?v=aZ363CKSTfI | YouTube (landscape, 31 s) | Creator: @sanchezae | Subject: Homelander (The Boys) | Song: TENZOO - BLOODY BRAZIL | 1.31M views, 42.9K likes | 2024-06-29
- Why it's elite: [F] Huge hollow-outline and filled lettering (I'M NOT SUGGESTING, ANYMORE, BETTER) in blue/red neon placed behind the cut-out character, with lens flares and bursts; a template for outline-text over roto.
- Techniques: outline-text, text-behind-subject, roto-cutout, glow, lens-flare, 3d-text
- Steal this: alternate hollow-outline and solid words behind the same person so the beat reads as "fill" vs "empty".

### 30. Sukuna's Dance, Bullseye (sanchezae): neon-sign type, fire and a phone-screen insert
- Link: https://www.youtube.com/watch?v=7l3VjQwXqk8 | YouTube (landscape, 22 s) | Creator: @sanchezae | Subject: Sukuna (JJK) | Song: Icey AK - Bullseye (feat. Rarin) | 521K views, 17.0K likes | 2024-06-19
- Why it's elite: [F] 3D neon-sign DANCE in perspective, BULLSEYE lettering behind the character, fire energy around the body, and a phone-screen frame that shows the dance reel inside the scene. Shows type, FX and a screen insert in 22 s.
- Techniques: 3d-text, text-behind-subject, particles (fire), roto-cutout, split-screen-grid (phone insert)
- Steal this: put the "reel" inside a phone or TV in the scene for one beat; it frames the athlete and plays the platform inside itself.

### 31. One Piece "Life Force" (Molob): hit FX layers on every impact
- Link: https://www.youtube.com/watch?v=XN_fwAgjhGs | YouTube (landscape, 19 s) | Creator: @Molob (418K subs) | Subject: One Piece (translates to sports) | Song: Life Force, RJ Pasin | 964K views, 40.3K likes | 2024-10-30
- Why it's elite: [F] Title says it took far too long. Ice, fire and water FX layers burst on each impact, film-strip frames and heavy blur; After Effects 2021. A model for "every hit gets a different material" (ice, flame, water).
- Techniques: overlay-texture (ice/fire/water), particles, motion-blur, speed-ramp
- Steal this: give each sound hit a different material layer (ice, spark, smoke) so no two hits look the same.

### 32. Hikari (Rethink:cc): neon glitch density and a tutorial-for-likes end card
- Link: https://www.youtube.com/watch?v=v8BwXIdNqZ8 | YouTube (landscape, 25 s) | Creator: @rethink_cc (20K subs) | Subject: Gojo (JJK, translates to sports) | Song: Hikari - Clovis Reyes and VDYCD | 1.13M views, 40.1K likes | 2025-03-01
- Why it's elite: [F] Title: "Making this edit nearly BROKE my pc". It opens on screenshots of viewer comments, then dense purple/cyan glitch, RGB split and electric overlays with white flashes; it ends on "200 likes and i release a tutorial on the formula also subscribe cuz why not", an engagement hook.
- Techniques: glitch, rgb-split, chromatic-aberration, strobe, overlay-texture, white-flash
- Steal this: open with real viewer comments as the hook and promise something at a like target on the end card (stems, project file, bonus ending); it turns the last second into a CTA.

### 33. Collage trail effect (Toby Garrow tutorial): echo images locked to the camera move
- Link: https://www.youtube.com/watch?v=uJor5NsSohk | YouTube tutorial (445 s, chapters: Principles, Tutorial, Tracking Data, Adding Effects) | Creator: @tobygarrow (12.3K subs; IG tobygarrow) | Subject: sports graphics | Song: n/a | 491K views, 29.1K likes | 2023-04-22
- Why it's elite: [M] The description describes it as a collage trail effect that is very common in current sports graphics (2023); a script by Luke Harris automates the parenting step. The clone-trail family (see 22, 34, 35) is the standard way to show a move.
- Techniques: clone, echo-trails, split-screen-grid (collage), 3d-camera
- Steal this: trail the SAME cut-out in a staggered collage along the camera move instead of an opacity echo.

### 34. NBA Playoffs commercial motion trail (Peter Sarellas tutorial): roto, motion blur, trail
- Link: https://www.youtube.com/watch?v=Bhouu0sLNJ0 | YouTube tutorial (1203 s) | Creator: @petersarellas (43.2K subs) | Subject: ESPN NBA Playoffs 2024 spot (reference commercial itself not located) | Song: n/a | 38.1K views, 1.8K likes | 2024-05-03
- Why it's elite: [F] Chapters: Selecting the right footage, Rotoscoping the subject, Adding motion blur, Compositing the scene, Creating the motion trail, Stylizing the trail. On-screen shot criteria (seen in frames): subject moves in one direction, nothing crossing in front of the subject, strong contrast, shallow depth of field.
- Techniques: roto-cutout, echo-trails, motion-blur, bg-swap
- Steal this: pick clips for roto by those four criteria and you cut roto time sharply; the criteria are a clip-selection checklist.

### 35. Gatorade commercial clone trail (Peter Sarellas tutorial): ghost dunkers
- Link: https://www.youtube.com/watch?v=lo8CpAeYafs | YouTube tutorial (651 s, chapters: Creating the Mask, Animating the Mask, Duplicating the Effect, Animating the Effect) | Creator: @petersarellas | Subject: basketball, Gatorade ad (reference commercial not located) | Song: n/a | 43.9K views, 2.4K likes | 2020-11-24
- Why it's elite: [F] The opening frames show the Gatorade "FOREVER" spot with several ghost copies of one dunking player in the air at once. A 2020 classic still cited in 2024 trail tutorials; follow-up: Freeze Clone Trail in AE 2024 (https://www.youtube.com/watch?v=xUgwZhl169w).
- Techniques: clone, echo-trails, roto-cutout, freeze-frame
- Steal this: freeze the hero at 3-4 moments of one move and keep each copy on screen; a "multi-exposure" hit that fits a bar of music.

### 36. House of Highlights / Boxing Loop VFX breakdown (C.M. de la Vega): particles, anime freeze, fire, glow
- Link: https://www.youtube.com/watch?v=yc5D1ASrnzw | YouTube tutorial (655 s, chapters: Particle effects, Anime style freeze frame, Fire and spark compositing, Advanced glowing character) | Creator: @cmdelavega (96.9K subs) | Subject: viral sports pages (House of Highlights, Boxing Loop) | Song: n/a | 5.7K views | 2021-07-19
- Why it's elite: [F] Breaks down the effect types those IG sports pages use: particle bursts on impact, an anime-style freeze frame, fire and spark composites, a glowing outline character. Old, but the effect list is still the menu.
- Techniques: particles, freeze-frame, outline-stroke, glow, overlay-texture (fire/sparks)
- Steal this: use his four effect types as a checklist for hit moments: burst, freeze, flame, glow-outline.

### 37. FENDI trend edit (Dhruv Efx, Ronaldo): neon ring around an outlined cut-out
- Link: https://www.youtube.com/watch?v=97NU_R8Q5yI | YouTube (portrait card in a 16:9 frame, 19 s) | Creator: @DhruvEfx (Dhruv Efx, 7.18K subs) | Subject: Ronaldo | Song: Fendi 2 (Rakhim) per the Edits27 tutorial for the same trend | 14.2K views, 512 likes | 2025-12-18
- Why it's elite: [F] A small-channel copy of the Dec 2025 "FENDI" look: a glowing neon ring framing a roto'd, outlined Ronaldo, the keyword FENDI stacked three times as a yellow-glow ladder, ember circle on the beat. Description: After Effects / Alight Motion with XML presets and a character-cutout tutorial (https://www.youtube.com/watch?v=nm-HG5xfACw). Mobile editors can reach this look.
- Techniques: outline-stroke, glow, roto-cutout, kinetic-type, split-screen-grid (framed card)
- Steal this: ring-plus-outline around the cut-out, with the hook word stacked 3x in glow, as the "song hook" frame on the chorus.

---

## 2. Creators / accounts to study

| Handle | Platform | Link | Signature style (roto/compositing) | Followers if seen |
|---|---|---|---|---|
| @sanchezae | YouTube (IG sanchezamv1, TikTok sanchezamv) | https://www.youtube.com/channel/UCH2bqtMMFTB1m2pA80E40Eg | 3D/extruded type behind roto'd subjects, scene swaps, celebrity cameos (IShowSpeed); AE 2024; sells project files | YT 417K; IG 155K; TikTok "400K+" (own bio) |
| @HeroEdit_ae (Hero Edit) | YouTube | https://www.youtube.com/channel/UCs9x_hj1sinFSMdFNEmvEDw | Effect-first football edits (roto outline aura, particles); CapCut vs AE challenges that show effect cost | YT 48.5K |
| @iluxha_aep (iluxhaep) | YouTube (TikTok @iluxhaep) | https://www.youtube.com/channel/UC8xwDBgBu9plFK4ziPgl2LA | Montagem hard edits: neon outline type, HUD rings, Blender; cuts own audio | YT 12.6K |
| @Dr1zzy.aep. (Dr1zzy) | YouTube (IG dr1zzy.aep, TikTok @dr1zzy_tktk) | https://www.youtube.com/channel/UCxOHqUoVcZL5xFtsfxSSRYw | Football x anime composites, echo trails, particle dissolves; releases edited audio too | YT 26.3K; IG 3.2K |
| @pyeftbl | YouTube (TikTok @pyeftbl) | https://www.youtube.com/channel/UCE_TIQteaxc2rKS940amhFw | Tracked stadium text and lightning (2023 long edit); Shorts channel | YT 41.6K |
| @slicx7 (Slicx7) | YouTube | https://www.youtube.com/channel/UCX71Nred0VUttoV98i_9OUw | Player text tracking, glow names on shirts; huge Shorts reach (top Shorts 2.2M to 8.1M views, Aug-Oct 2026); style copied by many tutorials | YT 4.67M |
| @fictic_editz (FicTic) | YouTube + IG fictic_editz | https://www.youtube.com/channel/UCKCx4uzF33YfzcQFIflhfIg | Meme-structure edits, scribble marks, pop-up cutout transitions, free AE packs | YT 720K; IG 241K |
| @bela-films (Bela Films) | YouTube | https://www.youtube.com/channel/UC-TuibyYcf-20cq98PcnIew | One-colour typographic F1 edits with type behind drivers (Kendrick audio) | YT 6.79K |
| @yunsuv | YouTube | https://www.youtube.com/channel/UCSsr7z9jDd7APrgjqSHHC_w | F1 edits with giant serif type behind the driver; poster palettes | YT 2.08K |
| @austineditz (Austin Edits) | YouTube | https://www.youtube.com/channel/UCr9i2UveBVqtp_t9JBS6LDQ | Neymar cut-out collages, AE | YT 5.62K |
| @crn7.aep1 | YouTube | https://www.youtube.com/channel/UCdYT_dFvb3gVQyYDDrm1arw | Neon and glitch tracked type into pitch footage; AE 2024 | YT 1.53K |
| @FootyAnimeFlicks | YouTube | https://www.youtube.com/channel/UC5-tLaGjMJh-MnkDIni0KMg | Lightning/energy overlays on Ronaldo | YT 2.06K |
| @Blubzz (Blubz) | YouTube | https://www.youtube.com/channel/UCUZROQKH8W636R3nHwSIFdg | Football-anime World Cup crossovers with 3D titles | YT 143K |
| @Molob | YouTube | https://www.youtube.com/channel/UCzUkYRCLaWNm6MgPq6NiRhQ | Anime AMV with material FX per hit (ice, fire, water); AE 2021 | YT 418K |
| @rethink_cc | YouTube | https://www.youtube.com/channel/UCWiOE7MFUlhOTptf7DirS8g | Dense neon glitch AMV; end-card CTA | YT 20K |
| @ImaginaryFootball_ch | YouTube | https://www.youtube.com/channel/UCRdaKeoN45gI42rBCl70sWw | Viral scale/composite gags (giant Messi) | YT 32.7K |
| @henycreate (HENYCREATE) | YouTube | https://www.youtube.com/channel/UCQCg6vdyo0pW_-I_iI6f-6Q | World Cup 2026 motion-design promos (numerals, silhouettes) | YT 313 |
| @p3dits (P3DITS) | YouTube (IG p3dits_ig, TikTok p3dits_tt) | https://www.youtube.com/channel/UCX5lktQweL1v3v2tIY6OviQ | NBA edits, polished caption/type system (little roto; see 02, 05) | YT 28K; IG 22.7K |
| @petersarellas | YouTube (IG psarellas) | https://www.youtube.com/channel/UCQyOY90tpeWVHtuaL0SpMYg | Freelance sports videographer; clone/motion trail breakdowns of TV spots | YT 43.2K |
| @tobygarrow | YouTube (IG tobygarrow) | https://www.youtube.com/channel/UCRv29Vi9SC2GZRsqeJdzUHA | Sports graphics: collage trail | YT 12.3K |
| @TyloFX (Tylo FX) | YouTube | https://www.youtube.com/channel/UCZ7Xo1VHf53y_KsW5rT9yig | Sports-edit effect tutorials (text reveal, scribble outline, transitions) | YT 62.9K |
| @cmdelavega (C.M. de la Vega) | YouTube | https://www.youtube.com/channel/UCSh0sqPs9SoZRWn0VlaXccA | Sports VFX breakdowns and toolkits | YT 96.9K |
| @hoboedits0 (HOBO Ae) | YouTube | https://www.youtube.com/channel/UCkYHlDumH7P93VxBcgAsbvQ | AE football-edit tutorials: depth style, GTA trend, head tracking, Twixtor, Topaz | YT 81.8K |
| @4nasxd (AnasFTBL) | YouTube (TikTok @4nas.ftbl) | https://www.youtube.com/channel/UCA5N29hNiGQbQrrG_7f2Y_A | AE tutorial for the tvrood trend ("Clip preparation and ai" chapter) | YT 60.6K |
| @NDKEdit | YouTube | https://www.youtube.com/channel/UCOVro7KprlP7Sf4RfxNGpfQ | CapCut tutorial for the tvrood style (192K views) | YT 111K |
| @xxahid | YouTube | https://www.youtube.com/channel/UCzQLZdT2_vg6FzrpFoI3b_g | Long AE breakdown of the sanchezae style | YT 10.1K |
| @DhruvEfx (Dhruv Efx) | YouTube | https://www.youtube.com/channel/UCcRFvEtYNW3WbBqmGIipanA | Alight Motion / AE trend copies with free XML presets (FENDI character cutout, No Batidao) | YT 7.18K |
| @tvrood and @ftb.aep | TikTok (handles seen in tutorial titles, profiles not reachable) | n/a | Originators of the "tvrood style" (Montagem Tenta, Mar 2026) | not seen (unverified) |

---

## 3. Breakdowns / tutorials found

Edit-style breakdowns (finished-edit looks):
| Title | Link | Technique |
|---|---|---|
| Edit Like Sanchezae - Step-by-Step AE Tutorial (XXAHID, 1322 s, 111K views, 2025-07-25) | https://www.youtube.com/watch?v=JXgeSUU1D4M | the sanchezae look: 3D/roto type, scene composites (entries 1-3) |
| @slicx7 Like Player Text tracking tutorial on After Effects (Edits27, 2026-03-06) | https://www.youtube.com/watch?v=UrH7AuGlMb0 | tracked-text on players (entry 10) |
| Player Text tracking tutorial on CapCut (FB Edits, 291K views) | https://www.youtube.com/watch?v=iJC4jSn8zvs | tracked-text, mobile version |
| @slicx7 Like Player Highlight Effect On CapCut (FB Edits, 242K views) | https://www.youtube.com/watch?v=oYEYm0_0wx0 | player highlight / outline glow |
| @slicx7 Like Texture Text Edits On CapCut (FB Edits, 167K views) | https://www.youtube.com/watch?v=nsXfsnQw6w0 | textured type |
| Text Reveal Effect - After Effects Tutorial (Sports Edits) (Tylo FX, 2023-10-28; chapter "Masking") | https://www.youtube.com/watch?v=Uh7oVUm347M | text reveal behind subject; "pretty popular in sports editing" |
| SCRIBBLE OUTLINE EFFECT - AFTER EFFECTS (Tylo FX, 405 s) | https://www.youtube.com/watch?v=lDwlM-p0bk0 | scribble outline |
| Paper Outline Effect Tutorial - After Effects (Tylo FX, 106K views) | https://www.youtube.com/watch?v=8jcBW6wJh-U | paper/cut-out outline |
| Effect Ideas For Your Sport Videos (Tylo FX, 114K views, 2022) | https://www.youtube.com/watch?v=eovjI9fHwHE | three sports effects |
| FicTic Like Pop Up Cutout Transition (SLIPTIC, 2025-10-23; chapters: freeze frames, masking the subject, white flash, pop out, camera shake) | https://www.youtube.com/watch?v=slMj3A0U8DY | freeze-frame cutout pop-out |
| Character Introduction Freeze Animation, Premiere Pro (Enam Alamin, 486K views) | https://www.youtube.com/watch?v=j_UOvUeZEjI | freeze-frame character intro in Premiere (our stack) |
| CapCut Tutorial: Character Introduction Edit (The TecNIL, 440K views) | https://www.youtube.com/watch?v=GzODpc4g5Hs | freeze-frame cutout with name card, mobile |
| Trending CUTOUT Transition Edit In CapCut (DarkJen 2.0, 260K views) | https://www.youtube.com/watch?v=MQPcuCLb24E | cutout transition |
| Instagram Trending Masking Editing Tutorial, Glowing Cutout, CapCut (shahfaiz_editz, 378K views) | https://www.youtube.com/watch?v=t9dqmMpxjhE | glowing cutout mask |
| Ripped Paper Effect Transition in Premiere Pro (GlintDrox, 82K views) | https://www.youtube.com/watch?v=ucfJMxPTdLo | paper rip reveal in Premiere |
| How to Edit an EPIC Ripped Paper Transition, Premiere Pro (Peter Sarellas, 697 s) | https://www.youtube.com/watch?v=txiG3zaKHx8 | paper rip reveal, sports videographer |
| Outline Effect Tutorial in After Effects, AMV (Smertimba Graphics, 135K views) | https://www.youtube.com/watch?v=dfxrPt3TXZ8 | outline-stroke |
| CRAZY GLOW OUTLINE EFFECT in After Effects (Bryan Delimata, 86K views) | https://www.youtube.com/watch?v=ZI1sYf_NYKA | glowing outline (found by search; not frame-checked) |
| Aura Effect Tutorial (Royale_aep, 68K views) | https://www.youtube.com/watch?v=7RfVQuKDWcM | aura / energy around a subject |
| Neymar Energy Football Effect (MB AE Tutorials, 2025-09-24) | https://www.youtube.com/watch?v=DT1SxlSdQG8 | electric energy ball with glow |
| How to Create a FIRE BALL EFFECT, Football Edits (Goal Media, 55K views) | https://www.youtube.com/watch?v=47RiwEQ9240 | fire on the ball |
| effects for jugg edits, After Effects (naevisvfx, 60 s, 318K views, 2025-05-29; effect names are on screen: Fractal Noise, BCC Textured Wipe, Tracking Box, BCC Atmospheric Glow, Screen Blending Mode Clip Reveal, S_WarpBubble + S_WarpWaves, Levels, Crosssphere Bokeh) | https://www.youtube.com/watch?v=uQoBVfT7PKA | catalog of AE effect looks with their plugin names (frame-checked); AMV scene, translates to sports |
| VFX Breakdown: House of Highlights / Boxing Loop (C.M. de la Vega) | https://www.youtube.com/watch?v=yc5D1ASrnzw | particles, anime freeze frame, fire, glow outline |
| NBA Playoffs commercial motion trail (Peter Sarellas) | https://www.youtube.com/watch?v=Bhouu0sLNJ0 | roto + motion trail |
| Gatorade commercial clone trail (Peter Sarellas) | https://www.youtube.com/watch?v=lo8CpAeYafs | clone trail |
| Freeze Clone Trail Effect in AE 2024 (Peter Sarellas, 1452 s) | https://www.youtube.com/watch?v=xUgwZhl169w | freeze + clone trail |
| Creating a Collage Trail Effect (Toby Garrow) | https://www.youtube.com/watch?v=uJor5NsSohk | collage trail |
| CapCut Tutorial - Freeze Frame Clone Trail Effect (Tinh, 659K views) | https://www.youtube.com/watch?v=esVryXgaqE0 | clone trail on mobile |

2025-26 trend tutorials (each rides a specific sound; see Patterns):
| Title | Link | Technique |
|---|---|---|
| "Tvrood Style Edit" trend on CapCut, MONTAGEM TENTA (NDK Edit, 192K views) | https://www.youtube.com/watch?v=wRXFfd6EoSY | tvrood style (roto outline on HUD card, 3D camera) |
| New Football @tvrood Trend edit on After Effects + PJF (AnasFTBL, 44K views, 2026-03-16; chapters: Clip preparation and ai, Camera animation setup, Smoothing with plugins) | https://www.youtube.com/watch?v=Ew3VS7OvDc4 | tvrood style in AE |
| depth style trend tutorial on After Effects (HOBO Ae, 61K views, 2026-08-17) | https://www.youtube.com/watch?v=nPKy09lfoTc | depth style |
| HOW TO: Make A Depth Style Edit, After Effects (rdylt09, 53K views, 2026-08-20; chapters incl. Face tracking and positioning, Color and depth effects) | https://www.youtube.com/watch?v=ZbM2ZWPgDBg | depth style |
| New viral depth map style trend tutorial on CapCut (FB Edits, 21K views, 2026-08-20) | https://www.youtube.com/watch?v=ToFFptYXWRA | depth style on mobile |
| Trending DEPTH Effect in Alight Motion (Alit Editz, 53K views; chapters: Remove BG, Depth Effects Steps) | https://www.youtube.com/watch?v=GiyCpHxVej0 | depth style with background removal |
| Viral Football DEPTH STYLE trend in CapCut (MT_EDITZ, 15K views, 2026-08-17) | https://www.youtube.com/watch?v=c_y7bCHdZjo | depth style |
| Full FENDI Trend Edit tutorial on After Effects (Edits27, 27K views, 2025-12-18) | https://www.youtube.com/watch?v=eg28notnbqg | FENDI trend (song Fendi 2, Rakhim) |
| FENDI STYLE CHARACTER CUTOUT TUTORIAL (Dhruv Efx, Alight Motion) | https://www.youtube.com/watch?v=nm-HG5xfACw | character cutout |
| Viral Football GTA Edit on After Effects (Edits27, 2026-06-03; AI prompts for GTA-style art in description) | https://www.youtube.com/watch?v=3X-H8RAEC_Y | GTA loading-screen illustration trend |
| Viral 3D Camera View Effect on After Effects (Edits27, 2026-03-21; song Montagem Tenta) | https://www.youtube.com/watch?v=keQxgWtzvxw | 3d-camera on a flat clip |
| How to make a football edit on After Effects (HOBO Ae, 379K views; chapters: head tracking, twixtor, topaz) | https://www.youtube.com/watch?v=Y8h380HdGCM | full AE football edit |
| How to Make Football Edit in After Effects (MORIZ EDIT; chapter Text tracking) | https://www.youtube.com/watch?v=oL4FX-XQDwY | text tracking |
| Trending MONTAGEM GUERREIRO Full Edit (Gujju Edition, 1554 s; chapters: tracking and stabilization, applying visual effects) | https://www.youtube.com/watch?v=aeY-6Hesu-o | Montagem full edit |

Roto and matte tools creators publicise (what people say they use):
| Title | Link | Tool |
|---|---|---|
| After Effects NEW Object Matte Tool, AI Rotoscoping is HERE (Lines To Designs, 89K views) | https://www.youtube.com/watch?v=wvKtlB0fRoU | AE Object Matte (see 09 #26) |
| I Can't Believe Meta SAM 2 Beat Adobe at This (Lines To Designs) | https://www.youtube.com/watch?v=CbyO-5yM11o | Meta SAM 2 vs Adobe |
| 7 Roto Brush Secrets (Lines To Designs, 128K views) | https://www.youtube.com/watch?v=s8oL-rS29fc | AE Roto Brush |
| Replace rotoscoping using SAM3 AI model in ComfyUI (Diyz3n) | https://www.youtube.com/watch?v=mmwFq0GkiP8 | SAM 3 in ComfyUI |
| How to ROTOSCOPE / MASK OUT A PERSON in DaVinci Resolve and Runway (GoldenEye.mp4, 125K views) | https://www.youtube.com/watch?v=LzRWGdx1H2A | Runway + Resolve |
| I used AI to ROTOSCOPE in PREMIERE PRO, Runwayml (AKV-Studios, 92K views) | https://www.youtube.com/watch?v=ZfMJTXVQezE | Runway into Premiere |
| AI Rotoscoping Vs DaVinci and After Effects (Joshua M Kerr) | https://www.youtube.com/watch?v=AHeXHIT-jT8 | comparison |
| Text Behind Person Effect, CapCut (Digital Guide, 833K views) | https://www.youtube.com/watch?v=sKF5vQsZZs0 | CapCut auto cutout / remove background |
| Easiest ROTOSCOPING METHOD using Mocha Pro (Phoenix, 44K views) | https://www.youtube.com/watch?v=9AUzHoY0r4c | Mocha |
| Editing Challenge #3: 1 Minute vs 10 minutes vs 1 Hour (Hero Edit, 535K views; chapters at 1:23, 2:10, 3:10) | https://www.youtube.com/watch?v=t_v7xQs68eo | effect level per hour of work |
| 10 Minutes vs 1 Hour vs 10 Hours: Which Edit Is Better? (AE Stark, 152K views, 2026-07-12) | https://www.youtube.com/watch?v=bckig93C8Qc | effect level per hour of work |

Other tools named by creators in descriptions or captions: Blender (iluxhaep entry 4), Twixtor (sanchezae), Topaz (HOBO Ae), After Effects 2020/2021/2024 (Dr1zzy, Molob, crn7.aep., sanchezae), Alight Motion XML presets (Dhruv Efx), "BCC+DEPTH MAP ML" (IG @know_with_haroon, unverified what the plugin name is), "PJF" presets (AnasFTBL). No creator in what I read names a specific AI roto tool for football edits; the visible methods are AE Roto Brush or Mocha for AE editors and CapCut/Alight "remove background" for mobile editors.

---

## 4. Patterns noticed

- Type is the compositing layer. The strongest roto work here is not an outline but a GIANT word placed behind the cut-out athlete (sanchezae 3D type, iluxhaep neon outline type, yunsuv and Bela serif/orange type, Sky and HENYCREATE numerals). The word is bigger than the person, so it still reads at phone size.
- One visual system per edit, effects vary inside it. Bela keeps one orange; yunsuv one red serif; Hero one cyan aura; sanchezae pink/gold. The type and palette stay fixed so heavy effects do not look random.
- Roto is spent on the hero frame, not the whole clip. Outline auras, particle edges and dissolves last about 1-3 s on the key shots (Hero about 13 s, Ronaldo ember about 15 s, Dr1zzy dissolve at about 1:05); the rest is cc-grade, blur and cuts. Budget roto for 4-6 hero moments, not every clip.
- Clip choice decides roto cost. Peter Sarellas' checklist (subject moves one direction, nothing crossing in front, high contrast, shallow depth of field) is the cheapest way to avoid bad mattes; also use the highest-quality source (compressed broadcast footage mats badly).
- Scenes, not just effects. The top edits swap the WORLD around the cut-out (Viking sea, clouds, tunnel, stage, bokeh), and the player is the constant. A 1-second environment swap on the drop reads as a bigger move than another flash.
- Human marks sell polish: hand-scribbled words and arrows (FicTic, sanchezae "I AM"), ink-hatch texture (Hero), torn-paper edges, rounded-corner insets. Cheap, readable on a phone, hard for competitors to copy exactly.
- Trends are effect + sound packages and move in weeks. tvrood style rides "Montagem Tenta" (Mar 2026; edit-audio uploads of Montagem Tenta alone reach 2.2M to 5.4M views), FENDI rides "Fendi 2" (Dec 2025), depth style rides "Pursuit" (Aug 2026), GTA edit (Jun 2026). Depth style alone had at least six tutorials dated 17-28 Aug 2026 (4K to 61K views each; AE, CapCut, Alight Motion), so a client track that owns a visual trend gets pulled up with it.
- The edit and the audio are one product. Top AE editors cut the audio themselves (FL Studio, "Edited by me", separate audio channels) and sell project files; for us that means delivering a slowed or ultra-slowed variant of the client song as part of the package.
- Cross-posting: sanchezae posts landscape edits as letterboxed Shorts (Speed x Ronaldo Short 1.0M, Messi Short 279K, Haaland Short 141K). The best hard edits on YouTube are mostly 16:9; vertical-native ones live on TikTok/IG, which I could not open. Check IG/TikTok directly before copying a 16:9 look into 9:16.
- Reach comes from concept first: giant Messi (10.4M), FicTic pun edits (8.9M), CapCut vs AE side-by-side (3.0M) all win on one idea that is legible in the first second; the compositing is only the carrier.
- Credits and inspiration chains are open: iluxhaep and Dr1zzy both write "ib: @sanchezae" in descriptions, tutorials are named "like @slicx7", "like @sanchezae", "like FicTic". Approaching a top editor for a promo is the norm (they list "DM for promo").
- Gap: no standout colour-pop sports edit found. Only B&W-to-colour (NBA on ESPN spot, entry 26) and mobile tutorials; if we want colour-pop it is likely a mask plus grade job we define ourselves.
