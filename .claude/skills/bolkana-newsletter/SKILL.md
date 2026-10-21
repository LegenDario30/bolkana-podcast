---
name: "bolkana-newsletter"
description: "Escribe la newsletter de cada episodio del podcast de Bolkana con la voz de Lavin, la maqueta con la plantilla de la marca y la deja como borrador en Brevo a través de su MCP (sin enviarla ni programarla). Úsala cuando el usuario diga «haz la newsletter del 18», «prepara el email del episodio», «sube la newsletter a Brevo», «newsletter de Edu / del invitado», o pida el HTML de la newsletter de un episodio."
---

# Newsletter del podcast de Bolkana

Una newsletter por episodio para anunciarlo a la lista de Bolkana. **Su único objetivo es que la gente haga clic y vea el
episodio**, no que lo lea todo en el email. Corta, en la voz de Lavin, y con el botón de YouTube bien visible.

Archivos de la skill (no copiarlos a otro sitio):
- `plantilla.html`: diseño aprobado (#17). Solo cambian los marcadores `{{…}}`; el resto no se toca sin que lo pida el usuario.
- `rellenar.py`: `python3 rellenar.py <newsletter.json> <salida.html>`. Falla si queda algún marcador sin rellenar.

Por episodio se guardan en `episodios/<NN | Invitado>/`: `newsletter.json` (los datos) y `newsletter.html` (lo que va a Brevo).
Ejemplo completo y aprobado: `episodios/17 | Kompanion/newsletter.json`.

## 1. Datos que hacen falta

Sácalos de `EPISODIO.md`, `guiones.md` y la transcripción (`02_transcripcion/`); pide al usuario solo lo que falte:

- Número de episodio, invitado, cargo y empresa.
- **Enlace del vídeo en YouTube.** YouTube lo da en cuanto el vídeo se programa, aunque no se publique hasta el día siguiente.
- **Enlace del episodio en Spotify**, si ya lo tiene. Antes de publicarse da 404; es normal, pero hay que avisar al usuario para que
  lo compruebe antes del envío.
- **Apple Podcasts y Amazon Music** van siempre a `https://links.bolkana.com/podcast` (el Linktree), porque esas plataformas
  cogen el episodio del feed después de que salga en Spotify y su enlace no se conoce antes.

## 2. El texto

Estructura fija (la de la plantilla):

1. Etiqueta «THE BOLKANA PODCAST · #NN» y titular «Nuevo episodio con <Invitado>, <cargo> de <Empresa>».
2. Párrafos de Lavin en primera persona: «Hola,» → «Esta semana me senté con <Invitado>, <cargo> de <Empresa>.» → **un gancho de
   1–2 frases con el dato más llamativo** (cifras en `<strong style="font-weight:700;">`).
3. «Tres momentos de la conversación que no te puedes perder:» y **3 temas con emoji**. Cada tema **deja la intriga, no da la
   respuesta** («Por qué un inversor no quiso entrar… por ir demasiado bien», no «porque los fondos tienen objetivos de equity»).
   Uno puede llevar un toque personal de Lavin si es verdad («Se lo pregunté sin rodeos»).
4. Firma «Un abrazo, **Lavin 🌋**» (va **antes** de los botones y el volcán en la misma línea; ya lo resuelve la plantilla).
5. Botón oscuro con el logo de YouTube y banda roja «¿O prefieres escucharlo en otro lado?» con Spotify, Apple Podcasts y Amazon Music.

Reglas:
- **Breve.** Si hace falta bajar en el móvil para ver el botón de YouTube, sobra texto. Nada de lecciones largas ni capítulos
  con minutos (eso va en la descripción de YouTube o en un post de LinkedIn).
- **No inventar.** Cada cifra y cada cita, comprobada en la transcripción. Corregir lo que whisper escribe mal (la lista está en
  `EPISODIO.md`). Si una cifra no está clara (p. ej. el importe final de la ronda), preguntar.
- Si el equipo fundador es de varias personas, escribir en plural («Empezaron», «Acaban de cerrar»).
- Español de España, tono Bolkana: frases cortas, directo, nada de relleno.

**Asunto:** empieza por 🌋 y lleva el gancho más fuerte (una cifra o una contradicción). Ej.: «🌋 5.000 € de capital, cero
marketing y una ronda cerrada en una semana».
**Previsualización:** completa el asunto sin repetirlo; mejor por debajo de ~90 caracteres para que se vea entera en el móvil. Sin 🌋.

Enseña al usuario el asunto, la previsualización y el texto (en bloque citado, como se leerá) **antes** de tocar Brevo.

## 3. Maquetar

1. Escribe `newsletter.json` en la carpeta del episodio (mismos campos que el del #17: `asunto`, `preview`, `numero`, `titular`,
   `parrafos`, `intro_temas`, `temas`, `urls`, `brevo`).
2. `python3 .claude/skills/bolkana-newsletter/rellenar.py "episodios/<NN | Invitado>/newsletter.json" "episodios/<NN | Invitado>/newsletter.html"`
3. Ábrelo en el navegador integrado y revisa que se lea bien.

El diseño **se adapta al modo del lector** (claro u oscuro), como un correo normal: no tiene fondo propio y el texto cambia de
color con `prefers-color-scheme`. El usuario rechazó el fondo negro fijo y también forzar el modo claro. Si se toca la plantilla,
comprobar los dos modos (en local la vista previa siempre sale en claro: para ver el oscuro, haz una copia temporal que cambie
`@media (prefers-color-scheme: dark)` por `@media all` y ponga fondo `#121212` al `body`).

## 4. Subir a Brevo (MCP)

Las herramientas son del conector de Brevo (prefijo `mcp__<uuid>__…`); cárgalas con ToolSearch (`brevo campaign`). Solo permiten
**leer y crear** campañas: **no editan, no borran y no suben imágenes.**

1. Pide permiso al usuario antes de crear nada en Brevo (es un servicio externo).
2. `email_campaign_management_create_email_campaign` con:
   - `name`: `Podcast | <Invitado> | <Empresa> | <dd/mm/aaaa del envío>`
   - `sender`: `{"id": 1}` (Bolkana · info@bolkana.com) y `replyTo`: `info@bolkana.com`
   - `subject` y `previewText` del JSON
   - `recipients`: `{"listIds": [9, 2, 12, 11]}` (las listas de todas las newsletters del podcast)
   - `htmlContent`: el contenido **completo** de `newsletter.html`
3. Comprueba con `email_campaign_management_get_email_campaigns` (`status: "draft"`, `excludeHtmlContent: true`) que sale con el
   nombre, el asunto y las listas bien.

**Nunca enviar ni programar** (no pasar `scheduledAt`). El envío lo programa el usuario en Brevo, **1–2 horas después de que se
publique el episodio**, para que todos los enlaces funcionen.

Como el MCP no edita: cada cambio que pida el usuario es un borrador nuevo. Para no llenar Brevo de copias, si el usuario ya está
retocando la campaña en Brevo, dale el **HTML completo** en un bloque de código para que lo pegue en el editor de código, en lugar
de crear otro borrador. Si se crean varios, recuérdale cuáles borrar.

Lo que hay que decirle al usuario al terminar:
- Que se envíe una prueba y la mire en el móvil en modo claro y oscuro.
- Que confirme el nombre del remitente al programar (Brevo puede mostrar «[DEFAULT_FROM_NAME]»; debe salir «Bolkana», o
  «Lavin de Bolkana» si decide firmar como persona).
- Que compruebe el enlace de Spotify si al crear el borrador daba 404.

## Referencia

- Resultados de las newsletters anteriores del podcast (~135 contactos): 47–54 % de aperturas pero solo 10–16 personas hacen clic.
  Por eso el formato es corto y con un botón principal.
- La cabecera es el banner de Bolkana ya alojado en Brevo
  (`https://img.mailinblue.com/8232339/images/content_library/original/68d3ee8ab5223caa0e040c15.jpg`). El logo de YouTube del
  botón viene de Wikimedia; si el usuario lo sube a Brevo, cambiar la URL en `plantilla.html`.
