# Design System: Outcome

**Project ID:** N/A (Outcome brand guidelines, not a Stitch project)

## 1. Visual Theme & Atmosphere

Outcome is a **reliable-rebel prediction markets protocol**, and the visual system mirrors that duality. The atmosphere is **loud, high-conviction, and cinematic**, built to shout one idea per frame at the biggest size the canvas can carry. Outcome layouts feel less like a software product and more like a **poster, a billboard, or a protest flyer**, rendered with the discipline of an institutional brand.

The overall mood is **declarative, quietly forceful, and anti-corporate**. Outcome sounds like someone who already knows the answer and is not trying to convince you, and the visuals carry the same posture. Imagery is a **stylized oil painting**, every photo passing through a single painterly treatment so a feed of unrelated subjects still reads as one brand. Photographs are not scenes viewed through a window, they are atmosphere, a backdrop the headline sits on top of.

**Key Characteristics:**

- One dominant idea per frame, rendered in uppercase Narrow Ultrabold type at display scale
- Compositions snap to a nine-region placement grid, never free-positioned, never center-stacked
- Layouts read from across a room, no gentle hierarchy, no soft wrapping
- Oil-painted imagery used as canvas or cutout, never as a decorative subject inside a frame
- Textured backgrounds (canvas weave, spray paint, halftone dots) map one-to-one with three brand sub-groups
- Nine-palette, eleven-step color system with ten swappable themes, any theme on any graphic
- Confident, earned, never performed. Rebellious energy without casino or gambling visual language

## 2. Color Palette & Roles

Outcome runs on nine palettes, each with eleven steps from 50 (almost white) to 950 (near black). Ten themes compose those steps into background, secondary, and text slots, and any theme can be applied to any graphic. Three brand sub-groups (Main, Culture, Business) bind specific themes to specific textures.

### Main Group (default, canvas texture)

Used for protocol-level communication, product surfaces, and the hero brand. Pairs with canvas-weave textures.

- **Signal Green 500** (#1AFF57) and **Deep Forest 900** (#055D1C) - the dominant Outcome green, a saturated, high-voltage lime that reads as "go, act now." The 500 step is the hero accent, the 900 step is the anchoring dark shell.
- **Violet Ultra 400** (#8952EE) and **Twilight Indigo 900** (#240F4C) - the quieter sibling to green, a hyper-saturated electric violet used when green would read too familiar. Same role, different temperature.
- **Near-Black Neutral 900** (#171717) and **Off-White Neutral 100** (#F5F5F5) - the neutral-dark and neutral-light themes, used for deadpan, editorial, or utility surfaces where color would distract from the line.

### Culture Group (spray texture)

Used for community, social, campaign, and subcultural moments. Pairs with hand-sprayed paint-burst textures.

- **High-Vis Yellow 400** (#E6FF2F) - warning-sign yellow, the loudest color in the system, reserved for statements that need to be impossible to ignore.
- **Rally Orange 500** (#FF8825) - saturated traffic-cone orange, used when energy should feel kinetic and physical rather than digital.
- **Protest Pink 200** (#FF9DBE) - a soft, cotton-candy pink used as a quieter Culture accent, subversive rather than playful.

### Business Group (halftone texture)

Used for institutional, macro-finance, and partnership moments. Pairs with printed-dot halftone textures.

- **Executive Teal 700** (#04AC7D) - a deep, confident teal that reads as institutional without feeling corporate.
- **Protocol Blue 700** (#03379D) - a dense, trader-terminal blue, used when the context is macro, fixed-income, or analytical.
- **Alert Red 300** (#FD6C6B) - a punchy, non-emergency red. Strong enough to demand attention, warm enough to not trigger casino associations.

### Functional Colors

Outcome avoids baking in global semantic tokens (success/error) at the brand level because a theme swap can repaint everything. When a surface needs clear feedback, the closest palette match to the theme is used: a **Signal Green** derivative for positive states, **Alert Red 400** (#FC403E) for critical states, **Alert Orange 600** (#F37003) for warnings, **Protocol Blue 500** (#0053FB) for informational callouts.

### Canonical Theme Mappings (for reference)

Each theme binds palette steps to three roles: background, secondary, and text. The ten themes are interchangeable, and any theme can be applied to any graphic.

- **Green** theme: bg green-500, secondary green-600, text green-900
- **Orange** theme: bg orange-500, secondary orange-600, text orange-950
- **Teal** theme: bg teal-700, secondary teal-800, text teal-950
- **Blue** theme: bg blue-700, secondary blue-800, text blue-200
- **Purple** theme: bg purple-400, secondary purple-600, text purple-100
- **Yellow** theme: bg yellow-400, secondary yellow-600, text yellow-900
- **Pink** theme: bg pink-200, secondary pink-300, text pink-800
- **Red** theme: bg red-300, secondary red-400, text red-800
- **Dark Gray** theme: bg neutral-900, secondary neutral-800, text neutral-100
- **Light Gray** theme: bg neutral-100, secondary neutral-200, text neutral-900

## 3. Typography Rules

**Primary Font Family:** PP Neue Corp, used in exactly two weights.
**Character:** A condensed display grotesque with an ultrabold narrow face that reads as half type, half signage. No serifs, no rounded corners, no humanism. The face is architectural, mechanical, and load-bearing.

### Hierarchy & Weights

- **Headline:** PP Neue Corp Narrow Ultrabold, **uppercase always**, tight line-height, display size from 48px up to 120px or more, capable of filling roughly half the canvas at base scale (240pt design unit). Headlines crop against canvas edges on purpose, they are the reason the graphic exists.
- **Subhead:** PP Neue Corp Narrow Ultrabold, sentence case, 20px to 80px, used sparingly as a caption to the headline, never as a peer. When present, it reads quieter and smaller.
- **Body:** PP Neue Corp Normal Medium, sentence case, 14px to 44px, a short supporting line pinned to a corner opposite the headline. Information, not decoration, never more than a sentence or two.
- **Caption & Footer:** PP Neue Corp Normal Medium, 10px to 28px, reserved for metadata, handles, dates, small print.

### Spacing Principles

- Headlines use tight line-height so the uppercase block reads as a single mass
- Body copy has relaxed line-height for legibility at small sizes
- No mixing of two large type sizes in the same frame, one hierarchy, one winner
- Type can tuck behind cutouts or break along subject edges, as long as the first word stays legible
- Never add drop shadows, outlines, or tints to make type legible. Recompose the layout or swap the theme instead.

## 4. Component Stylings

Outcome is primarily a **graphic and campaign system** rather than a classic UI component library. The Brand Shrine app that hosts it uses Phosphor Icons, short radii, and a deliberately restrained component set that stays out of the way. What follows describes both the graphic layer language and the app component treatment.

### Buttons

- **Shape:** Subtly rounded corners, short radius. Never pill-shaped, never square-sharp.
- **Primary CTA:** Theme background color with theme text color, no gradients, no glows. The button takes its entire color scheme from whichever theme is active, so the same component swatches differently on a Green surface vs a Pink one.
- **Hover State:** Step one level darker in the palette (for example, green-500 to green-600 on the background). Instant, no fade.
- **Typography:** PP Neue Corp Narrow Ultrabold for emphasis labels, PP Neue Corp Normal Medium for utility buttons
- **Never:** Drop shadows, multi-stop gradients, emoji, casino-style framing

### Cards & Containers

- **Corner Style:** Short, disciplined radius, same family as the buttons.
- **Background:** A flat theme color, or the theme color with a matching brand texture on top. Photographs never sit behind cards, only inside them.
- **Shadow Strategy:** Flat by default. Any depth comes from color contrast, not elevation.
- **Border:** Optional hairline in the theme secondary step, used only when contrast against the surface is low.
- **Padding:** Generous, so type can sit at full display weight without crowding edges.

### Inputs & Forms

- **Stroke Style:** Single-pixel border in the theme secondary color.
- **Background:** Theme background, unchanged on focus. Focus is communicated by a border color shift to the theme text color.
- **Corner Style:** Matches buttons and cards.
- **Typography:** PP Neue Corp Normal Medium, placeholder at reduced opacity.
- **Error State:** Border and helper text swap to Alert Red 400 (#FC403E), no icon flourishes.

### Iconography

- **System:** Phosphor Icons, one weight per surface (Regular is default).
- **Sizing:** Icons size to the type they sit next to, not an arbitrary pixel value.
- **Usage:** In-product via the React package, in Figma via the official Phosphor plugin. Never mix weights within a surface.

### Imagery (Graphic Component)

- **Treatment:** Every photograph passes through the in-app oil-painting stylization pipeline. No stock photography, no external AI filters.
- **Full Image:** The stylized oil-painted photo sits as a full-bleed background. Use when the subject is the point.
- **Cutout:** The stylized subject is isolated on a flat theme color or textured canvas. Always crop the cutout against one or two canvas edges, never float with air on all four sides.
- **Never:** Place stylized imagery on a photographic background, darken or lighten to force contrast, run through external filters.

### Texture Layer

Textures are load-bearing, not decorative. They identify the brand sub-group in a single glance.

- **Main group:** Canvas-weave texture (painterly fabric, ties back to the oil-painting treatment)
- **Culture group:** Hand-sprayed paint-burst texture (loose, expressive)
- **Business group:** Printed halftone-dot texture (clean, editorial)

Texture family and theme group are bound one-to-one. A Culture theme (orange, yellow, pink) pairs with spray. A Business theme (teal, blue, red) pairs with halftone. A Main theme (green, purple, neutrals) pairs with canvas.

## 5. Layout Principles

Outcome layouts are **loud on purpose**. One dominant idea per frame. If a viewer can read the headline from across a room, the layout is working.

### Canvas Presets

Every deliverable starts from a platform preset. Sizes are fixed, not suggestions.

- **Instagram Post, LinkedIn Post:** 1080 x 1080
- **Instagram Story, TikTok Post:** 608 x 1080
- **Instagram Landscape:** 1080 x 566
- **X Post:** 1080 x 608
- **X Header:** 1080 x 360
- **LinkedIn Article:** 1080 x 564

If a needed shape is not in this list, a new preset is added rather than stretching an existing one.

### The Placement Grid

Inside any canvas, content snaps to one of **nine regions**, never free-positioned.

- **Full:** entire canvas (single full-bleed region)
- **Four halves:** top (0,0,100,50), bottom (0,50,100,50), left (0,0,50,100), right (50,0,50,100)
- **Four quadrants:** top-left (0,0,50,50), top-right (50,0,50,50), bottom-left (0,50,50,50), bottom-right (50,50,50,50)

Combine **one image placement with one text placement** that complements it, then anchor logo and body copy to corners.

### Corner Anchoring

The logo and body copy always occupy corners opposite the headline's visual weight. This is what gives every Outcome layout the same rhythm even when content changes.

- **Logo** sits in the corner farthest from the headline's focal point. If the headline bleeds top-left, the logo sits bottom-right.
- **Body copy** mirrors the same logic. Pinned to a balancing corner, can share a side with the logo but never overlaps.
- **Corners are not soft.** Content sits on the edge grid, not floated inward with padding.
- When in doubt, draw a diagonal through the canvas. Headline on one end, logo and body on the other.

### Layer Order

Layers stack back to front in this strict order, nothing else inserts:

1. **Background** (solid theme color, or a photograph when the image is the canvas)
2. **Texture** (brand-specific halftone, spray, or canvas, enabled by default)
3. **Image** (photograph or cutout when it is a foreground element)
4. **Headline**
5. **Body**
6. **Logo**
7. **Footer**

### Whitespace & Rhythm

- Whitespace is the canvas, not padding. Large expanses of flat theme color are correct.
- Type crops against edges on purpose. Ultrabold type looks strongest when it nudges canvas boundaries.
- No center-stacked headline, subhead, and body. That is a template, not a statement.
- No rotation, no free-positioning, no mixing of two large type sizes in the same frame.

## 6. Design System Notes for Stitch Generation

When generating new screens or graphics for Outcome, reference these specific instructions.

### Language to Use

- **Atmosphere:** "Loud, declarative, cinematic poster language with institutional discipline"
- **Type:** "Uppercase PP Neue Corp Narrow Ultrabold at display scale" (not "big bold headline")
- **Imagery:** "Stylized oil-painted photograph" (not "photo" or "image")
- **Layouts:** "Snap to one of nine placement regions, full bleed or halves or quadrants" (not "center" or "grid")
- **Voice:** "Quietly forceful, earned confidence, no qualifiers" (not "fun" or "playful")

### Color References

Always use descriptive names with hex codes:

- Primary hero: "Signal Green 500 (#1AFF57) on Near-Black Neutral 900 (#171717)"
- Alternate hero: "Violet Ultra 400 (#8952EE) on Twilight Indigo 900 (#240F4C)"
- Campaign accent: "High-Vis Yellow 400 (#E6FF2F)" or "Rally Orange 500 (#FF8825)"
- Institutional: "Executive Teal 700 (#04AC7D)" or "Protocol Blue 700 (#03379D)"

### Component Prompts

- "Create a full-bleed social post on the Green theme, uppercase Narrow Ultrabold headline cropping against the top-left edge, Outcome logo anchored bottom-right, canvas-weave texture on the background."
- "Design a Culture-group campaign graphic at 1080 x 1080, Rally Orange 500 background with spray texture, stylized cutout portrait in the left quadrants, short body line pinned to the bottom-right corner."
- "Build an institutional Business-group graphic on the Protocol Blue theme, halftone texture, one sentence of quietly forceful headline copy, no imagery."

### Banned Language and Treatments

- **Banned words in copy:** bet, wager, wagering, gambling, punt, game-changing, VCs, discounts, payout percentages. Avoid "stacks" and casino-adjacent framing. Avoid hedges like "we believe", "we think", "perhaps", "maybe", "hopefully".
- **Banned treatments:** drop shadows on type or logos, gradient overlays on photography, non-Phosphor icons, stock photography, external AI filters, photographic backgrounds behind stylized images, mixing texture families across brand groupings.

### Incremental Iteration

When refining existing graphics:

1. Focus on ONE element at a time ("adjust the headline placement", "swap the theme from Orange to Yellow")
2. Be specific about the change ("move the headline from bottom-left quadrant to top-half", not "rebalance the layout")
3. Reference the nine-region placement grid, the three texture families, and the ten themes by name rather than by pixel value
