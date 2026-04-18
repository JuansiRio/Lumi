# 🧠 MOTOR DE RAZONAMIENTO — LUMI
### *Cómo Lumi piensa, razona y procesa cada caso de principio a fin*

> Documento técnico-conceptual del sistema de inteligencia de Lumi
> Autor: Felipe Cruz
> Versión 2.0 — Abril 2026

> **NOTA DE REMISIÓN:**
> Este documento describe la arquitectura general del motor de razonamiento.
> Para los principios conceptuales profundos (cadena epistémica, modelo vivo del caso,
> calibración procesal, documento híbrido, trazabilidad numérica), consultar:
> → `LUMI_MOTOR_RAZONAMIENTO_AVANZADO_v2.md` — Principios I a IX
>
> Para los prompts operativos de cada instancia y fase, consultar:
> → `PROMPTS_POR_INSTANCIA_v3.md` — Fases 0 a 8 con instrucciones completas

---

## PRINCIPIO RECTOR

Lumi no procesa casos. Lumi **razona** casos.

```
PROCESAR:
Recibir input → aplicar regla → entregar output
(lo hace cualquier formulario)

RAZONAR:
Recibir input → cuestionar el input →
buscar lo que no está → calcular consecuencias →
anticipar contraargumentos → ponderar escenarios →
construir la mejor ruta posible →
saber cuándo esa ruta cambia
```

La diferencia no es técnica. Es la diferencia entre una herramienta y un colega.

---

## PROTOCOLO DE ENTRADA — CÓMO LUMI RECIBE UN CASO

> *"La complejidad del sistema vive adentro, no en la puerta de entrada."*

### El principio

El punto de entrada a LUMI es siempre el mismo: **un campo en blanco.**

El abogado comparte lo que tiene, en el formato en que lo tiene.
LUMI lee, extrae, infiere — y solo entonces pregunta lo que no pudo resolver solo.

No hay formulario de onboarding. No hay estructura impuesta. No hay checklist inicial.
El rigor no depende de cómo llega la información. Depende de cómo LUMI la procesa.

### Formatos válidos de entrada

LUMI acepta cualquier combinación de los siguientes, sin jerarquía entre ellos:

```
→ Texto libre        Mensaje en chat, resumen informal, contexto narrado
→ Transcripción      Nota de voz del cliente, grabación de reunión
→ PDF                Acta, contrato, sentencia, tutela, resolución
→ Imagen             Foto de documento, captura de pantalla, evidencia
→ Word / Excel       Contratos, liquidaciones, tablas de cálculo
→ Combinaciones      Cualquier mezcla de los anteriores
```

No existe un formato incorrecto.
Lo incorrecto es pedirle al abogado que organice antes de que LUMI haya leído.

### Lo que LUMI hace internamente antes de responder

```
1. LECTURA COMPLETA
   Lee todo lo recibido sin filtros previos.
   No asume formato. No asume estructura.

2. EXTRACCIÓN
   Identifica: partes, hechos, fechas, pretensiones,
   documentos mencionados, riesgos visibles.

3. CLASIFICACIÓN TENTATIVA
   ¿Qué tipo de caso parece ser?
   ¿Qué área del derecho activa?
   ¿Hay alertas inmediatas que deban nombrarse
   antes de continuar? (caducidad, riesgo ético,
   hecho disruptivo)

4. IDENTIFICACIÓN DE VACÍOS
   ¿Qué información es necesaria y no fue aportada?
   ¿Esos vacíos son bloqueantes o se puede
   trabajar con lo que hay?

5. RESPUESTA CALIBRADA
   LUMI responde con lo que puede analizar ya,
   y pregunta solo lo que realmente necesita —
   una o dos preguntas máximo, ordenadas por impacto.
```

### La regla de las preguntas

LUMI no pregunta para completar un formulario.
LUMI pregunta cuando la respuesta **mueve el caso** — hacia arriba o hacia abajo.

> Si una pregunta no cambia el análisis, la estrategia o la probabilidad de éxito, no se hace.

Las preguntas se generan en orden de impacto, no en orden lógico ni cronológico.
En el primer intercambio: máximo dos preguntas. El abogado no viene a ser interrogado.

### Lo que LUMI nunca hace en la entrada

```
❌ Pedir que el caso llegue estructurado
❌ Exigir todas las partes antes de arrancar
❌ Hacer preguntas genéricas de onboarding
❌ Bloquear el análisis por información faltante
❌ Asumir que el insumo llegará en formato jurídico

✅ Leer lo que llega y estructurarlo internamente
✅ Trabajar con lo disponible y señalar los vacíos
✅ Preguntar solo lo que mueve el caso
✅ Marcar vacíos como [DESCONOCIDO] y avanzar
✅ Procesar desde nota de voz, foto o texto informal
```

### Activación del protocolo completo

Una vez que LUMI tiene suficiente información para orientar el caso,
activa las fases del motor en el orden que corresponda.

**"Suficiente" no significa "completo."**
Significa suficiente para que el análisis tenga más valor que el silencio.

---

## ARQUITECTURA GENERAL DEL RAZONAMIENTO

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 0 — CAPTURA E INTELIGENCIA INICIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
0A — Auditor de hechos
0B — Detector de cambio de caso
0C — Estratega inicial
0D — Mapa probatorio

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 1 — MOTOR DE PREGUNTAS CRÍTICAS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1A — El Interrogador
1B — El Integrador (+ segunda ronda si aplica)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 2 — MOTOR PROBABILÍSTICO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2A — El Calculador
2B — Análisis de sensibilidad

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GENERACIÓN — LUMI ESCRIBE EL BORRADOR
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 3 — REVISIÓN JURÍDICA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3A — Revisor jurídico especializado
3B — Corrección 1 → Borrador v2

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 4 — VALIDACIÓN DE FUENTES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4A — Validador de fuentes (4 niveles)
4B — Corrección 2 → Borrador v3

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 5 — SIMULACIÓN ADVERSARIAL Y RIESGO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5A — Abogado contrario de alto nivel
5B — Análisis de nulidades propias
5C — Corrección 3 → Borrador v4

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 6 — PREGUNTAS FINALES AL ABOGADO
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6A — El Afinador
6B — Ajuste final → Borrador pre-final

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 7 — CONSISTENCIA Y MODO CLIENTE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7A — Verificador de consistencia interna
7B — Revisor del Modo Cliente

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE FINAL — CERTIFICACIÓN Y ENTREGA
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FASE 8 — CICLO DE VIDA POST-RADICACIÓN
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8A — Radar de plazos
8B — Analizador de respuestas
8C — Generador de piezas procesales sucesivas
8D — Analizador de fallos
8E — Depósito de inteligencia
```

---

## FASE 0 — CAPTURA E INTELIGENCIA INICIAL

### El principio de esta fase

Un borrador construido sobre hechos incompletos nace mal. Ninguna revisión posterior lo salva. Esta fase existe para garantizar que Lumi nunca escribe sobre base inestable.

---

### INSTANCIA 0A — Auditor de Hechos

**Qué hace:**
Verifica que los hechos del caso sean completos, consistentes y suficientes para el tipo de proceso antes de escribir una sola línea.

**Capa 1 — Completitud estructural**

Cada tipo de caso tiene un set mínimo de hechos sin los cuales es imposible proceder. Ejemplos:

```
TUTELA DE SALUD — hechos mínimos
├── Identidad y afiliación al sistema de salud
├── Diagnóstico médico documentado
├── Servicio o medicamento negado (específico)
├── Quién negó (EPS, IPS, médico, comité)
├── Cómo negó (escrito, verbal, silencio)
├── Cuándo negó (fecha exacta)
├── Qué pasó después de la negativa
└── Estado actual de salud del paciente

DESPIDO LABORAL — hechos mínimos
├── Tipo de contrato y fecha de inicio
├── Fecha y modalidad de terminación
├── Causa alegada por el empleador
├── Si se firmó algo al momento del despido
├── Si se recibió algún pago
├── Si hay testigos del despido
└── Si hay comunicaciones escritas

PROCESO EJECUTIVO — hechos mínimos
├── Título ejecutivo identificado
├── Cuantía exacta de la deuda
├── Fecha de exigibilidad
├── Si hay pagos parciales realizados
├── Bienes conocidos del deudor
└── Si el deudor está notificado de la deuda
```

**Capa 2 — Consistencia temporal**

Lumi construye una línea de tiempo interna y detecta:
- Hechos que ocurren antes de que fuera posible que ocurrieran
- Plazos que no cuadran con las fechas narradas
- Contradicciones entre relato del cliente y documentos aportados
- Fechas que activarían caducidad inminente no detectada

**Capa 3 — Detección de hechos ocultos por patrón**

El sistema conoce los patrones de omisión más frecuentes por tipo de caso:

```
EN DIVORCIOS — omisiones frecuentes
├── Violencia intrafamiliar (cambia la ruta completamente)
├── Bienes que el otro cónyuge no sabe que existen
├── Deudas ocultas que afectan la sociedad conyugal
├── Preferencia de custodia expresada por los hijos
└── Separaciones previas no formalizadas

EN LABORALES — omisiones frecuentes
├── Documentos firmados bajo presión al momento del despido
├── Pagos informales no registrados en nómina
├── Testigos presenciales del despido o acoso
├── Comunicaciones del empleador post-despido
└── WhatsApps o correos que revelan el motivo real

EN TUTELAS DE SALUD — omisiones frecuentes
├── Intentos previos de reclamación ante la EPS
├── Quejas ante la Supersalud no resueltas
├── Otros familiares con la misma negativa de la misma EPS
├── Condiciones de vulnerabilidad del paciente
└── Si el médico tratante pertenece a la red de la EPS

EN SUCESIONES — omisiones frecuentes
├── Bienes que no están a nombre del causante
├── Deudas del causante no declaradas
├── Herederos que el cliente no menciona
├── Testamento cuya existencia se desconoce
└── Conflictos previos entre herederos
```

**Output de 0A:**
```
RESULTADO AUDITORÍA DE HECHOS

Estado: INCOMPLETO / COMPLETO / INCONSISTENTE

Hechos faltantes críticos (bloquean el proceso):
→ [lista]

Inconsistencias detectadas:
→ [lista con explicación]

Patrones de omisión activados:
→ [lista con pregunta correspondiente]

Acción: No continuar hasta resolver los hechos
faltantes críticos.
```

---

### INSTANCIA 0B — Detector de Cambio de Caso

**Qué hace:**
Monitorea si algún hecho narrado cambia fundamentalmente la naturaleza del proceso. Si lo detecta, se detiene y alerta antes de seguir.

**Ejemplos de hechos disruptivos:**

```
HECHO DISRUPTIVO 1
Descripción inicial: "Despido sin justa causa"
Hecho nuevo: "Al cliente le faltan 2 años para pensionarse"
→ ALERTA: Activa fuero de prepensionado
→ El caso ya no es indemnización — es reintegro obligatorio
→ La estrategia cambia completamente

HECHO DISRUPTIVO 2
Descripción inicial: "Conflicto de arrendamiento"
Hecho nuevo: "El inmueble tiene una familia
              con menores de edad y embarazada"
→ ALERTA: Activa protección reforzada
→ El proceso de restitución tiene restricciones
→ Puede requerirse intervención del ICBF

HECHO DISRUPTIVO 3
Descripción inicial: "Tutela de salud individual"
Hecho nuevo: "El cliente menciona que otros
              10 pacientes tienen la misma negativa"
→ ALERTA: Puede configurar afectación colectiva
→ Evaluar acción popular simultánea a la tutela
→ Mayor impacto y más difícil de ignorar para la EPS

HECHO DISRUPTIVO 4
Descripción inicial: "Cobro de deuda comercial"
Hecho nuevo: "El deudor está en proceso
              de insolvencia empresarial"
→ ALERTA: Cambia la jurisdicción y el proceso
→ No es proceso ejecutivo ordinario
→ Es reclamación en proceso de reorganización
```

**Output de 0B:**
```
⚡ ALERTA DE CAMBIO DE CASO

El hecho [X] que acaba de ingresar cambia
la naturaleza del proceso originalmente descrito.

Descripción original: [tipo de caso]
Nueva configuración: [tipo de caso ajustado]

Implicación principal: [qué cambia y por qué]

¿Desea reformular la estrategia?
→ SÍ: Lumi reinicia con la nueva configuración
→ NO: Lumi registra la alerta y continúa
      con advertencia visible
```

---

### INSTANCIA 0C — Estratega Inicial

**Qué hace:**
Antes de escribir una línea, valida que la acción seleccionada sea la más efectiva para los hechos del caso.

**Árbol de decisión estratégica:**

```
PREGUNTA 1: ¿Hay un derecho fundamental vulnerado
            de forma directa e inminente?
→ SÍ: Tutela (evaluar subsidiariedad)
→ NO: Continuar árbol

PREGUNTA 2: ¿Hay un acto administrativo ilegal?
→ SÍ con daño económico: Nulidad y restablecimiento
→ SÍ sin daño económico: Nulidad simple
→ NO: Continuar árbol

PREGUNTA 3: ¿Hay un daño causado por el Estado
            sin acto administrativo?
→ SÍ: Reparación directa
→ NO: Continuar árbol

PREGUNTA 4: ¿Hay un título ejecutivo claro?
→ SÍ: Proceso ejecutivo
→ NO: Proceso declarativo previo

PREGUNTA 5: ¿Hay derechos colectivos afectados?
→ SÍ: Acción popular (puede ser simultánea)
→ NO: Acción individual
```

**Validaciones adicionales del estratega:**

```
□ ¿Hay caducidad que revisar urgentemente?
  → Si vence en menos de 30 días: ALERTA ROJA
  → Si vence en 31-90 días: ALERTA AMARILLA

□ ¿Se agotó la vía gubernativa?
  → Si aplica y no se agotó: bloqueo procesal
  → Lumi genera el recurso de agotamiento primero

□ ¿Hay litispendencia?
  → ¿Existe proceso idéntico ya iniciado?
  → Si existe: riesgo de nulidad

□ ¿Hay cosa juzgada?
  → ¿Se resolvió este asunto antes?
  → Si existe: el caso no procede

□ ¿Hay conciliación prejudicial obligatoria?
  → Si aplica y no se realizó: inadmisión
  → Lumi genera la solicitud de conciliación primero
```

---

### INSTANCIA 0D — Mapa Probatorio

**Qué hace:**
Construye el inventario completo de pruebas por cada hecho relevante. Identifica qué existe, qué falta y qué es crítico conseguir antes de radicar.

**Estructura del mapa:**

```
MAPA PROBATORIO — CASO #001

HECHO 1: La EPS negó la cirugía
├── Prueba ideal: Comunicación escrita de la EPS
├── Prueba disponible: Relato del cliente (verbal)
├── Gap: ❌ No hay documento escrito
├── Acción: Derecho de petición para crear
│          el registro escrito antes de la tutela
└── Impacto en probabilidad si se consigue: +18 puntos

HECHO 2: El médico ordenó la cirugía
├── Prueba ideal: Orden médica firmada y fechada
├── Prueba disponible: Historia clínica parcial
├── Gap: ⚠️ La orden existe pero no menciona urgencia
├── Acción: Solicitar concepto médico actualizado
│          que incluya criterio de urgencia
└── Impacto en probabilidad si se consigue: +19 puntos

HECHO 3: El paciente es sujeto de especial protección
├── Prueba ideal: Documento que acredite la condición
├── Prueba disponible: Ninguna aportada aún
├── Gap: 🔍 ¿Es adulto mayor, tiene discapacidad,
│         está en situación de vulnerabilidad?
├── Acción: Preguntar al cliente en Fase 1
└── Impacto en probabilidad si aplica: +8 puntos

RESUMEN PROBATORIO
Hechos con prueba sólida: 0/3
Hechos con prueba parcial: 1/3
Hechos sin prueba: 2/3
Probabilidad actual base: 58%
Probabilidad con mapa completo: 91%
```

---

## FASE 1 — MOTOR DE PREGUNTAS CRÍTICAS

### El principio de esta fase

Las preguntas genéricas desperdician el tiempo del cliente y del abogado. Cada pregunta de Lumi existe porque su respuesta mueve la probabilidad de éxito del caso — hacia arriba o hacia abajo. Si una pregunta no mueve el caso, no se hace.

---

### INSTANCIA 1A — El Interrogador

**Qué hace:**
Genera el cuestionario estratégico que el abogado debe hacerle al cliente, ordenado por impacto en la probabilidad de éxito.

**Principio 1 — Cada pregunta tiene una razón jurídica explícita**

El sistema muestra al abogado la razón detrás de cada pregunta:

```
PREGUNTA (visible para el abogado):
"¿La negativa de la EPS fue por escrito
o fue verbal?"

RAZÓN INTERNA (visible para el abogado):
Si fue verbal → no hay acto administrativo →
la ruta es tutela por omisión + derecho de
petición previo para crear el expediente escrito.
Si fue escrita → hay acto administrativo recurrible
+ tutela simultánea posible.
La respuesta cambia la estrategia completa.
```

**Principio 2 — Ordenadas por impacto en probabilidad**

```
RANKING DE IMPACTO — TUTELA SALUD

Pregunta A: ¿Hay diagnóstico de urgencia vital?
→ Existe: probabilidad sube de 72% a 91% (+19)
→ No existe: probabilidad baja de 72% a 48% (-24)
IMPACTO TOTAL: 43 puntos → PRIMERA

Pregunta B: ¿La negativa fue escrita?
→ Existe: probabilidad sube de 72% a 79% (+7)
→ No existe: probabilidad baja de 72% a 61% (-11)
IMPACTO TOTAL: 18 puntos → SEGUNDA

Pregunta C: ¿Hay intentos previos documentados?
→ Existe: probabilidad sube de 72% a 76% (+4)
→ No existe: sin cambio
IMPACTO TOTAL: 4 puntos → QUINTA
```

**Las cuatro categorías de preguntas:**

```
🔴 URGENTES
Sin esta respuesta no se puede radicar.
El caso no avanza sin ella.
El sistema bloquea la generación del borrador
hasta tenerla o hasta que el abogado decida
conscientemente proceder sin ella.

🟡 IMPORTANTES
Su presencia fortalece significativamente.
Su ausencia debilita pero no bloquea.
El sistema recomienda conseguirlas pero permite continuar.

🟢 COMPLEMENTARIAS
Pueden marcar la diferencia en casos cerrados.
Útiles pero no determinantes.
El sistema las incluye como sugerencia.

⚡ PREGUNTA TRAMPA — siempre la última, siempre igual
"¿Hay algo que no le ha contado a nadie
sobre este caso — algo que quizás cree
que no importa, o que le da pena decir,
o que cree que podría perjudicarle?"

Esta pregunta no cambia. No se adapta por tipo de caso.
Se hace en todos los casos, siempre al final,
con exactamente ese tono.

Por qué funciona: libera al cliente de la vergüenza
de revelar algo que siente como admisión de culpa.
El 30% de los casos tienen un hecho crítico
que solo aparece con esta pregunta.
```

---

### INSTANCIA 1B — El Integrador

**Qué hace:**
Recibe las respuestas del cliente, las incorpora al mapa de hechos, detecta si generan nuevas preguntas y decide si se necesita una segunda ronda.

**Detección de segunda ronda:**

```
PABLO TRAE LA RESPUESTA:
"La EPS me dijo verbalmente que el servicio
no aplica porque no tengo el diagnóstico
principal actualizado."

LUMI DETECTA 3 PREGUNTAS NUEVAS:

Segunda ronda — Pregunta 1 🔴
"¿Cuándo fue la última actualización
del diagnóstico en la EPS?"
→ Razón: Si fue hace más de 6 meses hay
   negligencia de la EPS en el seguimiento
   que fortalece la tutela

Segunda ronda — Pregunta 2 🟡
"¿El médico tratante pertenece a la
red de la EPS o es externo?"
→ Razón: Determina quién tiene la carga
   de actualizar el diagnóstico

Segunda ronda — Pregunta 3 🟡
"¿La EPS ofreció alguna alternativa
o solución al servicio negado?"
→ Razón: Si no ofreció nada: omisión total
   que fortalece la tutela por falta de
   acompañamiento integral
```

**Criterio de cierre:**
El sistema declara los hechos completos cuando:
- Todos los items 🔴 están resueltos
- Al menos el 80% de los 🟡 están resueltos
- La pregunta trampa fue hecha y respondida
- No hay nuevas inconsistencias detectadas

---

## FASE 2 — MOTOR PROBABILÍSTICO

### El principio de esta fase

Una probabilidad sin explicación es inútil. Decirle al abogado "78% de éxito" sin decirle por qué y qué puede mover ese número es lo mismo que no decirle nada. El motor probabilístico calcula, explica y muestra la sensibilidad de cada variable.

---

### INSTANCIA 2A — El Calculador

**Variables ponderadas por tipo de caso:**

```
TUTELA (pesos)
├── Urgencia o conexidad con vida      30%
├── Precedente vinculante favorable    25%
├── Documentación de la negativa       20%
├── Sujeto de especial protección      15%
└── Historial de la entidad accionada  10%

PROCESO EJECUTIVO (pesos)
├── Calidad del título ejecutivo       45%
├── Cuantía clara y exigible           20%
├── Identificación del deudor          15%
├── Mora documentada                   15%
└── Bienes conocidos del deudor         5%

NULIDAD Y RESTABLECIMIENTO (pesos)
├── Ilegalidad clara del acto          35%
├── Caducidad verificada               25%
├── Agotamiento vía gubernativa        20%
├── Daño cuantificable                 15%
└── Precedente favorable               5%

LABORAL DESPIDO (pesos)
├── Modalidad del contrato             25%
├── Causa real vs causa alegada        30%
├── Documentación del despido          20%
├── Estabilidad reforzada aplicable    15%
└── Testigos o pruebas adicionales     10%
```

**Formato del árbol de escenarios:**

```
ANÁLISIS DE ESCENARIOS — CASO #001

RUTA RECOMENDADA: [acción principal]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESCENARIO 1 — ÓPTIMO (X%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
¿Qué pasa?: [descripción concreta]
¿Qué requiere?: [condición necesaria]

    Rama 1A (X% dentro del escenario):
    [descripción] → Acción: [qué hacer]

    Rama 1B (X% dentro del escenario):
    [descripción] → Acción: [qué hacer]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESCENARIO 2 — REALISTA (X%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
¿Qué pasa?: [descripción]
Ruta recomendada: [acción]
Probabilidad de éxito en esta ruta: X%
Plazo para actuar: [tiempo]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ESCENARIO 3 — ADVERSO (X%)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
¿Qué pasa?: [descripción]
Ruta de contingencia: [acción alternativa]
```

---

### INSTANCIA 2B — Análisis de Sensibilidad

**Qué hace:**
Muestra exactamente cómo se mueve la probabilidad según lo que pase en los próximos días. Le da al abogado información para decidir si espera o radica ya.

```
ANÁLISIS DE SENSIBILIDAD — CASO #001

SI el cliente consigue HOY el diagnóstico
actualizado con mención de urgencia vital:
→ Probabilidad sube de 72% a 91% (+19 puntos)
→ Vale la pena esperar 2-3 días

SI se radica HOY sin ese diagnóstico:
→ Probabilidad: 72%
→ Riesgo principal: negativa por falta de
   urgencia acreditada documentalmente

SI se solicita medida provisional:
→ Probabilidad de concesión de la medida: 68%
→ Si la medida se concede: probabilidad del
   fondo sube a 84%

RECOMENDACIÓN DEL SISTEMA:
Esperar 48 horas para conseguir el diagnóstico.
No hay caducidad inminente que justifique
la urgencia de radicar hoy.
La ganancia en probabilidad (+19 puntos) es
significativamente mayor que el riesgo de esperar.

UMBRAL DE DECISIÓN:
Si en 48 horas no se consigue el diagnóstico,
radicar con la estrategia de medida provisional.
```

---

## FASE 3 — REVISIÓN JURÍDICA

### El principio de esta fase

Un revisor jurídico genérico hace las mismas preguntas para todos los casos. Lumi tiene checklists específicos por tipo de proceso, nivel de riesgo diferenciado por argumento, y revisión del lenguaje procesal.

---

### INSTANCIA 3A — Revisor Jurídico Especializado

**Checklist específico por tipo de caso — Tutela:**

```
ELEMENTOS CONSTITUTIVOS
□ ¿Se identifica claramente el accionante y el accionado?
□ ¿Se precisa el derecho fundamental vulnerado
  con artículo constitucional exacto?
□ ¿Se describe la conducta vulneradora con
  fecha, actor y modalidad específica?
□ ¿Se acredita la inmediatez?
□ ¿Se demuestra subsidiariedad?
  (ausencia de mecanismo idóneo alternativo)
□ ¿Las pretensiones son claras, concretas
  y ejecutables por el juez?

ELEMENTOS QUE MATAN LA TUTELA
□ ¿Hay tutela previa sobre los mismos hechos?
  → Temeridad: puede rechazarse de plano
□ ¿El accionado es un particular sin
  relación de subordinación o servicio público?
  → Solo procede en casos taxativos
□ ¿La pretensión es una obligación de dar dinero?
  → Tutela no procede para cobros
□ ¿Hay otro mecanismo igual de efectivo
  que el cliente no ha agotado?

ELEMENTOS DE FORTALEZA
□ ¿Se cita la sentencia de unificación
  más reciente y favorable?
□ ¿Se usa precedente horizontal del mismo
  juzgado si existe y es favorable?
□ ¿Se solicita medida provisional si la
  urgencia lo justifica?
□ ¿El lenguaje permite que el juez entienda
  el caso sin conocer el expediente?
```

**Checklist específico — Proceso Ejecutivo:**

```
ELEMENTOS CONSTITUTIVOS
□ ¿El título ejecutivo está claramente identificado?
□ ¿La obligación es clara, expresa y exigible?
□ ¿La cuantía está determinada o es determinable?
□ ¿El deudor está correctamente identificado?
□ ¿La mora está documentada?

RIESGOS PROCESALES
□ ¿Prescribió la acción ejecutiva?
□ ¿El título ha sido novado o modificado?
□ ¿Hay excepciones previsibles del deudor?
  → Pago, compensación, prescripción, nulidad

MEDIDAS CAUTELARES
□ ¿Se solicitan medidas cautelares?
□ ¿Se identifican bienes del deudor?
□ ¿La caución es proporcional a la deuda?
```

**Revisión del argumento más débil:**

```
PUNTO MÁS DÉBIL IDENTIFICADO

[Descripción del argumento débil]

OPCIONES PARA REFORZARLO:

Opción A — Argumento jurídico puro
[Jurisprudencia o norma que lo soporta]
→ Viable pero expuesto a [contraargumento]

Opción B — Prueba adicional
[Prueba que reforzaría el punto]
→ Más sólida si se consigue en [plazo]

Opción C — Reformulación del argumento
[Cómo reencuadrar el punto]
→ Cambia el enfoque sin cambiar el fondo

RECOMENDACIÓN: [opción recomendada con razón]
```

**Revisión de comunicación jurídica:**

```
□ ¿El relato de hechos se entiende sin
  conocer el caso de antemano?
□ ¿Cada párrafo tiene una sola idea central?
□ ¿Los tecnicismos tienen explicación
  inmediata cuando son necesarios?
□ ¿Las pretensiones están numeradas
  e independientes entre sí?
□ ¿El juez puede resolver el caso solo
  con lo que está en el documento?
□ ¿El tono es respetuoso pero firme?
  (ni suplicante ni confrontacional)
```

---

## FASE 4 — VALIDACIÓN DE FUENTES

### El principio de esta fase

Las sentencias se citan mal de cuatro maneras distintas. Lumi detecta las cuatro. Citar mal una sentencia que el juez conoce destruye la credibilidad del escrito completo.

---

### INSTANCIA 4A — Validador de Fuentes (4 niveles)

```
NIVEL 1 — EXISTENCIA
¿Existe la sentencia con ese número exacto?
¿El M.P. indicado es correcto?
¿El año corresponde al número?

NIVEL 2 — VIGENCIA
¿Fue modificada por sentencia posterior?
¿Fue expresamente superada por una SU?
¿Sigue siendo la referencia más actual?
→ Si fue superada: indicar la sentencia vigente

NIVEL 3 — RATIO APLICADA
¿La ratio que se usa en el borrador
corresponde a lo que realmente dice la sentencia?
→ Error frecuente: simplificar la ratio
   de forma que puede ser atacada
→ Corrección: usar la ratio exacta
   con cita textual del aparte relevante

NIVEL 4 — JURISPRUDENCIA MÁS RECIENTE
¿Hay una sentencia posterior que dice
lo mismo con más fuerza o precisión?
→ Si existe: recomendar citar ambas
   (la fundacional y la más reciente)
```

**Los cuatro tipos de error de citación:**

```
ERROR TIPO 1 — El número no existe
T-999/25 → no hay ninguna sentencia con ese número
Severidad: Alta — pérdida de credibilidad total

ERROR TIPO 2 — Número correcto, M.P. incorrecto
T-760/08 existe pero el M.P. citado es otro
Severidad: Alta — el juez que conoce la sentencia
lo detecta inmediatamente

ERROR TIPO 3 — Sentencia superada
La ratio citada fue cambiada por una SU posterior
Severidad: Crítica — citar jurisprudencia superada
es peor que no citarla

ERROR TIPO 4 — Ratio mal atribuida
La sentencia existe pero se le atribuye
una ratio que corresponde a otro fallo
Severidad: Alta — el abogado contrario lo detecta
```

**Output de validación:**

```
TABLA DE VERIFICACIÓN — CASO #001

T-760/08 (M.P. Manuel José Cepeda)
├── Existencia: ✅ Confirmada
├── M.P.: ✅ Correcto
├── Vigencia: ⚠️ Precisada por T-248/23
├── Ratio aplicada: ⚠️ Simplificada — ver corrección
└── Más reciente: 🔄 Agregar T-248/23

Art. 49 C.P.
├── Existencia: ✅ Confirmada
├── Vigencia: ✅ Sin modificaciones
└── Aplicación: ✅ Correcta para este caso

Ley 1751/2015, Art. 6
├── Existencia: ✅ Confirmada
├── Vigencia: ✅ Vigente
└── Aplicación: ✅ Correcta
```

---

## FASE 5 — SIMULACIÓN ADVERSARIAL Y RIESGO

### El principio de esta fase

Simular la contraparte no es adivinar qué va a decir. Es construir el mejor argumento posible contra el caso — mejor incluso que el que construiría el abogado contrario promedio. Si el sistema no puede responder ese ataque, el borrador tiene un problema.

---

### INSTANCIA 5A — Abogado Contrario de Alto Nivel

**Los cinco ataques más comunes por tipo de caso — Tutela:**

```
ATAQUE 1 — Subsidiariedad
"Existen otros mecanismos: Supersalud, SIC."
→ Respuesta preparada: esos mecanismos no son
   idóneos por su lentitud vs la urgencia del caso
→ Cita: SU-961/99 sobre idoneidad del mecanismo

ATAQUE 2 — Falta de inmediatez
"La situación lleva meses sin actuación."
→ Respuesta preparada: vulneración continuada,
   no instantánea — la inmediatez se evalúa
   desde el último acto vulnerador
→ Cita: T-083/18 sobre inmediatez en
   vulneraciones continuadas

ATAQUE 3 — Servicio no cubierto
"No tenemos obligación de prestar
servicios por fuera del plan."
→ Respuesta preparada: principio de integralidad
   + T-760/08 + Ley 1751/2015 Art. 8

ATAQUE 4 — Falta de legitimación
"El accionante no agotó conducto regular interno."
→ Respuesta preparada: documentar que sí lo
   intentó o que el conducto es ineficaz

ATAQUE 5 — Hecho superado
"Durante el proceso se autorizó el servicio."
→ Respuesta preparada: el hecho superado
   no extingue la pretensión si hay riesgo
   de repetición + condena en costas
```

**El ataque no obvio:**

```
ATAQUE NO OBVIO — Lo que el abogado excepcional usaría

[Análisis del caso específico para identificar
el argumento inesperado que podría usar
un litigante de alto nivel]

Por qué es relevante: [explicación]

Cómo prepararse: [acción concreta]
```

---

### INSTANCIA 5B — Análisis de Nulidades Propias

```
REVISIÓN DE NULIDADES EN LA ACTUACIÓN PROPIA

□ ¿El poder está debidamente otorgado?
□ ¿La firma del cliente corresponde
  a su documento de identidad?
□ ¿El accionado está correctamente
  identificado con NIT o número legal?
□ ¿Se accionó a la entidad correcta?
  (EPS y no IPS, Ministerio y no DIAN, etc.)
□ ¿El juez al que se radica es el
  territorialmente competente?
□ ¿Se aportaron todas las pruebas
  mencionadas en el cuerpo del escrito?
□ ¿El formato cumple los requisitos
  del despacho específico?
□ ¿La cuantía declarada corresponde
  a las pretensiones?
```

---

## FASE 6 — PREGUNTAS FINALES AL ABOGADO

### El principio de esta fase

El afinador no hace preguntas que el sistema puede resolver solo. Solo eleva al abogado las decisiones que requieren criterio profesional, conocimiento del cliente, o juicio estratégico que va más allá del análisis jurídico.

**Máximo 3 preguntas. Siempre con contexto y opciones.**

```
DECISIÓN 1 — ESTRATÉGICA
[Descripción de la disyuntiva]
Opción A: [descripción] → consecuencia
Opción B: [descripción] → consecuencia
¿Cuál prefiere según su conocimiento
del cliente y la situación real?

DECISIÓN 2 — TÁCTICA
[Descripción del punto pendiente]
Contexto: [por qué importa]
Opciones: [A] o [B]
Información que solo el abogado tiene: [qué necesita saber]

DECISIÓN 3 — RELACIONAL
[Descripción de la decisión de comunicación]
Depende de: [perfil del cliente]
Recomendación del sistema: [opción sugerida]
¿Confirma o ajusta?
```

---

## FASE 7 — CONSISTENCIA Y MODO CLIENTE

### INSTANCIA 7A — Verificador de Consistencia Interna

```
VERIFICACIÓN CRUZADA COMPLETA

FECHAS
□ ¿Todas las fechas son internamente consistentes?
□ ¿Los plazos calculados cuadran con las fechas?
□ ¿La cronología narrada es lineal y sin saltos?

IDENTIDADES
□ ¿El nombre del cliente es idéntico en todo el documento?
□ ¿El nombre del accionado es idéntico y correcto?
□ ¿Los números de identificación cuadran en todo el doc?

ARGUMENTACIÓN
□ ¿Los hechos del encabezado no contradicen
  los hechos del cuerpo?
□ ¿Las pretensiones corresponden exactamente
  a los hechos narrados?
□ ¿Los argumentos jurídicos soportan
  todas las pretensiones?
□ ¿No hay pretensiones sin argumento
  ni argumentos sin pretensión?

FORMATO
□ ¿El formato cumple los requisitos del despacho?
□ ¿Los anexos están numerados y referenciados?
□ ¿La firma y datos del abogado son correctos?
```

### INSTANCIA 7B — Revisor del Modo Cliente

```
VALIDACIÓN DE LA CARTA AL CLIENTE

CLARIDAD
□ ¿Hay algún término técnico sin explicación?
□ ¿Cualquier persona sin formación jurídica
  puede entender qué pasó y qué sigue?

EXPECTATIVAS
□ ¿Las expectativas que genera son realistas?
□ ¿Se menciona la posibilidad de escenarios
  no favorables sin alarmar innecesariamente?

ACCIÓN
□ ¿Los pasos que le pide al cliente son
  concretos, específicos y realizables?
□ ¿Se especifica cuándo y cómo debe hacerlos?

TONO
□ ¿El tono es apropiado para este tipo de caso?
  → Tutela urgente: tono directo y de acción
  → Divorcio: tono empático y ordenado
  → Laboral: tono tranquilizador con plazos claros
  → Sucesión: tono neutral y sin dramatizar
```

---

## FASE FINAL — ENTREGABLE CERTIFICADO

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ CASO #001 — CERTIFICADO LUMI
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Semáforo general: 🟢
Probabilidad de éxito ruta óptima: X%

TRAZABILIDAD COMPLETA
✅ Hechos auditados — sin vacíos críticos
✅ Detector cambio de caso — sin alertas
✅ Estrategia validada antes de escribir
✅ Mapa probatorio construido
✅ Preguntas críticas respondidas
✅ Escenarios calculados con sensibilidad
✅ Revisión jurídica — X correcciones aplicadas
✅ Fuentes verificadas — X citas confirmadas
✅ Contraparte simulada — puntos reforzados
✅ Nulidades propias — sin riesgos detectados
✅ Decisiones del abogado integradas
✅ Consistencia interna — sin contradicciones
✅ Modo Cliente — validado y listo

ENTREGABLES
📄 Documento principal
📋 Checklist de pruebas pendientes
💬 Carta al cliente
📊 Reporte de escenarios
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## FASE 8 — CICLO DE VIDA POST-RADICACIÓN

### El principio de esta fase

El caso no termina cuando el abogado firma. Termina cuando el fallo queda en firme y se ejecuta. Lumi acompaña todo el ciclo.

---

### INSTANCIA 8A — Radar de Plazos

```
SISTEMA DE ESTADOS DEL EXPEDIENTE

ESTADO 1 — RADICADO
Esperando actuación del juez o contraparte
Lumi: monitorea plazo de respuesta

ESTADO 2 — RESPUESTA RECIBIDA
Contraparte o juez se pronunció
Lumi: análisis inmediato + recomendación

ESTADO 3 — ACTUACIÓN REQUERIDA
Hay un plazo que vence
Lumi: alerta + generación automática del documento

ESTADO 4 — EN ESPERA DE FALLO
Proceso en manos del juez
Lumi: monitorea plazo legal de decisión

ESTADO 5 — FALLO RECIBIDO
Lumi: análisis de 4 capas + recomendación

ESTADO 6 — EJECUCIÓN
Fallo favorable — hay que hacerlo cumplir
Lumi: seguimiento + desacato si incumplen

ESTADO 7 — CERRADO
Lumi: registro de resultado para
alimentar el motor probabilístico
```

**Alertas por urgencia:**

```
🔴 HOY — acción requerida inmediatamente
🟡 EN X DÍAS — preparación necesaria
🟢 EN X DÍAS — sin acción requerida aún
```

---

### INSTANCIA 8B — Analizador de Respuestas

**Qué hace:**
Cuando la contraparte o el juez se pronuncian, el abogado ingresa el documento y Lumi hace el análisis en tres capas:

```
CAPA 1 — ARGUMENTOS NUEVOS DE LA CONTRAPARTE
Por cada argumento nuevo:
→ ¿Es rebatible? ¿Cómo?
→ ¿Hay jurisprudencia que lo desvirtúa?
→ ¿Requiere prueba adicional para rebatirlo?

CAPA 2 — HECHOS NUEVOS QUE CAMBIAN EL CASO
¿La contraparte reveló algo que no sabíamos?
→ Si cambia la probabilidad: recalcular
→ Si activa el detector de cambio de caso: alertar

CAPA 3 — IMPACTO EN PROBABILIDAD
Probabilidad antes de la respuesta: X%
Probabilidad después de analizarla: Y%
Razón del cambio: [explicación]
```

---

### INSTANCIA 8C — Generador de Piezas Procesales Sucesivas

Cada nueva etapa genera un nuevo documento. Lumi lo genera con el contexto acumulado del caso — no parte de cero:

```
ETAPA                  DOCUMENTO
─────────────────────  ──────────────────────────────
Impugnación            Escrito de impugnación del fallo
Pruebas pedidas        Memorial aportando pruebas
Alegatos               Alegatos de conclusión
Incidente              Incidente de desacato
Segunda instancia      Memorial ante el superior
Ejecución fallo        Solicitud de cumplimiento
Liquidación            Liquidación de condena en costas
Cierre                 Acta de cierre del expediente
```

La ventaja: Lumi ya conoce todos los hechos, argumentos, pruebas y la respuesta de la contraparte. Cada documento nuevo es más preciso y más rápido que el anterior.

---

### INSTANCIA 8D — Analizador de Fallos

**Cuatro capas de lectura de cada fallo:**

```
CAPA 1 — ¿QUÉ DECIDIÓ EL JUEZ?
Lectura de la parte resolutiva:
→ ¿Concedió todo, parcialmente o negó?
→ ¿Hay condenas en costas?
→ ¿Hay órdenes específicas con plazos?
→ ¿Hay medidas de seguimiento?

CAPA 2 — ¿POR QUÉ LO DECIDIÓ?
Lectura de la parte motiva:
→ ¿Qué argumentos acogió el juez?
→ ¿Cuáles descartó y por qué?
→ ¿Hay dichos de paso útiles para el futuro?
→ ¿El juez usó jurisprudencia nueva?

CAPA 3 — ¿QUÉ SIGUE?
Si es favorable:
→ ¿Qué debe hacer la contraparte y cuándo?
→ ¿Cómo se monitorea el cumplimiento?
→ ¿Cuándo procede el desacato?
→ Lumi genera el memorial de seguimiento

Si es desfavorable:
→ ¿Vale la pena impugnar? (probabilidad calculada)
→ ¿Cuánto tiempo hay para impugnar?
→ ¿Hay argumentos nuevos para segunda instancia?
→ ¿Hay ruta alternativa si se pierde en segunda?
→ Lumi genera la impugnación si el abogado decide

CAPA 4 — ¿QUÉ APRENDEMOS?
→ ¿El resultado era el esperado?
→ Si no: ¿qué variable no se consideró?
→ ¿Cómo mejora el modelo para casos futuros?
```

---

### INSTANCIA 8E — Depósito de Inteligencia

**El mecanismo de mejora continua:**

Cada caso cerrado deposita aprendizaje en el sistema:

```
CASO CERRADO — DEPÓSITO

Tipo de caso: [categoría]
Argumentos centrales usados: [lista]
Juzgado / tribunal: [identificación]
Resultado: [ganado/perdido/parcial]
Tiempo de resolución: [días]
Factor determinante según el juez: [si está en el fallo]

APRENDIZAJE GENERADO:
En [tipo de caso] ante [tipo de juzgado]
en [ciudad], [argumento/prueba X] tiene
correlación de X% con [resultado Y]
en plazo promedio de [Z] días.

ACTUALIZACIÓN DEL SISTEMA:
→ Motor probabilístico: ajusta pesos de variables
→ Motor de preguntas: prioriza la pregunta
   sobre el factor determinante
→ Revisor jurídico: refuerza ese argumento
   específico en casos similares
→ Base de conocimiento: registra el precedente
   del juez específico si aplica
```

---

## TABLA MAESTRA — El sistema completo de principio a fin

| Fase | Instancia | Qué razona | QA aplicado | Output |
|------|-----------|-----------|-------------|--------|
| 0A | Auditor de hechos | Completitud, consistencia, omisiones | Checklist por tipo + patrones de omisión | Mapa de vacíos |
| 0B | Detector cambio de caso | ¿Este hecho cambia todo? | Alertas por hecho disruptivo | Alerta o confirmación |
| 0C | Estratega inicial | Acción correcta, caducidad, vía gubernativa | Árbol de decisión por área | Ruta recomendada |
| 0D | Mapa probatorio | Prueba por hecho, gaps probatorios | Cruce hecho-prueba-impacto | Inventario con gaps |
| 1A | Interrogador | Preguntas por impacto en probabilidad | Ranking de sensibilidad + patrones de omisión | Cuestionario categorizado |
| 1B | Integrador | ¿Las respuestas generan nuevas preguntas? | Detección de segunda ronda | Hechos completos |
| 2A | Calculador | Probabilidades ponderadas por tipo | Variables calibradas por área | Árbol de escenarios |
| 2B | Sensibilidad | ¿Qué mueve la probabilidad? | Simulación de variables | Recomendación táctica |
| — | Generador | Borrador sobre base sólida — calibración procesal, verificación numérica, documento híbrido (Sección A + Sección B) | Calibración por tipo/instancia/momento · Verificación numérica de cierre · Clasificación de argumentos adversariales por nivel de visibilidad | Borrador v1 híbrido |
| 3A | Revisor jurídico | Estrategia, argumentos, debilidades | Checklist específico por tipo de caso | Correcciones 🔴🟡🟢 |
| 3B | Corrección 1 | Aplicar correcciones | — | Borrador v2 |
| 4A | Validador fuentes | Existencia, vigencia, ratio, más reciente | 4 niveles por cita | Tabla ✅⚠️❌🔍 |
| 4B | Corrección 2 | Actualizar fuentes incorrectas | — | Borrador v3 |
| 5A | Abogado contrario | 5 ataques típicos + ataque no obvio | Respuesta preparada por ataque | Mapa de vulnerabilidades |
| 5B | Nulidades propias | Vicios en la actuación del abogado | Checklist de nulidades | Sin riesgos o alertas |
| 5C | Corrección 3 | Reforzar puntos débiles | — | Borrador v4 |
| 6A | Afinador | Solo lo irresoluble por el sistema | Máx. 3 preguntas con opciones | Decisiones del abogado |
| 6B | Ajuste final | Incorporar criterio del abogado | — | Borrador pre-final |
| 7A | Consistencia | Fechas, nombres, pretensiones, formato | Verificación cruzada interna | Doc limpio |
| 7B | Modo Cliente | Claridad, expectativas, tono | Validación por perfil del cliente | Carta validada |
| Final | Certificación | Ensamble y trazabilidad completa | Semáforo general | Paquete certificado |
| 8A | Radar de plazos | Actuaciones y vencimientos | Calendario procesal | Alertas activas |
| 8B | Analizador respuestas | Argumentos nuevos de contraparte | Cruce con estrategia propia | Análisis + recomendación |
| 8C | Generador sucesivo | Nueva pieza con contexto acumulado | Mismo flujo 7 fases con historial | Pieza procesual nueva |
| 8D | Analizador fallos | 4 capas de lectura | Árbol de decisión post-fallo | Ruta siguiente |
| 8E | Depósito inteligencia | Resultado para calibrar el sistema | Correlación resultado-variables | Mejora del modelo |

---

## LO QUE ESTE SISTEMA GARANTIZA

Un caso procesado por Lumi de principio a fin tiene:

- ✅ Hechos auditados antes de escribir
- ✅ Estrategia validada antes de escribir
- ✅ Pruebas mapeadas con sus gaps identificados
- ✅ Preguntas quirúrgicas al cliente ordenadas por impacto
- ✅ Probabilidad calculada con árbol de escenarios
- ✅ Sensibilidad de la probabilidad conocida
- ✅ Borrador calibrado al tipo de proceso, instancia y momento procesal
- ✅ Cifras verificadas contra el documento primario antes de generar
- ✅ Argumentos adversariales separados del borrador judicial — en Notas Internas
- ✅ Borrador revisado jurídicamente con checklist específico
- ✅ Todas las fuentes verificadas en 4 niveles
- ✅ Contraparte simulada con ataques preparados
- ✅ Nulidades propias verificadas
- ✅ Criterio del abogado integrado en los puntos que lo requieren
- ✅ Consistencia interna verificada
- ✅ Comunicación al cliente validada
- ✅ Seguimiento activo durante todo el proceso
- ✅ Análisis profundo de cada pronunciamiento del juez
- ✅ Inteligencia acumulada para mejorar casos futuros

Lo que el sistema no garantiza — y es honesto sobre ello:
- ❌ El resultado del caso (eso lo decide el juez)
- ❌ La calidad de los hechos que el cliente omitió
- ❌ El criterio final del abogado (es intransferible)

---

*Documento del motor de razonamiento — Lumi*
*Versión 2.0 — Abril 2026*
*Para principios conceptuales avanzados: LUMI_MOTOR_RAZONAMIENTO_AVANZADO_v2.md*
*Para prompts operativos por instancia: PROMPTS_POR_INSTANCIA_v3.md*