"""
Tests unitarios — subagente extractor (Sprint 1).

Anthropic, Supabase (vía ``create_client``) y ``parse_document`` / LlamaParse van mockeados.
"""

from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock, patch
from uuid import UUID, uuid4

import pytest

from apps.agents.models.documento import DocumentoExtracto, ExtractorInput, ExtractorOutput
from apps.agents.models.hecho import EstatusEpistemico
from apps.agents.subagents.extractor import _extraer_objeto_json, run
from apps.agents.tools import db


def _payload_dos_hechos() -> dict[str, Any]:
    return {
        "tipo_detectado": "acta_icbf",
        "hechos": [
            {"contenido": "Primera obligación pactada en audiencia.", "estatus_epistemico": "inferido", "fuente": "p.1"},
            {"contenido": "Segunda obligación: pensión mensual.", "estatus_epistemico": "verificado", "fuente": None},
        ],
        "partes_detectadas": [{"nombre": "María Pérez", "rol": "demandante"}],
        "fechas_detectadas": [{"fecha": "2024-03-15", "contexto": "fecha de audiencia"}],
        "alertas": ["Revisar términos"],
    }


def _extractor_input(caso_id: UUID | None = None) -> ExtractorInput:
    """Genera input válido (UUID v4). El fixture ``caso_sayago_id`` no es UUID4 RFC4122."""
    cid = caso_id if caso_id is not None else uuid4()
    return ExtractorInput(
        documento_id=uuid4(),
        caso_id=cid,
        archivo_bytes=b"%PDF-1.4 fake",
        mime_type="application/pdf",
    )


@patch("apps.agents.subagents.extractor.db.log_trazabilidad")
@patch("apps.agents.subagents.extractor.db.save_hecho")
@patch("apps.agents.subagents.extractor.db.save_documento")
@patch("apps.agents.subagents.extractor._llamada_extractor_haiku")
@patch("apps.agents.subagents.extractor.parse_document")
def test_run_returns_extractor_output_with_hechos(
    mock_parse_document: MagicMock,
    mock_llamada_extractor_haiku: MagicMock,
    mock_save_documento: MagicMock,
    mock_save_hecho: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Caso obligatorio 1: ``run()`` devuelve ``ExtractorOutput`` con ``hechos_detectados`` no vacío."""
    mock_parse_document.return_value = DocumentoExtracto(texto_extraido="Texto del acta ICBF.", metadatos={})
    payload = _payload_dos_hechos()
    mock_llamada_extractor_haiku.return_value = (payload, 80, 120, 42)
    id_a, id_b = uuid4(), uuid4()
    mock_save_hecho.side_effect = [id_a, id_b]

    out = run(_extractor_input())

    assert isinstance(out, ExtractorOutput)
    assert len(out.hechos_detectados) >= 1
    assert all(isinstance(h.id, UUID) for h in out.hechos_detectados)


@patch("apps.agents.subagents.extractor.db.log_trazabilidad")
@patch("apps.agents.subagents.extractor.db.save_hecho")
@patch("apps.agents.subagents.extractor.db.save_documento")
@patch("apps.agents.subagents.extractor._llamada_extractor_haiku")
@patch("apps.agents.subagents.extractor.parse_document")
def test_run_calls_log_trazabilidad_exactly_once(
    mock_parse_document: MagicMock,
    mock_llamada_extractor_haiku: MagicMock,
    mock_save_documento: MagicMock,
    mock_save_hecho: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Caso obligatorio 2: ``log_trazabilidad`` exactamente una vez."""
    mock_parse_document.return_value = DocumentoExtracto(texto_extraido="x", metadatos={})
    mock_llamada_extractor_haiku.return_value = (_payload_dos_hechos(), 10, 20, 1)
    mock_save_hecho.side_effect = [uuid4(), uuid4()]

    run(_extractor_input())

    assert mock_log_trazabilidad.call_count == 1


@patch("apps.agents.subagents.extractor.db.log_trazabilidad")
@patch("apps.agents.subagents.extractor.db.save_hecho")
@patch("apps.agents.subagents.extractor.db.save_documento")
@patch("apps.agents.subagents.extractor._llamada_extractor_haiku")
@patch("apps.agents.subagents.extractor.parse_document")
def test_run_calls_save_documento_exactly_once(
    mock_parse_document: MagicMock,
    mock_llamada_extractor_haiku: MagicMock,
    mock_save_documento: MagicMock,
    mock_save_hecho: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Caso obligatorio 3: ``save_documento`` exactamente una vez."""
    mock_parse_document.return_value = DocumentoExtracto(texto_extraido="x", metadatos={})
    mock_llamada_extractor_haiku.return_value = (_payload_dos_hechos(), 10, 20, 1)
    mock_save_hecho.side_effect = [uuid4(), uuid4()]

    run(_extractor_input())

    assert mock_save_documento.call_count == 1


@patch("apps.agents.subagents.extractor.db.log_trazabilidad")
@patch("apps.agents.subagents.extractor.db.save_hecho")
@patch("apps.agents.subagents.extractor.db.save_documento")
@patch("apps.agents.subagents.extractor._llamada_extractor_haiku")
@patch("apps.agents.subagents.extractor.parse_document")
def test_run_saves_one_hecho_per_json_hecho(
    mock_parse_document: MagicMock,
    mock_llamada_extractor_haiku: MagicMock,
    mock_save_documento: MagicMock,
    mock_save_hecho: MagicMock,
    mock_log_trazabilidad: MagicMock,
) -> None:
    """Caso obligatorio 4: un ``save_hecho`` por cada hecho en el JSON."""
    mock_parse_document.return_value = DocumentoExtracto(texto_extraido="x", metadatos={})
    payload = _payload_dos_hechos()
    mock_llamada_extractor_haiku.return_value = (payload, 10, 20, 1)
    mock_save_hecho.side_effect = [uuid4(), uuid4()]

    run(_extractor_input())

    hechos_en_json = len(payload["hechos"])
    assert mock_save_hecho.call_count == hechos_en_json


def test_extraer_objeto_json_plain_object() -> None:
    """Caso obligatorio 5a: JSON sin markdown."""
    raw = '{"tipo_detectado": "otro", "hechos": [], "alertas": []}'
    out = _extraer_objeto_json(raw)
    assert out["tipo_detectado"] == "otro"
    assert out["hechos"] == []


def test_extraer_objeto_json_fenced_markdown() -> None:
    """Caso obligatorio 5b: JSON dentro de fence markdown."""
    inner = '{"tipo_detectado": null, "hechos": [{"contenido": "c", "estatus_epistemico": "inferido"}], "alertas": []}'
    raw = f"```json\n{inner}\n```"
    out = _extraer_objeto_json(raw)
    assert out["tipo_detectado"] is None
    assert len(out["hechos"]) == 1


def test_extraer_objeto_json_raises_when_no_object() -> None:
    """Caso obligatorio 6a: sin JSON válido (sin llaves)."""
    with pytest.raises(ValueError, match="no contiene"):
        _extraer_objeto_json("solo texto sin objeto")


def test_extraer_objeto_json_raises_when_invalid_json() -> None:
    """Caso obligatorio 6b: llaves presentes pero JSON inválido."""
    with pytest.raises(ValueError, match="JSON del modelo"):
        _extraer_objeto_json("{esto no es json válido}")


def test_save_hecho_returns_uuid_when_supabase_ok(monkeypatch: pytest.MonkeyPatch) -> None:
    """Caso obligatorio 7: ``save_hecho`` devuelve UUID cuando Supabase responde con ``id``."""
    esperado = uuid4()
    caso_id = uuid4()
    mock_client = MagicMock()
    mock_client.table.return_value.insert.return_value.execute.return_value = MagicMock(
        data=[{"id": str(esperado)}],
    )
    monkeypatch.setattr("apps.agents.tools.db.create_client", lambda _url, _key: mock_client)

    resultado = db.save_hecho(
        caso_id,
        "extractor",
        "Hecho de prueba",
        EstatusEpistemico.inferido,
        fuente="doc-test",
    )

    assert resultado == esperado
    assert isinstance(resultado, UUID)


def test_log_trazabilidad_inserts_all_required_fields(monkeypatch: pytest.MonkeyPatch) -> None:
    """Caso obligatorio 8: ``log_trazabilidad`` arma el insert con todos los campos requeridos."""
    mock_client = MagicMock()
    monkeypatch.setattr("apps.agents.tools.db.create_client", lambda _url, _key: mock_client)
    caso_id = uuid4()

    db.log_trazabilidad(
        caso_id,
        agente="extractor",
        modelo="claude-haiku-4-5",
        tokens_input=100,
        tokens_output=200,
        duracion_ms=55,
        costo_usd=0.012345,
    )

    mock_client.table.assert_called_once_with("trazabilidad")
    insert_arg: dict[str, Any] = mock_client.table.return_value.insert.call_args[0][0]
    assert insert_arg == {
        "caso_id": str(caso_id),
        "agente": "extractor",
        "modelo": "claude-haiku-4-5",
        "tokens_input": 100,
        "tokens_output": 200,
        "duracion_ms": 55,
        "costo_usd": 0.012345,
    }
