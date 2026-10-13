# Encargo para un agente de edición (uno por clip)

Lanzar con la herramienta Agent (`subagent_type: general-purpose`, `run_in_background: true`), **2 o 3 a la vez como
máximo**. Cuando uno termina, se lanza el siguiente de la lista. Los renders van en cola de uno en uno (`render_queue.sh`),
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

Música: elige con _sistema/musica/analisis.json y CANCIONES.md y corta con bgmcut.py. Intenta no
repetir las canciones ya asignadas en este episodio: <lista de clip → canción ya asignadas>.
NO escribas en CANCIONES.md ni en EPISODIO.md ni en estado.json: lo hace la sesión principal con tu informe.

Render: NO uses npm run render directamente. Usa la cola compartida:
  bash ~/.claude/skills/bolkana-episodio/scripts/render_queue.sh "<proyecto>" "<ep>/04_renders/final/#<EP> | clip_<NN>_<slug>.mp4"
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
