#!/usr/bin/env bash
# align_dtw.sh <audio16k.wav> <lang> <out.json> — whisper token timings with DTW (much tighter onsets than segment timestamps).
set -e; source "$(dirname "$0")/_env.sh"
[ -x "$WHISPER_CLI" ] && [ -f "$WHISPER_MODEL" ] || { echo "whisper-cli/model not found (set WHISPER_CLI / WHISPER_MODEL)"; exit 1; }
preset=$(basename "$WHISPER_MODEL" .bin | sed 's/ggml-//')   # small / base / medium …
"$WHISPER_CLI" -m "$WHISPER_MODEL" -l "${2:-es}" -dtw "$preset" -nfa -ojf -f "$1" -of "${3%.json}" >/dev/null 2>&1
python3 -c "import json,sys;d=json.load(open('$3'));n=sum(1 for s in d['transcription'] for t in s['tokens'] if t.get('t_dtw',-1)>=0);print('dtw tokens:',n)"
