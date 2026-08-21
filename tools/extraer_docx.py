#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae las imágenes de los DOCX de PAU 2025/Preguntas PAU, con su posición
real dentro del documento.

Por qué este script importa más que el de los PDF: estos 12 documentos son
exactamente los que el campo `fuente` de preguntasjsonentrenamiento.json y
preguntasjsonsimulacro.json ya cita por nombre. El vínculo
pregunta -> documento NO hay que adivinarlo, ya está registrado.

Y hay un segundo motivo. Un DOCX no es solo un ZIP con imágenes en
word/media/: word/document.xml conserva el ORDEN del documento, con el texto
y las referencias a las imágenes intercalados. Recorriéndolo se sabe qué
párrafo precede a cada figura, así que cada imagen sale con su enunciado
literal alrededor — la misma calidad de contexto que el modo B de los PDF,
pero sin nada deducido.

Salida:
  assets/figuras/docx/<doc>/imageN.webp   (+ .thumb.webp)
  _archivo/originales/docx/<doc>/imageN.<ext>
  data/figuras-docx.json

Todo el texto guardado es literal. Nada se redacta ni se resume.
"""

from __future__ import annotations

import hashlib
import io
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
import zipfile
from datetime import date
from pathlib import Path

import imagehash
from PIL import Image

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "PAU 2025" / "Preguntas PAU"
DIR_ARCHIVO = RAIZ / "_archivo" / "originales" / "docx"
DIR_DATOS = RAIZ / "data"

LADO_MIN_PX = 120
RATIO_MAX = 8.0
TINTA_MIN = 0.010
ANCHO_MAX = 1200
ANCHO_THUMB = 480
CALIDAD_WEBP = 85
CALIDAD_THUMB = 72
CONTEXTO_LARGO = 400

EXT_VALIDAS = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tif", ".tiff", ".webp", ".emf", ".wmf"}

NS = {
    "w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main",
    "a": "http://schemas.openxmlformats.org/drawingml/2006/main",
    "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
    "v": "urn:schemas-microsoft-com:vml",
    "rel": "http://schemas.openxmlformats.org/package/2006/relationships",
}
R_EMBED = f"{{{NS['r']}}}embed"
R_ID = f"{{{NS['r']}}}id"
W_T = f"{{{NS['w']}}}t"
W_P = f"{{{NS['w']}}}p"


def slug(texto: str) -> str:
    t = unicodedata.normalize("NFD", texto)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.lower().replace("ñ", "n")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", t)[:70] or "doc"


def limpia(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


# ══════════════════════════════════════════════════════════════════════
#  RECORRIDO DEL DOCUMENTO EN ORDEN
# ══════════════════════════════════════════════════════════════════════

def mapa_relaciones(z: zipfile.ZipFile) -> dict[str, str]:
    """rId -> nombre de archivo en word/media/."""
    try:
        raiz = ET.fromstring(z.read("word/_rels/document.xml.rels"))
    except Exception:
        return {}
    mapa = {}
    for rel in raiz.findall(f"{{{NS['rel']}}}Relationship"):
        destino = rel.get("Target", "")
        if "media/" in destino:
            mapa[rel.get("Id", "")] = Path(destino).name
    return mapa


def secuencia_documento(z: zipfile.ZipFile) -> list[dict]:
    """
    Devuelve los párrafos en orden: {"texto": str, "imagenes": [media...]}.
    Es lo que permite decir qué enunciado precede a cada figura.
    """
    try:
        raiz = ET.fromstring(z.read("word/document.xml"))
    except Exception:
        return []

    rels = mapa_relaciones(z)
    parrafos = []
    for p in raiz.iter(W_P):
        texto = "".join(n.text or "" for n in p.iter(W_T))
        imagenes = []
        for blip in p.iter(f"{{{NS['a']}}}blip"):
            rid = blip.get(R_EMBED)
            if rid and rid in rels:
                imagenes.append(rels[rid])
        for vml in p.iter(f"{{{NS['v']}}}imagedata"):  # imágenes antiguas
            rid = vml.get(R_ID)
            if rid and rid in rels:
                imagenes.append(rels[rid])
        parrafos.append({"texto": limpia(texto), "imagenes": imagenes})
    return parrafos


RE_NUM = re.compile(r"^\s*(\d{1,2})\s*[.\-–)]")


def contexto_de(parrafos: list[dict], idx: int) -> dict:
    """Texto literal antes y después del párrafo que contiene la figura."""
    antes, despues = [], []
    for j in range(idx - 1, -1, -1):
        if parrafos[j]["texto"]:
            antes.insert(0, parrafos[j]["texto"])
        if sum(len(x) for x in antes) > CONTEXTO_LARGO:
            break
    for j in range(idx + 1, len(parrafos)):
        if parrafos[j]["texto"]:
            despues.append(parrafos[j]["texto"])
        if sum(len(x) for x in despues) > CONTEXTO_LARGO:
            break

    # Última numeración vista antes de la figura: "3." o "12)".
    numero = None
    for j in range(idx, -1, -1):
        m = RE_NUM.match(parrafos[j]["texto"])
        if m:
            numero = m.group(1)
            break

    return {
        "texto_antes": (" ".join(antes)[-CONTEXTO_LARGO:] or None),
        "texto_despues": (" ".join(despues)[:CONTEXTO_LARGO] or None),
        "parrafo_indice": idx,
        "numero_detectado": numero,
        "nota": "Texto literal del DOCX en orden de documento.",
    }


# ══════════════════════════════════════════════════════════════════════
#  IMAGEN
# ══════════════════════════════════════════════════════════════════════

def fraccion_tinta(img: Image.Image) -> float:
    g = img.convert("L").resize((96, 96))
    return sum(g.histogram()[:235]) / float(96 * 96)


def motivo_descarte(img: Image.Image) -> str | None:
    w, h = img.size
    if min(w, h) < LADO_MIN_PX:
        return "tamano-minimo"
    if max(w, h) / max(1, min(w, h)) > RATIO_MAX:
        return "proporcion-extrema"
    if fraccion_tinta(img) < TINTA_MIN:
        return "casi-monocromo"
    return None


def guardar(img, webp: Path, thumb: Path, original: Path, bruto: bytes):
    for p in (webp, thumb, original):
        p.parent.mkdir(parents=True, exist_ok=True)
    original.write_bytes(bruto)

    rgb = img.convert("RGB")
    pub = rgb
    if pub.width > ANCHO_MAX:
        pub = pub.resize((ANCHO_MAX, round(pub.height * ANCHO_MAX / pub.width)), Image.LANCZOS)
    pub.save(webp, "WEBP", quality=CALIDAD_WEBP, method=6)

    th = rgb
    if th.width > ANCHO_THUMB:
        th = th.resize((ANCHO_THUMB, round(th.height * ANCHO_THUMB / th.width)), Image.LANCZOS)
    th.save(thumb, "WEBP", quality=CALIDAD_THUMB, method=6)
    return pub.size


# ══════════════════════════════════════════════════════════════════════

def main() -> int:
    if not FUENTE.is_dir():
        print(f"No encuentro {FUENTE}")
        return 1

    figuras, por_hash, descartes = [], {}, {}
    docs = sorted(FUENTE.glob("*.docx"))
    print(f"=== {len(docs)} DOCX ===")

    for ruta in docs:
        nombre_doc = slug(ruta.stem)
        try:
            z = zipfile.ZipFile(ruta)
        except Exception as e:
            print(f"  {ruta.name}: ilegible ({e})")
            continue

        parrafos = secuencia_documento(z)
        # media -> primer párrafo donde aparece (el orden del documento)
        posicion: dict[str, int] = {}
        for i, p in enumerate(parrafos):
            for m in p["imagenes"]:
                posicion.setdefault(m, i)

        medias = [n for n in z.namelist()
                  if n.startswith("word/media/") and Path(n).suffix.lower() in EXT_VALIDAS]
        medias.sort(key=lambda n: posicion.get(Path(n).name, 10**6))

        n_doc = 0
        con_contexto = 0
        for nombre in medias:
            base_media = Path(nombre).name
            bruto = z.read(nombre)
            try:
                img = Image.open(io.BytesIO(bruto))
                img.load()
            except Exception:
                descartes["ilegible"] = descartes.get("ilegible", 0) + 1
                continue

            motivo = motivo_descarte(img)
            if motivo:
                descartes[motivo] = descartes.get(motivo, 0) + 1
                continue

            buf = io.BytesIO()
            img.convert("RGB").save(buf, "PNG")
            sha = hashlib.sha256(buf.getvalue()).hexdigest()
            ph = str(imagehash.average_hash(img.convert("RGB"), hash_size=12))

            idx = posicion.get(base_media)
            ctx = (contexto_de(parrafos, idx) if idx is not None else {
                "texto_antes": None, "texto_despues": None,
                "parrafo_indice": None, "numero_detectado": None,
                "nota": "La imagen está en word/media/ pero no se localiza en "
                        "document.xml: sin posición no se deduce el apartado.",
            })
            if ctx["texto_antes"]:
                con_contexto += 1

            aparicion = {"docx": ruta.name, "media": base_media, "parrafo": idx}
            if ph in por_hash:
                fig = figuras[por_hash[ph]]
                if aparicion not in fig["apariciones"]:
                    fig["apariciones"].append(aparicion)
                descartes["duplicada"] = descartes.get("duplicada", 0) + 1
                continue

            stem = Path(nombre).stem
            rel_webp = f"assets/figuras/docx/{nombre_doc}/{stem}.webp"
            rel_thumb = f"assets/figuras/docx/{nombre_doc}/{stem}.thumb.webp"
            ancho, alto = guardar(
                img, RAIZ / rel_webp, RAIZ / rel_thumb,
                DIR_ARCHIVO / nombre_doc / base_media, bruto,
            )

            por_hash[ph] = len(figuras)
            figuras.append({
                "id": f"figdocx-{nombre_doc[:40]}-{stem}",
                "archivo": rel_webp,
                "miniatura": rel_thumb,
                "ancho": ancho,
                "alto": alto,
                "sha256": sha,
                "phash": ph,
                "metodo": "docx-media",
                "origen": {
                    # El nombre coincide literalmente con el campo `fuente`
                    # de los JSON de preguntas: vínculo ya registrado.
                    "documento": f"PAU 2025/Preguntas PAU/{ruta.name}",
                    "fuente_json": ruta.name,
                    "media": base_media,
                    "parrafo": idx,
                },
                "apariciones": [aparicion],
                "contexto": ctx,
                "revision": {
                    "estado": "pendiente",
                    "alt": None,
                    "alt_origen": None,
                    "etiquetas": [],
                },
                "extraccion": {
                    "fecha": date.today().isoformat(),
                    "herramienta": "zipfile + xml.etree + pillow",
                    "script": "tools/extraer_docx.py",
                },
            })
            n_doc += 1
        z.close()
        print(f"  {ruta.name}")
        print(f"    guardadas {n_doc} de {len(medias)} · con contexto literal: {con_contexto}")

    DIR_DATOS.mkdir(parents=True, exist_ok=True)
    (DIR_DATOS / "figuras-docx.json").write_text(json.dumps({
        "generado": date.today().isoformat(),
        "script": "tools/extraer_docx.py",
        "nota": "Los nombres de documento coinciden con el campo `fuente` de "
                "preguntasjsonentrenamiento.json y preguntasjsonsimulacro.json. "
                "Todo el texto de `contexto` es literal del DOCX.",
        "total": len(figuras),
        "figuras": figuras,
    }, ensure_ascii=False, indent=2), encoding="utf-8")

    con_ctx = sum(1 for f in figuras if f["contexto"].get("texto_antes"))
    print("\n══════════ RESUMEN DOCX ══════════")
    print(f"figuras guardadas          : {len(figuras)}")
    print(f"con contexto literal        : {con_ctx}")
    print(f"sin posición en document.xml: {len(figuras) - con_ctx}")
    for k, v in sorted(descartes.items()):
        print(f"  descarte {k:20} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
