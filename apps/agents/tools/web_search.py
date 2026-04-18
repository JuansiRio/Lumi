"""Búsqueda web (Tavily) — firma S0.3."""

from __future__ import annotations

import os
from typing import Any

# Dominios orientados a fuentes jurídicas oficiales y repositorios colombianos habituales.
_DOMINIOS_JURIS_COLOMBIA: tuple[str, ...] = (
    "corteconstitucional.gov.co",
    "consejodeestado.gov.co",
    "suin-juriscol.gov.co",
    "ramajudicial.gov.co",
    "funcionpublica.gov.co",
    "secretariasenado.gov.co",
    "senado.gov.co",
    "camara.gov.co",
    "presidencia.gov.co",
    "minjusticia.gov.co",
)


def busqueda_tavily(query: str, *, max_results: int = 8) -> list[dict[str, Any]]:
    """
    Consulta Tavily restringiendo resultados a dominios jurídicos colombianos.

    Usa ``TAVILY_API_KEY`` desde el entorno. Si falta la clave o la llamada falla,
    devuelve lista vacía.
    """
    clave = os.environ.get("TAVILY_API_KEY", "").strip()
    if not clave:
        return []
    q = query.strip()
    if not q:
        return []
    try:
        from tavily import TavilyClient

        cliente = TavilyClient(api_key=clave)
        respuesta: dict[str, Any] = cliente.search(
            q,
            search_depth="basic",
            max_results=max_results,
            include_domains=list(_DOMINIOS_JURIS_COLOMBIA),
            timeout=45.0,
        )
    except Exception:
        return []

    resultados = respuesta.get("results")
    if not isinstance(resultados, list):
        return []

    normalizados: list[dict[str, Any]] = []
    for item in resultados:
        if not isinstance(item, dict):
            continue
        normalizados.append(
            {
                "title": str(item.get("title", "")),
                "url": str(item.get("url", "")),
                "content": str(item.get("content", "")),
                "score": item.get("score"),
            }
        )
    return normalizados


def search_web(query: str, *, max_results: int = 5) -> list[dict[str, Any]]:
    """Alias orientado a agentes; delega en ``busqueda_tavily``."""
    return busqueda_tavily(query, max_results=max_results)
