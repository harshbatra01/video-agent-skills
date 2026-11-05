# Music first

- Choose the tempo so the hook's key words land on it without retiming (minidoc-01: 96 bpm; whip on beat 2, polaroid one
  beat, name on beat 3, drop on an 8th). One beat = 60/bpm s; snap every cut to a 16th.
- Sections from the voice cues with an energy level (1 drone, 2 ticks, 3 pulse, 4 full) mirroring the reference's
  energy curve (reference drops near 5, 17, 35, 51 and 63 s; soundbites with music out).
- Hits: drops (a riser that ends one 16th early, then an impact on the beat), impacts on numbers and stamps, hits on
  section starts, swells, clicks for literal objects (a lock, a switch).
- Every cut gets a sound (tick and glitch for plain cuts, whoosh and impact for flashes and whips). Check: at least +3 dB in
  the 50 ms after the cut against the 50 ms before (minidoc-01 v6: 119 of 131).
- The music's own sound: the synth score in `synth.py` is a stand-in; the user judged it "not good at all for this
  video". Licensed loops (Looperman needs the user's login; no automated downloads) or a real track at the same bpm replace
  it later without changing the plan.
- Voice pacing: tighten pauses on the waveform only (`tighten2.py`); speed up with `atempo` (pitch kept) if the read is slow.
  Cutting on word timings clipped "Ja-nuary" and "De-cember".
