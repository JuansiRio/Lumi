# LUMI JUDICIAL — Technical Brief v2.0
> Sistema de inteligencia jurídica con agentes orquestados para apoyo al abogado
> Autor: Felipe Andrés Cruz · Juan Simón Obando · Abril 2026
> Estado: MVP — Primera iteración

---

## ÍNDICE

1. [Título y alcance](#1-título-y-alcance)
2. [Contexto del sistema](#2-contexto-del-sistema)
3. [Requerimientos técnicos](#3-requerimientos-técnicos)
4. [Restricciones](#4-restricciones)
5. [Definition of Done](#5-definition-of-done)
6. [Planning de implementación](#6-planning-de-implementación)
7. [Arquitectura de referencia](#7-arquitectura-de-referencia)
8. [Glosario](#8-glosario)

---
---

## ROLES DEL SISTEMA

> Este documento usa las siguientes convenciones de rol:

| Variable | Significado | Quién puede serlo |
|----------|-------------|-------------------|
| `{nombre_abogado}` | El abogado activo que usa el sistema en una sesión | Cualquier abogado autorizado con TP vigente |
| `{tp_abogado}` | Tarjeta profesional del abogado activo | Registrada en el perfil del usuario |
| `El abogado` | Referencia genérica al profesional del derecho responsable | Mismo que `{nombre_abogado}` |
| `El arquitecto` | Quien diseña, configura y mejora el sistema | Felipe Cruz u otro operador técnico |
| `El cliente` | La persona o empresa que contrata el servicio jurídico | Nunca interactúa directamente con LUMI |

**Regla deontológica central:** Solo quien tiene Tarjeta Profesional vigente puede aprobar,
firmar y entregar documentos jurídicos generados por LUMI. El arquitecto y los operadores
técnicos no tienen esa facultad, independientemente de su participación en el sistema.

---

## 1. TÍTULO Y ALCANCE

**Plataforma web de razonamiento jurídico orquestado por agentes — LUMI Judicial MVP**

### ¿Qué es?

LUMI Judicial es una plataforma web conversacional que asiste al abogado {nombre_abogado} en el análisis y construcción de casos jurídicos. El sistema ejecuta un motor de razonamiento estructurado en 8 fases secuenciales, delegando tareas especializadas a subagentes aislados, y persiste todo el estado del caso en base de datos para superar la limitación de la ventana de contexto del modelo de lenguaje.

### ¿Qué NO es?

- No es un chatbot genérico de consultas legales
- No interactúa con clientes directamente
- No toma decisiones jurídicas — propone, El abogado decide y firma
- No es un sistema multiusuario en esta iteración (un abogado por cuenta)

### Alcance del MVP

El MVP está completo cuando el abogado activo puede ejecutar un caso jurídico completo —desde la ingesta de documentos hasta la generación del borrador Word— directamente desde la plataforma, replicando el resultado del caso *Sayago Álzate vs. Roldán Morales* que fue construido manualmente en esta sesión de referencia.

---

## 2. CONTEXTO DEL SISTEMA

### El problema que resuelve

Los procesos judiciales colombianos requieren análisis jurídico estructurado, revisión documental exhaustiva, estimación de probabilidades y generación de documentos formales. Hoy, el abogado realiza todo esto manualmente o apoyado en conversaciones ad hoc con modelos de IA, lo que genera tres problemas:

1. **Pérdida de contexto**: Las conversaciones con IA se saturan y pierden información crítica del caso
2. **Falta de estructura**: El razonamiento no sigue un orden verificable de fases
3. **Sin memoria entre sesiones**: Cada sesión empieza desde cero

###"El sistema no existe hoy como código. Toda la base de conocimiento y los prompts viven en archivos .md. Este brief inicia la primera implementación desde cero.

### Cómo funciona el sistema

```
El abogado 
    │
    ▼
Interfaz conversacional 
    │
    ▼
Agente principal LUMI Core 
    │   ├── Lee contexto comprimido de la BD (no el historial completo)
    │   ├── Ejecuta fases secuenciales
    │   └── Delega a subagentes cuando corresponde
    │
    ├──► Subagente: Extractor de documentos (automático al subir archivos)
    ├──► Subagente: Motor probabilístico (Fase 2A — sesión aislada)
    ├──► Subagente: Simulación adversarial (Fase 5A — sesión completamente separada)
    ├──► Subagente: Verificación de jurisprudencia (Tavily + base de conocimiento)
    └──► Subagente: Control de calidad QA (antes de entregar cualquier borrador)
    │
    ▼
Capa de datos 
    ├── PostgreSQL: casos, hechos, partes, sesiones, outputs por fase
    ├── pgvector: embeddings de documentos y jurisprudencia
    └── Storage: archivos originales (PDF, Word, imágenes)
```

### Las 8 fases del motor de razonamiento

El sistema ejecuta estas fases en orden estricto. El abogado aprueba cada fase antes de avanzar a la siguiente.

| Fase | Nombre | Agente | Descripción |
|------|--------|--------|-------------|
| 0E | Análisis ético | LUMI Core | Conflicto de interés, solidez de pretensión, señales de omisión |
| 0A | Auditoría de hechos | LUMI Core | Completitud, consistencia temporal, vacíos probatorios |
| 0C | Estrategia inicial | LUMI Core | Acción jurídica correcta, competencia, caducidad, árbol de decisión |
| 1A | Preguntas críticas al cliente | LUMI Core | Cuestionario que el abogado le hace al cliente |
| 1C | Teoría del caso | LUMI Core | Narrativa jurídica central, hechos más poderosos |
| 2A | Motor probabilístico | Subagente probabilistico | Rango de probabilidad bayesiano por factor |
| 5A | Simulación adversarial | Subagente adversario | 5 argumentos en contra, ataque no obvio, vulnerabilidad probatoria |
| GEN | Generación del borrador | LUMI Core + QA | Documento jurídico completo + protocolo de verificación |

### Caso de referencia

El caso *Sayago Álzate vs. Roldán Morales* (demanda ejecutiva de alimentos, ~$57.5M COP) fue construido manualmente en la sesión de origen. Ese caso es el **benchmark del MVP**: el sistema debe poder reproducir ese resultado —análisis + borrador Word— desde la plataforma.

---

## 3. REQUERIMIENTOS TÉCNICOS

### 3.1 Stack tecnológico

#### Frontend
```
Framework:     Next.js 14 (App Router)
Lenguaje:      TypeScript (obligatorio — el sistema maneja muchos contratos de datos)
Estilos:       Tailwind CSS
Autenticación: NextAuth.js con Magic Link por email (sin contraseña)
               — Correos autorizados en la whitelist inicial
Deploy target: Vercel
```

> **¿Por qué Magic Link?** Es el método más simple y seguro. El abogado recibe un link por correo, hace clic y entra. Sin contraseñas que recordar ni rotar.

#### Backend — Agentes
```
Framework:     FastAPI (Python 3.11+)
Lenguaje:      Python con type hints en todos los módulos
SDK de IA:     anthropic (SDK oficial) — sin LangChain, sin abstracciones intermedias
               Control directo sobre cada llamada al modelo
Búsqueda web:  Tavily API
Parsing docs:  LlamaParse (PDF, Word) + Claude Vision (imágenes, fotos de documentos)
```

#### Base de datos
```
Proveedor:     Supabase (PostgreSQL + pgvector + Storage + Auth en un servicio)
ORM:           Supabase Python Client / Supabase JS Client (según capa)
Embeddings:    pgvector — dimensión 1536 (compatible con text-embedding-3-small de OpenAI
               o el modelo que Anthropic habilite)
Storage:       Supabase Storage para archivos originales
```

#### Estructura del repositorio
```
lumi-judicial/           ← Raíz del monorepo
├── apps/
│   ├── web/             ← Next.js frontend
│   │   ├── app/
│   │   │   ├── (auth)/
│   │   │   │   └── login/
│   │   │   ├── casos/
│   │   │   │   ├── page.tsx          ← Lista de casos
│   │   │   │   └── [id]/
│   │   │   │       ├── chat/
│   │   │   │       │   └── page.tsx  ← Interfaz conversacional
│   │   │   │       └── documentos/
│   │   │   │           └── page.tsx  ← Gestor de documentos
│   │   │   └── api/
│   │   │       ├── auth/             ← NextAuth endpoints
│   │   │       └── casos/            ← Proxy al backend FastAPI
│   │   ├── components/
│   │   │   ├── Chat/
│   │   │   ├── DocumentUpload/
│   │   │   └── FaseIndicator/
│   │   └── lib/
│   │       ├── supabase.ts
│   │       └── api-client.ts
│   │
│   └── agents/          ← FastAPI backend
│       ├── main.py      ← Entry point FastAPI
│       ├── core/
│       │   ├── lumi_core.py        ← Agente principal
│       │   ├── context_manager.py  ← Compresión de contexto entre sesiones
│       │   └── prompts/            ← Archivos .md con prompts por fase
│       │       ├── fase_0e.md
│       │       ├── fase_0a.md
│       │       ├── fase_0c.md
│       │       ├── fase_1a.md
│       │       ├── fase_1c.md
│       │       ├── fase_gen.md
│       │       └── sistema_base.md ← Prompt maestro de LUMI
│       ├── subagents/
│       │   ├── probabilistic.py    ← Fase 2A
│       │   ├── adversarial.py      ← Fase 5A
│       │   ├── jurisprudence.py    ← Verificación jurídica
│       │   ├── qa.py               ← Control de calidad
│       │   └── extractor.py        ← Procesamiento de documentos
│       ├── tools/
│       │   ├── document_parser.py  ← LlamaParse + Vision
│       │   ├── web_search.py       ← Tavily
│       │   ├── word_generator.py   ← Generación .docx
│       │   └── db.py               ← Cliente Supabase
│       ├── models/                 ← Pydantic models (contratos de datos)
│       │   ├── caso.py
│       │   ├── hecho.py
│       │   ├── documento.py
│       │   └── fase_output.py
│       └── routers/
│           ├── casos.py
│           ├── chat.py
│           ├── documentos.py
│           └── fases.py
│
├── packages/
│   └── database/
│       ├── schema.sql              ← Schema completo de Supabase
│       └── migrations/
│
├── docs/
│   ├── BASE_CONOCIMIENTO_JURIDICO.md
│   ├── MOTOR_RAZONAMIENTO.md
│   └── ARQUITECTURA.md
│
├── .env.example                    ← Variables de entorno documentadas
├── docker-compose.yml              ← Desarrollo local
└── README.md
```

### 3.2 Modelos de IA y criterio de selección

| Subagente | Modelo | Justificación |
|-----------|--------|---------------|
| LUMI Core (conversación + fases) | `claude-sonnet-4-5` | Razonamiento complejo, narrativa jurídica |
| Subagente adversarial (5A) | `claude-sonnet-4-5` | Requiere el mismo nivel de sofisticación |
| Subagente probabilístico (2A) | `claude-haiku-4-5` | Tarea acotada, 5x más barato |
| Extractor de documentos | `claude-haiku-4-5` | Extracción estructurada, alta velocidad |
| Control de calidad QA | `claude-haiku-4-5` | Checklist verificable, sin razonamiento libre |
| Verificación jurisprudencia | `claude-haiku-4-5` | Tarea de búsqueda y validación acotada |

**Regla de selección**: Usar `claude-haiku-4-5` siempre que la tarea sea acotada y verificable (extracción, clasificación, checklists). Escalar a `claude-sonnet-4-5` solo cuando se requiere razonamiento libre, narrativa o simulación estratégica.

### 3.3 Contratos de datos — Modelos Pydantic

```python
# models/caso.py
from pydantic import BaseModel, UUID4
from enum import Enum
from datetime import datetime

class TipoAccion(str, Enum):
    ejecutivo = "ejecutivo"
    tutela = "tutela"
    laboral = "laboral"
    nulidad_restablecimiento = "nulidad_restablecimiento"
    reparacion_directa = "reparacion_directa"
    otro = "otro"

class EstadoCaso(str, Enum):
    activo = "activo"
    pausado = "pausado"
    cerrado = "cerrado"

class Caso(BaseModel):
    id: UUID4
    nombre_caso: str
    tipo_accion: TipoAccion
    estado: EstadoCaso
    fase_actual: str
    tokens_consumidos: int = 0
    costo_usd: float = 0.0
    created_at: datetime
    updated_at: datetime

# models/hecho.py
class EstatusEpistemico(str, Enum):
    verificado = "verificado"
    inferido = "inferido"
    desconocido = "desconocido"
    contradicho = "contradicho"

class Hecho(BaseModel):
    id: UUID4
    caso_id: UUID4
    fase_origen: str
    contenido: str
    estatus_epistemico: EstatusEpistemico
    fuente: str | None = None

# models/fase_output.py
class FaseOutput(BaseModel):
    caso_id: UUID4
    fase: str
    version: int
    contenido: dict          # output estructurado de la fase
    aprobado_abogado: bool = False
    anotaciones: str | None = None
    tokens_usados: int
    costo_usd: float
```

### 3.4 API Endpoints — FastAPI

```
POST   /casos/                          Crear nuevo caso
GET    /casos/                          Listar casos
GET    /casos/{id}                      Detalle del caso
PATCH  /casos/{id}                      Actualizar estado/fase

POST   /casos/{id}/chat                 Enviar mensaje al agente LUMI Core
GET    /casos/{id}/chat/historial       Últimos N mensajes de la sesión

POST   /casos/{id}/documentos           Subir documento (activa extractor)
GET    /casos/{id}/documentos           Listar documentos del caso

POST   /casos/{id}/fases/{fase}/aprobar Aprobar fase y comprimir contexto
GET    /casos/{id}/fases/               Ver outputs de todas las fases

GET    /casos/{id}/borrador             Descargar borrador .docx
GET    /casos/{id}/costos               Resumen de tokens y costo USD
```

### 3.5 Gestión de contexto entre sesiones

**El problema que resuelve**: Evitar que el historial completo de la conversación sature la ventana de contexto del modelo (200.000 tokens máximo).

**Mecanismo**:
1. Cuando El abogado aprueba una fase, LUMI Core genera un **resumen estructurado** de esa fase (800-1200 tokens)
2. El resumen se guarda en `outputs_fases`
3. El historial de mensajes se archiva en `sesiones` (no se borra, solo se archiva)
4. En la siguiente fase, LUMI Core carga **solo los resúmenes**, no el historial completo

**Contexto que LUMI Core recibe en cada turno** (~15.000-25.000 tokens):
```
sistema_base.md          ← Prompt maestro y reglas de LUMI
resúmenes de fases       ← Un resumen por fase completada (~800 tokens c/u)
hechos del caso          ← Recuperados por búsqueda semántica (los más relevantes)
últimos 20 mensajes      ← Sesión activa actual
fase_actual.md           ← Prompt específico de la fase en curso
```

### 3.6 Almacenamiento de prompts

Los prompts de cada fase se almacenan como archivos `.md` en `apps/agents/core/prompts/`. Esto permite:
- Editar prompts sin modificar código Python
- Control de versiones sobre los prompts con git
- Que Cursor/Claude Code pueda leer y actualizar los prompts como parte del desarrollo

Estructura de un archivo de prompt:
```markdown
# FASE 0E — ANÁLISIS ÉTICO

## Rol
Eres LUMI ejecutando la Fase 0E...

## Instrucciones
1. Verifica conflicto de interés...
2. Evalúa solidez de la pretensión...

## Output esperado
Semáforo por verificación + decisión de continuar o alertar.

## Formato de respuesta
[definir formato JSON estructurado]
```

### 3.7 Trazabilidad y costos

Cada llamada a la API de Anthropic debe registrarse automáticamente:

```python
# tools/db.py
async def log_llamada_api(
    caso_id: str,
    agente: str,
    modelo: str,
    tokens_input: int,
    tokens_output: int,
    duracion_ms: int
) -> None:
    costo = calcular_costo(modelo, tokens_input, tokens_output)
    # INSERT en tabla trazabilidad
    # UPDATE tokens_consumidos y costo_usd en tabla casos
```

**Precios de referencia para el cálculo** (verificar en tiempo de desarrollo):
- `claude-sonnet-4-5`: $3 / MTok input · $15 / MTok output
- `claude-haiku-4-5`: $0.25 / MTok input · $1.25 / MTok output

### 3.8 Contratos de agentes — Inputs y Outputs

Cada agente y subagente tiene un contrato fijo. Cursor debe respetar
estos contratos al generar los módulos en `subagents/` y `core/`.
Los tipos referenciados aquí están definidos en `models/`.

---

#### LUMI Core — Agente orquestador principal
```python
# core/lumi_core.py

Input:
    caso_id:       UUID4
    mensaje:       str                  # mensaje del abogado en el chat
    fase_actual:   str                  # ej: "0E", "0A", "1C", "GEN"

Output: LumiCoreResponse
    respuesta:          str             # texto que ve el abogado en el chat
    fase_output:        FaseOutput | None   # solo cuando la fase concluye
    subagente_llamado:  str | None      # nombre del subagente si fue delegado
    tokens_usados:      int
    costo_usd:          float
```

---

#### Context Manager — Construcción del contexto comprimido
```python
# core/context_manager.py

Input:
    caso_id:        UUID4
    fase_actual:    str
    max_tokens:     int = 25_000

Output: ContextoComprimido
    prompt_maestro:     str             # contenido de sistema_base.md
    resumenes_fases:    list[str]       # un resumen por fase aprobada
    hechos_relevantes:  list[Hecho]     # top-K por búsqueda semántica
    ultimos_mensajes:   list[dict]      # últimos 20 mensajes de la sesión
    prompt_fase:        str             # contenido de fase_XX.md
    total_tokens_est:   int             # estimación antes de llamar al modelo
```

---

#### Subagente Extractor de Documentos
```python
# subagents/extractor.py

Input:
    documento_id:   UUID4
    caso_id:        UUID4
    archivo_bytes:  bytes
    mime_type:      str                 # "application/pdf" | "image/jpeg" | etc.

Output: ExtractorOutput
    texto_extraido:     str
    hechos_detectados:  list[Hecho]     # hechos con estatus_epistemico asignado
    partes_detectadas:  list[dict]      # nombre, rol (demandante/demandado/otro)
    fechas_detectadas:  list[dict]      # fecha, contexto
    alertas:            list[str]       # ej: "Posible caducidad detectada"
    tokens_usados:      int
    costo_usd:          float
```

---

#### Subagente Motor Probabilístico — Fase 2A
```python
# subagents/probabilistic.py
# Corre en sesión aislada. No recibe historial de conversación.

Input:
    hechos:         list[Hecho]
    tipo_accion:    TipoAccion
    teoria_caso:    str                 # output de Fase 1C

Output: ProbabilisticOutput
    rango_min:      float               # ej: 0.55
    rango_max:      float               # ej: 0.80
    centro_masa:    float               # ej: 0.68
    factores:       list[Factor]        # cada factor con peso y dirección
    justificacion:  str
    advertencias:   list[str]           # vacíos probatorios que afectan el rango
    tokens_usados:  int
    costo_usd:      float

# Factor:
#   nombre:     str
#   peso:       float       # 0.0 a 1.0
#   direccion:  str         # "favorable" | "desfavorable" | "neutro"
#   nota:       str
```

---

#### Subagente Simulación Adversarial — Fase 5A
```python
# subagents/adversarial.py
# Corre en sesión completamente separada. Sin acceso al historial de LUMI Core.

Input:
    hechos:         list[Hecho]
    teoria_caso:    str                 # output de Fase 1C
    tipo_accion:    TipoAccion

Output: AdversarialOutput
    argumentos:             list[str]   # exactamente 5, ordenados por impacto
    ataque_no_obvio:        str         # el argumento que LUMI Core no anticipó
    vulnerabilidad_probatoria: str      # el hueco más peligroso en las pruebas
    nulidades_propias:      list[str]   # riesgos procedimentales del caso propio
    tokens_usados:          int
    costo_usd:              float
```

---

#### Subagente Verificación de Jurisprudencia
```python
# subagents/jurisprudence.py

Input:
    citas:          list[str]           # lista de sentencias a verificar
    caso_id:        UUID4

Output: JurisprudenciaOutput
    resultados:     list[VerificacionCita]
    tokens_usados:  int
    costo_usd:      float

# VerificacionCita:
#   cita_original:  str                 # ej: "CSJ SCC 3 may. 2019"
#   estado:         str                 # "✅ VERIFICADA" | "⚠️ PROBABLE" | "🔴 VERIFICAR"
#   fuente:         str                 # "base_conocimiento" | "tavily" | "no_encontrada"
#   nota:           str | None
```

---

#### Subagente Control de Calidad — QA
```python
# subagents/qa.py

Input:
    borrador_texto: str
    hechos:         list[Hecho]
    teoria_caso:    str
    tipo_accion:    TipoAccion

Output: QAOutput
    semaforo_general:   str             # "🟢 LISTO" | "🟡 OBSERVACIONES" | "🔴 CRÍTICO"
    correcciones:       list[Correccion]
    aprobado:           bool
    tokens_usados:      int
    costo_usd:          float

# Correccion:
#   prioridad:      str                 # "🔴 crítico" | "🟡 importante" | "🟢 menor"
#   ubicacion:      str                 # sección o párrafo donde está el problema
#   descripcion:    str
#   sugerencia:     str
```

---

#### Tool — Generador de Borrador Word
```python
# tools/word_generator.py
# No es un agente con modelo. Es una herramienta determinista.

Input:
    caso_id:            UUID4
    outputs_fases:      dict[str, FaseOutput]   # todas las fases aprobadas
    hechos:             list[Hecho]
    metadata_caso:      Caso

Output: WordOutput
    archivo_bytes:      bytes           # contenido del .docx
    nombre_archivo:     str             # ej: "demanda_sayago_alzate_v1.docx"
    paginas_estimadas:  int
    advertencias:       list[str]       # secciones que quedaron incompletas
```

---

## 4. RESTRICCIONES

### 4.1 Lo que el sistema NO debe hacer

- **No usar LangChain ni frameworks de agentes de terceros** — control directo sobre cada llamada con el SDK de Anthropic. Esto garantiza trazabilidad exacta de tokens y comportamiento predecible.
- **No cargar el historial completo de mensajes** en ninguna llamada al modelo. Siempre usar el mecanismo de compresión por fases.
- **No permitir que un subagente tenga acceso al historial de otro subagente**. Los subagentes 2A y 5A deben correr en sesiones completamente aisladas.
- **No saltar fases**. El sistema debe bloquear el avance si la fase anterior no fue aprobada por el abogado, excepto que el abogado la fuerce explícitamente con confirmación.
- **No inventar jurisprudencia**. Si una sentencia no puede ser verificada, el sistema debe marcarla con `🔴 VERIFICAR` y nunca presentarla como verificada.
- **No interactuar con el cliente final**. Toda la interacción es entre LUMI y el abogado activo exclusivamente.

### 4.2 Estándares de código

#### Python
```
- Type hints obligatorios en todas las funciones y métodos
- Pydantic para todos los modelos de datos (sin dicts sin tipar)
- Async/await para todas las llamadas a BD y APIs externas
- Docstrings en todas las funciones públicas
- Manejo explícito de excepciones (sin bare except)
- Variables de entorno por .env — sin credenciales hardcodeadas
- Linter: ruff (más rápido que flake8, recomendado para proyectos nuevos)
```

#### TypeScript / Next.js
```
- TypeScript strict mode activado
- Interfaces explícitas para props de componentes
- No usar `any` — siempre tipar correctamente
- Server Components por defecto, Client Components solo cuando sea necesario
- Variables de entorno en .env.local — nunca en el código
- Linter: ESLint con configuración de Next.js
```

#### General
```
- Commits en inglés, convención: feat/fix/chore/docs/refactor
- Un archivo .env.example documentado con todas las variables necesarias
- docker-compose.yml funcional para levantar el entorno local completo
- README.md con instrucciones de setup en menos de 5 pasos
```

### 4.3 Seguridad

- El correo del abogado debe estar en una whitelist en variable de entorno, no en base de datos
- Supabase Row Level Security activado desde el inicio para aislar casos
- Todos los uploads de documentos deben validar tipo de archivo antes de procesar (solo PDF, DOCX, XLSX, JPG, PNG, JPEG)
- Las claves de API (Anthropic, Tavily, Supabase) nunca deben aparecer en logs ni en el frontend

### 4.4 Manejo de errores

Toda llamada a API externa (Anthropic, Tavily, LlamaParse, Supabase) debe tener:
- Timeout explícito
- Retry con backoff exponencial (máximo 3 intentos)
- Fallback comunicado al abogado en la interfaz (nunca un error 500 sin contexto)

---

## 5. DEFINITION OF DONE

### 5.1 Definition of Done del MVP completo

#### Prueba de aceptación final

El MVP se considera entregado cuando el abogado ejecuta esta secuencia
sin intervención técnica y sin errores:

1. Accede a la plataforma desde su navegador con Magic Link
2. Crea el caso *Sayago Álzate vs. Roldán Morales*
3. Sube el Acta SIM 11054012 — el extractor detecta automáticamente
   las obligaciones y las cifras
4. Ejecuta las 8 fases en secuencia, aprobando cada una
5. Descarga el `.docx` generado
6. El `.docx` es equivalente al borrador de referencia
   (validado por el abogado activo, no por criterio técnico)

**Evidencia requerida**: video o screenshots del flujo completo + 
archivo `.docx` descargado + reporte de pytest con cobertura ≥ 80%.

Sin esa evidencia, el MVP no está done aunque todos los checkboxes estén marcados.

#### Funcionalidad
- [ ] El abogado puede autenticarse con Magic Link en su correo
- [ ] El abogado puede crear un caso nuevo con nombre y tipo de acción
- [ ] El abogado puede subir documentos (PDF, Word, imágenes) y el sistema los procesa automáticamente
- [ ] LUMI Core ejecuta las 8 fases en secuencia, esperando aprobación del abogado en cada una
- [ ] Los subagentes 2A, 5A, QA y Jurisprudencia corren correctamente desde la plataforma
- [ ] El sistema genera y permite descargar el borrador en formato `.docx`
- [ ] El contexto del caso persiste entre sesiones (El abogado puede cerrar el navegador y retomar)
- [ ] El abogado puede ver el costo estimado en USD del caso en tiempo real
- [ ] El caso *Sayago vs. Roldán* puede reproducirse completo desde la plataforma

#### Calidad técnica
- [ ] Cobertura de tests: mínimo 80% en los módulos de agentes (pytest)
- [ ] Todos los endpoints de FastAPI documentados con OpenAPI (generado automáticamente por FastAPI — sin trabajo adicional)
- [ ] Trazabilidad: cada llamada a Anthropic queda registrada en la tabla `trazabilidad`
- [ ] Sin credenciales hardcodeadas en el código
- [ ] `.env.example` con todas las variables documentadas
- [ ] `docker-compose.yml` levanta el entorno local con un solo comando

#### Experiencia del abogado
- [ ] La interfaz es conversacional — El abogado escribe, LUMI responde
- [ ] Los errores se comunican en lenguaje claro, no como stack traces
- [ ] El sistema indica en qué fase está el caso en todo momento
- [ ] Los documentos subidos aparecen confirmados con su tipo detectado

### 5.2 Definition of Done por módulo

#### Módulo 1 — Infraestructura base
- [ ] Repositorio GitHub privado creado con estructura definida en sección 3.1
- [ ] Supabase: proyecto creado, schema aplicado, RLS activado
- [ ] Next.js corriendo en local con auth Magic Link funcional
- [ ] FastAPI corriendo en local, health check respondiendo
- [ ] docker-compose levanta ambos servicios con un comando

#### Módulo 2 — Extractor de documentos
- [ ] Upload de PDF/Word/imagen desde la interfaz
- [ ] Subagente extractor procesa el archivo y guarda en Supabase Storage
- [ ] Texto extraído guardado en tabla `documentos`
- [ ] Metadatos estructurados (tipo, fecha, valor, partes) guardados en `hechos`
- [ ] Test: subir el Acta SIM 11054012 y verificar que extrae correctamente las obligaciones

#### Módulo 3 — LUMI Core + Fases 0E, 0A, 0C
- [ ] Conversación funcional con LUMI Core en la interfaz
- [ ] Las tres primeras fases se ejecutan en secuencia
- [ ] El abogado puede aprobar cada fase
- [ ] Output de cada fase guardado en `outputs_fases`
- [ ] Contexto comprimido funcional (no carga historial completo)

#### Módulo 4 — Fases 1A, 1C + Subagentes 2A, 5A
- [ ] Fases 1A y 1C ejecutándose correctamente
- [ ] Subagente Motor Probabilístico produce rango con justificación
- [ ] Subagente Adversarial produce 5 argumentos en contra en sesión aislada
- [ ] Outputs integrados por LUMI Core y presentados al abogado

#### Módulo 5 — QA + Generación de borrador
- [ ] Subagente QA revisa el borrador antes de entregarlo
- [ ] Sistema genera archivo `.docx` descargable
- [ ] El borrador incluye el protocolo de verificación al final
- [ ] Test: generar el borrador del caso Sayago vs. Roldán y comparar con el de referencia

#### Módulo 6 — Jurisprudencia + Trazabilidad + Costos
- [ ] Subagente de jurisprudencia busca en Tavily + base de conocimiento .md
- [ ] Cada cita produce semáforo de verificación
- [ ] Dashboard de costos por caso visible para el abogado activo
- [ ] Tabla `trazabilidad` registrando todas las llamadas

---

## 6. PLANNING DE IMPLEMENTACIÓN

Ver documento separado: `LUMI_JUDICIAL_IMPLEMENTATION_PLAN_v2.md`

---

## 7. ARQUITECTURA DE REFERENCIA

### Flujo de datos completo

```
[Abogado] → escribe en chat
    │
    ▼
[Next.js] → POST /casos/{id}/chat
    │
    ▼
[FastAPI — LUMI Core]
    │
    ├── 1. Context Manager: carga contexto comprimido de Supabase
    │       └── prompt maestro + resúmenes de fases + hechos relevantes
    │
    ├── 2. Llama a Anthropic API (claude-sonnet-4-5)
    │       └── Registra en tabla trazabilidad
    │
    ├── 3. Si es output de fase: guarda en outputs_fases
    │
    ├── 4. Si requiere subagente:
    │       ├── Motor Probabilístico → sesión aislada → Haiku
    │       ├── Adversarial → sesión separada → Sonnet
    │       ├── Jurisprudencia → Tavily + base MD → Haiku
    │       └── QA → checklist → Haiku
    │
    └── 5. Retorna respuesta a Next.js
    │
    ▼
[Next.js] → muestra respuesta en chat
[Abogado] → lee, anota, aprueba fase
```

### Gestión de contexto — Diagrama

```
Sesión 1 (Fase 0E + 0A)
├── Historial: 45 mensajes → archivado en tabla sesiones
└── Resumen 0E: 600 tokens → guardado en outputs_fases
└── Resumen 0A: 750 tokens → guardado en outputs_fases

Sesión 2 (Fase 0C + 1A) — carga:
├── Resumen 0E (600 tokens)
├── Resumen 0A (750 tokens)
├── Prompt maestro (2.000 tokens)
├── Prompt fase 0C (800 tokens)
├── Hechos relevantes por semántica (3.000 tokens)
└── Total contexto: ~7.150 tokens ← vs. 45.000 si cargara historial completo
```

---

## 8. GLOSARIO

| Término | Definición en este sistema |
|---------|---------------------------|
| **LUMI Core** | Agente principal que conduce la conversación con el abogado y orquesta las fases |
| **Subagente** | Agente especializado que corre en sesión aislada para una tarea acotada |
| **Fase** | Etapa del motor de razonamiento jurídico (0E, 0A, 0C, 1A, 1C, 2A, 5A, GEN) |
| **Contexto comprimido** | Resúmenes de fases anteriores que reemplazan el historial completo |
| **Hecho** | Unidad atómica de información del caso con estatus epistémico (verificado/inferido/desconocido) |
| **Output de fase** | Resultado estructurado de una fase, aprobado por el abogado, guardado en BD |
| **Ventana de contexto** | Límite de tokens que el modelo puede procesar en una sola llamada (200.000 en Claude) |
| **Magic Link** | Método de autenticación por email: se recibe un link con un solo uso para iniciar sesión |
| **RLS** | Row Level Security — mecanismo de Supabase para que cada usuario solo vea sus propios datos |
| **pgvector** | Extensión de PostgreSQL para almacenar y buscar vectores de embeddings semánticamente |
| **Embedding** | Representación numérica del texto que permite búsqueda por similitud semántica |
| **Trazabilidad** | Registro completo de cada llamada a la API: modelo, tokens, costo, duración |

---

*LUMI Judicial Technical Brief v2.0 · Abril 2026*
*LUMI propone. El abogado decide y firma.*
