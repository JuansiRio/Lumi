"""Casos — endpoints Brief 3.4 (S0.3 sin lógica)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/casos", tags=["casos"])


@router.post("/")
async def create_caso() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/")
async def list_casos() -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{caso_id}")
async def get_caso(caso_id: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.patch("/{caso_id}")
async def update_caso(caso_id: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{caso_id}/borrador")
async def get_borrador(caso_id: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{caso_id}/costos")
async def get_costos(caso_id: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")
