# S8 Red team: a skeptical stranger scrolls past Metro Media House

Status: done (13:21 to 13:25 IST). S6 had no scripts yet at 13:22, so script hooks were not red-teamed.

Lens: someone who has never heard of this page, thumb moving, sound maybe off. Each problem: what they think in the first 3 s, why they scroll or distrust, severity, fix.

## 1. IDEAS.md hooks and kickers, and the STUDY.md formula

### IDEAS.md
**1a. Son hook: "This might be the most expensive handshake in history, and the man on the left is about to find out if he can do it twice."** Severity: HIGH.
- First 3 s: "Two men shaking hands. Who are they? Do what twice?"
- Why they scroll: 26 words, about 9 s at 175 wpm, so the point lands after the 3 s window (the page puts 13 to 16 words in the first 5 s). Masayoshi Son's face is not known to most scrollers, and the name is held back, so nothing in frame is familiar. "The man on the left" needs the photo, which IDEAS says still "needs finding". A handshake is not "expensive"; a stranger who knows the story thinks "it was a meeting, not a handshake" (fact looks wrong).
- Fix: put a known noun in the hook (ChatGPT). See section 3.

**1b. Son kicker: "The first time, he lost his own money. This time, he borrowed it first."** Severity: HIGH.
- Rests on a claim IDEAS itself marks unchecked (the borrowing). If wrong, it is a factual accusation about a real person. "Borrowed it first" is also clunky to hear.
- Fix: a kicker that needs no new fact (section 3).

**1c. OpenAI Mafia hook: "This might be the most expensive group photo in AI, and most of the people in it don't work there anymore."** Severity: HIGH.
- First 3 s: "Which photo? Work where?" "There" points at nothing if the photo has no visible OpenAI label. The photo may not exist (IDEAS kill check 1).
- The title "worth more than it was" rests on a C-grade Dealroom total ($1.3 trillion, 65 startups). A stranger who follows AI thinks "that can't be right" (fact looks wrong).
- Also: conflict of interest (Claude is Anthropic's) and it repeats the page's own YC and PayPal Mafia shape, so a follower thinks "again?".
- Fix: drop the valuation claim; lead with "quit the company behind ChatGPT"; disclose the Anthropic link if the user picks it.

**1d. OpenAI Mafia kicker: "The PayPal Mafia built the internet you scroll. The OpenAI Mafia is building the thing that scrolls for you."** Severity: MEDIUM.
- Reuses PAL's exact phrase "the internet you scroll" (STUDY section 10 item 21 says do not copy exact lines). "The thing that scrolls for you" is unclear: an agent, a feed, a bot? A stranger never saw PAL, so the callback is lost on them.

**1e. Huang hook: "This might be the most valuable table in the world."** Severity: MEDIUM.
- Good length (10 words). But first 3 s: "a diner booth" and, for many, "I've seen the Denny's story" (IDEAS: very heavily covered). "Most valuable" is only true while Nvidia leads; check market cap on the post date.
- Fact trap for any rewrite: Huang washed dishes at a Denny's as a teen, not at the San Jose Denny's where Nvidia was planned (common reporting, recheck at source). Never say "where he used to wash dishes".

**1f. Traitorous Eight hook: "Before the PayPal Mafia, there was this photo."** Severity: HIGH.
- First 3 s: "Old black and white men in suits. What is the PayPal Mafia?" Needs knowledge, names not famous, no moving footage, Magnum rights.
- Fact looks loose: "They started Fairchild, then Intel". Only two of the eight (Noyce and Moore) co-founded Intel, with Andy Grove. Shockley calling them "traitors" is the common telling; confirm the attribution at source before the voice says he said it.
- Kicker "These eight built the thing it runs on" is fine if the line stays about chips, not "everything".

### STUDY.md formula and use/change/drop list
**1g. Name held back 8 to 17 s (item 4).** Severity: HIGH for unknown faces. Works when the face or photo is famous (Ackman meme, Solvay, YC). With Son, a stranger gets an unknown face, no name and no known noun for 8+ s. Rule fix in section 3.

**1h. Comparison slot under the no-film default (beat 2, item 14).** Severity: HIGH. The page proves "basically Tony Stark / the Wolf of Wall Street" with the film clip. Without the clip the line is a bare claim and the 4 to 8 s window loses its picture. Fix: compare to something already on the viewer's phone or a rival people know, proved with real footage or a printed object.

**1i. Beat 4 says "dated run", but 3 of 4 reels say zero dates.** Severity: MEDIUM. Dates read as "history lesson" to a stranger. Fix: at most 2 spoken dates; print the rest.

**1j. Zoom out to now sits at 75 to 90%.** Severity: MEDIUM. A stranger decides in 3 s, long before the zoom-out. Fix: tease the present-day stake inside the hook line (one known noun), pay it off at 75 to 90%.

**1k. 3x3 white-block reveal over 1 to 1.3 s.** Severity: MEDIUM. Frame 0 is mostly white blocks; in a feed it can read as a blank or loading frame, and the cover frame may be white. Fix: photo at least half visible at frame 0, sharp by 0.6 s; pick a custom cover.

**1l. Small captions on a 16:9 reel.** Severity: MEDIUM (check on a phone). Cap height 3.4 to 3.7% of a landscape frame shown inside a vertical phone screen is small; sound-off strangers lean on the big words. Fix: the 8 to 15 big words must tell the story alone; first big word by 1.5 s.

**1m. "This might be the most..." on every reel.** Severity: LOW to MEDIUM. Reads as a bait template to a stranger unless the frame proves it fast. Fix: the superlative must be checkable and a number, logo or known noun must be on screen by 2 s.

**1n. The formula is from 4 reels with no view data.** Severity: LOW. It is a hypothesis (STUDY says so). Do not let the rule book lock it as law beyond the measured ranges.

## 2. Sprint files as of 13:22 IST
**S6-scripts.md** had only its header and picks (Son, Huang, Traitorous Eight; OpenAI Mafia skipped for the conflict flag). No hooks or kickers to test yet.
- **2a. Traitorous Eight as script 3.** Severity: HIGH. It fails S5's own idea rules: "a name a stranger half-knows" (IDEAS who score 5) and "list 3+ real clips" (IDEAS: footage thin, mostly stills, Magnum photo). Fix: only keep it if moving archive of Noyce or Moore is found; otherwise drop it and ship two scripts.
- **2b. Huang.** Severity: MEDIUM. Feed fatigue (IDEAS: very heavily covered). Fix: the booth is the photo, but the hook must carry the twist (dishwasher, 30 days) inside 3 s.
- **2c. Son.** Severity: HIGH. The handshake photo is not found. Fix: hook on footage that exists (Son on stage with Altman, per IDEAS) and say ChatGPT in the hook.

**S5-rule-book.md** (sections 1 and 2 only):
- **2d. "Do not say the person's name in the first 3 s; hold it to 8 to 17 s."** Severity: HIGH. Needs a condition: only when a known noun or famous photo is in the first 3 s (see 1g).
- **2e. Hook "This is / This might be [one of] the most [X]".** Severity: MEDIUM. "Might be one of the most" stacks two hedges; a stranger hears bait. The rule has no word cap. All 4 hooks are 10 to 11 words (PAL 11, ACK 11, EIN 11, YC 10, counted from STUDY section 7). IDEAS hooks run 26 (Son) and 21 (OpenAI Mafia).
- **2f. Idea rules are good** ("stranger half-knows", "3+ real clips"). Add: the hook claim must be A or B grade.

## 3. Fixed versions (all numbers still need the source check IDEAS asks for)

### Hooks
- **Son:** "This man once lost about 70 billion dollars. Now he's betting billions on ChatGPT." (14 words; $70 billion is B grade; picture: Son on stage, ChatGPT logo as big word.) Page-shape option: "This might be the most expensive bet in tech, and it's on ChatGPT." Use only if the OpenAI figure is confirmed in SoftBank filings.
- **Huang:** "A former Denny's dishwasher planned Nvidia in this Denny's booth." (10 words; "former" matters, he did not wash dishes at that Denny's.) Beat 3 paradox: "And he still runs it like it's 30 days from going broke."
- **Traitorous Eight (only if footage is found):** "These eight men quit their boss in 1957. Two of them started Intel." (13 words; Noyce and Moore co-founded Intel in 1968.)
- **OpenAI Mafia (only if the user accepts the conflict, with disclosure):** "These people all quit the company that made ChatGPT. Now they run its rivals." Check every face in the photo first.

### Kickers (no new facts allowed in a kicker)
- **Son:** "The first time, he was right too early. This time, he can't afford to be."
- **Huang:** "He built Nvidia scared of running out of money. It made more than anyone. He's still scared." Cut to the plaque. (Check "more than anyone" against the latest results, or drop that sentence.)
- **Traitorous Eight:** "Their boss won the Nobel Prize. They won the industry." (Keep "industry" about chips.)
- **OpenAI Mafia:** "They left OpenAI to slow it down. Now they're racing it." (Fits the Anthropic founders only; check the stated reason they left.)

### Rule changes for S5
1. Hook sentence 10 to 11 words, hard cap 14. First 5 s stays 13 to 16 words.
2. Hold the name to 8 to 17 s only if a known noun (ChatGPT, Nvidia, Intel, PayPal) or a famous photo is in the first 3 s. Otherwise put the known noun in the hook.
3. No C-grade number in the first 5 s or in the kicker. The hook's superlative must be checkable.
4. A kicker may not add a fact the body did not show.
5. Comparison slot without film: a rival group, a known person or a product, proved with real footage, a logo burst or a printed card. If nothing fits, skip it and name earlier (EIN names at 3.7 s and still scored 21/24).
6. At most 2 spoken dates; print the rest.
7. Frame 0 shows at least half the hook photo, sharp by 0.6 s; set a custom cover (sharp photo plus the first big word).
8. Sound-off test: read only the big words; a stranger must get who, what and the stake.
9. "One of the most" only when "the most" would be false. Never reuse the page's exact lines ("the internet you scroll").
10. Idea needs a name a stranger half-knows (Big score who 7+) and 3+ real moving clips, or it does not reach scripting.

Main finding: the IDEAS hooks fail a stranger's 3 seconds because they are too long (26 and 21 words against the page's 10 to 11), hold back both the name and any known noun, and lean on unconfirmed photos and C-grade facts.
