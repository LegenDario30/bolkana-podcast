#!/usr/bin/env bash
# render_queue.sh <project dir> <output.mp4> — render one clip, but only one render at a time on this Mac.
# Several clip agents edit in parallel; the render is what saturates the machine, so they queue here (mkdir lock).
# A lock older than 45 min is treated as stale (crashed render) and removed.
set -e; LOCK="${TMPDIR:-/tmp}/bolkana-render.lock"; P="$1"; OUT="$2"
[ -n "$P" ] && [ -n "$OUT" ] || { echo "uso: render_queue.sh <proyecto> <salida.mp4>"; exit 1; }
[ -d "$P" ] || { echo "ERROR: no existe el proyecto $P"; exit 1; }
waited=0
until mkdir "$LOCK" 2>/dev/null; do
  if [ -n "$(find "$LOCK" -maxdepth 0 -mmin +45 2>/dev/null)" ]; then echo "lock caducado, lo quito"; rm -rf "$LOCK"; continue; fi
  [ $((waited % 60)) = 0 ] && echo "en cola: renderizando $(cat "$LOCK/who" 2>/dev/null) …"
  sleep 10; waited=$((waited+10))
done
echo "$(basename "$P")" > "$LOCK/who"; trap 'rm -rf "$LOCK"' EXIT
mkdir -p "$(dirname "$OUT")"
if [ -f "$OUT" ]; then PREV="$(dirname "$OUT")/../borradores/_prev"; mkdir -p "$PREV"; B="$(basename "$OUT" .mp4)"; D="$PREV/$B.mp4"
  [ -e "$D" ] && D="$PREV/${B}_$(date +%Y%m%d-%H%M%S).mp4"   # never overwrite an earlier saved version
  mv "$OUT" "$D"; echo "render anterior movido a $D"; fi
cd "$P" || { echo "ERROR: no existe el proyecto $P"; exit 1; }
npm run render -- -o "$OUT" || { echo "ERROR: el render ha fallado"; exit 1; }
[ -s "$OUT" ] || { echo "ERROR: no se ha escrito $OUT"; exit 1; }
echo "render listo: $OUT"
