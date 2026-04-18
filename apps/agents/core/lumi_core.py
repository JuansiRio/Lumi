"""LUMI Core — orquestador principal (Brief 3.8, tarea S2.2)."""

from __future__ import annotations

import json
import os
import time
from typing import Any
from uuid import UUID

from pydantic import ValidationError

from apps.agents.core import context_manager
from apps.agents.core.json_utils import extraer_primer_json_con_clave_fase_y_rango
from apps.agents.models.caso import ContextoComprimido
from apps.agents.models.fase_output import FaseOutput, LumiCoreInput, LumiCoreResponse
from apps.agents.tools import db

MODELO_LUMI_CORE = "claude-sonnet-4-5"
AGENTE_TRAZABILIDAD = "lumi_core"


def _sonnet_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """Precios de referencia Brief 3.7: Sonnet 4.5 — $3/MTok in, $15/MTok out."""
    return (input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0


def _respuesta_sin_bloque_json(texto: str, inicio: int, fin_exclusivo: int) -> str:
    """Quita el fragmento JSON del texto mostrado al abogado."""
    izq = texto[:inicio].rstrip()
    der = texto[fin_exclusivo:].lstrip()
    if izq and der:
        return f"{izq}\n\n{der}".strip()
    return (izq or der).strip() or texto.strip()


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
    return {"valor": valor}


def _construir_fase_output(
    raw: dict[str, Any],
    *,
    caso_id: UUID,
    tokens_api: int,
    costo_api: float,
) -> FaseOutput:
    fase_raw = raw.get("fase")
    if fase_raw is None:
        raise ValueError("El JSON de fase no incluye 'fase'.")
    fase = context_manager._canonical_fase_code(str(fase_raw))

    version_val = raw.get("version")
    if version_val is None:
        version = db.get_max_version_output_fase(caso_id, fase) + 1
    else:
        version = int(version_val)

    contenido = _normalizar_contenido_fase(raw.get("contenido"))

    aprobado = bool(raw.get("aprobado_abogado", False))
    anotaciones = raw.get("anotaciones")
    anotaciones_str = str(anotaciones) if anotaciones is not None else None

    tok = raw.get("tokens_usados")
    tokens_usados = int(tok) if tok is not None else int(tokens_api)

    costo_raw = raw.get("costo_usd")
    costo_usd = float(costo_raw) if costo_raw is not None else float(costo_api)

    return FaseOutput(
        caso_id=caso_id,
        fase=fase,
        version=version,
        contenido=contenido,
        aprobado_abogado=aprobado,
        anotaciones=anotaciones_str,
        tokens_usados=tokens_usados,
        costo_usd=costo_usd,
    )


def _ensamblar_user_contexto(ctx: ContextoComprimido, mensaje_abogado: str) -> str:
    hechos_json = json.dumps(
        [h.model_dump(mode="json") for h in ctx.hechos_relevantes],
        ensure_ascii=False,
    )
    mensajes_json = json.dumps(ctx.ultimos_mensajes, ensure_ascii=False, default=str)
    resumenes = "\n\n".join(ctx.resumenes_fases) if ctx.resumenes_fases else "(sin resúmenes de fases aprobadas previas)"

    return (
        "## Instrucciones de fase\n"
        f"{ctx.prompt_fase}\n\n"
        "## Resúmenes de fases aprobadas\n"
        f"{resumenes}\n\n"
        "## Hechos relevantes (JSON)\n"
        f"{hechos_json}\n\n"
        "## Últimos mensajes de la sesión (JSON)\n"
        f"{mensajes_json}\n\n"
        "## Mensaje del abogado\n"
        f"{mensaje_abogado.strip()}\n\n"
        "Si concluyes formalmente esta fase y debes registrar un output estructurado, "
        "incluye en tu respuesta un único objeto JSON (con la clave \"fase\") con los campos "
        "requeridos para el output de fase. LUMI propone; el abogado decide y firma."
    )


def process_message(inp: LumiCoreInput) -> LumiCoreResponse:
    """
    Procesa un turno de chat: contexto comprimido, Claude Sonnet, sesión y trazabilidad.

    Tras la llamada a Sonnet se analiza el texto en busca de un JSON con clave ``fase``;
    si es válido como ``FaseOutput``, ese bloque se retira de la respuesta mostrada al abogado.
    Orden de persistencia: mensajes de sesión (abogado y LUMI), ``log_trazabilidad``,
    y finalmente ``save_output_fase`` cuando corresponda.
    """
    caso_uuid = UUID(str(inp.caso_id))
    fase_para_sesion = context_manager._canonical_fase_code(inp.fase_actual)

    ctx = context_manager.build_context(caso_uuid, inp.fase_actual)

    system = (
        f"{ctx.prompt_maestro.strip()}\n\n"
        "Eres LUMI, asistente jurídico para el derecho colombiano. "
        "Responde con rigor, en español, sin inventar hechos no sustentados en el contexto. "
        "Cuando corresponda un cierre de fase con output estructurado, añade el objeto JSON "
        'con clave "fase" además de tu respuesta en prosa.'
    )
    user_content = _ensamblar_user_contexto(ctx, inp.mensaje)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY no está definida; es necesaria para LUMI Core.")

    from anthropic import Anthropic

    client = Anthropic(api_key=api_key)
    t0 = time.perf_counter()
    msg = client.messages.create(
        model=MODELO_LUMI_CORE,
        max_tokens=8_192,
        system=system,
        messages=[{"role": "user", "content": user_content}],
    )
    duracion_ms = int((time.perf_counter() - t0) * 1000)

    texto_modelo = ""
    for bloque in msg.content:
        if bloque.type == "text":
            texto_modelo += bloque.text

    uso = msg.usage
    input_tokens = int(uso.input_tokens)
    output_tokens = int(uso.output_tokens)
    tokens_total = input_tokens + output_tokens
    costo = _sonnet_cost_usd(input_tokens, output_tokens)

    fase_output: FaseOutput | None = None
    respuesta_texto = texto_modelo.strip()

    hallazgo = extraer_primer_json_con_clave_fase_y_rango(texto_modelo)
    if hallazgo is not None:
        raw_dict, ini, fin = hallazgo
        try:
            fase_output = _construir_fase_output(
                raw_dict,
                caso_id=caso_uuid,
                tokens_api=tokens_total,
                costo_api=costo,
            )
            respuesta_texto = _respuesta_sin_bloque_json(texto_modelo, ini, fin)
        except (ValueError, TypeError, KeyError, ValidationError):
            fase_output = None
            respuesta_texto = texto_modelo.strip()

    db.save_sesion_mensaje(caso_uuid, "abogado", inp.mensaje.strip(), fase=fase_para_sesion)
    db.save_sesion_mensaje(caso_uuid, "lumi", respuesta_texto, fase=fase_para_sesion)

    db.log_trazabilidad(
        caso_uuid,
        AGENTE_TRAZABILIDAD,
        MODELO_LUMI_CORE,
        input_tokens,
        output_tokens,
        duracion_ms,
        costo,
    )

    if fase_output is not None:
        db.save_output_fase(fase_output)

    return LumiCoreResponse(
        respuesta=respuesta_texto,
        fase_output=fase_output,
        subagente_llamado=None,
        tokens_usados=tokens_total,
        costo_usd=costo,
    )
