"""Motor probabilístico (2A) — firma S0.3."""

from __future__ import annotations

from models.caso import TipoAccion
from models.fase_output import ProbabilisticOutput
from models.hecho import Hecho


async def run_probabilistic(
    hechos: list[Hecho],
    tipo_accion: TipoAccion,
    teoria_caso: str,
) -> ProbabilisticOutput:
    ...
