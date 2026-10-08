# Esquemas SVG del tema A3 (lípidos) de BioCelia.
# Uso: python tools/esquemas_tema_a3.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, P, d, INK, BLUE

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "a3")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO, VERDE = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"
COLA = "#b8862d"


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)


def save(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def linea(a, b, w=2.6, col=INK, extra=""):
    return f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-width="{w}" stroke-linecap="round" {extra}/>'


def zigzag(x, y, n, paso=20, alto=12, ang=0.0, col=INK, w=2.6):
    """Cadena en zigzag de n enlaces desde (x, y) en la dirección ang (grados). Devuelve (svg, puntos)."""
    ux, uy = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    nx, ny = -uy, ux
    pts = []
    for i in range(n + 1):
        off = alto / 2 if i % 2 else -alto / 2
        pts.append((x + ux * paso * i + nx * off, y + uy * paso * i + ny * off))
    s = "".join(linea(a, b, w, col) for a, b in zip(pts, pts[1:]))
    return s, pts


def doble(a, b, lado=1, col=INK, w=2.2, k=5):
    """Segunda línea de un doble enlace, paralela y hacia dentro."""
    vx, vy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(vx, vy)
    nx, ny = -vy / n * lado * k, vx / n * lado * k
    return linea((a[0] + nx + vx * 0.15, a[1] + ny + vy * 0.15), (b[0] + nx - vx * 0.15, b[1] + ny - vy * 0.15), w, col)


# ─── 1 · Ácidos grasos y punto de fusión ──────────────────────────────────
def acidos_grasos():
    b = ""
    s, pts = zigzag(60, 80, 16, 21, 12)
    b += s + text(pts[-1][0] + 8, pts[-1][1] + 6, "COOH", 18, "start", 900, fill=ROJO)
    b += f'<rect x="{pts[-1][0] + 2}" y="{pts[-1][1] - 18}" width="66" height="32" rx="8" fill="none" stroke="{BLUE}" stroke-width="2" stroke-dasharray="5 4"/>'
    b += text(pts[-1][0] + 35, pts[-1][1] - 26, "cabeza polar", 12, weight=900, fill=BLUE)
    b += text(200, 108, "cola apolar (hidrófoba)", 12, weight=900, fill=COLA)
    b += text(30, 30, "Saturado · ácido esteárico (18 C)", 17, "start", 900, fill=PRI)
    b += text(30, 140, "solo enlaces simples → cadena recta · punto de fusión 69,6 °C (sólido)", 14, "start", 700, fill=GRIS)
    s1, p1 = zigzag(60, 210, 8, 21, 12)
    ini = p1[-1]
    s2, p2 = zigzag(ini[0], ini[1], 8, 21, 12, ang=30)
    b += s1 + s2 + doble(p1[-1], p2[1], 1, ROJO, 2.4) + linea(p1[-1], p2[1], 2.6, ROJO)
    b += text(p2[-1][0] + 8, p2[-1][1] + 6, "COOH", 18, "start", 900, fill=ROJO)
    b += text(ini[0] - 20, ini[1] + 44, "doble enlace (cis) → «codo»", 14, "middle", 800, fill=ROJO)
    b += text(30, 180, "Insaturado · ácido oleico (18 C)", 17, "start", 900, fill=PRI)
    b += text(30, 330, "un doble enlace → cadena doblada · punto de fusión 13,4 °C (líquido)", 14, "start", 700, fill=GRIS)
    save("acidos-grasos.svg", svg(620, 345, b, "Ácido esteárico saturado y recto y ácido oleico insaturado con un codo"))


def empaquetamiento():
    b = text(165, 26, "Saturados: se empaquetan", 16, weight=900, fill=PRI) + text(165, 46, "muchas interacciones → sólidos", 13, weight=700, fill=GRIS)
    for i in range(6):
        x = 70 + i * 38
        b += f'<circle cx="{x}" cy="80" r="11" fill="{BLUE}"/>'
        s, _ = zigzag(x, 92, 7, 17, 8, ang=90, col=COLA, w=3)
        b += s
    b += text(495, 26, "Insaturados: los codos los separan", 16, weight=900, fill=PRI) + text(495, 46, "menos interacciones → líquidos", 13, weight=700, fill=GRIS)
    for i in range(5):
        x = 390 + i * 52
        b += f'<circle cx="{x}" cy="80" r="11" fill="{BLUE}"/>'
        s1, p = zigzag(x, 92, 4, 17, 8, ang=90, col=COLA, w=3)
        s2, _ = zigzag(p[-1][0], p[-1][1], 3, 17, 8, ang=90 + (30 if i % 2 else -30), col=COLA, w=3)
        b += s1 + s2
    b += f'<line x1="330" y1="30" x2="330" y2="230" stroke="#dde5ec" stroke-width="2"/>'
    b += text(330, 250, "Más larga la cadena → más interacciones → punto de fusión más alto. Más dobles enlaces → más bajo.", 13, weight=800)
    save("acidos-grasos-empaquetamiento.svg", svg(660, 262, b, "Los ácidos grasos saturados se empaquetan y son sólidos; los insaturados, con codos, son líquidos"))


# ─── 2 · Esterificación y saponificación ────────────────────────────────────
def cadena_ag(x, y, n=6, col=COLA):
    s, pts = zigzag(x, y, n, 16, 9, col=col, w=2.6)
    return s, pts


def esterificacion():
    b = ""
    # glicerina
    for i, yy in enumerate((70, 130, 190)):
        b += text(70, yy + 6, "CH₂" if i != 1 else "CH", 17, "end", 900)
        b += text(76, yy + 6, "–OH", 17, "start", 900, fill=ROJO)
        if i < 2:
            b += linea((55, yy + 12), (55, yy + 46), 2.4)
    b += text(70, 240, "glicerina", 15, weight=900, fill=PRI)
    b += text(160, 136, "+", 30, weight=900)
    # tres ácidos grasos
    for yy in (70, 130, 190):
        b += text(195, yy + 6, "HO–CO", 17, "start", 900, fill=ROJO)
        s, _ = cadena_ag(258, yy, 6)
        b += s
    b += text(300, 240, "3 ácidos grasos", 15, weight=900, fill=PRI)
    b += f'<line x1="380" y1="118" x2="460" y2="118" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    b += f'<line x1="460" y1="146" x2="380" y2="146" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    b += text(420, 106, "esterificación", 13, weight=900, fill=PRI) + text(420, 168, "hidrólisis", 13, weight=900, fill=TEAL)
    b += text(420, 186, "(saponificación con NaOH/KOH)", 11, weight=800, fill=TEAL)
    # triacilglicérido
    for i, yy in enumerate((70, 130, 190)):
        b += text(540, yy + 6, "CH₂" if i != 1 else "CH", 17, "end", 900)
        b += f'<rect x="545" y="{yy - 14}" width="58" height="28" rx="7" fill="#fff4df" stroke="{ACC}" stroke-width="2"/>'
        b += text(548, yy + 6, "–O–CO", 17, "start", 900, fill=ROJO)
        s, _ = cadena_ag(612, yy, 6)
        b += s
        if i < 2:
            b += linea((525, yy + 12), (525, yy + 46), 2.4)
    b += text(640, 240, "triacilglicérido", 15, weight=900, fill=PRI)
    b += text(780, 136, "+ 3 H₂O", 20, "start", 900, fill=BLUE)
    b += text(574, 30, "enlaces éster", 14, weight=900, fill=ACC)
    save("esterificacion-triacilglicerido.svg", svg(880, 255, b, "Esterificación: glicerina y tres ácidos grasos forman un triacilglicérido y tres moléculas de agua"))


def jabon():
    b = '<rect x="0" y="0" width="660" height="260" fill="#eaf4fb"/>'
    # gota de grasa con jabones alrededor
    cx, cy = 200, 135
    b += f'<circle cx="{cx}" cy="{cy}" r="62" fill="#f3d27a" stroke="#c9a227" stroke-width="2"/>'
    b += text(cx, cy + 5, "grasa", 15, weight=900, fill="#7a5c00")
    for k in range(18):
        ang = k * 20
        cab = P((cx, cy), d(ang), 100)
        fin = P((cx, cy), d(ang), 50)
        b += linea(cab, fin, 3, COLA)
        b += f'<circle cx="{cab[0]:.1f}" cy="{cab[1]:.1f}" r="9" fill="{BLUE}"/>'
    b += text(200, 252, "Micela de jabón: las colas atrapan la grasa", 14, weight=800)
    # una molécula de jabón ampliada
    b += f'<circle cx="430" cy="70" r="16" fill="{BLUE}"/>' + text(430, 76, "–COO⁻ Na⁺", 13, "start", 900, fill="#fff") if False else ""
    s, pts = zigzag(380, 80, 8, 18, 10, col=COLA)
    b += s + f'<circle cx="{pts[-1][0] + 14:.1f}" cy="{pts[-1][1]:.1f}" r="14" fill="{BLUE}"/>'
    b += text(pts[-1][0] + 32, pts[-1][1] + 5, "COO⁻ Na⁺", 15, "start", 900, fill=BLUE)
    b += text(470, 40, "Jabón = sal de ácido graso", 16, weight=900, fill=PRI)
    b += text(470, 118, "cola apolar: se une a la grasa", 13, weight=800, fill="#8a6d00")
    b += text(560, 150, "cabeza iónica: se une al agua", 13, weight=800, fill=BLUE)
    b += text(480, 200, "Al aclarar, el agua arrastra", 14, weight=800) + text(480, 220, "las micelas con la grasa.", 14, weight=800)
    save("jabon-micela.svg", svg(660, 262, b, "Las moléculas de jabón rodean una gota de grasa formando una micela que el agua arrastra"))


# ─── 3 · Lípidos saponificables en bloques ─────────────────────────────────
def bloque(x, y, w, h, t, col, fondo, tc=None, size=14):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fondo}" stroke="{col}" stroke-width="2"/>'
    return s + text(x + w / 2, y + h / 2 + size * 0.35, t, size, weight=900, fill=tc or col)


def cola(x, y, n=7):
    s, _ = zigzag(x, y, n, 16, 8, col=COLA, w=3)
    return s


def saponificables():
    GL, AG, FO, AL = ("#e7f0f8", PRI), ("#fdf3e0", COLA), ("#fbe3df", ROJO), ("#efe6fb", LILA)
    b = ""
    cols = [(20, "Triacilglicérido (grasa)", "reserva energética"), (290, "Cera", "protección, impermeabilización"),
            (560, "Fosfoglicérido (fosfolípido)", "membranas"), (830, "Esfingolípido", "membranas (mielina, reconocimiento)")]
    for x, t, f in cols:
        b += text(x + 125, 30, t, 16, weight=900, fill=PRI) + text(x + 125, 262, f, 13, weight=800, fill=GRIS)
    # TAG
    b += bloque(20, 50, 60, 170, "Glicerina", PRI, GL[0], size=12)
    for yy in (65, 120, 175):
        b += bloque(80, yy, 50, 30, "éster", ACC, "#fff4df", size=11) + cola(132, yy + 15, 6)
    # cera: alcohol de cadena larga – éster – ácido graso
    sa, _ = zigzag(292, 130, 5, 16, 8, col="#7b8a97", w=3)
    b += sa + bloque(374, 115, 46, 30, "éster", ACC, "#fff4df", size=11) + cola(422, 130, 6)
    b += text(332, 104, "alcohol de", 11, weight=800, fill=GRIS) + text(332, 117, "cadena larga", 11, weight=800, fill=GRIS)
    b += text(470, 110, "ácido graso", 11, weight=800, fill=COLA)
    b += text(415, 180, "las dos partes son apolares:", 11, weight=800, fill=GRIS) + text(415, 194, "muy hidrófobas", 11, weight=800, fill=GRIS)
    # fosfoglicérido
    b += bloque(560, 50, 60, 170, "Glicerina", PRI, GL[0], size=12)
    for yy in (65, 120):
        b += bloque(620, yy, 50, 30, "éster", ACC, "#fff4df", size=11) + cola(672, yy + 15, 6)
    b += bloque(620, 175, 52, 30, "P", ROJO, FO[0], size=14) + bloque(674, 175, 110, 30, "aminoalcohol", LILA, AL[0], size=12)
    b += text(700, 240, "cabeza polar: fosfato + aminoalcohol", 11, weight=800, fill=ROJO)
    # esfingolípido
    b += bloque(830, 50, 70, 170, "Esfingosina", PRI, GL[0], size=11)
    b += bloque(900, 80, 50, 30, "amida", ACC, "#fff4df", size=11) + cola(952, 95, 6)
    b += bloque(900, 160, 150, 30, "grupo polar", LILA, AL[0], size=12)
    b += text(975, 210, "fosfocolina → esfingomielina", 11, weight=800, fill=LILA) + text(975, 226, "glúcido → glucoesfingolípido", 11, weight=800, fill=LILA)
    b += text(882, 46, "ceramida = esfingosina + ácido graso", 11, "start", 800, fill=GRIS) if False else ""
    save("lipidos-saponificables.svg", svg(1080, 275, b, "Composición de los lípidos saponificables: triacilglicérido, cera, fosfoglicérido y esfingolípido"))


# ─── 4 · Fosfolípido detallado ─────────────────────────────────────────────
def fosfolipido():
    b = ""
    b += f'<rect x="20" y="20" width="230" height="250" rx="14" fill="#e7f0f8" stroke="{BLUE}" stroke-width="2" stroke-dasharray="6 5"/>'
    b += text(135, 305, "cabeza polar (hidrófila)", 14, weight=900, fill=BLUE)
    b += text(470, 305, "colas apolares (hidrófobas)", 14, weight=900, fill=COLA)
    # aminoalcohol (colina) – fosfato – glicerina
    b += bloque(40, 40, 120, 40, "colina (N⁺)", LILA, "#efe6fb", size=13)
    b += linea((100, 80), (100, 110))
    b += bloque(60, 110, 80, 40, "fosfato⁻", ROJO, "#fbe3df", size=13)
    b += linea((140, 130), (190, 130))
    b += bloque(190, 60, 50, 190, "", PRI, "#cfe0f2", size=12)
    b += f'<text x="215" y="155" font-size="14" font-weight="900" fill="{PRI}" text-anchor="middle" transform="rotate(-90 215 155)" font-family="Nunito, Segoe UI, sans-serif">glicerina</text>'
    for yy, ins in ((95, False), (205, True)):
        b += bloque(240, yy - 15, 56, 30, "éster", ACC, "#fff4df", size=11)
        if ins:
            s1, p1 = zigzag(298, yy, 7, 18, 10, col=COLA, w=3)
            s2, p2 = zigzag(p1[-1][0], p1[-1][1], 8, 18, 10, ang=26, col=COLA, w=3)
            b += s1 + s2 + doble(p1[-2], p1[-1], 1, ROJO) + linea(p1[-2], p1[-1], 3, ROJO)
            b += text(p1[-1][0], p1[-1][1] - 18, "doble enlace", 12, weight=800, fill=ROJO)
            b += text(610, 236, "ácido graso insaturado", 12, weight=800, fill=GRIS)
        else:
            s, _ = zigzag(298, yy, 15, 18, 10, col=COLA, w=3)
            b += s + text(560, 70, "ácido graso saturado", 12, weight=800, fill=GRIS)
    save("fosfolipido.svg", svg(690, 320, b, "Estructura de un fosfolípido: cabeza polar con colina, fosfato y glicerina, y dos colas de ácidos grasos"))


# ─── 5 · Terpenos ─────────────────────────────────────────────────────────
def terpenos():
    b = text(115, 28, "Isopreno (5 C)", 17, weight=900, fill=PRI)
    pts = [(40, 125), (80, 102), (120, 125), (160, 102)]
    b += "".join(linea(a, c) for a, c in zip(pts, pts[1:]))
    b += doble(pts[0], pts[1], 1) + doble(pts[2], pts[3], 1)
    b += linea(pts[1], (80, 70))
    b += text(80, 62, "CH₃", 13, weight=800)
    b += text(115, 160, "unidad de los terpenos", 13, weight=800, fill=GRIS)
    # β-caroteno simplificado
    x0, y0 = 300, 110

    def hexa(cx, cy, r=26):
        v = [(cx + r * math.cos(math.radians(60 * k + 30)), cy + r * math.sin(math.radians(60 * k + 30))) for k in range(6)]
        return "".join(linea(v[i], v[(i + 1) % 6]) for i in range(6)), v
    h1, v1 = hexa(x0, y0)
    b += h1
    # anillo β-ionona: C6 = v1[5] (une la cadena), C5 = v1[0], C1 = v1[4]
    c6 = v1[5]
    s, cad = zigzag(c6[0], c6[1] + 7, 19, 22, 14)  # cad[0] = C6, cad[1] = C7 … cad[19] = C6'
    b += s

    def metilo(p, arriba):
        return linea(p, (p[0], p[1] - 22 if arriba else p[1] + 22), 2.2)
    # 9 dobles enlaces conjugados en la cadena: C7=C8, C9=C10, C11=C12, C13=C14, C15=C15' y simétricos
    for i in range(1, 19, 2):
        b += doble(cad[i], cad[i + 1], 1 if cad[i][1] > cad[i + 1][1] else -1, ROJO, 2.2, 4)
    for i in (3, 7, 12, 16):  # metilos en C9, C13, C13', C9'
        b += metilo(cad[i], cad[i][1] < cad[i - 1][1])
    r = 26
    c6b = cad[-1]
    h2, v2 = hexa(c6b[0] - r * math.cos(math.radians(210)), c6b[1] - r * math.sin(math.radians(210)))
    b += h2
    # dobles enlaces C5=C6 de cada anillo, metilo en C5 y dos metilos en C1
    for c6x, c5, c1, cen in ((v1[5], v1[0], v1[4], (x0, y0)), (v2[3], v2[2], v2[4], (c6b[0] - r * math.cos(math.radians(210)), c6b[1] - r * math.sin(math.radians(210))))):
        lado = 1 if (c5[0] - c6x[0]) * (cen[1] - c6x[1]) - (c5[1] - c6x[1]) * (cen[0] - c6x[0]) > 0 else -1
        b += doble(c6x, c5, lado, ROJO, 2.2, 4)
        dx, dy = c5[0] - cen[0], c5[1] - cen[1]
        b += linea(c5, (c5[0] + dx * 0.75, c5[1] + dy * 0.75), 2.2)
        b += linea(c1, (c1[0] - 16, c1[1] - 16), 2.2) + linea(c1, (c1[0] + 16, c1[1] - 16), 2.2)
    b += text(560, 28, "β-caroteno (tetraterpeno, 40 C)", 17, weight=900, fill=ACC)
    b += text(560, 168, "muchos dobles enlaces alternos → color (naranja)", 13, weight=800, fill=GRIS)
    b += f'<line x1="560" y1="185" x2="560" y2="208" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
    b += text(560, 230, "se rompe por la mitad → 2 vitamina A", 14, weight=900, fill=PRI)
    save("terpenos-isopreno-caroteno.svg", svg(860, 245, b, "El isopreno es la unidad de los terpenos; el beta-caroteno es un tetraterpeno precursor de la vitamina A"))


# ─── 6 · Esteroides ────────────────────────────────────────────────────────
def anillos(ox, oy, a=34):
    """Núcleo de esterano: anillos A, B, C (hexágonos) y D (pentágono)."""
    def hexv(c):
        return [(c[0] + a * math.cos(math.radians(-90 + 60 * k)), c[1] + a * math.sin(math.radians(-90 + 60 * k))) for k in range(6)]
    A = (ox, oy)
    B = (ox + a * math.sqrt(3), oy)
    C = (B[0] + a * math.sqrt(3) * math.cos(math.radians(-60)), B[1] + a * math.sqrt(3) * math.sin(math.radians(-60)))
    vA, vB, vC = hexv(A), hexv(B), hexv(C)
    # pentágono D sobre la arista derecha de C (vértices a -30° y 30°)
    p1, p2 = vC[1], vC[2]
    m = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
    R = a / (2 * math.sin(math.radians(36)))
    dist = a / (2 * math.tan(math.radians(36)))
    Dc = (m[0] + dist, m[1])
    a1 = math.degrees(math.atan2(p1[1] - Dc[1], p1[0] - Dc[0]))
    vD = [(Dc[0] + R * math.cos(math.radians(a1 + 72 * k)), Dc[1] + R * math.sin(math.radians(a1 + 72 * k))) for k in range(5)]
    s = ""
    for v in (vA, vB, vC):
        s += "".join(linea(v[i], v[(i + 1) % 6]) for i in range(6))
    s += "".join(linea(vD[i], vD[(i + 1) % 5]) for i in range(5))
    centros = {"A": A, "B": B, "C": C, "D": Dc}
    return s, centros, vA, vB, vC, vD


def esteroides():
    b = text(140, 28, "Esterano", 17, weight=900, fill=PRI) + text(140, 48, "(ciclopentanoperhidrofenantreno)", 12, weight=700, fill=GRIS)
    s, cen, *_ = anillos(70, 150, 30)
    b += s
    for k, c in cen.items():
        b += text(c[0], c[1] + 6, k, 16, weight=900, fill=LILA)
    # colesterol
    s, cen, vA, vB, vC, vD = anillos(400, 160, 34)
    b += s + text(470, 28, "Colesterol", 17, weight=900, fill=ACC)
    ho = vA[4]  # vértice inferior izquierdo
    b += linea(ho, (ho[0] - 30, ho[1] + 14))
    b += text(ho[0] - 34, ho[1] + 22, "HO", 16, "end", 900, fill=ROJO)
    b += doble(vB[3], vB[4], -1)  # doble enlace C5=C6
    b += linea(vA[0], (vA[0][0], vA[0][1] - 26)) if False else ""
    for v in (vB[5], vC[1]):  # metilos en C10 y C13
        b += linea(v, (v[0], v[1] - 26))
    # la cadena lateral (C20-C27) sale del C17: vértice superior del anillo D distinto del C13 (vD[0])
    top = min(vD[1:], key=lambda v: v[1])
    cad = [top]  # C17 → C20 → C22 → C23 → C24 → C25 → C26
    for i in range(6):
        p = cad[-1]
        cad.append((p[0] + 22, p[1] + (-12 if i % 2 == 0 else 12)))
    b += "".join(linea(a, c) for a, c in zip(cad, cad[1:]))
    b += linea(cad[1], (cad[1][0], cad[1][1] - 22))  # metilo C21 en el C20
    b += linea(cad[5], (cad[5][0], cad[5][1] - 22))  # metilo C27 en el C25
    b += text(cad[-1][0] - 40, cad[-1][1] + 40, "cadena lateral", 12, weight=800, fill=GRIS)
    b += text(470, 270, "–OH polar pequeño + núcleo apolar: se intercala en la membrana", 13, weight=800, fill=GRIS)
    save("esteroides-colesterol.svg", svg(760, 285, b, "Núcleo de esterano con sus cuatro anillos y fórmula del colesterol"))


# ─── 7 · Clasificación ─────────────────────────────────────────────────────
def clasificacion():
    def caja(x, y, w, t, sub="", col=PRI, fondo="#e7f0f8"):
        s = f'<rect x="{x - w / 2}" y="{y - 24}" width="{w}" height="{48 if sub else 40}" rx="12" fill="{fondo}" stroke="{col}" stroke-width="2"/>'
        s += text(x, y + (0 if sub else 4), t, 15, weight=900, fill=col)
        if sub:
            s += text(x, y + 17, sub, 11.5, weight=700, fill=GRIS)
        return s

    def ln(a, b2):
        return f'<path d="M{a[0]},{a[1]} V{(a[1] + b2[1]) / 2} H{b2[0]} V{b2[1]}" fill="none" stroke="#9aa8b4" stroke-width="2"/>'
    b = ""
    b += ln((520, 50), (290, 120)) + ln((520, 50), (830, 120))
    b += ln((290, 145), (160, 210)) + ln((290, 145), (430, 210))
    b += ln((160, 235), (80, 300)) + ln((160, 235), (210, 300))
    b += ln((430, 235), (360, 300)) + ln((430, 235), (525, 300))
    b += ln((830, 145), (730, 210)) + ln((830, 145), (930, 210))
    b += caja(520, 34, 160, "LÍPIDOS", "", "#fff", PRI)
    b += caja(290, 120, 320, "Saponificables", "con ácidos grasos · forman jabones", PRI)
    b += caja(830, 120, 330, "Insaponificables", "sin ácidos grasos · no forman jabones", ACC, "#fff4df")
    b += caja(160, 214, 180, "Simples", "solo C, H, O", TEAL, "#e3f4f1")
    b += caja(430, 214, 200, "Complejos", "también P, N, S…", TEAL, "#e3f4f1")
    b += caja(80, 304, 140, "Acilglicéridos", "grasas", TEAL, "#e3f4f1")
    b += caja(210, 304, 110, "Ceras", "", TEAL, "#e3f4f1")
    b += caja(360, 304, 150, "Fosfoglicéridos", "fosfolípidos", LILA, "#efe6fb")
    b += caja(525, 304, 160, "Esfingolípidos", "", LILA, "#efe6fb")
    b += caja(730, 214, 180, "Terpenos", "derivan del isopreno", ACC, "#fff4df")
    b += caja(930, 214, 180, "Esteroides", "derivan del esterano", ACC, "#fff4df")
    save("clasificacion-lipidos.svg", svg(1040, 335, b, "Clasificación de los lípidos en saponificables e insaponificables"))


# ─── 8 · Funciones ────────────────────────────────────────────────────────
def funciones():
    b = ""
    items = [("Reserva energética", "triacilglicéridos · 9 kcal/g"), ("Estructural", "fosfolípidos, colesterol"), ("Protectora", "ceras"),
             ("Hormonal", "hormonas esteroideas"), ("Vitamínica", "A, D, E, K"), ("Pigmentos", "carotenos, xantofilas")]
    for i, (t, sub) in enumerate(items):
        cx, cy = 85 + i * 160, 75
        if i == 0:  # adipocito
            b += f'<circle cx="{cx}" cy="{cy}" r="44" fill="#fdf3e0" stroke="{COLA}" stroke-width="2.5"/><circle cx="{cx}" cy="{cy + 4}" r="34" fill="#f3d27a"/><ellipse cx="{cx + 28}" cy="{cy - 26}" rx="9" ry="6" fill="#7a5c00"/>'
        elif i == 1:  # bicapa
            for j in range(5):
                x = cx - 40 + j * 20
                b += f'<circle cx="{x}" cy="{cy - 30}" r="7" fill="{BLUE}"/><circle cx="{x}" cy="{cy + 30}" r="7" fill="{BLUE}"/>'
                b += linea((x, cy - 23), (x, cy - 3), 2.4, COLA) + linea((x, cy + 23), (x, cy + 3), 2.4, COLA)
        elif i == 2:  # hoja con gotas
            b += f'<path d="M{cx - 45},{cy + 25} C{cx - 30},{cy - 40} {cx + 30},{cy - 50} {cx + 45},{cy - 25} C{cx + 30},{cy + 30} {cx - 20},{cy + 40} {cx - 45},{cy + 25}z" fill="#7ccf68" stroke="#3a8a2c" stroke-width="2.5"/>'
            for x, y in ((-10, -5), (12, -18), (-22, 12)):
                b += f'<ellipse cx="{cx + x}" cy="{cy + y}" rx="5" ry="7" fill="#d6ecfa" stroke="{BLUE}" stroke-width="1.5"/>'
        elif i == 3:  # anillos esteroides
            s, *_ = anillos(cx - 34, cy + 10, 18)
            b += s
        elif i == 4:  # cápsula
            b += f'<rect x="{cx - 44}" y="{cy - 18}" width="88" height="36" rx="18" fill="#f7c948" stroke="#b08a1a" stroke-width="2.5"/><line x1="{cx}" y1="{cy - 18}" x2="{cx}" y2="{cy + 18}" stroke="#b08a1a" stroke-width="2"/>'
        else:  # zanahoria
            b += f'<path d="M{cx - 14},{cy - 30} L{cx + 14},{cy - 30} L{cx},{cy + 45}z" fill="#f08a24" stroke="#b5600f" stroke-width="2.5"/>'
            b += f'<path d="M{cx},{cy - 30} l-12,-22 M{cx},{cy - 30} l0,-26 M{cx},{cy - 30} l12,-22" stroke="#3a8a2c" stroke-width="4" fill="none"/>'
        b += text(cx, 150, t, 16, weight=900, fill=PRI) + text(cx, 170, sub, 12, weight=700, fill=GRIS)
    save("lipidos-funciones.svg", svg(960, 185, b, "Funciones de los lípidos: reserva, estructural, protectora, hormonal, vitamínica y pigmentos"))


# ─── 9 · Aterosclerosis ───────────────────────────────────────────────────
def arteria():
    b = ""
    for cx, placa, t, sub in ((150, False, "Arteria sana", "la sangre circula sin obstáculos"), (450, True, "Aterosclerosis", "placa de ateroma: estrecha la luz")):
        b += f'<circle cx="{cx}" cy="110" r="85" fill="#e59a90" stroke="#a33a36" stroke-width="3"/>'
        b += f'<circle cx="{cx}" cy="110" r="62" fill="#f8d7d3"/>'
        if placa:
            b += f'<path d="M{cx - 60},{110 - 15} A62,62 0 0 1 {cx + 45},{110 - 42} Q{cx + 10},{110 - 5} {cx - 60},{110 - 15}z" fill="#f3d27a" stroke="#c9a227" stroke-width="2"/>'
            b += f'<circle cx="{cx + 5}" cy="140" r="34" fill="#c0392b" opacity="0.85"/>'
        else:
            b += f'<circle cx="{cx}" cy="110" r="52" fill="#c0392b" opacity="0.85"/>'
        b += text(cx, 222, t, 16, weight=900, fill=PRI) + text(cx, 242, sub, 13, weight=700, fill=GRIS)
    save("aterosclerosis.svg", svg(600, 255, b, "Corte de una arteria sana y de una arteria con placa de ateroma"))


# ─── 10 · Ceras: molécula y cutícula de una hoja ──────────────────────────
def ceras():
    b = text(200, 30, "Una cera", 18, weight=900, fill=PRI)
    sa, pa = zigzag(30, 110, 9, 17, 9, col="#7b8a97", w=3)
    b += sa + bloque(pa[-1][0] + 2, 95, 52, 30, "éster", ACC, "#fff4df", size=12)
    sb, pb = zigzag(pa[-1][0] + 56, 110, 9, 17, 9, col=COLA, w=3)
    b += sb
    b += text(105, 82, "monoalcohol de cadena larga", 12, weight=800, fill=GRIS)
    b += text(pb[0][0] + 75, 82, "ácido graso de cadena larga", 12, weight=800, fill=COLA)
    b += text(200, 160, "los dos extremos son apolares → muy hidrófoba,", 13, weight=800, fill=INK)
    b += text(200, 178, "sólida a temperatura ambiente", 13, weight=800, fill=INK)
    # hoja con cutícula
    x0 = 430
    b += text(x0 + 180, 30, "Función protectora e impermeabilizante", 16, weight=900, fill=PRI)
    b += f'<rect x="{x0}" y="70" width="360" height="22" rx="4" fill="#f3d27a" stroke="#c9a227" stroke-width="2"/>'
    b += text(x0 + 180, 86, "cutícula de cera", 13, weight=900, fill="#8a6d10")
    for i in range(6):
        b += f'<rect x="{x0 + i * 60}" y="92" width="60" height="70" fill="#cfe8c4" stroke="#3f8a3a" stroke-width="2"/>'
    b += text(x0 + 180, 182, "células de la epidermis de la hoja", 12, weight=800, fill=VERDE)
    for cx in (x0 + 70, x0 + 190, x0 + 300):
        b += f'<path d="M{cx},38 q-13,18 0,26 q13,-8 0,-26z" fill="#9fd0f0" stroke="#2a7fc1" stroke-width="1.5"/>'
    b += text(x0 + 180, 212, "el agua no la atraviesa: evita la pérdida de agua", 13, weight=800, fill=BLUE)
    b += text(400, 262, "También en plumas, pelo y piel de vertebrados, exoesqueleto de insectos y panales de abeja.", 13, weight=700, fill=GRIS)
    save("ceras.svg", svg(820, 280, b, "Una cera es el éster de un ácido graso y un monoalcohol de cadena larga; forma la cutícula impermeable de las hojas"))


# ─── 11 · Esfingolípidos ──────────────────────────────────────────────────
def esfingolipidos():
    b = ""
    tipos = [(30, "Esfingomielina", "fosfocolina", ROJO, "#fbe3df", "vaina de mielina de los axones"),
             (470, "Glucoesfingolípido", "glúcido(s)", VERDE, "#e3f2df", "glucocálix: reconocimiento celular")]
    for x, t, g, col, fondo, fun in tipos:
        b += text(x + 200, 28, t, 17, weight=900, fill=PRI)
        b += bloque(x + 14, 58, 122, 34, g, col, fondo, size=13)
        b += linea((x + 75, 92), (x + 75, 112))
        b += bloque(x + 30, 112, 90, 80, "", PRI, "#cfe0f2")
        b += text(x + 75, 148, "esfingosina", 12, weight=900, fill=PRI)
        b += text(x + 75, 164, "(aminoalcohol)", 10, weight=800, fill=GRIS)
        # cola de la esfingosina
        s1, _ = zigzag(x + 122, 128, 11, 18, 9, col="#7b8a97", w=3)
        b += s1
        # amida + ácido graso
        b += bloque(x + 122, 160, 50, 28, "amida", ACC, "#fff4df", size=11)
        s2, _ = zigzag(x + 174, 174, 9, 18, 9, col=COLA, w=3)
        b += s2 + text(x + 290, 205, "ácido graso", 12, weight=800, fill=COLA)
        b += text(x + 215, 148, "cadena de la esfingosina", 11, "start", 800, fill=GRIS)
        b += f'<rect x="{x + 18}" y="104" width="380" height="104" rx="10" fill="none" stroke="{ACC}" stroke-width="1.5" stroke-dasharray="3 4"/>'
        b += text(x + 330, 224, "ceramida", 12, weight=900, fill=ACC)
        b += text(x + 150, 80, "← cabeza polar", 13, "start", 900, fill=BLUE)
        b += text(x + 200, 256, "Función: " + fun, 14, weight=900, fill=col)
    b += text(450, 290, "Sin glicerina: ceramida (esfingosina + ácido graso por enlace amida) + un grupo polar. Son anfipáticos y forman parte de las membranas.", 13, weight=700, fill=GRIS)
    save("esfingolipidos.svg", svg(900, 305, b, "Esfingolípidos: la ceramida unida a fosfocolina forma la esfingomielina y unida a glúcidos forma los glucoesfingolípidos"))


if __name__ == "__main__":
    for f in (acidos_grasos, empaquetamiento, esterificacion, jabon, saponificables, fosfolipido, terpenos, esteroides, clasificacion, funciones, arteria, ceras, esfingolipidos):
        f()
