# Esquemas SVG del tema C3 (ciclo celular y cáncer) de BioCelia.
# Uso: python tools/esquemas_tema_c3.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "c3")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, LILA, ROJO, VERDE, TEAL = "#0f4c81", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a", "#2a9d8f"
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


def sector(cx, cy, r1, r2, a1, a2, col):
    """Sector de corona circular entre los ángulos a1 y a2 (grados, sentido horario desde arriba)."""
    def P(r, a):
        t = math.radians(a - 90)
        return cx + r * math.cos(t), cy + r * math.sin(t)
    x1, y1 = P(r2, a1); x2, y2 = P(r2, a2); x3, y3 = P(r1, a2); x4, y4 = P(r1, a1)
    g = 1 if a2 - a1 > 180 else 0
    return (f'<path d="M{x1:.1f},{y1:.1f} A{r2},{r2} 0 {g} 1 {x2:.1f},{y2:.1f} L{x3:.1f},{y3:.1f} '
            f'A{r1},{r1} 0 {g} 0 {x4:.1f},{y4:.1f}z" fill="{col}" stroke="#fff" stroke-width="3"/>')


def polar(cx, cy, r, a):
    t = math.radians(a - 90)
    return cx + r * math.cos(t), cy + r * math.sin(t)


# ---------------------------------------------------------------- ciclo
def ciclo():
    cx, cy, r1, r2 = 330, 270, 110, 200
    fases = [("G1", 0, 150, "#7fb3e6", "crecimiento: síntesis de", "proteínas, ARN y orgánulos"),
             ("S", 150, 250, "#2a7fc1", "replicación del ADN;", "síntesis de histonas"),
             ("G2", 250, 320, "#5aa0d8", "preparación", "para la división"),
             ("M", 320, 360, ROJO, "mitosis y", "citocinesis")]
    b = ""
    for n, a1, a2, col, *_ in fases:
        b += sector(cx, cy, r1, r2, a1, a2, col)
        x, y = polar(cx, cy, (r1 + r2) / 2, (a1 + a2) / 2)
        b += text(x, y + 9, n, 28, weight=900, fill="#fff")
    b += f'<circle cx="{cx}" cy="{cy}" r="{r1 - 6}" fill="#f6f9fb"/>'
    b += text(cx, cy - 10, "CICLO", 22, weight=900, fill=PRI) + text(cx, cy + 18, "CELULAR", 22, weight=900, fill=PRI)
    # arco de interfase
    b += f'<path d="M{polar(cx, cy, r2 + 22, 3)[0]:.1f},{polar(cx, cy, r2 + 22, 3)[1]:.1f} A{r2 + 22},{r2 + 22} 0 1 1 {polar(cx, cy, r2 + 22, 317)[0]:.1f},{polar(cx, cy, r2 + 22, 317)[1]:.1f}" fill="none" stroke="{PRI}" stroke-width="3" stroke-dasharray="8 6"/>'
    x, y = polar(cx, cy, r2 + 44, 200)
    b += text(x - 10, y, "INTERFASE", 18, "end", 900, fill=PRI)
    x, y = polar(cx, cy, r2 + 38, 340)
    b += text(x, y, "FASE M", 16, "end", 900, fill=ROJO)
    # explicaciones
    for k, (n, a1, a2, col, l1, l2) in enumerate(fases):
        ty = 110 + k * 90
        b += f'<rect x="700" y="{ty - 32}" width="330" height="72" rx="14" fill="#fff" stroke="{col}" stroke-width="2.5"/>'
        b += text(720, ty, n, 22, "start", 900, fill=col) + text(780, ty - 4, l1, 15, "start", 800) + text(780, ty + 18, l2, 15, "start", 800)
    # G0
    gx, gy = polar(cx, cy, r2, 75)
    b += flecha(gx + 6, gy, gx + 70, gy + 40, GRIS, 2.5)
    b += f'<circle cx="{gx + 104}" cy="{gy + 62}" r="34" fill="#eef1f4" stroke="{GRIS}" stroke-width="2.5"/>' + text(gx + 104, gy + 70, "G0", 22, weight=900, fill=GRIS)
    b += text(700, 470, "G0: células que dejan de dividirse", 15, "start", 900, fill=GRIS) + text(700, 492, "(neuronas, fibras musculares) o lo hacen", 14, "start", 800, fill=GRIS)
    b += text(700, 512, "solo si reciben señales (hepatocitos).", 14, "start", 800, fill=GRIS)
    # puntos de control
    for a, et in ((140, "G1/S (punto R)"), (316, "G2/M"), (352, "M (huso)")):
        x, y = polar(cx, cy, r2 + 6, a)
        b += f'<circle cx="{x:.1f}" cy="{y:.1f}" r="13" fill="#fff4df" stroke="{ACC}" stroke-width="3"/>' + text(x, y + 6, "!", 16, weight=900, fill=ACC)
    b += text(cx, 520, "! = puntos de control", 15, weight=900, fill=ACC)
    save("ciclo-celular.svg", svg(1050, 540, b, "Fases del ciclo celular, fase G0 y puntos de control"))


# ---------------------------------------------------------------- ADN y cromátidas
def adn():
    x0, y0, w, h = 110, 50, 760, 250
    def Y(c):
        return y0 + h - c / 4 * h
    b = linea(x0, y0 + h, x0 + w, y0 + h, INK, 2.5) + linea(x0, y0 + h, x0, y0 - 10, INK, 2.5)
    for c in (2, 4):
        b += text(x0 - 12, Y(c) + 5, f"{c}C", 15, "end", 900, fill=GRIS) + linea(x0, Y(c), x0 + w, Y(c), "#e1e7ec", 1)
    b += text(36, y0 + h / 2, "ADN por célula", 15, weight=900, fill=GRIS, style=f'transform="rotate(-90 36 {y0 + h / 2})"')
    seg = [(0, 2), (200, 2), (330, 4), (470, 4), (600, 4), (600, 2), (760, 2)]
    b += f'<polyline points="{" ".join(f"{x0 + x},{Y(c):.1f}" for x, c in seg)}" fill="none" stroke="{PRI}" stroke-width="4.5"/>'
    for a, c_, n in ((0, 200, "G1"), (200, 330, "S"), (330, 470, "G2"), (470, 600, "M"), (600, 760, "G1")):
        b += text(x0 + (a + c_) / 2, y0 + h + 24, n, 16, weight=900, fill=ROJO if n == "M" else PRI)
    b += f'<rect x="{x0 + 470}" y="{y0 - 10}" width="130" height="{h + 10}" fill="{ROJO}" opacity="0.06"/>'
    # cromosomas
    def cromo(x, y, dos):
        s = ""
        cols = ["#e05a4f"]
        if dos:
            s += f'<rect x="{x - 10}" y="{y - 24}" width="9" height="48" rx="4.5" fill="#e05a4f" stroke="{INK}"/><rect x="{x + 1}" y="{y - 24}" width="9" height="48" rx="4.5" fill="#e05a4f" stroke="{INK}"/>'
            s += f'<circle cx="{x}" cy="{y - 4}" r="4" fill="{INK}"/>'
        else:
            s += f'<rect x="{x - 4.5}" y="{y - 24}" width="9" height="48" rx="4.5" fill="#e05a4f" stroke="{INK}"/><circle cx="{x}" cy="{y - 4}" r="3.5" fill="{INK}"/>'
        return s
    b += cromo(x0 + 100, Y(2) - 50, False) + text(x0 + 100, Y(2) - 86, "1 cromátida", 13, weight=900, fill=GRIS)
    b += cromo(x0 + 400, Y(4) + 60, True) + text(x0 + 400, Y(4) + 104, "2 cromátidas", 13, weight=900, fill=GRIS)
    b += cromo(x0 + 680, Y(2) - 50, False) + text(x0 + 680, Y(2) - 86, "1 cromátida", 13, weight=900, fill=GRIS)
    b += text(x0 + w / 2, y0 + h + 60, "El número de cromosomas no cambia en la fase S; lo que se duplica es el ADN (cada cromosoma pasa a tener dos cromátidas).", 12.5, weight=800, fill=PRI)
    save("adn-ciclo.svg", svg(900, 380, b, "Variación de la cantidad de ADN a lo largo del ciclo celular"))


# ---------------------------------------------------------------- cáncer
def cel(x, y, r, tipo):
    if tipo == "n":
        return f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fdf3e7" stroke="{MEMB}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="{r * 0.38}" fill="#cfe0f2"/>'
    return (f'<path d="M{x - r},{y} q{r * 0.3},{-r * 1.1} {r},{-r} q{r * 0.9},{r * 0.2} {r * 0.8},{r * 0.9} q{-r * 0.2},{r * 0.8} {-r},{r * 0.6} q{-r * 0.8},{-r * 0.1} {-r * 0.8},{-r * 1.5}z" '
            f'fill="#f7c6c0" stroke="{ROJO}" stroke-width="2"/><circle cx="{x}" cy="{y}" r="{r * 0.5}" fill="#c0392b" opacity="0.7"/>')


def cancer():
    b = ""
    paneles = [("1 · Tejido normal", "las células se dividen solo cuando hace falta"),
               ("2 · Primeras mutaciones", "una célula escapa del control y prolifera"),
               ("3 · Tumor", "masa de células que se dividen sin control"),
               ("4 · Tumor maligno", "invade los tejidos vecinos"),
               ("5 · Metástasis", "células que viajan por la sangre o la linfa")]
    for i, (t, s) in enumerate(paneles):
        x0 = 10 + i * 232
        b += f'<rect x="{x0}" y="10" width="222" height="300" rx="14" fill="{"#f6f9fb" if i % 2 == 0 else "#fff"}" stroke="#d5dde3"/>'
        b += text(x0 + 111, 36, t, 15, weight=900, fill=ROJO if i else PRI)
        b += text(x0 + 111, 292, s, 11, weight=800, fill=GRIS)
        # membrana basal
        b += linea(x0 + 10, 230, x0 + 212, 230, "#8b6a2c", 4)
        # epitelio
        for k in range(7):
            cxk = x0 + 25 + k * 29
            mal = (i == 1 and k == 3) or (i >= 2 and 2 <= k <= 4)
            b += cel(cxk, 212, 13, "c" if mal else "n")
        if i == 1:
            b += text(x0 + 112, 180, "⚡ mutación", 12, weight=900, fill=ROJO)
        if i >= 2:
            pts = [(x0 + 111 + dx, 175 + dy) for dx, dy in ((-30, 0), (0, -6), (30, 0), (-15, -28), (15, -28), (0, -52), (-34, -30), (34, -30))]
            for px, py in pts:
                b += cel(px, py, 14, "c")
        if i >= 3:
            for px, py in ((x0 + 90, 248), (x0 + 120, 260), (x0 + 140, 245)):
                b += cel(px, py, 11, "c")
            b += text(x0 + 180, 262, "invasión", 11, weight=900, fill=ROJO)
        if i == 4:
            b += f'<path d="M{x0 + 160},230 C{x0 + 175},260 {x0 + 195},250 {x0 + 212},270" fill="none" stroke="{ROJO}" stroke-width="10" opacity="0.25"/>'
            b += cel(x0 + 196, 258, 8, "c") + text(x0 + 111, 66, "→ otros órganos", 13, weight=900, fill=ROJO)
            b += text(x0 + 111, 82, "(tumores secundarios)", 11, weight=800, fill=GRIS)
    b += text(590, 340, "El cáncer se origina por la acumulación de varias mutaciones en una misma célula a lo largo del tiempo.", 14, weight=900, fill=PRI)
    save("desarrollo-cancer.svg", svg(1180, 355, b, "Desarrollo de un cáncer: de las primeras mutaciones a la metástasis"))


def genes():
    b = ""
    def coche(x, y, freno_ok, acel_ok):
        s = f'<rect x="{x}" y="{y}" width="140" height="44" rx="14" fill="#cfe3f5" stroke="{PRI}" stroke-width="2.5"/>'
        s += f'<rect x="{x + 30}" y="{y - 26}" width="70" height="30" rx="10" fill="#e3eef8" stroke="{PRI}" stroke-width="2.5"/>'
        s += f'<circle cx="{x + 32}" cy="{y + 46}" r="14" fill="#3b4a5a"/><circle cx="{x + 108}" cy="{y + 46}" r="14" fill="#3b4a5a"/>'
        return s
    cols = [("Célula normal", "acelerador y freno funcionan", True, True, PRI),
            ("Protooncogén → oncogén", "acelerador bloqueado: siempre «dividirse»", False, True, ROJO),
            ("Gen supresor inactivado", "sin freno: no se detiene el ciclo", True, False, ROJO)]
    for i, (t, s, acel, freno, c) in enumerate(cols):
        x0 = 10 + i * 340
        b += f'<rect x="{x0}" y="10" width="330" height="260" rx="16" fill="{"#f6f9fb" if i % 2 == 0 else "#fff"}" stroke="#d5dde3"/>'
        b += text(x0 + 165, 40, t, 17, weight=900, fill=c) + text(x0 + 165, 62, s, 12.5, weight=800, fill=GRIS)
        b += coche(x0 + 95, 130, freno, acel)
        # pedales
        b += f'<rect x="{x0 + 70}" y="200" width="70" height="30" rx="8" fill="{"#e5f4ec" if acel else "#fde8e6"}" stroke="{VERDE if acel else ROJO}" stroke-width="2.5"/>' + text(x0 + 105, 220, "acelerador", 12, weight=900, fill=VERDE if acel else ROJO)
        b += f'<rect x="{x0 + 190}" y="200" width="70" height="30" rx="8" fill="{"#e5f4ec" if freno else "#fde8e6"}" stroke="{VERDE if freno else ROJO}" stroke-width="2.5"/>' + text(x0 + 225, 220, "freno", 12, weight=900, fill=VERDE if freno else ROJO)
        if not acel:
            b += text(x0 + 105, 252, "pisado siempre", 12, weight=900, fill=ROJO)
        if not freno:
            b += text(x0 + 225, 252, "roto", 12, weight=900, fill=ROJO)
        if i > 0:
            for k in range(3):
                b += linea(x0 + 60 - k * 14, 140 + k * 12, x0 + 85 - k * 14, 140 + k * 12, ROJO, 3)
    b += text(510, 296, "Protooncogenes: estimulan la división (acelerador) · Genes supresores de tumores (p53…): la frenan o reparan el ADN (freno)", 13.5, weight=900, fill=PRI)
    save("genes-cancer.svg", svg(1030, 312, b, "Protooncogenes como acelerador y genes supresores como freno del ciclo celular"))


def prevencion():
    cols = [("Agentes físicos", PRI, "#e3eef8", ["Radiación UV (sol, cabinas)", "Rayos X y γ, radón"], "Protección solar, evitar quemaduras"),
            ("Agentes químicos", ACC, "#fff4df", ["Tabaco (benzopireno…)", "Alcohol, amianto", "Aflatoxinas, contaminantes"], "No fumar, menos alcohol"),
            ("Agentes biológicos", VERDE, "#e5f4ec", ["Virus del papiloma (VPH)", "Virus de las hepatitis B y C", "Helicobacter pylori"], "Vacunas (VPH, hepatitis B)")]
    b = ""
    for i, (t, c, f, ej, prev) in enumerate(cols):
        x = 10 + i * 340
        b += f'<rect x="{x}" y="10" width="330" height="230" rx="16" fill="{f}" stroke="{c}" stroke-width="2.5"/>'
        b += text(x + 165, 42, t, 19, weight=900, fill=c)
        for k, e in enumerate(ej):
            b += text(x + 24, 80 + k * 26, "• " + e, 14, "start", 800)
        b += f'<rect x="{x + 16}" y="176" width="298" height="46" rx="12" fill="#fff" stroke="{c}"/>' + text(x + 165, 205, "✓ " + prev, 13.5, weight=900, fill=c)
    hab = ["Dieta rica en fruta, verdura y fibra", "Actividad física y peso saludable", "Cribados: mama, colon, cuello de útero"]
    b += f'<rect x="10" y="256" width="1010" height="96" rx="16" fill="#efe7fb" stroke="{LILA}" stroke-width="2.5"/>'
    b += text(515, 284, "Hábitos de vida saludables", 17, weight=900, fill=LILA)
    for k, h in enumerate(hab):
        b += text(30 + k * 335, 322, "✓ " + h, 13.5, "start", 800)
    save("prevencion-cancer.svg", svg(1030, 365, b, "Agentes cancerígenos y medidas de prevención del cáncer"))


if __name__ == "__main__":
    ciclo(); adn(); cancer(); genes(); prevencion()
