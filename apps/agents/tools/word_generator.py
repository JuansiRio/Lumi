"""Generación de borrador Word — firma S0.3."""

from __future__ import annotations

from uuid import UUID

from models.caso import Caso
from models.fase_output import FaseOutput, WordOutput
from models.hecho import Hecho


def generate_word_document(
    caso_id: UUID,
    outputs_fases: dict[str, FaseOutput],
    hechos: list[Hecho],
    metadata_caso: Caso,
) -> WordOutput:
    ...
