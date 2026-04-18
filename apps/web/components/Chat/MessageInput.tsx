"use client";

import { useState } from "react";

import { postChat } from "@/lib/api-client";

type MessageInputProps = {
  casoId: string;
  onMessageSent: () => void;
};

export function MessageInput({ casoId, onMessageSent }: MessageInputProps) {
  const [texto, setTexto] = useState("");
  const [enviando, setEnviando] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const enviar = async () => {
    const t = texto.trim();
    if (!t || !casoId || enviando) {
      return;
    }
    setEnviando(true);
    setError(null);
    try {
      await postChat(casoId, t);
      setTexto("");
      onMessageSent();
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo enviar el mensaje.");
    } finally {
      setEnviando(false);
    }
  };

  return (
    <div className="border-t border-neutral-200 bg-white p-3" aria-label="Entrada de mensaje">
      {error && (
        <p className="mb-2 text-sm text-red-700" role="alert">
          {error}
        </p>
      )}
      <div className="flex gap-2">
        <textarea
          className="min-h-[44px] flex-1 resize-y rounded-lg border border-neutral-300 px-3 py-2 text-sm text-neutral-900 outline-none ring-primary focus:border-primary focus:ring-1 disabled:bg-neutral-100"
          placeholder="Escriba su mensaje para LUMI…"
          rows={2}
          value={texto}
          disabled={enviando || !casoId}
          onChange={(e) => setTexto(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              void enviar();
            }
          }}
        />
        <button
          type="button"
          className="self-end rounded-lg bg-primary px-4 py-2 text-sm font-medium text-white transition hover:opacity-90 disabled:cursor-not-allowed disabled:opacity-50"
          disabled={enviando || !texto.trim() || !casoId}
          onClick={() => void enviar()}
        >
          {enviando ? "Enviando…" : "Enviar"}
        </button>
      </div>
    </div>
  );
}
