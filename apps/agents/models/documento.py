"""Contratos de documentos ingestados + extractor (3.8)."""

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import UUID4, BaseModel, Field

from .hecho import Hecho


class EstadoDocumento(str, Enum):
    pendiente = "pendiente"
    procesando = "procesando"
    listo = "listo"
    error = "error"


class Documento(BaseModel):
    """Registro persistido de un archivo del caso (tabla documentos)."""

    id: UUID4
    caso_id: UUID4
    nombre_original: str
    mime_type: str
    tipo_detectado: str | None = None
    estado: EstadoDocumento = EstadoDocumento.pendiente
    texto_extraido: str | None = None
    storage_path: str | None = None
    created_at: datetime
    updated_at: datetime


class DocumentoCreate(BaseModel):
    """Payload típico al registrar un upload antes del procesamiento."""

    nombre_original: str
    mime_type: str


class DocumentoExtracto(BaseModel):
    """Resultado estructurado del parsing (texto + metadatos), previo o paralelo al extractor LLM."""

    texto_extraido: str
    metadatos: dict[str, Any] = Field(default_factory=dict)


class RolParte(str, Enum):
    demandante = "demandante"
    demandado = "demandado"
    otro = "otro"


class ParteDetectada(BaseModel):
    nombre: str
    rol: RolParte


class FechaDetectada(BaseModel):
    fecha: str
    contexto: str


class ExtractorInput(BaseModel):
    """Input — Subagente Extractor de Documentos (3.8)."""

    documento_id: UUID4
    caso_id: UUID4
    archivo_bytes: bytes
    mime_type: str


class ExtractorOutput(BaseModel):
    """Output — Subagente Extractor de Documentos (3.8)."""

    texto_extraido: str
    hechos_detectados: list[Hecho]
    partes_detectadas: list[ParteDetectada]
    fechas_detectadas: list[FechaDetectada]
    alertas: list[str]
    tokens_usados: int
    costo_usd: float
