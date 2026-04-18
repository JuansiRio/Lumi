# 📚 BIBLIOTECA DE PREGUNTAS CRÍTICAS — LUMI v2.0
### *Epistemología del interrogatorio jurídico aplicada al litigio colombiano*

> Documento operacional y epistémico del sistema Lumi
> Autor base: Felipe Cruz
> Versión 3.0 — Abril 2026 — Generalización a roles genéricos
> **CONFIDENCIAL — DOCUMENTO VIVO**

---

## FUNDAMENTOS EPISTEMOLÓGICOS DEL INTERROGATORIO JURÍDICO

### Por qué el interrogatorio es más difícil que el análisis

El análisis jurídico trabaja con hechos. El interrogatorio trabaja con relatos sobre hechos narrados por personas que tienen intereses en cómo esos hechos son percibidos. Eso es epistemológicamente diferente.

Un hecho es lo que ocurrió. Un relato es la construcción narrativa que el cliente hace de lo que ocurrió, filtrada por su memoria, su interpretación, su vergüenza, su miedo, su esperanza de resultado, y su comprensión del sistema jurídico. El abogado que trata el relato del cliente como si fuera el hecho opera con un mapa incorrecto.

Esta biblioteca no contiene solo preguntas. Contiene una teoría del interrogatorio jurídico basada en cuatro proposiciones:

**Proposición 1 — El cliente no miente, pero tampoco dice la verdad**
La mayoría de los clientes no son deliberadamente deshonestos. Pero tienen falsos recuerdos (especialmente sobre hechos traumáticos), racionalizaciones consolidadas (historias que se han contado a sí mismos tantas veces que se volvieron reales), omisiones estratégicas inconscientes (no mencionan lo que los hace quedar mal, sin decidir conscientemente omitirlo), y lagunas genuinas (simplemente no saben o no recuerdan). El interrogatorio debe diseñarse para trabajar con esta realidad, no ignorarla.

**Proposición 2 — Lo que el cliente quiere decir que quiere y lo que realmente quiere son frecuentemente cosas distintas**
Un cliente que dice "quiero que me paguen lo que me deben" puede realmente querer vindication moral, reconocimiento de que lo que le hicieron estuvo mal, o simplemente que el proceso termine y él pueda seguir con su vida. La estrategia óptima para cada uno de esos objetivos reales es diferente. Si el abogado no sabe cuál es el objetivo real, puede ganar el caso y perder al cliente.

**Proposición 3 — El sistema jurídico colombiano no es el único sistema normativo relevante**
Colombia tiene pluralismo jurídico real: el derecho estatal formal coexiste con el derecho propio de comunidades indígenas, con el derecho consuetudinario campesino, con los códigos informales de economías ilegales, y con las normas de hecho del conflicto armado. En muchas regiones de Caldas, ignorar las normas informales que rigen la conducta real de las partes produce estrategias jurídicas formalmente correctas y socialmente inaplicables.

**Proposición 4 — El tiempo del cliente no es el tiempo del proceso**
El proceso tiene su propio ritmo. El cliente tiene el suyo. Un proceso de nulidad y restablecimiento puede durar 4 años. Durante esos 4 años, el cliente tiene que seguir viviendo — y frecuentemente tiene que seguir interactuando con la contraparte, dependiendo económicamente de una resolución que no llega, y sosteniendo una carga emocional que el abogado no ve. El interrogatorio debe evaluar si el cliente puede sostener el proceso en el tiempo que va a tomar.

---

## ARQUITECTURA DE LA BIBLIOTECA

### Capas del interrogatorio

Esta biblioteca está organizada en seis capas que se ejecutan en secuencia, no en paralelo:

```
CAPA 0 — META-INTERROGATORIO
¿Está el cliente en condiciones de ser interrogado?
¿Qué factores distorsionan la comunicación en esta entrevista?

CAPA 1 — OBJETIVOS REALES
¿Qué quiere realmente el cliente?
¿Puede sostener el proceso que lo llevaría a ese objetivo?

CAPA 2 — HECHOS Y SU DIMENSIÓN PARALELA
Los hechos del caso y las dimensiones ocultas que no se narran voluntariamente.

CAPA 3 — TERRENO ECONÓMICO
El paisaje económico del caso más allá de la cuantía declarada.

CAPA 4 — DIMENSIONES PARALELAS DEL ORDENAMIENTO
Penal, disciplinaria, internacional, consuetudinaria.

CAPA 5 — PREGUNTAS ESPECÍFICAS POR TIPO DE CASO
El banco técnico por área del derecho.

CAPA 6 — CONOCIMIENTO TÁCITO DEL ABOGADO ACTIVO
El protocolo para capturar y registrar lo que el abogado activo sabe y el sistema no puede generar.
```

### Taxonomía de preguntas

```
[A] ACTIVADORA — revela protección constitucional especial
[B] RUPTURA — rompe omisión voluntaria o involuntaria
[C] RIESGO — revela vulnerabilidad propia del cliente
[D] CUANTIFICADORA — establece cifras, fechas y magnitudes procesales
[E] JURISDICCIONAL 🧭 — depende del circuito y contraparte específica
[F] TÁCITA — viene de la experiencia acumulada del abogado activo, no del sistema
[G] ECONÓMICA — mapea el terreno económico del caso
[H] PARALELA — activa dimensión penal, disciplinaria o internacional
[I] TOLERANCIA — evalúa si el cliente puede sostener el proceso
[J] OBJETIVO — revela lo que el cliente realmente quiere vs. lo que dice
[K] SEMIÓTICA — guía de observación, no pregunta directa
```

---

## CAPA 0 — META-INTERROGATORIO

*Antes de hacer una sola pregunta sobre el caso, evaluar si las condiciones de la entrevista permiten obtener información confiable.*

*Fundamento: la psicología del testimonio (Loftus, 1979; Wells y Olson, 2003) ha demostrado que el trauma, el miedo, la vergüenza y la presión distorsionan el recuerdo y la comunicación de forma sistemática y predecible. Un abogado que ignora el estado del cliente en la entrevista recibe información menos confiable que uno que lo evalúa.*

---

**META-01** [K] — EVALUACIÓN DEL ESTADO DEL CLIENTE
*No es una pregunta — es una guía de observación antes de comenzar*

¿El cliente llegó acompañado? ¿Quién lo acompaña y qué rol juega esa persona?
*Si llegó con alguien que habla por él: ¿es representante legítimo o es quien controla la narrativa?*

¿El cliente llora, tiembla, o muestra señales físicas de angustia?
*Si sí: el interrogatorio directo produce omisiones y distorsiones. Primero estabilizar emocionalmente.*

¿El cliente muestra señales de haber preparado un guión?
*Respuestas muy pulidas, sin vacilaciones, con fechas exactas memorizadas pueden indicar narrativa construida, no memoria espontánea. Requiere preguntas laterales para verificar.*

¿El cliente evita mirar a los ojos cuando habla de ciertos hechos específicos?
*La comunicación no verbal de incomodidad con temas específicos señala los puntos donde la omisión estratégica es más probable.*

¿El cliente minimiza consistentemente la gravedad de lo que le ocurrió?
*Normalización del daño, especialmente en casos de violencia, acoso, o discriminación. Puede indicar trauma no procesado o miedo a la reacción del abogado.*

**Decisión post-evaluación:**
Si el cliente está en crisis emocional severa → No iniciar el interrogatorio jurídico. Primero acompañar emocionalmente y reagendar.
Si el cliente llegó con alguien que controla la narrativa → Solicitar reunión individual antes de continuar.
Si el cliente muestra narrativa excesivamente preparada → Comenzar por preguntas periféricas antes de ir al núcleo.
Si el estado es adecuado → Continuar a Meta-02.

---

**META-02** [K] — IDENTIFICACIÓN DEL CLIENTE REAL
*Antes de preguntar sobre el caso, establecer quién toma realmente las decisiones*

Para el cliente: *"¿Viene usted en nombre propio, o viene representando a alguien más — su familia, su comunidad, su empresa?"*
Razón: En Colombia, especialmente en casos familiares, comunitarios y empresariales, la persona que se sienta frente al abogado frecuentemente no es quien tomará las decisiones sobre el proceso. El "cliente real" puede ser la familia reunida en asamblea, el consejo de la comunidad indígena, o el socio mayoritario que nunca aparece. Diseñar la estrategia sin saber quién toma las decisiones es diseñarla para el mensajero.

Para el cliente: *"¿Hay alguien más que deba estar de acuerdo con lo que usted y yo decidamos aquí?"*
Razón: Detecta veto players — personas que pueden bloquear la estrategia aunque no estén presentes en la reunión. Un cónyuge que no quiere litigar, un hermano que tiene una versión diferente de los hechos, un socio con intereses opuestos.

---

**META-03** [K] — CALIDAD DE LA MEMORIA
Para el cliente: *"¿Esto que me está contando lo recuerda muy bien, o hay partes que no recuerda con claridad?"*
Razón: La metacognición sobre la propia memoria es un indicador útil de la confiabilidad del relato. Un cliente que reconoce sus lagunas es epistemológicamente más confiable que uno que afirma recordar todo con precisión perfecta. Además, identificar las lagunas de memoria desde el inicio permite saber dónde hay que buscar documentos o testigos para reconstruir lo que el cliente no recuerda.

---

## CAPA 1 — OBJETIVOS REALES DEL CLIENTE

*Fundamento: la teoría de la decisión racional aplicada al derecho (Posner, 1973) predice que el litigante elige estrategias que maximizan su utilidad esperada. Pero la utilidad del cliente no siempre es lo que el abogado asume. Si el abogado maximiza la probabilidad de un resultado que el cliente no quería realmente, el proceso fue exitoso y el cliente está insatisfecho.*

---

**OBJ-01** [J] [🔑]
Para el cliente: *"Si al final de este proceso pasa exactamente lo mejor que puede pasar — ¿qué pasa? ¿Cómo queda su vida?"*
Razón: Esta pregunta obliga al cliente a articular su objetivo real en términos concretos, no en términos jurídicos. "Que me paguen" no es un objetivo real — es un mecanismo. "Poder pagar la escuela de mis hijos sin pedir prestado" es el objetivo real. "Que reconozcan que me trataron injustamente" es un objetivo que el proceso ejecutivo no satisface, pero que una disculpa formal sí. Esta pregunta revela si la estrategia jurídica óptima y el objetivo real del cliente son compatibles.

---

**OBJ-02** [J]
Para el cliente: *"¿Hay algo que para usted sería peor que no ganar el caso?"*
Razón: Identifica los límites del cliente — lo que no está dispuesto a sacrificar en el proceso. Algunos clientes no pueden permitirse que el proceso se haga público porque afecta su reputación en la comunidad. Otros no pueden permitirse perder la relación con la contraparte (el familiar, el vecino, el cliente comercial). Otros no pueden permitirse un proceso largo porque necesitan el dinero urgente. Sin saber esto, el abogado puede recomendar una estrategia que gana el caso y destruye algo más valioso para el cliente.

---

**OBJ-03** [J] [🔑]
Para el cliente: *"Si la otra parte le propusiera arreglar esto hoy mismo, sin proceso, ¿qué le tendría que ofrecer para que usted dijera sí?"*
Razón: Esta pregunta revela el BATNA (Best Alternative to a Negotiated Agreement) del cliente con más precisión que cualquier análisis jurídico. Si el cliente dice un número o una condición que es razonablemente alcanzable sin litigio, la estrategia óptima puede ser la negociación, no el proceso. Si el cliente dice algo inalcanzable o dice "no hay ningún arreglo posible", revela que el objetivo real no es el resultado sino el proceso mismo (vindication, venganza, reconocimiento).

---

**OBJ-04** [I] [🔑]
Para el cliente: *"¿Cuánto tiempo puede usted aguantar esta situación sin que se resuelva? ¿Hay alguna fecha límite — económica, personal, de salud — más allá de la cual necesita que esto esté resuelto?"*
Razón: La tolerancia temporal del cliente es un factor estratégico de primer orden que el análisis jurídico puro ignora. Un proceso de nulidad y restablecimiento puede durar 4 años. Si el cliente no puede aguantar más de 6 meses sin ingresos, esa no es la estrategia correcta aunque tenga 80% de probabilidad de éxito. La evaluación de la tolerancia temporal define qué estrategia es realmente viable para este cliente específico.

---

**OBJ-05** [I]
Para el cliente: *"¿Tiene que seguir interactuando con la persona o entidad contra quien va a actuar — tiene que seguir siendo su paciente, su empleado, su vecino, su proveedor?"*
Razón: La continuidad de la relación con la contraparte durante el proceso es uno de los factores de riesgo más subestimados en el diseño de estrategias. Un empleado que litiga a su empleador y sigue trabajando allí durante el proceso está expuesto a represalias sutiles que pueden destruir el caso y su situación laboral simultáneamente. Una comunidad que litiga a una empresa que opera en su territorio y de la que depende económicamente enfrenta presiones que el análisis jurídico no captura.

---

**OBJ-06** [I]
Para el cliente: *"¿Tiene usted los recursos — tiempo, dinero, energía emocional — para acompañar este proceso durante el tiempo que puede tomar?"*
Razón: El acceso real a la justicia no es solo un problema jurídico — es un problema de recursos. Un cliente sin recursos para desplazarse a audiencias en la ciudad, sin tiempo libre de trabajo para atender el proceso, o sin estabilidad emocional para sostener la incertidumbre prolongada, abandonará el proceso antes de que termine. Saberlo desde el inicio permite diseñar una estrategia que el cliente pueda realmente sostener.

---

## CAPA 2 — HECHOS Y SUS DIMENSIONES OCULTAS

*Las preguntas de esta capa no buscan los hechos que el cliente narró — buscan los hechos que el cliente no narró.*

---

**HEC-01** [B] [⚡] [🔑]
Para el cliente: *"Antes de que me cuente los detalles, dígame: ¿hay alguna parte de esta historia que usted nunca le ha contado a nadie, porque le da vergüenza, porque le parece que lo pone a usted en mal lugar, o porque cree que nadie le va a creer?"*
Razón: Esta es la versión más poderosa de la pregunta trampa, y debe hacerse PRIMERO, no último. Si se hace al final, el cliente ya construyó su narrativa y la pregunta trampa tiene que trabajar contra esa inercia. Si se hace al principio, el cliente no ha consolidado aún qué revelar y qué ocultar — la ventana está más abierta.

---

**HEC-02** [B]
Para el cliente: *"¿Hay alguien que sepa lo que le pasó — un familiar, un amigo, un vecino, un compañero de trabajo — y que tenga una versión diferente de lo que usted me está contando?"*
Razón: Las versiones alternativas de los hechos del caso, especialmente las de personas cercanas al cliente, son el territorio donde la contraparte va a buscar prueba. Identificarlas desde el inicio permite anticiparlas o incorporarlas productivamente al análisis. Un testigo que tiene una versión diferente no es necesariamente un testigo hostil — puede ser un testigo que conoce hechos que el cliente no mencionó.

---

**HEC-03** [C] [🔑]
Para el cliente: *"¿Hubo algo que usted hizo o dejó de hacer que pudo haber contribuido a que llegaran a esta situación?"*
Razón: La responsabilidad concurrente del cliente es el argumento defensivo más frecuente de la contraparte y el más devastador cuando aparece por sorpresa en el proceso. Esta pregunta no busca culpar al cliente — busca que el abogado sepa antes que la contraparte cuáles son las vulnerabilidades propias del caso. Lo que se sabe antes puede manejarse; lo que aparece en el proceso sin anticipación destruye la credibilidad.

---

**HEC-04** [B] [🔑]
Para el cliente: *"¿En algún momento usted firmó algo — cualquier documento, aunque no supiera bien qué era — relacionado con esta situación?"*
Razón: Los documentos firmados sin comprensión completa son la fuente más frecuente de sorpresas procesales. Paz y salvos en despidos laborales, autorizaciones en procesos médicos, actas de recibo en contratos estatales, renuncias de derechos en acuerdos privados. El cliente frecuentemente no los menciona porque no sabe que son relevantes o porque no quiere que el abogado piense que fue descuidado. Conocerlos desde el inicio define si hay que atacar esos documentos o trabajar con ellos.

---

**HEC-05** [H] [🔑]
Para el cliente: *"¿Lo que le pasó podría ser también un delito — algo que otra persona le hizo que en su opinión debería estar penado por la ley?"*
Razón: En Colombia, muchas situaciones tienen simultáneamente una dimensión civil/administrativa y una penal. Un despido discriminatorio puede ser también una conducta penal. Una negativa de EPS que produce una lesión grave puede activar responsabilidad penal médica. Un acto administrativo ilegal puede ser un delito de prevaricato o de contrato sin cumplimiento de requisitos legales. La denuncia penal no es siempre la estrategia principal, pero puede ser la palanca que cambia el comportamiento de la contraparte.

---

**HEC-06** [H]
Para el cliente: *"¿Ha habido amenazas — directas o indirectas — relacionadas con este caso? ¿Alguien le ha dicho que no demande, que retire la queja, o que guarde silencio?"*
Razón: En Colombia, las amenazas contra personas que ejercen derechos pueden activar mecanismos específicos: tutela por amenaza al derecho a la vida y la integridad, medidas de protección de la UNP (Unidad Nacional de Protección), y mecanismos internacionales de protección a defensores de derechos humanos. Además, las amenazas son evidencia de que la contraparte tiene algo que ocultar y que el caso tiene más peso del que parece.

---

**HEC-07** [H] [🔑]
Para el cliente: *"¿Este problema que usted tiene tiene alguna relación con el conflicto armado — con desplazamiento, con grupos armados, con la pérdida de tierras durante la violencia?"*
Razón: La Ley 1448 de 2011 (Ley de Víctimas y Restitución de Tierras) crea un sistema paralelo y especializado de reparación para víctimas del conflicto armado. Dada la historia del conflicto en Caldas y el Eje Cafetero, muchos casos que llegan a un consultorio como laborales, civiles, o administrativos tienen en su fondo una dimensión de conflicto que activa este sistema. Si no se pregunta, nunca se sabe. Si se sabe, hay todo un marco de derechos adicionales disponible.

---

## CAPA 3 — TERRENO ECONÓMICO

*Fundamento: el análisis económico del derecho (Coase, 1960; Posner, 1973) demuestra que las decisiones de litigar o no litigar son fundamentalmente decisiones económicas sobre costos, beneficios e incentivos. Un abogado que diseña estrategias sin mapear el terreno económico del caso diseña en el vacío.*

---

**ECO-01** [G] [🔑]
Para el cliente: *"¿Cuánto le está costando esta situación hoy — en dinero, en salud, en tiempo — mientras no se resuelve?"*
Razón: El costo del status quo es el costo que el cliente paga cada día que el problema no se resuelve. Si ese costo es alto, urgencia real y cualquier solución rápida vale más que una solución perfecta tardía. Si ese costo es bajo, el cliente puede darse el lujo de esperar la mejor estrategia aunque tome más tiempo. Este número define la urgencia real del caso independientemente de la urgencia procesal.

---

**ECO-02** [G] [🔑]
Para el cliente: *"¿Qué tan importante es esta situación para la otra parte — para la empresa, la entidad, o la persona contra quien va a actuar? ¿Cuánto les importa este caso?"*
Razón: El comportamiento de la contraparte en el proceso depende de cuánto le importa el resultado. Una EPS que tiene 500 tutelas similares en curso tratará este caso de forma completamente diferente a una EPS que tiene este caso como el primero de su tipo. Un empleador que tiene reputación que proteger cederá más fácilmente que uno que opera en el anonimato. Saber el peso relativo del caso para la contraparte define las tácticas de presión disponibles.

---

**ECO-03** [G]
Para el cliente: *"¿La persona o entidad contra quien va a actuar tiene problemas económicos, está en proceso de quiebra, o está en una situación financiera difícil?"*
Razón: Una sentencia favorable contra una entidad insolvente o en liquidación no tiene valor práctico. La solvencia de la contraparte es un prerequisito de la ejecutabilidad de cualquier fallo. Si la contraparte está en problemas financieros, hay que evaluar si el litigio tiene sentido o si hay que concentrarse en las medidas cautelares urgentes.

---

**ECO-04** [G] [🔑]
Para el cliente: *"Si no hace nada — si simplemente deja las cosas como están — ¿qué pasa? ¿La situación mejora sola, empeora, o se queda igual?"*
Razón: Esta pregunta evalúa el costo de no litigar, que es el benchmark real contra el que se debe comparar cualquier estrategia. Si la situación mejora sola (la EPS autorizará eventualmente, el empleador pagará por presión social, el acto administrativo expirará por sí mismo), litigar tiene un costo de oportunidad que debe considerarse. Si la situación empeora con el tiempo (prescripción, deterioro de la salud, pérdida del territorio), la urgencia se confirma.

---

**ECO-05** [G]
Para el cliente: *"¿Hay otras personas o entidades que también se vean afectadas por lo que le pasó — proveedores, clientes, socios, familiares — y que podrían tener interés en que esto se resuelva?"*
Razón: Los terceros con interés en el resultado del caso pueden ser aliados estratégicos o actores que complican el proceso. Un proveedor al que también le deben dinero puede aportar pruebas y compartir costos de un proceso ejecutivo. Un familiar que también fue afectado puede ser legitimado activo adicional que aumenta las pretensiones. Una organización que ha sufrido el mismo problema de la misma contraparte puede ser codemandante en una acción de grupo.

---

## CAPA 4 — DIMENSIONES PARALELAS DEL ORDENAMIENTO

*Colombia tiene un ordenamiento jurídico pluriestratificado. Un caso que parece puramente civil puede tener dimensiones penales, disciplinarias, constitucionales, y hasta internacionales. No explorarlas es dejar palancas sobre la mesa.*

---

### IV.A — Dimensión Penal

**PEN-01** [H] [🔑]
Para el cliente: *"¿Alguien cometió un delito en esta historia — alguien falsificó un documento, lo engañó con información falsa, lo amenazó, o se aprovechó de su cargo para perjudicarlo?"*
Razón jurídica: La denuncia penal puede ser la palanca más poderosa de un caso civil o administrativo — no porque el proceso penal resuelva el problema principal, sino porque cambia los incentivos de la contraparte. Un empleador que enfrenta simultáneamente una demanda laboral y una investigación por acoso o por utilización indebida de información cede más fácilmente. Un funcionario público que ve una denuncia disciplinaria y penal procesa el caso administrativo diferente. La denuncia penal no es siempre estrategia principal — pero ignorarla cuando aplica es perder presión disponible.

Delitos frecuentemente asociados a casos civiles/laborales/administrativos:
→ Laboral: acoso laboral como delito (Ley 1010), discriminación (Art. 137 C.P.), violación de la reserva industrial
→ Salud: abandono de paciente, omisión de agente retenedor (aportes no pagados)
→ Contratación estatal: contrato sin cumplimiento de requisitos (Art. 410 C.P.), celebración indebida de contratos (Art. 408 C.P.), interés indebido en la celebración de contratos (Art. 409 C.P.)
→ Administrativo: prevaricato por acción (Art. 413 C.P.) cuando el funcionario profirió resolución contraria a norma expresa
→ Civil: estafa (Art. 246 C.P.) en casos de fraude contractual, abuso de confianza (Art. 249 C.P.)

---

**PEN-02** [H]
Para el cliente: *"¿Usted tiene alguna investigación penal, disciplinaria, o administrativa en su contra relacionada con esta situación?"*
Razón: La existencia de un proceso en contra del cliente es la sorpresa más devastadora que puede ocurrir en un proceso iniciado por el cliente. Si el cliente demanda y simultáneamente es investigado por la misma situación, la contraparte puede usar esa investigación para cambiar el balance de poder procesal. Saberlo desde el inicio es indispensable.

---

### IV.B — Dimensión Disciplinaria

**DIS-01** [H] [🔑]
Para el cliente: *"¿El funcionario público o el profesional que le causó el daño tiene la obligación de respetar un código ético o un régimen disciplinario especial?"*
Razón jurídica: En Colombia, los servidores públicos están sujetos al Código Disciplinario Único (Ley 1952 de 2019) y los profesionales (médicos, abogados, ingenieros) a sus respectivos códigos deontológicos. La queja disciplinaria ante la Procuraduría (para servidores públicos), la Superintendencia respectiva (para profesionales regulados), o los tribunales ético-profesionales cumple dos funciones: crea un expediente formal de la conducta y cambia los incentivos del infractor. Un médico que sabe que hay una queja ante el Tribunal Ético Médico actúa diferente. Un funcionario con queja ante la Procuraduría actúa diferente.
Tiempo de respuesta disciplinaria: generalmente más rápido que el proceso principal. Puede producir resultados tangibles mientras el proceso principal avanza.

---

### IV.C — Dimensión Internacional y de Derechos Humanos

**INT-01** [H] [🔑]
Para el cliente: *"¿Lo que le pasó es parte de un patrón — hay muchas otras personas en la misma situación por las mismas causas y por el mismo actor?"*
Razón jurídica: Cuando una violación de derechos es sistemática y no individual, se activan mecanismos diferentes: la acción de grupo (Ley 472/98) para daños comunes, el estado de cosas inconstitucional (herramienta de la Corte Constitucional para problemas estructurales), y en casos de extrema gravedad, los mecanismos internacionales de la CIDH (Comisión Interamericana de Derechos Humanos) y los órganos de tratados de la ONU.
Casos que han llegado a la CIDH desde Colombia: masacres, desapariciones forzadas, violencia sistemática contra líderes sociales, desplazamiento masivo, vulneraciones del derecho a la salud con características de discriminación sistémica.
Impacto estratégico: La sola notificación a la CIDH cambia el comportamiento del Estado colombiano. No resuelve el caso individual, pero crea presión política que a veces es más efectiva que la presión judicial interna.

---

**INT-02** [H]
Para el cliente: *"¿Usted es líder social, defensor de derechos humanos, periodista, sindicalista, o tiene algún rol de representación o advocacy en su comunidad?"*
Razón: Colombia es uno de los países con más líderes sociales y defensores de derechos humanos asesinados en el mundo. Los mecanismos de protección disponibles para esta población son diferentes y más robustos: medidas cautelares de la CIDH, medidas provisionales de la Corte IDH, programas de protección de la UNP, y acompañamiento de organizaciones internacionales de protección. Si el cliente tiene este perfil y su situación tiene conexión con su actividad de defensa, el marco jurídico disponible es cualitativamente diferente.

---

### IV.D — Dimensión de Víctimas del Conflicto (Ley 1448 de 2011)

*Esta subsección es especialmente relevante en Caldas y el Eje Cafetero dado el historial del conflicto armado en la región.*

---

**VIC-01** [H] [A] [🔑]
Para el cliente: *"¿En algún momento de su vida — o de la vida de su familia — tuvieron que abandonar su casa, su tierra, o su comunidad por la violencia o porque alguien los obligó?"*
Razón jurídica: La condición de víctima del conflicto armado (Art. 3 Ley 1448/11) es una categoría jurídica con efectos sustantivos: derecho a la verdad, la justicia y la reparación; inscripción en el Registro Único de Víctimas; acceso al sistema de reparaciones administrativas; y en casos de despojo, la ruta de restitución de tierras ante los Juzgados Especializados de Restitución de Tierras. Esta condición puede coexistir con cualquier otro tipo de caso. Un cliente que fue desplazado, perdió sus tierras, y ahora enfrenta un problema laboral, tiene dos casos potenciales, no uno.

---

**VIC-02** [H]
Para el cliente: *"¿Algún familiar suyo fue asesinado, desaparecido, o herido por la violencia?"*
Razón jurídica: Los familiares de víctimas directas del conflicto armado son también víctimas con derechos propios a la reparación integral. Los perjuicios morales por la pérdida de un familiar en el conflicto son reconocidos y cuantificables jurídicamente. La Unidad para la Atención y Reparación Integral a las Víctimas (UARIV) administra las reparaciones administrativas; la JEP (Jurisdicción Especial para la Paz) tiene competencia para ciertos hechos cometidos en el marco del conflicto.

---

**VIC-03** [H] [🧭]
Para el cliente: *"¿Ha recibido alguna reparación, indemnización, o ayuda del Estado relacionada con esa situación?"*
🧭 Razón: Las reparaciones ya recibidas pueden afectar las pretensiones en otros procesos, dependiendo de la naturaleza de la reparación. Esto requiere análisis específico de los documentos de la reparación recibida.
[{abogado}: ¿Cuál es la práctica de los jueces del circuito de Caldas respecto a la concurrencia de reparaciones del sistema de víctimas con pretensiones en otros procesos?]

---

### IV.E — Dimensión del Derecho Propio y Pluralismo Jurídico

*Especialmente relevante para abogados con práctica en derecho étnico-territorial*

**PLU-01** [H] [🔑]
Para el cliente: *"¿Este problema fue discutido o intentó resolverse dentro de la propia comunidad — con el cabildo, con las autoridades propias, con los mayores — antes de venir aquí?"*
Razón jurídica: Las comunidades indígenas y afrodescendientes con reconocimiento oficial tienen jurisdicción especial propia (Art. 246 C.P.). Un conflicto que fue conocido y decidido por la autoridad indígena competente puede tener efectos de cosa juzgada para el sistema formal, o puede requerir coordinación entre los dos sistemas. Además, acudir al sistema formal sin agotar el mecanismo propio puede generar tensiones dentro de la comunidad que complican el caso.

---

**PLU-02** [H]
Para el cliente: *"¿Hay normas propias de su comunidad, acuerdos o costumbres que gobiernen esta situación y que sean diferentes de lo que dice la ley del Estado?"*
Razón jurídica: El pluralismo jurídico real en Colombia implica que en muchos territorios coexisten el derecho estatal, el derecho consuetudinario indígena o afrodescendiente, y en algunas zonas, normas impuestas por actores ilegales. Ignorar las normas no estatales en el diseño de una estrategia produce estrategias formalmente correctas que son socialmente inaplicables o que generan conflictos adicionales dentro de la comunidad. El abogado que solo conoce el derecho formal no tiene mapa completo del terreno.

---

## CAPA 5 — PREGUNTAS TÉCNICAS POR TIPO DE CASO

---

## SECCIÓN I — TUTELA

### I.1 — TUTELA DE SALUD

**T-S-01** [A] [🔑]
Para el cliente: *"¿Cuántos años tiene usted — o la persona a quien cuida? ¿Tiene alguna discapacidad reconocida o en proceso de reconocimiento?"*
Razón jurídica: La edad activa sujeto de especial protección (adulto mayor > 60, menor de edad). La discapacidad activa la Convención de Derechos de Personas con Discapacidad (bloque de constitucionalidad) y la Ley 1618/13. Ambas categorías elevan el estándar de protección y eliminan el debate sobre subsidiariedad con mayor facilidad.
🟡 Referencia jurisprudencial a verificar: SU-677/17 y línea de tutelas de salud por sujetos de especial protección.

---

**T-S-02** [B] [🔑]
Para el cliente: *"¿El médico que lo atiende trabaja para su EPS o es médico particular?"*
Razón jurídica: La prescripción de médico no adscrito a la EPS no genera automáticamente la obligación de la EPS. La Corte ha establecido matices importantes: si el médico de la EPS no prescribió porque no existe en la red de la EPS, la obligación sí surge. Si el cliente prefirió médico particular sin intentar acceder al médico de la EPS, la situación es diferente. Esta distinción define completamente la argumentación.

---

**T-S-03** [D] [🔑]
Para el cliente: *"¿Cuándo exactamente le negaron el servicio o medicamento? ¿Se lo dijeron por escrito o fue verbal?"*
Razón: Inmediatez + construcción del expediente de la negativa. Si fue verbal, hay que crear el expediente ahora con derecho de petición. Si fue escrita, el documento es la prueba central.

---

**T-S-04** [B] [⚡]
Para el cliente: *"¿Fue a la EPS, llamó, o usó la app para pedir el servicio antes de venir aquí? ¿Qué le dijeron exactamente?"*
Razón: Distingue quién negó (EPS o IPS o médico de guardia sin autoridad decisoria) y construye el expediente de agotamiento interno. Fundamental para el análisis de subsidiariedad.

---

**T-S-05** [A] [🔑]
Para el cliente: *"¿Usted o la persona que cuida tiene una condición que se está empeorando — que con el paso de los días o semanas el daño es mayor o irreversible?"*
Razón: La urgencia de daño inminente o irreversible activa la solicitud de medida provisional (Art. 7 D. 2591/91) y elimina el debate sobre subsidiariedad con mayor contundencia. Es el argumento más poderoso de la tutela de salud.

---

**T-S-06** [B]
Para el cliente: *"¿Conoce a otras personas en su misma EPS con el mismo problema?"*
Razón: Activa la posibilidad de efectos inter comunis o de acción de grupo. Cambia el alcance potencial del caso.

---

**T-S-07** [C]
Para el cliente: *"¿Hay algo en sus hábitos o en su trabajo que su médico le haya dicho que está relacionado con su enfermedad?"*
Razón: Anticipa el argumento de la EPS de exclusión por origen laboral o por conducta del afiliado.

---

**T-S-08** [E] [🧭]
Para el cliente: *"¿Cuál es exactamente su EPS?"*
🧭 [{abogado}: En el circuito de Caldas, ¿cuáles EPS son conocidas por incumplir fallos? ¿Cuáles tienen litigantes recurrentes con argumentos defensivos predecibles? ¿Hay jueces que tienen posiciones conocidas sobre determinadas EPSs?]

---

**T-S-09** [H]
Para el cliente: *"¿La negativa de la EPS le ha causado un daño que ya ocurrió — una lesión, un deterioro que ya pasó, que no se puede deshacer?"*
Razón: Si ya hay daño consumado, puede haber tanto tutela (para el servicio futuro) como reparación directa o proceso de responsabilidad civil médica (por el daño ya causado). Dos casos, no uno.

---

**T-S-10** [F]
[{abogado}: PROTOCOLO DE CAPTURA — responder]
Caso de tutela de salud que perdiste o que casi pierdes por una pregunta que no hiciste:
→ ¿Qué tipo de caso era?
→ ¿Qué información faltó?
→ ¿Cuál habría sido la pregunta que la habría revelado?
→ ¿Cómo se la harías al cliente la próxima vez?

---

### I.2 — TUTELA DE OTROS DERECHOS FUNDAMENTALES

**T-O-01** [A] [🔑]
Para el cliente: *"¿Usted o alguien que depende de usted vive de lo que le están negando — si no se resuelve esto, no pueden comer, pagar arriendo, o cubrir lo básico?"*
Razón: Activa el mínimo vital como derecho fundamental independiente, lo que puede hacer procedente la tutela incluso cuando el derecho principal es patrimonial.

---

**T-O-02** [D]
Para el cliente: *"¿Cuánto tiempo lleva en esta situación sin que nadie le resuelva el problema?"*
Razón: Define el argumento de inmediatez en ambas direcciones: si es muy reciente, hay urgencia. Si lleva mucho tiempo, hay que justificar la demora o argumentar la vulneración continuada.

---

**T-O-03** [B]
Para el cliente: *"¿Intentó resolverlo por otra vía antes de venir aquí?"*
Razón: Construye el argumento de subsidiariedad (los otros mecanismos fallaron o son inidóneos).

---

**T-O-04** [H] [🔑]
Para el cliente: *"¿Lo que le están haciendo lo hacen también con otras personas en la misma situación que usted?"*
Razón: Si hay patrón sistemático, puede configurarse estado de cosas inconstitucional o efectos inter comunis de la tutela. Cambia completamente el alcance del caso.

---

## SECCIÓN II — LABORAL

### II.1 — DESPIDO

**L-D-01** [A] [🔑]
Para el cliente: *"¿Cuánto tiempo le falta para pensionarse?"*
Razón: Fuero de prepensionado (< 3 años). Cambia de indemnización a reintegro. El caso más valioso cambia completamente de naturaleza.
🟡 SU-049/17 — verificar vigencia y precisión del M.P.

---

**L-D-02** [A] [🔑]
Para el cliente: *"¿Es miembro de un sindicato o de una organización de trabajadores?"*
Razón: Fuero sindical (Art. 405 C.S.T.) — sin desafuero previo, el despido es ineficaz independientemente de la causa.

---

**L-D-03** [A] [🔑]
Para el cliente: *"Cuando la despidieron, ¿estaba de incapacidad médica, embarazada, o en licencia de maternidad o paternidad?"*
Razón: Múltiples fueros de protección constitucional reforzada. Despido ineficaz de pleno derecho en varios supuestos. La Corte ha establecido presunción de discriminación que invierte la carga de la prueba.

---

**L-D-04** [A]
Para el cliente: *"¿Tiene usted alguna discapacidad o enfermedad crónica que su empleador conocía?"*
Razón: Art. 26 Ley 361/97 — protección reforzada para personas en situación de discapacidad. Requería autorización del Ministerio del Trabajo para el despido.

---

**L-D-05** [B] [⚡] [🔑]
Para el cliente: *"El día que la despidieron o después, ¿firmó algún documento? ¿Le explicaron qué era antes de firmar?"*
Razón: Paz y salvos, actas de terminación por mutuo acuerdo, liquidaciones con renuncias. Vicio del consentimiento atacable si firmó bajo presión o sin comprensión. Conocerlo primero es crítico.

---

**L-D-06** [B] [🔑]
Para el cliente: *"¿Tiene mensajes de WhatsApp, correos, o cualquier comunicación escrita del jefe o de Recursos Humanos sobre su despido o sobre problemas previos?"*
Razón: Las comunicaciones informales son frecuentemente la mejor prueba de la causa real del despido cuando difiere de la causa declarada. Los clientes no asocian sus chats con evidencia jurídica.

---

**L-D-07** [C] [⚡]
Para el cliente: *"¿Hubo algo que usted hizo — una queja, un reclamo, algo que haya dicho — que cree que molestó al empleador antes del despido?"*
Razón: Identifica si el despido fue represalia por ejercicio de un derecho protegido (queja ante Mintrabajo, denuncia de accidente, afiliación a sindicato). La represalia por ejercicio de derecho tiene protección constitucional adicional.

---

**L-D-08** [D]
Para el cliente: *"¿Cuánto ganaba exactamente — sueldo básico más todo lo demás — en el último año?"*
Razón: La liquidación de la indemnización incluye componentes que el trabajador no contabiliza: bonificaciones habituales, horas extras, viáticos permanentes. La subestimación reduce las pretensiones desde el inicio.

---

**L-D-09** [D] [🔑]
Para el cliente: *"¿Puede consultar su historia laboral en Colpensiones o en su fondo de pensiones? ¿Sabe si le pagaron los aportes durante todo el tiempo que trabajó?"*
Razón: La historia laboral de Colpensiones es la prueba más objetiva del tiempo real de la relación laboral y de si se pagaron los aportes. Gratuita, objetiva, y muchos clientes no saben que existe.

---

**L-D-10** [I] [🔑]
Para el cliente: *"¿Tiene que pedir referencia laboral a ese empleador para conseguir trabajo? ¿Necesita de alguna forma seguir teniendo buenas relaciones con ellos?"*
Razón: La continuidad de la dependencia del cliente del empleador define las tácticas disponibles. Un proceso muy agresivo puede ser contraproducente si el cliente necesita esa referencia para su próximo trabajo.

---

**L-D-11** [H] [🔑]
Para el cliente: *"¿Cree usted que la razón real por la que la despidieron fue algo diferente a lo que le dijeron formalmente — discriminación, represalia, o algo que no se atreverían a decir abiertamente?"*
Razón: La causa real del despido puede ser discriminación por género, raza, orientación sexual, opinión política, o condición de salud — todas causas con protección constitucional reforzada. Si el cliente lo sospecha, hay que investigarlo antes de construir la estrategia.

---

**L-D-12** [F]
[{abogado}: PROTOCOLO DE CAPTURA — responder]
Caso laboral donde la pregunta que faltó cambió el resultado:
→ ¿Qué no preguntaste?
→ ¿Qué habría cambiado si lo hubieras sabido desde el principio?
→ ¿Cuál es la pregunta que harías ahora?

---

### II.2 — ACOSO LABORAL

**L-A-01** [D] [🔑]
Para el cliente: *"¿Tiene registro — fechas, descripción de lo que pasó, quién estaba presente — de los episodios de acoso?"*
Razón: La Ley 1010 exige que el acoso sea repetido y sistemático. Sin cronología documentada, el caso es extremadamente difícil de probar. El registro cronológico, aunque sea en el teléfono, es la base de la prueba.

---

**L-A-02** [B]
Para el cliente: *"¿Hay compañeros que hayan visto lo que pasó y que estén dispuestos a declararlo?"*
Razón: Los testigos-compañeros son la prueba más directa pero también la más difícil de conseguir porque temen represalias. Identificarlos y evaluar su disposición desde el principio define la estrategia probatoria.

---

**L-A-03** [B] [🔑]
Para el cliente: *"¿Interpuso queja ante el Comité de Convivencia Laboral de la empresa?"*
Razón: El Comité (Resolución 652 de 2012 del Mintrabajo) es el mecanismo interno obligatorio. Su ausencia puede ser usada para argumentar que no se agotó el mecanismo previo. Si ya se interpuso, ese expediente es prueba central.

---

**L-A-04** [C] [⚡]
Para el cliente: *"¿Hay algún conflicto personal — no laboral — entre usted y la persona que dice que la acosa?"*
Razón: La existencia de conflicto personal previo es el argumento defensivo más frecuente del acosador: "no es acoso, es un conflicto entre iguales". Conocerlo antes permite construir la distinción entre conflicto personal y acoso laboral.

---

**L-A-05** [I]
Para el cliente: *"¿Sigue trabajando en el mismo lugar? ¿Tiene que ver a esa persona todos los días?"*
Razón: Si el cliente sigue expuesto al acosador durante el proceso, la primera acción puede ser una medida de protección o una reubicación urgente, no el proceso de acoso laboral propiamente dicho.

---

### II.3 — INCUMPLIMIENTO DE PRESTACIONES

**L-P-01** [D]
Para el cliente: *"¿Tiene los desprendibles de nómina de los últimos años?"*
Razón: Prueba documental central del pago o no pago de prestaciones. Sin ellos, el cálculo es estimativo.

---

**L-P-02** [D] [🔑]
Para el cliente: *"¿Cuánto tiempo lleva sin que le paguen? ¿La empresa tiene dificultades económicas que todos saben?"*
Razón: Si la empresa está en dificultades, hay riesgo de insolvencia. Las medidas cautelares sobre bienes de la empresa deben solicitarse urgentemente antes de que desaparezcan los activos. El caso cambia de laboral a concursal potencialmente.

---

**L-P-03** [H]
Para el cliente: *"¿Hay otros compañeros en la misma situación — que también les deben prestaciones?"*
Razón: Si hay múltiples trabajadores afectados por el mismo empleador, puede haber demanda colectiva, acción de grupo, o presión sindical más efectiva que el proceso individual.

---

## SECCIÓN III — DERECHO ADMINISTRATIVO

### III.1 — NULIDAD Y RESTABLECIMIENTO

**A-N-01** [D] [🔑]
Para el cliente: *"¿Cuándo exactamente le notificaron la decisión? ¿Le entregaron algo por escrito — un papel, una carta, una resolución?"*
Razón: Caducidad de 4 meses desde notificación del acto en firme (Art. 164 CPACA). La notificación incorrecta puede significar que la caducidad no ha comenzado. Este es frecuentemente el punto más importante del caso.

---

**A-N-02** [D] [🔑]
Para el cliente: *"¿Interpuso algún recurso — una carta, una solicitud — después de recibir la decisión? ¿La entidad le respondió?"*
Razón: El agotamiento de la vía gubernativa es requisito de procedibilidad. Si no se agotó y aplica, el sistema debe generar el recurso, no la demanda. Si se agotó, la caducidad se suspendió durante el trámite.

---

**A-N-03** [D]
Para el cliente: *"¿Cuánto dinero exactamente perdió por culpa de esa decisión? ¿Puede demostrarlo con documentos?"*
Razón: La cuantificación y acreditación del daño define las pretensiones de restablecimiento. Sin cuantificación, las pretensiones patrimoniales son especulativas.

---

**A-N-04** [C] [⚡]
Para el cliente: *"¿Cumplía usted con todos los requisitos que la ley exigía para recibir lo que le negaron?"*
Razón: Si el cliente no cumplía todos los requisitos, el acto administrativo puede haber sido legal aunque incómodo. Saberlo antes evita construir un caso sobre una premisa falsa.

---

**A-N-05** [H] [🔑]
Para el cliente: *"¿Tiene usted información de que otros en la misma situación recibieron una decisión diferente — que a otros sí les concedieron lo que a usted les negaron?"*
Razón: La diferencia de trato en situaciones análogas activa el principio de igualdad (Art. 13 C.P.) y puede configurar un acto discriminatorio con protección constitucional adicional y mayor carga argumentativa para la entidad.

---

**A-N-06** [E] [🧭]
Para el cliente: *"¿Sabe exactamente cuál es la entidad que tomó la decisión — su nombre legal completo?"*
🧭 [{abogado}: ¿Hay entidades del orden departamental o municipal en Caldas que hayan sido reestructuradas o fusionadas recientemente que generen confusión sobre el demandado correcto en acciones contencioso-administrativas?]

---

### III.2 — REPARACIÓN DIRECTA

**A-R-01** [D] [🔑]
Para el cliente: *"¿Cuándo exactamente ocurrió el hecho que le causó el daño — o cuándo se enteró de que el daño vino de ese hecho?"*
Razón: Caducidad de 2 años desde el hecho o desde el conocimiento del daño y su origen. En daños diferidos (enfermedades, perjuicios que se manifiestan tiempo después), la caducidad puede ser más favorable de lo que parece.

---

**A-R-02** [A] [🔑]
Para el cliente: *"¿El daño lo sufrió usted directamente, o también lo sufrieron miembros de su familia?"*
Razón: La tipología de perjuicios del Consejo de Estado (daño emergente, lucro cesante, perjuicios morales, daño a la salud, daños convencionales y relacionales) aplica por separado para cada afectado. Los familiares son legitimados activos adicionales que multiplican las pretensiones.

---

**A-R-03** [C]
Para el cliente: *"¿Usted estaba haciendo algo riesgoso o que podría haber contribuido al hecho que le causó el daño?"*
Razón: Culpa exclusiva de la víctima o culpa concurrente son causales de exoneración o reducción. Anticiparlas permite construir la respuesta defensiva desde el inicio.

---

**A-R-04** [D]
Para el cliente: *"¿Qué pruebas tiene del daño — facturas médicas, informes, registros, fotos, lo que sea?"*
Razón: El daño en la reparación directa debe estar acreditado documentalmente. Sin prueba del daño, las pretensiones son teóricas.

---

**A-R-05** [H] [🔑]
Para el cliente: *"¿Hay otras personas que sufrieron el mismo daño por el mismo hecho del Estado?"*
Razón: Si hay múltiples víctimas del mismo hecho estatal, puede haber acción de grupo (Ley 472/98) más efectiva que múltiples acciones individuales, especialmente si el daño fue un accidente, una falla de servicio en salud, o un error en operativo policial o militar.

---

## SECCIÓN IV — PROCESO EJECUTIVO

**E-01** [D] [🔑]
Para el cliente: *"¿Tiene el documento original de la deuda — el pagaré, la factura, la sentencia — con la firma del deudor?"*
Razón: El título ejecutivo debe cumplir los tres requisitos (claro, expreso, exigible). Sin el original, el proceso no procede.

---

**E-02** [D]
Para el cliente: *"¿Hay pagos parciales que el deudor haya hecho desde que dejó de pagar? ¿Tiene registro de esos pagos?"*
Razón: Reducen la cuantía pero también constituyen reconocimiento implícito de la deuda. Relevante para eliminar el argumento de inexistencia.

---

**E-03** [C] [🔑]
Para el cliente: *"¿Hay alguna razón por la que el deudor podría argumentar que no debe — un incumplimiento suyo, un bien que no le entregó en buen estado, un servicio que no prestó correctamente?"*
Razón: Las excepciones de mérito del deudor (pago, compensación, prescripción, inexistencia, nulidad) son más fáciles de anticipar y desvirtuar cuando se conocen desde el inicio.

---

**E-04** [G] [🔑]
Para el cliente: *"¿Sabe si el deudor tiene bienes — propiedades, vehículos, cuentas — que pueda embargar? ¿Sabe si está en dificultades financieras?"*
Razón: La ejecutabilidad del proceso depende de que haya bienes para embargar. Un fallo favorable contra un deudor insolvente no tiene valor práctico.

---

**E-05** [H]
Para el cliente: *"¿Sabe si el deudor tiene otras deudas con otros acreedores — si hay más gente buscando cobrarle?"*
Razón: Si hay múltiples acreedores, puede haber proceso de insolvencia en curso (Ley 1116/06) que cambia completamente la jurisdicción y el proceso. El primero en embargar puede ser el primero en cobrar — la urgencia de las medidas cautelares depende de esta información.

---

## SECCIÓN V — FAMILIA

### V.1 — DIVORCIO Y SEPARACIÓN

**F-D-01** [A] [🔑]
Para el cliente: *"Durante su matrimonio o relación, ¿su pareja la golpeó, la amenazó, o la hizo sentir miedo de alguna forma — aunque fuera una sola vez?"*
Razón: La violencia intrafamiliar cambia la ruta completamente. Primero: medidas de protección urgentes ante Comisaría de Familia (Ley 294/96 / Ley 1257/08). Segundo: puede generar proceso penal paralelo. Tercero: causal de divorcio con efectos en la liquidación de la sociedad conyugal. La normalización de la violencia por parte del cliente es frecuente — hay que preguntar directamente y con claridad.

---

**F-D-02** [B] [⚡] [🔑]
Para el cliente: *"¿Hay bienes — propiedades, negocios, dinero — que estén a nombre de otra persona pero que en realidad sean de su pareja o de los dos?"*
Razón: La simulación de titularidad para evadir la liquidación de la sociedad conyugal es una práctica documentada. Los bienes fraudulentamente traspasados pueden ser incluidos mediante acción de simulación. Hay que identificarlos antes de que desaparezcan durante el proceso.

---

**F-D-03** [A] [🔑]
Para el cliente: *"¿Tienen hijos? ¿Cuántos años tienen? ¿Con quién viven ahora? ¿Han expresado con quién quieren vivir?"*
Razón: El interés superior del menor (Art. 44 C.P. / Ley 1098/06) es el eje del proceso cuando hay hijos. La preferencia del menor expresada con edad y madurez suficiente (generalmente > 7 años) es un elemento que el juez considera. El entorno de cuidado de cada progenitor define la estrategia de custodia.

---

**F-D-04** [C]
Para el cliente: *"¿Hay deudas grandes — créditos, hipotecas, préstamos — que usted o su pareja adquirieron juntos durante la relación?"*
Razón: Los pasivos de la sociedad conyugal se liquidan junto con los activos. Omitirlos produce una liquidación incompleta que puede generar reclamaciones posteriores de acreedores contra ambos cónyuges.

---

**F-D-05** [I] [🔑]
Para el cliente: *"¿Puede mantenerse económicamente durante el tiempo que dure el proceso de divorcio — que puede tomar entre 1 y 3 años?"*
Razón: Si la dependencia económica del cliente del cónyuge es total, la primera acción puede ser una cuota alimentaria provisional, no el proceso de divorcio. El orden de las acciones depende de la urgencia económica del cliente.

---

**F-D-06** [H]
Para el cliente: *"¿La violencia que sufrió fue conocida por alguien — un médico, un familiar, un vecino, alguien que la vio?"*
Razón: Los testigos de la violencia y los registros médicos de lesiones son la prueba más sólida en los casos de violencia intrafamiliar. Identificarlos desde el inicio define la estrategia probatoria.

---

### V.2 — ALIMENTOS

**F-A-01** [D] [🔑]
Para el cliente: *"¿Cuánto gana la persona a quien le va a pedir alimentos? ¿Tiene trabajo, negocio, propiedades?"*
Razón: La cuota alimentaria se fija según la capacidad del alimentante (Art. 413 C.C.). La prueba de la capacidad económica del alimentante es el reto central del proceso — frecuentemente la oculta. Mecanismos de investigación disponibles: RUNT (vehículos), catastro (inmuebles), RUES (empresas), extracto de aportes a seguridad social (ingresos declarados).

---

**F-A-02** [I]
Para el cliente: *"¿El alimentante sabe que usted va a pedir la cuota? ¿Cómo cree que va a reaccionar?"*
Razón: Si el alimentante va a ocultar activos o ingresos en cuanto se entere de la acción, las medidas cautelares sobre sus bienes deben solicitarse de forma urgente antes de notificarle. El orden de las actuaciones depende de esta información.

---

## SECCIÓN VI — SUCESIÓN

**S-01** [B] [🔑]
Para el cliente: *"¿Sabe si había algún testamento? ¿Su familiar mencionó alguna vez que lo había hecho?"*
Razón: Si hay testamento, el proceso es testamentario, no intestado. Omitirlo produce un proceso que puede ser anulado si el testamento aparece después. Verificar en notarías antes de iniciar.

---

**S-02** [B] [⚡]
Para el cliente: *"¿Hay algún heredero que no esté incluido en la lista — un hijo no reconocido, un familiar con quien no se hablan, alguien que la familia omite voluntariamente?"*
Razón: Los legitimarios con derecho a la herencia pueden reclamarla aunque no sean mencionados en el proceso. Su omisión puede producir nulidades procesales y demandas de petición de herencia.

---

**S-03** [C] [🔑]
Para el cliente: *"¿El fallecido tenía deudas — créditos, embargos, obligaciones — que usted sepa?"*
Razón: Los herederos que aceptan la herencia sin beneficio de inventario responden por las deudas del causante. Si las deudas superan los activos, hay que aceptar con beneficio de inventario o renunciar. Saberlo antes evita que el heredero asuma involuntariamente pasivos que no calculó.

---

**S-04** [B]
Para el cliente: *"¿Hay bienes que no estaban a nombre del fallecido pero que en realidad eran de él — propiedades registradas a nombre de terceros, negocios informales?"*
Razón: Los bienes que pertenecían de facto al causante pero no estaban a su nombre requieren acciones adicionales (simulación, declaración de pertenencia) para integrarse a la masa herencial.

---

## SECCIÓN VII — CONTRATACIÓN ESTATAL

**CS-01** [D] [🔑]
Para el cliente: *"¿Tiene el contrato original firmado, con todas sus páginas, adiciones, pólizas, y actas?"*
Razón: El contrato estatal con todos sus documentos integra el marco jurídico completo. Sin el expediente contractual completo, el análisis es parcial.

---

**CS-02** [B] [🔑]
Para el cliente: *"¿Envió comunicaciones escritas a la entidad durante la ejecución — reportes de problemas, solicitudes, quejas, actas parciales?"*
Razón: En contratos estatales, las reclamaciones por desequilibrio económico y las quejas por incumplimiento de la entidad deben hacerse durante la ejecución, no solo después. Las comunicaciones enviadas son la mejor prueba. Los contratistas frecuentemente las tienen pero no saben que son evidencia jurídica.

---

**CS-03** [G] [🔑]
Para el cliente: *"¿El contrato tiene cláusula de solución de controversias — arbitraje, amigable composición — o dice algo sobre cómo se resuelven los conflictos?"*
Razón: Si el contrato tiene cláusula compromisoria, el juez natural es el árbitro, no el juez contencioso-administrativo. Radicar ante el juez equivocado produce nulidad por falta de jurisdicción.

---

**CS-04** [H] [🔑]
Para el cliente: *"¿Cree usted que hubo irregularidades en la forma en que se asignó o ejecutó el contrato — favoritismos, sobornos, incumplimientos que beneficiaron a otros?"*
Razón: Los contratos irregulares pueden tener dimensión penal (Art. 408-410 C.P.) y disciplinaria (Ley 1952/19). La denuncia penal o disciplinaria puede ser palanca complementaria al proceso de controversias contractuales.

---

**CS-05** [E] [🧭]
🧭 [{abogado}: ¿Cuáles entidades del orden territorial en Caldas tienen patrones conocidos de incumplimiento contractual, de imposición de sanciones abusivas, o de terminación unilateral injustificada? ¿Con cuáles es más efectivo conciliar que litigar?]

---

## SECCIÓN VIII — DERECHO ÉTNICO-TERRITORIAL

*Esta sección es la de mayor especificidad epistemológica de toda la biblioteca. Requiere el conocimiento de campo del abogado activo más que cualquier otra. El sistema aporta el marco jurídico; el abogado activo aporta el conocimiento real de cómo funcionan las comunidades, los territorios, y los actores en su circuito.*

*Fundamento jurídico: C.P. arts. 7, 63, 93, 246, 286, 329, 330 / Convenio 169 OIT (Ley 21/91) / Ley 70/93 / D. 2164/95 / Jurisprudencia constitucional sobre consulta previa: SU-123/18 🟡, T-661/15 🟡, T-972/14 🟡*

---

**ET-01** [A] [🔑]
Para el cliente: *"¿La comunidad está reconocida oficialmente — tiene resguardo, cabildo organizado, o personería jurídica ante el Ministerio del Interior?"*
Razón jurídica: El nivel de reconocimiento determina qué mecanismos están disponibles. Resguardo constituido = protección de Arts. 63 y 330 C.P. (inalienabilidad, imprescriptibilidad). Comunidad en proceso de reconocimiento = protecciones diferentes pero igualmente invocables — la identidad étnica no depende del reconocimiento formal. El proceso de reconocimiento puede tramitarse simultáneamente con la acción de protección.

---

**ET-02** [A] [🔑]
Para el cliente: *"¿Hay algún proyecto — una obra, una explotación de recursos, una infraestructura — que esté ocurriendo o que vaya a ocurrir en territorio de la comunidad o que los afecte?"*
Razón jurídica: La consulta previa, libre e informada (Art. 6 Convenio 169 OIT / Art. 330 C.P.) es derecho fundamental. La omisión de la consulta produce la nulidad de los actos administrativos que la autorizaron. La Corte ha establecido en SU-123/18 🟡 los estándares de la consulta previa. La acción judicial puede ser simultánea nulidad del acto + tutela por vulneración del derecho fundamental a la consulta.
🧭 [{abogado}: ¿Cuáles proyectos específicos en Caldas y el Eje Cafetero han omitido consulta previa? ¿Cuáles entidades (ANLA, ANM, ANH, gobernaciones, municipios) son las que más frecuentemente la omiten en esta región?]

---

**ET-03** [B] [🔑]
Para el cliente: *"¿Han intentado comprar, arrendar, o tomar el territorio de la comunidad por métodos informales — presiones, amenazas, acuerdos verbales con algunos miembros — fuera de los procesos legales formales?"*
Razón jurídica: El Art. 63 C.P. establece la inalienabilidad, imprescriptibilidad e inembargabilidad de los territorios de los grupos étnicos. Los intentos de transferir esos territorios por vías informales son nulos de pleno derecho. Pero la presión informal sobre líderes y miembros individuales es una táctica documentada para generar hechos consumados que luego se presentan como acuerdos válidos.
🧭 [{abogado}: ¿Cuáles actores — empresas, particulares, entidades — son conocidos en la región por usar estas tácticas?]

---

**ET-04** [PLU-01 aplicado] [🔑]
Para el cliente: *"¿Este problema fue llevado ante las autoridades propias de la comunidad — el cabildo, el consejo mayor, los mayores? ¿Qué decidieron?"*
Razón jurídica: La jurisdicción especial indígena (Art. 246 C.P.) tiene competencia para conocer y decidir conflictos que ocurren dentro del territorio y entre miembros de la comunidad. Una decisión de la autoridad indígena competente puede tener efectos de cosa juzgada. Además, acudir al sistema formal sin agotar el mecanismo propio puede ser visto como una ruptura del tejido comunitario que complica el caso.

---

**ET-05** [A] [🔑]
Para el cliente: *"¿La situación que me describe afecta el territorio, la cultura, las prácticas tradicionales, o la autonomía de la comunidad como colectivo — o es un problema individual de un miembro?"*
Razón jurídica: La distinción entre derechos colectivos del pueblo étnico y derechos individuales de sus miembros define completamente la estrategia. Los derechos colectivos del pueblo (territorio, consulta previa, autonomía, identidad cultural) se defienden con la comunidad como parte legitimada, no con el individuo. Los derechos individuales del miembro se defienden con el individuo, pero invocando su condición de pertenencia a la comunidad como factor de protección reforzada.

---

**ET-06** [B] [🔑]
Para el cliente: *"¿Hay divisiones dentro de la comunidad sobre cómo manejar este problema — hay miembros que quieren actuar de una forma y otros que quieren actuar diferente?"*
Razón: Las divisiones internas de una comunidad son explotadas sistemáticamente por quienes quieren vulnerar sus derechos colectivos. Un acuerdo negociado con una facción de la comunidad que no tiene legitimidad para representarla es nulo jurídicamente pero puede crear hechos consumados difíciles de revertir. El abogado necesita saber si la comunidad habla con una sola voz o si hay fragmentación interna que hay que manejar.
🧭 [{abogado}: COMPLETAR con conocimiento de las dinámicas específicas de las comunidades que has representado]

---

**ET-07** [H] [🔑]
Para el cliente: *"¿Hay líderes de la comunidad que hayan recibido amenazas, que hayan sido señalados, o que hayan sufrido cualquier forma de presión relacionada con este problema?"*
Razón: Las amenazas contra líderes de comunidades étnicas activan mecanismos de protección específicos: medidas cautelares de la CIDH, programas de protección de la UNP, mecanismos de la relatoría especial de la ONU para pueblos indígenas, y el sistema del IACHR de medidas cautelares por riesgo inminente. La sola solicitud de medidas cautelares a la CIDH cambia el comportamiento del Estado.

---

**ET-08** [D] [🔑]
Para el cliente: *"¿La comunidad tiene documentados sus derechos sobre el territorio — mapas, actas, acuerdos históricos, registros de uso tradicional del suelo?"*
Razón jurídica: En los procesos de ampliación, constitución, o defensa de resguardos, la prueba del uso y ocupación tradicional del territorio (no solo el título formal) es central. El Convenio 169 OIT y la jurisprudencia constitucional reconocen el derecho al territorio incluso sin título formal, basado en la ocupación tradicional. Los documentos que acreditan ese uso son frecuentemente orales o informales — hay que identificarlos y preservarlos.
[{abogado}: ¿Qué tipo de documentación de uso territorial han producido las comunidades del circuito que has acompañado? ¿Cuáles tribunales han reconocido esos documentos como prueba?]

---

**ET-09** [F] [🔑]
[{abogado}: PROTOCOLO DE CAPTURA — esta sección es la más importante de toda la biblioteca]

Caso de derecho étnico-territorial donde la pregunta que faltó fue determinante:
→ ¿Qué tipo de comunidad y qué tipo de caso?
→ ¿Qué no preguntaste y por qué?
→ ¿Qué habría cambiado si lo hubieras sabido?
→ ¿Cuál es la pregunta que harías ahora?

Conocimiento sobre actores específicos en Caldas y el Eje Cafetero:
→ ¿Cuáles empresas son las que más frecuentemente vulneran derechos de comunidades en esta región?
→ ¿Cuáles entidades del Estado son las que más frecuentemente omiten consulta previa?
→ ¿Cuáles comunidades tienen las disputas territoriales más activas?
→ ¿Cuáles son las dinámicas específicas de las relaciones interétnicas en esta zona?

Conocimiento sobre la jurisprudencia local:
→ ¿Cuáles jueces del circuito tienen mayor sensibilidad sobre derecho étnico?
→ ¿Cuáles argumentos han funcionado y cuáles han fallado en este circuito específico?
→ ¿El Tribunal Administrativo de Caldas tiene posición propia sobre algún aspecto del derecho étnico-territorial?

---

**ET-10** [F]
[{abogado}: COMPLETAR — Preguntas sobre dinámica cultural interna de las comunidades]

Hay preguntas que solo un abogado con conocimiento de campo puede hacer — preguntas sobre cómo funcionan internamente las comunidades específicas que el abogado activo ha acompañado. Estas preguntas no pueden ser generadas por el sistema porque requieren conocimiento etnográfico y de confianza construida con las comunidades:

Pregunta 1: *"[{abogado}: texto exacto de la pregunta]"*
Comunidades donde aplica: *[descripción]*
Razón: *[por qué esta dinámica interna es relevante para la estrategia jurídica]*

Pregunta 2: *"[{abogado}: texto]"*
Comunidades donde aplica: *[descripción]*
Razón: *[explicación]*

Pregunta 3: *"[{abogado}: texto]"*

---

## SECCIÓN IX — ACCIONES POPULARES Y DE GRUPO

**AP-01** [A] [🔑]
Para el cliente: *"¿Esto afecta solo a usted o hay más personas en la misma situación?"*
Razón: La acción popular (Art. 88 C.P. / Ley 472/98) protege derechos colectivos — no es para daños individuales. La acción de grupo (Ley 472/98 arts. 46 y ss.) protege daños individuales de un número plural de personas causados por el mismo hecho. Distinguir cuál aplica define completamente la acción y las pretensiones.

---

**AP-02** [G] [🔑]
Para el cliente: *"¿Hay alguna organización, ONG, o entidad pública que ya esté trabajando este problema en la comunidad — que ya haya denunciado esto o que tenga información sobre lo que está pasando?"*
Razón: Los actores populares no necesitan ser los únicos interesados en el caso. La coordinación con organizaciones que ya tienen información, evidencia, o recursos para sostener el proceso puede hacer la diferencia entre una acción popular exitosa y una que se pierde por falta de prueba o de recursos para sostener el proceso.

---

**AP-03** [H]
Para el cliente: *"¿El problema que describe tiene solución — la persona o entidad que lo causa puede parar si se le ordena?"*
Razón: La acción popular busca la cesación de la amenaza o la vulneración del derecho colectivo. Si el daño ya es irreversible, la acción popular puede no ser el mecanismo principal — puede combinarse con acciones de reparación.

---

## SECCIÓN X — PREGUNTAS TRANSVERSALES DE CIERRE

*Aplican a todo tipo de caso. Se ejecutan siempre al final.*

**TC-01** [B]
Para el cliente: *"¿Consultó este problema con otro abogado antes? ¿Qué le dijeron?"*
Razón: Detecta litispendencia potencial, revela si hay un proceso ya iniciado, y calibra las expectativas del cliente cuando el otro abogado le dijo algo diferente de lo que este análisis sugiere.

---

**TC-02** [J] [🔑]
Para el cliente: *"Si yo pudiera garantizarle el mejor resultado posible de este caso — ¿qué cambiaría en su vida?"*
Razón: La versión más profunda de OBJ-01. Hecha al final, cuando el cliente ya está más relajado y ha procesado la conversación, revela el objetivo real con más precisión.

---

**TC-03** [I]
Para el cliente: *"¿Tiene apoyo — familia, amigos, alguien — que lo acompañe durante este proceso?"*
Razón: El acompañamiento social del cliente es un factor de tolerancia al proceso. Un cliente aislado que enfrenta solo la incertidumbre de un litigio prolongado abandona más fácilmente. Saberlo permite anticipar qué tipo de acompañamiento necesita del abogado.

---

**TC-04** [B] [⚡] — LA PREGUNTA TRAMPA — SIEMPRE LA ÚLTIMA
Para el cliente: *"Antes de terminar: ¿hay algo que no me ha contado — algo que quizás cree que no importa, que le da pena decir, que cree que lo pone en mal lugar, o que simplemente no sé por qué no me dijo?"*
Razón: La pregunta trampa hecha al final, cuando la conversación ya tiene confianza construida, es más efectiva que hecha al principio. Es la última oportunidad de cerrar el gap de información antes de construir la estrategia. Lo que el cliente revela aquí frecuentemente es lo más relevante para la contraparte.

---

## CAPA 6 — PROTOCOLO DE CAPTURA DEL CONOCIMIENTO TÁCITO DEL ABOGADO ACTIVO

*Esta es la inversión más importante de la biblioteca a largo plazo.*

### Por qué el conocimiento tácito es el activo más valioso

El abogado activo sabe cosas que ningún sistema de IA puede generar: qué pregunta de un caso que perdió habría cambiado el resultado. Cómo actúa una EPS específica en su circuito. Cuál juez tiene una posición establecida sobre fuero sindical. Cómo razona el Tribunal de su región sobre nulidades de actos de entidades territoriales.

Ese conocimiento es el diferenciador real del sistema. No está en las bases de datos ni en la jurisprudencia pública. Está en la experiencia del abogado activo y en este momento existe solo en su cabeza.

El protocolo a continuación está diseñado para extraerlo de manera sistemática. Se ejecuta una vez al iniciar el sistema con un nuevo abogado y se actualiza con cada caso cerrado.

### Protocolo de entrevista de conocimiento — Para el abogado activo

**Parte A — Extracción por casos que salieron mal o que casi salen mal**

Para cada área de práctica principal, responder:

1. ¿Cuál es el caso que casi perdiste por una pregunta que no hiciste?
   → ¿Qué tipo de caso?
   → ¿Qué información faltó?
   → ¿Cuándo y cómo apareció esa información — en el proceso, por la contraparte, en el fallo?
   → ¿Cuál es la pregunta que habrías necesitado hacer?

2. ¿Cuál es el caso que ganaste por una pregunta que sí hiciste y que otros abogados no habrían hecho?
   → ¿Qué pregunta fue?
   → ¿Qué reveló?
   → ¿Por qué pocos abogados la harían?

3. ¿Cuál es la información que te da más miedo no tener cuando recibes un caso nuevo de cada tipo?

**Parte B — Extracción por actores recurrentes**

Para cada entidad, empresa, o tipo de contraparte que aparece frecuentemente en la práctica:

→ Nombre o descripción de la contraparte recurrente
→ ¿Cuál es su patrón de comportamiento en el proceso?
→ ¿Cuáles argumentos defensivos usa recurrentemente?
→ ¿Qué táctica ha funcionado contra ellos y cuál no?
→ ¿Hay algo sobre ellos que no está en ningún expediente pero que sabes por experiencia?

**Parte C — Extracción por despachos y jueces**

Para cada juzgado o tribunal donde se llevan casos frecuentemente:

→ Despacho
→ ¿Tiene el despacho posiciones conocidas sobre algún tipo de caso o argumento?
→ ¿Hay prácticas formales o informales del despacho que hay que conocer?
→ ¿Qué errores frecuentes cometen otros abogados en ese despacho?

**Parte D — Registro de nuevas preguntas en el tiempo**

Cada vez que un caso revela una pregunta nueva, registrar en este formato:

```
NUEVA PREGUNTA — [fecha de registro]
Código: [secuencial por área]
Tipo: [A/B/C/D/E/F/G/H/I/J]
Área: [área del derecho]
Para el cliente: "[texto exacto]"
Razón jurídica: [explicación]
Impacto estratégico: [qué cambia]
Origen: [tipo de caso + resultado + lo que reveló la pregunta]
Registrado por: {nombre_abogado}
```

---

## TABLA MAESTRA DE PRIORIZACIÓN

| Tipo de caso | Preguntas esenciales (siempre) | Preguntas de profundidad | Preguntas de circuito |
|-------------|-------------------------------|--------------------------|----------------------|
| Tutela salud | T-S-01, T-S-02, T-S-03, T-S-05 | T-S-04, T-S-06, T-S-09 | T-S-08 🧭 |
| Tutela otros derechos | T-O-01, T-O-03 | T-O-02, T-O-04 | — |
| Despido | L-D-01, L-D-02, L-D-03, L-D-05, L-D-06 | L-D-04, L-D-07, L-D-08, L-D-09 | L-D-10, L-D-11 🧭 |
| Acoso laboral | L-A-01, L-A-02, L-A-03 | L-A-04, L-A-05 | — |
| Prestaciones | L-P-01, L-P-02 | L-P-03 | — |
| Nulidad/restablecimiento | A-N-01, A-N-02, A-N-04 | A-N-03, A-N-05 | A-N-06 🧭 |
| Reparación directa | A-R-01, A-R-02, A-R-04 | A-R-03, A-R-05 | — |
| Proceso ejecutivo | E-01, E-03, E-04 | E-02, E-05 | E-04 🧭 |
| Divorcio | F-D-01, F-D-02, F-D-03 | F-D-04, F-D-05, F-D-06 | — |
| Alimentos | F-A-01, F-A-02 | — | — |
| Sucesión | S-01, S-02, S-03 | S-04 | — |
| Contratación estatal | CS-01, CS-02, CS-03 | CS-04 | CS-05 🧭 |
| Acción popular/grupo | AP-01, AP-03 | AP-02 | — |
| Étnico-territorial | ET-01, ET-02, ET-04, ET-05 | ET-03, ET-06, ET-07, ET-08 | ET-09, ET-10 🧭 |
| CAPAS 0-4 (siempre) | META-01, META-02, OBJ-01, OBJ-02, OBJ-03, OBJ-04, HEC-01, HEC-05 | HEC-02, HEC-03, HEC-04, HEC-06, HEC-07 | — |
| CIERRE (siempre) | TC-04 (pregunta trampa) | TC-01, TC-02, TC-03 | — |

---

## TABLA COMPARATIVA v1.0 vs v2.0

| Dimensión | v1.0 | v2.0 |
|-----------|------|------|
| Cliente | Asumido cooperativo y racional | Capa 0: evaluación del estado antes de interrogar |
| Objetivo real | No contemplado | Capa 1: 6 preguntas de objetivos y tolerancia |
| Terreno económico | "¿Cuánto perdió?" | Capa 3: 5 preguntas de análisis económico del caso |
| Dimensión penal | 1 mención genérica | 8 preguntas específicas con tipificación penal |
| Víctimas del conflicto | Ausente | Sección IV.D: 3 preguntas con marco completo de Ley 1448 |
| Pluralismo jurídico | Ausente | Sección IV.E: 2 preguntas estructurales |
| Disciplinaria | Ausente | 2 preguntas con análisis de impacto táctico |
| Internacional | Ausente | 2 preguntas con mecanismos CIDH |
| Étnico-territorial | 3 preguntas + 7 espacios vacíos | 10 preguntas desarrolladas + protocolo de captura del abogado activo |
| Conocimiento tácito | "COMPLETAR" sin estructura | Protocolo de captura en 4 partes con formato de registro |
| Métricas | Tabla vacía | Protocolo de actualización continua con formato definido |

---

## REGISTRO DE ACTUALIZACIONES

| Fecha | Código | Pregunta | Origen | Registrado por |
|-------|--------|----------|--------|----------------|
| Abr 2026 | — | Versión 2.0 base | Rediseño epistemológico | Felipe Cruz |
| Abr 2026 | — | Versión 3.0 — generalización de roles, Capa 6 genérica para cualquier abogado | Evolución del sistema LUMI | Felipe Cruz |

---

*Documento operacional — Lumi v3.0*
*Versión 3.0 — Abril 2026*
*Estado: BASE VALIDADA — el Protocolo de Captura de Conocimiento se ejecuta al incorporar cada nuevo abogado al sistema*
*CONFIDENCIAL — Propiedad de Felipe Cruz*
