# Pendientes técnicos — LUMI Judicial

## Para atender en Sprint 5 (Deploy)
- [x] Vulnerabilidades Next.js — resuelto con npm audit fix --force
      Next actualizado a 14.2.35, eslint-config-next a 16.2.4
      Queda 1 vulnerabilidad high de DoS — pendiente para Sprint 5

## Para atender cuando corresponda
- [ ] Instalar Python 3.11+ y verificar importaciones con:
      python -c "from apps.agents.models import Caso; print(Caso)"
- [ ] Crear función RPC match_hechos en Supabase antes de S2.1
- [ ] Migrar llama-parse al nuevo SDK llama-cloud>=1.0 antes del deploy
      Ver: https://github.com/run-llama/llama-cloud-py