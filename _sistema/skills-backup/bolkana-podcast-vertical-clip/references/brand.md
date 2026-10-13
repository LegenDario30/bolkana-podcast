# Bolkana: brand rules for vertical video

Sources: *Bolkana Brand Book v1.0* (June 2025, Bayarri & Spagnoli), *Marca-Bolkana* rebranding
proposal, and `bolkana-design.md` (the web design system, April 2026). The originals are in the
`~/Bolkana/Bolkana Podcast/_sistema/marca/` (`brand-book/`, `bolkana-design.md`, `brand-assets/`, `frame.md`).
This file turns them into rules for a 1080×1920 frame. Where the web rules don't fit video (sizes,
motion), the video rule is given and marked **(video)**.

Bolkana is a fundraising advisory for pre-seed to Series A founders. It is equity-free and puts the founder first, and it runs *The Bolkana Podcast*.
Voice: direct, operator-minded, short sentences, no fluff, specific over inspirational. Claim:
**"Smart Fundraising for Bold Founders."** Web tagline: *"we're here for the founder behind the pitch"*.

## Colours (use these hex values exactly)

| Token | Hex | Role in a clip |
|---|---|---|
| `--graphite` | `#232323` | Primary ground: tints, cards (Pantone Neutral Black C) |
| `--bone` | `#F3F3F3` | Primary text, logo, light chips/cards (Pantone Cool Gray 1 C). Never pure #FFF |
| `--lava` | `#D31C1F` | Secondary accent: climax slab, negatives, the "x" in chips, gradient (Pantone 485 C) |
| `--grass` | `#5CD41C` | Secondary accent: caption keywords, eyebrows/labels, gradient (Pantone 802 C) |
| `--lava-soft` | `#D54B4D` | Softer red: warnings, mid states |
| `--grass-soft` | `#44A85A` | Softer green: positive states, progress |
| `--surface` / `--deep` | `#141414` / `#0D0D0D` | Dark cards / deepest surfaces |
| `--muted` | `#6B7C89` | Hairline borders, secondary labels |
| `--fg2` | `#999999` | Supporting text |

- Never use pure black or white (`#000`, `#FFF`). Use Graphite and Bone.
- No other hues: no yellow, blue (`#0066ff`), purple or magenta. The old template's yellow `#FFD84D` is retired.
- The template keeps aliases so older scene code stays on-brand: `--ink`→graphite, `--paper`→bone,
  `--y`→grass, `--red`→lava.

## The Bolkana gradient (glow)

A splash of Lava with a splash of Grass, blurred so it reads as light rather than a shape. It sits on Graphite (or over B&W footage) and is
always an accent:
- Keep it to **≤ 25 % of the frame**, anchored to a corner or an edge (bottom-left on the title,
  or a corner of a key scene card). It should never be the subject.
- Never replace Lava or Grass with other colours, and never put the gradient over the logo.
- In the template use the `.glow` class (two overlapping radial gradients blurred 100 px). Use it on the title and one or two key scenes at most. Never use it as a full-section background.
- The hairline gradient `linear-gradient(90deg, var(--lava), var(--grass))` is allowed as a thin
  accent line (split seam, progress bars).

## Typography (fonts ship in `assets/brand/fonts`, wired by `@font-face` in the template)

| Role | Font | (video) size on 1080×1920 |
|---|---|---|
| Titles, captions, big numbers, slabs | **Outfit SemiBold 600** (Light 300 / Regular 400 for large quiet display) | captions 84 px · title 88 px · card headlines 96–130 px |
| Subtitles, eyebrows, labels | **Karla Medium 500** | 28–40 px |
| Body / small copy inside cards | **Karla Regular 400 / Light 300** | 30–38 px |

- Use **sentence case**, with lowercase for attitude ("we're here for the founder behind the pitch"). No
  ALL CAPS headlines and no wide letter-spacing (the old Montserrat 900 uppercase look is retired).
  A short eyebrow can stay as it is. Keep tracking at 0.02 em or less.
- No italics anywhere.
- Outfit is for display only and never for paragraphs. Karla covers everything else.
- Roboto Mono is only for data annotations, and it is not bundled, so avoid it.
- Minimum size on screen **(video)**: 26 px.
- Use `text-wrap: pretty` for multi-line display copy, or `white-space:nowrap` with shortened copy.

## Logo

Files are in `assets/brand/logos/`, and build.py copies them to `<project>/brand/logos/`.

| File | Use |
|---|---|
| `isotype_bone.svg` | The mark on its own, on Graphite, dark footage or Lava: title eyebrow |
| `logotype_bone.svg` | Wordmark with the symbol, on dark: **top-left of the header** |
| `ibinn_logotype.png` | Sponsor (Ibinn), white artwork cropped from `Logomark/Ibinn logotype/Logo_Sponsor.png`: **top-right of the header** |
| `logotype_claim_bone.svg` | Wordmark with the claim "Smart Fundraising for Bold Founders." (not used in vertical clips: no end card) |
| `*_graphite.svg` | The same set for light (Bone) grounds |

- The logo goes only on Bone or Graphite grounds (or dark footage under the template shade). Never
  use Lava or Grass as the logo colour, and never put the gradient over it.
- Never stretch, recolour, rotate or add effects (no blur-in, glow or drop shadow on the logo
  itself). Fades and small translations are fine.
- Safe zone: keep at least the height of the "B" of the logotype clear on every side. For the isotype,
  keep its own height clear.
- Minimum digital width is 100 px without the claim and 300 px with it. 
- Use the logo with its symbol. The symbol may appear alone (title eyebrow).

## Iconography

`assets/brand/icons/` holds about 1,000 solid, rounded icons (Iconsax "Bold" style, fill `#292D32`).
That style is the brand's: solid fills with rounded corners. Don't use outline icons or emoji. In `scenes.html` write
`{{icon:ghost}}`, `{{icon:money-add}}`, etc. build.py inlines the SVG with `fill=currentColor`, so
the icon takes the text colour; size it with `font-size` or `width`/`height` on `.ico`. Search
names with `ls assets/brand/icons | grep -i <word>`. Self-drawn SVG is fine for animated
diagrams (routes, radars, bars), as long as it keeps solid fills, rounded joins and the brand
colours.

## Photography and footage

- The brand book says photography is black-and-white only, optionally with a "crystal
  distortion" glitch, with young people as the focal point. The web system (2026) shows warm,
  high-contrast colour photos of real people.
- For podcast footage, the default is `brand.footage: "color"` (real speakers, natural skin). Set
  `"bw"` in `edit.json` for the editorial brand-book look: grayscale with a contrast lift, plus the
  Lava/Grass glow from a corner. That is exactly the poster and phone use case in the brand book.
- Still images used as B-roll (people, volcano, texture) should be black-and-white, with the
  glow as the only colour.
- Never crop people into circles (no round avatars). Use square or portrait crops with 4–8 px
  radius.

## Components (video versions)

- **Card**: `.card` (x 130–950) has a dark surface `rgba(20,20,20,.94)`, a 2 px hairline border in muted at 55 %
  and a 28 px radius, with **no drop shadow**. `.card.light` is Bone with Graphite text. Separate things
  with borders, not shadows.
- **Chip**: a 100 px pill radius (the brand pill button). It is Bone with Graphite text by default, and that is the
  client's preferred look for lists. Keep every item in a list the same colour, and use the compact size (84 px tall,
  42 px text). `.chip.dark` is the surface with a hairline border, and `.chip.lava` is the negative or emphasis version
  (e.g. the last item, "Ni para nada"). The `.x` badge is Lava.
- **Eyebrow / label**: `.eyebrow` is Karla 500 in Grass on dark and in muted on light, like the
  web's category labels. In video, use it **only in the title**. The client removed every eyebrow placed above a
  scene or chip list ("Como decimos en Bolkana", "Te impacta en"…).
- **Emphasis in captions (default climax)**: the caption keeps running and the key words turn Lava
  (`.cg span.red`, via `redWords()`). This replaced the big slabs ("Un cóctel mortal", "Burnout", "Arriesgando todo",
  "No te lo tomes a lo personal").
- **Climax slab** (only for a 1–3 word exclamation, e.g. "¡Petarás!"): Lava ground, Bone Outfit SemiBold text, 24–30 px
  radius, no shadow, compact (≤ 110 px text), off the face.
- **Brand header v2 (client-approved 2026-10-01; always on, from 0.1 s to the last frame)** — built into the template:
  - **Top row**, between Instagram's back arrow (x≈100–135) and camera (x≈932–985), y≈165–215 of the frame:
    `logotype_bone.svg` 236 px wide at x 327 / y 174, and the sponsor logo `ibinn_logotype.png` (Ibinn), 58 px tall, at
    x 635 / y 165, with **"En colaboración con"** (Karla 500, 26 px, Bone) centred above Ibinn at y 131.
    Never recolour, stretch or add effects to either logo.
  - **YouTube**: the YouTube icon (brand set, Bone) + `wearebolkana` (Karla 500, 28 px), centred at y≈1566 — between
    the captions and Instagram's username line.
  - Set `brand.header: false` only for non-social outputs, and `brand.youtube` to change the handle.
- **No end card** (client request, 2026-10-03): no Graphite card, title echo or logotype + claim after the last word,
  and no extra seconds. The clip ends where the speech ends; the climax graphic holds to the last frame.

## Safe area: full-screen Instagram Reels on a 19.5:9 phone (iPhone 17)

The reel fills the whole screen above the tab bar. Because the phone is taller than 9:16, Instagram scales
the 1080×1920 frame to the screen height and **crops about 52 px on each side** (about 98 px if it also runs behind the
tab bar). Measured on the frame:

| Zone (frame px) | What covers it | Rule |
|---|---|---|
| x 0–130 and x 950–1080 | side crop (52–98 px) and margin | No logo or text. Only footage or backgrounds may reach the edges. |
| y 0–≈240 | status bar, Dynamic Island, back arrow (left), camera (right) | Nothing. |
| y ≈130–225, x 327–760 | **brand header v2** (Bolkana + "En colaboración con" Ibinn), in the IG arrow/camera row | Reserved. |
| y ≈1560–1615, centred | YouTube `wearebolkana` | Reserved. |
| y < 400 | header and IG chrome | No scene elements. Top chips start at `top:410px` or lower. |
| x > ≈900, y ≈1000–1640 | IG action column (like, comment, repost, share, more, audio) | Keep text off it. Captions span x 180–900. |
| y > ≈1640 | IG username, Follow, description, audio line | No text or key content. |

Captions are therefore 1–2 words and 13 chars or fewer (`capChars` 13), inside x 180–900. Title lines are 16 chars or fewer at 88 px.

## Motion

- On the web, Bolkana motion is restrained: opacity fades, a short translateY, a slow ticker. In
  video, keep that character. Use clean `power3`/`power4` eases, short fades and mask reveals.
  Avoid bouncy or elastic effects on brand elements (logos, header).
- Energy belongs to the edit (jump-cut reframes, punch-ins, blur dissolves), not to decoration.
  `flash`/`shake` are **off by default**. The client found the white flash plus aggressive zoom too dramatic and removed
  them from every clip. Use them only on request.
- Motion should be physically plausible: a gauge needle trembles by **rotating about its pivot** (tip up/down), not by
  sliding on x. Bars and counters fill slowly enough to be read (≥ 0.5 s per step) and hold on their final value.
- The glow drifts slowly (sine, 20–60 px), which echoes the brand's intro video.

## Don'ts (checked in QA)

- No yellow, blue, purple or magenta, and no pure #000 or #FFF.
- No ALL-CAPS display type, no italics, no Montserrat.
- No emoji (build.py warns about them).
- No drop shadows on cards or chips. Only the caption text-shadow is allowed, because it keeps captions legible.
- Never use the gradient as a full background, more than about 25 % of the frame, or over the logo.
- Never stretch, recolour or put effects on the logo, and never put it on Lava or Grass.
- No circular photo crops.
- Nothing outside the Reels safe area (see "Safe area"): no text in the side 130 px, nothing above y≈240, no scene element above y≈400.
