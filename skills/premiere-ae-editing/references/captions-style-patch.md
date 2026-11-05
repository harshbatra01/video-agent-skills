# Styling Premiere caption tracks by patching the saved project

Premiere's scripting can create a caption track (`seq.createCaptionTrack(srtItem, 0, Sequence.CAPTION_FORMAT_SUBTITLE)`,
through the bridge, premiere-ui.md) but cannot style it. The style lives in the saved .prproj (gzip XML): every caption
`<Block>` has a `<FormattedTextData Encoding="base64" BinaryHash=...>` blob and the track has a
`<CaptionDataTemplateStyle>`. Proven in Premiere 26.5.1 on the Mac on 9-10 Oct 2026 (one reel: 104 captions placed and
styled, then 74 more in a later version). The scripts are plain Python (gzip, base64, struct), so they should run on
Windows too, but they have not been tried on a Windows project yet: test on a scratch copy first. Caption structure and
how to delete captions you made: prproj-format.md section 10.

## Workflow
1. Build the caption track (SRT imported under a NEW file name each time: Premiere keeps an old item's captions), save,
   and CLOSE the project in Premiere.
2. `python scripts/captions/style_captions.py IN.prproj --list` shows the fonts in use (new captions carry Premiere's
   default font; on the Mac it was built on that was Monaco, so check `--list` on yours).
3. `python scripts/captions/style_captions.py IN.prproj OUT.prproj --font Inter-ExtraBold --size 33 --color 255,255,255
   --no-shadow --box 5,11,20 --box-opacity 86 --pad 14 --only-font Monaco [--y-json heights.json]`.
   It writes a new file and never touches the input. Verified: its output was byte-identical to the hand patch used on
   that reel for all 130 caption blobs of the project. `--dry` reports without writing; `--offset F` sets one raw
   vertical offset for every touched caption.
4. Ask before opening the output in a Premiere that has the user's projects open, open it as a second project, and
   export frames at a few caption times to check.
5. Burn captions into an export with an .epr copy whose `ADBECaptionExportOption` is 2 (0 none, 1 sidecar .srt).

## Blob format
12-byte header (u32 length of the FlatBuffer, u32 0, u32 0x11223344) followed by a FlatBuffer.
`scripts/captions/fbtool.py` parses and rebuilds it without a schema. Content is stored once per BinaryHash and other
elements reference it with an empty element (prproj-format.md section 14), so a patched blob gets a NEW hash (12 random
bytes as 8-4-4-4-12 hex, the last 8 hex digits = `%08x` of byte length + 12) and the hash is swapped everywhere.
Duplicate caption texts share one blob, so they share a style.

## Field map (root.f0 = the style table), verified by renders
- f1 = vector of font PostScript names. Variable fonts need Adobe's instance names: Lora italic = `LoraItalic-Italic` /
  `LoraItalic-MediumItalic` (`Lora-Italic` silently falls back to another font); Inter works as `Inter-ExtraBold`.
  Premiere only sees fonts installed before it launched.
- f0 = runs; run.f0 = text, run.f1 = character style: f1 size (f32), f2 fill colour table {f0 r, f1 g, f2 b} as u8 (an
  absent channel = 255), f4 stroke colour, f5 stroke on (u8), f6 stroke width.
- Shadow: f10 colour, f11 on (u8; default 1, set 0 to remove), f12 opacity %, f14/f15/f16 distance/size/blur-like floats.
- Background box: f17 colour, f18 on (u8 1, REQUIRED), f19 opacity in percent (68.0, not 0.68), f20 padding in px.
- f33 = table; f33.f2 (f32) = vertical offset as a fraction of frame height from the default bottom slot. On 1080x1920,
  offset = (y - 959) / 1922.2 - 0.439 for a caption centred at y (-0.439 puts it at y 959, -0.259 at y 1305). Measured
  on 1080x1920 only: measure again on another frame size. f33.f4 and f33.f5 (u32, default 2/2) are alignment enums:
  leave them.
- Premiere blends the box in linear light, so it reads slightly lighter than an sRGB mock at the same opacity (the same
  reason graphics need about 97% opacity to look solid, prproj-format.md section 9).
- Still unknown: the box corner radius (boxes render square).

## Traps
- **Writing f32 values into unknown fields (f7, f8, f9, f21) crashed Premiere on project open** (uncaught exception, every
  open project went down). Only write fields whose types appear in real reference blobs.
- Read run text, sizes and the font list by schema, not by guessing: some caption strings look like valid tables and get
  misread (`fbtool.FORCE` pins those paths).
- A malformed caption blob crashes Premiere on open: validate (the script re-parses the XML) and test on a copy.
- At Lora Italic 58 in 1080x1920 the caption width limit is about 780 px; longer lines wrap, so split captions first.
- To discover a new field safely: make a scratch project with test captions named "variant 0", "variant 1"..., apply
  variants with `scripts/captions/exp_patch.py SRC.prproj DST.prproj variants.py` (see `variants_example.py`), render
  frames, compare. exp_patch.py RUNS the variants file as Python: only feed it a variants file you wrote yourself.
