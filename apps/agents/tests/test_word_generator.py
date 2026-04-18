"""
Tests unitarios — generador Word (Sprint 4).

Herramienta determinista: sin mocks de red ni de modelos.
"""

from __future__ import annotations

import io
import zipfile
from datetime import datetime
from uuid import UUID, uuid4

from apps.agents.models.caso import Caso, EstadoCaso, TipoAccion
from apps.agents.models.fase_output import FaseOutput, WordGeneratorInput
from apps.agents.models.hecho import EstatusEpistemico, Hecho
from apps.agents.tools.word_generator import generate_word_document

_PENDIENTE = "[PENDIENTE - fase no completada]"


def _caso_metadata(caso_id: UUID) -> Caso:
    ahora = datetime.now()
    return Caso(
        id=caso_id,
        nombre_caso="Caso Word Test",
        tipo_accion=TipoAccion.ejecutivo,
        estado=EstadoCaso.activo,
        fase_actual="GEN",
        created_at=ahora,
        updated_at=ahora,
    )


def _fase_aprobada(caso_id: UUID, fase: str, contenido: dict) -> FaseOutput:
    return FaseOutput(
        caso_id=caso_id,
        fase=fase,
        version=1,
        contenido=contenido,
        aprobado_abogado=True,
        tokens_usados=1,
        costo_usd=0.0,
    )


def _document_xml(archivo_bytes: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(archivo_bytes)) as zf:
        return zf.read("word/document.xml").decode("utf-8")


def test_generate_word_document_returns_word_output_with_non_empty_bytes() -> None:
    """``generate_word_document`` retorna ``WordOutput`` con ``archivo_bytes`` no vacío."""
    cid = uuid4()
    fo = _fase_aprobada(cid, "0E", {"resumen": "Listo para Word."})
    h = Hecho(
        id=uuid4(),
        caso_id=cid,
        fase_origen="0A",
        contenido="Contenido mínimo.",
        estatus_epistemico=EstatusEpistemico.verificado,
        fuente=None,
    )
    inp = WordGeneratorInput(
        caso_id=cid,
        outputs_fases={"0E": fo},
        hechos=[h],
        metadata_caso=_caso_metadata(cid),
    )
    out = generate_word_document(inp)
    assert len(out.archivo_bytes) > 1000


def test_nombre_archivo_prefijo_borrador_y_extension_docx() -> None:
    """El nombre empieza por ``borrador_`` y termina en ``.docx``."""
    cid = uuid4()
    fo = _fase_aprobada(cid, "0A", {"x": 1})
    inp = WordGeneratorInput(
        caso_id=cid,
        outputs_fases={"0A": fo},
        hechos=[],
        metadata_caso=_caso_metadata(cid),
    )
    out = generate_word_document(inp)
    assert out.nombre_archivo.startswith("borrador_")
    assert out.nombre_archivo.endswith(".docx")


def test_fases_sin_output_incluyen_marcador_pendiente() -> None:
    """Las fases sin entrada en ``outputs_fases`` incluyen el marcador de pendiente en el XML."""
    cid = uuid4()
    fo = _fase_aprobada(cid, "0E", {"solo": "0E"})
    inp = WordGeneratorInput(
        caso_id=cid,
        outputs_fases={"0E": fo},
        hechos=[],
        metadata_caso=_caso_metadata(cid),
    )
    out = generate_word_document(inp)
    xml = _document_xml(out.archivo_bytes)
    assert xml.count(_PENDIENTE) >= 3


def test_verificar_en_contenido_aparece_en_documento() -> None:
    """Si el contenido incluye ``VERIFICAR``, la cadena aparece en el documento generado."""
    cid = uuid4()
    fo = _fase_aprobada(cid, "0C", {"nota": "Cuantía VERIFICAR contra planillas."})
    inp = WordGeneratorInput(
        caso_id=cid,
        outputs_fases={"0C": fo},
        hechos=[],
        metadata_caso=_caso_metadata(cid),
    )
    out = generate_word_document(inp)
    xml = _document_xml(out.archivo_bytes)
    assert "VERIFICAR" in xml


def test_paginas_estimadas_al_menos_uno() -> None:
    """``paginas_estimadas`` es un entero >= 1."""
    cid = uuid4()
    fo = _fase_aprobada(cid, "GEN", {"borrador": "x" * 5000})
    inp = WordGeneratorInput(
        caso_id=cid,
        outputs_fases={"GEN": fo},
        hechos=[],
        metadata_caso=_caso_metadata(cid),
    )
    out = generate_word_document(inp)
    assert isinstance(out.paginas_estimadas, int)
    assert out.paginas_estimadas >= 1


def test_sin_hechos_agrega_advertencia_hechos_vacios() -> None:
    """Sin hechos se registra advertencia sobre lista vacía."""
    cid = uuid4()
    fo = _fase_aprobada(cid, "1C", {"oracion_central": "Narrativa"})
    inp = WordGeneratorInput(
        caso_id=cid,
        outputs_fases={"1C": fo},
        hechos=[],
        metadata_caso=_caso_metadata(cid),
    )
    out = generate_word_document(inp)
    assert any("hechos" in a.lower() for a in out.advertencias)
