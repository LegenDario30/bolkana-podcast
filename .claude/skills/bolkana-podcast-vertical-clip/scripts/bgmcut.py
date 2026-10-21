#!/usr/bin/env python3
"""bgmcut.py <project dir> <song> <approx from s> <total s> [name] — music bed for a clip from the Bolkana library.
<song>: a file in <podcast root>/_sistema/musica/ or a unique fragment of its name ("chill", "Enough", "Velvet").
<approx from>: the section you chose from analisis.json / CANCIONES.md ("Tramos útiles"). It is snapped to the strongest onset
(a hit of the rhythm) within ±1 s, so the bed starts on the beat (0 stays 0). <total>: video length (no tail).
Writes <project>/.media/audio/bgm/<name>.mp3: fade in 0.25 s, fade out 1.5 s ending with the last word, −16 LUFS.
Then edit.json → "music": {"file": ".media/audio/bgm/<name>.mp3", "volume": ≈0.22, "carve": 0.3}, build, carve, mixcheck."""
import sys, os, glob, subprocess, numpy as np
from _audio import load, FF, music_lib
if len(sys.argv) < 5: sys.exit(__doc__)
P, song, t, total = sys.argv[1], sys.argv[2], float(sys.argv[3]), float(sys.argv[4]); name = sys.argv[5] if len(sys.argv) > 5 else "bgm"
LIB = music_lib(P)
if not os.path.isfile(song):
    hits = [f for f in glob.glob(os.path.join(LIB, "*.mp3")) if song.lower() in os.path.basename(f).lower()]
    if len(hits) != 1: sys.exit(f"song '{song}' not found or ambiguous in {LIB}: " + ", ".join(map(os.path.basename, glob.glob(os.path.join(LIB, '*.mp3')))))
    song = hits[0]
def onset_snap(f, t, sr=22050):
    if t <= 0: return 0.0
    s0 = max(0, t - 1); x = load(f, sr, s0, 2); h, n = 256, 1024
    fr = np.lib.stride_tricks.sliding_window_view(x, n)[::h] * np.hanning(n); S = np.log1p(np.abs(np.fft.rfft(fr, axis=1)))
    fl = np.maximum(0, np.diff(S, axis=0)).sum(1); i = int(np.argmax(fl)); return round(s0 + (i + 1) * h / sr - 0.02, 3)
s = onset_snap(song, t); os.makedirs(os.path.join(P, ".media/audio/bgm"), exist_ok=True)
out = os.path.join(P, ".media/audio/bgm", name + ".mp3"); fo = max(0, total - 1.6)
subprocess.run([FF, "-v", "error", "-y", "-ss", str(s), "-t", str(total + 0.2), "-i", song, "-af",
                f"afade=t=in:st=0:d=0.25,afade=t=out:st={fo}:d=1.5,loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "192k", out], check=True)
print(f"wrote {out} ← {os.path.basename(song)} from {s} s (asked {t}, snapped to the beat), {total} s")
print(f'edit.json: "music": {{"file": ".media/audio/bgm/{name}.mp3", "volume": 0.22, "carve": 0.3}}')
