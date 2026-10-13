# Locates ffmpeg / whisper-cli / whisper model. Override with FFMPEG_DIR, WHISPER_CLI, WHISPER_MODEL.
_up(){ d="$PWD"; while [ "$d" != "/" ]; do [ -e "$d/$1" ] && { echo "$d/$1"; return; }; d=$(dirname "$d"); done; }
if [ -n "$FFMPEG_DIR" ]; then export PATH="$FFMPEG_DIR:$PATH"; elif ! command -v ffmpeg >/dev/null; then t=$(_up tools/bin); [ -z "$t" ] && t=$(_up _sistema/tools/bin); [ -n "$t" ] && export PATH="$t:$PATH"; fi
command -v ffmpeg >/dev/null || { echo "ffmpeg not found (set FFMPEG_DIR)" >&2; }
_w=$(_up tools/whisper.cpp/build/bin/whisper-cli); [ -z "$_w" ] && _w=$(_up _sistema/tools/whisper.cpp/build/bin/whisper-cli)
: "${WHISPER_CLI:=${HYPERFRAMES_WHISPER_PATH:-$_w}}"
[ -z "$WHISPER_CLI" ] && WHISPER_CLI=$(command -v whisper-cli)
for m in "$WHISPER_MODEL" ~/.cache/hyperframes/whisper/models/ggml-small.bin ~/.cache/hyperframes/whisper/models/ggml-base.bin; do [ -n "$m" ] && [ -f "$m" ] && { WHISPER_MODEL="$m"; break; }; done
export WHISPER_CLI WHISPER_MODEL
