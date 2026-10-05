# Esquemas SVG del tema E2 (ingeniería genética y biotecnología) de BioCelia.
# Uso: python tools/esquemas_tema_e2.py
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, INK

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "e2")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, ACC, LILA, ROJO, VERDE, TEAL = "#0f4c81", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a", "#2a9d8f"
BASE_COL = {"A": "#d1495b", "T": "#edae49", "G": "#00798c", "C": "#30638e"}
PAR = {"A": "T", "T": "A", "G": "C", "C": "G"}


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


def et(x, y, t, col=INK, size=13, anchor="middle", w=800):
    return text(x, y, t, size, anchor, w, fill=col)


def num(x, y, n, col=PRI):
    return f'<circle cx="{x}" cy="{y}" r="15" fill="{col}"/>' + et(x, y + 5, str(n), "#fff", 14, w=900)


def plasmido(cx, cy, r, col=PRI, hueco=None, inserto=None, marcador=True):
    """Plásmido circular; hueco = ángulo (grados) del corte; inserto = ángulo del gen insertado."""
    b = ""
    if hueco is None and inserto is None:
        b += f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{col}" stroke-width="7"/>'
    else:
        a0 = math.radians((hueco if hueco is not None else inserto) + 12)
        a1 = math.radians((hueco if hueco is not None else inserto) - 12 + 360)
        x0, y0 = cx + r * math.cos(a0), cy + r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy + r * math.sin(a1)
        b += f'<path d="M{x0:.1f},{y0:.1f} A{r},{r} 0 1 1 {x1:.1f},{y1:.1f}" fill="none" stroke="{col}" stroke-width="7"/>'
        if inserto is not None:
            b += f'<path d="M{x1:.1f},{y1:.1f} A{r},{r} 0 0 1 {x0:.1f},{y0:.1f}" fill="none" stroke="{ROJO}" stroke-width="9"/>'
    if marcador:
        a0, a1 = math.radians(130), math.radians(170)
        b += f'<path d="M{cx + r * math.cos(a0):.1f},{cy + r * math.sin(a0):.1f} A{r},{r} 0 0 1 {cx + r * math.cos(a1):.1f},{cy + r * math.sin(a1):.1f}" fill="none" stroke="{VERDE}" stroke-width="9"/>'
    return b


# ------------------------------------------------------------ enzima de restricción
def restriccion():
    sec = "TACGAATTCGCA"
    x0, y1, y2, dx = 170, 110, 190, 46
    b = et(450, 34, "Enzima de restricción EcoRI: reconoce GAATTC y corta entre G y A en ambas hebras", PRI, 15, w=900)
    for i, n in enumerate(sec):
        x = x0 + i * dx
        en = 3 <= i <= 8
        for y, nn in ((y1, n), (y2, PAR[n])):
            b += f'<rect x="{x - 18}" y="{y - 18}" width="36" height="36" rx="7" fill="{BASE_COL[nn]}" opacity="{1 if en else 0.55}"/>' + et(x, y + 6, nn, "#fff", 17, w=900)
        b += linea(x, y1 + 20, x, y2 - 20, GRIS, 1.5, 'stroke-dasharray="3 3"')
    b += et(x0 - 40, y1 + 6, "5'", GRIS, 15, w=900) + et(x0 + 11 * dx + 40, y1 + 6, "3'", GRIS, 15, w=900)
    b += et(x0 - 40, y2 + 6, "3'", GRIS, 15, w=900) + et(x0 + 11 * dx + 40, y2 + 6, "5'", GRIS, 15, w=900)
    b += f'<rect x="{x0 + 3 * dx - 26}" y="{y1 - 28}" width="{6 * dx + 6}" height="{y2 - y1 + 56}" rx="12" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="7 5"/>'
    # cortes
    xc1 = x0 + 3 * dx + dx / 2
    xc2 = x0 + 7 * dx + dx / 2
    b += f'<path d="M{xc1},{y1 - 34} V{y1 + 22} H{xc2} V{y2 + 34}" fill="none" stroke="{ROJO}" stroke-width="3.5"/>'
    b += et(xc1, y1 - 42, "✂ corte", ROJO, 14, w=900) + et(xc2, y2 + 54, "✂ corte", ROJO, 14, w=900)
    b += et(450, 270, "Secuencia diana palindrómica: GAATTC se lee igual en las dos hebras en sentido 5'→3'", GRIS, 13.5)
    # resultado
    y = 330
    izq = [("TACG", "ATGCTTAA")]
    xs = 160
    # fragmento izquierdo
    for i, n in enumerate("TACG"):
        b += f'<rect x="{xs + i * 34 - 15}" y="{y - 15}" width="30" height="30" rx="6" fill="{BASE_COL[n]}"/>' + et(xs + i * 34, y + 5, n, "#fff", 14, w=900)
    for i, n in enumerate("ATGCTTAA"):
        b += f'<rect x="{xs + i * 34 - 15}" y="{y + 25}" width="30" height="30" rx="6" fill="{BASE_COL[n]}"/>' + et(xs + i * 34, y + 45, n, "#fff", 14, w=900)
    # fragmento derecho
    xr = 560
    for i, n in enumerate("AATTCGCA"):
        b += f'<rect x="{xr + i * 34 - 15}" y="{y - 15}" width="30" height="30" rx="6" fill="{BASE_COL[n]}"/>' + et(xr + i * 34, y + 5, n, "#fff", 14, w=900)
    for i, n in enumerate("GCGT"):
        b += f'<rect x="{xr + (i + 4) * 34 - 15}" y="{y + 25}" width="30" height="30" rx="6" fill="{BASE_COL[n]}"/>' + et(xr + (i + 4) * 34, y + 45, n, "#fff", 14, w=900)
    b += f'<rect x="{xs + 4 * 34 - 19}" y="{y + 19}" width="{4 * 34 + 4}" height="42" rx="8" fill="none" stroke="{LILA}" stroke-width="3"/>'
    b += f'<rect x="{xr - 19}" y="{y - 21}" width="{4 * 34 + 4}" height="42" rx="8" fill="none" stroke="{LILA}" stroke-width="3"/>'
    b += et(450, y + 100, "EXTREMOS COHESIVOS: colas de una sola hebra complementarias (AATT / TTAA)", LILA, 14, w=900)
    b += et(450, y + 122, "Cualquier ADN cortado con la misma enzima puede emparejarse con ellos; la ADN ligasa sella los enlaces fosfodiéster.", GRIS, 13)
    save("enzima-restriccion.svg", svg(900, 470, b, "Corte de una enzima de restricción y extremos cohesivos"))


# ------------------------------------------------------------ ADN recombinante (insulina)
def recombinante():
    b = ""
    # paso 1: gen humano
    b += num(40, 60, 1)
    b += f'<rect x="70" y="40" width="220" height="40" rx="8" fill="#fff" stroke="{GRIS}" stroke-width="2"/>'
    b += f'<rect x="140" y="44" width="80" height="32" rx="6" fill="{ROJO}"/>' + et(180, 66, "gen", "#fff", 14, w=900)
    b += et(180, 106, "ADN humano: se aísla el gen de la insulina", INK, 13) + et(180, 124, "(o ADNc obtenido con transcriptasa inversa)", GRIS, 12)
    # plásmido
    b += num(40, 200, 1)
    b += plasmido(180, 220, 52)
    b += et(180, 226, "plásmido", PRI, 13, w=900) + et(180, 300, "vector con gen de resistencia", VERDE, 12, w=900) + et(180, 316, "a un antibiótico (marcador)", VERDE, 12, w=900)
    # paso 2: corte
    b += flecha(300, 64, 395, 140, INK) + flecha(250, 220, 380, 200, INK)
    b += num(440, 60, 2) + et(440, 100, "Corte con la misma", INK, 13, w=900) + et(440, 118, "enzima de restricción", ROJO, 13, w=900)
    b += f'<rect x="400" y="140" width="80" height="26" rx="6" fill="{ROJO}"/>' + et(440, 158, "inserto", "#fff", 12, w=900)
    b += plasmido(440, 240, 44, hueco=0)
    b += et(440, 314, "extremos cohesivos", LILA, 12, w=900)
    # paso 3: ligasa
    b += flecha(500, 200, 590, 200, INK)
    b += num(660, 60, 3) + et(660, 100, "Unión con", INK, 13, w=900) + et(660, 118, "ADN ligasa", PRI, 13, w=900)
    b += plasmido(660, 220, 52, inserto=0)
    b += et(660, 300, "ADN RECOMBINANTE", ROJO, 13, w=900)
    # paso 4: introducción en bacteria
    b += flecha(730, 220, 800, 220, INK)
    b += num(880, 60, 4) + et(880, 100, "Se introduce en", INK, 13, w=900) + et(880, 118, "la bacteria (E. coli)", TEAL, 13, w=900)
    b += f'<rect x="810" y="170" width="150" height="100" rx="50" fill="#dff3ef" stroke="{TEAL}" stroke-width="3"/>'
    b += f'<path d="M840,215 q15,-25 35,0 t35,0" fill="none" stroke="{INK}" stroke-width="2.5"/>'
    b += plasmido(920, 240, 16, inserto=0, marcador=False)
    b += et(885, 300, "bacteria transformada", TEAL, 12, w=900)
    # paso 5: selección
    b += flecha(885, 330, 885, 380, INK)
    b += num(990, 395, 5)
    b += f'<ellipse cx="885" cy="430" rx="80" ry="34" fill="#fff4df" stroke="{ACC}" stroke-width="2.5"/>'
    for dx, dy in ((-40, -8), (0, 10), (30, -12), (50, 8), (-20, 14)):
        b += f'<circle cx="{885 + dx}" cy="{430 + dy}" r="7" fill="{TEAL}"/>'
    b += et(885, 490, "Selección: medio con antibiótico;", INK, 12.5, w=900) + et(885, 506, "solo crecen las que tienen el plásmido", GRIS, 12)
    # paso 6: cultivo
    b += flecha(800, 430, 640, 430, INK)
    b += num(560, 370, 6)
    b += f'<rect x="490" y="390" width="140" height="90" rx="20" fill="#fbe9c8" stroke="{INK}" stroke-width="3"/>'
    for dx, dy in ((-40, 0), (0, 20), (30, -10), (-15, -20), (40, 25)):
        b += f'<rect x="{560 + dx - 9}" y="{435 + dy - 4}" width="18" height="8" rx="4" fill="{TEAL}"/>'
    b += et(560, 500, "Cultivo en fermentador:", INK, 12.5, w=900) + et(560, 516, "la bacteria transcribe y traduce el gen", GRIS, 12)
    b += flecha(480, 430, 360, 430, INK)
    b += caja(260, 430, 190, 56, "INSULINA HUMANA", ROJO, "#fdeaea", 15, "se extrae y purifica")
    b += et(500, 560, "Funciona porque el código genético es universal: la bacteria «lee» el gen humano igual que lo haría una célula humana.", PRI, 13.5, w=900)
    save("adn-recombinante.svg", svg(1020, 580, b, "Obtención de insulina humana mediante ADN recombinante"))


# ------------------------------------------------------------ ADNc
def adnc():
    b = et(450, 30, "TRANSCRIPTASA INVERSA: de ARNm a ADN complementario (ADNc)", PRI, 15, w=900)
    # gen eucariota
    y = 80
    b += et(20, y + 6, "Gen eucariota", INK, 13, "start", 900)
    segs = [("E", 70), ("I", 60), ("E", 90), ("I", 70), ("E", 60)]
    x = 150
    for t, w in segs:
        col = PRI if t == "E" else "#c7cdd3"
        b += f'<rect x="{x}" y="{y - 14}" width="{w}" height="28" rx="5" fill="{col}"/>' + et(x + w / 2, y + 5, "exón" if t == "E" else "intrón", "#fff" if t == "E" else GRIS, 11.5, w=900)
        x += w
    b += flecha(300, 104, 300, 140, INK) + et(312, 128, "transcripción y maduración (en la célula)", GRIS, 12, "start")
    # ARNm
    y = 166
    b += et(20, y + 6, "ARNm maduro", INK, 13, "start", 900)
    x = 220
    for w in (70, 90, 60):
        b += f'<rect x="{x}" y="{y - 12}" width="{w}" height="24" rx="5" fill="{ACC}"/>'
        x += w
    b += et(560, y + 5, "sin intrones", ACC, 13, "start", 900)
    b += flecha(330, 186, 330, 222, ROJO, 2.5) + et(342, 210, "transcriptasa inversa (de retrovirus)", ROJO, 13, "start", 900)
    # ADNc
    y = 246
    b += et(20, y + 6, "ADNc", INK, 13, "start", 900)
    x = 220
    for w in (70, 90, 60):
        b += f'<rect x="{x}" y="{y - 12}" width="{w}" height="24" rx="5" fill="{LILA}"/>'
        x += w
    b += et(560, y + 5, "ADN copia del gen, sin intrones", LILA, 13, "start", 900)
    b += et(450, 300, "Las bacterias no pueden eliminar intrones: con el ADNc pueden fabricar la proteína eucariota (insulina).", PRI, 13.5, w=900)
    save("adnc.svg", svg(900, 320, b, "Obtención de ADN complementario con la transcriptasa inversa"))


# ------------------------------------------------------------ PCR
def pcr():
    b = ""
    def hebra(x, y, w, col, et_=None):
        return f'<rect x="{x}" y="{y - 6}" width="{w}" height="12" rx="6" fill="{col}"/>'
    pasos = [(1, "Desnaturalización", "≈ 95 ºC", ROJO, "se rompen los puentes de", "hidrógeno: hebras separadas"),
             (2, "Hibridación de cebadores", "≈ 50-65 ºC", LILA, "los cebadores se unen a sus", "secuencias complementarias"),
             (3, "Extensión", "≈ 72 ºC", VERDE, "la Taq polimerasa (termoestable)", "añade desoxirribonucleótidos")]
    # ADN molde
    b += et(110, 40, "ADN molde", INK, 14, w=900)
    b += hebra(30, 80, 160, PRI) + hebra(30, 100, 160, "#7aa7d1")
    for k in range(12):
        b += linea(40 + k * 13, 86, 40 + k * 13, 94, GRIS, 1.5)
    b += flecha(200, 90, 250, 90, INK)
    for i, (n, t, temp, c, l1, l2) in enumerate(pasos):
        x = 260 + i * 250
        b += f'<rect x="{x}" y="20" width="230" height="240" rx="16" fill="#fff" stroke="{c}" stroke-width="2.5"/>'
        b += num(x + 26, 46, n, c) + et(x + 125, 52, t, c, 14.5 if len(t) < 20 else 13, w=900)
        b += et(x + 115, 78, temp, INK, 15, w=900)
        if n == 1:
            b += hebra(x + 35, 110, 160, PRI) + hebra(x + 35, 150, 160, "#7aa7d1")
        elif n == 2:
            b += hebra(x + 35, 110, 160, PRI) + hebra(x + 35, 150, 160, "#7aa7d1")
            b += hebra(x + 155, 124, 40, LILA) + hebra(x + 35, 136, 40, LILA)
            b += et(x + 175, 96, "cebador", LILA, 11.5, w=900)
        else:
            b += hebra(x + 35, 110, 160, PRI) + hebra(x + 35, 150, 160, "#7aa7d1")
            b += hebra(x + 155, 124, 40, LILA) + hebra(x + 35, 136, 40, LILA)
            b += f'<rect x="{x + 75}" y="{136 - 5}" width="100" height="10" rx="5" fill="{VERDE}"/>'
            b += f'<rect x="{x + 55}" y="{124 - 5}" width="100" height="10" rx="5" fill="{VERDE}"/>'
            b += flecha(x + 172, 140, x + 192, 140, VERDE, 2) + flecha(x + 58, 120, x + 40, 120, VERDE, 2)
        b += et(x + 115, 200, l1, INK, 12.5) + et(x + 115, 218, l2, INK, 12.5)
        if i < 2:
            b += flecha(x + 232, 140, x + 248, 140, INK, 2.5)
    # ciclo
    b += f'<path d="M1010,240 C1060,300 760,330 400,300" fill="none" stroke="{GRIS}" stroke-width="2.5" stroke-dasharray="7 5" marker-end="url(#fk)"/>'
    b += et(700, 342, "Se repite el ciclo 25-35 veces en un termociclador", GRIS, 13.5, w=900)
    # crecimiento
    y0 = 380
    b += et(40, y0 + 20, "Copias:", INK, 14, "start", 900)
    for k, n in enumerate((1, 2, 4, 8)):
        x = 160 + k * 170
        for j in range(n):
            b += hebra(x + (j % 4) * 34, y0 + 6 + (j // 4) * 22, 28, PRI) + hebra(x + (j % 4) * 34, y0 + 14 + (j // 4) * 22, 28, "#7aa7d1")
        b += et(x + 50, y0 + 66, f"ciclo {k}: {n}", GRIS, 12.5, w=900)
    b += et(900, y0 + 20, "tras n ciclos: 2ⁿ copias", ROJO, 16, w=900)
    b += et(900, y0 + 44, "(30 ciclos ≈ mil millones)", GRIS, 12.5)
    b += et(560, y0 + 100, "Reactivos: ADN molde · cebadores (primers) · desoxirribonucleótidos (dNTP) · Taq polimerasa · tampón con Mg²⁺", PRI, 13.5, w=900)
    save("pcr.svg", svg(1120, 500, b, "Etapas de la reacción en cadena de la polimerasa (PCR)"))


# ------------------------------------------------------------ electroforesis
def electroforesis():
    b = ""
    x0, y0, w, h = 80, 70, 520, 380
    b += f'<rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="10" fill="#eef3f8" stroke="{INK}" stroke-width="3"/>'
    b += et(x0 + w / 2, y0 - 30, "(−) polo negativo · pocillos", INK, 14, w=900)
    b += et(x0 + w / 2, y0 + h + 34, "(+) polo positivo", ROJO, 14, w=900)
    carriles = ["M", "Madre", "Hijo/a", "P1", "P2"]
    bandas = {"M": [10, 7, 5, 3, 2, 1], "Madre": [7, 3], "Hijo/a": [7, 2], "P1": [5, 3], "P2": [2, 1]}
    def ypos(kb):
        return y0 + 30 + (math.log10(12) - math.log10(kb)) / (math.log10(12) - math.log10(0.8)) * (h - 50)
    for i, c in enumerate(carriles):
        x = x0 + 60 + i * 100
        b += f'<rect x="{x - 30}" y="{y0 + 10}" width="60" height="12" rx="3" fill="#fff" stroke="{GRIS}" stroke-width="1.5"/>'
        b += et(x, y0 - 6, c, PRI if c != "M" else GRIS, 13, w=900)
        for kb in bandas[c]:
            col = LILA if c == "M" else ("#0f4c81" if c in ("Madre", "Hijo/a") else ACC)
            if c == "Hijo/a" and kb == 2:
                col = VERDE
            if c == "P2" and kb == 2:
                col = VERDE
            b += f'<rect x="{x - 28}" y="{ypos(kb) - 5}" width="56" height="10" rx="3" fill="{col}"/>'
    for kb in bandas["M"]:
        b += et(x0 - 10, ypos(kb) + 5, f"{kb} kb", GRIS, 12, "end", 900)
    b += flecha(x0 + w + 30, y0 + 30, x0 + w + 30, y0 + h - 20, ROJO, 3)
    b += et(x0 + w + 44, y0 + 140, "el ADN (carga", ROJO, 13, "start", 900) + et(x0 + w + 44, y0 + 158, "negativa) migra", ROJO, 13, "start", 900) + et(x0 + w + 44, y0 + 176, "hacia el polo +", ROJO, 13, "start", 900)
    b += et(x0 + w + 44, y0 + 230, "los fragmentos", INK, 13, "start") + et(x0 + w + 44, y0 + 248, "pequeños avanzan", INK, 13, "start") + et(x0 + w + 44, y0 + 266, "más deprisa", INK, 13, "start")
    b += et(x0 + w + 44, y0 + 320, "M = marcador de", LILA, 13, "start", 900) + et(x0 + w + 44, y0 + 338, "tamaño conocido", LILA, 13, "start", 900)
    b += et(400, 512, "Prueba de paternidad: la banda de 7 kb del hijo/a viene de la madre; la de 2 kb solo puede venir de P2.", PRI, 13.5, w=900)
    save("electroforesis.svg", svg(800, 530, b, "Electroforesis en gel de fragmentos de ADN y prueba de paternidad"))


# ------------------------------------------------------------ CRISPR
def crispr():
    b = et(560, 30, "CRISPR-Cas9: unas «tijeras» genéticas guiadas por un ARN", PRI, 16, w=900)
    # ADN
    y1, y2 = 200, 236
    b += linea(60, y1, 620, y1, PRI, 8) + linea(60, y2, 620, y2, "#7aa7d1", 8)
    for k in range(28):
        b += linea(70 + k * 20, y1 + 5, 70 + k * 20, y2 - 5, GRIS, 1.5)
    b += f'<rect x="250" y="{y1 - 10}" width="200" height="56" rx="8" fill="none" stroke="{ACC}" stroke-width="2.5" stroke-dasharray="6 4"/>'
    b += et(350, y2 + 44, "secuencia diana (gen que se quiere editar)", ACC, 13, w=900)
    # Cas9
    b += f'<path d="M210,170 C190,90 290,60 350,70 C440,60 500,100 490,170 C480,270 440,290 350,282 C260,290 220,250 210,170Z" fill="{LILA}" opacity="0.25" stroke="{LILA}" stroke-width="3"/>'
    b += et(350, 100, "Cas9", LILA, 20, w=900) + et(350, 120, "(endonucleasa)", LILA, 12.5, w=900)
    # ARN guía
    b += f'<path d="M270,{y1 - 22} H430 q30,0 40,-40 q10,-30 50,-30" fill="none" stroke="{ROJO}" stroke-width="5"/>'
    b += et(530, 122, "ARN guía", ROJO, 15, "start", 900) + et(530, 140, "complementario de la", GRIS, 12, "start") + et(530, 156, "secuencia diana", GRIS, 12, "start")
    # corte
    b += et(350, y1 + 24, "✂", ROJO, 26, w=900)
    b += et(350, 330, "Cas9 corta las dos hebras en el punto exacto que indica el ARN guía", INK, 13.5, w=900)
    # resultados
    b += flecha(640, 218, 700, 160, INK) + flecha(640, 218, 700, 280, INK)
    b += caja(870, 150, 300, 70, "Inactivar el gen", PRI, "#e3eef8", 15, "la célula repara el corte con errores")
    b += caja(870, 290, 300, 70, "Corregir o insertar", VERDE, "#e5f4ec", 15, "se aporta un ADN molde con la secuencia correcta")
    b += et(560, 380, "Origen: sistema de defensa de bacterias y arqueas frente a virus. Las siglas CRISPR nombran las secuencias repetidas del ADN; Cas, las enzimas que cortan.", GRIS, 12.5)
    b += et(560, 402, "Aplicaciones: terapia génica (anemia falciforme), modelos animales de enfermedades, mejora de cultivos, investigación básica.", PRI, 13, w=900)
    save("crispr.svg", svg(1120, 420, b, "Edición genética con CRISPR-Cas9"))


# ------------------------------------------------------------ terapia génica
def terapia():
    b = et(530, 30, "TERAPIA GÉNICA: introducir, corregir o sustituir genes para tratar una enfermedad", PRI, 15, w=900)
    # ex vivo
    b += f'<rect x="20" y="56" width="500" height="300" rx="16" fill="#fff" stroke="{TEAL}" stroke-width="2.5"/>'
    b += et(270, 86, "EX VIVO (fuera del cuerpo)", TEAL, 16, w=900)
    b += caja(110, 150, 150, 54, "1 · Se extraen", INK, "#f4f7fa", 13, "células del paciente")
    b += flecha(186, 150, 254, 150, INK)
    b += caja(340, 150, 160, 54, "2 · Se les añade", INK, "#f4f7fa", 13, "el gen sano (vector)")
    b += flecha(340, 178, 340, 230, INK)
    b += caja(340, 260, 160, 54, "3 · Se cultivan", INK, "#f4f7fa", 13, "y se seleccionan")
    b += flecha(258, 260, 190, 260, INK)
    b += caja(110, 260, 150, 54, "4 · Se reinyectan", INK, "#f4f7fa", 13, "al paciente")
    b += et(270, 330, "Ej.: células madre de la sangre (inmunodeficiencias,", GRIS, 12) + et(270, 346, "anemia falciforme); linfocitos CAR-T contra el cáncer", GRIS, 12)
    # in vivo
    b += f'<rect x="540" y="56" width="500" height="300" rx="16" fill="#fff" stroke="{LILA}" stroke-width="2.5"/>'
    b += et(790, 86, "IN VIVO (dentro del cuerpo)", LILA, 16, w=900)
    # virus vector
    cx, cy = 650, 200
    pts = " ".join(f"{cx + 34 * math.cos(math.radians(60 * k + 30)):.1f},{cy + 34 * math.sin(math.radians(60 * k + 30)):.1f}" for k in range(6))
    b += f'<polygon points="{pts}" fill="#efe7fb" stroke="{LILA}" stroke-width="3"/>'
    b += f'<path d="M{cx - 16},{cy} q8,-12 16,0 t16,0" fill="none" stroke="{ROJO}" stroke-width="3"/>'
    b += et(cx, cy + 58, "virus modificado", LILA, 12.5, w=900) + et(cx, cy + 74, "con el gen sano", ROJO, 12.5, w=900)
    b += flecha(700, 200, 800, 200, INK)
    b += f'<ellipse cx="900" cy="200" rx="90" ry="60" fill="#fdf3e7" stroke="{ACC}" stroke-width="3"/>'
    b += f'<circle cx="890" cy="200" r="24" fill="#c9b7ef" stroke="{LILA}" stroke-width="2"/>'
    b += f'<path d="M878,200 q6,-8 12,0 t12,0" fill="none" stroke="{ROJO}" stroke-width="3"/>'
    b += et(900, 282, "célula del tejido enfermo", ACC, 12.5, w=900)
    b += et(790, 330, "Ej.: ceguera hereditaria (retina), atrofia muscular", GRIS, 12) + et(790, 346, "espinal: el vector se inyecta en el órgano o en la sangre", GRIS, 12)
    b += et(530, 386, "Se modifican células somáticas: el cambio no pasa a la descendencia (la línea germinal no se puede modificar en España). Vectores: virus no patógenos, liposomas.", PRI, 13, w=900)
    save("terapia-genica.svg", svg(1060, 400, b, "Terapia génica ex vivo e in vivo"))


if __name__ == "__main__":
    restriccion(); recombinante(); adnc(); pcr(); electroforesis(); crispr(); terapia()
