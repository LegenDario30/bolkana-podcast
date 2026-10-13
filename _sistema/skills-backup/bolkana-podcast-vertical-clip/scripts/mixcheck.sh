#!/usr/bin/env bash
# mixcheck.sh <project_dir> — how loud is the music bed under the voice, as the renderer actually mixes it?
# Builds two throwaway copies next to the project (as-is, and with the music muted), lets `hyperframes render` write its
# mixed audio track (it does that before capturing frames — ~30–60 s each), stops the render, and subtracts the two.
# Prints the voice loudness, the music-only loudness and the gap. Target: music 19–21 dB under the voice
# (client, 2026-10-05: library songs must be subtle, never in front, ~20 dB under). Adjust edit.json → music.volume and re-run.
set -e; exec </dev/null   # never read the caller's stdin (it ate a batch loop's list once)
source "$(dirname "$0")/_env.sh"
P="$(cd "$1" && pwd)"; PARENT="$(dirname "$P")"; NAME="$(basename "$P")"; SK="$(cd "$(dirname "$0")" && pwd)"
TMP="$(mktemp -d)"; VER=$(grep -o 'hyperframes@[0-9.]*' "$P/package.json" | head -1 | cut -d@ -f2); VER=${VER:-latest}
grab(){ # $1 variant name, $2 volume override ('' = keep)
  local C="$PARENT/_mixcheck_${NAME}_$1"; rm -rf "$C"; cp -R "$P" "$C"
  if [ -n "$2" ]; then python3 - "$C" "$2" <<'PY'
import json,sys,re
p=sys.argv[1]+'/index.html'; s=open(p).read()
s=re.sub(r'(<audio id="music"[^>]*data-volume=")[0-9.]+(")', r'\g<1>'+sys.argv[2]+r'\2', s); open(p,'w').write(s)
PY
  fi
  mkdir -p "$TMP/$1"; (cd "$C" && npx --yes hyperframes@$VER render -o "$TMP/$1/t.mp4" . </dev/null >/dev/null 2>&1) & local RP=$!; disown $RP 2>/dev/null || true
  for i in $(seq 1 150); do f=$(ls "$TMP/$1"/work-*/audio.m4a 2>/dev/null | head -1)
    if [ -n "$f" ] && [ "$(stat -f%z "$f" 2>/dev/null || stat -c%s "$f")" -gt 50000 ]; then sleep 3; cp "$f" "$TMP/$1.m4a"; break; fi; sleep 2; done
  pkill -P $RP 2>/dev/null || true; kill $RP 2>/dev/null || true; sleep 2; pkill -f "$TMP/$1/t.mp4" 2>/dev/null || true
  rm -rf "$C"; [ -f "$TMP/$1.m4a" ] || { echo "no audio for $1"; exit 1; }
}
L(){ ffmpeg -hide_banner -nostats -i "$1" -af ebur128 -f null - 2>&1 | grep -A1 "Integrated loudness" | grep "I:" | awk '{print $2}'; }
grab mix ""; grab voice 0
ffmpeg -v error -y -i "$TMP/mix.m4a" -i "$TMP/voice.m4a" -filter_complex "[0][1]amerge=inputs=2,pan=stereo|c0=c0-c2|c1=c1-c3" "$TMP/music.wav"
V=$(L "$TMP/voice.m4a"); M=$(L "$TMP/music.wav")
python3 - "$V" "$M" <<'PY'
import sys; v,m=float(sys.argv[1]),float(sys.argv[2]); g=v-m
verdict="OK" if 19<=g<=21 else ("too quiet: raise music.volume" if g>21 else "too loud: lower music.volume")
print(f"voice {v:.1f} LUFS · music {m:.1f} LUFS · music sits {g:.1f} dB under the voice → {verdict}")
PY
rm -rf "$TMP"
