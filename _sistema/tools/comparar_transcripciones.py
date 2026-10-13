import json, re, sys, os, time, difflib, unicodedata, statistics as st

import argparse
ap = argparse.ArgumentParser()
ap.add_argument("--model", default="small")            # small | medium ...
ap.add_argument("--prompt", default=None)              # vocabulario del dominio (initial_prompt)
ap.add_argument("--out", default=None)                 # JSON de salida (por defecto fw_words_<model>[_prompt].json)
ap.add_argument("--orig", default="podcast_words.json")
ap.add_argument("--wav", default="podcast_16k.wav")
A = ap.parse_args()
ORIG = A.orig
WAV = A.wav
NEW = A.out or ("fw_words_%s%s.json" % (A.model, "_prompt" if A.prompt else ""))

def norm(t):
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^\w]", "", t)

if not os.path.exists(NEW):
    from faster_whisper import WhisperModel
    t0 = time.time()
    m = WhisperModel(A.model, device="cpu", compute_type="int8", cpu_threads=4)
    segs, info = m.transcribe(WAV, language="es", word_timestamps=True,
                              beam_size=1, condition_on_previous_text=False,
                              initial_prompt=A.prompt)
    out = []
    for s in segs:
        for w in (s.words or []):
            out.append({"text": w.word.strip(), "start": round(w.start, 3),
                        "end": round(w.end, 3), "prob": round(w.probability, 3)})
    json.dump(out, open(NEW, "w"), ensure_ascii=False, indent=1)
    print("faster-whisper (%s%s): %d palabras en %.0f s" % (A.model, " + prompt" if A.prompt else "", len(out), time.time() - t0))

a = json.load(open(ORIG)); b = json.load(open(NEW))
# descarta tokens vacíos tras normalizar (solo puntuación)
a = [w for w in a if norm(w["text"])]; b = [w for w in b if norm(w["text"])]
na = [norm(w["text"]) for w in a]; nb = [norm(w["text"]) for w in b]
sm = difflib.SequenceMatcher(None, na, nb, autojunk=False)

lines = []; same = rep = ins = dele = 0
ds, de = [], []
for tag, i1, i2, j1, j2 in sm.get_opcodes():
    if tag == "equal":
        for k in range(i2 - i1):
            same += 1
            ds.append(b[j1 + k]["start"] - a[i1 + k]["start"])
            de.append(b[j1 + k]["end"] - a[i1 + k]["end"])
    else:
        t0 = a[i1]["start"] if i1 < len(a) else (a[-1]["end"] if a else 0)
        orig = " ".join(w["text"] for w in a[i1:i2]) or "—"
        new = " ".join(w["text"] for w in b[j1:j2]) or "—"
        if tag == "replace": rep += max(i2 - i1, j2 - j1)
        elif tag == "insert": ins += j2 - j1
        else: dele += i2 - i1
        ctx = " ".join(w["text"] for w in a[max(0, i1 - 4):i1])
        lines.append("[%02d:%05.2f] ...%s | ORIGINAL: %s | NUEVA: %s" % (t0 // 60, t0 % 60, ctx, orig, new))

def pct(x, th): return 100.0 * sum(1 for v in x if abs(v) <= th) / max(1, len(x))
def p95(x):
    s = sorted(abs(v) for v in x); return s[int(0.95 * (len(s) - 1))] if s else 0

R = []
R.append("== RESUMEN ==")
R.append("Palabras original: %d | nueva: %d | iguales: %d (%.1f %%)" % (len(a), len(b), same, 100 * same / max(1, len(a))))
R.append("Cambiadas: %d | solo en la nueva: %d | solo en la original: %d" % (rep, ins, dele))
R.append("")
R.append("== TIEMPOS (en las %d palabras iguales; nueva − original) ==" % same)
for nm, x in (("inicio", ds), ("fin", de)):
    if x:
        R.append("%-6s media %+0.3f s | mediana %+0.3f s | |p95| %0.3f s | máx %0.3f s | ±50 ms: %.0f %% | ±100 ms: %.0f %% | ±200 ms: %.0f %%"
                 % (nm, st.mean(x), st.median(x), p95(x), max(abs(v) for v in x), pct(x, .05), pct(x, .10), pct(x, .20)))
TERMS = ["bolkana", "why", "escepticos", "ghosting", "emprendedora", "emprendedor", "impostora", "desaprender"]
R.append("")
R.append("== TÉRMINOS CLAVE (apariciones: original -> nueva) ==")
for t in TERMS:
    R.append("%-14s %3d -> %3d" % (t, sum(1 for x in na if x == t), sum(1 for x in nb if x == t)))
if ds and st.median([abs(v) for v in ds]) > 5:
    R.append("!! AVISO: desfase mediano > 5 s; el alineado parece desplazado, no fiarse de los tiempos.")
R.append("")
R.append("== DIFERENCIAS DE TEXTO (%d bloques) ==" % len(lines))
R.extend(lines[:80])
if len(lines) > 80: R.append("... y %d más (ver compare_report.txt)" % (len(lines) - 80))
open("compare_report.txt", "w").write("\n".join(R[:6] + ["", "== DIFERENCIAS DE TEXTO (completo) =="] + lines) + "\n")
print("\n".join(R))
