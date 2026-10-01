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
