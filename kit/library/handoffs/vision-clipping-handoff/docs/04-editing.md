<!-- Boss-kit copy of the 7 Oct 2026 handoff (history; newer research corrected some claims). The partner who ran that session is called "the partner" here. -->

# Editing

The partner edits these himself. He is relatively new to this specific style, so the knowledge below is what was gathered to close that gap.

The two published pages are richer than this doc on their own subjects:
- **Drill Edit Handbook**, https://claude.ai/artifact/GoL6m1UuDdMH7ejwNZ1eQE
- **Hoops and Hurt**, https://claude.ai/artifact/34DKGT8tqFuZtmPbUd6c97

---

## 1. The effects glossary: the real names

**This is the highest value section on this page.** Roughly half the obvious search terms are not what editors actually say, so searching them returns nothing and you conclude the technique is secret. The struck terms below are searches that fail.

| What it is | What editors actually call it | What does NOT work |
|---|---|---|
| The warped lens look | **Fisheye**, or **reverse fisheye**. Built from Premiere's **Lens Distortion** effect; older tutorials use **Spherize** | |
| Colour fringing split | **RGB split** or **chromatic aberration**, both fine. The transition form is a **chromatic flash transition** | |
| Camera punch on the beat | **Beat shake**, **bass shake**, **camera shake**, **impact effect** | ~~zoom punch~~ |
| Cutting to solid black or white on the beat | **White flash transition**, **blank video cuts**, **photo bursts**, **strobe** | ~~flash frames~~ (a film term) |
| Motion blur trails | **Slow shutter**, **Echo** (Premiere's effect is literally named Echo), **ghosting** (the Cole Bennett community name) | ~~shutter drag~~ (a stills term) |
| Warping melt effect | **Liquid effect**, **liquify**, **displacement**, **liquid explosion** | ~~trippie effect~~ |
| Compression artefact smear | **Datamosh**. Two different methods: true datamoshing strips I-frames in Avidemux, the fake version is a displacement map in After Effects | |
| Streaked pixel sort | **Pixel sort**. The tool is AE Pixel Sorter | |
| Tape degradation | **Camcorder effect** or **VHS look**. Adjacent: Super 8, 16mm, Kodak frames | ~~Hi8~~, ~~digital8~~ |
| Held frame | **Freeze frame** (Premiere's command is **Add Frame Hold**), **stutter** | ~~frame blending~~ (a render setting, different thing) |
| Speed change | **Speed ramping**. "Time remapping" is the menu name | |
| Fast pan cut | **Whip pan**, **whip transition**. The spin variant is sold as a **rotopack** | |
| Overlay footage for glow | **Light leaks**, **anamorphic flares**, **refraction** | |
| Colour work | **LUTs**, **colour grade** | ~~split toning~~ (a Lightroom term) |
| Text on the beat | **Animated lyrics**, **motion tracked lyrics**, **kinetic typography** | ~~ad-lib pop-ups~~ |

**One more he asked about specifically:** the white silhouette flash is called **"Body Flash"**. The terms he would naturally have tried (silhouette flash, roto flash, subject flash reveal) are not real community terms.

### The search-term unlock

**There is almost no tutorial content filed under "UK drill".** The entire tutorial economy for this look is built around **New York drill**. Same toolkit, roughly ten times the results. Search "new york drill music video effects", "rap music video effects premiere pro", "how to edit like jerry production" (Lil Durk's editor, the most copied in US drill), "how to edit like cole bennett".

---

## 2. Premiere Pro 26.0 AI Object Mask

Shipped **20 January 2026**. This is the biggest practical change to this kind of editing in years, and it is native.

What it does: native rotoscoping without After Effects. Text behind subject, background and sky replacement, colour isolation, outline and glow, mask wipes.

What to know going in:
- **Adobe's own guidance is that it gets you to roughly 80 percent, then you finish manually.** Do not plan a shot around it being perfect.
- Masks moved. They now sit under a new **Object Tool** and appear in the panel as **"Unassigned Masks"**. If you are looking for them where they used to be, they are not there.

---

## 3. UK drill style

The reference points the partner gave: EsDeeKid's "4 Raws", Central Cee, Digga D, and the GRM Daily / Pressplay / Link Up TV house look.

**Three findings that change the approach:**

**The fisheye is usually not a lens.** The documented working UK drill rig is a **Panasonic GH5S + Sigma 18-35mm f/1.8**, with no fisheye glass anywhere. The warp comes from Premiere's Lens Distortion effect. This is why fisheye tutorials vastly outnumber fisheye lens discussion in this scene.

**"Run and gun" is the shooting style, not the edit.** He asked about this. Drippy Visuals has a video literally titled "How I Shoot Run & Gun Drill Music Videos". Nobody calls the cut that.

**Halation is done in camera.** A **Moment Cine Bloom** filter on the lens, not a post glow. Easy to miss and hard to fake convincingly.

**One more:** the "4 Raws" original has **no official music video**. EsDeeKid's channel has eight videos and it is not one of them. The video anyone means is the **Timothée Chalamet remix**, 19 December 2025, shot by **Archie Erskine**, his house filmmaker. Erskine's annual showreels on the GlobalNotLocal channel are the single best study resource for this look.

**The crew structure worth copying:** the remix credits a **separate human being for VHS**, running a camcorder alongside the A camera. Real degraded tape layered against clean footage, not a filter. And the division is shooter/VFX plus editor/colourist (Erskine and SLIPPN), with both operating cameras. That is why the videos feel cut rather than assembled.

---

## 4. Build recipes

### Basketball, target 14 to 18 seconds, six to eight clips

| Time | Beat | What |
|---|---|---|
| 0:00 to 0:02 | Cold open | Slow push on a face or a held still. No music yet, or crowd ambience only. Subject must be recognisable in frame one |
| 0:02 | First hit | Hard cut on the downbeat into a play already in motion. Never start a clip from the dribble up |
| 0:02 to 0:08 | Three plays | One per bar. Escalate: handle, finish, something absurd. **Speed ramp into the release, real time on contact** |
| 0:08 to 0:09 | Beat switch | Black frame, white flash, or freeze on the release. Kill audio for two frames |
| 0:09 to 0:15 | Second half | Clips roughly half the length. RGB split on each make |
| 0:15 to 0:18 | The button | Biggest play last, freeze on the reaction, hold a full beat past the music. The hold is what makes people rewatch |

**The reframe rule:** basketball's main camera is a wide side court angle. One static 9:16 crop does not work, because the ball handler frequently ends up outside it. **Keyframe the position and follow the player**, two or three keyframes per clip.

**Audio:** basketball is **not** the football phonk formula. It is Travis Scott, Kanye, jersey club, Detroit and Memphis rap. The top tier runs on about seven songs: SDP Interlude, FE!N, Runaway, Highest in the Room, Murder On My Mind, Nightcrawler, Tell më. Shape never varies: 18 to 65 seconds, one player, one track.

### Fight, target 12 to 16 seconds

| Time | Beat | What |
|---|---|---|
| 0:00 to 0:03 | The line | 2 to 4 seconds of a fighter talking. **Voice starts before any visual.** Over black, or heavily graded |
| 0:03 | Hard cut | Straight into the walkout or first exchange. No transition. The absence of an effect is the effect |
| 0:03 to 0:07 | Walkout and face off | Slower clips, 1 to 1.5 seconds. Buying tension before you spend it |
| 0:07 to 0:11 | Exchanges | Shorter clips. **Slow motion on the wind up, real time on contact.** Reverse that and every punch looks weightless |
| 0:11 to 0:12 | The finish | White flash on the connecting frame, 2 to 3 frames only. Then hold the drop a full beat |
| 0:12 to 0:16 | Aftermath | Freeze on the reaction. Cut the music out a beat early and let room tone run. The silence is what people replay |

**The one rule:** aura reads as **controlled, not aggressive**. Opening on shouting fails because a shouted line has nowhere to go, since the drop is already louder. Open quiet and let the beat be the volume.

**Also:** the first three seconds is the retention window, so a cold open is 2 to 4 seconds, not longer.

### Three fight styles, do not blend them by accident
1. **The MIX.** One fighter, one track, rhythmic cutting, almost no VFX. Highest views per video. Owl Prod., One Moment.
2. **The cinematic film.** Narrative, voiceover, real grade, five minutes to over an hour. Lowest volume, highest respect. Hizzer, Mike Ciavarro, Gibson Media.
3. **The TikTok phonk edit.** Shake, zoom, chromatic aberration, 15 to 60 seconds. Where volume and trends live. **This is Vision Clipping's lane.**

---

## 5. The verified aura cold open clips

He asked specifically for a fighter or soldier saying something cold before a hard cut. These were verified for exact wording, event and date.

**Best single pick, fight:** Mike Tyson after stopping Lou Savarese, **Hampden Park, Glasgow, 24 June 2000**, to Jim Gray of Showtime. *"My style is impetuous, my defense is impregnable, and I'm just ferocious."* It starts quiet and religious then escalates hard **in one continuous take**, so you get the aura open and the drop landing from one clip. Transcript at speakola.com/sports/mike-tyson-eat-his-children-2000. This seven seconds is far less used than the famous line from the same rant.

**Peak aura but completely spent:** Khabib, **6 April 2018**, Brooklyn. *"You want to talk to me? Send me location."* Flat, controlled, the archetype. It also has its own Know Your Meme entry and four TikTok discovery pages.

**Best no-words option:** **Tyson Fury and Deontay Wilder, 15 June 2021**, LA trilogy press conference. Five minutes of unbroken eye contact, Wilder in headphones refusing to answer questions, Wilder eventually walks away. Five minutes of usable footage, zero audio rights, and nobody uses it because the Fury edit canon is all shouting.

**Best military option, real UGC register:** **Mattis, August 2017**, *"you just hold the line"*. Filmed on a soldier's phone, troops in a circle, no podium. And **Lt Col Stuart Scheller, 26 August 2021**, *"I demand accountability"*, active duty Marine on a webcam, dead flat, relieved of command the next day.

### Fabricated or misquoted, do not use

- **Tyson's "everybody has a plan until they get punched in the mouth" has no recording and is misquoted.** The original is *"Everybody has plans until they get hit for the first time"*, said to an **Associated Press** reporter on **19 August 1987** about Tyrell Biggs. It was a print quote. "Punched in the mouth" is a later corruption.
- **"Float like a butterfly"** was written by **Drew Bundini Brown**, Ali's speechwriter.
- **"Impossible is nothing"** is **Adidas advertising copy** by a copywriter named Aimee Lehto. It is all over motivational fight compilations as an Ali quote.
- **"It ain't about how hard you hit"** is Stallone in **Rocky Balboa (2006)**.
- **"Inch by inch"** is Pacino in **Any Given Sunday (1999)**, an American football film.
- **"I'm just here so I don't get fined"** is **Marshawn Lynch** at the Super Bowl, not Nick Diaz.
- **"So live your life that the fear of death can never enter your heart"**, the most used military edit cold open on the internet, is the closing voiceover of **Act of Valor (2012)**. The film stars real active duty SEALs, which is why everyone thinks it is real footage.
- **Patton:** no authentic recording exists at all. The circulating transcript is a reconstruction; the voice is the 1970 George C. Scott film.
- **Full Metal Jacket's drill instructor** is R. Lee Ermey acting. A US political campaign used it as real in 2024 and got caught.
- **Churchill's famous 1940 speeches** were never recorded live. The circulating audio is a 1949 re-recording, and one widely shared file is mislabelled with a 1940 date.
