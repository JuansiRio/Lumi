"""Fases — endpoints Brief 3.4 (S0.3 sin lógica)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/casos", tags=["fases"])


@router.post("/{caso_id}/fases/{fase}/aprobar")
async def aprobar_fase(caso_id: str, fase: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{caso_id}/fases")
async def list_outputs_fases(caso_id: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")
