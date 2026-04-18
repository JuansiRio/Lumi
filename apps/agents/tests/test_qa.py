"""
Tests unitarios — subagente QA (Sprint 4).

Anthropic y Supabase (vía ``log_trazabilidad``) van mockeados.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest

from apps.agents.models.caso import TipoAccion
from apps.agents.models.fase_output import QAInput, QAOutput, SemaforoQA
from apps.agents.models.hecho import EstatusEpistemico, Hecho
from apps.agents.subagents.qa import run_qa

_SEMAFOROS_VALIDOS: tuple[SemaforoQA, ...] = ("🟢 LISTO", "🟡 OBSERVACIONES", "🔴 CRÍTICO")


def _hecho_minimo(caso_id: UUID) -> Hecho:
    return Hecho(
        id=uuid4(),
        caso_id=caso_id,
        fase_origen="GEN",
        contenido="Hecho de apoyo para QA.",
        estatus_epistemico=EstatusEpistemico.verificado,
        fuente="test",
    )


def _qa_input(caso_id: UUID | None = None, borrador: str = "Demanda de prueba.") -> QAInput:
    cid = caso_id if caso_id is not None else uuid4()
    return QAInput(
        borrador_texto=borrador,
        hechos=[_hecho_minimo(cid)],
        teoria_caso="Teoría resumida del caso.",
        tipo_accion=TipoAccion.ejecutivo,
    )


def _texto_modelo_con_json_qa(contenido: dict[str, Any]) -> str:
    payload: dict[str, Any] = {
        "fase": "QA",
        "version": 1,
        "contenido": contenido,
        "tokens_usados": 150,
        "costo_usd": 0.001,
    }
    return "Narrativa QA.\n\n" + json.dumps(payload, ensure_ascii=False)


@patch("apps.agents.subagents.qa.db.log_trazabilidad")
@patch("apps.agents.subagents.qa._llamada_haiku_aislada")
def test_run_qa_returns_qa_output_with_valid_semaforo(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """``run_qa`` retorna ``QAOutput`` con ``semaforo_general`` en el conjunto permitido."""
    contenido: dict[str, Any] = {
        "semaforo_general": "🟢 LISTO",
        "correcciones": [],
        "aprobado": True,
    }
    mock_llamada.return_value = (_texto_modelo_con_json_qa(contenido), 50, 80, 10)

    out = asyncio.run(run_qa(_qa_input()))

    assert isinstance(out, QAOutput)
    assert out.semaforo_general in _SEMAFOROS_VALIDOS


@patch("apps.agents.subagents.qa.db.log_trazabilidad")
@patch("apps.agents.subagents.qa._llamada_haiku_aislada")
def test_run_qa_calls_log_trazabilidad_exactly_once(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """``log_trazabilidad`` se invoca exactamente una vez por ejecución."""
    contenido: dict[str, Any] = {
        "semaforo_general": "🟡 OBSERVACIONES",
        "correcciones": [],
        "aprobado": False,
    }
    mock_llamada.return_value = (_texto_modelo_con_json_qa(contenido), 10, 10, 1)

    asyncio.run(run_qa(_qa_input()))

    assert mock_log_trazabilidad.call_count == 1


@patch("apps.agents.subagents.qa.db.log_trazabilidad")
@patch("apps.agents.subagents.qa._llamada_haiku_aislada")
def test_run_qa_semaforo_critico_entonces_aprobado_false(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Semáforo 🔴 CRÍTICO implica ``aprobado=False``."""
    contenido: dict[str, Any] = {
        "semaforo_general": "🔴 CRÍTICO",
        "correcciones": [],
        "aprobado": True,
    }
    mock_llamada.return_value = (_texto_modelo_con_json_qa(contenido), 10, 10, 1)

    out = asyncio.run(run_qa(_qa_input()))

    assert out.semaforo_general == "🔴 CRÍTICO"
    assert out.aprobado is False


@patch("apps.agents.subagents.qa.db.log_trazabilidad")
@patch("apps.agents.subagents.qa._llamada_haiku_aislada")
def test_run_qa_listo_sin_correcciones_criticas_entonces_aprobado_true(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """🟢 LISTO sin correcciones 🔴 crítico implica ``aprobado=True``."""
    contenido: dict[str, Any] = {
        "semaforo_general": "🟢 LISTO",
        "correcciones": [
            {
                "prioridad": "🟢 menor",
                "ubicacion": "p. 2",
                "descripcion": "Tilde",
                "sugerencia": "Corregir ortografía.",
            }
        ],
        "aprobado": False,
    }
    mock_llamada.return_value = (_texto_modelo_con_json_qa(contenido), 10, 10, 1)

    out = asyncio.run(run_qa(_qa_input()))

    assert out.semaforo_general == "🟢 LISTO"
    assert out.aprobado is True


@patch("apps.agents.subagents.qa.db.log_trazabilidad")
@patch("apps.agents.subagents.qa._llamada_haiku_aislada")
def test_run_qa_correccion_critica_fuerza_aprobado_false_aunque_listo(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Corrección ``🔴 crítico`` fuerza ``aprobado=False`` aunque el semáforo sea 🟢 LISTO."""
    contenido: dict[str, Any] = {
        "semaforo_general": "🟢 LISTO",
        "correcciones": [
            {
                "prioridad": "🔴 crítico",
                "ubicacion": "Pretensión principal",
                "descripcion": "Falta de sustento documental.",
                "sugerencia": "Anexar prueba.",
            }
        ],
        "aprobado": True,
    }
    mock_llamada.return_value = (_texto_modelo_con_json_qa(contenido), 10, 10, 1)

    out = asyncio.run(run_qa(_qa_input()))

    assert out.semaforo_general == "🟢 LISTO"
    assert out.aprobado is False
    assert any(c.prioridad == "🔴 crítico" for c in out.correcciones)


@patch("apps.agents.subagents.qa.db.log_trazabilidad")
@patch("apps.agents.subagents.qa._llamada_haiku_aislada")
def test_run_qa_sin_json_valido_fallback_aprobado_false(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Sin JSON con clave ``fase``: fallback con ``aprobado=False``."""
    mock_llamada.return_value = ("Respuesta sin objeto JSON utilizable.", 5, 5, 1)

    out = asyncio.run(run_qa(_qa_input()))

    assert out.aprobado is False
    assert out.semaforo_general == "🔴 CRÍTICO"
    assert len(out.correcciones) >= 1
