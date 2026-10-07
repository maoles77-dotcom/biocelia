# Esquemas SVG del tema B3 (mutaciones, variabilidad y biodiversidad) de BioCelia.
# Uso: python tools/esquemas_tema_b3.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "b3")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO, VERDE = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"
ARN = "#8e44ad"
MONO = 'font-family="Consolas, monospace"'

# Código genético estándar (NCBI tabla 1), orden U C A G
_T = "FFLLSSSSYY**CC*WLLLLPPPPHHQQRRRRIIIMTTTTNNKKSSRRVVVVAAAADDEEGGGG"
_3 = {"F": "Phe", "L": "Leu", "S": "Ser", "Y": "Tyr", "*": "STOP", "C": "Cys", "W": "Trp", "P": "Pro", "H": "His", "Q": "Gln",
      "R": "Arg", "I": "Ile", "M": "Met", "T": "Thr", "N": "Asn", "K": "Lys", "V": "Val", "A": "Ala", "D": "Asp", "E": "Glu", "G": "Gly"}


def traducir(arnm):
    aa = []
    for i in range(0, len(arnm) - 2, 3):
        c = arnm[i:i + 3]
        a = _3[_T["UCAG".index(c[0]) * 16 + "UCAG".index(c[1]) * 4 + "UCAG".index(c[2])]]
        aa.append(a)
        if a == "STOP":
            break
    return aa


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


# ---------------------------------------------------------------- mutaciones puntuales
def puntuales():
    orig = "AUGGCAUUCCAAUGG"
    casos = [("Original", orig, None, ""),
             ("Sustitución silenciosa", "AUGGCGUUCCAAUGG", 5, "mismo aminoácido (código degenerado)"),
             ("Sustitución con cambio de sentido", "AUGGCAUCCCAAUGG", 7, "cambia un aminoácido"),
             ("Sustitución sin sentido", "AUGGCAUUCUAAUGG", 9, "aparece un codón de parada: proteína corta"),
             ("Inserción", "AUGGGCAUUCCAAUGG", 3, "se desplaza la pauta de lectura"),
             ("Deleción", "AUGCAUUCCAAUGG", 4, "se desplaza la pauta de lectura")]
    W = 13.5  # ancho de letra
    b = text(30, 30, "ARNm (5'→3') y polipéptido resultante", 18, "start", 900, fill=PRI)
    y = 70
    for k, (nom, seq, pos, efecto) in enumerate(casos):
        b += f'<rect x="10" y="{y - 28}" width="1080" height="70" rx="12" fill="{"#f6f9fb" if k % 2 == 0 else "#fff"}"/>'
        b += text(24, y - 2, nom, 15, "start", 900, fill=ROJO if k else PRI)
        if efecto:
            b += text(24, y + 20, efecto, 12, "start", 800, fill=GRIS)
        # secuencia en codones
        x = 330
        for i in range(0, len(seq), 3):
            cod = seq[i:i + 3]
            for j, ch in enumerate(cod):
                idx = i + j
                marcado = pos is not None and (idx == pos if nom != "Deleción" else False)
                col = ROJO if marcado else ARN
                if marcado:
                    b += f'<rect x="{x - 2}" y="{y - 17}" width="{W + 2}" height="24" rx="4" fill="#fde8e6"/>'
                b += text(x + W / 2, y, ch, 17, weight=900, fill=col, style=MONO)
                x += W
            x += 8
        if nom == "Deleción":
            b += text(330 + 3 * W + 4, y - 22, "▼ falta la G del 2.º codón", 11, "start", 900, fill=ROJO)
        # aminoácidos
        aas = traducir(seq)
        ax = 640
        ref = traducir(orig)
        for n_aa, a in enumerate(aas):
            stop = a == "STOP"
            cambia = n_aa >= len(ref) or ref[n_aa] != a
            fill = "#fde8e6" if stop else ("#fff4df" if cambia else "#e5f4ec")
            b += f'<rect x="{ax}" y="{y - 18}" width="{62 if stop else 54}" height="26" rx="13" fill="{fill}" stroke="{ROJO if stop else VERDE}" stroke-width="1.8"/>'
            b += text(ax + (31 if stop else 27), y, a, 13, weight=900, fill=ROJO if stop else INK)
            ax += 66 if stop else 60
        if not aas[-1] == "STOP" and len(seq) % 3:
            b += text(ax + 4, y, "…", 16, "start", 900, fill=GRIS)
        y += 76
    b += text(550, y - 14, "Las sustituciones afectan a un solo codón; las inserciones y deleciones (de 1 o 2 bases) cambian todos los aminoácidos siguientes.", 13, weight=800, fill=GRIS)
    save("mutaciones-puntuales.svg", svg(1100, y, b, "Mutaciones puntuales: sustituciones, inserción y deleción y su efecto en la proteína"))
    return [(c[0], traducir(c[1])) for c in casos]


# ---------------------------------------------------------------- cromosómicas
COLS = {"A": "#e76f51", "B": "#f4a261", "C": "#e9c46a", "D": "#8ab17d", "E": "#2a9d8f", "F": "#457b9d", "G": "#6d597a",
        "P": "#b8c0ff", "Q": "#9bf6ff", "R": "#caffbf", "S": "#fdffb6"}


def cromosoma(x, y, letras, cen=2, w=40, h=36):
    """Cromosoma horizontal: bandas con letra; centrómero tras 'cen' bandas."""
    s = ""
    cx = x
    for i, l in enumerate(letras):
        if i == cen:
            s += f'<path d="M{cx},{y + 4} Q{cx + 9},{y + h / 2} {cx},{y + h - 4} L{cx + 18},{y + h - 4} Q{cx + 9},{y + h / 2} {cx + 18},{y + 4}z" fill="#3b4a5a"/>'
            cx += 18
        r = 14 if i in (0, len(letras) - 1) else 3
        s += f'<rect x="{cx}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{COLS.get(l, "#ccc")}" stroke="{INK}" stroke-width="1.5"/>'
        s += text(cx + w / 2, y + h / 2 + 6, l, 16, weight=900, fill=INK)
        cx += w
    return s


def cromosomicas():
    filas = [("Original", ["A", "B", "C", "D", "E", "F"], None, ""),
             ("Deleción", ["A", "B", "C", "E", "F"], None, "se pierde un fragmento (D)"),
             ("Duplicación", ["A", "B", "C", "D", "D", "E", "F"], None, "se repite un fragmento (D)"),
             ("Inversión", ["A", "B", "C", "E", "D", "F"], None, "un fragmento gira 180º (D-E)")]
    b = text(30, 34, "Mutaciones cromosómicas: cambia la estructura de un cromosoma", 18, "start", 900, fill=PRI)
    y = 64
    for nom, l, _, ef in filas:
        b += text(30, y + 24, nom, 16, "start", 900, fill=ROJO if nom != "Original" else PRI)
        b += text(30, y + 44, ef, 12, "start", 800, fill=GRIS)
        b += cromosoma(260, y, l)
        y += 72
    # translocación
    b += text(30, y + 24, "Translocación", 16, "start", 900, fill=ROJO)
    b += text(30, y + 44, "intercambio entre cromosomas", 12, "start", 800, fill=GRIS)
    b += text(30, y + 60, "no homólogos", 12, "start", 800, fill=GRIS)
    b += cromosoma(260, y, ["A", "B", "C", "D", "E", "F"]) + cromosoma(260, y + 46, ["P", "Q", "R", "S"], cen=1)
    b += flecha(580, y + 40, 640, y + 40)
    b += cromosoma(660, y, ["A", "B", "C", "D", "R", "S"]) + cromosoma(660, y + 46, ["P", "Q", "E", "F"], cen=1)
    save("mutaciones-cromosomicas.svg", svg(1000, y + 100, b, "Mutaciones cromosómicas: deleción, duplicación, inversión y translocación"))


# ---------------------------------------------------------------- genómicas
def par(x, y, col, n=2, h=70, paso=18):
    s = ""
    for k in range(n):
        cx = x + k * paso
        s += f'<rect x="{cx - 5}" y="{y}" width="10" height="{h}" rx="5" fill="{col}" stroke="{INK}" stroke-width="1.2"/>'
        s += f'<rect x="{cx - 6}" y="{y + h * 0.35}" width="12" height="5" fill="#3b4a5a"/>'
    return s


def genomicas():
    cols = ["#e76f51", "#2a9d8f", "#e9c46a"]
    casos = [("Normal (2n = 6)", [2, 2, 2], "euploide", PRI),
             ("Triploide (3n = 9)", [3, 3, 3], "poliploidía", ROJO),
             ("Tetraploide (4n = 12)", [4, 4, 4], "poliploidía", ROJO),
             ("Trisomía (2n + 1 = 7)", [2, 3, 2], "aneuploidía", ACC),
             ("Monosomía (2n − 1 = 5)", [2, 1, 2], "aneuploidía", ACC)]
    b = text(30, 34, "Mutaciones genómicas: cambia el número de cromosomas", 18, "start", 900, fill=PRI)
    for i, (nom, ns, tipo, c) in enumerate(casos):
        cx0 = 20 + i * 200
        b += f'<rect x="{cx0}" y="56" width="186" height="210" rx="16" fill="{"#f6f9fb" if i % 2 == 0 else "#fff"}" stroke="#d5dde3"/>'
        paso = 18 if sum(ns) <= 7 else 12
        x = cx0 + 93 - (sum(ns) * paso + 20 - paso) / 2
        for j, n in enumerate(ns):
            b += par(x, 100, cols[j], n, paso=paso)
            x += n * paso + 10
        b += text(cx0 + 93, 210, nom, 13, weight=900, fill=c)
        b += text(cx0 + 93, 236, tipo, 14, weight=900, fill=c)
    b += text(510, 296, "Poliploidía: juegos completos de más (3n, 4n…) · Aneuploidía: sobra o falta algún cromosoma (2n + 1, 2n − 1)", 14, weight=800, fill=GRIS)
    save("mutaciones-genomicas.svg", svg(1020, 316, b, "Mutaciones genómicas: poliploidías y aneuploidías"))


def no_disyuncion():
    b = text(30, 34, "Origen de las aneuploidías: no disyunción en la meiosis", 18, "start", 900, fill=PRI)
    R, A = "#e76f51", "#2a9d8f"

    def celula(cx, cy, r, cromos):
        s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="#f2f8ec" stroke="{VERDE}" stroke-width="3"/>'
        n = len(cromos)
        for k, col in enumerate(cromos):
            x = cx - (n - 1) * 9 + k * 18
            s += f'<rect x="{x - 4}" y="{cy - 22}" width="8" height="44" rx="4" fill="{col}" stroke="{INK}" stroke-width="1"/>'
        return s
    b += '<g transform="translate(0,34)">'
    b += celula(110, 180, 56, [R, A])
    b += text(110, 262, "célula 2n", 14, weight=900, fill=GRIS) + text(110, 280, "(un par de homólogos)", 12, weight=800, fill=GRIS)
    b += flecha(172, 160, 262, 110) + flecha(172, 200, 262, 250)
    b += text(216, 180, "meiosis I:", 13, weight=900, fill=ROJO) + text(216, 196, "no se separan", 13, weight=900, fill=ROJO)
    b += celula(310, 100, 44, [R, A]) + celula(310, 260, 44, [])
    for k, (cy, cr) in enumerate(((60, [R, A]), (140, [R, A]), (220, []), (300, []))):
        b += flecha(356, 100 if k < 2 else 260, 440, cy)
        b += celula(480, cy, 34, cr)
        b += text(530, cy + 5, "n + 1" if cr else "n − 1", 16, "start", 900, fill=ROJO)
    b += text(480, 346, "gametos", 14, weight=900, fill=GRIS)
    b += flecha(600, 60, 690, 120) + flecha(600, 300, 690, 260)
    b += text(745, 108, "+ gameto normal (n)", 13, weight=800, fill=GRIS) + text(745, 274, "+ gameto normal (n)", 13, weight=800, fill=GRIS)
    b += celula(800, 160, 40, [R, A, R]) + text(860, 165, "2n + 1: trisomía", 16, "start", 900, fill=ACC)
    b += celula(800, 230, 30, [A]) + text(860, 235, "2n − 1: monosomía", 16, "start", 900, fill=ACC)
    b += "</g>"
    save("no-disyuncion.svg", svg(1060, 400, b, "No disyunción en la meiosis y formación de trisomías y monosomías"))


# ---------------------------------------------------------------- agentes
def agentes():
    b = ""
    cols = [("Físicos", PRI, "#e3eef8", ["Radiación UV", "Rayos X y γ (ionizantes)"], ["UV: dímeros de timina", "Ionizantes: roturas del ADN"]),
            ("Químicos", ACC, "#fff4df", ["5-bromouracilo (análogo de base)", "Ácido nitroso", "Agentes alquilantes, acridinas", "Benzopireno (humo del tabaco)"], ["Cambian o sustituyen bases,", "o se intercalan en el ADN"]),
            ("Biológicos", VERDE, "#e5f4ec", ["Virus (p. ej., VPH)", "Transposones (elementos", "genéticos móviles)"], ["Insertan su ADN en el", "genoma y alteran genes"])]
    for i, (t, c, f, ej, ef) in enumerate(cols):
        x = 20 + i * 340
        b += f'<rect x="{x}" y="20" width="320" height="240" rx="18" fill="{f}" stroke="{c}" stroke-width="2.5"/>'
        b += text(x + 160, 56, t, 22, weight=900, fill=c)
        for k, e in enumerate(ej):
            b += text(x + 24, 92 + k * 24, ("• " if not e.startswith("genéticos") else "  ") + e, 14, "start", 800)
        for k, e in enumerate(ef):
            b += text(x + 160, 212 + k * 20, e, 13, weight=900, fill=c)
    # dímero de timina
    y0 = 290
    b += text(20, y0 + 10, "Ejemplo: la radiación UV une dos timinas contiguas de la misma hebra (dímero de timina)", 15, "start", 900, fill=PRI)
    xs = [120 + k * 60 for k in range(8)]
    seq = "ACTTGAGC"
    for k, (x, l) in enumerate(zip(xs, seq)):
        b += linea(x, y0 + 40, x, y0 + 74, "#5b8fc7", 6)
        b += text(x, y0 + 118, l, 18, weight=900, fill=ROJO if k in (2, 3) else INK, style=MONO)
    b += linea(100, y0 + 40, 560, y0 + 40, "#1f5f99", 6)
    b += f'<path d="M{xs[2]},{y0 + 72} C{xs[2]},{y0 + 96} {xs[3]},{y0 + 96} {xs[3]},{y0 + 72}" fill="none" stroke="{ROJO}" stroke-width="4"/>'
    for k in range(4):
        b += linea(640 + k * 20, y0 + 30, 660 + k * 20, y0 + 70, "#b388eb", 3, 'stroke-dasharray="6 4"')
    b += text(700, y0 + 98, "UV", 22, weight=900, fill=LILA)
    b += text(820, y0 + 60, "deforma la doble hélice:", 14, "start", 800, fill=GRIS) + text(820, y0 + 80, "errores al replicar", 14, "start", 800, fill=GRIS)
    save("agentes-mutagenicos.svg", svg(1060, y0 + 140, b, "Agentes mutagénicos físicos, químicos y biológicos; dímero de timina"))


# ---------------------------------------------------------------- variabilidad
def variabilidad():
    R, A = "#e76f51", "#2a9d8f"
    b = ""
    # panel 1: sobrecruzamiento
    b += f'<rect x="10" y="10" width="500" height="330" rx="18" fill="#f6f9fb" stroke="#d5dde3"/>'
    b += text(260, 44, "Recombinación (sobrecruzamiento)", 18, weight=900, fill=PRI)
    b += text(260, 66, "profase I de la meiosis", 13, weight=800, fill=GRIS)

    def crom(x, y, partes, h=180):
        s = ""
        yy = y
        for col, frac in partes:
            s += f'<rect x="{x - 7}" y="{yy}" width="14" height="{h * frac}" rx="6" fill="{col}" stroke="{INK}" stroke-width="1"/>'
            yy += h * frac
        return s
    # antes
    b += crom(80, 100, [(R, 1)]) + crom(100, 100, [(R, 1)]) + crom(140, 100, [(A, 1)]) + crom(160, 100, [(A, 1)])
    b += f'<path d="M100,230 C115,210 125,250 140,230" fill="none" stroke="{INK}" stroke-width="3"/>' + text(120, 300, "quiasma", 13, weight=900, fill=INK)
    b += flecha(200, 190, 290, 190)
    # después
    b += crom(330, 100, [(R, 1)]) + crom(350, 100, [(R, 0.66), (A, 0.34)]) + crom(400, 100, [(A, 0.66), (R, 0.34)]) + crom(420, 100, [(A, 1)])
    b += text(375, 310, "cromátidas recombinadas:", 13, weight=900, fill=ACC) + text(375, 326, "nuevas combinaciones de alelos", 13, weight=800, fill=GRIS)
    # panel 2: segregación al azar
    b += f'<rect x="530" y="10" width="520" height="330" rx="18" fill="#fff" stroke="#d5dde3"/>'
    b += text(790, 44, "Segregación cromosómica al azar", 18, weight=900, fill=PRI)
    b += text(790, 66, "anafase I: cada par se reparte independientemente", 13, weight=800, fill=GRIS)
    combos = [("R1", "R2"), ("R1", "A2"), ("A1", "R2"), ("A1", "A2")]
    for k, (c1, c2) in enumerate(combos):
        cx = 600 + k * 120
        b += f'<circle cx="{cx}" cy="170" r="44" fill="#f2f8ec" stroke="{VERDE}" stroke-width="2.5"/>'
        b += f'<rect x="{cx - 18}" y="140" width="12" height="50" rx="6" fill="{R if c1[0] == "R" else A}" stroke="{INK}"/>'
        b += f'<rect x="{cx + 6}" y="150" width="12" height="32" rx="6" fill="{R if c2[0] == "R" else A}" stroke="{INK}"/>'
    b += text(780, 250, "Con n = 2 pares: 2² = 4 tipos de gametos", 15, weight=900, fill=ACC)
    b += text(780, 276, "En la especie humana (n = 23): 2²³ ≈ 8,4 millones", 15, weight=900, fill=ACC)
    b += text(780, 310, "rojo = cromosoma de origen materno · verde = paterno", 12, weight=800, fill=GRIS)
    b += text(530, 372, "+ Mutación (nuevos alelos) + Fecundación (unión al azar de gametos) = VARIABILIDAD GENÉTICA", 16, weight=900, fill=ROJO)
    save("fuentes-variabilidad.svg", svg(1060, 392, b, "Fuentes de variabilidad genética: recombinación y segregación al azar"))


if __name__ == "__main__":
    for nom, aa in puntuales():
        print(" ", nom, "-".join(aa))
    cromosomicas(); genomicas(); no_disyuncion(); agentes(); variabilidad()
