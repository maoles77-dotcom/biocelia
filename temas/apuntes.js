// BioCelia · Apuntes PAU: índice activo, botón de imprimir y soluciones desplegadas al imprimir.
(function () {
  // Al imprimir (o guardar en PDF) se abren todas las soluciones y se restauran después.
  var abiertas = [];
  window.addEventListener('beforeprint', function () {
    abiertas = [];
    document.querySelectorAll('details').forEach(function (d) {
      if (!d.open) { abiertas.push(d); d.open = true; }
    });
  });
  window.addEventListener('afterprint', function () {
    abiertas.forEach(function (d) { d.open = false; });
    abiertas = [];
  });

  document.querySelectorAll('[data-imprimir]').forEach(function (b) {
    b.addEventListener('click', function () { window.print(); });
  });

  // Ampliar figuras: en el móvil los esquemas anchos quedan con letra muy pequeña. Al tocar la figura
  // (o «Ampliar») se abre a pantalla completa con zoom (+/−, pellizco) y se recorre deslizando.
  var visor = null, vImg, vTit, vCaja, zoom = 1, origen = null;
  function abrirFigura(img) {
    if (!visor) {
      visor = document.createElement('div'); visor.className = 'visor-fig'; visor.setAttribute('role', 'dialog'); visor.setAttribute('aria-modal', 'true');
      visor.innerHTML = '<div class="vf-barra"><span class="vf-tit"></span><button type="button" class="vf-btn" data-z="-1" aria-label="Reducir">−</button>' +
        '<button type="button" class="vf-btn" data-z="1" aria-label="Ampliar">+</button><button type="button" class="vf-btn vf-cerrar" aria-label="Cerrar">✕</button></div>' +
        '<div class="vf-caja"><img alt=""></div>';
      document.body.appendChild(visor);
      vImg = visor.querySelector('img'); vTit = visor.querySelector('.vf-tit'); vCaja = visor.querySelector('.vf-caja');
      visor.querySelector('.vf-cerrar').addEventListener('click', cerrarFigura);
      Array.prototype.forEach.call(visor.querySelectorAll('[data-z]'), function (b) {
        b.addEventListener('click', function () { ponerZoom(zoom * (b.dataset.z > 0 ? 1.5 : 1 / 1.5)); });
      });
      document.addEventListener('keydown', function (e) { if (e.key === 'Escape' && visor.classList.contains('abierto')) cerrarFigura(); });
    }
    origen = img;
    vImg.src = img.currentSrc || img.src; vImg.alt = img.alt;
    var cap = img.closest('figure') && img.closest('figure').querySelector('figcaption');
    vTit.textContent = cap ? cap.textContent.trim() : '';
    visor.classList.add('abierto'); document.documentElement.classList.add('vf-bloqueo');
    // en pantallas estrechas se abre ya ampliada para que la letra se lea
    ponerZoom(window.innerWidth < 700 ? Math.min(3, 760 / window.innerWidth) : 1);
    vCaja.scrollTop = 0; vCaja.scrollLeft = 0;
    visor.querySelector('.vf-cerrar').focus();
  }
  function ponerZoom(z) { zoom = Math.max(1, Math.min(5, z)); vImg.style.width = (zoom * 100) + '%'; }
  function cerrarFigura() {
    visor.classList.remove('abierto'); document.documentElement.classList.remove('vf-bloqueo');
    if (origen) origen.focus();
  }
  document.querySelectorAll('.figura img').forEach(function (img) {
    img.tabIndex = 0; img.setAttribute('role', 'button');
    img.setAttribute('aria-label', 'Ampliar figura: ' + (img.alt || ''));
    img.addEventListener('click', function () { abrirFigura(img); });
    img.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); abrirFigura(img); } });
    var b = document.createElement('button'); b.type = 'button'; b.className = 'fig-ampliar'; b.textContent = '🔍 Ampliar'; b.tabIndex = -1;
    b.setAttribute('aria-hidden', 'true');
    b.addEventListener('click', function () { abrirFigura(img); });
    img.parentNode.insertBefore(b, img);
  });

  // Tablas: si no están ya en un contenedor desplazable, se envuelven para que en el móvil se deslicen sin desbordar la página.
  document.querySelectorAll('table').forEach(function (t) {
    if (t.closest('.tabla-wrap')) return;
    var w = document.createElement('div'); w.className = 'tabla-wrap';
    t.parentNode.insertBefore(w, t); w.appendChild(t);
  });

  // En pantallas anchas el índice queda desplegado; en el móvil, plegado.
  var indice = document.querySelector('.indice');
  if (indice && window.matchMedia('(min-width: 1100px)').matches) indice.open = true;

  // Resalta en el índice la sección que se está leyendo.
  var enlaces = document.querySelectorAll('.indice a[href^="#"]');
  if (!('IntersectionObserver' in window) || !enlaces.length) return;
  var mapa = {};
  enlaces.forEach(function (a) { mapa[a.getAttribute('href').slice(1)] = a; });
  var obs = new IntersectionObserver(function (entradas) {
    entradas.forEach(function (e) {
      if (!e.isIntersecting) return;
      enlaces.forEach(function (a) { a.classList.remove('activo'); });
      var a = mapa[e.target.id];
      if (a) a.classList.add('activo');
    });
  }, { rootMargin: '0px 0px -70% 0px' });
  Object.keys(mapa).forEach(function (id) {
    var s = document.getElementById(id);
    if (s) obs.observe(s);
  });
})();
