# Esquemas SVG del tema A7 (vitaminas y salud) de BioCelia.
# Uso: python tools/esquemas_tema_a7.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, P, d, INK, BLUE

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "a7")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO, VERDE = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)


def save(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def linea(a, b, w=2.6, col=INK, extra=""):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def gota(x, y, s=1.0, fill=BLUE):
    return (f'<path d="M{x},{y - 22 * s} C{x + 5 * s},{y - 8 * s} {x + 16 * s},{y} {x + 16 * s},{y + 9 * s} '
            f'A16,16 0 0 1 {x - 16 * s},{y + 9 * s} C{x - 16 * s},{y} {x - 5 * s},{y - 8 * s} {x},{y - 22 * s}z" fill="{fill}"/>')


# ─── 1 · Clasificación ─────────────────────────────────────────────────────
def clasificacion():
    b = ""
    for x, t, col, fondo, vits, props in (
        (200, "Hidrosolubles", BLUE, "#e3f1fb", ["C", "B₁", "B₂", "B₃", "B₉", "B₁₂"],
         ["solubles en agua", "precursoras de coenzimas", "el exceso se elimina por la orina", "hay que tomarlas a diario"]),
        (600, "Liposolubles", ACC, "#fff4df", ["A", "D", "E", "K"],
         ["solubles en grasas (lípidos)", "se absorben con las grasas", "se acumulan en hígado y tejido graso", "el exceso puede ser tóxico"])):
        b += f'<rect x="{x - 180}" y="20" width="360" height="300" rx="18" fill="{fondo}" stroke="{col}" stroke-width="3"/>'
        b += text(x, 58, t, 22, weight=900, fill=col)
        n = len(vits)
        for i, v in enumerate(vits):
            cx = x - (n - 1) * 26 + i * 52
            if col == BLUE:
                b += gota(cx, 106, 1.25, col) + text(cx, 120, v, 15, weight=900, fill="#fff")
            else:
                b += f'<circle cx="{cx}" cy="108" r="22" fill="{col}"/>' + text(cx, 115, v, 18, weight=900, fill="#fff")
        for k, p in enumerate(props):
            b += text(x, 174 + k * 32, "• " + p, 15, weight=800, fill=INK)
    b += text(400, 345, "Criterio de clasificación: su solubilidad en agua o en disolventes apolares.", 15, weight=800, fill=GRIS)
    save("clasificacion-vitaminas.svg", svg(800, 360, b, "Vitaminas hidrosolubles, C y grupo B, y liposolubles, A, D, E y K, con sus propiedades"))


# ─── 2 · Vitaminas y coenzimas ─────────────────────────────────────────────
def coenzimas():
    b = text(420, 30, "Muchas vitaminas B son precursoras de coenzimas", 18, weight=900, fill=PRI)
    filas = [("B₂ (riboflavina)", "FAD", "transporta electrones (respiración)"),
             ("B₃ (niacina)", "NAD⁺ / NADP⁺", "transporta electrones (respiración, fotosíntesis)"),
             ("B₅ (ácido pantoténico)", "coenzima A", "transporta grupos acetilo (ciclo de Krebs)")]
    for i, (v, c, f) in enumerate(filas):
        y = 80 + i * 74
        b += gota(70, y + 4, 1.0) + text(100, y + 10, v, 16, "start", 900, fill=BLUE)
        b += f'<line x1="300" y1="{y + 4}" x2="360" y2="{y + 4}" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
        b += f'<rect x="370" y="{y - 18}" width="150" height="44" rx="10" fill="#f4a261" stroke="#b5600f" stroke-width="2"/>' + text(445, y + 10, c, 16, weight=900, fill="#5a2a00")
        b += f'<line x1="530" y1="{y + 4}" x2="560" y2="{y + 4}" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
        b += text(570, y + 10, f, 14, "start", 800, fill=GRIS)
    b += text(420, 310, "Sin la vitamina no se forma la coenzima y la enzima que la necesita no funciona.", 14, weight=800, fill=ROJO)
    save("vitaminas-coenzimas.svg", svg(950, 325, b, "Las vitaminas B2, B3 y B5 son precursoras de las coenzimas FAD, NAD y coenzima A"))


# ─── 3 · Enfermedades carenciales ─────────────────────────────────────────
def carencias():
    b = ""
    items = [("C", "Escorbuto", "encías que sangran,", "mala cicatrización", BLUE),
             ("B₉", "Espina bífida", "defecto del tubo neural", "del feto (embarazo)", BLUE),
             ("B₁₂", "Anemia perniciosa", "menos glóbulos rojos", "", BLUE),
             ("A", "Ceguera nocturna", "mala visión con", "poca luz", ACC),
             ("D", "Raquitismo", "huesos blandos y", "deformados (niños)", ACC)]
    for i, (v, enf, l1, l2, col) in enumerate(items):
        cx, cy = 90 + i * 175, 90
        if i == 0:  # diente y encía con gota
            b += f'<path d="M{cx - 40},{cy + 10} Q{cx},{cy + 40} {cx + 40},{cy + 10} V{cy + 30} H{cx - 40}z" fill="#f2a7a0"/>'
            b += (f'<path d="M{cx - 22},{cy - 30} Q{cx - 24},{cy - 48} {cx - 8},{cy - 44} Q{cx},{cy - 40} {cx + 8},{cy - 44} Q{cx + 24},{cy - 48} {cx + 22},{cy - 30} '
                  f'L{cx + 16},{cy + 14} L{cx - 16},{cy + 14} Z" fill="#fff" stroke="#8a99a6" stroke-width="2.5"/>')
            b += gota(cx + 30, cy + 38, 0.55, ROJO)
        elif i == 1:  # columna con defecto
            for k in range(6):
                y = cy - 45 + k * 17
                fill = "#f2a7a0" if k == 4 else "#f3efe4"
                b += f'<rect x="{cx - 18}" y="{y}" width="36" height="13" rx="4" fill="{fill}" stroke="#a89f86" stroke-width="2"/>'
            b += f'<path d="M{cx + 22},{cy + 20} q14,0 14,-10" stroke="{ROJO}" stroke-width="3" fill="none"/>'
        elif i == 2:
            for dx, dy in ((-18, -10), (16, 6), (-4, 26)):
                b += f'<ellipse cx="{cx + dx}" cy="{cy + dy}" rx="18" ry="14" fill="#f0a8a4" stroke="#a33a36" stroke-width="2"/>'
            b += text(cx + 42, cy - 18, "↓", 26, weight=900, fill=ROJO)
        elif i == 3:  # ojo y luna
            b += f'<path d="M{cx - 44},{cy} Q{cx},{cy - 36} {cx + 44},{cy} Q{cx},{cy + 36} {cx - 44},{cy}z" fill="#fff" stroke="{INK}" stroke-width="2.5"/>'
            b += f'<circle cx="{cx}" cy="{cy}" r="15" fill="#3d5a80"/><circle cx="{cx}" cy="{cy}" r="6" fill="#111"/>'
            b += f'<path d="M{cx + 30},{cy - 50} a14,14 0 1 0 12,22 a11,11 0 1 1 -12,-22z" fill="#f7c948"/>'
        else:  # piernas arqueadas
            b += f'<path d="M{cx - 14},{cy - 50} C{cx - 40},{cy - 10} {cx - 40},{cy + 20} {cx - 18},{cy + 50}" fill="none" stroke="#a89f86" stroke-width="12" stroke-linecap="round"/>'
            b += f'<path d="M{cx + 14},{cy - 50} C{cx + 40},{cy - 10} {cx + 40},{cy + 20} {cx + 18},{cy + 50}" fill="none" stroke="#a89f86" stroke-width="12" stroke-linecap="round"/>'
        b += (gota(cx - 40, cy - 58, 0.8, col) if col == BLUE else f'<circle cx="{cx - 40}" cy="{cy - 55}" r="15" fill="{col}"/>')
        b += text(cx - 40, cy - 49, v, 12, weight=900, fill="#fff")
        b += text(cx, 172, enf, 16, weight=900, fill=PRI) + text(cx, 192, l1, 12.5, weight=800, fill=GRIS) + text(cx, 208, l2, 12.5, weight=800, fill=GRIS)
    save("carencias-vitaminas.svg", svg(880, 222, b, "Enfermedades por carencia de vitaminas: escorbuto (C), espina bífida (B9), anemia perniciosa (B12), ceguera nocturna (A) y raquitismo (D)"))


# ─── 4 · Pirámide de la dieta mediterránea ────────────────────────────────
def piramide():
    b = ""
    niveles = [("Ocasional", "carne roja, embutidos, dulces", "#e76f51"),
               ("Semanal", "pescado, legumbres, huevos, carne blanca", "#f4a261"),
               ("Diario", "frutos secos, lácteos, especias, ajo y cebolla", "#e9c46a"),
               ("En cada comida", "cereales (mejor integrales), frutas, verduras, aceite de oliva", "#8ab17d"),
               ("Base", "agua · actividad física · alimentos de temporada · comer en compañía", "#2a9d8f")]
    top, alto, W = 30, 62, 760
    cx = 420
    for i, (t, ej, col) in enumerate(niveles):
        y = top + i * alto
        w1, w2 = 120 + i * 150, 120 + (i + 1) * 150
        b += f'<path d="M{cx - w1 / 2},{y} H{cx + w1 / 2} L{cx + w2 / 2},{y + alto - 4} H{cx - w2 / 2}z" fill="{col}" stroke="#fff" stroke-width="3"/>'
        b += text(cx, y + 26, t, 16, weight=900, fill="#fff" if i in (0, 4) else INK)
        b += text(cx, y + 46, ej, 12.5, weight=800, fill="#fff" if i in (0, 4) else INK)
    b += text(cx, top + 5 * alto + 24, "Esquema basado en la pirámide de la dieta mediterránea (frecuencia de consumo).", 13, weight=700, fill=GRIS)
    save("piramide-dieta-mediterranea.svg", svg(840, top + 5 * alto + 40, b, "Pirámide de la dieta mediterránea por frecuencia de consumo"))


if __name__ == "__main__":
    for f in (clasificacion, coenzimas, carencias, piramide):
        f()
