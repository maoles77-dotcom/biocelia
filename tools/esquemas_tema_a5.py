# Esquemas SVG del tema A5 (enzimas) de BioCelia.
# Uso: python tools/esquemas_tema_a5.py
# Las curvas son cualitativas: muestran la forma de las gráficas que se piden interpretar, sin datos reales.
import math, os
import esquemas_tema_a1 as base
from esquemas_tema_a1 import svg, P, d, INK, BLUE

OUT = os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "a5")
os.makedirs(OUT, exist_ok=True)
GRIS = "#4c5b67"
PRI, TEAL, ACC, LILA, ROJO, VERDE = "#0f4c81", "#2a9d8f", "#c77d00", "#6d3fc0", "#c0392b", "#3f8a3a"
ENZ, ENZ_S = "#9ed49a", "#3f8a3a"
SUS, SUS_S = "#f7c948", "#8a6d00"


def text(x, y, s, *a, **k):
    return base.text(x, y, s.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;'), *a, **k)


def save(nombre, contenido):
    with open(os.path.join(OUT, nombre), "w", encoding="utf-8") as f:
        f.write(contenido)
    print("ok", nombre)


def ejes(x0, y0, w, h, ex, ey):
    s = f'<line x1="{x0}" y1="{y0 + h}" x2="{x0 + w}" y2="{y0 + h}" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
    s += f'<line x1="{x0}" y1="{y0 + h}" x2="{x0}" y2="{y0 - 8}" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>'
    s += text(x0 + w, y0 + h + 24, ex, 14, "end", 800)
    s += f'<text x="{x0 - 16}" y="{y0 + h / 2}" font-size="14" font-weight="800" fill="{INK}" text-anchor="middle" transform="rotate(-90 {x0 - 16} {y0 + h / 2})" font-family="Nunito, Segoe UI, sans-serif">{ey}</text>'
    return s


# ─── Enzima dibujada con su centro activo ─────────────────────────────────
def enzima(x, y, hueco="cuadrado", col=ENZ, st=ENZ_S, ancho=120, alto=80, sitio_reg=False):
    """Bloque con un hueco arriba (centro activo). Devuelve svg."""
    w, h = ancho, alto
    if hueco == "cuadrado":
        top = f"H{x - 14} V{y + 24} H{x + 14} V{y}"
    elif hueco == "deformado":
        top = f"H{x - 14} L{x - 4},{y + 24} L{x + 18},{y + 18} L{x + 14},{y}"
    else:
        top = ""
    path = f"M{x - w / 2},{y + h} V{y + 14} Q{x - w / 2},{y} {x - w / 2 + 14},{y} {top} H{x + w / 2 - 14} Q{x + w / 2},{y} {x + w / 2},{y + 14} V{y + h}z"
    s = f'<path d="{path}" fill="{col}" stroke="{st}" stroke-width="2.5"/>'
    if sitio_reg:
        s = s.replace(f"V{y + h}z", f"V{y + h - 10} H{x + 30} V{y + h - 26} H{x + 10} V{y + h}z") if False else s
    return s


def sustrato(x, y, col=SUS, st=SUS_S, et="S"):
    return f'<rect x="{x - 13}" y="{y - 36}" width="26" height="36" rx="5" fill="{col}" stroke="{st}" stroke-width="2"/>' + text(x, y - 13, et, 14, weight=900, fill=st)


# ─── 1 · Energía de activación ─────────────────────────────────────────────
def energia_activacion():
    x0, y0, W, H = 80, 30, 560, 280
    b = ejes(x0, y0, W, H, "transcurso de la reacción", "energía")
    yS, yP = y0 + 130, y0 + 220
    xS, xP = x0 + 70, x0 + W - 70
    sin = f'M{x0 + 10},{yS} H{xS} C{xS + 90},{yS} {x0 + 230},{y0 + 10} {x0 + 280},{y0 + 10} C{x0 + 330},{y0 + 10} {xP - 90},{yP} {xP},{yP} H{x0 + W - 10}'
    con = f'M{x0 + 10},{yS} H{xS} C{xS + 90},{yS} {x0 + 230},{y0 + 85} {x0 + 280},{y0 + 85} C{x0 + 330},{y0 + 85} {xP - 90},{yP} {xP},{yP} H{x0 + W - 10}'
    b += f'<path d="{sin}" fill="none" stroke="{ROJO}" stroke-width="4"/>'
    b += f'<path d="{con}" fill="none" stroke="{VERDE}" stroke-width="4" stroke-dasharray="10 6"/>'
    # flechas Ea
    for ytop, col, et, dx in ((y0 + 10, ROJO, "Ea sin enzima", -8), (y0 + 85, VERDE, "Ea con enzima", 18)):
        xa = x0 + 280 + dx
        b += f'<line x1="{xa}" y1="{yS}" x2="{xa}" y2="{ytop + 4}" stroke="{col}" stroke-width="2.5" marker-start="url(#fk)" marker-end="url(#fk)"/>'
    b += text(x0 + 262, y0 + 60, "Ea sin enzima", 14, "end", 900, fill=ROJO, style='style="paint-order:stroke;stroke:#fff;stroke-width:6px;stroke-linejoin:round"')
    b += text(x0 + 306, y0 + 118, "Ea con enzima", 14, "start", 900, fill=VERDE, style='style="paint-order:stroke;stroke:#fff;stroke-width:6px;stroke-linejoin:round"')
    b += f'<line x1="{xS - 50}" y1="{yS}" x2="{xP + 40}" y2="{yS}" stroke="{GRIS}" stroke-width="1.5" stroke-dasharray="4 4"/>'
    b += f'<line x1="{xP + 30}" y1="{yS}" x2="{xP + 30}" y2="{yP}" stroke="{PRI}" stroke-width="2.5" marker-start="url(#fk)" marker-end="url(#fk)"/>'
    b += text(xP + 38, (yS + yP) / 2 + 5, "energía liberada", 13, "start", 900, fill=PRI) + text(xP + 38, (yS + yP) / 2 + 22, "(igual en los dos casos)", 12, "start", 800, fill=GRIS)
    b += text(xS - 10, yS - 12, "sustratos", 14, weight=900) + text(xP, yP + 26, "productos", 14, weight=900)
    b += f'<line x1="440" y1="350" x2="470" y2="350" stroke="{ROJO}" stroke-width="4"/>' + text(476, 355, "sin enzima", 13, "start", 800)
    b += f'<line x1="560" y1="350" x2="590" y2="350" stroke="{VERDE}" stroke-width="4" stroke-dasharray="10 6"/>' + text(596, 355, "con enzima", 13, "start", 800)
    save("energia-activacion.svg", svg(780, 370, b, "Perfil de energía de una reacción con y sin enzima: la enzima baja la energía de activación sin cambiar la energía liberada"))


# ─── 2 · Mecanismo ──────────────────────────────────────────────────────────
def mecanismo():
    b = ""
    # E + S
    b += enzima(110, 120) + sustrato(110, 70) + text(110, 225, "Enzima + sustrato", 15, weight=900, fill=PRI)
    b += text(110, 40, "", 1)
    b += f'<line x1="190" y1="160" x2="250" y2="160" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    # ES
    b += enzima(330, 120) + f'<rect x="317" y="114" width="26" height="36" rx="5" fill="{SUS}" stroke="{SUS_S}" stroke-width="2"/>' + text(330, 137, "S", 14, weight=900, fill=SUS_S)
    b += text(330, 225, "Complejo enzima-sustrato", 15, weight=900, fill=PRI)
    b += f'<line x1="410" y1="160" x2="470" y2="160" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    # E + P
    b += enzima(550, 120)
    b += f'<rect x="512" y="60" width="18" height="30" rx="5" fill="#f4a261" stroke="#b5600f" stroke-width="2"/><rect x="570" y="52" width="18" height="30" rx="5" fill="#f4a261" stroke="#b5600f" stroke-width="2"/>'
    b += text(521, 50, "P", 13, weight=900, fill="#b5600f") + text(579, 42, "P", 13, weight=900, fill="#b5600f")
    b += text(550, 225, "Enzima libre + productos", 15, weight=900, fill=PRI)
    b += text(330, 30, "E + S ⇄ ES → E + P", 20, weight=900, fill=ACC)
    b += text(110, 250, "centro activo complementario", 12, weight=800, fill=GRIS)
    b += text(550, 250, "la enzima no se consume", 12, weight=800, fill=GRIS)
    save("mecanismo-enzimatico.svg", svg(660, 265, b, "Mecanismo de acción enzimática: enzima y sustrato forman un complejo y se liberan los productos y la enzima intacta"))


# ─── 3 · Holoenzima ─────────────────────────────────────────────────────────
def holoenzima():
    b = enzima(110, 90, "") + text(110, 140, "apoenzima", 15, weight=900, fill=ENZ_S) + text(110, 200, "parte proteica", 13, weight=800, fill=GRIS)
    b += text(205, 135, "+", 30, weight=900)
    b += f'<circle cx="290" cy="110" r="22" fill="{LILA}"/>' + text(290, 116, "Mg²⁺", 13, weight=900, fill="#fff")
    b += text(290, 160, "ion metálico", 13, weight=800, fill=LILA)
    b += text(290, 182, "o", 13, weight=800, fill=GRIS)
    b += f'<rect x="262" y="190" width="56" height="26" rx="8" fill="#f4a261" stroke="#b5600f" stroke-width="2"/>' + text(290, 208, "NAD⁺", 12, weight=900, fill="#7a3a00")
    b += text(290, 236, "coenzima (orgánica)", 13, weight=800, fill="#b5600f")
    b += text(290, 60, "cofactor", 15, weight=900, fill=PRI)
    b += f'<line x1="360" y1="130" x2="420" y2="130" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>'
    b += enzima(530, 90, "")
    b += f'<circle cx="530" cy="120" r="18" fill="{LILA}"/>' + text(530, 125, "Mg²⁺", 11, weight=900, fill="#fff")
    b += text(530, 200, "holoenzima (activa)", 15, weight=900, fill=PRI)
    save("holoenzima.svg", svg(650, 250, b, "La apoenzima más el cofactor, un ion metálico o una coenzima, forman la holoenzima activa"))


# ─── 4 · Curvas ────────────────────────────────────────────────────────────
def curva_sustrato():
    x0, y0, W, H = 70, 40, 470, 240
    b = ejes(x0, y0, W, H, "[sustrato]", "velocidad")
    vmax = y0 + 40
    pts = []
    for i in range(0, 101):
        s = i / 100 * 10
        v = s / (1.2 + s)
        pts.append(f"{x0 + i / 100 * (W - 20):.1f},{y0 + H - v * (H - 40) * 1.0:.1f}")
    b += f'<polyline points="{" ".join(pts)}" fill="none" stroke="{PRI}" stroke-width="4"/>'
    b += f'<line x1="{x0}" y1="{vmax}" x2="{x0 + W - 10}" y2="{vmax}" stroke="{ROJO}" stroke-width="2" stroke-dasharray="7 5"/>'
    b += text(x0 + W - 10, vmax - 10, "velocidad máxima: enzima saturada", 13, "end", 900, fill=ROJO)
    b += text(x0 + 90, y0 + H - 40, "más sustrato →", 12, "start", 800, fill=GRIS) + text(x0 + 90, y0 + H - 24, "más complejos ES", 12, "start", 800, fill=GRIS)
    b += text(x0 + W / 2, y0 + H + 52, "Cantidad de enzima, temperatura y pH constantes.", 13, weight=700, fill=GRIS)
    save("velocidad-sustrato.svg", svg(580, 345, b, "La velocidad aumenta con la concentración de sustrato hasta alcanzar la velocidad máxima cuando la enzima se satura"))


def campana(x0, y0, W, H, centro, ancho, col, w=4, asim=False, dash=""):
    pts = []
    for i in range(0, 201):
        x = i / 200
        if asim:
            v = math.exp(-((x - centro) / ancho) ** 2) if x <= centro else max(0, 1 - ((x - centro) / (ancho * 0.6)) ** 2)
        else:
            v = math.exp(-((x - centro) / ancho) ** 2)
        pts.append(f"{x0 + x * W:.1f},{y0 + H - v * (H - 30):.1f}")
    return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="{w}" {dash}/>'


def curvas_t_ph():
    b = ""
    x0, y0, W, H = 60, 50, 330, 220
    b += text(x0 + W / 2, 28, "Temperatura", 17, weight=900, fill=PRI)
    b += ejes(x0, y0, W, H, "temperatura", "actividad")
    b += campana(x0, y0, W - 10, H, 0.62, 0.22, ROJO, asim=True)
    xo = x0 + 0.62 * (W - 10)
    b += f'<line x1="{xo:.1f}" y1="{y0 + 30}" x2="{xo:.1f}" y2="{y0 + H}" stroke="{GRIS}" stroke-width="1.5" stroke-dasharray="4 4"/>'
    b += text(xo, y0 + H + 18, "óptima", 12, weight=900, fill=ROJO)
    b += text(x0 + 70, y0 + 120, "↑ T → más", 12, weight=800, fill=GRIS) + text(x0 + 70, y0 + 136, "choques E-S", 12, weight=800, fill=GRIS)
    b += text(x0 + W - 40, y0 + 100, "desnatura-", 12, weight=800, fill=ROJO) + text(x0 + W - 40, y0 + 116, "lización", 12, weight=800, fill=ROJO)
    ox = 470
    b += text(ox + W / 2, 28, "pH", 17, weight=900, fill=PRI)
    b += ejes(ox, y0, W, H, "pH", "actividad")
    for c, col, et in ((2 / 12, "#c0392b", "pepsina (≈2)"), (6.8 / 12, BLUE, "amilasa salival (≈7)"), (8 / 12, VERDE, "tripsina (≈8)")):
        b += campana(ox, y0, W, H, c, 0.08, col, 3.5)
    b += text(ox + 2 / 12 * W, y0 + 18, "pepsina", 12, weight=900, fill="#c0392b") + text(ox + 2 / 12 * W, y0 + 32, "(estómago)", 11, weight=800, fill=GRIS)
    b += text(ox + 6.8 / 12 * W - 12, y0 + 6, "amilasa", 12, weight=900, fill=BLUE)
    b += text(ox + 8 / 12 * W + 34, y0 + 32, "tripsina", 12, weight=900, fill=VERDE) + text(ox + 8 / 12 * W + 34, y0 + 46, "(intestino)", 11, weight=800, fill=GRIS)
    for v in (2, 4, 6, 8, 10):
        b += text(ox + v / 12 * W, y0 + H + 18, str(v), 12, weight=800)
    b += text(450, 330, "Curvas cualitativas. Cada enzima tiene su temperatura y su pH óptimos.", 13, weight=700, fill=GRIS)
    save("temperatura-ph.svg", svg(880, 345, b, "Actividad enzimática según la temperatura y según el pH, con un óptimo en cada caso"))


# ─── 5 · Inhibición ────────────────────────────────────────────────────────
def inhibicion():
    b = ""
    cols = [(130, "Competitiva (reversible)"), (440, "No competitiva (reversible)"), (750, "Irreversible")]
    for x, t in cols:
        b += text(x, 30, t, 16, weight=900, fill=PRI)
    # competitiva: el inhibidor ocupa el centro activo
    x = 130
    b += enzima(x, 140)
    b += f'<rect x="{x - 13}" y="134" width="26" height="36" rx="5" fill="#e76f51" stroke="#9c3b1f" stroke-width="2"/>' + text(x, 157, "I", 14, weight=900, fill="#fff")
    b += sustrato(x + 50, 110) + f'<line x1="{x + 37}" y1="80" x2="{x + 63}" y2="106" stroke="{ROJO}" stroke-width="3"/>'
    b += text(x, 255, "el inhibidor se parece al sustrato", 12, weight=800, fill=GRIS) + text(x, 271, "y compite por el centro activo", 12, weight=800, fill=GRIS)
    b += text(x, 293, "se supera añadiendo más sustrato", 12, weight=900, fill=VERDE)
    # no competitiva: inhibidor en otro sitio, centro activo deformado
    x = 440
    b += enzima(x, 140, "deformado")
    b += f'<circle cx="{x + 52}" cy="{140 + 60}" r="14" fill="#e76f51" stroke="#9c3b1f" stroke-width="2"/>' + text(x + 52, 205, "I", 13, weight=900, fill="#fff")
    b += sustrato(x - 6, 110) + f'<line x1="{x - 19}" y1="80" x2="{x + 7}" y2="106" stroke="{ROJO}" stroke-width="3"/>'
    b += text(x, 255, "se une a otro lugar y deforma", 12, weight=800, fill=GRIS) + text(x, 271, "el centro activo", 12, weight=800, fill=GRIS)
    b += text(x, 293, "más sustrato no lo evita", 12, weight=900, fill=ROJO)
    # irreversible: enlace covalente
    x = 750
    b += enzima(x, 140)
    b += f'<rect x="{x - 13}" y="134" width="26" height="36" rx="5" fill="#6d597a" stroke="#3c2f45" stroke-width="2"/>' + text(x, 157, "I", 14, weight=900, fill="#fff")
    b += f'<line x1="{x - 18}" y1="168" x2="{x + 18}" y2="168" stroke="{ROJO}" stroke-width="4"/>' + text(x, 236, "enlace covalente", 12, "middle", 900, fill=ROJO)
    b += text(x, 255, "unión permanente: la enzima", 12, weight=800, fill=GRIS) + text(x, 271, "queda inutilizada", 12, weight=800, fill=GRIS)
    b += text(x, 293, "venenos (metales pesados, gases nerviosos)", 12, weight=900, fill=ROJO)
    save("inhibicion.svg", svg(880, 305, b, "Inhibición competitiva, no competitiva e irreversible"))


def inhibicion_curvas():
    x0, y0, W, H = 70, 40, 470, 240
    b = ejes(x0, y0, W, H, "[sustrato]", "velocidad")

    def curva(km, vm, col, dash=""):
        pts = []
        for i in range(0, 101):
            s = i / 100 * 10
            v = vm * s / (km + s)
            pts.append(f"{x0 + i / 100 * (W - 20):.1f},{y0 + H - v * (H - 40):.1f}")
        return f'<polyline points="{" ".join(pts)}" fill="none" stroke="{col}" stroke-width="4" {dash}/>'
    b += curva(1.0, 1.0, PRI) + curva(4.5, 1.0, ACC, 'stroke-dasharray="10 6"') + curva(1.0, 0.55, ROJO, 'stroke-dasharray="3 5"')
    b += f'<line x1="{x0}" y1="{y0 + 40}" x2="{x0 + W - 10}" y2="{y0 + 40}" stroke="{GRIS}" stroke-width="1.5" stroke-dasharray="4 4"/>'
    b += text(x0 + W - 10, y0 + 30, "Vmax", 13, "end", 900, fill=GRIS)
    b += text(x0 + W + 10, y0 + 68, "sin inhibidor", 13, "start", 900, fill=PRI)
    b += text(x0 + W + 10, y0 + 96, "competitivo: más lento,", 13, "start", 900, fill=ACC) + text(x0 + W + 10, y0 + 112, "pero alcanza la Vmax", 13, "start", 900, fill=ACC)
    b += text(x0 + W + 10, y0 + 150, "no competitivo: la Vmax", 13, "start", 900, fill=ROJO) + text(x0 + W + 10, y0 + 166, "baja", 13, "start", 900, fill=ROJO)
    save("inhibicion-curvas.svg", svg(760, 320, b, "Velocidad frente a sustrato sin inhibidor, con inhibidor competitivo y con inhibidor no competitivo"))


# ─── 6 · Alosterismo ───────────────────────────────────────────────────────
def alosterismo():
    b = text(200, 28, "Enzima alostérica", 17, weight=900, fill=PRI)
    b += enzima(120, 80) + text(120, 190, "forma activa", 13, weight=900, fill=VERDE)
    b += f'<rect x="{120 + 25}" y="{80 + 52}" width="30" height="20" rx="4" fill="#fff" stroke="{ENZ_S}" stroke-width="2"/>' + text(160, 230, "centro regulador", 12, weight=800, fill=GRIS)
    b += f'<line x1="200" y1="120" x2="250" y2="120" stroke="{INK}" stroke-width="3" marker-end="url(#fk)"/>' + text(225, 108, "+ inhibidor", 12, weight=900, fill=ROJO)
    b += enzima(330, 80, "deformado", "#c9d6c4", "#7b8a97")
    b += f'<rect x="{330 + 25}" y="{80 + 52}" width="30" height="20" rx="4" fill="#e76f51" stroke="#9c3b1f" stroke-width="2"/>'
    b += text(330, 190, "forma inactiva", 13, weight=900, fill=ROJO)
    b += f'<line x1="470" y1="30" x2="470" y2="230" stroke="#dde5ec" stroke-width="2"/>'
    b += text(680, 28, "Retroinhibición (feedback)", 17, weight=900, fill=PRI)
    xs = [520, 610, 700, 790]
    for i, (x, m) in enumerate(zip(xs, "ABCD")):
        b += f'<circle cx="{x}" cy="110" r="24" fill="#e7f0f8" stroke="{PRI}" stroke-width="2"/>' + text(x, 116, m, 17, weight=900, fill=PRI)
        if i < 3:
            b += f'<line x1="{x + 26}" y1="110" x2="{x + 62}" y2="110" stroke="{INK}" stroke-width="2.5" marker-end="url(#fk)"/>' + text(x + 45, 98, f"E{i + 1}", 12, weight=900, fill=VERDE)
    b += f'<path d="M790,140 C790,200 565,200 565,124" fill="none" stroke="{ROJO}" stroke-width="2.5" stroke-dasharray="6 4" marker-end="url(#fk)"/>'
    b += text(680, 200, "el producto final D inhibe la primera enzima", 13, weight=900, fill=ROJO)
    b += text(680, 222, "→ no se fabrica más D del necesario", 13, weight=800, fill=GRIS)
    save("alosterismo.svg", svg(860, 240, b, "Enzima alostérica con forma activa e inactiva y retroinhibición de una ruta por su producto final"))


# ─── 7 · Catalasa ──────────────────────────────────────────────────────────
def catalasa():
    def tubo(x, liquido, burbujas, et, sub):
        s = f'<path d="M{x - 26},40 V200 A26,26 0 0 0 {x + 26},200 V40" fill="#fff" stroke="#7b8a97" stroke-width="3"/>'
        s += f'<path d="M{x - 24},120 V200 A24,24 0 0 0 {x + 24},200 V120z" fill="{liquido}"/>'
        s += f'<path d="M{x - 14},190 q14,-16 28,0 q-14,14 -28,0z" fill="#8b2e2e"/>'
        if burbujas:
            for bx, by, r in ((-10, 105, 7), (8, 90, 9), (-4, 70, 6), (12, 58, 7), (-12, 48, 5), (0, 112, 5)):
                s += f'<circle cx="{x + bx}" cy="{by}" r="{r}" fill="#fff" stroke="{BLUE}" stroke-width="1.5"/>'
        return s + text(x, 252, et, 14, weight=900) + text(x, 270, sub, 12, weight=800, fill=GRIS)
    b = tubo(100, "#d6ecfa", True, "Hígado crudo + H₂O₂", "burbujas de O₂") + tubo(300, "#d6ecfa", False, "Hígado hervido + H₂O₂", "sin burbujas")
    b += text(200, 300, "2 H₂O₂ → 2 H₂O + O₂ (catalasa)", 15, weight=900, fill=PRI)
    b += text(200, 322, "hervida, la catalasa se desnaturaliza", 13, weight=800, fill=ROJO)
    save("catalasa-higado.svg", svg(400, 335, b, "El hígado crudo descompone el agua oxigenada con burbujas por la catalasa; hervido, no"))


if __name__ == "__main__":
    for f in (energia_activacion, mecanismo, holoenzima, curva_sustrato, curvas_t_ph, inhibicion, inhibicion_curvas, alosterismo, catalasa):
        f()
