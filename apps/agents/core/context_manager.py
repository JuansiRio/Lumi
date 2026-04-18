"""
Context Manager — sección 3.5 del Technical Brief y tarea S2.1 del Implementation Plan.

Ensambla el contexto comprimido que recibe LUMI Core en cada turno, sin superar el
techo de tokens configurado (25.000 por defecto).
"""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any
from uuid import UUID

import httpx

from apps.agents.models.caso import ContextManagerInput, ContextoComprimido
from apps.agents.models.fase_output import FaseOutput
from apps.agents.models.hecho import Hecho
from apps.agents.tools import db

_PROMPTS_DIR = Path(__file__).resolve().parent / "prompts"

_FASE_CODE_TO_STEM: dict[str, str] = {
    "0E": "fase_0e",
    "0A": "fase_0a",
    "0C": "fase_0c",
    "1A": "fase_1a",
    "1C": "fase_1c",
    "2A": "fase_2a",
    "5A": "fase_5a",
    "GEN": "fase_gen",
}


def _canonical_fase_code(fase_actual: str) -> str:
    """Normaliza a código de fase estable ('0E', 'GEN', …) para BD y archivos."""
    raw = fase_actual.strip()
    low = raw.lower().replace(" ", "")
    if low.startswith("fase_"):
        suffix = low.removeprefix("fase_")
        if suffix == "gen":
            return "GEN"
        if len(suffix) == 2 and suffix[0].isdigit():
            return suffix.upper()
        return raw.upper()
    up = raw.upper()
    if up in _FASE_CODE_TO_STEM:
        return up
    return up


def _fase_prompt_filename(fase_actual: str) -> str:
    code = _canonical_fase_code(fase_actual)
    stem = _FASE_CODE_TO_STEM.get(code, f"fase_{code.lower()}")
    return f"{stem}.md"


def _read_text_file(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"No existe el archivo de prompt requerido: {path}")
    return path.read_text(encoding="utf-8")


def _fase_output_to_resumen_text(output: FaseOutput) -> str:
    c = output.contenido
    if isinstance(c, dict):
        if isinstance(c.get("resumen"), str):
            return c["resumen"]
        if isinstance(c.get("texto_resumen"), str):
            return c["texto_resumen"]
    return json.dumps(c, ensure_ascii=False)


def estimate_context_tokens(ctx: ContextoComprimido) -> int:
    """Estimación conservadora ~4 caracteres por token (español + JSON)."""
    bloques: list[str] = [
        ctx.prompt_maestro,
        "\n\n".join(ctx.resumenes_fases),
        json.dumps([h.model_dump(mode="json") for h in ctx.hechos_relevantes], ensure_ascii=False),
        json.dumps(ctx.ultimos_mensajes, ensure_ascii=False),
        ctx.prompt_fase,
    ]
    return sum(max(1, len(b) // 4) for b in bloques)


def _embed_query_text(text: str) -> list[float]:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY no está definida; es necesaria para la búsqueda semántica de hechos."
        )
    model = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")
    with httpx.Client(timeout=60.0) as client:
        r = client.post(
            "https://api.openai.com/v1/embeddings",
            headers={"Authorization": f"Bearer {api_key}"},
            json={"model": model, "input": text},
        )
        r.raise_for_status()
        data = r.json()
    return list(data["data"][0]["embedding"])


def _embedding_query_for_phase(fase_actual: str) -> str:
    code = _canonical_fase_code(fase_actual)
    return (
        f"Contexto jurídico fase {code}: hechos probatorios, narrativa, pruebas y riesgos "
        f"relevantes para esta etapa del razonamiento del caso."
    )


def _shrink_context_until_cap(ctx: ContextoComprimido, max_tokens: int) -> None:
    """
    Garantiza `estimate_context_tokens(ctx) <= max_tokens`.

    Orden: (1) reducir hechos a 5 si había más; (2) eliminar resúmenes de fase más antiguos;
    (3) eliminar mensajes más antiguos; (4) truncar el prompt de fase y luego el maestro.
    """
    while estimate_context_tokens(ctx) > max_tokens:
        if len(ctx.hechos_relevantes) > 5:
            ctx.hechos_relevantes = ctx.hechos_relevantes[:5]
            continue
        if len(ctx.resumenes_fases) > 1:
            ctx.resumenes_fases = ctx.resumenes_fases[1:]
            continue
        if len(ctx.ultimos_mensajes) > 1:
            ctx.ultimos_mensajes = ctx.ultimos_mensajes[1:]
            continue
        if len(ctx.prompt_fase) > 500:
            ctx.prompt_fase = ctx.prompt_fase[:-500]
            continue
        if len(ctx.prompt_maestro) > 500:
            ctx.prompt_maestro = ctx.prompt_maestro[:-500]
            continue
        break


def build_context(
    caso_id: UUID,
    fase_actual: str,
    *,
    max_tokens: int = 25_000,
    prompts_dir: Path | None = None,
) -> ContextoComprimido:
    """
    Construye `ContextoComprimido` según 3.5 / S2.1.

    Carga prompt maestro, resúmenes de fases aprobadas, hechos vía pgvector (RPC
    `match_hechos`), últimos 20 mensajes y prompt de la fase actual. Ajusta el
    contenido para no superar `max_tokens`.
    """
    base_dir = prompts_dir or _PROMPTS_DIR
    prompt_maestro = _read_text_file(base_dir / "sistema_base.md")

    outputs = db.get_outputs_fases(caso_id)
    resumenes_fases = [_fase_output_to_resumen_text(o) for o in outputs]

    query = _embedding_query_for_phase(fase_actual)
    embedding = _embed_query_text(query)
    hechos_relevantes = db.search_hechos_semanticos(caso_id, embedding, limit=10)

    ultimos_mensajes = db.get_ultimos_mensajes(caso_id, n=20)

    fase_name = _fase_prompt_filename(fase_actual)
    prompt_fase = _read_text_file(base_dir / fase_name)

    ctx = ContextoComprimido(
        prompt_maestro=prompt_maestro,
        resumenes_fases=resumenes_fases,
        hechos_relevantes=hechos_relevantes,
        ultimos_mensajes=ultimos_mensajes,
        prompt_fase=prompt_fase,
        total_tokens_est=0,
    )

    if estimate_context_tokens(ctx) > max_tokens:
        ctx.hechos_relevantes = ctx.hechos_relevantes[:5]

    _shrink_context_until_cap(ctx, max_tokens)
    ctx.total_tokens_est = estimate_context_tokens(ctx)
    return ctx


def build_context_managed(inp: ContextManagerInput, *, prompts_dir: Path | None = None) -> ContextoComprimido:
    """Variante que acepta `ContextManagerInput` (3.8)."""
    return build_context(inp.caso_id, inp.fase_actual, max_tokens=inp.max_tokens, prompts_dir=prompts_dir)


def _haiku_cost_usd(input_tokens: int, output_tokens: int) -> float:
    return (input_tokens / 1_000_000) * 0.25 + (output_tokens / 1_000_000) * 1.25


def compress_session(
    caso_id: UUID,
    fase: str,
    *,
    anthropic_model: str | None = None,
) -> FaseOutput:
    """
    Resume los mensajes de la fase aprobada (500–800 tokens objetivo) con Claude Haiku
    y persiste el resultado en `outputs_fases` vía `db.save_output_fase`.
    """
    from anthropic import Anthropic

    fase_code = _canonical_fase_code(fase)
    mensajes = db.get_mensajes_por_fase(caso_id, fase_code)
    if not mensajes:
        mensajes = db.get_ultimos_mensajes(caso_id, n=100)

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY no está definida; es necesaria para compress_session.")

    modelo = anthropic_model or os.environ.get("ANTHROPIC_MODEL_HAIKU", "claude-haiku-4-5")
    historial = json.dumps(mensajes, ensure_ascii=False, default=str)

    system = (
        "Eres un asistente que resume conversaciones jurídicas entre un abogado y LUMI. "
        "Produce un único resumen estructurado en español, entre 500 y 800 tokens de extensión, "
        "que conserve decisiones, vacíos probatorios, acuerdos y riesgos señalados. "
        "No inventes hechos; solo sintetiza lo dicho en los mensajes."
    )
    user = f"Mensajes JSON de la fase {fase_code}:\n{historial}"

    client = Anthropic(api_key=api_key)
    msg = client.messages.create(
        model=modelo,
        max_tokens=2_048,
        system=system,
        messages=[{"role": "user", "content": user}],
    )

    texto = ""
    for block in msg.content:
        if block.type == "text":
            texto += block.text

    usage = msg.usage
    input_tokens = int(usage.input_tokens)
    output_tokens = int(usage.output_tokens)
    total_tokens = input_tokens + output_tokens
    costo = _haiku_cost_usd(input_tokens, output_tokens)

    next_version = db.get_max_version_output_fase(caso_id, fase_code) + 1
    output = FaseOutput(
        caso_id=caso_id,
        fase=fase_code,
        version=next_version,
        contenido={
            "tipo": "resumen_sesion",
            "texto": texto.strip(),
            "fase": fase_code,
        },
        aprobado_abogado=False,
        anotaciones=None,
        tokens_usados=total_tokens,
        costo_usd=costo,
    )
    db.save_output_fase(output)
    return output
