#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Datos del juego «Crónicas de la Fortaleza Celular» (preguntas del Tribunal, amenazas, misiones y gremios).
Genera juego-fortaleza/datos.js, que usan las páginas de cartas y el mazo digital.

Las respuestas y palabras clave salen de los apuntes de BioCelia (temas/*.html), que siguen los criterios
oficiales de la PAU. Las amenazas solo usan hechos que están en esos apuntes.

Uso:  python tools/juego_fortaleza_datos.py
"""
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent

MAZOS = {
    'A': {'nombre': 'Biomoléculas', 'color': '#c98a1b'},
    'B': {'nombre': 'Genética molecular', 'color': '#2f62d6'},
    'C': {'nombre': 'Biología celular', 'color': '#1f8a5b'},
    'D': {'nombre': 'Metabolismo', 'color': '#c0392b'},
    'E': {'nombre': 'Microorganismos y biotecnología', 'color': '#7b4bb7'},
    'F': {'nombre': 'Inmunología', 'color': '#0a8fa8'},
}

# (pregunta, respuesta, palabras clave, tema de los apuntes)
P = {
'A': [
 ('¿Qué enlace une dos monosacáridos y cómo se forma?', 'Enlace O-glucosídico, entre dos grupos –OH, con pérdida de una molécula de agua.', ['O-glucosídico', 'agua'], 'a2'),
 ('Cita los dos polisacáridos de reserva y en qué seres vivos aparece cada uno.', 'Almidón en los vegetales y glucógeno en los animales.', ['almidón', 'glucógeno'], 'a2'),
 ('¿Qué función tiene la celulosa y dónde se encuentra?', 'Función estructural: forma la pared celular de los vegetales.', ['estructural', 'pared celular'], 'a2'),
 ('¿Por qué los fosfolípidos forman una bicapa en el agua?', 'Son anfipáticos: cabeza polar hidrófila hacia el agua y colas apolares hidrófobas enfrentadas hacia dentro.', ['anfipáticos', 'hidrófila', 'hidrófoba'], 'a3'),
 ('¿Qué es la saponificación?', 'La hidrólisis de un lípido con enlace éster mediante una base fuerte; produce jabón (sales de ácidos grasos).', ['hidrólisis', 'base', 'jabón'], 'a3'),
 ('Esteroles y esteroides, ¿son dos tipos distintos de lípidos?', 'No: los esteroles, como el colesterol, son esteroides. Son lípidos insaponificables.', ['esteroides', 'insaponificables'], 'a3'),
 ('¿Qué enlace une los aminoácidos de una proteína? Cita dos características.', 'Enlace peptídico: covalente y con carácter parcial de doble enlace, por lo que no puede girar y sus átomos quedan en un plano.', ['peptídico', 'doble enlace', 'no puede girar'], 'a4'),
 ('¿Qué es la desnaturalización de una proteína?', 'La pérdida de su estructura tridimensional, sin romper los enlaces peptídicos; la proteína pierde su función.', ['estructura tridimensional', 'enlaces peptídicos', 'función'], 'a4'),
 ('¿Qué es el centro activo de una enzima?', 'La región de la enzima a la que se une el sustrato y en la que se produce la catálisis.', ['sustrato', 'catálisis'], 'a5'),
 ('Diferencia la inhibición competitiva de la no competitiva.', 'Competitiva: el inhibidor se parece al sustrato y compite por el centro activo. No competitiva: se une a otro lugar y modifica el centro activo.', ['compite', 'centro activo'], 'a5'),
 ('¿Por qué la actividad de una enzima sube con la temperatura y después cae?', 'Al subir la temperatura aumenta la formación del complejo enzima-sustrato; por encima de la óptima, la enzima se desnaturaliza.', ['complejo enzima-sustrato', 'desnaturaliza'], 'a5'),
 ('¿Cuáles son los tres componentes de un nucleótido?', 'Una pentosa, una base nitrogenada y ácido fosfórico (fosfato).', ['pentosa', 'base nitrogenada', 'fosfato'], 'a6'),
 ('Cita dos diferencias de composición entre el ADN y el ARN.', 'El ADN tiene desoxirribosa y timina; el ARN tiene ribosa y uracilo.', ['desoxirribosa', 'ribosa', 'timina', 'uracilo'], 'a6'),
 ('¿Qué es el ATP y para qué sirve?', 'Un nucleótido (adenina, ribosa y tres fosfatos) que almacena y transfiere energía en los enlaces entre sus fosfatos.', ['nucleótido', 'energía'], 'd1'),
 ('¿Qué vitaminas son liposolubles?', 'Las vitaminas A, D, E y K.', ['A', 'D', 'E', 'K'], 'a7'),
],
'B': [
 ('¿Qué significa que la replicación del ADN es semiconservativa?', 'Cada molécula hija tiene una cadena antigua, que sirvió de molde, y otra de nueva síntesis.', ['cadena antigua', 'nueva síntesis'], 'b1'),
 ('¿Qué significa que la replicación es bidireccional?', 'Es bidireccional porque en cada origen de replicación se forman dos horquillas que avanzan en sentidos opuestos.', ['bidireccional', 'origen de replicación', 'dos horquillas'], 'b1'),
 ('¿Por qué una de las cadenas se sintetiza en fragmentos de Okazaki?', 'La ADN polimerasa solo sintetiza en sentido 5′→3′ y las cadenas son antiparalelas: la cadena retrasada se hace a trozos.', ['5′→3′', 'antiparalelas', 'retrasada'], 'b1'),
 ('¿Por qué la ADN polimerasa necesita un cebador?', 'No puede empezar una cadena: necesita un extremo 3′-OH libre, que aporta un cebador de ARN.', ['3′-OH', 'cebador de ARN'], 'b1'),
 ('¿Qué es la transcripción y qué enzima la realiza?', 'La síntesis de ARN complementario a una cadena de ADN que actúa como molde. La realiza la ARN polimerasa.', ['ARN', 'molde', 'ARN polimerasa'], 'b1'),
 ('¿Qué es el promotor?', 'La secuencia de ADN a la que se une la ARN polimerasa para iniciar la transcripción.', ['ARN polimerasa', 'iniciar la transcripción'], 'b1'),
 ('¿En qué consiste la maduración del ARNm en eucariotas?', 'Se eliminan los intrones y se unen los exones, y se añaden la caperuza (5′) y la cola de poli-A (3′).', ['intrones', 'exones', 'caperuza', 'poli-A'], 'b1'),
 ('¿Qué es un codón?', 'Un triplete de bases del ARNm que codifica un aminoácido (o una señal de inicio o de parada).', ['triplete', 'ARNm', 'aminoácido'], 'b1'),
 ('¿Qué significa que el código genético es degenerado?', 'Que varios codones codifican el mismo aminoácido.', ['varios codones', 'mismo aminoácido'], 'b1'),
 ('¿Qué significa que el código genético es universal?', 'Que es el mismo en casi todos los seres vivos.', ['mismo', 'seres vivos'], 'b1'),
 ('¿Qué función tiene el ARN de transferencia?', 'Lleva los aminoácidos al ribosoma y, con su anticodón, los coloca frente al codón correspondiente del ARNm.', ['aminoácidos', 'anticodón', 'codón'], 'b1'),
 ('¿Cuáles son las fases de la traducción?', 'Iniciación, elongación y terminación.', ['iniciación', 'elongación', 'terminación'], 'b1'),
 ('¿Dónde y cuándo se replica el ADN en una célula eucariota?', 'En el núcleo (y en mitocondrias y cloroplastos), durante la fase S de la interfase.', ['núcleo', 'fase S'], 'b1'),
 ('¿Qué es una mutación?', 'Una alteración del material genético. Puede ser génica, cromosómica o genómica.', ['alteración', 'material genético'], 'b3'),
 ('¿Por qué importa si una mutación ocurre en una célula germinal o en una somática?', 'La de una célula germinal se transmite a la descendencia; la de una somática solo afecta al individuo.', ['germinal', 'descendencia'], 'b3'),
],
'C': [
 ('¿Cómo es la membrana plasmática según el modelo del mosaico fluido?', 'Según el mosaico fluido, es una bicapa lipídica con proteínas integrales y periféricas y glúcidos en la cara externa; sus componentes se desplazan lateralmente.', ['mosaico fluido', 'bicapa lipídica', 'proteínas'], 'c1'),
 ('Diferencia el transporte pasivo del activo.', 'Pasivo: a favor de gradiente y sin gasto de energía. Activo: en contra de gradiente y con gasto de ATP.', ['gradiente', 'ATP'], 'c1'),
 ('¿Qué es la difusión facilitada?', 'Transporte pasivo, a favor de gradiente, a través de proteínas de canal o transportadoras (permeasas).', ['a favor de gradiente', 'proteínas'], 'c1'),
 ('¿Qué hace la bomba de sodio-potasio?', 'Saca 3 Na⁺ y mete 2 K⁺ en contra de gradiente, gastando un ATP: es transporte activo.', ['3 Na⁺', '2 K⁺', 'ATP'], 'c1'),
 ('Diferencia la endocitosis de la exocitosis.', 'Endocitosis: entrada de sustancias en vesículas que se forman desde la membrana. Exocitosis: salida en vesículas que se fusionan con la membrana.', ['vesículas', 'entrada', 'salida'], 'c1'),
 ('¿Qué le pasa a un glóbulo rojo en un medio hipotónico?', 'Entra agua por ósmosis, se hincha y estalla: hemólisis.', ['ósmosis', 'hemólisis'], 'c1'),
 ('¿Qué le pasa a una célula vegetal en un medio hipotónico?', 'Entra agua y la célula queda turgente; la pared celular impide que estalle.', ['turgente', 'pared celular'], 'c1'),
 ('¿Qué es la plasmólisis?', 'La pérdida de agua de una célula vegetal en un medio hipertónico: la membrana se separa de la pared.', ['hipertónico', 'se separa de la pared'], 'c1'),
 ('¿Qué función tiene el retículo endoplasmático rugoso?', 'Sintetizar en sus ribosomas las proteínas de secreción y de membrana, e iniciar su glucosilación.', ['ribosomas', 'proteínas de secreción'], 'c1'),
 ('Cita tres funciones del retículo endoplasmático liso.', 'Síntesis de lípidos, detoxificación y almacén de calcio.', ['lípidos', 'detoxificación', 'calcio'], 'c1'),
 ('¿Qué hace el aparato de Golgi?', 'Madura (glucosila), clasifica y empaqueta en vesículas las proteínas que recibe por la cara cis y expide por la cara trans; forma los lisosomas.', ['glucosila', 'vesículas', 'cis', 'trans'], 'c1'),
 ('¿Qué son los lisosomas?', 'Vesículas con enzimas hidrolíticas (hidrolasas ácidas) que realizan la digestión celular.', ['hidrolasas', 'digestión'], 'c1'),
 ('Cita tres pruebas de la teoría endosimbiótica.', 'Mitocondrias y cloroplastos tienen ADN circular, ribosomas 70S y doble membrana, y se dividen por bipartición.', ['ADN circular', '70S', 'doble membrana'], 'c1'),
 ('¿Qué ocurre en la anafase de la mitosis?', 'Se separan las cromátidas hermanas y cada una va a uno de los polos de la célula.', ['cromátidas hermanas', 'polos'], 'c2'),
 ('¿En qué se diferencia la citocinesis de una célula animal y de una vegetal?', 'Animal: estrangulamiento por un anillo contráctil. Vegetal: se forma un tabique, el fragmoplasto, a partir de vesículas del Golgi.', ['anillo contráctil', 'fragmoplasto'], 'c2'),
 ('¿Qué significado biológico tiene la meiosis?', 'Reduce a la mitad el número de cromosomas (gametos haploides) y produce variabilidad genética.', ['mitad', 'variabilidad genética'], 'c2'),
 ('¿Por qué una célula vegetal necesita mitocondrias si ya tiene cloroplastos?', 'El cloroplasto fabrica la materia orgánica, pero el ATP para sus funciones lo obtiene degradándola en la respiración celular, en las mitocondrias.', ['respiración celular', 'ATP'], 'd1'),
],
'D': [
 ('¿Dónde ocurre la glucólisis y qué se obtiene de una glucosa?', 'En el citosol: dos piruvatos, 2 ATP netos y 2 NADH.', ['citosol', 'piruvato', '2 ATP', 'NADH'], 'd2'),
 ('¿De qué tres formas se puede obtener ATP?', 'Fosforilación a nivel de sustrato, fosforilación oxidativa y fotofosforilación.', ['a nivel de sustrato', 'oxidativa', 'fotofosforilación'], 'd1'),
 ('¿Dónde ocurre el ciclo de Krebs y qué produce?', 'En la matriz mitocondrial; produce CO₂, NADH, FADH₂ y GTP.', ['matriz mitocondrial', 'CO₂', 'NADH', 'FADH₂'], 'd2'),
 ('¿Cuál es el último aceptor de electrones de la respiración aerobia?', 'El O₂, que se reduce a agua.', ['O₂', 'agua'], 'd2'),
 ('¿Dónde está la cadena respiratoria?', 'En la membrana mitocondrial interna (crestas).', ['membrana mitocondrial interna'], 'd2'),
 ('¿Por qué la fermentación rinde tan poca energía?', 'La degradación de la glucosa es incompleta: el producto final aún tiene energía; solo se obtienen los 2 ATP de la glucólisis.', ['incompleta', '2 ATP'], 'd5'),
 ('¿Para qué se reduce el piruvato en la fermentación?', 'Para regenerar el NAD⁺ que necesita la glucólisis.', ['regenerar', 'NAD⁺'], 'd5'),
 ('¿Qué produce la fermentación láctica y quién la realiza?', 'Ácido láctico; la realizan las bacterias lácticas y las células musculares sin oxígeno.', ['ácido láctico', 'bacterias lácticas'], 'd5'),
 ('¿Qué produce la fermentación alcohólica y quién la realiza?', 'Etanol y CO₂; la realizan las levaduras.', ['etanol', 'CO₂', 'levaduras'], 'd5'),
 ('¿Dónde ocurre la fase luminosa y qué se obtiene?', 'En la membrana de los tilacoides; se obtienen ATP, NADPH y O₂.', ['tilacoides', 'ATP', 'NADPH'], 'd3'),
 ('¿De dónde procede el O₂ que liberan las plantas?', 'De la fotólisis del agua, en la fase luminosa.', ['fotólisis del agua', 'fase luminosa'], 'd3'),
 ('¿Dónde ocurre el ciclo de Calvin y qué hace?', 'En el estroma: fija el CO₂ y lo reduce a azúcares con el ATP y el NADPH de la fase luminosa.', ['estroma', 'CO₂', 'ATP', 'NADPH'], 'd3'),
 ('¿Qué es la fotofosforilación?', 'La síntesis de ATP en la fase luminosa: los H⁺ acumulados en el lumen salen al estroma por la ATP sintasa.', ['ATP sintasa', 'lumen'], 'd3'),
 ('Diferencia catabolismo y anabolismo.', 'Catabolismo: degradación (oxidaciones) que libera energía. Anabolismo: síntesis (reducciones) que consume ATP.', ['degradación', 'síntesis', 'ATP'], 'd1'),
 ('¿Qué es la β-oxidación y dónde ocurre?', 'La degradación de los ácidos grasos a acetil-CoA, en la matriz mitocondrial.', ['ácidos grasos', 'acetil-CoA', 'matriz mitocondrial'], 'd2'),
 ('¿Qué es la quimiosíntesis?', 'La síntesis de materia orgánica con la energía de la oxidación de compuestos inorgánicos (bacterias quimioautótrofas).', ['oxidación', 'compuestos inorgánicos'], 'd3'),
],
'E': [
 ('Cita tres características de una célula bacteriana.', 'Es procariota (sin núcleo, con nucleoide), tiene ribosomas 70S y pared de peptidoglucano (mureína); puede tener plásmidos.', ['procariota', '70S', 'peptidoglucano'], 'e1'),
 ('¿Qué es un plásmido y para qué se usa en ingeniería genética?', 'Una pequeña molécula de ADN circular extracromosómica; se usa como vector para introducir genes.', ['ADN circular', 'vector'], 'e2'),
 ('¿Qué hacen las enzimas de restricción?', 'Cortan el ADN en secuencias específicas; permiten aislar genes e insertarlos en vectores.', ['cortan', 'secuencias específicas'], 'e2'),
 ('¿Por qué un gen humano con intrones no funciona en una bacteria?', 'Las bacterias no eliminan los intrones; se usa ADN complementario (ADNc), obtenido con transcriptasa inversa a partir del ARNm.', ['intrones', 'ADNc', 'transcriptasa inversa'], 'e2'),
 ('¿Qué hace la PCR?', 'Amplifica (copia muchas veces) un fragmento de ADN, con una ADN polimerasa resistente al calor (Taq).', ['amplifica', 'Taq'], 'e2'),
 ('¿Por qué un antibiótico puede matar bacterias sin dañar nuestras células?', 'Actúa sobre estructuras bacterianas que nuestras células no tienen, como la pared o los ribosomas 70S.', ['pared', '70S'], 'e1'),
 ('¿Qué son los virus?', 'Formas acelulares con un ácido nucleico (ADN o ARN) y una cápsida; son parásitos obligados.', ['acelulares', 'cápsida', 'parásitos obligados'], 'e1'),
 ('¿Por qué sube la masa del pan?', 'Por el CO₂ que producen las levaduras en la fermentación alcohólica.', ['CO₂', 'fermentación alcohólica'], 'd5'),
 ('¿Qué da el sabor ácido al pan de masa madre?', 'El ácido láctico que producen las bacterias lácticas (Lactobacillus) en la fermentación láctica.', ['ácido láctico', 'fermentación láctica'], 'd5'),
 ('¿Cómo se hace el yogur?', 'Bacterias lácticas fermentan la lactosa a ácido láctico; baja el pH y las proteínas de la leche coagulan.', ['lactosa', 'ácido láctico'], 'e1'),
 ('¿Qué es la biorremediación?', 'El uso de microorganismos para eliminar contaminantes del medio.', ['microorganismos', 'contaminantes'], 'e1'),
 ('¿Qué es un organismo transgénico?', 'Un organismo al que se le ha introducido un gen de otra especie.', ['gen', 'otra especie'], 'e2'),
 ('¿Por qué se usan tanto los microorganismos en la industria?', 'Crecen muy deprisa, son fáciles de cultivar, tienen un metabolismo muy variado y se pueden modificar genéticamente.', ['crecen', 'metabolismo'], 'e1'),
],
'F': [
 ('¿Qué es un antígeno?', 'Cualquier molécula capaz de desencadenar una respuesta inmunitaria.', ['respuesta inmunitaria'], 'f1'),
 ('¿Qué es un anticuerpo y qué células lo producen?', 'Una glucoproteína (inmunoglobulina) que se une de forma específica a un antígeno; lo producen las células plasmáticas.', ['inmunoglobulina', 'específica', 'células plasmáticas'], 'f1'),
 ('¿Por qué la respuesta secundaria es más eficaz que la primaria?', 'Gracias a las células de memoria: es más rápida, intensa y duradera.', ['células de memoria', 'rápida'], 'f1'),
 ('Diferencia la inmunidad activa de la pasiva.', 'Activa: el organismo fabrica sus anticuerpos (vacuna o infección) y es duradera. Pasiva: los recibe ya hechos (suero o madre) y es temporal.', ['anticuerpos', 'duradera', 'temporal'], 'f1'),
 ('Diferencia una vacuna de un suero.', 'Vacuna: antígenos; es preventiva y crea memoria. Suero: anticuerpos; es curativo y temporal.', ['antígenos', 'anticuerpos', 'memoria'], 'f1'),
 ('Diferencia la respuesta humoral de la celular.', 'Humoral: basada en los anticuerpos (linfocitos B). Celular: acción directa de células, como los linfocitos T y los macrófagos.', ['anticuerpos', 'linfocitos T'], 'f1'),
 ('¿Cómo destruye un macrófago a una bacteria?', 'Por fagocitosis: la engloba en un fagosoma, que se une a lisosomas cuyas enzimas la digieren.', ['fagocitosis', 'fagosoma', 'lisosomas'], 'f1'),
 ('¿Qué hace una célula presentadora de antígenos?', 'Un macrófago o una célula dendrítica presenta fragmentos del antígeno, unidos a moléculas del complejo mayor de histocompatibilidad, a los linfocitos T colaboradores.', ['complejo mayor de histocompatibilidad', 'T colaboradores'], 'f1'),
 ('¿Dónde maduran los linfocitos T y los B?', 'Los T, en el timo; los B, en la médula ósea.', ['timo', 'médula ósea'], 'f1'),
 ('¿Qué hacen los linfocitos T citotóxicos?', 'Destruyen las células infectadas por virus y las células tumorales.', ['células infectadas', 'tumorales'], 'f1'),
 ('¿Qué es una alergia?', 'Una respuesta exagerada (hipersensibilidad) frente a un antígeno inofensivo; intervienen la IgE y la histamina.', ['hipersensibilidad', 'IgE', 'histamina'], 'f1'),
 ('¿Qué es una enfermedad autoinmune?', 'Aquella en la que el sistema inmunitario ataca moléculas o células propias.', ['propias'], 'f1'),
 ('¿Por qué el VIH produce una inmunodeficiencia?', 'Infecta y destruye los linfocitos T colaboradores (T4), que coordinan la respuesta inmunitaria.', ['linfocitos T colaboradores', 'T4'], 'f1'),
 ('Cita barreras de la defensa inespecífica.', 'La piel y las mucosas, las secreciones (como la lisozima), la inflamación y la fagocitosis.', ['piel', 'mucosas', 'fagocitosis'], 'f1'),
],
}

# Amenazas y sucesos: celula = 'ambas' | 'animal' | 'vegetal'
AMENAZAS = [
 dict(nombre='Bacteria invasora', celula='animal', copias=2, tipo='amenaza',
      efecto='Pon una ficha de bacteria junto al Muelle. Mientras siga ahí, al final de cada ronda: −1 Homeostasis. Para eliminarla: captúrala en el Muelle (fagocitosis, Tribunal E) y llévala a la Mazmorra para digerirla (Tribunal F).',
      porque='La célula engloba la bacteria en un fagosoma, que se fusiona con los lisosomas: sus hidrolasas la digieren.'),
 dict(nombre='Plaga en la empalizada', celula='vegetal', copias=2, tipo='amenaza',
      efecto='Pon una ficha de plaga en la Empalizada. Mientras siga, al final de cada ronda: −1 Homeostasis. Para eliminarla: entrega en el Muelle una vesícula de pared (se fabrica en el Puerto de Golgi: 1 glucosa + 1 ATP).',
      porque='La pared celular protege a la célula vegetal; el aparato de Golgi fabrica polisacáridos de la pared y los envía en vesículas.'),
 dict(nombre='Virus en la muralla', celula='animal', copias=1, tipo='amenaza',
      efecto='Pon una ficha de virus en la Puerta de las Permeasas: queda cerrada. Para eliminarlo: fabrica una proteína de membrana (Biblioteca → Forja → Golgi) y entrégala en el Muelle, para que los linfocitos T citotóxicos reconozcan la célula (Tribunal F).',
      porque='Los linfocitos T citotóxicos destruyen las células infectadas por virus, que reconocen por las moléculas que estas muestran en su membrana.'),
 dict(nombre='Maldición de la colchicina', celula='ambas', copias=1, tipo='amenaza',
      efecto='Durante 2 rondas no se pueden usar las Calzadas de Microtúbulos ni montar el huso.',
      porque='La colchicina inhibe la polimerización de los microtúbulos: sin ellos no hay transporte por raíles ni huso acromático.'),
 dict(nombre='Veneno de cianuro', celula='ambas', copias=1, tipo='amenaza',
      efecto='Esta ronda, la Fragua (mitocondria) no produce ATP. Solo se puede obtener ATP por fermentación en la Plaza del Citosol.',
      porque='El cianuro bloquea una enzima de la cadena respiratoria: el transporte de electrones se para.'),
 dict(nombre='Falta de oxígeno', celula='ambas', copias=1, tipo='amenaza',
      efecto='Esta ronda, la Fragua no funciona. Solo se puede obtener ATP por fermentación en la Plaza del Citosol.',
      porque='Sin O₂, último aceptor de electrones, se detiene la respiración aerobia; la célula recurre a la fermentación.'),
 dict(nombre='Medio hipotónico', celula='ambas', copias=1, tipo='amenaza',
      efecto='Célula animal: −2 Homeostasis. Célula vegetal: sin efecto (y lo decís en voz alta: ¿por qué?).',
      porque='Entra agua por ósmosis: la célula animal se hincha y puede estallar; la vegetal queda turgente porque la pared lo impide.'),
 dict(nombre='Medio hipertónico', celula='ambas', copias=1, tipo='amenaza',
      efecto='−1 Homeostasis.',
      porque='La célula pierde agua por ósmosis: la animal se arruga y en la vegetal la membrana se separa de la pared (plasmólisis).'),
 dict(nombre='Helada', celula='ambas', copias=1, tipo='amenaza',
      efecto='Esta ronda, recoger en las puertas cuesta 2 acciones.',
      porque='Con el frío la membrana pierde fluidez.'),
 dict(nombre='Rayos ultravioleta', celula='ambas', copias=1, tipo='amenaza',
      efecto='El próximo pergamino de ARNm sale defectuoso y no sirve, salvo que antes alguien pague 1 ATP en la Biblioteca para reparar el ADN.',
      porque='Los agentes mutagénicos alteran el ADN; la célula tiene mecanismos de reparación.'),
 dict(nombre='Fiebre muy alta', celula='ambas', copias=1, tipo='amenaza',
      efecto='Retira una proteína que esté en juego (la que elija el grupo). Si no hay ninguna, −1 Homeostasis.',
      porque='Las temperaturas altas desnaturalizan las proteínas, que pierden su función.'),
 dict(nombre='Ayuno', celula='ambas', copias=1, tipo='amenaza',
      efecto='Esta ronda las puertas no dan glucosa. La Fragua puede quemar lípidos en su lugar (1 lípido → 4 ATP).',
      porque='Sin glucosa, la mitocondria obtiene acetil-CoA de los ácidos grasos por β-oxidación.'),
 dict(nombre='Veneno liposoluble', celula='animal', copias=1, tipo='amenaza',
      efecto='Pon una ficha de veneno en la Plaza del Citosol. Al final de cada ronda: −1 Homeostasis, hasta que alguien lo destoxifique en el Taller de Alquimia (1 ATP, Tribunal A).',
      porque='El retículo endoplasmático liso detoxifica sustancias tóxicas.'),
 dict(nombre='Orgánulo envejecido', celula='ambas', copias=1, tipo='amenaza',
      efecto='La Fragua no funciona hasta que alguien haga autofagia: 1 ATP en la Mazmorra (en la célula vegetal, en el Aljibe).',
      porque='Los orgánulos viejos se digieren y reciclan por autofagia.'),
 dict(nombre='Llega la noche', celula='ambas', copias=1, tipo='amenaza',
      efecto='Célula vegetal: la Torre del Sol (cloroplasto) no funciona esta ronda. Célula animal: sin efecto (¿por qué?).',
      porque='Sin luz no hay fase luminosa; la célula animal no hace fotosíntesis.'),
 dict(nombre='Antibiótico en el medio', celula='animal', copias=1, tipo='suceso',
      efecto='Retira una bacteria del exterior.',
      porque='Los antibióticos actúan sobre la pared o los ribosomas 70S de las bacterias, que la célula eucariota no tiene.'),
 dict(nombre='Banquete', celula='ambas', copias=1, tipo='suceso',
      efecto='Esta ronda, cada recogida en las puertas da 1 ficha más.',
      porque='Con más nutrientes fuera, entran más a favor de gradiente.'),
]

MISIONES = [
 dict(nombre='Secretar una hormona', celula='animal', modo='coop', premio='+2 Homeostasis',
      pasos=['Biblioteca: transcribe un ARNm', 'Forja del RER: tradúcelo (2 aminoácidos)', 'Puerto de Golgi: madura la proteína', 'Muelle: exocitosis'],
      porque='Ruta de secreción: núcleo → RER → Golgi → vesícula de secreción → membrana.'),
 dict(nombre='Reparar la muralla', celula='ambas', modo='coop', premio='+1 Homeostasis',
      pasos=['Taller de Alquimia (REL): fabrica 2 lípidos', 'Llévalos a cualquier puerta y entrégalos'],
      porque='El REL sintetiza los lípidos de las membranas.'),
 dict(nombre='Rearmar la mazmorra', celula='animal', modo='coop', premio='Las digestiones ya no necesitan Tribunal',
      pasos=['Biblioteca: ARNm', 'Forja del RER: proteína (enzimas hidrolíticas)', 'Puerto de Golgi: madúrala', 'Mazmorra: entrégala'],
      porque='Las hidrolasas se fabrican en el RER y el Golgi las empaqueta en lisosomas.'),
 dict(nombre='Instalar una bomba', celula='ambas', modo='coop', premio='La Torre de la Bomba ya no cuesta ATP',
      pasos=['Biblioteca: ARNm', 'Forja del RER: proteína de membrana', 'Puerto de Golgi: madúrala', 'Torre de la Bomba: instálala'],
      porque='Las proteínas de membrana se sintetizan en el RER y llegan a la membrana en vesículas desde el Golgi.'),
 dict(nombre='Guardar reservas', celula='ambas', modo='coop', premio='+1 Homeostasis y 2 ATP',
      pasos=['Animal: 3 glucosas + 1 ATP en la Plaza del Citosol (glucógeno)', 'Vegetal: 3 glucosas + 1 ATP en la Torre del Sol (almidón)'],
      porque='Los animales almacenan glucosa como glucógeno y los vegetales como almidón.'),
 dict(nombre='Reforzar la pared', celula='vegetal', modo='coop', premio='+2 Homeostasis',
      pasos=['Puerto de Golgi: 1 glucosa + 1 ATP (polisacáridos de la pared)', 'Muelle: exocitosis hacia la Empalizada'],
      porque='El Golgi sintetiza polisacáridos de la pared vegetal y los envía en vesículas.'),
 dict(nombre='Mantener la turgencia', celula='vegetal', modo='coop', premio='+2 Homeostasis',
      pasos=['Lleva 2 fichas cualesquiera (solutos) al Aljibe', 'Paga 1 ATP para meterlas en la vacuola'],
      porque='La vacuola acumula solutos; entra agua por ósmosis y la célula queda turgente.'),
 dict(nombre='Expansión del reino (división)', celula='ambas', modo='ambos', premio='+3 Homeostasis (en el modo competitivo, gana quien la complete primero)',
      pasos=['Biblioteca: replica el ADN (2 nucleótidos + 2 ATP, fase S)', 'Plaza del Citosol: fabrica tubulina en los ribosomas libres (ARNm + 2 aminoácidos + 1 ATP)',
             'Animal: Centrosoma · Vegetal: Polos del huso: monta el huso (tubulina + 2 ATP)',
             'Citocinesis. Animal: anillo contráctil en cualquier puerta (2 ATP). Vegetal: fragmoplasto, desde el Puerto de Golgi (1 glucosa + 1 ATP)'],
      porque='El ADN se replica en la fase S; el huso, de microtúbulos de tubulina, separa las cromátidas; la citocinesis es por estrangulamiento en la célula animal y por fragmoplasto en la vegetal.'),
]

GREMIOS = [
 dict(nombre='Maestre de la Biblioteca', organulo='Núcleo', celula='ambas', inicio='Gran Biblioteca',
      poder='Transcribir te cuesta 1 ATP menos (mínimo 0).'),
 dict(nombre='Maestra Forjadora', organulo='Retículo endoplasmático rugoso', celula='ambas', inicio='Forja del RER',
      poder='Al traducir en la Forja, necesitas 1 aminoácido menos.'),
 dict(nombre='Alquimista', organulo='Retículo endoplasmático liso', celula='ambas', inicio='Taller de Alquimia',
      poder='Al fabricar lípidos obtienes 1 más.'),
 dict(nombre='Capitana del Puerto', organulo='Aparato de Golgi', celula='ambas', inicio='Puerto de Golgi',
      poder='Puedes llevar 6 fichas en vez de 4 y moverte 2 lugares con una sola acción.'),
 dict(nombre='Guardián de la Muralla', organulo='Membrana plasmática', celula='ambas', inicio='Puerta de las Permeasas',
      poder='Recoger en una puerta te da 1 ficha más.'),
 dict(nombre='Señor de la Fragua', organulo='Mitocondria', celula='ambas', inicio='Fragua de la Mitocondria',
      poder='Al respirar obtienes 1 ATP más.'),
 dict(nombre='Carcelera de la Mazmorra', organulo='Lisosoma', celula='animal', inicio='Mazmorra Ácida',
      poder='Puedes capturar una bacteria estando en la Mazmorra, sin ir al Muelle: los lisosomas acuden al fagosoma.'),
 dict(nombre='Guardiana del Sol', organulo='Cloroplasto', celula='vegetal', inicio='Torre del Sol',
      poder='La fotosíntesis te da 1 glucosa más.'),
 dict(nombre='Señora del Aljibe', organulo='Vacuola', celula='vegetal', inicio='Gran Aljibe',
      poder='Una vez por ronda, puedes anular la pérdida de Homeostasis de un medio hipertónico o hipotónico.'),
]


# Trampas: afirmaciones con un error típico de examen (de la Ponencia de noviembre de 2026 y de los criterios).
# Hay que decir qué está mal y corregirlo con la palabra clave.
TRAMPAS = [
 ('La replicación del ADN avanza a ambos lados del origen.', 'Hay que escribir que es bidireccional: «a ambos lados» no puntuó en la PAU de 2026.', 'bidireccional'),
 ('En la replicación se unen nucleótidos.', 'Se unen desoxirribonucleótidos.', 'desoxirribonucleótidos'),
 ('En la fase luminosa el ATP se forma por fosforilación.', 'Se forma por fotofosforilación.', 'fotofosforilación'),
 ('La fase oscura de la fotosíntesis ocurre en la mitocondria.', 'Ocurre en el estroma del cloroplasto (ciclo de Calvin).', 'estroma'),
 ('Como tiene cloroplastos, la célula vegetal no necesita mitocondrias.', 'Las necesita: obtiene su ATP por respiración celular en las mitocondrias.', 'respiración celular'),
 ('Esteroles y esteroides son dos tipos distintos de lípidos insaponificables.', 'Los esteroles, como el colesterol, son esteroides.', 'esteroides'),
 ('El ATP solo se obtiene por fosforilación oxidativa y fotofosforilación.', 'Falta la fosforilación a nivel de sustrato (glucólisis, ciclo de Krebs).', 'a nivel de sustrato'),
 ('La masa madre tiene sabor ácido por la fermentación.', 'Hay que decir cuál: la fermentación láctica produce ácido láctico.', 'ácido láctico'),
 ('El nucléolo está rodeado por una membrana.', 'El nucléolo no tiene membrana: es una zona sin membrana del núcleo.', 'sin membrana'),
 ('Los centriolos son orgánulos con membrana.', 'Los centriolos son estructuras sin membrana, formadas por microtúbulos (9 tripletes).', 'sin membrana'),
 ('El ciclo de Krebs ocurre en las crestas mitocondriales.', 'Ocurre en la matriz mitocondrial; en la membrana interna (crestas) está la cadena respiratoria.', 'matriz'),
 ('Un ribosoma de 60S y otro de 40S forman un ribosoma de 100S.', 'Forman un ribosoma 80S: los coeficientes de sedimentación no se suman.', '80S'),
 ('La cara trans del Golgi recibe las vesículas del RER.', 'Las recibe la cara cis; por la cara trans salen las vesículas.', 'cara cis'),
 ('Los ribosomas del cloroplasto son 80S, como los del citosol.', 'Son 70S, como los de las bacterias: es una prueba de la endosimbiosis.', '70S'),
 ('El glucocáliz recubre las dos caras de la membrana.', 'Solo está en la cara externa.', 'cara externa'),
 ('El retículo endoplasmático liso sintetiza proteínas de secreción.', 'Eso lo hace el rugoso (RER), con sus ribosomas; el REL sintetiza lípidos y destoxifica.', 'rugoso'),
 ('Una célula animal en un medio hipotónico queda turgente.', 'Se hincha y estalla (hemólisis en el glóbulo rojo); la turgencia es de la célula vegetal, que tiene pared.', 'estalla'),
 ('En la anafase mitótica se separan los cromosomas homólogos.', 'Se separan las cromátidas hermanas; los homólogos se separan en la anafase I de la meiosis.', 'cromátidas hermanas'),
 ('La fermentación obtiene la misma energía que la respiración, pero sin oxígeno.', 'Obtiene muy poca: la degradación es incompleta y solo da 2 ATP.', 'incompleta'),
 ('Los iones atraviesan libremente la bicapa lipídica.', 'Necesitan proteínas de canal o transportadoras: el interior de la bicapa es hidrófobo.', 'proteínas'),
]

# Fichas de orgánulo: la carta de referencia de cada lugar del tablero.
ORGANULOS = [
 dict(lugar='Gran Biblioteca', organulo='Núcleo', membranas=2, celula='ambas',
      anatomia='Envoltura de doble membrana con poros, nucleoplasma, cromatina (ADN y proteínas) y nucléolo, que no tiene membrana.',
      poder=['envoltura nuclear', 'poros nucleares', 'cromatina', 'nucléolo'],
      conexion='Sus pergaminos (ARNm) salen por los poros hacia los ribosomas y la Forja del RER.',
      trampa='El nucléolo no tiene membrana.'),
 dict(lugar='Forja del RER', organulo='Retículo endoplasmático rugoso', membranas=1, celula='ambas',
      anatomia='Sáculos aplanados comunicados, con ribosomas en su cara externa; continúa con la envoltura nuclear.',
      poder=['ribosomas', 'proteínas de secreción', 'glucosilación'],
      conexion='Envía sus proteínas en vesículas a la cara cis del Golgi.',
      trampa='No confundirlo con el REL, que no tiene ribosomas.'),
 dict(lugar='Taller de Alquimia', organulo='Retículo endoplasmático liso', membranas=1, celula='ambas',
      anatomia='Red de túbulos sin ribosomas, comunicada con el RER.',
      poder=['síntesis de lípidos', 'detoxificación', 'calcio'],
      conexion='Sus lípidos renuevan las membranas de toda la fortaleza.',
      trampa='La palabra clave es «detoxificación» (o destoxificación).'),
 dict(lugar='Puerto de Golgi', organulo='Aparato de Golgi', membranas=1, celula='ambas',
      anatomia='Dictiosomas: pilas de sáculos aplanados con una cara cis (hacia el RER) y una cara trans, de la que salen vesículas.',
      poder=['cara cis', 'cara trans', 'glucosilación', 'vesículas de secreción'],
      conexion='Recibe del RER; expide hacia la membrana (exocitosis) y forma los lisosomas.',
      trampa='La cara cis es la que mira al RER.'),
 dict(lugar='Mazmorra Ácida', organulo='Lisosoma', membranas=1, celula='animal',
      anatomia='Vesícula con enzimas hidrolíticas que trabajan a pH ácido.',
      poder=['hidrolasas ácidas', 'heterofagia', 'autofagia'],
      conexion='Se fusiona con los fagosomas que llegan del Muelle.',
      trampa='Sus enzimas se fabrican en el RER, no en el lisosoma.'),
 dict(lugar='Fragua de la Mitocondria', organulo='Mitocondria', membranas=2, celula='ambas',
      anatomia='Doble membrana: la externa lisa y la interna plegada en crestas; matriz con ADN circular y ribosomas 70S.',
      poder=['crestas', 'matriz', 'ciclo de Krebs', 'fosforilación oxidativa'],
      conexion='Quema la glucosa (o los lípidos) que llega por la muralla y reparte el ATP a toda la fortaleza.',
      trampa='El ciclo de Krebs ocurre en la matriz, no en las crestas.'),
 dict(lugar='Torre del Sol', organulo='Cloroplasto', membranas=2, celula='vegetal',
      anatomia='Doble membrana, estroma con ADN circular y ribosomas 70S, y tilacoides apilados en grana.',
      poder=['tilacoides', 'estroma', 'fase luminosa', 'ciclo de Calvin'],
      conexion='Fabrica la glucosa que luego queman las mitocondrias de la misma célula.',
      trampa='La fase oscura (ciclo de Calvin) ocurre en el estroma.'),
 dict(lugar='Gran Aljibe', organulo='Vacuola', membranas=1, celula='vegetal',
      anatomia='Gran saco rodeado por el tonoplasto; en la célula vegetal adulta ocupa casi todo el volumen.',
      poder=['tonoplasto', 'turgencia', 'almacén'],
      conexion='Con la pared celular, mantiene la turgencia en un medio hipotónico.',
      trampa='Hay que usar la palabra «turgencia».'),
 dict(lugar='Centrosoma', organulo='Centrosoma (centriolos)', membranas=0, celula='animal',
      anatomia='Dos centriolos perpendiculares (diplosoma), cada uno de 9 tripletes de microtúbulos, sin membrana.',
      poder=['diplosoma', '9 tripletes', 'huso acromático'],
      conexion='Organiza los microtúbulos: las calzadas del tablero y el huso de la división.',
      trampa='Las células vegetales no tienen centriolos, pero sí forman huso.'),
 dict(lugar='Plaza del Citosol', organulo='Citosol y ribosomas libres', membranas=0, celula='ambas',
      anatomia='Medio acuoso con enzimas y ribosomas libres (80S: subunidades 60S y 40S), sin membrana.',
      poder=['glucólisis', 'ribosomas libres', '80S'],
      conexion='La glucólisis da el piruvato que entra en la mitocondria.',
      trampa='60S + 40S forman un ribosoma 80S, no 100S.'),
 dict(lugar='Puertas de la muralla', organulo='Membrana plasmática', membranas=1, celula='ambas',
      anatomia='Bicapa lipídica con proteínas integrales y periféricas, colesterol y glucocáliz en la cara externa.',
      poder=['mosaico fluido', 'bicapa lipídica', 'permeabilidad selectiva'],
      conexion='Por sus permeasas y bombas entran las materias primas.',
      trampa='Los iones no atraviesan la bicapa: necesitan proteínas.'),
]


def main():
    preguntas = []
    for mazo, lista in P.items():
        for i, (q, r, claves, tema) in enumerate(lista, 1):
            assert all(c.lower() in r.lower() for c in claves), (mazo, i, claves)
            preguntas.append(dict(id=f'{mazo}{i:02d}', mazo=mazo, pregunta=q, respuesta=r, claves=claves, tema=tema))
    trampas = [dict(id=f'T{i:02d}', afirmacion=a, correccion=c, clave=k) for i, (a, c, k) in enumerate(TRAMPAS, 1)]
    for t in trampas:
        assert t['clave'].lower() in t['correccion'].lower(), t
    datos = dict(mazos=MAZOS, preguntas=preguntas, amenazas=AMENAZAS, misiones=MISIONES, gremios=GREMIOS,
                 trampas=trampas, organulos=ORGANULOS)
    salida = RAIZ / 'juego-fortaleza' / 'datos.js'
    salida.parent.mkdir(exist_ok=True)
    salida.write_text('// Generado por tools/juego_fortaleza_datos.py: no editar a mano.\nwindow.FORTALEZA = '
                      + json.dumps(datos, ensure_ascii=False, indent=1) + ';\n', encoding='utf-8')
    print(len(preguntas), 'preguntas ·', len(AMENAZAS), 'amenazas ·', len(MISIONES), 'misiones ·', len(GREMIOS), 'gremios ·', len(TRAMPAS), 'trampas ·', len(ORGANULOS), 'orgánulos')


if __name__ == '__main__':
    main()
