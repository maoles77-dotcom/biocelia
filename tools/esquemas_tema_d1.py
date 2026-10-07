# Esquemas SVG del tema D1 (nutrición celular y metabolismo) de BioCelia.
# Uso: python tools/esquemas_tema_d1.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "d1")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, LILA, ROJO, VERDE, TEAL = "#0f4c81", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a", "#2a9d8f"
CITO, MITO = "#fdf3e7", "#fbe3d3"


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


# ---------------------------------------------------------------- tipos de nutrición
def tipos():
    b = ""
    x0, y0, cw, ch = 220, 70, 380, 170
    b += text(x0 + cw, 30, "Fuente de carbono", 18, weight=900, fill=PRI)
    b += text(x0 + cw / 2, 58, "CO₂ → AUTÓTROFOS", 16, weight=900, fill=VERDE) + text(x0 + cw * 1.5, 58, "materia orgánica → HETERÓTROFOS", 16, weight=900, fill=ACC)
    b += text(40, y0 + ch, "Fuente de energía", 18, weight=900, fill=PRI, style=f'transform="rotate(-90 40 {y0 + ch})"')
    b += text(150, y0 + ch / 2 - 6, "LUZ", 16, weight=900, fill="#c49a00") + text(150, y0 + ch / 2 + 14, "fotótrofos", 14, weight=800, fill=GRIS)
    b += text(150, y0 + ch * 1.5 - 6, "REACCIONES", 15, weight=900, fill=LILA) + text(150, y0 + ch * 1.5 + 14, "QUÍMICAS", 15, weight=900, fill=LILA) + text(150, y0 + ch * 1.5 + 32, "quimiótrofos", 14, weight=800, fill=GRIS)
    celdas = [("Fotoautótrofos", "luz + CO₂", "plantas, algas, cianobacterias", "#e5f4ec", VERDE),
              ("Fotoheterótrofos", "luz + materia orgánica", "algunas bacterias (bacterias purpúreas no del azufre)", "#fff4df", ACC),
              ("Quimioautótrofos", "oxidación de sustancias inorgánicas + CO₂", "bacterias nitrificantes, del azufre, del hierro", "#efe7fb", LILA),
              ("Quimioheterótrofos", "oxidación de materia orgánica", "animales, hongos, protozoos, la mayoría de bacterias", "#fdecea", ROJO)]
    for k, (t, e, ej, f, c) in enumerate(celdas):
        r, col = divmod(k, 2)
        x, y = x0 + col * cw, y0 + r * ch
        b += f'<rect x="{x + 6}" y="{y + 6}" width="{cw - 12}" height="{ch - 12}" rx="16" fill="{f}" stroke="{c}" stroke-width="2.5"/>'
        b += text(x + cw / 2, y + 48, t, 21, weight=900, fill=c)
        b += text(x + cw / 2, y + 82, e, 14, weight=900, fill=INK)
        b += text(x + cw / 2, y + 116, ej, 12.5, weight=800, fill=GRIS)
    b += text(x0 + cw, y0 + 2 * ch + 30, "Según el uso de oxígeno: aerobios · anaerobios estrictos (el O₂ les resulta tóxico)", 13, weight=800, fill=PRI) + text(x0 + cw, y0 + 2 * ch + 50, "· anaerobios facultativos (viven con o sin O₂, como las levaduras)", 13, weight=800, fill=PRI)
    save("tipos-nutricion.svg", svg(1000, y0 + 2 * ch + 66, b, "Tipos de nutrición según la fuente de carbono y la fuente de energía"))


# ---------------------------------------------------------------- catabolismo / anabolismo
def cat_ana():
    b = ""
    b += caja(170, 90, 260, 70, "Moléculas complejas", PRI, "#e3eef8", 17, "polisacáridos, lípidos, proteínas")
    b += caja(170, 330, 260, 70, "Moléculas sencillas", PRI, "#e3eef8", 17, "CO₂, H₂O, NH₃, lactato…")
    b += caja(830, 90, 260, 70, "Moléculas complejas", VERDE, "#e5f4ec", 17, "glúcidos, lípidos, proteínas, ADN")
    b += caja(830, 330, 260, 70, "Precursores sencillos", VERDE, "#e5f4ec", 17, "monosacáridos, aminoácidos…")
    b += flecha(170, 128, 170, 290, ROJO, 4) + flecha(830, 290, 830, 128, VERDE, 4)
    b += text(60, 200, "CATABOLISMO", 18, weight=900, fill=ROJO, style='transform="rotate(-90 60 200)"')
    b += text(940, 210, "ANABOLISMO", 18, weight=900, fill=VERDE, style='transform="rotate(90 940 210)"')
    for k, t in enumerate(["degradación", "oxidación", "libera energía (exergónico)"]):
        b += text(190, 190 + k * 22, "• " + t, 14, "start", 800, fill=ROJO)
    for k, t in enumerate(["síntesis", "reducción", "consume energía (endergónico)"]):
        b += text(810, 190 + k * 22, t + " •", 14, "end", 800, fill=VERDE)
    # monedas
    b += f'<ellipse cx="500" cy="160" rx="96" ry="36" fill="#fff4df" stroke="{ACC}" stroke-width="3"/>' + text(500, 158, "ATP", 22, weight=900, fill=ACC) + text(500, 178, "energía", 12, weight=800, fill=GRIS)
    b += f'<ellipse cx="500" cy="270" rx="118" ry="36" fill="#efe7fb" stroke="{LILA}" stroke-width="3"/>' + text(500, 266, "NADH · NADPH · FADH₂", 15, weight=900, fill=LILA) + text(500, 286, "poder reductor", 12, weight=800, fill=GRIS)
    b += flecha(300, 160, 398, 160, ACC, 3) + flecha(602, 160, 700, 160, ACC, 3)
    b += flecha(300, 270, 378, 270, LILA, 3) + flecha(622, 270, 700, 270, LILA, 3)
    b += text(500, 110, "el catabolismo los produce · el anabolismo los gasta", 13, weight=900, fill=GRIS)
    b += text(500, 395, "Además, el catabolismo aporta precursores (metabolitos intermedios) que el anabolismo usa como materia prima.", 13, weight=800, fill=PRI)
    save("catabolismo-anabolismo.svg", svg(1000, 415, b, "Catabolismo y anabolismo conectados por el ATP y el poder reductor"))


# ---------------------------------------------------------------- ATP y poder reductor
def atp_nadh():
    b = ""
    # ciclo ATP
    b += text(250, 34, "El ATP, moneda energética", 18, weight=900, fill=ACC)
    b += f'<ellipse cx="250" cy="90" rx="62" ry="30" fill="#fff4df" stroke="{ACC}" stroke-width="3"/>' + text(250, 97, "ATP", 22, weight=900, fill=ACC)
    b += f'<ellipse cx="250" cy="280" rx="80" ry="30" fill="#fff" stroke="{ACC}" stroke-width="3"/>' + text(250, 287, "ADP + Pi", 20, weight=900, fill=ACC)
    b += f'<path d="M190,262 C110,220 110,150 190,110" fill="none" stroke="{ROJO}" stroke-width="4" marker-end="url(#fk)"/>'
    b += f'<path d="M310,110 C390,150 390,220 310,262" fill="none" stroke="{VERDE}" stroke-width="4" marker-end="url(#fk)"/>'
    b += text(80, 170, "síntesis", 14, weight=900, fill=ROJO) + text(80, 188, "(fosforilación)", 12, weight=800, fill=GRIS)
    b += text(80, 210, "energía del", 12, weight=800, fill=ROJO) + text(80, 226, "catabolismo", 12, weight=800, fill=ROJO)
    b += text(450, 170, "hidrólisis", 14, weight=900, fill=VERDE) + text(450, 188, "libera energía", 12, weight=800, fill=GRIS)
    b += text(450, 210, "para el anabolismo,", 12, weight=800, fill=VERDE) + text(450, 226, "el transporte, el movimiento", 12, weight=800, fill=VERDE)
    b += text(250, 342, "Se obtiene por fosforilación a nivel de sustrato,", 12.5, weight=800, fill=GRIS) + text(250, 360, "fosforilación oxidativa o fotofosforilación", 12.5, weight=800, fill=GRIS)
    # poder reductor
    x = 760
    b += text(x, 34, "El poder reductor", 18, weight=900, fill=LILA)
    b += f'<ellipse cx="{x}" cy="90" rx="70" ry="30" fill="#fff" stroke="{LILA}" stroke-width="3"/>' + text(x, 97, "NAD⁺", 20, weight=900, fill=LILA)
    b += f'<ellipse cx="{x}" cy="280" rx="80" ry="30" fill="#efe7fb" stroke="{LILA}" stroke-width="3"/>' + text(x, 287, "NADH + H⁺", 20, weight=900, fill=LILA)
    b += f'<path d="M{x - 60},110 C{x - 140},150 {x - 140},220 {x - 60},262" fill="none" stroke="{ROJO}" stroke-width="4" marker-end="url(#fk)"/>'
    b += f'<path d="M{x + 60},262 C{x + 140},220 {x + 140},150 {x + 60},110" fill="none" stroke="{VERDE}" stroke-width="4" marker-end="url(#fk)"/>'
    b += text(x - 175, 160, "se reduce:", 14, weight=900, fill=ROJO) + text(x - 175, 178, "capta 2 e⁻ y H⁺", 12, weight=800, fill=GRIS) + text(x - 175, 196, "de un sustrato", 12, weight=800, fill=GRIS) + text(x - 175, 214, "que se oxida", 12, weight=800, fill=GRIS)
    b += text(x + 185, 160, "se oxida:", 14, weight=900, fill=VERDE) + text(x + 185, 178, "cede e⁻ y H⁺ a la", 12, weight=800, fill=GRIS) + text(x + 185, 196, "cadena respiratoria", 12, weight=800, fill=GRIS) + text(x + 185, 214, "(o a una síntesis)", 12, weight=800, fill=GRIS)
    b += text(x, 342, "NADH y FADH₂: catabolismo (respiración)", 12.5, weight=800, fill=GRIS) + text(x, 360, "NADPH: anabolismo (fotosíntesis, síntesis de lípidos)", 12.5, weight=800, fill=GRIS)
    save("atp-poder-reductor.svg", svg(1040, 380, b, "Ciclo del ATP y del NAD como transportadores de energía y de poder reductor"))


# ---------------------------------------------------------------- mapa del metabolismo
def mapa():
    b = ""
    # compartimentos
    b += f'<rect x="10" y="10" width="1180" height="620" rx="20" fill="{CITO}" stroke="#2a7fc1" stroke-width="3"/>'
    b += text(30, 40, "CITOSOL", 16, "start", 900, fill="#2a7fc1")
    b += f'<rect x="560" y="300" width="610" height="310" rx="60" fill="{MITO}" stroke="#b5532c" stroke-width="4"/>'
    b += text(1150, 334, "MITOCONDRIA", 16, "end", 900, fill="#b5532c")
    # polímeros
    b += caja(160, 90, 210, 54, "Polisacáridos", PRI, "#e3eef8", 16) + caja(600, 90, 210, 54, "Lípidos (triglicéridos)", PRI, "#e3eef8", 15) + caja(1000, 90, 210, 54, "Proteínas", PRI, "#e3eef8", 16)
    b += caja(160, 190, 170, 46, "Glucosa", INK, "#fff", 16) + caja(600, 190, 230, 46, "Ácidos grasos + glicerina", INK, "#fff", 14) + caja(1000, 190, 170, 46, "Aminoácidos", INK, "#fff", 16)
    b += flecha(160, 118, 160, 166) + flecha(600, 118, 600, 166) + flecha(1000, 118, 1000, 166)
    # glucólisis
    b += flecha(160, 214, 160, 330, ROJO, 3.5) + text(172, 280, "GLUCÓLISIS", 15, "start", 900, fill=ROJO) + text(172, 298, "2 ATP, 2 NADH", 12, "start", 800, fill=GRIS)
    b += caja(160, 360, 170, 46, "2 Piruvato", INK, "#fff", 16)
    # fermentaciones
    b += flecha(110, 384, 80, 470, LILA, 3) + flecha(210, 384, 250, 470, LILA, 3)
    b += caja(80, 500, 130, 46, "Lactato", LILA, "#efe7fb", 15) + caja(270, 500, 170, 46, "Etanol + CO₂", LILA, "#efe7fb", 15)
    b += text(175, 560, "FERMENTACIONES (sin O₂)", 14, weight=900, fill=LILA) + text(175, 578, "regeneran el NAD⁺", 12, weight=800, fill=GRIS)
    # entrada a mitocondria
    b += flecha(246, 360, 640, 400, ROJO, 3) + text(330, 368, "con O₂", 13, weight=900, fill=ROJO)
    b += caja(720, 410, 150, 46, "Acetil-CoA", INK, "#fff", 16)
    b += text(440, 352, "descarboxilación oxidativa (CO₂, NADH)", 11.5, weight=800, fill=GRIS)
    b += flecha(600, 214, 700, 384, ACC, 3) + text(660, 290, "β-OXIDACIÓN", 14, "start", 900, fill=ACC)
    # la glicerina no va a la β-oxidación: se incorpora a la glucólisis
    b += f'<path d="M485,206 L172,258" fill="none" stroke="{ACC}" stroke-width="2.2" stroke-dasharray="6 4" marker-end="url(#fk)"/>'
    b += text(370, 262, "glicerina → glucólisis", 12, weight=900, fill=ACC)
    b += flecha(1000, 214, 800, 386, TEAL, 3) + text(1000, 270, "desaminación", 13, "start", 900, fill=TEAL) + text(1000, 286, "(NH₃ → urea)", 12, "start", 800, fill=GRIS)
    # Krebs
    b += f'<circle cx="720" cy="530" r="58" fill="#fff" stroke="{ROJO}" stroke-width="4"/>' + text(720, 526, "CICLO DE", 13, weight=900, fill=ROJO) + text(720, 544, "KREBS", 16, weight=900, fill=ROJO)
    b += flecha(720, 434, 720, 470, INK, 3)
    b += text(620, 600, "CO₂", 15, weight=900, fill=GRIS) + flecha(668, 560, 634, 588, GRIS, 2)
    # cadena
    b += flecha(778, 530, 870, 530, LILA, 3) + text(824, 518, "NADH, FADH₂", 12, weight=900, fill=LILA)
    b += f'<rect x="880" y="470" width="270" height="120" rx="16" fill="#fff" stroke="{PRI}" stroke-width="3"/>'
    b += text(1015, 500, "CADENA RESPIRATORIA", 14, weight=900, fill=PRI) + text(1015, 520, "+ FOSFORILACIÓN OXIDATIVA", 13, weight=900, fill=PRI)
    b += text(1015, 546, "membrana interna (crestas)", 12, weight=800, fill=GRIS)
    b += text(1015, 572, "O₂ → H₂O · mucho ATP", 14, weight=900, fill=ACC)
    b += text(600, 655, "Glucólisis y fermentaciones: citosol · Descarboxilación del piruvato, Krebs y β-oxidación: matriz · Cadena y ATP sintasa: membrana interna", 12.5, weight=800, fill=GRIS)
    save("mapa-catabolismo.svg", svg(1200, 670, b, "Esquema general del catabolismo de glúcidos, lípidos y proteínas y su localización"))


def retro():
    b = ""
    xs = [100, 330, 560, 790]
    for k, (x, t) in enumerate(zip(xs, ["A", "B", "C", "D"])):
        b += f'<circle cx="{x}" cy="120" r="34" fill="{"#e5f4ec" if k == 3 else "#e3eef8"}" stroke="{VERDE if k == 3 else PRI}" stroke-width="3"/>' + text(x, 129, t, 26, weight=900, fill=VERDE if k == 3 else PRI)
        if k < 3:
            b += flecha(x + 38, 120, xs[k + 1] - 40, 120, INK, 3)
            b += f'<rect x="{(x + xs[k + 1]) / 2 - 36}" y="66" width="72" height="30" rx="10" fill="#fff4df" stroke="{ACC}" stroke-width="2"/>' + text((x + xs[k + 1]) / 2, 86, f"enzima {k + 1}", 13, weight=900, fill=ACC)
    b += f'<path d="M790,156 C790,240 215,240 215,100" fill="none" stroke="{ROJO}" stroke-width="3.5" stroke-dasharray="9 6" marker-end="url(#fk)"/>'
    b += text(500, 232, "el producto final D inhibe a la enzima 1", 15, weight=900, fill=ROJO)
    b += text(100, 52, "sustrato inicial", 13, weight=800, fill=GRIS) + text(790, 52, "producto final", 13, weight=800, fill=GRIS)
    b += text(445, 278, "Si sobra D, se frena su propia síntesis; cuando D se gasta, la enzima 1 vuelve a funcionar (inhibición alostérica).", 13, weight=800, fill=PRI)
    save("retroalimentacion.svg", svg(900, 295, b, "Regulación de una ruta metabólica por retroinhibición"))


if __name__ == "__main__":
    tipos(); cat_ana(); atp_nadh(); mapa(); retro()
