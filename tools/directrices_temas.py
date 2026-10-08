# Escribe en cada tema completo (temas/<id>-<slug>.html) el recuadro «Directrices de Andalucía 2026-27»
# con el TEXTO LITERAL de todos los resultados de aprendizaje que le corresponden.
# Fuente: data/directrices-2026-27.json (extraído del PDF oficial sel_2026-2027-Orientaciones_biologia.pdf).
# Uso: python tools/directrices_temas.py            -> todos los temas
#      python tools/directrices_temas.py a3         -> solo los que empiezan por "a3"
import html, json, re, sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
DATOS = json.loads((RAIZ / "data" / "directrices-2026-27.json").read_text(encoding="utf-8"))

# Apartados de cada tema. None = todos los resultados del apartado; una lista = solo esos números
# (se indica que el resto del apartado se trata en otro tema).
TEMAS = {
    "a1": [("A.1.1", None), ("A.1.2", None), ("A.2.1", None), ("A.4.2", [2, 3])],
    "a2": [("A.3.1", None), ("A.3.5", [1]), ("A.4.2", [5])],
    "a3": [("A.3.2", None), ("A.3.5", [1]), ("A.4.2", [1, 5])],
    "a4": [("A.3.3", list(range(1, 12))), ("A.3.5", [1]), ("A.4.2", [1, 5])],
    "a5": [("A.3.3", list(range(12, 20))), ("A.4.1", [1])],
    "a6": [("A.3.4", None)],
    "a7": [("A.4.1", None), ("A.4.2", None)],
    "a8": [("A.3.5", None)],
    "b1": [("B.1.1", None), ("B.1.2", None), ("B.2.1", None), ("B.2.2", None), ("B.3.1", None),
           ("B.3.2", None), ("B.4.1", None), ("B.5.1", None), ("B.5.2", None)],
    "b2": [("B.5.3", None)],
    "b3": [("B.6.1", None), ("B.6.2", None), ("B.6.3", None)],
    "c1": [("C.1.1", None), ("C.1.2", None), ("C.2.1", None), ("C.2.2", None), ("C.3.1", None),
           ("C.3.2", None), ("C.3.3", None), ("C.4.1", None), ("C.4.2", None)],
    "c2": [("C.5", [1, 2]), ("C.6.1", None), ("C.6.2", None), ("C.6.3", None), ("C.6.4", None)],
    "c3": [("C.5", [3, 4]), ("C.7.1", None), ("C.7.2", None), ("C.7.3", None)],
    "d1": [("D.1.1", None), ("D.1.2", None), ("D.1.3", None), ("D.1.4", None)],
    "d2": [("D.2.1", None), ("D.2.2", [2]), ("D.2.3", None)],
    "d3": [("D.3.2", None), ("D.3.3", None)],
    "d4": [("D.3.1", None)],
    "d5": [("D.2.2", None), ("D.4", None)],
    "e1": [("E.2.1", None), ("E.2.2", None), ("E.2.3", None)],
    "e2": [("E.1.1", None), ("E.1.2", None), ("E.1.3", None)],
    "f1": [("F.1.1", None), ("F.1.2", None), ("F.1.3", None), ("F.2.1", None), ("F.2.2", None),
           ("F.3.1", None), ("F.3.2", None), ("F.4.1", None), ("F.4.2", None), ("F.4.3", None)],
}


def caja(tema):
    partes = ['<div class="caja directrices" id="directrices">',
              '    <span class="titulo-caja">Directrices de Andalucía 2026-27 · todo lo que entra en este tema</span>',
              '    <p class="dir-nota">Texto literal de los resultados de aprendizaje de las Directrices y Orientaciones de Biología 2026-27. '
              'Cada punto está desarrollado en estos apuntes.</p>']
    for sec, nums in TEMAS[tema]:
        items = [r for r in DATOS["resultados"] if r["sec"] == sec and (nums is None or r["n"] in nums)]
        parcial = ' <span class="dir-parcial">(solo los puntos que tratan este tema)</span>' if nums else ''
        partes.append(f'    <p class="dir-tit"><b>{sec}</b> {html.escape(DATOS["titulos"][sec])}{parcial}</p>')
        partes.append('    <ol>')
        for r in items:
            partes.append(f'      <li value="{r["n"]}">{html.escape(r["t"])}</li>')
        partes.append('    </ol>')
    partes.append('  </div>')
    return '\n'.join(partes)


def main():
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    for p in sorted((RAIZ / "temas").glob("*.html")):
        if p.stem.endswith(("-resumen", "-presentacion")) or not p.name.startswith(filtro):
            continue
        tema = p.name[:2]
        s = p.read_text(encoding="utf-8")
        sec = re.search(r'<section class="seccion[^"]*" id="pau">.*?</section>', s, re.S)
        if not sec:
            sys.exit(f"{p.name}: no encuentro la sección «pau»")
        bloque = sec.group(0)
        nuevo, n = re.subn(r'<div class="caja directrices"[^>]*>.*?\n  </div>', lambda m: caja(tema), bloque, count=1, flags=re.S)
        if n != 1:
            sys.exit(f"{p.name}: no encuentro el recuadro de directrices")
        p.write_text(s.replace(bloque, nuevo), encoding="utf-8")
        total = sum(len([r for r in DATOS["resultados"] if r["sec"] == sc and (ns is None or r["n"] in ns)]) for sc, ns in TEMAS[tema])
        print(f"ok {p.name}: {total} resultados")


if __name__ == "__main__":
    main()
