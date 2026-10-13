---
name: bolkana-episodio
description: Dirige un episodio completo del podcast de Bolkana de principio a fin. Prepara la carpeta, transcribe el máster, propone ~20 guiones de clips verticales para que el usuario elija 12–15, los edita con 2–3 agentes en paralelo (skill bolkana-podcast-vertical-clip) y los renderiza de uno en uno. Después saca frames del invitado y del presentador sonriendo para la miniatura, prepara una ficha de publicación por clip (Instagram, TikTok, YouTube Shorts y LinkedIn) y lleva el estado al día. Úsala cuando el usuario diga "vamos con el 17", "ya tengo el máster del episodio X", "nuevo episodio", "sácame los clips de este podcast", "sigue con el episodio", "¿cómo va el 17?", o cuando deje un máster nuevo del podcast. Para editar un único clip suelto, usa directamente bolkana-podcast-vertical-clip.
---

# Bolkana · un episodio de principio a fin

Esta skill dirige y las demás ejecutan. Todo pasa en **una sesión principal** abierta en `~/Bolkana/Bolkana Podcast`. Esa sesión
lee la transcripción entera, propone los guiones, reparte la edición entre agentes y lleva el estado. Lee primero el
`CLAUDE.md` de la raíz: sus reglas fijas (marca, gráficos, cortes, música) mandan sobre todo lo de aquí.

`E=~/.claude/skills/bolkana-episodio/scripts` · `PY=~/Bolkana/Bolkana Podcast/_sistema/tools/whisper-venv/bin/python3`
(con whisper y numpy) · `EP="episodios/<NN | Invitado>"`

## Retomar siempre desde el estado

Cada episodio tiene un `estado.json` con la fase de cada clip. Al empezar o al oír "sigue con el 17" / "¿cómo va?":
```bash
python3 $E/estado.py "$EP"
```
Hay que continuar desde lo que falte y no rehacer lo que ya está. Fases de un clip:
`propuesto → elegido → editando → revision → aprobado → ficha → subido` (o `descartado`).

## Fases y puntos de control

| Fase | Quién la hace | Resultado | ✋ Quién decide |
|---|---|---|---|
| 0 · Preparar | Sesión principal | carpeta, máster, `EPISODIO.md` | — |
| 1 · Transcribir | Sesión principal, en segundo plano | `02_transcripcion/` | — |
| 2 · Guiones | Sesión principal | `guiones.md` con ~20 clips | **El usuario elige 12–15** |
| 3 · Edición | 2–3 agentes en paralelo, renders en cola | `04_renders/final/` | **El usuario revisa cada clip** |
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
"$PY" $E/transcribe.py "$EP"        # con run_in_background: tarda bastante con 1 h de audio
```
Genera `podcast_words.json` (palabra a palabra) y `podcast.txt` (por segmentos y con tiempos). Mientras transcribe, se
sacan unos frames del máster para saber dónde se sienta cada hablante y en qué planos sale. Eso se apunta en
`EPISODIO.md` → Hablantes.

### 2 · Guiones (~20 → el usuario elige 12–15)
Ver `references/guiones.md`: criterios, formato y registro en el estado. Se hace en la sesión principal, que lee la
transcripción completa. Al usuario se le da una tabla corta y se espera a que elija.

### 3 · Edición en paralelo
1. Con los clips elegidos se escribe `fragments.json` (rangos de palabra exactos de `guiones.md`) y se cortan todos de una
   vez con `cut_fragments.py` (skill del clip, paso 1b.2). Después se crea un proyecto por clip:
   `cp -R 03_clips/_base 03_clips/clip_NN_<slug>`.
2. Se lanzan **2 o 3 agentes a la vez como máximo**, uno por clip, con el encargo de `references/agente-clip.md`, en
   segundo plano. Al acabar uno se lanza el siguiente. Hay que empezar por los clips con más ★: así el usuario puede ir
   revisando pronto.
3. Los agentes editan en paralelo, pero **renderizan de uno en uno**. `render_queue.sh` hace de cola entre ellos, porque
   el render es lo que satura el Mac.
4. Con cada informe que llega: se actualizan el estado, `EPISODIO.md` y `CANCIONES.md`, se avisa al usuario en una línea
   y el clip pasa a `revision`.
5. **Revisión del usuario.** Cuando diga "ok" → `aprobado`. Si pide cambios, se aplica la regla de versiones del
   `CLAUDE.md`: `cp -R` a `_v2`, se edita la copia y el render anterior va a `borradores/_prev/`. Esto se puede hacer en la
   sesión principal o con otro agente si son muchos cambios. Hay que responder punto por punto.

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
