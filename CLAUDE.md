# The Bolkana Podcast · clips verticales

Aquí se sacan clips verticales (Reels / TikTok / Shorts) de cada episodio largo del podcast de Bolkana.
Abre Claude Code **siempre en esta carpeta** (`~/Bolkana/Bolkana Podcast`), no dentro de un episodio.

## Estructura

```
_sistema/                    lo que se reutiliza en todos los episodios (no se toca por episodio)
  tools/                     ffmpeg + whisper.cpp (los scripts de la skill lo encuentran solos)
  marca/                     brand-book/ (PDF), brand-assets/ (paquete completo), kit-video/ (logos+fuentes de los clips),
                             bolkana-design.md, frame.md  ← fuente de verdad de la marca
  referencias/               referencia.mp4 (estilo), capturas-cabecera/ (cómo se ve la cabecera en Reels)
  plantilla-episodio/        esqueleto que copia nuevo-episodio.sh
  musica/                    canciones sin copyright para los clips + CANCIONES.md (carácter y asignaciones) + analisis.json
  skills-backup/             copia de las skills bolkana-podcast-vertical-clip y bolkana-episodio (las vivas están en ~/.claude/skills)
  hyperframes-CLAUDE.md      guía genérica de HyperFrames (comandos npm, preview, check)
  nuevo-episodio.sh
episodios/<NN | Invitado>/
  EPISODIO.md                ficha: máster, offset, hablantes, invitado (cargo/empresa), tabla de clips  ← mantenerla al día
  estado.json                fase de cada clip (lo lleva estado.py de la skill bolkana-episodio)
  guiones.md                 los ~20 guiones propuestos (Claude) de los que el usuario elige 12–15
  01_fuente/                 máster "#NN | Invitado.mp4"
  02_transcripcion/          transcripción completa con tiempos por palabra
  03_clips/_base/            proyecto vacío; cada clip = cp -R _base clip_NN_<slug>
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
4. Edición con la skill **bolkana-podcast-vertical-clip**: `fragments.json` → `cut_fragments.py` → un proyecto por clip,
   editados por **2–3 agentes en paralelo**; los renders van **de uno en uno** (`render_queue.sh`). El usuario revisa cada clip.
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
- **Pendiente:** conectar rclone con Google Drive (la autorización la hace el usuario en su navegador); cambiar
  `transcribe.py` por faster-whisper (small int8 ≈ 7,6× más rápido, 96 % de palabras iguales) y añadirlo a `setup.sh`;
  adaptar la skill bolkana-episodio para que los pasos pesados corran en el Codespace.
- Permisos: pedir permiso al usuario antes de descargar, subir a servicios externos o hacer commit/push. Claude nunca
  introduce credenciales; las autorizaciones (gh, rclone) las hace el usuario.

## Reglas fijas (aprendidas en el #16)

- **Marca Bolkana siempre** (ver skill y `_sistema/marca/frame.md`): Graphite/Bone/Lava/Grass, Outfit 600 + Karla, cabecera v2
  (Bolkana + "En colaboración con" Ibinn arriba, YouTube wearebolkana abajo), vídeo **en color**, **sin end card**: el clip acaba en
  la última palabra.
- **Nunca editar un clip ya entregado ni sobrescribir su render.** Copiar el proyecto a `clip_NN_<slug>_v2` (`cp -R`, conserva
  enlaces), editar la copia, mover el render antiguo a `04_renders/borradores/_prev/` y renderizar con el mismo nombre en `final/`.
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
