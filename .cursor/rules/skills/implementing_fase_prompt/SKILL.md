---
name: implementing-fase-prompt
description: >-
  Authors phase prompt markdown files in apps/agents/core/prompts/ (fase_XX.md)
  with fixed structure: role, context, instructions, JSON output schema, blocking
  conditions, and deontological closing. Use when the implementation plan asks to
  create or fill prompts under apps/agents/core/prompts/.
---

# Implementing LUMI phase prompts

## Descripción
Patrón para escribir archivos `.md` de prompts de fase en `apps/agents/core/prompts/`.

## Cuándo usar este skill
Cuando el implementation plan indique llenar un archivo `fase_XX.md` en `apps/agents/core/prompts/`.

## Estructura obligatoria de cada prompt
1. **Rol** — quién es LUMI en esta fase
2. **Contexto** — qué información tiene disponible
3. **Instrucciones** — qué debe analizar y en qué orden
4. **Output esperado** — formato JSON exacto del resultado
5. **Condición de bloqueo** — cuándo LUMI debe detener el flujo

## Principio deontológico
Todo prompt debe incluir al final:

"LUMI propone. El abogado {nombre_abogado} decide y firma."

## Output JSON obligatorio
Cada fase debe terminar con un bloque JSON estructurado que el Context Manager pueda detectar y guardar en `outputs_fases`. El bloque debe tener siempre:

- `fase`: código de fase (ej: `"0E"`)
- `version`: número de versión
- `contenido`: dict con el resultado estructurado
- `tokens_usados`: int
- `costo_usd`: float

## Checklist antes de entregar
- [ ] El prompt incluye el principio deontológico
- [ ] El output JSON tiene la estructura de `FaseOutput`
- [ ] Las instrucciones son específicas para derecho colombiano
- [ ] No hay suposiciones sin base en los hechos del caso
- [ ] El prompt referencia los hechos del caso vía Context Manager
