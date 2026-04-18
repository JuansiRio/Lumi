from __future__ import annotations

import json
from typing import Any


def extraer_primer_json_con_clave_fase_y_rango(texto: str) -> tuple[dict[str, Any], int, int] | None:
    """
    Busca el primer objeto JSON en ``texto`` que contenga la clave ``fase``.

    Devuelve ``(objeto, inicio, fin_exclusivo)`` en índices de ``texto``, o ``None``.
    Usado por LUMI Core para retirar el bloque JSON de la respuesta al abogado.
    """
    dec = json.JSONDecoder()
    n = len(texto)
    i = 0
    while i < n:
        if texto[i] != "{":
            i += 1
            continue
        try:
            obj, end_rel = dec.raw_decode(texto[i:])
        except json.JSONDecodeError:
            i += 1
            continue
        if isinstance(obj, dict) and "fase" in obj:
            fin = i + end_rel
            return obj, i, fin
        i += 1
    return None


def extraer_primer_json_con_clave_fase(texto: str) -> dict[str, Any] | None:
    """
    Busca el primer objeto JSON en texto que contenga la clave fase.
    Compartido por lumi_core, probabilistic, adversarial y qa.
    """
    hall = extraer_primer_json_con_clave_fase_y_rango(texto)
    return hall[0] if hall else None
