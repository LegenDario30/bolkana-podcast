# QA checklist (snapshots + render)

Snapshot at every beat midpoint **and** at the start/end of every transition, split open/close and scene entrance.

1. `npm run check` clean — and remember a lint *error* disables layout/contrast audits ("0 samples" is not a pass).
2. Nothing visible early/late: each text appears on its word, not before (see scenes.md first gotcha).
3. Title fits on its lines inside x 130–950 and does not collide with captions (title ends above y≈1330).
4. Rows/chips text inside their boxes (long Spanish phrases overflow first).
5. **No graphic over a face**, the client's most frequent fix. Snapshot every graphic at the **tightest zoom** of its shot
   and at every camera cut or punch-in while it is up (a calendar that is fine at 3.0× covers the face at 3.45×). Check
   split panels especially: the speaker's face in the top panel, the listener in the bottom one.
6. Split: lower panel never black during open/close (build.py covers the transition window; if you hand-edit, the copy must span it). The gradient seam shows only when the split is fully open.
7. Every jump cut shows a framing change or is hidden under a transition/scene.
8. Captions on the seam while split, back at the bottom otherwise, never duplicated with a slam word.
9. Climax: by default captions with the key words in Lava (`redWords`) and no flash/shake. If a slab is used (1–3 words only), it is off the face and not clipped at the sides (≤118 px for ~9 chars).
10. **Ending:** no end card and no outro blur — the last frame is the speaker on the last word with the climax graphic still
    readable (it landed ≥ 1 s before the end and does not fade out). Root duration = video end (`tail` 0); the music bed fades with it.
11. **Title vs split / captions:** in a split the captions ride the seam (y≈960) — if the title is still up it collides
    (lint `content_overlap`). Open the split when the title leaves (show the wide shot full-frame under the title).
12. **Cards over a split:** a card spanning y≈900–1030 collides with the seam captions. If the card already shows the
    spoken words (a chat, a quote), hide `#caps` while it is on screen; otherwise move the card. End `seam` windows
    before a full-screen scene so the Lava→Grass line doesn't cut through it.
13. **Face position per clip:** the same camera framing drifts between parts of an episode (Cristina's close shot ranged
    x 490–555 in 1280 px). Check a snapshot at the tightest zoom of every shot and nudge the track x (≈ offset ÷ scale).
14. **Captions vs audio:** after cutting, a removed word whose onset lands next to a kept segment shows in the captions
    ("poco", "pues"); a kept word whose DTW onset falls outside its segment disappears. `cutplan.py` prunes the
    transcript; pin (`"pinned": true`) the ones that vanish.
15. Rendered MP4: `ffprobe` duration = root duration; `blackframe` count 0; 1.5 fps contact sheet; 6 fps strips over transitions; whisper on 3–4 rendered windows matches the captions.
16. Music: carve re-applied after the last build (build.py rewrites index.html and drops it).

17. **Brand pass** (`brand.md` → Don'ts): only brand hex values on screen; Outfit/Karla actually render
    (the snapshot shows Outfit's round "a" and "g", not a fallback sans, so if it falls back check that `brand/fonts` exists
    next to index.html); sentence case; no emoji; no shadows on cards; the glow stays at 25 % of the frame or less
    and never touches the logo; logos undistorted and in their safe zone; the header v2 (Bolkana + "En colaboración con" Ibinn at the top, YouTube
    `wearebolkana` above the IG username) is visible from 0.1 s to the end and nothing overlaps it. **Reels safe area (iPhone 17 full screen):** no logo or text in the side 130 px (crop),
    above y≈240 (arrow and camera), at x > 900 between y 1000 and 1640 (action column) or below y 1640 (username and description). No scene
    element above y 400. Check a snapshot with a top chip on screen, and preview it in the iPhone mockup if in doubt.

Known lint warnings you can accept: `composition_file_too_large`, `audio_carve_ungrouped_sources` (carve.sh lists the voice clips directly). `duplicate_media_discovery_risk` should not appear (build.py splits the colliding top clip); if it does, check hand edits.

### From the client review of 10 clips (2026-10-03/05): each one was asked for at least twice
18. **Word edges by ear**: whisper `[edge-2, edge]` for every segment end and the clip's last 3 s. A changed last word
    ("piso"/"pitch", "Volcano"/"Bolkana", a missing "-l" in "personal") means the tail is clipped. The energy map must
    show the cut on the dip after the word, not on its plateau.
19. **No dead air**: no pause longer than ~0.3 s inside a sentence (listen to every kept segment boundary).
20. **No caption duplicates**: no chip or card that only repeats the words being said; no eyebrow/header over a scene;
    lists that echo the speech hide `#caps` while on screen.
21. **Lists**: all chips the same colour (white/black by default), none overlapping each other or the captions, each
    entering on its own word (CSS `opacity:0` on every item so none shows early).
22. **Readable data**: bars, counters and gauges reach their final value and hold it for at least about 0.6 s before the
    scene leaves. Needles move like needles (rotation about the pivot).
23. **Seam and cards**: the Lava→Grass split line never crosses a card or the defocus.
24. **Revision round**: work in a new `_vN` project copy, render to the deliverable folder, never overwrite without
    moving the old file to `_prev/`, and report each requested point by its number.
25. **Frame 0**: snapshot at 0 s and 0.05 s. Nothing that animates in later (title lines, eyebrow, glow, chips) may be
    visible yet. A `fromTo(...,{...IR})` doesn't apply its from-state before it starts, so add a `tl.set` at 0 or CSS `opacity:0`.
26. **Music subtle, in the background**: a song from `_sistema/musica/` (never synthesized), and `bash "$SK"/mixcheck.sh <project>`
    reports the bed 19–21 dB under the voice (−16 LUFS excerpt, volume ≈ 0.18–0.28, carve 0.3). Fade in 0.25 s, fade out 1.5 s
    ending on the last word.

