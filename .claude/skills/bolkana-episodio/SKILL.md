---
name: bolkana-episodio
description: Dirige un episodio completo del podcast de Bolkana de principio a fin. Prepara la carpeta, transcribe el máster, propone ~20 guiones de clips verticales para que el usuario elija 12–15, los edita con 2 agentes en paralelo en el Codespace (skill bolkana-podcast-vertical-clip) y los renderiza de uno en uno. Después saca frames del invitado y del presentador sonriendo para la miniatura, prepara una ficha de publicación por clip (Instagram, TikTok, YouTube Shorts y LinkedIn) y lleva el estado al día. Úsala cuando el usuario diga "vamos con el 17", "ya tengo el máster del episodio X", "nuevo episodio", "sácame los clips de este podcast", "sigue con el episodio", "¿cómo va el 17?", o cuando deje un máster nuevo del podcast. Para editar un único clip suelto, usa directamente bolkana-podcast-vertical-clip.
---

# Bolkana · un episodio de principio a fin

Esta skill dirige y las demás ejecutan. Todo pasa en **una sesión principal** abierta en `~/Bolkana/Bolkana Podcast`. Esa sesión
lee la transcripción entera, propone los guiones, reparte la edición entre agentes y lleva el estado. Lee primero el
`CLAUDE.md` de la raíz: sus reglas fijas (marca, gráficos, cortes, música) mandan sobre todo lo de aquí.

`E="$HOME/Bolkana/Bolkana Podcast/.claude/skills/bolkana-episodio/scripts"` (siempre entre comillas: la ruta tiene espacios; en el Codespace `~/Bolkana/Bolkana Podcast` enlaza al repo) · `PY=~/Bolkana/Bolkana Podcast/_sistema/tools/whisper-venv/bin/python3`
(con whisper y numpy) · `EP="episodios/<NN | Invitado>"`

## Retomar siempre desde el estado

Cada episodio tiene un `estado.json` con la fase de cada clip. Al empezar o al oír "sigue con el 17" / "¿cómo va?":
```bash
python3 "$E"/estado.py "$EP"
```
Hay que continuar desde lo que falte y no rehacer lo que ya está. Fases de un clip:
`propuesto → elegido → editando → revision → aprobado → ficha → subido` (o `descartado`).

## Fases y puntos de control

| Fase | Quién la hace | Resultado | ✋ Quién decide |
|---|---|---|---|
| 0 · Preparar | Sesión principal | carpeta, máster, `EPISODIO.md` | — |
| 1 · Transcribir | Sesión principal, en segundo plano | `02_transcripcion/` | — |
| 2 · Guiones | Sesión principal | `guiones.md` con ~20 clips + 2 fijos (vinos, pregunta Ibinn) | **El usuario elige 12–15** |
| 3 · Edición | 2 agentes en paralelo (límite de uso), en el Codespace, renders en cola | `04_renders/final/` | **El usuario revisa cada clip** |
| 4 · Frames para la miniatura | Sesión principal | `05_miniaturas/frames/` (invitado y Lavin sonriendo) | **El usuario elige y hace la miniatura** |
| 5 · Fichas | Sesión principal | `06_pies-de-foto/` (una por clip) | — |
| 6 · Subida | **El usuario, a mano** | Buffer (IG, TikTok, YouTube) + LinkedIn | El usuario |

No hay que avanzar a la fase siguiente sin la decisión de los puntos marcados con ✋. Lo que sí se puede hacer es solapar
fases: mientras el usuario revisa los primeros clips, siguen editándose los demás.

### 0 · Preparar
- Si la carpeta no existe: `./_sistema/nuevo-episodio.sh <NN> "<Invitado>" [máster]`. Si existe pero está vacía, el script
  la rellena con la plantilla.
- El máster va en `01_fuente/#NN | Invitado.mp4`. Hay que medirlo con ffprobe (resolución, fps, duración).
- Hay que pedir al usuario **una sola vez para todo el episodio** el nombre completo del invitado, su cargo y su empresa,
  porque los pies de foto y las miniaturas los necesitan. Nunca hay que inventarlos. Se apuntan en `EPISODIO.md`.

### 1 · Transcribir (una vez por episodio)
```bash
"$PY" "$E"/transcribe.py "$EP"        # con run_in_background: tarda bastante con 1 h de audio
```
Genera `podcast_words.json` (palabra a palabra) y `podcast.txt` (por segmentos y con tiempos). Mientras transcribe, se
sacan unos frames del máster para saber dónde se sienta cada hablante y en qué planos sale. Eso se apunta en
`EPISODIO.md` → Hablantes.

### 2 · Guiones (~20 → el usuario elige 12–15)
Ver `references/guiones.md`: criterios, formato y registro en el estado. Se hace en la sesión principal, que lee la
transcripción completa. Al usuario se le da una tabla corta y se espera a que elija.

### 3 · Edición en paralelo (en el Codespace, desde el #17)
El máster y los proyectos viven en el Codespace; la sesión principal y los agentes lo manejan desde el Mac con
`bash "$E/cs.sh" '<comando>'` (ver `references/agente-clip.md` → «Modo Codespace»). Antes de empezar: `cs.sh 'git pull'`
para que el Codespace tenga las skills del repo, y comprobar disco (`df -h /workspaces`, hacen falta ~8 GB libres).
1. Con los clips elegidos se escribe `03_clips/fragments.json` (rangos de palabra exactos de `guiones.md`) y se crea un
   proyecto por clip copiando `_base` (`cp -a`; cambiar el id de `meta.json`). Se cortan todos de una vez en el Codespace,
   con `nohup` (tarda ~3 min por cada 30 s de clip) y lanzando el script desde un `.sh` propio (nunca `pkill -f` con un
   patrón que aparezca en el comando ssh: se mata a sí mismo):
   `cut_fragments.py --master "../01_fuente/#NN | Invitado.mp4" --words ../02_transcripcion/podcast_words.json --fragments fragments.json --root . --height 1440 --preset fast`
   (`--height 1440` = versión de trabajo de un máster 4K; `--preset fast` ≈ 2× más rápido que `slow`).
2. **Límite de uso del plan (lo que manda de verdad):** cada clip gasta ~10–15 % del límite de 5 h. Con 7 agentes se
   agotó la sesión en minutos. Por defecto **2 agentes a la vez** (4 si hay margen); mirar el uso con `get_usage` en cada
   aviso de un agente y pausar (TaskStop) los más atrasados antes de llegar al tope que diga el usuario. Un agente
   pausado o cortado por el límite conserva su trabajo: se retoma con SendMessage («retoma desde donde lo dejaste;
   el Codespace puede haberse apagado: relanza procesos perdidos»), nunca con un agente nuevo. Si el usuario lo
   autoriza, programar con CronCreate un aviso de un solo uso para retomarlos al reiniciarse el límite.
   Empezar por los clips con más ★; los dos fijos (vinos, Ibinn) al final.
3. Los agentes renderizan **de uno en uno** con `render_queue.sh` en el Codespace (~6 s por segundo de vídeo) y bajan el
   MP4 al Mac **comprobando que el tamaño coincide** (una descarga truncada pareció una «imagen congelada» en el #17).
4. Con cada informe: `estado.py set NN fase=revision proyecto=… dur=… cancion=…`, fila en `EPISODIO.md` y en
   `CANCIONES.md`, y al usuario **solo el enlace del clip** y, si las hay, las dudas que debe escuchar (lo pidió así).
5. **Revisión del usuario.** «Ok» → `aprobado`. Cambios → regla de versiones del `CLAUDE.md`: copiar a `_vN` con
   `rsync -a --exclude media OLD/ NEW/ && cp -al OLD/media NEW/media` (solo los vídeos de `media/` quedan como enlaces
   duros y no duplican GB; el resto se copia de verdad, porque `cat >` reescribe en sitio y tocaría la versión anterior;
   nunca reescribir un vídeo de `media/` con el mismo nombre), cambiar el id de `meta.json`, editar la copia, render al mismo nombre (render_queue guarda el anterior en `_prev/` con
   fecha si ya existe). Agrupar 3–4 clips de cambios pequeños por agente. Para alargar un clip, la sesión principal
   saca los rangos nuevos de `podcast_words.json`, los corta con `cut_fragments.py` en `clip_NN_<slug>_vN` y el agente
   rehace la edición desde el paso 1b.3.
6. **Al terminar cada tanda: parar el Codespace** (`gh codespace stop -c <nombre>`) e informar del consumo. Al pararlo se
   pierden `/tmp` y los procesos en marcha (renders a medias incluidos); el disco se conserva.

### 4 · Miniaturas: aquí solo se sacan los frames
Frame y miniatura **no son lo mismo**. Claude **solo extrae los frames**. La miniatura la hace el usuario después con la
skill **bolkana-podcast-miniaturas**, que no se ejecuta en esta fase salvo que él lo pida. Ejemplo de referencia:
`episodios/16 | Cristina Guzman/05_miniaturas/`.

1. Se sacan del máster, a resolución completa, frames candidatos del **invitado sonriendo** y de **Lavin sonriendo**: cara
   de frente o mirando hacia el centro, nítidos, sin manos delante de la cara y sin la boca a medio hablar. Hay que
   recorrer todo el episodio (las risas suelen estar en los momentos que se marcaron como humor en los guiones) y quedarse
   con unos 5 del invitado y unos 3 de Lavin.
2. Se guardan en `05_miniaturas/frames/` con el nombre `<persona>_<letra>_<mm>m<ss>s[_nota].png`, por ejemplo
   `cristina_A_06m47s.png` o `lavin_B_07m30s_mirando_izq.png`. Se le enseñan al usuario.
3. **El usuario elige** un frame de cada persona y los deja en `05_miniaturas/final/` como `#NN | Frame <Invitado>.png` y
   `#NN | Frame Lavin.png`. Con ellos crea las miniaturas usando bolkana-podcast-miniaturas:
   `#NN | <Invitado> 16-9.png` (YouTube) y `#NN | <Invitado> 4-5.png` (redes). Si lo pide, se le puede proponer una frase
   gancho sacada de los mejores guiones.

### 5 · Fichas de publicación
Ver `references/ficha-publicacion.md`. Hay una por clip aprobado, con los textos de la skill **bolkana-pies-de-foto**:
Instagram, TikTok, título y descripción de YouTube Shorts, y LinkedIn. Al final se le da al usuario un orden sugerido de
publicación.

### 6 · Subida (la hace el usuario)
El usuario sube cada vídeo a Buffer a mano, pega los textos de la ficha y usa los huecos de la cola de Buffer. LinkedIn
lo publica él directamente. **No hay que crear ni programar posts en Buffer**, porque el MCP solo acepta URLs públicas y
el plan gratuito tiene 10 posts programados. Si el usuario contrata un plan de pago o pide otra cosa, se vuelve a plantear.
Cuando diga qué clips ha subido, se marcan como `subido`.

Se puede hacer de forma opcional, si el usuario lo pide: unas semanas después, revisar con `get_aggregated_post_metrics`
de Buffer qué tipo de gancho funcionó mejor y tenerlo en cuenta en los guiones del siguiente episodio.

## Al terminar cada sesión de trabajo
`EPISODIO.md` (tabla de clips y estado), `estado.json` y `CANCIONES.md` tienen que estar al día. El usuario tiene que
poder abrir una sesión nueva, decir "sigue con el 17" y que todo continúe sin explicaciones.
