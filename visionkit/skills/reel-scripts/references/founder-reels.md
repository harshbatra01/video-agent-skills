# Founder and expert reels in the person's own voice

The offer this method came from (October 2026): reach busy tech founders and investors, learn how they talk and write,
script reels in their voice, and make the videos with AI (an avatar or a cloned voice, only with their consent). The
first scripts were for a finance creator (three reels, written for his 215 wpm desk-video pace) and a newsletter writer
(three reels at 200 wpm).

## Reference accounts and what they share
Five public accounts were studied: @wadhwanisubah (VC and startup news told through one person or one fight, the
presenter possibly an AI avatar), @drbenmiles (science news, 106 to 148 s, 2D animation, a pun and "follow for more"),
@damileearch (architecture theories, split-screen 3D renders, a comment-keyword ask), @thevarunmayya (tech and AI news,
designed cards, the same story posted with 2 or 3 different hooks), @businesswithbansal (marketing case studies, mostly
on camera, ending "What are your thoughts?").

Measured on 21 of their reels: median 77.5 s (most 60 to 97), 254 words, 204 wpm; speech from 0.0 s with no greeting
and the pauses cut. About half open with "[someone] just [did X]" or a contradiction; a name or number lands in the
first 3 s; the second line is an open loop ("Let me explain", "Here's what's actually going on"). The middle hinges on a
question, explains in plain steps with numbers, and has one plain personal reaction. Endings: a question for the
comments, a comment keyword, or a callback that flips the hook. On screen: a split-screen open with the proof on top,
the creator on screen anywhere from 2 to 100% of the time (an AI-presenter account uses 2 to 3 s beats on turn lines,
about 15 to 25%), B-roll as evidence (highlighted screenshots, company footage, built visuals), burned-in captions of 1
to 6 words, music well under the voice. Frame-level specs of these looks sit in the editing playbook's reference looks.

## Learning a person's voice
- **Their writing.** Best: official exports when the person is a client, or a Substack's `/feed` RSS (the 20 newest
  posts with full free text). For X, reading in the browser where the user is already signed in, or through the
  unofficial `api.fxtwitter.com/2/profile/<handle>/statuses?cursor=` mirror without a login (one writer: 333 posts in 17
  pages, about 3 months), both work, but both can break X's terms (its scraping clause) and put the reading account at
  risk: say so, use a throwaway monitoring account only, and let the reviewer decide (research-and-sourcing
  `references/licensing-and-rights.md` section 9). Never sign in through a mirror, never type a password anywhere. Rank
  posts by views or likes against the account's own median to find what landed.
- **Their speech.** Check the person's own videos first and measure their pace (self-filmed desk monologues at 190 to
  250 wpm are ideal). If their videos are third-party clips, use podcast appearances: download the audio only and
  transcribe it with condition-on-previous-text off (the `podcast-trailers` skill's `scripts/transcribe.py` does this
  on a Mac with mlx-whisper and on Windows with faster-whisper). Download only what the user asked for.
- **What to make reels about.** Audit every channel they run (followers, posting rate, who actually posts), rank topics
  by engagement against their median (one investor's robotaxi posts got 4.3x her median likes, AI posts 1.1x, although
  AI was her most frequent topic), and look for the gap: strong ideas that only ever existed as text are the pitch.
- **A short voice profile**: sentence length, the openers they use ("To investors,"), phrases they repeat, disclaimers
  they always carry ("Not financial advice"), what they never say.

## Writing the script
- Every line traceable to the person's own posts, essays or talks; their numbers from their own letters.
- Write for their measured pace: about 215 to 270 words for 60 to 80 s at 200 to 215 wpm (a slower speaker, such as a
  cloned voice at about 172 wpm, gets about 170 to 200 words for 60 to 70 s).
- Keep their disclaimers on money scripts; no swearing unless they swear; an in-voice AI disclosure works ("And no, I
  didn't film this one either.").
- Deliver the voice-over only; list the open production questions in chat: avatar or real footage, AI labels, where it
  posts, holdings disclosures, permissions for footage.
