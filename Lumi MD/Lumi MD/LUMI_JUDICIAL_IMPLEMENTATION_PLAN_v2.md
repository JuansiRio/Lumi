# LUMI JUDICIAL — Plan de Implementación
> Basado en Technical Brief v2.0
> Modalidad: paso a paso, sin código aún
> Audiencia: Cursor / Claude Code + El equipo técnico

---

## CÓMO LEER ESTE DOCUMENTO

Cada tarea tiene:
- **Qué hace**: la lógica en lenguaje natural
- **Archivos a crear**: lista con propósito de cada uno
- **Archivos a modificar**: cuál y por qué
- **Verificación**: cómo saber que funcionó antes de avanzar
- **Bloqueante de**: qué tareas no pueden empezar sin esta

Las tareas están ordenadas por dependencia estricta.
No avanzar a la siguiente sin que la verificación de la actual pase.

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

## SPRINT 0 — INFRAESTRUCTURA BASE
### Objetivo: Todo el entorno levantado, sin ninguna lógica de negocio aún

---

### TAREA S0.1 — Crear estructura del repositorio

**Qué hace:**
Crea el esqueleto completo del repositorio con todas las carpetas vacías
(o con archivos `.gitkeep` para que git las rastree). Ningún archivo tiene
lógica aún — solo la estructura que el resto del proyecto va a poblar.
Esto le da al agente de código un mapa claro de dónde va cada cosa
antes de empezar a escribir.

**Archivos a crear:**
```
lumi-judicial/
├── README.md
│   └── Propósito: instrucciones de setup en 5 pasos (vacías por ahora, se completan al final)
│
├── .gitignore
│   └── Propósito: excluir node_modules, __pycache__, .env, .env.local, archivos de build
│
├── .env.example
│   └── Propósito: lista comentada de TODAS las variables de entorno del sistema.
│       Cada variable tiene un comentario que explica para qué sirve y cómo obtenerla.
│       Es el único lugar donde está documentado qué credenciales necesita el proyecto.
│
├── docker-compose.yml
│   └── Propósito: define dos servicios — web (Next.js en puerto 3000)
│       y agents (FastAPI en puerto 8000). En esta tarea solo define la estructura,
│       los comandos de arranque se completan en S0.3 y S0.4.
│
├── apps/
│   ├── web/                    ← carpeta vacía con .gitkeep
│   └── agents/                 ← carpeta vacía con .gitkeep
│
└── packages/
    └── database/               ← carpeta vacía con .gitkeep
```

**Verificación:**
`git init` + `git add .` + `git commit` sin errores.
Repositorio visible en GitHub con la estructura de carpetas.

**Bloqueante de:** todas las demás tareas.

---

### TAREA S0.2 — Configurar proyecto Next.js

**Qué hace:**
Inicializa la aplicación Next.js 14 dentro de `apps/web/` con TypeScript,
Tailwind CSS y ESLint activados. Configura la estructura de carpetas
del App Router. No hay páginas con lógica aún — solo las páginas
vacías que se van a poblar, con el layout base que todas las páginas
van a compartir (fuente, colores, estructura general).

**Archivos a crear:**
```
apps/web/
├── package.json
│   └── Propósito: dependencias del frontend. Incluye next, react, typescript,
│       tailwindcss, @supabase/supabase-js, next-auth.
│
├── tsconfig.json
│   └── Propósito: configuración TypeScript con strict mode activado.
│       Esto obliga a que todos los tipos estén declarados explícitamente.
│
├── tailwind.config.ts
│   └── Propósito: define los colores, fuentes y breakpoints del sistema.
│       El color primario es azul (#1F4E79), tipografía Inter.
│
├── next.config.mjs
│   └── Propósito: configuración de Next.js. Define que las variables de
│       entorno NEXT_PUBLIC_* son accesibles en el cliente.
│
├── app/
│   ├── layout.tsx
│   │   └── Propósito: layout raíz de toda la aplicación. Incluye la fuente,
│   │       el proveedor de sesión de NextAuth y el proveedor de Supabase.
│   │       Todo lo que esté aquí aplica a todas las páginas.
│   │
│   ├── page.tsx
│   │   └── Propósito: página de inicio. Redirige a /login si no hay sesión,
│   │       o a /casos si hay sesión activa. No tiene contenido propio.
│   │
│   ├── (auth)/
│   │   └── login/
│   │       └── page.tsx
│   │           └── Propósito: página de login con Magic Link.
│   │               Muestra un campo de email y un botón.
│   │               Al enviar, NextAuth manda el link al correo del abogado.
│   │               Si el correo no está en la whitelist, muestra error.
│   │
│   ├── casos/
│   │   ├── page.tsx
│   │   │   └── Propósito: lista de todos los casos del abogado activo.
│   │   │       Muestra nombre, tipo de acción, fase actual y costo acumulado.
│   │   │       Botón para crear caso nuevo.
│   │   │
│   │   └── [id]/
│   │       ├── layout.tsx
│   │       │   └── Propósito: layout específico de un caso.
│   │       │       Muestra en la barra lateral: nombre del caso,
│   │       │       indicador de fase actual, y navegación entre
│   │       │       chat y documentos.
│   │       │
│   │       ├── chat/
│   │       │   └── page.tsx
│   │       │       └── Propósito: interfaz conversacional principal.
│   │       │           Muestra el historial de mensajes y el campo
│   │       │           de entrada. Es la página que el abogado usa el 90% del tiempo.
│   │       │
│   │       └── documentos/
│   │           └── page.tsx
│   │               └── Propósito: gestor de documentos del caso.
│   │                   Muestra los documentos subidos con su tipo detectado.
│   │                   Tiene el área de drag-and-drop para subir archivos.
│   │
│   └── api/
│       ├── auth/
│       │   └── [...nextauth]/
│       │       └── route.ts
│       │           └── Propósito: endpoint de NextAuth. Maneja el flujo
│       │               Magic Link: recibe el email, verifica si está en
│       │               whitelist, envía el correo con el link.
│       │
│       └── casos/
│           └── route.ts
│               └── Propósito: proxy que reenvía las llamadas del frontend
│                   al backend FastAPI. Agrega el token de sesión en cada
│                   llamada para que FastAPI sepa quién es el abogado activo.
│
├── components/
│   ├── Chat/
│   │   ├── ChatWindow.tsx
│   │   │   └── Propósito: componente que muestra el historial de mensajes.
│   │   │       Diferencia visualmente los mensajes del abogado (derecha)
│   │   │       y de LUMI (izquierda). Maneja el scroll automático al fondo.
│   │   │
│   │   ├── MessageInput.tsx
│   │   │   └── Propósito: campo de texto con botón de enviar.
│   │   │       Se bloquea mientras LUMI está respondiendo.
│   │   │       Muestra indicador de "LUMI está escribiendo..."
│   │   │
│   │   └── FaseIndicator.tsx
│   │       └── Propósito: barra que muestra las 8 fases como pasos.
│   │           Las fases completadas están en verde, la actual en azul,
│   │           las pendientes en gris. Incluye botón "Aprobar fase".
│   │
│   └── DocumentUpload/
│       └── DropZone.tsx
│           └── Propósito: área de drag-and-drop para subir archivos.
│               Acepta PDF, DOCX, XLSX, JPG, PNG, JPEG.
│               Muestra progreso de upload y confirmación del tipo detectado.
│
└── lib/
    ├── supabase.ts
    │   └── Propósito: cliente de Supabase configurado con las variables
    │       de entorno. Exporta un cliente para uso en el servidor
    │       (con service role) y otro para el cliente (con anon key).
    │
    └── api-client.ts
        └── Propósito: funciones tipadas para llamar al backend FastAPI.
            Cada función corresponde a un endpoint: createCaso, sendMessage,
            uploadDocument, approvePhase, downloadBorrador.
```

**Verificación:**
`cd apps/web && npm install && npm run dev` → app corre en localhost:3000
sin errores en consola. La página `/login` carga aunque aún no funcione.

**Bloqueante de:** S0.3, S0.5.

---

### TAREA S0.3 — Configurar proyecto FastAPI

**Qué hace:**
Inicializa la aplicación Python dentro de `apps/agents/` con FastAPI,
uvicorn y las dependencias necesarias. Crea un endpoint de health check
y la estructura de carpetas que los agentes van a poblar.
En esta tarea no hay lógica de IA — solo la aplicación corriendo.

**Archivos a crear:**
```
apps/agents/
├── requirements.txt
│   └── Propósito: lista de dependencias Python. Incluye fastapi, uvicorn,
│       anthropic, supabase, python-dotenv, pydantic, llama-parse,
│       tavily-python, python-docx, pytest, ruff.
│
├── main.py
│   └── Propósito: entry point de FastAPI. Registra todos los routers,
│       configura CORS para que Next.js pueda llamarlo,
│       y expone el endpoint /health.
│
├── .env
│   └── Propósito: copia de .env.example con las variables reales.
│       Este archivo NUNCA se sube a git (está en .gitignore).
│
├── core/
│   ├── __init__.py
│   ├── lumi_core.py
│   │   └── Propósito: módulo vacío con la firma de la función principal.
│   │       Se puebla en S2.2. Por ahora solo define que existe
│   │       una función process_message(caso_id, message) que retorna string.
│   │
│   ├── context_manager.py
│   │   └── Propósito: módulo vacío con la firma de build_context(caso_id, fase).
│   │       Se puebla en S2.1.
│   │
│   └── prompts/
│       ├── sistema_base.md
│       │   └── Propósito: el prompt maestro de LUMI — quién es, qué puede hacer,
│       │       qué NO puede hacer, las reglas que nunca abandona.
│       │       Este archivo se llena con el contenido del Motor de Razonamiento
│       │       que ya existe en el proyecto de referencia.
│       │
│       ├── fase_0e.md
│       ├── fase_0a.md
│       ├── fase_0c.md
│       ├── fase_1a.md
│       ├── fase_1c.md
│       ├── fase_2a.md
│       ├── fase_5a.md
│       └── fase_gen.md
│           └── Propósito de cada uno: instrucciones específicas para esa fase.
│               Input esperado, output esperado, formato de respuesta.
│               En esta tarea se crean los archivos vacíos con el título
│               y la estructura. El contenido se llena en S2.3 y S3.1.
│
├── subagents/
│   ├── __init__.py
│   ├── probabilistic.py    ← vacío con firma de función
│   ├── adversarial.py      ← vacío con firma de función
│   ├── jurisprudence.py    ← vacío con firma de función
│   ├── qa.py               ← vacío con firma de función
│   └── extractor.py        ← vacío con firma de función
│
├── tools/
│   ├── __init__.py
│   ├── document_parser.py  ← vacío con firma de función
│   ├── web_search.py       ← vacío con firma de función
│   ├── word_generator.py   ← vacío con firma de función
│   └── db.py               ← vacío con firma de función
│
├── models/
│   ├── __init__.py
│   ├── caso.py             ← vacío con Pydantic models
│   ├── hecho.py            ← vacío con Pydantic models
│   ├── documento.py        ← vacío con Pydantic models
│   └── fase_output.py      ← vacío con Pydantic models
│
└── routers/
    ├── __init__.py
    ├── casos.py            ← vacío con los endpoints definidos pero sin lógica
    ├── chat.py             ← vacío con los endpoints definidos pero sin lógica
    ├── documentos.py       ← vacío con los endpoints definidos pero sin lógica
    └── fases.py            ← vacío con los endpoints definidos pero sin lógica
```

**Verificación:**
`cd apps/agents && pip install -r requirements.txt && uvicorn main:app --reload`
→ FastAPI corre en localhost:8000
→ `curl localhost:8000/health` retorna `{"status": "ok", "version": "0.1.0"}`
→ `localhost:8000/docs` muestra la documentación automática de OpenAPI

**Bloqueante de:** S0.5, S1.1, S2.1.

---

### TAREA S0.4 — Configurar Supabase y schema de base de datos

**Qué hace:**
Crea el proyecto en Supabase, activa la extensión pgvector, aplica el
schema completo con todas las tablas, y configura Row Level Security
para que los casos estén aislados. También crea las políticas de acceso
que garantizan que solo el usuario autenticado vea sus propios casos.

**Archivos a crear:**
```
packages/database/
├── schema.sql
│   └── Propósito: script SQL completo que crea todas las tablas en orden.
│       El orden importa por las foreign keys:
│       1. casos
│       2. partes (referencia casos)
│       3. hechos (referencia casos, tiene columna embedding vector(1536))
│       4. documentos (referencia casos, tiene columna embedding vector(1536))
│       5. sesiones (referencia casos)
│       6. outputs_fases (referencia casos)
│       7. jurisprudencia (tiene columna embedding vector(1536))
│       8. trazabilidad (referencia casos)
│       Al final del script: activar RLS en todas las tablas y crear
│       las políticas de acceso.
│
├── rls_policies.sql
│   └── Propósito: políticas de Row Level Security separadas del schema
│       para mayor claridad. Define que un usuario solo puede
│       SELECT/INSERT/UPDATE/DELETE sus propios registros.
│       La regla central es: auth.uid() debe coincidir con el user_id del caso.
│
└── seed_jurisprudencia.sql
    └── Propósito: datos iniciales de jurisprudencia clave para el sistema.
        Incluye las sentencias más importantes del derecho de familia
        colombiano (CC, CSJ) que ya están identificadas en la
        BASE_CONOCIMIENTO_JURIDICO.md del proyecto de referencia.
        En esta tarea se crea el archivo vacío con los primeros 5-10 registros.
```

**Verificación:**
Desde el dashboard de Supabase → Table Editor:
- Todas las tablas existen
- La extensión `vector` está activada (Settings → Extensions)
- RLS está ON en todas las tablas
- `SELECT * FROM casos` retorna vacío (sin error)

**Bloqueante de:** S0.5, S1.1, S2.1.

---

### TAREA S0.5 — Autenticación Magic Link

**Qué hace:**
Configura NextAuth.js con el provider de Email (Magic Link).
Cuando el abogado ingresa su correo, NextAuth envía un email con un link
de un solo uso. Al hacer clic, el abogado queda autenticado.
La whitelist de emails autorizados está en una variable de entorno —
si el correo no está en la lista, se muestra un error claro.

**Archivos a modificar:**
```
apps/web/app/api/auth/[...nextauth]/route.ts
└── Por qué: se llena con la configuración real de NextAuth.
    Define el provider Email, configura el adaptador de Supabase
    para guardar las sesiones, y verifica contra la whitelist.

apps/web/app/(auth)/login/page.tsx
└── Por qué: se conecta con la acción de NextAuth para enviar el Magic Link.
    Muestra estado de éxito ("Revisa tu correo") o error ("Email no autorizado").

apps/web/app/layout.tsx
└── Por qué: envuelve la app con SessionProvider de NextAuth
    para que todas las páginas puedan leer la sesión.

apps/web/lib/supabase.ts
└── Por qué: se llena con la configuración real del cliente Supabase
    usando las variables de entorno del proyecto creado en S0.4.
```

**Variables de entorno que deben existir para esta tarea:**
```
NEXTAUTH_SECRET          ← string aleatorio (se genera con openssl rand -base64 32)
NEXTAUTH_URL             ← http://localhost:3000
AUTHORIZED_USERS    ← correos reales del equipo del despacho
EMAIL_SERVER_HOST        ← servidor SMTP (puede ser Gmail con App Password)
EMAIL_SERVER_PORT        ← 587 para Gmail
EMAIL_SERVER_USER        ← correo desde el que se envía
EMAIL_SERVER_PASSWORD    ← App Password de Gmail
EMAIL_FROM               ← "LUMI Judicial <noreply@lumijudicial.com>"
```

**Verificación:**
1. Ir a localhost:3000/login
2. Ingresar el correo del abogado
3. Recibir el email con el link
4. Hacer clic en el link
5. Ser redirigido a /casos (aunque esté vacía)
6. Intentar con un correo no autorizado → ver mensaje de error

**Bloqueante de:** S1.3, S2.4.

---

### TAREA S0.6 — Modelos Pydantic (contratos de datos)

**Qué hace:**
Define todos los modelos de datos del sistema en Python usando Pydantic.
Estos modelos son el contrato entre el backend FastAPI y la base de datos.
Al tenerlos definidos antes de escribir la lógica, el agente de código
sabe exactamente qué forma tiene cada objeto en el sistema.

**Archivos a modificar:**
```
apps/agents/models/caso.py
└── Por qué: define Caso, CasoCreate, CasoUpdate con todos los campos
    tipados. Incluye los enums TipoAccion y EstadoCaso.

apps/agents/models/hecho.py
└── Por qué: define Hecho, HechoCreate con EstatusEpistemico como enum.

apps/agents/models/documento.py
└── Por qué: define Documento, DocumentoCreate, DocumentoExtracto
    (el resultado que retorna el subagente extractor).

apps/agents/models/fase_output.py
└── Por qué: define FaseOutput con el campo contenido como dict genérico.
    Incluye el enum Fase con los valores: fase_0e, fase_0a, fase_0c,
    fase_1a, fase_1c, fase_2a, fase_5a, fase_gen.

apps/agents/models/trazabilidad.py
└── Por qué: define TrazabilidadEntry para registrar cada llamada a Anthropic.
    Incluye modelo, tokens_input, tokens_output, costo_usd, duracion_ms.
```

**Verificación:**
`python -c "from models.caso import Caso; print('OK')"` sin errores de importación.
Todos los modelos importan correctamente desde `main.py`.

**Bloqueante de:** S1.1, S2.1.

---

## SPRINT 1 — EXTRACTOR DE DOCUMENTOS
### Objetivo: El abogado puede subir un documento y el sistema lo procesa automáticamente

---

### TAREA S1.1 — Herramienta de parsing de documentos

**Qué hace:**
Implementa la lógica de extracción de texto de archivos.
Para PDF y Word usa LlamaParse. Para imágenes (fotos de documentos,
recibos, actas escaneadas) usa Claude Vision.
La herramienta devuelve el texto extraído más un conjunto de metadatos
estructurados (fecha, valores, partes mencionadas) independientemente
del tipo de archivo.

**Archivos a modificar:**
```
apps/agents/tools/document_parser.py
└── Por qué: implementa la lógica central de extracción.
    Define la función parse_document(file_path, file_type) que:
    - Detecta el tipo de archivo
    - Llama a LlamaParse si es PDF o DOCX
    - Llama a Claude Vision si es JPG, PNG, JPEG
    - Retorna un objeto DocumentoExtracto con texto + metadatos
    El manejo de errores es explícito: si LlamaParse falla,
    intenta con pypdf como fallback.
```

**Qué debe detectar el extractor para cada tipo de documento:**
```
Actas ICBF:
  → tipo: "acta_icbf"
  → extraer: número de audiencia, fecha, partes, obligaciones pactadas

Facturas de pensión/matrícula:
  → tipo: "factura_educacion"
  → extraer: número de factura, fecha, valor, concepto, alumno

Facturas de salud:
  → tipo: "factura_salud"
  → extraer: número, fecha, valor, paciente, diagnóstico/medicamento

Registros civiles:
  → tipo: "registro_civil"
  → extraer: nombre completo, fecha de nacimiento, padres

Documentos de identidad:
  → tipo: "documento_identidad"
  → extraer: nombre, número de documento, fecha expedición

Facturas de uniformes/útiles:
  → tipo: "factura_educacion"
  → extraer: número, fecha, valor, proveedor

Resoluciones y actos administrativos:
  → tipo: "acto_administrativo"
  → extraer: número, fecha, autoridad, resuelve

Cualquier otro:
  → tipo: "otro"
  → extraer: texto completo sin estructura
```

**Verificación:**
Subir el Acta SIM 11054012 (PDF) → el extractor retorna:
- `tipo: "acta_icbf"`
- `texto`: el texto completo de las 5 páginas
- `metadatos.obligaciones`: lista con las 4 obligaciones principales del acta
- Sin errores de timeout

**Bloqueante de:** S1.2.

---

### TAREA S1.2 — Subagente extractor completo

**Qué hace:**
> Contrato de datos: ver Brief sección 3.8 — Subagente Extractor de Documentos
Orquesta el flujo completo de procesamiento de un documento.
Recibe el archivo, llama al parser del S1.1, luego llama a Claude Haiku
para extraer los hechos del caso en formato estructurado, y guarda
todo en Supabase (el texto en `documentos`, los hechos en `hechos`).

**Archivos a modificar:**
```
apps/agents/subagents/extractor.py
└── Por qué: implementa el subagente completo.
    La función extract_document(file_bytes, filename, caso_id) hace:
    1. Llama a document_parser.parse_document()
    2. Llama a Claude Haiku con el texto extraído y un prompt
       que dice: "extrae los hechos jurídicamente relevantes de
       este documento en formato JSON estructurado"
    3. Guarda el documento en tabla `documentos` via db.py
    4. Guarda cada hecho en tabla `hechos` via db.py
    5. Registra la llamada a Anthropic en `trazabilidad`
    6. Retorna el DocumentoExtracto con confirmación de guardado

apps/agents/tools/db.py
└── Por qué: implementa las funciones de base de datos que el extractor necesita:
    - save_documento(documento: Documento) → UUID del documento guardado
    - save_hecho(hecho: HechoCreate) → UUID del hecho guardado
    - log_trazabilidad(entry: TrazabilidadEntry) → void
    Usa el cliente de Supabase con service role key para operaciones
    del servidor (no del cliente).
```

**Verificación:**
Llamar directamente al subagente con el Acta SIM como bytes →
- Tabla `documentos` tiene un nuevo registro con el texto del acta
- Tabla `hechos` tiene al menos 4 registros (una por obligación del acta)
- Tabla `trazabilidad` tiene un registro con el modelo "claude-haiku-4-5"
  y el costo calculado

**Bloqueante de:** S1.3.

---

### TAREA S1.3 — Endpoint de documentos en FastAPI + UI de upload

**Qué hace:**
Crea el endpoint `POST /casos/{id}/documentos` que recibe el archivo
desde el frontend, lo valida (tipo, tamaño máximo 50MB), lo sube a
Supabase Storage, y lanza el subagente extractor.
En paralelo, crea el componente de UI que permite al abogado arrastrar
archivos y ver el progreso.

**Archivos a modificar:**
```
apps/agents/routers/documentos.py
└── Por qué: implementa el endpoint de upload.
    Valida que el tipo de archivo sea permitido.
    Sube el archivo a Supabase Storage en la ruta casos/{id}/{filename}.
    Llama al subagente extractor de forma asíncrona (no hace esperar al abogado).
    Retorna inmediatamente con {"status": "procesando", "documento_id": uuid}.
    El frontend consulta el estado del documento periódicamente (polling).

apps/agents/routers/documentos.py (GET endpoint)
└── Por qué: implementa GET /casos/{id}/documentos.
    Retorna la lista de documentos del caso con su tipo detectado,
    fecha de carga y estado (procesando/procesado/error).

apps/web/components/DocumentUpload/DropZone.tsx
└── Por qué: implementa el área de drop de archivos.
    Al soltar un archivo: muestra spinner de "subiendo...",
    llama al endpoint de upload, y empieza a hacer polling cada 2
    segundos hasta que el estado cambia a "procesado".
    Al completarse muestra: "✅ Acta ICBF detectada — 4 hechos extraídos"

apps/web/app/casos/[id]/documentos/page.tsx
└── Por qué: muestra la lista de documentos del caso con el DropZone.
    Cada documento aparece con su ícono según tipo, nombre, fecha
    y el número de hechos extraídos.
```

**Verificación:**
1. El abogado va a /casos/{id}/documentos
2. Arrastra el Acta SIM 11054012
3. Ve el spinner de "procesando..."
4. Después de ~10 segundos ve "✅ Acta ICBF detectada — 4 hechos extraídos"
5. El documento aparece en la lista

**Bloqueante de:** S2.3 (para poder probar las fases con documentos reales).

---

## SPRINT 2 — LUMI CORE + FASES 0E, 0A, 0C
### Objetivo: La conversación con LUMI funciona y ejecuta las tres primeras fases

---

### TAREA S2.1 — Context Manager

**Qué hace:**
Implementa el mecanismo central que evita que la ventana de contexto
se sature. En lugar de cargar todo el historial, construye un contexto
"inteligente" que contiene solo lo necesario para la fase actual.
Es la pieza más crítica del sistema — si falla, el sistema pierde
coherencia entre sesiones.

**Archivos a modificar:**
```
apps/agents/core/context_manager.py
└── Por qué: implementa la función build_context(caso_id, fase_actual).
    El proceso que sigue:

    1. Carga el prompt maestro desde sistema_base.md (siempre presente)

    2. Carga los outputs de fases anteriores desde la tabla outputs_fases.
       Solo carga los que tienen aprobado_pablo = true.
       Cada output es un resumen de 500-800 tokens.

    3. Busca los hechos más relevantes para la fase actual.
       Hace una búsqueda semántica en la tabla hechos usando pgvector:
       convierte el nombre de la fase en un embedding y busca
       los 10 hechos más similares semánticamente.
       Esto evita cargar los 200+ hechos del caso completo.

    4. Carga los últimos 20 mensajes de la sesión actual
       desde la tabla sesiones.

    5. Carga el prompt específico de la fase desde fase_XX.md

    6. Concatena todo en el orden correcto y retorna el string.
       Si el total supera 30.000 tokens, hace una segunda ronda
       de compresión: reduce los hechos a los 5 más relevantes.

    También implementa compress_session(caso_id, fase):
    Toma los mensajes de la fase recién aprobada, llama a Claude Haiku
    para generar un resumen estructurado de 500-800 tokens,
    y lo guarda en outputs_fases.

apps/agents/tools/db.py
└── Por qué: agrega las funciones que el context manager necesita:
    - get_outputs_fases(caso_id) → list[FaseOutput]
    - get_ultimos_mensajes(caso_id, n=20) → list[dict]
    - search_hechos_semanticos(caso_id, query_embedding, limit=10) → list[Hecho]
    - save_sesion_mensaje(caso_id, rol, contenido) → void
    - save_output_fase(output: FaseOutput) → void
```

**Verificación:**
Llamar a `build_context(caso_id, "fase_0e")` con el caso de prueba →
- El string resultante tiene menos de 30.000 tokens
- Contiene el prompt maestro
- Contiene los hechos extraídos del Acta SIM
- No contiene historial de mensajes anterior (sesión nueva)

**Bloqueante de:** S2.2.

---

### TAREA S2.2 — LUMI Core — motor de conversación

**Qué hace:**
Implementa el agente principal que recibe el mensaje del abogado,
construye el contexto con el Context Manager, llama a Claude Sonnet,
guarda el intercambio en la sesión, y retorna la respuesta.
También detecta cuando LUMI produce un output de fase completo
y lo guarda automáticamente en `outputs_fases`.

**Archivos a modificar:**
```
apps/agents/core/lumi_core.py
└── Por qué: implementa la función process_message(caso_id, mensaje_pablo).
    El flujo que sigue:
    1. Carga el caso de la BD para saber la fase actual
    2. Llama a context_manager.build_context(caso_id, fase_actual)
    3. Arma el array de messages para Anthropic:
       [{"role": "system", "content": contexto}, ...últimos mensajes...,
        {"role": "user", "content": mensaje_pablo}]
    4. Llama a Claude Sonnet con ese array
    5. Guarda el mensaje del abogado y la respuesta de LUMI en sesiones
    6. Registra la llamada en trazabilidad
    7. Detecta si la respuesta contiene un output de fase estructurado
       (LUMI usa un formato especial cuando termina una fase)
    8. Si detecta output de fase: lo guarda en outputs_fases
    9. Retorna la respuesta de LUMI

apps/agents/routers/chat.py
└── Por qué: implementa los endpoints de chat.
    POST /casos/{id}/chat: recibe el mensaje, llama a lumi_core.process_message,
    retorna la respuesta.
    GET /casos/{id}/chat/historial: retorna los últimos N mensajes
    de la sesión actual para que el frontend los muestre.

apps/agents/routers/casos.py
└── Por qué: implementa los endpoints CRUD de casos.
    POST /casos: crea un caso nuevo con nombre y tipo de acción.
    GET /casos: lista los casos del usuario autenticado.
    GET /casos/{id}: retorna el detalle del caso incluyendo fase actual.
    PATCH /casos/{id}: actualiza el estado o la fase actual.
```

**Verificación:**
`curl -X POST localhost:8000/casos/{id}/chat -d '{"mensaje": "Hola LUMI"}'`
→ LUMI responde con el saludo de inicio de caso
→ La tabla `sesiones` tiene un nuevo registro con los dos mensajes
→ La tabla `trazabilidad` tiene el registro de la llamada

**Bloqueante de:** S2.3.

---

### TAREA S2.3 — Prompts de las fases 0E, 0A, 0C

**Qué hace:**
Llena los archivos de prompt para las tres primeras fases con el
contenido real del motor de razonamiento de LUMI. Estos archivos son
el corazón del sistema — definen exactamente qué analiza LUMI en cada
fase, qué preguntas hace, y qué formato tiene el output.
El contenido base existe en el Motor de Razonamiento del proyecto
de referencia y debe adaptarse al formato de archivos .md del sistema.

**Archivos a modificar:**
```
apps/agents/core/prompts/sistema_base.md
└── Por qué: se llena con el prompt maestro completo de LUMI.
    Incluye: quién es LUMI, el principio de firma (El abogado decide y firma),
    las 7 reglas que nunca abandona, los formatos de input que acepta,
    y las instrucciones sobre cómo usar los outputs de fases anteriores.

apps/agents/core/prompts/fase_0e.md
└── Por qué: se llena con las instrucciones de la Fase 0E — Análisis Ético.
    Define: las 4 verificaciones (conflicto de interés, solidez de pretensión,
    señales de omisión, responsabilidad del cliente), el formato del semáforo
    por verificación, y la condición de bloqueo si detecta problema grave.
    Define el formato JSON del output estructurado que LUMI debe producir
    al final de la fase para que el Context Manager lo detecte y guarde.

apps/agents/core/prompts/fase_0a.md
└── Por qué: se llena con las instrucciones de la Fase 0A — Auditoría de Hechos.
    Define: qué verificar para un proceso ejecutivo (título, cuantía, mora,
    pagos parciales, bienes del deudor), cómo marcar los vacíos como [DESCONOCIDO],
    la regla de no asumir hechos sin confirmación del abogado,
    y el formato del output estructurado con hechos verificados + lista de vacíos.

apps/agents/core/prompts/fase_0c.md
└── Por qué: se llena con las instrucciones de la Fase 0C — Estrategia Inicial.
    Define: el árbol de decisión para elegir la acción jurídica correcta,
    la verificación de competencia y caducidad, y el formato del output
    con las 2-3 rutas posibles y sus comparativas.
```

**Verificación:**
Ejecutar las 3 fases sobre el caso *Sayago vs. Roldán* (con los documentos
ya subidos en S1.3):
- Fase 0E retorna semáforo 🟢 + decisión de continuar
- Fase 0A retorna los 13 hechos verificados + lista de vacíos conocidos
- Fase 0C retorna árbol de decisión con proceso ejecutivo como acción principal

**Bloqueante de:** S2.4.

---

### TAREA S2.4 — UI conversacional completa

**Qué hace:**
Conecta el frontend con el backend para que la conversación sea
completamente funcional. El abogado escribe, LUMI responde, el historial
se muestra correctamente, y el indicador de fases refleja el estado real.

**Archivos a modificar:**
```
apps/web/components/Chat/ChatWindow.tsx
└── Por qué: se conecta con el endpoint GET /casos/{id}/chat/historial
    para cargar los mensajes al abrir la página. Diferencia visualmente
    mensajes de sistema (grises, información de fase) y mensajes
    normales de conversación.

apps/web/components/Chat/MessageInput.tsx
└── Por qué: se conecta con el endpoint POST /casos/{id}/chat.
    Implementa streaming de la respuesta si Anthropic lo soporta,
    o polling cada segundo hasta que la respuesta llegue.
    Bloquea el input mientras LUMI está respondiendo.

apps/web/components/Chat/FaseIndicator.tsx
└── Por qué: se conecta con GET /casos/{id} para leer la fase actual.
    Muestra las 8 fases como pasos visuales (completado/actual/pendiente).
    Incluye el botón "Aprobar esta fase" que llama a
    POST /casos/{id}/fases/{fase}/aprobar.

apps/web/app/casos/page.tsx
└── Por qué: se conecta con GET /casos para mostrar la lista real de casos.
    Incluye el botón "Nuevo caso" que abre un modal con nombre y tipo de acción.
    Al crear, llama a POST /casos y redirige al chat del caso nuevo.

apps/agents/routers/fases.py
└── Por qué: implementa el endpoint POST /casos/{id}/fases/{fase}/aprobar.
    Al aprobarse una fase:
    1. Llama a context_manager.compress_session(caso_id, fase)
       para comprimir el historial de esa fase en un resumen
    2. Actualiza fase_actual en la tabla casos a la siguiente fase
    3. Retorna confirmación
```

**Verificación:**
1. El abogado va a /casos, ve el caso creado
2. Entra al chat, escribe "analiza el caso"
3. LUMI responde con el análisis de la Fase 0E
4. El abogado hace clic en "Aprobar fase"
5. El indicador de fases avanza a 0A
6. El abogado puede cerrar el navegador, volver a entrar, y la conversación
   y la fase están exactamente donde las dejó

**Bloqueante de:** S3.1.

---

## SPRINT 3 — FASES 1A, 1C + SUBAGENTES 2A Y 5A
### Objetivo: El motor de razonamiento completo está funcionando

---

### TAREA S3.1 — Prompts de fases 1A, 1C y generación de borrador

**Qué hace:**
Llena los prompts de las fases intermedias y la fase de generación.
Fase 1A produce el cuestionario que el abogado le hace al cliente.
Fase 1C construye la teoría del caso — la narrativa central.
Fase GEN genera el borrador jurídico completo.

**Archivos a modificar:**
```
apps/agents/core/prompts/fase_1a.md
└── Por qué: define el cuestionario crítico al cliente.
    Incluye la instrucción de ordenar las preguntas por impacto,
    y que la última pregunta siempre sea la de información no revelada.
    El output es una lista numerada de preguntas con la justificación
    de por qué cada una importa.

apps/agents/core/prompts/fase_1c.md
└── Por qué: define la construcción de la teoría del caso.
    Incluye: la oración central, el arco narrativo completo,
    los 3 hechos más poderosos para el juez, y la imagen mental final.

apps/agents/core/prompts/fase_gen.md
└── Por qué: define la generación del borrador jurídico.
    Incluye la estructura completa de la demanda (partes, pretensiones,
    hechos, fundamentos, competencia, cuantía, pruebas, medidas cautelares,
    notificaciones, juramento).
    La instrucción crítica: lo que no puede verificarse se marca 🔴 VERIFICAR.
    Al final del borrador siempre incluir el protocolo de verificación.
```

**Verificación:**
Ejecutar Fase 1A sobre el caso de referencia → el output incluye las
11 preguntas críticas identificadas en el caso Sayago vs. Roldán.
Ejecutar Fase 1C → el output incluye la oración central y el arco narrativo.

**Bloqueante de:** S3.2, S3.3.

---

### TAREA S3.2 — Subagente Motor Probabilístico (Fase 2A)

**Qué hace:**
> Contrato de datos: ver Brief sección 3.8 — Subagente Motor Probabilístico (Fase 2A)
Implementa el subagente que calcula la probabilidad de éxito del caso.
La característica más importante: corre en una sesión completamente aislada.
No tiene acceso al historial de conversación con el abogado. Solo recibe
los hechos estructurados del caso. Esto evita el sesgo de confirmación
— el subagente no sabe qué construyó LUMI Core y debe evaluar desde cero.

**Archivos a modificar:**
```
apps/agents/subagents/probabilistic.py
└── Por qué: implementa la función run(caso_id) → ProbabilisticOutput.
    El proceso:
    1. Carga los hechos del caso desde la BD (no el historial)
    2. Carga el tipo de acción del caso
    3. Carga el prompt de la fase 2A (fase_2a.md)
    4. Hace UNA llamada a Claude Haiku con los hechos + prompt
       SIN ningún historial de conversación previo
    5. Parsea el output estructurado (rango, factores, justificaciones)
    6. Registra en trazabilidad
    7. Retorna ProbabilisticOutput

apps/agents/core/prompts/fase_2a.md
└── Por qué: define el modelo bayesiano de evaluación.
    Lista los factores a evaluar para cada tipo de acción (+/-/~/?)
    y la fórmula de traducción cualitativa a rango numérico.
    Define el formato de output: [RANGO: X%-Y%] con centro de masa en Z%.
    Incluye la advertencia epistemológica obligatoria sobre la naturaleza
    estimativa de las probabilidades.
```

**Verificación:**
Llamar directamente a `probabilistic.run(caso_id)` con el caso de referencia
→ retorna rango [67%-82%] o similar
→ el output NO contiene ninguna referencia a la conversación con el abogado
→ la tabla trazabilidad registra que el modelo usado fue "claude-haiku-4-5"

**Bloqueante de:** S3.4.

---

### TAREA S3.3 — Subagente Simulación Adversarial (Fase 5A)

**Qué hace:**
> Contrato de datos: ver Brief sección 3.8 — Subagente Simulación Adversarial (Fase 5A)
Implementa el subagente que simula al mejor abogado de la contraparte.
Aislamiento total: no sabe qué construyó LUMI Core, no tiene el historial
de conversación. Solo recibe los hechos del caso y la teoría del caso.
El aislamiento es la condición sine qua non de la utilidad de este subagente —
si supiera qué ya construyó LUMI, produciría ataques que LUMI Core
ya anticipó, sin aportar nada.

**Archivos a modificar:**
```
apps/agents/subagents/adversarial.py
└── Por qué: implementa la función run(caso_id) → AdversarialOutput.
    El proceso:
    1. Carga los hechos del caso desde la BD
    2. Carga el output de la Fase 1C (teoría del caso) desde outputs_fases
    3. NO carga el historial de conversación
    4. NO carga los outputs de fases 0E, 0A, 0C (para evitar contaminación)
    5. Llama a Claude Sonnet con hechos + teoría del caso + prompt adversarial
    6. Parsea: lista de 5 argumentos, ataque no obvio, vulnerabilidad probatoria
    7. Registra en trazabilidad
    8. Retorna AdversarialOutput

apps/agents/core/prompts/fase_5a.md
└── Por qué: define el rol del subagente adversarial.
    Instrucción central: "Eres el mejor abogado de la contraparte.
    Tu único objetivo es destruir el caso que se describe."
    Define: 5 argumentos más sólidos, el ataque no obvio (el que un
    abogado promedio no usaría), y la vulnerabilidad probatoria más peligrosa.
```

**Verificación:**
Llamar a `adversarial.run(caso_id)` con el caso de referencia →
- Retorna exactamente 5 argumentos numerados
- Incluye "el ataque no obvio" explícitamente
- Incluye "vulnerabilidad probatoria más peligrosa"
- Ningún argumento replica exactamente lo que LUMI Core ya anticipó

**Bloqueante de:** S3.4.

---

### TAREA S3.4 — Integración de subagentes en LUMI Core

**Qué hace:**
Conecta los subagentes 2A y 5A con el flujo principal.
LUMI Core detecta cuándo está en la fase correcta y delega a los
subagentes, integra sus outputs en la respuesta que le da al abogado,
y guarda los resultados en `outputs_fases`.

**Archivos a modificar:**
```
apps/agents/core/lumi_core.py
└── Por qué: agrega la lógica de delegación a subagentes.
    Cuando la fase actual es "fase_2a": llama a probabilistic.run(caso_id),
    recibe el output, y lo presenta al abogado como parte de la conversación.
    Cuando la fase actual es "fase_5a": llama a adversarial.run(caso_id),
    recibe el output, y lo integra en la respuesta de LUMI.
    En ambos casos el resultado se guarda en outputs_fases antes
    de presentarlo al abogado.
```

**Verificación:**
Ejecutar el caso de referencia hasta la Fase 2A desde la interfaz →
El abogado ve en el chat el rango de probabilidad con los factores.
Ejecutar hasta la Fase 5A → El abogado ve los 5 argumentos en contra.
Aprobar ambas fases → los outputs quedan guardados y el contexto avanza.

**Bloqueante de:** S4.1.

---

## SPRINT 4 — CONTROL DE CALIDAD + BORRADOR WORD
### Objetivo: El sistema genera el documento jurídico final

---

### TAREA S4.1 — Subagente Control de Calidad (QA)

**Qué hace:**
> Contrato de datos: ver Brief sección 3.8 — Subagente Control de Calidad QA
Implementa el subagente que revisa el borrador antes de entregárselo
al abogado. Su función es detectar errores antes de que el abogado los vea.
Corre automáticamente — El abogado nunca lo activa manualmente.

**Archivos a modificar:**
```
apps/agents/subagents/qa.py
└── Por qué: implementa la función run(borrador_texto, caso_id) → QAOutput.
    El QA verifica una checklist específica:
    - Coherencia interna: los hechos no se contradicen entre sí
    - Todas las pretensiones tienen sustento fáctico documentado
    - Las citas normativas son pertinentes al tipo de acción
    - El juramento estimatorio cuadra con los números de la liquidación
    - Los datos de identificación de las partes son correctos
    - Las medidas cautelares están bien formuladas
    - El protocolo de verificación está incluido al final
    Usa Claude Haiku porque es una tarea de verificación estructurada.
    Retorna QAOutput con semáforo general y lista de correcciones
    clasificadas como 🔴 críticas / 🟡 importantes / 🟢 complementarias.
    Si hay correcciones 🔴, las aplica automáticamente y genera
    un borrador v2 antes de entregárselo al abogado.
```

**Verificación:**
Introducir intencionalmente un error en el borrador del caso de referencia
(cambiar un número de cédula) → QA lo detecta como corrección 🔴 crítica
y la lista en el output.

**Bloqueante de:** S4.2.

---

### TAREA S4.2 — Generador de borrador Word

**Qué hace:**
Implementa la herramienta que convierte el borrador en texto que produce
LUMI Core en un archivo .docx descargable con formato jurídico profesional.
Usa python-docx para generar el archivo con las mismas características
que el borrador del caso de referencia: tablas de liquidación, texto
justificado, marcadores 🔴 VERIFICAR en rojo, protocolo de verificación
al final.

**Archivos a modificar:**
```
apps/agents/tools/word_generator.py
└── Por qué: implementa generate_docx(borrador_texto, caso_id) → bytes.
    Parsea el texto del borrador (que tiene estructura de secciones
    identificables: pretensiones, hechos, fundamentos, etc.)
    y lo convierte a un documento Word con:
    - Fuente Times New Roman 12pt, interlineado 1.5
    - Márgenes de 2.5cm en todos los lados
    - Secciones numeradas en negrita y subrayado
    - Tablas de liquidación formateadas con colores
    - Texto 🔴 VERIFICAR en color rojo para que el abogado los vea de inmediato
    - Protocolo de verificación al final en tabla con semáforo
    Guarda el .docx en Supabase Storage en la ruta casos/{id}/borrador_v{n}.docx
    Retorna los bytes del archivo para la descarga directa.
```

**Verificación:**
Llamar a `word_generator.generate_docx(borrador, caso_id)` con el borrador
del caso de referencia → el .docx generado contiene todas las secciones,
las tablas de liquidación son legibles, y los marcadores 🔴 están en rojo.
El archivo se puede abrir en Word sin errores.

**Bloqueante de:** S4.3.

---

### TAREA S4.3 — Flujo completo de generación y descarga

**Qué hace:**
Conecta todos los componentes del Sprint 4: cuando LUMI Core termina
la Fase GEN, automáticamente llama al QA, aplica las correcciones,
llama al generador Word, y deja el archivo disponible para descarga.
El abogado ve en el chat el resultado del QA y puede descargar el .docx.

**Archivos a modificar:**
```
apps/agents/core/lumi_core.py
└── Por qué: agrega el flujo de generación al final de la Fase GEN.
    Cuando LUMI produce el borrador completo:
    1. Llama a qa.run(borrador, caso_id) para revisión
    2. Si hay correcciones 🔴: las aplica y genera borrador v2
    3. Llama a word_generator.generate_docx(borrador_final, caso_id)
    4. Guarda el path del .docx en la tabla outputs_fases
    5. Informa al abogado en el chat: "El borrador está listo.
       QA encontró X correcciones (todas aplicadas). Puedes descargarlo."

apps/agents/routers/fases.py
└── Por qué: agrega el endpoint GET /casos/{id}/borrador.
    Recupera el path del .docx desde outputs_fases,
    obtiene el archivo de Supabase Storage,
    y lo retorna como descarga con el Content-Type correcto.

apps/web/components/Chat/ChatWindow.tsx
└── Por qué: detecta cuando un mensaje de LUMI contiene la señal
    de "borrador listo" y muestra un botón de descarga en el chat,
    sin que el abogado tenga que ir a otra página.
```

**Verificación:**
Ejecutar el caso de referencia completo desde la interfaz hasta la Fase GEN →
- LUMI produce el borrador en el chat
- El QA corre automáticamente
- El botón "Descargar borrador" aparece en el chat
- El .docx descargado es equivalente al de referencia

**Bloqueante de:** S5.1.

---

## SPRINT 5 — JURISPRUDENCIA, COSTOS Y PULIDO FINAL
### Objetivo: Sistema completo, desplegado y verificado con el caso de referencia

---

### TAREA S5.1 — Subagente de Verificación de Jurisprudencia

**Qué hace:**
> Contrato de datos: ver Brief sección 3.8 — Subagente Verificación de Jurisprudencia
Implementa el subagente que verifica cada sentencia citada en el borrador.
Busca en tres capas: primero en la base de conocimiento interna (el MD),
luego en Tavily para búsqueda web en fuentes colombianas oficiales,
y si no encuentra, marca como 🔴 VERIFICAR. Nunca inventa ni supone.

**Archivos a modificar:**
```
apps/agents/subagents/jurisprudence.py
└── Por qué: implementa run(lista_citas) → JurisprudenceOutput.
    Para cada cita en la lista:
    1. Busca en la tabla jurisprudencia de la BD (búsqueda exacta por número)
    2. Si no encuentra: busca en BASE_CONOCIMIENTO_JURIDICO.md
    3. Si no encuentra: llama a Tavily con query:
       "{corporación} {número} Colombia jurisprudencia"
       Fuentes prioritarias: corteconstitucional.gov.co, cortesuprema.gov.co,
       consejodeestado.gov.co, suin-juriscol.gov.co
    4. Si Tavily encuentra: extrae el ratio decidendi y guarda en la BD
       para futuras búsquedas (aprendizaje incremental)
    5. Si nada encuentra: marca como 🔴 VERIFICAR con instrucción específica
    Retorna tabla de verificación con semáforo por cada sentencia.

apps/agents/tools/web_search.py
└── Por qué: implementa search_jurisprudencia(query) usando la API de Tavily.
    Configura Tavily para buscar solo en dominios .gov.co y fuentes jurídicas.
    Limita los resultados a 5 por búsqueda y filtra por relevancia.
```

**Verificación:**
Llamar a `jurisprudence.run(["T-123/2020", "SU-456/2019", "INEXISTENTE-000"])`:
- T-123/2020 y SU-456/2019: retornan ✅ con el ratio decidendi
- INEXISTENTE-000: retorna 🔴 VERIFICAR con mensaje claro

**Bloqueante de:** S5.2.

---

### TAREA S5.2 — Dashboard de costos por caso

**Qué hace:**
Implementa la vista que muestra al abogado cuánto ha costado en términos
de tokens y dinero cada caso. Lee directamente de la tabla `trazabilidad`.
Esto permite al estudio de abogados calcular el costo por caso y
eventualmente definir el precio del servicio.

**Archivos a modificar:**
```
apps/agents/routers/casos.py
└── Por qué: agrega el endpoint GET /casos/{id}/costos.
    Consulta la tabla trazabilidad para el caso dado.
    Agrupa por modelo y retorna:
    - Total tokens consumidos (input + output)
    - Costo total en USD
    - Costo por modelo (sonnet vs haiku)
    - Costo por subagente (extractor, probabilistic, adversarial, qa, jurisprudencia)
    - Desglose por fase del proceso

apps/web/components/Chat/ (nuevo componente)
└── CostIndicator.tsx
    └── Propósito: pequeño indicador en la barra lateral del caso
        que muestra el costo acumulado en USD. Se actualiza en tiempo real
        al recibir cada respuesta de LUMI.
```

**Verificación:**
Al final del caso de referencia completo, el endpoint retorna:
- Costo total > $0 y < $10 USD (rango esperado para un caso completo)
- El desglose por subagente muestra que Haiku es más barato que Sonnet
- El componente en la UI lo muestra correctamente

---

### TAREA S5.3 — Tests con pytest

**Qué hace:**
Implementa los tests que validan el comportamiento del sistema.
No son tests de integración completos — son tests unitarios que
validan la lógica de cada módulo de forma aislada usando mocks
para las llamadas a APIs externas (Anthropic, Tavily, Supabase).

**Archivos a crear:**
```
apps/agents/tests/
├── conftest.py
│   └── Propósito: fixtures compartidos. Define el caso de prueba base
│       (una versión simplificada del caso Sayago vs. Roldán con los
│       datos reales pero reducida a los hechos mínimos necesarios).
│       Define mocks para la API de Anthropic que retornan respuestas
│       predefinidas sin hacer llamadas reales.
│
├── test_extractor.py
│   └── Propósito: valida que el extractor detecta correctamente el tipo
│       de documento y extrae los metadatos esperados.
│       Test principal: extraer el Acta SIM → tipo "acta_icbf" + 4 obligaciones.
│
├── test_context_manager.py
│   └── Propósito: valida que el contexto construido tiene menos de 30.000 tokens
│       y contiene los elementos correctos.
│       Test principal: contexto para fase_0e con caso completo → < 30.000 tokens.
│
├── test_probabilistic.py
│   └── Propósito: valida el formato del output del Motor Probabilístico.
│       Test principal: retorna un rango válido entre 0% y 100%
│       con al menos 3 factores evaluados.
│
├── test_adversarial.py
│   └── Propósito: valida que el output del adversarial tiene la estructura correcta.
│       Test principal: retorna exactamente 5 argumentos + 1 ataque no obvio
│       + 1 vulnerabilidad probatoria.
│
├── test_qa.py
│   └── Propósito: valida que el QA detecta errores introducidos intencionalmente.
│       Test principal: borrador con cédula incorrecta → QA retorna corrección 🔴.
│
└── test_word_generator.py
    └── Propósito: valida que el generador produce un .docx sin errores.
        Test principal: generar .docx con el borrador de referencia → archivo válido
        que se puede abrir con python-docx sin excepciones.
```

**Verificación:**
`pytest apps/agents/tests/ -v --cov=apps/agents --cov-report=term-missing`
→ cobertura ≥ 80% en módulos `core/` y `subagents/`
→ 0 tests fallidos

---

### TAREA S5.4 — Deploy a producción

**Qué hace:**
Despliega el sistema en los servicios cloud para que el abogado pueda
acceder desde su navegador sin necesidad de correr nada localmente.

**Archivos a modificar:**
```
apps/web/vercel.json (nuevo)
└── Propósito: configuración de Vercel. Define las variables de entorno
    de producción y el comando de build de Next.js.

apps/agents/railway.toml (o render.yaml) (nuevo)
└── Propósito: configuración del servicio cloud para FastAPI.
    Define el comando de inicio: uvicorn main:app --host 0.0.0.0 --port $PORT
    y las variables de entorno de producción.

README.md
└── Por qué: se completa con las instrucciones de setup en 5 pasos:
    1. Clonar el repositorio
    2. Copiar .env.example a .env.local y llenar las variables
    3. docker-compose up
    4. Aplicar el schema de Supabase
    5. npm run dev / uvicorn main:app --reload
```

**Verificación — La más importante del proyecto:**
El abogado accede desde su navegador personal a la URL de producción →
ejecuta el caso *Sayago Álzate vs. Roldán Morales* completo →
desde "describe el caso" hasta "descargar borrador" →
el .docx generado es equivalente al producido manualmente en la sesión
de referencia.

**Esta verificación ejecuta la Prueba de aceptación final definida en Brief sección 5.1.**

---

## RESUMEN DE DEPENDENCIAS

```
S0.1 (estructura repo)
  └──► S0.2 (Next.js)
  │      └──► S0.5 (Auth Magic Link)
  │               └──► S1.3 (UI upload)
  │               └──► S2.4 (UI chat)
  │
  └──► S0.3 (FastAPI)
  │      └──► S0.6 (modelos Pydantic)
  │               └──► S1.1 (document parser)
  │                       └──► S1.2 (subagente extractor)
  │                               └──► S1.3 (endpoint upload)
  │
  └──► S0.4 (Supabase schema)
         └──► S0.5, S0.6, S1.2
         └──► S2.1 (context manager)
                └──► S2.2 (lumi core)
                       └──► S2.3 (prompts fases 0E/0A/0C)
                               └──► S2.4 (UI chat)
                                      └──► S3.1 (prompts 1A/1C/GEN)
                                             └──► S3.2 (probabilistic)
                                             └──► S3.3 (adversarial)
                                                    └──► S3.4 (integración)
                                                           └──► S4.1 (QA)
                                                                  └──► S4.2 (word gen)
                                                                         └──► S4.3 (flujo completo)
                                                                                └──► S5.1 (jurisprudencia)
                                                                                └──► S5.2 (costos)
                                                                                └──► S5.3 (tests)
                                                                                └──► S5.4 (deploy)
```

---

## DECISIONES TÉCNICAS TOMADAS EN ESTE PLAN

Estas decisiones se tomaron para reducir la incertidumbre al ejecutar.
Si quieren cambiar alguna, hacerlo antes de empezar — no en medio del sprint.

| Decisión | Elección | Por qué |
|----------|----------|---------|
| Autenticación | Magic Link (email) | Sin contraseñas, sin complejidad. Un solo correo en whitelist en .env |
| ORM Python | Supabase Client (no SQLAlchemy) | Ya están en Supabase, el cliente propio es más simple para este caso |
| Deploy FastAPI | Railway | Git push y listo. Sin configuración de servidor. ~$5/mes |
| Streaming de chat | Polling cada 1s | Más simple que streaming real para el MVP. Se mejora en v2 |
| Monorepo | Sin herramienta de orquestación | Turborepo agrega complejidad innecesaria para este tamaño |
| Embeddings | text-embedding-3-small de OpenAI vía Supabase | Mejor soporte nativo en pgvector. Cambiar si Anthropic lanza embeddings |
| Formato de prompts | Archivos .md en el repo | Editables sin tocar código. Versionados con git |
| Tests de API | Mocks (sin llamadas reales) | Los tests no deben consumir tokens ni dinero de Anthropic |

---

*LUMI Judicial — Plan de Implementación v2.0 · Abril 2026*
*Próximo paso: ejecutar S0.1 — crear la estructura del repositorio*
