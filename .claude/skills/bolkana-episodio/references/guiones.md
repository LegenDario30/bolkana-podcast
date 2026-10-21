# Guiones: ~20 candidatos por episodio

Sustituye lo que antes hacía Gemini. Se lee la transcripción **entera** (`podcast.txt` con tiempos, y `podcast_words.json`
para las palabras exactas) en la sesión principal. No se reparte entre agentes: elegir bien exige ver el episodio completo.

## Qué es un buen clip de Bolkana

- **Se entiende sin el resto del episodio.** Si hace falta contexto previo ("como decía antes…"), no sirve o hay que
  empezar más tarde.
- **Gancho en los primeros 2–3 s:** una frase que choca, una cifra, una confesión, una opinión rotunda, una pregunta que el
  público de founders se hace. Si el gancho real está a mitad de la respuesta, se empieza ahí (o se trae delante con "…").
- **Una sola idea**, con desarrollo corto y un **cierre que remata** (frase redonda, conclusión, consejo accionable, risa).
  El clip acaba en la última palabra, sin end card.
- **Duración libre** (regla del usuario, 18-10-2026): no hay un rango fijo. Si el tema es relevante y aguanta, el clip
  puede ser largo (60 s o más); si la idea es corta, corto. Lo que manda es que no haya relleno.
- **Público:** founders y startups (fundraising, inversores, VC, equipo, salud mental del emprendedor, producto). Prima lo
  que se comparte o genera debate.
- **Variedad:** mezclar tonos (consejo práctico, confesión personal, polémica, humor, dato) y que no haya dos clips con la
  misma idea. Repartir por todo el episodio, no solo por los primeros 20 minutos.
- **Los fragmentos no tienen que ser seguidos** (regla del usuario, 18-10-2026): un clip puede juntar trozos de
  distintos momentos del episodio si suman a la misma idea (un dato de los primeros minutos que refuerza una opinión del
  final, por ejemplo). Sin límite fijo de fragmentos; cada salto tiene que entenderse sin contexto y no romper la imagen.
- Que hable sobre todo el invitado; Lavin cuando su pregunta o reacción hace de gancho o de remate.

## Dos reels fijos en todos los episodios

Además de los ~20 guiones, cada episodio lleva siempre estos dos. Van numerados detrás de los demás, entran directamente
como `elegido` y no cuentan en los 12–15 que elige el usuario:

- **Vinos de Karetta Maluca:** Lavin presenta los vinos (la causa a la que va parte del precio) y el invitado elige y coge
  su botella. Suele estar al final del episodio.
- **Pregunta de Alejandro Tagliaferro (Ibinn):** Lavin lanza la pregunta que manda Alejandro, de la agencia Ibinn, y el
  invitado responde. Se puede montar la respuesta con trozos de otros momentos si la completan.

## Proceso

1. Leer `podcast.txt` entero y marcar momentos candidatos (unos 30).
2. Quedarse con ~20, ordenados de más a menos potencial, y añadir los dos reels fijos (vinos e Ibinn).
3. Para cada uno, buscar en `podcast_words.json` la primera y la última palabra exactas (los tiempos de los briefs
   de Gemini eran aproximados; aquí ya salen exactos).
4. Escribir `guiones.md` en la raíz del episodio con el formato de abajo y registrar cada uno en el estado:
   `estado.py <ep> add NN slug=<slug> titulo="…" gancho=mm:ss dur=<s> fase=propuesto`.
5. Pasarle al usuario una tabla corta (Nº, título, duración, tono, ★ potencial) y que elija 12–15.
   Los elegidos → `fase=elegido`; el resto → `descartado` (no se borran del archivo, pueden servir más adelante).

## Formato de cada guion (`guiones.md`)

```markdown
## Clip 07: La falta de empatía inversora  ·  ★★★  ·  ~26 s  ·  tono: polémica
- **Slug:** empatia_inversora
- **Hablante:** Cristina (Lavin pregunta en el gancho)
- **Gancho** 7:14.82–7:20.88: "Mucho inversor debería haber emprendido antes…"
- **Desarrollo** 7:35.68–7:48.04: "Y el que ha emprendido … mucho más cercana"
- **Cierre** 7:53.54–8:06.14: "…son capaces de recibir un deck … de la persona"
- **Por qué funciona:** pone el foco en una queja habitual de los founders y da la vuelta al inversor; genera debate.
- **Énfasis / gráfico sugerido:** "empatía" en Lava; tarjeta de chat (inversor que no contesta), fuera de las caras.
- **Canción sugerida:** podcast (humano, cercano), desde ~5 s.
```

Los tiempos son de la transcripción (si el máster es otro encode, el offset va en `EPISODIO.md`). El "por qué funciona"
decide título, énfasis y zooms: el agente de edición lo usa tal cual.
