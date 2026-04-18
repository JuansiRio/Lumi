"""Control de calidad QA — Brief 3.8, tarea S4.1."""

from __future__ import annotations

import asyncio
import json
import os
import time
from typing import Any
from uuid import UUID

from pydantic import ValidationError

from apps.agents.models.fase_output import (
    Correccion,
    PrioridadCorreccion,
    QAInput,
    QAOutput,
    SemaforoQA,
)
from apps.agents.tools import db

QA_AGENTE = "qa"
MODELO_QA = "claude-haiku-4-5"

_CHECKLIST_QA = """
Checklist obligatoria (revisa cada ítem y refleja hallazgos en ``correcciones`` cuando aplique):

1. **Coherencia interna** — Los hechos del caso y el borrador no deben contradecirse entre sí.
2. **Sustento fáctico de pretensiones** — Cada pretensión relevante debe apoyarse en hechos documentados o claramente asentados en el texto.
3. **Citas normativas** — Las normas citadas deben ser pertinentes al ``tipo_accion`` (no exijas fallos concretos no verificables).
4. **Identificación de partes** — Nombres, documentos y calidades procesales coherentes con los hechos.
5. **Medidas cautelares** — Si el borrador las incluye, verificar que estén formuladas de forma procesalmente razonable; si no hay, marcar N/A sin inventar defectos.
6. **Protocolo de verificación** — Debe existir al final del borrador (o sección equivalente) un bloque de verificación/jurisprudencia o checklist de cierre según lo esperado en el documento.
7. **Números y cifras** — Cantidades, fechas y porcentajes coherentes con los hechos aportados (sin exigir peritaje que no conste).

Para cada problema, añade un ítem en ``correcciones`` con ``prioridad`` exactamente una de:
``\"🔴 crítico\"``, ``\"🟡 importante\"``, ``\"🟢 menor\"`` (con emoji y texto como en el contrato).
"""


def _haiku_cost_usd(input_tokens: int, output_tokens: int) -> float:
    """Precios de referencia Brief 3.7: Haiku 4.5 — $0.25/MTok in, $1.25/MTok out."""
    return (input_tokens / 1_000_000) * 0.25 + (output_tokens / 1_000_000) * 1.25


def _extraer_primer_json_con_clave_fase(texto: str) -> dict[str, Any] | None:
    """Busca el primer objeto JSON en ``texto`` que contenga la clave ``fase``."""
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


def _prioridad_correccion(valor: Any) -> PrioridadCorreccion | None:
    s = str(valor).strip() if valor is not None else ""
    candidatos: tuple[PrioridadCorreccion, ...] = ("🔴 crítico", "🟡 importante", "🟢 menor")
    for c in candidatos:
        if s == c:
            return c
    sl = s.lower()
    if "crítico" in sl or "critico" in sl:
        return "🔴 crítico"
    if "importante" in sl:
        return "🟡 importante"
    if "menor" in sl:
        return "🟢 menor"
    return None


def _correcciones_desde_payload(items: Any) -> list[Correccion]:
    salida: list[Correccion] = []
    if not isinstance(items, list):
        return salida
    for item in items:
        if not isinstance(item, dict):
            continue
        pr = _prioridad_correccion(item.get("prioridad"))
        if pr is None:
            continue
        ubicacion = str(item.get("ubicacion", "")).strip() or "—"
        descripcion = str(item.get("descripcion", "")).strip() or "—"
        sugerencia = str(item.get("sugerencia", "")).strip() or "—"
        try:
            salida.append(
                Correccion(
                    prioridad=pr,
                    ubicacion=ubicacion,
                    descripcion=descripcion,
                    sugerencia=sugerencia,
                )
            )
        except ValidationError:
            continue
    return salida


def _semaforo_desde_valor(valor: Any) -> SemaforoQA:
    s = str(valor).strip() if valor is not None else ""
    validos: tuple[SemaforoQA, ...] = ("🟢 LISTO", "🟡 OBSERVACIONES", "🔴 CRÍTICO")
    for v in validos:
        if s == v:
            return v
    if "CRÍTICO" in s or "CRITICO" in s.upper():
        return "🔴 CRÍTICO"
    if "OBSERVACIONES" in s.upper() or "AMARILLO" in s.upper():
        return "🟡 OBSERVACIONES"
    if "LISTO" in s.upper() or "VERDE" in s.upper():
        return "🟢 LISTO"
    return "🟡 OBSERVACIONES"


def _aprobado_coherente(
    semaforo: SemaforoQA,
    correcciones: list[Correccion],
    aprobado_modelo: bool | None,
) -> bool:
    """Reglas de negocio: semáforo, correcciones críticas y consistencia."""
    if any(c.prioridad == "🔴 crítico" for c in correcciones):
        return False
    if semaforo == "🔴 CRÍTICO":
        return False
    if semaforo == "🟡 OBSERVACIONES":
        return False
    if semaforo == "🟢 LISTO":
        return True
    return bool(aprobado_modelo)


def _qa_desde_raw(
    raw: dict[str, Any],
    *,
    tokens_api: int,
    costo_api: float,
) -> QAOutput:
    contenido = _normalizar_contenido_fase(raw.get("contenido"))
    semaforo = _semaforo_desde_valor(contenido.get("semaforo_general"))
    correcciones = _correcciones_desde_payload(contenido.get("correcciones"))
    raw_aprobado = contenido.get("aprobado")
    aprobado_modelo: bool | None
    if isinstance(raw_aprobado, bool):
        aprobado_modelo = raw_aprobado
    else:
        aprobado_modelo = None
    aprobado = _aprobado_coherente(semaforo, correcciones, aprobado_modelo)

    tok = raw.get("tokens_usados")
    tokens_usados = int(tok) if tok is not None else int(tokens_api)

    costo_raw = raw.get("costo_usd")
    costo_usd = float(costo_raw) if costo_raw is not None else float(costo_api)

    return QAOutput(
        semaforo_general=semaforo,
        correcciones=correcciones,
        aprobado=aprobado,
        tokens_usados=tokens_usados,
        costo_usd=costo_usd,
    )


def _fallback_qa(tokens_api: int, costo_api: float, motivo: str) -> QAOutput:
    return QAOutput(
        semaforo_general="🔴 CRÍTICO",
        correcciones=[
            Correccion(
                prioridad="🔴 crítico",
                ubicacion="Salida del modelo",
                descripcion=motivo[:400],
                sugerencia="Repetir la revisión QA o corregir el formato JSON de salida.",
            )
        ],
        aprobado=False,
        tokens_usados=int(tokens_api),
        costo_usd=float(costo_api),
    )


def _caso_id_desde_input(inp: QAInput) -> UUID:
    if not inp.hechos:
        raise ValueError("QAInput requiere al menos un hecho para determinar caso_id (trazabilidad).")
    return UUID(str(inp.hechos[0].caso_id))


def _construir_system_prompt() -> str:
    return (
        "Eres el subagente de **control de calidad (QA)** de LUMI para documentos jurídicos colombianos. "
        "Sesión **aislada**: no tienes historial de chat ni otros outputs de fases; solo el mensaje de usuario.\n\n"
        "Tu tarea es revisar el **borrador** contra la checklist y emitir un veredicto estructurado.\n\n"
        f"{_CHECKLIST_QA.strip()}\n\n"
        "### Formato de salida (obligatorio)\n"
        "Cierra con **un solo** objeto JSON válido (sin fence markdown) que incluya:\n"
        '- `"fase"`: `"QA"`\n'
        '- `"version"`: entero (p. ej. 1)\n'
        '- `"contenido"`: objeto con:\n'
        '  - `"semaforo_general"`: exactamente uno de `"🟢 LISTO"`, `"🟡 OBSERVACIONES"`, `"🔴 CRÍTICO"`\n'
        '  - `"correcciones"`: lista de objetos `{ "prioridad", "ubicacion", "descripcion", "sugerencia" }`\n'
        '  - `"aprobado"`: boolean (el backend puede recalcularlo según reglas; sé coherente con el semáforo)\n'
        '- `"tokens_usados"` y `"costo_usd"`: número entero y float estimados del turno.\n'
        "Si no hay correcciones, usa `correcciones: []`."
    )


def _construir_user_payload(inp: QAInput) -> str:
    hechos_json = json.dumps(
        [h.model_dump(mode="json") for h in inp.hechos],
        ensure_ascii=False,
    )
    tipo = inp.tipo_accion.value if hasattr(inp.tipo_accion, "value") else str(inp.tipo_accion)
    return (
        "## Datos para revisión QA\n\n"
        "### tipo_accion\n"
        f"{tipo}\n\n"
        "### teoria_caso\n"
        f"{inp.teoria_caso.strip()}\n\n"
        "### hechos (JSON)\n"
        f"{hechos_json}\n\n"
        "### borrador_texto\n"
        f"{inp.borrador_texto.strip()}\n"
    )


def _llamada_haiku_aislada(system: str, user_content: str) -> tuple[str, int, int, int]:
    """Devuelve (texto_modelo, input_tokens, output_tokens, duracion_ms)."""
    from anthropic import Anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY no está definida; es necesaria para el subagente QA.")

    client = Anthropic(api_key=api_key)
    t0 = time.perf_counter()
    msg = client.messages.create(
        model=MODELO_QA,
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


def _run_qa_sync(inp: QAInput) -> QAOutput:
    caso_uuid = _caso_id_desde_input(inp)
    system = _construir_system_prompt()
    user_content = _construir_user_payload(inp)

    texto_modelo, input_tokens, output_tokens, duracion_ms = _llamada_haiku_aislada(system, user_content)
    tokens_total = input_tokens + output_tokens
    costo = _haiku_cost_usd(input_tokens, output_tokens)

    raw = _extraer_primer_json_con_clave_fase(texto_modelo)
    if raw is None:
        out = _fallback_qa(
            tokens_total,
            costo,
            "No se encontró en la respuesta un objeto JSON con clave «fase».",
        )
    else:
        try:
            out = _qa_desde_raw(raw, tokens_api=tokens_total, costo_api=costo)
        except (TypeError, ValueError, KeyError, ValidationError):
            out = _fallback_qa(
                tokens_total,
                costo,
                "El JSON con «fase» no pudo mapearse a QAOutput.",
            )

    db.log_trazabilidad(
        caso_uuid,
        QA_AGENTE,
        MODELO_QA,
        input_tokens,
        output_tokens,
        duracion_ms,
        costo,
    )
    return out


async def run_qa(inp: QAInput) -> QAOutput:
    """
    Control de calidad del borrador: Haiku, sesión aislada, checklist interna.

    El JSON se detecta con el primer objeto que contiene la clave ``fase`` (típicamente ``\"QA\"``).
    """
    return await asyncio.to_thread(_run_qa_sync, inp)
