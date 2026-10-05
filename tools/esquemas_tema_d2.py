# Esquemas SVG del tema D2 (respiración celular) de BioCelia.
# Uso: python tools/esquemas_tema_d2.py
# Solo esquemas globales: las directrices piden sustratos, productos y localización, sin intermediarios.
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "d2")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, LILA, ROJO, VERDE, TEAL = "#0f4c81", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a", "#2a9d8f"
CITO, MATRIZ, MEMB = "#fdf3e7", "#fbe3d3", "#b5532c"


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


def pastilla(x, y, t, col, fondo):
    w = 14 + len(t) * 8.5
    return f'<rect x="{x - w / 2}" y="{y - 14}" width="{w}" height="28" rx="14" fill="{fondo}" stroke="{col}" stroke-width="2"/>' + text(x, y + 5, t, 13, weight=900, fill=col)


def carbonos(x, y, n, col):
    s = ""
    for k in range(n):
        s += f'<circle cx="{x - (n - 1) * 11 + k * 22}" cy="{y}" r="9" fill="{col}" stroke="{INK}" stroke-width="1.3"/>'
    return s


# ---------------------------------------------------------------- glucólisis
def glucolisis():
    b = f'<rect x="10" y="10" width="980" height="380" rx="20" fill="{CITO}" stroke="#2a7fc1" stroke-width="3"/>' + text(30, 40, "CITOSOL", 15, "start", 900, fill="#2a7fc1")
    b += text(160, 90, "Glucosa", 18, weight=900, fill=PRI) + carbonos(160, 120, 6, "#7fb3e6") + text(160, 150, "(6 C)", 13, weight=800, fill=GRIS)
    b += flecha(250, 120, 420, 120, INK, 3.5)
    b += text(335, 100, "fase de inversión", 13, weight=900, fill=ROJO)
    b += pastilla(335, 150, "− 2 ATP", ROJO, "#fde8e6")
    b += text(500, 90, "2 triosas", 16, weight=900, fill=PRI) + carbonos(500, 120, 3, "#7fb3e6") + carbonos(500, 150, 3, "#7fb3e6") + text(500, 180, "(2 × 3 C)", 13, weight=800, fill=GRIS)
    b += flecha(580, 135, 750, 135, INK, 3.5)
    b += text(665, 115, "fase de beneficio", 13, weight=900, fill=VERDE)
    b += pastilla(665, 165, "+ 4 ATP", VERDE, "#e5f4ec") + pastilla(665, 200, "+ 2 NADH", LILA, "#efe7fb")
    b += text(840, 90, "2 Piruvato", 18, weight=900, fill=PRI) + carbonos(840, 120, 3, "#f4a261") + carbonos(840, 150, 3, "#f4a261") + text(840, 180, "(ácido pirúvico, 2 × 3 C)", 12, weight=800, fill=GRIS)
    b += f'<rect x="120" y="250" width="760" height="110" rx="16" fill="#fff" stroke="{PRI}" stroke-width="2.5"/>'
    b += text(500, 282, "Glucosa + 2 NAD⁺ + 2 ADP + 2 Pi  →  2 Piruvato + 2 NADH + 2 H⁺ + 2 ATP + 2 H₂O", 16, weight=900, fill=PRI)
    b += text(500, 312, "Balance neto: 2 ATP (por fosforilación a nivel de sustrato) y 2 NADH", 14, weight=800, fill=INK)
    b += text(500, 338, "No necesita oxígeno: ocurre en condiciones aerobias y anaerobias, en todas las células", 13, weight=800, fill=GRIS)
    save("glucolisis.svg", svg(1000, 400, b, "Glucólisis: de una glucosa a dos piruvatos, con balance de ATP y NADH"))


def destinos():
    b = f'<rect x="10" y="10" width="1000" height="330" rx="20" fill="{CITO}" stroke="#2a7fc1" stroke-width="3"/>' + text(30, 40, "CITOSOL", 15, "start", 900, fill="#2a7fc1")
    b += f'<rect x="560" y="40" width="430" height="280" rx="60" fill="{MATRIZ}" stroke="{MEMB}" stroke-width="4"/>' + text(970, 70, "MITOCONDRIA (matriz)", 14, "end", 900, fill=MEMB)
    b += caja(150, 175, 160, 50, "Glucosa", PRI, "#e3eef8", 17)
    b += flecha(232, 175, 312, 175, ROJO, 3.5) + text(272, 162, "glucólisis", 12, weight=900, fill=ROJO)
    b += caja(400, 175, 160, 50, "2 Piruvato", INK, "#fff", 17)
    b += flecha(480, 160, 640, 110, VERDE, 3.5) + text(545, 152, "con O₂", 13, weight=900, fill=VERDE)
    b += caja(760, 110, 240, 56, "2 Acetil-CoA", INK, "#fff", 17, "+ 2 CO₂ + 2 NADH")
    b += text(760, 160, "descarboxilación oxidativa", 13, weight=900, fill=VERDE)
    b += flecha(760, 180, 760, 230, INK, 3) + caja(760, 268, 270, 52, "Ciclo de Krebs →", ROJO, "#fff", 16, "cadena respiratoria → CO₂, H₂O, mucho ATP")
    b += flecha(400, 202, 400, 262, LILA, 3.5) + text(412, 236, "sin O₂", 13, "start", 900, fill=LILA)
    b += caja(400, 296, 300, 52, "Fermentación", LILA, "#efe7fb", 16, "lactato, o etanol + CO₂; regenera el NAD⁺")
    save("destinos-piruvato.svg", svg(1020, 350, b, "Destinos del piruvato con oxígeno y sin oxígeno"))


# ---------------------------------------------------------------- Krebs
def krebs():
    cx, cy, r = 420, 280, 150
    b = f'<rect x="10" y="10" width="1000" height="540" rx="24" fill="{MATRIZ}" stroke="{MEMB}" stroke-width="3"/>' + text(30, 42, "MATRIZ MITOCONDRIAL", 15, "start", 900, fill=MEMB)
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ROJO}" stroke-width="10" opacity="0.85"/>'
    b += text(cx, cy - 8, "CICLO DE", 20, weight=900, fill=ROJO) + text(cx, cy + 20, "KREBS", 26, weight=900, fill=ROJO)
    b += text(cx, cy + 48, "(×2 por cada glucosa)", 12, weight=800, fill=GRIS)
    # entrada
    b += caja(cx, 60, 190, 50, "Acetil-CoA (2 C)", INK, "#fff", 15)
    b += flecha(cx, 86, cx, cy - r - 8, INK, 3)
    b += caja(cx - 250, cy - r + 10, 170, 50, "Oxalacético (4 C)", TEAL, "#e0f2ef", 14)
    b += flecha(cx - 165, cy - r + 10, cx - 90, cy - r + 40, TEAL, 2.5)
    b += text(cx - 250, cy - r + 52, "se regenera en cada vuelta", 11.5, weight=800, fill=TEAL)
    b += caja(cx + 250, cy - r + 10, 170, 50, "Citrato (6 C)", GRIS, "#fff", 14)
    b += flecha(cx + 70, cy - r + 10, cx + 162, cy - r + 10, GRIS, 2)
    # productos
    prods = [(cx + 200, cy + 30, "2 CO₂", GRIS, "#eef1f4"), (cx + 210, cy + 90, "3 NADH", LILA, "#efe7fb"),
             (cx + 160, cy + 150, "1 FADH₂", LILA, "#efe7fb"), (cx - 140, cy + 180, "1 GTP (= ATP)", ACC, "#fff4df")]
    for x, y, t, c, f in prods:
        b += pastilla(x, y, t, c, f)
    b += flecha(cx + r * 0.7, cy + 20, cx + 165, cy + 30, GRIS, 2) + flecha(cx + r * 0.6, cy + 70, cx + 168, cy + 88, LILA, 2)
    b += flecha(cx + r * 0.45, cy + 115, cx + 125, cy + 140, LILA, 2) + flecha(cx - r * 0.5, cy + 120, cx - 120, cy + 162, ACC, 2)
    # resumen
    b += f'<rect x="700" y="300" width="290" height="230" rx="16" fill="#fff" stroke="{PRI}" stroke-width="2.5"/>'
    lines = [("Por cada acetil-CoA:", PRI, 900), ("• oxida el grupo acetilo", INK, 800), ("  hasta 2 CO₂", INK, 800), ("• 3 NADH + 1 FADH₂", LILA, 900),
             ("  → a la cadena respiratoria", GRIS, 800), ("• 1 GTP (fosforilación", ACC, 900), ("  a nivel de sustrato)", ACC, 800), ("No usa O₂ directamente, pero", ROJO, 900), ("sin O₂ se detiene", ROJO, 900)]
    for k, (t, c, w) in enumerate(lines):
        b += text(716, 328 + k * 22, t, 13, "start", w, fill=c)
    save("ciclo-krebs.svg", svg(1020, 560, b, "Ciclo de Krebs: entradas y productos por vuelta"))


# ---------------------------------------------------------------- cadena y ATP sintasa
def cadena():
    W, H = 1100, 560
    b = f'<rect x="10" y="10" width="{W - 20}" height="150" rx="16" fill="#fdf0e6"/>' + text(30, 40, "ESPACIO INTERMEMBRANA", 15, "start", 900, fill=MEMB)
    b += f'<rect x="10" y="300" width="{W - 20}" height="{H - 310}" rx="16" fill="{MATRIZ}"/>' + text(30, H - 22, "MATRIZ", 15, "start", 900, fill=MEMB)
    # membrana interna
    for x in range(20, W - 20, 14):
        b += f'<circle cx="{x}" cy="172" r="6" fill="#f4a261"/><circle cx="{x}" cy="288" r="6" fill="#f4a261"/>'
        b += linea(x, 178, x, 225, "#e2c56a", 1.6) + linea(x, 235, x, 282, "#e2c56a", 1.6)
    b += text(W - 30, 236, "membrana interna", 13, "end", 900, fill=MEMB)
    cps = [(140, "I", 70, 150), (330, "III", 70, 130), (520, "IV", 70, 120)]
    for x, n, w, h in cps:
        b += f'<rect x="{x - w / 2}" y="{230 - h / 2}" width="{w}" height="{h}" rx="16" fill="#b9d3ee" stroke="{PRI}" stroke-width="2.5"/>' + text(x, 210, n, 22, weight=900, fill=PRI)
    b += f'<ellipse cx="236" cy="262" rx="20" ry="14" fill="#ffe08a" stroke="{ACC}" stroke-width="2"/>' + text(236, 267, "Q", 13, weight=900, fill="#8a5a00")
    b += f'<ellipse cx="425" cy="160" rx="18" ry="13" fill="#f6c3b5" stroke="{ROJO}" stroke-width="2"/>' + text(425, 165, "c", 13, weight=900, fill=ROJO)
    # electrones
    b += f'<path d="M140,270 C170,300 210,290 236,262 C262,240 300,250 330,240 C360,220 395,180 425,165 C455,175 490,210 520,240" fill="none" stroke="{LILA}" stroke-width="3.5" stroke-dasharray="7 5" marker-end="url(#fk)"/>'
    b += text(330, 330, "e⁻", 15, weight=900, fill=LILA)
    # NADH, FADH2
    b += pastilla(110, 380, "NADH", LILA, "#efe7fb") + flecha(118, 362, 136, 300, LILA, 2.5) + pastilla(110, 430, "NAD⁺ + H⁺", LILA, "#fff")
    b += pastilla(250, 400, "FADH₂", LILA, "#efe7fb") + flecha(250, 384, 238, 280, LILA, 2.5) + text(250, 438, "(entra por el", 11, weight=800, fill=GRIS) + text(250, 452, "complejo II)", 11, weight=800, fill=GRIS)
    # O2
    b += pastilla(520, 400, "½ O₂ + 2 H⁺", ROJO, "#fde8e6") + flecha(520, 384, 520, 300, ROJO, 2.5) + pastilla(520, 450, "H₂O", PRI, "#e3eef8")
    b += flecha(520, 414, 520, 434, PRI, 2)
    b += text(520, 490, "aceptor final", 12, weight=900, fill=ROJO)
    # bombeo de H+
    for x in (140, 330, 520):
        b += flecha(x, 160, x, 90, ACC, 3) + text(x + 16, 112, "H⁺", 15, "start", 900, fill=ACC)
    for k in range(10):
        b += text(160 + k * 52, 60 + (k % 2) * 16, "H⁺", 14, weight=900, fill=ACC)
    b += text(640, 36, "gradiente de protones (más H⁺ fuera)", 13, weight=900, fill=ACC)
    # ATP sintasa
    ax = 820
    b += f'<rect x="{ax - 20}" y="160" width="40" height="140" rx="10" fill="#d9c8f5" stroke="{LILA}" stroke-width="2.5"/>'
    b += f'<rect x="{ax - 8}" y="300" width="16" height="50" fill="#d9c8f5" stroke="{LILA}" stroke-width="2"/>'
    b += f'<circle cx="{ax}" cy="385" r="40" fill="#d9c8f5" stroke="{LILA}" stroke-width="2.5"/>' + text(ax, 381, "ATP", 13, weight=900, fill=LILA) + text(ax, 397, "sintasa", 13, weight=900, fill=LILA)
    b += flecha(ax, 70, ax, 330, ACC, 3.5) + text(ax + 14, 90, "H⁺", 15, "start", 900, fill=ACC)
    b += pastilla(ax + 160, 370, "ADP + Pi", ACC, "#fff") + flecha(ax + 115, 380, ax + 46, 385, ACC, 2)
    b += flecha(ax + 34, 410, ax + 110, 440, ACC, 2.5) + pastilla(ax + 150, 450, "ATP", ACC, "#fff4df")
    b += text(330, 525, "CADENA DE TRANSPORTE DE ELECTRONES", 15, weight=900, fill=PRI) + text(ax, 525, "FOSFORILACIÓN OXIDATIVA", 15, weight=900, fill=LILA)
    save("cadena-respiratoria.svg", svg(W, H, b, "Cadena de transporte de electrones y fosforilación oxidativa en la membrana mitocondrial interna"))


# ---------------------------------------------------------------- β-oxidación
def beta():
    b = f'<rect x="10" y="10" width="940" height="380" rx="20" fill="{MATRIZ}" stroke="{MEMB}" stroke-width="3"/>' + text(30, 40, "MATRIZ MITOCONDRIAL", 15, "start", 900, fill=MEMB)
    b += text(170, 80, "Ácido graso activado", 15, weight=900, fill=PRI) + text(170, 98, "(acil-CoA, n C)", 12, weight=800, fill=GRIS)
    b += carbonos(170, 130, 8, "#f4d06f") + f'<rect x="262" y="120" width="40" height="22" rx="6" fill="#e3eef8" stroke="{PRI}"/>' + text(282, 136, "CoA", 11, weight=900, fill=PRI)
    b += flecha(330, 130, 470, 130, ACC, 3.5) + text(400, 112, "una vuelta", 13, weight=900, fill=ACC)
    b += text(400, 160, "(4 reacciones)", 11.5, weight=800, fill=GRIS)
    b += carbonos(600, 110, 6, "#f4d06f") + f'<rect x="670" y="100" width="40" height="22" rx="6" fill="#e3eef8" stroke="{PRI}"/>' + text(690, 116, "CoA", 11, weight=900, fill=PRI)
    b += text(600, 90, "acil-CoA con 2 C menos", 13, weight=900, fill=PRI)
    b += carbonos(560, 170, 2, "#f4d06f") + f'<rect x="586" y="160" width="40" height="22" rx="6" fill="#e3eef8" stroke="{PRI}"/>' + text(606, 176, "CoA", 11, weight=900, fill=PRI)
    b += text(560, 206, "acetil-CoA → ciclo de Krebs", 13, weight=900, fill=ROJO)
    b += pastilla(840, 110, "1 NADH", LILA, "#efe7fb") + pastilla(840, 150, "1 FADH₂", LILA, "#efe7fb")
    b += f'<path d="M660,140 C720,280 330,290 220,165" fill="none" stroke="{ACC}" stroke-width="3" stroke-dasharray="8 6" marker-end="url(#fk)"/>'
    b += text(560, 300, "se repite hasta que todo el ácido graso se convierte en acetil-CoA", 13, weight=900, fill=ACC)
    b += f'<rect x="60" y="320" width="840" height="56" rx="14" fill="#fff" stroke="{PRI}" stroke-width="2"/>'
    b += text(480, 344, "Ácido graso de n carbonos (par): n/2 acetil-CoA, en (n/2 − 1) vueltas, con 1 NADH y 1 FADH₂ por vuelta", 13.5, weight=900, fill=PRI)
    b += text(480, 366, "Ejemplo: palmítico (16 C) → 8 acetil-CoA en 7 vueltas: 7 NADH + 7 FADH₂", 13, weight=800, fill=GRIS)
    save("beta-oxidacion.svg", svg(960, 400, b, "Beta-oxidación de los ácidos grasos en la matriz mitocondrial"))


def rendimiento():
    b = text(450, 34, "Energía obtenida de una glucosa", 18, weight=900, fill=PRI)
    x0, y0, h = 160, 70, 300
    vals = [("Fermentación", 2, "2 ATP", LILA), ("Respiración aerobia", 32, "≈ 30-38 ATP*", VERDE)]
    for k, (n, v, et, c) in enumerate(vals):
        x = x0 + 120 + k * 300
        hh = v / 34 * h
        b += f'<rect x="{x}" y="{y0 + h - hh}" width="140" height="{hh}" rx="8" fill="{c}" opacity="0.85"/>'
        b += text(x + 70, y0 + h - hh - 12, et, 18, weight=900, fill=c) + text(x + 70, y0 + h + 28, n, 16, weight=900, fill=INK)
    b += linea(x0 + 80, y0 + h, x0 + 700, y0 + h, INK, 2.5)
    b += text(450, y0 + h + 66, "Fermentación: oxidación incompleta, solo el ATP de la glucólisis. Respiración: oxidación completa a CO₂ y H₂O.", 13, weight=800, fill=GRIS)
    b += text(450, y0 + h + 88, "* Según el cálculo: los libros clásicos dan 36-38 ATP; los actuales, unos 30-32. Las directrices no piden el balance exacto.", 12, weight=800, fill=GRIS)
    save("rendimiento.svg", svg(900, 480, b, "Comparación del rendimiento energético de la fermentación y la respiración aerobia"))


if __name__ == "__main__":
    glucolisis(); destinos(); krebs(); cadena(); beta(); rendimiento()
