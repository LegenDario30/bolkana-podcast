# Scene patterns & gotchas

**Brand first:** every scene follows `brand.md`. Use the template tokens (`var(--graphite)`, `--bone`,
`--lava`, `--grass`…), never raw hex. Display text uses `.h` or Outfit 600 in sentence case, labels use `.eyebrow`
(Karla), cards are `.card` / `.card.light` with no shadows, and icons are `{{icon:name}}` from the brand set.
No emoji, no ALL CAPS, no yellow. For a fake UI (mail, chat, app), draw it in Bolkana colours
rather than imitating a real product's branding.

All examples live in `example/scenes.{css,html,js}` (anchors refer to `example/edit.json`).

## Patterns: client verdict (review of 10 clips, 2026-10-03/05)
The example (`example/`) predates that review, and some of its scenes were later removed by the client. Check the verdict before reusing one.

| Pattern | Use for | Example id | Verdict |
|---|---|---|---|
| Stat card with count-up + bar + icon needle | a number the speaker says ("40 kilos") | `#sA` | ✅ keep (let the bar finish and hold) |
| Floating chips with animated strike-through | things lost/given up ("sin deporte, sin cuidarte") | `#cDep #cCui` | ✅ small, white, off the face |
| Chips docked on the speaker panel during a split | list items while the listener reacts | `#cTi #cEm` | ✅ lower corner of the panel, away from the face |
| Stacked rows card on a grey screen, last row red | the list's punchline ("ni para nada") | `#sB` | ❌ grey screen re-showing a list already on screen; finish the list as a 3rd chip instead (red) |
| Icon draw-on (stroke-dashoffset) + two-line label | a metaphor ("deporte de riesgo") | `#sC` | ⚠️ ok, no eyebrow |
| Lower-half graphic panel sliding up (face kept in top half via camera fy .25) | a process / journey (route + km counter) | `#sD` | ✅ |
| Equation card on a grey screen (A = B) | a comparison | `#sE` | ❌ removed together with its audio ("felt odd") |
| Warning chip on a word ("Lesión") | — | `#cLes` | ❌ repeats the caption |
| Draining battery stepping on each repetition | repetition / attrition ("tirar y tirar y tirar") | `#bat` | ✅ placed on the chest, never on the face |
| Big Lava slab + flash + shake, caption skipped | climax word | `#pet` | ⚠️ only for a 1–3 word exclamation, without flash. The default is `redWords()` |
| Glow-accented quote card / tagline built word by word | the thesis ("we are here for the founder behind the pitch") | — | ✅ no eyebrow above it |
| Brand icon tile (`{{icon:…}}`) | a concept with no number | — | ✅ as **one big icon** (below) |

### New patterns the client liked
**Jargon cloud** (clip 06, "términos que no has oído en tu vida", which the client called the reference to reuse). Defocus the
facecam; 6–8 terms in pills (white / dark / one Lava) scattered between y 560 and 1220 pop in one by one (`back.out`),
bob gently, then all vibrate together on the closing word. No header.
```css
.jt{position:absolute;font-family:var(--display);font-weight:600;font-size:62px;line-height:1;white-space:nowrap;padding:22px 38px 26px;border-radius:100px;background:var(--bone);color:var(--graphite);opacity:0}
.jt.d{background:rgba(20,20,20,.94);border:2px solid rgba(107,124,137,.55);color:var(--bone)}  .jt.l{background:var(--lava);color:var(--bone)}
```
```js
defocus(B0,B1); scene('#sJerga',B0,B1); tl.fromTo('#sJerga',{scale:1.12},{scale:1,duration:.5,ease:'power3.out',...IR},B0);
['#j1','#j2','#j3','#j4','#j5','#j6','#j7'].forEach((s,i)=>{
  tl.fromTo(s,{opacity:0,scale:.6,filter:'blur(8px)'},{opacity:1,scale:1,filter:'blur(0px)',duration:.32,ease:'back.out(2)',...IR},T.terminos-.1+i*.36);
  tl.fromTo(s,{y:0},{y:i%2?-12:12,duration:1.6,ease:'sine.inOut',yoyo:true,repeat:1,...IR},T.terminos+.2+i*.36);});
tl.to('#sJerga .jt',{x:i=>[-6,8,-8,6,-5,7,-7][i],duration:.06,yoyo:true,repeat:5,ease:'none'},T.closingWord);
```
**One big icon**: the whole idea as one brand icon, ~400 px, centred (top ≈600) over a defocus with the glow. It pops on
the key word (`scale .3→1, rotation -18→0, back.out(2.2)`) and pulses (`scale 1.1 yoyo`) on the next one.

**Chip list in the caption zone**: 3 items left-aligned (x≈310, tops 1215/1315/1415) or a 2×2 grid (lefts 150/570,
tops 1160/1274). Each item enters on its word with a short scale pulse. Hide `#caps` while the list repeats the speech.

**Chat card** (an investor's reply): the avatar is a Grass square with the Graphite `{{icon:user}}` sized to fill it
(no octagon/hexagon icons inside squares). Sent file bubble in Grass, "Visto", typing dots, then each received
message in its **own** Bone bubble with a visible gap (~30 px) so it reads as a real chat. Hide `#caps`, and hide the
split seam while the card is up (see gotchas).

**Red caption climax**: `redWords(['burnout','problemas','mentales','graves','físicos'])`, or for common words limited to
one group: `redWords(['un','cóctel'],'cóctel'); redWords(['mortal']);`. Keep the impact SFX on the key word.

**Ending with a shared laugh**: if the source has both people laughing right after the last line, keep about 1 s of it and
open a split (`[laughAt, 960, .3]`, both from the wide shot) while the slab rises to the seam. The client loved this touch.

Keep 1 motion-graphic idea per ~6–8 s at most; alternate full B-roll, overlays on the face, and plain facecam.

## Gotchas (each cost a rebuild)
- `tl.fromTo(..., {...IR})` (immediateRender:false) does **not** hide the element before its start time. This bit the template's own title (visible at 0 s, then sliding in), so it now does `tl.set(…,0)`. Give every element that enters later `opacity:0` in CSS (or a `tl.set` at 0). Symptoms: "EMPRENDER" visible before it is said, a panel visible during the title.
- Off-screen-parked panels (yPercent 100) need `tl.set(sel,{yPercent:100},0)` and `data-layout-allow-overflow` on the panel.
- Count-ups / progress: drive text from a tweened proxy's `onUpdate` — seek-safe.
- **Reels safe area** (brand.md → "Safe area"): text and graphics stay in x 130–950. Nothing goes above y 400 (Instagram's arrow and camera
  and the header v2 live up there), and nothing over the YouTube handle at y≈1566. Top chips start at `top:410px`. Keep the right side clear (x > 900) between y 1000 and 1640, where
  Instagram's action column sits, and keep everything clear below y 1640 (username and description). In a split, the top panel's face is at y≈440, so dock chips on the
  side away from the face (camera `fx` .30/.70) or just above the seam (top ≈ 760).
- Don't put a scene element where the face is: check the speaker's head box in the split (top panel face at y≈440, head top ≈250). Nudge the camera (`fx .66, fy .52`) rather than shrinking the graphic.
- Big text must fit the 820 px safe width (x 130–950): at 100 px, sentence-case Outfit 600 fits about 17 chars per line, and at 130 px about 13. Use
  `white-space:nowrap` and shorten the copy instead of wrapping.
- The clip ends on `CFG.vidEnd` (no end card). The climax graphic holds to the last frame: don't fade it out at `CFG.vidEnd-.3`.
  Old projects carry that fade-out line; delete it when rebuilding.
- `.chip` sits at `left:130px` by default. To right-align, set `left:auto;right:Npx`. Don't centre with
  `transform:translateX(-50%)`, because GSAP's `IN()` rewrites `transform`.
- The template turns the split seam on with a `tl.set` **at** the split time. To hide it under a card, set
  `{opacity:0}` *after* that moment (`Math.max(B0,J[n])+.01`), or the template's set wins.
- Removing a scene by regex: watch the CSS's last line (`#a,#b{opacity:0}`). Removing `#b` must not leave `#a,`
  dangling, or the CSS parse error disables every lint audit.
- A camera row that shifted the face sideways to make room for a graphic (`fx .66`) must be re-centred (`.5`) when that
  graphic is removed, with a scale step at the jump cut so it doesn't read as a glitch.
- A graphic that repeats the spoken words (chat bubbles, a quote) → hide `#caps` while it is on screen, then bring them back.
- Don't animate `#stage` transforms except `x` for shake — the camera writes the panels, `filter` is used by `defocus`.
