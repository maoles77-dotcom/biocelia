#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Decide qué figuras se publican en el sitio y qué figuras se quedan en local.

Motivo, y son dos:

1. LICENCIA. El pie del sitio declara CC BY 4.0 a nombre de la autora. Los
   exámenes y criterios oficiales de las Universidades de Andalucía son
   documentos públicos y sus figuras se pueden reutilizar citando origen, que
   es justo lo que hace el índice. Pero las presentaciones de "PAU SALVA", los
   resúmenes editoriales y el temario de terceros son obra ajena: publicarlos
   bajo esa licencia sería incoherente.

2. PESO. La aplicación se instala en el móvil y precarga sus recursos. Un
   assets/ de más de 100 MB hace la instalación inviable en datos móviles.

Grupos publicables:
  · exámenes y criterios oficiales  -> sí
  · actividades por temas           -> sí
  · figuras de los DOCX de la autora-> sí (índice aparte)

No publicables (quedan indexadas, con la ruta local, y fuera del repo):
  · RESÚMENES PAU, TEMARIO PAU, PAU SALVA y los PDF sueltos de terceros

Nada se borra: lo no publicable se mueve a _archivo/no-publicadas/ y el índice
registra dónde está y por qué, así que la decisión es reversible con una línea.

Uso:  python tools/clasificar_publicacion.py [--simular]
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_DATOS = RAIZ / "data"
DESTINO_LOCAL = RAIZ / "_archivo" / "no-publicadas"

# Prefijos de `origen.pdf` (ruta dentro de PAU 2025) que sí se publican.
PUBLICABLES = (
    "EXÁMENES AÑOS ANTERIORES/",
    "ACTIVIDADES POR TEMAS/",
)

MOTIVO = ("Material de estudio de terceros: se conserva en local e indexado, "
          "pero no se republica bajo la licencia CC BY del sitio.")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--simular", action="store_true", help="no mueve archivos")
    args = ap.parse_args()

    ruta_idx = DIR_DATOS / "figuras.json"
    if not ruta_idx.exists():
        print(f"No encuentro {ruta_idx}. Ejecuta antes tools/extraer_figuras.py")
        return 1

    idx = json.loads(ruta_idx.read_text(encoding="utf-8"))
    n_pub = n_loc = 0
    movidos = 0

    for fig in idx["figuras"]:
        pdf = fig["origen"]["pdf"]
        publicable = any(pdf.startswith(p) for p in PUBLICABLES)
        # Un sello institucional repetido en decenas de documentos no se
        # publica aunque venga de un examen oficial.
        if fig["revision"]["estado"] == "descartada-boilerplate":
            publicable = False

        fig["publicada"] = publicable
        if publicable:
            n_pub += 1
            continue

        n_loc += 1
        fig["motivo_no_publicada"] = (
            MOTIVO if not pdf.startswith(PUBLICABLES)
            else "Repetida en muchos documentos: cabecera o sello institucional."
        )

        for campo in ("archivo", "miniatura"):
            rel = fig.get(campo)
            if not rel:
                continue
            origen = RAIZ / rel
            nuevo_rel = f"_archivo/no-publicadas/{rel.removeprefix('assets/figuras/')}"
            destino = RAIZ / nuevo_rel
            if origen.exists() and not args.simular:
                destino.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(origen), str(destino))
                movidos += 1
            fig[campo] = nuevo_rel

    if not args.simular:
        idx["publicadas"] = n_pub
        idx["solo_locales"] = n_loc
        ruta_idx.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")

        # Limpiar carpetas vacías que deja el movimiento.
        base = RAIZ / "assets" / "figuras"
        for d in sorted((p for p in base.rglob("*") if p.is_dir()),
                        key=lambda p: -len(p.parts)):
            try:
                d.rmdir()
            except OSError:
                pass

    peso = sum(p.stat().st_size for p in (RAIZ / "assets").rglob("*.webp")) / 1048576 \
        if (RAIZ / "assets").exists() else 0

    print("══════════ CLASIFICACIÓN ══════════")
    print(f"{'(simulación) ' if args.simular else ''}publicables      : {n_pub}")
    print(f"{'(simulación) ' if args.simular else ''}solo locales     : {n_loc}")
    if not args.simular:
        print(f"archivos movidos : {movidos}")
        print(f"peso de assets/  : {peso:,.1f} MB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
