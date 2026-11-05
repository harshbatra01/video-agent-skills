# Sound and voice

Claude cannot hear. The user judges all of this by ear. Numbers are from the Elon and Anthropic jobs.

## Order
Settle voice and music on the real read before the picture is built. On Elon, a stand-in stayed until v13 and the voice changed at v14, so the timing moved late.
On Anthropic, the user rejected all our music candidates and chose to send a track. Ask early.

## Voice
- The pick includes an energy test on the real script. On Elon, the user kept the original read after 5 livelier tests.
- Check the transcript against the script on every number.
- Word timings are valid only for that take.
- Fix gaps only in measured silence. Trusting word timings for cuts clipped "congratulations".
- Pace decides length: our 292 words ran 159 words a minute against the references' 180 to 210.

## Music
- Make music-only samples too. The user could not judge tracks under the voice.
- Music started 0.5 s in on Elon, the user's note.
- For a new track, find the tempo and beat map first (`reference-study/scripts/beat_map.py`).
- In the voice gaps, the references sit 2.5 to 4.7 dB under the voice. 10 dB under was too quiet.

## Sound effects, the user's rules
- A sound must feel caused by what is on screen. Pin each to a frame, on the exact word or frame change.
- Only at real shifts. Never on a timer, and never the same sound back to back.
- One gavel strike, not three. Flashes stop when the sound stops.
- Budget the first 5 s. Elon had 28 of its 51 cues there, which the user blames for the flop.
- Clusters and long quiet stretches, not even spacing. We cut 35 cues to 13.
- A real-world sound of the action beats a generic whoosh.

## Finish
Our delivered mix: -14.5 LUFS, peak -1.5 dBFS. Measure both. Passing numbers do not mean it sounds right.
