# 01 Shot labels: WHP and ATN

Status: see bottom line. Plain labels for every shot in both reels.

Sources: shot starts and short labels from `research/dhruvxr/raw/shots_by_hand.json` (31 WHP, 26 ATN). On-screen words from `research/dhruvxr/STUDY.md` sections 6 and 7 (frame ranges read there by hand), mapped to shots by frame overlap. Spoken words from `x-videos/*.transcript.json` (Whisper word times), any word whose time overlaps the shot. Seconds = frame / fps (WHP 30, ATN 29.97). "End" is the last frame of the shot (inclusive).

Measured vs judged: frames, seconds and spoken-word overlap are computed. Mono/colour is measured where marked "sat" (mean HSV saturation of the shot, 0 to 1, from the video). Shot type, what it shows and subject size are judged by eye and are marked as such. Claude cannot watch or hear; all picture judgments come from still strips and frames.

Shot type key: live footage (looks shot for this piece), stock-like (footage or photo that reads as library/archive material), designed graphic (made in software: marks, type cards, particles, collages), UI (screens, web pages, product interface), flash (1 to 2 frame white or bright frame), black.

## WHP (Whop brand film, 30 fps, 494 frames, 16.47 s)

| # | Frames (start-end, count) | Seconds | What it shows | Words on screen | Words spoken | Type | Subject size (% of frame, judged) | Mono / colour |
|---|---|---|---|---|---|---|---|---|
| 1 | 0-3 (4 f) | 0.00-0.13 (0.13 s) | Whop mark of dots | none | none | designed graphic | mark about 3 to 8%, centred on black (strip-checked) | mono (sat 0.002, colour px 0%, luma 0.04) |
| 2 | 4-5 (2 f) | 0.13-0.20 (0.07 s) | light bulb | none | none | stock-like | bulb about 20% (full height, narrow) (strip-checked) | mono (sat 0.002, colour px 0%, luma 0.22) |
| 3 | 6-7 (2 f) | 0.20-0.27 (0.07 s) | flare threshold | none | none | stock-like | white splash / bulb-skull composite about 15 to 30% (strip-checked) | mono (sat 0.004, colour px 0%, luma 0.14) |
| 4 | 8-9 (2 f) | 0.27-0.33 (0.07 s) | MRI head front | none | none | stock-like | head about 10 to 20%, grows over 2 f (strip-checked) | mono (sat 0.001, colour px 0%, luma 0.13) |
| 5 | 10-10 (1 f) | 0.33-0.37 (0.03 s) | white flash | none | none | flash | full-frame white (100%) (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.98) |
| 6 | 11-15 (5 f) | 0.37-0.53 (0.17 s) | pen macro | none | none | stock-like | pen about 10%, then hand about 60% (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.53) |
| 7 | 16-23 (8 f) | 0.53-0.80 (0.27 s) | hand writing desk | "// Ideas //" | none | stock-like | hand and pen about 10%, right edge (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.48) |
| 8 | 24-32 (9 f) | 0.80-1.10 (0.30 s) | pen line | "// Ideas //"; "@ Ideas //" | none | stock-like | hand and pen about 20%, upper right (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.65) |
| 9 | 33-44 (12 f) | 1.10-1.50 (0.40 s) | calligraphy pen low | "@ Ideas //" | Ideas. | stock-like | pen about 30%, diagonal (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.53) |
| 10 | 45-45 (1 f) | 1.50-1.53 (0.03 s) | white flash | "@ Ideas //" | Ideas. | flash | near full-frame white, pen silhouette about 10% (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.86) |
| 11 | 46-75 (30 f) | 1.53-2.53 (1.00 s) | ink drip macro | "@ Ideas //" | Ideas. | stock-like | pen tip and ink blot about 15%, top centre (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.54) |
| 12 | 76-77 (2 f) | 2.53-2.60 (0.07 s) | crowd + Audience | "Audience" | none | stock-like | crowd fills frame (100%), faces about 10% each (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.71) |
| 13 | 78-80 (3 f) | 2.60-2.70 (0.10 s) | white blowout | none | none | flash | blown-out face about 40% (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.89) |
| 14 | 81-85 (5 f) | 2.70-2.87 (0.17 s) | threshold crowd | "// Audience 0"; "@/ visibility //" | none | stock-like | crowd texture fills frame (100%) (strip-checked) | mono (sat 0.017, colour px 0%, luma 0.24) |
| 15 | 86-90 (5 f) | 2.87-3.03 (0.17 s) | crowd top-down | "// Audience 0"; "@/ visibility //" | none | stock-like | crowd texture fills frame (100%) (strip-checked) | mono (sat 0.015, colour px 0%, luma 0.12) |
| 16 | 91-111 (21 f) | 3.03-3.73 (0.70 s) | checkout UI tilted | "// Audience 0"; "@/ visibility //"; UI text: "Checkout", "Pro membership", "$49.00", "Pay $49.00" | none | UI | UI card about 60% for 2 f, then about 20% (strip-checked) | low colour (sat 0.084, colour px 6%, luma 0.03) |
| 17 | 112-129 (18 f) | 3.73-4.33 (0.60 s) | scan-line glitch tear, then log list (text rows), white tear blocks | none | none | UI | glitch tears across full frame, then log-list text column about 15% (strip-checked) | low colour (sat 0.010, colour px 1%, luma 0.24) |
| 18 | 130-194 (65 f) | 4.33-6.50 (2.17 s) | keyhole of dots, ownership | "ownership"; "/ˈōnərˌSHip/" | Ownership. | designed graphic | keyhole about 8%, centred, with dot clusters about 10% more (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.04) |
| 19 | 195-196 (2 f) | 6.50-6.57 (0.07 s) | white flash | "ownership"; "/ˈōnərˌSHip/" | Every | flash | full-frame white (100%) (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.99) |
| 20 | 197-242 (46 f) | 6.57-8.10 (1.53 s) | star particles | "ownership"; "/ˈōnərˌSHip/" | Every business. One | designed graphic | scattered star dots, each under 1%; keyhole fades out under them by about 6.77 s (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.01) |
| 21 | 243-244 (2 f) | 8.10-8.17 (0.07 s) | white logo bloom | none | One | flash | white bloom about 80%, mark about 5% (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.80) |
| 22 | 245-286 (42 f) | 8.17-9.57 (1.40 s) | glowing mark | none | One checkout. | designed graphic | mark about 5% with glow, shrinking to about 2% (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.06) |
| 23 | 287-300 (14 f) | 9.57-10.03 (0.47 s) | mark of photo tiles, this | "this" | This | designed graphic | tile mark about 5%, centre (strip-checked) | mono (sat 0.004, colour px 0%, luma 0.01) |
| 24 | 301-321 (21 f) | 10.03-10.73 (0.70 s) | photo collage | "this"; "$150M", "[ 14:02 ]" | This is where | designed graphic | collage cluster about 25%, each photo tile 2 to 4% (strip-checked) | low colour (sat 0.064, colour px 8%, luma 0.07) |
| 25 | 322-322 (1 f) | 10.73-10.77 (0.03 s) | white flash | none | where | flash | near full-frame white, faint hall silhouette (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.89) |
| 26 | 323-330 (8 f) | 10.77-11.03 (0.27 s) | terminal crowd slow shutter | none | where the | stock-like | hall fills frame; blurred people about 5 to 10% each (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.57) |
| 27 | 331-336 (6 f) | 11.03-11.23 (0.20 s) | spiral stairs | none | the internet | stock-like | stair spiral fills frame, tiny figure about 2% at centre (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.28) |
| 28 | 337-342 (6 f) | 11.23-11.43 (0.20 s) | fisheye climber | none | internet | stock-like | fisheye circle about 80%, climber about 15% (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.35) |
| 29 | 343-410 (68 f) | 11.43-13.70 (2.27 s) | dot globe fading | none | internet gets paid. | designed graphic | dot globe about 25%, centred (strip-checked) | mono (faint tint) (sat 0.048, colour px 0%, luma 0.01) |
| 30 | 411-420 (10 f) | 13.70-14.03 (0.33 s) | black | none | none | black | none (black) (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.00) |
| 31 | 421-493 (73 f) | 14.03-16.47 (2.43 s) | Whop wordmark | Whop logo + wordmark | WAP .com | designed graphic | logo + wordmark about 1%, centre; fades in f421 to about f430 (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.00) |

## ATN ("attention" manifesto, 29.97 fps, 448 frames, 14.95 s)

| # | Frames (start-end, count) | Seconds | What it shows | Words on screen | Words spoken | Type | Subject size (% of frame, judged) | Mono / colour |
|---|---|---|---|---|---|---|---|---|
| 1 | 0-3 (4 f) | 0.00-0.13 (0.13 s) | Apple card: logo tile, "Apple" label, page preview ("iPhone 17 Pro") | "a" | Yo, | designed graphic | logo tile about 5%, page preview about 15% (strip-checked) | low colour (sat 0.045, colour px 6%, luma 0.09) |
| 2 | 4-7 (4 f) | 0.13-0.27 (0.13 s) | Meta card: logo tile, page preview ("It's Your World.") | "a"; "a great" | Yo, | designed graphic | logo tile about 5%, page preview about 15% (strip-checked) | low colour (sat 0.051, colour px 4%, luma 0.23) |
| 3 | 8-11 (4 f) | 0.27-0.40 (0.13 s) | Whop card | "a great" | Yo, | designed graphic | logo tile about 5% (strip-checked) | colour (sat 0.097, colour px 10%, luma 0.05) |
| 4 | 12-15 (4 f) | 0.40-0.53 (0.13 s) | Wise card | "a great prduct" | Yo, | designed graphic | logo tile about 5%, page preview about 15% (strip-checked) | colour (sat 0.226, colour px 34%, luma 0.15) |
| 5 | 16-18 (3 f) | 0.53-0.63 (0.10 s) | Figma card | "a great prduct" | none | designed graphic | logo tile about 5%, page preview about 15% (strip-checked) | colour (sat 0.138, colour px 21%, luma 0.23) |
| 6 | 19-22 (4 f) | 0.63-0.77 (0.13 s) | Adobe card | "a great prduct" | none | designed graphic | logo tile about 5%, artwork band about 15% (strip-checked) | colour (sat 0.222, colour px 26%, luma 0.07) |
| 7 | 23-26 (4 f) | 0.77-0.90 (0.13 s) | orange asterisk card | "a great prduct" | none | designed graphic | asterisk disc about 5% (strip-checked) | low colour (sat 0.032, colour px 4%, luma 0.03) |
| 8 | 27-27 (1 f) | 0.90-0.93 (0.03 s) | near black | "a great prduct" | none | black | none (black) (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.00) |
| 9 | 28-29 (2 f) | 0.93-1.00 (0.07 s) | ChatGPT card | "a great prduct" | if | designed graphic | dim logo about 3% (strip-checked) | low colour (sat 0.033, colour px 2%, luma 0.01) |
| 10 | 30-66 (37 f) | 1.00-2.24 (1.23 s) | eye macro, cards in iris | "Isn't enough anymore." | if you don't shut your | stock-like | eye fills frame (100%), iris about 30%, cards in it about 5% (strip-checked) | colour (sat 0.098, colour px 11%, luma 0.26) |
| 11 | 67-152 (86 f) | 2.24-5.11 (2.87 s) | 3D wall of websites | "It gets ignored." | your mouth, I'ma shut it for you, PUNK! | UI | page cards cover about 60%, single page about 10% (strip-checked) | low colour (sat 0.063, colour px 6%, luma 0.14) |
| 12 | 153-179 (27 f) | 5.11-6.01 (0.90 s) | MRI head side, Attention | "Attention" | PUNK! | stock-like | head about 25%, right of frame (strip-checked) | mono (sat 0.009, colour px 0%, luma 0.03) |
| 13 | 180-191 (12 f) | 6.01-6.41 (0.40 s) | skier ridge | "attention isn't earned" + "by features." | none | stock-like | skier about 1%, snow ridge about 50% (strip-checked) | colour (sat 0.157, colour px 26%, luma 0.74) |
| 14 | 192-194 (3 f) | 6.41-6.51 (0.10 s) | painting | "attention isn't earned" + "by features." | none | stock-like | skier cut-out about 1% over full-frame painting (strip-checked) | colour (sat 0.353, colour px 65%, luma 0.23) |
| 15 | 195-197 (3 f) | 6.51-6.61 (0.10 s) | statue fountain | "attention isn't earned" + "by features." | none | stock-like | skier cut-out about 1% over full-frame statue (strip-checked) | mono (faint tint) (sat 0.072, colour px 0%, luma 0.17) |
| 16 | 198-200 (3 f) | 6.61-6.71 (0.10 s) | statue Venus | "attention isn't earned" + "by features." | none | stock-like | skier cut-out about 1% over full-frame statue (strip-checked) | mono (faint tint) (sat 0.058, colour px 0%, luma 0.37) |
| 17 | 201-203 (3 f) | 6.71-6.81 (0.10 s) | ceiling fresco | "attention isn't earned" + "by features." | none | stock-like | skier cut-out about 1% over full-frame fresco (strip-checked) | colour (sat 0.181, colour px 20%, luma 0.31) |
| 18 | 204-206 (3 f) | 6.81-6.91 (0.10 s) | wave painting | "attention isn't earned" + "by features." | none | stock-like | skier cut-out about 1% over full-frame painting (strip-checked) | colour (sat 0.317, colour px 33%, luma 0.15) |
| 19 | 207-209 (3 f) | 6.91-7.01 (0.10 s) | angel statue | "attention isn't earned" + "by features." | none | stock-like | skier cut-out about 1% over full-frame statue (strip-checked) | colour (sat 0.176, colour px 20%, luma 0.30) |
| 20 | 210-215 (6 f) | 7.01-7.21 (0.20 s) | painting boat | "attention isn't earned" + "by features." | none | stock-like | skier cut-out about 1% over full-frame painting (strip-checked) | colour (sat 0.216, colour px 32%, luma 0.30) |
| 21 | 216-221 (6 f) | 7.21-7.41 (0.20 s) | It's earned wrap + inverted window | "It's earned" | none | designed graphic | text band about 25% of height, skier about 5% (strip-checked) | low colour (sat 0.131, colour px 5%, luma 0.76) |
| 22 | 222-245 (24 f) | 7.41-8.21 (0.80 s) | skier, It's earned box | "It's earned" | none | stock-like | skier about 1 to 2%, text box about 5% (strip-checked) | low colour (sat 0.084, colour px 6%, luma 0.82) |
| 23 | 246-278 (33 f) | 8.21-9.31 (1.10 s) | skier, by perception | "by perception." | none | stock-like | skier about 1%, small text under 1% (strip-checked) | mono (sat 0.022, colour px 0%, luma 0.88) |
| 24 | 279-309 (31 f) | 9.31-10.34 (1.03 s) | black | none | none | black | none (black) (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.00) |
| 25 | 310-389 (80 f) | 10.34-13.01 (2.67 s) | dhruv | "dhruv" | none | designed graphic | single small word under 1%, centre (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.00) |
| 26 | 390-447 (58 f) | 13.01-14.95 (1.94 s) | black | none | none | black | none (black) (strip-checked) | mono (sat 0.000, colour px 0%, luma 0.00) |

## Summary: share of runtime by shot type (from frame counts)

| Reel | Type | Shots | Frames | Seconds | Share of runtime |
|---|---|---|---|---|---|
| WHP | live footage | 0 | 0 | 0.00 | 0.0% |
| WHP | stock-like | 14 | 102 | 3.40 | 20.6% |
| WHP | designed graphic | 8 | 333 | 11.10 | 67.4% |
| WHP | UI | 2 | 39 | 1.30 | 7.9% |
| WHP | flash | 6 | 10 | 0.33 | 2.0% |
| WHP | black | 1 | 10 | 0.33 | 2.0% |
| WHP | total | 31 | 494 | 16.47 | 100% |
| ATN | live footage | 0 | 0 | 0.00 | 0.0% |
| ATN | stock-like | 12 | 157 | 5.24 | 35.0% |
| ATN | designed graphic | 10 | 115 | 3.84 | 25.7% |
| ATN | UI | 1 | 86 | 2.87 | 19.2% |
| ATN | flash | 0 | 0 | 0.00 | 0.0% |
| ATN | black | 3 | 90 | 3.00 | 20.1% |
| ATN | total | 26 | 448 | 14.95 | 100% |

Type is judged per shot, so the shares carry that judgment; the frame counts under them are measured.

## Notes and limits

- Frame count: ffmpeg decoded 493 WHP frames; the hand list says 494. So WHP shot 31 may end at f492, not f493 (1 frame, 0.2% of runtime). ATN decoded 448, matching the list.
- Mono/colour is measured: each shot's frames were scaled to 64x36, then mean HSV saturation and the share of pixels with saturation over 0.25 (and value over 0.1) were taken. Rule: mono if colour px under 1% and sat under 0.03; "mono (faint tint)" if colour px under 1% but sat higher; "low colour" if colour px 1 to 10%; "colour" above 10%. Luma is mean Rec.709 luma, 0 to 1.
- Result: WHP is mono in 29 of 31 shots; only the checkout UI (orange Pay button) and the photo collage carry colour. ATN is colour in the brand cards, the eye, the skier and the art backgrounds, and mono in the MRI head, the near-black frame and the end.
- Subject size is judged by eye from the every-frame strips, as rough % of frame area. Strips viewed: WHP 0-12 s and 14-16 s; ATN 0-12 s. Not viewed: WHP 12-14 s and 16-16.5 s, ATN 12-15 s (these fall inside long shots already checked elsewhere: WHP 29 globe, 30 black, 31 wordmark; ATN 25 dhruv, 26 black).
- "What it shows" is the hand label from shots_by_hand.json, extended where a strip was viewed. Words on screen come from STUDY.md frame ranges and were spot-checked against the strips viewed (they match, e.g. ATN "It's earned" ends f245, "by perception." f246 to f278, "dhruv" from f310). Brand-card names and page previews in ATN are third-party UI text, noted only for shots 1 and 2.
- Shot type is judged. No shot reads as live footage shot for the piece; every footage shot reads as library or archive material, so "live footage" is 0% in both reels. Origin of any shot was not checked.
- Spoken words: Whisper word times; a word is listed under every shot its time span overlaps, so a word can appear under two shots. Whisper writes the brand as "WAP.com"; the picture shows Whop. ATN "speech" is a voice sample in the music, not a voiceover.

Status: FINAL for this sprint (written 07:50 UTC). Gaps listed in Notes.
