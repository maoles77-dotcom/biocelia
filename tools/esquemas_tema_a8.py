# Esquemas SVG del tema A8 (prácticas de identificación de biomoléculas) de BioCelia.
# Uso: python tools/esquemas_tema_a8.py
# Colores aproximados de los resultados de cada ensayo (orientativos, como en los libros de texto).
import os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK, BLUE

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "a8")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, ROJO, VERDE, LILA = "#0f4c81", "#c77d00", "#c0392b", "#3f8a3a", "#6d3fc0"


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)


def save(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def tubo(x, y, col, capa=None, w=22, h=120):
    s = f'<path d="M{x - w},{y} V{y + h} A{w},{w} 0 0 0 {x + w},{y + h} V{y}" fill="#fff" stroke="#7b8a97" stroke-width="3"/>'
    s += f'<path d="M{x - w + 2},{y + 45} V{y + h} A{w - 2},{w - 2} 0 0 0 {x + w - 2},{y + h} V{y + 45}z" fill="{col}"/>'
    if capa:
        s += f'<rect x="{x - w + 2}" y="{y + 45}" width="{2 * w - 4}" height="22" fill="{capa}"/>'
    return s


def ensayos():
    filas = [("Benedict", "glúcidos reductores", "#3b7dd8", "#c0392b", None, "azul → rojo ladrillo", "glucosa, fructosa, maltosa, lactosa"),
             ("Lugol", "almidón", "#d9a441", "#1f2a5a", None, "amarillo-pardo → azul-negro", "patata, harina, pan"),
             ("Biuret", "proteínas", "#7fb3e6", "#7b3fb0", None, "azul → violeta", "clara de huevo, leche"),
             ("Sudán", "lípidos", "#d6ecfa", "#d6ecfa", "#e8562a", "se tiñe de rojo la capa de grasa", "aceite, mantequilla")]
    b = text(130, 28, "Ensayo", 15, weight=900, fill=GRIS) + text(330, 28, "Negativo", 15, weight=900, fill=GRIS) + text(430, 28, "Positivo", 15, weight=900, fill=GRIS)
    b += text(700, 28, "Detecta · cambio · ejemplos +", 15, weight=900, fill=GRIS)
    for i, (n, det, neg, pos, capa, cambio, ej) in enumerate(filas):
        y = 50 + i * 190
        b += f'<rect x="10" y="{y - 10}" width="1000" height="180" rx="14" fill="{"#f6f9fb" if i % 2 == 0 else "#fff"}"/>'
        b += text(130, y + 80, n, 24, weight=900, fill=PRI)
        b += tubo(330, y, neg) + tubo(430, y, pos, capa)
        b += text(560, y + 50, det, 18, "start", 900, fill=PRI)
        b += text(560, y + 80, cambio, 15, "start", 800)
        b += text(560, y + 108, "+ " + ej, 14, "start", 700, fill=GRIS)
    save("ensayos-identificacion.svg", svg(1020, 50 + 4 * 190, b, "Resultados de los ensayos de Benedict, Lugol, Biuret y Sudán"))


def arbol():
    def caja(x, y, w, t, col=PRI, fondo="#e7f0f8", size=15):
        return f'<rect x="{x - w / 2}" y="{y - 22}" width="{w}" height="44" rx="12" fill="{fondo}" stroke="{col}" stroke-width="2"/>' + text(x, y + 5, t, size, weight=900, fill=col)

    def flecha(a, c, et=""):
        s = f'<line x1="{a[0]}" y1="{a[1]}" x2="{c[0]}" y2="{c[1]}" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
        if et:
            s += text((a[0] + c[0]) / 2 + 6, (a[1] + c[1]) / 2 - 4, et, 13, "start", 900, fill=ACC)
        return s
    b = caja(450, 34, 260, "Muestra desconocida")
    b += caja(450, 120, 220, "¿Lugol azul-negro?", ACC, "#fff4df") + flecha((450, 56), (450, 96))
    b += caja(200, 210, 200, "Hay almidón", VERDE, "#e5f4ec") + flecha((370, 130), (250, 188), "sí")
    b += caja(650, 210, 240, "¿Benedict rojo?", ACC, "#fff4df") + flecha((530, 130), (620, 188), "no")
    b += caja(500, 300, 240, "Glúcido reductor", VERDE, "#e5f4ec") + flecha((610, 232), (540, 278), "sí")
    b += caja(800, 300, 280, "Hidrolizar y repetir Benedict", ACC, "#fff4df", 13) + flecha((690, 232), (770, 278), "no")
    b += caja(680, 390, 260, "Rojo: disacárido no", VERDE, "#e5f4ec", 13) + text(680, 425, "reductor (sacarosa)", 13, weight=900, fill=VERDE) + flecha((790, 322), (720, 368), "")
    b += text(450, 470, "Biuret violeta → proteínas · Sudán rojo → lípidos (se aplican aparte).", 14, weight=800, fill=GRIS)
    save("arbol-identificacion.svg", svg(960, 490, b, "Árbol de decisión para identificar glúcidos con Lugol y Benedict"))


if __name__ == "__main__":
    ensayos()
    arbol()
