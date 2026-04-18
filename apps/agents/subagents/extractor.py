"""Subagente Extractor de documentos (3.8) — parsing + Claude Haiku + persistencia."""

from __future__ import annotations

import json
import os
import time
from typing import Any
from uuid import UUID

from pydantic import ValidationError

from apps.agents.models.documento import (
    ExtractorInput,
    ExtractorOutput,
    FechaDetectada,
    ParteDetectada,
    RolParte,
)
from apps.agents.models.hecho import EstatusEpistemico, Hecho
from apps.agents.tools import db
from apps.agents.tools.document_parser import parse_document

EXTRACTOR_AGENTE = "extractor"
EXTRACTOR_FASE_ORIGEN = "extractor"
MODELO_EXTRACTOR = "claude-haiku-4-5"


def _haiku_cost_usd(input_tokens: int, output_tokens: int) -> float:
    return (input_tokens / 1_000_000) * 0.25 + (output_tokens / 1_000_000) * 1.25


def _nombre_original_por_mime(mime_type: str) -> str:
    base = mime_type.split(";", maxsplit=1)[0].strip().lower()
    mapping: dict[str, str] = {
        "application/pdf": "documento.pdf",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "documento.docx",
        "image/jpeg": "documento.jpg",
        "image/jpg": "documento.jpg",
        "image/png": "documento.png",
        "image/webp": "documento.webp",
    }
    return mapping.get(base, "documento")


def _estatus_epistemico(valor: str | None) -> EstatusEpistemico:
    if not valor:
        return EstatusEpistemico.inferido
    try:
        return EstatusEpistemico(valor)
    except ValueError:
        return EstatusEpistemico.inferido


def _rol_parte(valor: str | None) -> RolParte:
    if not valor:
        return RolParte.otro
    try:
        return RolParte(valor)
    except ValueError:
        return RolParte.otro


def _extraer_objeto_json(texto: str) -> dict[str, Any]:
    s = texto.strip()
    if s.startswith("```"):
        lineas = s.splitlines()
        if lineas and lineas[0].lstrip().startswith("```"):
            lineas = lineas[1:]
        if lineas and lineas[-1].strip().startswith("```"):
            lineas = lineas[:-1]
        s = "\n".join(lineas).strip()
    inicio = s.find("{")
    fin = s.rfind("}")
    if inicio == -1 or fin == -1 or fin <= inicio:
        raise ValueError("La respuesta del modelo no contiene un objeto JSON.")
    try:
        return json.loads(s[inicio : fin + 1])
    except json.JSONDecodeError as exc:
        raise ValueError("JSON del modelo inválido.") from exc


def _llamada_extractor_haiku(texto_documento: str) -> tuple[dict[str, Any], int, int, int]:
    """Devuelve (payload_json, input_tokens, output_tokens, duracion_ms)."""
    from anthropic import Anthropic

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY no está definida; es necesaria para el extractor.")

    system = (
        "Eres un asistente jurídico para el derecho colombiano. "
        "Analizas el texto de un documento del expediente y respondes SOLO con un objeto JSON válido, "
        "sin markdown ni texto fuera del JSON."
    )
    schema = (
        "El JSON debe tener exactamente estas claves:\n"
        '- "tipo_detectado": string o null (ej: acta_icbf, factura_educacion, otro)\n'
        '- "hechos": lista de objetos {"contenido": string, "estatus_epistemico": '
        '"verificado"|"inferido"|"desconocido"|"contradicho", "fuente": string o null}\n'
        '- "partes_detectadas": lista de {"nombre": string, "rol": "demandante"|"demandado"|"otro"}\n'
        '- "fechas_detectadas": lista de {"fecha": string, "contexto": string}\n'
        '- "alertas": lista de strings (vacía si no hay)\n'
        "No inventes hechos que no estén fundados en el texto del documento."
    )
    user = f"Texto del documento:\n\n{texto_documento}\n\n{schema}"

    client = Anthropic(api_key=api_key)
    t0 = time.perf_counter()
    msg = client.messages.create(
        model=MODELO_EXTRACTOR,
        max_tokens=8_192,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    duracion_ms = int((time.perf_counter() - t0) * 1000)

    texto_respuesta = ""
    for bloque in msg.content:
        if bloque.type == "text":
            texto_respuesta += bloque.text

    uso = msg.usage
    input_tokens = int(uso.input_tokens)
    output_tokens = int(uso.output_tokens)
    payload = _extraer_objeto_json(texto_respuesta)
    return payload, input_tokens, output_tokens, duracion_ms


def _partes_desde_payload(items: list[Any]) -> list[ParteDetectada]:
    salida: list[ParteDetectada] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            salida.append(
                ParteDetectada(
                    nombre=str(item.get("nombre", "")).strip() or "—",
                    rol=_rol_parte(str(item.get("rol", "")).strip() or None),
                )
            )
        except ValidationError:
            continue
    return salida


def _fechas_desde_payload(items: list[Any]) -> list[FechaDetectada]:
    salida: list[FechaDetectada] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        try:
            salida.append(
                FechaDetectada(
                    fecha=str(item.get("fecha", "")).strip() or "—",
                    contexto=str(item.get("contexto", "")).strip() or "—",
                )
            )
        except ValidationError:
            continue
    return salida


def run(inp: ExtractorInput) -> ExtractorOutput:
    """
    Orquesta parsing, extracción estructurada con Haiku y persistencia en Supabase.

    No usa historial de conversación: una sola llamada al modelo con el texto parseado.
    """
    extracto = parse_document(inp.archivo_bytes, inp.mime_type)
    texto = extracto.texto_extraido

    payload, tokens_in, tokens_out, duracion_ms = _llamada_extractor_haiku(texto)
    costo = _haiku_cost_usd(tokens_in, tokens_out)
    tokens_total = tokens_in + tokens_out

    tipo_raw = payload.get("tipo_detectado")
    tipo_detectado = str(tipo_raw).strip() if tipo_raw is not None else None
    if tipo_detectado == "":
        tipo_detectado = None

    alertas_raw = payload.get("alertas")
    if isinstance(alertas_raw, list):
        alertas = [str(a) for a in alertas_raw if str(a).strip()]
    else:
        alertas = []

    partes = _partes_desde_payload(payload.get("partes_detectadas") or [])
    fechas = _fechas_desde_payload(payload.get("fechas_detectadas") or [])

    nombre_original = _nombre_original_por_mime(inp.mime_type)
    db.save_documento(
        UUID(str(inp.documento_id)),
        UUID(str(inp.caso_id)),
        nombre_original,
        inp.mime_type,
        texto_extraido=texto,
        tipo_detectado=tipo_detectado,
        estado="listo",
        storage_path=None,
    )

    hechos_detectados: list[Hecho] = []
    for h in payload.get("hechos") or []:
        if not isinstance(h, dict):
            continue
        contenido = str(h.get("contenido", "")).strip()
        if not contenido:
            continue
        estatus = _estatus_epistemico(str(h.get("estatus_epistemico", "")).strip() or None)
        fuente = h.get("fuente")
        fuente_str = str(fuente).strip() if fuente is not None else None
        if fuente_str == "":
            fuente_str = None

        hecho_id = db.save_hecho(
            UUID(str(inp.caso_id)),
            EXTRACTOR_FASE_ORIGEN,
            contenido,
            estatus,
            fuente=fuente_str,
        )
        hechos_detectados.append(
            Hecho(
                id=hecho_id,
                caso_id=UUID(str(inp.caso_id)),
                fase_origen=EXTRACTOR_FASE_ORIGEN,
                contenido=contenido,
                estatus_epistemico=estatus,
                fuente=fuente_str,
            )
        )

    db.log_trazabilidad(
        UUID(str(inp.caso_id)),
        EXTRACTOR_AGENTE,
        MODELO_EXTRACTOR,
        tokens_in,
        tokens_out,
        duracion_ms,
        costo,
    )

    return ExtractorOutput(
        texto_extraido=texto,
        hechos_detectados=hechos_detectados,
        partes_detectadas=partes,
        fechas_detectadas=fechas,
        alertas=alertas,
        tokens_usados=tokens_total,
        costo_usd=costo,
    )
