#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae preguntas PAU completas de los DOCX de PAU 2025/Preguntas PAU.

Estos documentos tienen una estructura muy regular, y contienen mucho más de
lo que los JSON actuales aprovechan:

    BLOQUE C
    2. El siguiente esquema representa un proceso básico...  (P2 2019)
    [IMAGEN]
    a) ¿Qué estructura representa? [0,1]
    b) Indique el nombre de los compuestos A, B, C... [0,8]
    a) Membrana tilacoidal
    b) A: H2O; B: H+; C: NADP+; D: NADPH...

Es decir: enunciado, figura, apartados con puntuación, solución oficial y la
referencia al examen de origen ("P2 2019" = pregunta 2 del examen de 2019).

Este script lo transcribe. NO redacta, NO resume y NO completa:
  · Todo texto sale literal del DOCX.
  · Los puntos se leen de las marcas [0,8] que ya están escritas.
  · Si un apartado no tiene solución en el documento, queda vacío.
  · La figura se vincula solo si está en el mismo tramo del documento, con la
    posición que da document.xml — nunca por parecido temático.
  · `bloque` y `tema` se deducen del nombre del archivo y de las cabeceras
    "BLOQUE X" del propio documento; si no hay dato, queda null.

Salida: data/preguntas-docx.json  (propuestas, todas con verificado=false)

Nada de esto entra en el banco publicado sin pasar por revisión humana.
"""

from __future__ import annotations

import json
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "PAU 2025" / "Preguntas PAU"
DIR_DATOS = RAIZ / "data"

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "v": "urn:schemas-microsoft-com:vml",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
W_T = f"{{{NS['w']}}}t"
W_P = f"{{{NS['w']}}}p"
R_EMBED = f"{{{NS['r']}}}embed"
R_ID = f"{{{NS['r']}}}id"

# Bloque a partir del prefijo del nombre de archivo. Es el propio esquema de
# la autora (B1 = biomoléculas, B2 = célula...), no una interpretación.
BLOQUE_POR_PREFIJO = {
    "B1": "Biomoléculas",
    "B2": "Célula",
    "B3": "Metabolismo",
    "B4": "Genética",
    "B5": "Inmunología",
}

# Acepta "3.", "3.-", "3 .-", "3)", "3 -". El formato "N.-" es el más común en
# estos documentos y era el que rompía la frontera entre preguntas.
RE_PREGUNTA = re.compile(r"^\s*(\d{1,2})\s*[.)\-–]\s*[-–.]?\s*(?=\S)")
# El sufijo se consume completo: hay documentos que escriben "a)" y otros
# "a).-", y si no se limpia el guion queda pegado al inicio del apartado.
RE_APARTADO = re.compile(r"^\s*([a-h])\s*\)[\s.\-–]*", re.IGNORECASE)
# Separador de apartados en línea, para los enunciados que los llevan dentro
# del mismo párrafo: "a) Defina... [0,6] b) Realice... [0,5]".
RE_APARTADO_INLINE = re.compile(r"(?:^|(?<=[\s.;:\]]))([a-h])\s*\)[\s.\-–]*", re.IGNORECASE)
RE_PUNTOS = re.compile(r"\[\s*(\d(?:[.,]\d+)?)\s*(?:puntos?|p)?\s*\]", re.IGNORECASE)
RE_REF_EXAMEN = re.compile(r"\(\s*P\s*(\d{1,2})\s*[-/ ]?\s*((?:19|20)\d{2})\s*\)", re.IGNORECASE)
RE_BLOQUE_CAB = re.compile(r"^\s*BLOQUE\s+([A-F])\b", re.IGNORECASE)


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.lower().replace("ñ", "n")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", t)[:70] or "doc"


def limpia(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def mapa_relaciones(z) -> dict[str, str]:
    try:
        raiz = ET.fromstring(z.read("word/_rels/document.xml.rels"))
    except Exception:
        return {}
    return {
        rel.get("Id", ""): Path(rel.get("Target", "")).name
        for rel in raiz.findall(f"{{{NS['rel']}}}Relationship")
        if "media/" in rel.get("Target", "")
    }


def secuencia(z) -> list[dict]:
    try:
        raiz = ET.fromstring(z.read("word/document.xml"))
    except Exception:
        return []
    rels = mapa_relaciones(z)
    fuera = []
    for p in raiz.iter(W_P):
        texto = limpia("".join(n.text or "" for n in p.iter(W_T)))
        imgs = []
        for blip in p.iter(f"{{{NS['a']}}}blip"):
            rid = blip.get(R_EMBED)
            if rid in rels:
                imgs.append(rels[rid])
        for vml in p.iter(f"{{{NS['v']}}}imagedata"):
            rid = vml.get(R_ID)
            if rid in rels:
                imgs.append(rels[rid])
        fuera.append({"texto": texto, "imagenes": imgs})
    return fuera


def trocear(parrafos: list[dict]) -> list[dict]:
    """Parte el documento en tramos, uno por pregunta numerada."""
    tramos, actual, bloque_cab = [], None, None
    for i, p in enumerate(parrafos):
        t = p["texto"]
        cab = RE_BLOQUE_CAB.match(t)
        if cab and len(t) < 40:
            bloque_cab = cab.group(1).upper()
            continue
        m = RE_PREGUNTA.match(t)
        # Un número seguido de texto largo abre pregunta; "3." solo, no.
        if m and len(t) > 40:
            if actual:
                tramos.append(actual)
            actual = {
                "numero": m.group(1),
                "bloque_cabecera": bloque_cab,
                "inicio": i,
                "parrafos": [p],
            }
        elif actual:
            actual["parrafos"].append(p)
    if actual:
        tramos.append(actual)
    return tramos


def partir_apartados(texto: str) -> list[dict]:
    """Parte 'a) ... [0,6] b) ... [0,5]' en apartados, esté en uno o varios
    párrafos. Devuelve el texto literal de cada uno."""
    marcas = list(RE_APARTADO_INLINE.finditer(texto))
    fuera = []
    for i, m in enumerate(marcas):
        fin = marcas[i + 1].start() if i + 1 < len(marcas) else len(texto)
        cuerpo = limpia(texto[m.end():fin])
        if not cuerpo:
            continue
        puntos = [float(x.replace(",", ".")) for x in RE_PUNTOS.findall(cuerpo)]
        fuera.append({
            "letra": m.group(1).lower(),
            "texto": cuerpo,
            "puntos": puntos[0] if puntos else None,
        })
    return fuera


def analizar_tramo(tramo: dict) -> dict:
    """
    Separa enunciado / apartados / solución dentro de un tramo.

    El criterio NO es el orden de las series de letras, que resultó poco
    fiable: es la presencia de la puntuación entre corchetes. En estos
    documentos el enunciado siempre lleva sus [0,5] y la solución oficial
    nunca los lleva. Es un rasgo del propio documento, no una suposición.
    """
    parrafos = [p for p in tramo["parrafos"] if p["texto"] or p["imagenes"]]
    imagenes = [m for p in parrafos for m in p["imagenes"]]

    con_marca, sin_marca = [], []
    for p in parrafos:
        if not p["texto"]:
            continue
        (con_marca if RE_PUNTOS.search(p["texto"]) else sin_marca).append(p["texto"])

    # El enunciado es la cabecera del primer párrafo, hasta el primer "a)".
    primero = parrafos[0]["texto"] if parrafos else ""
    m_prim = RE_APARTADO_INLINE.search(primero)
    enunciado = limpia(primero[: m_prim.start()] if m_prim else primero)

    # Apartados: todo el texto con puntuación, venga en el mismo párrafo del
    # enunciado o en párrafos aparte.
    apartados = partir_apartados(" ".join(con_marca))

    # Solución: los párrafos con forma de apartado y sin puntuación. Se
    # descartan los que preceden al primer apartado (son enunciado suelto).
    solucion = []
    for t in sin_marca:
        m = RE_APARTADO.match(t)
        if m:
            cuerpo = limpia(t[m.end():])
            if cuerpo:
                solucion.append({"letra": m.group(1).lower(), "texto": cuerpo, "puntos": None})
        elif not apartados and not solucion and len(t) > 3 and enunciado:
            enunciado = limpia(f"{enunciado} {t}")

    ref = RE_REF_EXAMEN.search(primero)
    return {
        "enunciado": RE_REF_EXAMEN.sub("", enunciado).strip(),
        "apartados": apartados,
        "solucion": solucion,
        "imagenes": imagenes,
        "ref_pregunta": ref.group(1) if ref else None,
        "ref_anio": int(ref.group(2)) if ref else None,
        # Señal de calidad para la revisión: si las letras de los apartados no
        # forman una secuencia limpia, el troceo es dudoso.
        "secuencia_limpia": [a["letra"] for a in apartados]
                            == sorted({a["letra"] for a in apartados}),
    }


def main() -> int:
    if not FUENTE.is_dir():
        print(f"No encuentro {FUENTE}")
        return 1

    # Índice de figuras ya extraídas, para vincular por nombre de media.
    figuras_por_media: dict[tuple[str, str], str] = {}
    idx_path = DIR_DATOS / "figuras-docx.json"
    if idx_path.exists():
        for f in json.loads(idx_path.read_text(encoding="utf-8"))["figuras"]:
            figuras_por_media[(f["origen"]["fuente_json"], f["origen"]["media"])] = f["id"]

    propuestas, avisos = [], []
    docs = sorted(FUENTE.glob("*.docx"))
    print(f"=== {len(docs)} DOCX ===")

    for ruta in docs:
        prefijo = ruta.stem.split(".")[0].strip().upper()
        bloque = BLOQUE_POR_PREFIJO.get(prefijo)
        doc_slug = slug(ruta.stem)

        try:
            z = zipfile.ZipFile(ruta)
        except Exception as e:
            avisos.append({"documento": ruta.name, "error": str(e)})
            continue

        tramos = trocear(secuencia(z))
        z.close()

        n_doc = n_img = n_sol = 0
        for tramo in tramos:
            d = analizar_tramo(tramo)
            texto_tramo = " ".join(p["texto"] for p in tramo["parrafos"])
            tiene_marcas = bool(RE_PUNTOS.search(texto_tramo))

            # No todas las preguntas usan apartados con letra: hay enunciados
            # corridos con la puntuación en línea, y otros que solo traen
            # figura. Descartar por falta de "a)" perdía documentos enteros.
            if len(d["enunciado"]) < 40:
                continue
            if not (d["apartados"] or tiene_marcas or d["imagenes"]):
                continue

            fig_ids = [
                figuras_por_media[(ruta.name, m)]
                for m in d["imagenes"] if (ruta.name, m) in figuras_por_media
            ]
            total = sum(a["puntos"] for a in d["apartados"] if a["puntos"])

            # Confianza en EL TROCEO, no en la riqueza del registro. Una
            # pregunta de enunciado corrido y puntuación en línea, sin
            # apartados con letra, está perfectamente bien troceada: lo que
            # delata un mal corte es una secuencia de letras desordenada.
            if not d["secuencia_limpia"]:
                confianza = "baja"
            elif d["solucion"]:
                confianza = "alta"
            else:
                confianza = "media"

            propuestas.append({
                "id": f"docx-{doc_slug[:34]}-{tramo['numero'].zfill(2)}-{len(propuestas) + 1:03d}",
                "bloque": bloque,
                "tema": None,
                "uso": ["entrenamiento"],
                "tipo": "competencial" if fig_ids else None,
                "dificultad": None,
                "enunciado": d["enunciado"],
                "apartados": d["apartados"],
                "puntos_total": round(total, 2) if total else None,
                "criterios": [f"{s['letra']}) {s['texto']}" for s in d["solucion"]],
                "tiene_criterios": bool(d["solucion"]),
                "tip": None,
                "imagen": ({
                    "figura_id": fig_ids[0],
                    "figuras_alternativas": fig_ids[1:],
                    "descripcion": None,
                    "descripcion_origen": None,
                    "estado": "vinculada-por-posicion",
                } if fig_ids else None),
                "fuente": {
                    "documento": f"PAU 2025/Preguntas PAU/{ruta.name}",
                    "fuente_json": ruta.name,
                    "bloque_cabecera": tramo["bloque_cabecera"],
                    "numero_en_documento": tramo["numero"],
                    "examen_pregunta": d["ref_pregunta"],
                    "examen_anio": d["ref_anio"],
                    "verificado": False,
                },
                "extraccion": {
                    "fecha": date.today().isoformat(),
                    "script": "tools/extraer_preguntas_docx.py",
                    "confianza_troceo": confianza,
                    "secuencia_apartados_limpia": d["secuencia_limpia"],
                    "nota": "Transcripción literal. Requiere revisión humana "
                            "antes de publicarse.",
                },
            })
            n_doc += 1
            n_img += 1 if fig_ids else 0
            n_sol += 1 if d["solucion"] else 0

        print(f"  {ruta.name}")
        print(f"    preguntas {n_doc:3}  ·  con figura {n_img:3}  ·  con solución {n_sol:3}")

    # Deduplicado por enunciado normalizado: los 12 documentos se solapan
    # entre sí y repiten preguntas clásicas.
    def clave(p: dict) -> str:
        t = unicodedata.normalize("NFD", p["enunciado"].lower())
        t = "".join(c for c in t if unicodedata.category(c) != "Mn")
        return re.sub(r"[^a-z0-9]+", "", t)[:180]

    vistos: dict[str, dict] = {}
    orden_conf = {"alta": 0, "media": 1, "baja": 2}
    duplicadas = 0
    for p in propuestas:
        k = clave(p)
        previo = vistos.get(k)
        if previo is None:
            vistos[k] = p
            continue
        duplicadas += 1
        # Se conserva el registro más completo, no el primero que apareció.
        mejor = min(
            (previo, p),
            key=lambda x: (
                orden_conf[x["extraccion"]["confianza_troceo"]],
                0 if x["tiene_criterios"] else 1,
                0 if x["imagen"] else 1,
                -len(x["apartados"]),
            ),
        )
        if mejor is p:
            p.setdefault("fuente", {})["tambien_en"] = previo["fuente"]["fuente_json"]
            vistos[k] = p
        else:
            previo.setdefault("fuente", {})["tambien_en"] = p["fuente"]["fuente_json"]
    propuestas = list(vistos.values())
    print(f"\ndeduplicadas por enunciado: {duplicadas}")

    DIR_DATOS.mkdir(parents=True, exist_ok=True)
    (DIR_DATOS / "preguntas-docx.json").write_text(json.dumps({
        "generado": date.today().isoformat(),
        "script": "tools/extraer_preguntas_docx.py",
        "nota": "PROPUESTAS, no banco publicable. Todo el texto es literal del "
                "DOCX; los puntos vienen de las marcas [0,8] ya escritas. "
                "Ninguna entra en la aplicación sin revisión humana.",
        "total": len(propuestas),
        "preguntas": propuestas,
        "avisos": avisos,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    con_fig = sum(1 for p in propuestas if p["imagen"])
    con_sol = sum(1 for p in propuestas if p["tiene_criterios"])
    con_ref = sum(1 for p in propuestas if p["fuente"]["examen_anio"])
    print("\n══════════ RESUMEN ══════════")
    print(f"preguntas transcritas    : {len(propuestas)}")
    print(f"  con figura vinculada   : {con_fig}")
    print(f"  con solución oficial   : {con_sol}")
    print(f"  con año de examen      : {con_ref}")
    for nivel in ("alta", "media", "baja"):
        n = sum(1 for p in propuestas
                if p["extraccion"]["confianza_troceo"] == nivel)
        print(f"  confianza {nivel:6}       : {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
