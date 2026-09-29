"""Genera el banco de preguntas de exámenes PAU de años anteriores.

Fuente única: data/historico/pau-AAAA.json (una por año, transcrita de los
exámenes y de los criterios oficiales de corrección).

Salidas:
  - data/preguntas-historico.js  → lo cargan Entrenamientopau.html y
    simulacropau.html con <script src>, igual que preguntas-figuras.js.
  - preguntasjsonentrenamiento.json y preguntasjsonsimulacro.json → se
    sustituyen las entradas históricas anteriores (campo "clave") por las
    nuevas, así que el script se puede ejecutar varias veces sin duplicar.

Reparto para el simulacro (formato 2025, todas las preguntas valen 2 puntos):
  - preguntas 1-3 (2 puntos, desarrollo)  → Parte II, electivas
  - pregunta 6 (2 puntos, con figura)     → Parte I, competenciales
  - preguntas 4-5 (1 punto)               → solo en Entrenamiento

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


def texto_plano(html):
    """Quita etiquetas para los JSON, que guardan texto sin formato."""
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


def validar(anio, examen, p):
    ref = f"{anio['anio']} E{examen['numero']}-{p['opcion']}{p['n']}"
    if p['bloque'] not in BLOQUES:
        raise SystemExit(f'{ref}: bloque desconocido «{p["bloque"]}»')
    if not p.get('c'):
        raise SystemExit(f'{ref}: sin criterios de corrección')
    figura = p.get('figura')
    if figura and not (ROOT / figura).is_file():
        raise SystemExit(f'{ref}: no existe la figura {figura}')


def construir(anios):
    entrenamiento, simulacro = [], []
    for anio in anios:
        a = anio['anio']
        for examen in anio['examenes']:
            documento = f"PAU Andalucía {a} · Examen {examen['numero']}"
            fuente = f"{anio['carpeta']}/{examen['enunciado']}"
            for p in examen['preguntas']:
                validar(anio, examen, p)
                clave = f"pau{a}-e{examen['numero']}-{p['opcion']}{p['n']}"
                puntos = 1 if p['n'] in (4, 5) else 2
                figura = p.get('figura')
                ref = f"Examen {examen['numero']}, opción {p['opcion']}, pregunta {p['n']}"
                comun = {
                    'id': clave,
                    'block': p['bloque'],
                    'topic': p['tema'],
                    'anio': a,
                    'hasImg': bool(figura),
                    'q': p['q'],
                    'c': p['c'],
                    'origen': {
                        'documento': documento,
                        'referencia': ref,
                        'fuente': fuente,
                        'criterios': f"{anio['carpeta']}/{examen['criterios']}",
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
                    'f': (f"Pregunta oficial de la PAU de Andalucía {anio['curso']} "
                          f"({ref}, {puntos} {'punto' if puntos == 1 else 'puntos'}). "
                          "La solución sigue los criterios específicos de corrección "
                          "oficiales: fíjate en cuánto vale cada idea."),
                })
                if p['n'] in (1, 2, 3, 6):
                    simulacro.append({**comun, 'isNew': p['n'] == 6})
    return entrenamiento, simulacro


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
        entrada = {
            'id': siguiente,
            'clave': p['id'],
            'bloque': p['block'],
            'tema': p['topic'],
            'tipo': tipo,
            'pregunta': texto_plano(p['q']),
            'respuesta': [texto_plano(c) for c in p['c']],
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
    print(f'Entrenamiento: {len(entrenamiento)} preguntas históricas.')
    print(f'Simulacro: {len(simulacro)} ({competenciales} Parte I, '
          f'{len(simulacro) - competenciales} Parte II).')


if __name__ == '__main__':
    main()
