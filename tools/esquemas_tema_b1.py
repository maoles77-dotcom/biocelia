# Esquemas SVG del tema B1 (genética molecular) de BioCelia.
# Uso: python tools/esquemas_tema_b1.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK, BLUE

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "b1")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO, VERDE = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"
VIEJA, NUEVA, CEBADOR, ARN = "#1f5f99", "#e07a2e", "#d62828", "#8e44ad"


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)


def save(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def linea(x1, y1, x2, y2, col=INK, w=3, extra=""):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def flecha(x1, y1, x2, y2, col=INK, w=2.5):
    m = "fl" if col == BLUE else "fk"
    return linea(x1, y1, x2, y2, col, w, f'marker-end="url(#{m})"')


def hebra(pts, col, w=6, flecha_fin=False):
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    s = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
    if flecha_fin:
        (xa, ya), (xb, yb) = pts[-2], pts[-1]
        ang = math.atan2(yb - ya, xb - xa)
        p1 = (xb + 12 * math.cos(ang), yb + 12 * math.sin(ang))
        p2 = (xb + 9 * math.cos(ang + 2.2), yb + 9 * math.sin(ang + 2.2))
        p3 = (xb + 9 * math.cos(ang - 2.2), yb + 9 * math.sin(ang - 2.2))
        s += f'<polygon points="{p1[0]:.1f},{p1[1]:.1f} {p2[0]:.1f},{p2[1]:.1f} {p3[0]:.1f},{p3[1]:.1f}" fill="{col}"/>'
    return s


def etiqueta(x, y, tx, ty, s, col=INK, anchor="middle", size=15):
    return linea(x, y, tx, ty, GRIS, 1.5, 'stroke-dasharray="4 3"') + text(tx, ty + (-6 if ty < y else 16), s, size, anchor, 900, fill=col)


def leyenda(x, y, items, size=14):
    s = ""
    for i, (col, t) in enumerate(items):
        s += f'<rect x="{x}" y="{y + i * 24 - 6}" width="30" height="8" rx="4" fill="{col}"/>' + text(x + 40, y + i * 24 + 3, t, size, "start", 800)
    return s


# ---------------------------------------------------------------- dogma central
def dogma():
    def nodo(x, y, t, col, fondo):
        return f'<rect x="{x - 95}" y="{y - 36}" width="190" height="72" rx="18" fill="{fondo}" stroke="{col}" stroke-width="3"/>' + text(x, y + 10, t, 28, weight=900, fill=col)
    b = nodo(140, 170, "ADN", VIEJA, "#e3eef8") + nodo(500, 170, "ARN", ARN, "#f1e6f8") + nodo(860, 170, "Proteína", VERDE, "#e5f4ec")
    b += flecha(240, 160, 396, 160, INK, 3) + text(318, 145, "transcripción", 17, weight=900, fill=PRI)
    b += flecha(600, 170, 756, 170, INK, 3) + text(678, 155, "traducción", 17, weight=900, fill=PRI)
    # replicaciones
    b += f'<path d="M100,132 C70,60 210,60 180,132" fill="none" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>' + text(140, 58, "replicación", 17, weight=900, fill=PRI)
    b += f'<path d="M460,132 C430,60 570,60 540,132" fill="none" stroke="{LILA}" stroke-width="3" stroke-dasharray="7 5" marker-end="url(#fk)"/>' + text(500, 52, "replicación del ARN", 16, weight=900, fill=LILA)
    b += text(500, 72, "(virus de ARN)", 14, weight=800, fill=LILA)
    # transcripción inversa
    b += f'<path d="M420,206 C360,260 280,260 220,212" fill="none" stroke="{LILA}" stroke-width="3" stroke-dasharray="7 5" marker-end="url(#fk)"/>'
    b += text(320, 270, "transcripción inversa", 16, weight=900, fill=LILA) + text(320, 290, "(retrovirus: retrotranscriptasa)", 14, weight=800, fill=LILA)
    b += text(500, 330, "— Dogma inicial (Crick, 1958)      - - - Ampliaciones posteriores", 15, weight=800, fill=GRIS)
    b += text(860, 245, "nunca de proteína", 14, weight=800, fill=ROJO) + text(860, 263, "a ácido nucleico", 14, weight=800, fill=ROJO)
    save("dogma-central.svg", svg(1000, 345, b, "Dogma central de la biología molecular y sus ampliaciones"))


# ---------------------------------------------------------------- genoma
def genoma():
    b = text(250, 30, "Procariota (bacteria)", 22, weight=900, fill=PRI) + text(750, 30, "Eucariota", 22, weight=900, fill=PRI)
    b += f'<rect x="40" y="55" width="420" height="250" rx="110" fill="#f2f8ec" stroke="{VERDE}" stroke-width="4"/>'
    b += f'<path d="M140,180 C140,110 260,100 300,140 C340,180 380,150 360,210 C340,260 250,250 220,240 C170,225 140,230 140,180z" fill="none" stroke="{VIEJA}" stroke-width="5"/>'
    b += f'<circle cx="400" cy="120" r="18" fill="none" stroke="{ACC}" stroke-width="4"/><circle cx="110" cy="250" r="14" fill="none" stroke="{ACC}" stroke-width="4"/>'
    b += text(250, 180, "nucleoide", 15, weight=900, fill=VIEJA)
    b += text(250, 200, "ADN circular", 14, weight=800, fill=VIEJA)
    b += etiqueta(400, 138, 250, 328, "plásmidos", ACC) + linea(110, 264, 250, 328, GRIS, 1.5, 'stroke-dasharray="4 3"')
    b += text(250, 370, "Sin envoltura nuclear · en el citoplasma", 14, weight=800, fill=GRIS)
    # eucariota: núcleo con cromosomas lineales
    b += f'<circle cx="750" cy="185" r="140" fill="#eef4fa" stroke="{PRI}" stroke-width="5" stroke-dasharray="26 6"/>'
    for i, (x, y, ang) in enumerate([(690, 120, 15), (810, 130, -20), (690, 240, -10), (810, 235, 25)]):
        r = math.radians(ang)
        dx, dy = 45 * math.cos(r), 45 * math.sin(r)
        b += linea(x - dx, y - dy, x + dx, y + dy, VIEJA, 6)
        for k in (-1, 0, 1):
            b += f'<circle cx="{x + k * dx * 0.6:.1f}" cy="{y + k * dy * 0.6:.1f}" r="7" fill="#f4a261" stroke="#b5651d" stroke-width="1.5"/>'
    b += text(750, 300, "núcleo", 15, weight=900, fill=PRI)
    b += etiqueta(855, 240, 940, 345, "histonas", "#b5651d")
    b += text(750, 370, "Varios cromosomas lineales en el núcleo", 14, weight=800, fill=GRIS)
    # tabla comparativa
    filas = [("Molécula", "una, circular", "varias, lineales"),
             ("Localización", "nucleoide (citoplasma)", "núcleo (+ mitocondrias, cloroplastos)"),
             ("Proteínas", "sin histonas", "asociado a histonas"),
             ("Genes", "continuos, sin intrones", "con exones e intrones"),
             ("ADN no codificante", "escaso", "abundante"),
             ("Plásmidos", "frecuentes", "raros (algunas levaduras)")]
    y0 = 400
    for i, (a, p, e) in enumerate(filas):
        y = y0 + i * 34
        b += f'<rect x="20" y="{y}" width="960" height="34" fill="{"#f6f9fb" if i % 2 == 0 else "#fff"}"/>'
        b += text(40, y + 23, a, 15, "start", 900, fill=PRI) + text(330, y + 23, p, 15, "middle", 800) + text(740, y + 23, e, 15, "middle", 800)
    save("genoma-pro-euc.svg", svg(1000, y0 + 6 * 34 + 10, b, "Genoma procariota y eucariota"))


def genes():
    def bloque(x, w, y, t, col, fondo, tc="#fff"):
        return f'<rect x="{x}" y="{y}" width="{w}" height="46" rx="6" fill="{fondo}" stroke="{col}" stroke-width="2"/>' + text(x + w / 2, y + 29, t, 15, weight=900, fill=tc)
    b = text(30, 40, "Gen procariota: continuo", 20, "start", 900, fill=PRI)
    y = 60
    b += linea(20, y + 23, 980, y + 23, GRIS, 4)
    b += bloque(60, 150, y, "promotor", ACC, "#fff4df", ACC) + bloque(220, 600, y, "región codificante continua", VIEJA, VIEJA) + bloque(830, 130, y, "terminador", ROJO, "#fde8e6", ROJO)
    b += text(520, y + 75, "A menudo varios genes seguidos se transcriben en un solo ARNm (policistrónico, operón)", 14, weight=800, fill=GRIS)
    b += text(30, 190, "Gen eucariota: fragmentado", 20, "start", 900, fill=PRI)
    y = 210
    b += linea(20, y + 23, 980, y + 23, GRIS, 4)
    b += bloque(60, 150, y, "promotor", ACC, "#fff4df", ACC)
    x = 220
    for i, (t, w) in enumerate([("exón", 130), ("intrón", 110), ("exón", 120), ("intrón", 110), ("exón", 120)]):
        if t == "exón":
            b += bloque(x, w, y, t, VIEJA, VIEJA)
        else:
            b += bloque(x, w, y, t, "#9aa7b2", "#e9edf0", GRIS)
        x += w + 2
    b += bloque(830, 130, y, "terminador", ROJO, "#fde8e6", ROJO)
    b += text(520, y + 75, "Exones: se expresan · Intrones: se transcriben pero se eliminan en la maduración (monocistrónico)", 14, weight=800, fill=GRIS)
    save("genes-pro-euc.svg", svg(1000, 310, b, "Estructura de un gen procariota y de un gen eucariota"))


# ---------------------------------------------------------------- Meselson y Stahl
def meselson():
    def duplex(x, y, c1, c2, h=110):
        s = linea(x, y, x, y + h, c1, 8) + linea(x + 22, y, x + 22, y + h, c2, 8)
        for k in range(1, 6):
            s += linea(x + 4, y + k * h / 6, x + 18, y + k * h / 6, "#b8c2cc", 2)
        return s
    P_, L_ = VIEJA, NUEVA
    b = text(110, 30, "Generación 0", 18, weight=900, fill=PRI) + text(380, 30, "Generación 1", 18, weight=900, fill=PRI) + text(740, 30, "Generación 2", 18, weight=900, fill=PRI)
    b += duplex(99, 60, P_, P_)
    b += flecha(160, 115, 300, 115) + text(230, 100, "replicación", 14, weight=800, fill=GRIS) + text(230, 140, "en ¹⁴N", 14, weight=900, fill=NUEVA)
    b += duplex(330, 60, P_, L_) + duplex(410, 60, L_, P_)
    b += flecha(470, 115, 590, 115) + text(530, 140, "en ¹⁴N", 14, weight=900, fill=NUEVA)
    for i, (c1, c2) in enumerate([(P_, L_), (L_, L_), (L_, L_), (L_, P_)]):
        b += duplex(625 + i * 80, 60, c1, c2)
    # tubos de centrifugación
    def tubo(cx, bandas, et):
        s = f'<path d="M{cx - 26},230 V380 A26,26 0 0 0 {cx + 26},380 V230" fill="#f4f8fb" stroke="#7b8a97" stroke-width="3"/>'
        for yb in bandas:
            s += f'<rect x="{cx - 22}" y="{yb - 5}" width="44" height="10" rx="4" fill="{INK}"/>'
        return s + text(cx, 440, et, 15, weight=900, fill=PRI)
    pos = {"pesado": 380, "intermedio": 330, "ligero": 280}
    b += tubo(110, [pos["pesado"]], "solo pesado") + tubo(380, [pos["intermedio"]], "solo intermedio") + tubo(740, [pos["intermedio"], pos["ligero"]], "intermedio + ligero")
    for nombre, yb in pos.items():
        b += text(905, yb + 5, nombre, 14, "start", 800, fill=GRIS) + linea(780, yb, 895, yb, "#c3ccd4", 1.2, 'stroke-dasharray="3 3"')
    b += text(905, pos["pesado"] + 23, "(¹⁵N-¹⁵N)", 13, "start", 800, fill=VIEJA) + text(905, pos["intermedio"] + 23, "(¹⁵N-¹⁴N)", 13, "start", 800, fill=GRIS) + text(905, pos["ligero"] + 23, "(¹⁴N-¹⁴N)", 13, "start", 800, fill=NUEVA)
    b += text(940, 240, "Densidad", 14, weight=900, fill=GRIS)
    b += leyenda(40, 480, [(VIEJA, "hebra original (¹⁵N, pesada)"), (NUEVA, "hebra nueva (¹⁴N, ligera)")])
    b += text(720, 494, "Cada ADN hijo: una hebra vieja + una nueva", 16, weight=900, fill=PRI)
    save("meselson-stahl.svg", svg(1020, 520, b, "Experimento de Meselson y Stahl: replicación semiconservativa"))


# ---------------------------------------------------------------- horquilla
def horquilla():
    b = ""
    # dúplex parental a la derecha
    for x in range(820, 1060, 20):
        b += linea(x, 238, x, 262, "#b8c2cc", 2)
    b += hebra([(820, 232), (1070, 232)], VIEJA) + hebra([(820, 268), (1070, 268)], VIEJA)
    # hebras molde abiertas
    b += hebra([(820, 232), (770, 232), (700, 140), (40, 140)], VIEJA)
    b += hebra([(820, 268), (770, 268), (700, 360), (40, 360)], VIEJA)
    b += text(28, 145, "3'", 16, "end", 900, fill=VIEJA) + text(1080, 237, "5'", 16, "start", 900, fill=VIEJA)
    b += text(28, 365, "5'", 16, "end", 900, fill=VIEJA) + text(1080, 273, "3'", 16, "start", 900, fill=VIEJA)
    # hebra adelantada (5'→3' hacia la horquilla)
    b += hebra([(60, 162), (88, 162)], CEBADOR, 7) + hebra([(88, 162), (628, 162)], NUEVA, 6, True)
    b += text(52, 185, "5'", 14, "middle", 900, fill=NUEVA)
    b += f'<ellipse cx="660" cy="162" rx="34" ry="22" fill="#d7ecd9" stroke="{VERDE}" stroke-width="2.5"/>' + text(660, 167, "ADN pol", 12, weight=900, fill=VERDE)
    # hebra retrasada: fragmentos de Okazaki (5'→3' alejándose de la horquilla)
    b += hebra([(60, 338), (252, 338)], NUEVA, 6)  # ya unida
    b += hebra([(262, 338), (392, 338)], NUEVA, 6)
    b += hebra([(392, 338), (418, 338)], CEBADOR, 7)  # cebador siendo eliminado
    b += hebra([(578, 338), (440, 338)], NUEVA, 6, True)
    b += hebra([(604, 338), (578, 338)], CEBADOR, 7)
    b += hebra([(712, 338), (686, 338)], CEBADOR, 7)
    b += text(52, 320, "3'", 14, "middle", 900, fill=NUEVA) + text(612, 322, "5'", 14, "middle", 900, fill=NUEVA)
    b += f'<ellipse cx="420" cy="338" rx="32" ry="20" fill="#d7ecd9" stroke="{VERDE}" stroke-width="2.5"/>' + text(420, 343, "ADN pol", 12, weight=900, fill=VERDE)
    b += f'<circle cx="257" cy="338" r="14" fill="#fde2c4" stroke="{ACC}" stroke-width="2.5"/>' + text(257, 343, "L", 13, weight=900, fill=ACC)
    b += f'<ellipse cx="715" cy="318" rx="28" ry="15" fill="#f6d6e0" stroke="{CEBADOR}" stroke-width="2"/>' + text(715, 322, "primasa", 11, weight=900, fill=CEBADOR)
    # helicasa, SSB, topoisomerasa
    b += f'<polygon points="790,226 812,214 834,226 834,274 812,286 790,274" fill="#ffe08a" stroke="{ACC}" stroke-width="3"/>' + text(812, 255, "H", 18, weight=900, fill="#8a5a00")
    for x, y in [(728, 148), (752, 190), (728, 352), (752, 310)]:
        b += f'<circle cx="{x}" cy="{y}" r="8" fill="#cfe3f5" stroke="{PRI}" stroke-width="1.8"/>'
    b += f'<rect x="930" y="216" width="56" height="68" rx="16" fill="#e7dcf7" stroke="{LILA}" stroke-width="3"/>' + text(958, 256, "T", 18, weight=900, fill=LILA)
    # etiquetas
    b += text(330, 205, "Hebra adelantada o conductora: continua", 17, weight=900, fill=NUEVA)
    b += text(330, 305, "Hebra retrasada o retardada: discontinua", 17, weight=900, fill=NUEVA)
    b += etiqueta(74, 162, 90, 70, "cebador (ARN)", CEBADOR, "start")
    b += etiqueta(510, 345, 520, 395, "fragmento de Okazaki", NUEVA)
    b += etiqueta(257, 352, 230, 395, "ADN ligasa", ACC)
    b += etiqueta(420, 358, 440, 440, "ADN pol I: quita el cebador y rellena", VERDE, "start", 14)
    b += etiqueta(660, 140, 660, 70, "ADN pol III", VERDE)
    b += etiqueta(715, 333, 760, 490, "primasa: fabrica cebadores", CEBADOR, "start", 14)
    b += etiqueta(812, 214, 840, 160, "helicasa: separa las hebras", ACC, "start", 14)
    b += etiqueta(752, 190, 770, 70, "SSB: mantienen separadas", PRI, "start", 14)
    b += etiqueta(958, 284, 958, 380, "topoisomerasa:", LILA, "middle", 14) + text(958, 414, "evita el superenrollamiento", 14, weight=900, fill=LILA)
    b += flecha(860, 330, 920, 330, INK, 3) + text(890, 318, "avance", 13, weight=900, fill=GRIS)
    b += leyenda(40, 480, [(VIEJA, "hebra molde (original)"), (NUEVA, "ADN nuevo"), (CEBADOR, "cebador de ARN")])
    save("horquilla-replicacion.svg", svg(1100, 540, b, "Horquilla de replicación: enzimas, hebra adelantada y hebra retrasada"))


def burbuja():
    b = ""
    b += hebra([(30, 228), (200, 228), (260, 140), (840, 140), (900, 228), (1070, 228)], VIEJA)
    b += hebra([(30, 272), (200, 272), (260, 360), (840, 360), (900, 272), (1070, 272)], VIEJA)
    for x in list(range(40, 200, 20)) + list(range(910, 1070, 20)):
        b += linea(x, 234, x, 266, "#b8c2cc", 2)
    b += text(18, 233, "3'", 15, "end", 900, fill=VIEJA) + text(1082, 233, "5'", 15, "start", 900, fill=VIEJA)
    b += text(18, 277, "5'", 15, "end", 900, fill=VIEJA) + text(1082, 277, "3'", 15, "start", 900, fill=VIEJA)
    # origen
    b += linea(550, 120, 550, 380, ROJO, 2, 'stroke-dasharray="6 4"') + text(550, 110, "origen de replicación", 16, weight=900, fill=ROJO)
    # hebras nuevas. Molde superior 3'→5' (izq→dcha): nueva 5'→3' hacia la derecha
    b += hebra([(556, 162), (812, 162)], NUEVA, 6, True)  # adelantada hacia horquilla derecha
    for x0 in (300, 390, 470):
        b += hebra([(x0, 162), (x0 + 62, 162)], NUEVA, 6, True)  # retrasada (fragmentos) hacia la derecha
    # molde inferior 5'→3': nueva 5'→3' hacia la izquierda
    b += hebra([(544, 338), (288, 338)], NUEVA, 6, True)  # adelantada hacia horquilla izquierda
    for x0 in (800, 710, 630):
        b += hebra([(x0, 338), (x0 - 62, 338)], NUEVA, 6, True)
    b += text(690, 190, "adelantada", 14, weight=900, fill=NUEVA) + text(410, 190, "retrasada", 14, weight=900, fill=NUEVA)
    b += text(410, 320, "adelantada", 14, weight=900, fill=NUEVA) + text(690, 320, "retrasada", 14, weight=900, fill=NUEVA)
    b += flecha(205, 250, 140, 250, INK, 4) + flecha(895, 250, 960, 250, INK, 4)
    b += text(200, 410, "horquilla", 16, weight=900, fill=ACC) + text(900, 410, "horquilla", 16, weight=900, fill=ACC)
    b += text(550, 440, "Burbuja de replicación: dos horquillas avanzan en sentidos opuestos (bidireccional)", 16, weight=900, fill=PRI)
    save("burbuja-replicacion.svg", svg(1100, 460, b, "Burbuja de replicación bidireccional"))


def origenes():
    b = text(240, 32, "Procariota: un origen", 20, weight=900, fill=PRI) + text(760, 32, "Eucariota: muchos orígenes", 20, weight=900, fill=PRI)
    # cromosoma circular con burbuja (forma theta)
    cx, cy, r = 240, 190, 105
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{VIEJA}" stroke-width="6"/>'
    b += f'<path d="M{cx + r * math.cos(math.radians(-130)):.1f},{cy + r * math.sin(math.radians(-130)):.1f} A{r - 16},{r - 16} 0 0 1 {cx + r * math.cos(math.radians(-50)):.1f},{cy + r * math.sin(math.radians(-50)):.1f}" fill="none" stroke="{NUEVA}" stroke-width="6"/>'
    b += f'<circle cx="{cx}" cy="{cy - r}" r="7" fill="{ROJO}"/>' + text(cx, cy - r - 14, "ori", 15, weight=900, fill=ROJO)
    for ang, sgn in ((-130, -1), (-50, 1)):
        x, y = cx + r * math.cos(math.radians(ang)), cy + r * math.sin(math.radians(ang))
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#ffe08a" stroke="{ACC}" stroke-width="2.5"/>'
    b += text(cx, cy + 6, "ADN circular", 15, weight=900, fill=VIEJA) + text(cx, cy + 26, "(citoplasma)", 13, weight=800, fill=GRIS)
    b += text(cx, 330, "Dos horquillas que se encuentran en el lado opuesto", 13, weight=800, fill=GRIS)
    # lineal eucariota con varias burbujas
    y = 190
    b += linea(520, y, 1000, y, VIEJA, 6)
    for xc in (580, 690, 800, 920):
        w = 34
        b += f'<path d="M{xc - w},{y} Q{xc},{y - 46} {xc + w},{y}" fill="none" stroke="{VIEJA}" stroke-width="6"/>'
        b += f'<path d="M{xc - w},{y} Q{xc},{y + 46} {xc + w},{y}" fill="none" stroke="{NUEVA}" stroke-width="6"/>'
        b += f'<circle cx="{xc}" cy="{y}" r="5" fill="{ROJO}"/>'
    b += text(760, 270, "ADN lineal largo, en el núcleo", 15, weight=900, fill=VIEJA)
    b += text(760, 300, "Muchos replicones a la vez: replicación más rápida", 13, weight=800, fill=GRIS)
    b += leyenda(560, 80, [(ROJO, "origen de replicación"), (ACC, "horquilla")])
    save("origenes-replicacion.svg", svg(1020, 350, b, "Origen único en procariotas y orígenes múltiples en eucariotas"))


# ---------------------------------------------------------------- transcripción
def transcripcion():
    b = ""
    # cadena codificante (arriba, 5'→3') y molde (abajo, 3'→5')
    b += hebra([(40, 150), (430, 150), (470, 110), (650, 110), (690, 150), (1060, 150)], "#5b8fc7")
    b += hebra([(40, 190), (430, 190), (470, 230), (650, 230), (690, 190), (1060, 190)], VIEJA)
    for x in list(range(50, 430, 20)) + list(range(700, 1060, 20)):
        b += linea(x, 156, x, 184, "#b8c2cc", 2)
    b += text(28, 155, "5'", 15, "end", 900, fill="#5b8fc7") + text(1072, 155, "3'", 15, "start", 900, fill="#5b8fc7")
    b += text(28, 195, "3'", 15, "end", 900, fill=VIEJA) + text(1072, 195, "5'", 15, "start", 900, fill=VIEJA)
    b += text(240, 135, "cadena codificante", 15, weight=900, fill="#5b8fc7") + text(240, 216, "cadena molde (se lee 3'→5')", 15, weight=900, fill=VIEJA)
    # promotor y terminador
    b += f'<rect x="80" y="142" width="140" height="56" rx="8" fill="#fff4df" fill-opacity="0.6" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b += text(150, 260, "promotor", 16, weight=900, fill=ACC) + text(150, 280, "(se une la ARN pol)", 13, weight=800, fill=ACC)
    b += f'<rect x="880" y="142" width="140" height="56" rx="8" fill="#fde8e6" fill-opacity="0.6" stroke="{ROJO}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b += text(950, 260, "terminador", 16, weight=900, fill=ROJO) + text(950, 280, "(señal de fin)", 13, weight=800, fill=ROJO)
    # ARN polimerasa
    b += f'<ellipse cx="560" cy="170" rx="130" ry="95" fill="#e5f4ec" fill-opacity="0.55" stroke="{VERDE}" stroke-width="3"/>'
    b += text(560, 60, "ARN polimerasa", 16, weight=900, fill=VERDE)
    # ARN naciente: emparejado con el molde (5'→3' hacia la derecha) y sale por arriba-izquierda
    b += hebra([(380, 300), (470, 250), (480, 212), (620, 212)], ARN, 6, True)
    b += text(370, 318, "5'", 15, "middle", 900, fill=ARN) + text(645, 216, "3'", 15, "start", 900, fill=ARN)
    b += text(330, 345, "ARN naciente (5'→3')", 16, weight=900, fill=ARN)
    b += flecha(700, 300, 820, 300, INK, 3) + text(760, 290, "avance", 14, weight=900, fill=GRIS)
    # secuencias
    y = 400
    b += f'<rect x="200" y="{y - 30}" width="700" height="140" rx="14" fill="#f6f9fb" stroke="#d5dde3"/>'
    filas = [("codificante", "5'-A T G G C C A A A-3'", "#5b8fc7"), ("molde", "3'-T A C C G G T T T-5'", VIEJA), ("ARNm", "5'-A U G G C C A A A-3'", ARN)]
    for i, (n, s, c) in enumerate(filas):
        b += text(350, y + i * 36, n, 16, "end", 900, fill=c) + text(380, y + i * 36, s, 20, "start", 900, fill=c, style='font-family="Consolas, monospace"')
    b += text(550, y + 120, "El ARNm = cadena codificante con U en lugar de T", 14, weight=900, fill=GRIS)
    save("transcripcion.svg", svg(1100, 540, b, "Transcripción: promotor, ARN polimerasa, cadena molde y cadena codificante"))


def maduracion():
    def tramo(x, w, y, t, col, fondo, tc="#fff"):
        return f'<rect x="{x}" y="{y}" width="{w}" height="36" rx="5" fill="{fondo}" stroke="{col}" stroke-width="2"/>' + text(x + w / 2, y + 24, t, 14, weight=900, fill=tc)
    b = f'<rect x="20" y="20" width="760" height="470" rx="40" fill="#eef4fa" stroke="{PRI}" stroke-width="4" stroke-dasharray="26 6"/>'
    b += text(60, 54, "NÚCLEO", 16, "start", 900, fill=PRI) + text(890, 54, "CITOPLASMA", 16, "middle", 900, fill=VERDE)
    # gen
    y = 80
    b += text(60, y + 24, "ADN", 16, "start", 900, fill=VIEJA)
    b += tramo(120, 90, y, "promotor", ACC, "#fff4df", ACC)
    x = 214
    seg = [("E1", 90), ("I1", 70), ("E2", 90), ("I2", 70), ("E3", 90)]
    for t, w in seg:
        b += tramo(x, w, y, t, VIEJA if t[0] == "E" else "#9aa7b2", VIEJA if t[0] == "E" else "#e9edf0", "#fff" if t[0] == "E" else GRIS)
        x += w + 2
    b += flecha(400, 125, 400, 168) + text(412, 152, "transcripción", 14, "start", 900, fill=PRI)
    # transcrito primario
    y = 180
    b += text(60, y + 24, "pre-ARNm", 15, "start", 900, fill=ARN)
    x = 214
    for t, w in seg:
        b += tramo(x, w, y, t, ARN if t[0] == "E" else "#9aa7b2", ARN if t[0] == "E" else "#e9edf0", "#fff" if t[0] == "E" else GRIS)
        x += w + 2
    b += text(60, y + 44, "(transcrito primario)", 12, "start", 800, fill=GRIS)
    b += flecha(400, 225, 400, 268) + text(412, 252, "maduración (sin detallar)", 14, "start", 900, fill=PRI)
    # caperuza, cola, intrones fuera
    y = 290
    b += f'<circle cx="196" cy="{y + 18}" r="16" fill="#ffe08a" stroke="{ACC}" stroke-width="2.5"/>' + text(196, y + 23, "cap", 11, weight=900, fill="#8a5a00")
    x = 214
    for t, w in seg:
        if t[0] == "E":
            b += tramo(x, w, y, t, ARN, ARN)
            x += w + 2
    b += text(x + 6, y + 24, "AAAA…", 16, "start", 900, fill=ACC)
    b += text(196, y + 62, "caperuza 5'", 13, weight=900, fill=ACC) + text(x + 40, y + 62, "cola poli-A 3'", 13, weight=900, fill=ACC)
    b += text(690, y - 54, "intrones eliminados", 13, weight=900, fill=GRIS) + text(690, y - 38, "(corte y empalme)", 13, weight=900, fill=GRIS)
    for k, xi in enumerate((620, 700)):
        b += f'<path d="M{xi},{y - 22} q15,-18 30,0 q15,18 30,0" fill="none" stroke="#9aa7b2" stroke-width="5"/>'
    b += text(400, 400, "ARNm maduro", 17, weight=900, fill=ARN)
    # poro y salida
    b += f'<rect x="768" y="300" width="24" height="70" fill="#fff" stroke="{PRI}" stroke-width="2"/>' + text(756, 392, "poro nuclear", 13, "end", 900, fill=PRI)
    b += flecha(600, 335, 850, 335, ARN, 4)
    b += f'<ellipse cx="900" cy="300" rx="44" ry="28" fill="#d6e9d4" stroke="{VERDE}" stroke-width="2.5"/><ellipse cx="900" cy="350" rx="36" ry="20" fill="#e9f3e8" stroke="{VERDE}" stroke-width="2.5"/>'
    b += text(900, 410, "ribosoma:", 14, weight=900, fill=VERDE) + text(900, 430, "traducción", 14, weight=900, fill=VERDE)
    save("maduracion-arnm.svg", svg(1000, 510, b, "Transcripción y maduración del ARNm en eucariotas"))


# ---------------------------------------------------------------- traducción
def traduccion():
    COD = ["AUG", "GCU", "UUC", "UAA", "…"]
    ANTI = {"AUG": "UAC", "GCU": "CGA", "UUC": "AAG"}
    AA = {"AUG": ("Met", "#e76f51"), "GCU": ("Ala", "#2a9d8f"), "UUC": ("Phe", "#e9c46a")}
    W = 66  # ancho de codón

    def arnt(cx, y, cod, cadena):
        s = f'<path d="M{cx - 24},{y - 8} V{y - 66} H{cx + 24} V{y - 8}z" fill="#fde2c4" stroke="{ACC}" stroke-width="2.2"/>'
        s += text(cx, y - 15, ANTI[cod], 13, weight=900, fill="#8a5a00", style='font-family="Consolas, monospace"')
        for k, a in enumerate(cadena):
            n, c = AA[a]
            s += f'<circle cx="{cx}" cy="{y - 80 - k * 27}" r="13" fill="{c}" stroke="{INK}" stroke-width="1.5"/>' + text(cx, y - 76 - k * 27, n, 10, weight=900, fill=INK)
        return s

    notas = [["La subunidad menor se une al ARNm", "y localiza el codón AUG.", "ARNt-Met (anticodón UAC) en el sitio P;", "después se une la subunidad mayor."],
             ["Entra un ARNt-aa en el sitio A.", "Enlace peptídico (peptidil transferasa).", "Translocación: el ribosoma avanza un", "codón; el ARNt libre sale por el sitio E."],
             ["Un codón de parada (UAA, UAG, UGA)", "llega al sitio A: entra un factor de", "liberación (FL), se libera el polipéptido", "y se separan las subunidades."]]
    b = ""
    for p, (tit, pos) in enumerate([("1 · Iniciación", 0), ("2 · Elongación", 1), ("3 · Terminación", 2)]):
        ox = 20 + p * 400
        cx, y = ox + 190, 250
        b += f'<rect x="{ox}" y="10" width="380" height="400" rx="18" fill="{"#f6f9fb" if p % 2 == 0 else "#fff"}" stroke="#d5dde3"/>'
        b += text(cx, 38, tit, 19, weight=900, fill=PRI)
        b += f'<clipPath id="c{p}"><rect x="{ox + 2}" y="10" width="376" height="400"/></clipPath><g clip-path="url(#c{p})">'
        # subunidades (detrás)
        b += f'<rect x="{cx - 1.5 * W - 12}" y="{y - 172}" width="{3 * W + 24}" height="166" rx="56" fill="#d6e9d4" fill-opacity="0.8" stroke="{VERDE}" stroke-width="2.5"/>'
        b += f'<ellipse cx="{cx}" cy="{y + 24}" rx="{1.7 * W}" ry="30" fill="#e9f3e8" stroke="{VERDE}" stroke-width="2.5"/>'
        for k, n in enumerate("EPA"):
            b += text(cx + (k - 1) * W, y - 180, n, 16, weight=900, fill=VERDE)
        # ARNm
        x0 = cx - (pos + 0.5) * W  # inicio del codón 0
        b += linea(ox + 30, y, x0 + 5 * W + 40, y, ARN, 5) + text(ox + 12, y - 8, "5'", 13, "start", 900, fill=ARN)
        for i, c in enumerate(COD):
            b += text(x0 + i * W + W / 2, y + 22, c, 15, weight=900, fill=ARN, style='font-family="Consolas, monospace"')
        if pos == 0:
            b += arnt(cx, y, "AUG", ["AUG"])
        elif pos == 1:
            b += arnt(cx - W, y - 30, "AUG", [])
            b += arnt(cx, y, "GCU", ["GCU", "AUG"])
            b += arnt(cx + W, y, "UUC", ["UUC"])
            b += linea(cx + 13, y - 80, cx + W - 13, y - 80, ROJO, 2.5, 'stroke-dasharray="4 3"')
            b += text(cx + W, y - 120, "enlace", 11, weight=900, fill=ROJO) + text(cx + W, y - 107, "peptídico", 11, weight=900, fill=ROJO)
        else:
            b += arnt(cx, y, "UUC", ["UUC", "GCU", "AUG"])
            b += f'<path d="M{cx + W - 22},{y - 8} h44 v-44 l-22,-20 l-22,20z" fill="#f6d6e0" stroke="{ROJO}" stroke-width="2.2"/>' + text(cx + W, y - 32, "FL", 13, weight=900, fill=ROJO)
        b += "</g>"
        for k, t in enumerate(notas[p]):
            b += text(cx, 330 + k * 19, t, 13, weight=800, fill=GRIS)
    b += text(620, 438, "Codones: AUG (Met) · GCU (Ala) · UUC (Phe) · UAA (parada). Los anticodones se leen 3'→5'.", 14, weight=900, fill=PRI)
    save("traduccion.svg", svg(1240, 455, b, "Etapas de la traducción: iniciación, elongación y terminación"))


def polisoma():
    b = linea(40, 220, 1000, 220, ARN, 5) + text(32, 225, "5'", 15, "end", 900, fill=ARN) + text(1008, 225, "3'", 15, "start", 900, fill=ARN)
    for i, x in enumerate((180, 400, 620, 840)):
        b += f'<ellipse cx="{x}" cy="196" rx="54" ry="34" fill="#d6e9d4" stroke="{VERDE}" stroke-width="2.5"/><ellipse cx="{x}" cy="240" rx="44" ry="18" fill="#e9f3e8" stroke="{VERDE}" stroke-width="2.5"/>'
        n = 2 + i * 2
        pts = [(x, 162)]
        for k in range(n):
            pts.append((x + 6 * math.sin(k * 1.3), 162 - 17 * (k + 1)))
        for k, (px, py) in enumerate(pts[1:]):
            b += f'<circle cx="{px:.1f}" cy="{py:.1f}" r="8" fill="{["#e76f51", "#2a9d8f", "#e9c46a", "#8ab17d"][k % 4]}" stroke="{INK}" stroke-width="1"/>'
    b += flecha(300, 290, 700, 290, INK, 3) + text(500, 315, "sentido de lectura del ARNm (5'→3')", 15, weight=900, fill=GRIS)
    b += text(520, 350, "Polirribosoma: varios ribosomas traducen el mismo ARNm a la vez; la cadena más larga es la del ribosoma más avanzado.", 14, weight=800, fill=PRI)
    save("polisoma.svg", svg(1040, 370, b, "Polirribosoma o polisoma"))


# ---------------------------------------------------------------- código genético
def codigo():
    tabla = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"  # código estándar (NCBI tabla 1), orden U C A G
    tres = {"F": "Phe", "L": "Leu", "S": "Ser", "Y": "Tyr", "*": "STOP", "C": "Cys", "W": "Trp", "P": "Pro", "H": "His", "Q": "Gln",
            "R": "Arg", "I": "Ile", "M": "Met", "T": "Thr", "N": "Asn", "K": "Lys", "V": "Val", "A": "Ala", "D": "Asp", "E": "Glu", "G": "Gly"}
    B = "UCAG"
    cw, ch, x0, y0 = 220, 30, 90, 90
    b = text(x0 + 2 * cw, 30, "Segunda base", 18, weight=900, fill=PRI)
    b += text(30, y0 + 8 * ch, "Primera base (5')", 18, weight=900, fill=PRI, style=f'transform="rotate(-90 30 {y0 + 8 * ch})"')
    b += text(x0 + 4 * cw + 50, y0 + 8 * ch, "Tercera base (3')", 18, weight=900, fill=PRI, style=f'transform="rotate(90 {x0 + 4 * cw + 50} {y0 + 8 * ch})"')
    for j, s2 in enumerate(B):
        b += text(x0 + j * cw + cw / 2, 70, s2, 22, weight=900, fill=PRI)
    for i, s1 in enumerate(B):
        b += text(x0 - 28, y0 + i * 4 * ch + 2 * ch + 8, s1, 22, weight=900, fill=PRI)
        for j, s2 in enumerate(B):
            b += f'<rect x="{x0 + j * cw}" y="{y0 + i * 4 * ch}" width="{cw}" height="{4 * ch}" fill="{"#f6f9fb" if (i + j) % 2 == 0 else "#fff"}" stroke="#c3ccd4"/>'
            for k, s3 in enumerate(B):
                aa = tabla[i * 16 + j * 4 + k]
                y = y0 + i * 4 * ch + k * ch + 21
                col = ROJO if aa == "*" else (VERDE if aa == "M" else INK)
                b += text(x0 + j * cw + 18, y, s1 + s2 + s3, 15, "start", 900, fill=col, style='font-family="Consolas, monospace"')
                b += text(x0 + j * cw + 90, y, tres[aa] + (" (inicio)" if aa == "M" else ""), 15, "start", 800, fill=col)
            if j == 3:
                for k, s3 in enumerate(B):
                    b += text(x0 + 4 * cw + 18, y0 + i * 4 * ch + k * ch + 21, s3, 15, weight=900, fill=GRIS)
    b += text(x0 + 2 * cw, y0 + 16 * ch + 32, "61 codones con sentido + 3 de parada (UAA, UAG, UGA) · AUG = metionina y señal de inicio", 15, weight=900, fill=PRI)
    save("codigo-genetico.svg", svg(x0 + 4 * cw + 80, y0 + 16 * ch + 50, b, "Tabla del código genético estándar"))


# ---------------------------------------------------------------- Tm
def tm():
    x0, y0, w, h = 90, 40, 620, 300
    b = linea(x0, y0 + h, x0 + w, y0 + h, INK, 2.5) + linea(x0, y0 + h, x0, y0, INK, 2.5)
    b += text(x0 + w / 2, y0 + h + 40, "Temperatura →", 16, weight=900, fill=GRIS)
    b += text(36, y0 + h / 2, "ADN desnaturalizado (%)", 16, weight=900, fill=GRIS, style=f'transform="rotate(-90 36 {y0 + h / 2})"')
    b += text(x0 - 10, y0 + 5, "100", 13, "end", 800, fill=GRIS) + text(x0 - 10, y0 + h / 2 + 5, "50", 13, "end", 800, fill=GRIS) + text(x0 - 10, y0 + h + 5, "0", 13, "end", 800, fill=GRIS)
    for tmx, col, et in ((0.38, "#e76f51", "más pares A=T"), (0.66, VIEJA, "más pares G≡C")):
        pts = []
        for k in range(101):
            t = k / 100
            f = 1 / (1 + math.exp(-(t - tmx) * 28))
            pts.append(f"{x0 + t * w:.1f},{y0 + h - f * h:.1f}")
        b += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="4"/>'
        xm = x0 + tmx * w
        b += linea(xm, y0 + h, xm, y0 + h / 2, col, 1.5, 'stroke-dasharray="5 4"') + text(xm, y0 + h + 20, "Tm", 14, weight=900, fill=col)
        b += text(xm - 14 if tmx < 0.5 else xm + 12, y0 + h / 2 - 12 if tmx < 0.5 else y0 + h / 2 + 30, et, 15, "start" if tmx > 0.5 else "end", 900, fill=col)
    b += linea(x0, y0 + h / 2, x0 + w, y0 + h / 2, "#c3ccd4", 1.2, 'stroke-dasharray="3 3"')
    b += text(x0 + w / 2, 22, "Tm: temperatura a la que se separa la mitad del ADN", 15, weight=900, fill=PRI)
    save("temperatura-fusion.svg", svg(740, 400, b, "Curvas de desnaturalización del ADN según su contenido en G-C"))


if __name__ == "__main__":
    dogma(); genoma(); genes(); meselson(); horquilla(); burbuja(); origenes()
    transcripcion(); maduracion(); traduccion(); polisoma(); codigo(); tm()
