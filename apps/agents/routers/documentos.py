"""Documentos — endpoints Brief 3.4 (upload + extractor + listado)."""

from __future__ import annotations

import asyncio
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

from fastapi import APIRouter, File, Header, HTTPException, UploadFile
from pydantic import BaseModel, Field

from apps.agents.models.documento import Documento, EstadoDocumento
from apps.agents.models.documento import ExtractorInput
from apps.agents.subagents.extractor import run as run_extractor
from apps.agents.tools import db
from apps.agents.tools.db import _supabase

from routers.casos import load_caso_row, parse_caso_uuid, require_user_uuid

router = APIRouter(prefix="/casos", tags=["documentos"])


def _client():
    try:
        return _supabase()
    except RuntimeError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


def _row_to_documento(row: dict[str, Any]) -> Documento:
    return Documento(
        id=row["id"],
        caso_id=row["caso_id"],
        nombre_original=str(row.get("nombre_original", "")),
        mime_type=str(row.get("mime_type", "")),
        tipo_detectado=row.get("tipo_detectado"),
        estado=EstadoDocumento(row.get("estado", "pendiente")),
        texto_extraido=row.get("texto_extraido"),
        storage_path=row.get("storage_path"),
        created_at=_parse_ts(row["created_at"]),
        updated_at=_parse_ts(row["updated_at"]),
    )


def _parse_ts(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        return datetime.fromisoformat(value.replace("Z", "+00:00"))
    raise HTTPException(status_code=500, detail="Formato de fecha inválido en documentos.")


class DocumentoUploadResponse(BaseModel):
    documento: Documento
    tokens_usados: int = Field(ge=0)
    costo_usd: float = Field(ge=0.0)


def _increment_caso_tokens_client(client: Any, caso_uuid: UUID, tokens: int, costo: float) -> None:
    row = client.table("casos").select("tokens_consumidos", "costo_usd").eq("id", str(caso_uuid)).limit(1).execute()
    rows = row.data or []
    if not rows:
        return
    from datetime import timezone

    prev_tok = int(rows[0].get("tokens_consumidos", 0))
    prev_cost = float(rows[0].get("costo_usd", 0.0))
    client.table("casos").update(
        {
            "tokens_consumidos": prev_tok + int(tokens),
            "costo_usd": round(prev_cost + float(costo), 6),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("id", str(caso_uuid)).execute()


@router.post("/{caso_id}/documentos", status_code=201, response_model=DocumentoUploadResponse)
async def post_documentos(
    caso_id: str,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
    file: UploadFile = File(...),
) -> DocumentoUploadResponse:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    load_caso_row(client, caso_uuid, user_uuid)

    nombre = (file.filename or "documento").strip() or "documento"
    mime = (file.content_type or "application/octet-stream").strip()
    doc_id = uuid4()

    try:
        raw = await file.read()
    except Exception:
        raise HTTPException(status_code=400, detail="No se pudo leer el archivo subido.") from None
    if not raw:
        raise HTTPException(status_code=400, detail="El archivo está vacío.")

    try:
        db.save_documento(
            doc_id,
            caso_uuid,
            nombre,
            mime,
            texto_extraido=None,
            tipo_detectado=None,
            estado="procesando",
            storage_path=None,
        )
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo registrar el documento.") from None

    inp = ExtractorInput(documento_id=doc_id, caso_id=caso_uuid, archivo_bytes=raw, mime_type=mime)
    try:
        ext_out = await asyncio.to_thread(run_extractor, inp)
    except RuntimeError as exc:
        try:
            db.save_documento(
                doc_id,
                caso_uuid,
                nombre,
                mime,
                texto_extraido=None,
                tipo_detectado=None,
                estado="error",
                storage_path=None,
            )
        except Exception:
            pass
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception:
        try:
            db.save_documento(
                doc_id,
                caso_uuid,
                nombre,
                mime,
                texto_extraido=None,
                tipo_detectado=None,
                estado="error",
                storage_path=None,
            )
        except Exception:
            pass
        raise HTTPException(status_code=500, detail="Falló la extracción del documento.") from None

    try:
        _increment_caso_tokens_client(client, caso_uuid, ext_out.tokens_usados, ext_out.costo_usd)
    except Exception:
        pass

    try:
        res = client.table("documentos").select("*").eq("id", str(doc_id)).limit(1).execute()
        rows = res.data or []
        if not rows:
            raise HTTPException(status_code=500, detail="Documento procesado pero no se pudo leer el registro.")
        doc = _row_to_documento(rows[0])
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo recuperar el documento tras el procesamiento.") from None

    return DocumentoUploadResponse(documento=doc, tokens_usados=ext_out.tokens_usados, costo_usd=ext_out.costo_usd)


@router.get("/{caso_id}/documentos", response_model=list[Documento])
async def list_documentos(
    caso_id: str,
    x_user_id: str | None = Header(default=None, alias="X-User-ID"),
) -> list[Documento]:
    user_uuid = require_user_uuid(x_user_id)
    caso_uuid = parse_caso_uuid(caso_id)
    client = _client()
    load_caso_row(client, caso_uuid, user_uuid)
    try:
        res = (
            client.table("documentos")
            .select("*")
            .eq("caso_id", str(caso_uuid))
            .order("created_at", desc=True)
            .execute()
        )
    except Exception:
        raise HTTPException(status_code=500, detail="No se pudo listar los documentos.") from None
    rows = res.data or []
    return [_row_to_documento(r) for r in rows]
