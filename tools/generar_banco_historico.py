"""Genera el banco de preguntas de exámenes PAU de años anteriores.

Fuente única: data/historico/pau-AAAA.json (una por año, transcrita de los
exámenes y de los criterios oficiales de corrección).

Marcas dentro de las soluciones ("c"):
  **texto**   palabra clave que aparece en los criterios oficiales
  ((texto))   explicación redactada por BioCelia, que no está en los criterios

Salidas:
  - data/preguntas-historico.js  → lo cargan Entrenamientopau.html y
    simulacropau.html con <script src>, igual que preguntas-figuras.js.
  - preguntasjsonentrenamiento.json y preguntasjsonsimulacro.json → se
    sustituyen las entradas históricas anteriores (campo "clave") por las
    nuevas, así que el script se puede ejecutar varias veces sin duplicar.

Reparto para el simulacro (todas sus preguntas valen 2 puntos):
  - preguntas de 2 puntos con figura (o "competencial": true, p. ej. un
    esquema o datos escritos en el enunciado) → Parte I (competenciales)
  - preguntas de 2 puntos sin figura → Parte II (electivas)
  - preguntas de 1 punto → se unen de dos en dos (I y II) dentro del mismo
    examen y opción, en orden; las que quedan sueltas se emparejan con otras
    sueltas del mismo año. La pareja va a la Parte I si alguna lleva figura.

Uso:  python tools/generar_banco_historico.py
"""
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
HISTORICO = ROOT / 'data' / 'historico'
SALIDA_JS = ROOT / 'data' / 'preguntas-historico.js'
JSON_ENTRENAMIENTO = ROOT / 'preguntasjsonentrenamiento.json'
JSON_SIMULACRO = ROOT / 'preguntasjsonsimulacro.json'

BLOQUES = {'Biomoléculas', 'Genética', 'Célula', 'Metabolismo',
           'Biotecnología', 'Inmunología', 'Microbiología'}

RE_CLAVE = re.compile(r'\*\*(.+?)\*\*')
RE_REDACTADO = re.compile(r'\(\((.+?)\)\)')


def a_html(texto):
    texto = RE_CLAVE.sub(r'<mark class="clave-criterio">\1</mark>', texto)
    return RE_REDACTADO.sub(r'<span class="redactado">\1</span>', texto)


def sin_marcas(texto):
    return RE_REDACTADO.sub(r'\1', RE_CLAVE.sub(r'\1', texto))


def texto_plano(html):
    """Quita etiquetas y marcas para los JSON, que guardan texto sin formato."""
    html = sin_marcas(html)
    html = re.sub(r'<br\s*/?>', ' ', html)
    html = re.sub(r'<sup>(.*?)</sup>', r'\1', html)
    return re.sub(r'<[^>]+>', '', html).strip()


def cargar_fuentes():
    anios = []
    for ruta in sorted(HISTORICO.glob('pau-*.json')):
        anios.append(json.loads(ruta.read_text(encoding='utf-8')))
    if not anios:
        raise SystemExit(f'No hay ficheros pau-*.json en {HISTORICO}')
    return anios


def puntos_de(p):
    # 2010-2016: las preguntas 4 y 5 valen 1 punto; el resto, 2.
    return p.get('puntos', 1 if p['n'] in (4, 5) else 2)


def validar(ref, p):
    if p['bloque'] not in BLOQUES:
        raise SystemExit(f'{ref}: bloque desconocido «{p["bloque"]}»')
    if not p.get('c'):
        raise SystemExit(f'{ref}: sin criterios de corrección')
    for c in p['c']:
        if c.count('**') % 2 or c.count('((') != c.count('))'):
            raise SystemExit(f'{ref}: marcas ** o (( )) desparejadas en «{c[:60]}»')
    figura = p.get('figura')
    if figura and not (ROOT / figura).is_file():
        raise SystemExit(f'{ref}: no existe la figura {figura}')


def construir(anios):
    entrenamiento, simulacro = [], []
    for anio in anios:
        a = anio['anio']
        sueltas_anio = []
        for examen in anio['examenes']:
            ex_id = examen.get('id') or f"e{examen['numero']}"
            ex_nombre = examen.get('nombre') or f"Examen {examen['numero']}"
            documento = f"PAU {anio.get('region', 'Andalucía')} {a} · {ex_nombre}"
            fuente = f"{anio['carpeta']}/{examen['enunciado']}"
            criterios = (f"{anio['carpeta']}/{examen['criterios']}"
                         if examen.get('criterios') else None)
            de_un_punto = {}
            for p in examen['preguntas']:
                opcion = p.get('opcion', '')
                ref_txt = ', '.join(x for x in (
                    ex_nombre, f'opción {opcion}' if opcion else '',
                    f"pregunta {p['n']}") if x)
                validar(f'{a} {ref_txt}', p)
                clave = re.sub(r'[^a-z0-9-]', '', f"pau{a}-{ex_id}-{opcion}{p['n']}".lower())
                puntos = puntos_de(p)
                figura = p.get('figura')
                comun = {
                    'id': clave,
                    'block': p['bloque'],
                    'topic': p['tema'],
                    'anio': a,
                    'hasImg': bool(figura),
                    'competencial': bool(figura) or bool(p.get('competencial')),
                    'q': p['q'],
                    'c': [a_html(c) for c in p['c']],
                    'origen': {
                        'documento': documento,
                        'referencia': ref_txt,
                        'fuente': fuente,
                        'criterios': criterios,
                        'examen_anio': a,
                        'verificado': True,
                    },
                }
                if figura:
                    comun['imgSrc'] = figura
                    comun['imgThumb'] = figura.replace('.webp', '.thumb.webp')
                    comun['imageDesc'] = p.get('figuraDesc')

                entrenamiento.append({
                    **comun,
                    'isNew': False,
                    'puntos': puntos,
                    'f': (f"Pregunta oficial de la PAU {anio.get('region', 'de Andalucía')} "
                          f"{anio['curso']} ({ref_txt}, {puntos} "
                          f"{'punto' if puntos == 1 else 'puntos'}). "
                          + p.get('tip', 'Resaltadas, las palabras clave de los criterios '
                                         'oficiales de corrección: son las que puntúan.')),
                })
                if puntos >= 2:
                    simulacro.append({**comun, 'isNew': comun['competencial']})
                else:
                    de_un_punto.setdefault(opcion, []).append(comun)
            for grupo in de_un_punto.values():
                while len(grupo) >= 2:
                    simulacro.append(unir(grupo.pop(0), grupo.pop(0)))
                sueltas_anio.extend(grupo)
        while len(sueltas_anio) >= 2:
            simulacro.append(unir(sueltas_anio.pop(0), sueltas_anio.pop(0)))
        if sueltas_anio:
            # Una sola suelta en todo el año: se une a la primera de 1 punto
            # de ese año para que no se pierda.
            otra = next(q for q in entrenamiento
                        if q['anio'] == a and q['puntos'] == 1
                        and q['id'] != sueltas_anio[0]['id'])
            simulacro.append(unir(sueltas_anio[0], otra))
    return entrenamiento, simulacro


def unir(p1, p2):
    """Dos preguntas de 1 punto → una de 2 puntos con apartados I y II."""
    figura = p1.get('imgSrc') or p2.get('imgSrc')
    con_fig = p1 if p1.get('imgSrc') else p2
    unida = {
        'id': f"{p1['id']}+{p2['id'].rsplit('-', 1)[-1]}",
        'block': p1['block'],
        'topic': (p1['topic'] if p1['topic'] == p2['topic']
                  else f"{p1['topic']} · {p2['topic']}"),
        'anio': p1['anio'],
        'hasImg': bool(figura),
        'q': (f"<b>I.</b> {p1['q']} <i>(1 punto)</i><br><br>"
              f"<b>II.</b> {p2['q']} <i>(1 punto)</i>"),
        'c': [f'<b>I.</b> {c}' for c in p1['c']] + [f'<b>II.</b> {c}' for c in p2['c']],
        'isNew': p1['competencial'] or p2['competencial'],
        'competencial': p1['competencial'] or p2['competencial'],
        'unida': [p1['id'], p2['id']],
        'origen': {
            **p1['origen'],
            'referencia': f"{p1['origen']['referencia']} + {p2['origen']['referencia']}",
        },
    }
    if figura:
        unida['imgSrc'] = figura
        unida['imgThumb'] = con_fig['imgThumb']
        unida['imageDesc'] = con_fig.get('imageDesc')
        unida['origen']['documento'] = con_fig['origen']['documento']
    return unida


def escribir_js(entrenamiento, simulacro):
    datos = json.dumps({'entrenamiento': entrenamiento, 'simulacro': simulacro},
                       ensure_ascii=False, indent=1)
    cabecera = (
        '/* ══════════════════════════════════════════════════════════════\n'
        f'   Generado por tools/generar_banco_historico.py el {date.today().isoformat()}.\n'
        '   NO editar a mano: se regenera desde data/historico/pau-*.json.\n'
        f'   {len(entrenamiento)} preguntas para Entrenamiento y '
        f'{len(simulacro)} para Simulacro,\n'
        '   de exámenes PAU oficiales con sus criterios de corrección.\n'
        '   ══════════════════════════════════════════════════════════════ */\n'
    )
    SALIDA_JS.write_text(f'{cabecera}window.BIOCELIA_HISTORICO = {datos};\n',
                         encoding='utf-8')


def actualizar_json(ruta, preguntas, tipo):
    actuales = json.loads(ruta.read_text(encoding='utf-8'))
    propias = [q for q in actuales if 'clave' not in q]
    siguiente = max((q['id'] for q in propias), default=0) + 1
    for p in preguntas:
        claves = [RE_CLAVE.findall(c.replace('<mark class="clave-criterio">', '**')
                                    .replace('</mark>', '**')) for c in p['c']]
        entrada = {
            'id': siguiente,
            'clave': p['id'],
            'bloque': p['block'],
            'tema': p['topic'],
            'tipo': tipo,
            'pregunta': texto_plano(p['q']),
            'respuesta': [texto_plano(c) for c in p['c']],
            'palabras_clave': sorted({k for ks in claves for k in ks}),
            'fuente': p['origen']['fuente'],
            'criterios': p['origen']['criterios'],
            'dificultad': 'media',
        }
        if p.get('imgSrc'):
            entrada['imagen'] = p['imgSrc']
        propias.append(entrada)
        siguiente += 1
    ruta.write_text(json.dumps(propias, ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8')


def main():
    entrenamiento, simulacro = construir(cargar_fuentes())
    escribir_js(entrenamiento, simulacro)
    actualizar_json(JSON_ENTRENAMIENTO, entrenamiento, 'respuesta breve')
    actualizar_json(JSON_SIMULACRO, simulacro, 'simulacro')
    competenciales = sum(q['isNew'] for q in simulacro)
    unidas = sum('unida' in q for q in simulacro)
    print(f'Entrenamiento: {len(entrenamiento)} preguntas históricas.')
    print(f'Simulacro: {len(simulacro)} ({competenciales} Parte I, '
          f'{len(simulacro) - competenciales} Parte II; {unidas} unen dos de 1 punto).')


if __name__ == '__main__':
    main()
