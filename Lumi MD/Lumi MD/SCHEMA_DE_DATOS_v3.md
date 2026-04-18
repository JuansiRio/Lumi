# 🗄️ SCHEMA DE DATOS — LUMI v2.0
### *Modelo de entidades jurídicamente fundado, epistémicamente riguroso y conforme a la Ley 1581 de 2012*

> Documento técnico-arquitectónico del sistema Lumi
> Autor: Felipe Cruz
> Versión 3.0 — Abril 2026 — Generalización de roles, campo abogado_fue_determinante
> **CONFIDENCIAL — Uso técnico interno**

---

## FUNDAMENTOS DE DISEÑO v2.0

### Por qué el v1.0 era insuficiente

El schema v1.0 cometía el error estructural más frecuente en sistemas de información jurídica: modelar el *proceso* como la unidad central en lugar del *asunto*, tratar las *normas* y los *precedentes* como texto en lugar de entidades, ignorar el *estatus epistémico* de los hechos individuales, y confundir el *tiempo del sistema* con el *tiempo jurídico*.

Esos no son errores técnicos menores — son errores que producen un sistema que aprende cosas incorrectas, no puede detectar conflictos de interés, no puede verificar vigencia normativa, y no puede distinguir entre un caso ganado sobre prueba sólida y uno ganado por factores externos al análisis.

El v2.0 parte de una premisa diferente: **el schema debe modelar la realidad jurídica tal como funciona, no tal como sería conveniente para una base de datos relacional.**

### Los siete principios de diseño del v2.0

```
PRINCIPIO 1 — El asunto precede al proceso
El asunto (la situación jurídica subyacente) puede generar
múltiples procesos. El schema modela ambos niveles.

PRINCIPIO 2 — Las normas y los precedentes son entidades
No son texto — tienen propiedades, relaciones, vigencia
temporal, y jerarquía. Se modelan como entidades propias.

PRINCIPIO 3 — Los hechos tienen estatus epistémico individual
Cada hecho sabe qué tan confiable es y por qué. No todos
los hechos son iguales epistemológicamente.

PRINCIPIO 4 — El tiempo jurídico tiene cuatro dimensiones
Tiempo de hechos, tiempo procesal, tiempo del sistema,
tiempo de vigencia normativa. Se modelan separadamente.

PRINCIPIO 5 — Las partes tienen roles, relaciones y conflictos
El modelo de partes soporta la complejidad real del litigio
colombiano: acciones colectivas, litisconsortes, comunidades,
y la detección estructural de conflictos de interés.

PRINCIPIO 6 — La privacidad distingue entre datos ordinarios
y datos sensibles (Ley 1581/2012). Los derechos del titular
son transacciones rastreables, no declaraciones de política.

PRINCIPIO 7 — La jurisdicción es una entidad, no un string.
Colombia tiene múltiples jurisdicciones con superposiciones
frecuentes. El schema las modela para aprender de ellas.
```

---

## PARTE I — CAPAS DE DATOS (actualización)

```
CAPA 0 — INFRAESTRUCTURA NORMATIVA Y JURISPRUDENCIAL
──────────────────────────────────────────────────────
Qué son: Normas y precedentes como entidades con propiedades.
Quién la gestiona: El arquitecto del sistema (actualizaciones) + sistema (queries).
Quién la consulta: Motor de razonamiento en cada caso.
Política: Permanente con versiones. Invalidación por derogación
          o superación jurisprudencial, nunca eliminación física.

CAPA 1 — DATOS IDENTIFICADOS DEL CLIENTE (PII)
Igual que v1.0, con adición de:
- Distinción entre datos ordinarios y datos sensibles
- Registro de derechos ejercidos por el titular
- Rastreo de consentimientos por propósito

CAPA 2 — DATOS DEL ASUNTO Y EL PROCESO
Nueva distinción: el asunto (situación subyacente) y el
proceso (la actuación judicial o administrativa específica).
Un asunto puede tener múltiples procesos.

CAPA 3 — HECHOS CON ESTATUS EPISTÉMICO
Cada hecho jurídico es una entidad individual con su
nivel de certeza, fuente, y estado de verificación.

CAPA 4 — PARTES Y SUS RELACIONES
Modelo rico de partes con roles, relaciones entre sí,
y mecanismo de detección de conflictos de interés.

CAPA 5 — JURISDICCIÓN Y TIEMPO JURÍDICO
Jurisdicción como entidad estructurada.
Tiempo jurídico en sus cuatro dimensiones.

CAPA 6 — INTELIGENCIA Y CALIBRACIÓN
Igual que v1.0 con mejoras al modelo causal.

CAPA 7 — COMUNIDADES (Especialidad étnico-territorial)
Entidades colectivas con derechos colectivos, estructura
de autoridad propia, y territorio.
```

---

## PARTE II — MODELO DE ENTIDADES

---

### BLOQUE A — INFRAESTRUCTURA NORMATIVA Y JURISPRUDENCIAL

#### ENTIDAD A1 — NORMA_JURIDICA

*Descripción: Las normas del ordenamiento colombiano como entidades con propiedades verificables.*

```sql
CREATE TABLE normas_juridicas (
  id_norma             UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Identificación formal
  tipo_norma           ENUM(
                         'constitucion',
                         'ley_organica',
                         'ley_estatutaria',
                         'ley_ordinaria',
                         'decreto_ley',
                         'decreto_reglamentario',
                         'decreto_compilatorio',
                         'resolucion',
                         'circular',
                         'acuerdo_municipal',
                         'tratado_internacional',
                         'convenio_oit'
                       ) NOT NULL,

  numero               VARCHAR(50),
  -- Ej: "1437", "2591", "169"

  anio                 SMALLINT,
  nombre_corto         VARCHAR(300),
  -- Ej: "CPACA", "Decreto de Tutela", "Convenio 169 OIT"

  nombre_completo      TEXT,
  entidad_expedidora   VARCHAR(200),

  -- Jerarquía
  nivel_jerarquico     SMALLINT NOT NULL,
  -- 1=Constitución/Bloque, 2=Leyes orgánicas/estatutarias,
  -- 3=Leyes ordinarias, 4=Decretos ley, 5=Decretos reglamentarios,
  -- 6=Resoluciones, 7=Circulares

  -- Vigencia temporal (crítica para análisis histórico)
  fecha_expedicion     DATE NOT NULL,
  fecha_vigencia_inicio DATE NOT NULL,
  -- Puede diferir de la fecha de expedición

  fecha_vigencia_fin   DATE,
  -- NULL si sigue vigente

  vigente              BOOL GENERATED ALWAYS AS (
    fecha_vigencia_fin IS NULL OR fecha_vigencia_fin > CURRENT_DATE
  ) STORED,

  -- Relaciones con otras normas
  deroga_a             UUID[] DEFAULT '{}',
  -- Array de id_norma que esta norma deroga

  modifica_a           UUID[] DEFAULT '{}',
  -- Array de id_norma que esta norma modifica

  es_derogada_por      UUID,
  -- FK a la norma que la derogó (si aplica)

  es_modificada_por    UUID[] DEFAULT '{}',
  -- Array de normas que la han modificado

  -- Artículos específicos frecuentemente citados
  articulos_clave      JSONB,
  -- [{"articulo": "86", "titulo": "Acción de Tutela",
  --   "texto_resumido": "...", "temas": ["tutela", "derechos_fundamentales"]}]

  -- Confianza en el registro
  verificado           BOOL DEFAULT FALSE,
  -- TRUE solo cuando el arquitecto verificó en suin-juriscol.gov.co
  url_fuente_oficial   TEXT,
  fecha_verificacion   DATE,

  creado_en            TS DEFAULT now(),
  actualizado_en       TS DEFAULT now()
);
```

**Por qué esta entidad es fundamental:**
Cuando el motor de razonamiento cita el Art. 86 C.P. en un caso de 2018, el sistema puede verificar que esa norma estaba vigente en 2018. Cuando una norma es derogada, el sistema puede alertar sobre todos los casos activos que la citan. Cuando la Instancia 4A produce el protocolo de verificación de fuentes, puede generar el link exacto a suin-juriscol.gov.co para cada norma.

---

#### ENTIDAD A2 — PRECEDENTE_JURISPRUDENCIAL

*Descripción: Las sentencias de las altas cortes como entidades con propiedades verificables, relaciones entre sí, y estatus epistémico del sistema.*

```sql
CREATE TABLE precedentes_jurisprudenciales (
  id_precedente        UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Identificación formal
  corte                ENUM(
                         'corte_constitucional',
                         'consejo_de_estado',
                         'corte_suprema_sala_civil',
                         'corte_suprema_sala_laboral',
                         'corte_suprema_sala_penal',
                         'tribunal_administrativo_caldas',
                         'otro_tribunal'
                       ) NOT NULL,

  tipo_sentencia       ENUM(
                         'T',   -- Tutela (CC)
                         'C',   -- Constitucionalidad (CC)
                         'SU',  -- Unificación (CC)
                         'A',   -- Auto (CC)
                         'SU_CE', -- Unificación Consejo de Estado
                         'CASACION',
                         'OTRO'
                       ) NOT NULL,

  numero               VARCHAR(20) NOT NULL,
  -- Ej: "760", "049", "123"

  anio                 SMALLINT NOT NULL,
  identificador_completo VARCHAR(50) GENERATED ALWAYS AS (
    tipo_sentencia || '-' || numero || '/' || anio::TEXT
  ) STORED,
  -- Ej: "T-760/08", "SU-049/17", "SU-123/18"

  magistrado_ponente   VARCHAR(200),
  -- Ej: "Manuel José Cepeda Espinosa"

  fecha_fallo          DATE,
  url_relatoría        TEXT,
  -- URL directa en corteconstitucional.gov.co o consejodeestado.gov.co

  -- Contenido jurídico
  temas                TEXT[],
  -- Ej: ARRAY['tutela_salud', 'sujeto_especial_proteccion']

  ratio_decidendi      TEXT,
  -- El holding vinculante — lo que el juez realmente decidió y por qué

  obiter_dicta         TEXT,
  -- Los dichos de paso — referenciales, no vinculantes

  regla_extraída       TEXT,
  -- La regla concreta que emerge de la ratio — para uso en argumentos

  -- Vigencia y relaciones jurisprudenciales
  vigente_como_precedente BOOL DEFAULT TRUE,

  superada_por         UUID REFERENCES precedentes_jurisprudenciales(id_precedente),
  -- La SU posterior que cambió la ratio

  aclara_a             UUID REFERENCES precedentes_jurisprudenciales(id_precedente),
  -- Si esta sentencia aclara otra

  normas_estudiadas    UUID[],
  -- Array de id_norma que esta sentencia interpretó

  -- Estatus epistémico del sistema sobre esta sentencia
  nivel_confianza_sistema ENUM(
                         'verificado_en_fuente_primaria',
                         'alta_confianza_entrenamiento',
                         'confianza_media',
                         'requiere_verificacion_externa'
                       ) NOT NULL DEFAULT 'confianza_media',

  verificado_por_pablo BOOL DEFAULT FALSE,
  fecha_verificacion_pablo DATE,
  notas_verificacion   TEXT,

  -- Efectividad observada en el circuito
  efectividad_circuito JSONB,
  -- [{"circuito": "Riosucio, Caldas", "tipo_caso": "tutela_salud",
  --   "evaluacion": "muy_efectivo|efectivo|neutral|poco_efectivo",
  --   "observacion": "...", "casos_base": [id_caso_anonimo]}]

  creado_en            TS DEFAULT now(),
  actualizado_en       TS DEFAULT now()
);
```

---

#### ENTIDAD A3 — CITA_JURIDICA

*Descripción: El vínculo entre un documento generado y las normas/precedentes que cita. Permite rastrear el uso y la efectividad de cada cita.*

```sql
CREATE TABLE citas_juridicas (
  id_cita              UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  documento_id         UUID NOT NULL REFERENCES documentos_generados(id_documento),
  caso_id              UUID NOT NULL REFERENCES casos(id_caso),

  -- Qué se cita
  tipo_fuente          ENUM('norma', 'precedente') NOT NULL,
  norma_id             UUID REFERENCES normas_juridicas(id_norma),
  precedente_id        UUID REFERENCES precedentes_jurisprudenciales(id_precedente),
  -- Exactamente uno de los dos debe ser NOT NULL

  -- Cómo se cita
  uso_en_documento     ENUM(
                         'fundamento_principal',
                         'fundamento_complementario',
                         'distinguible',
                         'referencia_contextual'
                       ) NOT NULL,

  parte_del_fallo_usada ENUM(
                         'ratio_decidendi',
                         'obiter_dicta',
                         'parte_resolutiva',
                         'norma_completa',
                         'articulo_especifico'
                       ),

  articulo_especifico  VARCHAR(50),
  -- Si es una norma, el artículo específico citado

  -- Estatus de verificación
  verificado_en_fuente BOOL DEFAULT FALSE,
  fecha_verificacion   DATE,
  verificado_por       ENUM('pablo_hoyos', 'sistema_lumi'),

  -- Resultado: ¿el juez acogió este argumento?
  acogido_por_juez     BOOL,
  -- NULL hasta que haya fallo. TRUE si el juez lo usó en su decisión.

  creado_en            TS DEFAULT now()
);
```

**Por qué esta entidad cierra el loop de aprendizaje:**
Con `CITAS_JURIDICAS`, el sistema puede responder preguntas como: "¿Cuál es la tasa de acogimiento de la SU-049/17 en el Juzgado Laboral del Circuito de Riosucio?" o "¿Cuáles son los artículos del CPACA que los jueces más frecuentemente rechazan como fundamento?" Eso convierte el depósito de inteligencia en aprendizaje jurisprudencial real.

---

### BLOQUE B — ASUNTO Y PROCESO

#### ENTIDAD B1 — ASUNTO

*Descripción: La situación jurídica subyacente del cliente. Puede generar múltiples procesos. Permite relacionar casos que emergen de la misma situación.*

```sql
CREATE TABLE asuntos (
  id_asunto            UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  id_asunto_anonimo    UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
  abogado_id           UUID NOT NULL REFERENCES abogados(id_abogado),

  descripcion_breve    VARCHAR(500),
  -- Descripción concisa de la situación subyacente (anonimizada)

  -- Dimensiones del asunto (puede tener varias simultáneamente)
  dimensiones          JSONB NOT NULL,
  -- {"laboral": true, "penal": false, "administrativo": true,
  --  "etnico_territorial": false, "victimas_conflicto": false,
  --  "internacional_ddhh": false}

  -- Estado general del asunto
  estado               ENUM(
                         'activo_sin_proceso',
                         'activo_con_procesos',
                         'cerrado_resuelto',
                         'cerrado_sin_resolucion'
                       ) DEFAULT 'activo_sin_proceso',

  -- Detección de conflicto de interés (en el asunto, no en el proceso)
  conflicto_interes_verificado BOOL DEFAULT FALSE,
  conflicto_interes_resultado  ENUM('limpio', 'advertencia', 'conflicto_real'),

  -- Metadatos
  fecha_apertura       DATE NOT NULL DEFAULT CURRENT_DATE,
  fecha_cierre         DATE,
  creado_en            TS DEFAULT now()
);

-- Vínculo privado: asunto <-> cliente (en private_schema)
CREATE TABLE asunto_cliente_vinculo (
  id_asunto            UUID NOT NULL REFERENCES asuntos(id_asunto),
  id_cliente           UUID NOT NULL REFERENCES clientes(id_cliente),
  rol_en_asunto        ENUM(
                         'afectado_principal',
                         'familiar_afectado',
                         'representante_legal',
                         'miembro_comunidad',
                         'comunidad_representada'
                       ) NOT NULL,
  PRIMARY KEY (id_asunto, id_cliente)
);
```

---

#### ENTIDAD B2 — PROCESO (anteriormente CASO)

*Descripción: Una actuación judicial o administrativa específica dentro de un asunto. Múltiples procesos pueden pertenecer al mismo asunto.*

```sql
CREATE TABLE procesos (
  id_proceso           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  id_proceso_anonimo   UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),
  asunto_id            UUID NOT NULL REFERENCES asuntos(id_asunto),
  abogado_id           UUID NOT NULL REFERENCES abogados(id_abogado),

  -- Clasificación jurídica detallada
  tipo_accion          ENUM(
    -- Constitucional
    'tutela', 'accion_popular', 'accion_grupo', 'cumplimiento',
    -- Contencioso-administrativa
    'nulidad_simple', 'nulidad_restablecimiento', 'reparacion_directa',
    'contractual', 'electoral', 'extension_jurisprudencia',
    -- Civil / Comercial
    'ejecutivo', 'ordinario_declarativo', 'verbal', 'verbal_sumario',
    'insolvencia', 'liquidacion',
    -- Laboral
    'ordinario_laboral', 'fuero_sindical', 'fuero_sindical_desafuero',
    -- Familia
    'divorcio', 'alimentos', 'custodia', 'adopcion', 'filiacion',
    -- Penal
    'denuncia_penal', 'victima_proceso_penal',
    -- Disciplinario
    'queja_disciplinaria_procuraduria', 'queja_etica_profesional',
    -- Especiales
    'restitucion_tierras', 'jep_sometimiento', 'consulta_previa_admin',
    'recurso_reposicion', 'recurso_apelacion', 'recurso_queja',
    'derecho_de_peticion', 'solicitud_conciliacion_prejudicial',
    'otro'
  ) NOT NULL,

  -- Estado y fase
  estado               ENUM(
    'en_analisis', 'en_produccion', 'radicado',
    'en_audiencia', 'en_espera_fallo', 'fallado_primera_instancia',
    'impugnado', 'fallado_segunda_instancia', 'en_casacion',
    'en_ejecucion', 'cerrado_favorable', 'cerrado_parcial',
    'cerrado_desfavorable', 'cerrado_conciliacion',
    'cerrado_desistimiento', 'abandonado'
  ) DEFAULT 'en_analisis',

  fase_motor_razonamiento ENUM(
    'fase_0_etica', 'fase_0_auditoria', 'fase_0_estrategia',
    'fase_0_probatorio', 'fase_1_preguntas', 'fase_1_integracion',
    'fase_15_narrativa', 'fase_2_probabilidad', 'fase_2_jurisdiccional',
    'generacion_borrador', 'fase_3_revision', 'fase_4_fuentes',
    'fase_5_adversarial', 'fase_6_afinador', 'fase_7_consistencia',
    'fase_final_certificacion', 'fase_8_post_radicacion'
  ) DEFAULT 'fase_0_etica',

  -- Jurisdicción (entidad, no string)
  jurisdiccion_id      UUID REFERENCES jurisdicciones(id_jurisdiccion),
  despacho_especifico  VARCHAR(300),

  -- Procesos relacionados en el mismo asunto
  proceso_principal_id UUID REFERENCES procesos(id_proceso),
  -- NULL si este es el proceso principal. Lleno si es subsidiario.

  tipo_relacion_proceso ENUM(
    'proceso_principal',
    'proceso_paralelo_complementario',
    'proceso_penal_simultáneo',
    'proceso_disciplinario_simultáneo',
    'segunda_instancia_de',
    'casacion_de',
    'ejecucion_de'
  ),

  -- Resultado económico (nuevo en v2.0)
  cuantia_pretendida   DECIMAL(18,2),
  cuantia_obtenida     DECIMAL(18,2),
  tasa_recuperacion    DECIMAL(5,2) GENERATED ALWAYS AS (
    CASE WHEN cuantia_pretendida > 0 AND cuantia_obtenida IS NOT NULL
    THEN (cuantia_obtenida / cuantia_pretendida) * 100
    ELSE NULL END
  ) STORED,

  honorarios_pactados  DECIMAL(18,2),
  gastos_procesales    DECIMAL(18,2),

  -- Resultado procesal
  resultado_nivel      SMALLINT CHECK (resultado_nivel BETWEEN 0 AND 5),
  resultado_descripcion TEXT,

  -- Tiempo jurídico (cuatro dimensiones — nuevo en v2.0)
  fecha_hechos_inicio  DATE,
  -- Cuándo comenzaron los hechos jurídicamente relevantes
  fecha_hechos_fin     DATE,
  -- Cuándo terminaron (puede ser ongoing para vulneraciones continuadas)
  fecha_apertura_proceso DATE NOT NULL DEFAULT CURRENT_DATE,
  fecha_radicacion     DATE,
  -- Cuándo se radicó el documento principal
  fecha_cierre         DATE,
  tiempo_resolucion_dias INT GENERATED ALWAYS AS (
    CASE WHEN fecha_cierre IS NOT NULL AND fecha_radicacion IS NOT NULL
    THEN fecha_cierre - fecha_radicacion ELSE NULL END
  ) STORED,

  -- Urgencia y caducidad
  fecha_caducidad      DATE,
  -- La fecha real, no un flag
  dias_para_caducidad  INT GENERATED ALWAYS AS (
    CASE WHEN fecha_caducidad IS NOT NULL
    THEN fecha_caducidad - CURRENT_DATE ELSE NULL END
  ) STORED,

  nivel_urgencia       ENUM('critico', 'urgente', 'proximo', 'normal')
                         GENERATED ALWAYS AS (
    CASE
      WHEN fecha_caducidad - CURRENT_DATE <= 3  THEN 'critico'
      WHEN fecha_caducidad - CURRENT_DATE <= 15 THEN 'urgente'
      WHEN fecha_caducidad - CURRENT_DATE <= 60 THEN 'proximo'
      ELSE 'normal'
    END
  ) STORED,

  creado_en            TS DEFAULT now(),
  modificado_en        TS DEFAULT now()
);
```

---

### BLOQUE C — HECHOS CON ESTATUS EPISTÉMICO

#### ENTIDAD C1 — HECHO_JURIDICO

*Descripción: Cada hecho jurídicamente relevante del caso como entidad individual con su propio estatus epistémico.*

*Fundamento: La epistemología jurídica distingue entre el factum probans (el hecho probatorio que acredita) y el factum probandum (el hecho a probar). Tratar todos los hechos con el mismo estatus epistémico produce análisis de probabilidad incorrecto y documentos con argumentos de diferente solidez presentados como iguales.*

```sql
CREATE TABLE hechos_juridicos (
  id_hecho             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proceso_id           UUID NOT NULL REFERENCES procesos(id_proceso),

  -- Identificación y clasificación
  descripcion          TEXT NOT NULL,
  -- El hecho en términos jurídicamente relevantes

  categoria            ENUM(
    'hecho_constitutivo',      -- Que funda la pretensión
    'hecho_impeditivo',        -- Que podría bloquear la pretensión
    'hecho_extintivo',         -- Que extinguiría el derecho
    'hecho_modificativo',      -- Que cambia el alcance del derecho
    'hecho_agravante',         -- Que aumenta la responsabilidad
    'hecho_atenuante'          -- Que reduce la responsabilidad
  ) NOT NULL,

  -- Tiempo jurídico del hecho
  fecha_ocurrencia     DATE,
  -- Cuándo ocurrió el hecho
  fecha_conocimiento   DATE,
  -- Cuándo el afectado tuvo conocimiento (relevante para caducidad)
  es_hecho_continuo    BOOL DEFAULT FALSE,
  -- TRUE para vulneraciones que persisten en el tiempo

  -- ESTATUS EPISTÉMICO (el corazón de esta entidad)
  fuente_del_hecho     ENUM(
    'declaracion_cliente',     -- El cliente lo dijo, sin verificar
    'documento_aportado',      -- Hay documento que lo acredita
    'documento_publico',       -- Documento de registro público verificable
    'inferencia_de_otros',     -- Se infiere de otros hechos
    'reconocimiento_contraparte', -- La contraparte lo admitió
    'perito',                  -- Un perito lo constató
    'inspeccion_ocular',       -- Verificación directa
    'conocimiento_del_abogado' -- el abogado activo lo sabe por su práctica
  ) NOT NULL,

  nivel_certeza        ENUM(
    'probado',           -- Acreditado por prueba documental o pericial
    'verosimil',         -- Consistente con otros hechos probados
    'declarado',         -- Dicho por el cliente, no verificado
    'inferido',          -- Deducido de otros hechos
    'disputado',         -- La contraparte lo niega
    'desconocido'        -- No se sabe si ocurrió
  ) NOT NULL,

  prueba_que_lo_acredita JSONB,
  -- [{"tipo": "carta_escrita", "descripcion": "Carta de la EPS de fecha X",
  --   "en_poder_de": "cliente|pablo|expediente|entidad"}]

  -- Verificación requerida
  requiere_verificacion BOOL DEFAULT FALSE,
  verificacion_completada BOOL DEFAULT FALSE,
  accion_para_verificar TEXT,
  -- Ej: "Solicitar a la EPS la historia clínica mediante derecho de petición"

  -- Vulnerabilidad adversarial
  atacable_por_contraparte BOOL DEFAULT FALSE,
  forma_de_ataque_probable TEXT,
  -- Alimenta la simulación adversarial (Fase 5)

  -- Norma o precedente aplicable a este hecho específico
  norma_aplicable_id   UUID REFERENCES normas_juridicas(id_norma),
  precedente_aplicable_id UUID REFERENCES precedentes_jurisprudenciales(id_precedente),

  creado_en            TS DEFAULT now(),
  actualizado_en       TS DEFAULT now()
);
```

---

### BLOQUE D — PARTES Y CONFLICTO DE INTERÉS

#### ENTIDAD D1 — PARTE

*Descripción: Cualquier actor con rol en un proceso — demandante, demandado, interviniente, testigo, perito, juez.*

```sql
CREATE TABLE partes (
  id_parte             UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Tipo de actor
  tipo_actor           ENUM(
    'persona_natural', 'persona_juridica_privada',
    'entidad_publica', 'comunidad_etnica', 'otro'
  ) NOT NULL,

  -- Identificación (anonimizada — PII en private_schema)
  nombre_anonimo       VARCHAR(300),
  -- Nombre sin datos que identifiquen al cliente si es contraparte
  -- Para contrapartes: nombre real (no son clientes del sistema)
  -- Para clientes: referencia al id_cliente en private_schema

  tipo_identificacion  ENUM('NIT', 'CC', 'colectivo', 'otro'),
  numero_identificacion VARCHAR(30),

  -- Para entidades: nombre oficial y tipo
  tipo_entidad         VARCHAR(100),
  -- Ej: "EPS", "Empleador", "Ministerio", "Municipio"

  -- Para comunidades: referencia a ENTIDAD G (comunidades)
  comunidad_id         UUID REFERENCES comunidades(id_comunidad),

  -- Patrón de comportamiento procesal (para contrapartes recurrentes)
  es_contraparte_recurrente BOOL DEFAULT FALSE,
  contraparte_id       UUID REFERENCES contrapartes(id_contraparte),

  -- Relaciones con otras partes (para detección de conflicto)
  relaciones           JSONB,
  -- [{"id_parte_relacionada": "uuid", "tipo_relacion": "familiar|socio|empleador",
  --   "descripcion": "..."}]

  creado_en            TS DEFAULT now()
);

-- Rol de cada parte en cada proceso
CREATE TABLE parte_proceso (
  id_parte             UUID NOT NULL REFERENCES partes(id_parte),
  id_proceso           UUID NOT NULL REFERENCES procesos(id_proceso),

  rol                  ENUM(
    'demandante_principal', 'codemandante', 'demandante_grupo',
    'demandado_principal', 'codemandado', 'litisconsorte_necesario',
    'litisconsorte_facultativo', 'interviniente_coadyuvante',
    'interviniente_ad_excludendum', 'llamado_en_garantia',
    'tercero_perjudicado', 'ministerio_publico',
    'testigo', 'perito', 'juez_ponente', 'juez_ad_quem'
  ) NOT NULL,

  fecha_vinculacion    DATE NOT NULL,
  activo               BOOL DEFAULT TRUE,

  PRIMARY KEY (id_parte, id_proceso, rol)
);
```

---

#### ENTIDAD D2 — CONFLICTO_DE_INTERES

*Descripción: Registro de la verificación de conflictos de interés. Implementa la detección estructural como función del sistema.*

*Fundamento: El Código Disciplinario del Abogado (Ley 1123 de 2007, Art. 34) establece la prohibición de representar intereses contrarios. La detección debe ser proactiva, no reactiva.*

```sql
CREATE TABLE conflictos_interes (
  id_conflicto         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proceso_id           UUID NOT NULL REFERENCES procesos(id_proceso),
  asunto_id            UUID NOT NULL REFERENCES asuntos(id_asunto),

  verificacion_ejecutada_en TS NOT NULL DEFAULT now(),

  -- Resultado de la verificación
  resultado            ENUM(
    'sin_conflicto',
    'conflicto_potencial_advertencia',
    'conflicto_real_bloqueo'
  ) NOT NULL,

  -- Si hay conflicto, descripción
  descripcion_conflicto TEXT,
  -- Ej: "{abogado} representó a Empresa X en caso laboral en 2022.
  --      Empresa X es ahora la contraparte en este proceso."

  -- Qué se verificó
  verificaciones_realizadas JSONB NOT NULL,
  -- {"representacion_anterior_contraparte": "verificado_sin_conflicto",
  --  "relacion_financiera_contraparte": "verificado_sin_conflicto",
  --  "cargo_publico_incompatible": "no_aplica",
  --  "asesor_previo_de_contraparte": "verificado_sin_conflicto",
  --  "familiar_parte_contraria": "verificado_sin_conflicto"}

  -- Decisión
  decision             ENUM('continuar', 'continuar_con_advertencia', 'no_continuar'),
  decision_de          ENUM('sistema_lumi', 'pablo_hoyos') NOT NULL,
  razon_decision       TEXT,

  creado_en            TS DEFAULT now()
);
```

---

### BLOQUE E — JURISDICCIÓN

#### ENTIDAD E1 — JURISDICCION

*Descripción: Las jurisdicciones colombianas como entidades con sus características, competencias, y patrones documentados.*

```sql
CREATE TABLE jurisdicciones (
  id_jurisdiccion      UUID PRIMARY KEY DEFAULT gen_random_uuid(),

  -- Clasificación
  tipo_jurisdiccion    ENUM(
    'ordinaria_civil',
    'ordinaria_laboral',
    'ordinaria_penal',
    'ordinaria_familia',
    'contencioso_administrativa',
    'constitucional',
    'jep',
    'restitucion_tierras',
    'especial_indigena',
    'arbitral',
    'conciliacion'
  ) NOT NULL,

  instancia            ENUM(
    'primera_instancia',
    'segunda_instancia',
    'casacion_revision',
    'unica_instancia'
  ) NOT NULL,

  -- Despacho específico
  nombre_despacho      VARCHAR(300) NOT NULL,
  ciudad               VARCHAR(100) NOT NULL,
  departamento         VARCHAR(100) NOT NULL,
  circuito             VARCHAR(100),

  -- Contacto y acceso
  direccion_fisica     VARCHAR(300),
  requiere_radicacion_fisica BOOL DEFAULT TRUE,
  acepta_radicacion_electronica BOOL DEFAULT FALSE,

  -- Conocimiento acumulado sobre este despacho
  -- (Alimentado por la Fase 2 del onboarding y por casos reales)
  conocimiento_pablo   JSONB,
  -- {"posicion_tutelas_salud": "favorable|neutral|desfavorable",
  --  "posicion_fuero_prepensionado": "...",
  --  "tiempo_promedio_tutela_dias": 10,
  --  "practicas_especificas": ["Requiere poder especial incluso para tutela"],
  --  "fuente": "pablo_experiencia_directa",
  --  "ultima_actualizacion": "2026-04-01"}

  -- Estadísticas acumuladas del sistema
  total_procesos_registrados INT DEFAULT 0,
  tasa_resultado_favorable DECIMAL(5,2),
  -- Se actualiza por trigger al cerrar procesos
  tiempo_promedio_resolucion_dias INT,

  activo               BOOL DEFAULT TRUE,
  creado_en            TS DEFAULT now(),
  actualizado_en       TS DEFAULT now()
);

-- Tabla de competencias concurrentes
-- Para casos donde hay superposición jurisdiccional
CREATE TABLE competencias_concurrentes (
  proceso_id           UUID NOT NULL REFERENCES procesos(id_proceso),
  jurisdiccion_id      UUID NOT NULL REFERENCES jurisdicciones(id_jurisdiccion),
  tipo_competencia     ENUM(
    'principal', 'subsidiaria', 'concurrente', 'potencial'
  ) NOT NULL,
  razon                TEXT,
  PRIMARY KEY (proceso_id, jurisdiccion_id)
);
```

---

### BLOQUE F — PRIVACIDAD CONFORME A LEY 1581/2012

#### ENTIDAD F1 — CONSENTIMIENTO_TRATAMIENTO

*Descripción: Registro granular de consentimientos por tipo de dato y propósito. Implementa purpose limitation y el derecho de revocatoria del titular.*

*Fundamento: La Ley 1581/2012, el Decreto 1377/2013 (ahora Decreto 1074/2015 Parte 2, Título 2), y los conceptos de la SIC (Superintendencia de Industria y Comercio) exigen que el consentimiento sea previo, expreso, informado, y revocable para cada propósito de tratamiento.*

```sql
CREATE TABLE consentimientos_tratamiento (
  id_consentimiento    UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cliente_id           UUID NOT NULL REFERENCES clientes(id_cliente),

  -- Propósito específico del tratamiento
  proposito            ENUM(
    'prestacion_servicio_juridico',    -- Propósito principal
    'datos_salud_tutela',              -- Dato sensible — requiere consentimiento adicional
    'datos_origen_etnico',             -- Dato sensible
    'datos_condicion_discapacidad',    -- Dato sensible
    'sistema_calibracion_anonimizado', -- Uso del caso (anonimizado) para calibrar el sistema
    'comunicaciones_comerciales'       -- Propósito secundario
  ) NOT NULL,

  -- Estado del consentimiento
  estado               ENUM(
    'otorgado', 'revocado', 'expirado'
  ) NOT NULL DEFAULT 'otorgado',

  -- Evidencia del consentimiento
  fecha_otorgamiento   TS NOT NULL,
  medio_otorgamiento   ENUM(
    'formulario_digital_firmado',
    'firma_fisica_digitalizada',
    'grabacion_verbal_con_testigo'
  ) NOT NULL,
  texto_exacto_firmado TEXT NOT NULL,
  -- El texto exacto al que el titular consintió, con versión del documento

  -- Revocatoria
  fecha_revocacion     TS,
  motivo_revocacion    TEXT,
  acciones_post_revocacion JSONB,
  -- Qué datos se anonimizaron o eliminaron tras la revocatoria
  -- y cuándo se ejecutaron esas acciones

  -- Datos sensibles requieren constancia adicional
  es_dato_sensible     BOOL GENERATED ALWAYS AS (
    proposito IN ('datos_salud_tutela', 'datos_origen_etnico',
                  'datos_condicion_discapacidad')
  ) STORED,

  consentimiento_especial_dato_sensible BOOL DEFAULT FALSE,
  -- Debe ser TRUE para datos sensibles. El sistema lo valida.

  creado_en            TS DEFAULT now()
);
```

---

#### ENTIDAD F2 — DERECHO_TITULAR_EJERCIDO

*Descripción: Registro de cada vez que un cliente ejerce sus derechos como titular de datos (acceso, corrección, supresión, portabilidad, revocatoria). La Ley 1581 obliga a responder en plazos específicos.*

```sql
CREATE TABLE derechos_titular_ejercidos (
  id_solicitud         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  cliente_id           UUID NOT NULL REFERENCES clientes(id_cliente),

  tipo_derecho         ENUM(
    'acceso',          -- Conocer qué datos se tratan (Art. 8a Ley 1581)
    'correccion',      -- Corregir datos inexactos (Art. 8b)
    'supresion',       -- Eliminar datos (Art. 8c)
    'revocatoria',     -- Revocar el consentimiento (Art. 8d)
    'queja_sic'        -- Queja ante la SIC (Art. 8f)
  ) NOT NULL,

  fecha_solicitud      TS NOT NULL,
  descripcion          TEXT NOT NULL,

  -- Plazo legal de respuesta (Art. 14 Ley 1581)
  fecha_limite_respuesta TS GENERATED ALWAYS AS (
    CASE tipo_derecho
      WHEN 'queja_sic' THEN fecha_solicitud + INTERVAL '15 days'
      ELSE fecha_solicitud + INTERVAL '10 days'
    END
  ) STORED,

  -- Gestión de la respuesta
  estado               ENUM(
    'pendiente', 'en_gestion', 'respondido', 'vencido_sin_respuesta'
  ) DEFAULT 'pendiente',

  fecha_respuesta      TS,
  respuesta_dada       TEXT,
  acciones_tomadas     JSONB,
  -- Qué se hizo en el sistema como consecuencia de la solicitud

  respondido_por       ENUM('felipe_cruz', 'pablo_hoyos'),
  creado_en            TS DEFAULT now()
);
```

---

#### ENTIDAD F3 — TRANSFERENCIA_DATOS

*Descripción: Registro de cada envío de datos al proveedor de IA (Claude/Anthropic). Documenta exactamente qué se envió, cuándo, y qué garantías aplican.*

*Fundamento: El Art. 26 de la Ley 1581 regula las transferencias internacionales de datos. Anthropic tiene servidores en EE.UU. Si el procesamiento ocurre fuera de Colombia, aplican las disposiciones sobre transferencias internacionales. Este registro es la evidencia del cumplimiento.*

```sql
CREATE TABLE transferencias_datos_ia (
  id_transferencia     UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proceso_id           UUID NOT NULL REFERENCES procesos(id_proceso),

  -- Qué se transfirió
  tipo_datos_enviados  ENUM(
    'hechos_anonimizados',
    'analisis_juridico',
    'borrador_para_revision',
    'cuestionario_preguntas'
  ) NOT NULL,

  id_caso_anonimo_enviado UUID NOT NULL,
  -- El id_anonimo que se usó — nunca el id real

  datos_no_incluidos   TEXT NOT NULL,
  -- Confirmación explícita de qué NO se envió
  -- Ej: "No se incluyó: nombre del cliente, número de ID,
  --      contacto, ni ningún dato identificador"

  -- Marco de la transferencia
  proveedor_ia         VARCHAR(100) DEFAULT 'Anthropic (Claude)',
  pais_servidor        VARCHAR(100) DEFAULT 'Estados Unidos',
  garantias_contractuales TEXT,
  -- Referencia a los términos de servicio de Anthropic que aplican

  -- Consentimiento aplicable
  consentimiento_id    UUID REFERENCES consentimientos_tratamiento(id_consentimiento),
  -- El consentimiento que autoriza este tratamiento

  fecha_transferencia  TS DEFAULT now(),
  hash_datos_enviados  VARCHAR(64)
  -- SHA-256 del payload enviado — para integridad y auditoría
);
```

---

### BLOQUE G — COMUNIDADES (Especialidad étnico-territorial)

#### ENTIDAD G1 — COMUNIDAD

*Descripción: Las comunidades indígenas y afrodescendientes como entidades colectivas con identidad jurídica propia, derechos colectivos, estructura de gobierno, y territorio.*

*Fundamento: Las comunidades étnicas no son grupos de individuos — son sujetos colectivos de derechos (Arts. 7, 330, 246 C.P.; Convenio 169 OIT; Ley 70/93). El esquema debe modelar esa naturaleza colectiva, no reducirla a un cliente individual.*

```sql
CREATE TABLE comunidades (
  id_comunidad         UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  id_comunidad_anonima UUID NOT NULL UNIQUE DEFAULT gen_random_uuid(),

  -- Identidad
  tipo_comunidad       ENUM(
    'indigena_resguardo_constituido',
    'indigena_sin_resguardo_en_proceso',
    'indigena_sin_reconocimiento',
    'afrodescendiente_consejo_comunitario',
    'afrodescendiente_otro',
    'raizal',
    'palenquero',
    'rom_gitano'
  ) NOT NULL,

  nombre_comunidad     VARCHAR(300) NOT NULL,
  pueblo_etnico        VARCHAR(200),
  -- Ej: "Embera Chamí", "Nasa", "Zenú"

  -- Reconocimiento formal
  reconocida_ministerio_interior BOOL DEFAULT FALSE,
  numero_resolucion_reconocimiento VARCHAR(100),

  -- Territorio
  tiene_resguardo_constituido BOOL DEFAULT FALSE,
  numero_resolucion_resguardo VARCHAR(100),
  municipios_territorio    TEXT[],
  departamentos_territorio TEXT[],
  hectareas_territorio     DECIMAL(15,2),

  -- Autoridades propias (estructura de gobierno)
  estructura_gobierno  ENUM(
    'cabildo',
    'consejo_comunitario',
    'consejo_mayor',
    'autoridad_tradicional',
    'asamblea_general',
    'otra'
  ),
  representante_legal  VARCHAR(300),
  -- Quien tiene personería jurídica para actuar ante el sistema formal

  -- Derecho propio
  tiene_reglamento_interno BOOL DEFAULT FALSE,
  jurisdiccion_especial_activa BOOL DEFAULT FALSE,
  -- TRUE si la comunidad ejerce activamente la jurisdicción especial indígena

  -- Situación de derechos (alimentado por casos)
  alertas_activas      JSONB,
  -- [{"tipo": "consulta_previa_omitida", "proyecto": "...",
  --   "entidad_responsable": "...", "urgencia": "alta"}]

  derechos_en_disputa  JSONB,
  -- Los derechos colectivos que están siendo litigados actualmente

  -- Conocimiento del abogado activo sobre esta comunidad
  conocimiento_pablo   TEXT,
  -- Lo que el abogado activo sabe sobre la comunidad que no está en registros públicos

  creado_en            TS DEFAULT now(),
  actualizado_en       TS DEFAULT now()
);

-- Vínculo entre procesos y comunidades
CREATE TABLE comunidad_proceso (
  comunidad_id         UUID NOT NULL REFERENCES comunidades(id_comunidad),
  proceso_id           UUID NOT NULL REFERENCES procesos(id_proceso),
  rol                  ENUM(
    'parte_activa_colectivo',
    'beneficiaria_efectos_inter_comunis',
    'interviniente',
    'afectada_indirecta'
  ) NOT NULL,
  PRIMARY KEY (comunidad_id, proceso_id)
);
```

---

#### ENTIDAD G2 — DERECHO_COLECTIVO_EN_PROCESO

*Descripción: Los derechos colectivos específicos que están en juego en un proceso étnico-territorial. Los derechos colectivos no son equivalentes a derechos individuales acumulados — son categorías jurídicas propias.*

```sql
CREATE TABLE derechos_colectivos_proceso (
  id_derecho           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proceso_id           UUID NOT NULL REFERENCES procesos(id_proceso),
  comunidad_id         UUID NOT NULL REFERENCES comunidades(id_comunidad),

  tipo_derecho         ENUM(
    'consulta_previa_libre_informada',  -- Art. 6 Conv. 169 OIT / Art. 330 C.P.
    'territorio_ancestral',             -- Arts. 63, 329, 330 C.P.
    'autodeterminacion_autonomia',      -- Art. 246 C.P.
    'identidad_cultural',               -- Art. 7 C.P.
    'recursos_naturales',               -- Art. 330 C.P.
    'jurisdiccion_especial',            -- Art. 246 C.P.
    'gobierno_propio',                  -- Art. 330 C.P.
    'etnoeducacion',                    -- Ley 115/94
    'salud_diferenciada',               -- Decreto 1811/90 y concordantes
    'participacion_decisiones',         -- Conv. 169 OIT Art. 7
    'retorno_territorio_desplazamiento' -- Autos 004, 005/09 CC
  ) NOT NULL,

  estado_derecho       ENUM(
    'amenazado',
    'vulnerado',
    'en_disputa',
    'en_proceso_reconocimiento',
    'reconocido_pendiente_garantia'
  ) NOT NULL,

  descripcion_situacion TEXT NOT NULL,
  -- La situación específica de este derecho en este caso

  norma_principal_id   UUID REFERENCES normas_juridicas(id_norma),
  precedente_principal_id UUID REFERENCES precedentes_jurisprudenciales(id_precedente),

  actor_que_amenaza    UUID REFERENCES partes(id_parte),
  -- La empresa, entidad, o persona que amenaza o vulnera el derecho

  creado_en            TS DEFAULT now()
);
```

---

### BLOQUE H — CALIBRACIÓN CON MODELO CAUSAL

#### ENTIDAD H1 — REGISTRO_CALIBRACION (rediseñado)

*Descripción: Registro de predicciones vs. resultados con distinción entre correlación y causalidad. Versión mejorada respecto al v1.0.*

```sql
CREATE TABLE registros_calibracion (
  id_registro          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  proceso_id_anonimo   UUID NOT NULL,

  tipo_accion          VARCHAR(100) NOT NULL,
  jurisdiccion_id      UUID REFERENCES jurisdicciones(id_jurisdiccion),
  contraparte_tipo     VARCHAR(100),

  -- Predicciones
  posterior_inferior   DECIMAL(5,2) NOT NULL,
  posterior_superior   DECIMAL(5,2) NOT NULL,
  posterior_centro_masa DECIMAL(5,2) NOT NULL,

  -- Factores evaluados CON su evaluación Y su peso asignado
  factores_evaluados   JSONB NOT NULL,
  -- [{"factor": "urgencia_vital_documentada",
  --   "evaluacion": "favorable|neutral|desfavorable|desconocido",
  --   "peso_asignado": "alto|medio|bajo",
  --   "razonamiento_de_inclusion": "..."}]

  input_jurisdiccional_disponible BOOL DEFAULT FALSE,

  -- Resultado
  resultado_nivel      SMALLINT CHECK (resultado_nivel BETWEEN 0 AND 5),
  resultado_como_porcentaje DECIMAL(5,2),

  -- Métricas de calibración
  dentro_del_rango     BOOL,
  diferencia_centro_masa DECIMAL(5,2),

  -- MODELO CAUSAL (nuevo en v2.0)
  -- La distinción entre correlación y causalidad

  factor_determinante_segun_fallo TEXT,
  -- Qué dijo el juez que fue lo determinante (solo de la parte motiva)

  factor_determinante_confirmado_en_modelo BOOL,
  -- ¿El factor que el juez identificó como determinante
  -- estaba en nuestro modelo de factores?

  factor_externo_no_modelado TEXT,
  -- Si hubo un factor determinante que el sistema no tenía en el modelo
  -- Ej: "El juez aplicó una SU del día anterior que no sabíamos"
  -- Ej: "La contraparte llegó a acuerdo por presión mediática"

  efecto_pablo_estrategia TEXT,
  -- Una decisión estratégica del abogado activo que fue determinante
  -- y que no estaba en el análisis de Lumi

  tipo_causa_resultado ENUM(
    'modelo_causal_correcto',        -- El factor que predijimos fue el determinante
    'correlacion_espuria',           -- El resultado fue por factor no modelado
    'abogado_fue_determinante',      -- La estrategia del abogado activo cambió el resultado
    'factor_externo_no_predecible',  -- Algo que nadie podría haber predicho
    'combinacion_factores'           -- Varios factores, no uno dominante
  ),

  -- Vigencia
  vigente_para_calibracion BOOL DEFAULT TRUE,
  fecha_invalidacion   TS,
  razon_invalidacion   TEXT,

  fecha_prediccion     DATE NOT NULL,
  fecha_resultado      DATE,
  creado_en            TS DEFAULT now()
);
```

---

## PARTE III — QUERIES CRÍTICAS ADICIONALES v2.0

**Q7 — Detección de conflicto de interés al abrir nuevo asunto**
```sql
-- ¿El abogado activo ha representado antes a alguien que ahora es contraparte,
-- o ha representado a la contraparte contra alguien similar al nuevo cliente?
SELECT
  p.id_proceso,
  a.descripcion_breve as asunto_previo,
  pp.rol as rol_previo,
  par.nombre_anonimo as parte_conflictiva,
  par.tipo_entidad
FROM partes par
JOIN parte_proceso pp ON pp.id_parte = par.id_parte
JOIN procesos p ON p.id_proceso = pp.id_proceso
JOIN asuntos a ON a.id_asunto = p.asunto_id
WHERE p.abogado_id = :abogado_id
  AND par.numero_identificacion = :identificacion_nueva_contraparte
  AND pp.rol IN ('demandante_principal', 'codemandante')
  -- ¿El abogado activo representó a alguien contra quien es ahora nuestro cliente?
UNION
SELECT
  p.id_proceso,
  a.descripcion_breve,
  pp.rol,
  par.nombre_anonimo,
  par.tipo_entidad
FROM partes par
JOIN parte_proceso pp ON pp.id_parte = par.id_parte
JOIN procesos p ON p.id_proceso = pp.id_proceso
JOIN asuntos a ON a.id_asunto = p.asunto_id
WHERE p.abogado_id = :abogado_id
  AND par.numero_identificacion = :identificacion_nueva_contraparte
  AND pp.rol IN ('demandado_principal', 'codemandado');
  -- ¿Esta contraparte fue antes cliente del abogado activo?
```

---

**Q8 — Efectividad de precedentes por jurisdicción (aprendizaje jurisprudencial)**
```sql
SELECT
  pj.identificador_completo,
  pj.tipo_sentencia,
  j.nombre_despacho,
  j.ciudad,
  COUNT(*) as veces_citado,
  SUM(CASE WHEN cj.acogido_por_juez = TRUE THEN 1 ELSE 0 END) as veces_acogido,
  ROUND(
    SUM(CASE WHEN cj.acogido_por_juez = TRUE THEN 1.0 ELSE 0.0 END)
    / NULLIF(COUNT(*), 0) * 100, 1
  ) as tasa_acogimiento_porcentaje
FROM citas_juridicas cj
JOIN precedentes_jurisprudenciales pj ON pj.id_precedente = cj.precedente_id
JOIN procesos p ON p.id_proceso = cj.caso_id
JOIN jurisdicciones j ON j.id_jurisdiccion = p.jurisdiccion_id
WHERE cj.acogido_por_juez IS NOT NULL  -- Solo casos con fallo
  AND p.abogado_id = :abogado_id
GROUP BY pj.identificador_completo, pj.tipo_sentencia, j.nombre_despacho, j.ciudad
HAVING COUNT(*) >= 3  -- Mínimo de casos para significancia
ORDER BY tasa_acogimiento_porcentaje DESC;
```

---

**Q9 — Análisis causal de resultados (para mejorar el modelo probabilístico)**
```sql
SELECT
  tipo_accion,
  tipo_causa_resultado,
  COUNT(*) as frecuencia,
  ROUND(AVG(diferencia_centro_masa), 2) as sesgo_promedio,
  COUNT(*) FILTER (WHERE factor_determinante_confirmado_en_modelo = TRUE)
    as veces_factor_estaba_en_modelo,
  COUNT(*) FILTER (WHERE factor_externo_no_modelado IS NOT NULL)
    as veces_factor_externo
FROM registros_calibracion
WHERE vigente_para_calibracion = TRUE
  AND fecha_resultado IS NOT NULL
GROUP BY tipo_accion, tipo_causa_resultado
ORDER BY tipo_accion, frecuencia DESC;
-- Responde: ¿cuándo acierta el modelo y por qué falla cuando falla?
```

---

**Q10 — Estado de derechos de titulares de datos con plazo vencido**
```sql
SELECT
  dts.id_solicitud,
  dts.tipo_derecho,
  dts.fecha_solicitud,
  dts.fecha_limite_respuesta,
  dts.fecha_limite_respuesta - now() as tiempo_restante,
  dts.estado,
  -- Sin PII del cliente — solo el ID para que el abogado identifique
  dts.cliente_id
FROM derechos_titular_ejercidos dts
WHERE dts.estado IN ('pendiente', 'en_gestion')
  AND dts.fecha_limite_respuesta <= now() + INTERVAL '2 days'
  -- Alerta 2 días antes del vencimiento
ORDER BY dts.fecha_limite_respuesta ASC;
-- Si hay registros aquí, el abogado está en riesgo de incumplir la Ley 1581
```

---

**Q11 — Normas citadas que ya no estaban vigentes en la fecha de los hechos**
```sql
SELECT
  p.id_proceso,
  p.tipo_accion,
  p.fecha_hechos_inicio,
  nj.nombre_corto,
  nj.fecha_vigencia_inicio,
  nj.fecha_vigencia_fin,
  cj.uso_en_documento,
  cj.verificado_en_fuente
FROM citas_juridicas cj
JOIN normas_juridicas nj ON nj.id_norma = cj.norma_id
JOIN procesos p ON p.id_proceso = cj.caso_id
WHERE p.fecha_hechos_inicio IS NOT NULL
  AND (
    -- La norma no había entrado en vigor cuando ocurrieron los hechos
    nj.fecha_vigencia_inicio > p.fecha_hechos_inicio
    OR
    -- La norma ya había sido derogada cuando ocurrieron los hechos
    (nj.fecha_vigencia_fin IS NOT NULL AND nj.fecha_vigencia_fin < p.fecha_hechos_inicio)
  );
-- Error jurídico grave: citar una norma inaplicable por tiempo
```

---

## PARTE IV — TABLA COMPARATIVA v1.0 vs v2.0

| Dimensión | v1.0 | v2.0 |
|-----------|------|------|
| Unidad central | Caso (proceso único) | Asunto + Proceso (varios procesos del mismo asunto) |
| Normas y precedentes | Texto en JSONB | Entidades propias con propiedades verificables |
| Hechos | Blob JSONB sin estatus epistémico | Entidades individuales con nivel_certeza y fuente |
| Tiempo jurídico | `creado_en` único | 4 dimensiones: hechos, proceso, sistema, vigencia normativa |
| Partes | contraparte_id + vinculo simple | Modelo rico con roles, relaciones, y detección de conflicto |
| Privacidad | Separación PII básica | Ley 1581 completa: datos sensibles, derechos del titular, transferencias |
| Jurisdicción | VARCHAR(200) | Entidad con características, competencias, y conocimiento acumulado |
| Comunidades | Ausente | Entidad G1 con derechos colectivos, autoridad propia, y territorio |
| Calibración | Correlación implícita | Modelo causal con distinción entre correlación y causalidad |
| Aprendizaje jurisprudencial | No soportado | Q8: tasa de acogimiento de precedentes por jurisdicción |
| Conflicto de interés | No soportado | Q7: detección estructural automatizable |
| Valor económico | Ausente | cuantia_pretendida, cuantia_obtenida, tasa_recuperacion |

---

## DECISIONES DE DISEÑO ADICIONALES v2.0

```
DECISIÓN 8 — El asunto como entidad separada del proceso
─────────────────────────────────────────────────────────
Decisión: Crear la entidad ASUNTO por encima de PROCESO.
Razón: Un cliente puede tener tutela + nulidad + denuncia
       sobre la misma situación. Sin ASUNTO, el sistema
       no puede relacionar esos procesos ni detectar
       conflictos cruzados entre ellos.
Costo: Mayor complejidad del modelo. Justificado porque
       el error de no tenerlo es mayor que el costo de tenerlo.

DECISIÓN 9 — Normas y precedentes como entidades con vigencia temporal
────────────────────────────────────────────────────────────────────────
Decisión: Modelar normas y precedentes como entidades.
Razón: Permite la Q11 (norma inaplicable por tiempo),
       la Q8 (efectividad de precedentes por jurisdicción),
       y la detección automática de precedentes superados.
Costo: Mantenimiento del catálogo normativo. El arquitecto del sistema
       actualiza cuando hay derogaciones o SU nuevas.
       Este costo es el mismo que tienen todos los abogados —
       el sistema simplemente lo hace estructural.

DECISIÓN 10 — Distinción datos ordinarios / datos sensibles
─────────────────────────────────────────────────────────────
Decisión: La entidad F1 distingue explícitamente datos
          sensibles (salud, etnia, discapacidad) con flag
          is_dato_sensible y consentimiento_especial.
Razón: El Art. 6 de la Ley 1581 exige que los datos
       sensibles tengan protección reforzada y que el
       consentimiento sea explícito e informado por separado.
       Las tutelas de salud generan datos de salud.
       Los casos étnicos generan datos de origen étnico.
       Sin esta distinción, el sistema viola la ley.

DECISIÓN 11 — Modelo causal en calibración
────────────────────────────────────────────
Decisión: El campo tipo_causa_resultado en registros_calibracion
          distingue entre modelo correcto, correlación espuria,
          efecto_abogado, y factor externo.
Razón: Sin esta distinción, el sistema aprende que el precedente
       X predice el resultado cuando en realidad el resultado
       se debió a algo no modelado. Correlación ≠ causalidad.
       El modelo causal produce calibración real.

DECISIÓN 12 — Comunidades como entidades colectivas (no individuos)
────────────────────────────────────────────────────────────────────
Decisión: La entidad G1 modela la comunidad como sujeto
          colectivo con estructura de gobierno propia,
          no como un grupo de clientes individuales.
Razón: El error de reducir una comunidad indígena a "el cliente
       Juan que es indígena" es jurídicamente incorrecto —
       los derechos colectivos pertenecen a la comunidad,
       no al individuo. El sistema debe modelar la realidad
       jurídica, no simplificarla para conveniencia técnica.
```

---

## REGISTRO DE VERSIONES

| Versión | Fecha | Cambio |
|---------|-------|--------|
| 1.0 | Abril 2026 | Schema inicial — 13 entidades |
| 2.0 | Abril 2026 | Rediseño epistemológico: asunto/proceso, normas/precedentes como entidades, hechos con estatus epistémico, tiempo jurídico tetradimensional, Ley 1581 completa, comunidades, modelo causal en calibración |
| 3.0 | Abril 2026 | Generalización de roles: referencias a Pablo → abogado activo, referencias a Felipe en gestión → arquitecto del sistema; campo pablo_fue_determinante → abogado_fue_determinante en registros_calibracion |

---

*Documento técnico-arquitectónico — Lumi v3.0*
*Versión 3.0 — Abril 2026*
*CONFIDENCIAL — Propiedad de Felipe Cruz*
