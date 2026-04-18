"""Simulación adversarial (5A) — Brief 3.8, tarea S3.3."""

from __future__ import annotations

import asyncio
import json
import os
import time
from pathlib import Path
from typing import Any
from uuid import UUID

from pydantic import ValidationError

from apps.agents.core.json_utils import extraer_primer_json_con_clave_fase
from apps.agents.models.fase_output import AdversarialInput, AdversarialOutput
from apps.agents.tools import db

ADVERSARIAL_AGENTE = "adversarial"
MODELO_ADVERSARIAL = "claude-sonnet-4-5"
_FASE_5A_PATH = Path(__file__).resolve().parent.parent / "core" / "prompts" / "fase_5a.md"


def _sonnet_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """Precios de referencia Brief 3.7: Sonnet 4.5 — $3/MTok in, $15/MTok out."""
    return (input_tokens / 1_000_000) * 3.0 + (output_tokens / 1_000_000) * 15.0


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


def _lista_strings(valor: Any) -> list[str]:
    if not isinstance(valor, list):
        return []
    return [str(x).strip() for x in valor if str(x).strip()]


def _cinco_argumentos(valor: Any) -> list[str]:
    items = _lista_strings(valor)
    while len(items) < 5:
        items.append(
            "— (Argumento no generado: verificar respuesta del modelo o repetir la simulación.)"
        )
    return items[:5]


def _nulidades_propias(valor: Any) -> list[str]:
    if isinstance(valor, list):
        return _lista_strings(valor)
    if isinstance(valor, str) and valor.strip():
        return [valor.strip()]
    return []


def _adversarial_desde_raw(
    raw: dict[str, Any],
    *,
    tokens_api: int,
    costo_api: float,
) -> AdversarialOutput:
    contenido = _normalizar_contenido_fase(raw.get("contenido"))
    argumentos = _cinco_argumentos(contenido.get("argumentos"))

    ataque = contenido.get("ataque_no_obvio")
    ataque_no_obvio = str(ataque).strip() if ataque is not None else ""
    if not ataque_no_obvio:
        ataque_no_obvio = "No se recibió ataque_no_obvio estructurado."

    vuln = contenido.get("vulnerabilidad_probatoria")
    vulnerabilidad = str(vuln).strip() if vuln is not None else ""
    if not vulnerabilidad:
        vulnerabilidad = "No se recibió vulnerabilidad_probatoria estructurada."

    nulidades = _nulidades_propias(contenido.get("nulidades_propias"))

    tok = raw.get("tokens_usados")
    tokens_usados = int(tok) if tok is not None else int(tokens_api)

    costo_raw = raw.get("costo_usd")
    costo_usd = float(costo_raw) if costo_raw is not None else float(costo_api)

    return AdversarialOutput(
        argumentos=argumentos,
        ataque_no_obvio=ataque_no_obvio,
        vulnerabilidad_probatoria=vulnerabilidad,
        nulidades_propias=nulidades,
        tokens_usados=tokens_usados,
        costo_usd=costo_usd,
    )


def _fallback_output(tokens_api: int, costo_api: float, motivo: str) -> AdversarialOutput:
    base = motivo[:400] if motivo else "Fallo al parsear la salida del modelo."
    return AdversarialOutput(
        argumentos=[
            f"{base} — revisar integridad del JSON (argumento 1/5).",
            f"{base} — revisar integridad del JSON (argumento 2/5).",
            f"{base} — revisar integridad del JSON (argumento 3/5).",
            f"{base} — revisar integridad del JSON (argumento 4/5).",
            f"{base} — revisar integridad del JSON (argumento 5/5).",
        ],
        ataque_no_obvio="No disponible: la respuesta no contenía un JSON válido con clave «fase» y contenido parseable.",
        vulnerabilidad_probatoria="No disponible por el mismo motivo; revisar hechos y repetir la simulación.",
        nulidades_propias=["VERIFICAR: reproducir la simulación tras corregir el formato de salida del modelo."],
        tokens_usados=int(tokens_api),
        costo_usd=float(costo_api),
    )


def _cargar_prompt_fase_5a() -> str:
    if not _FASE_5A_PATH.is_file():
        raise RuntimeError(f"No se encontró el prompt de fase 5A en {_FASE_5A_PATH}")
    return _FASE_5A_PATH.read_text(encoding="utf-8")


def _caso_id_desde_input(inp: AdversarialInput) -> UUID:
    if not inp.hechos:
        raise ValueError("AdversarialInput requiere al menos un hecho para determinar caso_id (trazabilidad).")
    return UUID(str(inp.hechos[0].caso_id))


def _construir_user_payload(inp: AdversarialInput, caso_id: UUID) -> str:
    hechos_json = json.dumps(
        [h.model_dump(mode="json") for h in inp.hechos],
        ensure_ascii=False,
    )
    tipo = inp.tipo_accion.value if hasattr(inp.tipo_accion, "value") else str(inp.tipo_accion)
    return (
        "## Datos para simulación adversarial (sesión aislada)\n\n"
        "**No se incluyen** en este mensaje los outputs de fases 0E, 0A ni 0C. "
        "Solo los siguientes bloques:\n\n"
        "### caso_id (para el JSON de salida)\n"
        f"{caso_id}\n\n"
        "### tipo_accion\n"
        f"{tipo}\n\n"
        "### teoria_caso\n"
        f"{inp.teoria_caso.strip()}\n\n"
        "### hechos (JSON)\n"
        f"{hechos_json}\n\n"
        "### Instrucción de cierre\n"
        "Eres el mejor abogado de la contraparte. Tu único objetivo es destruir el caso que se describe. "
        'Al final, emite un único objeto JSON con clave "fase": "5A" y el contenido requerido '
        "(exactamente 5 strings en `argumentos`, `ataque_no_obvio`, `vulnerabilidad_probatoria`, "
        "`nulidades_propias`, más `tokens_usados` y `costo_usd` en la raíz del objeto como indica el prompt de fase)."
    )


def _llamada_sonnet_aislada(system: str, user_content: str) -> tuple[str, int, int, int]:
    """Devuelve (texto_modelo, input_tokens, output_tokens, duracion_ms)."""
    from anthropic import Anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY no está definida; es necesaria para la simulación adversarial."
        )

    client = Anthropic(api_key=api_key)
    t0 = time.perf_counter()
    msg = client.messages.create(
        model=MODELO_ADVERSARIAL,
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


def _run_adversarial_sync(inp: AdversarialInput) -> AdversarialOutput:
    caso_uuid = _caso_id_desde_input(inp)
    prompt_fase = _cargar_prompt_fase_5a()
    user_content = _construir_user_payload(inp, caso_uuid)

    system = (
        "Sesión completamente aislada: no tienes historial de conversación de LUMI Core ni acceso a "
        "outputs de fases 0E, 0A o 0C; solo el mensaje de usuario con hechos, teoría del caso y tipo de acción.\n\n"
        "Aplica el siguiente prompt operativo de fase 5A:\n\n"
        f"{prompt_fase.strip()}"
    )

    texto_modelo, input_tokens, output_tokens, duracion_ms = _llamada_sonnet_aislada(system, user_content)
    tokens_total = input_tokens + output_tokens
    costo = _sonnet_cost_usd(input_tokens, output_tokens)

    raw = extraer_primer_json_con_clave_fase(texto_modelo)
    if raw is None:
        out = _fallback_output(
            tokens_total,
            costo,
            "No se encontró en la respuesta un objeto JSON con clave «fase».",
        )
    else:
        try:
            out = _adversarial_desde_raw(raw, tokens_api=tokens_total, costo_api=costo)
        except (TypeError, ValueError, KeyError, ValidationError):
            out = _fallback_output(
                tokens_total,
                costo,
                "El JSON con «fase» no pudo mapearse a AdversarialOutput.",
            )

    db.log_trazabilidad(
        caso_uuid,
        ADVERSARIAL_AGENTE,
        MODELO_ADVERSARIAL,
        input_tokens,
        output_tokens,
        duracion_ms,
        costo,
    )
    return out


async def run_adversarial(inp: AdversarialInput) -> AdversarialOutput:
    """
    Simulación adversarial 5A: Sonnet, ``fase_5a.md``, sin historial ni outputs 0E/0A/0C en el contexto.

    El JSON se detecta con el primer objeto que contiene la clave ``fase`` (mismo criterio que LUMI Core).
    """
    return await asyncio.to_thread(_run_adversarial_sync, inp)
