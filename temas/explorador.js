/* ══════════════════════════════════════════════════════════════
   BioCelia · Explorador de la célula
   Uso: <figure class="explorador" data-celulas="animal|vegetal"><figcaption>…</figcaption></figure>
   Usa las figuras propias de la célula animal y vegetal (assets/temas/c1). Al tocar un orgánulo
   (su punto o su nombre) se resalta y aparece su ficha: estructura y función, con los datos del tema.
   La mitocondria, el cloroplasto y el núcleo se pueden «ver por dentro» con su esquema detallado.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var RUTA = '../assets/temas/c1/';
  var CELULAS = {
    animal: { nombre: 'Célula animal', svg: 'celula-animal.svg' },
    vegetal: { nombre: 'Célula vegetal', svg: 'celula-vegetal.svg' }
  };
  // Fichas: estructura y función, resumidas del tema C1 (no añaden nada que no esté en él).
  var FICHAS = {
    'núcleo': { e: 'Doble membrana (envoltura nuclear) con poros; dentro, el nucleoplasma, la cromatina y el nucléolo.', f: 'Contiene la información genética (ADN) y dirige la actividad celular.', dentro: 'nucleo-interfasico.svg' },
    'nucléolo': { e: 'Zona sin membrana con ADN, ARN y proteínas.', f: 'Síntesis del ARN ribosómico y montaje de las subunidades de los ribosomas.' },
    'envoltura nuclear': { e: 'Doble membrana continua con el RER, con poros nucleares.', f: 'Separa el núcleo del citoplasma; los poros regulan el paso de moléculas (ARNm, subunidades ribosómicas, proteínas).' },
    'RER': { e: 'Cisternas (sacos aplanados) con ribosomas en la cara citosólica, continuas con la envoltura nuclear.', f: 'Síntesis de proteínas de membrana, de secreción y de los lisosomas; glucosilación inicial y plegamiento.' },
    'REL': { e: 'Túbulos sin ribosomas, continuos con el RER.', f: 'Síntesis de lípidos (fosfolípidos, colesterol, hormonas esteroideas), detoxificación (fármacos, alcohol) y almacén de Ca²⁺.' },
    'complejo de Golgi': { e: 'Dictiosomas: pilas de cisternas aplanadas con una cara cis, que recibe las vesículas del RER, y una cara trans, de la que salen las de secreción.', f: 'Maduración y glucosilación de proteínas y lípidos, clasificación y embalaje de los productos de secreción y formación de lisosomas. En vegetales, síntesis de polisacáridos de la pared.' },
    'mitocondria': { e: 'Doble membrana: la externa, muy permeable, y la interna, plegada en crestas. En la matriz, ADN circular, ribosomas y enzimas.', f: 'Respiración celular: obtención de ATP. Ciclo de Krebs y β-oxidación en la matriz; cadena respiratoria y fosforilación oxidativa en las crestas. Está en células animales y vegetales.', dentro: 'mitocondria.svg' },
    'lisosoma': { e: 'Vesícula con enzimas hidrolíticas (hidrolasas ácidas) que actúan a pH ácido (≈ 5). Procede del complejo de Golgi.', f: 'Digestión intracelular: de material del exterior (heterofagia) o de componentes de la propia célula (autofagia).' },
    'peroxisoma': { e: 'Vesícula de membrana simple con oxidasas y catalasa.', f: 'Las oxidasas oxidan sustancias (ácidos grasos de cadena muy larga, tóxicos) produciendo H₂O₂, que la catalasa descompone en agua y O₂. Detoxificación.' },
    'centrosoma': { e: 'Dos centriolos perpendiculares, cada uno con 9 tripletes de microtúbulos, rodeados de material pericentriolar.', f: 'Centro organizador de microtúbulos: forma el huso en la división celular. Solo en células animales.' },
    'ribosomas': { e: 'Sin membrana: ARN ribosómico y proteínas en dos subunidades (80S en el citosol eucariota).', f: 'Síntesis de proteínas (traducción). Libres en el citosol o adosados al RER.' },
    'vesícula': { e: 'Pequeño saco rodeado de membrana.', f: 'Transporta sustancias entre los orgánulos del sistema de endomembranas y hacia el exterior (exocitosis).' },
    'membrana plasmática': { e: 'Bicapa de fosfolípidos con colesterol (en animales), proteínas y, en la cara externa, glúcidos: modelo del mosaico fluido.', f: 'Barrera con permeabilidad selectiva, reconocimiento celular y comunicación (receptores de señales).' },
    'citosol': { e: 'Medio acuoso del citoplasma (≈ 85 % de agua) con proteínas, sales, ARN…', f: 'Lugar de muchas reacciones: glucólisis, síntesis de proteínas en ribosomas libres, fermentaciones y síntesis de ácidos grasos.' },
    'vacuola (tonoplasto)': { e: 'Vesícula grande rodeada por una membrana, el tonoplasto. En vegetales hay una o pocas, muy grandes.', f: 'Mantiene la turgencia; almacena agua, sales, pigmentos, reservas y desechos; también tiene enzimas digestivas.' },
    'cloroplasto': { e: 'Doble membrana; estroma con ADN circular, ribosomas 70S y gránulos de almidón; tilacoides con los pigmentos, apilados en grana.', f: 'Fotosíntesis: fase luminosa en los tilacoides y ciclo de Calvin en el estroma. Exclusivo de vegetales y algas.', dentro: 'cloroplasto.svg' },
    'pared celular': { e: 'Cubierta rígida por fuera de la membrana, sobre todo de celulosa, con hemicelulosa y pectinas.', f: 'Protección, forma y rigidez, resistencia a la presión osmótica (impide que la célula estalle) y unión entre células.' },
    'plasmodesmo': { e: 'Conducto que atraviesa la pared celular.', f: 'Comunica el citoplasma de células vecinas.' }
  };

  function el(tag, attrs, padre) {
    var e = document.createElementNS(NS, tag);
    for (var k in attrs) e.setAttribute(k, attrs[k]);
    if (padre) padre.appendChild(e);
    return e;
  }

  function montar(fig) {
    var tipos = (fig.dataset.celulas || 'animal|vegetal').split('|');
    var pest = document.createElement('div'); pest.className = 'exp-pestanas'; pest.setAttribute('role', 'tablist');
    var cuerpo = document.createElement('div'); cuerpo.className = 'exp-cuerpo';
    var lienzo = document.createElement('div'); lienzo.className = 'exp-lienzo';
    var ficha = document.createElement('div'); ficha.className = 'exp-ficha'; ficha.setAttribute('aria-live', 'polite');
    var lista = document.createElement('div'); lista.className = 'exp-lista'; lista.setAttribute('aria-label', 'Orgánulos');
    var barra = document.createElement('div'); barra.className = 'exp-barra';
    var bNombres = document.createElement('button'); bNombres.type = 'button'; bNombres.className = 'exp-btn'; bNombres.textContent = 'Ocultar nombres (repaso)';
    barra.appendChild(bNombres);
    var izq = document.createElement('div'); izq.appendChild(lienzo); izq.appendChild(lista);
    cuerpo.appendChild(izq); cuerpo.appendChild(ficha);
    var cap = fig.querySelector('figcaption');
    [pest, cuerpo, barra].forEach(function (x) { fig.insertBefore(x, cap); });
    var ocultos = false, actual = null, cache = {};

    function fichaInicial() {
      ficha.innerHTML = '<p class="exp-pista">Toca un orgánulo (su punto o su nombre) para ver cómo es y para qué sirve.</p>';
    }
    function cargar(nombre) {
      if (cache[nombre]) return Promise.resolve(cache[nombre]);
      return fetch(RUTA + nombre).then(function (r) { if (!r.ok) throw new Error(nombre); return r.text(); }).then(function (t) { cache[nombre] = t; return t; });
    }

    function verCelula(tipo) {
      Array.prototype.forEach.call(pest.children, function (b) { b.setAttribute('aria-selected', b.dataset.tipo === tipo); });
      cargar(CELULAS[tipo].svg).then(function (txt) {
        lienzo.innerHTML = txt.replace(/<\?xml[^>]*>/, '');
        var svg = lienzo.querySelector('svg'); svg.removeAttribute('width'); svg.removeAttribute('height');
        svg.classList.toggle('sin-nombres', ocultos);
        lista.innerHTML = ''; lista.hidden = false;
        Array.prototype.forEach.call(svg.querySelectorAll('text'), function (t) {
          var c = t.previousElementSibling, l = c && c.previousElementSibling;
          if (!(c && l && c.tagName === 'circle' && l.tagName === 'line')) return;
          var nombre = t.textContent.trim(), datos = FICHAS[nombre]; if (!datos) return;
          var g = el('g', { class: 'exp-punto', tabindex: '0', role: 'button', 'aria-label': nombre });
          t.parentNode.insertBefore(g, l);
          [l, c, t].forEach(function (x) { g.appendChild(x); });
          var halo = el('circle', { cx: c.getAttribute('cx'), cy: c.getAttribute('cy'), r: 13, class: 'exp-halo' });
          g.insertBefore(halo, g.firstChild);
          function elegir() {
            Array.prototype.forEach.call(svg.querySelectorAll('.exp-punto.activo'), function (x) { x.classList.remove('activo'); });
            g.classList.add('activo'); mostrar(nombre, datos);
          }
          g.addEventListener('click', elegir);
          // botón con el nombre: más fácil de tocar en el móvil que el punto del dibujo
          var bl = document.createElement('button'); bl.type = 'button'; bl.className = 'exp-chip'; bl.textContent = nombre;
          bl.addEventListener('click', function () { elegir(); Array.prototype.forEach.call(lista.children, function (x) { x.classList.toggle('activo', x === bl); }); });
          g.addEventListener('click', function () { Array.prototype.forEach.call(lista.children, function (x) { x.classList.toggle('activo', x === bl); }); });
          lista.appendChild(bl);
          g.addEventListener('keydown', function (e) { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); elegir(); } });
        });
        actual = tipo; fichaInicial();
      }).catch(function () { lienzo.innerHTML = '<p class="exp-error">No se ha podido cargar el esquema.</p>'; });
    }

    function mostrar(nombre, d) {
      var dondeVeg = nombre === 'cloroplasto' || nombre === 'pared celular' || nombre === 'plasmodesmo' || nombre === 'vacuola (tonoplasto)';
      ficha.innerHTML = '<h4>' + nombre.charAt(0).toUpperCase() + nombre.slice(1) + '</h4>' +
        '<p><b>Cómo es.</b> ' + d.e + '</p><p><b>Para qué sirve.</b> ' + d.f + '</p>' +
        (d.dentro ? '<button type="button" class="exp-btn exp-dentro">🔍 Ver por dentro</button>' : '');
      var b = ficha.querySelector('.exp-dentro');
      if (b) b.addEventListener('click', function () { verDentro(nombre, d.dentro); });
    }

    function verDentro(nombre, archivo) {
      cargar(archivo).then(function (txt) {
        lista.hidden = true;
        lienzo.innerHTML = '<div class="exp-zoom-cab"><button type="button" class="exp-btn exp-volver">← Volver a la célula</button><b>' +
          nombre.charAt(0).toUpperCase() + nombre.slice(1) + ' por dentro</b></div>' + txt.replace(/<\?xml[^>]*>/, '');
        var svg = lienzo.querySelector('svg'); svg.removeAttribute('width'); svg.removeAttribute('height');
        lienzo.querySelector('.exp-volver').addEventListener('click', function () { verCelula(actual); });
        lienzo.querySelector('.exp-volver').focus();
      });
    }

    tipos.forEach(function (tipo, i) {
      var b = document.createElement('button'); b.type = 'button'; b.className = 'exp-pestana'; b.setAttribute('role', 'tab');
      b.dataset.tipo = tipo; b.textContent = CELULAS[tipo].nombre;
      b.addEventListener('click', function () { verCelula(tipo); });
      pest.appendChild(b);
    });
    bNombres.addEventListener('click', function () {
      ocultos = !ocultos;
      bNombres.textContent = ocultos ? 'Mostrar nombres' : 'Ocultar nombres (repaso)';
      var svg = lienzo.querySelector('svg'); if (svg) svg.classList.toggle('sin-nombres', ocultos);
      fig.classList.toggle('sin-nombres', ocultos);
    });
    verCelula(tipos[0]);
  }

  function iniciar() { Array.prototype.forEach.call(document.querySelectorAll('figure.explorador'), montar); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
