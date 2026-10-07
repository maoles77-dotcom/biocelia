# Esquemas SVG del tema C1 (morfología celular) de BioCelia.
# Uso: python tools/esquemas_tema_c1.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "c1")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO, VERDE = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"
MEMB = "#2a7fc1"


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


def et(x, y, tx, ty, s, col=INK, size=14, anchor=None):
    """Etiqueta con línea guía desde (x, y) hasta el texto en (tx, ty)."""
    if anchor is None:
        anchor = "start" if tx > x else "end"
    dx = 4 if anchor == "start" else -4
    return (linea(x, y, tx - dx, ty - 5, GRIS, 1.3) + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.5" fill="{GRIS}"/>'
            + text(tx, ty, s, size, anchor, 800, fill=col))


# ---------------------------------------------------------------- piezas de orgánulos
def mitocondria(cx, cy, w=90, h=44, rot=0):
    s = f'<g transform="rotate({rot} {cx} {cy})">'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="{h / 2}" fill="#f6c7a8" stroke="#b5532c" stroke-width="2.5"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2 - 5}" ry="{h / 2 - 5}" fill="#fbe3d3" stroke="#b5532c" stroke-width="1.5"/>'
    n = max(3, int(w / 18))
    for k in range(n):
        x = cx - w / 2 + 12 + k * (w - 24) / (n - 1)
        top = k % 2 == 0
        y0 = cy - h / 2 + 5 if top else cy + h / 2 - 5
        y1 = cy + (h * 0.12 if top else -h * 0.12)
        s += f'<path d="M{x - 4},{y0} L{x - 4},{y1} Q{x},{y1 + (6 if top else -6)} {x + 4},{y1} L{x + 4},{y0}" fill="#f6c7a8" stroke="#b5532c" stroke-width="1.3"/>'
    return s + "</g>"


def cloroplasto(cx, cy, w=110, h=56, rot=0):
    s = f'<g transform="rotate({rot} {cx} {cy})">'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2}" ry="{h / 2}" fill="#bfe3b4" stroke="#2f7d32" stroke-width="2.5"/>'
    s += f'<ellipse cx="{cx}" cy="{cy}" rx="{w / 2 - 4}" ry="{h / 2 - 4}" fill="#d8f0d0" stroke="#2f7d32" stroke-width="1.2"/>'
    for k in range(4):
        gx = cx - w * 0.33 + k * w * 0.22
        for j in range(4):
            s += f'<rect x="{gx - 7}" y="{cy - 10 + j * 5}" width="14" height="4" rx="2" fill="#3f9142"/>'
        if k < 3:
            s += linea(gx + 7, cy, gx + w * 0.22 - 7, cy, "#3f9142", 1.5)
    return s + "</g>"


def golgi(cx, cy, esc=1.0):
    s = ""
    for k in range(5):
        w = (70 - k * 6) * esc
        y = cy - 20 * esc + k * 9 * esc
        s += f'<path d="M{cx - w / 2},{y} Q{cx},{y - 10 * esc} {cx + w / 2},{y}" fill="none" stroke="#c77d00" stroke-width="{5 * esc}" stroke-linecap="round"/>'
    for dx, dy in ((-44, 14), (44, 14), (-38, 32), (40, 34)):
        s += f'<circle cx="{cx + dx * esc}" cy="{cy + dy * esc}" r="{5 * esc}" fill="#ffd58a" stroke="#c77d00" stroke-width="1.5"/>'
    return s


def rer(x, y, w=120, n=4, esc=1.0):
    s = ""
    for k in range(n):
        yy = y + k * 14 * esc
        s += f'<path d="M{x},{yy} q{w / 4},-8 {w / 2},0 t{w / 2},0" fill="none" stroke="#7b5ea7" stroke-width="{5 * esc}" stroke-linecap="round"/>'
        for j in range(9):
            s += f'<circle cx="{x + 6 + j * w / 9:.1f}" cy="{yy - 6 * esc:.1f}" r="{1.8 * esc}" fill="{INK}"/>'
    return s


def rel(x, y, esc=1.0):
    return (f'<path d="M{x},{y} c20,-20 40,10 60,-6 s30,24 50,4 M{x + 10},{y + 18} c20,-14 40,14 60,0 s24,18 40,4" fill="none" '
            f'stroke="#9b7fc9" stroke-width="{6 * esc}" stroke-linecap="round"/>')


def nucleo(cx, cy, r=70, poros=True):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#dfe8f5" stroke="#3b5f8f" stroke-width="5"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r - 6}" fill="none" stroke="#3b5f8f" stroke-width="1.5"/>'
    if poros:
        for a in range(0, 360, 40):
            x, y = cx + (r - 3) * math.cos(math.radians(a)), cy + (r - 3) * math.sin(math.radians(a))
            s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#dfe8f5"/>'
    s += f'<circle cx="{cx + r * 0.2}" cy="{cy - r * 0.15}" r="{r * 0.28}" fill="#55606c"/>'
    for k in range(int(r / 6)):
        a = k * 2.4
        px, py = cx + r * 0.55 * math.cos(a) * ((k % 5) + 2) / 6, cy + r * 0.55 * math.sin(a) * ((k % 5) + 2) / 6
        s += f'<path d="M{px:.1f},{py:.1f} q{r * 0.05:.1f},{-r * 0.04:.1f} {r * 0.1:.1f},0 t{r * 0.1:.1f},0" fill="none" stroke="#7d8fa6" stroke-width="2"/>'
    return s


def ribos(pts, r=2.4):
    return "".join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{INK}"/>' for x, y in pts)


def centrosoma(cx, cy, esc=1.0):
    s = ""
    for a in range(0, 360, 30):
        s += linea(cx + 14 * esc * math.cos(math.radians(a)), cy + 14 * esc * math.sin(math.radians(a)),
                   cx + 34 * esc * math.cos(math.radians(a)), cy + 34 * esc * math.sin(math.radians(a)), "#8aa1b8", 1.5)
    s += f'<rect x="{cx - 12 * esc}" y="{cy - 5 * esc}" width="{16 * esc}" height="{10 * esc}" rx="2" fill="#5d7ea8"/>'
    s += f'<rect x="{cx + 2 * esc}" y="{cy - 10 * esc}" width="{10 * esc}" height="{18 * esc}" rx="2" fill="#5d7ea8"/>'
    return s


# ---------------------------------------------------------------- células
def celula_animal():
    b = f'<path d="M120,260 C110,120 260,40 420,60 C590,80 700,150 690,290 C680,430 560,500 400,490 C230,480 130,400 120,260z" fill="#fdf3e7" stroke="{MEMB}" stroke-width="5"/>'
    b += nucleo(390, 270, 85)
    b += rer(250, 150, 110, 3) + rel(520, 380)
    b += golgi(560, 200)
    b += mitocondria(230, 360, 90, 42, 20) + mitocondria(470, 430, 80, 38, -10) + mitocondria(600, 290, 70, 34, 70)
    b += f'<circle cx="300" cy="430" r="20" fill="#f3b8c8" stroke="#b03a5b" stroke-width="2.5"/>' + ribos([(293, 425), (305, 432), (300, 438)], 2)
    b += f'<circle cx="640" cy="380" r="12" fill="#e9f1c2" stroke="#7a8b1f" stroke-width="2.5"/>'
    b += centrosoma(500, 120, 0.9)
    b += ribos([(180, 220), (196, 250), (210, 300), (180, 310), (650, 230), (620, 420), (360, 470), (450, 110), (330, 400)])
    b += f'<circle cx="610" cy="140" r="9" fill="#ffe2a8" stroke="#c77d00" stroke-width="2"/>'
    # etiquetas
    L = [(392, 248, 760, 240, "núcleo"), (420, 268, 760, 270, "nucléolo"), (473, 290, 760, 300, "envoltura nuclear"),
         (300, 150, 30, 120, "RER"), (560, 375, 760, 420, "REL"), (590, 200, 760, 190, "complejo de Golgi"),
         (230, 360, 30, 380, "mitocondria"), (300, 440, 30, 450, "lisosoma"), (640, 380, 760, 380, "peroxisoma"),
         (500, 120, 760, 110, "centrosoma"), (180, 220, 30, 220, "ribosomas"), (610, 140, 760, 150, "vesícula"),
         (690, 300, 760, 330, "membrana plasmática"), (150, 330, 30, 300, "citosol")]
    for x, y, tx, ty, s in L:
        b += et(x, y, tx, ty, s, INK, 15)
    save("celula-animal.svg", svg(1090, 520, '<g transform="translate(150,0)">' + b + "</g>", "Célula eucariota animal con sus orgánulos"))


def celula_vegetal():
    b = f'<rect x="120" y="40" width="580" height="450" rx="26" fill="#e6f2d9" stroke="#5b8c2a" stroke-width="12"/>'
    b += f'<rect x="132" y="52" width="556" height="426" rx="18" fill="#f7fbef" stroke="{MEMB}" stroke-width="3"/>'
    b += f'<path d="M300,140 C300,100 600,100 610,150 L620,340 C620,400 330,410 310,360z" fill="#dff0fb" stroke="#4a8fc1" stroke-width="3"/>'
    b += nucleo(210, 380, 55)
    b += cloroplasto(220, 120, 100, 48, 10) + cloroplasto(640, 420, 90, 44, -15) + cloroplasto(220, 250, 90, 44, 80) + cloroplasto(460, 445, 90, 42, 0)
    b += mitocondria(650, 110, 70, 34, 30) + mitocondria(340, 450, 60, 30, -10)
    b += golgi(560, 455, 0.7) + rer(420, 75, 90, 2, 0.8)
    b += ribos([(170, 300), (300, 430), (650, 300), (650, 220), (400, 90)])
    b += linea(410, 40, 410, 52, "#6b4f1d", 4) + linea(400, 478, 400, 490, "#6b4f1d", 4)
    L = [(460, 250, 760, 240, "vacuola (tonoplasto)"), (210, 360, 30, 400, "núcleo"), (220, 120, 30, 110, "cloroplasto"),
         (650, 110, 760, 100, "mitocondria"), (560, 455, 760, 460, "complejo de Golgi"), (470, 70, 760, 60, "RER"),
         (700, 300, 760, 300, "pared celular"), (688, 360, 760, 360, "membrana plasmática"), (410, 46, 760, 20, "plasmodesmo"),
         (170, 300, 30, 300, "ribosomas")]
    for x, y, tx, ty, s in L:
        b += et(x, y, tx, ty, s, INK, 15)
    save("celula-vegetal.svg", svg(1090, 520, '<g transform="translate(150,0)">' + b + "</g>", "Célula eucariota vegetal con pared, cloroplastos y gran vacuola"))


def celula_procariota():
    b = f'<rect x="150" y="110" width="560" height="250" rx="125" fill="#f3ead7" stroke="#d9c38f" stroke-width="22" opacity="0.9"/>'
    b += f'<rect x="166" y="126" width="528" height="218" rx="109" fill="#fbf6ea" stroke="#8b6a2c" stroke-width="8"/>'
    b += f'<rect x="176" y="136" width="508" height="198" rx="99" fill="#fffdf6" stroke="{MEMB}" stroke-width="3"/>'
    b += f'<path d="M330,230 C320,180 430,170 450,210 C470,250 540,190 560,240 C580,290 450,300 420,270 C390,245 340,290 330,230z" fill="none" stroke="#1f5f99" stroke-width="4"/>'
    b += f'<circle cx="260" cy="200" r="16" fill="none" stroke="{ACC}" stroke-width="3.5"/>'
    b += f'<circle cx="610" cy="280" r="11" fill="none" stroke="{ACC}" stroke-width="3.5"/>'
    b += ribos([(240, 260), (260, 290), (300, 300), (600, 190), (630, 220), (560, 300), (300, 170), (500, 160)], 3)
    b += f'<ellipse cx="620" cy="160" rx="14" ry="10" fill="#e3d1ff" stroke="{LILA}" stroke-width="2"/>'
    b += f'<path d="M700,235 C760,200 790,270 850,235 S920,200 960,240" fill="none" stroke="{INK}" stroke-width="3.5"/>'
    for x, y, a in ((300, 112, -90), (360, 108, -90), (420, 108, -90), (480, 110, -90), (300, 358, 90), (380, 362, 90), (460, 362, 90), (540, 358, 90)):
        b += linea(x, y, x + 22 * math.cos(math.radians(a)), y + 22 * math.sin(math.radians(a)), "#7b8a97", 2)
    b += linea(210, 140, 160, 70, "#7b8a97", 3.5)
    L = [(470, 210, 470, 40, "nucleoide (cromosoma bacteriano)", "middle"), (260, 184, 40, 170, "plásmido", None),
         (240, 260, 40, 270, "ribosomas 70S", None), (620, 160, 760, 120, "inclusión", None), (850, 235, 860, 290, "flagelo", None),
         (420, 86, 600, 60, "fimbrias", None), (160, 70, 40, 60, "pilus", None), (430, 352, 430, 420, "cápsula", "middle"),
         (690, 300, 760, 330, "pared celular", None), (680, 260, 760, 370, "membrana plasmática", None), (200, 330, 40, 360, "citosol", None)]
    for x, y, tx, ty, s, an in L:
        b += et(x, y, tx, ty, s, INK, 15, an)
    save("celula-procariota.svg", svg(1130, 440, '<g transform="translate(150,0)">' + b + "</g>", "Célula procariota (bacteria) con sus componentes"))


# ---------------------------------------------------------------- membrana
def fosfolipido(x, y, arriba=True, col="#f4a261"):
    s = f'<circle cx="{x}" cy="{y}" r="7" fill="{col}" stroke="#b5651d" stroke-width="1.2"/>'
    d = 1 if arriba else -1
    s += linea(x - 3, y + 7 * d, x - 4, y + 38 * d, "#c9a227", 2.2) + linea(x + 3, y + 7 * d, x + 4, y + 38 * d, "#c9a227", 2.2)
    return s


def membrana():
    b = ""
    y1, y2 = 140, 236
    xs = [x for x in range(40, 1040, 16)]
    hueco = [(250, 330), (520, 600), (790, 840)]

    def libre(x):
        return not any(a <= x <= b_ for a, b_ in hueco)
    for x in xs:
        if libre(x):
            b += fosfolipido(x, y1, True) + fosfolipido(x, y2, False)
    # colesterol
    for x in (120, 440, 720, 940):
        b += f'<rect x="{x + 3}" y="{y1 + 10}" width="6" height="26" rx="3" fill="#7b3fb0"/>'
    # proteínas
    b += f'<path d="M250,110 C240,180 245,250 260,270 C290,290 320,280 330,260 C340,200 335,130 320,110 C300,95 265,95 250,110z" fill="#7fb3e6" stroke="#2a5d8f" stroke-width="2.5"/>'
    b += f'<path d="M522,110 C516,160 516,230 530,270 C560,290 590,280 598,260 C604,200 604,140 595,110 C575,96 540,96 522,110z" fill="#7fb3e6" stroke="#2a5d8f" stroke-width="2.5"/>'
    b += f'<rect x="548" y="112" width="20" height="156" rx="8" fill="#eaf4ff" stroke="#2a5d8f" stroke-width="1.5"/>'
    b += f'<ellipse cx="815" cy="132" rx="32" ry="20" fill="#7fb3e6" stroke="#2a5d8f" stroke-width="2.5"/>'
    b += f'<ellipse cx="420" cy="262" rx="40" ry="18" fill="#a6c8ea" stroke="#2a5d8f" stroke-width="2.5"/>'
    # glúcidos (cara externa)
    def cadena(x, y, n=4):
        s = ""
        for k in range(n):
            xx, yy = x + (6 if k % 2 else -6), y - 12 - k * 12
            s += f'<polygon points="{xx},{yy - 6} {xx + 6},{yy} {xx},{yy + 6} {xx - 6},{yy}" fill="#3f8a3a"/>'
        return s
    b += cadena(290, 100, 4) + cadena(150, 128, 3) + cadena(680, 128, 4) + cadena(815, 112, 3)
    # rótulos
    b += text(20, 30, "MEDIO EXTRACELULAR", 15, "start", 900, fill=PRI) + text(20, 360, "CITOPLASMA", 15, "start", 900, fill=PRI)
    L = [(150, 100, 200, 40, "glucolípido", "start"), (290, 64, 340, 20, "glucoproteína", "start"), (680, 80, 720, 30, "glucocáliz", "start"),
         (815, 118, 870, 50, "proteína periférica", "start"), (968, 140, 1000, 96, "cabeza hidrófila", "start"),
         (126, 165, 140, 322, "colesterol", "middle"), (296, 200, 330, 348, "proteína integral (transmembrana)", "middle"),
         (420, 270, 480, 322, "proteína periférica", "start"), (558, 190, 640, 348, "proteína canal", "start"),
         (972, 175, 1000, 322, "colas hidrófobas", "start")]
    for x, y, tx, ty, s, an in L:
        b += et(x, y, tx, ty, s, INK, 14, an)
    b += text(1050, 196, "bicapa", 14, "start", 900, fill=GRIS) + text(1050, 214, "lipídica", 14, "start", 900, fill=GRIS)
    b += linea(1040, 132, 1040, 244, GRIS, 2)
    save("mosaico-fluido.svg", svg(1130, 375, b, "Modelo del mosaico fluido de la membrana plasmática"))


def transporte():
    b = ""
    y1, y2 = 150, 250
    for x in range(30, 1110, 15):
        if not (330 <= x <= 390 or 560 <= x <= 630 or 800 <= x <= 880):
            b += f'<circle cx="{x}" cy="{y1}" r="6" fill="#f4a261"/>' + f'<circle cx="{x}" cy="{y2}" r="6" fill="#f4a261"/>'
            b += linea(x - 2, y1 + 6, x - 2, y1 + 44, "#e2c56a", 2) + linea(x - 2, y2 - 6, x - 2, y2 - 44, "#e2c56a", 2)
    b += text(20, 30, "Exterior", 15, "start", 900, fill=PRI) + text(20, 330, "Citoplasma", 15, "start", 900, fill=PRI)
    def mol(x, y, c, r=7):
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}" stroke="{INK}" stroke-width="1"/>'
    # A difusión simple
    for x, y in ((120, 60), (150, 90), (190, 70), (100, 100), (170, 120)):
        b += mol(x, y, "#9ad1f5")
    b += mol(160, 300, "#9ad1f5") + flecha(150, 110, 150, 290, PRI, 3)
    b += text(160, 380, "A · Difusión simple", 16, weight=900, fill=PRI) + text(160, 400, "por la bicapa: O₂, CO₂,", 13, weight=800, fill=GRIS) + text(160, 416, "etanol, sustancias apolares", 13, weight=800, fill=GRIS)
    # B canal
    b += f'<rect x="332" y="140" width="22" height="120" rx="8" fill="#7fb3e6" stroke="#2a5d8f" stroke-width="2"/><rect x="366" y="140" width="22" height="120" rx="8" fill="#7fb3e6" stroke="#2a5d8f" stroke-width="2"/>'
    for x, y in ((330, 70), (370, 90), (400, 60), (350, 110)):
        b += mol(x, y, "#ffb3b3", 6)
    b += mol(360, 300, "#ffb3b3", 6) + flecha(360, 120, 360, 290, ROJO, 3)
    b += text(360, 380, "B · Difusión facilitada", 16, weight=900, fill=ROJO) + text(360, 400, "por proteína canal: iones", 13, weight=800, fill=GRIS) + text(360, 416, "(agua: acuaporinas)", 13, weight=800, fill=GRIS)
    # C transportadora
    b += f'<path d="M562,140 L628,140 L612,200 L628,260 L562,260 L578,200z" fill="#9fd8c2" stroke="#1d7a5f" stroke-width="2.5"/>'
    for x, y in ((560, 70), (600, 95), (640, 60), (580, 110)):
        b += f'<rect x="{x - 7}" y="{y - 7}" width="14" height="14" rx="3" fill="#ffe08a" stroke="{INK}"/>'
    b += f'<rect x="588" y="294" width="14" height="14" rx="3" fill="#ffe08a" stroke="{INK}"/>' + flecha(595, 120, 595, 288, VERDE, 3)
    b += text(595, 380, "C · Difusión facilitada", 16, weight=900, fill=VERDE) + text(595, 400, "por proteína transportadora", 13, weight=800, fill=GRIS) + text(595, 416, "(permeasa): glucosa, aminoácidos", 13, weight=800, fill=GRIS)
    # D bomba Na/K
    b += f'<rect x="802" y="140" width="76" height="120" rx="14" fill="#d9c8f5" stroke="{LILA}" stroke-width="2.5"/>' + text(840, 205, "bomba", 12, weight=900, fill=LILA)
    for k in range(5):
        b += mol(800 + k * 18, 50 + (k % 2) * 16, "#ffd166", 6)
    b += text(780, 46, "Na⁺", 13, "end", 900, fill=ACC)
    for k in range(5):
        b += mol(800 + k * 18, 300 + (k % 2) * 14, "#8ecae6", 6)
    b += text(780, 316, "K⁺", 13, "end", 900, fill=PRI)
    b += flecha(820, 250, 820, 110, ACC, 3) + text(818, 104, "3 Na⁺", 12, "end", 900, fill=ACC)
    b += flecha(862, 120, 862, 280, PRI, 3) + text(866, 290, "2 K⁺", 12, "start", 900, fill=PRI)
    b += f'<ellipse cx="930" cy="280" rx="30" ry="15" fill="#fff4df" stroke="{ACC}" stroke-width="2"/>' + text(930, 285, "ATP", 13, weight=900, fill=ACC)
    b += flecha(905, 272, 882, 262, ACC, 2)
    b += text(860, 380, "D · Transporte activo", 16, weight=900, fill=LILA) + text(860, 400, "contra gradiente, con ATP:", 13, weight=800, fill=GRIS) + text(860, 416, "bomba de Na⁺/K⁺", 13, weight=800, fill=GRIS)
    b += f'<rect x="20" y="440" width="700" height="34" rx="10" fill="#e3eef8"/>' + text(370, 462, "A, B y C: transporte PASIVO (a favor de gradiente, sin gasto de energía)", 14, weight=900, fill=PRI)
    b += f'<rect x="740" y="440" width="380" height="34" rx="10" fill="#efe7fb"/>' + text(930, 462, "D: transporte ACTIVO (con ATP)", 14, weight=900, fill=LILA)
    save("transporte-membrana.svg", svg(1140, 490, b, "Difusión simple, difusión facilitada por canal y por transportadora y transporte activo"))


def osmosis():
    b = ""
    cols = [("Medio hipotónico", "entra agua", "#e3f2fd"), ("Medio isotónico", "sin cambio neto", "#f4f8fb"), ("Medio hipertónico", "sale agua", "#fff2e0")]
    for i, (t, s, f) in enumerate(cols):
        x = 230 + i * 300
        b += f'<rect x="{x - 140}" y="20" width="280" height="440" rx="18" fill="{f}" stroke="#c3ccd4"/>'
        b += text(x, 52, t, 18, weight=900, fill=PRI) + text(x, 74, s, 14, weight=800, fill=GRIS)
    b += text(40, 170, "Célula", 15, "middle", 900, fill=ROJO, style='transform="rotate(-90 40 170)"')
    b += text(40, 360, "Célula", 15, "middle", 900, fill=VERDE, style='transform="rotate(-90 40 360)"')
    b += text(62, 170, "animal", 15, "middle", 900, fill=ROJO, style='transform="rotate(-90 62 170)"')
    b += text(62, 360, "vegetal", 15, "middle", 900, fill=VERDE, style='transform="rotate(-90 62 360)"')
    # animal
    b += f'<circle cx="230" cy="160" r="56" fill="#f7c6c0" stroke="{ROJO}" stroke-width="3" stroke-dasharray="8 6"/>' + text(230, 244, "se hincha y estalla", 13, weight=900, fill=ROJO) + text(230, 260, "(lisis; hemólisis)", 12, weight=800, fill=GRIS)
    b += f'<ellipse cx="530" cy="160" rx="54" ry="40" fill="#f7c6c0" stroke="{ROJO}" stroke-width="3"/><ellipse cx="530" cy="160" rx="22" ry="14" fill="#f0a49a"/>' + text(530, 244, "normal", 13, weight=900, fill=ROJO)
    b += f'<path d="M790,160 l14,-30 l18,8 l20,-20 l10,26 l22,6 l-12,24 l12,22 l-24,6 l-8,24 l-20,-14 l-18,12 l-6,-24 l-22,-8 z" fill="#f7c6c0" stroke="{ROJO}" stroke-width="3"/>' + text(830, 244, "se arruga", 13, weight=900, fill=ROJO) + text(830, 260, "(crenación)", 12, weight=800, fill=GRIS)
    for k, x in enumerate((230, 530, 830)):
        pass
    # vegetal
    def vegetal(cx, cy, sep):
        s = f'<rect x="{cx - 60}" y="{cy - 50}" width="120" height="100" rx="8" fill="none" stroke="#5b8c2a" stroke-width="7"/>'
        w, h = 112 - sep * 2, 92 - sep * 2
        s += f'<rect x="{cx - w / 2}" y="{cy - h / 2}" width="{w}" height="{h}" rx="{8 + sep}" fill="#e6f2d9" stroke="{MEMB}" stroke-width="2.5"/>'
        vw, vh = max(w - 30, 10), max(h - 30, 10)
        s += f'<rect x="{cx - vw / 2}" y="{cy - vh / 2}" width="{vw}" height="{vh}" rx="{6 + sep}" fill="#cfe8fa" stroke="#4a8fc1" stroke-width="1.5"/>'
        return s
    b += vegetal(230, 360, 0) + text(230, 440, "turgente", 13, weight=900, fill=VERDE) + text(230, 456, "(la pared impide que estalle)", 12, weight=800, fill=GRIS)
    b += vegetal(530, 360, 3) + text(530, 440, "flácida", 13, weight=900, fill=VERDE)
    b += vegetal(830, 360, 22) + text(830, 440, "plasmólisis", 13, weight=900, fill=VERDE) + text(830, 456, "(la membrana se separa de la pared)", 12, weight=800, fill=GRIS)
    for x, d in ((230, 1), (830, -1)):
        if d > 0:
            b += flecha(x - 100, 110, x - 70, 130, PRI, 2.5) + text(x - 100, 100, "H₂O", 13, weight=900, fill=PRI)
        else:
            b += flecha(x + 70, 130, x + 100, 110, PRI, 2.5) + text(x + 104, 100, "H₂O", 13, weight=900, fill=PRI)
    save("osmosis-celulas.svg", svg(1000, 480, b, "Células animales y vegetales en medios hipotónico, isotónico e hipertónico"))


def endocitosis():
    b = ""
    paneles = [("Fagocitosis", "partículas grandes,", "microorganismos"), ("Pinocitosis", "líquido con", "solutos"),
               ("Mediada por receptor", "moléculas concretas", "(p. ej., colesterol-LDL)"), ("Exocitosis", "secreción al", "exterior")]
    for i, (t, s1, s2) in enumerate(paneles):
        x = 140 + i * 270
        b += f'<rect x="{x - 125}" y="20" width="250" height="330" rx="16" fill="{"#f6f9fb" if i % 2 == 0 else "#fff"}" stroke="#d5dde3"/>'
        b += text(x, 50, t, 17, weight=900, fill=PRI if i < 3 else VERDE)
        b += text(x, 300, s1, 13, weight=800, fill=GRIS) + text(x, 318, s2, 13, weight=800, fill=GRIS)
    # fagocitosis: pseudópodos rodeando bacteria
    b += f'<path d="M30,140 L80,140 C70,90 110,70 140,100 C170,70 210,90 200,140 L250,140" fill="none" stroke="{MEMB}" stroke-width="4"/>'
    b += f'<rect x="120" y="100" width="40" height="22" rx="11" fill="#8ab17d" stroke="{VERDE}" stroke-width="2"/>'
    b += f'<circle cx="140" cy="220" r="30" fill="#fff" stroke="{MEMB}" stroke-width="3"/><rect x="122" y="210" width="36" height="20" rx="10" fill="#8ab17d" stroke="{VERDE}" stroke-width="2"/>'
    b += flecha(140, 150, 140, 184) + text(140, 270, "fagosoma", 13, weight=900, fill=INK)
    # pinocitosis
    x = 410
    b += f'<path d="M{x - 110},140 L{x - 24},140 C{x - 24},180 {x + 24},180 {x + 24},140 L{x + 110},140" fill="none" stroke="{MEMB}" stroke-width="4"/>'
    for k in range(5):
        b += f'<circle cx="{x - 14 + k * 7}" cy="{150 + (k % 2) * 6}" r="2.5" fill="{PRI}"/>'
    b += f'<circle cx="{x}" cy="225" r="18" fill="#e3f2fd" stroke="{MEMB}" stroke-width="3"/>'
    for k in range(4):
        b += f'<circle cx="{x - 8 + k * 6}" cy="{224 + (k % 2) * 5}" r="2.3" fill="{PRI}"/>'
    b += flecha(x, 172, x, 202) + text(x, 270, "vesícula de pinocitosis", 13, weight=900, fill=INK)
    # mediada por receptor
    x = 680
    b += f'<path d="M{x - 110},140 L{x - 34},140 C{x - 34},190 {x + 34},190 {x + 34},140 L{x + 110},140" fill="none" stroke="{MEMB}" stroke-width="4"/>'
    for a in range(200, 341, 28):
        rx, ry = x + 34 * math.cos(math.radians(a)), 150 - 34 * math.sin(math.radians(a))
        b += f'<path d="M{rx:.1f},{ry:.1f} l-4,-8 m4,8 l4,-8" stroke="{LILA}" stroke-width="2.5"/>'
        b += f'<circle cx="{rx:.1f}" cy="{ry - 12:.1f}" r="4" fill="#ffd166" stroke="{INK}" stroke-width="1"/>'
    b += f'<circle cx="{x}" cy="235" r="22" fill="#fff" stroke="{MEMB}" stroke-width="3"/>'
    b += flecha(x, 192, x, 208) + text(x, 278, "receptores específicos", 13, weight=900, fill=INK)
    # exocitosis
    x = 950
    b += f'<path d="M{x - 110},140 L{x - 26},140 C{x - 26},120 {x + 26},120 {x + 26},140 L{x + 110},140" fill="none" stroke="{MEMB}" stroke-width="4"/>'
    for k in range(5):
        b += f'<circle cx="{x - 14 + k * 7}" cy="{110 - (k % 2) * 8}" r="3" fill="{VERDE}"/>'
    b += f'<circle cx="{x}" cy="230" r="22" fill="#e5f4ec" stroke="{MEMB}" stroke-width="3"/>'
    for k in range(4):
        b += f'<circle cx="{x - 9 + k * 6}" cy="{230 + (k % 2) * 5}" r="3" fill="{VERDE}"/>'
    b += flecha(x, 205, x, 160, VERDE) + text(x, 272, "vesícula de secreción", 13, weight=900, fill=INK)
    b += text(560, 380, "Endocitosis: la membrana se invagina y forma una vesícula hacia dentro · Exocitosis: una vesícula se fusiona con la membrana", 14, weight=900, fill=PRI)
    save("endocitosis-exocitosis.svg", svg(1100, 400, b, "Tipos de endocitosis y exocitosis"))


# ---------------------------------------------------------------- orgánulos
def endomembranas():
    b = f'<path d="M20,60 L20,40 Q20,20 40,20 L1060,20 Q1080,20 1080,40 L1080,60" fill="none" stroke="{MEMB}" stroke-width="5"/>'
    b += text(550, 14, "membrana plasmática", 13, weight=900, fill=MEMB)
    b += f'<path d="M20,420 A150,150 0 0 1 20,120" fill="#dfe8f5" stroke="#3b5f8f" stroke-width="5"/>' + text(60, 270, "núcleo", 16, "start", 900, fill="#3b5f8f")
    b += rer(200, 180, 180, 5, 1.1)
    b += text(290, 290, "RER", 18, weight=900, fill="#7b5ea7") + text(290, 310, "síntesis de proteínas", 13, weight=800, fill=GRIS) + text(290, 326, "de membrana y de secreción", 13, weight=800, fill=GRIS)
    b += rel(200, 400, 1.1) + text(290, 450, "REL: lípidos, detoxificación", 13, weight=800, fill="#9b7fc9")
    b += flecha(400, 200, 480, 200) + text(440, 190, "vesícula", 12, weight=800, fill=GRIS)
    b += f'<circle cx="460" cy="200" r="8" fill="#e8dff5" stroke="#7b5ea7" stroke-width="2"/>'
    b += golgi(580, 210, 1.5)
    b += text(580, 140, "cara cis", 13, weight=900, fill=ACC) + text(580, 290, "cara trans", 13, weight=900, fill=ACC)
    b += text(580, 320, "Golgi: maduración, glucosilación,", 13, weight=800, fill=GRIS) + text(580, 336, "clasificación y empaquetado", 13, weight=800, fill=GRIS)
    # salidas
    b += flecha(650, 240, 760, 110) + f'<circle cx="790" cy="90" r="16" fill="#e5f4ec" stroke="{VERDE}" stroke-width="2.5"/>'
    b += flecha(800, 72, 820, 46, VERDE) + text(850, 100, "vesícula de secreción → exocitosis", 13, "start", 900, fill=VERDE)
    b += flecha(660, 260, 760, 220) + f'<circle cx="784" cy="215" r="14" fill="#cfe3f5" stroke="{MEMB}" stroke-width="2.5"/>' + text(810, 220, "proteínas de membrana", 13, "start", 900, fill=MEMB)
    b += flecha(650, 280, 760, 340) + f'<circle cx="790" cy="350" r="20" fill="#f3b8c8" stroke="#b03a5b" stroke-width="2.5"/>' + text(820, 345, "lisosoma (hidrolasas)", 13, "start", 900, fill="#b03a5b")
    # fagosoma + lisosoma
    b += f'<circle cx="960" cy="420" r="22" fill="#fff" stroke="{MEMB}" stroke-width="2.5"/><rect x="948" y="412" width="24" height="14" rx="7" fill="#8ab17d"/>'
    b += flecha(812, 362, 930, 410) + text(1000, 462, "+ fagosoma → digestión (heterofagia)", 13, "end", 800, fill=GRIS)
    save("sistema-endomembranas.svg", svg(1100, 480, b, "Sistema de endomembranas: retículo, complejo de Golgi, vesículas y lisosomas"))


def mitocondria_grande():
    cx, cy, RX, RY, rx, ry = 520, 210, 300, 140, 284, 124
    b = f'<ellipse cx="{cx}" cy="{cy}" rx="{RX}" ry="{RY}" fill="#f6c7a8" stroke="#b5532c" stroke-width="4"/>'
    b += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fbe3d3" stroke="#b5532c" stroke-width="3"/>'
    crestas = []
    for k in range(9):
        x = cx - 230 + k * 57.5
        top = k % 2 == 0
        yt = cy - ry * math.sqrt(max(0, 1 - ((x - cx) / rx) ** 2))
        yb = cy + ry * math.sqrt(max(0, 1 - ((x - cx) / rx) ** 2))
        d = 0.62 * (yb - yt)
        if top:
            b += f'<path d="M{x - 9:.1f},{yt - 2:.1f} L{x - 9:.1f},{yt + d:.1f} Q{x:.1f},{yt + d + 14:.1f} {x + 9:.1f},{yt + d:.1f} L{x + 9:.1f},{yt - 2:.1f}" fill="#f6c7a8" stroke="#b5532c" stroke-width="3"/>'
            crestas.append((x, yt + d * 0.5, 1))
        else:
            b += f'<path d="M{x - 9:.1f},{yb + 2:.1f} L{x - 9:.1f},{yb - d:.1f} Q{x:.1f},{yb - d - 14:.1f} {x + 9:.1f},{yb - d:.1f} L{x + 9:.1f},{yb + 2:.1f}" fill="#f6c7a8" stroke="#b5532c" stroke-width="3"/>'
            crestas.append((x, yb - d * 0.5, -1))
    # ATP sintasas en la cara de la matriz de una cresta
    x0, y0, _ = crestas[2]
    for k in range(4):
        b += linea(x0 + 9, y0 - 30 + k * 18, x0 + 16, y0 - 30 + k * 18, "#6d3fc0", 2) + f'<circle cx="{x0 + 19}" cy="{y0 - 30 + k * 18}" r="4" fill="#6d3fc0"/>'
    b += f'<path d="M{cx - 40},{cy + 10} c15,-25 35,20 50,0 s25,-20 40,5 s-20,30 -45,20 s-35,0 -45,-25z" fill="none" stroke="#1f5f99" stroke-width="3"/>'
    b += ribos([(cx + 70, cy + 40), (cx + 84, cy + 50), (cx + 96, cy + 38), (cx + 60, cy - 50)], 4)
    a = math.radians(205)
    L = [(cx + RX * math.cos(a), cy + RY * math.sin(a), 180, 70, "membrana externa"),
         (cx - (RX + rx) / 2, cy, 180, 150, "espacio intermembrana"),
         (cx + rx * math.cos(math.radians(155)), cy + ry * math.sin(math.radians(155)), 180, 230, "membrana interna"),
         (crestas[0][0], crestas[0][1], 180, 320, "cresta mitocondrial"),
         (x0 + 19, y0 - 12, 880, 60, "ATP sintasa"),
         (cx + 130, cy - 10, 880, 150, "matriz"),
         (cx + 10, cy - 8, 880, 240, "ADN mitocondrial (circular)"),
         (cx + 84, cy + 50, 880, 330, "ribosomas mitocondriales")]
    for x, y, tx, ty, t in L:
        b += et(x, y, tx, ty, t, INK, 15)
    save("mitocondria.svg", svg(1100, 400, b, "Estructura de la mitocondria"))


def cloroplasto_grande():
    b = f'<ellipse cx="330" cy="200" rx="290" ry="140" fill="#bfe3b4" stroke="#2f7d32" stroke-width="4"/>'
    b += f'<ellipse cx="330" cy="200" rx="280" ry="130" fill="#e3f3dc" stroke="#2f7d32" stroke-width="2"/>'
    for k, gx in enumerate((150, 260, 380, 500)):
        for j in range(7):
            b += f'<rect x="{gx - 30}" y="{160 + j * 11 - (k % 2) * 10}" width="60" height="8" rx="4" fill="#3f9142" stroke="#256b28" stroke-width="1"/>'
        if k < 3:
            b += linea(gx + 30, 196, gx + 80, 196, "#3f9142", 3)
    b += f'<path d="M420,280 C450,250 480,300 510,270" fill="none" stroke="#1f5f99" stroke-width="3"/>'
    b += ribos([(200, 280), (220, 290), (240, 276), (330, 110)], 4)
    b += f'<ellipse cx="330" cy="290" rx="26" ry="14" fill="#fff" stroke="#9aa7b2" stroke-width="1.5"/>'
    L = [(330, 60, 700, 50, "membrana externa"), (330, 72, 700, 90, "membrana interna"), (380, 170, 700, 140, "grana"),
         (380, 160, 700, 180, "tilacoide"), (440, 196, 700, 220, "tilacoide del estroma (lamela)"), (400, 130, 700, 260, "estroma"),
         (465, 280, 700, 300, "ADN del cloroplasto (circular)"), (220, 290, 700, 340, "ribosomas 70S"), (330, 290, 120, 370, "gránulo de almidón")]
    for x, y, tx, ty, s in L:
        b += et(x, y, tx, ty, s, INK, 15)
    save("cloroplasto.svg", svg(1110, 390, '<g transform="translate(150,0)">' + b + "</g>", "Estructura del cloroplasto"))


def nucleo_grande():
    b = nucleo(300, 220, 180)
    b += rer(480, 120, 150, 3)
    # las cisternas del RER nacen de la membrana externa de la envoltura
    for k in range(3):
        yy = 120 + k * 14
        xe = 300 + math.sqrt(180 ** 2 - (yy - 220) ** 2)
        b += f'<path d="M{xe - 2:.1f},{yy} H482" fill="none" stroke="#7b5ea7" stroke-width="5" stroke-linecap="round"/>'
    L = [(300, 40, 600, 40, "envoltura nuclear (doble membrana)"), (134, 281, 20, 200, "poro nuclear"), (350, 180, 600, 200, "nucléolo"),
         (200, 270, 20, 300, "cromatina"), (300, 330, 600, 330, "nucleoplasma"), (520, 116, 600, 90, "RER (continuo con la envoltura)")]
    for x, y, tx, ty, s in L:
        b += et(x, y, tx, ty, s, INK, 15)
    save("nucleo-interfasico.svg", svg(1060, 420, '<g transform="translate(170,0)">' + b + "</g>", "Núcleo interfásico"))


def citoesqueleto():
    b = ""
    # microfilamento: doble hélice de esferas
    b += text(170, 34, "Microfilamentos (actina)", 16, weight=900, fill=ROJO) + text(170, 52, "≈ 7 nm", 13, weight=800, fill=GRIS)
    for k in range(14):
        x = 40 + k * 19
        b += f'<circle cx="{x}" cy="{90 + 8 * math.sin(k * 0.9)}" r="9" fill="#f4a3a3" stroke="{ROJO}" stroke-width="1.2"/>'
        b += f'<circle cx="{x + 9}" cy="{90 - 8 * math.sin(k * 0.9)}" r="9" fill="#e76f51" stroke="{ROJO}" stroke-width="1.2"/>'
    b += text(170, 140, "forma, microvellosidades, movimiento", 12, weight=800, fill=GRIS) + text(170, 156, "ameboide, contracción, anillo de la citocinesis", 12, weight=800, fill=GRIS)
    # intermedios
    b += text(500, 34, "Filamentos intermedios", 16, weight=900, fill=ACC) + text(500, 52, "≈ 10 nm", 13, weight=800, fill=GRIS)
    for k in range(4):
        b += f'<path d="M380,{78 + k * 7} C430,{68 + k * 7} 470,{98 + k * 7} 520,{78 + k * 7} S600,{68 + k * 7} 620,{82 + k * 7}" fill="none" stroke="{ACC}" stroke-width="4"/>'
    b += text(500, 140, "resistencia mecánica", 12, weight=800, fill=GRIS) + text(500, 156, "(queratina, neurofilamentos)", 12, weight=800, fill=GRIS)
    # microtúbulos
    b += text(830, 34, "Microtúbulos (tubulina α y β)", 16, weight=900, fill=PRI) + text(830, 52, "≈ 25 nm, huecos", 13, weight=800, fill=GRIS)
    for j in range(3):
        for k in range(10):
            b += f'<rect x="{710 + k * 24}" y="{70 + j * 14}" width="22" height="12" rx="4" fill="{"#7fb3e6" if (k + j) % 2 else "#2a7fc1"}"/>'
    b += text(830, 140, "huso mitótico, transporte de vesículas,", 12, weight=800, fill=GRIS) + text(830, 156, "centriolos, cilios y flagelos", 12, weight=800, fill=GRIS)
    # centriolo 9x3 y axonema 9+2
    def anillo(cx, cy, n, R, triple):
        s = ""
        for k in range(9):
            a = math.radians(k * 40 - 90)
            for t in range(n):
                rr = R + (t - (n - 1) / 2) * 0
                x = cx + R * math.cos(a) + (t - (n - 1) / 2) * 11 * math.cos(a + math.pi / 2 - 0.6)
                y = cy + R * math.sin(a) + (t - (n - 1) / 2) * 11 * math.sin(a + math.pi / 2 - 0.6)
                s += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="5.5" fill="#2a7fc1" stroke="#16466e" stroke-width="1"/>'
        return s
    b += anillo(220, 270, 3, 62, True) + text(220, 370, "Centriolo: 9 tripletes (9 × 3 + 0)", 15, weight=900, fill=PRI)
    b += text(220, 390, "en el centrosoma y como corpúsculo basal", 12, weight=800, fill=GRIS)
    b += f'<circle cx="640" cy="270" r="80" fill="#eef4fa" stroke="{MEMB}" stroke-width="3"/>'
    b += anillo(640, 270, 2, 58, False)
    b += f'<circle cx="632" cy="270" r="6" fill="#2a7fc1"/><circle cx="648" cy="270" r="6" fill="#2a7fc1"/>'
    b += text(640, 370, "Axonema de cilios y flagelos: 9 + 2", 15, weight=900, fill=PRI)
    b += text(640, 390, "9 dobletes periféricos + 2 microtúbulos centrales", 12, weight=800, fill=GRIS)
    b += text(900, 260, "membrana", 12, "start", 800, fill=MEMB) + linea(895, 256, 720, 262, GRIS, 1.2)
    save("citoesqueleto.svg", svg(1040, 410, b, "Componentes del citoesqueleto, centriolo y axonema"))


def ribosomas():
    def ribo(cx, cy, s, gr, pe, col, tot):
        r1, r2 = 40 * s, 28 * s
        o = f'<ellipse cx="{cx}" cy="{cy - r2 * 0.6}" rx="{r1}" ry="{r1 * 0.72}" fill="{col}" stroke="{INK}" stroke-width="2"/>'
        o += f'<ellipse cx="{cx}" cy="{cy + r1 * 0.55}" rx="{r2 * 1.1}" ry="{r2 * 0.6}" fill="#fff" stroke="{INK}" stroke-width="2"/>'
        o += text(cx, cy - r2 * 0.5, gr, 15, weight=900) + text(cx, cy + r1 * 0.6, pe, 14, weight=900)
        o += text(cx, cy + r1 * 1.4, tot, 20, weight=900, fill=PRI)
        return o
    b = ribo(170, 120, 1.25, "60S", "40S", "#cfe3f5", "80S")
    b += text(170, 250, "citosol de eucariotas", 14, weight=900, fill=INK) + text(170, 268, "(libres, en el RER y la envoltura)", 12, weight=800, fill=GRIS)
    b += ribo(450, 120, 1.0, "50S", "30S", "#e5f4ec", "70S")
    b += text(450, 250, "bacterias y cloroplastos", 14, weight=900, fill=INK)
    b += ribo(700, 120, 0.9, "39S", "28S", "#fbe3d3", "≈ 55S")
    b += text(700, 250, "mitocondrias (mamíferos)", 14, weight=900, fill=INK) + text(700, 268, "más parecidos a los bacterianos", 12, weight=800, fill=GRIS)
    b += text(440, 310, "Los antibióticos que bloquean los ribosomas bacterianos pueden afectar también a los de mitocondrias y cloroplastos.", 13, weight=800, fill=ROJO)
    b += text(440, 330, "S = unidad Svedberg (velocidad de sedimentación): no se suman (60S + 40S = 80S).", 13, weight=800, fill=GRIS)
    save("ribosomas.svg", svg(880, 345, b, "Ribosomas 80S, 70S y mitocondriales"))


def endosimbiosis():
    b = ""
    def cel(cx, cy, r, col="#fdf3e7"):
        return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{col}" stroke="{MEMB}" stroke-width="3.5"/>'
    b += cel(110, 170, 70) + f'<circle cx="110" cy="170" r="22" fill="#dfe8f5" stroke="#3b5f8f" stroke-width="3"/>'
    b += text(110, 270, "célula ancestral", 13, weight=900) + text(110, 286, "(con núcleo, anaerobia)", 12, weight=800, fill=GRIS)
    b += f'<rect x="210" y="80" width="54" height="26" rx="13" fill="#f6c7a8" stroke="#b5532c" stroke-width="2.5"/>' + text(237, 70, "bacteria aerobia", 12, weight=900, fill="#b5532c")
    b += flecha(225, 110, 170, 140)
    b += cel(380, 170, 80) + f'<circle cx="370" cy="160" r="24" fill="#dfe8f5" stroke="#3b5f8f" stroke-width="3"/>' + mitocondria(420, 215, 46, 22, 10) + mitocondria(340, 220, 40, 20, -20)
    b += text(380, 280, "eucariota heterótrofa", 13, weight=900) + text(380, 296, "(con mitocondrias: animales, hongos)", 12, weight=800, fill=GRIS)
    b += flecha(190, 170, 290, 170)
    b += f'<rect x="510" y="70" width="54" height="26" rx="13" fill="#bfe3b4" stroke="#2f7d32" stroke-width="2.5"/>' + text(537, 60, "cianobacteria", 12, weight=900, fill="#2f7d32")
    b += flecha(530, 100, 600, 140)
    b += flecha(470, 170, 580, 170)
    b += cel(680, 170, 85, "#f2f8ec") + f'<circle cx="660" cy="150" r="24" fill="#dfe8f5" stroke="#3b5f8f" stroke-width="3"/>' + mitocondria(720, 215, 42, 20, 0) + cloroplasto(650, 220, 52, 24, 10) + cloroplasto(725, 130, 48, 22, -30)
    b += text(680, 280, "eucariota autótrofa", 13, weight=900) + text(680, 296, "(con cloroplastos: algas, plantas)", 12, weight=800, fill=GRIS)
    pr = ["ADN propio, circular y sin histonas", "Doble membrana", "Se dividen por sí mismos (bipartición)", "Ribosomas parecidos a los bacterianos", "Tamaño similar al de una bacteria"]
    b += f'<rect x="820" y="40" width="260" height="230" rx="14" fill="#fff4df" stroke="{ACC}" stroke-width="2"/>' + text(950, 66, "Pruebas", 16, weight=900, fill=ACC)
    for k, p in enumerate(pr):
        b += text(834, 96 + k * 34, "✓ " + p, 12, "start", 800)
    save("endosimbiosis.svg", svg(1100, 310, b, "Teoría endosimbiótica del origen de mitocondrias y cloroplastos"))


def microscopios():
    cols = [("Óptico", "luz visible", "lentes de vidrio", ["ocular", "objetivo", "muestra", "condensador", "lámpara"], "#fff4df", ACC),
            ("Electrónico de transmisión (MET)", "haz de electrones", "lentes electromagnéticas", ["cañón de electrones", "lente condensadora", "corte ultrafino", "lente objetivo", "pantalla"], "#e3eef8", PRI),
            ("Electrónico de barrido (MEB)", "haz de electrones", "barre la superficie", ["cañón de electrones", "lentes", "bobinas de barrido", "muestra metalizada", "detector (lateral)"], "#efe7fb", LILA)]
    b = ""
    for i, (t, rad, len_, piezas, f, c) in enumerate(cols):
        x = 180 + i * 360
        b += f'<rect x="{x - 170}" y="10" width="340" height="420" rx="18" fill="{f}" stroke="{c}" stroke-width="2"/>'
        b += text(x, 40, t, 16, weight=900, fill=c)
        b += f'<rect x="{x - 40}" y="64" width="80" height="300" rx="10" fill="#fff" stroke="#9aa7b2" stroke-width="2"/>'
        ys = [90, 150, 210, 270, 330]
        for k, (y, p) in enumerate(zip(ys, piezas)):
            if "muestra" in p or "corte" in p:
                b += f'<rect x="{x - 30}" y="{y - 4}" width="60" height="8" fill="{ROJO}"/>'
            elif p in ("lámpara", "cañón de electrones"):
                b += f'<circle cx="{x}" cy="{y}" r="12" fill="#ffd166" stroke="{INK}"/>'
            elif p in ("pantalla", "detector"):
                b += f'<rect x="{x - 32}" y="{y - 8}" width="64" height="16" fill="#9be7a1" stroke="{INK}"/>'
            elif p == "bobinas de barrido":
                b += f'<rect x="{x - 36}" y="{y - 8}" width="16" height="16" fill="#c9b8ef" stroke="{INK}"/><rect x="{x + 20}" y="{y - 8}" width="16" height="16" fill="#c9b8ef" stroke="{INK}"/>'
            else:
                b += f'<ellipse cx="{x}" cy="{y}" rx="30" ry="9" fill="#cfe3f5" stroke="{INK}"/>'
            b += text(x + 48, y + 5, p, 11.5, "start", 800)
        b += text(x, 392, rad + " · " + len_, 13, weight=900, fill=c)
        b += text(x, 412, ["imagen en color; vivas o fijadas", "imagen 2D del interior; solo muertas", "imagen 3D de la superficie; solo muertas"][i], 12, weight=800, fill=GRIS)
    # recorrido de la radiación
    b += flecha(180, 316, 180, 104, ACC, 2) + flecha(540, 104, 540, 316, PRI, 2) + flecha(900, 104, 900, 260, LILA, 2)
    save("microscopios.svg", svg(1080, 440, b, "Microscopio óptico, electrónico de transmisión y electrónico de barrido"))


def escala():
    items = [("átomo", 0.1e-9), ("proteína", 5e-9), ("ribosoma", 25e-9), ("virus", 100e-9), ("bacteria", 2e-6), ("mitocondria", 2e-6), ("célula eucariota", 30e-6), ("óvulo humano", 120e-6)]
    x0, x1 = 60, 1000
    lo, hi = -10.5, -3
    def X(v):
        return x0 + (math.log10(v) - lo) / (hi - lo) * (x1 - x0)
    b = linea(x0, 150, x1, 150, INK, 3)
    for e, lab in ((-10, "0,1 nm"), (-9, "1 nm"), (-8, "10 nm"), (-7, "100 nm"), (-6, "1 µm"), (-5, "10 µm"), (-4, "100 µm"), (-3, "1 mm")):
        x = X(10 ** e)
        b += linea(x, 142, x, 158, INK, 2) + text(x, 178, lab, 13, weight=800, fill=GRIS)
    for k, (n, v) in enumerate(items):
        x = X(v)
        y = 120 - (k % 2) * 30
        b += f'<circle cx="{x:.1f}" cy="150" r="5" fill="{ROJO}"/>' + linea(x, 145, x, y + 6, GRIS, 1) + text(x, y, n, 13, weight=900)
    def banda(a, c_, y, t, col):
        return f'<rect x="{X(a):.1f}" y="{y}" width="{X(c_) - X(a):.1f}" height="22" rx="8" fill="{col}" opacity="0.85"/>' + text((X(a) + X(c_)) / 2, y + 16, t, 13, weight=900, fill="#fff")
    b += banda(0.2e-3, 1e-3, 200, "ojo", "#7b8a97")
    b += banda(0.2e-6, 0.2e-3, 230, "microscopio óptico (≥ 0,2 µm)", ACC)
    b += banda(0.2e-9, 0.2e-6, 260, "microscopio electrónico (≈ nm)", PRI)
    b += text(530, 310, "Límite de resolución: distancia mínima entre dos puntos para verlos separados (cuanto menor, mejor).", 13, weight=800, fill=GRIS)
    save("escala-microscopia.svg", svg(1060, 325, b, "Escala de tamaños y límites de resolución del ojo y los microscopios"))


if __name__ == "__main__":
    celula_animal(); celula_vegetal(); celula_procariota(); membrana(); transporte(); osmosis(); endocitosis()
    endomembranas(); mitocondria_grande(); cloroplasto_grande(); nucleo_grande(); citoesqueleto(); ribosomas(); endosimbiosis()
    microscopios(); escala()
