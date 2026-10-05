# Esquemas SVG del tema D5 (fermentaciones y aplicaciones industriales) de BioCelia.
# Uso: python tools/esquemas_tema_d5.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "d5")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, LILA, ROJO, VERDE, TEAL = "#0f4c81", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a", "#2a9d8f"


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)


def save(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def linea(x1, y1, x2, y2, col=INK, w=3, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def flecha(x1, y1, x2, y2, col=INK, w=2.5):
    return linea(x1, y1, x2, y2, col, w, 'marker-end="url(#fk)"')


def caja(x, y, w, h, t, col=PRI, fondo="#fff", size=15, sub=None):
    s = f'<rect x="{x - w / 2}" y="{y - h / 2}" width="{w}" height="{h}" rx="12" fill="{fondo}" stroke="{col}" stroke-width="2.5"/>'
    if sub:
        return s + text(x, y - 3, t, size, weight=900, fill=col) + text(x, y + 15, sub, 11.5, weight=800, fill=GRIS)
    return s + text(x, y + size * 0.35, t, size, weight=900, fill=col)


def pastilla(x, y, t, col, fondo, size=13):
    w = 14 + len(t) * size * 0.62
    return f'<rect x="{x - w / 2}" y="{y - 14}" width="{w}" height="28" rx="14" fill="{fondo}" stroke="{col}" stroke-width="2"/>' + text(x, y + 5, t, size, weight=900, fill=col)


# ---------------------------------------------------------------- rutas
def rutas():
    b = f'<rect x="10" y="10" width="1000" height="470" rx="20" fill="#fdf3e7" stroke="#2a7fc1" stroke-width="3"/>' + text(30, 40, "CITOSOL · sin oxígeno", 15, "start", 900, fill="#2a7fc1")
    b += caja(510, 80, 180, 48, "Glucosa", PRI, "#e3eef8", 18)
    b += flecha(510, 106, 510, 186, ROJO, 4) + text(524, 140, "glucólisis", 15, "start", 900, fill=ROJO)
    b += pastilla(400, 132, "+ 2 ATP", ACC, "#fff4df") + pastilla(400, 168, "2 NAD⁺ → 2 NADH", LILA, "#efe7fb", 12)
    b += caja(510, 212, 200, 48, "2 Piruvato", INK, "#fff", 18)
    # láctica
    b += flecha(420, 236, 250, 330, LILA, 3.5)
    b += caja(210, 360, 230, 54, "2 Lactato", LILA, "#efe7fb", 17, "(ácido láctico)")
    b += text(210, 410, "FERMENTACIÓN LÁCTICA", 15, weight=900, fill=LILA)
    b += text(210, 430, "bacterias lácticas, músculo,", 12, weight=800, fill=GRIS) + text(210, 446, "glóbulos rojos", 12, weight=800, fill=GRIS)
    # alcohólica
    b += flecha(600, 236, 770, 330, ACC, 3.5)
    b += caja(810, 360, 250, 54, "2 Etanol + 2 CO₂", ACC, "#fff4df", 17)
    b += text(810, 410, "FERMENTACIÓN ALCOHÓLICA", 15, weight=900, fill=ACC)
    b += text(810, 430, "levaduras (Saccharomyces)", 12, weight=800, fill=GRIS) + text(810, 446, "y algunas células vegetales", 12, weight=800, fill=GRIS)
    # NAD regenerado
    b += text(510, 300, "el NADH se oxida a NAD⁺ al reducir el piruvato:", 13, weight=900, fill=LILA)
    b += text(510, 318, "así la glucólisis puede continuar", 13, weight=900, fill=LILA)
    b += text(510, 470, "Balance: 2 ATP por glucosa (solo los de la glucólisis) · el NADH no gana nada: se regenera NAD⁺", 13, weight=800, fill=PRI)
    save("rutas-fermentacion.svg", svg(1020, 490, b, "Fermentación láctica y alcohólica a partir del piruvato"))


# ---------------------------------------------------------------- gráfica levaduras
def grafica():
    x0, y0, w, h = 90, 50, 760, 300
    b = linea(x0, y0 + h, x0 + w, y0 + h, INK, 2.5) + linea(x0, y0 + h, x0, y0 - 10, INK, 2.5)
    b += text(x0 + w / 2, y0 + h + 40, "tiempo", 15, weight=900, fill=GRIS)
    b += text(36, y0 + h / 2, "concentración", 15, weight=900, fill=GRIS, style=f'transform="rotate(-90 36 {y0 + h / 2})"')
    tc = 0.45
    def curva(f, col, et, lx, ly):
        pts = [(x0 + t * w, y0 + h - f(t) * h) for t in [k / 100 for k in range(101)]]
        return f'<polyline points="{" ".join(f"{a:.1f},{c:.1f}" for a, c in pts)}" fill="none" stroke="{col}" stroke-width="4"/>' + text(lx, ly, et, 15, "start", 900, fill=col)
    ox = lambda t: max(0.0, 0.85 * (1 - t / tc)) if t < tc else 0.0
    glu = lambda t: 0.9 - 0.25 * t / tc if t < tc else 0.65 - 0.65 * (t - tc) / (1 - tc) * 0.95
    eta = lambda t: 0.0 if t < tc else 0.7 * (1 - math.exp(-(t - tc) * 6))
    b += curva(ox, PRI, "O₂", x0 + 60, y0 + 180) + curva(glu, ACC, "glucosa", x0 + w - 120, y0 + h - 30) + curva(eta, VERDE, "etanol", x0 + w - 100, y0 + 70)
    b += linea(x0 + tc * w, y0 - 10, x0 + tc * w, y0 + h, GRIS, 1.5, 'stroke-dasharray="6 5"')
    b += text(x0 + tc * w / 2, y0 - 18, "t1: respiración celular", 15, weight=900, fill=PRI)
    b += text(x0 + tc * w + (1 - tc) * w / 2, y0 - 18, "t2: fermentación alcohólica", 15, weight=900, fill=VERDE)
    b += text(x0 + w / 2, y0 + h + 66, "Al agotarse el O₂ las levaduras fermentan: consumen la glucosa más deprisa (rinde menos) y aparece etanol.", 13, weight=800, fill=GRIS)
    save("grafica-levaduras.svg", svg(880, 440, b, "Concentración de oxígeno, glucosa y etanol en un cultivo de levaduras"))


# ---------------------------------------------------------------- aplicaciones
def aplicaciones():
    cols = [("Alcohólica · levaduras", ACC, "#fff4df", ["Pan: el CO₂ hace subir la masa", "Vino (mosto de uva), cerveza, sidra", "Vinos finos de Jerez y Montilla:", "  crianza bajo el «velo de flor»", "Bioetanol (combustible)"]),
            ("Láctica · bacterias lácticas", LILA, "#efe7fb", ["Yogur, kéfir, quesos", "Aceitunas de mesa (aderezo", "  «estilo sevillano» en salmuera)", "Encurtidos, chucrut", "Embutidos curados"]),
            ("Otras", VERDE, "#e5f4ec", ["Acética (Acetobacter): vinagre,", "  como el vinagre de Jerez", "Biogás (metano) a partir de", "  residuos agrícolas y ganaderos", "Antibióticos, enzimas, ácidos"])]
    b = ""
    for i, (t, c, f, ej) in enumerate(cols):
        x = 10 + i * 340
        b += f'<rect x="{x}" y="10" width="330" height="270" rx="16" fill="{f}" stroke="{c}" stroke-width="2.5"/>'
        b += text(x + 165, 42, t, 17, weight=900, fill=c)
        for k, e in enumerate(ej):
            b += text(x + (22 if not e.startswith("  ") else 36), 80 + k * 34, ("• " if not e.startswith("  ") else "") + e.strip(), 14, "start", 800)
    b += text(515, 310, "Andalucía: aceituna de mesa, vinos y vinagres de Jerez, Montilla-Moriles y el Condado, quesos… y valorización de residuos.", 13.5, weight=900, fill=PRI)
    save("aplicaciones-fermentacion.svg", svg(1030, 325, b, "Aplicaciones industriales de las fermentaciones, con ejemplos de Andalucía"))


if __name__ == "__main__":
    rutas(); grafica(); aplicaciones()
