/* ══════════════════════════════════════════════════════════════
   BioCelia · Esquemas para rotular
   Uso: <figure class="rotular" data-svg="../assets/temas/c1/celula-animal.svg"><figcaption>…</figcaption></figure>
   Toma una figura propia de los apuntes, cambia cada rótulo (línea + punto + texto) por una casilla
   numerada vacía y ofrece las etiquetas desordenadas. Se pueden arrastrar o tocar la etiqueta y luego
   la casilla (también con el teclado). Al imprimir queda como ficha: dibujo con casillas y lista de términos.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';

  function el(tag, attrs, padre) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (padre) padre.appendChild(e);
    return e;
  }
  function barajar(a) {
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }

  function montar(fig) {
    var lienzo = document.createElement('div'); lienzo.className = 'rot-lienzo';
    var instr = document.createElement('p'); instr.className = 'rot-instr';
    instr.textContent = 'Arrastra cada nombre a su casilla, o tócalo y después toca la casilla. Pulsa una casilla llena para vaciarla.';
    var banco = document.createElement('div'); banco.className = 'rot-banco'; banco.setAttribute('aria-label', 'Nombres para colocar');
    var barra = document.createElement('div'); barra.className = 'rot-barra';
    var res = document.createElement('p'); res.className = 'rot-resultado'; res.setAttribute('aria-live', 'polite');
    var cap = fig.querySelector('figcaption');
    [instr, lienzo, banco, barra, res].forEach(function (x) { fig.insertBefore(x, cap); });

    fetch(fig.dataset.svg).then(function (r) { if (!r.ok) throw new Error(); return r.text(); }).then(function (txt) {
      lienzo.innerHTML = txt.replace(/<\?xml[^>]*>/, '');
      var svg = lienzo.querySelector('svg');
      svg.removeAttribute('width'); svg.removeAttribute('height');
      var titulo = svg.querySelector('title'); if (titulo) titulo.textContent = 'Esquema para rotular: ' + titulo.textContent;

      // rótulos: <text> justo detrás de un punto (circle) que va detrás de una línea
      var rotulos = Array.prototype.filter.call(svg.querySelectorAll('text'), function (t) {
        var c = t.previousElementSibling, l = c && c.previousElementSibling;
        return c && l && c.tagName === 'circle' && l.tagName === 'line';
      });
      var ancho = 0, datos = rotulos.map(function (t) {
        var bb = t.getBBox(); ancho = Math.max(ancho, bb.width);
        return { t: t, nombre: t.textContent.trim(), bb: bb, ancla: t.getAttribute('text-anchor') || 'start', x: +t.getAttribute('x'), y: +t.getAttribute('y') };
      });
      var W = Math.min(Math.max(ancho + 18, 90), 280), seleccionado = null, zonas = [];

      datos.forEach(function (d, i) {
        var g = el('g', { class: 'zona', tabindex: '0', role: 'button', 'aria-label': 'Casilla ' + (i + 1) + ', vacía' });
        d.t.parentNode.insertBefore(g, d.t);
        var vb = svg.viewBox.baseVal, ctm = d.t.getCTM(), off = ctm ? ctm.e : 0;   // x del rótulo en el lienzo
        var hueco = d.ancla === 'end' ? off + d.x + 6 - (vb.x + 2) : vb.x + vb.width - 2 - (off + d.x - 6);
        var Wi = Math.max(Math.min(W, hueco), d.bb.width + 12);
        var x0 = d.ancla === 'end' ? d.x + 6 - Wi : d.x - 6;
        el('rect', { x: x0, y: d.bb.y - 4, width: Wi, height: d.bb.height + 8, rx: 6 }, g);
        var nx = d.ancla === 'end' ? x0 + Wi + 14 : x0 - 14;
        el('circle', { cx: nx, cy: d.bb.y + d.bb.height / 2, r: 11, class: 'zona-num' }, g);
        var n = el('text', { x: nx, y: d.bb.y + d.bb.height / 2 + 5, 'text-anchor': 'middle', class: 'zona-numtxt' }, g); n.textContent = i + 1;
        var tt = el('text', { x: d.ancla === 'end' ? d.x : d.x, y: d.y, 'text-anchor': d.ancla, class: 'zona-txt' }, g);
        d.t.parentNode.removeChild(d.t);
        var z = { g: g, txt: tt, correcto: d.nombre, puesto: null, n: i + 1 };
        zonas.push(z);
        g.addEventListener('click', function () { tocarZona(z); });
        g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); tocarZona(z); } });
      });

      // banco de nombres (desordenados)
      var chips = barajar(datos.map(function (d) { return d.nombre; })).map(function (nombre) {
        var b = document.createElement('button'); b.type = 'button'; b.className = 'rot-chip'; b.textContent = nombre;
        b.addEventListener('click', function () { if (b.dataset.arrastrado) { delete b.dataset.arrastrado; return; } elegir(b); });
        arrastre(b);
        banco.appendChild(b);
        return b;
      });

      function elegir(b) {
        if (b.disabled) return;
        if (seleccionado) seleccionado.classList.remove('sel');
        seleccionado = seleccionado === b ? null : b;
        if (seleccionado) seleccionado.classList.add('sel');
      }
      function poner(z, b) {
        if (z.puesto) quitar(z);
        z.puesto = b; z.txt.textContent = b.textContent; b.disabled = true; b.classList.remove('sel');
        z.g.classList.add('llena'); z.g.classList.remove('ok', 'ko', 'sol');
        z.g.setAttribute('aria-label', 'Casilla ' + z.n + ': ' + b.textContent);
        seleccionado = null; res.textContent = '';
      }
      function quitar(z) {
        if (!z.puesto) return;
        z.puesto.disabled = false; z.puesto = null; z.txt.textContent = '';
        z.g.classList.remove('llena', 'ok', 'ko', 'sol'); z.g.setAttribute('aria-label', 'Casilla ' + z.n + ', vacía');
      }
      function tocarZona(z) {
        if (seleccionado) poner(z, seleccionado);
        else if (z.puesto) quitar(z);
      }
      // arrastrar con ratón o dedo
      function arrastre(b) {
        var fantasma = null, mov = false;
        b.addEventListener('pointerdown', function (e) {
          if (b.disabled) return;
          mov = false;
          var x0 = e.clientX, y0 = e.clientY;
          function mover(ev) {
            if (!mov && Math.abs(ev.clientX - x0) + Math.abs(ev.clientY - y0) < 6) return;
            if (!mov) { mov = true; fantasma = b.cloneNode(true); fantasma.className = 'rot-chip rot-fantasma'; document.body.appendChild(fantasma); }
            fantasma.style.left = ev.clientX + 'px'; fantasma.style.top = ev.clientY + 'px';
            ev.preventDefault();
          }
          function soltar(ev) {
            document.removeEventListener('pointermove', mover); document.removeEventListener('pointerup', soltar);
            if (!mov) return;
            fantasma.remove(); b.dataset.arrastrado = '1';
            var dest = document.elementFromPoint(ev.clientX, ev.clientY), g = dest && dest.closest && dest.closest('.zona');
            var z = zonas.filter(function (zz) { return zz.g === g; })[0];
            if (z) poner(z, b);
          }
          document.addEventListener('pointermove', mover); document.addEventListener('pointerup', soltar);
        });
      }

      function boton(t, f) { var b = document.createElement('button'); b.type = 'button'; b.className = 'rot-btn'; b.textContent = t; b.addEventListener('click', f); barra.appendChild(b); }
      boton('Comprobar', function () {
        var bien = 0;
        zonas.forEach(function (z) {
          z.g.classList.remove('ok', 'ko', 'sol');
          if (!z.puesto) return;
          var ok = z.puesto.textContent === z.correcto; if (ok) bien++;
          z.g.classList.add(ok ? 'ok' : 'ko');
        });
        var vacias = zonas.filter(function (z) { return !z.puesto; }).length;
        res.textContent = bien + ' de ' + zonas.length + ' correctas' + (vacias ? ' · faltan ' + vacias + ' por colocar' : '') + (bien === zonas.length ? '. ¡Perfecto!' : '.');
      });
      boton('Ver solución', function () {
        zonas.forEach(function (z) { if (z.puesto) quitar(z); });
        zonas.forEach(function (z) {
          var b = chips.filter(function (c) { return c.textContent === z.correcto && !c.disabled; })[0];
          if (b) { poner(z, b); z.g.classList.add('sol'); }
        });
        res.textContent = 'Solución completa. Pulsa «Empezar de nuevo» para intentarlo sin mirar.';
      });
      boton('Empezar de nuevo', function () {
        zonas.forEach(quitar); res.textContent = '';
        barajar(chips).forEach(function (c) { banco.appendChild(c); });
      });
    }).catch(function () {
      lienzo.innerHTML = '<p class="rot-error">No se ha podido cargar el esquema.</p>';
    });
  }

  function iniciar() { Array.prototype.forEach.call(document.querySelectorAll('figure.rotular'), montar); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
