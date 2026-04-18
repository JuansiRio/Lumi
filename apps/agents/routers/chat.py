"""Chat — endpoints Brief 3.4 (S0.3 sin lógica)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/casos", tags=["chat"])


@router.post("/{caso_id}/chat")
async def post_chat(caso_id: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")


@router.get("/{caso_id}/chat/historial")
async def get_chat_historial(caso_id: str) -> None:
    raise HTTPException(status_code=501, detail="Not implemented")
