# Cold opens for interview shows (with b-roll, archive and graphics)

A cold open is the 45 to 90 s trailer at the top of an episode. The outline method in SKILL.md picks the moments; this
file covers the edit itself, learned on a spec trailer for a VC and private-markets podcast (Oct 2026) and from 23 cold
opens of 12 public shows that were pulled and studied for it.

## What the best VC and business opens do
- **End on a branded stop**: a logo sting, title card or name card, usually after one to two seconds of black. The black
  lets the viewer reset, and the logo marks where the episode proper begins.
- **Let numbers hook**: on investing shows the valuation, raise, revenue, fund size or contract size goes on screen as a
  caption or a highlighted headline, so someone who has never heard of the guest still gets the stakes in ten seconds.
- **Show the real proof**: the actual tweet, article or broadcast lower third with the key phrase highlighted (yellow or
  green), instead of someone describing it. Screenshots cost almost nothing and read on a phone.
- **One caption system per show**, used every week: big words behind the speaker's head (20VC), one centred serif word
  at a time with a gold key word (a16z), mixed weights with host questions in a different colour from guest answers
  (Diary of a CEO). The system is what makes a show recognisable from one frame.
- **Two structures**: a pure quote montage (Diary of a CEO, Lenny's, a16z, Cheeky Pint), or a montage that stops partway
  for the host to say who the guest is and why it matters (20VC on camera, Logan Bartlett in voice-over). The narrated
  version suits guests the audience will not recognise by face.
- **Proportions**: tighter VC trailers spend 25 to 45 s on quotes and the last 10 to 15 s on a title sequence; one show
  switches to black and white with an italic serif for the title cards, changing cards on the music about every 2.7 s.
- Some top shows have no cold open at all; a spec open shows a client a format they lack.

## The a16z look (frame-level notes on eight opens)
Serif captions of one to three words cut on with the speech, set in the empty side of the frame or behind the guest,
blooming in over 3 to 6 frames, one metallic gold word every line or two; designed accents that last frames, not
seconds (letters stretched for two frames, light streaks, italic turning roman); outside material placed on cream or
white paper in windows with gold foil bars or highlight wipes; one archive look per open (4:3 pillarbox, or black and
white with a heavy vignette, or dimmed stage clips); 2 to 6 frame transitions between montage shots (whips, zoom blurs,
glitch tears, flash frames) while interview shots keep moving with punch-ins and slow eased push-ins; the last line
cuts to black, about two seconds of silence, then the logo fades up. Their exact caption font could not be identified
(closest: Financier Display Light or Tiempos Headline Light for the wide style, Tiempos Fine at about 90% width for the
condensed one). Our own taste rule applies to the transitions: whips and glitches only where a frame check shows no
mirrored or static frame (`motion-design` `references/effect-vocabulary-and-taste.md`; the build mechanics are in
`premiere-ae-editing` `references/transitions.md`).

## How the spec trailer was built
- **No AI voice-over** on a finance interview show: a TTS read would feel gimmicky, so on-screen type does the bridging.
- **The string-out first**: cut points from word timings on the chosen passages (snap each one to the real pause with
  `premiere-ae-editing` `scripts/media/speech_cuts.py`), a string-out preview MP4, and an FCP7 XML for Premiere written
  by `premiere-ae-editing` `scripts/prproj/fcpxml.py` with scene markers and `--check` run before hand-off (our XML
  route; see that skill's `references/prproj-recipes.md`). The sequence ends on the frame where the logo goes. The
  user's own edit of that sequence then became the base.
- **Options as sequences**: when the user asked for a real cliffhanger ending and more hooks, the answer was an
  alternate sequence (same scenes, the close moved up, a smash to black mid-sentence) plus an options sequence with four
  hooks and three endings, each with a preview.
- **The styled test** (a16z look) as a separate sequence beside the user's: their cut punched in to 119% (115% still
  showed a sliver of the sponsor bug) with a Lumetri grade, b-roll on V2 with its own grade, an After Effects overlay
  rendered as ProRes 4444 with alpha on V3 (cream paper cards for a 19th-century painting, a stock ticker, a stage
  photo, an old browser showing the company's 2003 site, type cards for the numbers, serif captions of 1 to 3 words, an
  end card), music from about 15 s in at -21 dB, whooshes and a logo boom. The user's own sequence and After Effects
  project were left untouched (the overlay comps were built in a clearly named folder and not saved over their unsaved
  work).
- **Clean cut points**: the YouTube master had digital silence between edited phrases, so RMS gave exact edges; the
  transcript's word ends ran early and clipped a word until the out point moved into the silence.
- **Facts on screen**: check every number a guest says against a source (one guest misstated a company's sale price by
  about half a billion); put only sourced figures on screen. Never hint at material the guest asked to keep out.
- **AI-generated inserts** (only when the user asks for one; our user makes AI material with their own tools, so hand
  them this recipe): lock the look in one prompt where only one element changes per shot (a door that changes while the
  framing stays straight-on and symmetrical), specify the season and the light, and say "bare hands" if gloves would be
  wrong.
