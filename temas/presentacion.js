// BioCelia · Motor de las presentaciones: escala 16:9, teclado, gestos táctiles,
// pantalla completa, pasos que se revelan (.paso) y enlace directo a cada diapositiva (#5).
(function () {
  var lienzo = document.querySelector('.lienzo');
  var slides = Array.prototype.slice.call(document.querySelectorAll('.slide'));
  var total = slides.length;
  var actual = 0;

  // Pie con número de diapositiva
  var tituloTema = document.body.getAttribute('data-tema') || '';
  slides.forEach(function (s, i) {
    var pie = document.createElement('div');
    pie.className = 'pie';
    pie.innerHTML = '<span>BioCelia · ' + tituloTema + '</span><span>' + (i + 1) + ' / ' + total + '</span>';
    s.appendChild(pie);
    s.setAttribute('role', 'group');
    s.setAttribute('aria-roledescription', 'diapositiva');
    s.setAttribute('aria-label', (i + 1) + ' de ' + total);
  });

  var progreso = document.createElement('div');
  progreso.className = 'progreso';
  document.body.appendChild(progreso);

  var controles = document.createElement('div');
  controles.className = 'controles';
  controles.innerHTML =
    '<a href="' + (document.body.getAttribute('data-volver') || '../resumenespau.html') + '" title="Volver a los apuntes">✕</a>' +
    '<button type="button" data-acc="ant" aria-label="Anterior">◀</button>' +
    '<span class="contador" aria-live="polite"></span>' +
    '<button type="button" data-acc="sig" aria-label="Siguiente">▶</button>' +
    '<button type="button" data-acc="full" aria-label="Pantalla completa" title="Pantalla completa (F)">⛶</button>' +
    '<button type="button" data-acc="print" aria-label="Imprimir o guardar en PDF" title="Imprimir / PDF">🖨</button>';
  document.body.appendChild(controles);
  var contador = controles.querySelector('.contador');

  function escalar() {
    var k = Math.min(window.innerWidth / 1280, window.innerHeight / 720) * 0.98;
    lienzo.style.transform = 'scale(' + k + ')';
  }

  function pasos(s) { return Array.prototype.slice.call(s.querySelectorAll('.paso')); }

  function mostrar(n, desdeAtras) {
    actual = Math.max(0, Math.min(total - 1, n));
    slides.forEach(function (s, i) { s.classList.toggle('activa', i === actual); });
    pasos(slides[actual]).forEach(function (p) { p.classList.toggle('oculto', !desdeAtras); });
    contador.textContent = (actual + 1) + ' / ' + total;
    progreso.style.width = ((actual + 1) / total * 100) + '%';
    if (location.hash !== '#' + (actual + 1)) history.replaceState(null, '', '#' + (actual + 1));
  }

  function siguiente() {
    var oculto = slides[actual].querySelector('.paso.oculto');
    if (oculto) { oculto.classList.remove('oculto'); return; }
    if (actual < total - 1) mostrar(actual + 1);
  }
  function anterior() {
    var vistos = slides[actual].querySelectorAll('.paso:not(.oculto)');
    if (vistos.length) { vistos[vistos.length - 1].classList.add('oculto'); return; }
    if (actual > 0) mostrar(actual - 1, true);
  }
  function completa() {
    if (!document.fullscreenElement) {
      if (document.documentElement.requestFullscreen) document.documentElement.requestFullscreen();
    } else if (document.exitFullscreen) document.exitFullscreen();
  }

  controles.addEventListener('click', function (e) {
    var b = e.target.closest('button');
    if (!b) return;
    var a = b.getAttribute('data-acc');
    if (a === 'sig') siguiente();
    else if (a === 'ant') anterior();
    else if (a === 'full') completa();
    else if (a === 'print') window.print();
    b.blur();
  });

  document.addEventListener('keydown', function (e) {
    if (e.altKey || e.ctrlKey || e.metaKey) return;
    switch (e.key) {
      case 'ArrowRight': case 'PageDown': case ' ': case 'Enter': siguiente(); break;
      case 'ArrowLeft': case 'PageUp': case 'Backspace': anterior(); break;
      case 'Home': mostrar(0); break;
      case 'End': mostrar(total - 1, true); break;
      case 'f': case 'F': completa(); break;
      default: return;
    }
    e.preventDefault();
  });

  // Clic en la diapositiva: mitad derecha avanza, mitad izquierda retrocede.
  document.querySelector('.escenario').addEventListener('click', function (e) {
    if (e.target.closest('a, button, summary, details')) return;
    if (e.clientX > window.innerWidth / 2) siguiente(); else anterior();
  });

  var x0 = null;
  document.addEventListener('touchstart', function (e) { x0 = e.touches[0].clientX; }, { passive: true });
  document.addEventListener('touchend', function (e) {
    if (x0 === null) return;
    var dx = e.changedTouches[0].clientX - x0;
    if (Math.abs(dx) > 50) { if (dx < 0) siguiente(); else anterior(); }
    x0 = null;
  }, { passive: true });

  // Los controles se ocultan si el ratón no se mueve.
  var t;
  function despertar() {
    controles.classList.remove('dormido');
    clearTimeout(t);
    t = setTimeout(function () { controles.classList.add('dormido'); }, 2500);
  }
  document.addEventListener('mousemove', despertar);
  despertar();

  window.addEventListener('resize', escalar);
  window.addEventListener('hashchange', function () {
    var n = parseInt(location.hash.slice(1), 10);
    if (n && n - 1 !== actual) mostrar(n - 1);
  });

  escalar();
  var inicial = parseInt(location.hash.slice(1), 10);
  mostrar(inicial ? inicial - 1 : 0);
})();
