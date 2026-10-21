# Encargo para un agente de edición (uno por clip)

Lanzar con la herramienta Agent (`subagent_type: general-purpose`, `run_in_background: true`), **2–4 a la vez como
máximo** según el límite de uso (19-10-2026: con 7 se agotó la sesión; con 4 se quedó cerca, el usuario lo bajó a 2). Cuando uno termina, se lanza el siguiente de la lista. Los renders van en cola de uno en uno (`render_queue.sh`),
así que varios agentes pueden estar editando mientras otro renderiza.

Antes de lanzar: el corte de fragmentos (`cut_fragments.py`) ya se ha hecho en la sesión principal para todos los clips
elegidos, y cada clip tiene su proyecto `03_clips/clip_NN_<slug>/` (copia de `_base`).

## Plantilla del encargo (rellenar los <>)

```
Edita el clip <NN> del episodio #<EP> del podcast de Bolkana como vertical 9:16.

Carpeta del episodio: ~/Bolkana/Bolkana Podcast/episodios/<EP | Invitado>/
Proyecto del clip: 03_clips/clip_<NN>_<slug>/  (ya creado, con el corte de fragmentos hecho)
Guion: sección "Clip <NN>" de guiones.md en la carpeta del episodio (gancho/desarrollo/cierre, por qué funciona,
énfasis, canción sugerida). Datos del máster, offset y posición de las caras: EPISODIO.md.

Usa la skill bolkana-podcast-vertical-clip (cárgala con la herramienta Skill) y sigue su proceso desde el paso 1b.3
(analyze → align → edit.json → cutplan → escenas → música → build → check → carve → mixcheck → QA).
Lee y respeta ~/Bolkana/Bolkana Podcast/CLAUDE.md (reglas fijas de marca, gráficos, cortes y música).
Antes de entregar, repasa la sección «Client corrections from #17» de la skill de clips: es lo que el cliente
corrigió en el #17 y no debe repetirse.

Música: elige con _sistema/musica/analisis.json y CANCIONES.md y corta con bgmcut.py. Intenta no
repetir las canciones ya asignadas en este episodio: <lista de clip → canción ya asignadas>.
NO escribas en CANCIONES.md ni en EPISODIO.md ni en estado.json: lo hace la sesión principal con tu informe.

Render: NO uses npm run render directamente. Usa la cola compartida:
  bash "$HOME/Bolkana/Bolkana Podcast/.claude/skills/bolkana-episodio/scripts/render_queue.sh" "<proyecto>" "<ep>/04_renders/final/#<EP> | clip_<NN>_<slug>.mp4"
Después verifica el MP4 como dice la skill (hoja de contactos, whisper de los últimos 3 s y de cada borde).

No preguntes nada al usuario: si algo del guion no se puede hacer (un salto que rompe la frase, una cara tapada),
decide lo más fiel al "por qué funciona" y explícalo en el informe.

Informe final (breve, en español), con exactamente estos campos:
- render: ruta del MP4
- duracion: s
- cancion: archivo · desde s · volumen · dB bajo la voz (mixcheck)
- cortes: primera y última palabra, saltos hechos
- graficos: qué hay y cuándo
- dudas: lo que el usuario debería revisar (o "ninguna")
```

## Al recibir el informe (sesión principal)

1. `estado.py <ep> set NN fase=revision proyecto=… render=… dur=… cancion=…`
2. Añadir la fila del clip a `CANCIONES.md` → "Asignaciones" del episodio y a la tabla de `EPISODIO.md`.
3. Si quedan clips pendientes, lanzar el siguiente agente (pasándole las canciones ya asignadas).
4. Avisar al usuario en una línea (clip listo + dudas si las hay). No esperar a que acaben todos para enseñar los primeros.

## Modo Codespace (desde el #17)

Antes de lanzar agentes: las skills de Bolkana viven en el repo (`.claude/skills/`), así que en el Codespace basta con
`cs.sh 'git pull'` en la rama del episodio (sin cambios sin commitear allí). hyperframes-audio (carve.sh la usa) sigue en
`~/.claude/skills/` del Codespace, igual que en el Mac (`tar … | cs.sh 'tar -xf - -C ~/.claude/skills'` si falta).
El máster y los proyectos de los clips viven en el Codespace; el agente corre en el Mac y lo maneja todo por ssh con
`bash "$HOME/Bolkana/Bolkana Podcast/.claude/skills/bolkana-episodio/scripts/cs.sh" '<comando>'` (cwd = `/workspaces/bolkana-podcast`). Añadir al encargo:

```
TODO el trabajo pesado se hace en el Codespace, no en el Mac (8 GB, sin máster):
- Ejecuta cada comando con: bash "$HOME/Bolkana/Bolkana Podcast/.claude/skills/bolkana-episodio/scripts/cs.sh" '<comando>'
  El cwd es /workspaces/bolkana-podcast. Las rutas llevan "|" y espacios: dentro de las comillas simples usa siempre
  comillas dobles, p. ej. cs.sh 'cd "episodios/17 | Kompanion/03_clips/clip_01_x" && ls'.
- Proyecto: /workspaces/bolkana-podcast/episodios/<EP>/03_clips/clip_<NN>_<slug>/ (ya tiene media/clip_<NN>_<slug>_joined.mp4,
  clip/transcript.json y clip/fragments_plan.json del corte, a 2560×1440 y 25 fps). Empieza en el paso 1b.3 de la skill.
- Scripts de la skill en el Codespace: .claude/skills/bolkana-podcast-vertical-clip/scripts (ruta relativa al cwd; los mismos del repo).
  Lee SKILL.md y references/ en el Mac.
- Escribir archivos: créalos en una carpeta tuya del Mac y súbelos con  cs.sh 'cat > "<ruta>"' < archivo_local
  (o tar -cf - … | cs.sh 'tar -xf - -C "<dir>"'). Ver imágenes: cs.sh 'cat "<ruta.png>"' > local.png y léela.
- Render (en el Codespace, con rutas absolutas):
  cs.sh 'bash .claude/skills/bolkana-episodio/scripts/render_queue.sh "/workspaces/bolkana-podcast/episodios/<EP>/03_clips/clip_<NN>_<slug>" "/workspaces/bolkana-podcast/episodios/<EP>/04_renders/final/#<NN> | clip_<NN>_<slug>.mp4"'
  Después baja el MP4 al Mac, a la misma ruta bajo ~/Bolkana/Bolkana Podcast/, con cs.sh 'cat "<ruta>"' > "<ruta Mac>".
  Comandos largos (render, whisper): lánzalos con run_in_background y espera la notificación; no hagas bucles de sleep.
- No toques otros clips, no hagas git, no instales paquetes y no pares el Codespace (lo gestiona la sesión principal).
```

## Lecciones del #17 (añadir al encargo cuando aplique)

- **Versiones:** `rsync -a --exclude media <vigente>/ <nueva>/ && cp -al <vigente>/media <nueva>/media`, y nuevo id en
  `meta.json`. No `cp -a` a secas (duplicaba GB y llenó el disco) ni `cp -al` del proyecto entero.
- **Encuadre:** en el editado del #17 los primeros planos venían pegados arriba; escala mínima con la imagen arriba y
  comprobar que la cara no queda bajo la cabecera. En pantallas partidas, la cara de cada uno centrada en su mitad (el
  cliente se quejó de «ver solo el techo»). Revisar el seguimiento de cara (`trk`) en los tramos finales: una pista mal
  medida desliza la cámara.
- **Bordes de segmento:** revisar fotograma a fotograma; un cambio de cámara del editado 1–2 fotogramas antes del borde
  deja un fotograma suelto (la «pared roja» del #17). Mover el borde al fotograma del corte.
- **Subtítulos:** tras el render, mirar el **último fotograma**: si queda una palabra encima del subtítulo final, hay un
  grupo pegado. `build.py` quita `¿?¡!` de los subtítulos; si el cliente pide signos, se reponen con un `clip/postbuild.sh`
  que se ejecuta después de cada build (ver clip 21 del #17).
- **Bajar al Mac:** comprobar que el tamaño coincide con el del Codespace.
- **No borrar en el Mac:** sobrescribir el MP4 con el nuevo; la versión anterior queda en `borradores/_prev/` del Codespace.
