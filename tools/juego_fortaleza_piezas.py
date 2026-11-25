#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Piezas 3D de «Crónicas de la Fortaleza Celular» para imprimir en varios colores (Bambu Lab P1S con AMS).

Cada pieza se guarda en juego-fortaleza/piezas-3d/<pieza>/ como varios STL, uno por color (base, cuerpo, detalle,
detalle2), todos con las mismas coordenadas: en Bambu Studio se importan a la vez como una sola pieza con varias partes
y a cada parte se le asigna un filamento. También se genera una vista previa PNG de cada pieza.

Solo usa numpy y shapely: cada forma es un sólido cerrado; las formas que se tocan o se solapan dentro de un mismo STL
las une el laminador. Medidas en milímetros; la base mide 25 mm de diámetro.

Uso:  python tools/juego_fortaleza_piezas.py
"""
import math
import struct
from pathlib import Path

import numpy as np
import shapely
from shapely.geometry import Polygon, Point
from PIL import Image, ImageDraw

RAIZ = Path(__file__).resolve().parent.parent
SALIDA = RAIZ / 'juego-fortaleza' / 'piezas-3d'
SEG = 48


# ── Mallas básicas: arrays (n, 3, 3) de triángulos ───────────────────────────
def orientar(t):
    """Gira los triángulos si el volumen sale negativo (normales hacia dentro)."""
    v = np.einsum('ij,ij->i', t[:, 0], np.cross(t[:, 1], t[:, 2])).sum()
    return t[:, ::-1] if v < 0 else t


def torno(perfil, seg=SEG):
    """Revoluciona un perfil [(r, z), …] alrededor del eje z. Si empieza y acaba en r=0 es un sólido macizo;
    si no, el perfil se cierra sobre sí mismo (un anillo)."""
    p = [(float(r), float(z)) for r, z in perfil]
    cerrado = p[0][0] > 0
    if cerrado:
        p = p + [p[0]]
    ang = np.linspace(0, 2 * math.pi, seg, endpoint=False)
    c, s = np.cos(ang), np.sin(ang)
    anillos = [np.stack([r * c, r * s, np.full(seg, z)], 1) for r, z in p]
    tris = []
    for i in range(len(p) - 1):
        a, b = anillos[i], anillos[i + 1]
        r0, r1 = p[i][0], p[i + 1][0]
        for j in range(seg):
            k = (j + 1) % seg
            if r0 > 1e-9 and r1 > 1e-9:
                tris += [(a[j], a[k], b[k]), (a[j], b[k], b[j])]
            elif r0 <= 1e-9 and r1 > 1e-9:
                tris.append((a[j], b[k], b[j]))
            elif r0 > 1e-9 and r1 <= 1e-9:
                tris.append((a[j], a[k], b[j]))
    return orientar(np.array(tris))


def cilindro(r, h, z0=0.0, seg=SEG):
    return torno([(0, z0), (r, z0), (r, z0 + h), (0, z0 + h)], seg)


def cono(r0, r1, h, z0=0.0, seg=SEG):
    return torno([(0, z0), (r0, z0), (r1, z0 + h), (0, z0 + h)], seg)


def esfera(r, seg=SEG):
    n = seg // 2
    return torno([(r * math.sin(math.pi * i / n), -r * math.cos(math.pi * i / n)) for i in range(n + 1)], seg)


def toro(R, r, seg=SEG, seg2=20):
    return torno([(R + r * math.cos(2 * math.pi * i / seg2), r * math.sin(2 * math.pi * i / seg2)) for i in range(seg2)], seg)


def caja(sx, sy, sz):
    x, y, z = sx / 2, sy / 2, sz / 2
    v = np.array([[-x, -y, -z], [x, -y, -z], [x, y, -z], [-x, y, -z], [-x, -y, z], [x, -y, z], [x, y, z], [-x, y, z]])
    caras = [(0, 2, 1), (0, 3, 2), (4, 5, 6), (4, 6, 7), (0, 1, 5), (0, 5, 4), (1, 2, 6), (1, 6, 5), (2, 3, 7), (2, 7, 6), (3, 0, 4), (3, 4, 7)]
    return orientar(np.array([[v[a], v[b], v[c]] for a, b, c in caras]))


def extruir(poligono, h, z0=0.0):
    """Extruye un polígono (o varios) de shapely del plano xy entre z0 y z0+h."""
    from shapely.geometry.polygon import orient
    g = shapely.make_valid(poligono)
    piezas = [p for p in getattr(g, 'geoms', [g]) if p.geom_type == 'Polygon' and p.area > 1e-6]
    tris = []
    for p in piezas:
        p = orient(p, 1.0)                      # exterior antihorario, huecos horario
        for t in shapely.constrained_delaunay_triangles(p).geoms:
            (a, b, c) = list(t.exterior.coords)[:3]
            if (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0]) < 0:
                b, c = c, b
            tris.append(((a[0], a[1], z0), (c[0], c[1], z0), (b[0], b[1], z0)))
            tris.append(((a[0], a[1], z0 + h), (b[0], b[1], z0 + h), (c[0], c[1], z0 + h)))
        for anillo in [p.exterior] + list(p.interiors):
            pts = list(anillo.coords)
            for (x0, y0), (x1, y1) in zip(pts[:-1], pts[1:]):
                tris.append(((x0, y0, z0), (x1, y1, z0), (x1, y1, z0 + h)))
                tris.append(((x0, y0, z0), (x1, y1, z0 + h), (x0, y0, z0 + h)))
    return np.array(tris, dtype=float)


def tubo(puntos, r, seg=16):
    """Tubo cerrado de radio r a lo largo de una polilínea 3D."""
    P = np.array(puntos, dtype=float)
    T = np.gradient(P, axis=0)
    T /= np.linalg.norm(T, axis=1)[:, None]
    ref = np.array([0, 0, 1.0]) if abs(T[0, 2]) < .9 else np.array([1.0, 0, 0])
    N = np.cross(T[0], ref); N /= np.linalg.norm(N)
    anillos = []
    for i in range(len(P)):
        N = N - T[i] * np.dot(N, T[i]); N /= np.linalg.norm(N)
        B = np.cross(T[i], N)
        ang = np.linspace(0, 2 * math.pi, seg, endpoint=False)
        anillos.append(P[i] + r * (np.outer(np.cos(ang), N) + np.outer(np.sin(ang), B)))
    tris = []
    for i in range(len(P) - 1):
        a, b = anillos[i], anillos[i + 1]
        for j in range(seg):
            k = (j + 1) % seg
            tris += [(a[j], a[k], b[k]), (a[j], b[k], b[j])]
    for extremo, anillo in ((P[0], anillos[0]), (P[-1], anillos[-1])):
        for j in range(seg):
            tris.append((extremo, anillo[(j + 1) % seg], anillo[j]))
    t = np.array(tris)
    # las tapas pueden quedar invertidas respecto al tubo: se orienta todo por volumen
    return orientar(t)


def mover(t, x=0, y=0, z=0):
    return t + np.array([x, y, z])


def escalar(t, sx=1, sy=1, sz=1):
    return t * np.array([sx, sy, sz])


def girar(t, eje, grados):
    a = math.radians(grados)
    c, s = math.cos(a), math.sin(a)
    R = {'x': [[1, 0, 0], [0, c, -s], [0, s, c]], 'y': [[c, 0, s], [0, 1, 0], [-s, 0, c]], 'z': [[c, -s, 0], [s, c, 0], [0, 0, 1]]}[eje]
    return t @ np.array(R).T


def juntar(*partes):
    return np.concatenate([p for p in partes if p is not None and len(p)])


def media_elipsoide(a, b, c, seg=SEG):
    """Medio elipsoide con la cara plana en y=0 y el cuerpo hacia +y (semiejes a en x, b en y, c en z)."""
    n = seg // 4
    perfil = [(0, 0)] + [(math.cos(math.pi / 2 * i / n), math.sin(math.pi / 2 * i / n)) for i in range(n + 1)]
    t = torno(perfil, seg)            # eje z: cara plana en z=0, cuerpo hacia +z
    t = girar(t, 'x', -90)            # el eje pasa a ser y
    return orientar(escalar(t, a, b, c))


# ── La base común ────────────────────────────────────────────────────────────
def base():
    return torno([(0, 0), (12.5, 0), (12.5, 2.2), (11.8, 3), (0, 3)], 64)


Z0 = 3.0  # altura de la base


# ── Gremios ──────────────────────────────────────────────────────────────────
def almenas(r, z, n=8, tam=1.8, alto=2.2):
    return juntar(*[mover(caja(tam, tam, alto), r * math.cos(2 * math.pi * i / n), r * math.sin(2 * math.pi * i / n), z + alto / 2) for i in range(n)])


def pieza_biblioteca():
    """Núcleo: torre con doble muralla (envoltura nuclear) y portones (poros); pergamino y nucléolo."""
    cuerpo = juntar(
        torno([(9.2, Z0), (10.6, Z0), (10.6, Z0 + 7), (9.2, Z0 + 7)]),     # membrana externa
        torno([(7.2, Z0), (8.6, Z0), (8.6, Z0 + 9), (7.2, Z0 + 9)]),       # membrana interna
        cilindro(5.6, 20, Z0), almenas(5.0, Z0 + 20, 8, 2.0, 2.4),
        cilindro(10.6, 0.8, Z0), )
    poros = juntar(*[mover(girar(caja(1.6, 2.6, 4.2), 'z', a), 10.5 * math.cos(math.radians(a)), 10.5 * math.sin(math.radians(a)), Z0 + 2.4) for a in range(0, 360, 60)])
    pergamino = juntar(mover(girar(cilindro(1.6, 9, -4.5), 'y', 90), 0, 0, Z0 + 25.2),
                       mover(girar(cilindro(2.3, 0.8, -4.9), 'y', 90), 0, 0, Z0 + 25.2),
                       mover(girar(cilindro(2.3, 0.8, 4.1), 'y', 90), 0, 0, Z0 + 25.2))
    nucleolo = mover(esfera(2.2), 0, -5.6, Z0 + 13)
    return dict(cuerpo=cuerpo, detalle=juntar(poros, pergamino), detalle2=nucleolo)


def pieza_forja():
    """Retículo endoplasmático rugoso: cisternas apiladas con ribosomas por fuera; un yunque encima."""
    placa = Point(0, 0).buffer(1).simplify(0.01)
    estadio = shapely.affinity.scale(Point(0, 0).buffer(4.2, 24), 2.1, 1.0)
    capas = [extruir(estadio, 2.2, Z0 + 0.5 + i * 4.6) for i in range(3)]
    postes = [cilindro(1.6, 13.8, Z0) if False else mover(cilindro(1.4, 12.5, Z0), x, 0, 0) for x in (-6.5, 6.5)]
    yunque = Polygon([(-5.5, 0), (5.5, 0), (5.5, 1.2), (3, 1.8), (3, 3.6), (6.8, 4.4), (6.8, 6.2), (-4, 6.2), (-7.5, 5.4), (-4, 4.4), (-3, 3.6), (-3, 1.8), (-5.5, 1.2)])
    yunque = mover(girar(extruir(yunque, 4.4, -2.2), 'x', 90), 0, 0, Z0 + 0.5 + 2 * 4.6 + 2.2)
    cuerpo = juntar(*capas, *postes, yunque)
    ribos = []
    for i in range(3):
        z = Z0 + 0.5 + i * 4.6 + 1.1
        for k in range(14):
            a = 2 * math.pi * k / 14
            x, y = 8.82 * 1.02 * math.cos(a), 4.2 * 1.08 * math.sin(a)
            ribos.append(mover(esfera(1.05, 16), x, y, z))
    return dict(cuerpo=cuerpo, detalle=juntar(*ribos))


def pieza_alquimia():
    """Retículo endoplasmático liso: matraz rodeado de túbulos lisos, sin ribosomas."""
    matraz = torno([(0, Z0), (5.5, Z0), (8.2, Z0 + 4.5), (8.4, Z0 + 8), (6, Z0 + 12), (2.7, Z0 + 14.5), (2.7, Z0 + 23), (3.6, Z0 + 23.6), (3.6, Z0 + 24.8), (0, Z0 + 24.8)])
    helice = [(4.1 * math.cos(t), 4.1 * math.sin(t), Z0 + 14.8 + t * 0.55) for t in np.linspace(0, 4 * math.pi, 140)]
    tubos = juntar(tubo(helice, 0.9),
                   tubo([(8.0 * math.cos(t), 8.0 * math.sin(t), Z0 + 6.2 + 1.2 * math.sin(3 * t)) for t in np.linspace(0, 2 * math.pi, 120)], 0.9))
    liquido = torno([(7.6, Z0 + 4.4), (8.75, Z0 + 4.4), (8.9, Z0 + 7.2), (7.8, Z0 + 7.2)])
    return dict(cuerpo=matraz, detalle=tubos, detalle2=liquido)


def pieza_golgi():
    """Aparato de Golgi: cisternas curvas apiladas, con vesículas en los extremos."""
    cuerpo = []
    zc = Z0 - 6.5
    for R in (13.5, 16.0, 18.5, 21.0):
        arco = Point(0, 0).buffer(R + 1.8, 96).difference(Point(0, 0).buffer(R, 96))
        cuña = Polygon([(0, 0), (40 * math.sin(math.radians(-38)), 40 * math.cos(math.radians(-38))), (0, 40), (40 * math.sin(math.radians(38)), 40 * math.cos(math.radians(38)))])
        banda = arco.intersection(cuña)
        t = extruir(banda, 7, -3.5)               # plano xy → girar para que la curva quede en el plano xz
        t = girar(t, 'x', 90)
        cuerpo.append(mover(t, 0, 0, zc))
    cuerpo.append(mover(caja(2.2, 7, 17.6), 0, 0, Z0 + 8.8))
    vesiculas = []
    for R, lado in ((13.5, -1), (16.0, 1), (18.5, -1), (21.0, 1)):
        a = math.radians(41 * lado)
        vesiculas.append(mover(esfera(1.7, 24), (R + 0.9) * math.sin(a), 0, zc + (R + 0.9) * math.cos(a)))
    vesiculas.append(mover(esfera(2.1, 24), 0, 0, zc + 25.4))
    return dict(cuerpo=juntar(*cuerpo), detalle=juntar(*vesiculas))


def pieza_muralla():
    """Membrana plasmática: lienzo de muralla con cabezas hidrófilas en las dos caras, una torre que la atraviesa
    (proteína integral) y un estandarte solo por fuera (glucocáliz)."""
    muro = mover(caja(19, 5.2, 13), 0, 0, Z0 + 6.5)
    crenel = juntar(*[mover(caja(2.4, 5.2, 2.2), x, 0, Z0 + 14.1) for x in (-8.2, -4.1, 4.1, 8.2)])
    torre = juntar(cilindro(3.6, 19, Z0), almenas(3.2, Z0 + 19, 6, 1.6, 2.0))
    cabezas = []
    for lado in (-1, 1):
        for fila in range(3):
            for col in range(5):
                x = -8 + col * 4 + (2 if fila % 2 else 0)
                if abs(x) < 4.6 or x > 9:
                    continue
                cabezas.append(mover(esfera(1.25, 16), x, lado * 2.55, Z0 + 2.6 + fila * 3.9))
    mastil = mover(cilindro(0.55, 8, 0), -7.5, -3.6, Z0 + 10)
    bandera = mover(girar(extruir(Polygon([(0, 0), (4.6, -1.3), (0, -2.8)]), 0.9, -0.45), 'x', 90), -7.5, -3.6, Z0 + 17.8)
    return dict(cuerpo=juntar(muro, crenel, torre), detalle=juntar(*cabezas), detalle2=juntar(mastil, bandera))


def pieza_fragua():
    """Mitocondria: de pie y cortada a lo largo; doble membrana, crestas hacia dentro y una llama encima."""
    a, c = 7.2, 12.0
    Zp = Z0 + 1.6
    cuerpo = juntar(mover(media_elipsoide(a, 4.2, c), 0, 0, Zp + c), mover(caja(6, 3.6, 2.6), 0, 1.8, Z0 + 1.3))
    anillo = Point(0, 0).buffer(1, 64)
    elipse_ext = shapely.affinity.scale(anillo, a - 0.3, c - 0.3)
    elipse_int = shapely.affinity.scale(anillo, a - 1.6, c - 1.6)
    membrana_int = elipse_int.difference(shapely.affinity.scale(anillo, a - 2.6, c - 2.6))
    crestas = []
    for i, z in enumerate(np.linspace(-c + 4, c - 4, 6)):
        lado = -1 if i % 2 else 1
        x0 = lado * (a - 2.4)
        crestas.append(Polygon([(x0, z - 0.6), (x0 - lado * 4.6, z - 0.6), (x0 - lado * 4.6, z + 0.6), (x0, z + 0.6)]))
    dibujo = shapely.union_all([membrana_int] + crestas).intersection(elipse_ext)
    relieve = girar(extruir(dibujo, 1.0, 0), 'x', 90)       # plano xz, sobresale hacia -y
    relieve = mover(relieve, 0, 0.01, Zp + c)
    llama = mover(torno([(0, 0), (2.6, 1.2), (2.8, 3), (1.6, 5.4), (0, 7.6)], 24), 0, 1.6, Zp + 2 * c - 0.8)
    return dict(cuerpo=cuerpo, detalle=relieve, detalle2=llama)


def pieza_mazmorra():
    """Lisosoma: esfera de una sola membrana con rejas y burbujas de ácido."""
    Zc = Z0 + 9.0
    cuerpo = juntar(mover(esfera(7.8), 0, 0, Zc), cono(4.6, 3.6, 3.0, Z0, 40))
    rejas = [tubo([(8.0 * math.sin(t) * math.cos(a), 8.0 * math.sin(t) * math.sin(a), Zc - 8.0 * math.cos(t)) for t in np.linspace(0.55, 2.6, 30)], 0.7)
             for a in np.linspace(0, 2 * math.pi, 10, endpoint=False)]
    aros = [mover(toro(8.0 * math.sin(t), 0.8, SEG, 14), 0, 0, Zc - 8.0 * math.cos(t)) for t in (0.55, 2.6)]
    burbujas = [mover(esfera(r, 16), x, y, Zc + 7.5 + z) for x, y, z, r in ((0, 0, 1.2, 1.9), (1.8, 1, 3.6, 1.2), (-1.5, -0.8, 4.6, 0.9))]
    return dict(cuerpo=cuerpo, detalle=juntar(*rejas, *aros), detalle2=juntar(*burbujas))


def pieza_sol():
    """Cloroplasto: de pie y cortado, doble membrana, grana (pilas de tilacoides) unidas por lamelas y un sol."""
    a, c = 7.6, 10.5
    Zp = Z0 + 1.6
    cuerpo = juntar(mover(media_elipsoide(a, 4.0, c), 0, 0, Zp + c), mover(caja(6, 3.4, 2.6), 0, 1.7, Z0 + 1.3))
    anillo = Point(0, 0).buffer(1, 64)
    borde = shapely.affinity.scale(anillo, a - 0.4, c - 0.4).difference(shapely.affinity.scale(anillo, a - 1.3, c - 1.3))
    grana = []
    for gx in (-3.6, 0, 3.6):
        for k in range(5):
            grana.append(shapely.affinity.translate(shapely.box(-1.4, -0.42, 1.4, 0.42), gx, -4 + k * 1.15 + (0.6 if gx == 0 else 0)))
    lamelas = [shapely.box(-3.6, -1.0, 3.6, -0.6), shapely.box(-3.6, 1.6, 3.6, 2.0)]
    dibujo = shapely.union_all([borde] + grana + lamelas)
    relieve = mover(girar(extruir(dibujo, 1.0, 0), 'x', 90), 0, 0.01, Zp + c)
    sol = [mover(esfera(2.6, 24), 0, 1.8, Zp + 2 * c + 1.6)]
    for k in range(8):
        ang = 2 * math.pi * k / 8
        sol.append(mover(girar(cono(0.9, 0.1, 2.2, 2.4, 12), 'y', math.degrees(ang) + 90), 0, 1.8, Z0 + 2 * c + 1.6) if False else
                   mover(tubo([(2.4 * math.cos(ang), 0, 2.4 * math.sin(ang)), (4.2 * math.cos(ang), 0, 4.2 * math.sin(ang))], 0.55, 10), 0, 1.8, Zp + 2 * c + 1.6))
    return dict(cuerpo=cuerpo, detalle=relieve, detalle2=juntar(*sol))


def pieza_aljibe():
    """Vacuola: gran gota de agua (tonoplasto) dentro de una empalizada de estacas (pared celular)."""
    gota = torno([(0, Z0), (4.5, Z0 + 0.3), (7.2, Z0 + 4), (7.4, Z0 + 8), (5.8, Z0 + 12.5), (3, Z0 + 16), (0.8, Z0 + 19), (0, Z0 + 20)])
    estacas = []
    for k in range(14):
        ang = 2 * math.pi * k / 14
        x, y = 10.3 * math.cos(ang), 10.3 * math.sin(ang)
        h = 11 + (k % 2) * 1.6
        estacas.append(mover(juntar(cilindro(1.05, h, 0, 16), cono(1.05, 0.15, 1.8, h, 16)), x, y, Z0))
    travesaño = mover(toro(10.3, 0.7, 64, 12), 0, 0, Z0 + 6)
    return dict(cuerpo=gota, detalle=juntar(*estacas, travesaño))


# ── Tipos de célula ──────────────────────────────────────────────────────────
def pieza_neurona():
    soma = mover(escalar(esfera(4.6), 1, 1, 0.9), 0, 0, Z0 + 7)
    pie = cono(3.2, 2.0, 3.5, Z0, 32)
    dendritas = []
    for k in range(5):
        a = 2 * math.pi * k / 5 + 0.3
        p0 = np.array([3.6 * math.cos(a), 3.6 * math.sin(a), Z0 + 6.2])
        p1 = p0 + np.array([4.2 * math.cos(a), 4.2 * math.sin(a), -1.5])
        p2 = p1 + np.array([2.4 * math.cos(a + 0.6), 2.4 * math.sin(a + 0.6), -1.8])
        p3 = p1 + np.array([2.4 * math.cos(a - 0.6), 2.4 * math.sin(a - 0.6), 0.8])
        dendritas += [tubo([p0, (p0 + p1) / 2, p1], 0.85, 12), tubo([p1, p2], 0.6, 10), tubo([p1, p3], 0.6, 10)]
    axon = tubo([(0, 0, Z0 + 10), (0, 0, Z0 + 27)], 0.85, 14)
    botones = []
    for k in range(3):
        a = 2 * math.pi * k / 3
        p = (2.6 * math.cos(a), 2.6 * math.sin(a), Z0 + 30)
        botones += [tubo([(0, 0, Z0 + 26.8), p], 0.6, 10), mover(esfera(1.0, 14), *p)]
    mielina = [mover(cilindro(1.75, 3.6, 0, 24), 0, 0, Z0 + 12.2 + i * 4.6) for i in range(3)]
    return dict(cuerpo=juntar(soma, pie, *dendritas, axon, *botones), detalle=juntar(*mielina))


def pieza_hematie():
    """Glóbulo rojo: disco bicóncavo, de canto sobre un soporte."""
    perfil = [(0, -0.75)]
    for i in range(1, 25):
        r = 9.0 * i / 24
        x = r / 9.0
        e = 0.5 * (0.1 + 2.0 * x ** 2 - 1.12 * x ** 4) * math.sqrt(max(0.0, 1 - x ** 2)) * 9.0 / 2
        perfil.append((r, -max(e, 0.75 if i < 24 else 0.5)))
    perfil += [(r, -z) for r, z in reversed(perfil[1:])] + [(0, 0.75)]
    disco = mover(girar(torno(perfil, 64), 'x', 90), 0, 0, Z0 + 10.2)
    soporte = juntar(mover(caja(6, 5.2, 2.2), 0, 0, Z0 + 1.1))
    return dict(cuerpo=disco, detalle=soporte)


def pieza_espermatozoide():
    cola = tubo([(1.4 * math.sin(t * 1.4), 0, Z0 + t) for t in np.linspace(0, 16, 80)], 1.0, 12)
    pieza_media = cilindro(1.15, 4.6, Z0 + 16, 24)
    espiral = tubo([(1.35 * math.cos(t), 1.35 * math.sin(t), Z0 + 16 + t * 0.36) for t in np.linspace(0, 4 * math.pi, 90)], 0.4, 8)
    cabeza = mover(escalar(esfera(1, 40), 3.1, 2.0, 4.6), 0, 0, Z0 + 24.6)
    acrosoma = mover(escalar(torno([(0, 0.15)] + [(math.sin(math.pi / 2 * i / 12), 0.15 + math.cos(math.pi / 2 * i / 12)) for i in range(13)] + [(0, 0.15)][:0], 40), 3.25, 2.15, 2.9), 0, 0, Z0 + 26.6)
    pie = cilindro(2.2, 1.2, Z0, 24)
    return dict(cuerpo=juntar(cola, pieza_media, cabeza, pie), detalle=juntar(espiral, acrosoma))


def pieza_muscular():
    """Fibra muscular esquelética: cilindro estriado con muchos núcleos en la periferia."""
    fibra = juntar(cilindro(4.2, 24, Z0, 48), mover(esfera(4.2, 48), 0, 0, Z0 + 24) if False else cono(4.2, 3.2, 1.5, Z0 + 24, 48))
    estrias = [mover(toro(4.25, 0.35, 48, 10), 0, 0, Z0 + 1.6 + i * 1.6) for i in range(15)]
    nucleos = [mover(escalar(esfera(1, 20), 1.0, 1.0, 2.2), 4.3 * math.cos(a), 4.3 * math.sin(a), Z0 + z)
               for a, z in ((0.3, 5), (2.4, 9.5), (4.5, 14), (1.2, 18.5), (3.4, 22))]
    return dict(cuerpo=fibra, detalle=juntar(*estrias), detalle2=juntar(*nucleos))


def pieza_vegetal():
    """Célula vegetal: prisma con pared gruesa en las aristas, cloroplastos y núcleo desplazado."""
    citoplasma = mover(caja(13, 13, 18), 0, 0, Z0 + 9)
    aristas = []
    for sx in (-1, 1):
        for sy in (-1, 1):
            aristas.append(mover(caja(1.8, 1.8, 18.6), sx * 6.6, sy * 6.6, Z0 + 9.3))
    for z in (Z0 + 0.9, Z0 + 18):
        for sx in (-1, 1):
            aristas.append(mover(caja(1.8, 15, 1.8), sx * 6.6, 0, z))
            aristas.append(mover(caja(15, 1.8, 1.8), 0, sx * 6.6, z))
    cloros = []
    for (x, y, z, eje) in ((-6.5, -3, 5, 'x'), (-6.5, 3, 12, 'x'), (6.5, -2, 9, 'x'), (6.5, 3.5, 15, 'x'), (-2, -6.5, 14, 'y'), (3, -6.5, 6, 'y'), (0, 6.5, 10, 'y')):
        e = escalar(esfera(1, 20), 0.9 if eje == 'x' else 2.4, 0.9 if eje == 'y' else 2.4, 1.3)
        cloros.append(mover(e, x, y, Z0 + z))
    nucleo = mover(escalar(esfera(1, 24), 2.4, 0.9, 2.4), 3.6, 6.5, Z0 + 4)
    return dict(cuerpo=citoplasma, detalle=juntar(*aristas), detalle2=juntar(*cloros, nucleo))


def pieza_bacteria():
    """Bacilo inclinado, apoyado en su flagelo."""
    cuerpo = juntar(cilindro(3.6, 11, 0, 40), mover(esfera(3.6, 40), 0, 0, 0), mover(esfera(3.6, 40), 0, 0, 11))
    cuerpo = mover(girar(cuerpo, 'y', 35), -2.5, 0, Z0 + 11)
    flagelo = tubo([(-2.5 - 3.0 * math.sin(math.radians(35)) - 0.2 * t, 0.9 * math.sin(t * 1.3), Z0 + 11 - 3.0 * math.cos(math.radians(35)) - t * 0.95) for t in np.linspace(0, 8.4, 70)], 0.7, 12)
    soporte = cono(3.0, 1.8, 8.6, Z0, 32)
    return dict(cuerpo=juntar(cuerpo, mover(soporte, -2.0, 0, 0)), detalle=flagelo)


def pieza_levadura():
    """Levadura: célula ovalada con una yema (gemación)."""
    madre = juntar(mover(escalar(esfera(1, 48), 7, 7, 8), 0, 0, Z0 + 9.4), cono(4.4, 3.4, 2.6, Z0, 40))
    yema = mover(esfera(3.6, 36), 4.8, 0, Z0 + 18.0)
    cicatrices = [mover(toro(1.1, 0.35, 20, 8), *p) for p in ((-6.9, 0, Z0 + 8), (0, -6.9, Z0 + 10))]
    cicatrices = [mover(girar(toro(1.1, 0.35, 20, 8), 'y', 90), -6.95, 0, Z0 + 9.4), mover(girar(toro(1.1, 0.35, 20, 8), 'x', 90), 0, -6.95, Z0 + 11.4)]
    return dict(cuerpo=madre, detalle=yema, detalle2=juntar(*cicatrices))


PIEZAS = {
    'gremio-biblioteca': (pieza_biblioteca, 'Maestre de la Biblioteca · núcleo', dict(base='negro', cuerpo='blanco o beige', detalle='dorado', detalle2='rojo')),
    'gremio-forja': (pieza_forja, 'Maestra Forjadora · retículo endoplasmático rugoso', dict(base='negro', cuerpo='rojo o naranja', detalle='negro')),
    'gremio-alquimia': (pieza_alquimia, 'Alquimista · retículo endoplasmático liso', dict(base='negro', cuerpo='blanco o transparente', detalle='verde', detalle2='amarillo')),
    'gremio-puerto': (pieza_golgi, 'Capitana del Puerto · aparato de Golgi', dict(base='negro', cuerpo='beige o marrón', detalle='blanco')),
    'gremio-muralla': (pieza_muralla, 'Guardián de la Muralla · membrana plasmática', dict(base='negro', cuerpo='gris', detalle='blanco', detalle2='rojo')),
    'gremio-fragua': (pieza_fragua, 'Señor de la Fragua · mitocondria', dict(base='negro', cuerpo='rosa o naranja', detalle='rojo oscuro', detalle2='amarillo')),
    'gremio-mazmorra': (pieza_mazmorra, 'Carcelera de la Mazmorra · lisosoma', dict(base='negro', cuerpo='verde', detalle='gris o negro', detalle2='verde claro')),
    'gremio-sol': (pieza_sol, 'Guardiana del Sol · cloroplasto', dict(base='negro', cuerpo='verde claro', detalle='verde oscuro', detalle2='amarillo')),
    'gremio-aljibe': (pieza_aljibe, 'Señora del Aljibe · vacuola', dict(base='negro', cuerpo='azul o transparente', detalle='marrón')),
    'celula-neurona': (pieza_neurona, 'Neurona', dict(base='negro', cuerpo='amarillo', detalle='blanco')),
    'celula-globulo-rojo': (pieza_hematie, 'Glóbulo rojo', dict(base='negro', cuerpo='rojo', detalle='rojo')),
    'celula-espermatozoide': (pieza_espermatozoide, 'Espermatozoide', dict(base='negro', cuerpo='blanco', detalle='azul')),
    'celula-muscular': (pieza_muscular, 'Fibra muscular esquelética', dict(base='negro', cuerpo='rojo', detalle='blanco', detalle2='morado')),
    'celula-vegetal': (pieza_vegetal, 'Célula vegetal', dict(base='negro', cuerpo='verde claro', detalle='marrón', detalle2='verde oscuro')),
    'celula-bacteria': (pieza_bacteria, 'Bacteria (bacilo con flagelo)', dict(base='negro', cuerpo='verde', detalle='marrón')),
    'celula-levadura': (pieza_levadura, 'Levadura en gemación', dict(base='negro', cuerpo='beige', detalle='amarillo', detalle2='marrón')),
}

COLOR_VISTA = {'negro': (40, 40, 40), 'blanco': (235, 230, 215), 'dorado': (214, 168, 40), 'rojo': (196, 48, 40), 'naranja': (228, 120, 40),
               'verde': (60, 150, 60), 'verde claro': (150, 210, 110), 'verde oscuro': (30, 95, 40), 'amarillo': (240, 205, 50),
               'beige': (220, 195, 150), 'marrón': (120, 80, 45), 'gris': (150, 145, 140), 'azul': (70, 130, 210), 'rosa': (235, 150, 150),
               'morado': (120, 70, 160), 'rojo oscuro': (130, 30, 30), 'transparente': (190, 220, 235)}


def color_vista(nombre):
    return COLOR_VISTA.get(nombre.split(' o ')[0], (180, 180, 180))


# ── STL y vista previa ───────────────────────────────────────────────────────
def guardar_stl(t, ruta, nombre):
    with open(ruta, 'wb') as f:
        f.write(nombre.encode('ascii', 'replace')[:80].ljust(80, b' '))
        f.write(struct.pack('<I', len(t)))
        for a, b, c in t:
            n = np.cross(b - a, c - a)
            L = np.linalg.norm(n)
            n = n / L if L else n
            f.write(struct.pack('<12fH', *n, *a, *b, *c, 0))


def vista(partes, colores, ruta, tam=640, azimut=-35, elev=22):
    tris, cols = [], []
    for k, t in partes.items():
        tris.append(t)
        cols += [color_vista(colores[k])] * len(t)
    t = np.concatenate(tris)
    t = girar(t, 'z', azimut)
    t = girar(t, 'x', -(90 - elev))           # cámara mirando desde -y, inclinada
    n = np.cross(t[:, 1] - t[:, 0], t[:, 2] - t[:, 0])
    n /= np.linalg.norm(n, axis=1)[:, None] + 1e-12
    visibles = n[:, 2] > 0
    luz = np.array([-0.4, 0.5, 0.75]); luz /= np.linalg.norm(luz)
    brillo = 0.35 + 0.65 * np.clip(n @ luz, 0, 1)
    xy = t[:, :, :2]
    mn, mx = xy.reshape(-1, 2).min(0), xy.reshape(-1, 2).max(0)
    esc = (tam * 0.86) / max(mx - mn)
    centro = (mn + mx) / 2
    ss = 3
    img = Image.new('RGB', (tam * ss, tam * ss), (246, 238, 220))
    d = ImageDraw.Draw(img)
    orden = np.argsort(t[:, :, 2].mean(1))
    for i in orden:
        if not visibles[i]:
            continue
        p = [((x - centro[0]) * esc * ss + tam * ss / 2, -(y - centro[1]) * esc * ss + tam * ss / 2) for x, y in xy[i]]
        c = tuple(int(v * brillo[i]) for v in cols[i])
        d.polygon(p, fill=c)
    img.resize((tam, tam), Image.LANCZOS).save(ruta)


def main():
    SALIDA.mkdir(parents=True, exist_ok=True)
    resumen = []
    for clave, (funcion, titulo, colores) in PIEZAS.items():
        carpeta = SALIDA / clave
        carpeta.mkdir(exist_ok=True)
        partes = {'base': base(), **funcion()}
        for parte, t in partes.items():
            guardar_stl(t, carpeta / f'{clave}__{parte}.stl', f'{clave} {parte}')
        vista(partes, colores, carpeta / f'{clave}.png')
        alto = max(t[:, :, 2].max() for t in partes.values())
        resumen.append((clave, titulo, alto, colores))
        print(f'{clave}: {len(partes)} partes, {alto:.1f} mm de alto')
    with open(SALIDA / 'LEEME.txt', 'w', encoding='utf-8') as f:
        f.write('Piezas 3D de «Crónicas de la Fortaleza Celular»\n\n')
        f.write('Cada carpeta es una pieza. Sus STL son las partes de cada color, con las mismas coordenadas.\n'
                'En Bambu Studio: arrastra a la vez todos los STL de una carpeta y, cuando pregunte si quieres cargarlos\n'
                'como un solo objeto con varias partes, di que SÍ. Después asigna a cada parte un filamento del AMS.\n'
                'Base de 25 mm. Sin soportes, salvo lo que se indica.\n\n')
        for clave, titulo, alto, colores in resumen:
            f.write(f'{clave}  ·  {titulo}  ·  {alto:.0f} mm de alto\n')
            for parte, col in colores.items():
                f.write(f'    {parte:9s} → {col}\n')
            f.write('\n')


if __name__ == '__main__':
    main()
