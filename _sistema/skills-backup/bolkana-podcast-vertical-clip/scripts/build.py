#!/usr/bin/env python3
"""Build a HyperFrames vertical-clip composition from an edit decision file.

Usage (run from the build dir, normally <project>/clip/):
  python3 build.py                 # edit.json + scenes.* + template -> ../index.html
  python3 build.py --words         # print every transcript word with refined source/output time (pick anchors)
  python3 build.py --dry           # print anchors/captions/panels without writing

Inputs in the build dir:
  edit.json      edit decisions (schema: SKILL.md → "edit.json")
  scenes.css / scenes.html / scenes.js   project-specific motion graphics (optional)
                 scenes.html may use {{icon:<name>}} (any file in assets/brand/icons, e.g. {{icon:ghost}}) —
                 it is inlined as <span class="ico">…</span> with fill=currentColor (size it with font-size / width)
Brand (Bolkana): fonts + logos are copied to <projectRoot>/brand/ on every build; edit.json "brand" block:
  {"footage": "color"|"bw", "header": true, "youtube": "wearebolkana", "eyebrow": "The Bolkana Podcast"}
  header = v2: Bolkana logotype + Ibinn sponsor ("En colaboración con") in the IG arrow/camera row, YouTube handle above the IG username
  No end card: the clip ends on its last word ("tail" defaults to 0)
  align-dtw.json whisper DTW token timings of the same audio (optional, from align_dtw.sh)
"""
import json, re, sys, os, difflib, unicodedata, shutil

HERE = os.path.dirname(os.path.abspath(__file__))
TEMPLATE = os.path.join(HERE, "..", "assets", "template.html")
BRAND = os.path.join(HERE, "..", "assets", "brand")
args = set(sys.argv[1:])
E = json.load(open("edit.json"))
ROOT = E.get("projectRoot", "..")
P = lambda p: os.path.join(ROOT, p)

SEG = [tuple(s) for s in E["segments"]]
SIL = [tuple(s) for s in E.get("silences", [])]
FULL, SPL = E.get("fyFull", .36), E.get("fySplit", .46)

def o(t):
    """source seconds -> output seconds (times inside a removed range snap to the next kept segment).
    The containing segment wins first, so a segment reused out of source order (e.g. a borrowed pause) works."""
    acc = 0
    for a, b in SEG:
        if a <= t <= b: return round(acc + t - a, 3)
        acc += b - a
    acc = 0
    for a, b in SEG:
        if t < a: return round(acc, 3)
        acc += b - a
    return round(acc, 3)

# ---------- words: transcript text, onsets refined with DTW and snapped out of measured silences ----------
W = [w for w in json.load(open(P(E.get("transcript", "assets/transcript.json")))) if w["text"].strip()]
norm = lambda x: unicodedata.normalize("NFD", re.sub(r"[^\w]", "", x.lower())).encode("ascii", "ignore").decode()
dt = {}
if os.path.exists(E.get("dtw", "align-dtw.json")):
    D = []
    for seg in json.load(open(E.get("dtw", "align-dtw.json")))["transcription"]:
        for t in seg["tokens"]:
            if t["text"].startswith("[_") or t.get("t_dtw", -1) < 0: continue
            if t["text"].startswith(" ") or not D: D.append([t["t_dtw"] / 100, t["text"].strip()])
            else: D[-1][1] += t["text"]
    D = [d for d in D if norm(d[1])]
    A = [norm(w["text"].split(" ")[-1]) for w in W]; B = [norm(d[1]) for d in D]
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, A, B, autojunk=False).get_opcodes():
        if tag in ("equal", "replace") and i2 - i1 == j2 - j1:
            for k in range(i2 - i1): dt[i1 + k] = D[j1 + k][0]
lead = E.get("dtwLead", 0.1)
fix = E.get("textFixes", {})
words = []
for i, w in enumerate(W):
    s = w["start"] if w.get("pinned") else dt[i] - lead if i in dt else w["start"]   # "pinned": true keeps a hand-set onset
    for a, b in SIL:
        if a - 0.08 <= s < b: s = b + 0.02
    txt = w["text"]
    for k, v in fix.items(): txt = re.sub(r"\b%s\b" % re.escape(k), v, txt)
    words.append([s, txt, w.get("id", "w%d" % i)])
for i in range(1, len(words)):
    if words[i][0] < words[i - 1][0] + 0.07: words[i][0] = words[i - 1][0] + 0.07

BR = {"footage": "color", "header": True, "youtube": "wearebolkana", "eyebrow": "The Bolkana Podcast", **E.get("brand", {})}

if "--words" in args:
    for s, txt, wid in words:
        inside = any(a <= s <= b for a, b in SEG)
        print(f"{wid:>6}  src {s:7.2f}  out {o(s):7.2f}  {'' if inside else '[CUT] '}{txt}")
    sys.exit()

# ---------- captions: 1–2 words, ≤13 chars, break on punctuation / pause / keyword ----------
KEY = {k.lower() for k in E.get("keywords", [])}
caps = []; cur = None
for s, txt, _ in words:
    if not any(a <= s <= b for a, b in SEG) and not any(a <= s + 0.15 <= b for a, b in SEG):
        continue                                            # word lives in a removed range (filler, retake)
    clean = re.sub(r"[.,;:!?¿¡]", "", txt).strip()
    parts = clean.split(" "); isk = any(p.lower() in KEY for p in parts)
    brk = (cur is None or len(cur["w"]) >= 2 or len(" ".join(x[1] for x in cur["w"]) + " " + clean) > E.get("capChars", 13)
           or cur["p"] or s - cur["last"] > 0.35 or isk or any(x[2] for x in cur["w"]))
    if brk: cur = {"s": s, "w": [], "p": False, "last": s}; caps.append(cur)
    cur["w"].append([o(s), clean, isk]); cur["p"] = bool(re.search(r"[.,;:!?]$", txt)); cur["last"] = s
segs = []; acc = 0
for a, b in SEG:
    segs.append({"ms": a, "d": round(b - a - (0.001 if (a, b) != SEG[-1] else 0), 3), "st": round(acc, 3)}); acc += b - a
vidEnd = round(acc, 3); total = round(acc + E.get("tail", 0), 2)   # no end card: the clip ends on its last word (tail only if explicitly asked)
out = []
for i, c in enumerate(caps):
    s = o(c["s"]); nxt = o(caps[i + 1]["s"]) if i + 1 < len(caps) else vidEnd
    out.append({"s": s, "e": round(min(nxt, s + 1.1), 3), "w": c["w"]})

# ---------- anchors: word ids + source-time cuts -> output seconds ----------
ref = {wid: s for s, _, wid in words}
T = {k: o(ref[v]) for k, v in E.get("keys", {}).items()}
T.update({k: o(v) for k, v in E.get("srcKeys", {}).items()})
J = [s["st"] for s in segs]
def at(expr):
    """'name', 'name-0.12', 'seg:3', 'seg:3+0.4', 'end', or a number -> output seconds"""
    if isinstance(expr, (int, float)): return float(expr)
    m = re.match(r"^\s*([A-Za-z_][\w]*(?::\d+)?|[\d.]+)((?:\s*[+-]\s*[\d.]+)*)\s*$", str(expr))
    if not m: raise SystemExit(f"bad time expression: {expr}")
    head, tail = m.group(1), m.group(2)
    if head.startswith("seg:"): v = J[int(head[4:]) - 1]
    elif head == "end": v = vidEnd
    elif re.match(r"^[\d.]+$", head): v = float(head)
    else:
        if head not in T: raise SystemExit(f"unknown anchor '{head}' (define it in keys/srcKeys)")
        v = T[head]
    for sign, num in re.findall(r"([+-])\s*([\d.]+)", tail): v += float(num) if sign == "+" else -float(num)
    return round(v, 3)

trk = {name: [[o(t), x, y] for t, x, y in pts] for name, pts in E["tracks"].items()}
def keys(lst):
    r = []
    for k in lst:
        t, who, s, s1, fx, fy = k[:6]; d = k[6] if len(k) > 6 else 0; e = k[7] if len(k) > 7 else "out"
        fy = FULL if fy == "full" else SPL if fy == "split" else fy
        r.append({"t": at(t), "who": who, "s": s, "s1": s1, "fx": fx, "fy": fy, "d": d, "e": e})
    return sorted(r, key=lambda k: k["t"])
camTop = keys(E["camera"]["top"]); camBot = keys(E["camera"].get("bottom", []))
split = sorted([[at(t), h, d] for t, h, d in E.get("split", [[0, 1920, 0]])])
seam = [[at(a), at(b)] for a, b in E.get("seam", [])]

# lower-panel visibility windows (split open, including its open/close transitions)
wins = []; openT = None
for i, (t, h, d) in enumerate(split):
    if h < 1920 and openT is None: openT = t
    if h >= 1920 and openT is not None: wins.append((openT, t + d + 0.05)); openT = None
if openT is not None: wins.append((openT, vidEnd))

# ---------- media nodes ----------
src = E["source"]
top = [dict(s, id=f"v{i}") for i, s in enumerate(segs, 1)]
bot = []
for w0, w1 in wins:
    for i, s in enumerate(segs, 1):
        a, b = max(w0, s["st"]), min(w1, s["st"] + s["d"])
        if b - a > 0.02:
            bot.append({"id": f"vb{len(bot)+1}", "st": round(a, 3), "d": round(b - a, 3), "ms": round(s["ms"] + a - s["st"], 3)})
# an identical top/bottom pair (same start+duration) trips duplicate_media_discovery_risk: split the top one in two
final_top = []
for s in top:
    if any(abs(b["st"] - s["st"]) < 1e-6 and abs(b["d"] - s["d"]) < 1e-6 for b in bot):
        h = round(s["d"] / 2, 3)
        final_top += [{"id": s["id"] + "a", "st": s["st"], "d": h, "ms": s["ms"]},
                      {"id": s["id"] + "b", "st": round(s["st"] + h, 3), "d": round(s["d"] - h, 3), "ms": round(s["ms"] + h, 3)}]
    else: final_top.append(s)
vid = lambda s, tr, ind: f'{ind}<video id="{s["id"]}" class="clip" src="{src}" data-start="{s["st"]}" data-duration="{s["d"]}" data-media-start="{s["ms"]}" data-track-index="{tr}" muted playsinline></video>'
V = "\n".join(vid(s, 0, "      ") for s in final_top)
VB = "\n".join(vid(s, 1, "      ") for s in bot)
AU = "\n".join(f'  <audio id="a{i}" src="{src}" data-start="{s["st"]}" data-duration="{s["d"]}" data-media-start="{s["ms"]}" data-track-index="10"></audio>' for i, s in enumerate(segs, 1))
mu = E.get("music")
MU = f'  <audio id="music" src="{mu["file"]}" data-start="0" data-duration="{total}" data-track-index="11" data-volume="{mu.get("volume", .22)}"></audio>' if mu else ""
SX = []
for i, x in enumerate(E.get("sfx", []), 1):
    t = at(x["at"]); d = x.get("dur", 0.6) if x.get("dur") != "rest" else round(total - t, 2)
    d = round(min(d, total - t), 2)   # never run past the end of the clip
    SX.append(f'  <audio id="sx{i}" src="{x["file"]}" data-start="{round(t,2)}" data-duration="{d}" data-track-index="{12 + i % 3}" data-volume="{x.get("vol", .22)}"></audio>')

tt = E.get("title", {})
cfg = {"srcW": E.get("srcW", 1920), "srcH": E.get("srcH", 1080), "total": total, "vidEnd": vidEnd, "segs": segs, "caps": out, "t": T,
       "trk": trk, "camTop": camTop, "camBot": camBot, "split": split, "seam": seam,
       "capSkip": E.get("capSkip", []), "titleOut": at(tt.get("out", 3.5)), "header": bool(BR["header"])}

print("anchors:", json.dumps(T, ensure_ascii=False))
print(f"video {vidEnd}s · total {total}s · jump cuts at {J[1:]}")
print("split windows (lower panel):", wins)
for c in out: print(f'{c["s"]:6.2f}-{c["e"]:6.2f}  ' + " ".join(("*" if w[2] else "") + w[1] for w in c["w"]))
if "--dry" in args: sys.exit()

rd = lambda f: open(f).read() if os.path.exists(f) else ""

# ---------- brand kit -> <projectRoot>/brand (fonts + logos; icons are inlined) ----------
for sub in ("fonts", "logos"):
    dst = P(os.path.join("brand", sub)); os.makedirs(dst, exist_ok=True)
    for f in os.listdir(os.path.join(BRAND, sub)): shutil.copy2(os.path.join(BRAND, sub, f), os.path.join(dst, f))
def icon(m):
    if isinstance(m, str): m = re.match(r"(.*)", m)
    f = os.path.join(BRAND, "icons", m.group(1).strip() + ".svg")
    if not os.path.exists(f): raise SystemExit(f"unknown brand icon '{m.group(1)}' (see assets/brand/icons/)")
    svg = re.sub(r"<\?xml[^>]*>", "", open(f).read()).strip()
    svg = re.sub(r'\s(width|height)="[^"]*"', "", svg, count=2).replace('"#292D32"', '"currentColor"').replace('"black"', '"currentColor"')
    return '<span class="ico">' + svg + '</span>'
scenes_html = re.sub(r"\{\{icon:([^}]+)\}\}", icon, rd("scenes.html"))
for bad in re.findall(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", scenes_html + rd("scenes.js")):
    print("WARNING: emoji in scenes (Bolkana: no emoji) ->", bad)
FOOT = "filter:grayscale(1) contrast(1.08) brightness(.98)" if BR["footage"] == "bw" else ""
h = open(TEMPLATE).read()
for k, v in {"__LANG__": E.get("lang", "es"), "__SRCW__": str(cfg["srcW"]), "__SRCH__": str(cfg["srcH"]), "__TOTAL__": str(total),
             "__VIDEOS__": V, "__VIDEOS_B__": VB, "__AUDIO__": AU, "__MUSIC__": MU, "__SFX__": "\n".join(SX),
             "__TITLE_PILL__": tt.get("eyebrow", tt.get("pill", BR["eyebrow"])), "__TITLE_A__": tt.get("a", ""), "__TITLE_B__": tt.get("b", ""),
             "__END_A__": tt.get("endA", tt.get("a", "")), "__END_B__": tt.get("endB", tt.get("b", "")), "__FOOTAGE_FILTER__": FOOT,
             "__YT_ICON__": icon("youtube"), "__YT_HANDLE__": BR["youtube"],
             "__SCENES_CSS__": rd("scenes.css"), "__SCENES_HTML__": scenes_html, "__SCENES_JS__": rd("scenes.js"),
             "__CFG__": json.dumps(cfg, ensure_ascii=False)}.items():
    h = h.replace(k, v)
open(P("index.html"), "w").write(h)
print("wrote", P("index.html"), "— re-run the music carve after every build (it edits index.html)")
