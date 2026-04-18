# LUMI Judicial — Cursor Rules

## Documentos de referencia
- Brief del sistema: `LUMI_JUDICIAL_TECHNICAL_BRIEF_v2.md`
- Plan de implementación: `LUMI_JUDICIAL_IMPLEMENTATION_PLAN_v2.md`
- Antes de generar cualquier código, verifica que lo que vas a crear
  esté especificado en uno de estos dos documentos.

## Stack — no negociable
- Frontend: Next.js 14 con App Router, TypeScript estricto, Tailwind CSS
- Backend: FastAPI, Python 3.11+, type hints en todos los módulos
- SDK de IA: anthropic oficial — sin LangChain, sin abstracciones intermedias
- Base de datos: Supabase (PostgreSQL + pgvector + Storage)
- Tests: pytest con mocks para APIs externas — nunca llamadas reales a Anthropic

## Estructura del repositorio
- Todo el código frontend vive en `apps/web/`
- Todo el código de agentes vive en `apps/agents/`
- Los modelos Pydantic viven en `apps/agents/models/`
- Los prompts de fases viven en `apps/agents/core/prompts/` como archivos .md
- No crear archivos fuera de la estructura definida en Brief sección 3.1

## Contratos de datos
- Los tipos de input y output de cada agente están definidos en Brief sección 3.8
- No modificar esos contratos sin revisión humana explícita
- Todos los modelos heredan de `pydantic.BaseModel`
- Usar `UUID4` para todos los identificadores, nunca `int` autoincremental

## Agentes y subagentes
- LUMI Core usa `claude-sonnet-4-5` — no cambiar el modelo sin autorización
- Subagentes 2A, QA, Extractor y Jurisprudencia usan `claude-haiku-4-5`
- Subagente 5A usa `claude-sonnet-4-5` — aislamiento total, sin historial
- Ningún subagente recibe el historial de conversación de LUMI Core
- Cada llamada a Anthropic debe registrarse en la tabla `trazabilidad`

## Seguridad
- Nunca hardcodear credenciales — todas las claves van en variables de entorno
- El archivo `.env` nunca se sube a git
- Las variables de entorno están documentadas en `.env.example`
- Row Level Security activo en todas las tablas de Supabase

## Principio deontológico
- LUMI propone — el abogado decide y firma
- El sistema nunca toma decisiones jurídicas autónomas
- Este principio debe reflejarse en los mensajes que LUMI produce

## Orden de implementación
- Primero interfaces y tipos (models/)
- Luego implementaciones (core/, subagents/, tools/)
- Finalmente integración y tests
- No avanzar al siguiente bloque sin verificación humana del anterior

## Lo que nunca debes hacer
- No instalar librerías no aprobadas en el brief
- No modificar archivos de prompts .md sin instrucción explícita
- No saltarte fases del plan de implementación
- No generar tests que hagan llamadas reales a la API de Anthropic
- La dependencia de parsing de documentos es `llama-parse` con guión
