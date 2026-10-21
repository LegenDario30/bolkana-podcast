---
name: "bolkana-pies-de-foto"
description: "Genera pies de foto para los vídeos cortos del podcast Bolkana (Reels, TikTok, LinkedIn) a partir de la transcripción del clip, nº de episodio e invitado."
---

# Pies de foto Bolkana

Crea pies de foto para los clips cortos del podcast Bolkana. Respuestas breves y directamente usables, sin explicaciones largas.

## Datos necesarios

Si falta alguno, pídelo antes de generar:
1. Transcripción o texto del clip (con marcas de tiempo si las hay)
2. Número de episodio
3. Nombre del invitado, cargo y empresa

Si el usuario da un hashtag de tema, úsalo. Si no, elígelo según el contenido de la transcripción.

## Proceso

1. **Limpia la transcripción:** corrige errores de transcripción automática (p. ej. "gosting" → "ghosting") en todas las versiones.
2. **Genera 3 opciones de frase clave** con ángulos distintos:
   - Cita directa del invitado (la más compartible)
   - Idea reformulada como afirmación
   - Pregunta o gancho que invite al debate
3. **Revisa con rúbrica** y señala la favorita en una línea: gancho en la primera línea, claridad, fuerza de la cita, tono, encaje con la plataforma.
4. **Entrega dos versiones** con la favorita:
   - **Reels / TikTok:** corta.
   - **LinkedIn:** algo más sobria, con una frase de contexto y una pregunta final para generar comentarios.

## Formato

```
[Frase clave]

🌋 Episodio #[nº] con [Invitado], [Cargo] en [Empresa].

#Bolkana #[Tema]
```

## Reglas

- 🌋 es la firma fija de marca (viene del nombre Bolkana). Va delante de la línea del episodio, en todas las redes.
- Emojis: pocos y con intención. En LinkedIn, solo el 🌋 como único emoji (opcionalmente uno de tema en la frase si encaja de forma natural). En Reels/TikTok, máximo un emoji adicional de tema.
- Hashtags: siempre #Bolkana + un hashtag de tema (por ejemplo #Fundraising). No añadir más salvo petición.
- Idioma: español.
- Tres opciones bastan; no generar cinco.
- El cargo va como "[Cargo] en [Empresa]" (p. ej. "Fundador en Kompanion").
- Si el usuario elige y mezcla opciones, aplica su mezcla respetando el orden que pida y mantén el Reels corto (frase clave + una línea) y el LinkedIn con frase de contexto y pregunta final.
- **Reels de patrocinadores / marcas fijas (Ibinn, Karetta Maluca):** da más bombo. Tras la frase clave, añade un párrafo breve que presente a la marca (qué es, dónde, tamaño) y, para Ibinn, web y Instagram. Ejemplo: "El patrocinador de nuestro podcast, Ibinn, propone esta pregunta a [invitado]: …". Usa solo datos verificados (la web oficial o lo dicho en el episodio); si falta alguno, pregúntalo.
  - Ibinn: consultora y agencia de marketing digital de Alicante, más de 45 personas. Web ibinn.com · Instagram @ibinn.group. Su socio Alejandro Tagliaferro lanza una pregunta en cada episodio.
  - Karetta Maluca: parte del precio de cada botella va a proteger animales en peligro de extinción.
- En los clips de un episodio, no nombres fondos o empresas que whisper transcriba mal sin confirmarlos con el usuario (p. ej. JME Ventures).
- Entrega: una ficha por clip en `06_pies-de-foto/clip_NN_<slug>.md` más un `_TODOS_los_pies.md` con todo junto para poder leerlo de una vez.
- Termina preguntando si se cambia algo o se pasa al siguiente clip.

## Ejemplo (Episodio #16, Cristina Guzman, Principal en SparkFood)

Reels / TikTok:
```
"Si te hacen ghosting, next." 👻

🌋 Episodio #16 con Cristina Guzman, Principal en SparkFood.

#Bolkana #Fundraising
```

LinkedIn:
```
"Si te hacen ghosting, next." Un inversor que deja de contestar no merece estar en tu radar.

¿Qué opináis: se puede volver a confiar en un fondo que desapareció y luego regresa?

🌋 Episodio #16 con Cristina Guzman, Principal en SparkFood.

#Bolkana #Fundraising
```