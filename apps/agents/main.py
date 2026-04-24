"""Entry point FastAPI — LUMI Judicial agents (S0.3)."""

from pathlib import Path
import os
import sys

_here = Path(__file__).resolve().parent
# En local: .../apps/agents → subir 2 niveles para imports absolutos
# En Railway: /app → ya está en el directorio correcto
_candidates = [
    _here.parents[1],  # local: raíz del repo
    _here,             # Railway: /app
]
for _candidate in _candidates:
    if str(_candidate) not in sys.path:
        sys.path.insert(0, str(_candidate))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import casos, chat, documentos, fases

app = FastAPI(title="LUMI Judicial — Agents", version="0.1.0")

CORS_ORIGINS = os.environ.get(
    "CORS_ORIGINS",
    "http://localhost:3000"
)
CORS_ORIGINS = [o.strip() for o in CORS_ORIGINS.split(",") if o.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
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
