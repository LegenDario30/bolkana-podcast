---
version: alpha
name: Bolkana — Frame (video / frame layer)
description: >
  Video-first spec of the Bolkana brand (Brand Book v1.0, June 2025 + bolkana-design.md, April 2026).
  Graphite ground, Bone type, Lava + Grass as secondary accents and as the soft "Bolkana gradient"
  glow (≤25 % of the frame), Outfit SemiBold display + Karla body, sentence case, no shadows, solid
  rounded icons, isotype / logotype in Bone on dark. Full rules: ~/.claude/skills/bolkana-podcast-vertical-clip/references/brand.md
unit: the frame — 1080×1920 primary (shorts); 1920×1080 and 1:1 use the same atoms
principle: atoms are sacred · composition is free · the gradient is an accent, never the subject

colors:
  graphite: "#232323"     # primary ground (Pantone Neutral Black C)
  bone: "#F3F3F3"         # primary text / logo / light cards (Pantone Cool Gray 1 C)
  lava: "#D31C1F"         # secondary accent — negatives, climax, gradient (Pantone 485 C)
  grass: "#5CD41C"        # secondary accent — keywords, labels, gradient (Pantone 802 C)
  lava-soft: "#D54B4D"
  grass-soft: "#44A85A"
  surface: "#141414"
  deep: "#0D0D0D"
  muted: "#6B7C89"        # hairline borders, secondary labels
  fg2: "#999999"

radii:
  pill: "100px"
  card: "28px"            # (video) — web uses 16px at 1440w
  photo: "4px"

typography:
  display:  { fontFamily: "Outfit", weight: 600, lineHeight: 1.02, tracking: "-0.015em", color: "bone", case: "sentence" }
  caption:  { fontFamily: "Outfit", px: 84, weight: 600, color: "bone", keyword: "grass" }
  title:    { fontFamily: "Outfit", px: 88, weight: 600, color: "bone" }
  subtitle: { fontFamily: "Karla", weight: 500, px: 40, lineHeight: 1.2 }
  eyebrow:  { fontFamily: "Karla", weight: 500, px: 30, tracking: "0.02em", color: "grass" }
  body:     { fontFamily: "Karla", weight: 400, px: 34, lineHeight: 1.3 }
  fonts: "brand/fonts/*.ttf — Outfit 300/400/500/600, Karla 300/400/500/600/700 (declare with @font-face)"

logos:
  isotype: "brand/logos/isotype_bone.svg (on dark) · isotype_graphite.svg (on light)"
  logotype: "brand/logos/logotype_bone.svg · logotype_graphite.svg"
  claim: "brand/logos/logotype_claim_bone.svg — 'Smart Fundraising for Bold Founders.'"
  min-width: "100px without claim · 300px with claim"
  safe-zone: "height of the logotype 'B' on all sides"
  sponsor: "brand/logos/ibinn_logotype.png — Ibinn ('The digital way'), podcast sponsor; never recolour"

header:
  version: "v2 (client-approved 2026-10-01), visible the whole clip (vertical / social)"
  top-row: "logotype_bone.svg 236px at x327 y174 + ibinn_logotype.png 58px tall at x635 y165, in the row of IG's back arrow and camera"
  sponsor-label: "'En colaboración con' — Karla 500 26px Bone, centred over Ibinn at y131"
  youtube: "YouTube icon (Bone) + 'wearebolkana' — Karla 500 28px, centred at y≈1566 (between captions and the IG username)"
ending: "no end card (client, 2026-10-03): the clip ends on its last word; the climax graphic holds to the last frame"
  why: "Full-screen Reels on iPhone 17 (19.5:9) crops ≈52–98px per side; arrow/camera cover y<240; action column x>900 (y 1000–1640); username/description y>1640"
safe-area:
  text-x: "130–950 (captions 180–900)"
  scene-top: "≥400 (top chips at 410)"

components:
  glow:
    description: "Bolkana gradient — overlapping radial Lava + Grass, blur ~100px, anchored to a corner/edge, ≤25 % of frame, slow sine drift. Never full background, never over the logo."
  card:
    backgroundColor: "rgba(20,20,20,.94)"
    border: "2px solid rgba(107,124,137,.55)"
    rounded: "{radii.card}"
    shadow: "none"
  card-light: { backgroundColor: "{colors.bone}", textColor: "{colors.graphite}", shadow: "none" }
  chip: { backgroundColor: "{colors.bone}", textColor: "{colors.graphite}", rounded: "{radii.pill}", badge: "{colors.lava}" }
  climax-slab: { backgroundColor: "{colors.lava}", textColor: "{colors.bone}", typography: "Outfit 600" }
  icons: "Iconsax Bold set (solid fills, rounded corners) — assets/bolkana brand assets/Icons, fill=currentColor"
---

## Overview
Bolkana: equity-free fundraising advisory for pre-seed → Series A founders; *The Bolkana Podcast*.
Voice: direct, operator-minded, founder-first, short sentences, specific > inspirational. Claim:
"Smart Fundraising for Bold Founders." Concept: a volcano — Graphite rock, Bone terrain, Lava energy,
Grass renewal.

## The Frame
Dark Graphite ground always. Photography is B&W in the brand book (optional crystal/glitch distortion,
young people as focal point); podcast footage may stay in colour. The Lava/Grass glow enters from a
corner as the only colour accent on stills and cards. Brand header v2 (Bolkana + 'En colaboración con' Ibinn in the IG arrow/camera row, YouTube wearebolkana above the
username). Vertical clips end on the last word: no end card, no logotype + claim outro.

## Do / Don't
- Do: Outfit for display, Karla for everything else; sentence case; hairline borders; brand icons.
- Don't: yellow / blue / purple / magenta, pure #000/#FFF, ALL CAPS display, italics, emoji, drop
  shadows on cards, circular photo crops, gradient > 25 % or as section background, gradient over the
  logo, Lava/Grass logo, stretched/recoloured logo.

## Sources
`assets/bolkana md/bolkana-design.md` · `assets/bolkana brand book/*.pdf` · `assets/bolkana brand assets/`
(logos, fonts, gradients, icons, photography, 16:9 intro video).
