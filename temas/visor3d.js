/* ══════════════════════════════════════════════════════════════
   BioCelia · Visor 3D de moléculas para los apuntes
   Uso:
     <figure class="visor3d" data-mols="d-gliceraldehido|l-gliceraldehido"
             data-nombres="D-gliceraldehído|L-gliceraldehído"
             data-modo="espejo" data-marcar="quiral"> … <figcaption>…</figcaption></figure>
   · data-mols: ficheros .sdf de assets/moleculas (sin extensión), separados por |
   · data-modo: "espejo" (dos enantiómeros a cada lado de un espejo) o "pareja"
   · data-marcar: "quiral" (carbono asimétrico) o "anomerico" (C1 y su –OH)
   Coordenadas de PubChem / PDB, preparadas con tools/moleculas_3d.py.
   La librería 3Dmol.js (licencia BSD) se carga solo cuando el visor aparece en pantalla.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var LIB = 'https://cdnjs.cloudflare.com/ajax/libs/3Dmol/2.4.2/3Dmol-min.js';
  var RUTA = '../assets/moleculas/';
  var SEP0 = 3.2;           // separación (Å) por defecto de cada molécula respecto al centro
  var carga = null;

  function cargarLib() {
    if (window.$3Dmol) return Promise.resolve();
    if (carga) return carga;
    carga = new Promise(function (ok, ko) {
      var s = document.createElement('script');
      s.src = LIB; s.onload = ok; s.onerror = ko;
      document.head.appendChild(s);
    });
    return carga;
  }

  // Desplaza en x todas las coordenadas de un SDF (formato V2000).
  function desplazar(sdf, dx) {
    var l = sdf.split(/\r?\n/), na = parseInt(l[3].slice(0, 3), 10);
    for (var i = 4; i < 4 + na; i++) {
      var x = parseFloat(l[i].slice(0, 10)) + dx;
      l[i] = ('          ' + x.toFixed(4)).slice(-10) + l[i].slice(10);
    }
    return l.join('\n');
  }

  function boton(txt, titulo) {
    var b = document.createElement('button');
    b.type = 'button'; b.className = 'visor3d-btn'; b.textContent = txt;
    if (titulo) b.title = titulo;
    return b;
  }

  function montar(fig) {
    var mols = fig.dataset.mols.split('|');
    var nombres = (fig.dataset.nombres || '').split('|');
    var modo = fig.dataset.modo || 'pareja';
    var marcar = fig.dataset.marcar || '';
    var SEP = parseFloat(fig.dataset.sep) || SEP0;

    var lienzo = document.createElement('div');
    lienzo.className = 'visor3d-lienzo';
    lienzo.setAttribute('aria-hidden', 'true');
    var barra = document.createElement('div');
    barra.className = 'visor3d-barra';
    var bGirar = boton('⟳ Girar', 'Activa o detiene el giro automático');
    var bEstilo = boton('Esferas', 'Cambia entre bolas y varillas y modelo de esferas');
    var bSuper = modo === 'espejo' ? boton('Intentar superponer', 'Lleva una molécula sobre la otra') : null;
    var bCentro = boton('Centrar');
    [bGirar, bEstilo, bSuper, bCentro].forEach(function (b) { if (b) barra.appendChild(b); });
    var ayuda = document.createElement('p');
    ayuda.className = 'visor3d-ayuda';
    ayuda.textContent = 'Arrastra para girar · rueda o pellizco para acercar';
    var cap = fig.querySelector('figcaption');
    fig.insertBefore(lienzo, cap); fig.insertBefore(barra, cap); fig.insertBefore(ayuda, cap);

    Promise.all([cargarLib()].concat(mols.map(function (m) {
      return fetch(RUTA + m + '.sdf').then(function (r) { if (!r.ok) throw new Error(m); return r.text(); });
    }))).then(function (res) {
      var datos = res.slice(1);
      var v = $3Dmol.createViewer(lienzo, { backgroundColor: '#f7fafc', antialias: true });
      var esferas = false, superpuesto = false, girando = false;

      function estilo(m) {
        m.setStyle({}, esferas ? { sphere: { scale: 0.85 } } : { stick: { radius: 0.14 }, sphere: { scale: 0.26 } });
      }

      function marcas(m, dx) {
        var at = m.selectedAtoms({});
        at.forEach(function (a) {
          var vec = a.bonds.map(function (i) { return at[i]; });
          var pes = vec.filter(function (b) { return b.elem !== 'H'; });
          var oxi = vec.filter(function (b) { return b.elem === 'O'; });
          if (a.elem !== 'C') return;
          if (marcar === 'quiral' && pes.length === 3 && vec.length === 4) {
            v.addLabel('C*', { position: { x: a.x, y: a.y, z: a.z + 0.6 }, fontSize: 13, fontColor: '#ffffff',
              backgroundColor: '#c77d00', backgroundOpacity: 0.95, inFront: true, alignment: 'center' });
          }
          if (marcar === 'anomerico' && oxi.length === 2) {
            v.addLabel('C1', { position: { x: a.x, y: a.y, z: a.z + 0.6 }, fontSize: 13, fontColor: '#ffffff',
              backgroundColor: '#c77d00', backgroundOpacity: 0.95, inFront: true, alignment: 'center' });
            oxi.forEach(function (o) {
              var anillo = o.bonds.filter(function (i) { return at[i].elem === 'C'; }).length === 2;
              if (!anillo) v.addStyle({ model: m, index: o.index }, { sphere: { scale: esferas ? 0.9 : 0.42, color: '#d63384' } });
            });
          }
        });
      }

      function dibujar(rehacerVista) {
        v.removeAllModels(); v.removeAllLabels(); v.removeAllShapes();
        datos.forEach(function (sdf, i) {
          var dx = (i === 0 ? -SEP : SEP);
          if (superpuesto && i === 1) dx = -SEP;               // el reflejo se lleva sobre el original
          var m = v.addModel(desplazar(sdf, dx), 'sdf');
          estilo(m); marcas(m, dx);
          var c = m.selectedAtoms({}).reduce(function (s, a) { s.y = Math.min(s.y, a.y); return s; }, { y: 99 });
          if (nombres[i] && !(superpuesto && i === 1)) {
            v.addLabel(nombres[i], { position: { x: dx, y: c.y - 1.6, z: 0 }, fontSize: 14, fontColor: '#0f4c81',
              backgroundColor: '#ffffff', backgroundOpacity: 0.9, borderColor: '#0f4c81', borderThickness: 1, alignment: 'center' });
          }
        });
        if (modo === 'espejo' && !superpuesto) {
          v.addBox({ center: { x: 0, y: 0, z: 0 }, dimensions: { w: 0.04, h: 6.5, d: 5.5 }, color: '#7fb3e6', opacity: 0.32 });
          v.addLabel('espejo', { position: { x: 0, y: 3.6, z: 0 }, fontSize: 12, fontColor: '#5c6b78', showBackground: false, alignment: 'center' });
        }
        if (rehacerVista) v.zoomTo();
        v.render();
      }

      dibujar(true);
      if (modo === 'espejo') v.rotate(-28, 'y');            // el espejo se ve como plano, no de canto
      v.zoom(modo === 'espejo' ? 0.92 : 1.25); v.render();
      fig.classList.add('visor3d-listo');

      bGirar.addEventListener('click', function () {
        girando = !girando; v.spin(girando ? 'y' : false, 0.6);
        bGirar.setAttribute('aria-pressed', girando);
      });
      bEstilo.addEventListener('click', function () {
        esferas = !esferas; bEstilo.textContent = esferas ? 'Bolas y varillas' : 'Esferas'; dibujar(false);
      });
      if (bSuper) bSuper.addEventListener('click', function () {
        superpuesto = !superpuesto;
        bSuper.textContent = superpuesto ? 'Separar' : 'Intentar superponer';
        dibujar(false);
      });
      bCentro.addEventListener('click', function () { v.zoomTo(); v.zoom(0.92); v.render(); });
      window.addEventListener('resize', function () { v.resize(); v.render(); });
    }).catch(function (e) {
      if (window.console) console.error("visor3d", e);
      lienzo.innerHTML = '<p class="visor3d-error">No se ha podido cargar el modelo 3D. Comprueba la conexión a internet.</p>'; lienzo.title = String(e && e.message || e);
    });
  }

  function iniciar() {
    var figs = document.querySelectorAll('figure.visor3d');
    if (!figs.length) return;
    if (!('IntersectionObserver' in window)) { figs.forEach(montar); return; }
    var io = new IntersectionObserver(function (ents) {
      ents.forEach(function (e) { if (e.isIntersecting) { io.unobserve(e.target); montar(e.target); } });
    }, { rootMargin: '300px' });
    figs.forEach(function (f) { io.observe(f); });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
