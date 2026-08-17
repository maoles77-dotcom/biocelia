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
| `Entrenamientopau.html` | Banco de 258 preguntas con criterios de corrección y tips, más diccionario de 805 términos |
| `simulacropau.html` | 122 preguntas con estructura de examen |
| `laboratoriocompetencial.html` | Casos de razonamiento científico |

## Ver en local

Basta abrir `index.html` en el navegador. Cuando los datos se separen a
`data/*.json` (fase 3 de la hoja de ruta) hará falta un servidor local, porque
el navegador bloquea `fetch` sobre `file://`:

```bash
python -m http.server 8000
# después: http://localhost:8000
```

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
