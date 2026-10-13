#!/usr/bin/env bash
# faces.sh <video> <t0> <dur> <every_s> <cropW> <cropH> <cropX> <cropY> <out.jpg>
# Tiles crops of the source every N seconds with a grid; each grid cell = cropW/8 source px. Read face centres off it.
set -e; source "$(dirname "$0")/_env.sh"
ffmpeg -v error -y -ss "$2" -t "$3" -i "$1" -vf "fps=1/$4,crop=$5:$6:$7:$8,scale=320:-1,drawgrid=w=40:h=40:color=white@0.5,tile=5x2" -frames:v 1 "$9"
echo "tile 320px wide = $5 source px → 1 grid cell (40px) = $(( $5 / 8 )) source px; frame k at t=$2+k*$4; add crop offset ($7,$8)"
