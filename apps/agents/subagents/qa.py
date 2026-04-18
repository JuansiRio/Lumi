"""Control de calidad QA — firma S0.3."""

from __future__ import annotations

from models.caso import TipoAccion
from models.fase_output import QAOutput
from models.hecho import Hecho


async def run_qa(
    borrador_texto: str,
    hechos: list[Hecho],
    teoria_caso: str,
    tipo_accion: TipoAccion,
) -> QAOutput:
    ...
