"""Documentos — endpoints Brief 3.4 (S0.3 sin lógica)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/casos", tags=["documentos"])


@router.post("/{caso_id}/documentos")
async def post_documentos(caso_id: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{caso_id}/documentos")
async def list_documentos(caso_id: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")
