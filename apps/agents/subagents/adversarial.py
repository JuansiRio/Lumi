"""Simulación adversarial (5A) — firma S0.3."""

from __future__ import annotations

from models.caso import TipoAccion
from models.fase_output import AdversarialOutput
from models.hecho import Hecho


async def run_adversarial(
    hechos: list[Hecho],
    teoria_caso: str,
    tipo_accion: TipoAccion,
) -> AdversarialOutput:
    ...
