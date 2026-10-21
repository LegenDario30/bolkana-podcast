#!/usr/bin/env python3
"""Turn kept word ranges into edit.json segments, prune the caption transcript, and verify by ear (whisper).

Usage (from anywhere):  python3 cutplan.py <project dir>            plan from clip/keep.json
                         python3 cutplan.py <project dir> verify     keep hand-edited segments, only re-verify
Needs, in <project>/clip/: edit.json (with "silences"), keep.json, transcript.json, analysis/audio16k.wav
(from analyze.sh), align-dtw.json (optional, from align_dtw.sh).

keep.json = [["w1","w38"], ["w42","w45"], ...]  inclusive word-id ranges to keep, in order.
- Each range starts/ends at the lowest-energy 10 ms point next to its edge words (never inside the neighbour).
- Pauses longer than MAXP inside a range are shortened to PAD on each side (jump cuts the camera must cover).
- transcript.json is pruned to the kept words (the untouched copy is saved once as transcript_full.json; make
  manual text fixes or "pinned": true onsets there, then re-run). Without this, a cut word whose DTW onset lands
  within 0.15 s of a kept segment sneaks into the captions.
- The edited audio is rendered to analysis/edited16k.wav and transcribed whole: read it — a clipped first syllable
  ("es" for "ves", "inversor" without "mucho") or a leftover filler shows up there. Fix by nudging the segment
  edges in edit.json and run again with `verify`.
"""
import json, subprocess, sys, os, wave, array, math, re
C = os.path.abspath(sys.argv[1]); B = os.path.join(C, "clip"); HERE = os.path.dirname(os.path.abspath(__file__))
MAXP, PAD = 0.26, 0.09
verify = len(sys.argv) > 2 and sys.argv[2] == "verify"
tf, tfull = os.path.join(B, "transcript.json"), os.path.join(B, "transcript_full.json")
if not os.path.exists(tfull): json.dump(json.load(open(tf)), open(tfull, "w"), ensure_ascii=False, indent=1)
FULL = json.load(open(tfull)); keep = json.load(open(os.path.join(B, "keep.json")))
n = lambda x: int(x[1:])
inside = lambda w: any(n(a) <= n(w["id"]) <= n(b) for a, b in keep)
E_ = json.load(open(os.path.join(B, "edit.json")))
if not verify:
    json.dump(FULL, open(tf, "w"), ensure_ascii=False, indent=1)     # all words, so --words knows every neighbour
    out = subprocess.run(["python3", f"{HERE}/build.py", "--words"], cwd=B, capture_output=True, text=True).stdout
    ON = {}; ORDER = []
    for l in out.splitlines():
        m = re.match(r"\s*(w\d+)\s+src\s+([\d.]+)", l)
        if m: ON[m[1]] = float(m[2]); ORDER.append(m[1])
    w = wave.open(os.path.join(B, "analysis", "audio16k.wav")); sr = w.getframerate(); a = array.array('h'); a.frombytes(w.readframes(w.getnframes())); S = sr // 100
    E = [10 * math.log10(sum(x * x for x in a[i:i + S]) / S + 1e-9) - 90.3 for i in range(0, len(a) - S, S)]; dur = len(a) / sr
    sm = lambda k: sum(E[max(0, k - 2):k + 3]) / len(E[max(0, k - 2):k + 3])
    def minE(lo, hi):
        lo = max(0, int(lo * 100)); hi = min(len(E) - 1, int(hi * 100))
        return lo / 100 if hi <= lo else min(range(lo, hi + 1), key=lambda k: (round(sm(k)), k)) / 100
    segs = []
    for s, e in keep:
        i = ORDER.index(s); j = ORDER.index(e)
        prev = ON[ORDER[i - 1]] if i > 0 else 0
        nxt = ON[ORDER[j + 1]] if j + 1 < len(ORDER) else dur
        segs.append([round(minE(max(prev + .12, ON[s] - .3), ON[s] + .02), 2), round(min(dur - .02, minE(max(ON[e] + .15, nxt - .35), min(nxt + .02, dur))), 2)])
    res = []
    for a0, b0 in segs:
        cur = a0; k = int(a0 * 100) + 1; run = None
        while k < int(b0 * 100):
            q = sm(k) < -40
            if q and run is None: run = k
            if (not q or k == int(b0 * 100) - 1) and run is not None:
                if (k - run) / 100 > MAXP and run / 100 - a0 > .1 and b0 - k / 100 > .1:
                    res.append([round(cur, 2), round(run / 100 + PAD, 2)]); cur = k / 100 - PAD
                run = None
            k += 1
        res.append([round(cur, 2), b0])
    E_["segments"] = res; json.dump(E_, open(os.path.join(B, "edit.json"), "w"), indent=1, ensure_ascii=False)
res = E_["segments"]
pr = [w for w in FULL if inside(w)]
json.dump(pr, open(tf, "w"), ensure_ascii=False, indent=1)
print("segments", len(res), "output", round(sum(b - a for a, b in res), 2), "s"); print(res)
print("caption words dropped:", [w["text"] for w in FULL if not inside(w)])
fc = "".join(f"[0:a]atrim={a0}:{b0},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b0-a0-0.01:.3f}:d=0.01[a{i}];" for i, (a0, b0) in enumerate(res))
fc += "".join(f"[a{i}]" for i in range(len(res))) + f"concat=n={len(res)}:v=0:a=1[o]"
pv = os.path.join(B, "analysis", "edited16k.wav")
sh = lambda cmd: subprocess.run(["bash", "-c", f'source "{HERE}/_env.sh"; {cmd}'], capture_output=True, text=True, cwd=C)
sh(f'ffmpeg -v error -y -i "{os.path.join(B, "analysis", "audio16k.wav")}" -filter_complex "{fc}" -map "[o]" -ar 16000 -ac 1 "{pv}"')
print("── edited audio, transcribed ──"); print(sh(f'"$WHISPER_CLI" -m "$WHISPER_MODEL" -l es -nt -f "{pv}" 2>/dev/null').stdout.strip())
