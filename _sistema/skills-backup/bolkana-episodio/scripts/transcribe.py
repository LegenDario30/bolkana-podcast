#!/usr/bin/env python3
"""transcribe.py <episode dir> [model] — transcribe the whole master once, word by word (openai-whisper, Spanish).
Run with ~/Bolkana/Bolkana Podcast/_sistema/tools/whisper-venv/bin/python3 and in the background: ~1 h of audio takes a while.
Writes 02_transcripcion/: podcast_16k.wav, podcast_whisper.json, podcast_words.json ({text,start,end,prob,id}) and podcast.txt
([mm:ss.ss] per segment) — the same layout as #16, which cut_fragments.py and the clip skill expect."""
import os, sys, glob, json, subprocess
ep = os.path.abspath(sys.argv[1]); model_name = sys.argv[2] if len(sys.argv) > 2 else "small"
root = ep
while root != "/" and not os.path.isdir(os.path.join(root, "_sistema")): root = os.path.dirname(root)
os.environ["PATH"] = os.path.join(root, "_sistema/tools/bin") + ":" + os.environ["PATH"]
masters = sorted(glob.glob(os.path.join(ep, "01_fuente", "*.mp4")) + glob.glob(os.path.join(ep, "01_fuente", "*.mov")))
if not masters: sys.exit("no master in 01_fuente/")
T = os.path.join(ep, "02_transcripcion"); os.makedirs(T, exist_ok=True); wav = os.path.join(T, "podcast_16k.wav")
if not os.path.exists(wav):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", masters[0], "-ac", "1", "-ar", "16000", wav], check=True)
import whisper
r = whisper.load_model(model_name).transcribe(wav, language="es", word_timestamps=True, verbose=False, condition_on_previous_text=False)
json.dump(r, open(os.path.join(T, "podcast_whisper.json"), "w"), ensure_ascii=False, indent=1)
words = []
for s in r["segments"]:
    for w in s.get("words", []):
        words.append({"text": w["word"].strip(), "start": round(w["start"], 3), "end": round(w["end"], 3), "prob": round(w.get("probability", 0), 3), "id": "w%d" % len(words)})
json.dump(words, open(os.path.join(T, "podcast_words.json"), "w"), ensure_ascii=False, indent=1)
with open(os.path.join(T, "podcast.txt"), "w") as f:
    for s in r["segments"]:
        m, sec = divmod(s["start"], 60); f.write("[%02d:%05.2f] %s\n" % (m, sec, s["text"].strip()))
print("master", os.path.basename(masters[0]), "· words", len(words), "· segments", len(r["segments"]))
