# BioCelia — PAU Biología

Plataforma de preparación de la PAU de Biología para Andalucía (curso 25/26).
Recursos organizados por bloques y competencias, con enfoque en la comprensión
conceptual, la aplicación y la argumentación científica.

**Sitio publicado:** https://maoles77-dotcom.github.io/biocelia/

## Secciones

| Página | Contenido |
| --- | --- |
| `index.html` | Portada y navegación |
| `orientacionespau.html` | Saberes básicos, resultados de aprendizaje y criterios de evaluación |
| `resumenespau.html` | Resúmenes y apuntes por bloques temáticos |
| `Entrenamientopau.html` | Banco de 766 preguntas con criterios de corrección y tips, más diccionario de 805 términos |
| `simulacropau.html` | 572 preguntas con estructura de examen |
| `laboratoriocompetencial.html` | Casos de razonamiento científico |
| `laboratorioinvestigacion.html` | «Tu primer año en el laboratorio»: 19 expedientes que aplican las novedades de la PAU 2026-27, con decisiones, informe modelo y progreso |

## Ver en local

Basta abrir `index.html` en el navegador. Cuando los datos se separen a
`data/*.json` (fase 3 de la hoja de ruta) hará falta un servidor local, porque
el navegador bloquea `fetch` sobre `file://`:

```bash
python -m http.server 8000
# después: http://localhost:8000
```

## Exámenes PAU de años anteriores

Cada año se transcribe en `data/historico/pau-AAAA.json`: enunciado oficial,
solución según los criterios oficiales de corrección y, si la hay, la figura
extraída del PDF. Después se ejecuta:

```bash
python tools/generar_banco_historico.py
```

que regenera `data/preguntas-historico.js` (lo cargan Entrenamiento y
Simulacro) y añade las preguntas a `preguntasjsonentrenamiento.json` y
`preguntasjsonsimulacro.json` sin duplicar. En el simulacro, las preguntas
de 2 puntos con figura van a la Parte I y el resto a la Parte II; las de 1
punto se unen de dos en dos (apartados I y II) para no perder ninguna.

En las soluciones, `**texto**` marca las palabras clave de los criterios
oficiales (se ven resaltadas) y `((texto))` lo que ha redactado BioCelia y
no está en los criterios (se ve en morado). Las figuras se recortan del PDF
a 200 ppp en `assets/figuras/historico/AAAA/` para conservar las etiquetas.

Incorporados: 2010 a 2014 (348 preguntas; de 2012 no está el examen 2) y el modelo oficial de prueba de las Directrices 2026-27 (8 preguntas, etiqueta «Modelo 26-27»).

## Qué no está en el repositorio

El material fuente —273 PDF de exámenes y criterios, presentaciones, resúmenes
y apuntes, 922 MB en total— se mantiene en local y está excluido en
`.gitignore`. Al repositorio solo suben la aplicación y, más adelante, las
figuras extraídas de los exámenes oficiales en formato WebP, con su procedencia
registrada.

## Estado

Publicación inicial: las seis páginas tal como estaban, servidas desde GitHub
Pages. Pendiente, por orden:

1. Sistema visual unificado y navegación inyectada desde un solo archivo
2. Datos fuera del HTML, a `data/*.json`, con identificadores estables
3. Extracción e indexado de las figuras de los PDF
4. Vinculación pregunta ↔ figura con revisión humana
5. Manifest y service worker para instalación como app móvil

## Licencia

© 2026 María Dolores Gámez Ortiz.
Contenido bajo [Licencia Creative Commons Atribución 4.0 Internacional](http://creativecommons.org/licenses/by/4.0/).
