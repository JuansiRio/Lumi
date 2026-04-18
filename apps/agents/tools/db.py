"""Cliente Supabase — solo operaciones usadas por el Context Manager."""

from __future__ import annotations

import json
import os
from typing import Any
from uuid import UUID

from supabase import Client, create_client

from apps.agents.models.fase_output import FaseOutput
from apps.agents.models.hecho import EstatusEpistemico, Hecho


def _supabase() -> Client:
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or os.environ.get("SUPABASE_KEY", "")
    if not url or not key:
        raise RuntimeError(
            "SUPABASE_URL y SUPABASE_SERVICE_ROLE_KEY (o SUPABASE_KEY) deben estar definidos."
        )
    return create_client(url, key)


def _row_to_hecho(row: dict[str, Any]) -> Hecho:
    return Hecho(
        id=row["id"],
        caso_id=row["caso_id"],
        fase_origen=str(row.get("fase_origen", "")),
        contenido=str(row.get("contenido", "")),
        estatus_epistemico=EstatusEpistemico(row["estatus_epistemico"]),
        fuente=row.get("fuente"),
    )


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


def get_outputs_fases(caso_id: UUID) -> list[FaseOutput]:
    """Carga outputs de fase del caso con aprobación del abogado (solo aprobados)."""
    client = _supabase()
    res = (
        client.table("outputs_fases")
        .select("*")
        .eq("caso_id", str(caso_id))
        .eq("aprobado_abogado", True)
        .order("fase")
        .order("version")
        .execute()
    )
    rows = res.data or []
    return [_row_to_fase_output(r) for r in rows]


def get_ultimos_mensajes(caso_id: UUID, n: int = 20) -> list[dict[str, Any]]:
    """Últimos N mensajes de la sesión activa, del más antiguo al más reciente."""
    client = _supabase()
    res = (
        client.table("sesiones")
        .select("*")
        .eq("caso_id", str(caso_id))
        .order("created_at", desc=True)
        .limit(n)
        .execute()
    )
    rows: list[dict[str, Any]] = list(res.data or [])
    rows.reverse()
    return rows


def search_hechos_semanticos(
    caso_id: UUID,
    query_embedding: list[float],
    limit: int = 10,
) -> list[Hecho]:
    """
    Hechos más similares al embedding en el caso.

    Requiere la función RPC `match_hechos` en Postgres (pgvector).
    Si la RPC no existe o falla, hace fallback a los últimos `limit` hechos del caso.
    """
    client = _supabase()
    try:
        res = client.rpc(
            "match_hechos",
            {
                "query_embedding": query_embedding,
                "p_caso_id": str(caso_id),
                "match_count": limit,
            },
        ).execute()
        rows = res.data or []
        return [_row_to_hecho(r) for r in rows]
    except Exception:
        # RPC `match_hechos` ausente o error de red/pgvector: degradación controlada.
        res = (
            client.table("hechos")
            .select("*")
            .eq("caso_id", str(caso_id))
            .order("id", desc=True)
            .limit(limit)
            .execute()
        )
        rows = res.data or []
        rows.reverse()
        return [_row_to_hecho(r) for r in rows]


def save_sesion_mensaje(
    caso_id: UUID,
    rol: str,
    contenido: str,
    *,
    fase: str | None = None,
) -> None:
    """Inserta un mensaje en la sesión conversacional."""
    client = _supabase()
    payload: dict[str, Any] = {
        "caso_id": str(caso_id),
        "rol": rol,
        "contenido": contenido,
    }
    if fase is not None:
        payload["fase"] = fase
    client.table("sesiones").insert(payload).execute()


def get_max_version_output_fase(caso_id: UUID, fase: str) -> int:
    """Mayor número de versión existente para (caso_id, fase), o 0 si no hay filas."""
    client = _supabase()
    res = (
        client.table("outputs_fases")
        .select("version")
        .eq("caso_id", str(caso_id))
        .eq("fase", fase)
        .order("version", desc=True)
        .limit(1)
        .execute()
    )
    rows = res.data or []
    if not rows:
        return 0
    return int(rows[0]["version"])


def save_output_fase(output: FaseOutput) -> None:
    """Persiste un output de fase (insert)."""
    client = _supabase()
    payload: dict[str, Any] = {
        "caso_id": str(output.caso_id),
        "fase": output.fase,
        "version": output.version,
        "contenido": output.contenido,
        "aprobado_abogado": output.aprobado_abogado,
        "anotaciones": output.anotaciones,
        "tokens_usados": output.tokens_usados,
        "costo_usd": output.costo_usd,
    }
    client.table("outputs_fases").insert(payload).execute()


def get_mensajes_por_fase(caso_id: UUID, fase: str) -> list[dict[str, Any]]:
    """Mensajes de sesión asociados a una fase (columna `fase`), orden cronológico."""
    client = _supabase()
    res = (
        client.table("sesiones")
        .select("*")
        .eq("caso_id", str(caso_id))
        .eq("fase", fase)
        .order("created_at")
        .execute()
    )
    return list(res.data or [])


def save_documento(
    documento_id: UUID,
    caso_id: UUID,
    nombre_original: str,
    mime_type: str,
    *,
    texto_extraido: str | None,
    tipo_detectado: str | None,
    estado: str,
    storage_path: str | None = None,
) -> UUID:
    """
    Inserta o actualiza un registro en ``documentos`` por clave primaria ``documento_id``.

    ``estado`` debe ser uno de: pendiente, procesando, listo, error.
    """
    client = _supabase()
    payload: dict[str, Any] = {
        "id": str(documento_id),
        "caso_id": str(caso_id),
        "nombre_original": nombre_original,
        "mime_type": mime_type,
        "tipo_detectado": tipo_detectado,
        "estado": estado,
        "texto_extraido": texto_extraido,
        "storage_path": storage_path,
    }
    client.table("documentos").upsert(payload).execute()
    return documento_id


def save_hecho(
    caso_id: UUID,
    fase_origen: str,
    contenido: str,
    estatus_epistemico: EstatusEpistemico,
    *,
    fuente: str | None = None,
) -> UUID:
    """Inserta un hecho y devuelve su ``id``."""
    client = _supabase()
    payload: dict[str, Any] = {
        "caso_id": str(caso_id),
        "fase_origen": fase_origen,
        "contenido": contenido,
        "estatus_epistemico": estatus_epistemico.value,
        "fuente": fuente,
    }
    res = client.table("hechos").insert(payload).execute()
    rows = res.data or []
    if not rows or rows[0].get("id") is None:
        raise RuntimeError("Supabase no devolvió el id del hecho insertado.")
    return UUID(str(rows[0]["id"]))


def log_trazabilidad(
    caso_id: UUID,
    agente: str,
    modelo: str,
    tokens_input: int,
    tokens_output: int,
    duracion_ms: int,
    costo_usd: float,
) -> None:
    """Registra una llamada a API (Anthropic) en la tabla ``trazabilidad``."""
    client = _supabase()
    client.table("trazabilidad").insert(
        {
            "caso_id": str(caso_id),
            "agente": agente,
            "modelo": modelo,
            "tokens_input": int(tokens_input),
            "tokens_output": int(tokens_output),
            "duracion_ms": int(duracion_ms),
            "costo_usd": float(costo_usd),
        }
    ).execute()
