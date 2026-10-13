# Style guide — reading a reference & the default look

## What to extract from a reference video (ref.sh output)
Write each as a concrete rule you will implement, not an adjective:
- **Cut rhythm**: median shot length (the original reference: 1–3 s), how often the framing changes on the same speaker.
- **Transitions**: hard cut vs. blur dissolve (soft 0.2–0.4 s blur+fade), split reveal (B-roll slides into one half), zoom-blur punch.
- **Captions**: words per group (ref: 1–2), case, weight, size relative to frame, position (ref: centred, chest height), highlight colour, in/out animation (ref: none — hard cut).
- **B-roll**: full-screen vs. split vs. floating card/icon over the speaker; how long it stays.
- **Camera**: constant slow push-ins, step punch-ins between medium and close.
- **Branding**: persistent handle / watermark / progress bar?

## Default look implemented by the template (Bolkana: rules in `brand.md`)
A reference video tells you **rhythm, transitions, camera and caption timing**. Colours, fonts and
logo always come from the Bolkana brand, so don't copy a reference's palette or typeface.
- Canvas 1080×1920. Fonts are Outfit 600 (display, captions) and Karla 500/400 (labels, body), loaded via
  `@font-face` from `brand/fonts/` (build.py copies them into the project).
- Tokens: `--graphite #232323` (ground), `--bone #F3F3F3` (text, light cards), `--grass #5CD41C`
  (keywords, eyebrows), `--lava #D31C1F` (negatives, climax), plus `--lava-soft`, `--grass-soft`,
  `--surface`, `--muted`.
- Captions: Outfit 600 at 84 px, 1–2 words, at most 13 chars, inside x 180–900 in sentence case (as spoken), Bone, keywords in Grass, soft dark shadow. The band
  top sits at 1392 px (bottom third, above the platform UI). Captions come in hard (0.09 s rise) and go out hard. In a split they ride the
  seam (y≈960).
- Title: an eyebrow (isotype + "The Bolkana Podcast", Karla 500) and two Outfit 600 lines at 88 px, revealed
  from a mask. A Lava/Grass glow rises from the bottom-left corner. Everything leaves with a blur-up before the first B-roll.
- Brand header v2 for the whole clip: Bolkana logotype + "En colaboración con" Ibinn in the row of Instagram's back arrow and
  camera, YouTube icon + `wearebolkana` centred at y≈1566. No end card: the clip ends on its last word, with the climax graphic
  still on screen.
- Primary transition: a **blur dissolve**. The facecam goes to `blur(26px)` with a 55 % Graphite tint behind a
  card, for 0.35–0.45 s in and out. Accents: split-panel slide-up, zoom-through (scene scale 1.18→1),
  and, on the climax, the key caption words turning Lava (`redWords`). The old Bone flash + shake is opt-in only:
  the client removed it everywhere.
- Element entrance: opacity 0→1, y +36→0, scale .96→1, blur 10→0, 0.42 s power3.out. Exits take 0.28 s
  power2.in.
- Readable sizes: chips 42–46 px (84 px tall for lists), card headlines 96–130 px. Eyebrow labels (28–34 px) only in the title. Cards are dark with a
  hairline border (or `.light`), have no shadow and use 28 px radius. Chips are 100 px pills.
