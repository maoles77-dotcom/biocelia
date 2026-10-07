# Esquemas SVG del tema A6 (ácidos nucleicos) de BioCelia.
# Uso: python tools/esquemas_tema_a6.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, P, d, INK, BLUE

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "a6")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO, VERDE = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"
COL_BASE = {"A": "#e76f51", "T": "#2a9d8f", "U": "#8ab17d", "G": "#264653", "C": "#e9c46a"}
FOSF, FOSF_S = "#f7c948", "#8a6d00"
AZ, AZ_S = "#f6c3b5", "#b5533c"


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)


def save(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def linea(a, b, w=2.6, col=INK, extra=""):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def poligono(cx, cy, r, n, rot, fill, st, w=2.5):
    pts = " ".join(f"{cx + r * math.cos(math.radians(rot + 360 / n * k)):.1f},{cy + r * math.sin(math.radians(rot + 360 / n * k)):.1f}" for k in range(n))
    return f'<polygon points="{pts}" fill="{fill}" stroke="{st}" stroke-width="{w}"/>'


def fosfato(x, y, r=20):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{FOSF}" stroke="{FOSF_S}" stroke-width="2.5"/>' + text(x, y + r * 0.3, "P", r * 0.9, weight=900, fill="#6b5000")


def base_n(x, y, letra, r=24, et=True):
    col = COL_BASE[letra]
    tc = "#fff" if letra in "AGT" else INK
    if letra in "AG":  # púrica: dos anillos
        s = poligono(x - r * 0.42, y, r * 0.62, 6, 30, col, INK, 2) + poligono(x + r * 0.62, y, r * 0.55, 5, 0, col, INK, 2)
    else:
        s = poligono(x, y, r * 0.72, 6, 30, col, INK, 2)
    if et:
        s += text(x - (r * 0.42 if letra in "AG" else 0), y + 6, letra, r * 0.7, weight=900, fill=tc)
    return s


# ─── 1 · Nucleótido ────────────────────────────────────────────────────────
def nucleotido():
    b = ""
    cx, cy, r = 300, 160, 48
    # pentosa (pentágono con O arriba)
    ang = [-90 + 72 * k for k in range(5)]
    v = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in ang]
    b += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in v)}" fill="{AZ}" stroke="{AZ_S}" stroke-width="3"/>'
    b += f'<circle cx="{v[0][0]:.1f}" cy="{v[0][1]:.1f}" r="10" fill="#fff"/>' + text(v[0][0], v[0][1] + 5, "O", 15, weight=900, fill=ROJO)
    etq = {1: "1′", 2: "2′", 3: "3′", 4: "4′"}
    pos = {1: v[1], 2: v[2], 3: v[3], 4: v[4]}
    for k, p in pos.items():
        dx = 16 if p[0] > cx else -16
        dy = 20 if k in (1, 4) else (16 if p[1] > cy else -6)  # 1′ y 4′ debajo del vértice, lejos de los enlaces
        b += text(p[0] + dx, p[1] + dy, etq[k], 13, weight=900, fill=LILA)
    # C5' y fosfato
    c5 = (v[4][0] - 30, v[4][1] - 34)
    b += linea(v[4], c5, 3) + text(c5[0] + 24, c5[1] + 12, "C5′", 13, weight=900, fill=LILA)
    b += linea(c5, (150, c5[1]), 3) + fosfato(130, c5[1], 24)
    b += text(190, c5[1] - 30, "enlace éster", 13, weight=900, fill=ACC) + text(190, c5[1] - 14, "(fosfoéster)", 12, weight=800, fill=ACC)
    # base en C1'
    bpos = (480, v[1][1])
    b += linea(v[1], (bpos[0] - 40, bpos[1]), 3) + base_n(bpos[0], bpos[1], "A", 40)
    b += text(400, bpos[1] - 34, "enlace", 13, weight=900, fill=ACC) + text(400, bpos[1] - 18, "N-glucosídico", 13, weight=900, fill=ACC)
    # OH en 2' y 3'
    p2, p3 = v[2], v[3]
    b += linea(p2, (p2[0], p2[1] + 30), 2.4) + text(p2[0], p2[1] + 46, "OH / H", 14, weight=900, fill=ROJO)
    b += linea(p3, (p3[0], p3[1] + 30), 2.4) + text(p3[0], p3[1] + 46, "OH", 14, weight=900, fill=ROJO)
    b += text(p2[0] + 4, p2[1] + 66, "ribosa / desoxirribosa", 12, weight=800, fill=GRIS)
    # llaves
    b += f'<path d="M260,300 H560" stroke="{TEAL}" stroke-width="3" fill="none"/>' + text(410, 322, "nucleósido = pentosa + base", 15, weight=900, fill=TEAL)
    b += f'<path d="M100,350 H560" stroke="{PRI}" stroke-width="3" fill="none"/>' + text(330, 372, "nucleótido = fosfato + pentosa + base", 15, weight=900, fill=PRI)
    b += text(130, 60, "ácido fosfórico", 14, weight=900, fill="#6b5000") + text(300, 90, "pentosa", 14, weight=900, fill=AZ_S) + text(480, 90, "base nitrogenada", 14, weight=900, fill=PRI)
    save("nucleotido.svg", svg(620, 385, b, "Nucleótido: ácido fosfórico unido por enlace éster al carbono 5 de la pentosa, y base nitrogenada unida al carbono 1 por enlace N-glucosídico"))


# ─── 2 · Bases ─────────────────────────────────────────────────────────────
def bases():
    b = text(170, 30, "Púricas (dos anillos)", 17, weight=900, fill=PRI) + text(540, 30, "Pirimidínicas (un anillo)", 17, weight=900, fill=PRI)
    for i, (l, nom, donde) in enumerate((("A", "Adenina", "ADN y ARN"), ("G", "Guanina", "ADN y ARN"))):
        x = 100 + i * 150
        b += base_n(x, 100, l, 60) + text(x, 175, nom, 15, weight=900) + text(x, 194, donde, 12, weight=800, fill=GRIS)
    for i, (l, nom, donde) in enumerate((("C", "Citosina", "ADN y ARN"), ("T", "Timina", "solo ADN"), ("U", "Uracilo", "solo ARN"))):
        x = 420 + i * 110
        b += base_n(x, 100, l, 60) + text(x, 175, nom, 15, weight=900) + text(x, 194, donde, 12, weight=800, fill=ROJO if "solo" in donde else GRIS)
    b += f'<line x1="330" y1="40" x2="330" y2="200" stroke="#dde5ec" stroke-width="2"/>'
    save("bases-nitrogenadas.svg", svg(700, 210, b, "Bases púricas, adenina y guanina, y pirimidínicas, citosina, timina y uracilo"))


# ─── 3 · Cadena y enlace fosfodiéster ──────────────────────────────────────
def cadena():
    b = text(130, 26, "Extremo 5′ (fosfato libre)", 14, weight=900, fill=PRI)
    secuencia = "ATGC"
    y = 70
    for i, l in enumerate(secuencia):
        yy = y + i * 110
        b += fosfato(80, yy, 18)
        b += linea((98, yy), (130, yy + 18), 3)
        b += poligono(160, yy + 40, 30, 5, -90, AZ, AZ_S)
        b += text(128, yy + 24, "5′", 11, weight=900, fill=LILA)
        b += linea((190, yy + 40), (240, yy + 40), 3) + base_n(275, yy + 40, l, 34)
        if i < len(secuencia) - 1:
            b += linea((150, yy + 66), (98, yy + 104), 3)
            b += text(150, yy + 80, "3′", 11, weight=900, fill=LILA)
            b += f'<rect x="60" y="{yy + 76}" width="104" height="44" rx="8" fill="none" stroke="{ACC}" stroke-width="2" stroke-dasharray="5 4"/>'
    b += linea((150, y + 3 * 110 + 66), (150, y + 3 * 110 + 92), 3) + text(150, y + 3 * 110 + 110, "OH", 15, weight=900, fill=ROJO)
    b += text(130, y + 3 * 110 + 134, "Extremo 3′ (–OH libre)", 14, weight=900, fill=PRI)
    b += text(340, 140, "enlace fosfodiéster:", 14, "start", 900, fill=ACC)
    b += text(340, 160, "fosfato entre el C3′ de un", 13, "start", 800, fill=GRIS) + text(340, 178, "nucleótido y el C5′ del siguiente", 13, "start", 800, fill=GRIS)
    b += text(340, 260, "La secuencia de bases", 14, "start", 900, fill=PRI) + text(340, 280, "(5′ → 3′) es la estructura", 13, "start", 800, fill=GRIS) + text(340, 298, "primaria y contiene", 13, "start", 800, fill=GRIS) + text(340, 316, "la información genética", 13, "start", 800, fill=GRIS)
    save("cadena-polinucleotido.svg", svg(560, 520, b, "Cadena de nucleótidos unidos por enlaces fosfodiéster, con un extremo 5 con fosfato y un extremo 3 con OH"))


# ─── 4 · Doble hélice ──────────────────────────────────────────────────────
def doble_helice():
    b = ""
    x0, y0, H, A = 150, 50, 420, 70
    pares = "ATGCGATCTAGC"
    n = 60
    # hebras
    def hebra(fase, col):
        pts = [(x0 + A * math.sin(2 * math.pi * t / n * 2 + fase), y0 + H * t / n) for t in range(n + 1)]
        return pts
    h1, h2 = hebra(0, PRI), hebra(math.pi, ROJO)
    for i, l in enumerate(pares):
        t = (i + 0.5) / len(pares)
        k = int(t * n)
        a, c = h1[k], h2[k]
        m = ((a[0] + c[0]) / 2, a[1])
        comp = {"A": "T", "T": "A", "G": "C", "C": "G"}[l]
        b += linea(a, m, 7, COL_BASE[l]) + linea(m, c, 7, COL_BASE[comp])
    for pts, col in ((h1, "#3d85c6"), (h2, "#e07a5f")):
        b += f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="9" stroke-linecap="round"/>'
    b += text(x0 - A - 10, y0 - 10, "5′", 16, weight=900, fill="#3d85c6") + text(x0 - A - 10, y0 + H + 22, "3′", 16, weight=900, fill="#3d85c6")
    b += text(x0 + A + 12, y0 - 10, "3′", 16, weight=900, fill="#e07a5f") + text(x0 + A + 12, y0 + H + 22, "5′", 16, weight=900, fill="#e07a5f")
    b += f'<line x1="{x0 - A}" y1="{y0 + H + 40}" x2="{x0 + A}" y2="{y0 + H + 40}" stroke="{INK}" stroke-width="2" marker-start="url(#fk)" marker-end="url(#fk)"/>' + text(x0, y0 + H + 60, "2 nm", 14, weight=900)
    b += f'<line x1="{x0 + A + 50}" y1="{y0}" x2="{x0 + A + 50}" y2="{y0 + H / 2}" stroke="{INK}" stroke-width="2" marker-start="url(#fk)" marker-end="url(#fk)"/>'
    b += text(x0 + A + 58, y0 + H / 4, "una vuelta:", 13, "start", 900) + text(x0 + A + 58, y0 + H / 4 + 18, "3,4 nm", 13, "start", 900) + text(x0 + A + 58, y0 + H / 4 + 36, "(≈10 pares)", 12, "start", 800, fill=GRIS)
    # panel derecho: complementariedad
    ox = 420
    b += text(ox + 150, 40, "Bases complementarias", 17, weight=900, fill=PRI)
    for j, (l1, l2, nh) in enumerate((("A", "T", 2), ("G", "C", 3))):
        yy = 110 + j * 150
        b += base_n(ox + 70, yy, l1, 56) + base_n(ox + 230, yy, l2, 56)
        for k in range(nh):
            off = (k - (nh - 1) / 2) * 16
            b += f'<line x1="{ox + 118}" y1="{yy + off}" x2="{ox + 192}" y2="{yy + off}" stroke="{BLUE}" stroke-width="3" stroke-dasharray="5 4"/>'
        b += text(ox + 150, yy + 58, f"{l1} = {l2}: {nh} puentes de hidrógeno", 14, weight=900, fill=BLUE)
    b += text(ox + 150, 410, "púrica siempre frente a pirimidínica", 13, weight=800, fill=GRIS)
    b += text(ox + 150, 430, "→ anchura constante de la hélice", 13, weight=800, fill=GRIS)
    b += text(ox + 150, 470, "Regla de Chargaff (ADN bicatenario):", 14, weight=900, fill=ACC)
    b += text(ox + 150, 492, "A = T y G = C → A + G = T + C", 14, weight=900, fill=ACC)
    save("doble-helice.svg", svg(760, 545, b, "Doble hélice del ADN con cadenas antiparalelas y bases complementarias A-T con dos puentes de hidrógeno y G-C con tres"))


# ─── 5 · Empaquetamiento ───────────────────────────────────────────────────
def empaquetamiento():
    b = ""
    # 1 doble hélice
    pts1 = [(40 + i * 3, 110 + 10 * math.sin(i / 3)) for i in range(40)]
    pts2 = [(40 + i * 3, 110 - 10 * math.sin(i / 3)) for i in range(40)]
    for pts, col in ((pts1, "#3d85c6"), (pts2, "#e07a5f")):
        b += f'<polyline points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" fill="none" stroke="{col}" stroke-width="3"/>'
    b += text(100, 160, "Doble hélice", 14, weight=900) + text(100, 178, "2 nm", 12, weight=800, fill=GRIS)
    b += f'<line x1="170" y1="110" x2="200" y2="110" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
    # 2 nucleosomas
    for i in range(4):
        x = 225 + i * 32
        b += f'<ellipse cx="{x}" cy="110" rx="12" ry="16" fill="#f4a261" stroke="#b5600f" stroke-width="2"/>'
        b += f'<path d="M{x - 14},100 Q{x},88 {x + 14},100 M{x - 14},120 Q{x},132 {x + 14},120" fill="none" stroke="#3d85c6" stroke-width="2.5"/>'
        if i < 3:
            b += linea((x + 14, 120), (x + 18, 100), 2.5, "#3d85c6")
    b += text(270, 160, "Nucleosomas", 14, weight=900) + text(270, 178, "«collar de perlas» · 11 nm", 12, weight=800, fill=GRIS)
    b += text(270, 64, "ADN + octámero de histonas", 12, weight=800, fill="#b5600f")
    b += f'<line x1="350" y1="110" x2="380" y2="110" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
    # 3 solenoide (fibra de 30 nm)
    for i in range(9):
        x = 400 + i * 12
        y = 110 + 18 * math.sin(i * 1.2)
        b += f'<circle cx="{x}" cy="{y:.1f}" r="9" fill="#f4a261" stroke="#b5600f" stroke-width="1.5"/>'
    b += text(450, 160, "Fibra de 30 nm", 14, weight=900) + text(450, 178, "(solenoide)", 12, weight=800, fill=GRIS)
    b += f'<line x1="520" y1="110" x2="550" y2="110" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
    # 4 bucles
    for k in range(5):
        ang = -60 + k * 30
        b += f'<path d="M600,110 q{60 * math.cos(math.radians(ang)) - 10:.0f},{-60 * math.sin(math.radians(ang)) - 30:.0f} {60 * math.cos(math.radians(ang)) + 10:.0f},{-60 * math.sin(math.radians(ang)):.0f}" fill="none" stroke="#b5600f" stroke-width="5"/>' if False else ""
    for k in range(5):
        y = 70 + k * 20
        b += f'<path d="M580,{y} q40,-14 0,-4" fill="none" stroke="#b5600f" stroke-width="5"/>' if False else ""
    b += '<path d="M570,110 C590,40 640,60 620,110 C600,160 650,170 660,110 C670,50 720,70 700,110" fill="none" stroke="#b5600f" stroke-width="6"/>'
    b += text(635, 160, "Bucles y más", 14, weight=900) + text(635, 178, "plegamientos", 12, weight=800, fill=GRIS)
    b += f'<line x1="715" y1="110" x2="745" y2="110" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
    # 5 cromosoma metafásico
    cx = 800
    for dx in (-14, 14):
        b += f'<path d="M{cx + dx},40 C{cx + dx - 12},70 {cx + dx - 12},95 {cx + dx},110 C{cx + dx + 12},125 {cx + dx + 12},155 {cx + dx},185" fill="none" stroke="#7b3fb0" stroke-width="22" stroke-linecap="round"/>'
    b += f'<circle cx="{cx}" cy="110" r="9" fill="#f7c948" stroke="#8a6d00" stroke-width="2"/>'
    b += text(cx, 215, "Cromosoma", 14, weight=900) + text(cx, 233, "metafásico", 12, weight=800, fill=GRIS)
    b += text(cx + 52, 70, "cromátida", 12, "start", 900, fill="#7b3fb0") + text(cx + 30, 116, "centrómero", 12, "start", 900, fill="#8a6d00")
    save("empaquetamiento-adn.svg", svg(950, 245, b, "Niveles de empaquetamiento del ADN: doble hélice, nucleosomas, fibra de 30 nanómetros, bucles y cromosoma metafásico"))


# ─── 6 · ATP ───────────────────────────────────────────────────────────────
def atp():
    b = base_n(90, 110, "A", 60)
    b += text(80, 175, "adenina", 14, weight=900, fill="#e76f51")
    b += linea((150, 110), (185, 110), 3)
    b += poligono(225, 112, 38, 5, -90, AZ, AZ_S) + text(225, 175, "ribosa", 14, weight=900, fill=AZ_S)
    b += linea((262, 110), (300, 110), 3)
    for i in range(3):
        x = 320 + i * 72
        b += fosfato(x, 110, 22)
        if i < 2:
            b += f'<path d="M{x + 24},110 q12,-12 24,0" fill="none" stroke="{ROJO}" stroke-width="4"/>'
            b += text(x + 36, 92, "~", 26, weight=900, fill=ROJO)
    b += text(392, 175, "tres fosfatos", 14, weight=900, fill="#6b5000")
    b += text(392, 60, "enlaces ricos en energía (~)", 13, weight=900, fill=ROJO)
    b += f'<path d="M140,215 H540" stroke="{TEAL}" stroke-width="3"/>' + text(340, 237, "adenosina = adenina + ribosa (nucleósido)", 13, weight=900, fill=TEAL)
    # ciclo
    b += text(340, 290, "ATP  →  ADP + Pi + energía", 18, weight=900, fill=PRI)
    b += text(340, 318, "hidrólisis: libera energía para el trabajo celular (síntesis, transporte, contracción)", 13, weight=800, fill=GRIS)
    b += text(340, 340, "ADP + Pi + energía → ATP: en la respiración y la fotosíntesis (fosforilación)", 13, weight=800, fill=GRIS)
    save("atp.svg", svg(680, 355, b, "ATP: adenina, ribosa y tres fosfatos con enlaces ricos en energía; su hidrólisis a ADP libera energía"))


# ─── 7 · Tipos de ARN ──────────────────────────────────────────────────────
def arn_tipos():
    b = text(150, 28, "ARN mensajero", 17, weight=900, fill=PRI)
    seq = "AUGGCUUAC"
    for i, l in enumerate(seq):
        x = 30 + i * 28
        b += f'<rect x="{x}" y="70" width="24" height="36" rx="5" fill="{COL_BASE[l]}"/>' + text(x + 12, 94, l, 14, weight=900, fill="#fff" if l in "AG" else INK)
    b += linea((28, 66), (290, 66), 4, "#8ab17d")
    for k in range(3):
        b += f'<path d="M{30 + k * 84},116 H{108 + k * 84}" stroke="{ACC}" stroke-width="3"/>' + text(69 + k * 84, 134, "codón", 12, weight=900, fill=ACC)
    b += text(150, 166, "lineal, monocatenario · copia la", 13, weight=800, fill=GRIS) + text(150, 184, "información del ADN y la lleva al ribosoma", 13, weight=800, fill=GRIS)
    # ARNt hoja de trébol
    ox = 470
    b += text(ox, 28, "ARN de transferencia", 17, weight=900, fill=PRI)
    b += f'<path d="M{ox},60 V120 M{ox - 10},60 V120" stroke="#8ab17d" stroke-width="6"/>'
    b += f'<circle cx="{ox - 60}" cy="140" r="28" fill="none" stroke="#8ab17d" stroke-width="6"/><circle cx="{ox + 55}" cy="140" r="28" fill="none" stroke="#8ab17d" stroke-width="6"/>'
    b += f'<path d="M{ox - 5},120 V200" stroke="#8ab17d" stroke-width="12"/>'
    b += f'<path d="M{ox - 11},140 H{ox - 32} M{ox + 1},140 H{ox + 27}" stroke="#8ab17d" stroke-width="8"/>'
    b += f'<circle cx="{ox - 5}" cy="228" r="28" fill="none" stroke="#8ab17d" stroke-width="6"/>'
    for i, l in enumerate("GAU"):
        x = ox - 25 + i * 20
        b += f'<rect x="{x - 9}" y="250" width="18" height="24" rx="4" fill="{COL_BASE[l]}"/>' + text(x, 267, l, 12, weight=900, fill="#fff" if l in "AG" else INK)
    b += text(ox - 5, 296, "anticodón", 13, weight=900, fill=ACC)
    b += f'<circle cx="{ox}" cy="48" r="13" fill="#9b7fd1"/>' + text(ox + 22, 52, "aminoácido (extremo 3′)", 12, "start", 900, fill=LILA)
    b += text(ox, 322, "hoja de trébol: zonas de doble hélice", 12, weight=800, fill=GRIS) + text(ox, 338, "transporta los aminoácidos al ribosoma", 12, weight=800, fill=GRIS)
    # ARNr: ribosoma
    ox = 780
    b += text(ox, 28, "ARN ribosómico", 17, weight=900, fill=PRI)
    b += f'<ellipse cx="{ox}" cy="110" rx="80" ry="48" fill="#b8d8f0" stroke="#3d85c6" stroke-width="3"/>'
    b += f'<ellipse cx="{ox}" cy="178" rx="68" ry="30" fill="#d9ebf7" stroke="#3d85c6" stroke-width="3"/>'
    b += text(ox, 115, "subunidad mayor", 13, weight=900, fill="#1f4e79") + text(ox, 183, "subunidad menor", 13, weight=900, fill="#1f4e79")
    b += text(ox, 240, "ARNr + proteínas", 14, weight=900, fill=PRI)
    b += text(ox, 262, "forma los ribosomas,", 12, weight=800, fill=GRIS) + text(ox, 278, "donde se sintetizan las proteínas", 12, weight=800, fill=GRIS)
    save("arn-tipos.svg", svg(900, 350, b, "Tipos de ARN: mensajero lineal con codones, de transferencia en hoja de trébol con anticodón y ribosómico formando los ribosomas"))


if __name__ == "__main__":
    for f in (nucleotido, bases, cadena, doble_helice, empaquetamiento, atp, arn_tipos):
        f()
