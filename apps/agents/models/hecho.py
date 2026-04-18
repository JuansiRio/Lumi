"""Contratos de hechos — sección 3.3."""

from enum import Enum

from pydantic import UUID4, BaseModel


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
