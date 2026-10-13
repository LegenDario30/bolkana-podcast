---
name: bolkana-podcast-vertical-clip
description: Bolkana-branded vertical shorts. Turn podcast / interview / talking-head footage (horizontal 16:9 or already-vertical) plus a word-level transcript into a polished, dynamic 9:16 short (Reels / TikTok / Shorts) with HyperFrames — silence & filler cleanup, word-accurate captions, speaker-tracked reframing, stacked split-screen for listener reactions, zooms on hooks, motion-graphic B-roll with blur dissolves, title card, a royalty-free song from the Bolkana music library sitting low under the voice, QA snapshots and render. Use this whenever the user wants to edit, cut, reframe, "make viral", "make dynamic/professional", subtitle, or convert a podcast/interview/talking-head clip into a vertical short — even if they only say "edita este vídeo", "hazlo vertical", "clip corto", "añade subtítulos y música", "estilo como esta referencia", or hand over an MP4 + transcript.json. Every clip follows the Bolkana brand (Graphite/Bone/Lava/Grass, Outfit + Karla, Lava-Grass glow, header with Bolkana logo + Ibinn sponsor in the Instagram arrow/camera row and YouTube wearebolkana above the username, no end card — the clip ends on its last word) — use it for any Bolkana / The Bolkana Podcast video.
---

# Bolkana · podcast → vertical short (HyperFrames)

This skill packages a proven pipeline: a data-driven HyperFrames template whose camera engine
reframes a 16:9 (or 9:16) master onto a 1080×1920 canvas, follows whoever is speaking, stacks
two speakers in a split-screen, and punches in on hooks — all as a pure function of time, so it
is seek-safe and renders deterministically. Each project only writes an **`edit.json`** (cuts,
anchors, face tracks, camera keys, splits) and its own **scenes** (motion graphics). The build
script turns that into `index.html`.

The worked example in `references/example/` is a real 34 s clip (restyled to the Bolkana brand).
Open it whenever you are unsure how a field or a scene is meant to look. It predates the client's graphics review: some of
its scenes (`#sB`, `#sE`, `#cLes`, the flash on `#pet`) were later rejected. Check `references/scenes.md` → "client verdict"
before copying one.

## Brand: Bolkana (non-negotiable)

Every clip made with this skill is a Bolkana piece. **Read `references/brand.md` before planning
scenes.** The template already implements the brand layer:
- Graphite ground, Bone text, Grass keywords and eyebrows, Lava for negatives and the climax. These are tokens only
  (`var(--graphite)` and so on), never raw hex, and never yellow, blue or pure black/white.
- Outfit 600 for captions and display, Karla for labels and body, in sentence case with no italics. The fonts
  ship in `assets/brand/fonts` and build.py copies them, with the logos, to `<project>/brand/` on every
  build.
- **Brand header (v2, client-approved)** for the whole clip: the Bolkana logotype and the **Ibinn** sponsor logo side by side in
  the row of Instagram's back arrow and camera (y≈165–215), with "En colaboración con" above Ibinn; the YouTube icon +
  `wearebolkana` sits centred at y≈1566, between the captions and the IG username. It is built into the template — don't re-add it in scenes.css.
- **Reels safe area (iPhone 17, full screen):** the frame is cropped about 52–98 px per side, the back arrow and camera cover
  y < 240, the action column covers x > 900 between y 1000 and 1640, and the username and description cover y > 1640. Text stays in
  x 130–950, captions in x 180–900, and scene elements below y 400 (top chips at `top:410px`). See brand.md → "Safe area".
- Title with an eyebrow (isotype + "The Bolkana Podcast") and a Lava/Grass glow taking 25 % of the frame or less.
- **No end card.** The client asked (2026-10-03) for the clip to end where the speech ends: no Graphite card, no title echo, no
  logotype + claim, no extra 2 s. `tail` defaults to 0; the climax simply holds on screen until the last frame.
- **Graphics policy (client review of 10 clips, 2026-10-03/05):** few graphics, never over a face, never repeating the
  caption. The default climax is the **normal captions with the key words in Lava** (`redWords()`), not a big slab, with no
  flash and no shake. See step 3 → "Graphics policy" for the full list. It is the most-corrected thing in this skill.
- Brand icons: `{{icon:<name>}}` in `scenes.html` (about 1,000 solid, rounded Iconsax-Bold icons in
  `assets/brand/icons`). No emoji.
- `edit.json → "brand"`: `footage` `"color"` (always, unless the user explicitly asks for B&W — the brand book's B&W is only
  for a few stills) or `"bw"`, `header` true/false, `youtube` handle (default `wearebolkana`), `eyebrow` text.

A reference video only informs rhythm, transitions, camera and caption timing. It never overrides
colours, fonts or the logo. The original brand sources are in `~/Bolkana/Bolkana Podcast/_sistema/marca/`
(`bolkana-design.md`, `frame.md`, `brand-book/`, `brand-assets/`) (including the 16:9 brand intro
`Video Intro/New intro bolkana high resolution.mp4`, 8.5 s, which suits horizontal pieces only — never
append it or any outro to a vertical clip).

## Before you start

- Load `/hyperframes` first (it routes to `/general-video`, `/hyperframes-core`, `/media-use`,
  `/hyperframes-audio`); this skill is the recipe, those own the framework rules. Follow the
  project's CLAUDE.md (e.g. run `npm run check` after every edit).
- Tools: ffmpeg/ffprobe, `whisper-cli` + a ggml model (HyperFrames ships them; `scripts/_env.sh`
  finds `tools/` or `_sistema/tools/` in any parent folder, `~/.cache/hyperframes/whisper/models`;
  override with `FFMPEG_DIR`, `WHISPER_CLI`, `WHISPER_MODEL`), node, python3 (stdlib only).
- **Bolkana episodes** live in `~/Bolkana/Bolkana Podcast/episodios/<NN | Invitado>/` (master in `01_fuente/`, transcript in
  `02_transcripcion/`, one project per clip in `03_clips/clip_NN_<slug>/`, renders in `04_renders/`). Start a new clip with
  `cp -R 03_clips/_base 03_clips/clip_NN_<slug>` (it already has the `assets` → `01_fuente` and `.media` symlinks and a
  `package.json` pointing at `_sistema/tools`). Follow the root `CLAUDE.md` there.
- Outside that layout, work in a **new versioned folder** (`v3/`, `v4/`…) next to the previous ones, with symlinks to
  `assets` and `.media`, a copy of `hyperframes.json`/`package.json`/`meta.json` (new id), and a
  `clip/` build dir. Never overwrite an earlier version; name the render the way the user asked
  (`renders/v4.mp4`).
- **Revision rounds on delivered clips** ("para el clip 5: quita…, mueve…"): never edit the delivered project or overwrite
  its render. `cp -R` the project to `<clip>_v2`, `_v3`… (symlinks survive), give `meta.json` a new id, edit the copy and
  render into the deliverable folder with the same file name (Bolkana: `04_renders/final/#NN | clip_NN_<slug>.mp4` of the episode).
  If that file already exists, move the old one to a `_prev/` folder first. Report point by point, in the user's numbering.
- Respect media constraints the user states (e.g. "don't use music_bed.mp3"). If the transcript
  file the user mentioned is missing, ask — don't invent one.

`SK=~/.claude/skills/bolkana-podcast-vertical-clip/scripts`

## 1 · Analyse the footage

```bash
bash $SK/analyze.sh assets/<video>.mp4 clip/analysis
```
Gives camera cuts (source seconds), silences at −30/−26 dB, a 20 ms energy map
(`energy.txt`), a 1 fps contact sheet and a 16 kHz wav. Look at the contact sheet: which shots
exist (close A, two-shot, close B), where each person sits, where burned-in logos are (keep crops
off them).

If a reference video is given, run `bash $SK/ref.sh assets/<ref>.mp4 clip/analysis/ref` and read
the tiles + transition strips. Write down, concretely: cut rhythm, caption style/position, how
B-roll enters (blur dissolve? split reveal?), zoom behaviour, overlays. Read
`references/style-guide.md` for what to extract and the default look this template implements.

## 1b · Batches: several fragments of a long episode

When the user sends a list of clips as fragments of the full episode ("Clip N: gancho 2:03 … desarrollo … cierre …
+ por qué funciona"), the timestamps are approximate and the quotes are paraphrased or elided with "…". Work like this:
1. Transcribe the whole episode once (word-level whisper) and find each quote's exact first/last word there.
   The "…" in a quote usually means "skip what's in between" — follow it; the "por qué funciona" note tells you the angle.
2. Write `fragments.json` (generous ranges at word edges) and cut every clip from the HD master in one go:
   `python3 $SK/cut_fragments.py --master "assets/<ep>.mp4" --words <ep_words.json> --fragments fragments.json --root <batch>`
   (`--offset` if the master is a different encode than the transcribed audio). One project per clip under `<batch>/clip_NN/`.
3. Per clip: `analyze.sh` on `media/clip_NN_joined.mp4`, `align_dtw.sh`, a skeleton `edit.json` (source, srcW/H, transcript,
   dtw, silences from silencedetect −30 dB d=0.12), then the fine cut with `cutplan.py` (step 2).

## 2 · Transcript → clean cut list

The user's transcript text is authoritative; its timestamps are often off by 0.2–0.7 s. Tighten
them:

```bash
bash $SK/align_dtw.sh clip/analysis/audio16k.wav es clip/align-dtw.json
```
`build.py` matches DTW tokens to transcript words and snaps onsets out of measured silences.

Decide **segments** (kept source ranges): remove silences > ~0.25 s, retakes, fillers. Put the
cut points inside silences with ~0.06 s padding so no word is clipped. Verify every doubtful gap
by listening through whisper on the window — this is how hidden fillers ("eh…", a stray "y")
show up:
```bash
bash $SK/chunk.sh clip/analysis/audio16k.wav es 8.28 8.70 8.70 9.50
```
Short windows can hallucinate; confirm with two overlapping windows and the energy map.

Then `python3 $SK/build.py --words` (from `clip/`) lists every word with refined source/output
time — use it to pick anchor word ids and to check the cut didn't swallow a word.

**Word-edge rule (the most repeated client fix: "pitch", "tiempo", "nada", "lesiones", "Bolkana", "personal" were all
clipped).** Transcript `end` times are unreliable — a word's decay often runs 0.1–0.3 s past them. For **every** segment end,
and above all the last one:
1. Print a 10 ms energy map around the edge and cut at the energy dip *after* the word's tail (~40–55 dB), never on a plateau.
2. Whisper the window `[edge-2, edge]` alone: a changed last word ("piso" for "pitch", "Volcano" for "Bolkana") means the
   tail is cut. Then whisper `[edge, edge+0.6]` to see what follows.
3. If the next word starts with no gap ("Bolkana, ¿no?", "personal porque"), either keep the pair or cut at the tiny dip
   between them. Don't cut inside the first word.
4. If the word's tail lies past the **fragment** end (the joined media itself was cut too early), re-cut that fragment from
   the master with a later `end`, and shift every later clip-local time (segments, silences, srcKeys, tracks, transcript,
   `align-dtw.json` `t_dtw`) by the extra length. Re-cutting only the last fragment needs no shift.
5. No pause longer than ~0.3 s inside a sentence ("inglés … en paralelo" read as dead air). Cut it.

**Letting a graphic breathe.** When a word carries a graphic that needs time ("puede ser un año" + a bar filling to 12), add
real silence after it. If the speaker runs straight on, borrow a clean silent range from elsewhere in the same media as its
own segment (the facecam is defocused behind the card, so the jump is invisible). build.py handles out-of-order segments.

**Faster, verified path (`cutplan.py`).** Write `clip/keep.json` with the word-id ranges to keep
(`[["w1","w38"],["w42","w45"],…]`, dropping fillers, retakes, stutters, asides), then
`python3 $SK/cutplan.py <project>`: it places every cut at the lowest-energy point next to the edge words, shortens
pauses > 0.26 s, writes `segments`, prunes `transcript.json` to the kept words (original kept as `transcript_full.json`
— do text fixes there) and **transcribes the edited audio whole**. Read that transcript: a clipped onset shows up as a
changed word ("es" for "ves", missing "mucho", "exactamente" for "completamente"). Nudge those segment edges by hand
(use a 10 ms energy map around the point) and re-run with `verify`. Short-window `chunk.sh` checks help confirm what a
gap holds. If DTW puts a kept word's onset outside its segment (it vanishes from the captions), set its start by hand in
the transcript and add `"pinned": true` — build.py then keeps that onset.

## 3 · Plan beats (write it before building)

A table of output-time beats: what the viewer sees at each moment. Guidelines that worked:
- **Title** over the first ~2–4 s in the lower-middle (above captions), out before the first
  B-roll or split. It enters at ~0.35 s (eyebrow), with the lines at +0.1/+0.25 s, and must **not** be visible on frame 0.
  If `title.out` is early, the template pulls the entry forward, but never before 0.05 s. Plan for `title.out` ≥ 2.5 s. If the first scene
  starts before ~2 s (clip 8's card started at 1.9 s), push that scene later or the title is barely readable. The template sets its start state at 0 (`tl.set`), so check
  the 0 s snapshot whenever you touch the title code; it used to flash in full, vanish and then slide in. Write it in the brand voice: short, direct, sentence case, ≤16 chars per line, specific
  (e.g. "El ghosting de los fondos", "Inversores sin empatía").
- **Ending:** no end card. The video ends on the last word, **complete** (see the word-edge rule). The default climax is the
  captions carrying on as usual with the key words in Lava (`redWords(['cóctel','mortal'])`), plus the impact SFX and
  at most a smooth zoom. A slab is acceptable only for a short exclamation of 1–3 words ("¡Petarás!", "¡Que no coja el
  dinero!"), compact and off the face. No fade-out, no blur.
- **Every jump cut changes the framing** (scale step 10–20 % or a new composition) — otherwise it
  reads as a glitch. Camera changes in the source are also great places to hide cuts.
- **Hooks / punchlines get a smooth zoom** (0.2–0.3 s, ease-out) ; lists get stepped punches
  (one per item); the climax gets the tightest frame. **No `flash()`/`shake()` by default.** The client called the flash and
  aggressive zoom on "ayer" unnecessary and removed every climax flash; use them only if asked.
- **Split-screen** only when the listener's reaction adds meaning (nod, laugh, shock) *and* both
  are on camera at that moment. Never fake a reaction from another moment; say so if none exist.
- **B-roll / motion graphics** on the key concepts (numbers, lists, metaphors), 1.3–2.6 s each,
  facecam defocused behind (blur dissolve). Keep the caption band (y≈1390–1520) clear.
- Captions stay on screen through everything except a word a scene slams in big type (`capSkip`).

### Graphics policy (what the client removed or asked for, clip after clip)
Plan **fewer** graphics than you think: about one strong idea per 6–8 s, and plain facecam with captions is a valid beat.
- **No chip that just repeats the caption** ("Venture capital", "No conoces a nadie", "Estrés emocional", "Lesión",
  "Touch points", "Quédate con lo que sea" were all removed). A graphic must add what the caption can't: a number, a
  list that builds, a metaphor, an UI (chat), a cloud of terms.
- **No eyebrows/headers above scenes** ("Como decimos en Bolkana", "Términos que no has oído…", "El motor equivocado",
  "Aplica el filtro…", "Inversores que han emprendido", "Te impacta en" were too much). The title eyebrow is the only one.
- **One idea → one big icon.** A concept card with a heading and text ("La admiración de mi padre") became just the brand
  icon, ~400 px, centred, popping on the key word and pulsing on the next.
- **No grey/defocus screen just to re-show a list that's already on screen.** Defocus only for new content; a list that
  is building keeps going over the video.
- **Never over a face**, including during punch-ins and splits (the most frequent layout fix). Lists and chips go on the
  chest, in the caption zone, or on the side away from the gaze. In a split, they go in the lower corner of the speaker's
  panel. Snapshot every graphic at the tightest zoom of its shot.
- **Lists: small white chips, black text** (`.chip` default, `height:84px; font-size:42px` reads best), the same colour
  for all items (no dark/white mix), one per spoken item, never overlapping. 3 items stack left-aligned; 4 items make a
  2×2 grid just above the captions (tops ≈1160/1274, columns left 150/570). If the list repeats the speech
  word for word, **hide `#caps` while it's on screen**.
- **Liked, reuse it:** the jargon cloud (scenes.md → "Jargon cloud"), chips that build with a strike-through, the chat card,
  counters and bars that fill visibly (give them time), and the split with both people laughing at the end.

## 4 · Speaker tracking data

Measure face centres (source px) per shot:
```bash
bash $SK/faces.sh assets/<video>.mp4 17 18 2 960 720 240 0 clip/analysis/woman.jpg
```
(`t0 dur every cropW cropH cropX cropY out`) — read positions off the grid (the script prints the
px-per-cell). Sample every ~2 s on moving speakers, one point for static ones. Enter them as
`tracks` (`[srcTime, x, y]`), one track per person *per shot type* (e.g. `MC` man close, `MW` man
in two-shot, `WW`, `WC`).

Scale reference for a 1920×1080 source on 1080×1920: full-height needs s ≥ 1.78 (medium shot);
two-shot person ≈ 2.5–3.0; split panels (1080×960) ≈ 2.5–3.0. The engine clamps so no edge is
ever revealed. Upscales above ~3× get soft — tell the user when a shot is limited by resolution.

## 5 · Write `clip/edit.json`

Copy `references/example/edit.json` and adapt. Fields:

| field | meaning |
|---|---|
| `source`, `srcW`, `srcH`, `lang` | master video (paths relative to project root) |
| `transcript`, `dtw` | word list `[{text,start,end,id}]`, DTW json |
| `segments` | kept source ranges `[a,b]` in order |
| `silences` | measured pauses (from analyze) used to snap onsets |
| `textFixes`, `keywords`, `capSkip` | caption text fixes, Grass-highlighted words, words hidden from captions |
| `keys` / `srcKeys` | anchors: name → word id / name → source seconds (camera cuts) |
| `tracks` | face tracks per person/shot `[[srcT,x,y],…]` |
| `title` | `eyebrow` (default "The Bolkana Podcast"), `a`, `b` lines, `out` anchor |
| `brand` | `{"footage":"color"\|"bw", "header":true, "youtube":"wearebolkana", "eyebrow":"…"}` (see brand.md) |
| `tail`, `capChars` | seconds held after the last word (default 0 — keep it 0: no end card), max chars per caption group (default 13, to fit the 720 px safe caption band) |
| `camera.top` / `camera.bottom` | rows `[at, track, scale, driftScale, faceX, faceY('full'/'split'/0–1), easeDur?, 'out'/'io'?]` |
| `split` | `[at, topPanelHeight(1920 full / 960 split), transitionDur]` |
| `seam` | `[from, to]` windows showing the Lava→Grass split line |
| `music`, `sfx` | bed file + volume; sfx `{at,file,vol,dur|'rest'}` (build.py clamps every sfx to the clip end) |

Time expressions everywhere: `"anchor"`, `"anchor-0.12"`, `"seg:4"` (start of 4th kept segment =
a jump cut), `"seg:4+0.4"`, `"end"`, or seconds. Camera rows with no ease are hard reframes;
between rows scale drifts linearly (slow push). Lower-panel video copies are generated
automatically from the split windows.

## 6 · Scenes (motion graphics)

Write `clip/scenes.css`, `clip/scenes.html`, `clip/scenes.js`. The template gives you `tl`, `T`
(anchors, output s), `J` (jump cuts), `CFG`, `IR`, and helpers `IN(sel,t,{y,s,d})`,
`OUT(sel,t)`, `defocus(t0,t1)`, `scene(id,t0,t1)`, `redWords(words, inGroupWith?)` (paints caption words Lava: the
default climax), `flash(t)`, `shake(t)` (opt-in only), plus CSS classes
`.scene .card .card.light .eyebrow .h .chip .chip.dark .chip.lava .glow .ico` and the brand tokens
`--graphite --bone --lava --grass --lava-soft --grass-soft --surface --muted --fg2` (with the legacy aliases
`--ink --paper --y --red`). Before writing scenes, read `references/brand.md` and
`references/scenes.md` (patterns and the gotchas that cost time), and reuse from
`references/example/scenes.*`.

## 7 · Music & SFX

**Only the songs in `_sistema/musica/`.** Never synthesize a bed (the synthesized ones were rejected as
"de ascensor"; the old generator is parked in `scripts/_rechazado/`) and never pull music from elsewhere. Choose by analysis,
not by name — this is how the #16 beds were picked:

1. **Analysis of the library** (once; re-run when songs are added — and check new ones are instrumental with whisper):
   `$PY $SK/music_analyze.py` → `_sistema/musica/analisis.json`: tempo + pulse strength, key (major/minor), brightness,
   band balance, percussiveness and the **energy curve in 5 s blocks**. `CANCIONES.md` turns it into character, "usar para"
   and "tramos útiles". (`$PY` = `~/Bolkana/Bolkana Podcast/_sistema/tools/whisper-venv/bin/python3`, it has numpy.)
2. **Song ↔ script.** Match the clip's tone and its "por qué funciona" to the song's character (minor/dark/low → serious,
   introspective; major/warm/slow → reflection, vulnerability; bright/fast/strong pulse → energy, mindset; funk only for light
   content). Vary songs within an episode where you can; repeats are allowed.
3. **Section ↔ clip arc.** On the energy curve pick a window as long as the clip that sits inside a useful section: no near-silent
   intro, no dropout/break (e.g. chill 40–60 s), no fading tail. If the clip builds to a climax, a section whose energy rises
   toward it (Midnight Velvet 0–15 s) works; otherwise pick a stable stretch. Bright songs (the_mountain, podcast) → lower volume.
4. **Cut on the beat:**
```bash
$PY $SK/bgmcut.py <project> <song> <approx from s> <total s>   # snaps to the strongest onset ±1 s → .media/audio/bgm/bgm.mp3
```
   It snaps the start to a hit of the rhythm, fades in 0.25 s, fades out 1.5 s ending on the last word (`<total>` = video length,
   no tail) and normalizes to −16 LUFS. Then edit.json: `"music": {"file": ".media/audio/bgm/bgm.mp3", "volume": 0.22, "carve": 0.3}`.
5. Log song, snapped start and final volume in `CANCIONES.md` → "Asignaciones" (one table per episode).

SFX: soft whoosh on each B-roll entrance (vol ≈ 0.22), low impact on the climax (`dur:"rest"`).

**Subtle, never in front: about 20 dB under the voice (19–21).** Volume usually lands at 0.18–0.28 (bright songs like
the_mountain or The Choice lower). Measure:
```bash
bash $SK/mixcheck.sh <project>      # → "music sits 20.1 dB under the voice → OK"; target 19–21 dB
```
It grabs the renderer's own mix (as-is and with the music muted), so it measures what the viewer hears. About 1–2 min.

## 8 · Build → check → carve → QA → render

```bash
cd clip && python3 $SK/build.py && cd ..
npm run check                      # must pass with 0 errors
bash $SK/carve.sh .                # voice carve of the music bed (strength = music.carve, 0.3) — re-run after EVERY build
bash $SK/mixcheck.sh .             # once per clip, before the final render: music 19–21 dB under the voice
npx hyperframes snapshot --at <beat midpoints and every transition start/end> --no-end --describe false -o <scratch>/snaps .
```
Inspect the contact sheets yourself; fix and rebuild until clean — `references/qa-checklist.md`
lists what to look for (each item is a bug that actually happened). Then
`npm run render -- -o ../renders/<name>.mp4` (~8 s of render per output second), and verify the
MP4: contact sheet at 1.5 fps, a 6 fps strip over every split/transition, and whisper on 3–4
windows of the rendered audio to confirm captions line up. **Always whisper the last 3 s** and every edge you touched;
the last word must come out intact.

## 9 · Report

Tell the user, in their language: output path, brand options used (footage colour/B&W, header), duration, the beat table (what happens when),
what was cleaned (fillers found), where splits were used and why (and where they could not be),
music provenance, any resolution limits, and errors found & fixed in QA. Offer a Studio preview
(`npx hyperframes preview --background`) for manual tweaks.
