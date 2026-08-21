#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Convierte las preguntas con figura al formato que consumen las páginas y las
deja listas para Entrenamiento y Simulacro.

Genera data/preguntas-figuras.js, un archivo JavaScript que asigna el banco a
window.BIOCELIA_FIGURAS. Se carga con <script src>, NO con fetch, y eso es
deliberado: fetch falla al abrir un HTML con doble clic (file://), así que un
JSON obligaría a levantar un servidor cada vez para trabajar en local. Con un
<script> funciona igual en el disco y en GitHub Pages.

Qué entra y qué no:
  · Solo preguntas con figura vinculada POR POSICIÓN en el documento. Ninguna
    se empareja por parecido temático.
  · Se excluyen las de troceo dudoso.
  · Si existe revision.json (exportado por tools/revisor.html), manda: lo
    descartado no entra y lo aprobado se marca como verificado.

Qué NO se inventa:
  · `imageDesc` queda a null. No hay descripción fiable de la figura y no se
    redacta una: el texto alternativo se escribe en el revisor, donde se
    guarda marcado como redacción propia.
  · `c` (criterios) queda vacío si el documento no traía solución.
  · `topic` sale del nombre del archivo de origen, que es un dato, no una
    interpretación del contenido.

Uso:  python tools/integrar_figuras.py
"""

from __future__ import annotations

import json
import re
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DIR_DATOS = RAIZ / "data"
SALIDA = DIR_DATOS / "preguntas-figuras.js"

CONFIANZA_EXCLUIDA = {"baja"}


def tema_desde_documento(nombre: str) -> str:
    """
    'B3.TEMA 11-12. METABOLISMO.docx' -> 'Tema 11-12 · Metabolismo'
    Es el propio nombre del archivo: un dato, no una lectura del contenido.
    """
    base = re.sub(r"\.docx$", "", nombre, flags=re.IGNORECASE)
    m = re.search(r"TEMA\s*([\d\s\-]+)\.?\s*(.+)$", base, flags=re.IGNORECASE)
    if m:
        num = re.sub(r"\s+", "", m.group(1)).strip(".-")
        titulo = m.group(2).strip(" .")
        return f"Tema {num} · {titulo.capitalize()}"
    return base.replace("_", " ").strip().capitalize()


def enunciado_html(p: dict) -> str:
    """Enunciado + apartados en el HTML que ya saben pintar las páginas.

    Los apartados conservan sus marcas [0,5] tal como venían en el documento:
    las páginas las detectan y las resaltan solas, así que no se añaden aparte
    para no duplicarlas."""
    partes = [f"<b>{p['enunciado']}</b>"]
    for a in p.get("apartados") or []:
        partes.append(f"{a['letra']}) {a['texto']}")
    return "<br>".join(partes)


def main() -> int:
    ruta_p = DIR_DATOS / "preguntas-docx.json"
    ruta_f = DIR_DATOS / "figuras-docx.json"
    if not (ruta_p.exists() and ruta_f.exists()):
        print("Faltan data/preguntas-docx.json o data/figuras-docx.json.")
        return 1

    preguntas = json.loads(ruta_p.read_text(encoding="utf-8"))["preguntas"]
    figuras = {f["id"]: f for f in json.loads(ruta_f.read_text(encoding="utf-8"))["figuras"]}

    # Decisiones humanas, si ya se ha revisado algo.
    decisiones: dict[str, dict] = {}
    ruta_rev = DIR_DATOS / "revision.json"
    if ruta_rev.exists():
        rev = json.loads(ruta_rev.read_text(encoding="utf-8"))
        for r in rev.get("preguntas", []):
            decisiones[r["id"]] = r
        for r in rev.get("figuras", []):
            decisiones[r["id"]] = r
        print(f"revision.json encontrado: {len(decisiones)} decisiones humanas")

    banco, motivos = [], {"sin-figura": 0, "troceo-dudoso": 0,
                          "descartada-en-revision": 0, "figura-inexistente": 0}

    for p in preguntas:
        if not p.get("imagen"):
            motivos["sin-figura"] += 1
            continue
        if p["extraccion"].get("confianza_troceo") in CONFIANZA_EXCLUIDA:
            motivos["troceo-dudoso"] += 1
            continue

        d = decisiones.get(p["id"])
        if d and d.get("estado") == "descartada":
            motivos["descartada-en-revision"] += 1
            continue

        fig = figuras.get(p["imagen"]["figura_id"])
        if not fig or not (RAIZ / fig["archivo"]).exists():
            motivos["figura-inexistente"] += 1
            continue

        d_fig = decisiones.get(fig["id"])
        if d_fig and d_fig.get("estado") == "descartada":
            motivos["descartada-en-revision"] += 1
            continue

        doc = p["fuente"]["fuente_json"]
        banco.append({
            "id": p["id"],
            "block": (d.get("bloque") if d else None) or p["bloque"],
            "topic": (d.get("tema") if d else None) or tema_desde_documento(doc),
            "isNew": True,          # lleva figura -> Parte I competencial
            "hasImg": True,
            "imgSrc": fig["archivo"],
            "imgThumb": fig["miniatura"],
            # Texto alternativo: solo si una persona lo ha escrito en el
            # revisor. Nunca generado.
            "imageDesc": (d_fig or {}).get("alt"),
            "q": enunciado_html(p),
            "c": p.get("criterios") or [],
            "f": f"Pregunta y figura transcritas de «{doc}»."
                 + (" La solución mostrada es la del propio documento."
                    if p.get("tiene_criterios") else
                    " El documento no incluía solución para esta pregunta."),
            "origen": {
                "documento": doc,
                "figura": fig["id"],
                "examen_anio": p["fuente"].get("examen_anio"),
                "verificado": bool(d and d.get("estado") == "aprobada"),
            },
        })

    DIR_DATOS.mkdir(parents=True, exist_ok=True)
    cuerpo = json.dumps(banco, ensure_ascii=False, indent=1)
    SALIDA.write_text(
        "/* ══════════════════════════════════════════════════════════════\n"
        f"   Generado por tools/integrar_figuras.py el {date.today().isoformat()}.\n"
        "   NO editar a mano: se regenera. Para cambiar una pregunta, edítala\n"
        "   en el revisor y vuelve a ejecutar el script.\n"
        f"   {len(banco)} preguntas con figura, vinculadas por posición en el\n"
        "   documento de origen.\n"
        "   ══════════════════════════════════════════════════════════════ */\n"
        f"window.BIOCELIA_FIGURAS = {cuerpo};\n",
        encoding="utf-8")

    verificadas = sum(1 for b in banco if b["origen"]["verificado"])
    con_sol = sum(1 for b in banco if b["c"])
    con_alt = sum(1 for b in banco if b["imageDesc"])
    peso = SALIDA.stat().st_size / 1024

    print("══════════ INTEGRACIÓN ══════════")
    print(f"preguntas integradas   : {len(banco)}")
    print(f"  con solución oficial : {con_sol}")
    print(f"  revisadas por persona: {verificadas}")
    print(f"  con texto alternativo: {con_alt}")
    print(f"archivo                : data/preguntas-figuras.js ({peso:,.0f} KB)")
    print("descartadas:")
    for k, v in motivos.items():
        print(f"  {k:24} {v}")
    import collections
    print("por bloque:", dict(collections.Counter(b["block"] for b in banco)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
