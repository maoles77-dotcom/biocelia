# Esquemas SVG del tema A2 (glúcidos) de BioCelia.
# Uso: python tools/esquemas_tema_a2.py
# Proyecciones de Haworth: se dibujan los –OH y los grupos –CH2OH; se omiten los H por claridad.
# Convención D: lo que en Fischer está a la derecha queda abajo en Haworth.
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, P, d, INK, BLUE

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "a2")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b"


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)


def save(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def linea(a, b, w=2.2, col=INK, extra=""):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def grupo(x, y, et, size=15, anchor="middle"):
    col = ROJO if et.startswith("O") or et.endswith("OH") else INK
    if et == "CH₂OH":
        col = INK
    return text(x, y + size * 0.35, et, size, anchor, 800, fill=col)


# ─── Haworth ──────────────────────────────────────────────────────────────
PIRANOSA = {"O": (40, -28), 1: (75, 0), 2: (40, 28), 3: (-40, 28), 4: (-75, 0), 5: (-40, -28)}
FURANOSA = {"O": (0, -32), 1: (62, -8), 2: (38, 30), 3: (-38, 30), 4: (-62, -8)}


def anillo(cx, cy, geo, subs, k=1.0, etiqueta_c=False, resalta=None, rot=False):
    """subs: {carbono: (arriba, abajo)} con textos ('' = nada). rot=True gira 180° sobre el eje vertical
    (izquierda↔derecha y delante↔detrás; arriba y abajo se conservan)."""
    def pos(key):
        x, y = geo[key]
        if rot:
            x, y = -x, -y
        return (cx + x * k, cy + y * k)
    orden = ["O"] + sorted(c for c in geo if c != "O")
    pts = [pos(c) for c in orden]
    s = ""
    n = len(pts)
    for i in range(n):
        a, b = pts[i], pts[(i + 1) % n]
        delante = (a[1] > cy and b[1] > cy - 2) or (b[1] > cy and a[1] > cy - 2)
        s += linea(a, b, 6.5 if delante else 2.6)
    o = pos("O")
    s += f'<circle cx="{o[0]:.1f}" cy="{o[1]:.1f}" r="{11 * k:.1f}" fill="#fff"/>' + text(o[0], o[1] + 6 * k, "O", 17 * k, weight=900, fill=ROJO)
    L = 32 * k
    for c, (arr, abj) in subs.items():
        x, y = pos(c)
        for et, sgn in ((arr, -1), (abj, 1)):
            if not et:
                continue
            fin = (x, y + sgn * L)
            col = ACC if resalta == c else INK
            s += linea((x, y), (x, fin[1] + sgn * (-7 * k)), 2.2, col)
            lado = x - cx
            if abs(lado) > 50 * k:
                s += grupo(x + (3 if lado > 0 else -3) * k, fin[1] + sgn * 4 * k, et, 14 * k, "start" if lado > 0 else "end")
            else:
                s += grupo(x, fin[1] + sgn * 4 * k, et, 14 * k)
        if etiqueta_c:
            dx = 14 * k if x >= cx else -14 * k
            s += text(x + dx, y + (12 * k if y > cy else -4 * k), str(c), 11 * k, "middle", 800, fill=LILA)
    if resalta:
        x, y = pos(resalta)
        s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{8 * k:.1f}" fill="none" stroke="{ACC}" stroke-width="2.5"/>'
    return s, pos


GLC_A = {1: ("", "OH"), 2: ("", "OH"), 3: ("OH", ""), 4: ("", "OH"), 5: ("CH₂OH", "")}
GLC_B = {1: ("OH", ""), 2: ("", "OH"), 3: ("OH", ""), 4: ("", "OH"), 5: ("CH₂OH", "")}
GAL_B = {1: ("OH", ""), 2: ("", "OH"), 3: ("OH", ""), 4: ("OH", ""), 5: ("CH₂OH", "")}
RIB_B = {1: ("OH", ""), 2: ("", "OH"), 3: ("", "OH"), 4: ("CH₂OH", "")}
DRIB_B = {1: ("OH", ""), 3: ("", "OH"), 4: ("CH₂OH", "")}
# Fructofuranosa: el carbono anomérico es el C2 (posición 1 del pentágono), el C3 es la 2, el C4 la 3 y el C5 la 4.
FRU_B = {1: ("OH", "CH₂OH"), 2: ("OH", ""), 3: ("", "OH"), 4: ("CH₂OH", "")}


# ─── Fischer ──────────────────────────────────────────────────────────────
def fischer(x, y, arriba, filas, abajo, paso=42, size=17, nombre=None, sub=None, asim=False):
    s = ""
    yy = y
    s += grupo(x, yy, arriba, size)
    for izq, der in filas:
        yy += paso
        s += linea((x, yy - paso + 12), (x, yy - 10), 2.4)
        if izq == "=O":
            s += text(x, yy + 6, "C", size, weight=900)
            s += f'<line x1="{x + 11}" y1="{yy - 3}" x2="{x + 34}" y2="{yy - 3}" stroke="{INK}" stroke-width="2.2"/><line x1="{x + 11}" y1="{yy + 3}" x2="{x + 34}" y2="{yy + 3}" stroke="{INK}" stroke-width="2.2"/>'
            s += grupo(x + 50, yy, "O", size)
            continue
        c = "C*" if asim and izq != der else "C"
        s += text(x, yy + 6, c if c == "C" else "C", size, weight=900, fill=ACC if c == "C*" else INK)
        if c == "C*":
            s += text(x + 9, yy - 6, "*", 14, "start", 900, fill=ACC)
        s += linea((x - 11, yy), (x - 34, yy), 2.2) + linea((x + 11, yy), (x + 34, yy), 2.2)
        s += grupo(x - 40, yy, izq, size, "end") + grupo(x + 40, yy, der, size, "start")
    yy += paso
    s += linea((x, yy - paso + 12), (x, yy - 10), 2.4)
    s += grupo(x, yy, abajo, size)
    if nombre:
        s += text(x, yy + 36, nombre, 17, weight=900, fill=PRI)
    if sub:
        s += text(x, yy + 56, sub, 13, weight=700, fill=GRIS)
    return s


def fischer_monosacaridos():
    b = ""
    datos = [
        ("CHO", [("H", "OH")], "CH₂OH", "D-gliceraldehído", "aldotriosa"),
        ("CH₂OH", [("=O", "")], "CH₂OH", "Dihidroxiacetona", "cetotriosa"),
        ("CHO", [("H", "OH"), ("H", "OH"), ("H", "OH")], "CH₂OH", "D-ribosa", "aldopentosa"),
        ("CHO", [("H", "H"), ("H", "OH"), ("H", "OH")], "CH₂OH", "D-desoxirribosa", "2-desoxialdopentosa"),
        ("CHO", [("H", "OH"), ("HO", "H"), ("H", "OH"), ("H", "OH")], "CH₂OH", "D-glucosa", "aldohexosa"),
        ("CHO", [("H", "OH"), ("HO", "H"), ("HO", "H"), ("H", "OH")], "CH₂OH", "D-galactosa", "aldohexosa"),
        ("CH₂OH", [("=O", ""), ("HO", "H"), ("H", "OH"), ("H", "OH")], "CH₂OH", "D-fructosa", "cetohexosa"),
    ]
    for i, (a, f, ab, nom, sub) in enumerate(datos):
        x = 90 + i * 165
        b += fischer(x, 40, a, f, ab, nombre=nom, sub=sub)
    b += text(590, 345, "En la serie D, el –OH del carbono asimétrico más alejado del carbonilo está a la derecha.", 15, weight=700, fill=GRIS)
    save("fischer-monosacaridos.svg", svg(1180, 360, b, "Proyecciones de Fischer del gliceraldehído, la dihidroxiacetona, la ribosa, la desoxirribosa, la glucosa, la galactosa y la fructosa"))


def isomeria():
    b = ""
    b += fischer(150, 70, "CHO", [("H", "OH")], "CH₂OH", paso=55, size=20, nombre="D-gliceraldehído", asim=True)
    b += fischer(450, 70, "CHO", [("HO", "H")], "CH₂OH", paso=55, size=20, nombre="L-gliceraldehído", asim=True)
    b += f'<line x1="300" y1="40" x2="300" y2="220" stroke="{GRIS}" stroke-width="2" stroke-dasharray="7 6"/>'
    b += text(300, 30, "espejo", 14, weight=800, fill=GRIS)
    b += text(300, 290, "Enantiómeros: imágenes especulares no superponibles", 17, weight=900, fill=PRI)
    b += text(300, 314, "C* = carbono asimétrico (4 sustituyentes distintos)", 14, weight=700, fill=ACC)
    save("isomeria-gliceraldehido.svg", svg(600, 330, b, "D-gliceraldehído y L-gliceraldehído: enantiómeros con un carbono asimétrico"))


def ciclacion():
    b = fischer(110, 60, "CHO", [("H", "OH"), ("HO", "H"), ("H", "OH"), ("H", "OH")], "CH₂OH", paso=46, nombre="D-glucosa", sub="forma lineal")
    b += text(150, 66, "C1", 13, "start", 800, fill=LILA) + text(18, 250, "C5", 13, "start", 800, fill=LILA)
    b += f'<line x1="230" y1="180" x2="300" y2="140" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    b += f'<line x1="230" y1="200" x2="300" y2="250" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    b += text(265, 205, "ciclación", 14, weight=800, fill=GRIS)
    s1, _ = anillo(430, 120, PIRANOSA, GLC_A, 1.0, True, resalta=1)
    s2, _ = anillo(430, 300, PIRANOSA, GLC_B, 1.0, True, resalta=1)
    b += s1 + s2
    b += text(560, 120, "α-D-glucopiranosa", 17, "start", 900, fill=PRI) + text(560, 142, "–OH del C1 hacia abajo", 14, "start", 700, fill=GRIS)
    b += text(560, 300, "β-D-glucopiranosa", 17, "start", 900, fill=PRI) + text(560, 322, "–OH del C1 hacia arriba", 14, "start", 700, fill=GRIS)
    b += text(560, 200, "C1 = carbono anomérico", 16, "start", 900, fill=ACC)
    b += text(450, 395, "El C1 del aldehído reacciona con el –OH del C5 y se cierra el anillo (hemiacetal).", 14, weight=700, fill=GRIS)
    save("ciclacion-glucosa.svg", svg(820, 410, b, "Ciclación de la D-glucosa: forma lineal y anómeros alfa y beta"))


def ciclicos():
    b = ""
    items = [
        (PIRANOSA, GLC_B, "β-D-glucosa", "piranosa (anillo de 6)"),
        (PIRANOSA, GAL_B, "β-D-galactosa", "–OH del C4 arriba"),
        (FURANOSA, FRU_B, "β-D-fructosa", "furanosa (anillo de 5)"),
        (FURANOSA, RIB_B, "β-D-ribosa", "furanosa"),
        (FURANOSA, DRIB_B, "β-D-desoxirribosa", "sin –OH en el C2"),
    ]
    for i, (geo, subs, nom, sub) in enumerate(items):
        x = 110 + i * 205
        s, _ = anillo(x, 120, geo, subs, 0.95)
        b += s + text(x, 230, nom, 17, weight=900, fill=PRI) + text(x, 252, sub, 13, weight=700, fill=GRIS)
    save("monosacaridos-ciclicos.svg", svg(1040, 268, b, "Fórmulas cíclicas de la glucosa, la galactosa, la fructosa, la ribosa y la desoxirribosa"))


def puente(a, o, b2):
    return linea(a, (o[0], o[1]), 2.4) + linea((o[0], o[1]), b2, 2.4) + f'<circle cx="{o[0]}" cy="{o[1]}" r="11" fill="#fff"/>' + text(o[0], o[1] + 6, "O", 17, weight=900, fill=ROJO)


def disacarido_14(x0, y0, sub1, sub2, beta, k=0.85):
    """Monosacárido 1 (C1, α abajo o β arriba) unido al C4 de la glucosa 2."""
    s1 = dict(sub1)
    s1[1] = ("", "")  # el –OH del C1 forma el enlace
    s2 = dict(sub2)
    s2[4] = ("", "")
    a, p1 = anillo(x0, y0, PIRANOSA, s1, k)
    c, p2 = anillo(x0 + 200 * k, y0, PIRANOSA, s2, k)
    c1, c4 = p1(1), p2(4)
    o = ((c1[0] + c4[0]) / 2, y0 + (-34 if beta else 34) * k)
    return a + c + puente(c1, o, c4), o


def disacaridos():
    b = ""
    k = 0.85
    # maltosa
    s, o = disacarido_14(90, 110, GLC_A, GLC_A, False, k)
    b += s + text(175, 215, "Maltosa", 19, weight=900, fill=PRI) + text(175, 236, "Glc α(1→4) Glc · reductora", 14, weight=700, fill=GRIS)
    b += text(o[0], o[1] + 30, "α(1→4)", 13, weight=900, fill=ACC)
    # celobiosa
    s, o = disacarido_14(530, 110, GLC_B, GLC_A, True, k)
    b += s + text(615, 215, "Celobiosa", 19, weight=900, fill=PRI) + text(615, 236, "Glc β(1→4) Glc · reductora", 14, weight=700, fill=GRIS)
    b += text(o[0], o[1] - 18, "β(1→4)", 13, weight=900, fill=ACC)
    # lactosa
    s, o = disacarido_14(90, 350, GAL_B, GLC_A, True, k)
    b += s + text(175, 455, "Lactosa", 19, weight=900, fill=PRI) + text(175, 476, "Gal β(1→4) Glc · reductora", 14, weight=700, fill=GRIS)
    b += text(o[0], o[1] - 18, "β(1→4)", 13, weight=900, fill=ACC)
    # sacarosa: α-glucosa C1 – O – C2 de la β-fructosa (anillo girado)
    sg = dict(GLC_A)
    sg[1] = ("", "")
    g, pg = anillo(560, 330, PIRANOSA, sg, k)
    fru = {1: ("", "CH₂OH"), 2: ("OH", ""), 3: ("", "OH"), 4: ("CH₂OH", "")}
    f, pf = anillo(700, 420, FURANOSA, fru, k, rot=True)
    c1, c2 = pg(1), pf(1)
    o = (c1[0] + 10, c1[1] + 42)
    b += g + f + linea(c1, o, 2.4) + linea(o, c2, 2.4) + f'<circle cx="{o[0]}" cy="{o[1]}" r="11" fill="#fff"/>' + text(o[0], o[1] + 6, "O", 17, weight=900, fill=ROJO)
    b += text(860, 330, "Sacarosa", 19, "start", 900, fill=PRI) + text(860, 351, "Glc α(1→2)β Fru", 14, "start", 700, fill=GRIS)
    b += text(860, 371, "no reductora: une los", 14, "start", 700, fill=GRIS) + text(860, 389, "dos C anoméricos", 14, "start", 700, fill=GRIS)
    save("disacaridos.svg", svg(1060, 500, b, "Maltosa, celobiosa, lactosa y sacarosa con sus enlaces O-glucosídicos"))


def enlace():
    k = 0.8
    b = ""
    s1, p1 = anillo(90, 110, PIRANOSA, GLC_A, k)
    s2, p2 = anillo(320, 110, PIRANOSA, GLC_A, k)
    b += s1 + s2 + text(205, 112, "+", 30, weight=900)
    # resaltar OH implicados
    c1 = p1(1)
    c4 = p2(4)
    b += f'<rect x="{c1[0] - 18}" y="{c1[1] + 20}" width="36" height="24" rx="6" fill="none" stroke="{ACC}" stroke-width="2.5"/>'
    b += f'<rect x="{c4[0] - 18}" y="{c4[1] + 20}" width="36" height="24" rx="6" fill="none" stroke="{ACC}" stroke-width="2.5"/>'
    b += f'<line x1="430" y1="100" x2="500" y2="100" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    b += f'<line x1="500" y1="125" x2="430" y2="125" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    b += text(465, 88, "condensación", 13, weight=800, fill=PRI) + text(465, 148, "hidrólisis", 13, weight=800, fill=TEAL)
    b += text(465, 168, "(+ H₂O)", 12, weight=700, fill=TEAL)
    s, o = disacarido_14(590, 110, GLC_A, GLC_A, False, k)
    b += s + text(o[0], o[1] + 58, "enlace O-glucosídico α(1→4)", 13, weight=900, fill=ACC)
    b += text(900, 112, "+ H₂O", 20, "start", 900, fill=BLUE)
    b += text(495, 235, "El –OH del carbono anomérico (C1) reacciona con un –OH de otro monosacárido y se libera una molécula de agua.", 14, weight=700, fill=GRIS)
    save("enlace-o-glucosidico.svg", svg(990, 250, b, "Formación del enlace O-glucosídico entre dos glucosas para dar maltosa y agua"))


# ─── Polisacáridos (esquema) ────────────────────────────────────────────────
def hexa(x, y, r=11, fill="#7fb3d5", stroke="#2c6e9e"):
    pts = " ".join(f"{x + r * math.cos(math.radians(60 * k + 30)):.1f},{y + r * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
    return f'<polygon points="{pts}" fill="{fill}" stroke="{stroke}" stroke-width="1.5"/>'


def polisacaridos():
    b = ""
    # amilosa: hélice
    for i in range(16):
        x = 40 + i * 17
        y = 110 + 32 * math.sin(i * 0.9)
        fr = math.cos(i * 0.9) > 0
        b += hexa(x, y, 10, "#7fb3d5" if fr else "#c4dcef")
    b += text(170, 215, "Amilosa", 18, weight=900, fill=PRI) + text(170, 234, "lineal, α(1→4), en hélice", 13, weight=700, fill=GRIS)

    def arbol(x0, y0, ramas, col, st):
        s = ""
        for (x1, y1, x2, y2) in ramas:
            n = int(math.hypot(x2 - x1, y2 - y1) // 18) + 1
            for j in range(n):
                t = j / max(1, n - 1)
                s += hexa(x0 + x1 + (x2 - x1) * t, y0 + (y1 + (y2 - y1) * t) * 0.8, 8, col, st)
        return s
    ramas_ap = [(0, 0, 230, 0), (60, 0, 140, -60), (140, 0, 220, 60), (100, -30, 170, -95), (180, 30, 250, 80)]
    b += arbol(340, 110, ramas_ap, "#f2c27b", "#b07d1f")
    b += text(460, 215, "Amilopectina", 18, weight=900, fill=PRI) + text(460, 234, "α(1→4) + ramas α(1→6)", 13, weight=700, fill=GRIS)
    ramas_gl = [(0, 0, 220, 0), (30, 0, 90, -60), (70, 0, 130, 55), (110, 0, 170, -60), (150, 0, 210, 55), (60, -30, 20, -80), (100, 28, 60, 80), (140, -30, 200, -95), (180, 28, 230, 85)]
    b += arbol(640, 110, ramas_gl, "#f4a6b8", "#c0607a")
    b += text(750, 215, "Glucógeno", 18, weight=900, fill=PRI) + text(750, 234, "como la amilopectina, más ramificado", 13, weight=700, fill=GRIS)
    # celulosa: cadenas paralelas con puentes de H
    for j in range(4):
        y = 70 + j * 32
        for i in range(12):
            b += hexa(920 + i * 19, y, 9, "#9ed49a", "#2c6e2a")
        if j < 3:
            for i in range(0, 12, 2):
                b += f'<line x1="{922 + i * 19}" y1="{y + 10}" x2="{922 + i * 19}" y2="{y + 22}" stroke="{BLUE}" stroke-width="2" stroke-dasharray="3 3"/>'
    b += text(1025, 215, "Celulosa", 18, weight=900, fill=PRI) + text(1025, 234, "lineal, β(1→4); puentes de H → fibras", 13, weight=700, fill=GRIS)
    b += text(600, 268, "Cada hexágono es una glucosa. Esquema sin escala.", 13, weight=700, fill=GRIS)
    save("polisacaridos.svg", svg(1160, 280, b, "Esquema de la amilosa en hélice, la amilopectina y el glucógeno ramificados y la celulosa en cadenas paralelas"))


# ─── Localización y función ───────────────────────────────────────────────
def funciones():
    b = ""
    # patata (almidón)
    b += '<ellipse cx="110" cy="95" rx="70" ry="48" fill="#d9b56f" stroke="#9a7330" stroke-width="2.5"/>'
    for x, y in ((80, 80), (130, 70), (110, 115), (150, 105)):
        b += f'<circle cx="{x}" cy="{y}" r="3.5" fill="#9a7330"/>'
    b += text(110, 180, "Almidón", 19, weight=900, fill=PRI) + text(110, 200, "reserva en vegetales", 14, weight=700, fill=GRIS) + text(110, 218, "(amiloplastos: tubérculos, semillas)", 12, weight=600, fill=GRIS)
    # hígado y músculo (glucógeno)
    b += '<path d="M290,60 C350,40 420,50 430,80 C440,115 380,140 330,135 C300,130 270,100 290,60z" fill="#b5533c" stroke="#7e3424" stroke-width="2.5"/>'
    b += text(360, 180, "Glucógeno", 19, weight=900, fill=PRI) + text(360, 200, "reserva en animales", 14, weight=700, fill=GRIS) + text(360, 218, "(hígado y músculo)", 12, weight=600, fill=GRIS)
    # pared celular (celulosa)
    b += '<rect x="550" y="45" width="130" height="95" rx="10" fill="#e3f4df" stroke="#3f8a3a" stroke-width="7"/>'
    b += '<rect x="566" y="60" width="98" height="65" rx="8" fill="#b9e3b3"/><circle cx="615" cy="92" r="14" fill="#7aa86f"/>'
    b += text(615, 180, "Celulosa", 19, weight=900, fill=PRI) + text(615, 200, "estructural", 14, weight=700, fill=GRIS) + text(615, 218, "(pared de la célula vegetal)", 12, weight=600, fill=GRIS)
    # escarabajo (quitina)
    b += '<ellipse cx="870" cy="100" rx="38" ry="50" fill="#3d5a3a" stroke="#1f3320" stroke-width="2.5"/><line x1="870" y1="52" x2="870" y2="150" stroke="#1f3320" stroke-width="2"/>'
    b += '<circle cx="870" cy="50" r="15" fill="#3d5a3a"/>'
    for sgn in (-1, 1):
        for yy in (80, 100, 120):
            b += f'<line x1="{870 + sgn * 36}" y1="{yy}" x2="{870 + sgn * 62}" y2="{yy + 12}" stroke="#1f3320" stroke-width="3"/>'
    b += text(870, 180, "Quitina", 19, weight=900, fill=PRI) + text(870, 200, "estructural", 14, weight=700, fill=GRIS) + text(870, 218, "(exoesqueleto de artrópodos, pared de hongos)", 12, weight=600, fill=GRIS)
    b += text(240, 252, "Enlaces α → reserva energética (se hidrolizan con facilidad)", 15, weight=900, fill=ACC)
    b += text(745, 252, "Enlaces β → función estructural (fibras resistentes)", 15, weight=900, fill="#3f8a3a")
    save("polisacaridos-funciones.svg", svg(1000, 268, b, "Dónde están y para qué sirven el almidón, el glucógeno, la celulosa y la quitina"))


# ─── Pruebas de laboratorio ───────────────────────────────────────────────
def tubo(x, col_liq, et, sub, col_et=INK):
    s = f'<path d="M{x - 22},40 V190 A22,22 0 0 0 {x + 22},190 V40" fill="#fff" stroke="#7b8a97" stroke-width="3"/>'
    s += f'<path d="M{x - 20},110 V190 A20,20 0 0 0 {x + 20},190 V110z" fill="{col_liq}"/>'
    s += f'<rect x="{x - 27}" y="32" width="54" height="10" rx="4" fill="#cfd8df"/>'
    s += text(x, 240, et, 15, weight=900, fill=col_et) + text(x, 258, sub, 12, weight=700, fill=GRIS)
    return s


def pruebas():
    b = text(175, 20, "Benedict (o Fehling): azúcares reductores", 15, weight=900, fill=PRI)
    b += tubo(80, "#3b7dd8", "Negativo", "sigue azul") + tubo(250, "#c0392b", "Positivo", "rojo ladrillo")
    b += text(165, 290, "glucosa, fructosa, maltosa, lactosa: +", 13, weight=800) + text(165, 308, "sacarosa y polisacáridos: −", 13, weight=800)
    b += f'<line x1="355" y1="30" x2="355" y2="310" stroke="#dde5ec" stroke-width="2"/>'
    b += text(545, 20, "Lugol: almidón", 16, weight=900, fill=PRI)
    b += tubo(460, "#d9a441", "Negativo", "amarillo-pardo") + tubo(630, "#1f2a5a", "Positivo", "azul-negro")
    b += text(545, 290, "el yodo se aloja en la hélice de la amilosa", 13, weight=800)
    save("pruebas-benedict-lugol.svg", svg(720, 320, b, "Resultados de las pruebas de Benedict o Fehling y de Lugol"))


# ─── Clasificación ────────────────────────────────────────────────────────
def clasificacion():
    def caja(x, y, w, t, sub="", col=PRI, fondo="#e7f0f8"):
        s = f'<rect x="{x - w / 2}" y="{y - 24}" width="{w}" height="{48 if sub else 40}" rx="12" fill="{fondo}" stroke="{col}" stroke-width="2"/>'
        s += text(x, y + (0 if sub else 4), t, 16, weight=900, fill=col)
        if sub:
            s += text(x, y + 17, sub, 12, weight=700, fill=GRIS)
        return s

    def ln(a, b2):
        return f'<path d="M{a[0]},{a[1]} V{(a[1] + b2[1]) / 2} H{b2[0]} V{b2[1]}" fill="none" stroke="#9aa8b4" stroke-width="2"/>'
    b = ""
    b += ln((520, 50), (220, 120)) + ln((520, 50), (720, 120))
    b += ln((720, 145), (600, 210)) + ln((720, 145), (900, 210))
    b += ln((600, 235), (480, 300)) + ln((600, 235), (720, 300))
    b += ln((220, 145), (220, 210))
    b += caja(520, 34, 180, "GLÚCIDOS", "", "#fff", PRI)
    b += caja(220, 120, 290, "Monosacáridos (osas)", "no hidrolizables · 3-7 C")
    b += caja(720, 120, 200, "Ósidos", "hidrolizables")
    b += caja(220, 214, 330, "Aldosas / cetosas", "triosas, tetrosas, pentosas, hexosas…", TEAL, "#e3f4f1")
    b += caja(600, 214, 220, "Holósidos", "solo monosacáridos")
    b += caja(900, 214, 240, "Heterósidos", "osas + otra molécula", ACC, "#fff4df")
    b += caja(480, 304, 240, "Oligosacáridos", "2-10 osas (disacáridos)", TEAL, "#e3f4f1")
    b += caja(720, 304, 220, "Polisacáridos", "muchas osas", TEAL, "#e3f4f1")
    b += text(720, 352, "homopolisacáridos (un tipo de osa) · heteropolisacáridos (varios)", 13, weight=700, fill=GRIS)
    save("clasificacion-glucidos.svg", svg(1040, 365, b, "Clasificación de los glúcidos en monosacáridos y ósidos"))


# ─── Glucemia (esquema cualitativo) ─────────────────────────────────────────
def glucemia():
    x0, y0, W, H = 80, 30, 520, 220
    b = f'<line x1="{x0}" y1="{y0 + H}" x2="{x0 + W}" y2="{y0 + H}" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
    b += f'<line x1="{x0}" y1="{y0 + H}" x2="{x0}" y2="{y0 - 10}" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
    b += text(x0 + W, y0 + H + 24, "tiempo tras la ingesta", 14, "end", 800)
    b += f'<text x="30" y="{y0 + H / 2}" font-size="14" font-weight="800" fill="{INK}" transform="rotate(-90 30 {y0 + H / 2})" text-anchor="middle" font-family="Nunito, Segoe UI, sans-serif">glucosa en sangre</text>'
    base_y = y0 + H - 40

    def curva(pico_x, pico_y, col, w=3.5):
        return (f'<path d="M{x0},{base_y} C{x0 + pico_x * 0.5},{base_y} {x0 + pico_x * 0.6},{pico_y} {x0 + pico_x},{pico_y} '
                f'S{x0 + pico_x * 1.6},{base_y} {x0 + W - 20},{base_y}" fill="none" stroke="{col}" stroke-width="{w}"/>')
    b += curva(110, y0 + 20, ROJO) + curva(220, y0 + 80, ACC)
    b += f'<line x1="{x0}" y1="{base_y}" x2="{x0 + W - 20}" y2="{base_y}" stroke="#3f8a3a" stroke-width="3.5" stroke-dasharray="9 6"/>'
    b += text(x0 + 120, y0 + 10, "glucosa: se absorbe directamente", 14, "start", 900, fill=ROJO)
    b += text(x0 + 245, y0 + 74, "almidón: antes hay que hidrolizarlo", 14, "start", 900, fill="#8a5600")
    b += text(x0 + W - 20, base_y + 22, "celulosa: no la digerimos", 14, "end", 900, fill="#3f8a3a")
    b += text(340, 300, "Esquema cualitativo (sin valores), según los criterios de la PAU 2013.", 12, weight=700, fill=GRIS)
    save("glucemia-glucosa-almidon-celulosa.svg", svg(640, 312, b, "Subida de la glucemia tras ingerir glucosa, almidón o celulosa"))


if __name__ == "__main__":
    for f in (fischer_monosacaridos, isomeria, ciclacion, ciclicos, disacaridos, enlace, polisacaridos, funciones, pruebas, clasificacion, glucemia):
        f()
