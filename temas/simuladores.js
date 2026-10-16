/* ══════════════════════════════════════════════════════════════
   BioCelia · Simuladores didácticos
   <figure class="simulador" data-sim="enzima">…</figure>   actividad enzimática (T, pH, sustrato, enzima, inhibidores)
   <figure class="simulador" data-sim="osmosis">…</figure>  ósmosis en un glóbulo rojo y en una célula vegetal
   Son modelos cualitativos: reproducen el comportamiento que se estudia en la PAU, no medidas reales.
   Datos usados: células humanas a 37 °C y pH 6,5-7,5 (Lodish); pepsina pH 1,5-2 y tripsina 7,5-8
   (temario PAU, Bloque I); suero fisiológico 0,9 % NaCl, isotónico con la sangre (tema C1).
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var reducir = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;

  function crear(tag, cls, html) { var e = document.createElement(tag); if (cls) e.className = cls; if (html !== undefined) e.innerHTML = html; return e; }
  function control(etq, tipo, opc) {
    var w = crear('label', 'sim-control');
    var t = crear('span', 'sim-etq', etq); w.appendChild(t);
    var i;
    if (tipo === 'select') {
      i = crear('select');
      opc.opciones.forEach(function (o) { var op = crear('option', null, o[1]); op.value = o[0]; i.appendChild(op); });
    } else {
      i = crear('input'); i.type = 'range'; i.min = opc.min; i.max = opc.max; i.step = opc.paso; i.value = opc.valor;
    }
    var v = crear('output', 'sim-valor'); w.appendChild(i); if (tipo !== 'select') w.appendChild(v);
    return { el: w, input: i, out: v };
  }

  /* ─── gráfica de línea sencilla en SVG ─── */
  function grafica(tit, ejeX, ejeY, xmin, xmax) {
    var W = 320, H = 200, m = { l: 40, r: 12, t: 26, b: 36 };
    function X(x) { return m.l + (x - xmin) / (xmax - xmin) * (W - m.l - m.r); }
    function Y(y) { return H - m.b - y * (H - m.t - m.b); }
    var div = crear('div', 'sim-graf');
    function pintar(curvas, punto, marcas) {
      var s = '<svg viewBox="0 0 ' + W + ' ' + H + '" role="img" aria-label="' + tit + '">';
      s += '<text x="' + (W / 2) + '" y="16" text-anchor="middle" class="g-tit">' + tit + '</text>';
      s += '<line x1="' + m.l + '" y1="' + (H - m.b) + '" x2="' + (W - m.r) + '" y2="' + (H - m.b) + '" class="g-eje"/><line x1="' + m.l + '" y1="' + m.t + '" x2="' + m.l + '" y2="' + (H - m.b) + '" class="g-eje"/>';
      s += '<text x="' + (W / 2) + '" y="' + (H - 6) + '" text-anchor="middle" class="g-etq">' + ejeX + '</text>';
      s += '<text x="12" y="' + (H / 2) + '" text-anchor="middle" class="g-etq" transform="rotate(-90 12 ' + (H / 2) + ')">' + ejeY + '</text>';
      (marcas || []).forEach(function (mk) { s += '<text x="' + X(mk) + '" y="' + (H - m.b + 14) + '" text-anchor="middle" class="g-num">' + String(mk).replace('.', ',') + '</text>'; });
      curvas.forEach(function (c) {
        s += '<polyline fill="none" class="' + c.cls + '" points="' + c.p.map(function (q) { return X(q[0]).toFixed(1) + ',' + Y(Math.max(0, Math.min(1.05, q[1]))).toFixed(1); }).join(' ') + '"/>';
      });
      if (punto) s += '<circle cx="' + X(punto[0]) + '" cy="' + Y(Math.min(1.05, punto[1])) + '" r="6" class="g-punto"/>';
      div.innerHTML = s + '</svg>';
    }
    return { el: div, pintar: pintar };
  }

  /* ═════════ SIMULADOR DE ENZIMAS ═════════ */
  var ENZIMAS = {
    celular: { nombre: 'Enzima de una célula humana', pH: 7.0, anchoPH: 1.6, nota: 'óptimos de una célula humana: unos 37 °C y pH 6,5-7,5' },
    pepsina: { nombre: 'Pepsina (estómago)', pH: 1.75, anchoPH: 1.3, nota: 'pepsina: pH óptimo 1,5-2, el del estómago' },
    tripsina: { nombre: 'Tripsina (duodeno)', pH: 7.75, anchoPH: 1.4, nota: 'tripsina: pH óptimo 7,5-8, el del intestino' }
  };
  var TOPT = 37, KM = 10;
  function fT(T) {                 // sube al calentar hasta el óptimo y cae al desnaturalizarse
    if (T <= TOPT) return Math.pow(2, (T - TOPT) / 10);
    return Math.exp(-Math.pow((T - TOPT) / 9, 2));
  }
  function fpH(pH, e) { return Math.exp(-Math.pow((pH - e.pH) / e.anchoPH, 2)); }

  function simEnzima(fig) {
    var cont = crear('div', 'sim-cont'), mando = crear('div', 'sim-mandos'), vis = crear('div', 'sim-vis');
    var cEnz = control('Enzima', 'select', { opciones: Object.keys(ENZIMAS).map(function (k) { return [k, ENZIMAS[k].nombre]; }) });
    var cT = control('Temperatura', 'range', { min: 0, max: 80, paso: 1, valor: 37 });
    var cpH = control('pH', 'range', { min: 0, max: 14, paso: 0.1, valor: 7 });
    var cS = control('Concentración de sustrato', 'range', { min: 0, max: 100, paso: 1, valor: 40 });
    var cE = control('Cantidad de enzima', 'range', { min: 1, max: 3, paso: 1, valor: 2 });
    var cInh = control('Inhibidor', 'select', { opciones: [['no', 'Sin inhibidor'], ['comp', 'Competitivo'], ['nocomp', 'No competitivo']] });
    var cI = control('Concentración de inhibidor', 'range', { min: 0, max: 10, paso: 1, valor: 0 });
    [cEnz, cT, cpH, cS, cE, cInh, cI].forEach(function (c) { mando.appendChild(c.el); });
    var bOpt = crear('button', 'sim-btn', 'Condiciones óptimas'); bOpt.type = 'button'; mando.appendChild(bOpt);
    var lectura = crear('div', 'sim-lectura'), expl = crear('div', 'sim-expl'); expl.setAttribute('aria-live', 'polite');
    var gS = grafica('Velocidad y sustrato', '[sustrato]', 'velocidad', 0, 100),
        gT = grafica('Velocidad y temperatura', 'temperatura (°C)', 'velocidad', 0, 80),
        gP = grafica('Velocidad y pH', 'pH', 'velocidad', 0, 14);
    var graf = crear('div', 'sim-grafs'); [gS, gT, gP].forEach(function (g) { graf.appendChild(g.el); });
    vis.appendChild(lectura); vis.appendChild(graf); vis.appendChild(expl);
    cont.appendChild(mando); cont.appendChild(vis);
    fig.insertBefore(cont, fig.querySelector('figcaption'));

    var VMAX1 = 1 / 3;               // con la cantidad máxima de enzima la velocidad llega a 1
    function velocidad(p, S) {
      var vmax = VMAX1 * p.E * fT(p.T) * fpH(p.pH, p.enz), km = KM;
      if (p.inh === 'comp') km = KM * (1 + p.I / 2);
      if (p.inh === 'nocomp') vmax = vmax / (1 + p.I / 2);
      return vmax * S / (km + S);
    }
    function leer() {
      return { enz: ENZIMAS[cEnz.input.value], T: +cT.input.value, pH: +cpH.input.value, S: +cS.input.value, E: +cE.input.value, inh: cInh.input.value, I: cInh.input.value === 'no' ? 0 : +cI.input.value };
    }
    function serie(f, a, b, n) { var r = []; for (var i = 0; i <= n; i++) { var x = a + (b - a) * i / n; r.push([x, f(x)]); } return r; }
    function actualizar() {
      var p = leer();
      cI.el.classList.toggle('sim-off', p.inh === 'no'); cI.input.disabled = p.inh === 'no';
      cT.out.textContent = p.T + ' °C'; cpH.out.textContent = p.pH.toFixed(1).replace('.', ','); cS.out.textContent = p.S;
      cE.out.textContent = ['', 'poca', 'media', 'mucha'][p.E]; cI.out.textContent = p.I;
      var ref = { enz: p.enz, T: TOPT, pH: p.enz.pH, E: p.E, inh: 'no', I: 0 };
      var v = velocidad(p, p.S), vref = velocidad(ref, 100);
      gS.pintar([{ cls: 'g-ref', p: serie(function (S) { return velocidad(ref, S); }, 0, 100, 60) }, { cls: 'g-act', p: serie(function (S) { return velocidad(p, S); }, 0, 100, 60) }], [p.S, v], [0, 50, 100]);
      gT.pintar([{ cls: 'g-act', p: serie(function (T) { return velocidad({ enz: p.enz, T: T, pH: p.pH, E: p.E, inh: p.inh, I: p.I }, p.S); }, 0, 80, 80) }], [p.T, v], [0, 20, 37, 60, 80]);
      gP.pintar([{ cls: 'g-act', p: serie(function (q) { return velocidad({ enz: p.enz, T: p.T, pH: q, E: p.E, inh: p.inh, I: p.I }, p.S); }, 0, 14, 84) }], [p.pH, v], [0, 2, 4, 7, 10, 14]);
      lectura.innerHTML = '<span>Velocidad de reacción</span><b>' + Math.round(v * 100) + '</b><span class="sim-uds">(unidades arbitrarias; máximo 100)</span>';
      var t = [];
      if (p.T > 55) t.push('A ' + p.T + ' °C la enzima, que es una proteína, está <b class="clave">desnaturalizada</b>: ha perdido su estructura y su actividad.');
      else if (p.T > TOPT + 3) t.push('Por encima de la <b class="clave">temperatura óptima</b> la actividad cae porque la enzima empieza a <b>desnaturalizarse</b>.');
      else if (p.T < TOPT - 3) t.push('Por debajo del óptimo la enzima actúa más despacio (hay menos choques entre enzima y sustrato), pero <b>no se desnaturaliza</b>.');
      else t.push('Estás cerca de la <b class="clave">temperatura óptima</b>.');
      var dpH = Math.abs(p.pH - p.enz.pH);
      if (dpH > 3) t.push('El pH está muy lejos del <b class="clave">pH óptimo</b> de esta enzima: cambian las cargas de sus aminoácidos y se desnaturaliza.');
      else if (dpH > 0.8) t.push('Fuera de su <b class="clave">pH óptimo</b> la actividad baja: se dificulta la unión del sustrato al centro activo.');
      else t.push('El pH está cerca del óptimo de esta enzima (' + p.enz.nota + ').');
      if (p.S > 0 && p.S >= 60 && p.inh !== 'comp') t.push('Con mucho sustrato la curva se aplana: es la <b class="clave">saturación</b>, todos los centros activos están ocupados. Solo añadiendo más enzima aumentaría la velocidad máxima.');
      if (p.inh === 'comp' && p.I > 0) t.push('El inhibidor <b class="clave">competitivo</b> se une al centro activo y compite con el sustrato: si aumentas mucho el sustrato, su efecto se reduce.');
      if (p.inh === 'nocomp' && p.I > 0) t.push('El inhibidor <b class="clave">no competitivo</b> se une a otra zona de la enzima: baja la velocidad máxima aunque añadas mucho sustrato.');
      if (p.S === 0) t.push('Sin sustrato no hay reacción.');
      expl.innerHTML = '<p>' + t.join(' ') + '</p><p class="sim-nota">En la gráfica del sustrato, la línea discontinua es la misma enzima en condiciones óptimas y sin inhibidor.</p>';
    }
    [cEnz, cT, cpH, cS, cE, cInh, cI].forEach(function (c) { c.input.addEventListener('input', actualizar); c.input.addEventListener('change', actualizar); });
    cEnz.input.addEventListener('change', function () { cpH.input.value = ENZIMAS[cEnz.input.value].pH; actualizar(); });
    bOpt.addEventListener('click', function () { cT.input.value = TOPT; cpH.input.value = ENZIMAS[cEnz.input.value].pH; cInh.input.value = 'no'; cI.input.value = 0; actualizar(); });
    actualizar();
  }

  /* ═════════ SIMULADOR DE ÓSMOSIS ═════════ */
  function simOsmosis(fig) {
    var cont = crear('div', 'sim-cont'), mando = crear('div', 'sim-mandos'), vis = crear('div', 'sim-vis');
    var cCel = control('Célula', 'select', { opciones: [['roja', 'Glóbulo rojo (célula animal)'], ['vegetal', 'Célula vegetal']] });
    var cM = control('Concentración de solutos del medio', 'range', { min: 0, max: 3, paso: 0.05, valor: 1 });
    mando.appendChild(cCel.el); mando.appendChild(cM.el);
    var bot = crear('div', 'sim-botones');
    [['Agua destilada', 0], ['Isotónico', 1], ['Muy concentrado', 2.6]].forEach(function (b) {
      var x = crear('button', 'sim-btn', b[0]); x.type = 'button'; x.addEventListener('click', function () { cM.input.value = b[1]; actualizar(); }); bot.appendChild(x);
    });
    mando.appendChild(bot);
    var escena = crear('div', 'sim-escena'), estado = crear('div', 'sim-lectura'), expl = crear('div', 'sim-expl'); expl.setAttribute('aria-live', 'polite');
    vis.appendChild(estado); vis.appendChild(escena); vis.appendChild(expl);
    cont.appendChild(mando); cont.appendChild(vis);
    fig.insertBefore(cont, fig.querySelector('figcaption'));

    var gotas = [], raf = null, flujo = 0, visible = !('IntersectionObserver' in window);   // la animación solo corre mientras se ve
    for (var i = 0; i < 26; i++) gotas.push({ a: Math.random() * 6.283, f: Math.random(), v: 0.004 + Math.random() * 0.004 });

    function dibujo(tipo, r) {      // r = concentración del medio / concentración interior
      var s = '<svg viewBox="0 0 520 300" role="img" aria-label="Célula en el medio elegido">';
      var fondo = r < 0.97 ? '#eaf4fd' : r > 1.03 ? '#fdf3e4' : '#eef4ee';
      s += '<rect x="0" y="0" width="520" height="300" rx="14" fill="' + fondo + '"/>';
      if (tipo === 'roja') {
        var esc = r < 1 ? 1 + (1 - r) * 0.55 : 1 - Math.min(0.32, (r - 1) * 0.22);
        var estalla = r < 0.45;
        if (estalla) {
          s += '<g opacity="0.75"><path d="M190 150 q30 -70 70 -40 M330 150 q-30 70 -70 40 M200 175 q40 40 90 10" stroke="#c0392b" stroke-width="6" fill="none" stroke-linecap="round"/></g>' +
            '<circle cx="260" cy="150" r="70" fill="#f6c6c0" opacity="0.35"/>';
        } else if (r > 1.03) {
          var n = 16, pts = [], R = 70 * esc;
          for (var k = 0; k < n * 2; k++) { var a = k / (n * 2) * 6.283, rr = k % 2 ? R : R + 10 * Math.min(1, (r - 1) * 1.2); pts.push((260 + rr * Math.cos(a)).toFixed(1) + ',' + (150 + rr * Math.sin(a)).toFixed(1)); }
          s += '<polygon points="' + pts.join(' ') + '" fill="#e2726b" stroke="#a93226" stroke-width="3" stroke-linejoin="round"/>';
        } else {
          s += '<ellipse cx="260" cy="150" rx="' + (75 * esc) + '" ry="' + (60 * esc) + '" fill="#e2726b" stroke="#a93226" stroke-width="3"/>' +
            (r >= 0.97 ? '<ellipse cx="260" cy="150" rx="' + (38 * esc) + '" ry="' + (28 * esc) + '" fill="#d35f58" opacity="0.6"/>' : '');
        }
      } else {
        // pared rígida fija; protoplasto (membrana + citoplasma) y vacuola según el agua
        var enc = r <= 1 ? 1 : 1 - Math.min(0.45, (r - 1) * 0.3);
        var w = 200 * enc, h = 150 * enc;
        s += '<rect x="150" y="65" width="220" height="170" rx="16" fill="none" stroke="#2e7d32" stroke-width="10"/>';
        var gx = 260 - w / 2, gy = 150 - h / 2;
        s += '<rect x="' + gx + '" y="' + gy + '" width="' + w + '" height="' + h + '" rx="' + (14 * enc + 2) + '" fill="#c8e6c9" stroke="#1e7a4c" stroke-width="2.5"/>';
        var vw = w * (r < 0.97 ? 0.84 : 0.6 * enc + 0.06), vh = h * (r < 0.97 ? 0.82 : 0.58 * enc + 0.06);
        s += '<rect x="' + (260 - vw / 2) + '" y="' + (150 - vh / 2) + '" width="' + vw + '" height="' + vh + '" rx="12" fill="#dff1fb" stroke="#5b9bd5" stroke-width="2"/>';
        for (var c = 0; c < 4; c++) s += '<ellipse cx="' + (gx + 18 + c * (w - 36) / 3) + '" cy="' + (gy + 12) + '" rx="9" ry="5" fill="#2e7d32"/>';
        s += '<text x="260" y="58" text-anchor="middle" class="o-etq">pared celular</text><text x="260" y="155" text-anchor="middle" class="o-etq">vacuola</text>';
      }
      if (tipo === 'roja' && Math.abs(r - 1) > 0.03 && r >= 0.45)
        s += '<ellipse cx="260" cy="150" rx="75" ry="60" fill="none" stroke="#555" stroke-width="1.5" stroke-dasharray="6 5"/><text x="260" y="282" text-anchor="middle" class="o-etq o-gris">línea discontinua: tamaño en medio isotónico</text>';
      s += '<g id="o-gotas"></g></svg>';
      return s;
    }
    function animar() {
      var g = escena.querySelector('#o-gotas'); if (!g) return;
      var s = '';
      gotas.forEach(function (d) {
        if (!reducir) { d.f += d.v; if (d.f > 1) { d.f = 0; d.a = Math.random() * 6.283; } }
        var desde = flujo > 0 ? 190 : 85, hasta = flujo > 0 ? 85 : 190;
        if (flujo === 0) { desde = 120 + 40 * Math.sin(d.a * 3); hasta = 130 + 40 * Math.cos(d.a * 3); }
        var rad = desde + (hasta - desde) * d.f;
        s += '<circle cx="' + (260 + rad * Math.cos(d.a) * 1.25).toFixed(1) + '" cy="' + (150 + rad * Math.sin(d.a) * 0.75).toFixed(1) + '" r="3.2" fill="#2f62d6" opacity="0.65"/>';
      });
      g.innerHTML = s;
      raf = !reducir && visible ? requestAnimationFrame(animar) : null;
    }
    function actualizar() {
      var tipo = cCel.input.value, r = +cM.input.value;
      flujo = r < 0.97 ? 1 : r > 1.03 ? -1 : 0;      // 1: entra agua; -1: sale agua
      escena.innerHTML = dibujo(tipo, r);
      var medio = r < 0.97 ? 'hipotónico' : r > 1.03 ? 'hipertónico' : 'isotónico';
      var nacl = tipo === 'roja' ? ' · equivale a ≈ ' + (0.9 * r).toFixed(2).replace('.', ',') + ' % de NaCl' : '';
      cM.out.textContent = r === 0 ? 'agua destilada' : (r.toFixed(2).replace('.', ',') + ' × el interior');
      estado.innerHTML = '<span>Medio</span><b>' + medio + '</b><span class="sim-uds">' + (flujo > 0 ? 'el agua entra en la célula' : flujo < 0 ? 'el agua sale de la célula' : 'sin intercambio neto de agua') + nacl + '</span>';
      var t;
      if (tipo === 'roja') {
        if (r < 0.45) t = 'Medio muy <b class="clave">hipotónico</b>: entra tanta agua por ósmosis que el glóbulo rojo se hincha hasta <b class="clave">estallar</b>: es la <b class="clave">hemólisis</b>. Las células animales no tienen pared que las proteja.';
        else if (flujo > 0) t = 'Medio <b class="clave">hipotónico</b>: el agua pasa por ósmosis de la disolución más diluida (fuera) a la más concentrada (dentro) y el glóbulo rojo <b>se hincha</b>.';
        else if (flujo < 0) t = 'Medio <b class="clave">hipertónico</b>: sale agua y el glóbulo rojo se deshidrata y <b>se arruga</b> (<b class="clave">crenación</b>).';
        else t = 'Medio <b class="clave">isotónico</b> (como el suero fisiológico, 0,9 % de NaCl): no hay intercambio neto de agua y el volumen no cambia.';
      } else {
        if (flujo > 0) t = 'Medio <b class="clave">hipotónico</b>: entra agua, la vacuola se llena y la célula queda <b class="clave">turgente</b>, presionando contra la pared. La <b class="clave">pared celular</b> impide que estalle.';
        else if (flujo < 0) t = 'Medio <b class="clave">hipertónico</b>: sale agua, la vacuola se reduce y la membrana se separa de la pared: es la <b class="clave">plasmólisis</b>.';
        else t = 'Medio <b class="clave">isotónico</b>: no hay intercambio neto de agua y el volumen no cambia; la célula vegetal queda <b>flácida</b> (sin turgencia).';
      }
      expl.innerHTML = '<p>' + t + '</p><p class="sim-nota">El agua atraviesa la membrana por ósmosis (por la bicapa y por las acuaporinas) desde el medio hipotónico hacia el hipertónico.</p>';
      if (raf) cancelAnimationFrame(raf);
      animar();
    }
    cCel.input.addEventListener('change', actualizar); cM.input.addEventListener('input', actualizar);
    if ('IntersectionObserver' in window) new IntersectionObserver(function (e) {
      visible = e[0].isIntersecting;
      if (visible && !raf) animar();
    }).observe(escena);
    actualizar();
  }

  function iniciar() {
    Array.prototype.forEach.call(document.querySelectorAll('figure.simulador'), function (f) {
      if (f.dataset.sim === 'enzima') simEnzima(f);
      if (f.dataset.sim === 'osmosis') simOsmosis(f);
    });
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
