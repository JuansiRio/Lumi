"""Extracción de texto: PDF y DOCX (LlamaParse), imágenes (Claude Vision, Haiku). — S1.1."""

from __future__ import annotations

import base64
import os
from typing import Final

from llama_parse import LlamaParse, ResultType

from apps.agents.models.documento import DocumentoExtracto

MIME_PDF: Final[str] = "application/pdf"
MIME_DOCX: Final[str] = (
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
)
VISION_MIMES: Final[frozenset[str]] = frozenset(
    {
        "image/jpeg",
        "image/png",
        "image/webp",
    }
)
VISION_MODEL: Final[str] = "claude-haiku-4-5"


def _normalize_mime(mime_type: str) -> str:
    """Quita parámetros (`; charset=...`) y unifica variantes comunes."""
    base = mime_type.split(";", maxsplit=1)[0].strip().lower()
    if base == "image/jpg":
        return "image/jpeg"
    return base


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"{name} no está definida; es necesaria para parse_document.")
    return value


def _llama_synthetic_filename(mime_type: str) -> str:
    if mime_type == MIME_PDF:
        return "document.pdf"
    if mime_type == MIME_DOCX:
        return "document.docx"
    raise ValueError(f"mime_type inesperado para LlamaParse: {mime_type!r}")


def _parse_with_llama_parse(archivo_bytes: bytes, mime_type: str) -> DocumentoExtracto:
    api_key = _require_env("LLAMA_CLOUD_API_KEY")
    file_name = _llama_synthetic_filename(mime_type)
    parser = LlamaParse(
        api_key=api_key,
        result_type=ResultType.TXT,
        verbose=False,
        show_progress=False,
    )
    documents = parser.load_data(
        archivo_bytes,
        extra_info={"file_name": file_name},
    )
    if not documents:
        raise RuntimeError("LlamaParse no devolvió ningún fragmento de texto.")
    partes: list[str] = []
    for doc in documents:
        fragmento = (getattr(doc, "text", None) or "").strip()
        if fragmento:
            partes.append(fragmento)
    texto = "\n\n".join(partes).strip()
    metadatos: dict[str, object] = {
        "parser": "llama_parse",
        "mime_type": mime_type,
        "fragmentos": len(documents),
    }
    return DocumentoExtracto(texto_extraido=texto, metadatos=metadatos)


def _parse_with_claude_vision(archivo_bytes: bytes, mime_type: str) -> DocumentoExtracto:
    api_key = _require_env("ANTHROPIC_API_KEY")
    from anthropic import Anthropic

    b64 = base64.standard_b64encode(archivo_bytes).decode("ascii")
    client = Anthropic(api_key=api_key)
    ocr_prompt = (
        "Transcribe todo el texto visible en la imagen en orden de lectura natural. "
        "Conserva números, fechas y símbolos tal como aparecen. "
        "Si no hay texto legible, responde exactamente: [sin_texto_legible]. "
        "No añadas comentarios; solo el texto transcrito."
    )
    msg = client.messages.create(
        model=VISION_MODEL,
        max_tokens=8_192,
        system="Sigues la petición del usuario con fidelidad al contenido visible.",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
                            "data": b64,
                        },
                    },
                    {"type": "text", "text": ocr_prompt},
                ],
            }
        ],
    )
    texto_acumulado = ""
    for block in msg.content:
        if block.type == "text":
            texto_acumulado += block.text
    usage = msg.usage
    metadatos: dict[str, object] = {
        "parser": "claude_vision",
        "mime_type": mime_type,
        "model": VISION_MODEL,
        "input_tokens": int(usage.input_tokens),
        "output_tokens": int(usage.output_tokens),
    }
    return DocumentoExtracto(
        texto_extraido=texto_acumulado.strip(),
        metadatos=metadatos,
    )


def parse_document(archivo_bytes: bytes, mime_type: str) -> DocumentoExtracto:
    """
    Extrae texto de un archivo en memoria según su ``mime_type``.

    - ``application/pdf`` y DOCX Open XML → LlamaParse (``LLAMA_CLOUD_API_KEY``).
    - ``image/jpeg``, ``image/png``, ``image/webp`` → Claude Vision
      (``ANTHROPIC_API_KEY``, ``claude-haiku-4-5``).
    """
    if not isinstance(archivo_bytes, (bytes, bytearray)):
        raise TypeError("archivo_bytes debe ser bytes o bytearray.")
    data = bytes(archivo_bytes)
    if not data:
        raise ValueError("archivo_bytes está vacío.")

    mt = _normalize_mime(mime_type)
    if mt in (MIME_PDF, MIME_DOCX):
        return _parse_with_llama_parse(data, mt)
    if mt in VISION_MIMES:
        return _parse_with_claude_vision(data, mt)

    soportados = ", ".join(
        sorted({MIME_PDF, MIME_DOCX, *VISION_MIMES, "image/jpg"})
    )
    raise ValueError(
        f"mime_type no soportado: {mime_type!r}. Tipos soportados: {soportados}."
    )
