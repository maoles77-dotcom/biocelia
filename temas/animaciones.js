/* ══════════════════════════════════════════════════════════════
   BioCelia · Animaciones paso a paso (replicación, transcripción, traducción)
   Uso: <figure class="animacion" data-anim="replicacion"><figcaption>…</figcaption></figure>
   Cada animación es una lista de pasos con su dibujo (SVG propio) y su explicación.
   Botones: anterior, siguiente, reproducir y reiniciar; también con las flechas del teclado
   cuando la animación tiene el foco. Al imprimir se muestran los pasos como lista.
   ══════════════════════════════════════════════════════════════ */
(function () {
  'use strict';
  var NS = 'http://www.w3.org/2000/svg';
  var C = { viejo: '#2f62d6', nuevo: '#1e7a4c', arn: '#d63384', gris: '#9aa7b3', tinta: '#1f2d3a', suave: '#5c6b78' };

  // ── utilidades de dibujo (devuelven cadenas SVG) ──
  function linea(x1, y1, x2, y2, color, ancho, extra) {
    return '<line x1="' + x1 + '" y1="' + y1 + '" x2="' + x2 + '" y2="' + y2 + '" stroke="' + color + '" stroke-width="' + (ancho || 6) + '" stroke-linecap="round"' + (extra || '') + '/>';
  }
  function texto(x, y, t, opc) {
    opc = opc || {};
    return '<text x="' + x + '" y="' + y + '" font-size="' + (opc.tam || 16) + '" font-weight="' + (opc.peso || 700) + '" fill="' + (opc.color || C.tinta) +
      '" text-anchor="' + (opc.ancla || 'middle') + '"' + (opc.mono ? ' font-family="ui-monospace, Consolas, monospace"' : '') + '>' + t + '</text>';
  }
  function enzima(x, y, w, h, color, nombre, nuevo) {
    return '<g class="' + (nuevo ? 'aparece' : '') + '"><rect x="' + (x - w / 2) + '" y="' + (y - h / 2) + '" width="' + w + '" height="' + h + '" rx="' + Math.min(18, h / 2) +
      '" fill="' + color + '" fill-opacity="0.9" stroke="#ffffff" stroke-width="2"/>' + texto(x, y + 5, nombre, { tam: 14, color: '#ffffff' }) + '</g>';
  }
  function peldanos(x1, x2, y1, y2) {
    var s = '';
    for (var x = x1 + 9; x < x2; x += 18) s += linea(x, y1 + 4, x, y2 - 4, '#c8d2dc', 3);
    return s;
  }
  function svg(cuerpo) { return '<svg viewBox="0 0 1000 420" xmlns="' + NS + '" role="img">' + cuerpo + '</svg>'; }

  /* ═════════ REPLICACIÓN (una horquilla, procariotas) ═════════
     Hebra molde de arriba: 3′ (izquierda) → 5′ (derecha). Hebra molde de abajo: 5′ → 3′.
     La horquilla avanza hacia la derecha: la hebra nueva de arriba (adelantada) crece hacia la derecha
     de forma continua; la de abajo (retrasada) se hace en fragmentos que crecen hacia la izquierda. */
  function dibujoReplicacion(e) {
    var s = '', fx = e.fx, yA = 120, yB = 300, dA = 195, dB = 225;
    // dúplex parental por delante de la horquilla
    s += peldanos(fx, 960, dA, dB);
    s += linea(fx, dA, 960, dA, C.viejo) + linea(fx, dB, 960, dB, C.viejo);
    if (fx < 940) {
      // hebras separadas (molde) detrás de la horquilla
      s += linea(40, yA, fx - 50, yA, C.viejo) + linea(fx - 50, yA, fx, dA, C.viejo);
      s += linea(40, yB, fx - 50, yB, C.viejo) + linea(fx - 50, yB, fx, dB, C.viejo);
      s += texto(28, yA + 6, '3′', { color: C.viejo }) + texto(28, yB + 6, '5′', { color: C.viejo });
    } else {
      s += linea(40, dA, fx, dA, C.viejo) + linea(40, dB, fx, dB, C.viejo) + peldanos(40, fx, dA, dB);
      s += texto(28, dA + 6, '3′', { color: C.viejo }) + texto(28, dB + 6, '5′', { color: C.viejo });
    }
    s += texto(978, dA + 6, '5′', { color: C.viejo }) + texto(978, dB + 6, '3′', { color: C.viejo });
    if (e.origen) s += '<g class="aparece">' + linea(500, 160, 500, 260, '#c77d00', 3, ' stroke-dasharray="6 5"') + texto(500, 150, 'origen de replicación', { color: '#c77d00' }) + '</g>';
    // hebra adelantada (nueva) pegada a la molde de arriba
    var yN = yA + 22, yR = yB - 22;
    if (e.cebA) s += linea(e.cebA[0], yN, e.cebA[1], yN, C.arn, 7);
    if (e.adel) s += linea(e.adel[0], yN, e.adel[1], yN, C.nuevo, 7) + peldanos(e.adel[0], e.adel[1], yA, yN);
    // hebra retrasada: fragmentos de Okazaki [inicioADN, finADN(5′), cebador inicio, cebador fin]
    (e.frag || []).forEach(function (f) {
      s += linea(f.adn[0], yR, f.adn[1], yR, C.nuevo, 7) + peldanos(f.adn[0], f.adn[1], yR, yB);
      if (f.ceb) s += linea(f.ceb[0], yR, f.ceb[1], yR, C.arn, 7);
    });
    // proteínas SSB en las hebras sencillas
    (e.ssb || []).forEach(function (p) { s += '<circle class="aparece" cx="' + p[0] + '" cy="' + p[1] + '" r="9" fill="#e5a00d" stroke="#fff" stroke-width="2"/>'; });
    // enzimas
    (e.enz || []).forEach(function (z) { s += enzima(z[1], z[2], z[3] || 120, 34, z[4], z[0], z[5]); });
    // leyenda
    s += '<g font-size="14">' + linea(40, 405, 70, 405, C.viejo, 6) + texto(78, 410, 'hebra molde (antigua)', { ancla: 'start', tam: 14 }) +
      linea(270, 405, 300, 405, C.nuevo, 6) + texto(308, 410, 'hebra nueva (ADN)', { ancla: 'start', tam: 14 }) +
      linea(470, 405, 500, 405, C.arn, 6) + texto(508, 410, 'cebador (ARN)', { ancla: 'start', tam: 14 }) +
      '<circle cx="660" cy="405" r="8" fill="#e5a00d"/>' + texto(674, 410, 'proteínas SSB', { ancla: 'start', tam: 14 }) + '</g>';
    if (e.nota) s += texto(500, 382, e.nota, { color: C.suave, tam: 15, peso: 600 });
    return svg(s);
  }
  var HEL = '#c77d00', TOPO = '#6d3fc0', PRI = '#d63384', POL3 = '#1e7a4c', POL1 = '#0e7490', LIG = '#b03a2e';
  var REPLICACION = [
    { t: 'El punto de partida', x: 'La replicación empieza en el <b class="clave">origen de replicación</b> (uno solo en el cromosoma circular de las bacterias). Desde él avanzan <b class="clave">dos horquillas</b> en sentidos opuestos: la replicación es <b>bidireccional</b>. Aquí seguimos una de ellas. Las dos hebras son <b class="clave">antiparalelas</b> (fíjate en los extremos 3′ y 5′).',
      e: { fx: 960, origen: true } },
    { t: 'Helicasa y topoisomerasa', x: 'La <b class="clave">helicasa</b> rompe los puentes de hidrógeno y <b class="clave">separa las dos hebras</b>: se forma la horquilla. Por delante, la <b class="clave">topoisomerasa</b> elimina el <b>superenrollamiento</b> que produce la apertura (corta y vuelve a unir el ADN).',
      e: { fx: 430, enz: [['Helicasa', 425, 210, 100, HEL, true], ['Topoisomerasa', 600, 165, 130, TOPO, true]] } },
    { t: 'Proteínas SSB', x: 'Las <b class="clave">proteínas SSB</b> se unen a las hebras sencillas e <b class="clave">impiden que vuelvan a unirse</b> mientras esperan a ser copiadas.',
      e: { fx: 430, ssb: [[150, 120], [250, 120], [350, 120], [150, 300], [250, 300], [350, 300]], enz: [['Helicasa', 425, 210, 100, HEL], ['Topoisomerasa', 600, 165, 130, TOPO]] } },
    { t: 'La primasa pone el cebador', x: 'La ADN polimerasa no puede empezar una cadena desde cero: necesita un extremo 3′ libre. La <b class="clave">primasa</b> (una ARN polimerasa) sintetiza un <b class="clave">cebador de ARN</b> corto, complementario a la hebra molde.',
      e: { fx: 430, cebA: [60, 110], ssb: [[250, 120], [350, 120], [150, 300], [250, 300], [350, 300]], enz: [['Primasa', 90, 80, 90, PRI, true], ['Helicasa', 425, 210, 100, HEL], ['Topoisomerasa', 600, 165, 130, TOPO]] } },
    { t: 'Hebra adelantada: continua', x: 'La <b class="clave">ADN polimerasa III</b> añade desoxirribonucleótidos complementarios (A–T, G–C) al extremo 3′ del cebador, siempre en sentido <b class="clave">5′→3′</b>. En esta hebra avanza en el <b class="clave">mismo sentido que la horquilla</b>: es la <b class="clave">hebra adelantada</b>, que se sintetiza de forma <b class="clave">continua</b> con un solo cebador.',
      e: { fx: 600, cebA: [60, 110], adel: [110, 540], ssb: [[150, 300], [250, 300], [350, 300], [450, 300]], enz: [['ADN pol III', 540, 80, 110, POL3, true], ['Helicasa', 595, 210, 100, HEL], ['Topoisomerasa', 770, 165, 130, TOPO]] } },
    { t: 'Hebra retrasada: fragmentos de Okazaki', x: 'La otra hebra molde va en sentido contrario. Como la polimerasa solo sintetiza 5′→3′, aquí trabaja <b class="clave">en sentido opuesto al avance</b> de la horquilla, en trozos: los <b class="clave">fragmentos de Okazaki</b>. Cada uno empieza con su propio <b>cebador de ARN</b> puesto por la primasa. Es la <b class="clave">hebra retrasada</b>, que se sintetiza de forma <b class="clave">discontinua</b>.',
      e: { fx: 600, cebA: [60, 110], adel: [110, 540], frag: [{ adn: [120, 470], ceb: [470, 520] }], enz: [['ADN pol III', 120, 340, 110, POL3, true], ['ADN pol III', 540, 80, 110, POL3], ['Helicasa', 595, 210, 100, HEL], ['Topoisomerasa', 770, 165, 130, TOPO]] } },
    { t: 'La horquilla avanza', x: 'La helicasa sigue abriendo el ADN. La hebra adelantada se alarga sin interrupción; en la retrasada, la primasa pone un nuevo cebador cerca de la horquilla y la polimerasa fabrica <b>otro fragmento de Okazaki</b>, que crece hasta llegar al cebador del anterior.',
      e: { fx: 820, cebA: [60, 110], adel: [110, 760], frag: [{ adn: [120, 470], ceb: [470, 520] }, { adn: [520, 690], ceb: [690, 740] }], enz: [['ADN pol III', 760, 80, 110, POL3], ['ADN pol III', 575, 340, 110, POL3, true], ['Helicasa', 815, 210, 100, HEL], ['Topoisomerasa', 905, 150, 130, TOPO]] } },
    { t: 'La ADN polimerasa I quita los cebadores', x: 'La <b class="clave">ADN polimerasa I</b> <b class="clave">elimina el cebador de ARN</b> y rellena el hueco con ADN. Lo mismo hace con todos los cebadores, también el de la hebra adelantada. Entre los fragmentos queda un pequeño corte en el esqueleto.',
      e: { fx: 820, adel: [60, 760], frag: [{ adn: [120, 470] }, { adn: [470, 690], ceb: [690, 740] }], enz: [['ADN pol I', 480, 340, 110, POL1, true], ['Helicasa', 815, 210, 100, HEL]], nota: '…queda un corte entre el primer fragmento y el siguiente' } },
    { t: 'La ADN ligasa une los fragmentos', x: 'La <b class="clave">ADN ligasa</b> <b class="clave">une los fragmentos de Okazaki</b> formando un enlace fosfodiéster. Al final, cada molécula de ADN tiene <b class="clave">una hebra antigua y otra nueva</b> (azul + verde): la replicación es <b class="clave">semiconservativa</b>.',
      e: { fx: 820, adel: [60, 760], frag: [{ adn: [120, 690], ceb: [690, 740] }], enz: [['ADN ligasa', 470, 340, 120, LIG, true], ['Helicasa', 815, 210, 100, HEL]], nota: 'cada nueva doble hélice = una hebra antigua (azul) + una nueva (verde)' } }
  ];

  /* ═════════ TRANSCRIPCIÓN (procariotas) ═════════ */
  var COD = 'ACTATGGCTTTCTAA', MOL = 'TGATACCGAAAGATT', ARN = 'ACUAUGGCUUUCUAA';
  function dibujoTranscripcion(e) {
    var s = '', x0 = 270, dx = 30, yC = 150, yM = 250, yR = 330;
    // regiones del gen
    s += '<rect x="70" y="118" width="180" height="164" rx="10" fill="#fff4df"/>' + texto(160, 108, 'promotor', { color: '#c77d00' });
    s += '<rect x="' + (x0 + COD.length * dx + 5) + '" y="118" width="150" height="164" rx="10" fill="#fbeae8"/>' + texto(x0 + COD.length * dx + 80, 108, 'terminador', { color: '#b03a2e' });
    s += linea(40, yC, 960, yC, C.viejo, 4) + linea(40, yM, 960, yM, C.viejo, 4);
    s += texto(28, yC + 6, '5′', { color: C.viejo }) + texto(978, yC + 6, '3′', { color: C.viejo }) + texto(28, yM + 6, '3′', { color: C.viejo }) + texto(978, yM + 6, '5′', { color: C.viejo });
    s += texto(40, yC - 66, 'cadena codificante', { ancla: 'start', color: C.viejo, tam: 15 }) + texto(40, yM + 55, 'cadena molde (se lee 3′→5′)', { ancla: 'start', color: C.viejo, tam: 15 });
    for (var i = 0; i < COD.length; i++) {
      var x = x0 + i * dx + dx / 2, abierta = e.burbuja && i >= e.burbuja[0] && i < e.burbuja[1];
      s += texto(x, yC - (abierta ? 18 : -26), COD[i], { mono: true, tam: 17, color: C.tinta });
      s += texto(x, yM + (abierta ? 28 : -14), MOL[i], { mono: true, tam: 17, color: C.tinta });
      if (!abierta) s += linea(x, yC + 32, x, yM - 30, '#c8d2dc', 2);
    }
    if (e.arn) {
      s += texto(x0 - 10, yR + 6, '5′', { color: C.arn, ancla: 'end' });
      for (i = 0; i < e.arn; i++) s += texto(x0 + i * dx + dx / 2, yR + 6, ARN[i], { mono: true, tam: 19, color: C.arn });
      if (e.fin) s += texto(x0 + e.arn * dx + 6, yR + 6, '…3′', { color: C.arn, ancla: 'start' });
      s += texto(x0 - 30, yR + 30, 'ARN', { color: C.arn, ancla: 'end', tam: 15 });
    }
    if (e.pol !== undefined) {
      var px = e.pol;
      s += '<g class="aparece"><rect x="' + (px - 95) + '" y="' + (yC - 52) + '" width="190" height="' + (yM - yC + 104) + '" rx="40" fill="#6d3fc0" fill-opacity="0.18" stroke="#6d3fc0" stroke-width="3"/>' +
        texto(px, yC - 62, 'ARN polimerasa', { color: '#6d3fc0' }) + '</g>';
    }
    if (e.nota) s += texto(500, 400, e.nota, { color: C.suave, tam: 15, peso: 600 });
    return svg(s);
  }
  var TRANSCRIPCION = [
    { t: 'Un gen en el ADN', x: 'Se transcribe <b class="clave">una sola cadena</b>: la <b class="clave">cadena molde</b>. La otra, la <b class="clave">cadena codificante</b>, es complementaria y antiparalela. Antes del gen está el <b class="clave">promotor</b> y al final, la <b class="clave">señal de terminación</b>.',
      e: {} },
    { t: 'Iniciación: la ARN polimerasa se une al promotor', x: 'La <b class="clave">ARN polimerasa</b> reconoce el <b class="clave">promotor</b> y se une a él <span class="extra">(en bacterias, gracias a su factor σ)</span>.',
      e: { pol: 160 } },
    { t: 'Abre la doble hélice y empieza sin cebador', x: 'La propia ARN polimerasa <b>abre la doble hélice</b> (no necesita helicasa) y empieza a unir <b class="clave">ribonucleótidos complementarios</b> a la cadena molde: frente a T pone A, frente a A pone <b>U</b>, frente a G pone C y frente a C pone G. <b>No necesita cebador.</b>',
      e: { pol: x0p(1), burbuja: [0, 4], arn: 3 } },
    { t: 'Elongación', x: 'La polimerasa avanza leyendo la molde en sentido <b class="clave">3′→5′</b>, y el ARN crece en sentido <b class="clave">5′→3′</b>. Detrás de ella, el ADN <b>vuelve a cerrarse</b>.',
      e: { pol: x0p(5), burbuja: [3, 8], arn: 7 } },
    { t: 'Elongación (continúa)', x: 'Cada nuevo ribonucleótido se une al anterior por un <b>enlace fosfodiéster</b>. El ARN se va separando del ADN.',
      e: { pol: x0p(10), burbuja: [8, 13], arn: 12 } },
    { t: 'Terminación', x: 'Al transcribir la <b class="clave">señal de terminación</b>, la polimerasa se separa y se libera el ARN. Compara: el ARN tiene la <b class="clave">misma secuencia que la cadena codificante, con U en lugar de T</b>.',
      e: { arn: 15, fin: true, nota: 'codificante 5′-ACT ATG GCT TTC TAA-3′  →  ARN 5′-ACU AUG GCU UUC UAA…-3′' } }
  ];
  function x0p(i) { return 270 + i * 30 + 15; }

  /* ═════════ TRADUCCIÓN ═════════ */
  var CODONES = ['ACU', 'AUG', 'GCU', 'UUC', 'UAA'], ANTI = { AUG: 'UAC', GCU: 'CGA', UUC: 'AAG' }, AA = { AUG: 'Met', GCU: 'Ala', UUC: 'Phe' };
  var AAC = { Met: '#c77d00', Ala: '#1e7a4c', Phe: '#2f62d6' };
  function cx(i) { return 150 + i * 120 + 60; }        // centro del codón i
  function arnt(i, aa, pepAqui, cadena, sale) {
    // ARNt en el codón i: tallo con anticodón abajo; el aminoácido (o la cadena) arriba
    var x = cx(i), y0 = 300, s = '<g class="' + (sale ? 'sale' : 'aparece') + '">';
    s += '<path d="M' + (x - 26) + ' ' + (y0 - 12) + ' L' + (x - 26) + ' ' + (y0 - 105) + ' Q' + x + ' ' + (y0 - 130) + ' ' + (x + 26) + ' ' + (y0 - 105) + ' L' + (x + 26) + ' ' + (y0 - 12) + ' Z" fill="#e7f0f8" stroke="#5c6b78" stroke-width="2"/>';
    s += texto(x, y0 - 18, ANTI[CODONES[i]], { mono: true, tam: 16, color: '#5c6b78' });
    if (aa || cadena) {
      var aas = cadena || [aa];
      aas.forEach(function (a, k) {
        var ay = y0 - 140 - (aas.length - 1 - k) * 40;
        s += '<circle cx="' + x + '" cy="' + ay + '" r="18" fill="' + AAC[a] + '"/>' + texto(x, ay + 5, a, { tam: 13, color: '#fff' });
        if (k > 0) s += linea(x, ay - 22, x, ay - 18, '#1f2d3a', 3);
      });
    }
    return s + '</g>';
  }
  function dibujoTraduccion(e) {
    var s = '', y = 300;
    if (e.p !== undefined && e.menor) s += '<g class="aparece"><ellipse cx="' + cx(e.p) + '" cy="' + (y + 56) + '" rx="200" ry="34" fill="#9a6fd6" fill-opacity="0.35" stroke="#7b55c0" stroke-width="2"/>' + texto(cx(e.p) + 230, y + 90, 'subunidad menor', { tam: 14, color: '#7b55c0', ancla: 'start' }) + '</g>';
    // ARNm con sus codones
    s += texto(130, y + 36, '5′', { color: C.arn, ancla: 'end' }) + texto(cx(4) + 80, y + 36, '…3′', { color: C.arn, ancla: 'start' });
    CODONES.forEach(function (c, i) {
      s += '<rect x="' + (cx(i) - 58) + '" y="' + (y + 12) + '" width="116" height="38" rx="6" fill="' + (i === 1 || i === 4 ? '#fde7ef' : '#fff') + '" stroke="' + C.arn + '" stroke-width="2"/>';
      s += texto(cx(i), y + 38, c, { mono: true, tam: 19, color: C.arn });
    });
    s += texto(cx(1), y + 72, 'inicio', { tam: 13, color: C.suave }) + texto(cx(4), y + 72, 'terminación', { tam: 13, color: C.suave });
    // ribosoma: subunidad menor bajo el ARNm, mayor encima con los sitios E, P, A
    if (e.p !== undefined) {
      var px = cx(e.p);
      if (e.mayor) {
        s += '<g class="aparece"><rect x="' + (px - 190) + '" y="' + (y - 210) + '" width="380" height="205" rx="70" fill="#9a6fd6" fill-opacity="0.18" stroke="#7b55c0" stroke-width="2"/>' +
          texto(px + 230, y - 180, 'subunidad mayor', { tam: 14, color: '#7b55c0', ancla: 'start' });
        ['E', 'P', 'A'].forEach(function (l, k) { s += texto(px + (k - 1) * 120, y - 188, l, { tam: 18, color: '#7b55c0' }); });
        s += '</g>';
      }
    }
    (e.t || []).forEach(function (r) { s += arnt(r[0], r[1], false, r[2], r[3]); });
    if (e.fl) s += '<g class="aparece"><rect x="' + (cx(4) - 34) + '" y="' + (y - 130) + '" width="68" height="120" rx="14" fill="#b03a2e"/>' + texto(cx(4), y - 66, 'FL', { color: '#fff' }) + texto(cx(4), y - 140, 'factor de liberación', { tam: 13, color: '#b03a2e' }) + '</g>';
    if (e.libre) {
      s += '<g class="aparece">';
      ['Met', 'Ala', 'Phe'].forEach(function (a, k) { s += '<circle cx="' + (700 + k * 44) + '" cy="70" r="18" fill="' + AAC[a] + '"/>' + texto(700 + k * 44, 75, a, { tam: 13, color: '#fff' }); });
      s += texto(744, 112, 'polipéptido liberado', { tam: 14, color: C.suave }) + '</g>';
    }
    if (e.activa) {
      s += '<g class="aparece"><rect x="60" y="30" width="420" height="120" rx="16" fill="#fff4df" stroke="#c77d00"/>' +
        texto(270, 58, 'aminoacil-ARNt sintetasa', { color: '#c77d00' }) +
        '<circle cx="120" cy="105" r="18" fill="#c77d00"/>' + texto(120, 110, 'Met', { tam: 13, color: '#fff' }) +
        texto(175, 110, '+  ARNt  +  ATP', { ancla: 'start' }) + texto(420, 110, '→  Met-ARNt', { ancla: 'middle' }) + '</g>';
    }
    if (e.nota) s += texto(500, 412, e.nota, { color: C.suave, tam: 15, peso: 600 });
    return svg(s);
  }
  var TRADUCCION = [
    { t: 'Activación de los aminoácidos', x: 'En el citoplasma, la enzima <b class="clave">aminoacil-ARNt sintetasa</b> une cada aminoácido a su ARNt, con gasto de <b>ATP</b>. Se forma el <b>aminoacil-ARNt</b>. Abajo, el ARNm que vamos a traducir.',
      e: { activa: true } },
    { t: 'Iniciación: la subunidad menor', x: 'La <b class="clave">subunidad menor</b> del ribosoma se une al ARNm y localiza el <b class="clave">codón de inicio AUG</b>.',
      e: { p: 1, menor: true } },
    { t: 'El ARNt iniciador, en el sitio P', x: 'El <b>ARNt iniciador</b>, que lleva <b>metionina</b> y tiene el anticodón <b>UAC</b> (complementario de AUG), se coloca sobre el codón de inicio.',
      e: { p: 1, menor: true, t: [[1, 'Met']] } },
    { t: 'Se une la subunidad mayor', x: 'Se une la <b class="clave">subunidad mayor</b> y el ribosoma queda completo, con tres sitios: <b>E</b> (salida), <b>P</b> (peptidil), donde está el ARNt iniciador, y <b>A</b> (aminoacil), libre frente al siguiente codón.',
      e: { p: 1, menor: true, mayor: true, t: [[1, 'Met']] } },
    { t: 'Elongación: entra un aminoacil-ARNt en A', x: 'Entra en el <b>sitio A</b> el aminoacil-ARNt cuyo <b class="clave">anticodón es complementario</b> del codón: frente a GCU, el ARNt con anticodón CGA, que lleva <b>alanina</b>.',
      e: { p: 1, menor: true, mayor: true, t: [[1, 'Met'], [2, 'Ala']] } },
    { t: 'Se forma el enlace peptídico', x: 'La <b class="clave">peptidil transferasa</b> forma el <b class="clave">enlace peptídico</b> entre el carboxilo de la metionina y el amino de la alanina. El dipéptido queda en el ARNt del sitio A; el ARNt del sitio P se queda sin aminoácido.',
      e: { p: 1, menor: true, mayor: true, t: [[1, null], [2, null, ['Met', 'Ala']]] } },
    { t: 'Translocación', x: '<b class="clave">Translocación</b>: el ribosoma <b>avanza un codón</b> hacia el extremo 3′. El ARNt con el dipéptido pasa al sitio P, el ARNt vacío pasa al sitio E y sale, y el sitio A queda libre frente a UUC.',
      e: { p: 2, menor: true, mayor: true, t: [[1, null, null, true], [2, null, ['Met', 'Ala']]] } },
    { t: 'Otro aminoácido, otro enlace', x: 'Entra en A el ARNt con anticodón AAG, que lleva <b>fenilalanina</b>, y se forma un nuevo enlace peptídico: el tripéptido <b>Met-Ala-Phe</b> queda en el ARNt del sitio A.',
      e: { p: 2, menor: true, mayor: true, t: [[2, null], [3, null, ['Met', 'Ala', 'Phe']]] } },
    { t: 'Nueva translocación', x: 'El ribosoma avanza otro codón. Ahora en el sitio A está <b>UAA</b>, un <b class="clave">codón de terminación</b>, que <b>ningún ARNt reconoce</b>.',
      e: { p: 3, menor: true, mayor: true, t: [[2, null, null, true], [3, null, ['Met', 'Ala', 'Phe']]] } },
    { t: 'Terminación', x: 'Entra un <b>factor de liberación</b>, se <b class="clave">libera el polipéptido</b> y las <b>subunidades del ribosoma se separan</b>. La cadena se plegará después en su estructura definitiva.',
      e: { p: 3, menor: true, libre: true, fl: true, nota: 'ARNm 5′-…AUG GCU UUC UAA…-3′  →  Met-Ala-Phe' } }
  ];

  var ANIMS = {
    replicacion: { pasos: REPLICACION, dibujo: dibujoReplicacion, titulo: 'Replicación del ADN (una horquilla, procariotas)' },
    transcripcion: { pasos: TRANSCRIPCION, dibujo: dibujoTranscripcion, titulo: 'Transcripción (procariotas)' },
    traduccion: { pasos: TRADUCCION, dibujo: dibujoTraduccion, titulo: 'Traducción' }
  };

  function boton(txt, et) {
    var b = document.createElement('button'); b.type = 'button'; b.className = 'anim-btn'; b.innerHTML = txt; b.setAttribute('aria-label', et); b.title = et; return b;
  }

  function montar(fig) {
    var A = ANIMS[fig.dataset.anim]; if (!A) return;
    var n = 0, timer = null;
    var cab = document.createElement('div'); cab.className = 'anim-cab';
    var lienzo = document.createElement('div'); lienzo.className = 'anim-lienzo';
    var expl = document.createElement('div'); expl.className = 'anim-texto'; expl.setAttribute('aria-live', 'polite');
    var barra = document.createElement('div'); barra.className = 'anim-barra';
    var bIni = boton('⏮', 'Volver al principio'), bAnt = boton('◀ Anterior', 'Paso anterior'),
        bPlay = boton('▶ Reproducir', 'Reproducir automáticamente'), bSig = boton('Siguiente ▶', 'Paso siguiente');
    [bIni, bAnt, bPlay, bSig].forEach(function (b) { barra.appendChild(b); });
    var puntos = document.createElement('div'); puntos.className = 'anim-puntos';
    A.pasos.forEach(function (p, i) {
      var d = document.createElement('button'); d.type = 'button'; d.className = 'anim-punto'; d.setAttribute('aria-label', 'Paso ' + (i + 1) + ': ' + p.t);
      d.addEventListener('click', function () { parar(); ir(i); }); puntos.appendChild(d);
    });
    // versión para imprimir: todos los pasos como lista
    var lista = document.createElement('ol'); lista.className = 'anim-lista';
    A.pasos.forEach(function (p) { var li = document.createElement('li'); li.innerHTML = '<b>' + p.t + '.</b> ' + p.x; lista.appendChild(li); });
    var cap = fig.querySelector('figcaption');
    [cab, lienzo, expl, puntos, barra, lista].forEach(function (el) { fig.insertBefore(el, cap); });
    fig.tabIndex = 0;

    function ir(i) {
      n = Math.max(0, Math.min(A.pasos.length - 1, i));
      var p = A.pasos[n];
      cab.innerHTML = '<span class="anim-num">Paso ' + (n + 1) + ' de ' + A.pasos.length + '</span> ' + p.t;
      lienzo.innerHTML = A.dibujo(p.e);
      var sv = lienzo.querySelector('svg'); if (sv) sv.setAttribute('aria-label', p.t);
      expl.innerHTML = p.x;
      Array.prototype.forEach.call(puntos.children, function (d, k) { d.classList.toggle('activo', k === n); d.setAttribute('aria-current', k === n ? 'step' : 'false'); });
      bAnt.disabled = n === 0; bSig.disabled = n === A.pasos.length - 1;
    }
    function parar() { if (timer) { clearInterval(timer); timer = null; } bPlay.innerHTML = '▶ Reproducir'; }
    bAnt.addEventListener('click', function () { parar(); ir(n - 1); });
    bSig.addEventListener('click', function () { parar(); ir(n + 1); });
    bIni.addEventListener('click', function () { parar(); ir(0); });
    bPlay.addEventListener('click', function () {
      if (timer) { parar(); return; }
      if (n === A.pasos.length - 1) ir(0);
      bPlay.innerHTML = '⏸ Pausa';
      timer = setInterval(function () { if (n >= A.pasos.length - 1) { parar(); return; } ir(n + 1); }, 5500);
    });
    fig.addEventListener('keydown', function (ev) {
      if (ev.key === 'ArrowRight') { parar(); ir(n + 1); ev.preventDefault(); ev.stopPropagation(); }
      if (ev.key === 'ArrowLeft') { parar(); ir(n - 1); ev.preventDefault(); ev.stopPropagation(); }
    });
    ir(0);
  }

  function iniciar() { Array.prototype.forEach.call(document.querySelectorAll('figure.animacion'), montar); }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', iniciar); else iniciar();
})();
