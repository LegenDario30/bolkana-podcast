#!/usr/bin/env bash
# ref.sh <reference.mp4> <outdir> — contact sheets + scene-change times + 10fps strips around the first transitions.
set -e; source "$(dirname "$0")/_env.sh"; R="$1"; O="${2:-analysis/ref}"; mkdir -p "$O"
ffmpeg -v error -y -i "$R" -vf "fps=2,scale=180:-1,tile=8x3" "$O/tile_%02d.jpg"
cuts=$(ffmpeg -i "$R" -vf "select='gt(scene,0.2)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*" | cut -d: -f2 | tr '\n' ' ')
echo "scene changes: $cuts"; i=0
for c in $cuts; do s=$(python3 -c "print(max(0,$c-0.6))"); ffmpeg -v error -y -ss "$s" -t 1.2 -i "$R" -vf "fps=10,scale=180:-1,tile=6x2" -frames:v 1 "$O/trans_$c.jpg"; i=$((i+1)); [ $i -ge 4 ] && break; done
ls "$O"
