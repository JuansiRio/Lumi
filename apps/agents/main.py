"""Entry point FastAPI — LUMI Judicial agents (S0.3)."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import casos, chat, documentos, fases

app = FastAPI(title="LUMI Judicial — Agents", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(casos.router)
app.include_router(chat.router)
app.include_router(documentos.router)
app.include_router(fases.router)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "version": "0.1.0"}
