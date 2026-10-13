#!/usr/bin/env bash
# mkbgm.sh <project dir> <name> <dur> <drop> <hit> [bpm] [style: lofi|warm|lively|upbeat] — original synthesized music bed, mastered to .media/audio/bgm/<name>.mp3
# dur = clip length (CFG.total, = video end: there is no end card); drop = a beat before the climax; hit = climax time.
set -e; source "$(dirname "$0")/_env.sh"; P="$1"; mkdir -p "$P/clip/analysis" "$P/.media/audio/bgm"
ST="${7:-lofi}"
node "$(dirname "$0")/make_music.mjs" "$P/clip/analysis/bgm.wav" --dur "$3" --drop "$4" --hit "$5" --bpm "${6:-96}" --style "$ST" >/dev/null
case "$ST" in lively|upbeat) FX="lowpass=f=13000,aecho=0.8:0.4:60:0.12" ;; *) FX="lowpass=f=8000,aecho=0.8:0.5:60|110:0.25|0.18" ;; esac
ffmpeg -v error -y -i "$P/clip/analysis/bgm.wav" -af "$FX,afade=t=out:st=$(python3 -c "print(max(0,$3-0.8))"):d=0.75,loudnorm=I=-16:TP=-1.5" -b:a 192k "$P/.media/audio/bgm/$2.mp3"
echo "wrote $P/.media/audio/bgm/$2.mp3"
