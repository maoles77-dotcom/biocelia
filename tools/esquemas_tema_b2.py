# Esquemas SVG del tema B2 (regulación de la expresión génica) de BioCelia.
# Uso: python tools/esquemas_tema_b2.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "b2")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO, VERDE = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"
ADN, ARN = "#1f5f99", "#8e44ad"


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


def tramo(x, w, y, t, col, fondo, tc="#fff", h=40, size=14):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="{fondo}" stroke="{col}" stroke-width="2"/>' + text(x + w / 2, y + h / 2 + 5, t, size, weight=900, fill=tc)


# ---------------------------------------------------------------- operón lac
def operon():
    def adn(y):
        s = linea(20, y + 20, 1060, y + 20, GRIS, 4)
        s += tramo(40, 120, y, "gen regulador", LILA, "#efe7fb", LILA, size=13)
        s += tramo(250, 100, y, "promotor", ACC, "#fff4df", ACC)
        s += tramo(352, 90, y, "operador", ROJO, "#fde8e6", ROJO)
        s += tramo(444, 220, y, "lacZ", ADN, ADN) + tramo(666, 180, y, "lacY", ADN, ADN) + tramo(848, 150, y, "lacA", ADN, ADN)
        s += text(721, y - 10, "genes estructurales", 14, weight=900, fill=ADN)
        return s

    def represor(cx, cy, activo=True):
        s = f'<path d="M{cx - 40},{cy + 18} L{cx - 40},{cy - 14} Q{cx - 40},{cy - 34} {cx - 20},{cy - 34} L{cx + 20},{cy - 34} Q{cx + 40},{cy - 34} {cx + 40},{cy - 14} L{cx + 40},{cy + 18} L{cx + 14},{cy + 18} L{cx + 14},{cy + 4} L{cx - 14},{cy + 4} L{cx - 14},{cy + 18}z" fill="#d9c8f5" stroke="{LILA}" stroke-width="2.5"' + ('' if activo else f' transform="rotate(-18 {cx} {cy})"') + '/>'
        return s + text(cx, cy - 10, "represor", 12, weight=900, fill=LILA)

    b = ""
    # Panel A: sin lactosa
    b += f'<rect x="10" y="10" width="1060" height="290" rx="18" fill="#f6f9fb" stroke="#d5dde3"/>'
    b += text(30, 44, "A · Sin lactosa: operón reprimido (apagado)", 20, "start", 900, fill=PRI)
    y = 200
    b += adn(y)
    b += flecha(100, y - 4, 100, 130) + text(110, 110, "ARNm → represor activo", 13, "start", 800, fill=LILA)
    b += represor(397, y - 22)
    b += f'<ellipse cx="290" cy="{y - 40}" rx="48" ry="32" fill="#d7ecd9" stroke="{VERDE}" stroke-width="2.5"/>' + text(290, y - 36, "ARN pol", 13, weight=900, fill=VERDE)
    b += text(560, 110, "El represor se une al operador:", 15, "start", 900, fill=ROJO)
    b += text(560, 132, "la ARN polimerasa no puede transcribir", 15, "start", 800, fill=ROJO)
    b += text(560, 154, "→ no se fabrican las enzimas", 15, "start", 800, fill=ROJO)
    b += linea(540, 160, 620, 160, ROJO, 0)
    # Panel B: con lactosa
    oy = 320
    b += f'<rect x="10" y="{oy}" width="1060" height="420" rx="18" fill="#fff" stroke="#d5dde3"/>'
    b += text(30, oy + 34, "B · Con lactosa: operón inducido (encendido)", 20, "start", 900, fill=PRI)
    y = oy + 190
    b += adn(y)
    b += flecha(100, y - 4, 100, oy + 120) + text(110, oy + 100, "ARNm → represor", 13, "start", 800, fill=LILA)
    # represor inactivado con inductor, separado
    b += represor(330, oy + 80, False)
    b += f'<circle cx="344" cy="{oy + 92}" r="11" fill="#f4a261" stroke="#b5651d" stroke-width="2"/>'
    b += text(400, oy + 84, "inductor (alolactosa):", 13, "start", 900, fill="#b5651d") + text(400, oy + 102, "el represor cambia de forma", 13, "start", 800, fill="#b5651d")
    b += text(400, oy + 120, "y se suelta del operador", 13, "start", 800, fill="#b5651d")
    b += f'<ellipse cx="560" cy="{y - 40}" rx="48" ry="32" fill="#d7ecd9" stroke="{VERDE}" stroke-width="2.5"/>' + text(560, y - 36, "ARN pol", 13, weight=900, fill=VERDE)
    b += flecha(612, y - 40, 680, y - 40, VERDE, 3)
    # ARNm policistrónico y proteínas
    my = y + 80
    b += linea(444, my, 1000, my, ARN, 6) + text(436, my + 5, "5'", 14, "end", 900, fill=ARN) + text(1008, my + 5, "3'", 14, "start", 900, fill=ARN)
    b += text(721, my - 12, "un solo ARNm policistrónico", 14, weight=900, fill=ARN)
    b += flecha(721, y + 44, 721, my - 26, ARN, 2.5)
    for cx, n, f in ((554, "β-galactosidasa", "hidroliza la lactosa"), (756, "permeasa", "la introduce en la célula"), (923, "transacetilasa", "")):
        b += flecha(cx, my + 8, cx, my + 44, GRIS, 2)
        b += f'<rect x="{cx - 80}" y="{my + 50}" width="160" height="{50 if f else 34}" rx="12" fill="#e5f4ec" stroke="{VERDE}" stroke-width="2"/>' + text(cx, my + 72, n, 14, weight=900, fill=VERDE)
        if f:
            b += text(cx, my + 90, f, 12, weight=800, fill=GRIS)
    save("operon-lac.svg", svg(1080, 750, b, "Operón lactosa: reprimido sin lactosa e inducido con lactosa"))


# ---------------------------------------------------------------- cromatina
def cromatina():
    b = text(260, 34, "Eucromatina", 22, weight=900, fill=VERDE) + text(780, 34, "Heterocromatina", 22, weight=900, fill=ROJO)
    # eucromatina: collar de perlas laxo con ARN pol
    pts = [(60 + i * 40, 170 + 40 * math.sin(i * 0.9)) for i in range(11)]
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    b += f'<path d="{d}" fill="none" stroke="{ADN}" stroke-width="4"/>'
    for x, y in pts[::2]:
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="#f4a261" stroke="#b5651d" stroke-width="1.8"/>'
    x, y = pts[5]
    b += f'<ellipse cx="{x:.1f}" cy="{y - 38:.1f}" rx="40" ry="24" fill="#d7ecd9" stroke="{VERDE}" stroke-width="2.5"/>' + text(x, y - 34, "ARN pol", 12, weight=900, fill=VERDE)
    b += text(260, 270, "Laxa, poco condensada", 16, weight=900, fill=VERDE)
    b += text(260, 294, "Accesible: genes ACTIVOS (se transcriben)", 15, weight=800)
    b += text(260, 318, "Zonas claras del núcleo al MET", 14, weight=800, fill=GRIS)
    # heterocromatina: nucleosomas apretados
    for fila in range(4):
        for col in range(7):
            cx = 650 + col * 34 + (17 if fila % 2 else 0)
            cy = 110 + fila * 30
            b += f'<circle cx="{cx}" cy="{cy}" r="15" fill="#f4a261" stroke="#b5651d" stroke-width="1.8"/>'
    b += f'<path d="M640,100 C700,90 760,130 900,100 M640,160 C720,150 780,190 910,160" fill="none" stroke="{ADN}" stroke-width="4" opacity="0.7"/>'
    b += f'<ellipse cx="960" cy="140" rx="40" ry="24" fill="#d7ecd9" stroke="{VERDE}" stroke-width="2.5" opacity="0.6"/>' + text(960, 144, "ARN pol", 12, weight=900, fill=VERDE)
    b += linea(930, 112, 990, 170, ROJO, 4) + linea(990, 112, 930, 170, ROJO, 4)
    b += text(780, 270, "Muy condensada", 16, weight=900, fill=ROJO)
    b += text(780, 294, "Inaccesible: genes INACTIVOS (no se transcriben)", 15, weight=800)
    b += text(780, 318, "Zonas oscuras (junto a la envoltura nuclear)", 14, weight=800, fill=GRIS)
    b += linea(520, 50, 520, 330, "#d5dde3", 2)
    save("eucromatina-heterocromatina.svg", svg(1040, 345, b, "Eucromatina laxa y activa frente a heterocromatina condensada e inactiva"))


def nucleo():
    b = f'<circle cx="230" cy="210" r="180" fill="#eef4fa" stroke="{PRI}" stroke-width="6" stroke-dasharray="30 7"/>'
    import random
    random.seed(4)
    for k in range(26):
        a = random.uniform(0, 2 * math.pi)
        if -0.3 < (a + math.pi) % (2 * math.pi) - math.pi < 0.9:
            continue  # deja libre el lado derecho por donde pasan las etiquetas
        r = random.uniform(150, 166)
        b += f'<ellipse cx="{230 + r * math.cos(a):.1f}" cy="{210 + r * math.sin(a):.1f}" rx="{random.uniform(12, 22):.1f}" ry="{random.uniform(7, 11):.1f}" transform="rotate({math.degrees(a) + 90:.0f} {230 + r * math.cos(a):.1f} {210 + r * math.sin(a):.1f})" fill="#3b4a5a"/>'
    for cx, cy in ((150, 150), (130, 250), (190, 310)):
        b += f'<ellipse cx="{cx}" cy="{cy}" rx="22" ry="14" fill="#3b4a5a"/>'
    b += f'<circle cx="250" cy="180" r="40" fill="#8d97a3" stroke="#55606c" stroke-width="2"/>'
    b += text(470, 70, "heterocromatina", 16, "start", 900, fill=ROJO) + linea(465, 66, 358, 100, GRIS, 1.5, 'stroke-dasharray="4 3"')
    b += text(470, 300, "eucromatina", 16, "start", 900, fill=VERDE) + linea(465, 296, 330, 285, GRIS, 1.5, 'stroke-dasharray="4 3"')
    b += text(470, 210, "nucleolo", 16, "start", 900, fill=GRIS) + linea(465, 206, 288, 190, GRIS, 1.5, 'stroke-dasharray="4 3"')
    b += text(470, 370, "envoltura nuclear", 16, "start", 900, fill=PRI) + linea(465, 366, 360, 336, GRIS, 1.5, 'stroke-dasharray="4 3"')
    save("nucleo-cromatina.svg", svg(660, 410, b, "Núcleo interfásico con eucromatina clara y heterocromatina oscura"))


# ---------------------------------------------------------------- niveles
def niveles():
    pasos = [("Cromatina", "ADN del núcleo", ADN, "#e3eef8"), ("Transcrito primario", "pre-ARNm", ARN, "#f1e6f8"),
             ("ARNm maduro", "sale al citoplasma", ARN, "#f1e6f8"), ("Proteína", "", VERDE, "#e5f4ec"), ("Proteína activa", "", VERDE, "#e5f4ec")]
    regs = [("1 · Condensación de la cromatina", "eucromatina / heterocromatina", True),
            ("2 · Transcripción", "factores de transcripción", True),
            ("3 · Maduración del ARNm", "empalme alternativo", True),
            ("4 · Traducción", "", False)]
    b = ""
    x0, w, gap = 20, 170, 70
    for i, (t, s, c, f) in enumerate(pasos):
        x = x0 + i * (w + gap)
        b += f'<rect x="{x}" y="60" width="{w}" height="70" rx="14" fill="{f}" stroke="{c}" stroke-width="2.5"/>' + text(x + w / 2, 92, t, 16, weight=900, fill=c)
        if s:
            b += text(x + w / 2, 114, s, 12, weight=800, fill=GRIS)
        if i < 4:
            b += flecha(x + w + 4, 95, x + w + gap - 6, 95)
            col = ROJO if regs[i][2] else "#9aa7b2"
            cx = x + w + gap / 2
            b += f'<circle cx="{cx}" cy="95" r="0"/>'
            b += linea(cx, 140, cx, 172, col, 2, 'stroke-dasharray="4 3"')
            b += f'<rect x="{cx - 112}" y="174" width="224" height="{56 if regs[i][1] else 40}" rx="10" fill="{"#fde8e6" if regs[i][2] else "#eef1f4"}" stroke="{col}" stroke-width="2"/>'
            b += text(cx, 197, regs[i][0], 13, weight=900, fill=col)
            if regs[i][1]:
                b += text(cx, 218, regs[i][1], 12, weight=800, fill=GRIS)
    b += text(x0 + 4 * (w + gap) + w / 2, 152, "(después: modificaciones,", 12, weight=800, fill="#9aa7b2") + text(x0 + 4 * (w + gap) + w / 2, 168, "degradación…)", 12, weight=800, fill="#9aa7b2")
    b += text(600, 30, "Niveles de regulación de la expresión génica en eucariotas", 18, weight=900, fill=PRI)
    b += text(600, 268, "En rojo, los niveles que piden las directrices 26-27; en gris, otros niveles.", 13, weight=800, fill=GRIS)
    save("niveles-regulacion.svg", svg(1200, 285, b, "Niveles de regulación de la expresión génica en eucariotas"))


def empalme():
    b = text(30, 34, "Un gen, varias proteínas: empalme alternativo", 20, "start", 900, fill=PRI)
    y = 60
    b += text(30, y + 26, "pre-ARNm", 15, "start", 900, fill=ARN)
    x = 140
    xs = {}
    for t, w in [("E1", 90), ("I", 50), ("E2", 90), ("I", 50), ("E3", 90), ("I", 50), ("E4", 90)]:
        ex = t[0] == "E"
        b += tramo(x, w, y, t, ARN if ex else "#9aa7b2", ARN if ex else "#e9edf0", "#fff" if ex else GRIS)
        if ex:
            xs[t] = x
        x += w + 2
    b += flecha(330, 112, 220, 170) + flecha(500, 112, 610, 170)
    for k, (ox, exs, nombre) in enumerate(((60, ["E1", "E2", "E4"], "Proteína A"), (500, ["E1", "E3", "E4"], "Proteína B"))):
        x = ox
        for e in exs:
            b += tramo(x, 90, 180, e, ARN, ARN)
            x += 92
        b += flecha(ox + 138, 228, ox + 138, 262)
        b += f'<rect x="{ox + 58}" y="268" width="160" height="40" rx="14" fill="#e5f4ec" stroke="{VERDE}" stroke-width="2.5"/>' + text(ox + 138, 294, nombre, 16, weight=900, fill=VERDE)
    b += text(470, 340, "Según el tipo de célula se conservan unos exones u otros (los intrones siempre se eliminan).", 14, weight=800, fill=GRIS)
    save("empalme-alternativo.svg", svg(940, 360, b, "Empalme alternativo: un mismo pre-ARNm origina dos ARNm y dos proteínas"))


# ---------------------------------------------------------------- diferenciación
def diferenciacion():
    celulas = [("Hepatocito", "#f6d6c4", "#b5651d"), ("Célula β del páncreas", "#f5e6b8", ACC), ("Fibra muscular", "#f6d6e0", ROJO)]
    genes = [("Enzimas de la glucólisis", [1, 1, 1]), ("Albúmina", [1, 0, 0]), ("Insulina", [0, 1, 0]), ("Actina y miosina musculares", [0, 0, 1]), ("Hemoglobina", [0, 0, 0])]
    b = text(520, 30, "Todas tienen el mismo genoma; cada una expresa genes distintos", 18, weight=900, fill=PRI)
    for i, (n, f, c) in enumerate(celulas):
        cx = 420 + i * 220
        if i == 0:
            b += f'<polygon points="{cx - 46},{90} {cx},{64} {cx + 46},{90} {cx + 46},{140} {cx},{166} {cx - 46},{140}" fill="{f}" stroke="{c}" stroke-width="3"/>'
        elif i == 1:
            b += f'<ellipse cx="{cx}" cy="115" rx="48" ry="46" fill="{f}" stroke="{c}" stroke-width="3"/>'
            for k in range(6):
                b += f'<circle cx="{cx - 22 + (k % 3) * 22}" cy="{100 + (k // 3) * 34}" r="5" fill="{c}"/>'
        else:
            b += f'<rect x="{cx - 80}" y="95" width="160" height="40" rx="20" fill="{f}" stroke="{c}" stroke-width="3"/>'
            for k in range(9):
                b += linea(cx - 64 + k * 16, 100, cx - 64 + k * 16, 130, c, 1.5)
        b += f'<circle cx="{cx}" cy="115" r="14" fill="#cfe0f2" stroke="{PRI}" stroke-width="2"/>' if i != 2 else f'<ellipse cx="{cx - 40}" cy="115" rx="10" ry="7" fill="#cfe0f2" stroke="{PRI}" stroke-width="2"/><ellipse cx="{cx + 40}" cy="115" rx="10" ry="7" fill="#cfe0f2" stroke="{PRI}" stroke-width="2"/>'
        b += text(cx, 196, n, 15, weight=900, fill=c)
    y0 = 220
    for j, (g, v) in enumerate(genes):
        y = y0 + j * 40
        b += f'<rect x="20" y="{y}" width="1060" height="40" fill="{"#f6f9fb" if j % 2 == 0 else "#fff"}"/>'
        b += text(36, y + 26, g, 15, "start", 900, fill=INK)
        for i, on in enumerate(v):
            cx = 420 + i * 220
            if on:
                b += f'<rect x="{cx - 52}" y="{y + 8}" width="104" height="24" rx="12" fill="#e5f4ec" stroke="{VERDE}" stroke-width="2"/>' + text(cx, y + 25, "se expresa", 12, weight=900, fill=VERDE)
            else:
                b += f'<rect x="{cx - 52}" y="{y + 8}" width="104" height="24" rx="12" fill="#eef1f4" stroke="#9aa7b2" stroke-width="2"/>' + text(cx, y + 25, "silenciado", 12, weight=900, fill=GRIS)
    b += text(36, y0 + 5 * 40 + 28, "Genes de mantenimiento (glucólisis): en todas las células · Genes específicos: solo en un tipo celular.", 14, "start", 800, fill=GRIS)
    save("diferenciacion-celular.svg", svg(1100, y0 + 5 * 40 + 46, b, "Diferenciación celular por expresión diferencial de genes"))


if __name__ == "__main__":
    operon(); cromatina(); nucleo(); niveles(); empalme(); diferenciacion()
