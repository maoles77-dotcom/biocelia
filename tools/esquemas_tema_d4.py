# Esquemas SVG del tema D4 (anabolismo heterótrofo) de BioCelia.
# Uso: python tools/esquemas_tema_d4.py
import os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "d4")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, LILA, ROJO, VERDE, TEAL = "#0f4c81", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a", "#2a9d8f"


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


def pastilla(x, y, t, col, fondo, size=13):
    w = 14 + len(t) * size * 0.62
    return f'<rect x="{x - w / 2}" y="{y - 14}" width="{w}" height="28" rx="14" fill="{fondo}" stroke="{col}" stroke-width="2"/>' + text(x, y + 5, t, size, weight=900, fill=col)


# ---------------------------------------------------------------- niveles
def niveles():
    b = ""
    filas = [("Macromoléculas", ["Proteínas", "Polisacáridos", "Lípidos", "Ácidos nucleicos"], "#e3eef8", PRI, 70),
             ("Monómeros", ["Aminoácidos", "Monosacáridos", "Ácidos grasos + glicerina", "Nucleótidos"], "#fff4df", ACC, 230),
             ("Precursores sencillos", ["piruvato · acetil-CoA · intermediarios del ciclo de Krebs · triosas · CO₂ · NH₃"], "#e5f4ec", VERDE, 390)]
    for t, cajas, f, c, y in filas:
        b += f'<rect x="160" y="{y - 46}" width="780" height="92" rx="18" fill="{f}" stroke="{c}" stroke-width="2.5"/>'
        b += text(176, y - 26, t, 13, "start", 900, fill=c)
        n = len(cajas)
        for k, cj in enumerate(cajas):
            x = 160 + 780 * (k + 0.5) / n
            b += text(x, y + 6, cj, 15 if n > 1 else 14, weight=900, fill=INK)
    # flechas
    b += flecha(1000, 420, 1000, 60, VERDE, 5) + text(1030, 240, "ANABOLISMO", 17, weight=900, fill=VERDE, style='transform="rotate(-90 1030 240)"')
    b += text(1060, 240, "divergente · gasta ATP y NADPH", 12, weight=800, fill=GRIS, style='transform="rotate(-90 1060 240)"')
    b += flecha(110, 60, 110, 420, ROJO, 5)
    b += text(80, 240, "CATABOLISMO", 17, weight=900, fill=ROJO, style='transform="rotate(-90 80 240)"')
    b += text(50, 240, "convergente · produce ATP y NADH", 12, weight=800, fill=GRIS, style='transform="rotate(-90 50 240)"')
    b += flecha(550, 346, 550, 278, VERDE, 3) + flecha(550, 186, 550, 118, VERDE, 3)
    b += text(560, 316, "1.ª fase: síntesis de monómeros", 13, "start", 900, fill=VERDE) + text(560, 156, "2.ª fase: polimerización", 13, "start", 900, fill=VERDE)
    b += text(550, 470, "Los heterótrofos parten de precursores orgánicos (del catabolismo o de la dieta); los autótrofos, además, los fabrican desde el CO₂.", 13, weight=800, fill=PRI)
    save("niveles-anabolismo.svg", svg(1100, 490, b, "Fases del anabolismo: de precursores sencillos a macromoléculas"))


# ---------------------------------------------------------------- glucosa
def glucosa():
    b = f'<rect x="10" y="10" width="980" height="420" rx="20" fill="#fdf3e7" stroke="#2a7fc1" stroke-width="3"/>' + text(30, 40, "Ejemplo: el hígado", 15, "start", 900, fill="#2a7fc1")
    b += caja(500, 90, 200, 54, "Glucógeno", PRI, "#e3eef8", 18)
    b += caja(500, 230, 200, 54, "Glucosa", PRI, "#e3eef8", 18)
    b += caja(500, 370, 300, 54, "Piruvato, lactato,", INK, "#fff", 14, "aminoácidos, glicerina")
    b += f'<path d="M440,203 C400,160 400,150 440,117" fill="none" stroke="{VERDE}" stroke-width="4" marker-end="url(#fk)"/>'
    b += text(390, 150, "glucogenogénesis", 15, "end", 900, fill=VERDE) + text(390, 170, "(síntesis de glucógeno)", 12, "end", 800, fill=GRIS)
    b += f'<path d="M560,117 C600,150 600,160 560,203" fill="none" stroke="{ROJO}" stroke-width="4" marker-end="url(#fk)"/>'
    b += text(610, 150, "glucogenólisis", 15, "start", 900, fill=ROJO) + text(610, 170, "(degradación del glucógeno)", 12, "start", 800, fill=GRIS)
    b += f'<path d="M440,343 C400,300 400,290 440,257" fill="none" stroke="{VERDE}" stroke-width="4" marker-end="url(#fk)"/>'
    b += text(390, 290, "gluconeogénesis", 15, "end", 900, fill=VERDE) + text(390, 310, "(glucosa desde precursores no glúcidos)", 12, "end", 800, fill=GRIS)
    b += f'<path d="M560,257 C600,290 600,300 560,343" fill="none" stroke="{ROJO}" stroke-width="4" marker-end="url(#fk)"/>'
    b += text(610, 290, "glucólisis", 15, "start", 900, fill=ROJO)
    b += text(860, 330, "Tras comer (insulina):", 13, weight=900, fill=VERDE) + text(860, 348, "se almacena glucógeno", 12, weight=800, fill=GRIS)
    b += text(860, 385, "En ayuno o ejercicio (glucagón):", 13, weight=900, fill=ROJO) + text(860, 403, "se libera glucosa a la sangre", 12, weight=800, fill=GRIS)
    save("metabolismo-glucosa.svg", svg(1000, 440, b, "Síntesis y degradación del glucógeno y de la glucosa en el hígado"))


# ---------------------------------------------------------------- ácidos grasos
def acidos_grasos():
    b = ""
    b += f'<rect x="10" y="10" width="480" height="300" rx="18" fill="#fdf3e7" stroke="#2a7fc1" stroke-width="2.5"/>' + text(250, 40, "SÍNTESIS (anabolismo) · CITOSOL", 15, weight=900, fill=VERDE)
    b += caja(250, 90, 180, 46, "Acetil-CoA", INK, "#fff", 15)
    b += flecha(250, 114, 250, 196, VERDE, 4)
    b += pastilla(110, 150, "gasta ATP", ACC, "#fff4df") + pastilla(390, 150, "gasta NADPH", LILA, "#efe7fb")
    b += caja(250, 222, 200, 46, "Ácido graso", PRI, "#e3eef8", 15) + text(250, 270, "se añaden unidades de 2 C (complejo ácido graso sintasa)", 12, weight=800, fill=GRIS)
    b += text(250, 292, "→ con glicerina forma triglicéridos (REL)", 12, weight=900, fill=VERDE)
    b += f'<rect x="510" y="10" width="480" height="300" rx="18" fill="#fbe3d3" stroke="#b5532c" stroke-width="2.5"/>' + text(750, 40, "DEGRADACIÓN (catabolismo) · MITOCONDRIA", 15, weight=900, fill=ROJO)
    b += caja(750, 90, 200, 46, "Ácido graso", PRI, "#e3eef8", 15)
    b += flecha(750, 114, 750, 196, ROJO, 4) + text(760, 160, "β-oxidación", 14, "start", 900, fill=ROJO)
    b += pastilla(620, 150, "produce NADH", LILA, "#efe7fb") + pastilla(620, 186, "y FADH₂", LILA, "#efe7fb")
    b += caja(750, 222, 180, 46, "Acetil-CoA", INK, "#fff", 15) + text(750, 270, "se separan unidades de 2 C", 12, weight=800, fill=GRIS)
    b += text(750, 292, "→ ciclo de Krebs", 12, weight=900, fill=ROJO)
    b += text(500, 340, "Rutas opuestas con enzimas y compartimentos distintos: así se regulan por separado.", 14, weight=900, fill=PRI)
    save("acidos-grasos.svg", svg(1000, 360, b, "Síntesis de ácidos grasos en el citosol frente a beta-oxidación en la mitocondria"))


def aminoacidos():
    b = ""
    b += caja(170, 120, 230, 60, "Esqueleto carbonado", VERDE, "#e5f4ec", 14, "intermediarios de la glucólisis y Krebs")
    b += caja(170, 260, 230, 60, "Grupo amino (–NH₂)", ACC, "#fff4df", 14, "de otro aminoácido (transaminación)")
    b += flecha(290, 130, 430, 180, INK, 3) + flecha(290, 250, 430, 205, INK, 3)
    b += caja(530, 190, 190, 56, "Aminoácido", PRI, "#e3eef8", 17)
    b += flecha(628, 190, 740, 190, INK, 3) + text(684, 176, "traducción", 12, weight=900, fill=PRI)
    b += caja(840, 190, 180, 56, "Proteína", PRI, "#e3eef8", 17) + text(840, 236, "(ribosomas, RER)", 12, weight=800, fill=GRIS)
    b += f'<rect x="380" y="290" width="600" height="80" rx="14" fill="#fde8e6" stroke="{ROJO}" stroke-width="2"/>'
    b += text(680, 318, "Aminoácidos esenciales: no los podemos fabricar y deben estar en la dieta", 14, weight=900, fill=ROJO)
    b += text(680, 344, "(valina, leucina, isoleucina, treonina, metionina, fenilalanina, triptófano, lisina e histidina)", 12, weight=800, fill=GRIS)
    save("aminoacidos.svg", svg(1000, 390, b, "Síntesis de aminoácidos y proteínas; aminoácidos esenciales"))


if __name__ == "__main__":
    niveles(); glucosa(); acidos_grasos(); aminoacidos()
