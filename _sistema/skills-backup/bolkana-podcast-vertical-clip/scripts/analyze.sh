#!/usr/bin/env bash
# analyze.sh <video> <outdir> — probe, camera cuts, silences, 20ms energy map, contact sheet, 16k wav.
set -e; source "$(dirname "$0")/_env.sh"
V="$1"; O="${2:-analysis}"; mkdir -p "$O"
echo "== probe"; ffprobe -v error -show_entries stream=codec_type,width,height,r_frame_rate,duration -of compact "$V"
echo "== camera cuts (scene>0.2, source seconds)"; ffmpeg -i "$V" -vf "select='gt(scene,0.2)',showinfo" -f null - 2>&1 | grep -o "pts_time:[0-9.]*" | cut -d: -f2 | tr '\n' ' '; echo
for n in -30 -26; do echo "== silences ${n}dB ≥0.15s (start end)"; ffmpeg -i "$V" -af silencedetect=n=${n}dB:d=0.15 -f null - 2>&1 | grep -o "silence_\(start\|end\): [0-9.]*" | awk '{print $2}' | paste - - | tr '\t' ' ' | tr '\n' ';'; echo; done
ffmpeg -v error -y -i "$V" -ac 1 -ar 16000 "$O/audio16k.wav"
ffmpeg -v error -y -i "$V" -ac 1 -ar 16000 -f s16le "$O/audio16k.raw"
python3 - "$O/audio16k.raw" > "$O/energy.txt" <<'PY'
import array,math,sys
a=array.array('h');a.frombytes(open(sys.argv[1],'rb').read());W=320  # 20 ms
rows=[]
for i in range(0,len(a)-W,W):
  s=sum(x*x for x in a[i:i+W])/W; d=10*math.log10(s+1e-9)-90.3
  rows.append(' ' if d<-40 else '.' if d<-32 else ':' if d<-26 else '|' if d<-18 else '#')
print("# 20ms per char; ' ' silence  . very low  : low  | speech  # loud")
for k in range(0,len(rows),100): print('%6.2f %s'%(k*0.02,''.join(rows[k:k+100])))
PY
echo "== energy map → $O/energy.txt"; head -3 "$O/energy.txt"
ffmpeg -v error -y -i "$V" -vf "fps=1,scale=320:-1,tile=6x6" -frames:v 1 "$O/contact.jpg" && echo "== contact sheet (1 fps) → $O/contact.jpg"
