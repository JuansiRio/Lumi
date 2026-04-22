"""Fases — aprobación, outputs, borrador Word y costos (Brief 3.4)."""

from __future__ import annotations

import asyncio
import json
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field

from apps.agents.core.context_manager import _canonical_fase_code, compress_session
from apps.agents.models.fase_output import FaseOutput, WordGeneratorInput
from apps.agents.models.hecho import EstatusEpistemico, Hecho
from apps.agents.tools.db import _supabase
from apps.agents.tools.word_generator import generate_word_document

from routers.casos import load_caso_row, parse_caso_uuid, require_user_uuid, row_to_caso

router = APIRouter(prefix="/casos", tags=["fases"])

FASE_SEQUENCE: tuple[str, ...] = ("0E", "0A", "0C", "1A", "1C", "2A", "5A", "GEN")


def _client():
    try:
        return _supabase()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def _row_to_fase_output(row: dict[str, Any]) -> FaseOutput:
    contenido = row.get("contenido")
    if isinstance(contenido, str):
        contenido = json.loads(contenido)
    if contenido is None:
        contenido = {}
    return FaseOutput(
        caso_id=row["caso_id"],
        fase=str(row["fase"]),
        version=int(row["version"]),
        contenido=contenido,
        aprobado_abogado=bool(row.get("aprobado_abogado", False)),
        anotaciones=row.get("anotaciones"),
        tokens_usados=int(row.get("tokens_usados", 0)),
        costo_usd=float(row.get("costo_usd", 0.0)),
    )


def _row_to_hecho(row: dict[str, Any]) -> Hecho:
    return Hecho(
        id=row["id"],
        caso_id=row["caso_id"],
        fase_origen=str(row.get("fase_origen", "")),
        contenido=str(row.get("contenido", "")),
        estatus_epistemico=EstatusEpistemico(row["estatus_epistemico"]),
        fuente=row.get("fuente"),
    )


def _next_fase(code: str) -> str | None:
    c = _canonical_fase_code(code)
    if c not in FASE_SEQUENCE:
        return None
    i = FASE_SEQUENCE.index(c)
    if i + 1 >= len(FASE_SEQUENCE):
        return None
    return FASE_SEQUENCE[i + 1]


def _increment_caso_tokens(client: Any, caso_uuid: UUID, tokens: int, costo: float) -> None:
    row = client.table("casos").select("tokens_consumidos", "costo_usd").eq("id", str(caso_uuid)).limit(1).execute()
    rows = row.data or []
    if not rows:
        return
    prev_tok = int(rows[0].get("tokens_consumidos", 0))
    prev_cost = float(rows[0].get("costo_usd", 0.0))
    client.table("casos").update(
        {
            "tokens_consumidos": prev_tok + int(tokens),
            "costo_usd": round(prev_cost + float(costo), 6),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("id", str(caso_uuid)).execute()


class AprobarFaseResponse(BaseModel):
    fase_aprobada: str
    nueva_fase_actual: str
    tokens_resumen: int = Field(ge=0)
    costo_resumen_usd: float = Field(ge=0.0)


class CostosResumen(BaseModel):
    tokens_input_trazabilidad: int
    tokens_output_trazabilidad: int
    tokens_total_trazabilidad: int
    costo_usd_trazabilidad: float
    tokens_consumidos_caso: int
    costo_usd_caso: float


@router.post("/{caso_id}/fases/{fase}/aprobar", response_model=AprobarFaseResponse)
async def aprobar_fase(
    caso_id: str,
    fase: str,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> AprobarFaseResponse:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    row = load_caso_row(client, caso_uuid, user_uuid)
    fase_url = _canonical_fase_code(fase)
    fase_caso = _canonical_fase_code(str(row["fase_actual"]))
    if fase_url != fase_caso:
        raise HTTPException(
            status_code=400,
            detail=f"Solo puede aprobar la fase actual del caso ({fase_caso}).",
        )
    try:
        resumen: FaseOutput = await asyncio.to_thread(compress_session, caso_uuid, fase_url)
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo comprimir la sesión de la fase.") from None

    try:
        client.table("outputs_fases").update({"aprobado_abogado": True}).eq("caso_id", str(caso_uuid)).eq(
            "fase", fase_url
        ).execute()
    except Exception:
        pass

    siguiente = _next_fase(fase_url) or fase_url
    try:
        client.table("casos").update(
            {
                "fase_actual": siguiente,
                "updated_at": datetime.now(timezone.utc).isoformat(),
            }
        ).eq("id", str(caso_uuid)).eq("user_id", str(user_uuid)).execute()
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo actualizar la fase del caso.") from None

    try:
        _increment_caso_tokens(client, caso_uuid, resumen.tokens_usados, resumen.costo_usd)
    except Exception:
        pass

    return AprobarFaseResponse(
        fase_aprobada=fase_url,
        nueva_fase_actual=siguiente,
        tokens_resumen=resumen.tokens_usados,
        costo_resumen_usd=resumen.costo_usd,
    )


@router.get("/{caso_id}/fases", response_model=list[FaseOutput])
async def list_outputs_fases(
    caso_id: str,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> list[FaseOutput]:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    load_caso_row(client, caso_uuid, user_uuid)
    try:
        res = (
            client.table("outputs_fases")
            .select("*")
            .eq("caso_id", str(caso_uuid))
            .order("fase")
            .order("version")
            .execute()
        )
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo cargar los outputs de fases.") from None
    rows = res.data or []
    return [_row_to_fase_output(r) for r in rows]


def _latest_outputs_by_fase(rows: list[dict[str, Any]]) -> dict[str, FaseOutput]:
    best: dict[str, tuple[int, FaseOutput]] = {}
    for r in rows:
        fo = _row_to_fase_output(r)
        key = str(fo.fase)
        prev = best.get(key)
        if prev is None or fo.version > prev[0]:
            best[key] = (fo.version, fo)
    return {k: v[1] for k, v in best.items()}


@router.get("/{caso_id}/borrador")
async def get_borrador(
    caso_id: str,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> Response:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    row = load_caso_row(client, caso_uuid, user_uuid)
    meta = row_to_caso(row)
    try:
        out_rows = (
            client.table("outputs_fases").select("*").eq("caso_id", str(caso_uuid)).order("fase").order("version").execute()
        )
        he_rows = client.table("hechos").select("*").eq("caso_id", str(caso_uuid)).order("created_at").execute()
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo cargar datos para el borrador.") from None
    outputs_map = _latest_outputs_by_fase(list(out_rows.data or []))
    hechos = [_row_to_hecho(h) for h in (he_rows.data or [])]
    inp = WordGeneratorInput(
        caso_id=caso_uuid,
        outputs_fases=outputs_map,
        hechos=hechos,
        metadata_caso=meta,
    )
    try:
        word_out = await asyncio.to_thread(generate_word_document, inp)
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo generar el documento Word.") from None
    return Response(
        content=word_out.archivo_bytes,
        media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        headers={"Content-Disposition": f'attachment; filename="{word_out.nombre_archivo}"'},
    )


@router.get("/{caso_id}/costos", response_model=CostosResumen)
async def get_costos(
    caso_id: str,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> CostosResumen:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    row = load_caso_row(client, caso_uuid, user_uuid)
    try:
        t_res = client.table("trazabilidad").select("tokens_input", "tokens_output", "costo_usd").eq("caso_id", str(caso_uuid)).execute()
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo cargar la trazabilidad de costos.") from None
    tin = tout = 0
    costo_sum = 0.0
    for r in t_res.data or []:
        tin += int(r.get("tokens_input", 0))
        tout += int(r.get("tokens_output", 0))
        costo_sum += float(r.get("costo_usd", 0.0))
    return CostosResumen(
        tokens_input_trazabilidad=tin,
        tokens_output_trazabilidad=tout,
        tokens_total_trazabilidad=tin + tout,
        costo_usd_trazabilidad=round(costo_sum, 6),
        tokens_consumidos_caso=int(row.get("tokens_consumidos", 0)),
        costo_usd_caso=float(row.get("costo_usd", 0.0)),
    )
