#!/usr/bin/env bash
# Prepara el Codespace con las mismas herramientas que usa el Mac.
# Se ejecuta una sola vez al crear el Codespace (postCreateCommand).
set -uo pipefail
ROOT="/workspaces/bolkana-podcast"
TOOLS="$ROOT/_sistema/tools"
mkdir -p "$TOOLS/bin"

echo "== 1/7 Paquetes del sistema =="
sudo apt-get update -y
sudo apt-get install -y ffmpeg cmake build-essential git rclone jq \
  libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 \
  libatspi2.0-0 libxcomposite1 libxdamage1 libxfixes3 libxrandr2 libgbm1 \
  libpango-1.0-0 libcairo2 libasound2
ffmpeg -version >/dev/null 2>&1 || echo "AVISO: ffmpeg no arranca; revisar dependencias"

echo "== 2/7 Rutas que esperan las skills (~/Bolkana/Bolkana Podcast) =="
mkdir -p "$HOME/Bolkana"
ln -sfn "$ROOT" "$HOME/Bolkana/Bolkana Podcast"
ln -sf "$(command -v ffmpeg)"  "$TOOLS/bin/ffmpeg"
ln -sf "$(command -v ffprobe)" "$TOOLS/bin/ffprobe"

echo "== 3/7 Whisper (Python, modelo small) =="
python3 -m venv "$TOOLS/whisper-venv"
"$TOOLS/whisper-venv/bin/pip" install --upgrade pip
"$TOOLS/whisper-venv/bin/pip" install torch --index-url https://download.pytorch.org/whl/cpu
"$TOOLS/whisper-venv/bin/pip" install openai-whisper numpy
"$TOOLS/whisper-venv/bin/python3" -c "import whisper; whisper.load_model('small')"

echo "== 4/7 whisper.cpp (whisper-cli) y modelo ggml-small =="
if [ ! -d "$TOOLS/whisper.cpp" ]; then
  git clone --depth 1 https://github.com/ggml-org/whisper.cpp "$TOOLS/whisper.cpp"
fi
( cd "$TOOLS/whisper.cpp" && cmake -B build && cmake --build build -j"$(nproc)" --config Release )
sudo ln -sf "$TOOLS/whisper.cpp/build/bin/whisper-cli" /usr/local/bin/whisper-cli
mkdir -p "$HOME/.cache/hyperframes/whisper/models"
( cd "$TOOLS/whisper.cpp" && bash models/download-ggml-model.sh small )
cp -n "$TOOLS/whisper.cpp/models/ggml-small.bin" "$HOME/.cache/hyperframes/whisper/models/ggml-small.bin"

echo "== 5/7 Claude Code =="
npm install -g @anthropic-ai/claude-code

echo "== 6/7 Skills de Bolkana =="
mkdir -p "$HOME/.claude/skills"
for s in bolkana-episodio bolkana-podcast-vertical-clip; do
  rm -rf "$HOME/.claude/skills/$s"
  cp -R "$ROOT/_sistema/skills-backup/$s" "$HOME/.claude/skills/$s"
done

echo "== 7/7 HyperFrames: Chrome de render y comprobación =="
npx -y hyperframes browser ensure || echo "AVISO: no se pudo preparar Chrome; revisar con 'npx hyperframes doctor'"
npx -y hyperframes doctor || true

cat >> "$HOME/.bashrc" <<'RC'
export WHISPER_MODEL="$HOME/.cache/hyperframes/whisper/models/ggml-small.bin"
cd "$HOME/Bolkana/Bolkana Podcast" 2>/dev/null || true
RC

echo "Listo. Abre una terminal nueva y escribe: claude"
