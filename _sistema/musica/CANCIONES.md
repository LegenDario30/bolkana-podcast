# Biblioteca de música (sin copyright)

Las canciones son de fondo. Deben quedar a unos **20 dB por debajo de la voz**, sutiles y nunca protagonistas.

Ninguna tiene voz ni letra (comprobado con whisper). El carácter de cada una se ha deducido de su análisis: tempo, tonalidad, brillo, percusión y evolución de la energía. Los datos están en `analisis.json`, que genera `music_analyze.py` (skill bolkana-podcast-vertical-clip). Hay que volver a ejecutarlo si se añaden canciones. Cada tramo se recorta con `bgmcut.py`, que lo ajusta al golpe de ritmo más cercano.

| Canción | Dur. | Tempo / tono | Carácter | Usar para | Tramos útiles |
|---|---|---|---|---|---|
| **Dagored – Midnight Velvet** | 2:00 | ~76 BPM (half-time) · La menor | Nocturna, aterciopelada, grave, algo tensa | Temas serios o introspectivos: riesgo, presión, dudas | 0–15 s es una intro suave que crece (buena para un arco hacia el clímax). Cuerpo en 15–50 s y 60–100 s |
| **NVL8 – Enough** | 2:30 | ~76 BPM · Fa mayor | Lenta, cálida, emocional, mucho grave | Reflexión, vulnerabilidad, aprendizaje personal, desgaste | Los primeros ~12 s son casi silencio, **empezar a partir de 15 s**. Estable en 15–135 s |
| **Walen – The Choice** | 2:09 | ~112 BPM · Re mayor | Pads densos y constantes, poca percusión, inspiradora | Propósito, decisiones, cambio de rumbo | Plana de principio a fin, vale cualquier tramo. Pesa en medios, así que mejor a volumen bajo |
| **prettyjohn1 – chill** | 1:29 | ~92 BPM · Do mayor | Beat chill hip-hop, relajado y seguro | Consejos con tono distendido, anécdotas | 0–40 s y 60–85 s. En 40–60 s hay un parón |
| **prettyjohn1 – funk** | 0:56 | ~117 BPM · Fa mayor | Funky, brillante, festiva | Contenido ligero o divertido. **No encaja con temas serios** | 0–48 s |
| **prettyjohn1 – instagram reel** | 0:41 | ~96 BPM · Sol menor | Beat de reel, con pulso marcado y algo de tensión | Ritmo ágil: abrumarse, mucha información, dinamismo | Solo 0–30 s (después se apaga). Para clips de ≤30 s |
| **prettyjohn1 – podcast** | 1:09 | ~92 BPM · Do mayor | Amable, "de podcast", luminosa | Temas humanos y cercanos: empatía, relaciones | Empezar en ~5 s. Estable en 5–45 s |
| **the_mountain – podcast music** | 1:26 | ~117 BPM · Do mayor | Corporativa, optimista y con energía, muy brillante | Motivación, mentalidad, energía | 10–75 s. Es la más brillante (agudos), así que volumen bajo |

## Asignaciones

### #16 · Cristina Guzman (2026-10-05)

| Clip | Canción | Desde | Volumen |
|---|---|---|---|
| 01 ghosting | chill | 0.0 s | 0.22 |
| 02 mentalidad | the_mountain | 9.6 s | 0.28 |
| 03 desaprender | Enough | 15.8 s | 0.19 |
| 04 40kg | Midnight Velvet | 60.0 s | 0.18 |
| 05 impostor | Midnight Velvet | 0.0 s | 0.22 |
| 06 vc_abrumador | instagram reel | 0.0 s | 0.19 |
| 07 empatía inversora | podcast | 5.8 s | 0.22 |
| 08 agotamiento | Enough | 84.2 s | 0.22 |
| 09 razones equivocadas | The Choice | 0.0 s | 0.22 |
| 10 filtro del no | chill | 11.1 s | 0.22 |

### #17 · Kompanion (2026-10-18)

| Clip | Canción | Desde | Volumen |
|---|---|---|---|
| 01 cinco_mil (v2, épica) | Midnight Velvet | 7.15 s | 0.28 |
| 02 vende_antes | the_mountain | 9.6 s | 0.28 |
| 03 equity_objetivos | Midnight Velvet | 15.2 s | 0.25 |
| 04 le_da_igual | instagram reel | 0.0 s | 0.24 |
| 05 ia_asesoria | The Choice | 0.0 s | 0.185 |
| 06 diez_administrativos | chill | 8.5 s | 0.22 |
| 07 generacion_jubila (v2) | Enough | 84.2 s | 0.24 |
| 08 chatgpt_marketing | funk | 0.0 s | 0.22 |
| 09 cto_confianza | podcast | 5.85 s | 0.22 |
| 10 espana_pequena | Midnight Velvet | 60.0 s | 0.28 |
| 11 plan_financiero | Enough | 19.8 s | 0.28 |
| 12 cafe_desconocido | funk | 20.0 s | 0.27 |
| 16 dejar_el_curro | The Choice | 60.0 s | 0.195 |
| 15 ronda_una_semana | instagram reel | 0.0 s | 0.26 |
| 19 sin_prisa | Enough | 99.1 s | 0.24 |
| 21 vino_karetta | The Choice | 29.4 s | 0.20 |
| 22 pregunta_ibinn | the_mountain | 20.8 s | 0.18 |
