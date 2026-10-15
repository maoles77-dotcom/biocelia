#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Prepara las coordenadas 3D de los visores de los apuntes (assets/moleculas/).

Las moléculas salen de PubChem (conformero 3D) o del Protein Data Bank y solo se
reorientan para que se vean bien, sin tocar su geometría:

- gliceraldehído: el D se orienta con la cadena carbonada en vertical (como en
  la proyección de Fischer) y el L se obtiene reflejándolo en un plano, que es
  exactamente lo que es un enantiómero. Se comprueba que el reflejo sea (S).
- glucosa: la β se superpone a la α por los seis átomos del anillo (Kabsch), así
  las dos se ven en la misma postura y solo cambia el –OH del carbono anomérico.

Uso: python tools/moleculas_3d.py
"""
from pathlib import Path
import numpy as np

DIR = Path(__file__).resolve().parent.parent / "assets" / "moleculas"


def leer_sdf(ruta):
    lineas = ruta.read_text(encoding="utf-8").splitlines()
    na, nb = int(lineas[3][:3]), int(lineas[3][3:6])
    atomos = [(l[31:34].strip(), np.array([float(l[0:10]), float(l[10:20]), float(l[20:30])])) for l in lineas[4:4 + na]]
    enlaces = [(int(l[0:3]) - 1, int(l[3:6]) - 1, int(l[6:9])) for l in lineas[4 + na:4 + na + nb]]
    return atomos, enlaces


def escribir_sdf(ruta, titulo, atomos, enlaces, nota):
    out = [titulo, "  BioCelia (coordenadas de PubChem, solo reorientadas)", nota,
           f"{len(atomos):3d}{len(enlaces):3d}  0  0  0  0  0  0  0  0999 V2000"]
    for el, p in atomos:
        out.append(f"{p[0]:10.4f}{p[1]:10.4f}{p[2]:10.4f} {el:<3} 0  0  0  0  0  0  0  0  0  0  0  0")
    for a, b, o in enlaces:
        out.append(f"{a + 1:3d}{b + 1:3d}{o:3d}  0  0  0  0")
    out += ["M  END", "$$$$", ""]
    ruta.write_text("\n".join(out), encoding="utf-8")


def vecinos(enlaces, i):
    return [b if a == i else a for a, b, _ in enlaces if i in (a, b)]


def quiral_rs(atomos, enlaces, c):
    """Configuración R/S de un carbono con prioridades CIP sencillas (válido para el gliceraldehído)."""
    def prioridad(i, desde):
        el = atomos[i][0]
        z = {"O": 8, "N": 7, "C": 6, "H": 1}[el]
        sus = sorted((({"O": 8, "N": 7, "C": 6, "H": 1}[atomos[j][0]]) for j in vecinos(enlaces, i) if j != desde), reverse=True)
        dobles = [o for a, b, o in enlaces if i in (a, b) and o == 2]
        if dobles:  # el C=O del aldehído cuenta el O dos veces
            sus = sorted(sus + [8], reverse=True)
        return (z, sus)
    vs = vecinos(enlaces, c)
    orden = sorted(vs, key=lambda j: prioridad(j, c), reverse=True)
    a, b, cc, d = (atomos[j][1] - atomos[c][1] for j in orden)
    giro = np.dot(np.cross(a - d, b - d), cc - d)
    return "R" if giro < 0 else "S"


def kabsch(P, Q):
    """Rotación que lleva P (centrado) sobre Q (centrado)."""
    H = P.T @ Q
    U, S, Vt = np.linalg.svd(H)
    d = np.sign(np.linalg.det(Vt.T @ U.T))
    D = np.diag([1, 1, d])
    return Vt.T @ D @ U.T


def gliceraldehido():
    atomos, enlaces = leer_sdf(DIR / "d-gliceraldehido-pubchem.sdf")
    C = [i for i, (el, _) in enumerate(atomos) if el == "C"]
    pesados = lambda i: [j for j in vecinos(enlaces, i) if atomos[j][0] != "H"]
    c2 = next(i for i in C if len(pesados(i)) == 3)
    c1 = next(i for i in C if i != c2 and any(o == 2 for a, b, o in enlaces if i in (a, b)))
    c3 = next(i for i in C if i not in (c1, c2))
    pos = np.array([p for _, p in atomos]); centro = pos[c2].copy(); pos -= centro
    # eje y: de C3 a C1 (el carbonilo arriba, como en Fischer)
    y = pos[c1] - pos[c3]; y /= np.linalg.norm(y)
    oh = next(j for j in pesados(c2) if atomos[j][0] == "O")
    x = pos[oh] - np.dot(pos[oh], y) * y; x /= np.linalg.norm(x)
    z = np.cross(x, y)
    R = np.vstack([x, y, z])
    pos = pos @ R.T
    d_atomos = [(el, p) for (el, _), p in zip(atomos, pos)]
    l_atomos = [(el, p * np.array([-1, 1, 1])) for el, p in d_atomos]
    assert quiral_rs(d_atomos, enlaces, c2) == "R" and quiral_rs(l_atomos, enlaces, c2) == "S"
    escribir_sdf(DIR / "d-gliceraldehido.sdf", "D-gliceraldehido", d_atomos, enlaces, "PubChem CID 79014, (2R)")
    escribir_sdf(DIR / "l-gliceraldehido.sdf", "L-gliceraldehido", l_atomos, enlaces,
                 "Reflejo especular del D-gliceraldehido (PubChem CID 79014): (2S), como el CID 439723")
    print("gliceraldehído: D =", quiral_rs(d_atomos, enlaces, c2), "· L =", quiral_rs(l_atomos, enlaces, c2))


def anillo(atomos, enlaces):
    """Átomos del anillo de piranosa en orden O5, C1, C2, C3, C4, C5."""
    pesados = lambda i: [j for j in vecinos(enlaces, i) if atomos[j][0] != "H"]
    o5 = next(i for i, (el, _) in enumerate(atomos) if el == "O" and sum(atomos[j][0] == "C" for j in vecinos(enlaces, i)) == 2)
    c1 = next(j for j in vecinos(enlaces, o5) if sum(atomos[k][0] == "O" for k in vecinos(enlaces, j)) == 2)
    orden, prev, cur = [o5, c1], o5, c1
    while len(orden) < 6:
        nxt = next(j for j in pesados(cur) if j != prev and atomos[j][0] == "C" and j not in orden
                   and (len(orden) < 5 or o5 in vecinos(enlaces, j)))
        orden.append(nxt); prev, cur = cur, nxt
    return orden


def glucosas():
    a_at, a_en = leer_sdf(DIR / "alfa-glucosa-pubchem.sdf")
    b_at, b_en = leer_sdf(DIR / "beta-glucosa-pubchem.sdf")
    ra, rb = anillo(a_at, a_en), anillo(b_at, b_en)
    A = np.array([a_at[i][1] for i in ra]); B = np.array([b_at[i][1] for i in rb])
    ca, cb = A.mean(0), B.mean(0)
    # orientación de la α: plano medio del anillo horizontal (normal en z) y C1 a la derecha
    pa = np.array([p for _, p in a_at]) - ca
    _, _, vt = np.linalg.svd(A - ca); nrm = vt[2]
    x = (a_at[ra[1]][1] - ca); x -= np.dot(x, nrm) * nrm; x /= np.linalg.norm(x)
    # anillo de canto: la normal del anillo en vertical (y) e inclinado 22° hacia el observador,
    # para que se vea si el –OH del C1 es axial (vertical) o ecuatorial (hacia el lado)
    if np.dot(np.cross(x, nrm), a_at[ra[3]][1] - ca) > 0: nrm = -nrm
    Ror = np.vstack([x, nrm, np.cross(x, nrm)])
    t = np.radians(22); Ror = np.array([[1, 0, 0], [0, np.cos(t), -np.sin(t)], [0, np.sin(t), np.cos(t)]]) @ Ror
    pa = pa @ Ror.T
    # como en Haworth: el –OH del C1 de la α hacia abajo (si queda arriba, giro de 180° sobre el eje x)
    o1 = next(j for j in vecinos(a_en, ra[1]) if a_at[j][0] == "O" and j != ra[0])
    if pa[o1][1] > 0:
        F = np.diag([1, -1, -1]); Ror = F @ Ror; pa = pa @ F.T
    R = kabsch(B - cb, A - ca)
    pb = ((np.array([p for _, p in b_at]) - cb) @ R.T) @ Ror.T
    rms = np.sqrt((((B - cb) @ R.T - (A - ca)) ** 2).sum(1).mean())
    escribir_sdf(DIR / "alfa-glucosa.sdf", "alfa-D-glucopiranosa", [(el, p) for (el, _), p in zip(a_at, pa)], a_en, "PubChem CID 79025")
    escribir_sdf(DIR / "beta-glucosa.sdf", "beta-D-glucopiranosa", [(el, p) for (el, _), p in zip(b_at, pb)], b_en,
                 "PubChem CID 64689, superpuesta a la alfa por el anillo")
    print(f"glucosas: anillos superpuestos con RMSD {rms:.3f} Å")


def descargar_ccd(codigo, nombre):
    """Coordenadas ideales del diccionario de ligandos del PDB (RCSB), si no están ya guardadas."""
    ruta = DIR / f"{nombre}-pdb.sdf"
    if not ruta.exists():
        import urllib.request
        url = f"https://files.rcsb.org/ligands/view/{codigo}_ideal.sdf"
        ruta.write_bytes(urllib.request.urlopen(url, timeout=60).read())
    return ruta


def cabeza_polar(atomos, enlaces):
    """Átomo que marca el extremo polar: P (fosfolípidos), C del –COOH (ácidos grasos) u O del –OH (colesterol)."""
    els = [el for el, _ in atomos]
    if "P" in els:
        return els.index("P")
    for i, el in enumerate(els):
        if el == "C" and sum(els[j] == "O" for j in vecinos(enlaces, i)) == 2 and \
                sum(els[j] == "C" for j in vecinos(enlaces, i)) == 1:
            return i
    return next(i for i, el in enumerate(els) if el == "O")


def lipido(codigo, nombre, nota):
    """Orienta una molécula alargada con su eje mayor en vertical y el extremo polar arriba."""
    atomos, enlaces = leer_sdf(descargar_ccd(codigo, nombre))
    pos = np.array([p for _, p in atomos]); pesados = np.array([el != "H" for el, _ in atomos])
    c = pos[pesados].mean(0); pos = pos - c
    _, _, vt = np.linalg.svd(pos[pesados])
    eje, eje2 = vt[0], vt[1]
    if np.dot(pos[cabeza_polar(atomos, enlaces)], eje) < 0:
        eje = -eje
    R = np.vstack([eje2, eje, np.cross(eje2, eje)])
    pos = pos @ R.T
    escribir_sdf(DIR / f"{nombre}.sdf", nombre, [(el, p) for (el, _), p in zip(atomos, pos)], enlaces, nota)
    alto = pos[pesados][:, 1].max() - pos[pesados][:, 1].min()
    print(f"{nombre}: {len(atomos)} átomos, {alto:.1f} Å de largo")


def alanina():
    """L-alanina de PubChem en posición de Fischer (–COOH arriba, –CH3 abajo, N y H hacia el observador)
    y la D como su reflejo. Se comprueba que la L sea (S) y la D (R)."""
    ruta = DIR / "l-alanina-pubchem.sdf"
    if not ruta.exists():
        import urllib.request
        ruta.write_bytes(urllib.request.urlopen(
            "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound/cid/5950/SDF?record_type=3d", timeout=60).read())
    atomos, enlaces = leer_sdf(ruta)
    els = [el for el, _ in atomos]
    pes = lambda i: [j for j in vecinos(enlaces, i) if els[j] != "H"]
    ca = next(i for i, el in enumerate(els) if el == "C" and len(pes(i)) == 3)
    cooh = next(j for j in pes(ca) if els[j] == "C" and sum(els[k] == "O" for k in vecinos(enlaces, j)) == 2)
    ch3 = next(j for j in pes(ca) if els[j] == "C" and j != cooh)
    n = next(j for j in pes(ca) if els[j] == "N")
    h = next(j for j in vecinos(enlaces, ca) if els[j] == "H")
    pos = np.array([p for _, p in atomos]) - atomos[ca][1]
    y = pos[cooh] - pos[ch3]; y /= np.linalg.norm(y)
    z = pos[n] / np.linalg.norm(pos[n]) + pos[h] / np.linalg.norm(pos[h]); z -= np.dot(z, y) * y; z /= np.linalg.norm(z)
    x = np.cross(y, z)
    pos = pos @ np.vstack([x, y, z]).T
    l_at = [(el, p) for el, p in zip(els, pos)]
    d_at = [(el, p * np.array([-1, 1, 1])) for el, p in l_at]
    assert quiral_rs(l_at, enlaces, ca) == "S" and quiral_rs(d_at, enlaces, ca) == "R"
    assert pos[n][0] < 0, "en la L-alanina el –NH2 debe quedar a la izquierda (Fischer)"
    escribir_sdf(DIR / "l-alanina.sdf", "L-alanina", l_at, enlaces, "PubChem CID 5950, (2S)")
    escribir_sdf(DIR / "d-alanina.sdf", "D-alanina", d_at, enlaces, "Reflejo especular de la L-alanina (PubChem CID 5950): (2R)")
    print("alanina: L = S (–NH2 a la izquierda) · D = R")


def proteina(codigo, nombre, hetero=(), orientar=False, ensamblaje=False):
    """Estructura del PDB sin aguas ni ligandos (salvo los indicados), con sus registros HELIX/SHEET."""
    import urllib.request
    txt = urllib.request.urlopen(f"https://files.rcsb.org/download/{codigo}.pdb", timeout=120).read().decode()
    if ensamblaje:   # unidad biológica: se aplican las matrices BIOMT del propio fichero (REMARK 350)
        mats = {}
        for l in txt.splitlines():
            if l.startswith("REMARK 350 BIOMOLECULE:") and not l.split(":")[1].strip() == "1":
                break                                   # solo la unidad biológica 1 (la de los autores)
            if l.startswith("REMARK 350   BIOMT"):
                k, n = int(l[18]), int(l[19:23]); v = [float(x) for x in l[23:].split()]
                mats.setdefault(n, [None] * 3)[k - 1] = v
        cadenas = "ABCDEFGH"; nuevas = []
        atomos = [l for l in txt.splitlines() if l.startswith("ATOM")]
        for i, (n, m) in enumerate(sorted(mats.items())):
            M = np.array([r[:3] for r in m]); t = np.array([r[3] for r in m])
            for l in atomos:
                p = np.array([float(l[30:38]), float(l[38:46]), float(l[46:54])]) @ M.T + t
                nuevas.append(l[:21] + cadenas[i] + l[22:30] + f"{p[0]:8.3f}{p[1]:8.3f}{p[2]:8.3f}" + l[54:])
            nuevas.append("TER")
        hel = [l for l in txt.splitlines() if l.startswith(("HELIX", "SHEET"))]
        # cada copia lleva sus hélices (la cadena va en las columnas 20 y 32 del registro HELIX)
        hel = [h[:19] + c + h[20:31] + c + h[32:] for c in cadenas[:len(mats)] for h in hel if h.startswith("HELIX")]
        txt = "\n".join(hel + nuevas)
    # De las hélices solo se conservan las α (clase 1 del formato PDB); las 3₁₀ y otras se ven como bucles.
    quedan = [l for l in txt.splitlines() if l.startswith(("SHEET", "ATOM", "TER"))
              or (l.startswith("HELIX") and l[38:40].strip() == "1")
              or (l.startswith("HETATM") and (l[17:20].strip() in hetero
                                              or (hetero == "*" and l[17:20].strip() not in ("HOH", "MG", "MN", "NA", "K", "CL"))))]
    if orientar:   # eje mayor en vertical y segundo eje en horizontal (solo se giran las coordenadas)
        idx = [i for i, l in enumerate(quedan) if l.startswith(("ATOM", "HETATM"))]
        P = np.array([[float(quedan[i][30:38]), float(quedan[i][38:46]), float(quedan[i][46:54])] for i in idx])
        c = P.mean(0); _, _, vt = np.linalg.svd(P - c)
        R = np.vstack([vt[1], vt[0], np.cross(vt[1], vt[0])])
        Q = (P - c) @ R.T
        for i, q in zip(idx, Q):
            l = quedan[i]; quedan[i] = l[:30] + f"{q[0]:8.3f}{q[1]:8.3f}{q[2]:8.3f}" + l[54:]
    cab = [f"REMARK   BioCelia: PDB {codigo} (RCSB Protein Data Bank), sin aguas" + (", solo girada" if orientar else "")]
    (DIR / f"{nombre}.pdb").write_text("\n".join(cab + quedan + ["END", ""]), encoding="utf-8")
    print(f"{nombre}: PDB {codigo}, {sum(l.startswith('ATOM') for l in quedan)} átomos")


if __name__ == "__main__":
    alanina()
    proteina("1UBQ", "ubiquitina")
    proteina("4HHB", "hemoglobina", hetero=("HEM",))
    proteina("9LYZ", "lisozima", hetero=("AMU", "NAG"))
    proteina("1BNA", "adn", orientar=True)
    proteina("1EHZ", "arnt", hetero="*", orientar=True)   # con sus nucleótidos modificados
    proteina("1KX5", "nucleosoma")
    proteina("1J4N", "acuaporina", ensamblaje=True)        # tetrámero (unidad biológica)
    gliceraldehido()
    glucosas()
    lipido("STE", "acido-estearico", "PDB, diccionario de ligandos: STE (coordenadas ideales)")
    lipido("OLA", "acido-oleico", "PDB, diccionario de ligandos: OLA (coordenadas ideales)")
    lipido("CLR", "colesterol", "PDB, diccionario de ligandos: CLR (coordenadas ideales)")
