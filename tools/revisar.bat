@echo off
REM ═══════════════════════════════════════════════════════════════
REM  Abre el revisor de BioCelia.
REM
REM  Levanta un servidor local en la carpeta del proyecto y abre el
REM  navegador. Hace falta el servidor porque el navegador bloquea la
REM  lectura de archivos vecinos cuando la página se abre con doble
REM  clic, y sin eso el revisor no puede cargar los JSON solo.
REM
REM  Para cerrarlo: cierra esta ventana negra.
REM ═══════════════════════════════════════════════════════════════
setlocal
cd /d "%~dp0.."

set PY=%LOCALAPPDATA%\Programs\Python\Python312\python.exe
if not exist "%PY%" set PY=python

echo.
echo   Revisor BioCelia
echo   ----------------
echo   Servidor en http://localhost:8765
echo   Cierra esta ventana cuando termines.
echo.

start "" "http://localhost:8765/tools/revisor.html"
"%PY%" -m http.server 8765
