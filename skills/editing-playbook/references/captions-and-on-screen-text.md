# Captions and on-screen text

What the words on screen say, where they sit, how they read, and when captions step aside. Animation recipes for
titles, kinetic type and caption effects live in motion-design; caption track mechanics and styling patches in
premiere-ae-editing (captions-style-patch.md, prproj-format.md).

## Contents
1. Readable on a phone first
2. Where text goes (safe zones in numbers)
3. When captions go off (caption rule 1)
4. The words must be true
5. Subtitles and caption chunks
6. House looks that were approved
7. Fonts and their traps
8. Names on files and on screen

## 1. Readable on a phone first
- Small text never sits straight on bright footage. The first name title was rejected: "the white is clashing with the
  sky", "not readable". Give small text a backing (a dark rounded plate at about 90% with a thin edge, a bottom
  gradient, or dark ink on a light card) and size it for a phone.
- Sizes that passed on 1080x1920: a name about 35 px on a dark plate, a sub line about 26 px; nothing under about 26 px
  (friend's rule); on native pages at most 2 text sizes and nothing under 40 px. 16:9 overlines 56 px or more. Small tags
  were still asked "a biit more visible... not a lot just a bit" (+20%).
- Labels on light or coloured backgrounds go dark and big ("bigger and darker" for light grey labels on pink, "hard to
  read on a phone").
- Before delivering any title, caption or card, mock it on GRADED frames from every location it will sit over (a
  bright sky, a dark sofa, a white board) with the real caption at its real place, and check contrast.

## 2. Where text goes (safe zones in numbers)
- Never over a face or mouth: a dark plate "sort of overing her mouth" and "this graphic and gradient is over her face"
  were both sent back.
- One coherent zone: everything not tied to a prop on screen lives in the lower caption zone with the same bottom
  gradient ("keep it coherent with other graphics as to not clash"). The approved ad title sits just below the caption
  line.
- Treat the editor's own placements in his latest save as the brief (he moved three titles to the top-left by hand;
  that spot then went into all eight ads).
- A borrowed 16:9 clip can sit letterboxed on a black 9:16 canvas with the hook text in the black space: no reframing,
  and it is the default look of borrowed-footage hits (23 of 71 measured TikToks were not 9:16). In the news-page
  layout, wide clips sit in a blurred box above the headline; tweet videos put the clip under the card.
- A title card wider than a portrait frame goes full width on a blurred backdrop (keep its own frame) instead of a crop
  that cuts its words.

| Where | Keep text inside | Why |
|---|---|---|
| Paid Reels and Stories ads (1080x1920) | aim clear of the top ~14% and bottom ~35% (about 270 and 670 px); never inside the top 220 px or the bottom 420 px (the smaller margin also quoted, used as the hard limit) | app header, buttons, the CTA and the caption cover them; the approved ads' low captions were never checked in an ad preview (social-video-formats platforms-and-policies.md section 3) |
| Feed (4:5) | a top-left title about 250 px from the top | the 4:5 crop and the header cut a higher title |
| News reels | headline and face between about 15% and 65% of the height | the profile grid crops 9:16 to 3:4 (240 px off top and bottom); the buttons cover the right and bottom |
| Native posts (TikTok, Reels) | x 120 to 918, y 270 to 1250; cover text inside the central 1080x1350; nothing in the bottom 20% or the right 160 px | measured against native references; grid crop |
| Music edits (band layout) | type between 10% and 76% of the height; titles in the top bar, captions in the bottom bar | the band leaves bars for type; app chrome |
| YouTube end screen (1920x1080) | keep clear: video element about x 1050 to 1810, y 300 to 730; subscribe about x 1500 to 1700, y 790 to 990 | the user adds the elements in YouTube Studio; never add them yourself |

## 3. When captions go off (caption rule 1)
- Captions on top of on-screen text "doesn't make sense" (friend's reviewer; we did the same on our own ads). Drop
  captions while a designed graphic prints the spoken words or numbers in large type (a big counter, a typed question,
  stacked words, a text beat). Keep them over the presenter, footage and document screenshots.
- When the voice reads text that is already on screen (a tweet, a letter, a headline), animate that text instead (lines
  appear as spoken, earlier lines dim, a highlight follows the words). One reference reel captioned only 31% of its
  spoken words for this reason.
- The editor is "ALL FOR IT" when graphics replace subtitles, but **disable** the covered subtitles, never delete them
  ("do not do destructive stuff do not delete captions just disable them if we want them later"). Caption tracks always
  draw above video tracks in Premiere, so a graphic on a video track sits under any caption still enabled.
- An ad whose words are all carried by graphics may have no caption track at all.

## 4. The words must be true
- On-screen text matches the words said: "WE FORMULATED" over "reformulated" was rejected.
- Use the client's exact wording for names, badges and axis labels ("Overpriced Win", "Not Worth It", a named axis that
  must never be called something else).
- Brand and product names are spelled right even when speech-to-text mishears them (a brand name heard as a common
  word): type them from the brief, not from the transcript.
- Only headlines that really ran, word for word, and only real numbers. Never the same figure twice in one frame; one
  number per frame (friend's reviewer: two numbers in a counter "looked odd").
- Do not highlight a brand's own marketing claim as if it were evidence ("dont highlight 6 mins").
- Credentials in a lower third carry risk (an AI presenter labelled with a professional title puts monetisation at risk):
  flag them, the client decides.
- A typo or placeholder in the editor's own caption track (a duplicate line, a "New Caption" placeholder) is reported,
  not silently fixed.

## 5. Subtitles and caption chunks
- **Subtitles are for speech only, never lyrics** (news and talking posts): stop subtitles before a song comes in,
  because the song is the audio and lyrics on screen add nothing and risk misquotes. Designed lyric type in a music edit
  is a different device (section 6). Star out swears (f*ck, sh*t...) on social pages.
- **Follow the speech phrases:** break at a pause over 0.3 s, at . ! ? or at a new transcript segment; split a phrase
  evenly into chunks of up to 4 words; each line ends at the next start or 0.4 s after its last word. A word-count
  chunker cut a thought in half ("TOO MUCH MAN PEACE").
- **Chunk size by look:** news-page subtitles up to 4 words per chunk; ads 2 to 4 words, about 1 s per 3 words, keyword
  in the accent colour (research); native posts 4 to 9 readable words at a time, nothing tiny (under 1.8% of frame
  height); friend's references: news reels 3 to 4 (never over 8), designed explainers a fixed 2 words locked to word
  onsets, mini-docs 1 to 3, paper-desk builds word by word to about 6 then clears.
- **Reading speed:** on-screen text at about 15 characters a second (Netflix caps 20), at least 1.5 s on screen; for data
  explainers hold = max(1.0, 0.4 + 0.33 x words) s, a headline at most 7 words, 42 characters a line, 2 lines; a hero
  number at least 150 px, held still 0.5 s after it lands.
- **Timing:** each word or phrase appears on its first spoken frame and swaps with a hard cut; a word starting within
  about 0.2 s before a cut appears on the cut (references: captions within 0.1 s of their first word, most following the
  last one with no gap).
- **Two speakers, two caption colours** (narrator white on a dark pill, guest yellow with no pill, or host questions in
  another colour) so the viewer always knows who speaks.
- Captions live on their own track or comp, never inside scene comps, so they change without touching animation.

## 6. House looks that were approved
- **Native social pages (the news pages' house look, also the reference for other clipping clients):** a bold caps
  headline with coloured numbers, a tweet card over a clip, carousels. Numbers always in the accent colour, on cards,
  video headlines and every carousel slide ("#68 in red"); 1 to 3 hook words marked as accent. Accent by story type:
  beef, court and breaking red; charts and money green; throwback and birthday orange; news yellow. A platform's logo
  tile instead of a label pill (a logo is read faster than a word). The page mark is the page's avatar + @handle, never a
  text wordmark. iPhone-style emoji only (Windows emoji look off-brand). Burned-in headlines carry at most one, at the
  end of the hook, never in a brand's closing line (the editor's own split layout is the exception: a fire and a "!!" in
  its caption box); post captions 1 to 2.
- **Rejected on native pages:** the white rounded TikTok box with black lowercase text ("TOOO off beat"; not to be
  confused with the approved split layout's white caption box in black bold caps between two photos); template chrome
  (avatar-and-handle headers, category pills, slide counters, footers, legal lines on frame); a designed card or
  dashboard in place of a moment; slide-ins, wipes and counting numbers; a pitch on screen ("Trade now", URLs, fees).
  Text reacts, it does not explain. One text treatment per page.
- **Captions with personality, but light:** fact first, a short reaction or question last ("Troll of the year?"); hype
  and heavy slang read as AI or spam ("have personality dont overdo it tho"). Urgency words only where they fit.
- **Headline grammar per story type,** borrowed from the pages that lead the niche, so captions are fast and native:
  "ARTIST & ARTIST - Title" for collaborations; "TITLE OUT NOW" plus a siren emoji for releases; "N years ago today ...
  Favourite track?" for anniversaries; one CAPS keyword, one emoji and asterisk-censored swears on beef pages; a neutral,
  sourced line for stats; many leaders always end on a question. Lead with names, 6 to 14 words, facts only. Detail and
  the leaders' patterns: social-video-formats.
- **Premium ads:** name title in bold condensed type plus a small brand-gold pill, below the caption line, animated (a
  dark glass plate at chest height was "so off putting"); a sports-broadcast strap was liked; dynamic emphasis captions
  on B-roll (small kicker over one huge word, a red word for the negative) were loved; stacked synced words "perfect";
  accents white, red for negatives, green for ticks; code card dark, rising, starting on the word "code". Build recipes:
  motion-design.
- **"Premium calm" explainers:** semibold humanist type (Proxima Nova Semibold class), slightly smaller, wider tracking
  on caps, thin accent bars, sentence-case sub lines, dark ink on light cards, one verdict stamp at most, little text
  ("too much text man try to show"); never heavy poster type ("too poster ish").
- **Music edits:** one type family plus one accent colour per edit; designed, textured type (depth copy, grain, sheen),
  a big word plus a small caption; never spaced out over the face, never bland; text only where it means something (no
  literal word on an object: "this gift one is there for no reason at all"); titles in the top bar, lyric words in the
  bottom bar on the sung syllables; avoid default caption templates (Montserrat + yellow keyword + emoji). Recipes:
  motion-design.
- **Platform UI:** never show Instagram's or another platform's real UI in an ad without permission; design your own
  question or comment card. Tweet cards only for our own accounts.

## 7. Fonts and their traps
- A condensed headline face was hard to read on a phone on video (a 5-font test settled it): use a readable heavy sans
  for video headlines, condensed faces for cards.
- The friend's reviewer set SF Pro Display as his caption font; that is his taste, not ours, and Apple's licence looks
  written for Apple-platform interface work: prefer Inter (open licence) when that look is wanted.
- Numbers need lining figures (some serifs set old-style figures that After Effects scripts cannot switch).
- Missing glyphs render blank with no error; Premiere only sees fonts installed before it launched; variable fonts may
  need Adobe's instance names. Mechanics and checks: premiere-ae-editing.
- Fonts are licences: the boss needs his own copies of commercial faces (Proxima Nova and others), and Adobe Fonts give
  no file path for scripts. For browser-made mock frames, mock an Adobe Fonts face with its Google Fonts version and say
  so.

## 8. Names on files and on screen
- Client-visible names (exports, delivered sequences, shared folders, comps a client opens) carry the job and the
  version only. Never put "Claude" in a name a client sees (renders, sequences, delivered files, client-visible
  projects); internal tools and work files may use it.
- Name renders after the job and version, the way the user names his own (job name + v3), never by guesswork about
  which file is which.
