"""Tests del subagente de jurisprudencia (Brief 3.8 / S5.1)."""

from __future__ import annotations

import asyncio
from collections.abc import Iterator
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from apps.agents.models.fase_output import JurisprudenciaInput, JurisprudenciaOutput
from apps.agents.subagents.jurisprudence import (
    _cita_en_base,
    run_jurisprudence,
)


def _fake_busqueda_tavily(_query: str) -> list[dict[str, Any]]:
    return []


@pytest.fixture(autouse=True)
def patch_log_trazabilidad() -> Iterator[None]:
    with patch("apps.agents.subagents.jurisprudence.db.log_trazabilidad", MagicMock()):
        yield


def test_run_jurisprudence_returns_non_empty_resultados() -> None:
    texto: str = (
        "Referencia interna CSJ 2019-12345 sobre responsabilidad civil "
        "para verificación de citas en pruebas automatizadas."
    )
    cita: str = "CSJ 2019-12345 sobre responsabilidad civil"

    async def _run() -> JurisprudenciaOutput:
        with (
            patch(
                "apps.agents.subagents.jurisprudence._cargar_texto_base_juridica",
                return_value=texto,
            ),
            patch(
                "apps.agents.subagents.jurisprudence.busqueda_tavily",
                side_effect=_fake_busqueda_tavily,
            ),
        ):
            return await run_jurisprudence(
                JurisprudenciaInput(
                    caso_id=uuid4(),
                    citas=[cita],
                )
            )

    out: JurisprudenciaOutput = asyncio.run(_run())
    assert isinstance(out, JurisprudenciaOutput)
    assert len(out.resultados) >= 1
    assert out.resultados[0].cita_original == cita


def test_sin_tavily_todas_citas_probable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    texto: str = "Base con CSJ 2020-99999 y expediente para coincidencia débil."
    citas: list[str] = [
        "CSJ 2020-99999 sentencia de prueba con suficiente longitud",
        "EXP 2021-55667788 otro fragmento largo para el test",
    ]

    async def _run() -> JurisprudenciaOutput:
        with (
            patch(
                "apps.agents.subagents.jurisprudence._cargar_texto_base_juridica",
                return_value=texto,
            ),
            patch(
                "apps.agents.subagents.jurisprudence.busqueda_tavily",
                side_effect=_fake_busqueda_tavily,
            ),
        ):
            return await run_jurisprudence(
                JurisprudenciaInput(caso_id=uuid4(), citas=citas)
            )

    out: JurisprudenciaOutput = asyncio.run(_run())
    assert len(out.resultados) == len(citas)
    for r in out.resultados:
        assert r.estado == "⚠️ PROBABLE"


def test_cita_en_base_retorna_fuente_base_conocimiento(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.delenv("TAVILY_API_KEY", raising=False)
    cita_larga: str = "SENTENCIA UNICA INTERNA XYZABC123456789 PARA FUENTE BASE"
    texto: str = f"Párrafo que incluye {cita_larga} como subcadena exacta."

    async def _run() -> JurisprudenciaOutput:
        with (
            patch(
                "apps.agents.subagents.jurisprudence._cargar_texto_base_juridica",
                return_value=texto,
            ),
            patch(
                "apps.agents.subagents.jurisprudence.busqueda_tavily",
                side_effect=_fake_busqueda_tavily,
            ),
        ):
            return await run_jurisprudence(
                JurisprudenciaInput(caso_id=uuid4(), citas=[cita_larga])
            )

    out: JurisprudenciaOutput = asyncio.run(_run())
    assert len(out.resultados) == 1
    assert out.resultados[0].fuente == "base_conocimiento"


def test_cita_no_encontrada_retorna_verificar(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setenv("TAVILY_API_KEY", "clave-falsa-solo-para-test")
    cita: str = (
        "ZZZ_INEXISTENTE_99999_NI_EN_BASE_NI_EN_TAVILY_MOCK_CITA_LARGA_SUFICIENTE"
    )

    async def _run() -> JurisprudenciaOutput:
        with (
            patch(
                "apps.agents.subagents.jurisprudence._cargar_texto_base_juridica",
                return_value="",
            ),
            patch(
                "apps.agents.subagents.jurisprudence.busqueda_tavily",
                side_effect=_fake_busqueda_tavily,
            ),
        ):
            return await run_jurisprudence(
                JurisprudenciaInput(caso_id=uuid4(), citas=[cita])
            )

    out: JurisprudenciaOutput = asyncio.run(_run())
    assert len(out.resultados) == 1
    assert out.resultados[0].estado == "🔴 VERIFICAR"


def test_cita_en_base_coincidencia_fuerte_por_subcadena() -> None:
    cita: str = "fragmento_exacto_largo_para_fuerte"
    texto_base: str = (
        "Preámbulo legal fragmento_exacto_largo_para_fuerte y cierre del documento."
    )
    fuerte: bool
    debil: bool
    fuerte, debil = _cita_en_base(cita, texto_base)
    assert fuerte is True
    assert debil is True


def test_cita_en_base_texto_vacio_retorna_false_false() -> None:
    fuerte: bool
    debil: bool
    fuerte, debil = _cita_en_base("cualquier cita con texto", "")
    assert fuerte is False
    assert debil is False
