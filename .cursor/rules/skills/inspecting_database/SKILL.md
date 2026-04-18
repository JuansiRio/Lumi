# Skill: inspecting_database

## Descripción
Inspecciona el schema y datos de Supabase usando el MCP configurado
en .cursor/mcp.json. Solo lectura — nunca modifica datos.

## Cuándo usar este skill
- Antes de implementar un módulo que usa la BD
- Para verificar que una migración se aplicó correctamente
- Para confirmar que los tipos Pydantic coinciden con el schema real
- Para debuggear queries que retornan resultados inesperados

## Cómo usar el MCP de Supabase
1. Listar tablas disponibles en el proyecto
2. Inspeccionar el schema de una tabla específica
3. Ejecutar queries SELECT para verificar datos
4. Nunca ejecutar INSERT, UPDATE, DELETE o DROP

## Verificaciones obligatorias antes de implementar un módulo
- Confirmar que la tabla existe con el nombre exacto
- Confirmar que los campos coinciden con el modelo Pydantic en apps/agents/models/
- Confirmar que los tipos de datos son compatibles
  (uuid → UUID4, text → str, boolean → bool, numeric → float, jsonb → dict)
- Confirmar que RLS está activo en la tabla

## Mapeo de tipos Supabase → Pydantic
| Supabase      | Pydantic Python  |
|---------------|------------------|
| uuid          | UUID4            |
| text          | str              |
| boolean       | bool             |
| integer       | int              |
| numeric(14,6) | float            |
| jsonb         | dict             |
| timestamptz   | datetime         |
| vector(1536)  | list[float]      |

## Lo que retornas al agente principal
Resumen compacto:
✅ Tabla: [nombre] — existe y tiene RLS activo
✅ Campos verificados: [lista]
✅ Tipos compatibles con modelo Pydantic
⚠️ Diferencia encontrada: [descripción si aplica]
