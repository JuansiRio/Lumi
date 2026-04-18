---
name: implementing-subagent
description: >-
  Implements LUMI subagents in apps/agents/subagents/: load data from db, call
  Anthropic with the correct model, parse typed Pydantic output, log trazabilidad.
  Use when the implementation plan assigns a module under apps/agents/subagents/
  or when building extractor, probabilistic, adversarial, qa, or jurisprudence agents.
---

# Implementing LUMI subagents

## Descripción
Patrón para implementar un subagente de LUMI: carga datos, llama a Anthropic, parsea output tipado y registra trazabilidad.

## Cuándo usar este skill
Cuando el implementation plan indique implementar un módulo en `apps/agents/subagents/`.

## Contrato obligatorio
- El contrato de input/output está definido en Brief sección 3.8
- Los tipos ya existen en `apps/agents/models/`
- No crear tipos nuevos sin revisión humana

## Patrón de implementación
1. Importar los modelos tipados correspondientes de `apps/agents/models/`
2. Cargar datos necesarios desde BD vía `apps/agents/tools/db.py`
3. NO cargar historial de conversación (sesiones aisladas)
4. Construir el prompt desde el archivo `.md` correspondiente en `apps/agents/core/prompts/`
5. Llamar a Anthropic con el modelo correcto según Brief sección 3.2
6. Parsear el output al modelo Pydantic de retorno
7. Registrar la llamada en trazabilidad vía `db.py`
8. Retornar el modelo tipado

## Modelos por subagente
- `extractor` → `claude-haiku-4-5`
- `probabilistic` → `claude-haiku-4-5`
- `adversarial` → `claude-sonnet-4-5`
- `qa` → `claude-haiku-4-5`
- `jurisprudence` → `claude-haiku-4-5`

## Checklist antes de entregar
- [ ] Type hints en todas las funciones
- [ ] Sin credenciales hardcodeadas
- [ ] Llamada a Anthropic registrada en trazabilidad
- [ ] Output es el modelo Pydantic definido en Brief 3.8
- [ ] Sin llamadas reales a Anthropic en tests (solo mocks)
- [ ] Sin acceso al historial de conversación de LUMI Core
