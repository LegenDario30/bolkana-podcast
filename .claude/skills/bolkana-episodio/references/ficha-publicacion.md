# Ficha de publicación (una por clip aprobado)

El usuario sube los vídeos a Buffer a mano (el MCP de Buffer solo acepta URLs públicas) y usa los huecos que propone la
cola de Buffer. LinkedIn no está en Buffer: lo publica a mano. Claude **no** crea posts en Buffer ni programa nada; deja la
ficha lista para copiar y pegar.

Los textos salen de la skill **bolkana-pies-de-foto** (frase clave, firma 🌋, #Bolkana + hashtag de tema). Pasarle la
transcripción del clip ya montado (`clip/transcript.json` del proyecto vigente), el nº de episodio y el invitado con
cargo y empresa (de `EPISODIO.md`). Elegir la favorita de las 3 opciones sin preguntar y anotar las otras dos al final
de la ficha por si el usuario prefiere otra.

Archivo: `06_pies-de-foto/#<EP> | clip_<NN>_<slug>.md`

```markdown
# #17 · Clip 03 · <título>
Vídeo: 04_renders/final/#17 | clip_03_<slug>.mp4  ·  <dur> s

## Instagram (Reel)
<pie Reels/TikTok>

## TikTok
<mismo pie que Instagram>

## YouTube Shorts
Título: <máx. 100 caracteres, con gancho; sin hashtags>
Descripción:
<pie Reels/TikTok>

#Shorts

## LinkedIn (a mano)
<pie LinkedIn>

---
Otras opciones de frase clave: 1) … 2) …
```

Reglas: YouTube necesita título (Buffer lo exige) y suele funcionar mejor como pregunta o promesa, no como la cita
literal. No inventar cargos ni empresas: si faltan en `EPISODIO.md`, preguntar una vez al usuario para todo el episodio.

Al terminar todas las fichas: `estado.py <ep> set NN fase=ficha` y darle al usuario la lista de fichas en orden de
publicación sugerido (alternar tonos y no poner seguidos dos clips con la misma canción). Cuando el usuario diga que ha
subido unos clips, marcarlos `fase=subido`.
