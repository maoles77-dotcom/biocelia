# Esquemas SVG del tema E1 (microorganismos y aplicaciones biotecnológicas) de BioCelia.
# Uso: python tools/esquemas_tema_e1.py
import os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "e1")
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


def et(x, y, t, col=INK, size=13, anchor="middle", w=800):
    return text(x, y, t, size, anchor, w, fill=col)


# ------------------------------------------------------------ iconos
def bacteria(cx, cy, s=1.0, col=TEAL):
    w, h = 90 * s, 44 * s
    b = f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="#dff3ef" stroke="{col}" stroke-width="3"/>'
    b += f'<path d="M{cx - 22 * s},{cy} q8,-12 16,0 t16,0 t16,0" fill="none" stroke="{INK}" stroke-width="2"/>'
    b += f'<path d="M{cx + w / 2},{cy} q14,-10 26,0 t26,0" fill="none" stroke="{col}" stroke-width="2.2"/>'
    for k in range(5):
        b += f'<circle cx="{cx - 30 * s + k * 14 * s}" cy="{cy + 11 * s}" r="2.2" fill="{GRIS}"/>'
    return b


def eucariota(cx, cy, r, fondo, col, nucleo="#c9b7ef", cloro=False, pared=False):
    b = ""
    if pared:
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="{r + 5}" ry="{r * 0.8 + 5}" fill="none" stroke="{col}" stroke-width="2"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r * 0.8}" fill="{fondo}" stroke="{col}" stroke-width="3"/>'
    b += f'<circle cx="{cx - r * 0.25}" cy="{cy - r * 0.1}" r="{r * 0.3}" fill="{nucleo}" stroke="{LILA}" stroke-width="2"/>'
    if cloro:
        for dx, dy in ((0.4, -0.3), (0.35, 0.35), (-0.1, 0.45)):
            b += f'<ellipse cx="{cx + dx * r}" cy="{cy + dy * r}" rx="{r * 0.2}" ry="{r * 0.1}" fill="#7fbf6a" stroke="{VERDE}" stroke-width="1.5"/>'
    return b


def virus(cx, cy, s=1.0):
    pts = []
    import math
    for k in range(6):
        a = math.radians(60 * k + 30)
        pts.append(f"{cx + 26 * s * math.cos(a):.1f},{cy - 10 + 26 * s * math.sin(a):.1f}")
    b = f'<polygon points="{" ".join(pts)}" fill="#fdeaea" stroke="{ROJO}" stroke-width="3"/>'
    b += f'<path d="M{cx - 10},{cy - 14} q6,8 12,0 t10,4" fill="none" stroke="{INK}" stroke-width="2"/>'
    b += linea(cx, cy + 16, cx, cy + 40, ROJO, 3)
    for dx in (-14, 14):
        b += linea(cx, cy + 40, cx + dx, cy + 52, ROJO, 2.5)
    return b


# ------------------------------------------------------------ grupos de microorganismos
def grupos():
    b = caja(560, 34, 300, 46, "MICROORGANISMOS", PRI, "#e3eef8", 18)
    b += et(560, 76, "seres vivos que solo se ven con el microscopio", GRIS, 13)
    # ramas
    b += linea(560, 86, 560, 104, INK, 2.5) + linea(140, 104, 980, 104, INK, 2.5)
    xs = [140, 345, 560, 770, 980]
    for x in xs:
        b += flecha(x, 104, x, 124)
    datos = [
        ("Bacterias", TEAL, "PROCARIOTAS", "unicelulares", ["autótrofas o", "heterótrofas", "bipartición"]),
        ("Algas microscópicas", VERDE, "EUCARIOTAS", "uni- o pluricelulares", ["autótrofas:", "fotosíntesis", "sin tejidos"]),
        ("Hongos", ACC, "EUCARIOTAS", "levaduras y mohos", ["heterótrofos", "pared de quitina", "sin fotosíntesis"]),
        ("Protozoos", LILA, "EUCARIOTAS", "unicelulares", ["heterótrofos", "sin pared", "sin fotosíntesis"]),
        ("Virus", ROJO, "ACELULARES", "no son células", ["parásitos", "obligados", "sin metabolismo"]),
    ]
    for x, (n, c, org, sub, lis) in zip(xs, datos):
        b += f'<rect x="{x - 98}" y="128" width="196" height="330" rx="16" fill="#fff" stroke="{c}" stroke-width="2.5"/>'
        b += et(x, 156, n, c, 16 if len(n) < 12 else 14.5, w=900)
        if n == "Bacterias":
            b += bacteria(x - 12, 222, 1.0)
        elif n.startswith("Algas"):
            b += eucariota(x, 222, 42, "#eaf6e4", VERDE, cloro=True, pared=True)
        elif n == "Hongos":
            b += eucariota(x - 40, 226, 22, "#fff4df", ACC, pared=True)
            b += eucariota(x - 10, 206, 14, "#fff4df", ACC, pared=True)
            b += f'<path d="M{x + 18},{258} v-50 M{x + 18},{224} l18,-22 M{x + 36},{202} l8,-12 M{x + 36},{202} l14,-4 M{x + 36},{202} l4,-14" stroke="{ACC}" stroke-width="3" fill="none" stroke-linecap="round"/>'
            for dx, dy in ((8, -12), (14, -4), (4, -14)):
                b += f'<circle cx="{x + 36 + dx * 1.3}" cy="{202 + dy * 1.3}" r="3.5" fill="{ACC}"/>'
        elif n == "Protozoos":
            b += f'<path d="M{x - 50},222 q10,-40 45,-36 q40,-10 50,22 q14,30 -20,40 q-30,18 -55,0 q-30,-6 -20,-26z" fill="#efe7fb" stroke="{LILA}" stroke-width="3"/>'
            b += f'<circle cx="{x - 4}" cy="222" r="12" fill="#c9b7ef" stroke="{LILA}" stroke-width="2"/>'
            b += f'<circle cx="{x + 24}" cy="236" r="7" fill="#fff" stroke="{LILA}" stroke-width="1.5"/>'
        else:
            b += virus(x, 216)
        b += f'<rect x="{x - 78}" y="{290}" width="156" height="28" rx="14" fill="{c}"/>' + et(x, 309, org, "#fff", 13, w=900)
        b += et(x, 342, sub, GRIS, 12.5)
        for k, l in enumerate(lis):
            b += et(x, 372 + k * 22, l, INK, 13)
    b += et(560, 486, "Ejemplos: Lactobacillus, Streptomyces (bacterias) · Chlorella (alga) · Saccharomyces, Penicillium (hongos) · Plasmodium (protozoo)", PRI, 13, w=900)
    save("grupos-microorganismos.svg", svg(1120, 500, b, "Grupos de microorganismos y su organización celular"))


# ------------------------------------------------------------ fermentador
def fermentador():
    b = ""
    # tanque
    x0, y0, w, h = 380, 140, 260, 330
    b += f'<rect x="{x0 - 14}" y="{y0 + 40}" width="{w + 28}" height="{h - 60}" rx="30" fill="#e7f1fb" stroke="{PRI}" stroke-width="2" stroke-dasharray="7 5"/>'
    b += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="34" fill="#fff" stroke="{INK}" stroke-width="4"/>'
    b += f'<rect x="{x0 + 4}" y="{y0 + 90}" width="{w - 8}" height="{h - 94}" rx="30" fill="#fbe9c8"/>'
    b += f'<path d="M{x0 + 4},{y0 + 90} h{w - 8}" stroke="{ACC}" stroke-width="2"/>'
    # agitador
    cx = x0 + w / 2
    b += f'<rect x="{cx - 30}" y="{y0 - 50}" width="60" height="36" rx="6" fill="#dfe6ec" stroke="{INK}" stroke-width="2.5"/>' + et(cx, y0 - 27, "motor", INK, 12)
    b += linea(cx, y0 - 14, cx, y0 + 280, INK, 4)
    for yy in (y0 + 160, y0 + 250):
        b += f'<rect x="{cx - 48}" y="{yy - 7}" width="96" height="14" rx="4" fill="{GRIS}"/>'
    # burbujas
    for k, (dx, dy) in enumerate(((-80, 260), (-60, 220), (70, 270), (90, 200), (-90, 160), (60, 140), (-30, 300), (30, 190))):
        b += f'<circle cx="{cx + dx}" cy="{y0 + dy}" r="{4 + k % 3}" fill="#fff" stroke="{PRI}" stroke-width="1.5"/>'
    # microbios
    for dx, dy in ((-50, 120), (40, 230), (-95, 290), (95, 300), (10, 120), (-20, 205)):
        b += f'<rect x="{cx + dx - 9}" y="{y0 + dy - 4}" width="18" height="8" rx="4" fill="{TEAL}"/>'
    # entrada aire
    b += linea(x0 - 30, y0 + h - 20, cx - 20, y0 + h - 20, PRI, 3) + flecha(x0 - 200, y0 + h - 20, x0 + 30, y0 + h - 20, PRI, 3)
    b += et(x0 - 205, y0 + h - 34, "aire estéril (O₂)", PRI, 14, "start", 900) + et(x0 - 205, y0 + h + 2, "si el proceso es aerobio", GRIS, 12, "start")
    # entrada medio
    b += flecha(x0 - 200, y0 + 40, x0 + 40, y0 + 40, VERDE, 3)
    b += et(x0 - 205, y0 + 26, "medio de cultivo estéril", VERDE, 14, "start", 900) + et(x0 - 205, y0 + 62, "+ inóculo del microorganismo", GRIS, 12, "start")
    # salida gases
    b += flecha(x0 + w - 50, y0 + 4, x0 + w - 50, y0 - 50, GRIS, 3) + et(x0 + w - 40, y0 - 40, "gases (CO₂)", GRIS, 13, "start", 900)
    # sondas
    for k, (t, c) in enumerate((("T", ROJO), ("pH", LILA), ("O₂", PRI))):
        xx = x0 + w - 70 + k * 28
        b += linea(xx, y0 + 6, xx, y0 + 140, c, 3) + f'<circle cx="{xx}" cy="{y0 + 144}" r="5" fill="{c}"/>'
    b += et(x0 + w + 30, y0 + 120, "sensores: temperatura,", INK, 13, "start") + et(x0 + w + 30, y0 + 138, "pH, oxígeno, espuma", INK, 13, "start")
    b += et(x0 + w + 30, y0 + 200, "camisa de refrigeración", PRI, 13, "start", 900) + et(x0 + w + 30, y0 + 218, "(mantiene la temperatura", GRIS, 12, "start") + et(x0 + w + 30, y0 + 234, "óptima)", GRIS, 12, "start")
    # salida producto
    b += linea(cx, y0 + h, cx, y0 + h + 66, ACC, 3)
    b += caja(cx + 210, y0 + h + 66, 250, 48, "Separación y purificación", ACC, "#fff4df", 14)
    b += flecha(cx, y0 + h + 66, cx + 82, y0 + h + 66, ACC, 3)
    b += flecha(cx + 336, y0 + h + 66, cx + 386, y0 + h + 66, ACC, 3)
    b += et(cx + 392, y0 + h + 60, "PRODUCTO", ACC, 15, "start", 900) + et(cx + 392, y0 + h + 80, "antibiótico, insulina, enzima…", GRIS, 12, "start")
    b += et(560, 34, "FERMENTADOR o BIORREACTOR: cultivo a gran escala en condiciones controladas y estériles", PRI, 15, w=900)
    save("fermentador.svg", svg(1120, 570, b, "Esquema de un fermentador industrial"))


# ------------------------------------------------------------ antibióticos
def antibioticos():
    b = ""
    cx, cy = 360, 250
    b += f'<rect x="{cx - 220}" y="{cy - 110}" width="440" height="220" rx="110" fill="none" stroke="{ACC}" stroke-width="10"/>'
    b += f'<rect x="{cx - 206}" y="{cy - 96}" width="412" height="192" rx="96" fill="#eef8f6" stroke="{TEAL}" stroke-width="3"/>'
    b += f'<path d="M{cx - 120},{cy - 10} q20,-40 50,-6 t60,10 t50,-14 t40,20" fill="none" stroke="{INK}" stroke-width="3"/>'
    b += f'<circle cx="{cx + 110}" cy="{cy + 50}" r="16" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    for k in range(9):
        b += f'<circle cx="{cx - 150 + k * 20}" cy="{cy + 50 + (k % 2) * 10}" r="5" fill="{LILA}"/>'
    # etiquetas
    b += linea(cx - 190, cy - 70, cx - 220, cy - 132, GRIS, 1.5) + et(cx - 220, cy - 158, "PARED (peptidoglucano)", ACC, 13.5, w=900) + et(cx - 220, cy - 140, "penicilina, cefalosporinas", INK, 13)
    b += linea(cx - 120, cy + 58, cx - 180, cy + 150, GRIS, 1.5) + et(cx - 180, cy + 168, "RIBOSOMAS 70S (síntesis de proteínas)", LILA, 13.5, w=900) + et(cx - 180, cy + 186, "estreptomicina, tetraciclina, cloranfenicol", INK, 13)
    b += linea(cx - 40, cy - 30, cx + 40, cy - 150, GRIS, 1.5) + et(cx + 40, cy - 176, "ADN (replicación)", INK, 13.5, w=900) + et(cx + 40, cy - 158, "quinolonas", INK, 13)
    b += linea(cx + 180, cy - 60, cx + 200, cy - 112, GRIS, 1.5) + et(cx + 200, cy - 138, "MEMBRANA", TEAL, 13.5, w=900) + et(cx + 200, cy - 120, "polimixinas, gramicidinas", INK, 13)
    b += linea(cx + 120, cy + 64, cx + 170, cy + 150, GRIS, 1.5) + et(cx + 200, cy + 168, "plásmido: puede llevar", INK, 13) + et(cx + 200, cy + 186, "genes de resistencia", ROJO, 13, w=900)
    # columna derecha
    x = 700
    b += f'<rect x="{x}" y="60" width="360" height="370" rx="16" fill="#fff" stroke="{PRI}" stroke-width="2.5"/>'
    b += et(x + 180, 90, "¿Por qué no dañan a nuestras células?", PRI, 15, w=900)
    lineas = [("• Las células eucariotas no tienen", INK), ("  pared de peptidoglucano.", INK), ("• Sus ribosomas son 80S, no 70S.", INK),
              ("  (Ojo: las mitocondrias tienen 70S)", LILA), ("", INK),
              ("¿Y contra los virus?", ROJO), ("• No sirven: los virus no tienen", INK), ("  pared, ni ribosomas, ni metabolismo", INK), ("  propio. Se usan antivirales.", INK),
              ("", INK), ("Origen: hongos (Penicillium) y", ACC), ("bacterias (Streptomyces).", ACC)]
    for k, (l, c) in enumerate(lineas):
        if l:
            b += et(x + 22, 126 + k * 25, l, c, 14 if c != ROJO else 15, "start", 900 if c in (ROJO,) else 800)
    save("dianas-antibioticos.svg", svg(1080, 470, b, "Dianas de los antibióticos en la célula bacteriana"))


# ------------------------------------------------------------ resistencia
def resistencia():
    import random
    random.seed(7)
    b = ""
    paneles = [("1 · Población inicial", "casi todas sensibles; alguna resistente", 2),
               ("2 · Tratamiento con antibiótico", "mueren las sensibles", 2),
               ("3 · Tras varias generaciones", "las resistentes se han multiplicado", 22)]
    for i, (t, s, nres) in enumerate(paneles):
        x0 = 20 + i * 340
        b += f'<rect x="{x0}" y="20" width="310" height="260" rx="16" fill="#fff" stroke="{PRI}" stroke-width="2.5"/>'
        b += et(x0 + 155, 50, t, PRI, 15, w=900)
        pos = [(x0 + 40 + (k % 6) * 46, 90 + (k // 6) * 34) for k in range(24)]
        for k, (x, y) in enumerate(pos):
            x += random.randint(-6, 6)
            res = k in (5, 14) if nres == 2 else True
            if i == 1 and not res:
                b += f'<rect x="{x - 15}" y="{y - 6}" width="30" height="12" rx="6" fill="none" stroke="#b9c2c9" stroke-width="2" stroke-dasharray="3 3"/>'
                continue
            if i == 2 and k >= nres:
                continue
            col = ROJO if res else TEAL
            b += f'<rect x="{x - 15}" y="{y - 6}" width="30" height="12" rx="6" fill="{col}"/>'
        b += et(x0 + 155, 262, s, GRIS, 13)
        if i < 2:
            b += flecha(x0 + 312, 150, x0 + 336, 150, INK, 3)
    b += f'<rect x="300" y="300" width="18" height="10" rx="5" fill="{TEAL}"/>' + et(326, 310, "sensible", INK, 13, "start")
    b += f'<rect x="420" y="300" width="18" height="10" rx="5" fill="{ROJO}"/>' + et(446, 310, "resistente (por mutación o por un plásmido)", INK, 13, "start")
    b += et(510, 340, "El antibiótico no crea la resistencia: SELECCIONA a las bacterias que ya eran resistentes.", PRI, 14, w=900)
    save("resistencia-antibioticos.svg", svg(1030, 356, b, "Selección de bacterias resistentes a un antibiótico"))


# ------------------------------------------------------------ aplicaciones
def aplicaciones():
    campos = [
        ("Alimentación", ACC, "#fff4df", ["Pan, vino, cerveza (levaduras)", "Yogur, queso (bacterias lácticas)", "Vinagre (Acetobacter)", "Enzimas: quimosina (cuajo)"]),
        ("Salud y farmacia", LILA, "#efe7fb", ["Antibióticos (Penicillium,", "  Streptomyces)", "Insulina y hormona del", "  crecimiento recombinantes", "Vacunas (hepatitis B)"]),
        ("Industria química", PRI, "#e3eef8", ["Aminoácidos (glutamato, lisina)", "Ácidos orgánicos (cítrico)", "Enzimas de detergentes", "Bioplásticos"]),
        ("Energía", "#8a6d00", "#fbf3d1", ["Bioetanol (levaduras)", "Biogás: metano por digestión", "  anaerobia de residuos", "  (arqueas metanógenas)"]),
        ("Medio ambiente", VERDE, "#e5f4ec", ["Biorremediación (mareas negras)", "Depuración de aguas", "Compostaje", "Biolixiviación de metales"]),
        ("Agricultura", TEAL, "#e0f3f1", ["Fijación de N₂ (Rhizobium)", "Bioinsecticidas (Bacillus", "  thuringiensis)", "Plantas transgénicas"]),
    ]
    b = ""
    for i, (t, c, f, ej) in enumerate(campos):
        x = 10 + (i % 3) * 340
        y = 10 + (i // 3) * 220
        b += f'<rect x="{x}" y="{y}" width="330" height="205" rx="16" fill="{f}" stroke="{c}" stroke-width="2.5"/>'
        b += et(x + 165, y + 34, t, c, 18, w=900)
        for k, e in enumerate(ej):
            ind = e.startswith("  ")
            b += et(x + (36 if ind else 22), y + 72 + k * 30, ("" if ind else "• ") + e.strip(), INK, 14, "start")
    save("aplicaciones-biotecnologia.svg", svg(1030, 450, b, "Campos de aplicación de la biotecnología con microorganismos"))


# ------------------------------------------------------------ depuradora
def depuradora():
    b = ""
    y = 150
    etapas = [(90, "Agua residual", GRIS, "#eef1f4", None),
              (270, "Pretratamiento", GRIS, "#eef1f4", "rejas, arenas, grasas"),
              (460, "Primario", PRI, "#e3eef8", "decantación de sólidos"),
              (680, "Secundario (biológico)", VERDE, "#e5f4ec", None),
              (890, "Decantador", PRI, "#e3eef8", "secundario"),
              (1060, "Agua al río", TEAL, "#e0f3f1", "o reutilización")]
    for x, t, c, f, s in etapas:
        ancho = 230 if "Secundario" in t else 150
        alto = 150 if "Secundario" in t else 64
        b += caja(x, y, ancho, alto, t, c, f, 14 if len(t) < 16 else 13.5, s) if "Secundario" not in t else f'<rect x="{x - ancho / 2}" y="{y - alto / 2}" width="{ancho}" height="{alto}" rx="14" fill="{f}" stroke="{c}" stroke-width="3"/>'
    for a, bb in ((90, 270), (270, 460), (460, 680), (680, 890), (890, 1060)):
        w1 = 75 if a in (90, 270, 460, 890) else 115
        w2 = 75 if bb != 680 else 115
        b += flecha(a + w1 + 2, y, bb - w2 - 4, y, PRI, 3.5)
    # detalle secundario
    b += et(680, 96, "Secundario (biológico)", VERDE, 15, w=900)
    for dx, dy in ((-70, 6), (-30, 30), (20, 4), (60, 24), (-60, 44), (40, 46), (0, 18)):
        b += f'<rect x="{680 + dx - 10}" y="{y + dy - 4}" width="20" height="8" rx="4" fill="{TEAL}"/>'
    for dx in (-80, -40, 0, 40, 80):
        b += f'<circle cx="{680 + dx}" cy="{y + 64}" r="4" fill="#fff" stroke="{PRI}" stroke-width="1.5"/>'
    b += et(680, y - 34, "bacterias aerobias + aireación", INK, 12.5)
    b += et(680, y - 18, "oxidan la materia orgánica", INK, 12.5)
    # fangos
    b += flecha(460, y + 34, 460, 300, GRIS, 3) + flecha(890, y + 34, 890, 270, GRIS, 3)
    b += linea(890, 270, 890, 300, GRIS, 3) + linea(890, 300, 600, 300, GRIS, 3) + flecha(890, 300, 610, 300, GRIS, 3)
    b += et(660, 290, "fangos", GRIS, 12.5, w=900) + et(420, 250, "fangos", GRIS, 12.5, "end", 900)
    b += caja(520, 320, 170, 60, "Digestor anaerobio", ROJO, "#fdeaea", 14, "arqueas metanógenas")
    b += flecha(480, 352, 430, 394, ROJO, 3) + flecha(580, 352, 700, 380, ROJO, 3)
    b += caja(400, 420, 220, 44, "Biogás (metano) → energía", ROJO, "#fff", 13.5)
    b += caja(780, 404, 230, 44, "Fango estabilizado → abono", VERDE, "#fff", 13.5)
    b += et(560, 30, "DEPURACIÓN BIOLÓGICA DE AGUAS RESIDUALES (EDAR)", PRI, 16, w=900)
    save("depuradora.svg", svg(1140, 460, b, "Esquema de una estación depuradora de aguas residuales"))


# ------------------------------------------------------------ medio ambiente
def ambiente():
    paneles = [
        ("Biorremediación", VERDE, "#e5f4ec", ["Microorganismos que degradan", "contaminantes: hidrocarburos", "(mareas negras), insecticidas,", "disolventes…", "→ recuperan el ecosistema"]),
        ("Compostaje", ACC, "#fff4df", ["Restos orgánicos (poda,", "estiércol, residuos de cosecha)", "degradados por bacterias y", "hongos en presencia de O₂", "→ compost (abono)"]),
        ("Biolixiviación", PRI, "#e3eef8", ["Bacterias quimiosintéticas", "(Acidithiobacillus) oxidan", "sulfuros del mineral y liberan", "metales (cobre) en disolución", "→ aprovecha minerales pobres"]),
        ("Fijación de N₂", TEAL, "#e0f3f1", ["Rhizobium en nódulos de las", "raíces de leguminosas:", "N₂ atmosférico → amonio", "que usa la planta", "→ menos abonos químicos"]),
    ]
    b = ""
    for i, (t, c, f, ej) in enumerate(paneles):
        x = 10 + i * 262
        b += f'<rect x="{x}" y="10" width="250" height="230" rx="16" fill="{f}" stroke="{c}" stroke-width="2.5"/>'
        b += et(x + 125, 42, t, c, 17, w=900)
        for k, e in enumerate(ej):
            fin = e.startswith("→")
            b += et(x + 125, 80 + k * 30, e, c if fin else INK, 13.5, w=900 if fin else 800)
    save("medio-ambiente.svg", svg(1060, 250, b, "Microorganismos en la mejora del medio ambiente"))


if __name__ == "__main__":
    grupos(); fermentador(); antibioticos(); resistencia(); aplicaciones(); depuradora(); ambiente()
