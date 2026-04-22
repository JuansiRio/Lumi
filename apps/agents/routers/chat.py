"""Chat — endpoints Brief 3.4 (LUMI Core + historial)."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException, Query
from pydantic import BaseModel, Field

from apps.agents.core.lumi_core import process_message
from apps.agents.models.fase_output import LumiCoreInput, LumiCoreResponse
from apps.agents.tools.db import _supabase

from routers.casos import load_caso_row, parse_caso_uuid, require_user_uuid

router = APIRouter(prefix="/casos", tags=["chat"])


def _client():
    try:
        return _supabase()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


class ChatMensajeRequest(BaseModel):
    mensaje: str = Field(min_length=1, max_length=50_000)


class MensajeHistorialItem(BaseModel):
    id: str | None = None
    rol: str
    contenido: str
    fase: str | None = None
    created_at: datetime | None = None


def _row_sesion_to_item(row: dict[str, Any]) -> MensajeHistorialItem:
    cid = row.get("id")
    return MensajeHistorialItem(
        id=str(cid) if cid is not None else None,
        rol=str(row.get("rol", "")),
        contenido=str(row.get("contenido", "")),
        fase=row.get("fase"),
        created_at=_parse_created(row.get("created_at")),
    )


def _parse_created(value: Any) -> datetime | None:
    if value is None:
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    return None


def _increment_caso_tokens(client: Any, caso_uuid: UUID, tokens: int, costo: float) -> None:
    row = client.table("casos").select("tokens_consumidos", "costo_usd").eq("id", str(caso_uuid)).limit(1).execute()
    rows = row.data or []
    if not rows:
        return
    prev_tok = int(rows[0].get("tokens_consumidos", 0))
    prev_cost = float(rows[0].get("costo_usd", 0.0))
    from datetime import datetime, timezone

    client.table("casos").update(
        {
            "tokens_consumidos": prev_tok + int(tokens),
            "costo_usd": round(prev_cost + float(costo), 6),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("id", str(caso_uuid)).execute()


@router.post("/{caso_id}/chat", response_model=LumiCoreResponse)
async def post_chat(
    caso_id: str,
    body: ChatMensajeRequest,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> LumiCoreResponse:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    row = load_caso_row(client, caso_uuid, user_uuid)
    fase_actual = str(row["fase_actual"])
    inp = LumiCoreInput(caso_id=caso_uuid, mensaje=body.mensaje, fase_actual=fase_actual)
    try:
        out: LumiCoreResponse = await asyncio.to_thread(process_message, inp)
    except HTTPException:
        raise
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        raise HTTPException(
            status_code=500,
            detail="No se pudo procesar el mensaje con LUMI Core. Verifique la configuración del servicio.",
        ) from None
    try:
        _increment_caso_tokens(client, caso_uuid, out.tokens_usados, out.costo_usd)
    except Exception:
        pass
    return out


@router.get("/{caso_id}/chat/historial", response_model=list[MensajeHistorialItem])
async def get_chat_historial(
    caso_id: str,
    n: int = Query(default=50, ge=1, le=200),
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> list[MensajeHistorialItem]:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    load_caso_row(client, caso_uuid, user_uuid)
    try:
        res = (
            client.table("sesiones")
            .select("*")
            .eq("caso_id", str(caso_uuid))
            .order("created_at", desc=True)
            .limit(n)
            .execute()
        )
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo cargar el historial de chat.") from None
    rows: list[dict[str, Any]] = list(res.data or [])
    rows.reverse()
    return [_row_sesion_to_item(r) for r in rows]
