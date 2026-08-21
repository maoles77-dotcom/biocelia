#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Extrae las figuras de los PDF de PAU 2025 y construye el índice.

Dos modos complementarios, porque uno solo no basta:

  A · ráster incrustado   page.get_images()  -> microfotografías, imágenes
                                                pegadas en resúmenes y temario.
  B · recorte renderizado page.get_drawings() -> esquemas vectoriales de examen
                                                (mitocondria numerada, pedigrí,
                                                curva de anticuerpos...). Estos
                                                NO son imágenes incrustadas: si
                                                solo se hiciera el modo A se
                                                perderían todos.

Salidas:
  assets/figuras/<doc>/pN-XX.webp        figura publicable (máx. 1200 px)
  assets/figuras/<doc>/pN-XX.thumb.webp  miniatura (480 px)
  _archivo/originales/<doc>/pN-XX.png    original sin tocar (fuera del repo)
  data/figuras.json                      índice con procedencia verificable

Regla que gobierna todo el archivo: ningún texto se redacta. Todo lo que se
guarda en `contexto` es literal del PDF. Las descripciones se dejan a null y
las rellena una persona en la fase de revisión.

Uso:
    python tools/extraer_figuras.py                 # todos los grupos
    python tools/extraer_figuras.py --grupo examenes
    python tools/extraer_figuras.py --limite 5      # prueba rápida
"""

from __future__ import annotations

import argparse
import hashlib
import io
import json
import re
import sys
import unicodedata
from collections import defaultdict
from datetime import date
from pathlib import Path

import imagehash
import pymupdf
from PIL import Image

# ══════════════════════════════════════════════════════════════════════
#  RUTAS
# ══════════════════════════════════════════════════════════════════════

RAIZ = Path(__file__).resolve().parent.parent
FUENTE = RAIZ / "PAU 2025"
DIR_FIGURAS = RAIZ / "assets" / "figuras"
DIR_ARCHIVO = RAIZ / "_archivo" / "originales"
DIR_DATOS = RAIZ / "data"

# Grupos en orden de valor: los exámenes y las actividades son donde viven
# las figuras que acompañan a preguntas; el resto es material de estudio.
GRUPOS = {
    "examenes": ["EXÁMENES AÑOS ANTERIORES"],
    "actividades": ["ACTIVIDADES POR TEMAS"],
    "resumenes": ["RESÚMENES PAU", "TEMARIO PAU"],
    "apoyo": ["PAU SALVA"],
    "sueltos": ["."],  # PDF en la raíz de PAU 2025
}

# ══════════════════════════════════════════════════════════════════════
#  UMBRALES DE FILTRADO
#  Puntos de partida razonados; se calibran con los primeros resultados.
# ══════════════════════════════════════════════════════════════════════

LADO_MIN_PX = 120          # descarta iconos, viñetas y artefactos
RATIO_MAX = 8.0            # descarta filetes, subrayados y bordes de tabla
FRACCION_PAGINA_MAX = 0.90 # más que esto es fondo o escaneo de página entera
TINTA_MIN = 0.010          # < 1 % de píxeles no-fondo = recorte en blanco
PRIMITIVAS_MIN = 4         # un clúster con menos trazos no es una figura
HUECO_CLUSTER = 14.0       # pt: distancia a la que dos trazos son el mismo dibujo
PADDING_CLUSTER = 6.0      # pt de margen alrededor del recorte

# Tope del recorte vectorial. Sin él, la absorción de etiquetas se desborda:
# cada bloque absorbido acerca el rectángulo a más bloques y acaba tragándose
# la página entera, enunciado incluido.
FRACCION_CLUSTER_MAX = 0.55
# Solo se absorbe lo que parece una ETIQUETA de figura ("1", "Grupo 2",
# "estroma"), nunca un párrafo de enunciado.
ETIQUETA_MAX_CHARS = 45
ETIQUETA_AREA_MAX = 0.030
# Un trazo ancho y plano es un separador de apartados, no parte de un dibujo.
SEPARADOR_ANCHO = 0.70
SEPARADOR_GROSOR = 6.0
DPI_RENDER = 200
ANCHO_MAX = 1200
ANCHO_THUMB = 480
CALIDAD_WEBP = 85
CALIDAD_THUMB = 72
APARICIONES_BOILERPLATE = 10  # mismo phash en más PDF = sello institucional
MAX_FIGURAS_DOC = 120      # tope de seguridad por documento


# ══════════════════════════════════════════════════════════════════════
#  UTILIDADES
# ══════════════════════════════════════════════════════════════════════

def slug(texto: str) -> str:
    """Nombre de carpeta seguro, sin tildes ni espacios."""
    t = unicodedata.normalize("NFD", texto)
    t = "".join(c for c in t if unicodedata.category(c) != "Mn")
    t = t.lower().replace("ñ", "n")
    t = re.sub(r"[^a-z0-9]+", "-", t).strip("-")
    return re.sub(r"-{2,}", "-", t)[:70] or "doc"


def rects_solapan(a: pymupdf.Rect, b: pymupdf.Rect, hueco: float) -> bool:
    return not (
        a.x1 + hueco < b.x0 or b.x1 + hueco < a.x0
        or a.y1 + hueco < b.y0 or b.y1 + hueco < a.y0
    )


def agrupar(rects: list[pymupdf.Rect], hueco: float) -> list[tuple[pymupdf.Rect, int]]:
    """Une rectángulos próximos. Devuelve (rect_union, nº de primitivas)."""
    grupos: list[tuple[pymupdf.Rect, int]] = [(pymupdf.Rect(r), 1) for r in rects]
    cambiado = True
    while cambiado:
        cambiado = False
        salida: list[tuple[pymupdf.Rect, int]] = []
        for rect, n in grupos:
            for i, (otro, m) in enumerate(salida):
                if rects_solapan(rect, otro, hueco):
                    salida[i] = (otro | rect, m + n)
                    cambiado = True
                    break
            else:
                salida.append((rect, n))
        grupos = salida
    return grupos


def metadatos_examen(rel: Path) -> dict:
    """Año y convocatoria deducidos SOLO de la ruta y el nombre del archivo."""
    partes = [p for p in rel.parts]
    texto = " ".join(partes).lower()

    anio = None
    for p in partes:
        if re.fullmatch(r"(19|20)\d{2}", p):
            anio = int(p)
            break
    if anio is None:
        m = re.search(r"\b(20[0-2]\d)\b", rel.name)
        if m:
            anio = int(m.group(1))

    convocatoria = None
    for clave, valor in [
        ("titular", "titular"), ("suplente", "suplente"), ("suplemente", "suplente"),
        ("reserva", "reserva"), ("junio", "junio"), ("septiembre", "septiembre"),
        ("julio", "julio"), ("ordinaria", "ordinaria"), ("extraordinaria", "extraordinaria"),
        ("ord", "ordinaria"), ("extra", "extraordinaria"), ("sept", "septiembre"),
    ]:
        if clave in texto:
            convocatoria = valor
            break

    es_criterios = bool(re.search(r"criterio", texto))
    return {"anio": anio, "convocatoria": convocatoria, "es_criterios": es_criterios}


# ══════════════════════════════════════════════════════════════════════
#  CANDIDATAS POR PÁGINA
# ══════════════════════════════════════════════════════════════════════

def candidatas_raster(page: pymupdf.Page) -> list[dict]:
    """Modo A: imágenes incrustadas, con su posición en la página."""
    fuera = []
    vistos = set()
    for info in page.get_images(full=True):
        xref = info[0]
        if xref in vistos:
            continue
        vistos.add(xref)
        try:
            rects = page.get_image_rects(xref)
        except Exception:
            rects = []
        rect = rects[0] if rects else None
        fuera.append({"metodo": "raster-incrustado", "xref": xref, "rect": rect})
    return fuera


def candidatas_vectoriales(page: pymupdf.Page) -> list[dict]:
    """Modo B: clústeres de trazos vectoriales, ampliados con sus etiquetas."""
    pagina = page.rect
    area_pagina = pagina.get_area() or 1.0

    rects = []
    for d in page.get_drawings():
        r = d.get("rect")
        if r is None or r.is_empty:
            continue
        # Separadores de apartados y marcos de página: anchos y planos.
        if r.width > pagina.width * SEPARADOR_ANCHO and r.height < SEPARADOR_GROSOR:
            continue
        if r.height > pagina.height * SEPARADOR_ANCHO and r.width < SEPARADOR_GROSOR:
            continue
        if r.get_area() > area_pagina * FRACCION_CLUSTER_MAX:
            continue
        rects.append(r)

    if not rects:
        return []

    # Solo las etiquetas cortas son candidatas a formar parte de la figura.
    etiquetas = [
        pymupdf.Rect(b[:4]) for b in page.get_text("blocks")
        if b[4].strip()
        and len(b[4].strip()) <= ETIQUETA_MAX_CHARS
        and pymupdf.Rect(b[:4]).get_area() < area_pagina * ETIQUETA_AREA_MAX
    ]

    fuera = []
    for rect, n_primitivas in agrupar(rects, HUECO_CLUSTER):
        if n_primitivas < PRIMITIVAS_MIN:
            continue
        # Ampliar para abarcar las etiquetas que caen dentro: los números
        # 1, 2, 3 de los esquemas forman parte de la figura y sin ellos el
        # recorte no sirve para responder la pregunta.
        final = pymupdf.Rect(rect)
        tope = area_pagina * FRACCION_CLUSTER_MAX
        for _ in range(3):
            crecio = False
            for b in etiquetas:
                if b in final:
                    continue
                if rects_solapan(final, b, 2.0):
                    nuevo = final | b
                    if nuevo.get_area() <= tope:
                        final = nuevo
                        crecio = True
            if not crecio:
                break
        if final.get_area() > tope:
            continue
        final = (final + (-PADDING_CLUSTER, -PADDING_CLUSTER,
                          PADDING_CLUSTER, PADDING_CLUSTER)) & pagina
        fuera.append({
            "metodo": f"recorte-render@{DPI_RENDER}dpi",
            "xref": None,
            "rect": final,
            "primitivas": n_primitivas,
        })

    # Fusionar clústeres que se solapen tras la ampliación
    unidas: list[dict] = []
    for c in sorted(fuera, key=lambda x: -x["rect"].get_area()):
        if any(c["rect"] in u["rect"] for u in unidas):
            continue
        unidas.append(c)
    return unidas


# ══════════════════════════════════════════════════════════════════════
#  RASTERIZADO Y FILTROS
# ══════════════════════════════════════════════════════════════════════

def imagen_de_candidata(doc, page, cand) -> Image.Image | None:
    try:
        if cand["metodo"] == "raster-incrustado":
            bruto = doc.extract_image(cand["xref"])
            return Image.open(io.BytesIO(bruto["image"]))
        pix = page.get_pixmap(clip=cand["rect"], dpi=DPI_RENDER, alpha=False)
        return Image.open(io.BytesIO(pix.tobytes("png")))
    except Exception:
        return None


def fraccion_tinta(img: Image.Image) -> float:
    """Proporción de píxeles que no son fondo. Caza recortes en blanco."""
    g = img.convert("L").resize((96, 96))
    hist = g.histogram()
    oscuros = sum(hist[:235])
    return oscuros / float(96 * 96)


def motivo_descarte(img: Image.Image, cand: dict, page: pymupdf.Page) -> str | None:
    w, h = img.size
    if min(w, h) < LADO_MIN_PX:
        return "tamano-minimo"
    if max(w, h) / max(1, min(w, h)) > RATIO_MAX:
        return "proporcion-extrema"
    if cand.get("rect") is not None:
        area_pagina = page.rect.get_area() or 1.0
        fraccion = cand["rect"].get_area() / area_pagina
        # El recorte vectorial se mide con el tope estricto: si abarca más de
        # media página ya no es una figura, es el enunciado entero.
        limite = (FRACCION_CLUSTER_MAX if cand["metodo"].startswith("recorte")
                  else FRACCION_PAGINA_MAX)
        if fraccion > limite:
            return "pagina-completa"
    if fraccion_tinta(img) < TINTA_MIN:
        return "casi-monocromo"
    return None


def guardar(img: Image.Image, destino_webp: Path, destino_thumb: Path,
            destino_png: Path) -> tuple[int, int]:
    destino_png.parent.mkdir(parents=True, exist_ok=True)
    destino_webp.parent.mkdir(parents=True, exist_ok=True)

    rgb = img.convert("RGB")
    rgb.save(destino_png, "PNG", optimize=True)

    publicable = rgb
    if publicable.width > ANCHO_MAX:
        alto = round(publicable.height * ANCHO_MAX / publicable.width)
        publicable = publicable.resize((ANCHO_MAX, alto), Image.LANCZOS)
    publicable.save(destino_webp, "WEBP", quality=CALIDAD_WEBP, method=6)

    thumb = rgb
    if thumb.width > ANCHO_THUMB:
        alto = round(thumb.height * ANCHO_THUMB / thumb.width)
        thumb = thumb.resize((ANCHO_THUMB, alto), Image.LANCZOS)
    thumb.save(destino_thumb, "WEBP", quality=CALIDAD_THUMB, method=6)

    return publicable.size


# ══════════════════════════════════════════════════════════════════════
#  CONTEXTO LITERAL
# ══════════════════════════════════════════════════════════════════════

RE_OPCION = re.compile(r"\bOPCI[ÓO]N\s+([AB])\b", re.IGNORECASE)
RE_PREGUNTA = re.compile(r"(?m)^\s*(\d{1,2})\s*[.\-–)]\s*[-–]?\s*")

# Cabeceras y bloques de instrucciones. Son tablas vectoriales, así que el
# modo B las recorta como si fueran figuras; y como el texto cambia de un
# curso a otro ("CURSO 2009-2010"), el hash perceptual no siempre las une.
# Filtrarlas por su texto literal es determinista y no descarta nada real:
# ninguna figura de biología contiene estas frases.
FRASES_CABECERA = (
    "universidades de andalucia",
    "prueba de acceso",
    "pruebas de acceso",
    "evaluacion de bachillerato",
    "universidades publicas",
    "instrucciones:",
    "criterios especificos de correccion",
    "criterios generales de correccion",
    "duracion: una hora",
    "puntuacion maxima",
)


def _sin_tildes(t: str) -> str:
    t = unicodedata.normalize("NFD", t)
    return "".join(c for c in t if unicodedata.category(c) != "Mn").lower()


def es_cabecera(page: pymupdf.Page, rect: pymupdf.Rect | None) -> bool:
    if rect is None:
        return False
    try:
        texto = _sin_tildes(page.get_textbox(rect) or "")
    except Exception:
        return False
    return any(f in texto for f in FRASES_CABECERA)


def contexto_literal(page: pymupdf.Page, rect: pymupdf.Rect | None) -> dict:
    """Texto tal cual aparece en el PDF alrededor de la figura. Sin redactar."""
    bloques = [b for b in page.get_text("blocks") if b[4].strip()]
    bloques.sort(key=lambda b: (b[1], b[0]))
    texto_pagina = "\n".join(b[4].strip() for b in bloques)

    antes, despues = [], []
    if rect is not None:
        for b in bloques:
            if b[3] <= rect.y0 + 2:
                antes.append(b[4].strip())
            elif b[1] >= rect.y1 - 2:
                despues.append(b[4].strip())

    def recorta(trozos, n=2, largo=320):
        t = " ".join(trozos[-n:] if trozos is antes else trozos[:n])
        t = re.sub(r"\s+", " ", t).strip()
        return t[:largo] or None

    previo = " ".join(antes)
    m_op = None
    for m in RE_OPCION.finditer(previo or texto_pagina):
        m_op = m
    m_pr = None
    for m in RE_PREGUNTA.finditer(previo):
        m_pr = m

    return {
        "texto_antes": recorta(antes),
        "texto_despues": recorta(despues),
        "opcion": m_op.group(1).upper() if m_op else None,
        "pregunta_detectada": m_pr.group(1) if m_pr else None,
    }


def unidades_pregunta(doc, rel: Path, meta: dict) -> list[dict]:
    """
    Trocea el PDF en unidades de pregunta usando la estructura regular de la
    PAU (OPCIÓN A/B, numeración 1.- a 6.-). Texto siempre literal: es la
    materia prima para ampliar el banco sin inventar enunciados.
    """
    unidades = []
    for n_pag in range(doc.page_count):
        page = doc[n_pag]
        texto = page.get_text("text")
        if not texto.strip():
            continue
        opcion = None
        for m in RE_OPCION.finditer(texto):
            opcion = m.group(1).upper()

        cortes = list(RE_PREGUNTA.finditer(texto))
        if not cortes:
            continue
        for i, m in enumerate(cortes):
            ini = m.start()
            fin = cortes[i + 1].start() if i + 1 < len(cortes) else len(texto)
            cuerpo = re.sub(r"[ \t]+", " ", texto[ini:fin]).strip()
            if len(cuerpo) < 80:
                continue
            puntos = [p.replace(",", ".") for p in re.findall(r"\[\s*(\d(?:[.,]\d+)?)", cuerpo)]
            unidades.append({
                "documento": rel.as_posix(),
                "pagina": n_pag + 1,
                "anio": meta["anio"],
                "convocatoria": meta["convocatoria"],
                "es_criterios": meta["es_criterios"],
                "opcion": opcion,
                "numero": m.group(1),
                "texto_literal": cuerpo[:4000],
                "puntos_detectados": [float(p) for p in puntos],
                "verificado": False,
            })
    return unidades


# ══════════════════════════════════════════════════════════════════════
#  PROCESO
# ══════════════════════════════════════════════════════════════════════

def procesar_pdf(ruta: Path, estado: dict) -> None:
    rel = ruta.relative_to(FUENTE)
    meta = metadatos_examen(rel)
    carpeta = slug(rel.parent.as_posix() if rel.parent.as_posix() != "." else "sueltos")
    nombre_doc = slug(ruta.stem)
    sub = f"{carpeta}/{nombre_doc}" if carpeta else nombre_doc

    try:
        doc = pymupdf.open(ruta)
    except Exception as e:
        estado["ilegibles"].append({"documento": rel.as_posix(), "error": str(e)})
        return

    estado["unidades"].extend(unidades_pregunta(doc, rel, meta))

    sin_texto = 0
    n_doc = 0

    for n_pag in range(doc.page_count):
        if n_doc >= MAX_FIGURAS_DOC:
            break
        page = doc[n_pag]

        if not page.get_text("text").strip():
            sin_texto += 1

        candidatas = candidatas_raster(page) + candidatas_vectoriales(page)
        for idx, cand in enumerate(candidatas, start=1):
            if n_doc >= MAX_FIGURAS_DOC:
                break
            if es_cabecera(page, cand.get("rect")):
                estado["contadores"]["cabecera-institucional"] += 1
                continue

            img = imagen_de_candidata(doc, page, cand)
            if img is None:
                estado["contadores"]["ilegible"] += 1
                continue

            motivo = motivo_descarte(img, cand, page)
            if motivo:
                estado["contadores"][motivo] += 1
                continue

            buf = io.BytesIO()
            img.convert("RGB").save(buf, "PNG")
            sha = hashlib.sha256(buf.getvalue()).hexdigest()
            ph = str(imagehash.average_hash(img.convert("RGB"), hash_size=12))

            aparicion = {
                "pdf": rel.as_posix(),
                "pagina": n_pag + 1,
                "bbox": [round(v, 1) for v in tuple(cand["rect"])] if cand.get("rect") else None,
            }

            # Repetida: se guarda una sola vez y se anota la aparición.
            clave = estado["por_hash"].get(ph) or estado["por_sha"].get(sha)
            if clave:
                fig = estado["figuras"][clave]
                if aparicion not in fig["apariciones"]:
                    fig["apariciones"].append(aparicion)
                estado["contadores"]["duplicada"] += 1
                continue

            n_doc += 1
            fid = f"fig-{nombre_doc[:40]}-p{n_pag + 1}-{idx:02d}"
            if fid in estado["figuras"]:
                fid = f"{fid}-{len(estado['figuras'])}"

            rel_webp = f"assets/figuras/{sub}/p{n_pag + 1}-{idx:02d}.webp"
            rel_thumb = f"assets/figuras/{sub}/p{n_pag + 1}-{idx:02d}.thumb.webp"
            try:
                ancho, alto = guardar(
                    img,
                    RAIZ / rel_webp,
                    RAIZ / rel_thumb,
                    DIR_ARCHIVO / sub / f"p{n_pag + 1}-{idx:02d}.png",
                )
            except Exception as e:
                estado["contadores"]["error-guardado"] += 1
                estado["ilegibles"].append({"documento": rel.as_posix(), "error": str(e)})
                continue

            estado["figuras"][fid] = {
                "id": fid,
                "archivo": rel_webp,
                "miniatura": rel_thumb,
                "ancho": ancho,
                "alto": alto,
                "sha256": sha,
                "phash": ph,
                "metodo": cand["metodo"],
                "origen": {
                    "pdf": rel.as_posix(),
                    "pagina": n_pag + 1,
                    "bbox": aparicion["bbox"],
                    "anio": meta["anio"],
                    "convocatoria": meta["convocatoria"],
                    "es_criterios": meta["es_criterios"],
                },
                "apariciones": [aparicion],
                "contexto": contexto_literal(page, cand.get("rect")),
                "revision": {
                    "estado": "pendiente",
                    "alt": None,
                    "alt_origen": None,
                    "etiquetas": [],
                },
                "extraccion": {
                    "fecha": date.today().isoformat(),
                    "herramienta": f"pymupdf {pymupdf.__doc__.split()[1] if pymupdf.__doc__ else ''}".strip(),
                    "script": "tools/extraer_figuras.py",
                },
            }
            estado["por_hash"][ph] = fid
            estado["por_sha"][sha] = fid
            estado["contadores"]["guardada"] += 1

    if doc.page_count and sin_texto == doc.page_count:
        estado["requieren_ocr"].append({
            "documento": rel.as_posix(),
            "paginas": doc.page_count,
            "motivo": "ninguna pagina devuelve texto: probable escaneo",
        })
    doc.close()


def marcar_boilerplate(estado: dict) -> int:
    """Un mismo phash en muchos PDF distintos es un sello o logotipo."""
    n = 0
    for fig in estado["figuras"].values():
        pdfs = {a["pdf"] for a in fig["apariciones"]}
        if len(pdfs) > APARICIONES_BOILERPLATE:
            fig["revision"]["estado"] = "descartada-boilerplate"
            fig["revision"]["etiquetas"] = ["repetida-en-muchos-documentos"]
            n += 1
    return n


def escribir_salidas(estado: dict, n_boiler: int = 0) -> int:
    """
    Vuelca el índice a disco. Se llama periódicamente, no solo al final: si el
    proceso se interrumpe, las imágenes ya extraídas conservan su procedencia.
    Sin índice, un directorio lleno de recortes no sirve para nada.
    """
    DIR_DATOS.mkdir(parents=True, exist_ok=True)
    figuras = sorted(estado["figuras"].values(), key=lambda f: f["id"])

    (DIR_DATOS / "figuras.json").write_text(
        json.dumps({
            "generado": date.today().isoformat(),
            "script": "tools/extraer_figuras.py",
            "completo": estado.get("completo", False),
            "grupos_procesados": estado.get("grupos_hechos", []),
            "umbrales": {
                "lado_min_px": LADO_MIN_PX,
                "ratio_max": RATIO_MAX,
                "fraccion_pagina_max": FRACCION_PAGINA_MAX,
                "fraccion_cluster_max": FRACCION_CLUSTER_MAX,
                "tinta_min": TINTA_MIN,
                "primitivas_min": PRIMITIVAS_MIN,
                "dpi_render": DPI_RENDER,
            },
            "total": len(figuras),
            "figuras": figuras,
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    (DIR_DATOS / "unidades-pregunta.json").write_text(
        json.dumps({
            "generado": date.today().isoformat(),
            "script": "tools/extraer_figuras.py",
            "nota": "Texto literal de los PDF. Materia prima para ampliar el "
                    "banco; nada redactado.",
            "total": len(estado["unidades"]),
            "unidades": estado["unidades"],
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    (DIR_DATOS / "extraccion-informe.json").write_text(
        json.dumps({
            "generado": date.today().isoformat(),
            "completo": estado.get("completo", False),
            "grupos_procesados": estado.get("grupos_hechos", []),
            "descartes": dict(sorted(estado["contadores"].items())),
            "figuras_guardadas": len(figuras),
            "marcadas_boilerplate": n_boiler,
            "requieren_ocr": estado["requieren_ocr"],
            "ilegibles": estado["ilegibles"],
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    return len(figuras)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--grupo", choices=list(GRUPOS) + ["todos"], default="todos")
    ap.add_argument("--limite", type=int, default=0, help="máx. PDF (prueba)")
    ap.add_argument("--cada", type=int, default=25,
                    help="PDF entre puntos de guardado del índice")
    args = ap.parse_args()

    if not FUENTE.is_dir():
        print(f"No encuentro {FUENTE}", file=sys.stderr)
        return 1

    grupos = list(GRUPOS) if args.grupo == "todos" else [args.grupo]

    estado = {
        "figuras": {},
        "por_hash": {},
        "por_sha": {},
        "unidades": [],
        "requieren_ocr": [],
        "ilegibles": [],
        "contadores": defaultdict(int),
        "grupos_hechos": [],
        "completo": False,
    }

    for nombre in grupos:
        pdfs: list[Path] = []
        for prefijo in GRUPOS[nombre]:
            base = FUENTE if prefijo == "." else FUENTE / prefijo
            if not base.is_dir():
                continue
            it = base.glob("*.pdf") if prefijo == "." else base.rglob("*.pdf")
            pdfs.extend(sorted(it))
        if args.limite:
            pdfs = pdfs[: args.limite]

        print(f"\n=== {nombre}: {len(pdfs)} PDF ===", flush=True)
        for i, ruta in enumerate(pdfs, 1):
            print(f"  [{i}/{len(pdfs)}] {ruta.relative_to(FUENTE).as_posix()}", flush=True)
            try:
                procesar_pdf(ruta, estado)
            except Exception as e:  # ningún PDF roto detiene el barrido
                estado["ilegibles"].append({
                    "documento": ruta.relative_to(FUENTE).as_posix(),
                    "error": f"{type(e).__name__}: {e}",
                })
            if args.cada and i % args.cada == 0:
                n = escribir_salidas(estado)
                print(f"      · guardado parcial: {n} figuras indexadas", flush=True)

        estado["grupos_hechos"].append(nombre)
        escribir_salidas(estado)
        print(f"=== {nombre} terminado · índice guardado ===", flush=True)

    estado["completo"] = True
    n_boiler = marcar_boilerplate(estado)

    total = escribir_salidas(estado, n_boiler)

    print("\n══════════ RESUMEN ══════════")
    print(f"figuras guardadas      : {total}")
    print(f"  de ellas boilerplate : {n_boiler}")
    print(f"unidades de pregunta   : {len(estado['unidades'])}")
    print(f"PDF que requieren OCR  : {len(estado['requieren_ocr'])}")
    print(f"PDF ilegibles          : {len(estado['ilegibles'])}")
    print("descartes:")
    for k, v in sorted(estado["contadores"].items()):
        print(f"  {k:22} {v}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
