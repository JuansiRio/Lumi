"""Verificación de jurisprudencia — firma S0.3."""

from __future__ import annotations

from uuid import UUID

from models.fase_output import JurisprudenciaOutput


async def run_jurisprudence(citas: list[str], caso_id: UUID) -> JurisprudenciaOutput:
    ...
