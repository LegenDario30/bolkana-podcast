#!/usr/bin/env python3
"""music_analyze.py [library dir] — analyze every song in the Bolkana music library (default <podcast root>/_sistema/musica/).
Per song: duration, tempo (onset autocorrelation) + pulse strength, key, brightness (median spectral centroid), band balance,
dynamics, percussiveness and the energy curve in 5 s blocks (dB). Writes <library>/analisis.json and prints a summary.
Run it once when songs are added; read it (with CANCIONES.md) to pick the song and the section that fits each clip.
Also check new songs for vocals with whisper before using them (they must be instrumental)."""
import numpy as np, subprocess, sys, os, glob, json
from _audio import load, FF, music_lib
SR = 22050
KEYS = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
MAJ = np.array([6.35,2.23,3.48,2.33,4.38,4.09,2.52,5.19,2.39,3.66,2.29,2.88])
MIN = np.array([6.33,2.68,3.52,5.38,2.60,3.53,2.54,4.75,3.98,2.69,3.34,3.17])
LIB = sys.argv[1] if len(sys.argv) > 1 else music_lib()
out = {}
for f in sorted(glob.glob(os.path.join(LIB, "*.mp3")) + sorted(glob.glob(os.path.join(LIB, "*.wav")))):
    x = load(f, SR); n, h = 2048, 512
    frames = np.lib.stride_tricks.sliding_window_view(x, n)[::h] * np.hanning(n)
    S = np.abs(np.fft.rfft(frames, axis=1)); fr = np.fft.rfftfreq(n, 1 / SR)
    rms = np.sqrt((frames ** 2).mean(1)); cent = (S * fr).sum(1) / (S.sum(1) + 1e-9)
    flux = np.maximum(0, np.diff(np.log1p(S), axis=0)).sum(1); flux = (flux - flux.mean()) / (flux.std() + 1e-9)
    fps = SR / h; ac = np.correlate(flux, flux, 'full')[len(flux) - 1:]
    lags = np.arange(len(ac)); bpm = 60 * fps / np.maximum(lags, 1)
    m = (bpm > 70) & (bpm < 180); L = lags[m][np.argmax(ac[m])]
    tot = S.sum(); band = lambda a, b: round(100 * S[:, (fr >= a) & (fr < b)].sum() / tot, 1)
    bands = {"sub<120": band(0, 120), "low120-500": band(120, 500), "mid500-2k": band(500, 2000), "pres2-6k": band(2000, 6000), "air>6k": band(6000, 11025)}
    ch = np.zeros(12); sel = (fr > 55) & (fr < 2000); pc = np.round(69 + 12 * np.log2(fr[sel] / 440)).astype(int) % 12
    pw = (S[:, sel] ** 2).sum(0)
    for i in range(12): ch[i] = pw[pc == i].sum()
    best = max((np.corrcoef(np.roll(P, k), ch)[0, 1], k, nm) for P, nm in ((MAJ, 'mayor'), (MIN, 'menor')) for k in range(12))
    seg = int(5 * fps); curve = [round(float(20 * np.log10(rms[i:i + seg].mean() + 1e-9)), 1) for i in range(0, len(rms), seg)]
    db = 20 * np.log10(rms + 1e-9)
    out[os.path.basename(f)] = dict(dur=round(len(x) / SR, 1), tempo=round(60 * fps / L, 1), pulse=round(float(ac[L] / ac[0]), 2),
        key=f"{KEYS[best[1]]} {best[2]}", keyconf=round(float(best[0]), 2), brillo_hz=int(np.median(cent)), bands=bands,
        dyn_db=round(float(np.percentile(db, 95) - np.percentile(db, 10)), 1), perc=round(float((flux > 2).mean() * 100), 1), curve5s=curve)
json.dump(out, open(os.path.join(LIB, "analisis.json"), "w"), indent=1, ensure_ascii=False)
for k, v in out.items():
    print(f"== {k}\n   {v['dur']} s · {v['tempo']} BPM (pulso {v['pulse']}) · {v['key']} · brillo {v['brillo_hz']} Hz · perc {v['perc']}% · dyn {v['dyn_db']} dB")
    print("   bandas", v['bands']); print("   energía/5s", v['curve5s'])
print("wrote", os.path.join(LIB, "analisis.json"))
