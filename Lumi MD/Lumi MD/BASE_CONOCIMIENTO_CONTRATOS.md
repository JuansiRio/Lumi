# BASE DE CONOCIMIENTO — DERECHO DE CONTRATOS COLOMBIA
### *Módulo de contratación privada para LUMI Judicial*

> Versión 1.0 — Abril 2026
> Tipos cubiertos: Prestación de servicios · Contrato laboral · Acuerdos entre socios · Licencias
> Clasificación: Conocimiento interno del sistema — no exponer al usuario final

---

## ROLES DEL SISTEMA

| Variable | Significado |
|----------|-------------|
| `{nombre_abogado}` | El abogado activo que revisa y firma el contrato |
| `El abogado` | Referencia genérica al profesional responsable |
| `El cliente` | Quien encarga el contrato al despacho |

**Regla deontológica central:** Todo contrato generado por LUMI debe ser revisado,
ajustado si corresponde, y entregado bajo la responsabilidad del abogado activo.
LUMI genera el borrador. El abogado lo valida y firma la asesoría.

---

## ÍNDICE

1. [Marco general del contrato en Colombia](#1-marco-general)
2. [Contrato de prestación de servicios](#2-prestación-de-servicios)
3. [Contrato laboral](#3-contrato-laboral)
4. [Acuerdos entre socios](#4-acuerdos-entre-socios)
5. [Contratos de licencia](#5-licencias)
6. [Cláusulas transversales críticas](#6-cláusulas-transversales)
7. [Alertas y errores más frecuentes](#7-alertas-y-errores)
8. [Protocolo de generación de contratos en LUMI](#8-protocolo-lumi)

---

## 1. MARCO GENERAL DEL CONTRATO EN COLOMBIA

### Fuentes normativas principales

| Norma | Contenido relevante |
|-------|-------------------|
| Código Civil (Ley 84/1873) | Definición, formación, efectos, nulidades, modos de extinción |
| Código de Comercio (D. 410/1971) | Contratos mercantiles, actos de comercio, sociedades |
| Código Sustantivo del Trabajo (D. 2663/1950) | Contrato laboral, obligaciones, terminación |
| Ley 1258/2008 | Sociedad por Acciones Simplificada (SAS) |
| Ley 23/1982 y Ley 1915/2018 | Derechos de autor y licencias |
| Ley 1480/2011 | Estatuto del consumidor |
| Decreto 1074/2015 | Reglamentación comercial y de propiedad industrial |

### Principios que rigen todos los contratos

**Autonomía de la voluntad**
Las partes pueden acordar lo que quieran siempre que no violen normas imperativas,
el orden público ni las buenas costumbres. Este principio tiene más alcance
en contratos comerciales que en laborales, donde las normas son de orden público
y no pueden desfavorecerse para el trabajador.

**Buena fe objetiva (Art. 1603 C.C.)**
Los contratos obligan no solo a lo pactado expresamente sino a todo lo que
corresponda a la naturaleza del contrato. La buena fe es objetiva —
la conducta debe ser la que razonablemente se esperaría de alguien leal y diligente,
no basta con creer que se actúa bien.

**Relatividad**
El contrato solo produce efectos entre las partes y sus causahabientes.
No obliga a terceros, aunque puede generar efectos frente a ellos en casos específicos.

**Consensualismo**
La mayoría de los contratos se perfeccionan por el solo consentimiento (Art. 1500 C.C.).
La escritura no es requisito de existencia sino de prueba, excepto en contratos solemnes
(ej: compraventa de inmuebles requiere escritura pública).

### Elementos esenciales de cualquier contrato (Art. 1501 C.C.)

**1. Capacidad**
Personas naturales mayores de 18 años.
Personas jurídicas: representadas por quien tenga facultades suficientes.
⚠️ Error frecuente: el representante legal firma pero el certificado de existencia
y representación no le da facultades para ese acto específico.

**2. Consentimiento libre de vicios**
Sin error, fuerza ni dolo.
En personas jurídicas lo da el representante legal o quien esté facultado en estatutos o poder.

**3. Objeto lícito**
Lo que las partes se obligan a dar, hacer o no hacer. Debe ser posible,
determinado o determinable, y lícito.
⚠️ Objeto ilícito hace el contrato absolutamente nulo de pleno derecho.

**4. Causa lícita**
La razón que induce a contratar.
⚠️ Contratos con causa ilícita (ej: encubrir relación laboral como prestación de servicios)
son absolutamente nulos y generan responsabilidades adicionales.

### Clasificación práctica

**Por las obligaciones que genera:**
- *Bilaterales*: ambas partes se obligan recíprocamente (la mayoría)
- *Unilaterales*: solo una parte se obliga (donación, comodato)

**Por su ejecución en el tiempo:**
- *De ejecución instantánea*: se cumplen en un solo acto
- *De tracto sucesivo*: se ejecutan en el tiempo (servicios, arrendamiento, laboral)
  ⚠️ En los de tracto sucesivo, la terminación anticipada sin justa causa genera
  perjuicios por el período no ejecutado.

**Por su regulación:**
- *Típicos*: regulados por la ley (compraventa, arrendamiento, laboral)
- *Atípicos*: no tienen regulación específica pero son válidos
  (consultoría especializada, acuerdos de influencer, contratos de desarrollo de software)
  En los atípicos, lo que diga el contrato es casi todo lo que hay.

---

## 2. CONTRATO DE PRESTACIÓN DE SERVICIOS

### Qué es y cuándo se usa

El contrato por el cual una persona natural o jurídica se obliga a ejecutar
una actividad específica para otra, de manera independiente, a cambio de honorarios.

Es el contrato más usado para contratar consultores, freelancers, asesores,
diseñadores, desarrolladores y cualquier profesional independiente.
Su principal ventaja frente al laboral es la flexibilidad.
Su principal riesgo es que puede ser declarado laboral si en la realidad existe subordinación.

### Base legal

- Código Civil, Arts. 2063 y ss. — arrendamiento de servicios
- Código de Comercio, Arts. 1340 y ss. — contrato de empresa
- Código Sustantivo del Trabajo, Art. 23 — presunción de contrato laboral
- Jurisprudencia CSJ sobre el contrato realidad

### La distinción crítica frente al contrato laboral

| Elemento | Prestación de servicios | Contrato laboral |
|----------|------------------------|------------------|
| Subordinación | NO — autonomía técnica total | SÍ — el empleador da órdenes |
| Herramientas | El contratista pone las suyas | El empleador las provee |
| Horario | Libre — importa el resultado | Fijado por el empleador |
| Seguridad social | El contratista la paga completa | Empleador paga parte |
| Lugar de trabajo | El contratista elige | Generalmente definido |
| Exclusividad | No aplica salvo pacto | Implícita en la subordinación |

### La regla más importante: el contrato realidad

La Corte Suprema de Justicia ha establecido que si en la práctica el contratista
trabaja bajo subordinación —aunque el papel diga "prestación de servicios"—
el juez laboral puede declarar que existió contrato laboral desde el inicio.

Consecuencias: el contratante debe pagar retroactivamente salud y pensión
del empleador, cesantías, primas, vacaciones, intereses y multas.

**Señales de subordinación que convierten una prestación de servicios en contrato laboral:**
- Horario fijo controlado por la empresa
- Uso de correo corporativo del contratante
- Instrucciones sobre *cómo* hacer el trabajo (no solo el resultado)
- Uso de equipos y herramientas de la empresa
- Imposibilidad de prestar servicios a otros clientes simultáneamente
- Funciones permanentes, no proyectos específicos

### Cláusulas esenciales

**Objeto**
Describir con precisión qué actividad se ejecuta. Mientras más específico,
más difícil argumentar relación laboral.
❌ "El contratista prestará servicios de apoyo a la empresa"
✅ "El contratista ejecutará el diseño UX del módulo de pagos de la aplicación móvil,
entregando los siguientes productos: [lista con fechas]"

**Plazo**
Inicio y terminación. Si es por proyecto, definir el hito de entrega.
Mecanismo de renovación si aplica.

**Valor y forma de pago**
Honorarios totales o por hito. Periodicidad. Forma de pago.
Definir si los honorarios incluyen IVA o si aplica por encima.
Definir si se reembolsan gastos y bajo qué condiciones.

**Independencia y autonomía**
Declaración expresa de que el contratista actúa con total independencia técnica
y administrativa, determina sus propios métodos y horarios, y usa sus propias herramientas.
⚠️ Esta cláusula no es suficiente por sí sola si la práctica es diferente.
Lo que importa es la realidad de la ejecución, no solo el papel.

**Seguridad social**
El contratista declara que está obligado a pagar sus propias cotizaciones
sobre el 40% del valor de los honorarios como base mínima.
El contratante declara que no tiene obligación de pagar seguridad social.

**Propiedad intelectual** ← la más frecuentemente omitida
¿A quién pertenecen los resultados del trabajo?
Por defecto, el creador conserva derechos morales irrenunciables.
Los derechos patrimoniales pueden cederse o licenciarse contractualmente.
Si el contratante quiere la propiedad total del resultado, incluir cesión expresa
de derechos patrimoniales de autor.
Sin esta cláusula, el diseñador o desarrollador puede negarse a entregar el trabajo
o impedir su uso alegando que le pertenece.

**Confidencialidad**
Qué información es confidencial. Duración (2-5 años post-contrato es el estándar).
Excepciones (información pública, que ya tenía antes, que recibe de terceros legítimamente).

**Terminación anticipada**
Por incumplimiento. Por acuerdo. Por caso fortuito.
Preaviso mínimo para terminación sin justa causa (estándar: 30 días).
Consecuencias económicas de cada tipo de terminación.

**Resolución de conflictos**
Negociación directa → conciliación → arbitraje o juez ordinario.
Si se elige arbitraje: número de árbitros, reglas aplicables, lugar.

### Variantes importantes

**Contrato de consultoría**
El consultor da opinión y recomendaciones pero no ejecuta.
Tiene obligación de medio, no de resultado.
Incluir cláusula expresa: "Las recomendaciones constituyen opinión profesional
basada en la información disponible y no garantizan el resultado del negocio."

**Contrato de agencia independiente / representación comercial**
El agente promueve productos o servicios del empresario a cambio de comisión.
Regulado por Código de Comercio, Arts. 1317 y ss.
⚠️ ALERTA CRÍTICA: La terminación de un contrato de agencia comercial
genera derecho a indemnización equitativa (Art. 1324 C.Co.) aunque la terminación
sea unilateral del empresario sin justa causa.
Muchas empresas terminan agentes sin saber que deben una indemnización calculada
sobre las utilidades del agente. Es uno de los errores más costosos.

**Contrato de obra**
Obligación de resultado: entregar una obra determinada (software, diseño, campaña).
Garantía de calidad: el contratante puede reclamar por vicios ocultos durante
el plazo de garantía pactado o el legal supletorio.

---

## 3. CONTRATO LABORAL

### Por qué es diferente a todos los demás

El contrato laboral es el único en el que el principio de autonomía de la voluntad
cede completamente. Las normas laborales son de orden público —
cualquier cláusula que desmejore al trabajador frente a la ley es ineficaz,
aunque el trabajador la haya firmado libremente.

LUMI no solo genera el contrato laboral: verifica que cada cláusula cumpla
el mínimo legal. Si el cliente quiere incluir algo que viola la ley laboral,
el sistema lo advierte antes de generar el documento.

### Los tres elementos del contrato laboral (Art. 23 CST)

**1. Prestación personal del servicio**
El trabajador ejecuta personalmente las actividades. No puede delegar en un tercero.

**2. Subordinación y dependencia**
El empleador puede dar órdenes sobre el tiempo, modo y lugar de prestación.
Este es el elemento definitorio — lo que hace que un contrato sea laboral.

**3. Remuneración**
El trabajador recibe un salario a cambio del servicio.

Si los tres elementos existen en la práctica, hay contrato laboral —
independientemente del nombre que le den las partes al documento.

### Tipos de contrato laboral

**A término indefinido**
Sin fecha de terminación pactada. Mayor estabilidad para el trabajador.
El empleador puede terminarlo sin causa pagando indemnización (Art. 64 CST).

**A término fijo**
Plazo definido: mínimo 1 día, máximo 3 años. Prorrogable indefinidamente.
⚠️ Si se prorroga 3 veces o más, la no renovación genera indemnización
equivalente al término que restaba.
⚠️ Si el empleador no notifica la no renovación con 30 días de anticipación,
el contrato se entiende renovado automáticamente.

**De obra o labor**
Dura hasta terminar la obra o labor específica.
Muy usado en construcción y proyectos. Termina naturalmente con la obra
sin indemnización, pero sí genera si el empleador lo termina antes.

**De aprendizaje (Ley 789/2002)**
Entre empresa y estudiante para etapa productiva.
Remuneración: 75% SMMLV en etapa lectiva, 100% en etapa productiva.
No genera prestaciones sociales completas — pero sí obligaciones específicas.

### Estructura salarial

**Salario base**
Mínimo igual al SMMLV ($1.423.500 en 2026).
⚠️ Si se pacta por debajo del SMMLV, la diferencia es exigible de todas formas.

**Salario en especie**
Puede pactarse que parte del salario se pague en bienes o servicios.
Máximo 50% si el salario total es hasta 2 SMMLV.
Máximo 30% si supera ese monto.
⚠️ Si no se pacta expresamente como salario en especie, los beneficios
pueden igualmente ser declarados salario si son remunerativos.

**Salario integral**
Solo para trabajadores que ganen más de 10 SMMLV ($14.235.000 en 2026).
Incluye prestaciones, recargos y beneficios. Debe pactarse por escrito.
⚠️ Pactar salario integral para quien gana menos de 10 SMMLV es ineficaz —
el trabajador puede reclamar las prestaciones como si fuera salario ordinario.

**Elementos no salariales**
Las partes pueden pactar que ciertos pagos no son salario:
gastos de representación, bonos sujetos a condición, beneficios extralegales.
Requisito: pacto escrito genuino.
⚠️ Si el empleador paga bonos fijos mensuales sin condición, la Corte
los declara salario aunque el contrato diga lo contrario.

### Prestaciones sociales — mínimos no negociables

| Prestación | Valor | Quién paga | Cuándo |
|------------|-------|------------|--------|
| Prima de servicios | 1 mes de salario/año (2 pagos) | Empleador | Jun 30 y Dic 20 |
| Cesantías | 1 mes de salario/año | Empleador | Feb 14 al fondo |
| Intereses de cesantías | 12% anual sobre cesantías | Empleador | Ene 31 |
| Vacaciones | 15 días hábiles/año | Empleador | Al tomarlas |
| Dotación | 3 veces/año si salario ≤ 2 SMMLV | Empleador | Feb, Jun, Oct |

### Aportes a seguridad social y parafiscales

| Concepto | % Empleador | % Trabajador | Base |
|----------|-------------|--------------|------|
| Salud | 8.5% | 4% | Salario |
| Pensión | 12% | 4% | Salario |
| ARL | 0.52% - 8.7% | 0% | Salario |
| SENA | 2% | 0% | Nómina total |
| ICBF | 3% | 0% | Nómina total |
| Caja de compensación | 4% | 0% | Nómina total |

⚠️ LUMI debe calcular y mostrar el costo real del empleado antes de generar
el contrato. Un salario de $2.000.000 tiene un costo real de aproximadamente
$2.720.000-$2.800.000 para el empleador incluyendo todos los parafiscales
y prestaciones proporcionales.

### Fueros de estabilidad reforzada — no se puede despedir sin autorización del Ministerio

| Fuero | Cobertura |
|-------|-----------|
| Maternidad | Durante el embarazo y 6 meses después del parto |
| Lactancia | Durante el período de lactancia |
| Sindical | Trabajadores con fuero sindical |
| Prepensionado | Los 3 años anteriores a la pensión |
| Discapacidad | Trabajadores con limitaciones físicas o mentales |
| Enfermedad | Trabajador en incapacidad médica |

⚠️ Despedir a alguien con fuero sin autorización del Ministerio del Trabajo genera:
nulidad del despido + reintegro + pago de salarios durante el tiempo no trabajado
+ indemnización adicional. Es uno de los errores más costosos en derecho laboral.

### Causales de terminación con justa causa (Art. 62 CST — taxativas)

Las más frecuentes:
- Incumplimiento grave de obligaciones contractuales
- Actos de violencia dentro o fuera del trabajo
- Revelación de secretos técnicos o comerciales
- Daño intencional a bienes del empleador
- Rendimiento deficiente persistente y documentado
- Acoso laboral probado

⚠️ El empleador debe seguir el procedimiento correcto: comunicar los hechos
al trabajador, escuchar sus descargos, y tomar la decisión motivada.
Sin ese procedimiento, el despido puede ser declarado ilegal aunque haya justa causa.

### Indemnización por despido sin justa causa (Art. 64 CST)

**Contrato indefinido:**
- Primero año: 30 días de salario
- Año 2 en adelante: 20 días de salario por año adicional
- Para salarios superiores a 10 SMMLV: 20 días por primer año + 15 por año adicional

**Contrato a término fijo:**
El valor de los salarios correspondientes al tiempo que faltaba para terminar el contrato.

---

## 4. ACUERDOS ENTRE SOCIOS

### Por qué es el contrato más importante que un emprendedor firmará

El acuerdo de socios regula la relación entre los fundadores de una empresa.
Define quién tiene cuánto, quién decide qué, qué pasa si un socio quiere salir,
qué pasa si alguien incumple, y cómo se reparte el valor si la empresa se vende.

Sin este acuerdo, rigen los estatutos y la ley — que en muchos casos producen
resultados que ningún socio habría querido.

El tipo societario más relevante para emprendedores en Colombia es la SAS
(Sociedad por Acciones Simplificada, Ley 1258/2008) por su flexibilidad.
Todo lo que sigue aplica principalmente a SAS.

### Los dos documentos que gobiernan la relación entre socios

**Estatutos sociales**
Documento constitutivo registrado en Cámara de Comercio. Es público.
Define: objeto social, capital, representación legal, reuniones, distribución de utilidades.

**Acuerdo de socios (shareholders agreement)**
Documento privado entre los socios. No es obligatorio registrarlo (aunque puede).
Complementa y desarrolla los estatutos en aspectos que los socios no quieren
hacer públicos o que la ley permite regular contractualmente.

⚠️ Muchos emprendedores colombianos constituyen su SAS con estatutos minimalistas
("estatutos básicos de Confecámaras") y sin acuerdo de socios.
Eso funciona bien mientras todo va bien. Se rompe en el primer conflicto.

### Cláusulas esenciales del acuerdo de socios

**1. Tabla de capitalización**
Porcentaje exacto de cada socio desde el inicio y cómo puede cambiar.
Tipos de acciones si las hay (ordinarias vs. preferentes).
Mecanismo para nuevas emisiones: ¿requieren unanimidad? ¿supermayoría?

**2. Vesting — la cláusula que protege la empresa de socios que se van**
El vesting establece que los socios "se ganan" su participación gradualmente
en el tiempo, no toda de golpe desde el día uno.

Estándar en el mercado de startups colombiano y global:
- Período de cliff: 1 año. Si el socio se va antes del año, no recibe nada.
- Período de vesting total: 4 años.
- Después del cliff: el socio gana las acciones del cliff de golpe,
  y el resto se distribuye mensualmente por los 3 años restantes.

Sin vesting, un cofundador puede retirarse a los 6 meses conservando el 40%
de la empresa, sin poder hacer nada al respecto.

**3. Good leaver / Bad leaver**
Define qué pasa con las acciones cuando un socio sale.

*Good leaver* (salida legítima: muerte, enfermedad grave, acuerdo amistoso):
→ Vende sus acciones a valor justo de mercado.
→ Los demás socios tienen derecho de preferencia para comprar.

*Bad leaver* (fraude, competencia desleal, incumplimiento grave):
→ Vende sus acciones al precio más bajo entre valor nominal y valor de mercado.
→ Es una penalidad económica por la salida indebida.

**4. Drag along y tag along**

*Tag along (derecho de acompañamiento)*
Si un socio mayoritario vende su participación a un tercero, los socios minoritarios
tienen derecho a vender sus acciones al mismo precio y condiciones.
Protege a los minoritarios de quedar con un nuevo socio mayoritario no deseado.

*Drag along (derecho de arrastre)*
Si la mayoría (generalmente 60-75%) quiere vender la empresa, puede obligar
a los minoritarios a vender también.
Protege la capacidad de la mayoría de cerrar una venta cuando un minoritario
se niega por razones personales.

**5. Derecho de preferencia (right of first refusal)**
Antes de vender acciones a un tercero, el socio debe ofrecérselas primero
a los otros socios al mismo precio y condiciones.
Plazo para ejercer: 15-30 días estándar.

**6. Restricciones a la transferencia**
En startups es frecuente prohibir la venta de acciones sin aprobación
del consejo o los demás socios por un período (generalmente 3-5 años).
Evita que un socio insatisfecho venda a un competidor.

**7. Pacto de no competencia**
El socio activo se compromete a no competir con la empresa durante su participación
y por un período después de salir.
Límites razonables en Colombia: 1-2 años, actividades claramente definidas,
compensación si es muy restrictivo.
⚠️ Pactos de no competencia indefinidos o sin compensación tienden a ser
declarados ineficaces por desproporcionados.

**8. Compromisos de dedicación**
Si un socio es además empleado o directivo: dedicación mínima requerida.
Consecuencias si incumple (puede activar el mecanismo de bad leaver).

**9. Gobierno corporativo — reglas de decisión**
¿Qué decisiones requieren unanimidad?
(ej: venta de la empresa, modificación de estatutos, emisión de nuevas acciones)
¿Qué decisiones requieren supermayoría?
(ej: 75% para cambiar el objeto social)
¿Qué puede decidir solo el representante legal?
¿Cómo se rompe un empate entre socios con participaciones iguales?

**10. Distribución de utilidades**
La ley colombiana exige distribuir mínimo el 50% de las utilidades líquidas.
El acuerdo puede exigir más o establecer condiciones adicionales.
Para startups: frecuentemente se pacta reinversión total hasta alcanzar
un hito específico (break even, primera ronda, meta de ingresos).

**11. Mecanismos de resolución de conflictos entre socios**

*Shot gun clause (cláusula de escopeta):*
Si hay un conflicto irresoluble entre socios igualitarios (50/50), cualquiera
puede activar: propone un precio para las acciones. El otro debe elegir:
o vende al precio propuesto, o compra al mismo precio.
Fuerza propuestas de precio justas porque quien propone no sabe si será
vendedor o comprador.

*Buy-sell agreement:*
Cualquier socio puede ofrecer comprar la participación de los otros a un precio.
Los otros deben vender o comprar al mismo precio.

*Mediación y arbitraje:*
Instancias previas a los mecanismos coercitivos.
El Centro de Arbitraje y Conciliación de la CCB es el estándar en Colombia.

### Aspectos específicos para startups con inversión

**Acciones preferentes para inversionistas**
Los inversionistas generalmente reciben acciones preferentes con derechos adicionales:
- Liquidation preference: cobran primero que los fundadores en una venta
- Anti-dilución: protección ante nuevas rondas a valoración menor
- Derecho de información: acceso a estados financieros periódicos
- Derecho de veto sobre decisiones estratégicas

**SAFE (Simple Agreement for Future Equity)**
Instrumento frecuente en rondas pre-seed. No es deuda ni acciones —
es un derecho a recibir acciones en la siguiente ronda con descuento o cap de valoración.
En Colombia es válido como instrumento atípico pero debe estructurarse cuidadosamente
para evitar que se clasifique como deuda y genere obligaciones de intereses.

---

## 5. LICENCIAS

### Qué es una licencia

Autorización del titular de un derecho de propiedad intelectual
para que un tercero lo use bajo condiciones específicas, conservando el titular la propiedad.
La licencia no transfiere la propiedad — transfiere el derecho de uso.

### Licencias de software

**Marco normativo:**
Ley 23/1982 — derechos de autor
Ley 1915/2018 — reforma a la ley de derechos de autor
Decisión 351 de la CAN

El software en Colombia es protegido como obra literaria por derechos de autor.
La protección es automática desde la creación — no requiere registro,
aunque el registro ante la DNDA es evidencia de titularidad.

**Cláusulas críticas en licencias de software:**

*Alcance del uso*
¿Cuántos usuarios? ¿Cuántos dispositivos? ¿Cuántas instancias? ¿En qué actividades?

*Territorio*
¿Solo Colombia? ¿América Latina? ¿Mundial?

*Exclusividad*
¿El licenciatario es el único que puede usar el software en ese mercado o sector?
La exclusividad generalmente implica un precio mayor y obligaciones de mínimo de uso.

*Derecho de modificación*
¿Puede el licenciatario modificar el código?
Si puede, ¿a quién pertenecen las modificaciones?
Si el licenciatario no tiene derecho a modificar, ¿cómo se gestionan las solicitudes
de cambio o personalización?

*Sublicencias*
¿Puede el licenciatario dar acceso a terceros?
Si es SaaS, ¿puede el licenciatario recomercializar el servicio?

*Código fuente*
¿Se entrega el código fuente o solo el ejecutable?
Si se entrega código fuente, ¿bajo qué condiciones de confidencialidad?
¿Hay escrow del código fuente para proteger al licenciatario si el licenciante desaparece?

*SLA (Service Level Agreement) para software como servicio:*
- Disponibilidad garantizada (uptime): estándar 99.5% o 99.9%
- Tiempo de respuesta para incidentes críticos (P1: 1-4 horas; P2: 8-24 horas)
- Penalidades por incumplimiento del SLA (créditos de servicio)
- Procedimiento de reporte y escalamiento de bugs

*Garantías y limitación de responsabilidad*
En licencias de software es estándar limitar la responsabilidad al valor del contrato.
Sin esta cláusula, si el software falla y causa perjuicios, la responsabilidad
puede ser desproporcionada al precio pagado.

### Licencias de marca

**Marco normativo:**
Decisión 486 de la Comunidad Andina
Ley 1648/2013
Regulación de la SIC

**Cláusulas críticas:**

*Control de calidad*
⚠️ El licenciante DEBE mantener control sobre la calidad de productos y servicios
que se ofrecen bajo su marca. Si pierde ese control, puede perder la marca
por cancelación por engaño al consumidor. Esta cláusula protege tanto al licenciante
como a los consumidores.

*Territorio y canal*
¿En qué ciudades o regiones puede usar la marca?
¿Solo en ciertos canales (retail, online, institucional)?

*Regalías*
Porcentaje de ventas netas o monto fijo mensual.
Obligación de reportar ventas mensualmente o trimestralmente.
Derecho del licenciante a auditar los libros del licenciatario.
Mínimo garantizado (si el licenciatario no vende lo suficiente, igual debe pagar mínimos).

*Terminación y uso post-terminación*
¿Cuánto tiempo tiene el licenciatario para dejar de usar la marca después
de terminar el contrato? (estándar: 30-60 días para retirar inventario)
¿Qué pasa con el inventario marcado que quede sin vender?

### Licencias de contenido (obras protegidas por derechos de autor)

Aplica a: fotografías, textos, música, videos, diseños, ilustraciones, código.

**Cesión vs. licencia — distinción fundamental:**

*Cesión de derechos patrimoniales:*
El creador transfiere permanentemente los derechos al cliente.
El cliente pasa a ser el titular patrimonial.
El creador conserva derechos morales (atribución de autoría) que son irrenunciables.

*Licencia:*
El creador conserva la titularidad y autoriza el uso bajo condiciones específicas
(tiempo, territorio, modalidades de uso).

⚠️ Sin una cláusula de cesión o licencia explícita en un contrato de prestación
de servicios creativos, el cliente que pagó por el diseño, la fotografía o el código
puede encontrarse sin derecho legal a usarlo si hay un conflicto posterior.

**Derechos morales — no son transferibles ni renunciables en Colombia**
El autor siempre tiene derecho a que se le atribuya la obra y a que no se distorsione.
En la práctica comercial esto se maneja pactando que el autor no ejercerá
activamente ese derecho — lo que es diferente a renunciarlo.

### Open source y licencias permisivas

Para software con componentes open source, verificar qué tipo de licencia
tiene cada componente:
- *MIT / BSD / Apache 2.0*: permisivas — se puede incluir en software propietario
- *GPL / LGPL*: copyleft — el software que las incorpora debe también ser open source
- *AGPL*: copyleft fuerte — aplica incluso si se distribuye como servicio web

⚠️ Incluir componentes GPL en software comercial sin licencia comercial dual
puede obligar a liberar el código fuente de todo el producto.

---

## 6. CLÁUSULAS TRANSVERSALES CRÍTICAS

Aplicables a todos o la mayoría de los contratos.
LUMI las incluye por defecto y solo las omite cuando el cliente
tiene razones específicas confirmadas.

### Confidencialidad

**Elementos mínimos:**
1. Definición precisa de qué es información confidencial
2. Obligaciones del receptor: no divulgar, no usar para propósitos distintos,
   proteger con el mismo nivel que su propia información confidencial
3. Excepciones: información pública, que el receptor ya tenía, recibida
   legítimamente de terceros, que debe divulgarse por orden judicial o legal
4. Duración: durante el contrato y X años después (estándar: 2-5 años,
   algunos elementos como datos personales de clientes pueden ser indefinidos)
5. Consecuencias del incumplimiento: daños y perjuicios más cláusula penal

**NDA independiente vs. NDA integrado al contrato**
Si la negociación requiere compartir información confidencial antes de firmar
el contrato principal, el NDA debe firmarse primero como documento separado.
Una vez firmado el contrato, el NDA integrado lo reemplaza o coexiste con él.

### Cláusula penal

Suma fija acordada como indemnización en caso de incumplimiento de una obligación.
Cumple dos funciones: apremiar al cumplimiento y fijar anticipadamente el monto del daño.

⚠️ El juez puede reducirla si es desproporcionada (Art. 1601 C.C.).
El estándar razonable es que no supere el valor de la obligación principal.

⚠️ Si se cobra la cláusula penal no se puede también cobrar el daño real,
a menos que se pacte expresamente que la cláusula penal es adicional y no sustitutiva.

### Limitación de responsabilidad

Para contratos comerciales (no laborales), es estándar limitar la responsabilidad
al valor del contrato o a un múltiplo de él.

Incluir exclusión de daños indirectos y consecuenciales:
lucro cesante, pérdida de oportunidad de negocio, daño a la reputación,
daño a relaciones comerciales.

⚠️ Esta cláusula no aplica a dolo o culpa grave — en Colombia no se puede
limitar contractualmente la responsabilidad por dolo.

### Fuerza mayor y caso fortuito

Eventos imprevisibles e irresistibles que impiden el cumplimiento.

El contrato debe definir:
1. ¿Qué eventos califican? ¿Incluye fallas de internet, crisis económica,
   cambios normativos, pandemia?
2. ¿Qué obligaciones se suspenden y por cuánto tiempo?
3. Si la fuerza mayor dura más de X meses, cualquiera puede terminar
   el contrato sin indemnización
4. Obligación de notificación: la parte afectada notifica dentro de X días hábiles

### Integralidad del contrato (merger clause)

"El presente contrato constituye el acuerdo completo entre las partes y reemplaza
cualquier acuerdo, negociación, representación o entendimiento anterior, verbal o escrito."

Evita que una parte alegue acuerdos verbales previos que modifiquen el contrato escrito.

### Modificaciones

"Cualquier modificación debe constar por escrito y ser firmada por ambas partes."

Sin esta cláusula, una modificación verbal puede ser vinculante si se prueba el acuerdo.

### Cesión del contrato

"Ninguna parte puede ceder sus derechos u obligaciones sin el consentimiento
previo y escrito de la otra parte, salvo [excepciones específicas pactadas]."

### Divisibilidad

"Si alguna cláusula de este contrato fuera declarada inválida o inaplicable,
las demás cláusulas continuarán en pleno vigor."

Sin esta cláusula, la nulidad de una cláusula puede argumentarse para nulitar todo el contrato.

### Ley aplicable y jurisdicción

Para contratos entre partes de diferentes ciudades o países:
- Ley aplicable: ley colombiana (o la que se acuerde para contratos internacionales)
- Ciudad para efectos de notificaciones judiciales y extrajudiciales
- Mecanismo de resolución de conflictos: arbitraje o juez ordinario

---

## 7. ALERTAS Y ERRORES MÁS FRECUENTES

### Los 12 errores que LUMI detecta automáticamente

**Error 1 — Prestación de servicios con elementos de subordinación**
Señales de alerta en el brief del cliente:
- "El contratista trabajará en nuestras oficinas"
- "El contratista tendrá horario de 8am a 5pm"
- "El contratista usará nuestro correo corporativo"
- "El contratista no puede trabajar para otros clientes"
- "El contratista reportará al gerente"
→ Riesgo de contrato realidad. Recomendar contrato laboral o reestructurar la relación.

**Error 2 — Contrato laboral sin cláusula de elementos no salariales**
Si el cliente quiere pagar bonos, auxilios o beneficios en especie sin definirlos
como "no salariales" en el contrato, se vuelven base de prestaciones sociales.

**Error 3 — Contrato de servicios creativos sin cláusula de propiedad intelectual**
Sin la cesión de derechos, el contratante puede no tener derecho legal
a usar lo que pagó.

**Error 4 — Acuerdo de socios sin vesting**
Un cofundador puede retirarse a los 6 meses conservando el 40% de la empresa.

**Error 5 — Terminación de agente comercial sin pago de indemnización**
La terminación del contrato de agencia comercial siempre genera derecho
a indemnización equitativa (Art. 1324 C.Co.), aunque sea terminación unilateral.

**Error 6 — Contrato laboral sin verificación de fuero**
Despedir a alguien con fuero (maternidad, discapacidad, prepensionado) sin
autorización del Ministerio del Trabajo es uno de los errores más costosos.

**Error 7 — Licencia de software sin SLA ni limitación de responsabilidad**
Si el software falla y el cliente pierde dinero, sin SLA y sin limitación
de responsabilidad la exposición del proveedor puede ser ilimitada.

**Error 8 — Contrato sin mecanismo de terminación anticipada**
Si el contrato puede terminarse de un día para otro sin consecuencias,
la parte débil queda desprotegida. La ausencia de preaviso genera perjuicios.

**Error 9 — Acuerdo de socios sin mecanismo de resolución de conflictos**
Si los socios llegan al 50/50 sin mecanismo de desempate, la empresa queda
paralizada hasta que un juez decida — lo que puede tardar años.

**Error 10 — Contrato con representante legal sin verificar sus facultades**
Si el certificado de Cámara de Comercio limita las facultades del representante
a contratos de cierto monto o tipo, firmar por encima de eso puede hacer
el contrato inoponible a la sociedad.

**Error 11 — Pacto de no competencia desproporcionado o sin compensación**
Un pacto de no competencia de 5 años o con actividades demasiado amplias
es potencialmente ineficaz. Mejor uno específico y razonable que uno
amplio pero inaplicable.

**Error 12 — Contrato en español con partes extranjeras sin ley aplicable**
Para contratos con partes de otros países, si no se define ley aplicable
ni jurisdicción, el primer conflicto activa un debate procesal internacional
antes de entrar al fondo.

---

## 8. PROTOCOLO DE GENERACIÓN DE CONTRATOS EN LUMI

### Preguntas que LUMI hace antes de generar cualquier contrato

**Preguntas universales (todos los contratos):**

1. ¿Quiénes son las partes? Nombre completo, tipo (persona natural o jurídica),
   NIT o cédula, ciudad de domicilio, representante legal si es empresa.
2. ¿Cuál es el objeto exacto del contrato? ¿Qué se va a hacer, entregar o usar?
3. ¿Cuánto tiempo durará la relación?
4. ¿Cuánto se pagará, cómo y cuándo?
5. ¿Hay información confidencial que proteger?
6. ¿Hay activos intelectuales involucrados (código, diseño, contenido, marca, patente)?
7. ¿Qué pasa si una de las partes incumple?
8. ¿Cómo quieren resolver los conflictos: conciliación, arbitraje o juez?

**Preguntas específicas por tipo:**

*Para prestación de servicios:*
- ¿El contratista trabajará solo para esta empresa o para varios clientes?
- ¿Trabajará en las instalaciones del contratante o desde su propio espacio?
- ¿Usará equipos o herramientas del contratante?
- ¿Recibirá instrucciones sobre el método o solo sobre el resultado final?
- ¿Quién va a ser dueño de lo que produzca (código, diseño, contenido)?

*Para contrato laboral:*
- ¿Cuál es el salario mensual acordado?
- ¿Hay beneficios adicionales (auxilio de transporte, alimentación, vehículo)?
  Si los hay, ¿se quiere pactar expresamente que no son salario?
- ¿El trabajador maneja dinero, bienes o información confidencial?
  (Puede ser relevante para la justa causa en caso de terminación)
- ¿El trabajador tiene alguna condición de salud conocida o está
  en período de embarazo o lactancia? (Activa análisis de fueros)
- ¿Cuántos años le faltan para pensionarse? (Fuero de prepensionado)

*Para acuerdo de socios:*
- ¿Cuántos socios son y cuál es el porcentaje de cada uno?
- ¿Todos los socios van a trabajar activamente en la empresa o hay socios
  solo financieros/pasivos?
- ¿Han discutido qué pasa si un socio quiere salir?
- ¿Tienen una valoración o metodología de valoración acordada?
- ¿Esperan recibir inversión externa en el corto o mediano plazo?

*Para licencias:*
- ¿Qué exactamente se está licenciando (software, marca, contenido, patente)?
- ¿Es exclusiva o no exclusiva?
- ¿En qué territorio aplica?
- ¿Hay código fuente involucrado? ¿Se entrega o solo el ejecutable/acceso?
- ¿Es un pago único, suscripción o regalías sobre ventas?

### Cómo LUMI estructura el borrador del contrato

**Estructura estándar de cualquier contrato:**

```
ENCABEZADO
→ Nombre del contrato
→ Ciudad y fecha
→ Identificación completa de las partes

CONSIDERANDOS (opcional pero recomendado)
→ Por qué las partes están firmando este contrato
→ Establece el contexto y la intención

CLÁUSULAS
→ Objeto
→ Obligaciones de cada parte
→ Precio/contraprestación
→ Plazo y condiciones de renovación
→ Confidencialidad
→ Propiedad intelectual (si aplica)
→ Limitación de responsabilidad
→ Fuerza mayor
→ Causales de terminación
→ Consecuencias de la terminación
→ Resolución de conflictos
→ Ley aplicable y jurisdicción
→ Disposiciones finales (integralidad, modificaciones, cesión, divisibilidad)

FIRMAS
→ Nombre completo, documento, calidad en que firma
→ Si es empresa: nombre, NIT, representante legal, cargo
→ Espacio para fecha y ciudad de firma
```

### Marcadores de verificación que LUMI incluye en el borrador

Todo contrato generado incluye al final una tabla de verificación:

| # | Verificar | Estado |
|---|-----------|--------|
| 1 | Capacidad de las partes (mayoría de edad / facultades del representante) | 🔴 VERIFICAR |
| 2 | Certificado de existencia y representación vigente (si es empresa) | 🔴 VERIFICAR |
| 3 | Cláusulas específicas según la naturaleza real de la relación | ✅ Incluidas |
| 4 | Ley aplicable y jurisdicción definidas | ✅ Incluidas |
| 5 | Firmas de ambas partes en todas las páginas (o solo en la última si se prefiere) | 🔴 VERIFICAR antes de firmar |
| 6 | Verificar si el contrato requiere autenticación notarial | 🔴 Según el tipo |
| 7 | Revisar si hay obligaciones de registro (ej: licencias de marca ante SIC) | 🔴 Verificar |

### La regla de oro para contratos en LUMI

Antes de generar cualquier contrato, LUMI verifica si la descripción del cliente
activa alguna de las alertas del punto 7. Si activa una alerta, la comunica
antes de generar el borrador. Nunca genera un contrato de prestación de servicios
sin primero preguntar sobre los indicadores de subordinación.

El borrador que genera LUMI es un punto de partida profesional,
no un documento listo para firmar sin revisión del abogado.
El abogado activo ajusta según las particularidades del caso,
las necesidades específicas del cliente, y su criterio profesional.

---

## NOTAS DE VERSIÓN

| Versión | Fecha | Cambio |
|---------|-------|--------|
| 1.0 | Abril 2026 | Documento inicial — cubre prestación de servicios, contrato laboral, acuerdos entre socios y licencias para la práctica de emprendedores y empresas en Colombia |

---

*LUMI Judicial — Base de Conocimiento Contratos v1.0*
*LUMI propone. El abogado decide y firma. Siempre.*
