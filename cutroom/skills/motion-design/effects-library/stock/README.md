# Stock for the effects library

The builders import these files by name from this folder. Nothing here is downloaded yet except the generated tile.
Downloads need the user's go-ahead first (state file, source and size). All clips: 1920x1080 ProRes 422 LT, the first
10 s of the Pexels file, native frame rate kept. Pexels licence: free, no attribution needed; keep the ids so the
source can be found again.

| file | content | fps | source | used by |
|---|---|---|---|---|
| jogger.mov | man in grey hoodie and sunglasses jogging toward camera on a lakeside path, bright hazy day | 29.97 | Pexels 4065468 | whip_pan_wipe |
| field_runner.mov | runner in purple vest on a grass field, seen from behind / side | 24 | Pexels 7187086 | luma_dissolve, gradient_depth_reveal, mixed_media_cutout |
| hood_man.mov | bearded man in black hoodie, dark background with a white light streak | 25 | Pexels 6964237 | (not used by the 18 builders) |
| wall_dancer.mov | man freestyle dancing in front of a light concrete wall (3.5 s only) | 25 | Pexels 5362374 | slow_shutter_echo_trail |
| skater.mov | skateboarder legs and board on a concrete ramp, blue sky, trees | 23.976 | Pexels 18006885 | pixel_reveal, whip_pan_wipe |
| taxi_interior.mov | taxi interior POV, driver and windscreen, city street | 23.976 | Pexels 34539090 | whip_pan_wipe |
| steering_wheel.mov | close-up of hands on a steering wheel, dark interior | 25 | Pexels 35666229 | (not used by the 18 builders) |
| clouds_a.mov | big white cumulus on blue sky (slow) | 30 | Pexels 1288012 | pixel_dither_background, shake_chroma_impact (alone) |
| clouds_b.mov | white clouds, pale blue sky | 23.976 | Pexels 5094475 | (not used by the 18 builders) |
| rain_street.mov | rainy street at night, wet asphalt with red and white light reflections | 23.976 | Pexels 12570193 | hail_mary_highlight_streak, whip_pan_wipe, shake_chroma_impact (alone) |
| blossom_photo.png | still: pink cherry blossom branch on pure white, 1920x1280 | still | Pexels photo 4366839 | (not used by the 18 builders) |
| field_runner_matte.mov | person matte for field_runner.mov (white = runner) | 24 | made from the clip | gradient_depth_reveal, mixed_media_cutout |
| wall_dancer_matte.mov | person matte for wall_dancer.mov (white = dancer) | 25 | made from the clip | slow_shutter_echo_trail |
| sfx_layering/sfx_mid_whoosh.mp3 | an air whoosh, loudest point about 0.2 s into the file | audio | any licensed whoosh | whip_pan_wipe (missing from the source list: the build stops without it) |
| sfx_layering/sfx_low_boom.mp3 | a low sub hit, loudest point about 0.233 s into the file | audio | any licensed boom | whip_pan_wipe (missing from the source list) |
| pixel_dither_tile_12px.png | 12x12 grey threshold tile (each grey = the brightness a pixel needs to turn to paper) | still | generated, included | pixel_dither_background |

## Mattes
- Mac: the source made both mattes with Apple Vision person segmentation.
- Windows: use the SAM 2 matte tooling from the music-edit kit, or any roto. Same length, frame rate and frame size
  as the clip, white = the person, black = background.

## Notes
- The SFX files are not on Pexels: use the user's licensed library and note which file was used.
- Clips that are not used by any builder can be skipped.
