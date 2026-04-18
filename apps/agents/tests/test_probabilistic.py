"""
Tests unitarios — subagente motor probabilístico 2A (Sprint 3).

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
from apps.agents.models.fase_output import ProbabilisticInput, ProbabilisticOutput
from apps.agents.models.hecho import EstatusEpistemico, Hecho
from apps.agents.subagents.probabilistic import run_probabilistic


def _hecho_minimo(caso_id: UUID) -> Hecho:
    return Hecho(
        id=uuid4(),
        caso_id=caso_id,
        fase_origen="0A",
        contenido="Hecho de prueba para motor probabilístico.",
        estatus_epistemico=EstatusEpistemico.verificado,
        fuente="test",
    )


def _probabilistic_input(caso_id: UUID | None = None) -> ProbabilisticInput:
    cid = caso_id if caso_id is not None else uuid4()
    return ProbabilisticInput(
        hechos=[_hecho_minimo(cid)],
        tipo_accion=TipoAccion.ejecutivo,
        teoria_caso="Teoría sintética: obligación alimentaria y mora documentada.",
    )


def _texto_modelo_con_json_fase(contenido: dict[str, Any]) -> str:
    payload: dict[str, Any] = {
        "fase": "2A",
        "version": 1,
        "contenido": contenido,
        "tokens_usados": 200,
        "costo_usd": 0.002,
    }
    return "Análisis previo en prosa.\n\n" + json.dumps(payload, ensure_ascii=False)


@patch("apps.agents.subagents.probabilistic.db.log_trazabilidad")
@patch("apps.agents.subagents.probabilistic._llamada_haiku_aislada")
def test_run_probabilistic_returns_probabilistic_output_with_valid_range(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """``run_probabilistic`` retorna ``ProbabilisticOutput`` con rangos en [0, 1]."""
    contenido: dict[str, Any] = {
        "rango_min": 0.42,
        "rango_max": 0.78,
        "centro_masa": 0.55,
        "factores": [
            {"nombre": "Título ejecutivo", "peso": 0.4, "direccion": "favorable", "nota": "Sólido"},
        ],
        "justificacion": "Prior actualizado por factores.",
        "advertencias": [],
    }
    mock_llamada.return_value = (_texto_modelo_con_json_fase(contenido), 100, 150, 50)

    out = asyncio.run(run_probabilistic(_probabilistic_input()))

    assert isinstance(out, ProbabilisticOutput)
    assert 0.0 <= out.rango_min <= 1.0
    assert 0.0 <= out.rango_max <= 1.0
    assert 0.0 <= out.centro_masa <= 1.0


@patch("apps.agents.subagents.probabilistic.db.log_trazabilidad")
@patch("apps.agents.subagents.probabilistic._llamada_haiku_aislada")
def test_run_probabilistic_rango_min_centro_masa_rango_max_ordering(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """``rango_min`` <= ``centro_masa`` <= ``rango_max`` (tras normalización del subagente)."""
    contenido: dict[str, Any] = {
        "rango_min": 0.3,
        "rango_max": 0.9,
        "centro_masa": 0.85,
        "factores": [
            {"nombre": "F1", "peso": 0.5, "direccion": "neutro", "nota": "n"},
        ],
        "justificacion": "j",
        "advertencias": [],
    }
    mock_llamada.return_value = (_texto_modelo_con_json_fase(contenido), 10, 20, 1)

    out = asyncio.run(run_probabilistic(_probabilistic_input()))

    assert out.rango_min <= out.centro_masa <= out.rango_max


@patch("apps.agents.subagents.probabilistic.db.log_trazabilidad")
@patch("apps.agents.subagents.probabilistic._llamada_haiku_aislada")
def test_run_probabilistic_calls_log_trazabilidad_exactly_once(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """``log_trazabilidad`` se invoca exactamente una vez por ejecución."""
    contenido: dict[str, Any] = {
        "rango_min": 0.5,
        "rango_max": 0.6,
        "centro_masa": 0.55,
        "factores": [{"nombre": "F", "peso": 1.0, "direccion": "neutro", "nota": "x"}],
        "justificacion": "x",
        "advertencias": [],
    }
    mock_llamada.return_value = (_texto_modelo_con_json_fase(contenido), 5, 5, 1)

    asyncio.run(run_probabilistic(_probabilistic_input()))

    assert mock_log_trazabilidad.call_count == 1


@patch("apps.agents.subagents.probabilistic.db.log_trazabilidad")
@patch("apps.agents.subagents.probabilistic._llamada_haiku_aislada")
def test_run_probabilistic_sin_json_con_clave_fase_usa_fallback_35_65(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Sin objeto JSON con clave ``fase``: fallback con rango 0.35–0.65 y centro 0.5."""
    mock_llamada.return_value = (
        "Solo texto del modelo sin ningún JSON que contenga la clave fase requerida.",
        80,
        40,
        10,
    )

    out = asyncio.run(run_probabilistic(_probabilistic_input()))

    assert out.rango_min == pytest.approx(0.35)
    assert out.rango_max == pytest.approx(0.65)
    assert out.centro_masa == pytest.approx(0.5)


@patch("apps.agents.subagents.probabilistic.db.log_trazabilidad")
@patch("apps.agents.subagents.probabilistic._llamada_haiku_aislada")
def test_run_probabilistic_factores_tiene_al_menos_un_elemento(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """``factores`` nunca queda vacío: con lista vacía en JSON se inserta factor sustituto."""
    contenido: dict[str, Any] = {
        "rango_min": 0.4,
        "rango_max": 0.6,
        "centro_masa": 0.5,
        "factores": [],
        "justificacion": "Sin factores en modelo.",
        "advertencias": ["vacío probatorio"],
    }
    mock_llamada.return_value = (_texto_modelo_con_json_fase(contenido), 10, 10, 1)

    out = asyncio.run(run_probabilistic(_probabilistic_input()))

    assert len(out.factores) >= 1
