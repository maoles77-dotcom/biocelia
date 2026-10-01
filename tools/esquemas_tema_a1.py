# Genera los esquemas SVG del tema A1 (bioelementos, agua y sales) de BioCelia.
# Uso: python tools/esquemas_tema_a1.py [carpeta_salida]   (por defecto assets/temas/a1)
import math, os, sys

OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(__file__), "..", "assets", "temas", "a1")
FONT = "Nunito, 'Segoe UI', system-ui, sans-serif"
O_COL, O_STROKE = "#d64541", "#9e2a26"
H_COL, H_STROKE = "#f4f6f8", "#7b8a97"
INK = "#22313f"
BLUE = "#2a7fc1"
ANG = 104.5


def d(a):
    r = math.radians(a)
    return math.cos(r), math.sin(r)


def P(p, v, k):
    return (p[0] + v[0] * k, p[1] + v[1] * k)


def svg(w, h, body, title):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" '
            f'font-family="{FONT}"><title>{title}</title>\n'
            '<defs><marker id="fl" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{BLUE}"/></marker>'
            '<marker id="fk" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker>'
            '<radialGradient id="gO" cx="35%" cy="35%" r="70%"><stop offset="0" stop-color="#f08a7e"/><stop offset="1" stop-color="#c0392b"/></radialGradient>'
            '<radialGradient id="gH" cx="35%" cy="35%" r="70%"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#d5dde3"/></radialGradient>'
            '</defs>\n' + body + '</svg>\n')


def text(x, y, s, size=14, anchor="middle", weight=600, fill=INK, style=""):
    return f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" text-anchor="{anchor}" font-weight="{weight}" fill="{fill}" {style}>{s}</text>\n'


def molecule(o, a, L=26, ro=15, rh=9, labels=False):
    """Agua con O en o y el primer enlace O-H en la dirección a (grados)."""
    h1 = P(o, d(a), L)
    h2 = P(o, d(a + ANG), L)
    s = ""
    for h in (h1, h2):
        s += f'<line x1="{o[0]:.1f}" y1="{o[1]:.1f}" x2="{h[0]:.1f}" y2="{h[1]:.1f}" stroke="#55626e" stroke-width="5" stroke-linecap="round"/>\n'
    s += f'<circle cx="{o[0]:.1f}" cy="{o[1]:.1f}" r="{ro}" fill="url(#gO)" stroke="{O_STROKE}" stroke-width="1.5"/>\n'
    for h in (h1, h2):
        s += f'<circle cx="{h[0]:.1f}" cy="{h[1]:.1f}" r="{rh}" fill="url(#gH)" stroke="{H_STROKE}" stroke-width="1.5"/>\n'
    if labels:
        s += text(o[0], o[1] + ro * 0.32, "O", round(ro * 0.9), fill="#fff", weight=800)
        for h in (h1, h2):
            s += text(h[0], h[1] + rh * 0.4, "H", round(rh * 1.1), weight=800)
    return s, h1, h2


def hbond(a, b, ra, rb):
    vx, vy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(vx, vy)
    u = (vx / n, vy / n)
    p, q = P(a, u, ra + 2), P(b, u, -(rb + 2))
    return f'<line x1="{p[0]:.1f}" y1="{p[1]:.1f}" x2="{q[0]:.1f}" y2="{q[1]:.1f}" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="5 4"/>\n'


def save(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(content)
    print("ok", name)


# 1 · Molécula de agua ----------------------------------------------------
def agua_molecula():
    o = (230, 125)
    L = 92
    h1, h2 = P(o, d(37.75), L), P(o, d(142.25), L)
    b = ""
    # pares de electrones no compartidos
    for ang in (215.25, 324.75):
        c = P(o, d(ang), 52)
        b += (f'<ellipse cx="{c[0]:.1f}" cy="{c[1]:.1f}" rx="26" ry="15" transform="rotate({ang:.1f} {c[0]:.1f} {c[1]:.1f})" '
              'fill="#fbe3df" stroke="#e59a90" stroke-width="1.5"/>\n')
        for k in (-7, 7):
            e = P(c, d(ang + 90), k)
            b += f'<circle cx="{e[0]:.1f}" cy="{e[1]:.1f}" r="3.2" fill="{O_STROKE}"/>\n'
    for h in (h1, h2):
        b += f'<line x1="{o[0]}" y1="{o[1]}" x2="{h[0]:.1f}" y2="{h[1]:.1f}" stroke="#55626e" stroke-width="10" stroke-linecap="round"/>\n'
    # arco del ángulo
    p1, p2 = P(o, d(142.25), 58), P(o, d(37.75), 58)
    b += f'<path d="M{p1[0]:.1f},{p1[1]:.1f} A58,58 0 0 0 {p2[0]:.1f},{p2[1]:.1f}" fill="none" stroke="{INK}" stroke-width="2"/>\n'
    b += text(230, 205, "104,5°", 17, weight=800)
    b += f'<circle cx="{o[0]}" cy="{o[1]}" r="40" fill="url(#gO)" stroke="{O_STROKE}" stroke-width="2"/>\n'
    b += text(o[0], o[1] + 9, "O", 26, fill="#fff", weight=800)
    for h in (h1, h2):
        b += f'<circle cx="{h[0]:.1f}" cy="{h[1]:.1f}" r="24" fill="url(#gH)" stroke="{H_STROKE}" stroke-width="2"/>\n'
        b += text(h[0], h[1] + 7, "H", 20, weight=800)
    # cargas parciales
    b += text(230, 42, "δ⁻", 26, fill=O_STROKE, weight=800)
    b += text(h1[0] + 34, h1[1] + 30, "δ⁺", 24, fill=BLUE, weight=800)
    b += text(h2[0] - 34, h2[1] + 30, "δ⁺", 24, fill=BLUE, weight=800)
    # rótulos
    b += text(40, 52, "Pares de electrones", 13, "start", 700)
    b += text(40, 68, "no compartidos", 13, "start", 700)
    b += f'<line x1="150" y1="64" x2="183" y2="88" stroke="{INK}" stroke-width="1.3" marker-end="url(#fk)"/>\n'
    b += text(420, 112, "Enlace covalente", 13, "end", 700)
    b += text(420, 128, "polar (O–H)", 13, "end", 700)
    b += f'<line x1="345" y1="134" x2="272" y2="150" stroke="{INK}" stroke-width="1.3" marker-end="url(#fk)"/>\n'
    b += text(250, 262, "Molécula neutra con distribución asimétrica de cargas: un dipolo eléctrico.", 13, weight=600, fill="#4c5b67")
    save("agua-molecula.svg", svg(500, 275, b, "Estructura de la molécula de agua"))


# 2 · Puentes de hidrógeno -----------------------------------------------
def puentes():
    c = (250, 175)
    L, hb = 38, 62
    b = ""
    parts = []
    s, h1, h2 = molecule(c, 37.75, L=38, ro=22, rh=13, labels=True)
    centro = s
    # vecinos que reciben los H del central
    for h, phi in ((h1, 37.75), (h2, 142.25)):
        on = P(h, d(phi), hb)
        ms, _, _ = molecule(on, phi - 52.25, L=38, ro=22, rh=13, labels=True)
        parts.append(ms)
        b += hbond(h, on, 13, 22)
    # vecinos que ceden un H al O central
    for psi in (215.25, 324.75):
        hn = P(c, d(psi), hb)
        on = P(hn, d(psi), L)
        ms, _, _ = molecule(on, psi + 180, L=38, ro=22, rh=13, labels=True)
        parts.append(ms)
        b += hbond(hn, c, 13, 22)
    body = b + "".join(parts) + centro
    body += text(280, 340, "Cada molécula puede formar hasta 4 puentes de hidrógeno (2 con sus H y 2 con su O).", 13, fill="#4c5b67")
    # leyenda
    body += f'<line x1="380" y1="40" x2="410" y2="40" stroke="#55626e" stroke-width="5" stroke-linecap="round"/>'
    body += text(418, 45, "Enlace covalente", 13, "start")
    body += f'<line x1="380" y1="64" x2="410" y2="64" stroke="{BLUE}" stroke-width="2.5" stroke-dasharray="5 4"/>'
    body += text(418, 69, "Puente de hidrógeno", 13, "start")
    save("agua-puentes-hidrogeno.svg", svg(560, 355, body, "Puentes de hidrógeno entre moléculas de agua"))


# 3 · Solvatación del NaCl -------------------------------------------------
def solvatacion():
    b = ""
    na, cl = (140, 160), (430, 160)
    for k in range(6):
        ang = k * 60 + 30
        o = P(na, d(ang), 58)
        ms, _, _ = molecule(o, ang - 52.25)
        b += ms
    b += f'<circle cx="{na[0]}" cy="{na[1]}" r="22" fill="#8e5bb5" stroke="#5e3a7a" stroke-width="2"/>'
    b += text(na[0], na[1] + 6, "Na⁺", 15, fill="#fff", weight=800)
    for k in range(6):
        psi = k * 60
        hn = P(cl, d(psi), 44)
        o = P(hn, d(psi), 26)
        ms, _, _ = molecule(o, psi + 180)
        b += ms
    b += f'<circle cx="{cl[0]}" cy="{cl[1]}" r="30" fill="#2f9e63" stroke="#1d6b42" stroke-width="2"/>'
    b += text(cl[0], cl[1] + 6, "Cl⁻", 16, fill="#fff", weight=800)
    b += text(140, 278, "El catión atrae el polo negativo (O)", 13)
    b += text(430, 278, "El anión atrae el polo positivo (H)", 13)
    b += text(285, 28, "Capa de solvatación: el agua rodea los iones y los mantiene separados", 15, weight=800)
    save("agua-solvatacion-nacl.svg", svg(570, 295, b, "Disolución del cloruro sódico en agua"))


# 4 · Tensión superficial y capilaridad --------------------------------------
def capilaridad():
    b = ""
    # panel A: tensión superficial
    b += text(150, 26, "Tensión superficial (cohesión)", 15, weight=800)
    b += '<rect x="20" y="120" width="260" height="150" rx="6" fill="#a9d4f2"/>'
    b += '<line x1="20" y1="120" x2="280" y2="120" stroke="#2a7fc1" stroke-width="3"/>'
    # zapatero
    b += f'<ellipse cx="150" cy="96" rx="26" ry="8" fill="#5b4636"/>'
    for sx in (-1, 1):
        for k, (dx, ey) in enumerate(((20, 0), (40, -2), (58, -4))):
            x0 = 150 + sx * 12
            xe = 150 + sx * (40 + k * 22)
            b += f'<path d="M{x0},{98} Q{150 + sx * (24 + k * 14)},{78 - k * 3} {xe},{118}" fill="none" stroke="#5b4636" stroke-width="2.4"/>'
            b += f'<path d="M{xe - 7},{120} q7,6 14,0" fill="none" stroke="#2a7fc1" stroke-width="1.5"/>'
    # moléculas superficie e interior
    pts_s = [(50 + 40 * i, 132) for i in range(6)]
    for (x, y) in pts_s:
        b += f'<circle cx="{x}" cy="{y}" r="7" fill="url(#gO)" stroke="{O_STROKE}"/>'
    for (x, y) in pts_s[1:5]:
        b += f'<line x1="{x}" y1="{y + 9}" x2="{x}" y2="{y + 28}" stroke="{INK}" stroke-width="1.6" marker-end="url(#fk)"/>'
    mid = (130, 215)
    b += f'<circle cx="{mid[0]}" cy="{mid[1]}" r="7" fill="url(#gO)" stroke="{O_STROKE}"/>'
    for ang in range(0, 360, 60):
        e = P(mid, d(ang), 26)
        s0 = P(mid, d(ang), 10)
        b += f'<line x1="{s0[0]:.1f}" y1="{s0[1]:.1f}" x2="{e[0]:.1f}" y2="{e[1]:.1f}" stroke="{INK}" stroke-width="1.6" marker-end="url(#fk)"/>'
    b += text(150, 290, "En la superficie la atracción neta va hacia el interior:", 12, weight=600, fill="#4c5b67")
    b += text(150, 306, "la superficie resiste ser atravesada.", 12, weight=600, fill="#4c5b67")
    # panel B: capilaridad
    ox = 330
    W = "#a9d4f2"
    b += text(ox + 160, 26, "Capilaridad (cohesión + adhesión)", 15, weight=800)
    b += f'<rect x="{ox + 70}" y="190" width="230" height="80" rx="6" fill="{W}"/>'
    b += f'<line x1="{ox + 70}" y1="190" x2="{ox + 300}" y2="190" stroke="#2a7fc1" stroke-width="3"/>'
    for (tx, top, w) in ((ox + 110, 70, 14), (ox + 175, 130, 26), (ox + 245, 165, 40)):
        b += f'<rect x="{tx - w / 2}" y="{top}" width="{w}" height="{250 - top}" fill="{W}"/>'
        b += f'<path d="M{tx - w / 2},{top - 1} q{w / 2},{w * 0.45} {w},0 z" fill="#ffffff"/>'
        b += f'<path d="M{tx - w / 2},{top} q{w / 2},{w * 0.45} {w},0" fill="none" stroke="#2a7fc1" stroke-width="2"/>'
        b += f'<line x1="{tx - w / 2 - 2}" y1="50" x2="{tx - w / 2 - 2}" y2="250" stroke="#7b8a97" stroke-width="3"/>'
        b += f'<line x1="{tx + w / 2 + 2}" y1="50" x2="{tx + w / 2 + 2}" y2="250" stroke="#7b8a97" stroke-width="3"/>'
    b += f'<line x1="{ox + 68}" y1="88" x2="{ox + 99}" y2="80" stroke="{INK}" stroke-width="1.4" marker-end="url(#fk)"/>'
    b += text(ox + 64, 80, "adhesión", 12, "end", 700)
    b += text(ox + 64, 95, "a la pared", 12, "end", 700)
    b += text(ox + 175, 290, "Cuanto más estrecho es el tubo, más asciende el agua", 11.5, weight=600, fill="#4c5b67")
    b += text(ox + 175, 306, "(ascenso de la savia bruta por el xilema).", 12, weight=600, fill="#4c5b67")
    save("agua-tension-capilaridad.svg", svg(660, 320, b, "Tensión superficial y capilaridad del agua"))


# 5 · Densidad del hielo -----------------------------------------------------
def hielo():
    b = '<defs><linearGradient id="lago" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#b9def5"/><stop offset="1" stop-color="#2f6f9f"/></linearGradient></defs>'
    b += '<rect x="0" y="0" width="520" height="70" fill="#eef5fb"/>'
    b += '<path d="M0,70 L520,70 L520,300 L0,300 z" fill="url(#lago)"/>'
    b += '<rect x="0" y="62" width="520" height="30" fill="#f4fbff" stroke="#9cc7e3" stroke-width="2"/>'
    b += text(260, 82, "Hielo (0 °C): menos denso, flota y aísla del frío exterior", 14, weight=800)
    b += text(260, 40, "Aire a −30 °C", 14, weight=700, fill="#4c5b67")
    b += text(440, 140, "0 – 4 °C", 13, weight=800, fill="#123")
    b += text(440, 275, "4 °C", 15, weight=800, fill="#fff")
    b += text(440, 292, "máxima densidad", 12, weight=700, fill="#fff")
    for (x, y, s) in ((120, 180, 1), (230, 240, -1), (330, 200, 1)):
        b += (f'<g transform="translate({x},{y}) scale({s},1)"><path d="M-22,0 q22,-16 44,0 q-22,16 -44,0z" fill="#f2a541" stroke="#a8641a"/>'
              '<path d="M22,0 l14,-10 v20z" fill="#f2a541" stroke="#a8641a"/><circle cx="-12" cy="-2" r="2.2" fill="#222"/></g>')
    b += text(200, 316, "El agua líquida sigue bajo el hielo y la vida acuática se mantiene.", 13, weight=600, fill="#4c5b67")
    save("agua-hielo-densidad.svg", svg(520, 325, b, "El hielo flota y protege la vida acuática"))


# 6 · Ósmosis en un tubo en U ----------------------------------------------
def osmosis():
    import random
    random.seed(4)
    b = ""

    def tubo(ox, hl, hr, title):
        s = text(ox + 120, 24, title, 15, weight=800)
        # paredes del tubo
        s += f'<path d="M{ox + 20},50 V250 Q{ox + 20},280 {ox + 50},280 H{ox + 190} Q{ox + 220},280 {ox + 220},250 V50" fill="none" stroke="#7b8a97" stroke-width="4"/>'
        s += f'<path d="M{ox + 80},50 V220 H{ox + 160} V50" fill="none" stroke="#7b8a97" stroke-width="4"/>'
        # agua izquierda y derecha
        s += f'<path d="M{ox + 22},{hl} H{ox + 78} V222 H{ox + 120} V278 H{ox + 50} Q{ox + 22},278 {ox + 22},250 z" fill="#d6ecfa"/>'
        s += f'<path d="M{ox + 162},{hr} H{ox + 218} V250 Q{ox + 218},278 {ox + 190},278 H{ox + 120} V222 H{ox + 162} z" fill="#d6ecfa"/>'
        s += f'<line x1="{ox + 120}" y1="222" x2="{ox + 120}" y2="278" stroke="{O_STROKE}" stroke-width="3" stroke-dasharray="4 3"/>'
        return s

    b += tubo(10, 90, 90, "Al principio")
    b += tubo(300, 120, 60, "Al cabo de un tiempo")
    for ox, hl, hr in ((10, 90, 90), (300, 120, 60)):
        for _ in range(4):
            x, y = random.uniform(ox + 30, ox + 70), random.uniform(hl + 10, 210)
            b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#e0a43a"/>'
        for _ in range(16):
            x, y = random.uniform(ox + 170, ox + 210), random.uniform(hr + 10, 240)
            b += f'<circle cx="{x:.0f}" cy="{y:.0f}" r="5" fill="#e0a43a"/>'
    b += f'<line x1="380" y1="250" x2="460" y2="250" stroke="{BLUE}" stroke-width="3" marker-end="url(#fl)"/>'
    b += text(414, 244, "H₂O", 12, "end", fill=BLUE, weight=800)
    b += text(60, 305, "Hipotónica", 13, weight=800)
    b += text(190, 305, "Hipertónica", 13, weight=800)
    b += text(140, 322, "Membrana semipermeable (solo pasa el agua)", 12, fill=O_STROKE, weight=700)
    b += text(420, 305, "El agua pasa de la disolución diluida", 12, weight=600, fill="#4c5b67")
    b += text(420, 321, "a la concentrada y sube su nivel", 12, weight=600, fill="#4c5b67")
    b += f'<circle cx="250" cy="45" r="5" fill="#e0a43a"/>'
    b += text(260, 50, "soluto", 12, "start", 700)
    save("osmosis-tubo.svg", svg(560, 335, b, "Ósmosis a través de una membrana semipermeable"))


# 7 · Células en distintos medios ------------------------------------------
def celulas():
    b = ""
    cols = (("Medio hipotónico", "entra agua"), ("Medio isotónico", "sin cambio neto"), ("Medio hipertónico", "sale agua"))
    xs = (130, 330, 530)
    for (t, s), x in zip(cols, xs):
        b += text(x, 26, t, 16, weight=800)
        b += text(x, 44, s, 13, weight=600, fill="#4c5b67")
    b += text(16, 135, "Célula", 13, "start", 800)
    b += text(16, 151, "animal", 13, "start", 800)
    b += text(16, 315, "Célula", 13, "start", 800)
    b += text(16, 331, "vegetal", 13, "start", 800)

    def flechas(x, y, r, dentro):
        s = ""
        for ang in (200, 340):
            a, bb = P((x, y), d(ang), r + 30), P((x, y), d(ang), r + 6)
            if not dentro:
                a, bb = bb, a
            s += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{bb[0]:.1f}" y2="{bb[1]:.1f}" stroke="{BLUE}" stroke-width="3" marker-end="url(#fl)"/>'
        return s

    rbc, rbc_s = "#d9534f", "#a33a36"
    # hipotónico: hinchado y roto
    x, y = xs[0], 140
    b += f'<circle cx="{x}" cy="{y}" r="50" fill="#f3b6b3" stroke="{rbc_s}" stroke-width="2.5" stroke-dasharray="70 8 40 10 200"/>'
    b += flechas(x, y, 50, True)
    b += text(x, 222, "Se hincha → hemólisis", 13, weight=800, fill=rbc_s)
    # isotónico: disco bicóncavo
    x = xs[1]
    b += f'<ellipse cx="{x}" cy="{y}" rx="48" ry="40" fill="{rbc}" stroke="{rbc_s}" stroke-width="2"/>'
    b += f'<ellipse cx="{x}" cy="{y}" rx="22" ry="17" fill="#ec8e8a"/>'
    b += f'<line x1="{x - 75}" y1="{y}" x2="{x - 55}" y2="{y}" stroke="{BLUE}" stroke-width="3" marker-end="url(#fl)"/>'
    b += f'<line x1="{x + 55}" y1="{y}" x2="{x + 75}" y2="{y}" stroke="{BLUE}" stroke-width="3" marker-end="url(#fl)"/>'
    b += text(x, 222, "Forma normal", 13, weight=800, fill=rbc_s)
    # hipertónico: crenado
    x = xs[2]
    pts = []
    for i in range(121):
        t = 2 * math.pi * i / 120
        r = 34 + 4.5 * math.sin(11 * t)
        pts.append(f"{x + r * math.cos(t):.1f},{y + r * math.sin(t):.1f}")
    b += f'<polygon points="{" ".join(pts)}" fill="{rbc}" stroke="{rbc_s}" stroke-width="2"/>'
    b += flechas(x, y, 38, False)
    b += text(x, 222, "Se arruga → crenación", 13, weight=800, fill=rbc_s)

    # células vegetales
    y0 = 255
    wall, wall_s = "#cfe8c9", "#3f8a3a"
    for i, x in enumerate(xs):
        b += f'<rect x="{x - 62}" y="{y0}" width="124" height="104" rx="8" fill="{wall}" stroke="{wall_s}" stroke-width="5"/>'
    # turgente
    x = xs[0]
    b += f'<rect x="{x - 56}" y="{y0 + 6}" width="112" height="92" rx="5" fill="#9ed49a" stroke="#2c6e2a" stroke-width="2"/>'
    b += f'<rect x="{x - 44}" y="{y0 + 16}" width="88" height="72" rx="10" fill="#e3f4ff" stroke="#6aa6cf" stroke-width="1.5"/>'
    for ang in (200, 340):
        a, bb = P((x, y0 + 52), d(ang), 95), P((x, y0 + 52), d(ang), 66)
        b += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{bb[0]:.1f}" y2="{bb[1]:.1f}" stroke="{BLUE}" stroke-width="3" marker-end="url(#fl)"/>'
    b += text(x, y0 + 57, "vacuola", 11, weight=700, fill="#3a6f93")
    b += text(x, y0 + 128, "Turgente (la pared evita", 13, weight=800, fill=wall_s)
    b += text(x, y0 + 144, "que estalle)", 13, weight=800, fill=wall_s)
    # isotónico/flácida
    x = xs[1]
    b += f'<rect x="{x - 55}" y="{y0 + 8}" width="110" height="88" rx="10" fill="#9ed49a" stroke="#2c6e2a" stroke-width="2"/>'
    b += f'<rect x="{x - 36}" y="{y0 + 22}" width="72" height="60" rx="12" fill="#e3f4ff" stroke="#6aa6cf" stroke-width="1.5"/>'
    b += text(x, y0 + 128, "Flácida", 13, weight=800, fill=wall_s)
    # plasmólisis
    x = xs[2]
    b += f'<path d="M{x - 36},{y0 + 22} q-12,30 2,62 q34,12 66,-4 q10,-30 -4,-58 q-30,-10 -64,0z" fill="#9ed49a" stroke="#2c6e2a" stroke-width="2"/>'
    b += f'<ellipse cx="{x}" cy="{y0 + 52}" rx="16" ry="13" fill="#e3f4ff" stroke="#6aa6cf" stroke-width="1.5"/>'
    for ang in (200, 340):
        a, bb = P((x, y0 + 52), d(ang), 40), P((x, y0 + 52), d(ang), 72)
        b += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{bb[0]:.1f}" y2="{bb[1]:.1f}" stroke="{BLUE}" stroke-width="3" marker-end="url(#fl)"/>'
    b += text(x, y0 + 128, "Plasmólisis (la membrana", 13, weight=800, fill=wall_s)
    b += text(x, y0 + 144, "se separa de la pared)", 13, weight=800, fill=wall_s)
    save("osmosis-celulas.svg", svg(640, 410, b, "Comportamiento de células animales y vegetales en medios de distinta concentración"))


if __name__ == "__main__":
    for f in (agua_molecula, puentes, solvatacion, capilaridad, hielo, osmosis, celulas):
        f()
