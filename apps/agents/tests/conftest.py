"""
Fixtures compartidos — caso base reducido y entorno seguro para mocks (S5.3).

No realiza llamadas a Supabase, Anthropic ni OpenAI.
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock
from uuid import UUID, uuid4

import pytest

from apps.agents.models.hecho import EstatusEpistemico, Hecho


@pytest.fixture(autouse=True)
def _fake_external_env(monkeypatch: pytest.MonkeyPatch) -> None:
    """Evita dependencias reales si algún código lee variables de entorno."""
    monkeypatch.setenv("SUPABASE_URL", "http://localhost:54321")
    monkeypatch.setenv("SUPABASE_KEY", "test-service-role-key")
    monkeypatch.setenv("OPENAI_API_KEY", "test-openai-key")
    monkeypatch.setenv("ANTHROPIC_API_KEY", "test-anthropic-key")


@pytest.fixture
def caso_sayago_id() -> UUID:
    """Identificador de caso de prueba (referencia Sayago vs. Roldán, simplificado)."""
    return uuid4()


@pytest.fixture
def prompts_dir(tmp_path: Path) -> Path:
    """Directorio con prompts mínimos válidos para `build_context`."""
    d = tmp_path / "prompts"
    d.mkdir()
    (d / "sistema_base.md").write_text(
        "# LUMI — sistema base (test)\n"
        "Reglas deontológicas y alcance del asistente jurídico.\n" * 20,
        encoding="utf-8",
    )
    (d / "fase_0e.md").write_text(
        "# Fase 0E — análisis ético (test)\n"
        "Verificar conflicto de interés y solidez de la pretensión.\n" * 15,
        encoding="utf-8",
    )
    return d


@pytest.fixture
def hecho_demanda(caso_sayago_id: UUID) -> Hecho:
    """Hecho mínimo tipo demanda ejecutiva de alimentos (referencia reducida)."""
    return Hecho(
        id=uuid4(),
        caso_id=caso_sayago_id,
        fase_origen="0E",
        contenido="Demanda ejecutiva de alimentos por suma aproximada de 57.5M COP.",
        estatus_epistemico=EstatusEpistemico.verificado,
        fuente="acta_icbf",
    )


@pytest.fixture
def hecho_acta(caso_sayago_id: UUID) -> Hecho:
    return Hecho(
        id=uuid4(),
        caso_id=caso_sayago_id,
        fase_origen="0A",
        contenido="Acta SIM: obligación de pensión acordada entre las partes.",
        estatus_epistemico=EstatusEpistemico.verificado,
        fuente="acta_icbf",
    )


def hecho_row_dict(
    *,
    hecho_id: UUID,
    caso_id: UUID,
    contenido: str,
    fase_origen: str = "0E",
    estatus: str = "verificado",
) -> dict[str, Any]:
    """Fila `hechos` tal como vendría de PostgREST."""
    return {
        "id": str(hecho_id),
        "caso_id": str(caso_id),
        "fase_origen": fase_origen,
        "contenido": contenido,
        "estatus_epistemico": estatus,
        "fuente": "test",
    }


def fase_output_row_dict(
    *,
    caso_id: UUID,
    fase: str,
    version: int,
    contenido: dict[str, Any],
    aprobado_abogado: bool,
) -> dict[str, Any]:
    return {
        "caso_id": str(caso_id),
        "fase": fase,
        "version": version,
        "contenido": contenido,
        "aprobado_abogado": aprobado_abogado,
        "anotaciones": None,
        "tokens_usados": 100,
        "costo_usd": 0.01,
    }


@pytest.fixture
def patch_create_client(monkeypatch: pytest.MonkeyPatch) -> Callable[[MagicMock], None]:
    """Inyecta un cliente Supabase falsificado en `db.create_client`."""

    def apply(client: MagicMock) -> None:
        monkeypatch.setattr(
            "apps.agents.tools.db.create_client",
            lambda _url, _key: client,
        )

    return apply


@pytest.fixture
def anthropic_message_factory() -> Callable[[str, int, int], MagicMock]:
    """Crea una respuesta mínima compatible con `compress_session`."""

    def make(text: str, in_tok: int, out_tok: int) -> MagicMock:
        block = MagicMock(type="text", text=text)
        usage = MagicMock(input_tokens=in_tok, output_tokens=out_tok)
        return MagicMock(content=[block], usage=usage)

    return make
