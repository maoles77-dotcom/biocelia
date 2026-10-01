# Ilustraciones adicionales del tema A1 (sobre todo para la presentación).
# Uso: python tools/esquemas_tema_a1_extra.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, molecule, hbond, P, d, INK, BLUE, O_STROKE


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)

GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0"
COL_AT = {"O": "#c0392b", "N": "#1f5fa8", "S": "#a07800", "H": "#5c6b78", "C": INK, "R": LILA, "R'": LILA}


def save(nombre, contenido):
    with open(os.path.join(base.OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def estructura(atomos, enlaces, size=22):
    """Fórmula desarrollada: atomos = {id: (x, y, etiqueta)}, enlaces = [(a, b, orden)]."""
    s = ""
    for a, b, orden in enlaces:
        (x1, y1, _), (x2, y2, _) = atomos[a], atomos[b]
        n = math.hypot(x2 - x1, y2 - y1)
        ux, uy = (x2 - x1) / n, (y2 - y1) / n
        def hueco(et):
            ancho = max(1, len(et.replace('₂', '').replace('₃', ''))) * size * 0.38
            return max(size * 0.62, abs(ux) * ancho + abs(uy) * size * 0.62)
        ga, gb = hueco(atomos[a][2]), hueco(atomos[b][2])
        p, q = (x1 + ux * ga, y1 + uy * ga), (x2 - ux * gb, y2 - uy * gb)
        offs = (0,) if orden == 1 else (-4, 4)
        for o in offs:
            s += (f'<line x1="{p[0] - uy * o:.1f}" y1="{p[1] + ux * o:.1f}" x2="{q[0] - uy * o:.1f}" y2="{q[1] + ux * o:.1f}" '
                  f'stroke="{INK}" stroke-width="2.4" stroke-linecap="round"/>')
    for x, y, et in atomos.values():
        col = COL_AT.get(et, INK)
        s += text(x, y + size * 0.36, et, size, weight=800, fill=col)
    return s


# 1 · Tabla periódica con los bioelementos --------------------------------
def tabla_bioelementos():
    filas = [
        {1: "H", 18: "He"},
        dict(zip([1, 2, 13, 14, 15, 16, 17, 18], "Li Be B C N O F Ne".split())),
        dict(zip([1, 2, 13, 14, 15, 16, 17, 18], "Na Mg Al Si P S Cl Ar".split())),
        dict(zip(range(1, 19), "K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr".split())),
        dict(zip(range(1, 19), "Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe".split())),
    ]
    prim = set("H C N O P S".split())
    sec = set("Na K Ca Mg Cl".split())
    oli = set("Li B F Si V Cr Mn Fe Co Cu Zn Se Mo Sn I".split())
    c, g, x0, y0 = 48, 4, 22, 20
    b = ""
    for r, fila in enumerate(filas):
        for col, sim in fila.items():
            x, y = x0 + (col - 1) * (c + g), y0 + r * (c + g)
            if sim in prim:
                fill, tc = PRI, "#fff"
            elif sim in sec:
                fill, tc = TEAL, "#fff"
            elif sim in oli:
                fill, tc = ACC, "#fff"
            else:
                fill, tc = "#eef2f5", "#a3b1bd"
            b += f'<rect x="{x}" y="{y}" width="{c}" height="{c}" rx="7" fill="{fill}"/>'
            b += text(x + c / 2, y + c / 2 + 7, sim, 19, weight=800, fill=tc)
    ly = y0 + 5 * (c + g) + 24
    for i, (col, et) in enumerate(((PRI, "Primarios ≈ 96 %"), (TEAL, "Secundarios ≈ 3,9 %"),
                                   (ACC, "Oligoelementos < 0,1 %"), ("#eef2f5", "No esenciales"))):
        x = x0 + (0, 230, 470, 730)[i]
        b += f'<rect x="{x}" y="{ly - 15}" width="20" height="20" rx="5" fill="{col}" stroke="#cbd5de"/>'
        b += text(x + 28, ly, et, 16, "start", 700)
    save("tabla-bioelementos.svg", svg(980, ly + 20, b, "Tabla periódica con los bioelementos primarios, secundarios y oligoelementos"))


# 2 · Composición del cuerpo humano (anillo) ---------------------------------
def composicion():
    datos = [("O", 65, "#d64541"), ("C", 18.5, "#3d4a56"), ("H", 9.5, "#9fb3c4"), ("N", 3.3, BLUE),
             ("Ca", 1.5, TEAL), ("P", 1.0, ACC), ("Otros", 1.2, "#b48ad6")]
    cx, cy, R, r = 170, 170, 145, 82
    b, a0 = "", -math.pi / 2
    for et, v, col in datos:
        a1 = a0 + 2 * math.pi * v / 100
        big = 1 if a1 - a0 > math.pi else 0
        p1, p2 = (cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1))
        q1, q2 = (cx + r * math.cos(a1), cy + r * math.sin(a1)), (cx + r * math.cos(a0), cy + r * math.sin(a0))
        b += (f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A{R},{R} 0 {big} 1 {p2[0]:.1f},{p2[1]:.1f} L{q1[0]:.1f},{q1[1]:.1f} '
              f'A{r},{r} 0 {big} 0 {q2[0]:.1f},{q2[1]:.1f} z" fill="{col}" stroke="#fff" stroke-width="2"/>')
        a0 = a1
    b += text(cx, cy - 4, "Cuerpo", 20, weight=800)
    b += text(cx, cy + 20, "humano", 20, weight=800)
    for i, (et, v, col) in enumerate(datos):
        y = 40 + i * 40
        b += f'<rect x="360" y="{y - 18}" width="24" height="24" rx="6" fill="{col}"/>'
        b += text(396, y, et, 20, "start", 800)
        b += text(560, y, f"{v:g} %".replace(".", ","), 20, "end", 700, fill=GRIS)
    b += text(360, 330, "% en masa", 15, "start", 600, fill=GRIS)
    save("composicion-cuerpo.svg", svg(580, 345, b, "Composición del cuerpo humano en porcentaje de masa"))


# 3 · El carbono -------------------------------------------------------------
def carbono():
    b = ""
    c = (130, 150)
    for (x, y), dash in (((130, 50), ""), ((45, 205), ""), ((215, 205), ""), ((200, 95), 'stroke-dasharray="6 5"')):
        b += f'<line x1="{c[0]}" y1="{c[1]}" x2="{x}" y2="{y}" stroke="#55626e" stroke-width="6" stroke-linecap="round" {dash}/>'
        b += f'<circle cx="{x}" cy="{y}" r="18" fill="url(#gH)" stroke="#7b8a97" stroke-width="1.5"/>'
        b += text(x, y + 6, "H", 16, weight=800)
    b += f'<circle cx="{c[0]}" cy="{c[1]}" r="30" fill="#3d4a56"/>'
    b += text(c[0], c[1] + 8, "C", 24, fill="#fff", weight=800)
    b += text(130, 262, "Tetravalente: 4 enlaces", 16, weight=800)
    b += text(130, 282, "dirigidos a un tetraedro", 14, weight=600, fill=GRIS)

    def atomoC(x, y, r=15):
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#3d4a56"/>' + text(x, y + 5, "C", 14, fill="#fff", weight=800)

    # cadena
    pts = [(300 + i * 46, 80 if i % 2 == 0 else 52) for i in range(7)]
    pts.insert(4, None)
    pts = [p for p in pts if p]
    s = ""
    for a, bb in zip(pts, pts[1:]):
        s += f'<line x1="{a[0]}" y1="{a[1]}" x2="{bb[0]}" y2="{bb[1]}" stroke="#55626e" stroke-width="5"/>'
    rama = (pts[3][0], 120)
    s += f'<line x1="{pts[3][0]}" y1="{pts[3][1]}" x2="{rama[0]}" y2="{rama[1]}" stroke="#55626e" stroke-width="5"/>'
    for p in pts + [rama]:
        s += atomoC(*p)
    b += s + text(440, 160, "Cadenas lineales y ramificadas", 16, weight=800)
    # anillo
    ac = (380, 222)
    hexa = [(ac[0] + 36 * math.cos(math.radians(60 * k + 30)), ac[1] + 36 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    for a, bb in zip(hexa, hexa[1:] + hexa[:1]):
        b += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{bb[0]:.1f}" y2="{bb[1]:.1f}" stroke="#55626e" stroke-width="5"/>'
    for p in hexa:
        b += atomoC(p[0], p[1], 13)
    b += text(380, 302, "Anillos", 16, weight=800)
    # doble enlace
    for o in (-5, 5):
        b += f'<line x1="520" y1="{235 + o}" x2="600" y2="{235 + o}" stroke="#55626e" stroke-width="4"/>'
    b += atomoC(520, 235) + atomoC(600, 235)
    b += text(560, 302, "Enlaces dobles", 16, weight=800)
    save("carbono.svg", svg(680, 310, b, "El carbono es tetravalente y forma cadenas, anillos y enlaces dobles"))


# 4 · Reconocer biomoléculas -------------------------------------------------
def reconocer():
    b = ""
    for x in (250, 500, 750):
        b += f'<line x1="{x}" y1="30" x2="{x}" y2="300" stroke="#dde5ec" stroke-width="2"/>'
    # Glucosa (proyección de Haworth)
    v = {"O": (160, 105), "C1": (200, 145), "C2": (165, 185), "C3": (85, 185), "C4": (50, 145), "C5": (85, 105)}
    orden = ["O", "C1", "C2", "C3", "C4", "C5", "O"]
    for a, bb in zip(orden, orden[1:]):
        w = 7 if (a, bb) in (("C2", "C3"),) else 3.5
        b += f'<line x1="{v[a][0]}" y1="{v[a][1]}" x2="{v[bb][0]}" y2="{v[bb][1]}" stroke="{INK}" stroke-width="{w}" stroke-linecap="round"/>'
    b += f'<circle cx="160" cy="105" r="13" fill="#fff"/>' + text(160, 112, "O", 20, weight=800, fill=COL_AT["O"])
    for (x, y), up in ((v["C1"], False), (v["C2"], False), (v["C3"], True), (v["C4"], False)):
        y2 = y - 30 if up else y + 30
        b += f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y2 + (8 if up else -8)}" stroke="{INK}" stroke-width="2.4"/>'
        b += text(x, y2 + (0 if up else 10), "OH", 16, weight=800, fill=COL_AT["O"])
    b += f'<line x1="85" y1="105" x2="85" y2="72" stroke="{INK}" stroke-width="2.4"/>' + text(85, 64, "CH₂OH", 16, weight=800)
    b += text(125, 262, "Glúcido", 20, weight=900, fill=PRI)
    b += text(125, 284, "muchos –OH · anillo con O", 14, weight=600, fill=GRIS)
    # Ácido graso
    xs = [270 + i * 19 for i in range(10)]
    pts = " ".join(f"{x},{150 if i % 2 else 170}" for i, x in enumerate(xs))
    b += f'<polyline points="{pts}" fill="none" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
    b += text(xs[-1] + 8, 157, "–COOH", 20, "start", 900, fill=COL_AT["O"])
    b += f'<rect x="265" y="190" width="175" height="8" rx="4" fill="#f2c94c" opacity="0.55"/>'
    b += text(352, 222, "cola hidrocarbonada", 13, weight=700, fill="#8a6d00")
    b += text(375, 262, "Lípido", 20, weight=900, fill=TEAL)
    b += text(375, 284, "larga cola –CH₂– · –COOH", 14, weight=600, fill=GRIS)
    # Aminoácido
    b += estructura({"c": (625, 150, "C"), "h": (625, 92, "H"), "r": (625, 208, "R"), "n": (548, 150, "H₂N"), "co": (708, 150, "COOH")},
                    [("c", "h", 1), ("c", "r", 1), ("c", "n", 1), ("c", "co", 1)], 22)
    b += text(625, 262, "Aminoácido", 20, weight=900, fill=ACC)
    b += text(625, 284, "–NH₂ y –COOH en el mismo C", 14, weight=600, fill=GRIS)
    # Nucleótido
    b += '<line x1="795" y1="170" x2="840" y2="170" stroke="#55626e" stroke-width="4"/><line x1="890" y1="160" x2="925" y2="140" stroke="#55626e" stroke-width="4"/>'
    b += '<circle cx="790" cy="170" r="22" fill="#f2c94c" stroke="#a07800" stroke-width="2"/>' + text(790, 177, "P", 20, weight=900, fill="#6b5000")
    pent = [(865 + 30 * math.cos(math.radians(-90 + 72 * k)), 172 + 30 * math.sin(math.radians(-90 + 72 * k))) for k in range(5)]
    b += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pent)}" fill="#f6c3b5" stroke="#b5533c" stroke-width="2.5"/>'
    hexa = [(950 + 28 * math.cos(math.radians(60 * k + 30)), 128 + 28 * math.sin(math.radians(60 * k + 30))) for k in range(6)]
    b += f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in hexa)}" fill="#cfe2f7" stroke="#1f5fa8" stroke-width="2.5"/>'
    b += text(790, 215, "fosfato", 13, weight=700, fill=GRIS) + text(865, 222, "pentosa", 13, weight=700, fill=GRIS) + text(950, 86, "base", 13, weight=700, fill=GRIS)
    b += text(875, 262, "Nucleótido", 20, weight=900, fill=LILA)
    b += text(875, 284, "fosfato + pentosa + base", 14, weight=600, fill=GRIS)
    save("biomoleculas-reconocer.svg", svg(1000, 300, b, "Cómo reconocer un glúcido, un lípido, un aminoácido y un nucleótido"))


# 5 · Tipos de enlace ------------------------------------------------------------
def lipido(x, y, ang, L=34, cab=9):
    u = d(ang)
    t = P((x, y), u, L)
    s = ""
    for o in (-3, 3):
        s += (f'<line x1="{x - u[1] * o:.1f}" y1="{y + u[0] * o:.1f}" x2="{t[0] - u[1] * o:.1f}" y2="{t[1] + u[0] * o:.1f}" '
              'stroke="#b8862d" stroke-width="2.2" stroke-linecap="round"/>')
    s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{cab}" fill="{BLUE}" stroke="#145a8c" stroke-width="1.5"/>'
    return s


def enlaces():
    b = ""
    for x in (250, 500, 750):
        b += f'<line x1="{x}" y1="20" x2="{x}" y2="270" stroke="#dde5ec" stroke-width="2"/>'
    # covalente
    b += '<circle cx="100" cy="130" r="42" fill="url(#gO)" stroke="#9e2a26" stroke-width="2" opacity="0.92"/>'
    b += '<circle cx="158" cy="130" r="28" fill="url(#gH)" stroke="#7b8a97" stroke-width="2" opacity="0.92"/>'
    b += text(88, 138, "O", 24, fill="#fff", weight=800) + text(168, 137, "H", 20, weight=800)
    b += '<circle cx="132" cy="121" r="5" fill="#f2c94c" stroke="#6b5000"/><circle cx="132" cy="139" r="5" fill="#f2c94c" stroke="#6b5000"/>'
    b += text(125, 225, "Covalente", 20, weight=900, fill=PRI) + text(125, 247, "comparten electrones", 14, weight=600, fill=GRIS)
    # iónico
    b += f'<circle cx="330" cy="130" r="26" fill="#8e5bb5"/>' + text(330, 137, "Na⁺", 17, fill="#fff", weight=800)
    b += f'<circle cx="430" cy="130" r="34" fill="#2f9e63"/>' + text(430, 137, "Cl⁻", 18, fill="#fff", weight=800)
    b += f'<line x1="360" y1="130" x2="393" y2="130" stroke="{INK}" stroke-width="2.5" marker-start="url(#fk)" marker-end="url(#fk)"/>'
    b += text(375, 225, "Iónico", 20, weight=900, fill=PRI) + text(375, 247, "atracción entre iones", 14, weight=600, fill=GRIS)
    # puente de hidrógeno
    m1, h1, _ = molecule((548, 125), 0, L=36, ro=24, rh=14, labels=True)
    o2 = (h1[0] + 56, h1[1])
    m2, _, _ = molecule(o2, -52.25, L=36, ro=24, rh=14, labels=True)
    b += hbond(h1, o2, 14, 24) + m1 + m2
    b += text(625, 225, "Puente de hidrógeno", 20, weight=900, fill=BLUE) + text(625, 247, "entre H (δ⁺) y O o N (δ⁻)", 14, weight=600, fill=GRIS)
    # hidrofóbica
    b += '<rect x="772" y="40" width="210" height="160" rx="12" fill="#d6ecfa"/>'
    for k in range(10):
        ang = k * 36
        cpt = P((877, 120), d(ang), 52)
        b += lipido(cpt[0], cpt[1], ang + 180, L=36, cab=9)
    b += text(875, 225, "Hidrofóbica", 20, weight=900, fill=TEAL) + text(875, 247, "lo apolar se agrupa", 14, weight=600, fill=GRIS)
    save("enlaces-tipos.svg", svg(1000, 265, b, "Enlace covalente, iónico, puente de hidrógeno e interacción hidrofóbica"))


# 6 · Grupos funcionales --------------------------------------------------------------
def grupos():
    W, H, G = 240, 200, 12
    tiles = [
        ("Hidroxilo", "–OH", "glúcidos, glicerina", {"r": (55, 105, "R"), "o": (120, 105, "O"), "h": (180, 105, "H")}, [("r", "o", 1), ("o", "h", 1)]),
        ("Carbonilo · aldehído", "–CHO", "aldosas", {"r": (50, 125, "R"), "c": (120, 125, "C"), "o": (120, 60, "O"), "h": (185, 125, "H")}, [("r", "c", 1), ("c", "o", 2), ("c", "h", 1)]),
        ("Carbonilo · cetona", ">C=O", "cetosas", {"r": (50, 125, "R"), "c": (120, 125, "C"), "o": (120, 60, "O"), "r2": (190, 125, "R'")}, [("r", "c", 1), ("c", "o", 2), ("c", "r2", 1)]),
        ("Carboxilo", "–COOH", "ácidos grasos, aminoácidos", {"r": (40, 125, "R"), "c": (100, 125, "C"), "o": (100, 60, "O"), "o2": (160, 125, "O"), "h": (210, 125, "H")}, [("r", "c", 1), ("c", "o", 2), ("c", "o2", 1), ("o2", "h", 1)]),
        ("Amino", "–NH₂", "aminoácidos, bases", {"r": (55, 105, "R"), "n": (120, 105, "N"), "h1": (175, 75, "H"), "h2": (175, 140, "H")}, [("r", "n", 1), ("n", "h1", 1), ("n", "h2", 1)]),
        ("Tiol (sulfhidrilo)", "–SH", "cisteína → puentes S–S", {"r": (55, 105, "R"), "s": (120, 105, "S"), "h": (180, 105, "H")}, [("r", "s", 1), ("s", "h", 1)]),
        ("Amida", "–CO–NH–", "enlace peptídico", {"r": (35, 112, "R"), "c": (90, 112, "C"), "o": (90, 55, "O"), "n": (150, 112, "N"), "h": (150, 158, "H"), "r2": (208, 112, "R'")}, [("r", "c", 1), ("c", "o", 2), ("c", "n", 1), ("n", "h", 1), ("n", "r2", 1)]),
    ]
    b = ""
    for i, (nom, form, donde, at, en) in enumerate(tiles):
        x, y = (i % 4) * (W + G), (i // 4) * (H + G)
        b += f'<g transform="translate({x},{y})"><rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="#f6f9fb" stroke="#dde5ec" stroke-width="2"/>'
        b += text(14, 28, nom, 16, "start", 900, fill=PRI) + text(W - 14, 28, form, 16, "end", 800, fill=ACC)
        b += estructura(at, en, 22)
        b += text(W / 2, H - 12, donde, 13, weight=700, fill=GRIS) + "</g>"
    x, y = 3 * (W + G), H + G
    b += f'<g transform="translate({x},{y})"><rect x="0" y="0" width="{W}" height="{H}" rx="14" fill="#fff" stroke="#dde5ec" stroke-width="2" stroke-dasharray="6 5"/>'
    b += text(W / 2, 40, "R = resto de la molécula", 15, weight=800, fill=LILA)
    for k, (et, nom) in enumerate((("O", "oxígeno"), ("N", "nitrógeno"), ("S", "azufre"), ("C", "carbono"))):
        b += text(70, 80 + k * 28, et, 20, weight=900, fill=COL_AT[et]) + text(92, 80 + k * 28, nom, 15, "start", 700, fill=GRIS)
    b += "</g>"
    save("grupos-funcionales.svg", svg(4 * W + 3 * G, 2 * H + G, b, "Fórmulas de los grupos funcionales hidroxilo, carbonilo, carboxilo, amino, tiol y amida"))


# 7 · Lípidos anfipáticos en agua -----------------------------------------------------
def micela():
    b = '<rect x="250" y="20" width="510" height="260" rx="16" fill="#d6ecfa"/>'
    # molécula aislada
    b += lipido(110, 70, 90, L=120, cab=24)
    b += text(150, 76, "Cabeza polar", 16, "start", 800, fill=BLUE) + text(150, 94, "(hidrófila)", 14, "start", 600, fill=GRIS)
    b += text(130, 160, "Cola apolar", 16, "start", 800, fill="#8a6d00") + text(130, 178, "(hidrófoba)", 14, "start", 600, fill=GRIS)
    b += text(110, 260, "Molécula anfipática", 17, weight=900)
    # micela
    for k in range(16):
        ang = k * 22.5
        cpt = P((385, 140), d(ang), 70)
        b += lipido(cpt[0], cpt[1], ang + 180, L=50, cab=11)
    b += text(385, 262, "Micela", 18, weight=900, fill=PRI)
    # bicapa
    for i in range(8):
        x = 515 + i * 28
        b += lipido(x, 70, 90, L=58, cab=11) + lipido(x, 210, 270, L=58, cab=11)
    b += text(613, 262, "Bicapa (membranas)", 18, weight=900, fill=PRI)
    b += text(505, 45, "agua", 14, weight=700, fill="#2a6f9e")
    save("lipidos-micela-bicapa.svg", svg(770, 290, b, "Molécula anfipática con cabeza polar y cola apolar; en agua forma micelas y bicapas"))


# 8 · Aminoácido anfótero ---------------------------------------------------------------
def anfotero():
    b = ""
    estados = (("Medio ácido", "H₃N⁺", "COOH", "carga +"), ("pH neutro", "H₃N⁺", "COO⁻", "ion dipolar"), ("Medio básico", "H₂N", "COO⁻", "carga −"))
    for i, (t, am, ca, nota) in enumerate(estados):
        x = 140 + i * 300
        b += f'<rect x="{x - 125}" y="40" width="250" height="160" rx="14" fill="#f6f9fb" stroke="#dde5ec" stroke-width="2"/>'
        b += text(x, 30, t, 17, weight=900, fill=PRI)
        b += estructura({"c": (x, 120, "C"), "h": (x, 72, "H"), "r": (x, 168, "R"), "n": (x - 68, 120, am), "co": (x + 70, 120, ca)},
                        [("c", "h", 1), ("c", "r", 1), ("c", "n", 1), ("c", "co", 1)], 20)
        b += text(x, 225, nota, 15, weight=700, fill=GRIS)
    for i, (et, sub) in enumerate((("−H⁺", "cede H⁺: ácido"), ("−H⁺", "cede H⁺: ácido"))):
        x = 290 + i * 300
        b += f'<line x1="{x - 22}" y1="120" x2="{x + 22}" y2="120" stroke="{ACC}" stroke-width="3" marker-end="url(#fk)"/>'
        b += text(x, 108, et, 15, weight=900, fill=ACC)
    b += text(440, 258, "El –COOH puede ceder H⁺ (ácido) y el –NH₂ puede captarlo (base): carácter anfótero.", 15, weight=700)
    save("aminoacido-anfotero.svg", svg(880, 270, b, "Un aminoácido en medio ácido, neutro y básico: carácter anfótero"))


# 9 · Abundancia de agua ---------------------------------------------------------------
def abundancia():
    cols = [("Medusa", 98, "98 %"), ("Embrión", 90, "> 90 %"), ("Cerebro", 85, "≈ 85 %"), ("Adulto", 63, "≈ 63 %"),
            ("Hueso", 22, "≈ 22 %"), ("Semilla", 15, "10-20 %"), ("Esmalte", 3, "< 5 %")]
    b = ""

    def icono(i, cx):
        if i == 0:
            s = f'<path d="M{cx - 42},78 Q{cx},-2 {cx + 42},78 Q{cx},66 {cx - 42},78z" fill="#c7b3ef" stroke="#7d5fc0" stroke-width="2"/>'
            for k in range(5):
                x = cx - 30 + k * 15
                s += f'<path d="M{x},78 q-6,12 0,22 q6,10 0,22" fill="none" stroke="#7d5fc0" stroke-width="2"/>'
            return s
        if i == 1:
            return (f'<ellipse cx="{cx + 8}" cy="88" rx="26" ry="20" fill="#f4c2ad" stroke="#b5735a" stroke-width="2"/>'
                    f'<circle cx="{cx - 10}" cy="58" r="24" fill="#f4c2ad" stroke="#b5735a" stroke-width="2"/><circle cx="{cx - 16}" cy="54" r="3" fill="#7a4a3a"/>')
        if i == 2:
            s = f'<ellipse cx="{cx}" cy="70" rx="46" ry="34" fill="#f5b3c3" stroke="#c0607a" stroke-width="2"/>'
            for dx, dy in ((-24, -12), (0, -18), (22, -8), (-18, 12), (12, 14)):
                s += f'<path d="M{cx + dx - 12},{70 + dy} q6,-8 12,0 q6,8 12,0" fill="none" stroke="#c0607a" stroke-width="2"/>'
            return s + f'<line x1="{cx}" y1="38" x2="{cx}" y2="102" stroke="#c0607a" stroke-width="1.5"/>'
        if i == 3:
            return (f'<circle cx="{cx}" cy="34" r="16" fill="#8fb0d6" stroke="#4f78a8" stroke-width="2"/>'
                    f'<rect x="{cx - 24}" y="54" width="48" height="58" rx="18" fill="#8fb0d6" stroke="#4f78a8" stroke-width="2"/>')
        if i == 4:
            s = ""
            for x in (cx - 36, cx + 36):
                for y in (62, 82):
                    s += f'<circle cx="{x}" cy="{y}" r="12" fill="#f3efe4" stroke="#a89f86" stroke-width="2"/>'
            return s + f'<rect x="{cx - 38}" y="62" width="76" height="20" fill="#f3efe4"/><line x1="{cx - 38}" y1="62" x2="{cx + 38}" y2="62" stroke="#a89f86" stroke-width="2"/><line x1="{cx - 38}" y1="82" x2="{cx + 38}" y2="82" stroke="#a89f86" stroke-width="2"/>'
        if i == 5:
            return (f'<ellipse cx="{cx}" cy="72" rx="38" ry="25" fill="#c99b5f" stroke="#8a6232" stroke-width="2"/>'
                    f'<path d="M{cx - 20},64 q20,14 40,0" fill="none" stroke="#8a6232" stroke-width="2"/>')
        return (f'<path d="M{cx - 30},44 Q{cx - 32},20 {cx - 12},26 Q{cx},32 {cx + 12},26 Q{cx + 32},20 {cx + 30},44 '
                f'L{cx + 22},104 Q{cx + 16},116 {cx + 10},100 L{cx + 4},74 L{cx - 4},74 L{cx - 10},100 Q{cx - 16},116 {cx - 22},104 Z" '
                'fill="#ffffff" stroke="#8a99a6" stroke-width="2.5"/>')

    for i, (nom, pct, et) in enumerate(cols):
        cx = 75 + i * 140
        b += icono(i, cx)
        b += text(cx, 142, nom, 17, weight=900)
        top, alto = 160, 120
        h = alto * pct / 100
        b += f'<rect x="{cx - 34}" y="{top + alto - h:.1f}" width="68" height="{h:.1f}" fill="#5dade2"/>'
        b += f'<path d="M{cx - 36},{top} V{top + alto} H{cx + 36} V{top}" fill="none" stroke="#7b8a97" stroke-width="3"/>'
        ty = min(top + alto - h - 8, top + alto - 8) if pct > 25 else top + alto - h - 8
        b += text(cx, ty if pct <= 25 else top + alto - h + 24, et, 16, weight=900, fill=INK if pct <= 25 else "#fff")
    save("agua-abundancia.svg", svg(980, 290, b, "Porcentaje de agua en distintos organismos, tejidos y edades"))


# 10 · Hoja frente a roca --------------------------------------------------------------
def termometro(x, y, frac, col, et):
    s = f'<rect x="{x - 8}" y="{y}" width="16" height="90" rx="8" fill="#fff" stroke="#7b8a97" stroke-width="2"/>'
    s += f'<rect x="{x - 4}" y="{y + 90 - 84 * frac:.1f}" width="8" height="{84 * frac:.1f}" fill="{col}"/>'
    s += f'<circle cx="{x}" cy="{y + 98}" r="13" fill="{col}" stroke="#7b8a97" stroke-width="2"/>'
    return s + text(x + 22, y + 30, et, 22, "start", 900, fill=col)


def hoja_roca():
    b = '<rect x="0" y="0" width="700" height="250" fill="#f3f8fc"/><rect x="0" y="250" width="700" height="60" fill="#d9c7a7"/>'
    b += '<circle cx="70" cy="60" r="34" fill="#f7c948"/>'
    for k in range(10):
        a = d(k * 36)
        p1, p2 = P((70, 60), a, 44), P((70, 60), a, 58)
        b += f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#f7c948" stroke-width="4" stroke-linecap="round"/>'
    # planta
    b += '<path d="M230,250 Q232,200 228,150" fill="none" stroke="#3f8a3a" stroke-width="6"/>'
    b += '<path d="M228,160 C170,150 150,100 170,70 C220,80 240,120 228,160z" fill="#6cc070" stroke="#2c6e2a" stroke-width="2.5"/>'
    b += '<path d="M230,190 C290,190 320,150 305,115 C255,120 232,160 230,190z" fill="#6cc070" stroke="#2c6e2a" stroke-width="2.5"/>'
    for x, y in ((180, 70), (205, 60), (300, 105)):
        b += f'<path d="M{x},{y} q-8,-12 0,-24 q8,-12 0,-24" fill="none" stroke="{BLUE}" stroke-width="2.5" marker-end="url(#fl)"/>'
    b += text(330, 40, "H₂O (vapor)", 16, "start", 800, fill=BLUE)
    b += termometro(330, 120, 0.4, BLUE, "25 °C")
    # roca
    b += '<path d="M470,250 L500,190 L560,165 L620,180 L660,250z" fill="#9aa3a8" stroke="#6b7479" stroke-width="2.5"/>'
    b += termometro(560, 40, 0.85, "#c0392b", "45 °C")
    b += text(350, 290, "Al transpirar, el agua absorbe mucho calor al evaporarse y refrigera la hoja.", 16, weight=700)
    save("hoja-roca-vaporizacion.svg", svg(700, 310, b, "Una hoja al sol está más fresca que una roca gracias a la evaporación del agua"))


# 11 · Escala de pH --------------------------------------------------------------------
def escala_ph():
    x0, x1, y = 40, 960, 110
    b = ('<defs><linearGradient id="gph" x1="0" x2="1"><stop offset="0" stop-color="#d73027"/><stop offset="0.3" stop-color="#fdae61"/>'
         '<stop offset="0.5" stop-color="#a6d96a"/><stop offset="0.7" stop-color="#4ba3d6"/><stop offset="1" stop-color="#5e3c99"/></linearGradient></defs>')
    b += f'<rect x="{x0}" y="{y}" width="{x1 - x0}" height="36" rx="18" fill="url(#gph)"/>'
    for v in range(15):
        x = x0 + (x1 - x0) * v / 14
        b += f'<line x1="{x:.1f}" y1="{y + 36}" x2="{x:.1f}" y2="{y + 46}" stroke="{INK}" stroke-width="2"/>' + text(x, y + 66, str(v), 16, weight=800)
    marcas = [(2, "Jugo gástrico", 62, "middle"), (3, "Vinagre", 30, "middle"), (5, "Café", 62, "middle"),
              (7, "Agua pura", 30, "end"), (7.4, "Sangre", 62, "start"), (8.2, "Agua de mar", 30, "start"), (13, "Lejía", 62, "middle")]
    for v, et, yt, anc in marcas:
        x = x0 + (x1 - x0) * v / 14
        b += f'<line x1="{x:.1f}" y1="{yt + 8}" x2="{x:.1f}" y2="{y - 2}" stroke="{INK}" stroke-width="1.5"/>'
        tx = x + (8 if anc == "end" else -8 if anc == "start" else 0)
        b += text(tx, yt, f"{et} ({str(v).replace('.', ',')})", 16, anc, 800)
    b += text(x0, y + 100, "← ácido (más H⁺)", 16, "start", 900, fill="#c0392b")
    b += text((x0 + x1) / 2, y + 100, "neutro", 16, weight=900, fill="#3f8a3a")
    b += text(x1, y + 100, "básico (menos H⁺) →", 16, "end", 900, fill="#5e3c99")
    save("escala-ph.svg", svg(1000, 225, b, "Escala de pH con ejemplos: jugo gástrico, vinagre, café, agua pura, sangre, agua de mar y lejía"))


# 12 · Sales precipitadas ----------------------------------------------------------------
def sales_estructurales():
    b = ""
    # hueso
    cx = 120
    for x in (cx - 60, cx + 60):
        for y in (80, 112):
            b += f'<circle cx="{x}" cy="{y}" r="20" fill="#f3efe4" stroke="#a89f86" stroke-width="2.5"/>'
    b += f'<rect x="{cx - 62}" y="80" width="124" height="32" fill="#f3efe4"/>'
    b += f'<line x1="{cx - 62}" y1="80" x2="{cx + 62}" y2="80" stroke="#a89f86" stroke-width="2.5"/><line x1="{cx - 62}" y1="112" x2="{cx + 62}" y2="112" stroke="#a89f86" stroke-width="2.5"/>'
    b += text(cx, 200, "Huesos y dientes", 18, weight=900) + text(cx, 224, "fosfato de calcio · Ca₃(PO₄)₂", 15, weight=700, fill=GRIS)
    # concha
    cx, cy = 370, 96
    pts = []
    for i in range(220):
        t = i / 220 * 5.2 * math.pi
        r = 4 + 4.6 * t
        pts.append(f"{cx + r * math.cos(t):.1f},{cy + r * math.sin(t):.1f}")
    b += f'<circle cx="{cx}" cy="{cy}" r="78" fill="#f0d9b5" stroke="#a0784a" stroke-width="2.5"/>'
    b += f'<polyline points="{" ".join(pts)}" fill="none" stroke="#a0784a" stroke-width="3"/>'
    b += text(cx, 200, "Conchas y caparazones", 18, weight=900) + text(cx, 224, "carbonato de calcio · CaCO₃", 15, weight=700, fill=GRIS)
    # diatomea
    cx, cy = 630, 96
    b += f'<circle cx="{cx}" cy="{cy}" r="76" fill="#e6f2df" stroke="#5a8f3c" stroke-width="3"/>'
    for r in (24, 48):
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#5a8f3c" stroke-width="1.5"/>'
    for k in range(24):
        p1, p2 = P((cx, cy), d(k * 15), 24), P((cx, cy), d(k * 15), 74)
        b += f'<line x1="{p1[0]:.1f}" y1="{p1[1]:.1f}" x2="{p2[0]:.1f}" y2="{p2[1]:.1f}" stroke="#5a8f3c" stroke-width="1.5"/>'
    b += text(cx, 200, "Caparazón de diatomeas", 18, weight=900) + text(cx, 224, "sílice · SiO₂", 15, weight=700, fill=GRIS)
    # otolito/cáscara de huevo
    cx = 870
    b += f'<ellipse cx="{cx}" cy="98" rx="56" ry="72" fill="#fbf6ec" stroke="#b9a98a" stroke-width="2.5"/>'
    for x, y in ((-20, -30), (15, -10), (-5, 25), (25, 30), (-30, 10)):
        b += f'<circle cx="{cx + x}" cy="{98 + y}" r="2.5" fill="#d2c5ab"/>'
    b += text(cx, 200, "Cáscara de huevo", 18, weight=900) + text(cx, 224, "carbonato de calcio", 15, weight=700, fill=GRIS)
    save("sales-estructurales.svg", svg(1000, 240, b, "Sales minerales precipitadas con función estructural: huesos, conchas, diatomeas y cáscara de huevo"))


# 13 · Bomba de sodio y potasio --------------------------------------------------------------
def bomba():
    b = '<rect x="0" y="0" width="700" height="170" fill="#eaf4fb"/><rect x="0" y="230" width="700" height="170" fill="#fdf3e4"/>'
    for x in range(10, 700, 22):
        if 290 < x < 410:
            continue
        b += f'<circle cx="{x}" cy="180" r="8" fill="{BLUE}"/><circle cx="{x}" cy="220" r="8" fill="{BLUE}"/>'
        b += f'<line x1="{x - 2}" y1="188" x2="{x - 2}" y2="212" stroke="#b8862d" stroke-width="2"/><line x1="{x + 2}" y1="188" x2="{x + 2}" y2="212" stroke="#b8862d" stroke-width="2"/>'
    b += '<rect x="300" y="150" width="100" height="100" rx="26" fill="#9b7fd1" stroke="#6d3fc0" stroke-width="3"/>'
    b += text(350, 196, "Bomba", 16, fill="#fff", weight=900) + text(350, 216, "Na⁺/K⁺", 16, fill="#fff", weight=900)
    b += text(20, 30, "Medio extracelular", 17, "start", 900, fill="#2a6f9e")
    b += text(20, 390, "Citoplasma", 17, "start", 900, fill="#8a5600")

    def ion(x, y, et, col):
        return f'<circle cx="{x}" cy="{y}" r="17" fill="{col}"/>' + text(x, y + 5, et, 13, fill="#fff", weight=800)
    NA, K = "#8e5bb5", ACC
    for x, y in ((60, 80), (130, 125), (200, 60), (480, 90), (560, 50), (630, 125), (520, 140)):
        b += ion(x, y, "Na⁺", NA)
    for x, y in ((440, 40), (250, 140)):
        b += ion(x, y, "K⁺", K)
    for x, y in ((60, 290), (140, 340), (220, 280), (560, 350), (630, 280), (200, 360), (520, 270)):
        b += ion(x, y, "K⁺", K)
    for x, y in ((470, 360), (90, 340)):
        b += ion(x, y, "Na⁺", NA)
    b += f'<line x1="282" y1="280" x2="282" y2="115" stroke="{NA}" stroke-width="4" marker-end="url(#fk)"/>' + text(272, 100, "3 Na⁺ salen", 16, "end", 900, fill=NA)
    b += f'<line x1="418" y1="115" x2="418" y2="280" stroke="{K}" stroke-width="4" marker-end="url(#fk)"/>' + text(428, 300, "2 K⁺ entran", 16, "start", 900, fill="#8a5600")
    b += text(350, 280, "ATP → ADP + P", 14, weight=800, fill=LILA)
    save("bomba-sodio-potasio.svg", svg(700, 400, b, "Bomba de sodio y potasio: el Na+ predomina fuera de la célula y el K+ dentro"))


# 14 · Ósmosis en la cocina ---------------------------------------------------------------
def cocina():
    b = ""
    for x in (333, 666):
        b += f'<line x1="{x}" y1="20" x2="{x}" y2="300" stroke="#dde5ec" stroke-width="2"/>'
    # salazón (pescado con sal)
    b += '<path d="M60,140 Q150,70 240,140 Q150,210 60,140z" fill="#c9d6de" stroke="#6f8796" stroke-width="2.5"/>'
    b += '<path d="M240,140 L290,105 L290,175z" fill="#c9d6de" stroke="#6f8796" stroke-width="2.5"/><circle cx="95" cy="132" r="5" fill="#2c3e50"/>'
    for x, y in ((70, 80), (120, 60), (180, 66), (230, 92), (90, 205), (150, 222), (215, 200), (40, 170)):
        b += f'<rect x="{x}" y="{y}" width="14" height="14" fill="#fff" stroke="#9aa8b4" stroke-width="1.5" transform="rotate(20 {x + 7} {y + 7})"/>'
    for x, y in ((150, 120), (190, 150)):
        b += f'<path d="M{x},{y} l-16,-20" stroke="{BLUE}" stroke-width="3" marker-end="url(#fl)"/>'
        b += f'<path d="M{x - 22},{y - 34} q-5,8 0,12 q5,-4 0,-12z" fill="{BLUE}"/>'
    b += text(166, 262, "Salazón", 20, weight=900, fill=PRI) + text(166, 284, "medio hipertónico: sale agua", 14, weight=700, fill=GRIS)
    # almíbar
    b += '<rect x="420" y="70" width="160" height="170" rx="20" fill="#f6d28a" stroke="#b07d1f" stroke-width="3"/><rect x="430" y="50" width="140" height="26" rx="6" fill="#c0392b"/>'
    for x, y in ((470, 130), (530, 160), (480, 200), (540, 110)):
        b += f'<circle cx="{x}" cy="{y}" r="22" fill="#f39c4a" stroke="#c46a1b" stroke-width="2"/>'
    b += '<g transform="translate(600,90)"><ellipse cx="0" cy="0" rx="18" ry="10" fill="#7dbb6a" stroke="#3f7a32" stroke-width="2"/>'
    b += '<line x1="-22" y1="-14" x2="22" y2="14" stroke="#c0392b" stroke-width="4"/><line x1="-22" y1="14" x2="22" y2="-14" stroke="#c0392b" stroke-width="4"/></g>'
    b += text(500, 262, "Almíbar", 20, weight=900, fill=PRI) + text(500, 284, "los microorganismos se deshidratan", 14, weight=700, fill=GRIS)
    # lechuga
    b += '<path d="M760,220 C700,160 720,70 770,50 C820,70 840,160 780,220z" fill="#7ccf68" stroke="#3a8a2c" stroke-width="2.5"/><path d="M770,215 Q770,130 770,58" stroke="#3a8a2c" stroke-width="2" fill="none"/>'
    b += '<path d="M880,220 C860,190 905,170 915,150 C925,130 965,140 950,170 C940,195 905,215 892,222z" fill="#c4c96a" stroke="#7d8a2c" stroke-width="2.5"/>'
    for x, y in ((875, 130), (935, 110), (965, 190)):
        b += f'<rect x="{x}" y="{y}" width="11" height="11" fill="#fff" stroke="#9aa8b4" transform="rotate(20 {x} {y})"/>'
    b += text(770, 245, "en agua", 14, weight=800, fill="#3a8a2c") + text(912, 245, "con sal", 14, weight=800, fill="#7d8a2c")
    b += text(835, 272, "Lechuga", 20, weight=900, fill=PRI) + text(835, 294, "turgente / se arruga", 14, weight=700, fill=GRIS)
    save("osmosis-cocina.svg", svg(1000, 300, b, "Ósmosis en la cocina: salazón, almíbar y lechuga aliñada"))


# 15 · Tampón bicarbonato ---------------------------------------------------------------
def tampon():
    b = ""

    def chip(x, y, et, col="#e7f0f8", tc=PRI, w=None):
        w = w or 24 + 13 * len(et)
        return (f'<rect x="{x - w / 2}" y="{y - 26}" width="{w}" height="44" rx="12" fill="{col}"/>' + text(x, y + 4, et, 20, weight=900, fill=tc))

    def flecha(x1, x2, y):
        return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'

    b += text(20, 30, "Si sobra ácido (H⁺):", 18, "start", 900, fill="#c0392b")
    y = 85
    b += chip(80, y, "H⁺", "#fbeae8", "#c0392b") + text(140, y + 6, "+", 26, weight=900) + chip(220, y, "HCO₃⁻")
    b += flecha(285, 340, y) + chip(410, y, "H₂CO₃") + flecha(475, 530, y) + chip(625, y, "CO₂ + H₂O", w=160)
    b += flecha(710, 770, y)
    # pulmones
    b += '<path d="M840,50 V75" stroke="#c0607a" stroke-width="6"/><path d="M840,75 L815,90 M840,75 L865,90" stroke="#c0607a" stroke-width="5"/>'
    b += '<path d="M812,80 C780,85 775,140 800,145 C820,148 828,120 826,95z" fill="#f5b3c3" stroke="#c0607a" stroke-width="2.5"/>'
    b += '<path d="M868,80 C900,85 905,140 880,145 C860,148 852,120 854,95z" fill="#f5b3c3" stroke="#c0607a" stroke-width="2.5"/>'
    b += text(900, 170, "el CO₂ se expulsa al respirar", 14, "end", 800, fill=GRIS)
    b += text(20, 215, "Si falta ácido (medio básico):", 18, "start", 900, fill="#5e3c99")
    y = 265
    b += chip(130, y, "H₂CO₃") + flecha(195, 250, y) + chip(320, y, "HCO₃⁻") + text(385, y + 6, "+", 26, weight=900) + chip(440, y, "H⁺", "#fbeae8", "#c0392b")
    b += text(500, y + 6, "→ se liberan H⁺ y el pH vuelve a bajar", 17, "start", 800, fill=GRIS)
    save("tampon-bicarbonato.svg", svg(940, 300, b, "Funcionamiento del tampón bicarbonato cuando sobra o falta ácido"))


# 16 · Carencias y salud ---------------------------------------------------------------
def salud():
    b = ""
    items = [("Agua", "deshidratación"), ("Hierro", "anemia"), ("Yodo", "bocio"), ("Calcio", "osteoporosis"), ("Flúor", "caries"), ("Na, K, Mg", "calambres, arritmias")]
    for i, (et, enf) in enumerate(items):
        cx, cy = 85 + i * 162, 80
        if i == 0:
            b += f'<path d="M{cx},{cy - 50} C{cx + 10},{cy - 20} {cx + 38},{cy + 5} {cx + 38},{cy + 22} A38,38 0 0 1 {cx - 38},{cy + 22} C{cx - 38},{cy + 5} {cx - 10},{cy - 20} {cx},{cy - 50}z" fill="#5dade2" stroke="#2a7fc1" stroke-width="2.5"/>'
        elif i == 1:
            b += f'<ellipse cx="{cx}" cy="{cy}" rx="46" ry="38" fill="#d9534f" stroke="#a33a36" stroke-width="2.5"/><ellipse cx="{cx}" cy="{cy}" rx="20" ry="15" fill="#ec8e8a"/>'
        elif i == 2:
            b += (f'<path d="M{cx - 6},{cy - 8} C{cx - 30},{cy - 50} {cx - 52},{cy - 20} {cx - 46},{cy + 20} C{cx - 40},{cy + 48} {cx - 12},{cy + 30} {cx - 6},{cy + 10}z" fill="#f2a7a0" stroke="#b5533c" stroke-width="2.5"/>'
                  f'<path d="M{cx + 6},{cy - 8} C{cx + 30},{cy - 50} {cx + 52},{cy - 20} {cx + 46},{cy + 20} C{cx + 40},{cy + 48} {cx + 12},{cy + 30} {cx + 6},{cy + 10}z" fill="#f2a7a0" stroke="#b5533c" stroke-width="2.5"/>'
                  f'<rect x="{cx - 9}" y="{cy - 4}" width="18" height="14" fill="#f2a7a0" stroke="#b5533c" stroke-width="2"/>')
        elif i == 3:
            for x in (cx - 40, cx + 40):
                for y in (cy - 10, cy + 10):
                    b += f'<circle cx="{x}" cy="{y}" r="13" fill="#f3efe4" stroke="#a89f86" stroke-width="2.5"/>'
            b += f'<rect x="{cx - 42}" y="{cy - 10}" width="84" height="20" fill="#f3efe4"/><line x1="{cx - 42}" y1="{cy - 10}" x2="{cx + 42}" y2="{cy - 10}" stroke="#a89f86" stroke-width="2.5"/><line x1="{cx - 42}" y1="{cy + 10}" x2="{cx + 42}" y2="{cy + 10}" stroke="#a89f86" stroke-width="2.5"/>'
        elif i == 4:
            b += (f'<path d="M{cx - 30},{cy - 26} Q{cx - 32},{cy - 50} {cx - 12},{cy - 44} Q{cx},{cy - 38} {cx + 12},{cy - 44} Q{cx + 32},{cy - 50} {cx + 30},{cy - 26} '
                  f'L{cx + 22},{cy + 34} Q{cx + 16},{cy + 46} {cx + 10},{cy + 30} L{cx + 4},{cy + 4} L{cx - 4},{cy + 4} L{cx - 10},{cy + 30} Q{cx - 16},{cy + 46} {cx - 22},{cy + 34} Z" '
                  'fill="#fff" stroke="#8a99a6" stroke-width="2.5"/>'
                  f'<circle cx="{cx + 8}" cy="{cy - 24}" r="7" fill="#6b4f2a"/>')
        else:
            b += f'<path d="M{cx + 8},{cy - 50} L{cx - 26},{cy + 6} H{cx - 2} L{cx - 10},{cy + 50} L{cx + 28},{cy - 8} H{cx + 4}z" fill="#f7c948" stroke="#b08a1a" stroke-width="2.5"/>'
        b += text(cx, 160, et, 19, weight=900, fill=PRI) + text(cx, 184, enf, 15, weight=700, fill=GRIS)
    save("salud-carencias.svg", svg(980, 200, b, "Consecuencias de la carencia de agua, hierro, yodo, calcio, flúor, sodio, potasio y magnesio"))


if __name__ == "__main__":
    for f in (tabla_bioelementos, composicion, carbono, reconocer, enlaces, grupos, micela, anfotero, abundancia,
              hoja_roca, escala_ph, sales_estructurales, bomba, cocina, tampon, salud):
        f()
