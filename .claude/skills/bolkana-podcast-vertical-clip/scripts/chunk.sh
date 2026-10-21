#!/usr/bin/env bash
# chunk.sh <audio16k.wav> <lang> <t0> <t1> [<t0> <t1> ...] — transcribe short windows to find fillers / verify what a gap holds.
source "$(dirname "$0")/_env.sh"; A="$1"; L="$2"; shift 2; TMP=$(mktemp -d)
while [ $# -ge 2 ]; do ffmpeg -v error -y -ss "$1" -to "$2" -i "$A" -af "apad=whole_len=32000" "$TMP/c.wav"
  echo "[$1-$2] $("$WHISPER_CLI" -m "$WHISPER_MODEL" -l "$L" -nt -f "$TMP/c.wav" 2>/dev/null | tr '\n' ' ')"; shift 2; done
rm -rf "$TMP"
