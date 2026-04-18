"use client";

import { useCallback, useEffect, useState } from "react";

import type { MensajeHistorial } from "@/lib/api-client";
import { getChatHistorial } from "@/lib/api-client";

type ChatWindowProps = {
  casoId: string;
  refreshTrigger: number;
};

export function ChatWindow({ casoId, refreshTrigger }: ChatWindowProps) {
  const [mensajes, setMensajes] = useState<MensajeHistorial[]>([]);
  const [cargando, setCargando] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const cargar = useCallback(async () => {
    if (!casoId) {
      return;
    }
    setCargando(true);
    setError(null);
    try {
      const data = await getChatHistorial(casoId, 80);
      setMensajes(data);
    } catch (e) {
      setError(e instanceof Error ? e.message : "No se pudo cargar el historial.");
    } finally {
      setCargando(false);
    }
  }, [casoId]);

  useEffect(() => {
    void cargar();
  }, [cargar, refreshTrigger]);

  if (!casoId) {
    return null;
  }

  return (
    <div
      className="flex min-h-0 flex-1 flex-col gap-3 overflow-y-auto px-4 py-4"
      aria-label="Chat"
    >
      {cargando && (
        <p className="text-center text-sm text-neutral-500" role="status">
          Cargando conversación…
        </p>
      )}
      {error && (
        <p className="rounded-md bg-red-50 px-3 py-2 text-sm text-red-800" role="alert">
          {error}
        </p>
      )}
      {!cargando && !error && mensajes.length === 0 && (
        <p className="text-center text-sm text-neutral-500">Aún no hay mensajes en este caso.</p>
      )}
      {mensajes.map((m) => {
        const esAbogado = m.rol === "abogado";
        const esLumi = m.rol === "lumi";
        const alineacion = esAbogado ? "items-end" : "items-start";
        const bubble =
          esAbogado
            ? "rounded-2xl rounded-br-sm bg-primary text-white"
            : esLumi
              ? "rounded-2xl rounded-bl-sm border border-neutral-200 bg-white text-neutral-900"
              : "rounded-2xl border border-dashed border-neutral-300 bg-neutral-50 text-neutral-700";
        return (
          <div key={m.id ?? `${m.created_at}-${m.rol}-${m.contenido.slice(0, 24)}`} className={`flex w-full flex-col ${alineacion}`}>
            <div className={`max-w-[85%] px-4 py-2 text-sm shadow-sm ${bubble}`}>
              <p className="whitespace-pre-wrap break-words">{m.contenido}</p>
              <p className={`mt-1 text-[10px] uppercase tracking-wide ${esAbogado ? "text-blue-100" : "text-neutral-400"}`}>
                {m.rol}
                {m.fase ? ` · ${m.fase}` : ""}
              </p>
            </div>
          </div>
        );
      })}
    </div>
  );
}
