# The Bolkana Podcast · clips verticales

Aquí se sacan clips verticales (Reels / TikTok / Shorts) de cada episodio largo del podcast de Bolkana.
Abre Claude Code **siempre en esta carpeta** (`~/Bolkana/Bolkana Podcast`), no dentro de un episodio.

## Estructura

```
.claude/skills/              LAS skills de Bolkana (única copia, con historial en git): bolkana-episodio,
                             bolkana-podcast-vertical-clip, bolkana-podcast-miniaturas, bolkana-pies-de-foto.
                             Se editan aquí y se suben con commit; no duplicarlas en ~/.claude/skills ni en claude.ai.
_sistema/                    lo que se reutiliza en todos los episodios (no se toca por episodio)
  tools/                     ffmpeg + whisper.cpp (los scripts de la skill lo encuentran solos)
  marca/                     brand-book/ (PDF), brand-assets/ (paquete completo), kit-video/ (logos+fuentes de los clips),
                             bolkana-design.md, frame.md  ← fuente de verdad de la marca
  referencias/               referencia.mp4 (estilo), capturas-cabecera/ (cómo se ve la cabecera en Reels)
  plantilla-episodio/        esqueleto que copia nuevo-episodio.sh
  musica/                    canciones sin copyright para los clips + CANCIONES.md (carácter y asignaciones) + analisis.json
  hyperframes-CLAUDE.md      guía genérica de HyperFrames (comandos npm, preview, check)
  nuevo-episodio.sh
episodios/<NN | Invitado>/
  EPISODIO.md                ficha: máster, offset, hablantes, invitado (cargo/empresa), tabla de clips  ← mantenerla al día
  estado.json                fase de cada clip (lo lleva estado.py de la skill bolkana-episodio)
  guiones.md                 los ~20 guiones propuestos (Claude) de los que el usuario elige 12–15
  01_fuente/                 máster "#NN | Invitado.mp4"
  02_transcripcion/          transcripción completa con tiempos por palabra
  03_clips/_base/            proyecto vacío; cada clip = cp -a _base clip_NN_<slug>
  03_clips/clip_NN_<slug>/   un proyecto HyperFrames por clip (solo la versión vigente)
  04_renders/final/          lo que se entrega: "#NN | clip_NN_<slug>.mp4"
  04_renders/borradores/     renders anteriores (_prev/ para versiones sustituidas)
  05_miniaturas/frames/      frames candidatos (invitado y Lavin sonriendo) que saca Claude
  05_miniaturas/final/       frames elegidos por el usuario + sus miniaturas 16-9 y 4-5 (skill bolkana-podcast-miniaturas)
  06_pies-de-foto/           una ficha de publicación por clip
  .media/                    música (bgm) y sfx del episodio
  _archivo/                  pruebas y versiones viejas; no se edita
```

## Proceso de un episodio

Lo dirige la skill **bolkana-episodio** ("vamos con el 17", "sigue con el 17", "¿cómo va el 17?"). Resumen:

1. `./_sistema/nuevo-episodio.sh 17 "Nombre Invitado" [ruta/master.mp4]` y pedir cargo y empresa del invitado.
2. Transcribir el máster entero una vez (whisper, palabra a palabra) a `02_transcripcion/`.
3. Claude lee la transcripción completa y propone **~20 guiones** en `guiones.md` (gancho / desarrollo / cierre con tiempos
   exactos, cita, "por qué funciona"). **El usuario elige 12–15.** El "por qué funciona" decide título, énfasis y zooms.
   Duración libre (si el tema lo merece, más largo) y fragmentos de distintos momentos si suman a la misma idea.
   **Siempre 2 reels fijos más:** los vinos de Karetta Maluca (el invitado coge su botella) y la pregunta de Alejandro
   Tagliaferro (Ibinn).
4. Edición con la skill **bolkana-podcast-vertical-clip**: `fragments.json` → `cut_fragments.py` → un proyecto por clip,
   editados por **2 agentes en paralelo** (el límite de uso del plan manda; ver la skill); los renders van **de uno en uno** (`render_queue.sh`). El usuario revisa cada clip.
5. Claude saca **frames** del invitado y de Lavin sonriendo → `05_miniaturas/frames/`. El usuario elige y crea él las miniaturas
   con **bolkana-podcast-miniaturas** en `05_miniaturas/final/` (frame ≠ miniatura). Una ficha de publicación por clip
   (Instagram, TikTok, YouTube Shorts, LinkedIn) con **bolkana-pies-de-foto** → `06_pies-de-foto/`.
6. **El usuario sube los vídeos a Buffer a mano** (cola de Buffer: IG, TikTok, YouTube) y publica LinkedIn a mano. Claude
   no crea posts en Buffer.
7. `EPISODIO.md`, `estado.json` y `_sistema/musica/CANCIONES.md` siempre al día.

## Trabajo en la nube (Codespace) — desde el #17

El Mac (MacBook Pro 2017, 8 GB, ~5 GB libres) no aguanta el trabajo pesado. Reparto:

- **Codespace** (`musical-broccoli-vg76w7vqw79f7gp`, repo LegenDario30/bolkana-podcast, 4 núcleos / 16 GB / ~21 GB libres,
  ruta `/workspaces/bolkana-podcast`, enlace `~/Bolkana/Bolkana Podcast`): descargar másters de Drive, transcribir, cortar,
  renderizar, sacar frames. Claude lo controla desde el Mac con `gh codespace ssh -c <nombre> -- '<comando>'` (gh está en
  `~/.local/bin`). Para pasar archivos: `tar … | gh codespace ssh … 'tar -x'` o `gh codespace ssh … 'cat archivo' > local`.
- **Mac**: guiones, revisión, miniaturas, pies de foto, EPISODIO.md / estado.json. Al Mac solo vuelven resultados ligeros
  (transcripción, frames, renders finales para revisar). **Nunca se descarga un máster al Mac.**
- **Másters**: se quedan en Google Drive. En el Codespace se bajan de uno en uno con rclone, se saca una versión de trabajo
  y se borra el original (no caben varios másters HD a la vez).
- **Material del #17 en adelante:** vídeo editado (versión final para publicar, sin cortes; ~4,4 GB) + una cámara por persona
  y un plano general (~26 GB cada una) + WAV de los micros. Base de los clips y audio = el editado (se baja entero). Las
  cámaras **no se descargan**: se leen desde Drive (rclone) y se extrae solo el tramo que haga falta como plano recurso
  (reacción real del mismo instante). Sincronía: un único desfase por cámara respecto al editado, medido por audio y anotado
  en EPISODIO.md. Plan B si leer de Drive va mal: unas pocas reacciones fijas por persona cortadas en el Codespace. El WAV
  queda en Drive como respaldo.
- **Cuota** (cuenta Free, límite de gasto 0 USD; 120 h-núcleo/mes y 15 GB/mes, se reinicia el día 1): parar el Codespace al
  acabar (`gh codespace stop -c <nombre>`) e informar del consumo real al usuario
  (`gh api "/users/LegenDario30/settings/billing/usage?year=AAAA&month=M"`).
- **Verificado (13-10-2026):** el render de HyperFrames en el Codespace sale igual que en el Mac (clip 05 del #16: SSIM 0,994,
  mismo volumen) y tarda ~6 s por segundo de vídeo. /dev/shm = 1 GB, ffmpeg 4.4.2.
- **Hecho en el #17:** rclone conectado a Drive (remoto `gdrive:`); la skill bolkana-episodio ya trabaja en el Codespace
  (`cs.sh`, versión de trabajo a 1440p, `render_queue.sh` allí). Las skills viven en `.claude/skills/` del repo y en el
  Codespace se enlazan en `~/.claude/skills` (`setup.sh`).
- **Transcripción:** se mantiene `transcribe.py` (openai-whisper small) tal como estaba. En el #17 se probó faster-whisper
  y al usuario no le convenció; queda para decidir más adelante (21-10-2026). No cambiarlo sin que lo pida.
- **Cerrar un episodio (para dejar sitio al siguiente; el disco del Codespace es de 32 GB):** con los clips aprobados y los
  finales en el Mac, en el Codespace sobran el máster de `01_fuente/` (sigue en Drive), los `*_joined.mp4` de
  `03_clips/*/media/` (se regeneran del máster), `02_transcripcion/podcast_16k.wav` y `04_renders/borradores/`. Claude no
  borra de forma permanente: le da al usuario el comando para que lo ejecute él. Luego `git stash list` limpio, rama
  fusionada en `main` y Codespace en `main` antes de crear el siguiente.
- Permisos: pedir permiso al usuario antes de descargar, subir a servicios externos o hacer commit/push. Claude nunca
  introduce credenciales; las autorizaciones (gh, rclone) las hace el usuario.

## Reglas fijas (aprendidas en el #16)

- **Marca Bolkana siempre** (ver skill y `_sistema/marca/frame.md`): Graphite/Bone/Lava/Grass, Outfit 600 + Karla, cabecera v2
  (Bolkana + "En colaboración con" Ibinn arriba, YouTube wearebolkana abajo), vídeo **en color**, **sin end card**: el clip acaba en
  la última palabra.
- **Nunca editar un clip ya entregado ni sobrescribir su render.** Copiar el proyecto a `clip_NN_<slug>_v2`
  (`rsync -a --exclude media OLD/ NEW/ && cp -al OLD/media NEW/media`: los vídeos como enlaces duros para no llenar el disco),
  editar la copia y renderizar con el mismo nombre en `final/` (`render_queue.sh` guarda el anterior en `borradores/_prev/`).
- **Gráficos (gusto del cliente):** pocos, nunca encima de una cara (revisar en cada zoom y corte), nunca repitiendo lo que dicen los
  subtítulos. Nada de "slabs" grandes de clímax, flashes ni zoom agresivo, ni eyebrows tipo "Como decimos en Bolkana". Clímax =
  subtítulos normales con palabras clave en Lava. Gustó: la "nube de jerga" (chips flotantes con la cara desenfocada) y listas de
  chips blancos pequeñas fuera de las caras. Si una lista repite lo que se dice, ocultar subtítulos mientras está.
- **Cortes:** nunca cortar el final de una palabra ni dejar silencios muertos. Verificar cada borde con whisper (regla word-edge de la skill).
- **Música:** se usan las canciones sin copyright de `_sistema/musica/`, nunca la música sintetizada (rechazada: "de ascensor").
  Hay que elegir la canción que encaje con el guion de cada clip; se pueden repetir canciones (ver tabla en `_sistema/musica/CANCIONES.md`).
  Debe sonar **sutil, de fondo, nunca protagonista**: unos **20 dB bajo la voz** (≈19–21, medir con `mixcheck.sh`), con carve 0.3.
  Hay que normalizar cada recorte a −16 LUFS; el volumen suele quedar en 0.18–0.28. El tramo se recorta empezando en un golpe del
  ritmo, con fundido de entrada de 0.25 s y de salida de 1.5 s al final del clip.
- El título no debe verse en el frame 0; entra hacia ~0.35 s.
- **Aprendido en el #17:** subtítulos en minúscula al empezar frase salvo nombres propios (lo hace `build.py`), clips de
  35–45 s por defecto, y la lista de correcciones del cliente en la skill de clips («Client corrections from #17»):
  repasarla antes de entregar cada clip para evitar rondas de cambios.
