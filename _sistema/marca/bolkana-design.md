# Bolkana Design System — design.md

> Last updated: April 27, 2026  
> Source of truth: `Digital.fig` + uploaded brand assets

---

## Brand

**Bolkana** is a fundraising advisory platform for startup founders at pre-seed through Series A. Their core offering is an equity-free program that helps founders raise capital while protecting their cap table and vision. They also provide fractional support in Finance, Product, and Branding — and run *The Bolkana Podcast*.

**Personality:** Direct. Operator-minded. Founder-first. Not a VC, not a bank — a partner.  
**Tone:** Short sentences. No fluff. Lowercase for attitude (*"we're here for the founder behind the pitch"*). Specific and practical over inspirational.

---

## Colors

### Base palette

| Token | Hex | Usage |
|---|---|---|
| `--color-bg` | `#1a1a1a` | Primary page background |
| `--color-bg-surface` | `#141414` | Card and form surfaces |
| `--color-bg-deep` | `#0d0d0d` | Upload areas, deepest surfaces |
| `--color-fg-primary` | `#f3f3f3` | Primary text, icons |
| `--color-fg-secondary` | `#999999` | Secondary / supporting text |
| `--color-fg-muted` | `#6b7c89` | Labels, placeholders, borders |
| `--color-fg-dark` | `#232323` | Text on light/green backgrounds |

### Brand accents

| Token | Hex | Usage |
|---|---|---|
| `--color-red` | `#d54b4d` | CTA sections ("Made for founders", "Apply") |
| `--color-green` | `#5cd41c` | Service category labels (Finance, Product…) |
| `--color-green-ticker` | `#44a85a` | Ticker strip bg · primary buttons · submit |
| `--color-border` | `#6b7c89` | Form inputs, card borders |

### Rules
- All pages use a **dark ground** (`#1a1a1a`). No light-mode variant exists.
- Red (`#d54b4d`) is reserved for full-width CTA sections only — never on components.
- Lime green (`#5cd41c`) is for category labels only — never for backgrounds.
- Green (`#44a85a`) is the **primary action color** — buttons, submit, CTAs.
- Never use gradients as section backgrounds. Gradients appear only as subtle radial glows on hero sections.

---

## Typography

### Typefaces

| Family | Role | Weights used |
|---|---|---|
| **Outfit** | Display / headlines | 300 (Light), 400 (Regular), 600 (SemiBold) |
| **Karla** | Body / UI / labels | 300 (Light), 400 (Regular), 500 (Medium), 700+ via variable |
| **Roboto Mono** | Data / annotations | 500 (Medium) — external, not bundled |

### Type scale

| Name | Font | Size | Line height | Weight | Color |
|---|---|---|---|---|---|
| Hero | Outfit | 96px | 106px | 400 | `#f3f3f3` |
| Display | Outfit | 48px | 100% | 400 | `#f3f3f3` |
| Display SM | Outfit | 32px | 100% | 400 | `#f3f3f3` |
| Section | Outfit | 24px | 100% | 400 | `#f3f3f3` |
| Body LG | Karla | 20px | 26px | 300 | `#f3f3f3` |
| Body | Karla | 16px | 20px | 400 | `#f3f3f3` |
| Body Light | Karla | 16px | 20px | 300 | `#999999` |
| Label | Karla | 16px | 19px | 500 | `#6b7c89` |
| Body SM | Karla | 14px | 20px | 300 | `#f3f3f3` |
| Ticker | Karla | 14px | 20px | 500 | `#232323` |
| Category | Karla | 16px | 20px | 400 | `#5cd41c` |

### Rules
- **Outfit** is strictly for section headings and display text. Never body copy.
- **Karla** covers everything else: navigation, body, labels, forms, captions.
- No italic in the UI. Italic variant is available but not used in the website.
- `text-wrap: pretty` on all multi-line display text.
- Minimum font size in the UI: **13px**.

---

## Spacing

Page uses a consistent spacing scale. All values in px.

| Token | Value | Key usage |
|---|---|---|
| `--space-1` | 4px | Icon gaps, micro |
| `--space-2` | 8px | Label gaps, tight stacks |
| `--space-3` | 12px | Inline gaps |
| `--space-4` | 16px | Form input padding, card gaps |
| `--space-5` | 24px | Card internal padding, item gaps |
| `--space-6` | 32px | Modal padding |
| `--space-7` | 40px | Section pad (sm) · CTA band vertical |
| `--space-8` | 48px | Hero actions gap |
| `--space-9` | 56px | **Page horizontal gutter** |
| `--space-10` | 60px | Section vertical padding (small) |
| `--space-12` | 120px | Section vertical padding (large) |

**Page width:** 1440px max. Horizontal gutter: 56px each side.  
**Team card gap:** 16px.  
**Form field gap:** 16px (grid), 8px (label-to-input).

---

## Border Radius

| Token | Value | Usage |
|---|---|---|
| `--radius-sm` | 4px | Photo cards, image containers |
| `--radius-md` | 8px | Form inputs, submit button |
| `--radius-lg` | 16px | Application form card |
| `--radius-pill` | 100px | Pill buttons |

---

## Components

### Pill Button (ghost/CTA)
- Transparent fill, `1px solid #f3f3f3` border on dark backgrounds
- On red sections: `1px solid rgba(243,243,243,0.7)`
- `border-radius: 100px`, padding: `11px 24px`
- Karla 400, 16px, `#f3f3f3`
- Hover: `opacity: 0.75`
- May include a trailing icon (SVG, 18×18)

### Primary Button
- Fill: `#44a85a` (green)
- `border-radius: 8px`, padding: `14–16px`
- Karla 500, 16px, `#f3f3f3`
- Hover: `opacity: 0.85`
- Used for: form submit, primary actions

### Ticker / Marquee Strip
- Height: 52px, full viewport width
- Background: `#44a85a`
- Text: Karla 500, 14px, `#232323`
- Content: *"we're here for the founder behind the pitch"* repeated
- Separator: Bolkana isotype mark (two curved SVG paths), `fill: #232323`
- Two variants: forward scroll and reverse scroll (used in pairs)
- Animation: CSS `translateX` loop, ~20s duration

### Form Card
- Background: `#141414`
- Border: `1px solid #6b7c89`
- `border-radius: 16px`, padding: `24–32px`
- Contains: 2-column input grid + upload field + footer row

### Form Input
- Background: `#0d0d0d`
- Border: `1px solid #6b7c89`
- `border-radius: 8px`, padding: `14–16px`
- Karla 500, 16px
- Placeholder color: `#6b7c89`
- Focus: border changes to `#f3f3f3`

### Upload Field
- Background: `#0d0d0d`
- Border: `1px dashed #6b7c89`
- `border-radius: 8px`
- Icon: upload SVG, `stroke: #6b7c89`
- Text: Karla 500, `#6b7c89`

### Team Photo Card
- Photo: square aspect ratio, `border-radius: 4px`, `overflow: hidden`
- Hover: `transform: scale(1.04)` on the image (transition 0.4s ease)
- Gradient overlay: `linear-gradient(transparent 40%, rgba(0,0,0,0.7) 100%)`
- Name: Karla 500, 18px, `#f3f3f3`
- Role: Karla 300, 14px, `#999999`
- Grid: 4 columns, 16px gap

### Service List Item
- Category label: Karla 400, 16px, `#5cd41c`
- Description: Karla 300, 14px, 20px line height, `#f3f3f3`
- Divider: `1px solid rgba(243,243,243,0.2)` below each item

### Navigation
- Fixed, `backdrop-filter: blur(8px)`, `background: rgba(26,26,26,0.85)`
- Logo: isotype + wordmark (Outfit 400, 22px)
- Links: Karla 400, 16px, opacity 0.75 default → 1 on hover
- CTA: pill button style, right-aligned

### CTA Band (red sections)
- Full-width, `background: #d54b4d`
- Padding: `40px 56px`
- Layout: headline left · body copy center · pill button right
- Headline: Outfit 400, 48px, `#f3f3f3`
- Body: Karla 300, 20px, 26px line height, `#f3f3f3`

---

## Logo & Identity

All logo files are in `assets/bolkana brand assets/Logomark/` (SVG + PNG):
`isotype/` (isotype_bone · isotype_graphite), `logotype/` (logotype_bone · logotype_graphite),
`claim/` (logotype_claim_bone · logotype_claim_graphite).
Other brand assets live alongside them in `assets/bolkana brand assets/`: `Typography/` (Outfit, Karla),
`Icons/` (Iconsax Bold set), `Gradient/` (Lava/Grass blobs), `Photography/`, `Effects/`, `Team/`,
`Video Intro/` (16:9 brand intro) and `Assets/` (favicon, LinkedIn, mail signatures).
For video, ready-to-use copies of fonts + logos are in `mi-video/brand/`.

| File | Usage |
|---|---|
| `logotype_bone.svg` | Full wordmark, on dark / red / black backgrounds |
| `logotype_graphite.svg` | Full wordmark, on light backgrounds |
| `isotype_bone.svg` | Mark only, on dark / red / black |
| `isotype_graphite.svg` | Mark only, on light backgrounds |
| `logotype_claim_bone.svg` | Wordmark + tagline, dark backgrounds |
| `logotype_claim_graphite.svg` | Wordmark + tagline, light backgrounds |

**Color rendering:**  
- On dark, red, or black: use `_bone` variant. Apply `filter: brightness(0) invert(1)` if SVG fill is unset.  
- On white or light: use `_graphite` variant. Apply `filter: brightness(0)` if SVG fill is unset.

**Clear space:** Maintain at least the height of the isotype mark as clear space on all sides.  
**Minimum size:** Isotype no smaller than 16px tall. Logotype no smaller than 20px tall.

---

## Imagery

- **Photography style:** Warm-toned, high-contrast color photos of real people. Cropped square or portrait. Never circular avatars.
- **All photos on dark ground** — no light-background photo layouts.
- **Podcast section:** Video thumbnail bleeds to right edge. Dark gradient overlay for legibility.
- **Hero section:** No photography — radial gradient glow effect only.
- **Photo cards:** 4px border radius. No drop shadow. No border.

---

## Motion & Animation

- **Ticker:** The only persistent animation. CSS `translateX` loop. Two strips (forward + reverse) used in pairs.
- **Hover states:** Opacity fade on buttons (0.15s). Scale on team photos (0.4s ease).
- **Modal:** Opacity + translateY enter transition (0.25s).
- **No page-enter animations.** No scroll-triggered animations. No parallax.

---

## Don'ts

- No light backgrounds for any section except explicit on-light logo usage.
- No gradient backgrounds on sections.
- No rounded avatars (circular crops).
- No emoji anywhere in the UI.
- No blue (`#0066ff`) — replaced by green for all button/action contexts.
- No pink/magenta (`#e8178a`) in production UI — annotation color only.
- No Roboto Mono in UI — strictly for data/annotation contexts.
- No italic type in the UI.
- No drop shadows on cards — use borders for separation.
- Never stretch or recolor the logo.
