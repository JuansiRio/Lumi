"""Motor probabilístico (2A) — Brief 3.8, tarea S3.2."""

from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any
from uuid import UUID

from pydantic import ValidationError

from apps.agents.models.fase_output import Factor, ProbabilisticInput, ProbabilisticOutput
from apps.agents.tools import db

PROBABILISTIC_AGENTE = "probabilistic"
MODELO_PROBABILISTIC = "claude-haiku-4-5"
_FASE_2A_PATH = Path(__file__).resolve().parent.parent / "core" / "prompts" / "fase_2a.md"


def _haiku_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """Precios de referencia Brief 3.7: Haiku 4.5 — $0.25/MTok in, $1.25/MTok out."""
    return (input_tokens / 1_000_000) * 0.25 + (output_tokens / 1_000_000) * 1.25


def _extraer_primer_json_con_clave_fase(texto: str) -> dict[str, Any] | None:
    """
    Busca el primer objeto JSON en ``texto`` que contenga la clave ``fase``.

    Mismo patrón que ``apps.agents.core.lumi_core._extraer_primer_json_con_clave_fase``.
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
            return obj
        i += 1
    return None


def _normalizar_contenido_fase(valor: Any) -> dict[str, Any]:
    if isinstance(valor, dict):
        return valor
    if isinstance(valor, str):
        try:
            parsed = json.loads(valor)
            if isinstance(parsed, dict):
                return parsed
        except json.JSONDecodeError:
            pass
        return {"texto": valor}
    return {}


def _clamp01(x: Any) -> float:
    try:
        v = float(x)
    except (TypeError, ValueError):
        return 0.5
    return max(0.0, min(1.0, v))


def _factores_desde_payload(items: Any) -> list[Factor]:
    salida: list[Factor] = []
    if not isinstance(items, list):
        return salida
    for item in items:
        if not isinstance(item, dict):
            continue
        nombre = str(item.get("nombre", "")).strip() or "—"
        nota = str(item.get("nota", "")).strip() or "—"
        peso_raw = item.get("peso", 0.2)
        try:
            peso = float(peso_raw)
        except (TypeError, ValueError):
            peso = 0.2
        peso = max(0.0, min(1.0, peso))
        dir_raw = str(item.get("direccion", "neutro")).strip().lower()
        if dir_raw not in ("favorable", "desfavorable", "neutro"):
            dir_raw = "neutro"
        try:
            salida.append(Factor(nombre=nombre, peso=peso, direccion=dir_raw, nota=nota))
        except ValidationError:
            continue
    return salida


def _advertencias_desde_payload(valor: Any) -> list[str]:
    if not isinstance(valor, list):
        return []
    return [str(a).strip() for a in valor if str(a).strip()]


def _probabilistic_desde_raw(
    raw: dict[str, Any],
    *,
    tokens_api: int,
    costo_api: float,
) -> ProbabilisticOutput:
    contenido = _normalizar_contenido_fase(raw.get("contenido"))

    r_min = _clamp01(contenido.get("rango_min"))
    r_max = _clamp01(contenido.get("rango_max"))
    if r_max < r_min:
        r_min, r_max = r_max, r_min

    c_m = _clamp01(contenido.get("centro_masa"))
    if c_m < r_min:
        c_m = r_min
    if c_m > r_max:
        c_m = r_max

    factores = _factores_desde_payload(contenido.get("factores"))
    if not factores:
        factores = [
            Factor(
                nombre="Sin factores estructurados en la respuesta",
                peso=1.0,
                direccion="neutro",
                nota="El modelo no devolvió la lista de factores esperada; revisar el JSON.",
            )
        ]

    just = contenido.get("justificacion")
    justificacion = str(just).strip() if just is not None else ""
    if not justificacion:
        justificacion = "Sin campo justificacion en contenido; usar narrativa del modelo en prosa si está disponible."

    advertencias = _advertencias_desde_payload(contenido.get("advertencias"))

    tok = raw.get("tokens_usados")
    tokens_usados = int(tok) if tok is not None else int(tokens_api)

    costo_raw = raw.get("costo_usd")
    costo_usd = float(costo_raw) if costo_raw is not None else float(costo_api)

    return ProbabilisticOutput(
        rango_min=r_min,
        rango_max=r_max,
        centro_masa=c_m,
        factores=factores,
        justificacion=justificacion,
        advertencias=advertencias,
        tokens_usados=tokens_usados,
        costo_usd=costo_usd,
    )


def _fallback_output(tokens_api: int, costo_api: float, motivo: str) -> ProbabilisticOutput:
    return ProbabilisticOutput(
        rango_min=0.35,
        rango_max=0.65,
        centro_masa=0.5,
        factores=[
            Factor(
                nombre="Incertidumbre por parseo o respuesta incompleta",
                peso=1.0,
                direccion="neutro",
                nota=motivo[:500],
            )
        ],
        justificacion=motivo,
        advertencias=[motivo],
        tokens_usados=int(tokens_api),
        costo_usd=float(costo_api),
    )


def _cargar_prompt_fase_2a() -> str:
    if not _FASE_2A_PATH.is_file():
        raise RuntimeError(f"No se encontró el prompt de fase 2A en {_FASE_2A_PATH}")
    return _FASE_2A_PATH.read_text(encoding="utf-8")


def _caso_id_desde_input(inp: ProbabilisticInput) -> UUID:
    if not inp.hechos:
        raise ValueError("ProbabilisticInput requiere al menos un hecho para determinar caso_id (trazabilidad).")
    return UUID(str(inp.hechos[0].caso_id))


def _construir_user_payload(inp: ProbabilisticInput) -> str:
    hechos_json = json.dumps(
        [h.model_dump(mode="json") for h in inp.hechos],
        ensure_ascii=False,
    )
    tipo = inp.tipo_accion.value if hasattr(inp.tipo_accion, "value") else str(inp.tipo_accion)
    return (
        "## Datos del caso (subagente aislado — sin historial de chat)\n\n"
        "### tipo_accion\n"
        f"{tipo}\n\n"
        "### teoria_caso\n"
        f"{inp.teoria_caso.strip()}\n\n"
        "### hechos (JSON)\n"
        f"{hechos_json}\n\n"
        "### Instrucción de cierre\n"
        'Concluye con un único objeto JSON que incluya la clave "fase": "2A" y los campos '
        "exigidos en el prompt de fase (incluyendo contenido con rango_min, rango_max, "
        "centro_masa, factores, justificacion, advertencias, tokens_usados, costo_usd). "
        "Los valores rango_* y centro_masa deben ser floats entre 0 y 1."
    )


def _llamada_haiku_aislada(system: str, user_content: str) -> tuple[str, int, int, int]:
    """Devuelve (texto_modelo, input_tokens, output_tokens, duracion_ms)."""
    from anthropic import Anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY no está definida; es necesaria para el motor probabilístico."
        )

    client = Anthropic(api_key=api_key)
    t0 = time.perf_counter()
    msg = client.messages.create(
        model=MODELO_PROBABILISTIC,
        max_tokens=8_192,
        system=system,
        messages=[{"role": "user", "content": user_content}],
    )
    duracion_ms = int((time.perf_counter() - t0) * 1000)

    texto = ""
    for bloque in msg.content:
        if bloque.type == "text":
            texto += bloque.text

    uso = msg.usage
    input_tokens = int(uso.input_tokens)
    output_tokens = int(uso.output_tokens)
    return texto, input_tokens, output_tokens, duracion_ms


def _run_probabilistic_sync(inp: ProbabilisticInput) -> ProbabilisticOutput:
    caso_uuid = _caso_id_desde_input(inp)
    prompt_fase = _cargar_prompt_fase_2a()
    user_content = _construir_user_payload(inp)

    system = (
        "Eres el subagente de motor probabilístico de LUMI (Fase 2A) para el derecho colombiano. "
        "Sesión aislada: no asumas historial de conversación fuera del mensaje de usuario con datos. "
        "Aplica en su integridad el siguiente prompt de fase 2A:\n\n"
        f"{prompt_fase.strip()}"
    )

    texto_modelo, input_tokens, output_tokens, duracion_ms = _llamada_haiku_aislada(system, user_content)
    tokens_total = input_tokens + output_tokens
    costo = _haiku_cost_usd(input_tokens, output_tokens)

    raw = _extraer_primer_json_con_clave_fase(texto_modelo)
    if raw is None:
        out = _fallback_output(
            tokens_total,
            costo,
            "No se encontró en la respuesta un objeto JSON con clave «fase».",
        )
    else:
        try:
            out = _probabilistic_desde_raw(raw, tokens_api=tokens_total, costo_api=costo)
        except (TypeError, ValueError, KeyError, ValidationError):
            out = _fallback_output(
                tokens_total,
                costo,
                "El JSON con «fase» no pudo mapearse a ProbabilisticOutput.",
            )

    db.log_trazabilidad(
        caso_uuid,
        PROBABILISTIC_AGENTE,
        MODELO_PROBABILISTIC,
        input_tokens,
        output_tokens,
        duracion_ms,
        costo,
    )
    return out


async def run_probabilistic(inp: ProbabilisticInput) -> ProbabilisticOutput:
    """
    Motor probabilístico 2A: Haiku, prompt ``fase_2a.md``, sesión sin historial de conversación.

    El JSON se detecta buscando el primer objeto con clave ``fase`` (mismo criterio que LUMI Core).
    """
    return await asyncio.to_thread(_run_probabilistic_sync, inp)
