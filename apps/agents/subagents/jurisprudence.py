"""Verificación de jurisprudencia — Brief 3.8, tarea S5.1 (sin LLM)."""

from __future__ import annotations

import asyncio
import os
import re
from pathlib import Path
from typing import Any
from uuid import UUID

from apps.agents.models.fase_output import JurisprudenciaInput, JurisprudenciaOutput, VerificacionCita
from apps.agents.tools import db
from apps.agents.tools.web_search import busqueda_tavily

JURISPRUDENCE_AGENTE = "jurisprudence"
MODELO_TRAZA = "tavily-search"


def _raiz_repositorio() -> Path:
    """``apps/agents/subagents`` → raíz del repo (tres niveles arriba)."""
    return Path(__file__).resolve().parents[3]


def _rutas_base_conocimiento() -> tuple[Path, ...]:
    raiz = _raiz_repositorio()
    return (
        raiz / "Lumi MD" / "Lumi MD" / "BASE_CONOCIMIENTO_JURIDICO_COLOMBIA_v2.md",
        raiz / "docs" / "BASE_CONOCIMIENTO_JURIDICO.md",
        raiz / "docs" / "BASE_CONOCIMIENTO_JURIDICO_COLOMBIA_v2.md",
    )


def _cargar_texto_base_juridica() -> str:
    for ruta in _rutas_base_conocimiento():
        if ruta.is_file():
            return ruta.read_text(encoding="utf-8", errors="replace")
    return ""


def _normalizar_cita(cita: str) -> str:
    return " ".join(cita.split()).strip()


def _tokens_busqueda(cita: str) -> list[str]:
    """Fragmentos útiles para coincidencia laxa (expediente, siglas, año)."""
    limpia = _normalizar_cita(cita)
    if not limpia:
        return []
    tokens: list[str] = []
    for m in re.finditer(r"\b(?:19|20)\d{2}\b", limpia):
        tokens.append(m.group(0))
    for m in re.finditer(r"\b(?:SCC|CSJ|STJ|CE|CC)\b\.?\s*\d+[\w./-]*", limpia, re.IGNORECASE):
        tokens.append(m.group(0).strip())
    for m in re.finditer(r"\b(?:EXP|T-|Rad\.?|Radicado)\s*[\d.-]+\b", limpia, re.IGNORECASE):
        tokens.append(m.group(0).strip())
    palabras = [p.strip(".,;:") for p in re.split(r"\s+", limpia) if len(p.strip(".,;:")) >= 5]
    tokens.extend(palabras[:6])
    vistos: set[str] = set()
    salida: list[str] = []
    for t in tokens:
        tl = t.lower()
        if tl not in vistos and len(tl) >= 4:
            vistos.add(tl)
            salida.append(t)
    return salida[:12]


def _cita_en_base(cita: str, texto_base: str) -> tuple[bool, bool]:
    """
    Devuelve (coincidencia_fuerte, coincidencia_debil).

    Fuerte: la cita normalizada aparece como subcadena del texto base.
    Débil: varios tokens distintivos aparecen en el texto base.
    """
    if not texto_base.strip():
        return False, False
    c = _normalizar_cita(cita).lower()
    tl = texto_base.lower()
    if len(c) >= 12 and c in tl:
        return True, True
    toks = _tokens_busqueda(cita)
    if not toks:
        return False, False
    aciertos = sum(1 for t in toks if t.lower() in tl)
    return False, aciertos >= 2 or (len(toks) == 1 and aciertos == 1)


def _cita_en_resultados_tavily(cita: str, resultados: list[dict[str, Any]]) -> bool:
    c = _normalizar_cita(cita).lower()
    if len(c) < 8:
        return False
    for item in resultados:
        blob = f"{item.get('title', '')} {item.get('content', '')} {item.get('url', '')}".lower()
        if c[: min(40, len(c))] in blob:
            return True
        for tok in _tokens_busqueda(cita)[:4]:
            if len(tok) >= 6 and tok.lower() in blob:
                return True
    return False


def _verificar_cita(
    cita: str,
    *,
    texto_base: str,
    sin_tavily: bool,
) -> VerificacionCita:
    """Orden: base interna → Tavily → marcar según reglas."""
    cita_limpia = _normalizar_cita(cita)
    if not cita_limpia:
        return VerificacionCita(
            cita_original=cita,
            estado="🔴 VERIFICAR",
            fuente="no_encontrada",
            nota="Cita vacía o no utilizable.",
        )

    fuerte, debil = _cita_en_base(cita_limpia, texto_base)

    if sin_tavily:
        if fuerte:
            return VerificacionCita(
                cita_original=cita_limpia,
                estado="⚠️ PROBABLE",
                fuente="base_conocimiento",
                nota="Coincidencia en base interna; TAVILY_API_KEY no configurada — confirmar en fuente oficial.",
            )
        if debil:
            return VerificacionCita(
                cita_original=cita_limpia,
                estado="⚠️ PROBABLE",
                fuente="base_conocimiento",
                nota="Coincidencia parcial en base interna; sin Tavily no se cruza con web. TAVILY_API_KEY no configurada.",
            )
        return VerificacionCita(
            cita_original=cita_limpia,
            estado="⚠️ PROBABLE",
            fuente="no_encontrada",
            nota="No hallada en base local; TAVILY_API_KEY no configurada — verificación externa pendiente.",
        )

    if fuerte:
        return VerificacionCita(
            cita_original=cita_limpia,
            estado="✅ VERIFICADA",
            fuente="base_conocimiento",
            nota="La cita (o su forma normalizada) aparece en la base de conocimiento jurídico interna.",
        )

    resultados = busqueda_tavily(f"{cita_limpia} Colombia jurisprudencia sentencia")
    if debil and not resultados:
        return VerificacionCita(
            cita_original=cita_limpia,
            estado="⚠️ PROBABLE",
            fuente="base_conocimiento",
            nota="Coincidencia parcial en base interna; Tavily no devolvió resultados en dominios filtrados.",
        )

    if resultados and _cita_en_resultados_tavily(cita_limpia, resultados):
        return VerificacionCita(
            cita_original=cita_limpia,
            estado="⚠️ PROBABLE",
            fuente="tavily",
            nota="Resultado en dominios jurídicos colombianos; contrastar con el fallo original.",
        )

    if debil:
        return VerificacionCita(
            cita_original=cita_limpia,
            estado="⚠️ PROBABLE",
            fuente="base_conocimiento",
            nota="Coincidencia débil en base interna; sin confirmación en Tavily.",
        )

    return VerificacionCita(
        cita_original=cita_limpia,
        estado="🔴 VERIFICAR",
        fuente="no_encontrada",
        nota="No localizada en base interna ni en resultados Tavily (dominios jurídicos CO).",
    )


def _run_jurisprudence_sync(inp: JurisprudenciaInput) -> JurisprudenciaOutput:
    texto_base = _cargar_texto_base_juridica()
    sin_tavily = not bool(os.environ.get("TAVILY_API_KEY", "").strip())

    resultados: list[VerificacionCita] = []
    for cita in inp.citas:
        resultados.append(_verificar_cita(str(cita), texto_base=texto_base, sin_tavily=sin_tavily))

    tokens_estimados = sum(len(str(c)) for c in inp.citas) + len(texto_base) // 100
    if os.environ.get("SUPABASE_URL") and (
        os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY")
    ):
        try:
            db.log_trazabilidad(
                UUID(str(inp.caso_id)),
                JURISPRUDENCE_AGENTE,
                MODELO_TRAZA,
                int(tokens_estimados),
                0,
                0,
                0.0,
            )
        except Exception:
            pass

    return JurisprudenciaOutput(
        resultados=resultados,
        tokens_usados=int(tokens_estimados),
        costo_usd=0.0,
    )


async def run_jurisprudence(inp: JurisprudenciaInput) -> JurisprudenciaOutput:
    """
    Verifica citas contra la base jurídica local y Tavily (dominios colombianos).

    No utiliza Anthropic. Si ``TAVILY_API_KEY`` no está definida, todas las citas
    se marcan como ``⚠️ PROBABLE`` según reglas de negocio.
    """
    return await asyncio.to_thread(_run_jurisprudence_sync, inp)
