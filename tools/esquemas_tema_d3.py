# Esquemas SVG del tema D3 (fotosíntesis y quimiosíntesis) de BioCelia.
# Uso: python tools/esquemas_tema_d3.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "d3")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, LILA, ROJO, VERDE, TEAL = "#0f4c81", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a", "#2a9d8f"
ESTROMA, LUMEN, TIL = "#e3f3dc", "#f6fbe9", "#3f9142"
LUZ = "#e0a800"


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


def pastilla(x, y, t, col, fondo, size=13):
    w = 14 + len(t) * size * 0.62
    return f'<rect x="{x - w / 2}" y="{y - 14}" width="{w}" height="28" rx="14" fill="{fondo}" stroke="{col}" stroke-width="2"/>' + text(x, y + 5, t, size, weight=900, fill=col)


def rayo(x, y, L=60, ang=55):
    t = math.radians(ang)
    dx, dy = L * math.cos(t), L * math.sin(t)
    pts = [(x - dx, y - dy), (x - dx * 0.55 + 6, y - dy * 0.55 - 4), (x - dx * 0.45 - 6, y - dy * 0.45 + 4), (x, y)]
    d = "M" + " L".join(f"{a:.1f},{c:.1f}" for a, c in pts)
    return f'<path d="{d}" fill="none" stroke="{LUZ}" stroke-width="4" stroke-linejoin="round" marker-end="url(#fk)"/>'


# ---------------------------------------------------------------- esquema global
def global_():
    b = f'<ellipse cx="520" cy="270" rx="500" ry="250" fill="#bfe3b4" stroke="#2f7d32" stroke-width="5"/>'
    b += f'<ellipse cx="520" cy="270" rx="488" ry="238" fill="{ESTROMA}" stroke="#2f7d32" stroke-width="2"/>'
    b += text(520, 52, "CLOROPLASTO", 15, weight=900, fill="#2f7d32")
    # tilacoides (granum)
    for j in range(6):
        b += f'<rect x="140" y="{140 + j * 30}" width="200" height="22" rx="11" fill="{TIL}" stroke="#256b28" stroke-width="1.5"/>'
    b += text(240, 350, "TILACOIDES (granum)", 14, weight=900, fill="#256b28")
    b += text(240, 372, "FASE LUMINOSA", 17, weight=900, fill=PRI) + text(240, 392, "(fotoquímica)", 13, weight=800, fill=GRIS)
    b += rayo(170, 135, 70, 60) + text(110, 90, "LUZ", 16, weight=900, fill=LUZ)
    b += pastilla(90, 200, "H₂O", PRI, "#e3eef8") + flecha(112, 200, 136, 200, PRI, 2.5)
    b += pastilla(330, 120, "O₂", ROJO, "#fde8e6") + flecha(300, 140, 320, 134, ROJO, 2)
    # Calvin
    cx, cy = 760, 260
    b += f'<circle cx="{cx}" cy="{cy}" r="90" fill="#fff" stroke="{ACC}" stroke-width="6"/>' + text(cx, cy - 4, "CICLO DE", 15, weight=900, fill=ACC) + text(cx, cy + 18, "CALVIN", 20, weight=900, fill=ACC)
    b += text(cx - 80, 440, "ESTROMA · FASE BIOSINTÉTICA", 15, weight=900, fill=PRI) + text(cx - 80, 460, "(de fijación del carbono)", 13, weight=800, fill=GRIS)
    b += pastilla(cx, 120, "CO₂", GRIS, "#eef1f4") + flecha(cx, 134, cx, 166, GRIS, 2.5)
    b += pastilla(cx + 100, 398, "glúcidos (triosas → glucosa)", VERDE, "#e5f4ec", 12) + flecha(cx + 40, cy + 88, cx + 80, 382, VERDE, 2.5)
    # intercambio
    b += flecha(350, 220, 660, 220, LILA, 3.5) + text(505, 206, "ATP + NADPH", 15, weight=900, fill=LILA)
    b += flecha(660, 290, 350, 290, GRIS, 2.5) + text(505, 312, "ADP + Pi + NADP⁺", 13, weight=900, fill=GRIS)
    b += text(520, 495, "6 CO₂ + 6 H₂O + luz → C₆H₁₂O₆ + 6 O₂", 17, weight=900, fill=PRI)
    save("fotosintesis-global.svg", svg(1040, 530, b, "Esquema global de la fotosíntesis: fase luminosa en los tilacoides y ciclo de Calvin en el estroma"))


# ---------------------------------------------------------------- fase luminosa
def luminosa():
    W, H = 1300, 560
    b = f'<rect x="10" y="10" width="{W - 20}" height="150" rx="16" fill="{ESTROMA}"/>' + text(30, 40, "ESTROMA", 15, "start", 900, fill="#2f7d32")
    b += f'<rect x="10" y="300" width="{W - 20}" height="{H - 310}" rx="16" fill="{LUMEN}"/>' + text(30, H - 22, "LUMEN (espacio tilacoidal)", 15, "start", 900, fill="#2f7d32")
    for x in range(20, W - 20, 14):
        b += f'<circle cx="{x}" cy="172" r="6" fill="#9ccc7a"/><circle cx="{x}" cy="288" r="6" fill="#9ccc7a"/>'
        b += linea(x, 178, x, 225, "#c7d77a", 1.6) + linea(x, 235, x, 282, "#c7d77a", 1.6)
    b += text(W - 30, 324, "membrana del tilacoide", 13, "end", 900, fill="#256b28")
    comps = [(170, "PS II", 110, 150, "#7ec27a"), (420, "Cit b₆f", 80, 130, "#b9d3ee"), (640, "PS I", 100, 150, "#7ec27a")]
    for x, n, w, h, c in comps:
        b += f'<rect x="{x - w / 2}" y="{230 - h / 2}" width="{w}" height="{h}" rx="18" fill="{c}" stroke="#256b28" stroke-width="2.5"/>' + text(x, 200, n, 17, weight=900, fill="#1b4d1e")
    b += f'<ellipse cx="300" cy="258" rx="22" ry="14" fill="#ffe08a" stroke="{ACC}" stroke-width="2"/>' + text(300, 263, "PQ", 11, weight=900, fill="#8a5a00")
    b += f'<ellipse cx="530" cy="305" rx="22" ry="14" fill="#cfe3f5" stroke="{PRI}" stroke-width="2"/>' + text(530, 310, "PC", 11, weight=900, fill=PRI)
    b += f'<ellipse cx="770" cy="150" rx="24" ry="15" fill="#f6d6e0" stroke="{ROJO}" stroke-width="2"/>' + text(770, 155, "Fd", 12, weight=900, fill=ROJO)
    # luz
    b += rayo(140, 150, 80, 60) + rayo(610, 150, 80, 60) + text(80, 70, "luz", 15, weight=900, fill=LUZ) + text(550, 70, "luz", 15, weight=900, fill=LUZ)
    # electrones
    b += f'<path d="M200,270 C240,290 270,280 300,258 C330,236 380,240 420,250 C460,270 500,300 530,305 C570,300 610,280 640,250 C680,200 720,160 770,150" fill="none" stroke="{LILA}" stroke-width="3.5" stroke-dasharray="7 5" marker-end="url(#fk)"/>'
    b += text(460, 330, "e⁻", 15, weight=900, fill=LILA)
    # fotólisis
    b += pastilla(130, 400, "2 H₂O", PRI, "#e3eef8") + flecha(150, 385, 165, 310, PRI, 2.5)
    b += pastilla(130, 460, "O₂ + 4 H⁺", ROJO, "#fde8e6") + text(130, 494, "fotólisis del agua", 12, weight=900, fill=ROJO)
    # NADP+
    b += pastilla(870, 80, "NADP⁺ + H⁺", LILA, "#fff") + flecha(790, 140, 830, 100, LILA, 2.5) + pastilla(990, 80, "NADPH", LILA, "#efe7fb") + flecha(930, 80, 950, 80, LILA, 2)
    # bombeo de H+
    b += flecha(470, 150, 470, 330, ACC, 3) + text(486, 360, "H⁺", 15, "start", 900, fill=ACC)
    b += text(470, 132, "H⁺", 14, weight=900, fill=ACC)
    for k in range(8):
        b += text(260 + k * 60, 420 + (k % 2) * 18, "H⁺", 14, weight=900, fill=ACC)
    b += text(560, 480, "gradiente de protones (más H⁺ en el lumen)", 13, weight=900, fill=ACC)
    # ATP sintasa
    ax = 1110
    b += f'<rect x="{ax - 20}" y="160" width="40" height="140" rx="10" fill="#d9c8f5" stroke="{LILA}" stroke-width="2.5"/>'
    b += f'<rect x="{ax - 8}" y="110" width="16" height="50" fill="#d9c8f5" stroke="{LILA}" stroke-width="2"/>'
    b += f'<circle cx="{ax}" cy="80" r="0"/>'
    b += f'<ellipse cx="{ax}" cy="110" rx="44" ry="26" fill="#d9c8f5" stroke="{LILA}" stroke-width="2.5"/>' + text(ax, 106, "ATP", 12, weight=900, fill=LILA) + text(ax, 120, "sintasa", 12, weight=900, fill=LILA)
    b += flecha(ax, 440, ax, 140, ACC, 3.5) + text(ax + 14, 420, "H⁺", 15, "start", 900, fill=ACC)
    b += pastilla(ax + 100, 160, "ADP + Pi", ACC, "#fff") + flecha(ax + 70, 146, ax + 46, 124, ACC, 2)
    b += pastilla(ax + 110, 40, "ATP", ACC, "#fff4df") + flecha(ax + 34, 92, ax + 90, 50, ACC, 2.5)
    b += text(ax, 520, "FOTOFOSFORILACIÓN", 14, weight=900, fill=LILA)
    save("fase-luminosa.svg", svg(W, H, b, "Fase luminosa de la fotosíntesis en la membrana del tilacoide"))


def fotosistema():
    b = f'<ellipse cx="300" cy="190" rx="250" ry="150" fill="#e5f4ec" stroke="{TIL}" stroke-width="3"/>'
    for k in range(14):
        a = k * 2 * math.pi / 14
        x, y = 300 + 180 * math.cos(a), 190 + 100 * math.sin(a)
        col = "#3f9142" if k % 3 else "#f4a261"
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="14" fill="{col}" stroke="#256b28" stroke-width="1.5"/>'
        nx, ny = 300 + 110 * math.cos(a), 190 + 60 * math.sin(a)
        b += linea(x, y, nx, ny, LUZ, 1.6, 'stroke-dasharray="3 3"')
    b += f'<circle cx="300" cy="190" r="40" fill="#256b28" stroke="#123d14" stroke-width="3"/>' + text(300, 186, "centro de", 11, weight=900, fill="#fff") + text(300, 200, "reacción", 11, weight=900, fill="#fff")
    b += rayo(110, 70, 80, 50) + text(40, 30, "fotón", 14, weight=900, fill=LUZ)
    b += flecha(340, 190, 600, 190, LILA, 3.5) + text(470, 176, "e⁻ de alta energía", 13, weight=900, fill=LILA) + text(470, 212, "→ cadena de transporte", 12, weight=800, fill=GRIS)
    b += text(320, 368, "Los pigmentos antena (clorofilas, carotenoides) captan la luz", 13, weight=800, fill=GRIS)
    b += text(320, 388, "y pasan la energía al centro de reacción, cuya clorofila se excita", 13, weight=800, fill=GRIS)
    b += text(320, 408, "y cede un electrón. PS II: P680 · PS I: P700", 13, weight=800, fill=GRIS)
    save("fotosistema.svg", svg(640, 420, b, "Funcionamiento de un fotosistema: antena y centro de reacción"))


# ---------------------------------------------------------------- Calvin
def calvin():
    cx, cy, r = 420, 280, 150
    b = f'<rect x="10" y="10" width="1000" height="520" rx="24" fill="{ESTROMA}" stroke="#2f7d32" stroke-width="3"/>' + text(30, 42, "ESTROMA DEL CLOROPLASTO", 15, "start", 900, fill="#2f7d32")
    b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ACC}" stroke-width="10" opacity="0.85"/>'
    pasos = [(-60, "1 · FIJACIÓN", "CO₂ + ribulosa-1,5-bisfosfato", "enzima RuBisCO"), (60, "2 · REDUCCIÓN", "gasta ATP y NADPH", "→ triosas fosfato"), (180, "3 · REGENERACIÓN", "de la ribulosa", "gasta ATP")]
    for a, t1, t2, t3 in pasos:
        t = math.radians(a - 90)
        x, y = cx + (r + 4) * math.cos(t), cy + (r + 4) * math.sin(t)
        b += f'<rect x="{x - 105}" y="{y - 32}" width="210" height="64" rx="14" fill="#fff" stroke="{ACC}" stroke-width="2.5"/>'
        b += text(x, y - 10, t1, 14, weight=900, fill=ACC) + text(x, y + 8, t2, 12, weight=800) + text(x, y + 24, t3, 12, weight=800, fill=GRIS)
    b += text(cx, cy - 4, "CICLO DE", 18, weight=900, fill=ACC) + text(cx, cy + 22, "CALVIN", 24, weight=900, fill=ACC)
    b += pastilla(cx + 300, 90, "CO₂ (atmósfera)", GRIS, "#eef1f4") + flecha(cx + 250, 104, cx + 140, 140, GRIS, 2.5)
    b += pastilla(cx + 330, 300, "ATP + NADPH", LILA, "#efe7fb") + text(cx + 330, 330, "(de la fase luminosa)", 12, weight=800, fill=GRIS) + flecha(cx + 260, 300, cx + 200, 330, LILA, 2.5)
    b += pastilla(cx + 300, 420, "triosas fosfato → glucosa,", VERDE, "#e5f4ec", 12) + text(cx + 300, 450, "almidón, sacarosa, otras moléculas", 12, weight=800, fill=VERDE)
    b += flecha(cx + 150, 370, cx + 210, 410, VERDE, 2.5)
    b += pastilla(cx - 250, 430, "ADP + Pi + NADP⁺", GRIS, "#fff") + text(cx - 250, 460, "vuelven a la fase luminosa", 12, weight=800, fill=GRIS)
    b += text(510, 505, "Para una glucosa: 6 vueltas, 6 CO₂, 18 ATP y 12 NADPH", 16, weight=900, fill=PRI)
    save("ciclo-calvin.svg", svg(1020, 540, b, "Ciclo de Calvin: fijación, reducción y regeneración"))


# ---------------------------------------------------------------- factores
def factores():
    b = ""
    def ejes(x0, y0, w, h, tx, ty, tit):
        s = linea(x0, y0 + h, x0 + w, y0 + h, INK, 2) + linea(x0, y0 + h, x0, y0, INK, 2)
        s += text(x0 + w / 2, y0 + h + 26, tx, 13, weight=800, fill=GRIS)
        s += text(x0 - 16, y0 + h / 2, ty, 13, weight=800, fill=GRIS, style=f'transform="rotate(-90 {x0 - 16} {y0 + h / 2})"')
        s += text(x0 + w / 2, y0 - 14, tit, 15, weight=900, fill=PRI)
        return s
    # luz
    x0, y0, w, h = 50, 50, 260, 200
    b += ejes(x0, y0, w, h, "intensidad de luz", "fotosíntesis", "Luz")
    pts = [(x0 + t * w, y0 + h - h * 0.85 * (1 - math.exp(-t * 5))) for t in [k / 50 for k in range(51)]]
    b += f'<polyline points="{" ".join(f"{a:.1f},{c:.1f}" for a, c in pts)}" fill="none" stroke="{LUZ}" stroke-width="4"/>'
    b += text(x0 + w - 4, y0 + 18, "saturación", 12, "end", 900, fill=GRIS)
    # CO2
    x0 = 400
    b += ejes(x0, y0, w, h, "concentración de CO₂", "fotosíntesis", "CO₂")
    pts = [(x0 + t * w, y0 + h - h * 0.85 * (1 - math.exp(-t * 4))) for t in [k / 50 for k in range(51)]]
    b += f'<polyline points="{" ".join(f"{a:.1f},{c:.1f}" for a, c in pts)}" fill="none" stroke="{GRIS}" stroke-width="4"/>'
    b += text(x0 + w - 4, y0 + 18, "hasta un máximo", 12, "end", 900, fill=GRIS)
    # temperatura
    x0 = 750
    b += ejes(x0, y0, w, h, "temperatura", "fotosíntesis", "Temperatura")
    pts = []
    for k in range(51):
        t = k / 50
        v = math.exp(-((t - 0.62) / 0.2) ** 2) if t < 0.62 else math.exp(-((t - 0.62) / 0.09) ** 2)
        pts.append((x0 + t * w, y0 + h - h * 0.85 * v))
    b += f'<polyline points="{" ".join(f"{a:.1f},{c:.1f}" for a, c in pts)}" fill="none" stroke="{ROJO}" stroke-width="4"/>'
    b += text(x0 + 0.62 * w, y0 + 18, "óptima", 12, weight=900, fill=GRIS) + text(x0 + w - 6, y0 + h - 70, "enzimas", 11, "end", 900, fill=ROJO) + text(x0 + w - 6, y0 + h - 56, "desnaturalizadas", 11, "end", 900, fill=ROJO)
    b += text(530, 310, "También influyen el agua (sin agua se cierran los estomas y falta CO₂) y la concentración de O₂ (fotorrespiración).", 13, weight=800, fill=PRI)
    save("factores-fotosintesis.svg", svg(1060, 330, b, "Influencia de la luz, el CO2 y la temperatura en la fotosíntesis"))


# ---------------------------------------------------------------- quimiosíntesis
def quimio():
    b = f'<rect x="10" y="10" width="1000" height="360" rx="20" fill="#f6f2fb" stroke="{LILA}" stroke-width="2.5"/>'
    b += text(510, 44, "Quimiosíntesis: energía química de compuestos inorgánicos, sin luz", 18, weight=900, fill=LILA)
    b += f'<rect x="40" y="80" width="400" height="230" rx="16" fill="#fff" stroke="{LILA}" stroke-width="2"/>'
    b += text(240, 108, "1 · Oxidación de sustancias inorgánicas", 15, weight=900, fill=LILA)
    ej = [("NH₃ → NO₂⁻", "bacterias nitrosificantes (Nitrosomonas)"), ("NO₂⁻ → NO₃⁻", "bacterias nitrificantes (Nitrobacter)"), ("H₂S → S → SO₄²⁻", "bacterias incoloras del azufre"), ("Fe²⁺ → Fe³⁺", "bacterias del hierro")]
    for k, (r, n) in enumerate(ej):
        b += text(60, 146 + k * 40, r, 15, "start", 900, fill=INK) + text(60, 164 + k * 40, n, 12, "start", 800, fill=GRIS)
    b += flecha(450, 195, 560, 195, LILA, 3.5) + pastilla(505, 160, "ATP", ACC, "#fff4df") + pastilla(505, 232, "NADH", LILA, "#efe7fb")
    b += f'<rect x="580" y="80" width="400" height="230" rx="16" fill="#fff" stroke="{ACC}" stroke-width="2"/>'
    b += text(780, 108, "2 · Fijación del CO₂ (ciclo de Calvin)", 15, weight=900, fill=ACC)
    b += f'<circle cx="780" cy="200" r="58" fill="#fff" stroke="{ACC}" stroke-width="5"/>' + text(780, 196, "ciclo de", 13, weight=900, fill=ACC) + text(780, 214, "Calvin", 15, weight=900, fill=ACC)
    b += pastilla(640, 150, "CO₂", GRIS, "#eef1f4") + flecha(660, 160, 724, 182, GRIS, 2)
    b += pastilla(900, 270, "materia orgánica", VERDE, "#e5f4ec") + flecha(830, 236, 880, 258, VERDE, 2)
    b += text(510, 345, "Son bacterias quimioautótrofas: cierran ciclos biogeoquímicos (nitrógeno, azufre) y sostienen ecosistemas sin luz (fuentes hidrotermales).", 13, weight=800, fill=PRI)
    save("quimiosintesis.svg", svg(1020, 380, b, "Quimiosíntesis: oxidación de compuestos inorgánicos y fijación de CO2"))


if __name__ == "__main__":
    global_(); luminosa(); fotosistema(); calvin(); factores(); quimio()
