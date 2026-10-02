# Esquemas SVG del tema C2 (mitosis y meiosis) de BioCelia.
# Uso: python tools/esquemas_tema_c2.py
# Célula modelo 2n = 4: un par grande y un par pequeño; rojo = origen materno, azul = paterno.
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "c2")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, LILA, ROJO, VERDE = "#0f4c81", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"
MAT, PAT = "#e05a4f", "#3a7bd5"        # cromosomas materno y paterno
HUSO = "#9fb4c7"
MEMB = "#2a7fc1"
L_G, L_P = 54, 32                       # longitud del cromosoma grande y del pequeño


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


# ---------------------------------------------------------------- piezas
def cromatida(x, y, L, col, punta=None, w=9):
    """Cromátida vertical centrada en (x, y); 'punta' = color del extremo inferior recombinado."""
    s = f'<rect x="{x - w / 2:.1f}" y="{y - L / 2:.1f}" width="{w}" height="{L}" rx="{w / 2}" fill="{col}" stroke="{INK}" stroke-width="1"/>'
    if punta:
        s += f'<rect x="{x - w / 2:.1f}" y="{y + L * 0.18:.1f}" width="{w}" height="{L * 0.32:.1f}" rx="{w / 2}" fill="{punta}" stroke="{INK}" stroke-width="1"/>'
    return s


def doble(x, y, L, c1, c2=None, p1=None, p2=None, sep=10):
    """Cromosoma de dos cromátidas (lado a lado) unidas por el centrómero en (x, y)."""
    c2 = c2 or c1
    s = cromatida(x - sep / 2, y, L, c1, p1) + cromatida(x + sep / 2, y, L, c2, p2)
    return s + f'<circle cx="{x}" cy="{y - L * 0.12:.1f}" r="4.5" fill="{INK}"/>'


def simple(x, y, L, col, punta=None):
    return cromatida(x, y, L, col, punta) + f'<circle cx="{x}" cy="{y - L * 0.12:.1f}" r="3.5" fill="{INK}"/>'


def centrosoma(x, y, aster=True):
    s = ""
    if aster:
        for a in range(0, 360, 30):
            s += linea(x + 7 * math.cos(math.radians(a)), y + 7 * math.sin(math.radians(a)), x + 18 * math.cos(math.radians(a)), y + 18 * math.sin(math.radians(a)), HUSO, 1.4)
    return s + f'<rect x="{x - 6}" y="{y - 3}" width="9" height="6" rx="1.5" fill="#5d7ea8"/><rect x="{x}" y="{y - 6}" width="6" height="10" rx="1.5" fill="#5d7ea8"/>'


def huso(px, py, puntos):
    return "".join(linea(px, py, x, y, HUSO, 1.6) for x, y in puntos)


def celula(cx, cy, rx=95, ry=80, fill="#fdf3e7"):
    return f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="{fill}" stroke="{MEMB}" stroke-width="3"/>'


def panel(x, y, w, h, titulo, sub="", col=PRI, fondo="#f6f9fb"):
    s = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fondo}" stroke="#d5dde3"/>'
    s += text(x + w / 2, y + 24, titulo, 15, weight=900, fill=col)
    if sub:
        s += text(x + w / 2, y + h - 12, sub, 11.5, weight=800, fill=GRIS)
    return s


# ---------------------------------------------------------------- cromosoma metafásico
def cromosoma():
    x, y, L = 260, 210, 300
    b = ""
    for dx in (-22, 22):
        b += f'<path d="M{x + dx - 18},{y - L / 2 + 18} Q{x + dx - 18},{y - L / 2} {x + dx},{y - L / 2} Q{x + dx + 18},{y - L / 2} {x + dx + 18},{y - L / 2 + 18} L{x + dx + 10},{y - 30} Q{x + dx},{y - 18} {x + dx + 10},{y - 6} L{x + dx + 18},{y + L / 2 - 18} Q{x + dx + 18},{y + L / 2} {x + dx},{y + L / 2} Q{x + dx - 18},{y + L / 2} {x + dx - 18},{y + L / 2 - 18} L{x + dx - 10},{y - 6} Q{x + dx},{y - 18} {x + dx - 10},{y - 30}z" fill="#e9a6a0" stroke="{ROJO}" stroke-width="2.5"/>'
        for yy in (y - 110, y - 70, y + 40, y + 90):
            b += f'<rect x="{x + dx - 16}" y="{yy}" width="32" height="10" fill="#c76b63" opacity="0.6"/>'
    b += f'<ellipse cx="{x - 10}" cy="{y - 18}" rx="6" ry="14" fill="#2f3b48"/><ellipse cx="{x + 10}" cy="{y - 18}" rx="6" ry="14" fill="#2f3b48"/>'
    for dx in (-22, 22):
        b += f'<rect x="{x + dx - 18}" y="{y - L / 2 - 2}" width="36" height="14" rx="7" fill="#7b3fb0" opacity="0.75"/>'
        b += f'<rect x="{x + dx - 18}" y="{y + L / 2 - 12}" width="36" height="14" rx="7" fill="#7b3fb0" opacity="0.75"/>'
    def et(px, py, tx, ty, s, col=INK):
        return linea(px, py, tx - 6, ty - 5, GRIS, 1.3) + f'<circle cx="{px}" cy="{py}" r="2.5" fill="{GRIS}"/>' + text(tx, ty, s, 16, "start", 900, fill=col)
    b += et(x + 22, y + 60, 420, y + 70, "cromátida") + text(420, y + 90, "(dos, idénticas: cromátidas hermanas)", 13, "start", 800, fill=GRIS)
    b += et(x, y - 18, 420, y - 18, "centrómero (constricción primaria)")
    b += et(x + 14, y - 22, 420, y - 52, "cinetocoro (se une al huso)", LILA)
    b += et(x + 30, y - L / 2 + 4, 420, y - 140, "telómero", LILA)
    b += linea(x - 34, y - 90, 150, y - 105, GRIS, 1.3) + f'<circle cx="{x - 34}" cy="{y - 90}" r="2.5" fill="{GRIS}"/>' + text(144, y - 100, "brazo corto", 16, "end", 900)
    b += linea(x - 34, y + 80, 150, y + 115, GRIS, 1.3) + f'<circle cx="{x - 34}" cy="{y + 80}" r="2.5" fill="{GRIS}"/>' + text(144, y + 120, "brazo largo", 16, "end", 900)
    b += text(260, 400, "Cromosoma metafásico: un cromosoma con dos cromátidas", 15, weight=900, fill=PRI)
    save("cromosoma-metafasico.svg", svg(760, 420, b, "Partes del cromosoma metafásico"))


# ---------------------------------------------------------------- haploide y diploide
def ciclo_vital():
    b = ""
    def cel(cx, cy, r, cromos, fill="#fdf3e7", et=""):
        s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{MEMB}" stroke-width="3"/>'
        n = len(cromos)
        for k, (col, L) in enumerate(cromos):
            s += simple(cx - (n - 1) * 9 + k * 18, cy, L, col)
        if et:
            s += text(cx, cy + r + 22, et, 14, weight=900, fill=PRI)
        return s
    M1, M2, P1, P2 = "#f2a29b", "#c0392b", "#8fb8ee", "#1f4f99"
    b += cel(100, 80, 48, [(M1, L_G * .8), (M2, L_G * .8), (M1, L_P * .8), (M2, L_P * .8)]) + text(100, 30, "madre 2n = 4", 13, weight=900, fill=ROJO)
    b += cel(100, 230, 48, [(P1, L_G * .8), (P2, L_G * .8), (P1, L_P * .8), (P2, L_P * .8)]) + text(100, 300, "padre 2n = 4", 13, weight=900, fill=PRI)
    b += flecha(152, 80, 290, 80) + flecha(152, 230, 290, 230) + text(220, 70, "meiosis", 14, weight=900, fill=ROJO) + text(220, 220, "meiosis", 14, weight=900, fill=ROJO)
    b += cel(330, 80, 38, [(M2, L_G * .8), (M1, L_P * .8)], "#fff4df") + text(330, 136, "óvulo n = 2", 13, weight=900, fill=ACC)
    b += cel(330, 230, 38, [(P1, L_G * .8), (P2, L_P * .8)], "#fff4df") + text(330, 286, "espermatozoide n = 2", 13, weight=900, fill=ACC)
    b += flecha(372, 95, 470, 140) + flecha(372, 215, 470, 165) + text(420, 158, "fecundación", 14, weight=900, fill=VERDE)
    b += cel(540, 150, 60, [(M2, L_G), (P1, L_G), (M1, L_P), (P2, L_P)], et="cigoto 2n = 4")
    b += text(540, 252, "cada par: un homólogo de la", 12, weight=800, fill=GRIS) + text(540, 268, "madre y otro del padre", 12, weight=800, fill=GRIS)
    b += flecha(608, 150, 690, 150) + text(650, 140, "mitosis", 14, weight=900, fill=PRI)
    for k in range(6):
        a = math.radians(k * 60)
        b += f'<circle cx="{750 + 26 * math.cos(a):.1f}" cy="{150 + 26 * math.sin(a):.1f}" r="16" fill="#fdf3e7" stroke="{MEMB}" stroke-width="2"/>'
    b += text(750, 214, "células somáticas 2n", 14, weight=900, fill=PRI) + text(750, 230, "(organismo pluricelular)", 12, weight=800, fill=GRIS)
    b += text(450, 350, "La meiosis reduce a la mitad el número de cromosomas y la fecundación lo restablece: se mantiene constante en la especie.", 13, weight=800, fill=GRIS)
    b += text(450, 370, "Especie humana: 2n = 46 (células somáticas) · n = 23 (gametos)", 14, weight=900, fill=PRI)
    save("haploide-diploide.svg", svg(880, 385, b, "Células diploides, gametos haploides, fecundación y mitosis"))


# ---------------------------------------------------------------- mitosis
def mitosis():
    W, H = 230, 260
    b = ""
    tit = [("Interfase (G2)", "ADN ya duplicado"), ("Profase", "condensación, huso, sin envoltura"), ("Metafase", "cromosomas en la placa ecuatorial"),
           ("Anafase", "se separan las cromátidas"), ("Telofase y citocinesis", "dos núcleos, surco de segmentación")]
    for i, (t, s) in enumerate(tit):
        x0 = 10 + i * (W + 10)
        b += panel(x0, 10, W, H, t, s)
        cx, cy = x0 + W / 2, 140
        if i == 0:
            b += celula(cx, cy)
            b += f'<circle cx="{cx}" cy="{cy}" r="44" fill="#dfe8f5" stroke="#3b5f8f" stroke-width="3"/><circle cx="{cx + 12}" cy="{cy - 10}" r="12" fill="#55606c"/>'
            for k in range(8):
                a = k * 0.8
                b += f'<path d="M{cx - 26 + 14 * math.cos(a):.1f},{cy + 12 + 8 * math.sin(a):.1f} q6,-5 12,0 t12,0" fill="none" stroke="#7d8fa6" stroke-width="2"/>'
            b += centrosoma(cx + 60, cy - 40) + centrosoma(cx + 72, cy - 30, False)
        elif i == 1:
            b += celula(cx, cy)
            b += f'<circle cx="{cx}" cy="{cy}" r="50" fill="none" stroke="#3b5f8f" stroke-width="2.5" stroke-dasharray="10 8"/>'
            b += doble(cx - 22, cy - 6, L_G, MAT) + doble(cx + 10, cy + 10, L_G, PAT) + doble(cx + 30, cy - 18, L_P, MAT) + doble(cx - 4, cy + 30, L_P, PAT)
            b += centrosoma(cx - 70, cy - 30) + centrosoma(cx + 70, cy - 30)
            b += f'<path d="M{cx - 64},{cy - 30} Q{cx},{cy - 70} {cx + 64},{cy - 30}" fill="none" stroke="{HUSO}" stroke-width="1.6"/>'
        elif i == 2:
            b += celula(cx, cy, 95, 92)
            ys = [cy - 54, cy - 12, cy + 24, cy + 52]
            cr = [(MAT, L_G), (PAT, L_G), (MAT, L_P), (PAT, L_P)]
            pts = []
            for (col, L), yy in zip(cr, ys):
                # cromátidas hermanas una a cada lado del ecuador, mirando a polos opuestos
                b += doble(cx, yy, L * 0.68, col)
                pts.append((cx, yy - L * 0.08))
            b += huso(cx - 80, cy, [(cx - 6, p[1]) for p in pts]) + huso(cx + 80, cy, [(cx + 6, p[1]) for p in pts])
            b += centrosoma(cx - 80, cy) + centrosoma(cx + 80, cy)
            b += linea(cx, cy - 86, cx, cy + 86, ROJO, 1.2, 'stroke-dasharray="4 4"')
        elif i == 3:
            b += celula(cx, cy, 105, 76)
            cr = [(MAT, L_G), (PAT, L_G), (MAT, L_P), (PAT, L_P)]
            ys = [cy - 42, cy - 14, cy + 14, cy + 40]
            for (col, L), yy in zip(cr, ys):
                for sgn in (-1, 1):
                    xx = cx + sgn * 48
                    b += f'<g transform="rotate({90 if sgn > 0 else -90} {xx} {yy})">' + simple(xx, yy, L * 0.8, col) + "</g>"
                    b += linea(cx + sgn * 88, cy, xx + sgn * 16, yy, HUSO, 1.4)
            b += centrosoma(cx - 88, cy) + centrosoma(cx + 88, cy)
        else:
            b += f'<path d="M{cx - 100},{cy} C{cx - 100},{cy - 80} {cx - 10},{cy - 80} {cx},{cy - 26} C{cx + 10},{cy - 80} {cx + 100},{cy - 80} {cx + 100},{cy} C{cx + 100},{cy + 80} {cx + 10},{cy + 80} {cx},{cy + 26} C{cx - 10},{cy + 80} {cx - 100},{cy + 80} {cx - 100},{cy}z" fill="#fdf3e7" stroke="{MEMB}" stroke-width="3"/>'
            for sgn in (-1, 1):
                nx = cx + sgn * 52
                b += f'<circle cx="{nx}" cy="{cy}" r="30" fill="#dfe8f5" stroke="#3b5f8f" stroke-width="2.5"/>'
                for k, (col, L) in enumerate([(MAT, L_G), (PAT, L_G), (MAT, L_P), (PAT, L_P)]):
                    b += cromatida(nx - 15 + k * 10, cy, L * 0.55, col, w=6)
            b += text(cx, cy + 22, "◄ surco ►", 10, weight=900, fill=ROJO)
    b += text(600, 300, "Resultado: dos células hijas con el mismo número de cromosomas (2n = 4) y la misma información genética que la madre.", 14, weight=900, fill=PRI)
    save("mitosis-fases.svg", svg(1210, 315, b, "Fases de la mitosis en una célula animal con 2n = 4"))


def citocinesis():
    b = panel(10, 10, 440, 300, "Célula animal: estrangulamiento", "anillo contráctil de actina y miosina → surco de segmentación", ROJO)
    cx, cy = 230, 160
    b += f'<path d="M{cx - 150},{cy} C{cx - 150},{cy - 100} {cx - 20},{cy - 100} {cx},{cy - 40} C{cx + 20},{cy - 100} {cx + 150},{cy - 100} {cx + 150},{cy} C{cx + 150},{cy + 100} {cx + 20},{cy + 100} {cx},{cy + 40} C{cx - 20},{cy + 100} {cx - 150},{cy + 100} {cx - 150},{cy}z" fill="#fdf3e7" stroke="{MEMB}" stroke-width="3"/>'
    for sgn in (-1, 1):
        b += f'<circle cx="{cx + sgn * 80}" cy="{cy}" r="34" fill="#dfe8f5" stroke="#3b5f8f" stroke-width="2.5"/>' + centrosoma(cx + sgn * 130, cy - 30, False)
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="10" ry="42" fill="none" stroke="{ROJO}" stroke-width="5" stroke-dasharray="3 3"/>'
    b += linea(cx + 12, cy - 44, cx + 70, cy - 90, GRIS, 1.3) + text(cx + 74, cy - 92, "anillo contráctil", 13, "start", 900, fill=ROJO)
    b += linea(cx, cy + 42, cx - 40, cy + 112, GRIS, 1.3) + text(cx - 44, cy + 118, "surco", 13, "end", 900, fill=ROJO)
    b += panel(470, 10, 440, 300, "Célula vegetal: fragmoplasto", "vesículas del Golgi se fusionan → placa celular → nueva pared", VERDE)
    cx = 690
    b += f'<rect x="{cx - 160}" y="{cy - 95}" width="320" height="190" rx="10" fill="#f2f8ec" stroke="#5b8c2a" stroke-width="9"/>'
    for sgn in (-1, 1):
        b += f'<circle cx="{cx + sgn * 85}" cy="{cy}" r="34" fill="#dfe8f5" stroke="#3b5f8f" stroke-width="2.5"/>'
    for k in range(9):
        b += f'<circle cx="{cx + (k % 2) * 4 - 2}" cy="{cy - 56 + k * 14}" r="6" fill="#ffd58a" stroke="{ACC}" stroke-width="1.5"/>'
    b += linea(cx, cy - 34, cx, cy + 34, "#7aa33a", 5)
    b += linea(cx + 8, cy - 60, cx + 60, cy - 84, GRIS, 1.3) + text(cx + 64, cy - 80, "vesículas del Golgi", 13, "start", 900, fill=ACC)
    b += linea(cx + 4, cy + 20, cx - 30, cy + 114, GRIS, 1.3) + text(cx - 34, cy + 120, "placa celular", 13, "end", 900, fill=VERDE)
    b += text(460, 340, "En las células vegetales tampoco hay centriolos: el huso se forma sin ellos y sin áster (huso anastral).", 13, weight=800, fill=GRIS)
    save("citocinesis.svg", svg(920, 355, b, "Citocinesis por estrangulamiento en la célula animal y por fragmoplasto en la vegetal"))


# ---------------------------------------------------------------- meiosis
def meiosis():
    W, H = 280, 270
    b = ""
    tit = [("Profase I", "bivalentes y sobrecruzamiento (quiasmas)"), ("Metafase I", "bivalentes en la placa ecuatorial"),
           ("Anafase I", "se separan los cromosomas homólogos"), ("Telofase I", "2 células haploides, cromosomas dobles"),
           ("Metafase II", "cromosomas en la placa de cada célula"), ("Anafase II", "se separan las cromátidas hermanas"),
           ("Telofase II", "4 células haploides n = 2"), ("Resultado", "4 gametos distintos entre sí y de la madre")]
    # cromátidas: grande M (MAT, MAT con punta PAT), grande P (PAT con punta MAT, PAT); pequeño sin recombinar
    for i, (t, s) in enumerate(tit):
        r, c = divmod(i, 4)
        x0, y0 = 10 + c * (W + 10), 10 + r * (H + 10)
        b += panel(x0, y0, W, H, t, s, ROJO if i < 4 else PRI)
        cx, cy = x0 + W / 2, y0 + 140
        if i == 0:
            b += celula(cx, cy, 110, 90)
            b += f'<circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="#3b5f8f" stroke-width="2.5" stroke-dasharray="10 8"/>'
            # bivalente grande con quiasma
            bx, by = cx - 18, cy
            b += cromatida(bx - 15, by, L_G, MAT) + cromatida(bx - 5, by, L_G, MAT, PAT) + cromatida(bx + 5, by, L_G, PAT, MAT) + cromatida(bx + 15, by, L_G, PAT)
            b += linea(bx - 6, by + 4, bx + 6, by + 16, INK, 2) + linea(bx + 6, by + 4, bx - 6, by + 16, INK, 2)
            b += doble(cx + 30, cy - 8, L_P, MAT) + doble(cx + 52, cy - 8, L_P, PAT)
            b += linea(bx + 6, by + 10, cx - 70, cy + 70, GRIS, 1.2) + text(cx - 72, cy + 82, "quiasma", 12, "end", 900, fill=INK)
            b += centrosoma(cx - 90, cy - 40) + centrosoma(cx + 90, cy - 40)
        elif i == 1:
            b += celula(cx, cy, 115, 90)
            b += linea(cx, cy - 80, cx, cy + 80, ROJO, 1.2, 'stroke-dasharray="4 4"')
            for yy, L, ci, cd, pi, pd in ((cy - 28, L_G, MAT, PAT, PAT, MAT), (cy + 40, L_P, MAT, PAT, None, None)):
                b += doble(cx - 13, yy, L * 0.8, ci, ci, None, pi)
                b += doble(cx + 13, yy, L * 0.8, cd, cd, pd, None)
                b += linea(cx - 95, cy, cx - 30, yy, HUSO, 1.5) + linea(cx + 95, cy, cx + 30, yy, HUSO, 1.5)
            b += centrosoma(cx - 95, cy) + centrosoma(cx + 95, cy)
        elif i == 2:
            b += celula(cx, cy, 120, 86)
            for yy, L, col, punta, sgn in ((cy - 30, L_G, MAT, PAT, -1), (cy + 32, L_P, MAT, None, -1), (cy - 30, L_G, PAT, MAT, 1), (cy + 32, L_P, PAT, None, 1)):
                xx = cx + sgn * 58
                b += doble(xx, yy, L * 0.8, col, col, punta if sgn > 0 else None, punta if sgn < 0 else None)
                b += linea(cx + sgn * 100, cy, xx + sgn * 20, yy, HUSO, 1.4)
            b += centrosoma(cx - 100, cy) + centrosoma(cx + 100, cy)
        elif i == 3:
            for sgn, col, punta in ((-1, MAT, PAT), (1, PAT, MAT)):
                ccx = cx + sgn * 66
                b += f'<circle cx="{ccx}" cy="{cy}" r="58" fill="#fdf3e7" stroke="{MEMB}" stroke-width="3"/>'
                b += doble(ccx - 12, cy, L_G * 0.8, col, col, None, punta) + doble(ccx + 18, cy + 4, L_P * 0.8, col)
            b += text(cx - 66, cy + 80, "n = 2", 13, weight=900, fill=ACC) + text(cx + 66, cy + 80, "n = 2", 13, weight=900, fill=ACC)
        elif i in (4, 5, 6):
            for sgn, col, punta in ((-1, MAT, PAT), (1, PAT, MAT)):
                ccx = cx + sgn * 66
                if i == 6:
                    for d in (-1, 1):
                        b += f'<circle cx="{ccx}" cy="{cy + d * 40}" r="34" fill="#fff4df" stroke="{MEMB}" stroke-width="2.5"/>'
                    b += simple(ccx - 8, cy - 40, L_G * 0.7, col) + simple(ccx + 10, cy - 40, L_P * 0.7, col)
                    b += simple(ccx - 8, cy + 40, L_G * 0.7, col, punta) + simple(ccx + 10, cy + 40, L_P * 0.7, col)
                    continue
                b += f'<ellipse cx="{ccx}" cy="{cy}" rx="58" ry="70" fill="#fdf3e7" stroke="{MEMB}" stroke-width="3"/>'
                b += centrosoma(ccx, cy - 60, False) + centrosoma(ccx, cy + 60, False)
                if i == 4:
                    b += f'<g transform="rotate(90 {ccx - 14} {cy})">' + doble(ccx - 14, cy, L_G * 0.7, col, col, None, punta) + "</g>"
                    b += f'<g transform="rotate(90 {ccx + 26} {cy})">' + doble(ccx + 26, cy, L_P * 0.7, col) + "</g>"
                    for xx in (ccx - 14, ccx + 26):
                        b += linea(ccx, cy - 60, xx, cy - 10, HUSO, 1.3) + linea(ccx, cy + 60, xx, cy + 10, HUSO, 1.3)
                    b += linea(ccx - 50, cy, ccx + 50, cy, ROJO, 1.2, 'stroke-dasharray="4 4"')
                else:
                    b += simple(ccx - 12, cy - 36, L_G * 0.6, col) + simple(ccx + 12, cy - 36, L_P * 0.6, col)
                    b += simple(ccx - 12, cy + 36, L_G * 0.6, col, punta) + simple(ccx + 12, cy + 36, L_P * 0.6, col)
                    for xx in (ccx - 12, ccx + 12):
                        b += linea(ccx, cy - 60, xx, cy - 46, HUSO, 1.3) + linea(ccx, cy + 60, xx, cy + 46, HUSO, 1.3)
        else:
            gam = [(MAT, None, MAT), (MAT, PAT, MAT), (PAT, None, PAT), (PAT, MAT, PAT)]
            for k, (cg, pg, cp) in enumerate(gam):
                gx = x0 + 42 + k * 65
                b += f'<circle cx="{gx}" cy="{cy}" r="29" fill="#fff4df" stroke="{MEMB}" stroke-width="2.5"/>'
                b += simple(gx - 8, cy, L_G * 0.7, cg, pg) + simple(gx + 10, cy, L_P * 0.7, cp)
            b += text(cx, cy + 56, "dos con cromátidas recombinadas", 12, weight=800, fill=GRIS)
            b += text(cx, cy - 50, "(con otra segregación, saldrían", 12, weight=800, fill=GRIS) + text(cx, cy - 36, "otras combinaciones)", 12, weight=800, fill=GRIS)
    b += text(590, 576, "MEIOSIS I: división reduccional (separa homólogos) · MEIOSIS II: división ecuacional (separa cromátidas), sin replicación previa", 14, weight=900, fill=PRI)
    save("meiosis-fases.svg", svg(1170, 590, b, "Fases de la meiosis en una célula con 2n = 4, con sobrecruzamiento"))


# ---------------------------------------------------------------- comparación y ADN
def comparacion():
    b = panel(10, 10, 420, 300, "Mitosis", "células somáticas · 1 división", PRI)
    def cel(cx, cy, r, cromos, fill="#fdf3e7"):
        s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{MEMB}" stroke-width="2.5"/>'
        n = len(cromos)
        for k, (col, L, p) in enumerate(cromos):
            s += simple(cx - (n - 1) * 8 + k * 16, cy, L, col, p)
        return s
    dip = [(MAT, L_G * .8, None), (PAT, L_G * .8, None), (MAT, L_P * .8, None), (PAT, L_P * .8, None)]
    b += cel(110, 150, 50, dip) + text(110, 222, "2n = 4", 14, weight=900, fill=PRI)
    b += flecha(166, 130, 250, 90) + flecha(166, 170, 250, 210)
    b += cel(310, 90, 46, dip) + cel(310, 215, 46, dip)
    b += text(310, 158, "2 células 2n, idénticas", 13, weight=900, fill=PRI)
    b += panel(450, 10, 520, 300, "Meiosis", "células germinales · 2 divisiones", ROJO)
    b += cel(550, 150, 50, dip) + text(550, 222, "2n = 4", 14, weight=900, fill=ROJO)
    b += flecha(606, 150, 660, 150) + text(633, 140, "I y II", 12, weight=900, fill=ROJO)
    gam = [[(MAT, L_G * .8, None), (MAT, L_P * .8, None)], [(MAT, L_G * .8, PAT), (MAT, L_P * .8, None)], [(PAT, L_G * .8, None), (PAT, L_P * .8, None)], [(PAT, L_G * .8, MAT), (PAT, L_P * .8, None)]]
    for k, g in enumerate(gam):
        b += cel(710 + (k % 2) * 90, 95 + (k // 2) * 110, 38, g, "#fff4df")
    b += text(890, 150, "4 células", 13, "start", 900, fill=ROJO) + text(890, 166, "n, distintas", 13, "start", 900, fill=ROJO)
    save("mitosis-vs-meiosis.svg", svg(985, 320, b, "Comparación del resultado de la mitosis y de la meiosis"))


def adn_grafica():
    x0, y0, w, h = 90, 40, 820, 260
    def Y(c):
        return y0 + h - c / 4 * h
    b = linea(x0, y0 + h, x0 + w, y0 + h, INK, 2.5) + linea(x0, y0 + h, x0, y0 - 10, INK, 2.5)
    for c in (1, 2, 4):
        b += text(x0 - 10, Y(c) + 5, f"{c}C", 14, "end", 900, fill=GRIS) + linea(x0, Y(c), x0 + w, Y(c), "#e1e7ec", 1)
    b += text(30, y0 + h / 2, "Cantidad de ADN", 15, weight=900, fill=GRIS, style=f'transform="rotate(-90 30 {y0 + h / 2})"')
    # mitosis (izquierda) y meiosis (derecha)
    seg_mit = [(0, 2), (90, 2), (150, 4), (240, 4), (300, 4), (300, 2), (370, 2)]
    seg_mei = [(430, 2), (500, 2), (560, 4), (640, 4), (690, 4), (690, 2), (750, 2), (750, 1), (815, 1)]
    for seg, col in ((seg_mit, PRI), (seg_mei, ROJO)):
        b += f'<polyline points="{" ".join(f"{x0 + x},{Y(c):.1f}" for x, c in seg)}" fill="none" stroke="{col}" stroke-width="4"/>'
    for x, t in ((45, "G1"), (120, "S"), (195, "G2"), (270, "M"), (335, "G1")):
        b += text(x0 + x, y0 + h + 22, t, 13, weight=900, fill=PRI)
    for x, t in ((465, "G1"), (530, "S"), (600, "G2"), (663, "M. I"), (722, "M. II"), (785, "gametos")):
        b += text(x0 + x, y0 + h + 22, t, 12, weight=900, fill=ROJO)
    b += text(x0 + 185, y0 + h + 48, "MITOSIS", 15, weight=900, fill=PRI) + text(x0 + 620, y0 + h + 48, "MEIOSIS", 15, weight=900, fill=ROJO)
    b += linea(x0 + 400, y0 - 10, x0 + 400, y0 + h, GRIS, 1.2, 'stroke-dasharray="5 5"')
    b += text(x0 + w / 2, y0 + h + 76, "C = cantidad de ADN de una célula haploide (gameto). 2n en G1 = 2C; tras la fase S, 4C (mismo nº de cromosomas, con dos cromátidas).", 12.5, weight=800, fill=GRIS)
    save("adn-mitosis-meiosis.svg", svg(940, 390, b, "Variación de la cantidad de ADN en el ciclo con mitosis y con meiosis"))


if __name__ == "__main__":
    cromosoma(); ciclo_vital(); mitosis(); citocinesis(); meiosis(); comparacion(); adn_grafica()
