# Genera los PDF de los apuntes (tema completo, resumen y presentación) con Chrome sin ventana.
# Uso: python tools/generar_pdf_temas.py            -> todos los temas/*.html
#      python tools/generar_pdf_temas.py a1          -> solo los que empiezan por "a1"
import functools, http.server, os, subprocess, sys, threading
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
CHROME = next((p for p in (
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
) if os.path.exists(p)), None)

def main():
    if not CHROME:
        sys.exit("No encuentro Chrome ni Edge.")
    filtro = sys.argv[1] if len(sys.argv) > 1 else ""
    paginas = sorted(p for p in (RAIZ / "temas").glob("*.html") if p.name.startswith(filtro))
    (RAIZ / "temas" / "pdf").mkdir(exist_ok=True)

    class Silencioso(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    manejador = functools.partial(Silencioso, directory=str(RAIZ))
    servidor = http.server.ThreadingHTTPServer(("127.0.0.1", 0), manejador)
    threading.Thread(target=servidor.serve_forever, daemon=True).start()
    puerto = servidor.server_address[1]

    for p in paginas:
        salida = RAIZ / "temas" / "pdf" / (p.stem + ".pdf")
        subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
                        "--virtual-time-budget=5000", f"--print-to-pdf={salida}",
                        f"http://127.0.0.1:{puerto}/temas/{p.name}"],
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        print("ok", salida.relative_to(RAIZ))
    servidor.shutdown()

if __name__ == "__main__":
    main()
