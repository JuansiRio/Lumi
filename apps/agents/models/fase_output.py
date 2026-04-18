"""Outputs por fase, orquestador LUMI Core y subagentes de fase — 3.3 y 3.8."""

from __future__ import annotations

from enum import Enum
from typing import Annotated, Literal

from pydantic import UUID4, BaseModel, Field

from .caso import Caso, TipoAccion
from .hecho import Hecho


DireccionFactor = Literal["favorable", "desfavorable", "neutro"]

EstadoVerificacionCita = Literal["✅ VERIFICADA", "⚠️ PROBABLE", "🔴 VERIFICAR"]

FuenteVerificacionCita = Literal["base_conocimiento", "tavily", "no_encontrada"]

SemaforoQA = Literal["🟢 LISTO", "🟡 OBSERVACIONES", "🔴 CRÍTICO"]

PrioridadCorreccion = Literal["🔴 crítico", "🟡 importante", "🟢 menor"]


class FaseCodigo(str, Enum):
    """Códigos de fase alineados con el motor (tabla / API)."""

    fase_0e = "0E"
    fase_0a = "0A"
    fase_0c = "0C"
    fase_1a = "1A"
    fase_1c = "1C"
    fase_2a = "2A"
    fase_5a = "5A"
    fase_gen = "GEN"


class FaseOutput(BaseModel):
    caso_id: UUID4
    fase: str
    version: int
    contenido: dict
    aprobado_abogado: bool = False
    anotaciones: str | None = None
    tokens_usados: int
    costo_usd: float


class LumiCoreInput(BaseModel):
    """Input — LUMI Core (3.8)."""

    caso_id: UUID4
    mensaje: str
    fase_actual: str


class LumiCoreResponse(BaseModel):
    """Output — LUMI Core (3.8)."""

    respuesta: str
    fase_output: FaseOutput | None = None
    subagente_llamado: str | None = None
    tokens_usados: int
    costo_usd: float


class Factor(BaseModel):
    """Factor bayesiano — Motor probabilístico (3.8)."""

    nombre: str
    peso: float = Field(ge=0.0, le=1.0)
    direccion: DireccionFactor
    nota: str


class ProbabilisticInput(BaseModel):
    """Input — Subagente Motor Probabilístico / Fase 2A (3.8)."""

    hechos: list[Hecho]
    tipo_accion: TipoAccion
    teoria_caso: str


class ProbabilisticOutput(BaseModel):
    """Output — Subagente Motor Probabilístico / Fase 2A (3.8)."""

    rango_min: float
    rango_max: float
    centro_masa: float
    factores: list[Factor]
    justificacion: str
    advertencias: list[str]
    tokens_usados: int
    costo_usd: float


class AdversarialInput(BaseModel):
    """Input — Subagente Simulación Adversarial / Fase 5A (3.8)."""

    hechos: list[Hecho]
    teoria_caso: str
    tipo_accion: TipoAccion


class AdversarialOutput(BaseModel):
    """Output — Subagente Simulación Adversarial / Fase 5A (3.8)."""

    argumentos: Annotated[list[str], Field(min_length=5, max_length=5)]
    ataque_no_obvio: str
    vulnerabilidad_probatoria: str
    nulidades_propias: list[str]
    tokens_usados: int
    costo_usd: float


class VerificacionCita(BaseModel):
    """Elemento de resultado — verificación jurisprudencia (3.8)."""

    cita_original: str
    estado: EstadoVerificacionCita
    fuente: FuenteVerificacionCita
    nota: str | None = None


class JurisprudenciaInput(BaseModel):
    """Input — Subagente Verificación de Jurisprudencia (3.8)."""

    citas: list[str]
    caso_id: UUID4


class JurisprudenciaOutput(BaseModel):
    """Output — Subagente Verificación de Jurisprudencia (3.8)."""

    resultados: list[VerificacionCita]
    tokens_usados: int
    costo_usd: float


class Correccion(BaseModel):
    """Ítem de corrección — QA (3.8)."""

    prioridad: PrioridadCorreccion
    ubicacion: str
    descripcion: str
    sugerencia: str


class QAInput(BaseModel):
    """Input — Subagente Control de Calidad (3.8)."""

    borrador_texto: str
    hechos: list[Hecho]
    teoria_caso: str
    tipo_accion: TipoAccion


class QAOutput(BaseModel):
    """Output — Subagente Control de Calidad (3.8)."""

    semaforo_general: SemaforoQA
    correcciones: list[Correccion]
    aprobado: bool
    tokens_usados: int
    costo_usd: float


class WordGeneratorInput(BaseModel):
    """Input — Tool Generador de Borrador Word (3.8)."""

    caso_id: UUID4
    outputs_fases: dict[str, FaseOutput]
    hechos: list[Hecho]
    metadata_caso: Caso


class WordOutput(BaseModel):
    """Output — Tool Generador de Borrador Word (3.8)."""

    archivo_bytes: bytes
    nombre_archivo: str
    paginas_estimadas: int
    advertencias: list[str]
