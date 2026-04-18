"""
Tests unitarios — subagente simulación adversarial 5A (Sprint 3).

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
from apps.agents.models.fase_output import AdversarialInput, AdversarialOutput
from apps.agents.models.hecho import EstatusEpistemico, Hecho
from apps.agents.subagents.adversarial import _cinco_argumentos, run_adversarial


def _hecho_minimo(caso_id: UUID) -> Hecho:
    return Hecho(
        id=uuid4(),
        caso_id=caso_id,
        fase_origen="0A",
        contenido="Hecho de prueba para simulación adversarial.",
        estatus_epistemico=EstatusEpistemico.verificado,
        fuente="test",
    )


def _adversarial_input(caso_id: UUID | None = None) -> AdversarialInput:
    cid = caso_id if caso_id is not None else uuid4()
    return AdversarialInput(
        hechos=[_hecho_minimo(cid)],
        teoria_caso="Narrativa del demandante: incumplimiento y daño.",
        tipo_accion=TipoAccion.ejecutivo,
    )


def _texto_modelo_con_json_fase(contenido: dict[str, Any]) -> str:
    payload: dict[str, Any] = {
        "fase": "5A",
        "version": 1,
        "contenido": contenido,
        "tokens_usados": 300,
        "costo_usd": 0.01,
    }
    return "Párrafo introductorio.\n\n" + json.dumps(payload, ensure_ascii=False)


@patch("apps.agents.subagents.adversarial.db.log_trazabilidad")
@patch("apps.agents.subagents.adversarial._llamada_sonnet_aislada")
def test_run_adversarial_returns_exactly_five_argumentos(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """``run_adversarial`` retorna ``AdversarialOutput`` con exactamente 5 argumentos."""
    argumentos = [f"Argumento adversarial número {i} con sustento procesal." for i in range(1, 6)]
    contenido: dict[str, Any] = {
        "argumentos": argumentos,
        "ataque_no_obvio": "Ataque lateral sobre prescripción atípica del título.",
        "vulnerabilidad_probatoria": "Ausencia de peritazgo contable sobre la mora.",
        "nulidades_propias": ["VERIFICAR: emplazamiento"],
    }
    mock_llamada.return_value = (_texto_modelo_con_json_fase(contenido), 200, 400, 60)

    out = asyncio.run(run_adversarial(_adversarial_input()))

    assert isinstance(out, AdversarialOutput)
    assert len(out.argumentos) == 5


@patch("apps.agents.subagents.adversarial.db.log_trazabilidad")
@patch("apps.agents.subagents.adversarial._llamada_sonnet_aislada")
def test_run_adversarial_calls_log_trazabilidad_exactly_once(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """``log_trazabilidad`` se invoca exactamente una vez por ejecución."""
    contenido: dict[str, Any] = {
        "argumentos": [f"A{i}" for i in range(5)],
        "ataque_no_obvio": "x",
        "vulnerabilidad_probatoria": "y",
        "nulidades_propias": [],
    }
    mock_llamada.return_value = (_texto_modelo_con_json_fase(contenido), 10, 10, 1)

    asyncio.run(run_adversarial(_adversarial_input()))

    assert mock_log_trazabilidad.call_count == 1


@patch("apps.agents.subagents.adversarial.db.log_trazabilidad")
@patch("apps.agents.subagents.adversarial._llamada_sonnet_aislada")
def test_run_adversarial_sin_json_valido_fallback_cinco_argumentos(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Sin JSON con clave ``fase``: fallback con exactamente 5 strings en ``argumentos``."""
    mock_llamada.return_value = (
        "Respuesta del modelo sin bloque JSON parseable con clave fase.",
        50,
        50,
        5,
    )

    out = asyncio.run(run_adversarial(_adversarial_input()))

    assert len(out.argumentos) == 5
    assert all(isinstance(a, str) and len(a) > 0 for a in out.argumentos)


def test_cinco_argumentos_rellena_hasta_cinco_cuando_hay_menos() -> None:
    """``_cinco_argumentos`` completa con marcadores hasta llegar a 5 elementos."""
    parcial: list[str] = ["Primer ataque", "Segundo ataque"]
    out = _cinco_argumentos(parcial)

    assert len(out) == 5
    assert out[0] == "Primer ataque"
    assert out[1] == "Segundo ataque"
    assert "Argumento no generado" in out[2]


@patch("apps.agents.subagents.adversarial.db.log_trazabilidad")
@patch("apps.agents.subagents.adversarial._llamada_sonnet_aislada")
def test_run_adversarial_ataque_y_vulnerabilidad_no_vacios(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """``ataque_no_obvio`` y ``vulnerabilidad_probatoria`` no quedan vacíos (valores o defaults)."""
    contenido: dict[str, Any] = {
        "argumentos": [f"Arg {i}" for i in range(5)],
        "ataque_no_obvio": "  Ataque sofisticado sobre cosa juzgada parcial.  ",
        "vulnerabilidad_probatoria": "  Falta de cadena de custodia en anexos.  ",
        "nulidades_propias": ["Ineptitud"],
    }
    mock_llamada.return_value = (_texto_modelo_con_json_fase(contenido), 10, 10, 1)

    out = asyncio.run(run_adversarial(_adversarial_input()))

    assert len(out.ataque_no_obvio.strip()) > 0
    assert len(out.vulnerabilidad_probatoria.strip()) > 0


@patch("apps.agents.subagents.adversarial.db.log_trazabilidad")
@patch("apps.agents.subagents.adversarial._llamada_sonnet_aislada")
def test_run_adversarial_campos_vacios_en_json_recibe_defaults_no_vacios(
    mock_llamada: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Si el modelo envía cadenas vacías, el subagente sustituye por textos no vacíos."""
    contenido: dict[str, Any] = {
        "argumentos": [f"Arg {i}" for i in range(5)],
        "ataque_no_obvio": "",
        "vulnerabilidad_probatoria": "   ",
        "nulidades_propias": [],
    }
    mock_llamada.return_value = (_texto_modelo_con_json_fase(contenido), 10, 10, 1)

    out = asyncio.run(run_adversarial(_adversarial_input()))

    assert len(out.ataque_no_obvio.strip()) > 0
    assert len(out.vulnerabilidad_probatoria.strip()) > 0
