"""Casos — endpoints Brief 3.4 (CRUD + helpers compartidos para otros routers)."""

from __future__ import annotations

import traceback
import logging

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel, Field, model_validator
from supabase import Client

from apps.agents.models.caso import Caso, EstadoCaso, TipoAccion
from apps.agents.tools.db import _supabase

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/casos", tags=["casos"])

FASES_VALIDAS: frozenset[str] = frozenset({"0E", "0A", "0C", "1A", "1C", "2A", "5A", "GEN"})


def _client() -> Client:
    try:
        return _supabase()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def require_user_uuid(x_user_id: str | None) -> UUID:
    if not x_user_id or not str(x_user_id).strip():
        raise HTTPException(status_code=400, detail="Falta el header X-User-ID.")
    try:
        return UUID(str(x_user_id).strip())
    except ValueError:
        raise HTTPException(status_code=400, detail="X-User-ID debe ser un UUID válido.")


def parse_caso_uuid(caso_id: str) -> UUID:
    try:
        return UUID(str(caso_id).strip())
    except ValueError:
        raise HTTPException(status_code=400, detail="El identificador del caso no es un UUID válido.")


def load_caso_row(client: Client, caso_uuid: UUID, user_uuid: UUID) -> dict[str, Any]:
    res = (
        client.table("casos")
        .select("*")
        .eq("id", str(caso_uuid))
        .eq("user_id", str(user_uuid))
        .limit(1)
        .execute()
    )
    rows = res.data or []
    if not rows:
        raise HTTPException(status_code=404, detail="No se encontró el caso o no tiene permiso para acceder.")
    return rows[0]


def row_to_caso(row: dict[str, Any]) -> Caso:
    return Caso(
        id=row["id"],
        nombre_caso=str(row["nombre_caso"]),
        tipo_accion=TipoAccion(row["tipo_accion"]),
        estado=EstadoCaso(row["estado"]),
        fase_actual=str(row["fase_actual"]),
        tokens_consumidos=int(row.get("tokens_consumidos", 0)),
        costo_usd=float(row.get("costo_usd", 0.0)),
        created_at=_parse_ts(row["created_at"]),
        updated_at=_parse_ts(row["updated_at"]),
    )


def _parse_ts(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise HTTPException(status_code=500, detail="Formato de fecha inválido en la base de datos.")


class CasoCreateRequest(BaseModel):
    nombre_caso: str = Field(min_length=1, max_length=500)
    tipo_accion: TipoAccion


class CasoPatchRequest(BaseModel):
    estado: EstadoCaso | None = None
    fase_actual: str | None = Field(default=None, max_length=32)

    @model_validator(mode="after")
    def al_menos_un_campo(self) -> CasoPatchRequest:
        if self.estado is None and self.fase_actual is None:
            raise ValueError("Debe enviar al menos estado o fase_actual.")
        return self


@router.post("/", status_code=201, response_model=Caso)
async def create_caso(
    body: CasoCreateRequest,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> Caso:
    try:
        user_uuid = require_user_uuid(x_user_id)
        client = _client()
        payload: dict[str, Any] = {
            "user_id": str(user_uuid),
            "nombre_caso": body.nombre_caso.strip(),
            "tipo_accion": body.tipo_accion.value,
            "estado": EstadoCaso.activo.value,
            "fase_actual": "0E",
            "tokens_consumidos": 0,
            "costo_usd": 0.0,
        }
        res = client.table("casos").insert(payload).select("*").limit(1).execute()
        rows = res.data or []
        if not rows:
            raise HTTPException(status_code=500, detail="No se pudo crear el caso (sin datos devueltos).")
        return row_to_caso(rows[0])
    except HTTPException:
        raise
    except Exception:
        error_detail = traceback.format_exc()
        logger.error(f"Error creando caso: {error_detail}")
        raise HTTPException(status_code=500, detail=error_detail)


@router.get("/", response_model=list[Caso])
async def list_casos(x_user_id: str | None = Header(default=None, alias="X-User-ID")) -> list[Caso]:
    user_uuid = require_user_uuid(x_user_id)
    client = _client()
    try:
        res = (
            client.table("casos")
            .select("*")
            .eq("user_id", str(user_uuid))
            .order("updated_at", desc=True)
            .execute()
        )
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo listar los casos.") from None
    rows = res.data or []
    return [row_to_caso(r) for r in rows]


@router.get("/{caso_id}", response_model=Caso)
async def get_caso(
    caso_id: str,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> Caso:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    row = load_caso_row(client, caso_uuid, user_uuid)
    return row_to_caso(row)


@router.patch("/{caso_id}", response_model=Caso)
async def update_caso(
    caso_id: str,
    body: CasoPatchRequest,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> Caso:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    load_caso_row(client, caso_uuid, user_uuid)
    update_payload: dict[str, Any] = {"updated_at": datetime.now(timezone.utc).isoformat()}
    if body.estado is not None:
        update_payload["estado"] = body.estado.value
    if body.fase_actual is not None:
        f = body.fase_actual.strip().upper()
        if f not in FASES_VALIDAS:
            raise HTTPException(
                status_code=400,
                detail=f"fase_actual no válida. Valores permitidos: {', '.join(sorted(FASES_VALIDAS))}.",
            )
        update_payload["fase_actual"] = f
    try:
        res = (
            client.table("casos")
            .update(update_payload)
            .eq("id", str(caso_uuid))
            .eq("user_id", str(user_uuid))
            .select("*")
            .limit(1)
            .execute()
        )
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo actualizar el caso.") from None
    rows = res.data or []
    if not rows:
        raise HTTPException(status_code=404, detail="No se encontró el caso o no tiene permiso para acceder.")
    return row_to_caso(rows[0])
