"""Contratos de dominio caso — sección 3.3 + contratos de contexto (3.8)."""

from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import UUID4, BaseModel, Field

from .hecho import Hecho


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


class ContextManagerInput(BaseModel):
    """Input — Context Manager (3.8)."""

    caso_id: UUID4
    fase_actual: str
    max_tokens: int = Field(default=25_000, ge=1)


class ContextoComprimido(BaseModel):
    """Output — Context Manager (3.8)."""

    prompt_maestro: str
    resumenes_fases: list[str]
    hechos_relevantes: list[Hecho]
    ultimos_mensajes: list[dict]
    prompt_fase: str
    total_tokens_est: int
