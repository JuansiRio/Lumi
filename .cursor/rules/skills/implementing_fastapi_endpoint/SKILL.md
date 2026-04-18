---
name: implementing-fastapi-endpoint
description: >-
  Implements or updates FastAPI routers in apps/agents/routers/: Pydantic-validated
  inputs, session auth from headers, agent/tool calls, db persistence, trazabilidad
  when Anthropic is used, typed responses and correct HTTP status codes.
  Use when the implementation plan touches apps/agents/routers/ or Brief section 3.4 APIs.
---

# Implementing FastAPI endpoints (LUMI agents)

## Descripción
Patrón para implementar endpoints FastAPI en `apps/agents/routers/`.

## Cuándo usar este skill
Cuando el implementation plan indique implementar o modificar un archivo en `apps/agents/routers/`.

## Patrón de implementación
1. Definir el router con el prefijo correcto
2. Validar el input con modelos Pydantic de `apps/agents/models/`
3. Verificar autenticación — el token de sesión viene del header
4. Llamar al agente o tool correspondiente
5. Guardar resultados en BD vía `apps/agents/tools/db.py`
6. Registrar en trazabilidad si hubo llamada a Anthropic
7. Retornar respuesta tipada con status code correcto

## Endpoints definidos en el brief
Ver Brief sección 3.4 — no crear endpoints fuera de esa lista sin revisión humana.

## Checklist antes de entregar
- [ ] Type hints en todas las funciones
- [ ] Input validado con Pydantic
- [ ] Errores retornan mensajes claros, nunca stack traces
- [ ] Status codes correctos (200, 201, 400, 404, 500)
- [ ] CORS configurado para Next.js en `main.py`
- [ ] Documentación OpenAPI generada automáticamente por FastAPI
