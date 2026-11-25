#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dibuja el tablero de «Crónicas de la Fortaleza Celular» (A3 apaisado, dos caras: célula animal y vegetal)
como SVG en juego-fortaleza/tablero-animal.svg y tablero-vegetal.svg.

Estética épica, pero cada adorno es biología:
  · la muralla es una bicapa: cabezas hidrófilas hacia fuera y hacia dentro, colas hidrófobas en el centro;
    las torres que la atraviesan son proteínas integrales; los estandartes, solo por fuera, son el glucocáliz;
  · las calzadas son microtúbulos (adoquines alternos de tubulina α y β);
  · el centrosoma son dos centriolos perpendiculares; en la vista de frente se ven sus 9 tripletes;
  · el núcleo tiene doble muralla con poros; la mitocondria, doble muralla con crestas; el Golgi, cara cis y trans;
  · la célula vegetal tiene empalizada (pared de celulosa) con plasmodesmos, gran vacuola y cloroplastos con grana.
El color de cada casilla indica el mazo del Tribunal que se usa al activar ese lugar.
Uso:  python tools/juego_fortaleza_tablero.py
"""
import math
import random
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
W, H = 4200, 2970          # décimas de milímetro: A3 apaisado
COL = {'A': '#c98a1b', 'B': '#2f62d6', 'C': '#1f8a5b', 'D': '#c0392b', 'E': '#7b4bb7', 'F': '#0a8fa8', '-': '#6b5a3e'}
TINTA = '#2e1f0c'
FUENTE = "Cinzel, 'Cormorant Garamond', Georgia, serif"
TEXTO = "'Cormorant Garamond', Georgia, serif"
azar = random.Random(26)


def esc(t):
    return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def nota(x, y, texto, tam=34, ancla='middle', rot=0, color='#5a3b14'):
    r = f' transform="rotate({rot} {x} {y})"' if rot else ''
    return (f'<text x="{x}" y="{y}" font-size="{tam}" font-style="italic" font-family="{TEXTO}" fill="{color}" '
            f'text-anchor="{ancla}" stroke="#f3e2bb" stroke-width="7" paint-order="stroke"{r}>{esc(texto)}</text>')


# ── Definiciones comunes ─────────────────────────────────────────────────────
def defs():
    return '''<defs>
  <filter id="papel" x="0" y="0" width="100%" height="100%">
    <feTurbulence type="fractalNoise" baseFrequency=".011" numOctaves="5" seed="11" result="r"/>
    <feColorMatrix in="r" type="matrix" values="0 0 0 0 .45  0 0 0 0 .3  0 0 0 0 .12  0 0 0 .7 0"/>
    <feComposite in2="SourceGraphic" operator="in"/>
  </filter>
  <filter id="sombra" x="-30%" y="-30%" width="160%" height="160%">
    <feDropShadow dx="10" dy="14" stdDeviation="9" flood-color="#2a1806" flood-opacity=".45"/>
  </filter>
  <filter id="brillo" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="38"/></filter>
  <radialGradient id="vineta" cx="50%" cy="50%" r="75%">
    <stop offset="55%" stop-color="#000" stop-opacity="0"/><stop offset="88%" stop-color="#5a3510" stop-opacity=".45"/>
    <stop offset="100%" stop-color="#2a1404" stop-opacity=".85"/>
  </radialGradient>
  <radialGradient id="fuego"><stop offset="0" stop-color="#fff1a8"/><stop offset=".35" stop-color="#ffb02e"/><stop offset="1" stop-color="#ff5a14" stop-opacity="0"/></radialGradient>
  <radialGradient id="luzcalida"><stop offset="0" stop-color="#ffe7a0" stop-opacity=".95"/><stop offset="1" stop-color="#ffcf6b" stop-opacity="0"/></radialGradient>
  <radialGradient id="acido"><stop offset="0" stop-color="#d8ff8a"/><stop offset=".5" stop-color="#7fd35b"/><stop offset="1" stop-color="#3f8a2a" stop-opacity="0"/></radialGradient>
  <radialGradient id="aguaviva"><stop offset="0" stop-color="#e8f7ff"/><stop offset="1" stop-color="#7fb8d8"/></radialGradient>
  <radialGradient id="solgrad"><stop offset="0" stop-color="#fffbe0"/><stop offset=".5" stop-color="#ffd84d"/><stop offset="1" stop-color="#ffb000" stop-opacity="0"/></radialGradient>
  <linearGradient id="piedra" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#cdb98f"/><stop offset="1" stop-color="#9c8458"/></linearGradient>
  <linearGradient id="madera" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#9a6a35"/><stop offset=".5" stop-color="#c08a4c"/><stop offset="1" stop-color="#8a5a2a"/></linearGradient>
  <linearGradient id="mar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#9fc4c9"/><stop offset="1" stop-color="#6f9ea7"/></linearGradient>
  <pattern id="olas" width="260" height="120" patternUnits="userSpaceOnUse">
    <path d="M0 60 q32 -30 65 0 t65 0 t65 0 t65 0" fill="none" stroke="#e9f2f0" stroke-width="5" opacity=".55"/>
    <path d="M30 100 q20 -16 40 0" fill="none" stroke="#e9f2f0" stroke-width="4" opacity=".4"/>
  </pattern>
  <pattern id="ladrillo" width="90" height="50" patternUnits="userSpaceOnUse">
    <rect width="90" height="50" fill="#b7a07a"/>
    <path d="M0 0 H90 M0 25 H90 M45 0 V25 M0 25 V50 M90 25 V50" stroke="#7d6644" stroke-width="3" fill="none"/>
  </pattern>
  <pattern id="adoquin" width="60" height="60" patternUnits="userSpaceOnUse">
    <rect width="60" height="60" fill="#d8c398"/>
    <circle cx="15" cy="15" r="11" fill="#c4ad80"/><circle cx="45" cy="45" r="11" fill="#c4ad80"/>
  </pattern>
  <pattern id="burbujas" width="60" height="60" patternUnits="userSpaceOnUse">
    <circle cx="15" cy="20" r="7" fill="#efffd9"/><circle cx="42" cy="44" r="5" fill="#efffd9"/>
  </pattern>
</defs>'''


def fondo():
    s = f'<rect width="{W}" height="{H}" fill="#e7d1a0"/>'
    s += f'<rect width="{W}" height="{H}" fill="#e7d1a0" filter="url(#papel)" opacity=".75"/>'
    for _ in range(9):   # manchas de pergamino viejo
        x, y, r = azar.randint(200, W - 200), azar.randint(200, H - 200), azar.randint(120, 320)
        s += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#b88d4a" opacity=".07"/>'
    return s


def marco():
    s = f'<rect width="{W}" height="{H}" fill="url(#vineta)"/>'
    s += f'<rect x="36" y="36" width="{W - 72}" height="{H - 72}" rx="26" fill="none" stroke="{TINTA}" stroke-width="12"/>'
    s += f'<rect x="62" y="62" width="{W - 124}" height="{H - 124}" rx="18" fill="none" stroke="#7a5320" stroke-width="5" stroke-dasharray="30 10 6 10"/>'
    for (x, y) in ((62, 62), (W - 62, 62), (62, H - 62), (W - 62, H - 62)):
        s += (f'<g transform="translate({x},{y})"><circle r="46" fill="#e7d1a0" stroke="{TINTA}" stroke-width="8"/>'
              f'<path d="M0 -30 L9 -9 L30 0 L9 9 L0 30 L-9 9 L-30 0 L-9 -9 Z" fill="#8c2f1f"/></g>')
    return s


def estandarte(x, y, titulo, subtitulo, ancho=1500):
    """Título en una cinta con colas de golondrina."""
    a = ancho / 2
    s = f'<g transform="translate({x},{y})" filter="url(#sombra)">'
    s += f'<path d="M{-a - 150} 40 l90 -55 l-35 85 l35 85 l-90 -55 Z" fill="#7a1f14"/><path d="M{a + 150} 40 l-90 -55 l35 85 l-35 85 l90 -55 Z" fill="#7a1f14"/>'
    s += f'<path d="M{-a - 60} -20 H{-a} V140 H{-a - 60} Z" fill="#8f2618" stroke="{TINTA}" stroke-width="6"/><path d="M{a + 60} -20 H{a} V140 H{a + 60} Z" fill="#8f2618" stroke="{TINTA}" stroke-width="6"/>'
    s += f'<path d="M{-a} -40 Q0 -90 {a} -40 L{a} 150 Q0 100 {-a} 150 Z" fill="#a8301f" stroke="{TINTA}" stroke-width="8"/>'
    s += f'<path d="M{-a + 30} -22 Q0 -70 {a - 30} -22" fill="none" stroke="#e9c46a" stroke-width="5"/>'
    s += f'<path d="M{-a + 30} 132 Q0 84 {a - 30} 132" fill="none" stroke="#e9c46a" stroke-width="5"/>'
    s += f'<text x="0" y="52" font-size="92" font-weight="700" font-family="{FUENTE}" fill="#fff4d8" text-anchor="middle" stroke="#4a120a" stroke-width="5" paint-order="stroke">{esc(titulo)}</text>'
    s += f'<text x="0" y="112" font-size="48" font-style="italic" font-family="{TEXTO}" fill="#ffe6b0" text-anchor="middle">{esc(subtitulo)}</text>'
    return s + '</g>'


def rosa(x, y, r=150):
    s = f'<g transform="translate({x},{y})" opacity=".9">'
    s += f'<circle r="{r}" fill="#efdcae" stroke="{TINTA}" stroke-width="6"/><circle r="{r * .78}" fill="none" stroke="{TINTA}" stroke-width="3" stroke-dasharray="10 8"/>'
    for a in range(0, 360, 45):
        L = r * (1.25 if a % 90 == 0 else .8)
        p = lambda ang: (L * math.sin(math.radians(ang)), -L * math.cos(math.radians(ang)))
        (x1, y1), (x2, y2), (x3, y3) = p(a + 8), p(a), p(a - 8)
        s += f'<path d="M0 0 L{x1:.0f} {y1:.0f} L{x2:.0f} {y2:.0f} Z" fill="#8c2f1f"/>'
        s += f'<path d="M0 0 L{x3:.0f} {y3:.0f} L{x2:.0f} {y2:.0f} Z" fill="#e9c46a" stroke="{TINTA}" stroke-width="2"/>'
    s += f'<text y="{-r * 1.32:.0f}" font-size="54" font-weight="700" font-family="{FUENTE}" fill="{TINTA}" text-anchor="middle">N</text></g>'
    return s


# ── Muralla-membrana (sobre cualquier contorno muestreado) ───────────────────
def contorno_elipse(cx, cy, rx, ry, n=420):
    pts = []
    for i in range(n):
        t = 2 * math.pi * i / n
        x, y = cx + rx * math.cos(t), cy + ry * math.sin(t)
        nx, ny = math.cos(t) / rx, math.sin(t) / ry
        L = math.hypot(nx, ny)
        pts.append((x, y, nx / L, ny / L))
    return pts


def contorno_rect(x0, y0, w, h, r, paso=24):
    """Rectángulo redondeado muestreado a paso constante, con normales hacia fuera."""
    cxs = [(x0 + w - r, y0 + r, -90), (x0 + w - r, y0 + h - r, 0), (x0 + r, y0 + h - r, 90), (x0 + r, y0 + r, 180)]
    rectas = [((x0 + r, y0), (x0 + w - r, y0), (0, -1)), ((x0 + w, y0 + r), (x0 + w, y0 + h - r), (1, 0)),
              ((x0 + w - r, y0 + h), (x0 + r, y0 + h), (0, 1)), ((x0, y0 + h - r), (x0, y0 + r), (-1, 0))]
    pts = []
    for k in range(4):
        (ax, ay), (bx, by), (nx, ny) = rectas[k]
        L = math.hypot(bx - ax, by - ay)
        for i in range(int(L // paso)):
            f = i * paso / L
            pts.append((ax + (bx - ax) * f, ay + (by - ay) * f, nx, ny))
        cx, cy, a0 = cxs[k]
        narc = int((math.pi / 2 * r) // paso)
        for i in range(narc):
            a = math.radians(a0 + 90 * i / narc)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a), math.cos(a), math.sin(a)))
    return pts


def torre_muralla(x, y, r=95, alto=150):
    s = f'<g transform="translate({x:.0f},{y:.0f})" filter="url(#sombra)">'
    s += f'<path d="M{-r} 0 V{-alto} A{r} {r * .4:.0f} 0 0 1 {r} {-alto} V0 A{r} {r * .4:.0f} 0 0 1 {-r} 0 Z" fill="url(#piedra)" stroke="{TINTA}" stroke-width="7"/>'
    s += f'<ellipse cx="0" cy="{-alto}" rx="{r}" ry="{r * .4:.0f}" fill="#d8c59c" stroke="{TINTA}" stroke-width="7"/>'
    for k in range(-3, 4):
        s += f'<rect x="{k * r * .27 - 10:.0f}" y="{-alto - r * .4 - 24 + abs(k) * 3:.0f}" width="20" height="30" fill="#c8b488" stroke="{TINTA}" stroke-width="4"/>'
    s += f'<rect x="-14" y="{-alto + 40}" width="28" height="46" rx="14" fill="#ffcf6b" stroke="{TINTA}" stroke-width="4"/>'
    return s + '</g>'


def muralla(pts, torres=(), banderas=True, grosor=150):
    g = grosor / 2
    exterior = ' '.join(f'{x + nx * g:.0f},{y + ny * g:.0f}' for x, y, nx, ny in pts)
    interior = ' '.join(f'{x - nx * g:.0f},{y - ny * g:.0f}' for x, y, nx, ny in pts)
    s = f'<g filter="url(#sombra)"><path d="M{exterior} Z M{interior} Z" fill="url(#ladrillo)" fill-rule="evenodd"/></g>'
    s += f'<polygon points="{exterior}" fill="none" stroke="{TINTA}" stroke-width="7"/>'
    s += f'<polygon points="{interior}" fill="none" stroke="{TINTA}" stroke-width="6"/>'
    # bicapa: cabezas en las dos caras y colas enfrentadas en el centro
    for i, (x, y, nx, ny) in enumerate(pts):
        if i % 2:
            continue
        tx, ty = -ny, nx
        for lado in (1, -1):
            hx, hy = x + nx * lado * (g - 24), y + ny * lado * (g - 24)
            for d in (-6, 6):
                ax, ay = hx + tx * d - nx * lado * 15, hy + ty * d - ny * lado * 15
                bx, by = x + tx * d + nx * lado * 6, y + ty * d + ny * lado * 6
                s += f'<line x1="{ax:.0f}" y1="{ay:.0f}" x2="{bx:.0f}" y2="{by:.0f}" stroke="#6d5531" stroke-width="3"/>'
            s += f'<circle cx="{hx:.0f}" cy="{hy:.0f}" r="15" fill="#efe3c4" stroke="#5c4526" stroke-width="3"/>'
    # almenas por fuera
    for i, (x, y, nx, ny) in enumerate(pts):
        if i % 4:
            continue
        ang = math.degrees(math.atan2(ny, nx)) + 90
        mx, my = x + nx * (g + 18), y + ny * (g + 18)
        s += f'<rect x="{mx - 18:.0f}" y="{my - 20:.0f}" width="36" height="40" fill="#b7a07a" stroke="{TINTA}" stroke-width="4" transform="rotate({ang:.0f} {mx:.0f} {my:.0f})"/>'
    # glucocáliz: estandartes solo en la cara externa
    if banderas:
        for i, (x, y, nx, ny) in enumerate(pts):
            if i % 26 != 13:
                continue
            px, py = x + nx * (g + 40), y + ny * (g + 40)
            qx, qy = x + nx * (g + 150), y + ny * (g + 150)
            tx, ty = -ny, nx
            col = ('#8c2f1f', '#2b4a6b', '#1f6b43')[i % 3]
            s += f'<line x1="{px:.0f}" y1="{py:.0f}" x2="{qx:.0f}" y2="{qy:.0f}" stroke="{TINTA}" stroke-width="7"/>'
            s += f'<path d="M{qx:.0f} {qy:.0f} L{qx + tx * 70 - nx * 20:.0f} {qy + ty * 70 - ny * 20:.0f} L{qx - nx * 55:.0f} {qy - ny * 55:.0f} Z" fill="{col}" stroke="{TINTA}" stroke-width="4"/>'
    # torres = proteínas integrales que atraviesan la bicapa
    for i in torres:
        x, y, nx, ny = pts[i]
        s += torre_muralla(x, y)
    return s


# ── Calzadas de microtúbulos y caminos ───────────────────────────────────────
def curva(a, b, c=0):
    (x1, y1), (x2, y2) = a, b
    dx, dy = x2 - x1, y2 - y1
    L = math.hypot(dx, dy) or 1
    return (x1 + x2) / 2 - dy / L * c, (y1 + y2) / 2 + dx / L * c


def camino(a, b, c=0):
    qx, qy = curva(a, b, c)
    d = f'M{a[0]} {a[1]} Q{qx:.0f} {qy:.0f} {b[0]} {b[1]}'
    return (f'<path d="{d}" fill="none" stroke="#6d5531" stroke-width="34" stroke-linecap="round" opacity=".35"/>'
            f'<path d="{d}" fill="none" stroke="#8a6a3a" stroke-width="20" stroke-linecap="round" stroke-dasharray="1 44"/>')


def calzada(a, b, c=0):
    """Microtúbulo: calzada ancha con adoquines alternos de tubulina α (claros) y β (oscuros)."""
    qx, qy = curva(a, b, c)
    d = f'M{a[0]} {a[1]} Q{qx:.0f} {qy:.0f} {b[0]} {b[1]}'
    return (f'<path d="{d}" fill="none" stroke="{TINTA}" stroke-width="88" stroke-linecap="round" opacity=".8"/>'
            f'<path d="{d}" fill="none" stroke="#d9c49a" stroke-width="72" stroke-linecap="round"/>'
            f'<path d="{d}" fill="none" stroke="#a8875a" stroke-width="56" stroke-dasharray="26 26"/>'
            f'<path d="{d}" fill="none" stroke="#efe0b8" stroke-width="56" stroke-dasharray="26 26" stroke-dashoffset="26" opacity=".95"/>')


# ── Edificios ────────────────────────────────────────────────────────────────
def brillo(r, grad='fuego', op=.85):
    return f'<circle r="{r}" fill="url(#{grad})" opacity="{op}" filter="url(#brillo)"/>'


def llama(x, y, e=1):
    return (f'<g transform="translate({x},{y}) scale({e})"><path d="M-30 30 Q-34 -30 0 -80 Q8 -40 26 -55 Q44 -10 30 30 Z" fill="#ff8a1e" stroke="#b02a10" stroke-width="5"/>'
            f'<path d="M-12 28 Q-14 -6 2 -34 Q10 -8 14 28 Z" fill="#ffe27a"/></g>')


def biblioteca():
    s = brillo(260, 'luzcalida', .9)
    s += '<g filter="url(#sombra)">'
    s += f'<path d="M-170 120 V-120 L0 -230 L170 -120 V120 Z" fill="url(#piedra)" stroke="{TINTA}" stroke-width="8"/>'
    s += '<path d="M-190 -112 L0 -250 L190 -112" fill="none" stroke="#6b2a14" stroke-width="22" stroke-linejoin="round"/>'
    s += f'<path d="M-120 120 V-20 a120 120 0 0 1 240 0 V120 Z" fill="#5a3416" stroke="{TINTA}" stroke-width="6"/>'
    for fila, yy in enumerate((-50, 0, 50)):
        for i in range(7):
            x = -100 + i * 30
            s += f'<rect x="{x}" y="{yy}" width="22" height="42" rx="9" fill="{["#f0e2bd", "#e3cc95", "#f7ecd2"][(i + fila) % 3]}" stroke="#3b2410" stroke-width="3"/>'
    s += f'<circle cx="0" cy="-150" r="34" fill="#ffd36b" stroke="{TINTA}" stroke-width="6"/>'
    s += f'<path d="M-60 132 h120 l20 30 h-160 Z" fill="#f7ecd2" stroke="{TINTA}" stroke-width="5"/></g>'
    return s


def forja():
    s = brillo(230, 'fuego', .7)
    s += '<g filter="url(#sombra)">'
    s += f'<path d="M-200 110 V-60 L-120 -150 H120 L200 -60 V110 Z" fill="#7b6650" stroke="{TINTA}" stroke-width="8"/>'
    s += f'<rect x="80" y="-250" width="60" height="120" fill="#5c4a38" stroke="{TINTA}" stroke-width="6"/>'
    s += '<path d="M110 -260 q-40 -60 10 -110 q50 -40 10 -100" fill="none" stroke="#8a8378" stroke-width="22" opacity=".5" stroke-linecap="round"/>'
    s += '<path d="M-70 110 V20 a70 70 0 0 1 140 0 V110 Z" fill="#2b1b0e"/>'
    s += llama(0, 95, 1.2)
    # los ribosomas, adosados a los muros: por eso el retículo es «rugoso»
    for x, y in ((-175, -20), (-178, 40), (-150, 95), (175, -20), (178, 40), (150, 95), (-110, -120), (110, -120), (-40, -140), (40, -140)):
        s += f'<circle cx="{x}" cy="{y}" r="17" fill="#3a2614" stroke="#e9c46a" stroke-width="3"/>'
    return s + '</g>' + nota(0, 175, 'ribosomas en sus muros', 32)


def alquimia():
    s = brillo(180, 'acido', .45)
    s += '<g filter="url(#sombra)">'
    for x, h in ((-170, 150), (-60, 220), (60, 190), (170, 140)):
        s += f'<rect x="{x - 40}" y="{-h}" width="80" height="{h + 90}" rx="40" fill="#b79c6f" stroke="{TINTA}" stroke-width="7"/>'
    s += '<path d="M-130 -80 Q0 -150 130 -80" fill="none" stroke="#7a5a2a" stroke-width="18"/>'
    s += f'<path d="M-30 -10 h60 v40 l50 90 a20 20 0 0 1 -18 30 h-124 a20 20 0 0 1 -18 -30 l50 -90 Z" fill="#d6f0c4" stroke="{TINTA}" stroke-width="7"/>'
    s += '<path d="M-62 110 h124 l20 30 h-164 Z" fill="#e8b23a"/>'
    s += f'<circle cx="160" cy="70" r="55" fill="#c7b2ef" stroke="{TINTA}" stroke-width="7"/>'
    s += f'<circle cx="-165" cy="80" r="45" fill="#ffd27a" stroke="{TINTA}" stroke-width="7"/>'
    return s + '</g>' + nota(0, 190, 'túbulos sin ribosomas', 32)


def golgi():
    s = '<g filter="url(#sombra)">'
    s += f'<rect x="-260" y="80" width="520" height="70" fill="url(#madera)" stroke="{TINTA}" stroke-width="7"/>'
    s += ''.join(f'<rect x="{x}" y="150" width="22" height="70" fill="#6b4a24" stroke="{TINTA}" stroke-width="5"/>' for x in (-240, -120, 0, 120, 220))
    for i, ancho in enumerate((440, 400, 360, 320, 280)):
        y = -150 + i * 46
        s += f'<path d="M{-ancho / 2} {y} q{ancho / 2} 46 {ancho} 0 v24 q{-ancho / 2} 46 {-ancho} 0 Z" fill="#d6b77c" stroke="{TINTA}" stroke-width="6"/>'
    s += f'<circle cx="-250" cy="-120" r="30" fill="#efdcb3" stroke="{TINTA}" stroke-width="5"/><circle cx="-300" cy="-60" r="24" fill="#efdcb3" stroke="{TINTA}" stroke-width="5"/>'
    s += f'<circle cx="230" cy="40" r="34" fill="#efdcb3" stroke="{TINTA}" stroke-width="5"/><circle cx="300" cy="-10" r="28" fill="#efdcb3" stroke="{TINTA}" stroke-width="5"/>'
    s += '</g>'
    return s + nota(-300, -170, 'cara cis', 36) + nota(300, 110, 'cara trans', 36)


def mazmorra():
    s = brillo(230, 'acido', .8)
    s += '<g filter="url(#sombra)">'
    s += f'<ellipse cx="0" cy="20" rx="220" ry="150" fill="#3a382a" stroke="{TINTA}" stroke-width="9"/>'
    s += '<ellipse cx="0" cy="40" rx="170" ry="95" fill="#8be06a"/><ellipse cx="0" cy="40" rx="170" ry="95" fill="url(#burbujas)" opacity=".7"/>'
    s += ''.join(f'<line x1="{x}" y1="-120" x2="{x}" y2="-30" stroke="#1f1e16" stroke-width="12"/>' for x in (-90, -45, 0, 45, 90))
    s += '<path d="M-110 -120 h220" stroke="#1f1e16" stroke-width="14"/>'
    return s + '</g>' + nota(0, 205, 'hidrolasas ácidas (pH ácido)', 32)


def fragua():
    s = brillo(260, 'fuego', .75)
    s += '<g filter="url(#sombra)">'
    s += f'<ellipse rx="250" ry="150" fill="#d9a184" stroke="{TINTA}" stroke-width="9"/>'
    s += '<ellipse rx="222" ry="124" fill="#f6dcc8" stroke="#8c3b22" stroke-width="6"/>'
    # crestas: la membrana interna plegada
    s += '<path d="M-170 118 V-10 M-110 -122 V20 M-50 122 V-20 M10 -124 V25 M70 122 V-15 M130 -115 V10 M180 95 V-5" stroke="#8c3b22" stroke-width="20" stroke-linecap="round" fill="none"/>'
    s += llama(0, -10, 1.1)
    return s + '</g>' + nota(0, 205, 'doble muralla y crestas', 34)


def centrosoma():
    """Dos centriolos perpendiculares; en la vista de frente se ven sus 9 tripletes de microtúbulos."""
    s = brillo(200, 'luzcalida', .45)
    s += '<g filter="url(#sombra)">'
    for ang in range(0, 360, 24):
        r = math.radians(ang)
        s += f'<line x1="{60 * math.cos(r):.0f}" y1="{60 * math.sin(r):.0f}" x2="{230 * math.cos(r):.0f}" y2="{230 * math.sin(r):.0f}" stroke="#a8875a" stroke-width="8" opacity=".7"/>'
    s += f'<g transform="translate(-40,10) rotate(-25)"><rect x="-150" y="-50" width="190" height="100" rx="14" fill="#c7a76d" stroke="{TINTA}" stroke-width="7"/>'
    s += ''.join(f'<line x1="{x}" y1="-46" x2="{x}" y2="46" stroke="#8a6d3b" stroke-width="7"/>' for x in (-120, -90, -60, -30, 0))
    s += '</g>'
    s += f'<g transform="translate(90,-30)"><circle r="75" fill="#d9bf86" stroke="{TINTA}" stroke-width="7"/>'
    for k in range(9):
        a = math.radians(k * 40)
        cx, cy = 50 * math.cos(a), 50 * math.sin(a)
        for j in range(3):
            ox, oy = cx + (j - 1) * 12 * -math.sin(a), cy + (j - 1) * 12 * math.cos(a)
            s += f'<circle cx="{ox:.0f}" cy="{oy:.0f}" r="7" fill="#7a5a2a"/>'
    s += '</g></g>'
    return s + nota(20, 150, 'centriolos: 9 tripletes', 32)


def plaza():
    s = '<g filter="url(#sombra)">'
    s += f'<ellipse cx="0" cy="40" rx="230" ry="95" fill="url(#adoquin)" stroke="{TINTA}" stroke-width="7"/>'
    for x, c in ((-130, '#8c2f1f'), (0, '#2b4a6b'), (130, '#1f6b43')):
        s += f'<rect x="{x - 45}" y="-60" width="90" height="70" fill="#d8c39a" stroke="{TINTA}" stroke-width="6"/>'
        s += f'<path d="M{x - 60} -60 L{x} -110 L{x + 60} -60 Z" fill="{c}" stroke="{TINTA}" stroke-width="6"/>'
    # ribosomas libres: los «puestos» del mercado (dos subunidades)
    for x, y in ((-180, 60), (-90, 90), (60, 95), (150, 70), (200, 30), (-210, 15)):
        s += f'<g transform="translate({x},{y})"><circle r="16" fill="#3a2614"/><circle cx="-12" cy="-12" r="11" fill="#5a3b1d"/></g>'
    return s + '</g>'


def muelle():
    s = '<g filter="url(#sombra)">'
    s += f'<rect x="-230" y="40" width="460" height="60" fill="url(#madera)" stroke="{TINTA}" stroke-width="7"/>'
    s += ''.join(f'<rect x="{x}" y="100" width="22" height="70" fill="#6b4a24" stroke="{TINTA}" stroke-width="5"/>' for x in (-210, -90, 30, 150))
    s += f'<path d="M-150 40 q0 -120 -10 -170 M-160 -120 h110 l-110 70" fill="#f1e4c2" stroke="{TINTA}" stroke-width="6"/>'
    s += f'<circle cx="40" cy="-20" r="62" fill="#efdcb3" stroke="{TINTA}" stroke-width="7"/><circle cx="40" cy="-20" r="26" fill="#c0392b" opacity=".85"/>'
    s += f'<circle cx="160" cy="-40" r="50" fill="#efdcb3" stroke="{TINTA}" stroke-width="7"/><circle cx="160" cy="-40" r="20" fill="#2f62d6" opacity=".85"/>'
    return s + '</g>'


def torre_bomba():
    return torre_muralla(0, 60, 110, 230) + nota(0, 130, 'bomba Na⁺/K⁺: gasta ATP', 32)


def puerta_permeasas():
    s = torre_muralla(-150, 70, 80, 160) + torre_muralla(150, 70, 80, 160)
    s += f'<g filter="url(#sombra)"><path d="M-80 80 V-60 a80 80 0 0 1 160 0 V80 Z" fill="#5b4126" stroke="{TINTA}" stroke-width="7"/>'
    s += ''.join(f'<line x1="{x}" y1="-120" x2="{x}" y2="80" stroke="#2b1d0e" stroke-width="8"/>' for x in (-45, -15, 15, 45))
    return s + '</g>'


def sol():
    s = f'<g transform="translate(170,-200)">{brillo(170, "solgrad", 1)}<circle r="70" fill="#ffe066" stroke="#c98a1b" stroke-width="7"/></g>'
    s += '<g filter="url(#sombra)">'
    s += f'<ellipse rx="260" ry="140" fill="#7fb85a" stroke="{TINTA}" stroke-width="9"/>'
    s += '<ellipse rx="234" ry="116" fill="#b8e08f" stroke="#2f6b25" stroke-width="5"/>'
    for gx in (-140, -45, 50, 145):
        for k in range(5):
            s += f'<rect x="{gx - 34}" y="{-60 + k * 24}" width="68" height="17" rx="8" fill="#3f8a32" stroke="#1d4515" stroke-width="3"/>'
    return s + '</g>' + nota(0, 195, 'grana de tilacoides en el estroma', 32)


def aljibe():
    s = '<g filter="url(#sombra)">'
    s += f'<ellipse rx="300" ry="140" fill="url(#aguaviva)" stroke="{TINTA}" stroke-width="9"/>'
    s += '<path d="M-200 -10 q35 -24 70 0 t70 0 t70 0 t70 0 t70 0" fill="none" stroke="#4f8fb5" stroke-width="7"/>'
    return s + '</g>' + nota(0, 175, 'tonoplasto: la muralla de la vacuola', 32)


def polos():
    s = brillo(170, 'luzcalida', .35)
    for lado in (-1, 1):
        cx = lado * 190
        for ang in range(-60, 61, 15):
            r = math.radians(ang + (0 if lado < 0 else 180))
            s += f'<line x1="{cx}" y1="0" x2="{cx + 190 * math.cos(r):.0f}" y2="{190 * math.sin(r):.0f}" stroke="#8a6d3b" stroke-width="7"/>'
        s += f'<path d="M{cx} -55 L{cx + 35 * lado} 0 L{cx} 55 L{cx - 35 * lado} 0 Z" fill="#c7a76d" stroke="{TINTA}" stroke-width="6"/>'
    return s + nota(0, 120, 'huso sin centriolos', 32)


def nucleo(cx, cy, r):
    s = f'<g filter="url(#sombra)"><circle cx="{cx}" cy="{cy}" r="{r}" fill="#d8c08e" stroke="{TINTA}" stroke-width="10"/></g>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r - 34}" fill="#efe1bd" stroke="{TINTA}" stroke-width="8"/>'
    s += f'<circle cx="{cx}" cy="{cy}" r="{r - 17}" fill="none" stroke="#a88d5c" stroke-width="18" stroke-dasharray="4 22"/>'
    for ang in range(15, 375, 45):          # poros nucleares: puentes levadizos
        a = math.radians(ang)
        x, y = cx + (r - 17) * math.cos(a), cy + (r - 17) * math.sin(a)
        s += f'<g transform="translate({x:.0f},{y:.0f}) rotate({ang + 90})"><rect x="-26" y="-30" width="52" height="60" rx="8" fill="#5b4126" stroke="{TINTA}" stroke-width="5"/><line x1="0" y1="-26" x2="0" y2="26" stroke="#e9c46a" stroke-width="5"/></g>'
    s += f'<circle cx="{cx + r * .5:.0f}" cy="{cy + r * .35:.0f}" r="{r * .14:.0f}" fill="#8a6d3b" opacity=".85"/>'
    s += nota(cx + r * .5, cy + r * .35 + r * .14 + 40, 'nucléolo', 30)
    s += nota(cx, cy + r + 52, 'doble muralla nuclear con poros', 34)
    return s


# ── Lugares (edificio + casilla + cinta con el nombre) ───────────────────────
def cinta(x, y, nombre, bio, accion, ancho):
    a = ancho / 2
    s = f'<g transform="translate({x},{y})">'
    s += f'<path d="M{-a - 50} 10 l40 -24 l-12 46 l12 46 l-40 -24 Z" fill="#c9ae7b" stroke="{TINTA}" stroke-width="5"/>'
    s += f'<path d="M{a + 50} 10 l-40 -24 l12 46 l-12 46 l40 -24 Z" fill="#c9ae7b" stroke="{TINTA}" stroke-width="5"/>'
    alto = 150 if accion else 112
    s += f'<path d="M{-a} -24 Q0 -44 {a} -24 L{a} {alto - 24} Q0 {alto - 44} {-a} {alto - 24} Z" fill="#f6e9c8" stroke="{TINTA}" stroke-width="5"/>'
    s += f'<text x="0" y="26" font-size="50" font-weight="700" font-family="{FUENTE}" fill="{TINTA}" text-anchor="middle">{esc(nombre)}</text>'
    s += f'<text x="0" y="68" font-size="38" font-style="italic" font-family="{TEXTO}" fill="#6b4a1e" text-anchor="middle">{esc(bio)}</text>'
    if accion:
        s += f'<text x="0" y="106" font-size="33" font-family="{TEXTO}" fill="{TINTA}" text-anchor="middle">{esc(accion)}</text>'
    return s + '</g>'


ICONOS = dict(biblioteca=biblioteca, forja=forja, alquimia=alquimia, golgi=golgi, mazmorra=mazmorra, fragua=fragua,
              centrosoma=centrosoma, plaza=plaza, muelle=muelle, bomba=torre_bomba, permeasas=puerta_permeasas,
              sol=sol, aljibe=aljibe, polos=polos)


def edificio(x, y, icono, dx=0, dy=-260, escala=1.0):
    return f'<g transform="translate({x + dx},{y + dy}) scale({escala})">{ICONOS[icono]()}</g>'


def casilla(x, y, mazo, nombre, bio, accion, ancho=560):
    col = COL[mazo]
    s = f'<g filter="url(#sombra)"><circle cx="{x}" cy="{y}" r="86" fill="#f6e9c8" stroke="{TINTA}" stroke-width="8"/></g>'
    s += f'<circle cx="{x}" cy="{y}" r="70" fill="#f6e9c8" stroke="{col}" stroke-width="18"/>'
    if mazo != '-':
        s += f'<text x="{x}" y="{y + 28}" font-size="80" font-weight="700" font-family="{FUENTE}" fill="{col}" text-anchor="middle">{mazo}</text>'
    else:
        s += f'<path d="M{x - 26} {y + 18} V{y - 10} a26 26 0 0 1 52 0 V{y + 18} Z" fill="#5b4126"/>'
    s += cinta(x, y + 140, nombre, bio, accion, ancho)
    return s


MEMBRANAS = dict(muelle=1, citosol=0, centrosoma=0, biblioteca=2, forja=1, alquimia=1, golgi=1, mazmorra=1,
                 fragua=2, sol=2, aljibe=1, polos=0)


def anillos(x, y, n):
    """Número de membranas del orgánulo: 0, 1 o 2 anillos (como en la tabla de clasificación por membranas)."""
    s = f'<g transform="translate({x},{y})"><circle r="44" fill="#f6e9c8" stroke="{TINTA}" stroke-width="5"/>'
    if n == 0:
        s += f'<circle r="24" fill="none" stroke="#8a6a3a" stroke-width="6" stroke-dasharray="6 7"/><line x1="-26" y1="26" x2="26" y2="-26" stroke="#8c2f1f" stroke-width="6"/>'
    if n >= 1:
        s += f'<circle r="28" fill="none" stroke="{TINTA}" stroke-width="7"/>'
    if n == 2:
        s += f'<circle r="16" fill="none" stroke="{TINTA}" stroke-width="7"/>'
    return s + '</g>'


def trampa(a, b, c=0):
    x, y = curva(a, b, c)
    x, y = (x + (a[0] + b[0]) / 2) / 2, (y + (a[1] + b[1]) / 2) / 2
    s = f'<g transform="translate({x:.0f},{y:.0f})" filter="url(#sombra)"><circle r="50" fill="#3b3a2c" stroke="#e9c46a" stroke-width="7"/>'
    s += '<circle cy="-8" r="22" fill="#f1e4c2"/><rect x="-12" y="8" width="24" height="16" rx="4" fill="#f1e4c2"/>'
    s += '<circle cx="-8" cy="-10" r="6" fill="#3b3a2c"/><circle cx="8" cy="-10" r="6" fill="#3b3a2c"/></g>'
    return s


def leyenda_extra(x, y):
    s = f'<g filter="url(#sombra)"><rect x="{x}" y="{y}" width="760" height="150" rx="22" fill="#f6e9c8" stroke="{TINTA}" stroke-width="6"/></g>'
    s += trampa((x + 70, y + 50), (x + 70, y + 50))
    s += f'<text x="{x + 140}" y="{y + 64}" font-size="40" font-family="{TEXTO}" fill="{TINTA}">Trampa: corrige el error típico</text>'
    s += f'<g transform="translate({x + 70},{y + 112}) scale(.7)">{anillos(0, 0, 2)}</g>'
    s += f'<text x="{x + 140}" y="{y + 126}" font-size="40" font-family="{TEXTO}" fill="{TINTA}">Anillos: membranas del orgánulo</text>'
    return s


def pistas(y0):
    s = f'<text x="250" y="{y0 - 34}" font-size="48" font-weight="700" font-family="{FUENTE}" fill="{TINTA}">Homeostasis</text>'
    for i in range(11):
        x = 250 + i * 118
        s += f'<g filter="url(#sombra)"><rect x="{x}" y="{y0}" width="104" height="104" rx="16" fill="{"#e9a48f" if i <= 3 else "#f6e9c8"}" stroke="{TINTA}" stroke-width="6"/></g>'
        s += f'<text x="{x + 52}" y="{y0 + 72}" font-size="54" font-family="{FUENTE}" fill="{TINTA}" text-anchor="middle">{i}</text>'
    s += f'<text x="2950" y="{y0 - 34}" font-size="48" font-weight="700" font-family="{FUENTE}" fill="{TINTA}">Ronda</text>'
    for i in range(1, 9):
        x = 2950 + (i - 1) * 118
        s += f'<g filter="url(#sombra)"><circle cx="{x + 52}" cy="{y0 + 52}" r="52" fill="#f6e9c8" stroke="{TINTA}" stroke-width="6"/></g>'
        s += f'<text x="{x + 52}" y="{y0 + 72}" font-size="54" font-family="{FUENTE}" fill="{TINTA}" text-anchor="middle">{i}</text>'
    return s


def leyenda(y):
    nombres = [('A', 'Biomoléculas'), ('B', 'Genética'), ('C', 'Célula'), ('D', 'Metabolismo'), ('E', 'Microbiología'), ('F', 'Inmunología')]
    s = f'<text x="1640" y="{y - 34}" font-size="48" font-weight="700" font-family="{FUENTE}" fill="{TINTA}">Mazos del Tribunal</text>'
    for i, (k, n) in enumerate(nombres):
        x = 1660 + (i % 3) * 420
        yy = y + 40 + (i // 3) * 72
        s += f'<circle cx="{x}" cy="{yy - 14}" r="28" fill="#f6e9c8" stroke="{COL[k]}" stroke-width="10"/>'
        s += f'<text x="{x}" y="{yy}" font-size="40" font-weight="700" font-family="{FUENTE}" fill="{COL[k]}" text-anchor="middle">{k}</text>'
        s += f'<text x="{x + 44}" y="{yy}" font-size="42" font-family="{TEXTO}" fill="{TINTA}">{n}</text>'
    return s


def leyenda_caminos(x, y):
    s = f'<g filter="url(#sombra)"><rect x="{x}" y="{y}" width="760" height="230" rx="22" fill="#f6e9c8" stroke="{TINTA}" stroke-width="6"/></g>'
    s += camino((x + 50, y + 62), (x + 210, y + 62))
    s += f'<text x="{x + 250}" y="{y + 76}" font-size="40" font-family="{TEXTO}" fill="{TINTA}">Camino: 1 lugar por acción</text>'
    s += calzada((x + 60, y + 160), (x + 200, y + 160))
    s += f'<text x="{x + 250}" y="{y + 150}" font-size="40" font-family="{TEXTO}" fill="{TINTA}">Calzada de microtúbulos:</text>'
    s += f'<text x="{x + 250}" y="{y + 195}" font-size="40" font-family="{TEXTO}" fill="{TINTA}">hasta 3 lugares (tubulina α y β)</text>'
    return s


# ── Mar extracelular: los invasores, dibujados como son ──────────────────────
def bacteria(x, y, ang=0, e=1):
    s = f'<g transform="translate({x},{y}) rotate({ang}) scale({e})" filter="url(#sombra)">'
    s += '<path d="M-150 0 q-40 -30 -80 0 t-80 0 t-80 0" fill="none" stroke="#3b2a14" stroke-width="7"/>'
    s += f'<rect x="-150" y="-55" width="300" height="110" rx="55" fill="#a7c46a" stroke="{TINTA}" stroke-width="8"/>'
    s += '<rect x="-130" y="-38" width="260" height="76" rx="38" fill="none" stroke="#6b8a35" stroke-width="5"/>'
    s += '<path d="M-60 0 q20 -20 40 0 t40 0" fill="none" stroke="#4a6a20" stroke-width="6"/>'
    return s + '</g>'


def virus(x, y, e=1):
    s = f'<g transform="translate({x},{y}) scale({e})" filter="url(#sombra)">'
    for a in range(0, 360, 30):
        r = math.radians(a)
        s += f'<line x1="{60 * math.cos(r):.0f}" y1="{60 * math.sin(r):.0f}" x2="{95 * math.cos(r):.0f}" y2="{95 * math.sin(r):.0f}" stroke="{TINTA}" stroke-width="8"/>'
        s += f'<circle cx="{100 * math.cos(r):.0f}" cy="{100 * math.sin(r):.0f}" r="12" fill="#c06bc0" stroke="{TINTA}" stroke-width="4"/>'
    s += f'<circle r="64" fill="#e3b6e3" stroke="{TINTA}" stroke-width="8"/>'
    s += f'<polygon points="0,-34 30,-17 30,17 0,34 -30,17 -30,-17" fill="#9b4f9b" stroke="{TINTA}" stroke-width="4"/>'
    return s + '</g>'


def serpiente(x, y, e=1, voltear=False):
    f = -1 if voltear else 1
    s = f'<g transform="translate({x},{y}) scale({f * e},{e})" opacity=".85">'
    s += '<path d="M0 0 q40 -90 90 0 q40 -90 90 0 q40 -90 90 0" fill="none" stroke="#3d6b70" stroke-width="34" stroke-linecap="round"/>'
    s += '<path d="M0 0 q40 -90 90 0 q40 -90 90 0 q40 -90 90 0" fill="none" stroke="#7fb3b0" stroke-width="16" stroke-linecap="round"/>'
    s += f'<path d="M270 0 q30 -40 70 -30 q-10 30 -40 40 Z" fill="#3d6b70" stroke="{TINTA}" stroke-width="5"/><circle cx="318" cy="-22" r="6" fill="#ffd36b"/>'
    return s + '</g>'


# ── Cara A: célula animal ────────────────────────────────────────────────────
def animal():
    L = {'permeasas': (470, 1520), 'bomba': (1700, 450), 'muelle': (3720, 1260),
         'citosol': (1080, 1900), 'centrosoma': (1150, 1070), 'biblioteca': (2050, 1380),
         'forja': (2920, 960), 'alquimia': (2880, 2160), 'golgi': (3250, 1700),
         'mazmorra': (2200, 2330), 'fragua': (1620, 2400)}
    s = defs() + fondo()
    s += f'<rect x="62" y="62" width="{W - 124}" height="{H - 124}" rx="18" fill="url(#mar)" opacity=".55"/>'
    s += f'<rect x="62" y="62" width="{W - 124}" height="{H - 124}" rx="18" fill="url(#olas)"/>'
    s += nota(3720, 270, 'Mar extracelular', 58, color='#23484e')
    s += bacteria(3560, 470, -12, .8) + virus(3980, 560, .75) + bacteria(330, 2470, 20, .65)
    s += serpiente(2620, 230, .8) + serpiente(380, 820, .7, True)
    s += nota(3740, 720, 'bacterias con flagelo y virus con envoltura', 30, color='#23484e')
    s += '<ellipse cx="2100" cy="1540" rx="1700" ry="1150" fill="#efdcb2"/>'
    s += '<ellipse cx="2100" cy="1540" rx="1700" ry="1150" fill="#e7d1a0" filter="url(#papel)" opacity=".55"/>'
    s += muralla(contorno_elipse(2100, 1540, 1700, 1150), torres=(150, 250, 330))
    s += nota(2880, 330, 'Muralla = membrana: cabezas hidrófilas fuera y dentro, colas hidrófobas en el centro', 30)
    s += nota(330, 2010, 'torres = proteínas integrales', 30)
    s += nota(700, 420, 'estandartes: glucocáliz, solo por fuera', 32, rot=-28)
    s += nucleo(2050, 1380, 440)
    for a, b in [('permeasas', 'citosol'), ('permeasas', 'centrosoma'), ('bomba', 'centrosoma'), ('bomba', 'forja'),
                 ('citosol', 'centrosoma'), ('citosol', 'biblioteca'), ('citosol', 'fragua'), ('fragua', 'mazmorra'),
                 ('mazmorra', 'alquimia'), ('alquimia', 'golgi'), ('alquimia', 'muelle'), ('forja', 'biblioteca'),
                 ('citosol', 'mazmorra')]:
        s += camino(L[a], L[b])
    for a, b, c in [('centrosoma', 'forja', -280), ('forja', 'golgi', 0), ('golgi', 'muelle', 0), ('centrosoma', 'fragua', 140)]:
        s += calzada(L[a], L[b], c)
    for a, b in [('citosol', 'biblioteca'), ('fragua', 'mazmorra'), ('bomba', 'forja'), ('alquimia', 'muelle'), ('permeasas', 'centrosoma')]:
        s += trampa(L[a], L[b])
    s += edificio(*L['permeasas'], 'permeasas', dy=-270, escala=.9)
    s += edificio(*L['bomba'], 'bomba', dx=430, dy=-120, escala=.9)
    s += edificio(*L['muelle'], 'muelle', dy=-280)
    s += edificio(*L['citosol'], 'plaza', dy=-250)
    s += edificio(*L['centrosoma'], 'centrosoma', dy=-300, escala=.95)
    s += edificio(*L['biblioteca'], 'biblioteca', dy=-230, escala=.95)
    s += edificio(*L['forja'], 'forja', dy=-290, escala=.9)
    s += edificio(*L['alquimia'], 'alquimia', dx=-70, dy=-270, escala=.8)
    s += edificio(*L['golgi'], 'golgi', dy=-290, escala=.85)
    s += edificio(*L['mazmorra'], 'mazmorra', dy=-270, escala=.85)
    s += edificio(*L['fragua'], 'fragua', dy=-280, escala=.85)
    s += casilla(*L['permeasas'], '-', 'Puerta de las Permeasas', 'proteínas transportadoras', 'Recoger: 2 fichas gratis', 640)
    s += casilla(*L['bomba'], '-', 'Torre de la Bomba', 'transporte activo', 'Recoger: 1 ATP → 3 fichas')
    s += casilla(*L['muelle'], 'E', 'Muelle de Vesículas', 'endocitosis y exocitosis', 'Entregar · capturar bacterias', 600)
    s += casilla(*L['citosol'], 'D', 'Plaza del Citosol', 'glucólisis · ribosomas libres', 'Fermentar · ribosomas (mazo A)', 600)
    s += casilla(*L['centrosoma'], 'C', 'Centrosoma', 'centriolos · huso', 'Montar el huso')
    s += casilla(*L['biblioteca'], 'B', 'Gran Biblioteca', 'núcleo · ADN', 'Transcribir · replicar', 520)
    s += casilla(*L['forja'], 'A', 'Forja del RER', 'retículo endoplasmático rugoso', 'Traducir: proteína', 640)
    s += casilla(*L['alquimia'], 'A', 'Taller de Alquimia', 'retículo endoplasmático liso', 'Lípidos · destoxificar', 640)
    s += casilla(*L['golgi'], 'C', 'Puerto de Golgi', 'aparato de Golgi', 'Madurar · empaquetar')
    s += casilla(*L['mazmorra'], 'F', 'Mazmorra Ácida', 'lisosoma · hidrolasas', 'Digerir · autofagia')
    s += casilla(*L['fragua'], 'D', 'Fragua de la Mitocondria', 'respiración celular', 'Respirar: 1 glucosa → 4 ATP', 660)
    for k, n in MEMBRANAS.items():
        if k in L:
            s += anillos(L[k][0] + 112, L[k][1] - 62, n)
    s += estandarte(1080, 200, 'Crónicas de la Fortaleza Celular', 'Cara A · El Reino Animal', 1500)
    s += rosa(3990, 1960, 95)
    s += leyenda_caminos(3300, 2330) + leyenda_extra(3300, 2160)
    s += pistas(2770) + leyenda(2770)
    s += marco()
    return s


# ── Cara B: célula vegetal ───────────────────────────────────────────────────
def vegetal():
    L = {'permeasas': (450, 1500), 'bomba': (1120, 470), 'muelle': (3740, 1700),
         'citosol': (900, 2230), 'polos': (760, 1080), 'biblioteca': (1360, 1200),
         'sol': (2120, 860), 'fragua': (2900, 860), 'forja': (2120, 1540), 'golgi': (3200, 1560),
         'alquimia': (3150, 2230), 'aljibe': (2050, 2230)}
    s = defs() + fondo()
    # empalizada: pared celular de celulosa, atravesada por plasmodesmos
    x0, y0, w, h = 150, 150, W - 300, H - 520
    s += f'<g filter="url(#sombra)"><rect x="{x0}" y="{y0}" width="{w}" height="{h}" rx="140" fill="url(#madera)" stroke="{TINTA}" stroke-width="10"/></g>'
    for x in range(x0 + 160, x0 + w - 140, 62):
        s += f'<path d="M{x} {y0 + 12} l18 -40 l18 40 Z" fill="#a8743c" stroke="{TINTA}" stroke-width="4"/>'
        s += f'<path d="M{x} {y0 + h - 12} l18 40 l18 -40 Z" fill="#a8743c" stroke="{TINTA}" stroke-width="4"/>'
    for yy in (900, 1700):
        s += f'<rect x="{x0 + w - 70}" y="{yy}" width="80" height="110" rx="20" fill="#3a2614" stroke="{TINTA}" stroke-width="6"/>'
        s += f'<rect x="{x0 - 10}" y="{yy + 200}" width="80" height="110" rx="20" fill="#3a2614" stroke="{TINTA}" stroke-width="6"/>'
    s += nota(x0 + w - 90, 1060, 'plasmodesmo', 32, ancla='end')
    s += nota(W / 2, y0 + h + 72, 'Empalizada = pared celular de celulosa: protege y evita que la célula estalle', 38)
    s += f'<rect x="300" y="300" width="{W - 600}" height="{H - 820}" rx="90" fill="#efdcb2"/>'
    s += f'<rect x="300" y="300" width="{W - 600}" height="{H - 820}" rx="90" fill="#e7d1a0" filter="url(#papel)" opacity=".55"/>'
    s += muralla(contorno_rect(300, 300, W - 600, H - 820, 90), torres=(70, 190, 330), banderas=False, grosor=120)
    s += f'<g filter="url(#sombra)"><ellipse cx="2050" cy="2190" rx="700" ry="280" fill="#cfe6f2" stroke="#3d7fa8" stroke-width="14"/></g>'
    s += nucleo(1360, 1200, 360)
    for a, b in [('permeasas', 'polos'), ('permeasas', 'citosol'), ('bomba', 'polos'), ('bomba', 'sol'),
                 ('polos', 'biblioteca'), ('biblioteca', 'forja'), ('biblioteca', 'citosol'), ('forja', 'sol'),
                 ('sol', 'fragua'), ('fragua', 'golgi'), ('golgi', 'alquimia'), ('alquimia', 'muelle'),
                 ('alquimia', 'aljibe'), ('aljibe', 'citosol'), ('aljibe', 'forja')]:
        s += camino(L[a], L[b])
    for a, b, c in [('forja', 'golgi', 0), ('golgi', 'muelle', 0), ('citosol', 'polos', -170)]:
        s += calzada(L[a], L[b], c)
    for a, b in [('biblioteca', 'forja'), ('sol', 'fragua'), ('aljibe', 'citosol'), ('golgi', 'alquimia'), ('bomba', 'polos')]:
        s += trampa(L[a], L[b])
    s += edificio(*L['permeasas'], 'permeasas', dy=-270, escala=.85)
    s += edificio(*L['bomba'], 'bomba', dx=-420, dy=40, escala=.8)
    s += edificio(*L['muelle'], 'muelle', dy=-280, escala=.9)
    s += edificio(*L['citosol'], 'plaza', dy=-240, escala=.9)
    s += edificio(*L['polos'], 'polos', dy=-230, escala=.9)
    s += edificio(*L['biblioteca'], 'biblioteca', dy=-220, escala=.85)
    s += edificio(*L['sol'], 'sol', dy=-280, escala=.85)
    s += edificio(*L['fragua'], 'fragua', dy=-270, escala=.85)
    s += edificio(*L['forja'], 'forja', dy=-270, escala=.85)
    s += edificio(*L['golgi'], 'golgi', dy=-280, escala=.8)
    s += edificio(*L['alquimia'], 'alquimia', dy=-280, escala=.8)
    s += nota(2050, 1990, 'tonoplasto: la membrana de la gran vacuola', 34)
    s += casilla(*L['permeasas'], '-', 'Puerta de las Permeasas', 'proteínas transportadoras', 'Recoger: 2 fichas gratis', 640)
    s += casilla(*L['bomba'], '-', 'Torre de la Bomba', 'transporte activo', 'Recoger: 1 ATP → 3 fichas')
    s += casilla(*L['muelle'], 'E', 'Muelle de Vesículas', 'exocitosis hacia la pared', 'Entregar', 600)
    s += casilla(*L['citosol'], 'D', 'Plaza del Citosol', 'glucólisis · ribosomas libres', 'Fermentar · ribosomas (mazo A)', 600)
    s += casilla(*L['polos'], 'C', 'Polos del Huso', 'huso sin centriolos', 'Montar el huso')
    s += casilla(*L['biblioteca'], 'B', 'Gran Biblioteca', 'núcleo · ADN', 'Transcribir · replicar', 520)
    s += casilla(*L['sol'], 'D', 'Torre del Sol', 'cloroplasto · fotosíntesis', 'Fotosíntesis: 2 glucosas', 600)
    s += casilla(*L['fragua'], 'D', 'Fragua de la Mitocondria', 'respiración celular', 'Respirar: 1 glucosa → 4 ATP', 660)
    s += casilla(*L['forja'], 'A', 'Forja del RER', 'retículo endoplasmático rugoso', 'Traducir: proteína', 640)
    s += casilla(*L['golgi'], 'C', 'Puerto de Golgi', 'aparato de Golgi', 'Madurar · pared · fragmoplasto', 600)
    s += casilla(*L['alquimia'], 'A', 'Taller de Alquimia', 'retículo endoplasmático liso', 'Fabricar lípidos', 640)
    s += casilla(*L['aljibe'], 'C', 'Gran Aljibe', 'vacuola central', 'Turgencia · autofagia')
    for k, n in MEMBRANAS.items():
        if k in L:
            s += anillos(L[k][0] + 112, L[k][1] - 62, n)
    s += estandarte(1150, 200, 'Crónicas de la Fortaleza Celular', 'Cara B · El Reino Vegetal', 1500)
    s += leyenda_caminos(3240, 390) + leyenda_extra(3240, 640)
    s += pistas(2770) + leyenda(2770)
    s += marco()
    return s


def svg(cuerpo):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="420mm" height="297mm">'
            + cuerpo + '</svg>\n')


def main():
    carpeta = RAIZ / 'juego-fortaleza'
    carpeta.mkdir(exist_ok=True)
    (carpeta / 'tablero-animal.svg').write_text(svg(animal()), encoding='utf-8')
    (carpeta / 'tablero-vegetal.svg').write_text(svg(vegetal()), encoding='utf-8')
    print('tableros escritos')


if __name__ == '__main__':
    main()
