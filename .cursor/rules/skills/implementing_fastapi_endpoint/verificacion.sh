#!/bin/bash
echo "Corriendo tests del módulo..."
cd apps/agents
python -m pytest tests/ -v --cov=apps/agents/routers \
  --cov-report=term-missing
if [ $? -eq 0 ]; then
  echo "✅ Verificación exitosa"
else
  echo "🔴 Tests fallaron — no avanzar al siguiente módulo"
  exit 1
fi
