# Esquemas SVG del tema F1 (inmunología) de BioCelia.
# Uso: python tools/esquemas_tema_f1.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "f1")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, LILA, ROJO, VERDE, TEAL = "#0f4c81", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a", "#2a9d8f"
ROSA = "#d1495b"


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


def ab(cx, cy, s=1.0, col=PRI, ang=0):
    """Anticuerpo pequeño en forma de Y; (cx, cy) es la bisagra; ang gira la molécula."""
    L, A = 26 * s, 22 * s
    b = linea(cx, cy, cx, cy + L, col, 4 * s) + linea(cx, cy, cx - A * 0.8, cy - A, col, 4 * s) + linea(cx, cy, cx + A * 0.8, cy - A, col, 4 * s)
    return f'<g transform="rotate({ang} {cx} {cy})">{b}</g>'


def celula(cx, cy, r, fondo, col, nucleo=None, etiqueta=None, size=12.5):
    b = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fondo}" stroke="{col}" stroke-width="2.5"/>'
    if nucleo == "redondo":
        b += f'<circle cx="{cx}" cy="{cy}" r="{r * 0.62}" fill="{col}" opacity="0.35"/>'
    elif nucleo == "lobulado":
        for dx, dy in ((-0.35, -0.15), (0.05, 0.2), (0.38, -0.12)):
            b += f'<circle cx="{cx + dx * r}" cy="{cy + dy * r}" r="{r * 0.24}" fill="{col}" opacity="0.4"/>'
    elif nucleo == "rinon":
        b += f'<path d="M{cx - r * 0.45},{cy - r * 0.2} q{r * 0.45},{-r * 0.5} {r * 0.9},0 q{-r * 0.1},{r * 0.25} {-r * 0.1},{r * 0.45} q{-r * 0.4},{r * 0.2} {-r * 0.8},{-r * 0.45}z" fill="{col}" opacity="0.4"/>'
    if etiqueta:
        b += et(cx, cy + r + 16, etiqueta, col, size, w=900)
    return b


def bacteria(cx, cy, s=1.0, col=VERDE, ang=0):
    w, h = 34 * s, 16 * s
    return f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{h / 2}" fill="#e5f4ec" stroke="{col}" stroke-width="2" transform="rotate({ang} {cx} {cy})"/>'


# ------------------------------------------------------------ órganos y células
def organos():
    b = et(560, 30, "ÓRGANOS Y CÉLULAS DEL SISTEMA INMUNITARIO", PRI, 16, w=900)
    # órganos
    b += f'<rect x="20" y="50" width="400" height="430" rx="16" fill="#fff" stroke="{PRI}" stroke-width="2.5"/>'
    b += et(220, 80, "Órganos linfoides", PRI, 16, w=900)
    b += et(220, 110, "PRIMARIOS: se forman y maduran los linfocitos", ROJO, 13, w=900)
    b += caja(120, 158, 170, 58, "Médula ósea", ROJO, "#fdeaea", 15, "origen de todas; maduran B")
    b += caja(320, 158, 170, 58, "Timo", ROJO, "#fdeaea", 15, "maduran los linfocitos T")
    b += et(220, 230, "SECUNDARIOS: los linfocitos se encuentran", VERDE, 13, w=900) + et(220, 248, "con los antígenos y se activan", VERDE, 13, w=900)
    b += caja(120, 300, 170, 58, "Ganglios linfáticos", VERDE, "#e5f4ec", 14, "filtran la linfa")
    b += caja(320, 300, 170, 58, "Bazo", VERDE, "#e5f4ec", 15, "filtra la sangre")
    b += caja(220, 390, 300, 58, "Amígdalas, placas de Peyer…", VERDE, "#e5f4ec", 14, "tejido linfoide de las mucosas")
    # árbol celular
    x0 = 450
    b += f'<rect x="{x0}" y="50" width="650" height="430" rx="16" fill="#fff" stroke="{LILA}" stroke-width="2.5"/>'
    b += celula(775, 110, 22, "#f4f7fa", GRIS, "redondo")
    b += et(775, 80, "célula madre de la médula ósea", GRIS, 13, w=900)
    b += flecha(755, 128, 630, 180, GRIS) + flecha(795, 128, 920, 180, GRIS)
    b += et(680, 150, "línea mieloide", ACC, 14, "end", 900) + et(870, 150, "línea linfoide", LILA, 14, "start", 900)
    mie = [(510, "Neutrófilo", "lobulado", "fagocito"), (590, "Monocito →", "rinon", "macrófago"), (670, "Mastocito,", "redondo", "basófilo")]
    for x, n, nu, f in mie:
        b += celula(x, 240, 22, "#fff4df", ACC, nu)
        b += et(x, 284, n, ACC, 12.5, w=900) + et(x, 300, f, ACC, 12.5, w=900)
    lin = [(850, "Linfocito B", "redondo"), (940, "Linfocito T", "redondo"), (1030, "Célula NK", "redondo")]
    for x, n, nu in lin:
        b += celula(x, 240, 20, "#efe7fb", LILA, nu)
        b += et(x, 284, n, LILA, 12.5, w=900)
    b += linea(510, 214, 670, 214, ACC, 2) + linea(590, 196, 590, 214, ACC, 2)
    b += linea(850, 214, 1030, 214, LILA, 2) + linea(940, 196, 940, 214, LILA, 2)
    funcs = [("Neutrófilos y macrófagos: fagocitosis; el macrófago presenta antígenos.", ACC),
             ("Mastocitos y basófilos: liberan histamina (inflamación, alergia).", ACC),
             ("Linfocitos B: se transforman en células plasmáticas (anticuerpos) y de memoria.", LILA),
             ("Linfocitos T: cooperadores (activan a otros) y citotóxicos (destruyen células).", LILA),
             ("Células NK: destruyen células infectadas o tumorales sin reconocer un antígeno concreto.", LILA)]
    for k, (f, c) in enumerate(funcs):
        b += et(x0 + 20, 345 + k * 26, f, c, 13, "start")
    save("organos-celulas.svg", svg(1120, 500, b, "Órganos linfoides y células del sistema inmunitario"))


# ------------------------------------------------------------ inflamación
def inflamacion():
    b = et(530, 30, "RESPUESTA INFLAMATORIA (defensa inespecífica)", PRI, 16, w=900)
    # piel
    b += f'<path d="M20,90 H430 L470,140 L510,90 H1040 V130 H20Z" fill="#f6dcc6" stroke="{ACC}" stroke-width="2"/>'
    b += et(80, 115, "piel", ACC, 13, w=900)
    b += f'<path d="M455,60 L485,120" stroke="{GRIS}" stroke-width="5" stroke-linecap="round"/>' + et(420, 60, "herida", GRIS, 13, "end", 900)
    for dx, dy, a in ((470, 160, 20), (500, 185, -30), (440, 200, 60), (530, 165, 0)):
        b += bacteria(dx, dy, 0.8, VERDE, a)
    b += et(600, 175, "bacterias", VERDE, 13, "start", 900)
    # mastocito
    b += celula(250, 200, 30, "#fff4df", ACC, "redondo")
    for k in range(7):
        a = math.radians(k * 50)
        b += f'<circle cx="{250 + 44 * math.cos(a):.1f}" cy="{200 + 44 * math.sin(a):.1f}" r="4" fill="{ROSA}"/>'
    b += et(250, 266, "mastocito", ACC, 13, w=900) + et(250, 284, "libera histamina", ROSA, 13, w=900)
    # capilar
    b += f'<rect x="20" y="330" width="1020" height="90" fill="#fde3e3" stroke="{ROJO}" stroke-width="3"/>'
    b += f'<path d="M20,330 H1040 M20,420 H1040" stroke="{ROJO}" stroke-width="5" stroke-dasharray="40 14"/>'
    b += et(60, 380, "capilar", ROJO, 13, "start", 900)
    for x in (150, 230, 320, 700, 800, 900, 980):
        b += f'<ellipse cx="{x}" cy="380" rx="16" ry="9" fill="{ROJO}" opacity="0.7"/>'
    # neutrófilos saliendo
    b += celula(470, 380, 18, "#fff", PRI, "lobulado")
    b += celula(560, 330, 18, "#fff", PRI, "lobulado")
    b += celula(600, 250, 18, "#fff", PRI, "lobulado")
    b += flecha(470, 360, 540, 340, PRI) + flecha(570, 312, 595, 272, PRI)
    b += et(640, 300, "diapédesis: los leucocitos", PRI, 13, "start", 900) + et(640, 318, "atraviesan la pared del capilar", PRI, 13, "start", 900)
    b += et(630, 230, "fagocitosis", PRI, 13, "start", 900)
    b += linea(530, 196, 586, 240, GRIS, 1.5, 'stroke-dasharray="4 3"')
    # efectos
    b += et(250, 316, "vasodilatación y más permeabilidad", ROJO, 13, w=900)
    signos = [("Rubor (enrojecimiento)", "más sangre en la zona"), ("Calor", "más riego sanguíneo"),
              ("Edema (hinchazón)", "sale plasma del capilar"), ("Dolor", "presión y mediadores"),
              ("Pus", "leucocitos y bacterias muertos")]
    for k, (s, c) in enumerate(signos):
        x = 20 + k * 206
        b += f'<rect x="{x}" y="440" width="196" height="56" rx="10" fill="#fff" stroke="{ROJO}" stroke-width="2"/>'
        b += et(x + 98, 464, s, ROJO, 13.5, w=900) + et(x + 98, 484, c, GRIS, 12)
    save("inflamacion.svg", svg(1060, 510, b, "Respuesta inflamatoria tras una herida en la piel"))


# ------------------------------------------------------------ anticuerpo
def anticuerpo():
    b = ""
    cx, cy = 360, 300
    brazo = 170
    def brazo_pts(lado):
        dx = -1 if lado == "i" else 1
        u = (dx / math.sqrt(2), -1 / math.sqrt(2))
        return u
    for lado, xoff in (("i", -14), ("d", 14)):
        u = brazo_pts(lado)
        x0 = cx + xoff
        # cadena pesada: tallo + brazo
        xe, ye = x0 + u[0] * brazo, cy + u[1] * brazo
        b += f'<path d="M{x0},{cy + 190} V{cy} L{xe:.1f},{ye:.1f}" fill="none" stroke="{PRI}" stroke-width="16" stroke-linejoin="round" stroke-linecap="round"/>'
        # cadena ligera (fuera)
        n = (u[1] * (-1 if lado == "i" else 1), -u[0] * (-1 if lado == "i" else 1))
        n = (-abs(n[0]) if lado == "i" else abs(n[0]), abs(n[1]))
        off = 26
        s0 = 0.3
        xa, ya = x0 + u[0] * brazo * s0 + n[0] * off, cy + u[1] * brazo * s0 + n[1] * off
        xb, yb = x0 + u[0] * brazo + n[0] * off, cy + u[1] * brazo + n[1] * off
        b += linea(xa, ya, xb, yb, TEAL, 14)
        # región variable (punta)
        xv, yv = x0 + u[0] * brazo * 0.72 + n[0] * off / 2, cy + u[1] * brazo * 0.72 + n[1] * off / 2
        b += f'<line x1="{xv:.1f}" y1="{yv:.1f}" x2="{xv + u[0] * brazo * 0.3:.1f}" y2="{yv + u[1] * brazo * 0.3:.1f}" stroke="{ACC}" stroke-width="54" stroke-linecap="round" opacity="0.28"/>'
        # puente disulfuro H-L
        xm, ym = x0 + u[0] * brazo * 0.42, cy + u[1] * brazo * 0.42
        b += linea(xm, ym, xm + n[0] * off, ym + n[1] * off, ROJO, 4, 'stroke-dasharray="4 3"')
    # disulfuros entre pesadas
    for yy in (cy + 18, cy + 36):
        b += linea(cx - 14, yy, cx + 14, yy, ROJO, 4, 'stroke-dasharray="4 3"')
    # antígeno
    b += f'<g transform="translate(-4,40)"><path d="M150,60 q-30,40 10,70 q30,30 70,0 q40,-30 10,-70 q-40,-40 -90,0z" fill="#efe7fb" stroke="{LILA}" stroke-width="3"/>'
    b += f'<path d="M218,118 l14,14 l-14,10 z" fill="{LILA}"/></g>'
    b += et(140, 90, "antígeno", LILA, 14, "end", 900)
    # etiquetas
    lab = [(600, 120, "Región variable (puntas de los brazos)", ACC, "se une al antígeno → parátopo"),
           (600, 190, "Cadena ligera (L)", TEAL, "2 iguales"),
           (600, 250, "Cadena pesada (H)", PRI, "2 iguales; forman el tallo"),
           (600, 320, "Puentes disulfuro", ROJO, "unen las cadenas"),
           (600, 410, "Región constante", INK, "el tallo y el resto de los brazos;"),
           ]
    for x, y, t, c, s in lab:
        b += et(x, y, t, c, 15, "start", 900) + et(x, y + 20, s, GRIS, 12.5, "start")
    b += et(600, 450, "la reconocen fagocitos y complemento;", GRIS, 12.5, "start") + et(600, 470, "define la clase (IgG, IgA, IgM, IgE, IgD)", GRIS, 12.5, "start")
    b += linea(470, 185, 590, 120, GRIS, 1.5) + linea(497, 190, 590, 188, GRIS, 1.5) + linea(392, 260, 590, 248, GRIS, 1.5)
    b += linea(378, 330, 590, 318, GRIS, 1.5) + linea(380, 440, 590, 410, GRIS, 1.5)
    b += et(40, 200, "epítopo: zona del", LILA, 13, "start", 900) + et(40, 218, "antígeno que reconoce", LILA, 13, "start", 900) + et(40, 236, "el anticuerpo", LILA, 13, "start", 900)
    b += linea(110, 186, 212, 172, GRIS, 1.5)
    b += et(450, 520, "Glucoproteína en forma de Y (inmunoglobulina), fabricada por las células plasmáticas.", PRI, 14, w=900)
    save("anticuerpo.svg", svg(900, 540, b, "Estructura de un anticuerpo"))


# ------------------------------------------------------------ clases de Ig
def clases():
    b = ""
    datos = [("IgG", PRI, "monómero", ["la más abundante en sangre", "respuesta SECUNDARIA", "atraviesa la PLACENTA"]),
             ("IgM", ROJO, "pentámero", ["la primera en aparecer:", "respuesta PRIMARIA", "muy aglutinante"]),
             ("IgA", TEAL, "dímero", ["en SECRECIONES: saliva,", "lágrimas, mucosas,", "LECHE materna"]),
             ("IgE", ACC, "monómero", ["ALERGIAS: se une a", "mastocitos y basófilos;", "también parásitos"]),
             ("IgD", LILA, "monómero", ["en la MEMBRANA de", "los linfocitos B", "(receptor)"])]
    for i, (n, c, f, l) in enumerate(datos):
        x = 20 + i * 214
        b += f'<rect x="{x}" y="10" width="200" height="330" rx="16" fill="#fff" stroke="{c}" stroke-width="2.5"/>'
        b += et(x + 100, 42, n, c, 22, w=900)
        cx, cy = x + 100, 135
        if n == "IgM":
            for k in range(5):
                a = k * 72
                b += ab(cx + 34 * math.sin(math.radians(a)), cy - 34 * math.cos(math.radians(a)), 0.95, c, a + 180)
            b += f'<circle cx="{cx}" cy="{cy}" r="7" fill="{c}"/>'
        elif n == "IgA":
            b += ab(cx - 32, cy, 1.2, c, -90) + ab(cx + 32, cy, 1.2, c, 90)
            b += f'<circle cx="{cx}" cy="{cy}" r="6" fill="{c}"/>'
        elif n == "IgD":
            b += f'<rect x="{x + 30}" y="{cy + 34}" width="140" height="14" rx="4" fill="#efe7fb" stroke="{c}" stroke-width="1.5"/>'
            b += ab(cx, cy - 6, 1.6, c)
        else:
            b += ab(cx, cy - 10, 1.8, c)
        b += et(x + 100, 220, f, GRIS, 13, w=900)
        for k, t in enumerate(l):
            b += et(x + 100, 252 + k * 22, t, INK, 12.5)
    save("clases-inmunoglobulinas.svg", svg(1090, 350, b, "Clases de inmunoglobulinas y sus funciones"))


# ------------------------------------------------------------ reacciones Ag-Ac
def reacciones():
    b = ""
    pan = [("Neutralización", PRI, "el anticuerpo bloquea la zona", "con la que el virus o la toxina actúa"),
           ("Aglutinación", ROJO, "agregados de células", "(bacterias, glóbulos rojos)"),
           ("Precipitación", TEAL, "agregados insolubles de", "antígenos solubles que precipitan"),
           ("Opsonización", ACC, "el anticuerpo recubre al antígeno", "y facilita su fagocitosis")]
    for i, (t, c, l1, l2) in enumerate(pan):
        x = 10 + i * 262
        b += f'<rect x="{x}" y="10" width="250" height="300" rx="16" fill="#fff" stroke="{c}" stroke-width="2.5"/>'
        b += et(x + 125, 42, t, c, 17, w=900)
        cx, cy = x + 125, 150
        if i == 0:
            pts = " ".join(f"{cx + 32 * math.cos(math.radians(60 * k + 30)):.1f},{cy + 32 * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
            b += f'<polygon points="{pts}" fill="#fdeaea" stroke="{ROJO}" stroke-width="2.5"/>'
            for k in range(6):
                a = 60 * k
                b += ab(cx + 58 * math.sin(math.radians(a)), cy - 58 * math.cos(math.radians(a)), 0.85, c, a + 180)
            b += et(cx, cy + 6, "virus", ROJO, 12, w=900)
        elif i == 1:
            for dx, dy in ((-50, -30), (40, -40), (-40, 45), (50, 40), (0, 0)):
                b += bacteria(cx + dx, cy + dy, 1.0, VERDE, (dx + dy) % 60)
            for (x1, y1), (x2, y2) in (((-50, -30), (0, 0)), ((40, -40), (0, 0)), ((-40, 45), (0, 0)), ((50, 40), (0, 0)), ((-50, -30), (40, -40))):
                mx, my = cx + (x1 + x2) / 2, cy + (y1 + y2) / 2
                b += ab(mx, my, 0.7, c, math.degrees(math.atan2(y2 - y1, x2 - x1)) + 90)
        elif i == 2:
            for k in range(14):
                xx = cx - 70 + (k % 5) * 35 + (k // 5) % 2 * 17
                yy = cy - 40 + (k // 5) * 40
                b += f'<circle cx="{xx}" cy="{yy}" r="7" fill="{LILA}"/>'
                if k % 2 == 0:
                    b += ab(xx + 16, yy + 10, 0.55, c, 40)
            b += f'<path d="M{cx - 90},{cy + 75} H{cx + 90}" stroke="{GRIS}" stroke-width="3"/>' + et(cx, cy + 92, "precipitado", GRIS, 12, w=900)
        else:
            b += bacteria(cx - 30, cy, 1.6, VERDE)
            for k in range(5):
                b += ab(cx - 52 + k * 12, cy - 28, 0.6, c, 0)
            b += f'<path d="M{cx + 30},{cy - 60} q70,10 70,60 q0,60 -70,60 q30,-30 0,-60 q30,-30 0,-60z" fill="#fff4df" stroke="{ACC}" stroke-width="2.5"/>'
            b += et(cx + 70, cy + 80, "macrófago", ACC, 12, w=900)
        b += et(x + 125, 266, l1, INK, 12.5) + et(x + 125, 284, l2, INK, 12.5)
    save("reacciones-antigeno-anticuerpo.svg", svg(1060, 320, b, "Tipos de reacción antígeno-anticuerpo"))


# ------------------------------------------------------------ respuesta específica
def especifica():
    b = et(560, 28, "RESPUESTA INMUNITARIA ESPECÍFICA: humoral y celular", PRI, 16, w=900)
    # macrófago
    b += f'<path d="M60,170 q-10,-70 60,-80 q70,-10 90,40 q30,60 -20,90 q-60,30 -100,0 q-40,-20 -30,-50z" fill="#fff4df" stroke="{ACC}" stroke-width="3"/>'
    b += bacteria(110, 140, 0.9, VERDE)
    b += et(130, 258, "1 · Macrófago (CPA)", ACC, 13.5, w=900) + et(130, 276, "fagocita y procesa", GRIS, 12) + et(130, 292, "el antígeno", GRIS, 12)
    # CMH
    b += f'<path d="M208,150 h14 v-14 h10 v28 h-24z" fill="{LILA}"/>' + f'<circle cx="236" cy="150" r="6" fill="{VERDE}"/>'
    b += et(230, 110, "CMH + antígeno", LILA, 12.5, w=900)
    # Th
    b += celula(330, 150, 32, "#efe7fb", LILA, "redondo")
    b += et(318, 204, "2 · Linfocito T", LILA, 13.5, w=900) + et(318, 222, "cooperador (Th)", LILA, 13.5, w=900)
    b += et(318, 240, "reconoce el antígeno", GRIS, 12) + et(318, 256, "y libera citocinas", GRIS, 12)
    b += flecha(250, 150, 292, 150, INK)
    # ramas
    b += flecha(360, 130, 470, 90, INK) + flecha(360, 175, 470, 330, INK)
    # humoral
    b += f'<rect x="480" y="46" width="620" height="200" rx="16" fill="#f3f9ff" stroke="{PRI}" stroke-width="2.5"/>'
    b += et(790, 70, "HUMORAL (anticuerpos)", PRI, 15, w=900)
    b += celula(540, 140, 28, "#e3eef8", PRI, "redondo")
    b += et(540, 196, "Linfocito B", PRI, 13, w=900) + et(540, 212, "activado", GRIS, 12)
    b += flecha(572, 125, 660, 105, INK) + flecha(572, 155, 660, 185, INK)
    b += celula(700, 105, 26, "#e3eef8", PRI, "rinon")
    b += et(780, 100, "Célula plasmática", PRI, 13, "start", 900) + et(780, 118, "fabrica anticuerpos", GRIS, 12, "start")
    for k in range(4):
        b += ab(940 + k * 30, 115, 0.7, PRI, 20 * k - 30)
    b += celula(700, 190, 22, "#fff", PRI, "redondo")
    b += et(780, 186, "Linfocito B de memoria", PRI, 13, "start", 900) + et(780, 204, "respuesta secundaria", GRIS, 12, "start")
    b += et(790, 232, "frente a antígenos extracelulares (bacterias, toxinas, virus libres)", GRIS, 12)
    # celular
    b += f'<rect x="480" y="262" width="620" height="200" rx="16" fill="#fbf7ff" stroke="{LILA}" stroke-width="2.5"/>'
    b += et(790, 286, "CELULAR (linfocitos T citotóxicos)", LILA, 15, w=900)
    b += celula(540, 360, 28, "#efe7fb", LILA, "redondo")
    b += et(540, 414, "Linfocito Tc", LILA, 13, w=900)
    b += flecha(572, 360, 660, 360, INK)
    b += f'<circle cx="720" cy="360" r="40" fill="#fdeaea" stroke="{ROJO}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b += f'<circle cx="720" cy="360" r="14" fill="{ROJO}" opacity="0.3"/>'
    for k in range(6):
        a = math.radians(k * 60)
        b += f'<path d="M{720 + 46 * math.cos(a):.1f},{360 + 46 * math.sin(a):.1f} l{6 * math.cos(a):.1f},{6 * math.sin(a):.1f}" stroke="{ROJO}" stroke-width="3"/>'
    b += et(780, 340, "destruye células infectadas", ROJO, 13, "start", 900) + et(780, 358, "por virus, tumorales", ROJO, 13, "start", 900) + et(780, 376, "o trasplantadas", ROJO, 13, "start", 900)
    b += et(780, 404, "(las reconoce por su CMH", GRIS, 12, "start") + et(780, 420, "con antígenos extraños)", GRIS, 12, "start")
    b += et(790, 450, "también deja linfocitos T de memoria", GRIS, 12)
    save("respuesta-especifica.svg", svg(1120, 480, b, "Respuesta inmunitaria específica humoral y celular"))


# ------------------------------------------------------------ primaria y secundaria
def primaria_secundaria():
    x0, y0, w, h = 90, 50, 860, 320
    b = linea(x0, y0 + h, x0 + w, y0 + h, INK, 2.5) + linea(x0, y0 + h, x0, y0 - 10, INK, 2.5)
    b += et(x0 + w / 2, y0 + h + 44, "tiempo (días)", GRIS, 14, w=900)
    b += text(36, y0 + h / 2, "concentración de anticuerpos", 14, weight=900, fill=GRIS, style=f'transform="rotate(-90 36 {y0 + h / 2})"')
    t2 = 0.5
    def curva(f, col, dash=""):
        pts = [(x0 + t * w, y0 + h - f(t) * h) for t in [k / 200 for k in range(201)]]
        return f'<polyline points="{" ".join(f"{a:.1f},{c:.1f}" for a, c in pts)}" fill="none" stroke="{col}" stroke-width="4" {dash}/>'
    g = lambda t, t0, a, s, d: a * math.exp(-((t - t0) / s) ** 2) if t < t0 else a * math.exp(-((t - t0) / d) ** 2)
    igm = lambda t: g(t, 0.17, 0.22, 0.06, 0.09) + g(t, t2 + 0.07, 0.2, 0.03, 0.06)
    igg = lambda t: (g(t, 0.24, 0.12, 0.08, 0.2) if t < t2 else 0.12 * math.exp(-((t2 - 0.24) / 0.2) ** 2) * 0 + 0.03 + 0) + (g(t, t2 + 0.12, 0.85, 0.06, 0.4) if t > t2 else 0)
    b += curva(igm, ROJO) + curva(igg, PRI)
    for t, s in ((0.04, "1.ª exposición"), (t2, "2.ª exposición (mismo antígeno)")):
        x = x0 + t * w
        b += flecha(x, y0 + h + 30, x, y0 + h + 4, VERDE, 3) + et(x, y0 + h + 22, "", INK)
        b += et(x + 6, y0 - 16, s, VERDE, 13.5, "start", 900)
        b += linea(x, y0 - 6, x, y0 + h, VERDE, 1.5, 'stroke-dasharray="6 5"')
    b += et(x0 + 0.17 * w, y0 + h - 0.22 * h - 12, "IgM", ROJO, 15, w=900)
    b += et(x0 + 0.33 * w, y0 + h - 0.1 * h - 14, "IgG", PRI, 15, w=900)
    b += et(x0 + 0.66 * w, y0 + h - 0.85 * h - 12, "IgG", PRI, 15, w=900)
    b += et(x0 + 0.62 * w, y0 + h - 0.2 * h, "IgM", ROJO, 15, "start", 900)
    b += et(x0 + 0.2 * w, y0 + 60, "PRIMARIA", ROJO, 16, w=900) + et(x0 + 0.2 * w, y0 + 80, "lenta (latencia de días)", GRIS, 12.5) + et(x0 + 0.2 * w, y0 + 96, "poco intensa · sobre todo IgM", GRIS, 12.5)
    b += et(x0 + 0.86 * w, y0 + 200, "SECUNDARIA", PRI, 16, w=900) + et(x0 + 0.86 * w, y0 + 220, "rápida e intensa,", GRIS, 12.5) + et(x0 + 0.86 * w, y0 + 236, "duradera · sobre todo IgG", GRIS, 12.5)
    b += et(x0 + w / 2, y0 + h + 76, "La diferencia la marcan las células de memoria: así funcionan las vacunas y las dosis de recuerdo.", PRI, 14, w=900)
    save("respuesta-primaria-secundaria.svg", svg(980, 470, b, "Respuesta inmunitaria primaria y secundaria"))


# ------------------------------------------------------------ curso de una infección
def curso():
    x0, y0, w, h = 80, 70, 800, 240
    b = linea(x0, y0 + h, x0 + w, y0 + h, INK, 2.5) + linea(x0, y0 + h, x0, y0 - 10, INK, 2.5)
    fases = [(0, 0.25, "1 · Incubación", "el patógeno se multiplica; sin síntomas", "#eef1f4"),
             (0.25, 0.6, "2 · Fase sintomática", "aparecen los síntomas", "#fdeaea"),
             (0.6, 1.0, "3 · Convalecencia", "recuperación", "#e5f4ec")]
    for a, c, t, s, f in fases:
        b += f'<rect x="{x0 + a * w}" y="{y0 - 10}" width="{(c - a) * w}" height="{h + 10}" fill="{f}" opacity="0.7"/>'
        b += et(x0 + (a + c) / 2 * w, y0 - 26, t, INK, 14, w=900) + et(x0 + (a + c) / 2 * w, y0 + h + 24, s, GRIS, 12)
    def curva(f, col):
        pts = [(x0 + t * w, y0 + h - f(t) * h) for t in [k / 200 for k in range(201)]]
        return f'<polyline points="{" ".join(f"{a:.1f},{c:.1f}" for a, c in pts)}" fill="none" stroke="{col}" stroke-width="4"/>'
    pat = lambda t: 0.85 * math.exp(-((t - 0.38) / 0.16) ** 2)
    igm = lambda t: 0.55 * math.exp(-((t - 0.42) / (0.1 if t < 0.42 else 0.14)) ** 2)
    igg = lambda t: 0.75 / (1 + math.exp(-(t - 0.6) / 0.05)) if t < 0.85 else 0.75 / (1 + math.exp(-(0.25) / 0.05)) - (t - 0.85) * 0.3
    b += curva(pat, GRIS) + curva(igm, ROJO) + curva(igg, PRI)
    b += et(x0 + 0.3 * w, y0 + h - 0.88 * h, "patógeno", GRIS, 13.5, w=900)
    b += et(x0 + 0.42 * w, y0 + h - 0.22 * h, "A: IgM", ROJO, 14, w=900)
    b += et(x0 + 0.86 * w, y0 + h - 0.78 * h, "B: IgG", PRI, 14, w=900)
    b += et(x0 + w / 2, y0 + h + 54, "Infección no es lo mismo que enfermedad: en la incubación ya hay infección (y puede haber contagio) sin síntomas.", PRI, 13, w=900)
    save("curso-infeccion.svg", svg(900, 390, b, "Fases de una enfermedad infecciosa y anticuerpos IgM e IgG"))


# ------------------------------------------------------------ tipos de inmunidad
def tipos():
    b = et(40, 70, "", INK)
    b += caja(330, 34, 300, 40, "ACTIVA: el organismo fabrica", VERDE, "#e5f4ec", 14)
    b += caja(720, 34, 300, 40, "PASIVA: recibe anticuerpos hechos", ACC, "#fff4df", 14)
    b += et(90, 128, "NATURAL", PRI, 16, w=900) + et(90, 274, "ARTIFICIAL", LILA, 16, w=900)
    celdas = [(330, 130, "Pasar la infección", "linfocitos propios", VERDE), (720, 130, "Anticuerpos de la madre", "IgG por la placenta; IgA en la leche", ACC),
              (330, 276, "Vacunación", "antígenos del patógeno", VERDE), (720, 276, "Sueroterapia", "anticuerpos de otra persona o animal", ACC)]
    for x, y, t, s, c in celdas:
        b += f'<rect x="{x - 180}" y="{y - 56}" width="360" height="112" rx="14" fill="#fff" stroke="{c}" stroke-width="2.5"/>'
        b += et(x, y - 14, t, c, 17, w=900) + et(x, y + 10, s, GRIS, 13)
    b += et(330, 162, "memoria · duradera", VERDE, 13, w=900) + et(720, 162, "sin memoria · temporal", ACC, 13, w=900)
    b += et(330, 308, "PREVENTIVA · memoria · tarda en actuar", VERDE, 13, w=900) + et(720, 308, "CURATIVA · inmediata · dura poco", ACC, 13, w=900)
    save("tipos-inmunidad.svg", svg(920, 350, b, "Tipos de inmunidad adquirida: activa y pasiva, natural y artificial"))


# ------------------------------------------------------------ alergia
def alergia():
    b = et(530, 30, "REACCIÓN ALÉRGICA (hipersensibilidad inmediata)", PRI, 16, w=900)
    # primer contacto
    b += f'<rect x="20" y="50" width="490" height="300" rx="16" fill="#fff" stroke="{PRI}" stroke-width="2.5"/>'
    b += et(265, 80, "1.er contacto: SENSIBILIZACIÓN (sin síntomas)", PRI, 14, w=900)
    for dx, dy in ((60, 140), (80, 170), (50, 190)):
        b += f'<circle cx="{dx}" cy="{dy}" r="9" fill="#f4d35e" stroke="{ACC}" stroke-width="2"/>'
    b += et(70, 222, "alérgeno", ACC, 12.5, w=900) + et(70, 238, "(polen…)", GRIS, 12)
    b += flecha(110, 170, 160, 170, INK)
    b += celula(200, 170, 28, "#e3eef8", PRI, "redondo", "linfocito B → plasmática", 12)
    b += flecha(240, 170, 300, 170, INK)
    for k in range(3):
        b += ab(320 + k * 22, 172, 0.7, ACC, 0)
    b += et(342, 210, "IgE", ACC, 14, w=900)
    b += flecha(380, 170, 410, 170, INK)
    b += celula(450, 170, 30, "#fff4df", ACC, "redondo")
    for k in range(5):
        a = -150 + k * 30
        b += ab(450 + 34 * math.cos(math.radians(a)), 170 + 34 * math.sin(math.radians(a)), 0.55, ACC, a + 90 + 180)
    for dx, dy in ((-10, 8), (8, -6), (12, 12), (-6, -12)):
        b += f'<circle cx="{450 + dx}" cy="{170 + dy}" r="4" fill="{ROSA}"/>'
    b += et(450, 236, "mastocito con IgE", ACC, 12.5, w=900) + et(450, 252, "en su membrana", GRIS, 12)
    b += et(265, 300, "El sistema inmunitario produce IgE frente a", GRIS, 12.5) + et(265, 318, "una sustancia inofensiva", GRIS, 12.5)
    # segundo contacto
    b += f'<rect x="530" y="50" width="510" height="300" rx="16" fill="#fff" stroke="{ROJO}" stroke-width="2.5"/>'
    b += et(785, 80, "2.º contacto: REACCIÓN", ROJO, 14, w=900)
    cx, cy = 640, 190
    b += celula(cx, cy, 34, "#fff4df", ACC, "redondo")
    for k in range(5):
        a = -150 + k * 30
        b += ab(cx + 38 * math.cos(math.radians(a)), cy + 38 * math.sin(math.radians(a)), 0.55, ACC, a + 90 + 180)
    for k in range(3):
        a = math.radians(-130 + k * 40)
        b += f'<circle cx="{cx + 64 * math.cos(a):.1f}" cy="{cy + 64 * math.sin(a):.1f}" r="9" fill="#f4d35e" stroke="{ACC}" stroke-width="2"/>'
    for k in range(8):
        a = math.radians(-60 + k * 13)
        b += f'<circle cx="{cx + 60 * math.cos(a):.1f}" cy="{cy + 60 * math.sin(a):.1f}" r="4" fill="{ROSA}"/>'
    b += et(cx, cy + 66, "el alérgeno se une a las IgE", GRIS, 12) + et(cx, cy + 82, "y el mastocito se desgranula", GRIS, 12)
    b += et(790, 140, "HISTAMINA", ROSA, 16, "start", 900)
    efectos = ["vasodilatación (rojez, calor)", "más permeabilidad (edema)", "más secreciones (moco, lágrimas)", "contracción de bronquios (asma)", "si es generalizada: anafilaxia"]
    for k, e in enumerate(efectos):
        b += et(790, 172 + k * 24, "• " + e, INK, 13, "start")
    b += flecha(710, 160, 780, 140, ROSA)
    b += et(530, 376, "Tratamiento: antihistamínicos; en la anafilaxia, adrenalina.", PRI, 13.5, w=900)
    save("alergia.svg", svg(1060, 392, b, "Mecanismo de una reacción alérgica"))


if __name__ == "__main__":
    organos(); inflamacion(); anticuerpo(); clases(); reacciones(); especifica(); primaria_secundaria(); curso(); tipos(); alergia()
