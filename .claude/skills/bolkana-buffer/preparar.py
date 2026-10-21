#!/usr/bin/env python3
"""Prepara la programación en Buffer de los clips de un episodio.

Empareja cada vídeo de la carpeta de Drive con su ficha de 06_pies-de-foto/, comprueba que el enlace de descarga
directa funciona, calcula un clip por día (mismo día en los 3 canales, a la hora del horario de Buffer de cada canal)
y deja las variables listas para pegar en `execute_mutation` (createPost), 10 posts por canal como máximo.

Uso:
  python3 preparar.py "<carpeta episodio>" <url o id carpeta Drive> <horario.json> \
      --desde 2026-10-22 [--clips 01-10] [--colaborador kompanion_hq] [--salida buffer_plan.json]

horario.json = la salida de la consulta `channels { id service postingSchedule { day times } }` de la skill
(o directamente {"channels": [...]}).
"""
import argparse, json, re, sys, urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

TZ = ZoneInfo("Europe/Madrid")
DIAS = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
FIRMA = re.compile(r"^🌋 Episodio #\d+")


def ids_drive(carpeta):
    fid = re.search(r"folders/([\w-]+)", carpeta)
    fid = fid.group(1) if fid else carpeta
    html = urllib.request.urlopen(f"https://drive.google.com/embeddedfolderview?id={fid}").read().decode()
    pares = re.findall(r'file/d/([\w-]+).*?flip-entry-title">([^<]+)', html, re.S)
    vids = {}
    for fid_, nombre in pares:
        m = re.search(r"clip_(\d+)_[\w]+", nombre)
        if m and nombre.endswith(".mp4"):
            vids[m.group(0)] = (fid_, nombre.strip())
    return vids


def url_directa(fid):
    return f"https://drive.usercontent.google.com/download?id={fid}&export=download"


def comprobar(url):
    req = urllib.request.Request(url, headers={"Range": "bytes=0-1023"})
    with urllib.request.urlopen(req) as r:
        return r.headers.get("Content-Type", "")


def leer_ficha(path):
    s = path.read_text()
    titulo = re.sub(r"^#\s*Clip\s*\d+\s*·\s*", "", s.splitlines()[0]).strip()
    bloque = re.search(r"##+ Reels[^\n]*\n+```\n(.*?)\n```", s, re.S)
    if not bloque:
        sys.exit(f"Sin bloque 'Reels / TikTok / YouTube Shorts' en {path.name}")
    texto = bloque.group(1).strip()
    if not any(FIRMA.match(l) for l in texto.splitlines()):
        print(f"AVISO: {path.name} no lleva la firma 🌋 Episodio #NN", file=sys.stderr)
    return titulo, texto


def horario(path):
    d = json.loads(Path(path).read_text())
    chans = d.get("channels") or d.get("data", {}).get("channels") or d
    out = {}
    for c in chans:
        out[c["service"]] = {
            "id": c["id"],
            "slots": {s["day"]: sorted(s["times"]) for s in c["postingSchedule"] if not s.get("paused")},
        }
    for svc in ("instagram", "tiktok", "youtube"):
        if svc not in out:
            sys.exit(f"Falta el canal {svc} en {path}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("episodio")
    ap.add_argument("drive")
    ap.add_argument("horario")
    ap.add_argument("--desde", required=True, help="primer día (YYYY-MM-DD); nunca hoy")
    ap.add_argument("--clips", help="rango NN-MM o lista NN,MM (por defecto todos los que tengan vídeo y ficha)")
    ap.add_argument("--colaborador", help="usuario de IG de la empresa del invitado, sin @")
    ap.add_argument("--salida", default="buffer_plan.json")
    a = ap.parse_args()

    ep = Path(a.episodio)
    fichas = {p.stem: p for p in (ep / "06_pies-de-foto").glob("clip_*.md")}
    vids = ids_drive(a.drive)
    claves = sorted(set(fichas) & set(vids), key=lambda k: int(k.split("_")[1]))
    sin_video = sorted(set(fichas) - set(vids))
    if sin_video:
        print("Fichas sin vídeo en Drive:", ", ".join(sin_video), file=sys.stderr)
    if a.clips:
        if "-" in a.clips:
            i, j = (int(x) for x in a.clips.split("-"))
            quiero = set(range(i, j + 1))
        else:
            quiero = {int(x) for x in a.clips.split(",")}
        claves = [k for k in claves if int(k.split("_")[1]) in quiero]
    if not claves:
        sys.exit("No hay clips que programar")

    hoy = datetime.now(TZ).date()
    d0 = date.fromisoformat(a.desde)
    if d0 <= hoy:
        sys.exit(f"--desde tiene que ser posterior a hoy ({hoy})")
    hor = horario(a.horario)
    num = re.match(r"(\d+)", ep.name)
    num = num.group(1) if num else "?"

    posts, tabla = {"instagram": [], "tiktok": [], "youtube": []}, []
    for n, k in enumerate(claves):
        dia = d0 + timedelta(days=n)
        titulo, texto = leer_ficha(fichas[k])
        fid, nombre = vids[k]
        url = url_directa(fid)
        tipo = comprobar(url)
        if "video" not in tipo:
            sys.exit(f"{k}: el enlace de Drive no da un vídeo ({tipo}). ¿Está compartido con «cualquiera con el enlace»?")
        fila = {"clip": k, "dia": dia.isoformat(), "titulo": titulo}
        for svc in ("instagram", "tiktok", "youtube"):
            slots = hor[svc]["slots"].get(DIAS[dia.weekday()])
            if not slots:
                sys.exit(f"{svc} no tiene hueco el {DIAS[dia.weekday()]}: revisa el horario en Buffer")
            hh, mm = map(int, slots[0].split(":"))
            due = datetime(dia.year, dia.month, dia.day, hh, mm, tzinfo=TZ).isoformat()
            asset = [{"video": {"url": url, "metadata": {"title": f"#{num} | {k}.mp4", "thumbnailOffset": 2000}}}]
            meta = {
                "instagram": {"instagram": {"type": "reel", "shouldShareToFeed": True,
                                            **({"collaborators": [a.colaborador]} if a.colaborador else {})}},
                "tiktok": {"tiktok": {"title": titulo}},
                "youtube": {"youtube": {"title": titulo[:100], "categoryId": "22", "privacy": "public",
                                        "notifySubscribers": False, "madeForKids": False}},
            }[svc]
            posts[svc].append({"channelId": hor[svc]["id"], "schedulingType": "automatic", "mode": "customScheduled",
                               "dueAt": due, "text": texto, "assets": asset, "metadata": meta})
            fila[svc] = slots[0]
        tabla.append(fila)

    for svc, lista in posts.items():
        if len(lista) > 10:
            sys.exit(f"{svc}: {len(lista)} posts; el plan gratuito permite 10 programados por canal. Usa --clips.")

    letras = "abcdefghij"[: len(claves)]
    mutation = ("mutation C(" + ", ".join(f"${l}: CreatePostInput!" for l in letras) + ") { "
                + " ".join(f"{l}: createPost(input: ${l}) {{ ...R }}" for l in letras)
                + " } fragment R on PostActionPayload { __typename ... on MutationError { message } "
                  "... on PostActionSuccess { post { id status dueAt } } }")
    plan = {"tabla": tabla, "lotes": {svc: {"mutation": mutation, "variables": dict(zip(letras, lista))}
                                      for svc, lista in posts.items()}}
    Path(a.salida).write_text(json.dumps(plan, ensure_ascii=False, indent=1))

    print(f"{'clip':32} {'día':11} {'IG':6} {'TikTok':6} {'YT':6}  título")
    for f in tabla:
        print(f"{f['clip']:32} {f['dia']:11} {f['instagram']:6} {f['tiktok']:6} {f['youtube']:6}  {f['titulo']}")
    print(f"\nPlan guardado en {a.salida}")


if __name__ == "__main__":
    main()
