"""Rellena plantilla.html con el newsletter.json de un episodio → HTML listo para Brevo.

Uso: python3 rellenar.py <newsletter.json> <salida.html>
Falla si queda algún {{MARCADOR}} sin rellenar (los de Brevo, con espacios, se respetan).
"""
import html, json, pathlib, re, sys

tpl = pathlib.Path(__file__).with_name("plantilla.html").read_text(encoding="utf-8")
d = json.loads(pathlib.Path(sys.argv[1]).read_text(encoding="utf-8"))

P = "margin:0 0 18px 0;color:#232323;"
parrafos = d["parrafos"]  # HTML permitido (p. ej. <strong>) para resaltar cifras
parrafos_html = "\n    ".join(
    f'<p class="tx" style="{P if i < len(parrafos) - 1 else "margin:0;color:#232323;"}">{t}</p>'
    for i, t in enumerate(parrafos))

temas_html = "".join(
    f'<tr><td width="34" valign="top" style="padding:0 0 18px 0;font-size:20px;line-height:26px;">{e}</td>'
    f'<td class="tx" valign="top" style="padding:0 0 18px 0;font-family:\'Karla\',Arial,sans-serif;font-size:17px;'
    f'line-height:26px;font-weight:400;color:#232323;">{html.escape(t)}</td></tr>'
    for e, t in d["temas"])

rep = {
    "ASUNTO": html.escape(d["asunto"]),
    "NUMERO": d["numero"],
    "TITULAR": html.escape(d["titular"]),
    "PARRAFOS": parrafos_html,
    "INTRO_TEMAS": html.escape(d.get("intro_temas", "Tres momentos de la conversación que no te puedes perder:")),
    "TEMAS": temas_html,
    "URL_YOUTUBE": d["urls"]["youtube"],
    "URL_SPOTIFY": d["urls"]["spotify"],
    "URL_APPLE": d["urls"].get("apple", "https://links.bolkana.com/podcast"),
    "URL_AMAZON": d["urls"].get("amazon", "https://links.bolkana.com/podcast"),
}
for k, v in rep.items():
    tpl = tpl.replace("{{" + k + "}}", v)

faltan = re.findall(r"\{\{[A-Z_]+\}\}", tpl)
if faltan:
    sys.exit(f"Faltan marcadores sin rellenar: {faltan}")

out = pathlib.Path(sys.argv[2])
out.write_text(tpl, encoding="utf-8")
print(out, len(tpl), "bytes")
