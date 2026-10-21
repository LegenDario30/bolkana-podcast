#!/usr/bin/env bash
# carve.sh <project_dir> — voiceover carve of the music bed (id="music") against every voice track. Re-run after each build.
set -e; source "$(dirname "$0")/_env.sh"; cd "$1"
VER=$(grep -o 'hyperframes@[0-9.]*' package.json 2>/dev/null | head -1 | cut -d@ -f2); VER=${VER:-latest}
CORE="${HF_CORE_DIR:-$HOME/.cache/hyperframes/hfcore-$VER}"
[ -d "$CORE/node_modules/@hyperframes/core" ] || { mkdir -p "$CORE"; (cd "$CORE" && npm i --silent --no-audit --no-fund @hyperframes/core@$VER); }
# strength: edit.json → music.carve (default 0.3). 0.8 (the carve.mjs default) pushed the bed ~26 dB under the voice, which is inaudible.
ST=$(python3 -c "import json;print(json.load(open('clip/edit.json')).get('music',{}).get('carve',0.3))" 2>/dev/null || echo 0.3)
node ~/.claude/skills/hyperframes-audio/scripts/carve.mjs --comp index.html --bed music --core "$CORE" --strength "$ST" | tail -3
