---
name: "bolkana-buffer"
description: "Programa en Buffer (por su MCP) los clips verticales de un episodio del podcast de Bolkana: Reels de Instagram con la empresa del invitado como colaborador, TikTok y YouTube Shorts, un clip al día, con los vídeos de una carpeta de Google Drive y los textos de las fichas de 06_pies-de-foto/. Úsala cuando el usuario diga «programa los clips del 18 en Buffer», «sube los reels», «aquí tienes la carpeta de Drive con los vídeos», «programa del 11 al 17», «mueve / reprograma los clips en Buffer» o pregunte qué hay programado."
---

# Programar los clips de un episodio en Buffer

El usuario da **la carpeta de Drive con los vídeos finales** y Claude los programa en Buffer con el texto de su ficha.
LinkedIn no está en Buffer: el usuario lo publica a mano y Claude le da el texto de la ficha.

Archivos de la skill:
- `preparar.py`: empareja vídeos y fichas, comprueba los enlaces de Drive, calcula el calendario y deja listas las
  variables de `createPost` para cada canal.

## Datos fijos

- Organización «My organization» `6ac3ca360da1297365556f65` (Europe/Madrid). Canales:
  YouTube «Bolkana» `6ac3e5096a5c39ccb6227092`, Instagram «wearebolkana» (business) `6ac3cb276a5c39ccb6212dc4`,
  TikTok «wearebolkana» `6ac3cc516a5c39ccb6214f04`.
- **Plan gratuito: 10 posts programados por canal.** Cada clip son 3 posts (uno por canal), así que caben 10 clips a la vez.
- **Colaborador solo en los Reels de Instagram**: la cuenta de IG de la empresa del invitado (#17: `kompanion_hq`).
  Pregúntala si no está en `EPISODIO.md` y anótala allí. TikTok y YouTube no tienen colaboradores.

## Reglas (aprendidas en el #17; no saltárselas)

1. **Un clip por día, el mismo día en los tres canales**, en el orden de los números de clip. Se empieza **el día siguiente**:
   nunca se programa nada para hoy. Si ya hay clips programados, se empieza el día después del último.
2. Cada post sale a **la hora del horario de Buffer de ese canal para ese día de la semana**, y siempre con
   **hora fija (`customScheduled`)**. No se usa `addToQueue`: Buffer recoloca los posts de la cola cada vez que cambia otro
   post, y en el #17 eso movió un clip a «hoy».
3. **Texto:** el bloque «Reels / TikTok / YouTube Shorts» de la ficha, igual en los 3 canales. **Título** de YouTube y
   TikTok: el encabezado de la ficha (`# Clip NN · <título>`), como máximo 100 caracteres.
4. **Portada en el segundo 2** (`thumbnailOffset: 2000`) en los 3 canales.
5. Instagram: Reel con `shouldShareToFeed: true` y `collaborators`. YouTube: categoría 22, público, sin avisar a los
   suscriptores, `madeForKids: false`.
6. **Vídeos:** `https://drive.usercontent.google.com/download?id=<ID>&export=download`. La carpeta tiene que estar compartida
   con «cualquiera con el enlace». Buffer guarda ese enlace, no una copia, así que **no se pueden mover, renombrar ni dejar
   de compartir los vídeos hasta que se publiquen**. Recuérdaselo al usuario.
7. **Nunca borrar posts** (`delete_post` es irreversible). Para quitar algo de la cola, pásalo a borrador
   (`editPost` con `saveToDraft: true`); el borrado definitivo lo hace el usuario en Buffer.
8. Cuando el usuario da la carpeta y pide programar, se programa directamente, sin borrador previo. Si la petición es
   ambigua («haz lo mismo», «prepáralos»), pregunta antes si quiere borradores o programarlos ya.

## Paso a paso

### 1. Estado actual de Buffer
`get_account` (para la hora actual) y luego, con `execute_query`:
```graphql
query { posts(first: 50, input: {organizationId: "6ac3ca360da1297365556f65",
  filter: {status: [scheduled, sending, draft, error]}, sort: [{field: dueAt, direction: asc}]}) {
  edges { node { id status channelService dueAt isCustomScheduled assets { ... on VideoAsset { video { title } } } } } } }
```
Así sabrás cuántos huecos quedan por canal (10 − programados) y desde qué día empezar.

### 2. Horario de cada canal
```graphql
query { channels(input: {organizationId: "6ac3ca360da1297365556f65"}) {
  id service postingSchedule { day times paused } } }
```
Guarda el resultado tal cual en el scratchpad como `horario.json`.

### 3. Preparar el plan
```bash
python3 .claude/skills/bolkana-buffer/preparar.py "episodios/<NN | Invitado>" "<url carpeta Drive>" <scratchpad>/horario.json \
  --desde AAAA-MM-DD --clips 01-10 --colaborador <usuario_ig> --salida <scratchpad>/buffer_plan.json
```
El script falla si un enlace de Drive no devuelve un vídeo, si una ficha no tiene el bloque de Reels, si `--desde` es hoy
o anterior, o si un canal pasaría de 10 posts. Imprime la tabla del calendario: revísala (orden, días, horas en hora de
Madrid; el script ya tiene en cuenta el cambio de hora).

### 4. Crear los posts
Para cada canal (`instagram`, `tiktok`, `youtube`), una llamada a `mcp__buffer__execute_mutation` con
`lotes.<canal>.mutation` y `lotes.<canal>.variables` de `buffer_plan.json`. Los Reels **tienen que ir por
`execute_mutation`**: `collaborators` no está en el esquema público ni en `create_post`, pero Buffer lo acepta así
(comprobado en el #17). Por la API no se puede leer de vuelta: pide al usuario que confirme en Buffer que aparece en el
primer Reel.

### 5. Comprobar
Repite la consulta del paso 1: los 3 posts de cada clip tienen que estar el mismo día, ninguno hoy, todos con
`isCustomScheduled: true`, `thumbnailOffset: 2000` y en `durationMs` la duración real del clip (señal de que Buffer leyó
el vídeo de Drive; pide `video { thumbnailOffset durationMs }` en la consulta).
Dale al usuario la tabla final (día · IG · TikTok · YouTube, en hora de Madrid) y el texto de LinkedIn de cada clip.

## Mover o reprogramar
`editPost` **revalida el post entero**: hay que mandar siempre `text`, `assets`, `metadata` (con `collaborators` en los
Reels, o se pierde) y, para cambiar la hora, `mode: customScheduled` + `dueAt` con el desfase correcto (+02:00 en horario de
verano, +01:00 desde el último domingo de octubre). Los posts que subió el usuario a mano tienen el vídeo en
`buffer-media-uploads.s3.amazonaws.com/...`; usa esa URL tal cual (`get_post` → `assets[].source`).
Antes de mover nada, explica el nuevo calendario completo y espera el OK: es fácil malinterpretar «muévelos un día».

## Después de publicar
El día del primer clip, comprueba con `list_posts` (`status: [sent, error]`) que ha salido en los 3 canales. Si alguno
da error, enséñale al usuario `error.message`.
