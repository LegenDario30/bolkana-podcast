---
name: "bolkana-podcast-miniaturas"
description: "Crea las miniaturas de cada episodio del podcast de Bolkana: YouTube 16:9 y redes 4:5, con recortes del invitado y de Lavi, colores del brand book y el patrocinio de Ibinn."
---

# Miniaturas del podcast de Bolkana

Genera por episodio DOS PNG a partir de los mismos datos:
- **wide**: YouTube, 1920×1080.
- **tall**: LinkedIn, Instagram, TikTok, Linktree, 1080×1350 (4:5).

Responde en español y de forma breve. Entrega siempre los dos PNG con SendUserFile.
Referencia aprobada: #17 Kompanion (`episodios/17 | Kompanion/05_miniaturas/final/`, 21-10-2026). Si hay dudas de estilo, abrirla y copiarla.

## Diseño (decidido con Iria, no cambiar sin que lo pida)
- **Composición:** invitado a la izquierda sobre rojo, Lavi (presentador, es la marca) a la derecha sobre verde, graphite en el centro. Las caras van en COLOR, nunca en blanco y negro. Ambos con recorte de pecho hacia arriba, mirando hacia el centro. Lavi siempre aparece, y se coloca hacia la derecha, no demasiado al centro.
- **Colores del brand book:** Graphite `#232323`, Lava `#D31C1F`, Grass `#5CD41C`, Bone `#F3F3F3`. No usar `#000000` ni `#FFFFFF`.
- **Fondo (cambiado en el #17):** NADA de rellenar medio lienzo de rojo y verde. Un **halo** rojo detrás de la cabeza del invitado y uno verde detrás de la de Lavi, que **se funden pronto a graphite**: el centro, la zona del titular y la parte de abajo quedan casi negros. Valores por defecto del template (`gs` 1150 en wide, `gs2` 900 en tall, opacidad `ga` .95 en el centro y `gm` .38/.34 a mitad). Si un halo queda descentrado de la cabeza, moverlo con `glx/gly/grx/gry` (wide) o `glx2/gly2/grx2/gry2` (tall).
- **Micrófonos:** en wide se dejan los dos micros, pero separando a las personas hacia los lados para que no queden detrás del titular (`gl` -190, `hr` -210 por defecto). En **tall solo se ve el micro de Lavi**: el del invitado se borra y se reconstruye su ropa (ver paso 3). Ver dos micros juntos en el centro del 4:5 queda feo.
- **Tipografía:** Outfit (800 para el titular, 600 para el resto).
- **Titular:** frase gancho de máximo 5-6 palabras, en 2-3 líneas con saltos `<br>` puestos a mano, color Bone. La idea clave en Grass con `<span class=hl>` (una sola mancha verde: p. ej. «La <span class=hl>IA</span> va a<br>sustituir a<br>tu gestor»). No debe tocar las caras. En YouTube debe completar el título, no repetirlo.
- **Nombre del invitado:** en mayúsculas con letter-spacing, y debajo su cargo y empresa («Fundador de Kompanion»); solo la empresa si no se da cargo. En tall va bien abajo, justo encima de la fila inferior y sin solaparse con el titular.
- **Ibinn (patrocinador principal):** en AMBOS formatos, arriba y centrado: «En colaboración con» + logo de Ibinn.
- **Solo YouTube (wide):** SIN logo de Bolkana y SIN «Disponible en».
- **Solo redes (tall):** abajo a la izquierda «Disponible en» con iconos de YouTube, Spotify, Apple Podcasts y Amazon Music; abajo a la derecha el logo de Bolkana.
- **Prueba obligada:** reducir cada miniatura a 170 px de ancho y comprobar que se leen las caras y el titular.

## Datos que hay que pedir por episodio
1. Fotos: lo normal es que Iria pase **dos capturas** (invitado y Lavi, ~1276×1620, webp). Si no, sacar frames del vídeo (paso 1). Lavi e invitado **sonriendo** salvo que diga otra cosa. Si el frame es de 720p las caras salen blandas: avisar.
2. Nombre del invitado, cargo y empresa (no inventarlos; si falta, preguntar). Suele estar en `EPISODIO.md`.
3. Frase gancho. Si no la trae, **proponer ~10** basadas en lo que dice el invitado (leer `guiones.md` / transcripción; cifras reales). Estilo de referencia: «Emprender te está costando la salud» (#16) y «La IA va a sustituir a tu gestor» (#17): directa, al espectador, 5-6 palabras. Si la pide «menos provocativa», tirar de curiosidad e historia («Un café que acabó en inversión», «Empezó con 5.000 € y una web»). Dar 2-3 favoritas con el porqué.

## Dónde va cada cosa (proyecto `~/Bolkana/Bolkana Podcast`)
- Entrega: `episodios/<NN | Invitado>/05_miniaturas/final/`: `#NN | <Invitado> 16-9.png`, `#NN | <Invitado> 4-5.png`, y las fotos usadas como `#NN | Frame <Nombre>.png` (+ `#NN | Frame <Nombre> sin micro.png`).
- Candidatos de frames: `05_miniaturas/frames/` (con hojas de contactos `hoja_<quien>.jpg`).
- Si se rehace una miniatura entregada, mover la anterior a `final/_prev/` (`… v1.png`), nunca sobrescribirla sin más.
- Apuntar en `EPISODIO.md` (Notas) el titular, las fotos y los parámetros usados.

## Recursos (todo está en `_sistema/marca/`; se preparan en `thumbs/assets/` con `prep_assets.py`)
- `ibinn.png`: `brand-assets/Logomark/Ibinn logotype/Logo_Sponsor.png` (blanco con alfa), recortado al bbox.
- `logo.png`: `brand-assets/Logomark/logotype/logotype_bone.png` (isotipo + «Bolkana», bone con alfa), recortado al bbox.
- `outfit/outfit-600|700|800.ttf`: de `brand-assets/Typography/Outfit.zip` → `static/Outfit-SemiBold|Bold|ExtraBold.ttf`.
- `ic_youtube|spotify|apple|amazon.png`: recortados de `episodios/16 | Cristina Guzman/05_miniaturas/final/#16 | Cristina Guzman 4-5.png` (cajas x 60-121 / 133-175 / 187-229 / 241-283, y 1283-1325; 2 px hacia dentro, máscara redondeada, escalar ×3).
- `guest.png` (con micro, para wide), `guest_nomic.png` (sin micro, para tall; si el invitado no tiene micro delante, copiar guest.png) y `host.png`.
- Scripts: `scripts/` de esta skill (`.claude/skills/bolkana-podcast-miniaturas/scripts/`: `template.py`, `prep_assets.py`, `borrar_micro.py`). En el Codespace están en el repo (`/workspaces/bolkana-podcast/.claude/skills/…`): copiarlos a `/tmp/thumbs/`.

## Dónde se ejecuta: el Codespace
El Mac (8 GB, sin PIL/rembg/Playwright) no se usa para esto. Todo en el Codespace del podcast (ver CLAUDE.md del proyecto; `cs.sh '<cmd>'` en `.claude/skills/bolkana-episodio/scripts/`):
- `/workspaces` va justo de disco: trabajar en **`/tmp/thumbs`** y el venv en **`/tmp/tv`**. **`/tmp` se borra al parar el Codespace**: hay que volver a subir entradas y reinstalar cada vez.
- Subir: `COPYFILE_DISABLE=1 tar --no-xattrs -C <dir> -c . | cs.sh 'mkdir -p /tmp/thumbs/in && tar -x -C /tmp/thumbs/in'`. Bajar: `cs.sh 'cat /tmp/thumbs/x.png' > local.png`. No imprimir nada por stdout en el mismo comando que un `tar -c` (rompe el tar).
- Instalar: `python3 -m venv /tmp/tv; export XDG_CACHE_HOME=/tmp/cache TMPDIR=/tmp U2NET_HOME=/tmp/u2net; /tmp/tv/bin/pip install torch --index-url https://download.pytorch.org/whl/cpu; /tmp/tv/bin/pip install "rembg[cpu]" pillow numpy playwright simple-lama-inpainting opencv-python-headless`.
- Chrome para Playwright: el de HyperFrames, `~/.cache/hyperframes/chrome/chrome-headless-shell/linux-*/chrome-headless-shell-linux64/chrome-headless-shell` (ya puesto en `template.py`).
- Al acabar: `gh codespace stop -c <nombre>` e informar del consumo (h-núcleo del mes, de 120).

## Pasos
1. **Frames del vídeo** (solo si Iria no pasa fotos). El máster está en el Codespace (`01_fuente/`, 4K, un keyframe por segundo):
   - Sacar todos los keyframes pequeños, rápido: `ffmpeg -skip_frame nokey -i master.mp4 -vf scale=480:-2 -vsync 0 -q:v 4 /tmp/kf/%06d.jpg` (frame n ≈ segundo (n-1)·1.001).
   - Clasificar por color de fondo: rojo > 40 % de píxeles = primer plano del invitado; verde > 30 % = primer plano de Lavi (OpenCV, HSV). Los detectores de sonrisa de OpenCV no sirven: puntuar «dientes visibles» en la boca solo orienta.
   - Hojas de contactos (8 columnas, número en cada miniatura), elegir a ojo sonrisas, y extraer esos instantes en 4K (`-ss t -frames:v 1 -q:v 2`). Lavi sonríe poco en su primer plano: buscar al principio y al final del episodio; en el plano general se ríe más (en 4K vale).
   - Bajar al Mac los 4K + hojas con la cara recortada a `05_miniaturas/frames/` y que Iria elija.
2. **Recortar personas** con rembg, **modelo `isnet-general-use`** (mantiene el micro; `u2net_human_seg` se lo come y deja muescas):
   - NUNCA borrar zonas con rectángulos. Para quitar restos (silla, mesa, vaso): corte horizontal limpio por debajo del pecho (la parte de abajo queda en el borde del lienzo) y difuminado suave de alfa en la esquina inferior.
   - Revisar el recorte sobre fondo verde o rojo antes de montar.
```python
from rembg import remove, new_session
from PIL import Image, ImageFilter
import numpy as np
s=new_session('isnet-general-use')
im=Image.open('frame.png').convert('RGB')        # si el frame es ancho, recortar antes a una caja alrededor de la persona
o=remove(im,session=s,alpha_matting=True,alpha_matting_foreground_threshold=240,alpha_matting_background_threshold=15,alpha_matting_erode_size=8)
o=o.crop((0,0,o.width,Y_PECHO))   # #17 (1276x1620): Edu 1380, Lavi 1330
W,H=o.size; a=np.array(o.getchannel('A')).astype(float)/255
x=np.arange(W)[None,:]/W; y=np.arange(H)[:,None]/H
ss=lambda t,a0,a1:(lambda u:u*u*(3-2*u))(np.clip((t-a0)/(a1-a0),0,1))
sx=ss(x,0.04,0.30); sy=ss(y,0.70,0.90); a=a*(1-(1-sx)*sy)   # esquina inf. izquierda (Lavi: restos de silla); invitado: 1-x
o.putalpha(Image.fromarray((a*255).astype('uint8'))); o=o.crop(o.getbbox())
# si el frame es de 720p: o=o.resize((int(o.width*1.6),int(o.height*1.6)),Image.LANCZOS)
rgb=o.convert('RGB').filter(ImageFilter.UnsharpMask(radius=2,percent=50,threshold=2)); rgb.putalpha(o.getchannel('A'))
rgb.save('assets/host.png')   # o guest.png / guest_nomic.png
```
3. **Quitar el micro del invitado (para tall)** con `scripts/borrar_micro.py`:
   - Mirar la zona con una rejilla (líneas cada 50 px con coordenadas) y pasar un polígono **amplio** que envuelva micro, soporte y cable: `python borrar_micro.py frame_edu.png "860,830 900,782 1000,786 1100,815 1180,785 1276,735 1276,1075 1150,1075 1000,1065 900,995 858,920"` (valores del #17). La máscara se saca por color (lo que no es ni camisa azul ni fondo rojo dentro del polígono); si la ropa no es azul, cambiar el rango de `shirt`.
   - LaMa rellena la camisa y el fondo de forma natural (el hombro queda redondeado). Revisar `_mask.png` y el resultado.
   - Recortar el frame limpio con rembg (paso 2) → `raw.png`, y pulir el borde: `python borrar_micro.py --borde raw.png frame_edu_mask.png` → `raw_fix.png` (alfa suave y sin el filo rojo/morado que deja el fondo). Revisar sobre verde y sobre graphite. De ahí sale `guest_nomic.png` (paso 2: corte de pecho + unsharp).
4. **Renderizar:** `scripts/template.py` copiado en `thumbs/`:
```
python template.py '{"title":"La <span class=hl>IA</span> va a<br>sustituir a<br>tu gestor","name":"Edu Mas","company":"Fundador de Kompanion"}' salida
```
   Genera `salida_wide.png` y `salida_tall.png`. Los valores por defecto son los aprobados en el #17. Parámetros opcionales (JSON):
   - `fs` / `fs2`: titular en wide (122) / tall (100). Si una línea es larga, acortar la frase antes de bajar el tamaño.
   - `gl` / `hr`: posición del invitado / Lavi en wide (-190 / -210; más negativo = más hacia fuera). Ajustar hasta que los micros no queden detrás del titular.
   - `glt` / `hrt`: posición del invitado / Lavi en tall (-40 / -90; si Lavi tapa el hombro del invitado, más negativo).
   - `gt`: imagen del invitado en tall (`guest_nomic.png`).
   - Halos: `gs`, `gs2`, `ga`, `gm`, `glx/gly/grx/gry`, `glx2/gly2/grx2/gry2`.
5. **Revisar:** abrir los PNG y comprobar: titular nunca sobre las caras ni con un micro detrás, nombre y empresa sin tocar el titular en tall, recortes sin bordes duros, halos detrás de las cabezas y el resto graphite, un solo micro en tall, y prueba a 170 px. Iterar, guardar en `final/` con los nombres de arriba y enviar los dos archivos.

## Casos especiales
- **Dos invitados:** el lado rojo debe admitir dos caras; reducir la escala y revisar el solape con el titular.
- **Titular largo:** acortarlo antes de reducir la tipografía.
- **Falta la empresa o el cargo:** preguntar; no inventarlos.
- **Mesa, vaso o silla en el recorte:** se quitan cortando por debajo y difuminando, nunca con rectángulos. El micro de Lavi se queda; el del invitado solo se quita en tall.
- **Tarea programada para más tarde** (Iria se queda sin créditos): copiar antes las fotos que haya pegado en el chat a `05_miniaturas/final/` (el scratchpad se pierde).

## Scripts (en `scripts/`)
- `template.py`: render de las dos miniaturas (Playwright + Chrome de HyperFrames). Valores por defecto = #17.
- `borrar_micro.py`: borrar el micro del invitado con LaMa (`frame.png "polígono"`) y pulir el borde (`--borde raw.png mask.png`).
- `prep_assets.py`: prepara `assets/` (logos, iconos, fuentes) desde `/tmp/thumbs/in/` (subir ahí: `ibinn_src.png` = Logo_Sponsor.png, `logo_src.png` = logotype_bone.png, `ep16_45.png` = miniatura 4-5 del #16, `Outfit-SemiBold/Bold/ExtraBold.ttf`).
