#!/usr/bin/env python3
"""estado.py <episode dir> [clip NN field=value ...] — read or update the episode state (estado.json) and print the table.
  estado.py ep                         → table
  estado.py ep set 03 fase=render_ok proyecto=03_clips/clip_03_x render="04_renders/final/#17 | clip_03_x.mp4"
  estado.py ep add 03 slug=x titulo="…" gancho=12:03 cierre=13:01
Phases (in order): propuesto → elegido → editando → revision → aprobado → ficha → subido. Plus "descartado".
`subido` is set only when the user says they uploaded it to Buffer / LinkedIn."""
import json, os, sys
FASES = ["propuesto", "elegido", "editando", "revision", "aprobado", "ficha", "subido", "descartado"]
ep = os.path.abspath(sys.argv[1]); p = os.path.join(ep, "estado.json")
st = json.load(open(p)) if os.path.exists(p) else {"episodio": os.path.basename(ep), "clips": {}}
if len(sys.argv) > 3 and sys.argv[2] in ("set", "add"):
    nn = sys.argv[3].zfill(2); c = st["clips"].setdefault(nn, {"fase": "propuesto"})
    for kv in sys.argv[4:]:
        k, v = kv.split("=", 1)
        if k == "fase" and v not in FASES: sys.exit(f"fase desconocida: {v} ({', '.join(FASES)})")
        c[k] = v
    json.dump(st, open(p, "w"), indent=1, ensure_ascii=False)
cnt = {f: 0 for f in FASES}
print(f"{'Nº':<4}{'fase':<12}{'slug':<28}{'gancho':<8}{'dur':<7}{'canción':<16}título")
for nn, c in sorted(st["clips"].items()):
    cnt[c.get("fase", "propuesto")] += 1
    print(f"{nn:<4}{c.get('fase',''):<12}{c.get('slug','')[:27]:<28}{c.get('gancho',''):<8}{c.get('dur',''):<7}{c.get('cancion','')[:15]:<16}{c.get('titulo','')}")
print(" · ".join(f"{f} {n}" for f, n in cnt.items() if n))
