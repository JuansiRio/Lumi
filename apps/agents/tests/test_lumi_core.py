"""
Tests unitarios — LUMI Core (Sprint 2).

Anthropic, Supabase (``db``) y ``build_context`` (OpenAI/embeddings vía context manager) van mockeados.
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import MagicMock, patch
from uuid import uuid4

from apps.agents.core.lumi_core import _extraer_primer_json_con_clave_fase, process_message
from apps.agents.models.caso import ContextoComprimido
from apps.agents.models.fase_output import LumiCoreInput, LumiCoreResponse


def _lumi_input(*, mensaje: str = "¿Qué opinas del conflicto?", fase: str = "0E") -> LumiCoreInput:
    return LumiCoreInput(
        caso_id=uuid4(),
        mensaje=mensaje,
        fase_actual=fase,
    )


def _contexto_minimo(*, prompt_fase: str = "Instrucciones de fase de prueba.") -> ContextoComprimido:
    return ContextoComprimido(
        prompt_maestro="Sistema base de prueba. " * 20,
        resumenes_fases=[],
        hechos_relevantes=[],
        ultimos_mensajes=[],
        prompt_fase=prompt_fase,
        total_tokens_est=120,
    )


def _anthropic_response(texto: str, in_tok: int = 100, out_tok: int = 40) -> MagicMock:
    bloque = MagicMock(type="text", text=texto)
    uso = MagicMock(input_tokens=in_tok, output_tokens=out_tok)
    return MagicMock(content=[bloque], usage=uso)


@patch("apps.agents.core.lumi_core.db.get_max_version_output_fase", return_value=0)
@patch("apps.agents.core.lumi_core.db.save_output_fase")
@patch("apps.agents.core.lumi_core.db.log_trazabilidad")
@patch("apps.agents.core.lumi_core.db.save_sesion_mensaje")
@patch("anthropic.Anthropic")
@patch("apps.agents.core.lumi_core.context_manager.build_context")
def test_process_message_returns_non_empty_respuesta(
    mock_build_context: MagicMock,
    mock_anthropic_cls: MagicMock,
    mock_save_sesion: MagicMock,
    mock_log_trazabilidad: MagicMock,
    mock_save_output_fase: MagicMock,
    mock_max_version: MagicMock,
) -> None:
    """Caso obligatorio 1: ``process_message`` devuelve ``LumiCoreResponse`` con respuesta no vacía."""
    mock_build_context.return_value = _contexto_minimo()
    inst = MagicMock()
    inst.messages.create.return_value = _anthropic_response("Respuesta sustantiva para el abogado.")
    mock_anthropic_cls.return_value = inst

    out = process_message(_lumi_input())

    assert isinstance(out, LumiCoreResponse)
    assert len(out.respuesta.strip()) > 0


@patch("apps.agents.core.lumi_core.db.get_max_version_output_fase", return_value=0)
@patch("apps.agents.core.lumi_core.db.save_output_fase")
@patch("apps.agents.core.lumi_core.db.log_trazabilidad")
@patch("apps.agents.core.lumi_core.db.save_sesion_mensaje")
@patch("anthropic.Anthropic")
@patch("apps.agents.core.lumi_core.context_manager.build_context")
def test_process_message_calls_log_trazabilidad_once(
    mock_build_context: MagicMock,
    mock_anthropic_cls: MagicMock,
    mock_save_sesion: MagicMock,
    mock_log_trazabilidad: MagicMock,
    mock_save_output_fase: MagicMock,
    mock_max_version: MagicMock,
) -> None:
    """Caso obligatorio 2: ``log_trazabilidad`` exactamente una vez."""
    mock_build_context.return_value = _contexto_minimo()
    inst = MagicMock()
    inst.messages.create.return_value = _anthropic_response("Texto.")
    mock_anthropic_cls.return_value = inst

    process_message(_lumi_input())

    assert mock_log_trazabilidad.call_count == 1


@patch("apps.agents.core.lumi_core.db.get_max_version_output_fase", return_value=0)
@patch("apps.agents.core.lumi_core.db.save_output_fase")
@patch("apps.agents.core.lumi_core.db.log_trazabilidad")
@patch("apps.agents.core.lumi_core.db.save_sesion_mensaje")
@patch("anthropic.Anthropic")
@patch("apps.agents.core.lumi_core.context_manager.build_context")
def test_process_message_saves_two_sesion_messages(
    mock_build_context: MagicMock,
    mock_anthropic_cls: MagicMock,
    mock_save_sesion: MagicMock,
    mock_log_trazabilidad: MagicMock,
    mock_save_output_fase: MagicMock,
    mock_max_version: MagicMock,
) -> None:
    """Caso obligatorio 3: dos ``save_sesion_mensaje`` (abogado y lumi)."""
    mock_build_context.return_value = _contexto_minimo()
    inst = MagicMock()
    inst.messages.create.return_value = _anthropic_response("Respuesta LUMI.")
    mock_anthropic_cls.return_value = inst
    inp = _lumi_input(mensaje="Mi consulta procesal.")

    process_message(inp)

    assert mock_save_sesion.call_count == 2
    primera = mock_save_sesion.call_args_list[0]
    segunda = mock_save_sesion.call_args_list[1]
    assert primera[0][1] == "abogado"
    assert primera[0][2] == "Mi consulta procesal."
    assert segunda[0][1] == "lumi"
    assert segunda[0][2] == "Respuesta LUMI."


@patch("apps.agents.core.lumi_core.db.get_max_version_output_fase", return_value=0)
@patch("apps.agents.core.lumi_core.db.save_output_fase")
@patch("apps.agents.core.lumi_core.db.log_trazabilidad")
@patch("apps.agents.core.lumi_core.db.save_sesion_mensaje")
@patch("anthropic.Anthropic")
@patch("apps.agents.core.lumi_core.context_manager.build_context")
def test_process_message_detects_and_saves_fase_output_when_json_has_fase(
    mock_build_context: MagicMock,
    mock_anthropic_cls: MagicMock,
    mock_save_sesion: MagicMock,
    mock_log_trazabilidad: MagicMock,
    mock_save_output_fase: MagicMock,
    mock_max_version: MagicMock,
) -> None:
    """Caso obligatorio 4: con JSON con clave ``fase`` se persiste ``FaseOutput``."""
    mock_build_context.return_value = _contexto_minimo()
    payload_fase: dict[str, Any] = {
        "fase": "0E",
        "version": 1,
        "contenido": {"resumen": "Cierre de fase de prueba"},
        "aprobado_abogado": False,
        "tokens_usados": 200,
        "costo_usd": 0.01,
    }
    texto_modelo = "Párrafo visible.\n\n" + json.dumps(payload_fase, ensure_ascii=False)
    inst = MagicMock()
    inst.messages.create.return_value = _anthropic_response(texto_modelo)
    mock_anthropic_cls.return_value = inst

    out = process_message(_lumi_input())

    assert mock_save_output_fase.call_count == 1
    arg_fase = mock_save_output_fase.call_args[0][0]
    assert arg_fase.fase == "0E"
    assert arg_fase.contenido == {"resumen": "Cierre de fase de prueba"}
    assert out.fase_output is not None
    assert "Párrafo visible." in out.respuesta
    assert '"fase"' not in out.respuesta


@patch("apps.agents.core.lumi_core.db.save_output_fase")
@patch("apps.agents.core.lumi_core.db.log_trazabilidad")
@patch("apps.agents.core.lumi_core.db.save_sesion_mensaje")
@patch("anthropic.Anthropic")
@patch("apps.agents.core.lumi_core.context_manager.build_context")
def test_process_message_does_not_save_output_fase_without_fase_json(
    mock_build_context: MagicMock,
    mock_anthropic_cls: MagicMock,
    mock_save_sesion: MagicMock,
    mock_log_trazabilidad: MagicMock,
    mock_save_output_fase: MagicMock,
) -> None:
    """Caso obligatorio 5: sin JSON de fase no se llama ``save_output_fase``."""
    mock_build_context.return_value = _contexto_minimo()
    inst = MagicMock()
    inst.messages.create.return_value = _anthropic_response('Solo prosa. Otro objeto {"x": 1} sin clave fase.')
    mock_anthropic_cls.return_value = inst

    process_message(_lumi_input())

    assert mock_save_output_fase.call_count == 0


def test_extraer_primer_json_con_clave_fase_finds_in_mixed_text() -> None:
    """Caso obligatorio 6: JSON con ``fase`` dentro de texto mixto (prosa + objeto)."""
    inner = {"fase": "0A", "version": 2, "contenido": {"k": 1}}
    texto = (
        "Párrafo narrativo previo al cierre estructurado.\n\n"
        + json.dumps(inner, ensure_ascii=False)
        + "\n\nNota final sin más JSON."
    )
    hallazgo = _extraer_primer_json_con_clave_fase(texto)
    assert hallazgo is not None
    obj, ini, fin = hallazgo
    assert obj["fase"] == "0A"
    assert texto[ini:fin].startswith("{")
    assert json.loads(texto[ini:fin])["contenido"] == {"k": 1}


def test_extraer_primer_json_con_clave_fase_returns_none_without_fase() -> None:
    """Caso obligatorio 7: sin objeto JSON que contenga ``fase`` → ``None``."""
    assert _extraer_primer_json_con_clave_fase("No hay llaves útiles.") is None
    assert _extraer_primer_json_con_clave_fase('{"etapa": "0E"}') is None

