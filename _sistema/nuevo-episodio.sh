#!/bin/bash
# Crea la carpeta de un episodio nuevo a partir de la plantilla.
# Uso:  ./_sistema/nuevo-episodio.sh 17 "Nombre Invitado"  [ruta/al/master.mp4]
set -e
cd "$(dirname "$0")/.."
EP="$1"; INV="$2"; MASTER="$3"
[ -z "$EP" ] || [ -z "$INV" ] && { echo 'Uso: ./_sistema/nuevo-episodio.sh 17 "Nombre Invitado" [master.mp4]'; exit 1; }
DIR="episodios/$EP | $INV"
if [ -e "$DIR" ]; then
  [ -z "$(ls -A "$DIR")" ] || { echo "Ya existe y no está vacía: $DIR"; exit 1; }
  cp -R _sistema/plantilla-episodio/. "$DIR/"; echo "La carpeta existía vacía: la relleno con la plantilla"
else
  cp -R _sistema/plantilla-episodio "$DIR"
fi
sed -i.bak -e "s/__EP__/$EP/g" -e "s/__INVITADO__/$INV/g" "$DIR/EPISODIO.md" && rm -f "$DIR/EPISODIO.md.bak"
sed -i.bak -e "s/__EP__/$EP/g" -e "s/__DATE__/$(date -u +%Y-%m-%dT%H:%M:%SZ)/" "$DIR/03_clips/_base/meta.json" && rm -f "$DIR/03_clips/_base/meta.json.bak"
if [ -n "$MASTER" ]; then mv "$MASTER" "$DIR/01_fuente/#$EP | $INV.mp4"; fi
echo "Creado: $DIR"
echo "Siguiente: pon el máster en 01_fuente/ (si no lo has pasado) y dile a Claude \"vamos con el $EP\"."
