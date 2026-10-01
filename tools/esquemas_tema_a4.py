# Esquemas SVG del tema A4 (proteínas) de BioCelia.
# Uso: python tools/esquemas_tema_a4.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, P, d, INK, BLUE
from esquemas_tema_a1_extra import estructura, COL_AT

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "a4")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO, VERDE = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"
COL_AT.update({"H₂N": "#1f5fa8", "COOH": ROJO, "H₃N⁺": "#1f5fa8", "COO⁻": ROJO})


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)


def save(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def linea(a, b, w=2.6, col=INK, extra=""):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


# ─── 1 · Aminoácido ────────────────────────────────────────────────────────
def aminoacido():
    b = estructura({"c": (230, 140, "C"), "h": (230, 70, "H"), "r": (230, 212, "R"), "n": (130, 140, "H₂N"), "co": (335, 140, "COOH")},
                   [("c", "h", 1), ("c", "r", 1), ("c", "n", 1), ("c", "co", 1)], 28)
    b += text(250, 125, "α", 18, "start", 900, fill=ACC)
    b += text(130, 185, "grupo amino", 15, weight=900, fill="#1f5fa8") + text(130, 203, "(básico)", 13, weight=700, fill=GRIS)
    b += text(335, 185, "grupo carboxilo", 15, weight=900, fill=ROJO) + text(335, 203, "(ácido)", 13, weight=700, fill=GRIS)
    b += text(230, 250, "radical o cadena lateral: distinto en cada aminoácido", 14, weight=800, fill=LILA)
    b += text(230, 30, "Carbono α unido a –NH₂, –COOH, H y R", 16, weight=900, fill=PRI)
    save("aminoacido.svg", svg(460, 265, b, "Estructura general de un aminoácido"))


def tipos_aminoacidos():
    tipos = [("Apolares (hidrófobos)", "Alanina", ["CH₃"], TEAL),
             ("Polares sin carga", "Serina", ["CH₂", "OH"], BLUE),
             ("Ácidos (carga −)", "Aspártico", ["CH₂", "COO⁻"], ROJO),
             ("Básicos (carga +)", "Lisina", ["(CH₂)₄", "NH₃⁺"], LILA)]
    b = ""
    for i, (t, nom, r, col) in enumerate(tipos):
        x = 120 + i * 240
        b += f'<rect x="{x - 108}" y="14" width="216" height="290" rx="14" fill="#f6f9fb" stroke="{col}" stroke-width="2.5"/>'
        b += text(x, 42, t, 15, weight=900, fill=col)
        at = {"c": (x, 120, "C"), "h": (x, 74, "H"), "n": (x - 66, 120, "H₃N⁺"), "co": (x + 68, 120, "COO⁻")}
        en = [("c", "h", 1), ("c", "n", 1), ("c", "co", 1)]
        y = 166
        prev = "c"
        for k, g in enumerate(r):
            at[f"r{k}"] = (x, y, g)
            en.append((prev, f"r{k}", 1))
            prev = f"r{k}"
            y += 46
        b += estructura(at, en, 20)
        b += f'<rect x="{x - 46}" y="148" width="92" height="{46 * len(r) - 6}" rx="8" fill="none" stroke="{col}" stroke-width="2" stroke-dasharray="5 4"/>'
        b += text(x, 288, nom, 17, weight=900, fill=PRI)
    b += text(480, 330, "Se clasifican por su radical R (a pH 7, grupos amino y carboxilo ionizados).", 14, weight=700, fill=GRIS)
    save("aminoacidos-tipos.svg", svg(960, 345, b, "Tipos de aminoácidos según su radical: apolares, polares sin carga, ácidos y básicos"))


# ─── 2 · Enlace peptídico ──────────────────────────────────────────────────
def peptidico():
    b = ""

    def aa(x, r, idx):
        return estructura({"c": (x, 110, "C"), "h": (x, 62, "H"), "r": (x, 158, r), "n": (x - 62, 110, "H₂N"), "co": (x + 64, 110, "COOH")},
                          [("c", "h", 1), ("c", "r", 1), ("c", "n", 1), ("c", "co", 1)], 20)
    b += aa(90, "R₁", 1) + text(195, 117, "+", 28, weight=900) + aa(300, "R₂", 2)
    b += f'<rect x="153" y="96" width="30" height="26" rx="6" fill="none" stroke="{ACC}" stroke-width="2.5"/>'
    b += f'<rect x="219" y="96" width="16" height="26" rx="5" fill="none" stroke="{ACC}" stroke-width="2.5"/>'
    b += text(168, 90, "OH", 12, weight=900, fill=ACC) + text(227, 90, "H", 12, weight=900, fill=ACC)
    b += f'<line x1="410" y1="110" x2="470" y2="110" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    b += text(440, 98, "– H₂O", 13, weight=900, fill=BLUE)
    # dipéptido
    at = {"n": (520, 110, "H₂N"), "c1": (585, 110, "C"), "h1": (585, 62, "H"), "r1": (585, 158, "R₁"),
          "co": (650, 110, "C"), "o": (650, 58, "O"), "nh": (715, 110, "N"), "hn": (715, 160, "H"),
          "c2": (780, 110, "C"), "h2": (780, 62, "H"), "r2": (780, 158, "R₂"), "cooh": (848, 110, "COOH")}
    en = [("n", "c1", 1), ("c1", "h1", 1), ("c1", "r1", 1), ("c1", "co", 1), ("co", "o", 2), ("co", "nh", 1), ("nh", "hn", 1),
          ("nh", "c2", 1), ("c2", "h2", 1), ("c2", "r2", 1), ("c2", "cooh", 1)]
    b += f'<rect x="628" y="40" width="110" height="135" rx="10" fill="#fff4df" stroke="{ACC}" stroke-width="2.5"/>'
    b += estructura(at, en, 20)
    b += text(683, 196, "enlace peptídico", 15, weight=900, fill=ACC)
    b += text(520, 196, "extremo N-terminal", 12, weight=800, fill="#1f5fa8") + text(848, 196, "extremo C-terminal", 12, weight=800, fill=ROJO)
    b += text(470, 245, "Covalente · carácter parcial de doble enlace: rígido, sin giro y con sus átomos en un mismo plano.", 15, weight=800, fill=GRIS)
    save("enlace-peptidico.svg", svg(940, 262, b, "Dos aminoácidos se unen por un enlace peptídico y forman un dipéptido liberando agua"))


# ─── 3 · Niveles estructurales ─────────────────────────────────────────────
COLS = ["#e76f51", "#f4a261", "#e9c46a", "#2a9d8f", "#264653", "#8ab17d", "#bc6c25", "#6d597a"]


def helice(cx, y0, vueltas=4, r=26, paso=34, w=7, col="#d1495b", hb=False, rgrupos=False):
    s = ""
    pts = []
    n = int(vueltas * 36)
    for i in range(n + 1):
        t = i / 36 * 2 * math.pi
        pts.append((cx + r * math.cos(t), y0 + paso * t / (2 * math.pi), math.sin(t)))
    # parte de atrás primero
    for a, c in zip(pts, pts[1:]):
        if a[2] < 0:
            s += linea(a[:2], c[:2], w, "#e8a0aa")
    if hb:
        for i in range(0, n - 36, 9):
            a, c = pts[i], pts[i + 36]
            if a[2] >= 0:
                s += f'<line x1="{a[0]:.1f}" y1="{a[1] + 5:.1f}" x2="{c[0]:.1f}" y2="{c[1] - 5:.1f}" stroke="{BLUE}" stroke-width="2" stroke-dasharray="4 3"/>'
    for a, c in zip(pts, pts[1:]):
        if a[2] >= 0:
            s += linea(a[:2], c[:2], w, col)
    if rgrupos:
        for i in range(4, n, 10):
            a = pts[i]
            dx = 1 if a[0] >= cx else -1
            fin = (a[0] + dx * 22, a[1])
            s += linea(a[:2], fin, 2, LILA) + f'<circle cx="{fin[0]:.1f}" cy="{fin[1]:.1f}" r="5" fill="{LILA}"/>'
    return s


def lamina(x0, y0, n_hebras=3, largo=8, paso=24, sep=56, flechas=True, hb=True, rgrupos=False):
    s = ""
    hebras = []
    for j in range(n_hebras):
        y = y0 + j * sep
        pts = [(x0 + i * paso, y + (8 if i % 2 else -8)) for i in range(largo + 1)]
        hebras.append(pts)
    if hb:
        for j in range(n_hebras - 1):
            for i in range(1, largo, 2):
                a, c = hebras[j][i], hebras[j + 1][i]
                s += f'<line x1="{a[0]:.1f}" y1="{a[1] + 4:.1f}" x2="{c[0]:.1f}" y2="{c[1] - 12:.1f}" stroke="{BLUE}" stroke-width="2" stroke-dasharray="4 3"/>'
    for j, pts in enumerate(hebras):
        s += "".join(linea(a, c, 6, "#3d85c6") for a, c in zip(pts, pts[1:]))
        if flechas:
            fin, prev = (pts[-1], pts[-2]) if j % 2 == 0 else (pts[0], pts[1])
            ang = math.atan2(fin[1] - prev[1], fin[0] - prev[0])
            tip = (fin[0] + 16 * math.cos(ang), fin[1] + 16 * math.sin(ang))
            l = (fin[0] + 9 * math.cos(ang + 1.9), fin[1] + 9 * math.sin(ang + 1.9))
            r = (fin[0] + 9 * math.cos(ang - 1.9), fin[1] + 9 * math.sin(ang - 1.9))
            s += f'<polygon points="{tip[0]:.1f},{tip[1]:.1f} {l[0]:.1f},{l[1]:.1f} {r[0]:.1f},{r[1]:.1f}" fill="#3d85c6"/>'
        if rgrupos:
            for i, p in enumerate(pts):
                if i % 2 == 0:
                    s += f'<circle cx="{p[0]:.1f}" cy="{p[1] - 13:.1f}" r="4.5" fill="{LILA}"/>'
                else:
                    s += f'<circle cx="{p[0]:.1f}" cy="{p[1] + 13:.1f}" r="4.5" fill="{LILA}" opacity="0.55"/>'
    return s


def niveles():
    b = ""
    # primaria
    b += text(130, 30, "1. Primaria", 18, weight=900, fill=PRI)
    nombres = ["Gly", "Ala", "Ser", "Lys", "Val", "Cys", "Glu", "Leu"]
    for i, nm in enumerate(nombres):
        x, y = 30 + (i % 4) * 66, 80 + (i // 4) * 74
        if i % 4 and True:
            b += linea((x - 44, y), (x - 22, y), 3)
        if i == 4:
            b += f'<path d="M{30 + 3 * 66},{80 + 22} Q{30 + 3 * 66 + 40},{120} {x + 20},{y - 8}" fill="none" stroke="{INK}" stroke-width="3"/>' if False else linea((30 + 3 * 66, 102), (x, y - 22), 3)
        b += f'<circle cx="{x}" cy="{y}" r="22" fill="{COLS[i]}"/>' + text(x, y + 5, nm, 13, weight=900, fill="#fff")
    b += text(130, 250, "secuencia de aminoácidos", 13, weight=800, fill=GRIS) + text(130, 268, "(enlaces peptídicos)", 13, weight=800, fill=GRIS)
    # secundaria
    b += text(420, 30, "2. Secundaria", 18, weight=900, fill=PRI)
    b += helice(360, 60, 4, 22, 36)
    b += text(360, 230, "α-hélice", 14, weight=900, fill="#d1495b")
    b += lamina(410, 80, 3, 5, 22, 48)
    b += text(470, 230, "lámina β", 14, weight=900, fill="#3d85c6")
    b += text(420, 268, "(puentes de H)", 13, weight=800, fill=GRIS)
    # terciaria
    b += text(690, 30, "3. Terciaria", 18, weight=900, fill=PRI)
    b += ('<path d="M600,200 C580,140 640,90 690,110 C740,130 700,170 660,160 C620,150 640,70 700,60 '
          'C770,50 790,120 760,160 C730,200 680,230 640,215" fill="none" stroke="#d1495b" stroke-width="9" stroke-linecap="round"/>')
    b += ('<path d="M690,240 C720,215 760,240 790,215" fill="none" stroke="#3d85c6" stroke-width="9" stroke-linecap="round"/>')
    b += text(690, 268, "plegamiento 3D (enlaces entre radicales)", 13, weight=800, fill=GRIS)
    # cuaternaria
    b += text(960, 30, "4. Cuaternaria", 18, weight=900, fill=PRI)
    for (x, y, col) in ((915, 110, "#d1495b"), (1005, 110, "#3d85c6"), (915, 190, "#3d85c6"), (1005, 190, "#d1495b")):
        b += f'<circle cx="{x}" cy="{y}" r="40" fill="{col}" opacity="0.85"/>'
        b += f'<rect x="{x - 8}" y="{y - 8}" width="16" height="16" rx="3" fill="#f7c948" stroke="#8a6d00"/>'
    b += text(960, 250, "varias cadenas", 13, weight=800, fill=GRIS) + text(960, 268, "(ej.: hemoglobina, 4 cadenas)", 13, weight=800, fill=GRIS)
    save("niveles-estructurales.svg", svg(1080, 285, b, "Niveles estructurales de las proteínas: primaria, secundaria, terciaria y cuaternaria"))


def secundaria():
    b = text(150, 28, "α-hélice", 19, weight=900, fill="#d1495b")
    b += helice(150, 55, 5, 40, 44, 9, hb=True, rgrupos=True)
    b += text(160, 300, "dextrógira · 3,6 aminoácidos por vuelta", 12.5, weight=800, fill=GRIS)
    b += text(160, 318, "radicales hacia fuera", 12.5, weight=800, fill=GRIS)
    b += text(160, 336, "puentes de H entre C=O y N–H", 12.5, weight=800, fill=GRIS)
    b += f'<line x1="330" y1="30" x2="330" y2="330" stroke="#dde5ec" stroke-width="2"/>'
    b += text(540, 28, "Lámina β (hoja plegada)", 19, weight=900, fill="#3d85c6")
    b += lamina(400, 90, 3, 11, 26, 68, rgrupos=True)
    b += text(540, 300, "cadenas en zigzag, paralelas o antiparalelas", 13, weight=800, fill=GRIS)
    b += text(540, 318, "puentes de H entre C=O y N–H de cadenas contiguas", 13, weight=800, fill=GRIS)
    b += text(540, 336, "radicales alternativamente arriba y abajo", 13, weight=800, fill=GRIS)
    b += f'<line x1="620" y1="56" x2="660" y2="56" stroke="{BLUE}" stroke-width="2" stroke-dasharray="4 3"/>' + text(666, 61, "puente de H", 13, "start", 800, fill=BLUE)
    save("estructura-secundaria.svg", svg(760, 350, b, "Alfa-hélice y lámina beta con sus puentes de hidrógeno"))


def terciaria():
    b = '<path d="M60,240 C40,160 120,90 200,110 C280,130 250,190 200,200 C150,210 140,120 230,70 C330,20 420,80 420,160 C420,240 330,270 260,250" fill="none" stroke="#d1495b" stroke-width="10" stroke-linecap="round"/>'
    items = [((200, 200), (230, 70), "S–S", "puente disulfuro (covalente)", ACC, 470, 60),
             ((150, 150), (200, 110), "H", "puente de hidrógeno", BLUE, 470, 110),
             ((420, 160), (340, 220), "±", "interacción iónica (– COO⁻ · · · NH₃⁺ –)", ROJO, 470, 160),
             ((280, 140), (330, 150), "", "interacciones hidrofóbicas y de Van der Waals", TEAL, 470, 210)]
    for a, c, et, t, col, tx, ty in items:
        if et:
            b += f'<line x1="{a[0]}" y1="{a[1]}" x2="{c[0]}" y2="{c[1]}" stroke="{col}" stroke-width="3.5" stroke-dasharray="6 4"/>'
            m = ((a[0] + c[0]) / 2, (a[1] + c[1]) / 2)
            b += f'<circle cx="{m[0]}" cy="{m[1]}" r="13" fill="#fff" stroke="{col}" stroke-width="2"/>' + text(m[0], m[1] + 5, et, 12, weight=900, fill=col)
        else:
            for x, y in ((285, 140), (305, 160), (325, 140), (300, 120)):
                b += f'<circle cx="{x}" cy="{y}" r="10" fill="{TEAL}" opacity="0.8"/>'
        b += f'<rect x="{tx - 12}" y="{ty - 12}" width="14" height="14" rx="3" fill="{col}"/>' + text(tx + 10, ty, t, 15, "start", 800)
    b += text(470, 262, "Todas se establecen entre los radicales R.", 14, "start", 800, fill=GRIS)
    save("enlaces-terciaria.svg", svg(860, 285, b, "Enlaces e interacciones que estabilizan la estructura terciaria: puentes disulfuro, de hidrógeno, iónicos e hidrofóbicos"))


def desnaturalizacion():
    b = text(140, 28, "Proteína nativa", 17, weight=900, fill=PRI)
    b += '<path d="M60,200 C40,140 100,80 160,100 C220,120 190,170 150,170 C110,170 120,90 180,70 C240,50 260,120 230,170 C200,210 140,230 110,215" fill="none" stroke="#d1495b" stroke-width="9" stroke-linecap="round"/>'
    b += text(140, 255, "forma 3D → funcional", 13, weight=800, fill=VERDE)
    b += f'<line x1="270" y1="120" x2="370" y2="120" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    b += f'<line x1="370" y1="150" x2="270" y2="150" stroke="{INK}" stroke-width="3" marker-end="url(#fk)" stroke-dasharray="6 4"/>'
    b += text(320, 106, "calor, pH extremo", 13, weight=900, fill=ROJO) + text(320, 175, "renaturalización", 13, weight=900, fill=VERDE)
    b += text(320, 192, "(si es reversible)", 11, weight=800, fill=GRIS)
    b += text(510, 28, "Desnaturalizada", 17, weight=900, fill=PRI)
    b += '<path d="M390,140 C420,110 450,170 480,130 C510,90 540,170 570,130 C600,95 620,150 640,120" fill="none" stroke="#d1495b" stroke-width="9" stroke-linecap="round"/>'
    b += text(515, 210, "se pierden 2.ª, 3.ª y 4.ª", 13, weight=800, fill=ROJO) + text(515, 228, "se conserva la 1.ª (enlaces peptídicos)", 13, weight=800, fill=GRIS)
    b += text(515, 255, "→ pierde la función", 13, weight=800, fill=ROJO)
    b += f'<line x1="680" y1="30" x2="680" y2="265" stroke="#dde5ec" stroke-width="2"/>'
    b += text(840, 28, "Hidrólisis", 17, weight=900, fill=PRI)
    for i in range(7):
        x = 730 + i * 34
        b += f'<circle cx="{x}" cy="{130 + (i % 2) * 20}" r="13" fill="{COLS[i]}"/>'
    b += text(840, 210, "rompe los enlaces peptídicos", 13, weight=800, fill=ROJO) + text(840, 228, "(enzimas proteasas, ácidos)", 13, weight=800, fill=GRIS)
    b += text(840, 255, "→ aminoácidos libres", 13, weight=800, fill=PRI)
    save("desnaturalizacion-hidrolisis.svg", svg(960, 270, b, "La desnaturalización pierde la forma pero conserva la secuencia; la hidrólisis rompe la cadena en aminoácidos"))


def globular_fibrosa():
    b = text(170, 28, "Globulares", 18, weight=900, fill=PRI)
    b += '<path d="M170,60 C230,55 260,110 245,150 C230,195 170,210 130,190 C85,170 80,110 110,80 C125,66 150,61 170,60z" fill="#f4c0c7" stroke="#d1495b" stroke-width="3"/>'
    b += '<path d="M120,120 C150,90 200,140 230,110 M130,160 C160,130 200,180 235,150" fill="none" stroke="#d1495b" stroke-width="4"/>'
    b += text(170, 235, "esféricas · solubles en agua", 13, weight=800, fill=GRIS)
    b += text(170, 253, "enzimas, hemoglobina, anticuerpos, albúminas", 13, weight=800, fill=GRIS)
    b += text(510, 28, "Fibrosas", 18, weight=900, fill=PRI)
    for k in range(3):
        b += f'<path d="M370,{100 + k * 14} ' + " ".join(f"Q{385 + i * 30},{(100 + k * 14) + (-14 if i % 2 else 14)} {400 + i * 30},{100 + k * 14}" for i in range(9)) + '" fill="none" stroke="#3d85c6" stroke-width="5"/>'
    b += text(510, 235, "alargadas · insolubles", 13, weight=800, fill=GRIS)
    b += text(510, 253, "estructurales: colágeno, queratina, elastina", 13, weight=800, fill=GRIS)
    save("globulares-fibrosas.svg", svg(680, 270, b, "Proteínas globulares, esféricas y solubles, y fibrosas, alargadas e insolubles"))


# ─── 4 · Funciones ────────────────────────────────────────────────────────
def funciones():
    items = [("Catalítica", "enzimas"), ("Estructural", "colágeno, queratina"), ("Transporte", "hemoglobina"), ("Contráctil", "actina, miosina"),
             ("Defensiva", "anticuerpos"), ("Hormonal", "insulina"), ("Reconocimiento", "receptores de membrana"), ("Reserva", "ovoalbúmina, caseína")]
    b = ""
    for i, (t, ej) in enumerate(items):
        cx, cy = 80 + (i % 4) * 230, 70 + (i // 4) * 170
        if i == 0:  # enzima con sustrato
            b += f'<path d="M{cx - 45},{cy + 30} V{cy - 20} Q{cx - 45},{cy - 40} {cx - 25},{cy - 40} H{cx - 12} V{cy - 12} H{cx + 12} V{cy - 40} H{cx + 25} Q{cx + 45},{cy - 40} {cx + 45},{cy - 20} V{cy + 30}z" fill="#9ed49a" stroke="{VERDE}" stroke-width="2.5"/>'
            b += f'<rect x="{cx - 10}" y="{cy - 58}" width="20" height="40" rx="4" fill="#f7c948" stroke="#8a6d00" stroke-width="2"/>'
        elif i == 1:  # triple hélice
            for k, col in enumerate(("#e76f51", "#2a9d8f", "#264653")):
                b += f'<path d="M{cx - 50},{cy + k * 5 - 5} ' + " ".join(f"Q{cx - 45 + j * 20},{cy + (-14 if (j + k) % 2 else 14)} {cx - 40 + j * 20},{cy + k * 5 - 5}" for j in range(5)) + f'" fill="none" stroke="{col}" stroke-width="4"/>'
        elif i == 2:  # glóbulo rojo con O2
            b += f'<ellipse cx="{cx}" cy="{cy}" rx="44" ry="34" fill="#d9534f"/><ellipse cx="{cx}" cy="{cy}" rx="18" ry="13" fill="#ec8e8a"/>'
            b += f'<circle cx="{cx + 40}" cy="{cy - 34}" r="10" fill="#fff" stroke="{BLUE}" stroke-width="2"/>' + text(cx + 40, cy - 30, "O₂", 10, weight=900, fill=BLUE)
        elif i == 3:  # filamentos
            b += linea((cx - 50, cy - 12), (cx + 20, cy - 12), 7, "#e9c46a") + linea((cx - 20, cy + 12), (cx + 50, cy + 12), 7, "#e9c46a")
            b += linea((cx - 30, cy), (cx + 30, cy), 10, "#bc6c25")
            for x in (-20, 0, 20):
                b += linea((cx + x, cy), (cx + x + 8, cy - 9), 3, "#bc6c25")
        elif i == 4:  # anticuerpo en Y
            b += linea((cx, cy + 35), (cx, cy), 9, "#6d597a") + linea((cx, cy), (cx - 30, cy - 32), 9, "#6d597a") + linea((cx, cy), (cx + 30, cy - 32), 9, "#6d597a")
        elif i == 5:  # hormona → receptor
            b += f'<circle cx="{cx - 25}" cy="{cy - 10}" r="13" fill="#f4a261"/><path d="M{cx},{cy + 30} V{cy - 5} H{cx + 12} V{cy + 10} H{cx + 26} V{cy - 5} H{cx + 38} V{cy + 30}" fill="#8ab17d" stroke="{VERDE}" stroke-width="2"/>'
        elif i == 6:  # célula con receptores
            b += f'<path d="M{cx - 55},{cy + 20} Q{cx},{cy - 5} {cx + 55},{cy + 20}" fill="none" stroke="{BLUE}" stroke-width="6"/>'
            for x in (-30, 0, 30):
                b += linea((cx + x, cy + 10), (cx + x, cy - 15), 4, "#6d597a") + f'<circle cx="{cx + x}" cy="{cy - 20}" r="6" fill="#6d597a"/>'
        else:  # huevo
            b += f'<ellipse cx="{cx}" cy="{cy}" rx="34" ry="44" fill="#fbf6ec" stroke="#b9a98a" stroke-width="2.5"/><circle cx="{cx}" cy="{cy + 6}" r="17" fill="#f2c94c"/>'
        b += text(cx, cy + 70, t, 16, weight=900, fill=PRI) + text(cx, cy + 89, ej, 12, weight=700, fill=GRIS)
    save("proteinas-funciones.svg", svg(930, 350, b, "Funciones de las proteínas con ejemplos"))


def biuret():
    def tubo(x, col, et, sub):
        s = f'<path d="M{x - 22},40 V190 A22,22 0 0 0 {x + 22},190 V40" fill="#fff" stroke="#7b8a97" stroke-width="3"/>'
        s += f'<path d="M{x - 20},110 V190 A20,20 0 0 0 {x + 20},190 V110z" fill="{col}"/>'
        return s + text(x, 240, et, 15, weight=900) + text(x, 258, sub, 12, weight=700, fill=GRIS)
    b = text(165, 20, "Biuret: proteínas", 16, weight=900, fill=PRI)
    b += tubo(80, "#7fb3e6", "Negativo", "azul") + tubo(250, "#7b3fb0", "Positivo", "violeta")
    b += text(165, 290, "detecta los enlaces peptídicos", 13, weight=800)
    save("prueba-biuret.svg", svg(330, 305, b, "Prueba de Biuret: negativa azul y positiva violeta"))


if __name__ == "__main__":
    for f in (aminoacido, tipos_aminoacidos, peptidico, niveles, secundaria, terciaria, desnaturalizacion, globular_fibrosa, funciones, biuret):
        f()
